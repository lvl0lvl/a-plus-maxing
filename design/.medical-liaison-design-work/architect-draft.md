---
title: medical-liaison (Role 7) Design Doc — Architect Draft (Phase 1)
type: design-doc-drafter-fragment
drafter: health-specialist-architect
role_slug: medical-liaison
role_class: specialist
pass: 3
sections_owned: [1, 2, 3, 4, 13, 15, 16]
pass_1_substrate: design/.medical-liaison-design-work/domain-research.md
base: bfb89bf (worktree HEAD at draft time, 2026-05-29)
status: architect-draft (feeds Phase-2 orchestrator synthesis; SE + QA drafters own the other sections)
---

# medical-liaison (Role 7) — Architect Draft

Sections owned by this drafter: §1, §2, §3, §4, §13, §15, §16. The SE drafter owns §5–§10, §12; the QA drafter owns §11, §14, §17, §18. I do NOT author those here. Cross-references to them are by section number only.

Substrate: `design/.medical-liaison-design-work/domain-research.md` (Findings A1–A4, B1–B4, C1–C4, D1–D4, E1–E5, F1–F4; Recommendations R1–R16; OQ-1–OQ-5). Cited by Finding/R/OQ ID throughout.

---

## §1 — Problem Statement

medical-liaison is the project's non-prescribing care-coordination and adjudication specialist. It collates compounds tagged `risk_tier: medium+` into a doctor-visit queue, runs a BPMH-shaped reconciliation intake, surfaces interaction/contraindication conflicts with explicit source attribution, assembles the operator's first-MD-visit handout, and serves as the canonical `BLOCK_WITH_OVERRIDE_PATH` adjudicator that sets `severity_final` on HIGH/MEDIUM safety findings. Its value is elicitation and collation discipline, not clinical judgment (Synthesis pattern 1): it never prescribes, never authors wiki entries, and never renders an interaction or deprescribing verdict.

Specific gaps this role addresses:

1. **No role finalizes a `BLOCK_WITH_OVERRIDE_PATH` verdict.** Role 4 (medical-safety-reviewer) emits `severity_proposed` only and is structurally forbidden from finalizing its own verdict; pre-Role-7 the project falls back to `operator-with-warning`, which is the operator (A3) adjudicating their own block. A finding-raiser that finalizes its own verdict carries self-preference bias (~10–25%) compounded by sycophancy (~98% reversal under pushback). Source: Finding E4; Role 4 §4.4 OUTBOUND row 4; §14 EC-4.
2. **No role owns the doctor-visit queue or the MD handout.** Specialist risk-floor HALTs route to "medical-liaison's doctor-visit queue" (Role 1 §13 row 6 + §14 EC-10) but no deployed role drains that queue into a clinician-ready artifact. Source: Finding F1; Role 1 §13 row 6.
3. **No role runs omission-resistant medication/supplement reconciliation.** Omission is the dominant transition error (~one-third of patients; 85% origin-in-history) and supplement non-disclosure runs ~67%; passive intake reproduces both gaps. No prior specialist elicits a five-field, supplement-inclusive, second-source-confirmed record. Source: Findings A2, A3, A4.
4. **No role owns the override record schema.** The `BLOCK_WITH_OVERRIDE_PATH` adjudicator slot exists (Role 4 §4.4 row 4) but the override-record field-set, the severity-scaled evidence rung, and the content-validation discipline (not mere presence) are unowned. Source: Findings D1–D4, F2.

---

## §2 — Role Definition

### 2.1 Identity

You are the medical-liaison. You collate `risk_tier: medium+` compounds and contraindications into a doctor-visit queue, assemble the MD handout, and adjudicate HIGH/MEDIUM safety blocks by setting `severity_final` against an out-of-band override record — you never prescribe.

*(Word count: 39. No must/never/always/refuse lexicon — "never prescribe" is a function statement, not a modal directive; the SE drafter should verify the deployed Identity stays ≤40 words per §13 R13-1 and re-checks the lexicon. Anti-sycophancy anchor lives in §5/§11, inherited three-mechanism from Role 1 §4 OUTBOUND row 5; the deployed Identity sentence carries no modal lexicon by R1/R3.)*

### 2.2 Role Boundaries

**I own:** the `artifacts/_doctor-visit-queue` artifact and its SBAR-shaped handout skeleton (Finding F3); `contraindications` entries (WIKI row); the BPMH-shaped reconciliation intake (Findings A1–A4); the severity-ranked, source-attributed interaction-triage surface (Findings B1, B4); `severity_final` adjudication AND the override record for HIGH/MEDIUM `BLOCK_WITH_OVERRIDE_PATH` findings (Findings E4, D1–D4); the approval gate on threat-model-catalog entries before they become invariants (Role 4 §4.4 OUTBOUND row 3 — approval, NOT authoring).

