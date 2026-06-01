# genetics-specialist — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case."

- `vault/library/_source-whitelist.md` — the admissible-source gate; the grounding spine. Load when grounding any cited genetics identifier (gene symbol / rsID / star-allele / HLA field / ACMG tier / CPIC level / PMID / effect size) — a `vault/dna/` page or PGx flag resolves against a dispatched-research return + this whitelist; an ungrounded figure or a DTC-vendor/raw number → BASIS_NOT_REVIEWABLE. This role owns the `vault/dna/` write surface (variant pages + per-variant analysis) but consumes any goal-agnostic `vault/library/` genetics subtree read-only, never authored here.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires (centrally BASIS_NOT_REVIEWABLE for the DTC floor, TIME_CRITICAL for the EMERGENCY floor, AUTHORITY_FRAMING_BYPASS); emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (genetics-specialist = genetic-pgx-high, mode_floor deep, target_class reference). Load when dispatching `aplus-research`; never hardcode a lower mode.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`) binds at dispatch, never in a goal-agnostic library read (PF-S2-04); the refusal taxonomy + GRADE grammar auto-load per Context Loading, not as conditional refs.
