"""By-data-class capture seam tests (ADR-0014-T1).

`scripts/serve/capture.py`'s `persist_capture` routes each submitted form field by
its data class (the recipe's Grounded Field Map): a de-identified `SUMMARY_FIELD_SET`
token -> the store via the UNCHANGED `store.append` tagged `source:"intake"`; a
raw/record-only value -> the gitignored `vault/scaffold/filled/` operator record;
never a raw value into a field-set store item.

Cycle 1 — AC-1 per-wired-field round-trip (each wired token -> `store.read` tagged
`source:"intake"` -> `summarize` returns it under the token), AC-6 curated-token-only
`rx-interaction-classes`, and the Risk Negative-1 setup (a Step-3 "train around"
capture writes a `raw-symptom-free-text` item that `summarize` DERIVES into
`active-issue-class`, never the raw text).

Cycle 3 — the PII-boundary proofs: the fresh-clone tracked-tree scan returns 0
operator tokens after a full capture session, `summarize` RAISES on a raw-PII value
planted into a field-set item, and `block-pii-commit` would DENY a staged filled
scaffold. Each gate carries its negative control proving it is failing-capable.
"""

import functools
import subprocess
import sys
from pathlib import Path

from scripts.guard import pii_scan
from scripts.plan.router import SUMMARY_FIELD_SET, summarize
from scripts.serve import capture
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# An identity config that is ABSENT on disk: identity-token detection is empty (the
# operator's real name/contact are not in the tree), while the value-class patterns
# (any-domain email, phone, postal) still run — exactly the fresh-clone posture.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def _bound(root):
    """The instance-bound store_read `summarize` requires (recipe caller contract)."""
    return functools.partial(store.read, root=root)


def _summary(root):
    """Run `summarize` over a tmp instance with an absent identity config."""
    return summarize(_bound(root), identity_config=_ABSENT_IDENTITY)


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-1 per-wired-field round-trip
# --------------------------------------------------------------------------- #

# The de-identified wired tokens this task captures, each with a synthetic value
# that is a valid de-identified token (no raw PII) and is distinctive enough that a
# cross-stream leak would be detectable.
_WIRED_VALUES = {
    "goal-domains": "strength;recovery",
    "goal-targets": "add 10 lb to squat by september",
    "goal-priority-order": "1-strength;2-recovery;3-longevity",
    "hard-limits": "no overhead pressing; one rest day minimum",
    "recovery-status-band": "moderate",
    "rx-interaction-classes": "bleeding-risk;cyp3a4-pgp",
}


def test_every_wired_token_is_in_the_field_set():
    """AC-1: every token the capture seam writes to the store is a SUMMARY_FIELD_SET member.

    Grounds the capture seam's wired-token set against the LIVE allowlist — a token
    the seam would write that is NOT in the field set is a bug (it would write a
    novel store item `summarize`/`dispatch` reject). The module's load-time tripwire
    enforces the same; this pins it from the test side.
    """
    for token in _WIRED_VALUES:
        assert token in SUMMARY_FIELD_SET, f"{token!r} is not a SUMMARY_FIELD_SET token"
    assert set(capture.WIRED_TOKENS) <= set(SUMMARY_FIELD_SET), (
        "capture.WIRED_TOKENS carries a token absent from SUMMARY_FIELD_SET"
    )


def test_wired_field_round_trips_store_then_summarize(tmp_path):
    """AC-1: each wired field -> store item (source:"intake") -> summarize under its token.

    For each wired de-identified token, persist a synthetic value into a tmp store
    root via the capture seam, assert `store.read(token)` returns the reading tagged
    `source:"intake"` with the captured value, and assert `summarize` returns that
    value under the token name. Asserts 0 wired fields are missing from the summary.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        dict(_WIRED_VALUES), root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )

    summary = _summary(store_root)
    for token, value in _WIRED_VALUES.items():
        readings = store.read(token, root=store_root)
        assert len(readings) == 1, f"{token!r} did not land exactly one reading"
        assert readings[0]["source"] == "intake", f"{token!r} not tagged source:intake"
        assert readings[0]["value"] == value, f"{token!r} stored the wrong value"
        assert summary.get(token) == value, f"summarize did not return {token!r} under its token"

    missing = [t for t in _WIRED_VALUES if summary.get(t) != _WIRED_VALUES[t]]
    assert not missing, f"wired fields missing from the summary: {missing}"


def test_wired_token_value_is_a_utc_offset_timepoint(tmp_path):
    """AC-1: the capture write carries a UTC-offset timepoint (store sort correctness).

    The store's `read` sorts lexicographically on `timepoint` and assumes the
    producer wrote a UTC-offset string. A capture write that omitted the offset
    would sort wrong against other producers; assert the offset is present.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"goal-domains": "strength"}, root=store_root, scaffold_root=tmp_path / "scaffold",
        identity_config=_ABSENT_IDENTITY,
    )
    tp = store.read("goal-domains", root=store_root)[0]["timepoint"]
    assert tp.endswith("+00:00") or "+" in tp[10:] or tp[10:].count("-") >= 1, (
        f"timepoint {tp!r} is not a UTC-offset string"
    )


