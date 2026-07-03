"""Profile-aware Care Assistant conversation tests (the continuous post-unlock care chat).

`care_chat.respond` is the POST-unlock care conversation — distinct from `chat.dispatch_turn` (the
pre-unlock intake elicitation, which carries only the de-identified gap-set and extracts facts). It
re-reads the de-identified `router.summarize` profile server-side each turn and carries it as context
so the Care Assistant reasons over the operator's full (de-identified) profile and the conversation
stays coherent (the care-review clarifying questions are the opening turns). ONE `converse` call over
the no-train lane; 0 raw PII in the profile context; fail-closed on a failed call.

MOCK/FIXTURE-tested at 0 live spend: a recording mock backend records the converse payload; the store
is a tmp root. No live API, no key, no non-loopback socket.
"""

import functools
import json

import pytest

from scripts.model.client import ModelCallError
from scripts.plan import router
from scripts.serve import care_chat
from scripts.store import store


class _RecordingBackend:
    """A converse backend that records the payload and returns a scripted reply."""

    def __init__(self, *, reply="Got it — tell me more about the shoulder.", raise_error=False):
        self.reply = reply
        self.raise_error = raise_error
        self.calls = []

    def converse(self, messages):
        self.calls.append(messages)
        if self.raise_error:
            raise ModelCallError("model down")
        return {"reply": self.reply, "extraction": []}


def _seed(root):
    """Seed a small de-identifiable profile into a tmp store (drives router.summarize)."""
    for item, value in (("sex-for-dosing", "male"), ("equipment-access-class", "full-home-gym"),
                        ("goal-domains", "Workout;Nutrition"), ("date-of-birth", "1970")):
        store.append(item, {"item": item, "timepoint": "2026-06-01T00:00:00+00:00",
                            "source": "intake", "value": value}, root=root)


def _reader(root):
    return functools.partial(store.read, root=root)


def test_respond_carries_the_care_profile_plus_conversation_plus_turn(tmp_path):
    """The care turn's payload = the operator's FULL care profile + the conversation + the turn.

    `respond` re-reads the operator's full care profile server-side (`_care_profile`: identity-safe
    demographics/goals/genetics + the raw health detail) and builds a converse payload whose first turn
    carries it, followed by the prior conversation and the current operator turn. Proves the Care
    Assistant reasons over the operator's real profile AND has the conversation continuity (the opening
    clarifying questions ride in `conversation`).
    """
    root = tmp_path / "store"
    _seed(root)
    scaffold = tmp_path / "scaffold"
    backend = _RecordingBackend()
    conversation = [{"role": "assistant", "content": "Is 55 your age or your training years?"}]
    receipt = care_chat.respond("It's my age.", conversation, client=backend, store_root=root, scaffold_root=scaffold)
    assert receipt["reply"] == backend.reply, "the care turn did not return the model reply"
    assert len(backend.calls) == 1, "the care turn did not make exactly one converse call"
    payload = backend.calls[0]
    # First turn = the operator's full care profile context (server-derived, not client-supplied).
    first = json.loads(payload[0]["content"])
    assert first.get("task") == "care-conversation", "the first turn is not the care-conversation profile context"
    assert first["profile"] == care_chat._care_profile(_reader(root), scaffold_root=scaffold), (
        "the context profile is not the server-derived full care profile"
    )
    # The prior conversation (the opening question) + the current turn are present, in order.
    contents = [t["content"] for t in payload]
    assert "Is 55 your age or your training years?" in contents, "the opening question is not carried in the conversation"
    assert payload[-1]["content"] == "It's my age.", "the current operator turn is not the last message"
    # Every entry is API-valid (role in {user, assistant}, string content).
    for t in payload:
        assert t["role"] in ("user", "assistant") and isinstance(t["content"], str)


def test_respond_profile_context_carries_no_raw_pii(tmp_path):
    """Pure IDENTITY stays stripped from the care profile — the raw DOB never crosses.

    The care agent carries the operator's raw HEALTH detail (that is the point), but pure identity is
    still stripped: a store with a full-date DOB derives an AGE token (never the date string), so the
    care payload carries the age, not the raw birth date. Proves the identity line holds even though
    the health detail is intentionally raw.
    """
    root = tmp_path / "store"
    store.append("date-of-birth", {"item": "date-of-birth", "timepoint": "2026-06-01T00:00:00+00:00",
                                   "source": "intake", "value": "1986-03-14"}, root=root)
    _seed(root)
    backend = _RecordingBackend()
    care_chat.respond("hi", [], client=backend, store_root=root)
    wire = json.dumps(backend.calls[0])
    assert "1986-03-14" not in wire, "the raw DOB crossed into the care-conversation payload (de-id breach)"


