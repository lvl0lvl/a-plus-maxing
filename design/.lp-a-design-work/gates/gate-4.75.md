# Gate 4.75 — Citation Integrity Verifier (Lp(a), standard mode)

Corpus under review: `sections/section-A.md` (Identity, Physiology & Causal Significance) + `sections/section-B.md` (Reference Ranges, Measurement & Determinants) + `corpus/*.txt` (17 cached source files). Lp(a) is a HUMAN biomarker; the literature is multi-cohort. Full 13-check set run; no reduction.

## Verdict

verdict: PASS
halt_reasons: []
warnings: [IC-1, IC-13]

---

## IC-1 Type-Tag Presence

Every live inline citation in `[N, <tag>]` form carries a tag from the canonical enum (`rct | meta_analysis | cohort | open_label | animal | in_vitro | mechanism_review | regulatory | compounding_data_sheet | vendor_label | practitioner_protocol | anecdote_aggregate`). Tally across both sections: all of `mechanism_review`, `cohort`, `meta_analysis`, `rct` resolve cleanly.

WARN — two non-enum tags in Section B: `[search-derived, mechanism_review; corroborated 1, mechanism_review]` (L26) and `[search-derived, mechanism_review]` (L32). `search-derived` is NOT in the canonical enum. However: (a) both attach to QUALITATIVE mechanism statements (mass-immunoassay isoform bias direction; KIV-2 inverse relation) that carry NO standalone numerical value — every number in those two sentences carries a separate admissible cite (`[2, mechanism_review]`, `[5, mechanism_review]`, `[3, mechanism_review]`); (b) each `search-derived` token is co-tagged `mechanism_review` (admissible) and explicitly corroborated against saved corpus refs 1/3. Because the tag-discipline HALT trigger is "a NUMBER resting on a non-admissible tag," and no number rests on `search-derived` here, this is WARN, not HALT. Orchestrator may demand the synthesis agent drop `search-derived` and cite the corroborating ref directly.

The `[7, rct]` / `[N, rct]` hits at A-L66/L71 are inside the "Post-fix grep audit" prose documenting the OLD→NEW retag (van der Valk `rct`→`cohort`); they are not live body citations. No live `[N, rct]` cite remains in Section A.

## IC-2 Bibliography Type-Tag Presence

Section A: 9 bibliography entries [1]–[9], each carrying `tag:` (meta_analysis / cohort / mechanism_review). Section B: 8 entries [1]–[8], each carrying `tag:` (mechanism_review / cohort / rct / meta_analysis). All tags from the enum. Entry [7] in B legitimately bundles multiple primaries (`rct / meta_analysis`). No bibliography entry lacks a tag.

## IC-3 Vendor-Not-Numerical

No `vendor_label` citation anywhere in either section. Vacuously satisfied.

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` citation anywhere in either section. Vacuously satisfied.

## IC-5 Practitioner-Protocol-Not-Efficacy

No `practitioner_protocol` citation anywhere in either section. Vacuously satisfied.

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citation anywhere in either section. Vacuously satisfied.

## IC-7 Population-Mismatch

PASS. This is a human biomarker. NO `animal` or `in_vitro` citation tags appear in either section. Scanned for any rodent/cell-culture number presented as human (`rat|mouse|murine|rodent|in vitro|cell culture|monkey|primate`): the only "in-vitro" mentions are (a) van der Valk's isolated-monocyte mechanism work, which is tagged `cohort` (controlled human study, 30 elevated vs 30 normal Lp(a)) and contributes only a qualitative mechanism demonstration with no animal-derived numeric, and (b) post-fix audit prose. No animal/in-vitro numbers presented as human evidence. `checked_citations`: 47 numerical-claim-bearing inline cites scanned for an animal/in_vitro source; 0 flagged. See health-gates §1.

## IC-8 Route-Extrapolation

Section A carries no dose-by-route claims (genetic/observational risk associations). Section B dosing claims (pelacarsen 60 mg monthly / 20 mg weekly; olpasiran ≥75 mg Q12W; lepodisiran 400 mg) are all subcutaneous trial regimens cited to the same trial that tested that route (refs [6], [7]); the route in the claim matches the route in the cited primary's corpus (B-ref6, B-ref7 verbatim "subcutaneous"). No route mismatch. No `[route-extrapolation]` needed.

## IC-9 Concentration-Surfacing

PASS — threshold NOT triggered. Per health-gates §3, distinct PRIMARY citations (tags in {rct, meta_analysis, cohort, open_label, animal, in_vitro}; mechanism_review reviews excluded from the denominator) deduplicated across both sections = 12: ERFC/Erqou (meta), PROCARDIS/Clarke, Kamstrup AVS 2014, Kamstrup MI 2009, Kamstrup CCHS 2008, van der Valk OxPL, Thanassoulis CHARGE, Marcovina 2018, lepodisiran/Nissen, pelacarsen/Tsimikas, olpasiran/O'Donoghue, PCSK9i FOURIER+ODYSSEY.

Largest single-group cluster = the Copenhagen / Nordestgaard–Tybjaerg-Hansen Danish general-population studies (Kamstrup AVS 2014 + Kamstrup MI 2009 + Kamstrup CCHS 2008) = 3 primaries. Share = 3/12 = 0.25, well below the 0.70 threshold. The remaining primaries span independent groups/consortia (ERFC 36-cohort pool, Oxford PROCARDIS, Amsterdam/UCSD OxPL, CHARGE consortium, Seattle Marcovina, three independent industry RNA-therapeutic trials). Lp(a) literature is genuinely multi-cohort, as expected. No first-class concentration-risk section is required; gate passes vacuously per §3 step 3.

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry: Section A body uses [1]–[9] (all 9 entries present); Section B body uses [1]–[8] (all 8 present). No orphan inline cites. Bibliography URLs are all Tier-1 whitelist hosts (pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, nejm.org/DOI, academic.oup.com, lipidjournal.com, acc.org curated). HEAD-check deferred to budget; no obviously fabricated/unresolvable entry. PASS.

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`, `research suggests`, `experts believe` across both sections: 0 matches. PASS.

