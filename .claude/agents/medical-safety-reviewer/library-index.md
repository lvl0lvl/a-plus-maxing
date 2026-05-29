# medical-safety-reviewer — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for an `/upgrade-agent` adversarial-safety dispatch. Auto-loaded files and substrate are declared in agent.md §Context Loading and are not duplicated here.

## Reference Map

| Reference | Path / Source | When to Load | Role-Specific Notes |
|-----------|---------------|--------------|---------------------|
| Reviewer-output audit script | scripts/audit-safety-reviewer-output.sh | Only when LIVE, to run the mechanical pre-audit on the reviewer's OWN findings report before return (§5 rule 10) or read a failing exit code | PROPOSED — does not yet exist (design §13). While PROPOSED, the six structural checks (schema validates, locators resolve, probe-hash uniqueness, threat-model cell enumeration, severity_proposed-only, composite_band→deploy_verdict mapping) are hand-run via Read+grep; never self-attest a check not actually run; never patch the script — file a bug + escalate. [PF-S3-01, PF-S6-01 at file-load layer] |
| Specialist audit script | scripts/audit-specialist-profile.sh | Only when LIVE, as the mechanical-pre-audit prerequisite BEFORE adversarial probing (§4.2 row 2; Finding 7); `audit_passed: false` returns the candidate to Role 2 without Role 4 dispatch | PROPOSED — does not yet exist; Role-2-owned (design §13). While PROPOSED, the candidate's `audit_passed: true` frontmatter is a necessary input, not a verdict. Consume the result; never patch or self-author the script. |
| Per-attack-class published reference | substrate domain-research.md citations (e.g., medRxiv Authority Impersonation [6], HiddenLayer universal-bypass [3]) | When authoring `decision_rule_applied` for a finding (design §10.4 step 18) | Read the cited lines only; never tag external research live (tavily/WebFetch forbidden). The substrate is the frozen Pass-1 corpus. |
| Prior Architecture Questions | design/.medical-safety-reviewer-design-work/architecture-questions/AQ-<NNN>-*.md | When authoring a new AQ, to avoid duplicating an open one | Check before raising a taxonomy-gap or H-class-boundary AQ (e.g., a needed 9th refusal class, H4/H6 ambiguity per Limitation 13). |
| Prior reviewer findings | design/.medical-safety-reviewer-design-work/reviews/<slug>-*.md | When the candidate has prior reviewer history (re-review-on-amendment per §4.3 row 3) | Load as `prior_findings:` inputs, never as verdicts (mechanical-fix-is-not-a-verdict; PF-S3-01 medical analog). Re-dispatch with fresh probes when ancestry SHA drifts (AP-6). |
| Threat-model catalog history | basic-memory MCP search (project a-plus-maxing) | When auditing whether a candidate's threat surface is already cataloged (design §10.4 step 19) | The live catalog file `templates/threat-model-catalog.yaml` is AUTO-load (PROPOSED — does NOT exist on disk yet; do NOT fire `context-load-missing` HALT on its absence: until OQ-7 builds it, substrate Finding 4 L119–L155 is the de-facto A×S×P×H source per agent.md §Context Loading). Only its historical/versioned entries are conditional via MCP. |

## Loading Rules

- **Max conditional references per dispatch:** 3 (the table above is the candidate set; design §10.4).
- **Skip-pre-loading:** per agent.md §Context Loading, conditional reads happen only when the current probe/section needs them. Do not load "just in case."
- **Why the taxonomies + threat-model catalog are NOT here:** design §10.1 lists `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, and `templates/threat-model-catalog.yaml` (PROPOSED) as AUTO-load — the reviewer audits every candidate against all three, every dispatch, and re-Reads them BETWEEN probe classes (§10.7) — so they live in agent.md §Context Loading, not in this conditional table. Likewise the Role 1/2/3 §4 OUTBOUND tables, `memory/process-failures.md`, `INVARIANTS.md`, and `vault/meta/operator-profile.md` are auto-load. This conditional table holds only references read on a specific probe/finding/re-review trigger.
- **No MCP-first override:** all references above are static project artifacts (the catalog-history entry is a search over project-local vault notes, not an external doc); the Context7 override in LIBRARY_INDEX_TEMPLATE.md does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references. The orchestrator should NOT route framework refs to this profile. All references above are role-specific adversarial-review substrate.
