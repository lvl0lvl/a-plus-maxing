---
title: "mental-performance-coach Design Doc — Phase-3 Role-3 Coverage Red-Team"
type: red-team-coverage
role_reviewer: health-edge-case-reviewer (Role 3)
artifact_under_review: design/mental-performance-coach-design.md
substrate: design/.mental-performance-coach-design-work/domain-research.md
canonical_inputs:
  - templates/refusal-class-taxonomy.yaml
  - templates/specialist-risk-class.yaml
  - design/sleep-coach-design.md (claimed precedent)
  - memory/process-failures.md
phase: design-doc Phase 3 (coverage; NOT a deployed agent.md)
generated: 2026-05-31
coverage_verdict: BLOCK_WITH_FINDINGS
severity_note: severity_proposed only — severity_final is the adjudicator's (Role 7 / medical-liaison)
---

# mental-performance-coach Design Doc — Phase-3 Role-3 Coverage Red-Team

## coverage_verdict: BLOCK_WITH_FINDINGS

Three findings (F-001 P1, F-002 P1, F-003 P2). The SI floor (the single load-bearing surface,
Finding 14) is comprehensively encoded and grep-resolves on every §15.2 assertion — that is NOT
the gap. The gaps are class-encoding coherence (DEVICE_FUNCTION operationally used as an active
routing class in §6/§8/§17 but declared "held off" / not-encoded in §2.2), the absence of the
§11.3 boundary-class-coverage ledger that the claimed-precedent sleep-coach carries (and which is
this Role's own canonical discipline per Core Rule 3), and a missing §15.2 acceptance criterion
binding that ledger. None of the three touches the SI floor, the dispatch floor, or a fabricated
number; all three are coverage/coherence, recoverable at Phase 5 by a drafter without a substrate
re-run.

---

## Mechanical pre-audit (run before semantic adjudication — Core Rule 5, R7)

- schema: this report carries header + boundary_class_coverage block + numbered findings — PASS.
- enum: every severity_proposed drawn from {PATIENT-SAFETY-CRITICAL, REGULATORY-BREACH,
  EVIDENCE-FABRICATION, COVERAGE-GAP, STYLISTIC} — PASS.
- locator-resolves: artifact + substrate + both YAMLs + sleep-coach + PF log all read this session — PASS.
- quoted-text-verbatim: each quoted_text below copied from the cited line — PASS.
- status-transition-legal: Phase-3-Red-Team-Pending → coverage_verdict emitted, no edit to artifact — PASS.
- self-audit (Core Rule 11): boundary_class_coverage enumerates all 8 classes with a locator each;
  AUTHORITY_FRAMING_BYPASS verdict explicit; TIME_CRITICAL (SI floor) explicit — PASS, does not crash.

---

## boundary_class_coverage (all 8 canonical classes — `templates/refusal-class-taxonomy.yaml`)

AUTHORITY_FRAMING_BYPASS verdict is explicit and TIME_CRITICAL (the SI floor) is explicit, per the mandate.

| # | Class | Verdict | Locator + grep pattern → result |
|---|---|---|---|
| 1 | `AUTHORITY_FRAMING_BYPASS` | **[covered] — MANDATORY, satisfied** | §2.2 L46 "Encoded: `AUTHORITY_FRAMING_BYPASS` (mandatory — operator classed A3)"; reinforced §6 step 3 L141, §5 rule 12 L133, §12.4 L284. `grep -w AUTHORITY_FRAMING_BYPASS` → 8 matches. §13 LIVE row `authority-framing-mandatory` resolves in `scripts/audit-specialist-profile.sh` (subcheck verified on disk). |
| 2 | `TIME_CRITICAL` | **[covered] — the SI floor, load-bearing** | §2.2 L46; Core Rule 1 L122; §6 step 2 L140; §7 L152; §14 L319. `grep -w TIME_CRITICAL` → 5. SI bands fully present: `active SI.*EMERGENCY`→3, `passive.*URGENT`→5, `benign trailing`→5, `minimization.*never downgrade`→4, `medical-liaison`→24, `persists across turns`→3. |
| 3 | `PATIENT_FACING_DIRECTIVE` | **[covered]** | §2.2 L46 (in Encoded set); Core Rule 2 L123; §6 step 3 L141; §14 L321. `grep -w PATIENT_FACING_DIRECTIVE` → 7. |
| 4 | `PRESCRIPTIVE_DIRECTIVE` | **[covered]** | §2.2 L46; §5 rule 6 L127; §6 step 3 L141; §12.4 L285. `grep -w PRESCRIPTIVE_DIRECTIVE` → 8. |
| 5 | `BASIS_NOT_REVIEWABLE` | **[covered]** | §2.2 L46; §6 step 5 L143; §7 L156; §14 L324. `grep -w BASIS_NOT_REVIEWABLE` → 5. |
| 6 | `DEVICE_FUNCTION` | **[INCONSISTENT — see F-001]** | §2.2 L46 declares it "held off … not encoded" yet §6 step 3 L141 routes a request deterministically *to* DEVICE_FUNCTION, §8 L171 cites "(DEVICE_FUNCTION)" as the governing restriction, §17.1 risk-5 L375 names a "DEVICE_FUNCTION restriction" as a mitigation. `grep -w DEVICE_FUNCTION` → 4 (all 4 *use* it as an active class; the one §2.2 mention denies encoding it). Operationally encoded, declared not-encoded. |
| 7 | `IMAGE_OR_SIGNAL_INPUT` | **[not-covered: narrowed — correctly]** | §2.2 L46 "narrowed (Read is text/markdown only; no PSG/EEG/ECG raw-signal interpretation)"; §8 L171 forbids raw-signal interpretation. Taxonomy `mandatory_when: Tools permits Read against image MIME OR WebFetch from image URLs`; this doc's Tools (§8 L162) permits neither — `grep -icE "tavily|WebSearch|WebFetch"` in doc → 0. Narrowing is contract-correct, not a gap. |
| 8 | `HIGH_RISK_SAMD` | **[not-covered: out-of-scope — correctly]** | §2.2 L46 "out-of-scope (inform-class, no diagnose/treat function)". Taxonomy trigger is a Class-III SaMD treat/diagnose function the inform-class posture does not perform; mirrors sleep-coach §11.3 disposition. Not a gap. |

Coverage tally: 5 cleanly covered (incl. both mandatory: AFB + TIME_CRITICAL); 1 inconsistent (DEVICE_FUNCTION, F-001); 2 correctly-excluded with cited rationale (IMAGE, HIGH_RISK_SAMD). The ≥4-class + AFB-mandatory floor is met on the operative set regardless of F-001's resolution.

---

## Findings

### F-001 — DEVICE_FUNCTION is operationally an active refusal/routing class but §2.2 declares it not-encoded ("held off")

- **finding_id:** F-001
- **edge_case_class:** class-encoding inconsistency (the in-/out-of-vocabulary trigger boundary region — Role-3-owned)
- **section affected:** §2.2 (L46) vs §6 step 3 (L141), §8 restrictions (L171), §17.1 risk 5 (L375), §13 (no DEVICE_FUNCTION audit row)
- **severity_proposed:** COVERAGE-GAP / P1-revise
- **source_claim_locator:** `grep -w DEVICE_FUNCTION design/mental-performance-coach-design.md` → 4 matches. Three (§6 L141, §8 L171, §17.1 L375) *use* it as the deterministic class a continuous-monitoring / wearable-score-as-readout request maps to; one (§2.2 L46) *denies* it is encoded.
- **quoted_text:** §2.2 L46 — "`DEVICE_FUNCTION` is held off by the inform-class posture (no continuous stress-monitoring-with-alerts; a wearable score is never a measured readout)." Contradicted by §6 step 3 L141 — "a 'continuously monitor my stress and alert me' / read-a-wearable-score-as-readout request → DEVICE_FUNCTION" and §8 L171 — "no continuous stress-monitoring-with-alerts and no treating a wearable score as a measured readout (DEVICE_FUNCTION)."
- **why_it_is_a_gap:** This is the exact class-encoding-inconsistency pattern the claimed-precedent sleep-coach's own Phase-3 red-team caught as finding C-4 (severity H4): "PATIENT_FACING_DIRECTIVE marked covered … but absent from the §2.2 encoded set." Here the polarity is inverted — DEVICE_FUNCTION is *used* as an active class downstream while §2.2 declares it *not* encoded. sleep-coach §2.2 L48 ENCODES DEVICE_FUNCTION in its set and §11.3 marks it `covered`; this doc, claiming to mirror sleep-coach, demotes the same class to "held off" while still routing to it. A deterministic §6 routing target that the encoded-set declaration disowns leaves the deployed agent without a contract anchor for the card string + escalation_target that §6/§8 presuppose. The §13 mechanical map has no DEVICE_FUNCTION row, so nothing audits the inconsistency.
- **recommendation {action, target_field}:** action=`reconcile_class_encoding`; target_field=§2.2 encoded-set declaration (move DEVICE_FUNCTION from "held off" into the Encoded set, OR remove it as a deterministic routing target from §6 step 3 / §8 / §17.1 and re-route continuous-monitoring/wearable-as-readout to an encoded class). NOT a fix authored here — surfaced for the Phase-5 drafter / adjudicator.
- **severity_final:** {set_by: pending-adjudicator, verdict: pending}

### F-002 — §11 lacks the §11.3 boundary-class-coverage ledger the precedent carries and that this Role's Core Rule 3 mandates

- **finding_id:** F-002
- **edge_case_class:** coverage-ledger omission (boundary-class enumeration discipline)
- **section affected:** §11 (ends at §11.2 L224; no §11.3) vs synthesis-note L17 claim
- **severity_proposed:** COVERAGE-GAP / P1-revise
- **source_claim_locator:** `grep -nE "^### 11\.[0-9]"` → only `11.1` (L211) and `11.2` (L224); no `11.3`. `grep -niE "boundary.class coverage|all 8 canonical"` → 1 hit, all at §2.2 L46 (prose, not a ledger). Compare sleep-coach: `grep -niE "11\.3"` → L251 "### 11.3 Boundary-class coverage (all 8 canonical refusal classes)" — a per-class table.
- **quoted_text:** synthesis-note L17 — "coverage/edge-case sections (§6, §7, §10, §14, §18) follow the edge-case-reviewer lens." The list omits a §11.3, and §2.2 L46 self-labels "the boundary-class coverage of the canonical 8" — but it is a single prose sentence, not the per-class `[covered]/[not-covered] + locator` ledger that the edge-case-reviewer discipline (this Role's Core Rule 3) requires and that sleep-coach §11.3 materializes.
- **why_it_is_a_gap:** sleep-coach — the doc this artifact claims to "mirror + intensify" — carries an explicit §11.3 table enumerating all 8 classes with verdict + grounding, expressly "so the Phase-3 coverage gate has an explicit ledger." That ledger is where sleep-coach's own C-2/C-4 ledger-vs-encoded-set inconsistencies were caught and corrected. This doc has no equivalent, so the F-001 DEVICE_FUNCTION inconsistency had no in-doc ledger to surface it before red-team. The §2.2 prose is a coverage *claim*; it is not the auditable per-class ledger the precedent established as the coverage-gate artifact.
- **recommendation {action, target_field}:** action=`add_boundary_class_ledger`; target_field=new §11.3 (mirror sleep-coach §11.3 — all 8 classes, verdict, grounding locator). NOT authored here.
- **severity_final:** {set_by: pending-adjudicator, verdict: pending}

### F-003 — §15.2 acceptance criteria have no AC binding the 8-class boundary ledger / deterministic class mapping

- **finding_id:** F-003
- **edge_case_class:** acceptance-criterion coverage gap (downstream-enforcement)
- **section affected:** §15.2 (L338–L348) vs sleep-coach §15.2 AC3 (L366)
- **severity_proposed:** COVERAGE-GAP / P2-annotate
- **source_claim_locator:** `awk` over §15.2 → no AC contains `boundary.class | 11.3 | ledger | deterministic` (zero matches). Compare sleep-coach §15.2 AC3 L366 — "§6 step 3 maps each directive request to a single deterministic class."
- **quoted_text:** §15.2 AC2 L339 — "Role Boundaries encode ≥4 taxonomy class IDs including `AUTHORITY_FRAMING_BYPASS` (`grep -w` ≥1)." This counts classes but does not assert (a) a per-class coverage ledger exists, nor (b) each §6 directive maps to exactly one deterministic class — the two checks that would have caught F-001/F-002 at the AC gate.
- **why_it_is_a_gap:** AC2 verifies a count, not coverage coherence. Without an AC binding the deterministic-class-mapping (sleep-coach AC3) or the §11.3 ledger, the §15.2 gate cannot fail on the F-001 inconsistency or the F-002 omission — the deployed agent.md could ship with DEVICE_FUNCTION still split between "held off" and "active routing target" and pass §15.2. This is the downstream-enforcement face of F-001/F-002.
- **recommendation {action, target_field}:** action=`add_acceptance_criterion`; target_field=§15.2 (an AC asserting each §6 directive maps to one deterministic encoded class, and the §11.3 ledger enumerates all 8). NOT authored here.
- **severity_final:** {set_by: pending-adjudicator, verdict: pending}

---

## Probe results that PASSED (coverage confirmed — cited so "no gap" is not asserted blind)

Per Role-3 anti-pattern discipline (do not declare "no gap" without per-class grep evidence): the
following surfaces were probed and are covered. These are NOT findings.

- **SI floor completeness (Finding 14, load-bearing).** active→EMERGENCY/passive→URGENT bands, benign-
  trailing-never-cancels, minimization-never-downgrades, persists-across-turns, routes-to-LIVE-medical-
  liaison, never-diagnose/score/treat — all present and grep-resolve (Core Rule 1 L122; §6 step 2 L140;
  §7 L152; §14 L319–L320; §15.2 AC3 L340). Every §15.2 grep assertion returns ≥1. No band missing vs the
  sleep-coach precedent (sleep-coach §5 rule 8 / §12.4); the doc additionally adds the medical-liaison-
  offline degraded-mode fail-safe (§14 L325) and the two-boundary stimulant composition (§5 rule 6 L127,
  §7 L153, §12.4 L278). **No gap.**
- **performance-vs-clinical boundary, paired (not one-sided).** Burnout-as-disorder / PHQ-9-GAD-7-pattern →
  escalate (Core Rule 2 L123; §14 L321) is correctly PAIRED with burnout-workload/recovery IN-lane and
  stress-resilience levers as adjuncts (L23, L123 "burnout … is in-lane for workload/recovery", L321
  "offer in-lane stress-resilience levers as adjuncts"). PHQ-9/GAD-7/C-SSRS not-scored: grep 4/7/3, every
  hit in a refuse-to-score context. The doc is not one-sidedly refusing. **No gap (paired probe satisfied).**
- **lead-with-levers, nootropic→supplement escalation, GRADE two-axis HALT, mechanism-vs-outcome,
  correlation-vs-causation, wearable caveat, brain-training refusal, aplus dispatch floor, no-self-attest.**
  All grep-resolve: `supplement-specialist`→19 (incl. §2.2 Role Boundaries + Core Rule 5 L126); BDNF→8 with
  `population-mismatch`→6 (Core Rule 8 L129); Mediterranean→7 (Core Rule 9 L130); `readiness|black-box|
  wearable`→15 (Core Rule 10 L131); brain-training/far-transfer (Core Rule 11 L132); `aplus-research
  --mode=standard --target-class=protocol`→6 with no bare `deep-research` used as a dispatch (all 6
  `deep-research` hits are "never the bare deep-research" prohibitions); no `vault/compounds` in the
  Write/Edit scope (§8 L162 Write scope excludes it; the 3 `vault/compounds` write-context hits are all
  the prohibition clause itself, not a write grant). **No gap.**
- **§3 digest vs substrate counts.** §3.1 = 15 finding rows; §3.2 = 15 R-rows; substrate = 15 `### Finding`
  headings + 15 top-level §4 recs. Counts match (15/15). All §3.1 + §3.2 verdicts ACCEPTED, no TBD. **No gap.**
- **§13 mechanical map status tags.** LIVE rows resolve on disk (`scripts/audit-specialist-profile.sh` +
  all 10 named `--check` subchecks verified present; `.claude/hooks/enforce-role-inlining.sh` present);
  PROPOSED SI-floor script correctly absent + flagged non-gating (§18 OQ-1); REFERENCED INV-* rows all
  resolve in INVARIANTS.md (7/7 checked). Status tags coherent. **No gap.** (DEVICE_FUNCTION's *absence*
  from §13 is folded into F-001, not double-counted here.)
- **§11.1 PF coverage.** 8 distinct PFs verdicted (PF-S2-01..06, PF-S3-01, PF-S6-01), each resolves in
  `memory/process-failures.md`. NOTE (out_of_scope_observations, not a finding): sleep-coach §11.1 also
  carries PF-S12-01 + PF-S13-01 as explicit OUT-OF-SCOPE rows; this doc omits both. They are session-
  lifecycle PFs and genuinely out-of-scope for runtime, so omission is defensible — but the precedent
  lists-and-dispositions them rather than dropping them. Surfaced for the adjudicator's awareness; below
  the P3 bar as a coverage finding.
- **§16 invariants scope + concentration claim.** Research-domain IN-scope is correct (the role dispatches
  aplus-research). The 0.143 concentration-share claim (§16 L360) matches the substrate verbatim
  (domain-research L13, L226, L341: "share 0.143"). INV-BRANCH-NOT-MAIN out-of-scope is correct. **No gap.**
- **Identity ≤40 words.** §2.1 L38 = 30 words. **No gap.**
- **988 parameterized.** §17.2 assumption 4 L383 "988 is the parameterized US escalation target, not a
  hardcoded universal." **No gap.**

---

## out_of_scope_observations (one-line, not edited, not re-dispatched)

- §11.1 omits PF-S12-01/PF-S13-01 that the sleep-coach precedent dispositions as OUT-OF-SCOPE rows
  (defensible omission; noted, not promoted to a finding).
- Appendix A is the empty Phase-3 placeholder; this report is the Role-3 input it will be populated from
  at Phase 5 (not a defect at Phase 3).

---

## 7 Communication fields (to orchestrator)

1. **Status:** complete — Phase-3 Role-3 coverage red-team of the design doc; mechanical pre-audit PASS, semantic adjudication done, self-audit non-crashing.
2. **Artifact paths:** review target `design/mental-performance-coach-design.md`; report written to `design/.mental-performance-coach-design-work/red-team-role3-coverage.md`.
3. **Specialist slug + ancestry:** `mental-performance-coach`; specialist / protocol-medium / standard / protocol (confirmed in `templates/specialist-risk-class.yaml` L82-L86); Pass-3 doc, substrate `domain-research.md` (15 findings / 15 R).
4. **Findings count + severity distribution + coverage_verdict:** 3 findings — COVERAGE-GAP×3 (P1×2, P2×1); 0 PATIENT-SAFETY-CRITICAL, 0 REGULATORY-BREACH, 0 EVIDENCE-FABRICATION, 0 STYLISTIC. **coverage_verdict: BLOCK_WITH_FINDINGS.**
5. **Boundary-class coverage tally (AFB explicit):** 5 covered (incl. both mandatory — AUTHORITY_FRAMING_BYPASS satisfied, TIME_CRITICAL/SI-floor satisfied), 1 inconsistent (DEVICE_FUNCTION — F-001), 2 correctly-excluded with rationale (IMAGE_OR_SIGNAL_INPUT narrowed, HIGH_RISK_SAMD out-of-scope). ≥4 + AFB-mandatory floor met regardless of F-001.
6. **Blockers / AQs:** none requiring an Architecture Question (no fabricated/needed-new class; no cross-role INBOUND-row touch). F-001/F-002/F-003 route to the Phase-5 drafter + adjudicator, not to an edit by this Role.
7. **Self-audit attestation:** boundary_class_coverage enumerates all 8 classes with a per-class locator; every coverage-gap claim carries a grep pattern + result; severity_proposed only (severity_final pending-adjudicator on all 3); no edit made to the artifact under review; proposed severity maintained without new evidence.
