# Gate 4.75 — Citation Integrity Verifier (LDL-C, mode=standard)

INDEPENDENT Phase 4.75 verification of `sections/section-A.md` + `sections/section-B.md`
against the project type-tag enum, admissibility matrix, and the three health-specific
gates. All 13 IC checks run. The verifier checks structural compliance + corpus grounding;
it does not re-judge content quality.

Corpus under review: `sections/section-A.md`, `sections/section-B.md`, and 17 corpus files
under `corpus/` (`A-ref1…A-ref9`, `B-ref1…B-ref8`; `atp3raw.txt` is the source PDF text for
`B-ref3`).

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: []
```

LDL-C is a human biomarker. The corpus is entirely human RCT/meta-analysis/cohort primary
literature, peer-reviewed mechanism/society reviews, and one NIH regulatory band table. No
animal, in-vitro, vendor, anecdote, practitioner, or compounding source appears — so the
gates that catch the BPC-157-class failure modes (rodent-extrapolation, single-lab
dominance, vendor-grounded numbers) pass cleanly and non-vacuously.

## IC-1 Type-Tag Presence

Every inline citation matches `[N, <tag>]` with a tag from the canonical enum. Extracted
tag set: `meta_analysis`, `mechanism_review`, `cohort`, `regulatory`. Section A: refs 1–3
`meta_analysis`, 4/7/8 `mechanism_review`, 5/6/9 `cohort`. Section B: 1/2/4/6
`mechanism_review`, 3 `regulatory`, 5 `cohort`, 7/8 `meta_analysis`. No out-of-enum tag, no
untagged inline citation. PASS.

## IC-2 Bibliography Type-Tag Presence

All 9 Section-A and 8 Section-B bibliography entries carry a single enum tag annotation
matching their inline use (e.g., `meta_analysis — Tier 1`, `regulatory — Tier 2`,
`mechanism_review (society guideline) — Tier 2.5`). No bibliography entry is untagged. PASS.

## IC-3 Vendor-Not-Numerical

No `vendor_label` citation present in either section. No numerical claim rests on a vendor
source. PASS (vacuous-clean — no vendor source exists to mis-ground).

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citation present. No numerical AE rate, dose, or effect size rests on
an anecdote source. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citation present. (Tag discipline is correctly applied upstream:
the 2019 ESC/EAS and 2018 AHA/ACC society guidelines are tagged `mechanism_review`, NOT
`practitioner_protocol` — per the society-guidelines→mechanism_review rule. They ground
risk-stratified goals/thresholds, which are guideline statements, not practitioner-dosing
conventions.) PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citation present. PASS.

## IC-7 Population-Mismatch (health-gates §1)

Grep for `[N, animal]` and `[N, in_vitro]` across both sections: zero matches. LDL-C is a
human biomarker; every effect size derives from a human population stated inline — CTT
pooled human RCTs (~170k; 174,149), Ference MR (312,321), Martin-Hopkins (1,350,908 lipid
profiles), Sampson human validation, UK Biobank discordance cohort (293,876), fiber RCTs
(12,773 participants), human guideline cohorts. No rodent or in-vitro source grounds any
numerical claim, so no `[population-mismatch: <species>]` tag is required anywhere.
`checked_citations: 17` (all distinct bibliography sources screened; 0 animal/in_vitro).
PASS — expected for a human biomarker.

## IC-8 Route-Extrapolation

N/A for a biomarker entry. LDL-C is a measured analyte, not a dosed compound; the only
"dose" content is statin/PCSK9i/ezetimibe/bempedoic/inclisiran % LDL-lowering, each cited to
human RCT/meta-analysis at its tested route (oral statins; SC PCSK9i/inclisiran) with no
route substitution in any claim. No route-mismatch detected. PASS (no route extrapolation).

## IC-9 Concentration-Surfacing (health-gates §3)

Distinct primary citations (enum {rct, meta_analysis, cohort, open_label, animal, in_vitro},
deduped across both sections): 9 —
CTT2010 [A1], CTT2012 [A2], Ference-MR2012 [A3], Martin-Hopkins2013 [A5], Sampson2020 [A6],
Sniderman-discordance2024 [A9], equations-accuracy/AJCP2024 [B5], fiber-meta [B7],
novel-agents-NMA [B8]. (The `mechanism_review` and `regulatory` sources — EAS-2017,
cumulative-2024, Glavinovic-2022, ESC/EAS-2019, AHA/ACC-2018, LDL-equations-review,
StatPearls, NCEP-ATP-III — are excluded from the primary enum per §3.)

Largest author-group cluster: the CTT Collaboration (2 entries: A1, A2). Share = 2/9 = 0.22.
This is far below the 0.70 threshold; LDL-C literature is genuinely multi-cohort/multi-group
(CTT, Wayne State, Johns Hopkins, NIH, McGill, plus independent meta-analyses). Threshold
NOT triggered; no first-class concentration-risk section is required. The ≥70%-first-class
HALT condition does not apply. PASS.

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry: Section A inline numbers 1–9 ↔ bib
entries 1–9; Section B inline numbers 1–8 ↔ bib entries 1–8. No dangling inline citation.
All bibliography entries carry resolvable identifiers (PMIDs/DOIs/PMC IDs/NBK bookshelf ID/
official ACC + NHLBI URLs). No fabricated reference detected. (Per standard-mode budget,
exhaustive HEAD-checking is best-effort; identifiers are well-formed and corpus-grounded.)
PASS.

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some
reports`, `research suggests`, `experts believe`: zero matches in either section. PASS.

