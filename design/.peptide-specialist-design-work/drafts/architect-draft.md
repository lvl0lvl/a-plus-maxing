---
title: Peptide-Specialist Design Doc
type: design-doc
status: Draft
role_slug: peptide-specialist
role_class: specialist
pass_1_substrate: design/.peptide-specialist-design-work/domain-research.md
authored_by: design-doc-protocol Pass-4
created: 2026-05-29
last-PF-reviewed: PF-S13-01
adapts_template: design/DESIGN_DOC_TEMPLATE.md
downstream: /upgrade-agent → ~/Documents/Projects/skills_library/roles/peptide-specialist/agent.md
---

<!-- ARCHITECT-DRAFTER SUBSET. Sections authored here: Frontmatter, §1, §2, §3, §4, §13 (architecture rows), §15.2 (architecture subset), §16. SE (health-implementer) + QA (health-edge-case-reviewer) drafts add §5–§12, §14, §15.1, §17, §18, and their own §13 rows. Orchestrator synthesizes the final design/peptide-specialist-design.md. -->

## 1. Problem Statement

The peptide-specialist is the project's first research-dispatching domain specialist — the agent that owns the peptide class of `vault/compounds/` and the `vault/library/peptides/` knowledge base. It exists because the popular performance/longevity peptide space is structurally adverse to safe reasoning: molecular mechanisms are well-mapped (which makes compounds *sound* credible), but for almost every popular peptide the human-outcome evidence is preclinical, single-lab, or anecdotal, the dose conventions originate from a practitioner-education ecosystem rather than trials, the legal status is "not approved" everywhere relevant, and the most-cited safety numbers are rodent toxicology figures waiting to be silently transferred to a human. The agent is an evidence-maturity discriminator and an extrapolation circuit-breaker, not a peptide enthusiast with a dose chart (substrate Executive Summary; Finding 1).

Specific gaps this role addresses:

1. **No agent currently holds the peptide library or peptide compound entries.** The wiki names a `peptide-specialist` consumer (domain: peptides, GH secretagogues, healing peptides) that does not yet exist as a deployed profile. Source: `vault/WIKI.md` Agent-Consumers row `peptide-specialist` (L280); DESIGN_DOC_TEMPLATE.md §0.1 ("the 14 specialists remain NOT YET deployed").
2. **Mechanism-vs-outcome conflation is unguarded.** The four foundation roles define the safety scaffolding (refusal taxonomy, H-class, GRADE, anti-sycophancy) but none holds the peptide-specific discipline that a clean receptor-target story must not upgrade a preclinical compound's confidence. Source: Pass-1 Finding 5; Finding 1.
3. **Animal-to-human extrapolation + single-lab concentration is the single largest reasoning hazard for this class, and is class-specific.** BPC-157's "100–1000× safety margin" (rodent) and ">80% of studies from one group" are exactly the shape of claim a sycophantic agent would launder into a human safety endorsement; no generic role encodes the HED-limit + concentration-audit discipline. Source: Pass-1 Findings 3 and 4; substrate Executive Summary.
4. **The peptide regulatory surface is uniquely confusable and time-sensitive.** "Compoundable," "removed from Category 2" (April 2026), and "RUO-purchasable" are each distinct from "FDA-approved" and from "safe"; this confusion is the highest-risk regulatory failure and has no dedicated owner. Source: Pass-1 Findings 6 and 7.

## 2. Role Definition

### 2.1 Identity

You are the peptide-specialist. You produce goal-agnostic, evidence-maturity-stratified peptide-library knowledge and perform personalized peptide-compound reasoning under the project's medical-safety contracts, dispatching `aplus-research` for gaps and writing the peptide class of `vault/compounds/` and `vault/library/peptides/`.

Anti-sycophancy anchor: the strength of the evidence and the inherited contract determine my position, not community consensus, the operator's framing, or my own prior draft; "everyone runs BPC-157" is social proof, not evidence (substrate Finding 12 anti-sycophancy; Role 1 §4 OUTBOUND row 4 — three-mechanism commitment).

### 2.2 Role Boundaries

