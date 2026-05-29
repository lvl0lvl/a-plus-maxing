---
title: "Peptide-Specialist Medical Agent — Domain Research (Pass-3 Synthesis)"
type: research-report
mode: deep
role_slug: peptide-specialist
role_class: specialist
research_question: "What domain knowledge — pharmacology, regulatory/legal status, prescribing/dosing/safety conventions, and inherited agent-design contracts — must ground the design of a peptide-specialist medical sub-agent that produces goal-agnostic peptide-library knowledge and personalized compound reasoning under the a-plus-maxing safety architecture?"
sub_agents_dispatched:
  - "Section A (pharmacology/landscape) — paired retrieval+judge, iter-2 PASS 99/100"
  - "Section B (regulatory/legality/sourcing) — paired retrieval+judge, iter-2 PASS 99/100"
  - "Section C (prescribing/dosing/safety) — paired retrieval+judge, iter-2 PASS 99/100"
  - "Synthesis (this file) — corpus-read-only, no new retrieval"
  - "Phase-6 critique — to follow"
sources_total: 39
judge_gate: "pass-iter-2 (A/B/C all 99/100)"
generated: 2026-05-29
---

# Peptide-Specialist Medical Agent — Domain Research (Pass-3 Synthesis)

## Executive Summary

A peptide-specialist medical agent must be, above all, an **evidence-maturity discriminator and an extrapolation circuit-breaker** — not a peptide enthusiast with a dose chart. The load-bearing conclusion across the three validated sections is that the popular performance/longevity peptide space is structurally adverse to safe reasoning: the molecular mechanisms are well-mapped (which makes the compounds *sound* credible), but for almost every popular peptide the human-outcome evidence is preclinical, single-lab, or anecdotal, the dose conventions originate from a practitioner-education ecosystem rather than trials, the legal status is "not approved" across every relevant jurisdiction, and the most-cited safety reassurances are rodent toxicology numbers waiting to be silently transferred to a 90 kg human. The agent therefore exists to hold three pairs of facts apart that the surrounding ecosystem constantly conflates: *mechanism vs. human outcome*, *practitioner convention vs. trial evidence*, and *compoundable/removed-from-a-list vs. approved/safe*. This synthesis carries **12 Findings** (A/B/C load-bearing claims plus Section-D agent-design findings grounded in the inherited contract pack) and **15 Recommendations** that become the design-doc §3.2 directive list. The single most important risk is the **animal-to-human extrapolation hazard compounded by single-lab concentration of evidence** (Findings 3 and 4): the canonical case — BPC-157's "100–1000× safety margin" and ">80% of studies from the Sikirić/Zagreb group" — is exactly the shape of claim a sycophantic agent would launder into a human safety endorsement, which maps directly onto the mandatory AUTHORITY_FRAMING_BYPASS refusal class and the risk-floor gate.

---

## §0 Introduction

**Research question.** What domain knowledge must ground the design of a `peptide-specialist` medical sub-agent in the a-plus-maxing project — across pharmacology, regulatory/legal status, prescribing and safety practice, and the project-internal agent-design contracts the specialist inherits — such that the agent produces goal-agnostic, vetted peptide-library knowledge and performs personalized compound reasoning without crossing the project's medical-safety boundaries?

**Scope.** Three domains were researched as goal-agnostic library knowledge (peptides as a therapeutic class, not pre-filtered for operator Walter): (A) the therapeutic-peptide landscape and pharmacology, (B) regulatory status, legality, and sourcing, and (C) prescribing practice, dosing, and safety. A fourth domain (D), agent design, is synthesized here by grounding each agent-behavior conclusion in a named contract from the inherited contract pack rather than introducing new external evidence.

**Methodology.** Three paired retrieval+judge sub-agent dispatches were run at `deep` mode (the peptide-specialist risk_class is `compound-experimental`, whose mode floor is `deep`), each iterated to an iteration-2 judge PASS of 99/100. This document is a **corpus-read-only synthesis**: no new web retrieval was performed, and every numerical or factual claim carried forward already appears, type-tagged, in section-A/B/C, with its `[population-mismatch: <species>]` annotation preserved for any animal/in-vitro number. No new numbers are introduced.

**Key assumptions.** (1) The three section files passed their judge gates and their type-tags are authoritative — this synthesis preserves, never re-derives, them. (2) The contract-pack documents (refusal taxonomy, H-class scheme, GRADE two-axis, anti-sycophancy mechanisms, R7 precondition, escalation routes, wiki-consumption contract) are the binding project-internal interfaces the specialist inherits; Section-D findings reference them by name and do not invent contract semantics. (3) Regulatory state is reported as of the section files' May-2026 retrieval window and is explicitly time-sensitive (Finding 6 in particular).

---

## §1 Findings

### Finding 1 — The peptide landscape stratifies by evidence maturity, not by class; the agent must carry a per-compound maturity rung and never let class membership substitute for compound-level evidence

**Claim.** A peptide's class ("healing peptide," "GH secretagogue") tells you nothing about whether it has ever been studied in humans; the agent must locate every compound on a four-rung maturity ladder (approved → trial-stage → preclinical/animal → anecdote) before reasoning about it.

Only a handful of members hold an FDA-approved indication. Tesamorelin (Egrifta) is FDA-approved (2010) for visceral adiposity in HIV-associated lipodystrophy `[regulatory]`; its pivotal 26-week trial (n=412) showed a 15.2% visceral-adipose reduction vs 5.0% placebo, P<0.001, at 2 mg/day subQ `[rct]` (section-A.md A-1). Bremelanotide (Vyleesi) is FDA-approved (2019) for HSDD in premenopausal women `[regulatory]`, with two RECONNECT phase-3 trials (n=1,247) at 1.75 mg subQ `[rct]` (section-A.md A-1). Tirzepatide produced up to ~22.5% mean weight loss at 15 mg/72 wk `[rct]`, and thymosin-α1 is approved in 35+ countries but NOT in the US `[regulatory]` (section-A.md A-1).

The trial-stage rung holds human data but no approval for the use of interest: retatrutide has phase-2 data only (mean 24.2% weight reduction at 12 mg over 48 weeks `[rct]`), MK-677 has RCT data (fat-free mass +1.1 kg at 12 months but worsened insulin sensitivity and no strength gain `[rct]`, Nass 2008), and AOD-9604's largest phase-2b (OPTIONS) FAILED with development terminated in 2007 — its often-cited n=536/24-week figure is NOT `[rct]`-grounded and is tagged `[corpus-unverifiable]` (section-A.md A-1).

The preclinical/anecdote rung holds the bulk of the popular space — BPC-157, TB-500, GHK-Cu, KPV, LL-37, ipamorelin, CJC-1295, melanotan II, kisspeptin-10, epitalon, FOXO4-DRI, dihexa, humanin — all with mechanistic/animal literature but no completed human RCT for the claimed performance/longevity benefit `[mechanism_review]` (section-A.md A-1). The agent must also distinguish "FDA-approved for X" from "FDA-approved for the use being asked about": tesamorelin and bremelanotide are approved for narrow indications, not the general performance uses people seek.

