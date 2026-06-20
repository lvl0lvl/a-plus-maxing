# Section A: Physiology & What HbA1c Measures

## Non-Enzymatic Glycation and the Amadori Product

Hemoglobin A1c (HbA1c; NGSP %; IFCC mmol/mol) is formed through a two-step, non-enzymatic reaction between circulating glucose and the N-terminal valine residue of the β-chains of adult hemoglobin A (α₂β₂) [1, mechanism_review]. This process, a Maillard early-phase reaction, proceeds without enzymatic catalysis and is therefore properly termed *glycation* rather than glycosylation.

In the first, reversible step, the aldehyde group of glucose condenses with the free α-amino group of β-chain N-terminal valine to form a labile aldimine (Schiff base), sometimes designated labile HbA1c (LA1c) [1, mechanism_review]. Because this adduct is thermodynamically unstable, it either dissociates (reversibly) or undergoes the Amadori rearrangement: an acid-catalysed ring-opening through an iminium ion intermediate that resolves to a stable 1-amino-1-deoxyfructose ketoamine [2, mechanism_review]. This second step is irreversible under physiological conditions; the resulting ketoamine linkage defines HbA1c as an Amadori product, not an advanced glycation end-product (AGE). True AGEs require months-to-years of additional oxidative and cross-linking chemistry beyond the Amadori stage [2, mechanism_review].

The reaction is specific to the β-chain N-terminus because the microenvironment around β-Val-1 lowers its pKa, keeping the amine unprotonated and reactive at physiological pH. Glycation can also occur at α-chain N-terminal valines and ε-amino groups of lysine residues throughout the globin chains, producing other glycated fractions (HbA1a₁, HbA1a₂, HbA1b); these are structurally distinct from HbA1c and are excluded by the IFCC reference measurement procedure, which targets exclusively the glycated β-chain N-terminal hexapeptide [1, mechanism_review]. HbA0 denotes non-glycated hemoglobin or hemoglobin glycated at sites other than β-chain N-terminal valine.

The rate of HbA1c formation inside the erythrocyte is proportional to ambient glucose concentration: a higher prevailing glucose means a higher fraction of available β-chain N-termini are captured by the Amadori rearrangement over time [3, mechanism_review].

## Erythrocyte Lifespan and the Time-Integration Window

Once formed, the ketoamine bond linking glucose to β-Val-1 is stable for the remaining lifespan of the erythrocyte. Human erythrocytes cannot synthesise new hemoglobin, perform no further repair, and are cleared by the spleen after an average circulating lifespan of approximately 120 days (range roughly 70–140 days) [3, mechanism_review]. Consequently, the proportion of hemoglobin bearing an Amadori adduct at the β-chain N-terminus accumulates progressively as a red blood cell ages through this window — yielding a chemical record of cumulative glucose exposure.

Because the circulating erythrocyte pool at any moment contains cells of every age from newly released reticulocytes (age ~0) to cells approaching senescence (age ~120 days), a measured HbA1c value integrates the glycation history contributed by all of these cohorts simultaneously [4, mechanism_review]. The erythrocyte age distribution is not uniform: mathematical modelling using biotinylated red-cell survival data shows that the average *age* of circulating erythrocytes is approximately 49–53 days, and the effective average erythrocyte lifespan is closer to 80–90 days when non-senescence-mediated clearance mechanisms are included [4, mechanism_review]. This is why HbA1c broadly reflects 8–12 weeks of glycaemia rather than the full theoretical 120-day maximum.

## Temporal Weighting: The ~50% Contribution of the Preceding 30 Days

HbA1c is not a simple unweighted average across the full erythrocyte lifespan. Because freshly released erythrocytes are more abundant than older ones in a steady-state population, and because glycation of any individual cell accumulates from day 0, glucose exposure in the most recent weeks exerts disproportionate influence on the measured HbA1c [4, mechanism_review]. Kinetic modelling by Tahara and Shima (1995) showed that approximately 50% of a given HbA1c value is determined by mean plasma glucose during the preceding ~30 days, roughly 25% by the 30-day period before that (days 31–60), and the remaining ~25% by glucose exposure during days 61–120 before the measurement [5, mechanism_review]. Later modelling corroborated this hierarchy: half of the expected HbA1c change toward a new glucose target is reached in approximately 30 days after a step change in mean blood glucose [4, mechanism_review]. An immediate clinical corollary is that clinically meaningful HbA1c changes can be detected within 4–6 weeks of a sustained shift in glycaemia — the 120-day lifespan is the outer boundary, not the practical response horizon.

The glucose exposure from the most recent few days before sampling has minimal impact because the Schiff base formed at that point is still largely in the labile, pre-Amadori stage and can dissociate before the assay is performed. Standard HPLC and immunoassay methods explicitly exclude labile HbA1c to report only the stable Amadori product.

## The HbA1c–Mean Glucose Relationship and the ADAG Regression

The A1c-Derived Average Glucose (ADAG) Study (2006–2008), sponsored by the ADA, EASD, and IDF, was designed to define the mathematical relationship between HbA1c and average glucose rigorously [6, cohort]. The study enrolled 507 participants — 268 with type 1 diabetes, 159 with type 2 diabetes, and 80 normoglycaemic subjects — across 10 international centres. Each participant generated approximately 2,700 glucose measurements over 3 months using a hybrid protocol: continuous glucose monitoring (CGM) for at least 2 days on four separate occasions, plus seven-point daily capillary self-monitoring at least 3 days per week. HbA1c was measured centrally using a DCCT-traceable assay.

