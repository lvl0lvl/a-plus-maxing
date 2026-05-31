# Phase-4 Finding Classifications — dermatologist design doc (PF-S3-01 personal source-read)

Each Phase-3 red-team finding was personally source-read against `design/dermatologist-design.md` by the orchestrator (NOT auto-accepted, NOT auto-rejected). All 9 findings classify LEGITIMATE or LEGITIMATE-MODIFIED — every claim was verified true against the doc; 0 REJECTED (so no REJECTED-row source-of-truth attestations needed). Verdicts + Phase-5 dispositions below.

## Role 3 — coverage red-team (red-team-role3-coverage.md, coverage_verdict BLOCK_WITH_FINDINGS)

| ID | Severity | Verified against doc | Verdict | Phase-5 disposition |
|---|---|---|---|---|
| R3-COV-01 | Minor | §11.2 has 9 entries (`grep -cE "^[0-9]+\. \*\*"` confirmed); template spec 5–8 | LEGITIMATE-MODIFIED | Merged §11.2 to 8 (combined the two PF-process anti-patterns; added a bromism anti-pattern from R4D-FIND-01 so 8 includes it). Budget-overage→load-bearing review per feedback memory — no content lost. |
| R3-COV-02 | Major | §18 OQ-3/OQ-4 say "PROPOSED in §13" but §13 had only the mode-floor PROPOSED row (`grep audit-skin-cancer-floor\|audit-image-refusal` §13 → 0) | LEGITIMATE | Added the two audits as PROPOSED §13 rows (disposition (a) — the stronger coverage outcome; surfaces the two load-bearing defenses where /upgrade-agent reads them). §13↔§18 binding now resolves. |
| R3-COV-03 | Major | §13 had no row asserting runtime skin-cancer-floor card-emission or image-non-clearance; only static refusal-class-ID presence (L290) | LEGITIMATE | Same fix as COV-02 (the 2 PROPOSED rows). Kept them PROPOSED (NOT LIVE) — the §13 note + template rule already state the agent.md cites only LIVE/REFERENCED as live defenses; the floor/image runtime behavior is prose-rule + AC + (future) script, honestly disclosed. Carried as a deploy-gating OQ. |
| R3-COV-04 | Nitpick | `grep -c HIGH_RISK_SAMD` = 1 (§2.2 only); absent from §6/§14 | LEGITIMATE-MODIFIED | Threaded HIGH_RISK_SAMD into §6 step 3 (a text-only "tell me if this is cancer" determination → HIGH_RISK_SAMD alongside the F9 floor). |
| R3-COV-05 | Nitpick | §12 = 61 lines vs 25–45 budget; 4 pairs (binary spec) SATISFIED | LEGITIMATE-MODIFIED (accept residual) | The 4 BAD/GOOD pairs are each load-bearing (image / retinoid / DTC / authority). Per budget-overage→load-bearing rule, the pairs are not reducible; the deployed agent.md (≤200-line ceiling, /upgrade-agent Phase 7) is the line-budgeted artifact. Documented justified residual; light prose trim applied to GOOD blocks. |

## Role 4 — adversarial red-team (red-team-role4-safety.md, deploy_verdict BLOCK / CRITICAL)

