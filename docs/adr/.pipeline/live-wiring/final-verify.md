# Final-Verification Report — Plan-Generation Engine LIVE-WIRING ADR SET (Phase 8)

**Phase:** 8 (final verification, post-remediation). **Verifier role:** confirm EVERY red-team finding
(RT-01…RT-09) is fixed, the PART-A backfills (DF-1…DF-9) are append-only, bidirectionality is closed,
and no new contradiction/anti-pattern was introduced.

**Inputs read:** `red-team-report.md` (9 findings + DF roster); ADR-0026 (fixed); ADR-0027 (fixed);
`dag.md`; the 9 backfilled existing ADRs (via `git diff`); the LIVE
`scripts/plan/plan_orchestrator.py` (citation re-checks).

**HEADLINE: PASS on all checks. TOTAL FAIL COUNT = 0.** No remediation pass required.

---

## Per-finding verdicts

### RT-01 (HIGH) — keystone mechanism rewrite → **PASS**

ADR-0026 no longer claims `run_orchestrated` is byte-frozen / numstat=0. The real mechanism is stated
consistently across every load-bearing section:

- **Y-Statement (L3):** "`run_orchestrated`'s inline gate→branch→re-dispatch loop is EXTRACTED (a
  behavior-preserving refactor of the S92-authored orchestrator wrapper, NOT the byte-frozen inner
  engine) … so the loop logic exists ONCE (no fork), the inner engine stays byte-frozen, and
  `run_orchestrated`'s public behavior is preserved by the full existing test suite staying green."
- **Decision (L26):** "a **behavior-preserving control-inversion refactor of `run_orchestrated`**
  (the S92-authored WRAPPER, not the byte-frozen inner engine)" — the inline `while True:` is
  EXTRACTED into ONE shared driver both consumers drive; byte-frozen is scoped to the inner engine
  (`pipeline.run_generation etc.`, numstat=0).
- **Rationale (L32, "no-fork fidelity"):** explicitly states the floor "is not just the leaf helpers
  — it is the INLINE loop CONTROL FLOW," and that "Sharing only the leaf helpers … does NOT avoid
  forking that loop." A′ "EXTRACTS the loop control flow itself into ONE shared inverted driver."
- **Consequences Positive-1 (L41):** "0 duplicated copies of the revise-loop control flow … The
  no-fork property is ACHIEVED (not merely asserted): the loop sequencing itself, not only its leaf
  helpers, is the single definition."
- **Alternative A′ (L57):** "the inline revise loop is EXTRACTED into one shared control-inversion
  driver (a behavior-preserving refactor of the S92-authored `run_orchestrated` WRAPPER, the
  byte-frozen inner engine untouched)."
- **Falsification — frozen-engine probe (L102):** rewritten to THREE thresholds: (i) numstat=0 on the
  byte-frozen INNER ENGINE only (the WRAPPER "may take numstat > 0"); (ii) 0 duplicated loop copies by
  grep; (iii) the full existing test suite (1600+) stays green across the refactor.
- **OQ-1 (L115):** now the REAL bounded question — "the SHAPE of the shared control-inversion driver
  (generator/coroutine vs step state-machine) … and the EXACT extract boundary"; it names the
  data-dependent revise re-dispatch as WHY a shared inverted driver is required and leaf-sharing is
  not. Explicitly: "The no-fork-via-SHARED-DRIVER decision is FIXED here … What is OPEN is only the
  driver's realization shape." Not cosmetic.

**Residual-claim scan:** `grep` for "byte-frozen run_orchestrated" / "share helpers only" /
"does not re-implement the loop and does not edit `run_orchestrated`" → 0 hits in any load-bearing
section. The ONLY surviving leaf-helper-sharing language is the Revision-History **Initial-draft row
(L124)** — a clearly-historical record — with the very next row (L125) documenting the RT-01
correction. Allowed historical exception. **PASS.**

### RT-02 (HIGH) — core-capability-audit repoint de-mechanicalized → **PASS**

The "mechanical" framing is removed; an OQ was added; the resolved split is stated:

- **Validation criterion #4 (L97):** "`core-capability-audit.sh` asserts the DETERMINISTIC PYTHON
  SPINE is wired — and is HONEST about what a shell check can and cannot prove." The CALLER pin "moves
  to a module ON the A′ SPINE (`plan_orchestrator.py` / the new shared driver — **NOT `generate_plan.py`**,
  which is the Wave-2 single-domain caller and is NOT on the A′ path)"; the `--self-test` asserts the
  A′ inversion behaviors (**promotion-on-accept** + **0-plans-on-safety-not-True**) so the pass is
  non-tautological; the live subscription dispatch is "the S94 operator-present LIVE-test attestation
  (a release-gating record, not a shell check)."
- **OQ-4 (L118):** explicitly states "The repoint is NOT mechanical — it hides a real decision about
  what a shell audit can prove of a skill-driven path," and carries the resolved (a)-spine / (b)-S94
  split.
