---
source-specs: [docs/spec/adr-0052-widen-roster-spec.md]
adrs: [ADR-0052]
created: 2026-07-19
status: approved
total-waves: 2
critical-path-length: 2 tasks
estimated-effort: 3 task-days
---

# Build Plan: ADR-0052 — Widen the Plan-Authoring Roster to the Always-On Ten

This plan wave-schedules the three tasks of `docs/spec/adr-0052-widen-roster-spec.md` (widen the EFFECTIVE plan-authoring roster of the `/generate-plan` front door from the effective four to the always-on ten). All software: two production edits under `scripts/` (`scripts/model/client.py` T1; `scripts/plan/activation.py` + `scripts/serve/plan_loop.py` T2) plus their tests, and one new integration test (`tests/serve/test_plan_roster_widening.py` T3). The substrate is the project venv Python over the checked-in tree; tooling is `pytest`, `rg`, `git`. This is a `$0` mock/fixture build — no live SDK call, no spend; the operator-present LIVE run is an out-of-scope downstream checkpoint (spec Test Strategy). The frozen ADR-0032 `<always-frozen>` core + `track.py` stay byte-frozen (numstat = 0 vs `3ab1c3abb6c995fbaaadcb179735759e4a61d73d`); `RENDERABLE_DOMAINS` / `_PLAN_VALIDATORS` stay four (RT-009); `scripts/serve/server.py` and `scripts/serve/care_chat.py` are NOT modified (the grounded `synthesize(active, …)` leg already carries the full active set — spec Repo-Grounding Ledger T3 RGC-2, Stale-Premise-Reconciled). Every fixture is synthetic (PUBLIC repo).

## Infrastructure Prerequisites

| Prerequisite | Purpose | Verification Command |
|-------------|---------|---------------------|
| Project venv Python (3.14, per `.venv`) | Every task runs `pytest` and pure-function probes | `.venv/bin/python --version` |
| `pytest` + `jsonschema` in `.venv` | Every wave checkpoint runs `pytest` over the task's test files | `.venv/bin/python -c "import pytest, jsonschema"` |
| `git` on PATH with the repo initialized | The frozen-surface `git diff --numstat 3ab1c3ab …` mechanical assertion in every task | `git rev-parse --is-inside-work-tree` |
| `rg` (ripgrep) on PATH | Contract-symbol grounding scans across criteria | `rg --version` |
| Session test baseline recorded | The regression gate is "0 NEW failures vs baseline"; the baseline pre-existing reds must be recorded before Wave 1 | `.venv/bin/python -m pytest -q 2>&1 \| tail -1` (record the passed/failed counts) |

**Baseline note (BP-08 avoidance — no phantom infrastructure):** there is no server, no network, no egress harness in this build. Every checkpoint command is a `pytest` run or a pure `git`/`python` probe over the checked-in tree. The two entry points (T1, T2) are file-disjoint and need no shared substrate beyond the venv.

## Wave Schedule

Built from the spec's Dependency Map (`{ADR-0052-T1, ADR-0052-T2} → ADR-0052-T3`), independently re-confirmed acyclic by Kahn's (all 3 nodes ordered, 0 remain; the create-spec Phase-6 judge scored Dependency-Map Integrity 10/10). Two waves: the two file-disjoint entry points in parallel (Wave 1), then the composition gate that depends on both (Wave 2). Wave wall-clock = the max single-task estimate in the wave (tasks run in parallel). Critical path = `T1 → T3` (equal-length `T2 → T3`), 2 tasks.

### Wave 1: Authorable-Domain Widening + Unconditional Floor

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0052-T1 | Map the six always-on rich domains into `_AUTHOR_CONTRACT_SECTION` | SE | 0.5-1 day |
| ADR-0052-T2 | Raise the `active_plan_domains` floor to the always-on ten, UNCONDITIONALLY | SE | 1-1.5 days |

**Files (disjoint — fully parallel):** T1 → `scripts/model/client.py`, `tests/model/test_client.py`. T2 → `scripts/plan/activation.py`, `scripts/serve/plan_loop.py`, `tests/serve/test_plan_loop.py`, `tests/serve/test_orchestrator_synthesize.py`. No file is touched by both tasks (spec Shared-file coordination).

**Entry Criteria:**
- All Infrastructure Prerequisites pass verification; the session test baseline (passed/failed counts) is recorded.
- `git diff --numstat 3ab1c3abb6c995fbaaadcb179735759e4a61d73d -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py scripts/plan/track.py` prints nothing (frozen surface clean at wave entry).

