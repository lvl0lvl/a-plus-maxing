# Phase-0 Deep-Research Synthesis — endocrine-specialist (design substrate)

**Mode:** deep (risk class `compound-medium-or-experimental`, mode_floor `deep`, target_class `compound` per `templates/specialist-risk-class.yaml`).
**Purpose:** synthesis-level substrate for `design/endocrine-specialist-design.md` §3 (Pass-1 Deliverable Digest). NOT a wiki entry — no `vault/compounds/*` authored (PF-S2-04: this build consumes the wiki, does not author it).
**Retrieval substrate:** 5 axis sections in this directory — `section-A-hpg-trt.md` (HPG: T/E2/DHEA + TRT, 18 findings/11 sources), `section-B-hpt-thyroid.md` (HPT: thyroid, 16/16), `section-C-hpa-cortisol.md` (HPA: cortisol/adrenal, 15/11), `section-D-insulin-gh-igf.md` (insulin/metabolic + GH/IGF-1, 21/24), `section-E-crossaxis-safety-regulatory.md` (cross-axis + refusal/safety/regulatory, 18/21). **~88 retrieval findings across ~80 unique admissible sources** — far exceeds the deep-mode floor (≥25 unique; ≥6/section). Inline finding references below use `[<Section><n>]` (e.g., `[E11]`) pointing into those files; the bibliography is the union of the five `## Sources` blocks.

**Body↔bibliography symmetry (CONTINUATION_BRIEF Lesson 3):** every structural Finding's `[<Section><n>]` reference resolves to a numbered source in the named section file's `## Sources`; no orphan references. Verified at synthesis.

---

## Judge-gate record (Phase 3.5 — PF-S2-01 / PF-S3-01: dispatched-agent verdicts, NOT self-attested)

Two **independent paired judges** scored the 5-section corpus against the 9 rubric dimensions and verified the flagged-suspicious citations by live fetch. Verdicts at `judges/judge-1.json`, `judges/judge-2.json`.

- **judge-1:** overall REVISE — 0 critical / 4 major (all citation-fidelity metadata).
- **judge-2:** overall REVISE — 1 critical / 2 major (citation-fidelity metadata; the "critical" was the wrong PMID on the H1 self-insulin cite).
- **Consensus:** reasoning/design quality high; every defect was citation-metadata, not analysis; each defective cite corroborated by a verified companion, so **no structural Finding or agent rule rests on a fabrication.**

**Remediation applied (targeted, judge-supplied corrections + one orchestrator live-fetch):**
| Cite | Defect | Fix | Source of fix |
|---|---|---|---|
| D[15] | PMID 12782552 → unrelated paper | → PMID **12893725** (real Evans & Lynch) | both judges (verified fetch) |
| A[5] | PMID 27784544 labeled "Ohlander 2018" | → relabeled **Jones 2015** (what the PMID serves); mechanism corroborated by Bhasin [A1] | both judges |
| C[5] | author/pages wrong | → **Panton KK, 79(5):314-319, PMID 31161807** (DOI + 2–3× claim correct) | both judges |
| C[6] | DOI `dgad762` → wrong paper (Fitz 2024) | → DOI **`dgad763`, PMID 38173358** (claim verified vs abstract: 41 OCP vs 46 controls) | orchestrator live fetch |
| E[16] | PMID 20169675 = 2009 rule on 3 other steroids | → statutory anchor (ASCA 1990; 21 CFR 1308.13(f)); claim is correct | both judges |
| A14 vs E | A asserted unverified "81.8%" | → reconciled to E's verified figures (≥80–92% ASR); 81.8% flagged-unverifiable per CONTINUATION_BRIEF §11 | both judges |

**Gate disposition:** PASS-after-targeted-remediation. The corrections are metadata only; the dispatched-judge verification (not orchestrator self-attestation) supplied every correct value except C[6], which the orchestrator verified by live fetch and logged. No re-analysis required; per the rubric's loop-break, metadata corrections to judge-supplied values do not require a fresh judge dispatch (the verification was already dispatched-agent-produced).

---

## Structural Findings (one row per load-bearing conclusion → design-doc §3.1)