**I do NOT own:** the deploy-verdict schema or band→verdict mapping (medical-safety-reviewer Role 4, §4.4 row 1); `severity_proposed` / three-axis severity composition (Role 4); CRITICAL / H1–H2 disposition, which is `mechanical-auto-block-per-R3` and non-overridable except by Role 1 invariant amendment (medical-safety-reviewer Role 4 emits it; Role 1 health-specialist-architect owns the amendment); the 8-class refusal taxonomy, H-class enumeration, GRADE two-axis, three-mechanism anti-sycophancy (health-specialist-architect Role 1, §4 OUTBOUND rows 1–5); compound/biomarker/protocol wiki authoring and `aplus-research` dispatch (per-specialist runtime; medical-liaison `target_class: none`, collates only); the audit-script bash (health-implementer Role 2); clinical prescribing judgment (no role has it — it routes to the doctor).

When I detect a problem in a not-owned area, I write a one-line finding (clause + downstream owner) into the design-doc Phase-3 channel or, at runtime, append it to the doctor-visit queue and log to `vault/meta/contradictions.md`; I do not edit the affected artifact or construct an override path outside my HIGH/MEDIUM band.

**Hard adjudicator boundary (load-bearing).** medical-liaison sets `severity_final.set_by: medical-liaison` + a verdict ONLY for HIGH/MEDIUM `BLOCK_WITH_OVERRIDE_PATH` findings. For `composite_band: CRITICAL` OR `harm_class ∈ {H1, H2}`, the disposition is `mechanical-auto-block-per-R3` — non-overridable except by a Role 1 invariant amendment. medical-liaison MUST NOT construct an override record or override path for that band; the non-overridable property is asserted by a null/absent `override_path`, never by prose (Finding F1; Role 4 §4.4 row 4; substrate F4 AP-cue 5). Releasing an auto-block is the same sin as the reviewer softening one (Finding E4, symmetric).

---

## §3 — Pass-1 Deliverable Digest

Source: `design/.medical-liaison-design-work/domain-research.md` (path resolves; this role HAS its own Pass-3 deep-research, so §3 uses the standard Findings/Recommendations form, NOT the specialist-fallback inheritance form — the fallback applies only to specialists whose Pass-3 research has not been completed, per DESIGN_DOC_TEMPLATE.md §3).

Finding count in substrate: 21 `### Finding` headings (A1–A4, B1–B4, C1–C4, D1–D4, E1–E5 = 4+4+4+4+5). §3.1 has 21 rows. The F-series (F1–F4) are project-contract-mapping and worked-artifact sections, not `### Finding` headings — they are consumed in §4 and §13, not counted as Findings rows. (SE/QA: re-grep `^### Finding ` before finalize to confirm 21.)

### 3.1 Findings table

