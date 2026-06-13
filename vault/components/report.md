---
title: report — the Physician Face Sheet template
type: reference
status: active
created: 2026-06-12
last_reviewed: 2026-06-12
review_cadence: on-change
permalink: a-plus-maxing/components/report
---

# report (`vault/design/templates/report.py`)

**What:** the physician-facing artifact template (bead `nsxy`). Renders the
operator-signed face sheet per `vault/design/physician-facesheet-v1-spec.md`
— the v2 body governs section structure/typography/slot shapes, the signed v3
amendment block governs ALL color bindings. A callable
`render(store_read, _today=None) -> html_str`; `generate.run("report")` is
the production entry (the `_today` seam mirrors the dashboard's).

**Page one (the 90-second scan layer), in section order:**
1. Header — title 20px/700, `Prepared <date>` caption (the `_today` seam),
   2px training-blue rule, and the status line: operator INITIALS only
   (parsed from `vault/meta/operator-profile.md`'s title — the full name
   never renders), age BAND + issue status only when the profile fields are
   filled (`_PROFILE_PATH` is the test seam; unfilled/missing -> em-dash
   slots), last review + next visit em-dash (LM-01 gated).
2. Since your last review — training-tint card, training-text title. The
   production path renders the first-visit copy (`No prior review — full
   baseline below`, which doubles as the LM-01 awaiting state per the spec);
   `_triage_row` holds the populated delta-row anatomy (improving = PALETTE
   good ▲/▼; attention = the measured watch pair — watch-text directly on
   training-tint computes 4.31 < 4.5, so attention rows ride watch-tint;
   neutral = ink; unknown kind KeyErrors).
3. Current regimen — with adherence (supplements-teal bar): rows from
   TODAY's `plan::supplements` (`name — dose`) and `plan::peptides`
   (`compound · dose · route`; an `experimental` tag renders the detail in
   watch-text + `experimental — disclosure attached`), `since` = the plan
   reading's timepoint. Adherence = em-dash per row (the 30-day adherence
   aggregate model does not exist; never a fabricated %). No plan today ->
   one digit-free awaiting line.
4. Biomarkers — out of range or trending (`SECTION_ACCENTS["biomarkers"]`
   bar): one concern-tint row per `state_for == "concern"` item — display
   name in PALETTE concern, source-tier glyph (honest: only `manual` maps to
   ○ self-reported today; an unmapped source claims no tier), real
   `value · ref low – high · ±delta/windowd · drawn date` detail, and the
   `watch` chip on the registered watch pair (ONLY out-of-range registered
   markers get it). Then the good-tint collapse strip with the REAL good
   count. No biomarker streams at all -> one awaiting line.
5. Goals & trajectory (`SECTION_ACCENTS["goals"]` bar): awaiting line (no
   goal model).
6. Patient-generated signals — 30-day aggregates (sleep-indigo bar): the
   four stat boxes render STRUCTURE (wearable-tier top edge + glyph/label
   row) with em-dash values — the dashboard's designed-empty precedent;
   LM-02 gated.
7. Asks & agenda (nutrition-orange bar, nutrition-tint card): `Order today:`
   chips for provenance-PENDING `panel::` items (the `read_panel` reversed
   provenance scan over the read model — a landed result is never a pending
   chip); `Patient questions:` = the active peptide protocol's derived
   watch-out questions minus those with stored answers. Muted none-states
   when empty.
8. Footer — tier legend (glyphs ◆/●/○ in the base triple, tier WORDS in the
   `*-text` triple), the honesty line verbatim, generation date.

**Page 2 (detail layer):** every item's readings table, ABNORMAL-FIRST
(concern items lead, then item-sorted), each heading carrying its tier glyph
+ registered ref range caption. `plan::`/`plan-track::` keep the verbatim
heading+table routing (ADR-0010 D5 — no KPI/sparkline); a stream with NO
numeric reading routes table-only (strings never reach numeric viz — the
pre-redesign report crashed on string streams); numeric streams keep
KPI + polyline sparkline + table.

**Contracts:**
- The naive projection NEVER renders here (S52 operator decision; pinned by
  `test_projection_renders_on_dashboard_not_on_report`).
- Colors are `component_set` tokens only (PALETTE/CHROME/ACCENTS/
  SECTION_ACCENTS) with ONE spec-sanctioned exception:
  `_SELF_REPORTED_BASE = "#B7791F"` — the v3 block ships it as NON-TEXT tier
  chrome only (glyph fills, stat-box edges) and closes the registration list
  at four tokens, so it is deliberately not a system token.
- Every store-sourced string passes `cs._escape` at its sink; all attributes
  single-quoted (house escaping convention).
- Single-file zero-script (ADR-0004): inert everything; the shared
  `@media print` block is inherited unchanged and extended with the face
  sheet's own page rules (edge dropped, page-break before page 2). The
  print CONTRACT itself is unchanged.
- AA: every new rendered text/background pair is gate-measured
  (`test_facesheet_rendered_pairs_measure_aa` + the `.tint-watch` rule in
  the main gate's tint walk).

**Reads (pure, via the read model + registries):** `plan_schema.resolve_plan`,
`loop_schema.derive_watchout_questions` + the `_TAG_PANEL` provenance tag,
`biomarker_meta` (ranges, display names, numeric coercion),
`dashboard._format_number/_reading_date/_short_date/_MONTH_NAMES` (shared
formatting — reused, not re-derived). No store writers.

**Called by (production):** `generate.run("report")`.

**Governing:** `vault/design/physician-facesheet-v1-spec.md` (v3 bindings),
ADR-0004 (single-file + print), ADR-0009 D2 (honesty), ADR-0010 D5 (plan
routing).
