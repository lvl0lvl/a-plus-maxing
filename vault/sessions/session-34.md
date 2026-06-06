---
title: Session 34 — Wave-3 render engine (ADR-0004-T1 / gu4)
type: session
created: 2026-06-05
status: complete
permalink: a-plus-maxing/sessions/session-34
---

# Session 34 (2026-06-05) — V1 render engine + template component library (ADR-0004-T1)

One deliverable, one PR, rebase-merged to `main` (PR #53 @ `aa0d9e8`): the V1
data-OUT render engine `render.emit(template, store_read)` + the `component_set.py`
template component library + the dashboard/report templates, built by a dispatched
SE worker through the recipe's 3-cycle/12-step TDD, then a full 6-agent `/review-pr`
+ blind triage + blind verify (PF-S3-01 — load-bearing because ONE SE built
everything). Closed `gu4`; filed `5wo` (the F12 pagination contract gap).

## Published interfaces (durable contract record)

- **`emit(template, store_read) -> Path`** in `scripts/generate/render.py` — assembles a
  template (a module exposing `render(store_read)`, OR a bare callable) against the store
  read model, writes ONE self-contained HTML file with everything inlined (inline CSS +
  inline SVG, 0 external asset references), and RETURNS the path it wrote. The destination
  is engine-owned (`DEFAULT_OUT_DIR = vault/artifacts/generated/`, now gitignored); callers
  pass no output-path argument (a keyword-only `_out_dir` test seam exists, ruled an
  acceptable internal seam by the Contracts review — the published positional surface is
  preserved). Reads operator data ONLY from `store_read`. Before writing, scans every asset
  reference at its syntactic position (asset attributes + CSS `url()`/`@import` inside
  `<style>`) and RAISES `ValueError` on any external (non-`data:`/non-`#fragment`) reference.
  Consumed downstream by `ADR-0004-T2` (extends `render.py` — modifies the file, must
  preserve the signature + boundary), `ADR-0004-T3` (`generate.run` invokes it),
  `ADR-0006-T2` (plan render), `ADR-0007-T2` (views render + reuse the component set).
- **`vault/design/templates/component_set.py`** — the single inline-CSS/SVG component library
  (`head`/`tldr_banner`/`legend`/`kpi`/`sparkline` + the public `state_for(item)` helper) and
  the colorblind-safe semantic palette (good `#117733` / watch `#DDAA33` / concern `#882255`,
  never red-only — the concern state pairs a glyph). `dashboard.py` + `report.py` both assemble
  from it (no per-template color/markup literals). The palette + CIEDE2000 ΔE floor (15.0) +
  the named deuteranopia+protanopia (Viénot–Brettel–Mollon 1999) simulation are recorded
  independently in `vault/decisions/2026-06-05-render-colorblind-safe-palette.md` (a separate
  `docs(decision):` commit, OUTSIDE the 5-file build manifest, per recipe Deviation #1).

## The AC-3 measured-value accessibility gate (the load-bearing falsifiability thread)

`test_contrast_and_colorblind` is the recipe's Wave 3→4 go/no-go. It must turn RED if the
production palette regresses to colorblind-unsafe colors. The **central correctness thread
this session** was that the gate as first built was NOT falsifiable for member-collision drift:

1. The original gate computed the per-adjacent-pair CIEDE2000 ΔE over the DECISION palette
   values (`expected[role]`) — decision-vs-decision, self-referential — and checked palette
   membership as a SUBSET (`rendered <= expected_set`). Both halves passed regardless of what
   the production module rendered.
2. **The orchestrator's pre-review verification gave FALSE CONFIDENCE.** Probe-1 drifted a
   palette hex to a NON-member (`concern → #992266`); the membership check caught it, so the
   gate looked falsifiable. But probe-1 never tested a member-collision.
3. **The 6-agent `/review-pr` Test-Coverage agent caught the real hole by mutation:** drifting
   `good → #DDAA33` (watch's EXISTING hex — two semantic series now render an identical color, a
   genuine colorblind regression) left ALL 11 tests GREEN. The subset-membership check can't
   catch a member-collision, and the ΔE-over-decision can't catch a production drift.
4. **Fix:** compute contrast + per-adjacent-pair CIEDE2000 ΔE over the colors RENDERED into the
   emitted file (`:root` vars / data-driven strokes); assert role→hex EQUALITY vs the decision
   (not subset) + mutual DISTINCTNESS of the three rendered series; make the fixture render all
   three series as data-driven strokes (added `spo2 → watch`). The orchestrator independently
   re-verified by mutation: the `good → #DDAA33` collision now FAILS; a non-member drift FAILS;
   restored PASSES.

Lesson (logged in the S34 PF attestation): when self-verifying a falsifiability gate, test
EVERY failure mode it must catch (member-collision, not only non-member drift). The PF-S3-01
layered-review design is exactly what caught what the orchestrator's single probe missed — the
safeguard earned its keep, as it did on `n9h` (S33).

## Review outcome (PR #53)

6-agent `/review-pr` → 16 deduped findings → 2 blind-triage agents → **12 LEGITIMATE** (all
fixed + 12/12 blind-verified RESOLVED), **1 LEGITIMATE→beaded** (`5wo`), **3 NOT_A_BUG**;
**0 suppressed** (PF-S26-01; the matrix stayed priority-only). The standouts:

- **F6/F7 (TEST, Critical)** — the AC-3 ΔE tautology + subset-membership above.
- **F1 (SEC/HIST, Critical)** — `DEFAULT_OUT_DIR = vault/artifacts/generated/` was NOT gitignored;
  a real render writes operator-data HTML there, so `git add` would land operator PII in the
  tracked trunk (ADR-0005 release-blocking). Fixed: `.gitignore` += `vault/artifacts/generated/`.
- **F2 (SEC/BUG, Critical)** — the external-asset scan (regex over the assembled string) MISSED
  `@import`/`srcset`/`image-set`/`meta-refresh`/`poster` and FALSE-TRIPPED on benign operator
  `url(http://…)` text (F4, blocking the report). Fixed: reworked to an `HTMLParser`-position-aware
  scanner (CSS matched only inside `<style>`).
- **F5 (BUG, Important)** — `write_text` without `encoding=` failed on non-ASCII operator data
  under a non-UTF-8 locale → `encoding="utf-8"`.
- **F12 (API, Critical → BEADED `5wo`)** — `render.emit`'s single-`Path` return + single
  deterministic basename collide with downstream `ADR-0004-T2` AC-2, which requires ≥2 returned
  paths for pagination while forbidding any change to the path-return contract. Architect
  amendment required at the T1→T2 boundary BEFORE T2 is built (not silently inside T2).
- NOT_A_BUG (with cited evidence): F3 (`_escape` omits `"` but no double-quoted operator-data
  attribute sink exists), F13 (overwrite is the intended deterministic fresh-render behavior),
  F14 (both the callable and module template forms ARE documented).

## Recipe↔built drifts (surfaced, not silently followed)

- `/write-tests` is not invocable from a dispatched worker → the SE authored the RED tests directly.
- `rg`/`wc` in-test static scans → implemented as pure-Python (`re`/`pathlib`) for portability.
- The crit-3 palette was genuinely TBD upstream (the design source's Color Palette has zero hex) →
  resolved + recorded in an independent `vault/decisions/` entry (per the design source's line-24
  mandate), committed SEPARATELY (outside the 5-file build manifest); the gate reads its expected
  palette + floor from there (falsifiable on drift).
- `.gitignore += vault/artifacts/generated/` and the `5wo` bead were the two review-surfaced scope
  additions beyond the 5-file manifest (both justified).

## Carried forward

- **`5wo` (F12, P2)** — the `render.emit` pagination contract amendment; resolve before `ADR-0004-T2`.
- **`oaf` (ADR-0003-T3 scheduler)** READY — completes data-IN over the wired adapter set.
- **`ADR-0004-T3` (`generate.run`)** — the first-artifact producer (LM-04); consumes `render.emit`.
- Re-run the render-size measurement against the real template before `ADR-0004-T2`/`ADR-0007-T2`
  consume the cap; the plan-`template` producer (`4xe`). Still open: `1ww`/`qwj`/`1vi`/`ivt`/`z2u`.

Links: [[session-33]] (the wired adapters + the `Adapter` Protocol this session's render engine
reads the store through).
