---
title: Health Research Source Whitelist
type: reference
permalink: a-plus-maxing/library/source-whitelist
status: active
created: 2026-05-23
last_reviewed: 2026-05-23
review_cadence: phase (or on first wrong-source incident)
---

# Health Research Source Whitelist

Closed list of acceptable sources for any health-domain research — peptides, supplements, hormones, training literature, sleep, lymphatic, GI, lab interpretation. Modeled on Quant's `references/source-hierarchy.md` + `tier-2-5-host-whitelist.txt`.

Used by:
- Any specialist agent dispatching research (peptide-specialist, endocrine-specialist, gi-specialist, labs-specialist, etc.)
- Manual `deep-research` dispatches (pasted into prompt)
- `aplus-research` skill once built (loaded at Phase 1 scope, enforced at Phase 4.75)

Domain-specific whitelist subsets (e.g., compounding pharmacies for peptides only, manual-therapy bodies for lymphatic only) extend this base list — they don't replace it. Place those in `vault/library/<domain>/_source-whitelist-extension.md`.

If a research dispatch surfaces a source NOT in this list, the source is admissible only as `anecdote_aggregate` (qualitative leads, never numerical claims). Add a host to the whitelist only after manual review.

---

## Type-tag enum

Every source in a research report carries exactly one tag from this set:

| Tag | Meaning | May cite for |
|---|---|---|
| `rct` | Randomized controlled trial in humans | dose, effect size, n, AE rate, mechanism |
| `meta_analysis` | Systematic review or meta-analysis of human RCTs | pooled effect size, heterogeneity, all of the above |
| `cohort` | Prospective or retrospective human cohort | association strength, AE patterns |
| `open_label` | Human open-label / case series | dose ranges, qualitative effects, AE patterns |
| `animal` | Rodent / non-human primate / other animal | mechanism, dose-finding (extrapolation flagged) |
| `in_vitro` | Cell culture / biochemical | mechanism only |
| `mechanism_review` | Narrative or systematic review of pathway/mechanism | mechanism, receptor pharmacology |
| `regulatory` | FDA / EMA / TGA / Health Canada filing or guidance | regulated status, approved indication, approved dose, label AEs |
| `compounding_data_sheet` | Compounding pharmacy clinical data sheet with cited primaries | available dose forms, reconstitution, admin protocol (claims must cite their primaries to be admissible) |
| `vendor_label` | Research-chemical vendor product page or COA | purity claim, reconstitution math only — NEVER efficacy |
| `practitioner_protocol` | Prescriber reference text, conference handout, named-physician stated protocol | prescribing-practice dose / cycle / route conventions — NOT efficacy |
| `anecdote_aggregate` | Reddit / forum / podcast / blog without cited primaries | qualitative leads ONLY, never numerical |

---

## Tier 1 — Primary literature

Always admissible. Cite as `rct`, `meta_analysis`, `cohort`, `open_label`, `animal`, `in_vitro`, or `mechanism_review` per study design.

- `pubmed.ncbi.nlm.nih.gov`
- `ncbi.nlm.nih.gov` (PMC full-text)
- `clinicaltrials.gov`
- `cochranelibrary.com`
- `bmj.com`
- `thelancet.com`
- `nejm.org`
- `jamanetwork.com`
- `nature.com`
- `cell.com`
- `science.org`
- `sciencedirect.com`
- `springer.com`
- `wiley.com` (Wiley Online Library)
- `oup.com` (Oxford Academic)
- `diabetesjournals.org` (American Diabetes Association journals — Diabetes, Diabetes Care; added 2026-06-19 wiki-research)
- `journals.plos.org` / `plos.org` (Public Library of Science — PLoS ONE, PLoS Medicine; added 2026-06-19 wiki-research)
- `jci.org` (Journal of Clinical Investigation + JCI Insight; added 2026-06-19 wiki-research)
- `portlandpress.com` (Portland Press — Bioscience Reports, Biochemical Journal; added 2026-06-19 wiki-research)
- `karger.com`
- `frontiersin.org` (lower trust — open-access; flag any single-source claim)
- `mdpi.com` (lower trust — open-access; flag any single-source claim)
- `liebertpub.com` (Mary Ann Liebert — *Thyroid* (official ATA journal) + other peer-reviewed titles; added 2026-06-19 wiki-research, thyroid cluster)
- `tandfonline.com` (Taylor & Francis — peer-reviewed journals incl. Annals of Clinical Biochemistry, Critical Reviews in Clin Lab Sciences; added 2026-06-19 wiki-research)
- `degruyter.com` (De Gruyter — peer-reviewed journals incl. Clinical Chemistry and Laboratory Medicine (CCLM); added 2026-06-19 wiki-research)
- `biorxiv.org` (preprint — admissible but flag as `not-peer-reviewed`)
- `medrxiv.org` (preprint — same)

