# Section B: The eGFR Equations, Units, and CKD Staging

## Units and Standardization

Estimated GFR (eGFR) is reported in **mL/min/1.73 m²** — the GFR normalized to a standard body surface area of 1.73 m², which allows comparison across individuals of different body sizes. Serum creatinine (Scr) is measured in **mg/dL** in US practice (multiply by **88.4** to convert to µmol/L used in SI countries). All modern estimating equations require creatinine values that have been **standardized to isotope dilution mass spectrometry (IDMS)** reference methods; using non-IDMS-calibrated creatinine introduces systematic bias [1, cohort].

---

## The Estimating Equations

### MDRD (Modification of Diet in Renal Disease)

The 4-variable MDRD equation, reexpressed for standardized creatinine by Levey et al. in 2006, was the first widely adopted estimating equation:

> eGFR = 175 × Scr⁻¹·¹⁵⁴ × Age⁻⁰·²⁰³ × 0.742 [if female] × 1.21 [if Black]

(Scr in mg/dL, age in years) [1, cohort]

The MDRD equation systematically **underestimates GFR above ~60 mL/min/1.73 m²** — the range occupied by most people without CKD — and was calibrated in a predominantly CKD population. Its race coefficient (×1.21 for Black individuals) was an empirical correction based on population averages, not a biologically grounded mechanism.

---

### CKD-EPI Creatinine Equation (2009)

Levey, Stevens, Schmid et al. published the CKD-EPI creatinine equation in 2009, developed and validated by the Chronic Kidney Disease Epidemiology Collaboration across 8,254 participants from 10 studies [2, cohort]. The 2009 formula uses a two-slope spline to handle the nonlinear creatinine-GFR relationship:

> eGFR = 141 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^⁻¹·²⁰⁹ × 0.993^Age × 1.018 [if female] × 1.159 [if Black]

Where κ = 0.7 (female) or 0.9 (male); α = −0.329 (female) or −0.411 (male).

Compared to MDRD, CKD-EPI 2009 showed less bias (median difference 2.5 vs 5.5 mL/min/1.73 m²) and greater P30 accuracy — the proportion of estimates falling within 30% of a measured GFR — (84.1% vs 80.6%) [2, cohort]. P30 ≥90% is the preferred threshold for clinical-grade accuracy; neither the MDRD nor the 2009 CKD-EPI equation reached it universally, particularly at high GFR.

The 2009 equation retained a Black-race multiplier (×1.159) inherited from the MDRD approach. This coefficient was derived from observed differences in serum creatinine at equivalent measured GFR, attributed to higher average muscle mass in Black individuals — but race is a **social construct**, not a biological variable, and using it as a continuous biological input in a clinical formula introduced the risk of systematically overestimating GFR in Black patients, potentially delaying CKD diagnosis and transplant eligibility.

---

### The 2021 Race-Free CKD-EPI Refit — The Load-Bearing Development

In 2021, Inker LA, Eneanya ND, Coresh J, and colleagues (the CKD-EPI Collaboration) published **"New Creatinine- and Cystatin C-Based Equations to Estimate GFR without Race"** in the *New England Journal of Medicine* [3, cohort]. PMID: 34554658.

The investigators developed two new equations — one creatinine-based, one creatinine + cystatin C — in development cohorts of 8,254 and 5,352 participants respectively, then validated in 4,050 participants from 12 studies. The core change: **the race variable was eliminated entirely**, on the grounds that race "is a social and not a biologic construct" and that assigning systematically different eGFR estimates by race risks perpetuating health inequities, delaying nephrology referral, and distorting transplant wait-time accrual in Black patients.

**The 2021 CKD-EPI creatinine equation (race-free):**

> eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^⁻¹·²⁰⁰ × 0.9938^Age × 1.012 [if female]

Where κ = 0.7 (female) or 0.9 (male); α = −0.241 (female) or −0.302 (male) [3, cohort; 4, regulatory].

The coefficient shift (141→142, exponents slightly adjusted) reflects a refit of the entire spline rather than simply dropping the race term.

**Performance (P30 accuracy):**

| Equation | Black participants | Non-Black participants |
|----------|-------------------|------------------------|
| CKD-EPI creatinine 2021 | 87.2% | 86.5% |
| CKD-EPI creatinine-cystatin C 2021 | 90.5% | 90.8% |

The **creatinine-cystatin C combined equation (2021)** is the most accurate available in routine clinical practice, achieving P30 ≥90% across racial groups [3, cohort]. It performs this well because cystatin C is filtered by the glomerulus and not tubularly secreted or reabsorbed at meaningful rates, is produced at a rate largely independent of muscle mass, and therefore provides an orthogonal signal to creatinine that corrects for inter-individual variation in muscle mass — the primary source of creatinine-equation error. The NKF now recommends clinical laboratories adopt the 2021 CKD-EPI equations [4, regulatory].

---

## KDIGO CKD GFR Staging

The **KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease** (Kidney Int. 2024;105(4S):S117–S314; PMID 38490803) [5, regulatory] defines CKD using a three-axis classification: **Cause (C)**, **GFR category (G)**, **Albuminuria category (A)** — abbreviated **CGA**.

**CKD definition:** abnormalities of kidney structure or function present for **≥3 months** with implications for health. A single low eGFR reading is not CKD; chronicity must be established. This is clinically important: acute kidney injury (AKI) can produce the same eGFR number as G4 CKD but resolves with treatment, while CKD implies sustained, often progressive loss.

### GFR Categories

