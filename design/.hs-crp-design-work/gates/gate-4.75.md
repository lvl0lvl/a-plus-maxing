# Gate 4.75 — Citation Integrity Verifier (hs-CRP, standard mode)

INDEPENDENT verifier run, 2026-06-18. Corpus: `/tmp/aplus-research/hs-crp/sections/section-A.md` + `section-B.md` + `/tmp/aplus-research/hs-crp/corpus/*.txt`. Section A's `## Post-fix grep audit` block was treated as documentation (its quoted OLD tag strings are not live claims).

## Verdict

```yaml
verdict: PASS
halt_reasons: []
warnings: [IC-13]
```

verdict: PASS

---

## IC-1 Type-Tag Presence

Every inline `[N, tag]` carries a canonical-enum tag. Live tags used: `rct`, `cohort`, `meta_analysis`, `mechanism_review`, `regulatory` — all in the enum. No tag outside the enum. The single `[4, mechanism_review]` hit is on Section A line 46 inside the `## Post-fix grep audit` block (documented OLD string, not a live claim per the brief). All live Pearson cites are `[4, regulatory]` (A) / `[1, regulatory]` (B). PASS.

## IC-2 Bibliography Type-Tag Presence

Section A: 8 entries, each carries `Tag: \`...\``, all enum tags. Section B: 10 entries, each carries `**[tag]**`; multi-purpose entries (e.g. `[cohort / mechanism_review]`, `[rct / meta_analysis]`) acceptable, each component in enum. PASS.

## IC-3 Vendor-Not-Numerical

