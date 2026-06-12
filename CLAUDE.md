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

## Session Close Protocol

Before saying "done" or "complete":

1. **Run full test suite** -- `.venv/bin/python -m pytest -q` (the V1 Python suite, since S31/Wave 2). For governance/tooling-only sessions, run the relevant `scripts/tests/*.sh` shell suites.
2. **Scope check** -- `git diff --name-only`. Every file not in your original scope needs a justification.
3. **Drift detection (3 checks):**
   - **Task drift:** Re-read the scope contract from session start. Evaluate each acceptance criterion: PASS, FAIL, or CHANGED. If any criterion was silently changed during the session, that is drift. Document what changed and why.
   - **Architecture drift:** Read INVARIANTS.md (or the project's architecture-invariants doc). For each invariant, ask: "Did this session's work move the project closer to violating this invariant?" If yes for any invariant, flag it with the invariant ID.
   - **Vision drift:** In one sentence, state what the system IS after this session's changes. Compare against the first sentence of `design/vision.md` (or the project's vision doc). If they describe different systems, that is drift.
   Write all three checks explicitly. Do not skip any. Do not combine them into a summary.
4. **Update HANDOFF.md** with What Changed, Current State, What Is Next, Key References, and the **Top-3 active failure modes** pointer (VOLATILE — rotates each session). **Mandatory PF attestation:** either append a new entry to `memory/process-failures.md`, OR add an explicit line at the close: `S{N} close (YYYY-MM-DD): No new PF-class entries this session.` followed by 1-2 sentences of rationale listing what was observed but did NOT promote (and why). **Silence is NOT equivalent to absence.** This enforces INV-PF-ATTESTATION.
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
8.5. **Run audit scripts** -- For every invariant in INVARIANTS.md with a Mechanical Verification entry, run that script. On non-zero exit: do NOT commit until fixed or explicit user-adjudicated path-extension granted. Run all five at every close (and run `branch-completeness-audit.sh` at session OPEN too):
   - `scripts/handoff-audit.sh` — INV-HO-ROTATION + INV-HO-NO-STALE-HASH
   - `scripts/scope-contract-audit.sh --session <N>` — INV-SCOPE-CONTRACT (asserts latest contract matches current session)
   - `scripts/pf-attestation-audit.sh --session <N>` — INV-PF-ATTESTATION (asserts close attestation dated current session)
   - `scripts/skill-trace-audit.sh --session <N>` — INV-SKILL-TRACE (PF-S39/S40/S51 family: asserts the close attestation carries the per-PR gated-skill invocation table; the audit reads the PF log's `## Session <N>` section, so every close writes that section carrying the close attestation plus the per-PR table, or the exact sentence `No PR lifecycles ran this session.`)
   - `scripts/branch-completeness-audit.sh` — INV-TRUNK-COMPLETENESS (asserts the checkout holds every deployed agent on `origin/main` + the governance layer; catches branch-write fragmentation, PF-S22-01)

   Conditional: for any aplus-research dispatch this session run `scripts/audit-research-provenance.sh <design-work-dir> <slug>` (bda — asserts the mode-required attested gates are PRESENT, then runs `gate_attest.py verify-chain`; closes the vacuous-pass hole where verify-chain alone skips ABSENT gates). This is the INV-RESEARCH-PROVENANCE-DISJOINT enforcement and is mandatory before any specialist's research feeds a wiki write.
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
| What Did NOT Work (failed approaches) | `memory/process-failures.md` | HANDOFF.md carries pointer only |
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
- **DOCUMENT_RUBRIC.md** -- Rules for document lifecycle management

Query the vault: `mcp__basic-memory__search` with project `a-plus-maxing`.

## Hooks

Six PreToolUse hooks are registered (`.claude/settings.json`; the roster is pinned by `scripts/tests/test_settings_hook_paths.sh`), plus one git-native pre-push hook installed outside settings:

- **block-dangerous.sh** -- Denies recursive rm at root, `git reset --hard`, `git push --force` (allows `--force-with-lease`), `git clean -fd`
- **block-push-main.sh** -- Denies `git push <remote> main/master`. Use feature branches.
- **block-commit-main.sh** -- Denies commits on `main` (mirror of the push block).
- **block-ungated-vault-write.sh** -- Denies committing a `vault/{compounds,biomarkers,library}/` entity page that has not passed the ingestion gate (INV-WIKI-INGESTION-GATED).
- **enforce-role-inlining.sh** -- Denies a role-context Task dispatch that does not inline the full role profile (INV-ROLE-INLINING).
- **block-pii-commit.sh** -- Denies a commit that stages a filled-scaffold/store path or whose content carries operator PII (ADR-0005; registered S45, bead 3lv). Scans the repo receiving the commit (worktree-aware via the hook input's cwd; bead `29u4`) and runs `bd sync --flush-only` before reading `.beads/issues.jsonl` so bead text still pending in `.beads/beads.db` is scanned too, denying on flush failure (bead `ycqo`). **Commit-sequencing rule:** stage with `git add` as its own command, then `git commit` separately — the hook denies single-call stage+commit, `git commit -a/--all`, and pathspec `git commit <path>` (their content is invisible to the pre-command staged-set scan).
- **pre-push-pii-scan.sh** (`.claude/hooks/`, installed to `.git/hooks/pre-push` by `init_instance`, not a settings.json hook) -- Scans the push range as the backstop to the commit-time scan — for human-terminal commits (which bypass the PreToolUse hooks entirely) and for the commit scan's documented residuals (bead dv3); the bead-pending (`ycqo`) and worktree-blind (`29u4`) windows are closed at commit time since S52. `git push --no-verify` bypasses it.

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
- **Store-surface tasks:** any task writing to or reading from `scripts/store/` MUST satisfy `docs/checklists/store-adversarial-tests.md` (adversarial cross-stream + dedupe-collision + mutation battery; bead `pka`, S37-S41 pattern) — checked at Tier-1 self-check AND in the Tier-2 QA dispatch.
- **Per session:** one wave (or the remaining tasks of an open wave) → checkpoint → `/review-pr` → `/merge` → close. Each wave is a natural session boundary.
- **Live wave-state** (which tasks built/open) lives in `vault/meta/overview.md` (the phase-state owner — not here, to keep CLAUDE.md static). Out-of-order builds (S32-S35, PF-S36-01) left earlier waves partial; re-entry completes the open waves in order.

## Project-local skills

- **aplus-research** (`.claude/skills/aplus-research/`) — wraps global `deep-research` with mechanically enforced gates for health-domain research that lands in the wiki. Use via `/aplus-research "<question>" [--mode=...]`. Six blocking gates: scope (Phase 2.75), judge (3.5), integrity (4.75), critique (6, deep+), risk-floor (7.5, compounds), layers (8.5, standard+ compounds). Three health-specific gates not in `deep-research`: population-mismatch, risk-floor, concentration-audit. See `.claude/skills/aplus-research/SKILL.md`.
