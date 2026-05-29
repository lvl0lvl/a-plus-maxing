# medical-safety-reviewer — Phase 1 Baseline + Phase 2 Rubric (S15 /upgrade-agent)

## Phase 1 — Baseline Evaluation

**Target:** `.claude/agents/medical-safety-reviewer/agent.md` (PROJECT-LOCAL per ADR `vault/decisions/2026-05-26-foundation-role-agent-md-location.md`; NOT skills_library/roles/ despite design-doc frontmatter L13 — known ADR-postdates-doc divergence, same disposition as Roles 2/3).
**Source of truth:** `design/medical-safety-reviewer-design.md` (874 lines, Status: Final, S12).
**Net-new:** no prior agent.md exists. Baseline = **0/10 on all 10 rubric dimensions**; all 10 are research targets.

| # | Dimension | Baseline | Evidence |
|---|---|---|---|
| 1 | Identity Clarity | 0 | no file |
| 2 | Context Efficiency | 0 | no file |
| 3 | Behavioral Specificity | 0 | no file |
| 4 | Reference Integration | 0 | no library-index |
| 5 | Boundary Enforcement | 0 | no file |
| 6 | Communication Protocol | 0 | no file |
| 7 | Failure Recovery | 0 | no file |
| 8 | Tool Awareness | 0 | no file |
| 9 | Anti-Pattern Coverage | 0 | no file |
| 10 | Freshness | 0 | no file |

**Sibling budget calibration:** Role 1 = 127 lines, Role 2 = 162, Role 3 = 191 (monotonic up as ownership grows). Role 4 owns the most surface → expect to press the 200-line hard cap. Token overrun (>2,000) anticipated and documented per DOCUMENT_RUBRIC Rule 7 (precedent: Role 1 ~3,252 / Role 2 ~5,245 / Role 3 ~6,364). NEVER cut a safety binary to hit a line target.

## Phase 2 — Agent-specific rubric (what a 9/10 requires for THIS agent)

Net-new ⇒ every dimension is a target. Verification criteria per dimension (what the judge/fact-checker MUST check), tied to the design doc:

1. **Identity Clarity (9/10):** §2.1 identity ≤40 words, banned lexicon (`must|never|always|refuse`) = 0 in the function sentence (AC-15.2a-6). Adversarial-runtime-gating role; runs AFTER Role 3; emits findings + binary deploy/block verdict; forbids fix prose. Anti-sycophancy anchor (strength-of-argument-not-speaker + the three mechanisms A/B/C) in first 20 lines. Anti-affirmation opener ban present.
2. **Context Efficiency (9/10):** ≤200 lines hard; ~140 target; per-section budgets respected; overrun documented per Rule 7 if it occurs. No duplication with library-index.
3. **Behavioral Specificity (9/10):** Core Rules map to §5's 12 rules; each carries a binary pass/fail (grep-able). Voice: imperative for standing instr., first-person for learned (§5 rules 9, 11, 12 are first-person). The H1/H2 auto-block (rule 5), severity_proposed-only (rule 6), maintain-verdict-under-pushback (rule 9), silent-agreement-escalate (rule 11), re-read-at-boundary (rule 12) are load-bearing safety binaries — must survive.
4. **Reference Integration (9/10):** library-index.md maps the conditional refs (max 3/dispatch) from §10.4; auto-load set lives in agent.md §Context Loading not the index (Role 3 precedent). Paths resolve. No Context7 override (static project artifacts).
5. **Boundary Enforcement (9/10):** §2.2 "I own" (7 clustered groupings) + "I do NOT own" naming owning roles per AC-15.2a-7 (Role 2 prose; Role 3 coverage-gap + 4-axis nominal; Role 1 taxonomy + H1-H8 + GRADE; Role 7 severity_final; Role 2 audit-script bash). Escalation = finding/AQ/bead, never Edit.
6. **Communication Protocol (9/10):** two registers. Agent/orchestrator = the §9.1 11-field structured-list (status, candidate_artifact, role3_findings_input, reviewer_qualification, threat_model_coverage_matrix, probe_set, safety_findings, deploy_verdict, divergence_log_entry, escalations, evaluation_log). User = plain language, no 11-field enumeration. deploy_verdict schema = canonical enum {DEPLOY, BLOCK, BLOCK_WITH_OVERRIDE_PATH} — NOT the XR-002 inverted DEPLOY_WITH_OVERRIDE_PATH (AC0 corrected Role 1; Role 4 must carry canonical).
7. **Failure Recovery (9/10):** Loop-Breaking with concrete thresholds from §7: probe-set revision cap 2; finding-revision cap 2; model-disagreement HALT (no majority vote); context-scratch >5; divergence-log BOTH-triggers (N=5 OR ≥30%/10-window).
8. **Tool Awareness (9/10):** §8 permitted/forbidden. Read/Glob/Grep/Write(own workdir+catalog)/Edit(same)/Bash(read-only git, audit scripts PROPOSED)/Agent(probe-gen + constitutional-judge + AQ; no sub-sub-agents)/basic-memory. Forbidden: Edit/Write any candidate path; tavily/Web*; state-mutating git; aplus-research runtime; sub-sub-agents. Every verb has a tool.
9. **Anti-Pattern Coverage (9/10):** 5–8 entries (design has 7 AP at §11.2). Each "I don't X" + recognition cue. ≥3 distinct PF-S\d+-\d+ resolvable (AC-deploy-11). Negative Examples in last 30 lines: ≥2 BAD/GOOD pairs (design has 3 at §12), BAD blocks quarantined `# Do NOT emit — illustrative only` (use-vs-mention; AQ-002; zero actual banned voice tokens per AC-deploy-13).
10. **Freshness (9/10):** enums/paths/tool names current; hook v2.5 operational-slot (`## Modes`); the AC0-corrected verdict enum; PF citations resolve in current process-failures.md.

**Operational-slot section:** `## Modes` (covers probe-generation + deploy-block-verdict + sequential-execution per §16 INV-ROLE-INLINING row). This is the 9th-section synonym the hook requires (parity with Role 3).

**Hard safety binaries that MUST survive any trim (Rule 7):** H1/H2 auto-block non-overridable; severity_proposed-only (never severity_final by reviewer); deploy_verdict canonical 3-enum; default-to-BLOCK; maintain-verdict-under-pushback-without-evidence; coverage-pass≠deploy-verdict; re-dispatch-on-ancestry-drift; probe-freshness; operator-profile-as-audit-not-probe-input.