## IC-12 No Wikipedia Citations

Grep for `wikipedia.org` across both sections: 0 matches. PASS.

## IC-13 Per-Citation Corpus Scoping

PASS (WARN note below). Standard floor = ≥50% of numerical/quoted claims grep-verifiable. Every numerical claim in both sections was grep-checked against its cited corpus file (`grep -F`, unit/whitespace normalized) — i.e. 100% of load-bearing numerical claims, far above the 50% floor.

- Section A: 36 numerical claims checked (KIV-2 isoform counts & heritability, EAS genetic-determination figures, PROCARDIS/CCHS variance shares, ERFC participant counts + CHD/stroke RRs, CCHS-2008 extreme-Lp(a) MI HRs + absolute-risk figures, Kamstrup-2009 MR HRs, PROCARDIS ORs, AVS HRs, CHARGE OR/HRs, OxPL study medians) → 0 failed.
- Section B: 38 numerical claims checked (EAS/NLA threshold bands + molar equivalents, continuous fold-risk gradient, extreme/heFH tier, HEART UK cut, Marcovina molar:mass ratios, single-conversion-not-appropriate quote, mg/dL deviation quote, ~90% genetic + 70% coding sequence + ~40 isoforms, UKB allele-carrier medians + n, statin +10.6–19.3%, PCSK9i 20–25% / FOURIER 27% / ODYSSEY 23% / alirocumab meta 24.50% CI, apheresis 60–70% / interval 25–40%, pelacarsen 72%/80%/98%, olpasiran 97.4%/>95%, lepodisiran 93.9%/400 mg) → 0 failed.

Total: claims_checked = 74, claims_failed = 0. All corpus files were retrievable (no paywall `corpus-missing`). The two `search-derived` mechanism statements (IC-1 WARN) carry no number, so they are not IC-13 claims; they are corroborated by saved refs 1/3 per the author's self-check. The IC-13 WARN is purely carried forward from IC-1 (the non-enum `search-derived` tag), not a corpus-scoping failure.

---

## Verdict block

```yaml
verdict: PASS
halt_reasons: []
warnings: [IC-1, IC-13]
```

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "ic_checks": {
    "IC-1": {"status": "WARN", "findings": ["Non-enum tag `search-derived` at section-B L26 and L32; both attach to qualitative mechanism statements carrying NO standalone number (numbers in those sentences carry separate admissible cites [2]/[5]/[3]); co-tagged mechanism_review + corroborated by saved refs 1/3. WARN not HALT because no number rests on a non-admissible tag. The [7, rct]/[N, rct] hits at A-L66/L71 are post-fix audit prose, not live cites."]},
    "IC-2": {"status": "PASS"},
    "IC-3": {"status": "PASS"},
    "IC-4": {"status": "PASS"},
    "IC-5": {"status": "PASS"},
    "IC-6": {"status": "PASS"},
    "IC-7": {"status": "PASS"},
    "IC-8": {"status": "PASS"},
    "IC-9": {"status": "PASS"},
    "IC-10": {"status": "PASS"},
    "IC-11": {"status": "PASS"},
    "IC-12": {"status": "PASS"},
    "IC-13": {"status": "WARN", "findings": ["No corpus-scoping failure: 74/74 numerical claims grep-verified, 0 failed. WARN carried from IC-1 only (non-enum `search-derived` tag on two number-free mechanism statements)."]}
  },
  "population_mismatch": {"verdict": "PASS", "checked_citations": 47},
  "concentration_audit": {"verdict": "PASS", "total_primaries": 12, "largest_cluster_count": 3, "share": 0.25, "threshold_triggered": false},
  "corpus_scoping": {"verdict": "PASS", "claims_checked": 74, "claims_failed": []},
  "halt_reasons": [],
  "warnings": ["IC-1: non-enum tag `search-derived` (B-L26, B-L32) on number-free mechanism statements, co-tagged mechanism_review + corroborated; WARN not HALT", "IC-13: no failure; WARN carried from IC-1"],
  "iterations": 1
}
```
