---
title: Session 35 — Wave-4 generation entry point (ADR-0004-T3 / 3gp)
type: session
created: 2026-06-05
status: complete
permalink: a-plus-maxing/sessions/session-35
---

# Session 35 (2026-06-05/06) — on-demand + unattended-cron generation entry point (ADR-0004-T3)

One deliverable, one PR, rebase-merged to `main` (PR #55 @ `9cfb607`): the V1
generation entry point `generate.run(artifact_name)` — a thin on-demand +
unattended-cron entry over the merged `render.emit`, built by a dispatched SE
worker through the recipe's 2-cycle/8-step TDD, then a full 6-agent `/review-pr`
+ blind triage + blind verify (PF-S3-01 — load-bearing because ONE SE built
everything). Closed `3gp`; filed `4yk` (publish store cross-item read surface) +
`u8u` (store dir-edge).

## Published interface (durable contract record)

- **`run(artifact_name, *, _root=None, _out_dir=None) -> Path`** in
  `scripts/generate/generate.py` — ONE code path for both the on-demand and the
  unattended/cron entry mode. It assembles the cross-item store read model (the
  flat list `render.emit` consumes), selects the dashboard/report template by
  `artifact_name`, drives exactly ONE `render.emit(template, store_read, _out_dir=…)`,
  and returns the path `emit` wrote. It reads no stdin and prompts for nothing;
  opens no server and binds no listening socket (run-to-completion-and-exit); it
  does not swallow `render.emit`'s external-asset `ValueError` (surfaces a non-zero
  exit, never a partial/served artifact). `main`/`__main__` is the cron-/operator
  surface (`python -m scripts.generate.generate <artifact_name>` -> exit 0). The
  `_root`/`_out_dir` keyword-only seams mirror `emit`'s accepted `_out_dir` seam so
  tests stay hermetic (never touch the real gitignored store / generated dir); the
  published positional surface is `run(artifact_name)`. **A thin leaf** — no
  downstream task plans against `generate.run`'s internals (no outgoing interface
  edges). `render.py` is consumed read-only (unmodified — no ADR-0004-T2 collision).

## The AC-3 NG-4 falsifiability thread (the load-bearing one)

`test_run_binds_zero_listening_sockets` is the recipe's NG-4 go/no-go: it must turn
RED if `generate.run` opens a live server / listening socket. The **central
correctness thread this session** was that the gate as first built was NOT
falsifiable for the realistic breach shape:

1. The original gate monkeypatched `socket.socket.bind/.listen` at the class level in
   the PARENT interpreter and ran `generate.run` in-process — so it observed only
   same-interpreter listens.
2. **The orchestrator's pre-review verification gave FALSE CONFIDENCE.** The probe
   injected an IN-PROCESS listener (caught -> the gate looked falsifiable). It never
   tested a child-process listener.
3. **The 6-agent `/review-pr` Test-Coverage agent caught the real hole by mutation:**
   a listening socket opened in a CHILD PROCESS (an `os.fork()` child OR a freshly-
   spawned `subprocess`/new-interpreter child — the realistic "runs a server/daemon"
   shape) left the gate GREEN, because the parent-only monkeypatch cannot see a
   child's sockets. The orchestrator independently reproduced it (child listener ->
   gate stayed GREEN).
4. **Fix:** a `sitecustomize`-on-PYTHONPATH listen-recorder (wraps `socket.socket.listen`
   only — a bind-only UDP socket is no longer counted, fixing the counter semantics)
   that auto-imports in the observed process, in `os.fork()` children (inherited
   patched class), AND in spawned fresh interpreters (re-imported via inherited
   PYTHONPATH). The gate drives the REAL cron surface as a subprocess and asserts 0
   listens in its tree, with THREE positive controls (same-interpreter, fork-child,
   fresh-interpreter — each asserted > 0) + a negative control (asserted 0), so the
   observer is proven to discriminate across the process boundary. The orchestrator
   independently re-verified by mutation: an `os.fork()`-child listener and a
   `subprocess`-child listener BOTH now turn the gate RED.

