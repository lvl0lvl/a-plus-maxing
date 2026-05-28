---
title: health-edge-case-reviewer Design Doc — Phase 3 Red-Team Adversarial Review
type: red-team-findings
phase: 3
target: design/health-edge-case-reviewer-design.md
target_status_at_review: Phase-3 Red-Team Pending (816 lines, 18 sections + Appendix A stub)
reviewer_skill: ~/.claude/skills/adversarial-review/SKILL.md
session: S11
created: 2026-05-27
---

# Phase 3 Red-Team Adversarial Review — health-edge-case-reviewer Design Doc

Fresh-context adversarial walk per `~/.claude/skills/adversarial-review/SKILL.md`. 8 categories (A / E / C / R / O / S / D / L) walked across 18 sections consolidated into 7 sectional groups. Quote-grounded; every finding cites the exact passage in the design doc that contains the defect.

**Pre-check.** Three reference files loaded:
- `~/.claude/skills/adversarial-review/references/sample-reviews-documents.md` (4 calibration examples)
- `~/.claude/skills/adversarial-review/references/language-economy.md` (bidirectional token analysis)
- `~/.claude/skills/adversarial-review/references/instruction-safety.md` (containment patterns)

**Cross-document verification performed.** `design/health-specialist-architect-design.md` (Role 1 Final), `design/health-implementer-design.md` (Role 2 Final), `design/CONTINUATION_BRIEF.md`, `design/.health-edge-case-reviewer-design-work/domain-research.md`, `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, `INVARIANTS.md`, `memory/process-failures.md`, `scripts/` (3 files), `.claude/hooks/` (4 files), `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`.

**Sectional consolidation (per SKILL.md Step 3, >10 sections → 5-10 groups).** G1 = §§1-2 (Problem + Role Definition); G2 = §§3-4 (Pass-1 Digest + Cross-Role References); G3 = §§5-7 (Behavioral Rules + Ask-vs-Proceed + Loop-Breaking); G4 = §§8-10 (Tools + Communication + Context Loading); G5 = §§11-12 (Anti-Patterns + Negative Examples); G6 = §13 (Mechanical Enforcement Map); G7 = §§14-18 (Edge Cases + ACs + Invariants + Risk + Open Questions + Appendix A).

---

## Findings

### F-001 — §11.1 PF-S6-01 row cites wrong §13 row number

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Critical |
| **Section** | §11.1 (G5); §13 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §11.1 says re-review-on-amendment is enforced at §13 row 12, but §13 row 12 is "Atomic-claim decomposition (wiki-entry-review only)". The re-review-on-amendment audit is actually §13 row 22. EC-4 line 592 and EC-7 line 622 both cite row 22 correctly, so the doc contradicts itself.

**Evidence.** Line 335 (§11.1, PF-S6-01 row): "Mechanical guard: §13 row 12 (re-review-on-amendment trigger; `reviewed_against_ancestry_sha:` field)." Line 531 (§13 row 12): "Atomic-claim decomposition [R11; Finding 9; arch R3.11; wiki-entry-review only] ... For specialist-profile reviews (target_type == specialist_profile), this row is N/A". Line 541 (§13 row 22): "Re-review-on-amendment trigger [PF-S6-01; QA Q12] ... Role 3 maintains `reviewed_against_ancestry_sha:`".

**Adversarial probe.** "Every stated row number must match its row (C category, Step 3 priority 3)." An agent following the §11.1 row-12 pointer will land on atomic-claim decomposition (an N/A row for specialist-profile reviews), conclude PF-S6-01 has NO mechanical guard for specialist-profile reviews, and ship without ancestry tracking.

**Fix.** Replace "§13 row 12" with "§13 row 22" in line 335.

---

### F-002 — §11.1 PF-S2-04 row cites wrong §13 row number

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Critical |
| **Section** | §11.1 (G5); §13 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §11.1 says PF-S2-04 (operator-profile inlining) is guarded at §13 row 7, but §13 row 7 is "Mechanical-pre-audit before semantic adjudication". The operator-profile inlining audit is actually §13 row 5 ("operator-profile under-coverage surfacing" + "operator-inlining-detection").

**Evidence.** Line 331 (§11.1, PF-S2-04 row): "Mechanical guard: §13 row 7 (operator-profile inlining detection — finding when specialist body grep matches operator-name/date tokens)." Line 524 (§13 row 5): "also grep-checks specialist body for operator-bound tokens (`Walter`, `2026-01`, etc.) and emits a finding on any match" with check `--check operator-inlining-detection`. Line 526 (§13 row 7): "Mechanical-pre-audit before semantic adjudication".

**Adversarial probe.** Same C-category probe as F-001. Following row 7 leads to the wrong check; the operator-inlining grep at row 5 will never be invoked.

**Fix.** Replace "§13 row 7" with "§13 row 5" in line 331.

---

### F-003 — §11.1 PF-S2-05 row cites two wrong §13 row numbers

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Critical |
| **Section** | §11.1 (G5); §13 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §11.1 says PF-S2-05 (mental-model invocation of canonical taxonomy) is guarded at "§13 row 1 (canonical YAML sourced at every review) + row 11 (re-read cadence attestation)". Both row references are wrong. §13 row 1 is "Finding-not-fix + reviewer-finding schema"; §13 row 11 is "Adjudication path named". The re-read cadence attestation audit is actually §13 row 21 ("Self-audit-before-return + re-Read cadence attestation").

**Evidence.** Line 332 (§11.1, PF-S2-05 row): "Mechanical guard: §13 row 1 (canonical YAML sourced at every review) + row 11 (re-read cadence attestation)." Line 520 (§13 row 1): "Finding-not-fix + reviewer-finding schema". Line 530 (§13 row 11): "Adjudication path named". Line 540 (§13 row 21): "Self-audit-before-return + re-Read cadence attestation ... Output carries `re_read_attestation: {refusal_taxonomy_loaded_at, risk_class_table_loaded_at, review_started_at}`".

**Adversarial probe.** C-category. The "canonical YAML sourced at every review" check does not exist as a row at all — it is the verbal description of part of row 21. PF-S2-05 will appear guarded but has no actual row implementing the cited guard.

**Fix.** Replace "§13 row 1 (canonical YAML sourced at every review) + row 11 (re-read cadence attestation)" with "§13 row 21 (re-read cadence attestation, including refusal_taxonomy + risk_class_table loaded-at timestamps)" in line 332.

---

### F-004 — §11.1 PF-S2-02 row cites wrong §13 row for quoted-text-verbatim

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Critical |
| **Section** | §11.1 (G5); §13 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §11.1 says PF-S2-02 (citation/locator drift) is guarded at "§13 row 4 (locator-resolution) + row 5 (quoted_text verbatim)". Row 4 is correct (locator-resolution). Row 5 is wrong — row 5 is operator-profile under-coverage. The quoted-text-verbatim audit is §13 row 20.

**Evidence.** Line 329 (§11.1, PF-S2-02 row): "Mechanical guard: §13 row 4 (locator-resolution) + row 5 (quoted_text verbatim)." Line 524 (§13 row 5): "Operator-profile under-coverage surfacing (AQ-001-dependent)". Line 539 (§13 row 20): "Quoted-text-verbatim audit ... Every finding's `quoted_text:` appears verbatim at cited locator".

**Adversarial probe.** Same C-category cascade. The four mis-references in §11.1 (F-001 through F-004) suggest §13 was renumbered late in synthesis but §11.1 was not re-anchored. Calls into question every other §13 row pointer in §11.1.

**Fix.** Replace "§13 row 4 (locator-resolution) + row 5 (quoted_text verbatim)" with "§13 row 4 (locator-resolution) + row 20 (quoted_text verbatim)" in line 329. Audit the remaining §11.1 row references (PF-S2-01: rows 1+3; PF-S2-03: row 6; PF-S3-01: rows 2+3 — these four appear correct on inspection but the synthesizer should re-verify each before close).

---

### F-005 — `templates/AGENT_TEMPLATE.md` referenced as forbidden Edit target but file does not exist

| Field | Value |
|---|---|
| **Category** | R — Broken References |
| **Severity** | Important |
| **Section** | §8.3 (G4) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §8.3 lists `AGENT_TEMPLATE.md` (alongside `templates/`) as a forbidden Edit target. The project's `templates/` directory contains only `refusal-class-taxonomy.yaml` and `specialist-risk-class.yaml`; there is no `AGENT_TEMPLATE.md` in the project at all. The actual file is at `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` (verified via filesystem). A fresh agent following §8.3 cannot determine WHICH `AGENT_TEMPLATE.md` is forbidden — and may interpret the list adjacency `templates/`, `Role 1/2 design docs`, `DESIGN_DOC_TEMPLATE.md`, `AGENT_TEMPLATE.md` as project-relative.

**Evidence.** Line 225 (§8.3): "Edit / Write against any path under review: specialist `agent.md`, `.claude/agents/`, `templates/`, Role 1/2 design docs, `DESIGN_DOC_TEMPLATE.md`, `AGENT_TEMPLATE.md`, `INVARIANTS.md`, `CLAUDE.md`, `memory/process-failures.md`, `vault/library/`, ...". `ls /Users/waltermcgivney/Documents/Projects/a-plus-maxing/templates/` → only the two .yaml files. `find ... -name AGENT_TEMPLATE.md` → only `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`.

**Adversarial probe.** R-category: "Does every reference point to something real?" An agent literally checking `templates/AGENT_TEMPLATE.md` will fail. An agent guessing `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` is correct but the doc never says so.

**Fix.** Replace `AGENT_TEMPLATE.md` with the absolute path `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` in line 225. (Role 1 and Role 2 design docs both also reference AGENT_TEMPLATE.md — if they share this defect, it is an upstream issue to escalate via AQ rather than fix here.)

---

### F-006 — §13 row 1 lists `recommendation.action` enum but Negative Examples emit a different field name

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Important |
| **Section** | §13 row 1 (G6); §12 (G5); §2.2 (G1) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §13 row 1 defines the schema field as `recommendation.action ∈ {revise_wiki_entry, add_caveat, withdraw_claim, stratify_claim, refer_to_role4, escalate_to_adjudicator}`. The §12 Negative Examples emit `recommendation_class:` and `target_field:` as flat top-level fields, not as nested `recommendation.{action, target_field}`. §2.2 line 51 says "the per-finding output schema (... `paired_probe_status`)" but never lists `recommendation` as an owned field — it lists `recommendation` only in §4.3 row 1 as `recommendation{action,target_field}`. Three different shapes for the same field across §2.2, §4.3, §12, and §13.

**Evidence.** Line 520 (§13 row 1): "`recommendation.action ∈ {revise_wiki_entry, add_caveat, withdraw_claim, stratify_claim, refer_to_role4, escalate_to_adjudicator}` + `target_field`". Line 130 (§4.3 row 1): "`recommendation{action,target_field}`". Lines 461-464 (§12.2 GOOD example): `recommendation_class: add_refusal_class` and `target_field: Role Boundaries` (flat, no nesting; `add_refusal_class` is not in the row-1 enum). Line 501 (§12.3 GOOD): `recommendation_class: add_refusal_class` (same — flat, not in the enum).

**Adversarial probe.** D-category + C-category: the Negative Examples are the calibration the reviewer mimics. A reviewer copying §12.2 GOOD produces `recommendation_class: add_refusal_class` — which the row-1 schema validator (`scripts/audit-reviewer-output.sh --schema templates/reviewer-finding.schema.json`) will reject because (a) the field name is wrong and (b) `add_refusal_class` is not in the enum.

**Fix.** Decide one shape and apply it everywhere. Recommended: keep the nested `recommendation: {action, target_field}` per §13 row 1, expand the enum to include `add_refusal_class` (or rewrite the Negative Examples to use a canonical value like `revise_wiki_entry`), and update §12.2 GOOD + §12.3 GOOD to emit the nested form. Without this fix every Negative Example fails the schema the reviewer is supposed to satisfy.

---

### F-007 — §12 BAD examples emit literal severity tokens that the doc bans elsewhere

| Field | Value |
|---|---|
| **Category** | A — Ambiguous Instructions / Imperative Bleed |
| **Severity** | Important |
| **Section** | §12.3 (G5) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §12.3 BAD shows `severity_final: WARN  (set by reviewer)` and the Why explains BAD violates §5 rule 7. But §15.2b AC-deploy-19 says the deployed `agent.md` must satisfy `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" .claude/agents/health-edge-case-reviewer/agent.md = 0`. The deployed agent.md is downstream of this design doc via `/upgrade-agent` — if §12 BAD content gets carried verbatim into the deployed profile (per Role 2 §5 rule 4: "design doc legitimately quotes banned phrases inside §12 BAD code blocks; the deployed `agent.md` must not"), the deployed agent grep fails. This design doc does not itself contain banned tokens, but the per-instruction-safety reference §7 "Quarantine examples" pattern requires every BAD block to be explicitly marked as non-executable to defend against imperative bleed during the agent's runtime read of its own profile.

