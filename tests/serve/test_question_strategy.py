"""De-identified store-grounded question-strategy tests (ADR-0015-T2).

`scripts/serve/chat.py`'s `plan_next_turn(summary, covered_domains, declined_domains)`
computes the next-turn gap-set from the de-identified `router.summarize` mapping ONLY —
never the raw transcript, never the gitignored scaffold. It returns a `TurnIntent`
carrying token NAMES / domain names / booleans (0 raw operator string):
`{target_domain, missing_fields, domain_done, intake_complete, record_only}`.

Cycle 1 — AC-1 (de-identified-surface-only), AC-2 (store-grounded `domain_done` +
explicit-decline, never turn-count / model say-so — the PF-S87-01 anti-gap), AC-4
(de-identified `TurnIntent`: `missing_fields ⊆ SUMMARY_FIELD_SET`, 0 raw turn text).

Cycle 2 — AC-3 / CONCERN-1 (a chat-covered domain whose ADR-0019 token is NOT yet
minted reports "captured-for-record, not-planned", never `domain_done` vacuously) and
AC-5 (fail-loud malformed-control raises).

`domain_done` rests on the store-grounded summary (`router.py:411,416` — a field ABSENT
from the returned dict = its backing store item had no readings = not yet captured) plus
the explicit `declined_domains`, NEVER a turn count or a model-supplied flag.
"""

import ast
import functools
import inspect
from pathlib import Path

from scripts.plan.router import SUMMARY_FIELD_SET, summarize
from scripts.serve import chat
from scripts.serve.capture import GOAL_DOMAINS, WIRED_TOKENS, persist_capture
from scripts.store import store

REPO_ROOT = Path(__file__).resolve().parents[2]

# The fresh-clone identity posture (mirrors test_capture.py): the operator's real
# name/contact are not on disk, so identity-token detection is empty while the
# value-class patterns still run.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"


def _bound(store_root):
    """The instance-bound store_read `summarize` requires (recipe caller contract)."""
    return functools.partial(store.read, root=store_root)


def _summary(root):
    """Run `summarize` over a tmp instance's store dir with an absent identity config.

    Binds the reader to `root/"store"` — the same dir `_seed` captures into — so the
    summary reads the seeded tmp instance, not `vault/store/` under the cwd.
    """
    return summarize(_bound(root / "store"), identity_config=_ABSENT_IDENTITY)


# The chat-covered domains whose tokens ARE minted in SUMMARY_FIELD_SET today: the
# `goals` and `training` domains (their tokens are in WIRED_TOKENS / derived). The
# ADR-0019 nutrition/supplements/peptides tokens are NOT yet minted (Wave B) — those
# domains are the CONCERN-1 record-only cases, exercised in Cycle 2.
_GOALS_DOMAIN = "goals"
_TRAINING_DOMAIN = "training"

# Synthetic de-identified values for the minted tokens (valid tokens, no raw PII).
_GOALS_VALUES = {
    "goal-domains": "Workout;Nutrition",
    "goal-targets": "add ten pounds to squat",
    "goal-priority-order": "strength;hypertrophy",
    "hard-limits": "no overhead pressing",
}
# The `training` domain maps to `recovery-status-band` (wired) + `active-issue-class`
# (derived from the `train-around` free-text -> `raw-symptom-free-text` store item). To
# mint BOTH tokens the seed captures `recovery-status-band` AND a `train-around` value.
_TRAINING_VALUES = {
    "recovery-status-band": "moderate",
    "train-around": "sore lower back",
}


def _seed(root, values):
    """Capture `values` into a tmp instance store via the real capture seam."""
    store_root = root / "store"
    scaffold_root = root / "scaffold"
    persist_capture(
        dict(values), root=store_root, scaffold_root=scaffold_root,
        identity_config=_ABSENT_IDENTITY,
    )
    return store_root


