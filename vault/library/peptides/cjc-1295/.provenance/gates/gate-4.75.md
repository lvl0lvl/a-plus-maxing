# Gate 4.75 — Citation Integrity Verifier (CJC-1295 deep-research report)

Corpus: `sections/section-A.md` … `section-F.md` + `rubric.md`. Mode: deep (efficient calibration, judge bar 92). Iterations: 1.

Load-bearing citations spot-verified live via WebFetch (PubMed / ClinicalTrials.gov API / govinfo.gov / PMC / BSCG). Mechanical greps run over all six section bodies.

---

## IC-1 Type-Tag Presence

Every inline citation carries a tag from the canonical enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). Grep of all backtick-form and bracket-form tags returned only enum members: `rct`(11), `mechanism_review`(40), `regulatory`(39), `animal`(13), `cohort`(8), `practitioner_protocol`(8), `in_vitro`(2), `anecdote_aggregate`(2), `vendor_label`(1) backtick form; plus bracket-form `[compounding_data_sheet]`(10), `[vendor_label]`(7), `[rct]`(8), `[animal]`(4), `[in_vitro]`(2), `[regulatory]`(3). No out-of-enum tag found. No type-tag violations detected.

## IC-2 Bibliography Type-Tag Presence

All bibliography entries across A–F carry a `[tag]`/`` `tag` `` annotation from the enum (some with dual tags, e.g. `regulatory`/`anecdote_aggregate` on D[4], `animal` + `in_vitro` on C[1]). No untagged bibliography entries detected.

## IC-3 Vendor-Not-Numerical

Two `vendor_label` cites ground numbers: F[4] (~1–2 mg SC once weekly) and F[5] (reconstitution math 2 mg→1 mg/mL etc.). Both are route/frequency convention and reconstitution math — the permitted uses — and are explicitly labeled "NOT an efficacy claim" / "math only, no purity/efficacy assurance." No `vendor_label` cite grounds an efficacy, AE-rate, or therapeutic-dose-efficacy claim. No IC-3 violation detected.

## IC-4 Anecdote-Not-Numerical

One `anecdote_aggregate` cite: D[4] ("eleventh injection" detail), explicitly "(qualitative lead only; no numerical death rate is or can be derived from it)." No numerical AE rate, dose, or effect size grounded on anecdote. No IC-4 violation detected.

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` cites ground only: contraindications/monitoring/stopping criteria (D L44-46), DAC/no-DAC dosing conventions and gray-market labeling (E L5/L33, F). None is the sole source of an efficacy claim. Efficacy/AE rates (KIMS rates, cancer SIR 0.92) are carried by the `cohort` Johannsson cite D[6]. Section F explicitly declined to assert any `practitioner_protocol` claim for lack of attributable name+venue+date. No IC-5 violation detected.

## IC-6 Compounding-Data-Sheet-with-Efficacy

`compounding_data_sheet` cites (F[1], F[3], and the dosing-convention lines) ground dose form, strength, reconstitution, and dose/route/cycle convention only — no efficacy claim. No IC-6 violation detected.

## IC-7 Population-Mismatch (health-gates §1)

Animal numerical claims checked: A L29 (">72 h in rats"), A L47 (Alba, GHRH-knockout mouse, dosing-interval only), C L11/L20/L21 (rat conjugate — "~4-fold GH AUC", "~15 min", ">24 h", ">72 h"), C L26 ("2 µg... GHRHKO mice"), D L38 (Rittmaster, rat anterior pituitary cells). In every case the species name appears in the same sentence/clause as the number and the cited animal source is the sole source for that claim → health-gates §1 override (species-is-subject) applies; explicit `[population-mismatch:]` is optional. No human dose/AE/efficacy number is grounded on an animal source without species context. No n was invented anywhere — Jette and Alba per-arm n is honestly NOT asserted (paywalled Methods). No IC-7 violation detected.

## IC-8 Route-Extrapolation

All dose claims (human Teichman SC; rat/mouse Jette/Alba SC) keep route consistent between the claim and the cited primary's tested route. No dose value tested via one route is asserted for a different route. No `[route-extrapolation]` tag is required and none is missing. No IC-8 violation detected.

## IC-9 Concentration-Surfacing (health-gates §3)

Single-lineage share ≥ 70% (see concentration_audit below). The report surfaces this as a first-class finding under the top-level heading `### Concentration audit (Sikiric-style)` in Section C, with an explicit `FLAG (first-class finding): CONCENTRATION ALERT — meets the ≥70% threshold`, appearing before any indication subsection. Surfacing requirement satisfied. No IC-9 violation detected.

