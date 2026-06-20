---
title: "AST (Aspartate Aminotransferase): Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/ast/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.ast-design-work
provenance_slug: labs-specialist
source_count: 31
---

# AST (Aspartate Aminotransferase): Canonical Research Report

## Summary

Aspartate aminotransferase (AST; EC 2.6.1.1) is a pyridoxal-5′-phosphate (PLP, active vitamin B6)-dependent enzyme that catalyzes the reversible transamination of L-aspartate and α-ketoglutarate to oxaloacetate and L-glutamate — a reaction at the intersection of amino acid catabolism, gluconeogenesis, and the malate-aspartate shuttle. Results are reported in U/L (= IU/L). The defining interpretive fact about AST is that it is a **multi-organ enzyme, less liver-specific than ALT**: high catalytic activity is present in hepatocytes, cardiac myocytes, skeletal muscle, red blood cells (RBCs), kidney tubules, neurons, and pancreas. Because of this broad distribution, serum AST elevation cannot be attributed to the liver without co-interpreting ALT, creatine kinase (CK), and hemolysis status.

The central clinical tool for AST interpretation is the **De Ritis ratio** (AST÷ALT), introduced by Fernando De Ritis in 1957. A ratio >2 is the hallmark of alcoholic liver disease (ALD), driven by alcohol-induced mitochondrial injury releasing the mitochondrial AST isoform (mAST/GOT2) and by chronic vitamin B6 depletion that suppresses ALT more than AST [6, cohort; 11, cohort]. A ratio <1 characterizes MASLD and acute viral hepatitis, where cytoplasmic AST release predominates and ALT's longer plasma half-life (~35 hours vs. AST's ~16 hours) keeps it numerically higher [7, cohort]. A ratio rising above 1 in chronic liver disease of any cause signals advancing fibrosis and cirrhosis as hepatocyte mass is progressively replaced by scar [10, cohort; 12, cohort; 13, cohort]. Beyond liver disease, the De Ritis ratio has been validated as a prognostic marker for all-cause and cardiovascular mortality in general elderly populations (adjusted HR 1.68, 95% CI 1.47–1.91 for all-cause; adjusted HR 1.67, 95% CI 1.27–2.20 for cardiovascular) [31, cohort], in stable coronary artery disease (adjusted HR 1.27 per unit, 95% CI 1.09–1.48; p = 0.002) [28, cohort], and in post-AMI survivors (adjusted HR 1.23 per 1-SD, 95% CI 1.07–1.42; p = 0.004) [29, cohort].

A critical pre-analytic pitfall unique to AST is **hemolysis**: erythrocytes contain approximately 40-fold more AST than serum, so even mild in vitro hemolysis causes spurious AST elevation with little effect on ALT — artifactually raising the De Ritis ratio [18, cohort; 19, cohort]. A second important mimic is **macro-AST**, a benign condition in which AST forms high-molecular-weight complexes with immunoglobulins, extending its plasma half-life and producing persistently elevated AST with normal ALT, CK, GGT, and liver imaging [15, mechanism_review]. Confirmation uses polyethylene glycol (PEG) precipitation: a post-precipitation AST recovery ≤40% confirms macro-AST [15, mechanism_review]. The IFCC reference measurement procedure adds exogenous PLP to the assay, correcting for apoenzyme fraction in B6-deficient patients — but more than 60% of US laboratories omit this supplement, making full metrological standardization unachievable on those platforms [16, mechanism_review; 17, mechanism_review].

Conventional adult ULN clusters around 35–40 U/L (sex-dependent, men higher), but these thresholds are derived from unscreened populations and should be interpreted alongside the ×ULN bands defined in major guidelines: borderline (<2×), mild (2–5×), moderate (5–15×), marked (>15×), and massive (>10,000 U/L, essentially diagnostic of ischemic hepatopathy or toxin) [8, regulatory]. AST must always be interpreted WITH ALT, CK, hemolysis status, and the De Ritis ratio — never in isolation.

---

## Physiology & What AST Measures

### The Reaction and Isoenzymes

Aspartate aminotransferase (AST; EC 2.6.1.1) — historically designated SGOT (serum glutamic-oxaloacetic transaminase) or GOT — catalyzes the reversible transamination:

> **L-aspartate + α-ketoglutarate ⇌ oxaloacetate + L-glutamate**

PLP is covalently bound at the active site via a Schiff base with a lysine residue and serves as the direct amino-group carrier during transamination [1, mechanism_review]. This PLP-dependence has a key clinical implication: vitamin B6 depletion — common in heavy alcohol use, dialysis, and chronic inflammatory states — reduces aminotransferase activity, and because hepatic ALT is more acutely sensitive to PLP depletion than AST, ALT activity is preferentially suppressed, raising the observed AST/ALT ratio upward [6, cohort].

AST exists as **two genetically and immunologically distinct isoenzymes** encoded by separate nuclear genes:

| Isoenzyme | Gene | Chromosomal location | Subcellular compartment |
|-----------|------|---------------------|------------------------|
| Cytosolic AST (cAST, AST1) | *GOT1* | Chromosome 10q24.2 | Cytoplasm |
| Mitochondrial AST (mAST, AST2) | *GOT2* | Chromosome 16q21 | Mitochondrial matrix |

Both are homodimeric class-I PLP-dependent aminotransferases [1, mechanism_review; 2, mechanism_review]. The cytosolic isoform (GOT1) dominates routine serum assays under most circumstances; the mitochondrial isoform (GOT2) enters the circulation in appreciable quantities only when hepatocyte necrosis is severe enough to disrupt mitochondrial membranes [2, mechanism_review]. In alcoholic hepatitis, the mAST:cAST ratio in serum is elevated relative to viral hepatitis — reflecting mitochondrial susceptibility to ethanol — whereas in uncomplicated viral hepatitis, cAST release dominates.

