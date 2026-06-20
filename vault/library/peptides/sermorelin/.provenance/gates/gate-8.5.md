# Phase 8.5 LAYERS Gate — Sermorelin (deep mode, standard+ compound)

Both layers are mandatory for this standard+ compound. Verified the compound entry plus both layer documents.

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

PASS. Both layer files exist and are substantive.
- `practitioner-layer.md` (75 lines): full dose/route conventions, named-prescriber section, compounding-data-sheet gate result, reconstitution arithmetic table, a numbered `## Bibliography (own; tag + tier)` with 6 entries, and a `## Self-check` block. sha256 `497881ba932181207b05d7cdafca3438efbcd6c90bfcc151886b0961eb73227d` (matches prompt).
- `non-english-layer.md` (81 lines): Russian/Soviet, Chinese, originator-country sections, translation-handling notes, a `## Bibliography (own; tag + tier + language)`, and a `## Self-check` block. sha256 `b126190843f5c494fdbb029a530a90f6be0fcdbdf1f1491aea7323db5e549377` (matches prompt).

## Check 2 — Practitioner layer discipline

PASS.
- **No efficacy/AE-rate claim grounded in practice/vendor sources.** The scope banner (line 14) and the first Self-check bullet both state explicitly that no efficacy or AE-rate claim is grounded on any `compounding_data_sheet`/`practitioner_protocol`/`vendor_label` source; efficacy/safety state is delegated to the research report. Every figure is dose/route/cycle/reconstitution convention or regulatory fact.
- **Pediatric Geref label dose tagged `regulatory` and kept DISTINCT.** Line 20: "30 µg/kg/day SC at bedtime … labeled `regulatory` … not an adult convention," held separate from the adult convention. Reinforced in Self-check ("Pediatric vs adult kept distinct").
- **Adult compounded convention present** (~100–500 mcg SC nightly, ~5/7, empty stomach), distinct from the pediatric label dose.
- **Compounding data sheets found and tagged.** Three distinct admissible §503A compounding data sheets cited and tagged `compounding_data_sheet`: Empower [1], Strive [2], Olympia [3]. Count = 3.
- **No cross-attribution to CJC-1295 / tesamorelin.** Explicit "Keep sermorelin dosing SEPARATE" callout (line 28) plus a Self-check bullet flag tesamorelin's 2 mg/day and CJC-1295's weekly cadence as NOT applicable to sermorelin.
- Named-prescriber result is an honest negative (no name+venue+date located; clinic pages reported as generic conventions). Named physicians count = 0.

## Check 3 — Non-English layer honesty

PASS. Russian = one genuine Russian-LANGUAGE source (Brylëv et al. 2013, CyberLeninka), admissible **context-only**, grounding no efficacy/AE claim. Chinese = none Chinese-LANGUAGE primary located (only vendor/patent/database material). The non-English-LANGUAGE vs non-English-AUTHOR distinction is explicitly enforced (line 10, Self-check), excluding English-published originator/Chinese-group work from the count. No fabrication: the single cited record is real; excluded tertiary/HALT pages (Russian Wikipedia, .ru/Baidu monographs) are named only as exclusions. Net new non-English admissible primaries = 0, honestly reported.

## Check 4 — Compound entry

PASS.
- **Frontmatter correct:** `evidence_tier: B`, `risk_tier: medium`.
- **Pediatric-vs-adult + withdrawn-≠-unsafe framing present.** The "Read this first" block states the evidenced/approved use is pediatric GHD + diagnostic, demarcates the off-label adult use, and explains the ~2008 withdrawal was COMMERCIAL with the FDA 2013 Federal Register determination that it was NOT withdrawn for safety/effectiveness.
- **Relations complete:** research-report, practitioner-layer, non-english-layer, [[biomarkers/igf-1]], [[compounds/cjc-1295]], [[compounds/tesamorelin]], [[compounds/ipamorelin]] — all present.
- **No Wikipedia citation.** The only "Wikipedia" string (line 38) names Russian Wikipedia as an *excluded* HALT source — correct usage, not a citation.

## Verdict
verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/sermorelin/practitioner-layer.md","present":true,"sha256":"497881ba932181207b05d7cdafca3438efbcd6c90bfcc151886b0961eb73227d","compounding_sheets_count":3,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/sermorelin/non-english-layer.md","present":true,"sha256":"b126190843f5c494fdbb029a530a90f6be0fcdbdf1f1491aea7323db5e549377","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