**Exit Criteria / Checkpoint (machine-runnable Go/No-Go):**
- **T1 authorability:** `.venv/bin/python -c "from scripts.model import client; [client._contract_section(d) for d in ('workout','nutrition','peptides','supplements','endocrine','cardiovascular','recovery','sleep','longevity','mental-performance')]; print('OK')"` prints `OK` (all ten resolve, no `ValueError`), and `.venv/bin/python -c "from scripts.model import client; assert set(client._AUTHOR_CONTRACT_SECTION)=={'workout','nutrition','peptides','supplements','endocrine','cardiovascular','recovery','sleep','longevity','mental-performance'}; print('OK')"` prints `OK`.
- **T2 unconditional floor (the AR-006 partial-signal probe):** a partial-signal surface touching only `workout` returns a superset of the always-on ten — asserted by `tests/serve/test_plan_loop.py` (spec T2 AC-2), and `.venv/bin/python -c "from scripts.plan import activation; assert activation.ALWAYS_ON_DOMAINS <= activation.CARD_DOMAINS and len(activation.ALWAYS_ON_DOMAINS)==10 and (activation.CARD_DOMAINS - activation.ALWAYS_ON_DOMAINS)=={'dermatology','gi','lymphatic'}; print('OK')"` prints `OK`.
- **T2 coupled-test migration:** `.venv/bin/python -m pytest tests/serve/test_orchestrator_synthesize.py -q` passes (the two floor-coupled tests moved to the ten-domain floor — spec T2 AC-7; else the suite cannot stay green).
- **Unit suites green:** `.venv/bin/python -m pytest tests/model/test_client.py tests/serve/test_plan_loop.py tests/serve/test_orchestrator_synthesize.py -q` passes.
- **Frozen surface unchanged:** the same `git diff --numstat 3ab1c3ab … -- <six + track.py>` prints nothing (spec T1 AC-5 / T2 AC-8).
- **No new regression:** `.venv/bin/python -m pytest -q` shows 0 NEW failures vs the recorded baseline.
- **Verifier:** QA always (whole-wave diff); Architect conditional (the `_AUTHOR_CONTRACT_SECTION` map + the activation-vocabulary contract); plan-integrity gates the wave transition.

**Wall-clock estimate:** 1.5 days (T1, T2 in parallel).

---

### Wave 2: End-to-End Composition Gate

**Tasks:**
| Task ID | Title | Agent | Est. Effort |
|---------|-------|-------|-------------|
| ADR-0052-T3 | End-to-end composition gate — ten authored into `plan-model::`, render stays four | SE (+ QA test-strategy) | 1-1.5 days |

**Files:** CREATE `tests/serve/test_plan_roster_widening.py`. No production code (T1 + T2 + the already-wired `care_chat.synthesize(active, …)` compose to the widened authoring — spec T3 files note).

**Entry Criteria (Wave-1 checkpoint GREEN — a wave does not open on a skipped/reasoned checkpoint):**
- Wave-1 exit criteria all passed run-and-observed AND the Wave-1 PR merged to `main` (`git log --grep` the T1 + T2 task IDs on main).
- T1's `_AUTHOR_CONTRACT_SECTION` carries the always-on ten and T2's `activation.ALWAYS_ON_DOMAINS` is defined (Wave-2's fixture drives the real `_do_generate_plan` path that depends on both).

**Exit Criteria / Checkpoint (machine-runnable Go/No-Go):**
- **Composition ≥10 (placement, not existence):** `.venv/bin/python -m pytest tests/serve/test_plan_roster_widening.py -q` passes — a generation over an all-signal fixture records authored programs for ≥10 domains in the composed `plan-model::` version (the four renderable + the six always-on rich, each present by domain key), on a store seeded hold-free (spec T3 AC-1/AC-2).
- **Render stays four:** the same run asserts `len(plan_schema.RENDERABLE_DOMAINS) == 4` and the set unchanged (spec T3 AC-3 — the widening is authoring, not rendering).
- **Floor ↔ authorable coherence:** `set(activation.ALWAYS_ON_DOMAINS) == set(client._AUTHOR_CONTRACT_SECTION)` (spec T3 AC-4).
- **Progressive non-fabrication:** an empty-state surface authors no §11-§13 (`dermatology`/`gi`/`lymphatic`) program (spec T3 AC-5).
- **Frozen surface unchanged:** `git diff --numstat 3ab1c3ab … -- <six + track.py>` prints nothing (spec T3 AC-6); additionally `git diff --numstat main -- scripts/serve/server.py scripts/serve/care_chat.py` prints nothing (the no-server.py/care_chat-edit reconciliation held).
- **No new regression:** `.venv/bin/python -m pytest -q` shows 0 NEW failures vs baseline.
- **Verifier:** QA always (composition-gate test strategy + placement assertions); Architect conditional (the `plan-model::` placement contract); plan-integrity confirms the checkpoint ran.

**Wall-clock estimate:** 1.5 days.

---

## Constraint Propagation (from ADR-0052 / spec, enforced at every checkpoint)

| Constraint | Enforced at | Checkpoint assertion |
|-----------|-------------|----------------------|
| Frozen ADR-0032 six + `track.py` numstat == 0 vs `3ab1c3ab` | Wave 1 + Wave 2 entry & exit | the `git diff --numstat 3ab1c3ab … -- <six + track.py>` prints-nothing probe |
| `RENDERABLE_DOMAINS` / `_PLAN_VALIDATORS` stay four (RT-009) | Wave 2 exit | T3 AC-3 (`len==4` + set unchanged) |
| `server.py` / `care_chat.py` NOT modified (Stale-Premise-Reconciled) | Wave 2 exit | `git diff --numstat main -- server.py care_chat.py` prints nothing |
| Unconditional always-on-ten floor (partial-signal ⊇ ten) | Wave 1 exit | T2 AC-2 partial-signal probe + AC-4 conditional-idiom RED |
| §11-§13 stay progressive (no empty-state fabrication) | Wave 1 + Wave 2 exit | T2 AC-5 + T3 AC-5 |
| `$0` build (synthetic/fixture, PUBLIC repo) | every checkpoint | fixture/spy client, no live SDK call, no spend |

## Operator-Present Exit Gate (out of build scope)

After Wave 2 merges, the load-bearing NON-mock verification (spec Test Strategy / ADR-0052 OQ-4): the operator runs `/generate-plan` on their REAL data; the `plan-model::` record must carry authored programs for the active always-on domains (≥ the fixture-verified ten on an all-signal operator). This is operator-gated (real spend across up to ten no-train author calls) — recorded here, teed up in the HANDOFF, NOT a build task.
