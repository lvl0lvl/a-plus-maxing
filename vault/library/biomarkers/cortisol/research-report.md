---
title: "Cortisol: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/cortisol/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.cortisol-design-work
provenance_slug: labs-specialist
source_count: 17
---

# Cortisol: Canonical Research Report

## Summary

Cortisol is the primary endogenous glucocorticoid in humans, synthesized in the zona fasciculata of the adrenal cortex and acting on virtually every organ system to regulate metabolism, immune function, cardiovascular tone, and the stress response. Its secretion is governed by the hypothalamic-pituitary-adrenal (HPA) axis and is organized across multiple timescales — a prominent circadian rhythm, an ultradian pulsatile pattern, and acute stress-driven surges — making timed sampling a prerequisite for any meaningful interpretation [1, mechanism_review].

**Circadian dependence is the defining pre-analytical fact about cortisol.** Morning serum cortisol (drawn at 08:00–09:00) typically ranges from approximately 5–25 µg/dL (~138–690 nmol/L), with values near the upper end in the 30–45 minutes after waking (the cortisol awakening response). By midnight the same individual will be near 1–5 µg/dL (28–138 nmol/L). A single cortisol measurement without a precise collection time is nearly uninterpretable. Convert between conventional and SI units by multiplying by 27.6: 1 µg/dL = 27.6 nmol/L [6, regulatory].

**Dynamic testing dominates clinical cortisol diagnosis.** A single random or even morning cortisol rarely settles the clinical question. The workhorses are: the 1 mg overnight dexamethasone suppression test (DST; Cushing's screen: abnormal if post-dex cortisol ≥1.8 µg/dL [≥50 nmol/L]); late-night salivary cortisol (LNSC; loss of midnight nadir in Cushing's); 24-hour urinary free cortisol (UFC; integrated daily output); and the cosyntropin (ACTH, 250 µg) stimulation test (adrenal insufficiency: peak <18 µg/dL [<500 nmol/L] is abnormal on older immunoassays, equivalent to ~15 µg/dL [~411 nmol/L] on LC-MS/MS) [7, regulatory; 8, regulatory; 9, cohort].

Immunoassay remains the predominant measurement platform but carries important analytical liabilities: prednisolone cross-reacts at 148% and methylprednisolone at 249% on the Roche Elecsys (falsely elevating results); total serum cortisol misrepresents free cortisol whenever corticosteroid-binding globulin (CBG) is abnormal (elevated in estrogen/OCP/pregnancy → falsely high total; reduced in critical illness/nephrotic syndrome/cirrhosis → falsely low total). Salivary and urinary assays directly measure the free (biologically active) fraction and are unaffected by CBG changes [10, mechanism_review; 11, mechanism_review; 12, mechanism_review].

