---
title: dermatologist — Phase-0 Domain Research (synthesis)
type: domain-research
role_slug: dermatologist
role_class: specialist
mode: standard
target_class: compound
status: synthesized
created: 2026-05-31
pipeline: aplus-research (mode=standard) — design-research dispatch, lands in design-work NOT vault (PF-S2-04)
gates: gate-2.75 PASS; gate-3.5 PASS (3 sections, iter-2 convergence); gate-4.75 PASS (attested, verify-chain intact)
sources: sections/section-A.md (15 primaries), section-B.md (20+ primaries), section-C.md (12 primaries)
---

# dermatologist — Phase-0 Domain Research (synthesis)

Goal-agnostic library knowledge to ground the design of the `dermatologist` medical sub-agent in the a-plus-maxing project. Domain: skin / hair health, topical actives, photoaging, common dermatologic conditions at a literacy level, and the skin-cancer / clinical-image safety boundary. This synthesis reads ONLY the validated section corpus (`sections/section-{A,B,C}.md`), which passed the Phase-3.5 judge gate (iter-2 convergence after 3 real citation-fidelity defects were caught + fixed) and the Phase-4.75 integrity gate (attested, `verify-chain` intact). Per PF-S2-04 this is library research: the meta files load for linkage but are NOT injected; no operator personalization. Section line/citation references point into the corpus for traceability.

## 0. Evidence-landscape overview

The dermatology compound domain splits cleanly by evidence maturity, and that split is the design's organizing principle:

- **High-certainty / strong** — topical tretinoin (photoaging + acne), broad-spectrum sunscreen (photoaging prevention; SCC prevention), oral finasteride 1 mg and topical minoxidil for male AGA. These rest on Cochrane reviews, network meta-analyses, and pivotal RCTs (section-A [2], [8]; section-B [10], [3]).
- **Low–moderate / conditional** — cosmeceutical actives (niacinamide, topical vitamin C, AHA/BHA, ceramide/barrier moisturizers) and AGA adjuncts (ketoconazole, microneedling, LLLT, PRP). Small, heterogeneous, sometimes single-sponsor RCTs.
- **Experimental / insufficient** — topical research peptides (copper peptides / GHK-Cu), which are the peptide-specialist's domain at build (overlap boundary).

Two facts dominate the SAFETY design and have no analogue in a typical compound specialist: (1) **skin cancer is not remotely diagnosable** and the cost of a missed melanoma is irreversible, and (2) **skin is the most photo-pasted clinical domain**, so an uploaded lesion image is the single most likely unsafe-request vector. These make `IMAGE_OR_SIGNAL_INPUT` and a refer-not-reassure red-flag floor the dermatologist's centerpieces — structurally analogous to the gi-specialist's TIME_CRITICAL alarm floor, but image-driven.

