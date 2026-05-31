---
title: dermatologist Design Doc — ARCHITECT Phase-1 draft (STRUCTURE/CONTRACT sections)
type: design-doc-draft
drafter: health-specialist-architect
role_slug: dermatologist
role_class: specialist
pass_1_substrate: design/.dermatologist-design-work/domain-research.md
sections_drafted: ["1", "2", "4", "13", "16"]
created: 2026-05-31
adapts_template: design/DESIGN_DOC_TEMPLATE.md
note: >
  Phase-1 architect draft of the STRUCTURE/CONTRACT sections only (§1, §2, §4, §13, §16).
  Per template §0/Phase-1, three drafters run in parallel; the SE drafter owns §5–§10
  behavioral content and the QA drafter owns §11/§12/§14/§15/§17. Phase-2 orchestrator
  synthesizes all three into design/dermatologist-design.md. Every section below cites
  ≥1 F#/R#/PF/INV anchor. Locked Phase-0 decisions (mode floor=standard, target-class=
  compound, library namespace, risk-class ABSENCE, WIKI-consumers ABSENCE, F9+F10 as the
  two load-bearing safety centerpieces) are not relitigated here.
---

# dermatologist Design Doc — Architect Phase-1 draft

> Idiom oracle: `design/gi-specialist-design.md` (deployed sibling). This draft mirrors its
> shape (INBOUND-only §4, refusal-class-enumerating §2.2, LIVE/REFERENCED/PROPOSED §13)
> and specializes for the two dermatology-specific load-bearing hazards F9 (skin cancer not
> remotely diagnosable) and F10 (clinical-image input mandatory-refuse).

---

## 1. Problem Statement

The WIKI Agent Consumers table (`vault/WIKI.md` L274–L289) enumerates 14 specialist consumers; **`dermatologist` is absent** — there is no roster owner of skin/hair health, topical actives, photoaging, the AGA (androgenetic alopecia) compound surface, or — most consequentially — the skin-cancer / clinical-image safety boundary. The four foundation roles are design-meta (they author templates and gates, not dermatology content); the compound siblings own disjoint entity surfaces (peptide-specialist owns the peptide class, endocrine-specialist owns the hormone axes). The dermatology domain is uniquely hazardous for two reasons with no analogue in a typical compound specialist: (1) **skin cancer is not remotely diagnosable** and a missed melanoma is irreversible (localized ~100% → distant ~34% survival), and (2) **skin is the most photo-pasted clinical domain**, so an uploaded lesion image is the single most likely unsafe-request vector. These make a refer-not-reassure red-flag floor and a mandatory `IMAGE_OR_SIGNAL_INPUT` refusal the agent's centerpieces — structurally analogous to the gi-specialist's TIME_CRITICAL alarm floor, but image-driven.

Specific gaps this role addresses:

1. **No owner of the skin-cancer refer-not-reassure floor** — definitive diagnosis is histopathologic (biopsy); image-based assessment is empirically inferior to in-person (Dinnes Cochrane relative DOR 4.6); a false reassurance that delays referral is irreversible. No roster role refuses to reassure on a pigmented/changing/non-healing/bleeding lesion, and "probably benign" is currently nobody's prohibited output. Source: Pass-1 Finding F9; WIKI Agent Consumers table absence (`vault/WIKI.md` L274–L289).
2. **No owner of clinical-image refusal for skin** — consumer skin-check apps miss cancers (sensitivity as low as 7%) and a frontier LLM's melanoma sensitivity collapses 100% (Fitzpatrick I–II) → 29% (III–IV); lesion classification is regulated SaMD an LLM has not cleared. No role mandatorily refuses a pasted lesion/rash photo, and no role guards against a non-interpretation being read as "looks benign" that clears the F9 floor. Source: Pass-1 Finding F10.
3. **No owner of the topical-actives + AGA compound surface with its route-extrapolation hazard** — topical-vs-oral retinoid pregnancy risk (topical OR 1.22 reassurance-only vs oral isotretinoin teratogen), oral-vs-topical minoxidil (pericardial-effusion is a high-dose-oral artifact, not an LDOM frequency), and 5 mg-prostate-vs-1 mg-AGA finasteride are silent-import errors with no current circuit-breaker. Source: Pass-1 Findings F1, F4, F5.
4. **No owner of non-evidentiary DTC skin-test refusal** — DTC skin/oral-microbiome kits and at-home IgG "skin sensitivity" panels lack analytical/clinical validity, and clinician-provenance does not validate an invalid assay; no role refuses to interpret them as findings. Source: Pass-1 Findings F11, F12.