Linear regression between HbA1c (NGSP %) and calculated average glucose (AG) yielded [6, cohort]:

**eAG (mg/dL) = 28.7 × HbA1c (%) − 46.7**  (R² = 0.84, p < 0.0001)

**eAG (mmol/L) = 1.59 × HbA1c (%) − 2.59**

The relationship was statistically equivalent across subgroups defined by age, sex, diabetes type, race/ethnicity, and smoking status [6, cohort]. Reference values using the NGSP/IFCC master equation (IFCC [mmol/mol] = 10.93 × NGSP [%] − 23.50) [7, regulatory]:

| HbA1c NGSP (%) | HbA1c IFCC (mmol/mol) | eAG (mg/dL) | eAG (mmol/L) |
|:-:|:-:|:-:|:-:|
| 5.0 | 31 | 97 | 5.4 |
| 6.0 | 42 | 126 | 7.0 |
| 6.5 | 48 | 140 | 7.8 |
| 7.0 | 53 | 154 | 8.6 |
| 7.5 | 58 | 169 | 9.4 |
| 8.0 | 64 | 183 | 10.2 |
| 9.0 | 75 | 212 | 11.8 |
| 10.0 | 86 | 240 | 13.4 |

An R² of 0.84 means the regression accounts for 84% of the variance in average glucose; the remaining 16% reflects individual biological variation in glycation rate, erythrocyte lifespan, and red-cell membrane permeability to glucose — sources of inter-individual discordance between HbA1c and directly measured mean glucose [4, mechanism_review].

## What HbA1c Cannot Measure

Because HbA1c is a time-integrated, erythrocyte-lifespan-weighted retrospective average, it carries several inherent interpretive limits:

**No resolution of glycaemic variability.** Two individuals with identical HbA1c values can have radically different glycaemic profiles — one with stable mid-range glucose and one with oscillating extremes of hypoglycaemia and hyperglycaemia. HbA1c is insensitive to the amplitude or frequency of glucose fluctuations; continuous glucose monitoring metrics (time-in-range, coefficient of variation) are required to characterise variability [6, cohort].

**No single-time-point inference.** An HbA1c result cannot be reverse-engineered to estimate fasting glucose, postprandial glucose, or any other discrete glucose reading. The ADAG regression yields a population-mean estimate of average glucose, not a point measurement.

**Sensitivity to erythrocyte lifespan.** Any condition that shortens red-cell survival — haemolytic anaemia, sickle cell disease, recent transfusion, splenomegaly — reduces HbA1c relative to concurrent mean glucose. Conditions that prolong erythrocyte survival — iron-deficiency anaemia, B12/folate deficiency — spuriously elevate HbA1c [1, mechanism_review]. In these settings, alternative markers of shorter-term glycaemia (glycated albumin, fructosamine) may be necessary.

**Temporal lag.** Because recent glucose exerts only ~50% of the influence on HbA1c, a dramatic acute glucose excursion or acute normalization will not be fully visible in HbA1c for several weeks. HbA1c is calibrated for monitoring chronic glycaemic status, not acute changes.

---

## Bibliography

[1]. Chen C, et al. Interpretation of HbA1c lies at the intersection of analytical methodology, clinical biochemistry and hematology (Review). *Exp Ther Med*. 2022. PMC9634344. — tag: mechanism_review — tier: 1

[2]. Perrone A, et al. An overview on glycation: molecular mechanisms, impact on proteins, pathogenesis, and inhibition. *Biophys Rev*. 2024. DOI: 10.1007/s12551-024-01188-4. — tag: mechanism_review — tier: 1

[3]. Bunn HF, Gabbay KH, Gallop PM. The glycosylation of hemoglobin: relevance to diabetes mellitus. *Science*. 1978;200(4337):21–27. PMID: 635569. DOI: 10.1126/science.635569. — tag: mechanism_review — tier: 1

[4]. Oron T, et al. Glycated Hemoglobin, Plasma Glucose, and Erythrocyte Aging. PMC5094338. *J Diabetes Sci Technol*. 2016. — tag: mechanism_review — tier: 1

[5]. Tahara Y, Shima K. Kinetics of HbA1c, glycated albumin, and fructosamine and analysis of their weight functions against preceding plasma glucose level. *Diabetes Care*. 1995;18(4):440–447. PMID: 7497851. DOI: 10.2337/diacare.18.4.440. — tag: mechanism_review — tier: 1

[6]. Nathan DM, et al. (ADAG Study Group). Translating the A1C assay into estimated average glucose values. *Diabetes Care*. 2008;31(8):1473–1478. PMID: 18540046. PMC: PMC2742903. DOI: 10.2337/dc08-0545. — tag: cohort — tier: 1

[7]. NGSP/IFCC Master Equation. National Glycohemoglobin Standardization Program. NGSP–IFCC HbA1c standardisation reference. URL: https://ngsp.org/ifccngsp.asp. — tag: regulatory — tier: 2