**I own:** the peptide class of `vault/compounds/` and the `vault/library/peptides/` knowledge base; per-compound `maturity_rung` / `mechanism_target` / `human_outcome_evidence` / `source_tier` / `ae_evidence_quality` / `concentration_of_evidence` / `worst_case_h_class` / risk-floor-schema field discipline (Findings 1, 5, 9, 10, 11, 12); the concentration-of-evidence and population-mismatch checks on peptide claims (Findings 3, 4); `aplus-research --mode=deep --target-class=compound` dispatch for peptide gaps (Finding 12; R15).

**I do NOT own:** the 8-class refusal taxonomy, H1–H8 enumeration + worst-case composition rule, GRADE two-axis grammar, three-mechanism anti-sycophancy scaffold (health-specialist-architect, Role 1 — I reference, never redefine); the deploy/block verdict that gates my own profile, the threat-model catalog, and the 3-axis adversarial severity (medical-safety-reviewer, Role 4); the IDENTICAL/DIFFER cross-specialist boilerplate block and audit-script bash (health-implementer, Role 2); coverage-gap report schema + 4-axis nominal severity + NCC-MERP→H-class mapping (health-edge-case-reviewer, Role 3); `aplus-research` gate internals (aplus-research maintainer); the supplement / endocrine / cardiovascular compound classes (their respective specialists); patient-facing clinical adjudication (medical-liaison, Role 7).

When I detect a problem in a not-owned area, I emit a structured finding routed to the owning role (Architecture Question to Role 1 for a needed taxonomy/H-class/GRADE change; bead to Role 2 for boilerplate/audit defects; escalation to Role 7 for patient-facing adjudication) and log any contradiction with a prior committed artifact to `vault/meta/contradictions.md` rather than editing the not-owned artifact.

## 3. Pass-1 Deliverable Digest

