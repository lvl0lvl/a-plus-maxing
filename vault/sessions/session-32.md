---
title: Session 32 — Store-hardening (8s6) + Wave-3 ingestion (ADR-0003-T1)
type: session
created: 2026-06-05
status: complete
permalink: a-plus-maxing/sessions/session-32
---

# Session 32 (2026-06-05) — Store-hardening + Wave-3 ingestion

Two sequential deliverables, two PRs, each through a dispatched SE worker + a
full 6-agent `/review-pr` + blind triage + blind verify (PF-S3-01), each
rebase-merged to `main`:

1. **`8s6` (P1 store-durability)** — PR #46, merged at `9d476d7`. Completed the
   corruption-tolerance the PR #44 review had deferred.
2. **`6be` (ADR-0003-T1, Wave 3 ingestion)** — PR #47, merged at `5ca684e2`. The
   shared ingestion routine + adapter interface, built on the merged-hardened store.

Closed `8s6` + `6be`. Frontier advanced: `6be` unblocked `n9h` (ADR-0003-T2 adapters).

## PR #46 — store-hardening (`8s6`)

The store's `_read_lines` did a bare `json.loads` per line and `append` wrote in
non-atomic `"a"` mode, so one torn/partial line bricked an item's read AND append
(the brick was partly self-inflicted by the non-atomic append). Fixed:

- **`scripts/store/store.py` `_read_lines`** — skips a malformed line (`JSONDecodeError`)
  AND (review-completed) a valid-JSON-but-non-conformant line (a non-dict, or a dict
  missing a Line Field Set field), warning once per skip on the pinned stderr channel
  `STORE-SKIP: <path>:<1-based-lineno>` (parallels `pii_scan`'s `PII-HIT:`). So `read`
  (sort) and `append` (dedupe) only ever see conformant dict readings.
- **`append`** — validate → dedupe → rewrite the well-formed lines + the new line to a
  temp sibling, `fsync`, then `os.replace` (atomic on POSIX; a crash leaves the complete
  old or complete new file, never a torn line; fsync makes the new bytes durable first).
  Self-heals (drops malformed lines on the next write). `append`/`read` signatures and
  `keying.py` unchanged.

**Review (PR #46):** 13 legitimate findings (all fixed + blind-verified RESOLVED; 1
NOT_A_BUG — the self-heal drop is the approved policy; 0 suppressed). The load-bearing
pair: the original fix only handled `JSONDecodeError`, not a valid-JSON-non-conformant
line — three agents independently caught that the corruption class was half-closed.

## PR #47 — Wave-3 ingestion (`6be`, ADR-0003-T1)

### Published interfaces (durable contract record)

- **`scripts/ingest/adapter.py`** — `Adapter` (a `@runtime_checkable typing.Protocol`;
  the recipe left base-class-vs-Protocol to implementer discretion). The frozen export
  contract every adapter implements:
  - `source_tag(self) -> str` — the per-adapter source-identity DECLARATION. Consumed by
    `ADR-0003-T2` adapter conformance + any future routing/registry; **`ingest.run` does
    NOT call it** — readings self-carry their `source` field. (Documented after the review
    flagged it as published-but-unconsumed.)
  - `read_readings(self, export_file) -> Iterable[dict]` — yields Line-Field-Set readings.
  - `READING_FIELDS = keying.LINE_FIELDS` re-exported (single source of truth).
- **`scripts/ingest/ingest.py`**:
  - `run(adapter, export_file, root=store.DEFAULT_ROOT)` — reads via the adapter, writes
    each reading through `store.append`.
  - `manual_entry(item, reading, root=...)` — operator fallback; raises `ValueError` if
    `item` disagrees with `reading["item"]` (the file written and the stored `item` cannot
    diverge).
  - `import_csv(path, root=...)` — parses + validates the WHOLE CSV before any write
    (all-or-nothing): header must cover `LINE_FIELDS`; a ragged row (extra columns →
    `csv.DictReader` `None` key) or a missing/empty required field raises `ValueError` and
    writes nothing.
  - All three funnel through one internal `_store_reading(reading, root)` → `store.append`.
    **Dedupe is inherited through `store.append`** (which owns the single `keying.dedupe_key`
    call); ingest imports no keying and defines no key (Risk N3 single-key holds; `def .*key`
    under `scripts/ingest/` = 0). No raw NDJSON write, no model step (`egress_guard.run` over a
    real `ingest.run` is truthy; static model/API-client token scan = 0).

### Recipe↔built drifts (surfaced, not silently followed)

- The recipe text says `egress_guard.run(callable)`; the built guard is `run(operation)` (a
  zero-arg closure) — built to the real signature.
- `rg` is a non-executable shell shim on this host (`subprocess.run(["rg",...])` → FileNotFoundError),
  so the recipe's `rg "def .*key"`=0 (crit-3) and `rg` model-token=0 (crit-5 Half-B) static gates
  are implemented in pure-Python (same documented deviation `pii_scan.py` took). Committed
  positive-control tests prove the scans are failing-capable (detect a planted `def make_key` /
  `import openai`).
- `/write-tests` is not invocable from a dispatched worker — the SE authored the RED tests directly.
- **Additive `root=` kwarg** on `run`/`manual_entry`/`import_csv` (not in the recipe's frozen
  positional surface) — mirrors `store.append`/`read`; safe for the positional `ADR-0003-T2`/`T3`
  consumers + the 0-shared-routine-edit diff proof. A contract-text reconciliation the read-only
  recipe could not carry; noted here.

**Review (PR #47):** 22 legitimate findings (all fixed + blind-verified RESOLVED; 0 suppressed),
including **one CRITICAL** the review earned its keep on:

- **SEC-001 (CRITICAL) path traversal** — an untrusted CSV/manual `item` became the store
  filename `f"{item}.ndjson"` with no containment (`item="../escaped/pwn"` or an absolute path
  wrote OUTSIDE the gitignored store). Fixed at the single chokepoint: `store._item_path` now
  resolves the target and raises `ValueError` unless `target.parent == root.resolve()` (rejects
  `../x`, absolute, and `a/b`; an empty item maps to `root/.ndjson`, inside root, allowed). This
  guards read + all three write paths. Stated security motivation satisfies the
  no-defensive-programming gate.
- Plus the `import_csv` validation cluster, the uniform missing-field `ValueError`, the
  `manual_entry` divergence guard, the committed static-scan/AC-6 controls, the egress
  sandbox-availability skip-guard, and the docstring/contract corrections.

## Carried forward

- **`1vi` (P3, NEW):** a re-ingest (CSV/manual) cannot correct a stored reading's value — the
  dedupe key is `(item, timepoint, source)` (ADR-0002), value excluded, so a same-identity
  re-entry with a corrected value silently dedupes away (pinned as first-write-wins by a
  committed test). A value-edit workflow is a render/edit-layer product decision (ADR-0004+),
  not a keying change. Not blocking V1.
- Still open from PR #44: `1ww` (P2 concurrent-append race — premature for single-operator V1),
  `qwj` (P2 PII-free-trunk vault-prose operator name — before V1 ships), `ivt`/`z2u` (P3).
- Wave-3 frontier next: `n9h` (ADR-0003-T2 wired adapters — implement the `Adapter` Protocol;
  the 0-shared-routine-edit proof diffs `adapter.py`/`ingest.py`), `oaf` (ADR-0003-T3 scheduler —
  invokes `ingest.run`). Parallel-ready: `gu4` (render), `xlu` (pre-commit hook — resolve `qwj`
  first), `br1` (router spike).

Links: [[session-31]] (Wave 2 — the store + guard this session hardened + built on).
