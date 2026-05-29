# endocrine-specialist — library-index

Conditional references loaded only when a task names them; not pre-loaded.

- `vault/library/_source-whitelist.md` — the type-tag enum (`rct`, `meta_analysis`, `cohort`, `regulatory`, `practitioner_protocol`, `vendor_label`, `anecdote_aggregate`, etc.) + admissibility matrix. Load before weighing any source; vendor/anecdote never ground a numerical claim; READ-only.
- `vault/library/endocrine/<axis-or-compound>/research-report.md` — per-axis/compound primary-literature layer (HPG/HPT/HPA/insulin/GH-IGF), authored on first dispatch (absent until then). Load for the axis or compound in scope; the basis for GRADE `certainty` / `human_outcome_evidence` / `concentration_of_evidence` / `worst_case_h_class`.
- `vault/library/endocrine/<compound>/practitioner-layer.md` — per-compound prescribing-convention layer. Load to render `practitioner_protocol` doses as convention, never trial-validated or self-administration guidance.
- `vault/library/endocrine/<compound>/non-english-layer.md` — per-compound non-English literature. Load when a compound triggers `[non-English-literature]` single-source-language concentration risk.
- `templates/refusal-class-taxonomy.yaml` + `templates/specialist-risk-class.yaml` — the canonical taxonomy (8 classes; encode ≥4 incl AUTHORITY_FRAMING_BYPASS, the rest addressed-or-not-covered) + the deep/compound mode-floor. Load at every refusal-gate / dispatch enforcement point; READ-only.

NEW per-axis/compound layers are authored from `aplus-research --mode=deep --target-class=compound` output; EXISTING layers are consumed read-only, never re-authored (PF-S2-04).
