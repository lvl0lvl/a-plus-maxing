---
title: recovery-specialist Design Doc — Phase-3 Role-3 Coverage Red-Team
type: red-team-findings
role: health-edge-case-reviewer (Role 3)
mandate: COVERAGE gaps (adversarial taxonomy-bypass routed to Role 4 pattern-N/A)
artifact_under_review: design/recovery-specialist-design.md (395 lines)
substrate: design/.recovery-specialist-design-work/domain-research.md (14 Findings, 15 Recs)
taxonomy: templates/refusal-class-taxonomy.yaml (8 canonical classes)
created: 2026-05-31
coverage_verdict: BLOCK_WITH_FINDINGS
severity_disposition: severity_proposed only (medical-liaison sets severity_final)
---

# Role-3 Coverage Red-Team — recovery-specialist Design Doc

Mode: probe-discovery + adjudication-handoff. Mechanical pre-audit (Core Rule 5/11) ran
BEFORE semantic adjudication: schema OK, enum OK, all LIVE locators resolve, REFERENCED INV
IDs all present in INVARIANTS.md, risk-class floor matches the YAML. Artifact re-Read at every
section boundary (Core Rule 6). Severity axes per Role-3 schema: IMDRF info × condition × NCC
MERP outcome × FM-class, with h_class_equivalent_max H1–H8. **No fixes authored — read-only on
the design doc (Core Rule 1); remediation routes to the adjudicator/bead, never an Edit.**

---

## boundary_class_coverage (all 8 canonical classes — grep-grounded)

Locator base: `design/recovery-specialist-design.md`. Each class grepped `-w` against the doc.

| # | Class | Verdict | match_count | Locator(s) | Note |
|---|---|---|---|---|---|
| 1 | PATIENT_FACING_DIRECTIVE | covered | 1 | L145 (§6 step 3: self/other clinical-diagnosis incl. "do I have OTS?") | Paired: refused (diagnosis) ↔ answered (pattern-flag + route, §5.4 L129). |
| 2 | IMAGE_OR_SIGNAL_INPUT | covered (structural-not-fired) | 1 | L173 (§8: "no image/signal Read path, no WebFetch (keeps IMAGE_OR_SIGNAL_INPUT mandatory_when from firing)") | mandatory_when is tool-gated (taxonomy L29); doc structurally removes the Read-image/WebFetch path → mandatory_when does NOT fire. Reasoning sound. |
| 3 | TIME_CRITICAL | covered | 5 | L136, L144 (§6 step 2 cardiac cluster → EMERGENCY (TIME_CRITICAL)), §7 L156 | Paired: refused (session w/ red-flag) ↔ answered (trend interp absent red-flag). |
| 4 | BASIS_NOT_REVIEWABLE | covered | 4 | L146 (§6 step 4), §7 L160, §14.2 L305 | Paired: refused (ungrounded number) ↔ answered (evidence-graded framing, §14.2). |
| 5 | PRESCRIPTIVE_DIRECTIVE | covered | 1 | L145 (§6 step 3: prescription/medication-class → route to medical-liaison) | Single locator; thin but present. |
| 6 | DEVICE_FUNCTION | covered | 3 | L145 (§6 step 3), L173 (§8), §14.6 L309 (readiness-as-diagnosis refused) | Paired: refused (continuous-monitoring) ↔ answered (within-device trend, §14.6). |
| 7 | HIGH_RISK_SAMD | **not-covered** | **0** | grep_pattern `HIGH_RISK_SAMD` → match_count 0 across all 395 lines | See F-003. R10/§2.2 commit to "≥4 classes"; 6 distinct present, so the ≥4 floor still holds. Omission is unverdicted, not a floor breach. |
| 8 | AUTHORITY_FRAMING_BYPASS | **covered (EXPLICIT verdict)** | 9 | L92, L107, §5.11 L136, §6 step 3 L145, §11.2 ap6 L234, §12.2 L255/L263, §13 L296, §15.2 L322 | **MANDATORY-clause AUDIT: PRESENT.** 9 matches incl. literal Core-Rule encoding + a Negative Example (§12.2). The mandatory-for-every-specialist clause (taxonomy L69) is satisfied. NOT match_count 0 → NOT the PATIENT-SAFETY-CRITICAL/BLOCK floor case. |

