# Onboarding Question Bank

Derived from the S146 plan-gap analysis (the plan was a strategy briefing, not an executable daily system). This is what the **onboarding intake** must capture so the **care agent** starts with structure and only fills day-of specifics.

## Design rules (load-bearing)

1. **Capture the goal, not just the value.** The critical fact isn't "bed at 9" — it's "I need X hours." Anchor each question to the objective it serves so the plan can solve for it when inputs shift.
2. **A naive single-value question is worse than no question.** Where reality varies (sleep, training windows, work), the question captures the *pattern* (per-day / conditional / range) and allows **"varies / random"** as a first-class answer. A single value mapped to every day is a silent failure.
3. **Onboarding = durable structure + the shape of variability. Care agent = the day-of specific value.** Onboarding: "weekends are random, target 7 h." Care agent Saturday: "what time did you wake?" Taste-level detail ("no lima beans") and day-of state ("shoulder's cranky today") stay with the care agent.

## Capture shapes

`fixed` · `enum` · `list` · `range` · `per-day-grid` · `conditional/branching` · `goal+constraint` · `value-or-needs-test`

---

## §1 — Schedule & daily rhythm (the variability core)

| Q | shape | serves | naive-version failure |
|---|---|---|---|
| Target sleep hours + a 7-day grid of typical bed/wake, each tagged fixed/flexible, with "varies/random" selectable per day | goal + per-day-grid | sleep-debt math, wind-down timing, session placement | one bed/wake mapped to all 7 days is wrong on most of them; the *target hours* is what steers |
| Work hours + location per day (home/on-site/shift) | per-day-grid | explains why given days differ; anchors meal + training windows | a single "9–5" hides the days that break the pattern |
| Per day: when *can* you train + max minutes + AM/PM preference + "no-train" days | per-day + goal+constraint | places sessions in real windows; honors the ≤60-min cap | a fixed daily slot breaks the first long workday |
| Meal windows + any intermittent-fasting pattern + which meals are skippable/movable | per-day + conditional | meal timing vs training; realistic feeding schedule | assuming 3 fixed meals mis-times fuel around training |

## §2 — Food & meal prep

| Q | shape | serves |
|---|---|---|
| Minutes you'll spend on food prep, on which days + batch-cook vs cook-fresh preference | per-day + goal+constraint | **this is where "crockpot" comes from** — meals inside the time budget |
| Kitchen equipment (crockpot/Instant Pot/air fryer/grill/…) | checklist | which recipes are offerable at all |
| Diet framework + strictness + allergies + intolerances + religious/ethical avoids | enum + list | hard, medical-grade restrictions (distinct from taste) |
| Repeat tolerance ("distinct meals before you're bored") | scalar | build a small rotation, not a 30-meal calendar |
| Protein sources rotated + sourcing (grass-fed/organic access) + grocery cadence + budget ceiling | list + constraint | realistic, affordable recipes |

## §3 — Training

| Q | shape | serves | naive failure |
|---|---|---|---|
| Current working load or recent e1RM for key lifts, **in lb**, or "unknown → test" | list (lb) or value-or-needs-test | the plan can prescribe an actual load | no load → the plan degrades to philosophy |
| Home-gym inventory: bars, plate range, dumbbell range (lb), rack, machines, cardio kit | checklist + range | only prescribe what exists |
| Injury/limitation map: per issue — provoking movements, pain-free ROM, diagnosed vs self-identified, clinician restriction | list, per-injury | real substitutions + in-session pain rule |
| Measured benchmarks: HRmax, zone-2 pace-at-HR, 4×4 output | value-or-needs-test | "not measured" → schedule a test, don't guess |

## §4 — Meds, peptides & supplements

| Q | shape | serves |
|---|---|---|
| Per compound: dose, route, **injection/dose schedule + start date + current titration step**, prescriber yes/no | list, per-compound with schedule | the plan knows the retatrutide schedule + what to do with an already-running peptide stack |
| Per supplement: dose, timing, brand — **and the ingredient panel for any blend** | list with panels | an unnamed blend is un-screenable (the "Momentum shake" problem) |
| Is a clinician overseeing your retatrutide/peptides? (yes/no) | branching, load-bearing | if no, every "route to physician" item is a dead end — changes what the plan can responsibly recommend |

## §5 — Monitoring & access

| Q | shape | serves |
|---|---|---|
| Devices/data available: wearable (HRV/RHR/SpO₂ source), smart scale, BP cuff, CGM, Oura-pending | checklist | what the live loop can auto-ingest vs manual |
| Recent labs (upload) + a PCP/clinic for bloodwork + insurance/cost constraint | branching | turns "get baseline labs" into a real path |
| How you'll log adherence + the daily check-in (app/manual/voice/unwilling) | enum | defines the check-in *instrument* |

## §6 — Goals, boundaries & safety

| Q | shape | serves |
|---|---|---|
| Concrete goals + timeline + priority order, **in lb** (e.g. 238→220 lb by [date], hold strength) | targets (lb), ranked | steerable checkpoints replace "optimal health/fitness/longevity" |
| Hard limits (no anabolic steroids, cost ceiling, time ceiling, won't-do list) | list | boundaries enforced everywhere |
| Safety screens with **follow-through** branch (positive apnea → evaluated? scheduled? untreated?) | branching | a positive screen with no follow-through is why the apnea sat unaddressed |

---

## Care-agent territory (NOT onboarding)

The idiosyncratic, day-of, and fast-changing — onboarding hands the frame, the care agent fills the value:

- Taste-level dislikes ("no lima beans," "sick of chicken this week").
- Day-of state ("slept badly," "shoulder's cranky," "traveling Thursday, no crockpot").
- In-the-moment substitutions and one-offs (swap tonight's dinner, move a session, skip the sauna).
- Anything that changes faster than onboarding re-runs.

The split is the whole design: onboarding captures durable structure + the *shape* of variability; the care agent asks what today actually is.
