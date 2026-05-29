# labs-specialist — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-interpretation + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited reference range or target here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/biomarkers/` — existing vetted biomarker entity entries (the agent's own namespace); the source for a range's category tag (descriptive RI / decision limit / functional-optimal) and its GRADE intervention tier. Empty until the first panel lands → empty-state.
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard` for a reference-range/target gap (deep per-query for novel/outlier markers).
- `vault/meta/contradictions.md` — load/append only when a biomarker interpretation conflicts with a sibling specialist's entry or an active compound; log, never overwrite.
- `design/medical-safety-reviewer-design.md` (§4.4) — Role 4 deploy/block verdict schema; load only when consuming this profile's own deploy verdict.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`, `vault/dna/`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar, which auto-load once per dispatch (card text emitted by reference, not inlined).
