---
task-id: ADR-0026-T4
source-spec: docs/spec/live-wiring-spec.md
source-build-plan: docs/build-plan/build-plan-live-wiring.md
wave: 3
assigned-agent: SE
reviewers: [QA, Security]
created: 2026-06-24
status: draft
depends-on: [ADR-0026-T1, ADR-0026-T2]
---

# Recipe: Core-Capability-Audit Repoint + A′-Inversion `--self-test`

Move the `core-capability-audit.sh` `CALLER` pin off `generate_plan.py` onto the A′ spine, and add a
NON-TAUTOLOGICAL A′-inversion `--self-test`. Three changes: (1) `scripts/core-capability-audit.sh`
(Modify) — repoint the `CALLER` ([core-capability-audit.sh:47], currently
`$REPO_ROOT/scripts/plan/generate_plan.py`) onto the A′ spine (`plan_orchestrator.py` /
`plan_driver.py`); the structural checks assert the shared driver exists, drives
`pipeline.run_generation`, and the `safety_passed`/`accept`/`revise_domains` disposition gate is
present; repoint the behavioral check ([:68]) to invoke the A′ `--self-test`. (2)
`scripts/plan/_a_prime_self_test.py` (Create) — the A′-inversion self-test driver, modeled on
`generate_plan._self_test` ([generate_plan.py:454], which returns 0/1 + prints): seed a synthetic
PII-free fixture, drive the shared driver via a fixture `dispatch` through de-id→loop→promote→render,
and assert promotion-on-accept + 0-plans-on-safety-not-True. (3) `tests/plan/test_a_prime_self_test.py`
(Create) — unit tests for the self-test module.

The PF-S63-02 / INV-CORE-CAPABILITY discipline: the audit's behavioral leg must be NON-TAUTOLOGICAL —
it asserts the INVERTED loop behaviors (a plan promotes on accept; an injected safety-not-True
disposition surfaces 0 plans), not just "a plan renders." And the audit→self-test EXIT-CODE chain must
go RED end-to-end: the audit consumes ONLY the self-test's exit code (stdout/stderr suppressed), so a
self-test that PRINTED "FAIL" but `exit 0`'d would read GREEN — the self-test signals failure via a
NON-ZERO EXIT, never a printed message.

This task touches NO inner-engine module (numstat = 0). It repoints a shell script + adds a self-test
driver modeled on the existing one. `scripts/core-capability-audit.sh` +
`scripts/plan/_a_prime_self_test.py` + `tests/plan/test_a_prime_self_test.py` are the only files.
Deterministic, runs under `.venv`, 0 live spend; the live subscription dispatch is out of scope (S94).

## Entry State

**Prerequisites:**
- [ ] Task ADR-0026-T1 complete (the shared driver `scripts/plan/plan_driver.py` + its drive-protocol
      present + merged — the spine the audit pins + the self-test drives).