### Role in the Malate-Aspartate Shuttle

Beyond amino acid metabolism, the AST reaction is a core component of the **malate-aspartate shuttle (MAS)** — the primary mechanism by which cytosolic NADH reducing equivalents generated during glycolysis cross the inner mitochondrial membrane (which is impermeable to NADH) [3, mechanism_review]:

1. **Cytosol (MDH1):** Oxaloacetate + NADH → malate + NAD⁺
2. Malate enters the mitochondrion; mitochondrial MDH2 converts it back to oxaloacetate, reducing mitochondrial NAD⁺ → NADH for the respiratory chain
3. **Mitochondrial matrix (GOT2):** Oxaloacetate + glutamate → aspartate + α-ketoglutarate
4. Aspartate exits via the aspartate-glutamate carrier (electrogenic — driven by the mitochondrial proton gradient)
5. **Cytosol (GOT1):** Aspartate + α-ketoglutarate → oxaloacetate + glutamate, regenerating oxaloacetate for step 1

GOT2 loss-of-function mutations in humans produce a severe neonatal encephalopathy with epilepsy, progressive microcephaly, hyperlactatemia, and elevated citrulline — direct evidence that GOT2 is non-redundant and indispensable for maintaining cytoplasmic redox homeostasis and mitochondrial aspartate supply [1, mechanism_review; 2, mechanism_review]. GOT1 deficiency produces a distinct, milder phenotype (familial macro-AST with persistent serum elevation but no organ pathology) reflecting the different metabolic role of the cytosolic compartment.

### Tissue Distribution: Why AST Is Less Liver-Specific Than ALT

The central interpretive challenge with serum AST is its **broad multi-organ expression**. High AST catalytic activity is present in:

- Hepatocytes (liver)
- Cardiac myocytes
- Skeletal muscle
- Red blood cells (erythrocytes)
- Kidney tubular epithelium
- Brain neurons
- Pancreas

In quantitative terms, AST activity in myocardial and skeletal muscle tissue is comparable to — or exceeds — hepatic concentrations, meaning that injury to any of these tissues elevates serum AST [4, cohort; 5, cohort]. In a large multi-center study of COVID-19, AST elevations could be fully explained by the summed contributions of hepatocellular injury (~67%) and skeletal/cardiac muscle damage (~43%), with neither source dominant — a direct empirical illustration of multi-tissue origin [5, cohort].

By contrast, **ALT** is expressed at roughly 3,000-fold higher activity in hepatocyte cytosol than in any other tissue. Non-hepatic ALT concentrations are low enough that ALT elevation in the absence of muscle markers almost always reflects hepatocellular injury. This difference in tissue specificity is the biochemical foundation for the clinical dictum: **ALT is the more liver-specific enzyme; AST is the more sensitive but less specific marker of cellular injury across multiple organs** [4, cohort; 5, cohort].

### Plasma Half-Life: The Kinetic Basis of AST/ALT Patterns

Using first-order kinetic modeling applied to 6.5 million transaminase measurements in over 91,000 patients, Sherman and Goessling (2024) derived:

- **AST plasma half-life: ~15.8 hours** (clearance rate 1.13 day⁻¹)
- **ALT plasma half-life: ~34.6 hours** (clearance rate 0.47 day⁻¹)

AST is cleared from blood at more than twice the rate of ALT [7, cohort]. Following acute hepatocellular injury, both enzymes rise rapidly, but as injury resolves, **AST falls faster than ALT**. Consequently, in any setting where AST remains elevated relative to ALT — or where AST/ALT >2 — it implies either: (a) ongoing or severe injury that releases AST faster than it clears, (b) a non-hepatic source (cardiac or skeletal muscle), or (c) disproportionate mAST release from mitochondrial disruption as in alcoholic liver disease. The mitochondrial isoform (mAST/GOT2) has a substantially longer serum retention time than cytosolic AST, as it is released only with necrotic injury and is subsequently complexed with other cellular proteins that slow clearance.

---

## Reference Ranges, Units & The De Ritis Ratio

### Units and Conventional Reference Ranges

AST activity is reported in **U/L** (units per litre), which is numerically identical to IU/L and the SI-compliant kU/L × 1000. Results from different laboratories are not interchangeable without assay harmonization because AST lacks a commutable international reference material; method- and analyser-specific ULNs therefore vary [8, regulatory].

Conventional adult reference intervals reported by major clinical laboratories cluster around **17–40 U/L for women** and **17–50 U/L for men**, though published values differ modestly across assay platforms. A large cross-sectional analysis of more than 1.3 million consecutive blood samples confirmed significant sex dependence: the 95th-percentile for women younger than 50 is approximately 40 U/L, rising to ~45 U/L by age 60, while men's 95th percentile generally sits higher throughout adulthood before declining after age 60 [9, cohort]. The 2017 ACG Clinical Guideline uses 35 U/L (women) and 50 U/L (men) as working ULNs, but emphasizes that local laboratory reference intervals take precedence [8, regulatory].

Unlike ALT, for which evidence-based lower thresholds (~19–25 U/L in healthy women; ~29–33 U/L in men) have been proposed after careful exclusion of metabolic confounders, AST has received less attention as a standalone marker and the case for revising its ULN downward is less robustly studied [8, regulatory].

**Age and sex dependence are real but modest for AST.** Reference intervals are method- and population-specific; direct comparison across laboratories without standardization is unreliable [9, cohort].

