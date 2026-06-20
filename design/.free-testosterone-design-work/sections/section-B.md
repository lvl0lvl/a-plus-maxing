# Section B: How It's Determined — Measurement vs Calculation

Free testosterone (fT) constitutes roughly 1–4% of total circulating testosterone [1, mechanism_review]. The rest is bound to sex hormone–binding globulin (SHBG, ~44% — tight, biologically inactive) and albumin (~50–54% — loose, largely bioavailable); depending on population and measurement method, SHBG-bound fractions as high as 65% have been reported, but canonical reference-adult-male figures are ~44% SHBG-bound and ~50–54% albumin-bound [2, mechanism_review]. Because only the free fraction can cross cell membranes and activate the androgen receptor, accurate measurement of fT matters whenever total testosterone is discordant with clinical findings — for instance, when SHBG is elevated by age, liver disease, or hyperthyroidism, or suppressed by obesity and insulin resistance.

Three distinct approaches exist, and they are **not interchangeable**. Choosing the wrong one can produce values that are off by as much as 80% [4, cohort].

---

## 1. Equilibrium Dialysis (or Ultrafiltration) + LC-MS/MS — The Reference Method

Equilibrium dialysis (ED) is the gold-standard against which all other methods are benchmarked [1, mechanism_review; 2, regulatory]. In the standard protocol, serum is placed on one side of a semipermeable membrane; buffer occupies the other. The system equilibrates at 37 °C — typically overnight, though centrifugal ultrafiltration cartridges can accelerate this — after which only the unbound (free) hormone has crossed the membrane. The dialysate is then quantified, ideally by liquid chromatography–tandem mass spectrometry (LC-MS/MS), which can reliably detect concentrations down to ~1 pg/mL [1, mechanism_review].

Ultrafiltration (UF) is a practical variant: centrifugal force pushes the ultrafiltrate through the membrane, reducing equilibration time substantially. When UF is coupled to LC-MS/MS, it shows excellent agreement with standard ED (correlation coefficient r = 0.978, bias ≈ 2.4%) [5, cohort].

**Why it is the reference, and why it is rarely the routine:** ED + LC-MS/MS physically separates free hormone based on molecular size, making no assumptions about binding constants or albumin concentration. It is the only method that directly measures what is present in the dialysate. The downsides are real: specialized equipment, multi-step sample handling, long turnaround, and cost. Only a handful of reference laboratories and academic centers run a fully standardized ED pipeline. This is why the clinical world has converged on calculation.

---

## 2. Calculated Free Testosterone (cFT) — The Practical Clinical Standard

Because ED is operationally demanding, clinicians and researchers developed mass-action–based algebraic models that derive fT from inputs that are routinely measured: **total testosterone, SHBG, and albumin**. The two foundational equations are:

- **Södergård equation (1982):** Södergård et al. derived binding constants for testosterone to SHBG and albumin at 37 °C from experimental data, then applied the law of mass action to calculate the free fraction [3, cohort]. In men, approximately 2% of testosterone was unbound — consistent with later ED measurements.

- **Vermeulen equation (1999):** Vermeulen et al. refined this approach in a rigorous validation study (PMID 10523012), comparing calculated fT directly against apparent free testosterone concentration (AFTC) by ED. Their conclusion was unambiguous: calculated fT represents "a rapid, simple, and reliable index of bioavailable T, comparable to AFTC and suitable for clinical routine" [2, mechanism_review]. Concordance between Vermeulen and Södergård estimates is high (r ≈ 0.98) [see also 6, cohort].

In practice, albumin is often fixed at 4.3 g/dL (the population mean) because its intra-individual variation is small in non-critically-ill patients, and the output is not highly sensitive to this input. SHBG accuracy matters more: the Vermeulen equation's main known failure mode is pregnancy, where estradiol saturates SHBG binding sites and causes immunoassay-measured SHBG to overestimate effective binding capacity, artificially depressing cFT [2, mechanism_review].

The 2018 Endocrine Society Clinical Practice Guideline on testosterone therapy explicitly endorses cFT as a legitimate clinical tool: when ED is unavailable, clinicians may "estimate fT concentrations using a formula that accurately calculates fT concentrations using TT, SHBG, and albumin concentrations" [7, regulatory]. Online calculators implementing the Vermeulen equation (e.g., issam.ch/freetesto.htm) make this accessible at the point of care.

**Caveat:** cFT values trend approximately 20–24% higher than ED-measured fT in published comparisons [1, mechanism_review]. This systematic offset is consistent and predictable, not random noise, which is why cFT remains clinically useful as long as the same method is used for baseline and follow-up comparisons.

---

## 3. Direct Analog Immunoassay — Do Not Use

Many commercial automated analyzers offer a "free testosterone" result via a direct analog (tracer-based) immunoassay. This method adds a radiolabeled testosterone analog to unextracted serum, which is then made to compete with endogenous testosterone for binding to an immobilized antibody. The readout is intended to reflect the free fraction.

**The method does not work as described.** The fundamental problem is that the analog tracer behaves differently from native free testosterone: it interacts with serum binding proteins (SHBG and albumin) in a way the assay design does not account for, causing it to detect protein-bound testosterone rather than the genuinely free hormone [4, cohort]. Fritz et al. (2008, *Clinical Chemistry*) confirmed this mechanistically: when total testosterone was held constant while SHBG and bound fractions were varied, the analog assay tracked total testosterone — not the free fraction — demonstrating that the assay is measuring the wrong pool [4, cohort].

