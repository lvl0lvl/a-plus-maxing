# peptide-specialist — library-index

Conditional references loaded only when a task names them; not pre-loaded.

- `vault/library/peptides/_triage.md` — the closed peptide research surface. Load first when scoping which compound a query touches; READ-only.
- `vault/library/_source-whitelist.md` — the type-tag enum (`[primary]`, `[practitioner_protocol]`, `[vendor_label]`, `[anecdote_aggregate]`, `[population-mismatch]`, `[route-extrapolation]`). Load before weighing any source; READ-only.
- `vault/library/peptides/<compound>/research-report.md` — per-compound primary-literature layer. Load for the compound in scope; the basis for `maturity_rung` / `human_outcome_evidence` / `concentration_of_evidence`.
- `vault/library/peptides/<compound>/practitioner-layer.md` — per-compound prescribing-convention layer. Load to render `source_tier: practitioner_protocol` doses as convention, not trial-validated.
- `vault/library/peptides/<compound>/non-english-layer.md` — per-compound non-English literature. Load when a compound triggers `[non-English-literature]` (single-source-language concentration risk).

NEW per-compound layers are authored from `aplus-research --mode=deep --target-class=compound` output; EXISTING layers are consumed read-only, never re-authored (PF-S2-04).
