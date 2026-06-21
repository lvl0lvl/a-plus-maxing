---
title: Session 84 — independent re-review of the S83 ingestion-on-ramp merge (bead 9qx5)
type: session
date: 2026-06-21
owner: Walter McGivney
status: complete
---

# Session 84 — independent PR-#205 re-review (the S83 remediation)

**Goal:** Execute the operator's standing P1 directive (bead `9qx5`): run the PR-#205 `/review-pr` independence phases that S83 collapsed under context pressure — a profile-less BLIND TRIAGE (review Phase 3) + a profile-less EXECUTED BLIND VERIFY (Phase 7) against merged `main` — in a FRESH session, then fix-forward or bead anything they surface.

**Why this session exists:** S83 ran PR #205's six review agents properly but ran the post-Phase-1 independence steps (blind triage / SE fix / blind verify) DIRECTLY, and applied `/merge` as methodology — a DISCLOSED INV-SKILL-TRACE deviation forced by an exceptionally long single conversation (an S82 close + a full PR-#199 review + the whole build). The operator directed the independent passes be run "first thing in a fresh session." This is that session.

**Outcome:** The S83 ingestion-on-ramp merge is **independently confirmed sound.** No product code changed; no new escaped defect. `9qx5` closed; `dw8u` sharpened. `main` unchanged at `8b52019` save this docs-only close.

## How it ran (the independence restored)

Two profile-less general-purpose agents (opus), each in its **own** clean worktree off `origin/main` @ `8b52019` (baseline 1182 passed / 3 skipped), with **no access** to the S83 verdicts or the fix diffs:

- **Blind triage (read-only)** — classified each PR-#205 finding cluster against the merged source, grounded in file:line it personally read, re-verifying rather than trusting commit `7376a53`.
- **Executed blind verify (mutate-and-revert, isolated worktree)** — RAN the behavior behind each claimed fix and reported RESOLVED / STILL_PRESENT with executed evidence; restored the tree clean afterward.

## Findings (both passes converged)

| finding | triage verdict | executed verify |
|---|---|---|
| TEST-001 (`--source` test tautological) | RESOLVED | non-vacuous — RED under a mutation that ignores `--source` (`.json` auto-detect refuses) |
| QUAL-1/API-205-01/HIST-1 (CLI/status ↔ scheduler source-set drift) | RESOLVED | congruence test fails LOUD both ways (bogus-add + UNWIRED-flip) |
| QUAL-2/API-205-03 (private `_wearable` reach) | RESOLVED | `status.wearable_status` public + correct; no cross-module private reach |
| API-205-02/HIST-3 (docstring omits `'intake'`) | RESOLVED | docstring lists `'intake'`; `generate.run('intake')` renders 12 KB self-contained HTML |
| SEC-205-01 (decompression bomb) | DEFERRED-OK (`07f6`, operator sign-off) | STILL_PRESENT by design — no cap; 357 KB member copies in full (deferral legitimately open) |
| HIST-2 (whoop UNWIRED) | NOT_A_BUG (whoop is wired; reviewer misread docstring) | n/a — whoop in the wired set, congruence test passes |
| BUG-205-01 (`_dropzone` exists vs is_dir) | NOT_A_BUG-as-framed / DEFERRED-OK (`dw8u`) | raises `NotADirectoryError` (loud crash), NOT a silent misclassification |
| TEST-003/004/005, QUAL-3/4/5 | LEGIT-minor → DEFERRED-OK (`gzf7`/`dw8u`) | confirmed real-minor; no current bug |

Plus: zip-slip neutralized (a `../../../../tmp/…` member lands as basename inside the dropzone — escape target False); the full ingest+render path runs with **sockets blocked** (model-free + network-free confirmed by execution); the egress-guard suite green.

## Disposition

No divergence from the S83 dispositions, so **no fix-forward** in the product tree (the correctly-deferred minors stay beaded — per the audit-surfaced-fixes-are-exceptions discipline). `dw8u` sharpened with the executed BUG-205-01 repro (the `NotADirectoryError` crash path + the one-line `exists()`→`is_dir()` fix + the low-realism caveat). `9qx5` closed with the full evidence.

**One operator decision teed up:** SEC-205-01 / bead `07f6` — the DNA-export decompression cap is defensive programming (operator owns the file; lands locally), so it needs a binary sign-off: ADD the streamed byte-cap or ACCEPT the self-DoS risk and close won't-fix.

## Lesson (applied, not just logged)

The S83 recurrence-watch — *prefer a fresh conversation per work-unit* — was the remedy, and this session IS that remedy run. The collapse happened because one conversation tried to hold an S82 close + a PR review + a full build + a merge; the fix is to stop and resume fresh rather than collapse the sub-agent shape. Restored here: independent profile-less triage + executed verify, each in isolation.
