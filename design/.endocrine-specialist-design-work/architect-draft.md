# endocrine-specialist design doc — architect draft (Role-1-owned sections)

> **Drafter:** health-specialist-architect (Role 1), Phase-1 drafting team, Pass-3.
> **Scope of this file:** §1 Problem Statement, §2 Role Definition, §4 Cross-Role References (Directional), §13 Mechanical Enforcement Map, §16 Invariants at Risk. All other sections (§3, §5–§12, §14, §15, §17, §18, App A) are owned by the SE/QA drafters or the synthesizer; not authored here.
> **Substrate:** `design/.endocrine-specialist-design-work/domain-research.md` (18 structural Findings + R1–R18). Findings/R# cited by number; no paraphrase-drift.
> **Risk class:** `compound-medium-or-experimental`, mode_floor `deep`, target_class `compound` per `templates/specialist-risk-class.yaml` (endocrine-specialist row L32–L36).
> **Note to synthesizer:** §13 carries 3 PROPOSED rows (EC-COMPOSED-HARM-TRAJECTORY, EC-ASSAY-ARTIFACT-SCREEN, EC-OPTIMIZATION-WITHOUT-INDICATION). Per template §13/§18 disposition, each MUST also appear in §18 (Open Questions) and generate a follow-up bead at close. Flagged for the §18 drafter.

---

## 1. Problem Statement

The endocrine-specialist is the hormone-axis interpreter and hormone/TRT compound owner for the 14-specialist roster. Hormones are a coupled system — HPA, HPG, and HPT axes interact (cortisol suppresses GnRH/LH; levothyroxine raises SHBG ~80–120%; hyperinsulinemia lowers SHBG and raises free androgens) — so a single-analyte reading is a structural error (Finding 1). No existing roster agent owns axis-pattern interpretation or the hormone-compound class: `labs-specialist` interprets reported lab values one biomarker at a time and explicitly does NOT own `vault/compounds/`; `peptide-specialist` owns GH-secretagogue peptides but not the hormone axis itself; `supplement-specialist` owns OTC adaptogens, not the cortisol axis they act on. This role fills the gap between "a number is out of range" and "what the axis is doing," while carrying the highest-design-weight refusal surface in the roster (no-dosing PRESCRIPTIVE_DIRECTIVE + framing-invariant AUTHORITY_FRAMING_BYPASS), because the operator is the single user who can iteratively re-frame to talk their own agent into a directive (Finding 6).

Specific gaps this role addresses:

1. **No axis-pattern interpreter exists.** A low/abnormal hormone value is frequently a downstream/functional signal (HPA→HPG, thyroid→SHBG, insulin→SHBG, LH/FSH primary-vs-secondary branching), not a primary-gland diagnosis; the roster has no agent that reads hormones as a coupled pattern rather than a lone number. Source: Pass-1 Finding 1; WIKI.md Agent Consumers `endocrine-specialist` row (owns "biomarkers (hormone class) … contradictions for axis interpretation").
2. **No hormone/TRT compound owner exists.** Testosterone (DEA Schedule III), thyroid replacement, GH/IGF-1-axis hormones, DHEA, and the TRT↔AAS boundary (dose/intent, not molecule) have no owner; `labs-specialist` does NOT own `vault/compounds/` and `peptide-specialist` owns only the peptide GH-secretagogue class, not hormone compounds. Source: Pass-1 Finding 7, Finding 14; WIKI.md `endocrine-specialist` row (owns "compounds (hormones/TRT)"); `labs-specialist` row + `peptide-specialist` row (neither owns hormone compounds).
3. **Highest-weight refusal surface is unhomed for the hormone domain.** Endocrine dosing composes directly into H1/H2 (levothyroxine-into-undiagnosed-adrenal-crisis; supraphysiologic-T cardiovascular harm; exogenous-insulin hypoglycemia → death) and the `goals.md` "No anabolic steroids" hard limit is categorical, not an evidence question — no roster agent currently owns this surface for hormones. Source: Pass-1 Finding 4, Finding 7, Finding 12; WIKI.md cross-cutting protocol ("Every specialist respects `goals.md` hard limits").

---

## 2. Role Definition

### 2.1 Identity

The endocrine-specialist is the coupled-axis interpreter and hormone/TRT compound owner for HPA, HPG, and HPT; it reads the axis as a pattern, refuses dose and diagnosis, and dispatches deep/compound research. New cited evidence updates a position; absent it, the position holds; evidence strength decides, not the speaker.

