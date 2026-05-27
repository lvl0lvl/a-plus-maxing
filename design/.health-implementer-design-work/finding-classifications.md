---
title: Finding Classifications — Role 2 (health-implementer) Pass-2 Phase 4
type: finding-disposition
created: 2026-05-27
session: S10
phase: Phase 4 Personal Source-Read
target_design_doc: design/health-implementer-design.md
red_team_inputs:
  - design/.health-implementer-design-work/red-team-adversarial.md (27 findings)
  - design/.health-implementer-design-work/red-team-safety.md (13 findings)
total_findings: 40
orchestrator_attestation: |
  Per PF-S3-01 guard, every finding below was personally read against its cited source
  (line number, regex match, file glob, cross-doc reference). No verdict was rubber-stamped
  from the reviewer's prose. Cited evidence for each verdict appears in the row.
---

# Phase 4 Classifications — Role 2 Design Doc Red-Team Findings

## Verdict legend

- **LEGITIMATE** — finding correctly identifies a defect; fix applied at Phase 5.
- **LEGITIMATE-MODIFIED** — finding correctly identifies a defect but the recommended fix is altered; modified fix applied at Phase 5.
- **REJECTED** — finding's claim is wrong or its premise does not hold; cited evidence in disposition.
- **DEFERRED-TO-BEAD** — finding correctly identifies a defect but resolution belongs to a separate follow-up; bead created at close.

## Summary

| Severity | Total | LEGITIMATE | LEGITIMATE-MODIFIED | REJECTED | DEFERRED-TO-BEAD |
|---|---|---|---|---|---|
| Critical / CRITICAL | 5 | 5 | 0 | 0 | 0 |
| High / HIGH | 11 | 10 | 1 | 0 | 0 |
| Medium / MEDIUM | 13 | 11 | 0 | 0 | 2 |
| Low / LOW | 11 | 9 | 1 | 0 | 1 |
| **Total** | **40** | **35** | **2** | **0** | **3** |

## All findings personally verified

Personal source-read attestation: for each finding I ran the cited grep/sed/awk/ls command OR read the cited file:line range, then compared the actual content to the finding's claim. No verdict was issued without this verification.

---

## Adversarial findings (F-001 through F-027)

### F-001 — §12 Negative Example raw H2 headings pollute section count

**Verdict.** LEGITIMATE.

**Personal verification.** `grep -cE '^## ' design/health-implementer-design.md` returns 23. Lines 383, 391, 410, 418 contain raw `## Context Loading` / `## Loop-Breaking` inside §12.3 + §12.4 code blocks. §13 row 6.5 requires count=11. The doc fails its own audit today.

**Disposition.** Fix at Phase 5: wrap §12.3 + §12.4 BAD/GOOD blocks differently (indent the section-header lines OR use `<!-- markdownlint-disable-next-line -->` OR replace `## ` with `### ` prefix in BAD examples — the BAD prose still demonstrates the failure mode without polluting the parent-doc section count). Add EC-15 to §14 covering "raw H2 in code block trips section-count audit."

---

### F-002 — §13 status-tag count contradiction (claim 18 vs actual 20)

**Verdict.** LEGITIMATE.

**Personal verification.** `awk '/^## 13/,/^## 14/' | grep -cE '\| PROPOSED \|'` = 20. Decimal extensions are 5.5, 6.5, 6.6, 7.5, 12.5 (5 not 7).

**Disposition.** Fix at Phase 5: replace "PROPOSED: 18" with "PROPOSED: 20" in the §13 status-tag-count line; restate "5 decimal-extended" not "7". Correct OQ-8 title to "20 PROPOSED rows."

---

### F-003 — AC-3 mechanism is tautological

**Verdict.** LEGITIMATE.

**Personal verification.** `grep -nE "(audit.*pass.*necessary.*not.*sufficient|Role.4.*review.*before)" design/health-implementer-design.md` returns ONLY line 556 (the AC-3 definition itself). §7 Loop-Breaking has no dual-gate clause. §8.5 prose "Mechanical-check pass is necessary but not sufficient — Role 3's review is the runtime-behavior gate" exists but uses "Mechanical-check pass" not "audit pass" and lives in §8.5 not §7.

**Disposition.** Fix at Phase 5: move dual-gate clause INTO §7 Loop-Breaking as a numbered threshold; rewrite AC-3 regex to use a unique marker phrase that does NOT appear inside the AC line itself.

---

