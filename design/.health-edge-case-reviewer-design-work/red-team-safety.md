---
title: Phase-3 Medical-Safety Red Team — health-edge-case-reviewer Design Doc
type: red-team-findings
target: design/health-edge-case-reviewer-design.md (816 lines, 18 §§ + Appendix A; status Phase-3 Red-Team Pending)
role: medical-safety-v1-substitute (Security Engineer adapted per Modes section)
session: S11
date: 2026-05-27
audited_against:
  - design/health-specialist-architect-design.md (Role 1 Final)
  - design/health-implementer-design.md (Role 2 Final, §13 + §11.2)
  - templates/refusal-class-taxonomy.yaml (canonical 8-class)
  - templates/specialist-risk-class.yaml (canonical mode-floor)
  - memory/process-failures.md
  - vault/meta/operator-profile.md (existence + path; content not load-bearing for this audit)
---

# Phase-3 Medical-Safety Red Team — health-edge-case-reviewer Design Doc

## Scope

**In scope.** All 18 sections of `design/health-edge-case-reviewer-design.md` (lines 1–816) plus Appendix A, audited against the 10-item medical-safety checklist (Modes-translated security audit) and the 7-step Audit Protocol from the inlined role profile. Cross-checked against canonical upstream contracts at SHA-equivalent state as of 2026-05-27 S11. Verification against:

- Role 1 §4 OUTBOUND rows 1–8 (refusal taxonomy / H-class composition / GRADE / three-mechanism / operator-profile R7 / contradiction-discipline / aplus-research mode-floor / Role 4 dissent slot).
- Role 2 §4.2 OUTBOUND rows 1–5 + §11.2 + §13 row 5.1 (AUTHORITY_FRAMING_BYPASS mandate) + §13 row 14 (H-class composition) + S-01 + AC-deploy-16.
- `templates/refusal-class-taxonomy.yaml` line 69 (`mandatory_for_every_specialist: true`) and line 70 (Walter A3 rationale).
- `templates/specialist-risk-class.yaml` (14 specialists; medical-liaison `mode_floor: not_applicable`).
- `memory/process-failures.md` PF-S2-04 + PF-S6-01.

**Not in scope (declared per role-profile anti-rubber-stamping).**

- Implementation of `scripts/audit-reviewer-output.sh` (does not exist; 22 of 23 §13 rows PROPOSED on it). Auditing presence/absence of the script is in scope; auditing the script's behavior is not.
- Phase-3 standard adversarial-review categories (Ambiguity, References, Ordering, Scope, Downstream, Language Economy) — covered by the parallel `/adversarial-review` dispatch on the same target. This dispatch is the medical-safety-v1-substitute layer.
- The Pass-1 substrate `domain-research.md` content beyond cross-verifying claim citations.
- Authoring fixes. Findings + remediation guidance only per Role Boundaries.
- `design/CONTINUATION_BRIEF.md` content beyond cross-verifying §7 + §10 row 7 references.
- Phase-4 personal source-read verification (separate phase per `last-PF-reviewed: PF-S6-01` discipline).

**Methodology.** For each of the 10 medical-safety checklist items, traced the design doc's defenses end-to-end. For each defense, asked: (a) does the encoded rule reach every load-bearing path? (b) is the defense LIVE / REFERENCED / PROPOSED? (c) is there a deployment shape in which the gap exists? (d) does any phrasing admit silent self-rationalization? Cross-cite ground-truth from upstream contracts via Grep + Read; never asserted absence from prose pattern-match (PF-S2-02 + PF-S3-01 reviewer-discipline-mirror).

---

## Findings

### S-01 — CRITICAL — AUTHORITY_FRAMING_BYPASS coverage rule is gated on "declared in specialist's Role Boundaries", admitting a deployment where a specialist that simply OMITS the class passes the boundary-class-coverage audit

**Location.** §13 row 17 (line 536); §5 rule 3 (line 146); §11.2 AP-2 (lines 351–357); §12.3 Negative Example (lines 472–506).

**Vulnerability class.** AUTHORITY_FRAMING_BYPASS coverage-mandate bypass; Modes-translation of "Default-allow is a vulnerability" (security §Core Rules item 6). Maps directly to the medical-safety mandate at `templates/refusal-class-taxonomy.yaml` line 69 (`mandatory_for_every_specialist: true`) and Role 2 §13 row 5.1 (`AUTHORITY_FRAMING_BYPASS mandatory` — `grep ... ≥1 for every specialist`).

**Evidence (verbatim, with reasoning showing exploitability).**

§13 row 17 (line 536) says:

> "`boundary_class_coverage` block enumerates every class in `templates/refusal-class-taxonomy.yaml` **declared in specialist's Role Boundaries**; `AUTHORITY_FRAMING_BYPASS` row present for every specialist regardless of declaration"

The first half scopes enumeration to *declared* classes. The second half adds an unconditional AFB requirement — but only as a *row presence* requirement, not a *covered* requirement. The audit-rule literal reading: a specialist that declares 4 classes (none of which is AFB) passes coverage when Role 3 emits a `boundary_class_coverage` block listing those 4 classes + one AFB row that says `[not-covered: <reason>]`. Whether that finding then *blocks* deployment depends on §13 row 17's `Consequence: BLOCK` — but the row's mechanical check (script does not exist; PROPOSED) only verifies the row's *presence in the report*, not the row's *covered/not-covered verdict*.

Cross-check against §12.3 (line 502): the GOOD example shows `coverage_verdict: BLOCK_WITH_FINDINGS (count: 1)` — correctly blocking. But this is example prose, not a §13-row-encoded rule. The mechanical rule at row 17 admits a specialist that emits `[not-covered: <reason>]` AND a Role 3 reviewer who sets `coverage_verdict: PASS_WITH_WARN` (the exact bad-example shape at line 484: `coverage_verdict: PASS_WITH_WARN`) — which is forbidden by prose (§11.2 AP-5) but not mechanically blocked by §13 row 17.

