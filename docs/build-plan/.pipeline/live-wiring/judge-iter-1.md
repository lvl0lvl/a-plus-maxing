# Judge — Build Plan: Live-Wiring (iteration 1 of max 3)

**Plan:** `docs/build-plan/.pipeline/live-wiring/draft-plan.md`
**Source spec:** `docs/spec/live-wiring-spec.md`
**Validation:** `docs/build-plan/.pipeline/live-wiring/validation.md`
**Grounded live against:** `feature/engine-live-wiring-build @ 2a457de`, suite `1611 passed, 2 skipped` (re-run by this judge, 2026-06-24).

## AUTO-FAIL pre-check (run FIRST)

| Dimension | Auto-fail condition | Result |
|-----------|---------------------|--------|
| 1 Wave Integrity | task scheduled before its dependency | NOT TRIGGERED — W2-T2 dep T1(W1); W3-T3 dep T1/T2/0027-T1(W1/W2/W1); W3-T4 dep T1/T2(W1/W2); all predecessors in strictly-earlier waves |
| 2 Checkpoint Quality | checkpoint with no verification criteria | NOT TRIGGERED — all 3 boundaries carry named pytest/grep/numstat/exit-code gates |
| 3 Agent Assignment | impl task → Architect, or contract task → SE-only | NOT TRIGGERED — SE primary on all 5; Architect/Security are reviewers; the 3 seam/contract tasks all carry Architect review |
| 4 Critical Path | path includes a task NOT on the actual longest chain | NOT TRIGGERED — T1→T2→T3, length 3 = topo depth; T3 has the largest predecessor set (3) |
| 5 Risk Ordering | spike not in W1, or mitigating task after mitigated | NOT TRIGGERED — no spike (stated, Rule-1 exception); both crown-jewel boundaries in W1 before consumers |
| 6 Cross-Spec | two tasks both creating same file in same wave | NOT TRIGGERED — disjoint manifests verified per wave |
| 7 Spec Traceability | plan task not in any source spec | NOT TRIGGERED — 5 plan tasks ↔ 5 spec tasks, 1:1 |
| 8 Infrastructure | W1 task requires infra not listed | NOT TRIGGERED — all 8 prereqs listed + verified live |
| 9 Feedback Protocol | no protocol section, or missing category | NOT TRIGGERED — section present, 7 base + 4 project categories |
| 10 Downstream Readiness | missing wave schedule, or checkpoint w/o exit criteria | NOT TRIGGERED — wave schedule + per-boundary exit criteria present |

**No auto-fail.** Proceed to per-dimension scoring.

---

## Dimension 1 — Wave Integrity: 10/10

The three waves are the spec's three Kahn levels: W1 = {ADR-0027-T1, ADR-0026-T1} (both in-degree 0), W2 = {ADR-0026-T2}, W3 = {ADR-0026-T3, ADR-0026-T4}. Every dependency edge in the spec Dependency Map (`live-wiring-spec.md:164-173`) is honored by a strictly-earlier-wave placement:
- T2 dep T1 → W2 > W1 ✓
- T3 dep {T1, T2, 0027-T1} → W3 > {W1, W2, W1} ✓
- T4 dep {T1, T2} → W3 > {W1, W2} ✓

The build-vs-runtime divergence is correctly modeled: ADR-0026-T1 (keystone) has BUILD-dependency NONE on ADR-0027-T1 (it drives a fixture `dispatch`), so both are valid W1 entry points even though de-id-IN is the first RUNTIME stage. I verified this live: `run_orchestrated` already accepts a `dispatch`/`gate_dispatch`/`deid_client` seam (`plan_orchestrator.py:220`, the `deid_in(raw_intake, deid_client)` call at the loop head), so the extraction genuinely needs no live backend.

**Verification statement:** Each of the 4 dependency edges was checked against the spec Dependency Map and confirmed to place the dependent in a strictly-later wave; the two in-degree-0 entry points were confirmed build-independent against the live `run_orchestrated` seam signature. No violation.

## Dimension 2 — Checkpoint Quality: 10/10

Every checkpoint criterion is a concrete executable command with an expected result, not "tests pass" vagueness. Verified against the live tree:

