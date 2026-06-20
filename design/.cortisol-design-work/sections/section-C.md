# Section C: Measurement & Interferences

## C.1 Serum Total Cortisol: Immunoassay vs LC-MS/MS

Serum cortisol in routine clinical practice is almost universally measured by automated direct immunoassay (chemiluminescent, electrochemiluminescent, or enzyme-linked platforms). These assays quantify the sum of free and protein-bound cortisol without a prior extraction step, making them high-throughput and cost-effective. Their central limitation is analytical specificity: because cortisol antibodies are raised against a structurally complex steroid, they recognize other steroids that share similar ring architecture.

Liquid chromatography–tandem mass spectrometry (LC-MS/MS) separates cortisol from co-eluting steroids by both retention time and parent-ion/fragment-ion pair, then quantifies it against a stable-isotope internal standard. It is more accurate at low concentrations, is the recommended method for dynamic tests where interfering steroids accumulate (metyrapone challenge, adrenocortical hyperplasia), and is the only method capable of simultaneously identifying exogenous glucocorticoids in the same run [1, mechanism_review; 2, mechanism_review].

**Cross-reactivity magnitude.** On the Roche Elecsys platform — the most thoroughly characterized — cross-reactivity values reported in the package insert and independently confirmed are:

| Compound | Cross-reactivity (Roche Elecsys) | Clinical likelihood |
|---|---|---|
| 6-Methylprednisolone | 249% | High (therapeutic concentrations up to ~1,000 ng/mL) |
| Prednisolone | 148% | High (up to ~400 ng/mL in transplant patients) |
| 11-Deoxycortisol | Clinically significant | High during metyrapone challenge |
| 21-Deoxycortisol | Clinically significant | High in 21-hydroxylase deficiency |
| Cortisone | 0.3–31.1% depending on assay | Ubiquitous endogenous interferent |

[1, mechanism_review]

Prednisolone's cross-reactivity of 148% means that patients receiving therapeutic prednisolone can generate immunoassay cortisol readings elevated by the prednisolone itself — making a falsely suppressed or falsely normal result impossible to interpret without switching to LC-MS/MS. Methylprednisolone at 249% is clinically the most dangerous interferent in this class. By contrast, dexamethasone and betamethasone do not generally cross-react with cortisol immunoassays, which is why dexamethasone is used in suppression tests without LC-MS/MS interference — although confirmation of dexamethasone non-reactivity should be verified for any specific platform [2, mechanism_review].

Topical and inhaled corticosteroids are a subtler source of falsely elevated readings; prednisolone contamination of a salivary cortisol sample taken shortly after an oral dose has been documented as a clinically significant confounder for late-night salivary cortisol (LNSC) testing [1, mechanism_review].

## C.2 The CBG Problem (Load-Bearing Caveat)

Approximately 70–80% of circulating cortisol is bound to corticosteroid-binding globulin (CBG), 10–15% to albumin, and only 2–5% is free and biologically active. CBG is a high-affinity, low-capacity hepatic glycoprotein (SERPIN family); its concentration sets a ceiling on how much total cortisol the assay can detect before the free fraction begins to rise steeply. This means **total serum cortisol is an unreliable index of adrenal function whenever CBG is abnormal** [2, mechanism_review; 3, mechanism_review].

**States that raise CBG → falsely high total cortisol:**
- Oral contraceptives containing estrogen: CBG rises 2–3-fold above baseline. Total cortisol may reach levels indistinguishable from Cushing's syndrome while free cortisol remains normal. Women on combined oral contraceptives should ideally discontinue them for approximately 6 weeks before cortisol dynamic testing, or salivary/free cortisol should be used instead [3, mechanism_review].
- Pregnancy: CBG rises 2–3-fold. Both total and free cortisol are genuinely elevated in late pregnancy (HPA-axis resetting), but in the first trimester the total cortisol rise often exceeds the free-cortisol rise due to CBG induction alone.
- Estrogen-replacement therapy: same mechanism.

**States that lower CBG → falsely low total cortisol:**
- Critical illness / sepsis: CBG falls rapidly as an acute-phase response and due to cleavage by leukocyte elastase. A patient in septic shock may have a "subnormal" total cortisol reading despite an intact, appropriately activated adrenal axis. This is the central methodological challenge in diagnosing critical illness-related corticosteroid insufficiency (CIRCI) and is why some guidelines caution against relying on total serum cortisol alone in the ICU [3, mechanism_review].
- Nephrotic syndrome: hepatic CBG synthesis is outpaced by urinary protein losses. Total cortisol can fall below the lower end of the reference interval while free cortisol is normal or elevated.
- Cirrhosis: impaired hepatic synthesis reduces both CBG and albumin. Total cortisol underestimates the free fraction; ACTH-stimulation test cutoffs derived from healthy populations cannot be applied without modification [3, mechanism_review].

