# Section C: Measurement & Interferences

## The Core Measurement Challenge

Free T3 (fT3) circulates at remarkably low concentrations — roughly 2–6 pmol/L (approximately 1.3–3.9 pg/mL) — which is several-fold lower than free T4 and far lower than total T3 or total T4 [1, mechanism_review]. This picomolar range creates a fundamental analytical problem: any minor matrix perturbation, protein-binding artifact, or cross-reacting species introduces a proportionally large error in the reported free fraction. As Westbye et al. noted, T3 concentrations are roughly ten-fold lower than T4, meaning "measuring T3 has always presented a greater sensitivity and precision challenge than measuring T4" [1, mechanism_review].

**Reference method.** The gold standard for fT3 measurement is equilibrium dialysis (ED) or ultrafiltration to physically separate the free fraction, followed by quantification via isotope-dilution liquid chromatography–tandem mass spectrometry (ID-LC-MS/MS). This approach avoids binding-protein matrix effects that confound immunoassays and is not susceptible to antibody cross-reactivity or endogenous binding protein variation [1, mechanism_review]. Labcorp's Endocrine Sciences laboratory, for example, offers fT3 by dialysis/LC-MS/MS as its highest-fidelity option. The key limitation of ED/LC-MS/MS is complexity and cost, rendering it impractical for routine high-throughput clinical use.

**Routine immunoassays.** The vast majority of clinical laboratories use analog one-step automated immunoassays that estimate fT3 indirectly. These assays introduce a labeled T3 analog into serum and infer the free fraction from competition kinetics — without physically separating the free hormone. Because they do not remove binding proteins before measurement, they are sensitive to any factor that alters the T3/protein equilibrium in the sample [2, mechanism_review]. Welsh and Soldin documented that multiple studies found "falsely normal values for T3, FT3 and FT4 by immunoassay that are below the reference interval when measured by ultrafiltration LC-MS/MS," highlighting systematic immunoassay bias relative to the reference method [1, mechanism_review].

**Imprecision at low concentrations.** Modern fT3 immunoassays have improved: Lin (2024) reported within-run imprecision of approximately 2.0% CV for fT3, somewhat better than total T3 (~3.3% CV) [3, mechanism_review]. However, these precision estimates apply to the central assay range; imprecision increases substantially at the low end — the very range that matters for detecting hypothyroidism or tracking illness-driven suppression.

## Total T3 versus Free T3: When to Use Each

Because fT3 immunoassays are imprecise at low concentrations and susceptible to protein-binding artifacts, total T3 (tT3) is sometimes preferred — particularly for detecting hyperthyroidism [1, mechanism_review]. In hyperthyroid states, both total and free T3 are substantially elevated, and the signal-to-noise ratio favors total T3 on many platforms. Clinical utility of T3 measurement (in any form) is highest for: (a) T3 toxicosis, where TSH is suppressed and fT4 is normal or low but T3 is disproportionately elevated; and (b) early or subclinical hyperthyroidism where fT4 remains within range [3, mechanism_review]. Lin's institutional audit found T3 thyrotoxicosis occurred in only 1.6% of cases with concurrent TSH/fT4/fT3 results, supporting selective rather than reflex T3 ordering [3, mechanism_review].

For hypothyroidism monitoring, neither fT3 nor tT3 adds meaningful diagnostic information beyond TSH and fT4 in most patients. The major textbook of thyroid assay methodology explicitly states that T3 measurements "have no value for diagnosing or monitoring treatment for hypothyroidism" [1, mechanism_review]. Free T3 becomes clinically relevant in hypothyroidism primarily when investigating combination T4/T3 replacement therapy outcomes.

## Interferences

### Biotin (Vitamin B7)

Excess circulating biotin interferes with streptavidin-biotin capture systems that most automated immunoassays employ. In competitive fT3 assays (one-step platforms), excess biotin displaces the biotinylated capture complex, causing **falsely elevated** fT3 results. The direction of interference in TSH sandwich assays is opposite — biotin causes falsely low TSH [4, mechanism_review]. Platform dependency is critical: Roche Cobas platforms are affected across TSH, fT4, and fT3; Beckman platforms primarily affect fT4/fT3; Ortho platforms primarily affect TSH [4, mechanism_review]. Patients taking high-dose biotin supplements (≥10 mg/day or higher, as used in multiple sclerosis trials) should discontinue biotin for at least 48 hours before thyroid function testing.