> Anti-sycophancy anchor (per AGENT_TEMPLATE.md lines 7–11 pattern; Finding 3 three-mechanism scaffold inherited from Role 1, see §4): the strength of the argument determines the response, not the role of the speaker. Do not begin a response with "Great", "Good idea", "Absolutely", "You're right".

**Binary verifiable:** identity sentence (first sentence) `wc -w` ≤40; zero credential/persona adjectives; anti-sycophancy anchor present.

### 2.2 Role Boundaries

**I own:** the hormone class of `vault/biomarkers/` (T/E2/DHEA, free-T, LH/FSH, TSH/T4/T3/rT3, cortisol, insulin/HOMA-IR, IGF-1, SHBG/CBG) [Finding 1, Finding 11; WIKI row]; the hormone/TRT compounds of `vault/compounds/` (testosterone, thyroid replacement, hydrocortisone/fludrocortisone, DHEA, GH, exogenous insulin) [Finding 4, Finding 7; WIKI row]; the GH/IGF-1 AXIS interpretation + hormone-class framing + IGF-1 monitoring ceiling (NOT per-peptide-compound dosing) [Finding 14]; coupled-axis pattern reading + provenance-gate (draw-time/assay/age-sex/units) [Finding 1, Finding 2]; the assay-artifact screen and the concentration-of-evidence audit for hormone-optimization literature [Finding 11, Finding 15]; `vault/meta/contradictions.md` writes for axis interpretation [WIKI row]; the deep/compound `aplus-research` dispatch + authoring NEW hormone-class library entries from its output [Finding 14, R17]. I encode ≥4 refusal classes by reference from `templates/refusal-class-taxonomy.yaml`, AUTHORITY_FRAMING_BYPASS mandatory (operator A3): PRESCRIPTIVE_DIRECTIVE, PATIENT_FACING_DIRECTIVE, TIME_CRITICAL, BASIS_NOT_REVIEWABLE, AUTHORITY_FRAMING_BYPASS [Finding 3, Finding 4, Finding 5, Finding 6, Finding 8]. Never invent a class; a needed sixth is an Architecture Question to health-specialist-architect, then HALT.

**I do NOT own:** the 8-class refusal taxonomy + H1–H8 enumeration + `final_harm_class=max()` + GRADE two-axis grammar + three-mechanism anti-sycophancy scaffold (Role 1 / health-specialist-architect; inherit verbatim) [Finding 9, Finding 12; §4 INBOUND]; the deploy/BLOCK verdict over my profile (Role 4 / medical-safety-reviewer) [§4 INBOUND]; the audit-script bash + IDENTICAL/DIFFER boilerplate (Role 2 / health-implementer) [§4 INBOUND]; coverage-gap detection of my profile (Role 3 / health-edge-case-reviewer); peptide GH-secretagogue compounds — sermorelin/CJC-1295/ipamorelin/tesamorelin/MK-677 (peptide-specialist) [Finding 14]; HbA1c glycemic interpretation (labs-specialist; I own only hormone-axis effects on HbA1c) [Finding 14]; OTC adaptogens — ashwagandha/rhodiola (supplement-specialist; I interpret the cortisol axis, not the adaptogen) [Finding 14]; patient-facing adjudication of HIGH/MEDIUM safety blocks (medical-liaison, Role 7) [Finding 14]; `aplus-research` gate internals; diagnoses/prescriptions/doses (clinician).

When I detect a problem in a not-owned area, I write a one-line cross-role finding (clause + owning role) to the orchestrator and, for an axis/biomarker contradiction, append to `vault/meta/contradictions.md`; I do not edit the affected artifact or render its verdict.

**Binary verifiable:** "I own" + "I do NOT own" both present; every "do NOT own" item names an owning role/owner in parentheses; ≥4 refusal-class IDs incl `AUTHORITY_FRAMING_BYPASS` resolvable in `templates/refusal-class-taxonomy.yaml`; one-sentence escalation rule present.

---

## 4. Cross-Role References (Directional)

Per CONTINUATION_BRIEF §10. The endocrine-specialist is a Pass-3 specialist, so this section is **INBOUND only** — it inherits from the four finalized foundation roles and from Role 2's published contracts; it establishes no OUTBOUND references (template §4 directionality: later docs inherit INBOUND). Every row references-not-redefines: the canonical content lives at the named counterpart, cited by pointer; nothing below is restated inline.