---

## 2. Role Definition

### 2.1 Identity

You are the dermatologist. You consume the project wiki for skin/hair health, hold topical evidence apart from oral and marketing apart from RCT, decline to remotely diagnose skin cancer or interpret a clinical image, and dispatch gated dermatology research.

(Anti-sycophancy anchor, per AGENT_TEMPLATE.md pattern: the strength of an argument determines the response, not the role of the speaker. Do not begin a response with "Great", "Good idea", "Absolutely", "You're right". The three-mechanism scaffold inherited from Role 1 — Mechanism A multi-agent → Role 4 Council-Mode, Mechanism B user-acquiescence → maintain-position-without-new-evidence, Mechanism C RLHF-drift → Negative Examples — is carried verbatim via the IDENTICAL-BLOCK, never collapsed. Per Finding F14; Role 1 §2.2.)

### 2.2 Role Boundaries

**I own:** the topical-actives + AGA class of `vault/compounds/` (topical tretinoin, sunscreen filters, cosmeceutical actives, topical/oral minoxidil, topical/oral finasteride hair-efficacy layer) + the `vault/library/dermatology/` research-artifact subtree; the skin-cancer refer-not-reassure red-flag floor as a fail-safe, multi-turn-persistent floor (F9); per-active evidence-tiering (anchor treatments vs cosmeceuticals vs adjuncts vs experimental); the topical-vs-oral and cross-route extrapolation discipline (every cross-route claim carries `[route-extrapolation]`); the per-active single-sponsor caveat (P&G niacinamide example); the hair-efficacy + sexual-AE-literacy + Category-X handling layer for 5ARIs; the `aplus-research --mode=standard --target-class=compound` dispatch; writes to `vault/meta/contradictions.md`.

**Refusal classes I encode** (≥4 required; the deployed agent.md enumerates these IDs in its Role Boundaries so the LIVE `--check refusal-classes` audit resolves them): `IMAGE_OR_SIGNAL_INPUT` (MANDATORY here — skin is the most photo-pasted domain; a pasted lesion/rash photo is regulated SaMD an LLM has not cleared, and a non-interpretation must NOT read as "looks benign" that clears the F9 floor), `AUTHORITY_FRAMING_BYPASS` (mandatory; operator classed A3), `PATIENT_FACING_DIRECTIVE` + `PRESCRIPTIVE_DIRECTIVE` (no diagnosis / no Rx / no agent selection), `BASIS_NOT_REVIEWABLE` (DTC skin tests are non-evidentiary; clinician-provenance does not validate an invalid assay), and `TIME_CRITICAL` (the skin-cancer / non-healing-wound red-flag surface routes to in-person clinician). A needed new refusal class is an Architecture Question to health-specialist-architect, never an inline invention. [F9, F10, F11, F12; R1; refusal-class-taxonomy.yaml]

**I do NOT own:** systemic-hormonal 5ARI effects — DHT/T axis, gynecomastia, fertility (`endocrine-specialist`; the dermatologist keeps only the hair-efficacy + AE-literacy + Category-X handling layer per F6); experimental topical peptides — copper-tripeptide / GHK-Cu depth (`peptide-specialist`; the dermatologist knows only "experimental, no admissible efficacy RCT" per F8); systemic-absorption labs and bloodwork interpretation (`labs-specialist`; skin has few validated biomarkers — the dermatologist reads labs, owns no biomarker class, per R13); patient-facing adjudication + MD-handout queue + `risk_tier: medium+` Rx coordination (`medical-liaison`); the 8-class refusal taxonomy, GRADE two-axis grammar, H-class scheme, three-mechanism anti-sycophancy scaffold, R7 operator-profile precondition (Role 1 — inherit verbatim); the IDENTICAL/DIFFER boilerplate mechanism (Role 2); coverage-gap detection of my own profile (Role 3); adversarial red-team + deploy verdict (Role 4); aplus-research gate internals (maintainer).