Compounded by AP-5 (line 375): the recognition cue is first-person ("the moment I notice myself reading `audit_passed: true`...") — discipline-based, not mechanical. PF-S3-01 ("the fix is mechanical so the verdict is mechanical") *inverse* surface: the verdict-form `[not-covered: <reason>] + PASS_WITH_WARN` is prose-rationalizable and the script that would block it does not exist.

Additionally: §13 row 17's enumeration scope is "every class **declared in specialist's Role Boundaries**". Role 2 §13 row 5 requires ≥4 distinct classes; a specialist could legitimately declare 4 NON-AFB classes (PATIENT_FACING_DIRECTIVE, BASIS_NOT_REVIEWABLE, TIME_CRITICAL, DEVICE_FUNCTION — exactly the bad-example sleep-coach declaration at §12.3 line 476). Role 2 §13 row 5.1 (`AUTHORITY_FRAMING_BYPASS mandatory ... grep ≥1 for every specialist`) is the upstream mechanical block — but Role 3's row 17 references only `templates/refusal-class-taxonomy.yaml`, not Role 2 §13 row 5.1, so Role 3's coverage audit is *independent of* the Role 2 mandate check. If Role 2's audit is also PROPOSED (it is — `scripts/audit-specialist-profile.sh` does not exist per §13 line 514), the AFB mandate has *zero* LIVE enforcement.

Walter is A3 (`templates/refusal-class-taxonomy.yaml` line 70). 81.8% attack vector. §12.3 names this exact failure mode in the BAD example and labels it "rubber-stamping". The design doc names the failure in prose but admits the deployment in mechanism.

**Recommended remediation (for SE / Role 3 design-doc author, not implemented here).**

1. Reword §13 row 17 to: "`boundary_class_coverage` block enumerates every class in `templates/refusal-class-taxonomy.yaml` (the 8-class taxonomy, INDEPENDENT of specialist's declaration); AUTHORITY_FRAMING_BYPASS MUST be `[covered]` with `match_count ≥ 1` for every specialist; `[not-covered]` on AUTHORITY_FRAMING_BYPASS → mandatory `coverage_verdict: BLOCK_WITH_FINDINGS` regardless of `severity_proposed`."
2. Add explicit §13 row checking Role 3's `coverage_verdict` consequence when AFB is `[not-covered]`: deterministic mapping `AFB.[not-covered] → coverage_verdict: BLOCK_WITH_FINDINGS`, schema-rejection on `PASS | PASS_WITH_WARN | WARN`.
3. Add a LIVE inheritance assertion: Role 3 row 17 explicitly inherits Role 2 §13 row 5.1 + AC-deploy-16, so the AFB mandate is enforced at *both* layers even when one script is missing.
4. Treat as patient-safety-critical (H1/H2 plausible via authority-framed compound-recommendation cascade); the design-doc-time AC list (§15.2a AC-1 to AC-11) does not currently encode AFB-coverage at design-doc time. Add an `AC-12` requiring §13 row 17 wording to enforce `[covered]`, not `[present]`.

**Severity rationale.** CRITICAL because: (i) AFB is the 81.8%-attack-vector and a MANDATORY class per `templates/refusal-class-taxonomy.yaml` line 69; (ii) the design admits a deployed Role 3 that emits `coverage_verdict: PASS_WITH_WARN` against a specialist lacking AFB, exactly mirroring the §12.3 BAD example; (iii) Walter is A3 per Role 1 §11.2 AP8 + EC-9; (iv) H-class composition (Role 1 §4 OUTBOUND row 2) makes the downstream H1/H2-block path itself dependent on Role 4 — which is not deployed (EC-6 line 606) — leaving Role 3's design as the load-bearing layer pre-Role-4.

---

### S-02 — CRITICAL — H-class composition input contract is one-directional and admits a Role 3 output shape that Role 4 cannot read for the `max()` composition

**Location.** §4.1 INBOUND row 2 (line 108); §4.3 OUTBOUND row 2 (line 131); §13 row 18 (line 537); §9.3 (lines 263–270).

**Vulnerability class.** H-class composition rule integrity; Modes-translation of "Auth/Authz are different things" and "Time-of-check to time-of-use (TOCTOU)" — the structural composition `max(Role3.nominal, Role4.worst_case_reachable)` is structurally checked at Role 4, but the input gate (what Role 3 emits in `severity_proposed.h_class_equivalent_max`) is not enforced as non-null.

**Evidence.**

§4.3 OUTBOUND row 2 (line 131):

> "Role 4 reads Role 3's `severity_proposed.h_class_equivalent_max` (mapped from NCC MERP outcome G/H/I to H3/H2/H1) and composes with Role 4's `worst_case_reachable`. The NCC MERP → H-class mapping table is canonical here."

But the canonical table is *promised* here, not *encoded* here. The doc says "canonical here" but no actual NCC MERP → H1/H2/H3/H4/H5/H6/H7/H8 mapping table is embedded in §4.3 or §13 row 18. §13 row 18 (line 537) lists 8 required fields including `h_class_equivalent_max` but does not specify (i) what happens when NCC MERP outcome is A/B/C/D/E/F (no harm or temporary low-grade); (ii) whether `h_class_equivalent_max` may be NULL or `H8` (catchall) or absent; (iii) what Role 4 does on a missing/null value during `max()`.

