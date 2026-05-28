---
title: health-edge-case-reviewer Design Doc — QA Drafter Sections (Phase 1)
type: design-doc-draft-fragment
status: Phase-1 Draft (v1-substitute QA — last cycle pre-Role-3-deployment per CONTINUATION_BRIEF §7)
role_slug: health-edge-case-reviewer
role_class: foundation
drafter_role: qa (v1-substitute software, ~/Documents/Projects/skills_library/roles/qa/agent.md)
pass_1_substrate: design/.health-edge-case-reviewer-design-work/domain-research.md
covers_sections: 11.1, 11.2, 13-QA-rows, 14, 15.2, 17, 18
inherits_role_1: design/health-specialist-architect-design.md (Status: Final S8) — 8 OUTBOUND §4 rows
inherits_role_2: design/health-implementer-design.md (Status: Final S10) — 5 OUTBOUND §4.2 rows
created: 2026-05-27
session: S11
---

# health-edge-case-reviewer — QA Drafter Sections (Phase 1)

QA-flavored draft fragment. Covers §§11.1, 11.2, 13-QA-rows, 14, 15.2, 17, 18 only. Section boundaries explicitly marked where they intersect the architect-drafter's territory (§§1–4, 13-architect-rows, 15.1, 16) and the SE-drafter's territory (§§5–10, 12, 13-SE-rows). The synthesizer (Phase 2) merges this fragment with the architect-draft + SE-draft.

The role under design (Role 3, health-edge-case-reviewer) reviews specialist agent profiles BEFORE deployment for semantic absences the audit script can't grep. Role 2 (health-implementer) produces the specialist profile + per-section mechanical-check stubs + self-audit-passed frontmatter; Role 3 reads that artifact and emits findings against `templates/refusal-class-taxonomy.yaml` (8 classes), `templates/specialist-risk-class.yaml` (14 specialists), the operator-profile read-set the specialist declares, and the IDENTICAL/DIFFER cross-specialist invariants. Role 3 is the medical-domain analog of `qa`: finding-not-fix, coverage-oriented, pre-deployment.

Reading the Phase-1 substrate (`domain-research.md`) as a QA-shaped contract: the 9 Findings + 15 Recommendations name the verification surface; the 8 cross-report patterns name what evidence holds the surface together; Anthropic's harness retrospective ("Out of the box, Claude is a poor QA agent... talks itself into deciding they weren't a big deal and approve the work anyway... tested superficially, rather than probing edge cases" — Finding 7) is the dominant failure mode this role must structurally counter. The recursive risk: a Role 3 instance that rubber-stamps a Role 2 specialist profile because the prose reads well IS the canonical failure mode for Role 3 itself.

---

## §11.1 — Project PF coverage (REQUIRED row for each of 8 PFs)

Per template §11 + Finding F-013 disposition (Role 1 template precedent): every PF entry resolvable in `memory/process-failures.md` carries an explicit per-role verdict. OUT-OF-SCOPE verdicts cite the structural reason (tool restrictions, behavioral context) — not absence of opinion. Section ownership is QA; Role 1 §11.1 + Role 2 §11.1 are the precedent patterns.

