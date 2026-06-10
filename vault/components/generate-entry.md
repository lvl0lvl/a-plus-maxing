---
title: generate-entry — on-demand + cron artifact entry point
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-10
review_cadence: on-change
permalink: a-plus-maxing/components/generate-entry
---

# generate-entry (`scripts/generate/generate.py`)

**What:** the thin artifact entry point (ADR-0004-T3). `run(artifact_name)` assembles
the cross-item store read model, selects the template (`dashboard` | `report`), drives
exactly ONE `render.emit`, and returns the written path. One code path for interactive
and unattended/cron use: no stdin, no prompt, no server, run-to-completion. CLI:
`python -m scripts.generate.generate <artifact> [--root --out-dir]` → prints path,
exit 0.

**Contracts:**
- `_TEMPLATES = {"dashboard", "report"}` — unknown name KeyErrors.
- `_read_store(root)` enumerates `*.ndjson` under the root and concatenates per-item
  reads into the flat read model — a DOCUMENTED coupling to the store's on-disk layout
  (replace in one line when a published `store.read_all` exists). This is why ALL stream
  types (panel/watch-out/feedback) reach the dashboard template: routing is the
  TEMPLATE's job (type-routed since S48), not this enumerator's.
- `render.emit`'s external-asset refusal propagates (non-zero exit, never a partial
  artifact).
- Test seams: `_root`, `_out_dir` keyword-only.

**Called by (production):** the operator (CLI), cron, and the mixed-stream E2E test
(`tests/generate/test_dashboard_mixed_stream.py` — the production-path proof per the
CLAUDE.md verification mandate).

**Governing ADR:** ADR-0004 (T3 entry + T1 engine).