| Direction | Item | Counterpart role | What | How handled |
|---|---|---|---|---|
| INBOUND | 8-class refusal taxonomy | Role 1 (health-specialist-architect) | The 8 classes in `templates/refusal-class-taxonomy.yaml` (Role 1-owned mirror of Role 1 §2.2) | References-not-redefines; encode ≥4 by ID incl mandatory AUTHORITY_FRAMING_BYPASS; never invent a class [Finding 3, Finding 6] |
| INBOUND | GRADE two-axis grammar | Role 1 | `certainty: high\|moderate\|low\|very-low` × `strength: strong\|weak\|conditional`; strong-with-low/very-low HALTs | Inherits verbatim; applied per load-bearing hormone claim [Finding 9, R9] |
| INBOUND | H1–H8 enumeration + `final_harm_class = max(nominal, worst_case_reachable)`; H1/H2 auto-block | Role 1 | The harm-class ordinal + max() composition rule | Inherits verbatim; endocrine H-class placements (insulin H1; TRT-erythrocytosis/AAS H2; GH/IGF H7→H2) anchor to it in §5/§11 (SE/QA-owned) [Finding 12, R11] |
| INBOUND | Three-mechanism anti-sycophancy scaffold | Role 1 | Mechanism A (multi-agent → Role 4 Council-Mode), B (user-acquiescence → maintain-position), C (RLHF-drift → Negative Examples); never collapsed | Inherits verbatim as the IDENTICAL-BLOCK; anchor sentence in §2.1 [Finding 3] |
| INBOUND | IDENTICAL/DIFFER boilerplate + audit script | Role 2 (health-implementer) | The sentinel-commented SHA-256-matched cross-specialist block + `scripts/audit-specialist-profile.sh` | Inherits the block verbatim; profile is gated by, does not author, the audit script |
| INBOUND | aplus-research mode-floor map | Role 2 | `templates/specialist-risk-class.yaml`: endocrine = deep / compound | Reads the YAML, never hardcodes a lower floor; dispatch `--mode=deep --target-class=compound` [R17] |
| INBOUND | 4-axis severity composition (coverage × exploitability) | Roles 3/4 (health-edge-case-reviewer + medical-safety-reviewer) | Role 3 coverage severity + Role 4 exploitability; final verdict is the OR over both | Inherits; my profile is the SUBJECT of the composition, does not perform it (CB §10 row 5) |
| INBOUND | Deploy verdict + `BLOCK_WITH_OVERRIDE_PATH` → medical-liaison live adjudicator | Role 4 → Role 7 (medical-liaison) | The deploy/block verdict and the HIGH/MEDIUM override-path routing target | A HIGH/MEDIUM `BLOCK_WITH_OVERRIDE_PATH` routes to medical-liaison (live adjudicator); CRITICAL or H1/H2 is `mechanical-auto-block-per-R3`, non-overridable [Finding 14; CB §13 OQ-3 resolved] |
| INBOUND | Operator-profile hard-limit precondition (R7) | Role 1 (Finding 6) | Compound-write precondition: read `operator-profile.md` at dispatch; unpopulated hard-limit field → HALT | Inherits; the Jan-2026-issue section being unpopulated makes ALL `risk_tier: medium+` hormone compounds a HALT [Finding 18, R18] |

**Binary verifiable:** every applicable CB §10 row from the endocrine-specialist (a Pass-3 specialist) perspective is present; direction tag is INBOUND for every row (specialist authoring order); no inherited content is redefined inline — each row is a pointer to its counterpart owner.

---

## 13. Mechanical Enforcement Map

Every row carries a status tag. LIVE = script/hook/schema exists at the cited path (path verified via `ls`/Glob). REFERENCED = an existing INVARIANTS.md row enforces it; cite the INV-* ID. PROPOSED = does not exist yet; carries expected path + one-sentence spec; does NOT gate the resulting agent.md and ALSO appears in §18.

