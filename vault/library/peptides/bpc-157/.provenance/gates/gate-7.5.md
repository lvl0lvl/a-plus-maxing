# Gate 7.5 — Risk-Floor Verifier (Phase 7.5)

Compound: BPC-157 · risk_tier: **experimental** · entry: `/tmp/aplus-research/bpc-157/research-report.md`

## Verdict

verdict: PASS

All risk-floor fields required for an `experimental`-tier entry are present and either sourced or honestly marked as practitioner-convention.

- **Risk Profile › contraindications** — POPULATED, cited. §6.5 "Contraindication candidates" table (active malignancy, pregnancy/lactation, anticoagulant/antiplatelet + bleeding disorders, cardiovascular disease, severe hepatic/renal impairment), each with a stated mechanistic basis and sourcing tier citing mechanism-review [2][3] and/or practitioner-convention [33]; reinforced by §6.2 (oncologic precaution) and §6.4 (NO-system interaction theory). Sourcing tiers are honestly labeled (mechanism vs practitioner-convention).
- **Risk Profile › monitoring** — POPULATED, cited. §6.6 documents the lab/biomarker panel from the human IV pilot (vital signs, ECG, cardiac/hepatic/renal/thyroid/metabolic labs) [33b, open_label]; §6.1 notes the creatinine signal [28]; §6.7 states the practitioner-convention posture ("malignancy + lab monitoring," conservative cycling — explicitly "convention, not evidence"). Named lab assays satisfy the experimental-tier third-party (non-self-reported) monitoring requirement.
- **Trial Status › stopping criteria** — PRESENT, honestly marked. §6.7 states there is "no validated, human-evidence-based stopping rule for BPC-157" (cycling is convention only); §8 (N=1 / Trial-Design Considerations) carries the operator-specific pointer (response window unknown in humans; outcome measures indication-dependent; operator-specific fields left blank by design). Field is present and honestly labeled, per the library-canonical allowance.

Adverse-effects-literature (schema's fourth required field) is also POPULATED + cited (§6.1 animal toxicology; §6.6 human-pilot AE pattern).

```json
{
  "phase": "7.5",
  "compound_risk_tier": "experimental",
  "compound_entry_path": "/tmp/aplus-research/bpc-157/research-report.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "placeholder-with-pointer"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": [
    "creatinine (renal lab assay, §6.1/§6.6)",
    "ECG (§6.6)",
    "hepatic/renal/thyroid/metabolic lab panel (§6.6)"
  ],
  "halt_reasons": []
}
```
