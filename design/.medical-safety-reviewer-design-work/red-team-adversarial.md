---
title: Role 4 medical-safety-reviewer Design Doc — Adversarial Red-Team Review
type: red-team-findings
target: design/medical-safety-reviewer-design.md
target_sha_at_review: (orchestrator records)
reviewer: /adversarial-review skill (fresh-context dispatch)
session: S12
created: 2026-05-28
disposition_owner: orchestrator (Phase 4 per PF-S3-01 guard)
---

# Role 4 medical-safety-reviewer Design Doc — Adversarial Red-Team Review

Walk performed against `design/medical-safety-reviewer-design.md` (777 lines, 18 sections + Appendix A) per `~/.claude/skills/adversarial-review/SKILL.md`. 8 standard categories (A, E, C, R, O, S, D, L) plus 3 agent-design-doc-specific categories (CCI, AT, UA) covered. Cross-doc anchor integrity verified against substrate (`domain-research.md`), Role 1 / Role 2 / Role 3 design docs, `INVARIANTS.md`, `memory/process-failures.md`, `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`, and `design/DESIGN_DOC_TEMPLATE.md`.

Findings are descriptive only. Disposition (Legitimate / Rejected / Adopted-from-Rejected) is the orchestrator's Phase 4 work per PF-S3-01 guard.

Numbering: F-001 onward. Severity tiers per skill: Critical / High / Medium / Low. Category codes per task brief: C / CC / M / S / CCI / AT / UA + standard 8 (A / E / R / O / D / L).

---

## F-001 — §13 row pointer "Q-COS" not renumbered after Phase 5 synthesis consolidation

| Field | Value |
|-------|-------|
| Category | C — Internal Contradiction (renumbering propagation defect; AP-INCOMPLETE-PROPAGATION class per Risk-7) |
| Section | §5 rule 11 (line 175) |
| Severity | Major |
| Affected | design/medical-safety-reviewer-design.md:175 |

**Description.** Core Rule 11 cites "the cosine-similarity audit (§13 row Q-COS)" but no §13 row carries the label `Q-COS`. The actual cosine-similarity audit lives at §13 row 22 (line 538: "Intra-judge silent-agreement cosine audit (Mechanism A)"). The `Q-COS` label is a stale QA-drafter row ID that survived Phase 5's "20 architect-master + 7 SE + 9 QA = 36 → 25" deduplication without being rewritten. Self-attested Risk-7 (line 703) explicitly warns about this defect class and §15.2a does not pick it up.

**Evidence.** Line 175: `the cosine-similarity audit (§13 row Q-COS) flags`. §13 table (lines 515–541) contains rows 1–25 with no `Q-COS` label. Row 22 mechanism: `--check judge-cosine-similarity`. Synthesis preamble line 513 itself names `QA Q-COS`-style IDs as the old namespace being deduplicated.

**Fix.** Replace `§13 row Q-COS` with `§13 row 22`.

---

## F-002 — §11.1 PF-S2-04 cites stale row "Q1" instead of current §13 row 21

| Field | Value |
|-------|-------|
| Category | C — Internal Contradiction (renumbering propagation defect) |
| Section | §11.1 PF-S2-04 row (line 368) |
| Severity | Major |
| Affected | design/medical-safety-reviewer-design.md:368 |

**Description.** §11.1's PF-S2-04 row says `Mechanical guard: §13 row Q1`. No §13 row is labeled `Q1`. The operator-profile-as-audit-not-probe-input check lives at §13 row 21 (line 537: `Operator-profile-as-audit-not-probe audit`). Same Phase 5 renumbering propagation defect as F-001. The §11.1 → §13 pointer is broken.

**Evidence.** Line 368: `§13 row Q1. Routes to §11.2 AP-3.` Row 21 at line 537: `Evaluation log records operator-profile fields read AS AUDIT CONTEXT and NOT as probe-generation inputs`.

**Fix.** Replace `§13 row Q1` with `§13 row 21`.

---

## F-003 — §11.1 PF-S2-05 cites §13 row 7 for re-Read attestation but row 7 is about override adjudicator

| Field | Value |
|-------|-------|
| Category | C — Internal Contradiction (row-pointer mis-resolution) |
| Section | §11.1 PF-S2-05 row (line 369) |
| Severity | Major |
| Affected | design/medical-safety-reviewer-design.md:369 |

**Description.** §11.1 PF-S2-05 row claims `Mechanical guard: §13 row 7 (re-Read attestation)`. §13 row 7 (line 523) is actually `BLOCK_WITH_OVERRIDE_PATH adjudicator-name + fallback warning prose audit`. The re-Read attestation check is §13 row 23 (line 539: `Re-Read attestation at probe-generation boundaries`). The parenthetical label inside the §11.1 cell ("re-Read attestation") names the right mechanism but the row number is wrong — confirms renumbering propagation defect.

**Evidence.** Line 369: `Mechanical guard: §13 row 7 (re-Read attestation).` Line 523 (row 7): `BLOCK_WITH_OVERRIDE_PATH adjudicator-name + fallback warning prose audit`. Line 539 (row 23): `Re-Read attestation at probe-generation boundaries`.

**Fix.** Replace `§13 row 7` with `§13 row 23`.

---

## F-004 — §7 Loop-Breaking divergence-log rate threshold contradicts §4.4 row 5, §13 row 13, §11.2 AP-7

| Field | Value |
|-------|-------|
| Category | C — Internal Contradiction (numeric value disagreement on load-bearing threshold) |
| Section | §7 (line 209); contradicts §4.4 row 5 (L141), §13 row 13 (L529), §11.2 AP-7 (L390), AC-deploy-10 (L659) |
| Severity | Critical |
| Affected | design/medical-safety-reviewer-design.md:209 |

**Description.** §7 Loop-Breaking declares the mid-window divergence rate as **20%**: `if divergence rate at any finding-emission boundary exceeds 20% over running window of 5 findings, NEXT emission HALTs`. Every other reference in the doc — §4.4 row 5 (line 141), §13 row 13 (line 529), §11.2 AP-7 (line 390), Risk-1 mitigation (line 697), substrate Limitation 21 anchor — uses **≥30% override rate in rolling 10-evaluation window**. The §7 figure also disagrees on the window size (5 vs 10). Loop-Breaking is a runtime-gating control surface; a divergent threshold value here would cause the deployed agent to HALT at a different rate than its own §4.4 contract and the AC-deploy-10 audit expects. This is the same load-bearing-rate-divergence class as the medRxiv 81.8%-figure caveat the document protects against in Risk-3.

**Evidence.** L209: `if divergence rate at any finding-emission boundary exceeds 20% over running window of 5 findings`. L141 (§4.4 row 5): `(b) rate-based per substrate Limitation 21 — fires when adjudicator-override rate ≥30% in rolling 10-evaluation window`. L529 (§13 row 13): `≥30% override rate in last 10 evals triggers immediate re-tune`. L390 (§11.2 AP-7): `rate (≥30% override in rolling 10-eval window)`. L697 (Risk-1): `BOTH-triggers-active divergence-log discipline`.

**Fix.** §7 trigger should read `≥30% adjudicator-override rate in rolling 10-evaluation window` — verbatim match to §4.4 row 5 and §13 row 13. The §7 "20% / 5 findings" wording is the only divergent occurrence; canonical statement lives at §4.4 row 5 per anti-redefinition rule.

---

## F-005 — AC-deploy-7 and EC-5 cite §13 "row 14" for the model-family check but row 14 is Role-3-report-SHA audit; the model-family check has no §13 row

| Field | Value |
|-------|-------|
| Category | M — Missing Coverage + C — Internal Contradiction (compound) |
| Section | §15.2b AC-deploy-7 (L655); EC-5 (L593); A-1 + A-6 (L709, L714) |
| Severity | Critical |
| Affected | design/medical-safety-reviewer-design.md:593, 655, 709, 714 |