| # | Claim (1 sentence) | Source lines | AGENT_TEMPLATE section | Verdict |
|---|---|---|---|---|
| A1 | NPSG.03.06.01 defines the five-field record (name, dose, frequency, route, purpose) and pulls supplements into scope. | L34–L38 | Communication (handout schema); Modes (intake) | ACCEPTED |
| A2 | The reference method is a BPMH (interview + second source); recall alone is ~87% wrong. | L40–L44 | Core Rules; Modes (intake) | ACCEPTED |
| A3 | One-third of patients carry a transition error, 85% origin-in-history, omission dominant. | L46–L50 | Core Rules (omission-first); Anti-Patterns | ACCEPTED |
| A4 | Supplement non-disclosure (~67%) is the gap a prescription-only record cannot close. | L52–L56 | Core Rules; Communication (mandatory supplement rows) | ACCEPTED |
| B1 | Major interaction databases disagree massively on existence and moderately on severity. | L62–L72 | Core Rules (surface disagreement); Communication | ACCEPTED |
| B2 | Supplement-drug interactions are common but mostly low-severity; high-severity mechanisms are few/known. | L74–L78 | Core Rules (watchlist + honest base-rate labels) | ACCEPTED |
| B3 | LLMs are the weakest interaction layer (best OSS 38.12% on RxSafeBench, verified). | L80–L84 | Core Rules (never the interaction authority); Anti-Patterns | ACCEPTED |
| B4 | Clinicians override ~90% of DDI alerts; rank by significance or be ignored. | L86–L90 | Core Rules (severity-rank/threshold); Communication | ACCEPTED |
| C1 | SBAR is the front-loading discipline that flattens the hierarchy; evidence real but soft. | L96–L98 | Communication (SBAR handout) | ACCEPTED |
| C2 | Pre-visit ranked agendas help only when short and engaged; force prioritization. | L102–L106 | Communication (ranked top-3) | ACCEPTED |
| C3 | Patient-generated lists are authoritative for OTC/supplements but fail on completeness; enforce per-item schema. | L108–L112 | Communication (per-item schema) | ACCEPTED |
| C4 | Deprescribing frameworks (STOPP/START v3, Beers 2023, MAI): supply inputs, never verdicts. | L114–L118 | Core Rules (no STOP/START verdict); Communication | ACCEPTED |
| D1 | The AMA template: the narrative, not the signature, is the protection. | L124–L128 | Communication (override record); Anti-Patterns | ACCEPTED |
| D2 | Informed-refusal symmetry: refusing requires the same informed process plus risks-of-refusing plus a reason. | L130–L134 | Communication (override record fields) | ACCEPTED |
| D3 | SDM + Appelbaum–Grisso sliding scale: required rigor scales with severity. | L136–L140 | Core Rules (severity-scaled rung); Loop-Breaking | ACCEPTED |
| D4 | Auditability: verbatim caution + disclosed risks + reason + voluntariness + tamper-evident timestamp. | L142–L146 | Communication (override schema); §13 | ACCEPTED |
| E1 | Authority/educational framing is the dominant medical-LLM bypass (45.0%/83.3%, Ekram 2026). | L152–L156 | Anti-Patterns (AUTHORITY_FRAMING_BYPASS); §13 | ACCEPTED — corrected figure; see §18 OQ-2 |
| E2 | Sycophancy: ~98% reversal under pushback; 94–100% false-equivalence compliance. | L158–L162 | Core Rules (out-of-band auth); Anti-Patterns | ACCEPTED |
| E3 | Benchmark-passing models still fail injection at 80–100%; verify on the adversarial path. | L164–L168 | §15 (adversarial-path verification) | ACCEPTED |
| E4 | A finding-raiser that finalizes its own verdict is structurally biased; independent adjudication reduces error. | L170–L174 | Identity; Role Boundaries; Core Rules | ACCEPTED — the role's reason-to-exist |
| E5 | A non-prescribing agent still harms via omission, false reassurance, rationalizing self-overrides. | L176–L180 | Core Rules (false-reassurance is blockable); Anti-Patterns | ACCEPTED |

### 3.2 Pass-1 Recommendations (R1–R16)

| # | Recommendation (1 sentence) | Verdict | Rationale (DEFERRED/REJECTED only) |
|---|---|---|---|
| R1 | Five-field, supplement-inclusive handout schema. | ACCEPTED | — |
| R2 | Active, prompted, second-source elicitation (BPMH-shaped). | ACCEPTED | — |
| R3 | Omission-first bias. | ACCEPTED | — |
| R4 | Multi-source interaction triage, never an interaction verdict. | ACCEPTED | — |
| R5 | Severity-ranked, deduplicated, thresholded output. | ACCEPTED | — |
| R6 | Known-high-severity mechanism watchlist + honest base-rate labeling. | ACCEPTED | — |
| R7 | SBAR-shaped one-page handout, non-prescribing-bounded. | ACCEPTED | — |
| R8 | Supply deprescribing inputs, never verdicts. | ACCEPTED | — |
| R9 | Override record = digital AMA/informed-refusal note; validate content. | ACCEPTED | — |
| R10 | Severity-scaled override rigor (Appelbaum–Grisso). | ACCEPTED | — |
| R11 | Out-of-band, logged authorization; no in-conversation concession. | ACCEPTED | — |
| R12 | Educational/authority framing is elevated-risk, not neutralizing (AUTHORITY_FRAMING_BYPASS mandatory). | ACCEPTED | — |
| R13 | Adjudicate, do not self-finalize; default BLOCK; maintain verdict absent new cited evidence. | ACCEPTED | — |
| R14 | False reassurance and silent omission are blockable harms equal to commission. | ACCEPTED | — |
| R15 | Verify on the adversarial path. | ACCEPTED | — |
| R16 | Collation-only, no runtime research dispatch (`target_class: none`; mode-floor exempt). | ACCEPTED — see §13 PROPOSED-DEFECT row + §18 OQ-1 | The exemption is promised by the risk table but the LIVE R13-12 check does not honor it; the deployed profile cannot satisfy R13-12 without integrator adjudication. |

---

## §4 — Cross-Role References (Directional)

Per `DESIGN_DOC_TEMPLATE.md` §4. medical-liaison is a LATE role; §4 is INBOUND-heavy (inherits from Roles 1 + 4) with a small OUTBOUND set (the queue artifact contract + the escalation-intake contract). No upstream canonical statement is redefined — each row references by source-doc + §-row anchor.