Clinical anchors: sustained cortisol excess (Cushing's syndrome) produces central obesity, proximal myopathy, violaceous striae, hypertension, and metabolic dysregulation; adrenal insufficiency (AI) carries risk of adrenal crisis (life-threatening acute decompensation requiring immediate parenteral hydrocortisone). "Adrenal fatigue" — the claim that subclinical cortisol deficiency causes non-specific symptoms despite normal testing — is not a recognized endocrine diagnosis and is not supported by systematic review evidence [16, mechanism_review].

---

## Physiology & The HPA Axis

### Synthesis and the HPA Cascade

Cortisol is a steroid hormone derived from cholesterol through a multi-step enzymatic pathway in the **zona fasciculata** of the adrenal cortex. The rate-limiting step — transport of cholesterol from the outer to the inner mitochondrial membrane — is executed by the steroidogenic acute regulatory protein (StAR), after which CYP11A1 cleaves the cholesterol side-chain to form pregnenolone. Subsequent enzymes (CYP17A1, CYP11B1) complete cortisol biosynthesis [1, mechanism_review].

Cortisol secretion is driven by the **HPA axis**: a cascade beginning in the hypothalamic paraventricular nucleus (PVN), where parvocellular neurons synthesize and release **corticotropin-releasing hormone (CRH)** into the hypophyseal portal circulation. CRH reaches the anterior pituitary corticotrope cells and stimulates cleavage of pro-opiomelanocortin (POMC) to yield **adrenocorticotropic hormone (ACTH)**. ACTH then circulates to the adrenal cortex, where it binds the melanocortin-2 receptor (MC2R) on zona fasciculata cells, acutely upregulating StAR expression and driving cortisol release [1, mechanism_review].

**Arginine vasopressin (AVP)**, co-released from PVN neurons alongside CRH, potentiates ACTH secretion synergistically via a separate intracellular pathway (phospholipase C / protein kinase C) that amplifies the CRH-evoked adenylate cyclase signal — making AVP a significant modulator of the stress-activated HPA response [1, mechanism_review].

**Negative feedback** is the core regulatory brake on the axis. Cortisol — once elevated — binds glucocorticoid receptors in the hypothalamus and anterior pituitary, suppressing CRH and ACTH release and preventing runaway activation. Membrane-associated glucocorticoid receptors at the PVN mediate a rapid, non-genomic feedback arm within minutes; classical nuclear receptor feedback operates over hours. This dual-speed feedback maintains homeostasis while permitting the acute stress response [1, mechanism_review].

### Circadian Rhythm and the Cortisol Awakening Response

Cortisol secretion follows a powerful **circadian rhythm** driven by the suprachiasmatic nucleus (SCN), with output entrained to the light-dark cycle and tightly coupled to the sleep-wake transition. Plasma cortisol is at its **midnight nadir** — typically 1–5 µg/dL (28–138 nmol/L) — before rising sharply in the final hours of sleep, peaking in the early morning at approximately 10–20 µg/dL (276–552 nmol/L) in healthy adults [2, mechanism_review].

A distinct, superimposed phenomenon upon waking is the **cortisol awakening response (CAR)**: a rapid surge of 50–156% in free salivary cortisol occurring within the **first 30–45 minutes after morning awakening**. The CAR is separable from the underlying circadian rise and is understood to reflect a dual-control system — a circadian-primed component and an awakening-entrained trigger. Functionally, the CAR is hypothesized to prepare the organism for the metabolic and cognitive demands of the active phase [2, mechanism_review].

This rhythm has a critical practical implication: **a single cortisol measurement is uninterpretable without knowing the time of sampling**. The same individual will show plasma cortisol values differing by an order of magnitude between their morning peak and midnight nadir. Standard clinical morning cortisol is typically drawn 08:00–09:00, where a value below approximately 3 µg/dL (83 nmol/L) raises concern for adrenal insufficiency and above ~18–20 µg/dL (497–552 nmol/L) is generally reassuring for an intact axis [2, mechanism_review].

### Ultradian (Pulsatile) Secretion

Superimposed on the circadian envelope is an **ultradian pulsatile secretion pattern**: discrete bursts of cortisol release occurring approximately every 60–120 minutes throughout the 24-hour cycle, yielding roughly 12–18 discernible pulses per day. This pulsatility is intrinsic to the HPA axis — arising from the oscillatory dynamics of CRH and ACTH pulses — and is not merely noise. Glucocorticoid-responsive genes respond differently to pulsatile versus continuous glucocorticoid exposure; pulsatile delivery maintains glucocorticoid receptor sensitivity and supports stress responsiveness in ways that constant-level exposure does not [3, mechanism_review]. The CAR itself represents the first and largest ultradian pulse of the active phase.

### Plasma Binding: Total vs. Free Cortisol

In circulation, cortisol is predominantly protein-bound:

- **~75–80% bound to corticosteroid-binding globulin (CBG/transcortin)** — a hepatically synthesized high-affinity binding protein
- **~10–15% bound to albumin** (lower affinity, higher capacity)
- **~5–10% circulates as free (unbound) cortisol**

Only the free fraction is biologically active under the **free-hormone hypothesis** — able to diffuse across cell membranes and engage intracellular glucocorticoid receptors [4, mechanism_review].

CBG is not merely a passive carrier. Its binding affinity is temperature-sensitive (free cortisol roughly doubles for every 2°C rise in temperature within the 37–42°C range) and is reduced by neutrophil elastase cleavage at sites of inflammation — potentially quadrupling local free cortisol at inflamed tissues and creating a targeted glucocorticoid delivery mechanism [4, mechanism_review]. CBG levels are also influenced by estrogen (elevated in pregnancy/OCP use, raising total cortisol) and liver disease (reduced CBG, lowering total cortisol). Accordingly, **total plasma cortisol can mislead when CBG is abnormal** — the free or salivary cortisol fraction then becomes the more informative metric.

### Physiological Actions

Once free cortisol enters target cells and binds the glucocorticoid receptor (GR), it acts as a master metabolic and immunomodulatory signal:

- **Metabolic / gluconeogenic:** Cortisol promotes hepatic gluconeogenesis (stimulating key enzymes including PEPCK and G6Pase), increases amino acid mobilization from muscle, and stimulates lipolysis — net effect: elevating blood glucose and providing substrates for energy during stress.
- **Anti-inflammatory / immunomodulatory:** Cortisol suppresses NF-κB and AP-1 transcription factor activity, reduces synthesis of pro-inflammatory cytokines (IL-1β, IL-6, TNF-α), and stabilizes mast cells. At physiological concentrations it restrains excessive immune activation; at pharmacological doses it is broadly immunosuppressive.
- **Cardiovascular / permissive:** Cortisol is required for normal vascular responsiveness to catecholamines. It upregulates adrenergic receptor expression on vascular smooth muscle and potentiates vasopressor sensitivity — underpinning the hemodynamic compromise seen in acute adrenal insufficiency (Addisonian crisis).
- **CNS effects:** Glucocorticoid receptors are densely expressed in the hippocampus, prefrontal cortex, and amygdala. Acute cortisol modulates memory consolidation; chronic excess impairs hippocampal neurogenesis and memory. It also influences mood, arousal, and appetite [1, mechanism_review].

### Tissue-Level Regulation: 11β-HSD1 and 11β-HSD2

An additional regulatory layer operates at the tissue level via **11β-hydroxysteroid dehydrogenase** enzymes that interconvert cortisol and its inactive metabolite **cortisone**:

- **11β-HSD1** (widely expressed in liver, adipose tissue, brain, muscle): Acts predominantly as a **reductase**, regenerating active cortisol from inert cortisone. This amplifies intracellular glucocorticoid signaling in tissues beyond what circulating cortisol levels alone would predict. Upregulation of 11β-HSD1 in visceral adipose tissue in obesity is a recognized contributor to metabolic complications [5, mechanism_review].
- **11β-HSD2** (expressed in the kidney, colon, placenta): Acts as a **dehydrogenase**, rapidly inactivating cortisol to cortisone. This enzymatic barrier protects aldosterone-selective mineralocorticoid receptors in the distal nephron from illicit occupancy by cortisol (which otherwise has equal mineralocorticoid receptor affinity) — preventing sodium retention and hypertension [5, mechanism_review].

The 11β-HSD system means that circulating cortisol levels are an imperfect window into actual intracellular glucocorticoid exposure in any given tissue.

---

## Reference Ranges, Units & Dynamic Testing

### Why a Single Cortisol Value Is Rarely Enough

Cortisol follows a steep circadian rhythm: peak production occurs in the hour before waking (~6–8 AM), then declines through the day to reach its nadir around midnight [6, regulatory]. A single random cortisol reading without knowing the time of collection — or the assay used — is difficult to interpret. The corollary is clinically important: **timed and dynamic tests** (dexamethasone suppression, ACTH stimulation, late-night salivary sampling, 24-hour urinary collection) are the workhorses of cortisol diagnosis. A morning serum value provides only a rough screen; pathological patterns of secretion almost always require provocation or suppression testing to confirm.

### Reference Ranges and Unit Conversion

Serum cortisol is reported in **µg/dL** (conventional) or **nmol/L** (SI). Convert between them by multiplying by **27.6** (µg/dL → nmol/L) or dividing by 27.6 (nmol/L → µg/dL).

#### Commonly Cited Reference Ranges (immunoassay, adult)

| Time Point | µg/dL | nmol/L |
|---|---|---|
| Morning (6–8 AM) | ~5–25 | ~138–690 |
| Afternoon (~4 PM) | ~3–10 | ~83–276 |
| Late night / midnight | very low | typically <50–80 |

These ranges are **assay-dependent** and should not be applied across platforms [6, regulatory]. Immunoassays using polyclonal antibodies typically yield higher values than liquid chromatography–tandem mass spectrometry (LC-MS/MS), which is increasingly considered the reference standard. A value reported as 18 µg/dL on an older Roche Elecsys Cortisol I immunoassay corresponds to roughly 14.5 µg/dL (≈400 nmol/L) by LC-MS/MS [9, cohort]. Each laboratory should publish its own assay-validated reference interval; the ranges above are approximate population estimates and starting points, not universal cutoffs.

#### Quick Conversion Reference

| µg/dL | nmol/L |
|---|---|
| 1.8 | 50 |
| 3 | 83 |
| 5 | 138 |
| 10 | 276 |
| 15 | 414 |
| 18 | 497 |
| 20 | 552 |
| 25 | 690 |

### Dynamic Tests

#### 1. Overnight 1 mg Dexamethasone Suppression Test (DST) — Cushing's Screen

**Principle:** Dexamethasone (1 mg oral, taken at 11 PM) suppresses ACTH release; in healthy individuals, 8 AM cortisol the next morning will fall below the threshold. Loss of this suppression — i.e., cortisol remaining elevated — is the hallmark of autonomous cortisol production.

**Threshold (Endocrine Society):** A post-dexamethasone 8 AM serum cortisol **≥1.8 µg/dL (≥50 nmol/L)** constitutes a positive (abnormal) screen [7, regulatory]. Suppression to below this cutoff is normal and argues against Cushing's syndrome. The guideline adopted this lower cutoff (in place of the older 5 µg/dL / 138 nmol/L threshold) to achieve >95% sensitivity, accepting a specificity of approximately 80% — appropriate for a screening test where false negatives carry greater clinical cost than false positives [7, regulatory].

**Caveats:** Conditions that accelerate dexamethasone metabolism (phenytoin, rifampin, alcohol) or interfere with cortisol immunoassays can produce false positives. Depression, obesity, and chronic stress also blunt suppression. A positive screen requires confirmation with a second test.

#### 2. Late-Night Salivary Cortisol — Loss of the Midnight Nadir

**Principle:** Because free cortisol diffuses into saliva, a midnight salivary sample is a non-invasive proxy for serum-free cortisol at the physiological nadir. In Cushing's syndrome, the normal midnight trough is lost.

**Threshold:** The Endocrine Society guideline cites values above approximately **145 ng/dL (≈4 nmol/L)** as consistent with hypercortisolism, though published upper limits of normal range from 3.2 to 4 nmol/L across laboratories [7, regulatory]. As with all cortisol assays, the reference interval is **assay-specific** — each lab using its own validated cutoff.

**Clinical advantage:** It captures the **free (unbound) fraction** of cortisol, is unaffected by changes in CBG (e.g., with oral contraceptives), and can be collected at home. Sensitivity and specificity exceed 92% in well-conducted validation studies [7, regulatory].

#### 3. 24-Hour Urinary Free Cortisol (UFC) — Integrated Daily Output

**Principle:** The kidneys excrete the unbound fraction of circulating cortisol; a 24-hour collection integrates total free-cortisol output across the day and night, smoothing episodic variability.

**Interpretation:** Values above the upper limit of the laboratory's reference range are abnormal. The Endocrine Society emphasizes that **cut-off levels are method-specific**: immunoassay-based UFC measurements include some cortisol metabolites and run higher than LC-MS/MS, which measures cortisol alone [7, regulatory]. A single elevated UFC warrants confirmation; values more than fourfold above the upper reference limit are more specific for Cushing's syndrome. Incomplete collections (creatinine-adjusted volume check) are a common source of error.

**Important distinction:** UFC measures the **free** (biologically active) fraction, not total plasma cortisol. Changes in CBG do not affect it, unlike serum total cortisol.

#### 4. ACTH (Cosyntropin 250 µg) Stimulation Test — Adrenal Insufficiency

**Principle:** Synthetic ACTH (cosyntropin, 250 µg IV or IM) is given and serum cortisol is measured at 30 and 60 minutes. A normal adrenal cortex should respond with a brisk rise. Blunted response indicates adrenal insufficiency (primary or, if prolonged, secondary due to ACTH deprivation).

**Threshold (Endocrine Society, standard-dose test):** A peak cortisol **<500 nmol/L (<18 µg/dL)** at 30 or 60 minutes is consistent with adrenal insufficiency [8, regulatory]. Conversely, a peak **≥18–20 µg/dL (≥497–552 nmol/L)** makes primary adrenal insufficiency unlikely.

**Assay-dependence of the cutoff:** This 18 µg/dL threshold was established with older polyclonal immunoassays. With LC-MS/MS or newer monoclonal-antibody assays, the equivalent cutoff is approximately **411–414 nmol/L (~14.9–15 µg/dL)** at 30 minutes [9, cohort]. Applying the 18 µg/dL benchmark to LC-MS/MS results overdiagnoses adrenal insufficiency; assay-specific normative data should guide interpretation [8, regulatory; 9, cohort].

#### 5. Morning Serum Cortisol — Preliminary Screen for Adrenal Insufficiency

Before ordering dynamic testing, morning cortisol provides a rapid orientation [8, regulatory]:

| Morning Cortisol (8 AM) | Interpretation |
|---|---|
| **<3–5 µg/dL (<83–138 nmol/L)** | Suggestive of AI — proceed to confirmatory testing |
| **5–15 µg/dL (138–414 nmol/L)** | Gray zone — ACTH stimulation test required |
| **>15–18 µg/dL (>414–497 nmol/L)** | AI unlikely, but does not exclude partial secondary AI |

A morning cortisol below 140 nmol/L (5 µg/dL) paired with an elevated plasma ACTH supports primary adrenal insufficiency [8, regulatory]. A value above approximately 480 nmol/L (17 µg/dL) has been cited in some studies as sufficient to exclude the diagnosis, though the exact upper threshold remains debated given assay variability.

### Key Takeaways on Ranges and Dynamic Testing

1. **Context is everything.** Serum cortisol ranges from ~5 µg/dL (138 nmol/L) in the morning to near-zero at midnight in healthy individuals; a value is only meaningful relative to when it was drawn.
2. **Dynamic tests dominate.** The overnight DST (Cushing's screen) and cosyntropin stimulation test (AI screen) are the standard diagnostic workhorses; a random cortisol rarely answers the clinical question.
3. **The 1.8 µg/dL (50 nmol/L) DST cutoff** is the Endocrine Society's recommended threshold for Cushing's screening — substantially lower than the historical 5 µg/dL to preserve sensitivity.
4. **Assay platform shifts the cutoff.** LC-MS/MS returns lower cortisol values than immunoassay; the 18 µg/dL ACTH-stimulation threshold established with older assays corresponds to roughly 15 µg/dL (411–414 nmol/L) on LC-MS/MS. Always use assay-specific validated cutoffs.
5. **Salivary and urinary assays measure free cortisol.** They are unaffected by CBG changes and complement serum total cortisol for functional assessment.

---

## Measurement & Interferences

### Serum Total Cortisol: Immunoassay vs LC-MS/MS

Serum cortisol in routine clinical practice is almost universally measured by automated direct immunoassay (chemiluminescent, electrochemiluminescent, or enzyme-linked platforms). These assays quantify the sum of free and protein-bound cortisol without a prior extraction step, making them high-throughput and cost-effective. Their central limitation is analytical specificity: because cortisol antibodies are raised against a structurally complex steroid, they recognize other steroids that share similar ring architecture.

Liquid chromatography–tandem mass spectrometry (LC-MS/MS) separates cortisol from co-eluting steroids by both retention time and parent-ion/fragment-ion pair, then quantifies it against a stable-isotope internal standard. It is more accurate at low concentrations, is the recommended method for dynamic tests where interfering steroids accumulate (metyrapone challenge, adrenocortical hyperplasia), and is the only method capable of simultaneously identifying exogenous glucocorticoids in the same run [10, mechanism_review; 11, mechanism_review].

**Cross-reactivity magnitude.** On the Roche Elecsys platform — the most thoroughly characterized — cross-reactivity values reported in the package insert and independently confirmed are:

| Compound | Cross-reactivity (Roche Elecsys) | Clinical likelihood |
|---|---|---|
| 6-Methylprednisolone | 249% | High (therapeutic concentrations up to ~1,000 ng/mL) |
| Prednisolone | 148% | High (up to ~400 ng/mL in transplant patients) |
| 11-Deoxycortisol | Clinically significant | High during metyrapone challenge |
| 21-Deoxycortisol | Clinically significant | High in 21-hydroxylase deficiency |
| Cortisone | 0.3–31.1% depending on assay | Ubiquitous endogenous interferent |

[10, mechanism_review]

Prednisolone's cross-reactivity of 148% means that patients receiving therapeutic prednisolone can generate immunoassay cortisol readings elevated by the prednisolone itself — making a falsely suppressed or falsely normal result impossible to interpret without switching to LC-MS/MS. Methylprednisolone at 249% is clinically the most dangerous interferent in this class. By contrast, dexamethasone and betamethasone do not generally cross-react with cortisol immunoassays, which is why dexamethasone is used in suppression tests without LC-MS/MS interference — although confirmation of dexamethasone non-reactivity should be verified for any specific platform [11, mechanism_review].

Topical and inhaled corticosteroids are a subtler source of falsely elevated readings; prednisolone contamination of a salivary cortisol sample taken shortly after an oral dose has been documented as a clinically significant confounder for late-night salivary cortisol (LNSC) testing [10, mechanism_review].

### The CBG Problem (Load-Bearing Caveat)

Approximately 70–80% of circulating cortisol is bound to corticosteroid-binding globulin (CBG), 10–15% to albumin, and only 2–5% is free and biologically active. CBG is a high-affinity, low-capacity hepatic glycoprotein (SERPIN family); its concentration sets a ceiling on how much total cortisol the assay can detect before the free fraction begins to rise steeply. This means **total serum cortisol is an unreliable index of adrenal function whenever CBG is abnormal** [11, mechanism_review; 12, mechanism_review].

**States that raise CBG → falsely high total cortisol:**
- Oral contraceptives containing estrogen: CBG rises 2–3-fold above baseline. Total cortisol may reach levels indistinguishable from Cushing's syndrome while free cortisol remains normal. Women on combined oral contraceptives should ideally discontinue them for approximately 6 weeks before cortisol dynamic testing, or salivary/free cortisol should be used instead [12, mechanism_review].
- Pregnancy: CBG rises 2–3-fold. Both total and free cortisol are genuinely elevated in late pregnancy (HPA-axis resetting), but in the first trimester the total cortisol rise often exceeds the free-cortisol rise due to CBG induction alone.
- Estrogen-replacement therapy: same mechanism.

**States that lower CBG → falsely low total cortisol:**
- Critical illness / sepsis: CBG falls rapidly as an acute-phase response and due to cleavage by leukocyte elastase. A patient in septic shock may have a "subnormal" total cortisol reading despite an intact, appropriately activated adrenal axis. This is the central methodological challenge in diagnosing critical illness-related corticosteroid insufficiency (CIRCI) and is why some guidelines caution against relying on total serum cortisol alone in the ICU [12, mechanism_review].
- Nephrotic syndrome: hepatic CBG synthesis is outpaced by urinary protein losses. Total cortisol can fall below the lower end of the reference interval while free cortisol is normal or elevated.
- Cirrhosis: impaired hepatic synthesis reduces both CBG and albumin. Total cortisol underestimates the free fraction; ACTH-stimulation test cutoffs derived from healthy populations cannot be applied without modification [12, mechanism_review].

In all of these states, **salivary cortisol, urinary free cortisol (UFC), or directly measured serum free cortisol (by equilibrium dialysis or ultrafiltration + LC-MS/MS) should replace total cortisol** as the index of adrenal function. Calculated free cortisol using the Coolens equation (requires total cortisol + CBG measured on the same sample) correlates well with dialysis-derived free cortisol (r ≈ 0.98 in some datasets) and is a practical alternative when direct free-cortisol assays are unavailable [11, mechanism_review].

### Salivary Cortisol

Cortisol crosses the salivary gland epithelium by passive diffusion; only the free (unbound) fraction passes, so salivary cortisol directly reflects serum free cortisol and is independent of CBG changes. This makes it the specimen of choice for:

- **Late-night salivary cortisol (LNSC):** The loss of nadir suppression at 11 PM–midnight is a hallmark of autonomous hypercortisolism; salivary collection is non-invasive, can be performed at home, and captures the physiologically important circadian nadir without hospitalization. Endocrine Society guidelines list LNSC as a first-line Cushing's screening test [7, regulatory].
- **Cortisol awakening response (CAR):** Sequential salivary samples at wake, +30 min, and +60 min capture the HPA-axis morning activation pulse; not a clinical diagnostic test but a validated research phenotype.
- **CBG-confounded clinical situations** (oral contraceptives, critical illness, cirrhosis): salivary cortisol is unaffected by CBG and gives a direct free-cortisol read.

**Assay considerations.** Immunoassay salivary cortisol reads consistently higher than LC-MS/MS because cortisone — the inactive 11-keto metabolite — cross-reacts at 0.3–31.1% depending on the platform, and salivary cortisone is present at concentrations similar to or exceeding cortisol. This systematic positive bias means immunoassay-derived LNSC reference intervals cannot be applied to LC-MS/MS results and vice versa [11, mechanism_review; 13, cohort]. LC-MS/MS for saliva can simultaneously quantify cortisol and cortisone, with salivary cortisone emerging as a complementary marker because it is completely unaffected by topical or inhaled hydrocortisone contamination [11, mechanism_review].

**Pre-analytical risks specific to saliva:** blood contamination from bleeding gums falsely elevates results; hand contamination with topical hydrocortisone cream (including residue transferred during Salivette handling) is a documented source of false positives; salivary prednisolone after oral dosing directly cross-reacts in immunoassays. Samples should be frozen within 4 hours and are stable for at least 3 months at −20 °C [11, mechanism_review].

### 24-Hour Urinary Free Cortisol (UFC)

UFC measures the small filtered fraction of free cortisol (~1% of daily production) that escapes renal tubular reabsorption. It is an integrated 24-hour index of hypercortisolism, correlating with mean plasma free cortisol, and is less sensitive to the CBG problem than serum total cortisol.

**Immunoassay UFC over-reads substantially.** Urine contains not only unconjugated cortisol but abundant ring-A reduced metabolites (tetrahydrocortisol, allotetrahydrocortisol, tetrahydrocortisone) and other conjugated steroids that share structural epitopes. On two commercial immunoassays (Coat-A-Count RIA and Centaur), UFC was overestimated by approximately 1.9-fold and 1.6-fold respectively versus GC-MS reference values; LC-MS/MS achieved excellent agreement with GC-MS (slope 1.004, r² = 0.994) [13, cohort]. A systematic review of four newer automated immunoassay platforms versus LC-MS/MS confirmed a consistent proportional positive bias across all immunoassay platforms, of variable magnitude depending on metabolite cross-reactivity [11, mechanism_review].

The practical consequence: immunoassay UFC upper reference limits are set approximately 2-fold higher than LC-MS/MS limits. A lab switching methods without updating its reference interval will generate false-normal results in patients with mild Cushing's syndrome. LC-MS/MS is considered the reference method for UFC, is recommended by the Endocrine Society [7, regulatory], and is standard at major reference laboratories.

**Collection logistics.** A complete 24-hour collection is required; incomplete collections systematically underestimate UFC and are the most common source of false-normal results. Creatinine excretion should be reported in parallel as a completeness check. Water loading >5 L/day falsely elevates UFC by exceeding the CBG binding capacity in blood. Renal failure reduces UFC independent of adrenal status.

### Analytical Interferences

**Biotin (vitamin B7).** Many immunoassay platforms use streptavidin–biotin chemistry as a capture mechanism. High-dose biotin supplementation (≥5–10 mg/day, commonly taken for hair/nail products; up to 300 mg/day in some multiple sclerosis trials) saturates streptavidin binding sites. In competitive immunoassays (the format used for cortisol), this produces **falsely elevated results**. The FDA issued a safety communication in November 2017 flagging this risk. Biotin should be withheld for at least 8–48 hours before cortisol testing depending on dose; very high doses may require a longer washout [11, mechanism_review].

**Heterophile and anti-animal antibodies.** Endogenous heterophile antibodies (including human anti-mouse antibodies, HAMA) can form bridges between capture and signal antibodies in sandwich formats, but cortisol is measured by competitive immunoassay, making heterophile interference less common. Anti-streptavidin IgM antibodies have been described as mimicking the biotin-interference pattern.

**Exogenous glucocorticoids — clinical checklist:**
- Oral/systemic glucocorticoids: cross-reactivity as tabulated above; prednisolone and methylprednisolone are the highest-risk agents. Dexamethasone does not cross-react.
- Inhaled corticosteroids (fluticasone, budesonide): generally at low enough serum concentrations that immunoassay interference is minor but documented case reports exist.
- Topical corticosteroids: relevant for salivary cortisol (hand contamination) rather than serum total cortisol.

### Pre-Analytics: The Single Biggest Variable

**Sampling time.** Cortisol follows a steep circadian rhythm: morning peak (roughly 8 AM) of 10–25 µg/dL (275–690 nmol/L) versus nadir at midnight of <1.8 µg/dL (<50 nmol/L). An undocumented shift in draw time by even 2–3 hours can produce a change exceeding the cortisol reference interval entirely. Every cortisol result must be accompanied by the exact collection time, and morning draws should specify whether the sample was fasting and ambulatory.

**Venipuncture stress.** The act of catheter insertion or venipuncture activates a rapid ACTH-cortisol stress response that can raise serum cortisol by 30–50% within 20 minutes. Protocols for dynamic testing (ACTH stimulation, dexamethasone suppression) typically specify an indwelling cannula placed at least 30 minutes before sampling.

**Shift work and disrupted sleep.** The circadian cortisol nadir is anchored to the habitual sleep/wake cycle, not clock time. Night-shift workers or subjects with chronic sleep disruption have a phase-shifted cortisol nadir; applying standard morning reference intervals or late-night cut-offs to these populations without accounting for wake time introduces systematic misclassification.

**Standardization gaps.** Despite decades of use, cortisol immunoassays remain poorly harmonized across platforms; the bias between assays for the same specimen has been measured at 8–36% in proficiency surveys [10, mechanism_review]. There is a reference measurement procedure (RMP) for serum cortisol (JCTLM-listed LC-MS/MS reference method), but most routine immunoassays are not traceable to it. Clinicians comparing cortisol results from different laboratories or longitudinally switching assay platforms should verify that method-specific reference intervals are applied.

---

## Determinants & Clinical Significance

### High Cortisol States: Cushing's Syndrome

Cortisol excess — Cushing's syndrome — is classified by etiology before clinical features are addressed, because management depends entirely on the underlying cause.

#### Classification

**ACTH-dependent Cushing's syndrome** (~80–85% of endogenous cases) arises when an autonomous source of ACTH drives bilateral adrenal cortisol overproduction. The dominant form is **Cushing's disease**: a corticotroph pituitary adenoma secreting ACTH, accounting for approximately 70% of all endogenous Cushing's cases [7, regulatory; 14, regulatory]. The remaining ACTH-dependent fraction is **ectopic ACTH syndrome**, produced by non-pituitary tumors (small-cell lung carcinoma, bronchial carcinoids, pancreatic neuroendocrine tumors) and typically presenting with more severe, rapidly progressive hypercortisolism.

**ACTH-independent Cushing's syndrome** (~15–20% of endogenous cases) results from primary adrenal pathology — adrenocortical adenoma (benign, most common in this subtype), adrenocortical carcinoma (rare, often large with virilization), and, rarely, bilateral adrenal hyperplasia. In these states, autonomous adrenal cortisol suppresses ACTH to near-zero.

**Exogenous glucocorticoid use is the single most common cause of Cushing's syndrome overall** — far exceeding all endogenous etiologies combined — because corticosteroids are among the most widely prescribed drug classes globally. This form is clinically indistinguishable from endogenous Cushing's but produces suppressed ACTH and suppressed endogenous cortisol on standard assays; importantly, some immunoassays cross-react with synthetic glucocorticoids, artificially elevating measured cortisol [7, regulatory].

#### Clinical Features

The Endocrine Society diagnosis guideline [7, regulatory] identifies high-discriminatory features: easy bruising, facial plethora, proximal myopathy, and wide (>1 cm) violaceous (purple-red) striae. Supporting features include central/truncal obesity, supraclavicular and dorsocervical fat pads, hypertension, glucose intolerance or frank diabetes, early-onset osteoporosis, and neuropsychiatric disturbance. Children show weight gain with paradoxical growth arrest.

#### Recommended Screening Tests

The Endocrine Society recommends four initial biochemical tests, any one of which is acceptable as a first-line screen [7, regulatory]:

1. 24-hour urinary free cortisol (UFC) — integrates total daily cortisol output; a single normal result does not exclude cyclical disease
2. Late-night salivary cortisol (LNSC) — captures the nadir, which is pathologically elevated in Cushing's; two abnormal values recommended given intra-individual variation
3. 1 mg overnight dexamethasone suppression test (DST) — post-dex serum cortisol >50 nmol/L (>1.8 µg/dL) is abnormal
4. 2-day low-dose DST (2 mg/day) — a longer alternative with slightly higher specificity

An abnormal result on any single test warrants referral to endocrinology and confirmation with a second test before etiology workup (dynamic testing for ACTH source localization).

### Pseudo-Cushing's States

Pseudo-Cushing's describes conditions producing mild hypercortisolemia with overlapping clinical features of Cushing's syndrome, confounding biochemical workup. The two most common are **major depressive disorder** and **chronic alcohol use**. Other recognized states include poorly controlled type 2 diabetes, polycystic ovary syndrome with obesity, morbid obesity, and severe acute physical stress. The shared mechanism is heightened hypothalamic CRH secretion driving an otherwise structurally intact HPA axis — glucocorticoid feedback regulation is functionally impaired but the axis itself is not neoplastic. In pseudo-Cushing's, the biochemical and clinical picture typically resolves when the precipitating condition is treated, which is the critical distinction from true Cushing's [7, regulatory].

### Low Cortisol States: Adrenal Insufficiency

Adrenal insufficiency (AI) is classified by the anatomical level of failure [8, regulatory]:

#### Primary AI (Addison's Disease)

The adrenal cortex itself is destroyed or dysfunctional, causing simultaneous glucocorticoid AND mineralocorticoid (aldosterone) deficiency, with compensatory ACTH elevation (high ACTH is the biochemical hallmark). **Autoimmune adrenalitis is the commonest cause in the developed world**, accounting for 80–90% of primary AI in high-income countries; it may occur in isolation or as part of autoimmune polyglandular syndromes. Other causes include bilateral adrenal infiltration (tuberculosis — still dominant in high-prevalence regions; fungal infections, metastatic malignancy), hemorrhage (Waterhouse-Friderichsen syndrome in meningococcemia), and bilateral adrenalectomy.

#### Secondary AI

Failure at the pituitary level — deficient ACTH secretion — with intact adrenal anatomy. Causes include pituitary adenoma, surgery, radiation, or inflammatory/infiltrative disease. Because the zona glomerulosa is regulated by the renin-angiotensin system rather than ACTH, **mineralocorticoid secretion is largely preserved** in secondary AI — a key clinical distinction from primary AI (no salt-wasting crisis, though sodium can still fall via ADH dysregulation).

#### Tertiary AI and Exogenous-Glucocorticoid-Induced HPA Suppression

Tertiary AI is hypothalamic (CRH-deficient), but in clinical practice the **single most common cause of AI globally is exogenous glucocorticoid-induced HPA axis suppression** [8, regulatory]. Prolonged administration of corticosteroids by any route (oral, inhaled, topical, intra-articular, rectal) suppresses CRH and ACTH secretion via negative feedback; on discontinuation, the HPA axis may fail to recover for weeks to months, leaving patients at risk for cortisol deficiency, particularly under physiologic stress. The risk increases with dose, duration, and dosing timing; even inhaled corticosteroids at higher doses can produce meaningful suppression.

#### Adrenal Crisis

Adrenal crisis is a life-threatening acute decompensation — typically precipitated by physiologic stress (infection, surgery, trauma) in a patient with pre-existing AI — characterized by profound hypotension, volume depletion, hyponatremia, hyperkalemia (in primary AI), and altered consciousness. It is a medical emergency requiring immediate parenteral hydrocortisone (100 mg IV/IM) and aggressive fluid resuscitation [8, regulatory]. Patients with known AI must carry emergency injection kits and receive "sick-day rule" counseling (double or triple oral doses during illness). Mortality risk is substantial when crisis is not recognized and treated promptly.

### Determinants That Raise Cortisol

**Acute psychological and physical stress** is the most common transient cortisol elevator. Both psychological threat and physical noxious stimuli (pain, tissue damage, hypoglycemia, fever) activate the paraventricular nucleus, releasing CRH → pituitary ACTH → adrenal cortisol within minutes. Cortisol typically returns to baseline within 60–90 minutes of a resolved acute stressor.

**Chronic psychological stress** produces a more complex HPA pattern — initially elevated cortisol, but with prolonged chronic stress, blunted cortisol awakening response (CAR) and flattened diurnal slope in some individuals.

**Cushing's syndrome (endogenous or exogenous)** — as detailed above.

**Exogenous glucocorticoids:** Synthetic corticosteroids raise total measured glucocorticoid activity, and some immunoassays cross-react with prednisolone, methylprednisolone, and prednisone, yielding apparently elevated serum cortisol when endogenous cortisol is actually suppressed.

**Estrogen, oral contraceptives (OCP), and pregnancy:** Estrogen stimulates hepatic synthesis of CBG. Pregnancy and OCP use raise CBG two- to threefold, binding more circulating cortisol and elevating **total serum cortisol** without a proportional increase in **free (bioactive) cortisol**. This is an assay artifact for bound cortisol, not true hypercortisolism; free cortisol (salivary or 24-hour UFC) is a more reliable measure in these states.

**Major depression:** Activates the HPA axis through central CRH hypersecretion; produces mild to moderate hypercortisolemia that can mimic Cushing's (pseudo-Cushing's state).

**Chronic alcohol use:** Stimulates HPA axis via central mechanisms; long-term heavy use can cause persistent mild hypercortisolemia; this too is a recognized pseudo-Cushing's state.

**Critical illness:** Systemic illness and major surgery drive marked, transient cortisol elevation as part of the physiological stress response. In critical illness, total cortisol may appear low due to hypoalbuminemia and falling CBG even when free cortisol is normal — the basis of ongoing debate around "relative adrenal insufficiency" in the ICU.

**Sleep deprivation:** Partial or total sleep loss elevates evening cortisol. In a controlled sleep deprivation experiment (n = 11), next-evening cortisol was 37–45% higher after one night of partial or total sleep loss, with delayed onset of the overnight cortisol nadir by at least one hour [15, open_label].

**Acute intense exercise:** Produces a transient cortisol spike proportional to exercise intensity and duration; returns to baseline within hours in healthy individuals.

### Determinants That Lower Cortisol

- **Adrenal insufficiency (primary, secondary, or tertiary):** As detailed above.
- **Exogenous-glucocorticoid-induced HPA suppression:** Suppresses endogenous cortisol production; the measured total cortisol may be artifactually elevated by cross-reactive synthetic steroids while true endogenous cortisol output is reduced.
- **Hypopituitarism:** Deficient ACTH output from any pituitary disease reduces adrenal cortisol secretion without adrenal gland pathology.
- **Time of day:** Cortisol is lowest at night (midnight to early morning). Testing at the wrong time of day is the most common source of misinterpretation of a single cortisol value.

### The "Adrenal Fatigue" Construct — An Honest Assessment

"Adrenal fatigue" is the claim that non-specific symptoms (fatigue, brain fog, salt cravings, difficulty waking) reflect subclinical cortisol deficiency from chronically "exhausted" adrenal glands — despite normal formal testing. It is **not a recognized diagnosis in endocrinology** and is rejected by the Endocrine Society and other endocrine bodies.

A systematic review by Cadegiani and Kater (2016) specifically examined whether scientific evidence substantiates "adrenal fatigue" [16, mechanism_review]. Searching PubMed, MEDLINE, and Cochrane databases through April 2016, they identified 58 studies with strict inclusion criteria assessing cortisol profiles and fatigue/energy status. Key findings: the cortisol awakening response was normal in 51.9% of studies (27 reviewed); direct awakening cortisol was normal in 65.5% (29 studies); salivary cortisol rhythm showed no between-group differences in 61.5% (26 studies). The authors concluded: "there is no substantiation that 'adrenal fatigue' is an actual medical condition. Therefore, adrenal fatigue is still a myth" [16, mechanism_review].

This does **not** mean that HPA-axis dysregulation under chronic stress is absent — there is genuine research on blunted cortisol awakening responses in burnout, flattened diurnal slopes in certain chronic illness states, and HPA changes with chronic trauma. These are real phenomena studied under validated constructs (burnout, PTSD, chronic stress). The failure of "adrenal fatigue" as a construct is not a failure to recognize stress biology; it is a failure of a specific, unvalidated claim about subclinical adrenal dysfunction that cannot be demonstrated on objective testing. Treating presumed "adrenal fatigue" with glucocorticoids carries the documented risk of inducing genuine HPA suppression — creating the very cortisol deficiency the diagnosis claims to treat.

### Diurnal Cortisol Dysregulation: Associations with Metabolic and Cardiovascular Outcomes

An epidemiological literature — primarily prospective cohort studies — has examined associations between flattened diurnal cortisol slope, blunted cortisol awakening response, and adverse health outcomes.

In the **Whitehall II prospective cohort** (n = 4,047 British civil servants; mean follow-up 6.1 years), Kumari et al. (2011) found that a 1-SD flatter diurnal salivary cortisol slope was associated with a hazard ratio of 1.87 (95% CI 1.32–2.64) for cardiovascular mortality and 1.30 for all-cause mortality [17, cohort]. Importantly, this is an observational association: reverse causation, subclinical disease affecting both cortisol and mortality, and confounding by socioeconomic status, smoking, and baseline health are all plausible. A flattened slope cannot be interpreted as a causal driver of cardiovascular mortality on this evidence alone.

Associations between dysregulated cortisol patterns and metabolic syndrome, depression, and immune dysregulation have been reported in multiple smaller cohorts, but effect sizes are heterogeneous, the direction of causality is usually unclear, and confounding is substantial. These associations support monitoring cortisol in high-risk clinical contexts; they do not support therapeutic manipulation of cortisol in individuals with flattened slopes outside established diagnoses.

### Key Limitations: Why a Single Cortisol Value Is Rarely Interpretable

1. **Extreme time-dependence.** Cortisol varies ~10-fold across a normal day. A morning peak at 08:00 and an evening value at 20:00 span entirely different physiological ranges. A cortisol result without a precise draw time is nearly uninterpretable.
2. **CBG confounding.** Total immunoassay cortisol measures protein-bound plus free cortisol. Any condition altering CBG (estrogen, OCP, critical illness, nephrotic syndrome) produces a total cortisol that diverges from free (bioactive) cortisol.
3. **Immunoassay cross-reactivity.** Standard competitive immunoassays cross-react with synthetic glucocorticoids (prednisolone in particular) and cortisone. LC-MS/MS is gold standard when precision is required.
4. **Dynamic-test dependence for diagnosis.** Static cortisol values have limited diagnostic utility for AI and Cushing's; both diagnoses require dynamic testing (stimulation for AI; suppression for Cushing's).
5. **Stress of the blood draw.** Venipuncture itself is a stress stimulus; acutely anxious or distressed patients may show cortisol elevations that do not reflect their basal state.
6. **Episodic secretion and cyclical Cushing's.** Cushing's syndrome, especially from an ectopic or pituitary source, can be cyclical; a normal cortisol on a single sampling does not exclude the diagnosis when clinical suspicion is high.

