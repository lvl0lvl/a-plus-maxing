# Phase 7.5 — RISK-FLOOR Gate: Semaglutide

**Compound:** Semaglutide (GLP-1 receptor agonist)
**risk_tier:** medium (approved GLP-1 RA)
**Entry:** `vault/library/peptides/semaglutide/research-report.md`

## Summary

The Semaglutide report carries a complete, RCT- and label-grounded risk profile. All four required fields are populated and — as expected for an FDA/EMA-approved, hard-endpoint-trialed molecule — they are STRONG (Tier-1 label + large RCT sourced), not placeholder.

- **adverse_effects_literature — POPULATED.** §5 is an exhaustive safety section: GI-dominant AEs as the primary discontinuation driver (Wegovy nausea 44%, diarrhea 30%, vomiting 24%, constipation 24%; dose-dependent; §5.1); weight regain on discontinuation (~two-thirds within a year, STEP-1 extension, §5.2); lean-mass loss (~39–45% of weight lost, §5.3); gallbladder disease (cholelithiasis 1.6% vs 0.7%; RR ~1.37, §5.4); pancreatitis (labeled precautionary warning, §5.4); gastroparesis/ileus and peri-operative aspiration with ASA hold guidance (§5.5); diabetic retinopathy (SUSTAIN-6 HR 1.76, §5.6 / §3.1); the rodent thyroid C-cell / MTC BOXED WARNING stated precisely as rodent-derived, not human-demonstrated (§5.7); and the investigated-but-not-confirmed suicidality signal (§5.8). Every item the brief enumerated is present.

- **contraindications — POPULATED.** §5.9: personal/family history of medullary thyroid carcinoma (MTC); Multiple Endocrine Neoplasia syndrome type 2 (MEN 2); prior serious hypersensitivity to semaglutide or any excipient; plus pregnancy as a labeled caution (animal reproductive toxicity; discontinue before planned conception given the ~1-week half-life). Label-cited [20, 21, regulatory].

- **monitoring — POPULATED.** §5.9: renal function during GI-driven volume loss (AKI caution, §5.1); gallbladder symptom surveillance; pancreatitis symptom surveillance; retinal status in patients with prior diabetic retinopathy; hypoglycemia when co-administered with insulin/sulfonylureas. NAMED OBJECTIVE labs explicitly listed: HbA1c (glycemic efficacy/safety in the diabetic context), eGFR + serum creatinine (renal/AKI), and lipase if pancreatitis is suspected — plus body weight as the response measure. IGF-1 correctly noted as not relevant for a GLP-1 RA.

- **stopping_criteria — POPULATED.** §5.9: discontinue promptly if pancreatitis is suspected; hold per ASA guidance before anesthesia (~1 week pre-op for weekly formulations); discontinue for serious hypersensitivity. Cited [20, 25, regulatory/mechanism_review].

**RISK-FLOOR RULE check.** Third-party monitoring requires NAMED OBJECTIVE clinical/lab measures. The report names HbA1c, fasting/serum glucose, body weight, renal panel (eGFR/creatinine), and lipase (pancreatitis workup) — all standard third-party objective assays. Marker requirement satisfied → `third_party_monitoring_marker_present=true`.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"medium","compound_entry_path":"vault/library/peptides/semaglutide/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["HbA1c","fasting glucose","body weight","renal function (eGFR/creatinine)"],"halt_reasons":[],"iterations":1}
```