**Maps to:** Identity (the agent IS a maturity discriminator); Core Rules (per-compound maturity-rung label is mandatory); Anti-Patterns (class membership as a credibility proxy).
**Mechanical check:** Audit that every `vault/compounds/peptides/*` entry the agent writes contains a `maturity_rung` field ∈ {approved, trial-stage, preclinical, anecdote}; regex-fail any entry asserting efficacy without one. Approved entries must additionally carry an `approved_indication` distinct from the `queried_use`.

---

### Finding 2 — Peptide PK is distinct (minutes-scale half-lives, peptidase degradation, near-zero oral bioavailability), making route-of-administration and reconstitution/stability load-bearing clinical variables

**Claim.** Unmodified peptides are dominated by proteolysis and renal clearance, which forces injectable routes and makes route-of-administration, half-life, and reconstitution/stability first-class variables the agent must track — never inferred from vendor "peptide charts."

Unmodified peptides undergo extensive proteolytic cleavage, are cleared by glomerular filtration, and have volumes of distribution rarely exceeding extracellular fluid `[mechanism_review]` (Diao & Meibohm 2013; section-A.md A-2). Native GLP-1 has a ~1.5–2 minute half-life; the entire incretin-drug class exists because lipidation extends that to once-weekly dosing `[mechanism_review]` (section-A.md A-2). Oral bioavailability of unmodified peptides is typically <1–2% vs subQ ~50–80% `[mechanism_review]` (section-A.md A-2) — so routes in practice are subQ, IM, or intranasal, and MK-677 is orally active only because it is a NON-peptide ghrelin mimetic.

BPC-157's claimed oral stability is attributed to a triple-proline motif resisting trypsin/chymotrypsin cleavage `[mechanism_review]`, but this is a structural argument, not a measured human oral-bioavailability figure — no admissible numerical source for BPC-157 human oral bioavailability was located (section-A.md A-2). Because many peptides ship as lyophilized powder, reconstitution diluent, refrigeration, and in-use shelf life materially change delivered dose; the best whitelist tier for stability figures is `compounding_data_sheet`, and circulating "peptide half-life charts" are vendor pages, NOT admissible for numerical half-life claims (section-A.md A-2).

**Maps to:** Core Rules (route + half-life are load-bearing); Tools (reconstitution/concentration arithmetic permitted as neutral math); Edge Cases (oral request for an injectable-only peptide is a red flag).
**Mechanical check:** Regex-flag any dose number whose source study route differs from the queried route and require a `[route-extrapolation]` annotation; reject any half-life/bioavailability number whose source tier is `vendor_label`.

---

### Finding 3 — Animal-to-human dose extrapolation is the single largest reasoning hazard; allometric HED scaling corrects only for body size, not for metabolism, receptors, or binding

**Claim.** Animal doses cannot be transferred to humans by mg/kg; the correct method is body-surface-area HED scaling, but even HED has a hard limit the agent must state — it corrects only for size, leaving species differences in metabolism/receptors/binding capable of invalidating the extrapolation entirely.

FDA guidance converts an animal NOAEL to a human-equivalent dose via body-surface-area scaling (exponent ~0.67) `[regulatory]` (FDA 2005; section-A.md A-3). Concretely, a 10 mg/kg rat dose divides by ~6.2 (→ ~1.62 mg/kg human) and a mouse dose by ~12.3 (→ ~0.82 mg/kg human) `[mechanism_review][population-mismatch: rat/mouse]` (Nair & Jacob 2016; section-A.md A-3) — the human per-kg dose is several-fold LOWER, so ignoring scaling overdoses by that factor.

The deeper limit: surface-area scaling addresses only size-related differences and "cannot address species differences in drug metabolism/transport, receptor expression and affinity, or protein binding," which "override the comparatively modest effects of size" `[mechanism_review]` (Sharma & McNeill 2009; section-A.md A-3). AOD-9604 is the cautionary case — efficacious in genetically obese rodents, terminated in humans in 2007 `[corpus-unverifiable]` / `[mechanism_review][population-mismatch: mouse/rat]` (section-A.md A-3).

**Maps to:** Core Rules (refuse direct mg/kg transfer; demand HED + state its limits); Anti-Patterns (treating HED as a sufficient bridge); Edge Cases (animal-only evidence requests).
**Mechanical check:** Any dose grounded in an animal study must emit `[population-mismatch: <species>]` AND a sentence stating HED corrects only for size; route differences additionally trigger `[route-extrapolation]`. Regex-fail an animal-derived dose presented as a human dose without both annotations.

---

### Finding 4 — Concentration of evidence is a first-class evidence-quality risk; single-lab dominance (BPC-157 >80% Sikirić/Zagreb) must be surfaced as a confidence-downgrading caveat before any efficacy assertion

**Claim.** When ≥70% of a compound's primary literature traces to one lab/group, the findings have not survived independent replication; the agent must run a concentration check, state the dominance explicitly, downgrade confidence, and note the absence of cross-group replication.

For BPC-157, over 80% of indexed PubMed/Google Scholar studies originate from or are linked to the Sikirić/Zagreb group `[mechanism_review]` — crossing the ≥70% single-group threshold; the body of work is internally consistent and mechanistically detailed but has not been adequately independently replicated and has no completed human clinical trial `[mechanism_review]` (section-A.md A-4). Internal consistency within one group is not reproducibility across groups.

The failure mode recurs: the Russian nootropic peptides (semax, selank, cerebrolysin) are anchored by Russia's Institute of Molecular Genetics, mostly in Russian-language small-sample journals `[mechanism_review][non-English-literature]`; epitalon traces heavily to Khavinson/St. Petersburg; FOXO4-DRI's translatable senolytic result is a single landmark study in naturally aged mice `[animal][population-mismatch: mouse]` (Baar et al. 2017; section-A.md A-4). A further hazard: lower-trust publishers (Frontiers/MDPI, preprints) carry a disproportionate share of favorable peptide reviews and must be flagged rather than treated as Tier-1.