## IC-10 No Fabricated Citations

Inline-to-bibliography resolution: every inline `[N]` in each section resolves to a bibliography entry; no orphan inline cites; no orphan bibliography entries (A 1-7, B 1-6, C 1-4, D 1-7, E 1-10, F 1-6 all match). Load-bearing identifiers spot-verified live:
- Teichman 2006, PMID 16352683 — VERIFIED (first author Sam L Teichman, JCEM 2006; half-life 5.8–8.1 d; GH 2–10×; IGF-1 1.5–3× — all match).
- Jetté 2005, PMID 15817669 — VERIFIED (Lucie Jetté, Endocrinology 2005; "tetrasubstituted form of hGRF(1-29) with N-epsilon-3-maleimidopropionamide... lysine"; 4-fold GH; >72 h; rat — all match).
- Alba 2006, PMID 16822960 — VERIFIED (Maria Alba, AJP-Endo 2006; GHRH-knockout mouse; "2 microg of CJC-1295 at intervals of 24, 48, and 72 h" — all match).
- NCT00267527 — VERIFIED via ClinicalTrials.gov API v2 (CJC-1295, ConjuChem sponsor, HIV-associated visceral obesity, Phase 2, enrollment 120, status Terminated, no results posted — all match).
- FR Doc 2026-07361 (FR-2026-04-16) — VERIFIED via govinfo.gov (PCAC July 23–24 2026 meeting notice; lists the peptides under review; CJC-1295 NOT mentioned anywhere — matches the report's load-bearing absence claim).
- FR Doc 2024-24828 (FR-2024-10-25) — VERIFIED via govinfo.gov (Dec 4 2024 PCAC notice; lists all five CJC-1295 forms: free base, acetate, DAC free base, DAC acetate, DAC TFA — matches).
- WADA S2.2.4 naming — VERIFIED via BSCG source E[1] (CJC-1295 explicitly listed under S2.2.4 growth-hormone-releasing factors, prohibited at all times; FDA not approved — matches).
- Feng 2018, PMC5928873 — VERIFIED (Theranostics 2018; MPA→albumin Cys34 thiosuccinimide; prolonged half-life; anti-tumor — matches the chemistry quote in A).

No fabricated, wrong-PMID, or non-resolving citation detected. (URL HEAD-checks not exhaustively run for every non-load-bearing entry; spot-verification of all load-bearing primaries passed.)

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe` → no matches. No placeholder strings detected.

## IC-12 No Wikipedia Citations

Grep for `wikipedia` / `wiki` across all section bodies: matches are (a) self-check prose lines asserting "No Wikipedia citations" (B L83, C L59, E L58); (b) D L26 prose "Any wiki rendering..." (figure of speech, not a citation); (c) Section F L23/L37 which EXPLICITLY EXCLUDE the Russian SportWiki entry as a source ("a wiki — HALT, treated like Wikipedia and excluded as a source"). The rubric's self-check line containing the word "Wikipedia" is a check directive, not a citation. No Wikipedia or SportWiki citation appears in any bibliography. No real Wikipedia citation detected.

## IC-13 Per-Citation Corpus Scoping

Load-bearing numerical/quoted claims grep-verified against fetched corpora (deep mode): Teichman GH 2–10× / IGF-1 1.5–3× / half-life 5.8–8.1 d (matched in abstract); Jette ~4-fold GH AUC / >72 h / "tetrasubstituted... maleimidopropionamide... lysine" verbatim (matched); Alba "2 µg... 24, 48, 72 h" verbatim (matched); Ionescu 7.5-fold / 46% / 45% quote (consistent with PMID 17018654 abstract framing); Feng Cys34 thiosuccinimide quote (matched verbatim). Regulatory numeric/scope claims (FR-Doc peptide slates, NCT enrollment 120 / Terminated, five CJC-1295 nominated forms) all matched against primaries. CORPUS-MISSING (WARN, not HALT): exact per-arm animal n for Jette 2005 and Alba 2006 sits behind the OUP/AJP paywalled Methods — the report honestly does NOT assert an n for either (enumerates design instead), so there is no number-not-found violation. No `quote-not-found` or `number-not-found` failure detected.

## Population-Mismatch Gate (health-gates §1)

verdict PASS. checked_citations: 6 animal/in_vitro numerical contexts; flagged: none (all satisfy the species-is-subject override; no invented n; no animal number cross-attributed to a human dose/AE/efficacy claim).

## Concentration-Audit Gate (health-gates §3)

total_primaries (enumerated efficacy/PK preclinical primaries, Section C table) = 2: Jette 2005 (animal+in_vitro, all-ConjuChem) and Alba 2006 (animal mouse, academic-led w/ ConjuChem co-author supplying compound). Largest cluster = ConjuChem-touched = 2/2 = 1.00 (inclusive reading; stricter author-lineage reading = 0.50). Threshold 0.70 triggered = true. Surfaced as first-class finding "Concentration audit (Sikiric-style)" with explicit CONCENTRATION ALERT FLAG before any indication subsection. verdict PASS.

## Corpus-Scoping Gate

verdict PASS (WARN-noted). claims_checked across load-bearing numeric/quoted/scope claims; claims_failed: none. Two paywalled per-arm-n items are corpus-missing WARN, correctly handled by non-assertion in the draft (not HALT).

## Verdict

verdict: PASS

```yaml
verdict: PASS
halt_reasons: []
warnings:
  - IC-13: per-arm animal n for Jette 2005 and Alba 2006 is paywalled (OUP/AJP Methods) — corpus-missing; report correctly does not assert an n (WARN, not HALT).
  - IC-10: exhaustive URL HEAD-checks not run for every non-load-bearing bibliography entry; all load-bearing primaries spot-verified live and resolved.
  - WADA primary text (wada-ama.org) is JS-rendered and was not directly machine-fetchable; S2.2.4 CJC-1295 naming corroborated via the cited BSCG source and is consistent with the report's primary-text citation [E6].
```

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {"status": "PASS", "count_checked": 124, "count_flagged": 0},
    "IC-2": {"status": "PASS"},
    "IC-3": {"status": "PASS", "count_checked": 2, "count_flagged": 0},
    "IC-4": {"status": "PASS", "count_checked": 1},
    "IC-5": {"status": "PASS", "count_checked": 5, "count_flagged": 0},
    "IC-6": {"status": "PASS", "count_checked": 4},
    "IC-7": {"status": "PASS", "count_checked": 6, "count_flagged": 0},
    "IC-8": {"status": "PASS"},
    "IC-9": {"status": "PASS"},
    "IC-10": {"status": "PASS", "count_checked": 8, "count_flagged": 0},
    "IC-11": {"status": "PASS"},
    "IC-12": {"status": "PASS", "count_checked": 7, "count_flagged": 0},
    "IC-13": {"status": "WARN"}
  },
  "population_mismatch": {"verdict": "PASS", "checked_citations": 6, "flagged_citations": []},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 2, "largest_cluster_name": "ConjuChem", "largest_cluster_count": 2, "share": 1.0, "threshold_triggered": true, "surfaced_section_heading": "Concentration audit (Sikiric-style)"},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 18, "claims_failed": []},
  "halt_reasons": [],
  "warnings": [
    "IC-13: per-arm animal n for Jette 2005 and Alba 2006 paywalled (OUP/AJP Methods) — corpus-missing; report correctly asserts no n.",
    "IC-10: exhaustive HEAD-checks not run for every non-load-bearing entry; all load-bearing primaries spot-verified and resolved.",
    "WADA S2.2.4 primary text JS-rendered; CJC-1295 naming corroborated via cited BSCG source, consistent with report's primary citation."
  ]
}
```