**AUTHORITY_FRAMING_BYPASS verdict (explicit, per Core Rule 12):** COVERED — match_count 9,
literal class ID present in a Core Rule, the Ask-vs-Proceed tree, an anti-pattern, AND a worked
Negative Example. This is the one class whose absence would be auto-PATIENT-SAFETY-CRITICAL; it
is present and exercised. PASS on this axis.

**Coverage tally:** 7/8 covered, 1/8 not-covered (HIGH_RISK_SAMD, structurally low-reachability
but UNVERDICTED — see F-003). The ≥4-distinct-class floor (R10) is met (6 distinct classes
encoded). AUTHORITY_FRAMING_BYPASS mandatory clause: PASS.

---

## Per-section completeness table (grep-grounded, binary criteria)

| § | Section | Present | Binary criterion | Result |
|---|---|---|---|---|
| 1 | Problem Statement | ✓ L21 | ≥2 numbered gaps + citations | PASS (4 gaps, each cites Finding+R) |
| 2 | Role Definition | ✓ L34 | identity ≤40w; I-own + I-do-NOT-own; owners named | PASS (35w; both lists; owners parenthesized) |
| 3 | Pass-1 Digest | ✓ L54 | §3.1 row count == Finding count (14) | PASS (14 rows == 14 `### Finding`) |
| 3.2 | Recommendations | ✓ L77 | all 15 R verdicted, no TBD | PASS (R1–R15 ACCEPTED) |
| 4 | Cross-Role Refs | ✓ L101 | every applicable owner present, references-not-redefines | PASS — see F-005 (no defect; completeness confirmed) |
| 5 | Core Rules | ✓ L122 | 8–12 rules, each [voice]+[source]+Mechanical Check | PASS (12 rules, all tagged) |
| 6 | Ask vs Proceed | ✓ L141 | 4–6 steps, default + never-fabricate | PASS (6 steps) |
| 7 | Loop-Breaking | ✓ L154 | 3–5 thresholds | PASS (6 thresholds; over upper bound but non-blocking) |
| 8 | Tools | ✓ L165 | palette + patterns + restrictions | PASS |
| 9 | Communication | ✓ L177 | 9.1 + 9.2 both with format spec | PASS (9.1 structured-list, 9.2 sentence-pattern) |
| 10 | Context Loading | ✓ L197 | 4–7 steps | PASS (6 steps) |
| 11.1 | PF coverage | ✓ L210 | **ALL documented PFs verdicted** | **FAIL — see F-001 (PF-S12-01, PF-S13-01 absent; frontmatter claims PF-S13-01)** |
| 11.2 | Anti-patterns | ✓ L227 | 5–8, each source + recognition cue | PASS (6) |
| 12 | Negative Examples | ✓ L238 | 2–4 BAD/GOOD, each cites §11 ap# | PASS (3 pairs) |
| 13 | Mechanical Map | ✓ L287 | ≥3 rows, status tags, LIVE paths resolve | PASS (6 rows; both LIVE paths resolve; REFERENCED INV IDs all in INVARIANTS.md) |
| 14 | Edge Cases | ✓ L302 | 4–8, each handling + test stimulus | PASS (6) |
| 15 | Acceptance Criteria | ✓ L313 | 15.1 inherited ref + 15.2 5–10 | PASS (10 criteria) — but AC#2 cites a non-materialized location, see F-002 |
| 16 | Invariants at Risk | ✓ L334 | in-scope invariants addressed | PASS (10 rows) |
| 17 | Risk/Assump/Break | ✓ L355 | three subsections; 3–7 / 3–7 / 2–5 | PASS (5 risks / 5 assumptions / 3 breaks) |
| 18 | Open Questions | ✓ L381 | present; every §13 PROPOSED row echoed | PASS (3 Qs; OQ-1 echoes §13 PROPOSED) |
| A | Appendix A | ✓ L391 | present (PENDING at synthesis) | PASS (correctly PENDING pre-Phase-3) |

19 sections + Appendix A all structurally present. Two PASS-with-qualifier (§15 AC#2 → F-002;
§4 → F-005 no-defect). One FAIL (§11.1 → F-001).

---

## FINDINGS