### Heterophile Antibodies and Anti-Animal Antibodies

Human anti-mouse antibodies (HAMA) and other heterophile antibodies can cross-link assay antibodies, producing falsely elevated or falsely low results depending on assay architecture. Two-site sandwich assays (used for TSH) are more susceptible than competitive immunoassays used for fT3 [4, mechanism_review]. However, heterophile antibody interference in fT3 assays has been documented and can cause clinically significant elevation.

### Anti-Streptavidin and Anti-Ruthenium Antibodies

Endogenous antibodies directed against streptavidin (a capture reagent) or ruthenium (an electrochemiluminescence label used in Roche Cobas platforms) interfere in a manner that mimics biotin effect but via different mechanisms. Anti-streptavidin antibodies typically cause decreased TSH with elevated fT4/fT3; effects can persist for 18–24 months after initial detection. Anti-ruthenium antibody effects are more heterogeneous — typically elevated fT4/fT3 with decreased TSH but can be reversed — and may not be correctable by standard blocking reagents [4, mechanism_review]. Favresse et al. (2018) reported that ≥50% of documented thyroid interferences led to misdiagnosis or inappropriate management, underscoring the clinical stakes of these analytical pitfalls [4, mechanism_review].

### Anti-T3 Autoantibodies

Autoantibodies against T3 are a specific and often underrecognized fT3 pitfall. Their effect on immunoassay results depends critically on assay design:

- **One-step (competitive) assays:** Anti-T3 autoantibodies bind both the endogenous T3 and the labeled analog tracer, causing **falsely elevated** fT3 results — sometimes dramatically so, leading to a clinical picture resembling T3 toxicosis [5, mechanism_review].
- **Two-step assays:** Because patient serum and labeled tracer do not contact each other simultaneously, two-step formats are largely insensitive to anti-T3 autoantibodies, and measured fT3 is falsely low or undetectable [4, mechanism_review].

This assay-design dependency means discordant fT3 results across platforms — or fT3/TSH dissociation — should prompt investigation for anti-T3 autoantibodies. Courcelles et al. (2023) documented a case of falsely elevated T3 on two different immunoassay platforms (Roche Cobas 8000 and Abbott Architect i2000), ultimately identified via radioimmunoprecipitation and PEG precipitation [6, mechanism_review]. Detection is confirmed by repeating the assay after polyethylene glycol precipitation or by direct measurement using ED/LC-MS/MS, which is immune to antibody interference.

### Drugs Displacing T3 from Binding Proteins

Several commonly used drugs compete with T3 for binding sites on thyroid-binding globulin (TBG), albumin, and transthyretin, artificially raising the apparent free T3 fraction in immunoassays [2, mechanism_review]:

- **Furosemide** (doses >80 mg/day, especially IV): displaces T4 and T3 from TBG and albumin
- **Salicylates and NSAIDs**: compete for binding sites
- **Phenytoin**: displaces thyroid hormones and may additionally reduce total hormone concentrations
- **Heparin**: activates lipoprotein lipase, releasing free fatty acids that displace T3/T4 from binding proteins; effect appears within 2–15 minutes and is an in vitro artifact of sample handling, not an in vivo phenomenon [2, mechanism_review]
- **Amiodarone**: inhibits D1-mediated T4-to-T3 conversion, lowering fT3 via a physiological (not assay) mechanism

### Abnormal Binding Proteins

Conditions that alter TBG, albumin, or transthyretin concentrations or binding affinity — including familial dysalbuminaemic hyperthyroxinaemia (FDH), TBG excess or deficiency, and hypoalbuminaemia — can cause divergence between immunoassay-measured fT3 and the true free fraction [2, mechanism_review]. Reference methods (ED/LC-MS/MS) are unaffected because they physically remove binding proteins before quantification.

## Non-Thyroidal Illness Syndrome (NTIS): The Dominant Confounder

The largest source of low fT3 outside true thyroid disease is non-thyroidal illness syndrome (NTIS), also termed the euthyroid sick syndrome or low-T3 syndrome. During systemic illness, caloric restriction, or fasting, fT3 can fall substantially while TSH remains normal or slightly suppressed — a pattern that can be mistaken for central hypothyroidism or subclinical hypothyroid-T3 deficiency if the clinical context is not considered [7, mechanism_review; 8, mechanism_review].

