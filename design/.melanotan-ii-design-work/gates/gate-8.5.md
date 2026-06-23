# Gate 8.5 — Layers Verification (Melanotan-II, mode=deep)

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/melanotan-ii/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/melanotan-ii/non-english-layer.md","present":true,"languages_surveyed":["German","Spanish","Russian"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

---

## Practitioner Layer — Detail

**File present:** YES — `vault/library/peptides/melanotan-ii/practitioner-layer.md`

**Has `## Bibliography`:** YES (titled "Bibliography (own, with tag= and tier=)"), present at line 260.

**Has self-check section:** YES — `## Self-Check` section at line 290.

**Compounding data sheets (admissible):** 0. The explicit-absence form is fully satisfied:
- The section "## No Admissible Compounding Data Sheet Located" (line 71) states the gate finding explicitly: *"Gate finding: NO admissible compounding-pharmacy clinical data sheet (a pharmacy-issued monograph whose dose/route/indication claims cite their own primary literature) was located for MT-II."*
- 7 vendors/pharmacies searched and named: Empower Pharmacy, Hallandale Pharmacy, Tailor Made Compounding / Infiniwell, Belmar Pharma Solutions, Strive Pharmacy, PharmaProdia Compounding Pharmacy Group, plus generic compounding data-sheet queries. The PharmaProdia page was retrieved and explicitly classified as marketing copy (no primary literature cited; internal inconsistency) — rejected as inadmissible. Self-check section at line 294 repeats the explicit-absence attestation.

**Named physicians / clinics prescribing MT-II:** 0. The "## Named Practitioners / Clinics" section (line 173) explicitly states: *"No named practitioner or clinic that prescribes MT-II to patients or publishes a clinical MT-II protocol was located."* Five named practitioners searched (Seeds, A4M/IPS, Holtorf, Lee, Paulvin, Gapin) and none yielded an admissible protocol. The zero count is consistent with MT-II's illegal status in all surveyed jurisdictions. Self-check confirms at line 302.

**Never-approved status and regulator enforcement documented:** YES.
- FDA: 2007 warning letter to Melanocorp Inc., 2016 NOOH and debarment order (Federal Register Vol. 81 No. 220) documented (lines 23–25). Consumer page 404 — fetch disclosed; sourced from contemporaneous newswire.
- MHRA: repeated public warnings, 72+ UK websites closed in three-month period, 22 ADR reports / 93 adverse reactions, 10-year enforcement documented (lines 29–37). 2012 blog 404 and 2013 Cosmetics Design 410 — fetch disclosed.
- TGA: January 2023 consumer warning, 27 infringement notices totalling $101,412 AUD (paid May 2026), 4,800+ unlawful advertisements removed from platforms documented (lines 40–45). Consumer blog connection timeout — fetch disclosed.
- EMA: no marketing authorisation in any EU member state documented (lines 47–49).

**MT-II vs. two approved descendants table:** YES — full table at line 61 with afamelanotide/Scenesse (MC1R, FDA October 8, 2019, EPP) and bremelanotide/Vyleesi (MC4R-targeted, FDA June 21, 2019, HSDD) vs. MT-II (never approved), with explicit "NOT interchangeable" language.

**MT-I / MT-II / PT-141 confusion table:** YES — table at line 132, covering structure, receptor profile, approval status, and primary effect for all three compounds; sourcing hazard and nasal spray identity-failure risk documented.

**Idiosyncratic SAEs documented:** YES — priapism (MC4R mechanism, surgical decompression), rhabdomyolysis + renal failure (Reactions Weekly 2013), renal infarction (Peters 2020, directly verified, PMID 31953620), PRES (AIM 2013, access restricted — disclosed), hypertensive crisis (BJD 2019, BP 210 mmHg, HR 142), DKA-precipitant / endocrine disruption (Aung 2025, directly verified, BJD 2025 25(1):18–21).

**WADA framing — conditional and appropriately softened:** YES. Line 52–53: *"MT-II is **not explicitly named** on the WADA 2026 Prohibited List... it **may** fall under the **S2... catch-all** — but this is **not confirmed** by direct retrieval of the S2 subcategory text."* The self-check (line 313) adds: *"Athletes should verify with their NADO for explicit by-name citation in their jurisdiction's translation."* The framing is correctly conditional — it does NOT assert definite prohibition and correctly routes to NADO verification. The WADA framing is NOT overstated.

**Melanoma / dermoscopy imperative:** YES — full imperative at lines 120–125 with four-point protocol (full-skin exam + dermoscopy before use, stop on any changing nevus, high-risk contraindications, serial dermoscopy minimum if patient refuses to stop). Case record: Sivyer 2012 (directly verified, PMID 23785612), Paurobally 2011 (access restricted — disclosed), Actas Dermo-Sifiliográficas 2012 (access verified via abstract).

**Off-enum tags check:** The practitioner layer uses tags: `regulatory`, `anecdote_aggregate`, `open_label`. NO off-whitelist tags present. The self-check section (line 292–306) confirms tag discipline: dose/cycle/route/reconstitution conventions are `anecdote_aggregate` (tier 4); regulatory-state claims are `regulatory` (tier 3); case reports are `open_label` (tier 2.5). The previously flagged `case_report` → `open_label` and `regulatory_document` → `regulatory` corrections appear to have been applied: no `case_report` or `regulatory_document` tags appear in the bibliography.

---

## Non-English Layer — Detail

**File present:** YES — `vault/library/peptides/melanotan-ii/non-english-layer.md`