## Tier 2 — Regulatory / institutional

Always admissible. Cite as `regulatory`.

- `fda.gov`
- `ema.europa.eu`
- `tga.gov.au`
- `canada.ca/en/health-canada` (Health Canada)
- `thyroid.org` (American Thyroid Association — clinical guidelines; added 2026-06-19 wiki-research)
- `endocrine.org` (Endocrine Society — clinical practice guidelines; added 2026-06-19 wiki-research)
- `nih.gov` (broader NIH content beyond PubMed)
- `who.int`
- `cdc.gov`
- `dailymed.nlm.nih.gov` (FDA labels)
- `accessdata.fda.gov` (FDA approval letters, label PDFs)
- `ngsp.org` (National Glycohemoglobin Standardization Program — the DCCT-anchored US HbA1c standardization body: certified-method registry + the NGSP↔IFCC master equation; added 2026-06-19 wiki-research, HbA1c entry)
- `ifcc.org` (International Federation of Clinical Chemistry and Laboratory Medicine — SI-traceable reference measurement systems / calibration; added 2026-06-19 wiki-research)

## Tier 2.5 — Curated practitioner with cited primaries

Admissible IF the specific page cites primaries. Cite as the underlying primary's type, with the practitioner page in `notes` as the discovery source. NEVER cite the practitioner page as the primary.

- `examine.com` (citations are usually solid; verify each)
- `peterattiamd.com` (verify primary cites)
- `hubermanlab.com` (verify primary cites — episode show notes can be wrong)
- `rhonda-patrick.com` / `foundmyfitness.com` (verify primary cites)

## Tier 3 — Compounding pharmacies (clinical data sheets only)

Admissible as `compounding_data_sheet` for dose forms, reconstitution, admin protocol. NEVER for efficacy unless the data sheet cites its own primaries (then cite those primaries directly).

- `empowerpharmacy.com`
- `tailormadecompounding.com`
- `hallandalerx.com`
- `belmarpharmasolutions.com`
- `apsmeds.com`
- `strivepharmacy.com`

## Tier 4 — Research-chemical vendors

Admissible as `vendor_label` for purity COAs and reconstitution math ONLY. NEVER for efficacy. Always flag the source as gray-market.

- `peptidesciences.com`
- `corepeptides.com`
- `swisschems.is`
- `limitlesslifenootropics.com`
- `simplenutritionllc.com` (sometimes)

> If a peptide ONLY has vendor-label sourcing and no Tier 1/2 evidence, the compound page is auto-flagged `evidence_tier: D` and `status: excluded` pending primary literature.

## Tier 5 — Anecdote aggregates (qualitative leads only)

Admissible as `anecdote_aggregate` for surfacing AE patterns or dose ranges to investigate. NEVER as the basis for a recommendation.

- `reddit.com/r/Peptides`
- `reddit.com/r/PeptideResearch`
- `reddit.com/r/Nootropics`
- `reddit.com/r/Testosterone`
- `forums.peptidesum.com`
- `meso-rx.com` (forums)
- `excelmale.com` (forums)
- Podcast transcripts (cite episode + timestamp; downgrade to anecdote unless the speaker is the primary investigator of the cited study)

## Tier 2.7 — Practitioner protocols (prescribing-practice claims only)

Admissible as `practitioner_protocol` for documenting how licensed prescribers ACTUALLY DOSE / CYCLE / ROUTE a compound. Distinct from efficacy: practitioner protocols may NOT ground efficacy claims (only Tier 1/2 can).

