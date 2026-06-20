# Rubric — fasting-insulin (biomarker, standard mode)

**Judge threshold:** 92/100. route_fidelity + risk_floor_readiness = null (biomarker).

## Section plan (4 sections, paired retrieval+judge)
- **A — Physiology & What It Measures:** pancreatic β-cell insulin secretion; fasting (basal) insulin as the integral of basal secretion + hepatic insulin resistance; co-secretion with C-peptide (1:1 molar, C-peptide better reflects secretion due to no hepatic first-pass); ~50% hepatic first-pass extraction of insulin; pulsatile secretion; proinsulin/split products; why fasting insulin indexes basal hepatic insulin sensitivity + secretory tone.
- **B — Reference Ranges, Units & Thresholds:** the load-bearing caveat — **NO universally agreed cutpoint** (assay-dependent + population-dependent). Typical adult fasting insulin ~2–25 µIU/mL (often cited); "optimal/insulin-sensitive" commonly framed <~5–8 µIU/mL; give the µIU/mL ↔ pmol/L conversion (×6.0, some use ×6.945 — state which). HOMA-IR / QUICKI / HOMA-β / fasting insulin-resistance indices as the contextualizing tools (give the formulas). Population distributions where available. Make the "no validated diagnostic threshold" point explicit.
- **C — Measurement & Standardization:** the central problem — **insulin immunoassays are NOT harmonized/standardized**; proinsulin + split-product cross-reactivity differs by assay (RIA vs ELISA vs chemiluminescence vs the IFCC/ADA insulin-standardization workgroup effort); inter-assay disagreement can be large; pre-analytics (hemolysis degrades insulin via insulin-degrading enzyme; prompt separation; fasting requirement); high analytical + biological variability; why absolute cutpoints don't transfer across labs/assays.
- **D — Determinants & Clinical Significance:** hyperinsulinemia as the hallmark/earliest marker of insulin resistance (precedes glucose rise); fasting insulin / HOMA-IR predicts incident T2D, MASLD/NAFLD, metabolic syndrome, CVD (cite cohorts/meta-analyses); the compensatory-hyperinsulinemia → β-cell-failure trajectory (insulin rises then falls); determinants that raise (obesity, IR, refined-carb diet, inactivity, sleep loss) / lower (exercise, weight loss, low-carb, metformin, SGLT2i indirectly); limitations — assay non-standardization undermines absolute interpretation; single fasting point.

## Judge dimensions (0-100; total = rounded mean of non-null)
evidence_quality, citation_fidelity, type_tag_discipline, population_annotation, route_fidelity(null), concentration_audit_handling, risk_floor_readiness(null), reasoning_integrity, completeness_vs_brief.

## Tag-discipline rules the judge MUST enforce
- StatPearls / Endotext / NCBI Bookshelf / narrative reviews → `mechanism_review` (NEVER `regulatory`/`meta_analysis`/`rct`).
- Effect sizes / risk ratios / cohort associations → `rct`/`meta_analysis`/`cohort` (NAME the cohort/trial).
- Standards-body statements (ADA, IFCC insulin standardization) → `regulatory`. (ngsp.org + ifcc.org are now whitelisted Tier 2.)
- Reference ranges: state honestly that there is no harmonized cutpoint; attribute any quoted range to its source + assay.
- µIU/mL ↔ pmol/L conversion internally consistent; HOMA-IR/QUICKI formulas correct.
- No numeric on `vendor_label`/`anecdote_aggregate`/off-whitelist; every inline cite `[N, tag]` (no bare `[N]`); VERIFY enrollment N + effect sizes against the source.