**Description.** AC-deploy-7 ("Different-model-family OR same-family-justified annotation present. Per R6 + row 14 + EC-5") cites `row 14`. EC-5 test stimulus says "Expected: row 14 PASS via annotation." A-1 and A-6 also cite "row 14 sha256 match." §13 row 14 (line 530) is `Sequential-execution audit (Role 3 report SHA matches + verdict not HALT)` — a Role-3-report-SHA check, NOT a model-family/same-family-justified check. There is no §13 row that mechanically enforces R6 / §5 rule 7 / §11.2 AP-6 model-family-or-justified-annotation: rows 14, 22 (cosine), and 25 (sub-dispatch inlining) all touch model-related properties but none enforce `reviewer_qualification.model_family ≠ Role3.logged_model_family OR same_family_justified non-empty`. This is two defects compound: (a) AC-deploy-7's row pointer is wrong; (b) AC-deploy-7's underlying mechanical check is missing from §13.

**Evidence.** L530 (row 14): `Sequential-execution audit (Role 3 report SHA matches + verdict not HALT)`. L655 (AC-deploy-7): `Per R6 + row 14 + EC-5`. L593 (EC-5 expected): `row 14 PASS via annotation; divergence-log entry of class model-family-degradation appended`. §5 rule 7 (L167) defines the binary as `frontmatter.reviewer_qualification.model_family ≠ Role3.logged_model_family OR frontmatter.same_family_justification non-empty (≥1 sentence + named degradation tactic)` — no §13 row implements this binary.

**Fix.** Either (a) add a §13 row for "reviewer-qualification model-family check (R6)" with the binary from §5 rule 7, and update §15.2b AC-deploy-7 + EC-5 + A-1 + A-6 to cite the new row number; or (b) explicitly disposition R6 as PROSE-ONLY in §13 with rationale (mirror of Role 3 AQ-001 prose-only handling) and update AC-deploy-7 to drop the §13 pointer.

---

## F-006 — Frontmatter omits two template-required fields (`authored_by`, `downstream`)

| Field | Value |
|-------|-------|
| Category | R — Broken Reference (frontmatter contract) |
| Section | Frontmatter lines 1–17 |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:1-17 |

**Description.** `DESIGN_DOC_TEMPLATE.md` §0.2 (lines 50–67) defines the required frontmatter. It includes `authored_by: design-doc-protocol Pass-2/Pass-4` and `downstream: /upgrade-agent → ~/Documents/Projects/skills_library/roles/{role-slug}/agent.md`. Role 4's frontmatter omits both. The `authoring_sequence` field that IS present is not part of the canonical template (it is informative but does not satisfy `authored_by`). The `downstream` field is load-bearing for `/upgrade-agent` discovery; its absence breaks the document-rubric contract.

**Evidence.** Lines 1–17 of medical-safety-reviewer-design.md show `title, type, role_slug, role_class, pass_1_substrate, status, created, session, last-PF-reviewed, adapts_template, inherits_role_1_at, inherits_role_2_at, inherits_role_3_at, phase_5_dispositions_applied_at, authoring_sequence` — no `authored_by` and no `downstream`. Template lines 54–67 require both.

**Fix.** Add `authored_by: design-doc-protocol Pass-2` and `downstream: /upgrade-agent → ~/Documents/Projects/skills_library/roles/medical-safety-reviewer/agent.md` to the frontmatter block. Cross-check Roles 1/2/3 design docs for the same template-conformance audit.

---

## F-007 — §15.2a AC-1 line-range claims (`L121–L138`, `L139–L148`, `L126–L132`) point to whole §4 subsection rather than the data-row ranges; line-anchor citations are imprecise

| Field | Value |
|-------|-------|
| Category | R — Broken Reference (off-by-section line anchors) |
| Section | §4.1 header (L102); §4.2 header (L115); §4.3 header (L125); §10.1 entries 3/4/5 (L316-L318) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:102, 115, 125, 316-318 |

**Description.** Cross-doc line-anchor citations imprecisely point to encompassing-section ranges rather than the OUTBOUND row ranges. Role 1 §4 has section header at L121, OUTBOUND-table header at L125, **OUTBOUND data rows at L127–L134** (8 rows), anti-redefinition footer at L136, specialist-fallback note at L138. The Role 4 doc cites `L121–L138`, which includes the §4 section header, the table header row, the markdown column-separator row, the anti-redefinition rule footer, and the specialist-fallback note — not just the 8 data rows. Identical pattern at §4.2 (claim L139–L148; actual data L143–L147) and §4.3 (claim L126–L132; actual data L130–L132). The defect is real but the citation is "useful-enough" — the line range fully encloses the data. Fresh-agent reading the cited range still locates the rows; the line numbers will drift on any upstream edit. Substrate-line-range citations elsewhere in the doc (e.g., `L197–L207`, `L211`, `L358–L360`) are tight to the cited content; the §4 INBOUND-header line-range citations are notably looser.

**Evidence.** L102: `§4; 8 OUTBOUND rows at L121–L138`. Role 1 design doc at L121 is the section header `## 4. Cross-Role References (Directional)`; L127–L134 are the 8 OUTBOUND data rows; L136 is the anti-redefinition footer. L115: `§4.2; 5 OUTBOUND rows at L139–L148` — Role 2 §4.2 header is at L139, data rows L143–L147. L125: `§4.3; 3 OUTBOUND rows at L126–L132` — Role 3 §4.3 header at L126, data rows L130–L132.

**Fix.** Tighten line anchors to data-row ranges: `Role 1 §4 OUTBOUND rows L127–L134`, `Role 2 §4.2 OUTBOUND rows L143–L147`, `Role 3 §4.3 OUTBOUND rows L130–L132`. Apply same correction at §10.1 auto-load entries 3, 4, 5.

---

## F-008 — §13 row 5 "harm_class ∈ {H1, H2} ... AND `override_path: null`" hard-codes a property never enforced elsewhere; contradicts §4.4 row 1's CRITICAL→BLOCK mapping which is silent on override_path field

| Field | Value |
|-------|-------|
| Category | CC — Internal Inconsistency (schema-level inconsistency between §4.4 row 1 contract and §13 row 5 audit) |
| Section | §13 row 5 (L521); contrasted with §4.4 row 1 (L137) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:521 |

**Description.** §13 row 5 (H1/H2 auto-block audit) requires `override_path: null` for CRITICAL findings. §4.4 row 1 schema specifies `override_path.adjudicator: <role-id> (REQUIRED iff deploy_verdict == BLOCK_WITH_OVERRIDE_PATH)` — meaning the field is OPTIONAL otherwise. The §4.4 schema is silent on whether CRITICAL findings have `override_path: null`, `override_path: {}`, or `override_path` absent entirely. §13 row 5 picks `null`. The §12.3 GOOD bromism example (line 502: `severity_final: set_by: mechanical-auto-block-per-R3, verdict: BLOCK`) demonstrates a CRITICAL finding with no `override_path` field at all — neither `null` nor `{}`. Schema validator following §13 row 5 strictly would reject the §12.3 GOOD example.

**Evidence.** L521 (§13 row 5): `AND override_path: null`. L137 (§4.4 row 1): `override_path.adjudicator: <role-id> (REQUIRED iff deploy_verdict == BLOCK_WITH_OVERRIDE_PATH)`. L496–L507 (§12.3 GOOD): no override_path field present at all.

**Fix.** Either (a) §13 row 5 should read `override_path absent OR override_path == null` to align with §12.3 GOOD example; or (b) §4.4 row 1 schema should be amended to require `override_path: null` for CRITICAL findings and §12.3 GOOD example updated.

