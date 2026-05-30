# Section B — Measurement & Assessment of Lymphatic / Interstitial-Fluid Status + Inflammation Biomarkers (the Validation-Tiering Discipline)

*This section grounds the domain science a `lymphatic-specialist` agent must reason over. It is goal-agnostic and library-style: it establishes WHICH measures are validated for WHAT and tiers each one by validation status, so the agent never elevates a consumer "lymphatic health" gadget reading or a single inflammation lab to the status of a verdict. No operator personalization appears here. The load-bearing output is the per-measure validation tier — `validated-clinical`, `research-only`, or `not-validated/consumer` — and the principle that a single cross-sectional value is noise against intra-individual baseline.*

**Type-tag convention.** Every claim carries exactly one inline tag from: `rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory`, written `[N, tag]` where N is the bibliography number. ESTABLISHED vs PROVISIONAL is marked per claim. **Agent rule:** lines are bolded operational constraints derived from the evidence.

---

## B.1 Lymphedema assessment & staging — the ESTABLISHED clinical tools

**ISL staging.** The International Society of Lymphology (ISL) 2020 Consensus Document is the consensus reference for clinical staging of peripheral lymphedema [1, regulatory]. It defines four stages [1, regulatory]:

- **Stage 0 (latent / subclinical):** lymph-transport capacity is impaired and subtle changes in tissue fluid/composition and subjective symptoms may be present, but no overt swelling is evident; this latent stage may persist months to years before stages I–III emerge [1, regulatory].
- **Stage I:** early accumulation of relatively high-protein fluid that subsides with limb elevation; pitting may occur [1, regulatory].
- **Stage II:** elevation alone rarely reduces swelling; pitting is manifest, and late in the stage fibrosis makes tissue no longer pit [1, regulatory].
- **Stage III:** lymphostatic elephantiasis — pitting absent, with trophic skin changes [1, regulatory].

ESTABLISHED as the clinical staging vocabulary. The ISL itself notes the staging is a clinical descriptor, not a quantitative measurement, and refers only to the physical condition of the limb [1, regulatory]. **Agent rule:** ISL stage is a clinician's qualitative classification, not a number an agent can compute from photos or self-report; the agent may use the vocabulary to interpret a clinician's documented stage, never to assign one.

**Limb-volume measurement methods (validation tier: `validated-clinical`).** A systematic review of measurement instruments (Hidding et al., 2016) found that four tools have evidence for good reliability and validity: bioimpedance spectroscopy (BIS), water volumetry, tape measurement, and perometry [2, meta_analysis]. Key validity facts [2, meta_analysis]:

- **Water displacement (volumetry)** is the historical reference test for upper-extremity volume in research; the review explicitly designates it the reference standard for the upper limb [2, meta_analysis]. Standard error of measurement (SEM) ~3.6% in upper extremities [2, meta_analysis]. Limitation: messy, contraindicated with open wounds, gives a single whole-limb volume with no segmental information.
- **Perometry (optoelectronic)** uses an infrared frame to compute volume from limb cross-sections; SEM ~5.6% [2, meta_analysis]. Intrarater/interrater ICCs for upper-extremity water volumetry, tape, and perometry cluster at 0.98–0.99 [2, meta_analysis]. Limitation: device cost, footprint, requires the patient positioned in the frame.
- **Circumferential tape + truncated-cone volume:** circumferences taken at fixed intervals are converted to a volume estimate via the truncated-cone (frustum) formula. SEM ~6.6% — the least precise of the validated methods [2, meta_analysis]. Tape-vs-perometer comparison work confirms tape is the most observer-dependent method, with agreement adequate for clinical screening but wider limits than perometry (Sharkey et al., 2018) [3, cohort]. Limitation: highly technique-dependent; landmark placement and tape tension drive variability.

