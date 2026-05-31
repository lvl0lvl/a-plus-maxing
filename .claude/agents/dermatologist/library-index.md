# dermatologist — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case."

- `vault/library/dermatology/` — dermatology research-artifact subtree (topical-active, AGA, photoaging, cosmeceutical, condition-literacy entries). Load when authoring a NEW dermatology library entry from dispatch output or grounding a topical-active/AGA claim. Author goal-agnostically; never re-author an existing consumed entry (PF-S2-04).
- `vault/library/_source-whitelist.md` — the admissible-source gate. Load when grounding any cited dermatology value/dose/concentration/effect-size; an ungrounded figure → BASIS_NOT_REVIEWABLE.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires; emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (dermatologist = compound-medium, mode_floor standard). Load when dispatching `aplus-research`; never hardcode a lower mode.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`) binds at dispatch, never in a goal-agnostic library write (PF-S2-04); the refusal taxonomy + GRADE grammar auto-load per Context Loading, not as conditional refs.
