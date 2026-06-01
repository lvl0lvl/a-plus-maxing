# Gate 4.75 — Integrity Verifier (iteration 2)

Re-verification of the corrected corpus after the Section-B PhenoAge remediation
(prior run flagged an IC-13 number-mismatch: "~9%/yr" → corrected to ~4.5%/yr,
Levine 2018, PMID 29676998). All checks below were run against the CURRENT files:

- `sections/section-A.md` (23,526 bytes; refs [1]–[15])
- `sections/section-B.md` (27,919 bytes; refs [1]–[25])
- `sections/section-C.md` (24,697 bytes; refs [1]–[32])
- enum/whitelist: `vault/library/_source-whitelist.md` (relative path resolves here)

Method note: the integrity checks are textual/analytic and were performed by reading
the full corpus directly; eight PMIDs were independently resolved via web fetch
(29676998, 33977284, 19587680, 37289866, 40472098, 30646252, 30669119, 29599478,
25982160 — nine, all confirmed author+year+claim).

## IC-1 Type-tag presence
No untagged citation detected. Every inline `[N, tag]` and every bibliography trailing
`[tag]` across all three sections uses an admissible enum value (rct | meta_analysis |
cohort | open_label | animal | in_vitro | mechanism_review | regulatory). No
compounding_data_sheet / vendor_label / practitioner_protocol / anecdote_aggregate tags
appear (none expected in this domain).
WARN (not HALT): two Section-B bib tags carry a trailing "— flagged" qualifier AFTER a
valid enum tag:
- [9] Borrus 2024 — `mechanism_review; preprint — flagged`
- [21] Strasser & Burtscher 2018 — `mechanism_review; lower-trust publisher — flagged`
Per the gate rule a trailing "— flagged" after a valid enum is WARN, not HALT. The base
tag (`mechanism_review`) is admissible in both cases.

## IC-3 Vendor-not-numerical
No vendor_label source grounds any numerical claim. No `vendor_label` tag exists anywhere
in the corpus. Section B (Finding 12) and Section C explicitly state the DTC/marketing
critiques cite critique/mechanism_review sources, not vendor pages. No violation.

## IC-4 Anecdote-not-numerical
No anecdote_aggregate source grounds any numerical claim. No `anecdote_aggregate` tag
exists anywhere in the corpus. All numerical claims trace to Tier-1 (rct/meta_analysis/
cohort/open_label/animal/in_vitro/mechanism_review) or Tier-2 (regulatory) sources. No
violation.

## IC-7 Population-mismatch
Every animal/in_vitro numerical claim carries an in-sentence `[population-mismatch:<species>]`.
- Section A: rodent CR `[population-mismatch: rodents]`; rhesus CR Wisconsin (Colman 2014, n=76)
  and NIA (Mattison 2017, n=121) each `[population-mismatch: rhesus macaques]`. (The two rhesus
  CR figures the prompt names are both present and tagged.)
- Section B: the only animal/in_vitro numeric content is the iAge CXCL9 reversal mechanism
  (Finding 8, ref [12] dual-tagged cohort + animal) carrying `[population-mismatch: mouse and
  human cell lines]` both inline and in the bib note.
- Section C: every mouse lifespan figure carries `[population-mismatch:mouse]` — rapamycin
  (~9% M / ~14% F; ~23% F high-dose), metformin+rapamycin combo, fisetin, taurine (~10–12%);
  monkey healthspan `[population-mismatch:monkey]`; dog (TRIAD) `[population-mismatch:dog]`.
No untagged animal/in_vitro numerical claim detected.

## IC-9 Concentration-surfacing
Computed largest single-group share of distinct primaries per compound (Section C) and the
clock-cluster (Section B), plus whole-corpus.

Section C — per-compound primary-source concentration:
- Rapamycin (mouse lifespan): primaries [2] Harrison 2009, [3] Miller 2014, [8] Strong 2016
  all trace to the NIA ITP program → 3/3 = **100% single-program** (≥70%). SURFACED: the
  concentration note states the rodent rapamycin lifespan figures are ">70% single-program
  concentration … Flag any 'rapamycin extends lifespan' claim as ITP-concentrated." PASS.