In all of these states, **salivary cortisol, urinary free cortisol (UFC), or directly measured serum free cortisol (by equilibrium dialysis or ultrafiltration + LC-MS/MS) should replace total cortisol** as the index of adrenal function. Calculated free cortisol using the Coolens equation (requires total cortisol + CBG measured on the same sample) correlates well with dialysis-derived free cortisol (r ≈ 0.98 in some datasets) and is a practical alternative when direct free-cortisol assays are unavailable [2, mechanism_review].

## C.3 Salivary Cortisol

Cortisol crosses the salivary gland epithelium by passive diffusion; only the free (unbound) fraction passes, so salivary cortisol directly reflects serum free cortisol and is independent of CBG changes. This makes it the specimen of choice for:

- **Late-night salivary cortisol (LNSC):** The loss of nadir suppression at 11 PM–midnight is a hallmark of autonomous hypercortisolism; salivary collection is non-invasive, can be performed at home, and captures the physiologically important circadian nadir without hospitalization. Endocrine Society guidelines list LNSC as a first-line Cushing's screening test [5, regulatory].
- **Cortisol awakening response (CAR):** sequential salivary samples at wake, +30 min, and +60 min capture the HPA-axis morning activation pulse; not a clinical diagnostic test but a validated research phenotype.
- **CBG-confounded clinical situations** (oral contraceptives, critical illness, cirrhosis): salivary cortisol is unaffected by CBG and gives a direct free-cortisol read.

**Assay considerations.** Immunoassay salivary cortisol reads consistently higher than LC-MS/MS because cortisone — the inactive 11-keto metabolite — cross-reacts at 0.3–31.1% depending on the platform, and salivary cortisone is present at concentrations similar to or exceeding cortisol. This systematic positive bias means immunoassay-derived LNSC reference intervals cannot be applied to LC-MS/MS results and vice versa [2, mechanism_review; 4, cohort]. LC-MS/MS for saliva can simultaneously quantify cortisol and cortisone, with salivary cortisone emerging as a complementary marker because it is completely unaffected by topical or inhaled hydrocortisone contamination [2, mechanism_review].

**Pre-analytical risks specific to saliva:** blood contamination from bleeding gums falsely elevates results; hand contamination with topical hydrocortisone cream (including residue transferred during Salivette handling) is a documented source of false positives; salivary prednisolone after oral dosing directly cross-reacts in immunoassays. Samples should be frozen within 4 hours and are stable for at least 3 months at −20 °C [2, mechanism_review].

## C.4 24-Hour Urinary Free Cortisol (UFC)

UFC measures the small filtered fraction of free cortisol (~1% of daily production) that escapes renal tubular reabsorption. It is an integrated 24-hour index of hypercortisolism, correlating with mean plasma free cortisol, and is less sensitive to the CBG problem than serum total cortisol.

**Immunoassay UFC over-reads substantially.** Urine contains not only unconjugated cortisol but abundant ring-A reduced metabolites (tetrahydrocortisol, allotetrahydrocortisol, tetrahydrocortisone) and other conjugated steroids that share structural epitopes. On two commercial immunoassays (Coat-A-Count RIA and Centaur), UFC was overestimated by approximately 1.9-fold and 1.6-fold respectively versus GC-MS reference values; LC-MS/MS achieved excellent agreement with GC-MS (slope 1.004, r² = 0.994) [4, cohort]. A systematic review of four newer automated immunoassay platforms versus LC-MS/MS confirmed a consistent proportional positive bias across all immunoassay platforms, of variable magnitude depending on metabolite cross-reactivity [2, mechanism_review].

The practical consequence: immunoassay UFC upper reference limits are set approximately 2-fold higher than LC-MS/MS limits. A lab switching methods without updating its reference interval will generate false-normal results in patients with mild Cushing's syndrome. LC-MS/MS is considered the reference method for UFC, is recommended by the Endocrine Society [5, regulatory], and is standard at major reference laboratories.

**Collection logistics.** A complete 24-hour collection is required; incomplete collections systematically underestimate UFC and are the most common source of false-normal results. Creatinine excretion should be reported in parallel as a completeness check. Water loading >5 L/day falsely elevates UFC by exceeding the CBG binding capacity in blood. Renal failure reduces UFC independent of adrenal status.

## C.5 Analytical Interferences

