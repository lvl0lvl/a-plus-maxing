"""The out-of-band alpha-build config loader + the D5 shared-key provisioning bridge.

The alpha build lets a tester connect a wearable and reach the model without registering
their own OAuth apps or buying their own key: it distributes SHARED vendor OAuth credentials
(`client_id`/`client_secret` per confidential-client vendor) and an optional SHARED Anthropic
key. Those are global-revoke secrets on a PUBLIC repo, so they are distributed OUT OF BAND —
a config file on a path named by an env var (`APLUS_ALPHA_CONFIG`), OUTSIDE the repo tree,
never a tracked file (D4). `load_alpha_config()` reads it; with the env var unset it returns
an EMPTY config so connect degrades to per-vendor manual/skip rather than failing.

The D5 provisioning bridge (`provision_shared_key`) makes the shared Anthropic key the
"touch nothing" DEFAULT: it exports the shared key onto the env-first key path
(`ANTHROPIC_API_KEY`) ONLY when no bring-your-own key already resolves — so a BYO key (in the
env or the keychain) is never clobbered. It sets the env var and nothing else — no keychain
write, no model call.

Trust boundary (SEC-4 — stated assumptions, not code defects):
  * At rest, the out-of-band file holds the shared `client_secret` + shared key in PLAINTEXT;
    its file-permission protection is scoped to the operator/distribution and verified at the
    LIVE run (bead `a-plus-maxing-m8ia`), not enforced here.
  * The loader reads its config from an env-var-NAMED path, so an attacker who controls that
    env var points the loader (and the bridge's export) at an attacker-supplied key. Under the
    per-user-local-instance model this reduces to "the attacker already has the user's
    code-exec" (accepted).
"""

import enum
import json
import os
from dataclasses import dataclass
from pathlib import Path

from scripts.model import key_source

# The out-of-band pointer: an env var NAMING the config file's path (the file itself is never
# tracked). Matches the project's `APLUS_*` runtime-config env convention (APLUS_DATA_ROOT).
ALPHA_CONFIG_ENV = "APLUS_ALPHA_CONFIG"


class ClientType(enum.Enum):
    """How a vendor's OAuth client is provisioned in the one-click alpha connect flow.

    CONFIDENTIAL uses the shared `client_secret`; PKCE_PUBLIC needs no secret; PAT is the
    tester's own pasted token; EXCLUDED_FROM_ONE_CLICK renders the manual/deferred path
    (Garmin's OAuth-1.0a); MANUAL is the fallback for a vendor absent from the map.
    """

    CONFIDENTIAL = "confidential"
    PKCE_PUBLIC = "pkce-public"
    PAT = "pat"
    EXCLUDED_FROM_ONE_CLICK = "excluded-from-one-click"
    MANUAL = "manual"


# The grounded default per-vendor client-type set. Whoop-confidential + Garmin-excluded are
# HARD-grounded (spec:157 "≥Whoop confidential-client"; spec:31 Garmin OAuth-1.0a excluded);
# google-pkce + oura-pat are OQ-5 placeholders verified at LIVE dev-app registration (bead
# `a-plus-maxing-m8ia`). The map is DATA (a dict), extended via the `client_types` seam — so
# OQ-5 registration adds/edits a vendor row without a per-vendor code branch (AC-2).
DEFAULT_CLIENT_TYPES = {
    "whoop": ClientType.CONFIDENTIAL,
    "google": ClientType.PKCE_PUBLIC,
    "oura": ClientType.PAT,
    "garmin": ClientType.EXCLUDED_FROM_ONE_CLICK,
}


class AlphaConfigError(RuntimeError):
    """Loading the out-of-band alpha config failed.

    Raised fail-loud for an in-repo config path (the config must be out-of-band) or a
    present-but-malformed config file. The message is CONSTANT and never carries a secret
    value — a config error must not leak the shared secret into a traceback (the repo is
    PUBLIC).
    """


@dataclass(frozen=True)
class VendorCredential:
    """A shared OAuth credential for one confidential-client vendor.

    Attributes:
        client_id (str): The shared app's client id.
        client_secret (str | None): The shared client secret (None for a non-confidential
            vendor that carries no secret).
    """

    client_id: str
    client_secret: str | None


@dataclass(frozen=True)
class AlphaConfig:
    """The loaded alpha config: shared vendor creds + optional shared key + the type map.

    Attributes:
        vendors (dict): Vendor name -> its shared `VendorCredential` (empty when the config
            is absent).
        shared_api_key (str | None): The optional shared Anthropic key (None when absent).
        client_types (dict): Vendor name -> its `ClientType` (the data-driven map).
    """

    vendors: dict
    shared_api_key: str | None
    client_types: dict

    def client_type(self, vendor):
        """Resolve a vendor's client type; a vendor absent from the map is MANUAL (AR-005).

        Args:
            vendor (str): The vendor name.

        Returns:
            (ClientType) The vendor's client type, or `ClientType.MANUAL` when unmapped.
        """
        return self.client_types.get(vendor, ClientType.MANUAL)


