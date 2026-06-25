---
title: Session 96 — landed 8d8r (the SEC-1 de-id value-scan); the live run's value-defense is in place
type: session
date: 2026-06-25
owner: Walter McGivney
status: complete
permalink: a-plus-maxing/sessions/session-96
---

# Session 96 — the de-id value-scan (8d8r), pre-live-run hardening

**Shape:** a focused single-bead follow-up to the S95 live-wiring completion (operator-directed: "land 8d8r so the live run is fully unblocked"). TDD + a proportionate 2-lens adversarial review + merge. Mock/fixture-tested (0 live spend). The ONLY remaining step is the operator-present LIVE run.

## What was done

**8d8r — the de-id value-scan (SEC-1), merged PR #252 → `main` `f926596`.** `deid_in` (the model-backed de-id-IN boundary, the SOLE raw-PII egress on the plan path) enforced a KEY-NAME whitelist only (`set(summary) ⊆ SUMMARY_FIELD_SET`); a faithless/degraded no-train model could pass the whitelist yet echo raw operator PII into an allowed field's VALUE — which reaches the subscription specialists + the render (`deid_in` is the SOLE value-defense on the orchestrated path; it does NOT route through `router.dispatch`'s scalar gate). The fix adds a value-level scan after the whitelist: each value is scanned with the NON-TRUNCATING `pii_scan.scan_text_full` (mirrors `router.summarize`'s 8j6 gate but avoids the capped-`scan_text` straddle hole, bead `sc97`); any hit fails closed to a distinct `DEID_VALUE_PII` sentinel. 4 new tests (identity-PII, contact-PII-without-config, sc97-past-the-cap, clean-passes), mutation-verified non-vacuous. EXTEND-NOT-REBUILD: only `deid_in.py` + its test. Suite 1674/2.

## The review (the headline: the adversarial lens found real residuals)

A proportionate 2-lens adversarial review for the ~12-line crown-jewel diff (full profiles, executed — the 6-agent `/review-pr` pipeline is overkill for a tiny diff per the skill's own guidance):
- **Bug-Hunter: 0 bugs.** Fail-closed tightening; all value types handled (`str()` flattens containers for scanning); the single production caller composes (the new `identity_config` default keeps the 2-positional call valid); tests non-vacuous (mutation: 3/4 RED without the loop; the sc97 test REDs if `scan_text` replaces `scan_text_full`).
- **Security: ISSUES (not BLOCK).** Strictly safer than main; closes the dominant string-PII vector in any container nesting. Surfaced two PRE-EXISTING `pii_scan` recall residuals now load-bearing on this path: (a) numeric-typed identifiers (a phone/MRN/lab as a bare JSON number / 7+-digit run, which the text-regex value patterns miss) and (b) a two-line `\n`-split postal address (the postal regex is `[^\n]`-confined). Both **beaded** + surfaced as the operator's explicit pre-real-PII decision. The docstring's overstated "PII inside a container is caught too" claim was corrected honestly.

The disciplined response held the no-unapproved-defensive-programming rule: the obvious "fix" (a digit-run guard for the numeric residual) is defensive programming that needs operator sign-off, so it was beaded + surfaced, not bolted on unilaterally.

## State at close

- pytest **1674 passed / 2 skipped** on `main` `f926596`; EXTEND-NOT-REBUILD held. The de-id-IN crown-jewel boundary is strictly stronger.
- **No new PF.** Observed-but-not-promoted: the `/review-pr` skill was not invoked for #252 (a proportionate direct 2-lens review instead, sanctioned for a tiny diff; recorded honestly NO in the skill-trace table).
- Beads: closed `8d8r`; created the de-id-value-scan-residuals bead (P1, pre-real-PII). Carry: `stsq` (SEC-3 release gate), `zsp5`, `f0gh`.

## Next

The operator-present LIVE end-to-end run — `/generate-plan` over a PII-free SYNTHETIC summary first (real dispatch + real de-id spend, 0 real PII), then real data; the operator injects the no-train key. Before REAL PII: decide the 2 value-scan residuals (the residuals bead). The synthetic-first run is unaffected.