### 4.1 INBOUND from Role 1 (`design/health-specialist-architect-design.md` §4 OUTBOUND, L127–L134; §13 row 6 L480; §14 EC-10 L585)

| Direction | Item | Source anchor | How handled |
|---|---|---|---|
| INBOUND | 8-class refusal taxonomy (incl. AUTHORITY_FRAMING_BYPASS) | Role 1 §4 OUTBOUND row 1 (L127) | References by class name; deployed Role Boundaries cites ≥4 classes incl. mandatory AUTHORITY_FRAMING_BYPASS (Finding E1; §13 R13-5 + R13-5.1). Does NOT redefine. |
| INBOUND | H-class enumeration (H1–H8) + `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)` | Role 1 §4 OUTBOUND row 2 (L128) | medical-liaison parses `harm_class` as the input that determines whether a finding is in its HIGH/MEDIUM adjudication band or is `mechanical-auto-block-per-R3` (H1/H2). References by anchor; does not re-embed the composition rule. |
| INBOUND | GRADE two-axis discipline (certainty × strength; strong-with-low HALT) | Role 1 §4 OUTBOUND row 3 (L129) | Any claim-emitting surface in the handout (e.g., interaction triage notes) carries both axes; strong+low-certainty HALTs (§13 R13-5.5). Inherits vocabulary verbatim. |
| INBOUND | Three-mechanism anti-sycophancy (A / B / C) | Role 1 §4 OUTBOUND row 4 (L130) | Mechanism B (maintain-position-absent-new-cited-evidence) is the load-bearing one for the adjudicator (Finding E2 ~98% reversal); inherited verbatim into §5/§11. Mechanism A and C inherited per the structural slot. §13 R13-5.6 checks all three present. |
| INBOUND | Operator-profile hard-limit precondition | Role 1 §4 OUTBOUND row 5 (L131) | medical-liaison reads `vault/meta/operator-profile.md` at DISPATCH TIME to populate the queue and tighten contraindication filtering — never to relax a band (substrate F4 AP-cue 6). The template does NOT embed Walter's Jan-2026 issue; §13 R13-6.7 checks no operator-content leak. |
| INBOUND | Risk-floor escalation target = "medical-liaison's doctor-visit queue" | Role 1 §13 row 6 (L480) + §14 EC-10 (L585) | medical-liaison is the named drain for specialists' risk-floor HALTs. It receives the escalation; the specialist's two-step override-acknowledgment (canonical literal + contradictions-log) remains the specialist's contract. Defines the intake side as §4.3 OUTBOUND row 2 below. |

### 4.2 INBOUND from Role 4 (`design/medical-safety-reviewer-design.md` §4.4 OUTBOUND, L146–L150; EC-4 L597–L603)

| Direction | Item | Source anchor | How handled |
|---|---|---|---|
| INBOUND | Deploy-verdict schema + band→verdict mapping (CRITICAL→BLOCK; HIGH·MEDIUM→BLOCK_WITH_OVERRIDE_PATH; LOW·NONE→DEPLOY) | Role 4 §4.4 row 1 (L146) | Consumed as-is. medical-liaison acts only on the HIGH/MEDIUM rows of this mapping. Mapping is mechanical and owned by Role 4; medical-liaison does not re-derive a band. |
| INBOUND | `safety_finding` three-axis composite block (`severity_proposed: true`, `severity_final: null` until adjudicator sets) | Role 4 §4.4 row 2 (L147) | medical-liaison is the agent that flips `severity_final` from `null` to `{set_by: medical-liaison, ...}` for HIGH/MEDIUM. It reads `harm_class` (top-level composed) to gate auto-block. Does not author the composite. |
| INBOUND | Threat-model catalog approval gate ("medical-liaison approves entries before they become invariants") | Role 4 §4.4 row 3 (L148) | APPROVAL gate, not authoring. medical-liaison adjudicates whether a proposed A×S×P×H entry is ready to promote via the INVARIANTS change-discipline ritual; weighs Findings E1–E3 when approving an authority-framing / injection-class entry. Does not edit `templates/threat-model-catalog.yaml`. |
| INBOUND | `BLOCK_WITH_OVERRIDE_PATH` adjudicator slot; default adjudicator `medical-liaison`; pre-Role-7 fallback `operator-with-warning` + literal "operator is overriding a safety block"; H1/H2 CRITICAL non-overridable | Role 4 §4.4 row 4 (L149) + EC-4 (L597) | **medical-liaison's deployment FLIPS the fallback.** Post-deployment: `override_path.adjudicator: medical-liaison`, `severity_final.set_by: medical-liaison` for HIGH/MEDIUM. The `operator-with-warning` + `fallback_warning_prose` path is deprecated for HIGH/MEDIUM (mirror of Role 4 §17 BC-1, L741). medical-liaison references the canonical literal "operator is overriding a safety block" (Role 4 §13 row 7 / XR-004 / bead z8i), never redefines it. H1/H2 CRITICAL stays non-overridable (hard boundary, §2.2). |
| INBOUND | Divergence-log tuning cadence (count N=5 + rate ≥30% rolling-10) | Role 4 §4.4 row 5 (L150) | medical-liaison's adjudicator-override decisions are the input that Role 4's divergence log tunes against. medical-liaison logs each HIGH/MEDIUM verdict so Role 4's rate-based trigger has a denominator. References Role 4's cadence; does not own the re-tuning. |

