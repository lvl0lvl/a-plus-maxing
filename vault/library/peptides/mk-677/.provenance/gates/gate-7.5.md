# Gate 7.5 — RISK-FLOOR Verifier (MK-677)

**Compound:** MK-677 (ibutamoren) — oral, non-peptidic small-molecule GHS-R1a (ghrelin-receptor) agonist / GH secretagogue.
**risk_tier:** medium (unapproved oral GH secretagogue; dominant metabolic harm signal + CHF signal).
**Entry verified:** `vault/library/peptides/mk-677/research-report.md`, §5 Safety & Adverse Effects (lines 203–260).

## Verification

All four required risk-profile fields are POPULATED and citation-grounded in the report's Safety section:

- **adverse_effects_literature — POPULATED.** The dominant, best-replicated harm is METABOLIC: raised fasting glucose (+0.3 mmol/L over 2 yr [Nass 2008]; 5.4 → 6.8 mmol/L at 4 wk [Chapman 1996]; OGTT impairment in obese men [Svensson 1998]), reduced insulin sensitivity, and raised HbA1c (review-level) (§5.1). Plus increased appetite (on-target ghrelin agonism), transient peripheral edema/fluid retention, arthralgia/myalgia, a modest/inconsistent cortisol rise, probable lethargy/fatigue, and the trial-derived congestive-heart-failure (CHF) signal (~6.5% vs ~1.7%, Adunsky 2011) (§5.2–5.3). Theoretical IGF-1 malignancy and acromegaly-like class risks distinguished from trial-observed AEs (§5.4).

- **contraindications — POPULATED.** Diabetes mellitus / impaired fasting glucose / impaired glucose tolerance; congestive heart failure or significant cardiac risk / reduced cardiac reserve; active or recent malignancy; pregnancy and lactation (§5.5).

- **monitoring — POPULATED.** Fasting glucose + HbA1c as PRIMARY surveillance labs (baseline + on-treatment); add OGTT if pre-diabetic; IGF-1 to bound target engagement / malignancy-relevant exposure; clinical surveillance for edema and cardiac decompensation (§5.5).

- **stopping_criteria — POPULATED.** Discontinue for new/worsening edema with weight gain or dyspnea (possible CHF), for a clinically meaningful rise in fasting glucose/HbA1c into/toward the diabetic range, or for any sign of cardiac decompensation; the hip-fracture trial's early termination is cited as precedent (§5.5).

**RISK-FLOOR RULE (third-party monitoring marker).** Monitoring references NAMED OBJECTIVE LAB ASSAYS — fasting glucose, HbA1c, and IGF-1 — not self-reported subjective measures. Marker present → `third_party_monitoring_marker_present = true`.

No fields are empty or placeholder-only. No HALT conditions triggered.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"medium","compound_entry_path":"vault/library/peptides/mk-677/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["fasting glucose","HbA1c","IGF-1"],"halt_reasons":[],"iterations":1}
```
