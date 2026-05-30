# lymphatic-specialist — library index

Conditional references (load only when the task needs it; max 3 per dispatch; data-under-interpretation + auto-loaded static grammar do not count).

- `vault/library/_source-whitelist.md` — resolve every cited lymphatic norm, threshold (limb-volume SEM, ISL staging, BIS cut-points, node duration/size cut-points), or efficacy figure here before emitting; an ungrounded number routes to BASIS_NOT_REVIEWABLE.
- `vault/protocols/` (e.g. `vault/protocols/lymphatic.md`) — existing vetted lymphatic/drainage-modality protocol entries (the agent's own entity namespace); the source for a recommendation's GRADE certainty×strength and its established-vs-provisional tag. Scaffold until the first protocol is authored → empty-state. (Goal-agnostic lymphatic-protocol research-reports, when dispatched, land under `vault/library/protocols/<slug>/` per the aplus-research output convention.)
- `vault/library/biomarkers/<slug>/` — goal-agnostic inflammation-marker (hs-CRP/IL-6/TNF-α/ESR) research-reports, when dispatched via `--target-class=biomarker`; the validation-tier source for "systemic-inflammation, NOT lymphatic-function" framing.
- `.claude/skills/aplus-research/SKILL.md` — load only when dispatching `aplus-research --mode=standard --target-class=protocol` (or `--target-class=biomarker`) for a lymphatic-protocol / inflammation-marker literature gap.
- `vault/meta/contradictions.md` — load/append only when a lymphatic interpretation conflicts with a sibling specialist's entry or an active compound; log, never overwrite.

Not loaded here: operator state (`vault/meta/{operator-profile,current-state,goals}.md`), which binds at dispatch as context, never at authoring (PF-S2-04); and the refusal-class taxonomy + GRADE/H-class grammar + IDENTICAL anti-sycophancy block, which auto-load once per dispatch (card text emitted by reference, not inlined).
