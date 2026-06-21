# Gate 7.5 — Risk-Floor Verifier: Tirzepatide

**Compound:** Tirzepatide (dual GIP/GLP-1 receptor agonist; Mounjaro / Zepbound)
**risk_tier:** medium (approved, well-characterized, but real AE profile)
**Entry:** `vault/library/peptides/tirzepatide/research-report.md`
**Verified against:** report §5 (Safety & Adverse Effects, lines 177-222) + `references/health-gates.md` §2

## Summary

The Risk-Floor gate requires that the four safety scaffolding fields be populated, cited, and grounded in label/RCT evidence for any entry at `risk_tier: experimental|high`. Tirzepatide is `risk_tier: medium`, which is below the mandatory floor; this verification is run as a precautionary RISK-FLOOR pass and confirms a **complete** risk profile regardless.

All four required fields are POPULATED and grounded in FDA-label content (Mounjaro [20], Zepbound [21]) and pivotal RCTs (SURMOUNT-4 [9], SURMOUNT-1 body-comp substudy [24], perioperative multi-society guidance [25-periop]):

- **adverse_effects_literature** — POPULATED (§5.1–§5.7). GI events dominant and the main discontinuation driver [20][21]; acute gallbladder disease (cholecystitis 0.7% vs 0.2%) [21]; acute pancreatitis (labeled warning, prior-pancreatitis excluded) [21]; delayed gastric emptying → gastroparesis/ileus and peri-operative aspiration concern [25-periop]; predictable weight regain on discontinuation (SURMOUNT-4: +14.0% on switch to placebo) [9]; lean/fat-free mass loss (~26% of weight lost, DXA substudy) [24]; rodent-based thyroid C-cell / MTC boxed warning, human relevance undetermined [20]; hypoglycemia chiefly with concomitant insulin/sulfonylurea [21].
- **contraindications** — POPULATED (§5.8). Personal/family history of MTC or MEN 2; known serious hypersensitivity to tirzepatide/excipients [20][21]; not recommended in pregnancy (animal reproductive toxicity; discontinue when pregnancy recognized) and possible reduced oral-contraceptive efficacy [21].
- **monitoring** — POPULATED (§5.8). Glycemic and weight response; hydration and renal function during persistent GI symptoms (AKI from volume depletion); gallbladder and pancreatitis symptom surveillance; retinopathy in at-risk diabetics; objective labs HbA1c, basic metabolic/renal panel, lipase if pancreatitis suspected [20][21].
- **stopping_criteria** — POPULATED (§5.8). Discontinue if pancreatitis is suspected; discontinue for serious hypersensitivity; evaluate/stop on thyroid nodule or elevated calcitonin; mitigate GI intolerance by slowing/pausing titration before abandoning therapy [20][21].

**Third-party monitoring marker (RISK-FLOOR rule):** the report names objective, lab/instrument-measured markers — HbA1c, clinically-significant fasting glucose (<54 mg/dL), body weight, renal function (eGFR/creatinine / basic metabolic panel), and lipase if pancreatitis suspected. Named objective measures present → `third_party_monitoring_marker_present=true`.

No field is empty, missing, or placeholder-only. No HALT conditions triggered.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"medium","compound_entry_path":"vault/library/peptides/tirzepatide/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["HbA1c","fasting glucose","body weight","renal function (eGFR/creatinine)"],"halt_reasons":[],"iterations":1}
```