**Evidence.** Line 484 (§12.3 BAD): "severity_final: WARN  (set by reviewer)". Line 671 (§15.2b AC-deploy-19): "`grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" .claude/agents/health-edge-case-reviewer/agent.md` = 0." None of §12.1/§12.2/§12.3 BAD blocks carry a "Do NOT execute" prefix; they are headed only as `BAD (cites §11.2 AP-N):`. Per `instruction-safety.md` §7 "Quarantine examples" containment pattern, that label is the bare minimum but is not explicit enough that a downstream consumer (e.g., `/upgrade-agent` Phase 4) can mechanically distinguish "show the reviewer this is wrong" from "the reviewer should emit this shape".

**Adversarial probe.** A-category: "If I deliberately misread this in the most plausible wrong way, what breaks?" A `/upgrade-agent` worker condensing the design doc into the deployed profile may strip the `BAD (cites ...)` heading and carry the YAML block verbatim, producing a deployed agent.md that includes `severity_final: WARN  (set by reviewer)` — exactly the failure mode §12.3 is supposed to PREVENT, and a structural violation of §5 rule 7.

**Fix.** Add explicit "Do NOT emit — illustrative only" comments inside each BAD YAML block, AND add an explicit instruction in §12 (intro paragraph) stating that BAD blocks must not be reproduced in the deployed agent.md (mirroring Role 2 §5 rule 4 grep-scoping). Alternatively, replace the BAD-block YAML with a description-of-the-mistake prose, eliminating the imperative-bleed surface entirely.

---

### F-008 — §13 row 5 status conflicts with itself (PROPOSED + bifurcated WARN/BLOCK)

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Important |
| **Section** | §13 row 5 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §13 row 5 has Status `PROPOSED` and Consequence `WARN (pre-AQ-001) → BLOCK (post-AQ-001)`. The §13 status-tag rubric (cited from Role 2 §18 OQ-7 at line 512) defines exactly three values: LIVE, REFERENCED, PROPOSED. A Status of PROPOSED with a bifurcated Consequence creates an undefined state — a script does not know which Consequence to fire because the gating fact (AQ-001 resolved or not) is not a §13 row field; it is an external orchestrator decision tracked in §18 OQ-2. §13 row 5 is therefore neither auditable nor enforceable until AQ-001 lands.

**Evidence.** Line 524 (§13 row 5): "PROPOSED | WARN (pre-AQ-001) → BLOCK (post-AQ-001)". Line 512 (§13 preamble): "QA-strict tagging per project-wide resolution at Role 2 §18 OQ-7 (LIVE requires both (a) check script/hook exists AND (b) smoke test exercises it against a negative case; REFERENCED requires citing an INV-* ID whose mechanical verification is proven per `INVARIANTS.md`; PROPOSED otherwise)." Line 544: "Status-tag count. LIVE: 0. REFERENCED: 1 (row 23). PROPOSED: 22." — counted as a single PROPOSED, ignoring the bifurcation.

**Adversarial probe.** C + A: the row's behavior is conditional on a fact that does not live in any §13 field. A script reading `scripts/audit-reviewer-output.sh --check operator-profile-coverage` cannot tell whether to WARN or BLOCK without out-of-band knowledge of AQ-001's resolution state. Two reviewers will produce different behavior on the same artifact.

**Fix.** Either (a) split row 5 into two rows — 5a `WARN, PROPOSED pre-AQ-001` and 5b `BLOCK, PROPOSED post-AQ-001 trigger` — with an explicit dependency edge in §18 OQ-2, or (b) keep WARN as the active Consequence and add a §18 OQ-2 follow-up bead promoting WARN→BLOCK upon AQ-001 resolution. Either fix makes the row binary-auditable; the current bifurcation is not.

---

### F-009 — §13 row 12 status declares N/A for specialist-profile reviews but row is counted as PROPOSED

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Important |
| **Section** | §13 row 12 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §13 row 12 (atomic-claim decomposition) is N/A for specialist-profile reviews and BLOCK for wiki-entry reviews. The row 12 status is single-valued `PROPOSED` and Consequence is `BLOCK (wiki) / N/A (specialist)`. The line 544 status-tag count says "PROPOSED: 22" — counting row 12 once even though its applicability is binary on target_type. A reviewer running a specialist-profile review will be told row 12 is PROPOSED + BLOCK by the audit script invocation pattern, and either incorrectly halts on an N/A row or silently skips a row that should BLOCK in a sibling review type.

**Evidence.** Line 531 (§13 row 12): "PROPOSED | BLOCK (wiki) / N/A (specialist)". Line 544: "PROPOSED: 22". Line 531 body: "For wiki entries (target_type == compound\|biomarker\|protocol), ... For specialist-profile reviews (target_type == specialist_profile), this row is N/A".

**Adversarial probe.** C + O: the script-invocation pattern (`scripts/audit-reviewer-output.sh --check atomic-decomposition`) has no documented `--target-type` flag in §13 row 12. The applicability switch is described in prose but is not in the audit-script interface.

**Fix.** Add explicit `--target-type {specialist_profile, wiki_entry}` parameter to the row 12 audit-script invocation, and clarify that for `--target-type=specialist_profile` the row is auto-PASS (not BLOCK and not skipped). Update line 544 counts to reflect target-type-conditional applicability.

---

### F-010 — §15.2a AC-2 awk count discards `DEFERRED`/`REJECTED` verdicts but §3.2 has none, leaving the check tautological

| Field | Value |
|---|---|
| **Category** | E — Edge Case Gaps |
| **Severity** | Suggestion |
| **Section** | §15.2a AC-2 (G7); §3.2 (G2) |
| **Resolution** | Accept (low impact) or Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** AC-2 awk pattern accepts `ACCEPTED|DEFERRED|REJECTED` as valid verdicts. §3.2 contains 15 rows, all `ACCEPTED` (some with hyphenated qualifiers). The check is tautological for this doc — the only failure path is a row with verdict outside that set, which by construction will not occur. More important: the check counts `n==15` strictly. If a future amendment downgrades R11 from "ACCEPTED — narrowed-scope" to "DEFERRED", AC-2 still passes — but the design intent of R11 (atomic-claim decomposition narrowed to wiki entries) silently changed. No-action.

**Evidence.** Line 651 (AC-2): "`awk -F'|' '/^\| R[0-9]+/{n++; if($4 !~ /ACCEPTED|DEFERRED|REJECTED/) exit 2}END{exit (n==15)?0:3}' ...` exits 0." Lines 81-95 (§3.2): every R-row has `| ACCEPTED |` or `| ACCEPTED — calibration-pending |` or `| ACCEPTED — narrowed-scope |`.

**Adversarial probe.** E-category: "What scenario does this not address?" The check cannot detect downgrade of an ACCEPTED row to DEFERRED — both pass. The check also cannot detect when "ACCEPTED — calibration-pending" becomes vacuous (e.g., calibration completed but qualifier not removed).

**Fix.** Optional: tighten AC-2 to require strict `ACCEPTED` (without qualifier discounting), or accept the looseness as a known limitation. The current looseness is intentional per the explicit "Hyphenated qualifiers ... permitted" clause, so the finding is suggestion-only.

---

### F-011 — §5 rule 4 paired-probe annotation `[no-paired-probe-required: <rationale>]` is ambiguous about how the rationale is verified

| Field | Value |
|---|---|
| **Category** | A — Ambiguous Instructions |
| **Severity** | Important |
| **Section** | §5 rule 4 (G3); §13 row 8 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §5 rule 4 permits annotating `[no-paired-probe-required: <rationale>]` as an escape from paired-probe discipline. §13 row 8 audits "pair-existence audit walks finding set looking for unpaired refusals" but does not specify any check on the rationale content. The mechanical audit only verifies the annotation tag is PRESENT; it does not verify the rationale is non-empty, non-trivial, or substantive. A reviewer can satisfy paired-probe discipline by annotating `[no-paired-probe-required: skipped]` on every refusal — exactly the rubber-stamp surface §11.2 AP-2 forbids.

**Evidence.** Line 148 (§5 rule 4): "Pair every "specialist refused" probe with a "specialist answered" probe drawn from the same boundary region, or annotate `[no-paired-probe-required: <rationale>]`." Line 527 (§13 row 8): "Every "specialist refused" finding has a paired "specialist answered" finding from same `boundary_region` OR carries `[no-paired-probe-required: <rationale>]`; pair-existence audit walks finding set looking for unpaired refusals". Neither passage names a rationale-quality check.

**Adversarial probe.** A-category: "If I deliberately misread this in the most plausible wrong way, what breaks?" A reviewer interpreting "carry the annotation" as sufficient produces empty-annotation outputs that pass mechanical audit but defeat the paired-probe discipline this row exists to enforce.

**Fix.** Add to §13 row 8 a sub-check: every `[no-paired-probe-required: <rationale>]` annotation has `wc -w` ≥ 5 AND the rationale references the canonical taxonomy class identifier from `templates/refusal-class-taxonomy.yaml`. OR escalate the rationale-quality check to a paired adjudicator agent (mirroring §11.2 AP-7 divergence-log dispatch pattern), explicitly removing it from mechanical-audit scope.

---

### F-012 — §8.3 path list ambiguity: `templates/` could be read as forbidding Read, contradicting §10.1

| Field | Value |
|---|---|
| **Category** | A — Ambiguous Instructions |
| **Severity** | Suggestion |
| **Section** | §8.3 (G4); §10.1 (G4) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §8.3's forbidden list opens with "**Edit / Write against any path under review:** specialist `agent.md`, `.claude/agents/`, `templates/`, ...". The bold prefix scopes the prohibition to Edit/Write only. But the immediate-next-line phrase "**The reviewer never edits the artifact under review.**" generalizes to "edit"; combined with the path list including `templates/`, an agent could read the entire bullet as "the reviewer never touches anything under `templates/`" — forbidding the Read of `templates/refusal-class-taxonomy.yaml` and `templates/specialist-risk-class.yaml` that §10.1 items 6 and 7 mandate as auto-load. The bold prefix is the disambiguator but lives 3 words before the list, weak structural separation.

**Evidence.** Line 225 (§8.3): "**Edit / Write against any path under review:** specialist `agent.md`, `.claude/agents/`, `templates/`, Role 1/2 design docs, ... **The reviewer never edits the artifact under review.**". Lines 283-284 (§10.1 items 6+7): "**`templates/refusal-class-taxonomy.yaml`** — canonical 8-class taxonomy. Reviewer audits against this enum ... **`templates/specialist-risk-class.yaml`** — per-specialist `aplus-research` mode-floor table; reviewer audits mode-floor correctness against this table."

**Adversarial probe.** A-category. A fresh-context agent reading §8.3 first (because it precedes §10) may infer "templates/ is off-limits", then halt with an `inaccessible-canonical-taxonomy` error when §10.1 instructs auto-load. The bold-prefix disambiguator is small and easily missed.

**Fix.** Rephrase line 225 as "**Edit / Write (NOT Read) against any path under review:**" — making the Read-allowed semantics explicit. Alternatively, restructure §8.3 to list the paths under separate bullets per operation.

---

### F-013 — §11.2 AP count claim ("7 entries; 5–8 range") matches but §11.2 intro narrative is inconsistent

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Suggestion |
| **Section** | §11.2 (G5); §12 (G5) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §11.2 declares "7 entries". §12 opening line says "Three BAD/GOOD pairs targeting Role-3-specific failure modes. Re-anchored at synthesis to §11.2 AP numbering (SE-draft anticipated 1–5; QA delivered 7)." That parenthetical is process commentary that bleeds into the deployed-profile content. The phrase "SE-draft anticipated 1–5; QA delivered 7" is meaningful only to the synthesizer; it confuses a fresh-context reader who has no concept of "SE-draft" or "QA delivered" in the deployed agent's runtime.

**Evidence.** Line 339 (§11.2): "**7 entries; 5–8 range**". Line 403 (§12): "Three BAD/GOOD pairs targeting Role-3-specific failure modes. Re-anchored at synthesis to §11.2 AP numbering (SE-draft anticipated 1–5; QA delivered 7)."

**Adversarial probe.** A + L: the parenthetical is build-pipeline narrative leaking into a section whose downstream consumer is the deployed reviewer. The phrase has zero behavioral content; it costs ~12 tokens and adds confusion.

**Fix.** Delete the parenthetical "(SE-draft anticipated 1–5; QA delivered 7)" from line 403. The Phase-1 ownership story belongs in Appendix A.

---

### F-014 — `scripts/audit-reviewer-output.sh` referenced 14 times as if existent but does not exist; §18 OQ-1 acknowledges this only obliquely

| Field | Value |
|---|---|
| **Category** | R — Broken References + D — Downstream Breakage |
| **Severity** | Important |
| **Section** | §13 (G6); §18 OQ-1 (G7) |
| **Resolution** | Accept (explicitly PROPOSED) or Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** `scripts/audit-reviewer-output.sh` is the named mechanism for 14 §13 rows (rows 1-15 except 12 which uses `scripts/atomic-claim-decompose.sh` AND `scripts/audit-reviewer-output.sh`). The script does not exist (verified: `ls scripts/` returns only `handoff-audit.sh`, `pf-attestation-audit.sh`, `scope-contract-audit.sh`). The doc handles this by marking each row Status `PROPOSED` and routing the resolution to §18 OQ-1. This is the QA-strict project-wide convention (PROPOSED is permitted to reference non-existent scripts). The finding flags it as Important rather than Critical because the convention IS documented at line 512 — but the cumulative effect is that 14+ rows in §13 are bookkeeping placeholders, and the deployment-time AC list (§15.2b) only mentions `AC-deploy-14. scripts/audit-reviewer-output.sh exists and is executable`. There is no per-row deployment AC checking each `--check <name>` sub-command exists.

**Evidence.** Lines 520-535 (§13 rows 1-15): every Mechanism cell ends with `(PROPOSED)`. Line 666 (§15.2b AC-deploy-14): "`scripts/audit-reviewer-output.sh` exists and is executable. `test -x ...`. Promotes 22 PROPOSED §13 rows toward LIVE on per-row smoke-test landing." `ls /Users/waltermcgivney/Documents/Projects/a-plus-maxing/scripts/` → only 3 audit scripts exist, none named `audit-reviewer-output.sh`.

**Adversarial probe.** R + D: the deployed reviewer reading its profile sees mechanical guards it can invoke. At first dispatch, every `--check` invocation fails because neither the script nor the sub-commands exist. AC-deploy-14 only checks the SCRIPT exists, not the sub-commands; a script with `audit-reviewer-output.sh` that prints "not implemented" and exits 1 satisfies `test -x` but breaks every §13 row that depends on it.

**Fix.** Add to §15.2b a per-sub-command existence AC, e.g., `AC-deploy-14a. scripts/audit-reviewer-output.sh --list-checks emits ≥22 sub-command names`. Alternatively, scope the §13 mechanism column entries with explicit `(SUB-COMMAND PROPOSED — see AC-deploy-14a)` so the script-exists guard separates from each sub-command. Accept-as-PROPOSED is also legitimate per Role 2 §18 OQ-7, but the cluster size (15+ row references to a single non-existent script) warrants explicit acknowledgment in the §13 preamble.

---

### F-015 — §5 rule 12 forbids inventing refusal classes but §5 rule 8 contradictions field permits open-ended axis enumeration

| Field | Value |
|---|---|
| **Category** | C — Internal Contradictions |
| **Severity** | Suggestion |
| **Section** | §5 rule 8 (G3); §5 rule 12 (G3); OQ-5 (G7) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §5 rule 12 declares the 8-class refusal taxonomy is the "canonical source of truth" and any need for a 9th class routes through AQ. §5 rule 8 requires `stratification_attempted` with `stratification_axes_tried: [...]` — open-ended axis enumeration. §18 OQ-5 acknowledges "axis-set (population × dose × outcome × timing) may be insufficient ... If stratification rate <50% on genuine contradictions, Role 3 surfaces `edge_case_class: stratification-axis-gap` finding; orchestrator extends the axis-set." The axis-set therefore can grow inline ("orchestrator extends") whereas the taxonomy cannot. This asymmetry is reasonable in principle (taxonomy is statutory-anchored, axes are calibration-derived) but is not stated anywhere in the doc — a fresh reviewer trying to add a 5th axis (e.g., `comorbidity`) does not know whether to inline-extend or to AQ-route.

**Evidence.** Line 164 (§5 rule 12): "If a coverage gap implies a 9th class is needed, dispatch an Architecture Question to Role 1 per Role 2 §6 step 2; do NOT add a class inline." Line 156 (§5 rule 8): "`stratification_axes_tried: [...]`" (no enumeration constraint). Line 783 (§18 OQ-5): "If stratification rate <50% on genuine contradictions, Role 3 surfaces `edge_case_class: stratification-axis-gap` finding; orchestrator extends the axis-set."

**Adversarial probe.** C + A: two adjacent fields (`edge_case_class` enum vs `stratification_axes_tried` list) have asymmetric extension rules but the asymmetry is undocumented in §5. A reviewer encountering a novel axis cannot derive the correct behavior from rules 8 + 12 alone.

**Fix.** Add a sentence to §5 rule 8: "Axes may be extended inline; novel axes are reported in §18 OQ-5 cadence, not blocked. Class identifiers (rule 12) are statutorily anchored and require AQ; axes are calibration-derived and extend by orchestrator decision."

---

### F-016 — §9.1 field 2 "Artifact paths" includes `<timestamp>` placeholder with undefined precision

| Field | Value |
|---|---|
| **Category** | A — Ambiguous Instructions |
| **Severity** | Suggestion |
| **Section** | §9.1 (G4) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §9.1 field 2 names the findings report path as `design/.health-edge-case-reviewer-design-work/reviews/<specialist-slug>-<timestamp>.md`. `<timestamp>` precision is undefined. §12.2 GOOD shows `cardiovascular-specialist-2026-05-27T1503.md` (minute precision, T-separator). A reviewer producing two reports in the same minute would collide. The convention also clashes with the standard ISO 8601 "T15:03:00" form.

**Evidence.** Line 252 (§9.1 field 2): "findings report at `design/.health-edge-case-reviewer-design-work/reviews/<specialist-slug>-<timestamp>.md`". Line 451 (§12.2 GOOD): "cardiovascular-specialist-2026-05-27T1503.md".

**Adversarial probe.** A: same-minute collisions or filesystem-incompatible characters (`:` on Windows-bridged filesystems). E: no instruction for handling collision.

**Fix.** Specify timestamp format in §9.1 field 2: `<specialist-slug>-YYYY-MM-DDTHHMMSS.md` (seconds precision, no colon). Add an explicit collision-handling instruction (e.g., append `-r2`, `-r3`).

---

### F-017 — §13 row 23 cites the existing hook but consequence claim "All Role-3 dispatches ... inline full 11-section profile verbatim" is unverified

| Field | Value |
|---|---|
| **Category** | D — Downstream Breakage |
| **Severity** | Suggestion |
| **Section** | §13 row 23 (G6) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §13 row 23 is the only REFERENCED row, citing `INV-ROLE-INLINING` enforced at `.claude/hooks/enforce-role-inlining.sh`. The hook does exist (verified). But the row claims the hook covers "all Role-3 dispatches (including Architecture Question dispatches, divergence-log re-tuning agents)". The hook's actual behavior (from `INVARIANTS.md` line 41) is to match dispatches by "`H1=# {Role Name}` or `roles/<slug>/agent.md` ref". An Architecture Question dispatched WITHOUT either of those triggers (e.g., a Task-tool call with prompt prefix "Resolve AQ-001") would not be caught by the hook. The row's coverage claim is broader than the hook's actual scope.

