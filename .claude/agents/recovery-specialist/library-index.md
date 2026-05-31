# recovery-specialist — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-interpretation + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited recovery norm, HRV/RHR threshold, wearable validity statistic, or modality effect size here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/protocols/` (e.g. `vault/protocols/recovery.md`) + recovery `vault/parameters/` (sauna/cold dose) — existing vetted recovery-modality protocol/parameter entries (the agent's own entity namespace); the source for a recommendation's GRADE certainty×strength and its established/provisional/equivocal tag. Scaffold until the first protocol is authored → empty-state. (Goal-agnostic recovery-protocol research-reports, when dispatched, land under `vault/library/protocols/<slug>/` per the aplus-research output convention.)
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard --target-class=protocol` for a recovery-modality / autonomic-monitoring literature gap.
- `vault/meta/contradictions.md` — load/append only when a recovery interpretation conflicts with a sibling specialist's entry (sleep-coach / personal-trainer / cardiovascular-specialist / lymphatic-specialist) or an active compound; log, never overwrite.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar + IDENTICAL anti-sycophancy block, which auto-load once per dispatch (card text emitted by reference, not inlined).
