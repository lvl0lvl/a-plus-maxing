# Phase 7.5 Risk-Floor Gate — TB-500

## Verdict

**verdict: PASS** — all required risk-floor fields are present AND backed by cited sources in the report. TB-500 is `risk_tier=experimental`, so the floor is BLOCKING; it is satisfied here. The honest "no validated lab-monitoring panel" position is stated explicitly with rationale and citations, which counts as a populated monitoring position (not a miss). An objective, clinician-trackable third-party marker is present (required for `experimental` PASS).

## Field-by-field

### 1. adverse_effects_literature — PRESENT: yes · CITED: yes → **populated**
AE profile drawn from trials/preclinical, quantified and cited.
- §8.1 "Human adverse-event data (full-length Tβ4)": IV Phase 1 (recombinant hTβ4) SAD "AEs in 25/44 (56.8%) Tβ4 vs 7/10 (70%) placebo; all mild–moderate; no SAEs, no dose-limiting toxicities to 25 µg/kg [1]"; MAD "16/24 (66.7%) Tβ4 vs 5/6 (83.3%) placebo … no SAEs, no DLT [1]" (unified [9], Wang 2021, NL005 Phase 1, tier 1).
- §8.1 Phase 3 ophthalmic NK "16 AEs across 7 subjects; treatment-group burden (40%) ≈ placebo (37.5%); 1 treatment-related AE; 1 … serious AE; all resolved [2]" (unified [48], Sosne 2023, SEER-1, tier 1).
- §8.1 "dizziness, headache, pyrexia (1 subject each) [4]" (unified [63], tier 3 corroborating).
- §8.2 bidirectional tumor signal: pro-metastatic "46.7 (95% CI 35.0–57.7) vs 10.9 … P<.001 [5]" (unified [64], Cha 2003) with an explicit over-expression-vs-exogenous mechanism-of-evidence caveat; tumor-suppressor counter-direction in multiple myeloma [6] (unified [65]).

### 2. contraindications — PRESENT: yes (non-empty) · CITED: yes → **populated**
§8.4 "Contraindications & risk-floor" enumerates, each citing primary/mechanism or regulatory sources:
- "Active or history of solid malignancy / elevated cancer risk / undiagnosed masses → avoid (pro-angiogenic; pro-metastatic in a solid-tumor animal model) [5, 6]" — exactly the requested malignancy contraindication, carried with a prudent-default caveat (over-expression construct, §8.2) but unchanged in force.
- "Anyone subject to anti-doping testing → categorical contraindication (WADA-banned at all times, non-Specified) [10]" (unified [68], WADA 2026 List S2.3) — the requested tested-athletes = WADA-banned item.
- "Pregnancy/lactation → avoid (no human reproductive safety data) [3, 4]".
- "No established human dosing / no systemic safety regulatory file … treat any systemic self-administration as unstudied [1, 3]".
- "Product-quality risk: monitor for hypersensitivity/injection-site reactions; stop on systemic allergic signs [9]".

### 3. monitoring — PRESENT: yes (non-empty) · CITED: yes → **populated**
§8.4: "If used despite the above: baseline and periodic clinical review for new/growing lesions given the angiogenesis signal; watch for dizziness, headache, pyrexia and mild–moderate self-limited AEs seen in trials. **No validated lab-monitoring panel exists** [1, 5]." Also §8.4 "monitor for hypersensitivity/injection-site reactions [9]," and §10/§3.6 note FMD, hs-CRP, NT-proBNP are exploratory-only in the one fragment trial (NCT07487363) — i.e., not validated PD biomarkers. This is the honest "no validated monitoring biomarker, here is what a clinician can track instead and why" position the prompt explicitly counts as populated.

### 4. stopping_criteria — PRESENT: yes → **placeholder-with-pointer**
§8.4 "stop on systemic allergic signs [9]" gives a concrete stop trigger; §10 item names "a defined stop rule" as a required design element for any supervised use. Because this is a goal-agnostic library entry (operator/person-specific fields deliberately blank, per the front-matter banner), the stopping criterion is present at library-entry/placeholder-with-pointer level rather than a fully individualized protocol — which satisfies the schema's `placeholder-with-pointer` allowance for this field.

### 5. third_party_monitoring_marker_present — **true**
Objective markers a clinician could track ARE present:
- New/growing-lesion surveillance and baseline malignancy screening (clinical exam + imaging) — §8.4, §10.
- Injection-site / hypersensitivity examination (objective clinical signs) — §8.4.
- WADA doping-control assay: LC-MS detection of N-acetylated LKKTETQ in urine/plasma — an objective analytical marker (§1.3 / §4.2; unified [5] Ho 2012, tier 1).
Honest limit: there is NO validated efficacy/PD lab biomarker for the marketed use (no validated monitoring panel, §8.4), but the schema asks whether an objective trackable marker exists for clinician oversight — objective safety/analytical markers do exist, so this is `true` (consistent with the `experimental`-tier PASS requirement).

## Structured verdict

```json
{
  "phase": "7.5",
  "verdict": "PASS",
  "timestamp": "2026-06-19T13:44:06Z",
  "iterations": 1,
  "compound_risk_tier": "experimental",
  "compound_entry_path": "vault/compounds/tb-500.md",
  "required_fields": {
    "adverse_effects_literature": "populated",
    "contraindications": "populated",
    "monitoring": "populated",
    "stopping_criteria": "placeholder-with-pointer"
  },
  "third_party_monitoring_marker_present": true,
  "third_party_markers": [
    "new/growing-lesion surveillance + baseline malignancy screening (clinical exam + imaging)",
    "injection-site and hypersensitivity clinical examination",
    "WADA doping-control LC-MS detection of N-acetylated LKKTETQ in urine/plasma (objective analytical marker)",
    "NOTE: no validated efficacy/PD lab biomarker exists (FMD/hs-CRP/NT-proBNP are exploratory-only in NCT07487363)"
  ],
  "halt_reasons": [],
  "attestation_chain": {
    "iter_start_ts": "2026-06-19T13:44:06Z",
    "attest_ts": "2026-06-19T13:44:06Z",
    "iteration": 1,
    "agent_source_path": ".claude/skills/aplus-research/schemas/gate-7.5.schema.json",
    "agent_source_sha256": "78a8ae1e95995ec1e9a1b14a1dd678836d87715a3cb47c779be39c6912b7f203",
    "agent_source_mtime": "2026-06-18T20:04:15Z"
  }
}
```

### Notes on schema conformance
- For PASS, the schema requires `adverse_effects_literature`, `contraindications`, and `monitoring` to be `populated` — all three are, and are cited. `stopping_criteria` is allowed `placeholder-with-pointer`, used here for the goal-agnostic library entry.
- For PASS at `compound_risk_tier=experimental`, the schema requires `third_party_monitoring_marker_present=true` — satisfied.
- `halt_reasons` is empty (maxItems 0 under PASS), using only schema enum values had any been needed (risk-floor-incomplete | missing-contraindications | missing-monitoring | missing-stopping-criteria | missing-third-party-marker | missing-adverse-effects).
