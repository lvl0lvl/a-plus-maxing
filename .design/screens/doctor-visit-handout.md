# Screen: Doctor-Visit SBAR Handout

File: design/a+maxing_designs.pen
Root node: u5XdT (frame "Doctor Visit Handout", 820w, x:0 y:8000)
Theme: clinical (Clinical Light)
Authoritative structure: medical-liaison design §9.4

Approval status: APPROVED (Critic, iteration 2). Post-approval operator-review defect fix applied — see below.
Sibling: OSBCp (physician copy) sits to the RIGHT at x:940; 120px gap, non-overlapping.

## Post-approval fix (operator review) — BPC-157 regimen row cell-overflow
The "experimental — disclosure attached" amber chip overflowed the Why column into Source
("○ self" overlapped the chip). Fixed within the Why cell: chip shortened to "experimental",
"disclosure attached" re-expressed as a muted $clin-ink-2 caption (node 0SaLQ) wrapping below
the chip; chip padding [3,8]→[3,7]; BPC-157 row (6KJJU) alignItems center→start. Screenshot-
verified at the row (6KJJU) and whole table (tujH7): no overlap, no column-boundary crossing,
row grew cleanly, other rows unshifted. First-person "my prep" framing intentionally retained.

## What it is
One-page, print-native, SBAR-structured doctor-visit handout. Renders NO clinical
verdict — surfaces questions/requests + source-attributed facts only. Physician-
scannable in ~90 seconds. The page IS the print form (white page, no app chrome).

## Sections (top → bottom) and node ids
| Section | Node | Accent bar | Notes |
|---------|------|-----------|-------|
| Header | mtDRC | — (2px $clin-indigo rule) | title, right caption, W.M. status line |
| 1. Situation | CUp61 | $clin-indigo | 3 numbered ranked one-liners |
| 2. Background — regimen | KPIT0 | $clin-teal | custom table tujH7 (6 col, 5 rows) + amber BPC-157 row 6KJJU + recent-changes subline |
| 3. Background — interactions | msazv | $clin-rose | 3 severity rows; WATCH (amber) / MONITOR x2 (sky) chips |
| 4. Assessment | dO5FE | $clin-sky | "Patient observation — not a diagnosis" chip + 2 rows |
| 5. Recommendation | i1ZF0 | $clin-amber | no-verdict note line + 4 numbered requests |
| Footer | JXx8J | — (top divider) | source-tier legend (◆/●/○) + honesty + generated lines |

## Components / patterns
- No library component instanced directly — handout is custom frames built reusing the
  VISUAL LANGUAGE of comp/SpecRow (k69J6), comp/PlanCard (b0mE0: $clin-surface-2 card,
  cornerRadius 14, 1px $clin-line stroke, icon-chip + tint-bg chip), comp/LabMarker (dwDVR),
  comp/GoalRow (NBI78).
- Custom table (regimen-table tujH7): justified — the library has no table component.
  Hierarchy = table → row (frame) → cell (text, fixed-width). Header widths: Agent 200,
  Dose 62, Route 50, Freq 56, Why fill, Source 60.
- Chip pattern: tint-bg frame + tint-color 1px stroke + dark $clin-ink word, cornerRadius 6-7.

## Tokens used
Colors: $clin-surface, $clin-surface-2, $clin-line, $clin-ink, $clin-ink-2, $clin-ink-3,
$clin-indigo, $clin-teal, $clin-rose, $clin-sky, $clin-amber, $clin-amber-bg, $clin-sky-bg.
Fonts: $font-ui (Inter via clinical theme).

## Constraint compliance (screenshot-verified)
- No sparklines (print doc; numeric/word only).
- AA (iter 2 correction): essential body/captions are $clin-ink (16:1) or $clin-ink-2 (6.0:1).
  $clin-ink-3 (#9AA1B4, ~2.5:1) is NOT AA-safe and now carries ONLY the footer tier-legend glyph
  labels (glyph+word carve-out). Amber/teal never small text on white — ride chips/bars/tints with
  dark ink, or footer glyphs paired with shape+word. Recommendation ordinals set $clin-ink (not amber).
- Colorblind/print-safe: every color state carries a glyph (◆/●/○) or word (WATCH/MONITOR).
- No clinical verdict: Recommendation = questions/requests + explicit disclaimer line.
- Synthetic data; operator initials W.M. only; no contact info.

## Placeholder slots
None. All values are the brief's specified slot-shape sample data.
