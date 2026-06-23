## Verdict

verdict: PASS

```json
{"phase":"8.5","verdict":"PASS","iterations":1,"mode":"deep","practitioner_layer":{"path":"vault/library/peptides/semax/practitioner-layer.md","present":true,"compounding_sheets_count":0,"named_physicians_count":0,"has_bibliography":true,"has_self_check":true},"non_english_layer":{"path":"vault/library/peptides/semax/non-english-layer.md","present":true,"languages_surveyed":["Russian","Other","Chinese","German"],"has_bibliography":true,"has_self_check":true},"halt_reasons":[]}
```

---

## Prose Detail

### Gate 8.5 verification — Semax deep run

**Both files exist and have the required structure:**

- `vault/library/peptides/semax/practitioner-layer.md` — present, 348 lines
- `vault/library/peptides/semax/non-english-layer.md` — present, 508 lines

Each file has its own `## Bibliography` and a self-check section (`## Self-Check` / `## Self-check`). Both gates satisfied.

---

### Practitioner Layer — detailed verification

**Data-sheet finding:** Fully documented. Section "Compounding / Sourcing Data-Sheet" opens with: "Gate finding: NO admissible Western compounding-pharmacy clinical data sheet exists for Semax." The manufactured-Russian-biologic finding is explicit: Semax is a proprietary biologic manufactured by JSC Peptogen under Russian GMP — not a bulk API available for Western 503A compounding. The absence from every major 503A compounder (Empower, Tailor Made, Hallandale, Belmar, Strive) is explicitly named and confirmed.

**Russian registration as equivalent:** Documented in detail. Both registered formulations are covered: 0.1% intranasal (1 mg/mL) for outpatient cerebrovascular indications, ЖНВЛП-listed; 1% intranasal (10 mg/mL) for acute ischemic stroke inpatient. NOT-FDA/EMA/MHRA/TGA/Health Canada is stated explicitly for each authority.

**Vendor landscape documented:** CosmicNootropic, Peptide Sciences, Umbrella Labs — all tagged `anecdote_aggregate`. Limitless Life Nootropics (limitlesslifenootropics.com) — correctly tagged `vendor_label` (whitelisted). No off-whitelist vendor carries `vendor_label`.

**Five hazards — all present:**

1. **Single-lineage / open-label / zero-replication (Hazard 1):** 78–95% of publications carry IMG-RAS / Myasoedov authorship; zero independent non-Russian replication of BDNF-induction mechanism; zero RCTs; zero Western clinical trials. Explicitly stated.

2. **Healthy-adult population mismatch (Hazard 2):** All human efficacy/safety data from elderly Russian stroke/optic neuropathy/cerebrovascular disease patients. Healthy adults 20s–40s are categorically different. The conditional BDNF-induction finding (ischemic tissue > healthy tissue) is specifically cited as a biological challenge to the extrapolation.

3. **NASA near-zero-evidence + N-acetylation-abolishes-copper-chelation-neuroprotection (Hazard 3):** Zero peer-reviewed primary studies for NASA as a distinct compound. The Magrì 2016 finding (PMID 27586814) that N-terminal acetylation abolishes the neuroprotective copper-chelation effect is documented, with mechanistic explanation (CuN₄ → distorted CuN₃O coordination change). Whether this disrupts CNS receptor-binding pharmacology is explicitly flagged as unknown and unstudied.

4. **Grey-market intranasal hazards (Hazard 4):** Supply-chain risks (non-GMP synthesis, residual coupling reagents, no COA verification), route-specific risks (olfactory epithelium / cribriform plate proximity to CNS), and pharmacovigilance vacuum all documented.

5. **WADA S0 — hedged (Hazard 5):** Analysis distinguishes parent Semax (may not fall under S0 given Russian Roszdravnadzor registration — but athletes cannot assume this and must seek ADO ruling) from NASA (almost certainly caught by S0 catch-all as not approved anywhere). WADA PDF not directly retrievable is disclosed. Athletes directed to GlobalDRO.com and their NADO.

**PMIDs eutils-verified:** The self-check section lists 15 PMIDs confirmed via NCBI eutils (esummary.fcgi), with title/author/journal/year match stated for each. The 16th bibliography entry ([3] and [4]) are web references (off-whitelist vendor aggregate and Limitless Life Nootropics product listings), appropriately not assigned PMIDs. All 18 bibliography entries are accounted for. No fabricated cites detected.

**Off-enum tags:** The practitioner layer body uses only canonical tags: `regulatory`, `mechanism_review`, `open_label`, `animal`, `in_vitro`, `vendor_label`, `anecdote_aggregate`. Zero off-enum tags in inline citations or `**Tag:**` entries. The bibliography section uses prose descriptions, not tag fields, so no off-enum risk there.

**named_physicians_count:** 0. Explicitly documented: "No named Western practitioners or clinics prescribing Semax were located." Nine specific sources searched (Seeds Scientific, Holtorf Medical, Edwin Lee MD, Neil Paulvin DO, Tracy Gapin MD, IPS/A4M, peptidedosingprotocols.com, peptideinitiative.com, thepeptidecatalog.com, innerbody.com) — all negative. Absence attributed to lack of lawful Western prescribing framework, not search failure.

