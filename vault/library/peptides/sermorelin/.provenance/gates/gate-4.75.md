# Gate 4.75 — Citation Integrity Verifier (Sermorelin)

Mode: deep. Corpus: sections A–F. Iterations: 1.
Scope: IC-1…IC-13 + population_mismatch + concentration_audit + corpus_scoping.

## IC-1 Type-Tag Presence

Every inline citation carries a canonical type-tag. Tally across the corpus:
`regulatory` ×78, `mechanism_review` ×26, `cohort` ×10, `rct` ×6, `open_label` ×5,
`anecdote_aggregate` ×1. All six tags are in the enum. No bare/unknown inline tags.
The token `[dose/population-extrapolation]` appears ×5 (Section D) — this is an
*extrapolation annotation*, not a type-tag (it qualifies cross-class tesamorelin/
GH-replacement claims), and always co-occurs with a canonical `[regulatory]`/`[cohort]`/
`[rct]` type-tag on the same claim. Not an IC-1 violation. PASS.

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry in all six sections carries a `[<tag>]` / `type-tag:` annotation
from the enum (e.g., A[1] regulatory, A[2] mechanism_review, B[6] open_label, C[2] rct,
D[4] cohort, F[2] compounding_data_sheet, F[7] non-English review). Multi-purpose entries
(D[1] `[cohort / mechanism_review]`) are within spec. PASS.

## IC-3 Vendor-Not-Numerical

No inline `[vendor_label]` tag appears anywhere in the corpus. Vendor/compounding numerics
in Section F (concentrations, reconstitution draws) are tagged `compounding_data_sheet` /
`vendor_label (math only)` and confined to reconstitution arithmetic, vial size, and storage
convention — never efficacy/AE/dose-efficacy. PASS.

## IC-4 Anecdote-Not-Numerical