### 4.3 OUTBOUND from medical-liaison (NEW; consumed by orchestrator + specialists)

| Direction | Item | Counterpart | How handled |
|---|---|---|---|
| OUTBOUND | The `artifacts/_doctor-visit-queue` artifact contract (SBAR-shaped handout; severity-ranked source-attributed interaction list; five-field supplement-inclusive med table; ranked top-3 questions) | orchestrator (artifact consumer); operator (reader at July-2026 visit) | Defined here per Finding F3 (handout skeleton) + R1/R7. Downstream references the artifact by path; the schema is medical-liaison's. SE drafter instantiates the field-set in §9. |
| OUTBOUND | The escalation-intake contract: how a specialist's risk-floor HALT lands in the queue | all 14 specialists (escalation producers) | medical-liaison accepts an escalation carrying `{compound, risk_tier, contraindication_or_rx_collision, source_specialist}` and queues it severity-ranked (Finding F1 + B4). The specialist's emission contract (canonical literal + contradictions-log) is owned by Role 1 §13 row 6 / EC-10; medical-liaison owns only the receiving/ranking side. |
| OUTBOUND | The override record schema (the digital AMA/informed-refusal note) | orchestrator (deploy-gate consumer of `severity_final`) | Defined here per Findings D1–D4 + F2 + R9–R11; instantiated by the SE drafter in §9. Fields: `caution_verbatim`, `composite_band`, `risks_communicated` (incl. risks-of-proceeding), `operator_reason`, `evidence_tier_required`/`evidence_provided` (Appelbaum–Grisso rung), `override_literal` (canonical, referenced not redefined), `voluntariness_note`, `timestamp` + `contradictions_log_ref`. |

**Anti-redefinition rule.** Every INBOUND row references its source by path + §-row anchor; no upstream canonical statement (taxonomy, H-class, GRADE, band→verdict mapping, override literal) is inlined. The Phase-3 adversarial-review checks cross-sibling duplication.

---

## §13 — Mechanical Enforcement Map

`scripts/audit-specialist-profile.sh` is LIVE and executable on the worktree base (HEAD bfb89bf at draft time; the dispatch brief cited base c021cc1 — the script is present on both; SE/QA confirm path resolves at synthesis). Rows below are the checks the deployed medical-liaison `agent.md` must pass. Tags: LIVE (script exists + path verified), REFERENCED (an INVARIANTS.md row enforces it), PROPOSED / PROPOSED-DEFECT (does not gate, surfaced in §18).

