# Design Review State

## Screen: DIR Clinical Instrument (node nJ4f1)
File: design/a+maxing_designs.pen
Reviewed against: "Technical Instrument on warm paper" style system (kit node gOwal); reference approved layout node LXKlO (layout locked, not under review).

Status: REVISE
Iteration: 1 / 3
Max iterations: 3

Critic-side reference library: ABSENT (no project library/ files). Proceeded with named standard principles: visual-composition (hierarchy/contrast/figure-ground), color & typography discipline, UX hierarchy (Von Restorff / signal economy). Noted, not blocking.

### Verdict summary
Theme execution does NOT match the technical-instrument target. The skin is a partial re-palette: the warm-paper canvas, hairline borders, 3px card radius, and accent index numerals (01-04) landed correctly, but the dashboard retains the ORIGINAL light-skin's high-chroma data viz (multi-color donut rings, multi-color trend lines), blue gradients (logo mark, avatar, AI-card header, AI avatar), the saturated blue anatomical figure, and several invented off-palette tint chips (green #DFEAE2, blue #EEF0FE). Orange is used as TEXT in multiple places, violating the "marks/graphical only, never text" rule AND failing WCAG. This is why it reads as "not what I was looking for": the instrument target is monochrome-ink + sparse-orange-mark + flat; the result is still the colorful clinical dashboard wearing a beige coat.

### Findings (Rule 1 format) — see final report for full text.
Tier 1 (any one blocks): 3 open.
Tier 2: 3 criteria open.
MUST FIX: 6 | SHOULD FIX: 4 | NOTE: 3

---

## Component: Gauge Scratch — segmented radial-tick gauges (node Aepgh)
File: design/a+maxing_designs.pen
Built against: instrument-style reference (stopwatch/speedometer tick bezel); replaces 3 solid-arc donut rings.

Status: IN_PROGRESS (ready for Critic)
Iteration: 2 / 3 (geometry corrected — pivot was misdiagnosed in iter 1)

### Build summary
Parent frame `Gauge Scratch` (Aepgh) at x:11200 y:2700 on inst-canvas, holds 3 transparent layout:none gauge frames, 118x118 each:
- `gauge-recovery` (w3tYL): 60 ticks, 51 active teal ($inst-teal #256457), 9 inactive ($inst-tick-inactive #BCB3A2). 84% arc from 12 o'clock CW.
- `gauge-sleep` (9hUty): 60 ticks, 47 active orange ($inst-accent #E8542A), 13 inactive. 78% arc.
- `gauge-strain` (ArDeN): 60 ticks, 32 active sky ($inst-sky #2C6E9E), 28 inactive. 52% arc.

N = 60 ticks/gauge, every 6 degrees. Each tick = 2x11 rounded rect, OUTER end at radius 57 from center (59,59), extending inward (length 11) toward radius 46. Active run = first ceil(frac*60) ticks from top CW. Center (radius < ~46) left clear for numeral overlay.

### Geometry note (load-bearing) — CORRECTED iter 2
Pencil rotates a rectangle about the MIDPOINT OF ITS TOP EDGE (top-center), NOT the center and NOT the top-left corner. Positive rotation = clockwise. Iter-1's center-pivot and top-left-pivot formulas were both WRONG: they passed a 4-cardinal-point probe (degenerate at 0/90/180/270) but scattered at intermediate angles — only visible at 4x zoom, hidden by anti-alias blur at native 118px. Determined the true pivot empirically with a single rot-0 vs rot-30 bar pair sharing a top anchor.
Correct formula (top-center pivot, outer end pinned at radius 57):
  Px = 59 + 57*sin(theta);  Py = 59 - 57*cos(theta)   (theta = i*6deg, CW from top)
  node top-left:  x = Px - width/2 ;  y = Py ;  rotation = theta
Verified at 4x (a 472x472 verify ring of all 60 ticks) BEFORE rebuilding the real gauges — every tick aims at center, true circle, no scatter.

### Tokens
Added `$inst-tick-inactive` (#BCB3A2) — justified in .design/system.md (no existing token reads on the paper canvas). Reused active colors from existing $inst-teal / $inst-accent / $inst-sky (exact hex matches to brief).

### Self-check (iter 2)
Verified geometry at 4x (clean radial, true circle) then screenshotted all 3 real gauges + composite at native aspect. Each shows: even radial ticks pointing to center, active arc starting at 12 o'clock sweeping CW by the correct fraction, inactive gray reading clearly on #ECE7DC, center clear. Each gauge frame is a fixed 118x118 (square) so each ring is genuinely circular; the composite-view width>height is the parent frame's horizontal layout box, not ring distortion. All scratch/verify/probe frames deleted; placeholder false.
