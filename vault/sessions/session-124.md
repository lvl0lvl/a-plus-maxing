---
title: Session 124 — live-run pre-flight; mk0i author-output crash fixed + 5 review-caught safety findings closed before spend
type: session
date: 2026-07-09
status: complete
permalink: a-plus-maxing/sessions/session-124
---

# Session 124 — live-run pre-flight (merged)

## What landed
Operator-directed: "fix everything that needs to be fixed before we run." Verified the live-run readiness (key in keychain, anthropic SDK live, real store `vault/store/` = 6263 readings incl. DOB/demographics/goals/wearable/DNA, crown-jewel de-id LIVE-PROVEN S122), then closed the one real crash risk on the live plan path — `a-plus-maxing-mk0i`, the author-output-boundary 940o crash the S123 pkty review surfaced.

## The mk0i fix
`normalize_author_output` (`scripts/serve/intake_aggregate.py`, sibling of `normalize_summary`) coerces a model author envelope's per-rec scalar-contract fields so the frozen plan composer can't crash on a list/dict-valued field:
- `claim` → space-joined (not `; ` — that splits a limit-violating phrase past the substring HALT).
- `category` → non-scalar → None; scalar → `strip().lower() or None` — routing a non-matching/empty class into the composer's FAIL-CLOSED indeterminate path (NEVER joined — a joined class would miss the prohibited-class set and fail OPEN).
- `grounding` → an animal/in-vitro marker (list/tuple element OR dict value) preserved so the population-mismatch flag still fires.
- `numbers` → dict-only filter (a malformed number dropped, never crashes `_is_complete`).
Applied at the injectable `build_dispatch` seam (Path A, cadence) AND wrapped at `server.py`'s Path B `/generate-plan` (the UI front door). Frozen ADR-0032 spine numstat=0 — all fixes at non-frozen seams.

## The review earned its keep (PR #324, FULL 6-agent /review-pr)
The review of the FIRST cut of the fix caught 5 real findings BEFORE the real-spend run:
- **SEC-01 (fail-open, impact 4):** a scalar-string category in a non-canonical form ("Stimulant"/"stimulants"/" stimulant "/"") bypassed `assemble`'s exact lowercase-singular prohibited-class check → a prohibited-class rec shipped ACTIONABLE against a "no stimulants" hard-limit. Fixed by canonicalizing the scalar category; the plural/synonym residual (needs the frozen exact-match set) beaded `99y4`.
- **API-01/BUG-01 (Contracts + Bug-Hunter convergent):** the first fix wired normalize only at Path A (`build_dispatch`); the live `POST /generate-plan` (the operator's UI button, Path B) called `self.client.author` raw and reached the identical crash in the frozen `generate_plans → assemble`. Fixed by wrapping `server.py`; the durable single model-boundary beaded `ec4e`.
- **SEC-02:** the `; ` claim-join split a limit phrase → space-join.
- **SEC-03/TEST-02:** a dict-shaped grounding dropped the population-mismatch disclosure → scan dict values.
- **HIST-01/QUAL-01:** `_GROUNDING_FLAG_TOKENS` byte-mirrored `assemble.GROUNDING_NEEDS_FLAG` with no tripwire → a test-time desync pin.
All 5 blind-triaged LEGITIMATE (every deciding repro EXECUTED) → fixed at non-frozen seams → blind-verified RESOLVED with every guard reversion-proven load-bearing (incl. the API-01 probe driving the REAL /generate-plan server thread) → Phase-8 CLEAN → merged `52ba6a41`.

## PF-S124-01
Promoted (recurrence_count 2): a crash/safety-class fix placed at ONE seam handling only the demonstrated shape — not the adversarial variant space nor all production ingresses. Recurs S123 (my pkty audit missed the author boundary; the review found it, logged then as "review working"). On the 2nd instance it promotes. Guard: apply Call-Chain-Review / Factory-to-Component + adversarial variant enumeration BEFORE review for a fix backing real spend. Remediations: `99y4` (frozen enum), `ec4e` (single boundary), process bead `30l5`.

## Live-run readiness
The crown-jewel de-id path + the 4-domain compose are LIVE-READY (verified 0-spend); the author path now fails CLOSED on real/adversarial model output. **The operator-present LIVE run itself is the next step** — real spend, real data, operator present — and is the only remaining operator-gated action.

## Next
The LIVE run (operator-gated). Remaining beaded/gated: `99y4` (SEC-01 plural residual, frozen enum/Architect), `ec4e` (durable single boundary, Architect), `c34r` (active-issue → hard-limit safety-design, operator), `s923` (de-id-side boundary enforcement, Architect), the other beads unchanged.

## Related
- [[session-123]] (the pkty review that surfaced mk0i).