The clinical consequences are severe:

- Analog assay values are roughly one-eighth of cFT values in the same patients [4, cohort].
- Values vary systematically with SHBG concentration, which a free-fraction measurement should not do.
- The Endocrine Society's 2018 guideline states directly: "Clinicians should **not** use direct analog-based free testosterone immunoassays, as they are inaccurate" [7, regulatory].
- The 2007 Endocrine Society position statement on testosterone measurement (Rosner et al., PMID 17090633) likewise called for harmonized standards and flagged methodological pitfalls — including direct immunoassay limitations — in clinical testosterone testing [6b, regulatory].

Despite this, direct analog assays remain widely offered because they are cheap, rapid, and run on the same platforms as other immunoassays. The presence of a "free testosterone" line on a standard lab panel does not mean the method is valid. Clinicians should confirm which method a laboratory uses before interpreting results.

---

## Reference Ranges — Method-Dependent, No Universal Standard

**A harmonized reference interval for free testosterone does not exist.** The 2018 Endocrine Society guideline explicitly acknowledges that "a harmonized reference range for fT has not been established, so reference ranges may vary considerably depending on the specific equilibrium dialysis method or the algorithm used" [7, regulatory]. Laboratories are expected to establish their own method-specific ranges.

The best available standardized data come from Jasuja et al. (2023, *Andrology*), who applied a rigorously standardized ED procedure in healthy nonobese men (n = 145) and reported [8, cohort]:

| Group | Free T (pg/mL) | Free T (pmol/L) |
|-------|----------------|-----------------|
| All adult men (≥19 yr), 2.5th–97.5th %ile | 66–309 | 229–1072 |
| Young men (19–39 yr), 2.5th–97.5th %ile | 120–368 | 415–1274 |

For context, Endotext (NBK279145) cites mean ED-measured values of ~102 pg/mL in men aged 20–29 and ~80 pg/mL in men aged 70–79, reflecting the ~30–40% age-associated decline in free testosterone [1, mechanism_review]. Calculated fT (Vermeulen) runs about 20–24% higher than ED values in the same populations [1, mechanism_review].

Commonly cited broad clinical ranges — typically **46–224 pg/mL** (~160–776 pmol/L, ×3.467) or **~1.6–7.8 ng/dL** — reflect mixed-method literature averages and should be treated as orientation, not precision cutoffs.

### Unit Conversions

| From | To | Factor |
|------|----|--------|
| pg/mL → pmol/L | multiply by | **3.467** |
| pmol/L → pg/mL | multiply by | **0.2884** |
| ng/dL → nmol/L | multiply by | **0.03467** |
| nmol/L → ng/dL | multiply by | **28.84** |
| pg/mL → ng/dL | divide by | **10** |
| ng/dL → pg/mL | multiply by | **10** |

Example: 100 pg/mL = 10 ng/dL = 347 pmol/L (100 × 3.467). The free fraction constitutes approximately **1–4% of total T** in healthy adult men [1, mechanism_review; 3, cohort].

---

## Bibliography

1. Nankin HR, Calkins JH. "Laboratory Assessment of Testicular Function." In: Feingold KR, et al., eds. *Endotext* [Internet]. South Dartmouth, MA: MDText.com, Inc.; updated 2019. NCBI Bookshelf NBK279145. [mechanism_review]

2. Vermeulen A, Verdonck L, Kaufman JM. "A critical evaluation of simple methods for the estimation of free testosterone in serum." *J Clin Endocrinol Metab.* 1999;84(10):3666–3672. PMID: 10523012. [mechanism_review]

3. Södergård R, Bäckström T, Shanbhag V, Carstensen H. "Calculation of free and bound fractions of testosterone and estradiol-17 beta to human plasma proteins at body temperature." *J Steroid Biochem.* 1982;16(6):801–810. PMID: 7202083. [cohort]

4. Fritz KS, McKean AJ, Nelson JC, Wilcox RB. "Analog-based free testosterone test results linked to total testosterone concentrations, not free testosterone concentrations." *Clin Chem.* 2008;54(3):512–516. PMID: 18171714. [cohort]

5. Chen Y, Yazdanpanah M, Hoffman BR, Diamandis EP, Wong PY. "Direct measurement of serum free testosterone by ultrafiltration followed by liquid chromatography tandem mass spectrometry." *Clin Biochem.* 2010;43(4–5):490–496. PMID: 20026023. [cohort]

6. Travison TG, Zhuang WV, Lunetta KL, et al. "Calculated free testosterone in men: comparison of four equations and with free androgen index." *Clin Endocrinol (Oxf).* 2007;66(5):652–658. PMID: 17036414. [cohort]

6b. Rosner W, Auchus RJ, Azziz R, Sluss PM, Raff H. "Position statement: Utility, limitations, and pitfalls in measuring testosterone: an Endocrine Society position statement." *J Clin Endocrinol Metab.* 2007;92(2):405–413. PMID: 17090633. [regulatory]

7. Bhasin S, Brito JP, Cunningham GR, et al. "Testosterone Therapy in Men With Hypogonadism: An Endocrine Society Clinical Practice Guideline." *J Clin Endocrinol Metab.* 2018;103(5):1715–1744. PMID: 29562364. [regulatory]

8. Jasuja R, Pencina KM, Spencer DJ, et al. "Reference intervals for free testosterone in adult men measured using a standardized equilibrium dialysis procedure." *Andrology.* 2023;11(1):125–133. DOI: 10.1111/andr.13310. [cohort]
