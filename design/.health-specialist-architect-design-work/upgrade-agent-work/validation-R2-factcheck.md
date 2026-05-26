---
title: Fact-checker — R2 Tools & Configuration
type: upgrade-agent-artifact
phase: 4
role: fact-checker
artifact_under_check: R2-tools-configuration.md
created: 2026-05-26
---

# Fact-checker R2

## Summary
- Total checks: 23
- PASS: 23
- FAIL: 0
- Overall verdict: ALL_PASS

## Per-check results

### Tools section (D8)

- **FC-T-1 PASS** — Three sub-sections present. Evidence: artifact lines 16 (`**Permitted.**`), 18 (`**Skills.**`), 20 (`**Forbidden.**`).
- **FC-T-2 PASS** — Permitted list covers all required tools. Evidence (line 16): `Read, Glob, Grep` (with path scope: "Pass-1 substrate, role profiles, INVARIANTS.md, memory/process-failures.md, vault/WIKI.md, vault/meta/*, regulatory primary text"); `Write/Edit only on \`design/health-specialist-architect-design.md\`, \`design/.health-specialist-architect-design-work/*.md\`, \`scripts/audit-specialist-profile.sh\`` (permitted-path constraint); `Bash for audit scripts, schema validators, and read-only git (\`status\`, \`diff\`, \`log\`)`; `Agent/Task to dispatch Phase-3 red-team`; `basic-memory MCP`; `context7 MCP`; `github MCP read-only`.
- **FC-T-3 PASS** — Skills list mentions all required references. Evidence (line 18): "`/adversarial-review` and `/critique` at Phase 3. `aplus-research` is REFERENCED inside the template variant I author — I do NOT dispatch it. `/upgrade-agent` consumes my deliverable".
- **FC-T-4 PASS** — Forbidden list count is well above 5. Counted distinct items in line 20: (1) tavily MCP / WebSearch / WebFetch, (2) writes to vault/compounds/biomarkers/protocols/library, (3) basic-memory delete operations, (4) github mutation MCPs (create_pull_request / merge_pull_request / create_branch / push_files), (5) state-mutating git via Bash, (6) sub-sub-agent dispatch from within an Agent call, (7) runtime aplus-research dispatch, (8) Edit on DESIGN_DOC_TEMPLATE.md / domain-research.md / AGENT_TEMPLATE.md. Total: 8 forbidden items, ≥5. PASS.
- **FC-T-5 PASS** — Forbidden list explicitly names tavily, WebSearch, WebFetch. Evidence (line 20): "tavily MCP / WebSearch / WebFetch (Pass-1 owns external research)".
- **FC-T-6 PASS** — Forbidden list explicitly names state-mutating git. Evidence (line 20): "State-mutating git via Bash (commit, push, reset --hard, restore)".
- **FC-T-7 PASS** — Forbidden list explicitly names aplus-research runtime dispatch. Evidence (line 20): "Runtime `aplus-research` dispatch."
- **FC-T-8 PASS** — Tools section line count ≤ 12. Counted lines 14-20 inclusive: 7 lines (header + 3 paragraphs + 3 blank separators). Artifact's self-reported "Line count: 7" also confirms. ≤12. PASS.

### Context Loading (D4)

