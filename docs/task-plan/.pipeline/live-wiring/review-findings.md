# Recipe Review Findings — Live-Wiring (QA + Architect + Security, S93)

The 5 recipes were authored grounded (no blocking spec defect) and reviewed by QA (all 5) + Architect (keystone+wiring interfaces) + Security (de-id+PII-dispatch). The reviews found the recipes **conceptually sound** — the one CONTRACT gap (ARCH-1) is FIXED in `draft-ADR-0026-T2.md` (the `revise_domains` derivation rule). The remaining findings are recipe-EXECUTABILITY refinements (a gate that is GREEN-at-RED, a grep that false-positives, an extract boundary cited by a drifting line span). They are **blocking per the task-plan pipeline** and MUST be applied at build-RED time (the SE writing each RED test applies the fix as it lands). This ledger carries them forward — nothing is dropped.

**Degraded-mode note (S93):** a remediation subagent hit a monthly spend limit mid-run and the Bash safety-classifier was temporarily unavailable; ARCH-1 was applied directly via Edit; the rest are captured here for the build session (S94) to apply at RED time. This is a documented blocking dependency, not a silent drop.

## APPLIED (S93, directly)
- **ARCH-1 (CONTRACT, was blocking Wave 2) — draft-ADR-0026-T2.md:** the `revise_domains` derivation is now specified — `quality_judge` deductions key on rubric DIMENSIONS, not plan DOMAINS, so the domain comes from the assembled result's `results[domain].section["domain"]` for STRUCTURAL deductions; DIMENSION-level below-band deductions map to ALL run-set domains (conservative re-author, never silent `[]`); ∩ run-set. AC-2 is now non-tautological (structural→specific-domain; dimension-level→all-run-set). Encoded in Step-2 GREEN + the Interface Contract + AC-2.

## TO APPLY AT BUILD-RED TIME (S94, blocking per wave)