**Evidence.** Line 542 (§13 row 23): "All Role-3 dispatches (including Architecture Question dispatches, divergence-log re-tuning agents) inline full 11-section profile verbatim ... `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook". `INVARIANTS.md` line 41 INV-ROLE-INLINING property: "Agent dispatches matching role-context (`H1=# {Role Name}` or `roles/<slug>/agent.md` ref) inline the full 11-section profile verbatim."

**Adversarial probe.** D: a downstream consumer (orchestrator) reading row 23 believes the hook covers AQ dispatches. If AQ dispatches don't use the H1/roles-ref triggers, the inlining invariant is silently violated for that dispatch class.

**Fix.** Either (a) narrow the row 23 coverage claim to only dispatches matching the hook trigger pattern (and add a separate row covering AQ dispatch shape), or (b) extend the hook trigger pattern to catch AQ dispatches (out-of-scope for this doc; would route via INVARIANTS.md change-discipline ritual).

---

### F-018 — §16 candidate INV-COVERAGE-GAP-FINDING-SCHEMA promotion criteria require "≥1 specialist actually reviewed" but no specialist exists at Role 3 deployment

| Field | Value |
|---|---|
| **Category** | O — Ordering / Dependency Gaps |
| **Severity** | Suggestion |
| **Section** | §16 (G7) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §16 candidate INVs gate their promotion on "≥1 specialist actually reviewed". Per `templates/specialist-risk-class.yaml` and `vault/WIKI.md`, no specialist agent.md files have been authored yet (the 14-specialist roster is the downstream-of-this-design output of Role 2's later authoring waves). Role 3's first dispatch needs SOMETHING to review. The doc never names the order: does Role 2 author all 14 first, then Role 3 reviews all 14? Or does Role 2 author 1, then Role 3 reviews 1, then Role 2 authors 2, etc.? §17.2 A-2 says "Role 2 has executed at least one specialist before Role 3 first dispatch" — but the dispatch cadence ("one-then-review" vs "batch-then-review") is not stated.

**Evidence.** Line 693 (§16 INV-COVERAGE-GAP-FINDING-SCHEMA): "Promotion blocked on script existing AND ≥1 specialist actually reviewed (empirical schema calibration)." Line 720 (§17.2 A-2): "Role 2 design doc Final + Role 2 has executed at least one specialist before Role 3 first dispatch". Neither passage names the batch shape.

**Adversarial probe.** O: the candidate INV promotion path depends on the dispatch-cadence shape, but cadence is unspecified. If Role 2 batches all 14 before Role 3 sees any, calibration on 1 specialist is over-fit; if Role 3 sees 1-at-a-time, the candidate INV promotes too early.

**Fix.** Add to §16 candidate INV-COVERAGE-GAP-FINDING-SCHEMA: "Promotion threshold: review of N=3 specialists across ≥2 risk classes (per `templates/specialist-risk-class.yaml`) so the schema sees domain heterogeneity before promotion." Add to §17.2 A-2: "Dispatch cadence: orchestrator-determined; Role 3 calibration ACs assume ≥3 specialists across ≥2 risk classes before promotion of any candidate INV."

---

### F-019 — WITHDRAWN — `vault/library/_source-whitelist.md` verified to exist

| Field | Value |
|---|---|
| **Category** | R — Broken References (withdrawn) |
| **Severity** | n/a |
| **Section** | §10.1 item 12 (G4) |
| **Resolution** | Withdrawn — false positive |
| **Affected File** | n/a |

**Description.** Finding withdrawn after filesystem verification. `vault/library/_source-whitelist.md` exists. The §10.1 item 12 auto-load reference resolves cleanly. No defect.

**Verification.** `ls /Users/waltermcgivney/Documents/Projects/a-plus-maxing/vault/library/_source-whitelist.md` returns the file path. Auto-load discipline at §10.1 holds.

No action required.

---

### F-020 — §14 EC-5 cites `PF-S7-01` as a hypothetical "between authoring and Role 3 review" amendment, but the doc lists `last-PF-reviewed: PF-S6-01` — drift surface unstated

| Field | Value |
|---|---|
| **Category** | E — Edge Case Gaps |
| **Severity** | Suggestion |
| **Section** | §14 EC-5 (G7); frontmatter (G1) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** EC-5 names `PF-S7-01` as a hypothetical newer PF that the reviewer should detect. The frontmatter says `last-PF-reviewed: PF-S6-01`. Before the reviewer's deployment date, a new `PF-S<N>-NN` may already exist that the deployed profile doesn't know about. EC-5 specifies the detection path for amendment-AFTER-deployment but does not handle the case where a new PF lands BEFORE deployment but AFTER design-doc finalize (i.e., between Phase 5 close and `/upgrade-agent` Session B dispatch).

**Evidence.** Line 10 (frontmatter): "last-PF-reviewed: PF-S6-01". Lines 596-604 (EC-5): "Between authoring and Role 3 review, `memory/process-failures.md` gains `PF-S7-01` that supersedes the supplement-specialist's framing of PF-S2-04."

**Adversarial probe.** E: the window "design-doc finalize → /upgrade-agent dispatch" is not covered by EC-5's logic, which assumes the reviewer is already running.

**Fix.** Add an EC-5b or extend EC-5 to cover: "If `memory/process-failures.md` gains a new PF between this design doc's `last-PF-reviewed:` value and the Role 3 first dispatch, orchestrator re-routes design doc to Phase 5 amendment cycle (re-read PFs + re-pin `last-PF-reviewed:`) BEFORE `/upgrade-agent` Session B dispatches."

---

### F-021 — §17.1 Risk-5 cites "arXiv:2604.16790" as an external paper but substrate citation [38] format does not appear in design doc

| Field | Value |
|---|---|
| **Category** | L — Language Economy / Citation Hygiene |
| **Severity** | Suggestion |
| **Section** | §17.1 Risk-5 (G7) |
| **Resolution** | Accept (informational) |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §17.1 Risk-5 cites a paper directly by arXiv identifier ("Finding 6: Bias-in-the-Loop, arXiv:2604.16790"). The substrate's bibliography uses `[38]` reference notation. The design doc never establishes its own bibliography section; this is the only direct arXiv citation. Per Role 2 §13 row 8 + R8 of the substrate (citation discipline as 3-layer convergence), inline citations without locator anchors are exactly the surface PF-S2-02 catches. The citation IS verified (substrate L184 confirms the paper) but the inline form breaks the doc's own citation hygiene pattern.

**Evidence.** Line 711 (§17.1 Risk-5): "LLM-as-judge sensitivity to prompt design, surface-form bias (Finding 6: Bias-in-the-Loop, arXiv:2604.16790)". No bibliography section in design doc.

**Adversarial probe.** L: the inline citation costs ~6 tokens and adds a reference shape the rest of the doc doesn't use. A consistent doc cites `[Finding 6]` (the Pass-1 substrate Finding) without re-citing the underlying arXiv; the reviewer following Pass-1 anchor density (AC-10) treats `Finding 6` as sufficient.

**Fix.** Remove "arXiv:2604.16790" from line 711, keeping only "(Finding 6: Bias-in-the-Loop)". The Pass-1 substrate already carries the arXiv citation under `[38]`; the design doc does not need to duplicate.

---

### F-022 — §17.3 BC-2 cites a PF class identifier `AP-REVIEW-MISSED-COVERAGE` that does not exist in `memory/process-failures.md`

| Field | Value |
|---|---|
| **Category** | R — Broken References |
| **Severity** | Suggestion |
| **Section** | §17.3 BC-2 (G7) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** §17.3 BC-2 names a PF entry class `AP-REVIEW-MISSED-COVERAGE`. Anchor convention is `PF-S\d+-\d+` (per §5 rule 12 fabrication guard). `AP-REVIEW-*` is a different identifier shape — likely an anti-pattern class identifier projected forward, not an existing PF entry. The monitor script `scripts/pf-attestation-audit.sh extension parses PF log for AP-REVIEW-*` would never match because the PF identifier convention is `PF-S\d+-\d+`.

**Evidence.** Line 732 (§17.3 BC-2): "A deployed specialist (one Role 3 approved) is later found to have an uncovered refusal class via PF entry of class AP-REVIEW-MISSED-COVERAGE | `scripts/pf-attestation-audit.sh` extension parses PF log for `AP-REVIEW-*` and counts occurrences". `memory/process-failures.md` PF identifiers: `PF-S2-01`, `PF-S2-02`, ..., `PF-S6-01` — all use `PF-S<N>-<NN>` format.

**Adversarial probe.** R + A: `AP-REVIEW-*` is not a real grep target. The break condition can never fire as written.

**Fix.** Replace `AP-REVIEW-MISSED-COVERAGE` with a concrete future PF identifier convention. Suggested: "PF entry where the title contains `coverage gap missed by reviewer` or class tag `pf-class: review-missed-coverage`". Update the monitor script grep pattern accordingly.

---

### F-023 — §18 OQ-6 promises schema validation at "first Role 3 dispatch" but Phase 3 of /upgrade-agent runs before any specialist exists

| Field | Value |
|---|---|
| **Category** | O — Ordering / Dependency Gaps |
| **Severity** | Suggestion |
| **Section** | §18 OQ-6 (G7); §16 (G7) |
| **Resolution** | Prevent |
| **Affected File** | design/health-edge-case-reviewer-design.md |

**Description.** OQ-6 says the schema-vs-aplus-research-gate-JSON integration check happens at "First Role 3 dispatch + schema-validator authoring (row 1) at Session B". Session B is `/upgrade-agent` Phase 7 (per the project-local skill spec). But the reviewer's first dispatch must come AFTER Role 2 produces a specialist — which OQ-1 also blocks on script existence. The chain `OQ-1 → OQ-6 → row 1 LIVE` has at least three ordering constraints that are not made explicit anywhere.

**Evidence.** Line 791 (OQ-6): "First Role 3 dispatch + schema-validator authoring (row 1) at Session B surfaces integration gaps." Line 793 (OQ-6 blocker): "Non-blocking; blocks §13 row 1 LIVE; surfaces at first dispatch." Line 747 (OQ-1): "The 22 PROPOSED §13 rows all hinge on this script existing."

**Adversarial probe.** O: A "first Role 3 dispatch" needs (a) the agent profile deployed (Session B output), (b) a specialist to review (Role 2 wave output), (c) the audit script existing (OQ-1 resolution). Three sequential dependencies; OQ-6's resolution wording does not name them, so the orchestrator scheduling the integration test may try to run it before all three preconditions are met.

**Fix.** Add to OQ-6 the explicit dependency chain: "Resolution preconditions (sequential): (1) /upgrade-agent Session B produces .claude/agents/health-edge-case-reviewer/agent.md (AC-deploy-12); (2) scripts/audit-reviewer-output.sh exists (AC-deploy-14); (3) Role 2 has authored ≥1 specialist agent.md per §17.2 A-2."

---

## Coverage Matrix

Rows = sectional groups (§ ranges); columns = the 8 categories. Cells contain finding IDs that apply to that group + category, or `—` if no finding after honest probing. L applied as final sweep across all groups (per SKILL.md Step 3 final-sweep rule).

| Group | A | E | C | R | O | S | D | L |
|---|---|---|---|---|---|---|---|---|
| G1 §§1–2 Problem + Role Definition | — | — | F-006 (partial) | — | — | — | F-006 | — |
| G2 §§3–4 Pass-1 Digest + Cross-Role References | — | — | — | — | — | — | — | — |
| G3 §§5–7 Behavioral Rules + Ask-vs-Proceed + Loop-Breaking | F-011 | — | F-015 | — | — | — | — | — |
| G4 §§8–10 Tools + Communication + Context Loading | F-012, F-016 | — | — | F-005 | — | — | — | — |
| G5 §§11–12 Anti-Patterns + Negative Examples | F-007 | — | F-013 | — | — | — | F-006, F-007 | F-013 |
| G6 §13 Mechanical Enforcement Map | — | — | F-001, F-002, F-003, F-004, F-008, F-009 | F-014 | — | — | F-014, F-017 | — |
| G7 §§14–18 Edge Cases + ACs + Invariants + Risk + OQs + Appendix A | — | F-010, F-020 | — | F-022 | F-018, F-023 | — | — | F-021 |

**Coverage by category.**

- A (Ambiguous Instructions): F-007, F-011, F-012, F-016 (4 findings)
- E (Edge Case Gaps): F-010, F-020 (2 findings)
- C (Internal Contradictions): F-001, F-002, F-003, F-004, F-006, F-008, F-009, F-013, F-015 (9 findings — dominant category, cluster around §11.1↔§13 row-number drift)
- R (Broken References): F-005, F-014, F-022 (3 findings; F-019 withdrawn after filesystem verification)
- O (Ordering/Dependency Gaps): F-018, F-023 (2 findings)
- S (Scope Violations): 0 findings after honest probing. The doc's scope is well-bounded — §2.2 "I do NOT own" is exhaustive against Role 1 / Role 2 / Role 4 / Role 7; §8.3 explicitly forbids cross-role Edit; §16 explicitly excludes Research-domain INV-*. No scope creep into adjacent roles surfaced.
- D (Downstream Breakage): F-006, F-007, F-014, F-017 (4 findings — concentrated in §13 row → audit-script consumer chain)
- L (Language Economy): F-013, F-021 (2 findings; the doc is dense but most density is load-bearing per the fresh-agent test)

**Coverage check (per SKILL.md §Coverage Check).**

- [x] Minimum 2 findings per category OR documented honest probing (S has 0 after probing — documented)
- [x] Every procedure probed with A + O (§5 rules, §6 decision tree, §8 tool palette, §13 audit invocations)
- [x] Every cross-reference probed with R (filesystem-verified against scripts/, templates/, .claude/hooks/, vault/, design/, INVARIANTS.md, memory/, skills_library/)
- [x] Every section boundary probed with S
- [x] Every stated count probed with C (8 PFs ✓, 9 Findings ✓, 15 R's ✓, 7 APs ✓, 23 §13 rows ✓, 18 sections ✓, but §11.1 row pointers drift — F-001..F-004)
- [x] Every procedure's error/empty/boundary paths probed with E
- [x] Every output-format section probed with D (§9 communication, §13 schema, §12 examples)
- [x] Language economy (L) pass on all sections
- [x] Each finding has severity + resolution
- [x] Coverage matrix cells filled with finding IDs or "—"

**Verdict (per SKILL.md Step 4 calibration anchors).**

- 0 Critical-by-severity-alone (downstream consumer breaks with no recovery) in isolation, BUT the F-001..F-004 cluster (four §11.1 row-pointer errors) jointly degrades the PF-coverage table to the point that 4 of 8 PFs reference the wrong mechanical guard. A reviewer following §11.1 cannot trust the guard pointers and must re-verify every row reference against §13 — exactly the rubber-stamp surface the doc is designed to prevent. The cluster is Critical at the aggregate level even if each individual finding is "row number mismatch".
- F-005, F-006, F-008, F-009, F-011, F-014 are Important — each degrades audit-script behavior or schema-fitness without halting the pipeline outright.
- Remaining 12 findings (F-007, F-010, F-012, F-013, F-015 through F-018, F-020 through F-023) are Suggestion-tier: language-economy, narrative bleed from Phase-1, or downstream-precondition gaps that surface only at first dispatch.

**Aggregate disposition.** The doc is structurally sound at the §1-§10 level (Problem, Role Definition, Pass-1 Digest, Cross-Role References, Behavioral Rules, Ask-vs-Proceed, Loop-Breaking, Tools, Communication, Context Loading). The mechanical-enforcement layer (§11.1 ↔ §13) carries a row-numbering drift cluster (F-001..F-004) that synthesis appears to have introduced when §13 was consolidated from 44 drafter rows to 23. Phase 4 verification should re-run a §11.1-vs-§13 cross-reference audit before Phase 5 finalize.

**Notes for Phase 4 / Phase 5.**

- F-001 through F-004 cluster: investigate whether §11.1 was authored against an earlier §13 row numbering. If so, the fix is mechanical (replace 4 row numbers) but the LEGITIMATE-MODIFIED classification applies per Role 1's red-team disposition pattern.
- F-005 (AGENT_TEMPLATE.md path): if Role 1 and Role 2 design docs share the defect, escalate via AQ rather than inline-fix.
- F-019 withdrawn after live filesystem verification (`vault/library/_source-whitelist.md` exists).
- F-007 (BAD-block imperative bleed): consider mirroring Role 2 §5 rule 4's design-vs-deployed grep scoping.
- S category zero findings: documented honest probing of §2.2 ownership boundaries against Role 1 / Role 2 / Role 4 / Role 7 yielded no overreach. The doc is unusually scope-disciplined.

— end —
