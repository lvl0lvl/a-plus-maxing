# Phase 8.5 — LAYERS Gate: AOD-9604 (deep mode, standard+ compound)

Both layers mandatory at this mode. Verdict basis below.

## Check 1 — Both layers exist, non-trivial, Bibliography + Self-check

**PASS.** Both layers are present, substantial, and well-structured.

- **Practitioner layer** (`practitioner-layer.md`, sha256 `ec87d4bc…`): non-trivial (dose/route conventions, named-prescriber data point, trial-derived-for-contrast section, compounding/access gate, reconstitution arithmetic table). Has a numbered **Bibliography** (11 entries, each tag+tier) and a dedicated **Self-check** section (5 bullets).
- **Non-English layer** (`non-english-layer.md`, sha256 `19ce3b41…`): non-trivial (Russian, Chinese, Other/originator-country sections each with databases + search terms; translation-handling notes). Has a **Bibliography** (provenance/exclusion items, tag+tier+language) and a **Self-check** section (coverage gate, no-fabrication, LANGUAGE-vs-AUTHOR, translated-numerics, count).

## Check 2 — Practitioner layer discipline

**PASS.**

- **No efficacy/AE-rate claim grounded in practice/vendor sources.** The scope banner and Self-check both state every figure is dose/route/cycle/reconstitution convention or a regulatory/access fact (`practitioner_protocol`/`vendor_label`/`regulatory`), and that no efficacy or AE-rate claim is grounded on any source here. The efficacy state and safety record are deferred to the research report (§2/§5). Human efficacy is explicitly carried as **FAILED**, with repeated "no efficacy is implied by any dose here."
- **Gray-market ~300 mcg SC vs trial-derived oral dose kept distinct.** Gray-market convention = ~300 mcg SC once daily, AM fasted, 8–12 wk; trial-derived = oral ~1 mg/day, tagged `regulatory — trial-derived`, explicitly "NOT a convention," and the "trials used up to 1,000 mcg/day" claim flagged as a misattribution risk. The two are never conflated.
- **NOT-compoundable gate honest.** Explicit mechanical chain: §503A Category-2 (Sept 2023) → removed ~27 Sep 2024 **only because the nomination was withdrawn**, **never Category-1** → not lawfully compoundable. Compounding-data-sheet search recorded as **NONE FOUND** (Empower/Tailor Made/Hallandale/Belmar/APS/Strive), framed as the expected result; access channel = gray-market research-chemical only.
- **Named prescriber:** Dr. Dan Wool, NMD (Practical Vitality PLLC / "Natural Gastro," Scottsdale AZ; published 26 Feb 2026) — name + venue + date present → counts as one named-prescriber protocol. Venue-only clinic pages explicitly down-ranked as not meeting the name+venue+date bar. **named_physicians_count = 1.**

## Check 3 — Non-English layer honesty + LANGUAGE-vs-AUTHOR

**PASS.** Headline result is honest **"NONE LOCATED"** for both Russian (eLibrary/CyberLeninka — vendors only) and Chinese (CNKI/Wanfang/ChemicalBook — one reagent catalog citing English refs). The **LANGUAGE-vs-AUTHOR** distinction is explicitly enforced: non-Anglophone-authored but English-published work (Kwon & Park 2015 Korea; non-English-named co-authors on Monash/Metabolic papers) is correctly classed as already in the English corpus, not as non-English primaries. Originator-country (Australian) is English-language → valid "none non-English." Genuine non-English admissible sources added: **0** (clean, justified null). Databases + Cyrillic/Chinese search terms documented; no fabrication.

## Check 4 — Compound entry frontmatter + framing + relations + no Wikipedia

**PASS.**

- **Frontmatter:** `class: peptide` ✓, `evidence_tier: C` ✓, `risk_tier: experimental` ✓.
- **Framing present:** FAILED Phase-2b obesity RCT (~536 pts, 24 wk, oral, negative primary, program discontinued ~2007) ✓; Paradigm OA-conflation **excluded** as pentosan polysulfate (iPPS/Zilosul), not AOD-9604 ✓; self-affirmed **GRAS ≠ FDA approval / not a lawful US dietary ingredient** (DSHEA drug-exclusion) ✓; **WADA PROHIBITED** (S0 catch-all 2013, also S2 GH-fragment scope; Essendon AFL saga) ✓.
- **Relations:** links to research-report, practitioner-layer, non-english-layer, `[[biomarkers/igf-1]]`, and `[[compounds/tesamorelin]]` — all five present ✓.
- **No Wikipedia:** zero Wikipedia references in any of the three files (grep = 0). ✓

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","mode":"deep","practitioner_layer":{"path":"vault/library/peptides/aod-9604/practitioner-layer.md","present":true,"sha256":"ec87d4bcd0e27cae9f51c7c818a53e33dd22940af1ea5419eef8bebef9dc4b4d","compounding_sheets_count":0,"compounding_sheets_or_null_finding":true,"named_physicians_count":1,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/aod-9604/non-english-layer.md","present":true,"sha256":"19ce3b41f6fe392586b5d4643dfa05827a9e58509fa7ada64f074f513c73fac8","languages_surveyed":["Russian","Chinese","Other"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```
