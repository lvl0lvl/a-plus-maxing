# Section B: Reference Ranges, Tests, and the "Unreliable Test" Problem

## Units and Reference Intervals

Serum vitamin B12 (cobalamin) is reported in two unit systems: **pg/mL** (equivalently ng/L) and **pmol/L**. Conversion: **1 pg/mL = 0.738 pmol/L** — so 200 pg/mL ≈ 148 pmol/L and 900 pg/mL ≈ 664 pmol/L. Most laboratories use a reference range of roughly **200–900 pg/mL (148–664 pmol/L)**, though the exact interval varies by assay and population.

NICE guideline NG239 (2024) places confirmed-deficiency thresholds at **<180 ng/L (<133 pmol/L)** for total B12 and **<25 pmol/L** for active B12 (holotranscobalamin), with "deficiency unlikely" at **>350 ng/L (>258 pmol/L)** / **>70 pmol/L** respectively [1, regulatory].

---

## The Load-Bearing Problem: Why Total Serum B12 Is a Poor Diagnostic Test

Total serum cobalamin is the most-ordered first-line test for B12 deficiency. It is also, by a substantial body of evidence, a test with problematic sensitivity and specificity for true tissue-level deficiency [2, mechanism_review].

The core problem is biochemical: roughly 70–80% of circulating cobalamin is bound to haptocorrin (transcobalamin I), a metabolically inert transport protein — cells cannot take up haptocorrin-bound cobalamin via receptor-mediated endocytosis. Only the 20–30% bound to transcobalamin II ("active" fraction, measured as holotranscobalamin/holoTC) is bioavailable for cellular use [2, mechanism_review; 3, cohort]. Because the total assay measures both inert and active pools, a patient can have a normal-looking total B12 while tissues are functionally deficient. This structural mismatch produces false negatives (tissue-deficient patients with normal total B12) and less commonly false positives (elevated total B12 driven by haptocorrin with replete tissue stores).

### The Indeterminate Grey Zone

NICE NG239 [1, regulatory] formalises what clinicians have long observed: results between **180–350 ng/L (133–258 pmol/L)** for total B12, or **25–70 pmol/L** for active B12, constitute an **indeterminate result** — a grey zone where deficiency can be neither confirmed nor excluded on the index test alone. Carmel's 2011 *American Journal of Clinical Nutrition* review concluded that "reliance on one test alone courts frequent misdiagnosis" [2, mechanism_review].

The scale of the problem is quantified in Valente et al. (2011, *Clinical Chemistry*, n = 700 elderly subjects aged 63–97): **45% of participants fell in the indeterminate zone** on serum cobalamin alone, versus only 14% on holotranscobalamin — a threefold improvement [3, cohort]. Clarke et al. (2007, *Clinical Chemistry*, n = 2,403 older adults) found holoTC achieved AUC 0.85 vs. 0.76 for total B12 (p < 0.001) in detecting MMA-confirmed deficiency [4, cohort]. Stabler's 2013 *New England Journal of Medicine* clinical practice review — the most-cited English-language overview — acknowledges that current serum cobalamin assays have "insufficient sensitivity and specificity" and recommends methylmalonic acid as the functional confirmatory test [5, mechanism_review].

---

## The Functional Markers

### Holotranscobalamin (HoloTC / "Active B12")

HoloTC is the transcobalamin II-bound fraction — the only portion taken up by cells via receptor-mediated endocytosis and available for enzymatic function. Because the body depletes this active pool before total serum B12 falls measurably, **holoTC is an earlier marker of negative B12 balance** than total B12 [3, cohort; 4, cohort].

Valente et al. (2011, *Clin Chem*, n = 700 elderly subjects aged 63–97) found holoTC achieved AUC 0.90 (95% CI 0.86–0.93) vs. 0.80 for serum cobalamin and 0.78 for MMA against an erythrocyte cobalamin reference standard [3, cohort]. Critically, only 14% of participants fell in the holoTC indeterminate zone (20–30 pmol/L) vs. 45% on serum cobalamin alone — a threefold reduction in diagnostic ambiguity [3, cohort]. Clarke et al. (2007, *Clin Chem*, n = 2,403 older adults) confirmed the superiority of holoTC over total B12 for detecting MMA-confirmed deficiency: AUC 0.85 vs. 0.76 overall (p < 0.001), with consistent superiority in both normal-renal-function (AUC 0.87 vs. 0.79) and impaired-renal-function (AUC 0.85 vs. 0.74) subgroups [4, cohort]. NICE NG239 [1, regulatory] recognises HoloTC as an equivalent first-line alternative to total B12, and the preferred test during pregnancy (where total B12 is unreliable).