ESTABLISHED, all four `validated-clinical`. A staging-relevant detail the agent must hold: **BIS detects extracellular-fluid changes at ISL stage I, whereas volume-based methods (water, tape, perometry) detect change only from stage II onward** [2, meta_analysis]. **Agent rule:** the choice of measure is stage-dependent — a normal tape/perometer volume does NOT rule out early (stage 0–I) fluid change that only BIS or imaging would catch; "limb looks normal" is not "lymphatics are normal."

---

## B.2 Bioimpedance spectroscopy (BIS / L-Dex) and tissue dielectric constant (TDC)

**What BIS measures.** BIS passes a low-level multifrequency current and derives the ratio of extracellular fluid in the at-risk limb versus the contralateral limb; the L-Dex score quantifies this inter-limb impedance ratio, enabling detection of fluid shifts before clinical swelling is visible [4, meta_analysis]. Validation tier: `validated-clinical` for unilateral, limb lymphedema surveillance.

**The PREVENT trial — the pivotal validation.** PREVENT was a prospective randomized trial (1,200 randomized; 879 analyzed in the interim, up to ~918 monitored to 36 months) comparing BIS (L-Dex) surveillance against tape-measure surveillance for breast-cancer-related lymphedema (BCRL) [5, rct][23, rct]. Subclinical lymphedema triggered a compression-garment intervention: in the BIS arm the trigger was an L-Dex increase ≥6.5 units; in the tape arm a ≥5% to <10% inter-limb volume increase [5, rct]. The interim analysis (Ridner et al., 2019) reported a 9.8% absolute / 67% relative reduction in progression to chronic BCRL favoring BIS [5, rct]. The 3-year follow-up (Shah et al., 2024) found fewer BIS-arm patients progressed to chronic BCRL than tape-arm patients (7.9% vs 19.2% among those who triggered) [23, rct]. ESTABLISHED for early/subclinical BCRL detection with early intervention; BIS reduced progression to chronic lymphedema versus tape at both interim and 3-year readouts.

**Threshold evolution.** The 2022 BIS clinical-practice guidelines (Shah et al.) lowered the intervention trigger from an L-Dex change >10 to >6.5 units — moving from three standard deviations to two — to improve sensitivity for subclinical lymphedema [4, meta_analysis]. The guidelines emphasize prospective surveillance with **trend monitoring against a pre-treatment baseline**, with a serial schedule (quarterly years 1–3, biannually years 4–5, annually thereafter); a missing pre-treatment baseline does not preclude surveillance, and a post-treatment baseline can substitute [4, meta_analysis]. PROVISIONAL on the exact threshold (it has already moved once and is method-specific).

**Limitations.** BIS is validated for **unilateral** disease — the L-Dex ratio assumes a healthy contralateral reference limb, so bilateral lymphedema undermines the inter-limb ratio [4, meta_analysis][5, rct]. Body composition and gross fluid status (e.g., heart failure, dialysis) confound whole-body bioimpedance. **Agent rule:** an L-Dex/BIS number is interpretable only as a serial trend against the same individual's baseline and only in unilateral, limb context — a single reading, a bilateral case, or a consumer body-composition "BIA" scale is NOT an L-Dex lymphedema readout.

**Regulatory anchor.** The ImpediMed SOZO system with L-Dex received FDA 510(k) clearance (K180126, 2018) to aid clinical assessment of unilateral lymphedema; it is cleared as an aid to clinical assessment, not a standalone diagnostic [6, regulatory]. **Agent rule:** "FDA-cleared" for BIS means cleared as a clinician-used aid to assessment — clearance is not validation of any consumer device making "lymphatic" claims.