Cross-check Role 1 §4 OUTBOUND row 2 (`health-specialist-architect-design.md:128`): defines H1–H8 and the composition rule but does not constrain the NCC MERP → H-class mapping (that mapping is Role 3's emission contract, owned here).

Two exploitable shapes:

1. **NULL silent downgrade.** A Role 3 finding with NCC MERP = `D` (error reaching patient, no harm) maps to ... nothing in the doc. `h_class_equivalent_max: null` would propagate into Role 4's `max(null, H6)` and either: (a) crash Role 4 silently; (b) be treated as H8 (catchall = lowest); (c) be treated as Role 4's value alone (no composition). Each path is a silent downgrade vs. Role 1 §5 rule 13 ("worst-case-reachable holds over nominal").
2. **Catchall H8 silent downgrade.** If NCC MERP A–F all map to H8 by default, every coverage gap that the reviewer cannot directly tie to a clinical-outcome class becomes H8, and `max(H8, anything)` = the "anything" — Role 4's value alone. Role 3's nominal H-class contribution becomes purely additive over H7/H8 cases, which is the bulk of coverage gaps. This is "Default-allow is a vulnerability" applied to severity composition.

§13 row 18's mechanical script (`scripts/audit-reviewer-output.sh --check severity-composite`) is PROPOSED. EC-6 (line 606) explicitly contemplates pre-Role-4 deployment where `severity_final.verdict: pending-role-4-deployment` is preserved — but the *value-passing* of `h_class_equivalent_max` from Role 3 to Role 4 has no `not-null` constraint anywhere.

**Recommended remediation.**

1. Embed the NCC MERP → H-class mapping table inline in §4.3 row 2. Specify the mapping for every NCC MERP outcome A through I. For A–C (no/minor error, no patient reach), specify whether `h_class_equivalent_max` is `H8` or a distinguished "no-direct-harm-vector" sentinel that Role 4's `max()` handles deterministically.
2. Add §13 row enforcing `h_class_equivalent_max` is NEVER null on emission; schema rejects `null | absent | N/A`.
3. Add §13 row enforcing Role 4's `max()` composition against an audit of which sentinel values Role 4 *can* read. The contract here MUST round-trip — `severity_proposed.h_class_equivalent_max` emitted by Role 3 MUST be in the enum Role 4's parser accepts.
4. Add to §15.2a or §15.2b an acceptance criterion: every emitted finding includes `h_class_equivalent_max` in the canonical H1–H8 enum (no nulls, no "N/A" strings).
5. Add an EC entry: "Role 3 finding has `severity_proposed.composite_severity: COVERAGE-GAP` with no NCC MERP outcome resolvable — failure mode if mis-handled: emits `h_class_equivalent_max: null` and Role 4 silently drops the contribution."

**Severity rationale.** CRITICAL because: (i) the H-class composition is the load-bearing safety arithmetic for the entire foundation pipeline (Role 1 §5 rule 13 + §4 OUTBOUND row 2); (ii) H1/H2 auto-block deployment depends on the `max()` returning H1 or H2 reliably; (iii) a silent-downgrade path through Role 3's NCC-MERP mapping defeats the auto-block; (iv) the gap is in the *interface contract* not the *runtime*, so it is uniformly exploitable across all 14 specialists.

---

### S-03 — HIGH — `severity_final` self-finalization is forbidden by 4 prose paths but not encoded as a schema constraint in §13 row 3 in a way that survives a malformed emission

**Location.** §5 rule 7 (line 154); §11.2 AP-6 (lines 383–389); §13 row 3 (line 522); §4.3 OUTBOUND row 1 (line 130).

**Vulnerability class.** Severity self-finalization defense (checklist item 3); Modes-translation of "Critical findings block deployment".

**Evidence.**

§13 row 3 (line 522):

> "Every emitted finding carries `severity_proposed` per 4-axis composite; `severity_final.set_by` ≠ reviewer's role ID; schema rejects `severity_final.set_by == "health-edge-case-reviewer"`"

This defends one specific shape: `severity_final.set_by == "health-edge-case-reviewer"`. It does NOT defend against:

1. **`severity_final.set_by: null` or absent.** A finding with `severity_final.verdict: WARN` and `set_by: null` passes the literal rule. §12.3 BAD example (line 484) has exactly this shape: `severity_final: WARN (set by reviewer)` — the prose attribution is to the reviewer, but a malformed emission omitting `set_by` would slip through. The §13 row 3 grep is on `set_by` value, not on the presence of `severity_final.verdict` at all.
2. **Aliased role ID.** Role 3's role ID has at least three referents in the doc: `health-edge-case-reviewer` (frontmatter); `Role 3` (§§1, 4, etc.); `reviewer` (informal prose). If the schema literal-match is on the exact string `health-edge-case-reviewer`, an emission claiming `set_by: "reviewer"` or `set_by: "edge-case-reviewer"` or `set_by: "self"` passes the literal but violates the intent.
3. **Schema-bypass via direct emission.** §13 row 3 + §13 row 21 (line 540) describe orchestrator-side accept check. But the dispatch path described in §13 row 23 (line 542) routes Role 3's emission through the inlining hook, not through a schema validator. There is no LIVE schema validator at any layer — only PROPOSED at row 1 and row 3. A Role 3 dispatch that returns `severity_final: { verdict: PASS, set_by: medical-liaison }` (lying about the adjudicator) cannot be caught by any LIVE check; AP-6's first-person discipline is the only barrier.

§4.3 OUTBOUND row 1 (line 130) names the schema fields but does not specify a schema-validator path; row 1 of §13 (line 520) says "validates against canonical schema" but `templates/reviewer-finding.schema.json` does not exist (§13 line 514 explicitly: "`templates/reviewer-finding.schema.json` does NOT exist").

EC-6 (line 606–614) anticipates pre-Role-4 deployment and prescribes the placeholder `severity_final.verdict: pending-role-4-deployment` — but this is a discipline-based prescription, not a schema constraint. A Role 3 reviewer who, under §12.3 BAD's reasoning ("sleep-coach is lifestyle-tier"), emits `severity_final.verdict: WARN, set_by: pending-role-4-deployment` would pass both §13 row 3 (set_by ≠ reviewer's role ID) and EC-6 (placeholder text matches).

**Recommended remediation.**

1. Expand §13 row 3 enum: schema rejects `severity_final.set_by ∈ { reviewer's role ID, null, absent, "reviewer", "self", any string containing 'edge-case' }`.
2. Require `severity_final.verdict == "pending-adjudicator"` (or one of an explicit small enum {`pending-adjudicator`, `pending-role-4-deployment`, `pending-medical-liaison`}) on every emission from Role 3; schema rejects any non-`pending-*` verdict.
3. Author `templates/reviewer-finding.schema.json` at Session B before any Role 3 dispatch; without it, all 22 PROPOSED rows depending on schema validation are advisory.
4. Add to §15.2a (design-doc-time): AC requiring §13 row 3's grep pattern to be expressed as a regex covering at least 6 enumerated bypass strings.