# --------------------------------------------------------------------------- #
# Cycle 1 — AC-6 curated-token-only rx-interaction-classes (Risk Falsification rx)
# --------------------------------------------------------------------------- #


def test_rx_interaction_classes_written_only_from_supplied_class_tokens(tmp_path):
    """AC-6: rx-interaction-classes stores the supplied de-identified class tokens verbatim.

    The form supplies CURATED de-identified class tokens (a `;`-joined scalar); the
    seam writes them to the `rx-interaction-classes` store item as-is. No raw-drug
    name -> class derivation happens in the seam.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"rx-interaction-classes": "bleeding-risk;cyp3a4-pgp"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    readings = store.read("rx-interaction-classes", root=store_root)
    assert readings[0]["value"] == "bleeding-risk;cyp3a4-pgp"
    assert readings[0]["source"] == "intake"


def test_serve_layer_has_no_raw_drug_to_class_lookup():
    """AC-6 / Risk Falsification rx: scripts/serve/ carries 0 raw-drug-name->class map.

    The de-identification (drug name -> interaction class) is a CURATION step at the
    store layer per router.py, NEVER a code lookup in the serve layer. Assert no
    pharmacology map (a dict literal keyed on a raw drug name mapping to a class
    token) enters scripts/serve/. Reds if such a lookup is added.
    """
    serve_dir = REPO_ROOT / "scripts" / "serve"
    # A raw-drug-name -> interaction-class lookup would name common drugs as keys.
    raw_drug_markers = ("warfarin", "aspirin", "ibuprofen", "metformin", "statin", "ssri")
    for py in serve_dir.glob("*.py"):
        src = py.read_text().lower()
        for marker in raw_drug_markers:
            assert marker not in src, (
                f"{py.name} references a raw drug name {marker!r} — a raw-name->class "
                f"lookup must not enter the serve layer (de-id is a store-layer curation)"
            )


def test_raw_drug_name_is_never_written_into_rx_interaction_classes(tmp_path):
    """AC-6: a raw drug name supplied as a record-only field never reaches the rx item.

    A raw supplement/drug name (Step-5 raw stack) is a record-only field -> the
    gitignored scaffold, NEVER the `rx-interaction-classes` store item. Assert the
    rx item carries only the supplied class tokens, not a raw drug name.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {
            "rx-interaction-classes": "bleeding-risk",
            "supplement-stack": "warfarin 5mg; fish oil 2g",  # record-only raw stack
        },
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    rx = store.read("rx-interaction-classes", root=store_root)
    assert rx[0]["value"] == "bleeding-risk"
    assert "warfarin" not in rx[0]["value"], "a raw drug name leaked into rx-interaction-classes"


# --------------------------------------------------------------------------- #
# Cycle 1 — Risk Negative-1 setup: active-issue-class indirection
# --------------------------------------------------------------------------- #


