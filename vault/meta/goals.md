---
permalink: a-plus-maxing/meta/goals
---

---
title: Goals
type: note
permalink: a-plus-maxing/meta/goals
status: scaffold
created: 2026-05-23
last_reviewed: 2026-05-23
review_cadence: quarterly (or at milestone events: doctor visit, lab panel)
---

# Goals

Where Walter is going. Distinct from `operator-profile.md` (who he is) and `current-state.md` (where he is now).

The research agent reads this to anchor "given Walter's GOALS, does intervention X move him toward or away from them?"

Update at:
- Quarterly review
- Doctor visit close-outs (goals shift on new diagnosis or all-clear)
- Major life events (training cycle change, work demand change)

---

## North-star horizon

- **20-year vision:** <one sentence — what kind of body / mind / function does Walter want at age <N+20>?>
- **5-year vision:** <one sentence — what does on-track look like?>

## Active milestone: July 2026 doctor visit

(From `~/.claude/projects/.../memory/user_walter_context.md`)

- **Visit date:** <YYYY-MM-DD>
- **MD:** <name, practice>
- **Visit objectives:**
  - Establish primary-care relationship
  - Get baseline blood panel ordered (specify panel scope: <CBC + CMP + lipid + HbA1c + thyroid + vitamin D + others — Walter to confirm>)
  - Discuss January 2026 issue follow-up
  - <other>
- **Doctor-handout queue:** items waiting for this visit
  - <compound or question — source page>
  - (populated automatically by `aplus-research` when compounds flag `risk_tier: medium+`)

## Health goals by domain

For each: target state, current gap, priority (P0-P4 per project convention).

### Body composition
- **Target:** <body fat %, lean mass, weight>
- **Current gap:** <delta from `current-state.md`>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

### Strength / performance
- **Target:** <specific lifts, capacity markers>
- **Current gap:** <delta>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

### Cardiovascular / metabolic
- **Target:** <RHR, VO2max, fasting glucose, lipids, BP>
- **Current gap:** <pending labs>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

### Sleep / recovery
- **Target:** <hours, efficiency, HRV>
- **Current gap:** <pending Oura>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

### Cognitive
- **Target:** <subjective and/or objective markers>
- **Current gap:** <>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

### Recovery from January 2026 issue
- **Target:** <full resolution | stable management | other>
- **Current gap:** <ongoing | resolved>
- **Priority:** <0-4>
- **Strategy:** <one sentence — MD-led | self-managed | combined>

### Longevity / preventive
- **Target:** <biological age delta, biomarker targets>
- **Current gap:** <>
- **Priority:** <0-4>
- **Strategy:** <one sentence>

## Accepted tradeoffs

Things Walter has decided NOT to optimize, so the agent doesn't waste research cycles on them.

- <tradeoff: explicitly de-prioritized in favor of X>

## Explicit non-goals

Things Walter does NOT want, even if research would recommend them.

- <e.g., "no chronic Rx if avoidable" — agent flags but does not auto-suggest>

## Hard limits (research must respect)

- No anabolic steroids
- No compounds requiring weekly clinic visits
- Cost ceiling per intervention: <$/month>
- No interventions that would disqualify from <activity / event / insurance> if relevant
- <other>

---

## How the agent uses this file

Per dispatch the agent extracts:
- The active goal domain (research must serve a stated goal — generic "could be useful" is rejected)
- Priority weighting (P0 goals get more aggressive intervention recommendations than P4)
- Hard limits (compounds violating these auto-excluded, regardless of evidence)
- Doctor-handout queue (any flagged compound auto-added)

If the dispatch can't tie its research question to a goal-domain entry, it must HALT with `no-goal-anchor`.