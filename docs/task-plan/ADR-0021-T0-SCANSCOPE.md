---
task-id: ADR-0021-T0-SCANSCOPE
source-spec: docs/spec/adr-0020-0025-plan-gen-engine-spec.md
source-build-plan: docs/build-plan/build-plan-plan-gen-engine.md
wave: 1
assigned-agent: SE
reviewers: [QA, Security]
created: 2026-06-24
status: approved
---

# Recipe: [Spike] Fix the PII Scan-Scope Hole on the Maintained-Output Path

The scoped operator-NAME scan (`pii_scan.scan_scoped`, identity tokens over the
`data_bearing` subset) does not reach `vault/artifacts/generated/`, so a committed
maintained-HTML artifact carrying a re-inserted real NAME is name-scanned by neither
PII hook. This recipe extends the single-sourced `DATA_BEARING_PREFIXES` to cover that
directory and proves the coverage with a fixture test. This is the crown-jewel leak
boundary the ADR-0021 re-insertion (`reinsert_out.py`) and ADR-0025 maintained output
(`maintained.py`) tasks rest on; it is a hard dependency of both (spec Dependency Map).

## Entry State

**Prerequisites:**
- [ ] Wave 1 entry: this is an entry-point task (Dependencies: None) — no predecessor build-plan task to confirm complete.
- [ ] Full Python test suite passes (the EXTEND-NOT-REBUILD baseline): `.venv/bin/python -m pytest -q` (observed 2026-06-24: 1472 passed, 2 skipped, 0 failed).
- [ ] The governance/hook negative-test baseline passes before the change (the regression baseline for AC6): `bash scripts/tests/run-all-tests.sh` → exit 0 (the floor), AND the PII-hook-lib blast-radius set is green pre-change — `bash .claude/hooks/tests/test_block_ungated_vault_write.sh`, `bash .claude/hooks/tests/test_commit_matcher.sh`, `bash .claude/hooks/tests/test_resolve_target_repo.sh` → exit 0 each (these source the PII-hook libs directly and are not auto-discovered by `run-all-tests.sh`).
- [ ] The scan-scope hole is confirmed real: `rg -n "artifacts/generated" .claude/hooks/lib/pii-scan-scope.sh` returns NO match (`vault/artifacts/generated/` is absent from `DATA_BEARING_PREFIXES`).
- [ ] Both hooks build their `data_bearing` argv from `DATA_BEARING_PREFIXES`: `rg -n "DATA_BEARING_PREFIXES" .claude/hooks/block-pii-commit.sh .claude/hooks/pre-push-pii-scan.sh` matches the iteration site in each (`block-pii-commit.sh:279`, `pre-push-pii-scan.sh:126`).
- [ ] `vault/artifacts/generated/` is gitignored: `.gitignore` line 6 carries the entry (so the in-band leak vector is `git add -f` / `git commit --no-verify`, and this scan-scope change is the backstop).
- [ ] The synthetic identity token source exists for the fixture's deny case: `vault/meta/operator-identity.txt` present (gitignored; one regex per line).
- [ ] Working tree clean: `git status` shows no uncommitted changes in the file manifest paths.
- [ ] On a feature branch off `main`: `feature/pii-scanscope-artifacts` (never commit to `main`).

**Rollback target:** the commit immediately before this task's commit (entry-state HEAD).

## Context Load List

**Files to read:**
- `.claude/hooks/lib/pii-scan-scope.sh` — the single source of `DATA_BEARING_PREFIXES` / `PER_SE_DENY_PREFIXES`; the one line this task edits.
- `.claude/hooks/block-pii-commit.sh` — confirm how the commit hook partitions the staged set into `DATA_BEARING` from `DATA_BEARING_PREFIXES` (loop at L277-282) and passes it to `scan_scoped` on argv (L308-324); the recipe edits no logic here, only reads it to know the scope change propagates.
- `.claude/hooks/pre-push-pii-scan.sh` — confirm the push backstop builds `DATA_BEARING` from the same shared list (L124-129) and passes it to `scan_scoped` (L132-149); same read-only confirmation.
- `scripts/guard/pii_scan.py` — confirm `scan_scoped(changed, data_bearing, …)` runs the identity (operator-NAME) tokens ONLY over the `data_bearing` subset (L404-405); this is WHY adding the prefix to `DATA_BEARING_PREFIXES` (not just a fixture) is required.
- `.claude/hooks/tests/test_block_ungated_vault_write.sh` — the structural pattern for an isolated hook fixture test (temp git repo, `*_PROJECT_ROOT`/`*_PII_SCAN_ROOT` env overrides, allow-vs-deny non-tautological case pairing); model the new test on this shape.

