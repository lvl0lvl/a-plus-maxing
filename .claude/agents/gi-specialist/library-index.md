# gi-specialist — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case."

- `vault/library/gi/` — GI research-artifact subtree (microbiome, gut-barrier, probiotic-class, food-reaction taxonomy entries). Load when authoring a NEW GI library entry from dispatch output or grounding a biomarker/compound claim. Author goal-agnostically; never re-author an existing consumed entry (PF-S2-04).
- `vault/library/_source-whitelist.md` — the admissible-source gate. Load when grounding any cited GI value/dose/cutoff; an ungrounded figure → BASIS_NOT_REVIEWABLE.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires; emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (gi-specialist = compound-medium, mode_floor standard). Load when dispatching `aplus-research`; never hardcode a lower mode.
