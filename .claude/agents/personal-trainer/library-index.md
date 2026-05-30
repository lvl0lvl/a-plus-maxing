# personal-trainer — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-interpretation + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited training claim, threshold (set-volume, velocity-loss, healing-timeline ranges), or effect-size here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/protocols/exercise` + training `vault/parameters/` — the agent's own write namespace (training volumes/intensities, periodization/return-to-training entries); the source for a recommendation's GRADE certainty×strength and its established-vs-provisional tag. Scaffold (`exercise.md`) until the first protocol is authored → empty-state. (Goal-agnostic training/MSK-rehab research-reports, when dispatched, land under `vault/library/protocols/<slug>/` per the aplus-research output convention.)
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard --target-class=protocol` for a training-literature/MSK-rehab/parameter gap.
- `vault/meta/contradictions.md` — load/append only when a training interpretation conflicts with a sibling specialist's entry (e.g., a masters-protein parameter the nutritionist owns) or an active compound; log, never overwrite.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar + IDENTICAL anti-sycophancy block, which auto-load once per dispatch (card text emitted by reference, not inlined).