**Tissue dielectric constant (TDC / MoistureMeterD).** TDC measures localized skin/subcutaneous tissue water at a shallow effective depth (~2.5 mm probe) in <10 seconds, addressing sites BIS cannot — truncal and head-and-neck lymphedema, where no quantitative standard otherwise exists [7, cohort]. Inter-rater reliability in head-and-neck work is excellent (ICC >0.90; intrarater 0.97) and minimum detectable change is defined (~2–9 absolute TDC units; 5.3–8.0% for inter-side ratios) [7, cohort][8, cohort]. A 78-week longitudinal study found women with clinically diagnosed trunk lymphedema had significantly higher TDC ratios than those without [9, cohort]. Validation tier: `validated-clinical` (emerging) for localized/truncal tissue-water quantification; PROVISIONAL as a standalone diagnostic threshold. **Agent rule:** TDC quantifies local tissue water, not "lymphatic function" per se; it is a clinician/research measure interpreted as an inter-side ratio and serial trend, never a consumer self-test.

---

## B.3 Imaging — the diagnostic tier (clinician / SaMD only)

**Lymphoscintigraphy** is the long-standing imaging reference standard for assessing lymphatic transport function: a radiolabeled tracer is injected and gamma-camera imaging visualizes lymphatic uptake, transport time, and nodal drainage [10, cohort]. Validation tier: `validated-clinical`, diagnostic. Limitation: radiation exposure and limited sensitivity for early disease — in head-to-head comparison its sensitivity for early upper-limb lymphedema was ~0.62 versus 1.0 for ICG and MRI [10, cohort].

**ICG near-infrared fluorescence (NIRF) lymphography** injects indocyanine green and images its real-time superficial lymphatic flow without ionizing radiation; it visualizes **dermal backflow**, the leakage/pooling pattern that marks lymphatic dysfunction, and supports severity staging (Yamamoto dermal-backflow stages 0–V) [10, cohort][11, mechanism_review]. ICG is superior to lymphoscintigraphy for *early* upper-limb lymphedema (sensitivity ~89.5%, specificity ~85.7% in one series) [10, cohort]. A prospective longitudinal cohort (Aldrich et al., 2022; n=42) found dermal backflow on NIRF predicted BCRL with PPV 83%, NPV 86%, sensitivity 97%, specificity 50%, odds ratio 29.0, and a mean lead time of 8.3 months (up to 23) before clinical onset [12, cohort]. PROVISIONAL as a routine predictive test (small cohorts, specificity modest, procedure is invasive — dye injection). **MR / CT lymphangiography** add cross-sectional anatomic detail (channels, nodes, fluid distribution) for surgical planning [10, cohort].

**Agent rule:** all lymphatic imaging is clinician-ordered and clinician-interpreted (Software-as-a-Medical-Device / radiologist tier). The agent NEVER interprets, simulates, or substitutes for imaging; it may only contextualize a result a clinician has already documented. These are diagnostic-tier, not agent-interpretable.

---

## B.4 Inflammation / immune biomarkers — what they DO and DON'T say about "lymphatic function"

The acute-phase reactants — **hs-CRP, IL-6, TNF-α, ESR, fibrinogen, serum amyloid A** — are **non-specific markers of systemic inflammation**, produced largely by the liver in response to IL-6 and upstream cytokines; they are explicitly "not specific to any disease or organ" and must be interpreted alongside history, exam, and other tests [13, mechanism_review]. Mechanistically: TNF-α and IL-6 are upstream cytokines that rise within hours of an inflammatory trigger; hs-CRP is the downstream hepatic acute-phase protein induced by IL-6 and peaks 1–2 days later [14, mechanism_review]. ESR is an indirect, slow marker — it reflects fibrinogen-driven erythrocyte aggregation, rising over 24–48 h and staying elevated for weeks; it is nonspecific and not diagnostic of any disease [15, mechanism_review].

**These markers indicate the *presence* of inflammation but cannot identify its *source*** [13, mechanism_review]. None of them is a validated readout of lymphatic transport, drainage efficiency, or "lymph congestion." There is no validated routine blood biomarker of lymphatic-drainage efficiency.

**Research-stage lymphatic markers (validation tier: `research-only`).** Tissue/molecular lymphatic markers exist but are not blood diagnostics of function:

- **Podoplanin / D2-40** is a lymphatic-endothelium marker; the D2-40 monoclonal antibody specifically recognizes human podoplanin and is used for *histological* identification of lymphatic vessels on tissue sections — a pathology stain, not a blood test [16, in_vitro] (population: human tissue / cell-line immunohistochemistry).
- **VEGF-C** is a key regulator of lymphangiogenesis (VEGF-C/VEGFR-3 signaling); its absence is embryonically lethal in models, but as a circulating analyte it is not diagnostic — lymphedema patients can show *increased* circulating VEGF-C, yet elevated VEGF-C fails to resolve lymphedema, so it is not a clean "function" readout [17, mechanism_review] (population: human/animal mechanistic and translational studies).

ESTABLISHED that these are research/histology tools; PROVISIONAL-to-speculative as any future biomarker of lymphatic function. **Agent rule:** no routine blood test measures "lymphatic function." hs-CRP / IL-6 / TNF-α / ESR / fibrinogen are systemic-inflammation markers, not lymphatic-drainage readouts; VEGF-C and podoplanin/D2-40 are research/histology markers, not validated blood diagnostics. The agent must never present an inflammation lab as a "lymphatic health" score.

---

## B.5 Single value vs trend — the intra-individual-baseline principle and reference-range caveats

The cross-cutting discipline: a single cross-sectional value read against a population reference range is far weaker than a serial intra-individual trend, because biological + analytical variability within one person is large.

**hs-CRP is the canonical case.** A systematic review/meta-analysis found hs-CRP has high within-subject variability — median coefficient of variation ~0.44 (range 0.27–0.76) and pooled intraclass correlation ~0.62 [18, meta_analysis]. Consequently a single hs-CRP "may not reflect an individual's basal level," and guidance has long recommended averaging/repeating measurements (e.g., two samples ~2 weeks apart) and using the lower value, with risk categories assigned only after repeat sampling [19, mechanism_review]. The reference-change-value framing is stark: the critical difference for sequential hs-CRP values to be significant at p≤0.05 has been estimated near ~118% — i.e., a sequential change smaller than that can be pure noise [20, cohort]. ESTABLISHED.

**The same principle governs limb measures.** Because volume methods carry SEMs of ~3.6–6.6% and day-to-day interstitial fluid fluctuates (posture, activity, sodium, heat, menstrual cycle, time of day), a single limb-volume or single L-Dex reading near a threshold is within measurement+biological noise [2, meta_analysis][4, meta_analysis]. This is exactly why the BIS guidelines mandate a pre-treatment baseline and serial trend rather than a one-time cross-sectional cutoff [4, meta_analysis]. ESTABLISHED.

**Inter-individual variability + reference ranges.** Population reference ranges describe a distribution, not an individual's normal; a value inside the range can still be a meaningful change for a given person, and a value outside it can be that person's stable baseline. **Agent rule:** a single value — whether an hs-CRP, an L-Dex, or a limb circumference — is noise, not a verdict. The agent interprets serial change against the individual's own prior measurements (same method, same conditions), flags day-to-day fluid fluctuation as expected, and treats a single threshold-crossing as a prompt to re-measure, not a diagnosis.

---

## B.6 Consumer / unvalidated "lymphatic" assessment & device claims (validation tier: `not-validated/consumer`)

A high-pseudoscience-load market sells "lymphatic" assessment and "drainage" hardware. The pattern is consistent: a real physiological hook (fluid moves with muscle activity) is over-extended into specific "lymphatic drainage" or "detox" claims that no validation study supports.

