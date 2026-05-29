---
id: AQ-002
title: Voice-register audit (AC-deploy-11 / §13 row 4) conflates banned-phrase USE with MENTION
raised_by: orchestrator (S13 /upgrade-agent Role 2 deployment, Phase 3→4 boundary)
raised_at: 2026-05-28 (S13)
routes_to: orchestrator (pre-architect-runtime per Role 1 §18 OQ-2 disposition; design §6 step-2 stored-file channel)
affects: AC-deploy-11; §13 row 4; all 14 downstream specialist profiles
status: orchestrator-disposed (deploy-faithful + bead the audit-spec fix)
blocker: NO (audit script scripts/audit-specialist-profile.sh is PROPOSED/not-yet-built; no live gate fails)
---

# AQ-002 — Voice-register audit conflates USE with MENTION

## The gap

`design/health-implementer-design.md` requires the deployed `health-implementer/agent.md` to simultaneously:

1. **Name** the banned-modal regex to make Core Rule 4 a testable rule (§5 rule 4: "Banned `YOU MUST|NEVER EVER|CRITICAL:|IMPORTANT!|!!+` = 0").
2. **Teach** the anti-pattern (§11.2 AP2 cites the regex; §12.2 Negative Example's BAD block reproduces the literal tokens to illustrate the failure).
3. **Pass** AC-deploy-11 (§15.2b, design L586): `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" .claude/agents/health-implementer/agent.md` **= 0** — a whole-file grep with no code-fence or inline-code exclusion.

(1)+(2) put the literal tokens in the file; (3) forbids them. For a faithful port these are mutually unsatisfiable. The design's §5-rule-4 / §13-row-4 scope guard resolves the *design-doc-vs-deployed* axis (`design/*.md` exempt, `.claude/agents/*/agent.md` not) but NOT the *within-the-deployed-profile* axis.

## Empirical evidence (S13)

- Sibling `.claude/agents/health-specialist-architect/agent.md`: `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b"` = **0** — passes trivially because the architect role has no voice-register rule and never quotes the regex.
- A faithful Role 2 profile would match in **3 sites**: Core Rule 4 regex literal; Anti-Pattern #2 regex literal; §12.2 BAD block. Each is a MENTION (defining/teaching), not a USE (the profile's own voice issuing an aggressive modal).

## Interpretations

- **A (recommended).** AC-deploy-11 / §13 row 4 are defective as written: they conflate use with mention. The fix is a **mention-aware** voice-register audit — strip fenced code blocks (```` ``` ````-delimited) and inline-code backtick spans before grep, OR grep prose lines only. This is design-INTENDED (the design doc's own §13 row 4 contains the regex literal and is considered compliant) and generalizes: every one of the 14 specialists inherits a Core Rule 4 / IDENTICAL block that names the regex, so a mention-aware audit fixes all 14 once.
- **B (rejected).** Mangle the tokens in the deployed profile (spelled-out / middot / lowercased) so a naive whole-file grep passes. Rejected: degrades rule precision, diverges 14 profiles from the design's worked examples, is brittle (re-introduction is trivial), and trades a real teaching surface for a false-positive grep. No safety benefit — the issue is a grep false-positive, not an actual aggressive usage.

## Orchestrator disposition (user authority, pre-architect-runtime)

1. **Deploy faithfully.** The Role 2 profile keeps Core Rule 4 (names the ban), Anti-Pattern #2, and a voice-register Negative Example. Verified: zero aggressive *usages* in the profile's own voice; all banned-token matches are *mentions* inside regex literals or BAD fences.
2. **AC-deploy-11 evaluation:** PASS-on-intent (zero aggressive USAGES). The naive whole-file grep would false-positive on MENTIONS; resolution is the mention-aware audit below. Reported honestly at Phase 8 — not a silent pass.
3. **Bead the fix.** `scripts/audit-specialist-profile.sh` `--check voice-register` (and the AC-deploy-11 command) MUST be mention-aware. Annotate bead `a-plus-maxing-3y6` (audit-script authoring) with this requirement. Until the script ships, no live gate runs, so this is non-blocking.
4. **Role 1 spec note.** The AC-deploy-11 command text in the Role 1-owned audit-spec lineage needs amendment to the mention-aware form. This is a §4-OUTBOUND-adjacent edit; surfaced here for the architect's deployment (Role 1 is already deployed — route at next Role-1-spec touch) and flagged to the user at review-pr.
