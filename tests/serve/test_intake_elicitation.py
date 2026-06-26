"""SPA-surface not-naive intake-elicitation proof (ADR-0029-T4).

Proves on the SERVED POST `/chat` surface that a fresh operator — whose four chat-band
tokens sit at their `not-discussed` sentinel (`router._ALWAYS_SET_DERIVED`) — is ASKED the
genuine gap, and that those present sentinels read as a GAP (record-only), NEVER a vacuous
`domain_done` / `intake_complete` (PF-S87-01). A TEST-ONLY proof binding the already-built
`chat.plan_next_turn` / `dispatch_turn` mechanism over a MOCK backend at the ADR-0015
`ModelClient(backend=...)` seam (0 live spend, 0 production change).

The crux (PF-S87-01): the fresh-operator `router.summarize` output carries the four
`_ALWAYS_SET_DERIVED` tokens (`dietary-pattern-class` / `supplement-stack-class` /
`peptide-use-class` / `training-volume-band`) ALL PRESENT at `_NOT_DISCUSSED =
"not-discussed"` — so a present-KEY-means-captured reading would mark the
nutrition/supplements/peptides domains done off the sentinel. The built mechanism maps
those chat domains to the EMPTY token tuple (`chat._DOMAIN_TOKENS[d] == ()`), so they
resolve RECORD-ONLY and never gate `domain_done`. The recipe's Step-1b mutation oracle
(run transiently, never committed) confirmed the AC-2 assertions RED-trip if a domain were
re-mapped to a present sentinel token — the non-tautology proof.

Acceptance coverage (one cohesive not-naive proof over the served `/chat` surface):
- AC-1: a fresh operator is ASKED the open gap (`target_domain == "goals"`, non-empty
  `missing_fields`).
- AC-2: the present sentinel domains are RECORD-ONLY, never vacuously `domain_done`
  (PF-S87-01 / CONCERN-1), plus the `_DOMAIN_TOKENS[d] == ()` + `_NOT_DISCUSSED` grounding.
- AC-3: a genuine open gap keeps `intake_complete` False.
- AC-4: the gaps-filled complement completes (`intake_complete`/`domain_done` True) with the
  sentinel domains STILL record-only — the failing-capable negative control (non-tautology).
- AC-5: the served `progress` control surface carries token/domain names + booleans only
  (0 raw operator string; NFR-1).

Mirrors the `test_chat.py` served-`/chat` drive (`_ReplyBackend` / `_server_with_chat` /
`_post_chat`) and the `test_question_strategy.py` store-seed (`_seed` / `_summary` /
`_ABSENT_IDENTITY`) shapes — not a third mock/seed invention.
"""

import functools
import http.client
import json
import threading
from pathlib import Path

from scripts.model.client import ModelClient
from scripts.plan import router
from scripts.plan.router import SUMMARY_FIELD_SET, summarize
from scripts.serve import chat
from scripts.serve import server as serve_server
from scripts.serve.capture import persist_capture
from scripts.store import store

# The fresh-clone identity posture (mirrors test_chat.py / test_question_strategy.py): the
# operator's real name/contact are not on disk, so identity-token detection is empty while
# the value-class patterns still run.
_ABSENT_IDENTITY = "vault/meta/__no_such_identity_config__.txt"

# The three chat domains whose ADR-0019 tokens are NOT yet minted (Wave B): a fresh
# operator carries each at its `not-discussed` sentinel, so they are the CONCERN-1
# record-only domains the sentinel=gap proof pins.
_SENTINEL_DOMAINS = {"nutrition", "supplements", "peptides"}

# Synthetic de-identified values that mint the goals + training tokens through the real
# capture seam (mirrors test_question_strategy.py's `_GOALS_VALUES` / `_TRAINING_VALUES`).
# `training` maps to `recovery-status-band` (wired) + `active-issue-class` (derived from the
# `train-around` free-text), so seeding both mints the whole training domain.
_GAPS_FILLED_SEED = {
    "goal-domains": "Workout;Nutrition",
    "goal-targets": "add ten pounds to squat",
    "goal-priority-order": "strength;hypertrophy",
    "hard-limits": "no overhead pressing",
    "recovery-status-band": "moderate",
    "train-around": "sore lower back",
}


class _ReplyBackend:
    """A mock converse backend returning a scripted `{"reply", "extraction"}` (no egress).

    Mirrors `tests/serve/test_chat.py::_ReplyBackend`: an `extraction={}` proposes nothing,
    so nothing lands and the fresh-operator gap stays open over the served turn.
    """

    def __init__(self, reply="ok", extraction=None):
        self.reply = reply
        self.extraction = {} if extraction is None else extraction

    def converse(self, messages):
        return {"reply": self.reply, "extraction": dict(self.extraction)}


