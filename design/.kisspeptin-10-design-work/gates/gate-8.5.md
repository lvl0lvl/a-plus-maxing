# Gate 8.5 — Layers Verification (Kisspeptin-10, mode=deep)

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/kisspeptin-10/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/kisspeptin-10/non-english-layer.md","present":true,"languages_surveyed":["Japanese","Chinese","Russian"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

## Prose detail

### File existence

Both files are present and readable:
- `vault/library/peptides/kisspeptin-10/practitioner-layer.md` — confirmed present
- `vault/library/peptides/kisspeptin-10/non-english-layer.md` — confirmed present

---

### Practitioner layer

**Bibliography:** Present — 14 numbered entries with `tag=` and `tier=` annotations covering regulatory (PCAC, USADA), open-label academic, anecdote_aggregate, and vendor_label sources.

**Self-check:** Present — final section titled `## Self-check` explicitly verifies: no efficacy grounded on Tier-3/4 sources; data-sheet requirement satisfied in explicit-absence form; regulatory state verified; WADA status verified; all four hazards disclosed; named-practitioner conventions disclosed; convention divergence disclosed; fetch failures disclosed; off-whitelist sources check; gaps/residual limits enumerated.

**Compounding data sheet requirement (explicit-absence form):** PASSES. The document opens with section `## No admissible compounding-pharmacy clinical data sheet located` and the self-check repeats `No admissible compounding-pharmacy clinical data sheet was located for kisspeptin-10.` Seven pharmacies/vendors explicitly searched and reported as yielding no admissible sheet:
1. Empower Pharmacy — not listed as a compounded product
2. Tailor Made Compounding / Infiniwell — no public KP-10 clinical monograph
3. Hallandale Pharmacy — no public KP-10 clinical monograph
4. Belmar Pharma Solutions — no public KP-10 data sheet
5. Strive Pharmacy — no public KP-10 data sheet
6. APS (Applied Pharmacy Services) — no public KP-10 data sheet
7. Beverly Hills Rejuvenation Center — clinic marketing copy, explicitly not a compounding clinical data sheet

Three research-chemical vendor labels (Core Peptides, Heritage Labs, Biotech Peptides) were located and tagged `vendor_label` for purity/identity context only — explicitly stated as NOT constituting a compounding clinical data sheet. `compounding_sheets_count = 0` is correct and satisfies the gate via the explicit-no-sheet + vendor-list route.

**Named physicians count:** 0 admissible named prescribers with citable dated protocols. Beverly Hills Rejuvenation Center lists physician oversight language but no named physician and no dated protocol — categorized `anecdote_aggregate`. Seeds/A4M/IPS/Holtorf/Lee/Paulvin/Gapin/Campbell — each searched, none found, none fabricated. `named_physicians_count = 0` is accurate.

**Four required hazards confirmed present:**
1. KP-10 vs. KP-54 isoform confusion — fully documented (half-life table, MW, BBB crossing, LH duration)
2. Desensitization trap (KISS1R tachyphylaxis) — fully documented with specific observations from human and primate data
3. WADA S2 prohibition in males — documented with correction of FormBlends error
4. PT-141/Vyleesi is the approved HSDD drug, not KP-10 — fully documented with categorical difference stated

**US no-pathway (PCAC 11-0 vote, Oct 2024, 503A closed):** Confirmed present in the regulatory preamble box and bibliography source [1] (PCAC October 29, 2024, 11-to-0 against).

---

### Non-English layer

**Bibliography:** Present — 18-row table with columns `# | Citation (short) | Identifier | tag | tier | language`, covering all 18 admissible items (J1–J4, C1–C8, R1–R6).

**Self-check:** Present — section titled `## Self-check` with 7 checked items confirming: three languages surveyed, each language's database/search-term coverage, originator country noted, no fabricated citations, population annotations on all animal/cell entries, genuine non-English vs English-published distinction enforced, honest per-language findings. Concludes with explicit total count.

**Languages surveyed (≥3 required):** PASSES. Three languages confirmed:

- **Japanese:** 4 admissible items (J1–J4). J1 = invited review in *Nihon Yakurigaku Zasshi* (PMID 24107517). J2 = review in *Kenbikyo* (DOI 10.11410/kenbikyo.46.2_111, J-STAGE confirmed). J3 = review in *Nihon Juishikai Zasshi* (DOI 10.12935/jvma.64.39). J4 = conference proceedings primary in *Nihon Hanshoku Seibutsu Gakkai Koen Yoshishu* (DOI 10.14882/jrds.108.0_or2-2, CiNii confirmed). Explicitly noted: 0 full primary experimental articles in Japanese-language peer-reviewed journals; the Ohtaki/Takeda discovery and Nagoya University primary program are entirely English-published.

- **Chinese:** 8 admissible items (C1–C8). 5 primaries: C1 (castrated male mice, LPS/DEX on hypothalamic kisspeptin/GPR54), C3 (KISS1 tumor-suppressor in gastric cancer, n=50 human tissue + MKN-45 in vitro), C5 (electroacupuncture on hypothalamic kisspeptin in PCOS rats), C6 (electroacupuncture on ovarian kisspeptin/KISS1R in PCOS rats), C7 (kisspeptin in endometrial decidualization / RSA, n=45 human + hESC). 3 reviews: C2, C4, C8. All 8 confirmed "[Article in Chinese]" by PubMed language tag.

- **Russian:** 6 admissible items (R1–R6). 3 primaries: R1 (human ovarian tissue kisspeptin across ontogenesis, PMID 31800179), R2 (sirtuins and kisspeptin in ovarian aging, PMID 33993657), R4 (preoptic nucleus kisspeptin-melatonin interaction in aged male Wistar rats, PMID 25051762). 3 reviews: R3, R5, R6. All 6 confirmed "[Article in Russian]" by PubMed language tag.

**Total admissible non-English items:** 18 (J:4 + C:8 + R:6).

**Per-language findings:** Explicit per-language result stated in each section header ("Result: 4 genuinely Japanese-language admissible items located"; "Result: 8 genuinely Chinese-language admissible items located"; "Result: 6 genuinely Russian-language admissible items located"). Databases searched and search terms used documented for each language.

---

### Gate verdict: PASS

Both layers present, each with `## Bibliography` and a self-check section. Practitioner layer satisfies the data-sheet requirement via explicit-absence form with 7 searched vendors documented. Non-English layer documents ≥3 languages (Japanese, Chinese, Russian) with explicit per-language findings and 18 total admissible entries. No halt conditions triggered.