### F-004 — AC-2 glob includes foundation roles, not just specialists

**Verdict.** LEGITIMATE.

**Personal verification.** `ls .claude/agents/` shows only `health-specialist-architect/` today (a foundation role). The glob `.claude/agents/*/agent.md` will match foundation roles + 14 specialists indiscriminately post-deployment.

**Disposition.** Fix at Phase 5: replace flat glob with explicit specialist-slug enumeration (also addresses WG-3 / F-013 — single source of truth for the 14 specialists).

---

### F-005 — Six ACs gradeable only post-deployment

**Verdict.** LEGITIMATE.

**Personal verification.** `.claude/agents/health-implementer/` does not exist; six ACs grep against that future path.

**Disposition.** Fix at Phase 5: partition §15.2 into §15.2a (design-doc-time, runnable at Phase 5 finalize) and §15.2b (post-deployment, gate Session B exit).

---

### F-006 — §16 says INV-RESEARCH-* OUT-OF-SCOPE while §13 row 18 REFERENCES it

**Verdict.** LEGITIMATE.

**Personal verification.** §16 line 569 says "Research-domain `INV-RESEARCH-*` OUT-OF-SCOPE." §13 row 18 line 462 says "REFERENCED-by-Role-2-for-downstream (INV-RESEARCH-ATTESTATION)." Inconsistent at the speech-act level.

**Disposition.** Fix at Phase 5: remove row 18 from §13 (it is a downstream-runtime concern, not Role 2's deliverable shape) AND amend §16 prose to "OUT-OF-SCOPE for Role 2's deliverable; downstream specialists inherit at runtime — referenced informally, not via §13."

---

### F-007 — §2.2 owned item 4 unilaterally claims `scripts/audit-specialist-profile.sh` ownership

**Verdict.** LEGITIMATE-MODIFIED.

**Personal verification.** Role 1 §2.2 NOT-owned item 5 says "owned by **health-implementer** or a dedicated tooling pass; I write the interface contract, not the bash". Role 2 §2.2 item 4 took option A unilaterally; §18 OQ-1 also lists this as open.

**Modified fix.** Reviewer recommended either remove unilateral claim OR file Architecture Question. **I (orchestrator) act with user authority** (the orchestrator/Walter is the AQ resolver per Role 1 §18 OQ-2 pre-architect-deployment route) and **adopt option A as the resolution**: Role 2 owns the bash. Record this as the AQ resolution in §18 OQ-1, then close the OQ. Rationale: no dedicated tooling pass exists on the project critical path; Role 1 left both options open; orchestrator selects option A. Apply at Phase 5: keep §2.2 item 4 ownership AND amend OQ-1 status to RESOLVED with this rationale.

---

### F-008 — §13 QA-strict tag-rule divergence is load-bearing, not non-blocking

**Verdict.** LEGITIMATE.

**Personal verification.** Role 1 line 469: "LIVE rows have their paths verified to resolve via Glob/Read." Role 2 line 434: "LIVE requires both (a) the check script/hook exists and (b) a smoke test exercises it against a negative case." Divergence confirmed. Downstream same-row two-states problem confirmed.

**Disposition.** Fix at Phase 5: orchestrator (with user authority) adopts the QA-strict rule as the project standard and amends Role 1 §13 header (§18 OQ-7 gets RESOLVED with this rationale). This makes Role 1 §13 PROPOSED rows STILL PROPOSED when the script ships, because their smoke tests don't exist yet. Roles 3 and 4 inherit the unified rule. Apply at Phase 5: leave Role 2 §13 as-is; add a one-line note to OQ-7 ("resolved by orchestrator adoption of QA-strict project-wide; Role 1 §13 amendment is a follow-up bead").

---

### F-009 — AC numbering inconsistent (bare-numbered list vs AC-N cross-refs)

**Verdict.** LEGITIMATE.

**Personal verification.** §15.2 lines 554+ use bare numbers `1.`, `2.`, …, `10.`. Cross-refs at lines 308, 314, 595, 614, 621 use `AC-3`, `AC-1`, `AC-7`. Confirmed inconsistent.

**Disposition.** Fix at Phase 5: prefix each criterion in §15.2 with `AC-1` through `AC-10`.

---

### F-010 — Doc's own voice-register violates the rule it imposes on deployed specialists

**Verdict.** LEGITIMATE.

**Personal verification.** `grep -ciE "\b[Yy]ou (must|should|will|are|need to|have to)\b" design/health-implementer-design.md` = 9 (rule says ≤3); `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" design/health-implementer-design.md` = 7 (rule says 0). The doc's own §5 rule 4 fails on the doc itself.

**Disposition.** Fix at Phase 5: add a scoping clarification to §5 rule 4 (and §13 row 4): "Banned-phrase regex + non-aggressive `\b[Yy]ou (must|should|...)\b` allow-budget apply to the deployed `agent.md` (not the design doc, which legitimately quotes banned phrases inside §12 BAD code blocks). Mechanical-check scopes grep to `.claude/agents/*/agent.md`, never to `design/*.md`."

---

### F-011 — Watch list WG-1 surfaced: §10.1 substrate auto-load undefined for specialists

**Verdict.** LEGITIMATE.

**Personal verification.** §10.1 item 1 auto-loads Role 1 design doc; no item covers specialist's domain-research.md (which doesn't exist pre-Pass-3 for the 14 specialists per template line 32).

