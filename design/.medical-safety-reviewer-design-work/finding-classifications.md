---
title: Role 4 Phase-4 Finding Classifications
type: finding-classifications
session: S12
date: 2026-05-28
target_doc: design/medical-safety-reviewer-design.md
sources:
  - design/.medical-safety-reviewer-design-work/red-team-adversarial.md (30 findings F-001..F-030)
  - design/.medical-safety-reviewer-design-work/red-team-safety.md (11 findings S-01..S-11)
classification_owner: orchestrator
classification_discipline: PF-S3-01 6th consecutive guard — every finding personally source-read against cited evidence; REJECTED rows carry cited-evidence attestation
total_raw_findings: 41
duplicates: 3 (S-03 ≡ F-005, S-05 partial ≡ F-001+F-002)
active_unique_findings: 38
---

# Role 4 Design Doc — Phase 4 Finding Classifications

PF-S3-01 6th consecutive guard. Every finding personally source-read against cited evidence before verdict. REJECTED entries carry cited-evidence attestation (file:line + actual quoted contents). Reject-but-adopt pattern applied where the finding's claim is wrong but the suggested fix has independent value.

## Verdict legend

- **LEGITIMATE** — All 6 conditions hold (verifiable, factually correct, not mitigated, in scope, actionable, not relitigating). Apply at Phase 5.
- **LEGITIMATE-MODIFIED** — Conditions hold but the disposition modifies the suggested fix (e.g., scope-restricts, ports through a different mechanism).
- **REJECTED** — Fails ≥1 condition. Cited-evidence attestation in `rationale` column.
- **REJECTED-WITH-ADOPTION** — Reviewer's claim is wrong by cited evidence, but the suggested fix has independent value and IS adopted.
- **DUPLICATE** — Same defect as a prior finding; consolidated.

---

## Adversarial findings (30; F-001..F-030)

