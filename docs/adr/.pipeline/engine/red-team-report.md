# Red-Team Report — Plan-Generation Engine ADR Set (0020–0025), Phase 7

**Pipeline phase:** 7 (adversarial review of the COMPLETE set as a SYSTEM). The 6 engine ADRs
(0020–0025) each passed individual verification + judging; this review finds problems that emerge only
when the set is read together, against `dag.md`, `rubric.md`, the ADR anti-pattern catalog, and the
touched existing ADRs (0001/0004/0005/0006/0009/0015/0016) + the design doc 0022 supersedes.

**Reviewer:** fresh-context adversarial-review agent. Discipline: the 8-category document walk
(Ambiguity / Edge-Case / Contradiction / Reference / Ordering / Scope / Downstream / Language-Economy)
applied to the SET, plus the 6 create-adr Phase-7 systemic categories (DAG-integrity, cross-ADR
consistency, mapping-table coverage, systemic anti-patterns, coverage gaps, handoff completeness).

**Headline verdict:** the set is coherent and high-quality. The PII envelope (IN model-backed /
OUT deterministic) is genuinely coherent, not self-contradictory; the DAG is acyclic; no Mega-ADR;
every alternative is substantively analyzed. The findings are dominated by ONE class: the
**inverse-edge backfill is entirely undone** across all 6 ADRs and all 7 touched existing artifacts
(the authors explicitly DEFERRED it to Phase 8, by design — so this report's job is to produce the
complete Phase-8 backfill worklist, RT-01). Two BLOCKING findings of substance follow it: a
premature-tense claim (RT-02) and a sharpened crown-jewel hook-coverage fact (RT-03). The rest are
ADVISORY.

**Blocking vs Advisory tally:** 3 BLOCKING (RT-01, RT-02, RT-03), 8 ADVISORY (RT-04…RT-11).

---

## Category 1 — DAG Integrity (systemic)

**Narrating the walk.** I enumerated every edge in `dag.md` §2 (new-set) + §7 (cross-refs to existing
ADRs), then checked each against (a) the originating new ADR's Related Decisions table and (b) the
inverse edge in the partner/existing ADR. Cycle check: re-ran the §3 reachability by hand — asymmetric
edges 0022→0020, 0023→0022, 0024→0022, 0025→0022, 0025→0021; 0020 and 0021 are sinks; no node reaches
itself. **No cycle — confirmed.** Tier sort (0020,0021 → 0022 → {0023,0024,0025}) is valid.

**Forward (new-ADR → its Related Decisions) direction: CLEAN.** Every §2/§7 outbound edge appears in
the originating ADR's table with a type from the closed vocabulary (or correctly flagged as a prose
documentation relationship for `amends`/`supersedes`/`distinct-from`). 0020 carries 5 rows
(0015/0021/0016/0001/0005), 0021 carries 6 (0020/0005/0001/0004/0009/0025), 0022 carries 3
(0020/0006/0015), 0023 carries 3 (0022/0006/0024), 0024 carries 3 (0022/0006/0023), 0025 carries 3
(0022/0021/0004). Each resolves to a real ADR. No orphan outbound reference.

**Inverse (existing/sibling ADR → inbound edge) direction: ENTIRELY ABSENT.** This is RT-01 — the
crown finding of this category. I grepped all 7 touched existing artifacts; NONE carries an inbound
edge from the 0020–0025 set. The authors flagged this deferral explicitly (dag.md §7 "Inverse-edge
backfill required … deferred to AUTHOR/VERIFY phase" and every new ADR's closing paragraph says the
inverse edges "are backfilled … as those ADRs land"). So this is a KNOWN, by-design Phase-8 worklist,
not a defect the authors missed — but it IS the load-bearing integrity gap for the set, and producing
the exact list is this review's deliverable. See RT-01 for the complete fix table.