- **W1 frozen-engine:** `git diff --numstat <wave-base>..HEAD -- scripts/plan/orchestrate.py …router.py → 0 changed lines` — the 8 named modules all exist live (confirmed). Binary, executable.
- **W1 no-fork:** a grep over `plan_orchestrator.py` + `SKILL.md` for a SECOND copy of the `while True:` sequencing → EXACTLY 1 definition. Concrete.
- **W1 suite-green:** `.venv/bin/python -m pytest -q → 1611 passed, 2 skipped`. I re-ran this live; it matches.
- **W1 de-id 0-leak — raw-intake-in-memory-only (QA-1):** the criterion is a `tmp_path`-as-HOME/CWD `rglob("*")` filesystem scan (NOT a `builtins.open` write-spy) PLUS a **mutation step** that injects a `path.write_text(raw_intake)` inside the call boundary and asserts the scan goes RED. This is the recently-hardened non-vacuous gate and it is concrete + binary (`[draft-plan.md:116]`).
- **W2 composer-driver seam (QA-4):** feeds `gate_dispatch`'s REAL output into `plan_driver`'s `safety_passed is True` surface gate over an accept fixture and a malformed fixture, asserting accept→≥1 plan / malformed→0 plans `SAFETY_BLOCKED`. This is the buildable-at-W2 seam assertion; it is concrete (`[draft-plan.md:138]`).
- **W3 audit→self-test exit-code chain (QA-3):** drives `_a_prime_self_test.py` with a known-broken promote-everything stub and asserts `bash scripts/core-capability-audit.sh` exits NON-zero — explicitly via exit code, with stdout/stderr suppressed. I verified the live audit consumes the self-test ONLY via exit code (`core-capability-audit.sh:68`, `"$PY" -m … --self-test >/dev/null 2>&1`), so this gate's premise (a printed-FAIL-but-exit-0 would read GREEN) is real and the gate correctly targets it (`[draft-plan.md:162]`).

Every boundary names a verifier role (Security + Architect/QA + `plan-integrity`).

**Verification statement:** I executed the W1 suite gate live (1611/2, match); confirmed the frozen-engine numstat target files all exist; confirmed the audit's exit-code-only consumption of the self-test (so QA-3's exit-code premise is grounded); confirmed the QA-1 mutation step and QA-4 seam are concrete commands. No vague criterion.

## Dimension 3 — Agent Assignment Fit: 10/10

SE implements all 5 tasks (TDD per recipe). Reviewers are correct:
- ADR-0027-T1 (de-id egress + `ModelClient`/`_call` cross-module seam) → Architect + Security. Correct: PII boundary → Security; cross-module contract → Architect.
- ADR-0026-T1 (KEYSTONE shared-driver extraction) → Architect (extracted-driver contract + frozen-inner-engine boundary) + Security (fail-closed loop single-source-of-truth). Correct.
- ADR-0026-T2 (cross-module gate composition → 3-key disposition) → Architect (fixed-3-key contract) + Security (fail-closed-on-malformed + ≥2-lens). Correct.
- ADR-0026-T3 (skill front-door, prose + thin glue) → Security only. Correct — implementation, not a new cross-module contract; Security per the crown-jewel-on-every-wave rule.
- ADR-0026-T4 (audit repoint + self-test) → Security only. Correct — implementation; the inversion behaviors are the crown-jewel guarantee Security owns.

