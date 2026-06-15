# a-plus-maxing

## Project Overview

a-plus-maxing project. See HANDOFF.md for current session context.

## Session Start Protocol

Every session begins with these steps in order:

1. **Read HANDOFF.md** -- What happened last session. What is next. Any blockers. Read the Top-3 active failure modes pointer FIRST in the volatile section — that's the forward-facing readiness scan.
2. **Read INVARIANTS.md** -- The active register. Note any TODO mechanical-enforcement entries.
3. **Check git status** -- `git status && git log --oneline -5`. Right branch? Uncommitted changes? Resolve before starting.
4. **Read memory/process-failures.md** -- Every session start regardless of task simplicity. The point of the log is the next session doesn't re-make the mistake.
5. **Read vault/meta/landmarks.md** -- Active landmarks + trigger windows for any landmark within window today.
6. **Run test baseline** -- `.venv/bin/python -m pytest -q` (the V1 Python suite, since S31/Wave 2; `.venv` is the per-instance pytest runtime — Python 3.14 + pytest, gitignored). If tests fail before you changed anything, fix that first. Non-Python sessions: the shell audit suites under `scripts/tests/*.sh` are the baseline for governance/tooling work.
7. **Write the Scope Contract** -- Before writing any code, state in plain text and obtain user confirmation:

   ```markdown
   ## Scope Contract — Session [N]
   Goal: [one sentence, imperative mood]
   Acceptance criteria:
   - [ ] [binary pass/fail criterion 1]
   - [ ] [binary pass/fail criterion 2]
   Files I WILL touch: [explicit list]
   Files I will NOT touch: [explicit list — often the most valuable line]
   NOT doing: [explicit exclusions of plausibly-in-scope items]
   Invariants at risk: [IDs from INVARIANTS.md, or "none"]
   ```

   The contract is appended into HANDOFF.md after user confirmation. At session close, each AC is evaluated PASS / FAIL / CHANGED / N/A in writing. A criterion silently changed during the session is drift.

   **For `v1-build` tasks (executing a `docs/task-plan/` recipe):** the contract additionally cites the build-plan wave the task belongs to (per `docs/build-plan/build-plan-v1-full.md`) and attests the prior wave's checkpoint Go/No-Go passed before the task is built. Build via `/execute-plan` (see V1 Build Execution), never a hand-rolled per-task dispatch — PF-S36-01. (Mechanical enforcement of this field is a tracked follow-up, not yet in `scope-contract-audit.sh`.)

### Self-recognition flags (catch yourself BEFORE acting on these)

Per Rigor Framework Discipline 7 + PF-S3-01. When you catch yourself producing one of these framings, pause and explicitly call it out, then default to the thorough option:

- "Avoid clutter"
- "5 min of grunt work"
- "Minor accretion"
- "We'll formalize later" / "rolls into next cycle anyway"
- "Just docs-only" / "no behavior change"
- "Umbrella bead" / "consolidate into one item"
- "The fix is mechanical so the verdict is mechanical" (← canonical PF-S3-01 framing)
- "Re-dispatching would be expensive given how much I've already dispatched"
- "The agent's prose summary has the answer; the gate JSON is just bookkeeping"

### Core-capability-first gate (PF-S63-02)

Before adopting any secondary-work scope, answer in writing: **does the core capability — generating a followable health plan, end-to-end — work yet?** (As of S65: NO — there is no model/API client in `scripts/`, `plan/assemble.py` has no production caller, `generate.run` renders only dashboard/report; bead `71s4`.) Secondary work (substrate, polish, adapters, governance) does NOT proceed on the strength of "the components each pass their own tests" — that is the exact PF-S63-02 drift. If a session's goal is legitimately secondary, the scope contract states the core-capability answer explicitly and why the secondary work is the right next step anyway. The MECHANICAL form of this gate (a script asserting the path is wired) lands WITH the `71s4` build, since its checks depend on the path's shape. **Guard-loosening corollary (PF-S63-02):** treat any recommendation to LOOSEN a drift-guard as itself a red flag — name the failure class the guard prevents and obtain explicit informed sign-off before acting; never default-accept.