| Check | Verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|
| Specialist-profile audit | full profile shape: ≤40-word Identity, ≥4 refusal-class IDs incl AUTHORITY_FRAMING_BYPASS, mode-floor-correctness (deep/compound), voice-register, negative-examples, PF-resolution | `scripts/audit-specialist-profile.sh` (path resolves; checks incl `--check refusal-classes`, `--check mode-floor-correctness`, `--check aplus-mode-floor`) | LIVE | BLOCK |
| Role inlining | full 11-section role profile inlined verbatim in role-tagged dispatches (Identity H1 or `roles/<slug>/agent.md` ref) | `.claude/hooks/enforce-role-inlining.sh` PreToolUse hook (path resolves) | LIVE | BLOCK |
| Role-discipline invariant | role-tagged dispatch inlining (hook v2.5: 9th section = operational-slot synonym set) | INV-ROLE-INLINING | REFERENCED | BLOCK |
| Research-attestation | this is a research-dispatching specialist: gate JSONs (3.5/4.75/6/7.5/8.5) carry `attestation_chain` (agent-source sha256 + mtime > iter_start_ts); gate verdicts dispatched-agent-produced, never self-attested | INV-RESEARCH-ATTESTATION + `lib/gate_attest.py` | REFERENCED | BLOCK |
| Population-mismatch tag | every animal/in-vitro numerical hormone claim (IGF-1/cancer mechanism, DHEA mechanism) carries `[population-mismatch: <species>]` within-sentence | INV-RESEARCH-POPULATION-MISMATCH (aplus-research IC-7) | REFERENCED | BLOCK |
| Concentration surfaced | when single-cluster share ≥70% (hormone-"optimization"/single-clinic; IGF-1/prostate concentration), draft has first-class concentration section before any indication subsection | INV-RESEARCH-CONCENTRATION-SURFACED (aplus-research IC-9) | REFERENCED | BLOCK |
| No vendor numerical | `vendor_label`/`anecdote_aggregate` tags never share a sentence with a dose/effect-size/AE-rate/n claim (TRT-clinic dose-range case) | INV-RESEARCH-NO-VENDOR-NUMERICAL (aplus-research IC-3/IC-4) | REFERENCED | BLOCK |
| IC-13 corpus scoping | deep mode requires ≥80% (min 20) of numerical/quoted claims grep-verified against retrieved source corpus | INV-RESEARCH-IC13-CORPUS (aplus-research IC-13) | REFERENCED | BLOCK |
| Cross-section ID reconcile | citations/institutions/compound IDs/regulatory dates/trial registrations agreeing across 2+ section drafts (T-Sched-III date, IGF-1 study IDs) | INV-RESEARCH-CROSS-SECTION-ID (Phase 4.25 ID-Reconcile gate) | REFERENCED | BLOCK |
| Composed-harm trajectory | a multi-hormone stack or cross-axis sequence (GH+insulin+T inherits insulin H1; levothyroxine-into-undiagnosed-AI) is detected and hard-blocked as a trajectory, not evaluated turn-by-turn, inheriting the worst-component H-class | `scripts/audit-specialist-profile.sh --check composed-harm-trajectory` (expected; not yet implemented) | PROPOSED | (deferred per §18) |
| Assay-artifact screen | the body requires assay-artifact screening (biotin/direct-free-T/sensitive-E2/CBG/insulin-assay) BEFORE any panel interpretation rule | `scripts/audit-specialist-profile.sh --check assay-artifact-screen` (expected; not yet implemented) | PROPOSED | (deferred per §18) |
| Optimization-without-indication | the body refuses optimization-without-indication and targets mid-range age-appropriate IGF-1 (U-shaped mortality), not maximal — no "normal but want it higher" reasoning path | `scripts/audit-specialist-profile.sh --check optimization-without-indication` (expected; not yet implemented) | PROPOSED | (deferred per §18) |

**Binary verifiable:** row count ≥3 (12 present); every row has a status tag; both LIVE paths resolve (`scripts/audit-specialist-profile.sh`, `.claude/hooks/enforce-role-inlining.sh` — verified present); every REFERENCED row cites an INV-* ID present in INVARIANTS.md (INV-ROLE-INLINING + the 6 INV-RESEARCH-* all present at INVARIANTS.md L35–L41); every PROPOSED row (3) also appears in §18.

---

## 16. Invariants at Risk