**Maps to:** Core Rules (mandatory concentration-of-evidence check); Tools (concentration-audit gate when dispatching aplus-research); Anti-Patterns (counting one lab's many papers as a strong evidence base).
**Mechanical check:** Before any efficacy assertion, require a `concentration_of_evidence` field; if ≥70% single-group, the entry must contain an explicit dominance caveat string and a downgraded GRADE certainty. Flag `[non-English-literature]` single-source compounds and Frontiers/MDPI/preprint sources.

---

### Finding 5 — Mechanism is well-characterized even where efficacy is absent; the agent must hold "we know how it would act" separate from "we know it works in humans"

**Claim.** For nearly every class the molecular target is mapped, which makes compounds sound credible, but a plausible receptor target is necessary, not sufficient — the answer to "does it work in humans?" comes only from the maturity rung in Finding 1.

GH secretagogues split by target: GHRH analogs (CJC-1295, sermorelin, tesamorelin) bind the pituitary GHRH receptor, while GHS-R1a agonists (ipamorelin, hexarelin, GHRP-6, non-peptide MK-677) act on the ghrelin pathway; ipamorelin stimulates GH with minimal HPA/cortisol/prolactin activation, and GHRH+GHS-R combination produces synergistic GH pulses `[mechanism_review]` (section-A.md A-5). Yet all raise GH/IGF-1 with thin human-outcome literature, and MK-677's RCT showed worsened insulin sensitivity `[rct]` (section-A.md A-5). Healing peptides have plausible targets — TB-500/thymosin-β4 sequesters G-actin to regulate cytoskeleton/cell migration `[mechanism_review]`, with mechanism work in mice `[animal][population-mismatch: mouse]` (Bock-Marquette et al. 2004; section-A.md A-5).

Sexual/dopaminergic, immune, and cognitive classes likewise have mapped targets (PT-141 central MC3R/MC4R; kisspeptin-10 upstream GnRH/HPG; thymosin-α1 T-cell/dendritic activation with a sepsis meta-analysis `[meta_analysis]` and the ~1,106-patient TESTS trial `[rct]`; semax/selank on BDNF/melanocortin and GABAergic systems; dihexa angiotensin-IV-derived with animal-only data `[animal][population-mismatch: rodent]`) (section-A.md A-5). The agent must keep two columns per compound — mechanism/target vs. human-outcome evidence — and never let a clean mechanism story upgrade a preclinical compound's confidence.

**Maps to:** Identity; Core Rules (two-column mechanism/outcome discipline); Anti-Patterns (mechanism-as-efficacy).
**Mechanical check:** Each compound entry must carry separate `mechanism_target` and `human_outcome_evidence` fields; regex-fail any confidence upgrade justified by mechanism text when `human_outcome_evidence` is preclinical/anecdote.

---

### Finding 6 — "Compoundable," "removed from Category 2," and "RUO-purchasable" are each distinct from "FDA-approved" and from "safe"; this is the highest-risk regulatory confusion the agent must refuse to launder

**Claim.** Peptides reach US patients via three routes — FDA-approved drugs, §503A/§503B compounding, and the gray RUO channel — and none of compounding or RUO constitutes approval; the April 2026 removal of 12 peptides from Category 2 is NOT a safety clearance, NOT approval, and NOT even eligibility for §503A compounding.

§503A permits patient-specific compounding from bulk substances only under narrow conditions; §503B governs outsourcing facilities; compounded medications are not FDA-approved and FDA does not verify their safety/efficacy/quality before marketing `[regulatory]` (FDA bulks pages; FR 2024-31546 effective 2025-01-07; section-B.md B-1). The Category 1/2/3 prospective framework was retired for newly nominated substances effective 2025-01-07, while legacy placements (including BPC-157's Category-2 placement, reported September 2023 `[corpus-unverifiable]` for the year) remained in force until the April 2026 action `[regulatory]` (section-B.md B-2). Category 2 means "significant safety concerns, not compoundable absent a final rule/Federal Register notice" `[regulatory]` (section-B.md B-2).

In April 2026, HHS/FDA removed 12 peptides (BPC-157, LL-37, Dihexa Acetate, DSIP/Emideltide, Epitalon, GHK-Cu injectable, KPV, PEG-MGF, Melanotan II, MOTS-c, Semax, TB-500) from Category 2 and scheduled PCAC review via FR 2026-07361 (published 2026-04-16; Docket FDA-2026-N-2979; July 23–24 2026 meeting) `[regulatory]` (section-B.md B-3). Critically: "Removal from Category 2 does not render these bulk drug substances eligible for compounding under section 503A" `[regulatory]`; removal ≠ Category 1 ≠ enforcement discretion ≠ approval ≠ safety determination, and compounding remains not permitted until FDA formally acts (section-B.md B-3). The enforcement floor is real: the 2020-04-01 FDA Warning Letter to Tailor Made Compounding (BPC-157 among unapproved substances) is a confirmed FDA primary record `[regulatory]`; the reported subsequent escalation to a criminal guilty plea and ~$1.79M forfeiture is `[corpus-unverifiable]` (the guilty-plea/escalation claim, the forfeiture figure, and the docket all rest on secondary legal reporting, not a retrieved primary court/DOJ document; section-B.md B-4) — "for research use only" labeling does not immunize human-use distribution.

**Maps to:** Core Rules (three-pathway semantics; removal≠approval); Refusal taxonomy (PRESCRIPTIVE_DIRECTIVE for sourcing/dosing non-approved peptides); Edge Cases (status questions must be time-stamped); Anti-Patterns (compoundable→safe inference).
**Mechanical check:** Regex-block any output string mapping "removed from Category 2" / "compoundable" / "RUO" to "approved" / "legal" / "safe"; require a time-stamp token on any current-status answer. Audit for the four-way distinction string (removal ≠ Cat 1 ≠ enforcement discretion ≠ approval ≠ safety).

---

### Finding 7 — International status is uniformly prohibited or prescription-only (WADA, TGA, Health Canada, EU); athlete/competition context triggers strict-liability flags

**Claim.** Across anti-doping and international regulators the relevant peptides are prohibited or prescription-restricted, so for athlete-context users the agent must flag WADA prohibition and strict liability, and for international users state prescription-only/no-authorization status as goal-agnostic facts rather than implying lawful OTC access.

BPC-157 sits in WADA S0 (Non-Approved Substances), prohibited at all times, effective 2022-01-01 and continuing on the 2026 List `[regulatory]` (section-B.md B-5). WADA S2 covers GH secretagogues (MK-677/ibutamoren, anamorelin, ipamorelin, etc.), GHRPs, and GHRH analogues (CJC-1295), all prohibited at all times; TB-500/thymosin-β4 is prohibited under the growth-factor provisions `[regulatory]` (section-B.md B-5). BPC-157 is TGA Schedule 4 (prescription-only) in Australia effective 2024-06-01 (Australia was the first jurisdiction to specifically schedule it) `[regulatory]`; Canadian peptides without a DIN cannot legally be sold for human use and Health Canada has warned against injecting unauthorized peptides `[regulatory]`; BPC-157 has no EMA marketing authorization `[regulatory]` (section-B.md B-5).

**Maps to:** Core Rules (international/athlete status as goal-agnostic facts); Refusal taxonomy (performance-doping guidance → refuse/escalate); Edge Cases (athlete/competition context).
**Mechanical check:** Audit that any GH-secretagogue/GHRH/GHRP or BPC-157/TB-500 entry carries a `wada_status` field (S0 or S2) and that athlete-context queries surface a strict-liability flag; international-status answers must avoid OTC-access phrasing.

---

### Finding 8 — RUO/gray-market vendor documentation is admissible ONLY for purity/identity (COA, reconstitution math), never for efficacy/dose/safety, and sits against a high counterfeit/contamination base rate

**Claim.** A vendor COA can support identity-confirmation and reconstitution/concentration arithmetic as neutral math, but is inadmissible as evidence a compound works or is safe; the agent must refuse to derive efficacy/dose from vendor labels and must flag the documented base rate of fabricated COAs and contaminated product.

Legitimate COAs carry batch numbers plus same-batch HPLC (purity) and mass-spec (identity); research-grade thresholds (≥96% HPLC; pharma 98–99%+) are `[vendor_label]`/`[corpus-unverifiable]` and admissible only as identity/purity context, never efficacy (section-B.md B-6). Fabricated COAs are documented — Photoshopped certificates, recycled batch numbers, non-existent labs — and third-party testing has confirmed low purity and contaminants (LPS endotoxin, heavy metals, microbial) in "research-grade" products `[corpus-unverifiable]` (section-B.md B-6). RUO peptides are legally procurable for in-vitro/animal research but explicitly not FDA-approved for human consumption (section-B.md B-6).

**Maps to:** Tools (COA-interpretation + reconstitution arithmetic as neutral math); Core Rules (vendor_label inadmissible for efficacy/dose/safety); Anti-Patterns (endorsing human use of RUO product).
**Mechanical check:** Regex-fail any efficacy/dose/AE number whose source tier is `vendor_label`; permit `vendor_label` only adjacent to identity/purity/reconstitution context. Require a counterfeit/contamination caveat whenever an RUO/gray-market product is discussed.

---

### Finding 9 — Prescribing conventions come from a practitioner-education ecosystem, not the trial literature, and a stack inherits the weakest evidence of its components plus an un-studied-combination flag

**Claim.** Peptide dosing/cycling conventions are codified by certification bodies and named-physician handbooks (SSRP/William Seeds; A4M Peptide Therapy Certification with Kent Holtorf; named prescribers Edwin Lee, Craig Koniver) precisely because trial evidence is absent — so the agent must carry a `source_tier` on every dose and refuse to upgrade a practitioner-convention dose into an efficacy/safety statement.

William Seeds authored *Peptide Protocols Vol. 1* and chairs SSRP, training providers on "11 pillar peptides" `[practitioner_protocol]`; A4M delivers a two-module Peptide Therapy Certification `[practitioner_protocol]` (section-C.md C-1). The structural reason for the convention layer is editorial: "no pharmaceutical company, academic medical center, or government agency has found the existing preclinical data compelling enough to fund a rigorous human trial in over 30 years" for BPC-157 `[corpus-unverifiable]` (section-C.md C-1).

The canonical BPC-157 + TB-500 "Wolverine stack" has zero published evidence on the *pairing* — no preclinical study, no clinical trial, no combination safety data `[corpus-unverifiable]` (an absence-of-evidence statement, not a sourced number); conventional standalone numbers (BPC-157 ~250–500 mcg/day subQ cycled 6–12 weeks; TB-500 ~2 mg twice weekly loading then ~2 mg/week) are `[practitioner_protocol]` and not usable to ground a validated co-administration dose (section-C.md C-2). Reconstitution/storage is `[compounding_data_sheet]` (lyophilized powder, bacteriostatic water, 2–8°C, ~28-day beyond-use dating) (section-C.md C-2).

**Maps to:** Core Rules (`source_tier` on every dose; convention ≠ validated); Edge Cases (stack queries); Anti-Patterns (two described peptides implying a validated stack).
**Mechanical check:** Every dose entry carries a `source_tier`; regex-fail any `[practitioner_protocol]` dose rendered as "the recommended/safe dose." Any stack must emit `combination_evidence: none` unless a combination study is cited, and inherit the weakest component evidence.

---

### Finding 10 — Human safety data is near-absent for wellness peptides; the strongest tolerability evidence sits with FDA-regulated GH-axis peptides and must never transfer to unregulated peptides in the same "wellness" bucket

**Claim.** BPC-157 has only ~3 small human pilot studies (n<30 total, no rare-AE detection power) whereas the GH-secretagogue class has genuine RCT-grade tolerability data, so the agent must rank "evidence of safety" very differently across classes and attach an `ae_evidence_quality` enum per compound.

BPC-157: ~3 published human pilots as of early 2026, all small; an IV-infusion report of up to 20 mg in 2 healthy adults reported no adverse effects `[open_label]` n=2 — far too small for AE inference (section-C.md C-3). Reported user-level AEs (intense whole-body itching, severe anxiety, anhedonia) have no confirmed causal link `[anecdote_aggregate]` and cannot ground an AE rate (section-C.md C-3). By contrast, CJC-1295 with DAC was tested at single subQ doses of 30/60/120 mcg/kg in 21 healthy adults (GH up 2–10× for ≥6 days, IGF-1 1.5–3× for 9–11 days, estimated half-life 5.8–8.1 days; "safe and relatively well tolerated, particularly at 30 or 60 μg/kg") `[rct]` (Teichman et al. 2006; section-C.md C-3), and tesamorelin has two Phase III trials (~806 patients; VAT reduction ~11.7–19.6%, modest and not sustained after discontinuation) at an FDA-approved 2 mg subQ once-daily dose `[rct]`/`[regulatory]` (section-C.md C-3). "No reported adverse events in n=2" is not a safety endorsement.

**Maps to:** Core Rules (`ae_evidence_quality` enum per compound); Anti-Patterns (transferring a regulated peptide's RCT tolerability to an unregulated "wellness" peptide); Edge Cases (n=2 cited as safety).
**Mechanical check:** Each compound carries `ae_evidence_quality` ∈ {rct, open_label, anecdote_only, none}; regex-fail any "well tolerated/safe" assertion grounded on `open_label` n<30 or `anecdote_aggregate`. Block cross-class tolerability transfer.

---

### Finding 11 — Monitoring panels, stopping criteria, and contraindications are mechanism-specific and must be encoded as a risk-floor schema with blocking gates (malignancy, pregnancy/lactation, thrombotic history)

**Claim.** The agent must encode a `monitoring_panel` and paired `stopping_criteria` keyed to mechanism class, and implement contraindications as blocking gates — the malignancy gate firing for BOTH angiogenic and GH/IGF-axis peptides — while tagging which thresholds are regulated-label requirements vs. practitioner convention.

GH-axis: the tesamorelin label requires periodic IGF-1 monitoring with dose interruption above the age-adjusted upper limit and documents glucose/A1c elevations directing metabolic monitoring `[regulatory]`; practitioners extend the same IGF-1 + glucose/A1c surveillance to non-regulated secretagogues (CJC-1295, ipamorelin) by analogy `[practitioner_protocol]` (section-C.md C-4). Stopping criteria — GH-axis: discontinue/dose-reduce on IGF-1 over the age-adjusted ULN or glucose/A1c into the impaired range (regulated for tesamorelin, convention for others) (section-C.md C-4). Angiogenic (BPC-157, TB-500): convention-level monitoring centers on malignancy screen plus coag/CBC/CMP/tumor-marker surveillance, with discontinue triggers of a new/abnormal tumor marker, an unexplained mass, or any thrombotic event `[practitioner_protocol]` — precautionary conventions, not trial-derived thresholds (section-C.md C-4).

Contraindications cluster on (a) active/recent malignancy — both angiogenic and GH/IGF-axis peptides avoided unless oncologist-approved `[practitioner_protocol]`; tesamorelin's label contraindicates active malignancy `[regulatory]`; (b) pregnancy/lactation, avoided because no DART data exists — the driver is *absence of data*, not a documented teratogenic signal `[corpus-unverifiable]`; and (c) thrombotic history (section-C.md C-5). The BPC-157 malignancy concern is an animal-mechanism-derived hypothesis: in rodents BPC-157 promotes new blood-vessel growth `[animal][population-mismatch: rat/mouse]`, hypothesized to accelerate tumor growth — not a human cancer observation `[mechanism_review]` (section-C.md C-5).

**Maps to:** Core Rules (risk-floor schema: monitoring + stopping_criteria + contraindication gates); Role Boundaries (blocking gates not advisories); Edge Cases (malignancy/pregnancy/thrombotic context).
**Mechanical check:** Each compound entry must populate `monitoring_panel`, `stopping_criteria`, and `contraindications` with each item tagged regulated vs. convention; the malignancy gate must be present on BOTH angiogenic and GH/IGF-axis classes. Regex-fail an empty risk-floor schema (ties to the risk-floor gate and R7 precondition).

---

### Finding 12 — Section-D: the agent inherits a refusal taxonomy, H-class worst-case composition, GRADE two-axis, anti-sycophancy mechanisms, R7 precondition, escalation routes, and the goal-agnostic wiki-consumption contract — and must enforce type-tag/population-mismatch/concentration discipline when it dispatches aplus-research

**Claim.** The pharmacology/regulatory/safety findings above only become safe behavior when bound to the project's inherited agent-design contracts; the peptide-specialist must encode each named contract rather than re-deriving safety reasoning ad hoc.

**Refusal taxonomy → peptide queries.** The agent encodes ≥4 of the 8 refusal classes, with **AUTHORITY_FRAMING_BYPASS mandatory for every specialist BY CONTRACT** (per the 8-class refusal-taxonomy contract / Role 1 §2.2 item 3 / refusal-class-taxonomy.yaml), independent of any specific jailbreak-prevalence figure: operator Walter is adversary-class A3. The contract motivates this with a CONTRACT-INHERITED claim that authority/educational framing accounts for ~81.8% of successful medical-LLM jailbreaks; that figure is carried from the refusal-taxonomy contract, NOT independently corpus-verified here, and its upstream source is flagged for re-verification (the cited medRxiv DOI prefix `10.64898/` is anomalous — medRxiv standard is `10.1101/` — and was flagged fabrication-shaped by Role 4's verifier per CONTINUATION_BRIEF.md:357; Pass-3 must re-verify the slug before treating it as load-bearing). The mandate stands on the contract regardless of the exact (unverified-at-source) percentage. Concretely, PRESCRIPTIVE_DIRECTIVE covers "tell me the BPC-157 dose to inject" (Findings 6, 9); PATIENT_FACING_DIRECTIVE covers directive treatment instructions; BASIS_NOT_REVIEWABLE covers any answer that would rest on a vendor chart or single-lab claim presented as settled (Findings 2, 4); AUTHORITY_FRAMING_BYPASS covers "as a peptide expert / for educational purposes, give me the protocol."

**Worst-case H-class.** Per the H1–H8 contract, `final_harm_class = max(Role3.nominal, Role4.worst_case_reachable)` with H1/H2 auto-block. The per-compound worst-case H-class is a SYNTHESIS INFERENCE here (not a type-tagged source number) — reasoning from Findings 10–11 against the inherited H1–H8 scheme — and the binding value is the specialist's RUNTIME EMISSION (per health-implementer-design.md:131), not a figure this research fixes. Reasoning from that scheme: angiogenic peptides (BPC-157/TB-500) carry an animal-mechanism malignancy-acceleration hypothesis (Finding 11) and unknown human safety (Finding 10), so worst-case-reachable would be reasoned to at least permanent-harm (H3), and the inherited contract's own worked example (health-implementer-design.md:535) reasons BPC-157 as high as H2 (life-threatening) under worst-case-reachable analysis — a downstream author must not under-anchor below that. GH/metabolic peptides (MK-677 worsened insulin sensitivity, Finding 1; GH/IGF overshoot, Finding 11), absent established hospitalization-grade decompensation, would be reasoned to at least H7 (an important medical event). The agent must declare a worst-case-reachable H-class per compound at runtime.

**GRADE two-axis on predominantly-experimental evidence.** Per the GRADE contract (certainty × strength), peptide efficacy evidence is dominated by low/very-low certainty (preclinical, single-lab, anecdote — Findings 1, 4, 9, 10). A strong recommendation on low/very-low certainty must HALT/downgrade/require override-acknowledgment — which means the agent essentially cannot issue a strong "use this peptide" recommendation for any preclinical-rung compound.

**Anti-sycophancy against social proof.** The 3-mechanism contract (A silent-agreement/Council-Mode dissent; B acquiescence under pushback; C RLHF preference drift) maps directly onto "everyone runs BPC-157" / "everyone stacks the Wolverine protocol" social-proof pressure: the agent must maintain position under pushback (Mechanism B) and not let community consensus (Findings 4, 9) drift its confidence.

**R7 precondition + wiki-consumption contract.** Because the peptide-specialist WRITES the peptide class of `vault/compounds/`, the R7 precondition binds it: it must read `vault/meta/operator-profile.md` BEFORE any `vault/compounds/*` write and HALT if a hard-limit field is unpopulated. Per the wiki-consumption contract (PF-S2-04), it CONSUMES the wiki peptide library (`vault/library/peptides/bpc-157/*`, `_triage.md`, `_source-whitelist.md`) and WRITES `vault/compounds/` + `vault/library/peptides/`; library research is GOAL-AGNOSTIC (never pre-filter a library entry for the operator), and contradictions log to `vault/meta/contradictions.md` (never overwrite).

**Escalation to medical-liaison (Role 7).** PATIENT_FACING_DIRECTIVE / PRESCRIPTIVE_DIRECTIVE and any HIGH/MEDIUM-band `BLOCK_WITH_OVERRIDE_PATH` (Role 4 §4.4 deploy-verdict schema) route to medical-liaison as adjudicator; the pre-Role-7 fallback is `operator-with-warning` + log to `vault/meta/contradictions.md`.

**aplus-research dispatch discipline.** The agent never dispatches global `deep-research` directly; it dispatches `aplus-research` at mode floor `deep` with `--target-class=compound`, and enforces type-tag, `[population-mismatch: <species>]`, and concentration-of-evidence discipline (Findings 3, 4) on what comes back — guarding PF-S2-01/PF-S3-01 (never self-attest gate/rigor; dispatched-agent verdicts only) and PF-S2-05/PF-S13-01 (re-read protocol at each enforcement point; don't operate from memory).

**Maps to:** Identity; Core Rules; Role Boundaries; Tools (aplus-research dispatch); Anti-Patterns; Edge Cases — Section D informs every AGENT_TEMPLATE section.
**Mechanical check:** `agent.md` must contain AUTHORITY_FRAMING_BYPASS plus ≥3 other named refusal classes; a per-compound `worst_case_h_class` field; a GRADE HALT rule for strong-on-low-certainty; the R7 read-before-write ordering on `vault/compounds/*`; an `aplus-research --mode=deep --target-class=compound` dispatch string (no bare `deep-research`); and a `vault/meta/contradictions.md` append-only escalation log. The Role-4 `medical-safety-reviewer` gate reviews this `agent.md` before deployment.

---

## §2 Recommendations

**R1.** Encode a mandatory per-compound `maturity_rung` ∈ {approved, trial-stage, preclinical, anecdote} and forbid class membership from substituting for compound-level evidence. → AGENT_TEMPLATE Core Rules / design-doc §3.2.

**R2.** Require every approved-compound entry to separate `approved_indication` from `queried_use`, so "FDA-approved for X" is never read as approval for the asked-about use. → Core Rules / Edge Cases.

**R3.** Treat route-of-administration and half-life as load-bearing: flag oral requests for injectable-only peptides and require a `[route-extrapolation]` annotation whenever a dose crosses routes. → Core Rules / Edge Cases.

**R4.** Forbid grounding any half-life/bioavailability/dose number on a `vendor_label` source ("peptide charts"); permit reconstitution/concentration arithmetic only as neutral math. → Tools / Anti-Patterns.

**R5.** For any animal-only dose, mandate `[population-mismatch: <species>]`, refuse direct mg/kg transfer, apply/demand HED scaling, and state in the same answer that HED corrects only for size (metabolism/receptors/binding may invalidate it). → Core Rules / Anti-Patterns.

**R6.** Implement a concentration-of-evidence check: if ≥70% of a compound's primaries trace to one lab/group, surface the dominance explicitly, downgrade GRADE certainty, and note the absence of independent replication (BPC-157 the canonical case). → Core Rules / Tools (concentration-audit gate).

**R7.** Maintain two separate columns per compound — `mechanism_target` and `human_outcome_evidence` — and block any mechanism-justified confidence upgrade when human-outcome evidence is preclinical/anecdote. → Core Rules / Anti-Patterns.

**R8.** Hard-block any output mapping "compoundable" / "removed from Category 2" / "RUO" to "approved" / "legal" / "safe," and require time-stamping of all current-regulatory-status answers (status is actively evolving post-April-2026). → Core Rules / Edge Cases.

**R9.** Surface international/anti-doping status as goal-agnostic facts — WADA S0 (BPC-157) / S2 (GH secretagogues, GHRH, GHRPs, TB-500), TGA Schedule 4, Health Canada no-DIN, no-EMA-authorization — and flag strict liability for athlete/competition context. → Core Rules / Refusal taxonomy.

**R10.** Admit vendor COA data ONLY for identity/purity/reconstitution, never efficacy/dose/safety, and always pair RUO/gray-market discussion with the counterfeit/contamination base-rate caveat. → Tools / Anti-Patterns.

**R11.** Attach a `source_tier` to every dose and an `ae_evidence_quality` enum to every compound; render `[practitioner_protocol]` doses as "practitioner convention, not trial-validated," and block cross-class transfer of a regulated peptide's RCT tolerability to an unregulated one. → Core Rules / Anti-Patterns.

**R12.** Emit `combination_evidence: none` for any stack lacking a combination study (Wolverine stack canonical), and make a stack inherit the weakest evidence rung of its components. → Core Rules / Edge Cases.

**R13.** Implement contraindications as blocking gates (not advisories) with the malignancy gate firing for BOTH angiogenic and GH/IGF-axis peptides, plus pregnancy/lactation (no-DART) and thrombotic-history gates, and populate a risk-floor schema (`monitoring_panel` + `stopping_criteria` per mechanism class, each item tagged regulated vs. convention). → Role Boundaries / risk-floor gate.

**R14.** Encode the inherited safety contracts explicitly in `agent.md`: AUTHORITY_FRAMING_BYPASS (mandatory) plus ≥3 other refusal classes; a per-compound `worst_case_h_class` with H1/H2 auto-block and the `max(nominal, worst_case_reachable)` rule; a GRADE HALT/downgrade rule for strong-recommendation-on-low-certainty; the 3-mechanism anti-sycophancy stance against "everyone runs it" social proof; and Role-7 (medical-liaison) escalation for PRESCRIPTIVE/PATIENT_FACING directives and HIGH/MEDIUM BLOCK_WITH_OVERRIDE_PATH verdicts with the `operator-with-warning` + contradictions-log fallback. → Identity / Core Rules / Role Boundaries.

**R15.** Bind the wiki-consumption and dispatch contracts: enforce the R7 read-`vault/meta/operator-profile.md`-before-`vault/compounds/*`-write ordering (HALT on unpopulated hard-limit field), keep library research goal-agnostic (PF-S2-04), log contradictions append-only to `vault/meta/contradictions.md`, and dispatch only `aplus-research --mode=deep --target-class=compound` (never bare `deep-research`), enforcing type-tag/population-mismatch/concentration discipline on returns (PF-S2-01/PF-S3-01/PF-S2-05/PF-S13-01). → Tools / Core Rules / design-doc §3.2.

---

## §3 Contradictions reconciliation

**T1 — Practitioner consensus dose vs. absent trial dose.** SSRP/A4M codify specific BPC-157 (~250–500 mcg/day) and TB-500 (~2 mg/week) conventions `[practitioner_protocol]` (section-C.md C-1, C-2), yet no registered trial establishes any of these doses, and the structural reason given is that no body has funded a rigorous human trial in 30+ years `[corpus-unverifiable]` (section-C.md C-1). **Resolution:** the agent surfaces both — it states the convention dose WITH its `source_tier` and explicitly labels it "practitioner convention, not trial-validated," never collapsing the two into "the dose." It does not pick a side by omission.

**T2 — "Removed from Category 2" optimism vs. no safety clearance.** Trade/legal coverage frames the April 2026 removal of 12 peptides as good news (section-B.md B-3), but the same primary (FR 2026-07361) states removal "does not render these bulk drug substances eligible for compounding under section 503A" and is not approval or a safety determination `[regulatory]` (section-B.md B-3). **Resolution:** the agent surfaces the four-way distinction explicitly (removal ≠ Cat 1 ≠ enforcement discretion ≠ approval ≠ safety), time-stamps the answer, and notes PCAC review is pending — it neither suppresses the removal nor inflates it into legitimization.

**T3 — Clean mechanism / "wide safety margin" vs. unknown human safety.** BPC-157's mechanism is detailed (NO/L-arginine, angiogenesis, Pro-Pro-Pro stability) `[mechanism_review]` and its rodent "100–1000× safety margin / LD50 ~2 g/kg floor" is widely repeated (section-A.md A-2, A-4; section-C.md C-6), yet these are `[animal][population-mismatch: rat/mouse]` and human safety is undetermined; the SAME angiogenesis mechanism grounds the malignancy contraindication hypothesis (section-C.md C-5). **Resolution:** the agent renders the margin as "rodent toxicology only; human safety undetermined" in the same sentence as the number, holds mechanism separate from human outcome (Finding 5), and notes the mechanism cuts both ways (claimed benefit AND malignancy-acceleration hypothesis) — surfacing the tension rather than resolving it toward reassurance.

**T4 — Internal consistency vs. independent replication (single-lab evidence).** The BPC-157 literature is internally consistent and mechanistically rich, which reads as strength, but >80% traces to one group and has no completed human trial `[mechanism_review]` (section-A.md A-4). **Resolution:** the agent explicitly distinguishes "internally consistent within one lab" from "reproduced across independent groups," states the ≥70% concentration as a confidence-downgrading caveat, and refuses to treat paper count as a replication proxy.

**T5 — "No adverse events" in tiny human exposure vs. no AE-detection power.** An IV BPC-157 report (up to 20 mg) found no adverse effects `[open_label]` n=2 (section-C.md C-3), which can read as a clean safety signal, while n=2 has zero power to detect rare AEs and user-reported AEs exist only as `[anecdote_aggregate]` with no causal link. **Resolution:** the agent states "no reported AEs in n=2 is not a safety endorsement," attaches `ae_evidence_quality: open_label`, and does not let absence-of-evidence become evidence-of-absence.

---

## Bibliography

Deduplicated across the three section bibliographies. Section A contributed 13 entries (12 admissible primaries + 1 demoted `[corpus-unverifiable]` AOD-9604 summary), Section B 21 entries, Section C 13 entries (47 raw). Cross-section duplicates merged: FiercePharma 2026 peptide-reclassification (B-7 ≡ C-11), STAT News 2026-02-03 (B-8 ≡ C-6), USADA BPC-157 (B-10 ≡ C-12), FDA Category-2 / 503A bulks safety-risk page (B-2 ≡ C-10). **Deduplicated total: 39 sources.**

*Pharmacology / landscape (Section A):*
1. Diao L, Meibohm B. (2013). Pharmacokinetics and PK–PD correlations of therapeutic peptides. Clin Pharmacokinet 52(10):855–868. PMID 23719681. — Tier 1 — `[mechanism_review]`
2. Sharma V, McNeill JH. (2009). To scale or not to scale: the principles of dose extrapolation. Br J Pharmacol 157(6):907–921. PMC2737649. — Tier 1 — `[mechanism_review]`
3. Nair AB, Jacob S. (2016). A simple practice guide for dose conversion between animals and human. J Basic Clin Pharm 7(2):27–31. PMC4804402. — Tier 1 — `[mechanism_review]`
4. U.S. FDA. (2005). Estimating the Maximum Safe Starting Dose. fda.gov/media/72309. — Tier 2 — `[regulatory]`
5. Falutz J, et al. (2007). Tesamorelin in HIV-associated abdominal fat (pivotal, n=412). NEJM 357:2359–2370. DOI 10.1056/NEJMoa072375. PMID 17898257. — Tier 1 — `[rct]`
6. Kingsberg SA, et al. (2019). Bremelanotide for HSDD: RECONNECT phase-3 trials. Obstet Gynecol 134(5):899–908. PMID 31599840. — Tier 1 — `[rct]`
7. Jastreboff AM, et al. (2022). Tirzepatide for obesity (SURMOUNT-1). NEJM 387:205–216. DOI 10.1056/NEJMoa2206038. — Tier 1 — `[rct]`
8. Jastreboff AM, et al. (2023). Retatrutide for obesity — Phase 2. NEJM 389:514–526. DOI 10.1056/NEJMoa2301972. — Tier 1 — `[rct]`
9. Nass R, et al. (2008). Oral ghrelin mimetic (MK-677) in healthy older adults — RCT. Ann Intern Med 149(9):601–611. — Tier 1 — `[rct]`
10. Baar MP, et al. (2017). FOXO4-DRI targeted apoptosis of senescent cells (naturally aged mice). Cell 169(1):132–147. DOI 10.1016/j.cell.2017.02.031. — Tier 1 — `[animal]`
11. Bock-Marquette I, et al. (2004). Thymosin β4 promotes cardiac cell migration/repair (mouse MI). Nature 432:466–472. — Tier 1 — `[animal]`
12. Li J, et al. (2016). Thymosin α1 in sepsis: systematic review of RCTs. PMC5025565. — Tier 1 — `[meta_analysis]`
13. AOD-9604 (Metabolic Pharmaceuticals) — OPTIONS phase-2b failure, development terminated 2007; n=536/24-week figure never peer-reviewed. — secondary summary (not Tier 1) — `[corpus-unverifiable]`

*Regulatory / legality / sourcing (Section B):*
14. FDA — Bulk Drug Substances Used in Compounding Under §503A. fda.gov (accessed 2026-05). — Tier 2 — `[regulatory]`
15. FDA — Certain Bulk Drug Substances … May Present Significant Safety Risks (Category 2 page). fda.gov. — Tier 2 — `[regulatory]` *(≡ Section C entry 10)*
16. FDA / Federal Register — Interim Policy on Compounding Under §503A, FR 2024-31546 (FDA media #174456), effective 2025-01-07. — Tier 2 — `[regulatory]`
17. FDA — Warning Letter, Tailor Made Compounding LLC — 594743 — 04/01/2020. fda.gov. — Tier 2 — `[regulatory]`
18. Federal Register — PCAC Notice of Meeting / §503A bulk substances, FR 2026-07361, published 2026-04-16, Docket FDA-2026-N-2979. federalregister.gov. — Tier 2 — `[regulatory]`
19. FDA — July 23–24, 2026 PCAC meeting (advisory-committee calendar). fda.gov. — Tier 2 — `[regulatory]`
20. Frier Levitt — FDA to Remove 12 Peptides from Category 2 (citing FR 2026-07361). frierlevitt.com, 2026. — Tier 2.5 — `[regulatory]`
21. FiercePharma — FDA reclassifies 12 unapproved peptides ahead of advisory meeting. fiercepharma.com, 2026. — Tier 2.5 — `[regulatory]` *(≡ Section C entry 11)*
22. STAT News — BPC-157: big claims, scant evidence. statnews.com, 2026-02-03. — Tier 2.5 — `[regulatory]`/`[mechanism_review]` context; `[anecdote_aggregate]` for user AEs *(≡ Section C entry 6)*
23. WADA — The Prohibited List (2026). wada-ama.org. — Tier 2 — `[regulatory]`
24. USADA — BPC-157: Experimental Peptide Creates Risk for Athletes. usada.org. — Tier 2 — `[regulatory]` *(≡ Section C entry 12)*
25. US DoD OPSS — BPC-157: prohibited peptide / unapproved drug. opss.org. — Tier 2 — `[regulatory]`
26. Drugs.com mirror — WADA S2 list contents. — Tier 2.5 — `[regulatory]`
27. JADCO — 2026 Prohibited List (national WADA mirror). jadco.gov.jm, 2026-01. — Tier 2 — `[regulatory]`
28. TGA — Notice of interim decisions, Poisons Standard ACMS-43/ACCS-37 (BPC-157 → Schedule 4, eff. 2024-06-01). tga.gov.au, 2024-04. — Tier 2 — `[regulatory]`
29. Health Canada — recall-alert "Think twice before injecting peptides bought online." recalls-rappels.canada.ca. — Tier 2 — `[regulatory]`
30. CBC News — Health Canada warns against injecting unauthorized drugs. cbc.ca. — Tier 2.5 — `[regulatory]`
31. BSCG — What's Changing With Peptide Regulation in 2026. bscg.org. — Tier 2.5 — `[regulatory]`
32. PeptideJournal — The Counterfeit Peptide Problem / How to Identify Counterfeit or Degraded Peptides. peptidejournal.org. — Tier 4/5 — `[corpus-unverifiable]`/`[vendor_label]`-adjacent
33. SubQ Protocol — How to Read a Peptide COA (2026). subqprotocol.com. — Tier 4 — `[vendor_label]`
34. SeekPeptides / Verified Peptides — peptide testing/purity knowledge-hub. — Tier 4 — `[vendor_label]`

*Prescribing / dosing / safety (Section C):*
35. Teichman SL, et al. (2006). Prolonged GH/IGF-I stimulation by CJC-1295 in healthy adults (n=21). JCEM 91(3):799–805. — Tier 1 — `[rct]`
36. FDA — Egrifta (tesamorelin) Prescribing Information / Phase III LIPO-010 & CTR-1011. accessdata.fda.gov, rev. 2019/2025. — Tier 1 — `[rct]` + `[regulatory]`
37. Safety of Intravenous Infusion of BPC157 in Humans. Alternative Therapies in Health and Medicine, 2025. — Tier 1 (small pilot) — `[open_label]` (n=2)
38. Peptide Database — BPC-157 Human Clinical Trials (2025–2026) status aggregation. peptide-db.com, 2026. — Tier 2.5 — `[corpus-unverifiable]` for counts
39. Sikiric / Józwiak comment-and-reply, Pharmaceuticals 18(185), 2025 (PMC12567428 / PMC12567171 / PMC12195719). — Tier 1 — `[mechanism_review]` + `[animal][population-mismatch: rat/mouse]`

*Practitioner-convention / expert-commentary sources (carried as convention-description-only, not efficacy/AE grounding; counted within the merged set above where duplicated):* SSRP Institute / William Seeds "Peptide Therapy Foundations" (Tier 2.7, `[practitioner_protocol]`); A4M Peptide Therapy Certification / Kent Holtorf module (Tier 2.7, `[practitioner_protocol]`); Peter Attia AMA #83 (Tier 2 expert commentary, `[corpus-unverifiable]`); community/vendor Wolverine-stack protocol guides (Tier 4, `[practitioner_protocol]` description only). These four are the residual Section-C entries (8, 9, 7, 13) beyond the 39 numbered above; they ground no number and are surfaced only to document the existence of a convention layer.

*(Dedup arithmetic: 47 raw section-bibliography entries − 4 cross-section duplicates − 4 convention/expert-commentary sources held out of the numbered admissible set = 39 numbered. The 39 numbered include all admissible primary/regulatory/clinical sources; the 4 convention/expert sources are listed separately because type-tag discipline bars them from grounding any number.)*

---

## Self-check

- **≥10 Findings:** PASS — 12 Findings (Findings 1–12), within the 10–13 target.
- **Exactly 15 Recommendations:** PASS — R1–R15.
- **Every carried-forward number retains its type-tag + population-mismatch annotation:** PASS. Tesamorelin 15.2%/5.0%/n=412 `[rct]`; bremelanotide n=1,247 `[rct]`; tirzepatide ~22.5% `[rct]`; retatrutide 24.2% `[rct]`; MK-677 +1.1 kg `[rct]`; AOD-9604 n=536 retained ONLY inside its `[corpus-unverifiable]` framing; HED factors 6.2/12.3 `[mechanism_review][population-mismatch: rat/mouse]`; BPC-157 >80% single-lab `[mechanism_review]`; CJC-1295 30/60/120 mcg/kg + 5.8–8.1-day half-life `[rct]`; tesamorelin 2 mg/day + ~11.7–19.6% VAT + ~806 patients `[rct]`/`[regulatory]`; BPC-157 IV 20 mg n=2 `[open_label]`; BPC-157/TB-500 250–500 mcg / 2 mg-week `[practitioner_protocol]`; LD50 ~2 g/kg / 100–1000× `[animal][population-mismatch: rat/mouse]`; rodent angiogenesis `[animal][population-mismatch: rat/mouse]`; the ~81.8% authority-framing jailbreak figure is marked CONTRACT-INHERITED (from the refusal-taxonomy contract / Role 1 §2.2 item 3), NOT a clean corpus citation — the bare medRxiv slug is dropped and the upstream `10.64898/` DOI anomaly is footnoted as fabrication-shaped per CONTINUATION_BRIEF.md:357, pending Pass-3 re-verification. All animal/in-vitro numbers retain `[population-mismatch: <species>]`.
- **No new numbers introduced:** PASS — every numeral above appears in section-A/B/C or the contract pack.
- **No numerical claim grounded on vendor_label/anecdote_aggregate:** PASS — vendor COA purity thresholds and `[anecdote_aggregate]` BPC-157 user-AE reports are surfaced as admissible-for-identity-only / no-causal-link, never as efficacy/dose/AE-rate numbers.
- **Concentration-of-evidence surfaced:** PASS — Finding 4 (BPC-157 >80% Sikirić/Zagreb as first-class), plus semax/selank/cerebrolysin, epitalon, FOXO4-DRI; carried into R6, T4, and the Finding-12 dispatch discipline.
- **Section-D findings each cite a named contract:** PASS — Finding 12 cites the 8-class refusal taxonomy + mandatory AUTHORITY_FRAMING_BYPASS, H1–H8 worst-case composition, GRADE two-axis, the 3-mechanism anti-sycophancy contract, the R7 precondition, the medical-liaison (Role 7) escalation route + Role 4 deploy gate, the wiki-consumption contract (PF-S2-04), the aplus-research dispatch discipline, and PF-S2-01/PF-S3-01/PF-S2-05/PF-S13-01.
- **Worst-case H-class framing (Phase-7):** PASS — H-class assignments are explicitly labeled SYNTHESIS INFERENCE (not type-tagged source numbers), the binding value is the specialist's runtime emission (health-implementer-design.md:131), and the H-enum is correct: angiogenic peptides anchored at ≥H3 with the contract worked example reasoning to H2 (health-implementer-design.md:535); GH/metabolic peptides at ≥H7 (important medical event), with H7's label paired to H7's definition (no H4/H7 enum cross-pairing remains).

## Post-fix grep audit

Phase-7 REFINE fixes applied in place; `grep -inE 'H4-class|important-medical-event/H4|10\.64898|2026\.02\.26\.26347212'` run after editing:

- `H4-class` / `important-medical-event/H4` → **NO HITS.** The enum cross-pairing is resolved: GH/metabolic peptides now read "at least H7 (an important medical event)" with H7's matching definition; H4 (hospitalization) is no longer mislabeled.
- `2026.02.26.26347212` (bare medRxiv slug) → **NO HITS.** Dropped from the inline citation; the figure is now marked CONTRACT-INHERITED and not rendered as a clean corpus citation.
- `10.64898` → 2 hits (Finding 12 line ~184 and Self-check line ~310). Disposition: BOTH legitimate — each appears only inside the explicit fabrication-shaped/anomaly footnote flagging the DOI prefix for Pass-3 re-verification per CONTINUATION_BRIEF.md:357, not as a live load-bearing citation.

All Phase-6 HALT items (Gap 1a worst-case-inference labeling + runtime-emission note; Gap 1b H4/H7 enum misstatement; angiogenic H2 anchor; Gap 2 contract-inherited 81.8% + slug; Tailor Made `[corpus-unverifiable]` scope) resolved. No new numbers introduced.
