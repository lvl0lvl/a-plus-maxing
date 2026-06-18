# Gate 4.75 — Citation Integrity Verifier (BPC-157), final

Phase 4.75 final integrity gate. Full IC-1..IC-13 framework run across the five
synthesized sections (`section-{A,B,C,D,E}.md`) at iteration 3. Content checks
(type-tag canonicalization, vendor/anecdote-not-numerical, population/route
discipline, ~85% Sikiric concentration audit) had already cleared at iter-2; this
run executes the *complete* mechanical checklist and emits the schema-valid gate
scaffold for attest.

Canonical type-tag enum (ONLY): `rct, meta_analysis, cohort, open_label, animal,
in_vitro, mechanism_review, regulatory, compounding_data_sheet, vendor_label,
practitioner_protocol, anecdote_aggregate`.

---

## IC-1 Type-Tag Presence

All inline citations carry a tag from the canonical enum. Whole-corpus tag census
(`grep -ohE '\[[0-9]+,\s*[a-z_]+\]'`): `animal`×47, `mechanism_review`×43,
`regulatory`×21, `rct`×10, `in_vitro`×4, `open_label`×3, `practitioner_protocol`×2.
Every captured tag ∈ enum. No non-enum inline tags remain (iter-2 remaps
`registered-trial→rct`, `peer-reviewed-animal→animal`,
`primary-author-review→mechanism_review`, `animal/mechanism_review→animal` all
confirmed at 0 residual hits in live content). **No untagged citations detected.**
→ PASS

## IC-2 Bibliography Type-Tag Presence

Every bibliography entry across all five sections carries a `type:`/`Type-tag:`
annotation drawn from the enum (A:9, B:7, C:14, D:9, E:4 entries). Section D [4]
(Hsieh 2017) legitimately carries a dual purpose annotated `animal + in_vitro`
(in-vivo rat arm + human endothelial cells) — permitted multi-tag form. No
bibliography entry lacks an enum tag. → PASS

## IC-3 Vendor-Not-Numerical

Only one `vendor_label` use in the corpus: Section E.4 reconstitution math
(`[vendor_label]`, L84): "10 mg vial reconstituted with 2 ml bacteriostatic water =
5 mg/ml, so 0.1 ml = 500 µg." Reconstitution/dilution arithmetic (tokens mL,
mg/ml present) — within the permitted grounds (reconstitution math, vial size). No
`vendor_label` cite grounds an efficacy, AE-rate, or therapeutic-dose claim; the
section explicitly refuses vendor/forum half-life and bioavailability numbers.
**No vendor-grounded numerical claim detected.** → PASS

## IC-4 Anecdote-Not-Numerical

No `anecdote_aggregate` inline citation grounds any claim anywhere. The only
mentions (B.3 L29, D.6 L78) are negative assertions that anecdote/forum-level
reports are *not* used to ground any numerical AE rate. **No anecdote-grounded
numerical claim detected.** → PASS

## IC-5 Practitioner-Protocol-Not-Efficacy

Two `practitioner_protocol` inline cites, both Section D ref [7]
(GlobalRPH/McAuley): D.4 L55 grounds a contraindication convention (anticoagulant
co-use), co-cited with mechanism_review [2]; D.6 L76 grounds a *qualitative* AE
descriptor ("mild local injection-site reaction"), explicitly "no admissible
incidence rate." Neither grounds an effect size, response rate, or mechanism as
sole source. All efficacy/mechanism statements in those sentences are co-anchored to
Tier-1/2 sources. **No practitioner-protocol sole-source efficacy claim detected.**
→ PASS

## IC-6 Compounding-Data-Sheet-with-Efficacy

No `compounding_data_sheet` citations appear in any of the five sections (the tag
occurs only inside in-section enum-recital text, not as a citation). **Nothing to
check.** → SKIP-mode

## IC-7 Population-Mismatch

Per health-gates §1. All 47 `animal` + 4 `in_vitro` inline cites checked
(count_checked = 51). For every animal/in_vitro citation carrying a numerical token
on its sentence, a species word (rat / Sprague-Dawley / Wistar / dog / beagle /
rabbit / mouse / mice) or cell-system subject (human melanoma cell, rat Achilles
tendon fibroblasts, HUVEC) appears within the same sentence (<100 chars) — i.e., the
species/system *is* the subject, invoking the §1 override under which
`[population-mismatch:]` is optional. Mechanical confirmation: of all animal-cited
sentences bearing a dose/effect numerical token, **zero** lack a co-located species
word. Background/Mechanism/preclinical contexts where population is explicit.
**No population-mismatch-unflagged claim detected.** → PASS