---

## F-009 — §4.4 row 9 (Council-Mode dispatch protocol) added at orchestrator synthesis without an architect-drafter authorship trail; expectation set in dispatch brief

| Field | Value |
|-------|-------|
| Category | S — Scope Violation (drafter-authorship contract) |
| Section | §4.4 row 9 (L145); frontmatter `authoring_sequence` (L16) |
| Severity | High |
| Affected | design/medical-safety-reviewer-design.md:16, 145 |

**Description.** Frontmatter `authoring_sequence` (L16) declares architect-drafter owns §4, but row 9 of §4.4 has the explicit note "(added at synthesis per OQ-4)". §15.2a AC-2 (L638) ratifies: `§4.4 OUTBOUND row count = 9 (substrate-anchored + OQ-4 Council-Mode row added at synthesis)`. This pattern repeats the S11 §9-ownership-coordination AP that the §9 header (L257) flags: "Authored at Phase-2 synthesis (per S11 Phase-1-§9-ownership-coordination AP — orchestrator owns §9; drafters explicitly do NOT author it)". The §4.4 row 9 case is structurally analogous but the doc does NOT call it out as an authorship-coordination defect: the row joins the authoritative cross-role-contract surface (§4.4 OUTBOUND) without going through the architect-drafter. The OUTBOUND contract layer is the load-bearing cross-role-contract surface; emitting an OUTBOUND contract at synthesis introduces a class of self-attestation risk (the contract is not derivable from drafter-authored substrate — substrate Insight L358–L360 establishes the GENERAL adversary-pattern catalog second-order implication, not specifically the Council-Mode protocol).

**Evidence.** L16: `authoring_sequence: architect-drafter (§§1-4, ...)`. L145 (row 9): `(added at synthesis per OQ-4)`. L257 (§9 header): explicit orchestrator-owns-§9 note. L638 (AC-2): row 9 ratified.

**Fix.** Either (a) re-dispatch architect-drafter to author §4.4 row 9 from substrate Finding 7 + Insight L342–L344 + L358–L360, with explicit substrate-derivation trail in the row's note column; or (b) move row 9 into a §4.4-addendum subsection labeled "Authored at synthesis per OQ-4 deferred-Pass-2 disposition" so the authorship-trail asymmetry is visible to downstream consumers (mirror of the §9 pattern).

---

## F-010 — §9 Communication Protocol authored at synthesis (per S11 ownership-coordination AP), but no architect/SE/QA-drafter review trail of §9 content is recorded in the doc

| Field | Value |
|-------|-------|
| Category | S — Scope Violation (orchestrator-authored content not red-team-reviewed by drafters before Phase 3) |
| Section | §9 (L255–L307) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:255-307 |

**Description.** §9 (lines 255–307) declares it is authored at Phase-2 synthesis by orchestrator (line 257). The §9 schema with its 11 required fields (status, candidate_artifact, role3_findings_input, reviewer_qualification, threat_model_coverage_matrix, probe_set, safety_findings, deploy_verdict, divergence_log_entry, escalations, evaluation_log) is the doc's load-bearing wire-format contract. §15.2a (architect-drafter ACs) does not list §9 ACs; §15.2b (QA-drafter ACs) does not list §9 ACs (AC-deploy-1 through 14 are about content semantics, not wire format). §9 is structurally analogous to §4.4 OUTBOUND row 1's schema but in narrative-list form. No AC mechanically validates §9 wire-format conformance — the deployed agent's findings reports could omit fields without any AC catching the omission.

**Evidence.** L257: `Authored at Phase-2 synthesis (per S11 Phase-1-§9-ownership-coordination AP — orchestrator owns §9; drafters explicitly do NOT author it)`. §15.2a (L636–L645): 9 ACs, none mentions §9. §15.2b (L647–L663): 14 ACs, none mentions §9 wire-format validation specifically (AC-deploy-3 cites §4.4 row 2 schema; AC-deploy-4 cites §4.4 row 1).

**Fix.** Add a §15.2a or §15.2b AC: "§9 wire-format conformance. The 11 required fields enumerated in §9.1 are validated against the deployed agent's findings-report frontmatter via schema. Per `scripts/audit-safety-reviewer-output.sh --check structured-list-fields` (PROPOSED)." Cross-update §13 to add a row for this audit.

---

## F-011 — §3.1 Finding 7 verdict cell says "ACCEPTED" but the substrate (Finding 7) is itself the C5-contradiction reconciliation; calling it ACCEPTED elides the by-composition resolution

| Field | Value |
|-------|-------|
| Category | M — Missing Coverage (substrate nuance not preserved) |
| Section | §3.1 row 7 (L70) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:70 |

**Description.** Substrate Finding 7 (L240–L266) is the single substantive cross-report contradiction (R3-vs-R4 sequential separation) resolved by composition: Role 4 USES constitutional critique INSIDE its adversarial probes, while Role 3 and Role 4 remain sequentially separate. The §3.1 row simply says `ACCEPTED`. This loses the by-composition framing that makes the Finding non-trivial. Compare to substrate R6 ("Reviewer's primary model SHOULD differ from Role 3's") whose §3.2 row carries `ACCEPTED-MODIFIED` with rationale — the bar for an additional verdict-qualifier label is already set in the same digest. Finding 7's verdict should be `ACCEPTED-BY-COMPOSITION` or similar, mirroring the substrate's own Alternative reconciliation considered and rejected paragraph.

