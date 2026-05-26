---
title: Foundation-Role agent.md Location — Canonical in skills_library, Project Symlink
type: decision
status: active
owner: walter
created: 2026-05-26
last_reviewed: 2026-05-26
depends_on: ["2026-05-23-wiki-schema"]
superseded_by: null
review_cadence: per-deployment (re-rotate if /upgrade-agent canonical-path or enforce-role-inlining regex changes)
permalink: a-plus-maxing/decisions/2026-05-26-foundation-role-agent-md-location
---

# Decision: Foundation-Role agent.md Canonical Path

## Context

The a-plus-maxing project builds 14 medical specialist agent profiles per `vault/WIKI.md` Agent Consumers table, sequenced as 4 foundation roles → 3 pilot specialists → 11 remaining specialists. The foundation roles being authored are:

- `health-specialist-architect`
- `health-implementer`
- `health-edge-case-reviewer`
- `medical-safety-reviewer`

`vault/WIKI.md` references project-local agent profiles at `<project>/.claude/agents/<name>.md`. The global `/upgrade-agent` command (at `~/.claude/commands/upgrade-agent.md`) reads target profiles from `roles/{name}/agent.md` interpreted relative to `~/Documents/Projects/skills_library/`. The project's `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook implements INV-ROLE-INLINING by regex-matching `roles/[a-z-]+/agent\.md` against dispatch prompt bodies.

These three references (WIKI.md says project-local; `/upgrade-agent` says global skills_library; the hook regex pattern-matches the global skills_library path form) need a single resolution before any of the 4 foundation roles' agent.md files are actually authored.

The decision was raised during Session 5 scoping conversation (the same conversation that produced the Session 5 scope contract). Three options were discussed:

- **(a) Project-local everywhere.** Adapt `/upgrade-agent` to read project paths. Pro: clean isolation. Con: requires `/upgrade-agent` skill modification — out of scope per the S5 scope contract's "no skill modifications" boundary.
- **(b) Global skills_library only.** 14 new role directories land in global skills_library/roles/. Pro: matches `/upgrade-agent` and hook expectations. Con: profiles become invisible to project file tree; loses project-level visibility for ownership audit.
- **(c) Both — global as canonical source, project gets symlink or copy.** Pro: canonical lives where `/upgrade-agent` + hook expect; project gets visibility for ownership audit. Con: dual-maintenance risk if symlink/copy drifts.

## Decision

Option (c) is chosen.

- **Canonical:** `~/Documents/Projects/skills_library/roles/{role-slug}/agent.md`
- **Project visibility:** `<project>/.claude/agents/{role-slug}.md` — symlink (preferred) OR copy (acceptable; see Trade-off below) pointing at the canonical.

The 4 foundation role slugs (kebab-case, matching the regex `[a-z][a-z-]+`):

- `health-specialist-architect`
- `health-implementer`
- `health-edge-case-reviewer`
- `medical-safety-reviewer`

## Rationale

`/upgrade-agent` is a downstream consumer for actual profile authoring (Session B). Modifying `/upgrade-agent` to accept project-local paths is a non-trivial change to a global skill that other projects depend on — it would create cross-project breakage and is out of scope for the Session 5 work. Keeping the canonical at the skills_library path means `/upgrade-agent` reads its target from the location it natively expects.

The `enforce-role-inlining.sh` hook's regex (`roles/[a-z-]+/agent\.md`) was designed assuming the skills_library path form. Keeping the canonical at that path means the hook fires correctly on dispatches that should inline a role profile.

The `.claude/agents/{role-slug}.md` symlink (or copy) gives the project file tree visibility into which roles the project owns — important for the project's audit-script tooling (your work in `scripts/`) and for cross-document ownership matrix discipline in CLAUDE.md.

## Alternatives Considered (and rejected)

See Context. (a) rejected because requires `/upgrade-agent` skill modification. (b) rejected because loses project-level visibility for ownership audit. (c) chosen.

## Trade-off

Symlink vs copy in `.claude/agents/`:

- **Symlink (preferred):** zero-maintenance; canonical updates propagate instantly; git correctly tracks the symlink target. Risk: if the skills_library directory is moved (rename/relocation), the symlink breaks.
- **Copy:** more brittle (must re-sync after canonical updates); but survives skills_library relocation.

Default: symlink. If skills_library relocation becomes a real risk, revisit.

## Breaks If

- `/upgrade-agent` skill canonical-path lookup pattern changes (currently reads `roles/{name}/agent.md` under `~/Documents/Projects/skills_library/`).
- `enforce-role-inlining.sh` hook's regex changes to NOT match the skills_library path form.
- The skills_library directory is moved without updating the symlink.
- A future decision elects to relocate the 14 specialist agent.md files to a different canonical (in which case this decision is superseded).
- Cross-project skills_library is split (e.g., per-project skills_library copies are introduced), at which point "global skills_library" stops being a stable concept.

## Operational Pre-conditions (for Session B execution)

Before Session B authors the first foundation-role agent.md file via `/upgrade-agent`:

1. Confirm `~/Documents/Projects/skills_library/roles/{role-slug}/` does not already exist for any of the 4 foundation slugs (no name collision).
2. Confirm `.claude/agents/` directory exists in this project (create if missing).
3. For each foundation role authored, immediately create the symlink:
   `ln -s ~/Documents/Projects/skills_library/roles/{role-slug}/agent.md .claude/agents/{role-slug}.md`
4. Verify the symlink resolves with `readlink .claude/agents/{role-slug}.md`.
5. Test by dispatching a no-op Agent tool call referencing the role-slug; the `enforce-role-inlining.sh` hook should fire if the prompt does NOT inline the full 11-section profile.

## Relations

- `vault/decisions/2026-05-23-wiki-schema.md` — defines the 14-specialist roster
- `vault/WIKI.md` Agent Consumers — references `.claude/agents/` location (will resolve via symlink under this decision)
- `~/.claude/commands/upgrade-agent.md` — downstream consumer for actual profile authoring
- `.claude/hooks/enforce-role-inlining.sh` — INV-ROLE-INLINING enforcement; relies on this decision's canonical path form
- `design/{role}-design.md` (Pass 2 deliverables, pending) — design docs that inform Session B authoring
- `design/.{role}-design-work/domain-research.md` (Pass 1 deliverables, committed) — research substrate

## Documentation Lag Note

This decision was made in conversation during Session 5 scoping but was not recorded in vault at that time. The Session 5 scope contract referenced the decision only as a negative ("`.claude/agents/` deferred to Session B"). The parallel session's review of `design/CONTINUATION_BRIEF.md` surfaced the documentation gap and prompted this retrospective ADR write-up on 2026-05-26.

Per project change-discipline, decisions of this consequence (cross-cutting boundary that 14 role profiles will follow) should land in vault/decisions/ at the time of decision, not retrospectively. Recurrence guard: at any Pass 2 / Pass 3 scoping conversation, the first action is to check whether the scoping conversation produces a decision worth a vault ADR — if yes, write it before the work begins.