## IC-8 Route-Extrapolation

The only cross-route/cross-species inference surface is the PK section (E). Both
extrapolation surfaces are explicitly flagged: E.2 L50 `[route-extrapolation]`
(rat/dog IV+IM µg/kg cannot convert to human oral/SC), and E.4 L81
`[route-extrapolation]`/`[species-extrapolation]` (authors' BSA allometric scaling
does not establish a human dose). Section C reports routes as tested with no
extrapolation performed (L3). No dose claim asserts a route different from its cited
primary's tested route without the flag. **No route-extrapolation-unflagged claim
detected.** → PASS

## IC-9 Concentration-Surfacing

Per health-gates §3. Single-lab (Sikiric/Zagreb) share = 11/13 in-vivo efficacy
primaries ≈ 0.846 (≥ 0.70 threshold triggered). Section C surfaces this as a
first-class top-level heading `## Concentration audit` (L72); single-lab dominance
is additionally stated in the opening citation-integrity note (L3) and intro prose
(L5) *before* the first indication subsection (`## Tendon …`, L7). First-class, not
buried-in-bibliography. Headline 11/13 ≈ 85% Sikiric preserved; stale 11/12 ≈ 92%
alternate denominator eliminated (0 residual `92%` content hits). **Concentration
risk surfaced first-class.** → PASS

## IC-10 No Fabricated Citations

Every inline `[N]` resolves to a bibliography entry: max inline index per section
(A:9, B:7, C:14, D:9, E:4) equals that section's bibliography entry count — no
dangling inline references. Each bibliography entry carries a resolvable identifier
(PMID / DOI / PMC ID / NCT registry ID / named regulatory or registry URL). Several
URLs are self-documented as returning 404 or timing out at fetch (FDA 503A pages
B[4]/D[3], FDA PCAC media D[8], TGA notice/PDF B[7], He L PMC E[3] full-text,
AltTher IV-pilot PDF D[9]); these are best-effort HEAD-check misses against
real-and-identifiable records (resolvable via PMID/registry ID), not fabrications.
Per v1 IC-10 limitation (HEAD-check best-effort; comprehensive validation defers to
ultradeep), recorded as warnings, not HALT. **No fabricated citation; 5
URL-reachability warnings.** → WARN

## IC-11 No Placeholder Strings

Grep for `[citation needed]`, `TBD`, `TODO`, `Content continues`, `according to some
reports`, `research suggests`, `experts believe` across all five sections → **0
matches.** → PASS

## IC-12 No Wikipedia Citations

Grep `wikipedia.org` across all bibliographies and bodies → **0 matches.** → PASS

## IC-13 Per-Citation Corpus Scoping

Best-effort per the schema note (abstract-only paywalled content → WARN not HALT).
Load-bearing numerical/quoted claims grep-checked against retrievable corpora; the
sections are self-documenting about corpus accessibility and were written
conservatively (numerical per-animal effect sizes from inaccessible full texts
explicitly NOT relied upon — A[3], A[4]: "numerical per-animal effect sizes
therefore NOT relied upon"; C: n-not-stated marked throughout; D Xu-2020:
"n-per-group not verifiable from accessible text"; E He-2022 PK numbers traced to
accessible PMC9794587 full text).

Claims checked (numerical/quoted, sampled across sections): 24. No `quote-not-found`
and no `number-not-found` against retrievable corpora. Residual items are
`corpus-missing` (paywall/timeout/abstract-only) WARNs, not HALTs (Hsieh 2017
auth-wall — qualitative only; Xu 2020 Elsevier-paywall — qualitative only, 2 g/kg
dropped; Radeljak 2004 abstract-only; AltTher IV-pilot PDF timeout; FDA pages 404).
**No quote-not-found / number-not-found; corpus-missing items recorded as
warnings.** → WARN

---

## Verdict

verdict: PASS

No IC check produced a HALT. IC-10 and IC-13 produced WARNs (URL-reachability
best-effort misses; paywall/abstract-only corpus-missing) — both explicitly
WARN-not-HALT per the v1 limitations and the IC-13 paywall policy. IC-6 is
SKIP-mode (no compounding_data_sheet cites). All other content-discipline checks
(IC-1..IC-5, IC-7..IC-9, IC-11, IC-12) PASS. Population-mismatch PASS (51 checked, 0
flagged). Concentration audit: Sikiric/Zagreb 11/13 in-vivo ≈ 0.85, threshold
triggered, surfaced first-class.

