# Gate 7.5 — Risk-Floor Verifier (Retatrutide)

**Compound:** Retatrutide (LY3437943) — triple GIP/GLP-1/glucagon receptor agonist
**risk_tier:** experimental (INVESTIGATIONAL, unapproved by any regulator)
**Entry:** `vault/library/peptides/retatrutide/research-report.md`

Because the compound entry carries `risk_tier: experimental`, the risk-floor gate requires all four safety scaffolding fields to be populated from retrieved (Phase-2-trial-grounded) sources, and — per the experimental-tier special case — at least one third-party objective monitoring biomarker must be named (subjective self-report is insufficient).

## Field verification

- **adverse_effects_literature — POPULATED.** §5 documents a dose-dependent, titration-mitigated GI-dominant AE profile (nausea up to 60%, vomiting up to 26%, diarrhea, constipation) [3]; the glucagon-component dose-dependent heart-rate increase peaking at week 24 [3]; a retatrutide-specific cutaneous-hyperesthesia signal (~7% vs 1% placebo, dose-dependent to 14%) [3]; a transient early eGFR decrease (week 12) that recovers to net improvement by 48 weeks [12]; supraventricular-arrhythmia AE-of-special-interest (6% overall); one serious pancreatitis AE; explicit absence of long-term/CV-outcome/human-thyroid data; and a class-extrapolated (rodent) C-cell concern flagged as not measured in humans [3][5][6][12].

- **contraindications — POPULATED.** §5.5 gives precautionary/mechanism-derived contraindications appropriate to an investigational agent with no formal label: pregnancy/breastfeeding (no human reproductive-safety data); pre-existing tachyarrhythmia / conditions where sustained HR rise is hazardous (glucagon HR signal); history of pancreatitis or symptomatic gallbladder disease; concomitant insulin/sulfonylurea (titration hypoglycemia); and class-precautionary MTC/MEN-2 personal/family history (extrapolated from GLP-1 labeling) [3]. Active-malignancy/IGF-GLP class precaution is consistent with this precautionary frame.

- **monitoring — POPULATED.** §5.5 names objective measures: heart rate (signature glucagon effect); glucose / fasting glucose & HbA1c (especially early and on insulin/secretagogues) [6]; renal function / eGFR (transient early dip) [12]; body weight + nutritional adequacy during rapid loss; plus pancreatitis/biliary symptoms and cutaneous-sensitivity symptoms [3][12].

- **stopping_criteria — POPULATED.** §5.5 "Stopping": intolerable GI AEs (leading discontinuation cause), suspected pancreatitis, marked/symptomatic heart-rate elevation or arrhythmia, or pregnancy [3].

## Risk-floor special case (experimental tier)

The monitoring field references NAMED OBJECTIVE third-party-measurable markers — heart rate, HbA1c / fasting glucose, renal/eGFR (creatinine-based), and body weight — all lab- or clinically-measured rather than self-reported. The experimental-tier third-party-monitoring requirement is satisfied.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"experimental","compound_entry_path":"vault/library/peptides/retatrutide/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["heart rate","HbA1c","fasting glucose","eGFR/creatinine"],"halt_reasons":[],"iterations":1}
```