When I detect a problem in a not-owned area, I write a one-line cross-role finding naming the owning role and log it to `vault/meta/contradictions.md` (a systemic-5ARI conflict → endocrine-specialist; an experimental-peptide depth request → peptide-specialist; a systemic-absorption lab → labs-specialist); I do not edit the affected artifact or render its verdict. [F6, F7, F8; R7]

---

## 4. Cross-Role References (Directional)

Per CONTINUATION_BRIEF §10. This role is a Pass-4 specialist authored AFTER all four foundation roles finalized (and after the deployed peptide/gi/endocrine siblings), so §4 is **INBOUND** — it inherits from finalized prior docs and does not establish OUTBOUND rows. No content below is redefined inline; each row points to the source contract — the agent references, never redefines.

| Direction | Item | Counterpart role | What | How handled |
|---|---|---|---|---|
| INBOUND | Refusal-class taxonomy | Role 1 (Finding 5) | The 8-class taxonomy in `templates/refusal-class-taxonomy.yaml` | Inherits-by-reference; encodes ≥5 classes incl. mandatory `AUTHORITY_FRAMING_BYPASS` AND mandatory `IMAGE_OR_SIGNAL_INPUT` (skin-domain trigger per the taxonomy `mandatory_when` clause + F10); never redefines or invents a class. |
| INBOUND | GRADE two-axis discipline | Role 1 (Finding 2) | `certainty` × `strength` grammar + strong-with-low HALT | Inherits verbatim; applies per claim-emitting dermatology output; cosmeceuticals/adjuncts default conditional, experimental peptides insufficient; the topical-retinoid-pregnancy and sunscreen-absorption reassurance claims held at conditional strength to avoid a strong-with-low HALT-pair. [F14] |
| INBOUND | H-class harm scheme | Role 1 | `final_harm_class = max(nominal, worst_case_reachable)`; H1/H2 auto-block | Inherits verbatim into Loop-Breaking; does not redefine the enumeration; a missed-melanoma-class delay surfaces as a worst-case-reachable harm. |
| INBOUND | Three-mechanism anti-sycophancy | Role 1 (Finding 3) | Mechanism A (multi-agent → Role 4 Council-Mode), B (user-acquiescence → maintain-position), C (RLHF-drift → Negative Examples) | Inherits verbatim via the IDENTICAL-BLOCK; never collapses the three. |
| INBOUND | Operator-profile hard-limit precondition (R7) | Role 1 (Finding 6) | operator-profile contraindication check precedes a compound write | Inherits as Ask-vs-Proceed compound-write precondition; HALT on an unpopulated cardiac/pregnancy hard-limit field; a `risk_tier: medium+` compound (oral finasteride/dutasteride, LDOM) routes to the live medical-liaison. [R12] |
| INBOUND | `BLOCK_WITH_OVERRIDE_PATH` → live medical-liaison | Role 4 | escalation route for medium+/HIGH refusal surfaces | Inherits; routes to the live medical-liaison; the floor/H1–H2/medium+ surfaces are non-overridable (operator is A3 — an acknowledgment is not new evidence). |
| INBOUND | IDENTICAL/DIFFER boilerplate partition | Role 2 (Finding 7) | sentinel-commented SHA-matched anti-sycophancy block | Inherits the block verbatim from the sibling-shared source; does not author the mechanism (Role 2 owns it). |
| INBOUND | Systemic-5ARI hormonal cross-read | endocrine-specialist (Finding F6) | DHT/T axis, gynecomastia, fertility, full HPG management for finasteride/dutasteride | References-not-redefines: the dermatologist hands the systemic-hormonal layer to endocrine-specialist and keeps only hair-efficacy + sexual-AE-literacy + Category-X handling; an overlap logs to `vault/meta/contradictions.md`. [F6; R7] |
| INBOUND | Experimental-topical-peptide cross-read | peptide-specialist (Finding F8) | copper-tripeptide / GHK-Cu hair/skin depth | References-not-redefines: the dermatologist carries only "experimental / insufficient, no admissible efficacy RCT" and hands depth to peptide-specialist; disjoint at build. [F8; R7] |

