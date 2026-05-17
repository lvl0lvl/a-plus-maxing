---
title: 'Experiment: <name>'
type: experiment
status: planned | baseline | intervention | washout | complete | aborted
owner: walter
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
depends_on: []
superseded_by: null
review_cadence: weekly
intervention: <compound/intervention name, link to library entry>
design: AB | ABA | ABAB
start_date: YYYY-MM-DD
planned_end_date: YYYY-MM-DD
actual_end_date: null
permalink: a-plus-maxing/experiments/template
---

# Experiment: <Name>

## Hypothesis
Specific, falsifiable. "X will increase Y by Z amount over N weeks."

## Background
Why now? What in the library or in Walter's data motivates this trial?
Link to `library/<topic>/<thing>.md`.

## Design

### Type
AB / ABA / ABAB — and why this design was chosen.

### Periods
| Phase | Duration | Start | End | What changes |
|---|---|---|---|---|
| Baseline (A1) | 2 weeks | YYYY-MM-DD | YYYY-MM-DD | nothing — record only |
| Intervention (B1) | N weeks | YYYY-MM-DD | YYYY-MM-DD | start <intervention> at <dose> |
| Washout (A2) | N weeks | YYYY-MM-DD | YYYY-MM-DD | stop intervention |
| Re-intervention (B2) | N weeks | YYYY-MM-DD | YYYY-MM-DD | restart <intervention> |

### Intervention details
- What: exact compound, brand/source, batch if applicable
- Dose:
- Timing:
- Route:

### Primary outcome measure
The single thing you most care about moving. Pre-specified.

### Secondary outcome measures
Other things to track. Will inform but not determine the conclusion.

### Confounders to track
List things to watch. If any fires during a phase, note it and consider extending.

### Stopping rules
- Safety: stop immediately if <criteria>
- Futility: conclude null if <criteria> by <date>
- Success: declare effect if <magnitude> change in primary outcome and <persistence requirement>

## Data Collection
- Daily auto-data: HRV, sleep, weight (from Apple Health + Oura)
- Subjective: 1-line daily note in `daily/YYYY-MM-DD.md` tagged `#experiment-<slug>`
- Periodic measures: list each (e.g., "ApoB at week 0, 8, 16")
- Cost & supplier tracking

## Results (filled during trial)

### Phase A1 (baseline)
- Primary outcome baseline value (mean ± SD):
- Notable confounders during phase:

### Phase B1 (intervention)
- Primary outcome (mean ± SD):
- Delta vs baseline:
- Subjective notes:
- Confounders that fired:

### Phase A2 (washout, if applicable)
...

### Phase B2 (re-intervention, if applicable)
...

## Conclusion (at end)
- **Effect:** positive / null / negative / inconclusive
- **Confidence:** high / medium / low
- **Decision:** adopt / discontinue / extend trial / change protocol
- **Update to library:** what gets written back into `library/<topic>/<thing>.md`
- **Update to protocols:** if adopted, add to `protocols/supplement-stack.md` etc.

## References cited
- Linked from the library entry
- Any additional sources gathered during the trial