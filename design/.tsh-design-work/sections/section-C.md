# Section C: Measurement & Interferences

## Assay Design and Generations

Modern TSH measurement relies on third-generation immunometric sandwich assays. The operating principle is straightforward: two antibodies directed at distinct TSH epitopes bracket the analyte — one capture antibody immobilizes the complex on a solid phase, and one signal antibody generates a detectable readout. Because signal is proportional to analyte concentration, sandwich formats produce high dynamic range, and the use of two high-affinity monoclonal or polyclonal antibodies confers the specificity needed for a hormone with complex glycoform heterogeneity.

The evolution of TSH assays across three generations was organized around a single quantitative criterion: **functional sensitivity**, defined as the lowest TSH concentration measured with a between-run coefficient of variation (CV) ≤20%, established over a 6–8 week period [1, regulatory]. This metric is more stringent than the analytical limit of detection because it accounts for the day-to-day imprecision that governs clinical use. Nicoloff and Spencer formalized the generational framework, with each successive generation representing a tenfold improvement in functional sensitivity [2, mechanism_review]:

- **First generation** (radioimmunoassays, ~1960s–early 1980s): functional sensitivity ~1–2 mIU/L; adequate only for detecting overt hypothyroidism.
- **Second generation** (immunoradiometric assays, IRMA; ~1986): functional sensitivity ~0.1 mIU/L; first assays capable of distinguishing suppressed from normal TSH.
- **Third generation** (non-isotopic immunometric assays, ~1990s–present): functional sensitivity ≤0.01–0.02 mIU/L; the current standard worldwide [1, regulatory].

Third-generation assays are predominantly **chemiluminescent** (immunochemiluminometric assay, ICMA) or **electrochemiluminescent** (ECLIA, as in Roche Elecsys platforms). The Roche ECLIA system uses a ruthenium-based luminophore triggered by electrochemical voltage; Siemens ADVIA Centaur uses an acridinium ester. Abbott ARCHITECT and Beckman Access platforms use direct chemiluminescence. The functional sensitivity of third-generation ICMAs in routine use is typically 0.005–0.02 mIU/L [3, mechanism_review].

---

## Interferences: Falsely LOW TSH

### Biotin (High-Dose Supplements)

The most clinically important and now prevalent source of falsely low TSH is **exogenous biotin** taken at pharmacological doses (≥5 mg/day for cosmetic or neurological applications; doses up to 300 mg/day are used in multiple sclerosis protocols). Biotin is a small molecule that binds streptavidin with femtomolar affinity — exactly the binding pair exploited by biotin-streptavidin immunoassay platforms (Roche Elecsys; estimated >50% of global immunoassay reagents use this system) [4, mechanism_review].

The mechanism: excess circulating biotin competes with the biotinylated capture antibody for streptavidin binding sites on the solid phase. In a **sandwich** assay (TSH), this competition reduces the capture efficiency of the antibody-TSH complex, shrinking the signal and producing a **falsely low TSH**. In a **competitive** assay (fT4, fT3), the same competition displaces label from binding sites and produces a **falsely elevated** result. The combined pattern — suppressed TSH with elevated fT4/fT3 — exactly mimics Graves' disease [5, cohort]. A 63-year-old woman taking 300 mg/day biotin for multiple sclerosis presented with this biochemical picture; normalization within three days of stopping biotin confirmed assay interference [5, cohort]. Biotin concentrations of ≥20–50 µg/L have been shown to generate interference on Roche platforms, and pharmacological doses routinely exceed this threshold [5, cohort].

**Practical guidance:** Patients should stop biotin supplements for a minimum of 48–72 hours before thyroid testing. The interference is platform-specific; Abbott, Siemens, and Beckman platforms using direct (non-streptavidin) chemiluminescence are substantially less affected.

### Anti-Streptavidin Antibodies

A minority of patients develop **endogenous anti-streptavidin antibodies** — immunoglobulins that bind the streptavidin layer directly. Their effect mirrors exogenous biotin: they block biotinylated antibody binding and produce falsely low TSH and falsely high fT4/fT3. These antibodies persist for 18–24 months or longer, and unlike biotin, cannot be removed by supplement cessation [4, mechanism_review]. Detection requires testing on a non-streptavidin platform.

---

## Interferences: Falsely HIGH TSH

### Heterophile and Human Anti-Animal Antibodies (HAAAs)

**Heterophile antibodies** — broadly reactive immunoglobulins against animal protein epitopes, often stimulated by prior exposure to animal proteins (via pet contact, therapeutic monoclonal antibodies, or dietary exposure) — cross-bridge the capture and signal antibodies in a sandwich TSH assay, generating a falsely elevated signal even in the absence of TSH antigen. Human anti-mouse antibodies (HAMA) are the most common HAAA subtype; because many immunoassay antibodies are murine, HAMA are particularly disruptive to TSH measurement [4, mechanism_review]. Estimated interference rate is 0.05–6% depending on assay, with TSH-specific rates near 0.4%. The effect is almost always falsely **elevated** TSH.

