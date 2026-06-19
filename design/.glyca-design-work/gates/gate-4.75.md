# Gate 4.75 — Citation Integrity Verifier (GlycA)

Independent Phase 4.75 integrity verification. Mode = standard. All 13 IC checks run against
`sections/section-A.md` + `sections/section-B.md` and the saved corpus at `corpus/*.txt`.
The Section A "Post-fix grep audit" block (lines 112+) is documentation; its quoted OLD tag
strings (e.g. `[1, mechanism_review]` at line 114) are not live claims and are excluded.

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: [IC-13]
```

GlycA is a research/emerging-grade human serum/plasma NMR biomarker. No animal/in-vitro
extrapolation, no vendor/anecdote/practitioner/compounding citations. Every numerical claim is
sourced to a Tier 1/2 primary or review with an enum tag, and the load-bearing numbers grep-verify
against saved corpus. Two non-blocking quality notes (open-access MDPI single-source heritability;
medRxiv preprint Nightingale unit means) are already flagged inline in the draft.

## IC-1 Type-Tag Presence

All inline `[N, tag]` citations carry an enum tag. Distinct inline tags used across both sections:
`cohort` (32), `mechanism_review` (30), `meta_analysis` (1), `regulatory` (2). The single
`[1, mechanism_review]` at section-A line 114 is inside the Post-fix grep audit block documenting
the OLD (pre-retag) string — not a live citation. No non-enum tag detected. PASS.

## IC-2 Bibliography Type-Tag Presence

Section A bibliography (refs 1–9): 7× `cohort`, 1× `mechanism_review` (ref 8 Connelly 2017
J Transl Med), 1× `regulatory` (ref 9 StatPearls/NIH). Section B bibliography (refs 1–11): backtick
tags all from enum — `cohort`, `mechanism_review`, `meta_analysis`; multi-purpose annotations
(`[cohort — TwinsUK; open-access, flagged single-source]`, `[cohort — PREPRINT, not peer-reviewed]`)
preserve a valid base tag. The `[N, tag]` on section-B line 3 is the goal-statement template, not a
citation. PASS.

## IC-3 Vendor-Not-Numerical

No `vendor_label` citation appears anywhere. The only "vendor_label" string hits are in self-check
prose attesting absence ("no vendor_label … carries any number"). PASS — no vendor cites detected.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citation appears. Only self-check prose references the term. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citations detected. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations detected. PASS.

## IC-7 Population-Mismatch

No `animal` or `in_vitro` citations exist — GlycA is a human serum/plasma biomarker, so the §1
trigger is structurally absent. The women-only WHS-derived effect sizes (Akinkuolie 2014/2015,
Lawler 2016) are annotated as population *annotations* (cohort identity stated inline + in the
section-A self-check: "Women's Health Study = women only"), which is the correct treatment — these
are population annotations, NOT population mismatches (human → human). checked_citations = 13
distinct primaries reviewed for the animal/in-vitro trigger; 0 triggered. PASS.

## IC-8 Route-Extrapolation

GlycA is a measured circulating biomarker, not an administered compound; the report makes no dose/
route claims. Route-extrapolation is not applicable. PASS (no route-bearing dose claims).

## IC-9 Concentration-Surfacing

Distinct primaries (type ∈ {cohort, meta_analysis}), deduped across A+B by PMID/DOI = 13:
Otvos 2015 (25779987, appears in both A+B → deduped to 1), Akinkuolie 2014 (25249300),
Akinkuolie 2015 (25908766), Duprez 2016 (27173011), Gruppen 2015 (26398105), Ritchie 2015
(27136058), Lawler 2016 (26951635), Bariatric (PMC6585399), Exercise meta (30170218),
Julkunen UK Biobank (PMC9898515), Heritability MDPI (10.3390/biom14050563), McGarrah smoking
(28838917), medRxiv preprint (10.1101/2025.12.01.25341421). Reviews/regulatory excluded from
cluster math per §3 step 1.

Largest cluster = Mora/Brigham Women's Health Study group (Akinkuolie 2014, Akinkuolie 2015,
Lawler 2016) = 3 of 13. Share = 0.23, well below the 0.70 threshold. The evidence base spans
multiple independent groups/cohorts (WHS, MESA, PREVEND, FINRISK, UK Biobank, TwinsUK, MESA+ELSA).
threshold_triggered = false → no first-class concentration section required; gate passes
vacuously. PASS.

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry. Section A inline refs span 1–9, bibliography
has entries 1–9. Section B inline refs span 1–11, bibliography has entries 1–11. No orphan inline
cite; no inline number without a bibliography entry. PMIDs/DOIs/PMC IDs are concrete and
consistent across inline use and bibliography. PASS.

## IC-11 No Placeholder Strings

Grep for `citation needed | TBD | TODO | Content continues | according to some reports |
research suggests | experts believe` → no matches. PASS.

## IC-12 No Wikipedia Citations

No `*.wikipedia.org` URL in either bibliography. PASS.

## IC-13 Per-Citation Corpus Scoping

Standard-mode floor: ≥50% of numerical/quoted claims, minimum 10. Actual coverage far exceeds the
floor — ~80 load-bearing numerical/quoted claims grep-verified against saved corpus
(36 in Section A, 43 in Section B), 0 genuine failures.

Section A (36/36 PASS): Otvos correlations r=0.56/0.46/0.35, CVs 1.9%/2.6%/4.3% (A-ref1);
WHS n=27,491, 1,648 events, r=0.61, CVD HRs 1.64 (CI 1.39-1.93), per-SD 1.15, mut-adj 1.08
(A-ref2); T2D n=26,508, 2,087 cases, HRs 2.67/1.65/1.11 (A-ref3); MESA n=6,523, events
915/922/1,324 (A-ref4); PREVEND n=4,759, 298 events, HR 1.16, joint 1.79 (A-ref5); FINRISK
n=7,599, HRs 1.40/1.48/2.36/2.25 (A-ref6); mortality n=27,524, 3,523 deaths, 5y HR 1.21,
JUPITER n=12,527 HR 1.33 (A-ref7); CRP 100- to 1000-fold (A-ref9).

Section B (43/43 PASS): NMR 2.0 ppm, LabCorp 369/IQR 326-416, 400 cutpoint, RA/SLE 398,
psoriasis 412.3 (B-ref2); CVs 1.9%/2.6%/4.3%, hsCRP 29.2%, chol 5.7%, trig 18.0%, 23 volunteers,
MESA n=5537, r=0.56 (B-ref1); Nightingale means 1230/1216/1233/1236 (B-ref10); ~5% vs ~30%,
sex diff <10%, hsCRP 40% higher in women, JUPITER N=10,039, statin-failed-to-fall quote (B-ref9);
HFpEF HR 2.18 (CI 1.15-4.13), HFrEF 1.06, MESA n=6,507, 43% 5y CV-mortality (B-ref11); median HR
1.26, UKB n=118,461 (B-ref5); obese 451±47 / normal 326±36, BMI r=0.14, bariatric 383/348,
r=0.41 (B-ref3); smoking +19.9 / +4.1, n=11,509, pack-year +1.6 (B-ref8); exercise pooled -9.12,
n=1,568 (B-ref4); heritability h²=0.2971, CRP 0.2786, Rg=0.4397 (B-ref6). Verbatim quotes
verified: "GlycA levels failed to show significant reductions" (B-ref9); "greater long-term
stability than" hs-CRP (B-ref7).

Out-of-scope (no `[N, tag]` corpus citation): the rosuvastatin "37%" hs-CRP figure at section-B
line 36 is explicitly tagged `[external context; statin-CRP]` and re-flagged in the external-context
note (line 58) as "not a GlycA numeric claim" — it grounds no cited primary, so IC-13 does not
score it. The actual GlycA-statin claim is the verbatim quote from [9], which IS grounded.

WARN (non-blocking, already flagged inline in draft + self-check):
- Heritability ~30% (h²=0.2971, Rg=0.4397) rests SOLELY on ref 6 (MDPI Biomolecules 2024,
  open-access). Load-bearing single-source on a lower-trust open-access host → quality note. The
  number grep-verifies in corpus; the concern is source-trust, not fabrication. Already annotated
  `[cohort — TwinsUK; open-access, flagged single-source]`.
- Nightingale platform unit means (1230/1216/1233/1236 μmol/L) rest on ref 10 (medRxiv 2025
  preprint, not peer-reviewed) for the specific numeric values, cross-checked against ref 7
  (Nightingale platform doc) for the unit. Single-source-preprint for the exact means → quality
  note. Already annotated `[cohort — PREPRINT, not peer-reviewed]`.

Both are admissible per the whitelist (mdpi.com Tier 1 lower-trust; medrxiv.org Tier 1 preprint)
and the prompt's guidance ("a number resting SOLELY on a preprint is a quality note, WARN-worthy if
load-bearing, not auto-HALT"). No above-floor `number-not-found` / `quote-not-found` →
corpus_scoping verdict = PASS with WARN.

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {"IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"}, "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"}, "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"}, "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"}, "IC-13": {"status": "WARN", "findings": ["heritability ~30% (h2=0.2971, Rg=0.4397) rests solely on ref6 MDPI open-access — load-bearing single-source quality note, number grep-verified, already flagged inline", "Nightingale unit means (1230/1216/1233/1236 umol/L) rest on ref10 medRxiv preprint — single-source-preprint quality note, cross-checked vs ref7 platform doc, already flagged inline"]}},
  "population_mismatch": {"verdict": "PASS", "checked_citations": 13},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 13, "largest_cluster_count": 3, "share": 0.23, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 79, "claims_failed": []},
  "halt_reasons": [],
  "warnings": ["IC-13: heritability single-source open-access (MDPI ref6)", "IC-13: Nightingale unit means single-source preprint (medRxiv ref10)"],
  "iterations": 1
}
```
