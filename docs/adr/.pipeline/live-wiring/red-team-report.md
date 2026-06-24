# Red-Team Report — Plan-Generation Engine LIVE-WIRING ADR SET (ADR-0026 + ADR-0027)

**Phase:** 8 (red-team, whole-set). **Reviewed:** ADR-0026 (subscription-runtime driver A′),
ADR-0027 (live no-train de-id backend), read TOGETHER and against the existing ADRs they
amend/depend-on/constrain (0001/0005/0015/0016/0020/0021/0022/0023/0024/0025) + `dag.md` +
`rubric.md` + the 11-AP catalog + the LIVE code
(`plan_orchestrator.py`, `client.py`, `generate_plan.py`, `quality_judge.py`, `safety_review.py`,
`core-capability-audit.sh`, `generate-plan/SKILL.md`).

**Method:** adversarial-review 8-category walk (A/E/C/R/O/S/D/L) applied to the SET as a system —
the emphasis is cross-ADR contradictions, the keystone buildability claim, and the
core-capability-audit's ability to verify the A′ path. Individual ADRs already passed verify+judge
10/10; this walk hunts only what emerges when they are read together.

**Headline:** Two HIGH findings carry the report. **RT-01** — the keystone "share the helpers, drive
from the skill, don't fork, don't edit `run_orchestrated`" claim is NOT mechanically realizable as
written: the revise-loop CONTROL FLOW (the `while True:` + its mid-loop synchronous re-dispatch) is
inline in `run_orchestrated`, not a shareable helper, so A′ secretly requires EITHER a fork (the
A-naive option it rejects) OR a `run_orchestrated` edit (the frozen-engine breach it forbids); OQ-1
hides this. **RT-02** — the repointed `core-capability-audit.sh` cannot verify the REAL A′ path
(a skill driving subscription agents) with a shell grep + a Python `--self-test`; the audit's whole
reason to exist (PF-S63-02: prove the REAL core capability is wired) is defeated if it green-lights a
Python entrypoint that is NOT the live runtime. One genuine cross-ADR contradiction was found
(**RT-03**, the unattended/autonomous framing 0026↔0022). The KNOWN-deferred backfills are
correctly deferred and are listed verbatim below as the required FINAL-FIX work, not as defects.

---

## PART A — KNOWN-DEFERRED BACKFILL WORK (the dag-prescribed FINAL-FIX, NOT defects)

`dag.md §3/§9` prescribes that the 9 inverse Related-Decisions rows + the ADR-0022 Revision-History
amendment row are appended at the FINAL-FIX phase once BOTH new ADRs exist (a Tier-1 ADR may not
forward-reference a not-yet-authored Tier-2 ADR). VERIFIED absent today (0 hits of `ADR-0026`/`ADR-0027`
across all 7 existing ADRs + 0022 + 0020). This is the dag's correct sequencing — listed here as the
REQUIRED FINAL-FIX checklist, each exactly as `dag.md §3` spells it:

| # | Existing ADR | Inverse row to append | Type (existing ADR's side) |
|---|--------------|------------------------|----------------------------|
| DF-1 | ADR-0022 | `→ ADR-0026` (resolves OQ-1/OQ-3) **+ a Revision-History amendment row** (the exact text `dag.md §4` gives) | depends-on (inbound) |
| DF-2 | ADR-0020 | `→ ADR-0027` (implements the model-backed de-id-IN boundary) | depends-on (inbound) |
| DF-3 | ADR-0015 | `→ ADR-0026` (relates) **and** `→ ADR-0027` (enables) — two rows, matching 0015's existing convention | relates (0026) / enables (0027) |
| DF-4 | ADR-0001 | `→ ADR-0027` (the live form of the 0020↔0001 relaxation; tension stays anchored on 0020) | relates |
| DF-5 | ADR-0005 | `→ ADR-0027` (live raw-intake egress + key; tension stays anchored on 0020) | relates |
| DF-6 | ADR-0016 | `→ ADR-0027` (bounds the backend to the no-train lane) | constrains (inbound) |
| DF-7 | ADR-0006 | `→ ADR-0026` (the driver DRIVES the roster-assembly architecture) | relates |
| DF-8 | ADR-0023 | `→ ADR-0026` (gate_dispatch composes the judge verdict; resolves SHARED OQ-2) | depends-on (inbound) |
| DF-9 | ADR-0024 | `→ ADR-0026` (gate_dispatch composes the review result; resolves SHARED OQ-2) | depends-on (inbound) |

**Also deferred + required at FINAL FIX:** ADR-0022's OQ-1/OQ-3 + the SHARED-OQ-2 pointer must be
marked `RESOLVED-BY-ADR-0026` (annotated, not deleted) per `dag.md §4`. These are NOT counted as
findings. The ONLY backfill-class observation that IS a finding is RT-09 (a row the dag did NOT
enumerate — see Part B).

---

## PART B — NEW FINDINGS