**Do NOT load:** the ADRs (`docs/adr/ADR-002{0,1,5}*`), the DAG / dispositions / context docs under `docs/*/.pipeline/`, or any other `scripts/plan/` or `scripts/generate/` module — the spec already distilled the upstream research, and none of the de-id-IN / orchestrator / judge / maintained modules are touched by this task. Do NOT load `vault/meta/operator-identity.txt` contents into the recipe or test source (it is gitignored operator PII; the test reads it via path at runtime or seeds a SYNTHETIC token config — never inlines the real token).

## Risk Pre-Check

This task carries risk mitigations in the spec — Risk Pre-Check is REQUIRED.

- **Risk (ADR-0021 Consequence-Negative-2 / ADR-0025 Consequence-Negative-3): the name scan-scope hole** — a committed name-bearing maintained-HTML artifact under `vault/artifacts/generated/` is scanned only for contact tokens, never operator-NAME tokens, so a re-inserted real name reaches a committed/pushed file undetected.
  - **Gate condition:** before GREEN, the RED phase must add a test that stages a `vault/artifacts/generated/*.html` file containing the operator-identity token and asserts `block-pii-commit.sh` DENIES it (and `pre-push-pii-scan.sh` blocks it on a push range). On the unchanged code this test must FAIL (the artifact is currently ALLOWED). A test that passes on the current code does not exercise the hole and fails this gate.
  - **Placeholder rejection:** an `assert true` / `exit 0`-only case, or a case that asserts deny without a name token in the file, fails this gate.
- **Risk (ADR-0005 Falsification): ≥1 operator-PII value in a tracked file is release-blocking** — this task IS the boundary the ADR-0021/0025 egress rests on.
  - **Gate condition:** the fixture must include the negative-direction case (AC4): a de-identified (initials-only, no identity token, no contact token) `vault/artifacts/generated/*.html` is ALLOWED by both hooks. The deny case and the allow case differ ONLY by the presence of the name token — the pairing proves the change denies the leak without over-blocking the clean artifact. A fixture with no allow case fails this gate (it cannot show the change is not a blanket per-se-deny).

## Core Change (Decision)

**Decision: add `vault/artifacts/generated/` to `DATA_BEARING_PREFIXES`, NOT to `PER_SE_DENY_PREFIXES`.**

Grounding for the choice (the spec offers either; this recipe decides which makes a
re-inserted real NAME in a committed maintained-HTML artifact DENIED while a clean one
stays ALLOWED):

- `scan_scoped` (L404-405) runs the operator-NAME (`identity_config`) tokens ONLY over the `data_bearing` subset. Adding `vault/artifacts/generated/` to `DATA_BEARING_PREFIXES` puts every artifact under that path into the subset, so a re-inserted real name is now name-scanned → DENIED (AC2/AC3). This is the precise hole-closure: name coverage on the artifacts path.
- `PER_SE_DENY_PREFIXES` denies a file by LOCATION regardless of token content. But `vault/artifacts/generated/` is exactly where the LEGITIMATE de-identified (initials-only) rendered plan lives — that is the directory's purpose (it is the `render.emit` `DEFAULT_OUT_DIR`). A blanket per-se-deny would block the clean initials-only artifact too, violating AC4 ("does not over-block clean artifacts"). So per-se-deny is the WRONG instrument here.
- Therefore: `DATA_BEARING_PREFIXES` is the correct list. A clean artifact carries no identity token → ALLOWED; a name-bearing artifact carries the token → DENIED. The change is the ONE library edit (extend the array literal) + the new fixture test.

The single-sourced list means the edit propagates to BOTH hooks at once (each iterates
`DATA_BEARING_PREFIXES` to build its `data_bearing` argv) — no hook-side logic changes.

## TDD Steps

