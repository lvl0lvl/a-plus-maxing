# longevity-strategist — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case."

- `vault/library/longevity/` — longevity research-artifact subtree (established-lever evidence, geroprotector profiles — rapamycin/metformin/NAD+/senolytics, aging-clock interpretation entries). Load when authoring a NEW longevity library entry from dispatch output or grounding a lever/compound claim. Author goal-agnostically; never re-author an existing consumed entry (PF-S2-04).
- `vault/library/_source-whitelist.md` — the admissible-source gate. Load when grounding any cited longevity value / effect size / clock figure; an ungrounded figure → `BASIS_NOT_REVIEWABLE`.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires; emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (longevity-strategist = protocol-medium-or-compound-experimental, mode_floor deep). Load when dispatching `aplus-research`; never hardcode a lower mode.

Not loaded here: operator state (`vault/meta/{operator-profile,goals}.md`) binds at dispatch, never in a goal-agnostic library write (PF-S2-04); the refusal taxonomy + GRADE grammar auto-load per Context Loading, not as conditional refs.