def test_respond_fails_closed_on_model_error(tmp_path):
    """A failed/empty model call returns an honest degraded reply — no fabrication."""
    root = tmp_path / "store"
    _seed(root)
    backend = _RecordingBackend(raise_error=True)
    receipt = care_chat.respond("hi", [], client=backend, store_root=root)
    assert receipt.get("reply") is None and receipt.get("degraded") is True, "a failed care turn did not fail closed"


def test_respond_captures_a_proposed_fact_through_the_gate(tmp_path):
    """A care-agent-proposed fact is WRITTEN to the store through the de-identification gate.

    The care agent proposes a fact in its `extraction` (here a wired goal token); `respond` routes it
    through the SAME `extract.persist_extraction` -> `capture.persist_capture` gate the intake chat uses,
    so it lands in the store and the receipt reports it. Failing-capable: without the store-write wiring
    the fact never lands.
    """
    root = tmp_path / "store"
    scaffold = tmp_path / "scaffold"
    _seed(root)

    class _FactBackend:
        def converse(self, messages):
            return {"reply": "Noted — I've set your priority order.",
                    "extraction": {"goal-priority-order": "recovery then strength"}}

    receipt = care_chat.respond("prioritize recovery then strength", [], client=_FactBackend(),
                                store_root=root, scaffold_root=scaffold)
    assert "goal-priority-order" in receipt["receipt"]["store"], f"the proposed fact did not land: {receipt}"
    landed = [r["value"] for r in store.read("goal-priority-order", root=root)]
    assert "recovery then strength" in landed, "the care agent's fact was not written to the store"


def test_respond_raw_value_under_a_wired_token_routes_record_only_not_the_model_bound_item(tmp_path):
    """Crown-jewel: a raw value the care agent proposes under a wired token is gated, not trusted.

    The care agent must not be able to write a raw operator string straight into a model-bound token —
    the gate routes it by data class. A raw drug string proposed under `rx-interaction-classes` (the
    liaison-curated token, deliberately NOT wired) routes record-only, never the store token. Proves the
    care store-write rides the SAME gate, adding no trust-the-model path.
    """
    root = tmp_path / "store"
    scaffold = tmp_path / "scaffold"
    _seed(root)

    class _RawDrugBackend:
        def converse(self, messages):
            return {"reply": "ok", "extraction": {"rx-interaction-classes": "atorvastatin 20mg"}}

    care_chat.respond("I take atorvastatin", [], client=_RawDrugBackend(),
                      store_root=root, scaffold_root=scaffold)
    assert store.read("rx-interaction-classes", root=root) == [], (
        "a raw drug string the care agent proposed landed in the model-bound token (gate bypassed)"
    )


def test_respond_tolerates_a_malformed_conversation_entry(tmp_path):
    """A malformed conversation entry is skipped, not char-splatted into the payload (thread survival)."""
    root = tmp_path / "store"
    _seed(root)
    backend = _RecordingBackend()
    care_chat.respond("hi", [{"bad": "shape"}, "not-a-dict", {"role": "user", "content": "real"}],
                      client=backend, store_root=root)
    contents = [t["content"] for t in backend.calls[0]]
    assert "real" in contents, "a well-formed prior turn was dropped"
    assert "not-a-dict" not in contents, "a malformed entry was char-splatted into the payload"


