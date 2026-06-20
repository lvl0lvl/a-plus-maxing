# Screen: Doctor-Visit SBAR Handout — Physician copy (full face sheet)

File: design/a+maxing_designs.pen
Root node: OSBCp (frame "Doctor Visit Handout — Physician copy", 820w, x:940 y:8000)
Theme: clinical (Clinical Light)
Authoritative structure: medical-liaison design §9.4 + vault/design/physician-facesheet-v1-spec.md
("Page-one sections, in order").
Sibling: u5XdT (the patient "prep" copy) sits to the LEFT at x:0; 120px gap, non-overlapping.

Approval status: PENDING — iteration 2 (extended to the full populated face sheet); ready for
Design Critic re-review. Prior: APPROVED at iteration 1 (the SBAR-shaped physician copy).

## What it is
The clinician-facing patient face sheet — scannable in ~90s, leading with deltas, adherence,
abnormal biomarkers. Same locked Clinical Light print-native white page. Renders NO clinical
verdict. Neutral third-person. This is a MOCKUP showing the FULL POPULATED design; production
gates the not-yet-modeled sections (adherence %, deltas, signal aggregates, goals) behind honest
em-dash awaiting-states per the spec's gating rules — here sample slot data is shown so the
operator sees the design.

## Spec alignment note (Clinical Light mapping)
The spec's v3 amendment standardizes data-state color to the dashboard PALETTE (concern/watch/good
+ measured tints) and registers two section accents (biomarkers, goals). This Pencil mock works in
the file's Clinical Light token system per the operator brief, mapping the spec's data-states 1:1:
abnormal/out-of-range → $clin-rose + $clin-rose-bg; watch/attention/below-threshold → $clin-amber +
$clin-amber-bg; in-range/on-track/improving → $clin-teal + $clin-mint-bg; source tiers ◆ lab-grade
(sky) / ● wearable (teal) / ○ self-reported (amber). Glyph/shape redundancy kept (print/mono guarantee).

## Sections (top → bottom) and node ids
| # | Section | Node | Accent bar | Notes |
|---|---------|------|-----------|-------|
| — | Header | u4bJs | 2px $clin-indigo rule | "Patient Visit Summary" + caption + identity + provenance |
| ② | Reason for visit & review status | bKDzA | $clin-indigo | first line "No prior review — full baseline below" + 3 ranked reasons |
| ③ | Current regimen — with adherence | GMcT8 | $clin-teal | table XKgwt now 7 cols incl. Adherence (100% teal chips, "92% · 2 missed" amber, "not started" muted); BPC-157 row CEgWy spill-free; recent-changes subline |
| ④ | Flagged interactions & contraindications | VSzTf | $clin-rose | 3 severity rows WATCH→MONITOR→MONITOR; kept right after regimen |
| ⑤ | Biomarkers — out of range or trending | bSWXX | $clin-rose | 3 abnormal rows on $clin-rose-bg (marker name $clin-ink/700, value line, ◆ sky glyph, amber `watch` chip); mint in-range collapse strip ("full table on page 2", NO sparkline wording) |
| ⑥ | Goals & trajectory | OTjRV | $clin-teal | 4 rows + status chip (on track/improving = mint; needs attention = amber) |
| ⑦ | Patient-generated signals — 30-day aggregates | 5lNMU | $clin-indigo | 4 stat boxes; each 3px source-tier top edge + tier glyph + 15/700 value + arrow (HRV/Resting HR/Sleep wearable-teal; Training days self-amber, "– flat") |
| ⑧ | Patient-reported observations | jzBsm | $clin-sky | "Patient observation — not a diagnosis" chip + 2 rows |
| ⑨ | Asks & agenda | cgvIt | $clin-amber | no-verdict note + "Order today:" + 6 bordered draw chips + "Patient questions:" + 4 numbered questions (ordinals $clin-ink) |
| — | Footer | usNla | top divider | source-tier legend (◆/●/○) + honesty + "not a medical record" provenance |

## Components / patterns
Reuses the section/accent-bar/table/chip sub-patterns ($clin-surface-2 card, cornerRadius 12,
$clin-line stroke, 4px accent bar; table = frame rows/cells; tint-bg chips with dark $clin-ink word).
NEW patterns: biomarker abnormal row (rose-tint card + left value stack + ◆ glyph + watch chip);
signal stat box (clipped vertical frame, 3px tier-colored top edge, tier glyph+label row, value+arrow
row). No library component instanced; custom table justified (no library table).

## Tokens used
$clin-surface, $clin-surface-2, $clin-line, $clin-ink, $clin-ink-2, $clin-indigo, $clin-teal,
$clin-rose, $clin-rose-bg, $clin-sky, $clin-sky-bg, $clin-amber, $clin-amber-bg, $clin-mint-bg.
Fonts: $font-ui (Inter via clinical theme).

## Constraint compliance (screenshot-verified)
- No sparklines (in-range strip wording is "full table on page 2").
- AA: ALL data-state color rides chip/bar/tint chrome with dark $clin-ink text, or ≥14px-bold
  section headers; biomarker marker names $clin-ink (not rose); rose/amber/teal NEVER small text
  on white. Captions $clin-ink-2; $clin-ink-3 not used on essential text.
- Colorblind/print-safe: every state carries a glyph (◆/●/○/✓/▲/▼/–) or word (watch / on track /
  needs attention / experimental).
- No clinical verdict: ⑨ = questions/requests + disclaimer; header provenance line; footer "not a
  medical record".
- Synthetic data; operator initials W.M. only; no contact info.

## Placeholder slots
None — full populated mockup. (Production awaiting-states per spec gating are out of scope for the mock.)