### Elevation Bands (×ULN)

| Category | AST (×ULN) | Clinical implications |
|---|---|---|
| Borderline | < 2× | Isolated finding; recheck and investigate cause if persistent |
| Mild | 2–5× | Broad differential; include MASLD, ALD, drugs, thyroid, muscle |
| Moderate | 5–15× | Acute hepatocellular injury; more urgent evaluation warranted |
| Marked | > 15× | Acute viral hepatitis, ischemic hepatitis, toxin, Wilson's; AST may reach thousands |
| Massive | > 10,000 U/L | Ischemic hepatitis, acute acetaminophen toxicity |

These tiers are adapted from the ACG 2017 guideline categories, which were defined for ALT but are applied to AST in the same framework [8, regulatory]. At the marked-to-massive end, AST often rises faster and higher than ALT because of its mitochondrial isoform contribution and greater hepatic abundance; absolute levels above 1,000–3,000 U/L point strongly toward ischemic, toxin, or acute viral aetiology rather than chronic liver disease [8, regulatory; 10, cohort].

### The De Ritis Ratio

Introduced by Fernando De Ritis in 1957, the **AST÷ALT ratio** (De Ritis ratio) integrates both the tissue-distribution and kinetic differences between the enzymes into a single clinically actionable number. The ratio must be calculated whenever AST is abnormal; it substantially shifts the differential diagnosis.

#### Ratio > 2 — Strongly Suggests Alcoholic Liver Disease

A ratio consistently above **2** is the classic fingerprint of **alcoholic liver disease (ALD)**. The mechanism is dual: (1) ethanol metabolism and its aldehyde intermediates accelerate catabolism of PLP, the vitamin B6 cofactor. Because hepatic ALT is more acutely sensitive to PLP depletion than AST, ALT activity is preferentially suppressed, raising the ratio. (2) Alcohol-induced mitochondrial membrane injury causes disproportionate release of the mitochondrial isoform (mAST/GOT2).

The landmark study by Nyblom et al. (2004) examined three patient cohorts and found that a **high AST/ALT ratio indicates advanced alcoholic liver disease rather than simply heavy drinking** — patients with severe alcoholic hepatitis or cirrhosis drove the ratio elevation, not those with harmful alcohol use without significant hepatic injury [11, cohort]. A ratio ≥2 therefore flags *established hepatic injury* from alcohol, not merely alcohol exposure. Williams and Hoofnagle (1988) corroborated this in a series of 177 patients with chronic hepatitis: the AST/ALT ratio exceeds 2 in the great majority of ALD cases, whereas in non-alcoholic chronic hepatitis it typically stays below 1 [10, cohort]. In a matched case-control study (N = 70 NASH vs. 70 ALD), Sorbi, Boynton, and Lindor found a mean AST:ALT ratio of 2.6 in ALD versus 0.9 in NASH (p < 0.000001); a ratio ≥2 was strongly suggestive of ALD [24, cohort]. Diehl et al. (1984) provided the mechanistic evidence: in 12 patients with biopsy-confirmed alcoholic hepatitis, in vitro addition of PLP to liver homogenates rescued ALT activity but not AST activity; after one month of abstinence and B6 repletion, serum ALT rose and serum AST fell, significantly normalizing the ratio [6, cohort].

**Caution:** If AST/ALT >2 accompanies AST >1,000 U/L, reassess the aetiology — ischemic hepatitis, acute viral hepatitis, or toxin can all produce this pattern even when ALD is suspected.

#### Ratio < 1 — Typical of MASLD/NAFLD and Acute Viral Hepatitis

When the ratio is below **1** — ALT exceeds AST — the pattern favours **metabolic-associated steatotic liver disease (MASLD, formerly NAFLD)** or **acute viral hepatitis**. In MASLD, preserved hepatocyte mass with cytoplasmic rather than mitochondrial predominance keeps ALT activity disproportionately high. In acute viral hepatitis, cytoplasmic AST release is high but ALT release is proportionally higher still [10, cohort].

#### Ratio > 1 in Chronic Liver Disease — Suggests Advancing Fibrosis or Cirrhosis

In established chronic liver disease of any aetiology, a ratio that has **risen above 1** should prompt reassessment for fibrosis progression. Williams and Hoofnagle demonstrated that among chronic hepatitis B patients, the mean ratio was **0.59 without cirrhosis versus 1.02 with cirrhosis** — a statistically significant separation [10, cohort]. Nyblom et al. extended this to **primary biliary cholangitis (PBC)**: an AST/ALT ratio ≥1 was a strong predictor of liver-related death or need for transplantation (nearly fourfold higher risk), and correlated with histological cirrhosis [12, cohort]; the same group found the ratio elevated above 1 in cirrhotic patients with **primary sclerosing cholangitis (PSC)** [13, cohort]. In a cohort of chronic HBV-infected patients, an elevated AST:ALT ratio was associated with higher risk of cirrhosis development (HR = 2.77, p = 8.25 × 10⁻⁴) [23, cohort]. The mechanism: as hepatocyte mass is destroyed by progressive fibrosis, residual ALT-producing hepatocytes are preferentially lost, while AST continues to be released from surviving cells and non-hepatic sources.

**Practical De Ritis thresholds summary:**

| Ratio | Pattern |
|---|---|
| < 1 | MASLD, acute viral hepatitis |
| 1–2 | Non-specific; cirrhosis possible; chronic hepatitis |
| > 2 (AST usually < 300 U/L) | ALD — advanced injury; also seen in advanced cirrhosis of any cause |
| > 2 (AST > 1,000 U/L) | Re-evaluate: likely ischemic, acute hepatitis, or toxin even if ALD suspected |