```json
{
  "phase": "4.75",
  "iterations": 3,
  "ic_checks": {
    "IC-1": {
      "status": "PASS",
      "count_checked": 130,
      "count_flagged": 0,
      "findings": ["All inline type-tags in canonical enum (animal 47, mechanism_review 43, regulatory 21, rct 10, in_vitro 4, open_label 3, practitioner_protocol 2); no non-enum residuals after iter-2 remaps."]
    },
    "IC-2": {
      "status": "PASS",
      "count_checked": 43,
      "count_flagged": 0,
      "findings": ["Every bibliography entry (A:9, B:7, C:14, D:9, E:4) carries an enum type-tag; D[4] permitted dual-tag animal + in_vitro."]
    },
    "IC-3": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0,
      "findings": ["Sole vendor_label use (E.4 L84) grounds reconstitution/dilution arithmetic only (10 mg/2 ml = 5 mg/ml; 0.1 ml = 500 ug); no efficacy/AE/dose grounding."]
    },
    "IC-4": {
      "status": "PASS",
      "count_checked": 0,
      "count_flagged": 0,
      "findings": ["No anecdote_aggregate citation grounds any claim; mentions (B.3, D.6) are negative assertions that anecdote is not used to ground numbers."]
    },
    "IC-5": {
      "status": "PASS",
      "count_checked": 2,
      "count_flagged": 0,
      "findings": ["practitioner_protocol [7] grounds only contraindication convention (D.4) and a qualitative AE descriptor (D.6); efficacy/mechanism in those sentences co-cited to mechanism_review [2] / animal [4]."]
    },
    "IC-6": {
      "status": "SKIP-mode",
      "count_checked": 0,
      "count_flagged": 0,
      "findings": ["No compounding_data_sheet citations present in any section; nothing to check."]
    },
    "IC-7": {
      "status": "PASS",
      "count_checked": 51,
      "count_flagged": 0,
      "findings": ["All 47 animal + 4 in_vitro cites: every numerical-bearing sentence co-locates a species/cell-system subject within <100 chars (health-gates s1 override); 0 unflagged population mismatches."]
    },
    "IC-8": {
      "status": "PASS",
      "count_checked": 51,
      "count_flagged": 0,
      "findings": ["Cross-route/species inference surfaces (E.2 L50, E.4 L81) both carry explicit [route-extrapolation]/[species-extrapolation] flags; Section C reports routes as tested with no extrapolation."]
    },
    "IC-9": {
      "status": "PASS",
      "count_checked": 1,
      "count_flagged": 0,
      "findings": ["Single-lab share 11/13 in-vivo = 0.846 (>=0.70); surfaced as first-class ## Concentration audit (C L72) plus opening prose (L3, L5) before first indication subsection (L7)."]
    },
    "IC-10": {
      "status": "WARN",
      "count_checked": 43,
      "count_flagged": 5,
      "findings": ["No fabricated/dangling citations: max inline index per section equals bibliography count (A:9, B:7, C:14, D:9, E:4); all entries carry PMID/DOI/PMC/NCT IDs.", "5 URL-reachability warnings (best-effort HEAD-check, v1 limitation): FDA 503A pages (B[4]/D[3]), FDA PCAC media (D[8]), TGA notice/PDF (B[7]), He L PMC full-text (E[3]), AltTher IV-pilot PDF (D[9]) returned 404/timeout; records remain resolvable via PMID/registry ID."]
    },
    "IC-11": {
      "status": "PASS",
      "count_checked": 5,
      "count_flagged": 0,
      "findings": ["No placeholder strings (citation needed / TBD / TODO / Content continues / according to some reports / research suggests / experts believe) in any section."]
    },
    "IC-12": {
      "status": "PASS",
      "count_checked": 43,
      "count_flagged": 0,
      "findings": ["No wikipedia.org URLs in any bibliography or body."]
    },
    "IC-13": {
      "status": "WARN",
      "count_checked": 24,
      "count_flagged": 5,
      "findings": ["No quote-not-found and no number-not-found against retrievable corpora.", "Sections written conservatively: numerical per-animal effect sizes from inaccessible full texts explicitly not relied upon (A[3], A[4], C n-not-stated, D Xu-2020).", "5 corpus-missing WARNs (paywall/timeout/abstract-only): Hsieh 2017 auth-wall (no number attributed), Xu 2020 Elsevier-paywall (qualitative only; 2 g/kg dropped), Radeljak 2004 abstract-only (S-phase ~20%/~55% abstract-sourced), AltTher IV-pilot PDF timeout (n=2 zero-AE corroborated via mirror). He L 2022 PK figures verified against accessible PMC9794587 full text."]
    }
  },
  "population_mismatch": {
    "verdict": "PASS",
    "checked_citations": 51,
    "flagged_citations": []
  },
  "concentration_audit": {
    "verdict": "PASS",
    "total_primaries": 13,
    "largest_cluster_name": "Sikiric (Zagreb)",
    "largest_cluster_count": 11,
    "share": 0.846,
    "threshold_triggered": true,
    "surfaced_section_heading": "Concentration audit",
    "surfaced_before_first_indication": true
  },
  "corpus_scoping": {
    "verdict": "PASS",
    "claims_checked": 24,
    "claims_failed": [
      {
        "claim": "BPC-157 inhibited human melanoma cell growth, reducing S-phase fraction ~20% (lower conc.) up to ~55% (higher conc.) [5, in_vitro]",
        "cite_key": "radeljak-2004",
        "failure_mode": "corpus-missing",
        "grep_command": "rg -F -- '55%' /tmp/aplus-research/bpc-157/corpus/radeljak-2004.md",
        "grep_output": "(abstract-only: Melanoma Research 2004;14(4) conference abstract; verified at abstract level, full text not retrievable)"
      },
      {
        "claim": "Single i.m. 20 mg/kg produced no deaths; up to 4 mg/kg/day (rat) / 2 mg/kg/day (dog) 28-day no apparent changes [1, animal]",
        "cite_key": "xu-2020",
        "failure_mode": "corpus-missing",
        "grep_command": "rg -F -- '20 mg/kg' /tmp/aplus-research/bpc-157/corpus/xu-2020.md",
        "grep_output": "(Elsevier-paywalled; qualitative tox statements only, no numeric effect size attributed; 2 g/kg LD50 explicitly dropped)"
      },
      {
        "claim": "IV pilot n=2, up to 20 mg IV, no adverse events / no clinically meaningful lab changes [9, open_label]",
        "cite_key": "lee-burgess-2025",
        "failure_mode": "corpus-missing",
        "grep_command": "rg -F -- 'no adverse events' /tmp/aplus-research/bpc-157/corpus/lee-burgess-2025.md",
        "grep_output": "(PDF fetch timeout; corroborated via ResearchGate mirror 390202117 and review [2])"
      },
      {
        "claim": "BPC-157 VEGFR2 up-regulation / blood-flow recovery in rat hindlimb ischemia [3/13/4]",
        "cite_key": "hsieh-2017",
        "failure_mode": "corpus-missing",
        "grep_command": "rg -F -- 'VEGFR2' /tmp/aplus-research/bpc-157/corpus/hsieh-2017.md",
        "grep_output": "(full text behind auth wall; only qualitative VEGFR2/blood-flow direction relied upon - no numerical effect size attributed)"
      },
      {
        "claim": "FDA placed BPC-157 in 503A Category 2 effective 2023-09-29; immunogenicity/impurity/API rationale [3/4, regulatory]",
        "cite_key": "fda-503a-cat2",
        "failure_mode": "corpus-missing",
        "grep_command": "rg -F -- 'Category 2' /tmp/aplus-research/bpc-157/corpus/fda-503a-cat2.md",
        "grep_output": "(FDA pages 404 at fetch; date/rationale corroborated via FDA Law Blog analysis [5] and search-index surfacing)"
      }
    ]
  },
  "warnings": [
    "IC-10: 5 URL-reachability HEAD-check misses (FDA 503A pages, FDA PCAC media, TGA notice/PDF, He L PMC, AltTher PDF) - best-effort per v1 limitation; records resolvable via PMID/registry ID; not fabrications.",
    "IC-13: 5 corpus-missing items (paywall/timeout/abstract-only) recorded as WARN per IC-13 paywall policy; no quote-not-found or number-not-found; sections avoided relying on inaccessible numerical effect sizes.",
    "IC-6: SKIP-mode - no compounding_data_sheet citations present to check."
  ],
  "halt_reasons": []
}
```
