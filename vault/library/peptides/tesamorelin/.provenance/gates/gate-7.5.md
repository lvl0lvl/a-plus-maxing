# Gate 7.5 — Risk-Floor Verification: Tesamorelin

**Compound:** Tesamorelin (Egrifta / Egrifta SV / Egrifta WR; Theratechnologies)
**Risk tier:** medium (FDA-approved Rx; well-characterized, monitorable, reversible safety profile)
**Entry path:** `vault/library/peptides/tesamorelin/research-report.md`
**Verifier phase:** 7.5 (Risk-Floor Gate, health-gates.md §2)

## Summary

The risk-floor gate requires the four named Risk Profile fields to be populated from cited sources. Although the §2 health-gates rule formally triggers HALT only at `risk_tier: experimental|high`, this report is `risk_tier: medium` and was verified affirmatively — all four fields are not merely present but STRONG, grounded directly in the current Egrifta WR FDA prescribing label [2] plus the two pivotal Phase 3 RCTs (~806 pooled) [10][11][12]. The Safety section (§5) is the most complete risk scaffolding in the library to date.

Field-by-field findings:

- **adverse_effects_literature — POPULATED.** §5.1 enumerates label + RCT AE rates at ≥1% vs placebo: injection-site reactions (17% vs 6%; 25% all-events vs 14%), arthralgia (13% vs 11%), pain in extremity (6% vs 5%), myalgia (6% vs 2%), peripheral edema (6% vs 2%), paresthesia (5% vs 2%), hypoesthesia (4% vs 2%), carpal tunnel (1% vs 0%). The glucose signal is reported two-sided in §5.3 (mean glucose parameters unchanged in trials, but label HbA1c≥6.5% crossing 5% vs 1%, OR 3.3 [CI 1.4, 9.6]). IGF-1 supraphysiologic elevation quantified in §5.2 (47% >2 SDS, 36% >3 SDS at 26 wk). All cited [2][10][11].

- **contraindications — POPULATED.** §5.5 lists all four FDA-label contraindications: (1) HPA-axis disruption (hypophysectomy, hypopituitarism, pituitary tumor/surgery, head irradiation/trauma); (2) active malignancy; (3) known hypersensitivity to tesamorelin or excipients including mannitol; (4) pregnancy. Cited [2].

- **monitoring — POPULATED.** §5.6 (and §2.6) directs: monitor IGF-1 (keep within normal range; consider discontinuing for persistent >3 SDS), fasting glucose / HbA1c, clinical signs of fluid retention, and retinopathy screening in diabetics. Pre-initiation glucose status + malignancy screen. Cited [2].

- **stopping_criteria — POPULATED.** §5.6 lists: persistent IGF-1 elevation (>3 SDS), new/recurrent malignancy, uncontrolled glucose intolerance/diabetes, pregnancy, serious hypersensitivity, acute critical illness, and non-response. Cited [2].

**Risk-floor rule (third-party monitoring marker):** the monitoring field names three objective lab assays — IGF-1, fasting glucose, and HbA1c — all in §5.6 (line 294) and corroborated in §2.6 (IGF-1 normalization-range targeting). Named objective lab assays present → `third_party_monitoring_marker_present = true`. Self-reported subjective monitoring is not relied upon.

No halt conditions. All four fields are populated and STRONG.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"medium","compound_entry_path":"vault/library/peptides/tesamorelin/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["IGF-1","fasting glucose","HbA1c"],"halt_reasons":[],"iterations":1}
```