- [ ] Task ADR-0026-T2 complete (the composed `scripts/plan/gate_dispatch.py` present + merged — the
      gate whose disposition the self-test's accept / safety-not-True fixtures exercise).
- [ ] Wave 2 checkpoint passed Go (the composer emits the exact 3-key disposition, fails closed,
      runs both gates).
- [ ] Working tree clean: `git status` shows no changes (the daemon vault-frontmatter churn under
      `vault/**` is daemon noise — leave it uncommitted; see CLAUDE.md § Vault hygiene).
- [ ] Full test suite passes: `.venv/bin/python -m pytest -q`; the governance shell suite passes:
      `bash scripts/tests/run-all-tests.sh` (exit 0, the core-capability audit's own negative test
      green at the pre-repoint baseline).
- [ ] Infrastructure prerequisite verified — the audit + its scaffold + its negative test present:
      `test -f scripts/tests/run-all-tests.sh && test -f scripts/lib/audit-helpers.sh && test -f
      scripts/core-capability-audit.sh && grep -q "audit_init\|audit_exit" scripts/lib/audit-helpers.sh
      && test -f scripts/tests/test_core_capability_audit.sh && echo OK`.
- [ ] On feature branch: `feature/core-cap-audit-aprime` cut off `feature/engine-live-wiring-build`.

This entry state doubles as the rollback target — the entry-state commit is the Wave-2 → Wave-3
checkpoint HEAD (ADR-0026-T1/T2 merged).

## Context Load List

**Files to read:**
- `scripts/core-capability-audit.sh` — the audit being repointed: the `CALLER` pin ([:47],
  `generate_plan.py`), the structural checks ([:50-58], `assemble(` + `record_plan(`), the behavioral
  self-test invocation ([:60-73], `generate_plan --self-test`), the F-008 exit contract
  (`audit_init`/`violation`/`skipped`/`audit_summary`/`audit_exit`), and the test-hook env vars
  (`CORE_CAP_CALLER` / `CORE_CAP_PY` / `CORE_CAP_SKIP_BEHAVIORAL`).
- `scripts/plan/generate_plan.py` — `_self_test()` ([:454-537]): the analogue the A′ self-test is
  MODELED on (seeds a synthetic store, authors through a fixture backend, runs the wired path, renders
  the dashboard, asserts the recorded plan rendered, returns 0/1 + prints). Read its shape — the A′
  self-test mirrors the 0/1-exit + fixture-driven structure for a DIFFERENT path (the A′ inversion).
- `scripts/plan/plan_driver.py` — the shared driver (ADR-0026-T1) the self-test DRIVES via a fixture
  `dispatch`: its drive-protocol + the 3-key disposition it reads (`{accept, safety_passed,
  revise_domains}`) — so the self-test injects a fixture accept disposition + a fixture
  safety-not-True disposition.
- `scripts/plan/gate_dispatch.py` — the composer (ADR-0026-T2) — read the 3-key disposition shape the
  self-test's fixtures emit (the self-test may use a fixture disposition directly, or the real
  composer over fixture judge/review; pin which in GREEN).
- `scripts/lib/audit-helpers.sh` — the `audit_init`/`violation`/`skipped`/`info`/`audit_summary`/
  `audit_exit` scaffold + the F-008 fail-closed exit contract the Modify PRESERVES (read so the
  repoint does not break the exit semantics).
- `scripts/tests/test_core_capability_audit.sh` — the audit's OWN negative test (a deliberately-
  unwired path → RED) — read so the repoint keeps it RED-capable (the structural-only isolation via
  `CORE_CAP_SKIP_BEHAVIORAL` + a broken `CORE_CAP_CALLER`).

**Do NOT load:** the ADRs (`docs/adr/ADR-0026*.md`) — the spec distilled them; the inner-engine
modules (`orchestrate`/`pipeline`/`assemble`/`adjudicate`/`adjust`/`track`/`router`) — byte-frozen,
untouched; the skill (`SKILL.md`) — ADR-0026-T3, the parallel Wave-3 task with a disjoint manifest;
`scripts/model/client.py` — ADR-0027-T1's scope (the self-test uses a fixture `dispatch`, not the live
backend); any `vault/**` file — daemon-churned.

## Risk Pre-Check

This task carries the spec's ADR-0026-T4 Risk Mitigations field (the PF-S63-02 non-tautological guard
+ the F-008 fail-closed contract). Before proceeding to RED, verify a test exists (or the RED phase
adds one) for EACH; a placeholder test (`assert True`) fails this gate.

