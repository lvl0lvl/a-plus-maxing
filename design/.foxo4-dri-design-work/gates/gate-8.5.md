# Gate 8.5 — Layers Gate (Prescribing-Practice + Non-English)

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/foxo4-dri/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/foxo4-dri/non-english-layer.md","present":true,"languages_surveyed":["Chinese","Russian","Japanese"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

## Practitioner layer — detail

**File present:** YES — `vault/library/peptides/foxo4-dri/practitioner-layer.md`

**Has `## Bibliography`:** YES (lines 181–205, 12 numbered entries across regulatory, vendor_label, animal, mechanism_review, and anecdote_aggregate tags).

**Has `## Self-check`:** YES (lines 207–232).

**Compounding data sheets (admissible):** 0. The gate requirement is satisfied in explicit-absence form. Section heading reads "## No admissible compounding-pharmacy clinical data sheet located" with an explicit gate finding statement.

**Searched-vendor list present:** YES — 5 named pharmacies searched: Empower Pharmacy, Tailor Made Compounding, Hallandale Rx, Belmar Pharma Solutions, iRemedy Healthcare Peptide Intelligence Hub; plus generic compounding PDF queries. All returned negative. This satisfies the explicit-no-data-sheet + searched-vendor-list gate requirement.

**No legitimate 503A pathway:** Confirmed explicitly. FOXO4-DRI is absent from FDA Category 1, Category 2, and Category 3 503A bulk substance lists; never nominated to PCAC; no USP/NF monograph; no approved drug product. Stated in scope preamble, in the compounding section, and in the self-check.

**D-chirality-unverifiable problem:** Confirmed prominently disclosed — in the scope preamble (the CRITICAL identity problem section), in the vendor section (Pure Health Peptides / NovoPro Labs citations), and in the reconstitution section. Standard HPLC cannot verify D-amino acid chirality; only chiral HPLC or 2D NMR can confirm D-configuration, neither offered by grey-market suppliers.

**Born/Adnot 2023 Circulation adverse safety finding:** Confirmed — documented in "Safety as the dominant practitioner concern" section (reference [10], PMID 36515093). Born, Lipskaia, Adnot et al. at INSERM U955 / Hôpital Henri Mondor showed that eliminating senescent pulmonary endothelial cells with FOXO4-DRI paradoxically worsened pulmonary hemodynamics in mouse models of pulmonary hypertension. Identified as a specific absolute/high-caution contraindication for individuals with pulmonary hypertension or significant cardiovascular disease.

**Named physicians/clinics:** 0 verified. The document explicitly documents the absence: no named prescriber, no verifiable clinic URL, no NPI-listed physician was located advertising FOXO4-DRI. Fountain Life MD, AgelessRx, Defy.md — all searched; no accessible public FOXO4-DRI product or protocol page. Absence is stated, not papered over.

**named_physicians_count:** 0 (correct — the document explicitly finds and states zero).

## Non-English layer — detail

**File present:** YES — `vault/library/peptides/foxo4-dri/non-english-layer.md`

**Has `## Bibliography`:** YES (tabular bibliography, lines 133–142, with C1 + three excluded-chi entries, each with PMID/DOI, tag, tier, and language fields).

**Has `## Self-check`:** YES (lines 146–158, 8 checkbox items covering each language, the non-English-institution vs. non-English-language distinction, and the FOXO4 transcription factor vs. FOXO4-DRI peptide distinction).

**Languages surveyed:** 3 — Chinese, Russian, Japanese. Each has its own named section, per-language finding, databases-searched list, and search-terms-tried list.

**Per-language findings:**
- **Chinese:** 1 admissible item — PMID 29171222 (Liu BH et al., *Zhongguo Zhong Yao Za Zhi* 2017;42(16):3065–3071), a TCM-context aging review with a single passing FOXO4-DRI citation. Three additional Chinese-language FOXO4 transcription factor articles (PMIDs 32820304, 37462482, 37381959) were correctly identified, evaluated, and excluded with documented rationale. The Chinese-institution / English-published distinction is explicitly enforced (Zhang 2020, Li 2024, Han 2022, Kong 2025, Hu 2026 are English-published and belong to the English layer).
- **Russian:** 0 admissible. PubMed language filter returned 0 results; CyberLeninka and eLibrary.ru searches returned no Russian-language FOXO4-DRI article. Russian-language search terms documented.
- **Japanese:** 0 admissible. PubMed language filter returned 0 results; J-STAGE and CiNii searches returned 404 errors with Google site-search fallbacks returning no result. Japanese-language search terms documented.

**No fabricated citations:** The single admissible item carries PMID 29171222 and DOI 10.19540/j.cnki.cjcmm.20170731.001, both verifiable via NCBI E-utilities. Excluded articles carry verified PMIDs.

## Halt reasons

None. Both layers present with bibliography and self-check. Practitioner layer satisfies the explicit-no-data-sheet + searched-vendor-list requirement. Non-English layer covers ≥3 languages (Chinese, Russian, Japanese) with explicit per-language findings.