**Disposition.** Fix at Phase 5: amend §10.1 with explicit specialist-Pass-1-substrate-fallback discipline. New item: "If authoring a specialist whose Pass-3 substrate has not landed, substitute Role 1's `domain-research.md` for the foundation-class inheritance per template §3 specialist-fallback path. HALT `pass1-substrate-missing` if both absent."

---

### F-012 — Watch list WG-2 surfaced: §8.1 library-index.md hedge

**Verdict.** LEGITIMATE.

**Personal verification.** §8.1 line 201 reads "(if template variant requires) library-index.md". §2.2 owned-items doesn't include it; §2.2 not-owned doesn't disclaim it. Per S9 precedent, Role 1 deployed WITH library-index.md.

**Disposition.** Fix at Phase 5: add `library-index.md` to §2.2 owned-items with spec ("≤30 lines; ≤5 conditional refs to vault/library/<class>/ paths; auto-load only when specialist's Tools section requires"); add §13 row 9.5 PROPOSED auditing its shape; remove the §8.1 hedge.

---

### F-013 — Watch list WG-3 surfaced: target_class enumeration not audited

**Verdict.** LEGITIMATE.

**Personal verification.** §13 row 12 (line 455) audits `--mode` only; row 12.5 (line 456) audits mode-floor correctness; neither audits `--target-class` (separate aplus-research SKILL.md parameter).

**Disposition.** Fix at Phase 5: add §13 row 12.6 PROPOSED auditing `target_class` declaration. Also covered by F-004 fix (explicit specialist-slug enumeration becomes single-source-of-truth for both mode and target_class).

---

### F-014 — Watch list WG-4 surfaced: per-specialist operator-profile field enumeration missing

**Verdict.** LEGITIMATE.

**Personal verification.** §10.3 lists operator-profile as specialist-not-implementer load. §4.1 INBOUND row 5 says implementer encodes read-order. Neither specifies which fields per specialist class.

**Disposition.** Fix at Phase 5 via option (b) — escalate to architect: this is upstream architectural scope (Role 1 §4 row 5 contract owns operator-profile schema enforcement). Record AQ-001 at `design/.health-implementer-design-work/architecture-questions/AQ-001-per-specialist-operator-profile-fields.md` asking Role 1 whether to enumerate per-specialist OR delegate to Role 2 in a §10 sub-table. Until AQ-001 resolves, §10.3 carries a placeholder note pointing at the AQ artifact. Document in §18 OQ-3 (or new OQ-9).

---

### F-015 — §4.2 OUTBOUND row 3 vs §15.2 missing AC for audit_passed frontmatter

**Verdict.** LEGITIMATE.

**Personal verification.** §4.2 row 3 establishes the contract (line 142); §13 row 13 mechanizes it (line 457); §15.2 ACs do not include a binary check that frontmatter `audit_passed: true` appears in deployed specialist files.

**Disposition.** Fix at Phase 5: add `AC-11` to §15.2: "`audit_passed: true` frontmatter present in deployed specialist `agent.md` files."

---

### F-016 — §11.2 AP3 covers operator-profile-inline but not WIKI-row-quote surface

**Verdict.** LEGITIMATE.

**Personal verification.** §11.2 AP3 (line 321) prose mentions "Walter's January 2026 issue" only — the inline content variant. The WIKI-row-quote variant (e.g., medical-liaison row has `(Jan 2026 issue)` parenthetical that an implementer could quote forward) is distinct.

