## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","iterations":1,"compound_risk_tier":"medium","compound_entry_path":"vault/compounds/pt-141.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["blood pressure (ambulatory/clinical)","resting heart rate","dermatologic hyperpigmentation exam"],"halt_reasons":[]}
```

---

## Prose Detail

### Field verification

#### adverse_effects_literature — populated

Both source documents provide a comprehensive, sourced AE profile grounded in the RECONNECT Phase 3 trials (n=1,247) and the FDA-approved prescribing information (NDA 210557).

Key content confirmed present:

**Nausea (~40%):** Research report section 4.2 and section-D D.4.2 quote pooled RECONNECT rates: "Nausea occurred in 40.0% vs. 1.3% placebo" [FDA label / DailyMed, regulatory tier 1]. Named as the "primary discontinuation driver" with ~8% discontinuation in the double-blind phase, ~18.7–23.4% in the 52-week extension. Antiemetic pretreatment required in ~13% of patients. Persists through 52 weeks of open-label extension — not a self-limiting first-dose phenomenon.

**Focal hyperpigmentation (face/gingiva/breasts):** Section 4.2 and D.4.3 state: 1% incidence at label regimen (≤8 doses/month); 38% with daily dosing over 8 consecutive days. Mechanism documented as MC1R agonism of melanocytes. **Reversibility explicitly NOT confirmed**: "the label explicitly states resolution cannot be assumed" [1, regulatory].

**Flushing (20.3%), headache (11.3%), injection-site reactions (13.2%):** Tabulated in both documents from pooled RECONNECT data.

**Transient BP elevation:** Mean +6 mmHg systolic / +3 mmHg diastolic, peaking 2–4 h post-dose, resolving within 8–12 h, with compensatory HR decrease up to ~5 bpm [FDA label; White WB et al. 2017, PMID 27977473, ambulatory BP substudy n=397].

**Honest limits documented:**
- Off-label/grey-market use beyond approved scope: sections 3.3, 5.5 and D.2 address population mismatch, unverified purity, dosing without monitoring.
- Unverified-purity grey-market product: Evans-Brown 2009 cited for MT-II/grey-market parallel; compound-identity hazard explicitly discussed.
- MT-II / PT-141 sourcing confusion: section 1.2, 3.3, 5.5 address this directly with structural disambiguation table and grey-market conflation risk.
- Off-label male use without Phase 3 data: sections 3.1, 7.3 document no Phase 3 in men; only integrity-flagged Safarinejad data + small Phase I/II trials.

**Verdict on field: populated** — the well-characterized AE profile and all required honest limits are present in retrieved sources.

---

#### contraindications — populated

Section 4.3 and D.5 quote verbatim from the FDA label [NDA 210557, DailyMed SetID 8c9607a2]:

> "VYLEESI is contraindicated in patients who have uncontrolled hypertension or known cardiovascular disease."

Hard label contraindications present:
1. Uncontrolled hypertension ✓
2. Known cardiovascular disease ✓

Off-label-population caution present: section 3.1 and 7.3 address the off-label male ED population explicitly as "precisely the demographic in which these conditions are more prevalent," with no CV pre-screening in grey-market use — the caution is stated and grounded.

**Verdict on field: populated.**

---

#### monitoring — populated

Section 4.3 and D.4.4 / D.5 name objective monitoring requirements:

**PRIMARY — Blood pressure (clinical / ambulatory):**
- The label states: "measure BP before initiating; adhere to dosing frequency limits" [D.5, from FDA label].
- The White WB et al. 2017 ambulatory BP monitoring substudy (PMID 27977473, n=397 premenopausal women) is explicitly cited in section 2.3 and D.4.4: "A dedicated ambulatory monitoring substudy...confirmed the BP effect pattern and its transient nature." This is the specific ambulatory-BP-monitoring study named in the phase 7.5 brief.
- The CV contraindication basis is the transient +6/+3 mmHg BP rise — making blood pressure the primary objective monitoring target.

**Resting heart rate:**
- Section 4.3 and D.4.4 document "compensatory heart rate decrease up to ~5 bpm" [FDA label]. Heart rate is named as the objective compensation signal to monitor alongside BP.
- The wiki page [[biomarkers/resting-heart-rate]] is noted as an existing linked marker.

**Dermatologic hyperpigmentation exam:**
- Section 4.3 states: "Examine face, gingiva, and breasts at baseline and each follow-up visit" [from FDA label warnings].
- D.4.3 and D.5 explicitly state: "Patients should be monitored at each follow-up visit for new or expanding pigmented lesions on the face, gingiva, and breasts."

All three named objective monitoring markers from the phase brief are present and grounded in regulatory-tier-1 sources. Blood pressure is named as the primary objective monitor based on the contraindication basis + the White WB ambulatory study.

**Verdict on field: populated.**

---

#### stopping_criteria — populated

Sections 4.3 and D.5 enumerate the label-grounded stopping criteria:

1. No symptom improvement after 8 weeks → discontinue [FDA label, regulatory tier 1]
2. Sustained or severe BP elevation post-dose → hold and evaluate [FDA label]
3. New or progressive hyperpigmentation → consider discontinuation; no dose-reduction strategy is established [FDA label]
4. Symptomatic CV events (chest pain, syncope, dyspnea) → stop and evaluate urgently [FDA label]

The label dosing caps (≤1 dose/24 h, ≤8 doses/month) are also cited in D.2 and section 4.1, grounding the frequency-limiting criteria.

The honest off-label note is present in section 3.1 and 7.3: there is no validated efficacy biomarker for non-approved use in men, no 8-week response threshold validated for this population, reinforcing that "no efficacy signal after 8 weeks" is the relevant stopping anchor in the approved population.

**Verdict on field: populated.**

---

### Third-party objective monitoring markers

Three named markers, all grounded:

1. **Blood pressure (ambulatory/clinical)** — primary. FDA label contraindication basis (uncontrolled HTN/CVD); transient +6/+3 mmHg rise peaking 2–4 h post-dose; White WB et al. 2017 (PMID 27977473) ambulatory BP monitoring substudy cited in both documents. This is an objective, instrument-measured assay.

2. **Resting heart rate** — defensible linked marker. The compensatory HR decrease (~5 bpm) is part of the same hemodynamic response documented in the FDA label and the 52-week extension (Simon et al. 2019, PMID 31599847). Monitoring HR alongside BP captures the full hemodynamic picture. The wiki page [[biomarkers/resting-heart-rate]] exists.

3. **Dermatologic hyperpigmentation exam** — objective exam at documented anatomical sites (face, gingiva, breasts). Label-grounded (section 4.3, D.4.3, D.5). The irreversibility caveat ("resolution cannot be assumed") makes this a monitoring-for-harm marker, not merely for reassurance. Objective in the sense that pigmentary change is a visually assessable clinical finding at named anatomical sites.

**third_party_monitoring_marker_present: true** — all three markers are named in retrieved sources, grounded in regulatory-tier-1 citations (FDA label, White WB ambulatory study).

---

### Why compound_risk_tier = medium (not experimental, not low)

**Not "experimental"/uncharacterized:** PT-141/bremelanotide is FDA-approved (NDA 210557, June 21, 2019) with a characterized safety profile from the RECONNECT Phase 3 trials (n=1,247) and a 52-week open-label extension. The AE profile, contraindications, and hemodynamic signal are all documented from regulatory-grade evidence.

**Why not "low":** Four factors keep PT-141 above low-risk:
1. The transient BP elevation (+6/+3 mmHg) + hard label contraindications (uncontrolled HTN, known CVD) — a hemodynamic signal requiring CV pre-screening.
2. Focal hyperpigmentation that is not confirmed reversible — a potentially irreversible AE from the approved labeling.
3. The off-label/grey-market reality — the majority of actual use occurs outside the approved population, with unverified purity, without clinical monitoring, and without CV pre-screening.
4. MT-II/PT-141 sourcing confusion — compound-identity uncertainty in grey-market procurement is a documented risk (Evans-Brown 2009, BMJ).

**Medium tier is the honest tier:** Characterized safety profile (lowers from experimental), but CV contraindication + irreversible hyperpigmentation risk + grey-market confounders (raises from low). The research report's `risk_tier: approved-with-label-restrictions` is consistent with the medium classification.

---

### Summary

**verdict: PASS.** All four required risk-floor fields are populated from regulatory-tier-1 sources (FDA label NDA 210557, RECONNECT RCTs PMID 31599840/31599847, White WB ambulatory BP study PMID 27977473): adverse_effects_literature covers nausea (~40%), focal hyperpigmentation (1% label / 38% daily, not confirmed reversible), transient BP rise (+6/+3 mmHg), flushing, headache, injection-site reactions, plus the honest limits (off-label population, grey-market purity gaps, MT-II/PT-141 confusion); contraindications names both label contraindications (uncontrolled HTN, known CVD) plus off-label population caution; monitoring names blood pressure (primary, ambulatory/clinical, White WB substudy) + resting heart rate + dermatologic hyperpigmentation exam; stopping_criteria covers the 8-week no-response threshold, sustained BP elevation, progressive hyperpigmentation, and symptomatic CV events. compound_risk_tier = medium is correct: the compound is FDA-approved with a characterized safety profile (not experimental), but the CV contraindication, the irreversible-hyperpigmentation signal, and the grey-market/sourcing-confusion reality prevent a low-risk classification.
