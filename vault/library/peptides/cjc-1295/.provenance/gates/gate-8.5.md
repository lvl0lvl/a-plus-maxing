# Phase 8.5 LAYERS Gate — CJC-1295 (deep mode, standard+ compound)

Both mandatory layers (prescribing-practice + non-English) plus the compound entry were inspected. All admissibility checks pass.

## Check 1 — Both layer files exist and are non-trivial

PASS. `practitioner-layer.md` (84 lines) and `non-english-layer.md` (83 lines) both exist, are substantive, and carry correct frontmatter (`layer: prescribing-practice` / non-English coverage note). Neither is a stub. Recomputed sha256 of each matches the JSON block byte-for-byte.

## Check 2 — Practitioner layer

PASS.
- **No efficacy / AE-rate grounded on practice tiers.** The scope banner, every dose line, and the Self-check explicitly state that `practitioner_protocol` / `compounding_data_sheet` / `vendor_label` sources are admissible ONLY for dose/cycle/route/reconstitution conventions, and that no efficacy or AE-rate claim is grounded on any of them. Efficacy state is pointed to the research report, not asserted.
- **DAC vs no-DAC kept strictly separate.** With-DAC = ~1–2 mg SC once weekly (with a more conservative 100–300 mcg 1–3×/week compounding-guide figure, divergence reported-not-reconciled); no-DAC ("Mod GRF 1-29") = ~100 mcg (100–300) SC 1–3×/day, pre-bed/empty-stomach, stacked with ipamorelin. A load-bearing cross-attribution prohibition is stated twice (body + Self-check): once-weekly milligram ONLY to DAC, daily-microgram ONLY to no-DAC, with the mislabeling hazard flagged. No cross-attribution found.
- **Honest gates stated.** Named-prescriber: "NO named-prescriber primary source with verifiable name + venue + date located" → no `practitioner_protocol` claim asserted. Compounding: ONE historical Tailor Made Compounding monograph, flagged pre-restriction/withdrawn (FDA warning letter 04/01/2020; subsequent 503A Category 2), plus observed absence at Empower/other majors; no admissible current data sheet.

## Check 3 — Non-English layer

PASS. Honest null ("ZERO genuinely non-English admissible CJC-1295 primaries located"). The non-English-LANGUAGE vs non-English-AUTHOR distinction is enforced throughout: the Canadian ConjuChem originator pharmacology (Jetté 2005, PMID 15817669) is English-published and explicitly assigned to the English corpus, not counted here. Russian (eLibrary/CyberLeninka + open web; SportWiki excluded as wiki), Chinese (CNKI/Wanfang/ChemicalBook/Zhihu + PMC cross-check; NMPA 2017 doping-list logged as a regulatory artifact, not a primary), and originator-country all surveyed. No fabricated sources — the single real identifier asserted is the located Jetté 2005 record, shown only for lineage; translated-numerics tag N/A (no foreign primaries).

## Check 4 — Compound entry

PASS. Frontmatter: `evidence_tier: C`, `risk_tier: experimental` (correct). The DAC/no-DAC two-molecule fact is present and prominent (Metadata + "Read this first" banner + Protocol). No efficacy overstatement — GH/IGF-1 rises are explicitly framed as biomarkers, not proven clinical benefit; terminated trial and ConjuChem concentration alert recorded. Relations link the research-report, practitioner-layer, non-english-layer, [[biomarkers/igf-1]], and [[compounds/ipamorelin]] — all five present. No Wikipedia reference (the only wiki, Russian SportWiki, is explicitly excluded in the non-English layer).

## Verdict

verdict: PASS

```json
{
  "phase": "8.5",
  "verdict": "PASS",
  "mode": "deep",
  "practitioner_layer": {"path": "vault/library/peptides/cjc-1295/practitioner-layer.md", "present": true, "sha256": "943bc2800ac7ee1773a4aa1d21dbe4824bf0af068a2ed8df164eed72601c2cfe", "compounding_sheets_count": 1, "compounding_sheets_or_null_finding": true, "named_physicians_count": 0, "has_bibliography": true, "has_self_check": true},
  "non_english_layer": {"path": "vault/library/peptides/cjc-1295/non-english-layer.md", "present": true, "sha256": "8c89d8fdaaff6f795f7c9ce56de51c74f93d7cc60887e09b04119405c39a60cd", "languages_surveyed": ["Russian", "Chinese", "Other"], "has_bibliography": true, "has_self_check": true},
  "halt_reasons": []
}
```
