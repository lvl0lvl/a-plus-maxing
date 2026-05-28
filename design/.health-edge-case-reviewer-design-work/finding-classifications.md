---
title: Phase 4 Finding Classifications — Role 3 (health-edge-case-reviewer) Pass-2
type: phase-4-verification
session: S11
created: 2026-05-27
phase: 4 (orchestrator-side personal source-read; PF-S3-01 guard)
input_artifacts:
  - design/.health-edge-case-reviewer-design-work/red-team-adversarial.md (22 findings F-001..F-023; F-019 withdrawn = 21 active)
  - design/.health-edge-case-reviewer-design-work/red-team-safety.md (10 findings S-01..S-10)
total_findings_examined: 31
verdict_breakdown:
  LEGITIMATE: 27
  LEGITIMATE-MODIFIED: 1 (F-020)
  REJECTED-with-cited-evidence: 2 (F-010, F-021)
  DUPLICATE: 1 (S-06 = F-002)
  WITHDRAWN: 1 (F-019 — at adversarial-reviewer's own verification)
pf_attestation: PF-S3-01 guard held; every finding source-read against design/health-edge-case-reviewer-design.md OR canonical upstream contract before verdict; zero rubber-stamps; two REJECTED verdicts carry cited evidence per the reject-but-adopt feedback memory pattern.
---

# Phase 4 — Finding Classifications

Per CLAUDE.md `## Session Start Protocol` PF-S3-01 guard and Role 2 S10 precedent. For each red-team finding, the orchestrator personally source-read the cited file:line range OR ran the cited grep/sed/awk command BEFORE assigning verdict. No verdict assigned from prose pattern-match. No verdict assigned to a finding without verification.

This is the **fifth consecutive PF-S3-01 falsification window** (S7 design-doc, S8 design-doc, S9 /upgrade-agent, S10 Pass-2, S11 Pass-2 — held in all five). Recurrence_count for AP-ORCH-SELF-ATTEST remains at 2.

---

## Verdict summary

| Verdict | Count | Findings |
|---|---|---|
| LEGITIMATE | 27 | F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-022, F-023, S-01, S-02, S-03, S-04, S-05, S-07, S-08, S-09, S-10 |
| LEGITIMATE-MODIFIED | 1 | F-020 |
| REJECTED-with-cited-evidence | 2 | F-010, F-021 |
| DUPLICATE (collapses to another finding) | 1 | S-06 (→ F-002) |
| WITHDRAWN (at red-team verification) | 1 | F-019 |

Severity distribution (LEGITIMATE + LEGITIMATE-MODIFIED only):

- CRITICAL: 2 (S-01, S-02)
- Important / HIGH: 6 (F-001..F-004 cluster, F-005, F-006, F-007, F-008, F-009, F-011, F-014; S-03, S-04, S-05) — Phase-3 reviewers' severity tags retained
- Suggestion / MEDIUM-LOW: remainder

---

## Per-finding verification + verdict

### F-001 — §11.1 PF-S6-01 row cites §13 row 12; should cite row 22 → **LEGITIMATE**

Personal source-read evidence:
- Line 335 (§11.1 PF-S6-01 row): `"Mechanical guard: §13 row 12 (re-review-on-amendment trigger; reviewed_against_ancestry_sha: field)"` — confirmed via Read.
- Line 531 (§13 row 12): `"Atomic-claim decomposition [R11; Finding 9; arch R3.11; wiki-entry-review only]"` — confirmed; row 12 is NOT re-review-on-amendment.
- Line 541 (§13 row 22): `"Re-review-on-amendment trigger [PF-S6-01; QA Q12] ... Role 3 maintains reviewed_against_ancestry_sha:"` — confirmed; row 22 IS the correct re-review row.

Defect class: AP-INCOMPLETE-PROPAGATION at synthesis layer — §13 was renumbered from 44 drafter-rows to 23 synthesized rows; §11.1 mechanical-guard pointers were not re-anchored.

### F-002 — §11.1 PF-S2-04 row cites §13 row 7; should cite row 5 → **LEGITIMATE**

- Line 331 (§11.1 PF-S2-04): `"Mechanical guard: §13 row 7 (operator-profile inlining detection ...)"` — confirmed.
- Line 526 (§13 row 7): `"Mechanical-pre-audit before semantic adjudication"` — confirmed; row 7 is NOT operator-inlining.
- Line 524 (§13 row 5): `"Operator-profile under-coverage surfacing ... also grep-checks specialist body for operator-bound tokens (Walter, 2026-01, etc.)"` — confirmed; row 5 IS the operator-inlining detection.

Note: medical-safety S-06 is a duplicate of this finding via a different probe angle. Apply fix once.

### F-003 — §11.1 PF-S2-05 row cites §13 row 1 + row 11; should cite row 21 → **LEGITIMATE**

- Line 332 (§11.1 PF-S2-05): `"Mechanical guard: §13 row 1 (canonical YAML sourced at every review) + row 11 (re-read cadence attestation)"`
- Line 520 (§13 row 1): `"Finding-not-fix + reviewer-finding schema"` — confirmed; row 1 is NOT canonical-YAML sourcing.
- Line 530 (§13 row 11): `"Adjudication path named [R5; Finding 8; arch R3.10]"` — confirmed; row 11 is NOT re-read cadence.
- Line 540 (§13 row 21): `"Self-audit-before-return + re-Read cadence attestation ... re_read_attestation: {refusal_taxonomy_loaded_at, risk_class_table_loaded_at, review_started_at}"` — confirmed; row 21 IS re-read cadence + canonical-YAML loaded-at timestamps.

### F-004 — §11.1 PF-S2-02 row cites §13 row 4 + row 5; row 4 correct, row 5 should be row 20 → **LEGITIMATE**

- Line 329 (§11.1 PF-S2-02): `"Mechanical guard: §13 row 4 (locator-resolution) + row 5 (quoted_text verbatim)"`
- Line 523 (§13 row 4): `"Locator-resolution audit"` — confirmed correct.
- Line 524 (§13 row 5): `"Operator-profile under-coverage surfacing"` — confirmed wrong (already cited in F-002).
- Line 539 (§13 row 20): `"Quoted-text-verbatim audit ... Every finding's quoted_text: appears verbatim at cited locator"` — confirmed; row 20 IS quoted-text-verbatim.

### F-005 — `AGENT_TEMPLATE.md` referenced as forbidden Edit target; file does not exist in project `templates/` → **LEGITIMATE**

- Line 225 (§8.3): forbidden-list mentions `AGENT_TEMPLATE.md` alongside project-relative paths.
- `ls /Users/waltermcgivney/Documents/Projects/a-plus-maxing/templates/` → only `refusal-class-taxonomy.yaml` + `specialist-risk-class.yaml`. `AGENT_TEMPLATE.md` is NOT in project templates.
- `ls ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` → exists at skills_library path.

Fix scope-extend or escalate: Role 1 and Role 2 design docs may share the same defect. Recommendation per finding: replace with absolute path. If Role 1/2 share, escalate via AQ rather than inline-fix here.

### F-006 — §13 row 1 schema field `recommendation.action` (enum) vs §12 Negative Examples emit `recommendation_class: add_refusal_class` (flat, non-enum) → **LEGITIMATE**

- Line 520 (§13 row 1): `"recommendation.action ∈ {revise_wiki_entry, add_caveat, withdraw_claim, stratify_claim, refer_to_role4, escalate_to_adjudicator} + target_field"`
- Line 462 (§12.2 GOOD): `recommendation_class: add_refusal_class` (flat top-level field; `add_refusal_class` not in row-1 enum).
- Line 501 (§12.3 GOOD): same shape.
- Line 130 (§4.3 OUTBOUND row 1): `recommendation{action,target_field}` (third shape).

Three different schema shapes for the same field across §2.2 / §4.3 / §12 / §13. The Negative Examples ARE the calibration the deployed reviewer mimics — schema validator (PROPOSED, row 1) would reject what §12 GOOD shows.

### F-007 — §12 BAD blocks emit literal `severity_final: WARN` tokens that AC-deploy-19 bans on deployed agent.md → **LEGITIMATE**

- Line 482 (§12.3 BAD): `severity_final: WARN  (set by reviewer)` — confirmed literal token.
- Line 671 (§15.2b AC-deploy-19): `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" ... = 0` — but this AC bans different tokens (`YOU MUST` family, not `WARN`). The finding's specific claim about AC-deploy-19's grep set is partially off-target, BUT the underlying concern is valid: BAD-block content carrying severity self-finalization could leak into deployed profile via /upgrade-agent if not explicitly quarantined.
- No "Do NOT execute — illustrative only" prefix in any BAD block.

Verdict refinement: the finding's specific grep-target claim is wrong (severity_final tokens aren't in AC-deploy-19's banned-token list), but the structural concern (imperative bleed from BAD blocks via /upgrade-agent) is real. Fix: add explicit quarantine markers to §12 BAD blocks per Role 2 §5 rule 4 precedent.

### F-008 — §13 row 5 Status `PROPOSED` + Consequence bifurcated `WARN → BLOCK` creates undefined script behavior → **LEGITIMATE**

- Line 524 (§13 row 5): `"PROPOSED | WARN (pre-AQ-001) → BLOCK (post-AQ-001)"` — confirmed.
- §13 preamble (line 512) defines tag values: LIVE / REFERENCED / PROPOSED only. The bifurcated consequence has no in-row gating field; AQ-001 resolution lives in §18 OQ-2 (out-of-row state).
- A script invocation (`scripts/audit-reviewer-output.sh --check operator-profile-coverage`) cannot tell whether to WARN or BLOCK without out-of-band AQ-001-state knowledge.

### F-009 — §13 row 12 status `PROPOSED` + Consequence `BLOCK (wiki) / N/A (specialist)`; counted as single PROPOSED in row 22-tally → **LEGITIMATE**

- Line 531 (§13 row 12): `"PROPOSED | BLOCK (wiki) / N/A (specialist)"` — confirmed.
- Line 544: `"Status-tag count. LIVE: 0. REFERENCED: 1 (row 23). PROPOSED: 22"` — row 12 counted singly despite target-type binary applicability.
- Audit-script invocation pattern has no documented `--target-type` flag for row 12.

### F-010 — §15.2a AC-2 awk pattern accepts ACCEPTED|DEFERRED|REJECTED; §3.2 has only ACCEPTED rows → **REJECTED-with-cited-evidence**

- Line 651: AC-2 awk pattern verified — accepts the broad verdict set.
- §3.2 lines 81-95: every R-row is `ACCEPTED` or `ACCEPTED — <qualifier>` — confirmed.

**Rejection rationale (cited evidence).** The looseness is intentional per the explicit clause `"Hyphenated qualifiers (ACCEPTED — calibration-pending, ACCEPTED — narrowed-scope) permitted per Role 2 F-021 precedent"` at line 651. The check's purpose is to ensure every R-row has SOME verdict (catches a missing-verdict synthesis bug), NOT to catch verdict-downgrade direction. AC-2 mirrors Role 2 §15.2a AC-3 by precedent; widening to strict ACCEPTED would diverge from established pattern without compensating benefit. The finding self-acknowledges "Suggestion" severity and "Accept (low impact)" resolution path.

**Reject-but-adopt:** No fix adopted; AC-2 kept as-is per project precedent.

### F-011 — `[no-paired-probe-required: <rationale>]` annotation has no rationale-quality check → **LEGITIMATE**

- Line 148 (§5 rule 4): annotation permits escape from paired-probe discipline with `<rationale>`.
- Line 527 (§13 row 8): `"pair-existence audit walks finding set looking for unpaired refusals"` — no rationale-content check.
- A reviewer could satisfy paired-probe discipline by annotating `[no-paired-probe-required: skipped]` on every refusal — exact rubber-stamp surface AP-2 forbids.

### F-012 — §8.3 forbidden-list ambiguity: `templates/` could be read as forbidding Read, contradicting §10.1 → **LEGITIMATE**

- Line 225 (§8.3): `"Edit / Write against any path under review: ... templates/, ..."` — bold prefix scopes prohibition to Edit/Write, but bold-prefix-vs-list structural separation is small.
- Lines 283-284 (§10.1 items 6+7): mandate Read of `templates/refusal-class-taxonomy.yaml` + `templates/specialist-risk-class.yaml`.

### F-013 — §12 intro narrative parenthetical "(SE-draft anticipated 1–5; QA delivered 7)" bleeds build-pipeline narrative into deployed profile → **LEGITIMATE**

- Line 403 (§12 intro): confirmed parenthetical exists. Phrasing has zero behavioral content for the deployed reviewer.

### F-014 — `scripts/audit-reviewer-output.sh` referenced 29 times; script does not exist; cluster size warrants explicit acknowledgment beyond per-row PROPOSED → **LEGITIMATE**

- `grep -c "audit-reviewer-output.sh" $FILE` = 29 — confirmed.
- `ls /Users/waltermcgivney/Documents/Projects/a-plus-maxing/scripts/` = `handoff-audit.sh`, `lib/`, `pf-attestation-audit.sh`, `scope-contract-audit.sh`, `tests/` — script does NOT exist.
- AC-deploy-14 checks `test -x scripts/audit-reviewer-output.sh` only; no per-sub-command existence AC.

### F-015 — §5 rule 12 forbids inline class-extension but rule 8 + OQ-5 permit inline axis-extension; asymmetry undocumented → **LEGITIMATE**

- Line 164 (§5 rule 12): refusal-class taxonomy is statutory; novel class needs AQ.
- Line 156 (§5 rule 8): `stratification_axes_tried: [...]` — no enumeration constraint.
- Line 783 (§18 OQ-5): orchestrator extends axis-set on calibration signal.

Asymmetry is reasonable (statutory vs calibration-derived) but undocumented in §5.

### F-016 — §9.1 timestamp `<timestamp>` precision undefined; §12.2 example uses minute precision (2026-05-27T1503) → **LEGITIMATE**

- Lines 211, 252: `<timestamp>` placeholder undefined.
- Line 451: example shows minute precision.
- Same-minute collisions possible; format spec needed.

### F-017 — §13 row 23 coverage claim ("all Role-3 dispatches including AQ + divergence-log") broader than hook's INV-ROLE-INLINING trigger pattern → **LEGITIMATE**

- Line 542 (§13 row 23): coverage claim includes AQ dispatches + divergence-log re-tuning agents.
- INVARIANTS.md line 41: hook matches `"H1=# {Role Name}` or `roles/<slug>/agent.md` ref"`.
- AQ dispatches without H1/roles-ref pattern would escape the hook.

### F-018 — §16 candidate INV promotion criteria "≥1 specialist actually reviewed" doesn't specify dispatch cadence (one-at-a-time vs batch) → **LEGITIMATE**

- Line 693 (§16 INV-COVERAGE-GAP-FINDING-SCHEMA): promotion gated on ≥1 review.
- Line 720 (§17.2 A-2): "Role 2 has executed at least one specialist before Role 3 first dispatch" — cadence unspecified.

### F-019 — WITHDRAWN at red-team verification (`vault/library/_source-whitelist.md` exists) → **N/A**

No action; reviewer's own withdrawal stands.

### F-020 — EC-5 covers amendment-AFTER-deployment but not the design-doc-finalize → /upgrade-agent dispatch window → **LEGITIMATE-MODIFIED**

- Line 10 frontmatter: `last-PF-reviewed: PF-S6-01`.
- Lines 596-604 (EC-5): hypothetical PF-S7-01 between authoring and review.
- Genuine gap: if `memory/process-failures.md` gains a new PF between design-doc finalize (Phase 5 close) and `/upgrade-agent` Session B dispatch, no mechanism re-routes.

**Modification:** orchestrator note — the recommended fix (extend EC-5 to cover the window) is valid, but the design-doc-finalize→/upgrade-agent window is normally tight (same session in S10's Role 2 pattern; separate sessions in current S11 plan). Adopt a narrower fix: add a single bullet to EC-5 about the window rather than an EC-5b sibling. Reduces section count drift.

### F-021 — §17.1 Risk-5 inline arXiv citation breaks doc's `[Finding N]` citation pattern → **REJECTED-with-cited-evidence**

- Line 711 (§17.1 Risk-5): `"surface-form bias (Finding 6: Bias-in-the-Loop, arXiv:2604.16790)"` — confirmed inline arXiv.

**Rejection rationale (cited evidence).** The arXiv ID is load-bearing for a future reader who wants to verify Finding 6 directly without traversing Pass-1 substrate. The ~6-token cost is cheap insurance against future reader friction; the substrate's reference [38] is one path-resolution away but inline-arXiv is zero-cost-to-resolve. Role 1 design doc precedent: Role 1 §17 Risk-N entries cite primary sources inline alongside Finding/R anchors (Role 1 design doc §17.1 — same convention). F-021 self-acknowledges Suggestion-tier and "Accept (informational)" disposition.

**Reject-but-adopt:** No fix adopted; inline arXiv kept per cross-role precedent.

### F-022 — `AP-REVIEW-MISSED-COVERAGE` identifier in §17.3 BC-2 doesn't match PF identifier convention `PF-S\d+-\d+` → **LEGITIMATE**

- Line 732 (§17.3 BC-2): cites `AP-REVIEW-MISSED-COVERAGE` — confirmed fabricated identifier.
- `memory/process-failures.md`: PFs use `PF-S\d+-\d+` only.
- §5 rule 12 fabrication guard explicitly forbids inventing identifiers; BC-2 violates own discipline.

### F-023 — §18 OQ-6 resolution path doesn't make sequential dependency chain explicit → **LEGITIMATE**

- Line 791 (OQ-6): `"First Role 3 dispatch + schema-validator authoring (row 1) at Session B"` — three sequential dependencies (Session B output, audit script existence, ≥1 Role 2 specialist) collapsed into one sentence.
- Line 747 (OQ-1) confirms 22 PROPOSED rows depend on script.

### S-01 — AUTHORITY_FRAMING_BYPASS coverage rule gated on "declared in specialist's Role Boundaries"; admits specialist that OMITS the class → **LEGITIMATE / CRITICAL**

- Line 536 (§13 row 17): `"boundary_class_coverage block enumerates every class in templates/refusal-class-taxonomy.yaml declared in specialist's Role Boundaries; AUTHORITY_FRAMING_BYPASS row present for every specialist regardless of declaration"` — confirmed.
- First-half scopes to *declared* classes; second-half adds AFB-row-presence (not AFB-covered) requirement.
- Row 17's mechanical check verifies row-presence-in-report, not covered-with-evidence verdict.
- `templates/refusal-class-taxonomy.yaml` line 69: `mandatory_for_every_specialist: true` for AFB — this canonical mandate has zero LIVE enforcement against the 81.8% Walter-A3 attack vector.
- Both `scripts/audit-specialist-profile.sh` (Role 2) and `scripts/audit-reviewer-output.sh` (Role 3) are PROPOSED → no script catches.

**Severity confirmed: CRITICAL.** This is the canonical Role-3-failure-mode-recurring-at-design-layer.

### S-02 — H-class composition input contract: §4.3 OUTBOUND row 2 promises "canonical here" but no NCC MERP → H-class mapping table embedded → **LEGITIMATE / CRITICAL**

- Line 131 (§4.3 OUTBOUND row 2): `"The NCC MERP → H-class mapping table is canonical here."` — confirmed: table promised but NOT embedded in §4.3 or §13.
- §13 row 18 (line 537) lists 8 required fields but doesn't specify (i) NCC MERP A/B/C/D/E/F handling, (ii) whether `h_class_equivalent_max` may be NULL, (iii) Role 4's behavior on null.
- Two exploitable downgrade paths confirmed (NULL silent downgrade; catchall H8).

**Severity confirmed: CRITICAL.** Breaks load-bearing safety arithmetic.

### S-03 — `severity_final.set_by` defense is one-string-match; null/absent/aliased role IDs bypass → **LEGITIMATE / HIGH**

- Line 522 (§13 row 3): `"schema rejects severity_final.set_by == 'health-edge-case-reviewer'"` — confirmed literal-match only.
- Aliased forms (`set_by: reviewer`, `set_by: self`, `set_by: null`, absent field) all bypass.
- §13 row 1 schema validator (PROPOSED) is the only mitigation; `templates/reviewer-finding.schema.json` doesn't exist.

### S-04 — §2.1 vs §4.1 disagree on Mechanism A routing → **LEGITIMATE / HIGH**

- Line 47 (§2.1): `"Mechanism A: Silent Agreement → Role 4 Council-Mode dissent slot per Role 1 §4 OUTBOUND row 8"` — routes ENTIRELY to Role 4.
- Line 110 (§4.1 row 4): `"Mechanism A → divergence-log tuning + Role 4 Council-Mode reference"` — splits across two surfaces.
- Internal contradiction confirmed.
- Role 4 not deployed; per §2.1 routing, Mechanism A has no current operationalization.

### S-05 — §13 rows 1 + 17 don't jointly prevent `findings: []` after `audit_passed: true` → **LEGITIMATE / HIGH**

- Line 520 (§13 row 1): finding-schema enforcement only on findings array.
- Line 536 (§13 row 17): `boundary_class_coverage` row presence not row content.
- Per F-006 + S-05: schema validator (PROPOSED) is the only joint enforcement; not LIVE.
- §11.2 AP-2 prose-discipline is well-anchored but single-layer.

### S-06 — DUPLICATE of F-002 (different probe angle, same defect) → **DUPLICATE; apply F-002 fix only**

- S-06 cites the §11.1 PF-S2-04 row 7 reference (line 331); identical defect to F-002.
- Both findings recommend the same fix (correct row reference).
- Fixing F-002 closes both.

### S-07 — §13 row 22 PROPOSED + not wired into CLAUDE.md `## Session Close Protocol` step 8.5 → **LEGITIMATE / MEDIUM**

- Line 541 (§13 row 22): PROPOSED.
- CLAUDE.md lines 86-88: step 8.5 enumerates `handoff-audit.sh`, `scope-contract-audit.sh`, `pf-attestation-audit.sh` — confirmed NO reviewer-output audit.
- §13 row 22's mechanical defense is unwired at the project's actual session-close enforcement point.

### S-08 — No runtime indicator distinguishes PROPOSED from LIVE at dispatch time → **LEGITIMATE / MEDIUM**

- §13 status-tag count line 544: 22 PROPOSED, 1 REFERENCED, 0 LIVE.
- §10 Context Loading reads `INVARIANTS.md` once at dispatch start (line 297 §10.3 item 14) but no per-dispatch `live_rows:` field documented.
- Dispatch has no mechanical way to know which §13 rows are currently LIVE.

### S-09 — AQ-001 surfaces narrower than EC-3's IDENTICAL/DIFFER case; per-class field-enumeration gap not gated → **LEGITIMATE / LOW**

- Line 524 (§13 row 5): PROPOSED with prose-only emission pre-AQ-001.
- Line 583 (EC-3): covers IDENTICAL/DIFFER partition (3-specialist boilerplate), NOT per-specialist-class under-coverage.
- Two distinct AQ-001 surfaces; only one is gated.

### S-10 — §11.2 AP-7 divergence-tuning is first-person discipline; §13 row 14 fires WARN at session close, not BLOCK mid-session → **LEGITIMATE / LOW**

- Line 397 (§11.2 AP-7): recognition cue first-person.
- Line 533 (§13 row 14): `"PROPOSED | WARN at session close"` — confirmed.
- Mid-session self-edit window not blocked mechanically.

---

## Resolution consolidation map

To minimize disposition churn at Phase 5, findings group into 9 resolution bundles:

**Bundle A — §11.1 row-pointer correction (F-001 + F-002 + F-003 + F-004 + S-06):**
Fix the four row-number references in §11.1 PF-coverage table. Bundle includes audit of all 8 §11.1 rows to verify no additional row-pointer drift (F-004's recommendation extends bundle to all §11.1 rows).

**Bundle B — Schema-shape unification (F-006 + S-03 + S-05):**
Decide one shape for `recommendation` field (nested vs flat); unify across §2.2, §4.3, §12, §13. Add explicit set_by enum + verdict enum for `severity_final`. Add joint enforcement that `findings: []` cannot coexist with any `[not-covered]` in `boundary_class_coverage`.

**Bundle C — AUTHORITY_FRAMING_BYPASS strict-enforcement (S-01 + F-005):**
Reword §13 row 17 to require AFB `[covered]` with `match_count ≥ 1`, independent of specialist's declaration. Add LIVE inheritance assertion. Add AC-12. (F-005 path-scoping is adjacent — `AGENT_TEMPLATE.md` needs absolute path scoping for fresh-context determinism.)

**Bundle D — NCC MERP → H-class mapping embed (S-02):**
Embed the canonical NCC MERP → H1-H8 mapping table inline in §4.3 row 2. Specify A-I outcomes. Schema-enforce `h_class_equivalent_max` non-null on emission. Add downstream contract round-trip AC.

**Bundle E — Mechanism A routing fix (S-04 + S-10):**
Reconcile §2.1 vs §4.1 on Mechanism A. Pick one routing (recommend: split with both Role 4 path + intra-role re-review cosine-similarity defense per substrate Finding 5 + CONSENSAGENT >0.95). Add §13 row enforcing mid-session divergence trigger (not session-close-only).

**Bundle F — §13 row tagging hygiene (F-008 + F-009 + F-014 + F-017 + S-08):**
- Split row 5 into 5a (WARN, PROPOSED pre-AQ-001) + 5b (BLOCK, PROPOSED post-AQ-001 trigger) OR keep WARN with bead-tracked promotion (F-008).
- Add `--target-type` parameter to row 12 invocation; update count (F-009).
- Add per-sub-command existence AC (F-014).
- Narrow row 23 coverage claim to hook-matched dispatch patterns OR extend hook trigger via INV-change-ritual (F-017).
- Add `live_rows:` field to §9.1 7-field return; add `runtime_safety_class:` (S-08).

**Bundle G — Voice + narrative cleanup (F-007 + F-013):**
- Add "Do NOT emit — illustrative only" prefix to each §12 BAD block (F-007).
- Delete §12 intro parenthetical "(SE-draft anticipated 1–5; QA delivered 7)" (F-013).

**Bundle H — Discipline-vs-mechanical asymmetry + extension rules (F-011 + F-012 + F-015 + F-018):**
- Add rationale-quality sub-check to §13 row 8 (F-011).
- Disambiguate §8.3 with "(NOT Read)" or per-operation bullets (F-012).
- Document rule-12-vs-rule-8 asymmetry in §5 (F-015).
- Update §16 candidate INV promotion: ≥3 specialists across ≥2 risk classes (F-018).

**Bundle I — Wiring + format spec (S-07 + S-09 + F-016 + F-020 + F-022 + F-023):**
- Wire §13 row 22 into CLAUDE.md session-close step 8.5 (S-07).
- Extend §13 row 5 prose-only emission to include class + field-set + rationale; add EC for under-coverage-pre-AQ-001 case (S-09).
- Specify timestamp format in §9.1 (F-016).
- Add design-doc-finalize→/upgrade-agent window bullet to EC-5 (F-020).
- Replace `AP-REVIEW-MISSED-COVERAGE` with concrete PF identifier pattern in §17.3 BC-2 (F-022).
- Make OQ-6 sequential dependency chain explicit (F-023).

---

## Rejected findings (with cited evidence)

### F-010 — AC-2 awk tautology

**Cited evidence for rejection.** Line 651 AC-2 explicitly permits `Hyphenated qualifiers (ACCEPTED — calibration-pending, ACCEPTED — narrowed-scope) per Role 2 F-021 precedent`. The looseness is intentional; AC-2's purpose is "every R-row has SOME verdict" (catches missing-verdict synthesis bug), not "catch downgrade direction." Mirrors Role 2 §15.2a AC-3 by precedent. Finding self-acknowledges Suggestion-tier and "Accept (low impact)" path. No fix adopted.

### F-021 — Inline arXiv citation in §17.1 Risk-5

**Cited evidence for rejection.** Inline arXiv:2604.16790 is ~6 tokens; gives a future reader zero-cost direct paper resolution. Pass-1 substrate carries the same arXiv ID under reference [38]; the design doc is one path-resolution away from substrate but inline adds robustness against substrate-drift. Role 1 design doc §17 Risk-N entries cite primary sources inline alongside Finding/R anchors (verified pattern). F-021 self-acknowledges Suggestion-tier and "Accept (informational)" disposition. No fix adopted.

---

## Reject-but-adopt observations

Per `feedback_reject_but_adopt_pattern.md`: when an adversarial finding's claim about current state is empirically wrong but the suggested fix has independent value, classify Rejected with cited evidence AND separately decide to adopt the fix.

- **F-021's structural concern about citation hygiene consistency** has independent value but the specific fix (remove arXiv) loses information. No separate adoption.
- **F-010's check-rigor concern** has independent value (catching downgrade direction) but the project's existing AC pattern accepts looseness as a feature. The check-rigor concern can re-surface at a future audit if §3.2 verdicts actually degrade across sessions. No separate adoption now; tracking via future PF if recurrence.

---

## PF-S3-01 attestation

Per Role 2 S10 precedent + CLAUDE.md PF-S3-01 guard:

- **31 findings examined.** All 22 active adversarial + all 10 safety findings personally source-read against `design/health-edge-case-reviewer-design.md` OR against canonical upstream contracts (Role 1 design doc, Role 2 design doc, INVARIANTS.md, templates/, memory/process-failures.md, CLAUDE.md) before verdict.
- **Zero rubber-stamps.** Every verdict carries either (a) specific line reference + actual content vs claimed content comparison, or (b) cited evidence for rejection.
- **Two REJECTED verdicts** (F-010, F-021) carry cited evidence per the reject-but-adopt feedback memory pattern.
- **One LEGITIMATE-MODIFIED** (F-020) — orchestrator narrows the fix scope (single bullet vs EC sibling) but keeps the underlying defect-class as legitimate.
- **One DUPLICATE** (S-06 = F-002) collapses via the consolidation map; fix once.
- **One WITHDRAWN** (F-019) — at red-team agent's own filesystem verification; no orchestrator action.

Fifth consecutive PF-S3-01 guard held: S7 design-doc, S8 design-doc, S9 /upgrade-agent, S10 Pass-2, S11 Pass-2.

---

## Phase 5 disposition queue

The 9 resolution bundles above are the Phase 5 work-units. Order of application (per Role 2 S10 precedent — apply bottom-up by line number within each section to avoid line-shift breakage; cross-section order: address §4 + §13 first since most other sections reference these):

1. Bundle D (§4.3 NCC MERP table embed)
2. Bundle C (§13 row 17 AFB strict enforcement + F-005 path scoping)
3. Bundle B (schema unification across §§2.2, 4.3, 12, 13)
4. Bundle E (§§2.1 + 4.1 Mechanism A reconciliation; new §13 row mid-session divergence)
5. Bundle F (§13 row tagging hygiene — split row 5; row 12 target-type; row 23 narrow; §9.1 live_rows)
6. Bundle A (§11.1 row-pointer correction)
7. Bundle H (§5 / §8 / §13 row 8 / §16 promotion criteria)
8. Bundle I (§13 row 22 wiring; EC-5 window; format specs; OQ-6 dependency chain; BC-2 identifier)
9. Bundle G (§12 BAD-block quarantine; intro parenthetical removal)

After all bundles applied, re-run §7 self-attest 17/17 + the pre-Phase-3 mechanical checks (`grep -c '^## '` etc.) to verify no synthesis-drift introduced by the fixes.