Use case: every compound entry's "Prescribing-Practice Layer" section is populated from this tier, alongside Tier 3 compounding pharmacy data sheets.

- `seedsscientific.com` (Seeds Peptide Protocols — peptide-prescriber reference)
- `peptidesociety.org` / `internationalpeptidesociety.com` (IPS)
- `a4m.com` (American Academy of Anti-Aging Medicine — CME materials, conference handouts)
- `ifm.org` (Institute for Functional Medicine — peptide modules)
- `aaopm.com` (American Academy of Ozone & Peptide Medicine)
- `clinicalpeptidesociety.org`
- Named-physician published protocols where the physician is a known prescriber, the protocol is explicitly stated, and the venue is citable (book, lecture handout, podcast with timestamp, conference proceedings)
  - e.g., Edwin Lee, Kent Holtorf, William Seeds, Neil Paulvin, Tracy Gapin
- Conference proceedings: IHS (Integrative Healthcare Symposium), A4M World Congress, etc.

**Admissibility rules:**
- `practitioner_protocol` cite can support: dose range, route, cycle length, admin protocol, indication selection
- `practitioner_protocol` cite CANNOT support: efficacy claims, AE rates, mechanism — those require Tier 1/2
- Every `practitioner_protocol` cite must include practitioner name, venue (book/lecture/handout/podcast), date
- If a Tier 1/2 source contradicts a `practitioner_protocol` source on dose, flag in `meta/contradictions.md` and let the academic evidence win for the report's primary dose recommendation; report both

## Tier NE — Non-English literature

Non-English peer-reviewed literature is admissible under the SAME tier rules as English (i.e., a Russian peer-reviewed paper from a Tier-1-equivalent journal is admissible as `animal`, `rct`, etc.). Each compound entry's "Non-English Literature Coverage" section documents what was surveyed.

### Russian / Soviet / Post-Soviet

Especially relevant for: Selank, Semax, Cerebrolysin, Dihexa precursors, peptide bioregulators (Khavinson group: Epitalon, Vilon, Thymalin, Cortexin), many GH secretagogue derivatives, Soviet-era peptide therapeutics.

