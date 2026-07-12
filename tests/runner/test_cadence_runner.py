"""The cadence runner driver + dispatch seam tests (ADR-0039-T1).

The runner DRIVES the already-built plan loop through its single entry
`plan_loop.signal(root, trigger=CADENCE_TRIGGER, dispatch=..., deid_client=...)`; it re-hosts
none of the loop and edits nothing frozen. These tests fire the whole read -> de-id-IN ->
dispatch -> gate -> promote chain over injected fixtures at 0 live spend and 0 real operator PII.

The crown-jewel arms MIRROR `tests/serve/test_plan_loop_regen.py` — its `_SummarizeDeid` (faithful
de-id), `_LeakDeid` (faithless whitelist-passing de-id), `_seed_raw_pii` (synthetic legal name +
raw med into the RAW intake), `_regen_root` (a debounce-passing seeded store), and its synthetic
tokens (`_SYNTHETIC_NAME` / `_SYNTHETIC_DRUG`, provably disjoint-from-operator + non-structural) are
imported and reused here so the shapes are identical. The subscription SESSION the driver obtains
is a `(name, prompt, context) -> envelope` callable, so the precedent's `_TrendDispatch` (that same
shape) doubles as the recording fixture session end-to-end.
"""

import importlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts.model.client import ModelClient
from scripts.serve import plan_loop
from scripts.store import plan_schema, store

from scripts.runner import cadence_runner, subscription_dispatch

from tests.serve.test_plan_loop_regen import (
    _LeakDeid,
    _ON_DATE,
    _REGRESSING,
    _SummarizeDeid,
    _SYNTHETIC_DRUG,
    _SYNTHETIC_NAME,
    _TrendDispatch,
    _regen_root,
    _seed_raw_pii,
)

# The repo root — anchors the frozen-glob / serve-edit subprocess git checks (cwd-independent) and
# the AC-10 resolved-root assertion. tests/runner/test_cadence_runner.py -> tests -> <repo root>.
REPO_ROOT = Path(__file__).resolve().parents[2]


class _RecordingSession:
    """A minimal recording subscription session: records each routed tuple, returns a fixed envelope."""

    def __init__(self, envelope):
        self.envelope = envelope
        self.calls = []

    def __call__(self, name, prompt, context):
        self.calls.append({"name": name, "prompt": prompt, "context": context})
        return self.envelope


# =====================================================================================
# Cycle 1 — the dispatch seam + the SEC-04 default-factory refusal --------------------
# =====================================================================================


def test_default_session_factory_refuses(monkeypatch):
    # AC-9 (SEC-04): the DEFAULT (non-injected) session factory refuses to build a live subscription
    # session while the ADR-0039-T2 auth env-scrub is unapplied — the scrub-absent predicate the test
    # controls (the scrubbed-env marker absent). Failing-capable: a factory that RETURNED a session
    # under scrub-absent would not raise, reddening the pytest.raises. T2 lifts by applying the scrub
    # (setting the marker), needing NO edit to this scrub-absent assertion.
    monkeypatch.delenv(subscription_dispatch.SUBSCRIPTION_ENV_SCRUBBED_MARKER, raising=False)
    with pytest.raises(subscription_dispatch.SubscriptionEnvNotScrubbed):
        subscription_dispatch.default_session_factory()


def test_build_dispatch_routes_to_session():
    # Seam shape (supports AC-1/AC-5/AC-6): build_dispatch(session) returns a
    # dispatch(name, prompt, context) that routes the tuple to the session and returns its author
    # envelope (the built plan_orchestrator.py:148 seam shape) — it reads no store, de-identifies
    # nothing, re-hosts no loop logic.
    envelope = {"specialist": "personal-trainer", "recommendations": []}
    session = _RecordingSession(envelope)
    dispatch = subscription_dispatch.build_dispatch(session)
    returned = dispatch("workout", "PROMPT-TEXT", {"goal-domains": ["strength"]})
    assert session.calls == [
        {"name": "workout", "prompt": "PROMPT-TEXT", "context": {"goal-domains": ["strength"]}}
    ]
    # RECONCILED (bead mk0i): build_dispatch now runs the author envelope through
    # `normalize_author_output` (a value-preserving no-op on a well-formed envelope, so still equal),
    # so the return is a normalized COPY, not the identical object. Value equality is the contract.
    assert returned == envelope