Exactly one `[anecdote_aggregate]` cite (Section E, gray-market supply channel). It is paired
with `[regulatory]` and grounds a purely qualitative statement (existence of a "not-for-human-
use" online market and its identity/purity/sterility hazards) — no numerical AE rate, dose, or
effect size in the sentence. PASS.

## IC-5 Practitioner-Protocol-Not-Efficacy

`practitioner_protocol` cites (Section F: Strive, Houston Men's Clinic, Drip Hydration, GHRP
co-admin) ground only dose/route/cycle/admin conventions. Section F states explicitly: "no
efficacy or adverse-event numbers in this section are grounded on practitioner, vendor, or
compounding sources." No practitioner cite is the sole source of an efficacy claim. PASS.

## IC-6 Compounding-Data-Sheet-with-Efficacy

`compounding_data_sheet` cites (Empower, Strive, Olympia) ground only dose-form strengths,
admin conventions, and reconstitution math. No efficacy claim rests on a data sheet; the
section routes efficacy explicitly to the primary-literature sections. PASS.

## IC-7 Population-Mismatch

No `[animal]` or `[in_vitro]` inline tags exist in the corpus — the sermorelin evidence base
is entirely human (rct/cohort/open_label), regulatory, or mechanism_review. The §1 trigger
(numerical claim citing animal/in_vitro) never fires. Separately, the report exceeds the
minimum by carrying population labels on every efficacy figure: pediatric-GHD (Thorner 1996,
Prakash & Goa), idiopathic-short-stature-NOT-GHD (Kirk 1994, explicitly flagged), and
aging-adult (Corpas, Vittone, Khorram, Vitiello — each tagged "aging adults"). Cross-class
tesamorelin/GH-replacement claims carry `[dose/population-extrapolation]`. PASS.

## IC-8 Route-Extrapolation

Dose claims and their cited primaries' routes agree: pediatric SC (Thorner/Geref 30 µg/kg SC),
diagnostic IV (Ranke/label 1 µg/kg IV), aging-adult SC (Corpas/Vittone/Khorram/Vitiello SC),
compounded SC nightly (Section F). Route is stated in each citation/label. No SC↔IV↔oral
mismatch lacking a tag. PASS.

## IC-9 Concentration-Surfacing

See concentration_audit. Single-lineage share = 50% (2/4 primaries, Johns Hopkins/NIH), below
the 0.70 threshold. Threshold not triggered → no mandatory first-class concentration section
required. The report nonetheless surfaces the lineage analysis as a named "Concentration audit"
subsection in Section C, and explicitly notes the mis-credit-driven hazard (folding in
tesamorelin/GHRH-1,44 work would push the UW/Merriam share toward/over 70%). PASS.

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry. Load-bearing identifiers spot-verified
via PubMed/Europe PMC/govinfo:

- Prakash & Goa 1999, PMID **18031173** → BioDrugs 1999;12(2):139-157 — RESOLVES (Europe PMC core).
- Corpas 1992, PMID **1379256** → JCEM 1992;75(2):530-5 — RESOLVES; abstract matches claims.
- Vittone 1997 → Metabolism 1997;46(1):89-96, PMID **9005976** — RESOLVES (report omitted PMID; author/journal/year/title confirmed).
- Khorram/Laughlin/Yen 1997 → JCEM 1997;82(5):1472-9, PMID **9141536** — RESOLVES; abstract matches.
- Vitiello/Moe/Merriam 2006, PMID **16399214** → Neurobiol Aging 2006;27(2):318-23 — RESOLVES.
- Thorner/Geref International Study Group 1996, PMID **8772599** → JCEM 1996;81(3):1189-96 — RESOLVES.
- Baker 2012, PMID **22869065** → Arch Neurol 2012 — RESOLVES (tesamorelin; see guard below).
- Geref (sermorelin acetate) FDA label via RxList mirror — RESOLVES; label numerics confirmed
  (11–12 min t½, 5–20 min Tmax, 1-in-6 injection-site, 350 exposed/3 d/c, 6.5% hypothyroidism).
- FR Doc **2013-04827** (3/4/2013) — RESOLVES via govinfo primary; title, NDA 20-443 (1997-09-26),
  NDA 19-863 (1990-12-28), "not withdrawn for safety/effectiveness" all confirmed.
- FR Doc **2026-07361** (4/16/2026 PCAC notice) — RESOLVES via govinfo; seven peptides confirmed;
  sermorelin NOT named anywhere (load-bearing absence confirmed).
- WADA S2.2.4 — sermorelin's prohibited-at-all-times GHRH-analogue status corroborated.

No fabricated, non-resolving, or unattributable load-bearing identifier found.
WARN: FederalRegister.gov direct-fetch returns an access redirect (unblock wall); the govinfo
primary record resolves the content — this is an access wall, not a fabrication. Count flagged
for fabrication = 0. PASS.

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some reports`,
`research suggests`, `experts believe` → no matches in any section. PASS.

## IC-12 No Wikipedia Citations

No `wikipedia.org` / SportWiki URL appears in any of the six bibliographies. The only mention of
Wikipedia (Section F, line 29) is an explicit EXCLUSION note — the Russian-language "Соматолиберин"
Wikipedia entry was *excluded* as a HALT source. An exclusion note is not a citation. Spot URL
audit of all bibliography links confirms zero Wikipedia/wiki sources cited. PASS.

## IC-13 Per-Citation Corpus Scoping

Load-bearing numerical/scope claims grep-verified against retrieved primary abstracts:

- Corpas 1992: "0.5 mg and 1 mg SC twice daily, 14 days, n=10 old (~68y)/n=9 young, reverses
  GH+IGF-1 decrease" — MATCHES abstract.
- Vittone 1997: single nightly GHRH(1-29), elderly men — author/journal/scope MATCH.
- Khorram 1997: "10 µg/kg SC nightly, 16 wk, 10 women/9 men 55-71y, LBM/insulin/libido in MEN
  ONLY, skin thickness BOTH sexes" — MATCHES abstract verbatim on the sex-restriction and dose.
- Vitiello 2006: "89 healthy older adults ~68y, 6 mo daily GHRH, fluid-intelligence gains" — MATCHES.
- Thorner 1996: pediatric GHD, once-daily SC growth acceleration — MATCHES.
- Geref label numerics + FR 2013-04827 NDA facts + FR 2026-07361 peptide list — MATCH primary.

No quote-not-found, no number-not-found, no paraphrase-no-token-match.
WARN (corpus-missing, non-HALT): Khorram and Vittone full texts are paywalled (OUP / Metabolism);
verified via Europe PMC abstracts (abstract-only verified). FederalRegister.gov direct URL hits an
access wall; resolved via govinfo primary. Per IC-13/corpus_scoping policy, paywall = WARN, not HALT.
PASS.

## Tesamorelin-Miscredit Guard

CONFIRMED HELD. Baker 2012 (PMID 22869065) abstract states verbatim: "Participants
self-administered daily subcutaneous injections of **tesamorelin** (Theratechnologies Inc),
a stabilized analog of human GHRH (1 mg/d)." Section C cites Baker 2012 **only** in the
"Critical mis-credit flags" block as tesamorelin and explicitly says "Do not credit to
sermorelin." Friedman 2013 (tesamorelin) and the GHRH-1,44-amide walking/stair/visceral-fat
results are likewise demarcated away from sermorelin. No tesamorelin/CJC-1295/GHRH-1,44 study
is miscredited to sermorelin anywhere in §C (or §A/D, which reference tesamorelin only as a
structurally-distinct class comparator with explicit `[rct]`/`[regulatory]` + extrapolation tags).

## Verdict

verdict: PASS
halt_reasons: none
warnings: IC-10 (FederalRegister.gov access-wall — resolved via govinfo primary), IC-13 (Khorram/Vittone paywalled — verified abstract-only via Europe PMC)

```json
{
  "phase": "4.75",
  "verdict": "PASS",
  "iterations": 1,
  "ic_checks": {
    "IC-1": {
      "status": "PASS",
      "count_checked": 126,
      "count_flagged": 0
    },
    "IC-2": {
      "status": "PASS"
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-4": {
      "status": "PASS",
      "count_checked": 1
    },
    "IC-5": {
      "status": "PASS",
      "count_checked": 4,
      "count_flagged": 0
    },
    "IC-6": {
      "status": "PASS",
      "count_checked": 3
    },
    "IC-7": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0
    },
    "IC-8": {
      "status": "PASS"
    },
    "IC-9": {
      "status": "PASS"
    },
    "IC-10": {
      "status": "PASS",
      "count_checked": 11,
      "count_flagged": 0
    },
    "IC-11": {
      "status": "PASS"
    },
    "IC-12": {
      "status": "PASS",
      "count_checked": 29,
      "count_flagged": 0
    },
    "IC-13": {
      "status": "PASS"
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 0,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 4,
    "largest_cluster_name": "Johns Hopkins / NIH (Blackman lineage)",
    "largest_cluster_count": 2,
    "share": 0.5,
    "threshold_triggered": false,
    "surfaced_section_heading": "Concentration audit (Section C)"
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 11,
    "claims_failed": []
  },
  "halt_reasons": [],
  "warnings": [
    "IC-10: FederalRegister.gov direct fetch returns access redirect; resolved via govinfo primary record (not a fabrication)",
    "IC-13: Khorram 1997 and Vittone 1997 full text paywalled; numerical claims verified abstract-only via Europe PMC (corpus-missing WARN, not HALT)"
  ]
}
```