| Check | Verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|
| R13-1 Identity | `## Identity` present, ≤40 words, no banned adjectives | `scripts/audit-specialist-profile.sh` `check_identity` (L140) | LIVE | BLOCK |
| R13-2 Description routing | frontmatter `description:` ≤200 chars, ≥1 routing cue, no body leak | `check_description_routing` (L151) | LIVE | BLOCK |
| R13-3 Body length | body ≤200 lines AND ≤2500 cl100k tokens | `check_body_length` (L165) | LIVE | BLOCK |
| R13-4 Voice register | 0 banned-modal tokens in prose (code spans excluded) | `check_voice_register` (L182) | LIVE | BLOCK |
| R13-5 Refusal classes | ≥4 taxonomy refusal-class identifiers in Role Boundaries | `check_refusal_classes` (L191) | LIVE | BLOCK |
| R13-5.1 Authority framing | AUTHORITY_FRAMING_BYPASS present (mandatory; Walter A3) | `check_authority_framing` (L214) | LIVE | BLOCK |
| R13-5.5 GRADE two-axis HALT | certainty axis + strength axis + strong-with-low HALT disposition all present | `check_grade_halt` (L221) | LIVE | BLOCK |
| R13-5.6 Anti-sycophancy | Mechanisms A, B, C each present | `check_anti_sycophancy` (L232) | LIVE | BLOCK |
| R13-6.5 Section count | exactly 11 `## ` level-2 sections (10 base + Modes) | `check_section_count` (L252) | LIVE | BLOCK |
| R13-6.7 Operator no-writeback | 0 operator-bound content leaks (Walter\|2026-01\|January 2026); ≥1 operator-profile path ref | `check_operator_no_writeback` (L271) | LIVE | BLOCK |
| R13-7 Mechanical-Check/Binary line | every section carries a Mechanical Check / Binary line | `check_mechanical_stubs` (L280) | LIVE | BLOCK |
| R13-7.5 Section uniqueness | no duplicate section headings | `check_section_uniqueness` (L294) | LIVE | BLOCK |
| R13-9.5 Library-index | `library-index.md` companion exists, ≤30 lines, ≥1 `vault/library/` ref | `check_library_index` (L317) | LIVE | BLOCK |
| R13-11 PF resolution | ≥3 distinct PF-S#-## ids in Anti-Patterns, each resolvable in `memory/process-failures.md` | `check_pf_resolution` (L344) | LIVE | BLOCK |
| R13-12 aplus-research mode-floor | a `--mode` floor (standard\|deep\|ultradeep) present in Tools | `check_aplus_mode_floor` (L359) | **PROPOSED-DEFECT** | BLOCK (mis-fires for collation-only) |
| Role inlining | full 11-section profile inlined in role-tagged dispatches | `.claude/hooks/enforce-role-inlining.sh` | REFERENCED (INV-ROLE-INLINING) | BLOCK |
| Branch hygiene | working commits never on `main` | `.claude/hooks/block-commit-main.sh` | REFERENCED (INV-BRANCH-NOT-MAIN) | BLOCK |
| Override-record content validation | `caution_verbatim` non-empty; `operator_reason` non-trivial at HIGH; `evidence_provided` rung ≥ band rung; H1/H2/CRITICAL has null `override_path` | `scripts/audit-medical-liaison-override.sh` (does not exist) | PROPOSED | (deferred per §18 OQ-3) |
| Override literal presence | override record contains the canonical literal "operator is overriding a safety block" | grep target shared across project audits (Role 4 §13 row 7) | PROPOSED | (deferred per §18 OQ-3) |

**R13-12 PROPOSED-DEFECT detail (OQ-1).** `check_aplus_mode_floor` (L359, R13-12, BLOCK) is unconditional: it greps the Tools section for a `--mode` floor and violates if absent. It never reads `templates/specialist-risk-class.yaml`. Only the separate WARN check `check_mode_floor_correctness` (L366, R13-12.5) reads the risk table. The risk table (L93–L97) sets medical-liaison `mode_floor: not_applicable`, `target_class: none`, and states "Tools section MUST NOT declare aplus-research --mode entry (§13 row 12 audit exempts via this field)." The deployed health-implementer profile makes the same promise. A correctly-authored collation-only medical-liaison profile — which must NOT declare a `--mode` floor — therefore FAILS R13-12 (BLOCK). The fix (mirror the row-12.5 risk-table read so `mode_floor: not_applicable` skips R13-12) belongs to Role 2 (health-implementer owns the audit-script bash); medical-liaison cannot edit `scripts/`. Tagged PROPOSED-DEFECT; routed to §18 OQ-1 as an integrator bead. Until fixed, the integrator must adjudicate the known R13-12 BLOCK against the documented exemption rather than treating it as a deploy-blocker.

Note: R13-10 (Negative Examples count) and R13-15 (Modes shape) are WARN, not BLOCK; R13-8 / R13-9 (IDENTICAL/DIFFER) are corpus-gated and owned by Role 2's boilerplate discipline — not enumerated as medical-liaison BLOCK rows. SE/QA may add the WARN rows if they choose; they do not gate deployment.

---

## §15 — Acceptance Criteria (Role-Specific)

### 15.1 Inherited from `/upgrade-agent` Phase 7

Generic constraints (line count ≤200, token count, all AGENT_TEMPLATE.md sections present, library-index reference paths resolve, catalog entry consistency, BAD/GOOD pair count, anti-sycophancy placement, negative-examples placement, operational completeness) are enforced by `/upgrade-agent` Phase 7 (lines 291–301 of `upgrade-agent.md`) and not restated here.

### 15.2 Role-specific (binary)