# --------------------------------------------------------------------------- #
# AC-1 — de-identified-surface-only: reads ONLY router.summarize(store_read)
# --------------------------------------------------------------------------- #


# The STRATEGY surface this AC-1 invariant scopes to: `plan_next_turn` + its private
# gap-set helper `_missing_fields`. The module ALSO holds the ADR-0016-T1 per-turn
# DISPATCH (`dispatch_turn`/`_model_messages`/`_degraded_turn`/`_progress`), which
# legitimately references the model client + the raw turn — that is the dispatch's lane,
# not the strategy's. Scoping the scan to the strategy functions keeps this invariant's
# teeth (it still reds if `plan_next_turn` touches a raw/scaffold/model surface) without
# false-flagging the dispatch the strategy module now also carries.
_STRATEGY_FUNCTIONS = ("plan_next_turn", "_missing_fields")


def _chat_module_executable_names():
    """Every identifier referenced in the STRATEGY functions' EXECUTABLE code.

    Scans the `_STRATEGY_FUNCTIONS` subtrees of `scripts/serve/chat.py`'s AST (docstrings
    excluded) — so a raw/scaffold/model surface accessed in the STRATEGY is caught, while
    a mention in a docstring/comment, or a legitimate reference in the ADR-0016-T1
    dispatch (a different function in the same module), is not.
    """
    tree = ast.parse((REPO_ROOT / "scripts" / "serve" / "chat.py").read_text())
    names = set()
    for func in tree.body:
        if not (isinstance(func, ast.FunctionDef) and func.name in _STRATEGY_FUNCTIONS):
            continue
        for node in ast.walk(func):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                mod = getattr(node, "module", "") or ""
                names.add(mod)
                for alias in node.names:
                    names.add(alias.name)
    return names


def test_plan_next_turn_reads_no_raw_transcript_or_scaffold_surface():
    """AC-1: the strategy's CODE references 0 raw-transcript / scaffold / model surface.

    Scans `scripts/serve/chat.py`'s executable AST (not its docstrings — those may
    name the boundary they forbid). The strategy reads ONLY the de-identified `summary`
    mapping passed in; it must NOT reference the raw transcript, the gitignored
    scaffold writer, a model client, or a network surface — reading raw would cross the
    crown-jewel PII boundary.
    """
    referenced = _chat_module_executable_names()
    forbidden = {
        "scaffold", "scaffold_root", "_write_scaffold",  # the gitignored record
        "transcript", "turn_text", "turn_history",        # raw conversation text
        "converse", "messages", "create",                 # the model call (ADR-0016-T1's)
        "open", "read_text", "Path",                       # raw file/scaffold I/O
        "client",                                          # the model client module
    }
    leaked = forbidden & referenced
    assert not leaked, (
        f"plan_next_turn code references {sorted(leaked)} — the strategy must read "
        f"ONLY the de-identified summary, never a raw / scaffold / model / file surface"
    )


def test_plan_next_turn_signature_takes_the_summary_not_a_reader():
    """AC-1: the strategy receives the de-identified summary mapping, not a raw read.

    The caller binds `summarize(functools.partial(store.read, root=instance_root))`
    and passes its OUTPUT (the de-identified summary). The strategy's first parameter
    is that summary — it does not itself open the store, the scaffold, or the model.
    """
    params = list(inspect.signature(chat.plan_next_turn).parameters)
    assert params[:3] == ["summary", "covered_domains", "declined_domains"], (
        f"plan_next_turn signature drifted: {params!r}"
    )


def test_strategy_consumes_an_instance_bound_summary(tmp_path):
    """AC-1: the de-identified summary is the instance-bound `summarize` output.

    Binds `store.read` to the tmp instance root (the caller contract,
    `functools.partial(store.read, root=instance_root)`), so the strategy reads the
    tmp instance and NOT `vault/store/` under the cwd. A summary built from an
    unseeded instance carries no minted goal tokens -> the goals domain is not done.
    """
    summary = _summary(tmp_path)  # unseeded instance: no goal tokens present
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
    )
    assert intent.domain_done is False
    assert set(intent.missing_fields) == set(_GOALS_VALUES), (
        "an unseeded instance must report every goals token missing"
    )


