# Phase 8.5 — LAYERS Gate — Hexarelin (deep mode, standard+ compound)

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

PASS. Both mandatory layers are present and substantive.

- **Practitioner layer** (`vault/library/peptides/hexarelin/practitioner-layer.md`, sha256 `f57818d8…68dd`): 83 lines, fully sectioned (Dose/route conventions, Named-prescriber, Compounding data-sheet gate, Reconstitution math, Bibliography, Self-check). Non-trivial. **Has Bibliography** (§"Bibliography (own; tag + tier)", 9 numbered entries with tag + tier). **Has Self-check** (5 bullets). SHA256 matches the JSON claim exactly.
- **Non-English layer** (`vault/library/peptides/hexarelin/non-english-layer.md`, sha256 `0f41b02b…4689`): 76 lines, sectioned (Russian/Soviet, Chinese, Italian/originator/other, Translation handling, Bibliography, Self-check). Non-trivial. **Has Bibliography** (§"Bibliography (own; tag + tier + language)", NE-HEX-1 + non-admissible list). **Has Self-check** (5 bullets). SHA256 matches the JSON claim exactly.

## Check 2 — Practitioner layer discipline

PASS on all sub-checks.

- **No efficacy / AE-rate claim grounded in practice/vendor sources.** The scope banner and Self-check both state explicitly that `practitioner_protocol`, `compounding_data_sheet`, and `vendor_label` sources ground only dose/cycle/route/reconstitution conventions, never efficacy or AE-rate. Critically, the vendor desensitization percentages (40–60% / 50–75%) are explicitly **NOT** grounded here — only the cycling *convention* is retained, with the real ~45% magnitude deferred to research-report §2.4. This is exactly the discipline required.
- **~100 mcg SC 2–3×/day cycled-for-tachyphylaxis convention NOT cross-attributed to GHRH analogues.** The Stacking section reports the hexarelin (GHRP) + GHRH-analogue (CJC-1295 / sermorelin / tesamorelin) pairing as commercial convention only, and states hexarelin's ~100 mcg SC dosing is "kept distinct" and "not cross-attributed" to the GHRH partners. Self-check bullet 4 re-affirms. Cycling is framed around tachyphylaxis/receptor desensitization, not calendar.
- **Honest gates stated.** Named-prescriber: "**NONE admissible**" — both clinic pages (Wittmer, Revolution Health) fail name+venue+date and are downgraded to `practitioner_protocol_downgraded`; reported as absence, not fabricated. Compounding: "**NO compounding-pharmacy data sheet (and no compounded product) located**" — corroborated by hexarelin's absence from all §503A/PCAC lists and the April-2026 removed-12. Both gates reported honestly with count 0.

## Check 3 — Non-English layer honesty + LANGUAGE-vs-AUTHOR distinction

PASS.

- **Honest near-null.** Russian: one context-only secondary review (Brylëv 2013, Kursk State Univ., CyberLeninka), explicitly non-groundable for efficacy. Chinese: none located (hexarelin appears only as a referenced GH-secretagogue). Italian (originator country): no Italian-LANGUAGE primary — valid "none" because the Deghenghi/Ghigo/Locatelli originator lineage is English-published.
- **Non-English-LANGUAGE vs -AUTHOR distinction enforced** and called "load-bearing for hexarelin specifically." English-published Italian/Chinese-group work (Ghigo, Arvat, Locatelli, Bodart, Agbo) is explicitly excluded as already English-reachable; only primary-language Russian/Chinese/Italian work counted. Self-check confirms.
- **No fabrication.** The single asserted record is real and labeled a secondary review; gaps reported as gaps. Translated-numerics handling N/A (zero non-English primaries → zero foreign numerics). Genuine non-English admissible primaries added: 0.

## Check 4 — Compound entry

PASS.

- **Frontmatter correct:** `evidence_tier: C`, `risk_tier: experimental` (lines 6–7). Type compound, class peptide.
- **GHRP-not-GHRH framing present:** "Read this first" callout and Metadata both state hexarelin is a GHRP / GHS-R1a (ghrelin-receptor) agonist + CD36 binder, **NOT a GHRH analogue**, same class as GHRP-6/GHRP-2/ipamorelin, must not be confused with sermorelin/CJC-1295/tesamorelin.
- **Tachyphylaxis framing present:** "defining limitation is TACHYPHYLAXIS" with the 16-wk healthy-elderly data (GH AUC 19.1→10.5 µg/L·h, ~45% decline; IGF-1/IGFBP-3 unchanged P=0.24/0.74; reversible).
- **Relations complete:** links research-report, practitioner-layer, non-english-layer, [[biomarkers/igf-1]], [[compounds/ipamorelin]], [[compounds/sermorelin]] (lines 81–86). All six required relations present.
- **No Wikipedia.** Grep across all three files found zero Wikipedia citations. The two "SportWiki" mentions in the non-English layer are explicit *exclusions* (named as wiki-type, HALT-adjacent, non-admissible) — correct discipline, not a violation.

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/hexarelin/practitioner-layer.md","present":true,"sha256":"f57818d8c8f5d4033caee76f4c030778bf8793d00ae00235441bf06b465968dd","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/hexarelin/non-english-layer.md","present":true,"sha256":"0f41b02bbab49a3f089f89eefe1d0eb417e986789216e2ef191b5d8f60464689","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