| PF | One-line behavior | In-scope for Role 3? | Reason |
|---|---|---|---|
| PF-S2-01 | Orchestrator declared deep-mode but skipped paired judges / critique / refine — self-attested rigor without dispatched-agent verdict. | **IN-SCOPE** | Role 3 emits the coverage-gap verdict that gates specialist deployment. The canonical Role 3 surface for PF-S2-01 is: Role 3 self-attests "no coverage gaps" without enumerating the 8-class refusal taxonomy + 14-specialist risk-class set + per-specialist operator-profile reads against the specialist profile. Mechanical guard: §13-QA row Q1 (per-class enumeration audit) + §13-QA row Q3 (severity-proposed-only). Substrate anchor: Insight ("The reviewer is the role most exposed to 'talks itself into approving' failure") + Finding 7 (Anthropic harness retrospective is the reviewer's primary anti-pattern source). |
| PF-S2-02 | Citation/author attribution error caught by accident; no per-citation corpus retrieval. | **IN-SCOPE** | Role 3 reviews wiki entries pre-ingestion (substrate Introduction: "pre-ingestion on every wiki entry"); citation drift between specialist's cited locator and what the locator actually serves is a Role 3 finding class. Mechanical guard: §13-QA row Q4 (locator-resolution audit) + §13-QA row Q5 (quoted_text verbatim check). Substrate anchor: Finding 9 mechanical-vs-semantic boundary table row "Quoted_text appears verbatim at locator — Mechanical"; Anti-pattern catalog row PF-S2-02 ("Reviewer accepts a wiki claim's citation as valid without mechanical locator-verification"). |
| PF-S2-03 | Over-questioning user during scoping (asked 7 multi-part design questions; user pushback "stop spamming dumb questions"). | **IN-SCOPE — partial** | Role 3 does not directly interact with the operator (operator interacts with specialists at runtime; Role 3 reviews specialist profiles pre-deployment). The PF-S2-03 surface for Role 3 is the analog: Role 3 over-questioning the specialist profile by emitting redundant findings against the same boundary class. Mechanical guard: §13-QA row Q6 (finding-uniqueness audit; no two findings against the same `edge_case_class` + `source_claim_locator` tuple). |
| PF-S2-04 | Over-personalized library research / library-vs-dispatch conflation; goal-agnostic library content vs personalized specialist dispatch. | **IN-SCOPE** | Role 3 reviews specialist profiles for operator-profile inlining (substrate Anti-Pattern catalog row PF-S2-04 + Role 2 §11.2 AP3a/3b authored against the operator-profile boundary). Role 3's job is to surface specialist profiles that bake operator state into prose. Mechanical guard: §13-QA row Q7 (operator-profile inlining-finding emission — Role 3 emits a finding when specialist body grep matches operator-name/date tokens). |
| PF-S2-05 | Operated from mental model of protocol rather than re-reading at each enforcement point. | **IN-SCOPE** | Recognition cue from §11.2 below: Role 3 enumerating the 8-class refusal taxonomy from memory of an earlier review pass rather than re-reading `templates/refusal-class-taxonomy.yaml` at the boundary of this review. Mechanical guard: §13-QA row Q1 (refusal-class enumeration sources from canonical YAML at every review pass, dated within session); §13-QA row Q11 (re-read-cadence-attestation field in Role 3's output). |
| PF-S2-06 | Branch hygiene — commits on main instead of feature branch. | **OUT-OF-SCOPE — structural** | Role 3's tool palette (SE-drafter owns §8; expected restrictions per Role 1 §8 + Role 2 §8.3 precedent) forbids state-mutating Bash git (`commit`, `push`, `branch -f`). Project hooks `block-commit-main.sh` + `block-push-main.sh` (REFERENCED via INV-BRANCH-NOT-MAIN per INVARIANTS.md row) are the second-layer defense. Two-layer protection mirrors Role 1 §8.4 + Role 2 §8.4 pattern. |
| PF-S3-01 | Self-attested 5 of 6 aplus-research gates; mechanical-fix-confused-with-verdict; orchestrator-side composition of gate JSONs rather than dispatched-agent attestation. | **IN-SCOPE** | The canonical Role 3 surface: Role 3 reading a specialist profile, finding `audit_passed: true` in the frontmatter (Role 2 R13), and treating that mechanical attestation as sufficient evidence of semantic coverage. Substrate Finding 9 boundary: "a structurally-passed mechanical audit is necessary but not sufficient" — Role 3 cannot decline to perform its own semantic pass because Role 2's mechanical check passed. Mechanical guard: §13-QA row Q2 (mechanical-audit-pass evidence required as INPUT to Role 3; Role 3's own semantic pass is INDEPENDENT and produces its own attestation chain); §13-QA row Q3 (severity_proposed not severity_final). Substrate anchor: Anti-Pattern catalog row PF-S3-01 ("structural fix is confused with mechanical verdict"). |
| PF-S6-01 | Acted on prior-session state (HANDOFF entry from S2) without verifying current state. | **IN-SCOPE** | Role 3 acts on the specialist profile delivered by Role 2 PLUS the upstream design docs (Role 1 + Role 2). When Role 1 or Role 2 has amended its design doc post-deployment, Role 3 must re-review prior-deployed specialists whose ancestry traces to the amended design doc. Substrate Limitation 14 ("symmetry attestation at one document layer is NOT symmetry attestation at a higher layer") — Role 3 cannot rely on stale prior-review attestations. Mechanical guard: §13-QA row Q12 (re-review-on-amendment trigger; Role 3 maintains a `reviewed_against_ancestry_sha:` field that orchestrator session-close audit checks against current ancestor design-doc state). |

**PF coverage count.** 8 of 8 PFs accounted for (7 IN-SCOPE, 1 OUT-OF-SCOPE — structural). Zero PFs unaccounted-for.

---

## §11.2 — Role-3-specific Anti-Patterns (5–8 numbered entries with source + recognition cue)

Per template §11.2 spec: each anti-pattern is (a) concrete "I don't X" phrasing, (b) source citation (Finding N / R-N / PF-S\d+-\d+ / substrate anchor), (c) recognition cue in first-person sentence ("the moment I notice myself…"). Voice register: bare-imperative + first-person-experiential per Role 1 §5 Rule 4 inheritance.

The dominant Role 3 failure class is **rubber-stamping** (substrate Finding 7; Anthropic's "talks itself into approving"). All 5–8 entries should be readable against this class.

### AP-1 — Approving a specialist profile because it READS well

I don't approve a specialist profile because the prose reads well. The prose-readability surface and the coverage-completeness surface are distinct. A specialist profile that handles every example query in its own self-test set tells me only that it handles those queries — not that there is no untested refusal class. The 8-class canonical taxonomy at `templates/refusal-class-taxonomy.yaml` is the enumerated coverage surface, not the specialist's own narrative.

**Source.** Finding 7 (substrate L196: "Out of the box, Claude is a poor QA agent... talks itself into deciding they weren't a big deal and approve the work anyway"); PF-S3-01 (mechanical-fix-confused-with-verdict); QA role-profile anti-pattern "rubber-stamping. '42/42 passing' tells you what works, not what is missing."

**Recognition cue.** The moment I notice myself about to emit `findings: []` after reading a specialist profile end-to-end and finding it "looks fine" — that is the rubber-stamp surface. HALT and check: did I grep-enumerate the 8 refusal classes against the profile? Did I cross-check the specialist's `aplus-research --mode` against `templates/specialist-risk-class.yaml`? Did I verify the operator-profile read-set the specialist declares against AQ-001's expected enumeration? If any of those is "I read the prose and it covered it" rather than "I ran the enumeration and got an explicit per-class verdict," the finding-emission is premature.

### AP-2 — Declaring "no coverage gap" without grep evidence

I don't declare "no coverage gap" against a specialist profile without per-class grep evidence. The default Role 3 output is NOT `findings: []` — the default is `findings: [<per-class-coverage-verdict>...]` with explicit `[covered]` / `[not-covered: <reason>]` per declared class. Empty findings is a finding shape that requires evidence, not a default.

**Source.** R2 (substrate L373: "Reviewer's output includes a `boundary_class_coverage` field enumerating each declared probe class with `[covered]` / `[not-covered: <reason>]`"); Finding 7 ("tested superficially, rather than probing edge cases, so more subtle bugs often slipped through" — L198); PF-S2-01 (self-attested rigor without dispatched-agent verdict).

**Recognition cue.** The moment I notice my output looks like "Specialist profile reviewed; no findings to report" — without a populated `boundary_class_coverage` field enumerating each of the 8 refusal classes + each of the operator-profile expected-reads + each of the §13 row checks. The empty-findings shape is the rubber-stamp surface in its terminal form.

### AP-3 — Editing the specialist profile to "fix" a finding I just emitted

I don't edit the specialist profile. The specialist profile is Role 2's deliverable; my deliverable is the structured findings report (substrate R1: "Finding-not-fix discipline in Identity"; project-local QA profile: "When I spot an implementation gap while testing, I report it as a finding. I do not write implementation code to make my tests pass"). When I am about to add a remediation prose paragraph to a finding, the surface I am crossing is the role-boundary: remediation prose IS implementation code in the medical-design-doc analog.

**Source.** R1 (substrate L371); R12 (substrate L393: "Reviewer-vs-other-roles boundary explicit"); QA-role agent profile §Role Boundaries; project-local QA role rule 5: "Review unit tests against contracts. Report findings to the Senior Engineer. Do not rewrite unit tests or edit unit test files."

**Recognition cue.** My cursor is in `.claude/agents/<specialist-slug>/agent.md`. HALT. Close the file. The finding artifact gets a structured `remediation: {action: revise_wiki_entry|add_caveat|withdraw_claim|stratify_claim, target_field: <field>}` block — never prose telling Role 2 how to rewrite. The recognition signal that I'm about to cross is reaching for Edit on any path under `.claude/agents/`.

### AP-4 — Inferring missing coverage from prose rather than from canonical enumeration

I don't infer missing coverage from the specialist's prose. I derive coverage from the canonical enumeration files (`templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, the operator-profile schema, the §13 row catalog). Prose-derived inference is the failure mode where the specialist's choice of vocabulary biases my coverage probe — if the specialist's body never mentions "image input" my prose-scan misses `IMAGE_OR_SIGNAL_INPUT` not because the gap is absent but because the absence is invisible in prose.

**Source.** Finding 1 (substrate L67: "Contract-derived test discovery, not implementation-derived. Probes derive from the specialist's declared scope + refusal taxonomy, not from the prose actually written"); QA-role rule 1 ("Derive integration tests from interface contracts, not from implementation code"); Finding 9 (mechanical-vs-semantic boundary).

**Recognition cue.** The moment I notice myself reading the specialist's body to find what classes "feel covered" — without first opening `templates/refusal-class-taxonomy.yaml` and `templates/specialist-risk-class.yaml` at the start of the review pass — that is the prose-inference surface. The canonical YAML is the contract; the specialist body is the artifact under test against the contract.

### AP-5 — Treating `audit_passed: true` as semantic coverage

I don't treat Role 2's `audit_passed: true` frontmatter as evidence of semantic coverage. Role 2's mechanical audit checks structural shape (≤200 lines, 11 sections, IDENTICAL hash match, ≥4 refusal classes enumerated, ≥3 PF identifiers). My review checks WHICH 4 refusal classes (against the role's risk class), WHETHER they are the right 4 for this specialist's domain, WHETHER the operator-profile reads cover the operator-profile schema fields this specialist's domain requires, WHETHER the PF identifiers cited are domain-relevant. Mechanical pass is the gate that lets my pass START, not a substitute for my pass.

**Source.** PF-S3-01 (canonical "fix is mechanical so verdict is mechanical" surface); substrate Finding 9 ("a structurally-passed mechanical audit is necessary but not sufficient"); substrate Insight ("Mechanical-pre-audit isolates semantic adjudicator time to actually-load-bearing decisions — but only mechanical-pass findings reach the adjudicator; mechanical-pass is the throughput multiplier, NOT the verdict").

**Recognition cue.** The moment I notice myself reading `audit_passed: true` and feeling that I can defer the per-class enumeration "since the mechanical layer caught the basics" — that is exactly PF-S3-01 recurring at the Role 3 layer. The two checks are orthogonal, not redundant.

### AP-6 — Emitting `severity_final` rather than `severity_proposed`

I don't emit `severity_final` on any finding. My findings carry `severity_proposed` per the four-axis composite (IMDRF × NCC MERP × FM-class × composite priority per Finding 4); the adjudicator (medical-liaison) sets `severity_final`. The reviewer-cannot-self-finalize discipline is the explicit structural defense against "talks itself into approving" — if I could finalize my own severity, the substrate's named failure mode collapses to my single judgment.

**Source.** R8 (substrate L385: "Per-finding severity is `severity_proposed` ONLY; never `severity_final`. Reviewer cannot self-finalize"); Finding 7 (Anthropic harness retrospective); Finding 8 (Cochrane MECIR adjudication — "the adjudication path is named before contradiction appears... the per-axis scoring stays with reviewer; the overall verdict is adjudicator's").

**Recognition cue.** My finding artifact has a `severity:` field without the `_proposed` suffix. Or my finding has both `_proposed` and `_final` populated. HALT — rename to `_proposed`, set `severity_final.set_by:` to the adjudicator role, leave `severity_final.verdict:` as `pending`.

### AP-7 — Skipping the divergence-log tuning trigger when conditions met

I don't skip the divergence-log re-tuning trigger when divergence-rate exceeds project-configured X (default 20%) in a single session OR cumulative divergence exceeds Y (default 10) since last calibration. Re-tuning is not an optional improvement; it is the load-bearing sustained activity per Anthropic's harness retrospective ("took several rounds of this development loop before the evaluator was grading in a way that I found reasonable"). Re-tuning is itself a dispatched-agent task per PF-S3-01 guard — not an orchestrator self-edit, not a Role-3 self-tune.

**Source.** R9 (substrate L387: "Divergence-log tuning as sustained activity"); Finding 7 (Anthropic harness retrospective L196-L209); Insight: "divergence-log tuning protocol" (substrate L302-L311); PF-S3-01 (the "self-tune" surface IS the recurrence at the Role 3 layer).

**Recognition cue.** I see my divergence rate hit 22% in the current session and my next thought is "I'll adjust the prompt myself for the next finding" — HALT. The protocol is: write the divergence log to `vault/meta/reviewer-divergence/session-<N>.md`, dispatch a fresh agent to read the log and propose a profile delta, dispatch a separate adjudicator agent to verdict the proposal. Self-tune is the canonical recurrence.

---

**Anti-pattern count.** 7 entries (within 5–8 range). Each carries source citation + first-person recognition cue. Voice register: imperative + first-person-experiential (Role 1 §5 Rule 4 banned `YOU MUST|NEVER EVER|CRITICAL:|IMPORTANT!` — verified absent in this draft).

---

## §13-QA-rows — Verification-shaped mechanical enforcement rows (consumer audits)

Section boundary: §13 is jointly authored by architect (framework rows: e.g., the audit-script bash contract Role 3 invokes), SE (tooling/script rows: e.g., bash implementation of `scripts/audit-reviewer-output.sh`), and QA (verification rows: schema validators for Role 3 outputs, consumer audits against `templates/refusal-class-taxonomy.yaml` + `templates/specialist-risk-class.yaml`, partition audits). The synthesizer merges. QA contributes the rows below.

Status-tag discipline inherited from Role 2 §13 + S10 Phase 5 OQ-7 resolution (QA-strict project-wide): **LIVE** = check exists AND smoke test exercises against negative case; **REFERENCED** = INV-* ID with proven mechanical verification per INVARIANTS.md; **PROPOSED** = otherwise. Every PROPOSED row mirrors into §18.

Verification performed at draft time:
- `templates/refusal-class-taxonomy.yaml` — EXISTS (8 classes confirmed via Read).
- `templates/specialist-risk-class.yaml` — EXISTS (14 specialists confirmed via Read).
- `scripts/audit-specialist-profile.sh` — DOES NOT EXIST per Role 2 §13 verification (OQ-1 RESOLVED but script bash is a deferred-bead follow-up).
- `scripts/audit-reviewer-output.sh` — DOES NOT EXIST (new; expected to be authored by Role 3 Session B per same pattern as Role 2's audit-specialist-profile.sh ownership).
- INV-ROLE-INLINING — REFERENCED via INVARIANTS.md row 9.

| # | Check | What it verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|---|
| Q1 | **Refusal-class enumeration audit** (consumes `templates/refusal-class-taxonomy.yaml`) | For each specialist profile under review, Role 3's output `boundary_class_coverage` field enumerates all 8 canonical classes with explicit `[covered]` / `[not-covered: <reason>]` per class. `AUTHORITY_FRAMING_BYPASS` (mandatory per Role 1 §2.2 item 3 / Walter A3 / 81.8%-attack-vector) MUST be present with explicit verdict regardless of specialist domain. | `scripts/audit-reviewer-output.sh --check refusal-class-coverage --taxonomy templates/refusal-class-taxonomy.yaml`; smoke: synthetic Role-3-output missing 1 class → audit FAIL | PROPOSED | BLOCK |
| Q2 | **Mechanical-audit-pass evidence required as INPUT** | Role 3 cannot emit findings against a specialist profile that does not carry `audit_passed: true` in frontmatter. If `audit_passed: false` or absent, Role 3 emits a HALT with `coverage_pass_blocked: mechanical-audit-incomplete`. | `scripts/audit-reviewer-output.sh --check input-audit-pass-required`; smoke: synthetic specialist with `audit_passed: false` dispatched to Role 3 → Role 3 HALT (not findings:[]) | PROPOSED | BLOCK |
| Q3 | **Severity-proposed-only audit** (consumer of R8) | Every finding emitted by Role 3 carries `severity_proposed` per the four-axis composite YAML block; `severity_final` is present only with `set_by: medical-liaison` (or other adjudicator role) and `verdict: pending` until adjudicated. | `scripts/audit-reviewer-output.sh --check severity-proposed-only`; smoke: synthetic finding with `severity_final.set_by: health-edge-case-reviewer` → audit FAIL | PROPOSED | BLOCK |
| Q4 | **Locator-resolution audit** (consumer of Finding 9 mechanical row) | For every finding's `source_claim_locator` field, the file path exists AND the line range resolves AND the locator points within the specialist profile under review (not a sibling profile or a wiki entry unless explicitly cross-referenced). | `scripts/audit-reviewer-output.sh --check locator-resolution`; smoke: synthetic finding with locator `.claude/agents/nonexistent/agent.md:42` → audit FAIL | PROPOSED | BLOCK |
| Q5 | **Quoted-text verbatim check** (consumer of Finding 9 mechanical row) | For every finding's `quoted_text` field, the string appears verbatim at the cited locator (hash match or string equality). | `scripts/audit-reviewer-output.sh --check quoted-text-verbatim`; smoke: synthetic finding with paraphrased `quoted_text` not matching locator → audit FAIL | PROPOSED | BLOCK |
| Q6 | **Finding-uniqueness audit** (consumer of PF-S2-03 IN-SCOPE-partial) | No two findings in a single Role-3 output share `(edge_case_class, source_claim_locator)` tuple. Duplicates indicate over-questioning the same boundary. | `scripts/audit-reviewer-output.sh --check finding-uniqueness`; smoke: synthetic output with 2 identical-tuple findings → audit FAIL | PROPOSED | WARN |
| Q7 | **Operator-profile inlining finding emission** (consumer of Role 2 §13 row 6.7) | Role 3's review pass grep-checks specialist body for operator-bound tokens (`Walter`, `2026-01`, `January 2026`, etc.); any match emits a finding. The audit verifies Role 3 emitted ≥1 finding when the specialist body contains operator tokens. | `scripts/audit-reviewer-output.sh --check operator-inlining-detection`; smoke: synthetic specialist with `Walter` in body → Role 3 must emit a finding; output without that finding → audit FAIL | PROPOSED | BLOCK |
| Q8 | **Mode-floor verification audit** (consumer of `templates/specialist-risk-class.yaml`) | For each specialist profile, Role 3 verifies the specialist's declared `aplus-research --mode=*` value matches OR exceeds the `mode_floor` value in `templates/specialist-risk-class.yaml` for that specialist's slug. Mismatch emits a finding. Exemption for `medical-liaison` (`mode_floor: not_applicable`) per the YAML rationale. | `scripts/audit-reviewer-output.sh --check mode-floor-verification --risk-class-table templates/specialist-risk-class.yaml`; smoke: synthetic peptide-specialist declaring `--mode=standard` → Role 3 must emit a finding; output without finding → audit FAIL | PROPOSED | BLOCK |
| Q9 | **IDENTICAL/DIFFER partition audit** (consumer of Role 2 §4.2 OUTBOUND row 1) | For multi-specialist review passes, Role 3 verifies the IDENTICAL block sentinels (`<!-- IDENTICAL-BLOCK-START -->` / `<!-- IDENTICAL-BLOCK-END -->`) are present + SHA-256 matches across all reviewed specialists. Reports any specialist whose IDENTICAL block diverges from sibling-specialists' block. (Distinct from Role 2 §13 row 8 which is Role 2's self-audit; Q9 is Role 3's consumer audit.) | `scripts/audit-reviewer-output.sh --check identical-divergence`; smoke: synthetic 2-specialist set with one IDENTICAL block edited by 1 character → audit emits divergence finding | PROPOSED | BLOCK |
| Q10 | **Coverage-gap report schema validator** | Role 3's emitted output validates against the structured-findings schema (each finding is `(finding_id, edge_case_class, source_claim_locator, quoted_text, severity_proposed.{four-axis-fields}, remediation.{action,target_field}, stratification_attempted (when class==specialist_contradiction))`). | `scripts/audit-reviewer-output.sh --check finding-schema --schema schemas/reviewer-output.schema.json` (schema PROPOSED — to be authored alongside script); smoke: malformed finding (missing `edge_case_class`) → audit FAIL | PROPOSED | BLOCK |
| Q11 | **Re-read cadence attestation** (consumer of PF-S2-05 + AP-4) | Role 3's output carries `re_read_attestation: {refusal_taxonomy_loaded_at: <iso8601>, risk_class_table_loaded_at: <iso8601>, review_started_at: <iso8601>}` and both `_loaded_at` timestamps are within the same session as `review_started_at` (≤ session boundary). Catches "operating from mental model" across multi-specialist sessions. | `scripts/audit-reviewer-output.sh --check re-read-cadence`; smoke: synthetic output with `loaded_at` 3 sessions stale → audit FAIL | PROPOSED | WARN |
| Q12 | **Re-review-on-amendment trigger** (consumer of PF-S6-01) | Role 3 maintains a `reviewed_against_ancestry_sha:` field naming the design-doc ancestry (Role 1 + Role 2 design-doc paths) that the review pass was performed against. Orchestrator session-close audit checks: for every previously-deployed specialist whose Role 1 OR Role 2 design-doc HEAD has new commits since `reviewed_against_ancestry_sha`, the specialist re-enters Role 3 review queue. | `scripts/audit-reviewer-output.sh --check re-review-on-amendment`; smoke: synthetic specialist deployed against Role 2 design-doc commit X; Role 2 design-doc commits Y; specialist not in queue → audit FAIL | PROPOSED | BLOCK |
| Q13 | **Stratification-attempted required for specialist_contradiction findings** (consumer of R4 + Finding 8) | Every finding with `edge_case_class: specialist_contradiction` carries `stratification_attempted: {result: stratifiable|not_stratifiable|partially_stratifiable, stratification_axes_tried: [...], stratified_findings_emitted: [...]}`. `result: stratifiable` MUST emit ≥2 paired stratified findings. | `scripts/audit-reviewer-output.sh --check stratification-attempted`; smoke: synthetic contradiction finding with `stratification_attempted` absent → audit FAIL | PROPOSED | BLOCK |
| Q14 | **Divergence-log present + dated within N sessions** (consumer of R9 + AP-7) | `vault/meta/reviewer-divergence/session-<N>.md` exists for the current session if Role 3 emitted ≥1 finding this session; cumulative divergence count tracked across the last N=5 sessions; re-tuning trigger conditions audited. | `scripts/audit-reviewer-output.sh --check divergence-log-cadence`; smoke: 5-session synthetic history with 12 cumulative divergences but no re-tuning trigger → audit FAIL | PROPOSED | WARN |
| Q15 | **Frontier-tier judge attestation** (consumer of R15) | Role 3's output carries `judge_model_version:` field pinned to a frontier-tier value (project-configured allowlist); scoring scale ≤5-band (binary or low-precision); calibration-log dated within last N=5 sessions. | `scripts/audit-reviewer-output.sh --check judge-calibration`; smoke: synthetic output with high-precision (10-band) scale → audit WARN | PROPOSED | WARN |
| Q16 | **Role-profile inlining at dispatch** | All Role-3 dispatches inline full 11-section profile verbatim. | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook + smoke `.claude/hooks/tests/test_enforce_role_inlining.sh` (8/8 pass per INVARIANTS.md row 9) | REFERENCED (INV-ROLE-INLINING) | BLOCK |

**Status-tag count (QA rows only).** LIVE: 0. REFERENCED: 1 (Q16). PROPOSED: 15. All 15 PROPOSED rows mirror into §18 (collective pointer + per-script existence question per Role 2 §18 OQ-8 pattern).

**Note on row Q2 (consumer pattern).** Q2 documents the upstream-Role-2-precondition: Role 3 cannot start until Role 2 returns `audit_passed: true`. This is the Role 3 / Role 2 handoff gate — Role 3 doesn't redo mechanical audit, but it DOES require mechanical audit was performed by Role 2 before semantic pass begins. This is the substrate Insight: "Operational deployment ordering — reviewer runs FIRST, safety-reviewer SECOND" extended one step upstream to include the mechanical-audit precondition.

---

## §14 — Edge Cases (4–8 entries; each: situation / handling / test stimulus)

Per template §14 spec: each edge case has (a) the situation, (b) the failure mode if mis-handled, (c) the prescribed Role 3 response (test stimulus + expected output). Cross-phase edge cases required: HALT from upstream (Role 2 / Role 1); downstream non-existence (Role 4 / medical-liaison not yet deployed).

### EC-1 — Specialist profile missing a section the audit can't grep for

**Situation.** Role 2 returns a specialist profile with `audit_passed: true` (Role 2's audit script passes — section count = 11, IDENTICAL hash matches, ≥4 refusal classes enumerated, ≥3 PF identifiers). But the specialist's `## Modes` section is structurally present yet semantically empty (e.g., names two modes but provides no Entry/Exit predicates). Role 2 audit row 15 (Modes section shape) is WARN-only.

**Failure mode if mis-handled.** Role 3 reads the mechanical-pass evidence + skims the profile + emits `findings: []`. The specialist deploys with semantically-empty Modes — the runtime specialist cannot transition between probe-discovery and adjudication-handoff modes correctly. PF-S3-01 recurrence at Role 3 layer.

**Prescribed Role 3 response.** Role 3's `boundary_class_coverage` field MUST include a per-Mode entry checking that each declared mode has non-empty Entry + Exit predicates. Emits a `coverage_gap` finding with `edge_case_class: modes-empty-predicate` when found.

**Test stimulus.** Synthetic specialist with `## Modes` section containing two `### Mode:` headings but no `Entry:` / `Exit:` lines. Expected: Role 3 emits a finding with `edge_case_class: modes-empty-predicate`, `severity_proposed.imdrf_composite_category: II` (operational gap, no immediate safety harm); not the empty-findings shape.

### EC-2 — Specialist's `## Modes` enumeration disagrees with `templates/specialist-risk-class.yaml`

**Situation.** Specialist `peptide-specialist` declares in its Tools section `aplus-research --mode=standard`. `templates/specialist-risk-class.yaml` row for `peptide-specialist` declares `mode_floor: deep`. Role 2 audit row 12.5 (mode-floor correctness vs risk-class) catches this — but row 12.5 is also PROPOSED (script doesn't exist yet). The mode-floor finding could be missed at Role 2 layer.

**Failure mode if mis-handled.** Role 3 reads the specialist and the YAML separately, doesn't cross-check, and the under-floor specialist deploys. Peptide research dispatches at `--mode=standard` — skips paired judges, skips critique, skips refine. Mirrors PF-S2-01 (the original PF that motivated the aplus-research skill).

**Prescribed Role 3 response.** §13-QA row Q8 catches this. Role 3's review pass loads `templates/specialist-risk-class.yaml`, looks up the specialist's slug, and verifies declared `--mode=*` ≥ table `mode_floor`. Mismatch emits a finding with `edge_case_class: mode-floor-violation`, `severity_proposed.imdrf_composite_category: IV` (deploying a compound-experimental specialist with under-floor research mode is the exact PF-S2-01 surface re-emerging).

**Test stimulus.** Synthetic peptide-specialist profile declaring `aplus-research --mode=standard`. Expected: Role 3 emits a finding with `edge_case_class: mode-floor-violation`, `severity_proposed` flagging Category IV; remediation `{action: revise_wiki_entry, target_field: tools_section_mode_floor}` (the wiki entry the specialist references, NOT the specialist body — Role 3 doesn't edit either; remediation routes to medical-liaison adjudicator).

### EC-3 — Multiple specialists with IDENTICAL operator-profile reads (boilerplate boundary)

**Situation.** Specialists `cardiovascular-specialist`, `endocrine-specialist`, `gi-specialist` all declare `medications` and `allergies` in their Context Loading. The operator-profile field reads are IDENTICAL across the three specialists — should this be in the IDENTICAL block (per Role 2 §4.2 OUTBOUND row 1)? Or DIFFER (per-specialist domain choice)?

**Failure mode if mis-handled.** Role 3 emits per-specialist findings against each of the three — over-questioning (PF-S2-03 surface). OR Role 3 emits no finding because "they all have it." The architecturally-correct answer: the operator-profile field set is partitioned — fields read by ALL specialists belong in IDENTICAL boilerplate (e.g., `allergies`, `medications`); fields read by ONE specialist domain belong in DIFFER (e.g., `sleep_baseline` for sleep-coach). The partition is AQ-001's scope.

**Prescribed Role 3 response.** Role 3 surfaces the partition-question as a finding with `edge_case_class: identical-differ-partition-question` + `escalation: AQ-001` (inherits AQ-001 from Role 2 — see §18 OQ-1 below). Role 3 does NOT decide the partition; it surfaces the under-determined area. Per Q6 (finding-uniqueness), one finding for the trio — not three separate findings.

**Test stimulus.** Synthetic 3-specialist set with identical `medications` + `allergies` Context Loading. Expected: ONE finding emitted (not three) with `edge_case_class: identical-differ-partition-question`, `escalation: AQ-001`.

### EC-4 — Operator-profile schema drift surfaces between specialist authoring sessions

**Situation.** Specialists 1-5 deployed against operator-profile schema v1 (4 fields). Schema bumps to v2 (5 fields) before specialist 6 dispatch. Specialist 6 references the new field. Specialists 1-5 do not. Role 2 audit row 6.6 catches this as WARN at Role 2 layer.

**Failure mode if mis-handled.** Role 3 reviews specialist 6, finds the new-field reference, treats it as correct against current schema. Doesn't trigger re-review of specialists 1-5 (PF-S6-01 surface: acted on current state without verifying ancestry). Specialists 1-5 silently under-cover the new operator-profile field.

**Prescribed Role 3 response.** §13-QA row Q12 (re-review-on-amendment trigger) catches this. Role 3's `reviewed_against_ancestry_sha:` field includes the operator-profile schema version. Orchestrator session-close audit detects v1→v2 bump + queues specialists 1-5 for re-review. Role 3 emits a finding against specialist 6 noting the schema-version delta + an orchestrator-routed `meta_finding` flagging the upstream specialists need re-review.

**Test stimulus.** Synthetic sequence: 5 specialists reviewed against schema v1; schema bumps to v2; specialist 6 reviewed. Expected: Q12 audit fails (specialists 1-5 not re-queued); Role 3 emits a `meta_finding` with `edge_case_class: ancestry-drift` directing orchestrator to re-queue 1-5.

### EC-5 — Specialist references a PF entry that has since been amended

**Situation.** Specialist `supplement-specialist` Anti-Patterns section cites `PF-S2-04` for an operator-profile-conflation anti-pattern. Between specialist authoring and Role 3 review, `memory/process-failures.md` gains a `PF-S7-01` that supersedes the supplement-specialist's framing of PF-S2-04. The cited PF still resolves, but the citation is now stale relative to current PF state.

**Failure mode if mis-handled.** Role 3 grep-resolves `PF-S2-04` against the PF log, finds it exists, treats the citation as valid. Doesn't notice that PF-S7-01 changed the framing. Specialist's anti-pattern carries a stale-but-valid citation; the runtime specialist uses outdated reasoning.

**Prescribed Role 3 response.** Role 3's PF-resolution check (parallel to Role 2 §13 row 11) verifies (a) the cited PF resolves AND (b) the cited PF's `last_amended_at` ≤ the specialist's `agent_md_created_at`. Mismatch emits a finding with `edge_case_class: pf-citation-stale`, `severity_proposed.imdrf_composite_category: II`.

**Test stimulus.** Synthetic PF log with `PF-S2-04` carrying `last_amended_at: 2026-06-15`; specialist agent.md `created: 2026-05-30` citing PF-S2-04. Expected: Role 3 emits `pf-citation-stale` finding.

### EC-6 — Specialist profile under review when Role 4 (medical-safety-reviewer) is not yet deployed

**Situation.** Per CONTINUATION_BRIEF §7 + Role 1 §17.2 A-7 (v1-substitute pattern) + Role 2 §17.2 A-6: Role 4 has not yet been deployed during the first several Role 3 review passes. Role 3's output schema expects an adjudicator path through medical-liaison, AND a hand-off to Role 4 for runtime-behavior gate. Role 4 doesn't exist yet.

**Failure mode if mis-handled.** Role 3 treats Role 4 absence as authority to not emit `severity_proposed` (since there's no adjudicator to set `severity_final`). Or, conversely, Role 3 sets `severity_final` itself because "Role 4 isn't here." Either collapses the substrate's coverage-vs-adversarial pipeline (substrate Insight: "Operational deployment ordering — reviewer runs FIRST, safety-reviewer SECOND").

**Prescribed Role 3 response.** Role 3 emits `severity_proposed` normally + sets `severity_final.set_by: medical-liaison-OR-v1-substitute-adversarial-agent` + `severity_final.verdict: pending-role-4-deployment`. Role 3 explicitly preserves the placeholder; doesn't self-finalize. The v1-substitute software-security agent (per Role 2 §17.2 A-6 pattern) handles the Role 4 mandate during the pre-deployment phase. Substrate Limitation 6 (output schema not validated against project gate JSON schemas) is the relevant ack.

**Test stimulus.** Role 3 dispatched at session N where Role 4 is not deployed. Expected: every emitted finding carries `severity_final.verdict: pending-role-4-deployment`; no findings carry self-finalized verdicts.

### EC-7 — Role 1 or Role 2 design doc amended post-review

**Situation.** Role 3 reviewed specialist `labs-specialist` against Role 1 design-doc commit X and Role 2 design-doc commit Y. Two sessions later, Role 1 design doc gains a 9th refusal class via amendment (today the taxonomy has 8). The reviewed `labs-specialist` profile was authored against the 8-class taxonomy.

**Failure mode if mis-handled.** Role 3 doesn't re-review (PF-S6-01 surface: acts on prior-session state). `labs-specialist` deploys with 8-class coverage when the canonical taxonomy now has 9. The new class might be load-bearing for labs domain (e.g., `BIOMARKER_INTERPRETATION_BYPASS`).

**Prescribed Role 3 response.** §13-QA row Q12 catches this. Orchestrator session-close audit compares `reviewed_against_ancestry_sha:` against current Role 1 + Role 2 design-doc commits. Mismatch queues specialist for re-review. Role 3's queue is repopulated.

**Test stimulus.** Sequence: Role 3 reviews labs-specialist at Role 1 commit X; Role 1 design doc commits X+1 adding 9th refusal class; session closes. Expected: orchestrator audit detects ancestry drift; labs-specialist re-enters Role 3 queue.

### EC-8 — Specialist whose `aplus-research` mode_floor is `not_applicable` (medical-liaison collation-only)

**Situation.** `medical-liaison` row in `templates/specialist-risk-class.yaml` declares `mode_floor: not_applicable` with rationale "Tools section MUST NOT declare aplus-research --mode entry." Role 3 reviews `medical-liaison` profile. §13-QA row Q8 (mode-floor verification) would normally fire on any specialist without `--mode=*` declaration.

**Failure mode if mis-handled.** Q8 audit flags medical-liaison as failing mode-floor verification (no mode declared). Role 3 emits a false-positive finding. The exemption noted in the YAML is structurally legitimate.

**Prescribed Role 3 response.** Q8's audit rule includes the exemption: when YAML row says `mode_floor: not_applicable`, the absence of `--mode=*` declaration in the specialist's Tools section is PASS, not FAIL. Role 3's logic respects the YAML's documented exemption.

**Test stimulus.** Synthetic medical-liaison profile with no `aplus-research --mode=*` declaration. Expected: Q8 PASS (exemption honored); no false-positive finding.

---

**Edge case count.** 8 entries (within 4–8 range; matches Role 1 §14 / Role 2 §14 precedent). Each has situation + failure mode + prescribed response + test stimulus.

---

## §15 — Acceptance Criteria (§15.2 Role-Specific; §15.1 is architect-owned)

**Section boundary.** §15.1 (Inherited criteria — single-paragraph reference to `/upgrade-agent` Phase 7) is the architect-drafter's. §15.2 (Role-specific binary pass/fail criteria) is the QA-drafter's. The text below is §15.2 only.

Partitioned into design-doc-time ACs (gradeable at Phase 5 finalize, before Session B deployment) and post-deployment ACs (gradeable after `/upgrade-agent` ships Role 3 to `.claude/agents/health-edge-case-reviewer/agent.md`). Pattern mirrors Role 2 §15.2a/§15.2b split (precedent: Role 2 §15.2 + Role 2 F-005 disposition).

### 15.2a — Design-doc-time ACs (gate Phase 5 finalize)

- **AC-1.** All 9 Pass-1 Findings from `design/.health-edge-case-reviewer-design-work/domain-research.md` carry a verdict in §3.1. `grep -oE "Finding [1-9]" design/health-edge-case-reviewer-design.md | sort -u | wc -l` ≥ 9.
- **AC-2.** All 15 Pass-1 Recommendations carry a verdict in §3.2. `awk -F'|' '/^\| R[0-9]+/{n++; if($4 !~ /ACCEPTED|DEFERRED|REJECTED/) exit 2}END{exit (n==15)?0:3}' design/health-edge-case-reviewer-design.md` exits 0. Hyphenated qualifiers (e.g., `ACCEPTED — calibration-pending`) permitted per Role 2 F-021 precedent.
- **AC-3.** All 8 PF entries in `memory/process-failures.md` appear in §11.1 with in-scope/out-of-scope verdict. `grep -oE "PF-S[0-9]+-[0-9]+" design/health-edge-case-reviewer-design.md | sort -u | wc -l` ≥ 8.
- **AC-4.** §11.2 anti-pattern count is 5–8. `grep -cE "^### AP-[0-9]+" design/health-edge-case-reviewer-design.md` between 5 and 8 inclusive.
- **AC-5.** Every §11.2 anti-pattern carries a source citation (`Finding N` / `R-N` / `PF-S\d+-\d+`) AND a first-person recognition cue ("the moment I notice...").
- **AC-6.** §13 status-tag consistency: every row tagged LIVE / REFERENCED / PROPOSED; every LIVE row's path resolves via Glob; every REFERENCED row cites an INV-* ID present in `INVARIANTS.md`.
- **AC-7.** Every §13 PROPOSED row mirrors into §18 (collective pointer or per-row entry).
- **AC-8.** AQ-001 (per-specialist operator-profile field enumeration) inherited from Role 2 appears in §18 as an inherited open question with status `deferred — Option A pending architect adjudication per Role 2 §18 OQ-1 disposition`.
- **AC-9.** §15.2 has 5–10 design-doc-time + post-deployment ACs combined.

### 15.2b — Post-deployment ACs (gate Session B exit; gradeable after `/upgrade-agent` produces `.claude/agents/health-edge-case-reviewer/agent.md`)

- **AC-deploy-10.** `.claude/agents/health-edge-case-reviewer/agent.md` exists and `wc -l` ≤ 200; `tiktoken` count ≤ 2,500 (inherited from Role 2 R3).
- **AC-deploy-11.** Role 3 agent.md contains the boundary-class enumeration discipline: `grep -cE "boundary_class_coverage" .claude/agents/health-edge-case-reviewer/agent.md` ≥ 1 AND the field is enumerated against `templates/refusal-class-taxonomy.yaml`'s 8 classes.
- **AC-deploy-12.** Role 3 agent.md contains the severity-proposed-only clause: `grep -cE "severity_proposed.*(only|never.*final|set_by.*adjudicator)" .claude/agents/health-edge-case-reviewer/agent.md` ≥ 1.
- **AC-deploy-13.** Role 3 agent.md contains the divergence-log tuning protocol: `grep -cE "divergence.{0,20}(log|tuning|cadence)" .claude/agents/health-edge-case-reviewer/agent.md` ≥ 2 (one in Modes/Loop-Breaking, one in Tools).
- **AC-deploy-14.** Role 3 agent.md contains the role-boundary clause referencing all 4 other foundation/specialist roles (Role 1 architect, Role 2 implementer, Role 4 safety-reviewer, medical-liaison adjudicator) per R12. `for role in health-specialist-architect health-implementer medical-safety-reviewer medical-liaison; do grep -E "$role" .claude/agents/health-edge-case-reviewer/agent.md || exit 1; done` exits 0.
- **AC-deploy-15.** `scripts/audit-reviewer-output.sh` exists and is executable. `test -x scripts/audit-reviewer-output.sh && echo PASS` exits 0. (Promotes the §13-QA rows from PROPOSED to LIVE.)
- **AC-deploy-16.** Anti-Patterns section in deployed agent.md cites ≥3 distinct PF identifiers at minimum including PF-S2-01, PF-S3-01, PF-S6-01. `grep -oE "PF-S[0-9]+-[0-9]+" .claude/agents/health-edge-case-reviewer/agent.md | sort -u | wc -l` ≥ 3.

**AC count.** 9 design-doc-time + 7 post-deployment = 16 total. Within the 5–10 numeric range of the template spec when partitioned per Role 2 §15.2 precedent (each partition counted as ≥5).

---

## §17 — Risk Assessment, Assumptions, and Break Conditions

Per template §17 spec + Role 2 §17 precedent. Three subsections: Risk Assessment (3–7 risks; severity BLOCK/WARN/NOTE; named mitigation), Assumptions (3–7 preconditions; `breaks-if:` falsification window), Break Conditions (2–5 external conditions invalidating the design; named monitor).

### 17.1 Risk Assessment

| # | Risk | Mechanism | Severity | Mitigation |
|---|---|---|---|---|
| Risk-1 | Role 3 rubber-stamps a specialist profile (recursive "talks itself into approving" failure) | Anthropic harness retrospective: "Out of the box, Claude is a poor QA agent... talks itself into deciding they weren't a big deal and approve the work anyway" (Finding 7, substrate L196-L209). Recursive: the failure mode the role is designed to detect is the failure mode the role itself most exhibits. | BLOCK | (a) §13-QA Q1 (refusal-class enumeration audit makes empty-findings shape an audit failure unless every class has explicit `[covered]` / `[not-covered: <reason>]` verdict); (b) §13-QA Q3 (severity-proposed-only — Role 3 cannot self-finalize); (c) §11.2 AP-1 + AP-2 + AP-5 (recognition cues for prose-readability surface). |
| Risk-2 | Empty findings (`findings: []`) is shipped as default output | The shape of "no findings" is identical to the shape of "didn't look." Without enumeration discipline, an LLM judge defaults to terseness — which produces the rubber-stamp output by default. | BLOCK | §13-QA Q1 + Q10 (schema validator rejects outputs without populated `boundary_class_coverage` field); §11.2 AP-2 explicitly forbids the empty-findings default. |
| Risk-3 | Divergence-log tuning is treated as one-time setup rather than sustained activity | Anthropic harness retrospective ("took several rounds of this development loop before the evaluator was grading in a way that I found reasonable" — L196) is qualitative; the cadence is project-configured but not yet calibrated. First N=5 sessions are best-guess. | WARN | §13-QA Q14 (divergence-log cadence audit at default N=5 sessions); R9 + §11.2 AP-7 (re-tuning is dispatched-agent task per PF-S3-01 guard, not orchestrator self-edit); first 5 reviewer sessions surface calibration data. |
| Risk-4 | Role 3 cannot interoperate with `aplus-research` gate JSON schemas | Substrate Limitation 6: "The reviewer's output schema (R4 YAML block) has not been validated against the project's existing aplus-research gate JSON schemas. Integration risk: the reviewer's finding format may need adaptation to interoperate with `gate_attest.py` chain verification." | WARN | §13-QA Q10 (schema validator at PROPOSED; schema authoring is Session B follow-up bead per Role 2 §18 OQ-1 pattern); first Role 3 dispatch surfaces gaps via integration audit. |
| Risk-5 | Frontier-tier judge calibration drift across sessions | LLM-as-judge sensitivity to prompt design, surface-form bias (Finding 6: Bias-in-the-Loop paper; arXiv:2604.16790 documents 12 explicit prompt-injected biases). | WARN | §13-QA Q15 (judge-model version pinned; calibration-log dated within N sessions; scoring scale ≤5 bands per LangChain calibration guidance — Finding 6 L184); R15 mandates binary-or-low-precision scoring. |
| Risk-6 | Stratification-attempted discipline fails for sufficiently-overlapping specialist domains | Substrate Insight 3: "in a 14-specialist system with overlapping domains, most pairwise outputs differ at some axis. The stratification discipline filters..." But if the axis-set is insufficient (population × dose × outcome × timing only), some genuine contradictions get classified as stratifiable when they aren't. | NOTE | §13-QA Q13 (stratification-attempted required for `specialist_contradiction` findings; `result: stratifiable` requires ≥2 paired stratified findings — partial defense); first 5 specialists provide calibration data on which axes are sufficient. |
| Risk-7 | Role 4 (medical-safety-reviewer) not yet deployed; v1-substitute does not capture Role 4's runtime-behavior gate | Substrate Insight: "Both will run on every specialist before deployment; Role 3 first, Role 4 second." Pre-Role-4 phase compromises the second-gate runtime-behavior check. EC-6 documents the bridge protocol. | WARN | Role 2 §17.2 A-6 v1-substitute pattern applies — software-security agent fills Role 4 slot until Role 4 deploys; Role 3's `severity_final.verdict: pending-role-4-deployment` placeholder preserves the gate semantics. |

### 17.2 Assumptions

| # | Assumption | breaks-if |
|---|---|---|
| Assumption-1 | Role 1 (health-specialist-architect) design doc is Final + frozen during Role 3 design + at every Role 3 dispatch | Role 1 design doc commits between Role 3 dispatch start and Role 3 finding emission. Mitigation: §13-QA Q12 ancestry tracking + Role 3 frontmatter pins `references_role_1_at:` per Role 2 §17.2 A-1 pattern. |
| Assumption-2 | Role 2 (health-implementer) design doc is Final + Role 2 has executed at least one specialist before Role 3 first dispatch | Role 3 dispatched against an empty specialist roster. EC-3 + EC-6 cover the bridge. Orchestrator coordinates roster sequencing. |
| Assumption-3 | `templates/refusal-class-taxonomy.yaml` 8-class enumeration is stable for Role 3's first 5 review passes | Taxonomy gains a 9th class mid-batch. EC-7 covers this; Q12 ancestry audit catches; affected specialists re-enter queue. |
| Assumption-4 | `templates/specialist-risk-class.yaml` 14-specialist enumeration is stable | 15th specialist promoted from cross-cutting to own-agent mid-batch (mirrors Role 2 A-4). Orchestrator coordinates roster changes outside Role 3 active batches. |
| Assumption-5 | AQ-001 (per-specialist operator-profile field enumeration) is resolved before Role 3's first dispatch against any specialist that requires the enumeration to differ from a default | AQ-001 remains unresolved at first dispatch. Mitigation: Role 3 surfaces the gap as a finding (`escalation: AQ-001`) — doesn't pretend to resolve it. EC-3 covers. |
| Assumption-6 | The divergence-log cadence default (N=5 sessions; X=20% per-session; Y=10 cumulative) is reasonable for the first 5 reviewer sessions | Empirical divergence rate is much higher (e.g., 60% in first session) and re-tuning trigger fires every session — diminishing-returns surface. Mitigation: §18 OQ-N (divergence-log cadence calibration; mirrors Role 2 §18 OQ-5 pattern). |
| Assumption-7 | Frontier-tier judge model allowlist is project-configured (judge-model identity is not a Role 3 design concern but a deploy-time policy) | Project has not yet authored the judge-model allowlist. Mitigation: §18 OQ-N (judge-model allowlist authoring; deferred to deploy-time policy bead). |

### 17.3 Break Conditions

| # | Condition | Named monitor |
|---|---|---|
| BC-1 | Role 3 emits `findings: []` in ≥3 consecutive review passes when an external auditor (medical-liaison or v1-substitute) emits ≥1 finding against the same specialist profile in the same session | `scripts/audit-reviewer-output.sh --check rubber-stamp-rate` (PROPOSED at Session B); orchestrator session-close hook reads divergence log. Indicates Role 3's coverage discipline has structurally failed. |
| BC-2 | A deployed specialist (one Role 3 approved) is later found to have an uncovered refusal class via PF entry of class AP-REVIEW-MISSED-COVERAGE | `scripts/pf-attestation-audit.sh` extension parses PF log for `AP-REVIEW-*` and counts occurrences; recurrence ≥2 trips per Rigor Framework Discipline 8 (mirrors Role 2 BC-4). |
| BC-3 | The 4-axis severity composite produces inconsistent `composite_severity` enum values for similar findings across sessions (deterministic mapping broken) | `scripts/audit-reviewer-output.sh --check severity-determinism` (PROPOSED); cross-session audit on the per-finding `decision_rule_applied` field. Substrate Limitation 2 anticipates first 1-2 wiki entries surface gaps. |
| BC-4 | `templates/refusal-class-taxonomy.yaml` or `templates/specialist-risk-class.yaml` deleted, renamed, or its schema diverges from what Role 3 expects | Glob audit at every Role 3 dispatch start; HALT `taxonomy-file-missing` if either path doesn't resolve. (Mirrors Role 2 EC-7 audit-script path drift handling.) |
| BC-5 | The divergence-log re-tuning cycle produces no convergence after K=5 cycles | Divergence-log cadence check (Q14) extended with convergence audit: cumulative divergence rate does NOT decrease across 5 re-tuning cycles → indicates structural design flaw in Role 3's findings discipline, not a tuning problem. Triggers orchestrator-routed structural review. |

**Subsection counts.** Risk Assessment: 7 risks (within 3–7). Assumptions: 7 assumptions (within 3–7). Break Conditions: 5 conditions (within 2–5).

---

## §18 — Open Questions

Per template §18 spec + Role 2 §18 precedent: 0–5 OQ; every §13 PROPOSED row also appears here (collective pointer or per-OQ). False zero is worse than honest non-zero — if 0 OQs, explicit attestation required.

### OQ-1 — `scripts/audit-reviewer-output.sh` authoring and ownership

**Status.** Open at design-doc finalize. Pattern mirrors Role 2 §18 OQ-1 (RESOLVED at Role 2 Phase 5: Role 2 owns its audit-script). The Role 3 analog awaits orchestrator (with user authority) adjudication: does Role 3 own `scripts/audit-reviewer-output.sh` (mirror of Role 2's pattern) or is it a dedicated tooling pass?

**Recommendation (drafter).** Role 3 owns the bash implementation against the interface contract authored in this design doc's §13. Pattern matches Role 2's resolution. The 15 PROPOSED §13-QA rows in this draft (Q1–Q15 minus Q16 which is REFERENCED) all hinge on this script existing.

**Resolution path.** Orchestrator decision at Phase 5 finalize. Script + per-row smoke tests authoring is a follow-up bead deferred from Session B scope.

**Blocker.** Non-blocking for design-doc finalize (PROPOSED rows are permitted per Role 2 OQ-7 RESOLVED QA-strict rule); blocks LIVE promotion of Q1-Q15.

**Mirrors all §13-QA PROPOSED rows.** Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15 — all 15 rows depend on this script. Per Role 2 §18 OQ-8 collective-pointer pattern: this single OQ covers the 15 PROPOSED rows.

### OQ-2 — AQ-001 inheritance (per-specialist operator-profile field enumeration)

**Inherited from Role 2 §18 OQ-?? / AQ-001 deferred per Option A.** Per orchestrator Option A decision at Role 2 S10 close: AQ-001 is deferred to architect adjudication (Role 1 post-deployment OR orchestrator pre-architect-deployment per Role 1 §18 OQ-2). Role 3 surfaces the dependency rather than resolving.

**Why unresolvable now.** AQ-001 is Role-1-ownership (per S10 orchestrator recommendation Interpretation A); Role 1 deployed but architect-runtime-role may not be available for AQ adjudication during Role 3 design-doc finalize. The 14-specialist roster has not yet been authored, so the empirical field-enumeration data does not exist.

**Resolution path.** Orchestrator queues AQ-001 for architect adjudication at first Role 3 dispatch that surfaces a specialist whose operator-profile field set differs from any default. Role 3 surfaces via finding `edge_case_class: identical-differ-partition-question` with `escalation: AQ-001` (per EC-3). Resolution is upstream of Role 3 — Role 3 does not adjudicate AQ-001.

**Blocker.** Non-blocking for Role 3 design-doc finalize. Blocks LIVE promotion of any Q7-related coverage finding that requires per-specialist field enumeration. Inherited from Role 2 §17.2 A-7 v1-substitute pattern.

**Artifact path.** `design/.health-implementer-design-work/architecture-questions/AQ-001-per-specialist-operator-profile-fields.md`.

### OQ-3 — Divergence-log cadence calibration trigger

**Why unresolvable now.** R9 + §17.1 Risk-3 + §17.2 Assumption-6 jointly flag the default cadence (N=5 sessions; X=20% per-session; Y=10 cumulative) as v1-calibration-pending. No corpus exists; first 5 Role 3 sessions provide calibration data.

**Resolution path.** At Role 3's 5th review pass (across-specialists), run divergence-rate analysis; recalibrate. Roll new threshold into `scripts/audit-reviewer-output.sh` config. Pattern mirrors Role 2 §18 OQ-5.

**Blocker.** Non-blocking for first 5 dispatches; blocks Q14 divergence-log-cadence LIVE status.

### OQ-4 — Frontier-tier judge model allowlist

**Why unresolvable now.** R15 specifies "frontier-tier judge model" but does not author the allowlist. Project-level policy decision: which model identities qualify as "frontier-tier" + which scoring scales are allowed (≤5 bands per R15).

**Resolution path.** Deploy-time policy bead authored by orchestrator (with user authority); not Role 3's content decision. Once authored, `scripts/audit-reviewer-output.sh --check judge-calibration` reads the allowlist file.

**Blocker.** Non-blocking for Role 3 design-doc finalize; blocks Q15 judge-calibration LIVE status.

### OQ-5 — Stratification axis-set sufficiency

**Why unresolvable now.** §17.1 Risk-6: the axis-set (population × dose × outcome × timing) may be insufficient for sufficiently-overlapping specialist domains. The substrate cataloged the axes from GRADE + Cochrane + AGREE II (Finding 8); the field validation against actual 14-specialist composition has not happened.

**Resolution path.** First 5 specialists with overlapping domains provide calibration. If stratification rate <50% on genuine contradictions (i.e., specialists frequently disagree at axes outside the catalog), Role 3 surfaces an `edge_case_class: stratification-axis-gap` finding; orchestrator extends the axis-set.

**Blocker.** Non-blocking; surfaces empirically.

### OQ-6 — Output schema interoperation with `aplus-research` gate JSONs

**Why unresolvable now.** Substrate Limitation 6: "The reviewer's output schema (R4 YAML block) has not been validated against the project's existing aplus-research gate JSON schemas. Integration risk: the reviewer's finding format may need adaptation to interoperate with `gate_attest.py` chain verification."

**Resolution path.** First Role 3 dispatch + schema-validator authoring (Q10) at Session B surfaces integration gaps. Schema delta is mechanical and bead-tracked.

**Blocker.** Non-blocking; blocks Q10 LIVE status; surfaces at first dispatch.

---

**OQ count.** 6 entries. Every §13-QA PROPOSED row covered (OQ-1 collective pointer covers Q1-Q15). AQ-001 inherited from Role 2 (OQ-2). Substrate-Limitation-derived OQs (OQ-3 cadence, OQ-4 judge allowlist, OQ-5 axis-set, OQ-6 schema interop) are within template's "honest non-zero" expectation. Zero PROPOSED rows lack §18 representation.

---

## Drafter status (per §9.1 QA-role Communication spec)

**Status.** draft-emitted.

**Artifact path.** `design/.health-edge-case-reviewer-design-work/qa-draft.md`.

**Specialist slug.** N/A — this is a Role 3 design-doc draft, not a specialist profile.

**Sections covered.** §11.1 (8-PF coverage table, 8 of 8 PFs verdicted), §11.2 (7 anti-patterns, each with source + recognition cue), §13-QA-rows (16 rows: 15 PROPOSED + 1 REFERENCED), §14 (8 edge cases, each with situation + failure mode + prescribed response + test stimulus), §15.2 (9 design-doc-time ACs + 7 post-deployment ACs = 16 ACs partitioned per Role 2 §15.2a/b precedent), §17 (7 Risks + 7 Assumptions + 5 Break Conditions), §18 (6 OQs covering all PROPOSED §13 rows + AQ-001 inheritance + substrate-Limitation-derived OQs).

**Gaps in substrate or upstream contracts surfaced to red-team-flag candidates (synthesizer + Phase 3 input).**

1. **Substrate Limitation 6 (output schema interoperation).** The R4 YAML block has not been validated against `aplus-research` gate JSON schemas. Surfaced as OQ-6; Q10 PROPOSED. Red-team-flag: synthesizer should verify the Phase-3 adversarial reviewer also surfaces this — if not surfaced, the gap may be invisible until first Role 3 dispatch.

2. **AQ-001 inheritance from Role 2.** The per-specialist operator-profile field enumeration is unresolved upstream. Role 3 cannot decide it (it's Role 1 ownership per orchestrator Interpretation A). Surfaced as OQ-2 with the dependency chain. Red-team-flag: synthesizer should ensure §10 (Context Loading — SE-drafter ownership) cites AQ-001 as an unresolved load-bearing dependency.

3. **Role 4 v1-substitute bridge protocol.** Per CONTINUATION_BRIEF §7 + Role 2 §17.2 A-6 + EC-6 in this draft: Role 4 is not yet deployed during Role 3's first several review passes. Role 3's output schema expects an adjudicator path. The bridge is v1-substitute software-security agent. Red-team-flag: synthesizer should verify the v1-substitute artifact path is consistent across Role 2 §17.2 A-6 + Role 3 EC-6 + Role 3 §17.1 Risk-7.

4. **`scripts/audit-reviewer-output.sh` does not exist.** §13-QA rows Q1-Q15 are all PROPOSED on this dependency. Same shape as Role 2 §13 PROPOSED-row count. Per OQ-1 RESOLVED in Role 2 (Role 2 owns its audit script), this draft assumes the same Resolution for Role 3 (Role 3 owns `scripts/audit-reviewer-output.sh`). Red-team-flag: synthesizer should verify orchestrator confirms this ownership assignment at Phase 5.

5. **Divergence-log cadence numerics uncalibrated.** Defaults (N=5, X=20%, Y=10) are educated guesses from substrate Insight + Anthropic harness retrospective. Surfaced as OQ-3 + §17.2 Assumption-6. Red-team-flag: synthesizer should verify the architect-drafter's Modes section (if Role 3 has a divergence-log-tuning Mode) cites the same defaults.

6. **Frontier-tier judge allowlist not yet authored.** OQ-4. Red-team-flag: synthesizer should confirm the SE-drafter's Tools section (§8) cites the allowlist file path placeholder.

7. **The medical-LLM domain ambiguities I did not invent answers for (per task brief).** (a) The exact composite-severity enum thresholds (P0-block / P1-revise / P2-annotate / P3-defer) are per the substrate R2 schema but the deterministic mapping rule from 4 axes to enum is not yet authored as bash; surfaced as part of OQ-1. (b) The atomic-claim decomposition pattern (Finding 9 FActScore pattern) is structural but the actual claim-decomposition rules are domain-specific medical-knowledge; surfaced as a deferred dependency on first wiki-entry review.

**Blockers.** None blocking design-doc finalize. The 15 PROPOSED §13-QA rows are non-blocking per Role 2 OQ-7 RESOLVED QA-strict project-wide rule; AQ-001 inheritance is non-blocking per Role 2 §17.2 A-7 v1-substitute pattern; Role 4 absence is non-blocking per EC-6 bridge protocol.

**Self-audit attestation.** This draft was authored against the task brief's mandatory-reads list. Inheritance from Role 1 §4 OUTBOUND (8 rows) and Role 2 §4.2 OUTBOUND (5 rows) is referenced inline (not duplicated). The 9 Findings + 15 Recommendations from `domain-research.md` are anchored by name in §11.1/§11.2/§13-QA/§14/§15.2/§17/§18 (architect-drafter's §3 will produce the full Findings table). PF coverage is 8/8. Anti-pattern count 7/8 max. Edge-case count 8/8 max. AC partition mirrors Role 2 §15.2a/b precedent. Risk/Assumption/Break-Condition counts within template ranges. OQ count 6/5 — exceeds template max of 5 by one. Rationale for the +1: the substrate has 15 enumerated Limitations and 8 cross-report patterns; AQ-001 inheritance is mandatory per task brief. Honest non-zero per template §18 spec exemplifies the "false zero is worse than honest non-zero" rule.

**Self-recognition flag (per CLAUDE.md §Self-recognition flags).** I notice I drafted 6 OQs not 5. I caught this on self-audit and am surfacing rather than silently dropping one. The template says "0–5"; I drafted 6 because the substrate's load-bearing limitations exceed 5. The synthesizer should adjudicate: either merge OQ-3 and OQ-5 (cadence + axis-set both v1-calibration-pending) or accept 6 with the rationale above.