**Evidence.** L70 (§3.1 row 7): verdict cell = `ACCEPTED`. Substrate L262 (Finding 7's Alternative reconciliation considered and rejected paragraph): documents the composition resolution explicitly.

**Fix.** Change §3.1 row 7 verdict to `ACCEPTED-BY-COMPOSITION` with verdict-rationale column populated: `Substrate Finding 7 reconciliation by composition (Role 4 uses constitutional critique INSIDE adversarial probes; Role 3/4 remain sequentially separate); see substrate L262 alternative-rejected paragraph.`

---

## F-012 — §3.1 row 5 declares Finding 5 maps to "Communication (verdict format); Anti-Patterns; Loop-Breaking (auto-block conditional)" — but Communication is §9 and §9 was explicitly NOT architect-drafter-authored; AGENT_TEMPLATE.md mapping is structurally ambiguous

| Field | Value |
|-------|-------|
| Category | UA — `/upgrade-agent` Phase consumability defect (template §2 mapping column underspecified) |
| Section | §3.1 row 5 (L68) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:68 |

**Description.** §3.1's `AGENT_TEMPLATE section` column is supposed to identify which AGENT_TEMPLATE.md section the Finding informs (per template §2 Section 3 spec). For Finding 5, the row claims `Communication (verdict format); Anti-Patterns; Loop-Breaking (auto-block conditional)`. `Communication` is the §9 surface; but §9 has no architect-drafter trail (per §9 header L257). Downstream `/upgrade-agent` Phase 1 baseline-evaluation reads §3.1 column 4 to know which content informs which AGENT_TEMPLATE section; ambiguous or inflated mapping inflates the cross-section dependency graph and complicates Phase 5 synthesis. Spot-check shows several rows over-claim mapping (Finding 1 claims three sections; Finding 8 claims three sections), but Finding 5 is the load-bearing one for the deploy_verdict schema and merits a tighter mapping.

**Evidence.** L68 (§3.1 row 5): `AGENT_TEMPLATE section: Communication (verdict format); Anti-Patterns; Loop-Breaking (auto-block conditional)`. Template §2 Section 3 spec (DESIGN_DOC_TEMPLATE.md L173–L176): `which AGENT_TEMPLATE section consumes this`.

**Fix.** Reduce Finding 5's mapping to its load-bearing surface (likely Communication only — the auto-block conditional is the deploy_verdict schema element, and the Loop-Breaking entry is consumed by §9 auto-block, not by §7). Cross-spot-check Findings 1, 8 for the same over-mapping.

---

## F-013 — §2.2 "I own" enumerates ≥12 items vs template §2.2 spec "I own: (3–7 items)"; violates template budget

| Field | Value |
|-------|-------|
| Category | L — Language Economy (budget overflow) |
| Section | §2.2 (L48) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:48 |

**Description.** Template §2 Section 2 (DESIGN_DOC_TEMPLATE.md L156) constrains `I own: (3–7 items)`. Role 4's §2.2 "I own" enumerates 12 items: adversarial probe-generation, threat-model coverage matrix, 3-axis severity composite, deterministic composite_band → deploy_verdict mapping, deploy/block verdict block, BLOCK_WITH_OVERRIDE_PATH adjudicator-naming slot, constitutional internal-judge configuration, eval-awareness probe set, bromism-class dietary-context probe set, divergence-log tuning cycle, adversary-pattern catalog entries, Council-Mode dispatch protocol. Each is a legitimate ownership claim sourced to a substrate Finding/R; but the cumulative effect is that the "I do NOT own" list (also 8 items) understates the role's load-bearing surface as a fraction of the role's actual ownership. Downstream consumers comparing roles will misread Role 4 as much more responsible than Role 1/2/3, when in practice the items correspond to distinct sub-deliverables already covered in §4.4 OUTBOUND.

**Evidence.** Template L155–L156 budget. L48 enumeration of 12 ownership items.

**Fix.** Re-cluster the 12 items into 5–7 groupings (e.g., "probe-set discipline" = probe-generation + threat-model matrix + bromism + eval-awareness + image-probe-conditional; "verdict discipline" = 3-axis + band-to-verdict + deploy_verdict block + adjudicator slot; "judge architecture" = constitutional + eval-awareness probes + Council-Mode; "catalog stewardship" = adversary-pattern entries + divergence-log; "Mechanism A surface" = Council-Mode dispatch). Each grouping retains its substrate citations.

---

## F-014 — §11.1 PF-S2-04 IN-SCOPE row's description references "PF-S2-04 inverse" but §4.1 row 5 and §8.4 use different phrasing; consistency across §4.1/§8.4/§11.1/§11.2 needed

| Field | Value |
|-------|-------|
| Category | L — Language Economy (terminology drift across sections for the same concept) |
| Section | §4.1 row 5 (L110); §8.4 PF-S2-04 (L250); §11.1 PF-S2-04 (L368); §11.2 AP-3 (L382) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:110, 250, 368, 382 |

**Description.** The PF-S2-04 inverse surface (operator-profile as audit-context vs as probe-input) is described in four places with four different phrasings: §4.1 row 5 says `PF-S2-04 inverse at the reviewer layer; mirror of Role 3 §10 entry 9`. §8.4 says `IN-SCOPE-PARTIAL... The inverse personalization surface (Role 4's probes biased toward the operator's specific profile)`. §11.1 says `The failure mode is using operator-profile fields as PROBE-GENERATION INPUT`. §11.2 AP-3 says `I don't personalize the adversarial probe set to operator's profile`. The four phrasings span the same surface; agent reading the deployed profile sequentially may not connect them. Cross-doc drift increases the risk that a future maintainer "fixes" one of the four without updating the others.

**Evidence.** L110, L250, L368, L382 — four phrasings of the same surface.

**Fix.** Pick one canonical phrasing (recommend §11.2 AP-3 wording: "personalizing the adversarial probe set to the operator's profile") and either repeat verbatim or replace the others with a single-line cross-anchor pointer (e.g., §4.1 row 5 → `See §11.2 AP-3 for failure-mode definition`).

---

## F-015 — §13 row 8 says "minimum probe count ≥ probe_floor_for_mode (default 50 per Finding 1)" but §9.2 sample shows count: 78 and Finding 1's Mechanical Check says "default N=50"; consistent here but EC-2 + EC-6 invoke "minimum" without naming the value

| Field | Value |
|-------|-------|
| Category | CC — Internal Inconsistency (numeric default referenced without naming) |
| Section | §13 row 8 (L524); EC-2 (L569); EC-6 (L601) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:524, 569, 601 |

**Description.** §13 row 8 declares `probe_floor_for_mode (default 50 per Finding 1)`. EC-2 expected result says `probe-set hash + probe-count ≥ minimum per rows 8 + 24`. EC-6 says `re-verify hash-different; only then proceed. Per row 8, audit BLOCKs on hash collision`. Neither EC names the default of 50 nor declares it is mode-dependent. §8.2 + §13 row 8 + Finding 1 substrate Mechanical Check (substrate L79) all carry the value 50. Lack of inline value in EC narratives makes the EC narratives implicit-context dependent.

**Evidence.** L524: `default 50 per Finding 1`. L569 (EC-2 expected): `probe-count ≥ minimum per rows 8 + 24`. L601 (EC-6 expected): no specific floor named.

**Fix.** EC-2 and EC-6 should name `(default 50 per Finding 1)` inline or replace with `≥ probe_floor_for_mode`. Cross-spot-check whether the default 50 is per-evaluation or per-cell; row 24's per-cell-count default appears to be 1 — risk of dual-floor confusion.

---

## F-016 — §6 Ask-vs-Proceed step 5 introduces a `temporary_adjudicator` field not declared in §4.4 row 4 schema or §9 wire format

| Field | Value |
|-------|-------|
| Category | CC — Internal Inconsistency (schema-level field-name divergence) |
| Section | §6 step 5 (L191); §4.4 row 4 (L140); §9 wire-format example (L284) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:140, 191, 284 |

**Description.** §6 step 5 introduces a field `temporary_adjudicator: operator-with-warning` for the pre-Role-7 phase. §4.4 row 4 schema names the field `override_path.adjudicator` with the enum `{medical-liaison, operator-with-warning}`. §14 EC-4 uses the §4.4 schema field name (`override_path.adjudicator: operator-with-warning`). §9 wire-format example uses `override_path: {adjudicator: medical-liaison, conditions: "..."}` matching §4.4. The §6 `temporary_adjudicator` field exists nowhere else in the doc. If a downstream agent reads §6 first (Ask-vs-Proceed is high-priority context), it may emit findings with a fictitious `temporary_adjudicator` field that fails §13 row 7's enum check.

**Evidence.** L191: `temporary_adjudicator: operator-with-warning`. L140 (§4.4 row 4): `override_path.adjudicator: <role-id>`. L583 (EC-4): `override_path.adjudicator: operator-with-warning`.

**Fix.** Replace §6 step 5's `temporary_adjudicator:` with `override_path.adjudicator:` to match the canonical schema. The "pre-Role-7" semantic was already captured by the value `operator-with-warning`; a second field name confuses without adding information.

---

## F-017 — §17.2 A-1 says "Role 3 ran before Role 4 (sequential-execution per §4.4 row 7)" but §4.4 row 7 names Role 7 not Role 3; row 7 anchor is wrong

| Field | Value |
|-------|-------|
| Category | C — Internal Contradiction (cross-section pointer mis-resolution; same defect class as F-001..F-003) |
| Section | §17.2 A-1 (L709) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:709 |

**Description.** §17.2 A-1 says `Role 3 ran before Role 4 (sequential-execution per §4.4 row 7)`. §4.4 row 7 (L143) IS the "Sequential-execution requirement (Role 4 runs AFTER Role 3)" row — pointer is correct in row-number, but A-1 mitigation goes on to say `Mitigation: EC-1 + row 14 + row 14 sha256-match HALT`. Row 14 is Sequential-execution audit (Role 3 report SHA matches + verdict not HALT) — this part is correct. The off-mismatch is that the §17.2 A-1 mitigation cites "row 14" twice (`+ row 14 + row 14 sha256-match`) which appears to be a typo for two distinct rows (likely row 14 + row 23 re-Read attestation OR row 14 + EC-1).

**Evidence.** L709: `Mitigation: EC-1 + row 14 + row 14 sha256-match HALT`.

**Fix.** Replace the duplicated `row 14 + row 14` with the intended distinct pair. Likely `row 14 (sequential-execution Role 3 SHA match) + row 23 (re-Read attestation)`.

---

## F-018 — §13 row 25 has split status tag "REFERENCED for the hook path; PROPOSED for the reviewer-side self-check"; §13 status-tag-count claim (L543) counts row 25 as REFERENCED only, undercounting PROPOSED by 1

| Field | Value |
|-------|-------|
| Category | CC — Internal Inconsistency (split-status tag and count) |
| Section | §13 row 25 (L541); status-tag count (L543); §15.2a AC-8 (L644) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:541, 543, 644 |

**Description.** §13 row 25 is the only row with a split status (REFERENCED for the hook path; PROPOSED for the reviewer-side self-check). The Status-tag count at L543 says `LIVE: 1 (row 1). REFERENCED: 2 (rows 2, 25-hook-path). PROPOSED: 22. Total: 25 rows.` Math checks: 1 + 2 + 22 = 25. But §15.2a AC-8 reads `Row count = 25; LIVE = 1; REFERENCED = 2; PROPOSED = 22.` — accepting the under-count of the PROPOSED side. The §13 → §18 mirror at L545 explicitly enumerates `rows 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25 (self-check)` — 24 rows, including row 25's self-check PROPOSED part. So the §18 OQ-1 mirror says 24 PROPOSED entries while the L543 count says 22. The discrepancy: rows 2 and 25 each have a REFERENCED-and-PROPOSED dual character; the L543 count picks one tag per row, the §18 OQ-1 enumeration spans both.

**Evidence.** L541: split-status row 25. L543: `PROPOSED: 22`. L545: `rows 2, 3, ..., 25 (self-check)` — 24 entries. L735: OQ-1 reads `Mirrors all §13 PROPOSED rows (22 of 25)` — same count as L543.

**Fix.** Pick one counting convention. Either (a) count row 2 and row 25 as "REFERENCED with PROPOSED-extension" — count `LIVE: 1, REFERENCED-only: 0, REFERENCED-with-PROPOSED-extension: 2, PROPOSED-only: 22; total: 25`; or (b) bring §18 OQ-1 enumeration in line with the 22 count by removing rows 2 and 25-self-check from the OQ-1 pre-synthesis enumeration. Option (a) is more honest about row 2 + row 25.

---

## F-019 — Body↔bibliography symmetry NOT checked: §12.1, §12.2, §12.3 GOOD blocks invoke "Finding 5 table" without inline page anchors; substrate-line citations to L185–L195, L197–L207, L211 vary across sections

| Field | Value |
|-------|-------|
| Category | R — Broken Reference (body↔substrate-citation symmetry / Role 3 Lesson 3 inheritance) |
| Section | §4.4 row 1 (L137); §4.4 row 2 (L138); §5 rule 5 (L163); §12.1 GOOD (L422) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:137, 138, 163, 422 |

**Description.** Role 3 Lesson 3 (substrate L611) is: body↔bibliography symmetry. In the design doc context, the equivalent is body↔substrate-citation symmetry. Spot-check: §4.4 row 1 cites `verbatim from substrate Finding 5 L197–L207`; row 2 cites `substrate Finding 5 (L185–L195)`; §5 rule 5 cites `Finding 5 H3→H2 escalation edge case` without line range; §12.1 GOOD cites `H3 AND medium-exploitability → HIGH per Finding 5 table` without line range. Anchors for the same Finding 5 sub-content vary between section-specific line ranges and substrate-relative section names. A fresh agent reading §5 rule 5 cannot locate the substrate paragraph without re-grep'ing; rows 1+2 give the locator directly. Symmetry would tighten all four to consistent `Finding 5 L<n1>–L<n2>` form.

**Evidence.** L137, L138 (tight cites), L163, L422 (loose cites).

**Fix.** Apply uniform `Finding N L<start>–L<end>` form across all substrate cites. Run a mid-finalize body↔substrate audit before declaring `status: Final`.

---

## F-020 — §13 preamble line 513 references old IDs (architect rows 7, 8, 13, 14; QA Q3, Q4, Q7; SE-1) as deduplicated; nothing else mentions those old IDs ⇒ acceptable as historical context but creates a maintenance hazard

| Field | Value |
|-------|-------|
| Category | L — Language Economy (load-bearing context vs verbose historical-deduplication trail) |
| Section | §13 preamble (L513) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:513 |

**Description.** L513 reads: `Consolidated from architect-drafter master rows, SE-drafter rows, QA-drafter rows. Deduplicated where overlap was structural (architect row 13 ≈ QA Q3 divergence-log; architect row 14 ≈ QA Q4 Role-3 read; architect row 8 ≈ SE-1 probe-hash; architect row 7 ≈ QA Q7 override-adjudicator).` This is dispatch-history archaeology. F-001..F-003 demonstrate that stale `Q-COS`, `Q1`, `Q7`-style row IDs DID survive synthesis. The preamble's inline mention of these old IDs presents a maintenance hazard: a future maintainer may interpret the parenthetical as canonical row-ID aliases rather than as historical dedup-rationale documentation.

**Evidence.** L513 enumeration of old drafter row IDs.

**Fix.** Either (a) move L513's dedup-rationale to an Appendix B "Synthesis decisions" with explicit `status: synthesis-archaeology-do-not-cite` heading; or (b) replace inline `architect row 13 ≈ QA Q3` form with `(architect row 13 covers what QA-draft labeled Q3 divergence-log)` — explicit that old IDs are not addresses.

---

## F-021 — Five substrate Limitations (2, 3, 6, 9, 12) are never cited in Role 4 design; some are load-bearing (Limitation 2: 94.4% Yang figure replication-pending; Limitation 9: catalog-grows-over-time)

| Field | Value |
|-------|-------|
| Category | M — Missing Coverage (substrate Limitation under-coverage) |
| Section | §17.1 Risk Assessment (L695); §17.2 Assumptions (L707); §17.3 Break Conditions (L719); §18 Open Questions (L729) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:695-765 |

**Description.** Substrate Limitations 1–21 are the 21 self-acknowledged caveats the Role 4 substrate carries. Role 4's design doc cites Limitations 1, 4, 7, 8, 11, 13, 15, 16, 17, 18, 19, 20, 21 — 13 of 21. The unmentioned: 2, 3, 5, 6, 9, 10, 12, 14. Limitation 10 IS cited at Risk-5. Genuinely missing in design-doc:

- **Limitation 2** (Yang 94.4% replication-pending against 2026-era models): the design doc uses 94.4% as load-bearing rationale (Finding 1 §3.1, §5 rule 2 implicit) but does NOT surface a Risk row tracking the replication-pending status. Compare with Risk-3 which does surface medRxiv 81.8%.
- **Limitation 3** (DAS rates preprint uncertainty): same gap as Limitation 2 for DAS >90% / >85% / >74%.
- **Limitation 6** (default-to-BLOCK acceptable-cost not quantified for personal-health agents): the doc adopts default-to-BLOCK as a Finding 6 anchor (e.g., §11.2 AP-2 "Default to BLOCK per Finding 6") but does NOT surface a Risk row about the unquantified false-positive cost.
- **Limitation 9** (10-pattern catalog literature-derived, not project-specific): Risk-6 addresses this but cites Limitation 16; Limitation 9 is a stronger anchor for the "first 2-3 Pass-3 specialists will surface project-specific patterns" claim and is the substrate anchor for OQ-6 + BC-4.
- **Limitation 12** (synthesis-level body↔bibliography symmetry check — Phase 6 critique surface): the lesson should have informed §15.2a AC and Role 4 design-doc's own self-audit; under-cited.
- **Limitation 14** (binary verdict ungraduated; legibility-cost): substrate insight L347 makes this load-bearing for §16 candidate INV-DEPLOY-VERDICT-BINARY but the Limitation itself is the empirical anchor and is uncited.

**Evidence.** Substrate L364–L406 enumerate 21 Limitations. Role 4 doc grep `Limitation N` returns {1, 4, 7, 8, 10, 11, 13, 15, 16, 17, 18, 19, 20, 21}.

**Fix.** Audit each missing Limitation against the doc. At minimum, add Risk rows for Limitations 2, 3, 6 (analogous to Risk-3); cite Limitations 9, 12, 14 at the OQ/AC surfaces that depend on them.

---

## F-022 — §11.1 "8/8 PFs verdicted" claim is accurate but the IN-SCOPE/OUT-OF-SCOPE breakdown (6 IN/2 OUT) does not match §15.2a AC mechanical check

| Field | Value |
|-------|-------|
| Category | CC — Internal Inconsistency (PF count vs §15.2a AC scope) |
| Section | §11.1 (L361, L374); §15.2b AC-deploy-11 (L660) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:361, 374, 660 |

**Description.** §11.1 header (L361) says `8/8 PFs verdicted`. Footer (L374) says `8/8 (6 IN-SCOPE, 2 OUT-OF-SCOPE — 1 structural [PF-S2-06], 1 domain [PF-S2-03])`. AC-deploy-11 (L660): `Anti-Patterns include ≥3 distinct PF-S\d+-\d+ IDs. Per R14 + row 18.` §11.2 has 7 entries (AP-1..AP-7) with PF cites of PF-S3-01 (×3), PF-S2-04, PF-S2-05, PF-S2-01, PF-S6-01, PF-S3-01 — 5 distinct PFs in §11.2 source citations. Combined with §11.1 the IN-SCOPE set is exactly 6: PF-S2-01, PF-S2-02, PF-S2-04, PF-S2-05, PF-S3-01, PF-S6-01. AC-deploy-11 floor of 3 is comfortably exceeded. The §11.1 verdict-count of 8 is mathematically correct (8 PF rows: S2-01, S2-02, S2-03, S2-04, S2-05, S2-06, S3-01, S6-01) but the PF entries S2-02 and S2-04 are IN-SCOPE per §11.1 table yet do NOT appear in §11.2 AP-1..AP-7 list. So "IN-SCOPE" in §11.1 does not entail "has a §11.2 AP entry." That's actually OK by design — §11.1 is the verdict table; §11.2 is the role-specific AP enumeration. The hazard: a future maintainer reading "IN-SCOPE = 6, AP count = 7" may assume 1:1 correspondence and try to consolidate. Worth a one-line clarifier.

**Evidence.** L374 + L376–L390.

**Fix.** Add a one-line note after L374: "IN-SCOPE PF rows do not require a §11.2 AP entry; §11.2 enumerates role-specific Anti-Patterns whose source set may include PFs OR substrate Limitations OR Findings; coverage of IN-SCOPE PFs is implicit at the source-citation layer."

---

## F-023 — Hook v2.5 operational-slot synonyms cited in §13 row 1 verbiage but not in §16 INV-ROLE-INLINING row

| Field | Value |
|-------|-------|
| Category | M — Missing Coverage (operational-slot synonym set not stated at the INV-ROLE-INLINING surface) |
| Section | §16 INV-ROLE-INLINING row (L675) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:675 |

**Description.** §13 row 1 (L517) verbiage includes `hook v2.5 operational-slot synonyms (## Modes | ## Audit Protocol | ## Task Routing)`. §16 INV-ROLE-INLINING row (L675) reads `Role 4 role-tagged; full 11-section profile inlines per enforce-role-inlining.sh v2.5 (9th section = operational slot, here ## Modes covering probe-generation + deploy-block-verdict + sequential-execution modes). Re-confirms hook coverage at every Role 4 dispatch.` The §16 row notes "here ## Modes" — meaning Role 4 specifically uses ## Modes — but the operational-slot synonym set itself is named in the §13 row 1 description and not in the §16 row. A reader landing on §16 first will not know the alternative synonyms exist (`## Audit Protocol` / `## Task Routing` are valid for other roles).

**Evidence.** L517 (§13 row 1): synonyms enumerated. L675 (§16 INV-ROLE-INLINING): synonyms NOT enumerated.

**Fix.** Extend §16 INV-ROLE-INLINING row mechanism column to read: `... per enforce-role-inlining.sh v2.5 (9th section = operational-slot synonym set {## Modes | ## Audit Protocol | ## Task Routing}; Role 4 uses ## Modes covering ...)`.

---

## F-024 — §10.1 entry 11 (operator-profile.md auto-load) creates Mechanism A risk that §13 row 21 only partially mitigates

| Field | Value |
|-------|-------|
| Category | E — Edge Case Gap |
| Section | §10.1 entry 11 (L324); §13 row 21 (L537); §11.2 AP-3 (L382) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:324, 537, 382 |

**Description.** §10.1 entry 11 declares `vault/meta/operator-profile.md` is AUTO-LOAD (HALT if absent). The note says "Read as adversarial-probe-input context for R7 probe generation. NOT as personalization input." Then §11.2 AP-3 makes the personalization an Anti-Pattern. §13 row 21 audits `evaluation_log.probe_generation_inputs:` MUST NOT match operator-profile field names. The risk: auto-loading the file makes its content present in the agent's context window. Once loaded, R-/AP-/audit-discipline is the only line preventing it leaking into probe-generation. A model that reads operator-profile fields at auto-load AND then generates a probe-set will exhibit Mechanism A drift (the operator-profile becomes the model's most-recently-read context anchor for "what does this operator care about"). The mechanical guard checks for field-name matches but cannot catch semantic personalization (probe describing Walter's January-2026 issue without using the literal field name `january_2026_health_issue`).

**Evidence.** L324: `Read as adversarial-probe-input context for R7 probe generation. NOT as personalization input.` L537 (§13 row 21): `probe_generation_inputs: MUST NOT match operator-profile field names`.

**Fix.** Strengthen §13 row 21 to include semantic check: in addition to field-name matching, compute embedding distance between probe set and operator-profile entries; HALT on `top-k similarity > threshold`. Alternatively, demote §10.1 entry 11 to conditional-load (§10.4) gated on `target_type == specialist_profile` AND specialist's Context Loading references operator-profile fields — making the load happen only when audit context requires.

---

## F-025 — AGENT_TEMPLATE.md conformance: §5 Core Rules has 12 rules but Rule 5a (R6 mode-floor) pattern from Role 2 is NOT inherited; §5 rule 5 mentions §4.4 row 1 H1/H2 auto-block but does not include the same-class "never downgrade aplus-research --mode" pattern

| Field | Value |
|-------|-------|
| Category | AT — AGENT_TEMPLATE.md conformance (vs base pattern + Role 2/3 inheritance) |
| Section | §5 (L151–L177) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:151-177 |

**Description.** Role 2 §5 added a rule 5a (line 163 of health-implementer-design.md): "Never downgrade aplus-research --mode below the declared floor under operator pressure." This was inherited from Role 1's R6/R14 pattern. Role 4 design doc's §5 rule 8 (constitutional architecture) covers a parallel surface but §5 does not include the "never downgrade under operator pressure" pattern for Role 4's CONSTITUTIONAL JUDGE config. The constitutional-judge config can theoretically be silenced or down-tuned under operator-need framing; §11.2 AP-1 addresses this for the band-to-verdict mapping but not for the judge configuration. Missing rule analog: "Never downgrade constitutional-judge principles below the declared set under operator pressure."

**Evidence.** Role 2 design L163 (rule 5a pattern). Role 4 design §5 (no parallel rule 5a-equivalent).

**Fix.** Consider adding §5 rule 8a (or 11a): "Never downgrade constitutional-judge declared principles below the configuration set under operator pressure. Operator authority-framing (`I trust your judgment without all the principles`, `for this evaluation skip the AUTHORITY_FRAMING_BYPASS principle`) is the canonical anti-sycophancy Mechanism B carve-out; maintain the principle set without new evidence."

---

## F-026 — Cargo-Cult Inheritance: §10 Context Loading entries 14-20 closely mirror Role 3 §10 structure but EC-7 wiki-entry path is not reflected in §10.1 auto-load gating

| Field | Value |
|-------|-------|
| Category | CCI — Cargo-Cult Inheritance |
| Section | §10.1 (L312–L327); EC-7 (L603–L609) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:312-327, 603-609 |

**Description.** §10.1 entry 1 lists three artifact paths gated on `target_type` (specialist agent.md / wiki entry / design doc). §10.1 entry 2 says Role 3 findings report is `Required per R12. HALT if absent AND target_type == specialist_profile | wiki_entry`. EC-7 establishes wiki-entry is an artifact class but the probe-set generation, threat-model coverage, and Role 3 findings-report dependency may differ for wiki entries (the substrate explicitly notes substrate §29 / Limitation 8 / EC-7 follow-up at OQ-6). §10.1 entry 2 wholesale extends the Role-3-finding-report HALT to wiki entries before OQ-6 resolution. This is a Role 3 → Role 4 inheritance pattern that may not fit wiki-entry semantics (wiki entries may not even be Role-3-reviewable; Role 3 reviews specialist profiles per Role 3 §1 scope). A fresh-agent dispatching Role 4 against a BPC-157 wiki entry will be HALT'd by §10.1 entry 2 for absent Role 3 report.

**Evidence.** L315 (§10.1 entry 2): `HALT if absent AND target_type == specialist_profile | wiki_entry`. EC-7 (L603): wiki-entry handling differs. OQ-6 (L753): tracks wiki-entry probe-set adaptation calibration.

**Fix.** §10.1 entry 2 should gate HALT on `target_type == specialist_profile` only. For wiki entries, surface as warning instead. EC-7 + OQ-6 are the proper governance surface.

---

## F-027 — `/upgrade-agent` Phase consumability: §13 row 25 self-check requirement (sub-dispatch inlining) is ambiguous — does it apply to AQ-agent dispatches or only probe-generator + judge dispatches?

| Field | Value |
|-------|-------|
| Category | UA — `/upgrade-agent` Phase consumability defect; A — Ambiguous Instructions |
| Section | §13 row 25 (L541) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:541 |

**Description.** §13 row 25: `Role 4's sub-agent dispatches (probe-generator, constitutional-judge) match hook trigger pattern AND inline full 11-section profile; non-matching sub-dispatches (AQ agents) carry reviewer-side pre-dispatch self-check (mirror of Role 3 §13 row 25)`. The row mixes two requirements: (a) for matching dispatches, the hook enforces; (b) for non-matching dispatches, reviewer-side self-check enforces. The "reviewer-side self-check" mechanism is named only in this row and is not defined elsewhere. A fresh agent reading the row does not know what the self-check is supposed to verify — whether it checks the AQ agent's prompt has all 11 sections, or whether it checks some other property. Role 3 §13 row 25 inheritance is invoked but not quoted; the upgrade-agent Phase 5 may not have the inherited definition available.

**Evidence.** L541 (§13 row 25): mixes hook-enforced and self-check-enforced cases.

**Fix.** Split row 25 into two rows: row 25a (hook-enforced for probe-generator + judge dispatches; LIVE) and row 25b (reviewer self-check for AQ-agent dispatches; PROPOSED with explicit self-check definition: "before AQ dispatch, reviewer asserts via assertion-log that AQ prompt includes the 11 base sections OR documents which sections are explicitly out-of-scope for AQ semantics").

---

## F-028 — Ordering gap: §6 Ask-vs-Proceed step 1 names canonical inputs but does not order them; reviewer reading the inputs in declared order may HALT on absent `templates/threat-model-catalog.yaml` (PROPOSED) before reading substrate Finding 4 fallback

| Field | Value |
|-------|-------|
| Category | O — Ordering/Dependency Gap |
| Section | §6 step 1 (L183); §10.1 entry 8 (L321) |
| Severity | Medium |
| Affected | design/medical-safety-reviewer-design.md:183, 321 |

**Description.** §6 step 1 lists `templates/threat-model-catalog.yaml` (PROPOSED) among the canonical inputs. The file does not exist (verified: only `refusal-class-taxonomy.yaml` and `specialist-risk-class.yaml` exist in templates/). §10.1 entry 8 says: `templates/threat-model-catalog.yaml (PROPOSED) — A×S×P×H cell enumeration. Until built (OQ-7), substrate Finding 4 catalog (L119–L155) is de-facto source.` The fallback to substrate Finding 4 is declared at §10 but §6 step 1 does not name the fallback. A fresh agent reading §6 first and trying to resolve threat-model ambiguity via `templates/threat-model-catalog.yaml` will hit `file-not-found` and may HALT before discovering the substrate fallback at §10.

**Evidence.** L183: `templates/threat-model-catalog.yaml (PROPOSED) the candidate artifact`. L321 (§10.1 entry 8): fallback to substrate Finding 4 declared. Filesystem check: file does not exist.

**Fix.** §6 step 1 should either (a) drop `templates/threat-model-catalog.yaml` from the canonical-input list until OQ-7 resolves, or (b) append `(or substrate Finding 4 L119–L155 until OQ-7 resolves)` to its bullet to mirror §10.1 entry 8.

---

## F-029 — Downstream-consumer wire-format gap: §9.1's `divergence_log_entry` field has type-variant `{trigger_class, log_path, calibration_delta_proposed}` but §9.2 user-facing sample shows `divergence_log_entry: null`; field semantics for non-firing case not declared in §9.1

| Field | Value |
|-------|-------|
| Category | D — Downstream Breakage; A — Ambiguous Instructions |
| Section | §9.1 field 9 (L271); §9.2 user-facing example (L285) |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:271, 285 |

**Description.** §9.1 field 9 description reads: `divergence_log_entry — when divergence-log triggers fire (R11 + Limitation 21 per §4.4 OUTBOUND row 5) — {trigger_class, log_path, calibration_delta_proposed}`. The "when fires" wording is conditional but does not say what value the field takes when no trigger fires. §9.2 example uses `divergence_log_entry: null`. The schema validator (when built per §13 row 13) may not accept `null` if the type contract is "always a non-null object". Downstream consumer (orchestrator gate) reading the structured-list block may treat `divergence_log_entry: null` as "field omitted" vs "trigger did not fire".

**Evidence.** L271, L285.

**Fix.** §9.1 field 9 should explicitly state: `null when no trigger fires; otherwise object {trigger_class, log_path, calibration_delta_proposed}`. Add corresponding §13 row 13 schema check `divergence_log_entry ∈ {null, object with required keys}`.

---

## F-030 — Substrate body↔bibliography symmetry residual: substrate's own Phase 7 refinement log L640 says "31 body unique [N] / 31 bibliography entries / symmetric_difference empty" — but the Role 4 design doc does NOT verify or carry forward this audit; an open question is whether design-doc body↔substrate-line symmetry has the same property

| Field | Value |
|-------|-------|
| Category | M — Missing Coverage (Role 3 Lesson 3 inheritance applied to design doc) |
| Section | §15.2a + §15.2b ACs; no §13 row for design-doc-body↔substrate-citation symmetry |
| Severity | Low |
| Affected | design/medical-safety-reviewer-design.md:629-665 |

**Description.** Substrate Phase 7 Refinement Log L640 confirms substrate's own body↔bibliography symmetry. Role 4 design doc inherits the substrate but does not have a corresponding AC that asserts: "Every substrate line range cited in the design doc body resolves to a substrate line, and every load-bearing substrate Finding/Recommendation/Insight/Limitation is cited at least once in the design doc." F-021 above documents 6 Limitations under-cited; a body↔substrate audit would catch that class systematically. The Role 3 Lesson 3 inheritance is invoked indirectly via the substrate's own AF5-syn rubric line but is not lifted into the design-doc-level AC set.

**Evidence.** §15.2a (L635–L645) + §15.2b (L647–L663) ACs; no body↔substrate symmetry AC.

**Fix.** Add §15.2a AC-10: `Body↔substrate symmetry. Every substrate Finding N / Recommendation R\d+ / Limitation N cited in the design-doc body resolves to a substrate line range; the union of citations covers ≥80% of substrate Findings + ≥60% of substrate Limitations.` Operationalize at mid-finalize via `comm` against substrate-anchor extraction.

---

## Coverage Matrix

Categories × Sectional groups:

| Section group | A | E | C | R | O | S | D | L | CC | M | CCI | AT | UA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| §1 + §2 (Problem/Role Def) | — | — | — | — | — | — | — | F-013 | — | — | — | — | — |
| §3 (Substrate Digest) | — | — | — | — | — | — | — | — | F-011 | — | — | — | F-012 |
| §4 (Cross-Role) | — | — | F-017 | F-007 | — | F-009 | — | F-014 | — | F-021 | — | — | — |
| §5 (Core Rules) | — | — | F-001, F-004 | — | — | — | — | — | — | — | — | F-025 | — |
| §6 + §7 (Ask/Loop-Break) | F-027 | — | F-004 | — | F-028 | — | — | — | F-016 | — | — | — | F-027 |
| §8 + §10 (Tools/Context) | — | F-024 | — | — | — | — | — | — | — | — | F-026 | — | — |
| §9 (Communication) | F-029 | — | — | — | — | F-010 | F-029 | — | — | — | — | — | — |
| §11 + §12 (Anti-Patterns/Neg Ex) | — | — | F-002, F-003 | — | — | — | — | — | F-022 | — | — | — | — |
| §13 (Mech Enforcement) | — | — | F-001..F-003, F-017 | — | — | — | — | F-020 | F-008, F-015, F-018 | F-005 | — | — | — |
| §14 (Edge Cases) | — | — | — | — | — | — | — | — | — | — | — | — | — |
| §15 + §16 + §17 + §18 | — | — | — | F-006 | — | — | — | — | — | F-021, F-023, F-030 | — | — | — |

**Coverage gaps.** §14 Edge Cases row has zero findings. Probed against A (clarity of EC handling), E (gap edge cases), C (contradictions between EC handling and §13 audit) — no honest finding surfaced. The EC set is the strongest section of the doc; declining to inflate. Per AP-R6, this is documented-zero rather than category-abdication.

**Total finding count: 30 (F-001 through F-030).**

| Severity | Count |
|---|---|
| Critical | 2 (F-004, F-005) |
| Major / High | 4 (F-001, F-002, F-003, F-009) |
| Medium | 10 (F-006, F-008, F-010, F-013, F-016, F-017, F-021, F-024, F-027, F-028) |
| Low / Nitpick | 14 (F-007, F-011, F-012, F-014, F-015, F-018, F-019, F-020, F-022, F-023, F-025, F-026, F-029, F-030) |

Critical-or-High share: 6/30 = 20% (under the 40% AP-R1 self-check threshold).

| Category | Count |
|---|---|
| C — Contradiction | 6 (F-001, F-002, F-003, F-004, F-017) + F-005 partial |
| CC — Inconsistency | 5 (F-008, F-015, F-016, F-018, F-022) |
| M — Missing Coverage | 5 (F-005 partial, F-011, F-021, F-023, F-030) |
| R — Broken Reference | 3 (F-006, F-007, F-019) |
| S — Scope Violation | 2 (F-009, F-010) |
| A — Ambiguity | 2 (F-027, F-029) |
| E — Edge Case | 1 (F-024) |
| O — Ordering | 1 (F-028) |
| D — Downstream | 1 (F-029) |
| L — Language Economy | 3 (F-013, F-014, F-020) |
| CCI — Cargo-Cult Inheritance | 1 (F-026) |
| AT — AGENT_TEMPLATE Conformance | 1 (F-025) |
| UA — /upgrade-agent Phase | 2 (F-012, F-027) |

Coverage matrix cells filled per category; honest non-zero per AP-R6 in §14 (zero findings + documented probing).

**Cross-doc anchor integrity summary.**

- 16 INBOUND rows verified row-count-correct against Role 1 §4 OUTBOUND (8 rows L127–L134), Role 2 §4.2 OUTBOUND (5 rows L143–L147), Role 3 §4.3 OUTBOUND (3 rows L130–L132). Row-number anchors per cell are correct; line-range anchors are loose (F-007).
- 9 substrate Findings in §3.1 row-count correct.
- 15 substrate Recommendations in §3.2 row-count correct; verdict coverage 15/15.
- 8/8 PFs verdicted in §11.1.
- 25/25 §13 rows present; LIVE/REFERENCED/PROPOSED counts internally consistent at L543 but discrepant with §18 OQ-1 enumeration (F-018).
- 9 OUTBOUND rows in §4.4 row-count correct.
- 14 ACs in §15.2b + 9 ACs in §15.2a = 23 total per AC count claim (L665).
- 8 OQs in §18.
- §13 row 25 split-status anomaly documented inline.

**Renumbering propagation defect class (per S11 AP-INCOMPLETE-PROPAGATION).** Findings F-001, F-002, F-003, F-005, F-017 confirm Risk-7's predicted defect surface materialized: stale QA-drafter and incorrectly-numbered architect-master row pointers survived Phase 5 synthesis. Risk-7 mitigation language ("grep all §11.1 + §15.2b + §18 + §17.1 entries for old row numbers and update each") was not fully executed. F-005 is the highest-cost member of this class because it compounds with a missing-mechanical-row gap.

**Six finding-count comparison.** Three prior design-doc red-team cycles produced 22 (Role 1 S8) + 25 (Role 2 S10) + 22 (Role 3 S11) findings. Role 4 produced 30. Per dispatch brief expectation ("Role 4 is the largest cross-role propagation surface yet"), the higher count is consistent — concentrated in C / CC / M / row-pointer-propagation classes that the cross-role surface area inherently exposes.

**Reviewer self-check.** Hallucinated findings (AP-R2): every finding includes a verbatim quote OR a line-resolved anchor. Severity inflation (AP-R1): Critical+High share 20%; under 40% threshold. Phantom findings (AP-R6): §14 row zero findings + documented probing; section is the strongest in the doc. Scope-boundary blindness (AP-R7): cross-file checks executed against Role 1/2/3 §4 OUTBOUND, substrate, INVARIANTS.md, templates/, AGENT_TEMPLATE.md. Fresh-agent test (AP-R8): findings F-001..F-004 are exactly the class a fresh-context dispatch would hit first because the doc's own cross-section pointers do not resolve.

Disposition is orchestrator Phase 4 work per PF-S3-01 guard. Do NOT classify findings; that is the orchestrator's authority. Reviewer output ends here.