### The Essential Co-Interpretation Requirement: CK

An isolated AST elevation without a concurrent ALT elevation should trigger immediate measurement of **creatine kinase (CK)**:

- **Elevated AST + elevated CK, normal ALT** → skeletal or cardiac muscle source (rhabdomyolysis, myopathy, strenuous exercise, myocardial infarction)
- **Elevated AST + normal CK, elevated ALT** → hepatocellular injury
- **Elevated AST + normal CK, normal ALT** → consider macro-AST (see Measurement section), hemolysis, or thyroid disease

Dufour (1988) formalized the **CK:AST ratio** as a discriminator between cardiac and skeletal muscle sources of elevated CK: because skeletal muscle contains more CK and proportionally less AST than cardiac muscle, lower CK:AST ratios (< 14 when total CK is 300–1,200 U/L) pointed toward myocardial infarction with 95% sensitivity [14, mechanism_review]. **AST must never be interpreted in isolation from ALT and CK**; the trio together narrows the source differential far more reliably than any single enzyme alone.

---

## Measurement & Standardization

### The IFCC Reference Measurement Procedure

The IFCC reference measurement procedure for AST was published by Schumann et al. as Part 5 of the primary reference series for enzyme activity at 37°C [16, mechanism_review]. The procedure specifies: serum or plasma; reaction temperature 37°C; supplementation with **pyridoxal-5′-phosphate (P5P)** at 0.1 mmol/L, with a preincubation phase to reconstitute the apoenzyme before substrate addition [16, mechanism_review].

The P5P requirement is load-bearing. A portion of circulating AST exists as the inactive apoenzyme (cofactor-free). In populations with subclinical B6 deficiency — patients with acute myocardial infarction, chronic renal disease, inflammatory states, or alcohol use — this apoenzyme fraction is enlarged, and assays without P5P systematically underestimate true catalytic activity [17, mechanism_review]. Despite this, more than 60% of US laboratories and a similar proportion internationally still use aminotransferase assays without P5P supplementation, making full metrological traceability to the IFCC reference unachievable on those platforms [17, mechanism_review].

### The Coupled Enzymatic Assay (Reaction Principle)

The IFCC AST assay is a continuous kinetic indicator method [16, mechanism_review]. The primary (analytical) reaction is:

> L-aspartate + α-ketoglutarate → oxaloacetate + L-glutamate  (catalyzed by AST)

Oxaloacetate is detected via an indicator reaction with malate dehydrogenase (MDH) and NADH:

> Oxaloacetate + NADH + H⁺ → L-malate + NAD⁺  (catalyzed by MDH)

Because NADH absorbs at 340 nm and NAD⁺ does not, the reaction is measured as a continuous **decrease in absorbance at 340 nm**; ΔA₃₄₀/min is proportional to AST activity in U/L [16, mechanism_review]. Lactate dehydrogenase (LDH) is co-included to scavenge endogenous pyruvate, preventing spurious NADH consumption. MDH is added in excess to maintain linearity up to approximately 700 U/L.

### Hemolysis: A Dominant Pre-Analytic Interference

Hemolysis is the single most clinically significant pre-analytic interference for AST, and the effect is qualitatively different from its effect on ALT [18, cohort; 19, cohort]. The mechanism is direct: the **intracellular concentration of AST in red blood cells is approximately 40× higher than in serum/plasma** [18, cohort]. Erythrocyte lysis releases large quantities of AST into the sample.

The practical impact is quantified across multiple studies. At a hemolysis index (H-index) of 1+ (≈100 mg/dL free hemoglobin), AST rises by approximately 9.3% from baseline [18, cohort]. At severe hemolysis (plasma Hgb ~4.5 g/L), AST increases by roughly 30 U/L — a 2.5-fold rise above a low baseline — at levels below the threshold of visual detection [19, cohort]. Concentration-specific H-index thresholds have been developed: for AST values within the reference interval, an H-index up to 50–100 may be tolerable with an interpretive comment rather than outright rejection [20, open_label].

**ALT is largely immune to this effect.** Studies consistently find ALT percent differences from baseline of less than 3–5% across all clinically encountered hemolysis levels [18, cohort; 19, cohort]. Critically, hemolysis artifactually elevates the AST:ALT ratio — a major pitfall when the De Ritis ratio is used to distinguish alcoholic from non-alcoholic disease. Any elevated AST in a hemolyzed specimen must be flagged; if the elevation is isolated and unexplained, specimen recollection is required before clinical action.

### Macro-AST: Spurious Persistent Elevation

**Macro-AST** is a high-molecular-weight complex formed by the non-covalent binding of AST to a circulating immunoglobulin, most commonly IgG [15, mechanism_review]. The complex is too large for normal clearance, so AST activity accumulates in serum despite the absence of organ injury [15, mechanism_review].

The clinical signature is characteristic: AST elevated (sometimes markedly), ALT normal, all other organ-damage markers (ALP, GGT, bilirubin, CK, troponin) unremarkable. This pattern should trigger macro-AST testing rather than invasive workup.

**Detection** relies on **polyethylene glycol (PEG) precipitation**: PEG (20–25% w/v) precipitates immunoglobulins and their bound complexes. Residual supernatant AST activity **≤40%** of the pre-precipitation value (i.e., a drop of ≥60%) confirms macro-AST [15, mechanism_review]. Alternative approaches — ultrafiltration and protein-A/G immunodepletion — yield consistent results and can characterize the immunoglobulin class [15, mechanism_review].