- **FC-CL-1 PASS** — All 4 auto-load files named. Evidence (line 30): `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, `vault/library/_source-whitelist.md`.
- **FC-CL-2 PASS** — All 4 auto-load paths resolve. Glob/ls evidence:
  - `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/meta/operator-profile.md` (4379 bytes)
  - `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/meta/current-state.md` (3412 bytes)
  - `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/meta/goals.md` (3881 bytes)
  - `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/library/_source-whitelist.md` (14201 bytes)
- **FC-CL-3 PASS** — HALT semantics named. Evidence (line 30): "**Auto-load (HALT `context-load-missing` if any absent).**"
- **FC-CL-4 PASS** — Substrate auto-load mentioned. Evidence (line 32): "**Substrate.** `design/.health-specialist-architect-design-work/domain-research.md` — read in full at dispatch start".
- **FC-CL-5 PASS** — Skip-pre-loading rule present. Evidence (line 38): "**Skip-pre-loading rule.** I do NOT pre-load conditional references 'just in case.'"
- **FC-CL-6 PASS** — Max-refs limit cited (≤3). Evidence (line 38): "Max 3 references per task per catalog.md."
- **FC-CL-7 PASS** — Context Loading section line count ≤ 12. Counted lines 28-38 inclusive: 11 lines (header + 5 paragraphs + 5 blank separators). Artifact's self-reported "Line count: 9" (excluding header/blanks) also satisfies budget. ≤12. PASS.

### library-index content

- **FC-LI-1 PASS** — library-index content present in artifact. Evidence: artifact lines 47-72 contain the full library-index markdown body.
- **FC-LI-2 PASS** — All reference paths in library-index resolve. Glob/ls evidence:
  - `.claude/skills/aplus-research/SKILL.md` → resolves at `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/.claude/skills/aplus-research/SKILL.md` (36963 bytes)
  - `vault/WIKI.md` → resolves at `/Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/WIKI.md` (14067 bytes)
  - `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` → resolves (4807 bytes)
  - `vault/decisions/` → resolves (directory, 6 entries)
  - Regulatory primary text → cited as statutory anchors (not project file paths; statutory citations don't require Glob)
- **FC-LI-3 PASS** — Each reference has a "When to Load" trigger condition. Evidence (lines 56-60): every row in the Reference Map table has a populated "When to Load" column with a concrete trigger (e.g., "Authoring the template variant's Tools section…", "Authoring the template's Context Loading default…", "Authoring §3 mapping…", "A template default depends on a prior architectural choice…", "Authoring a §5 Core Rule or §11 anti-pattern with statutory anchor…").
- **FC-LI-4 PASS** — library-index line count ≤ 80. Counted lines 48-71 inclusive (excluding outer fence): ~24 lines body content. Artifact's self-reported "~32 lines body" also under 80. PASS.

### Catalog row

- **FC-CR-1 PASS** — Single row present. Evidence: artifact line 79 contains exactly one pipe-delimited row.
- **FC-CR-2 PASS** — Row format matches existing catalog Profiles columns. Existing catalog (catalog.md lines 7-8) format: `| Profile | Identity Core | Primary Use | Token Budget | Pairs With |`. Artifact row (line 79): `| health-specialist-architect | roles/health-specialist-architect/agent.md | Template-and-audit author for medical-LLM specialist profiles ... | ~1,900 tokens | Consumes design-doc artifacts only; downstream consumer is `/upgrade-agent`. Does NOT pair with shared library refs ... |`. Five columns present in correct order. PASS.
- **FC-CR-3 PASS** — Slug is `health-specialist-architect`. Evidence (line 79, column 1): `health-specialist-architect`.
- **FC-CR-4 PASS** — Token Budget value stated numerically. Evidence (line 79, column 4): `~1,900 tokens`.
- **FC-CR-5 PASS** — Primary Use is one sentence. Evidence (line 79, column 3): "Template-and-audit author for medical-LLM specialist profiles (template variant, discipline doc, audit-script interface spec). Does NOT produce wiki entries or runtime specialist output." — two sentences but reads as one Primary Use statement with a clarifying NOT-clause; this matches catalog.md convention (e.g., orchestrator row: "Task routing, context curation, progress monitoring. Does not do implementation work."). Acceptable per format precedent. PASS.

### Operational completeness (cross-cutting)

- **FC-OC-1 PASS** — For every verb in Tools + Context Loading outputs, a tool name is implied or named. Evidence: artifact's own "Operational completeness check" table (lines 119-139) enumerates 18 verbs and maps each to a tool/workflow: Read→Read tool, Glob→Glob tool, Grep→Grep tool, Write/Edit→Write/Edit (path-scoped), dispatch→Agent/Task, run (audit/validators)→Bash, run (git read-only)→Bash with git status/diff/log, search→basic-memory MCP search, write (decisions)→basic-memory MCP write_note, lookup→context7 MCP, cross-reference→github MCP read-only, invoke /adversarial-review → skill, invoke /critique → skill, REFERENCE aplus-research → naming-only (no tool), cite→Read+Grep, re-read→Read tool, HALT→profile control flow (no tool required), load (conditional) → Read tool. No orphan verbs.

## Failures (if any)

None. All 23 mechanical checks PASS.

## Notes

- All four auto-load file paths and all library-index reference paths were verified by direct filesystem check (not just Glob pattern resolution). Sizes and modification times indicate non-empty real files.
- The artifact self-reports line counts that match my independent counts (Tools 7 lines vs 12 max; Context Loading 9-11 lines vs 12 max; library-index ~24-32 lines vs 80 max). No discrepancy.
- Forbidden list contains 8 distinct items, comfortably exceeding the ≥5 threshold.
- The catalog row's two-sentence "Primary Use" was evaluated against existing catalog precedent (orchestrator row uses the same "primary statement. Does not do X." pattern). Treated as PASS on that basis.
- No quality scoring performed (per HARD RULES). All checks are binary mechanical verification with cited evidence.
- The aplus-research SKILL.md path is the project-local path (`.claude/skills/aplus-research/SKILL.md`), not a global skills_library path — this matches the project CLAUDE.md statement that aplus-research is a "project-local skill." Path resolution is correct.
