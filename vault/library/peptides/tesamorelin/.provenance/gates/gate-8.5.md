# Phase 8.5 — LAYERS Gate — Tesamorelin (deep mode, standard+ compound)

Both layers are mandatory at standard+ deep mode. Each check below is verified against the live files.

## Check 1 — Both layers exist, non-trivial, with Bibliography + Self-check

PASS. Both layers are present, substantive, and complete.

- `practitioner-layer.md` (sha256 `69ef056c…`, matches expected) is a full prescribing-practice document with sections for label doses, off-label conventions, named-prescriber protocols, compounding gate, reconstitution math, a numbered **Bibliography (12 entries)**, and a four-bullet **Self-check**. Non-trivial.
- `non-english-layer.md` (sha256 `eebc3a02…`, matches expected) is a full non-English survey with Russian, Chinese, Other/originator, translation-handling, a **Bibliography (NE-TESA-1…4)**, and a five-bullet **Self-check**. Non-trivial.

## Check 2 — Practitioner layer integrity

PASS.

- **No efficacy / AE-rate claim grounded in practice/vendor sources.** The scope banner and Self-check explicitly bar this; every figure is a dose/route/cycle/reconstitution convention or a regulatory/cost fact. Efficacy and AE rates are deferred to the research report.
- **Label doses tagged `regulatory`.** Egrifta **2 mg SC daily**, Egrifta SV **1.4 mg SC daily**, Egrifta WR **1.28 mg SC daily** are each individually carried with the `regulatory` tag and verified against DailyMed / accessdata.
- **Honest gates stated.** Named-prescriber protocols: **none located** that meet the name+venue+date bar — explicit absence, not fabricated (off-label conventions flagged UNATTRIBUTED). Compounding: **no live named-compounder tesamorelin product page** located (Empower carries sermorelin, not tesamorelin); only a 503Pharma trade explainer asserting conditional compoundability — reported as an explicit gate absence, consistent with tesamorelin's approved-drug/biologic status. compounding_sheets_count = 0 with a null-finding stated; named_physicians_count = 0.

## Check 3 — Non-English layer integrity

PASS.

- **Honest "none located."** Headline result is ZERO genuinely non-English admissible primaries; Russian and Chinese tracks reported as explicit nulls.
- **LANGUAGE vs AUTHOR distinction enforced.** The China-sited NCT07481734 is flagged as an English-protocol trial (non-English site, NOT non-English language) and explicitly excluded from the non-English-primary tally; the Synapse/智慧芽 entry is a database/pipeline record, not a primary.
- **No fabrication.** No invented author, journal, PMID, or DOI; the single concrete identifier (NCT07481734) is a real registry record.
- **Russian + Chinese + originator surveyed.** Russian (eLibrary/CyberLeninka, Cyrillic тезаморелин + releasing-hormone terms); Chinese (CNKI/Wanfang, 替莫瑞林); originator (Theratechnologies / MGH-Grinspoon, English-published — valid "none in another language").

## Check 4 — Compound entry integrity

PASS.

- **Frontmatter correct.** `evidence_tier: B`, `risk_tier: medium` — both as required.
- **Approved-vs-off-label demarcation present.** The "Read this first" block, Evidence Summary (APPROVED vs INVESTIGATIONAL vs ABSENT domains), and Decision Notes draw the line sharply: approved only for VAT reduction in HIV-lipodystrophy; NAFLD/cognition investigational; bodybuilding/athletic/anti-aging/healthy-adult fat loss have zero human efficacy data.
- **Relations complete.** Links to research-report, practitioner-layer, non-english-layer, `[[biomarkers/igf-1]]`, `[[compounds/cjc-1295]]`, and `[[compounds/ipamorelin]]` are all present.
- **No Wikipedia.** Confirmed absent from the compound entry and both layers (grep clean; the only Wikipedia hit in the directory is in research-report.md, which is out of this gate's scope).

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/tesamorelin/practitioner-layer.md","present":true,"sha256":"69ef056cd4ec56d5effddb39cd8cb087032f6bfa04d06d9735e1605e2a3253ca","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/tesamorelin/non-english-layer.md","present":true,"sha256":"eebc3a0241f495b8792faa774ca29105d8789e08970da03fc7b00dd7b742d143","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
