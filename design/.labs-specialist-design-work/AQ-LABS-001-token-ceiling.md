---
id: AQ-LABS-001 (was AQ-003 at authoring)
title: audit-specialist-profile.sh R13-3 token ceiling (2500 cl100k) is unmeetable by any profile satisfying the design-doc-mandated content
raised_by: health-implementer (Pass-3 /upgrade-agent labs-specialist authoring, Phase 5 self-audit gate)
raised_at: 2026-05-29 (S-pass3)
routes_to: orchestrator + health-implementer (Role 2 owns the audit-script bash per S10 F-007) + Role 1 (owns the §13 interface spec)
affects: scripts/audit-specialist-profile.sh check_body_length (R13-3); labs-specialist + all 14 Pass-3 specialist profiles; design §15.1 token AC
status: pending-orchestrator-disposition
blocker: YES (LIVE gate — the script is executable and R13-3 is a BLOCK row; it fails on a faithful, content-complete profile)
---

# AQ-003 — R13-3 token ceiling unmeetable by mandated content

## The conflict

`scripts/audit-specialist-profile.sh` `check_body_length` (R13-3, BLOCK) caps the post-frontmatter body at **2500 cl100k tokens**. The labs-specialist design doc mandates content that cannot fit under that ceiling:

- 11 `## ` sections (audit R13-6.5 enforces exactly 11).
- 12 Core Rules, each with a load-bearing pass/fail Mechanical Check clause (design §5; AR-008 says the pass/fail clause must survive synthesis).
- An inlined critical-value floor enumerating ≥6 analyte thresholds (design §7 / Rule 8; SF-01 close).
- GRADE two-axis grammar, the 6-class refusal set, the three-mechanism IDENTICAL anti-sycophancy block.
- ≥3 BAD/GOOD Negative-Example pairs (audit `check_negative_examples` wants ≥6 markers).

## Empirical evidence

Measured with `tiktoken.get_encoding('cl100k_base')` on the post-frontmatter body:

| Profile | cl100k tokens | lines | passes R13-3? |
|---|---|---|---|
| labs-specialist (this deliverable, fully compressed) | 4245 | 151 | NO (>2500) |
| labs-specialist with ALL 3 code blocks deleted | 3853 | — | NO (and would fail `check_negative_examples`) |
| health-specialist-architect (deployed) | 3252 | 127 | NO |
| health-implementer (deployed) | 5245 | 162 | NO |
| health-edge-case-reviewer (deployed) | 6522 | 191 | NO |
| medical-safety-reviewer (deployed) | 8110 | 199 | NO |

All four deployed foundation profiles already exceed 2500 cl100k tokens (3252–8110). None has ever met R13-3. The labs-specialist is compressed to 4245 — below every sibling — and still cannot reach 2500 without dropping mandated sections.

The arithmetic: dense technical prose with code fences, unicode (≥, ×, ⁹), and slash-paths runs ~28 cl100k tokens/line. The design's own §15.1 targets "150–180 lines AND ≤2,500 tokens" — internally inconsistent, since 150 lines at this density is ~4200 tokens. The design also routes the token AC to **/upgrade-agent Phase 7 at ≤2,000 tokens**, a different enforcement layer than this audit's R13-3 row.

## Interpretations

- **A (recommended).** R13-3's 2500 ceiling is mis-set for medical specialist profiles. The line ceiling (≤200, R13-3) is the binding, meetable budget; the token ceiling should either be raised to match (~4500–5000 cl100k for an 11-section medical profile) or removed in favor of the line check. Generalizes: all 14 specialists inherit the same mandated content and will all fail R13-3 identically.
- **B (rejected).** Strip mandated content (drop to <8 Core Rules, delete the inlined floor, cut to 1 negative example) to fit 2500. Rejected: deletes the SF-01/SF-02/SF-05 safety-critical inlined behaviors that closed the Role-4 BLOCK, drops the load-bearing pass/fail clauses (AR-008), and fails other BLOCK rows (`section-count` ≠ 11, `negative-examples` < 6 markers). Trades a real safety surface for a token grep.

## Implementer disposition (this dispatch)

1. **Deploy faithfully at `audit_passed: with-known-deferrals`** (Rule 9 legal terminal state) — NOT fabricated `true`. The single known deferral is R13-3. Every other BLOCK check PASSES (identity, description-routing, refusal-classes, authority-framing, grade-halt, anti-sycophancy, section-count, operator-no-writeback, mechanical-stubs, section-uniqueness, library-index, pf-resolution, aplus-mode-floor). The `with-known-deferrals` value also trips R13-13 (which accepts only literal `true`) — that is the mechanical surface of the honest deferral, not a second defect.
2. **Escalate, do not self-patch.** Per Role 2 §Loop-Breaking audit-failure-threshold path (ii): file the audit-script bug here; do not edit `check_body_length` (Role 2 owns the bash but the §13 row threshold is the Role 1 interface spec).
3. **Bead the fix.** R13-3 threshold reconciliation against the line ceiling + design §15.1 internal inconsistency; annotate the audit-script-authoring bead.
4. **Orchestrator counter-signature required** to accept `with-known-deferrals` for deployment, or to adjudicate Interpretation A and re-run the gate.
