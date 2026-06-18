# Design System Notes

## File
design/a+maxing_designs.pen — "Technical Instrument on warm paper" skin.
Token names in this file are bare (`$inst-teal`), NOT `$--` prefixed. Match the file's convention.

## Tokens used by gauge scratch work
| Token | Value | Role |
|-------|-------|------|
| `$inst-canvas` | #ECE7DC | warm paper dashboard background |
| `$inst-teal` | #256457 | gauge-recovery active arc |
| `$inst-accent` | #E8542A | gauge-sleep active arc |
| `$inst-sky` | #2C6E9E | gauge-strain active arc |

## New token (justification, Context Loading rule)
| Token | Value | Why new |
|-------|-------|---------|
| `$inst-tick-inactive` | #BCB3A2 | Recessive radial-tick color for instrument gauges. No existing token expresses it: `$inst-line` (#D6CFBE) is too light to read on the #ECE7DC paper canvas. This warm gray is reused across all three gauges, so it is a real shared token rather than a one-off. |

## Pencil rotation pivot (load-bearing, learned the hard way)
A rotated rectangle in this Pencil build pivots about the MIDPOINT OF ITS TOP EDGE (top-center) — not its center, not its top-left. Positive `rotation` is clockwise. For a radial tick of width w pinned by its OUTER end at radius R, angle theta (CW from top, center (cx,cy)):
  Px = cx + R*sin(theta);  Py = cy - R*cos(theta);  node x = Px - w/2; node y = Py; rotation = theta.
Do NOT validate a radial layout with only 0/90/180/270 probes — those are degenerate and pass under several wrong pivot models. Validate at an intermediate angle (e.g. 30/45 deg) and at high zoom (small ticks blur their error away at native size).
Dashed ellipse strokes are NOT a substitute: `dashPattern` (and `cap:"butt"`) are silently dropped on ellipse strokes here — a swept arc renders solid with pie end-lines, not a tick bezel.
