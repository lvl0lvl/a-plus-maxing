# Gate 8.5 — LAYERS Gate Verification: Semaglutide (deep mode)

Both layers are mandatory at standard+ deep mode. All four checks verified against the live files; both layer SHA256 hashes match the expected values exactly.

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

PASS. Both layer files are present and substantial:
- `vault/library/peptides/semaglutide/practitioner-layer.md` — full prescribing-practice layer (label titration for all three formulations, compounded/access landscape, microdosing, muscle-preservation convention, cost), with a numbered **Bibliography (own; tag + tier)** [1]–[8] and a four-part **Self-check**. SHA256 `a98cf12f6d07cba6a263b3613264670fd54cf1c7b6525225085d2391790d790d` matches expected.
- `vault/library/peptides/semaglutide/non-english-layer.md` — Russian/Chinese/Japanese-other survey with translation-handling, a **Bibliography (own; tag + tier + language)** (single language-verification entry NE-SEMA-X1), and a five-bullet **Self-check**. SHA256 `bfc4b7bdddcf5054c6a3a0145df933bf9606c7e8c8e471e897586a204d5739b2` matches expected.

Neither is a stub.

## Check 2 — Practitioner layer: no efficacy/AE-rate from practice/vendor; titration tagged regulatory; compounding as context without endorsing legality

PASS. The layer's frontmatter scope field explicitly restricts it to "dose/route/titration/access conventions ONLY — NOT efficacy or AE-rate." All three label titration schedules — Ozempic (0.25→0.5→1→2 mg), Wegovy (0.25→0.5→1→1.7→2.4 mg), Rybelsus (3→7→14 mg) — are tagged `regulatory` (authoritative, DailyMed labels). No efficacy or adverse-event-rate claim is grounded on any practice/vendor source: the only Tier-1 trial source cited ([7], STEP-1 DXA substudy) is used solely to frame the muscle-preservation convention and is explicitly flagged "NOT for an efficacy claim in this layer." Microdosing and the protein/resistance-training adjunct are tagged `practitioner_protocol` and explicitly marked "not efficacy-grounding." Cost is `vendor_label` (pricing only). Compounded-semaglutide is reported as practice/regulatory context — the shortage-resolution (Feb 21, 2025), 503A/503B wind-down deadlines, salt-form/counterfeit cautions, and dosing-error alert are all `regulatory` context, with the Self-check stating the layer "does not assert current compounding legality and does not ground efficacy on any compounded-supply source." Zero admissible compounding data sheets are cited (the compounded material is treated as regulatory/practice context, not as a cited compounding_data_sheet). Zero named physicians: the absence of a distinct named-prescriber/society protocol beyond the label is reported honestly ("reported honestly rather than fabricated"), not invented.

## Check 3 — Non-English: honest "none distinct" with LANGUAGE vs AUTHOR distinction

PASS. Headline result: "ZERO genuinely non-English-LANGUAGE admissible semaglutide primaries located." Required tracks all surveyed with explicit none-located findings: Russian/Soviet (derivative commentary/vendor only), Chinese (China-population PIONEER 11/12 confirmed English-published, DOI 10.1007/s00125-024-06142-3), Japanese/other (Japanese-population data English-published). The non-English-**LANGUAGE** vs non-English-**AUTHOR** distinction is named as "the load-bearing rule" and applied throughout — trials authored in China/Japan but published in English are reachable by the English layer and excluded here. The single bibliography item is recorded for language-verification provenance only, explicitly excluded as a non-English source. Honest, well-characterized null.

## Check 4 — Compound entry

PASS. Frontmatter is correct: `class: peptide`, `evidence_tier: A`, `risk_tier: medium`. The "Read this first" block is balanced — large population-specific benefits (STEP-1 ~14.9% weight, SELECT MACE HR 0.80, FLOW kidney HR 0.76, SUSTAIN/PIONEER HbA1c) paired with equally concrete caveats (GI-dominant AEs, weight regain on discontinuation, lean-mass loss, gallbladder/pancreatitis). Thyroid framing correct: "C-cell / medullary-thyroid-carcinoma BOXED WARNING is RODENT-based and has NOT been demonstrated in humans" (repeated in Risk Profile). Suicidality framing correct: "investigated and has NOT been confirmed." SURMOUNT-OSA non-miscredit present and explicit in both the read-first block and Evidence Summary: "SURMOUNT-OSA studied TIRZEPATIDE, NOT semaglutide — do not credit OSA benefit here." Relations link the research-report, both layers, [[biomarkers/hba1c]], [[biomarkers/fasting-glucose]], and [[compounds/tirzepatide]]. No Wikipedia citation in any of the three files (grep confirmed clean across all).

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/semaglutide/practitioner-layer.md","present":true,"sha256":"a98cf12f6d07cba6a263b3613264670fd54cf1c7b6525225085d2391790d790d","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/semaglutide/non-english-layer.md","present":true,"sha256":"bfc4b7bdddcf5054c6a3a0145df933bf9606c7e8c8e471e897586a204d5739b2","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