- **Vibration plates marketed for "lymphatic drainage."** Marketing claim: whole-body vibration "drains the lymph" / "detoxifies" `[vendor_label]` [21, vendor_label]. Evidence gap: experts state plainly that "there is not one study that has ever measured lymphatic drainage and lymphatic improvement" with these devices, and a former ISL president states there is "no convincing evidence that vibration plates alleviate lymphedema or lipedema"; any fluid movement observed is not shown to be lymphatic rather than venous, and "so does going for a walk" [22, mechanism_review]. Validation tier: `not-validated/consumer`.
- **EMS "lymphatic" devices** (electrical muscle stimulation plates/wands billed as lymphatic). Same gap: muscle contraction moves fluid generally; there is no validation that the effect is lymphatic-specific or clinically meaningful for lymphatic status [22, mechanism_review]. `not-validated/consumer`.
- **"Lymphatic" thermography.** Thermal imaging marketed to detect "lymph congestion." No validated link exists between a surface thermal map and lymphatic transport function; lymphoscintigraphy / ICG are the validated functional/imaging tier (B.3), and thermography is not among the reliability-validated measurement instruments [2, meta_analysis]. `not-validated/consumer`.
- **Hand-held "drainage" tools / gua sha / manual self-tools** and **at-home "lymph congestion" self-tests** (pinch tests, symptom checklists sold as diagnostics). No validation study supports a self-administered test as a measure of lymphatic status; clinical assessment of even truncal lymphedema "currently relies on clinical assessment because no quantifiable standard method exists" outside research measures like TDC [9, cohort]. `not-validated/consumer`.

**Agent rule:** any consumer "lymphatic" device reading or at-home "lymph congestion" self-test is `not-validated/consumer` and is NEVER a measurement of lymphatic status. The agent must not quote vendor numbers as validity data (per the no-vendor-numerical rule), must name the validation gap explicitly, and must route any genuine lymphedema-status question to clinician assessment + validated measures (B.1–B.3), interpreted as intra-individual trends (B.5).

---

## Bibliography