---

## Bibliography

[1]. Herman JP, McKlveen JM, Ghosal S, Kopp B, Wulsin A, Makinson R, Scheimann J, Myers B. Regulation of the hypothalamic-pituitary-adrenocortical stress response. Compr Physiol. 2016;6(2):603–621. PMID: 27065163. DOI: 10.1002/cphy.c150015. — tag: mechanism_review — tier: 1

[2]. Stalder T, Oster H, Abelson JL, Huthsteiner K, Klucken T, Clow A. The cortisol awakening response: regulation and functional significance. Endocr Rev. 2025;46(1):43–59. PMID: 39177247. DOI: 10.1210/endrev/bnae024. — tag: mechanism_review — tier: 1

[3]. Lightman SL, Conway-Campbell BL. The crucial role of pulsatile activity of the HPA axis for continuous dynamic equilibration. Nat Rev Neurosci. 2010;11(10):710–718. PMID: 20842176. DOI: 10.1038/nrn2914. — tag: mechanism_review — tier: 1

[4]. Chan WL, Carrell RW, Zhou A, Read RJ. How changes in affinity of corticosteroid-binding globulin modulate free cortisol concentration. J Clin Endocrinol Metab. 2013;98(8):3315–3322. PMID: 23783094. DOI: 10.1210/jc.2012-4280. — tag: mechanism_review — tier: 1