### RT-01: The keystone "share the helpers, don't fork, don't edit `run_orchestrated`" claim is not mechanically realizable as written — the revise-loop CONTROL FLOW is inline, not a shareable helper

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradiction (intra-ADR, surfaced only by reading the ADR against the live loop structure) |
| **Severity** | High |
| **Affected ADRs** | ADR-0026 (Decision, Rationale "no-fork fidelity", Consequences Positive-1, Alternative A′, OQ-1, Falsification "frozen-engine probe") |
| **Affected File** | `scripts/plan/plan_orchestrator.py` (lines 136–305, the `run_orchestrated` body; specifically the `while True:` at 260 with `_safe_gate` at 261 and `_dispatch_domains` at 294) |
| **Resolution** | Prevent — OQ-1 must be promoted from "which file shape" to "DOES a helper-sharing skill driver realize the revise loop WITHOUT a fork or a `run_orchestrated` edit; if not, the no-fork claim is conditional and the ADR must say so." |

**Description.** The keystone correctness claim is: A′ keeps the safety loop in ONE place (Python)
because the new step-driver SHARES `run_orchestrated`'s helpers rather than re-implementing them, the
engine is byte-frozen (`numstat=0` on `run_orchestrated`), and the skill drives the agent dispatches
from outside. Stress-tested against the live structure, this does not hold for the DYNAMIC re-dispatch
the revise loop requires.

The helpers the ADR names as shareable — `_dispatch_domains`, `_safe_gate`, `_promote_plans`,
`_honest_no_plan` — are all LEAF operations (verified: each is a module-level `def`, lines 345/373/398/424).
But the LOOP CONTROL FLOW that sequences them is NOT a helper. It is the inline `while True:` block
inside `run_orchestrated` (lines 260–300): it calls `_safe_gate(gate_dispatch, result)` (the GATE
dispatch) at line 261, branches on the disposition, checks the cap, then calls
`_dispatch_domains(revise_domains, …)` (the SPECIALIST re-dispatch) at line 294 — and
`_dispatch_domains` synchronously calls `dispatch(domain, prompt, summary)` (line 369). The
re-dispatch DECISION ("which domains to re-author") is computed from the gate disposition produced by
the PREVIOUS pass, INSIDE the loop body.

Under A′ both `dispatch` (a subscription specialist agent) and `gate_dispatch` (the composed
judge∥safety, each a subscription agent) are Claude-Code agents the Python frame "cannot synchronously
spawn and pull output back from" — the ADR's own Context (Y-Statement, Context ¶2). So to run the
revise loop the skill must drive those two dispatches. But they are invoked from INSIDE the inline
`while True:`. There are exactly three ways to reconcile that, and the ADR endorses none cleanly:

1. **Re-implement the `while True:` control flow in the skill** so the skill owns the
   gate→branch→re-dispatch sequencing and only calls the leaf helpers — this is precisely
   **Alternative A-naive** ("the bounded loop … now lives in BOTH the Python `run_orchestrated` AND the
   skill prose, which can drift"), the option ADR-0026 REJECTS as the forked-safety-loop failure class.
   Sharing the leaf helpers does not avoid the fork: the fork is in the LOOP, not the leaves.
2. **Edit `run_orchestrated`** to invert control — e.g. turn the inline dispatch sites into
   yields/callbacks the skill resumes between agent dispatches. This is the **frozen-engine breach** the
   ADR's own falsification "frozen-engine probe" says must `halt` (`numstat > 0 on run_orchestrated`).
3. **Drive `run_orchestrated` from Python with a `dispatch` that bridges to skill-staged envelopes**
   (OQ-1's second sub-option) — but a Python `dispatch` that "synchronously returns a subscription
   agent's envelope into the call stack" is exactly **Alternative B**, which the ADR rejects for V1 as
   blocked by the synchronous-dispatch impossibility. You cannot pre-stage the revise-pass envelopes
   before the loop runs, because WHICH domains get re-dispatched is only known mid-loop from the gate
   disposition (line 286, `revise_domains = disposition.get("revise_domains")`).

OQ-1 frames the open item as cosmetic — "a standalone step-driver the skill calls between dispatches,
OR `run_orchestrated` invoked with a bridging `dispatch` … the choice does not change the decision,
only its realization." That is the contradiction: the choice DOES change the decision, because the
INITIAL-pass dispatch (a flat fan-out before any gate) can be staged-then-driven, but the REVISE-pass
re-dispatch (data-dependent, mid-loop) cannot be, with the loop frozen and unforked. The ADR's
no-fork claim is true for the initial pass and UNRESOLVED for the revise loop, and the ADR does not
say so.

**Evidence.**
- ADR-0026 Decision: "exposed to the skill through a NEW thin step-driver … that SHARES
  `run_orchestrated`'s helpers — it does not re-implement the loop and does not edit `run_orchestrated`."
- ADR-0026 Rationale (no-fork): "A′ exposes that floor to the skill as deterministic STEP entrypoints
  and shares the existing helpers (`_dispatch_domains`, `_safe_gate`, `_promote_plans`,
  `_honest_no_plan`, the disposition check)."
- ADR-0026 OQ-1: "Both forms share `_dispatch_domains`/`_safe_gate`/`_promote_plans`/`_honest_no_plan`;
  the choice does not change the decision, only its realization."
- LIVE: `plan_orchestrator.py:260` `while True:` … `:261` `disposition = _safe_gate(gate_dispatch, result)`
  … `:286` `revise_domains = disposition.get("revise_domains")` … `:294`
  `authors.update(_dispatch_domains(revise_domains, summary, gates, dispatch, budget))` — the gate
  dispatch and the specialist re-dispatch are BOTH invoked inside the inline loop, and the re-dispatch
  target is computed from the prior pass's disposition. The loop is not extracted to a helper; only its
  leaves are.

**Fix.** Rewrite OQ-1 (and add a sentence to the Decision + the no-fork Rationale) to make the
buildability question explicit and bounded: "OPEN: can a helper-sharing skill driver realize the
DATA-DEPENDENT revise re-dispatch (re-author the domains a mid-loop gate disposition names) WITHOUT
(a) re-implementing the `while True:` gate→branch→re-dispatch control flow in the skill — the A-naive
fork — OR (b) editing `run_orchestrated` to invert control past the dispatch sites — the frozen-engine
breach? The initial flat fan-out can be staged-then-driven; the revise loop cannot. If neither (a)
nor (b) is avoidable, the no-fork-AND-frozen-engine claim is CONDITIONAL — name which constraint
yields (a bounded, reviewed `run_orchestrated` control-inversion edit is the likeliest, and would make
the 'frozen-engine probe' falsification a SCOPED allowance, not an absolute `numstat=0`)." Until OQ-1
is resolved this way, the "0 duplicated copies of the loop logic" confirmation criterion and the
absolute frozen-engine falsification are in tension with the design they gate.

---

### RT-02: The repointed `core-capability-audit.sh` cannot verify the REAL A′ path — a shell grep + Python `--self-test` proves a NON-live entrypoint, defeating PF-S63-02's whole point

| Field | Value |
|-------|-------|
| **Category** | D — Downstream Breakage + S — Scope (the "mechanical repoint, not a decision" exclusion hides an unverifiable-by-construction problem) |
| **Severity** | High |
| **Affected ADRs** | ADR-0026 (Validation "core-capability-audit.sh is repointed … and passes its `--self-test`"; `dag.md §9` "the mechanical core-capability-audit repoint … rides ADR-0026's Validation Approach as a confirmation criterion, NOT a new ADR") |
| **Affected File** | `scripts/core-capability-audit.sh` (CALLER pin `:47`, the grep checks `:54-57`, the behavioral self-test `:68`); `scripts/plan/generate_plan.py` (`_self_test` `:454-537`, a SINGLE-domain `compute_plan→assemble→record_plan` path); `scripts/plan/plan_orchestrator.py` (`run_orchestrated`, the A′ path, NO production caller) |
| **Resolution** | Prevent — the repoint is NOT mechanical; it hides a real decision (what a shell audit CAN assert about a skill-driven path) and must be lifted out of the "excluded as mechanical" bucket into an explicit Open Question or a follow-on ADR. |

**Description.** `core-capability-audit.sh` is the PF-S63-02 mechanical guard: its job is to prove the
REAL core capability — generating a followable plan end-to-end — stays WIRED, so "is it wired?" is a
CHECKED answer not a remembered one. It does this two ways: (1) STRUCTURAL — grep the CALLER
(`generate_plan.py`) for `assemble(` + `record_plan(` (`:54-57`); (2) BEHAVIORAL — run
`generate_plan --self-test` under `.venv` (`:68`), which authors a fixture envelope through a mock
backend and asserts a dashboard renders.

ADR-0026's A′ decision MOVES the real V1 runtime OFF this path. The live A′ sequence (dag.md §7) is:
de-id IN → the SKILL dispatches subscription specialist AGENTS → `run_orchestrated`'s revise loop →
`reinsert_out` → `reemit_maintained`. Two facts make the audit unable to verify that:

1. **`generate_plan.generate_plan` is NOT on the A′ path.** It is the SINGLE-DOMAIN Wave-2 caller
   (`compute_plan` → `assemble` → `record_plan`). The A′ runtime goes through `run_orchestrated` →
   `pipeline.run_generation` (VERIFIED: `run_orchestrated` calls `pipeline.run_generation`, not
   `generate_plan.generate_plan`; and `run_orchestrated` has NO production caller today — `rg
   run_orchestrated scripts/` finds only its own def + the budget docstring, which ADR-0026 Context
   itself states). So "repoint the CALLER from `generate_plan.py` to the live-wired engine front door"
   has no Python file to point at that IS the live path: the front door is the `/generate-plan` SKILL.
2. **A shell audit cannot invoke a skill session or assert subscription-agent dispatch.** The
   behavioral check runs `"$PY" -m scripts.plan.<module> --self-test`. A `--self-test` can only run the
   DETERMINISTIC mock-backend path (no live agent, no live API — by design, so it runs in CI, per
   `generate_plan.py:_self_test`). It therefore proves the Python plumbing, NOT that the SKILL drives
   real specialists over the de-identified summary into the frozen loop. The thing PF-S63-02 exists to
   catch — components green in isolation while the REAL assembled path is unbuilt — is exactly what a
   mock-backed self-test of a non-live entrypoint would MISS. A green audit over `run_orchestrated`'s
   `--self-test` (with a fixture `dispatch`) would assert "the loop runs with injected envelopes,"
   which is true and was true BEFORE A′ — a tautological pass against the A′ capability (the project's
   own "No Tautological Tests" mandate).

ADR-0026 and `dag.md §9` both classify this as "mechanical … NOT a new ADR." It is not mechanical:
deciding WHAT a shell audit can assert about a skill-driven, agent-dispatching path — and whether the
PF-S63-02 guard can mechanically cover the A′ runtime at all, or must be supplemented by an
operator-present LIVE-test attestation (the S94 live test the ADRs reference) — is a genuine decision
with a real risk if gotten wrong (a green guard over a path that is not the live one).

**Evidence.**
- `core-capability-audit.sh:47` `CALLER="${CORE_CAP_CALLER:-$REPO_ROOT/scripts/plan/generate_plan.py}"`;
  `:54` `grep -Eq 'assemble\(' "$CALLER"`; `:68` `"$PY" -m scripts.plan.generate_plan --self-test`.
- `generate_plan.py:543-545` docstring: "Interactive plan generation runs via the orchestrator
  (runtime A), not this CLI — the only CLI action is the deterministic self-test."
- `plan_orchestrator.py:148` `run_orchestrated` "drives `pipeline.run_generation`"; VERIFIED no
  production caller of `run_orchestrated`.
- ADR-0026 Validation: "the audit's CALLER pin (currently `scripts/plan/generate_plan.py`) moves to
  the driver path, and its grep/self-test targets assert the engine path (de-id → subscription dispatch
  → `run_orchestrated` → `reinsert_out` → maintained render) is wired." — A shell grep + a mock
  self-test cannot assert "subscription dispatch."

**Fix.** Remove the "mechanical, not a decision" classification for the repoint. Add an Open Question
to ADR-0026 (or a short follow-on ADR): "Given A′'s live path is skill-driven (a subscription-agent
dispatch loop), what CAN `core-capability-audit.sh` mechanically assert, and what must move to an
operator-present LIVE-test attestation? Candidate split: (a) the audit STRUCTURALLY asserts the
deterministic-driveable spine is wired — `run_orchestrated` exists, shares the helpers, calls
`pipeline.run_generation`, and a fixture-`dispatch` `--self-test` runs de-id→loop→promote→render
end-to-end (this is real and non-tautological IF the self-test asserts PROMOTION-on-accept and
0-plans-on-not-True, exercising the A′ inversion, not just 'a plan renders'); (b) the audit CANNOT
assert the skill drives real agents — that is the S94 LIVE-test's job, recorded as a release-gating
attestation, not a shell check." Make explicit that the CALLER pin moves to a Python module on the A′
SPINE (`plan_orchestrator.py` / a new step-driver), not `generate_plan.py`, and that the self-test
must exercise the revise-loop inversion (RT-01), or the guard is green against the wrong path.

---

### RT-03: Cross-ADR contradiction — ADR-0022's "unattended / repeatable" chosen-capability vs ADR-0026's "cannot run truly unattended (no human session present)"

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradiction (cross-ADR, the highest-value check) |
| **Severity** | Medium |
| **Affected ADRs** | ADR-0022 (Decision, Rationale "autonomy/repeatability", Consequences Positive-1, Alternative A "When this becomes the right choice"); ADR-0026 (Consequences Negative-1, Y-Statement) |
| **Resolution** | Prevent — ADR-0026 already names the gap once; it must RECONCILE it against 0022's load-bearing word, not just record the coupling, and the ADR-0022 amendment row (DF-1) is the place to do it. |

**Description.** ADR-0022's chosen capability — the reason it supersedes S68 — is "repeatable
UNATTENDED end-to-end generation" (Y-Statement), "run the full generate→judge→safety-review→revise
loop UNATTENDED and repeatably" (Positive-1), justified because "a human-driven session does not scale
to running the loop repeatedly or unattended." The word "unattended" is load-bearing in 0022 — it is
the discriminator against Alternative B (the interactive session).

ADR-0026 then selects A′, whose Negative-1 says the V1 runtime "is a Claude Code SUBSCRIPTION SESSION,
not a headless service — plan generation cannot run truly UNATTENDED (no human session present); it is
'autonomous within a session'." So the runtime 0026 wires does NOT deliver the unattended capability
0022 chose. This is a genuine contradiction in the framing: 0022 sells "unattended," 0026 delivers
"autonomous within a session, NOT unattended." A reader taking 0022 at face value would believe V1 can
run headless/scheduled; 0026 says it cannot.

The two are RECONCILABLE — 0022's real discriminator was "without a human walking EACH safety-relevant
DISPATCH by hand," and A′ does remove the per-dispatch human checkpoint (the human starts a session;
the session then drives all dispatches autonomously). But 0026 only RECORDS the gap as a coupling
negative ("the live form of the subscription-coupling negative ADR-0022 recorded"); it does not
correct 0022's overclaim. ADR-0022 read alone still asserts "unattended" as a delivered V1 property,
which A′ falsifies.

