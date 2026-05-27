# health-specialist-architect — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for a Phase-2/Phase-3 design-authoring task. Auto-loaded files and substrate are declared in agent.md §Context Loading and are not duplicated here.

## Reference Map

| Reference | Path / Source | When to Load | Role-Specific Notes |
|-----------|---------------|--------------|---------------------|
| aplus-research SKILL | .claude/skills/aplus-research/SKILL.md | Authoring the template variant's Tools section or its `Permitted Skills` list (R14); confirming the six blocking gates referenced by downstream specialists | Treat as REFERENCED-not-dispatched. The architect names the skill in the template; the specialist runs it. Do not invoke gates from this role. |
| vault/WIKI.md | vault/WIKI.md | Authoring the template's Context Loading default (R5, R7) or specifying the contradiction-logging discipline (Finding 7, R9) | Read the Agent Consumers section and entity schemas only. Do not load full WIKI for unrelated authoring passes. |
| AGENT_TEMPLATE.md + existing role profiles | ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md, ~/Documents/Projects/skills_library/roles/{role}/agent.md | Authoring §3 mapping or verifying base-section coverage; cross-referencing how other foundation roles encode a section | Read template as evidence, never edit (§8.3 forbids). Existing profiles are precedent, not template — copy patterns, not content. |
| vault decisions | vault/decisions/ | A template default depends on a prior architectural choice (e.g., a refusal-class taxonomy item or audit-script contract) | Cite ADR by filename in the design-doc. Do not duplicate ADR content into the template variant. |
| Regulatory primary text | (see notes) | Authoring a §5 Core Rule or §11 anti-pattern with statutory anchor; encoding the device-vs-non-device verdict in the template's refusal taxonomy | Sources: FD&C Act §520(o)(1)(E) [statutory]; FDA 2026 CDS Final Guidance §V [regulatory]; IMDRF SaMD N12; FDA GMLP principles 1-10. Cite the section/principle, not the whole document. The verdict against the anchor is load-bearing; wording is editorial (per §9.2). |

## Loading Rules

- **Max references per task:** 3 (per catalog.md Budget Guardrails; inherited).
- **Skip-pre-loading:** Per design-doc §10.5, conditional reads happen only when the task surface requires them. Do not load "just in case."
- **Cross-reference pairs:** aplus-research SKILL + vault/WIKI.md when authoring the template's Tools and Context Loading sections together (R5, R7, R14 cluster). AGENT_TEMPLATE.md + an existing role profile when authoring §3 base-section mapping. Regulatory text + vault decisions when authoring a refusal-taxonomy item that has both a statutory anchor and a project ADR.
- **No MCP-first override:** Unlike framework refs in catalog.md, all references above are static project artifacts (skill docs, vault content, regulatory text). The Context7 override pattern in `LIBRARY_INDEX_TEMPLATE.md` does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references that framework-coding roles use. The orchestrator should NOT route framework refs (e.g., `nextjs`, `security`, `testing`) to this profile. All references above are role-specific design substrate.
