---
title: store — local NDJSON time-series store
type: reference
status: active
created: 2026-06-10
last_reviewed: 2026-06-12
review_cadence: on-change
permalink: a-plus-maxing/components/store
---

# store (`scripts/store/store.py` + `scripts/store/keying.py`)

**What:** the local append/read time-series store. One `.ndjson` file per item under the
gitignored store root (`vault/store/` = `store.DEFAULT_ROOT`). Local file I/O only — no
network, no model step (ADR-0001 → ADR-0002).

**Contracts:**
- `keying.LINE_FIELDS = (item, timepoint, source, value)` — the closed Line Field Set
  every store line carries; the ONLY key definition in the codebase (ADR-0002-T0).
- Dedupe identity = `(item, timepoint, source)` — value EXCLUDED, so a re-append of the
  same tuple is an idempotent no-op (`keying.dedupe_key`). Distinct same-timepoint
  entries need a varying source (see `loop_schema._content_tag`).
- `store.append(item, reading, root)` — validates conformance, atomic rewrite
  (temp sibling → fsync → `os.replace`), self-heals malformed lines.
- `store.read(item, root)` — returns conformant readings sorted lexicographically by
  `timepoint` (assumes UTC-offset timestamps). Malformed lines skipped with a
  `STORE-SKIP: <path>:<line>` stderr signal (a consumer-visible channel). A directory
  named `<item>.ndjson` under the root raises `IsADirectoryError` out of `read`
  (`read_all` propagates) — fail-fast at the storage boundary, not guarded (bead u8u,
  convention default).
- `store._item_path` rejects any item whose path is not a direct child of the root
  (path-escape guard); `::`-prefixed items are direct children (legal).
- `store.items(root)` — sorted item slugs under the root (owns the one-`.ndjson`-per-item
  layout knowledge); enumeration is by NAME only — a directory named `*.ndjson` is
  enumerated as an item, deliberately unfiltered (its `read` raises, per the fail-fast
  contract above). `store.read_all(root)` — the flat cross-item read model,
  item-name-sorted outer order, timepoint-sorted within item. `read_all` delegates
  through `read`, so the STORE-SKIP channel passes through unchanged (bead 4yk;
  ADR-0002 v1.3 amendment).

**Called by (production):** `loop_schema` (all writers/readers), `generate.run`
(via `store.read_all`), ingest adapters, router tests/seeds.

**Governing ADR:** ADR-0002 (store), ADR-0003 (ingestion keying).