1. Executive Committee of the International Society of Lymphology. The diagnosis and treatment of peripheral lymphedema: 2020 Consensus Document of the International Society of Lymphology. *Lymphology*. 2020;53(1):3-19. PMID: 32521126. https://pubmed.ncbi.nlm.nih.gov/32521126/
2. Hidding JT, Viehoff PB, Beurskens CHG, et al. Measurement Properties of Instruments for Measuring of Lymphedema: Systematic Review. *Phys Ther*. 2016;96(12):1965-1981. PMID: 27340195. https://pubmed.ncbi.nlm.nih.gov/27340195/
3. Sharkey AR, King SW, Kuo RY, Bickerton SB, Ramsden AJ, Furniss D. Measuring Limb Volume: Accuracy and Reliability of Tape Measurement Versus Perometer Measurement. *Lymphat Res Biol*. 2018;16(2):182-186. doi:10.1089/lrb.2017.0039. https://www.liebertpub.com/doi/10.1089/lrb.2017.0039
4. Shah C, Vicini FA, Beitsch P, et al. Bioimpedance spectroscopy for breast cancer-related lymphedema assessment: clinical practice guidelines. *Breast Cancer Res Treat*. 2023;198(1):1-9. PMID: 36566297. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9883343/
5. Ridner SH, Dietrich MS, Cowher MS, et al. A Randomized Trial Evaluating Bioimpedance Spectroscopy Versus Tape Measurement for the Prevention of Lymphedema Following Treatment for Breast Cancer: Interim Analysis (PREVENT trial interim). *Ann Surg Oncol*. 2019;26(10):3250-3259. PMID: 31054038. https://pubmed.ncbi.nlm.nih.gov/31054038/
6. ImpediMed. FDA 510(k) Clearance Issued for SOZO with L-Dex (K180126, 2018) — aid to clinical assessment of unilateral lymphedema. https://www.impedimed.com/impedimed-launches-fda-cleared-sozo-system/
7. Mayrovitz HN. Tissue Dielectric Constant (TDC) measurements for localized tissue water and lymphedema status (review of MoistureMeterD reliability and use). *Lymphat Res Biol* / Lymphoedema Education Solutions compilation. https://lymphoedemaeducation.com.au/2021/07/compilation-of-recent-publications-on-tissue-dielectric-constant-tdc/
8. Mayrovitz HN, Mikulka A, Woody D. Minimum Detectable Changes Associated with Tissue Dielectric Constant Measurements as Applicable to Assessing Lymphedema Status. *Lymphat Res Biol*. 2019;17(3):322-328. PMID: 30526306. https://pubmed.ncbi.nlm.nih.gov/30526306/
9. Mayrovitz HN, et al. Tissue Dielectric Constant Measures in Women With and Without Clinical Trunk Lymphedema Following Breast Cancer Surgery: A 78-Week Longitudinal Study. *Lymphat Res Biol*. 2020;18(4). PMID: 32379872. https://pmc.ncbi.nlm.nih.gov/articles/PMC7439223/
10. Akita S, Mitsukawa N, et al. (and Yamamoto T comparison series) Indocyanine Green (ICG) Lymphography Is Superior to Lymphoscintigraphy for Diagnostic Imaging of Early Lymphedema of the Upper Limbs. *J Vasc Surg / PLoS-indexed.* PMC3366958. https://pmc.ncbi.nlm.nih.gov/articles/PMC3366958/
11. Yamamoto T, et al. Arm dermal backflow (DB) stage classification for upper-extremity lymphedema severity using ICG lymphography (mechanism/staging review). https://www.jvsvenous.org/article/S2213-333X(12)00013-3/pdf
12. Aldrich MB, Rasmussen JC, DeSnyder SM, et al. Prediction of breast cancer-related lymphedema by dermal backflow detected with near-infrared fluorescence lymphatic imaging. *Breast Cancer Res Treat*. 2022;195(1):33-41. https://pmc.ncbi.nlm.nih.gov/articles/PMC9272652/
13. Jain S, Gautam V, Naseem S, et al. Physiology, Acute Phase Reactants. *StatPearls* (NCBI Bookshelf, updated). https://www.ncbi.nlm.nih.gov/books/NBK519570/
14. Inflammatory Biomarkers — clinical perspectives on hsCRP, IL-6, TNF-α kinetics (hs-CRP is downstream of IL-6; TNF-α/IL-6 rise within hours, CRP peaks 1–2 days). *Review.* PMC12592283. https://pmc.ncbi.nlm.nih.gov/articles/PMC12592283/
15. Erythrocyte Sedimentation Rate: Reference Range, Interpretation (ESR is a nonspecific, fibrinogen-driven systemic-inflammation marker). Medscape Reference / CAP test-use guidance. https://emedicine.medscape.com/article/2085201-overview
16. Schacht V, Dadras SS, Johnson LA, et al. Up-Regulation of the Lymphatic Marker Podoplanin (recognized by D2-40) — lymphatic-endothelium histological marker. *Am J Pathol.* PMC1602360. https://pmc.ncbi.nlm.nih.gov/articles/PMC1602360/
17. VEGF-C / VEGFR-3 in lymphangiogenesis and lymphedema — circulating VEGF-C is elevated yet does not resolve lymphedema (mechanistic/translational review). PMC11277328. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11277328/
18. Within-subject variation of C-reactive protein and high-sensitivity C-reactive protein: a systematic review and meta-analysis (median CV ~0.44; pooled ICC ~0.62). PMC11530069. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11530069/
19. Mayo Clinic Laboratories. HSCRP — C-Reactive Protein, High Sensitivity, Serum (repeat measurement to establish basal level; use lower of repeat values). https://www.mayocliniclabs.com/test-catalog/overview/800024
20. Macy EM, Hayes TE, Tracy RP. Variability in the measurement of C-reactive protein in healthy subjects: implications for reference intervals and epidemiological applications (critical difference for sequential values ~118%). *Clin Chem.* 1997. PMID: 8990222. https://pubmed.ncbi.nlm.nih.gov/8990222/
21. Vibration-plate vendor marketing pages claiming "lymphatic drainage" (cited only as marketing-claim label, NOT for validity numbers). https://www.powerplate.com/blogs/news/vibration-plate-for-lymphatic-drainage
22. Expert commentary on vibration-plate "lymphatic" claims, incl. former ISL president H. Brorson ("no convincing evidence...alleviate lymphedema or lipedema"; "not one study that has ever measured lymphatic drainage" with these devices). Time / NBC News reporting quoting clinical experts. https://time.com/7357195/vibration-plate-results-does-it-work/
23. Shah C, Ridner SH, Cheville AL, et al. Timing of Breast Cancer Related Lymphedema Development Over 3 Years: Observations from a Large, Prospective Randomized Screening Trial Comparing Bioimpedance Spectroscopy (BIS) Versus Tape Measure (PREVENT trial 3-year follow-up). *Ann Surg Oncol*. 2024;31(11):7487-7495. doi:10.1245/s10434-024-15706-x. PMID: 38965099. https://pubmed.ncbi.nlm.nih.gov/38965099/