This is a single TDD cycle (one library edit + one fixture test; well under the
multi-cycle threshold).

### Step 1: RED — Write the Failing Fixture Test

Call `/write-tests` to author `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh`, an isolated bash fixture test (modeled on `test_block_ungated_vault_write.sh`: a temp git repo via `mktemp -d`, `git init` on a feature branch, the hook pointed at the temp repo via its `*_PROJECT_ROOT` / `*_SCAN_ROOT` env overrides, and a SYNTHETIC operator-identity token config so no real PII enters the test tree), targeting:
- AC-2: a staged `vault/artifacts/generated/plan.html` whose CONTENTS contain the (synthetic) operator-identity token is DENIED by `block-pii-commit.sh` (the hook prints a deny decision / exits with the deny path).
- AC-3: the same name-bearing artifact, presented as a changed file in a push range, is DENIED by `pre-push-pii-scan.sh` (exit 1).
- AC-4: a de-identified `vault/artifacts/generated/plan.html` (initials-only, no identity token, no contact token) is ALLOWED by BOTH hooks (no deny / exit 0). This is the non-tautological pair to AC-2/AC-3 — the two cases differ only by the name token.
- Risk (ADR-0021 N2 / ADR-0025 N3): the AC-2/AC-3 deny cases ARE the risk-mitigation tests; the AC-4 allow case proves the change is not a blanket per-se-deny.

**[AMENDED 2026-06-24 — QA SHOULD-FIX: force the gitignored artifact into the scanned set.]** `vault/artifacts/generated/` is gitignored (`.gitignore:6`), so a plain `git add vault/artifacts/generated/plan.html` NO-OPS — the path never enters `git diff --cached`, the staged set stays empty, and `block-pii-commit.sh` exits 0 for the WRONG reason (empty staged set, not a clean scan). The fixture MUST force the artifact into the scanned input:
- **AC-2 (commit gate):** stage with `git add -f vault/artifacts/generated/plan.html` so the gitignored file enters `git diff --cached`; then assert `block-pii-commit.sh` DENIES on the identity-token scan over a NON-EMPTY `data_bearing` match. The assertion must confirm the deny is triggered BY the name-token match (e.g. the deny message names the artifact / the identity rule), not by an empty staged set — a separate "empty staged set → allow" control case proves the deny is content-driven.
- **AC-3 (push backstop):** `git add -f` the artifact AND create a commit (`git commit` on the temp branch) so the file actually lands in the push RANGE the hook reads (`pre-push-pii-scan.sh` scans the commit range, not the index); then assert the hook DENIES over the non-empty range. A range with no commit carrying the artifact is the same empty-set false-pass.
- **AC-4 (allow control):** the de-identified artifact is likewise `git add -f`'d (+ committed for the push case) so it too enters a NON-EMPTY scanned set — proving the ALLOW is a clean-scan allow, not an empty-set allow. The deny (AC-2/AC-3) and allow (AC-4) cases differ ONLY by the presence of the identity token in an equally-staged file.

The test must seed its identity token via a synthetic config file inside the temp repo (the same one-regex-per-line shape `pii_scan` loads), pointed at by the hook's scan-root / identity-config seam — NEVER the real `vault/meta/operator-identity.txt` token value.

Run: `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh`
Expected: FAIL — on the unchanged `pii-scan-scope.sh`, `vault/artifacts/generated/` is NOT in `DATA_BEARING_PREFIXES`, so the `-f`-staged name-bearing artifact, though present in `git diff --cached` / the push range, is not in the `data_bearing` subset and is NOT name-scanned → the AC-2/AC-3 deny assertions fail (the artifact is currently allowed despite being in the scanned set). (The AC-4 allow case passes even on the unchanged code — that is expected; the RED signal is the deny cases failing on a NON-EMPTY staged set.)

### Step 2: GREEN — Extend the Scan Scope

