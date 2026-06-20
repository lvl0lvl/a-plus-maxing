# Section C: Measurement & Standardization

## Ion-Selective Electrode (ISE): The Modern Standard

Serum sodium is measured in virtually all contemporary clinical laboratories using ion-selective electrode (ISE) potentiometry. The ISE consists of a sodium-selective membrane — typically incorporating a neutral carrier or glass electrode — that generates a potential difference proportional to the logarithm of the sodium ion (Na⁺) activity in the sample (the Nernst equation). That activity is then converted to concentration using a calibration derived from reference standards. ISE has displaced flame photometry as the dominant platform because it requires no combustible gas, is fully automatable on high-throughput chemistry analyzers, and operates with small sample volumes [1, mechanism_review].

### The Load-Bearing Distinction: Direct vs. Indirect ISE

ISE analyzers operate in one of two fundamentally different modes, and the difference has major clinical consequences.

**Direct ISE** presents the sample to the electrode membrane **without prior dilution**. This is the method used by point-of-care devices and blood-gas analyzers (e.g., Radiometer ABL series, Siemens RAPIDPoint). Because no dilution step occurs, the electrode responds to Na⁺ activity **in the plasma water phase itself** — the phase where sodium actually exists. Plasma normally contains approximately 93% water by mass (0.93 kg/L), with the remaining ~7% occupied by proteins and lipids. Direct ISE measures sodium in that aqueous phase, giving a result that reflects the physiologically meaningful quantity: sodium activity in plasma water [1, mechanism_review; 2, cohort].

**Indirect ISE** — used by the large automated chemistry analyzers that process the majority of hospital specimens (e.g., Roche Cobas, Abbott Architect, Siemens Dimension) — **dilutes the sample** (typically 1:20 to 1:34 with an ionic-strength adjustment buffer) before presenting it to the electrode. The calculation that converts the measured activity back to a reported plasma sodium concentration **assumes that plasma water constitutes exactly 0.93 kg/L** (i.e., the normal 93% water fraction). In a healthy person, this assumption is essentially correct, and indirect ISE gives a result closely comparable to direct ISE and to the historical flame photometry reference [1, mechanism_review; 5, mechanism_review].

### Pseudohyponatremia: The Electrolyte Exclusion Effect

The critical failure mode of indirect ISE arises when the 0.93 kg/L plasma-water assumption breaks down — specifically in **severe hyperlipidemia** (hypertriglyceridemia, hypercholesterolemia) or **severe hyperproteinemia** (paraproteinemia from multiple myeloma, IVIG infusion, polyclonal immunoglobulin disorders). In these states, the displaced water fraction falls substantially — toward 0.80–0.85 kg/L or below — while the volume occupied by lipid or protein rises correspondingly. The indirect ISE method, still assuming 0.93 kg/L of water per liter of plasma, systematically underestimates the sodium concentration. This artifact is called **pseudohyponatremia**, and its mechanism is the **electrolyte exclusion effect**: sodium (which exists only in the water phase) is excluded from the solid-phase volume, but the dilution-based method attributes that volume to the aqueous compartment [1, mechanism_review; 3, cohort].

The magnitude is clinically significant. Studies comparing indirect ISE against direct ISE in patients with elevated total protein (>7.9 g/dL) found an average sodium underestimation of **–6.1 mmol/L**, with 70% of hyperproteinemic specimens showing a clinically meaningful discrepancy [2, cohort]. One case series found that **43% of ICU patients** exceeded the 4 mmol/L threshold for clinically relevant disagreement between methods [1, mechanism_review]. In extreme cases — for example, severe hypertriglyceridemia (triglycerides >15 mmol/L) — the sodium artefact can be quantified as approximately **1 mmol/L per 10 mmol/L increment in total lipids** [6, cohort]. In IVIG-treated patients, where exogenous immunoglobulin sharply raises total protein (documented cases: 8.0 → 9.6 g/dL), the indirect ISE can underestimate true plasma sodium by **6 mmol/L or more**, with published corrective formulas proving unreliable in these settings [7, cohort]. Hypercholesterolemia — less commonly recognized than hypertriglyceridemia — can also drive pseudohyponatremia; routine lipemia indices used by chemistry analyzers may fail to flag cholesterol-mediated interference, since those indices are calibrated for triglyceride-based turbidity [8, cohort].

**Direct ISE is immune to pseudohyponatremia.** Because no dilution step is applied, the plasma solid fraction does not enter the calculation. Direct ISE measures what is actually present in the water phase, regardless of how elevated lipid or protein may be [2, cohort; 4, cohort]. This is why confirmation of a suspected pseudohyponatremia requires reflexing the specimen to a blood-gas analyzer using the direct ISE mode — or using plasma (rather than whole blood) validated for that instrument [4, cohort].

### Flame Photometry: The Historical Reference

Before ISE became universal, **flame emission photometry** (flame photometry) was the reference method for serum sodium and potassium. A diluted specimen is atomized and aspirated into a flame; sodium atoms absorb thermal energy, become electronically excited, and emit light at a characteristic wavelength (589 nm for Na); the emitted intensity is compared against calibrators [5, mechanism_review]. Flame photometry was accurate and robust, but required combustible gas supplies, was susceptible to matrix-dependent quenching, and was slower than modern ISE. Critically, because flame photometry **also dilutes the sample** before measurement, it is **equally susceptible to the electrolyte exclusion effect** — pseudohyponatremia was first characterized as a flame photometry artifact before indirect ISE was understood to share the same vulnerability [1, mechanism_review]. Flame photometry is now largely replaced in clinical chemistry by ISE, though it remains the historical anchor for traceability.

