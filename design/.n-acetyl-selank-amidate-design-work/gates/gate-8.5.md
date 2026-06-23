---
phase: "8.5"
compound: n-acetyl-selank-amidate
mode: deep
verifier: layers-gate
date: 2026-06-21
---

## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/n-acetyl-selank-amidate/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/n-acetyl-selank-amidate/non-english-layer.md","present":true,"languages_surveyed":["Russian","Chinese","German"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

## Prose Detail

### Practitioner Layer

**File:** `vault/library/peptides/n-acetyl-selank-amidate/practitioner-layer.md`
**Present:** YES

**Bibliography:** Present. 9 entries, contiguous integers [1]–[9]. Tags used: `vendor_label` ([1], [3], [4]), `anecdote_aggregate` ([2], [5], [8], [9]), `regulatory` ([6], [7]). No off-enum tags found — `regulatory_document` (the tag that was reportedly fixed) does not appear; `regulatory` is used correctly throughout.

**Self-check:** Present (`## Self-check` section, covering all six required checks including the explicit-absence data-sheet attestation, regulatory honesty, named-practitioner disclosure, four hazards, off-whitelist-source check, and whitelisted vendor confirmation).

**Compounding data sheet (explicit-absence form):** NO admissible data sheet was located. The gate heading `## No admissible compounding-pharmacy clinical data sheet located` satisfies the explicit-no-sheet requirement. Searched vendors documented: Empower Pharmacy, Tailor Made Compounding / Infiniwell, Hallandale Pharmacy, Belmar Pharma Solutions, Strive Pharmacy, Simon's Compounding (confirmed NOT a 503A pharmacy), Paragon Sports Medicine (clinic, no named protocol), plus generic PDF query sweeps. This satisfies the vendor-list requirement. `compounding_sheets_count = 0` (explicit-absence form, not a search failure — regulatory state explains the gap: Selank acetate is not on the 503A Category 1 bulks list).

**Named physicians:** `named_physicians_count = 0`. Explicit no-practitioner disclosure: no named MD/DO/NP + clinic + date + N-Acetyl-Selank-Amidate-specific protocol was located. Searched list documented (Seeds, Holtorf, Lee, Paulvin, Gapin, A4M/IPS, Klearmind Clinics, Paragon Sports Medicine, innerbody.com, peptideinitiative.com, peptidedosingprotocols.com, thepeptidecatalog.com).

**Regulatory history documented:** Analog-approved-nowhere confirmed; parent-Selank-Russia-only confirmed; Selank acetate / TP-7 503A Category 2 history (September 2023 placement → September 27, 2024 nominator-withdrawal removal → NOT a safety clearance, NOT Category 1 authorized) confirmed at [6, regulatory] and in the regulatory section.

**Vendor split confirmed:** Limitless Life Nootropics (`vendor_label`, [3]) and Pure Health Peptides (`vendor_label`, [4]) are whitelisted; Umbrella Labs, BC9.co, Peptide Sciences, Simon's Compounding are collectively tagged `anecdote_aggregate` [5]. Simon's Compounding is also cited individually as [1, vendor_label] for the COA/product detail but the NOT-a-503A-pharmacy distinction is explicit.

**Four hazards documented upfront:**
1. Selank-vs-analog conflation — binding-epitope disruption (N-terminal acetylation eliminates free α-amine of Thr residue, key Tuftsin receptor-binding element): confirmed.
2. Immunogenicity from subcutaneous injection of a terminally modified non-endogenous peptide: confirmed.
3. Population-direction reversal (anxiolytic in anxious patients may be activating/anxiogenic in healthy non-anxious users): confirmed.
4. WADA S0 unambiguously applicable (no regulatory approval anywhere); S2 (PMC13164565 assertion) not independently confirmed against primary WADA document — disclosed explicitly: confirmed.

**Dosing conventions:** Intranasal (600–900 mcg/day, 2–3 sprays, up to 14 days on [8, anecdote_aggregate]) and subcutaneous injection (150–300 mcg/day or 250–500 mcg/day, 4–6 weeks on [9, anecdote_aggregate]) both tagged anecdote_aggregate and explicitly stated to ground NO efficacy claim.

**Off-enum tag check:** PASS. No `regulatory_document` tag found. All tags are drawn from the valid enum: `vendor_label`, `anecdote_aggregate`, `regulatory`.

---

### Non-English Layer

**File:** `vault/library/peptides/n-acetyl-selank-amidate/non-english-layer.md`
**Present:** YES

**Bibliography:** Present. Table format (R1–R10), 10 entries. All entries carry either a confirmed PMID (R1–R7) or a confirmed CyberLeninka stable URL (R8–R10). Tags: `open_label` (R1, R2), `animal_model` (R3, R4, R5, R6, R7, R9, R10), `in_vitro` (R8) — all valid enum values. No off-enum tags.

