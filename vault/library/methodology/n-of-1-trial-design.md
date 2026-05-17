---
title: N-of-1 Trial Design
type: reference
status: active
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/library/methodology/n-of-1-trial-design
---

# N-of-1 Trial Design

How to run a real n=1 experiment instead of "I tried it and felt better." Every entry in `experiments/` follows this methodology.

## Core principles

### 1. Single-variable changes
Change one thing at a time. If you start magnesium glycinate AND drop evening caffeine, you can't attribute changes to either. Exception: stacking multiple things known to be synergistic where the trial question is "does the stack work" — but then the stack is the variable, and you can't decompose it.

### 2. Pre-specified outcomes
Decide what you're measuring BEFORE starting. Otherwise you'll find post-hoc whatever moved. Outcomes should be:
- Measurable (HRV, sleep efficiency, ApoB, body weight, RPE, subjective 1-10 scale)
- Linked to the claim (a sleep aid → sleep efficiency, not "energy")
- Realistic given the intervention's expected effect size

### 3. Adequate baseline
Two weeks of stable baseline data BEFORE intervention. This sets the noise floor — you can't claim a signal without knowing the variance.

### 4. Adequate duration
Different outcomes move on different timescales:

| Outcome | Time to see effect | Trial duration |
|---|---|---|
| Sleep quality | 3-7 days | 2-4 weeks |
| HRV | 2-4 weeks | 6-8 weeks |
| Resting HR | 2-4 weeks | 6-8 weeks |
| Energy/cognition (subjective) | days | 2-4 weeks |
| Body weight | 1-2 weeks | 4-12 weeks |
| Body composition (DEXA) | 8-12 weeks | 12-24 weeks |
| Lipids (ApoB, LDL) | 6-12 weeks | 12-16 weeks |
| HbA1c | 8-12 weeks (lags glucose) | 12-16 weeks |
| Inflammation (hs-CRP) | 4-8 weeks | 8-12 weeks |
| Strength / performance | 4-8 weeks | 8-16 weeks |

If the trial duration is shorter than the outcome's response time, the trial is invalid.

### 5. Design types

- **AB:** baseline → intervention. Cheapest, weakest. Risks confounding with seasonality, weather, life events.
- **ABA:** baseline → intervention → washout. Stronger — if the signal reverses on washout, attribution is more credible.
- **ABAB:** baseline → intervention → washout → intervention again. Strongest practical design for n=1. Use for low-risk reversible interventions.

Choose the strongest design the intervention's safety profile allows.

### 6. Confounder control
List every confounder you can't control (travel, sleep disruption, illness, stress, weather, training load changes). Track them. If a confounder fires during the trial, either extend the trial or invalidate that window.

### 7. Honest stopping rules
Define before starting:
- **Safety stop:** any adverse effect at threshold X → stop immediately
- **Futility stop:** if no signal by week N at expected dose, stop and conclude null
- **Success criterion:** what magnitude of change counts as a real effect (not just statistical noise)

If you don't pre-commit to stopping rules, you'll either keep going forever or quit when bored.

### 8. Source quality on the supply side
Especially for peptides and research-chemical-tier compounds: source matters more than dose. A trial with a contaminated/underdosed supply tests the supply chain, not the compound. Track:
- Supplier
- Batch / COA reference if available
- Storage conditions

### 9. Document the null
A trial that shows nothing is still valuable. Write up null results with the same rigor as positives. They go in `experiments/` and inform `library/<thing>.md` with `walter_status: discontinued` + rationale.

## Experiment file structure

See `experiments/_template.md` for the file skeleton.

## Common failure modes
- Stopping too early because nothing visible at week 2 (most outcomes need longer)
- Continuing too long because "it might still work" (predefined stopping rules prevent this)
- Adding a second variable mid-trial ("I'll also start X to amplify")
- Comparing to a remembered baseline instead of recorded data
- Subjective-only outcomes for objective claims ("I feel sharper" without cognitive testing)
- Not distinguishing "feels good" placebo from real effect (blinding is hard n=1 but possible for some interventions via timing)