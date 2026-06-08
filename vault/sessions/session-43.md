---
title: Session 43 — residual-bead PII/safety hardening (Track 1)
type: note
status: active
owner: walter
created: 2026-06-08
permalink: a-plus-maxing/sessions/session-43
---

# Session 43 (2026-06-07→08) — residual-bead cleanup, Track-1 PII/safety boundary

## Unit
First post-V1-build residual-bead session. Goal: fix open beads in least-reversible-risk priority order — Track 1 (PII/safety boundary) first, then Track 2 (V1 correctness). Each its own short-lived `fix/` branch → FULL `/review-pr` → `/merge`. Track 1's shippable parts landed; Track 2 not reached (session length).

## Merged (2 reviewed PRs, 4 beads closed)
- **PR #75 (PR-1a) — runtime PII guards.** `8j6` (P1): the in-summary PII gate. The 7 non-derived pass-through summary fields were read VERBATIM in `router.summarize`'s else-branch → raw PII in a free-text field (goal-targets/hard-limits) reached BOTH the model sink (via `dispatch`) and the render sink (via `assemble`). Fix placed the fail-closed gate IN `summarize` — the single point covering both sinks (the defined 0-raw-PII boundary) — via a new `pii_scan.scan_text`. `2x1`: `pii_scan` contact + identity patterns compiled `re.IGNORECASE` (`Op.User@Gmail.COM` now hits). `fga`: runtime scalar gate in `dispatch` (positive allowlist — None/str/int/float/bool; rejects bytes/containers). Option (a) closed-vocab store schema REJECTED (touches `keying`).
- **PR #76 (PR-1b) — `cvr` shared git-commit matcher.** Hardened the matcher IDENTICALLY across all 3 commit hooks (block-pii-commit / block-commit-main / block-ungated-vault-write) to catch env-var-prefix / path-prefix / trailing-separator forms; the review then closed two PRE-EXISTING bypasses (leading-whitespace, embedded-newline) via NORM hardening (`tr '\n' ';'` + strip). Empirically validated; bypass tests added to all 3 harnesses (25/30/14 green).

## Review — the layered `/review-pr` earned its keep on BOTH PRs (7th + 8th consecutive)
Both ran the FULL 6-agent `/review-pr` + dispatched profile-less Phase-3 blind triage + Phase-7 blind verify (PF-S40-01 + PF-S39-01 HELD ×2; 0 suppressed, PF-S26-01).
- #75 caught a **P1 PII detection-vocabulary gap**: the gate catches gmail + operator-name but NOT phone/postal/non-gmail email per `EXCLUDED_RAW_PII` → beaded `g5x` (a cross-cutting scanner-vocabulary redesign, not the `8j6` "integrate pii_scan" scope). Blind-verified 6/6 legit fixes.
- #76 caught **two PRE-EXISTING PII-distribution bypasses** (leading-whitespace, embedded-newline in the matcher) + a stale security comment the builder's green tests missed. Blind triage: 6 fix-now / 3 bead / 4 not-a-bug. Blind-verified 6/6.

## Deferred for cause (NOT shipped)
- **`3lv` (register the PII commit hook):** dry-running the about-to-be-registered hook DENIED with 14 hits — its generic-`@gmail.com` agnostic scan runs TRUNK-WIDE and flags LEGITIMATE content (the scanner's own test fixtures + the auto-staged `.beads/issues.jsonl`). Registering as-designed is **clone-hostile + workflow-breaking**. Root: the generic `@gmail.com` pattern is the wrong tool for a trunk-wide scan — the operator's real contact should be detected like the operator NAME (operator-specific, config-driven, gitignored, data-bearing-scoped). DEFERRED to that redesign (folds with `g5x`). `settings.json` registration edited then REVERTED — no net governance-config change.
- **`10h`:** verified against `assemble._halt_disposition` — catching a present-but-wrong category needs a compound→class registry assemble has no access to. Genuinely beyond V1's trust model. Kept open, documented.

## Beads filed (open follow-ups)
`g5x` P1 (pii_scan detection vocabulary), `7zj` P2 (`settings.json` hardcodes absolute hook paths → **all hooks inert on a clone** — gates alpha-testers; fix via `$CLAUDE_PROJECT_DIR`), `mic` P2 (extract the shared commit matcher to `.claude/hooks/lib/`), `5i2` P3 (matcher over-matches `git log --grep commit`), `bie` P3 (INVARIANTS smoke-test counts).

## PF / falsification windows
**No new PF.** PF-S40-01, PF-S39-01, PF-S26-01, PF-S25-01, PF-S6-01, PF-S37-01, PF-S13-01 all HELD (detail in HANDOFF S43 PF attestation). Notable: PF-S6-01 (verify-first) was load-bearing — the `3lv` blocker was found by DRY-RUNNING the hook (not assumed), and an `rg -r <replacement>` display-mangle that looked like a broken test was caught by reading the actual file. The auto-mode classifier twice gated authorized hook edits (a harness-permission interaction, handled by revert + re-confirm) — not a PF.

## State after S43
`main` at the PR #76 merge (`62cda05`) + the S43 close PR. V1 build COMPLETE (18/18), PII/safety boundary partially hardened. Suite 285/2; shell hook suites 25/30/14; branch-completeness 0. Forward (S44): finish Track 1 (`g5x`+`3lv` redesign, `7zj`, `mic`, `dv3`, `rnm`) before LM-04 real data; then Track 2 (V1 correctness: `s38`+`byj`, `5q5`, etc.); LM-04 + library track. [[sessions/session-42]]
