# aplus-research skill — test findings (dogfood)

Issues surfaced while running `/aplus-research` by hand on a fresh machine to produce the
BPC-157 re-run. Captured for potential fixes (a-plus skill and/or the shared skills_library).
Categorized by where the fix would land. Started 2026-06-18 (S15, from skill_consolidator).

| # | Where | Severity | Finding | Disposition |
|---|---|---|---|---|
| AR-1 | a-plus `aplus-research` | major | **Pre-flight verifies `jsonschema` (documented HALT) but NOT the wrapped `deep-research` skill.** Phases 2/3/4/5 are "execute deep-research Phase N"; if `~/.claude/skills/deep-research` is absent/broken (it was a dangling symlink here), those phases have no implementation and nothing HALTs early. | Add a `deep-research`-resolves check to the pre-flight → HALT `deep-research-missing`. Filed for fix. |
| AR-2 | a-plus `aplus-research` (portability) | major | **Tooling hardcoded to MCP.** `allowed-tools` + body name `mcp__tavily__*` + `mcp__basic-memory__*`; a session without those servers can't run the skill as written. The functions (web search/extract, vault-note writes) are substitutable (WebSearch/WebFetch + filesystem writes). Same class as skills_library `ky9` (execute-plan hardcoded pytest). | Document MCP-agnostic fallbacks, or detect-and-substitute. Filed. |
| AR-3 | setup friction | minor | Fresh-machine run needed `pip install jsonschema` + vendoring `deep-research` from skills_library. The jsonschema HALT is documented but there's no one-shot "items to install" note for a new workspace. | Add a pre-flight setup checklist / `requirements`. Noted. |
| AR-4 | environment (not a skill bug) | info | `~/.claude/skills/deep-research` was a **broken symlink** — listed by `ls` but no `SKILL.md`. The wrapper has no resilience to a dangling deep-research install. | Covered by AR-1's resolve-check (checks the target, not just the entry). |
| AR-5 | a-plus `aplus-research` | major | **SKILL.md gate-2.75 example omits two schema-REQUIRED fields: `timestamp` (always) and `update_reason_slug` (when update_mode+PASS).** An orchestrator following the documented JSON block (SKILL.md lines 160-171) produces a schema-INVALID gate that HALTs `schema-validation-failed`. Doc↔schema drift. | Sync the SKILL.md example to the schema (add `timestamp` + `update_reason_slug`). Filed. |

## Substitutions in effect for this run (so results are interpretable)
- Web research: **WebSearch + WebFetch** instead of `mcp__tavily__tavily_search/extract`.
- Vault writes: **direct filesystem Write/Edit** instead of `mcp__basic-memory__write_note`.
- deep-research phases: followed from `skills_library/skills/deep-research/{SKILL.md,reference/}` (read + execute), since the global skill wasn't installed.
- `aplus-research` itself executed **by hand** (it's a-plus project-local, not registered in this skill_consolidator-rooted session).

(Appended as the run surfaces more.)

## AR-6 (MAJOR/BLOCKING) — gate_attest Phase-3.5 gate-global mtime breaks per-section remediation
SKILL.md Phase 3.5 = per-section re-dispatch; gate_attest uses ONE gate-global `iter_start_ts` and rejects any judge JSON older than it. Sections converging at different iterations (A iter3, B/D iter1, C/E iter2) → attest HALTs `stale-agent-source` on the earlier ones → the gate can never reach PASS for the common partial-remediation case. Fix: per-section iteration tracking, or accept a PASS judge by its own iter, or mandate+cost a whole-phase final re-judge. (skill_consolidator bead filed.)

**AR-6 STATUS: FIXED** (commit 9ae92e8) — gate_attest now resolves each Phase-3.5 judge against the iteration it claims; smoke tests 16→18 (T_AR6a positive + T_AR6b negative); the BPC-157 gate-3.5 composes PASS. PR to lvl0lvl/a-plus-maxing.
