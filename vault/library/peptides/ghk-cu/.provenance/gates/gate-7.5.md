# Phase 7.5 Risk-Floor Gate — GHK-Cu

## Verdict

verdict: PASS (all required fields populatable from cited sources)

risk_tier = experimental (injectable/systemic) → floor is BLOCKING. All four required fields are present AND cited, and an objective third-party monitoring marker exists (mandatory for experimental-tier PASS per schema allOf clause). No HALT.

## Field-by-field (present? cited? report location)

### adverse_effects_literature — PRESENT ✓ / CITED ✓ → `populated`
- **Topical (CIR-safe):** CIR 2018 "safe in present practices of use and concentration," <10 ppm family-wide; topical AE limited to rare mild local irritation/sensitization, contact dermatitis "very rarely reported," patch-test precaution. Report §8.1, cited [46][51][49][12].
- **Injectable AE existence (cited, with honest no-trial caveat):** injection-site reactions (redness/swelling/pain), transient flushing, metallic taste recorded as **existence-of-AE-type only**; the "8–12% injection-site reactions" figure is explicitly **rejected as not admissible** (no controlled human trial grounds it). Report §8.4, cited [52]; supporting topical tolerability [42][43].
- **No injectable human safety trial — explicitly noted:** "no controlled human trial of injectable/systemic GHK-Cu exists" / "has not been characterized in a controlled human trial." §8.4.

### contraindications — PRESENT ✓ (non-empty) / CITED ✓ → `populated`
- **Wilson's disease + other copper-metabolism/copper-overload disorders** (Indian childhood cirrhosis, idiopathic copper toxicosis): reach copper toxicity below the 10 mg/day UL; GHK-Cu supplies bioavailable copper → **absolute contraindication for systemic/injectable use** (the principal contraindication group). §8.3, cited [47]. Reinforced §10, §11.
- **Copper-chelation therapy** (GHK-Cu counteracts chelation — contraindication/interaction). §8.3, cited [52].
- **Concurrent copper supplementation** (CAUTION — cumulative load toward UL, especially systemic). §8.3, cited [48][47].
- Note: pregnancy/lactation is **not explicitly enumerated** in the report's contraindication list; field is still populated and cited on the load-bearing Wilson's/copper-overload basis. (Honest gap flagged, non-blocking — does not affect populated status.)

### monitoring — PRESENT ✓ (non-empty) / CITED ✓ → `populated`
- **Serum copper, ceruloplasmin, and liver function** are the relevant monitoring axes for systemic/injectable use (by analogy to copper-overload management; liver damage is the UL-defining endpoint). §8.3, cited [47]. Echoed §10.
- Honest qualifier: no GHK-Cu-*specific* validated trial protocol — but copper status IS objectively monitorable, which satisfies populated monitoring per gate guidance.

### stopping_criteria — PRESENT ✓ / CITED ✓ → `populated`
- **Topical stopping criterion:** discontinue and consider patch testing / dermatology referral on local irritation or suspected allergic contact dermatitis. §8.3, cited [51].
- (Systemic stopping is by-analogy to copper-overload/UL/liver-endpoint monitoring, §8.3/§10; the field has concrete cited content, so populated rather than placeholder.)

### third_party_monitoring_marker_present — TRUE ✓
- Objective copper-status markers exist and are named: **serum copper** and **ceruloplasmin** (plus liver function as the UL-defining safety axis). §8.3, cited [47]. Satisfies the experimental-tier mandatory-marker requirement (schema allOf: experimental + PASS ⇒ marker must be true).

## Structured verdict

```json
{"phase":"7.5","verdict":"PASS","compound_risk_tier":"experimental","compound_entry_path":"vault/compounds/ghk-cu.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"populated"},"third_party_monitoring_marker_present":true,"third_party_markers":["serum copper","ceruloplasmin","liver function"],"halt_reasons":[],"iterations":1,"timestamp":"2026-06-19T15:17:57Z","attestation_chain":{"iter_start_ts":"2026-06-19T15:17:57Z","attest_ts":"2026-06-19T15:17:57Z","iteration":1,"agent_source_path":"/Users/Flybottle/Documents/Projects/a+research/.claude/skills/aplus-research/schemas/gate-7.5.schema.json","agent_source_sha256":"78a8ae1e95995ec1e9a1b14a1dd678836d87715a3cb47c779be39c6912b7f203","agent_source_mtime":"2026-06-18T20:04:15Z"}}
```