Changes to make:
- `.claude/hooks/lib/pii-scan-scope.sh`: extend the `DATA_BEARING_PREFIXES` array literal (the single-sourced list at the bottom of the file) to include the `vault/artifacts/generated/` prefix, alongside the existing scaffold / store / DNA-raw / labs-raw prefixes. Add a one-line comment naming why the artifacts dropzone joins the name-scan scope (it holds the maintained re-inserted-name render; ADR-0021 N2 / ADR-0025 N3). Do NOT touch `PER_SE_DENY_PREFIXES` (per the Decision — the directory legitimately holds the clean initials-only render, so it must not be denied by location). This satisfies AC-1 (the prefix now appears in `DATA_BEARING_PREFIXES`, both hooks build `data_bearing` from it) and, via the single-sourced list, AC-2/AC-3 (the name-bearing artifact enters the `data_bearing` subset and is name-scanned → DENIED) while keeping AC-4 (a clean artifact carries no token → ALLOWED).

Run: `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh`
Expected: PASS — all four cases (AC-2 deny commit, AC-3 deny push, AC-4 allow clean × both hooks) green.

### Step 3: REFACTOR

Review for:
- Consistency of the new array entry with the existing `DATA_BEARING_PREFIXES` literal — same `vault/<dir>/` trailing-slash form, alphabetical/grouped placement matching the existing comment grouping, no duplicate prefix.
- The new comment matches the file's existing single-source-rationale comment style (no restated logic, just the why).
- The fixture test's helper naming and temp-repo teardown (`trap … EXIT`) follow `test_block_ungated_vault_write.sh` conventions; no leaked temp dirs, no reliance on the real identity config.

Run: `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh`
Expected: PASS (no behavior change).

### Step 4: REGRESSION

Run, in order:
1. `bash scripts/tests/run-all-tests.sh` — the governance-negative-test FLOOR (must not regress).
2. The `.claude/hooks/tests/` PII-hook-lib blast-radius regression set, each run directly:
   - `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh` (the new fixture, AC-5)
   - `bash .claude/hooks/tests/test_block_ungated_vault_write.sh`
   - `bash .claude/hooks/tests/test_commit_matcher.sh`
   - `bash .claude/hooks/tests/test_resolve_target_repo.sh`
3. `.venv/bin/python -m pytest -q` — the Python suite (the scope change touches no Python; stays green).

Expected: PASS on all.

**[AMENDED 2026-06-24 — QA SHOULD-FIX: re-ground AC-6.]** `scripts/tests/run-all-tests.sh` is the governance-negative-test FLOOR and must not regress, but it discovers `test_*.sh` ONLY under `scripts/tests/` — and that directory carries ZERO PII-hook tests. So `run-all-tests.sh` passing does NOT exercise the PII-hook libs this change touches. The actual blast-radius regression for the PII-hook lib (`commit-matcher.sh` partitions the staged set the scope feeds; `resolve-target-repo.sh` scopes which repo each hook scans) is the `.claude/hooks/tests/` suite, which sources those libs DIRECTLY and is NOT auto-discovered — so it MUST be run by hand (step 2 above). `test_commit_matcher.sh` + `test_resolve_target_repo.sh` are the PII-hook-lib unit pins (a malformed `DATA_BEARING_PREFIXES` array edit, or any lib breakage the scope change induces, surfaces in these); `test_block_ungated_vault_write.sh` is the sibling-hook structural regression. AC-6 is therefore: `run-all-tests.sh` green (the floor) AND the four `.claude/hooks/tests/` suites green (the PII-hook-lib blast radius) — not auto-discovery of the new fixture.

## Interface Contracts

This task does not create or modify shared code interfaces. The single edited symbol,
`DATA_BEARING_PREFIXES` in `.claude/hooks/lib/pii-scan-scope.sh`, is an existing
internal contract already consumed by both PII hooks via `source`; this task extends
its VALUE (one added prefix), not its name, shape, or the consuming loops. No
downstream task plans against a new signature. (The ADR-0021-T1 re-insertion and
ADR-0025-T1 maintained-output tasks depend on the BEHAVIOR this enables — name-scan
coverage on `vault/artifacts/generated/` — which their own acceptance criteria
re-verify against the live hooks; they do not import this list.)

## Verification Checklist