**One premature claim (RT-02):** ADR-0023 L77 states the inverse edges "**are backfilled** into those
ADRs per the DAG forward-reference rule" — present/completed tense. They are NOT backfilled (verified:
ADR-0022 carries no inbound `depends-on` from 0023; ADR-0006 carries no `relates ADR-0023`; ADR-0024
carries no reciprocal `complements`). Every OTHER new ADR uses correct future/conditional tense ("are
backfilled … as those ADRs land", "backfilled … once ADR-0025 is authored", "backfilled into ADR-0023
when it is authored"). ADR-0023 is the lone present-tense outlier asserting a state that does not hold.

---

## Category 2 — Cross-ADR Consistency

**Narrating the walk.** I checked the PII-envelope coherence (the load-bearing systemic question),
shared terminology, and quantitative claims across the set.

**The PII envelope (0020 IN model-backed / 0021 OUT deterministic) is COHERENT — confirmed, not a
finding.** The two halves make OPPOSITE model/deterministic choices, and the asymmetry is justified as
a system:
- **IN (0020) needs a model** because the de-id target is rich free-form conversational intake that a
  keyword-bucketer (`router.summarize`'s closed `SUMMARY_FIELD_SET`) cannot faithfully de-identify —
  it collapses a paragraph to one band-token. De-identification of unstructured free-text is a
  structure-preserving transform a model can do and a whitelist cannot.
- **OUT (0021) must NOT touch a model** because the OUT job is pure string substitution (re-insert the
  real name the IN side stripped), sourced from the gitignored identity config. Routing the real name
  THROUGH a model to format it would add a second PII-handling surface for zero capability gain — the
  format-adaptivity a model could add is a property of the ADR-0025 maintained-format step, not the
  re-insertion step.

The two do not contradict each other: 0020 strips on the way in, 0021 restores on the way out, and
each separately honors "the persisted/committed store stays de-identified." Recorded as `complements`
(one envelope), not `tensions-with`. The asymmetry is the RIGHT call and the rationale holds at the
system level. (Note for the record: the discovery doc decision-3 originally TITLED 0021 "a model-backed
PII re-insertion boundary (operator's stated target)"; the authored ADR correctly chose deterministic
re-insertion after weighing it as Alternative A vs B. That title-vs-decision shift is a deliberate,
well-argued design move, not a drift — but a Phase-8 editor should confirm the discovery title is not
later cited as if 0021 were model-backed.)

**Shared terminology: consistent.** "de-id IN / de-id OUT," "the PII envelope," "fail-closed,"
"persisted/committed store stays de-identified," "no-train lane," "raw-egress class," "the crown-jewel
relaxation," "gitignored-only" are used uniformly across all 6 ADRs and dag.md §§5–6. No term drift of
the "de-id boundary vs de-id wrapper" kind the rubric dim-6 warns about.

**Quantitative claims: consistent.** The 0-leak thresholds (0 raw-PII past boundary / 0 raw-PII in
committed file in 0020; 0 real-PII in tracked file in 0021/0025) are identical across the three
PII ADRs. The ~30-day no-train retention window is cited identically (and identically tagged
`[VENDOR-CLAIM]`/`[UNVERIFIED]`) in 0020 and traced to ADR-0001 OQ-2 / ADR-0016 OQ-1 — no divergent
number. The <500KB / WCAG-AA / 0-external-request budget is cited identically in 0025 and inherited
from 0004. No quantitative contradiction found.

**One real cross-ADR sharpening (RT-03), not a contradiction:** all three PII ADRs describe the
`block-pii-commit.sh` coverage gap (the shared OQ-1) as "the fixtures plant under `vault/scaffold/filled/`
+ `vault/store/`, the `vault/artifacts/generated/` surface is not yet in those fixtures." That framing
is accurate but UNDERSTATES the gap. The hook's content scan (`pii_scan.scan_scoped`) is two-scoped:
contact tokens (email) scan trunk-wide, but **operator-NAME tokens scan ONLY the `data_bearing` subset**
(`scaffold/filled/`, `store/`, `dna/raw/`, `labs/raw/`). `vault/artifacts/generated/` is NOT
data-bearing — so a committed maintained-HTML artifact carrying the **re-inserted full name** (the exact
PII 0021 adds) would be scanned for contact tokens but **not for the name token**. The gap is structural
(scan SCOPE), not merely a missing test fixture. `.gitignore` still covers the path, so a leak needs
`git add -f` / `--no-verify` — the residual the ADRs do name — but the Phase-8 prerequisite build task
should fix the scan SCOPE (`DATA_BEARING_PREFIXES` or the per-se-deny set), not just add a fixture.

---

## Category 3 — Mapping-Table Coverage (dissents / OQs / risks → right section, no orphans)

**Narrating the walk.** I traced every dissent, open question, and risk to its owning section and
checked the SHARED hook-fixture OQ for cross-ADR consistency.

**The shared hook-fixture OQ (0021 OQ-1 + 0025 OQ-1) is consistently stated and owned in BOTH —
confirmed.** Both phrase it identically ("Do `block-pii-commit.sh` + `pre-push-pii-scan.sh` deny a
committed maintained-HTML artifact carrying re-inserted PII?"), both own it to Walter, both gate it
"Before ADR-0025 build," both label it "the SHARED OQ," both tie it to dag.md §6's Pending tension and
the prerequisite-build-task framing, and 0020 OQ-1 + 0020's fourth review-trigger + 0024 are all
consistent with it. It IS the load-bearing crown-jewel residual for the whole set, and the set treats
it as such (3 ADRs carry it; the dag §6 Pending status flows from it). **No orphan, no inconsistency**
— except that the gap is understated (RT-03, above; the OQ should be re-scoped to the scan-SCOPE fix).

**Dissent preservation:** 0020 carries an explicit named Dissent (the summaries-not-raw purist
position) with its reconsideration conditions — substantive, not strawed. 0021/0022/0023/0024/0025 fold
their dissent into the status-quo Alternative B with genuine "when this becomes the right choice"
conditions. No dummy alternative anywhere (see Category 4).

**OQ owner/date completeness (RT-04, advisory):** several OQ target dates are non-actionable for
build-planning. ADR-0021 OQ-2 = "TBD"; ADR-0023 OQ-1/OQ-3, ADR-0024 OQ-1/OQ-3, ADR-0025 OQ-1/OQ-2 = a
relative "Before ADR-00NN build" rather than a date; ADR-0024 OQ-2 / ADR-0023 OQ-2 = "Coordinated with
ADR-00NN build." For a SET handed to build-planning, "before the build that consumes me" is a real
dependency edge but not a schedulable date — the next stage cannot sequence them without resolving the
relative-to-absolute mapping.

---

## Category 4 — Systemic Anti-Patterns

**Narrating the walk.** The individual judges cleared each ADR; I re-checked at the SET level whether a
pattern that is benign per-ADR becomes systemic across all 6.

- **AP-03 (no Negative consequence) — CLEAN at set level.** All 6 carry substantive Negative
  subsections with 1+ year-horizon costs (0020: standing raw-egress exposure; 0022: lost human
  checkpoint; 0023: can reject a safe plan; 0024: load-bearing-tier dependency; 0025: state/staleness
  surface). No systemic Free-Lunch.
- **AP-04 (dummy alternative) — CLEAN at set level.** Every Alternatives section gives each rejected
  option a genuine advantage AND a "when this becomes the right choice." 0020-B (deterministic-IN)
  preserves the 0-raw-PII invariant; 0021-A (model-OUT) gains format adaptivity; 0022-C (standalone
  API) is more provider-portable; 0023-C (per-domain judges) parallelizes/localizes; 0024-C (single
  reviewer) is cheaper; 0025-C (live server) has richest continuity. NONE is a strawman.
- **AP-08 (Mega-ADR) — CLEAN.** Each Decision is one choice. The folds (D-F revise loop into
  0023/0024; D-H substitution seam into 0022; tracking/testing surfaces into 0025) are correctly folded
  as MECHANISMS inside one decision, not bundled second decisions. No "and"-joined titles.
- **Falsification quality at set level — CLEAN and notably strong.** Every ADR carries a named
  load-bearing falsification test with a quantitative threshold: 0020 raw-PII-leak probe (0 hits);
  0021 re-inserted-PII commit/push probe (0 hits); 0022 inner-safety-gate-bypass test (0 plans past an
  unadjudicated hold); 0023 seeded-quality-defect (0 defective plans surfaced) + bounded-revise
  (0 past cap N); 0024 seeded-emergent-issue (0 unsafe-emergent plans surfaced) + double-gate/gap;
  0025 re-inserted-PII-in-committed-render (0 hits) + store-divergence. No systemic "review
  periodically" weakness — the rubric dim-4 floor is met set-wide.
- **AP-02 / AP-10 / AP-11 — CLEAN.** Confidence tags ([VERIFIED]/[VENDOR-CLAIM]/[UNVERIFIED]) are used
  consistently; the one vendor/unverified claim (retention window) is tagged in every appearance.

**One systemic observation (RT-05, advisory):** all 6 ADRs lean on the SAME "the build pipeline already
proved this pattern" justification (execute-plan/rubric judge for 0023; /review-pr for 0024;
orchestrator-runs-specialists for 0022). This is legitimate evidence, not AP-02 sales-pitch (each cites
a real project artifact). But at the SET level it is a single point of evidentiary dependence: if the
build-pipeline analogy is weaker for a HEALTH plan than for a code artifact (a mis-judged code
deliverable costs a revise; a mis-judged health plan can cost clinical harm), three of the six
load-bearing decisions inherit that weakness together. Worth a sentence in each acknowledging the
analogy's limit, or one OQ owning "is the code-pipeline analogy sound for the clinical-harm stakes."

---

## Category 5 — Coverage Gaps (decisions that SHOULD exist but were not identified)

Probing the five named sub-questions:

**(a) Judge+safety findings → REVISE loop iteration/halt policy (folded into 0023/0024) — COHERENT,
not a gap, with one residual (RT-06, advisory).** The revise loop folded cleanly: 0023 owns the
quality-revise (bounded cap N, escalate on N+1), 0024 owns the safety-revise (bounded, dedupe lens
conflicts). BUT the COMPOSITION of the two loops is an open seam the set acknowledges but does not
resolve: both fold "the D-F revise loop," both feed "the same folded revise loop," and the
one-combined-tier-vs-two-gates + ordering question is carried as 0023 OQ-2 / 0024 OQ-2 "coordinated
across the pair." That is the right place for it — but the SET ships to build-planning with the
revise-loop TOPOLOGY (shared loop vs two loops; quality-then-safety vs parallel; does a safety revise
re-trigger a quality judge pass?) unresolved. This is a known open question, correctly owned, but it is
the single most build-blocking ambiguity in the set: a builder cannot implement the orchestrator's
control flow without it. Flag it as the #1 OQ to close before the Tier-3 build, not a gap in the ADRs.

**(b) The model-substitution seam (folded into 0022) — adequately covered.** 0022 folds D-H, cites the
ADR-0015 seam, names the falsification (>1 file outside the `ModelClient` seam on a backend swap =
ossified), and carries OQ-3 (where the drive layer lives / how much re-validates on cutover). Coverage
is adequate; the drive-layer-coupling negative is honestly stated. Not a gap.

**(c) Ordering of the new stages — PARTIAL GAP (RT-07, advisory).** The end-to-end stage order (de-id
IN → orchestrate → {judge ∥ safety-review} → revise → de-id OUT → maintained format) is stated as a
PHRASE in several places (0022 Y-Statement + Decision "generate→judge→safety-review→revise";
0024 Decision "parallel to or after the ADR-0023 quality judge, before the plan is surfaced") but is
NOT pinned in any single authoritative location as the canonical pipeline order. dag.md gives the
DEPENDENCY tiers (a partial order), not the RUNTIME stage sequence — and the two differ: 0021 (de-id
OUT) is Tier 1 by dependency but runs LAST at runtime (render-time). A builder reading the tier sort
could mis-order de-id OUT. The judge∥safety ordering is explicitly unresolved (point (a)). No ADR or
dag section carries the definitive runtime stage sequence as a labeled artifact; it falls between the
dependency DAG and the prose. The spec stage should pin it.

**(d) Cost/rate-limits of the autonomous orchestrator running specialists+judge+safety repeatedly —
PARTIAL GAP (RT-08, advisory).** This IS surfaced — 0022 OQ-2 (subscription rate/concurrency ceiling),
0023/0024 Negatives (recurring dispatch cost multiplied by re-runs), 0024 OQ-1 (lens count). But it is
surfaced as scattered per-ADR OQs/Negatives, never as one aggregate budget. The autonomous loop runs:
N specialists + 1 judge + (≥2 safety lenses + triage) + (≤N_q quality-revise rounds) + (≤N_s
safety-revise rounds), RE-RUN on every wearable/lab arrival. No ADR multiplies these into a per-plan or
per-month dispatch-volume estimate against the subscription ceiling 0022 OQ-2 names. For a "subscription
orchestrator" whose whole cost case (0022 Rationale) rests on subscription having no marginal per-call
charge, the absent aggregate makes the OQ-2 ceiling unsizable — the set cannot say whether the chosen
runtime survives its own loop. Worth one consolidating OQ owning the aggregate dispatch budget.

**(e) Failure/rollback if the de-id API boundary is DOWN — REAL GAP (RT-09, advisory→arguably
blocking).** 0020 specifies fail-closed for a FAILED/partial de-id CALL (→ honest no-plan, mirroring
`AUTHOR_CALL_FAILED`). But the SET has a hard new runtime dependency: 0020 Negative explicitly says
"the plan path gains a hard runtime dependency on the no-train API and network for de-id-IN … a
model-backed boundary cannot [run offline]." NO ADR addresses the SYSTEM-LEVEL outage path: if the
de-id API is down, the orchestrator (0022) cannot dispatch (no de-identified summary), so the judge
(0023), safety review (0024), and maintained re-emit (0025) all have nothing to gate/render. The
fail-closed-per-call contract degrades to honest-no-plan, which is SAFE — but the set never STATES that
a boundary outage halts the entire engine to honest-no-plan, nor whether a maintained artifact (0025)
that already exists from a prior run is left stale-but-readable or invalidated during an outage. This is
the one genuine missing decision: "engine behavior under de-id-boundary unavailability." It is probably
just "honest-no-plan, prior maintained artifact stays as last-good" — but that is unstated, and 0025's
staleness/divergence Negative + Falsification-2 intersect it without resolving it. Recommend a one-line
addition to 0020 (or 0022) Consequences pinning the system-level degrade, and a 0025 note on
outage-time artifact state.

---

## Category 6 — Handoff Completeness (actionable for build-planning?)

**Narrating the walk.** I checked whether the tier map + validation criteria + OQs + constraint
propagation + tension resolutions are concrete enough for the spec/build-plan stage to consume.

**Strong:** the tier map (dag §4) is unambiguous and build-orderable (Tier 1 pair → Tier 2 → Tier 3
trio). Constraint propagation (§5) is explicit and transitivity-checked. Tension resolutions (§6) each
carry trade-off + mitigation + reconsideration trigger and are correctly promoted to OQs in both
tensioned ADRs + prerequisite build tasks. Validation criteria are testable with quantitative
thresholds (Category 4). The extend-not-rebuild grounding (§9) is stated so the build phase will not
re-author the reconciler.

**Gaps for build-planning (collected from above):**
- The inverse-edge backfill (RT-01) is a Phase-8 worklist the build cannot skip — the set is not
  cross-reference-complete until it lands.
- The revise-loop topology (RT-06) and the canonical runtime stage order (RT-07) must be pinned before
  the Tier-3 build can implement the orchestrator control flow.
- The three Pending tensions (§6) rest on a hook fix whose SCOPE is mis-stated (RT-03) — the prerequisite
  build task must fix the scan scope, not just add a fixture.
- OQ dates are relative-not-absolute (RT-04) and the aggregate cost budget (RT-08) + outage degrade
  (RT-09) are unsized.

**One handoff-actionability nit (RT-10, advisory):** 0023 OQ-1 (the revise cap N) and 0025 OQ-2 (re-emit
atomicity) are tagged "an implementation detail the spec resolves" while ALSO being the mechanism their
own load-bearing Falsification tests assert against (0023 bounded-revise test asserts halt at N; 0025
Falsification-2 asserts no committed divergence). A value that a falsification test depends on is not a
free "spec detail" — N and the atomicity mechanism are load-bearing parameters the spec MUST fix before
the test is writable, which the handoff should mark as blocking-for-test, not deferrable.

**Language-economy nit (RT-11, advisory):** the closing cross-reference paragraph in each ADR re-states
the full backfill list + "cross-reference authority for the engine set: dag.md §7" verbatim. Across 6
ADRs this is ~6 near-identical paragraphs. Load-bearing once (the canonical-authority pointer); the
repeated full backfill enumeration is the kind of duplication that goes stale the moment the backfill
lands (it will then describe a completed action in future tense). Recommend trimming each to the
one-line authority pointer + "see dag.md §7 for the backfill worklist" after RT-01 is executed.

---

## Findings

### RT-01: Inverse-edge backfill is entirely undone across all 6 new + 7 existing artifacts (the Phase-8 worklist)

| Field | Value |
|-------|-------|
| **Category** | R (Broken/Missing References) + DAG-Integrity systemic |
| **Severity** | High |
| **Resolution** | Prevent (execute the backfill in Phase 8) |
| **Affected** | ADR-0001, 0004, 0005, 0006, 0009, 0015, 0016 (existing); ADR-0020–0025 (sibling/inbound) + the design doc |
| **Blocking?** | **BLOCKING** (Phase-8 worklist; the set is not cross-reference-complete until it lands) |

**Description:** Every outbound edge from the new set is present in its originating ADR, but ZERO inverse
edges have been backfilled into the partner/existing artifacts. The authors deferred this by design
(dag §7), so this finding's job is the complete, verified backfill table. Grep-verified absent.

**Evidence:** dag.md §7 "Inverse-edge backfill required (integrity Check 5, deferred to AUTHOR/VERIFY
phase)." Grep of ADR-0001/0004/0005/0006/0009/0015/0016 for `ADR-002[0-5]` returns 0 hits.

**Fix — the complete Phase-8 backfill table (the worklist):**

| # | Backfill INTO | Add row / edit | Type | Pairs with (outbound source) |
|---|---------------|----------------|------|------------------------------|
| 1 | ADR-0001 | `tensions-with ADR-0020` | tensions-with | ADR-0020 → 0001 |
| 2 | ADR-0001 | `relates ADR-0021` | relates | ADR-0021 → 0001 |
| 3 | ADR-0005 | `tensions-with ADR-0020` | tensions-with | ADR-0020 → 0005 |
| 4 | ADR-0005 | `tensions-with ADR-0021` | tensions-with | ADR-0021 → 0005 |
| 5 | ADR-0015 | `relates ADR-0020` (the de-id-IN runs through the client seam) | relates/depends-on-inverse | ADR-0020 → 0015 |
| 6 | ADR-0015 | `relates ADR-0022` (the orchestrator dispatches through the seam) | relates | ADR-0022 → 0015 |
| 7 | ADR-0016 | `amended-by ADR-0020` (second raw-egress class) | amended-by (doc) | ADR-0020 → 0016 |
| 8 | ADR-0004 | `amended-by ADR-0025` (maintained lifecycle) | amended-by (doc) | ADR-0025 → 0004 |
| 9 | ADR-0004 | `superseded-posture-by ADR-0021` (data-out initials-only) | supersedes-posture-inverse (doc) | ADR-0021 → 0004 |
| 10 | ADR-0009 | `superseded-posture-by ADR-0021` (D2 initials-only render rule) | supersedes-posture-inverse (doc) | ADR-0021 → 0009 |
| 11 | ADR-0006 | `relates ADR-0022` (orchestrator drives roster assembly) | relates | ADR-0022 → 0006 |
| 12 | ADR-0006 | `relates ADR-0023` (judge over assembled plan) | relates | ADR-0023 → 0006 |
| 13 | ADR-0006 | `relates ADR-0024` (safety review over assembled plan) | relates | ADR-0024 → 0006 |
| 14 | design doc `plan-generation-pipeline-v1.md` | add `superseded_by: ADR-0022` frontmatter + a `superseded_by` pointer on the §"Runtime model" section | superseded_by | ADR-0022 → design doc |
| 15 | ADR-0022 (body) | inbound `depends-on` rows from ADR-0023, 0024, 0025 (currently only OUTbound 0020/0006/0015 present) | depends-on (inbound) | 0023/0024/0025 → 0022 |
| 16 | ADR-0021 (body) | inbound `depends-on` row from ADR-0025 — already present as `(depends-on, inbound)` placeholder L81; confirm it survives as a real row when 0025 lands | depends-on (inbound) | 0025 → 0021 |
| 17 | ADR-0023 (body) | reciprocal `complements ADR-0024` — present L75; confirm reciprocity holds both ways | complements | 0024 ↔ 0023 |
| 18 | ADR-0024 (body) | reciprocal `complements ADR-0023` — present L75; confirm | complements | 0023 ↔ 0024 |

Items 15–18 are intra-new-set reciprocity confirmations (the complement pair 0023↔0024 IS recorded both
ways already — verify it survives; the 0022 inbound `depends-on` from the Tier-3 ADRs is the item most
likely to be forgotten because 0022 was authored BEFORE its dependents). Items 1–14 are the
existing-artifact backfills that are genuinely absent today.

---

### RT-02: ADR-0023 L77 claims the inverse edges "are backfilled" (present tense) — they are not

| Field | Value |
|-------|-------|
| **Category** | C (Internal Contradiction) / R |
| **Severity** | Medium |
| **Resolution** | Prevent |
| **Affected** | ADR-0023 |
| **Blocking?** | **BLOCKING** (a false completed-state claim about cross-reference integrity) |

**Description:** ADR-0023 asserts a backfill action is DONE that has not been performed, contradicting
both the on-disk state and the future-tense phrasing every sibling ADR correctly uses.

**Evidence:** ADR-0023 L77: "the inverse edges (ADR-0022 gains the inbound `depends-on` from this ADR,
ADR-0006 gains `relates ADR-0023`, ADR-0024 carries the reciprocal `complements`) **are backfilled**
into those ADRs per the DAG forward-reference rule." Verified false: `grep relates docs/adr/ADR-0006*`
shows no `ADR-0023` row; ADR-0022's table has no inbound 0023 `depends-on`. Contrast ADR-0020 L87 ("are
backfilled … **as those ADRs land**"), ADR-0024 L77 ("backfilled … **when it is authored**"), ADR-0021
L81 ("backfilled … **once ADR-0025 is authored**") — all correctly future/conditional.

**Fix:** Change "are backfilled into those ADRs" → "are to be backfilled into those ADRs at the Phase-8
backfill (RT-01) — they are recorded in dag.md §7 and not yet written into the target ADRs." Align tense
with the sibling ADRs.

---

### RT-03: The shared hook-coverage OQ (0021/0025 OQ-1) understates the gap — it is a scan-SCOPE hole, not a missing fixture

| Field | Value |
|-------|-------|
| **Category** | E (Edge-Case Gap) / D (Downstream Breakage) |
| **Severity** | High |
| **Resolution** | Prevent (fix the scan scope; re-scope the OQ + prerequisite build task) |
| **Affected** | ADR-0021 (OQ-1, Negative-2), ADR-0025 (OQ-1, Negative-3), ADR-0020 (review-trigger 4); dag §6 |
| **Blocking?** | **BLOCKING** (the crown-jewel residual the whole set's PII safety rests on, mis-scoped) |

**Description:** All three PII ADRs describe the gap as "the maintained-HTML path is not yet in the hook
TEST FIXTURES." The real gap is deeper: `block-pii-commit.sh`'s content scan (`pii_scan.scan_scoped`)
scans operator-NAME tokens ONLY over the `data_bearing` prefix subset, which does NOT include
`vault/artifacts/generated/`. The re-inserted full NAME (exactly 0021's OUT-side PII) on a committed
maintained-HTML artifact would NOT be caught by the name scan — only the trunk-wide CONTACT-token scan
(email/handles) covers that path. So adding a test fixture under the current scope would still not deny
a name-bearing artifact; the SCOPE must change.

**Evidence:** `pii_scan.scan_scoped` (scripts/guard/pii_scan.py L375+): "identity, data-bearing only:
operator-name tokens over the `data_bearing` subset." `pii-scan-scope.sh` L30: `DATA_BEARING_PREFIXES`
= `scaffold/filled/`, `store/`, `dna/raw/`, `labs/raw/` — `vault/artifacts/generated/` absent.
ADR-0021 OQ-1 / Negative-2 and ADR-0025 OQ-1 / Negative-3 frame it as fixtures only.

**Fix:** Re-scope the shared OQ-1 and the dag §6 prerequisite build task from "add a fixture for the
artifacts path" to "extend the name-token scan SCOPE (add `vault/artifacts/generated/` to
`DATA_BEARING_PREFIXES`, or add it to `PER_SE_DENY_PREFIXES`) AND add the fixture proving the scope
change denies a name-bearing committed maintained-HTML artifact." Note that `.gitignore` already covers
the path, so the residual leak vector is `git add -f` / `--no-verify` — the ADRs correctly name that;
the scope fix closes the in-band path.

---

### RT-04: OQ target dates across the set are relative-not-absolute, blocking schedulability

| Field | Value |
|-------|-------|
| **Category** | E / Handoff |
| **Severity** | Low |
| **Resolution** | Handle |
| **Affected** | ADR-0021 OQ-2; 0023 OQ-1/2/3; 0024 OQ-1/2/3; 0025 OQ-1/2 |
| **Blocking?** | Advisory |

**Description:** Many OQ target dates are "Before ADR-00NN build" / "Coordinated with ADR-00NN build" /
"TBD" rather than dates. Build-planning cannot sequence them without mapping each relative target to the
absolute wave it gates.
**Evidence:** ADR-0021 OQ-2 "TBD"; ADR-0023 OQ-1 "Before ADR-0023 build"; ADR-0024 OQ-2 "Coordinated
with ADR-0023 build."
**Fix:** At spec stage, resolve each "Before ADR-00NN build" to the absolute Tier-2/Tier-3 build wave
date; replace "TBD" with the gating wave.

---

### RT-05: Three load-bearing decisions inherit the same "the build pipeline proved it" evidence; the code→clinical-harm analogy limit is unstated

| Field | Value |
|-------|-------|
| **Category** | S (Scope) / systemic evidence |
| **Severity** | Medium |
| **Resolution** | Handle |
| **Affected** | ADR-0022, 0023, 0024 |
| **Blocking?** | Advisory |

**Description:** 0022 (orchestrator-runs-specialists), 0023 (judge), 0024 (multi-lens review) all
justify themselves by analogy to the autonomous BUILD pipeline. The analogy is legitimate but the stakes
differ: a mis-judged code deliverable costs a revise; a mis-judged health plan can cost clinical harm.
The set never states the analogy's limit.
**Evidence:** 0023 Rationale "the build pipeline already runs this produce→judge→iterate shape
successfully"; 0024 Rationale "the `/review-pr` evidence"; 0022 Rationale "the build pipeline already
demonstrates the orchestrator-runs-specialists pattern."
**Fix:** Add one sentence to each (or one shared OQ) acknowledging that the code-pipeline analogy's
failure cost is lower than the clinical-harm cost, and that the judge/review bars are tuned for the
higher stakes accordingly.

---

### RT-06: The revise-loop composition topology across 0023+0024 is unresolved — the #1 build-blocking ambiguity

| Field | Value |
|-------|-------|
| **Category** | O (Ordering/Dependency Gap) |
| **Severity** | High |
| **Resolution** | Prevent (resolve the shared OQ before the Tier-3 build) |
| **Affected** | ADR-0023 (OQ-2), ADR-0024 (OQ-2); dag §1 §6 |
| **Blocking?** | Advisory (correctly owned as an OQ, but must close before Tier-3 implementation) |

**Description:** Both ADRs feed "the same folded revise loop" and both fold "the D-F revise loop," but
whether it is ONE shared loop or TWO; whether quality runs before/after/parallel-to safety; and whether
a safety revise re-triggers a quality judge pass are all unresolved (carried as the shared OQ). The set
ships to build with the orchestrator's central control flow undefined.
**Evidence:** ADR-0023 OQ-2 "Is the plan-quality judge ONE combined review tier … or TWO distinct
gates, and in what order"; ADR-0024 OQ-2 identical; dag §1 "the discovery-flagged open question … is a
compose-the-seam concern."
**Fix:** Resolve the shared OQ at the spec stage as a prerequisite for the Tier-3 build; pin the loop
topology (single vs dual loop, ordering, re-trigger rule) before the orchestrator control flow is
implemented.

---

### RT-07: No single authoritative artifact pins the canonical RUNTIME stage order (distinct from the dependency tiers)

| Field | Value |
|-------|-------|
| **Category** | O / D |
| **Severity** | Medium |
| **Resolution** | Prevent |
| **Affected** | dag.md (§4 gives tiers, not runtime order); 0022/0024 (state it only in prose) |
| **Blocking?** | Advisory |

**Description:** The runtime sequence (de-id IN → orchestrate → {judge ∥ safety} → revise → de-id OUT →
maintained format) lives only as scattered prose. dag §4 gives the DEPENDENCY tier order, which DIFFERS:
0021 (de-id OUT) is Tier 1 by dependency but runs LAST at runtime. A builder following the tier sort
could mis-place de-id OUT.
**Evidence:** dag §4 puts 0021 in Tier 1; 0021 Decision makes re-insertion "render-time-only." 0022
Decision states the order as a phrase ("generate→judge→safety-review→revise"); no labeled
runtime-sequence artifact exists.
**Fix:** Add a "Runtime stage order" subsection to dag.md (or the spec) distinguishing the
DEPENDENCY-author order (tiers) from the RUNTIME-execution order, explicitly noting de-id OUT is
authored Tier-1 but executes last.

---

### RT-08: The autonomous loop's aggregate dispatch cost is never summed against the subscription ceiling it depends on

| Field | Value |
|-------|-------|
| **Category** | E / S |
| **Severity** | Medium |
| **Resolution** | Handle |
| **Affected** | ADR-0022 (OQ-2 + cost Rationale), 0023, 0024 |
| **Blocking?** | Advisory |

**Description:** The cost case for choosing subscription (0022) rests on subscription having no marginal
per-call charge, but the loop's per-plan dispatch VOLUME (N specialists + judge + ≥2 safety lenses +
triage + ≤N_q + ≤N_s revise rounds, × every re-run) is never aggregated against the rate/concurrency
ceiling 0022 OQ-2 names. The set cannot say whether the chosen runtime survives its own loop.
**Evidence:** 0022 OQ-2 (ceiling, unsized); 0023 Negative-1 + 0024 Negative-1 (recurring cost,
un-aggregated); 0024 OQ-1 (lens count, the multiplier).
**Fix:** Add one consolidating OQ (owned by 0022) computing the aggregate per-plan and per-re-run
dispatch volume and checking it against the subscription ceiling, so OQ-2's "does the ceiling bind" is
answerable.

---

### RT-09: No decision covers engine behavior when the de-id API boundary is DOWN (system-level outage)

| Field | Value |
|-------|-------|
| **Category** | E (Edge-Case Gap) |
| **Severity** | Medium |
| **Resolution** | Prevent |
| **Affected** | ADR-0020 (per-call fail-closed only), 0022, 0025 |
| **Blocking?** | Advisory (the closest thing to a genuinely missing decision) |

**Description:** 0020 fail-closes on a failed/partial de-id CALL, but no ADR states the SYSTEM-level
degrade when the de-id API/network is unavailable: the orchestrator (0022) cannot produce a summary, so
judge/review/maintained-format all idle, and 0025's existing maintained artifact's outage-time state
(stale-but-readable vs invalidated) is unspecified. The likely answer is "honest-no-plan; prior
maintained artifact stays last-good" — but it is unstated, and 0025's staleness/divergence Negative
intersects it without resolving it.
**Evidence:** 0020 Negative "the plan path gains a hard runtime dependency on the no-train API and
network for de-id-IN: a deterministic in-process gate could run offline; a model-backed boundary
cannot." No ADR addresses boundary-down system behavior. 0025 Falsification-2 covers a partial RE-EMIT,
not an outage.
**Fix:** Add one Consequence/OQ to 0020 (or 0022) pinning the system-level degrade under
de-id-boundary unavailability (engine halts to honest-no-plan; the engine is offline-incapable for
NEW plans), and a 0025 note that an outage leaves the last-good maintained artifact in place, never
a partial re-emit.

---

### RT-10: Load-bearing parameters (revise cap N, re-emit atomicity) are tagged "spec detail" while a falsification test depends on them

| Field | Value |
|-------|-------|
| **Category** | C / Handoff |
| **Severity** | Low |
| **Resolution** | Handle |
| **Affected** | ADR-0023 (OQ-1), ADR-0025 (OQ-2) |
| **Blocking?** | Advisory |

**Description:** 0023 OQ-1 (revise cap N) and 0025 OQ-2 (re-emit atomicity) are framed as
"implementation detail the spec resolves," but each is the exact mechanism its own load-bearing
Falsification test asserts against — so they are blocking-for-test parameters, not free spec details.
**Evidence:** 0023 bounded-revise Falsification asserts "halts at the iteration cap N"; OQ-1 leaves N
open + "the mechanism is a build-plan parameter." 0025 Falsification-2 asserts no committed divergence;
OQ-2 leaves the atomicity mechanism open.
**Fix:** Mark 0023 OQ-1 (N) and 0025 OQ-2 (atomicity) as blocking-for-test — the spec must fix them
before the falsification tests are writable, not defer them as ordinary implementation choices.

---

### RT-11: Six near-identical closing cross-reference paragraphs re-enumerate the backfill list (staleness + token cost)

| Field | Value |
|-------|-------|
| **Category** | L (Language Economy) |
| **Severity** | Low |
| **Resolution** | Accept (until RT-01 lands), then trim |
| **Affected** | ADR-0020–0025 (each closing cross-ref paragraph) |
| **Blocking?** | Advisory |

**Description:** Each ADR's closing paragraph re-states the full backfill enumeration + the canonical
"cross-reference authority: dag.md §7" pointer. The pointer is load-bearing once; the repeated full
enumeration goes stale the moment RT-01 executes (it will then narrate a completed action in future
tense).
**Evidence:** ADR-0020 L87, 0021 L81-end, 0022 L80, 0023 L77, 0024 L77, 0025 L80 — each carries the
backfill list verbatim.
**Fix:** After RT-01 is executed, trim each closing paragraph to the one-line authority pointer; drop
the per-ADR backfill enumeration (it lives canonically in dag §7 / this report's RT-01 table).

---

## Coverage Matrix

| Phase-7 Category | Walk result | Findings |
|------------------|-------------|----------|
| 1 — DAG integrity (cycle / edge bidirectionality / inverse backfill) | No cycle; forward edges clean; inverse backfill entirely absent (by design) | RT-01, RT-02 |
| 2 — Cross-ADR consistency (envelope coherence / terms / quant) | Envelope coherent; terms + numbers consistent; hook-OQ understated | RT-03 (+ RT-05) |
| 3 — Mapping-table coverage (dissent/OQ/risk; shared OQ) | Shared OQ consistent + owned in both; OQ dates relative | RT-04 |
| 4 — Systemic anti-patterns (AP-03/04/08, falsification) | Clean set-wide; one shared-evidence concentration | RT-05 |
| 5 — Coverage gaps (a–e) | (a) coherent w/ residual; (b) covered; (c) partial; (d) partial; (e) real gap | RT-06, RT-07, RT-08, RT-09 |
| 6 — Handoff completeness | Strong; blocked on backfill + loop-topology + scope fix + test-params | RT-10, RT-11 |

**8-category document walk (applied to the set):** A — RT-06/RT-07 (ordering ambiguity). E — RT-03,
RT-08, RT-09 (edge/outage/cost gaps). C — RT-02, RT-10 (false-state claim, mis-tagged params). R —
RT-01, RT-02 (missing/stale references). O — RT-06, RT-07 (runtime ordering). S — RT-05 (shared-evidence
scope). D — RT-03, RT-07 (downstream hook + builder mis-order). L — RT-11 (duplication).

## Verdict

The engine ADR set is coherent and ships a strong, falsifiable system. **3 BLOCKING** items for Phase 8:
RT-01 (execute the full inverse-edge backfill table), RT-02 (fix the false "are backfilled" tense in
0023), RT-03 (re-scope the crown-jewel hook OQ from "missing fixture" to "scan-scope hole"). The
8 advisories cluster on build-planning readiness (loop topology RT-06, runtime order RT-07, cost
aggregate RT-08, outage degrade RT-09) — none blocks the ADRs as DECISIONS, but RT-06/RT-09 should close
before the Tier-3 build. The PII envelope's IN-model/OUT-deterministic asymmetry is the right call and
holds as a system.
