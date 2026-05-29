# Section B — Consumer Wearable Sleep/Recovery Tracking: Validity, Limitations, Correct Interpretation

Scope: evidence base grounding how a `sleep-coach` agent must interpret consumer-wearable sleep and recovery metrics — Oura ring primarily (purchase pending; data does not yet exist), plus WHOOP, Apple Watch, Fitbit. The agent must (a) function correctly with NO wearable data, and (b) once data exists, apply the validity caveats below. The throughline of the literature: **two-state sleep/wake epoch detection is reasonably validated; auto-staging and composite "readiness/recovery" scores are weakly validated or unvalidated and must not be treated as clinical measures.**

---

## B.1 Validation Against Polysomnography (PSG) and ECG

PSG is the gold standard for sleep architecture; ECG (specifically RR-interval RMSSD) is the gold standard for HRV. Consumer devices are validated against these.

### The dominant, reproducible finding: high sleep sensitivity, poor wake specificity

Across independent validations the same pattern recurs: devices detect *sleep* epochs well but detect *wake* epochs poorly, so they systematically overestimate total sleep time (TST) and underestimate wake.

- In a seven-device controlled-lab validation, sleep-epoch **sensitivity was uniformly high (all ≥0.93)**, while **wake-detection specificity ranged only 0.18–0.54** (Fitbit Alta HR best at 0.54; Garmin devices worst at 0.18–0.19); most devices overestimated TST, with Garmin biases ~44–47 min [1, cohort]. The same study found sleep-*stage* assessment "inconsistent," with per-stage sensitivity only ~30–70% [1, cohort].
- A prospective multicenter validation of 11 consumer trackers reproduced the pattern: **all devices detected >90% of sleep epochs (sensitivity), but specificity for wake was 29–52%** [2, cohort].
- This high-sensitivity/low-specificity signature is the consensus structural limitation of consumer sleep tracking, not a quirk of one device [1, cohort][2, cohort].

**Agent implication:** a wearable "you slept 7h45m" is biased upward; reported wake-after-sleep-onset is biased downward. The agent must treat TST as an over-estimate and never reassure a user that fragmented sleep is fine because the device "only" logged a few wake minutes.

### Oura ring specifically

- **Gen1 vs PSG (de Zambotti 2019, n=41 adolescents/young adults):** sleep-detection **sensitivity 96%**, **wake specificity 48%**; stage agreement **light 65%, deep 51%, REM 61%**; the ring underestimated deep sleep ~20 min and overestimated REM ~17 min; TST not statistically different from PSG [3, cohort]. This is the canonical, honest early result: good at "asleep vs awake," mediocre-to-poor at staging.
- **Gen3 with the OSSA 2.0 algorithm vs multi-night ambulatory PSG (Svensson 2024, n=96, 421,045 epochs):** sleep-wake **2-stage accuracy 94% (accelerometer-only) to 96% (full model with autonomic + circadian features)**; **4-stage accuracy 57% (accelerometer-only) rising to 79% (full model)**; staging **Cohen's κ ≈ 0.65** (PABAK 0.83), with per-stage accuracy ~75.5% light, 88.6% deep, 90.6% REM [4, cohort] *(these per-stage and κ figures are vendor-reported in a manufacturer-linked study and have not been independently re-verified against the full text — see Self-check; a published critical Comment on this paper exists [4b])*. Generation-over-generation, adding PPG-derived autonomic and circadian features lifted 4-stage accuracy from 57% to 79% — real improvement on the vendor's own data, but still well short of inter-scorer PSG agreement (~83% / κ~0.76 between trained human scorers), and κ≈0.65 places staging at only "substantial" not "near-perfect" agreement [4, cohort].

**Agent implication:** Oura's staging improved markedly Gen1→Gen3, but a single night's "deep sleep 38 min" is the weakest output and must carry the widest uncertainty band. The validated layer is sleep/wake; the staging layer is advisory only.

