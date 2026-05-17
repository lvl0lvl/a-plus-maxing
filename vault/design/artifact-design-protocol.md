---
title: HTML Artifact Design Protocol
type: rubric
status: draft
owner: walter
created: 2026-05-16
last_reviewed: 2026-05-16
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/design/artifact-design-protocol-1
---

# HTML Artifact Design Protocol

> **Purpose:** Consistency across all generated HTML artifacts so that
> - reports look and feel the same regardless of which session generated them
> - Walter and his doctor can scan a familiar layout without re-learning each time
> - new Claude sessions know exactly how to produce an artifact without prompting

## Status
**Draft skeleton.** The categories below are placeholders. We refine each section as we generate the first artifacts and learn what works in practice (per the "design from observed friction" principle).

Any session generating an HTML artifact MUST read this file first. If a category here is still TBD, the session should make a defensible choice, note the choice in the artifact, and propose a permanent rule via a `decisions/` entry.

## Artifact Types

| Type | Frequency | Audience | Output Path |
|---|---|---|---|
| Daily anomaly note | as triggered | Walter | `daily/YYYY-MM-DD.md` (markdown only) |
| Weekly review | weekly | Walter | `weekly/YYYY-Www.html` + paired `.md` |
| Monthly review | monthly | Walter | `reviews/monthly/YYYY-MM.html` + `.md` |
| Quarterly review | quarterly | Walter | `reviews/quarterly/YYYY-Qn.html` + `.md` |
| Doctor visit handout | per visit | Doctor | `artifacts/doctor-visits/YYYY-MM-DD.html` |
| Lab result integration | per panel | Walter | `labs/YYYY-MM-DD-panel.md` + paired `.html` |
| Genetic report | once + on update | Walter | `dna/report.html` |
| Protocol change diff | per change | Walter | `decisions/YYYY-MM-DD-{slug}.html` |

## Design System (skeleton — fill as we go)

### Typography
- TBD: serif vs sans, heading scale, body size, line-height

### Color Palette
- TBD primary, accent, semantic (good / watch / concern)
- **Must be print-safe** (doctor handouts may be printed)
- High contrast, accessible (WCAG AA minimum)

### Components (to be specified)
- KPI card — single metric + trend arrow + delta vs target
- Sparkline — small inline trend, 30-90 day window
- Comparison table — current vs target vs prior period
- Timeline — events + labs over time
- Protocol diff — current → proposed, side by side, with rationale per change
- TL;DR banner — opens every artifact

### Layout Rules
- TBD: max width, single-column vs multi, mobile-first?

### File Conventions
- **Single-file HTML.** Inline CSS in `<style>`, inline SVG for charts, no external assets, no CDN dependencies, no JS frameworks
- Must work offline (open from disk, no network)
- Vanilla HTML5, vanilla CSS, minimal vanilla JS only if interactivity is needed
- File size target: under 500KB

### Content Rules
- Every artifact opens with a one-sentence TL;DR
- Every claim cites its source file (e.g., "see `daily/2026-05-14.md`")
- Every recommendation includes confidence level + reversibility note
- No emoji unless explicitly requested by Walter
- Numbers always include units and reference range where applicable
- "Out of range" values flagged with semantic color, never red-only (colorblind-safe)

## When HTML vs Markdown Only
- **HTML** when: spatial layout matters, audience includes anyone other than Walter, comparison/diff content, dashboard-style data display, doctor-facing
- **Markdown only** when: agent's own notes, plain logs, decisions records, internal protocol files, daily auto-logs

## Inheritance Rule
New sessions must read this file before generating any artifact in `artifacts/`, `weekly/`, `reviews/`, `dna/`, or `labs/`. If this file conflicts with a one-off user instruction in the current session, the session instruction wins, and the session must propose a permanent update here via a `decisions/` entry.