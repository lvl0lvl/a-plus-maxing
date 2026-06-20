# Gate 7.5 — RISK-FLOOR Verifier (Hexarelin)

**Compound:** Hexarelin (examorelin) — `risk_tier: experimental` (unapproved GHRP / ghrelin-receptor agonist; never past Phase II; no product label; non-selective HPA/prolactin co-stimulation; measurable acute cardiac/hemodynamic effects).

**Rule applied (health-gates §2).** An `experimental`-tier compound entry must populate four template fields from cited sources, and — because the tier is `experimental` — at least one monitoring item must reference a named objective lab assay (subjective self-report alone is insufficient).

## Field verification (source: research-report.md §5 Safety & Adverse Effects)

- **adverse_effects_literature — POPULATED.** §5.1 documents observed trial AEs: transient facial flushing/warmth [11]; cortisol/ACTH/prolactin co-elevation (non-selectivity; ACTH/cortisol comparable to hCRH [11], cortisol ~40% / prolactin ~180% rises [2_massoud]); cardiac/hemodynamic effects including a measurable mean-arterial-pressure rise during the 24-patient bypass study [22]; decreased slow-wave sleep [11]. §5.3 carries GH/IGF-1 class risks explicitly flagged as extrapolated via `[dose-extrapolation]` (glucose intolerance, fluid retention/arthralgia/CTS, IGF-1–cancer association). Class-risk vs. observed-AE distinction is explicit.
- **contraindications — POPULATED.** §5.4: active/recent malignancy; uncontrolled diabetes / significant glucose intolerance; cardiac conditions / hemodynamically fragile patients; hyperprolactinemia; pregnancy and lactation; known hypersensitivity.
- **monitoring — POPULATED.** §5.5: IGF-1 (interpreted against age- and sex-specific reference range, `[[biomarkers/igf-1]]`); fasting glucose ± HbA1c; prolactin and morning cortisol with chronic dosing; blood pressure / heart rate.
- **stopping_criteria — POPULATED.** §5.5: IGF-1 above upper age/sex range; new/worsening hyperglycemia; significant fluid retention, arthralgia, or carpal-tunnel symptoms; sustained blood-pressure rise; any new cardiac symptom; pregnancy; plus scheduled cycling/washout given within-weeks desensitization.

## Third-party monitoring marker (experimental-tier special case)

Named objective lab assays are present in `monitoring`: **IGF-1**, **fasting glucose**, **HbA1c** (plus prolactin and morning cortisol). IGF-1 carries an explicit `[[biomarkers/igf-1]]` pointer and an age/sex reference-range interpretation rule. The marker requirement is satisfied: `third_party_monitoring_marker_present = true`.

All four required fields are populated from cited sources and the experimental-tier third-party-marker requirement is met. No HALT conditions.

## Verdict
verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"experimental","compound_entry_path":"vault/library/peptides/hexarelin/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["IGF-1","fasting glucose","HbA1c"],"halt_reasons":[],"iterations":1}
```
