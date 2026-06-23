## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/mots-c/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":1,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/mots-c/non-english-layer.md","present":true,"languages_surveyed":["Russian","Chinese","Japanese"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

## Prose detail

### Practitioner layer

**File present:** Yes — `vault/library/peptides/mots-c/practitioner-layer.md`.

**Bibliography present:** Yes — `## Bibliography (own, with tag= and tier=)` section at lines 136–156, with 10 numbered entries, each carrying explicit `tag=` and `tier=` annotations.

**Self-check present:** Yes — `## Self-check` section at lines 158–176 covering: no-efficacy-on-lower-tiers, data-sheet-requirement-satisfied (explicit-absence form), regulatory-state, named-prescriber disclosure, dose-convention divergence, off-whitelist source check, and gaps/residual limits.

**Compounding-pharmacy clinical data sheets (admissible):** 0. The file correctly invokes the explicit-absence form under `## No admissible compounding-pharmacy clinical data sheet located` (line 17). Eight named pharmacies/vendors were searched — Empower Pharmacy, Empower Peptides, Tailor Made Compounding/Infiniwell, Hallandale Pharmacy, Belmar Pharma Solutions, APS, Strive Pharmacy, iPharma Pharmacy — plus generic compounding PDF queries. None yielded a clinical monograph citing its own primary literature. The absence is explained by the regulatory state: MOTS-c was removed from FDA 503A Category 2 effective April 15–22, 2026, with PCAC review scheduled July 23, 2026; no USP/NF monograph or settled 503A authorization exists. The vendor labels located (Verified Peptides, Pure Health Peptides) carry "not for human use" disclaimers and are correctly tagged `vendor_label` / tier=4, admissible only for purity/identity math.

**Named physicians:** 1 — Dr. Iman Bar, MD (DrBarx.com, Newport Beach CA), blog post September 26, 2025, tagged `practitioner_protocol` / tier=2.7. Jay Campbell (jaycampbell.com, April 29, 2026) is also named but correctly classified as `anecdote_aggregate` / tier=4 (fitness author, not an MD). Seeds / A4M / IPS / Holtorf / Lee / Paulvin / Gapin: searched, none locatable to venue+date, correctly not fabricated. `named_physicians_count` = 1 (Dr. Bar only; Campbell is not a licensed MD and is correctly not counted as a named physician).

**Gate criterion satisfied:** YES. The explicit "no admissible data sheet located" statement is present and is accompanied by the required searched-vendor list (eight named sources). Per the skill's Phase 8.5 criterion, this satisfies the data-sheet requirement in its explicit-absence form.

---

### Non-English layer

**File present:** Yes — `vault/library/peptides/mots-c/non-english-layer.md`.

**Bibliography present:** Yes — `## Bibliography` section at lines 96–111, structured as a table with columns: #, Citation, Identifier, tag, tier, language. Entries cover: explicit R-none / C-none rows, one Russian-language landscape review (CyberLeninka, stable URL), and seven English-published Chinese-institution boundary papers (B1–B7, each with verified PMID).

**Self-check present:** Yes — `## Self-check` section at lines 115–124 with checkmarks for: Russian surveyed, Chinese surveyed, originator-country noted, no fabricated citations, population annotations on animal entries, Chinese-vs-English-published distinction enforced, and honest none-located statements. Final count explicitly stated: 0 genuinely non-English admissible primaries (Russian: 0, Chinese: 0).

**Languages surveyed:**

- **Russian:** CyberLeninka.ru (direct + Google site-search), eLibrary.ru (403; site-search fallback), PubMed (Russian filter), Google Scholar (Russian filter + multiple Cyrillic search strings: «МОТС-с», «MOTS-c», «митохондриальный пептид MOTS-c», «митохондриально-кодируемый пептид», etc.), web search for Russian academic hits. Result: 0 admissible primaries. One landscape-only passing mention in a CyberLeninka mitochondria review (Kit et al., 2024) documented and excluded. Explicit none-located stated.

- **Chinese:** CNKI (indirect/site-search), CQVIP, Wanfang Data, PKU-CCJ, PubMed (Chinese filter), Google Scholar (Chinese filter + character strings: «MOTS-c», «线粒体源性肽 MOTS-c», «线粒体开放读码框 12S rRNA», «MOTS-c 运动», etc.). Result: 0 admissible Chinese-language primaries. Seven English-published Chinese-institution papers (B1–B7, Chengdu Sport University / Xihua University / Xuzhou Medical University groups) correctly classified as English-layer content and documented in the boundary section. Explicit none-located stated.

- **Originator country:** USA (USC, Lee/Cohen 2015 discovery) — originator-country literature is English, already in the English layer. No distinct non-English originator-country literature exists.

**Gate criterion satisfied:** YES. Both Russian and Chinese are surveyed with explicit none-located statements. The Chinese-institution English-published boundary papers are correctly classified and excluded from the non-English count. The admissibility distinction (English-published ≠ non-English primary) is explicitly enforced and documented. The zero-admissible-primaries result is correctly framed as a genuine finding (MOTS-c is a US-origin compound with no Russian-language research footprint and Chinese groups publishing exclusively in English), not a search gap.

---

### Summary

Both layer files exist, each has its own `## Bibliography` and self-check section. The practitioner layer carries the required explicit no-data-sheet-located finding with a named 8-vendor search list, satisfying the gate in its absence form. The non-English layer documents exhaustive surveys of Russian and Chinese with explicit none-located findings per language, correctly distinguishing English-published Chinese-institution papers from genuine non-English primaries.

**Gate 8.5: PASS.**
