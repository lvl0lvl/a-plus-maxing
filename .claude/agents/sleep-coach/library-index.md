# sleep-coach — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-interpretation + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited sleep norm, threshold (≥7 h floor, STOP-Bang/Epworth cut-points), or efficacy figure here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/library/protocols/` — existing vetted sleep/circadian protocol entries (the agent's own namespace); the source for a recommendation's GRADE certainty×strength and its established-vs-provisional tag. Empty until the first protocol lands → empty-state.
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard --target-class=protocol` for a sleep-protocol/circadian-literature gap.
- `vault/meta/contradictions.md` — load/append only when a sleep interpretation conflicts with a sibling specialist's entry or an active compound; log, never overwrite.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar + IDENTICAL anti-sycophancy block, which auto-load once per dispatch (card text emitted by reference, not inlined).
