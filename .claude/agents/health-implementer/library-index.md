# health-implementer — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for a `/upgrade-agent` Phase 5 specialist-authoring task. Auto-loaded files and substrate are declared in agent.md §Context Loading and are not duplicated here.

## Reference Map

| Reference | Path / Source | When to Load | Role-Specific Notes |
|-----------|---------------|--------------|---------------------|
| Refusal-class taxonomy | templates/refusal-class-taxonomy.yaml | Authoring a specialist's Role Boundaries refusal-class enumeration (R5; ≥4 distinct, `AUTHORITY_FRAMING_BYPASS` mandatory) | The audit-readable mirror of Role 1 §2.2 item 3. Encode ≥4 existing classes; never invent a class — a needed 5th class is an Architecture Question (worked example B). |
| Specialist risk-class table | templates/specialist-risk-class.yaml | Setting a specialist's `aplus-research` mode floor in its Tools section (R12; EC-5) | Mode floor ≥ the role's risk-class-derived minimum. peptide-specialist → `--mode=deep`; sleep-coach → `--mode=standard`. Do not default `--mode=standard` for compound-class specialists. |
| Audit script | scripts/audit-specialist-profile.sh | Self-audit before return; source only to diagnose a failing check | PROPOSED — does not yet exist (design §13 rows all PROPOSED). When LIVE, run against own output and return `audit_passed: true`; while PROPOSED, return `deferred-script-absent` with AQ/bead ref (per agent.md Core Rule 9; the full legal terminal-state set lives there). Do not patch the script; file a bug and escalate. |
| Prior-finalized specialist profiles | .claude/agents/<slug>/agent.md | Authoring the IDENTICAL block (SHA-256 match) or checking R9 DIFFER Jaccard ≤0.30 | Load 1–2 priors per pairwise check, not all 14. IDENTICAL content is copied verbatim from canonical, never edited per-specialist. |
| Base agent template | ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md | Verifying base-section coverage and the 11-section count (10 base + Modes) at a section boundary | Read as evidence, never edit (§Tools forbids). Re-read at each section boundary; do not enumerate sections from memory (PF-S2-05). |

## Loading Rules

- **Max conditional references per task:** 5 (the table above is the full set).
- **Skip-pre-loading:** Per agent.md §Context Loading, conditional reads happen only when the section being authored requires them. Do not load "just in case."
- **Cross-reference pair:** refusal-class taxonomy + a prior-finalized specialist profile when authoring the IDENTICAL block (refusal scaffold is IDENTICAL content). specialist-risk-class table + AGENT_TEMPLATE.md when authoring the Tools section.
- **No MCP-first override:** all references above are static project artifacts. The Context7 override in `LIBRARY_INDEX_TEMPLATE.md` does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references. The orchestrator should NOT route framework refs to this profile. All references above are role-specific authoring substrate.