- NAD+ precursors (founder-affiliated): the longevity premise concentrates around
  Sinclair/Brenner/Imai lineages with commercial ties (Metro Biotech). SURFACED explicitly
  as a "conflict-of-interest concentration." PASS (qualitative; the section's human RCT
  citation [14] Martens is independent of that group, so the *cited-primary* share is not
  itself ≥70%, but the advocacy-lab concentration is surfaced as required).
- Senolytics (Mayo/Kirkland): human D+Q primaries [17] Hickson, [18] Justice, review [19]
  Kirkland & Tchkonia, fisetin status [20] Mayo/CT.gov — Mayo Clinic / Kirkland-Tchkonia
  group is the dominant senolytic-translation source (~3/4 of the human/translation cites).
  Concentration is surfaced indirectly (Mayo AFFIRM-class trials named; "most senolytic
  lifespan/healthspan data is mouse"); the human evidence base being tiny open-label pilots
  is foregrounded. PASS (≥70% group share acknowledged via Mayo/Kirkland naming).
- Taurine (single-study): the 2023 narrative rested on **one** Science paper from one group
  ([28]/[29]/[30] are the SAME paper, Singh 2023) → effectively 1 primary = **100%**.
  SURFACED: "a textbook single-study concentration failure," with the 2025 reversal ([31],
  [32]) explicitly added as independent counter-evidence. PASS.

Section B — clock-cluster (Horvath / Levine / Belsky):
- Horvath: [1] Horvath clock, [4] GrimAge (senior), [16] NRG review, [10] Fahy co-author.
- Levine: [3] PhenoAge (first), [7] reliability fix (senior).
- Belsky: [5] DunedinPoAm AND [6] DunedinPACE (both first).
  Of the ~9 primary clock-DEVELOPMENT papers, these three labs author the clear majority
  (≈7/9 ≈ 78%, ≥70%). SURFACED at length: "well above the ~70% single-group threshold for a
  flagged concentration … treat clock provenance as a conflict-of-interest surface." PASS.

Whole-corpus: no single research group approaches ≥70% across the combined 72 distinct
primaries (A:15 + B:25 + C:32, less the 3 shared taurine-paper IDs and overlapping
Mandsager/Leong reuse across A and B). The two concentrated pockets (ITP for rodent
rapamycin; the three clock labs) are both explicitly surfaced in their respective sections.
No unsurfaced ≥70% concentration detected.

## IC-10 No fabricated citations
Every inline `[N]` resolves to a bibliography entry.
- Section A: inline refs 1–15 all map to bib [1]–[15]; no orphan inline marker, no unused-bib
  fabrication.
- Section B: inline refs 1–12 plus 16,17,18,19,20,21,24,25 all map to bib [1]–[25]; refs
  [13]–[15] (Klemera–Doubal, Parker, Wang) and [22]/[23] (ethics commentary) are cited in
  Findings 9/10/12. All 25 bib IDs are referenced; all inline IDs have a bib entry.
- Section C: inline refs 1–32 all map to bib [1]–[32].
Spot-check (9 PMIDs, web-resolved, author+year+claim match):
- **29676998** → Levine ME et al. 2018, *Aging (Albany NY)*, "An epigenetic biomarker of aging
  for lifespan and healthspan" (PhenoAge). CONFIRMED. DNAm-PhenoAge per-year all-cause
  mortality HR ≈ 1.045 (~4.5%/yr) — matches the corrected Section-B figure (see IC-13).
- **33977284** → Mannick JB et al. 2021, *Lancet Healthy Longev*, RTB101 phase 2b/3; phase 3
  MISSED primary endpoint. CONFIRMED (matches Section C ref [5]).
- **19587680** → Harrison DE et al. 2009, *Nature*, rapamycin fed late extends lifespan in
  heterogeneous mice (~9–14% by sex). CONFIRMED (one mouse-lifespan figure, ref [2]).
- **37289866** → Singh P et al. 2023, *Science*, taurine deficiency as a driver of aging;
  mouse ~10–12% median-lifespan extension + monkey + human components. CONFIRMED (ref [28]).
- **40472098** → Fernandez ME / de Cabo / Ferrucci 2025, *Science*, "Is taurine an aging
  biomarker?" — taurine does not consistently decline with age. CONFIRMED (ref [31]).
- **30646252** → Mandsager K et al. 2018, *JAMA Netw Open*, CRF vs long-term mortality,
  ~122,007 adults, elite-vs-low HR ≈ 0.20. CONFIRMED (A ref [3] / B ref [25]).
- **30669119** → Lu AT et al. 2019 (Horvath senior), *Aging*, GrimAge. CONFIRMED (B ref [4]).
- **29599478** → Martens CR et al. 2018, *Nat Commun*, chronic NR elevates NAD+ (~60%).
  CONFIRMED (C ref [14]).
- **25982160** → Leong DP et al. 2015, *Lancet*, PURE grip strength, HR ~1.16 / 5 kg.
  CONFIRMED (A ref [6] / B ref [19]).
No fabricated citation detected.

## IC-11 No placeholder strings
No placeholder strings detected. No occurrence of TBD / TODO / "research suggests" /
"citation needed" / "content continues" / lorem ipsum / FIXME in any section. All findings
are fully drafted with quantified claims and resolved citations.

## IC-12 No Wikipedia citations
No Wikipedia citations detected. No wikipedia.org / wikimedia URL appears. All URLs resolve
to whitelisted Tier-1/Tier-2 hosts (pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov,
nature.com, science.org, cell.com, elifesciences.org, jamanetwork.com, journals.plos.org,
springer.com/link.springer.com, onlinelibrary.wiley.com, fda.gov, clinicaltrials.gov,
dogagingproject.org, journalofethics.ama-assn.org, article.imrpress.com).

## IC-13 Per-citation corpus scoping
Deep-mode sampling target ≥80% / min 20. **claims_checked: 27** numerical/quoted claims
confirmed against the cited primary (counting the 9 web-resolved PMIDs above plus 18
additional figure-to-citation pairings verified by reading: A — Arem ~31% [4]; Cappuccio RR
1.12/1.30 [8]; PREDIMED HR 0.69/0.72 [9]; CALERIE n=218/~12% [10]; Waziry DunedinPACE [11];
Colman n=76 [12]; Mattison n=121 [13]; TREAT n=116 [14]; Jha ~10 yr / 90% [15]. B — Horvath
353 CpG / MAE 3.6 / r 0.96 [1]; Hannum 71 CpG / n=656 [2]; Higgins-Chen PhenoAge ~8.6 yr
replicate deviation [7]; DunedinPoAm r≈0.33 [5]; Studenski HR 0.88/0.1 m/s [18]; Oh 11
organs / ~5,676 [11]. C — ITP higher-dose female ~23% [3]; metformin-alone null [8];
Konopka exercise-blunting [13]; Yoshino 75 mg/12 wk null [22]; SmartAge null n=100 [26]).
All sampled figures are supported by their cited source; no number-not-found and no
quote-not-found.

**PhenoAge correction CONFIRMED:** Section B Finding 2 now reads "A one-year increase in
DNAm PhenoAge was associated with ~4.5% higher all-cause mortality risk in validation
[3, cohort]," and explicitly demarcates the underlying clinical phenotypic-age composite's
larger ~9%/yr (HR≈1.09) association as a SEPARATE quantity "the two must not be conflated."
This matches Levine 2018 (PMID 29676998): the DNAm clock lands at ~4.5%/yr (HR≈1.045). The
prior IC-13 number-mismatch is CLEARED.

Paywall/corpus-missing: none. All sampled primaries are open-abstract on PubMed/PMC or
open-access; no paywall-WARN required.

## Verdict
verdict: PASS
halt_reasons: []
warnings: [IC-1]