**Mechanism.** Two deiodinase changes drive NTIS:
1. **D1 (type 1 deiodinase) downregulation** in liver and skeletal muscle reduces the peripheral conversion of T4 to the active T3 — the dominant pathway for circulating T3 production [7, mechanism_review].
2. **D3 (type 3 deiodinase) upregulation** — particularly in critical illness — inactivates both T4 and T3 by converting them to reverse T3 (rT3) and other inactive iodothyronines [7, mechanism_review; 8, mechanism_review].

The net result is low serum T3 (both total and free), often with elevated rT3. Note, however, that rT3 elevation is not universal: Fliers and Boelen (2021) caution that rT3 "may be normal or even reduced in some NTIS cases," particularly in prolonged critical illness [7, mechanism_review].

**Fasting and caloric restriction.** Even in healthy individuals, fasting reduces serum T3 within 24–48 hours, with decreases proportional to the severity and duration of energy restriction. Very low calorie diets, prolonged fasting, and ketogenic diets all suppress T3 via D1 inhibition — a normal adaptive response to reduce metabolic rate during energy deficit [8, mechanism_review]. This means any fT3 value obtained during active weight loss, illness, or hospitalization must be interpreted with caution; it reflects the sum of thyroid secretion AND peripheral deiodination status, not thyroid gland function alone.

**Sample handling.** fT3 immunoassays require serum or lithium heparin plasma in plastic transport tubes; EDTA, oxalate, and citrate anticoagulants are contraindicated. Sample stability is limited, and prolonged room-temperature exposure or lipemia can alter results on some platforms.

## Standardization Status

The IFCC Committee for Standardization of Thyroid Function Tests (C-STFT) has developed a conventional reference measurement procedure (cRMP) for fT4 based on equilibrium dialysis + ID-LC-MS/MS, and has indicated the same framework extends to fT3 [IFCC C-STFT website]. However, fT3 standardization lags fT4: the fT3 reference procedure is less mature, inter-laboratory harmonization is substantially worse than for TSH or fT4, and no widely adopted certified reference material for fT3 currently exists. The consequence is that reported fT3 reference intervals and absolute values are not directly comparable across laboratory platforms or between institutions — a point of particular importance when tracking individual patients across different laboratory systems.

---

## Bibliography

1. Welsh KJ, Soldin SJ. DIAGNOSIS OF ENDOCRINE DISEASE: How reliable are free thyroid and total T3 hormone assays? *Eur J Endocrinol.* 2016;175(6):R255–R263. PMID: 27737898. [mechanism_review]

2. Koulouri O, Moran C, Halsall D, Chatterjee K, Gurnell M. Pitfalls in the measurement and interpretation of thyroid function tests. *Best Pract Res Clin Endocrinol Metab.* 2013;27(6):745–762. PMID: 24275187. [mechanism_review]

3. Lin Y. To test or not to test? Clinical utility and considerations for triiodothyronine (T3) testing. *Academy of Diagnostics & Laboratory Medicine Scientific Short.* Published March 26, 2024. Available at: https://myadlm.org/science-and-research/scientific-shorts/2024/clinical-utility-and-considerations-for-triiodothyronine-testing. [mechanism_review]

4. Favresse J, Burlacu MC, Maiter D, Gruson D. Interferences With Thyroid Function Immunoassays: Clinical Implications and Detection Algorithm. *Endocr Rev.* 2018;39(5):830–850. PMID: 29982406. [mechanism_review]

5. Lewandowski KC, Dąbrowska K, Lewiński A. Case report: When measured free T4 and free T3 may be misleading. Interference with free thyroid hormones measurements on Roche® and Siemens® platforms. *Thyroid Res.* 2012;5(1):11. PMID: 23107155. [mechanism_review]

6. Courcelles L, Luyten U, Wauthier L, Verbeke N, Burlacu MC, Gruson D. Characterisation of an interference affecting the triiodothyronine measurement on two different immunoassays. *Acta Clin Belg.* 2023;78(5):406–409. PMID: 37042022. [mechanism_review]

7. Fliers E, Boelen A. An update on non-thyroidal illness syndrome. *J Endocrinol Invest.* 2021;44(8):1597–1607. PMID: 33320308. [mechanism_review]

8. Moura Neto A, Zantut-Wittmann DE. Abnormalities of Thyroid Hormone Metabolism during Systemic Illness: The Low T3 Syndrome in Different Clinical Settings. *Int J Endocrinol.* 2016;2016:2157583. PMID: 27803712. [mechanism_review]