def test_train_around_writes_raw_symptom_item_summarize_derives_issue_class(tmp_path):
    """Risk Negative-1: a Step-3 'train around' capture -> raw-symptom item -> derived class.

    The "train around / injury" input writes a `raw-symptom-free-text` store item
    (NOT `active-issue-class` directly). `summarize` then DERIVES `active-issue-class`
    from it as a de-identified body-region class — the raw text never appears under
    the field-set token.
    """
    store_root = tmp_path / "store"
    capture.persist_capture(
        {"train-around": "tweaked my lower back deadlifting last week"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    # The raw item is written under raw-symptom-free-text, NOT active-issue-class.
    assert store.read("raw-symptom-free-text", root=store_root), "train-around did not write the raw-symptom item"
    assert store.read("active-issue-class", root=store_root) == [], (
        "train-around wrongly wrote active-issue-class directly (must be derived, not stored)"
    )
    summary = _summary(store_root)
    assert summary.get("active-issue-class") == "back-region", (
        "summarize did not derive active-issue-class from the raw-symptom item"
    )
    # The raw free-text never appears under the field-set token.
    assert "deadlifting" not in str(summary.get("active-issue-class", ""))


# --------------------------------------------------------------------------- #
# Cycle 3 — AC-2 two-surface negative placement (record-only -> scaffold ONLY)
# --------------------------------------------------------------------------- #


def test_record_only_field_lands_in_scaffold_not_in_any_field_set_item(tmp_path):
    """AC-2 / Risk Negative-2: a record-only value lands ONLY under the scaffold root.

    A Step-4 dietary-pattern and a raw Step-5 supplement name are record-only — they
    land under the gitignored scaffold root and NOT under any SUMMARY_FIELD_SET store
    item (the project assert-placement mandate: assert NOT in the wrong place).
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    record_only = {
        "dietary-pattern": "mediterranean-ish, high protein",
        "supplement-stack": "creatine monohydrate 5g",
    }
    capture.persist_capture(
        record_only, root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )

    # Positive: the record-only values are present somewhere under the scaffold root.
    scaffold_text = "".join(p.read_text() for p in scaffold_root.rglob("*") if p.is_file())
    assert "mediterranean" in scaffold_text, "the dietary-pattern record-only value did not land in the scaffold"
    assert "creatine" in scaffold_text, "the supplement-stack record-only value did not land in the scaffold"

    # Negative (the load-bearing assertion): NO SUMMARY_FIELD_SET store item carries a
    # record-only value. Iterate EVERY field-set token.
    for token in SUMMARY_FIELD_SET:
        for reading in store.read(token, root=store_root):
            v = str(reading["value"])
            assert "mediterranean" not in v and "creatine" not in v, (
                f"a record-only value leaked into the {token!r} field-set store item"
            )


# --------------------------------------------------------------------------- #
# Cycle 3 — AC-3 fresh-clone PII scan + AC-4 summarize-gate-raises
# --------------------------------------------------------------------------- #


_ABSENT_CONTACT = "vault/meta/__no_such_contact_config__.txt"


def test_full_capture_session_leaves_tracked_tree_pii_free(tmp_path):
    """AC-3 / Risk Negative-1: after a full capture session, the TRACKED tree carries 0 PII.

    Run a full synthetic Steps-2..5 capture against tmp roots (the values include a
    distinctive record-only string), then run the SINGLE-SOURCED scan policy
    `pii_scan.scan_scoped` — the exact policy the `block-pii-commit` hook + the
    pre-push backstop run — over the git-tracked file set in the fresh-clone posture
    (no operator identity/contact configs, no data-bearing paths). The captured
    values live ONLY under the gitignored store + scaffold, so the tracked tree
    carries 0 operator tokens.

    (`scan_scoped`, not raw `scan`: the trunk scanner applies the structural
    store-line patterns ONLY to non-fixture paths — `tests/` fixtures embed synthetic
    reading-shaped literals by construction, the documented known-fixture partition,
    so a raw whole-tree structural scan floods on them. `scan_scoped` is the policy
    that holds the clonability guarantee this AC asserts.)

    Failing-capable per the planted-leak control below: a real operator token written
    into a tracked path IS caught.
    """
    store_root = tmp_path / "store"
    scaffold_root = tmp_path / "scaffold"
    capture.persist_capture(
        {
            **_WIRED_VALUES,
            "dietary-pattern": "high protein",
            "supplement-stack": "creatine monohydrate 5g",
            "train-around": "lower back caution",
        },
        root=store_root, scaffold_root=scaffold_root, identity_config=_ABSENT_IDENTITY,
    )
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hits = pii_scan.scan_scoped(
        tracked, [], contact_config=_ABSENT_CONTACT, identity_config=_ABSENT_IDENTITY,
    )
    assert hits == 0, f"the tracked tree carries {hits} operator-PII hit(s) after a capture session"

    # Sanity: the capture DID write under the gitignored roots (the values live there).
    assert store.read("goal-domains", root=store_root), "the capture wrote nothing to the tmp store"
    assert list(scaffold_root.rglob("*")), "the capture wrote nothing to the tmp scaffold"

    # NEGATIVE CONTROL (failing-capable): plant a real operator-contact token into a
    # tracked-path-shaped file and confirm the SAME scan policy catches it — proving
    # the 0-hit result above is a real clean, not a constant-zero scan.
    leak = tmp_path / "leaked-tracked.md"
    leak.write_text("reach the operator at operator@example.com")
    contact_cfg = tmp_path / "contact.txt"
    contact_cfg.write_text(r"operator@example\.com")
    planted = pii_scan.scan_scoped(
        [str(leak)], [], contact_config=str(contact_cfg), identity_config=_ABSENT_IDENTITY,
    )
    assert planted >= 1, "the scan policy did not catch a planted operator-contact leak (not failing-capable)"


def test_summarize_raises_on_raw_pii_planted_in_field_set_item(tmp_path):
    """AC-4 / Risk Negative-1: summarize RAISES on raw PII in a field-set item (adversarial).

    Plant a raw-PII value (an email) into a pass-through SUMMARY_FIELD_SET store item
    via `store.append` (simulating a capture bug that mis-routed raw text into a
    field-set item). `summarize` must RAISE ValueError (the 8j6 fail-closed gate) —
    the runtime backstop the boundary depends on.

    Failing-capable per the negative control below.
    """
    store_root = tmp_path / "store"
    # NEGATIVE CONTROL: a CLEAN field-set value does NOT raise (the gate is selective).
    capture.persist_capture(
        {"goal-targets": "add 10 lb to squat"},
        root=store_root, scaffold_root=tmp_path / "scaffold", identity_config=_ABSENT_IDENTITY,
    )
    _summary(store_root)  # must not raise on the clean value

    # Now plant raw PII into a field-set item (a mis-routed capture bug, simulated).
    import datetime
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    store.append(
        "hard-limits",
        {"item": "hard-limits", "timepoint": ts, "source": "intake",
         "value": "contact me at operator@example.com"},
        root=store_root,
    )
    try:
        _summary(store_root)
    except ValueError:
        pass  # expected — the gate raised on the planted PII
    else:
        raise AssertionError("summarize did NOT raise on raw PII planted in a field-set item")


def test_block_pii_commit_denies_a_staged_filled_scaffold(tmp_path):
    """AC-3-deny: block-pii-commit would DENY a staged vault/scaffold/filled/ value.

    Stage a filled-scaffold value under `vault/scaffold/filled/` in a throwaway git
    repo (so the real tree is untouched), then invoke the hook with a `git commit`
    command and assert the deny verdict. Honors the commit-sequencing rule: the
    staging `git add` runs as its OWN command, separate from the asserted commit.
    """
    import json
    import os

    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    # The scaffold prefix the hook denies on (single-sourced in pii-scan-scope.sh).
    scaffold_file = repo / "vault" / "scaffold" / "filled" / "operator-record.json"
    scaffold_file.parent.mkdir(parents=True)
    scaffold_file.write_text('{"dietary-pattern": "high protein"}\n')
    # Stage as its OWN command (the sequencing rule).
    subprocess.run(["git", "add", "vault/scaffold/filled/operator-record.json"], cwd=repo, check=True)

    hook = REPO_ROOT / ".claude" / "hooks" / "block-pii-commit.sh"
    hook_input = json.dumps({
        "tool_input": {"command": "git commit -m 'add record'"},
        "cwd": str(repo),
    })
    env = dict(os.environ, BLOCK_PII_COMMIT_PROJECT_ROOT=str(repo))
    proc = subprocess.run(
        ["bash", str(hook)], input=hook_input, cwd=repo, env=env,
        capture_output=True, text=True,
    )
    assert '"permissionDecision":"deny"' in proc.stdout, (
        f"block-pii-commit did not DENY a staged filled scaffold; stdout={proc.stdout!r} stderr={proc.stderr!r}"
    )
