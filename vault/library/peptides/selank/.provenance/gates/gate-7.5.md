# Phase 7.5 Risk-Floor — Selank

Compound, risk_tier = experimental (Russia-registered tuftsin-analogue anxiolytic; unapproved US/EU; evidence_tier C, single-network Russian lineage). Verifying the four required risk-floor fields against §4 Safety and the abstract of the retrieved research report.

## Field-by-field

1. **adverse_effects_literature → POPULATED.**
   §4 carries actual AE data from the literature, not a placeholder. Intranasal tolerability is characterized: the most commonly noted *actual* adverse effect is **mild local nasal irritation** (route-specific, minor). The favorable Russian record is reported with citations — anxiolysis comparable to medazepam/phenazepam **without sedation, muscle relaxation, cognitive/amnestic impairment, tolerance, dependence, or withdrawal** [10][12][11], with the instrument-anchored Medvedev 2015 UKU-tolerability study [11] directly measuring reduction of phenazepam sedation/memory/withdrawal symptoms. Animal data: no tolerance after 14 days; no motor depression with Selank+diazepam [14]. The Western counterweight is explicitly carried: **Doyno & White 2021** classify Selank as a "poorly studied Russian drug with GABAergic mechanisms ... inexplicably sold to US consumers," grouping it with agents whose illicit use can cause "abuse, dependence, and subsequent withdrawal syndromes," and call for abuse-potential evaluation before public access [19]. Honest bounding (single-lineage, short exposure, evidence grade LOW–MODERATE) is stated.

2. **contraindications → POPULATED.**
   §4 "Contraindications (precautionary)" gives real precautionary content: **pregnancy and lactation — no human safety data, avoid**; unapproved/unverified gray-market product caution (unknown purity, no GMP, no clinical oversight); **GABAergic co-use** (benzodiazepines, alcohol, CNS depressants) treated as untested/uncharacterized rather than assumed safe. Correctly notes there are no Western label-defined contraindications because Selank is unapproved in the West.

3. **monitoring → POPULATED.**
   §4 "Monitoring & stopping criteria" states monitoring is **clinical, not biomarker-based — no validated Selank safety biomarker or therapeutic drug level**. Practical monitoring: standardized anxiety instruments (Hamilton Anxiety, Zung, CGI as used in trials [10]), subjective tolerability, and local nasal-tolerance check for the intranasal route.

4. **stopping_criteria → POPULATED.**
   Explicit criteria given (not placeholder): discontinue for hypersensitivity/allergic reaction, persistent local nasal irritation, paradoxical worsening of anxiety/agitation, any neuropsychiatric change, or signs of a contaminated/adulterated product. Notes that no withdrawal syndrome is reported (so no benzodiazepine-style taper expected) but, because this rests on single-lineage Russian data, **a cautious step-down is reasonable absent Western confirmation**. This is populated, real clinical-judgment content — beyond a mere placeholder-with-pointer.

## Third-party monitoring marker

Present (true). For this experimental-tier compound the safety/monitoring content contains explicit markers that oversight should involve a clinician / third party:
- "no validated Selank safety biomarker or therapeutic drug level" → monitoring is necessarily **clinical**, not self-administered lab-driven.
- Gray-market product caution citing absence of "clinical oversight" and no GMP assurance.
- Recommendation that "a cautious step-down is reasonable" on discontinuation — a clinical-judgment / supervision marker.
- Doyno & White call for formal abuse-potential evaluation before public access [19], reinforcing the regulated-oversight stance.

## Verdict
verdict: PASS

```json
{
  "phase": "7.5",
  "verdict": "PASS",
  "timestamp": "2026-06-21T03:02:00Z",
  "iterations": 1,
  "compound_risk_tier": "experimental",
  "compound_entry_path": "/tmp/aplus-research/selank/synthesis/research-report.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "populated"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": [
    "no validated Selank safety biomarker or therapeutic drug level — monitoring is clinical",
    "gray-market product caution: no clinical oversight, no GMP assurance",
    "cautious step-down reasonable on discontinuation (clinical-judgment marker)",
    "Doyno & White 2021 call for abuse-potential evaluation before public access [19]"
  ],
  "halt_reasons": []
}
```
