# supplement-specialist — library-index

Conditional references loaded only when a task names them; not pre-loaded. The supplement-specialist CONSUMES these read-only — it authors no `vault/library/` subtree (unlike peptide-specialist); its owned writes are `vault/compounds/` (supplement class) + `vault/protocols/supplement-stack`.

- `vault/library/_source-whitelist.md` — the type-tag enum (`rct`, `meta_analysis`, `cohort`, `open_label`, `animal`, `in_vitro`, `mechanism_review`, `regulatory`, `compounding_data_sheet`, `vendor_label`, `practitioner_protocol`, `anecdote_aggregate`) + tier admissibility. Load before weighing any source; READ-only.
- `vault/library/peptides/_triage.md` — the inherited compound-class taxonomy + admissibility convention this role mirrors for its own class scoping; READ-only structural template (the supplement-specialist owns no `_triage` of its own).
- `vault/library/supplements/<compound>/research-report.md` — per-compound primary-literature layer the role CONSUMES when in scope (authored by a separate wiki campaign, not this role); the basis for `maturity_rung` / `human_outcome_evidence` / `concentration_of_evidence`.
- `vault/library/methodology/evidence-tiers.md` — the evidence-tier matrix the compound `evidence_tier` field resolves against; READ-only.

EXISTING layers are consumed read-only, never re-authored (PF-S2-04); new supplement research lands in `vault/compounds/<slug>.md` + `vault/protocols/supplement-stack` from `aplus-research --mode=deep --target-class=compound` output.
