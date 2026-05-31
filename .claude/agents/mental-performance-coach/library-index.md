# mental-performance-coach — library-index

Conditional references. Load only when the section being authored/served needs it; never pre-load "just in case." Max 3 conditional refs per dispatch.

- `vault/library/<cognitive-class>/` — cognitive/stress research-artifact subtree (focus/working-memory/processing-speed protocols, stress-resilience, cognitive-training-transfer entries). Load when authoring a NEW cognitive library entry from dispatch output or grounding a cognition claim. Author goal-agnostically; never re-author an existing consumed entry (PF-S2-04).
- `vault/library/_source-whitelist.md` — the admissible-source gate. Load when grounding any cited cognition value/effect-size/threshold; an ungrounded figure → BASIS_NOT_REVIEWABLE.
- `templates/refusal-class-taxonomy.yaml` — the canonical 8-class taxonomy. Load when a refusal class fires; emit the card by reference; never invent a class.
- `templates/specialist-risk-class.yaml` — the mode-floor map (mental-performance-coach = protocol-medium, mode_floor standard, target_class protocol). Load when dispatching `aplus-research`; never hardcode a lower mode.
- `vault/compounds/` (cognitive class) — READ-ONLY, for routing context only. Load when a nootropic/cognitive-compound query arrives, to confirm the routing target before filing the Architecture Question to supplement-specialist; never author here.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`) binds at dispatch, never in a goal-agnostic library write (PF-S2-04); the refusal taxonomy + GRADE grammar auto-load per Context Loading, not as conditional refs; sleep/diet protocols are sleep-coach/nutritionist-owned (cross-read as cognition inputs, never authored).