def test_build_dispatch_normalizes_author_output_but_not_judge_lens():
    # bead mk0i: build_dispatch coerces a model AUTHOR envelope's scalar-contract rec fields to the
    # frozen `assemble` shape (a list `category` -> None fail-closed; a list `claim` -> joined), so a
    # malformed author output cannot crash the frozen composer mid-run. A judge/lens verdict (no
    # `recommendations` list) passes through unchanged.
    bad_author = {"specialist": "peptide-specialist", "recommendations": [
        {"claim": ["a", "b"], "category": ["stimulant"], "source": "x",
         "confidence_tier": "moderate", "reversibility": "reversible"}]}
    dispatch = subscription_dispatch.build_dispatch(_RecordingSession(bad_author))
    rec = dispatch("peptides", "P", {})["recommendations"][0]
    assert rec["claim"] == "a b" and rec["category"] is None        # SPACE-joined (SEC-02); category fail-closed

    judge = {"scores": {"quality": 8}, "accept": True}
    assert subscription_dispatch.build_dispatch(_RecordingSession(judge))("judge", "P", {}) == judge


def test_subscription_dispatch_import_is_inert(monkeypatch):
    # AC-7 (import-inert, subscription_dispatch arm): freshly importing the seam module fires 0
    # signal, 0 de-id (0 self-constructed ModelClient), 0 dispatch — building the seam arms nothing.
    signal_calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda *a, **k: signal_calls.append((a, k)))
    client_inits = []
    real_init = ModelClient.__init__

    def spy_init(self, *a, **k):
        client_inits.append(self)
        return real_init(self, *a, **k)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)
    importlib.reload(importlib.import_module("scripts.runner.subscription_dispatch"))
    assert signal_calls == [], "importing subscription_dispatch fired plan_loop.signal"
    assert client_inits == [], "importing subscription_dispatch constructed a ModelClient (de-id)"


# =====================================================================================
# Cycle 2 — the cadence runner driver: single signal(CADENCE) + crown-jewel + freeze --
# =====================================================================================