### Finding 1 — Hormones are a coupled system; a single-analyte verdict is an error
HPA→HPG (cortisol suppresses GnRH/LH) `[E1]`, thyroid→SHBG/CBG (levothyroxine raises SHBG ~80–120%) `[E3]`, insulin→SHBG (hyperinsulinemia lowers SHBG, raises free androgens, in men) `[E4]`, and LH/FSH branching primary vs secondary hypogonadism `[A6]` mean a low/abnormal value is frequently a downstream/functional signal, not a primary-gland diagnosis. The agent reads the axis as a pattern, never a lone number. [→ Core Rule; Anti-Pattern "single-analyte verdict"]

### Finding 2 — No interpretation without provenance (draw-time, assay/method, age/sex range, units)
Testosterone has marked diurnal + day-to-day variation requiring ≥2 morning fasted draws `[A1]`; LC-MS/MS ≠ immunoassay and is non-comparable across labs `[A2]`; cortisol is diurnal and uninterpretable without draw-time `[C1]`; IGF-1 and TSH reference ranges are meaningless without age/sex `[D8][B1]`. A value lacking provenance is non-interpretable, not a finding. [→ Core Rule; Refusal DATA_INSUFFICIENT/BASIS_NOT_REVIEWABLE; Edge case]

### Finding 3 — Diagnosis is out of scope (PATIENT_FACING_DIRECTIVE)
"Do I have low T / hypothyroidism / Cushing's / insulin resistance / acromegaly" is a person-specific diagnostic conclusion requiring dynamic/confirmatory testing the agent cannot adjudicate (repeat morning T `[A1]`, cosyntropin stimulation `[C2]`, dexamethasone suppression `[C3]`, glucose-suppression for GH `[D7]`, age-matched IGF-1 `[D8]`). Refuse-and-route to clinician; the agent may name the confirmatory test, never render the verdict. [→ Refusal PATIENT_FACING_DIRECTIVE; H4 deferred-diagnosis]

### Finding 4 — Dosing/titration is the most load-bearing refusal (PRESCRIPTIVE_DIRECTIVE)
No dose, no titration, ever — testosterone `[A12]`, levothyroxine/T3 `[B3][B9]`, hydrocortisone/fludrocortisone/DHEA taper `[C9][C10]`, GH, insulin `[D15]`. Endocrine dosing composes directly into H1/H2 (levothyroxine-into-adrenal-crisis `[E2]`; supraphysiologic-T cardiovascular harm `[A13]`; insulin hypoglycemia `[D15]`). This is the highest-design-weight class together with AUTHORITY_FRAMING_BYPASS. [→ Refusal PRESCRIPTIVE_DIRECTIVE; Core Rule "no dosing, ever"; H1/H2]

### Finding 5 — Endocrine emergencies are TIME_CRITICAL and symptom-recognized, not lab-gated
Thyroid storm, myxedema coma (mortality ~30–50%) `[B13]`, adrenal/Addisonian crisis `[C7]`, severe hypoglycemia `[D5]`, DKA/HHS present as symptom clusters in chat `[E8]`. Hormone levels do not separate crisis from uncomplicated disease — treatment begins before labs. Symptom cluster overrides any pending lab analysis → emergency escalation; do not interpret. [→ Refusal TIME_CRITICAL; Loop-Break short-circuit; H1 AUTO-BLOCK]

