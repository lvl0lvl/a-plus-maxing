# Gate 8.5 — Layers Verification (Humanin, mode=deep)

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/humanin/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":1,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/humanin/non-english-layer.md","present":true,"languages_surveyed":["Japanese","Chinese","Russian"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

## Prose Detail

### Practitioner Layer

**File:** `vault/library/peptides/humanin/practitioner-layer.md` — PRESENT.

**Bibliography:** Present. Section heading `## Bibliography (own, with tag= and tier=)` at line 161. Contains 8 numbered references (sources 1–8) plus entry 5a, each carrying explicit `tag=` and `tier=` annotations.

**Self-check:** Present. Section `## Self-check` at line 181. Covers: no-data-sheet gate finding confirmation, no-efficacy-grounded-on-tiers confirmation, regulatory-state honesty, pro-tumor contraindication disclosure, native-vs-analog caveat, named-prescriber conventions, convention-divergence disclosure, off-whitelist sources check, source-4 retrieval caveat, and residual gaps.

**Compounding data sheets (admissible):** 0 admissible compounding-pharmacy clinical data sheets. The document's `## No admissible compounding-pharmacy clinical data sheet located` section provides the explicit-absence finding in gate-compliant form, with a 6-pharmacy search list:
- Empower Pharmacy
- Tailor Made Compounding
- Hallandale Pharmacy
- Belmar Pharma Solutions
- South Lake Pharmacy / SL Compounding
- iPharma Pharmacy
…plus generic compounding PDF queries. No admissible data sheet was returned by any of these. This satisfies the explicit-no-sheet + vendor-list gate requirement.

**Research-chemical vendor labels:** 2 vendor labels found (InvivoChem, Pure Health Peptides), both explicitly tagged `vendor_label` and tier=4, restricted to purity/identity/reconstitution math only.

**Named physicians:** 1 verifiable named physician with venue and NPI confirmed: Dr. Richard Koffler, MD (Physiatrist), Holistic Medical Wellness, Miami Beach FL / Woodbury NY, NPI 1467557264, tagged `practitioner_protocol` tier=2.7. A second named clinic (Paragon Sports Medicine) appeared as `anecdote_aggregate` — not a physician protocol. Jay Campbell, Ben Greenfield: fitness authors, not MDs. Named_physicians_count = 1 (the one carrying a verifiable NPI and prescriber framing).

**Dominant safety point:** Pro-tumor contraindication (anti-apoptotic mechanism; TNBC Moreno Ayala 2020 animal data) is positioned before the dose conventions section and is the lead safety concern — confirmed prominent placement.

**Regulatory state:** Humanin confirmed not on FDA 503A Category 1 or Category 2; no 503A compounding pathway; no IND; no completed Phase 1; no USP/NF monograph. No legitimate prescribing pathway exists.

**Gate verdict for practitioner layer: PASS** — explicit-absence form with 6-vendor search list satisfies the data-sheet gate. Bibliography and self-check present.

---

### Non-English Layer

**File:** `vault/library/peptides/humanin/non-english-layer.md` — PRESENT.

**Bibliography:** Present. Formal bibliography table at line 287 (`## Bibliography`), covering all 8 admissible non-English primaries plus the excluded CyberLeninka reference, each with identifier, tag, tier, and language columns.

**Self-check:** Present. Section `## Self-check` at line 305. Per-language checklist items for Japanese, Chinese, and Russian; originator-country note; no-fabrication attestation; population annotations; HNG-analog flags; genuine-non-English vs English-published distinction enforcement; honest per-language findings and final count.

**Languages surveyed:** 3 — Japanese, Chinese, Russian. Meets the ≥3 requirement.

**Per-language findings:**

- **Japanese:** 2 admissible items (J1: Niikura et al. 2003, PMID 12649845, *Nihon Ronen Igakkai Zasshi*; J2: Niikura & Nishimoto 2004, CiNii CRID 1050845762328562944, *Keio Igaku*). Both are invited reviews from the originator Nishimoto lab at Keio University. Both confirmed "[Article in Japanese]" by PubMed language indexing / CiNii language tag. Databases searched: CiNii Research, J-STAGE, PubMed (language filter), KAKENHI.

- **Chinese:** 4 admissible items (C1–C4). 1 review (C1, PMID 17262962) + 3 primary experimental studies (C2: PMID 19377823, in vitro cortical neurons; C3: PMID 20423647, in vitro PC12 cells, HNG-analog; C4: PMID 23258324, in vivo rat spatial memory, HNG-analog). All confirmed "[Article in Chinese]" by PubMed language filter. Databases searched: PubMed, CNKI (indirect), Wanfang, CQVIP, CJCB direct URL, Chinese-character web search terms.

- **Russian:** 2 admissible primary studies (R1: PMID 16583711, yeast two-hybrid molecular study, ING RAS Moscow 2006; R2: PMID 30726649, human clinical CHD study, Military Medical Academy St. Petersburg 2018). Both confirmed "[Article in Russian]" by PubMed language indexing / journal identity. R2 is the only Russian-language human clinical humanin study in the indexed literature (n=59 CHD patients). Databases searched: PubMed, CyberLeninka, eLibrary.ru, Russian-character web search terms.

**Non-English primary count:** 8 total admissible (Japanese: 2 reviews; Chinese: 1 review + 3 primary; Russian: 2 primary). Three experimental primaries (C2, C3, C4) and two Russian primaries (R1, R2) add evidence beyond the English corpus.

**Gate verdict for non-English layer: PASS** — ≥3 languages with explicit per-language findings confirmed; bibliography and self-check present; no fabricated citations; admissibility distinction (English-published vs non-English-language) enforced throughout.

---

### Overall Gate 8.5 Verdict: PASS

Both mandatory layers are present. Both carry an independent bibliography and a self-check section. The practitioner layer satisfies the data-sheet gate via the explicit-absence form with a 6-vendor searched list. The non-English layer documents ≥3 languages (Japanese, Chinese, Russian) with explicit per-language findings and 8 verified admissible non-English primaries (0 fabricated).
