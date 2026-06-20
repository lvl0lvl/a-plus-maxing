# Rubric — fasting-glucose (biomarker, standard mode)

**Judge threshold:** 92/100 (standard). Each section judged independently.

## Section plan (4 sections, paired retrieval+judge)
- **A — Physiology & Regulation:** what fasting plasma glucose (FPG) measures; fasting-state glucose homeostasis (hepatic glucose output, insulin/glucagon, peripheral uptake); what drives the fasting set-point; dawn phenomenon; relationship of FPG to overall glycemia.
- **B — Reference Ranges, Units & Diagnostic Thresholds:** ADA vs WHO normal / impaired-fasting-glucose (prediabetes) / diabetes cutoffs; "optimal" vs "diagnostic" framing; mg/dL ↔ mmol/L (÷18.0 / ×18.0); population distributions/percentiles.
- **C — Measurement & Pre-analytics:** enzymatic (hexokinase / glucose-oxidase) assay; the 8-h fasting requirement; in-tube glycolysis and tube choice (fluoride-oxalate vs citrate-buffered vs rapid plasma separation); plasma vs serum vs capillary vs point-of-care; biological + analytical variability (CV); FPG vs HbA1c vs OGTT (concordance/discordance).
- **D — Determinants & Clinical Significance:** genetics (GCK/MODY2; common-variant loci) + diet, activity, sleep, stress/cortisol, drugs that raise (glucocorticoids, thiazides, atypical antipsychotics) / lower (metformin, SGLT2i, GLP-1 etc.); what FPG predicts (incident T2D, CV/all-cause mortality); relationship to fasting insulin / HOMA-IR; limitations of a single fasting point.

## Judge dimensions (0-100 each; total = rounded mean of non-null)
- evidence_quality — claims grounded in Tier-1/2 sources at the right design.
- citation_fidelity — every numeric/threshold claim carries a resolvable `[N, tag]`; bibliography complete.
- type_tag_discipline — each source one tag from the whitelist enum; guideline thresholds tagged `regulatory` or `mechanism_review`; no efficacy/number on vendor/anecdote.
- population_annotation — any animal/in-vitro number flagged with species/system (mostly N/A for a human clinical marker).
- route_fidelity — N/A for a biomarker (score null).
- concentration_audit_handling — single-source dominance flagged (for a guideline-based marker, ensure thresholds attributed to the actual issuing body, ADA/WHO/IDF, not a secondary review).
- risk_floor_readiness — null (biomarker, not compound).
- reasoning_integrity — honest framing (FPG single-point variability; FPG vs HbA1c discordance stated, not hidden).
- completeness_vs_brief — section covers its scope.

## Health-specific checks (from references/health-gates)
- Thresholds attributed to the issuing guideline body with year (ADA Standards of Care 20xx; WHO/IDF).
- mg/dL ↔ mmol/L conversions internally consistent (factor 18.0).
- No diagnostic threshold grounded on a secondary blog/vendor source.