[5]. Chapman K, Holmes M, Seckl J. 11β-hydroxysteroid dehydrogenases: intracellular gate-keepers of tissue glucocorticoid action. Physiol Rev. 2013;93(3):1139–1206. PMID: 23899562. DOI: 10.1152/physrev.00020.2012. — tag: mechanism_review — tier: 1

[6]. Endocrine Society. Cortisol Reference Values and Interpretation. Endocrine Society Clinical Resources. endocrine.org. — tag: regulatory — tier: 2

[7]. Nieman LK, Biller BMK, Findling JW, Newell-Price J, Savage MO, Stewart PM, Montori VM. The diagnosis of Cushing's syndrome: an Endocrine Society clinical practice guideline. J Clin Endocrinol Metab. 2008;93(5):1526–1540. PMID: 18334580. — tag: regulatory — tier: 2

[8]. Bornstein SR, Allolio B, Arlt W, Barthel A, Don-Wauchope A, Hammer GD, Husebye ES, Merke DP, Murad MH, Stratakis CA, Torpy DJ. Diagnosis and treatment of primary adrenal insufficiency: an Endocrine Society clinical practice guideline. J Clin Endocrinol Metab. 2016;101(2):364–389. PMID: 26760044. — tag: regulatory — tier: 2

[9]. Okutan S, Jørgensen NT, Pedersen LE, Borresen SW, Hilsted L, Hansen LF, Feldt-Rasmussen U, Klose M. Determination of cortisol cut-off limits and steroid dynamics in the ACTH stimulation test: a comparative analysis using Roche Elecsys Cortisol II immunoassay and LC-MS/MS. Endocrine. 2024;85(1):321–330. PMID: 38460071. — tag: cohort — tier: 1

