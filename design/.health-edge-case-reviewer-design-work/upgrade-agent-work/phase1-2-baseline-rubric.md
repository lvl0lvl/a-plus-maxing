# Phase 1 Baseline + Phase 2 Rubric — health-edge-case-reviewer (Role 3 Session B, S14)

## Phase 1 — Baseline Evaluation

**Net-new authoring.** `ls .claude/agents/health-edge-case-reviewer/` → absent. No prior `agent.md` exists. Baseline = **0/10 on all 10 rubric dimensions** by construction. All 10 dimensions are research targets.

Source of truth: `design/health-edge-case-reviewer-design.md` (888 lines, Status: Final, red-team reviewed, all findings classified). Structural standard: `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`. Shape oracles: `.claude/agents/health-specialist-architect/agent.md` (Role 1, 127 lines / ~3,252 tok) + `.claude/agents/health-implementer/agent.md` (Role 2, 162 lines / ~5,245 tok). Deploy target: `.claude/agents/health-edge-case-reviewer/{agent,library-index}.md` per ADR `vault/decisions/2026-05-26-foundation-role-agent-md-location.md`.

**Token-budget prior (Rule 7 / S9+S13 precedent).** Medical-domain density pushes foundation profiles over the ~2,000-tok target (Role 1 ~3,252; Role 2 ~5,245). Role 3 carries a 4-axis severity composite, NCC MERP→H-class mapping, 8-class taxonomy audit, 9 composition-test patterns, 7-field return — expect overrun. DOCUMENT_RUBRIC Rule 7: classify load-bearing vs reducible; trim only reducible; document residual vs bead 2qq; never cut a safety binary.

**XR-002 (bead 4ej) status.** Design doc carries 0 `*_WITH_OVERRIDE_PATH` tokens. Role 3's verdict enum is `coverage_verdict ∈ {PASS, BLOCK_WITH_FINDINGS, HALT}` — distinct from the deploy-gate verdict carrying the inversion. Role 3 does NOT inherit XR-002. Re-verify on deployed agent.md at Phase 7.

## Phase 2 — Agent-specific rubric (research targets, all 10 dims)

Mapped to the design doc's own §-structure. A 9/10 for THIS agent:

| Dim | 9/10 for Role 3 | Verification (judge checks) |
|---|---|---|
| 1 Identity Clarity | ≤40-word declarative Identity (§2.1 verbatim, 31 words); coverage-gap-detection + pre-deployment + finding-not-fix unambiguous in first 20 lines; three-mechanism anti-sycophancy anchored (Mechanism C primary; A→Role 4 Council + intra-role cosine; B→maintain-position) | wc -w Identity ≤40; anti-sycophancy in first 20 lines; "finding, not fix" + "pre-deployment" + "coverage" present |
| 2 Context Efficiency | ≤200 lines hard / token overrun documented per Rule 7; per-section budgets respected | wc -l ≤200; tiktoken measured; residual documented |
| 3 Behavioral Specificity | 12 Core Rules (§5) each with binary pass/fail; first-person on rules 6+10 (learned-failure), imperative elsewhere; no buried checklists | each rule testable; voice tags correct |
| 4 Reference Integration | library-index maps the conditional refs (max 3/dispatch); auto-load vs NOT-auto-load (wiki content) boundary explicit; no MCP-first override misapplied | paths resolve via Glob; loading rules match §10 |
| 5 Boundary Enforcement | §2.2 I-own / I-do-NOT-own with owning role in parens (Role 1/2/4/7/orchestrator each named); finding-not-edit escalation specified | every not-owned item names owner; escalation = finding/AQ/bead never Edit |
| 6 Communication Protocol | 7-field orchestrator return (§9.1) + user register (§9.2) + Role 4 downstream format (§9.3); coverage_verdict enum + AFB-explicit tally | two registers distinct; 7 fields present; output format not prose |
| 7 Failure Recovery | 5 Loop-Breaking thresholds (§7): finding-revision cap 2, re-review round cap 3, probe-fabrication binary-0, mechanical-pre-audit-fail binary, context-scratch >5 | concrete numeric/binary thresholds |
| 8 Tool Awareness | §8 Permitted/Skills/Forbidden; Edit restricted to own work dir (never artifact under review); negative constraints present; every verb has a tool | Edit-boundary explicit; forbidden list present |
| 9 Anti-Pattern Coverage | 7 Role-3 anti-patterns (§11.2 AP-1..7) as "I don't X" with recognition cue; ≥3 distinct PF IDs (PF-S2-01/S3-01/S6-01 min); Negative Examples (3 BAD/GOOD §12) last 30 lines | 5-8 APs; ≥3 PF IDs grep-resolve; recency placement |
| 10 Freshness | refusal-taxonomy + risk-class YAML paths current; no stale advice; Context7 override noted where version-dependent | paths exist; no stale framework refs |

**Post-deployment ACs to satisfy (design §15.2b — gate Session B exit):** AC-deploy-12 (file exists), -15 (≥3 PF IDs), -16 (severity_proposed + severity_final.set_by adjudicator), -17 (divergence-log + N=5 cadence), -18 (stratification_attempted + stratifiable), -19 (voice bans = 0). AC-deploy-13/14/14a (schema + audit-reviewer-output.sh existence) are PROPOSED script-existence ACs → follow-up beads, not blocking this deploy (mirror Role 2 S13 audit_passed: deferred-script-absent posture).

**Modes decision flag for synthesis.** Design maps Findings 2/5/9 → Modes (probe-discovery, adjudication-handoff, composition-test). Role 1/2 deployed with a single mode for hook satisfaction. Resolve at synthesis: encode the modes the design intends without blowing the line budget (candidate: 2-3 named modes with Entry/Exit, or single mode if budget forces — flag residual).
