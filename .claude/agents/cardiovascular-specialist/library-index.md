# cardiovascular-specialist — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case."

- `vault/library/_source-whitelist.md` — the admissible-source gate; the grounding spine. Load when grounding any cited CV value/dose/cutoff/effect-size (a biomarker/protocol/parameter claim resolves against a dispatched-research return + this whitelist); an ungrounded figure → BASIS_NOT_REVIEWABLE. This role owns NO `vault/library/` write class per the WIKI (CV compounds are name-and-route reasoning, never owned library writes); if a goal-agnostic CV research subtree exists it is consumed read-only, never authored here.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires; emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (cardiovascular-specialist = compound-medium, mode_floor standard, target_class compound). Load when dispatching `aplus-research`; never hardcode a lower mode.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`) binds at dispatch, never in a goal-agnostic library read (PF-S2-04); the refusal taxonomy + GRADE grammar auto-load per Context Loading, not as conditional refs.