- The repoint is no longer called mechanical and no longer targets `generate_plan.py` as the live
  path. **PASS.**

### RT-03 (MED) — unattended → autonomous-within-session, BOTH sides → **PASS**

- **ADR-0026 Negative-1 (L46):** "This REFINES ADR-0022's 'unattended' claim: A′ delivers 'autonomous
  WITHIN a subscription session (no per-dispatch human checkpoint),' not headless/scheduled — a human
  starts the session, which then drives all dispatches autonomously."
- **ADR-0022 Revision-History amendment row (DF-1 diff, 2026-06-24):** carries the same refinement
  sentence — "ADR-0026's A′ selection refines this ADR's 'unattended' to 'autonomous WITHIN a
  subscription session (no per-dispatch human checkpoint)' — a human starts the session; truly
  headless/scheduled execution is the all-API North-Star cutover (ADR-0015 seam), not V1."

Both sides present. **PASS.**

### RT-04 / RT-05 / RT-06 (ADR-0026 small fixes) → **PASS (all three)**

- **RT-04 (Decision fold half-sentence):** present — "(this ADR also fixes the composed `gate_dispatch`
  topology and the subscription dispatch wiring as direct consequences of the A′ choice — see Related
  Decisions 0023/0024)" (L26; grep count = 1).
- **RT-05 (OQ-2 NOTE pinning the 3 fixed keys):** present — OQ-2 (L116): "**NOTE: the disposition
  OUTPUT KEYS (`accept`, `safety_passed`, `revise_domains`) are FIXED by the loop … and are NOT open**
  — Validation confirmation criterion #2 pins them deliberately."
- **RT-06 (∥ → AND):** present — criterion #2 (L95): "runs `quality_judge` AND `review_plan` (both
  gate at this stage; order/concurrency is the OQ-2 composition; the loop consumes one composed
  disposition)" (grep "both gate at this stage" count = 1).

### RT-07 (ADR-0027) — SUMMARY_FIELD_SET same-contract clause → **PASS**

ADR-0027 Decision (L25): "(the same `SUMMARY_FIELD_SET` shape `router.summarize` emits persisted-side
— `deid_in` enforces the subset, so the live IN summary and the persisted summary share ONE contract,
not two distinct summaries)" (grep count = 1).

### RT-09 (dag.md) — ADR-0025 reasoned-exclusion line → **PASS**

`dag.md §3` (L111-114): "**Reasoned exclusion — ADR-0025 (RT-09).** ADR-0025 takes NO edge to the
live-wiring set — it renders `run_orchestrated`'s output and re-emits on new data REGARDLESS of who
drives the loop; A′ does not change the rendered output's shape … Recorded so the absence is a
decision, not an omission."

---

## PART A — DF-1…DF-9 APPEND-ONLY backfill check → **PASS (all 9)**

`git diff` run per existing ADR. Removed-line accounting: 0022 removed=3, 0023 removed=1, 0024 removed=1,
all OTHERS removed=0. Every removed line was verified to be an **OQ row or the SHARED-OQ-2 prose-pointer
re-emitted in place WITH a `RESOLVED-BY-ADR-0026` annotation appended** — the prescribed in-place
annotation pattern, never a deletion. A targeted grep confirmed **0 removed lines touch any
Y-Statement / Decision / Rationale / Context / Consequences / Alternatives** heading-anchored line in
any of the three.

| DF | ADR | Diff content (all additive / in-place annotation) | Type matches dag.md §3? |
|----|-----|---------------------------------------------------|-------------------------|
| DF-1 | 0022 | NEW inbound `ADR-0026 \| depends-on (inbound)` RD row; NEW Revision-History amendment row; in-place `[RESOLVED-BY-ADR-0026]` on OQ-1 + OQ-3; in-place `RESOLVED-BY-ADR-0026` annotation on the SHARED-OQ-2 prose-pointer | YES — depends-on inbound + amendment row + OQ-1/OQ-3 + SHARED-OQ-2 prose-pointer annotation. **PASS** |
| DF-2 | 0020 | NEW inbound `ADR-0027 \| depends-on (inbound)` RD row + Revision-History row | YES — depends-on (inbound). **PASS** |
| DF-3 | 0015 | TWO NEW RD rows: `ADR-0026 \| relates` AND `ADR-0027 \| enables` + Revision-History row | YES — relates (0026) / enables (0027), matching 0015's convention. **PASS** |
| DF-4 | 0001 | NEW `ADR-0027 \| relates` RD row + Revision-History row; tension stays anchored on 0020 | YES — relates. **PASS** |
| DF-5 | 0005 | NEW `ADR-0027 \| relates` RD row + Revision-History row; tension stays anchored on 0020 | YES — relates. **PASS** |
| DF-6 | 0016 | NEW `ADR-0027 \| constrains` RD row + Revision-History row | YES — constrains. **PASS** |
| DF-7 | 0006 | NEW `ADR-0026 \| relates` RD row + Revision-History row | YES — relates. **PASS** |
| DF-8 | 0023 | NEW inbound `ADR-0026 \| depends-on (inbound)` RD row; in-place `[RESOLVED-BY-ADR-0026]` annotation on SHARED OQ-2 + Revision-History row | YES — depends-on inbound + OQ-2 annotation. **PASS** |
| DF-9 | 0024 | NEW inbound `ADR-0026 \| depends-on (inbound)` RD row; in-place `[RESOLVED-BY-ADR-0026]` annotation on SHARED OQ-2 + Revision-History row | YES — depends-on inbound + OQ-2 annotation. **PASS** |

