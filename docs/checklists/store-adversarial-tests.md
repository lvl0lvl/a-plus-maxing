# Store-Adversarial Test Checklist

**Status:** MANDATE, not advice (bead `pka`; placement operator-adjudicated S51).
**Applies to:** every task that writes to or reads from `scripts/store/` (`store.py`, `keying.py`, `loop_schema.py`, `biomarker_meta.py`, and any future store surface). Binding at builder Tier-1 self-check AND in the Tier-2 QA dispatch.

## Why this is a mandate

For five consecutive waves (S37–S41) a safety/PII surface passed the builder's green tests AND Tier-2 (QA + Architect + Security) and was caught only by Tier-3 `/review-pr`. S41's two escapes were both store-keying cases (PR #71; `vault/sessions/session-41.md`): a cross-stream namespace collision where `read_panel` returned a fabricated biomarker value, and a same-timepoint carry-forward dedupe-drop where a contraindication answer was silently dropped — a safety surface. The builder and Tier-2 systematically under-test store-keying collision, dedupe, and cross-stream cases; this checklist shifts the catch upstream of Tier-3. It codifies what the S51 store wave (PRs #98/#99/#101) practiced ad hoc: mutation batteries on every store read/write surface.

## Required adversarial tests (minimum — all four, every store-surface task)

1. **Cross-stream namespace collision.** A read for stream X must never return stream Y's value. Test that a shared bare item name across two streams cannot cross-read (the S41 `read_panel` fabricated-biomarker case — stream namespacing `panel::`/`watch-out::`/`biomarker::`/`feedback::` exists because this escaped to Tier-3).

2. **Same-key collision / same-timepoint dedupe-drop.** Two distinct entries that legitimately share a timepoint must BOTH persist; identical re-entries must stay idempotent. Test the normal-ingest boundary where a second write at an existing `(item, timepoint, source)` is dropped (the S41 carry-forward dropped-contraindication case — content-hashed source tags exist because this escaped to Tier-3).

3. **Dedupe-key boundary cases.** The dedupe identity is `(item, timepoint, source)` — `value` is EXCLUDED (`scripts/store/keying.py`, ADR-0002's D3 follow-up via ADR-0003 OQ-2). Test each field's contribution: same key + different value collides on normal ingest (second write dropped, by design; the explicit correction path instead appends-and-supersedes per ADR-0002 v1.4, pending merge of the store-correction branch — add the correction-path adversarial case when that surface lands); any single field differing does not collide. A test asserting only "no duplicates after re-run" does not cover this.

4. **Mutation-style verification.** At least one test per surface must FAIL when the keying/dedupe logic is deliberately broken (e.g., dedupe key widened to include `value`, or a stream namespace prefix removed). Run the mutation, observe RED, revert. A battery that stays green under these mutations is tautological and does not satisfy this checklist.

## Enforcement points

- **Builder (Tier-1):** the task's verification checklist names the four categories above with the specific tests covering each; "store tests pass" alone is insufficient.
- **Tier-2 QA dispatch:** the dispatch prompt cites this file; the QA review verifies all four categories are present and non-tautological (category 4 actually ran RED) before the wave passes.

## References

- `scripts/store/keying.py` — single source of truth for the line field set and dedupe identity (ADR-0002-T0)
- `docs/adr/ADR-0002-local-first-time-series-store.md` — store substrate; D3/OQ-1 deferred the exact key the code now fixes
- `vault/sessions/session-41.md` — the two S41 Tier-3 catches this checklist exists to move upstream
- Bead `pka` — the S37–S41 five-wave pattern and the S51 adjudication