**Evidence.**
- ADR-0022 Y-Statement: "to achieve repeatable UNATTENDED end-to-end generation."
- ADR-0022 Positive-1: "The engine CAN run the full generate→judge→safety-review→revise loop
  UNATTENDED and repeatably."
- ADR-0026 Negative-1: "plan generation cannot run truly UNATTENDED (no human session present); it is
  'autonomous within a session'."

**Fix.** In the ADR-0022 Revision-History amendment row (DF-1, authored at FINAL FIX) add one
sentence: "ADR-0026's A′ selection refines this ADR's 'unattended' to 'autonomous WITHIN a subscription
session, no per-dispatch human checkpoint' — a human starts the session; truly headless/scheduled
execution is the all-API North-Star cutover (ADR-0015 seam), not V1." And in ADR-0026 Negative-1,
change "the live form of the subscription-coupling negative ADR-0022 recorded" to additionally state
"this REFINES ADR-0022's 'unattended' claim, which A′ delivers as 'autonomous-within-session', not
headless." This converts a silent contradiction into an explicit refinement.

---

### RT-04: ADR-0026 folds two sub-decisions (gate_dispatch composition topology + specialist/lens dispatch wiring) into a "select a driver model" ADR — AP-08 (Mega-ADR) pressure that the fold acknowledges but the Decision sentence buries