An important interpretive nuance: P5P can reactivate the apoenzyme fraction within the macro-AST complex, so P5P-supplemented assays may measure higher macro-AST activity than non-supplemented assays. A laboratory's transition to an IFCC-compliant P5P platform can unmask or amplify macro-AST that was previously cryptic; PEG precipitation results should be interpreted using the same analytical method (with or without P5P) for both pre- and post-precipitation measurements [21, mechanism_review]. Macro-AST is a **benign finding** — once confirmed, no organ-directed treatment is required.

### Cytosolic vs. Mitochondrial Isoenzymes (Specialized Measurement)

Although hepatocytes contain approximately 80% mAST by total activity, **healthy serum is dominated by cAST**; mitochondrial AST is a minor fraction in the absence of severe or necrotic injury. Mild, reversible membrane damage releases cAST preferentially, while mAST release requires disruption of the inner mitochondrial membrane. Elevated mAST therefore signals severe injury — liver ischemia, acute necrosis, halothane hepatotoxicity. mAST can be selectively measured via immunoinhibition but lacks IFCC standardization and remains a specialized research tool.

### Sample Stability

Serum AST is robust to freeze-thaw cycling: no statistically significant change was found after ten freeze-thaw cycles at −20°C, and stability extended over three months of storage at −20°C [22, cohort]. For routine samples, separation within 1–2 hours and measurement within 24 hours at 2–8°C is standard. Severe lipemia can impair 340 nm absorbance measurement in instruments without bichromatic correction.

---

## Determinants & Clinical Significance

### Hepatic Elevation: The De Ritis Ratio as Diagnostic Context

AST is elevated in all major causes of hepatocellular injury, but its interpretation is almost never made in isolation. The De Ritis ratio (reviewed in the preceding section) encodes the pathophysiological source: because mitochondrial AST (mAST) constitutes roughly 80% of total intrahepatic AST, conditions that destroy mitochondria selectively (alcoholic hepatitis, advanced fibrosis, ischemia) raise the ratio; conditions that injure hepatocyte cytoplasm while sparing mitochondria (early MASLD, acute viral hepatitis) often drive ALT higher and lower the ratio [30, mechanism_review].

**Metabolic dysfunction-associated steatotic liver disease (MASLD).** In early MASLD, ALT typically exceeds AST (De Ritis ratio < 1.0), reflecting preferential cytosolic injury with intact mitochondria. As hepatic fibrosis develops and hepatocyte mass is replaced by fibrous tissue, mitochondrial leak increases and the ratio climbs toward or above 1; a ratio >1 in a patient with known MASLD is therefore a clinically useful signal of advancing disease [30, mechanism_review]. This ratio shift with fibrosis was confirmed in a chronic HBV cohort where an elevated AST:ALT ratio was associated with higher risk of cirrhosis development (HR = 2.77, p = 8.25 × 10⁻⁴) [23, cohort].

**Alcoholic liver disease (ALD).** A De Ritis ratio ≥2 is a hallmark of alcoholic hepatitis and more severe ALD. The dual mechanism is: (i) alcohol and its metabolite acetaldehyde directly damage mitochondria, releasing mAST; (ii) chronic alcohol use depletes pyridoxal-5′-phosphate (B6), a required cofactor for ALT synthesis, selectively suppressing ALT activity and widening the ratio. In a matched case-control study, Sorbi, Boynton, and Lindor found a mean AST:ALT ratio of 2.6 in ALD versus 0.9 in NASH (p < 0.000001) [24, cohort].

**Viral hepatitis, drug-induced, and ischemic hepatitis.** In acute viral hepatitis, both enzymes rise dramatically with ALT typically predominating (ratio <1). Drug/toxin-induced liver injury follows a similar pattern unless mitochondrial toxins (e.g., valproate, amiodarone) are involved. Ischemic hepatitis ("shock liver") produces the most dramatic absolute AST elevations of any liver condition, often exceeding 1,000–5,000 U/L within 24 hours, reflecting massive simultaneous cytosolic and mitochondrial release from hypoperfused hepatocytes.

### Non-Hepatic Sources: The Core Interpretive Challenge

#### Cardiac: Historical Significance, Supplanted by Troponin

In 1954, LaDue, Wroblewski, and Karmen reported that AST (then GOT) rose in serum within hours of acute myocardial infarction (AMI), initiating the era of enzyme-based cardiac diagnosis [25, mechanism_review]. The kinetic profile of AST in AMI: onset 12–24 h post-event, peak at 1–2 days, return to baseline by 10–14 days. However, AST is expressed abundantly in liver, skeletal muscle, and kidney — its cardiac specificity is therefore low. The development of CK-MB in the 1970s and cardiac troponins (cTnI, cTnT) in the 1990s rendered AST obsolete for cardiac diagnosis. Cardiac troponins are now the sole guideline-endorsed biomarkers for AMI [25, mechanism_review]. **AST is no longer used in the diagnosis of acute coronary syndromes.** Its historical cardiac role is noted because occasional incidental AST elevation in a perioperative or post-cardioversion context may be partly myocardial in origin.

#### Skeletal Muscle: The Most Clinically Relevant Non-Hepatic Source

Skeletal muscle is the single most important non-hepatic cause of AST elevation encountered in clinical practice. Any cause of muscle necrosis or hyperpermeability raises both AST and ALT — with AST rising disproportionately — making the De Ritis ratio an unreliable liver marker in this setting.