## Session Close Protocol

Before saying "done" or "complete":

1. **Run full test suite** -- `.venv/bin/python -m pytest -q` (the V1 Python suite, since S31/Wave 2). For governance/tooling-only sessions, run the relevant `scripts/tests/*.sh` shell suites.
2. **Scope check** -- `git diff --name-only`. Every file not in your original scope needs a justification.
3. **Drift detection (3 checks):**
   - **Task drift:** Re-read the scope contract from session start. Evaluate each acceptance criterion: PASS, FAIL, or CHANGED. If any criterion was silently changed during the session, that is drift. Document what changed and why.
   - **Architecture drift:** Read INVARIANTS.md (or the project's architecture-invariants doc). For each invariant, ask: "Did this session's work move the project closer to violating this invariant?" If yes for any invariant, flag it with the invariant ID.
   - **Vision drift:** In one sentence, state what the system IS after this session's changes. Compare against the first sentence of `design/vision.md` (or the project's vision doc). If they describe different systems, that is drift.
   Write all three checks explicitly. Do not skip any. Do not combine them into a summary.
4. **Update HANDOFF.md** with What Changed, Current State, What Is Next, Key References, and the **Top-3 active failure modes** pointer (VOLATILE — rotates each session). **Mandatory PF attestation:** either append a new entry to `memory/process-failures.md`, OR add an explicit line at the close: `S{N} close (YYYY-MM-DD): No new PF-class entries this session.` followed by 1-2 sentences of rationale listing what was observed but did NOT promote (and why). **Silence is NOT equivalent to absence.** This enforces INV-PF-ATTESTATION. **Disclosure ledger (Rigor Framework Discipline 8 / F-013, formalized S65):** the close attestation also carries a `Disclosure ledger (S{N} close)` block — every failure caught this session that the operator did NOT flag, each with its detection mode (`self`/`gate`) + `surfaced_by`, plus a count of how many reached the operator only because they asked (target: 0 — self/gate should catch them first). An empty ledger is stated explicitly (`Caught this session: 0`), never omitted.
5. **Apply the rotation rule to every VOLATILE-labeled section** (mandatory at session close).

   The rotation rule applies to:
   - HANDOFF.md step-12 context-package pointer
   - HANDOFF.md Current State (volatile)
   - HANDOFF.md What Is Next (volatile)
   - HANDOFF.md Scope Contract Evaluation (volatile)
   - Project-local `MEMORY.md` ONLY when it exceeds 150 lines

   It does NOT apply to user-scoped `~/.claude/projects/.../memory/MEMORY.md` (tool-managed by claude-mem; out of scope).

   The 6 clauses (apply to ANY VOLATILE-labeled section, not only step-12):

   1. **Replace, don't accrue.** A VOLATILE section's body contains ONLY the current session's content. Prior-session bullets are REMOVED, not preserved inline. The prior context is the archaeology — HANDOFF/MEMORY does not mirror its contents.
   2. **Single-line Historical pointer.** At most one line per VOLATILE section may reference the prior session's archived content, in the form `**Historical (kept for reference):** vault/sessions/session-<N>.md` (or analogous artifact path). No horizontal rules, no re-labels, no inline content excerpt.
   3. **No sha256 prefixes in narrative.** HANDOFF/MEMORY prose does not cite sha256 hash prefixes (`sha256 abc123…`). Hashes are brittle — they go stale the moment a fix-commit lands. sha256 provenance lives in versioned artifacts (ADRs, vault decisions, vault context-packages). HANDOFF points at those artifacts by filename.
   4. **Self-dating volatile facts.** HANDOFF may cite `main at {SHA}` but only adjacent to a date/session stamp (e.g., `as of YYYY-MM-DD S<N> close`) so staleness is self-evident to the next reader.
   5. **No duplicate "Historical" labels.** The word "Historical" appears at most once per VOLATILE section.
   6. **Session-close diff check.** Before committing the HANDOFF/MEMORY update, diff each VOLATILE section against the previous version. Removed lines should include ALL prior-session inline content; kept lines should be structural scaffold (section header + current-session summary + single Historical pointer).

   Apply this rule to ANY VOLATILE-labeled section, not only step-12. Specifically: HANDOFF.md Current State + MEMORY.md when >150 lines.

