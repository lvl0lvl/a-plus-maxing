# Gate 8.5 — LAYERS (Retatrutide, deep mode, standard+ compound)

Both layers are mandatory at this mode. All three target files read and verified; both layer sha256 hashes recomputed and match the claimed values.

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

PASS. Both `practitioner-layer.md` and `non-english-layer.md` exist and are substantive (not stubs).
- Practitioner layer: scope-discipline header, "Dose reference (TRIAL-DERIVED)", "Gray-market / access", "Named-prescriber / guideline protocols", a 7-item **Bibliography** (each tagged + tiered), and a 4-paragraph **Self-check**.
- Non-English layer: Russian, Chinese, Japanese/other tracks, Translation-handling section, a **Bibliography** (one provenance-only item NE-RETA-D1), and a 5-bullet **Self-check** with explicit gate results.
- sha256 verified: practitioner `51833eed…262757` (match), non-English `02ff25ec…1a84fe9` (match).

## Check 2 — Practitioner layer discipline

PASS.
- **No efficacy/AE-rate claim grounded in practice/vendor sources.** The header and Self-check both explicitly route every efficacy/AE figure to the research report (§2/§3/§5) as Tier-1 Phase-2 evidence. The body contains only dose/route/titration conventions, regulatory-status facts, gray-market/access description, and a qualitative cost note. Vendor/journalistic items (`vendor_label`, `journalistic-context`) and the one practitioner voice (`practitioner_protocol`, Hormachea RD — opinion/advice) ground no efficacy or AE-rate claim.
- **Dose framed as TRIAL-DERIVED, not a label.** Section title is literally "Dose reference (TRIAL-DERIVED, NOT a label)"; the trial titration (1/4/8/12 mg; initial 2/4 mg; SC weekly ×48 wk; Phase-3 6 mg intermediate step) is tagged `regulatory / trial-derived` throughout and repeatedly stated to be "never a clinical dose," "not a how-to," "no validated dose for any indication, no approved package insert."
- **Gray-market premature-use caution prominent; no compounding pathway.** "Especially premature" appears in the read-first header, the gray-market section, and the Self-check. "No lawful compounding pathway" is stated with FDA grounding (cannot be compounded under federal law; not a component of an FDA-approved drug). Documented sterility-test failures despite high-purity COAs are flagged as a real, not theoretical, failure mode.
- Compounding sheets count: **0** (and the absence is reported as an honest finding, not fabricated). Named-physician/prescriber protocols: **0** (Hormachea RD is the only practitioner voice and she advises *against* non-trial use rather than supplying a protocol — correctly not counted as a named-prescriber dosing protocol).

## Check 3 — Non-English honest "none distinct" + LANGUAGE-vs-AUTHOR

PASS. Headline result is an honest, well-characterized near-null: **0 genuinely non-English-LANGUAGE admissible primaries.** The non-English-LANGUAGE vs non-English-AUTHOR distinction is explicitly load-bearing and enforced — the TRIUMPH international sites and the dedicated Phase 1 study in Japanese adults (PMDA support) are run at non-English sites but **published/reported in English**, so they belong to the English layer. Russian, Chinese, and Japanese/other tracks all surveyed (Chinese footprint is supply-chain/commercial, not scholarly). The only genuinely non-English *document* is a J-GLOBAL/JST machine-translation index of an English review (cited for provenance only, grounds no claim). No fabrication; translated-numerics tagging N/A (zero foreign-language numerics).

## Check 4 — Compound entry

PASS.
- **Frontmatter:** `class: peptide`, `evidence_tier: B`, `risk_tier: experimental` — all correct.
- **INVESTIGATIONAL framing / −24.2% pairing.** Every occurrence of the −24.2%/48-wk/12 mg headline is paired with hard qualifiers: read-first block ("INVESTIGATIONAL, NOT APPROVED anywhere" + "Phase 2 only"), Evidence Summary ("Phase 2 / investigational"), risk_tier and metadata ("INVESTIGATIONAL — not approved … most advanced evidence is Phase 2"). Phase-3 TRIUMPH explicitly flagged as sponsor topline press releases / not verified efficacy.
- **Triple mechanism** present: GIP + GLP-1 + glucagon (GCGR) receptor agonist, with the glucagon arm called out as the defining differentiator vs tirzepatide and semaglutide.
- **Relations** link: research-report, practitioner-layer, non-english-layer, `[[biomarkers/hba1c]]`, `[[compounds/tirzepatide]]`, `[[compounds/semaglutide]]` — all required links present.
- **No Wikipedia.** No wikipedia.org reference anywhere in the entry or either layer.

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/retatrutide/practitioner-layer.md","present":true,"sha256":"51833eed9e1f044a3b0c3ca9f0c0212bf918df4a7771e004c4fb344053262757","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/retatrutide/non-english-layer.md","present":true,"sha256":"02ff25ec6bc586087f95071cb48a799782a7f098767d1edb26c97385e1a84fe9","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