### Cross-device staging accuracy

Independent head-to-head validations of six wrist devices for stage scoring against PSG confirm that **epoch-by-epoch staging remains the weakest function across the category**, with substantial misclassification especially of N1/light and wake [5, cohort]. npj Digital Medicine's reliability evaluation reaches the same conclusion: staging reliability is device- and stage-dependent and should not be read as clinical sleep architecture [6, cohort].

---

## B.2 HRV from PPG vs ECG; RHR; and the Nature of "Readiness/Recovery" Scores

### PPG HRV vs ECG RMSSD

Consumer rings/watches derive HRV from **photoplethysmography (PPG)** — optical pulse-interval timing — not the electrical RR intervals ECG measures. Under ideal conditions (still, sleeping, sinus rhythm) agreement for time-domain HRV is reasonable; it degrades sharply with motion, arrhythmia, and low signal quality.

- **WHOOP 2.0 vs ECG during slow-wave sleep (n=6):** HR agreement near-perfect (ICC 1.00, bias ≤0.39 bpm). For HRV, **RMSSD bias 1.33–4.90 ms with limits of agreement ±11.26–15.96 ms (ICC 0.98–0.99)**; for ln RMSSD the **bias ±LOA approached or exceeded the smallest worthwhile change (1.5–6.5%) and coefficient of variation (3–13%)** — i.e., the device's measurement error is on the same order as the physiological change one would try to detect [7, cohort]. Stage-matched (during PSG-defined SWS) the ln RMSSD LOA widened to ±22.31% [7, cohort].
- Independent Oura nocturnal HR/HRV analyses against ECG report strong resting agreement but the same dependence on artifact-free signal [8, cohort].
- **Where it breaks down:** HRV error from PPG rises **14–51% above resting baseline during activity/motion** [9, cohort]; arrhythmia (notably atrial fibrillation) inflates beat-to-beat variability and corrupts pulse-interval estimates [10, cohort]; low heart rate and poor perfusion degrade peak detection. PPG HRV is therefore only trustworthy at rest/asleep in sinus rhythm.

**Agent implication:** nocturnal resting HRV (ln RMSSD) from a ring is the most defensible recovery signal, but its night-to-night measurement error is comparable to the change being interpreted. The agent must not act on small single-night HRV swings, and must withhold interpretation entirely for users with known arrhythmia.

### Resting heart rate (RHR)

RHR is the best-validated cardiac metric on these devices — agreement with ECG is typically near-perfect at rest (ICC ~1.00 in the WHOOP data [7, cohort]; comparable for Oura [8, cohort]). RHR is a reasonable trend input.

### "Readiness," "Recovery," and "Sleep Score" composites

These are **proprietary, vendor-defined indices, not validated clinical constructs.** Oura "Readiness," WHOOP "Recovery," and Fitbit/Apple sleep scores blend RHR, HRV, sleep duration/staging, body temperature, and prior-day activity through closed algorithms that change between firmware versions. No peer-reviewed validation establishes that any of these composite scores predicts a clinical outcome, and the AASM position is that consumer technologies broadly lack validation and FDA clearance (B.5) [11, regulatory]. Because they inherit the staging errors of B.1 and the HRV noise of this section, **the composite is necessarily noisier than its weakest validated input.**

**Agent implication:** the agent must treat readiness/recovery scores as motivational summaries, never as physiological measurements. It must never say "your recovery is 34%, you are under-recovered" as if reporting a measured biomarker. It may, at most, note a *sustained downward trend* in the underlying validated inputs (RHR up, HRV down over a rolling window).

---

## B.3 Night-to-Night Variability: Single-Night Metrics Are Noise

Even with a perfect device, single-night sleep and HRV values are dominated by night-to-night biological variability, so trend interpretation — not point readings — is the only defensible approach.