# --------------------------------------------------------------------------- #
# AC-2 — store-grounded domain_done + explicit-decline (PF-S87-01 anti-gap)
# --------------------------------------------------------------------------- #


def test_domain_with_all_tokens_present_is_done(tmp_path):
    """AC-2: a domain whose every mapped token is in `summary` is `domain_done`."""
    root = _seed(tmp_path, _GOALS_VALUES)
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
    )
    assert intent.domain_done is True
    assert intent.missing_fields == ()
    assert intent.target_domain is None  # nothing left to ask


def test_domain_with_a_missing_token_is_not_done_even_after_n_turns(tmp_path):
    """AC-2: a missing-token domain is NOT done, and turn count cannot make it done.

    Seed only THREE of the goals tokens (omit `hard-limits`). The domain is not done
    no matter how many turns have elapsed: `plan_next_turn` takes no turn count, and
    the missing token keeps it open. This is the PF-S87-01 anti-gap — a turn-count
    "done" would silently leave `hard-limits` un-captured.
    """
    partial = {k: v for k, v in _GOALS_VALUES.items() if k != "hard-limits"}
    root = _seed(tmp_path, partial)
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
    )
    assert intent.domain_done is False
    assert "hard-limits" in intent.missing_fields
    # plan_next_turn takes no turn-count parameter — there is no surface by which a
    # high turn count could flip the verdict (the anti-gap, structurally).
    assert "turn" not in inspect.signature(chat.plan_next_turn).parameters


def test_declined_domain_is_done(tmp_path):
    """AC-2: an explicitly-declined domain IS done even with missing tokens.

    The operator declined `goals`; the domain is done despite no tokens captured —
    a silently-dropped decline would re-ask it forever (Design §1.2).
    """
    summary = _summary(tmp_path)  # unseeded: no goals tokens present
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains={_GOALS_DOMAIN},
    )
    assert intent.domain_done is True
    assert intent.target_domain is None


def test_done_does_not_rest_on_model_say_so(tmp_path):
    """AC-2: a model-asserted done flag in `summary` cannot make a domain done.

    `summary` is the de-identified mapping; the strategy keys done off the PRESENCE
    of the domain's SUMMARY_FIELD_SET tokens + the explicit decline ONLY. A planted
    model-style `domain_done`/`done` key in the mapping is ignored — done stays
    store-grounded.
    """
    summary = _summary(tmp_path)  # unseeded
    summary["domain_done"] = True  # a model say-so flag, NOT a field-set token
    summary["done"] = True
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
    )
    assert intent.domain_done is False, "done must not rest on a model-supplied flag"


def test_intake_complete_only_when_every_covered_domain_done(tmp_path):
    """AC-2: `intake_complete` is true only when every covered domain is done."""
    root = _seed(tmp_path, _GOALS_VALUES)  # goals done, training not
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary,
        covered_domains={_GOALS_DOMAIN, _TRAINING_DOMAIN},
        declined_domains=set(),
    )
    assert intent.intake_complete is False
    assert intent.target_domain == _TRAINING_DOMAIN  # the next not-done domain


def test_intake_complete_true_when_all_done(tmp_path):
    """AC-2: every covered domain done (captured or declined) -> intake_complete."""
    root = _seed(tmp_path, {**_GOALS_VALUES, **_TRAINING_VALUES})
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary,
        covered_domains={_GOALS_DOMAIN, _TRAINING_DOMAIN},
        declined_domains=set(),
    )
    assert intent.intake_complete is True
    assert intent.target_domain is None


# --------------------------------------------------------------------------- #
# AC-4 — de-identified TurnIntent: token/domain names + booleans only
# --------------------------------------------------------------------------- #


