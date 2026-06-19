# Gate 4.75 — Citation Integrity Verifier — Triglycerides (TG)

Mode: standard. Corpus: `sections/section-A.md`, `sections/section-B.md`, `corpus/*.txt` (20 files).
Section A `## Post-fix grep audit` block (lines 60-85) treated as remediation documentation; its quoted OLD strings (`[3, cohort]`, `[3`) are not scored as live claims.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: []
```

---

## IC-1 Type-Tag Presence

Every inline citation in both sections is `[N, <tag>]` with `<tag>` drawn from the canonical enum. Live tags used: `mechanism_review`, `meta_analysis`, `cohort`, `rct`, `regulatory`. No off-enum tag in any live (non-audit-block) line. The only `[3, cohort]` occurrence (section-A L67) sits inside the Post-fix re-cite ledger documenting the OLD (corrected) string and is not a live claim. **PASS.**

## IC-2 Bibliography Type-Tag Presence

All bibliography entries carry a bracketed/backticked enum tag (A: refs 1-9; B: refs 1-11). A refs 2/6 annotate `[cohort/Mendelian randomization]` and ref 7 `[meta_analysis/Mendelian randomization]`; "Mendelian randomization" is a descriptive design qualifier, not a competing enum token — the leading enum tag (`cohort` / `meta_analysis`) is valid, and multiple tags are permitted by IC-2. B ref 7 `regulatory/mechanism_review` (Lovaza FDA indication) — both enum-valid. **PASS.**

## IC-3 Vendor-Not-Numerical

No `vendor_label` cite in either section. The two grep hits are Self-check prose attesting the *absence* of vendor sourcing, not citations. **No vendor-not-numerical violation detected.** PASS.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` cite in either section. **No anecdote-not-numerical violation detected.** PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` cite present (this is a biomarker reference, not a compound dispatch). **No practitioner-protocol-efficacy violation detected.** PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` cite present. **No compounding-data-sheet violation detected.** PASS.

## IC-7 Population-Mismatch

Grep for `[N, animal]` and `[N, in_vitro]` inline cites returns ZERO matches across both sections. The TG evidence base is entirely human (meta_analysis / cohort / MR / rct) plus society guideline/consensus syntheses (`mechanism_review`). No numerical claim is grounded on a non-human source, so no `[population-mismatch: <species>]` annotation is required. Human → expected PASS, confirmed. **PASS.** `checked_citations: 0` animal/in_vitro cites requiring a tag.

## IC-8 Route-Extrapolation

Only oral pharmacotherapy doses appear (Lovaza 4 g/day, icosapent ethyl 4 g/day, fibrate/statin/omega-3 % reductions) — all cited to sources testing the same oral route; biomarker thresholds and assay claims carry no route. No route mismatch. **No route-extrapolation violation detected.** PASS.

## IC-9 Concentration-Surfacing

Distinct primaries (enum `rct`/`meta_analysis`/`cohort`; `mechanism_review`/`regulatory` excluded per §3 calc), deduplicated across both sections: 9 — Sarwar 2007 (Cambridge/ERFC), Sarwar/TG-CDGC 2010 (Cambridge/ERFC), Do 2013 (Broad/Kathiresan), Varbo 2013 (Copenhagen/Nordestgaard), Crosby 2014 (NHLBI ESP working group), Duran 2020 (Brigham/WHS), Bhatt 2019 REDUCE-IT (Brigham), White 2015 (Brigham/WHS), B-ref5 biological-variation group (misc).

Largest first-author-institution cluster = Cambridge/ERFC (Sarwar ×2) = 2/9 = 0.222. Even under the most aggressive honest grouping — merging all Brigham-affiliated work (Duran + Bhatt + White) into one cluster — share = 3/9 = 0.333. Both are far below the 0.70 HALT threshold. The TG literature is genuinely multi-cohort (Copenhagen, Cambridge/ERFC, Broad, NHLBI ESP, Brigham/WHS); Nordestgaard appears as one of several independent groups, not a dominant single lab. `threshold_triggered: false` — no first-class concentration section required. **PASS.**

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry (A: 1-9 all used and present; B: 1-11 all used and present). All entries carry real PMIDs/DOIs/PMC IDs as transcribed in the corpus headers (HEAD-check not re-run online; identifiers internally consistent with corpus). No inline cite without a bibliography entry. **No fabricated citations detected.** PASS.