### Standardization and Metrological Traceability

Sodium measurement traceability in clinical laboratories runs through the **NIST Standard Reference Material (SRM) 956 series** — frozen human serum certified for sodium, potassium, chloride, and several other electrolytes. The most recent version, SRM 956e (issued December 2024), provides three concentration levels spanning the clinically relevant range, with certified sodium values traceable to primary methods. The SRM 956 series was developed in conjunction with the **Clinical and Laboratory Standards Institute (CLSI) documentary standard C29-A2**, which codifies the standardization of ISE systems to the flame photometric reference method. This traceability chain grounds both direct and indirect ISE calibration against a common metrological anchor [9, mechanism_review].

One measurement-mode consequence of this traceability architecture is that **direct ISE and indirect ISE can report systematically different values in normal specimens**. Direct ISE measures Na⁺ *activity* in plasma water (molal scale), which — after accounting for the molal activity coefficient of sodium in plasma (~0.747) and the normal plasma water fraction — tends to read **2–7 mmol/L higher** than indirect ISE in method-comparison studies under normal physiological conditions [1, mechanism_review; 5, mechanism_review]. Because of this systematic offset, laboratories using direct ISE must apply **method-specific reference intervals** rather than assuming the canonical 136–145 mmol/L range (which was established with indirect ISE / flame photometry platforms).

### Pre-analytic Artifacts

Two pre-analytic errors are particularly important for sodium:

**IV-line contamination (spuriously HIGH sodium).** Drawing blood from a line above an infusing normal saline (0.9% NaCl, ~154 mmol/L Na) introduces saline into the sample, producing a falsely elevated sodium result. This is a classic spurious hypernatremia; the artifact is recognized by the implausibly high sodium combined with dilution of other analytes (low creatinine, low albumin, abnormal glucose) in the same specimen. The solution is to discard an adequate volume before collection or to redraw from a distal site [1, mechanism_review].

**Serum vs. plasma vs. whole blood.** Small systematic differences exist between matrices. In head-to-head comparison of whole blood (direct ISE on blood-gas analyzer) and plasma (same direct ISE), the average difference is modest (~1.3 mmol/L), well within clinical tolerance in most settings [4, cohort]. Serum and lithium-heparin plasma perform equivalently for sodium under standard conditions.

---

## Bibliography

1. Datta SK, Chopra P. "Interference in Ion-Selective Electrodes Due to Proteins and Lipids." *Journal of Applied Laboratory Medicine*. 2022;7(2):589–595. https://doi.org/10.1093/jalm/jfab125 — tag: mechanism_review — tier: 1

2. Katrangi W, Baumann NA, Nett RC, Karon BS, Block DR. "Prevalence of Clinically Significant Differences in Sodium Measurements Due to Abnormal Protein Concentrations Using an Indirect Ion-Selective Electrode Method." *Journal of Applied Laboratory Medicine*. 2019;4(3):427–432. https://doi.org/10.1373/jalm.2018.028720 — tag: cohort — tier: 1

3. Maas AH, Siggaard-Andersen O, Weisberg HF, Zijlstra WG. "Ion-selective electrodes for sodium and potassium: a new problem of what is measured and what should be reported." *Clinical Chemistry*. 1985;31(3):482–485. https://doi.org/10.1093/clinchem/31.3.482 — tag: mechanism_review — tier: 1

4. Vera MA, Sutphin A, Hansen L, El-Khoury JM. "Resolving Pseudohyponatremia: Validation of Plasma Sodium on Radiometer ABL800 Blood Gas Analyzers for Immediate Reflex Testing." *Laboratory Medicine*. 2022;53(5):e105–e108. https://doi.org/10.1093/labmed/lmab114 — tag: cohort — tier: 1

5. Levy GB. "Determination of sodium with ion-selective electrodes." *Clinical Chemistry*. 1981;27(8):1435–1438. https://doi.org/10.1093/clinchem/27.8.1435 — tag: mechanism_review — tier: 1

6. Dimeski G, Mollee P, Carter A. "Effects of Hyperlipidemia on Plasma Sodium, Potassium, and Chloride Measurements by an Indirect Ion-Selective Electrode Measuring System." *Clinical Chemistry*. 2006;52(1):155–156. https://doi.org/10.1373/clinchem.2005.054981 — tag: cohort — tier: 1

7. Virk MS, Dean NP, Wong ECC. "Severe Underestimation of Serum Na following IVIG Treatment." *Laboratory Medicine*. 2018;49(4):372–376. https://doi.org/10.1093/labmed/lmy025 — tag: cohort — tier: 1

8. Merrill AE, Day JR, Simonson TJ, Meeusen JW, Donato LJ. "Complex Hyponatremia in a Cancer Patient with Hypercholesterolemia." *Clinical Chemistry*. 2025;71(9):928–932. https://doi.org/10.1093/clinchem/hvaf038 — tag: cohort — tier: 1

9. National Institute of Standards and Technology. "An SRM for Accuracy in Electrolyte Panel Clinical Tests." NIST News, February 2025. https://www.nist.gov/news-events/news/2025/02/srm-accuracy-electrolyte-panel-clinical-tests — tag: mechanism_review — tier: 2