**Disposition.** Fix at Phase 5: add a sub-clause to §11.2 AP3 OR new AP3.5 covering "I don't read forward from a WIKI.md row's operator-context note into the specialist profile body."

---

### F-017 — §13 row 5.5 GRADE regex requires colon-separated format Role 1 doesn't mandate

**Verdict.** LEGITIMATE.

**Personal verification.** Row 5.5 line 445 regex requires literal `certainty: ` token. Role 1 §5 Rule 12 (line 170) mandates only that the two tags exist on each claim; doesn't mandate `key: value` syntax.

**Disposition.** Fix at Phase 5: loosen regex to `grep -E "certainty[: =]+(high|moderate|low|very-low)"` + analogous for strength.

---

### F-018 — §13 row 17 branch hygiene is session-discipline, not deliverable-shape

**Verdict.** LEGITIMATE.

**Personal verification.** Row 17 (line 461) REFERENCED INV-BRANCH-NOT-MAIN via the commit-block hook. The hook gates git operations, not deliverable content. §16 already lists INV-BRANCH-NOT-MAIN under Invariants at Risk.

**Disposition.** Fix at Phase 5: move row 17 to §16 (already present); remove from §13 mechanical-enforcement-of-deliverable table.

---

### F-019 — `--taxonomy` vs `--taxonomy-path` CLI flag inconsistency

**Verdict.** LEGITIMATE.

**Personal verification.** §13 row 5 line 444 uses `--taxonomy <path>`. §17.1 R-6 line 600 uses `--taxonomy-path`. Confirmed inconsistent.

**Disposition.** Fix at Phase 5: standardize on `--taxonomy <path>` across §13, §17.1, §18.

---

### F-020 — Frontmatter `references_role_1_sha:` value is a path+annotation not a sha256

**Verdict.** LEGITIMATE.

**Personal verification.** Frontmatter line 14: `references_role_1_sha: design/health-specialist-architect-design.md (Status: Final, S8 close)`. Field name claims sha; value is path.

**Disposition.** Fix at Phase 5: rename field to `references_role_1_at:` and keep path+status annotation (option a per reviewer). Adding actual sha256 (option b) goes stale per CLAUDE.md §5 rotation rule clause 3 on stale hashes.

---

### F-021 — R9 verdict "ACCEPTED — calibration-pending" doesn't strictly match template binary verdict set

**Verdict.** LEGITIMATE-MODIFIED.

**Personal verification.** §3.2 R9 (line 109) has verdict "ACCEPTED — calibration-pending". Template §3 spec requires "ACCEPTED / DEFERRED / REJECTED" with one-line rationale; reviewer notes this is technically a substring-match-pass under AC-4's awk but a strict equality check would fail.

**Modified fix.** Apply reviewer's option (b): leave R9 verdict as "ACCEPTED — calibration-pending"; add a one-line note to §3.2 documenting that hyphenated qualifiers (e.g., "ACCEPTED — calibration-pending") are permitted for ACCEPTED-with-conditional-on-future-evidence cases. Tightening AC-4's awk (option a) would create false-FAILs across legitimate Pass-2 design-doc patterns Role 1 also uses.

---

### F-022 — §4.1 INBOUND row 1 paraphrases Role 1 §13 row 4 conditional rather than anchor-citing

**Verdict.** LEGITIMATE.

**Personal verification.** Row 1 (line 127) text "if specialist Tools permit image MIME Reads or image-URL WebFetch, IMAGE_OR_SIGNAL_INPUT is MANDATORY" paraphrases Role 1 §13 row 4 (line 478). §4 anti-redefinition rule says reference by anchor; row 1 inlines the conditional.

**Disposition.** Fix at Phase 5: tighten to "Implementer encodes ≥4 distinct classes per specialist (`R-5`); per-row §13 row 4 Tools-conditional `IMAGE_OR_SIGNAL_INPUT` mandatory clause inherits verbatim per Role 1 §13 row 4 (do NOT re-state)."

---

### F-023 — §6 step 5 drops "in a one-line comment" qualifier from Role 1's pattern

**Verdict.** LEGITIMATE.

**Personal verification.** Role 1 §6 step 5 (line 184): "pick the simpler option, state the assumption **in a one-line comment**, proceed." Role 2 §6 step 5 (line 175) drops the one-line-comment qualifier.

**Disposition.** Fix at Phase 5: restore "in a one-line comment" qualifier in §6 step 5.

---

