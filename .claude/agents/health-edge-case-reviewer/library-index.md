# health-edge-case-reviewer — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for a `/upgrade-agent` coverage-review dispatch. Auto-loaded files and substrate are declared in agent.md §Context Loading and are not duplicated here.

## Reference Map

| Reference | Path / Source | When to Load | Role-Specific Notes |
|-----------|---------------|--------------|---------------------|
| Specialist audit script | scripts/audit-specialist-profile.sh | Only when LIVE, to read a failing exit code or run the script as the mechanical-pre-audit prerequisite (§5 rule 5; Finding 9) | PROPOSED — does not yet exist (design §13; Role 2 verdict carries). While PROPOSED, treat the specialist's `audit_passed: true` frontmatter as a necessary input, not a verdict. Consume the result; never patch the script — file a bug + escalate. [PF-S6-01 at file-load layer] |
| Prior Architecture Questions | design/.health-edge-case-reviewer-design-work/architecture-questions/AQ-<NNN>-*.md | When authoring a new AQ, to avoid duplicating an open one | AQ-001 (per-specialist operator-profile fields) is the standing dependency; check it before raising an operator-coverage AQ. |
| Prior reviewer findings | design/.health-edge-case-reviewer-design-work/reviews/<slug>-*.md | When the specialist has prior reviewer history (re-review round 2 or 3 per §7) | Load priors as `prior_findings:` inputs, never as verdicts (re-review-on-amendment; PF-S3-01 medical analog). Re-review must not exceed >0.95 cosine similarity to the prior round (§13 row 24). |

## Loading Rules

- **Max conditional references per dispatch:** 3 (the table above is the full set; §10.4).
- **Skip-pre-loading:** per agent.md §Context Loading, conditional reads happen only when the section under audit needs them. Do not load "just in case."
- **Why the taxonomy + risk-class table are NOT here:** design §10.1 lists `templates/refusal-class-taxonomy.yaml` and `templates/specialist-risk-class.yaml` as AUTO-load (the reviewer audits every profile against both, every dispatch), so they live in agent.md §Context Loading, not in this conditional table. This diverges from Role 2's library-index, which lists the taxonomy as conditional because Role 2 loads it only when authoring the refusal-class section.
- **No MCP-first override:** all references above are static project artifacts; the Context7 override in LIBRARY_INDEX_TEMPLATE.md does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references. The orchestrator should NOT route framework refs to this profile. All references above are role-specific review substrate.