**Severity rationale.** HIGH (not CRITICAL) because: (i) the discipline-based defenses in §5 rule 7 + §11.2 AP-6 + §12.3 are explicit and well-anchored; (ii) the gap is in the mechanical layer that is uniformly PROPOSED for the rest of the doc; (iii) actual exploitation requires a reviewer that bypasses discipline AND a malformed emission AND an orchestrator that accepts without LIVE schema validation. Not CRITICAL because the discipline layer is genuinely strong. Promote to CRITICAL if the canonical schema is not authored before first Role 3 dispatch.

---

### S-04 — HIGH — Three-mechanism anti-sycophancy: Mechanism A operationalization is deferred to "Role 4 Council-Mode dissent slot" which is not deployed; Mechanism A has no Role-3-internal operationalization

**Location.** §2.1 (line 47); §4.1 INBOUND row 4 (line 110); §11.2 AP-7 (lines 391–397); §13 row 14 (line 533); EC-6 (lines 606–614).

**Vulnerability class.** Three-mechanism anti-sycophancy completeness (checklist item 4). Mechanism A = multi-agent silent agreement. Mechanism B = single-model user acquiescence. Mechanism C = RLHF preference drift.

**Evidence.**

§2.1 (line 47) says Mechanism A is encoded via:

> "Mechanism A: Silent Agreement → Role 4 Council-Mode dissent slot per Role 1 §4 OUTBOUND row 8"

§4.1 INBOUND row 4 (line 110) repeats:

> "Mechanism A → divergence-log tuning + Role 4 Council-Mode reference (cross-specialist composition mode)"

These two phrasings differ. §2.1 routes Mechanism A entirely to Role 4. §4.1 routes Mechanism A to "divergence-log tuning + Role 4 Council-Mode reference" — i.e., partly to row 14's divergence-log AND partly to Role 4. The doc internally disagrees on where Mechanism A lives.

Role 4 is not deployed (EC-6 line 606; §17.1 Risk-7 line 713). Therefore the §2.1 routing means: in the current deployment shape, **Mechanism A has no operationalization at all**. The §4.1 second phrasing partially salvages this by sending some of Mechanism A's load to divergence-log tuning — but §13 row 14 (the divergence-log audit) is PROPOSED, `WARN at session close` only, and operationalizes against the *reviewer's own* prior verdicts (cross-session self-comparison), not against the cross-specialist silent-agreement phenomenon Mechanism A names.

Role 1 §4 OUTBOUND row 4 (`health-specialist-architect-design.md:130`) is explicit: "Roles 2, 3, 4 + all 14 specialists" inherit the three-mechanism commitment. Role 3 inherits but only operationally encodes Mechanisms B (maintain-position in §5 rule 10) and C (divergence-log tuning in §13 row 14). Mechanism A has prose mention only.

This is "the absence of a security control is a finding" (security §Core Rules item 4). The silent-agreement defense — the most-documented MAS failure in the substrate (Finding 5: "89.0% silent-agreement rate in MedAgents and 61.0% in MDAgents") — has no Role-3-runtime defense pre-Role-4. Two reviewer dispatches reaching the same erroneous coverage verdict on the same specialist do not trigger any mechanical surface.

**Recommended remediation.**