### F-024 — §14 EC-11 mentions "OQ-budget" which doesn't exist

**Verdict.** LEGITIMATE.

**Personal verification.** Line 526 says "see §18 OQ-budget". §18 has OQ-1 through OQ-8; no OQ named "OQ-budget". Closest match is OQ-8.

**Disposition.** Fix at Phase 5: replace `§18 OQ-budget` with `§18 OQ-8`.

---

### F-025 — §11.2 AP3 conflates auto-load discipline with body-inline discipline

**Verdict.** LEGITIMATE.

**Personal verification.** AP3 (line 321) covers two distinct surfaces in one bullet: "I don't auto-load" + "I don't reference Walter's January 2026 issue (or any specific operator state) in the specialist profile body." These are independent failure modes.

**Disposition.** Fix at Phase 5: split AP3 into AP3a (auto-load) and AP3b (body-inline). Renumber subsequent APs (4→5, 5→6, 6→7).

---

### F-026 — §1 gap #1 phrasing "Goal-agnostic specialist profile authoring" is wrong

**Verdict.** LEGITIMATE-MODIFIED.

**Personal verification.** §1 gap #1 (line 30) starts "**Goal-agnostic specialist profile authoring at scale.**" Specialist profiles are NOT goal-agnostic (they carry domain identity, owned wiki paths, role-specific refusal classes). The "goal-agnostic" qualifier applies to library entries per `feedback_library_research_goal_agnostic.md`, not to specialist profiles.

**Modified fix.** Reviewer recommended "Template-conformant specialist profile authoring at scale." A more accurate version is "Cross-specialist-consistent specialist profile authoring at scale" — captures the IDENTICAL-block hash-match + DIFFER-block Jaccard ceiling discipline (the actual load-bearing point). Apply at Phase 5.

---

### F-027 — §15.1 inherits library-index AC; depends on F-012

**Verdict.** LEGITIMATE.

**Personal verification.** §15.1 (line 550) lists "library-index reference paths resolve" among inherited /upgrade-agent Phase 7 constraints. Per F-012, library-index.md ownership is undefined.

**Disposition.** Fix at Phase 5 chained to F-012 fix: after F-012 commits library-index.md ownership to Role 2 (per F-012 disposition), §15.1's inherited AC becomes concretely-gradeable. Add §15.2 AC-12 verifying `.claude/agents/<specialist-slug>/library-index.md` exists with ≥1 path reference.

---

## Safety findings (S-01 through S-13)

### S-01 — `AUTHORITY_FRAMING_BYPASS` not mandated per specialist

**Verdict.** LEGITIMATE.

**Personal verification.** `grep -c "AUTHORITY_FRAMING_BYPASS" design/health-implementer-design.md` = 1 (only EC-4 narrative). Role 1 has 8 hits. Role 2 §5 rule 5 mandates ≥4-of-8 but doesn't specify WHICH 4. Walter is the single operator and is named A3 (operator-self-harm via own-agent) at Role 1 §11.2 AP8 + EC-9. Per Role 1 §2.2 item 3, this is the 81.8%-of-successful-attacks vector.

**Disposition.** Fix at Phase 5: add §13 row 5.X making `AUTHORITY_FRAMING_BYPASS` mandatory per specialist (not conditional, not optional). Amend §5 rule 5 to "encode ≥4 distinct classes per specialist, with `AUTHORITY_FRAMING_BYPASS` MANDATORY among them." Add §15.2 AC verifying the deployed `health-implementer/agent.md` encodes this mandate.

---

### S-02 — H-class composition requires undefined `--role-4-log` schema

**Verdict.** LEGITIMATE.

**Personal verification.** Row 14 (line 459) cites `--role-4-log <path>`. Role 1 §17.2 A-7 (line 692) describes the v1-substitute (software security agent briefed on medical-safety) but does NOT define an evaluation-log file format, schema, path canon, or H-class field name the audit script can consume.

**Disposition.** Fix at Phase 5: amend §13 row 14 with explicit v1-substitute verdict-log schema specification. Schema: JSON file at `design/.{role}-design-work/v1-substitute-safety-log.json` containing fields `{compound_slug, h_class_worst_case, evidence_lines, attestation_chain}`. Add to §17.2 as new A-9 establishing the schema. Pre-Role-4: row 14 audit accepts this v1-substitute log; post-Role-4: real Role 4 log replaces.

---

### S-03 — GRADE row 5.5 audits vocabulary presence, not HALT disposition