def _serve_in_thread(srv):
    """Run srv.serve_forever on a daemon thread; return the thread."""
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    return thread


def _server_with_chat(tmp_path, backend):
    """Build a loopback server whose `/chat` dispatch uses a tmp store + a mock client.

    Mirrors `tests/serve/test_chat.py::_server_with_chat`: ephemeral port 0, tmp
    store/scaffold roots, and the mock backend injected at the ADR-0015
    `ModelClient(backend=...)` seam (0 live API call, 0 key).
    """
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=ModelClient(backend=backend),
    )
    return srv, srv.server_address[1]


def _post_chat(port, payload):
    """POST a JSON `/chat` turn body; return (status, parsed-or-raw response)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    body = json.dumps(payload).encode("utf-8")
    conn.request("POST", "/chat", body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    text = resp.read().decode("utf-8")
    conn.close()
    return resp.status, json.loads(text)


def _drive_chat(tmp_path, *, covered, turn="hi", seed=None):
    """Seed (optionally), serve, POST one `/chat` turn, return the receipt's `progress`.

    Pre-seeds the served server's `store_root` via the real `persist_capture` seam (the
    AC-4 gaps-filled complement), then drives ONE served turn over a mock backend whose
    `extraction={}` lands nothing. Returns the de-identified `progress` projection.
    """
    if seed:
        persist_capture(
            dict(seed), root=tmp_path / "store", scaffold_root=tmp_path / "scaffold",
            identity_config=_ABSENT_IDENTITY,
        )
    srv, port = _server_with_chat(tmp_path, _ReplyBackend())
    _serve_in_thread(srv)
    try:
        status, resp = _post_chat(
            port, {"turn": turn, "conversation": [], "covered_domains": sorted(covered)}
        )
        assert status == 200, f"served /chat did not answer 200: {status}"
        assert resp.get("degraded") is not True, f"served turn degraded: {resp}"
        return resp["progress"]
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- #
# AC-1 — a fresh operator is ASKED the open gap (not skipped)
# --------------------------------------------------------------------------- #


def test_fresh_operator_is_asked_the_open_gap(tmp_path):
    """AC-1: a fresh-store served `/chat` turn ASKS the open `goals` gap, not skips it.

    Over a fresh store (nothing landed) the served receipt's `progress` targets the open
    planner-feeding `goals` domain and lists its four absent tokens as `missing_fields` —
    the operator is asked the genuine gap, never silently passed over.
    """
    progress = _drive_chat(tmp_path, covered={"goals", "training"})
    assert progress["target_domain"] == "goals"
    assert set(progress["missing_fields"]) == set(chat._DOMAIN_TOKENS["goals"]), (
        "a fresh operator must be asked every absent goals token"
    )
    assert progress["missing_fields"], "the fresh gap must be NON-EMPTY (the operator is asked)"


# --------------------------------------------------------------------------- #
# AC-2 — SENTINEL = GAP, never vacuous `domain_done` (PF-S87-01 / CONCERN-1)
# --------------------------------------------------------------------------- #


def test_sentinel_domains_are_record_only_never_domain_done(tmp_path):
    """AC-2: the present `not-discussed` sentinel domains are RECORD-ONLY, never done.

    A fresh-store served `/chat` turn covering the three sentinel domains — whose tokens
    sit at the present `not-discussed` sentinel in the summary — resolves them to
    `record_only`, NEVER `domain_done`. The present sentinel is never read as captured
    (the PF-S87-01 anti-gap): a present-KEY-means-captured strategy would flip these.
    """
    progress = _drive_chat(tmp_path, covered=_SENTINEL_DOMAINS)
    assert _SENTINEL_DOMAINS <= set(progress["record_only"]), (
        "the present-sentinel domains must report record-only (captured-for-record)"
    )
    assert progress["domain_done"] is False, (
        "a present sentinel must NEVER count as a planner-feeding done (PF-S87-01)"
    )


def test_record_only_domains_have_no_field_set_token(tmp_path):
    """AC-2 grounding: the sentinel domains map to NO field-set token, present at sentinel.

    Re-grounds the proof against the live surface so it REDS (rather than silently testing a
    now-minted domain) if a future ADR-0019 batch mints a nutrition/supplements/peptides
    token: (a) `chat._DOMAIN_TOKENS[d] == ()` for each, and (b) the `_NOT_DISCUSSED`
    sentinel anchor — the four `_ALWAYS_SET_DERIVED` tokens are PRESENT in a fresh
    operator's summary at exactly that sentinel, which is what makes the sentinel=gap proof
    non-vacuous (a present key that must NOT read as captured).
    """
    for domain in _SENTINEL_DOMAINS:
        assert chat._DOMAIN_TOKENS[domain] == (), (
            f"{domain!r} now maps to a minted token — re-ground the sentinel=gap fixture "
            f"against a still-unminted chat domain"
        )
    assert router._NOT_DISCUSSED == "not-discussed"
    fresh = summarize(
        functools.partial(store.read, root=tmp_path / "store"),
        identity_config=_ABSENT_IDENTITY,
    )
    for token in router._ALWAYS_SET_DERIVED:
        assert fresh.get(token) == router._NOT_DISCUSSED, (
            f"a fresh operator must carry {token!r} PRESENT at the {router._NOT_DISCUSSED!r} "
            f"sentinel — the present-key reality the sentinel=gap proof rests on"
        )


# --------------------------------------------------------------------------- #
# AC-3 — NEVER vacuous `intake_complete` while a real gap is open
# --------------------------------------------------------------------------- #


def test_open_gap_keeps_intake_complete_false(tmp_path):
    """AC-3: an open goals gap (plus record-only domains) keeps `intake_complete` False.

    A fresh-store served `/chat` turn covering `goals` (absent tokens) AND the three
    sentinel domains does NOT complete — the present sentinels do not let the loop
    terminate while a genuine planner-feeding gap is open.
    """
    progress = _drive_chat(tmp_path, covered={"goals"} | _SENTINEL_DOMAINS)
    assert progress["intake_complete"] is False, (
        "intake must NOT complete while a real goals gap is open (PF-S87-01)"
    )
    assert progress["target_domain"] == "goals"


# --------------------------------------------------------------------------- #
# AC-4 — failing-capable negative control: the gaps-filled complement
# --------------------------------------------------------------------------- #


def test_gaps_filled_complement_completes_with_sentinels_still_record_only(tmp_path):
    """AC-4: the complement completes — with the sentinel domains STILL record-only.

    PRE-SEED the served server's store with the goals + training tokens, cover all five
    chat domains, and drive one served turn: `intake_complete` and `domain_done` both turn
    True (a genuine goals/training done), AND the three sentinel domains REMAIN exactly the
    `record_only` set. This complement to AC-2/AC-3 proves the verdicts distinguish complete
    from incomplete (not constant-False), and that the present sentinels are NOT counted as
    captured (they would drop out of `record_only` if they were — the non-tautology the
    Step-1b mutation oracle RED-trips).
    """
    progress = _drive_chat(
        tmp_path, covered={"goals", "training"} | _SENTINEL_DOMAINS, seed=_GAPS_FILLED_SEED,
    )
    assert progress["intake_complete"] is True, "the gaps-filled complement must complete"
    assert progress["domain_done"] is True, "a genuine goals/training done must be reported"
    assert set(progress["record_only"]) == _SENTINEL_DOMAINS, (
        "the present sentinels must STAY record-only — never counted as captured/done"
    )


# --------------------------------------------------------------------------- #
# AC-5 — de-identified control surface: 0 raw operator string (NFR-1)
# --------------------------------------------------------------------------- #


def test_progress_carries_only_names_and_booleans_no_raw_value(tmp_path):
    """AC-5: the served `progress` carries token/domain names + booleans only — no raw text.

    A served `/chat` turn whose TEXT carries an identifiable raw operator value (a name)
    must not project that value into `progress`: the raw value appears NOWHERE in the
    receipt's progress, AND every progress value is a domain name (∈ `CHAT_DOMAINS`), a
    token name (∈ `SUMMARY_FIELD_SET`), a boolean, or None.
    """
    raw_name = "Walter McGivney"
    progress = _drive_chat(
        tmp_path, covered={"goals"} | _SENTINEL_DOMAINS,
        turn=f"My name is {raw_name}, let's set goals",
    )
    serialized = json.dumps(progress)
    for fragment in (raw_name, "Walter", "McGivney"):
        assert fragment not in serialized, (
            f"a raw operator value ({fragment!r}) leaked into the de-identified progress"
        )

    assert progress["target_domain"] is None or progress["target_domain"] in chat.CHAT_DOMAINS
    for field in progress["missing_fields"]:
        assert field in SUMMARY_FIELD_SET, f"{field!r} is not a SUMMARY_FIELD_SET token name"
    for domain in progress["record_only"]:
        assert domain in chat.CHAT_DOMAINS, f"{domain!r} is not a chat domain name"
    assert isinstance(progress["domain_done"], bool)
    assert isinstance(progress["intake_complete"], bool)