A striking example: a single post-thyroidectomy patient showed TSH values of 5.52 µIU/mL on Siemens, 0.54 on Abbott, 0.12 on Roche, and <0.015 on Beckman — reflecting highly platform-specific HAAA affinity [6, cohort]. Heterophilic antibody blocker pretreatment collapsed all values toward zero, confirming interference.

**Rheumatoid factor** (anti-IgG IgM) can similarly bridge detection antibodies, and its prevalence in autoimmune thyroid disease patients creates a clinical trap. Detection strategies include serial dilution testing (non-linearity across dilutions), heterophilic blocking tubes (HBT), and parallel testing on a second platform.

### Macro-TSH

**Macro-TSH** refers to high-molecular-weight TSH circulating as an immune complex — TSH bound to anti-TSH IgG autoantibodies. Prevalence is approximately 0.6–1.6% of patients with persistently elevated TSH who are otherwise asymptomatic [4, mechanism_review]. Because the complex is TSH-antigen-positive but biologically inert, the TSH assay reads it as elevated TSH while fT4 and fT3 remain normal. This pattern exactly mimics subclinical hypothyroidism and has led to inappropriate levothyroxine initiation in documented cases. Detection by polyethylene glycol (PEG) precipitation — which preferentially precipitates large immune complexes — or gel filtration chromatography separates macro-TSH from authentic free TSH.

### Anti-Ruthenium Antibodies

Endogenous antibodies targeting the ruthenium chelate used as the electrochemiluminescent signal molecule in Roche ECLIA platforms can produce **variable interference** — most commonly falsely elevated TSH, but occasionally affecting fT4 and fT3 independently. Prevalence is <0.1–0.24% [4, mechanism_review]. These are detected by switching to a non-ruthenium platform.

---

## Non-Thyroidal Illness (Sick Euthyroid / NTIS)

In patients with acute or severe systemic illness, TSH follows a characteristic biphasic pattern that is not reflective of intrinsic thyroid dysfunction. During the acute phase of critical illness, inflammatory cytokines, elevated cortisol, and dopamine all suppress TSH at the level of the thyrotroph and hypothalamus; serum TSH may fall below 0.1 mIU/L in up to 3% of acutely ill hospitalized patients, even in the absence of true hyperthyroidism [4, mechanism_review]. The parallel fall in T3 (conversion to reverse-T3 replaces the deiodination pathway) and T4 completes the "sick euthyroid" pattern.

During **recovery**, TSH may rebound transiently above the reference range — sometimes into a range suggesting subclinical or overt hypothyroidism — before returning to normal. Measuring TSH during the rebound phase of an acute illness without knowledge of the preceding course has led to unnecessary levothyroxine initiation. The clinical rule: **interpret TSH only in the context of the acute illness trajectory**, and confirm any abnormal TSH with a repeat measurement after recovery unless there is compelling reason to act immediately.

---

## Diurnal Variation and Sampling Timing

TSH secretion follows a robust circadian rhythm driven by the suprachiasmatic nucleus. The nocturnal surge peaks between 02:00–04:00 h; the daytime nadir falls between 07:00–14:00 h. The mean diurnal amplitude is approximately 140% of the nadir value — a peak roughly 2.4-fold higher than the trough in some studies [7, cohort]. Superimposed on this are approximately 13 pulsatile TSH bursts per 24 hours (mean pulse mass ~0.90 mU/L, duration ~20 minutes) [7, cohort].

In healthy individuals with TSH near the population midpoint, the diurnal swing does not typically produce diagnostic misclassification. However, for values near the upper or lower reference limits — the zones where subclinical hypo- or hyperthyroidism is considered — sampling time can shift a borderline result into or out of the normal range. Most reference intervals are derived from morning fasting samples; TSH values drawn in the late afternoon should be interpreted with this in mind.

---

## Drug Effects on TSH (Cross-Reference: Determinants Section)

Several drug classes suppress TSH through central mechanisms and can produce a biochemical picture of central hypothyroidism when the cause is not recognized [8, mechanism_review]:

- **Dopamine and dopamine agonists** suppress TSH via D2 receptor activation on thyrotrophs, inhibiting both TRH signaling and Tshb transcription. Infused dopamine at ICU doses (≥2 µg/kg/min) reliably suppresses TSH. This compounds the NTIS-related suppression in critically ill patients and requires the same interpretive caution.
- **Glucocorticoids** at high doses suppress hypothalamic pro-TRH mRNA and blunt TSH secretion transiently; chronic physiologic replacement doses do not cause significant TSH suppression.
- **Somatostatin analogues** and **rexinoids** (bexarotene) can cause clinically significant central hypothyroidism [8, mechanism_review].
- **Amiodarone** is a special case: its high iodine content inhibits thyroid hormone synthesis (Wolff-Chaikoff effect) and may cause true hypo- or hyperthyroidism, not only a laboratory artifact.