**Biotin (vitamin B7).** Many immunoassay platforms use streptavidin–biotin chemistry as a capture mechanism. High-dose biotin supplementation (≥5–10 mg/day, commonly taken for hair/nail products; up to 300 mg/day in some multiple sclerosis trials) saturates streptavidin binding sites. In competitive immunoassays (the format used for cortisol), this produces **falsely elevated results**. The FDA issued a safety communication in November 2017 flagging this risk. Biotin should be withheld for at least 8–48 hours before cortisol testing depending on dose; very high doses may require a longer washout [2, mechanism_review].

**Heterophile and anti-animal antibodies.** Endogenous heterophile antibodies (including human anti-mouse antibodies, HAMA) can form bridges between capture and signal antibodies in sandwich formats, but cortisol is measured by competitive immunoassay, making heterophile interference less common. Anti-streptavidin IgM antibodies have been described as mimicking the biotin-interference pattern.

**Exogenous glucocorticoids — clinical checklist:**
- Oral/systemic glucocorticoids: cross-reactivity as tabulated above; prednisolone and methylprednisolone are the highest-risk agents. Dexamethasone does not cross-react.
- Inhaled corticosteroids (fluticasone, budesonide): generally at low enough serum concentrations that immunoassay interference is minor but documented case reports exist.
- Topical corticosteroids: relevant for salivary cortisol (hand contamination) rather than serum total cortisol.

## C.6 Pre-Analytics: The Single Biggest Variable

**Sampling time.** Cortisol follows a steep circadian rhythm: morning peak (roughly 8 AM) of 10–25 µg/dL (275–690 nmol/L) versus nadir at midnight of <1.8 µg/dL (<50 nmol/L). An undocumented shift in draw time by even 2–3 hours can produce a change exceeding the cortisol reference interval entirely. Every cortisol result must be accompanied by the exact collection time, and morning draws should specify whether the sample was fasting and ambulatory.

**Venipuncture stress.** The act of catheter insertion or venipuncture activates a rapid ACTH-cortisol stress response that can raise serum cortisol by 30–50% within 20 minutes. Protocols for dynamic testing (ACTH stimulation, dexamethasone suppression) typically specify an indwelling cannula placed at least 30 minutes before sampling.

**Shift work and disrupted sleep.** The circadian cortisol nadir is anchored to the habitual sleep/wake cycle, not clock time. Night-shift workers or subjects with chronic sleep disruption have a phase-shifted cortisol nadir; applying standard morning reference intervals or late-night cut-offs to these populations without accounting for wake time introduces systematic misclassification.

**Standardization gaps.** Despite decades of use, cortisol immunoassays remain poorly harmonized across platforms; the bias between assays for the same specimen has been measured at 8–36% in proficiency surveys [1, mechanism_review]. There is a reference measurement procedure (RMP) for serum cortisol (JCTLM-listed LC-MS/MS reference method), but most routine immunoassays are not traceable to it. Clinicians comparing cortisol results from different laboratories or longitudinally switching assay platforms should verify that method-specific reference intervals are applied.

---

## Bibliography

1. Krasowski MD, Drees D, Morris CS, Maakestad J, Blau JL, Ekins S. Cross-reactivity of steroid hormone immunoassays: clinical significance and two-dimensional molecular similarity prediction. *BMC Clin Pathol.* 2014;14:33. PMID: 25071417. [mechanism_review]

2. Casals G, Hanzu FA. Cortisol measurements in Cushing's syndrome: immunoassay or mass spectrometry? *Ann Lab Med.* 2020;40(4):285–296. PMID: 32067427. [mechanism_review]

3. El-Farhan N, Rees DA, Evans C. Measuring cortisol in serum, urine and saliva — are our assays good enough? *Ann Clin Biochem.* 2017;54(3):308–322. PMID: 28068807. [mechanism_review]

4. Wood L, Ducroq DH, Fraser HL, Gillingwater S, Evans C, Pickett AJ, Rees DW, John R, Turkes A. Measurement of urinary free cortisol by tandem mass spectrometry and comparison with results obtained by gas chromatography-mass spectrometry and two commercial immunoassays. *Ann Clin Biochem.* 2008;45(Pt 4):380–388. PMID: 18583623. [cohort]

5. Nieman LK, Biller BMK, Findling JW, Newell-Price J, Savage MO, Stewart PM, Montori VM. The diagnosis of Cushing's syndrome: an Endocrine Society Clinical Practice Guideline. *J Clin Endocrinol Metab.* 2008;93(5):1526–1540. PMID: 18334580. [regulatory]