| Field | Value |
|-------|-------|
| **Category** | S — Scope + systemic AP-08 check |
| **Severity** | Low |
| **Affected ADRs** | ADR-0026 (Decision, metadata `amends-posture`, Revision History; `dag.md §"Decision set"` records the fold) |
| **Resolution** | Accept (documented) — the fold was adjudicated at the Discovery gate and the composed `gate_dispatch` IS downstream of the driver choice; flagged for the record per the systemic AP sweep, not a blocking fix. |

**Description.** The systemic AP-08 sweep asks: does any ADR cram independent decisions joined by
"and"? ADR-0026's Decision contains three things — (1) adopt A′; (2) "The composed `gate_dispatch`
adapter … is folded into this driver model"; (3) the specialist/lens dispatch wiring. `dag.md` records
this as a deliberate fold ("ADR-0026 … folds the composed `gate_dispatch` topology (discovery #3) +
the subscription specialist/safety-lens dispatch wiring (discovery #5)"). The fold is DEFENSIBLE — the
gate-composition shape and the dispatch wiring are both consequences of WHO drives (the A′ choice), not
independent axes — and the Discovery gate resolved both fold-candidates. So this is not a true Mega-ADR
(the sub-items depend-on the driver choice; they are not unrelated topics joined by "and"). But the
Decision SENTENCE understates it: a reader scanning only Decision + Y-Statement sees "select a driver
model" and may miss that the composed-gate topology (the SHARED OQ-2, a build-blocking control-flow
decision) is being resolved HERE.

**Evidence.** ADR-0026 Decision: "The composed `gate_dispatch` adapter and the specialist/lens dispatch
wiring are folded into this driver model." `dag.md §"Decision set"` fold column for ADR-0026.

**Fix (accept, optional).** No structural change required (the fold is correct and recorded). If
desired, add a half-sentence to the Decision making the fold visible at a glance: "(this ADR also fixes
the composed `gate_dispatch` topology and the subscription dispatch wiring as direct consequences of
the A′ choice — see Related Decisions 0023/0024)." Recorded here so the systemic AP-08 sweep is not
silently "N/A."

---

### RT-05: ADR-0026's OQ-2 defers the composed-gate topology to spec, but its own Validation "confirmation criterion" ALREADY ASSERTS a concrete gate_dispatch return shape — an ordering/dependency gap a spec author hits