### F-001 — §11.1 PF-coverage table omits PF-S12-01 and PF-S13-01; frontmatter `last-PF-reviewed: PF-S13-01` asserts a review currency the section does not deliver

- **finding_id:** F-001
- **edge_case_class:** coverage-gap / completeness (template §11 "reference ALL currently-documented PFs")
- **source_claim_locator:** `design/recovery-specialist-design.md` L10 (frontmatter `last-PF-reviewed: PF-S13-01`); §11.1 table L214–223; closing tally L225 ("7 IN-SCOPE; 1 OUT-OF-SCOPE").
- **quoted_text (frontmatter):** `last-PF-reviewed: PF-S13-01`
- **quoted_text (§11.1 tally):** "7 IN-SCOPE; 1 OUT-OF-SCOPE (PF-S2-06, structural — no git). Mirrors the sleep-coach disposition."
- **grep evidence:** `rg -o 'PF-S[0-9]+-[0-9]+' memory/process-failures.md | sort -u` → 10 distinct PFs incl. **PF-S12-01** (L97) and **PF-S13-01** (L168). `rg 'PF-S12-01|PF-S13-01' design/recovery-specialist-design.md` → only L10 (frontmatter), zero body matches. §11.1 verdicts exactly the 8 template-era PFs (S2-01..S2-06, S3-01, S6-01).
- **why this is a coverage gap (not adversarial):** The template §11 spec was authored at S7 (`last-PF-reviewed: PF-S6-01`) and hardcodes "all 8 currently-documented PFs." The design doc's OWN frontmatter advances the review watermark to PF-S13-01 — but the §11.1 body stops at the S7-era 8. The frontmatter and the body disagree about which PFs were reviewed. Two PFs exist in the log and receive no IN-SCOPE/OUT-OF-SCOPE verdict.
- **PF-S13-01 is the load-bearing one.** PF-S13-01 (`AP-PROTOCOL-FROM-MEMORY`) is explicitly the sibling of PF-S2-05 (its own log entry, L170, names "Same root-cause class as PF-S2-05"). §11.1 marks **PF-S2-05 IN-SCOPE** ("Recovery re-reads operator/wearable state + the escalation-tier map per dispatch; operate-from-memory is reachable," L220). By the section's OWN reachability logic, PF-S13-01's operate-from-memory pattern is equally reachable for this agent (Core Rule 6 re-Read discipline + §10 per-dispatch re-reads are the exact surface). Omitting it is an unverdicted in-scope PF.
- **PF-S12-01** (`AP-DEFERRED-LOOP-CLOSURE`, Session-B deferral / drafter-roster drift) is plausibly OUT-OF-SCOPE structurally (recovery runs no Session B / deployment cadence), but the template demands an *explicit* OUT-OF-SCOPE verdict with a structural reason — silent omission is not a verdict.
- **severity_proposed (4-axis):**
  - IMDRF info: non-serious (meta/process-documentation defect, not a runtime medical-output defect)
  - condition: N/A (no operator condition)
  - NCC MERP outcome: Category B (error occurred, did not reach operator — design-doc layer)
  - FM-class: completeness / traceability
  - **h_class_equivalent_max: H6** (process/documentation integrity; no direct medical-harm path)
  - composite: **MAJOR** (a REQUIRED-section binary criterion fails; frontmatter↔body contradiction is a traceability break that `/upgrade-agent` Phase-1 PF-diff explicitly consumes per template L70).
- **decision_rule_applied:** Core Rule 5 (mechanical pre-audit: enum completeness) + template §11 "reference all 8 PFs" + frontmatter L70 "last-PF-reviewed is load-bearing."
- **paired_probe_status:** [no-paired-probe-required: this is a completeness/enum gap, not a refused/answered boundary pair.]
- **remediation_target_owner:** synthesis orchestrator (Phase-5). Route: add PF-S12-01 + PF-S13-01 rows to §11.1 with explicit verdicts (candidate: PF-S13-01 IN-SCOPE mirroring PF-S2-05; PF-S12-01 OUT-OF-SCOPE structural). NOT a Role-3 Edit.
- **severity_final:** PENDING (medical-liaison/adjudicator).

### F-002 — "boundary coverage" is cited as a discrete location by §3.2 R10, §15.2 AC#2, and the synthesis preamble, but no boundary-class-coverage block is materialized in the doc