[10]. Krasowski MD, Drees D, Morris CS, Maakestad J, Blau JL, Ekins S. Cross-reactivity of steroid hormone immunoassays: clinical significance and two-dimensional molecular similarity prediction. BMC Clin Pathol. 2014;14:33. PMID: 25071417. — tag: mechanism_review — tier: 1

[11]. Casals G, Hanzu FA. Cortisol measurements in Cushing's syndrome: immunoassay or mass spectrometry? Ann Lab Med. 2020;40(4):285–296. PMID: 32067427. — tag: mechanism_review — tier: 1

[12]. El-Farhan N, Rees DA, Evans C. Measuring cortisol in serum, urine and saliva — are our assays good enough? Ann Clin Biochem. 2017;54(3):308–322. PMID: 28068807. — tag: mechanism_review — tier: 1

[13]. Wood L, Ducroq DH, Fraser HL, Gillingwater S, Evans C, Pickett AJ, Rees DW, John R, Turkes A. Measurement of urinary free cortisol by tandem mass spectrometry and comparison with results obtained by gas chromatography-mass spectrometry and two commercial immunoassays. Ann Clin Biochem. 2008;45(Pt 4):380–388. PMID: 18583623. — tag: cohort — tier: 1

[14]. Nieman LK, Biller BMK, Findling JW, Murad MH, Newell-Price J, Savage MO, Tabarin A. Treatment of Cushing's syndrome: an Endocrine Society clinical practice guideline. J Clin Endocrinol Metab. 2015;100(8):2807–2831. PMID: 26222757. — tag: regulatory — tier: 2

[15]. Leproult R, Copinschi G, Buxton O, Van Cauter E. Sleep loss results in an elevation of cortisol levels the next evening. Sleep. 1997;20(10):865–870. PMID: 9415946. — tag: open_label — tier: 2

[16]. Cadegiani FA, Kater CE. Adrenal fatigue does not exist: a systematic review. BMC Endocr Disord. 2016;16(1):48. PMID: 27557747. — tag: mechanism_review — tier: 1

[17]. Kumari M, Shipley M, Stafford M, Kivimaki M. Association of diurnal patterns in salivary cortisol with all-cause and cardiovascular mortality: findings from the Whitehall II study. J Clin Endocrinol Metab. 2011;96(5):1478–1485. PMID: 21346074. — tag: cohort — tier: 1