- **Risk — PF-S63-02 / INV-CORE-CAPABILITY: the guard tautologically passes (it asserts "a plan
  renders," not the inversion).** Gate: the `--self-test` asserts the INVERTED behaviors — ≥1 plan
  promoted on a fixture accept disposition (AC-3) AND 0 plans surfaced past an injected safety-not-True
  disposition (AC-4); the self-test exits non-zero if either inversion breaks.
- **Risk — the audit→self-test exit-code chain reads a tautological pass (QA-3).** Gate: drive
  `_a_prime_self_test.py` with a KNOWN-BROKEN spine (a promote-everything stub that surfaces a plan
  PAST a non-True safety disposition) and assert `bash scripts/core-capability-audit.sh` exits
  NON-zero — the self-test signals failure via a NON-ZERO EXIT (not a printed message), and the audit
  propagates that non-zero exit (does not swallow it to 0).
- **Risk — the F-008 fail-closed contract is broken by the repoint (a check that could not RUN reads
  as clean).** Gate: the repoint preserves the `audit_init`/`audit_exit` scaffold + the
  `skipped()`/FATAL-on-skip posture — the audit's own negative test still goes RED on an unwired path
  (AC-8).

The gate conditions reference live tests / audit exit codes, not subjective assessments.

## TDD Steps

Four TDD cycles. Cycle 1 the self-test module (promotion-on-accept + 0-plans-on-safety-not-True, the
0/1-exit driver). Cycle 2 the audit repoint (CALLER off `generate_plan.py` + structural A′-spine
asserts + behavioral repoint). Cycle 3 the audit→self-test exit-code chain (RED on a known-broken
spine, QA-3). Cycle 4 the governance-suite green incl. the audit's own negative test still RED. The
self-test uses a fixture `dispatch`, 0 live spend.

**Self-test construction note (read before RED):** model the A′ self-test on `generate_plan._self_test`
([:454]) — a `_self_test()` returning 0 on a wired A′ spine, non-zero on any inversion break, with a
`main()`/`--self-test` CLI entry the audit invokes (`python -m scripts.plan._a_prime_self_test
--self-test`). The self-test drives `plan_driver` via a FIXTURE `dispatch` + a fixture disposition
through de-id (a PII-free synthetic intake) → loop → promote → render. The FAILURE signal is the
NON-ZERO EXIT (QA-3) — print is advisory, the exit code is load-bearing.

### Cycle 1: Steps 1-4 — the A′-inversion self-test (promotion-on-accept + 0-plans-on-safety-not-True)

#### Step 1: RED — Write Failing Tests
Call `/write-tests` for `scripts/plan/_a_prime_self_test.py` (new suite
`tests/plan/test_a_prime_self_test.py`) targeting:
- AC-3 (non-tautological promotion-on-accept): the self-test drives the shared driver with a fixture
  `dispatch` + a fixture ACCEPT disposition and asserts ≥1 plan is promoted/rendered — the self-test
  returns 0 on the wired path; a variant surfacing 0 plans on accept makes it return non-zero. Assert
  `_self_test()` returns 0 on the accept path.
- AC-4 (non-tautological 0-plans-on-safety-not-True): the self-test drives the shared driver with an
  injected `safety_passed` not-True disposition and asserts 0 plans surface — the self-test returns
  non-zero if ≥1 plan surfaces past a non-True safety disposition. (This is what makes the pass
  non-tautological — it exercises the INVERTED loop, not just "a plan renders.") Assert the safety-
  not-True branch surfaces 0 plans and the self-test's inversion assertion holds.
- AC-7 (suite gate): `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py` passes (the
  accept path promotes ≥1 plan; the safety-not-True path surfaces 0 plans; 0 live calls).

Run: `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py -q`
Expected: FAIL (`scripts/plan/_a_prime_self_test.py` does not yet exist).

#### Step 2: GREEN — Implement
Changes to make:
- `scripts/plan/_a_prime_self_test.py` (Create): write the A′-inversion self-test, modeled on
  `generate_plan._self_test`. A `_self_test()` that (a) seeds a synthetic PII-free fixture (a synthetic
  operator-state store + a synthetic raw-PII-free intake), (b) drives `plan_driver` via a fixture
  `dispatch` + a fixture accept disposition through de-id→loop→promote→render, asserts ≥1 plan
  promoted/rendered, and (c) drives it again with an injected `safety_passed` not-True disposition,
  asserts 0 plans surface. Returns 0 when BOTH inversion behaviors hold, non-zero (and prints the
  failing behavior) when either breaks — the NON-ZERO EXIT is the failure signal (QA-3). Add a
  `main()`/`--self-test` CLI entry (`python -m scripts.plan._a_prime_self_test --self-test`) the audit
  invokes. Deterministic, 0 live spend. (satisfies AC-3, AC-4)

Run: `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py -q`
Expected: PASS

#### Step 3: REFACTOR
Review for duplication with `generate_plan._self_test` — the A′ self-test seeds a synthetic store the
SAME way; extract a shared fixture-seeding helper ONLY if both genuinely share it (do not refactor
`generate_plan._self_test` itself — it stays the `generate_plan` gate's analogue; the A′ self-test
asserts a DIFFERENT path). Naming consistency with the existing self-test idiom. No behavior change.
Run targets: `tests/plan/test_a_prime_self_test.py`. Expected: PASS, no behavior change.

#### Step 4: REGRESSION
Run: `.venv/bin/python -m pytest -q`
Expected: PASS (no tests outside task scope broken).

### Cycle 2: Steps 5-8 — the audit repoint (CALLER off generate_plan.py + structural A′-spine + behavioral)

#### Step 5: RED — Write Failing Tests
Call `/write-tests` for `scripts/core-capability-audit.sh` (extend
`tests/plan/test_a_prime_self_test.py` with shell-driven cases, OR a `scripts/tests/` shell case
mirroring `test_core_capability_audit.sh`) targeting:
- AC-1 (CALLER repoint): a grep over `scripts/core-capability-audit.sh` finds 0 references to
  `generate_plan.py` as the `CALLER` and ≥1 to the A′ spine module (`plan_orchestrator.py` /
  `plan_driver.py`).
- AC-2 (structural A′-spine asserts): the structural checks assert the shared driver exists, references
  `pipeline.run_generation`, and the `safety_passed`/`accept`/`revise_domains` disposition gate is
  present — each a grep that goes RED if the path is unwired.
- AC-5 (audit exits 0 on the wired spine): `bash scripts/core-capability-audit.sh` exits 0 on the
  wired A′ spine (the repointed structural + behavioral checks pass under `.venv`).
- AC-6 (live dispatch out of scope, S94): the audit does NOT claim to verify the live subscription
  dispatch — the self-test uses a fixture `dispatch`; an info line / comment states the boundary.

Run: `bash scripts/core-capability-audit.sh; echo "exit=$?"` (and the new shell case)
Expected: FAIL (the audit still pins `generate_plan.py` + invokes `generate_plan --self-test`; the A′
structural asserts + the A′ behavioral invocation do not yet exist).

#### Step 6: GREEN — Implement
Changes to make:
- `scripts/core-capability-audit.sh` (Modify): move the `CALLER` default ([:47]) off
  `$REPO_ROOT/scripts/plan/generate_plan.py` onto the A′ spine (`$REPO_ROOT/scripts/plan/plan_driver.py`
  and/or `plan_orchestrator.py`). Repoint the structural checks ([:50-58]): assert the shared driver
  exists, references `pipeline.run_generation`, and the disposition gate (`safety_passed` / `accept` /
  `revise_domains`) is present — each a grep that `violation`s if the path is unwired. Repoint the
  behavioral check ([:60-73]): invoke the A′ `--self-test`
  (`python -m scripts.plan._a_prime_self_test --self-test`) instead of `generate_plan --self-test`.
  Add an info line stating the live subscription dispatch is the S94 attestation, out of the audit's
  reach (the self-test uses a fixture `dispatch`). PRESERVE the `audit_init`/`violation`/`skipped`/
  `audit_summary`/`audit_exit` scaffold + the F-008 exit contract verbatim (do not edit the
  scaffold). (satisfies AC-1, AC-2, AC-5, AC-6)

Run: `bash scripts/core-capability-audit.sh; echo "exit=$?"`
Expected: exit 0 (the wired A′ spine passes)

#### Step 7: REFACTOR
Review the repointed greps for consistency with the existing `violation PF-S63-02 "..."` idiom + the
test-hook env-var pattern (`CORE_CAP_CALLER` still overrides the caller; add no new hook unless the A′
behavioral check needs one). No behavior change. Run targets: `bash scripts/core-capability-audit.sh`.
Expected: exit 0.

#### Step 8: REGRESSION
Run: `.venv/bin/python -m pytest -q && bash scripts/tests/run-all-tests.sh; echo "exit=$?"`
Expected: pytest PASS; the governance shell suite exit 0 (no pre-existing audit test regresses yet —
Cycle 4 pins the negative test).

### Cycle 3: Steps 9-10 — the audit→self-test exit-code chain (QA-3: RED on a known-broken spine)

#### Step 9: RED — Write Failing Tests
Call `/write-tests` for the audit→self-test exit-code chain (`tests/plan/test_a_prime_self_test.py` +
a shell case) targeting:
- QA-3 (audit→self-test exit-code chain goes RED end-to-end): drive `_a_prime_self_test.py` with a
  KNOWN-BROKEN spine (a promote-everything stub that surfaces a plan PAST a non-True safety
  disposition, inverting the fail-closed gate — injected via a test hook / monkeypatch on the
  self-test's driver) and assert (a) the self-test produces a NON-ZERO exit code, AND (b)
  `bash scripts/core-capability-audit.sh` (invoked with the broken-spine self-test) propagates that
  non-zero exit — the audit does not swallow it to 0. This proves the audit's BEHAVIORAL leg goes RED
  THROUGH the exit-code path: the audit consumes ONLY the self-test's exit code (stdout/stderr
  suppressed at [:68]), so a self-test that printed "FAIL" but `exit 0`'d would read GREEN (the exact
  PF-S63-02 tautology this criterion prevents).

