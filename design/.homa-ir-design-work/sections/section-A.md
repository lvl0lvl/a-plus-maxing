# Section A: What HOMA-IR Is and the Underlying Model

## The Homeostatic Model: Fasting-State Physiology

Insulin resistance — the blunted ability of target tissues to respond to insulin — is central to the pathophysiology of type 2 diabetes, metabolic syndrome, and cardiovascular disease. Its direct measurement requires resource-intensive, invasive techniques. The Homeostatic Model Assessment (HOMA), introduced by Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, and Turner RC in 1985, offered a practical alternative [1, cohort]. By exploiting the biology of the fasting steady state, HOMA allowed clinicians and researchers to infer insulin resistance and beta-cell function from two routine measurements: fasting plasma glucose (FPG) and fasting plasma insulin (FPI).

The physiological logic rests on a feedback circuit that operates continuously in the post-absorptive state. In healthy fasting physiology, hepatic glucose production (HGP) is the primary determinant of FPG. The liver senses circulating insulin and suppresses glucose output proportionally; pancreatic beta-cells, in turn, sense glucose and adjust insulin secretion accordingly. The system normally converges on a homeostatic equilibrium — a stable pair of fasting glucose and insulin concentrations that reflects the balance between insulin secretory capacity and insulin action. HOMA-IR models this equilibrium mathematically: a given pair of fasting values encodes information about where along the insulin-resistance axis the individual sits [1, cohort]. Because the fasting glucose level is predominantly governed by hepatic glucose output (skeletal muscle is largely quiescent after an overnight fast, not consuming glucose against an insulin gradient), the fasting pair of FPG × FPI most directly reflects **hepatic** insulin resistance — the degree to which the liver fails to suppress glucose production in response to ambient insulin [2, cohort].

## HOMA1: The 1985 Linear Approximation

The original 1985 publication provided a simple algebraic formula derived from piecewise linear approximations to the full computer model's dose-response curves [1, cohort]:

> **HOMA-IR = (FPG [mmol/L] × FPI [μU/mL]) / 22.5**

(In US units: (FPG [mg/dL] × FPI [μU/mL]) / 405)

A parallel formula yielded a percentage estimate of beta-cell function (%B). The normalizing constant 22.5 was chosen so that a healthy young adult with FPG of 4.5 mmol/L and FPI of 5 μU/mL would score exactly 1.0, representing nominal insulin sensitivity. The formula was computationally convenient and enabled large-scale epidemiological work, but it carried deliberate simplifications: it assumed linear relationships across the physiological range, used a single compartment for insulin action (without separating hepatic from peripheral contributions), and did not account for proinsulin cross-reactivity in insulin assays or for glucose losses via the kidney at hyperglycemic concentrations [3, mechanism_review].

## HOMA2: The Updated Nonlinear Computer Model

Levy JC, Matthews DR, and Hermans MP published a pivotal correction in 1998 [4, cohort]: the original approximation formulae produced systematically biased estimates when applied to subjects outside the narrow normal range for which the linear approximation was adequate, particularly in individuals with insulin resistance or frank hyperglycemia. The 1998 paper clarified that HOMA should be executed using the full computer program — not the simplified formula — whenever quantitative comparisons across a wide physiological range are required [4, cohort].

Wallace TM, Levy JC, and Matthews DR formalized this distinction comprehensively in their 2004 review [3, mechanism_review], now the standard reference for HOMA2. HOMA2 — the updated, nonlinear computer model available from the Diabetes Trials Unit at the University of Oxford — differs from HOMA1 in three material respects:

1. **Nonlinear dose-response curves.** The HOMA2 model replaces the piecewise linear approximations of 1985 with nonlinear (sigmoidal) physiological functions governing both beta-cell insulin secretion in response to glucose and tissue glucose uptake in response to insulin. This substantially improves accuracy across the full pathophysiological range from lean normoglycemic individuals to patients with overt type 2 diabetes [3, mechanism_review].

2. **Proinsulin correction.** HOMA2 incorporates a module for proinsulin secretion, accounting for the fact that many insulin immunoassays cross-react with intact proinsulin and split proinsulin fragments (which circulate at higher concentrations in insulin-resistant and early-diabetic states). This allows either total immunoreactive insulin or specific insulin assay values to be entered appropriately [3, mechanism_review].

3. **Renal glucose loss.** At elevated fasting glucose concentrations (typically above approximately 10 mmol/L), significant glucose is lost via the kidney, altering the apparent fasting glucose level relative to what the endocrine feedback circuit "sees." HOMA2 includes a renal glucose reabsorption module so that the model remains applicable in hyperglycemic subjects [3, mechanism_review].

## HOMA-%S and HOMA-%B: Companion Outputs

HOMA-IR is not the only output the model produces. HOMA2 yields three simultaneous estimates from the same fasting pair:

- **HOMA-IR**: the insulin resistance index (dimensionless; higher = more resistant)
- **HOMA-%S** (insulin sensitivity): expressed as a percentage of a normal reference population value; the reciprocal concept to HOMA-IR
- **HOMA-%B** (beta-cell function): the estimated secretory capacity of the beta-cell mass, expressed as a percentage of normal

In practice, HOMA-%B is used in research on beta-cell preservation in pre-diabetes and early type 2 diabetes [3, mechanism_review; 5, cohort]. For clinical and epidemiological purposes, HOMA-IR is the dominant output, appearing in more than 500 publications in the years following the original paper [3, mechanism_review].

## What HOMA-IR Estimates — and What It Does Not

A critical interpretive constraint follows directly from the fasting physiology the model encodes. Because HGP is the dominant determinant of FPG during a post-absorptive fast — and because HGP suppression by insulin constitutes hepatic insulin action — **HOMA-IR is primarily a surrogate for hepatic insulin resistance** [2, cohort]. Tripathy et al. demonstrated in a cohort of subjects spanning normal glucose tolerance through frank type 2 diabetes that HOMA-IR correlated strongly with hepatic insulin sensitivity (measured by stable isotope tracer during the euglycemic-hyperinsulinemic clamp), with hepatic sensitivity explaining approximately 40% of HOMA-IR's variance in subjects with impaired glucose tolerance [2, cohort]. Critically, HOMA-IR did not correlate significantly with the M-value — the clamp's measure of whole-body (predominantly skeletal-muscle) glucose disposal — in subjects with impaired fasting glucose, confirming the conceptual boundary: HOMA-IR and peripheral insulin sensitivity are partially dissociable [2, cohort].

Peripheral (skeletal-muscle) insulin resistance — the dominant defect governing postprandial glucose disposal — requires dynamic testing to quantify. The euglycemic-hyperinsulinemic clamp (gold standard), the Matsuda index from an OGTT, and related methods capture the ability of pharmacological insulin concentrations to drive glucose uptake into muscle, a process that is essentially silent in the fasting state [3, mechanism_review]. A patient can have severely impaired peripheral insulin sensitivity while maintaining a modest HOMA-IR if their hepatic response to basal insulin remains partially intact — a dissociation that is common in early obesity-related insulin resistance and explains why HOMA-IR underestimates the severity of insulin resistance in populations where peripheral resistance predominates.

This does not diminish HOMA-IR's value. As a fasting-state hepatic surrogate, it is highly practical — requiring a single blood draw, no infusion protocol, and no specialized laboratory beyond standard glucose and insulin assays — and it predicts type 2 diabetes incidence and metabolic risk robustly at the population level [3, mechanism_review; 5, cohort]. Its appropriate domain is epidemiological characterization, baseline assessment, and longitudinal tracking of hepatic insulin sensitivity in response to lifestyle or pharmacological intervention, interpreted with awareness that it does not capture the full picture of whole-body insulin action.

---

## Bibliography

[1]. Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. Homeostasis model assessment: insulin resistance and beta-cell function from fasting plasma glucose and insulin concentrations in man. *Diabetologia*. 1985;28(7):412–419. PMID: 3899825. DOI: 10.1007/BF00280883. — tag: cohort — tier: 1

[2]. Tripathy D, Almgren P, Tuomi T, Groop L. Contribution of insulin-stimulated glucose uptake and basal hepatic insulin sensitivity to surrogate measures of insulin sensitivity. *Diabetes Care*. 2004;27(9):2204–2210. PMID: 15333485. DOI: 10.2337/diacare.27.9.2204. — tag: cohort — tier: 1

[3]. Wallace TM, Levy JC, Matthews DR. Use and abuse of HOMA modeling. *Diabetes Care*. 2004;27(6):1487–1495. PMID: 15161807. DOI: 10.2337/diacare.27.6.1487. — tag: mechanism_review — tier: 1

[4]. Levy JC, Matthews DR, Hermans MP. Correct homeostasis model assessment (HOMA) evaluation uses the computer program. *Diabetes Care*. 1998;21(12):2191–2192. PMID: 9839117. DOI: 10.2337/diacare.21.12.2191. — tag: cohort — tier: 1

[5]. Hill NR, Levy JC, Matthews DR. Expansion of the homeostasis model assessment of β-cell function and insulin resistance to enable clinical trial outcome modeling through the interactive adjustment of physiology and treatment effects: iHOMA2. *Diabetes Care*. 2013;36(8):2324–2330. PMID: 23564921. DOI: 10.2337/dc12-0607. — tag: cohort — tier: 1

[6]. Reaven GM. What do we learn from measurements of HOMA-IR? *Diabetologia*. 2013;56(8):1867–1868. PMID: 23722624. DOI: 10.1007/s00125-013-2948-3. — tag: mechanism_review — tier: 1