---

## TSH–fT4 Discordance Patterns

The log-linear inverse relationship between TSH and fT4 is load-bearing for interpretation. When this relationship is violated, specific diagnoses must be considered (see Determinants section for the full matrix):

| Pattern | Likely cause |
|---------|-------------|
| High TSH, low fT4 | Primary hypothyroidism (the canonical pattern) |
| Low TSH, high fT4 | Primary hyperthyroidism or exogenous T4 excess |
| Low TSH, low/normal fT4 | Central hypothyroidism; NTIS acute phase; dopamine/glucocorticoid suppression |
| Normal/high TSH, high fT4 | Assay interference (biotin, anti-Ru); TSH-secreting pituitary adenoma; thyroid hormone resistance |
| High TSH, normal fT4 | Subclinical hypothyroidism; recovery phase NTIS; macro-TSH; heterophile antibody interference |

Central hypothyroidism deserves particular note: in this condition the log-linear relationship is dissolved because the pituitary produces biologically less potent TSH isoforms; serum fT4 — not TSH — becomes the monitoring parameter for levothyroxine adequacy.

---

## Assay Standardization and Harmonization

TSH immunoassays are not harmonized across analytical platforms — no commutable certified reference material is in routine use for TSH, meaning assay-specific biases cannot be eliminated by simple recalibration to a common standard in the way that is possible for many small-molecule analytes. The WHO International Standard for TSH (e.g. IS 80/558 and its successors) serves as a reference preparation for biological potency assignment, but method-specific differences persist because commercial assays use different antibody pairs, signal chemistries, and calibration approaches. Consequently, TSH results and their associated reference intervals are method-dependent and are not freely interchangeable across laboratories or platforms; a value of 3.8 mIU/L on one system does not carry the same clinical meaning as 3.8 mIU/L on another [9, mechanism_review]. The IFCC Committee for Standardization of Thyroid Function Tests (C-STFT) has documented between-assay biases of up to ~39% across major platforms and continues to pursue harmonization through patient-sample-based calibration traceability, though full commutability-based standardization remains an unresolved goal [9, mechanism_review].

---

## Bibliography

1. Van Uytfanghe K et al. Thyroid Tests — Clinical and Laboratory Status [ATA Statement]. Thyroid. 2023. DOI: THY-2023-0169. [regulatory]

2. Nicoloff JT, Spencer CA. The use and misuse of the sensitive thyrotropin assays. J Clin Endocrinol Metab. 1990;71(3):553–558. DOI: 10.1210/jcem-71-3-553. PMID: 2203796. [mechanism_review]

3. Wilkinson E, Rae PW, Thomson KJ, Toft AD, Spencer CA, Beckett GJ. Chemiluminescent third-generation assay (Amerlite TSH-30) of thyroid-stimulating hormone in serum or plasma assessed. Clin Chem. 1993;39(10):2166–2173. PMID: 8403404. [mechanism_review]

4. Favresse J, Burlacu MC, Maiter D, Gruson D. Interferences with thyroid function immunoassays: clinical implications and detection algorithm. Endocr Rev. 2018;39(5):830–850. DOI: 10.1210/er.2018-00119. PMID: 29982406. [mechanism_review]

5. Elston MS, Sehgal S, Du Toit S, Yarndley T, Conaglen JV. Factitious Graves' disease due to biotin immunoassay interference — a case and review of the literature. J Clin Endocrinol Metab. 2016;101(9):3251–3255. DOI: 10.1210/jc.2016-1971. PMID: 27362288. [cohort]

6. Cheng X, Guo X, Chai X, Hu Y, Lian X, Zhang G. Heterophilic antibody interference with TSH measurement on different immunoassay platforms. Clin Chim Acta. 2021;513:120–124. PMID: 33285118. [cohort]

7. van der Spoel E, Roelfsema F, van Heemst D. Within-person variation in serum thyrotropin concentrations: main sources, potential underlying biological mechanisms, and clinical implications. Front Endocrinol. 2021;12:619568. PMID: 33716972. [cohort]

8. Haugen BR. Drugs that suppress TSH or cause central hypothyroidism. Best Pract Res Clin Endocrinol Metab. 2009;23(6):793–800. PMID: 19942154. [mechanism_review]

9. Thienpont LM, Van Uytfanghe K, Beastall G, et al.; IFCC Working Group on Standardization of Thyroid Function Tests. Report of the IFCC Working Group for Standardization of Thyroid Function Tests; part 1: thyroid-stimulating hormone. Clin Chem. 2010;56(6):902–911. PMID: 20395624. DOI: 10.1373/clinchem.2009.140178. [mechanism_review]