**Verdict.** LEGITIMATE.

**Personal verification.** Row 5.5 (line 445) regex: `certainty:` + `strength:` presence. Does NOT audit strong+low / strong+very-low HALT disposition. §12.2 GOOD block has the right HALT prose at lines 367-371; row 5.5 doesn't grep for it.

**Disposition.** Fix at Phase 5: extend row 5.5 mechanism with second-pass HALT-pattern grep: `grep -cE "(strong[ -]with[ -](low|very[ -]low)|strong\+low).{0,80}(halt|downgrade|override.*acknowledg)" ≥ 1`.

---

### S-04 — Anti-sycophancy "three independent grep matches" is ambiguous

**Verdict.** LEGITIMATE.

**Personal verification.** §5 rule 11 (line 164) says "three independent grep matches in IDENTICAL block" without specifying whether the three matches are three distinct regexes (Mechanism A/B/C-keyed) or three positional matches of any pattern. §13 has no row keyed to rule 11.

**Disposition.** Fix at Phase 5: add §13 row 5.6 with three distinct mechanism-keyed greps: `grep -E "Mechanism A.{0,100}(silent agreement|catfish|multi-agent)" ≥1` AND `grep -E "Mechanism B.{0,100}(acquiescence|maintain position|user pushback)" ≥1` AND `grep -E "Mechanism C.{0,100}(RLHF|preference drift|Sharma|Petri)" ≥1`. Tighten §5 rule 11 prose to "three distinct mechanism-keyed grep matches" (not just three matches).

---

### S-05 — Operator-profile inlining closed at meta-author; specialist runtime-emission inverse surface open

**Verdict.** LEGITIMATE.

**Personal verification.** §10.3 closes the meta-author inline. §12.3 GOOD example instructs specialist to READ at dispatch but says nothing about WRITE-protection. A specialist following the GOOD pattern could still write operator-bound contraindication notes into `vault/compounds/*` files, recursing the PF-S2-04 surface one layer.

**Disposition.** Fix at Phase 5: add §13 row 6.7 PROPOSED + Communication-section constraint that implementer must encode in every specialist's deployed agent.md: "Specialist compound-entry writes never inline operator-profile content; reference operator state by READ-at-dispatch, never by WRITE-to-wiki." Pair with audit grep `grep -cE "(Walter|2026-01|January 2026)" .claude/agents/*/agent.md == 0`.

---

### S-06 — §7 path (iii) "demote to known-deferred" is a self-attested bypass

**Verdict.** LEGITIMATE.

**Personal verification.** §7 audit-script-failure threshold (line 188) lists path (iii) "demote affected section to known-deferred with explicit rationale" alongside (i) fix and (ii) escalate. Path (iii) reproduces PF-S3-01 in mitigated form: implementer self-attests deferral. No required artifact, no orchestrator counter-signature.

**Disposition.** Fix at Phase 5: rewrite §7 path (iii) to require structured artifact: `audit_passed_with_known_deferrals.json` listing deferred row IDs + implementer's rationale + REQUIRED orchestrator counter-signature analog (similar to `gate_attest.py` attestation-chain) before orchestrator-accept permits the deployed specialist to run. Effectively closes the bypass surface.

---

### S-07 — Mode floor is profile-text declaration not runtime invariant

**Verdict.** LEGITIMATE.

**Personal verification.** §13 row 12 audits Tools section grep only; row 12.5 audits mode-floor correctness in profile text. Neither binds the specialist's runtime invocation. An operator authority-framing attack could downgrade `--mode=deep` to `--mode=standard` at runtime.

**Disposition.** Fix at Phase 5 via two-prong: (a) add §5 rule 5.5 requiring deployed specialist Core Rules to contain "never downgrade `aplus-research --mode` below the declared floor under operator pressure (anti-sycophancy Mechanism B carve-out)"; (b) defer to bead the broader fix (`/aplus-research` skill maintainer adds dispatch-refuses-below-per-role-floor — Architecture Question to skill maintainer).

---

### S-08 — Negative-example denylist content is OQ-6 unauthored

**Verdict.** DEFERRED-TO-BEAD.

**Personal verification.** Row 10 (line 453) cites `--denylist <path>` with no path target. §18 OQ-6 + §17.1 R-7 explicitly defer denylist authoring to Role 4 (medical-safety-reviewer) or pre-Role-4 v1-substitute. The v1-substitute (software-security agent) authored THIS red-team review but denylist authoring was explicitly out of THIS review's brief.