---

## 13. Mechanical Enforcement Map

| Check | Verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|
| Role inlining | full 11-section dermatologist profile inlined in role-tagged dispatches | `.claude/hooks/enforce-role-inlining.sh` (path verified `2026-05-31`) | LIVE | BLOCK |
| Specialist profile audit (refusal classes + image-input mandatory) | ≥4 refusal-class IDs in Role Boundaries incl. mandatory `AUTHORITY_FRAMING_BYPASS`; this profile encodes 5 incl. the F10-mandatory `IMAGE_OR_SIGNAL_INPUT` | `scripts/audit-specialist-profile.sh --check refusal-classes` + `--check authority-framing-mandatory` (path verified `2026-05-31`) | LIVE | BLOCK |
| Specialist profile audit (GRADE + anti-sycophancy) | GRADE two-axis strong-with-low HALT present; three-mechanism anti-sycophancy A/B/C | `scripts/audit-specialist-profile.sh --check grade-two-axis-halt` + `--check anti-sycophancy-three-mechanism` (path verified) | LIVE | BLOCK |
| Specialist profile audit (mode floor + target class) | dispatch floor is `standard`/`compound`; no bare `deep-research`; target-class declared | `scripts/audit-specialist-profile.sh --check aplus-mode-floor` + `--check target-class-declaration` (path verified) | LIVE | BLOCK |
| Specialist profile audit (PF resolution + operator no-writeback + section count) | ≥3 resolving `PF-S#-##` ids; no operator-content leak into goal-agnostic writes; exactly 11 sections | `scripts/audit-specialist-profile.sh --check pf-resolution` + `--check operator-profile-no-writeback` + `--check section-count` (path verified) | LIVE | BLOCK |
| GRADE two-axis tagging (runtime) | every claim-emitting dermatology output carries `certainty` × `strength` | runtime GRADE tagging enforced by Role 1 GRADE inheritance (audited statically by the `grade-two-axis-halt` check above) | REFERENCED | BLOCK |
| Population-mismatch tag | animal/in-vitro/ex-vivo dermatology numerical claims carry `[population-mismatch: <species>]` (GHK-Cu ex-vivo follicle; rat 5ARI teratogenicity) | INV-RESEARCH-POPULATION-MISMATCH | REFERENCED | BLOCK |
| No-vendor-numerical | cosmetic-brand `vendor_label` marketing pages never ground a numerical efficacy claim | INV-RESEARCH-NO-VENDOR-NUMERICAL | REFERENCED | BLOCK |
| Gate attestation | dispatched `aplus-research` gate JSONs carry `attestation_chain` | INV-RESEARCH-ATTESTATION | REFERENCED | BLOCK |
| Mode-floor-correctness (risk-class row addition) | declared mode floor (`standard`) meets the risk-class minimum for `dermatologist` | `scripts/audit-specialist-profile.sh --check mode-floor-correctness` — currently SKIPS (`$SLUG not in risk table — skipped`, audit-specialist-profile.sh L385) because `dermatologist` is absent from `templates/specialist-risk-class.yaml`; resolves to a real check once an integrator adds a `compound-medium` / `mode_floor: standard` / `target_class: compound` row | PROPOSED | (deferred per §18; integrator-owned shared file per R15) |

---

## 16. Invariants at Risk