All 9 diffs are append-only (NEW RD rows + NEW Revision-History rows + in-place `RESOLVED-BY-ADR-0026`
OQ/pointer annotations). Each DF's relationship type matches `dag.md §3`. **PASS.**

---

## Bidirectionality (check 8) → **PASS**

Every edge ADR-0026/ADR-0027 declares now has its reciprocal in the existing ADR (spot-checks):

| Outbound edge declared | Reciprocal in existing ADR (from diff) | Verdict |
|------------------------|----------------------------------------|---------|
| 0026 `depends-on` 0022 | 0022 gained `ADR-0026 \| depends-on (inbound)` + amendment row | **PASS** |
| 0026 `depends-on` 0023 | 0023 gained `ADR-0026 \| depends-on (inbound)` | **PASS** |
| 0026 `depends-on` 0024 | 0024 gained `ADR-0026 \| depends-on (inbound)` | **PASS** |
| 0027 `depends-on` 0020 | 0020 gained `ADR-0027 \| depends-on (inbound)` | **PASS** |
| 0027 `depends-on` 0015 | 0015 gained `ADR-0027 \| enables` | **PASS** |

(Also confirmed: 0026 `relates` 0015 → 0015 `ADR-0026 \| relates`; 0026 `relates` 0006 → 0006
`ADR-0026 \| relates`; 0027 `relates` 0001/0005 → both gained `ADR-0027 \| relates`; 0027 `constrains`
0016 → 0016 `ADR-0027 \| constrains`. Every loop closed.)

---

## No new contradiction / anti-pattern (check 9) → **PASS**

- **No leftover contradiction from the RT-01 rewrite.** A full-file grep for "byte-frozen
  run_orchestrated" / "share helpers only" / the old refuted phrasings found 0 hits outside the
  historical Revision-History Initial-draft row. Context ¶ (L22) draws the two-tier distinction
  explicitly (inner engine byte-frozen vs `run_orchestrated` WRAPPER refactorable); Decision, Rationale,
  Consequences, Alternative A′, Falsification, OQ-1 all agree. No section contradicts another.
- **Consequences still carries ≥1 substantive Negative (AP-03).** ADR-0026 Consequences has **3**
  Negatives (subscription-session coupling / 1+yr; the bounded WRAPPER refactor + new seam; live
  dispatch non-determinism). ADR-0027 carries 4. No fairy-tale.
- **Citations resolve (spot-check against LIVE `plan_orchestrator.py`).** `while True:` at L260;
  `_safe_gate(gate_dispatch, result)` at L261; `safety_passed is True` gate at L265; `accept is True`
  at L271; `_promote_plans` at L273; `revise_domains = disposition.get("revise_domains")` at L286;
  `_dispatch_domains(revise_domains, …)` re-dispatch at L294; dispatch-cap halt at L301-305. Leaf-helper
  defs at L345 (`_dispatch_domains`) / L373 (`_safe_gate`) / L398 (`_honest_no_plan`) / L424
  (`_promote_plans`) — all EXACTLY as ADR-0026 and the red-team report cite. `_promote_plans` body spans
  L424-~462 (the cited 424-466 range is accurate). Every cited line number is correct against the live
  tree.

---

## Summary table

| Check | Verdict |
|-------|---------|
| RT-01 (HIGH, keystone mechanism) | **PASS** |
| RT-02 (HIGH, audit repoint) | **PASS** |
| RT-03 (MED, unattended both sides) | **PASS** |
| RT-04 (Decision fold half-sentence) | **PASS** |
| RT-05 (OQ-2 fixed-keys NOTE) | **PASS** |
| RT-06 (∥ → AND) | **PASS** |
| RT-07 (0027 SUMMARY_FIELD_SET clause) | **PASS** |
| RT-08 (no-action — quantitative consistency) | **PASS (N/A, recorded only)** |
| RT-09 (dag ADR-0025 reasoned-exclusion) | **PASS** |
| PART A DF-1…DF-9 append-only | **PASS (9/9)** |
| Bidirectionality | **PASS** |
| No new contradiction / anti-pattern | **PASS** |

**TOTAL FAIL COUNT = 0. No remediation pass required. The live-wiring ADR set is GO.**
