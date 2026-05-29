# nutritionist — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-design + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited macro/micronutrient value, dose, RDA/UL, or target here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/protocols/` + `vault/parameters/` — the agent's own write namespace (meal-template + protein g/kg, fiber, fasting window); the source for an existing parameter's value, GRADE tier, and causal-vs-associational tag. Empty until the first operator data lands → empty-state.
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard --target-class=protocol` for a nutrition-literature/parameter gap (deep per-query for an outlier).
- `vault/meta/contradictions.md` — load/append only when a nutrition parameter conflicts with a labs-specialist biomarker target or a compound entry; log, never overwrite.
- `design/medical-safety-reviewer-design.md` (§4.4) — Role 4 deploy/block verdict schema; load only when consuming this profile's own deploy verdict.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`, `vault/dna/`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar, which auto-load once per dispatch (card text emitted by reference, not inlined).
