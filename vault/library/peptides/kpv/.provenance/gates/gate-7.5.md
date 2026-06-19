# Phase 7.5 Risk-Floor Gate — KPV (iteration 2)

## Verdict

verdict: PASS

(Independent re-verification of the updated report §8.4. The authoritative rule — health-gates.md §2 — requires an experimental-tier `monitoring` field to reference `[[biomarkers/<name>]]` OR a named lab assay; it does NOT require a compound-SPECIFIC validated biomarker. The iteration-2 §8.4 now names objective lab assays. third_party_monitoring_marker_present is now true and honest.)

## Field-by-field

Each field: present? cited? location; objective-assay note where relevant.

- **adverse_effects_literature — PRESENT, CITED → populated.**
  Location: §8 + §8.1 + §8.2. Animal existence-of-AE data are reported (α-MSH(11-13) no toxicity at doses tested [1, animal]; oral KPV DSS/TNBS no drug-attributable toxicity [2, animal]; HA-NP KPV no cytotoxicity / spleen-colon histology not different from healthy controls [4, animal]). Practitioner/vendor tolerability figures ("no LD50 / ≥100 mg/kg / 4–12-wk chronic") are explicitly carried as UNVERIFIED [5, practitioner_protocol][6, vendor_label]. The honest "no human AE rate" framing is preserved. Field is populated from retrieved sources, cited.

- **contraindications — PRESENT, CITED → populated.**
  Location: §8.4 (plus §8.3 theoretical risks). Named contraindications/cautions with cites: no established human safety margin [3, mechanism_review][8, regulatory]; pregnancy/breastfeeding — avoid [5, practitioner_protocol]; history-of/active cancer — caution/avoid [5, practitioner_protocol][3, mechanism_review]; active infection / immunodeficiency / concurrent immunosuppressants — caution (immunomodulatory) [5, practitioner_protocol]. Non-empty, cited.

- **monitoring — PRESENT, CITED, OBJECTIVE NAMED ASSAYS → populated.**
  Location: §8.4, "Objective monitoring (named assays, not a KPV-specific surrogate)" bullet. Names three objective lab assays:
    • **hs-CRP** (systemic inflammation) — referenced as `[[biomarkers/hs-crp]]` (wikilink resolves; target file `vault/biomarkers/hs-crp.md` confirmed to exist).
    • **fecal calprotectin** — named objective gut-inflammation lab assay (IBD/gut use case).
    • **CBC + CMP** — named general safety lab assays, warranted given KPV's immunomodulatory action.
  Cited [3, mechanism_review][2, animal]. The bullet explicitly states these are general objective inflammation/safety assays and NOT validated surrogates of KPV activity, and that no KPV-specific validated biomarker of effect exists.
  **These named objective lab assays (hs-CRP via `[[biomarkers/hs-crp]]`, fecal calprotectin, CBC/CMP) satisfy the §2 third-party-monitoring requirement.** The requirement is satisfied by an OBJECTIVE named lab assay; a compound-SPECIFIC validated biomarker is NOT required. The honest caveat about the absence of a KPV-specific biomarker does not negate the presence of objective named assays — it is the correct, honest framing.

- **stopping_criteria — PRESENT (library-canonical pointer) → placeholder-with-pointer.**
  Location: §8.4, "Stopping rule (inferable, not from a trial)" bullet — discontinue and seek care for worsening infection, allergic/injection-site reaction, or unexpected systemic symptoms; states no KPV-specific validated monitoring panel / biomarker-based stopping criterion is established (objective monitoring would use the named general assays). Cited [3, mechanism_review]. Header and pointer present per the library-canonical override. Non-empty.

## Structured verdict

```json
{"phase":"7.5","verdict":"PASS","timestamp":"2026-06-19T16:40:01Z","iterations":2,"compound_risk_tier":"experimental","compound_entry_path":"vault/library/peptides/kpv/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"placeholder-with-pointer"},"third_party_monitoring_marker_present":true,"third_party_markers":["hs-CRP","fecal calprotectin","CBC/CMP"],"halt_reasons":[],"attestation_chain":{"iter_start_ts":"2026-06-19T16:39:08.122013+00:00","attest_ts":"2026-06-19T16:40:01Z","iteration":2,"agent_source_path":"vault/library/peptides/kpv/research-report.md","agent_source_sha256":"fa58c90827556093b352cd2d9c12ff2f1ba20c06a8acb692b2806ce5172e88ae","agent_source_mtime":"2026-06-19T12:38:22Z"}}
```