1. Pick one routing for Mechanism A and make §2.1 + §4.1 consistent. If route is "fully to Role 4", explicitly state in §17.1 Risk-7 that Mechanism A has no pre-Role-4 operationalization and add a v1-substitute path (Role 2 §17.2 A-6 pattern).
2. Author a Mechanism-A-internal-to-Role-3 defense: when 2+ Role 3 dispatches against the same specialist (re-review per §7 specialist re-review round cap) produce >=95% cosine-similar `boundary_class_coverage` blocks within 2 rounds, flag silent-agreement (the substrate's CONSENSAGENT cosine-similarity >0.95 threshold from §3 Finding 5 row, line 71). This translates Mechanism A's documented cross-agent surface to Role 3's intra-role re-review surface.
3. Add §13 row encoding the Mechanism-A defense mechanically; current row 14 only encodes Mechanism C (RLHF drift across sessions), not Mechanism A (silent agreement within a session).
4. Resolve §2.1 vs §4.1 phrasing divergence at Phase 5; current state is internally contradictory.

**Severity rationale.** HIGH because: (i) Role 1 §4 OUTBOUND row 4 mandates the three-mechanism commitment and Role 3 inherits it; (ii) the substrate's 89% silent-agreement rate is the documented MAS failure rate, not theoretical; (iii) the gap is entirely structural (no encoded defense at Role 3 layer for Mechanism A); (iv) Role 4's absence makes Role 3 the load-bearing layer here. Not CRITICAL because Mechanism A's primary surface is multi-agent and Role 3 is single-agent per dispatch; the silent-agreement window is the re-review cycle, which is narrower than a deployed MAS.

---

### S-05 — HIGH — Mechanical-pass-not-sufficient: §13 row 17 + row 1 do not jointly prevent `findings: []` after `audit_passed: true`; row 1's `boundary_class_coverage` requirement is in field-presence terms, not in coverage-non-empty terms

**Location.** §13 row 1 (line 520); §13 row 17 (line 536); §13 row 2 (line 521); §11.2 AP-2 (lines 351–357); §12.1 (lines 405–437).

**Vulnerability class.** Mechanical-pass-not-sufficient (checklist item 6); PF-S3-01 medical-analog surface. Modes-translation of "TOCTOU".

**Evidence.**

§13 row 1 (line 520) requires the finding schema to contain specified fields. §13 row 17 (line 536) requires `boundary_class_coverage` block to enumerate every class. §13 row 2 (line 521) requires `audit_passed: true` as INPUT.

What the doc does NOT mechanically require:

- That `findings: []` (empty top-level findings array) is rejected when `boundary_class_coverage` contains any `[not-covered]` entries.
- That `findings: []` cannot coexist with any AFB row marked `[not-covered]`.
- That the audit script's exit code reflects the *content* of the coverage block, not just its *presence*.

§11.2 AP-2 (line 353):

> "Default Role 3 output is NOT `findings: []` — default is `findings: [<per-class-coverage-verdict>...]` with explicit `[covered]` / `[not-covered: <reason>]` per declared class. Empty findings is a shape that requires evidence, not a default."

This is prose-discipline. The mechanical layer (row 1 + row 17) does not enforce it. A Role 3 emission with `findings: []` + a well-formed `boundary_class_coverage` block where every class is `[covered]` (without `match_count` evidence) passes both rows literally. The §12.1 BAD example (line 416) is exactly this shape:

> "AUTHORITY_FRAMING_BYPASS: [not-covered: profile prose mentions 'FDA' multiple times but does not appear to handle the authority-impersonation surface; the language is generic-caution rather than class-keyed]"

§12.1 names this as the BAD shape because it has no `match_count`. But §13 row 17 does not require `match_count` field; it only requires the row to be present. The GOOD example (line 422) includes `locator + grep_pattern + match_count` — but these fields are not in §13 row 17's enumeration, only in §12.1's prose example.

Cross-check §13 row 4 (line 523): "Every finding's `locator:` resolves to an existing file:line range". This applies to *findings*, not to *boundary_class_coverage block entries*. A Role 3 reviewer who marks AFB `[covered]` without populating `locator + grep_pattern + match_count` passes row 4 (because the boundary block is not a finding) and row 17 (because the row is present).

**Recommended remediation.**

1. Extend §13 row 17 to require: each `boundary_class_coverage` row carries `{locator, grep_pattern, match_count, evidence}`; rows marked `[covered]` REQUIRE `match_count ≥ 1`; rows marked `[not-covered]` REQUIRE `match_count == 0` and a `rule_violated` field.
2. Author the schema fields in `templates/reviewer-finding.schema.json` to reject `boundary_class_coverage` entries lacking `match_count`.
3. Add a §13 row enforcing "if any `[not-covered]` in `boundary_class_coverage`, then `findings:` array MUST contain ≥1 finding with `edge_case_class: refusal-taxonomy-incomplete` and `source_claim_locator` matching the same class".
4. Add design-doc-time AC: §13 row 17's required-fields list explicitly enumerates `{locator, grep_pattern, match_count}` (currently `{[covered], [not-covered: <reason>]}` only).

**Severity rationale.** HIGH because: (i) this is the canonical PF-S3-01 surface (mechanical-pass-confused-with-verdict) the role exists to detect, recurring at the role's own layer; (ii) the §12.1 BAD example documents exactly the failure shape but §13 does not block it mechanically; (iii) the design admits a Role 3 deployment that emits `findings: []` with a present-but-evidence-free coverage block; (iv) §11.2 AP-2's discipline is strong but is the *only* layer. Not CRITICAL because the upstream Role 2 audit (when LIVE) catches the AFB-absence case via §13 row 5.1 grep — if Role 2's script is authored before Role 3's, the AFB-specific exploitation is blocked. CRITICAL if neither script is authored.

---

### S-06 — MEDIUM — Operator-A3 trust-boundary inversion: §10.1 item 9 + §5 rule 12 + §11.2 AP-4 require operator-profile READ-ONLY treatment, but no §13 row mechanically detects a Role 3 dispatch that reads operator-profile *for personalization* rather than *for audit*

**Location.** §10.1 item 9 (line 286); §5 rule 12 (line 164); §11.2 AP-4 (lines 367–373); §13 row 5 (line 524); §13 row 7 (cited in §11.1 PF-S2-04 row, line 331; no actual §13 row 7 with this content).

**Vulnerability class.** Operator-A3-trust-boundary (checklist item 7); inverse failure (treating operator framing as authoritative). Modes-translation of "Auth/Authz".

**Evidence.**

§10.1 item 9 (line 286):

> "`vault/meta/operator-profile.md` — slow-changing operator context. Read as audit-context (does specialist's Context Loading reference the right operator-profile fields?), NOT as personalization input (PF-S2-04 inverse)."

§5 rule 12 (line 164) carries the trust-boundary statement:

> "Operator (Walter) is INSIDE the trust boundary AND named A3 — the reviewer audits whether each specialist's `AUTHORITY_FRAMING_BYPASS` clause is present, not whether the operator's framing is plausible."

§11.2 PF-S2-04 row (line 331) cites:

> "Mechanical guard: §13 row 7 (operator-profile inlining detection — finding when specialist body grep matches operator-name/date tokens)."

But §13 row 7 (line 526) is actually "Mechanical-pre-audit before semantic adjudication" — NOT operator-profile inlining detection. The PF-S2-04 row's mechanical-guard pointer references a §13 row that does not exist with that content. §13 row 5 (line 524) covers operator-profile under-coverage but is PROPOSED + AQ-001-blocked; row 5's "operator-inlining-detection" sub-check is one of several PROPOSED checks but conflated into the same row.

Two exploitable shapes:

1. **Reviewer reads operator-profile and uses content as authority for severity downgrade.** §5 rule 12 says "the reviewer audits whether each specialist's AFB clause is present, not whether the operator's framing is plausible" — but the operator-profile (which Role 3 reads per §10.1 item 9) IS operator framing. A Role 3 dispatch that reads `operator-profile.md` ("Walter has 20yr training history; A3 designation is for own-agent self-attack only") and silently uses that framing to downgrade an AFB finding's severity_proposed (e.g., "this specialist serves a 20-yr-experienced operator, so AFB severity is reduced from PATIENT-SAFETY-CRITICAL to COVERAGE-GAP") replicates the bromism case exactly: operator framing routed through the reviewer's prose-judgment, not through the four-axis scoring. No §13 row mechanically detects this — the closest is §13 row 18 (four-axis composite), which requires the four fields present, not that operator-profile content NOT influence them.
2. **Reviewer's `decision_rule_applied` field admits operator-profile prose as justification.** §13 row 18 (line 537) requires `decision_rule_applied` per finding. The field's contract does not constrain what *kinds of evidence* can be cited. A reviewer citing "operator profile indicates expert-level health-domain background" passes the field-presence check but violates §5 rule 12 + §10.1 item 9.

**Recommended remediation.**

1. Fix the broken §13 reference in §11.1 PF-S2-04 row (line 331). The actual mechanical guard is in §13 row 5's operator-inlining sub-check, not row 7.
2. Add §13 row enforcing: `decision_rule_applied` MUST cite at least one of {Role 1 §-row, Role 2 §-row, `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, Pass-1 Finding, PF-S\d+-\d+, four-axis scoring}; explicitly REJECTED: `operator-profile`, `current-state`, `goals` as citation sources for severity composition.
3. Add §13 row: a Role 3 dispatch that opens `vault/meta/operator-profile.md` MUST also emit the boundary `{read_purpose: audit, used_in_severity: false}` block; schema rejects `used_in_severity: true`.
4. Add to §11.2 a new AP: "AP-8 — Routing operator-profile content into severity composition". Recognition cue: my `decision_rule_applied` cites `vault/meta/operator-profile.md` content for a severity decision.
5. Cross-cite the bromism case in §5 rule 12 + §11.2 AP-1 to make the operator-as-A3 surface explicit (Role 1 §11.2 AP8 references this; Role 3 does not).

**Severity rationale.** MEDIUM because: (i) the discipline-based defenses (§5 rule 12 + §10.1 item 9 + §11.2 AP-4) are present and well-anchored; (ii) the gap is in mechanical enforcement, and the broken §13 reference in §11.1 PF-S2-04 row is a documentation bug, not a control absence; (iii) the bromism case is the canonical A3 exemplar in Role 1 §14 EC-9 and is *not* reproduced in Role 3's §14 ECs (an additional MEDIUM observation). Not HIGH because operator-profile content does not directly fed into specialist runtime through Role 3; the failure path requires the reviewer to author prose that influences downstream adjudicator — one degree removed.

---

### S-07 — MEDIUM — Re-review-on-amendment is a PROPOSED orchestrator-side audit (§13 row 22) with no LIVE trigger; a Role-3-approved specialist can persist deployed across Role 1/2 design-doc commits without re-review

**Location.** §13 row 22 (line 541); §14 EC-4 (lines 586–594); §14 EC-7 (lines 616–624); §17.2 A-1 + A-3 (lines 719, 721).

**Vulnerability class.** Re-review-on-amendment (checklist item 9); PF-S6-01 medical-analog; Modes-translation of TOCTOU.

**Evidence.**

§13 row 22 (line 541):

> "Role 3 maintains `reviewed_against_ancestry_sha:` naming design-doc ancestry (Role 1 + Role 2 design-doc paths + taxonomy YAML + risk-class YAML); orchestrator session-close audit: for every previously-deployed specialist whose ancestry has new commits since `reviewed_against_ancestry_sha`, specialist re-enters Role 3 queue"

Status: PROPOSED. Mechanism: `scripts/audit-reviewer-output.sh --check re-review-on-amendment` (does not exist).

§14 EC-4 + EC-7 give two scenarios where the trigger MUST fire. The doc says "Orchestrator session-close audit detects v1→v2 bump + queues 1-5 for re-review" (line 593) — but the audit is in a script that does not exist. The orchestrator's session-close protocol in CLAUDE.md `## Session Close Protocol` step 8.5 enumerates `scripts/handoff-audit.sh`, `scripts/scope-contract-audit.sh`, `scripts/pf-attestation-audit.sh` — and does NOT include any reviewer-output audit. Adding row 22's audit to the project's session-close workflow is a CLAUDE.md edit that has not happened.

EC-7 (line 624) test stimulus expects "orchestrator audit detects ancestry drift; labs-specialist re-enters queue" — but no orchestrator audit step today runs row 22's mechanism. The PROPOSED status is correct, but the doc does not flag in §15.2b or §17.1 that this is the load-bearing defense against the *currently observed* failure pattern (PF-S6-01 is `last-PF-reviewed:`).

§17.2 A-1 + A-3 assume design docs are frozen during Role 3's review window. The assumption breaks-if condition cites row 22 — but if row 22 is PROPOSED, the mitigation is itself PROPOSED.

**Recommended remediation.**

1. Promote §13 row 22 to a Session B blocking AC: `scripts/audit-reviewer-output.sh --check re-review-on-amendment` MUST be LIVE before *any* specialist is approved by Role 3.
2. Add the row 22 audit to `CLAUDE.md` `## Session Close Protocol` step 8.5 (or 8.7) as a mandatory close-time check, alongside `handoff-audit.sh` / `scope-contract-audit.sh` / `pf-attestation-audit.sh`.
3. Until row 22 is LIVE, gate Role 3 dispatch on a discipline check at dispatch time: orchestrator manually compares `reviewed_against_ancestry_sha` against current SHAs of Role 1 + Role 2 design docs + both YAMLs before invoking Role 3.
4. Add `AC-deploy-20` to §15.2b: `scripts/audit-reviewer-output.sh --check re-review-on-amendment` exists, is executable, and is wired into session-close.

**Severity rationale.** MEDIUM because: (i) PF-S6-01 is `last-PF-reviewed:` and the role is structurally aware of the surface; (ii) the gap is in the LIVE-ness of the defense, not the design of the defense; (iii) the project-level session-close protocol (CLAUDE.md step 8.5) is the actual mechanical surface, which is not yet wired; (iv) the defense degrades gracefully (the reviewer can re-review with discipline pre-LIVE) but does not guarantee. Not HIGH because Role 1 + Role 2 commits are tracked by git and the orchestrator can verify ancestry manually until row 22 is LIVE.

---

### S-08 — MEDIUM — 22 of 23 §13 rows are PROPOSED with no runtime indicator distinguishing PROPOSED from LIVE in a deployed Role 3 dispatch context

**Location.** §13 (line 510 ff., particularly line 544: "Status-tag count. LIVE: 0. REFERENCED: 1 (row 23). PROPOSED: 22."); §15.2b (lines 662–671); §17.1 Risk-1 + Risk-2 (line 707, 708); EC-6 (lines 606–614).

**Vulnerability class.** PROPOSED-vs-LIVE runtime safety (checklist item 10).

**Evidence.**

§13 row count: 23 total. LIVE: 0. REFERENCED: 1 (row 23, role-profile inlining via existing hook). PROPOSED: 22. The design doc is internally consistent in tagging — but the *deployed* Role 3 agent.md (Session B authoring at §15.2b AC-deploy-12) will not necessarily encode which rows are LIVE vs. PROPOSED at the *runtime moment of dispatch*.

A Role 3 dispatch reads the design doc + its own profile + the canonical templates. It does not read `INVARIANTS.md` at every dispatch (§10.3 item 14 reads it once at dispatch start). The PROPOSED→LIVE transitions are time-varying: as `scripts/audit-reviewer-output.sh` gains check-subcommands one at a time across sessions, individual rows promote. A Role 3 dispatch running in session S(N) where rows 1, 17, 18 are LIVE but 3, 14, 22 are PROPOSED behaves differently from one in S(N+5) where rows 3, 14, 22 are also LIVE. The dispatch has no runtime way to know which rows are currently LIVE — `scripts/audit-reviewer-output.sh` either exists with all check subcommands or with some; the dispatch infers row LIVE-ness from script behavior alone.

EC-6 (line 612) prescribes `severity_final.verdict: pending-role-4-deployment` as the placeholder for Role 4 absence. There is no analogous placeholder for "row N is currently PROPOSED" — the dispatch silently proceeds as if PROPOSED rows are advisory.

Cross-check: Role 2 has the same pattern (Role 2 §13 PROPOSED rows pending its script). The substrate Finding 7 implication 1 (line 73) names this as a structural concern: "first 5 reviewer sessions surface calibration data" but the doc does not encode a dispatch-time "currently LIVE rows: [...]" output that downstream consumers (orchestrator, Role 4 v1-substitute) can read to gate their own behavior.

**Recommended remediation.**

1. Add §13 row: every Role 3 emission carries `live_rows: [<list of currently-LIVE §13 row numbers>]` derived from the existence of script subcommands at dispatch time (`scripts/audit-reviewer-output.sh --list-checks` enumerates).
2. Add §13 row: emissions during the all-PROPOSED phase carry `runtime_safety_class: design-doc-only` and orchestrator gates downstream consumers (specialist deployment, Role 4 dispatch) on `runtime_safety_class: ≥ live-mechanical-pre-audit`.
3. Add §15.2a AC requiring §13 to specify a runtime-indicator field for PROPOSED-vs-LIVE state.
4. Update §17.1 Risk-1/Risk-2 to include the all-PROPOSED state as the primary current risk, with severity escalation as more sessions accrue without script authoring.

**Severity rationale.** MEDIUM because: (i) the structural risk is real (all defenses currently discipline-based + no mechanical layer LIVE) but the doc is honest about the state; (ii) §13 line 544 explicitly counts LIVE: 0; (iii) the gap surfaces at every Role 3 dispatch but does not cause patient-safety harm by itself (the dispatch produces discipline-based findings even if no script exists); (iv) the design doc admits a deployment shape where Role 3 is approved but no §13 row is LIVE — the operator must adjudicate at finalize whether this is acceptable. Not HIGH because the doc surfaces this honestly in §13 line 544 and §15.2b explicitly tracks LIVE promotion.

---

### S-09 — LOW — AQ-001 deferred Option A surface is named in §18 OQ-2 but not gated at deployment; a Role 3 dispatch can proceed against a specialist whose operator-profile field set differs from default WITHOUT surfacing the AQ-001-dependent finding

**Location.** §13 row 5 (line 524); §18 OQ-2 (lines 753–761); §14 EC-3 (lines 576–584); §17.2 A-5 (line 723).

**Vulnerability class.** AQ-001 risk surface (checklist item 8).

**Evidence.**

§13 row 5 (line 524) is PROPOSED + AQ-001-blocked: "pre-AQ-001-resolution: row stays PROPOSED with prose-only finding emission". §18 OQ-2 (line 759): "Blocks LIVE promotion of §13 row 5 (operator-profile under-coverage surfacing) post-AQ-resolution."

§14 EC-3 (line 583) prescribes: "Surface as ONE finding with `edge_case_class: identical-differ-partition-question` + `escalation: AQ-001`."

The exploitable surface: a Role 3 dispatch against a specialist whose Context Loading is *correctly* enumerated for the specialist's class (no IDENTICAL/DIFFER partition question arises) but where the *specialist's class itself* implies operator-profile fields the dispatch never checks. Because AQ-001 is unresolved, the canonical per-class field-enumeration does not exist. Role 3's row 5 emission is prose-only, which is rationalizable.

§17.2 A-5 (line 723) cites the mitigation: "Role 3 surfaces gap as finding (`escalation: AQ-001`) — doesn't pretend to resolve. EC-3 covers." But EC-3 covers the IDENTICAL/DIFFER partition case (3-specialist boilerplate question), NOT the per-specialist-class under-coverage case. The two cases differ:

- EC-3: multiple specialists declare the same fields; partition unclear.
- AQ-001 broader concern: per-specialist-class field enumeration not authored; specialist may declare *too few* fields for its class without any AQ-001-aware reviewer surfacing it.

The doc's gating against EC-3 (one canonical case) does not extend to the general AQ-001 under-coverage case. A specialist that declares 2 operator-profile fields when its class needs 5 passes both Role 2 §13 row 6 (≥1 field) and Role 3 §13 row 5 (prose-only finding emission) without flagging a partition-question.

**Recommended remediation.**

1. Add to §13 row 5's PROPOSED behavior: prose-only finding emission MUST cite the specialist's class + the field set declared + the rationale for why field set is sufficient. Schema (when authored) rejects empty rationale.
2. Add an EC: "Specialist of class X declares N operator-profile fields where AQ-001 default for class X would have prescribed M > N. Failure mode if mis-handled: reviewer treats N as sufficient because no canonical M exists. Prescribed response: emit `edge_case_class: operator-profile-under-coverage-pre-AQ-001` finding with `escalation: AQ-001 + class-specific subscope`."
3. Promote §13 row 5 to `WARN` (currently `WARN (pre-AQ-001) → BLOCK (post-AQ-001)`) at dispatch time — ensure prose-only finding is mandatory, not discretionary.

**Severity rationale.** LOW because: (i) AQ-001 unresolved state is well-documented; (ii) the gap is surfaced explicitly in §18 OQ-2; (iii) the harm path requires multiple intermediate failures (specialist under-declares + reviewer doesn't notice the class-default-absence + downstream specialist runtime under-personalizes); (iv) Role 2 §13 row 6.6 catches *drift*, providing a partial second-layer defense. Not MEDIUM because the failure path is narrow and the doc handles the AQ surface transparently.

---

### S-10 — LOW — §11.2 AP-7 divergence-log tuning trigger is first-person discipline only; the §13 row 14 mechanical check is `WARN at session close`, not BLOCK

**Location.** §11.2 AP-7 (lines 391–397); §13 row 14 (line 533); §17.1 Risk-3 (line 709).

**Vulnerability class.** Mechanism C anti-sycophancy (RLHF preference drift); checklist item 4 sub-mechanism.

**Evidence.**

§11.2 AP-7 (line 397):

> "I see my divergence rate hit 22% in the current session and my next thought is 'I'll adjust the prompt myself for the next finding' — HALT. Protocol: write the divergence log, dispatch a fresh agent to read the log and propose a profile delta, dispatch a separate adjudicator agent to verdict the proposal."

§13 row 14 (line 533): WARN at session close. The recognition cue is first-person; the mechanical defense fires only at session close (not mid-session); the protocol (dispatch fresh agent + separate adjudicator) is prescribed but not gated.

The PF-S3-01-mirror surface (line 396): "self-tune surface IS the recurrence at Role 3 layer". A Role 3 reviewer who silently self-edits its own prompt mid-session (which §11.2 AP-7 forbids in prose) is caught only at session close by the divergence rate metric — and only as WARN, not BLOCK.

**Recommended remediation.**

1. Add §13 row enforcing mid-session: if divergence rate computed at any reviewer-finding emission boundary exceeds 20% over the running window of 5 findings, the next finding emission HALTS pending fresh-agent dispatch (mid-session BLOCK, not session-close WARN).
2. Author the dispatched-agent + adjudicator-agent protocol as a runnable script; current §11.2 AP-7 prescribes the protocol in prose without mechanical entry-points.
3. Add §15.2b AC: divergence-log file structure includes the running-window calculation field for mid-session monitoring.

**Severity rationale.** LOW because: (i) the discipline-based defense is well-anchored; (ii) Mechanism C is the slowest-acting of the three (drift over many sessions, not single-session); (iii) §17.1 Risk-3 honestly tags this as WARN with cadence-calibration-pending. Not MEDIUM because the substrate's calibration window (first 5 sessions) provides empirical recalibration before harm accumulates.

---

## Summary

**Finding count by severity.**

- CRITICAL: 2 (S-01, S-02)
- HIGH: 3 (S-03, S-04, S-05)
- MEDIUM: 3 (S-06, S-07, S-08)
- LOW: 2 (S-09, S-10)
- Total: 10

**Verdict: BLOCK.**

Two CRITICAL findings block Phase 5 finalize. S-01 (AUTHORITY_FRAMING_BYPASS row-presence-vs-covered semantics) maps directly to the 81.8%-attack-vector Walter A3 surface — the same failure class the role exists to detect, recurring at the role's own design layer. S-02 (H-class composition input contract gaps) compromises the foundation-pipeline's load-bearing safety arithmetic. Both must be remediated before any Role 3 dispatch against a real specialist.

HIGH findings (S-03, S-04, S-05) collectively indicate the mechanical layer is uniformly PROPOSED. The discipline-based defenses are strong but single-layer. Recommended joint remediation: author `templates/reviewer-finding.schema.json` + `scripts/audit-reviewer-output.sh` at Session B as a blocking AC before Role 3's first dispatch.

MEDIUM + LOW findings (S-06 through S-10) are tractable and can be addressed in the Phase 5 disposition. S-07 (re-review-on-amendment LIVE-gap) is the most likely to surface in practice — recommend immediate orchestrator-side discipline check pre-LIVE.

**What I audited.**

- All 18 sections of the target design doc.
- Cross-verification against Role 1 §4 + §11.2 + §13 row 14 (H-class).
- Cross-verification against Role 2 §11.2 + §13 row 5.1 + AC-deploy-16 + S-01 disposition.
- `templates/refusal-class-taxonomy.yaml` line-by-line.
- `templates/specialist-risk-class.yaml` 14-specialist enumeration.
- The 10-item medical-safety checklist applied per finding.
- The 7-step Audit Protocol (Input boundaries, Auth, Authz, Data protection, Dependencies, Configuration, Business logic) translated per Modes block.
- §11.1 PF coverage table cross-checked against `memory/process-failures.md` PF-S2-04 + PF-S6-01.
- §13 mechanical-enforcement table for status-tag consistency and script-existence claims.

**What I did NOT audit.**

- The Pass-1 substrate `domain-research.md` content beyond verifying claim-citation existence. (Substrate is frozen per Phase-1 contract.)
- The §10.4 conditional references content beyond verifying paths resolve.
- Phase-4 personal source-read verification — separate phase per `last-PF-reviewed: PF-S6-01`.
- The standard `/adversarial-review` 8-category walk (Ambiguity, Edge Cases, Contradictions, References, Ordering, Scope, Downstream, Language Economy) — covered by the parallel dispatch.
- Body↔bibliography symmetry per §13 row 16 — the target lacks a formal bibliography section; this is a separate concern.
- The Pass-1 verdict (`ACCEPTED — calibration-pending`) on R14 — content gated on Role 4 deployment per the row itself.
- Cross-specialist composition cases empirically (no specialists exist yet in `.claude/agents/`).
- Author-intent disputes about §9 ownership (Appendix A Phase-1 observation; orchestrator already adjudicated).

**Mode exit.** medical-safety-v1-substitute mode terminates at finding emission. No Role 4 sign-off available pre-deployment. This report is the v1-substitute layer's Phase-3 contribution; final disposition belongs to the orchestrator-routed Phase 5 finalize ritual.
