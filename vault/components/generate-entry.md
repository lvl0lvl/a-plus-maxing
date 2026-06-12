---
title: generate-entry — on-demand + cron artifact entry point
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-11
review_cadence: on-change
permalink: a-plus-maxing/components/generate-entry
---

# generate-entry (`scripts/generate/generate.py`)

**What:** the thin artifact entry point (ADR-0004-T3). `run(artifact_name)` reads the
cross-item store read model via `store.read_all`, selects the template
(`dashboard` | `report`), drives exactly ONE `render.emit`, and returns the written
path. One code path for interactive and unattended/cron use: no stdin, no prompt, no
server, run-to-completion. CLI:
`python -m scripts.generate.generate <artifact> [--root --out-dir]` → prints path,
exit 0.

**Contracts:**
- `_TEMPLATES` is a name→module dict (`"dashboard"`/`"report"` → its template module);
  `run()` raises `KeyError` naming the known set for an unknown artifact name.
- The flat read model comes from the published `store.read_all(root)` (the store owns
  item enumeration + cross-item ordering since the bead-4yk collapse; the local
  `_read_store` helper is gone). This is why ALL stream types (panel/watch-out/feedback)
  reach the dashboard template: routing is the TEMPLATE's job (type-routed since S48),
  not the read model's.
- `render.emit`'s external-asset refusal propagates (non-zero exit, never a partial
  artifact).
- Test seams: `_root`, `_out_dir` keyword-only.

**Called by (production):** the operator (CLI), cron, and the mixed-stream E2E test
(`tests/generate/test_dashboard_mixed_stream.py` — the production-path proof per the
CLAUDE.md verification mandate).

**Governing ADR:** ADR-0004 (T3 entry + T1 engine).