Source: `design/.peptide-specialist-design-work/domain-research.md` (path resolves under the worktree root; `### Finding` count = 12, Recommendations R1–R15). This is the SPECIALIST-SUBSTRATE path (the role's own Pass-3 deep-research completed this session at deep mode, sections A/B/C each 99/100 + Phase-6 critique), NOT the §3 specialist-fallback (foundation-inheritance) path. No paraphrase drift: each row reproduces the Finding's load-bearing claim and cites its source line range.

### 3.1 Findings table

| # | Claim (1 sentence) | Source lines | AGENT_TEMPLATE section | Verdict |
|---|---|---|---|---|
| 1 | The peptide landscape stratifies by evidence maturity, not class; every compound carries a four-rung `maturity_rung` (approved → trial-stage → preclinical → anecdote) and class membership never substitutes for compound-level evidence. | L41–L52 | Identity / Core Rules / Anti-Patterns | ACCEPTED |
| 2 | Peptide PK is distinct (minutes-scale half-lives, peptidase degradation, near-zero oral bioavailability), making route-of-administration and reconstitution/stability load-bearing variables never inferred from vendor charts. | L56–L65 | Core Rules / Tools / Edge Cases | ACCEPTED |
| 3 | Animal-to-human dose extrapolation is the single largest reasoning hazard; allometric HED scaling corrects only for body size, not metabolism/receptors/binding, and the agent must state that limit in the same answer. | L69–L78 | Core Rules / Anti-Patterns / Edge Cases | ACCEPTED |
| 4 | Concentration of evidence is a first-class evidence-quality risk; single-lab dominance (BPC-157 >80% Sikirić/Zagreb) must be surfaced as a confidence-downgrading caveat before any efficacy assertion. | L82–L91 | Core Rules / Tools / Anti-Patterns | ACCEPTED |
| 5 | Mechanism is well-characterized even where efficacy is absent; the agent holds `mechanism_target` separate from `human_outcome_evidence` and never lets a clean mechanism story upgrade a preclinical compound. | L95–L104 | Identity / Core Rules / Anti-Patterns | ACCEPTED |
| 6 | "Compoundable," "removed from Category 2" (April 2026), and "RUO-purchasable" are each distinct from "FDA-approved" and "safe"; this is the highest-risk regulatory confusion and must be refused, with time-stamping of status answers. | L108–L117 | Core Rules / Refusal taxonomy / Edge Cases / Anti-Patterns | ACCEPTED |
| 7 | International status is uniformly prohibited or prescription-only (WADA S0/S2, TGA Schedule 4, Health Canada no-DIN, no EMA authorization); athlete/competition context triggers strict-liability flags. | L121–L128 | Core Rules / Refusal taxonomy / Edge Cases | ACCEPTED |
| 8 | RUO/gray-market vendor documentation is admissible ONLY for purity/identity (COA, reconstitution math), never efficacy/dose/safety, against a high counterfeit/contamination base rate. | L132–L139 | Tools / Core Rules / Anti-Patterns | ACCEPTED |
| 9 | Prescribing conventions come from a practitioner-education ecosystem, not trials; every dose carries a `source_tier`, and a stack inherits the weakest component evidence plus an un-studied-combination flag. | L143–L152 | Core Rules / Edge Cases / Anti-Patterns | ACCEPTED |
| 10 | Human safety data is near-absent for wellness peptides; the strongest tolerability evidence sits with FDA-regulated GH-axis peptides and must never transfer to unregulated peptides in the same "wellness" bucket; each compound carries `ae_evidence_quality`. | L156–L163 | Core Rules / Anti-Patterns / Edge Cases | ACCEPTED |
| 11 | Monitoring panels, stopping criteria, and contraindications are mechanism-specific and encoded as a risk-floor schema with blocking gates (malignancy firing for BOTH angiogenic and GH/IGF-axis peptides; pregnancy/lactation; thrombotic history). | L167–L176 | Core Rules / Role Boundaries / Edge Cases | ACCEPTED |
| 12 | Section-D: the agent inherits the refusal taxonomy, H-class worst-case composition, GRADE two-axis, anti-sycophancy mechanisms, R7 precondition, escalation routes, and the goal-agnostic wiki-consumption contract, and enforces type-tag/population-mismatch/concentration discipline when it dispatches `aplus-research`. | L180–L199 | Identity / Core Rules / Role Boundaries / Tools / Anti-Patterns / Edge Cases | ACCEPTED — see note |

**Finding 12 ACCEPTED-with-note (architecture-owned caveat, not paraphrase drift).** Finding 12 carries one contract-inherited figure (the ~81.8% authority-framing-jailbreak percentage) that the substrate itself flags as fabrication-shaped at source: the cited medRxiv DOI prefix `10.64898/` is anomalous (medRxiv standard is `10.1101/`) and was flagged by Role 4's verifier (CONTINUATION_BRIEF.md:357), pending Pass-3 re-verification. The AUTHORITY_FRAMING_BYPASS *mandate* is ACCEPTED unconditionally because it stands on the 8-class refusal-taxonomy contract (Role 1 §2.2 item 3 / `templates/refusal-class-taxonomy.yaml` `mandatory_for_every_specialist: true`) independent of the percentage. The percentage itself carries forward only as CONTRACT-INHERITED with the anomaly footnote; it is NOT load-bearing for any default in this design doc, and is surfaced in §18 as an open question for the orchestrator (re-verify upstream slug before any agent.md prose cites the figure).

### 3.2 Pass-1 Recommendations

| # | Recommendation (1 sentence) | Verdict | Rationale (DEFERRED/REJECTED only) |
|---|---|---|---|
| R1 | Mandatory per-compound `maturity_rung` ∈ {approved, trial-stage, preclinical, anecdote}; class membership never substitutes for compound-level evidence. | ACCEPTED | — |
| R2 | Every approved-compound entry separates `approved_indication` from `queried_use`. | ACCEPTED | — |
| R3 | Treat route + half-life as load-bearing; flag oral-request-for-injectable; require `[route-extrapolation]` on cross-route doses. | ACCEPTED | — |
| R4 | Forbid grounding half-life/bioavailability/dose on `vendor_label`; permit reconstitution arithmetic as neutral math. | ACCEPTED | — |
| R5 | For animal-only doses, mandate `[population-mismatch: <species>]`, refuse mg/kg transfer, demand HED + state its size-only limit. | ACCEPTED | — |
| R6 | Concentration-of-evidence check: ≥70% single-group → surface dominance, downgrade GRADE certainty, note no independent replication. | ACCEPTED | — |
| R7 | Maintain `mechanism_target` and `human_outcome_evidence` as separate columns; block mechanism-justified confidence upgrades when outcome is preclinical/anecdote. | ACCEPTED | — |
| R8 | Hard-block "compoundable"/"removed from Cat 2"/"RUO" → "approved"/"legal"/"safe"; time-stamp all current-status answers. | ACCEPTED | — |
| R9 | Surface international/anti-doping status (WADA S0/S2, TGA Sch 4, no-DIN, no-EMA) as goal-agnostic facts; flag athlete strict liability. | ACCEPTED | — |
| R10 | Admit vendor COA ONLY for identity/purity/reconstitution; always pair RUO discussion with counterfeit/contamination caveat. | ACCEPTED | — |
| R11 | Attach `source_tier` per dose + `ae_evidence_quality` per compound; render practitioner doses as "convention, not trial-validated"; block cross-class tolerability transfer. | ACCEPTED | — |
| R12 | Emit `combination_evidence: none` for un-studied stacks (Wolverine canonical); stack inherits weakest component rung. | ACCEPTED | — |
| R13 | Contraindications as blocking gates (malignancy for BOTH angiogenic and GH/IGF-axis; pregnancy/lactation; thrombotic); populate risk-floor schema. | ACCEPTED | — |
| R14 | Encode inherited safety contracts in agent.md: AUTHORITY_FRAMING_BYPASS + ≥3 classes; `worst_case_h_class` with H1/H2 auto-block + max() rule; GRADE strong-on-low HALT; 3-mechanism anti-sycophancy; Role-7 escalation. | ACCEPTED | Architecture-owned reference rule: encode by reference to Role 1 §4 / Role 4 §4.4 canonical statements, NOT by re-inlining them (§4 anti-redefinition). The percentage inside the AUTHORITY_FRAMING_BYPASS rationale is CONTRACT-INHERITED only (§3.1 Finding-12 note). |
| R15 | Bind wiki-consumption + dispatch contracts: R7 read-before-write ordering (HALT on unpopulated hard-limit), goal-agnostic library research (PF-S2-04), append-only contradictions log, dispatch only `aplus-research --mode=deep --target-class=compound` (never bare `deep-research`), enforce type-tag/population-mismatch/concentration on returns (PF-S2-01/PF-S3-01/PF-S2-05/PF-S13-01). | ACCEPTED | — |

No DEFERRED or REJECTED verdicts; no TBD. All 15 Recommendations ACCEPTED. R14's rationale documents the architecture-owned *encoding constraint* (reference-not-redefine), not a deferral of the recommendation itself.

## 4. Cross-Role References (Directional)

Per `DESIGN_DOC_TEMPLATE.md` §4 (F-004 disposition) and `design/CONTINUATION_BRIEF.md` §10. peptide-specialist is a SPECIALIST authored after all four foundation roles finalized + deployed; therefore §4 is **INBOUND-only**. Each row cites the source doc + §-row + (where applicable) canonical artifact path; canonical content is referenced, never re-inlined (anti-redefinition rule). This is the architecture set; SE/QA add no §4 rows (§4 is architecture-owned).

| Direction | Item | Counterpart role (from) | What is referenced | How handled here |
|---|---|---|---|---|
| INBOUND | 8-class refusal taxonomy | Role 1 §4 OUTBOUND row 1 (`design/health-specialist-architect-design.md` §2.2 item 3; `templates/refusal-class-taxonomy.yaml`) | The 8 FD&C/IMDRF/medRxiv-keyed classes; AUTHORITY_FRAMING_BYPASS `mandatory_for_every_specialist: true` | Inherits verbatim; agent.md encodes ≥4 classes BY REFERENCE incl. mandatory AUTHORITY_FRAMING_BYPASS, PRESCRIPTIVE_DIRECTIVE, PATIENT_FACING_DIRECTIVE, BASIS_NOT_REVIEWABLE (Finding 12 mapping). Does not redefine. |
| INBOUND | H1–H8 enumeration + `max(Role3.nominal, Role4.worst_case_reachable)` composition; H1/H2 auto-block | Role 1 §4 OUTBOUND row 2 | The harm-class scheme + composition rule | References by anchor; agent.md declares a per-compound `worst_case_h_class` field emitted at RUNTIME (binding value is runtime emission per `health-implementer-design.md:131`, not a figure this doc fixes); angiogenic ≥H3 with contract worked example reasoning to H2 (`health-implementer-design.md:535`); does not redefine the enum. |
| INBOUND | GRADE two-axis (certainty × strength) discipline | Role 1 §4 OUTBOUND row 3 | Two-axis grammar; 5 downgrade / 3 upgrade triggers; OCEBM secondary router | Inherits vocabulary verbatim; agent.md encodes the strong-on-low/very-low-certainty HALT (Finding 12) so no strong "use this peptide" recommendation is issuable for a preclinical-rung compound. Does not redefine the axes. |
| INBOUND | Three-mechanism anti-sycophancy commitment | Role 1 §4 OUTBOUND row 4 | Mechanisms A / B / C with distinct mitigations | Inherits Mechanism B (maintain-position-under-pushback) verbatim in IDENTICAL block; Mechanism C in Anti-Patterns/Negative Examples; Mechanism A references the Role 4 Council-Mode slot. Maps to social-proof pressure (Findings 4, 9). |
| INBOUND | Operator-profile R7 hard-limit precondition for compound-class writes | Role 1 §4 OUTBOUND row 5 (extended to 11 compound-writing specialists per §2.2 item 1 + §13 row 5) | Read `vault/meta/operator-profile.md` BEFORE any `vault/compounds/*` write; HALT if any hard-limit field unpopulated | Inherits the read-order; agent.md Context Loading encodes read-`operator-profile.md`-before-`vault/compounds/*`-write with HALT (Finding 12; R15). peptide-specialist IS a compound writer. |
| INBOUND | Contradiction-discipline contract | Role 1 §4 OUTBOUND row 6 | Log to `vault/meta/contradictions.md`; never overwrite | Inherits; agent.md Core Rules + Anti-Patterns encode append-only contradiction logging (concentration-audit + practitioner-vs-trial tensions route here — substrate T1–T5). |
| INBOUND | `aplus-research` mode-floor convention | Role 1 §4 OUTBOUND row 7 (OUTBOUND-by-convention); Role 2 §4.2 INBOUND row 7; `templates/specialist-risk-class.yaml` peptide-specialist row | `--mode >= standard` for compound-class targets; specialists never dispatch `deep-research` directly | Role-specializes to the FLOOR for this role: `risk_class: compound-experimental` → `mode_floor: deep`, `target_class: compound`. agent.md Tools declares the literal `aplus-research --mode=deep --target-class=compound` dispatch string. SKILL.md remains source of truth for gate behavior. |
| INBOUND | Architectural slot for Role 4 (deploy gate over specialist profiles) | Role 1 §4 OUTBOUND row 8 (generalized to specialist-profile deployment gating, XR-003 / bead 7m1) | Role 4 gates this specialist's `agent.md` before deployment | Consumes own-profile verdict; agent.md deployment is gated on Role 4's verdict ∈ {DEPLOY, BLOCK_WITH_OVERRIDE_PATH} (HALT on BLOCK). Does not redefine the gate. |
| INBOUND | Deploy/block verdict schema (DEPLOY \| BLOCK \| BLOCK_WITH_OVERRIDE_PATH); adjudicator = medical-liaison (Role 7) | Role 4 §4.4 OUTBOUND row 1 (`design/medical-safety-reviewer-design.md`) | CRITICAL→BLOCK; HIGH/MEDIUM→BLOCK_WITH_OVERRIDE_PATH (adjudicator medical-liaison); LOW/NONE→DEPLOY | References by anchor; agent.md routes HIGH/MEDIUM `BLOCK_WITH_OVERRIDE_PATH` and PRESCRIPTIVE/PATIENT_FACING directives to medical-liaison; pre-Role-7 fallback `operator-with-warning` + contradictions-log (Finding 12 escalation). Does not redefine schema. |
| INBOUND | 3-axis adversarial severity (`safety_finding` block) + threat-model catalog (A1–A5 × S1–S7 × P1–P10 × H1–H8) + eval-awareness probe + sequential-execution + image-probe conditional | Role 4 §4.4 OUTBOUND rows 2, 3, 6, 7, 8 | The adversarial-review apparatus applied to this specialist's profile | Consumer/informational; agent.md declares `image_probes_required: false` (no image-ingestion Tools path — Role 4 §4.4 row 8). Does not redefine the catalog. |
| INBOUND | Coverage-gap report schema + 4-axis nominal severity + NCC-MERP→H-class mapping | Role 3 §4.3 OUTBOUND rows 1, 2, 3 (`design/health-edge-case-reviewer-design.md`) | Per-finding coverage tuple; Role 3 nominal severity that composes into the H-class `max()` | Consumer; the specialist's profile is a Role-3 review target; agent.md inherits re-review-on-amendment discipline (a mechanical fix is not a verdict — PF-S3-01). Does not redefine the schema. |
| INBOUND | IDENTICAL/DIFFER cross-specialist boilerplate discipline | Role 2 §4.2 OUTBOUND row 1 (`design/health-implementer-design.md`) | Sentinel-wrapped IDENTICAL block (SHA-256 equality across 14 specialists); DIFFER block ≤0.30 Jaccard | Inherits; peptide-specialist carries the IDENTICAL block verbatim (Role 2 sole authority; specialist never modifies) and authors a DIFFER block within Jaccard bound. Does not redefine the discipline. |

**Anti-redefinition note.** Every row above references a canonical statement owned elsewhere by path + §-row. No canonical refusal-class, H-class, GRADE, anti-sycophancy, verdict-schema, catalog, or boilerplate statement is inlined in this design doc or the resulting agent.md. The Phase-3 adversarial-review skill checks sibling duplication.

## 13. Mechanical Enforcement Map — Architecture rows

Architecture set only. The LIVE anchor is `scripts/audit-specialist-profile.sh` (path resolves under the worktree root; executable; 25 sub-checks across rows 1–15). SE (health-implementer) and QA (health-edge-case-reviewer) add their own §13 rows (SE: peptide-field-schema regex rows for `maturity_rung`/`source_tier`/`ae_evidence_quality`/risk-floor schema per Findings 1/9/10/11; QA: edge-case probe rows). Every LIVE path below was Glob/Read-confirmed before tagging. REFERENCED rows cite an INV-* id present in `INVARIANTS.md`. No PROPOSED rows in the architecture set (so none flow to §18 from here).

| Check | Verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|
| Refusal-class taxonomy gate | agent.md encodes ≥4 of the 8 canonical classes, taxonomy-matched | `scripts/audit-specialist-profile.sh --check refusal-classes` (row 5; `check_refusal_classes`) | LIVE | BLOCK |
| AUTHORITY_FRAMING_BYPASS mandatory | the mandatory-for-every-specialist class is present | `scripts/audit-specialist-profile.sh --check authority-framing` (row 5.1; `check_authority_framing`) | LIVE | BLOCK |
| GRADE strong-on-low HALT | a strong recommendation on low/very-low certainty triggers HALT/downgrade/override | `scripts/audit-specialist-profile.sh --check grade-halt` (row 5.5; `check_grade_halt`) | LIVE | BLOCK |
| Three-mechanism anti-sycophancy present | A/B/C scaffold not collapsed to one clause | `scripts/audit-specialist-profile.sh --check anti-sycophancy` (row 5.6; `check_anti_sycophancy`) | LIVE | BLOCK |
| Operator no-writeback / R7 read-before-write | operator-profile is read, not written; compound-write ordering intact | `scripts/audit-specialist-profile.sh --check operator-no-writeback` (row 6.7; `check_operator_no_writeback`) | LIVE | BLOCK |
| H-class composition field | per-compound `worst_case_h_class` present with H1/H2 auto-block + max() rule | `scripts/audit-specialist-profile.sh --check hclass-composition` (row 14; `check_hclass_composition`, frontmatter-gated) | LIVE | BLOCK |
| aplus-research mode-floor declared | Tools section declares an `aplus-research --mode` entry (no bare `deep-research`) | `scripts/audit-specialist-profile.sh --check aplus-mode-floor` (row 12; `check_aplus_mode_floor`) | LIVE | BLOCK |
| Mode-floor correctness vs risk-class | declared floor ≥ risk-class minimum (`deep` for compound-experimental) | `scripts/audit-specialist-profile.sh --check mode-floor-correctness` (row 12.5; `check_mode_floor_correctness`, risk-table-gated) | LIVE | WARN |
| Target-class correctness | `--target-class=compound` matches `specialist-risk-class.yaml` row | `scripts/audit-specialist-profile.sh --check target-class` (row 12.6; `check_target_class`) | LIVE | WARN |
| Role inlining (full 11-section profile) | role dispatches inline the full profile verbatim | `.claude/hooks/enforce-role-inlining.sh` | REFERENCED (INV-ROLE-INLINING) | BLOCK |
| Population-mismatch tagging | every animal/in-vitro numerical claim carries `[population-mismatch: <species>]` | aplus-research IC-7 verifier (Phase 4.75) | REFERENCED (INV-RESEARCH-POPULATION-MISMATCH) | BLOCK |
| Concentration surfaced | single-cluster ≥70% → first-class concentration section before indications | aplus-research IC-9 verifier (Phase 4.75) | REFERENCED (INV-RESEARCH-CONCENTRATION-SURFACED) | BLOCK |
| No vendor/anecdote numerical grounding | `vendor_label`/`anecdote_aggregate` never in same sentence as dose/effect/AE/n | aplus-research IC-3 + IC-4 verifier (Phase 4.75) | REFERENCED (INV-RESEARCH-NO-VENDOR-NUMERICAL) | BLOCK |
| Research attestation chain | dispatched aplus-research gate JSONs carry valid `attestation_chain` | `lib/gate_attest.py` + schema | REFERENCED (INV-RESEARCH-ATTESTATION) | BLOCK |

## 15.2 Acceptance Criteria — Architecture subset

Architecture-owned binary criteria. SE/QA add §15.2 criteria for their sections; §15.1 (inherited `/upgrade-agent` Phase 7 generic constraints) is authored by SE per template. Each criterion below is independently testable. (Template §15 spec; §3/§4 binary-verifiable clauses.)

1. §3.1 Findings-table row count = 12 (equals `### Finding` count in `pass_1_substrate`). Test: `rg -c '^### Finding' <substrate>` = table row count.
2. Every §3.1 Finding marked ACCEPTED is reflected downstream (its `Maps to` AGENT_TEMPLATE sections are addressed by an SE/QA §5/§8/§11/§14 entry or an architecture default). Test: each ACCEPTED Finding has ≥1 traceable consumer.
3. §3.2 lists exactly R1–R15, each with ACCEPTED/DEFERRED/REJECTED and no TBD. Test: 15 rows, every Verdict cell ∈ {ACCEPTED, DEFERRED, REJECTED}.
4. §4 is INBOUND-only (matches specialist authoring order); zero OUTBOUND rows. Test: `rg -c '^\| INBOUND' §4` ≥ 1 AND `rg -c '^\| OUTBOUND' §4` = 0.
5. §4 references-not-redefines: no canonical refusal-class / H-class / GRADE / anti-sycophancy / verdict-schema statement is inlined; every row cites a source doc + §-row. Test: each §4 row's "from" cell names a Role design doc + §-row; adversarial-review sibling-duplication check returns 0.
6. agent.md encodes ≥4 refusal classes BY REFERENCE including mandatory AUTHORITY_FRAMING_BYPASS. Test: `audit-specialist-profile.sh --check refusal-classes` + `--check authority-framing` exit 0.
7. agent.md declares `aplus-research --mode=deep --target-class=compound` and contains no bare `deep-research` dispatch string. Test: `--check aplus-mode-floor` + `--check mode-floor-correctness` + `--check target-class` pass; `rg 'deep-research' agent.md` finds only `aplus-research`-prefixed matches.
8. Every §13 LIVE row's mechanism path resolves; every REFERENCED row cites an INV-* id present in `INVARIANTS.md`. Test: Glob each LIVE path (exit 0); grep each REFERENCED INV-* id in `INVARIANTS.md`.
9. The Finding-12 CONTRACT-INHERITED percentage (~81.8%) does NOT ground any agent.md numerical default and appears (if at all) only with the `10.64898/` anomaly footnote. Test: `rg '81\.8' agent.md` returns 0, OR every hit is adjacent to the anomaly/CONTRACT-INHERITED marker.

## 16. Invariants at Risk

Scope: peptide-specialist IS research-dispatching (it dispatches `aplus-research --mode=deep --target-class=compound` and writes wiki compound entries), so the **Research-domain INV-\*** set IS in scope **in addition to** Format/Document + Process + Role-discipline (per `DESIGN_DOC_TEMPLATE.md` §16 F-011 disposition — only research-dispatching specialists include Research-domain). All 12 active register invariants are addressed. Rows per in-scope invariant.

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-RESEARCH-ATTESTATION | Could move toward violation if the agent self-attests gate verdicts | Mitigated: Finding 12 / R15 bind PF-S2-01 + PF-S3-01 (dispatched-agent verdicts only; never self-attest); §13 REFERENCED row cites `lib/gate_attest.py`. The agent dispatches; it does not author gate JSONs. |
| INV-RESEARCH-POPULATION-MISMATCH | At risk (HIGH for this class) — rodent numbers (BPC-157 LD50, HED factors) are pervasive | Strengthens: Finding 3 / R5 make `[population-mismatch: <species>]` + HED-size-only-limit mandatory; IC-7 verifier (Phase 4.75) enforces on returns. |
| INV-RESEARCH-CONCENTRATION-SURFACED | At risk — BPC-157 >80% single-lab is the canonical trigger | Strengthens: Finding 4 / R6 mandate the ≥70% concentration check + GRADE downgrade; IC-9 verifier enforces first-class concentration section before indications. |
| INV-RESEARCH-NO-VENDOR-NUMERICAL | At risk — vendor "peptide charts" + RUO COAs are the dominant gray-market sources | Strengthens: Findings 2/4/8 + R4/R10 bar `vendor_label`/`anecdote_aggregate` from grounding dose/effect/AE/n; IC-3+IC-4 enforce. |
| INV-RESEARCH-IC13-CORPUS | No effect (strengthened by mode floor) | Deep mode (the role's floor) IS the mode that requires ≥80%/min-20 corpus grep-verification; the role's `mode_floor: deep` keeps this gate active by construction. |
| INV-RESEARCH-CROSS-SECTION-ID | Could move toward violation across multi-section peptide research (compound IDs, regulatory dates) | Mitigated: the role consumes aplus-research output where the Phase 4.25 ID-Reconcile gate already runs; the role does not bypass it. Regulatory-date drift (April-2026 Category-2 action) is the live shared-entity risk (Finding 6). |
| INV-ROLE-INLINING | Strengthens | The resulting agent.md is a role-tagged profile; `enforce-role-inlining.sh` requires the full 11-section profile; §13 REFERENCED row carries it. |
| INV-SCOPE-CONTRACT | No effect | The specialist agent does not perform session-lifecycle scope-contract work; that is orchestrator/Walter. |
| INV-PF-ATTESTATION | No effect | Session-close attestation is orchestrator/Walter scope, not specialist-runtime. |
| INV-BRANCH-NOT-MAIN | No effect | The specialist agent's tool palette does not include state-mutating git; commits are out-of-scope (structural). |
| INV-HO-ROTATION | No effect | HANDOFF.md hygiene is orchestrator/Walter scope; the specialist does not write HANDOFF.md. |
| INV-HO-NO-STALE-HASH | No effect | Same as INV-HO-ROTATION — HANDOFF narrative is not a specialist surface. |