1. Identity sentence ≤40 words, contains no must/never/always/refuse modal lexicon, states the collate-and-adjudicate function and the non-prescribing bound (§13 R13-1).
2. Role Boundaries cites ≥4 of the 8 refusal classes, including AUTHORITY_FRAMING_BYPASS verbatim (§13 R13-5, R13-5.1).
3. The hard adjudicator boundary appears verbatim: medical-liaison sets `severity_final` ONLY for HIGH/MEDIUM; CRITICAL / H1–H2 is `mechanical-auto-block-per-R3` with a null/absent `override_path` (grep for both the band literal and "mechanical-auto-block-per-R3").
4. The override record schema names all eight fields from §4.3 OUTBOUND row 3 (caution_verbatim, composite_band, risks_communicated, operator_reason, evidence_tier_required/evidence_provided, override_literal, voluntariness_note, timestamp+contradictions_log_ref).
5. The deployed profile references the canonical override literal "operator is overriding a safety block" exactly and does NOT redefine it (grep returns the exact string; no alternative wording of the literal).
6. The override authorization is specified as out-of-band + logged, NOT an in-conversation concession (Finding E2; grep Core Rules / Communication for "out-of-band" or "logged artifact" framing).
7. GRADE two-axis present on any claim-emitting handout surface with a strong-with-low-certainty HALT disposition (§13 R13-5.5).
8. All three anti-sycophancy mechanisms (A/B/C) present; Mechanism B explicitly covers maintain-verdict-absent-new-cited-evidence (§13 R13-5.6; Finding E4/E2).
9. Anti-Patterns cite ≥3 resolvable PF-S#-## ids (§13 R13-11) and include the operator-as-A3 / educational-framing cue (Finding E1; substrate F4 AP-cue 1).
10. No operator-bound content leak (no "Walter" / "January 2026" in the profile body); operator-profile referenced by path only (§13 R13-6.7).

---

## §16 — Invariants at Risk

Scope: Format/Document + Process + Role-discipline categories. Research-domain INV-RESEARCH-* are OUT-OF-SCOPE: medical-liaison has `target_class: none` and dispatches no `aplus-research` (R16; risk table L93–L97), so it produces no wiki content and triggers no research gate. (The R13-12 mis-fire of OQ-1 is an audit-SCRIPT defect, not a research-domain invariant in scope here.)

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-ROLE-INLINING | Strengthens | The deployed agent.md is an 11-section role profile inlined per `enforce-role-inlining.sh`; the adjudicator role's full boundary set must be inlined or a role-tagged dispatch is structurally incomplete. |
| INV-BRANCH-NOT-MAIN | No effect | medical-liaison performs no session-lifecycle git work; tool restrictions exclude state-mutating git. |
| INV-SCOPE-CONTRACT | No effect | Runtime adjudication is not session-lifecycle work; no scope contract authored by this role. |
| INV-PF-ATTESTATION | No effect | Session-close attestation is the orchestrator's, not this role's. |
| INV-HO-ROTATION / INV-HO-NO-STALE-HASH | No effect | medical-liaison writes to `artifacts/_doctor-visit-queue` and `vault/meta/contradictions.md`, not HANDOFF.md. |

**Candidate invariants the adjudicator role implies (surfaced for the INVARIANTS change-discipline ritual; NOT promoted here):**

- **INV-OVERRIDE-RECORD-SCHEMA (PROPOSED).** Every HIGH/MEDIUM `BLOCK_WITH_OVERRIDE_PATH` finalized by medical-liaison carries an override record with all eight §4.3 fields, content-validated (not presence-validated), with `evidence_provided` rung ≥ `composite_band` rung per the Appelbaum–Grisso scale (Findings D3, D4, F2). Mechanical home: the PROPOSED `scripts/audit-medical-liaison-override.sh` row in §13. Establishes the non-rubber-stamp property mechanically.
- **INV-CRITICAL-NON-OVERRIDABLE (PROPOSED).** No finding with `composite_band: CRITICAL` OR `harm_class ∈ {H1, H2}` may carry a non-null `override_path`; the adjudicator must not construct one (Finding F1; Role 4 §4.4 row 4; substrate F4 AP-cue 5). Mechanical home: a grep asserting null/absent `override_path` whenever band is CRITICAL or harm_class is H1/H2. This is the adjudicator-side mirror of Role 4's H1/H2 auto-block; it closes the symmetric "liaison talks itself INTO releasing an auto-block" gap that the Role-4-side check alone does not cover.

Both candidates require the four-step INVARIANTS change ritual (cite → evidence → user approval → Change Log row) and are NOT added to the register by this draft. PF-S3-01 (mechanical-fix-is-not-a-verdict) and INV-ROLE-INLINING are the two live invariants this role's design most directly touches.

---

## Orchestrator Communication Block (7 fields)

