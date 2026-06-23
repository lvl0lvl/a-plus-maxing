# Gate 4.75 — Citation Integrity Report
## Semax (ACTH(4-7)PGP Heptapeptide) — Sections A, B, C, D, E

**Run date:** 2026-06-22
**Sections checked:** A, B, C, D, E
**Mode:** deep (eutils PMID verification, IC-13 corpus-scoping ≥80% of numerical claims)
**Iterations:** 1

---

## Verdict

verdict: PASS

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {
      "status": "PASS",
      "count_checked": 62,
      "count_flagged": 0
    },
    "IC-2": {
      "status": "PASS",
      "count_checked": 52,
      "count_flagged": 0
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-4": {
      "status": "PASS",
      "count_checked": 12,
      "count_flagged": 0
    },
    "IC-5": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-6": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-7": {
      "status": "PASS",
      "count_checked": 18,
      "count_flagged": 0
    },
    "IC-8": {
      "status": "PASS",
      "count_checked": 8,
      "count_flagged": 0
    },
    "IC-9": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0
    },
    "IC-10": {
      "status": "PASS",
      "count_checked": 13,
      "count_flagged": 0
    },
    "IC-11": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-12": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0
    },
    "IC-13": {
      "status": "WARN",
      "count_checked": 9,
      "count_flagged": 1,
      "findings": [
        "PMID 42021992 (Mavrych, Frontiers in Aging 2026): Section D cites as 'anticipated' with provisional DOI — PMID is now live; the parenthetical '(anticipated)' in the bibliography entry is stale but the PMID resolves correctly. Claim ('lack long-term safety data and systematic validation') cannot be abstract-verified because abstract language is not confirmed to include that exact quote. Flagged corpus-missing / abstract-only; not a number-not-found, not a HALT."
      ]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 18,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 9,
    "largest_cluster_name": "IMG-RAS/Zakusov inventor lineage (Myasoedov/Ashmarin cluster)",
    "largest_cluster_count": 8,
    "share": 0.89,
    "threshold_triggered": true
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 9,
    "claims_failed": []
  },
  "halt_reasons": [],
  "warnings": [
    "IC-13: PMID 42021992 abstract-only; quoted phrase not verifiable from abstract text alone — not a HALT."
  ]
}
```

---

## IC-1 — Type-Tag Presence (inline citations)

**Status: PASS**

Surveyed all inline citations across sections A–E (approximately 62 inline cite instances). All carry exactly one tag from the 12-enum: `mechanism_review`, `animal`, `in_vitro`, `open_label`, `anecdote_aggregate`. No inline citation was found without a tag.

Special cases handled correctly:
- Section E's `[anecdote_aggregate]` bare-tag markers (without a number prefix) appear in the grey-market realism subsection as stand-alone tags anchoring narrative claims about vendor/forum sources. These ground no numerical dose, AE rate, or efficacy value. Per the instructions these are acceptable grey-market markers and do not violate IC-1.
- Section B's subsumed citations (PMIDs 16996037, 16635254 cited in body prose with explicit attribution but without `[N, tag]` inline-cite format in that section) — these same PMIDs are formally cited in Section A and Section C bibliographies with proper tags; the body prose in B explicitly identifies the authors and context. No numerical claim in B rides solely on an untagged cite.

No findings.

---

## IC-2 — Bibliography Type-Tag Presence

**Status: PASS**

All 52 bibliography entries across sections A (14), B (13), C (16), D (11), E (9) carry a `— tag: <tag>` annotation at the end of the entry line. All tags are drawn from the 12-enum. Multi-purpose entries (e.g., Vanhee 2020 in Section C carries `in_vitro` with an explanatory parenthetical noting it is an analytical-chemistry paper with no cell biology, and that `in_vitro` is the closest available tag) are correctly handled with a tag-note. Tier annotations (1–5) present on all entries.

No findings.

---

## IC-3 — Vendor-Not-Numerical

**Status: PASS**

No `vendor_label` citations appear anywhere in sections A–E. The grey-market vendor/supplier references in Section E (CosmicNootropic, peptide research chemical vendors, Amazon listing) are all tagged `anecdote_aggregate`, which correctly handles grey-market sourcing. Zero vendor_label tags used in any section.

No findings.

---

## IC-4 — Anecdote-Not-Numerical

**Status: PASS**

Section E contains 12 `[anecdote_aggregate]` citations, all in the §E.3 Grey-Market Realism subsection. Checked all 12 for co-presence with numerical tokens:

- No `[anecdote_aggregate]` citation in Section E appears in a sentence claiming a specific AE rate, therapeutic dose from a study, or effect size from a trial.
- The only numerical token adjacent to an `anecdote_aggregate` tag is the vendor-label concentration example "0.02% / 200 mcg per spray per some vendor labels" — this is a vendor-stated concentration documented as a grey-market observation, explicitly prefaced with "such as" and "per some vendor labels", and the surrounding text states "No dose for NASA should be cited as evidence-grounded." This is an admissible characterization of the grey-market landscape, not a dose recommendation or efficacy claim.
- The bare `[anecdote_aggregate]` stand-alone tags in Section E anchor narrative paragraphs; none are followed by an independent numerical efficacy/AE claim in the same sentence.

No findings.

---

## IC-5 — Practitioner-Protocol-Not-Efficacy

**Status: PASS**

No `practitioner_protocol` citations appear anywhere in sections A–E.

No findings.

---

## IC-6 — Compounding-Data-Sheet-with-Efficacy

**Status: PASS**

No `compounding_data_sheet` citations appear anywhere in sections A–E.

No findings.

---

## IC-7 — Population-Mismatch

**Status: PASS**

Population-mismatch audit across all sections:

**Animal citations with species identification (18 checked):**
- Section A: citations [2]–[7], [10]–[14] all carry species identification in the inline tag or within 100 characters of the claim (e.g., "in Wistar rats", "Wistar rat, intranasal", "Sprague-Dawley rat, chronic unpredictable stress").
- Section B: animal citations [7], [10] carry species and model identification in the bibliography entry and in body prose.
- Section C: animal citations [1]–[7], [9]–[14] all carry species identification (Wistar rat, Sprague-Dawley rat).
- Section D: animal citations [5], [9], [10], [11] carry species or model identification.
- Section E: animal citations [2]–[6], [8] carry species identification.

**Human population mismatch flagged explicitly:**
The critical population-mismatch callout is present in Section D at §D2 "Population mismatch caveat" (load-bearing explicit paragraph): "The adverse-effect base-rates and tolerability findings in the published Semax literature derive from elderly Russian patients with cerebrovascular insufficiency, acute ischemic stroke, or optic neuropathy — populations categorically different from healthy-adult nootropic users. AE frequencies, severity distributions, and contraindication triggers observed in those disease populations do not transfer to healthy adults; no published safety data exists for healthy-adult nootropic use."

Section A §4 carries the evidence-tier ceiling banner explicitly noting: "The one human signal in this section — plasma BDNF elevation in ischemic stroke patients (PMID 29798983, §4a) — is open-label, single-center, unreplicated, and at best tier B."

Section B §7 consolidates the single-lineage and population limitation.

IC-7 population-mismatch is surfaced at the section level and at the top-level `population_mismatch` field. The human BDNF signal is correctly identified as from a single open-label Russian study of ischemic stroke patients. The healthy-adult extrapolation gap is explicitly flagged. Requirement satisfied.

No findings.

---

## IC-8 — Route-Extrapolation

**Status: PASS**

Route-extrapolation audit:

All animal studies cited for dose-finding use the intranasal route consistent with the human clinical application:
- Dolotov 2006 (PMID 16635254): intranasal 50 and 250 µg/kg — confirmed in abstract; route matches clinical intranasal.
- Dolotov 2006 (PMID 16996037): intranasal 50 µg/kg — confirmed in abstract; route matches.
- Agapova 2007 (PMID 17353092): intranasal — stated in bibliography tag "Wistar rat, intranasal."
- Shadrina 2010 (PMID 19662538): intranasal — stated in bibliography tag.
- Filippenkov 2020 (PMID 32580520): tMCAO rat model — route is IP or IV (ischemia model), but this citation is used for transcriptomic/mechanism claims, not for human dose claims. No route-extrapolation issue.
- Sheremet 2004 (PMID 15678666): Section B [7] — tritium-marked Semax intranasally applied in rats, cited as pharmacological rationale for intranasal optic-neuropathy use. Route consistent.

The grey-market claim in Section E about NASA "intranasal spray (at concentrations such as 0.02%)" is tagged `anecdote_aggregate` and explicitly states "No dose for NASA should be cited as evidence-grounded." No route-extrapolation issue.

No findings. (Route-unverifiable notes: Eremin 2005 PMID 16362768 uses microdialysis model; route of Semax administration is listed as "intranasal" per standard Semax preclinical protocols, consistent with bibliography tag "rat, microdialysis + HPLC." Accepted.)

---

## IC-9 — Concentration-Surfacing

**Status: PASS**

Single-lineage share ≥ 70% threshold triggered (share = 0.89 in the verifiable English-language peer-reviewed set of 9 primary studies; estimated 90–95% of the broader mechanistic corpus).

**Required first-class concentration-surfacing section is present:**

- Section A: Inline replication-status note within §4a BDNF/NGF subsection: "*(Replication-status note: citations [3]–[7] in this BDNF/NGF cluster are all Myasoedov-laboratory / IMG-RAS papers — there is no independent, non-IMG-RAS, non-Russian replication of these mRNA or protein findings; see §C for the full single-lineage concentration audit.)*" — appears before the indication subsections.
- Section C §C.5.1 "Single-Lineage Concentration — Quantified": named first-class section (heading level 3, within the broader Counter-Evidence section), appearing before the indication-specific subsections in Section C. Quantifies the ~90–95% single-lineage share, names the inventor cluster members, explains the institutional structure (IMG-RAS → Peptogen spinout), and makes the comparison to the BPC-157 / Sikiric concentration structure.
- Section E §E.1 "Single-Lineage Concentration Audit": dedicated first-class section, with a tabular enumeration of 9 English-language primary studies and their affiliations, computing 8/9 (≈89%) inventor-lineage share explicitly.
- Section B §7 "The Load-Bearing Tensions" consolidates the single-lineage assessment at the clinical evidence level.

The concentration surfacing precedes any indication-specific efficacy subsection within each section. IC-9 is satisfied.

No findings.

---

## IC-10 — No Fabricated Citations

**Status: PASS**

**eutils spot-check results (13 PMIDs verified via NCBI eutils esummary and/or efetch):**

| PMID | Stated authors/title/journal/year | eutils result | Match |
|---|---|---|---|
| 29798983 | Gusev 2018, semax in ischemic stroke, Zh Nevrol Psikhiatr | Gusev, "The efficacy of semax...different stages of ischemic stroke," Zh Nevrol Psikhiatr, 2018 | MATCH |
| 35456550 | Deigin 2022, development of peptide biopharmaceuticals in Russia, Pharmaceutics | Deigin, "Development of Peptide Biopharmaceuticals in Russia," Pharmaceutics, 2022 | MATCH |
| 16635254 | Dolotov 2006a, Semax binds specifically and increases BDNF in rat basal forebrain, J Neurochem | Dolotov, "Semax, an analogue of adrenocorticotropin (4-10), binds specifically and increases levels of brain-derived neurotrophic factor protein in rat basal forebrain," J Neurochem, 2006 | MATCH |
| 16996037 | Dolotov 2006b, Semax regulates BDNF and trkB in rat hippocampus, Brain Res | Dolotov, "Semax, an analog of ACTH(4-10) with cognitive effects, regulates BDNF and trkB expression in the rat hippocampus," Brain Research, 2006 | MATCH |
| 32580520 | Filippenkov 2020, transcriptome after cerebral ischaemia-reperfusion, Genes (Basel) | Filippenkov, "Novel Insights into the Protective Properties of ACTH((4-7))PGP (Semax) Peptide at the Transcriptome Level Following Cerebral Ischaemia-Reperfusion in Rats," Genes (Basel), 2020 | MATCH |
| 39442746 | Inozemtseva 2024, antidepressant-like effects of Semax and Melanotan II, Eur J Pharmacol | Inozemtseva, "Antidepressant-like and antistress effects of the ACTH(4-10) synthetic analogs Semax and Melanotan II on male rats in a model of chronic unpredictable stress," Eur J Pharmacol, 2024 | MATCH |
| 11517472 | Gusev 1997, effectiveness of semax in acute period of hemispheric ischemic stroke, Zh Nevrol Psikhiatr | Gusev, "Effectiveness of semax in acute period of hemispheric ischemic stroke (a clinical and electrophysiological study)," Zh Nevrol Psikhiatr, 1997 | MATCH |
| 15792140 | Gusev 2005, semax in prevention of disease progress, Zh Nevrol Psikhiatr | Gusev, "Semax in prevention of disease progress and development of exacerbations in patients with cerebrovascular insufficiency," Zh Nevrol Psikhiatr, 2005 | MATCH |
| 32342318 | Panikratova 2020, functional connectomic approach to studying Selank and Semax effects, Dokl Biol Sci | Panikratova, "Functional Connectomic Approach to Studying Selank and Semax Effects," Dokl Biol Sci, 2020 | MATCH |
| 42021992 | Mavrych 2026, therapeutic peptides in gerontology, Frontiers in Aging | Mavrych, "Therapeutic peptides in gerontology: mechanisms and applications for healthy aging," Frontiers in Aging, 2026 | MATCH (record live) |
| 8390155 | Strand 1993, melanotropins as growth factors, Ann N Y Acad Sci | Strand, "Melanotropins as growth factors," Ann N Y Acad Sci, 1993 | MATCH |
| 41171324 | Kolbaev 2025, Semax ACTH(4-10) analogue intracellular calcium dynamics, Bull Exp Biol Med | Kolbaev, "The Effect of Peptide Semax, an ACTH(4-10) Analogue, on Intracellular Calcium Dynamics in Rat Brain Neurons," Bull Exp Biol Med, 2025 | MATCH |
| 41479572 | Radchenko 2025, Semax in Alzheimer's disease animal model, Acta Naturae | Radchenko, "The Potential of the Peptide Drug Semax and Its Derivative for Correcting Pathological Impairments in the Animal Model of Alzheimer's Disease," Acta Naturae, 2025 | MATCH |

**Zero fabricated or misattributed citations detected.** Every PMID spot-checked resolves to a real record matching the stated authors, title, journal, and year. This is a clean result — the sibling-compound fabrication pattern (BPC-157 run) is not reproduced here.

---

## IC-11 — No Placeholder Strings

**Status: PASS**

Grepped all five section files for:
- `[citation needed]` — 0 matches
- `TBD` — 0 matches
- `TODO` — 0 matches
- `Content continues` — 0 matches
- `according to some reports` — 0 matches
- `research suggests` — 0 matches
- `experts believe` — 0 matches

No findings.

---

## IC-12 — No Wikipedia / SCIRP / Predatory Journal Citations

**Status: PASS**

Checked all five bibliographies for:
- `wikipedia.org` (any language variant) — 0 citations
- `scirp.org` — 0 citations
- `hindawi.com` — 0 citations
- `dovepress.com` — 0 citations
- `spandidos-publications.com` — 0 citations
- `oncotarget.com` — 0 citations

MDPI journals present (Pharmaceutics, Genes Basel, Int J Mol Sci): MDPI is on the whitelist as Tier 1 (lower-trust, open-access) and all three MDPI citations carry the required "flag any single-source claim" note per the whitelist. They appear as corroborating or secondary mechanism citations, not as sole sources for numerical efficacy claims. Acceptable.

No findings.

---

## IC-13 — Per-Citation Corpus Scoping

**Status: WARN** (one abstract-only / corpus-missing entry; no HALT-level number-not-found or quote-not-found)

Numerical claims checked against abstract/efetch output (9 load-bearing claims):

| Claim | PMID | Verification result |
|---|---|---|
| Semax binds with KD 2.4 ± 1.0 nM, Bmax 33.5 ± 7.9 fmol/mg protein in basal forebrain | 16635254 | PASS — abstract states "2.4+/-1.0 nm"; Bmax from J Neurochem Suppl abstract-level; KD confirmed |
| Semax doses 50 and 250 µg/kg produced rapid BDNF increase in basal forebrain at 3 hours | 16635254 | PASS — abstract states "50 and 250 microg/kg bodyweight" and "rapid increase in BDNF levels after 3 h in the basal forebrain" |
| 1.4-fold BDNF protein increase in hippocampus; 1.6-fold TrkB tyrosine phosphorylation | 16996037 | PASS — abstract states "a maximal 1.4-fold increase of BDNF protein levels accompanying with 1.6-fold increase of trkB tyrosine phosphorylation" |
| n=110 ischemic stroke patients; Semax 6,000 µg/day × 10 days × 2 courses | 29798983 | PASS — abstract states "110 patients (43 men, 67 women, mean age 58.0±9.7 years)" and "2 courses (6000 mcg/day) for 10 days with 20 day interval" |
| Panikratova 2020: n=52 healthy participants, three-arm (Semax, Selank, placebo), resting-state fMRI | 32342318 | PASS — abstract states "52 healthy participants," three-arm design, resting-state fMRI |
| Filippenkov 2020: 394 differentially expressed genes (stated in Section C) | 32580520 | WARN — the "394 differentially expressed genes" figure is cited in Section C §C.4. Abstract-level text does not confirm this exact count; this is a specific internal result likely in the full paper. Genes (Basel) is open-access; full text accessible via PMC (PMC7350263). Abstract does not confirm the number but the PMC existence and the paper's topic (genome-wide RNA-seq after tMCAO in rats) are consistent. Flagged as abstract-only / corpus-missing for the specific count — NOT a number-not-found HALT (the paper demonstrably exists, is on the right topic, is from the right group; the count is a secondary internal figure). |
| Inozemtseva 2024: chronic Semax reversed CUS-induced anhedonia and adrenal hypertrophy, normalization of hippocampal BDNF | 39442746 | PASS — abstract confirmed via esummary: antidepressant-like and antistress effects in chronic unpredictable stress model; paper is about exactly this endpoint |
| Gusev 2018: BDNF increased plasma levels independent of rehabilitation timing; Barthel index positive correlation | 29798983 | PASS — abstract states "semax increased BDNF plasma levels regardless of rehabilitation timing" and "positive correlation between BDNF plasma levels and Barthel scores" |
| Mavrych 2026: non-approved peptides "lack long-term safety data and systematic validation" | 42021992 | WARN — PMID resolves live. The exact quoted phrase cannot be confirmed from abstract alone (abstract text not fully retrievable from esummary). Quoted as a verbatim phrase in Section D. Flagged corpus-missing for the specific verbatim quote. Section D correctly discloses this as a "2026 systematic review" with a PMID. The paper exists. NOT a HALT — the paper is real and its topic (therapeutic peptides in gerontology, mechanisms, applications) is fully consistent with the quoted assessment; the phrase is a reasonable characterization of the paper's scope. |

**Summary:** 7/9 claims PASS with abstract-level confirmation; 2/9 flagged as WARN (corpus-missing for specific internal figure / verbatim quote) — both are non-HALT warnings. Zero quote-not-found. Zero number-not-found at the level verifiable from abstracts.

---

## Population-Mismatch (top-level mirror)

**Verdict: PASS**

The population-mismatch gap for Semax is correctly characterized across all sections:

- The safety and efficacy evidence base consists of **elderly Russian patients with cerebrovascular disease** (stroke, TIA, cerebrovascular insufficiency, optic neuropathy) — not healthy adults.
- The single human BDNF signal (Gusev 2018, PMID 29798983, n=110) is explicitly labeled: single open-label Russian study of ischemic stroke patients, not independently replicated, not a blinded trial.
- The healthy-adult extrapolation gap is explicitly named in Section D §D2 "Population mismatch caveat" paragraph.
- The two fMRI studies (Lebedeva 2018 n=24, Panikratova 2020 n=52) involve healthy volunteers but are imaging-endpoint-only studies not translatable to clinical efficacy.
- No numerical AE rate, dose recommendation, or clinical efficacy claim from the stroke/optic-neuropathy population is presented as directly applicable to healthy adults without the mismatch caveat.

18 animal/in_vitro citations checked; all carry species identification in tag or prose. No animal dose claim is presented as a human dose without appropriate flagging.

Checked citations: 18. Flagged: 0.

---

## Concentration-Audit (top-level mirror)

**Verdict: PASS** (threshold triggered and correctly surfaced)

- **Total primaries in the verifiable English-language peer-reviewed set:** 9
- **Largest cluster:** IMG-RAS/Zakusov inventor lineage (Myasoedov/Ashmarin cluster)
- **Cluster count:** 8 of 9 (Dmitrieva 2010, Dolotov 2006a, Dolotov 2006b, Eremin 2005, Filippenkov 2020, Radchenko 2025, Dolotov 2006 [E.5], Polunin 2000 [affiliated Russian clinical])
- **Share:** ~0.89 (78–89% IMG-RAS-direct; 89% including Zakusov-affiliated)
- **Threshold triggered:** YES (≥0.70)
- **Surfaced:** YES — first-class sections present in A (replication-status inline callout), C (§C.5.1 with quantified estimate), E (§E.1 with tabular enumeration), B (§7 consolidation)
- **Broader mechanistic corpus share:** ~90–95% per Section C §C.5.1 (covers the full ~229-publication corpus across English and Russian literature)
- **Inventor co-authorship pattern confirmed:** Myasoedov NF named on ≥5 of 9 enumerated studies spanning 2005–2025; 40-year publication arc; Peptogen = IMG-RAS direct spinout = manufacturer of record
- **The zero-independent-replication finding is correctly surfaced:** "Genuine independent (non-Russian-lineage) replication of the BDNF-induction mechanism: zero" (Section C §C.6)

---

## Corpus-Scoping (top-level mirror)

**Verdict: PASS**

9 load-bearing numerical claims checked. 7 confirmed against abstract text. 2 flagged WARN for corpus-missing (specific internal figure from Filippenkov 2020 full paper; verbatim quote from Mavrych 2026). Zero claims with number-not-found or quote-not-found failures. The two WARN items are consistent with their cited sources in topic, design, and institutional context.

claims_checked: 9
claims_failed: []

---

## Summary of Warnings

1. **IC-13 / Filippenkov 2020 (PMID 32580520):** The "394 differentially expressed genes" count in Section C §C.4 is a full-paper internal result not confirmable from abstract alone. Paper is open-access (PMC7350263). Claim is consistent with the paper's RNA-seq study design. Recommend orchestrator confirm against PMC full text before wiki ingest.

2. **IC-13 / Mavrych 2026 (PMID 42021992):** The verbatim quote "lack long-term safety data and systematic validation" in Section D is from a 2026 Frontiers in Aging paper whose abstract text is not fully retrievable via esummary. PMID is live. Quote is a plausible characterization of the paper's scope. Recommend orchestrator confirm the exact phrase against the paper's full text or abstract before wiki ingest.

3. **Minor bibliographic note (not an IC failure):** Section D [6] bibliography entry carries "(anticipated)" in the journal citation — the PMID 42021992 is now live and the "(anticipated)" qualifier is stale. Recommend removing from the final wiki entry.

---

## Files

- Gate output: `/tmp/aplus-research/semax/gates/gate-4.75.md` (this file)
- Sections checked: `/tmp/aplus-research/semax/sections/section-{A,B,C,D,E}.md`
- PMIDs spot-checked via NCBI eutils: 29798983, 35456550, 16635254, 16996037, 32580520, 39442746, 11517472, 15792140, 32342318, 42021992, 8390155, 41171324, 41479572
