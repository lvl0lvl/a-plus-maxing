---
title: sleep-coach Design Doc — Phase-3 COVERAGE Red-Team
reviewer_role: health-edge-case-reviewer (Role 3)
target_type: design doc
target: design/sleep-coach-design.md
reviewed_against_ancestry: sleep-coach-design.md @ S-pass3 (status: Phase-3 Red-Team Pending)
substrate_checked: design/.sleep-coach-design-work/domain-research.md (14 Findings, 15 R — verified)
taxonomy: templates/refusal-class-taxonomy.yaml (8 classes — verified)
contract: design/DESIGN_DOC_TEMPLATE.md
emitted: severity_proposed only (never severity_final)
---

# Coverage Red-Team — sleep-coach Design Doc

Mechanical pre-audit ran BEFORE prose adjudication (Core Rule 5/11). Method: the 8 canonical
refusal-class IDs were grep-enumerated against the doc; the §3 Finding-table row count, the §5
Core-Rule count, the substrate Finding/Recommendation counts, the cited PF IDs, and the §5
Finding-citation set were all counted mechanically. Findings below carry a grep locator +
zero/nonzero match. No finding is asserted "absent" without a locator + pattern.

## Mechanical pre-audit results (counts that ground the findings)

| Probe | grep pattern | result | disposition |
|---|---|---|---|
| Substrate Finding headings | `^### Finding` in domain-research.md | 14 | matches §3 claim "14" — PASS |
| Substrate Recommendation rows | `^\| ?R[0-9]+` in domain-research.md | 15 | matches §3 claim "15 R1–R15" — PASS |
| §3.1 Findings-table rows | `^\| [0-9]+ \|` in design doc | 14 | matches substrate 14 — **no §3 count mismatch** |
| §5 Core-Rule count | `^[0-9]+\. \*\*` in §5 | 11 | matches frontmatter/AC "11" — PASS |
| Cited PF IDs resolve | `PF-S\d+-\d+` doc vs process-failures.md | 10/10 resolve | all resolve — PASS |
| §5 Finding-citation set | `F[0-9]+` inside §5 | F1–F8, F10–F14 | **F9 ABSENT from §5** — see C-1 |

The §3 Finding-count probe explicitly clears (the task asked me to probe for a mismatch; there
is none — 14 = 14 = 14).

---

## Findings

### C-1 — The "dominant boundary case" (empty-wearable-state, F9) has NO Core Rule

- **finding_id:** C-1
- **edge_case_class:** missing-coverage / under-specified-state (single-population: no-device-state)
- **severity_proposed:** IMDRF=informs-clinical-management · condition=non-serious · NCC-MERP=Category-C (reaches operator, no harm — fabrication risk) · FM-class=missed-gap · **h_class_equivalent_max: H4** (orthosomnia/fabricated-number risk if the empty-state discipline is not a standing rule)
- **source_claim_locator:** grep_pattern `F9` scoped to §5 (`awk '/## 5\./,/## 6\./'`); match_count in §5 = **0**. Contrast: §1 gap 4 (L30) calls empty-wearable "the dominant boundary case today"; §3.1 row 9 (L72) maps F9 to "Modes, Edge Cases, Context Loading" — NOT Core Rules; R9 (L93) says "Make the empty-wearable-state the dominant Mode."
- **quoted_text:** §5 rules 6 and 7 (L132–133) cover wearable validation-tiering and trend-vs-baseline but BOTH gate on data being PRESENT ("Every wearable-derived statement…", "a single night's HRV/efficiency number"). No rule fires when the Wearable section is `(none yet)`.
- **why_it_matters:** The doc's own §1 names this the dominant case today (Oura pending, LM-02). The behavioral floor "never fabricate an HRV/readiness number when asked 'what's my readiness?'" lives only in §6 step 5, §10 step 3, and §14 (Edge Cases) — none of which become a Core Rule in the deployed agent.md. Per the template's Synthesis Order (§5 of template), Core Rules map 1:1 to the agent.md Core Rules; Edge Cases (§14) is a meta-section that does NOT map to an agent.md section. So the single most-frequent runtime path has standing-rule coverage only via a Mode that emerges at synthesis discretion. A missed-gap, not a contradiction.
- **recommendation:** { action: "add a Core Rule (or fold into rule 6) that names the empty-wearable-state as the default operating mode and the no-fabrication floor when no device data is present, tagged [F9]", target_field: "§5 Core Behavioral Rules", owner: Role-2 }
- **severity_final:** { set_by: pending-adjudicator, verdict: pending }