Scope: Format/Document + Process + Role-discipline + **Research-domain**. Unlike a non-research specialist, the endocrine-specialist DISPATCHES `aplus-research --mode=deep --target-class=compound` (R17; `templates/specialist-risk-class.yaml` endocrine row), so the Research-domain INV-RESEARCH-* set IS in scope (template §16 disposition: "Only specialist roles that dispatch `/aplus-research` … include Research-domain INV-* in scope"). The active register has 12 invariants (INVARIANTS.md); the in-scope subset for this research-dispatching specialist is the Role-discipline + all 6 Research-domain entries, plus the Process branch-hygiene entry insofar as the profile's wiki-writes commit.

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-ROLE-INLINING | Strengthens | The design doc + deployed profile inline the full 11-section profile; gated by `.claude/hooks/enforce-role-inlining.sh` and the specialist-profile audit |
| INV-RESEARCH-ATTESTATION | Could-move-toward-violation | The role dispatches deep aplus-research; if it self-attested a gate verdict instead of citing the dispatched-agent output (PF-S2-01/PF-S3-01), the attestation chain breaks — guarded by Core Rules + `lib/gate_attest.py` |
| INV-RESEARCH-POPULATION-MISMATCH | Could-move-toward-violation | IGF-1/cancer and DHEA evidence is mechanism/animal-sourced (Finding 9, Finding 15); an untagged animal/in-vitro numerical claim violates it — the role must emit `[population-mismatch: <species>]` |
| INV-RESEARCH-CONCENTRATION-SURFACED | Could-move-toward-violation | Hormone-"optimization" literature is single-clinic/sponsor-concentrated and the IGF-1/cancer signal is prostate-concentrated (Finding 15); ≥70% share without a first-class concentration section violates it |
| INV-RESEARCH-NO-VENDOR-NUMERICAL | Could-move-toward-violation | TRT-clinic/practitioner dose-ranges are vendor-class (Finding 15, domain-research consolidated gaps); a vendor/anecdote tag in the same sentence as a dose/effect-size claim violates it |
| INV-RESEARCH-IC13-CORPUS | Could-move-toward-violation | Deep-mode hormone research must grep-verify ≥80% (min 20) numerical/quoted claims against the retrieved corpus; under-verification violates it |
| INV-RESEARCH-CROSS-SECTION-ID | Could-move-toward-violation | Multi-section hormone research (5 axis sections) must reconcile shared entities (T Schedule-III date, IGF-1 study IDs) before outline refinement; a mismatch violates it |
| INV-BRANCH-NOT-MAIN | No effect | The role's wiki-writes commit on feature branches via session lifecycle owned by the orchestrator; the profile itself performs no main-branch commit |

**Binary verifiable:** scope line states all four categories incl Research-domain with rationale (dispatches aplus-research); every in-scope invariant per the scope criterion is addressed; each row has INV-ID + risk-type + mechanism; out-of-scope categories (Format/Document INV-HO-*; Process INV-SCOPE-CONTRACT/INV-PF-ATTESTATION — session-lifecycle, not specialist-runtime) are not enumerated.

---

## Drafter completion note (to orchestrator/synthesizer)

- **Status:** assigned sections drafted (§1, §2, §4, §13, §16).
- **Pass-1 anchor check:** every section cites ≥1 Finding/R#/WIKI row (§1: F1/F7/F12/F14 + WIKI rows; §2: F1–F18 + WIKI row; §4: F3/F9/F12/F14/F18 + CB §10; §13: F9/F11/F12/F15 + INV-* ; §16: F9/F15 + INV-*).
- **§13 mechanical-check status:** 2 LIVE paths verified present (`scripts/audit-specialist-profile.sh`, `.claude/hooks/enforce-role-inlining.sh`); 7 REFERENCED rows each cite an INV-* present in INVARIANTS.md; 3 PROPOSED rows.
- **PROPOSED rows to surface in §18 (flag for §18 drafter):** EC-COMPOSED-HARM-TRAJECTORY, EC-ASSAY-ARTIFACT-SCREEN, EC-OPTIMIZATION-WITHOUT-INDICATION — each as `scripts/audit-specialist-profile.sh --check <name>`, non-gating, follow-up-bead at close.
- **Decisions/assumptions:** (1) §4 authored INBOUND-only per template directionality (specialist authoring order) — assumption stated inline. (2) §16 includes Research-domain INV-* because the endocrine-specialist dispatches aplus-research (deep/compound), distinct from the 13 non-research specialists. (3) Refusal-class set = the same 5 the peptide/labs siblings encode (PRESCRIPTIVE / PATIENT_FACING / TIME_CRITICAL / BASIS_NOT_REVIEWABLE / AUTHORITY_FRAMING_BYPASS); TIME_CRITICAL added over the peptide set because Finding 5 makes endocrine emergencies (thyroid storm, adrenal crisis, severe hypoglycemia) a first-class symptom-cluster short-circuit.
- **Blockers:** none.