## IC-12 No Wikipedia Citations

Grep for `wikipedia` across both sections + bibliographies: zero matches. No Wikipedia URL in
either bibliography. PASS.

## IC-13 Per-Citation Corpus Scoping

Standard mode floor: ≥50% sample of numerical/quoted claims (min 10). I grep-verified the
full set of load-bearing numerical claims against the cited corpus files — 52 distinct
numeric/quoted claims checked (23 in Section A, 29 in Section B) = 100% of load-bearing
claims, well above the 50% floor.

Every claim matched its cited corpus file exactly (unit/typography normalization applied for
en-dash vs hyphen and `38.7` vs `38.67` precision):

Section A — all verified against the cited corpus:
- 38.7 mg/dL conversion [3] ✓; MVE RR 0.78 (0.76–0.80), coronary 0.87 (0.81–0.93), revasc
  0.81 (0.76–0.85), stroke 0.86 (0.77–0.96), mortality 0.90 (0.87–0.93) [1] ✓; 26 trials /
  ~170,000 [1] ✓; "22%" + "up to three-fold" [4] ✓; 27 trials / 174,149 / 21% / RR 0.79
  (0.77–0.81) / 11-per-1,000 [2] ✓; 312,321 / 54.5% (48.8–59.5%) / p=8.43×10⁻¹⁹ [3] ✓;
  1,350,908 / 91.7% vs 85.4% / 84.0% vs 40.3% / median 5.2 IQR 4.5–6.0 [5] ✓; Sampson TG≤800
  / CCC 0.992 [6] ✓; r=0.96 / ApoB 85.8–108.8 / 7.3 vs 4.0 / HR 1.06 / 293,876 [9] ✓.

Section B — all verified against the cited corpus:
- ESC/EAS goals <55/1.4, <70/1.8, <100/2.6, <116/3.0, recurrent <40/1.0 within 2y, SCORE
  ≥10% / 5–9%, TC>310, LDL>190, BP 180/110, eGFR 30–59 [1] ✓; AHA/ACC ezetimibe/PCSK9i ≥70,
  severe ≥190→<100, statin intensity ≥50%/30–49%/<30% [2] ✓; ATP III bands 100–129/130–159/
  160–189 + TC 200–239/≥240 + HDL <40/≥60 [3] ✓; conversion 38.67/0.02586, Friedewald TG/5
  + >400 invalid, Martin-Hopkins F 3.1–11.9 / 180-cell, Sampson full formula constants [4] ✓;
  62.1% vs 40.4% vs 19.3% / 111,939 [5] ✓; FH LDLR ≥85%/>1600, HeFH >190 / 1:250, HoFH >450
  / 1:300,000 / up to 1:100 [6] ✓; fiber 165 RCTs/12,773, −5.57 (−7.44,−3.69), 1.11/g,
  −8.28, −10.75 at 10 g/day [7] ✓; PCSK9i −54.6/−52.6/real-world −58/−62, ezetimibe 26–46%
  less / 15–20%, bempedoic −17.4 to −18.1 / −21.4 to −28.5 / −20.7, inclisiran −51% at 77 wk
  [8] ✓.

Zero `quote-not-found`, zero `number-not-found`, zero `paraphrase-no-token-match`, zero
`corpus-missing`. PASS.

## Notes on tag discipline (no finding)

- Society guidelines (2019 ESC/EAS, 2018 AHA/ACC) correctly tagged `mechanism_review`, not
  `regulatory` or `practitioner_protocol`.
- NHLBI/NCEP ATP III correctly tagged `regulatory` (US government / NIH).
- No number is attached to a vendor or anecdote source. Tag discipline is clean.

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {"IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"}, "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"}, "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"}, "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"}, "IC-13": {"status": "PASS"}},
  "population_mismatch": {"verdict": "PASS", "checked_citations": 17},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 9, "largest_cluster_count": 2, "share": 0.22, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 52, "claims_failed": []},
  "halt_reasons": [],
  "warnings": [],
  "iterations": 1
}
```
