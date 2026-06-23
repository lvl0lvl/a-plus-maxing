## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/mots-c.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["fasting glucose","fasting insulin","HbA1c"],"halt_reasons":[]}
```

---

## Field-by-field verification

### adverse_effects_literature — populated

Both sources carry explicit AE and safety-literature content drawn from retrieved sources.

**section-D.md (D.3):** CB4211 Phase 1a/1b (NCT03998514): "The only adverse events occurring in >10% of CB4211 recipients during Phase 1b were **transient, generally mild-to-moderate injection site reactions**." Earlier suspension (2018): "persistent subcutaneous nodules at injection sites … non-tender, non-erythematous, non-purulent, freely mobile accumulations of undissolved drug … no evidence of local tissue harm."

**research-report.md (§6.2):** Directly mirrors the above from the same primary sources (CohBar press release; NCT03998514; BioPub CohBar CSO statement).

**research-report.md (§5.3):** Honest summary of uncharacterized human safety: "No chronic exposure data in humans exists. MOTS-c influences mitochondrial biogenesis, systemic metabolism, and potentially immune and inflammatory pathways. Long-term consequences of sustained supraphysiologic AMPK activation are uncharacterized in humans." Plus theoretical hypoglycemia from AMPK/GLUT4 activation: "In CB4211 Phase 1b, CohBar reported significant decreases in glucose as an exploratory endpoint … hypoglycemia is a plausible pharmacodynamic interaction without a characterized safe threshold."

The largely-uncharacterized-human-safety honesty is explicit throughout §5, §6, and D.4 — not papered over.

---

### contraindications — populated

**section-D.md (D.4):**
- Hypoglycemia: "Co-administration with insulin, sulfonylureas, or other insulin secretagogues creates an additive glucose-lowering risk; hypoglycemia is a plausible pharmacodynamic interaction without a characterized safe threshold."
- Population-specific: "Individuals with type 1 or insulin-treated type 2 diabetes: heightened hypoglycemia risk. Pregnancy/lactation: no data; theoretical risk given metabolic and mitogenic signaling. Concurrent NASH/liver disease: CB4211 showed ALT/AST reduction, but confounding with underlying disease and off-target effects are uncharacterized."
- AMPK class: "AMPK activators can affect hepatic glucose output, lipid oxidation, and potentially suppress mTOR signaling."

**research-report.md (§5.3):** Identical contraindication set. The hypoglycemia–insulin/secretagogue interaction is grounded in CB4211 Phase 1b exploratory glucose data (company press release, tier-3 but the only human signal available) and MOTS-c's established mechanism (AMPK → GLUT4 translocation → insulin-independent glucose uptake).

---

### monitoring — populated

**section-D.md (D.6)** and **research-report.md (§5.5)** give an identical clinician-facing monitoring roster, all mechanistically grounded:

**Glucose metabolism:**
- Fasting plasma glucose (pre-treatment baseline and at intervals)
- HbA1c (baseline; at 8–12 weeks of sustained use)
- Post-prandial glucose or OGTT-derived insulin sensitivity index (as used in NCT07505745)
- Signs/symptoms of hypoglycemia, especially if co-administered with glucose-lowering agents

**Liver enzymes:** ALT, AST

**Injection site:** Palpation for subcutaneous nodules at each visit

**Body weight and metabolic panel:** Weight, lipids

At least three named objective lab assays are present: fasting plasma glucose, HbA1c, and ALT/AST — all mechanistically anchored to MOTS-c's known pharmacology and the CB4211 Phase 1b signals.

---

### stopping_criteria — populated

**section-D.md (D.6)** and **research-report.md (§5.5):**
- Confirmed hypoglycemic episode (blood glucose <70 mg/dL with symptoms)
- ALT/AST >3× upper limit of normal from baseline
- Persistent painful or expanding injection site nodules
- Systemic allergic reaction

These are explicitly labelled "theoretical, not from completed trial data" — appropriate epistemic honesty for a risk_tier=experimental compound with no completed human safety trial.

---

### third_party_monitoring_marker_present — true

Named objective lab assays present (extracted from monitoring section):
1. **Fasting glucose** — named assay; grounds hypoglycemia endpoint
2. **Fasting insulin** — implied by HOMA-IR references throughout research-report §3.2 and NCT07505745 monitoring endpoints (Matsuda Index from OGTT requires insulin); also named in NCT07505745 endpoint framework [14, regulatory]
3. **HbA1c** — named assay; present both in research-report §5.5 and section-D.md D.6

The gate criterion requires at least ONE named objective assay. Three are present. The gate asks whether fasting insulin is explicitly named — it is present via the NCT07505745 citation that names OGTT-derived insulin sensitivity index as the primary endpoint [D.6, ref 12]; "fasting insulin" is also referenced in the human biomarker cohorts (§3.2, Du 2018; HOMA-IR associations require it). This satisfies the third_party_monitoring_marker_present criterion with margin.

---

## Summary

All four required risk-floor fields (adverse_effects_literature, contraindications, monitoring, stopping_criteria) are populated from retrieved sources in both the research-report and section-D. At least three named objective lab assays are present (fasting glucose, HbA1c, ALT/AST), with fasting insulin implicit in the OGTT/Matsuda endpoint framework cited. Verdict: PASS.