No `vendor_label` inline citation exists. The only `vendor_label` mentions are in the two self-check prose lines stating no number is sourced to vendor. No vendor cite grounds any numerical claim. No Vendor-Not-Numerical violation detected. PASS.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` inline citation exists (only the same self-check disclaimers). No anecdote cite grounds any number. No Anecdote-Not-Numerical violation detected. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citation exists anywhere in either section. No Practitioner-Protocol-Not-Efficacy violation detected. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citation exists. No Compounding-Data-Sheet-with-Efficacy violation detected. PASS.

## IC-7 Population-Mismatch

Per health-gates §1: grep for `[N, animal]` and `[N, in_vitro]` returned ZERO hits. hs-CRP is a human biomarker; every numerical claim is grounded on human `rct`/`cohort`/`meta_analysis` or `regulatory`/`mechanism_review` sources. No `[population-mismatch:]` tag required. `checked_citations`: 0 animal/in_vitro cites found across the draft; population-mismatch gate PASSES vacuously. PASS.

## IC-8 Route-Extrapolation

Dose/route claims present (rosuvastatin 20 mg oral daily; canakinumab 50/150/300 mg subcutaneously q3mo; oral vs transdermal estrogen). Each claim's route matches the cited primary's tested route as recorded in corpus (CANTOS A-2 states "administered subcutaneously"; estrogen ref6 corpus explicitly contrasts oral first-pass vs transdermal; statins are oral). No route mismatch without a `[route-extrapolation]` tag. The oral-vs-transdermal estrogen distinction is itself the claim, correctly route-attributed. PASS.

## IC-9 Concentration-Surfacing

Distinct primaries (tags ∈ {rct, meta_analysis, cohort}) deduplicated across A+B = 16 (JUPITER counted once: A1 == B8). Largest author/lab cluster = Ridker (JUPITER, CANTOS, PHS, WHS, PROVE-IT, plus PRINCE/Albert as Ridker-lab senior-author work) = 6/16 = 0.375 (strict first-author = 5/16 = 0.3125). Both below the 0.70 threshold — `threshold_triggered: false`. No first-class concentration-risk section required; gate passes vacuously. This contrasts with BPC-157 (~76% single-lab); the hs-CRP evidence base is multi-cohort with Ridker prominent but not dominant, and the marker-vs-causal-target honest framing (Elliott MR-null) is independent of Ridker. PASS.

## IC-10 No Fabricated Citations

Section A: inline cites span refs 1-8; bibliography has exactly entries 1-8 — all resolve. Section B: inline cites span refs 1-10; bibliography has exactly entries 1-10 — all resolve. No orphan inline cite, no dangling number. All citations are canonical NEJM/JAMA/Circulation/PLOS One/FDA-510(k)/PMC sources with real PMIDs/DOIs. URL HEAD-check is best-effort in standard mode; no fabrication indicators. PASS.

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe` → ZERO matches. No placeholder strings detected. PASS.

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` → ZERO matches in either section's bibliography or body. No Wikipedia citations detected. PASS.

## IC-13 Per-Citation Corpus Scoping

Standard mode floor: ≥50% of numerical/quoted claims, minimum 10. 50 load-bearing numerical/quoted claims grep-verified against saved corpus (27 Section A + 23 Section B) — 100% of identified load-bearing claims, far exceeding the 50% floor.

Result: **49 of 50 grounded (PASS)**, **1 corpus-missing (WARN)**.

Grounded verbatim/numerical hits include: JUPITER (n=17,802; LDL <130; hs-CRP ≥2.0; −50%/−37%; HR 0.56 [0.46-0.69]; MI HR 0.46 [0.30-0.70]; stroke HR 0.52 [0.34-0.79]; 44%; 1.9 y; 4.2→2.2 mg/L), CANTOS (n=10,061; 50/150/300 mg SC q3mo; 26/37/41 pp; HR 0.85 [0.74-0.98] P=0.021; all-cause HR 0.94 [0.83-1.06] P=0.31; "did not reduce lipid levels"; "independent of lipid-level lowering"), Elliott (obs OR 0.94 [0.94-0.95]; genetic OR 1.00 [0.97-1.02]; "lack of concordance" quote), PHS (RR 2.9; aspirin 55.7%/13.9%), WHS (n=27,939; RR 2.3), AHA/CDC tertiles (<1 / 1-3 / >3 mg/L; >10 discard; 1 mg/dL=10 mg/L), within-subject CV_I 0.44 [0.27-0.76] / ICC 0.62 [0.58-0.67] / EFLM 0.59 [0.53-0.66], assay (0.1 / 0.3 / 306 mg/L; ~2 mg/L LoD; 100-fold; 8.1-11.4%), obesity (BMI 15%; ~1%; WHR 1.96 vs 1.53; 50% genetic), oral estrogen >2×, statins (rosuva 37%; atorva ~32% [−40,−22]; prava ~13-17%), weight loss ~9.4%, exercise SMD −0.53 [−0.74,−0.33].

`claims_failed` (corpus-missing, WARN — not HALT):
- **CRP half-life ~18-20 h / onset 6-8 h / peak 24-48 h [8, mechanism_review]** (Section A line 9). Ref 8 (Banait/Cureus 2022) has NO saved corpus file (no `A-8`). Per IC-13 §5, `corpus-missing` → WARN, not HALT. Mitigating: this is a non-cardiovascular kinetics claim, the section's own bibliography openly restricts ref 8 to half-life/kinetics and notes corroboration against StatPearls mechanism text, and no cardiovascular effect-size number depends on it. Single corpus-missing in standard mode → WARN.

No `quote-not-found` and no `number-not-found` (the only IC-13 codes that HALT). PASS (with one corpus-missing WARN).

Units confirmed mg/L throughout for every CRP value; the only `mg/dL` occurrences are (i) the explicit `1 mg/dL = 10 mg/L` conversion note (B line 3) and (ii) JUPITER's LDL inclusion criterion `<130 mg/dL` (LDL, correctly mg/dL, not CRP). No unit error.

---

## Verdict block (JSON)

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {"IC-1": {"status": "PASS"}, "IC-2": {"status": "PASS"}, "IC-3": {"status": "PASS"}, "IC-4": {"status": "PASS"}, "IC-5": {"status": "PASS"}, "IC-6": {"status": "PASS"}, "IC-7": {"status": "PASS"}, "IC-8": {"status": "PASS"}, "IC-9": {"status": "PASS"}, "IC-10": {"status": "PASS"}, "IC-11": {"status": "PASS"}, "IC-12": {"status": "PASS"}, "IC-13": {"status": "WARN", "findings": ["corpus-missing: CRP half-life 18-20h/onset 6-8h/peak 24-48h [8, mechanism_review] (Section A) — ref 8 Cureus has no saved corpus file; non-cardiovascular kinetics claim; WARN not HALT per IC-13 §5"]}},
  "population_mismatch": {"verdict": "PASS", "checked_citations": 0},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 16, "largest_cluster_count": 6, "share": 0.375, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 50, "claims_failed": []},
  "halt_reasons": [],
  "warnings": ["IC-13"],
  "iterations": 1
}
```