**Rhabdomyolysis** provides the clearest illustration. In a prospective series (N = 165) of patients with CK ≥1,000 U/L, 97.8% had peak AST above normal and 84.1% had peak ALT above normal; the median AST:ALT ratio was 2.5 [26, cohort]. This high ratio mirrors ALD numerically, making CK the essential differentiator — CK is massively elevated in rhabdomyolysis (often >10,000 U/L) and absent from hepatocytes at significant levels. **GGT provides an additional discriminator**: GGT is not expressed in skeletal muscle, so a normal GGT with elevated AST argues against a hepatic source.

Nathwani, Pais, Reynolds, and Kaplowitz demonstrated that AST and ALT are both elevated acutely in muscle necrosis (AST:ALT >3), but AST declines faster due to its shorter half-life, causing the ratio to fall toward 1 within days — without any underlying liver disease [27, cohort]. This established that elevated aminotransferases in skeletal muscle disease are not a sign of hepatocellular injury.

Other muscle sources: **strenuous eccentric exercise** (delayed-onset muscle damage), **inflammatory myopathies** (polymyositis, dermatomyositis), **muscular dystrophies** (Duchenne, limb-girdle), and **generalized tonic-clonic seizures** (convulsive myonecrosis). In these settings, AST may be elevated 3- to 10-fold above normal in the complete absence of liver disease.

#### Hemolysis

Erythrocytes are AST-rich and ALT-poor. Both in-vivo hemolysis (hemolytic anemia) and in-vitro hemolysis (traumatic venipuncture, delayed specimen processing) release erythrocyte AST into the plasma, producing a spuriously elevated AST with a disproportionately lower ALT. In true hemolytic anemia, concurrent elevation of lactate dehydrogenase (LDH), unconjugated bilirubin, and reticulocytosis — with reduced haptoglobin — clarifies the picture [30, mechanism_review].

#### Other Non-Hepatic Sources

**Thyroid disease.** Hypothyroidism elevates AST (and LDH) through two mechanisms: myopathy induced by low circulating thyroid hormone, and MASLD secondary to impaired lipid metabolism. Correcting hypothyroidism typically normalizes aminotransferases [30, mechanism_review].

**Celiac disease.** Silent or untreated celiac disease causes mild aminotransferase elevation through intestinal inflammation-driven hepatic injury. Gluten withdrawal resolves enzyme levels in most cases.

**Macro-AST.** A benign condition where AST binds to circulating immunoglobulins (most often IgG or IgA), forming a macroenzyme complex with prolonged serum half-life and consequently elevated measured AST — without any organ pathology. Presents as isolated, persistently elevated AST with normal ALT, GGT, CK, and normal liver imaging [30, mechanism_review].

### The De Ritis Ratio as a Prognostic Marker

Beyond diagnostic utility in liver disease, the De Ritis ratio has been validated as a **prognostic marker for all-cause and cardiovascular mortality** in multiple cohorts.

**General elderly population (NHANES).** Ke et al. studied 6,415 participants aged ≥65 years from the NHANES survey (1999–2014, median follow-up 89 months) and found that a high De Ritis ratio was independently associated with all-cause mortality (adjusted HR 1.68; 95% CI 1.47–1.91) and cardiovascular mortality (adjusted HR 1.67; 95% CI 1.27–2.20). The ratio outperformed aminotransferases individually in predicting mortality [31, cohort].

**Stable coronary artery disease.** Ndrepepa et al. studied 3,392 patients with stable coronary artery disease treated with percutaneous coronary intervention at two Munich hospitals (2000–2011). Among those with aminotransferase levels outside the normal reference range, the De Ritis ratio was independently associated with all-cause mortality (adjusted HR 1.27 per unit; 95% CI 1.09–1.48; p = 0.002) [28, cohort].

**Post-AMI long-term mortality.** Steininger et al. followed 1,355 consecutive AMI patients over a median 8.6 years and found the De Ritis ratio remained an independent predictor of all-cause mortality (adjusted HR 1.23 per 1-SD; 95% CI 1.07–1.42; p = 0.004), adding prognostic information beyond NT-proBNP, troponin T, and CK [29, cohort].

The association is likely mediated by the ratio's reflecting a composite of hepatic inflammation, muscle wasting, and systemic metabolic stress. **It is associational, not causal**: no intervention trial has tested whether modifying the ratio improves outcomes.

### What Lowers AST / Low AST

**Vitamin B6 (pyridoxal-5′-phosphate) deficiency.** When assay reagents are not supplemented with exogenous P5P, measured AST (and ALT) may be falsely low in patients with B6 depletion — such as those on chronic dialysis, alcoholics, or malnourished individuals. Whether a specific laboratory includes P5P in its reagents is a non-trivial analytical consideration that affects the true clinical sensitivity of the assay [17, mechanism_review].

**Chronic kidney disease and dialysis.** Patients on hemodialysis exhibit systematically lower AST (and ALT) than non-uremic controls. The mechanism is partly B6 depletion and partly hemodilution; values within the reference range in a dialysis patient may represent significant underlying hepatic injury.

### Limitations and Interpretive Rules

1. **AST is organ-nonspecific.** Without co-measurement of ALT, CK, GGT, and LDH, AST elevation cannot be localized to a source. The source — liver, heart, skeletal muscle, RBC, kidney — must always be inferred from the full biochemical and clinical context [30, mechanism_review].
2. **Normal AST does not exclude liver disease.** In advanced cirrhosis and end-stage liver disease, hepatocyte mass is so reduced that both AST and ALT may fall toward normal despite severe histological injury. The De Ritis ratio tends to be elevated even when absolute values are low.
3. **Hemolysis and macro-AST are measurement artifacts.** Every unexpectedly elevated isolated AST should prompt assessment of specimen hemolysis and, if persistent, consideration of macro-AST.
4. **The De Ritis ratio cannot replace tissue diagnosis.** It is a probabilistic guide, not a substitute for biopsy, imaging, or clinical evaluation in ambiguous cases.