Concentration audit (Phase-4.75): single-cluster share ≈ 3.5% across 57 distinct primaries — the dermatology literature is NOT single-lab-dominated (unlike BPC-157's ~76% Sikiric share). The only industry-sponsor concentration (Procter & Gamble, niacinamide) is surfaced per-active with a certainty downgrade. So the concentration gate passes, and the discipline survives as a per-active caveat rule rather than a corpus-level dominance section.

## 1. Findings

### F1 — Topical retinoids are the best-evidenced dermatology active, but the topical-vs-oral pregnancy distinction is a load-bearing reasoning hazard
Topical tretinoin improves photoaging (Cochrane 30-trial review, dose-dependent for both efficacy AND irritation) and acne (network meta-analysis n=18,089; adapalene+BPO top-ranked) at **certainty: high, strength: strong** (section-A [1], [2], [4], [5]). But topical-retinoid first-trimester exposure shows **no significant malformation increase (OR 1.22, 95% CI 0.65–2.29)** — adequate to *reassure* after inadvertent exposure, underpowered to *justify* deliberate use (section-A [6]). This is categorically NOT oral isotretinoin (a potent human teratogen, iPLEDGE-regulated). Conflating topical and oral retinoid pregnancy risk is a named reasoning error the agent must not make. AGENT_TEMPLATE: Core Rules.

### F2 — Sunscreen is the only photoaging-PREVENTION active with RCT proof; filter systemic-absorption is a data-gap signal, NOT evidence of harm
The Nambour RCT (n=903, 4.5 yr) showed daily sunscreen produced **24% less skin aging (relative odds 0.76, 95% CI 0.59–0.98)** and reduced SCC (not BCC) (section-A [8], [9]) — **high/strong** for photoaging prevention. The FDA maximal-use RCT found four organic filters exceeded the 0.5 ng/mL plasma threshold, but the authors explicitly state this "does not indicate that individuals should refrain from the use of sunscreen" — a regulatory toxicology-trigger, not a harm endpoint (section-A [10], [11]). The agent must present absorption as a **data-gap (low certainty, conditional)**, never as a reason to avoid sunscreen. AGENT_TEMPLATE: Core Rules, Negative Examples.

### F3 — Cosmeceutical actives are low–moderate certainty / conditional, and marketing claims never ground efficacy
Niacinamide, topical vitamin C, AHA (glycolic/lactic), salicylic acid, and ceramide/barrier moisturizers each have positive but small, formulation-dependent RCTs (section-A [11b], [13], [14], [15], [16]). The niacinamide anchor RCT is P&G-sponsored — a **single-sponsor dominance caveat with certainty downgrade** (section-A [11b], A.4). Cosmetic-brand marketing pages are `vendor_label` and may never ground a numerical efficacy claim. Default disposition for cosmeceuticals: **conditional strength**. AGENT_TEMPLATE: Core Rules, Tools (type-tag discipline).

### F4 — AGA treatment is anchored by topical minoxidil + oral finasteride (men); female and route results do NOT transfer
Topical minoxidil 5% (OTC) and oral finasteride 1 mg (Rx) are **high/strong for male AGA** (section-B [3], [10]: finasteride +107/+138 hairs vs placebo). Critical non-transfer rules: (a) finasteride 1 mg is **ineffective in postmenopausal women** (Price RCT negative — section-B [14]); (b) most pivotal AGA RCTs are **male-only or sex-arm-restricted** (Kaufman, Olsen, Eun) — magnitudes do not generalize across sex (section-B [10], [12], [13], [5]). AGENT_TEMPLATE: Core Rules, Edge Cases.

### F5 — Route-extrapolation is the dominant integrity hazard in the hair domain
The pericardial-effusion / fluid-retention warning is an **antihypertensive-dose oral-minoxidil** artifact (multi-mg–tens-of-mg) and was NOT observed at low-dose-oral-minoxidil (LDOM) hair doses in pooled data — importing its frequency to LDOM is an error (section-B [7], [6]). Likewise topical finasteride lowers but does NOT eliminate systemic DHT suppression (section-B [20]), and the PCPT prostate-cancer framing is a 5 mg / older-men signal not transferable to 1 mg AGA use. Every cross-route claim carries `[route-extrapolation]`. AGENT_TEMPLATE: Core Rules, Anti-Patterns.

### F6 — 5ARI systemic-hormonal effects are the endocrine-specialist's domain; the dermatologist owns the hair-efficacy + AE-literacy + Category-X handling layer
Finasteride/dutasteride systemic hormonal management (DHT/T axis, gynecomastia, fertility) hands off to endocrine-specialist (section-B B.2). The dermatologist keeps: hair efficacy, the **sexual-dysfunction AE literacy** (RCT meta RR 1.57; finasteride RR 1.66; dutasteride RR 1.37 NS — section-B [15]), the **Category-X pregnancy/handling precaution** (no handling crushed tablets — section-B [9] `[population-mismatch: rat]` on the animal teratogenicity), **PFS framed as real-reports / contested-causation / low-certainty** (balanced both-sides — section-B [17], [18]), and the **PCPT high-grade signal paired with its detection-artifact reinterpretation** (section-B [18]). AGENT_TEMPLATE: Role Boundaries, Core Rules.

### F7 — AGA adjuncts are lower-tier; honest evidence-tiering is required
Ketoconazole shampoo (small non-RCT), microneedling (add-on benefit, unstandardized protocols), LLLT (pooled SMD 1.316 but device heterogeneity + industry involvement), and PRP (high heterogeneity, publication bias, no standardized protocol) are **low–moderate certainty, conditional** (section-B [21]–[24]). The agent must not present adjuncts at the certainty of the anchor treatments. AGENT_TEMPLATE: Core Rules.

### F8 — Experimental topical peptides (GHK-Cu) are the peptide-specialist's domain (overlap boundary, disjoint at build)
Copper-tripeptide hair/skin evidence is preclinical (`in_vitro` / ex-vivo, `[population-mismatch: human ex-vivo follicle / cultured cells]`), no Tier-1 AGA RCT (section-B [25]). Disposition: **experimental / insufficient**; the dermatologist knows only "experimental, no admissible efficacy RCT" and hands depth to peptide-specialist. AGENT_TEMPLATE: Role Boundaries.

### F9 — (LOAD-BEARING) Skin cancer is NOT remotely diagnosable; "probably benign" is a prohibited, high-harm output
Definitive diagnosis is **histopathologic (biopsy)**; best clinical triage is **in-person dermoscopy**; image-based assessment is **empirically inferior to in-person** (Dinnes Cochrane relative DOR 4.6, 95% CI 2.4–9.0; section-C [2]). The melanoma survival cliff — **localized ~100% → distant ~34%** (SEER; section-C [3]) — makes a false reassurance that delays referral an irreversible error. ABCDE + ugly-duckling + non-healing/bleeding/changing lesions are **recognition prompts, not a diagnostic test** (section-C [7], [8]). Design rule: a **refer-to-in-person-clinician red-flag floor** that refuses to reassure, persists across turns, and is fail-safe. This is the dermatologist's critical floor. AGENT_TEMPLATE: Core Rules, Ask vs Proceed, Loop-Breaking.

### F10 — (LOAD-BEARING) Clinical-image input must be REFUSED — lesion classification is regulated SaMD, and a general LLM is unsafe and skin-tone-biased
Consumer skin-check apps miss cancers (**sensitivity as low as 7%**; at review time none had FDA approval, only CE marking the authors called inadequate — section-C [1]); "dermatologist-level" CNN results (Esteva) were obtained on **curated biopsy-proven images, not consumer photos** (section-C [9]); and a frontier LLM's melanoma sensitivity **collapses from 100% (Fitzpatrick I–II) to 29% (III–IV) / 43% (V–VI)** — an equity failure exactly where melanoma is already under-detected (section-C [10]). Skin-lesion classification is SaMD subject to regulatory clearance; an un-validated LLM is definitively not a diagnostic device. Design rule: **`IMAGE_OR_SIGNAL_INPUT` is MANDATORY** for the dermatologist, and a non-interpretation must NOT read as "looks benign" that clears the F9 floor. AGENT_TEMPLATE: Role Boundaries, Core Rules, Negative Examples.

### F11 — Common conditions are literacy + OTC-vs-clinician-category only; "looks like X" is outside the boundary
Acne, rosacea, atopic dermatitis, and seborrheic dermatitis each have a guideline-defined OTC self-care envelope and a clinician-only therapeutic layer (section-C [4], [5], [6], [11]). Permitted agent output: literacy-level "what this is" + the OTC-vs-clinician *category* split. NOT permitted: assigning a diagnosis, prescribing, selecting an agent, or saying "looks like X" — any of these conditions can be mimicked by something requiring biopsy (seb derm/lupus, eczema/cutaneous-T-cell-lymphoma). AGENT_TEMPLATE: Core Rules, Role Boundaries.

### F12 — DTC skin tests are non-evidentiary (BASIS_NOT_REVIEWABLE)
DTC skin/oral microbiome kits lack analytical and clinical validity (regulatory/legal analysis — section-C [12]); at-home IgG "skin sensitivity" panels are advised against by allergy societies (IgG reflects exposure, not a clinical trigger); AI "skin-analysis"/skin-age camera apps are cosmetic scoring, not medical tests (section-C C.4). The agent treats DTC skin-test results as **non-evidentiary** and interprets nothing as a finding — a `BASIS_NOT_REVIEWABLE` refusal, and clinician-provenance ("my doctor ordered it") does not validate an invalid assay. AGENT_TEMPLATE: Core Rules, Ask vs Proceed.

### F13 — Evidence concentration is low; the discipline survives as a per-active single-sponsor caveat
Single-cluster share ≈3.5% (largest cluster 2/57 primaries) — no corpus-level dominance section required (gate-4.75 concentration_audit PASS). The one industry-sponsor concentration (P&G niacinamide) is surfaced with a certainty downgrade. Design rule: keep the **per-active single-sponsor caveat** even though the corpus-level gate passes. AGENT_TEMPLATE: Core Rules.

### F14 — GRADE two-axis discipline holds with no strong-on-low-certainty pairs
Every recommendation in the corpus carries `certainty × strength`; cosmeceuticals and adjuncts are held at conditional/weak, experimental peptides at insufficient, and the two safety-sensitive "reassurance" claims (topical-retinoid pregnancy, sunscreen-absorption) are explicitly held at **conditional strength to avoid a strong-with-low HALT-pair** (section-A A.4, section-B B.6). The agent inherits the project GRADE two-axis grammar and the strong-with-low HALT. AGENT_TEMPLATE: Core Rules, Loop-Breaking.

## 2. Recommendations (design implications for the dermatologist agent)

| # | Recommendation | Verdict | Maps to |
|---|---|---|---|
| R1 | Encode ≥4 refusal classes from the canonical taxonomy: **AUTHORITY_FRAMING_BYPASS** (mandatory; operator A3), **IMAGE_OR_SIGNAL_INPUT** (mandatory here — skin = most photo-pasted), **PATIENT_FACING_DIRECTIVE** + **PRESCRIPTIVE_DIRECTIVE** (no diagnosis/Rx), **BASIS_NOT_REVIEWABLE** (DTC tests), **TIME_CRITICAL** (for the skin-cancer/non-healing-wound floor). Never invent a class. | ACCEPTED | F9, F10, F11, F12 |
| R2 | The **skin-cancer red-flag floor** is the agent's critical floor: any pigmented / changing / non-healing / bleeding / ABCDE / ugly-duckling lesion → refer-to-in-person-clinician; refuse-not-reassure; "probably benign" is a prohibited output; floor persists across turns; fail-safe toward referral. | ACCEPTED | F9 |
| R3 | `IMAGE_OR_SIGNAL_INPUT` is mandatory: a pasted lesion/rash photo is refused (regulated SaMD an LLM has not cleared); a non-interpretation must NOT read as "looks benign" that clears R2. | ACCEPTED | F10 |
| R4 | GRADE two-axis (`certainty × strength`) on every claim-emitting recommendation; strong-with-low/very-low → HALT; cosmeceuticals + adjuncts default conditional; experimental peptides insufficient. | ACCEPTED | F14, F3, F7 |
| R5 | Encode the **topical-vs-oral retinoid pregnancy non-conflation rule** (topical OR 1.22 = reassurance-only; oral isotretinoin = potent teratogen). | ACCEPTED | F1 |
| R6 | **Route-extrapolation discipline**: oral-vs-topical minoxidil (pericardial effusion is a high-dose-oral artifact), oral-vs-topical finasteride (DHT partially suppressed topically), 5 mg-prostate-vs-1 mg-AGA — each carries `[route-extrapolation]`; never silently import. | ACCEPTED | F5 |
| R7 | **Cross-read boundaries**: systemic-hormonal 5ARI effects → endocrine-specialist; experimental topical peptides → peptide-specialist; systemic-absorption labs → labs-specialist. Overlaps log to `vault/meta/contradictions.md`; the dermatologist does not render the other domain's verdict. | ACCEPTED | F6, F8 |
| R8 | **Mode floor = `standard`, target-class = `compound`** (dermatologist classed compound-medium by sibling analogy). Escalate `--mode=deep` per-query only for a topical compound that lands at `risk_tier: experimental`. | ACCEPTED | F1–F8 |
| R9 | Keep the **per-active single-sponsor caveat** (P&G niacinamide example) even though the corpus-level concentration gate passes (~3.5%). | ACCEPTED | F13, F3 |
| R10 | **DTC skin-test results are non-evidentiary** → `BASIS_NOT_REVIEWABLE`; clinician-provenance does not validate an invalid assay (`AUTHORITY_FRAMING_BYPASS`). | ACCEPTED | F12 |
| R11 | **Common-conditions output bounded** to literacy + OTC-vs-clinician category; no diagnosis, no Rx, no agent selection; "looks like X" is outside the boundary (biopsy-mimics). | ACCEPTED | F11 |
| R12 | **Operator-profile precondition (R7-class)**: bind operator state at dispatch before any compound write; a `risk_tier: medium+` compound (oral finasteride/dutasteride, LDOM) routes to the live medical-liaison (`BLOCK_WITH_OVERRIDE_PATH`); unpopulated cardiac/pregnancy contraindication field → HALT the write. | ACCEPTED | F4, F6 |
| R13 | **Ownership**: writes the topical-actives + AGA class of `vault/compounds/` + `vault/library/dermatology/`; reads operator/current/goals + biomarkers/labs; no owned dermatology biomarker class (skin has few validated biomarkers — reads labs). WIKI Agent-Consumers row needs adding (integrator). | ACCEPTED | F1–F12 |
| R14 | **No self-attestation / no fabrication** (PF-S2-01/PF-S3-01): dispatch `aplus-research`, never bare `deep-research`; ground every value/dose/cutoff/refusal-class-ID to a whitelisted primary; no gate confirmed without the dispatched-agent artifact. | ACCEPTED | (process) |
| R15 | `dermatologist` is ABSENT from `templates/specialist-risk-class.yaml` → integrator bead to add a `compound-medium` / `mode_floor: standard` / `target_class: compound` row (so `audit-specialist-profile.sh --check mode-floor-correctness` resolves rather than skips). | DEFERRED — integrator-owned shared file | (process) |

## 3. Folded gate dispositions (design-research dispatch)

**Phase 7.5 RISK-FLOOR (folded — no single vault compound entry is written here).** For the medium+/experimental dermatology compounds (oral finasteride, dutasteride, LDOM), the risk-floor fields are **fillable from retrieved sources**, verified in Section B.5: contraindications (Category X for 5ARIs; cardiac / fluid-retention / pregnancy for LDOM — section-B [9], [26]); monitoring (sexual-AE counseling for 5ARIs, with the systemic-hormonal/DHT layer handed to endocrine; CV / edema / hypertrichosis for LDOM — section-B [15], [26]); stopping criteria (edema/effusion → reduce/stop LDOM; persistent sexual AE → stop 5ARI). When the deployed agent later writes an actual `vault/compounds/<slug>.md` at `risk_tier: medium+`, the real risk-floor gate fires (and a third-party monitoring biomarker is required for any `experimental`-tier write).

**Phase 8.5 LAYERS (folded into Section B/C per peptide/gi precedent).** Prescribing-practice layer is satisfied in **Section B.5** — LDOM International Modified Delphi consensus (JAMA Dermatol 2024, section-B [26]), real-world starting doses + titration + splitting (section-B [27]), and compounded-topical-finasteride conventions — all tagged `practitioner_protocol` / `compounding_data_sheet`, grounding dose/route/cycle only, with explicit divergences from RCT dose noted. Non-English literature layer is satisfied in **Section C.5** — explicit confirmed-absence of any admissible non-English PRIMARY that alters the conclusions, with Spanish (Actas Dermo-Sifiliográficas) and Chinese corroboration recorded as non-admissible (`anecdote_aggregate`). No separate vault layer files are written (design-research dispatch).

## 4. Provenance

- Gates: `gates/gate-2.75.json` (SCOPE PASS), `gates/gate-3.5-summary.md` + `judges/judge-{A,B,C}.json` (JUDGE PASS @92, iter-2 convergence; iter-1/iter-2 stamped copies preserved), `gates/gate-4.75.json` + `gates/gate-4.75.md` (INTEGRITY PASS, attested, `verify-chain` intact). Phase-4.25 cross-section identifier reconciliation folded into gate-4.75 IC-10 (no cross-section identifier disagreement — bibliographies are section-scoped, no PMID/DOI spans two sections).
- Corpus: `sections/section-A.md` (15 admissible primaries — retinoids/sunscreen/cosmeceuticals), `sections/section-B.md` (20+ — AGA/hair compounds + prescribing layer), `sections/section-C.md` (12 — conditions/red-flags/image+test validity + non-English survey). Total ~47 distinct primaries pre-dedup; 57 numbered bibliography entries; concentration share ~3.5%.
- Dispatch ledger: `dispatch-ledger.jsonl` (3 retrieval agent_ids recorded).
- Three real citation-fidelity defects were caught by independent dispatched judges and fixed with post-fix grep audits (Boutli F mis-attribution; Lucia-MS-vs-Thompson-IM first author; Dinnes Cochrane figures) — the PF-S2-02/PF-S3-01 discipline working as designed, not orchestrator self-attestation.
