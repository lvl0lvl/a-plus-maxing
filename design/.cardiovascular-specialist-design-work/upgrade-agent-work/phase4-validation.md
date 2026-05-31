# /upgrade-agent Phase 4 — Validation (cardiovascular-specialist agent.md)

Separate + parallel fresh agents per /upgrade-agent Hard Rules (fact-checker VERIFIES, judge SCORES; never self-score). Gate: artifact passes ONLY if fact-checker all-pass AND judge ≥9 on every dimension.

## Phase 5 authoring (health-implementer / Role 2, Mode:Authoring, full profile inlined)
- Output: `.claude/agents/cardiovascular-specialist/agent.md` (177 lines) + `library-index.md` (9 lines), NO YAML frontmatter.
- Self-audit (Core Rule 9): `scripts/audit-specialist-profile.sh` EXIT 0, 0 BLOCK, 1 WARN (token-density, documented WARN-not-BLOCK per bead 2qq — consistent with all 14 deployed specialists; the ≤200-line ceiling is the BLOCK and passes at 177). One BLOCK caught + fixed in-loop (Identity 42→40→29 words).
- IDENTICAL block sha256 = `35dbda2fb9d99540…` — byte-identical to lymphatic-specialist + endocrine-specialist (the canonical SHA-matched form; NOT gi's GI-tailed divergent variant).

## Phase 4 fact-checker (FRESH, parallel) — VERDICT: all_pass: true (12/12)
1 testable Core Rules (12/12 Mechanical Checks) · 2 every not-own names owner · 3 anti-patterns concrete + source + cue · 4 library-index paths resolve (advisory: `vault/library/cardiovascular/` was a dangling forward-pointer → FIXED Phase 7 AR-001) · 5 tools real · 6 line ≤200 (177); token WARN-not-BLOCK · 7 operational completeness: 0 gaps · 8 ≥4 refusal classes incl AUTHORITY_FRAMING_BYPASS + TIME_CRITICAL, none invented · 9 6 distinct PF ids resolve · 10 mode-floor standard/compound, no bare deep-research · 11 design-doc fidelity (TIME_CRITICAL floor, no-compounds-write, bromism CV-SF-05, content-trigger CV-SF-06) no drift · 12 IDENTICAL sentinel + A/B/C. Audit exit 0.

## Phase 4 quality judge (FRESH, parallel) — VERDICT: all_dimensions ≥9: true
Per-dimension: Identity Clarity 10 · Context Efficiency 9 · Behavioral Specificity 10 · Reference Integration 9 · Boundary Enforcement 10 · Communication Protocol 10 · Failure Recovery 10 · Tool Awareness 9 · Anti-Pattern Coverage 10 · Freshness 9. No remediation required. The 5 highest-safety-weight clauses (cardiac floor, causal-vs-associational, Rx name-and-route, device-screening, bromism-class) all judged concrete + testable + role-fit (not generic).

## Phase 6 adversarial review (`/adversarial-review` document version) — VERDICT: APPROVE-WITH-NITS
0 CRITICAL · 0 HIGH · 1 MEDIUM · 4 LOW · 2 NITPICK (full report: `phase6-adversarial-review.md`).
- AR-001 (MEDIUM, library-index dangling `vault/library/cardiovascular/`) → FIXED Phase 7 (folded grounding into the `_source-whitelist.md` bullet; removed the non-existent standalone path).
- AR-002 (LOW, no dedicated IMAGE/DEVICE BAD/GOOD pair) → ADDRESSED Phase 7 (Negative Example 1 GOOD now names the pasted-ECG `IMAGE_OR_SIGNAL_INPUT` non-interpretation; budget held at 4 pairs).
- AR-003 (LOW, "IDENTICAL" label vs gi) → premise corrected: the block IS byte-identical to the canonical lymphatic+endocrine form (gi is the documented outlier); the invariant holds. No fix.
- AR-004/006/007 (NITPICK/LOW compression) → ACCEPTED load-bearing, within the 177-line/≤200 budget.
- AR-005 (LOW, `vault/parameters/` not-yet-existing) → already mitigated by the Modes empty-state path.

## Phase 7 final consistency check
Re-run after edits: audit EXIT 0, 0 violations; 177 lines (≤200); IDENTICAL sha still `35dbda2fb9d99540…` == lymphatic; all AGENT_TEMPLATE sections present (11); anti-sycophancy in first 20 lines (L6); Negative Examples in the last section (BAD/GOOD pairs to EOF). All adversarial findings dispositioned.
