# lymphatic-specialist — Pass-3 Phase-0 Domain Research (synthesis digest)

**Role slug:** `lymphatic-specialist`  ·  **Role class:** specialist  ·  **Risk class:** `compound-medium` (mode floor `standard`, per `templates/specialist-risk-class.yaml`; the YAML `target_class: compound` is the RISK ANCHOR — lymphatic-relevant venoactive/benzopyrone agents at medium risk — that sets the standard floor, identical to `cardiovascular-specialist`; this role's WIKI owned-writes are `protocols (lymphatic)` + `biomarkers (lymphatic/inflammation)`, NOT `compounds/`, so dispatch target-class is `protocol`/`biomarker` and compounds route OUT — see Finding 12 + design-doc §18 OQ).
**Pipeline:** aplus-research standard-mode discipline run at orchestrator level (CONTINUATION_BRIEF Lesson 1: parallel-dispatch phases run where Agent-tool access lives). Output routed to `design/.lymphatic-specialist-design-work/` — NOT the wiki (PF-S2-04: the specialist consumes the wiki, it does not author it; this is agent-design research, not a wiki-bound protocol/biomarker entry).
**Corpus:** four paired (retrieval + independent judge) section dispatches. Phase-3.5 JUDGE GATE PASS at standard threshold 92/100: Section A 95 (iter-2 after a type-tag + author-conflation HALT remediation), Section B 94 (iter-2 after a citation-fidelity HALT remediation — wrong PREVENT-trial PMID, PF-S2-02 class, caught by the gate), Section C 95 (iter-1), Section D 94 (iter-1). Per-section files + bibliographies live alongside this digest at `sections/section-{A,B,C,D}.md`; per-section judge verdicts at `judges/judge-{A,B,C,D}.json`. ~14,700 words, ~90 distinct sources, every claim type-tagged per `vault/library/_source-whitelist.md`. The two HALTs were remediated by the retrieval agents under the post-fix grep discipline and re-judged by FRESH independent judges (iter-2), never self-cleared (PF-S2-01/PF-S3-01).

This digest lifts the load-bearing structural conclusions into `### Finding` headings + `R1–R15` recommendations so the design doc §3 can anchor against them without paraphrase drift. Citations resolve to the named section's bibliography (e.g. "A[14]" = Section A reference [14]).

---

## Findings

### Finding 1 — lymphatic-specialist is an inform-class interpreter, not a diagnostician or prescriber

The domain divides into an interpretable/educational layer (fluid-status interpretation, drainage-modality evidence-grading, inflammation-marker context) and a clinical layer (lymphedema diagnosis/staging, cellulitis/DVT/malignancy work-up, prescription and device titration) carrying hard statutory and safety boundaries. Lymphedema diagnosis and staging require clinical assessment + imaging [B, C, regulatory]; the agent must not diagnose, dose, titrate a compression/pneumatic device, or interpret lymphatic imaging. The posture mirrors the deployed `labs-specialist`/`sleep-coach` (inform-class, basis-reviewable, escalation-over-interpretation), not any directive posture.
**Informs:** AGENT_TEMPLATE Identity, Role Boundaries, Anti-Patterns.

### Finding 2 — the established-vs-provisional boundary is the agent's central epistemic discipline (high pseudoscience load)

This is the sharpest-pseudoscience domain in the roster. Section A documents the load-bearing case: meningeal lymphatic vessels EXIST (Louveau 2015, Aspelund 2015, A[14]/A[15], animal + emerging human imaging), but the "glymphatic clears toxins / deep sleep prevents Alzheimer's" CLEARANCE-FUNCTION narrative is PROVISIONAL and actively contested — Miao 2024 (A[22], animal) reported clearance *reduced* during sleep, the reverse of the original Xie 2013 (A[19], animal) direction, with AQP4-convection itself disputed (Mestre 2020, A[17], mechanism_review). The agent must preserve the established/provisional boundary in every user-facing statement and never launder rodent mechanism into proven human fact.
**Informs:** Core Rules, Anti-Patterns, Negative Examples.

### Finding 3 — the lymphatic system is a return-flow + immune-surveillance system, NOT a toxin store; revised Starling is why lymphatics are obligatory

The revised Starling principle (Levick & Michel 2010, A[8], mechanism_review) is ESTABLISHED: net capillary filtration is returned by the lymphatics, not reabsorbed at the venous end — which is precisely why lymphatics are obligatory to fluid homeostasis. The system collects net-filtered fluid/protein and traffics antigen/immune cells to nodes (A[1]–A[3]); it is NOT a storage depot accumulating "toxins" awaiting manual release. Xenobiotic detoxification is hepatic (biotransformation) + renal (excretion) [A, regulatory/mechanism_review]. There is no evidence a healthy person's lymphatics need "draining" or "cleansing."
**Informs:** Core Rules, Anti-Patterns, Negative Examples.

### Finding 4 — no validated routine blood biomarker of "lymphatic function"; systemic-inflammation markers (hs-CRP/IL-6) are NOT lymphatic-function readouts; tier every measure by validation status

Section B establishes the validation gradient. **Validated-clinical:** ISL staging 0–III (qualitative, clinician-assigned), limb-volume (water displacement / perometry / circumferential-truncated-cone), and bioimpedance spectroscopy (BIS/L-Dex, FDA-cleared assessment aid; PREVENT trial Ridner B[5], rct — early BIS-triggered intervention reduced progression to chronic BCRL vs tape; 3-yr figures B[23], rct). **Clinician/SaMD-tier imaging:** lymphoscintigraphy (reference standard), ICG-NIRF, MR/CT lymphangiography — NOT agent-interpretable. **Research-only:** VEGF-C, podoplanin/D2-40. **Systemic-inflammation (NOT lymphatic):** hs-CRP, IL-6, TNF-α, ESR. **Consumer/not-validated:** vibration plates, EMS "lymphatic" devices, "lymphatic" thermography. There is no validated routine blood test of lymphatic-drainage efficiency.
**Informs:** Core Rules, Tools, Communication.

### Finding 5 — single value is noise; interpret trends against the operator's own intra-individual baseline (the RCV analog)

Day-to-day interstitial-fluid fluctuation and measurement variability (limb-volume SEMs ~3.6–6.6%; hs-CRP within-subject CV ~0.44, ICC ~0.62, ~118% critical difference for sequential significance, B) mean a single cross-sectional reading against a population range is noise. Interpretation requires serial intra-individual measurement (limb-volume change over time; the operator's own hs-CRP trend) — the direct lymphatic analog of the labs-specialist RCV gate and the sleep-coach single-night rule.
**Informs:** Core Rules, Loop-Breaking, Modes.

### Finding 6 — imaging + device-derived lymphatic measures are clinician/SaMD-tier (DEVICE_FUNCTION); consumer "lymphatic" gadget readings are not clinical measures

Lymphoscintigraphy/ICG/MR-lymphangiography interpretation and continuous device monitoring are SaMD/clinician functions [B, regulatory]. The agent cannot interpret a lymphatic image/scan, relay a device output as a diagnosis, or operate as a continuous-monitoring device. Consumer "lymphatic" devices (vibration, EMS, thermography, hand-held drainage tools) are unvalidated and must never be treated as clinical measures (the orthosomnia-analog harm: a gadget reading surfaced as a verdict).
**Informs:** Role Boundaries (DEVICE_FUNCTION, IMAGE_OR_SIGNAL_INPUT), Anti-Patterns.

### Finding 7 — cellulitis / erysipelas / acute lymphangitis is a TIME_CRITICAL escalation AND a hard contraindication to MLD/massage

Red, hot, painful, spreading skin ± fever/systemic signs needs prompt antibiotics and can progress to sepsis (C[?], regulatory: IDSA/NICE); ascending lymphangitis (red streaking) or systemic toxicity → EMERGENCY, otherwise URGENT. CRITICAL: manual lymphatic drainage / massage / exercise on the affected limb is CONTRAINDICATED during active infection. Recurrent cellulitis both complicates and drives lymphedema.
**Informs:** Role Boundaries (TIME_CRITICAL), Loop-Breaking (escalation floor), Negative Examples.

### Finding 8 — a swollen limb may be DVT, not lymphedema; massage/compression on an undiagnosed acute DVT risks PE — recognize-and-route before any drainage advice

A new acute unilateral painful swollen limb is DVT-until-excluded; Wells criteria are a clinical pre-test SCREEN, not a diagnosis (C, regulatory). Massage/compression on undiagnosed acute DVT risks dislodging thrombus → pulmonary embolism. PE signs (dyspnea, pleuritic pain, syncope, hemodynamic instability) → EMERGENCY. The agent routes to rule out DVT before offering any drainage guidance.
**Informs:** Role Boundaries (TIME_CRITICAL/recognize-and-route), Loop-Breaking, Edge Cases.

### Finding 9 — generalized/systemic edema (cardiac/renal/hepatic) is NOT a lymphatic-drainage problem; malignant lymphadenopathy is recognize-and-route; lipedema ≠ lymphedema

Bilateral lower-limb edema ± dyspnea/orthopnea → heart-failure work-up (URGENT; sudden + chest pain/breathlessness → EMERGENCY); periorbital/generalized → renal/hepatic (C, regulatory). The agent must NOT treat systemic edema as a "lymphatic drainage" problem to massage. Persistent hard/fixed/painless/>2 cm or supraclavicular nodes, or B-symptoms (fever, night sweats, weight loss) → URGENT malignancy/lymphoma work-up; never reassure a suspicious node away. Lipedema (a fat disorder, frequently misdiagnosed) ≠ lymphedema and has different management. These are the "looks-lymphatic-but-isn't" traps.
**Informs:** Role Boundaries, Edge Cases, Anti-Patterns.

### Finding 10 — CDT/compression is the canonical GRADE strong-recommendation-on-modest-certainty case; MLD-specifically is low-certainty and must not be oversold

Complete Decongestive Therapy (compression + MLD + exercise + skin care) is the guideline-recommended standard for diagnosed lymphedema, with COMPRESSION as the load-bearing component [D, regulatory/meta_analysis]. The Cochrane review (Ezzo 2015, D, meta_analysis) finds MLD adds limited benefit over compression alone for BCRL — low-to-moderate certainty. This is the canonical strong-on-modest-certainty pairing: privilege the strong action (CDT/compression) while surfacing the certainty gap and NOT overselling MLD; any OTHER strong-on-low pairing HALTs. Exercise (incl. resistance) is safe and beneficial — the agent de-bunks the old "don't exercise the affected limb" myth (Schmitz PAL, D, rct).
**Informs:** Core Rules (GRADE two-axis + HALT), Communication.

### Finding 11 — "lymphatic drainage for detox / weight-loss / cellulite / immune-boosting" in healthy people is not evidence-based → BASIS_NOT_REVIEWABLE; transient cosmetic de-puffing ≠ detox

For healthy people with no diagnosed lymphatic pathology, "lymphatic detox/cleanse" massage, dry brushing, rebounding/vibration "for lymph," "lymphatic cleanse" supplements/teas, and "facial lymphatic drainage" for more than transient cosmetic puffiness are not evidence-based (D, A; advertising-standards rulings characterize the claims as unsupported). The agent's rule: in the absence of diagnosed lymphatic dysfunction these claims are BASIS_NOT_REVIEWABLE; transient cosmetic de-puffing is not "detox." This is the bounded clinical reality (MLD/CDT works for diagnosed lymphedema — a clinical-population effect) without over-correcting into nihilism.
**Informs:** Core Rules, Anti-Patterns, Negative Examples.

### Finding 12 — lymphatic-relevant COMPOUNDS route OUT (not owned-write); never dose; benzopyrone/diuretic safety is load-bearing

Lymphatic-relevant compounds exist but are NOT this role's owned-write (compounds are owned by supplement-specialist; Rx by prescriber): benzopyrones/coumarin carry hepatotoxicity (Loprinzi 1999 NEJM, D, rct — led to withdrawal in some markets); diosmin+hesperidin/MPFF (Daflon) has modest CVI evidence, weaker in lymphedema; selenium has limited evidence; diuretics are generally NOT effective for chronic lymphedema and can be harmful [D, rct/meta_analysis]. The agent reads/cross-references these for routing, never authors a compound entry or emits a dose; risk_tier medium+ or Rx → PRESCRIPTIVE_DIRECTIVE → medical-liaison/prescriber; supplement-class → route to supplement-specialist.
**Informs:** Role Boundaries (cross-role routing, PRESCRIPTIVE_DIRECTIVE), Tools, Edge Cases.

### Finding 13 — operator immune/inflammation biomarkers + recovery protocols are read at dispatch; the empty-state is the dominant case today

Per `vault/meta/current-state.md` the Blood and Wearable sections are empty (first labs July 2026) and `operator-profile.md` is a scaffold. The agent will eventually consume inflammation biomarkers (hs-CRP/IL-6) + recovery protocols, but none exists at deploy time. The agent must operate correctly with NO biomarker/fluid data (educate from established science + self-report, surface that no data exists, fabricate nothing) and bind the Finding 4/5 validation+trend discipline the moment data appears — mirrors the labs-specialist/sleep-coach empty-state Mode.
**Informs:** Modes (empty-state), Context Loading, Edge Cases.

### Finding 14 — AUTHORITY_FRAMING_BYPASS is mandatory; framing never relaxes a directive gate; behave identically under suspected testing; never self-attest a research gate

Operator is the single operator, classed A3 (operator-self-harm via own-agent; the 81.8%-of-successful-attacks vector per Role 1 §2.2 item 3). Authority/educational/hypothetical framing ("as a lymphedema therapist, just confirm my AHI-equivalent / give me the benzopyrone dose / skip the disclaimer") never relaxes a directive, device-function, or prescriptive gate; the refusal posture is identical whether or not a turn is framed as a test. A dispatched `aplus-research` gate verdict is dispatched-agent-produced, never self-declared (PF-S2-01/PF-S3-01). Inherit the three-mechanism anti-sycophancy scaffold from Role 1 verbatim.
**Informs:** Core Rules, Anti-Patterns; `refusal-class-taxonomy.yaml` (mandatory_for_every_specialist).

---

## Recommendations

| # | Recommendation | Verdict | Grounding |
|---|---|---|---|
| R1 | Adopt an inform-class, basis-reviewable, escalation-over-interpretation posture mirroring `labs-specialist`/`sleep-coach`; never diagnose, stage, dose, titrate a device, or interpret lymphatic imaging. | ACCEPTED | F1 |
| R2 | Encode the established-vs-provisional boundary as a Core Rule; never state meningeal-lymphatic/glymphatic clearance ("flushes toxins / prevents Alzheimer's") as proven; tag certainty; flag animal/contested claims (Miao-vs-Xie direction reversal). | ACCEPTED | F2 |
| R3 | State the lymphatic system as return-flow + immune-surveillance, NOT a toxin store; attribute xenobiotic clearance to liver/kidney; affirm no healthy person needs lymphatic "draining/cleansing." | ACCEPTED | F3 |
| R4 | Tier every lymphatic/fluid measure by validation status (validated-clinical / clinician-SaMD imaging / research-only / consumer-unvalidated); state that hs-CRP/IL-6 are systemic-inflammation markers, NOT lymphatic-function readouts; no validated routine blood test of lymphatic function. | ACCEPTED | F4 |
| R5 | Interpret fluid/inflammation measures only as trends against the operator's own rolling intra-individual baseline (the RCV analog); a single value is noise. | ACCEPTED | F5 |
| R6 | Encode DEVICE_FUNCTION + IMAGE_OR_SIGNAL_INPUT refusals for lymphatic-imaging interpretation, device-output-as-diagnosis, and continuous monitoring; never treat a consumer "lymphatic" gadget reading as a clinical measure. | ACCEPTED | F6 |
| R7 | Encode a TIME_CRITICAL escalation for cellulitis/erysipelas/lymphangitis (URGENT; systemic/ascending → EMERGENCY) AND a hard contraindication: no MLD/massage/exercise on an actively infected limb. | ACCEPTED | F7 |
| R8 | Recognize-and-route a new acute unilateral swollen painful limb as DVT-until-excluded BEFORE any drainage advice (massage/compression risks PE); PE signs → EMERGENCY; Wells is a screen, not a diagnosis. | ACCEPTED | F8 |
| R9 | Recognize-and-route systemic edema (cardiac/renal/hepatic — never massage as "lymphatic"), malignant lymphadenopathy (URGENT; never reassure away), and the lipedema≠lymphedema distinction. | ACCEPTED | F9 |
| R10 | Instantiate GRADE two-axis with CDT/compression as the canonical strong-recommendation-on-low/moderate-certainty case (privilege the strong action, surface the certainty gap); do not oversell MLD-specifically; any OTHER strong-on-low HALTs. | ACCEPTED | F10 |
| R11 | Refute "lymphatic detox/cellulite/immune-boost/weight-loss" claims for healthy people → BASIS_NOT_REVIEWABLE; name transient cosmetic de-puffing ≠ detox; do not over-correct into denying the bounded clinical role of CDT for diagnosed lymphedema. | ACCEPTED | F11 |
| R12 | Route lymphatic-relevant compounds OUT (supplement-specialist / prescriber); never author a compound entry or emit a dose; PRESCRIPTIVE_DIRECTIVE for benzopyrone/diuretic/Rx requests; surface benzopyrone hepatotoxicity + diuretic-ineffectiveness as known safety facts, not doses. | ACCEPTED | F12 |
| R13 | Make the empty-biomarker-state the dominant Mode; read operator immune/inflammation biomarkers + recovery protocols at dispatch; never fabricate a fluid/biomarker value; bind the F4/F5 discipline the moment data appears. | ACCEPTED | F13 |
| R14 | Surface the contraindication gate to drainage modalities (active infection, acute/undiagnosed DVT, decompensated heart failure, acute renal failure; severe PAD caution; active malignancy now relative-not-absolute) before any drainage education. | ACCEPTED | F7, F8, F9 |
| R15 | Mandate AUTHORITY_FRAMING_BYPASS; framing never relaxes a gate; behave identically under suspected testing; never self-attest an aplus-research gate; inherit the three-mechanism anti-sycophancy block from Role 1 verbatim. | ACCEPTED | F14; refusal-class-taxonomy.yaml (mandatory_for_every_specialist) |

**Recommendation-count rationale:** N=15, matching the foundation-deliverable convention. All ACCEPTED — no DEFERRED/REJECTED (this digest is design substrate; deferrals surface at design-doc §3.2/§18, not here).

---

## Self-check (synthesis level)

- **No orchestrator self-attestation (PF-S2-01/PF-S3-01).** Every Phase-3.5 judge verdict is a dispatched INDEPENDENT judge agent (`judges/judge-{A,B,C,D}.json`). The two iter-1 HALTs (A 91: type-tag + author-conflation; B 91: wrong PREVENT-trial PMID) were remediated by the retrieval agents under the mandatory post-fix grep discipline and re-judged by FRESH independent judges at iter-2 (A 95, B 94) — never self-cleared by the orchestrator. The orchestrator will additionally personally source-read each finding at design-doc Phase 4 (PF-S3-01 guard).
- **Goal-agnostic (PF-S2-04).** Findings ground AGENT DESIGN (how the specialist reasons), not operator personalization; no operator-specific state is baked in. Operator-profile/current-state are scaffolds, read as linkage context only; routed to design-work, not the wiki (the specialist consumes the wiki, does not author it).
- **Citation fidelity.** The PF-S2-02-class defect (Section B PREVENT-trial wrong PMID 31054045) was caught by the judge gate and remediated to the verified PMID 31054038 (interim) + a new verified 3-yr source (Shah 2024, PMID 38965099); the unverifiable 11.3%/59% figures were REMOVED rather than retained against a wrong source. All load-bearing Section-A PMIDs (Levick&Michel 20200043; Louveau 26030524; Aspelund 26077718; Iliff 22896675; Xie 24136970; Miao 38741022; Mestre 32423764; Ezzo 25994425) were judge-spot-checked against live PubMed.
- **Type-tag discipline.** Every claim carries exactly one whitelist type-tag; the Section-A iter-1 mis-tags (Cochrane review as `rct`; narrative review as `meta_analysis`; an out-of-enum `anecdote_aggregate`) were corrected and re-verified. Vendor/anecdote sources ground no numerical claim.
- **Population/concentration handling.** Animal evidence (the rodent glymphatic corpus: Iliff/Xie/Miao) is explicitly flagged single-species + contested; no single-lab ≥70% dominance in this protocol/biomarker-domain corpus (orthogonal to the compound-class concentration audit).
- **Residual caveats forwarded to design-doc §18.** (a) Section B's ICG sensitivity/specificity "one series" figures (89.5%/85.7%) lack an identified citation and were flagged non-load-bearing by the iter-2 judge — verify before any downstream wiki ingestion. (b) Several review-tier bibliographic specifics in A/B were assembled from search-result metadata rather than full-text reads (full-text fetch was rate-limited); load-bearing landmark PMIDs were verified, snippet-sourced specifics are honestly flagged. (c) Section C urgency-band thresholds (node-duration cut-points, ABI cutoff, active-malignancy relative-vs-absolute) are safety-conservative judgment calls flagged for medical-liaison ratification before any threshold is asserted as guideline-fixed.