def test_turn_intent_missing_fields_subset_of_field_set(tmp_path):
    """AC-4: `missing_fields ⊆ SUMMARY_FIELD_SET` — token NAMES only, 0 raw text."""
    partial = {k: v for k, v in _GOALS_VALUES.items() if k != "goal-targets"}
    root = _seed(tmp_path, partial)
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
    )
    assert set(intent.missing_fields) <= set(SUMMARY_FIELD_SET)
    # The captured raw value never appears in any intent field.
    for raw_value in _GOALS_VALUES.values():
        assert raw_value not in intent.missing_fields
        assert raw_value != intent.target_domain


def test_turn_intent_carries_only_names_and_booleans(tmp_path):
    """AC-4: every TurnIntent value is a token/domain name or a boolean — no raw text.

    `target_domain` is a domain name or None; `missing_fields` are token names;
    `domain_done`/`intake_complete` are booleans. No captured operator value (a
    `goal-targets` free-text, a `hard-limits` string) leaks into any field.
    """
    root = _seed(tmp_path, _GOALS_VALUES)
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary,
        covered_domains={_GOALS_DOMAIN, _TRAINING_DOMAIN},
        declined_domains=set(),
    )
    assert isinstance(intent.domain_done, bool)
    assert isinstance(intent.intake_complete, bool)
    assert intent.target_domain is None or intent.target_domain in {
        _GOALS_DOMAIN, _TRAINING_DOMAIN,
    }
    assert all(f in SUMMARY_FIELD_SET for f in intent.missing_fields)
    flat = " ".join(
        [str(intent.target_domain)] + list(intent.missing_fields)
    )
    for raw_value in {**_GOALS_VALUES, **_TRAINING_VALUES}.values():
        assert raw_value not in flat


# --------------------------------------------------------------------------- #
# AC-3 / CONCERN-1 — an unminted chat domain is record-only, never vacuously done
# --------------------------------------------------------------------------- #

# A chat-covered domain whose ADR-0019 token is NOT yet minted in SUMMARY_FIELD_SET
# (its mapped active-token set is empty). At this task's time `nutrition`/`supplements`/
# `peptides` are exactly those domains (their ADR-0019 tokens are Wave B). Grounded
# against the live surface — not a hand-picked literal.
_UNMINTED_DOMAIN = "nutrition"


def test_unminted_domain_has_no_field_set_token():
    """Grounding: the CONCERN-1 fixture domain genuinely maps to NO field-set token.

    Anchors the test to the live surface: if a future ADR-0019 batch mints a
    `nutrition` token, this guard reds so the CONCERN-1 fixture is re-grounded rather
    than silently testing a now-minted domain.
    """
    assert chat._DOMAIN_TOKENS[_UNMINTED_DOMAIN] == (), (
        f"{_UNMINTED_DOMAIN!r} now maps to a minted token — re-ground the CONCERN-1 "
        f"fixture against a still-unminted chat domain"
    )


def test_unminted_domain_reports_record_only_not_done(tmp_path):
    """AC-3 / CONCERN-1: an unminted chat domain is record-only, never `domain_done`.

    A chat-covered domain whose ADR-0019 token is NOT yet minted (empty `missing_fields`,
    no planner-feeding token) reports "captured-for-record, not-planned" and is NEVER
    reported `domain_done` vacuously. It must NOT be the `target_domain` (nothing to ask)
    and must NOT collapse into a done verdict that hides the un-minted gap.
    """
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary, covered_domains={_UNMINTED_DOMAIN}, declined_domains=set(),
    )
    assert _UNMINTED_DOMAIN in intent.record_only, (
        "an unminted chat domain must be reported record-only (captured-for-record)"
    )
    # It is never asked again (no minted token to gap-fill) ...
    assert intent.target_domain is None
    assert intent.missing_fields == ()
    # ... but it is NEVER vacuously `domain_done`: the record-only state is distinct.
    assert _UNMINTED_DOMAIN not in intent.record_only or intent.domain_done is False, (
        "an unminted domain must report record-only, NOT a vacuous domain_done"
    )