- Journals (variable English-abstract coverage; full text often Russian-only):
  - Eksperimental'naya i Klinicheskaya Farmakologiya (Experimental and Clinical Pharmacology)
  - Biulleten' Eksperimental'noi Biologii i Meditsiny (Bulletin of Experimental Biology and Medicine — Springer-translated)
  - Vestnik Rossiiskoi Akademii Meditsinskikh Nauk (Vestnik RAMN)
  - Zhurnal Nevrologii i Psikhiatrii im. S.S. Korsakova (Korsakov Journal of Neurology and Psychiatry)
  - Voprosy Biologicheskoi, Meditsinskoi i Farmatsevticheskoi Khimii
  - Doklady Akademii Nauk (Doklady Biological Sciences — Springer-translated)
  - Uspekhi Gerontologii (Advances in Gerontology — Khavinson's journal; Springer-translated)
- Institutes (whose research may be cited by name in any source):
  - Institute of Molecular Genetics RAS (Moscow) — Selank, Semax
  - Severtsov Institute of Ecology and Evolution
  - Engelhardt Institute of Molecular Biology RAS
  - St. Petersburg Institute of Bioregulation and Gerontology (Khavinson)
  - V.V. Zakusov Institute of Pharmacology
  - Serbsky Federal Medical Research Center (psychiatric peptide work)
- Databases:
  - eLibrary.ru (Russian Science Citation Index)
  - CyberLeninka (Russian open-access)
  - Russian patent database (FIPS / Rospatent)

### Chinese

Especially relevant for: replication work on Western-developed peptides, traditional Chinese medicine peptide derivatives, the People's Liberation Army medical research apparatus.

- Journals:
  - Chinese Medical Journal
  - Journal of Traditional Chinese Medicine
  - World Journal of Gastroenterology (English, but many Chinese authors — already in Tier 1)
  - Acta Pharmacologica Sinica
  - Drug Design Development and Therapy (English, many Chinese authors)
- Databases:
  - CNKI (China National Knowledge Infrastructure)
  - Wanfang Data
  - VIP Database

### Croatian / Eastern European

Especially relevant for: BPC-157 (Pliva-era documents), other Eastern European pharmaceutical programs.

- Lijecnicki Vjesnik (Croatian Medical Journal — secondary)
- Croatian Medical Journal (English, Tier 1-equivalent)
- Acta Pharmaceutica (Croatian Pharmaceutical Society — Sciendo, mostly English)

### Japanese / Korean / German / French

Surveyed on a per-compound basis when literature suggests originator-country relevance. Default: not surveyed unless specific reason.

### Translation handling

- Full text available with abstract in English: cite as if English (note language in citation).
- Abstract only in English, full text in source language: cite the abstract for high-level claim; do NOT cite specific numerical claims unless the abstract states them explicitly.
- Source-language only with no English abstract: flag as `non-english-untranslated`; note title (transliterated), authors, journal, year, DOI; cite the bibliographic reference but not the content; recommend follow-up translation if material.
- Translation tools (Google Translate, DeepL) acceptable for general comprehension but every numerical claim from a machine-translated source must carry inline `[translated:<tool>]` tag and any specific dose, n, or effect-size figure must be cross-verified against the source-language original.

## Excluded — do not cite

- Instagram, TikTok, YouTube videos without transcripts
- Bodybuilding forums without source citations
- Vendor blog "education" pages without primary citations
- AI-generated summary sites (medvidi, healthline marketing content)
- Sponsored content disguised as review

---

## Admissibility matrix

What each tier can support, as a claim type:

| Claim type | Tier 1 | Tier 2 | Tier 2.5 | Tier 2.7 | Tier 3 | Tier 4 | Tier 5 | Tier NE |
|---|---|---|---|---|---|---|---|---|
| Mechanism | yes | yes | yes (if cited) | no | no | no | no | yes (if tier-equivalent) |
| Efficacy / effect size | yes | yes | yes (if cited) | no | no | no | no | yes (if tier-equivalent) |
| Standard dose (literature) | yes | yes | yes (if cited) | no | yes (admin) | reconstitution-math only | no | yes (if tier-equivalent) |
| Practitioner dose (prescribing) | no | no | no | **yes** | yes | no | no | n/a |
| Cycle length convention | no | no | no | **yes** | yes | no | no | n/a |
| Adverse effect rate | yes | yes | yes (if cited) | no | no | no | qualitative leads | yes (if tier-equivalent) |
| Adverse effect existence | yes | yes | yes (if cited) | yes | yes | no | qualitative leads | yes |
| Reconstitution / route | yes | yes | yes (if cited) | yes | yes | yes | no | yes |
| Regulated status / availability | yes | yes | yes | no | yes | yes (gray-market self-disclosed) | no | yes (own-country) |
| Contraindications | yes | yes | yes (if cited) | yes (text-stated) | yes (label-derived) | no | qualitative leads | yes |

---

## How an agent uses this file

Per dispatch (any specialist):
1. Phase 1 scope: agent declares which tiers it will search.
2. Phase 3 retrieve: any source NOT on this whitelist (or its domain extension) gets auto-tagged `anecdote_aggregate`.
3. Phase 4.75 evidence-integrity gate: any numerical claim citing a `vendor_label` or `anecdote_aggregate` source HALTs the report.
4. Phase 8 wiki ingest: source → entry's `evidence_tier` per `library/methodology/evidence-tiers.md`, using the tag here to map (rct → S/A; meta_analysis → S; cohort → A/B; open_label → B; animal → C; in_vitro → C; vendor_label / anecdote → D).

Domain-extension whitelists (peptide compounders, lymphatic manual-therapy bodies, etc.) layer on top — load both the base list and the extension at Phase 1.

## Adding a host

To whitelist a new host:
1. Manual review: does the host meet the tier criteria?
2. Add to the appropriate tier above with a one-line note on what claim types it can support.
3. Update `vault/meta/log.md` with the add.
4. Note in `vault/meta/contradictions.md` if this host has historically disagreed with a higher tier.