**Self-check:** Present (`## Self-check` section, 11 checkboxes explicitly evaluating: three-language gate, Russian survey methodology, developer-network flagging, translation provenance, Chinese survey, German survey, analog-specific search in all languages, no-fabrication attestation, population annotation, tier ratings, honest per-language findings).

**Languages surveyed:** Three languages — Russian, Chinese, German. Satisfies ≥3 language requirement.

**Russian (PRIMARY):** 10 admissible Russian-language primaries confirmed.
- 7 PMID-bearing via PubMed eutils (LA=rus confirmed): R1 (PMID 26356395), R2 (PMID 18577961), R3 (PMID 18661785), R4 (PMID 19803361), R5 (PMID 20919548), R6 (PMID 19093364), R7 (PMID 15835541).
- 3 CyberLeninka stable-URL items: R8 (Skrebitsky 2016, *Nervnye bolezni*), R9 (Kozlovskaya 2005, *Psikhofarmakologiya i Biologicheskaya Narkologiya*), R10 (Murtalieva 2022, *Uchenye Zapiski Krymskogo Federal'nogo Universiteta*).
- Developer-network authorship flagged on all entries (IMG RAS, Zakusov Institute). Fully independent authorship (R7: MSU physiology faculty) explicitly noted.
- Translation provenance noted on all entries: full texts in Russian; NCBI English abstracts for R1–R7; no published English translation editions.

**Chinese:** 0 admissible primaries located. Explicit statement present. Databases searched: PubMed eutils (chinese[la] + "selank"[tiab]: 0 results), CNKI (indirect Google site-search: 0), Wanfang Data (redirect: 0), Baidu Scholar (塞兰克, TP-7 七肽 中文: 0 peer-reviewed results). Absence characterized as confident and consistent with Selank's Russia-exclusive research ecosystem.

**German:** 0 admissible primaries located. Explicit statement present. PubMed eutils (german[la] + "selank"[tiab]) returned 1 result — PMID 41848778 — retrieved via efetch, verified as *Zeitschrift für Rheumatologie* 2026 article on primary Sjögren's disease with no Selank content; dismissed as false positive, explicitly documented. Springermedizin.de, ZB MED, AWMF, Google Scholar German searches all returned 0 peer-reviewed German-language primaries.

**Analog-evidence-absence stated:** YES — explicitly and repeatedly:
- Opening disambiguation block: "N-Acetyl-Selank-Amidate is a Western grey-market coinage … does NOT appear by that name (or any near-equivalent) in Russian, Chinese, or German scientific literature … zero publications exist in any language on the analog as a distinct chemical entity."
- `## Analog-Specific Literature Survey (All Languages)` section heading: "Result: 0 publications on N-Acetyl-Selank-Amidate as a distinct chemical entity in any language."
- Russian landscape summary: analog-specific search terms («N-ацетил-селанк», «ацетилселанк», «N-acetyl selank») all returned zero results — confirmed.
- Self-check item 7: "N-Acetyl-Selank-Amidate has 0 peer-reviewed primaries in any language. Stated explicitly."
- Bibliography footer: "Admissible primary count: 10 total (Russian: 10; Chinese: 0; German: 0). Analog-specific primaries: 0 in any language."
- Landscape closing statement: "The analog N-Acetyl-Selank-Amidate has zero peer-reviewed primaries in any language — confirmed by exhaustive search."

The analog-absence is the single most prominently stated finding in this layer. It is stated correctly, consistently, and without equivocation.

---

### Gate Summary

| Criterion | Status |
|-----------|--------|
| Both files present | PASS |
| Practitioner: `## Bibliography` present | PASS |
| Practitioner: `## Self-check` present | PASS |
| Practitioner: admissible data sheet OR explicit-absence + vendor-list | PASS (explicit-absence form, 7 vendors named) |
| Practitioner: analog-approved-nowhere + parent-Russia-only + 503A Category 2 TP-7 history | PASS |
| Practitioner: vendor_label vs anecdote_aggregate split | PASS |
| Practitioner: 4 hazards documented upfront | PASS |
| Practitioner: dosing conventions tagged anecdote_aggregate | PASS |
| Practitioner: contiguous integer bib [1]–[9] | PASS |
| Practitioner: 0 off-enum tags | PASS |
| Non-English: `## Bibliography` present | PASS |
| Non-English: `## Self-check` present | PASS |
| Non-English: ≥3 languages surveyed with explicit per-language findings | PASS (Russian, Chinese, German) |
| Non-English: Russian PRIMARY = 10 genuinely Russian-language primaries (7 PMID + 3 CyberLeninka) | PASS |
| Non-English: Chinese 0, explicit | PASS |
| Non-English: German 0, explicit, false positive documented and dismissed | PASS |
| Non-English: analog = 0 primaries in any language, stated explicitly | PASS |
| **Overall gate verdict** | **PASS** |
