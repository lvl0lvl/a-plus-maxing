# Phase 4.75 — Citation Integrity Gate (mental-performance-coach, mode=standard)

Independent integrity sweep of section-A.md, section-B.md, section-C.md against the canonical IC-1…IC-13 checks (`references/citation-integrity.md`), the population-mismatch and concentration-audit rules (`references/health-gates.md` §1, §3), and the type-tag enum (`vault/library/_source-whitelist.md`). The verifier checks structural compliance, not content quality. IC-13 corpus scoping is SKIP-mode at standard.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: [IC-10]
```

verdict: PASS

## IC checks

| Check | Status | Checked / Flagged | Findings |
|---|---|---|---|
| IC-1 Type-tag presence | PASS | 64 inline `[N, tag]` checked / 0 flagged | Every inline citation carries exactly one tag drawn from the enum (`rct, meta_analysis, cohort, open_label, animal, in_vitro, mechanism_review, regulatory, vendor_label, practitioner_protocol, compounding_data_sheet, anecdote_aggregate`). A: 21 cites; B: 22 cites; C: 21 cites. No untagged inline cite; no out-of-enum tag. |
| IC-2 Bibliography type-tag presence | PASS | 64 bib entries (A 21 + B 20 + C 23) / 0 flagged | Every numbered bibliography entry ends in a single bracketed enum tag. No multi-tag entries present; none required. |
| IC-3 Vendor-not-numerical | PASS (SKIP — none present) | 0 `vendor_label` cites | No `vendor_label` citation exists in any section. The only `vendor_label` string in the corpus is in B's self-check (line 84) attesting "zero such sources used." Vacuously clean. |
| IC-4 Anecdote-not-numerical | PASS | 1 `anecdote_aggregate` cite (C[16]) / 0 flagged | C[16] (Cognitive Training Data open letter) is the only anecdote cite. Its sentence (C line 44) contains numerals "~133 scientists/practitioners" (a signatory count) and a year — neither is an AE rate, dose, or effect size. The text explicitly states [16] "never grounds an efficacy claim, only documents that dissent exists." No numerical efficacy/AE/dose claim rests on it. |
| IC-5 Practitioner-protocol-not-efficacy | PASS (SKIP — none present) | 0 `practitioner_protocol` cites | No `practitioner_protocol` citation in any section. (Section B routes prescription enhancers to a prescriber as PRESCRIPTIVE_DIRECTIVE but does not cite any practitioner-protocol source.) Vacuously clean. |
| IC-6 Compounding-data-sheet-with-efficacy | PASS (SKIP — none present) | 0 `compounding_data_sheet` cites | No `compounding_data_sheet` citation in any section. Vacuously clean. |
| IC-7 Population-mismatch | PASS | 3 animal cites checked / 0 flagged | See Population-mismatch block. All three animal-tagged numerical/mechanistic claims carry an in-sentence `[population-mismatch: <species>]`. No `in_vitro` cites present. |
| IC-8 Route-extrapolation | PASS | 2 route-divergent claims checked / 0 flagged | Section C §C-5 intranasal Semax [19] and Selank [21] human data each carry `[route-extrapolation: intranasal]` in-sentence; the text states "no oral-equivalence claim is made." Noopept [22] human data is oral and cited as oral (no route divergence). No oral claim is grounded on intranasal/IV data without a flag. Sections A and B make no compound-dosing/route claims. |
| IC-9 Concentration-surfacing | PASS | total_primaries 35 / 0 flagged | Largest single-group cluster = Russian-nootropic (Moscow: Institute of Molecular Genetics RAS + V.V. Zakusov Institute of Pharmacology), count 5, share 0.143. Below the 0.70 threshold — no mandatory first-class section required. (And the cluster is in fact already confined to and surfaced in a first-class labeled subsection §C-5 with an explicit concentration caveat.) See Concentration audit block. |
| IC-10 Cross-section identity | WARN (non-blocking) | 1 shared primary across sections / 0 identifier disagreements | The omega-3 dose-response meta-analysis (Shahinfar 2025, PMID 40836005, DOI 10.1038/s41598-025-16129-8) is cited in both A[10] and B[7]. Identifiers agree exactly; tags agree (both `meta_analysis`). No tag-discordance, no identifier conflict. Logged as WARN per the gate convention that any cross-section shared citation is surfaced; not a HALT. Confirms and extends the Phase 4.25 PASS. |
| IC-11 No placeholder strings | PASS | full-file grep / 0 hits | `rg` for `citation needed | TBD | TODO | Content continues | according to some reports | research suggests | experts believe` across all three sections returned zero matches. |
| IC-12 No Wikipedia citations | PASS | full-file grep / 0 hits | `rg` for `wikipedia.org` across all three sections returned zero matches. No Wikipedia URL in any bibliography. |
| IC-13 Per-citation corpus scoping | SKIP-mode | n/a | Standard mode → corpus scoping not executed; full corpus not retrieved per the gate's mode policy. `corpus_scoping.verdict = "SKIP-mode"`. |

## Population-mismatch

```yaml
verdict: PASS
checked_citations: 3
flagged_citations: []
```

Three `animal`-tagged citations carry numerical or mechanistic claims; each carries an in-sentence `[population-mismatch: <species>]`. No `in_vitro` citations present.

- **Section A, line 32 — [5, animal] (Gomez-Pinilla 2008, BDNF necessity):** "In rats, blocking hippocampal BDNF (TrkB-IgG) fully abolishes the spatial-learning benefit of one week of voluntary exercise…" carries `[population-mismatch: rat]` in the same sentence. The species is also the explicit subject ("In rats"), so the override would apply regardless. Flagged correctly. The human BDNF figures in the same finding (g=0.46, g=0.28) are grounded on [6, meta_analysis] (human), not the animal cite. PASS.
- **Section C, line 52 — [20, animal] (Eremin 2005, Semax striatal 5-HIAA +25%, mouse):** carries `[population-mismatch: mouse]` in the same sentence. PASS.
- **Section C, line 56 — [23, animal] (Ostrovskaya 2001, oral GVS-111 antiamnestic in rats at 0.5–10 mg/kg):** carries `[population-mismatch: rat]` in the same sentence. PASS.

Watch items from the brief confirmed clean: the BDNF rodent mechanism (Section A) and the Russian-nootropic rodent data (Section C §C-5) are both flagged. The Semax/Selank BDNF/NGF/TrkB upregulation prose ("predominantly rodent hippocampal data — do not upgrade to human-outcome certainty") is a qualitative not-upgraded caveat with no animal cite attached to a human-presented numerical claim — no flag required, and the prose explicitly down-weights it.

## Concentration audit

```yaml
concentration_audit:
  verdict: PASS
  total_primaries: 35
  largest_cluster_name: "Russian-nootropic cluster (Moscow: Institute of Molecular Genetics RAS + V.V. Zakusov Institute of Pharmacology)"
  largest_cluster_count: 5
  share: 0.143
  threshold_triggered: false
  surfaced_as_first_class_section: true   # §C-5, though not mandatory at this share