Run: the broken-spine shell case + `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py -q`
Expected: FAIL if the exit-code chain is not yet RED-capable (e.g. the self-test prints "FAIL" but
exits 0, or the audit swallows the non-zero exit) — the chain assertion is the new code.

#### Step 10: GREEN — Implement
Changes to make:
- `scripts/plan/_a_prime_self_test.py`: confirm the self-test signals failure via a NON-ZERO EXIT (not
  a printed message) — the inversion-break path returns non-zero. Add a test hook (an env var /
  injectable driver, mirroring `generate_plan`'s `CORE_CAP_*` hooks) so the known-broken spine can be
  injected for the QA-3 chain test WITHOUT being a production path (a loud WARNING if set in
  production, like the audit's existing test-hook warnings).
- `scripts/core-capability-audit.sh`: confirm the behavioral check propagates the self-test's non-zero
  exit (the `if ( ... "$PY" -m scripts.plan._a_prime_self_test --self-test >/dev/null 2>&1 ); then ...
  else violation ...` shape — the `violation` fires on a non-zero self-test exit, and `audit_exit`
  carries it to a non-zero audit exit). Do not swallow the exit to 0.

Run: the broken-spine shell case + `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py -q`
Expected: the broken-spine self-test exits non-zero AND the audit propagates it (the chain test passes
by asserting the non-zero propagation); the wired-spine path stays exit 0.

#### (REFACTOR folded — the exit-code propagation is the audit's existing `violation` path. REGRESSION:)
Run: `.venv/bin/python -m pytest -q`
Expected: PASS

### Cycle 4: Steps 11-12 — governance suite green incl. the audit's own negative test still RED

#### Step 11: RED — Write Failing Tests
Call `/write-tests` for the governance shell suite (confirm `scripts/tests/test_core_capability_audit.sh`
still goes RED on an unwired path after the repoint) targeting:
- AC-8 (governance suite green + the negative test still RED): `bash scripts/tests/run-all-tests.sh`
  exits 0 — no pre-existing audit test regresses after the repoint — AND the core-capability audit's
  own negative test (a deliberately-unwired path → RED, via `CORE_CAP_SKIP_BEHAVIORAL=1` +
  a broken `CORE_CAP_CALLER`, or the A′-spine equivalent) STILL goes RED. The negative test must
  exercise the A′ structural checks (the repointed greps), not the stale `generate_plan.py` checks.

Run: `bash scripts/tests/run-all-tests.sh; echo "exit=$?"`
Expected: FAIL if the repoint broke the negative test's RED-capability (e.g. the negative test still
unwires `generate_plan.py`, which the repointed audit no longer reads, so it goes GREEN vacuously) —
the negative test must be updated to unwire the A′ spine.

#### Step 12: GREEN — Implement
Changes to make:
- `scripts/tests/test_core_capability_audit.sh` (if the repoint stales its RED path): update the
  negative test to unwire the A′ SPINE (a broken `CORE_CAP_CALLER` pointing at a missing/unwired
  driver, or a structural-only isolation that the repointed greps go RED against) — so the negative
  test still proves the audit CAN go RED on an unwired A′ path. (This is a test-file update under the
  governance suite, in-scope as the audit's own negative-test maintenance; if the existing negative
  test stays RED-capable against the A′ spine unchanged, no edit — pin it.)

Run: `bash scripts/tests/run-all-tests.sh; echo "exit=$?"`
Expected: exit 0 (the suite green; the negative test still RED-capable against the A′ spine)

#### (REFACTOR folded. REGRESSION:)
Run: `.venv/bin/python -m pytest -q && bash scripts/tests/run-all-tests.sh`
Expected: pytest PASS; the governance shell suite exit 0.

**TDD step count: 12 (4 cycles, REFACTOR/REGRESSION folded on cycles 3-4).** Within the ≤10-cycles
guidance (4 cycles); the 8 ACs span the self-test inversion + the audit repoint + the exit-code chain
+ the negative-test-still-RED. One created self-test + one created test file + one modified audit (+ a
possible negative-test update, the audit's own).

## Interface Contracts

This task does NOT create a shared Python interface consumed by another build task — it CONSUMES the
ADR-0026-T1 `plan_driver` drive-protocol (the self-test drives it) and the ADR-0026-T2 composed
`gate_dispatch` (the self-test's disposition exercises it). The `--self-test` CLI entry
(`python -m scripts.plan._a_prime_self_test --self-test`) is an interface the AUDIT (a shell script in
the same task) consumes — both sides of that contract are in THIS task's manifest, so it is not a
cross-task interface. `_a_prime_self_test._self_test()` returns 0/non-zero — the exit-code contract
the audit's behavioral check reads (defined + consumed within this task). No downstream build task
consumes an interface this task introduces.

## Verification Checklist

- [ ] AC-1 (CALLER off `generate_plan.py` onto the A′ spine) — verified by `test_audit_caller_repointed`
      (grep `core-capability-audit.sh`: 0 `generate_plan.py` CALLER refs, ≥1 A′-spine module ref).
- [ ] AC-2 (structural A′-spine asserts) — verified by `test_audit_structural_asserts_a_prime_spine`
      (greps for the shared driver + `pipeline.run_generation` + the disposition gate, each RED on an
      unwired path).
- [ ] AC-3 (non-tautological promotion-on-accept) — verified by `test_self_test_promotes_on_accept`
      (the `--self-test` returns 0 on a fixture accept disposition; ≥1 plan promoted/rendered).
- [ ] AC-4 (non-tautological 0-plans-on-safety-not-True) — verified by
      `test_self_test_zero_plans_on_safety_not_true` (the `--self-test` returns non-zero if ≥1 plan
      surfaces past a non-True safety disposition; 0 plans surface).
- [ ] AC-5 (audit exits 0 on the wired spine) — verified by `bash scripts/core-capability-audit.sh`
      → exit 0.
- [ ] AC-6 (live dispatch out of scope, S94) — verified by `test_self_test_uses_fixture_dispatch`
      (the self-test constructs a fixture `dispatch`) + an audit info line stating the boundary.
- [ ] AC-7 (suite gate) — verified by `.venv/bin/python -m pytest tests/plan/test_a_prime_self_test.py`
      (the accept path promotes ≥1 plan; the safety-not-True path surfaces 0 plans; 0 live calls).
- [ ] AC-8 (governance suite green + negative test still RED) — verified by
      `bash scripts/tests/run-all-tests.sh` exit 0 + `test_core_capability_audit.sh`'s unwired-path
      case still RED against the A′ spine.
- [ ] Wave-3 audit gates carried: repoint [AC-1/2], non-tautological promotion-on-accept [AC-3],
      non-tautological 0-plans-on-safety-not-True [AC-4], the audit→self-test exit-code chain (QA-3 —
      RED on a known-broken spine, via NON-ZERO EXIT not a printed message) — verified by
      `test_audit_propagates_broken_spine_nonzero_exit` (the broken-spine self-test exits non-zero AND
      `bash scripts/core-capability-audit.sh` propagates the non-zero exit), and the
      run-all-tests-green-incl-the-audit's-own-negative-test-still-RED [AC-8].
- [ ] EXTEND-NOT-REBUILD gate green: `git diff --numstat <wave-base>..HEAD` on the 8 inner-engine
      files → 0 changed lines (the audit repoints; the self-test drives the existing spine).
- [ ] No regression in full test suite (`.venv/bin/python -m pytest -q`) + the governance shell suite
      (`bash scripts/tests/run-all-tests.sh` exit 0).
- [ ] Files modified match file manifest (`scripts/core-capability-audit.sh` +
      `scripts/plan/_a_prime_self_test.py` + `tests/plan/test_a_prime_self_test.py`, + a possible
      `scripts/tests/test_core_capability_audit.sh` negative-test update — the audit's own) — no scope
      creep.
- [ ] Interface contracts documented (the `--self-test` exit-code contract defined + consumed within
      this task; no cross-task interface).

## Commit

```
fix(audit): repoint core-capability onto A-prime spine
```
Stage only:
- `scripts/core-capability-audit.sh`
- `scripts/plan/_a_prime_self_test.py`
- `tests/plan/test_a_prime_self_test.py`
- `scripts/tests/test_core_capability_audit.sh` (ONLY if the repoint required updating the audit's own
  negative test to stay RED-capable against the A′ spine — document in Deviations if so)

Stage by explicit path (`git add <path>` as its own command, then `git commit` separately — the
PreToolUse hook denies single-call stage+commit, `git commit -a/--all`, and pathspec
`git commit <path>`). Do NOT `git add vault/` or the daemon frontmatter churn (CLAUDE.md § Vault
hygiene). Do NOT stage `.beads/issues.jsonl` / `harvest.jsonl` / `memory/process-failures.md`.

## Rollback

If verification fails after 3 fix cycles:
1. `git stash -m "failed-ADR-0026-T4-attempt-{N}"` — preserve work for diagnosis.
2. `git checkout {commit-before-task}` — revert to the entry-state commit (the Wave-2 → Wave-3
   checkpoint HEAD).
3. Update the bead tracker: flag ADR-0026-T4 as BLOCKED with the failure log.
4. Escalate: "Task ADR-0026-T4 failed verification after 3 attempts. Stash ref: {ref}. Failure log:
   {summary}."
5. After abandonment or re-planning, drop all `failed-ADR-0026-T4` entries from `git stash list`.

Do NOT: silently skip failing acceptance criteria, weaken tests to make them pass (especially the
non-tautological inversion asserts + the audit→self-test exit-code chain — a guard that tautologically
passes, or a self-test that signals failure via a printed message it `exit 0`s past, is the exact
PF-S63-02 failure this task exists to prevent), or proceed to the wave checkpoint with a broken state.

## Deviations

| # | Spec Says | Recipe Says | Reason | Impact |
|---|-----------|-------------|--------|--------|
| 1 | The File Manifest names `scripts/core-capability-audit.sh` (Modify) + `scripts/plan/_a_prime_self_test.py` (Create) + `tests/plan/test_a_prime_self_test.py` (Create). | The recipe MAY also touch `scripts/tests/test_core_capability_audit.sh` (the audit's OWN negative test) IF the CALLER repoint stales its RED path (it must unwire the A′ spine, not the retired `generate_plan.py` pin). | AC-8 requires the negative test to still go RED on an unwired A′ path; if it currently unwires `generate_plan.py` (which the repointed audit no longer reads), it would pass vacuously — a stale negative test is a defect AC-8 forbids. | Non-blocking. The negative-test update is the audit's own maintenance, in-scope as part of the repoint (the spec's AC-8 mandates it stay RED-capable). If the existing negative test stays RED-capable unchanged, no edit. Documented here per the recipe's scope-discipline. |