| Category | eGFR (mL/min/1.73 m²) | Description |
|----------|------------------------|-------------|
| G1 | ≥90 | Normal or high |
| G2 | 60–89 | Mildly decreased |
| G3a | 45–59 | Mildly to moderately decreased |
| G3b | 30–44 | Moderately to severely decreased |
| G4 | 15–29 | Severely decreased |
| G5 | <15 | Kidney failure |

G1 and G2 meet CKD criteria only when accompanied by **markers of kidney damage** (albuminuria, haematuria, structural abnormality, pathological diagnosis) present for ≥3 months — an eGFR ≥60 alone, without such markers, does not define CKD. The subdivision of Stage 3 into G3a and G3b reflects meaningfully different cardiovascular and progression risk even within the 30–59 mL/min/1.73 m² range.

### Albuminuria Categories

| Category | ACR (mg/g) | ACR (mg/mmol) | Description |
|----------|------------|----------------|-------------|
| A1 | <30 | <3 | Normal to mildly increased |
| A2 | 30–300 | 3–30 | Moderately increased |
| A3 | >300 | >30 | Severely increased (includes nephrotic-range) |

### The GFR × Albuminuria Heat Map

KDIGO presents a **5 × 3 risk grid** cross-tabulating G1–G5 against A1–A3 [5, regulatory]. Each cell carries a color denoting prognosis for CKD progression, ESRD, and cardiovascular mortality:

- **Green** — low risk (if no other kidney disease markers, does not meet CKD criteria)
- **Yellow** — moderately increased risk
- **Orange** — high risk
- **Red** — very high risk
- **Dark red** — highest risk

The heat map conveys that both axes are **independently prognostic**: a patient with G2 + A3 carries higher risk than a patient with G3a + A1, illustrating why albuminuria must be measured and not inferred from eGFR alone. KDIGO recommends measuring both eGFR and urine albumin-to-creatinine ratio (ACR) at least annually in people with established CKD.

---

## Caveats and Scope Limits of eGFR Estimation

**Single measurement ≠ CKD.** The ≥3-month chronicity requirement exists precisely because acute illness (volume depletion, NSAIDs, contrast agents, AKI) can transiently suppress eGFR into the G3–G4 range; repeat testing after the acute insult resolves is mandatory before diagnosing CKD.

**Age-related GFR decline.** Mean GFR falls roughly 1 mL/min/1.73 m² per year after age ~40 [5, regulatory]. An eGFR of 65 in a 75-year-old may reflect normal aging rather than CKD, especially if ACR is in the A1 range — though KDIGO does not apply age-specific eGFR thresholds.

**P30 accuracy and equation bias.** Even the best available equation (CKD-EPI creatinine-cystatin C 2021) has P30 ≈ 90% — meaning 1 in 10 estimates differs from the true GFR by more than 30%. The P30 metric is the standard for equation benchmarking because GFR measurement error itself limits expectations; however, at extreme GFR values (e.g., living kidney donor evaluation at eGFR >90), even a 30% error translates to a large absolute uncertainty [2, 3, cohort].

**Equation validity limits.** The CKD-EPI equations are not validated for: extremes of body composition (severe obesity, amputees, bodybuilders); rapidly changing GFR (AKI, post-transplant early phase); children and adolescents (use CKiD-U25 or Schwartz equations); conditions altering cystatin C independent of GFR (thyroid disease, high-dose corticosteroids). In these settings, measured GFR (via iohexol clearance or iothalamate) is the reference standard.

**Creatinine is not GFR.** Serum creatinine alone is a poor surrogate: a 50% loss of kidney function can occur before creatinine rises above the normal reference range, because the remaining nephrons hyperfiltrate. eGFR translates creatinine into a population-average GFR estimate, but the underlying assumptions (stable creatinine production, no tubular secretion confounders) are violated in some individuals. Cystatin C adds independent discriminative value precisely because it is not subject to the same confounders [3, cohort].

---

## Bibliography

1. Levey AS, Coresh J, Greene T, Stevens LA, Zhang YL, Hendriksen S, Kusek JW, Van Lente F; Chronic Kidney Disease Epidemiology Collaboration. Using standardized serum creatinine values in the modification of diet in renal disease study equation for estimating glomerular filtration rate. *Ann Intern Med.* 2006;145(4):247–254. PMID: 16908915. — tag: cohort — tier: 1

2. Levey AS, Stevens LA, Schmid CH, Zhang YL, Castro AF 3rd, Feldman HI, Kusek JW, Eggers P, Van Lente F, Greene T, Coresh J; CKD-EPI Collaboration. A new equation to estimate glomerular filtration rate. *Ann Intern Med.* 2009;150(9):604–612. PMID: 19414839. — tag: cohort — tier: 1

3. Inker LA, Eneanya ND, Coresh J, et al.; Chronic Kidney Disease Epidemiology Collaboration (CKD-EPI). New creatinine- and cystatin C-based equations to estimate GFR without race. *N Engl J Med.* 2021;385(19):1737–1749. PMID: 34554658. DOI: 10.1056/NEJMoa2102953. — tag: cohort — tier: 1

4. National Kidney Foundation. CKD-EPI Creatinine Equation (2021). National Kidney Foundation. https://www.kidney.org/ckd-epi-creatinine-equation-2021-0. Accessed 2026. — tag: regulatory — tier: 2

5. Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease. *Kidney Int.* 2024;105(4S):S117–S314. PMID: 38490803. DOI: 10.1016/j.kint.2023.10.018. — tag: regulatory — tier: 1