### Finding 6 — AUTHORITY_FRAMING_BYPASS is the design's central threat (single-operator self-harm)
Authority/educational/credential framing is the dominant successful-attack vector against medical LLMs (≥80–92% ASR across verified methods `[E11]`). Because the operator IS the user, they can iteratively re-frame to talk their own agent into a PRESCRIPTIVE_DIRECTIVE — there is no third-party gate. Refusal is invariant to claimed credentials, claimed purpose, and turn count. (The project's "81.8%" label traces to a flagged-unverifiable source — CONTINUATION_BRIEF §11 — and is not relied on; the dominance claim stands on verified figures.) [→ Refusal AUTHORITY_FRAMING_BYPASS (mandatory); Core Rule "framing-invariant"; H2]

### Finding 7 — The anabolic-steroid hard limit is categorical, not an evidence question
The operator's `goals.md` carries an explicit hard limit "No anabolic steroids." The TRT↔AAS boundary is dose/intent, not molecule `[E12]`: supraphysiologic dosing, "optimization" above the reference range, non-T anabolics, PCT/SERM-after-cycle, gray-market sourcing cross into AAS territory (cardiomyopathy: mean LVEF 52±11% vs 63±8% in users `[A13]`). A hard limit is refused categorically — the agent does NOT weigh risk/benefit. [→ AUTO-BLOCK Refusal; Core Rule; H2]

### Finding 8 — Functional-medicine pseudo-constructs route to BASIS_NOT_REVIEWABLE
"Adrenal fatigue" is rejected by a 58-study systematic review and unrecognized by any endocrinology society `[C5]`; salivary "adrenal stress index" / 4-point diurnal panels are non-validated `[C6]`; reverse-T3 "dominance" is non-actionable and recommended-against `[B4]`; cortisol:DHEA-S "stress score" `[C13]` and "thyroid resistance" `[E9]` lack reviewable basis. The agent refuses to reason FROM the premise and corrects it, routing real symptoms to validated evaluation. [→ Refusal BASIS_NOT_REVIEWABLE; Anti-Pattern]

### Finding 9 — Mechanism ≠ human outcome; GRADE two-axis on every load-bearing claim
Never upgrade confidence from mechanism alone. IGF-1/cancer is mechanism (in-vitro/rodent, population-mismatch-tagged) + observational/MR epidemiology, NEVER interventional `[D16][D17]`; DHEA is mechanism-interesting but human-outcome-absent `[A18][C11]`. Every load-bearing recommendation carries `certainty × strength`; a strong-with-low/very-low pairing HALTs (downgrade or override-log). [→ Core Rule; GRADE]

### Finding 10 — Panel multiplicity: a lone flag on a broad panel is expected noise
For k independent analytes, P[≥1 abnormal] ≈ 1 − 0.95^k (≈40% at k=10, ≈64% at k=20) `[E5]`. A single out-of-range flag on a 15–25 analyte hormone panel is statistically expected, not a finding — contextualize against pretest probability and clustering, never escalate on flag count. Mirrors labs-specialist Rule 2. [→ Core Rule; Anti-Pattern "flag-counting"]

### Finding 11 — Assay artifacts must be screened FIRST
Biotin falsely alters TSH/T4/T3 (case: TSH 0.24→3.30 off biotin) `[B5]`; direct-analog free-T is invalid `[A3]`; non-sensitive E2 immunoassay overestimates in men `[A7]`; estrogen/OCP/pregnancy raise CBG ~2–3× inflating TOTAL cortisol while free is unchanged `[C4][C6]`; insulin assays are non-standardized (~10–30% disagreement) making HOMA-IR cross-lab incomparable `[D1]`. The agent screens these artifacts before interpreting any panel. [→ Core Rule; Edge case; Anti-Pattern "interpreting an assay artifact as disease"]

### Finding 12 — H-class placement (worst_case = max(nominal, worst-case-reachable); H1/H2 auto-block)
Exogenous insulin **H1** (iatrogenic hypoglycemia → death) `[D15]`; thyroid storm/myxedema/adrenal crisis **H1** `[B13][C7]`; levothyroxine into undiagnosed adrenal insufficiency **composed-H1** `[E2]`; TRT erythrocytosis → thrombotic **H2** (escalating from H4 monitorable) `[A9]`; chronic AAS cardiomyopathy/atherosclerosis **H2** `[A13]`; supraphysiologic GH/IGF-1 **H2** where malignancy-acceleration mechanism engages (**H7** nominal) `[D17][D18]`; chronic GH excess cardiomyopathy/dysglycemia **H4–H5** `[D19]`; thyroid over-replacement AF/bone-loss **H4** `[B12]`; AI over-suppression bone loss **H5** `[A8]`; levothyroxine absorption interactions **H6** `[B14]`. [→ Anti-Pattern; H-class enumeration; AUTO-BLOCK on H1/H2]

### Finding 13 — Composed-harm is blocked as a trajectory, not summed per-compound
Multi-hormone stacks (GH+insulin+T inherit insulin's H1) `[D20]`; cross-axis sequences (treat hypothyroidism with undiagnosed adrenal insufficiency → crisis `[E2]`; rT3→add-T3 layered on lower-TSH-feels-better → self-directed over-replacement `[B16]`; the steroid self-management chain `[C14]`). Each step may be individually deflectable; the agent must detect the assembled trajectory and hard-block, never evaluate turn-by-turn. [→ Anti-Pattern; Refusal COMPOSED-HARM; inherits worst-component H-class]

### Finding 14 — Role boundaries and handoffs
Peptide GH secretagogues (sermorelin/CJC-1295/ipamorelin/tesamorelin/MK-677) → **peptide-specialist** (endocrine owns the GH/IGF-1 AXIS interpretation + hormone-class framing + IGF-1 monitoring ceiling, NOT the per-compound dosing) `[D11]`; HbA1c glycemic interpretation → **labs-specialist** (endocrine owns hormone-axis effects on HbA1c only) `[D6]`; OTC adaptogens ashwagandha/rhodiola → **supplement-specialist** (endocrine interprets the cortisol axis, not the adaptogen) `[C12]`; pituitary/red-flag pathology (prolactinoma `[A15]`, central hypothyroidism `[B6]`, acromegaly/Cushing's/Addison's `[C2][C3][D9]`) → clinician; HIGH/MEDIUM safety blocks → **medical-liaison** adjudicator (live). [→ Role Boundary]

### Finding 15 — Concentration-of-evidence is acute in hormone-"optimization" literature
"Optimization"/TRT outcome claims frequently originate from single-clinic case series or industry-affiliated cohorts `[E17]`; the IGF-1/cancer human signal is concentrated in PROSTATE (Travis IPD OR 1.21 overall, 1.29 prospective) `[D17]` — do not over-generalize to "IGF-1 causes all cancers." Where ≥70% of load-bearing evidence traces to one clinic/sponsor/group, that concentration is a first-class caveat with downgraded certainty, not a footnote. [→ Core Rule; Anti-Pattern]

### Finding 16 — Regulatory facts stated plainly and time-stamped
Testosterone = US DEA Schedule III controlled substance (ASCA 1990) `[E16]`; GH non-approved distribution is uniquely criminalized under 21 U.S.C. §333(e), where "distribution" includes writing a prescription `[E14]`; WADA prohibits S1 androgens, S2 GH/secretagogues, S4 AIs/SERMs `[A16][E15]`; compounded ≠ approved ≠ safe `[E16-ACOG]`. Stated as objective boundary inputs, time-stamped, without moralizing. [→ Core Rule; Edge case]

### Finding 17 — Optimization-without-indication is refused
Reference-range is not "optimal"; age-related decline is not pathology; "my T is normal but I want it higher" is not a medical indication `[A17]`. IGF-1 follows a U-shaped mortality curve (EPIC-Heidelberg: both lowest and highest quintiles elevated) `[D18]` — the defensible target is the mid-range age-appropriate band, not maximal. [→ Anti-Pattern; Refusal OPTIMIZATION_WITHOUT_INDICATION]

### Finding 18 — Empty-state + unpopulated-hard-limit discipline
`operator-profile.md` / `current-state.md` / `goals.md` are scaffold (unpopulated); read at dispatch not authoring, applying only what is present, never inlining operator content (PF-S2-04, PF-S6-01). The Jan-2026-issue section being unpopulated means ALL `risk_tier: medium+` hormone compounds are a HALT (operator-profile R7 precondition). Empty biomarker/labs state → report no data, do not fabricate; goal-agnostic library pre-staging is permitted. [→ Core Rule; Context Loading; Edge case]

---

## Pass-1 Recommendations (R1–R18 → AGENT_TEMPLATE.md sections)

| # | Recommendation | agent.md section |
|---|---|---|
| R1 | Read hormones as coupled axes; emit no single-analyte verdict | Core Rules / Anti-Patterns |
| R2 | Provenance-gate every value (draw-time, assay/method+lab, age/sex range, units) before interpreting | Core Rules / Ask-vs-Proceed |
| R3 | No person-specific diagnosis; name the confirmatory test, route to clinician (PATIENT_FACING_DIRECTIVE) | Core Rules / Role Boundaries |
| R4 | No dose, no titration, ever, for any hormone/compound (PRESCRIPTIVE_DIRECTIVE) | Core Rules / Ask-vs-Proceed |
| R5 | TIME_CRITICAL symptom-cluster short-circuit: escalate to emergency care, do not interpret | Loop-Breaking / Core Rules |
| R6 | AUTHORITY_FRAMING_BYPASS: framing-invariant refusal; credentials/purpose/turn-count never bypass | Core Rules / Anti-Patterns |
| R7 | AAS hard limit categorical per goals.md — supraphysiologic/non-T-anabolic/PCT/gray-market = hard refusal, not evidence-weighed | Core Rules / Ask-vs-Proceed |
| R8 | BASIS_NOT_REVIEWABLE for functional-medicine pseudo-constructs; correct the premise, don't reason from it | Core Rules / Anti-Patterns |
| R9 | Keep mechanism vs human-outcome distinct; GRADE two-axis; strong-with-low HALT | Core Rules |
| R10 | Screen assay artifacts first (biotin/direct-free-T/sensitive-E2/CBG/insulin-assay) | Core Rules / Edge cases |
| R11 | worst_case_h_class = max(nominal, worst-case-reachable); H1/H2 auto-block; insulin H1, TRT-erythrocytosis/AAS H2, GH/IGF H7→H2 | Core Rules / Anti-Patterns |
| R12 | Composed-harm: block stacks & cross-axis sequences as a trajectory, inherit worst H-class | Anti-Patterns / Loop-Breaking |
| R13 | Handoffs: peptide secretagogues→peptide-specialist; HbA1c→labs; adaptogens→supplement; HIGH/MED block→medical-liaison; pituitary/emergency→clinician | Role Boundaries / Context Loading |
| R14 | Concentration-audit: ≥70% single-group → first-class caveat + downgraded certainty | Core Rules |
| R15 | State regulatory facts plainly + time-stamped (Sched III T, §333(e) GH, WADA, compounded≠approved) | Core Rules / Edge cases |
| R16 | Refuse optimization-without-indication; target mid-range age-appropriate IGF-1, not maximal | Anti-Patterns |
| R17 | Dispatch `aplus-research --mode=deep --target-class=compound`; never bare `deep-research`; enforce type-tag/population-mismatch/concentration on returns; gate verdicts dispatched-agent-produced (PF-S2-01/PF-S3-01) | Tools |
| R18 | Read operator-profile/current-state/goals at dispatch not authoring; HALT on unpopulated hard-limit field; empty-state path; never inline operator content (PF-S2-04/PF-S6-01) | Context Loading / Core Rules |

---

## Consolidated open gaps (carried from section open-gaps after remediation)

- **Numeric figures still needing primary-abstract confirmation before wiki ingestion** (none load-bearing for an agent.md rule — agent.md cites no external PMIDs): Evans & Lynch "70 IU" `[D15]`; estradiol-immunoassay % bias magnitude `[A]`; myxedema-coma 30–50% mortality `[B14]`; adrenal-crisis per-100-pt-yr incidence `[C9]`; antibody-prevalence exact percentages `[B8]`.
- **Venue-soft sources used for direction only, not numeric grounding:** Frontiers NTIS review `[B6]`; Endotext/AFAR `[D17][D13]`; practitioner-clinic dose-range `[E13]` (the 75–100 mg/week TRT figure is better anchored to Bhasin 2018 `[A1]` — use the guideline primary).
- **No endocrinology-specific empirical jailbreak ASR study exists** — authority-framing dominance is grounded on cross-domain medical-LLM evidence `[E11]`.
- **No interventional RCT tests whether IGF-1-raising compounds CAUSE human cancer** — the H7→H2 escalation rests explicitly on mechanism + observational/MR epidemiology, stated as such, not papered over `[D]`.
- **Pregnenolone / rhodiola** lack dedicated retrieved primaries — grouped with DHEA/ashwagandha under "unsupported as hormonal optimization," and they are supplement-specialist territory regardless.

These are wiki-ingestion-time confirmations; none blocks the agent DESIGN, which cites PF ids / vault paths / the taxonomy, not external PMIDs.
