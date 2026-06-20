# Phase 7.5 Risk-Floor Gate — Ipamorelin

## Verdict

verdict: PASS

Compound risk_tier = experimental (frontmatter + §metadata) → BLOCKING risk-floor applies.
All three mandatory populated fields (adverse_effects_literature, contraindications,
monitoring) are present and cited; stopping_criteria present as rules + explicit
gap-pointer; and the experimental-tier third-party objective monitoring marker
requirement (health-gates.md §2, line 59) is satisfied by a named lab assay
([[biomarkers/igf-1]], plus fasting glucose / HbA1c).

## Field-by-field (each: present? cited? location)

- **adverse_effects_literature — present: y · cited: y · location: §7.1–§7.3, §7.7**
  - Beck 2014 RCT AE data: TEAE 87.5% ipamorelin vs 94.8% placebo, "well tolerated,
    no serious compound-related AEs" — §7.1, cited [1, rct] (unified [15], Beck 2014).
  - GH-axis class risks — peripheral edema, arthralgia, carpal-tunnel symptoms,
    impaired glucose tolerance / reduced insulin sensitivity — §7.2, cited
    [3, mechanism_review] (unified [19], Liu 2007).
  - FDA PCAC-flagged signals — fluid retention, hyperglycemia, congestive-heart-failure
    concern — §7.3, cited [4, regulatory] (unified [22], FDA PCAC Oct 29 2024).
  - Thin human safety / route-and-duration mismatch (7-day IV only, chronic SC
    uncharacterized) explicitly noted — §7.7.
  → populated.

- **contraindications — present: y (non-empty) · cited: y · location: §7.5**
  - Impaired glucose tolerance / diabetes — cited [3] (GH-axis insulin-resistance) +
    [4, regulatory] (PCAC hyperglycemia).
  - Active or history of malignancy — cited [5,6, cohort] (IGF-1–cancer prospective
    associations: breast OR 1.28; breast HR 1.25 / prostate HR 1.31) extended via the
    standard GH-therapy malignancy contraindication [3].
  - Fluid-overload states / heart failure — cited [3] (edema class effect) +
    [4, regulatory] (PCAC CHF concern).
  - NOTE (honest gap, non-blocking): the report does NOT carry an explicit
    pregnancy/lactation contraindication line; `doctor_discussion_required: true`
    is set in frontmatter but pregnancy/lactation is not separately stated/cited.
    Does not change the verdict — the field is non-empty and cited via the three
    items above, which clears the "populated" bar.
  → populated.

- **monitoring — present: y (non-empty) · names IGF-1 + glucose/HbA1c · cited: y · location: §7.5, §7.6, §10**
  - Serum IGF-1 — named objective assay, [[biomarkers/igf-1]]; explicitly "keep within
    age/sex reference range," NOT minimized (EPIC-Heidelberg U-shaped IGF-1–mortality,
    §7.6) — cited [2,3,5,6] (unified [21] Mukama 2023 grounds the U-shape).
  - Fasting glucose and HbA1c — insulin-resistance / hyperglycemia surveillance —
    cited [3,4].
  - Clinical surveillance for edema / arthralgia / carpal-tunnel — cited [3].
  → populated.

- **stopping_criteria — present: y · location: §7.5 ("Stopping rules") + §10**
  - Explicit rules: discontinue / re-evaluate on IGF-1 above age-adjusted range, new
    or worsening glucose dysregulation, or onset of edema/arthralgia/carpal-tunnel —
    each mapped to a cited risk [3,4]; with the honest pointer that "No validated
    ipamorelin-specific stopping threshold exists (gap)."
  → placeholder-with-pointer (real rules present, plus explicit gap-pointer to the
    absent validated threshold).

## Third-party objective monitoring marker (experimental-tier requirement)

- **present: y** — health-gates.md §2 (line 59) requires ≥1 monitoring item referencing
  `[[biomarkers/<name>]]` or a named lab assay. Satisfied by **IGF-1** ([[biomarkers/igf-1]]),
  the canonical objective GH-axis monitoring marker, plus **fasting glucose** and **HbA1c**.
  All are NAMED OBJECTIVE lab assays (not self-reported/subjective).

## Path note

The structured verdict below records `compound_entry_path` as the path that actually
exists on disk — `vault/library/peptides/ipamorelin/research-report.md`. The dispatch
brief named `vault/compounds/ipamorelin.md`, which does NOT exist (that directory holds
bpc-157/ghk-cu/kpv/tb-500 only). Recorded honestly rather than pointing at a missing file.

## Structured verdict

```json
{"phase":"7.5","compound_risk_tier":"experimental","compound_entry_path":"vault/library/peptides/ipamorelin/research-report.md","required_fields":{"adverse_effects_literature":"populated","contraindications":"populated","monitoring":"populated","stopping_criteria":"placeholder-with-pointer"},"third_party_monitoring_marker_present":true,"third_party_markers":["IGF-1","fasting glucose","HbA1c"],"halt_reasons":[],"iterations":1}
```