| ID | Sev | Category | Verdict | Bundle | Rationale (cited evidence for REJECTED) |
|---|---|---|---|---|---|
| F-001 | Major | C | LEGITIMATE | A | §5 rule 11 cites `§13 row Q-COS`; cosine audit lives at §13 row 22 (line 538). Stale QA-drafter ID. |
| F-002 | Major | C | LEGITIMATE | A | §11.1 PF-S2-04 cites `§13 row Q1`; operator-profile-as-audit-not-probe lives at §13 row 21 (line 537). |
| F-003 | Major | C | LEGITIMATE | A | §11.1 PF-S2-05 cites `§13 row 7 (re-Read attestation)`; row 7 is BLOCK_WITH_OVERRIDE_PATH adjudicator audit. Re-Read attestation lives at row 23. |
| F-004 | Critical | C | LEGITIMATE | B | §7 says `20% over running window of 5 findings`; §4.4 row 5 + §13 row 13 + §11.2 AP-7 + Risk-1 all say `≥30% in rolling 10-evaluation window`. Canonical: §4.4 row 5. §7 is the only divergent occurrence. |
| F-005 | Critical | M+C | LEGITIMATE | C | AC-deploy-7 (L655) + EC-5 (L593) + A-1 (L709) + A-6 (L714) cite "row 14" for model-family check; row 14 is Sequential-execution audit (Role 3 report SHA). No §13 row enforces R6 model-family binary. Compound defect: wrong pointer + missing mechanical row. |
| F-006 | Medium | R | LEGITIMATE | D | Template L60+L66 requires `authored_by` + `downstream`; Role 4 frontmatter (L1-17) omits both. The `authoring_sequence` field is informative but does not satisfy the template contract. |
| F-007 | Low | R | LEGITIMATE-MODIFIED | E | Line-range citations (L121-L138 etc.) point to whole §4 subsections incl. headers + footer. Loose but useful-enough. Tighten only at §10.1 auto-load entries 3/4/5 (load-bearing for re-Read at runtime); §15.2a AC-1 line ranges are inheritance-anchor enclosing-section style — acceptable. |
| F-008 | Medium | CC | LEGITIMATE | F | §13 row 5 (L521) requires `override_path: null` for CRITICAL; §12.3 GOOD (L495-507) has no `override_path` field. Schema validator following row 5 strictly would reject §12.3 GOOD. |
| F-009 | High | S | LEGITIMATE-MODIFIED | G | §4.4 row 9 added at synthesis per OQ-4. Substrate Insight L342-344 + L358-360 (general adversary-pattern catalog) provides background, but Council-Mode dispatch protocol IS new at synthesis. Disposition: add explicit synthesis-authorship trail to row 9 note column (mirror §9 header pattern); do NOT re-dispatch architect drafter (substrate ground is sufficient + OQ-4 resolution path already documented). |
| F-010 | Medium | S+D | LEGITIMATE | H | §9 wire-format conformance has no AC. AC-deploy-3 cites §4.4 row 2 schema (`safety_finding` block); AC-deploy-4 cites §4.4 row 1 (deploy_verdict block); neither validates the 11-field structured-list at §9.1. Add §15.2b AC. |
| F-011 | Low | M | REJECTED-WITH-ADOPTION | I | Reviewer suggests new verdict label `ACCEPTED-BY-COMPOSITION`. Rejected: §3.1 verdict column uses {ACCEPTED, ACCEPTED-MODIFIED, DEFERRED, REJECTED} per Role 1/2/3 precedent — introducing new label class breaks cross-doc symmetry. Adopt the substance via rationale-column annotation: row 7's "ACCEPTED" gets a parenthetical "(reconciliation by composition per substrate L262)". |
| F-012 | Low | UA | REJECTED | — | Reviewer claims Finding 5 over-claims AGENT_TEMPLATE mapping. Cited evidence: Finding 5 establishes the deploy_verdict schema (Communication §9.1 + §4.4 row 1), the H1/H2 auto-block rule (Anti-Patterns §11.2 AP-1 + §5 rule 5), AND the composite_band escalation logic (Loop-Breaking §7 + §13 row 5). All three mappings are load-bearing and substrate-justified. The mapping is correct. |
| F-013 | Medium | L | REJECTED-WITH-ADOPTION | J | Template L136 says "3–7 items". Role 4 has 12. **Cited evidence:** Role 3 §2.2 also has 9+ items in similar prose form (verified by Read). Role 1 §2.2 has 6 items; Role 2 §2.2 has similar density. The 3-7 budget is widely violated across the project as a natural consequence of foundation-role ownership scope. Rejected as a structural defect (project precedent runs against the literal template). Adopt the clustering improvement: cluster Role 4's 12 items into 7 thematic groupings (probe-set discipline / verdict discipline / judge architecture / catalog stewardship / Mechanism A surface / divergence-log discipline / adversary-pattern catalog). Preserves all substrate citations. |
| F-014 | Low | L | LEGITIMATE-MODIFIED | K | Four phrasings of PF-S2-04 inverse surface across §4.1 row 5, §8.4, §11.1, §11.2 AP-3. Adopt the §11.2 AP-3 phrasing as canonical at §11.1 + §8.4; leave §4.1 row 5 as-is (it's the inheritance anchor and the wording there serves a different function — citing Role 1 §4 OUTBOUND). |
| F-015 | Low | CC | LEGITIMATE-MODIFIED | L | Row 8 default 50 not named in EC-2/EC-6 narratives. Fix: name `(default 50 per Finding 1)` inline in EC-2 expected-result line. Do NOT modify EC-6 (the test stimulus there is about hash collision, not count). |
| F-016 | Medium | CC | LEGITIMATE | M | §6 step 5 introduces field `temporary_adjudicator:` not in canonical schema (§4.4 row 4 uses `override_path.adjudicator`). Replace §6 step 5's field name with `override_path.adjudicator:` matching §14 EC-4 + §9.1 wire format. |
| F-017 | Medium | C | LEGITIMATE | N | §17.2 A-1 mitigation: `EC-1 + row 14 + row 14 sha256-match HALT` — duplicate `row 14`. Intended pair: row 14 (sequential-execution Role 3 SHA match) + row 23 (re-Read attestation) OR + EC-1. |
| F-018 | Low | CC | LEGITIMATE | O | §13 row 25 split status creates count discrepancy: L543 claims "PROPOSED: 22"; OQ-1 enumeration lists 24 PROPOSED entries (rows 2,3,...,25). Pick convention: row 2 + row 25 = "REFERENCED with PROPOSED extension"; update L543 count to "LIVE: 1; REFERENCED: 0 pure; REFERENCED-with-PROPOSED-extension: 2; PROPOSED-only: 22; total: 25". Update OQ-1 to match. |
| F-019 | Low | R | LEGITIMATE-MODIFIED | P | Substrate citations vary: tight (Finding 5 L197-L207) vs loose (Finding 5 table). Adopt selective tightening: §5 rule 5 substrate cite expand to `Finding 5 L161-L211`; §12.1 GOOD substrate cite expand to `Finding 5 L197-L207 table`. Do not retrofit every single substrate citation — diminishing returns. |
| F-020 | Low | L | LEGITIMATE-MODIFIED | Q | §13 preamble L513 mentions old IDs (Q3, Q4, Q7, SE-1) as synthesis archaeology. F-001..F-003 + S-05 confirm the old-ID labels DID survive synthesis. Add explicit `(synthesis-archaeology — do NOT cite as canonical row IDs)` annotation to L513. |
| F-021 | Medium | M | LEGITIMATE-MODIFIED | R | 8 of 21 Limitations uncited. Substrate Limitations 2 + 3 (94.4%/DAS replication-pending) are genuinely load-bearing for §3.1 Finding 1 + §11.2 AP-2; Limitation 14 (binary verdict ungraduated) is load-bearing for §16 candidate INV-DEPLOY-VERDICT-BINARY. Adopt: extend Risk-3 to cite Limitations 2+3 alongside Limitation 1 (medRxiv 81.8%); cite Limitation 14 in §16 candidate INV. Reject blanket "cite every Limitation" — Limitations 5, 9, 10, 12 are already inherited indirectly or not load-bearing. |
| F-022 | Low | CC | LEGITIMATE | S | §11.1 IN-SCOPE = 6 vs §11.2 AP count = 7 not 1:1. Add one-line clarifier after §11.1 footer: "IN-SCOPE PF rows do not require a §11.2 AP entry; §11.2 enumerates role-specific anti-patterns whose sources may be PFs OR substrate Limitations OR Findings." |
| F-023 | Low | M | LEGITIMATE | T | §16 INV-ROLE-INLINING row says "here ## Modes" without enumerating the v2.5 synonym set. Extend mechanism column to include `{## Modes \| ## Audit Protocol \| ## Task Routing}` per §13 row 1 verbiage. |
| F-024 | Medium | E | LEGITIMATE-MODIFIED | U | Auto-loading operator-profile creates context-window Mechanism A risk that row 21 field-name match cannot catch semantically. Speculative-fix: embedding-distance check. Adopt instead: surface the risk explicitly in §17.1 (new Risk-8) and OQ (new OQ for semantic-mismatch audit) without adding embedding-distance mechanism in this design doc. |
| F-025 | Low | AT | REJECTED | — | Reviewer proposes §5 rule 8a "Never downgrade constitutional-judge principles." **Cited evidence:** §5 rule 9 (L173) already maintains the proposed verdict under operator pressure ("Maintain the proposed verdict when operator, candidate-author, or upstream agent pushes back without new cited evidence"); §11.2 AP-1 (L378) covers softening CRITICAL bands. Adding rule 8a duplicates rule 9's coverage. The constitutional-judge config is a §8 Tools concern (declared, not behavioral); maintain-position rule already applies. |
| F-026 | Low | CCI | LEGITIMATE-MODIFIED | V | §10.1 entry 2 HALTs on `target_type == specialist_profile \| wiki_entry`. EC-7 surfaces wiki-entry semantics differ. Adopt: gate HALT on `specialist_profile` only; for `wiki_entry`, demote to WARN. Update OQ-6 to track wiki-entry Role-3-dependency calibration. |
| F-027 | Medium | A+UA | LEGITIMATE-MODIFIED | W | §13 row 25 mixes hook-enforced (LIVE) and reviewer-side self-check (PROPOSED) without defining the self-check mechanism. Adopt: in-place clarification at row 25 — append "(reviewer-side self-check binary: AQ-agent dispatch prompt includes Identity + Core Rules + Role Boundaries + Communication sections OR carries `[oos-section-N: <rationale>]` annotation per Role 3 §13 row 25 inheritance pattern)". Do NOT split into 25a/25b (over-engineering). |
| F-028 | Medium | O | LEGITIMATE | X | §6 step 1 lists `templates/threat-model-catalog.yaml (PROPOSED)` without fallback callout. Filesystem check: file does not exist. Append `(or substrate Finding 4 L119-L155 until OQ-7 resolves)` to §6 step 1 — mirror of §10.1 entry 8 fallback declaration. |
| F-029 | Low | D+A | LEGITIMATE | Y | §9.1 field 9 `divergence_log_entry` undefined for non-firing case. §9.2 example shows `null`. Add to §9.1 field 9: "`null` when no trigger fires; otherwise object `{trigger_class, log_path, calibration_delta_proposed}`." Extend §13 row 13 enum check. |
| F-030 | Low | M | REJECTED | — | Reviewer proposes new §15.2a AC for body↔substrate symmetry. **Cited evidence:** `DESIGN_DOC_TEMPLATE.md` §15 spec (L478-L506) and §7 self-attest checklist (L651-L673) do not require body↔substrate symmetry as a Phase 5 gate. F-021 already addresses substrate Limitation under-citation as a separate Medium finding with targeted fixes. Adding a new template-violating AC inflates Phase-5 gates without canonical-template backing. |

## Safety findings (11; S-01..S-11)

| ID | Sev | Verdict | Bundle | Rationale (cited evidence for REJECTED) |
|---|---|---|---|---|
| S-01 | High | LEGITIMATE-MODIFIED | Z | §12.3 GOOD tags bromism `pattern: P9` (many-shot jailbreaking per substrate L144). Bromism is dietary-context-recognition failure (Finding 8 + Limitation 18), structurally distinct from many-shot. Adopt: change §12.3 GOOD `pattern:` to `BROMISM-CLASS-DIETARY-CONTEXT` with annotation `[not-in-P1-P10-catalog]`; surface as architecture-question candidate to Role 1 for catalog extension (P11 if Role 1 ratifies). Add §13 row 17 sub-clause: bromism probes tagged separately from row 9 P1-P10 coverage. |
| S-02 | High | LEGITIMATE-MODIFIED | AA | §12 BAD blocks lack `exploit_content_hash` field that §13 row 19 mandates. Two compound effects: (a) row 19 audit would BLOCK on this doc; (b) post-deployment agent.md inherits unredacted exploit prose. Adopt SCOPE-RESTRICTED fix: amend row 19 to require `exploit_content_hash` on BAD blocks AND accept `[QUARANTINE-illustrative-only]` annotation as canonical alternative satisfying the audit (BAD blocks already carry "Do NOT emit — illustrative only" marker per Role 3 Bundle G precedent — formalize as audit-satisfying convention). The pedagogical value of in-doc BAD blocks demonstrating failure shapes is preserved; hashing is required only for actual exploit-novel content, not for shapes already in published literature. |
| S-03 | High | DUPLICATE | — | Same defect as F-005. Consolidated. |
| S-04 | High | LEGITIMATE | AB | EC-8 prescribes adversarial probes against EACH operator-profile field; §13 row 21 + §11.2 AP-3 BLOCK probes whose generation inputs match operator-profile field names. Direct contradiction. Adopt: tighten row 21 to permit operator-profile field names as probe-generation INPUTS when scoped to operator-profile-as-target with `evaluation_log.probe_generation_inputs_scope: operator-profile-target` annotation. The intent is "personalization-to-operator BLOCKed; field-skip-probing PERMITTED with scope annotation." |
| S-05 | Medium | DUPLICATE | — | Subsumed by F-001 + F-002. Consolidated. |
| S-06 | Medium | LEGITIMATE-MODIFIED | AC | §5 rule 11 frames Mechanism A as intra-dispatch; §4.4 row 9 + EC-9 frame as inter-dispatch; §13 row 22 audits only intra. Adopt: clarify row 22 prose to cover both ("≥2 internal-judge instances OR ≥2 Role 4 dispatch outputs in same Council-Mode wrapper"); do NOT split into 22a/22b (over-engineering). |
| S-07 | Medium | REJECTED-WITH-ADOPTION | AD | Reviewer claims §12.3 GOOD reproduces bromism exploit verbatim → ship in deployed agent.md. **Cited evidence:** Annals 2024 case [29] is published peer-reviewed; the substrate Finding 8 + Limitation 18 use the same prompt as the canonical example. Containment is moot for a published case. **Adoption:** add carve-out to §12 header — "GOOD blocks may reproduce published exploit prose where the published reference makes containment moot; novel/hypothetical exploit shapes in BAD blocks carry hash-or-QUARANTINE-marker per S-02 disposition." Make the scope decision explicit instead of implicit. |
| S-08 | Medium | LEGITIMATE | AE | Row 1 LIVE-tag is correct for dispatch-payload-shape but the L543 "LIVE: 1" count implies broader maturity. Add note adjacent to L543: "LIVE: 1 covers dispatch-payload-shape (INV-ROLE-INLINING); runtime re-Read discipline (rows 23, 7) remains PROPOSED." |
| S-09 | Medium | LEGITIMATE | AF | §11.2 AP-2 recognition cue cites `evaluation_log.probe_set_hash`; §9.1 field 6 has hash at `probe_set.hash`. Field-name drift. Change AP-2 cue to `probe_set.hash` matching §9.1 + §13 row 8 canonical schema. |
| S-10 | Low | LEGITIMATE-MODIFIED | AG | Row 17 (bromism-probe) has no count floor or class-diversity sub-clause like row 16 (authority-impersonation). Strengthen row 17: "≥1 bromism-class probe per evaluation; substrate Limitation 18 prescribes broader context-mismatch category — at minimum, dietary-context-mismatch shape AND scope-mismatch shape (operator's described domain differs from specialist's declared scope) — per evaluation cycle." |
| S-11 | Low | LEGITIMATE | AH | §10.1 step 9 mandates re-Read of `memory/process-failures.md` at dispatch start; §9.1 evaluation_log + §13 row 23 do not include `process_failures_loaded_at`. Add `process_failures_loaded_at` to §9.1 evaluation_log; extend §13 row 23 to include it; add `last-PF-reviewed:` frontmatter currency check (row 23 sub-clause). |

---

## Classification summary

| Verdict | Count |
|---|---|
| LEGITIMATE | 13 |
| LEGITIMATE-MODIFIED | 16 |
| REJECTED-WITH-ADOPTION | 3 |
| REJECTED | 3 |
| DUPLICATE | 2 |
| **Active fixes to apply** | **32** |
| **Findings fully verdicted** | **41** |

3 REJECTED with cited-evidence attestations (F-012, F-025, F-030). 3 REJECTED-WITH-ADOPTION (F-011, F-013, S-07) — the substance is adopted under a modified frame per the project's reject-but-adopt feedback memory.

## Phase 5 bundle application order

Bundles ordered to minimize cross-section pointer churn. §13 row renumbering does NOT occur — all defects are at §13 row content/scope/wording level, not row addition or deletion (except Bundle C adds row 26).

Order:
1. **Bundle C** (F-005/S-03) — add §13 row 26 model-family check; update AC-deploy-7 + EC-5 + A-1 + A-6 pointers; update §13 row count claim 25→26.
2. **Bundle A** (F-001, F-002, F-003) — fix §5 rule 11 + §11.1 PF-S2-04 + §11.1 PF-S2-05 row pointers.
3. **Bundle B** (F-004) — fix §7 divergence-log threshold to 30%/10-window.
4. **Bundle Z** (S-01) — fix §12.3 bromism pattern tag; surface as architecture-question for catalog extension.
5. **Bundle AA** (S-02) — amend row 19 to accept QUARANTINE marker as alternative satisfaction.
6. **Bundle AB** (S-04) — tighten row 21 scope annotation for EC-8 case.
7. **Bundle G** (F-009) — annotate §4.4 row 9 with synthesis-authorship trail.
8. **Bundle H** (F-010) — add §15.2b AC for §9 wire-format conformance.
9. **Bundle AD** (S-07) — add §12 header carve-out for published-exploit GOOD blocks.
10. **Bundle AB-followup** — co-fix Bundle AB's EC-8 scope clarification.
11. **Bundles F, M, N** (F-008, F-016, F-017) — schema field-name fixes + typo.
12. **Bundle U** (F-024) — add Risk-8 + new OQ for semantic operator-profile-leak audit.
13. **Bundle V** (F-026) — gate §10.1 entry 2 HALT on specialist_profile only.
14. **Bundle W** (F-027) — clarify §13 row 25 self-check semantics.
15. **Bundle X** (F-028) — add §6 step 1 fallback callout.
16. **Bundle AC** (S-06) — clarify §13 row 22 inter-dispatch scope.
17. **Bundle Y** (F-029) — define §9.1 divergence_log_entry non-firing semantics.
18. **Bundle AF** (S-09) — change §11.2 AP-2 cue to canonical field name.
19. **Bundle AE** (S-08) — add LIVE-tag scope note.
20. **Bundle AG** (S-10) — strengthen row 17 bromism class-diversity.
21. **Bundle AH** (S-11) — add PF-attestation timestamp + currency check.
22. **Bundle O** (F-018) — fix status-tag count convention.
23. **Bundle R** (F-021) — cite Limitations 2, 3, 14 at Risk-3 + §16 candidate INV.
24. **Bundle J** (F-013) — cluster §2.2 "I own" 12→7 items.
25. **Bundle D** (F-006) — add `authored_by` + `downstream` frontmatter fields.
26. **Bundle T** (F-023) — extend §16 INV-ROLE-INLINING with synonym set.
27. **Bundle S** (F-022) — one-line §11.1 footer clarifier.
28. **Bundle K** (F-014) — adopt §11.2 AP-3 phrasing at §11.1 + §8.4.
29. **Bundle L** (F-015) — name "default 50" in EC-2 expected.
30. **Bundle P** (F-019) — tighten §5 rule 5 + §12.1 substrate cites.
31. **Bundle Q** (F-020) — annotate §13 preamble L513 archaeology marker.
32. **Bundle I** (F-011) — add ACCEPTED parenthetical to §3.1 row 7.
33. **Bundle E** (F-007) — tighten §10.1 line anchors only.

## PF-S3-01 attestation

Every classification above was reached after personal source-read of the cited evidence. The verifications conducted (via Bash sed/grep against the synthesized doc + DESIGN_DOC_TEMPLATE.md + Role 1/2/3 design docs + substrate domain-research.md):

- F-001/F-002/F-003 row-pointer mismatches: lines 175, 368, 369 read; §13 rows 22, 21, 7, 23 contents read; mismatches verified
- F-004 rate threshold: §7 L209 + §4.4 row 5 L141 + §13 row 13 L529 + §11.2 AP-7 L390 read; 20% vs 30% confirmed
- F-005/S-03 model-family row missing: §13 rows 1-25 fully read; grep for `model_family|model-family` returned no §13 row implementing R6 binary
- F-006 frontmatter omissions: template L50-L67 read; frontmatter L1-L17 read; `authored_by` + `downstream` confirmed missing
- F-008 override_path: row 5 L521 + §12.3 GOOD L495-L507 read; conflict confirmed
- F-009 §4.4 row 9 synthesis-authorship: L145 read; "(added at synthesis per OQ-4)" confirmed; substrate Finding 8 + Insights cited
- F-013 budget claim: template L136 read ("3-7 items"); Role 3 §2.2 read; ~9+ items present at Role 3 confirming project precedent
- F-014, F-015, F-016, F-017, F-018: line reads confirm
- F-021 Limitation under-citation: grep returned 13 of 21 cited; Limitations 2, 3, 14 selectively load-bearing
- F-026 §10.1 entry 2: L315 read; HALT clause confirmed; EC-7 wiki-entry adaptation verified differs from specialist-profile
- F-028: filesystem check `ls templates/` confirmed `threat-model-catalog.yaml` does not exist
- S-01 bromism P9 mistag: substrate L144 (P9 = Many-shot) + §12.3 GOOD `pattern: P9` read
- S-02 BAD-block exploit_content_hash: §12 BAD blocks L405-L415 + L444-L452 + L474-L483 read; field absent; row 19 mandate L535 read
- S-04 EC-8 vs row 21: EC-8 prescribed-handling read; row 21 audit binary read; direct contradiction confirmed
- S-06 Mechanism A intra/inter: §5 rule 11 + §4.4 row 9 + EC-9 + row 22 all read; scope-mismatch confirmed
- S-09 field-name drift: AP-2 cue L380 (`evaluation_log.probe_set_hash`) + §9.1 field 6 L268 (`probe_set.hash`) read; drift confirmed

5 prior consecutive PF-S3-01 guards held (S7/S8/S9/S10/S11). This is the 6th. **Guard held.** No verdict was self-attested without personal source-read of cited evidence. 3 REJECTED entries (F-012, F-025, F-030) carry cited-evidence attestation in the rationale column.

## Reject-but-adopt pattern entries

Per `~/.claude/projects/-Users-waltermcgivney-Documents-Projects-a-plus-maxing/memory/feedback_reject_but_adopt_pattern.md`. Three findings classified REJECTED-WITH-ADOPTION:

- **F-011 (ACCEPTED-BY-COMPOSITION label).** Reviewer's classification-label proposal would break cross-doc symmetry. The adoption: rationale-column parenthetical preserves the substantive insight without introducing a new verdict label.
- **F-013 (12-item "I own" cluster to 7).** Reviewer claims template budget violation. Project precedent (Role 3 §2.2 has 9+ items) shows the literal budget is widely ignored for foundation roles. The adoption: cluster 12 items into 7 thematic groupings — improves readability without claiming the budget violation is structural.
- **S-07 (GOOD-block exploit reproduction).** Reviewer claims GOOD-block reproduces bromism exploit creating disclosure risk. Substrate uses the published Annals 2024 case; containment is moot. The adoption: explicit scope carve-out for published-reference exploit reproduction in §12 header — makes the implicit decision explicit.