- HRV reproducibility is **parameter- and sleep-stage-dependent**: HR and HF power (in slow-wave sleep) reproduce well, but **LF power and LF/HF reproduce poorly across nights** [12, cohort].
- Short-term stability exists for some measures (HF-HRV, LF:HF cross-night ICC >0.79, correlations >0.87 in good sleepers) but not others — "for some measures one night is enough," implying for most it is not [13, cohort].
- HRV is **non-stationary across the night**; aggregating across sleep-stage epochs obscures transient effects and inflates both Type-I and Type-II error [14, cohort].
- Sleep-disordered-breathing signals show large night-to-night variance (cyclic-variation-of-HR coefficient of variation 66±35%; events missed on 62% of nights, ≥1 night missed in 88% of patients) — a single night can entirely miss a real condition [15, cohort].

**Agent implication:** the agent must interpret on **rolling averages (e.g., 7-day) and personal baselines**, never single nights. It must use **intra-individual baselining** (the user's own trailing distribution) rather than population norms — population "normal HRV" ranges span an order of magnitude and are meaningless for an individual. A one-night dip is expected variance, not a signal.

---

## B.4 Orthosomnia: Wearable Data Can Worsen Sleep and Anxiety

"Orthosomnia" — a perfectionistic preoccupation with achieving device-defined "perfect" sleep — is a documented iatrogenic harm of consumer sleep tracking.

- The term was coined in a **JCSM case series (Baron 2017)** describing patients seeking treatment for self-diagnosed sleep problems driven by tracker data, whose preoccupation with the data itself worsened sleep and anxiety; clinically, tracker data sometimes contradicted validated assessment yet patients trusted the device over the clinician [16, open_label].
- Orthosomnia is now measurable at population scale: a cross-sectional general-population study established measurable prevalence [17, cohort], and a validated instrument (Bergen Orthosomnia Scale) now exists [18, cohort], confirming it is a real, generalizable phenomenon rather than anecdote.

**Agent implication — load-bearing for agent safety design:** an agent that over-interprets consumer data is a direct orthosomnia risk vector. The agent must (1) de-emphasize nightly scores, (2) actively normalize variability, (3) never frame a number as a target to "beat," (4) avoid implying a single bad night caused daytime symptoms, and (5) detect and gently counter anxious over-monitoring rather than feed it. This is the strongest argument for the agent operating well WITHOUT wearable data and treating any data it later gets as low-authority trend context.

---

## B.5 Professional-Body Positions and Regulatory Status

### AASM

The American Academy of Sleep Medicine's position statement is explicit: **"Given the lack of validation and FDA clearance, consumer sleep technologies cannot be utilized for the diagnosis and/or treatment of sleep disorders at this time"** [11, regulatory]. CST data "should be considered in the context of a comprehensive sleep evaluation and should not replace validated diagnostic instruments," though it may enhance the patient–clinician interaction [11, regulatory]. A subsequent AASM update reiterated the need for validation, raw-data access, and FDA oversight [19, regulatory].

### What these devices are NOT cleared to do

- Oura and WHOOP are marketed primarily as **general-wellness devices**, not as cleared diagnostic Software-as-a-Medical-Device. They are **not cleared to diagnose sleep apnea, insomnia, or any sleep disorder**, and their sleep-staging outputs are not regulated medical measurements [11, regulatory].
- The boundary is actively enforced: in **July 2025 the FDA issued a warning letter to WHOOP** stating that its "Blood Pressure Insights" feature is a medical device under §201(h) of the FD&C Act being marketed without clearance — a direct demonstration that consumer-wearable health outputs crossing into diagnosis require, and lack, FDA authorization [20, regulatory].

**Agent implication:** the agent must position itself consistent with AASM — wearable data is supplementary trend context within a broader picture, never diagnostic. It must explicitly refuse to diagnose sleep apnea/insomnia from device data and must route suspected disorders (loud snoring, witnessed apneas, excessive daytime sleepiness, chronic insomnia) to a clinician/sleep study. This holds identically in the current no-data state.

---

## Design Synthesis (carry into agent spec)

1. **Validated vs not:** trust sleep/wake epoch detection and resting RHR as trend inputs; treat auto-staging (deep/REM minutes) as advisory; treat readiness/recovery/sleep scores as motivational, not measurements.
2. **Trend, not point:** interpret on rolling averages against the user's own baseline; single nights are noise.
3. **TST is biased up, wake biased down:** never reassure from device-reported low wake.
4. **HRV only at rest/sinus rhythm:** suppress HRV interpretation under motion or known arrhythmia; measurement error ≈ the change of interest.
5. **Orthosomnia guardrail:** de-emphasize scores, normalize variability, never set numeric "targets to beat."
6. **AASM-aligned non-diagnostic stance:** refuse diagnosis; route red-flag symptoms to clinicians. Holds with or without data.

---

## Bibliography

[1] Chinoy ED, et al. 2021 — *Sleep* — controlled-lab validation cohort (7 consumer devices vs PSG) — n=34 — DOI:10.1093/sleep/zsaa291 — https://academic.oup.com/sleep/article/44/5/zsaa291/6055610

[2] Lee T, et al. 2023 — *JMIR mHealth and uHealth* — prospective multicenter validation cohort (11 wearable/nearable/airable trackers vs PSG) — PMID:37917155 — https://pubmed.ncbi.nlm.nih.gov/37917155/

[3] de Zambotti M, et al. 2019 — *Behavioral Sleep Medicine* — validation cohort (Oura Gen1 vs PSG) — n=41 — PMID:28323455 / DOI:10.1080/15402002.2017.1300587 — https://pubmed.ncbi.nlm.nih.gov/28323455/

[4] Svensson T, et al. 2024 — *Sleep Medicine* — validation cohort (Oura Gen3, OSSA 2.0 vs multi-night ambulatory PSG) — n=96, 421,045 epochs — PMID:38382312 / DOI:10.1016/j.sleep.2024.01.020 — https://www.sciencedirect.com/science/article/pii/S1389945724000200 [MANUFACTURER-LINKED: Oura-affiliated authorship; flag as vendor-sourced validation. Per-stage/κ figures are vendor-reported, not independently re-verified — see Self-check.]

[4b] Lolli L, et al. 2024 — *Sleep Medicine* — published Comment on [4] (peer critique of the Svensson/OSSA 2.0 validation) — DOI:10.1016/j.sleep.2024.03.013 — https://doi.org/10.1016/j.sleep.2024.03.013

[5] Schyvens [first-author surname confirmed via Crossref; initials unconfirmed — not PubMed-indexed], et al. 2025 — *SLEEP Advances* — validation cohort (6 wrist devices, stage scoring vs PSG) — DOI:10.1093/sleepadvances/zpaf021 — https://academic.oup.com/sleepadvances/article/6/2/zpaf021/8090472

[6] Birrer [first-author surname confirmed via Crossref; initials unconfirmed — not PubMed-indexed], et al. 2024 — *npj Digital Medicine* — reliability evaluation cohort (wearable sleep staging) — DOI:10.1038/s41746-024-01016-9 — https://www.nature.com/articles/s41746-024-01016-9

[7] Bellenger CR, et al. 2021 — *Sensors (MDPI)* — validation cohort (WHOOP 2.0 PPG vs ECG, SWS) — n=6 — PMID:34065516 / DOI:10.3390/s21103571 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8160717/ [MDPI open-access: lower-trust tier; very small n=6]

[8] Cao R, et al. 2022 — *Journal of Medical Internet Research* — validation cohort (Oura nocturnal HR/HRV vs ECG, time & frequency domains) — PMC8808342 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8808342/

[9] Rehman RZU, et al. 2024 — *Sensors (Basel)* [MDPI: lower-trust open-access] — validation study (PPG vs ECG HRV across activity states; error +14–51% above rest) — PMC11548599 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11548599/

[10] Bashar SK, et al. 2019 — *Scientific Reports (Nature)* — cohort (wrist-PPG AF detection, motion-artifact handling) — PMID:31636284 / DOI:10.1038/s41598-019-49092-2 — https://www.nature.com/articles/s41598-019-49092-2

[11] Khosla S, et al. 2018 — *JCSM* — AASM position statement (regulatory/professional-body) — DOI:10.5664/jcsm.7128 — https://pmc.ncbi.nlm.nih.gov/articles/PMC5940440/

[12] Herzig D, et al. 2017 — *Frontiers in Physiology* — cohort (HRV reproducibility by parameter & sleep stage) — PMID:29367845 — https://pubmed.ncbi.nlm.nih.gov/29367845/

[13] Israel B, et al. 2012 — *Sleep* — cohort (sleep & HRV night-to-night stability, good sleepers vs insomnia) — PMC3413806 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3413806/

[14] Eddie D, et al. 2022 — *Sleep Medicine* — cohort (HRV non-stationarity across sleep-stage epochs) — PMC8923916 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8923916/

[15] Hayano J, et al. 2022 — *Annals of Noninvasive Electrocardiology* — cohort (sleep-apnea CVHR night-to-night variability, long-term ECG) — PMC8916582 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8916582/

[16] Baron KG, Abbott S, Jao N, Manalo N, Mullen R. 2017 — *JCSM* — case series / open-label (orthosomnia) — DOI:10.5664/jcsm.6472 — https://jcsm.aasm.org/doi/10.5664/jcsm.6472

[17] Jahrami H, et al. 2024 — *Brain Sciences (MDPI)* [lower-trust open-access] — cross-sectional cohort (orthosomnia general-population prevalence) — PMID:39595886 / PMC11592250 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11592250/

[18] Guldbrandsen BV, et al. 2025 — *Frontiers in Sleep* — instrument-validation cohort (Bergen Orthosomnia Scale, BOS) — PMID:41425191 — https://pubmed.ncbi.nlm.nih.gov/41425191/

[19] Schutte-Rodin S, et al. 2021 — *JCSM* — regulatory/professional-body update (AASM evaluation of consumer & clinical sleep technologies) — DOI:10.5664/jcsm.9580 — https://jcsm.aasm.org/doi/10.5664/jcsm.9580

[20] U.S. FDA 2025 — *FDA Warning Letter to WHOOP, Inc. (#709755, 07/14/2025)* — regulatory (Blood Pressure Insights marketed as unauthorized device under §201(h)) — https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-07142025

---

## Self-check

**Claims not fully groundable to a whitelisted primary at the level of detail stated:**
- [4] Citation now resolved to **Svensson T, et al. 2024, Sleep Medicine, PMID 38382312 / DOI 10.1016/j.sleep.2024.01.020** (the earlier "Ghorbani" attribution and placeholder DOI "…01.xxx" were wrong and have been removed). Gen3/OSSA 2.0 per-stage accuracy (75.5/88.6/90.6%) and κ (0.65) were retrieved via search-engine summary + ScienceDirect abstract; the full text is paywalled (HTTP 403). These specific per-stage and κ figures remain **vendor-reported and not independently re-verified against the full PDF** — flagged inline in B.1 — and should be confirmed before wiki ingestion. **This source is Oura-affiliated** (manufacturer-linked) and drew a published peer Comment ([4b] Lolli L, et al. 2024, Sleep Medicine, DOI 10.1016/j.sleep.2024.03.013), reinforcing its contested status. Independent replications [5][6] report staging as the category's weakest function, consistent with but less rosy than the vendor framing. Where manufacturer claims diverge from independent validation, defer to [1][2][5][6].
- [7] WHOOP/Sensors is **MDPI (lower-trust open-access) and n=6** — directionally consistent with [8] but underpowered; cite only as illustrative of PPG-HRV error magnitude, not definitive.
- First-author attributions were re-resolved against NCBI E-utilities (PubMed/PMC esummary) and Crossref DOI lookups (iter-2). Confirmed surname+initials: [2] Lee T, [4] Svensson T, [8] Cao R, [9] Rehman RZU, [10] Bashar SK, [12] Herzig D, [13] Israel B, [14] Eddie D, [15] Hayano J, [17] Jahrami H, [18] Guldbrandsen BV, [19] Schutte-Rodin S (plus pre-confirmed [1] Chinoy ED, [3] de Zambotti M, [7] Bellenger CR, [11] Khosla S, [16] Baron KG). Two corrections of journal-of-record surfaced during this pass: [2] is *JMIR mHealth and uHealth* (not generic *J Med Internet Res* multicenter), and [17] is *Brain Sciences* (MDPI) (not *JCSM* as previously listed). [5] Schyvens and [6] Birrer are confirmed by Crossref surname but are NOT PubMed-indexed, so initials remain unconfirmed and are marked as such inline rather than invented.
- The de Zambotti [3] journal is *Behavioral Sleep Medicine* (de Zambotti's broader body of work appears across SLEEP/Sensors); PMID 28323455 is the anchor.

**Where manufacturer claims diverge from independent validation:** Oura's own Gen3 validation [4] reports 4-stage accuracy up to 79% and "90%+" REM/deep accuracy; independent multi-device work [1][2][5] consistently finds staging "inconsistent" with per-stage sensitivity 30–70% and wake specificity often <0.5. The agent design must weight the **independent** finding (staging is unreliable) over the **manufacturer** finding.

**No-data caveat:** all of B is interpretive guidance for data that does not yet exist for this user. Sections B.3 (trend-not-point), B.4 (orthosomnia), and B.5 (non-diagnostic) are fully actionable in the current no-wearable state and constrain agent behavior independent of any device purchase.

---

## Post-fix grep audit (iter-2)

Authority for author/journal/DOI corrections: NCBI E-utilities (PubMed/PMC `esummary`) and Crossref DOI lookups, run during this iteration.

**FINDING 1 — placeholder DOI on [4]:**

| OLD | NEW |
|-----|-----|
| `[4] Ghorbani S / Oura validation team … DOI:10.1016/j.sleep.2024.01.xxx` | `[4] Svensson T, et al. 2024 … PMID:38382312 / DOI:10.1016/j.sleep.2024.01.020` |
| body: `(de Zambotti 2019 …)` line followed by Gen3 figures with no provenance flag | body: Gen3 figures now flagged `(vendor-reported … not independently re-verified … see Self-check; a published critical Comment exists [4b])`; resolvable DOI inserted |
| (none) | `[4b] Lolli L, et al. 2024 — Sleep Medicine — Comment on [4] — DOI:10.1016/j.sleep.2024.03.013` added |

Grep checks (whole file):
- `grep -inE 'sleep\.2024\.01\.xxx'` → **0 hits** (placeholder removed).
- `grep -inE 'Ghorbani'` → **1 hit, line 157** — legitimate: Self-check sentence documenting the corrected attribution ("the earlier 'Ghorbani' attribution … were wrong and have been removed"). Retained intentionally as a correction record.
- `grep -inE '\.xxx'` → **1 hit, line 157** — legitimate: quoted "…01.xxx" inside the Self-check correction note, not a live citation.
- `grep -inE '^\[4b\]'` → **1 hit, line 118** — Lolli Comment present.

**FINDING 2 — inferred/placeholder author strings:**

| Ref | OLD author string | NEW (verified) | Source of verification |
|-----|-------------------|----------------|------------------------|
| [2] | `Chee NIYN / Kim H` (+ journal `J Med Internet Res`) | `Lee T` (+ journal `JMIR mHealth and uHealth`) | PubMed esummary PMID 37917155 |
| [5] | `Stone JD / six-device validation team` | `Schyvens` [initials unconfirmed, not PubMed-indexed] | Crossref DOI 10.1093/sleepadvances/zpaf021 |
| [6] | `Birrer V` | `Birrer` [initials unconfirmed, not PubMed-indexed] | Crossref DOI 10.1038/s41746-024-01016-9 |
| [8] | `Cao R / Oura HR-HRV ECG analysis team` (+ `PMC (JMIR-family)`) | `Cao R` (+ `Journal of Medical Internet Research`) | PMC esummary PMC8808342 |
| [9] | `PPG-HRV activity-error analysis` (+ tag `mechanism_review`) | `Rehman RZU` (+ `Sensors (Basel)` MDPI, tag corrected to `cohort`) | PMC esummary PMC11548599 |
| [10] | `Wrist-PPG atrial-fibrillation detection study` | `Bashar SK` | PubMed esummary PMID 31636284 |
| [12] | `Reproducibility-of-HRV team` (+ `PubMed`, yr 2018) | `Herzig D` (+ `Frontiers in Physiology`, yr 2017) | PubMed esummary PMID 29367845 |
| [13] | `Israel B / short-term-stability team` (+ `PMC`) | `Israel B` (+ `Sleep`) | PMC esummary PMC3413806 |
| [14] | `Aggregating-HRV-across-epochs team` (+ `PMC`) | `Eddie D` (+ `Sleep Medicine`) | PMC esummary PMC8923916 |
| [15] | `Cyclic-variation-of-HR night-to-night team` (+ `PMC`) | `Hayano J` (+ `Annals of Noninvasive Electrocardiology`) | PMC esummary PMC8916582 |
| [17] | `Orthosomnia-prevalence team` (+ journal `JCSM (PMC)`) | `Jahrami H` (+ `Brain Sciences` MDPI) | PubMed esummary PMID 39595886 |
| [18] | `Bergen Orthosomnia Scale team` (+ `PubMed`) | `Guldbrandsen BV` (+ `Frontiers in Sleep`) | PubMed esummary PMID 41425191 |
| [19] | `AASM CST-evaluation update` | `Schutte-Rodin S` | PubMed esummary PMID 34314344 |

Grep checks (whole file):
- `grep -inE '(validation team|analysis team|Reproducibility-of-HRV team|short-term-stability team|Aggregating-HRV-across-epochs team|night-to-night team|prevalence team|Orthosomnia Scale team|CST-evaluation update)'` → **0 hits** (all "team" placeholders removed).
- `grep -inE 'Chee NIYN|Kim H'` → **0 hits**.
- `grep -inE 'Stone JD'` → **0 hits**.
- `grep -inE '— \*PMC\*|— \*PubMed\*|JMIR-family|JCSM \(PMC\)'` → **0 hits** (generic journal placeholders removed).
- `grep -inE 'mechanism_review'` → **0 hits** ([9] tag corrected to `cohort`; no other claim used that tag).

**Type-tag integrity:** every claim retains exactly one type-tag. Tag census after fixes: [1]×3, [2]×2, [3], [4]×2, [5], [6], [7]×3, [8]×2, [9], [10], [11]×4, [12], [13], [14], [15], [16], [17], [18], [19], [20] — all `cohort` except [11]/[19]/[20] `regulatory` and [16] `open_label`. The validated-vs-unvalidated distinction, orthosomnia (B.4), AASM/FDA (B.5) content is unchanged.

**Honesty note:** [5] Schyvens and [6] Birrer surnames are Crossref-confirmed but the journals are not PubMed-indexed, so initials could not be verified from a masthead and are deliberately omitted rather than invented (per "never invent a surname/initial"). No surname in this bibliography is fabricated; every NEW attribution traces to a cited PMID/PMCID/DOI lookup.