---

## Bibliography

[1]. van Karnebeek CDM, Ramos RJ, Wen X-Y, Tarailo-Graovac M, Gleeson JG, Skrypnyk C, Brand-Arzamendi K, Karbassi F, Issa MY, van der Lee R, Drögemöller BI, Koster J, Rousseau J, Campeau PM, Wang Y, Cao F, Li M, Ruiter J, Ciapaite J, Kluijtmans LAJ, Willemsen MAAP, Jans JJ, Ross CJ, Wintjes LT, Rodenburg RJ, Huigen MCDG, Jia Z, Waterham HR, Wasserman WW, Wanders RJA, Verhoeven-Duif NM, Zaki MS, Wevers RA. Bi-allelic GOT2 Mutations Cause a Treatable Malate-Aspartate Shuttle-Related Encephalopathy. *Am J Hum Genet*. 2019;105(3):534–548. PMID: 31422819. DOI: 10.1016/j.ajhg.2019.07.015. — tag: mechanism_review — tier: 1

[2]. Broeks MH, van Karnebeek CDM, Wanders RJA, Jans JJM, Verhoeven-Duif NM. Inborn disorders of the malate aspartate shuttle. *J Inherit Metab Dis*. 2021;44(4):792–808. PMID: 33990986. DOI: 10.1002/jimd.12402. — tag: mechanism_review — tier: 1

[3]. Borst P. The malate–aspartate shuttle (Borst cycle): How it started and developed into a major metabolic pathway. *IUBMB Life*. 2020;72(11):2241–2259. PMID: 32916028. DOI: 10.1002/iub.2367. — tag: mechanism_review — tier: 1

[4]. Aloisio E, Colombo G, Arrigo C, Dolci A, Panteghini M. Sources and clinical significance of aspartate aminotransferase increases in COVID-19. *Clin Chim Acta*. 2021;522:88–95. PMID: 34411557. DOI: 10.1016/j.cca.2021.08.012. — tag: cohort — tier: 1

[5]. Aloisio E, Panteghini M. Aspartate aminotransferase in COVID-19: A probably overrated marker. *Liver Int*. 2021;41(11):2809–2810. PMID: 34609789. DOI: 10.1111/liv.15068. — tag: cohort — tier: 1

[6]. Diehl AM, Potter J, Boitnott J, Van Duyn MA, Herlong HF, Mezey E. Relationship between pyridoxal 5'-phosphate deficiency and aminotransferase levels in alcoholic hepatitis. *Gastroenterology*. 1984;86(4):632–636. PMID: 6698365. — tag: cohort — tier: 1

[7]. Sherman MS, Goessling W. Discovery of biophysical rate laws from the electronic health record enables real-time liver injury estimation from transaminase dynamics. *Cell Rep Med*. 2024;5(11):101828. PMID: 39536750. DOI: 10.1016/j.xcrm.2024.101828. — tag: cohort — tier: 1

[8]. Kwo PY, Cohen SM, Lim JK. ACG Clinical Guideline: Evaluation of Abnormal Liver Chemistries. *Am J Gastroenterol*. 2017;112(1):18–35. PMID: 27995906. — tag: regulatory — tier: 2

[9]. Semmler G, Binter T, Kozbial K, et al. Age Dependence of Liver Enzymes: An Analysis of Over 1,300,000 Consecutive Blood Samples. *Clin Gastroenterol Hepatol*. 2022;20(3):e456–e465. PMID: 33524594. — tag: cohort — tier: 1

[10]. Williams AL, Hoofnagle JH. Ratio of serum aspartate to alanine aminotransferase in chronic hepatitis: relationship to cirrhosis. *Gastroenterology*. 1988;95(3):734–739. PMID: 3135226. — tag: cohort — tier: 1

[11]. Nyblom H, Berggren U, Balldin J, Olsson R. High AST/ALT ratio may indicate advanced alcoholic liver disease rather than heavy drinking. *Alcohol Alcohol*. 2004;39(4):336–339. PMID: 15208167. — tag: cohort — tier: 1

[12]. Nyblom H, Björnsson E, Simrén M, Aldenborg F, Almer S, Olsson R. The AST/ALT ratio as an indicator of cirrhosis in patients with PBC. *Liver Int*. 2006;26(7):840–845. PMID: 16911467. — tag: cohort — tier: 1

[13]. Nyblom H, Nordlinder H, Olsson R. High aspartate to alanine aminotransferase ratio is an indicator of cirrhosis and poor outcome in patients with primary sclerosing cholangitis. *Liver Int*. 2007;27(5):694–699. PMID: 17498256. — tag: cohort — tier: 1

[14]. Dufour DR. Creatine kinase:aspartate aminotransferase activity ratio as an indicator of the source of an increased creatine kinase activity. *Clin Chem*. 1988;34(12):2506–2510. PMID: 3197292. — tag: mechanism_review — tier: 1

[15]. van Wijk XMR, Magee CA, Wu AHB, Tana MM, Lynch KL. A comparison of methods for evaluation of a case of suspected macro-aspartate aminotransferase. *Clin Chim Acta*. 2016;463:1–3. DOI: 10.1016/j.cca.2016.10.011. — tag: mechanism_review — tier: 1