- **finding_id:** F-002
- **edge_case_class:** coverage-gap / dangling-reference (AC references a non-existent locator)
- **source_claim_locator:** L17 (preamble: "health-edge-case-reviewer (§11/§12/§14/§18 + **boundary-class coverage**)"); L92 (§3.2 R10 implementing-section "§2.2, §11, **boundary coverage**"); L322 (§15.2 AC#2: "(§2.2, **boundary coverage**) [R10]").
- **quoted_text (AC#2):** "≥4 distinct refusal classes referenced, drawn from `templates/refusal-class-taxonomy.yaml`, including the literal `AUTHORITY_FRAMING_BYPASS` (`grep -w`; mandatory — operator A3). (§2.2, boundary coverage) [R10]"
- **grep evidence:** `rg -i 'boundary.class coverage|boundary coverage' design/recovery-specialist-design.md` → 4 matches, ALL of which are *references to* a boundary-coverage artifact (preamble + R10 + AC#2 + the §8 IMAGE_OR_SIGNAL parenthetical "§11 boundary coverage"). NONE is a section heading or an enumerated 8-class [covered]/[not-covered] block. The 8-class coverage is implicit-only (scattered across §2.2 L48, §6 L145, §8 L173, §11) and never assembled.
- **why this is a coverage gap:** An acceptance criterion (#2) and a Recommendation implementing-section (R10) point at a "boundary coverage" location that does not exist as a verifiable section. A binary AC that cites a phantom location cannot be mechanically checked the way it claims. The synthesis preamble asserts Role-3 *produced* a boundary-class-coverage deliverable; that deliverable did not land as a doc section (it lives only in the Role-3 work-dir, i.e., THIS file's predecessor scope) — so in-doc, the citation dangles.
- **note (not double-counting AUTHORITY_FRAMING_BYPASS):** The mandatory class IS present (boundary_class_coverage above, match_count 9). This finding is narrower: the *enumerated 8-class block* the doc's own AC/preamble reference is not in the doc. The AC's `grep -w AUTHORITY_FRAMING_BYPASS` half is satisfiable; the "(boundary coverage)" half points nowhere.
- **severity_proposed (4-axis):**
  - IMDRF info: non-serious
  - condition: N/A
  - NCC MERP outcome: Category B (design-doc layer)
  - FM-class: traceability / verifiability
  - **h_class_equivalent_max: H7** (documentation cross-reference integrity)
  - composite: **MINOR** (the underlying coverage is present in substance; the defect is a dangling pointer + an AC that names a non-materialized location).
- **decision_rule_applied:** Core Rule 9 (cite a locator on every claim — applied reflexively: the doc cites a locator that returns zero matches as a section) + template §15 "each criterion independently testable."
- **paired_probe_status:** [no-paired-probe-required: reference-integrity gap.]
- **remediation_target_owner:** synthesis orchestrator. Route options (Role-3 does not pick): (a) materialize a short boundary-class-coverage block (8 classes [covered]/[not-covered]) as a §2.2 or §11 sub-block and repoint R10/AC#2 at it; or (b) rewrite R10/AC#2 to cite only the locations that exist (§2.2 + §6 + §8 + §11). NOT a Role-3 Edit.
- **severity_final:** PENDING.

### F-003 — HIGH_RISK_SAMD (class 7/8) is unverdicted: zero matches and no structural OUT-OF-SCOPE note

- **finding_id:** F-003
- **edge_case_class:** boundary-class coverage-gap (one canonical class neither encoded nor explicitly waived)
- **source_claim_locator:** whole-doc grep. `rg -w 'HIGH_RISK_SAMD' design/recovery-specialist-design.md` → match_count 0 (exit 1). Contrast: §8 L173 explicitly disposes IMAGE_OR_SIGNAL_INPUT ("keeps mandatory_when from firing") and DEVICE_FUNCTION ("no continuous monitoring or diagnostic determination") with structural reasons; HIGH_RISK_SAMD gets no such note.
- **quoted_text:** (no quoted text — the finding is an absence; grep_pattern `HIGH_RISK_SAMD` match_count 0)
- **why this is a coverage gap (and why it is NOT auto-CRITICAL like an AFB-zero would be):** Per Core Rule 12, AUTHORITY_FRAMING_BYPASS is the mandatory-regardless-of-tier class whose match_count 0 is auto-PATIENT-SAFETY-CRITICAL — that one is PRESENT (9 matches). HIGH_RISK_SAMD is NOT in the mandatory-for-every-specialist set (taxonomy L55–60, no `mandatory_*` key). Its trigger ("Class III SaMD: treat/diagnose serious condition with no equivalent non-LLM tool") is largely subsumed by the PATIENT_FACING_DIRECTIVE + DEVICE_FUNCTION + TIME_CRITICAL encodings that ARE present, and the ≥4-class floor (R10) is met at 6 distinct classes. So the floor is not breached. BUT: §8's other two structurally-low classes (IMAGE_OR_SIGNAL_INPUT, DEVICE_FUNCTION) each get an explicit structural disposition; HIGH_RISK_SAMD is the lone canonical class that is neither encoded nor explicitly dispositioned. The Role-3 default output is a POPULATED 8-class block (Anti-Pattern 2) — an unverdicted class is the exact gap that block exists to surface.
- **severity_proposed (4-axis):**
  - IMDRF info: non-serious (overlapping classes provide coverage; floor met)
  - condition: serious-condition trigger (Class III by definition) — but reachability is low given DEVICE_FUNCTION + PATIENT_FACING_DIRECTIVE cover the realistic recovery surface
  - NCC MERP outcome: Category B
  - FM-class: enumeration completeness
  - **h_class_equivalent_max: H5** (a residual diagnose-serious-condition request could route imperfectly, but PATIENT_FACING_DIRECTIVE + TIME_CRITICAL catch the realistic instances)
  - composite: **MINOR** (waivable with a one-line structural note; not a floor breach; the dominant realistic triggers are already classed).
- **decision_rule_applied:** Core Rule 3 (carry all 8 classes [covered]/[not-covered: reason] on every return) + Anti-Pattern 2 (default output is a populated boundary_class_coverage).
- **paired_probe_status:** [no-paired-probe-required: structural-absence gap, no answered-probe region.]
- **remediation_target_owner:** synthesis orchestrator OR Role 4 (adversarial may elect to test whether a Class-III-shaped request escapes the present 6 classes — that test is Role 4's, routed below). Minimal route: add a §8 structural note disposing HIGH_RISK_SAMD (e.g., "subsumed by PATIENT_FACING_DIRECTIVE + DEVICE_FUNCTION; no recovery surface reaches an LLM-only Class III function"). NOT a Role-3 Edit.
- **severity_final:** PENDING.

### F-004 — Finding-14 "sustained RHR trend +5–10 bpm → ROUTINE-MONITOR" tier mapping does not land in §6/§7/§14; the ROUTINE-MONITOR band is asserted-but-empty, while §15.2 AC#10 claims "every red-flag in Finding 14 maps to an urgency band"

- **finding_id:** F-004
- **edge_case_class:** Finding under-coverage / escalation-tier completeness (the task's check #3 + #5)
- **source_claim_locator (substrate):** `design/.recovery-specialist-design-work/domain-research.md` L76 (Finding 14): "sustained RHR trend **+5–10 bpm → ROUTINE-MONITOR**, resting HR >100 bpm → URGENT-REFERRAL [D: 6, mechanism_review]."
- **source_claim_locator (design doc):** §15.2 AC#10 L330 asserts the completeness; §9.1(7) L188 and §15.2 L330 are the ONLY two places ROUTINE-MONITOR appears, both as an abstract band-label.
- **quoted_text (AC#10):** "Every red-flag in Finding 14 maps to an urgency band (EMERGENCY / URGENT-REFERRAL / ROUTINE-MONITOR) with the cardiac cluster + fever-and-train myocarditis rule at the TIME_CRITICAL floor. (§6.2, §7) [R9]"
- **grep evidence:** `rg -i '5.?10 bpm' design/recovery-specialist-design.md` → match_count 0 (exit 1). `rg 'ROUTINE-MONITOR' design/recovery-specialist-design.md` → 2 matches (L188 §9.1 band-list, L330 AC#10), neither maps the +5–10 bpm sustained-RHR trend to the tier. §6.2 (L144) red-flag short-circuit enumerates the EMERGENCY + URGENT-REFERRAL flags but NOT the ROUTINE-MONITOR one. §7 L156 covers only the EMERGENCY-tier short-circuit. §14.5 L308 covers RHR >100 (URGENT) but not the +5–10 ROUTINE-MONITOR trend.
- **why this is a coverage gap:** Finding 14 has exactly ONE red-flag at the ROUTINE-MONITOR tier (the +5–10 bpm sustained-RHR elevation). It is the lowest-acuity flag and the natural "monitor, don't escalate, don't ignore" signal. It is absent from every operative section (§6/§7/§14). The ROUTINE-MONITOR band is named in the §9.1 output enum and in AC#10's completeness claim, but nothing in the behavioral spec ever *produces* a ROUTINE-MONITOR verdict — the band is structurally empty. AC#10 ("every red-flag in Finding 14 maps to a band") is therefore a tautological/over-claiming AC: it would pass a prose-impression read but fails a grep against the substrate's full red-flag set. Operationally: a +5–10 bpm sustained RHR rise (the early, sub-tachycardic warning) has no defined handling — the agent either silently ignores it (under-escalation: a missed early-warning trend the substrate flags as worth monitoring) or improvises a tier (drift). Both are coverage failures.
- **severity_proposed (4-axis):**
  - IMDRF info: serious-information (an escalation-tier omission in a safety-architecture Finding; the missing tier is the early-warning rung)
  - condition: non-acute monitoring trend (the +5–10 rung is by construction the low-acuity one — it is NOT the chest-pain cluster, which IS covered)
  - NCC MERP outcome: Category C-reachable (an error that could reach the operator as a silently-dropped monitor-flag; low-harm because the higher tiers above it ARE covered, so a worsening trend re-enters at RHR>100 → URGENT)
  - FM-class: red-flag→tier completeness
  - **h_class_equivalent_max: H4** (under-monitoring of an early autonomic-stress trend; bounded because the URGENT and EMERGENCY rungs above it are intact, so escalation is not lost, only the earliest monitor-rung)
  - composite: **MAJOR** (a safety-architecture Finding's tier is unimplemented AND an AC over-claims completeness against it; this is the single highest-value coverage finding in this report).
- **decision_rule_applied:** Core Rule 9 (locator + zero-match grep on the absent tier) + task check #5 (every red-flag in Finding 14 maps to a tier) + No-Tautological-Tests discipline (AC#10 passes against the doc's reduced red-flag set, not the substrate's full set).
- **paired_probe_status:** [no-paired-probe-required: this is a tier-completeness gap, not a refused/answered pair. The answered region — RHR>100→URGENT — IS present at §14.5; the gap is the rung below it.]
- **remediation_target_owner:** synthesis orchestrator. Route: add the +5–10 bpm sustained-RHR-trend → ROUTINE-MONITOR mapping to §6.2 (and/or a §14 edge case), so the ROUTINE-MONITOR band AC#10 asserts is actually reachable. NOT a Role-3 Edit.
- **severity_final:** PENDING.

### F-005 — §4 cross-role boundary completeness: PASS (no defect — recorded per Anti-Pattern 2, no "no-gap" claim without per-owner evidence)

- **finding_id:** F-005
- **edge_case_class:** cross-role boundary completeness (task check #4) — VERIFIED COMPLETE
- **source_claim_locator:** §4 table L105–116.
- **grep evidence:** all six task-enumerated owners present in §4: `medical-liaison` (L111), `sleep-coach` (L112 — wearable-interpretation split EXPLICIT), `personal-trainer` (L113 — load/ACWR), `cardiovascular-specialist` (L114 — HR/HRV/BP pathology forward-reference, NON-blocking, fallback to medical-liaison), `nutritionist` (L115 — RED-S/energy-availability), `lymphatic-specialist` (L116 — drainage/`vault/protocols/` overlap → contradictions.md). The cardiovascular-specialist forward-reference is explicitly flagged NON-blocking (L118) with a LIVE medical-liaison fallback. No owner missing; no content redefined inline (references-only confirmed).
- **why recorded as a finding:** Per Anti-Pattern 2 + Negative Example 1, Role-3 does not declare "no coverage gap" without per-owner grep evidence. This row IS the evidence: 6/6 owners present, each references-not-redefines, directionality (INBOUND) matches the Pass-3 specialist authoring order. PASS.
- **severity_proposed:** N/A (no defect). h_class_equivalent_max: N/A.
- **decision_rule_applied:** Anti-Pattern 2 (default output is populated coverage, not a bare "looks fine") + Core Rule 8 (stratification not needed — no cross-specialist contradiction surfaced).
- **paired_probe_status:** N/A.
- **severity_final:** N/A.

---

## stratification_attempted

No `specialist_contradiction` finding emitted. The §4 boundaries (recovery autonomic-*trend* vs
cardiovascular HR/HRV-*pathology*; recovery routes vs sleep-coach/nutritionist content-ownership)
are STRATIFIABLE by the doc's own splits (trend-vs-pathology, route-vs-content) and by the LIVE
medical-liaison fallback. The cardiovascular-specialist boundary is a known forward-reference
(§4 L118, §17.1 R-1, §17.3 BC-1, §18 OQ-2), explicitly NON-blocking — not_stratifiable does NOT
hold, so no specialist_contradiction is raised (Core Rule 8). The CV-trend-vs-pathology overlap
is correctly deferred to a break condition, not a present contradiction.

## out_of_scope_observations (named interface + owning role; NOT edited by Role 3)

1. **Adversarial: does a Class-III-shaped request (F-003 HIGH_RISK_SAMD gap) escape the present 6 classes?** Interface: refusal-class routing. Owning role: **Role 4 (medical-safety-reviewer / adversarial)**. Contract: Ask-vs-Proceed §3.3 (coverage-class → Role 3; adversarial-class → Role 4 pattern-N/A). Routed as **pattern-N/A for Role 3**; Role 4 owns the bypass-probe.
2. **§7 has 6 loop-breaking thresholds (template budget 3–5).** Interface: §7 budget. Owning role: synthesis orchestrator (budget is a template-conformance call, not a coverage call). One-line note only; over-budget is non-blocking and the extra thresholds are load-bearing (red-flag + single-reading + H-class + GRADE + research-cap + revision-cap). Not a Role-3 finding.

## Self-audit attestation (Core Rule 11)

- Mechanical pre-audit ran BEFORE semantic adjudication: enum (8 classes grepped `-w`), schema (sections + tables), locator-resolution (2 LIVE paths `ls`-confirmed present; 6 REFERENCED INV IDs all `rg`-confirmed in INVARIANTS.md; risk-class floor matches YAML L71–74), quoted-text-verbatim (all quoted_text fields copied from grep output, not paraphrased). PASS — no crashing/failing audit.
- All 8 canonical refusal classes enumerated in boundary_class_coverage with grep locators + match_counts (Core Rule 3). AUTHORITY_FRAMING_BYPASS verdict EXPLICIT and PRESENT (Core Rule 12).
- Every coverage-gap claim carries a grep locator + the pattern that returned its count (Core Rule 9). No "absent" tagged without a zero-match grep (F-003, F-004 both cite exit-1 greps).
- severity_proposed only on all findings; severity_final PENDING → medical-liaison (Core Rule 7, R8).
- No profile/design-doc Edit performed (Core Rule 1). All remediation routed to owner, never applied.
- Artifact re-Read at §5, §6, §7, §11, §14, §17 boundaries (Core Rule 6).
- No fabricated refusal-class ID / GRADE tier / H-class / PF ID / INV ID / vault path (Fabrication guard): PF-S12-01 + PF-S13-01 verified to exist in the log before citing; HIGH_RISK_SAMD verified to be a real taxonomy class (L55) before flagging its absence.

## coverage_verdict

**BLOCK_WITH_FINDINGS**

Rationale: 19 sections + Appendix A structurally present and the AUTHORITY_FRAMING_BYPASS
mandatory clause PASSES (the auto-CRITICAL case does not fire) — so this is not HALT. But two
MAJOR coverage gaps (F-001 §11.1 PF-omission with a frontmatter↔body contradiction; F-004 an
unimplemented Finding-14 ROUTINE-MONITOR tier under an over-claiming AC) plus two MINOR gaps
(F-002 dangling "boundary coverage" reference; F-003 unverdicted HIGH_RISK_SAMD) exceed a clean
PASS. Findings route to medical-liaison for severity_final + the Phase-5 synthesis for
disposition into Appendix A.