## IC-11 No Placeholder Strings

Grep for `citation needed | TBD | TODO | Content continues | according to some reports | research suggests | experts believe` → zero matches. **No placeholder strings detected.** PASS.

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` → zero matches in either bibliography. **No Wikipedia citations detected.** PASS.

## IC-13 Per-Citation Corpus Scoping

Standard mode floor = ≥50% of numerical/quoted claims (min 10). All load-bearing numerical claims were grepped against the saved corpus; 23 distinct claim-units checked, 23 grounded verbatim:

- **Section A:** "4× more cholesterol" (ref1); OR 1.72 (1.56-1.90), 10,158/262,525/29, Reykjavik 1.76 / EPIC 1.57 (ref8); APOA5 16.0% / 0.25 mmol/L / OR 1.18 (1.11-1.26) / HR 1.10 (1.08-1.12) / 12.2 nmol/L / p=4.4×10⁻²⁴ / p=2.6×10⁻⁷ (ref7); 185 variants (ref6); Varbo 60,608 / 10,668 / RR 3.3 (2.1-5.2) / 28% CRP (10-48) (ref2); APOC3 498 / 110,472 / 39% / OR 0.60 (0.47-0.75) (Crosby/ref9); Duran 480 / HR 3.05 (1.46-6.39) (ref5); Endocrine Society strata + "below 1000 mg/dl" (ref4); EAS/EFLM +0.3 mmol/L (26 mg/dL) / ≥2 mmol/L (175) / >5 mmol/L (440) (ref3) — all FOUND.
- **Section B:** NCEP fasting bands 150/199/499/500 (ref1/3/10); AHA optimal <100 + nonfasting ≥200 (ref10); Endo finer strata (ref1); pancreatitis 500/880/~10 mmol/12-38%/1500-2000/250-500 (ref1/3); EAS ≥2 mmol/L 175 + fasting ≥1.7 mmol/L 150 + 0.3 mmol/L + >5 mmol/L 440 (ref2); White 175/1.98/c-stat 0.656 vs 0.628 (ref11); 88.5 conversion (ref1); CVi 25% / CVG 35.9% / 23.9% / ≥2× (ref5); fibrate 30-50% + 10% RR (0-18) + 13% (7-19) (ref3/ref1); omega-3 20-50% / Lovaza 4 g / ≥500 / ↓39-45% (ref3/ref7); REDUCE-IT 8,179 / 135-499 / 17.2% / 22.0% / HR 0.75 (0.68-0.83) / ~25% (ref4); statin 10-30% / niacin 10-30% / ezetimibe 5-10% (ref3); FCS genes LPL/APOC2/APOA5/GPIHBP1/LMF1 / 50-90% LPL / ~1 in 600 (ref6) — all FOUND.

The iteration-2 remediation (APOC3 OR 0.60 re-cited from ref3 EAS/EFLM → Crosby 2014 ref9) is verified: `A-ref3` corpus contains only non-fasting/postprandial claims; `A-crosby-2014-apoc3.txt` contains 498/110,472/39%/OR 0.60 (0.47-0.75). Attribution now correct. 0 failures. **PASS.** `claims_checked: 23, claims_failed: []`.

---

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {"IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"}, "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"}, "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"}, "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"}, "IC-13": {"status": "PASS"}},
  "population_mismatch": {"verdict": "PASS", "checked_citations": 0},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 9, "largest_cluster_count": 3, "share": 0.333, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 23, "claims_failed": []},
  "halt_reasons": [],
  "warnings": [],
  "iterations": 1
}
```
