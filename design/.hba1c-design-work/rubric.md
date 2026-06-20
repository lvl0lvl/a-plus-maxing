# Rubric — hba1c (biomarker, standard mode)

**Judge threshold:** 92/100 (standard). Each section judged independently. route_fidelity + risk_floor_readiness = null (biomarker).

## Section plan (4 sections, paired retrieval+judge)
- **A — Physiology & What It Measures:** non-enzymatic glycation of the hemoglobin β-chain N-terminal valine; HbA1c as a time-integrated index of ~8–12-week mean glycemia weighted to the recent 30 days; dependence on RBC lifespan (~120 d); relationship to mean/estimated average glucose (eAG); why it is a retrospective average, not a spot value.
- **B — Reference Ranges, Units & Diagnostic Thresholds:** ADA: normal < 5.7%, prediabetes 5.7–6.4%, diabetes ≥ 6.5% (confirmed); individualized treatment targets (<7% general; <6.5% / <8% context-dependent); NGSP % ↔ IFCC mmol/mol conversion (the master equation IFCC = (NGSP−2.15)×10.929); eAG (ADAG) mapping (eAG mg/dL = 28.7×A1c − 46.7); population percentiles.
- **C — Measurement, Standardization & Interferences:** NGSP/IFCC standardization + DCCT anchoring; methods (HPLC ion-exchange, boronate affinity, immunoassay, enzymatic, POC); interferences that FALSELY raise/lower (hemoglobinopathies HbS/C/E/F, iron-deficiency anemia raises, hemolysis/↑RBC-turnover/recent blood loss/EPO lower, uremia/carbamylation, pregnancy); analytical + biological variability; the discordance with fructosamine/glycated albumin when RBC turnover is abnormal.
- **D — Determinants & Clinical Significance:** the glycation gap / hemoglobin glycation index; ethnicity offset; what HbA1c predicts (microvascular DCCT/UKPDS; macrovascular; all-cause mortality; the J-shaped relationship); HbA1c vs FPG vs OGTT discordance for diagnosis; drugs/conditions; limitations (cannot capture glycemic variability/hypoglycemia; the average can hide swings).

## Judge dimensions (0-100; total = rounded mean of non-null)
evidence_quality, citation_fidelity, type_tag_discipline, population_annotation, route_fidelity(null), concentration_audit_handling, risk_floor_readiness(null), reasoning_integrity, completeness_vs_brief.

## Tag-discipline rules the judge MUST enforce (lessons baked in)
- Diagnostic thresholds → attribute to the ISSUING body (ADA Standards of Care year; WHO 2011 HbA1c-for-diagnosis) tagged `regulatory`. NOT to StatPearls/Endotext/a secondary review.
- StatPearls / Endotext / NCBI Bookshelf / narrative reviews → `mechanism_review` (NEVER `regulatory`, `meta_analysis`, or `rct`).
- Effect sizes / risk ratios / trial results → `rct` (DCCT, UKPDS, ADVANCE, ACCORD) or `meta_analysis` or `cohort`; name the trial/cohort.
- Any animal/in-vitro number → flagged with species inline.
- Conversions internally consistent (NGSP↔IFCC master equation; eAG equation).
- No numeric/threshold on `vendor_label`/`anecdote_aggregate`; reviews don't ground effect sizes.
- Verify enrollment/N figures against the actual source (the fasting-glucose Cha-2013 lesson).