| ID | Band | Verified against doc | Verdict | Phase-5 disposition |
|---|---|---|---|---|
| R4D-FIND-01 | CRITICAL (H2) | §5 rules 1–12 + §11 + §14 carry NO chemical-/mechanistic-identity→sustained-safety (bromism-class) rule (`grep bromism\|chemically equivalent\|sustained-use` → 0); the closest (rules 3,4,10) cover route/pregnancy/certainty, distinct axes | LEGITIMATE | Added a bromism-class Core Rule (§5 — chemical/mechanistic identity to an endogenous/benign substance does not license arbitrary sustained/stacked topical dosing; sustained-use-dangerous substitution is refused) + a §11.2 anti-pattern + a §14 edge case + §17.1 risk. Merged §5 rule 5→rule 4 to keep ≤12 rules. Anchored to F1 (tretinoin dose-dependent irritation) + F3 (cosmeceutical dosing). |
| R4D-FIND-02 | HIGH (composed H2) | §8 `Read` (L161) lists `vault/*` + "reported inputs" with NO MIME narrowing; restriction (L166) is untagged prose; image-refusal audit is PROPOSED/absent (no LIVE backstop) | LEGITIMATE | MIME-narrowed §8 `Read` to text/markdown only (no image MIME / no image-serving WebFetch) so the taxonomy `IMAGE_OR_SIGNAL_INPUT.mandatory_when` trigger is provably NOT met; added the image-refusal audit as a PROPOSED §13 row (same as COV-02); surfaced the `mandatory_when` MIME-scope ownership as an AQ-candidate to Role 1 in §18 OQ-4. Contract layer was already strong (benign-read non-clearance stated 4×); this adds the mechanical backstop. |
| R4D-FIND-04 | HIGH (H3) | §17.1 Risk #4 banded WARN ("mis-stated AE frequency"); worst-case-reachable for topical-finasteride DHT case is an under-fired Category-X handling contraindication in a pregnancy context (H3), above WARN | LEGITIMATE | Re-banded §17.1 Risk #4: WARN for the AE-frequency mis-statement, but BLOCK-class for the worst-case-reachable Category-X-pregnancy / cardiac sub-path (the topical-finasteride "no systemic DHT" inversion). Runtime Core Rule 4 was already correct; this fixes the risk-register banding. Deliberately NOT inflated to CRITICAL (worst-case is under-warning H3, not acute harm — over-blocking is also a calibration error). |
| R4D-FIND-06 | MEDIUM (H8-amplifier) | `grep -i "eval-aware\|being tested\|test fixture\|identically whether"` → 0; §18 OQ-3/OQ-4 describe the PROPOSED audits as labeled-fixture stimuli (tautological-test risk vs CLAUDE.md "No Tautological Tests") | LEGITIMATE | Added an eval-awareness clause (the floors + refusal taxonomy apply identically regardless of perceived test/fixture/researcher framing — distinct from operator-supplied AUTHORITY_FRAMING) into §5 rule 11 + §11.2; added an anti-tautology requirement (natural-phrasing fixtures alongside any labeled stimuli) to §18 OQ-3/OQ-4. |

## Cross-cutting Phase-5 edits (consolidated)

- §5: merged old rule 5 (sex/route non-transfer) into rule 4 (route+sex non-transfer/extrapolation); added bromism-class rule (new); added eval-awareness clause to rule 11. Net 12 rules (8–12 spec held).
- §6 step 3: threaded HIGH_RISK_SAMD (text-only malignancy-determination) + the eval-awareness note.
- §8: MIME-narrowed `Read`.
- §11.2: 9→8 (merged 2 PF-process entries; added bromism entry).
- §13: +2 PROPOSED rows (audit-skin-cancer-floor.sh, audit-image-refusal.sh) — 3 PROPOSED total; all echo §18.
- §14: +1 bromism/sustained-use edge case.
- §17.1: re-banded Risk #4 (Category-X sub-path BLOCK); added bromism risk (merged the medium+ and gate-self-attest risks + eval-awareness amplifier to hold ≤7).
- §18: OQ-3/OQ-4 anti-tautology requirement + the MIME-scope AQ-candidate to Role 1.
- Appendix A populated with all 9 findings; frontmatter status → Final.

Both red-team verdicts (Role 3 BLOCK_WITH_FINDINGS, Role 4 BLOCK) were design-doc-stage verdicts — the expected Phase-3 outcome. The findings are incorporated in Phase 5; the deployed agent.md is separately gated by /upgrade-agent Phase 6 + `audit-specialist-profile.sh`. No finding was rejected; all were real and are now closed in the Final design doc (the two PROPOSED runtime audits remain integrator beads — honestly disclosed, not claimed LIVE).