def test_unminted_domain_alongside_open_minted_domain(tmp_path):
    """AC-3 / CONCERN-1: a record-only domain never short-circuits a real gap.

    With an unminted `nutrition` domain AND an incomplete `goals` domain covered, the
    strategy still targets the real open `goals` gap and reports `nutrition` record-only —
    the record-only state does not let the loop terminate while a minted gap is open.
    """
    partial = {k: v for k, v in _GOALS_VALUES.items() if k != "hard-limits"}
    root = _seed(tmp_path, partial)
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary,
        covered_domains={_GOALS_DOMAIN, _UNMINTED_DOMAIN},
        declined_domains=set(),
    )
    assert intent.target_domain == _GOALS_DOMAIN
    assert "hard-limits" in intent.missing_fields
    assert _UNMINTED_DOMAIN in intent.record_only
    assert intent.intake_complete is False


def test_intake_complete_with_only_record_only_domains(tmp_path):
    """AC-3 / CONCERN-1: a session of only record-only domains completes the loop.

    An unminted domain has no askable gap, so a session covering only unminted domains
    terminates (`intake_complete` True, no `target_domain`) WITH the record-only state
    reported — captured-for-record, not silently dropped, never a spurious open gap.
    """
    summary = _summary(tmp_path)
    intent = chat.plan_next_turn(
        summary,
        covered_domains={"nutrition", "supplements", "peptides"},
        declined_domains=set(),
    )
    assert intent.intake_complete is True
    assert intent.target_domain is None
    assert set(intent.record_only) == {"nutrition", "supplements", "peptides"}
    # CONCERN-1: an all-record-only session is NEVER vacuously `domain_done` — no
    # planner-feeding domain reached a genuine done, so domain_done is False even though
    # the loop terminates (the record-only domains are resolved-for-record, not planned).
    assert intent.domain_done is False


# --------------------------------------------------------------------------- #
# AC-5 — fail-loud malformed-control raises (never a silent loop corruption)
# --------------------------------------------------------------------------- #


def test_covered_domain_outside_chat_set_raises(tmp_path):
    """AC-5: a `covered_domains` member outside the chat-covered set raises fail-loud."""
    import pytest

    summary = _summary(tmp_path)
    with pytest.raises(chat.MalformedControlError):
        chat.plan_next_turn(
            summary, covered_domains={"not-a-chat-domain"}, declined_domains=set(),
        )


def test_declined_domain_outside_chat_set_raises(tmp_path):
    """AC-5: a `declined_domains` member outside the chat-covered set raises fail-loud."""
    import pytest

    summary = _summary(tmp_path)
    with pytest.raises(chat.MalformedControlError):
        chat.plan_next_turn(
            summary,
            covered_domains={_GOALS_DOMAIN},
            declined_domains={"not-a-chat-domain"},
        )


def test_declined_not_subset_of_covered_raises(tmp_path):
    """AC-5: `declined_domains ⊄ covered_domains` raises fail-loud.

    Declining a domain that was never covered is an inconsistent control state — it
    must raise, never silently mark an un-covered domain done.
    """
    import pytest

    summary = _summary(tmp_path)
    with pytest.raises(chat.MalformedControlError):
        chat.plan_next_turn(
            summary,
            covered_domains={_GOALS_DOMAIN},
            declined_domains={_TRAINING_DOMAIN},  # in CHAT_DOMAINS but not covered
        )


def test_non_dict_summary_raises():
    """AC-5: a non-dict `summary` raises fail-loud (never silently corrupts the loop)."""
    import pytest

    for bad in (None, ["goal-domains"], "goal-domains", 42):
        with pytest.raises(chat.MalformedControlError):
            chat.plan_next_turn(
                bad, covered_domains={_GOALS_DOMAIN}, declined_domains=set(),
            )
