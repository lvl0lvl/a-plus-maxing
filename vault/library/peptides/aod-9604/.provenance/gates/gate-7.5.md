# Gate 7.5 — RISK-FLOOR Verifier: AOD-9604

**Compound:** AOD-9604 (Tyr-hGH(177-191), synthetic C-terminal hGH "lipolytic" fragment)
**risk_tier:** experimental (unapproved hGH fragment; gray-market injectable, no published human SC data, FDA-flagged immunogenicity for uncharacterized product)
**Entry:** `vault/library/peptides/aod-9604/research-report.md`
**Gate spec:** `references/health-gates.md` §2 (Risk-Floor Gate, Phase 7.5)

## Summary

The Safety section (§5) of the AOD-9604 report carries a complete risk profile. All four
required fields are populated and citable from retrieved sources. Because `risk_tier:
experimental`, §2 of the gate additionally requires a third-party (objective) monitoring
marker. AOD-9604 is GH-axis-sparing by design, so no AOD-9604-specific validated biomarker
exists — but the report names two objective assays whose role is to confirm the absence of
GH-axis activity: **IGF-1** (confirm no rise) and **fasting glucose** (confirm no impairment).
These are named objective assays, satisfying the third-party-marker requirement.

### Field-by-field verification

- **adverse_effects_literature — POPULATED.** §5.1: pooled 6-trial human dataset (~893 adults),
  "very good safety and tolerability profile indistinguishable from placebo" [4]; headache most
  frequent AE but placebo-comparable; dose-related GI effects only at supraphysiologic 54 mg oral;
  no treatment-related SAEs/withdrawals. §5.2: GH-axis-sparing VERIFIED — no IGF-1 change, no
  glucose-tolerance impairment [4][5]. §5.4: honestly bounded — no long-term human data (max 24 wk),
  no published human subcutaneous-route data, FDA-flagged immunogenicity/aggregation/impurity
  concern for uncharacterized injectable [13].
- **contraindications — POPULATED.** §5.5: precautionary given unapproved/gray-market status —
  pregnancy/lactation (no human data, avoid); uncharacterized-injectable / unapproved-compound
  caution (FDA recommended against §503A bulks listing); WADA-prohibited [13][16][20]. Honest
  framing: "unapproved, uncharacterized injectable, no long-term data," not "known to be harmful."
- **monitoring — POPULATED.** §5.6: no validated AOD-9604-specific biomarker; GH-axis markers
  uninformative as *activity* markers by design. Conservative plan — baseline/periodic IGF-1
  (document expected absence of rise) and fasting glucose/HbA1c (document absence of metabolic
  harm), injection-site assessment for local reaction/infection, general clinical review [4][5][13].
- **stopping_criteria — POPULATED.** §5.6: discontinue for any new IGF-1 elevation or impaired
  glucose tolerance, injection-site infection/abscess, allergic/hypersensitivity reaction
  (possible aggregate/impurity immunogenicity), or any SAE; absence of measurable benefit is itself
  a reasonable reason to stop.

### Third-party monitoring marker (experimental-tier requirement)

RISK-FLOOR rule applied: a GH-axis-sparing compound does NOT require an AOD-9604-specific validated
biomarker. The relevant named objective assays are **IGF-1** (confirm no rise) and **fasting glucose**
(confirm no impairment), both present in §5.6. These are named objective lab assays →
`third_party_monitoring_marker_present = true`.

## Verdict

verdict: PASS

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"experimental","compound_entry_path":"vault/library/peptides/aod-9604/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["IGF-1","fasting glucose"],"halt_reasons":[],"iterations":1}
```