- [ ] AC-1: `vault/artifacts/generated/` appears in `DATA_BEARING_PREFIXES` in `.claude/hooks/lib/pii-scan-scope.sh`, and both hooks build their `data_bearing` argument from that shared list — verified by `rg "vault/artifacts/generated" .claude/hooks/lib/pii-scan-scope.sh` (matches) and `rg "DATA_BEARING_PREFIXES" .claude/hooks/block-pii-commit.sh .claude/hooks/pre-push-pii-scan.sh` (matches the iteration site in each).
- [ ] AC-2: a staged `vault/artifacts/generated/plan.html` containing the operator-identity token is DENIED by `block-pii-commit.sh` — verified by the deny case in `test_pii_scan_scope_artifacts.sh`.
- [ ] AC-3: the same name-bearing artifact in a push range is DENIED by `pre-push-pii-scan.sh` — verified by the push deny case in `test_pii_scan_scope_artifacts.sh`.
- [ ] AC-4: a de-identified (initials-only, no identity/contact token) `vault/artifacts/generated/plan.html` is ALLOWED by both hooks (no over-block) — verified by the allow case in `test_pii_scan_scope_artifacts.sh`.
- [ ] AC-5: `bash .claude/hooks/tests/test_pii_scan_scope_artifacts.sh` passes with both the deny case and the allow case green.
- [ ] AC-6: **[AMENDED 2026-06-24]** the governance FLOOR + the PII-hook-lib blast radius both green — `bash scripts/tests/run-all-tests.sh` (the floor; no governance negative test regresses) AND the directly-run `.claude/hooks/tests/` set: `test_pii_scan_scope_artifacts.sh`, `test_block_ungated_vault_write.sh`, `test_commit_matcher.sh`, `test_resolve_target_repo.sh` (the PII-hook libs `commit-matcher.sh`/`resolve-target-repo.sh` this scope change feeds — NOT auto-discovered by `run-all-tests.sh`, run by hand).
- [ ] Risk (ADR-0021 N2 / ADR-0025 N3) mitigation covered — by AC-2/AC-3 (name-bearing artifact DENIED) paired with AC-4 (clean artifact ALLOWED).
- [ ] Risk (ADR-0005 Falsification) — this task is the boundary; AC-2/AC-3 prove a re-inserted name cannot reach a committed/pushed artifact.
- [ ] No regression in the full Python suite: `.venv/bin/python -m pytest -q` green.
- [ ] Files modified match the file manifest (no scope creep): only `.claude/hooks/lib/pii-scan-scope.sh` (Modify) and `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh` (Create).
- [ ] Interface contracts documented (no new shared interface; the "no interfaces" statement above applies).

## Commit

```
fix(hooks): scan vault/artifacts/generated for operator names
```
Body explains why: the scoped operator-NAME scan excluded the maintained-output
dropzone, so a re-inserted real name in a committed plan render was undetected; adding
the prefix to the single-sourced `DATA_BEARING_PREFIXES` closes the hole for both the
commit gate and the push backstop. Cite ADR-0021 OQ-1 / ADR-0025 OQ-1 and the spec
disposition #1 (Block).

Stage only (each `git add` as its own command BEFORE `git commit` — the commit hook
denies single-call stage+commit):
- `.claude/hooks/lib/pii-scan-scope.sh`
- `.claude/hooks/tests/test_pii_scan_scope_artifacts.sh`

## Rollback

If verification fails after 3 fix cycles:
1. `git stash -m "failed-ADR-0021-T0-SCANSCOPE-attempt-{N}"` — preserve work for diagnosis.
2. `git checkout {commit-before-task}` — revert to the entry-state HEAD.
3. Update the issue tracker: flag ADR-0021-T0-SCANSCOPE as BLOCKED with the failure log.
4. Escalate: "Task ADR-0021-T0-SCANSCOPE failed verification after 3 attempts. Stash ref: {ref}. Failure log: {summary}." This task is a hard dependency of ADR-0021-T1 and ADR-0025-T1 — a BLOCKED state halts Wave 2's re-insertion task and Wave 3's maintained output.
5. After abandonment/re-planning, drop all `failed-ADR-0021-T0-SCANSCOPE` entries from `git stash list`.

Do NOT: silently skip a failing acceptance criterion, weaken a test to pass (e.g.
drop the AC-4 allow case to make a blanket per-se-deny "pass", or remove the name
token from the AC-2 fixture), or proceed to ADR-0021-T1 / ADR-0025-T1 with this
boundary broken.