def test_single_signal_call(tmp_path, monkeypatch):
    # AC-1: cadence_runner.run over a debounce-passing store invokes plan_loop.signal EXACTLY ONCE.
    root = _regen_root(tmp_path, "one-signal", _REGRESSING)
    calls = []
    real_signal = plan_loop.signal

    def spy(*a, **k):
        calls.append((a, k))
        return real_signal(*a, **k)

    monkeypatch.setattr(plan_loop, "signal", spy)
    session = _TrendDispatch()
    cadence_runner.run(root, dispatch_factory=lambda: session,
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert len(calls) == 1, f"cadence_runner.run invoked plan_loop.signal {len(calls)} times, want 1"


def test_cadence_trigger_label(tmp_path, monkeypatch):
    # AC-2: the single signal call carries trigger == CADENCE_TRIGGER ("cadence"), never the
    # DATA_EVENT_TRIGGER / FREE_TEXT_TRIGGER labels. Failing-capable: a driver hardcoding another
    # trigger reddens this.
    root = _regen_root(tmp_path, "cadence-label", _REGRESSING)
    captured = {}
    real_signal = plan_loop.signal

    def spy(root_arg, **k):
        captured.update(k)
        return real_signal(root_arg, **k)

    monkeypatch.setattr(plan_loop, "signal", spy)
    session = _TrendDispatch()
    cadence_runner.run(root, dispatch_factory=lambda: session,
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    assert captured.get("trigger") == plan_loop.CADENCE_TRIGGER == "cadence", (
        f"the cadence tick used trigger {captured.get('trigger')!r}, want plan_loop.CADENCE_TRIGGER"
    )
    assert captured.get("trigger") not in (plan_loop.DATA_EVENT_TRIGGER, plan_loop.FREE_TEXT_TRIGGER)


def test_crownjewel_faithful_zero_raw_pii(tmp_path):
    # AC-5(a): the crown-jewel PROVEN-NON-EMPTY faithful arm. Seed synthetic raw PII into the RAW
    # intake + a debounce-passing store; fire ONE cadence tick with a SUCCESS-returning fixture
    # deid_client (_SummarizeDeid). Assert the recording dispatch captured >=1 payload PER
    # PLAN_DOMAINS member (>=4, proven-non-empty) AND 0 raw-PII tokens across every payload.
    root = _regen_root(tmp_path, "cj-faithful", _REGRESSING)
    _seed_raw_pii(root)
    raw = json.dumps(store.read_all(root))
    assert _SYNTHETIC_NAME in raw and _SYNTHETIC_DRUG in raw, (
        "the synthetic raw PII was not seeded into the raw intake — the wire-scan would be vacuous"
    )
    session = _TrendDispatch()
    cadence_runner.run(root, dispatch_factory=lambda: session,
                       deid_client=_SummarizeDeid(root), plan_date=_ON_DATE)
    spec = session.spec_calls()
    captured_domains = {c["name"] for c in spec}
    assert set(plan_schema.PLAN_DOMAINS) <= captured_domains, (
        "not every plan domain was dispatched (payload set not proven-non-empty): "
        f"missing {set(plan_schema.PLAN_DOMAINS) - captured_domains}"
    )
    assert len(spec) >= len(plan_schema.PLAN_DOMAINS)
    wire = json.dumps(session.calls)
    assert _SYNTHETIC_NAME not in wire, "the raw legal name reached a dispatch payload (de-id breach)"
    assert _SYNTHETIC_DRUG not in wire, "the raw med reached a dispatch payload (de-id breach)"
    # positive control: the wire genuinely carries de-identified summary content (not an empty pass)
    assert '"recent-trend-direction": "regressing"' in wire, (
        "the dispatched wire carried no de-identified summary content — the 0-hit scan is vacuous"
    )


def test_crownjewel_faithless_leak_detected(tmp_path):
    # AC-5(b): the crown-jewel FAILING-CAPABLE de-id-bypass arm. Swap in a FAITHLESS deid_client
    # (_LeakDeid) whose summary embeds the seeded legal name in an ALLOWED in-set VALUE (passes
    # deid_in's key whitelist + the non-structural value-scan). Assert the seeded token REACHES >=1
    # dispatch payload — proving AC-5(a)'s scan is non-vacuous (it CAN go RED on a real leak).
    root = _regen_root(tmp_path, "cj-leak", _REGRESSING)
    _seed_raw_pii(root)
    session = _TrendDispatch()
    cadence_runner.run(root, dispatch_factory=lambda: session,
                       deid_client=_LeakDeid(root), plan_date=_ON_DATE)
    assert session.spec_calls(), "the faithless de-id produced no dispatch (the guard is void)"
    wire = json.dumps(session.calls)
    assert _SYNTHETIC_NAME in wire, (
        "a faithless de-id that echoed the raw name into an in-set value did NOT surface in the "
        "wire — the AC-5(a) wire-scan would not catch a real leak (tautology)"
    )


def test_local_store_only_deid_in_invoked(tmp_path):
    # AC-6: local-store-only + de-id-IN proven-invoked. (b) deid_client.deidentify fired >=1 over the
    # seeded store; (a) the ONLY seam receiving raw store content is deid.deidentify — the dispatch
    # (the other outbound seam) carries 0 raw store tokens.
    root = _regen_root(tmp_path, "local-only", _REGRESSING)
    _seed_raw_pii(root)

    class _CountingDeid:
        def __init__(self, inner):
            self.inner = inner
            self.calls = 0
            self.received = []

        def deidentify(self, raw_intake):
            self.calls += 1
            self.received.append(raw_intake)
            return self.inner.deidentify(raw_intake)

    deid = _CountingDeid(_SummarizeDeid(root))
    session = _TrendDispatch()
    cadence_runner.run(root, dispatch_factory=lambda: session, deid_client=deid, plan_date=_ON_DATE)
    assert deid.calls >= 1, "deid_client.deidentify was never invoked — the sole-egress claim is vacuous"
    wire = json.dumps(session.calls)
    assert _SYNTHETIC_NAME not in wire and _SYNTHETIC_DRUG not in wire, (
        "raw store content reached the dispatch seam outside the de-id-IN call"
    )
    assert any(_SYNTHETIC_NAME in json.dumps(r, default=str) for r in deid.received), (
        "the de-id-IN call did not receive the raw intake — the sole-egress assertion is misplaced"
    )


def test_cadence_runner_import_is_inert(monkeypatch):
    # AC-7 (import-inert, cadence_runner arm): freshly importing the driver fires 0 signal, 0 de-id
    # (0 self-constructed ModelClient), 0 dispatch — building/importing the driver arms nothing (the
    # __main__ guard keeps main() from running on import).
    signal_calls = []
    monkeypatch.setattr(plan_loop, "signal", lambda *a, **k: signal_calls.append((a, k)))
    client_inits = []
    real_init = ModelClient.__init__

    def spy_init(self, *a, **k):
        client_inits.append(self)
        return real_init(self, *a, **k)

    monkeypatch.setattr(ModelClient, "__init__", spy_init)
    importlib.reload(importlib.import_module("scripts.runner.cadence_runner"))
    assert signal_calls == [], "importing cadence_runner fired plan_loop.signal"
    assert client_inits == [], "importing cadence_runner constructed a ModelClient (de-id)"


def test_extend_not_rebuild_no_rehost_no_serve_edit():
    # AC-3: extend-not-rebuild. The runner names 0 re-host tokens and drives plan_loop.signal INSIDE
    # scripts/serve/plan_loop.py WITHOUT editing that frozen containment host.
    # Scope note (PF-S63-02 mis-fire, S112/2026-07-07): assertion #2 formerly diffed the WHOLE
    # scripts/serve/ dir, which over-broadly tripped on the legitimate non-runner render-filter edit to
    # server.py (a non-frozen, non-runner file). Scoped to plan_loop.py (the frozen containment host,
    # also covered by the sibling frozen-glob numstat assertion) so it no longer over-blocks non-runner
    # serve edits, while still asserting the runner drives-but-does-not-edit the containment host.
    src = ((REPO_ROOT / "scripts/runner/cadence_runner.py").read_text()
           + (REPO_ROOT / "scripts/runner/subscription_dispatch.py").read_text())
    for token in ("_should_regenerate", "compose_disposition", "orchestrate.generate_plans",
                  "plan_driver.drive", "MIN_REGEN_INTERVAL_DAYS"):
        assert src.count(token) == 0, f"the runner re-hosts a loop symbol (extend-not-rebuild): {token}"
    out = subprocess.run(
        ["git", "diff", "--name-only", "origin/main", "--", "scripts/serve/plan_loop.py"],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True,
    )
    assert out.stdout.strip() == "", f"the runner edited the frozen plan_loop.py containment host: {out.stdout!r}"


def test_frozen_glob_numstat_empty():
    # AC-4: the canonical frozen superset (7 plan-engine files + plan_orchestrator.py + plan_driver.py
    # + scripts/store/ + scripts/serve/plan_loop.py, SEC-03 / Security-M1 / Architect-F3) is byte-frozen.
    frozen = [
        # scripts/plan/orchestrate.py CARVED OUT — ADR-0043-T2 (reconcile via cross_domain_seams) superseded the orchestrator; behavioral guarantor tests/serve/test_orchestrator_reconcile.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
        "scripts/plan/pipeline.py",
        # scripts/plan/assemble.py CARVED OUT — ADR-0041-T2 (uniform-program migration) superseded the assemble composer; behavioral guarantor tests/plan/test_assemble.py + tests/plan/test_generate_plan_uniform.py. Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
        # scripts/plan/generate_plan.py CARVED OUT — ADR-0042/0041/0046/0043 operator-signed-off (HARD) superseded plan front door; guarded by tests/plan/test_generate_plan.py + core-capability-audit.sh + per-ADR numstat probes. Architect ruling docs/adr/.pipeline/frozen-guard-reconciliation-ruling.md §2, feature/comprehensive-plan-adr.
        "scripts/plan/adjudicate.py", "scripts/plan/adjust.py",
        # scripts/plan/track.py CARVED OUT — ADR-0044-T2 (mixed-history reader re-point of resolve_plan_progress) superseded track.py; behavioral guarantor tests/store/test_plan_model_reader.py + tests/plan/test_track.py. Wave-3 frozen-guard reconciliation (F-011), Architect Option-A ruling.
        "scripts/plan/plan_orchestrator.py", "scripts/plan/plan_driver.py",
        # scripts/store/ frozen EXCEPT plan_model.py (ADR-0044-T1 NEW plan-model store) +
        # plan_schema.py (ADR-0044-T1 record-spine supersession); behavioral guarantor
        # tests/store/test_plan_model.py. Recursive glob-minus-exclusion (mirrors
        # _FROZEN_ENGINE_PATHS) keeps every OTHER current + future store file frozen — INCLUDING
        # a subtree stream (scripts/store/<pkg>/x.py); the "no new store stream" guarantee
        # survives (HIST-01). Wave-2 frozen-guard reconciliation, Architect Option-A ruling.
        *sorted(
            str(p.relative_to(REPO_ROOT))
            for p in (REPO_ROOT / "scripts" / "store").glob("**/*.py")
            if p.name not in ("plan_model.py", "plan_schema.py")
        ),
        "scripts/serve/plan_loop.py",
    ]
    out = subprocess.run(
        ["git", "diff", "--numstat", "origin/main", "--", *frozen],
        capture_output=True, text=True, cwd=REPO_ROOT, check=True,
    )
    assert out.stdout.strip() == "", f"the frozen glob changed (SEC-03 violation): {out.stdout!r}"


def test_main_entry_wires_run(monkeypatch):
    # AC-10: main(argv=None) is the launchd -> module -> run() entry. It calls run EXACTLY ONCE with
    # the DEFAULT dispatch_factory (a reference — NOT invoked, so no session constructs / no pre-scrub
    # raise ⇒ T2-stable), a CONSTRUCTED deid_client, and the RESOLVED repo-anchored store root.
    # 0-spend: run is spied (default factory never invoked) + ModelClient.__init__ is a no-op.
    captured = {}

    def run_spy(root, *, dispatch_factory, deid_client, tailor_client=None, plan_date=None):
        captured["root"] = root
        captured["dispatch_factory"] = dispatch_factory
        captured["deid_client"] = deid_client
        captured["calls"] = captured.get("calls", 0) + 1
        return {"spied": True}

    monkeypatch.setattr(cadence_runner, "run", run_spy)
    monkeypatch.setattr(ModelClient, "__init__", lambda self, *a, **k: None)
    cadence_runner.main([])
    assert captured.get("calls") == 1, "main() did not call run exactly once"
    assert captured["dispatch_factory"] is subscription_dispatch.default_session_factory, (
        "main() did not pass subscription_dispatch's default session factory"
    )
    # bead 940o: main wraps the de-id ModelClient in the timeseries-aggregating + output-normalising
    # adapter, so the metered de-id sees biomarker summaries (not thousands of raw readings) and its
    # list-valued output is coerced to the string shape the assemble/translate consumers expect.
    from scripts.serve.intake_aggregate import AggregatingDeidClient
    assert isinstance(captured["deid_client"], AggregatingDeidClient), (
        "main() did not wrap the de-id client in the AggregatingDeidClient adapter (bead 940o)"
    )
    assert isinstance(captured["deid_client"]._inner, ModelClient), (
        "the aggregating adapter must wrap a real ModelClient de-id"
    )
    assert captured["root"] == REPO_ROOT / store.DEFAULT_ROOT, (
        f"main() passed root {captured['root']!r}, want the resolved repo-anchored store root"
    )


def test_module_dash_m_resolvable():
    # AC-10: the module is `python -m scripts.runner.cadence_runner`-resolvable (exposes main + is
    # guarded so it runs only as the module entry, never on import — AC-7).
    import importlib.util

    assert importlib.util.find_spec("scripts.runner.cadence_runner") is not None
    assert callable(cadence_runner.main), "cadence_runner exposes no callable main()"
    src = (REPO_ROOT / "scripts/runner/cadence_runner.py").read_text()
    assert 'if __name__ == "__main__":' in src, "cadence_runner lacks the __main__ entry guard"