def test_care_chat_route_answers_with_the_reply(tmp_path):
    """POST /care-chat answers with the Care Assistant reply (route wiring + thread survival).

    Drives the production `build_server` over tmp roots with an injected mock backend: a POST /care-chat
    turn returns the model reply as JSON; a malformed body degrades (never a dropped thread); an unknown
    POST still 404s. 0 live spend (mock backend, no key).
    """
    import http.client
    import threading

    from scripts.model.client import ModelClient
    from scripts.serve import server as serve_server

    class _Backend:
        def converse(self, messages):
            self.messages = messages
            return {"reply": "Thanks — I've noted your shoulder is left-side. What movements aggravate it?",
                    "extraction": []}

    backend = _Backend()
    _seed(tmp_path / "store")
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=ModelClient(backend=backend),
    )
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/care-chat",
                     body=json.dumps({"turn": "my left shoulder hurts",
                                      "conversation": [{"role": "assistant", "content": "Tell me about the shoulder."}]}).encode(),
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        data = json.loads(resp.read().decode())
        conn.close()
        assert resp.status == 200 and data["reply"].startswith("Thanks"), f"/care-chat did not answer: {data}"
        # the payload carried the de-id profile context + the opening question.
        wire = json.dumps(backend.messages)
        assert "care-conversation" in wire and "Tell me about the shoulder." in wire, "the care payload dropped the profile/opening"
        # a malformed body degrades, never drops the thread.
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/care-chat", body=b"not json{{{", headers={"Content-Type": "application/json"})
        bad = conn.getresponse()
        bad_body = json.loads(bad.read().decode())
        conn.close()
        assert bad.status != 200 and bad_body.get("degraded") is True, "a malformed care-chat body was not degraded"
    finally:
        srv.shutdown()
        srv.server_close()


def test_care_context_presents_weight_in_both_units_with_the_operator_preference(tmp_path):
    """The care context carries the weight in BOTH units (lb + kg) + the operator's chosen unit.

    The operator's complaint: they picked pounds but the assistant talked kg. The de-id summary carries
    `bodyweight-band` in kg; the care context now ALSO carries `operator_weight` in both units and
    `operator_weight_unit` (the captured preference), so the assistant leads with the operator's unit.
    Failing-capable: without this the context is kg-only.
    """
    import json as _json
    root = tmp_path / "store"
    scaffold = tmp_path / "scaffold"
    scaffold.mkdir(parents=True, exist_ok=True)
    store.append("bodyweight-kg", {"item": "bodyweight-kg", "timepoint": "2026-06-01T00:00:00+00:00",
                                   "source": "intake", "value": "108"}, root=root)
    (scaffold / "capture-2026-06-01T00-00-00.json").write_text(_json.dumps({"bodyweight-unit": "lbs"}))
    backend = _RecordingBackend()
    care_chat.respond("hi", [], client=backend, store_root=root, scaffold_root=scaffold)
    ctx = json.loads(backend.calls[0][0]["content"])
    assert ctx.get("operator_weight") == "238 lb (108 kg)", f"weight not presented in both units: {ctx.get('operator_weight')}"
    assert ctx.get("operator_weight_unit") == "pounds", f"the operator's unit preference is not carried: {ctx}"


def test_care_context_weight_both_units_even_without_a_captured_preference(tmp_path):
    """Even with NO captured unit preference (older intake), the context still carries BOTH units.

    So an operator whose intake predates the unit-capture still gets pounds in the assistant's context
    (their existing case), not kg-only — the preference just isn't asserted.
    """
    root = tmp_path / "store"
    store.append("bodyweight-kg", {"item": "bodyweight-kg", "timepoint": "2026-06-01T00:00:00+00:00",
                                   "source": "intake", "value": "108"}, root=root)
    backend = _RecordingBackend()
    care_chat.respond("hi", [], client=backend, store_root=root, scaffold_root=tmp_path / "no-scaffold")
    ctx = json.loads(backend.calls[0][0]["content"])
    assert ctx.get("operator_weight") == "238 lb (108 kg)", "the weight is not presented in both units without a preference"
    assert "operator_weight_unit" not in ctx, "a preference was asserted when none was captured"


def test_care_context_labels_chronological_age_and_glossarizes_the_token(tmp_path):
    """The care context presents the operator's age clearly + a glossary that `training-age-band` is age.

    `training-age-band` holds chronological age but its NAME implies training experience — which made
    the assistant re-ask "age or training years?". The context now carries `operator_age` + a
    `profile_glossary` clarifying the token, so the assistant leads with the operator's age and does not
    confuse it with lifting experience. Failing-capable: without the labeling the context is token-only.
    """
    root = tmp_path / "store"
    store.append("date-of-birth", {"item": "date-of-birth", "timepoint": "2026-06-01T00:00:00+00:00",
                                   "source": "intake", "value": "1970"}, root=root)
    backend = _RecordingBackend()
    care_chat.respond("hi", [], client=backend, store_root=root)
    ctx = json.loads(backend.calls[0][0]["content"])
    assert ctx.get("operator_age") and "years" in ctx["operator_age"], f"the age is not clearly labeled: {ctx.get('operator_age')}"
    glossary = ctx.get("profile_glossary", {})
    assert "training-age-band" in glossary and "chronological age" in glossary["training-age-band"], (
        f"the training-age-band token is not glossed as chronological age: {glossary}"
    )


def test_care_chat_persists_turn_and_get_conversation_restores(tmp_path):
    """A /care-chat turn is persisted to the conversation vault and GET /conversation restores it.

    The persistence + restore that makes conversations survive a reload (the operator never redoes
    them): a /care-chat POST records the operator turn + the assistant reply into a gitignored
    conversation file (sibling of the store), and GET /conversation?thread=care returns those turns.
    """
    import http.client
    import threading

    from scripts.model.client import ModelClient
    from scripts.serve import server as serve_server

    class _Backend:
        def converse(self, messages):
            return {"reply": "Noted — tell me more.", "extraction": []}

    _seed(tmp_path / "store")
    srv = serve_server.build_server(
        0, store_root=tmp_path / "store", dna_root=tmp_path / "dna",
        scaffold_root=tmp_path / "scaffold", client=ModelClient(backend=_Backend()),
    )
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("POST", "/care-chat",
                     body=json.dumps({"turn": "my left shoulder hurts", "conversation": [], "thread": "care"}).encode(),
                     headers={"Content-Type": "application/json"})
        conn.getresponse().read()
        conn.close()
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", "/conversation?thread=care")
        data = json.loads(conn.getresponse().read().decode())
        conn.close()
        turns = data["turns"]
        assert {"role": "user", "content": "my left shoulder hurts"} in turns, f"the operator turn was not restored: {turns}"
        assert any(t["role"] == "assistant" and t["content"] == "Noted — tell me more." for t in turns), (
            f"the assistant reply was not restored: {turns}"
        )
    finally:
        srv.shutdown()
        srv.server_close()
    assert (tmp_path / "conversations" / "care.md").exists(), "the conversation was not written to the gitignored vault"


def test_care_profile_carries_raw_health_detail_and_strips_pure_identity(tmp_path):
    """The care agent reads the operator's RAW health detail, with pure identity stripped.

    The operator -> care-agent link is private (the de-identification line is the care -> specialist
    hand-off), so the care profile carries the operator's ACTUAL peptide/supplement/diet/training/injury
    free-text — not the coarse specialist-facing bands — while legal name / exact DOB / contact / address
    stay absent (built on the identity-safe `router.summarize`, which never emits them; the DERIVED age
    still crosses). Failing-capable: reds if the detail is collapsed to a band, or if an identity item
    (raw name / raw DOB) appears in the profile.
    """
    import functools
    import json

    from scripts.serve import care_chat
    from scripts.store import store

    root = tmp_path / "store"
    tp = "2026-07-02T00:00:00+00:00"
    for item, value in [
        ("raw-peptide-free-text", "retatrutide 2mg/week titrating to 5mg, Glow stack"),
        ("raw-nutrition-free-text", "paleo, high protein"),
        ("raw-symptom-free-text", "left shoulder impingement, overhead press limited"),
        ("date-of-birth", "1971-03-04"),
        ("legal-name", "Jane Q Operator"),
    ]:
        store.append(item, {"item": item, "timepoint": tp, "source": "intake", "value": value}, root=root)

    # medications are record-only in the scaffold (raw drug names never de-identified) — the operator's
    # own agent still reads them; seed a scaffold capture carrying them.
    scaffold = tmp_path / "scaffold"
    scaffold.mkdir()
    (scaffold / "capture-2026-07-02T00-00-00+00-00.json").write_text(
        json.dumps({"rx-interaction-classes": "finasteride, testosterone, modafinil", "sleep-hours": "6.5"})
    )

    profile = care_chat._care_profile(functools.partial(store.read, root=root), scaffold_root=scaffold)
    # the operator's real specifics reach the agent (not a coarse band)
    assert "retatrutide" in profile["health_detail"]["peptides"]
    assert "paleo" in profile["health_detail"]["nutrition"]
    assert "impingement" in profile["health_detail"]["injuries"]
    # medications (record-only scaffold) reach the agent, clearly labelled
    assert "testosterone" in profile["health_detail"]["medications"]
    assert profile["record"]["sleep-hours"] == "6.5"
    # pure identity is stripped: no legal name, no raw birth date anywhere in the profile
    blob = json.dumps(profile).lower()
    assert "jane q operator" not in blob, "the operator's legal name leaked into the care profile"
    assert "1971-03-04" not in blob, "the operator's raw birth date leaked into the care profile"
    # but the DERIVED age (from the DOB) still crosses — the agent knows the operator is 55
    assert profile.get("training-age-band"), "the derived age should still be present for the agent"