[16]. Schumann G, Bonora R, Ceriotti F, Férard G, Ferrero CA, Franck PFH, Gella FJ, Hoelzel W, Jørgensen PJ, Kanno T, Kessner A, Klauke R, Kristiansen N, Lessinger JM, Linsinger TPJ, Misaki H, Panteghini M, Pauwels J, Schimmel HG, Vialle A, Weidemann G, Schlenck A. IFCC primary reference procedures for the measurement of catalytic activity concentrations of enzymes at 37°C. Part 5. Reference procedure for the measurement of catalytic concentration of aspartate aminotransferase. *Clin Chem Lab Med*. 2002;40(7):725–733. DOI: 10.1515/CCLM.2002.125. — tag: mechanism_review — tier: 1

[17]. Brinc D, Agbor TA, Fabros A, Cheng PL, Kulasingam V, Selvaratnam R. The harmonization hurdle — a case for pyridoxal-5′-phosphate. *J Appl Lab Med*. 2026. DOI: 10.1093/jalm/jfag018. — tag: mechanism_review — tier: 1

[18]. Parambu MM, Bush V. Evaluation of sensitive analytes to hemolysis interference on an automated chemistry analyzer. *J Appl Lab Med*. 2024;9(3):558–564. DOI: 10.1093/jalm/jfad124. — tag: cohort — tier: 1

[19]. Koseoglu M, Hur A, Atay A, Cuhadar S. Effects of hemolysis interference on routine biochemistry parameters. *Biochem Med (Zagreb)*. 2011;21(1):79–85. DOI: 10.11613/BM.2011.015. — tag: cohort — tier: 1

[20]. Rosemark CL, Baumann N, Block D, Andress B. Reducing hemolyzed specimen rejection for aspartate aminotransferase (AST): a quality improvement initiative to further optimize concentration-specific H-index thresholds. *Clin Chem*. 2024;70(Suppl 1):hvae106.097. DOI: 10.1093/clinchem/hvae106.097. — tag: open_label — tier: 1

[21]. Fermon EJ, Sy M, Drake TA, Song L. "Activation" of macro-AST by pyridoxal-5-phosphate in the assay for aspartate aminotransferase. *Clin Chem Lab Med*. 2024;63(4):e97–e100. PMID: 39402965. DOI: 10.1515/cclm-2024-0944. — tag: mechanism_review — tier: 1

[22]. Cuhadar S, Koseoglu M, Atay A, Dirican A. The effect of storage time and freeze-thaw cycles on the stability of serum samples. *Biochem Med (Zagreb)*. 2013;23(1). DOI: 10.11613/BM.2013.009. — tag: cohort — tier: 1

[23]. Lai X, Chen H, Dong X, Zhou G, Liang D, Xu F, Liu H, Luo Y, Liu H, Wan S. AST to ALT ratio as a prospective risk predictor for liver cirrhosis in patients with chronic HBV infection. *Eur J Gastroenterol Hepatol*. 2024;36(3):338–344. PMID: 38251454. — tag: cohort — tier: 1

[24]. Sorbi D, Boynton J, Lindor KD. The ratio of aspartate aminotransferase to alanine aminotransferase: potential value in differentiating nonalcoholic steatohepatitis from alcoholic liver disease. *Am J Gastroenterol*. 1999;94(4):1018–1022. PMID: 10201476. — tag: cohort — tier: 1

[25]. Tilea I, Varga A, Serban RC. Past, Present, and Future of Blood Biomarkers for the Diagnosis of Acute Myocardial Infarction — Promises and Challenges. *Diagnostics (Basel)*. 2021;11(5):881. PMID: 34063483. (Cites LaDue JS, Wroblewski F, Karmen A. *Science* 1954;120:497–499 as the original AST-AMI description.) — tag: mechanism_review — tier: 1

[26]. Jo KM, Heo NY, Park SH, Moon YS, Kim TO, Park J, Choi JH, Park YE, Lee J. Serum Aminotransferase Level in Rhabdomyolysis according to Concurrent Liver Disease. *Korean J Gastroenterol*. 2019;74(4):205–211. PMID: 31650796. — tag: cohort — tier: 1

[27]. Nathwani RA, Pais S, Reynolds TB, Kaplowitz N. Serum alanine aminotransferase in skeletal muscle diseases. *Hepatology*. 2005;41(2):380–382. PMID: 15660433. — tag: cohort — tier: 1

[28]. Ndrepepa G, Cassese S, Scalamogna M, Lahu S, Aytekin A, Xhepa E, Schunkert H, Kastrati A. Association of De Ritis Ratio with Prognosis in Patients with Coronary Artery Disease and Aminotransferase Activity within and outside the Healthy Values of Reference Range. *J Clin Med*. 2023;12(9):3174. PMID: 37176615. — tag: cohort — tier: 1

[29]. Steininger M, Winter MP, Reiberger T, Koller L, El-Hamid F, Forster S, Schnaubelt S, Hengstenberg C, Distelmaier K, Goliasch G, Wojta J, Toma A, Niessner A, Sulzgruber P. De-Ritis Ratio Improves Long-Term Risk Prediction after Acute Myocardial Infarction. *J Clin Med*. 2018;7(12):474. PMID: 30477196. — tag: cohort — tier: 1

[30]. Botros M, Sikaris KA. The de ritis ratio: the test of time. *Clin Biochem Rev*. 2013;34(3):117–130. PMID: 24353357. — tag: mechanism_review — tier: 1

[31]. Ke P, Zhong L, Peng W, Xu M, Feng J, Tian Q, He Y, Dowling R, Fu W, Jiang H, Zhao Z, Lu K, Lu Z. Association of the serum transaminase with mortality among the US elderly population. *J Gastroenterol Hepatol*. 2022;37(5):946–953. PMID: 35233823. DOI: 10.1111/jgh.15815. — tag: cohort — tier: 1
