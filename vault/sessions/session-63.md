---
title: Session 63 — WHOOP/noop ingestion adapter built + wired (read-only sqlite) + model-eval noop-AI-Coach prior art
type: note
owner: Walter McGivney
created: 2026-06-14
last_reviewed: 2026-06-14
status: active
permalink: a-plus-maxing/sessions/session-63
---

# Session 63 (2026-06-14)

Walter directed: "build the whoop. also, update the model-eval plan to consider noop's local AI
Coach approach." One substantive PR (#136) merged to `main` (`9cfbfef`); suite 833/2 (+10 net new
whoop tests). The headline: the fabricated WHOOP scaffold is replaced by a real, **wired**
read-only-sqlite adapter, and its own 6-agent review caught a load-bearing read-only-bypass + two
mutation-survive-green test holes — all fixed + blind-verified.

## What shipped (on `main`, #136)

- **The WHOOP/noop ingestion adapter** (`scripts/ingest/adapters/whoop.py`, bead `mdzq` build half).
  Replaces the fabricated `{metric_name,cycle_start,score}` JSON scaffold with a read-only
  (`sqlite3` `mode=ro` via `Path.as_uri()`) read of noop's documented `whoop.sqlite` `dailyMetric`
  table (`docs/DATA_MODEL.md`, schemaVersion 9), mapping each non-null daily metric →
  `{item, timepoint=day, source="whoop", value}`: recovery / strain[0–21] / hrv (`avgHrv`) /
  rhr (`restingHr`) / sleep-efficiency (`efficiency`) / spo2 (`spo2Pct`) / resp-rate (`respRateBpm`) /
  skin-temp-dev (`skinTempDevC`). NULL columns skipped (honest absence).
  - **Mechanism (ADR-0011 OQ-2/OQ-3, resolved at build) = read-only `sqlite3`, NOT the MCP
    subprocess.** The adapter contract is file-based (`read_readings(export_file)`), so a DB-file read
    fits the ADR-0003 seam with **0 edits** to the shared routine/scheduler; Python-native;
    license-safe (path (a): parse a file the operator owns — ships no noop code). MCP is the
    documented fallback.
  - **Wired** by removing the `UNWIRED` marker — `scheduler._wired_adapters()` on `main` now returns
    `['garmin','healthkit','oura','whoop']`. `scheduler.py` still names no `whoop` token (data-driven
    discovery). The ADR-0003 0-edit invariant held (numstat gates green); this is the FIRST
    live-source (non-JSON) adapter, proving the seam extends past the export-file shape.
  - **`source: whoop`** (device provenance, dedupe-distinct under `(item, timepoint, source)` — a
    Whoop hrv and a HealthKit/Oura hrv on the same day don't collide). The biomarker-PAGE
    `source: wearable` enum (ADR-0011 D4) is the separate page layer. (Operator-ratified the
    `whoop`-vs-`wearable` store-tag call at session open.)
  - **Store-adversarial battery** (mandate) on the whoop path: cross-stream, dedupe (idempotent
    re-run + distinct-day persistence), dedupe-key boundary (value + source), mutation
    (constant-timepoint → RED). Mutation-proven (strain-rescale → RED; constant-timepoint → RED).
- **`docs/model-eval/local-model-evaluation-plan.md`** — new §3.5 + §4b/§8 pointers: noop's AI Coach
  (`Strand/AI/AICoach.swift` + `AIProvider.swift`) as prior art for the local-inference integration
  seam — a BYO-provider protocol (`AIProviderClient`) + an OpenAI-compatible **Custom** provider
  pointing at a local server (Ollama/LM-Studio/llama.cpp `:11434/v1`), consent-gated, sending only a
  compact summary over the same on-device `dailyMetric` data the adapter ingests. Prior art for the
  *integration + context-builder*, NOT the model choice or the safety bar; reference-only under
  noop's PolyForm Noncommercial license (the harness stays a-plus-maxing's own Python).