5.5. **Stale-hash audit.** Audit HANDOFF.md and MEMORY.md for sha256 prefixes or branch SHAs in narrative prose. Move to artifact citations (vault notes, ADRs) if found.
6. **Update memory** -- Write vault notes for any decisions, patterns, or open questions.
7. **Update beads** -- `bd close` completed issues, `bd sync --flush-only`.
8. **Review documents** -- Run the Document Freshness Rubric (see DOCUMENT_RUBRIC.md). Flag or archive stale docs.
8.5. **Run the close gate** -- `scripts/close-audit.sh --session <N>` is the single mandatory close gate (Rigor Framework v1.0.0 Discipline 1 step 7 / F-008 fail-closed; adopted S64). It runs the negative-test FLOOR first — `toolkit/tests/run-all-tests.sh` + `scripts/tests/run-all-tests.sh`, proving each audit can still go RED on bad input (F-007) — then the per-close roster below, FATALing (exit 2) if any constituent could not RUN (a skipped check never reads as clean). It additionally runs a NON-GATING `falsification-scan` advisory (vendored `toolkit/scripts/falsification-scan.sh`, Wave B / S65) over THIS session's `## Session <N>` PF note — WARN-only, never affecting the gate verdict; review any surfaced anti-pattern (increment-by-default / framework-circularity / a-priori-by-construction / soft-confirmation-laundering) and confirm or dismiss it in the close attestation. On any non-zero exit: do NOT commit until fixed or explicit user-adjudicated path-extension granted. Roster (also run `branch-completeness-audit.sh` at session OPEN too):
   - `scripts/handoff-audit.sh` — INV-HO-ROTATION + INV-HO-NO-STALE-HASH
   - `scripts/scope-contract-audit.sh --session <N>` — INV-SCOPE-CONTRACT (asserts latest contract matches current session)
   - `scripts/pf-attestation-audit.sh --session <N>` — INV-PF-ATTESTATION (asserts close attestation dated current session)
   - `scripts/skill-trace-audit.sh --session <N>` — INV-SKILL-TRACE (PF-S39/S40/S51 family: asserts the close attestation carries the per-PR gated-skill invocation table; the audit reads the PF log's `## Session <N>` section, so every close writes that section carrying the close attestation plus the per-PR table, or the exact sentence `No PR lifecycles ran this session.`)
   - `scripts/branch-completeness-audit.sh` — INV-TRUNK-COMPLETENESS (asserts the checkout holds every deployed agent on `origin/main` + the governance layer; catches branch-write fragmentation, PF-S22-01)

   The gate default-excludes one tracked pre-existing red from the a-plus floor — `test_audit_research_provenance.sh` (environmental: `gate_attest verify-chain` needs `jsonschema`, absent here; bead `a-plus-maxing-d1kc`); the exclusion is printed loudly, never silent. Conditional: for any aplus-research dispatch this session run `scripts/audit-research-provenance.sh <design-work-dir> <slug>` (bda — asserts the mode-required attested gates are PRESENT, then runs `gate_attest.py verify-chain`; closes the vacuous-pass hole where verify-chain alone skips ABSENT gates). This is the INV-RESEARCH-PROVENANCE-DISJOINT enforcement and is mandatory before any specialist's research feeds a wiki write.
8.6. **Run the harvest gate (self-improvement loop, F-017)** -- For any process failure logged this session, `toolkit/scripts/harvest-gate.sh --pf memory/process-failures.md --harvest harvest.jsonl --beads .beads/issues.jsonl --session <N>` must pass: every session failure is captured in ALL of the PF log + `harvest.jsonl` + a bead, or the close fails. Seed a missing harvest record by hand-authoring a FAIL record conforming to `toolkit/schemas/harvest-record.md` (gate-required keys: `id`, `class`, `source_refs`, `detection_mode`, `recurrence_count` — set `id` to the PF-id token, e.g. `PF-S63-02`, so `harvest-gate` discovers it) and appending it to `harvest.jsonl`. `toolkit/scripts/pf-ingest.sh` is the COMPANION transform — it emits the anti-pattern / negative-example STUB that feeds `/upgrade-agent` (role) or `/upgrade-skill` (skill) so the failure permanently hardens the artifact that caused it (Loop A). NOTE: pf-ingest's emitted JSONL is NOT yet harvest-gate-valid (it uses `pf_id`/`record_type`, not the FAIL schema), so promote it to the schema before appending — a tracked toolkit rough edge, bead `po4x`. A zero-failure session passes vacuously ("nothing to gate"); reference PRIOR PFs DESCRIPTIVELY in the close attestation, not by bare `PF-S{N}-{NN}` token, or harvest-gate treats them as this-session failures (also `po4x`). Loop B (cross-deployment harvest) is a future discipline.

   **Close-attestation template (harvest-gate / skill-trace clean BY CONSTRUCTION — S65, bead `po4x`).** The upstream toolkit rough edges are not ours to patch (the vendored scripts are not forked); the a-plus-side mitigation is to author the session's PF section in this exact shape so both gates pass first time:

   ```markdown
   ## Session <N> (YYYY-MM-DD)

   ### Per-PR gated-skill invocation table (INV-SKILL-TRACE)
   | PR | `/review-pr` invoked fresh | `/merge` invoked fresh | Outcome |
   |----|----------------------------|------------------------|---------|
   | #NNN — <what> | YES — <how> | YES — <how> | <result> |
   <!-- if NO PR lifecycle ran this session, omit the table and instead put this -->
   <!-- EXACT sentence on its OWN line (line-anchored; optional leading **): -->
   No PR lifecycles ran this session.

   ### PF attestation
   S<N> close (YYYY-MM-DD): <One new PF promoted — PF-S<N>-NN | No new PF-class entries this session>. <rationale>. Prior PFs referenced DESCRIPTIVELY ("the verify-first discipline held"), NEVER by bare `PF-S{M}-NN` token.

   ### Disclosure ledger (S<N> close)
   Caught this session: <K>.   <!-- or exactly: Caught this session: 0 -->
   - <failure> — detection: <self|gate>; surfaced_by: <self|operator>.
   ```

   Two hard constraints this shape satisfies: (a) the skill-trace escape sentence is LINE-ANCHORED (own line); (b) the ONLY bare `PF-S<N>-NN` tokens in the section are genuine this-session promotions that ARE captured in `harvest.jsonl` + a bead — so harvest-gate's token-grep finds no uncaptured token.
8.7. **Landmark window check** -- Re-read `vault/meta/landmarks.md`. For each `active` landmark whose trigger window opened during this session, verify the corresponding action was performed.
9. **Commit and push** to your short-lived working branch (`feature/*` or `fix/*` off `main`). Open a PR to `main` if ready; never commit to `main` directly.

## Cross-Document Ownership Matrix

Each fact lives in exactly one document. If you find duplication, the table below names the owner; archive the duplicate per DOCUMENT_RUBRIC.md Rule 5.

| Fact / Concern | Owner | Notes |
|----------------|-------|-------|
| Session protocols (start/close) | CLAUDE.md | Static across sessions |
| Project conventions (branch, commit) | CLAUDE.md | Static |
| Hook configuration | `.claude/settings.json` | CLAUDE.md only describes |
| Current session continuity (what's next) | HANDOFF.md | VOLATILE |
| Scope contract for current session | HANDOFF.md | VOLATILE |
| Step-12 context-package pointer | HANDOFF.md | VOLATILE; rotation rule applies |
| What Did NOT Work (failed PROCESS approaches) | `memory/process-failures.md` | Protocol violations / near-misses; HANDOFF.md carries pointer only. EXCLUDES failed technical experiments |
| Failed TECHNICAL approaches (dead-end designs) | `vault/approaches/` | F-014 negative-knowledge ledger (adopted S65); query by tag before a non-trivial approach. See `vault/approaches/README.md` |
| Architectural decisions — product pipeline | `docs/adr/` (+ `docs/prd/`) | Numbered ADRs from `/create-adr` (V1 set: ADR-0001…0007); HANDOFF.md does NOT carry decision rationale |
| Architectural decisions — vault-native (governance / knowledge graph) | `vault/decisions/` | Date-named vault decisions; HANDOFF.md does NOT carry decision rationale |
| Component interfaces / parameters | `vault/components/`, `vault/parameters/` | Read source first, never write from memory |
| Phase-state facts (e.g., milestone status) | `vault/meta/overview.md` | NOT in HANDOFF.md (would accrue) |
| Cross-session research findings | `vault/research/` | HANDOFF.md cites by filename |
| Session summaries | `vault/sessions/session-<N>.md` | One per session |
| Active contradictions | `vault/meta/contradictions.md` | Updated on discovery |
| User directives + index | MEMORY.md (≤150 lines) | Index, not database |

## Knowledge Vault

This project uses a basic-memory vault at `vault/` for structured knowledge tracking.

- **CLAUDE.md** -- Static project instructions (loaded every session)
- **HANDOFF.md** -- Session-to-session continuity (what happened, what's next)
- **vault/** -- Structured knowledge graph (entities, decisions, relations) viewable in Obsidian
- **vault/approaches/** -- Negative-knowledge ledger (F-014, adopted S65): one file per ABANDONED technical approach (dead-end designs, rejected optimizations). Query by tag before committing to a non-trivial approach; append on abandon, never delete. See `vault/approaches/README.md`
- **DOCUMENT_RUBRIC.md** -- Rules for document lifecycle management

Query the vault: `mcp__basic-memory__search` with project `a-plus-maxing`.

## Hooks

Six PreToolUse hooks are registered (`.claude/settings.json`; the roster is pinned by `scripts/tests/test_settings_hook_paths.sh`), plus one git-native pre-push hook installed outside settings:

- **block-dangerous.sh** -- Denies recursive rm at root, `git reset --hard`, `git push --force` (allows `--force-with-lease`), `git clean -fd`
- **block-push-main.sh** -- Denies `git push <remote> main/master`. Use feature branches.
- **block-commit-main.sh** -- Denies commits on `main` in this trunk or its worktrees (mirror of the push block; a commit targeting a different repository passes through).
- **block-ungated-vault-write.sh** -- Denies committing a `vault/{compounds,biomarkers,library}/` entity page that has not passed the ingestion gate (INV-WIKI-INGESTION-GATED). Scoped to this trunk and its worktrees.
- **enforce-role-inlining.sh** -- Denies a role-context Task dispatch that does not inline the full role profile (INV-ROLE-INLINING).
- **block-pii-commit.sh** -- Denies a commit that stages a filled-scaffold/store path or whose content carries operator PII (ADR-0005; registered S45, bead 3lv). Scans the repo receiving the commit (worktree-aware via the hook input's cwd; bead `29u4`), scoped to this trunk and its worktrees — a commit targeting a different repository passes through. For MAIN-CHECKOUT commits it runs `bd sync --flush-only` before reading `.beads/issues.jsonl` so bead text still pending in the beads database is scanned too, denying on flush failure (bead `ycqo`); the flush is skipped when no database exists (a fresh clone commits cleanly) and for worktree commits (worktree pending-bead coverage = bd's own skip-staging behavior + the pre-push scan). **Commit-sequencing rule:** stage with `git add` as its own command, then `git commit` separately — the hook denies single-call stage+commit, `git commit -a/--all`, and pathspec `git commit <path>` (their content is invisible to the pre-command staged-set scan).
- **pre-push-pii-scan.sh** (`.claude/hooks/`, installed to `.git/hooks/pre-push` by `init_instance`, not a settings.json hook) -- Scans the push range as the backstop to the commit-time scan — for human-terminal commits (which bypass the PreToolUse hooks entirely), for the commit scan's documented residuals (bead dv3), and for worktree-PENDING bead text (the `ycqo` flush-before-scan runs only for main-checkout commits; bd skips staging in worktrees, so that text reaches the boundary here — the hook fires for worktree pushes too). The worktree-blind window (`29u4`) is closed at commit time since S52. `git push --no-verify` bypasses it.

The vendored rigor toolkit also ships **`toolkit/hooks/enforce-heartbeat-clause.sh`** (0-silent-drops: DENY a Task dispatch whose prompt lacks a liveness clause). It is **VENDORED S64 but NOT YET WIRED** into `.claude/settings.json`: it fires on EVERY Task dispatch and would deny `/review-pr`'s and `/aplus-research`'s un-clause'd internal dispatches. Wiring is deferred until those flows + a dispatch convention carry the clause — bead `a-plus-maxing-0qf6`, coupled with the global-skills sync. `test_settings_hook_paths.sh` still pins the 6 wired hooks; it gains the `toolkit/hooks/` portable prefix when the heartbeat hook is wired.

## Rigor Framework (vendored toolkit)

- **`rigor_version` is pinned to `1.0.0` in the root `rigor_version` file** (one machine-diffable line; pinned S64). The Rigor Framework + its runnable `toolkit/` is a versioned dependency, not a copied snapshot. Only `toolkit/` is **vendored** here (copied, not symlinked — it is the runtime enforcement floor and must survive clone/move); the framework doc + `VERSION` + `CHANGELOG.md` live in the skills_library at `${SKILLS_LIBRARY}/frameworks/rigor/` (default `~/Documents/Projects/skills_library/frameworks/rigor/`), NOT in this repo. Do NOT edit the vendored scripts: they ship with their negative tests, and edits fork the pull line.
- **Pull cadence (Discipline 11 / Loop B):** at the periodic drift-audit boundary, diff the pinned `rigor_version` (root file) against `${SKILLS_LIBRARY}/frameworks/rigor/VERSION`, read that repo's `CHANGELOG.md` delta, and pull the `toolkit/` delta — re-running `toolkit/tests/run-all-tests.sh` (a new audit adopts only if its negative test passes, F-007) before adopting, then bump the root `rigor_version` file.
- **What a-plus adopted (S64, Wave A):** the close gate (`scripts/close-audit.sh`, embodying `toolkit/scripts/close-audit.sh`), the negative-test floor (`scripts/tests/run-all-tests.sh` + `toolkit/tests/`), the `skipped()`/FATAL-on-skip posture in `scripts/lib/audit-helpers.sh`, and the self-improvement loop (`harvest.jsonl` + `toolkit/scripts/{pf-ingest,harvest-gate}.sh` + `toolkit/schemas/harvest-record.md`).
- **a-plus keeps its bespoke audits** (handoff / scope-contract / pf-attestation / skill-trace / branch-completeness / wiki-ingest / research-provenance / PII hooks) — domain-specific and in places more evolved than the toolkit generics; the toolkit versions are the upstream for future reconciliation, not a replacement.
- **Deferred (beaded follow-ons):** heartbeat-hook wiring (`0qf6`); `plan-integrity` role adoption; approaches + disclosure ledgers + `falsification-scan` advisory (Wave B); INVARIANTS rows for the new gates via the change-discipline ritual (Wave C); global `~/.claude/skills`+`commands` sync (Wave D).

## Conventions

- **Branch topology (since S22, ADR `2026-06-02-single-trunk-reconciliation`):** `main` is the single complete trunk (full roster + governance/tooling/vault). Work on **short-lived** `feature/<short-description>` / `fix/<short-description>` branches cut off `main`, PR back to `main`, delete after merge. No long-lived continuity-carrier branch (the old `feature/wiki-bpc157-aplus-research` model caused PF-S22-01 branch-write fragmentation and is retired). `INV-TRUNK-COMPLETENESS` (`branch-completeness-audit.sh`, open+close) guards against a branch ever again holding agents/governance the trunk lacks.
- Commit format: `{type}[({scope})]: brief description`
- All beads issues use priority 0-4 (not high/medium/low)
- Documents follow the freshness rubric in DOCUMENT_RUBRIC.md

## V1 Build Execution

The V1 build executes the approved 7-wave plan `docs/build-plan/build-plan-v1-full.md` (18 dependency-ordered tasks; recipes in `docs/task-plan/`). The terminal pipeline stage (`ADR → Spec → Build Plan → Task Plan → Execute Plan`) is run with the global **`/execute-plan`** skill (`~/.claude/skills/execute-plan/`) — read it IN FULL before invoking (PF-S17-01); never hand-roll a per-task SE-dispatch substitute (PF-S36-01).

- **Project path-mapping** (the skill's defaults differ): recipes = `docs/task-plan/<task-id>.md` (not `specs/recipes/`); build plan = `docs/build-plan/build-plan-v1-full.md` (not `specs/build-plans/`); role profiles = `~/Documents/Projects/skills_library/roles/<role>/agent.md` (the canonical project source per INV-ROLE-INLINING; the skill's default `~/.claude/roles/` is a symlink to the same target on the dev machine — use the skills_library path explicitly), inlined in full.
- **The wave is the unit.** Build in build-plan wave order; a wave is not done until ALL its tasks are built, its per-wave **checkpoint Go/No-Go ran green** (the cross-spec integration gates in the build plan), AND its PR merged. "Wave N" everywhere means the build-plan topological wave, NOT an ADR-family label (reconciled S36; bead `orl`).
- **Three-tier review** (per execute-plan): Tier-1 SE self-check (recipe verification checklist) → Tier-2 wave review (QA always; Architect/Security conditional, over the whole-wave diff) → Tier-3 `/review-pr` (6-agent) before merge. No tier is skippable.
- **Build-plan integrity** is verified by the `plan-integrity` role (`~/Documents/Projects/skills_library/roles/plan-integrity/agent.md`, inlined in full per INV-ROLE-INLINING; adopted S65 / Rigor Framework v1.0.0). Before a wave builds, it grounds every task's inputs against the LIVE tree (`stat`/`grep`, never the plan's own description), confirms the dependency map is an acyclic DAG with artifact-named edges, and confirms each wave's checkpoint is runnable; as the build executes, it gates each wave transition (a wave advances only when its checkpoint Go/No-Go RAN green — executed, not reasoned). It is a READ-ONLY verification role — reports findings + routes repairs, never authors the fix — so it does NOT deploy as an a-plus agent (it is correctly absent from `branch-completeness-audit`'s deployed-roster check) and is dispatched as a review lens alongside the Tier-2/Tier-3 reviewers.
- **Store-surface tasks:** any task writing to or reading from `scripts/store/` MUST satisfy `docs/checklists/store-adversarial-tests.md` (adversarial cross-stream + dedupe-collision + mutation battery; bead `pka`, S37-S41 pattern) — checked at Tier-1 self-check AND in the Tier-2 QA dispatch.
- **Per session:** one wave (or the remaining tasks of an open wave) → checkpoint → `/review-pr` → `/merge` → close. Each wave is a natural session boundary.
- **Live wave-state** (which tasks built/open) lives in `vault/meta/overview.md` (the phase-state owner — not here, to keep CLAUDE.md static). Out-of-order builds (S32-S35, PF-S36-01) left earlier waves partial; re-entry completes the open waves in order.

## Project-local skills

- **aplus-research** (`.claude/skills/aplus-research/`) — wraps global `deep-research` with mechanically enforced gates for health-domain research that lands in the wiki. Use via `/aplus-research "<question>" [--mode=...]`. Six blocking gates: scope (Phase 2.75), judge (3.5), integrity (4.75), critique (6, deep+), risk-floor (7.5, compounds), layers (8.5, standard+ compounds). Three health-specific gates not in `deep-research`: population-mismatch, risk-floor, concentration-audit. See `.claude/skills/aplus-research/SKILL.md`.
