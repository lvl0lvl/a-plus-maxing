# Phase 2.5 — RUBRIC (cardiovascular-specialist, mode=standard, threshold 92/100)

Each retrieval section is scored by a FRESH dispatched judge across the dimensions below (the judge JSON skeleton in SKILL.md Phase 3 is the output shape). A section PASSES at total ≥92. The dimensions map to the judge `dimension_scores` keys.

## Dimensions (0–100 each; total = rounded mean of non-null)

1. **evidence_quality** — claims rest on Tier-1/2 primaries (RCTs, meta-analyses, cohorts, regulatory/guideline). Landmark cardiovascular trials cited by name + registration where load-bearing (SPRINT, CTT, IMPROVE-IT, FOURIER, ODYSSEY, CLEAR, ASPREE, REDUCE-IT, JUPITER, CANTOS, MESA, Mandsager/Kodama). No reliance on a vendor/blog/forum for any numeric.
2. **citation_fidelity** — every numeric (effect size, RR/HR, sens/spec, mmHg, mmol/L, %, n, p) traces to a real cited primary whose first-author/year/PMID/DOI is correct; no fabricated or misattributed cite. (PF-S2-02 class.)
3. **type_tag_discipline** — every inline `[N, tag]` carries exactly one tag from the `_source-whitelist.md` enum (`rct|meta_analysis|cohort|open_label|animal|in_vitro|mechanism_review|regulatory|compounding_data_sheet|vendor_label|practitioner_protocol|anecdote_aggregate`). Guideline-society documents (AHA/ACC/ESC/ACSM) tag `regulatory` (guidance) or `practitioner_protocol` (dosing convention); their underlying trials cited as `rct`/`meta_analysis`.
4. **population_annotation** — any `animal`/`in_vitro` cite grounding a numeric carries `[population-mismatch: <species>]` in-sentence (cardiovascular sections should be overwhelmingly human; flag any animal-mechanism number). Sex-specific cohorts carry `[population-mismatch: <sex>]`.
5. **route_fidelity** — no dose-route extrapolation without `[route-extrapolation]` (most CV drugs oral; flag any mismatch).
6. **concentration_audit_handling** — distinct primaries are multi-group (cardiovascular evidence base is large + independent). Any localized single-group dependence (e.g., a single trialist/sponsor for one agent) is flagged in-section, not buried.
7. **risk_floor_readiness** — for every medium+ compound family (statins, antihypertensives, antiplatelets, PCSK9i, omega-3), contraindications + monitoring (named biomarker/sign) + stopping/holding criteria are fillable from retrieved sources. (null only for the pure-physiology / red-flag sections where no compound write applies.)
8. **reasoning_integrity** — correlation vs causation held apart (MR/genetic evidence flagged as causal where it is; observational associations flagged as such); mechanism vs human-outcome separated; absolute vs relative risk distinguished; no over-claim beyond the cited design.
9. **completeness_vs_brief** — the section covers every item enumerated in its plan.md brief; explicit confirmed-absence statements where a sub-topic yielded no admissible primary.

## Health-research mandatory dimensions (SKILL Phase 2.5)

- **Concentration audit** — count distinct primaries by group/sponsor; flag if ≥70% single-group (expected « 70% for cardiovascular).
- **Population annotation** — every animal cite carries species + n.
- **Route fidelity** — no route extrapolation without explicit tag.
- **Risk-floor readiness** — medium+ compound families have fillable contraindications + monitoring + stopping fields.

## Auto-fail (sub-agent scope; → HALT, re-dispatch)

- A numeric grounded by a `vendor_label`/`anecdote_aggregate` cite.
- An untagged inline citation, or a tag outside the enum.
- A fabricated/misattributed primary (wrong first author/year/PMID).
- A consumer-device claim presented as diagnostic (smartwatch ECG/cuffless BP as a diagnosis).
- A red-flag/symptom claim that softens the emergency floor (e.g., reassuring a chest-pain pattern).