| Field | Value |
|-------|-------|
| **Category** | O — Ordering/Dependency Gap + E — Edge Case |
| **Severity** | Medium |
| **Affected ADRs** | ADR-0026 (Validation confirmation criterion #2 vs OQ-2; the SHARED OQ-2 it inherits from ADR-0023/0024) |
| **Affected File** | `scripts/plan/plan_orchestrator.py:261-294` (the single-disposition loop the composite must fit); `scripts/plan/quality_judge.py:206-253` (`{verdict, dimensions, deductions}`); `scripts/plan/safety_review.py:110-169` (`{findings, passed, lenses}`) |
| **Resolution** | Prevent — state in OQ-2 that the disposition KEYS (`accept`/`safety_passed`/`revise_domains`) are FIXED by the frozen loop and only the COMPOSITION (one gate vs two, ordering, re-trigger) is open, so a spec author does not read the two as contradictory. |

**Description.** ADR-0026 confirmation criterion #2 states a concrete contract: gate_dispatch "returns
`{accept: verdict==ACCEPT, safety_passed: review.passed, revise_domains: ...}`." But OQ-2 says the
composed-gate topology (one combined gate vs two, ordering, re-trigger rule, joint cap) is UNRESOLVED
and deferred to spec/build-plan. A spec author reading both sees a confirmation criterion asserting the
exact return shape AND an open question saying the shape is undecided — which is authoritative?

The reconciliation (correct, but unstated): the frozen loop at `plan_orchestrator.py:261-294` CONSUMES
exactly three disposition keys — `safety_passed` (line 265, must be `is True`), `accept` (line 271),
`revise_domains` (line 286). Those KEYS are fixed by the byte-frozen loop and are NOT open. What OQ-2
leaves open is the COMPOSITION that PRODUCES them (whether quality and safety are one gate pass or two,
their ordering, the re-trigger rule, the joint cap) — i.e. the adapter's INTERNALS, not its output
contract. The ADR knows this (OQ-2: "the loop already reads one `{accept, safety_passed,
revise_domains}` disposition … a two-loop topology would need the composer … within the frozen loop's
contract"), but criterion #2 and OQ-2 read as contradictory to a fresh spec author who has not made
that distinction.

**Evidence.**
- ADR-0026 Validation criterion #2: "returns `{accept: verdict==ACCEPT, safety_passed: review.passed,
  revise_domains: ...}`."
- ADR-0026 OQ-2: "one combined gate vs two, quality-vs-safety ordering, the re-trigger rule, the joint
  iteration cap … or does it require a richer disposition shape?"
- LIVE: `plan_orchestrator.py:265` `disposition.get("safety_passed") is True`; `:271`
  `disposition.get("accept") is True`; `:286` `disposition.get("revise_domains")` — three fixed keys.

**Fix.** Add to OQ-2: "NOTE: the disposition OUTPUT KEYS (`accept`, `safety_passed`, `revise_domains`)
are FIXED by the byte-frozen loop (`plan_orchestrator.py:261-294`) and are NOT open — confirmation
criterion #2 pins them deliberately. OQ-2 is open ONLY on the adapter's INTERNAL composition (one gate
pass vs two, ordering, re-trigger, joint cap) that produces those keys. A two-pass topology must still
emit exactly that 3-key disposition." This removes the apparent contradiction.

---

### RT-06: Runtime-stage-order coherence across 0026+0027+0021 — COHERENT, with one terminology slip (`gate_dispatch` "∥" parallel vs the loop's SEQUENTIAL single-disposition read)

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradiction (cross-ADR/cross-doc, low-severity) + R — Reference |
| **Severity** | Low |
| **Affected ADRs** | `dag.md §7` stage 3 ("`{quality judge ∥ safety review}` composed via `gate_dispatch`"); ADR-0026 Validation criterion #2 ("runs `quality_judge` ∥ `review_plan`") |
| **Affected File** | `scripts/plan/plan_orchestrator.py:261` (the loop reads ONE disposition, sequentially) |
| **Resolution** | Accept — the `∥` is documented in dag.md as "both gate at this stage," not literal concurrency; harmless but worth a one-word note so a spec author does not infer required parallelism. |

**Description.** The runtime stage order (de-id IN → subscription dispatch+assemble → {judge ∥ safety}
composed gate → revise → deterministic de-id OUT → maintained render) is COHERENT across the set: 0027
owns stage 1, 0026 owns stages 2–4, 0021 (deterministic, model-free) owns stage 5, 0025 owns stage 6.
The asymmetry (model-backed de-id IN, deterministic model-FREE de-id OUT) is stated consistently —
ADR-0021 body: "no model on the OUT path at all"; ADR-0027: model call on the IN path; no ADR implies a
model on the OUT path. The PII-IN/OUT envelope is consistent. This is a PASS on the composition check.

The only slip is the `∥` notation. `dag.md §7` itself defines it ("the `∥` denotes 'both gate at this
stage'") so it is not literally a concurrency claim, but ADR-0026 criterion #2 reuses "`quality_judge`
∥ `review_plan`" without the gloss, and the frozen loop reads a SINGLE composed disposition
sequentially (one `_safe_gate` call at line 261). A spec author could over-read `∥` as "must dispatch
the two gates concurrently," which the loop neither requires nor supports.

**Evidence.** `dag.md §7` stage 3 + its gloss; ADR-0026 criterion #2 "runs `quality_judge` ∥
`review_plan`"; `plan_orchestrator.py:261` single sequential `_safe_gate`.

**Fix (accept).** In ADR-0026 criterion #2, change "runs `quality_judge` ∥ `review_plan`" to "runs
`quality_judge` AND `review_plan` (both gate at this stage; the order/concurrency is the OQ-2
composition, the loop consumes one composed disposition)." Cosmetic; prevents an over-read.

---

### RT-07: Shared-terminology consistency — PASS, with one drift: ADR-0027 says the de-id summary is "`SUMMARY_FIELD_SET`-shaped"; ADR-0022/the design doc call the dispatch input the "`router.summarize` summary" — confirm these name the SAME contract

| Field | Value |
|-------|-------|
| **Category** | R — Broken/Inconsistent Reference (terminology) |
| **Severity** | Low |
| **Affected ADRs** | ADR-0027 (Decision, Y-Statement: "`SUMMARY_FIELD_SET`-bounded summary"); ADR-0020 (`router.summarize` survives as persisted-side de-id); ADR-0026 (dispatches over "the de-identified summary") |
| **Affected File** | `scripts/plan/deid_in.py:71-72` (enforces `SUMMARY_FIELD_SET` subset); `scripts/plan/router.py` (`router.summarize`, `SUMMARY_FIELD_SET`) |
| **Resolution** | Accept — the set IS internally consistent (the de-id-IN output and the `router.summarize` output are both `SUMMARY_FIELD_SET`-bounded BY CONSTRUCTION, which is the design intent); noted so a reader does not think two different summaries exist. |

**Description.** Across the set the de-identified dispatch input is named three ways:
"`SUMMARY_FIELD_SET`-bounded summary" (0027), "the de-identified `router.summarize` summary" (0022,
the design doc, `generate_plan.py` docstrings), and "the de-identified summary the de-id-IN boundary
emits" (0026). These are intended to be the SAME contract: `deid_in` enforces the live backend's output
keys ⊆ `SUMMARY_FIELD_SET` (`deid_in.py:71-72`), and `router.summarize` derives over the same closed
`SUMMARY_FIELD_SET` — so both the live IN output and the persisted-side derivation are
`SUMMARY_FIELD_SET`-shaped by construction. The set is consistent. The only risk is a reader inferring
that the live de-id summary (0027) and the `router.summarize` summary (0022) are DIFFERENT objects;
they are the same SHAPE (the whitelist is the bridge), with 0027 producing it live for the plan path
and `router.summarize` producing the persisted-side one.

**Evidence.** ADR-0027 Decision: "a subset of `SUMMARY_FIELD_SET`"; `deid_in.py:71-72` (subset
enforcement); ADR-0020 "`summarize` survives as the persisted-side de-id"; ADR-0026 RD-0027 row "the
de-identified summary … that summary is the driver's input contract."

**Fix (accept).** Optionally add one clause to ADR-0027's Decision: "(the same `SUMMARY_FIELD_SET`
shape `router.summarize` emits persisted-side — `deid_in` enforces the subset, so the live IN summary
and the persisted summary share one contract)." Prevents the two-summaries misread. No correctness
issue.

---

### RT-08: Quantitative-claim consistency across >1 ADR — PASS (model id, pricing, dispatch cap) with one UNVERIFIED-tag asymmetry on the no-train retention window

| Field | Value |
|-------|-------|
| **Category** | C — Contradiction (quantitative cross-check) |
| **Severity** | Low |
| **Affected ADRs** | ADR-0027 (`claude-opus-4-8`, $5/$25 MTok, OQ-2 ~30-day no-train); ADR-0026 (rides the same `MODEL`); ADR-0020 (OQ-2 retention, UNVERIFIED) |
| **Resolution** | Accept — the numbers are consistent and correctly tagged; the retention window is consistently UNVERIFIED across 0020→0027 (inherited), which is correct, not a defect. |

**Description.** The quantitative claims appearing in more than one ADR are consistent: the de-id model
is `claude-opus-4-8` (0027 Decision + Rationale, matching the live `client.py:135` `MODEL`), and
ADR-0026 rides "the same `MODEL` attribute" for the de-id call without restating a different id. The
pricing ($5/$25 input/output per MTok for Opus; Sonnet $3/$15; Haiku $1/$5; Fable $10/$50) appears only
in 0027, tagged `[VENDOR-CLAIM]`. The dispatch cap is referenced by name (`DEFAULT_DISPATCH_CAP`), not
a literal, in both the code and 0026 — no number to conflict. The no-train retention window (~30 days)
is carried as 0027 OQ-2, explicitly inherited from ADR-0020 OQ-2 and tagged `[UNVERIFIED]` in BOTH —
a CONSISTENT non-claim (the set does not assert a verified window anywhere), which is the correct
posture. No contradiction.

**Evidence.** ADR-0027 Rationale pricing line `[VENDOR-CLAIM]`; `client.py:135` `MODEL =
"claude-opus-4-8"`; ADR-0027 OQ-2 "inherited from ADR-0020 OQ-2 … `[UNVERIFIED]`."

**Fix.** None required. Recorded so the quantitative cross-check is not silently "N/A."

---

### RT-09: Backfill roster GAP — ADR-0025 reciprocation for the A′ runtime is not in the dag's §3 list, yet ADR-0022 carries `ADR-0025 depends-on (inbound)` for "the orchestrator's reviewed plan"; A′ changes WHO produces that plan

| Field | Value |
|-------|-------|
| **Category** | R — Broken Reference + E — Edge Case (a relationship the dag did NOT enumerate) |
| **Severity** | Low |
| **Affected ADRs** | ADR-0025 (its `depends-on ADR-0022` "renders THIS orchestrator's reviewed plan"); ADR-0026 (the driver that now produces that plan); `dag.md §3` (no ADR-0025 ↔ ADR-0026 row) |
| **Resolution** | Handle — decide explicitly whether ADR-0025 needs ANY edge to ADR-0026. Likely NOT (0025 renders `run_orchestrated`'s output regardless of WHO drives it), but the set should STATE that, so the absence is a reasoned exclusion, not an oversight. |

**Description.** `dag.md §3` enumerates 9 inverse backfills (0022/0020/0015×2/0001/0005/0016/0006/0023/0024).
ADR-0025 is NOT among them — neither new ADR claims an edge to 0025. That is DEFENSIBLE: ADR-0025
renders `run_orchestrated`'s output, and A′ does not change `run_orchestrated`'s output shape, so 0025
is unaffected. BUT ADR-0022 ALREADY carries `ADR-0025 | depends-on (inbound) | … renders THIS
orchestrator's reviewed plan and re-emits it on new data; the orchestrator is the producer whose output
the re-emit lifecycle maintains.` ADR-0026 now FIXES who/what that producer-runtime is (the A′ driver).
So there is a transitive question the set leaves silent: does ADR-0025's "the orchestrator is the
producer" now point at the A′ driver (0026), warranting at least a `relates` note, or is 0025
deliberately edge-free to the live-wiring set? The dag does not say, and a downstream reader cannot
tell whether the absence is reasoned or missed.

**Evidence.** `dag.md §3` (9 rows, no 0025); ADR-0022 RD table `ADR-0025 | depends-on (inbound) | …
the orchestrator is the producer whose output the re-emit lifecycle maintains`; ADR-0026 Decision (the
driver "DRIVES … `reemit_maintained`" per dag.md §7 stage 6).

**Fix.** Add one line to `dag.md §3` (or §7) stating the reasoned exclusion: "ADR-0025 takes NO edge to
the live-wiring set: it renders `run_orchestrated`'s output and re-emits on new data REGARDLESS of who
drives the loop; A′ does not change the rendered output's shape, so 0025's existing `depends-on
ADR-0022` (the producer-runtime) needs no 0026 reciprocation. Recorded so the absence is a decision, not
an omission." This closes the silent gap without inventing an edge.

---

## PART C — SYSTEMIC ANTI-PATTERN SWEEP (the SET, not the individual ADRs)

| AP / systemic check | Verdict over the SET | Note |
|---------------------|----------------------|------|
| AP-01 Fairy Tale / weak Negatives | **PASS** | Both ADRs carry substantive, code-grounded Negatives (0026: subscription-session coupling, the new seam, non-determinism; 0027: live raw egress, no per-request no-train flag, hard network dependency, new raw-input surface). Not a systemic AP-03. |
| AP-04 Dummy Alternative (obvious-loser sweep) | **PASS** | Neither ADR has a strawman. 0026's A-naive and B are GENUINELY viable (A-naive "the simplest single-surface story," B "the strongest no-fork story in principle, future-adopted") — each with a "when this becomes the right choice." 0027's B (cheaper tier) and C (deterministic NER) both carry real advantages + win-conditions. No systemic AP-04. |
| Falsification quality (systemic) | **PASS** | Every Validation has quantitative falsification thresholds (0026: "≥1 duplicated copy → halt", "0 plans surfaced", "numstat > 0 → halt"; 0027: "0 raw-PII hits", "≥1 plan over a fabricated summary = breach", "0 API-key hits"). NOT the "review periodically" failure. CAVEAT: 0026's "frozen-engine probe" (absolute `numstat=0`) is in tension with RT-01 — if the revise loop needs a control-inversion edit, that falsification must become a SCOPED allowance. |
| AP-08 Mega-ADR | **Borderline — RT-04** | ADR-0026 folds gate-composition + dispatch wiring into "select a driver model"; defensible (downstream of the driver choice, adjudicated at Discovery) but understated in the Decision sentence. Low. |
| AP-06 Tunnel Vision (data-subject perspective) | **PASS** | Both ADRs explicitly bind "the data subject, not only the operator" (0027 Context ¶3; 0026 Context "the data subject's safety, not only the operator's convenience"). Multi-stakeholder. |
| AP-07 Blueprint-in-disguise | **PASS** | Both keep retry/backoff/exact-file-shape in OQs (0027 OQ-4, 0026 OQ-1), not the Decision. No over-specification. |

---

## Cross-ADR contradiction verdict

**One genuine cross-ADR contradiction found: RT-03** (ADR-0022 "unattended" vs ADR-0026 "not truly
unattended / autonomous-within-session"). Reconcilable, but ADR-0022 read alone overclaims a V1
capability A′ does not deliver; the fix is one sentence in the DF-1 amendment row + one in ADR-0026
Negative-1.

The composition checks PASS: the runtime stage order is coherent (RT-06 is a notation slip, not a
contradiction); the PII IN/OUT asymmetry (model-backed IN, deterministic model-free OUT) is stated
consistently across 0020/0021/0027 with no ADR implying a model on the OUT path; shared terminology
(subscription / no-train API / de-identified summary / `SUMMARY_FIELD_SET` / `gate_dispatch` /
fail-closed) is consistent (RT-07 is a same-shape naming note); quantitative claims (model id, pricing,
dispatch cap, retention) are consistent (RT-08).

**The most serious finding is RT-01 (keystone buildability), closely followed by RT-02
(core-capability-audit cannot verify the A′ path).** Both are HIGH and both attack the same soft spot:
A′'s claim that the live runtime is a skill driving subscription agents while the safety loop stays
frozen, unforked Python is asserted but not shown to be MECHANICALLY realizable (RT-01) or MECHANICALLY
verifiable (RT-02). Neither blocks the ADR from being a sound DECISION — A′ is the right driver model —
but both must be lifted out of "OQ-1 is just the file shape" / "the audit repoint is mechanical" into
explicit, resolved Open Questions before the spec/build-plan, or the build will hit the fork-vs-edit
dilemma (RT-01) and ship a green guard over the wrong path (RT-02).

---

## Coverage

| Category | Findings |
|----------|----------|
| A — Ambiguity | (folded into RT-01 OQ-1 ambiguity, RT-05 criterion-vs-OQ ambiguity) |
| E — Edge Cases | RT-05, RT-09 |
| C — Contradictions | RT-01, RT-03, RT-06, RT-08 |
| R — References | RT-07, RT-09 (+ Part A backfill verification: 9 deferred rows confirmed absent) |
| O — Ordering/Dependency | RT-05 |
| S — Scope | RT-02, RT-04 |
| D — Downstream | RT-02 |
| L — Language Economy | No blocking finding — both ADRs are dense but load-bearing (the Y-Statements are long but each clause is a real constraint; AP-R5 fresh-agent test passes). Not flagged. |

**9 findings: 2 High (RT-01, RT-02), 2 Medium (RT-03, RT-05), 5 Low (RT-04, RT-06, RT-07, RT-08, RT-09).**
High/High+Med ratio = 4/9 ≈ 44% — at the AP-R1 self-check line; justified because the two High findings
are the keystone + the PF-S63-02 guard, and the Mediums are a real cross-ADR contradiction + a
spec-author ordering trap, not inflation. The 5 Lows are honest accept/note-grade.