No implementation task is assigned to Architect as PRIMARY; no contract/seam task ships SE-only without Architect review. `plan-integrity` is correctly a read-only verification lens, not a deployed agent (consistent with CLAUDE.md's branch-completeness exclusion).

**Verification statement:** Each task's ownership was checked against the assignment heuristic (security-wins on PII/safety; Architect on cross-module seam/contract; SE primary). All 5 match; the three seam/contract tasks (0027-T1, 0026-T1, 0026-T2) all carry Architect review.

## Dimension 4 — Critical Path Accuracy: 10/10

Longest chain: ADR-0026-T1 → ADR-0026-T2 → ADR-0026-T3, length 3 = the topological depth. Verified by predecessor-set counting: T3 has 3 predecessors (T1, T2, 0027-T1), the largest of any task, and no shorter alternate route to T3 exists. The parallel tail T1→T2→T4 is correctly identified as also zero-wave-slack but off the named longest chain by tie-break (T4's predecessor set {T1,T2} is strictly smaller than T3's {T1,T2,0027-T1}).

Slack is calculated for the non-critical task: ADR-0027-T1 is assigned **2 waves slack** (in-degree 0, build-independent, consumed only by T3 in W3; pulled to W1 by the crown-jewel-boundary-first risk rule, not the path). This is correct — its only consumer is W3, so it could slip to W2 without delaying completion.

**Verification statement:** Predecessor sets were enumerated from the spec Dependency Map; T3's set (size 3) is the unique maximum, confirming T1→T2→T3 is the longest chain and that ADR-0027-T1's 2-wave slack is accurately derived from its single W3 consumer.

## Dimension 5 — Risk Ordering: 10/10

No separate spike task exists; the plan states this EXPLICITLY and invokes the Rule-1 exception (the two highest-risk entries — the de-id crown-jewel boundary and the keystone behavior-preserving refactor — are full BUILD tasks placed in W1, not knowledge-gathering spikes; their open questions OQ-1/OQ-4 resolve in-task during TDD bounded by ACs). This is the correct handling, not an evasion.

Risk-mitigating-before-mitigated holds throughout:
- ADR-0027-T1 (de-id boundary, W1) precedes ADR-0026-T3 (the egress that dispatches over its output, W3) — by 2 waves.
- ADR-0026-T1 (the un-forked single shared loop, W1) precedes every task that drives the loop (T2 W2, T3/T4 W3).
- ADR-0026-T2 (fail-closed-on-malformed disposition, W2) precedes T3/T4 (W3) that drive the gate E2E.

Security ordering: both crown-jewel boundaries in W1 before any de-identified-summary dispatch; Security review carries through the terminal wave. The SEC-1 build-vs-runtime watch-item (a future edit giving the keystone a LIVE raw-intake path pre-boundary would invert the 0-leak property) is a load-bearing call-out, correctly flagged as an execute-time watch-item for `plan-integrity` + Security.

**Verification statement:** Confirmed against the live seam that ADR-0026-T1 drives a fixture `dispatch` (`plan_orchestrator.py:220`), so its W1 placement ahead of the de-id boundary introduces no live raw-PII path. Every mitigating task precedes its mitigated consumer by ≥1 wave. Spike-absence is stated and justified.

## Dimension 6 — Cross-Spec Consistency: 10/10

Single-spec plan (one source spec), so no cross-spec merge. Within-spec shared-file sequencing is clean: `plan_orchestrator.py` is touched by exactly ONE task (ADR-0026-T1). Per-wave intra-wave file check:
- W1 {0027-T1, 0026-T1}: disjoint — `{client.py, test_client.py}` vs `{plan_driver.py, plan_orchestrator.py, test_plan_driver.py}`.
- W2 {0026-T2}: single task.
- W3 {0026-T3, 0026-T4}: disjoint — `{SKILL.md, test_generate_plan_skill_glue.py}` vs `{core-capability-audit.sh, _a_prime_self_test.py, test_a_prime_self_test.py}`.

No two tasks create the same file in the same wave; no duplicate tasks; tier ordering (de-id Tier-1 sink, driver Tier-2) respected. I confirmed the Create-target files are all ABSENT live (`plan_driver.py`, `gate_dispatch.py`, `_a_prime_self_test.py` + the 4 new test files) and the Modify-target files all PRESENT.

**Verification statement:** Each wave's manifests were intersected and found disjoint; the single shared file (`plan_orchestrator.py`) has a single modifier; all Create targets confirmed absent and Modify targets present on the live tree.

## Dimension 7 — Spec Traceability: 10/10

Every plan task traces 1:1 to a spec task block:
- ADR-0027-T1 → spec `### ADR-0027-T1` (`live-wiring-spec.md:57`)
- ADR-0026-T1 → spec `### ADR-0026-T1` (:78)
- ADR-0026-T2 → spec `### ADR-0026-T2` (:103)
- ADR-0026-T3 → spec `### ADR-0026-T3` (:122)
- ADR-0026-T4 → spec `### ADR-0026-T4` (:141)

No orphan plan task; no spec task dropped (5 ↔ 5). The plan's checkpoint criteria cite specific spec AC numbers (e.g., `[ADR-0027-T1 crit 7]`, `[ADR-0026-T1 crit 4]`) and I spot-checked them: draft-plan's "raw-intake-in-memory-only [crit 7]" maps to spec AC-7 (in-memory-only, LOAD-BEARING); "injected-safety-not-True [crit 4]" maps to spec ADR-0026-T1 AC-4; "0-plans-on-safety-not-True [crit 4]" maps to spec ADR-0026-T4 AC-4. The `source-specs` frontmatter lists `docs/spec/live-wiring-spec.md`.

**Verification statement:** All 5 plan task IDs were located as `### <id>` blocks in the source spec; ≥3 cited AC-number cross-references were checked and resolve to the correct spec acceptance criteria. No orphan, no drop.

## Dimension 8 — Infrastructure Completeness: 10/10

All 8 prerequisites carry a runnable verification command; I executed the load-bearing ones live:
- `.venv` baseline → ran `pytest -q`, got `1611 passed, 2 skipped` (match).
- Inner-engine 8 modules → all PRESENT.
- `ModelClient.deidentify` stub + `deid_in` whitelist + `ModelCallError` → confirmed (`client.py` `NotImplementedError` stub, `MODEL="claude-opus-4-8"`, lazy SDK import + `key_source.resolve`; `deid_in.py` `set(summary) <= set(SUMMARY_FIELD_SET)` → `DEID_CALL_FAILED`; `ModelCallError` class present).
- Gate callables → `quality_judge` (`quality_judge.py:206`), `review_plan` + `DEFAULT_LENSES` 3 lenses (`safety_review.py:43,110`).
- Inline loop + `gate_dispatch=` seam + `_promote_plans`→`store.append` → all confirmed (`plan_orchestrator.py` `while True:` body, `_promote_plans` at :424, `store.append` at :459).
- SDK absent → confirmed (`importlib.util.find_spec('anthropic') is None`).
- Audit scaffold + negative test → `core-capability-audit.sh`, `audit-helpers.sh`, `scripts/tests/test_core_capability_audit.sh` all present.
- Agents roster → all 7 directories present.

The plan correctly states no W1 task depends on an unlisted prerequisite.

**Verification statement:** I ran 6 of the 8 prerequisite verification commands directly (baseline, inner-engine, de-id stub, gate callables, inline-loop, SDK-absent, agents) and every one returned the asserted result. No phantom infrastructure.

## Dimension 9 — Feedback Protocol: 10/10

The Feedback Protocol section (`draft-plan.md:217-233`) covers all 7 base build-planning categories (spec defect, missing dependency, untestable AC, scope change, file-manifest conflict, oversized task, missing task) each with a blocking/non-blocking classification, PLUS four project-specific release-blocking categories that map to this build's crown-jewel obligations: crown-jewel 0-leak RED, no-fork violation, EXTEND-NOT-REBUILD numstat violation, 0-live-spend violation. Each names a concrete HALT action and a route-to-owner. The blocking issues emit a specific remediation message routing to `/create-spec` then `/create-build-plan`; non-blocking issues log to `deviations.md`.

**Verification statement:** Each of the 7 base categories + 4 project categories was confirmed present with an explicit action and blocks-plan classification; no execution-failure category is missing.

## Dimension 10 — Downstream Readiness: 10/10

The plan is parseable by the task-planning skill: frontmatter carries `source-specs`, `adrs`, `total-waves`, `critical-path-length`; the Wave Schedule has per-wave task tables (ID/Title/Agent/Effort), Entry Criteria, and Exit Criteria pointing to a per-wave Checkpoint Protocol with binary exit criteria; the Agent Assignment Matrix, Critical Path, Risk Schedule, Cross-Spec Coordination, Feedback Protocol, and Validation Checklist are all present. Every checkpoint has named exit criteria (no boundary lacks a Go/No-Go). Artifacts-Present lists per wave name exact created/modified paths. The 0-live-spend invariant is asserted at every boundary.

**Verification statement:** The wave schedule, per-wave entry/exit criteria, agent matrix, critical path, and Go/No-Go blocks were all confirmed present and structured; no checkpoint is missing exit criteria; all required machine-parseable fields are populated.

---

## Per-dimension scores

| # | Dimension | Score |
|---|-----------|-------|
| 1 | Wave Integrity | 10 |
| 2 | Checkpoint Quality | 10 |
| 3 | Agent Assignment Fit | 10 |
| 4 | Critical Path Accuracy | 10 |
| 5 | Risk Ordering | 10 |
| 6 | Cross-Spec Consistency | 10 |
| 7 | Spec Traceability | 10 |
| 8 | Infrastructure Completeness | 10 |
| 9 | Feedback Protocol | 10 |
| 10 | Downstream Readiness | 10 |

**Minimum dimension: 10/10. Threshold (every dimension ≥9): MET.**

## Verdict: ACCEPT

Auto-fail: NONE triggered. All 10 dimensions ≥9 (all 10/10). The plan's load-bearing premises were verified live against `feature/engine-live-wiring-build @ 2a457de`: the suite baseline (1611/2), the de-id stub + `MODEL` attr + lazy SDK import + `key_source.resolve`, the SDK-absent patch posture, the inline `while True:` loop with its `safety_passed is True` gate / accept-promote / revise-cap / out-of-run-set guard / de-id-sentinel / dispatch-cap halts, the `_promote_plans`→`store.append` write, the audit's exit-code-only consumption of the self-test (grounding the QA-3 exit-code-chain gate), the gate callables + 3-lens `DEFAULT_LENSES`, the inner-engine 8 modules frozen-set, the Create-targets-absent / Modify-targets-present manifest, and the 7-agent roster. The recently-hardened gates (QA-1 tmp-tree-rglob-with-mutation, QA-3 audit-exits-nonzero-on-broken-spine, QA-4 W2 composer-driver seam) are concrete, binary, and grounded in real live mechanics.

No fix list (ACCEPT).

## Minor observations (non-deducting — for the author's awareness, not blocking)

- The plan cites the de-id stub at `client.py:156-160`; the live stub body is a few lines lower (the `deidentify` method's `NotImplementedError` block). The premise (a `NotImplementedError` stub behind the existing seam) is unchanged; only the exact line cite drifts slightly. Not load-bearing for any gate (every gate keys off function/grep, not line number). No deduction.