def _repo_root():
    """Return the repo root, anchored on the nearest `.git` (not a fragile fixed offset).

    Walks up from this module toward the filesystem root and returns the first ancestor
    holding a `.git` entry (a dir in a normal checkout, a file in a worktree). Falls back to
    the pinned `scripts/serve/alpha_config.py -> parents[2]` offset if none is found.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists():
            return parent
    return here.parents[2]


def _within_repo(candidate):
    """Whether a config path resolves INSIDE the repo tree — case-folded (SEC-1).

    `Path.resolve()` does not case-fold on a case-insensitive filesystem (the operator's
    APFS host), so a lexical `is_relative_to` misses an in-tree path with a case-variant
    segment (`A-PLUS-MAXING/...`) that is nonetheless physically reachable. Case-folding
    BOTH operands with `str.casefold()` (NOT `os.path.normcase`, a POSIX no-op) closes that
    bypass while staying component-wise, so a sibling sharing a prefix (`a-plus-maxing-evil`)
    is not falsely matched.

    Args:
        candidate (str | Path): The config path to test.

    Returns:
        (bool) True when the resolved path is inside the repo tree.
    """
    resolved = Path(candidate).resolve()
    root = _repo_root()
    return Path(str(resolved).casefold()).is_relative_to(Path(str(root).casefold()))


def load_alpha_config(path=None, *, client_types=None):
    """Load the out-of-band alpha config, or an EMPTY config when it is not configured.

    The config path comes from `path` when given, else the `APLUS_ALPHA_CONFIG` env var. With
    neither set, returns an empty config (0 vendor creds, no shared key) so connect degrades
    to per-vendor manual/skip. An in-repo config path RAISES (case-folded, SEC-1) — the config
    can only be out-of-band. A present-but-malformed file RAISES fail-loud with a constant
    message (distinct from the unset-degrade), so a mis-supplied config is not silently empty.

    Args:
        path (str | Path, optional): An explicit config path; overrides the env var (and is
            subject to the same in-repo reject — not a bypass, A-F4). Defaults to the env var.
        client_types (dict, optional): A per-vendor client-type override (the AC-2 data seam);
            defaults to `DEFAULT_CLIENT_TYPES`.

    Returns:
        (AlphaConfig) The loaded config, or an empty config when unconfigured.

    Raises:
        AlphaConfigError: The config path is in-repo, or the file is present but unreadable
            or malformed — constant message, no secret value.
    """
    types = DEFAULT_CLIENT_TYPES if client_types is None else client_types
    source = path if path is not None else os.environ.get(ALPHA_CONFIG_ENV)
    if source is None:
        return AlphaConfig(vendors={}, shared_api_key=None, client_types=types)

    if _within_repo(source):
        raise AlphaConfigError(
            "Refusing to load the alpha config from inside the repo tree; the shared "
            "credentials must live out-of-band (never a tracked file)."
        )

    try:
        raw = json.loads(Path(source).read_text(encoding="utf-8"))
        # Validate value types INSIDE the try: a non-string is caught by the except below and
        # re-raised as the CONSTANT AlphaConfigError (AR-003 total fail-loud) — not a deferred
        # raw TypeError at the bridge (`os.environ[...] = <dict>`), and no secret in the message.
        vendors = {}
        for name, entry in raw.get("vendors", {}).items():
            client_id = entry["client_id"]
            client_secret = entry.get("client_secret")
            if not isinstance(client_id, str):
                raise TypeError("client_id must be a string")
            if client_secret is not None and not isinstance(client_secret, str):
                raise TypeError("client_secret must be a string or None")
            vendors[name] = VendorCredential(client_id=client_id, client_secret=client_secret)
        shared_api_key = raw.get("shared_api_key")
        if shared_api_key is not None and not isinstance(shared_api_key, str):
            raise TypeError("shared_api_key must be a string or None")
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        raise AlphaConfigError(
            "Could not read the out-of-band alpha config; the file is missing or malformed."
        ) from None

    return AlphaConfig(vendors=vendors, shared_api_key=shared_api_key, client_types=types)


def provision_shared_key(config, *, resolve=key_source.resolve):
    """Export the shared Anthropic key onto the env-first key path when no BYO key resolves.

    Attempts `resolve`; ONLY when it raises `KeyUnavailableError` (no bring-your-own key in
    the env or the keychain) and the config carries a shared key, exports that key as
    `os.environ["ANTHROPIC_API_KEY"]`, so the env-first branch resolves it on the next call
    with no keychain write. A BYO key makes `resolve` return without raising, so the bridge
    no-ops and never clobbers it — the shared key is the DEFAULT, not an override. Makes no
    model call and never logs the key value (the repo is PUBLIC).

    Args:
        config (AlphaConfig): The loaded config carrying the optional shared key.
        resolve (Callable, optional): The key-resolution seam; defaults to `key_source.resolve`.
            Tests inject `partial(key_source.resolve, keychain_runner=<empty>)` so the
            env-first branch stays real while the keychain shell-out is faked.
    """
    try:
        resolve()
    except key_source.KeyUnavailableError:
        if config.shared_api_key:
            os.environ[key_source.ENV_VAR] = config.shared_api_key
