---
title: Session 44 — Track-1 PII/safety hardening + clone-distribution (4 reviewed PRs)
type: note
status: active
owner: walter
created: 2026-06-09
permalink: a-plus-maxing/sessions/session-44
---

# Session 44 (2026-06-08→09) — Track-1 PII/safety + clone-distribution

## Unit
Second post-V1-build residual-bead session. Continued Track 1 (PII/safety) in least-reversible-risk priority order: the actionable P1 (`g5x`) + the Track-1 distribution items (`7zj`/`mic`/`rnm`), each its own short-lived `fix/` branch → FULL `/review-pr` → `/merge`. `dv3` deferred (infra decision); `3lv` stays blocked. Hook/settings editing was authorized this session.

## Merged (4 reviewed PRs, 4 beads closed)
- **PR #78 (`g5x`, P1) — runtime value-boundary PII detection.** Widened `pii_scan.scan_text` (the `router.summarize` value boundary; 8j6's gate) from gmail-only to non-gmail/generic email (+ googlemail), phone (E.164 + NANP), and an NFKC compatibility-homograph fold; asserted through `summarize` (both sinks). The review caught a **ReDoS** in the value scanner (the blind triage empirically REFUTED the security agent's anchored-domain fix — the input cap, not anchoring, was the real fix) and a **postal fail-close on legit Title-case health text** ("Dr Patel followup"). **Postal DROPPED** as net-harmful → bead `nue`; AC1 CHANGED, Walter blessed. `scan` (trunk) stays gmail-conservative (a guard test pins it).
- **PR #79 (`7zj`, P2) — governance-hook clone-portability.** `.claude/settings.json` registered all 5 PreToolUse hooks with absolute author-home paths → INERT on any clone. Switched to `${CLAUDE_PROJECT_DIR}/.claude/hooks/<hook>.sh` (claude-code-guide confirmed the documented placeholder + hooks hot-reload). **Verified live this session** (block-dangerous fired on the new path — a destructive dry-run denied). New `scripts/tests/test_settings_hook_paths.sh`.
- **PR #80 (`mic`, P2) — single-source the commit matcher.** The matcher regex + NORM were triplicated byte-identically across block-pii-commit / block-commit-main / block-ungated-vault-write. Extracted to a sourced `.claude/hooks/lib/commit-matcher.sh` (`is_git_commit`); the 3 hooks source it. Behavior-preserving (the 3 suites stayed 25/30/14). **The review caught a real FAIL-OPEN security regression the refactor introduced** — a `source lib` dependency under `set -uo pipefail` (no `set -e`) meant a missing/corrupt lib left `is_git_commit` undefined → `|| exit 0` → the fail-CLOSED PII hook silently skipped its scan. Fixed: block-pii-commit denies on a missing lib (fail-closed); the two annoyance guards loud-allow. The session's biggest catch (3 agents + blind triage).
- **PR #81 (`rnm`, P2) — pin the scaffold-value path (docs).** Pinned `vault/scaffold/filled/` as the filled-scaffold-value convention in ADR-0005 (the `.gitignore` + `block-pii-commit` SCAFFOLD_PREFIX + test fixtures all key off it; verified `init_instance` writes no value, so it's a forward convention). 3-agent docs review added the v1.4 Revision-History row + a dated cue resolving a stale-enforcement-bullet contradiction.

## Review — the layered `/review-pr` earned its keep on ALL 4 PRs (9th-12th consecutive)
Each ran the FULL methodology (6-agent, or the 3-agent docs subset for #81) + dispatched profile-less Phase-3 blind triage + Phase-7 blind verify (PF-S40-01 + PF-S39-01 HELD ×4; 0 suppressed, PF-S26-01). Notable: the #80 fail-open was a regression the orchestrator INTRODUCED in a "behavior-preserving" refactor — caught because the orchestrator proactively flagged the failure-posture question to the review AND the independent blind triage confirmed it. The mechanism held (every defect caught before `main`).

## Deferred / blocked / split
- **`dv3` (P3) DEFERRED** — the non-agent push backstop needs a mechanism decision (pre-push git hook, local-first fit but needs a clone-init install step, vs a `.github/workflows` CI check, auto-active but introduces hosted CI to a deliberately CI-less repo). Surfaced to Walter; he chose to close S44. Lean pre-push.
- **`3lv` (P2) BLOCKED** on `nue` — registering `block-pii-commit.sh` stays clone-hostile until the operator-specific contact-detection redesign lands.
- **Beads filed:** `nue` P2 (postal + operator-specific contact detection), `am4` P2 (ADR-0005 freshness sweep), `21o`/`70j`/`f12`/`qkb` P3.

## PF / falsification windows
**No new PF.** PF-S40-01 / PF-S39-01 / PF-S26-01 / PF-S25-01 / PF-S6-01 / PF-S37-01 / PF-S13-01 all HELD. PF-S6-01 (verify-first) was load-bearing repeatedly: `7zj`'s `${CLAUDE_PROJECT_DIR}` verified via claude-code-guide + a live-fire before trusting it; `rnm`'s path + no-competing-producer verified before pinning; `mic`'s byte-identical extraction verified. **Observed, NOT promoted:** the mic fail-open (caught by the process, not escaped); `block-dangerous` false-matched twice on dangerous-command literals in command strings (recovered, a documented gotcha); the rate-limit interruption (external, cost nothing — the lost blind-triage dispatch re-issued); the S43 close's stale-S42 HANDOFF accrual (cleaned at this close).

## State after S44
`main` at the 4 work merges + the S44 close PR. V1 build COMPLETE (18/18); PII/safety boundary hardened (runtime value-scan widened) AND clone-distributable (governance hooks portable, commit matcher single-sourced, scaffold convention pinned). Suite 310/2; shell suites pii 25 / commit-main 30 / ungated 14 / commit-matcher 30 / settings-hook-paths 12; branch-completeness 0. Forward (S45): finish Track 1 (`nue`+`3lv` redesign, `dv3`, `am4`) before LM-04; then Track 2 (V1 correctness); LM-04 + library track. [[sessions/session-43]]
