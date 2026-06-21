# Phase 8.5 — LAYERS Gate — Tirzepatide (deep mode, standard+ compound)

Both layers are mandatory at deep/standard+ mode. Verified against the three target files; sha256 of both layers recomputed and matched.

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

**PASS.** Both the prescribing-practice layer and the non-English layer exist and are substantive.

- Practitioner layer (`vault/library/peptides/tirzepatide/practitioner-layer.md`): full dose/route/titration sections, compounded/access landscape, muscle-preservation adjuncts, named-prescriber section, a 9-entry **Bibliography** (`## Bibliography`), and a 4-part **Self-check** (`## Self-check`). sha256 `8087e8a1…a199e27` matches the claimed value exactly.
- Non-English layer (`vault/library/peptides/tirzepatide/non-english-layer.md`): Russian/Chinese/Japanese-other tracks, translation handling, a 3-entry **Bibliography** (`## Bibliography`), and a 5-point **Self-check** (`## Self-check`). sha256 `3074ea02…a378bfe` matches the claimed value exactly.

Neither is a stub; both are non-trivial.

## Check 2 — Practitioner layer scope discipline

**PASS.**

- **No efficacy/AE-rate claim grounded in practice/vendor sources.** The scope banner and the Self-check both assert it explicitly, and the body holds to it: every figure is a dose/route/titration/access convention, a regulatory-status fact, or a pricing figure. The one Tier-1 body-composition source [9] (PMC systematic review, ~75% fat / ~25% lean) is used *only* to frame the muscle-preservation convention and is flagged "NOT to ground an efficacy claim in this layer." Efficacy/AE-rate claims are explicitly deferred to the research report (§2/§3/§5). Confirmed.
- **Label titration tagged `regulatory`.** The 2.5 → 5 → 7.5 → 10 → 12.5 → 15 mg ladder, the 4-week-per-step rule, max 15 mg, pediatric max 10 mg, and indication-specific maintenance (5/10/15 weight; 10/15 OSA) are each tagged `regulatory` and sourced to DailyMed Mounjaro [1] / Zepbound [2][3]. The 2.5 mg rung is correctly described as a non-therapeutic initiation step. Confirmed.
- **Compounded tirzepatide reported as context WITHOUT endorsing current legality.** The compounded/access section reports the 503A/503B shortage-era market, the Dec 19 2024 shortage-resolution determination, the 60-day (503A, ~Feb 18 2025) / 90-day (503B, ~Mar 19 2025) wind-down, the N.D. Tex. litigation/remand, and salt-form/counterfeit cautions — all tagged `regulatory`/`practitioner_protocol`. It states twice that it "does not endorse current legality of compounded tirzepatide" and advises treating post-2025 large-volume compounded offerings as outside the routine exemption. No legality endorsement; no efficacy grounded on compounded supply. Confirmed.

Named-physician/compounding-sheet count is 0 (no named-prescriber off-label protocol exists for an approved Rx; reported honestly, not fabricated) — consistent with the JSON `named_physicians_count: 0` and `compounding_sheets_count: 0` with the none-finding flag true.

## Check 3 — Non-English layer honesty + LANGUAGE/AUTHOR distinction

**PASS.** Headline is an honest "ZERO genuinely non-English-LANGUAGE admissible primaries located." The **non-English-LANGUAGE vs non-English-AUTHOR** distinction is stated as the load-bearing rule and applied throughout: SURMOUNT-CN (China population), SURMOUNT-J / SURPASS-J (Japan population) are flagged as authored in non-English-speaking countries but **published in English** (JAMA PMID 38819983; Lancet D&E), therefore reachable by the English layer and excluded here. The only genuinely non-English *documents* (Japanese interview form 添付文書/インタビューフォーム; Chinese 替尔泊肽 drug-info) are regulatory materials that mirror the label and ground no claim. Russian track surveyed → derivative/none-located. Coverage gate (Russian + Chinese + Japanese/other) satisfied. No fabrication; translated-numerics tagging N/A (zero foreign-language numerics asserted).

## Check 4 — Compound entry

**PASS.**

- **Frontmatter correct.** `class: peptide`, `evidence_tier: A`, `risk_tier: medium`. Confirmed (lines 5–7).
- **Balanced benefits + caveats.** "Read this first" and Decision Notes pair large documented benefits (HbA1c 2.0–2.6% T2D; ~20.9% weight at 15 mg non-diabetic obesity; first-ever FDA OSA drug) against concrete caveats (GI-dominant AEs, +14% regain on discontinuation per SURMOUNT-4, ~25% lean-mass loss, gallbladder/pancreatitis, peri-operative aspiration, single-sponsor ~95% concentration). Balanced.
- **Dual GIP+GLP-1.** Stated repeatedly and mechanistically explained ("twincretin," single 39-aa peptide, biased agonist) — and correctly used as the distinguisher from GLP-1-only semaglutide.
- **SURMOUNT-OSA belongs here.** Present in Evidence Summary (Malhotra 2024, PMID 38912654) and framed as the basis for the Dec 2024 approval (first FDA OSA drug). Correct placement.
- **Thyroid-rodent framing.** Consistently framed as a RODENT-based boxed warning with human relevance "not determined" — NOT human-demonstrated carcinogenicity (lines 20, 24, 65). Correct.
- **Relations.** All required links present (lines 80–85): research-report, practitioner-layer, non-english-layer, `[[biomarkers/hba1c]]`, `[[biomarkers/fasting-glucose]]`, `[[compounds/semaglutide]]`. Confirmed.
- **No Wikipedia.** Grep across all three files returns no Wikipedia/Wikimedia references. Confirmed.

## sha256 verification

Recomputed both layer hashes; both match the claimed JSON values exactly:
- practitioner: `8087e8a1aaa1c32407745aafae827cf69c3ecd03f1473836959e2f7a8a199e27` ✓
- non-english: `3074ea02b21cfbe7046e8548627f020d249ba1217799f2c1db315da9ca378bfe` ✓

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/tirzepatide/practitioner-layer.md","present":true,"sha256":"8087e8a1aaa1c32407745aafae827cf69c3ecd03f1473836959e2f7a8a199e27","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/tirzepatide/non-english-layer.md","present":true,"sha256":"3074ea02b21cfbe7046e8548627f020d249ba1217799f2c1db315da9ca378bfe","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
