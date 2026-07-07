---
title: Session 115 — SEC-01 sk-ant-api no-train-key secret scan (merged) + PF-S115-01
type: session
date: 2026-07-07
status: complete
permalink: a-plus-maxing/sessions/session-115
---

# Session 115 — block the no-train API key at commit (SEC-01, merged)

Passed THROUGH the S114 close into the highest-value follow-up from the aque review — the SEC-01 sibling (`n23r`). Built + merged (PR #306, `de12defa`): a leaked no-train API key (`sk-ant-api…` shape — the `a-plus-maxing-api-key` keychain item read by the de-id `ModelClient`, a live METERED-SPEND credential) is now BLOCKED at commit + pre-push in this PUBLIC repo, closing the sibling of ADR-0027's aspirational assurance.

## What was built
- **The sibling secret pattern** (`cf042bbc`): a 2nd `pii_scan.SECRET_PATTERNS` entry `"no-train-api-key"` (matching the `sk-ant-api…` shape), applied by the same unconditional `scan()` path aque added, so `scan_scoped` (the single policy both PII hooks run) blocks the key trunk-wide. The aque anti-overbroad test was **RECONCILED** — its `sk-ant-api` near-miss became a real match once the pattern was added (the "update related tests when behavior changes" mandate), so it was changed to a genuinely-non-matching prefix, covers both prefixes, and carries a `>= 2` two-class liveness assert. A new api detection test; the token fragment-assembled (0 self-trips).
- **The coupled ADR amendments:** append-only `[AMENDED 2026-07-07 (SEC-01)]` notes on ADR-0027 + ADR-0005 correcting the aspirational no-train-KEY at-commit-denial assurance — precisely: the raw-PII-residue clause was ALWAYS true (operator-PII detection), only the KEY clause was aspirational (no secret detection until aque/SEC-01).

## PF-S115-01 — the scan-tripping-literal class recurred twice, both gate-caught
Building this, two scan-tripping literals I authored were caught by GATES rather than my proactive self-check:
- The SEC-01 bead description carried a `sk-ant-api…`-shaped EXAMPLE literal that would self-trip the very pattern I was adding — caught by the build's **entry-state token scan** (mirroring the aque precondition), elided before adding the pattern.
- The first-draft `SECRET_PATTERNS` key NAME embedded a provider-SDK token, putting it into `scripts/guard/pii_scan.py` and tripping two crown-jewel serve/ingest egress guards — caught by the **full-suite regression** (2 new failures past the floor), fixed by renaming to `"no-train-api-key"` + rewording the comment.

Root cause: my in-build self-check grepped the SECRET shapes I was adding but not the egress-forbidden provider set, and I did not pre-scan bead descriptions. Lesson (PF-S115-01): on any tracked-file write during secret/egress work, proactively grep the FULL forbidden set (secret shapes + the provider set for `scripts/` files) BEFORE commit. Both gate-caught, no defect shipped.

## The /review-pr — the blind triage earned its keep
The REAL Tier-3 `Skill(review-pr, 306)` ran IN FULL (roster full-6). 3 findings, 0 Critical:
- **QUAL-01** (Code Quality) — the MODULE docstring named only the OAuth token after `SECRET_PATTERNS` gained the sibling (I updated the inline comment, not the docstring — the same "update one doc surface, miss another" class as aque's API-01). LEGITIMATE → fixed + blind-verified RESOLVED (names both, egress-clean).
- **TEST-01** (Test Coverage) — no `scan_scoped`-level api test. Blind-triaged **NOT_A_BUG**: the triage EXECUTED `scan_scoped` on a synthetic api key → already blocked, and the existing `include_structural=False` assert IS the fixture-partition call → the mirror closes no live gap. Beaded P3 optional-symmetry.
- **API-01** (Contracts, conflicting with a Historical suppressed note) — no ADR Revision-History row for the SEC-01 amendment. Blind-triaged **NOT_A_BUG**: the triage EXECUTED `git show ca2669ac` → the aque revision row accompanied a BODY change; table-row `[AMENDED]` edits get none, so SEC-01 is precedent-consistent — and adding one would have been INCONSISTENT with the aque precedent I nearly introduced.

The blind triage disproving two reviewer findings with executed evidence is the independence guarantee working: it caught that my inclination to "just add the revision row" would have introduced an inconsistency. Security/Bug-Hunter/Historical-Context 0-findings (all executed: ReDoS timing, disjoint-pattern regex, egress-clean grep, secrets-only 2733-file tree scan = 0). One informational sk-ant-admin completeness scope-note beaded P3 (dormant — no admin key exists).

Frozen ADR-0032 spine + `plan_loop.py` byte-frozen (numstat=0 — `pii_scan.py` is guard-layer); crown-jewel net-HARDENED (both Anthropic credential shapes the repo holds are now blocked at commit); 0 live spend.

Full detail: `memory/process-failures.md#session-115` + HANDOFF `## Scope Contract — Session 115`.