- **ADR-0011** — OQ-2/OQ-3 marked RESOLVED (read-only sqlite) + an S63 build amendment; the review
  aligned the Confirmation criterion (`source: whoop` + the `(item, timepoint, source)` key) and
  recorded the D4 `confidence`-carry deferral (the store Line-Field-Set has no `confidence` field).

## The #136 review — load-bearing

The 6-agent `/review-pr` + profile-less blind triage (which ran repros) caught real defects in the
orchestrator's own work:
- **SEC-1** — the `mode=ro` read-only guarantee was defeated by a `?`/`#` in the DB path (raw
  f-string URI); the triage's repro found a `#` opened the **wrong file**. Fixed via
  `Path.resolve().as_uri()` (percent-encodes). A load-bearing read-only/license invariant.
- **TEST-1** — 6 of 8 column→item mappings were pinned by presence (`len==1`), not value; a
  transposed mapping (spo2↔resp-rate) shipped a fabricated value on the wrong stream and survived
  green (the S41 fabricated-biomarker class). Fixed: value-assert each stream; mutation-proven.
- **TEST-2** — the `is None` NULL-skip was untested; a `not value` regression would silently drop
  honest zeros (strain=0). Fixed: honest-zero retention test; mutation-proven.
- 7 LEGITIMATE fixed + blind-verified 7/7; 2 OUT_OF_SCOPE beaded (`crgz`); BUG-1 beaded (`ienx`);
  the rest NOT_A_BUG/NOT_ACTIONABLE with documented evidence (the triage correctly rejected BUG-1 as
  V1-single-strap-bounded and HIST-3 option-b as unapproved defensive code).

## Governance / discipline

- **PF-S39-01 (gated-skill) HELD** — #136 + the close PR each got both `/review-pr` and `/merge`
  fresh via the Skill tool (`merge-methodology.md` read fresh; REST rebase under GraphQL throttle,
  full-40-char-SHA guard). Count stays 2.
- **PF-S6-01 (verify-first) HELD, notably** — directly applying S62's disclosed README-authoring
  lesson, this session read noop's ACTUAL source (DATA_MODEL.md, AICoach.swift, AIProvider.swift) +
  the adapter/store/registry contracts BEFORE building. The build was grounded in primary source.
- **PF-S40-01 / PF-S26-01 / PF-S51-01** HELD (blind triage+verify never self-triaged; 7 fixed + 3
  beaded, 0 suppressed; review agents read-only). **PF-S13-01/S37-01** HELD (open from files;
  DOCUMENT_RUBRIC + landmarks re-opened at 8/8.7). Off-main-archive-SHA HELD (S62 contract archived
  at on-main `ea9adcb`).
- **Observed, not promoted:** adding `biomarker_meta` registry rows for the new markers broke 5
  dashboard tests (they use those markers as unregistered exemplars) — caught by the suite, reverted
  + beaded; the build-then-verify mechanism working. The review caught real defects two/three levels
  deep — the layered mechanism working, not a PF.

## Beads

Created `crgz` (P3 — doc-freshness: supersede the stale "Whoop registered-but-unwired" gates in
`docs/spec/adr-0001-adr-0003-spec.md` + the build-plan Wave-4 checkpoint + the T2/T3 recipes) +
`ienx` (P3 — multi-device fail-loud hardening). Closed `1uav` (overtaken-by-events — its
`test_whoop_not_invoked` target was replaced). **`mdzq` stays OPEN**: the build + fixture tests +
adversarial battery merged, but the **real-data E2E validation tail remains** (gated on the operator
installing noop, bonding the strap, and offloading a sample). Correctness/governance tail unchanged.

## Next (S64)

No owed close PR. Forward (operator prioritizes): (1) the WHOOP adapter's **real-data E2E
validation** (`mdzq` tail — gated on the operator bonding the strap to noop + a sample; also unblocks
the LM-02 baseline); (2) the review beads `crgz` + `ienx`; (3) the remaining S61 plans (wiki research
[§8 D3], local-model eval [operator D2/D3/D5]); (4) the correctness/governance tail. LM-01 MD-visit
(2026-07-13) — the 14-day scoped-drift-audit window opens 2026-06-29. Baseline 833/2.