Lesson (logged in the S35 PF attestation, carried to Top-3): when self-verifying a
falsifiability gate, test EVERY failure mode it must catch — INCLUDING the
cross-process one, not only the obvious in-process case. This is the same class as
the S34 AC-3 member-collision near-miss. PF-S3-01's layered review caught what the
orchestrator's single probe missed — the safeguard earned its keep a 3rd consecutive
time (n9h S33, gu4 S34, 3gp S35).

## Review outcome (PR #55)

6-agent `/review-pr` (Security PASS, 0 findings) -> 12 deduped findings -> blind
triage -> **9 LEGITIMATE** (all fixed + 9/9 blind-verified RESOLVED), **2
LEGITIMATE->beaded** (`4yk`/`u8u`), **1 NOT_ACTIONABLE** (F10); **0 suppressed**
(PF-S26-01; the matrix stayed priority-only). The standouts:

- **F1/F2 (TEST, the load-bearing pair)** — the AC-3 child-process NG-4 blindness +
  the bind+listen counter over-count, above.
- **F5 (BUG/TEST)** — the AC-4 offline-open walk was vacuous on the real artifact (0
  asset refs -> the urlopen walk never ran -> `egress_run` truthy over a no-op closure).
  Fixed: a positive control runs the SAME walk over an off-host ref and asserts FALSY.
- **F3 (TEST)** — `pytest.raises(Exception)` tightened to `KeyError` (the documented contract).
- **F4 (TEST)** — added a test for the `main` argparse exit-2 path on an unknown name.
- **F6a (TEST)** — pinned the empty-store contract (run over an empty store succeeds).
- **F7/F8 (API/HIST, BEADED `4yk`)** — `generate._read_store` enumerates the store's
  on-disk NDJSON layout (`glob("*.ndjson")` + `p.stem`) because the store publishes
  only per-item `store.read(item)` (no read-all). The Contracts review independently
  reached the same BEAD-AND-PROCEED verdict (the `5wo` precedent); Historical flagged
  it must be a filed bead, not a silent NOTE. `4yk` (P2) = publish `store.read_all`/
  `store.items` (ADR-0002 amendment) + collapse the helper.
- F9/F11/F12 (QUAL) — import hygiene, drop the private `_mock_wraps` access, trim a
  redundant docstring clause.
- NOT_ACTIONABLE: F10 (the `_REF_RE`/`_asset_refs` test harness is a near-copy of
  `test_render.py`'s — deliberate test-file independence; no clearly-correct fix).
- DEFERRED->beaded: `u8u` (P3) — `store.read` raises `IsADirectoryError` on a
  directory named `<x>.ndjson` (pre-existing unchanged store.py; pathological).

## Recipe↔built drifts (surfaced, not silently followed)

- `/write-tests` is not invocable from a dispatched worker -> the SE authored the RED
  tests directly (same as S34).
- The store has no published cross-item read surface, but the templates consume a flat
  cross-item list and `render.emit` takes that list as an argument (the S34 PII-boundary
  decision: emit reads ONLY from `store_read`). So `generate.run` must assemble the
  cross-item model -> `_read_store` enumerates the store layout in one isolated helper,
  `store.py` UNMODIFIED, the coupling beaded (`4yk`). Flagged in the scope contract up
  front; the Contracts review independently endorsed bead-and-proceed.
- GraphQL throttled (limit 0) all session -> REST for PR create + merge; the merge
  readiness check caught the fix commit was unpushed before the merge (the methodology
  catching a real would-have-merged-the-unfixed-head error).

## Carried forward

- **`4yk` (P2)** — publish `store.read_all`/`store.items` + collapse `generate._read_store`;
  ADR-0002 amendment; do before/with `ADR-0004-T2`.
- **`u8u` (P3)** — the store dir-as-`.ndjson` `IsADirectoryError` edge.
- **`5wo` (P2)** — still: `render.emit` single-Path vs `ADR-0004-T2` pagination (blocks `yo6`).
- **`oaf` (ADR-0003-T3 scheduler)** READY — completes data-IN; the `rg "whoop" scheduler.py == 0` Wave 4->5 check lands there.
- The first ARTIFACT (LM-04) lands when `generate.run` is invoked with real operator data (Walter-pending exports) — the producer is now live.
- Still open: `4xe` (plan-`template` + render-size re-measure), `1vi`/`1ww`/`qwj`/`ivt`/`z2u`.

Links: [[session-34]] (the render engine + `render.emit` this session's entry point invokes).