1. **Status** — `draft-emitted`.
2. **Artifact paths** — `design/.medical-liaison-design-work/architect-draft.md` (this file). No other file written or modified.
3. **Coverage tally** — 7 of 18+A sections drafted (the architect-owned set: §1, §2, §3, §4, §13, §15, §16). SE owns §5–§10, §12; QA owns §11, §14, §17, §18. Not authored here.
4. **Mechanical-check status** — §13 enumerates 14 LIVE BLOCK rows + 2 REFERENCED + 1 PROPOSED-DEFECT (R13-12) + 2 PROPOSED (override-record + override-literal). LIVE script `scripts/audit-specialist-profile.sh` path verified executable (not run against a sample profile this dispatch — no deployed medical-liaison agent.md exists yet; the script gates Session B, per §13). R13-12 surfaced as PROPOSED-DEFECT per OQ-1. PROPOSED rows deferred per §18.
5. **Decisions (simpler-assumption choices)** —
   - §3 uses the standard Findings/Recommendations form (NOT specialist-fallback): assumption = "Pass-3 deep-research IS complete for this role" (substrate exists, 21 Findings + R1–R16); alternative not taken = the foundation-inheritance fallback form, which applies only to specialists lacking their own Pass-3 research.
   - §3.1 row count = 21 (the `### Finding` headings A1–E5); assumption = F1–F4 are contract-mapping sections, not Findings rows; alternative not taken = counting F-series as Findings (would mis-state the substrate's Finding count).
   - §13 tagged R13-12 PROPOSED-DEFECT rather than LIVE-passing: assumption = a correctly-authored collation-only profile cannot satisfy an unconditional `--mode`-floor grep; alternative not taken = instructing the SE drafter to declare a spurious `--mode` floor to pass R13-12 (would violate the risk-table exemption and R16).
6. **Blockers** — none for the architect-owned sections. Two cross-role items routed (not edited): OQ-1 (R13-12 script defect, Role-2-owned `scripts/`) and OQ-2 (81.8% misattribution in frozen Role-1/Role-4 files). Both are §18 OQ / integrator-bead candidates for the QA drafter to carry into §18.
7. **Pass-1 anchor check** — every section cites ≥1 Finding / R / §-row / PF / INV: §1 (E4, A2–A4, F1, D1–D4), §2 (E4, D1–D4, A1–A4, B1/B4, F1/F3, Role 1 §4, Role 4 §4.4), §3 (all 21 Findings + R1–R16), §4 (Role 1 §4 OUTBOUND rows 1–5 + §13 row 6 + EC-10; Role 4 §4.4 rows 1–5 + EC-4; F1/F3), §13 (R13-* script line refs + INV-ROLE-INLINING + INV-BRANCH-NOT-MAIN + OQ-1), §15 (Findings E1/E2/E4 + §13 rows), §16 (INV-ROLE-INLINING, PF-S3-01, Findings D3/D4/F1 + Role 4 §4.4 row 4).

---

## Surfaced findings carried for §18 (handoff to QA drafter — do not lose)

- **OQ-1** — R13-12 audit gap. `check_aplus_mode_floor` (L359, BLOCK) is unconditional and does not honor `mode_floor: not_applicable` from `templates/specialist-risk-class.yaml`; a correctly-authored collation-only medical-liaison profile fails it. Fix belongs to Role 2 (owns `scripts/`); medical-liaison cannot edit scripts. Integrator bead candidate; non-blocker if the integrator adjudicates the documented exemption. (§13 PROPOSED-DEFECT row.)
- **OQ-2** — 81.8% misattribution. The "81.8% authority-impersonation" figure in `templates/refusal-class-taxonomy.yaml` (AUTHORITY_FRAMING_BYPASS `statutory_anchor`, L62), Role 1 §2.2 item 3, and Role 4 substrate is a verified misattribution — 81.8% is JBDistill benchmark effectiveness [61], not a medical authority-impersonation share; the genuine figures are 45.0%/83.3% (Ekram 2026 [60]). Frozen files; correction is a cross-role bead for the owning roles. AUTHORITY_FRAMING_BYPASS remains mandatory regardless. (Substrate OQ-2.)
- **OQ-3** — the two PROPOSED §13 rows (`scripts/audit-medical-liaison-override.sh` content-validation + the override-literal grep) do not exist yet; they do not gate the deployed agent.md and must appear in §18 + generate a follow-up bead at session close (DESIGN_DOC_TEMPLATE.md §13 PROPOSED handling).
- **OQ-3..OQ-5 (substrate)** — population base rates (mechanisms/standards transfer, base rates do not), missing fish-oil/creatine base rate, Ekram PDF re-verification. QA drafter folds these into §18 alongside the above.