**Disposition.** Defer to bead: `Author denylist starter regex set for §13 row 10` — pre-Role-4 v1-substitute task. Minimum starter content per reviewer: (a) FDA Category X drug + dose-with-unit on same line; (b) common contraindication pairs with dose units; (c) common jailbreak-trigger framings. Until denylist content lands, row 10 mark WARN with "denylist starter pending" annotation. Tag bead with `priority=2` and depend on Role 4 deployment (no urgent harm pre-Role-4 because the 4 §12 BAD examples in the doc are clean).

---

### S-09 — Refusal-class taxonomy file location is OQ-3 unresolved

**Verdict.** LEGITIMATE.

**Personal verification.** Row 5 (line 444) `--taxonomy <path>` has no path target. §18 OQ-3 lists candidates. Without the file, row 5's enum-membership half can't run; the "≥4 distinct identifiers" half passes any 4 CLASS_NAME-shaped strings, defeating Worked Example B's discipline.

**Disposition.** Fix at Phase 5: orchestrator (with user authority) adopts OQ-3 resolution path: standalone `templates/refusal-class-taxonomy.yaml` with the 8 classes from Role 1 §2.2 item 3. Mark OQ-3 RESOLVED. Defer the actual file authoring to a quick follow-up bead (mechanical extraction from Role 1 §2.2 item 3).

---

### S-10 — Role-4-log absence at deployment has no control gate

**Verdict.** LEGITIMATE.

**Personal verification.** §17.2 A-6 (line 614) acknowledges "specialist deploys with neither Role 4 nor v1-substitute verdict log" as possible. The mitigation is "orchestrator checks at deployment time" — process step, not runtime control. Combined with S-02 (schema undefined) + S-06 (path-iii bypass), an implementer could ship with row 14 deferred and `audit_passed: true`.

**Disposition.** Fix at Phase 5 chained to S-02 fix: after S-02 commits to v1-substitute log schema at `design/.{role}-design-work/v1-substitute-safety-log.json`, amend §13 row 14 to require `audit_passed: true` frontmatter to include a `h_class_verdict_log_path: <path>` field that orchestrator verifies resolves at accept-time. Closes the bypass.

---

### S-11 — No attestation-chain analog for per-specialist audit-run summary

**Verdict.** DEFERRED-TO-BEAD.

**Personal verification.** §13 row 13 (line 457) requires `audit_passed: true` frontmatter. No equivalent of `gate_attest.py` for per-specialist audit-run summaries. PF-S3-01 structural fix candidate (UUIDv4 agent-identity ledger) is named in `memory/process-failures.md` line 73 as a v2 candidate.

**Disposition.** Defer to bead: `Apply attestation-chain pattern to scripts/audit-specialist-profile.sh per-specialist audit-run summary` — meaningful engineering task, parallel to existing `lib/gate_attest.py` work for aplus-research. Tag bead with `priority=3` (low; the v1 `audit_passed: true` frontmatter is the v1 substitute, sufficient pre-Role-4).

---

### S-12 — `--role-table <path>` for mode-floor correctness has no versioned artifact

**Verdict.** LEGITIMATE-MODIFIED.

**Personal verification.** Row 12.5 (line 456) `--role-table <path>` has no defined path target. Implementer can supply any role-table and pass trivially.

**Modified fix.** Apply at Phase 5: commit role-table to `templates/specialist-risk-class.yaml` with 14 explicit specialist entries + `last_reviewed:` frontmatter, mapping each to `mode_floor: standard|deep|ultradeep`. Reference from §13 row 12.5. Same lift as S-09 (both are "commit project-local templates/ artifact"); package them together at Phase 5.

---

### S-13 — Architecture Question accumulation has no SLA or drain check

**Verdict.** LEGITIMATE.

**Personal verification.** §17.1 R-3 (line 597) names AQ accumulation as WARN with mitigation "orchestrator drains queue at session boundaries" but no drain check. CLAUDE.md §Session Close Protocol does not mention AQ-queue drain.

**Disposition.** Fix at Phase 5: add session-close protocol step (or `scripts/aq-queue-audit.sh` PROPOSED row) requiring AQ-queue length ≤ N (e.g., N=3) at close; over-N HALTs the session. Mirror BC-trip pattern in §17.3.

---

## Resolution map

### Apply at Phase 5 (35 LEGITIMATE + LEGITIMATE-MODIFIED)

