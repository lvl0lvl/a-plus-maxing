# /upgrade-agent Phase 7 — Final Corrections (genetics-specialist)

Phase-6 adversarial review (`phase6-adversarial-review.md`) returned **DEPLOY-READY**: 0 Critical / 0 Major / 6 Minor / 3 Nitpick, all four Phase-3 red-team safety fixes PRESENT, all 6 PF ids + 8 refusal-class IDs + all `vault/`/`templates/` references resolved, live audit 0-BLOCK. No must-fix.

## Corrections applied to `.claude/agents/genetics-specialist/agent.md` (Phase 7)

| Finding | Severity | Applied |
|---|---|---|
| AR-004 | Minor | Added the composite-precedence clause to Core Rule 3: a finding that is BOTH unconfirmed-raw AND EMERGENCY-gene-class escalates `TIME_CRITICAL` first, carrying the unconfirmed-provenance flag — escalation not deferred pending confirmation. (Highest safety value: resolves the DTC-first vs EMERGENCY-first tie-break for the EC-11 composite.) |
| AR-005 | Minor | Core Rule 3 "facilitates referral" → "surfaces the referral recommendation and routes the disease-risk surface via the live `medical-liaison`" — ties the verb to the documented routing channel. |
| AR-001 | Minor | Context-Loading step 3 + Modes empty-state: "if `dna/raw` is empty" → "empty or absent" (the dir does not exist in the worktree; a missing-path read is fail-safe but now explicitly covered). |
| AR-007 | Nitpick | Tools: dropped the maintenance-fragile superlative "— the strictest research floor in the roster"; the `--mode=deep --target-class=reference` floor carries the behavior. |

## Routed to integrator (not applied here)

- **AR-003 (Minor, design-doc-side):** the design doc §5 preamble says "the four substrate safety floors are rules 1–4" which disagrees with §15.2 AC-2 (the privacy/exceptionalism floor is deployed as rule 10). The **deployed agent.md is already correct** (it omits the brittle numbering claim; all four floors are present as Core Rules r1/r2/r4/r10, each audited). Because `design/genetics-specialist-design.md` is Status:Final, the PROTOCOL DO-NOT forbids inline-editing it to fix a defect → routed to the integrator as a beads-to-create item (see outbox). Zero functional impact.
- **AR-009 / OQ-3 (Nitpick, integrator-side):** the `genetics-specialist` row in `templates/specialist-risk-class.yaml` is absent from the worktree base but present in main (deep/reference); the integrator confirms at rebase-merge. The in-profile prose dispatch floor (Core Rule 11 + Tools) is the standalone defense.

## Final consistency check (/upgrade-agent Phase 7)

- All 11 AGENT_TEMPLATE sections present; `## Modes` operational slot present. ✓
- Line count 170 (≤200 ceiling). ✓ Token 8673 cl100k (WARN-only documented medical overrun per Rule 7 / bead 2qq; the ≤200-line ceiling is the BLOCK and is met). 
- `library-index.md` 9 lines, ≥1 `vault/library/` conditional ref, paths resolve. ✓
- IDENTICAL block sha256 = `35dbda2fb9d99540aa7a1487f764c44b1553cfab33d13eb2015e0f4bd390b6f1` (byte-identical to deployed cardiovascular/labs siblings). ✓
- Anti-sycophancy in first 20 lines (IDENTICAL block L5–7); Negative Examples in last ~45 lines (recency). ✓
- `audit-specialist-profile.sh` (the mechanical fact-checker): **0 violation(s) / EXIT=0** (re-run post-correction). ✓
- Operational completeness: every verb maps to a tool/workflow (AR-005 closed the one "facilitate referral" indirection). ✓

**Deploy state: agent.md + library-index.md DEPLOYED, audit 0-BLOCK, adversarial DEPLOY-READY, Phase-7 corrections applied and re-audited clean.**
