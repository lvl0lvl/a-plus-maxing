# Phase 7.5 — RISK-FLOOR Gate: CJC-1295 (risk_tier=experimental)

Verifier: Phase 7.5 RISK-FLOOR. Source: `vault/library/peptides/cjc-1295/research-report.md` (§6 Safety & Adverse Effects). Rule reference: `references/health-gates.md` §2 (Risk-Floor Gate, Phase 7.5).

The compound entry declares `risk_tier: experimental` (frontmatter line 7; restated in §0 Metadata line 20), which triggers the risk-floor requirement that all four safety fields be populated from cited sources, plus the experimental-tier requirement of at least one named objective lab assay in monitoring.

## Field confirmation

- **adverse_effects_literature — POPULATED.** §6.1 reports the only published human safety dataset (Teichman 2006 `[rct]`): "safe and relatively well tolerated," "no serious adverse reactions," with mild/transient TEAEs (injection-site reactions, transient flushing/warmth, headache); circulating per-event percentages are explicitly flagged UNVERIFIED rather than asserted. §6.3 supplies the GH-axis / GHRH-analogue class risks from the KIMS long-term GH cohort (Johannsson 2022 `[cohort]`, n=15,809): fluid-retention complex (arthralgia, edema, myalgia, paresthesia, carpal tunnel), impaired glucose tolerance / insulin resistance (GH diabetogenic), headache, an associational (flagged non-causal) IGF-1/proliferation concern, and continuous-exposure somatotroph desensitization (Rittmaster 1987). Both the trial tolerability data and the class-risk literature are present and cited.

- **contraindications — POPULATED.** §6.4 lists contraindications / strong cautions: active or recent malignancy; pre-existing diabetes or impaired glucose tolerance; pregnancy and breastfeeding; and caution in significant or uninvestigated cardiovascular / cardiac-fluid states (grounded in the trial's lone death against presumed occult coronary disease). This matches the prompt's expected set (active malignancy; diabetes/glucose intolerance; pregnancy/lactation; cardiac/fluid states).

- **monitoring — POPULATED.** §6.4 specifies baseline + on-treatment monitoring: serum IGF-1 interpreted against age- and sex-specific reference ranges (keep within, not above, normal range), plus fasting glucose and HbA1c for glycaemic drift. Explicitly noted as standard, objective, validated assays.

- **stopping_criteria — POPULATED.** §6.4 enumerates stopping criteria: IGF-1 rising above age/sex reference range; new or worsening glucose intolerance; new fluid-retention symptoms (edema, paresthesia, carpal-tunnel symptoms, arthralgia); any new or suspicious mass / malignancy; any new cardiac symptoms. Field is present and non-empty.

## Third-party monitoring marker (experimental-tier requirement)

The risk-floor rule requires a NAMED OBJECTIVE LAB ASSAY, not a CJC-1295-specific validated biomarker. §6.4 names three objective, validated assays: **IGF-1** (held within age/sex reference range), **fasting glucose**, and **HbA1c**. These satisfy the requirement. No compound-specific biomarker is required and none is fabricated. → `third_party_monitoring_marker_present = true`.

## Verdict

verdict: PASS

All four required risk fields are populated from cited sources, and the experimental-tier objective-assay requirement is met by IGF-1 / fasting glucose / HbA1c. No fields are genuinely unpopulated; no false-HALT warranted.

```json
{
  "phase": "7.5",
  "verdict": "PASS",
  "compound_risk_tier": "experimental",
  "compound_entry_path": "vault/library/peptides/cjc-1295/research-report.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "populated"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": ["IGF-1", "fasting glucose", "HbA1c"],
  "halt_reasons": [],
  "iterations": 1
}
```