### C-2 — §11.3 boundary_class_coverage ledger mis-cites the grounding rules for BASIS_NOT_REVIEWABLE and PRESCRIPTIVE_DIRECTIVE

- **finding_id:** C-2
- **edge_case_class:** coverage-ledger integrity (self-audit defect — the ledger that the Phase-3 gate reads is wrong about where its own classes are grounded)
- **severity_proposed:** IMDRF=non-clinical (documentation) · condition=n/a · NCC-MERP=Category-A (no reach) · FM-class=phantom-citation · **h_class_equivalent_max: H2-process** (a coverage ledger that points at the wrong rule defeats the audit it exists to enable)
- **source_claim_locator:** grep_pattern `BASIS_NOT_REVIEWABLE` → §11.3 row (L253) cites "§5 R11"; but R11 (Core Rule 11, L137) is the fabricate/self-attest/AFB rule — it does NOT define BASIS_NOT_REVIEWABLE. BASIS_NOT_REVIEWABLE is actually grounded in §6 step 4 (L146) + §7 research-escalation-cap (L160). Likewise the PRESCRIPTIVE_DIRECTIVE row (L254) cites "§5 R8/R11"; rule 8 (L134) is the escalation floor and rule 11 is fabrication — neither names hypnotic-prescription routing as the prescriptive class; §6 step 3 (L145) is the actual locator.
- **quoted_text:** L253 `| BASIS_NOT_REVIEWABLE | covered | F2/F14; §5 R11, §6 step 4 |` and L254 `| PRESCRIPTIVE_DIRECTIVE | covered | F14; §5 R8/R11, §6 step 3 (hypnotics → prescriber) |`
- **why_it_matters:** The §11.3 ledger IS the artifact the Phase-3 coverage gate reads to confirm each class is grounded. If a downstream reader follows "§5 R11" to verify BASIS_NOT_REVIEWABLE, they land on the fabrication rule and find no basis-reviewability content — a verifier following the citation gets a false trail. The CLASSES are covered (both resolve elsewhere in the doc), so this is a citation-integrity defect, not a true coverage gap — but it degrades the ledger's auditability and risks a downstream "looks covered" rubber-stamp on a broken pointer.
- **recommendation:** { action: "correct the §11.3 grounding column: BASIS_NOT_REVIEWABLE → §6 step 4 + §7 research-escalation-cap; PRESCRIPTIVE_DIRECTIVE → §6 step 3 + §5 rule 8 escalation-floor (which routes hypnotics)", target_field: "§11.3 Boundary-class coverage table, Grounding column", owner: Role-2 }
- **severity_final:** { set_by: pending-adjudicator, verdict: pending }

### C-3 — RBD red-flag escalation has no concrete urgency selector ("URGENT-or-ROUTINE" with no decision rule)

