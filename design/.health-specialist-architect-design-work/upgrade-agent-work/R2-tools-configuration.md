---
title: R2 Tools & Configuration — Research Output
type: upgrade-agent-artifact
phase: 3
researcher: R2
created: 2026-05-26
---

# R2 Output

### Output A — Tools section (paste-ready, ≤12 lines)

```markdown
## Tools

**Permitted.** Read, Glob, Grep (Pass-1 substrate, role profiles, INVARIANTS.md, memory/process-failures.md, vault/WIKI.md, vault/meta/*, regulatory primary text). Write/Edit only on `design/health-specialist-architect-design.md`, `design/.health-specialist-architect-design-work/*.md`, `scripts/audit-specialist-profile.sh` (interface spec). Bash for audit scripts, schema validators, and read-only git (`status`, `diff`, `log`). Agent/Task to dispatch Phase-3 red-team — full role profile inlined per INV-ROLE-INLINING; no sub-sub-agents. basic-memory MCP (search + write decisions at close). context7 MCP for canonical API lookup. github MCP read-only.

**Skills.** `/adversarial-review` and `/critique` at Phase 3. `aplus-research` is REFERENCED inside the template variant I author — I do NOT dispatch it. `/upgrade-agent` consumes my deliverable; I do not invoke it.

**Forbidden.** tavily MCP / WebSearch / WebFetch (Pass-1 owns external research). Writes to `vault/compounds/`, `vault/biomarkers/`, `vault/protocols/`, `vault/library/<class>/`. `mcp__basic-memory__delete_note` / `delete_project`. `mcp__github__create_pull_request` / `merge_pull_request` / `create_branch` / `push_files`. State-mutating git via Bash (commit, push, reset --hard, restore). Sub-sub-agent dispatch from within an Agent call. Runtime `aplus-research` dispatch. Edit on `DESIGN_DOC_TEMPLATE.md`, `domain-research.md`, `AGENT_TEMPLATE.md`.
```

Line count: 7 (3 paragraphs + 4 blank/header). Within ≤12.

### Output B — Context Loading section (paste-ready, ≤12 lines)

```markdown
## Context Loading

**Auto-load (HALT `context-load-missing` if any absent).** `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, `vault/library/_source-whitelist.md` — I read these to author template defaults against the file's actual shape; I do NOT personalize architect-output to operator content.

**Substrate.** `design/.health-specialist-architect-design-work/domain-research.md` — read in full at dispatch start; cite Findings by number, never paraphrase.

**Project spec (re-read at section boundaries; PF-S2-05 guard).** `design/DESIGN_DOC_TEMPLATE.md`, `INVARIANTS.md`, `memory/process-failures.md`, `design/CONTINUATION_BRIEF.md`.

**Conditional (load only when task surface requires; see library-index.md).** aplus-research SKILL.md, vault/WIKI.md, AGENT_TEMPLATE.md + existing role profiles, vault/decisions/ ADRs, regulatory primary text.

**Skip-pre-loading rule.** I do NOT pre-load conditional references "just in case." Max 3 references per task per catalog.md.
```

Line count: 9. Within ≤12.

### Output C — library-index full content

Deployed to `~/Documents/Projects/skills_library/roles/health-specialist-architect/library-index.md`.

```markdown
# health-specialist-architect — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for a Phase-2/Phase-3 design-authoring task. The four auto-load files (`vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, `vault/library/_source-whitelist.md`) and the substrate (`design/.health-specialist-architect-design-work/domain-research.md`) are loaded by the agent profile itself and are NOT listed here.

## Reference Map

| Reference | Path | When to Load | Role-Specific Notes |
|-----------|------|--------------|---------------------|
| aplus-research SKILL | .claude/skills/aplus-research/SKILL.md | Authoring the template variant's Tools section or its `Permitted Skills` list (R14); confirming the six blocking gates referenced by downstream specialists | Treat as REFERENCED-not-dispatched. The architect names the skill in the template; the specialist runs it. Do not invoke gates from this role. |
| vault/WIKI.md | vault/WIKI.md | Authoring the template's Context Loading default (R5, R7) or specifying the contradiction-logging discipline (Finding 7, R9) | Read the Agent Consumers section and entity schemas only. Do not load full WIKI for unrelated authoring passes. |
| AGENT_TEMPLATE.md + existing role profiles | ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md, ~/Documents/Projects/skills_library/roles/{role}/agent.md | Authoring §3 mapping or verifying base-section coverage; cross-referencing how other foundation roles encode a section | Read template as evidence, never edit (§8.3 forbids). Existing profiles are precedent, not template — copy patterns, not content. |
| vault decisions | vault/decisions/ | A template default depends on a prior architectural choice (e.g., a refusal-class taxonomy item or audit-script contract) | Cite ADR by filename in the design-doc. Do not duplicate ADR content into the template variant. |
| Regulatory primary text | (statutory) FD&C Act §520(o)(1)(E); (regulatory) FDA 2026 CDS Final Guidance §V; IMDRF SaMD N12; FDA GMLP principles 1-10 | Authoring a §5 Core Rule or §11 anti-pattern with statutory anchor; encoding the device-vs-non-device verdict in the template's refusal taxonomy | Cite the section/principle, not the whole document. The verdict against the anchor is load-bearing; wording is editorial (per §9.2). |

## Loading Rules

- **Max references per task:** 3 (per catalog.md Budget Guardrails; inherited).
- **Skip-pre-loading:** Per design-doc §10.5, conditional reads happen only when the task surface requires them. Do not load "just in case."
- **Cross-reference pairs:** aplus-research SKILL + vault/WIKI.md when authoring the template's Tools and Context Loading sections together (R5, R7, R14 cluster). AGENT_TEMPLATE.md + an existing role profile when authoring §3 base-section mapping. Regulatory text + vault decisions when authoring a refusal-taxonomy item that has both a statutory anchor and a project ADR.
- **No MCP-first override:** Unlike framework refs in catalog.md, all references above are static project artifacts (skill docs, vault content, regulatory text). The Context7 override pattern in `LIBRARY_INDEX_TEMPLATE.md` does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references that framework-coding roles use. The orchestrator should NOT route framework refs (e.g., `nextjs`, `security`, `testing`) to this profile. All references above are role-specific design substrate.
```

Line count: ~32 lines body. Within ≤80.

### Output D — Catalog row (append to orchestrator catalog Profiles table)

```
| health-specialist-architect | roles/health-specialist-architect/agent.md | Template-and-audit author for medical-LLM specialist profiles (template variant, discipline doc, audit-script interface spec). Does NOT produce wiki entries or runtime specialist output. | ~1,900 tokens | Consumes design-doc artifacts only; downstream consumer is `/upgrade-agent`. Does NOT pair with shared library refs (frameworks/domains/pipelines); references are role-specific per health-specialist-architect/library-index.md. |
```

### Minimum Viable Encoding (10-15 lines)

Lines that MUST survive any further compression (load-bearing for D4/D8 verification):

1. Tools: permitted Read/Glob/Grep with path scope.
2. Tools: Write/Edit ONLY on `design/health-specialist-architect-design.md`, `design/.health-specialist-architect-design-work/*.md`, `scripts/audit-specialist-profile.sh`.
3. Tools: Bash read-only git only.
4. Tools: Agent/Task with INV-ROLE-INLINING and no sub-sub-agent rule.
5. Tools: basic-memory MCP + context7 MCP + github MCP read-only.
6. Skills: `/adversarial-review`, `/critique`, aplus-research REFERENCED-not-dispatched, `/upgrade-agent` as consumer.
7. Forbidden: tavily/WebSearch/WebFetch.
8. Forbidden: vault-write paths (compounds/biomarkers/protocols/library).
9. Forbidden: basic-memory delete + github mutation MCPs + state-mutating git.
10. Forbidden: sub-sub-agent dispatch, runtime aplus-research, Edit on template/substrate.
11. Context Loading: 4 auto-load files enumerated with HALT semantics.
12. Context Loading: substrate (domain-research.md) loaded in full at dispatch start.
13. Context Loading: 5 project-spec files (DESIGN_DOC_TEMPLATE.md, INVARIANTS.md, memory/process-failures.md, CONTINUATION_BRIEF.md) re-read at section boundaries.
14. Context Loading: conditional reads enumerated, deferred to library-index.md.
15. Context Loading: skip-pre-loading rule + max-3-refs limit.

### Cut Rationale

What was considered and excluded:

- **§8.4 PF-S2-06 OUT-OF-SCOPE reasoning.** Considered embedding the two-layer defense rationale in the Tools section. Cut: belongs in Anti-Patterns (R1 owns), not Tools. Tools states the boundary; Anti-Patterns explains why a PF is structurally unreachable.
- **§10.6 cross-role reference triggers.** Considered listing the outbound re-read discipline in Context Loading. Cut: this is a Communication-section concern (R3 owns the §4 outbound mechanics).
- **§10.7 scope-clarification paragraph** (template variant vs this design doc). Cut: this is meta-commentary that belongs in the design doc, not the deployed profile. Specialists reading the deployed profile do not need it.
- **Tier-Tag-gated Read discipline (F-S13).** Considered adding to Tools/Context Loading. Cut: it constrains the *template variant the architect designs*, not the architect itself. Belongs in the template-variant artifact, not the architect's profile.
- **Audit-script invocation cookbook.** Considered listing the three audit scripts explicitly. Cut: the architect *authors the interface spec*, doesn't run audit scripts in production. The Phase-7 verification path is owned by `/upgrade-agent`, not by the architect at runtime.
- **Regulatory primary-text per-section anchors** (full citation strings). Cut from Context Loading body, moved to library-index where the citation lives next to its trigger condition.
- **Context7 override pattern.** Cut: this role consumes no framework references with version drift, so the override is inert. Stated explicitly in library-index "Notes on framework."
- **Per-reference token counts.** Cut: not tracked for project-internal artifacts; only catalog.md's framework/domain refs carry token estimates.

### Operational completeness check

For each verb appearing in Output A + Output B + Output C, confirm a corresponding tool or workflow exists:

| Verb | Where it appears | Corresponding tool/workflow |
|------|------------------|------------------------------|
| Read | Tools, Context Loading | Read tool (permitted) |
| Glob | Tools | Glob tool (permitted) |
| Grep | Tools | Grep tool (permitted) |
| Write / Edit | Tools | Write/Edit (path-scoped) |
| dispatch | Tools (Phase-3 red-team) | Agent/Task tool (permitted) |
| run (audit scripts, schema validators) | Tools | Bash (permitted) |
| run (git read-only) | Tools | Bash with `git status`/`diff`/`log` |
| search (vault) | Tools | basic-memory MCP search |
| write (decisions at close) | Tools | basic-memory MCP write_note |
| lookup (canonical API) | Tools | context7 MCP |
| cross-reference (upstream artifacts) | Tools | github MCP read-only |
| invoke `/adversarial-review` | Tools | `/adversarial-review` skill |
| invoke `/critique` | Tools | `/critique` skill |
| REFERENCE aplus-research | Tools, library-index | naming in template — no tool needed |
| cite (Finding N / R<N>) | Context Loading | Read + Grep against `domain-research.md` |
| re-read (section boundary) | Context Loading | Read tool, per PF-S2-05 |
| HALT (`context-load-missing`) | Context Loading | profile-internal control flow (no tool required) |
| load (conditional reference) | Context Loading | Read tool, gated by library-index trigger |

Result: every verb maps to a permitted tool or named workflow. No orphan verbs.

### Source citations

| Line / claim | Source |
|--------------|--------|
| Permitted: Read / Glob / Grep with substrate + INVARIANTS + memory/process-failures + vault scopes | design-doc §8.1 lines 205-207 |
| Write/Edit path scope (`design/health-specialist-architect-design.md`, `design/.health-specialist-architect-design-work/*.md`, `scripts/audit-specialist-profile.sh`) | design-doc §8.1 line 208 |
| Bash read-only git + audit scripts | design-doc §8.1 line 209 |
| Agent/Task INV-ROLE-INLINING + no sub-sub-agent | design-doc §8.1 line 210 (cites Pass-1 Lesson 1) |
| basic-memory MCP permitted (search + close-time write) | design-doc §8.1 line 211 |
| context7 MCP permitted | design-doc §8.1 line 212 |
| github MCP read-only permitted | design-doc §8.1 line 213 |
| `/adversarial-review` + `/critique` skills | design-doc §8.2 lines 217-218 |
| aplus-research REFERENCED-not-dispatched | design-doc §8.2 line 219 (R14 anchor) |
| `/upgrade-agent` as consumer | design-doc §8.2 line 220 |
| Forbidden: tavily / WebSearch / WebFetch | design-doc §8.3 line 224 |
| Forbidden: vault-write paths | design-doc §8.3 line 225 |
| Forbidden: basic-memory delete operations | design-doc §8.3 line 226 |
| Forbidden: github PR-mutation MCPs | design-doc §8.3 line 227 |
| Forbidden: state-mutating git | design-doc §8.3 line 228 |
| Forbidden: sub-sub-agent dispatch | design-doc §8.3 line 229 (Pass-1 Lesson 1) |
| Forbidden: aplus-research runtime dispatch | design-doc §8.3 line 230 |
| Forbidden: Edit on DESIGN_DOC_TEMPLATE.md / domain-research.md / AGENT_TEMPLATE.md | design-doc §8.3 line 231 |
| 4 auto-load files (operator-profile / current-state / goals / source-whitelist) | design-doc §10.1 lines 290-293 |
| HALT `context-load-missing` semantics | design-doc §10.1 line 288 |
| Substrate load (domain-research.md, full at dispatch start, cite by number) | design-doc §10.2 line 297 |
| Project-spec reads (DESIGN_DOC_TEMPLATE.md / INVARIANTS.md / memory/process-failures.md / CONTINUATION_BRIEF.md) | design-doc §10.3 lines 301-304 |
| PF-S2-05 re-read-at-boundary discipline | design-doc §10.3 line 301 |
| Conditional reads (aplus-research SKILL / WIKI / AGENT_TEMPLATE.md / decisions / regulatory) | design-doc §10.4 lines 308-312 |
| Skip-pre-loading rule | design-doc §10.5 line 316 |
| Max 3 references per task | catalog.md "Budget Guardrails" line 87 |
| Catalog row format (Profile / Identity Core / Primary Use / Token Budget / Pairs With) | catalog.md Profiles table lines 7-16 |
| library-index Reference Map columns (Reference / Path / When to Load / Role-Specific Notes) | LIBRARY_INDEX_TEMPLATE.md lines 7-11 |
| library-index Loading Rules section (max-refs, cross-reference pairs, MCP-first note) | LIBRARY_INDEX_TEMPLATE.md lines 13-18 |
| Context7 override inapplicability for static project artifacts | LIBRARY_INDEX_TEMPLATE.md lines 20-29 vs design-doc §10.4 (no framework refs) |
| D4 verification criteria (4 auto-loads + max-refs limit + conditional triggers) | agent-rubric.md D4 lines 57-67 |
| D8 verification criteria (3 sub-sections + ≥5 forbidden items + operational completeness) | agent-rubric.md D8 lines 103-113 |
| Operational completeness verb→tool mandate | agent-rubric.md "Operational completeness" lines 159-169 |