```

**Method.** Distinct admissible primaries = inline citations tagged `rct | meta_analysis | cohort | open_label | animal | in_vitro`, deduplicated across all three sections by PMID/DOI. `mechanism_review`, `regulatory`, and `anecdote_aggregate` excluded per IC-9 / health-gates §3.

- Section A admissible primaries (13): [2],[3],[4],[5],[6],[7],[9],[10],[12],[18],[19],[20],[21].
- Section B admissible primaries (12): [1],[2],[3],[4],[5],[6],[7],[10],[13],[14],[16],[18].
- Section C admissible primaries (11): [3],[4],[7],[8],[12],[17],[19],[20],[21],[22],[23].
- Cross-section duplicate: Shahinfar 2025 omega-3 (PMID 40836005) = A[10] = B[7] → counted once.
- **Total distinct = 13 + 12 + 11 − 1 = 35.**

**Clusters.** Largest single-group cluster is the Russian-nootropic body confined to Section C §C-5: Kaplan [19], Eremin [20], Zozulia [21], Neznamov [22], Ostrovskaya [23] — the two Moscow institutes treated as one national cluster per §C-5's own analysis = 5 primaries. Next-largest is the Jaeggi/Buschkuehl working-memory-training group (A[20] Jaeggi, A[21] Au) = 2. All remaining 28 primaries are independent groups spanning exercise, sleep, nutrition, stress/HRV, caffeine, creatine, adaptogens, prescription-enhancer, instrument-validation, and wearable-validity literatures.

**Share = 5 / 35 = 0.143.** Far below the 0.70 health-gates §3 trigger. No mandatory first-class concentration section is required by the gate.

**Note (not required, but verified):** the §C-5 Russian-nootropic cluster — the brief's named candidate — is already housed inside a first-class labeled subsection (`## §C-5 Non-English (Russian nootropic) survey`) carrying an explicit "CANONICAL ≥70% watch item" caveat that within the §C-5 *sub-corpus* the institutional concentration exceeds 70%. That local (within-Russian-peptide) characterization is internally consistent and does not change the corpus-wide share, which is what IC-9 measures. Properly surfaced either way.

## Corpus scoping

```yaml
corpus_scoping:
  verdict: SKIP-mode
  mode: standard
  claims_checked: 0
  claims_failed: []
```

Standard mode → IC-13 per-citation corpus scoping is SKIP-mode. Full corpus not retrieved; no claim-vs-source grep performed. (Numerical-claim grounding was confirmed structurally: every numerical efficacy/AE/dose figure is attached to a Tier-1/2 study-design tag or a `regulatory` source, and no numerical claim rests on `vendor_label`/`anecdote_aggregate` — see IC-3/IC-4.)

## Halt reasons

(none — verdict PASS)

## Warnings

- **IC-10 (non-blocking):** One primary is shared across sections — Shahinfar 2025 omega-3 dose-response meta-analysis, PMID 40836005 / DOI 10.1038/s41598-025-16129-8, cited as A[10] and B[7]. Identifiers and type-tags agree across both occurrences (no tag-discordance, no identifier conflict). Surfaced per the cross-section-identity convention; deduplicated to a single primary in the IC-9 count. Confirms and extends the Phase 4.25 cross-section PASS.
- **Phase 4.25 carry-forward (byline/volume WARNs), all already remediated in-section and re-verified here:**
  - Section A [16] (Beerendonk/Mejías 2024, PNAS) volume/issue corrected `121(6)` → `121(5)`; grep confirms the old value has zero residual hits and `e2312898121`/PMID 38277436/DOI tail each occur exactly once on bibliography line 122.
  - Section B [20] (Lakhan 2012) PMID corrected `22574274` → `23139911`; the OLD PMID survives only inside B's post-fix audit trail (lines 95, 100) documenting its removal, not in the live bibliography line 77 (which now reads 23139911). B [2] byline expanded `James JE.` → `James JE, Rogers PJ`.
  - Section C [8] (Wastler 2023, SAFETY citation) fabricated author "Lucht L" removed; full verified author list substituted; "Lucht" has zero hits outside the audit trail. C [22] (Neznamov/Noopept) PMID/journal record made internally consistent (Russian original vs English translation disambiguated). C [23] (Ostrovskaya) full author list restored.
  - These are documented citation-fidelity fixes with grep verification in each section's "Post-fix grep audit"; none alters a numerical claim, a type-tag, a population-mismatch flag, or a route flag. No residual HALT-class defect.
```