**compounding_sheets_count:** 0. No Western 503A data sheet exists. The Russian registration is cited as the regulatory source (author-reported via Deigin 2022, PMID 35456550), not primary GRLS filing, with provenance caveat explicitly stated.

---

### Non-English Layer — detailed verification

**Languages surveyed (4 total; ≥3 gate satisfied):**

- **Russian (PRIMARY):** 86 PubMed-indexed items (semax[tiab] AND russian[la]); 10 admissible primary items selected (R1–R10) covering 1997–2021, spanning foundational synthesis, stroke clinical, ophthalmology, gene expression, peripheral pharmacology, and motor neuron disease. All 10 verified via PubMed eutils efetch (MEDLINE format, LA=rus confirmed). Admissibility boundary applied: English-translation-journal papers (PMID 22803132, 17603664; LA=eng+rus) excluded.

- **Ukrainian (→ "Other"):** 1 admissible primary (PMID 26552305; verified LA=ukr). Shypshyna et al. 2015, Bogomoletz Institute NASU, electrophysiology of Semax on glutamatergic synaptic activity in DRG/DH co-cultures. IMG-RAS co-authorship present (Myasoedov NF) but primary authorship is independent NASU institution.

- **Chinese:** 0 admissible primaries. PubMed eutils (semax AND chinese[la]): 0 results. CNKI, Wanfang, Baidu Scholar, web searches all negative. Absence consistent with Semax's non-entry into Chinese clinical/research market.

- **German:** 0 admissible primaries. PubMed eutils (german[la] + semax[tiab]): 1 result — PMID 6455927 — fetched via efetch and verified as an entirely unrelated 1981 neuromuscular blocking drugs article (*Anaesthesist*); dismissed as false positive with documentation. German academic portals (ZB MED, AWMF, Springermedizin) negative.

**"REINFORCES-not-RESOLVES" conclusion:** Present and prominently stated in two locations — the Russian landscape summary and the honest assessment section. Exact statement: "The non-English (especially Russian) literature is voluminous but REINFORCES rather than resolves the single-lineage and open-label concentration concern." The 86-item Russian corpus is identified as predominantly IMG-RAS/Myasoedov (mechanistic) and Gusev/Skvortsova/Pirogov RNRMU (clinical) — the same inventor-registration network.

**Near-independent primary:** Kurysheva et al. 2001 (R4; PMID 11569188) is explicitly identified as "the most institutionally independent clinical primary in this entire survey" — no IMG-RAS co-authorship. The Kursk State Medical University (Bobyntsev, R9) is identified as "fully independent of IMG-RAS" for peripheral/hepatic effects.

**No placebo-controlled trial in any language:** Stated explicitly in the self-check: "No placebo-controlled trial exists in any language."

**PMIDs verified:** Self-check confirms all 11 items (10 Russian + 1 Ukrainian) verified via PubMed eutils efetch (MEDLINE format). No fabricated cites detected.

---

### Residual finding — bibliography table off-enum (non-English layer)

The bibliography TABLE in the non-English layer (lines 483–485) uses `animal_model` for R7, R8, and R9 — a tag not in the canonical enum (`animal` is the correct form). The in-body `**Tag:**` entries for R7, R8, R9 (lines 248, 282, 314) all correctly use `animal`. The IC-1 inline citation check passes (all inline `[Rn, tag]` references use canonical tags). The IC-2 bibliography entry tag check identifies this residual discrepancy in the display table. This is a documentation-only residual — it does not affect any inline citation grounding or efficacy claim — and does not alter the PASS verdict. It should be corrected by updating the bibliography table cells for R7, R8, R9 from `animal_model` to `animal`.

---

### Summary verdict

**PASS.** Both layer files exist. Both have their own `## Bibliography` and self-check section. The practitioner layer fully documents: no Western 503A data sheet; manufactured Russian biologic (JSC Peptogen); Russian registration (0.1%/1% intranasal, ЖНВЛП-listed) as the regulatory equivalent; NOT FDA/EMA; all 5 hazards (single-lineage, healthy-adult population mismatch, NASA near-zero-evidence + N-acetylation-abolishes-copper-chelation-neuroprotection, grey-market intranasal, WADA-S0-hedged); 0 named Western practitioners; 0 Western compounding sheets; only Limitless Life Nootropics carrying `vendor_label` (all other vendors `anecdote_aggregate`). The non-English layer surveys 4 languages (Russian 10 items + Ukrainian 1 + Chinese 0 + German 0); satisfies ≥3 language gate; states the honest "REINFORCES-not-RESOLVES" conclusion for the single-lineage concern; confirms no placebo-controlled trial in any language; all 11 PMIDs eutils-verified. One residual: bibliography table uses `animal_model` (not `animal`) for R7, R8, R9 in the non-English layer display table — in-body tags are correct; should be corrected but does not halt ingestion.