### Wave 1 — draft-ADR-0026-T1.md (KEYSTONE)
- **QA-1 (MUST):** the frozen-engine probe (AC-1, inner-engine numstat=0) is mis-placed as a RED-first pytest test — it is GREEN at RED (the inner engine is unchanged before any code) and `<wave-base>` is unresolvable inside pytest. MOVE it to a Verification-Checklist SHELL gate at the Wave-1 checkpoint (matching the build-plan), `git merge-base HEAD <wave-branch>` for the base; frame it as a STANDING INVARIANT (run in REGRESSION/checkpoint), not a RED-first feature test.
- **QA-2 (MUST):** the no-fork probe greps the literal token `safety_passed is True`, which legitimately survives in `plan_orchestrator.py` comments/docstrings (~:76/211/378) → false-positive RED. Target EXECUTABLE control flow: grep the `while True:` loop header + the `disposition.get("safety_passed") is True` EXPRESSION at a non-comment line, OR strip comments before counting. (Apply the same fix to T3's skill-level no-fork grep.)
- **ARCH-2 (cross-module):** before extraction, ENUMERATE every `disposition.get(...)` read in `run_orchestrated`'s loop (a grep surfaced a possible `disposition.get("n")` adjacent read) and preserve each verbatim in the extracted driver; add a Verification line: "the extracted driver reads the SAME disposition keys (`accept`/`safety_passed`/`revise_domains` + any alias) the inline loop read — enumerated against the live function, not assumed." Reconcile the `n` read (preserve if real; test-confirm unreachable if dead).
- **ARCH-3 (extract boundary):** cite the extract boundary by STRUCTURE, not the line span `:260-300` (which EXCLUDES the scratch-store `tempfile.TemporaryDirectory` lifecycle at ~:252-259 the driver must own) — "from the scratch-`TemporaryDirectory` setup through the `while True:` body and its `_promote_plans` call."
- **QA-3 (SHOULD):** the store-seam golden-line — capture + COMMIT the golden store-line bytes from the pre-extraction (entry-state) HEAD as a static fixture in the Cycle-5 RED step, BEFORE GREEN modifies the promote seam (a runtime re-capture is tautological).

### Wave 1 — draft-ADR-0027-T1.md (de-id backend)
- **QA-4 (SHOULD):** relabel Cycles 3-4 RED expectations — the CLEAN probe is GREEN-on-the-oracle after Cycle 1; the MUTATION/leak-variant is the RED-capability demo. The RED obligation for these pin-existing-behavior cycles is satisfied by the VARIANT going RED, not the clean case.
- **SEC-2 (LOW):** extend the AC-7 tmp-tree rglob scan (already built for raw-PII tokens) to ALSO assert 0 files under the tmp tree carry the synthetic KEY token (closes the gitignored-key-residue gap the diff-only grep misses).

### Wave 2 — draft-ADR-0026-T2.md
- (ARCH-1 applied — see above. No further Wave-2 recipe findings; T2 was otherwise CLEAN per QA.)

### Wave 3 — draft-ADR-0026-T3.md (skill front-door)
- **QA-7 (SHOULD):** the recursive 0-raw-PII payload scan must SERIALIZE the ENTIRE dispatch payload to a string and grep that (the live `_dispatch_prompt` payload is a flat string with `json.dumps(summary)` embedded — dict/list recursion alone misses tokens inside the stringified prompt). Not an "OR" alternative.
- **QA-8 + SEC-1 (SHOULD/MEDIUM):** the prose-removal grep leaves a SECOND `router.summarize(store_read)` reference standing (SKILL.md ~:61 "the author's ONLY operator-state source is … `router.summarize(store_read)`"). On the A′ path the specialists author over the live `deid_in`/`ModelClient.deidentify` summary. Either require the grep find 0 surviving `router.summarize` de-id-IN/operator-state-source refs (both ~:48 and ~:61), OR disambiguate ~:61 (router.summarize survives ONLY as the persisted-side store-read gate per deid_in.py:11-14, NOT the A′ operator-state source). Scope to the de-id-IN/operator-state PHASE, not a whole-file count.
- **QA-2 (the skill no-fork grep):** same executable-not-token fix as Wave-1 QA-2.

### Wave 3 — draft-ADR-0026-T4.md (audit repoint + self-test)
- **QA-5 (MUST):** the repointed structural check must grep the RIGHT module per token — `pipeline.run_generation` lives in `plan_orchestrator.py` while the disposition gate (`safety_passed`/`accept`/`revise_domains`) lives in `plan_driver.py`. Pin each grep to its host module + assert EXECUTABLE references (the QA-2 comment-false-positive risk). State whether `$CALLER` becomes `plan_driver.py` or the check spans both. (Dropping the `record_plan(` check is CORRECT — the A′ spine doesn't call it.)
- **ARCH-4 (cross-module):** the A′-inversion self-test SHOULD drive the REAL `gate_dispatch` composer over fixture judge/review results (NOT a hand-shaped fixture disposition), so the audit's behavioral leg exercises the T1↔T2 seam end-to-end and `depends-on ADR-0026-T2` is real. Pin the real-composer route in the recipe (not "in GREEN").
- **QA-6 (SHOULD):** the negative-test (`scripts/tests/test_core_capability_audit.sh`) staleness fix must ENUMERATE the stub rewrites — case C's `wired.py` must contain the NEW A′-spine tokens (`run_generation` + the disposition tokens) else its GREEN inverts to a false RED; cases A/B2 must omit a SPECIFIC new token so they RED for the right reason.

### Cross-cutting (S94 forcing function)
- **SEC-3 (LOW):** confirm an S94 landmark/bead carries the LIVE-subscription-dispatch 0-raw-PII-to-a-REAL-agent observation as a release gate (the one crown-jewel property the mock build correctly DEFERS to S94 — it must not evaporate). See bead created S93.

## Status: ARCH-1 applied; 13 executability findings carried to S94 build-RED time (blocking per wave).