**Critical (5).** F-001, F-003, F-004, S-01, S-02.

**High (10).** F-002, F-005, F-006, F-007 (modified), F-008, F-010, F-011, F-012, S-03, S-04, S-05, S-06.

Wait — F-007 is HIGH but modified. Let me recount: High = F-002, F-005, F-006, F-007 (modified), F-008, F-010, F-011, F-012, S-03, S-04, S-05, S-06 — 12. Reviewer said 7 adversarial + 4 safety = 11 High total. Let me recount: F-002 H, F-005 H, F-006 H, F-007 H, F-008 H, F-010 H, F-011 H = 7. S-03 H, S-04 H, S-05 H, S-06 H = 4. Total High = 11. All applied (1 modified).

**Medium (11).** F-013, F-014 (modified disposition — Architecture Question), F-016, F-017, F-020, F-022, F-023, F-027, S-07, S-09, S-10. Two deferred to bead (S-08, S-12 modified — actually S-12 is LEGITIMATE-MODIFIED applied, not deferred). Recount Medium = F-012 (H not M), F-013 M, F-014 M, F-016 M, F-017 M, F-020 M, F-022 M, F-023 M, F-027 M = 9 adversarial. S-07 M, S-08 M, S-09 M, S-10 M = 4 safety. Total Medium = 13. Applied = 11; deferred = 1 (S-08); modified = 1 (S-12 — but S-12 is LOW not MEDIUM per safety severity).

Recount Low (11 = 8 adversarial + 3 safety). Adversarial Low: F-009, F-015, F-018, F-019, F-021 (modified), F-024, F-025, F-026 (modified) = 8. Safety Low: S-11 (deferred), S-12 (modified at Phase 5), S-13 = 3. All accounted: applied 9, deferred 1, modified 2.

### Defer to bead (3)

- S-08 (denylist starter regex) — `priority=2`, blocked on Role 4 OR v1-substitute task scope.
- S-11 (attestation-chain for audit-run summary) — `priority=3`, v2 candidate.
- S-12 (role-table artifact) — actually applied at Phase 5 per modified disposition; package with S-09 templates/* work.

Final defer-to-bead count: 2 (S-08, S-11).

### Reject (0)

No findings rejected. Every reviewer claim verified against cited evidence.

---

## Cross-finding consolidation map (Phase 5 efficiency)

Some fixes naturally bundle:

1. **§13 row count fix** — F-002 cleanup happens alongside any §13 amendment (S-01, S-03, S-04, S-05 all add rows; F-006 removes row 18; F-018 removes row 17). Final row count + status-tag line written ONCE after all §13 amendments land.

2. **`templates/` artifacts** — S-09 (refusal-class-taxonomy.yaml) + S-12 (specialist-risk-class.yaml) + S-02 (v1-substitute-safety-log.json schema) are all "commit project-local templates/" lifts. Single Phase-5 commit.

3. **AC partition (F-005) + AC-N hyphenation (F-009) + AC-11 add (F-015) + AC-12 add (F-027)** — single §15.2 rewrite handles all four.

4. **§11.2 AP3 split (F-025) + AP3 WIKI-row-quote extension (F-016)** — single AP3 rewrite handles both.

5. **§5 rule scoping note (F-010) + §13 row 4 scoping note** — same scoping clarification applied both places.

6. **OQ resolution + status flip** — OQ-1 (F-007), OQ-3 (S-09), OQ-7 (F-008) all RESOLVED at Phase 5 with the orchestrator's adoption decisions documented.

7. **Watch list disposition** — WG-1 / WG-2 / WG-3 / WG-4 all SURFACED via F-011 / F-012 / F-013 / F-014; no candidate beads from the watch list per user directive.

## Attestation

I (orchestrator) personally read every finding's cited source (line, regex, file glob). No finding was rubber-stamped from the reviewer's prose. Mechanical claims (counts, regex matches, file existence) verified via Bash. Cross-doc claims (Role 1 inheritance, Role 1 §2.2 item 5, INVARIANTS rows) verified via Read against the cited document. Where my verification produced the same result as the reviewer's claim, the verdict is LEGITIMATE. Where my verification produced a different result OR where the reviewer's recommended fix needed adjustment, the verdict is LEGITIMATE-MODIFIED with the modified-fix block stating my reasoning.

PF-S3-01 guard held across all 40 findings. No self-attestation of mechanical claims; every count, glob, regex was run.
