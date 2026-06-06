---
title: Render Colorblind-Safe Semantic Palette (good/watch/concern) + CIEDE2000 ΔE Floor
type: decision
status: active
owner: walter
created: 2026-06-05
last_reviewed: 2026-06-05
depends_on: [vault/design/artifact-design-protocol.md, docs/task-plan/ADR-0004-T1.md]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/decisions/2026-06-05-render-colorblind-safe-palette
---

# Decision: Render Colorblind-Safe Semantic Palette + Color-Distance Floor

## Context

`vault/design/artifact-design-protocol.md` § Color Palette names the semantic
roles (good / watch / concern) and the constraints (WCAG-AA minimum, print-safe,
"out of range flagged with semantic color, never red-only") but records ZERO hex
values, no color-distance metric, and no numeric threshold. ADR-0004-T1 crit 3
(the Wave 3→4 accessibility go/no-go) asserts that every rendered series color is
a member of "the artifact-design-protocol colorblind-safe semantic palette" and
that adjacent series are spaced above a *stated* deuteranopia/protanopia
color-distance threshold — but the reference set is TBD upstream.

Per the design source's line-24 mandate ("make a defensible choice … and propose
a permanent rule via a `decisions/` entry"), this entry RESOLVES and RECORDS the
concrete reference the ADR-0004-T1 crit-3 test (`test_contrast_and_colorblind`)
reads its expected palette + ΔE floor from. The test reads these values FROM THIS
ENTRY, not from `vault/design/templates/component_set.py`, so the gate is
falsifiable: if the production palette drifts from what is recorded here, the test
fails.

## Decision

**Semantic palette (good/watch/concern hex set).** Drawn from a Paul-Tol–style
colorblind-safe qualitative set, never red-only (the concern state pairs its
color with a glyph in the legend, and out-of-range values carry a semantic glyph):

```palette
good=#117733
watch=#DDAA33
concern=#882255
ciede2000_delta_e_floor=15.0
simulation=deuteranopia+protanopia
```

- **Body text pair (AA contrast):** ink `#1A1A1A` on paper `#FFFFFF` →
  contrast ratio ≈ 17.4 (≥ 4.5 normal-text floor, WCAG-AA). Muted caption
  `#555555` on paper → ≈ 7.46 (≥ 3.0 large-text floor). These two pairs are the
  text colors; the good/watch/concern hexes are series/category colors (chart
  strokes, swatches), not subject to the body-text 4.5 floor.
- **Color-distance metric:** CIEDE2000 ΔE (the modern perceptual color-difference
  formula; closed-form, computed in pure Python — no third-party dependency).
- **Color-vision simulation:** deuteranopia + protanopia, via the
  Viénot–Brettel–Mollon (1999) single-plane dichromat projection applied in
  linear-light sRGB. The ΔE for each adjacent series pair is computed under BOTH
  simulations.
- **ΔE floor:** **15.0**. Every adjacent-series pair, under each simulation, must
  compute a CIEDE2000 ΔE strictly greater than 15.0. This floor sits above the
  "clearly distinguishable colors" perceptual band (well above the ~2.3 JND) and
  below the worst pair the recorded palette actually achieves (the minimum
  observed adjacent ΔE under simulation is ≈ 29.4, watch/concern under
  deuteranopia), so the gate has real headroom yet fails if the palette regresses
  toward dichromat-indistinguishable colors.

## Consequences

- `component_set.py`'s PALETTE good/watch/concern MUST equal the hex set recorded
  here; `test_contrast_and_colorblind` reads the expected set + floor from THIS
  entry and asserts the rendered output against it (falsifiable on drift).
- Follow-up (per the ADR-0004-T1 second UPSTREAM FLAG): promote this recorded hex
  set + CIEDE2000 metric + simulation + numeric floor into
  `vault/design/artifact-design-protocol.md` § Color Palette, resolving its TBD,
  so future render tasks reference a pinned palette rather than re-resolving it.

## References

- vault/design/artifact-design-protocol.md § Color Palette (TBD source)
- docs/task-plan/ADR-0004-T1.md crit 3 + Deviation #1 + the two Upstream Flags
- Viénot F., Brettel H., Mollon J.D. (1999), dichromat color-vision simulation
- CIE (2001), CIEDE2000 color-difference formula