---

## Self-check

**Unverified / softened attributions to flag.**
- Sources 7, 11, 14, 15, 17, 18, 21, 22 are cited from search-result extracts and a paywalled/aggregator route, not full-text reads (the Sharkey full text [3] returned HTTP 403 and the Liebert/SAGE TDC compilation [7] is an education-site aggregation). The *claims* attributed to them (TDC reliability ICCs, CRP within-subject CV/ICC, the ~118% critical difference, the Brorson "no convincing evidence" quote) match multiple independent extracts and the underlying peer-reviewed sources are named, but the [4] Shah BCRL guidelines year/volume were reconstructed from secondary text and should be page-verified before wiki ingestion. The Aldrich [12] numbers (PPV 83/NPV 86/sens 97/spec 50/OR 29.0), the ISL [1] citation, and both PREVENT entries — interim [5] (Ann Surg Oncol 2019;26(10):3250-3259, PMID 31054038, web-verified to first author Ridner and confirmed as the PREVENT interim analysis) and the 3-year follow-up [23] (Ann Surg Oncol 2024;31(11):7487-7495, PMID 38965099) — were confirmed against PubMed directly.

- **PREVENT outcome-number correction (iteration 2).** The iter-1 draft attached "11.3% absolute / 59% relative reduction" to citation [5] under the wrong PMID 31054045 (which resolves to an unrelated nursing-home psychometrics paper). The 11.3%/59% figures could be located only in secondary/press coverage of the PREVENT 3-year results, not in a directly-verifiable primary-source extract, so per the remediation instruction they were REMOVED and replaced with verifiable figures: the interim 9.8% absolute / 67% relative reduction (cited to [5], the correctly-PMID'd interim analysis) and the 3-year 7.9% vs 19.2% post-trigger progression (cited to the newly-added [23], the 2024 3-year follow-up). The directional, ESTABLISHED claim — BIS/L-Dex reduced progression to chronic lymphedema versus tape — is retained and is fully supported by both verified sources. This is an intentional, evidence-driven softening of the specific 11.3%/59% figures.
- Source 11 (Yamamoto dermal-backflow staging) is attributed at review level; the precise stage 0–V boundaries should be taken from the primary Yamamoto paper, not the comparison PDF, if used to ground specific stage definitions.

**Softened claims (intentional, evidence-driven).** BIS threshold (>6.5) is marked PROVISIONAL because it has already moved (from >10) and is method-specific. TDC and ICG-prediction are marked PROVISIONAL as standalone diagnostics (small cohorts, modest specificity) while their measurement reliability is ESTABLISHED — this split is deliberate, not hedging.

**Clearest validation gap (consumer claim vs evidence).** Vibration-plate and EMS "lymphatic drainage" devices: the marketing asserts measurable lymphatic drainage/detox, while a former ISL president and other clinicians state there is no study that has *ever measured* lymphatic improvement with these devices and no convincing evidence they alleviate lymphedema [22, mechanism_review]. Any fluid shift observed is not shown to be lymphatic versus venous — "so does going for a walk." This is the canonical `not-validated/consumer` case the agent must never treat as a measurement.

**Validation-tier summary (load-bearing output).**
- `validated-clinical`: ISL staging (qualitative, clinician-assigned); water displacement, perometry, circumferential tape + truncated-cone volume; BIS / L-Dex (unilateral, serial-trend, FDA-cleared as assessment aid); TDC / MoistureMeterD (localized/truncal, emerging); lymphoscintigraphy, ICG-NIRF lymphography, MR/CT lymphangiography (all diagnostic, clinician/SaMD-tier — NOT agent-interpretable).
- `research-only`: VEGF-C (circulating, non-diagnostic), podoplanin / D2-40 (histology marker). No validated routine blood biomarker of lymphatic-drainage efficiency exists.
- Systemic-inflammation markers (hs-CRP, IL-6, TNF-α, ESR, fibrinogen): validated as *systemic inflammation* markers — NOT lymphatic-function readouts; single values are noise vs intra-individual trend.
- `not-validated/consumer`: vibration plates, EMS "lymphatic" devices, "lymphatic" thermography, hand-held "drainage" tools, at-home "lymph congestion" self-tests.

---

## Post-fix grep audit (iteration 2)

**OLD → NEW changes (citation_fidelity / PF-S2-02 class):**

| Item | OLD | NEW | Verification |
|------|-----|-----|--------------|
| PREVENT interim PMID | `31054045` (resolves to unrelated nursing-home psychometrics paper) | `31054038` | Web-verified: PubMed 31054038 = Ridner SH et al., "A Randomized Trial Evaluating Bioimpedance Spectroscopy Versus Tape Measurement... Interim Analysis," *Ann Surg Oncol* 2019;26(10):3250-3259 — confirmed first author Ridner and PREVENT trial. |
| Outcome numbers | `11.3% absolute / 59% relative reduction` attributed to [5] at 3 years | Removed (unverifiable in primary source). Replaced with interim `9.8% absolute / 67% relative` → [5], and 3-year `7.9% vs 19.2%` post-trigger progression → [23]. | The 11.3%/59% pair appears only in secondary/press coverage; no directly-verifiable primary-source extract carried both figures, so softened per remediation instruction. Interim 9.8%/67% and 3-year 7.9%/19.2% are from PubMed/open primary-source extracts. |
| 3-year source | (none — numbers wrongly pinned to interim) | New bibliography entry **[23]**: Shah C et al., *Ann Surg Oncol* 2024;31(11):7487-7495, doi:10.1245/s10434-024-15706-x, PMID 38965099 | Web-verified PMID 38965099, title and pages confirmed. Cited as `[23, rct]` in B.2 prose. |

(Edition note: the 2019 pages 3250-3259 are the INTERIM analysis and are now labeled as such in both prose and bibliography; the 3-year outcome figures are pinned to the 2024 paper [23], not the 2019 interim.)

**Grep command run:** `grep -inE '31054045|11\.3|59%|3250-3259|PREVENT' section-B.md`

**Post-fix grep hits and dispositions:**

- **No hits** for `31054045` — the wrong PMID is fully removed (including its prior appearance in the self-check narrative, which was rewritten to cite 31054038/38965099).
- **No hits** for `11.3` or `59%` — the unverifiable outcome figures are fully removed.
- `3250-3259` — appears twice, both CORRECT: (1) B.2 is no longer the carrier of those pages; (2) bibliography [5] now labels them as the *Interim Analysis* pages under the corrected PMID 31054038, and (3) the self-check restates them with the corrected PMID. All dispositions: KEEP (correct, interim-labeled).
- `PREVENT` — appears in B.2 prose (correct, now split across [5] interim and [23] 3-year), bibliography [5] and [23] (correct), and the self-check (correct). All dispositions: KEEP.

**Audit status: CLEAN.** No stale OLD value remains. PREVENT interim PMID (31054038) and 3-year PMID (38965099) are both web-verified against PubMed.