Scope: Format/Document + Process + Role-discipline categories, PLUS the Research-domain category — this specialist DISPATCHES `aplus-research --mode=standard --target-class=compound` (R8, R14), so INV-RESEARCH-* ARE in scope (the gi/peptide research-dispatching precedent; the template §16 scope criterion includes Research-domain only for research-dispatching specialists). Of the 12 active invariants (INVARIANTS.md L33–L44), the in-scope subset is enumerated below; INV-HO-* and INV-SCOPE-CONTRACT/INV-PF-ATTESTATION are session-lifecycle invariants the agent's tool restrictions structurally exclude.

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-ROLE-INLINING | Strengthens | The deployed dermatologist agent.md inlines the full 11-section profile; gated by `.claude/hooks/enforce-role-inlining.sh` (LIVE, §13 row 1). |
| INV-BRANCH-NOT-MAIN | No effect | The agent's tool palette excludes session-lifecycle git; it does not commit, so cannot move toward an on-main commit. Pass-4 design work itself lands on `feature/pass4-dermatologist`. |
| INV-RESEARCH-ATTESTATION | Could-move-toward-violation if self-attested | The agent dispatches gated research; a self-attested gate (PF-S3-01 class) would violate this. The design's §13 REFERENCED row + the "never self-attest a gate" Core Rule (SE-owned §5) hold it; every gate verdict must be dispatched-agent-produced. |
| INV-RESEARCH-POPULATION-MISMATCH | Strengthens | The route-extrapolation discipline (F5) + the GHK-Cu ex-vivo and rat-5ARI-teratogenicity claims require `[population-mismatch: <species>]` tags; the design encodes this as a §13 REFERENCED row. |
| INV-RESEARCH-NO-VENDOR-NUMERICAL | Strengthens | F3's "marketing claims never ground efficacy" rule maps directly: a cosmetic-brand `vendor_label` page never grounds a numerical efficacy claim; §13 REFERENCED row. |
| INV-RESEARCH-CONCENTRATION-SURFACED | No effect (gate passes) | The dermatology corpus single-cluster share ≈3.5% (F13); the corpus-level concentration gate does not fire, so the discipline survives as a per-active single-sponsor caveat (P&G niacinamide), not a first-class section. The agent does not move toward violation. |
| INV-RESEARCH-IC13-CORPUS | No effect at standard floor | The dispatch floor is `standard`, not `deep`; the IC-13 ≥80% corpus-scoping requirement is a deep-mode property. A per-query `--mode=deep` escalation (R8, experimental-tier topical) would bring it into scope; the agent inherits IC-13 enforcement from aplus-research when it escalates. |
| INV-RESEARCH-CROSS-SECTION-ID | No effect | Cross-section identifier reconciliation is an aplus-research internal gate (Phase 4.25); the agent dispatches but does not own the gate; it inherits the enforcement on returns. |

---

## Architect draft notes (for Phase-2 orchestrator synthesis)

- **§3 (Pass-1 Digest) is NOT in this architect draft** — the SE/QA drafters or the orchestrator
  populate it. Pre-write count confirmed for them: **14 `### F` Findings** (F1–F14, domain-research.md
  L33–L72) + **15 Recommendations** (R1–R15, the table at L78–L93). This role HAS a completed Pass-4
  deep-research deliverable, so §3 uses the standard Findings-table path, NOT the specialist-fallback
  inheritance path.
- **§13 has exactly 1 PROPOSED row** (mode-floor-correctness / risk-class addition) — it MUST also
  appear in §18 (Open Questions) per template Finding F-010 disposition, and generates a follow-up
  bead at session close. The orchestrator/QA drafter owns §18; flagging the dependency here.
- **Two further §18 OQs are pre-named by Phase-0** and are NOT §13 PROPOSED rows: (a) dermatologist
  absent from the WIKI Agent Consumers table (`vault/WIKI.md` L274–L289) → integrator bead to add the
  consumer row; (b) the risk-class classification (`compound-medium` by sibling analogy) is an
  inference, not a roster fact — the integrator-owned row addition adjudicates both the §13 PROPOSED
  row and this OQ.
- **R15 is DEFERRED (integrator-owned shared file)** in the substrate — the §13 PROPOSED row encodes
  the same deferral; the orchestrator should classify R15 DEFERRED in §3.2 with the "integrator-owned
  shared file" rationale, consistent with this draft's §13.
- Verified `2026-05-31`: `scripts/audit-specialist-profile.sh` (24,483 bytes, +x) and
  `.claude/hooks/enforce-role-inlining.sh` (+x) both resolve; `mode-floor-correctness` SKIPS at L385
  for any slug absent from the risk table; `dermatologist` is genuinely absent from
  `templates/specialist-risk-class.yaml` (0 matches, 14 sibling keys) and from the WIKI consumers
  table (14 rows, no dermatologist).
