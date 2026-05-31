# Phase 4.25 — Cross-Section Identity Reconciliation (mental-performance-coach)

Cross-section consistency audit over the three section drafts (A — cognition / lifestyle levers; B — nootropic compound landscape; C — mental-health boundary / consumer-product validity / Russian-peptide layer). Reconciliation is by IDENTITY (PMID / DOI / author-year / canonical name), NOT by section-local bibliography number. Each section numbers its own bibliography independently; the same paper appearing as [10] in A and [7] in B is expected and is NOT a mismatch.

## Verdict

verdict: PASS

No identifier or numeric disagreement found among shared entities. One shared-by-identity citation (the Shahinfar omega-3 meta-analysis) agrees on every identifier field across the two sections that cite it. Two completeness deltas on that same citation (B abbreviates the byline to "et al." and omits the volume A carries) are recorded as WARN — they are incompleteness, not contradiction, and do not HALT.

## Method note

- Mechanical sweep of all PMIDs and DOIs across the three files found exactly **one** PMID and **one** DOI appearing in 2+ files: PMID `40836005` / DOI `10.1038/s41598-025-16129-8` (Shahinfar omega-3), in A[10] and B[7]. No other primary is cited by shared identifier in 2+ sections.
- All other entities recurring across sections are either (a) shared *concepts* / *compound classes* / *named instruments* discussed via *different* primaries in each section (corroboration, not a shared-citation clash), or (b) entities that appear in only one section (no reconciliation possible or required).
- B-only PMID `22574274` flagged by the raw sweep is audit-trail-only (the OLD-value record in B's post-fix correction table; the live [20] is `23139911`). It is B-internal and absent from A and C — outside cross-section scope.

## Class 1 — Citations cited by shared identity in 2+ sections

| entity-id | sections | values in each | agree? | canonical value if mismatch |
|---|---|---|---|---|
| Shahinfar omega-3 dose-response MA — PMID | A[10], B[7] | A: `40836005` / B: `40836005` | PASS | — |
| Shahinfar omega-3 — DOI | A[10], B[7] | A: `10.1038/s41598-025-16129-8` / B: `10.1038/s41598-025-16129-8` | PASS | — |
| Shahinfar omega-3 — year | A[10], B[7] | A: `2025` / B: `2025` | PASS | — |
| Shahinfar omega-3 — source title | A[10], B[7] | A: *Scientific Reports* / B: *Scientific Reports* | PASS | — |
| Shahinfar omega-3 — type-tag | A[10], B[7] | A: `[meta_analysis]` / B: `[meta_analysis]` | PASS | — |
| Shahinfar omega-3 — first-author / byline | A[10], B[7] | A: `Shahinfar, H., Yazdian Z., Asgari Avini N., Torabinasab K., Shab-Bidar S.` / B: `Shahinfar H, et al.` | WARN | First author agrees ("Shahinfar H"). B truncates to "et al."; A carries the full list. Completeness delta, not an identity conflict. Recommend B adopt A's full byline for parity. |
| Shahinfar omega-3 — volume | A[10], B[7] | A: `15:30610` / B: (omitted) | WARN | A carries volume `15:30610`; B omits it. B has no conflicting value — incompleteness, not contradiction. Recommend B add `15:30610`. |

Body-text framing of this same paper: A characterizes omega-3 qualitatively ("no significant global-cognition benefit; some dose-dependent attention/perceptual-speed signals at higher intakes"); B quotes the per-2000 mg/day dose-response figures (attention SMD 0.98, processing speed SMD 0.50). These are different *levels of detail* drawn from the same source, not contradictory numbers — A states no figure that conflicts with B's. PASS (no numeric clash).

## Class 2 — Institutions / research groups

All institutional named entities are confined to Section C (§C-5 Russian-peptide layer). None recur in A or B, so there is no cross-section reconciliation. Recorded here for completeness; intra-C naming is internally consistent.

| entity-id | sections | values | agree? |
|---|---|---|---|
| Institute of Molecular Genetics RAS | C only (C5-1, C5-2, concentration notes) | "Institute of Molecular Genetics, Russian Academy of Sciences" / "Institute of Molecular Genetics RAS" | N/A (single section; intra-C consistent — same institute, full vs abbreviated form) |
| V.V. Zakusov Institute of Pharmacology | C only (C5-2, C5-3, concentration notes) | "V.V. Zakusov Institute of Pharmacology" / "Zakusov Research Institute of Pharmacology" | N/A (single section; intra-C consistent) |

## Class 3 — Compound / molecule identifiers

| entity-id | sections | naming used | shared dose/effect figure for SAME compound? | agree? |
|---|---|---|---|---|
| caffeine | B only (findings 1–4) | "caffeine" | A does not discuss caffeine (A finding 8 covers glucose/hydration/omega-3, not caffeine) | N/A (single section) |
| L-theanine | B only (findings 5–6) | "L-theanine" | — | N/A (single section) |
| creatine | B only (findings 7–8) | "creatine / creatine monohydrate" | — | N/A (single section) |
| omega-3 / DHA | A (finding 8), B (finding 9) | A: "Omega-3/DHA"; B: "Omega-3 / DHA" | Shared Shahinfar source reconciled in Class 1; A/B each also cite distinct second sources (A none beyond [10]; B adds Yurko-Mauro [13], C-only: none). No same-source numeric duplicated with differing values. | PASS (naming agrees; the one shared citation agrees) |
| modafinil | B (finding 13) | "modafinil" | C finding 10 (Moran) covers methylphenidate/amphetamine, not modafinil | PASS (naming agrees; B's modafinil figures from Roberts [18] are not duplicated in C) |
| methylphenidate | B (findings 13–14), C (finding 10) | both "methylphenidate" | B SMD figures from Roberts 2020 [18]; C incidence 0.10% from Moran 2019 [12] — DIFFERENT primaries, different endpoints (enhancement effect vs psychosis incidence). No same-source figure conflict. | PASS (naming agrees; no shared-source numeric) |
| amphetamine / D-amphetamine | B (findings 13–14), C (finding 10) | B: "D-amphetamine" (Roberts enhancement series) + "amphetamines" (finding 14 scheduling); C: "amphetamine" (Moran psychosis cohort) | Same drug class; different primaries, different endpoints (B: no enhancement effect; C: 0.21% psychosis incidence). Distinct sources, no numeric overlap. | PASS (consistent class naming; no shared-source numeric) |
| Semax / Selank / Noopept | C only (§C-5) | consistent | — | N/A (single section) |
| BDNF (exercise/Semax mechanism) | A (finding 4, rat), C (C5-1, Semax rodent) | "BDNF" both; both flagged rodent/predominantly-rodent, not upgraded to human | Different primaries (A: Gomez-Pinilla [5]; C: Semax rodent literature). No shared figure. Both hold BDNF as mechanism-not-human-outcome — consistent epistemic stance. | PASS (naming + epistemic framing agree) |

## Class 4 — Instruments / named entities

| entity-id | sections | values | agree? |
|---|---|---|---|
| PHQ-9 | C only (finding 3) | sens 88% / spec 88% at ≥10; Kroenke 2001, PMID 11556941 | N/A (single section) |
| GAD-7 | C only (finding 4) | sens 89% / spec 82% at ≥10; Spitzer 2006, PMID 16717171 | N/A (single section) |
| C-SSRS | C only (findings 6–7) | Posner 2011, PMID 22193671, 5-band ladder | N/A (single section) |
| Maslach Burnout Inventory | C only (finding 5) | Maslach & Jackson 1981, DOI 10.1002/job.4030020205 | N/A (single section) |
| ICD-11 burnout (QD85) | C only (finding 5) | WHO 28 May 2019, code QD85, "occupational phenomenon" | N/A (single section) |
| 988 Suicide & Crisis Lifeline | C only (findings 7, 9) | SAMHSA-funded, live 16 Jul 2022 | N/A (single section) |
| Lumosity FTC settlement | C only (finding 11) | $2,000,000 paid / $50,000,000 suspended judgment; matter 132-3212; civil action 3:16-cv-00001 N.D. Cal.; entered 8 Jan 2016 | N/A (single section; intra-C figures internally consistent) |

## Class 5 — Regulatory dates / numbers / recurring effect-sizes

| entity-id | sections | values | agree? |
|---|---|---|---|
| FTC Lumosity order (date / amount / matter no.) | C only (finding 11) | 8 Jan 2016 / $2M paid, $50M suspended / matter 132-3212 | N/A (single section) |
| SAMHSA 988 launch date | C only (finding 9) | 16 July 2022 (National Suicide Hotline Designation Act 2020) | N/A (single section) |
| EFSA creatine finding | B only (finding 8) | 2024, Article 13(5), PMID 39564533, "no cause-and-effect established"; effect only at 20 g/day | N/A (single section) |
| FDA caffeine 400 mg/day | B only (finding 4) | 400 mg/day no-adverse-effect threshold | N/A (single section) |
| near-transfer / far-transfer effect characterization | A (finding 12), C (findings 11–12) | A: verbal WM g≈0.31, visuospatial WM g≈0.28; far-transfer nonverbal g≈0.05, verbal g≈0.05 ns (Melby-Lervåg [19], PMID 27474138). C: qualitative "near present, far largely absent" (Simons [14], Stanford/Max Planck [15]). | PASS — same scientific conclusion (near real, far not demonstrated), DIFFERENT primaries, no shared figure to clash. Numbers in A are from a source C does not cite; C states no number that contradicts A. |

## Whole-corpus tally

- **Total shared entities scanned (appearing in 2+ sections):** 8
  - 1 shared-by-identity citation (Shahinfar omega-3) — reconciled across 7 metadata fields.
  - 4 shared compound/molecule names (omega-3/DHA, methylphenidate, amphetamine/D-amphetamine, BDNF) discussed via different primaries.
  - 1 shared concept (near/far-transfer brain-training) via different primaries.
  - (modafinil partially shared at class level — appears in B; the C stimulant finding is methylphenidate/amphetamine.)
- **Single-section entities recorded for completeness (no reconciliation required):** PHQ-9, GAD-7, C-SSRS, MBI, ICD-11 burnout, 988/SAMHSA, FTC Lumosity, EFSA creatine, FDA caffeine 400 mg, Institute of Molecular Genetics RAS, Zakusov Institute, caffeine, L-theanine, creatine, Semax/Selank/Noopept.
- **Mismatch count by class:** Class 1 = 0; Class 2 = 0; Class 3 = 0; Class 4 = 0; Class 5 = 0. **Total MISMATCH = 0.**
- **WARN count:** 2 — both on the Shahinfar citation (B byline truncated to "et al." vs A's full byline; B omits volume `15:30610` that A carries). Neither is an identifier/numeric disagreement.
- **Tag-discordance WARNs:** 0 — the one shared-identity citation carries `[meta_analysis]` in both sections; tags agree.

## Disposition

PASS. No HALT-class identifier or numeric disagreement exists across sections. The single shared-by-identity citation agrees on PMID, DOI, year, title, source, and type-tag. The two WARN items (byline abbreviation, missing volume on B[7]) are cosmetic completeness deltas, not contradictions, and are surfaced for optional parity polish — they do not block the integrity gate.

**Optional polish (non-blocking, for the synthesizing author's discretion):**
- B[7] could adopt A[10]'s full byline (`Shahinfar H, Yazdian Z, Asgari Avini N, Torabinasab K, Shab-Bidar S`) and add volume `15:30610` for byte-for-byte parity with A[10]. Identifiers already match, so this is cosmetic.
