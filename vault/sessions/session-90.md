---
title: Session 90 — conversational-intake Wave A (model boundary + conversation path) built + merged
type: session
date: 2026-06-22
owner: Walter McGivney
status: complete
---

# Session 90 — conversational-intake Wave A (autonomous build loop)

**Shape:** the pre-designated strict autonomous `/execute-plan` build loop. The operator opened the session ("open the session") and S90 ran the conversational-intake BUILD Wave A continuously — grounding → build → checkpoint → 3-tier review → merge → close — without pausing for status, per the standing autonomous directive. All on synthetic fixtures + mock clients; **0 live-API spend** (the operator's directive: the live run is the operator-present checkpoint after Wave B).

## What happened

1. **Session open + the park.** The local main checkout was found stranded on `main` @ `dfd44e8` (the operator's parallel-wiki WIP, 15 modified files), 6 commits behind `origin/main`. The build worktree `aplus-ingest-web` sat at `0cd9a24` (= `origin/main`, the S90 directive state). Baseline green (1264/3); LM-01 no trigger (today 2026-06-22 < the 2026-06-29 window open). To neutralize the PF-S71-01 worktree-commit false-block, the main checkout was PARKED on `s90-park` (a same-commit branch); the operator's WIP verified byte-identical (diff hash captured at park; re-verified at un-park).

2. **plan-integrity grounding → GO.** `plan-integrity` ground every Wave-A task's inputs against the live tree (the seams exist; model-client-import baseline 0; `scripts/model/` greenfield) + confirmed the acyclic DAG. Two cosmetic narrative-drift notes (a stale branch-anchor + minor line-offsets); SE agents grounded against the live symbols.

3. **Wave A built via `/execute-plan` (5 tasks, the serial spine `T1 → {T2 ∥ T3 ∥ 0017-T1} → 0016-T1`).** Each a fresh SE agent (full role profile inlined), each an atomic commit, each entry-state-checking its predecessor: `ADR-0015-T1` (swappable no-train model client + runtime key source, single model boundary, fail-closed) → `ADR-0015-T2` (de-identified store-grounded `plan_next_turn` + the `TurnIntent` contract with the CONCERN-1 `record_only` carrier) → `ADR-0015-T3` (plan-author re-wire through the one client, honest no-plan, `assemble` byte-unchanged) → `ADR-0017-T1` (model-proposes-gate-disposes extractor, 0 own `store.append`, + the H-2 `identity_config` wiring at both call sites) → `ADR-0016-T1` (the `/chat` egress seam, loopback, single-egress-class, fail-closed). The SE building the leaf SELF-CAUGHT a real crown-jewel leak at Tier-1 (the first dispatch put `summarize`'s raw free-text values on the model wire) and fixed it to carry only the de-identified `TurnIntent` structure.

4. **Wave-A checkpoint Go/No-Go — EXECUTED green.** Single model boundary (0 imports outside `scripts/model/`), runtime key never tracked, fail-closed on all 3 consumers, `/chat` loopback + single-egress-class, extractor gate-at-write, H-2 at both call sites, `assemble`/`router`/shared-ingest byte-unchanged, `core-capability-audit --self-test` green.

5. **Tier-2 wave review (QA + Security + Architect + plan-integrity, EXECUTED).** 4 findings → fixed: a HIGH crown-jewel leak (the in-population Canadian-postal value-PII gate gap — the operator's locale uses a non-US, Canadian-format postal — slipped the US-ZIP-anchored scanner into the plan-author egress; → PF-S90-01), a MEDIUM Wave-B blocker (`key_source` read `APLUS_NOTRAIN_API_KEY`/`aplus-notrain-api-key` vs the operator's real `ANTHROPIC_API_KEY`/`quant-primary-api`; reconciled), a QA test-gap (no behavioral `/chat` `identity_config` round-trip), an Architect DRY finding (`dispatch_turn` re-implemented the extract→persist chain). Architect traced NOTE-T3-1 (the Factory-to-Component wiring — the real-client author leg is the Wave-B `ADR-0017-T2` obligation) + NOTE-T2-2 (the `intake_complete` consumer semantics) as SOUND carried obligations.

6. **Tier-3 `/review-pr` (6-agent, independence INTACT).** 10 findings, all Suggestion-tier (quality gate PASS); blind-triaged to 6 LEGITIMATE + 2 OUT_OF_SCOPE + 1 NOT_A_BUG + 1 DECISION; 6 LEGITIMATE + 1 adopted (reject-but-adopt F-BUG-1, completing the existing fail-loud boundary posture) fixed → 7/7 executed-blind-verified RESOLVED. Notable: a tautological-for-the-named-path store-adversarial battery (the "extractor write path" tests called `store.append` directly — re-routed through the extractor) + the duplicated de-identified projection (single `_deidentified_view` helper).

7. **Merge + close.** plan-integrity GO; suite 1364/3; `/merge` PR #220 → `main` (REST, GraphQL exhausted, full-40-char SHA guard). Beads: `v70t` (PF-S90-01) + `j432`/`pqb0`/`zwow` (Wave-B follow-ups). Main checkout un-parked back to `main` @ `dfd44e8`; the operator's WIP preserved untouched.

## PF this session

**One new PF — PF-S90-01** (recurrence 6 of `AP-SELF-REVIEW-UNDER-PROBES-INTERACTION-SURFACE`, the PII-scanner-coverage sub-class cf PF-S76-01): the crown-jewel value-PII gate's Tier-1 tests used US-locale PII fixtures only, so the operator's actual Canadian postal format slipped the gate into the plan-author egress. Tier-2-caught in-population, fixed + Tier-3 blind-verified, 0 reached the operator. Structural fix (beaded `v70t`): seed the operator's actual locale into the crown-jewel gate tests. The DEFINING POSITIVE: the marquee crown-jewel interaction (the `/chat`-payload-vs-`summarize`-raw-passthrough leak) was SELF-CAUGHT at Tier-1 — the interaction-probe discipline's first clean self-catch on the highest-stakes surface. Full attestation + skill-trace + disclosure ledger (11 caught, 0 to operator) in `memory/process-failures.md` Session 90.

## Next (S91 — Wave B)

Build Wave B via `/execute-plan` (`ADR-0018-T1` demographic activation → `ADR-0019-T1` `SUMMARY_FIELD_SET` extension → `ADR-0017-T2` end-to-end). The carried Wave-A obligations land here (blocking at Wave-B close): wire a REAL `ModelClient` into the production author leg (NOTE-T3-1, `j432`); the `intake_complete` consumer semantics (NOTE-T2-2); seed the operator's Canadian locale into the crown-jewel gate tests (PF-S90-01, `v70t`). Then the LIVE operator-present run (the operator injects the key; PF-S87-01: a usable plan, not just chat plumbing).