### Methylmalonic Acid (MMA)

MMA is the most **specific functional marker** of cellular B12 deficiency available in routine practice. Mechanism: adenosylcobalamin is the required cofactor for methylmalonyl-CoA mutase; when depleted, MMA accumulates in blood and urine, directly reflecting impaired mitochondrial one-carbon flux [2, mechanism_review; 5, mechanism_review].

**Critical caveat: MMA also rises in renal impairment**, independent of B12 status, because reduced GFR slows MMA clearance. Clarke et al. [4, cohort] found renal dysfunction substantially compromised MMA's diagnostic accuracy while leaving holoTC and total B12 unaffected. MMA must be interpreted alongside eGFR or serum creatinine; it is not a standalone marker in patients with established renal impairment. Inborn errors of propionate metabolism produce an additional confound.

### Total Homocysteine (tHcy)

Homocysteine accumulates when remethylation fails — a process requiring methylcobalamin (B12), folate (as 5-methyltetrahydrofolate), and vitamin B6. This **three-way dependence makes tHcy a sensitive but non-specific marker**: elevated homocysteine cannot distinguish B12 deficiency from folate deficiency, B6 deficiency, or renal impairment [2, mechanism_review]. Valente et al. found homocysteine achieved AUC 0.78 — lower than holoTC (0.90) — consistent with its limited specificity [3, cohort]. Its clinical utility is as a confirmatory second-line test when MMA is unavailable, and in the B12–folate differential (isolated folate deficiency raises homocysteine but not MMA). NICE NG239 [1, regulatory] recommends accounting for folate status when interpreting tHcy results — an important caution given that folate supplementation can correct the anaemia of B12 deficiency while leaving neurological injury to progress.

---

## The Diagnostic Algorithm

NICE NG239 [1, regulatory] and Carmel [2, mechanism_review] converge on a stepwise approach:

1. **First-line:** Total B12 or active B12 (holoTC), clinician's or laboratory's choice. Pregnancy: holoTC only.
2. **Indeterminate / grey-zone result:** Add **serum MMA** as the functional confirmatory test. Plasma homocysteine is an alternative when MMA is unavailable, with lower specificity.
3. **Interpret MMA with renal function in view.** Elevated MMA with normal eGFR in a grey-zone patient is strong evidence of tissue deficiency; elevated MMA with impaired eGFR is inconclusive.
4. **B12 deficiency is a combined clinical and biochemical diagnosis.** No single biomarker suffices. Deficiency should not be ruled out solely on the basis of absent anaemia or absent macrocytosis — neurological presentations can precede haematological changes.

The serum B12 assay remains the appropriate starting point: it is inexpensive, widely available, and highly informative at the extremes. The problem lives in the middle — the grey zone estimated to encompass up to 45% of samples in elderly populations [3, cohort] — and that is exactly where a functional marker (MMA ± holoTC) is not optional.

---

## Bibliography

1. National Institute for Health and Care Excellence (NICE). *Vitamin B12 deficiency in over 16s: diagnosis and management*. NICE Guideline NG239. London: NICE; 2024. https://www.nice.org.uk/guidance/ng239 — tag: regulatory — tier: 1

2. Carmel R. Biomarkers of cobalamin (vitamin B-12) status in the epidemiologic setting: a critical overview of context, applications, and performance characteristics of cobalamin, methylmalonic acid, and holotranscobalamin II. *Am J Clin Nutr*. 2011;94(1):348S–358S. PMID: 21593511. DOI: 10.3945/ajcn.111.013441 — tag: mechanism_review — tier: 1

3. Valente E, Scott JM, Ueland P-M, Cunningham C, Casey M, Molloy AM. Diagnostic accuracy of holotranscobalamin, methylmalonic acid, serum cobalamin, and other indicators of tissue vitamin B12 status in the elderly. *Clin Chem*. 2011;57(6):856–863. PMID: 21482749. DOI: 10.1373/clinchem.2010.158154 — tag: cohort — tier: 1

4. Clarke R, Sherliker P, Hin H, et al. Detection of vitamin B12 deficiency in older people by measuring vitamin B12 or the active fraction of vitamin B12, holotranscobalamin. *Clin Chem*. 2007;53(5):963–970. PMID: 17363419. DOI: 10.1373/clinchem.2006.080382 — tag: cohort — tier: 1

5. Stabler SP. Clinical practice. Vitamin B12 deficiency. *N Engl J Med*. 2013;368(2):149–160. PMID: 23301732. DOI: 10.1056/NEJMcp1113996 — tag: mechanism_review — tier: 1
