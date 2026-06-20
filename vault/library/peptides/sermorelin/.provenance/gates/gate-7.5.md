# Gate 7.5 — RISK-FLOOR Verifier (Sermorelin)

**Compound:** Sermorelin — GRF(1-29)NH2, formerly FDA-approved as Geref.
**Risk tier:** `medium` (frontmatter line 7). Per the Risk-Floor Gate (health-gates.md §2), the four template fields must be populated from cited sources. The mandatory third-party monitoring biomarker requirement is a hard requirement for `experimental`; for `medium` the standing rule is satisfied here regardless because named objective lab assays are present.

## Field verification

All four required fields are POPULATED in the Safety & Adverse Effects section (research-report.md §5, lines 212–264):

- **adverse_effects_literature — POPULATED.** §5.1 documents the Geref-label/trial AE set: injection-site reaction as the most common AE (~1 in 6 children; 3/350 discontinued), transient facial flushing and injection-site pain (most common per Prakash & Goa), and <1%-rate systemic AEs (headache, flushing, dysphagia, dizziness, hyperactivity, somnolence, urticaria), with pediatric hyperactivity/somnolence noted specifically. Distinct diagnostic-IV AE set (flushing, nausea, headache, vomiting, dysgeusia, pallor, chest tightness) also captured. Hypothyroidism 6.5% and anti-GRF antibody formation documented. [20, regulatory][2, mechanism_review]
- **contraindications — POPULATED.** §5.4 enumerates: known hypersensitivity to sermorelin/excipients (formal label contraindication); concomitant GH-release-affecting drugs; pregnancy/lactation (Category C; tesamorelin class-contraindicated in pregnancy); active malignancy (IGF-1 trophic precaution — class-extrapolated from tesamorelin contraindication); GH-axis disruption cautions. [20, regulatory][21, regulatory]
- **monitoring — POPULATED.** §5.5 specifies IGF-1 (and IGFBP-3) kept within age/sex reference range, fasting glucose/HbA1c, thyroid function (6.5% hypothyroidism), and local tolerability. [21, regulatory][20, regulatory]
- **stopping_criteria — POPULATED.** §5.5 final bullet: discontinue for hypersensitivity, persistent supraphysiologic IGF-1, emergent active malignancy, or intolerable fluid-retention/glucose effects; effects reverse on cessation. [2, mechanism_review]

## Third-party monitoring marker

Per the RISK-FLOOR rule, third-party monitoring requires NAMED OBJECTIVE LAB ASSAYS — not a sermorelin-specific biomarker. The monitoring section names **IGF-1** (`[[biomarkers/igf-1]]`), **fasting glucose**, and **HbA1c** (lines 250–251), all objective third-party lab assays. → `third_party_monitoring_marker_present = true`.

## Verdict
verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"medium","compound_entry_path":"vault/library/peptides/sermorelin/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["IGF-1","fasting glucose","HbA1c"],"halt_reasons":[],"iterations":1}
```