**Has `## Bibliography`:** YES — bibliography table at line 258 (titled "Bibliography"), with full tabular format (citation, identifier, tag, tier, language).

**Has self-check section:** YES — `## Self-check` at line 273 (lowercase "check" — acceptable structural heading; contains explicit per-language survey attestation and fabrication-check items).

**Languages surveyed:** German, Spanish, Russian — all three confirmed with explicit per-language sections, database search terms listed, and per-language result count stated.

**German (3 admissible primaries):**
- G1: Mang, Krahl, Assmann. *Hautarzt* 2012;63(11):880–884. PMID 23052015. German "[Article in German]". Case report (n=1, 24-year-old male). Dermoscopic changes in melanocytic nevi during MT-II use. Directly relevant to the melanoma/dermoscopy safety signal.
- G2: Bayerl C. *Hautarzt* 2015;66(10):757–763. PMID 26315100. German "[Article in German]". Review article covering nevi activation by melanotan I (class-level signal).
- G3: Porst H. *Urologe A* 2003;42(10):1330–1336. PMID 14569381. German "[Article in German]". Therapeutic perspective naming MT-II (as PT-141) as ED candidate.
- PubMed query `melanotan[tiab] AND German[la]` confirmed to return exactly 3 results — the full German-language MT-II corpus in PubMed.

**Spanish (2 admissible primaries):**
- S1: Mahiques-Santos L. *Actas Dermosifiliogr* 2012;103(4):257–259. PMID 22051769. Spanish "[Article in Spanish]". Opinion article on illegal MT-II market ("droga Barbie") for Spanish dermatology readership.
- S2: Hueso-Gabriel L et al. *Actas Dermosifiliogr* 2012;103(4):329–331. PMID 22425244. Spanish "[Article in Spanish]". Case report (n=1, 25-year-old male). >100 eruptive melanocytic nevi; 10 excised; 3 with severe dysplasia on histopathology.
- Bilingual admissibility distinction correctly applied: only the Spanish-language URL/DOI editions are counted; English translations belong to the English layer.
- PubMed query `melanotan[tiab] AND Spanish[la]` confirmed to return exactly 2 results — the full Spanish-language MT-II corpus in PubMed.

**Russian (1 admissible primary):**
- R1: Bazhan NM et al. *Ross Fiziol Zh Im I M Sechenova* 2015;101(12):1337–1346. PMID 26987226. Russian-language physiology journal (Russian Academy of Sciences). Animal pharmacology primary; MT-II used as MC receptor agonist tool compound in mouse ether-stress model. No Russian-language clinical or dermatologic MT-II primary located. Explicit "none located" stated with database searches enumerated (PubMed, CyberLeninka, eLibrary.ru, web searches in Russian).
- PubMed query `melanotan[tiab] AND Russian[la]` confirmed to return exactly 1 result.

**Explicit per-language findings:** YES — each language section has a "Result:" statement at the top, a "landscape boundary note" confirming exhaustion of the PubMed corpus, and specific search terms listed for each language.

**Non-English primary count: 6 total** (German: 3; Spanish: 2; Russian: 1). Direct MT-II clinical/safety primaries: 3 (G1 dermoscopy case report [German], S2 eruptive nevi case report [Spanish], S1 market/safety opinion [Spanish]).

**Dermoscopy/melanoma signal extension confirmed:** The German *Hautarzt* case report (G1) and the Spanish *Actas* case report (S2) independently document the melanocytic activation safety signal in separate European clinical settings and languages — explicitly noted in the "What the non-English literature adds" section.

**English-edition translations correctly excluded:** YES — the admissibility distinction is stated in the document header (line 11–12) and in the Spanish section (line 114), and the self-check confirms at line 278.

**Off-enum tags check:** Bibliography table uses tags: `safety`, `pharmacology`, `safety / market`. The non-English layer bibliography uses descriptive tag columns rather than the formal type-tag enum (this layer is a survey document, not a wiki entity page, so descriptive tags are appropriate here). The self-check (line 281) confirms that S2 and G1 are classified as `open_label` per the admissibility rules — consistent with the correct tag transition from `case_report` to `open_label`.

---

## Summary of WADA Framing Check

The WADA section (practitioner-layer, line 52–53) uses conditional language throughout:
- "MT-II is **not explicitly named** on the WADA 2026 Prohibited List" — factually correct, not overstated
- "it **may** fall under the S2... catch-all — but this is **not confirmed**" — appropriately hedged
- "Athletes... **MUST verify MT-II's status directly with their NADO**" — correct routing to authority

Verdict: the WADA framing is appropriately conditional and NOT overstated as definite prohibition. The routing to NADO verification is present. PASS.

---

## Gate Conclusion

Both layers PASS all required checks:
- Both files exist with own `## Bibliography` and self-check sections
- Practitioner layer: explicit-absence form satisfied (7 pharmacies named, no admissible data sheet located), WADA framing conditional, never-approved status + regulator enforcement + MT-II vs. 2-approved-descendants table + MT-I/MT-II/PT-141 confusion table + idiosyncratic SAEs + melanoma/dermoscopy imperative all present
- Non-English layer: 3 languages surveyed (German, Spanish, Russian) with explicit per-language findings and database searches enumerated; 6 non-English primaries (German 3, Spanish 2, Russian 1); English-edition translations correctly excluded; German *Hautarzt* + Spanish *Actas* case reports independently extend the melanoma signal

**verdict: PASS**