- **finding_id:** C-3
- **edge_case_class:** red-flag without concrete escalation target+urgency (the task's named probe)
- **severity_proposed:** IMDRF=drives-clinical-management · condition=serious (RBD carries injury-to-self/bedpartner risk + is a documented α-synucleinopathy prodrome) · NCC-MERP=Category-D (could require monitoring/intervention to preclude harm) · FM-class=under-specified-escalation · **h_class_equivalent_max: H3** (under-escalation of a serious-condition red-flag)
- **source_claim_locator:** grep_pattern `RBD.*(URGENT|ROUTINE|EMERGENCY|refer)` → the ONLY rule-level routing match is §5 rule 8 (L134): `OSA-screen-positive / RBD / narcolepsy-with-safety-risk → URGENT-or-ROUTINE referral`. grep_pattern `RBD →` (RBD-specific band) → match_count = 0. RBD never gets its own urgency band or a rule that disambiguates URGENT vs ROUTINE.
- **quoted_text:** L134 `OSA-screen-positive / RBD / narcolepsy-with-safety-risk → URGENT-or-ROUTINE referral`
- **why_it_matters:** "URGENT-or-ROUTINE" is a disjunction with no selector — the agent cannot deterministically pass the rule's own Pass/fail ("a red-flag stimulus produces the matching urgency band"), because for RBD there is no single matching band. Contrast the suicidality red-flag (L134), which is fully banded (active SI → EMERGENCY; depressive mood → URGENT) and the drowsy-driving stimulus (acute advisory + URGENT). RBD/narcolepsy sit in an unbanded blend. §14 Edge Cases provides a test stimulus for OSA, suicidality, hypnotics, CBT-I, older-operator — but NO RBD/narcolepsy test stimulus exists (grep `RBD` in §14 = 0), so the under-specification is not closed by an Edge Case either. Note: §18 OQ-2 defers "suicidality escalation threshold calibration" to Role 4/medical-liaison, but it does NOT cover the RBD band ambiguity — that gap is unowned.
- **recommendation:** { action: "give RBD (and the narcolepsy/parasomnia cluster) a concrete default band with a stated selector (e.g., 'RBD/dream-enactment with injury history or bedpartner risk → URGENT; isolated report without safety risk → ROUTINE referral'), and add an RBD test stimulus to §14", target_field: "§5 Core Rule 8 escalation floor + §14 Edge Cases", owner: Role-2 }
- **severity_final:** { set_by: pending-adjudicator, verdict: pending }

### C-4 — PATIENT_FACING_DIRECTIVE coverage row routes "diagnose-me" to a class §6 actually maps to DEVICE_FUNCTION

- **finding_id:** C-4
- **edge_case_class:** class-to-route consistency (in-vocabulary-trigger mapped to two different classes)
- **severity_proposed:** IMDRF=informs · condition=non-serious · NCC-MERP=Category-B (error, no reach — the diagnosis still refuses, only the class label differs) · FM-class=class-aliasing · **h_class_equivalent_max: H4**
- **source_claim_locator:** grep_pattern `PATIENT_FACING_DIRECTIVE` → §11.3 (L250) grounds it in "§6 step 3 (diagnose-me/prescribe-me refusal)". But §6 step 3 (L145) maps "a diagnosis (OSA)" to `DEVICE_FUNCTION / PRESCRIPTIVE_DIRECTIVE / PATIENT_FACING_DIRECTIVE` as a 3-way slash with no rule for which fires. The §48 Identity list encodes DEVICE_FUNCTION for "OSA diagnosis" and does NOT list PATIENT_FACING_DIRECTIVE among the ≥4 encoded classes at all.
- **quoted_text:** L250 `| PATIENT_FACING_DIRECTIVE | covered | F1/F10; §5 R1, §6 step 3 (diagnose-me/prescribe-me refusal) |` vs L48 encoded set: `AUTHORITY_FRAMING_BYPASS … DEVICE_FUNCTION … TIME_CRITICAL … PRESCRIPTIVE_DIRECTIVE … BASIS_NOT_REVIEWABLE` (PATIENT_FACING_DIRECTIVE NOT in the encoded ≥4).
- **why_it_matters:** PATIENT_FACING_DIRECTIVE is marked `covered` in §11.3 but is not among the 5 classes the doc says it "encodes by reference" in §2.2 (L48) — it appears only as a slash-option in §6 step 3 and in the §11.3 ledger. A reviewer reading §2.2 would conclude PATIENT_FACING_DIRECTIVE is NOT an encoded class; a reviewer reading §11.3 would conclude it is. The diagnosis request DOES refuse (via DEVICE_FUNCTION), so there is no behavioral hole — this is a coverage-ledger-vs-encoded-set inconsistency that should be reconciled so the deployed agent.md has a deterministic class for a self-diagnosis request.
- **recommendation:** { action: "either add PATIENT_FACING_DIRECTIVE to the §2.2 encoded-class list with its trigger (self/other clinical-action request), or change the §11.3 ledger to mark it 'covered-via-DEVICE_FUNCTION/PRESCRIPTIVE' and remove the implication it is independently encoded; make §6 step 3 deterministic about which class fires for a diagnosis request", target_field: "§2.2 encoded-class list + §6 step 3 + §11.3 PATIENT_FACING_DIRECTIVE row", owner: Role-2 }
- **severity_final:** { set_by: pending-adjudicator, verdict: pending }

### C-5 — §13 Mechanical Enforcement Map asserts "11 `## ` sections" but the design doc never enumerates the deployed agent.md's Modes section content

- **finding_id:** C-5
- **edge_case_class:** downstream-synthesis under-specification (the Modes section that carries the dominant boundary case is asserted to exist but not specified)
- **severity_proposed:** IMDRF=non-clinical · condition=n/a · NCC-MERP=Category-A · FM-class=deferred-to-synthesis · **h_class_equivalent_max: H2-process**
- **source_claim_locator:** grep_pattern `Modes` → matches at L66/69/70/72 (§3 table maps 4 Findings to "Modes"), L205 (`enter the empty-state Mode (§Modes)`), L349 (`11 ## sections (10 base + Modes)`). grep_pattern `^### Mode|^## .*Modes` (a Modes section heading in THIS doc) → match_count = 0. The doc references "§Modes" (L205) as if it exists but there is no §Modes section in the design doc.
- **quoted_text:** L205 `Empty/absent → enter the empty-state Mode (§Modes); do not fabricate. [F9]` — the cross-reference `(§Modes)` resolves to nothing in this document.
- **why_it_matters:** This compounds C-1. The empty-wearable-state — the dominant boundary case — is routed to "§Modes," but no Modes section is authored in the design doc, and the template (§5 synthesis note, template L106/L622) explicitly says Modes "emerges as a /upgrade-agent Phase 5 synthesis output, not a 1:1 design-doc mapping" and "the synthesizer DECIDES whether to materialize a Modes section." So the doc asserts (§13 audit row, §15.1 NOTE) that the deployed agent.md WILL have exactly 11 sections including Modes, while leaving the Modes content for the dominant case to synthesizer discretion with no design-doc source. The dangling `(§Modes)` self-reference is the concrete defect; the substantive risk is that the dominant-case behavior is specified nowhere with standing-rule force.
- **recommendation:** { action: "either author the empty-state Mode behavior explicitly (a §Modes block or fold into §5 per C-1) so the (§Modes) reference resolves and the 11-section audit-row claim is grounded, or remove the dangling (§Modes) cross-reference and point F9 handling at the Core Rule added per C-1", target_field: "§10 step 1 cross-reference + §5/§Modes content", owner: Role-2 }
- **severity_final:** { set_by: pending-adjudicator, verdict: pending }

---

## Dimensions probed and found CLEAN (with grep evidence — not rubber-stamped)

- **GRADE strong-on-low bounding (the task's headline probe).** grep `EXCEPT CBT-I|other strong-with-low` → §5 rule 9 (L135), §7 GRADE-HALT (L158), §14 (L340), §15.2 #4 (L356) ALL state CBT-I is the SOLE sanctioned exception and "No other strong-with-low pair ships" / "every OTHER strong-with-low HALTs." The exception is bounded to a single named instance (CBT-I), with an operator-acknowledged-override escape for HALTs. A generic strong-on-low pairing does NOT ship un-HALTed. **CLEAN — no finding.**
- **§3 Finding-count mismatch (task probe).** 14 substrate headings = 14 §3.1 rows = §3 prose claim "14." grep `^### Finding`=14, `^\| [0-9]+ \|`=14. **CLEAN — no mismatch.**
- **AUTHORITY_FRAMING_BYPASS mandatory.** grep `AUTHORITY_FRAMING_BYPASS`=9 matches; encoded in §2.2 (L48 "mandatory; operator classed A3"), §5 rule 11 (L137), §6 step 3 (L145), §11.2 AP7 (L241), §11.3 (L257 "covered — MANDATORY"), §12.3 negative example (L294). Taxonomy `mandatory_for_every_specialist: true` honored, operator A3 cited. **CLEAN — fully covered.**
- **Anti-pattern recognition cues.** All 8 §11.2 anti-patterns (L235–242) carry a "Recognition cue:" — grep `Recognition cue:` = 8 matches, one per anti-pattern. **CLEAN — no cue-less anti-pattern.**
- **Operator-state leak (PF-S2-04).** grep `Walter|operator is [0-9]+|age [0-9]+ operator|70 yo` in doc = 0 operator-value inlines. §4 row (L115), §10 step 2 (L206), §17.2 assumption 5 (L402) all bind operator state at DISPATCH, never at authoring, and explicitly cite PF-S2-04. **CLEAN — no leak.**
- **IMAGE_OR_SIGNAL_INPUT narrowing.** grep `IMAGE_OR_SIGNAL` = 2; §8 (L176) + §11.3 (L251) refuse PSG/EEG/ECG and declare "no image/signal Tools path." Taxonomy `mandatory_when:` triggers only if Tools permit image MIME / image-URL WebFetch; the doc's Tools palette (§8) has no such path, so the narrowing is correctly justified. **CLEAN — covered-narrowed, justified.**

---

## boundary_class_coverage (all 8 canonical classes — AFB verdict explicit)

Built by grep-enumerating each class ID against the doc, NOT by reading prose (Core Rule 2/9).

| # | Class | grep match_count | Verdict | Locator + note |
|---|---|---|---|---|
| 1 | PATIENT_FACING_DIRECTIVE | 2 | **covered — with-defect (see C-4)** | §6 step 3 (L145), §11.3 (L250); NOT in §2.2 encoded set (L48); class-aliasing finding C-4 |
| 2 | IMAGE_OR_SIGNAL_INPUT | 2 | covered — narrowed (justified) | §8 (L176), §11.3 (L251); no image Tools path → mandatory_when untriggered |
| 3 | TIME_CRITICAL | 8 | covered | §2.2 (L48), §5 rule 8 (L134), §6 step 2 (L144), §7 floor (L156), §14 (L338) — SI fully banded EMERGENCY/URGENT |
| 4 | BASIS_NOT_REVIEWABLE | 8 | **covered — mis-cited grounding (see C-2)** | actual locator §6 step 4 (L146) + §7 (L160); §11.3 row points at wrong rule |
| 5 | PRESCRIPTIVE_DIRECTIVE | 7 | **covered — mis-cited grounding (see C-2)** | §6 step 3 (L145), §14 (L339 zolpidem stimulus); §11.3 row cites wrong rules |
| 6 | DEVICE_FUNCTION | 11 | covered | §2.2 (L48), §6 step 3 (L145), §11.3 (L255), §12.3 (L296); OSA/AHI/CPAP/continuous-monitor all refused |
| 7 | HIGH_RISK_SAMD | 1 | not-covered — out-of-scope (LEGITIMATE) | §11.3 (L256): held off by inform-class posture; not an active card; mirrors labs-specialist. Accepted as a justified not-covered, not a gap. |
| 8 | **AUTHORITY_FRAMING_BYPASS** | 9 | **covered — MANDATORY, VERIFIED** | §2.2 (L48), §5 rule 11 (L137), §6 step 3 (L145), §11.2 AP7 (L241), §11.3 (L257), §12.3 (L294); taxonomy `mandatory_for_every_specialist: true` honored; operator A3 cited |

**AFB verdict: PASS — covered, mandatory, operator-A3 anchored, present in ≥6 sections including a dedicated negative example.** This is the one class the Role-3 profile flags as PATIENT-SAFETY-CRITICAL-if-absent; it is not absent.

Coverage tally: 6 covered-substantively + 1 covered-narrowed-justified (IMAGE) + 1 not-covered-justified (HIGH_RISK_SAMD). 0 of the 8 classes is silently absent. The 3 covered-with-defect annotations (C-2 ×2, C-4) are citation/encoding defects in the LEDGER, not behavioral holes — the classes themselves all refuse correctly somewhere in the doc.

---

## coverage_verdict

**BLOCK_WITH_FINDINGS.**

Rationale: AFB is present and verified (the single PATIENT-SAFETY-CRITICAL gate clears), and all 8
classes resolve somewhere. No class is silently absent, so this is not a HALT. But 5 findings stand:
one true missed-gap on the doc's OWN dominant boundary case having no Core Rule (C-1), a compounding
dangling-Mode reference (C-5), an under-specified serious-condition red-flag band (C-3), and two
coverage-ledger integrity defects (C-2, C-4). C-1 and C-3 are the load-bearing ones (h_class_max H4
and H3 respectively). Per my profile (Negative Examples: "missing rule → BLOCK_WITH_FINDINGS even for
a low-risk domain"), a lifestyle-tier sleep domain does not earn a PASS while its dominant runtime
path lacks a standing rule.

## out_of_scope_observations

- **(Role 4, adversarial)** §18 OQ-2 forwards "suicidality escalation threshold calibration" to Role 4 + medical-liaison. The RBD band ambiguity (C-3) is adjacent but NOT covered by that OQ; whether RBD's default-band selector is a coverage fix (Role 2) or a safety-conservative adjudication (Role 4) may need Role-4 input. Interface: §5 rule 8 escalation floor / OQ-2. Clause crossed: Role-3 owns coverage-gap surfacing; Role-4 owns the safety-band adjudication.
- **(adjudicator/medical-liaison, severity_final)** All `severity_proposed` above are 4-axis proposals only; the severity_final verdict and any BLOCK-vs-WARN call on C-1/C-3 belongs to the adjudicator, not to this reviewer (Core Rule 7, R8).
- **(Role 2, profile prose)** The dangling `(§Modes)` reference (C-5) is a prose/structure defect; the fix is Role-2's authoring call (materialize Modes vs fold into §5). I emit the finding; I do not author the Mode block.

## Self-audit attestation

- Mechanical pre-audit ran before semantic adjudication (Core Rule 5/11): substrate counts, §3 row count, §5 rule count, PF-ID resolution, §5 Finding-citation set, and per-class grep all executed and recorded above. Not self-attested — the count tables are the produced artifacts.
- boundary_class_coverage enumerates all 8 classes with per-class grep match_count + locator (Core Rule 3, R2). No "absent" tag without a zero-match locator (Core Rule 9): C-1 (F9 in §5 = 0), C-5 (§Modes heading = 0), C-3 (`RBD →` band = 0).
- severity_proposed only, 4-axis + h_class_equivalent_max; no severity_final emitted (Core Rule 7, R8).
- I did not Edit the artifact (Core Rule 1, R1). No fabricated class ID / PF ID / vault path — all 10 cited PF IDs verified to resolve in process-failures.md.
- AFB verdict rendered explicit (PASS) per Communication field 5.
- This audit did not crash; it is therefore a passing self-audit (Core Rule 11).
