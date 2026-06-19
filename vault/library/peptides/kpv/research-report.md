---
title: KPV
type: compound
permalink: a-plus-maxing/library/peptides/kpv/research-report
class: peptide
evidence_tier: C
risk_tier: experimental
status: researching
created: 2026-06-19
last_verified: 2026-06-19
walter_status:
doctor_discussion_required: true
---

# KPV (Lys-Pro-Val · α-MSH(11-13))

## Metadata
- **class:** peptide (tripeptide; the C-terminal fragment of α-melanocyte-stimulating hormone)
- **evidence_tier: C** — the entire KPV evidence base is preclinical (rodent models + cell culture + ex-vivo human-tissue pharmaceutics); there are **zero human clinical studies of any design**, and within the gut/IBD literature that practitioner claims most lean on, ~75% of the in-vivo efficacy primaries come from a single lab.
- **risk_tier: experimental** — unapproved drug with no controlled human safety dataset; was placed in the FDA 503A interim Category 2 list (2023), then **removed from that list ~15 April 2026** (nomination withdrawn), now unlisted pending the 23–24 July 2026 PCAC review — and removal is not approval and does not make KPV lawfully compoundable.
- **status:** researching
- **last_verified:** 2026-06-19

> **Read this first — the honest evidence state.** KPV is the **C-terminal tripeptide of α-MSH** (Lys-Pro-Val; α-MSH residues 11–13). It is an anti-inflammatory tripeptide whose best-characterized action is, in the key models, **melanocortin-receptor-INDEPENDENT** — it works largely by getting inside cells (in the gut, via the di/tripeptide transporter PepT1) and inhibiting the intracellular NF-κB inflammatory pathway, rather than by binding a melanocortin receptor on the cell surface. The evidence is **entirely PRECLINICAL** — there are **zero human clinical studies of any design** (registry searches and the literature both return a clean null). The most commonly cited "human" paper, Pawar 2017, is an **ex-vivo skin-permeation study on excised skin in diffusion cells — not a trial.** The strongest data are in rodent colitis/IBD models, but ~75% of the gut-IBD in-vivo efficacy primaries come from a single lab (the Merlin group, Georgia State University). The native peptide's **antimicrobial activity is contested** (one positive single-lineage result versus an independent null). The acne and gout "efficacy" widely attributed to KPV is actually for **analogues — KdPT and the (CKPV)₂ dimer — not the KPV monomer.** Do **not** conflate KPV (Lys-Pro-Val) with **KdPT (Lys-D-Pro-Thr)**; they are different molecules and KdPT also has zero human trials. Regulatory state: not FDA-approved; placed in 503A Category 2 (2023), then removed ~April 2026 (nomination withdrawn), now unlisted pending the PCAC meeting on 23–24 July 2026 — **removal is not approval and KPV is not lawfully compoundable.** WADA: not individually named, but prohibited at all times under category S0 because it has no human therapeutic approval. The vendor "no LD50 / tolerated ≥100 mg/kg" tolerability figures are **unverified** and could not be traced to a primary toxicology study. Operator-specific fields (Walter's status, baseline biomarkers, goals, stack) are intentionally left blank — this is a goal-agnostic library entry.

---

## TL;DR

KPV (Lys-Pro-Val) is the three-residue C-terminal tail of α-MSH, marketed as an anti-inflammatory and "gut/skin healing" peptide. The mechanistic story is biologically coherent and unusually well-worked-out for such a small molecule: KPV enters cells (notably via the intestinal transporter PepT1) and suppresses NF-κB-driven inflammation from the inside, without needing a melanocortin receptor and without the pigment-stimulating action of the parent hormone. In rodent colitis the direction of effect (KPV reduces gut inflammation) replicates across at least four independent labs, multiple models, two species, and several routes. But the gap between that preclinical promise and the marketing is large and specific: there is **no human evidence of any kind** — no RCT, no cohort, no open-label trial, not even a registered protocol — for any indication; the precise magnitudes of effect (including the eye-catching "~12,000× more potent in a nanoparticle" figure) are largely single-lab; the native peptide's antimicrobial claim is contradicted by an independent replication; and the acne/gout data belong to chemically distinct analogues, not KPV itself. KPV is unapproved, not lawfully compoundable, and prohibited in sport. It is best understood as a **mechanistically attractive but clinically unproven experimental compound** whose strongest real signal is preclinical gut anti-inflammation.

---

## 1. Identity, Chemistry & Pharmacokinetics

### 1.1 What KPV actually is

KPV is the tripeptide **L-lysyl-L-prolyl-L-valine** (written H-Lys-Pro-Val-OH; one-letter code **K-P-V**). Its authoritative chemistry is: molecular formula **C₁₆H₃₀N₄O₄**, average molecular weight **342.43 g/mol**, **CAS 67727-97-3**, PubChem CID **125672** (catalogued there under the synonym "MSH (11-13)"); the IUPAC name is (2S)-2-[[(2S)-1-[(2S)-2,6-diaminohexanoyl]pyrrolidine-2-carbonyl]amino]-3-methylbutanoic acid [6, regulatory].

A small but important housekeeping point: some vendor pages quote a molecular weight of "~400 Da." **That number is wrong for the free tripeptide.** It most likely reflects an acetate/TFA salt form or a simple transcription error. The authoritative database value is **342.43 g/mol** [6, regulatory]; the vendor figure is cited here only to flag and reject it, not to ground any number [9, vendor_label].

### 1.2 Relation to α-MSH

KPV corresponds exactly to **residues 11–13 (the C-terminus) of α-melanocyte-stimulating hormone (α-MSH)**, which is itself a 13-residue (tridecapeptide) hormone derived from proopiomelanocortin (POMC); in its native form α-MSH is N-terminally acetylated and C-terminally amidated [5, mechanism_review]. The biologically interesting fact is that **most of α-MSH's anti-inflammatory activity localizes to this C-terminal tripeptide**, while KPV **lacks the pigmentary (melanogenic) action** of the parent hormone [5, mechanism_review]. In other words, KPV is the "anti-inflammatory message" of α-MSH stripped of the part that drives tanning — which is precisely why it has been pursued as a therapeutic candidate.

### 1.3 Receptor dependence — a key finding

The single most important pharmacological fact about KPV is that, **in the best-characterized models, its peripheral anti-inflammatory effect is melanocortin-receptor INDEPENDENT.** This is established by two independent lines of evidence:

- In murine **crystal (urate/MSU)-induced peritonitis**, KPV's anti-migratory effect (it reduced neutrophil/PMN accumulation) was **not blocked by melanocortin-receptor antagonists**, persisted in **MC1R-deficient (recessive-yellow, e/e) mice**, and — unlike the core α-MSH peptides — KPV **did not raise cAMP.** The authors concluded that KPV does not act through melanocortin receptors and more likely works by inhibiting IL-1β function [1, animal][1, in_vitro] (mouse; recessive-yellow e/e and wild-type; macrophage cultures in vitro) [route-extrapolation: intraperitoneal model].
- At the cellular/gut level, in intestinal epithelial (Caco2-BBE) and immune cells, KPV is taken up by the **PepT1 di/tripeptide transporter** and inhibits NF-κB and MAP-kinase signaling and cytokine secretion at **nanomolar** concentrations; the protective effect was attributed to PepT1-mediated uptake rather than melanocortin receptors — the Caco2-BBE cells lacked MC3R/MC5R, and α-MSH did not reproduce the effect comparably [2, animal][2, in_vitro] (mouse colitis in vivo + human-derived epithelial cell lines in vitro).

**Honest nuance.** "Receptor-independent" is the established conclusion **for KPV** in the peritonitis and gut-epithelial models — it is not a blanket claim across every cell type. The *parent* α-MSH genuinely does signal through melanocortin receptors (MC1R–MC5R), and broader reviews note that α-MSH and related tripeptides exert anti-inflammatory action through *both* receptor-dependent mechanisms (centrally/neurogenically, and on MCR-expressing peripheral cells) *and* direct intracellular mechanisms [5, mechanism_review]. What KPV does is **isolate the intracellular/receptor-independent arm.** (The mechanistic detail is developed in §2.)

### 1.4 Stability and degradation chemistry

As a small, linear, unmodified tripeptide, KPV is a substrate for peptidases and — administered systemically — would be expected to have the short plasma half-life typical of small peptides. However, **no admissible primary source providing a quantified KPV serum/plasma half-life or aqueous-solution stability constant was retrieved.** The "short half-life" expectation is therefore mechanistic inference from peptide chemistry, **not a cited measured value.** What *is* documented is functional rather than numeric: intact intestinal/colonic delivery of KPV depends on carrier-mediated (PepT1) uptake rather than passive diffusion [2], and topical KPV does not cross intact skin by passive diffusion [3]. The absence of a measured stability constant is a real gap (see §1.7).

### 1.5 Pharmacokinetics — oral / lumenal

KPV is **orally/lumenally absorbable via the proton-coupled oligopeptide transporter PepT1** (gene SLC15A1), which carries most di- and tripeptides. PepT1 is normally a small-intestinal transporter but is **induced in the colon during inflammation.** It has high affinity for KPV, transporting it into epithelial and immune cells even at low (nanomolar) luminal concentrations [2, in_vitro][2, mechanism_review].

This carrier-mediated route is biologically effective in rodent colitis: **oral KPV reduced the incidence/severity of both DSS- and TNBS-induced colitis** with decreased pro-inflammatory cytokine expression. The dosing/exposure paradigm used was ~100 µM in the drinking water (a lumenal-exposure parameter), while cell-uptake studies showed activity at ~10 nM [2, animal] (mouse; DSS and TNBS colitis models) [route: oral/lumenal]. An important caveat for any dosing extrapolation: that ~100 µM figure is a **dosing/exposure parameter in mice, not an absolute oral bioavailability fraction** — and as later delivery work shows, *free* oral KPV appears delivery-limited compared with formulated KPV (see §7).

### 1.6 Pharmacokinetics — topical / transdermal

**KPV does not cross intact human skin by passive diffusion.** In an ex-vivo permeation study using excised/dermatomed human skin in Franz diffusion cells, passive permeation was below the limit of detection (LOD 0.01 µg/mL). Physical enhancement was required: microneedle microporation gave a flux of ~4.4 µg/cm²/h; adding iontophoresis produced an ~8-fold increase, and combined microporation + iontophoresis a ~35-fold increase over microneedles alone [3, in_vitro] (excised human skin, in-vitro Franz-cell permeation) [route: transdermal]. The practical implication: a plain topical KPV cream applied to intact skin has no demonstrated route across the skin barrier — physical poration or another enhancement method is required for meaningful delivery. (This is an in-vitro tissue result, not an in-vivo human topical-efficacy demonstration.)

### 1.7 Pharmacokinetics — systemic

**No admissible primary human PK study** (plasma concentration–time, Cmax, AUC, clearance, or absolute bioavailability by any route) for KPV was retrieved. Systemic and parenteral PK parameters in humans are **unestablished** in the located literature. This is one of several "the number simply does not exist in a citable form" gaps that recur throughout this report.

### 1.8 KPV ≠ KdPT — the critical non-conflation

**KdPT (Lys-D-Pro-Thr) is a different tripeptide from KPV** — not a salt, not a formulation variant, not an alternate name. It is a derivative related to the α-MSH C-terminal region in which the proline is the **D-enantiomer** and **valine is replaced by threonine.** Its L-form sequence is homologous to residues 193–195 of IL-1β, which motivated an IL-1β-interaction hypothesis [4, animal][5, mechanism_review]. Like KPV, KdPT protects in experimental colitis (multiple murine models), promotes colonic epithelial proliferation, wound closure, and barrier function (transepithelial electrical resistance; tight-junction protein preservation after IFN-γ/TNF-α challenge), and does **not** affect melanogenesis in vitro; notably, KdPT acted **independently of IL-1 receptor type I in vivo**, distinguishing its mechanism from a simple IL-1RI antagonism [4, animal][4, in_vitro] (mouse colitis models in vivo + colonic epithelial cells in vitro).

Why this matters so much: a great deal of the dermatology and "anti-inflammatory" literature that gets attributed to "KPV" in vendor and blog write-ups is actually **KdPT** data (acne sebocytes in particular — see §7). Transferring a KdPT finding onto KPV as though it were the same molecule is a recurring and avoidable error.

### 1.9 Coverage gaps (Section 1)

- **No quantitative stability data** — no numeric KPV half-life, in-solution degradation rate, or storage-stability constant in any admissible primary; the "short half-life" claim is inference, not measurement.
- **No human/systemic PK** — no plasma concentration–time, Cmax, AUC, clearance, or absolute bioavailability for KPV by any route in humans.
- **Oral "absorption" is carrier-mediated and model-derived** — the ~100 µM oral-efficacy figure is a mouse dosing/exposure parameter, not a human bioavailability fraction.
- **Receptor-independence is model-specific** — established for KPV in MSU peritonitis and gut epithelium; the parent α-MSH does signal through melanocortin receptors and MC1R involvement is not excluded for KPV in *every* cell type.
- **Topical data are in-vitro human skin** — route-extrapolation to in-vivo human topical efficacy is not established here.

---

## 2. Mechanism of Action

**Bottom line up front:** KPV's anti-inflammatory action is mechanistically well-characterized **at the cell and animal level.** It converges on inhibition of **NF-κB** (and MAP-kinase) signaling; it is transported into cells by the **PepT1** di/tripeptide transporter; and its effect is **independent of melanocortin receptors** (i.e., intracellular/receptor-independent). All of this evidence is in vitro and in animal models — there are no human studies establishing these mechanisms in living humans, so any mechanism→human inference is extrapolation.

### 2.1 The smallest active fragment

KPV is the C-terminal tripeptide Lys-Pro-Val (α-MSH 11–13) and **retains the anti-inflammatory activity of the full 13-residue α-MSH hormone despite being only 3 of its 13 residues** [1, mechanism_review][6, mechanism_review]. The observation that the C-terminal tripeptide carries the anti-inflammatory "message" traces to early work and is summarized in the authoritative review literature [6, mechanism_review]. This is the foundational fact that makes KPV worth studying: it is the minimal sequence that preserves the useful (anti-inflammatory) action while shedding the pigmentary action.

### 2.2 NF-κB and MAP-kinase suppression

At **nanomolar concentrations** KPV inhibits activation of the **NF-κB** and **MAP-kinase** inflammatory signaling pathways and reduces pro-inflammatory cytokine/chemokine secretion [2, in_vitro]. Specifically, in human intestinal epithelial models (Caco2-BBE, HT29-Cl.19A) and human Jurkat T cells, **~10 nM KPV** suppressed NF-κB activation (luciferase reporter), MAP-kinase phosphorylation (ERK1/2, JNK, p38), and IL-8 expression/secretion [2, in_vitro]. The nanomolar potency is striking for a tripeptide and is consistent across the in-vitro work.

### 2.3 The intracellular NF-κB mechanism — and its single-lab caveat

KPV's molecular mechanism on NF-κB is **intracellular and post-receptor.** In the most mechanistically detailed study, KPV translocated into the cell nucleus, **stabilized the inhibitor IκBα** in TNF-α–stimulated cells, and **competitively blocked the interaction between the p65/RelA subunit of NF-κB and the nuclear-import carrier importin-α3 (Imp-α3)** — thereby suppressing nuclear translocation of p65 [3, in_vitro]. This was tested directly on KPV (Lys-Pro-Val), not extrapolated from other α-MSH fragments, in immortalized human bronchial epithelial cells (16HBE14o-) at 1–10 µg/mL [3, in_vitro].

**Single-lab caveat (carry this honestly).** The precise importin-α3/p65 step rests **primarily on this one KPV-specific study** (Land 2012, 16HBE14o- bronchial epithelium). It is genuinely a direct KPV test rather than an extrapolation, but **independent replication of the exact importin-α3 step is limited.** The right framing is: treat the precise molecular target (Imp-α3 competition) as **plausible-but-single-lab**, while the upstream phenotype (IκBα stabilization → NF-κB suppression) is **multiply supported** across studies [1][3].

### 2.4 Melanocortin-receptor independence

KPV's anti-inflammatory effect is **independent of melanocortin receptors (MC1R–MC5R).** KPV **lacks the core sequence motif** (His-Phe-Arg-Trp, α-MSH 6–9) that is required for melanocortin-receptor binding [6, mechanism_review]. In the Caco2-BBE and Jurkat models, neither MC3R nor MC5R was expressed and KPV did **not** raise intracellular cAMP (unlike the α-MSH controls), yet it remained anti-inflammatory [2, in_vitro]. In bronchial epithelium the effect was likewise concluded to be "independent of the melanocortin-receptor signalling system" and intracellular [3, in_vitro]. And in vivo, KPV reduced colitis even in **MC1R-mutant (MC1R e/e) mice**, indicating effects at least partially independent of MC1R signaling [4, animal].

For contrast and honesty: the full-length α-MSH *does* also have a genuine MC-receptor/cAMP arm — in RAW 264.7 macrophages, melanocortin peptides inhibit NF-κB DNA binding and nitric-oxide production via what is described as a **dual** (cAMP-dependent and -independent) mechanism [5, in_vitro]. So "KPV = α-MSH mechanism" is an over-simplification; KPV isolates the receptor-independent arm.

### 2.5 PepT1-mediated uptake — and the knockout that proves necessity

KPV enters cells via the **proton-coupled oligopeptide transporter PepT1 (SLC15A1)**, which is expressed in small-intestinal enterocytes, in colonic epithelium during inflammation, and in colonic/peripheral immune cells; this transporter-mediated uptake is **required** for KPV's intracellular anti-inflammatory action [2, in_vitro][7, animal]. KPV uptake by PepT1 was confirmed by competitive-inhibition and kinetic uptake assays in epithelial and immune cells [2, in_vitro]. Because PepT1 is up-regulated in inflamed colon (where it is normally low or absent), the transporter plausibly **targets KPV to inflamed tissue** [2, in_vitro].

The strongest causal evidence is genetic: in a murine colitis-associated-cancer model, KPV given to **wild-type** mice reduced inflammation and tumor burden, but the **same KPV gave no benefit in PepT1-knockout mice** — establishing PepT1 transport as **necessary** for KPV's anti-inflammatory/anti-tumorigenic effect [7, animal] (murine CAC model, WT vs PepT1-KO). This loss-of-effect-in-knockout result is the kind of clean causal demonstration that mechanistic stories often lack, and it is the backbone of the PepT1 narrative. (One honest limit: quantitative human enterocyte/immune-cell uptake parameters for KPV specifically are thin; the strongest causal data are the KO result and epithelial uptake kinetics.)

### 2.6 In-vivo anti-inflammatory action across models

KPV is anti-inflammatory in vivo in **multiple rodent colitis models.** Oral or intrarectal KPV reduced DSS- and TNBS-induced colitis with decreased pro-inflammatory cytokine expression (C57BL/6 mice; DSS 3% or TNBS 150 mg/kg; ~5–10 per group; KPV ~100 µM in drinking water) [2, animal]; and in an independent lab, KPV reduced disease activity, colon shortening, MPO activity, histologic inflammation, and cytokines in both DSS and CD45RB^hi T-cell-transfer colitis [4, animal]. (The efficacy detail is developed by domain in §7.)

### 2.7 Antimicrobial activity — in-vitro only, and contested

A mechanism distinct from immune modulation has been proposed: that α-MSH and its C-terminal tripeptide KPV have **direct antimicrobial activity.** In the originating study, α-MSH and KPV inhibited *Staphylococcus aureus* colony formation and reduced the viability and germ-tube formation of *Candida albicans*, over a broad concentration range including the picomolar; the proposed mechanism was peptide-induced elevation of microbial cAMP [8, in_vitro] (in vitro only; against *S. aureus* and *C. albicans*).

This claim must be carried with a strong caveat: it is **contested.** An independent group later synthesized capped KPV (Ac-KPV-NH₂) and found **no antimicrobial activity** under a variety of standard conditions (see §7 for the full replication conflict). The antimicrobial mechanism is therefore in-vitro-only and not robustly reproduced.

### 2.8 Coverage gaps (Section 2)

- **No human data for mechanism.** Every mechanistic claim derives from in-vitro (human cell lines + mouse macrophage/Jurkat) or rodent models. NF-κB/PepT1 mechanisms are not demonstrated in living humans.
- **Receptor-independence is well-supported but nuanced** — KPV itself is repeatedly shown receptor-independent and lacks the binding motif, but the parent α-MSH has a real MC-receptor/cAMP arm.
- **The importin-α3/p65 step is single-lab** — directly tested on KPV but not independently replicated at that exact step; the upstream IκBα/NF-κB phenotype is multiply supported.
- **PepT1 expression on immune cells** is asserted across the literature; the strongest causal evidence is the KO loss-of-effect plus epithelial uptake kinetics; human quantitative uptake parameters are thin.
- **Antimicrobial mechanism is in-vitro only and contested** — distinct from the anti-inflammatory mechanism.

---

## 3. Human Clinical Evidence

**State this plainly: there is essentially no human clinical evidence for KPV — none.**

As of June 2026, a thorough search of ClinicalTrials.gov, the EU/EudraCT registries, and PubMed/PMC returns **zero registered, completed, or results-posted human clinical trials of KPV** — no RCTs, no cohort studies, no open-label efficacy trials — for IBD/colitis, dermatology (atopic dermatitis, psoriasis), wound healing, or any other indication [1, regulatory][4, regulatory]. The entire KPV evidence base is **preclinical** (rodent models, cell culture) plus **ex-vivo human-tissue pharmaceutics** (transdermal-delivery studies on excised human skin, which are not clinical trials and enrolled no patients). The same is true for the analogue **KdPT**: no human trials, only animal/in-vitro work [7, anecdote_aggregate→null][8, regulatory].

### 3.1 Registry and literature null

- ClinicalTrials.gov for the intervention/term **"KPV"** returns **zero studies**; the term **"Lys-Pro-Val"** returns only unrelated full-text incidental matches (e.g., a prostate-radiation trial, a protease-supplement trial) with no KPV intervention; and **"KdPT"** returns **zero studies** [1, regulatory].
- EU registries (EudraCT / EU CTIS) and general registry/web searches for KdPT or KPV in IBD, atopic dermatitis, or psoriasis return **no registered or completed human trial** [2, regulatory].
- PubMed indexes ~50+ KPV publications spanning two decades; **none are human clinical trials.** The therapeutic studies are rodent colitis/IBD models, peritonitis/inflammation models, ocular and wound-healing animal models, and nanoparticle/oral-delivery formulation work in mice — plus in-vitro cell studies [3, anecdote_aggregate→null][4, regulatory][5, anecdote_aggregate→null]. The most-cited "KPV-IBD" paper (Dalmasso 2008, PMID 18061177) is a **mouse** DSS/TNBS colitis study, not human.

### 3.2 The Pawar 2017 "human skin" trap

The widely cited "KPV across **human skin**" paper (Pawar et al., *J Pharm Sci* 2017, PMID 28343991) is an **ex-vivo transdermal-permeation pharmaceutics study** using dermatomed/excised human skin in Franz diffusion cells. It **enrolled no living subjects, measured no clinical outcome, and is not a clinical trial** — it tests iontophoresis + microneedle delivery of KPV through skin tissue [6, regulatory] (design: ex-vivo human skin; n = skin samples, not patients; outcome = permeation flux, not therapeutic effect). It is commonly mis-presented as "human evidence." It is not. Likewise, in-vitro studies on "human keratinocytes / bronchial cells / peripheral-blood T cells" are cell culture, not trials.

### 3.3 KdPT — also no human trial

For the analogue **KdPT** (Lys-D-Pro-Thr), the principal study (Bettenworth/Böhm et al., 2011) reports protection from intestinal inflammation and barrier maintenance in **animal/in-vitro models only**; subsequent KdPT dermatology work (psoriasis-like disease) is in mouse models and human-skin-equivalents/biopsy-derived cells in vitro, not in patients in a controlled trial [7, anecdote_aggregate→null][8, regulatory]. **No completed human KdPT clinical trial exists** for IBD, atopic dermatitis, or psoriasis. Do not let KdPT preclinical data be miscited as human KPV evidence.

### 3.4 What "human evidence" the vendors actually cite

The "human evidence" cited by commercial peptide vendors and clinics (for eczema, acne, hidradenitis suppurativa, gut health) is **marketing/anecdotal**, not derived from any registered or peer-reviewed human trial; several vendor pages even explicitly concede "no human clinical trials" and "not FDA-approved." KPV is used off-label via compounding/"research-peptide" channels with **no published human efficacy or long-term safety data** [9, anecdote_aggregate][10, anecdote_aggregate].

### 3.5 Human study / trial table

| Study / item | Design | n | Outcome | NCT / PMID |
|---|---|---|---|---|
| ClinicalTrials.gov — intervention/term "KPV" | Registry query | — | **0 studies** | (none) |
| ClinicalTrials.gov — "KdPT" | Registry query | — | **0 studies** | (none) |
| EudraCT / EU CTIS — "KdPT" / "KPV" | Registry query | — | **0 studies** | (none) |
| Pawar et al. 2017 — "KPV across human skin" | **Ex-vivo** transdermal permeation (Franz cells) | excised human skin (no patients) | permeation/flux — **delivery study, NOT clinical** | PMID 28343991 |
| Dalmasso et al. 2008 (foundational IBD) | **Animal** (mouse DSS/TNBS colitis) | mice | ↓ intestinal inflammation — **preclinical** | PMID 18061177 |
| Bettenworth/Böhm 2011 (KdPT, IBD) | **Animal/in-vitro** | mice / cells | ↓ inflammation, barrier — **preclinical, KdPT** | PMC3157275 |
| **Human efficacy RCT / cohort / open-label of KPV** | — | — | **NONE FOUND** | — |

**Human clinical trials of KPV identified: 0** (0 RCT, 0 cohort, 0 open-label, 0 results-posted). **Human clinical trials of KdPT identified: 0.**

### 3.6 Coverage gaps (Section 3)

- **No human efficacy evidence for KPV, full stop** — in any indication. Any claim of KPV "human efficacy" is unsupported.
- **No human safety dataset** — no Phase I, no formal human safety/PK trial; tolerability claims are extrapolated from animal studies and uncontrolled anecdote.
- **The "human skin" citation is a trap** — Pawar 2017 is ex-vivo tissue, not a trial.
- **KdPT ≠ KPV, and KdPT also has no human trial** — keep them distinct.
- **Registry-search limit** — a trial registered under a proprietary code or sponsor alias could in principle be missed, but the convergent null across registry + literature + web makes a hidden completed trial unlikely.

---

## 4. Regulatory Status

### 4.1 FDA (United States)

- KPV is **not FDA-approved** for any indication and is **not** a listed dietary ingredient; products marketed for human use are unapproved drugs [8, regulatory].
- **503A status.** KPV (free base and acetate) was placed in the **interim 503A Category 2** list of bulk drug substances ("nominated but with identified safety risks") in **2023**; it was never in Category 1 [S1, regulatory][9, regulatory]. However, on **~15 April 2026 the FDA REMOVED KPV from Category 2** — its nomination was **withdrawn by the nominator**, and KPV was **one of 12 peptides removed in that action** (the same window as BPC-157 and TB-500). KPV is therefore **now UNLISTED** (in neither Category 1 nor Category 2), in regulatory limbo, **pending PCAC review on 23–24 July 2026** [9, regulatory][14, regulatory][15, regulatory]. One inference worth drawing explicitly: because the removal was driven by **nominator withdrawal** — an administrative/commercial act, not an FDA safety or efficacy determination — it is, if anything, a **neutral-to-negative** signal for the evidence base, **not a vindication** of KPV.
- **Removal from Category 2 is NOT an approval and does NOT authorize compounding.** Per the legal/industry coverage of the action: "removal from Category 2 does not render these bulk drug substances eligible for compounding under section 503A." KPV remains **not lawfully compoundable** unless and until it is reclassified into Category 1 (or covered by enforcement discretion) [14, regulatory][15, regulatory]. The bottom line is unchanged: KPV is not FDA-approved, not lawfully compoundable for these uses, and has no human data.
- **FDA's class-level rationale** historically cited for these peptides includes **immunogenicity, peptide-related impurities, characterization complexity, and lack of sufficient human safety/exposure data.** This is a class-level rationale; a KPV-specific FDA safety statement was not located in the retrieved primaries [9, regulatory].
- **PCAC review (23–24 July 2026).** KPV is on the Day-1 slate alongside BPC-157, TB-500, and MOTS-c (Day 2 covers DSIP/Emideltide, Semax, Epitalon). The committee will consider whether to recommend these peptides for inclusion on the 503A bulks list. **PCAC recommendations are non-binding**; even a favorable vote would require notice-and-comment rulemaking (typically >1 year) before 503A compounding could be lawful. **Do not characterize the July 2026 review as approval** [9, regulatory][10, regulatory][14, regulatory].

### 4.2 EU / other jurisdictions

No EMA marketing authorization for KPV was identified; topical/cosmetic use of KPV-type peptides exists in the unregulated supplement/cosmetic gray market. EU regulatory status is not affirmatively established in the retrieved sources — a coverage gap.

### 4.3 WADA anti-doping status

- **KPV / Lys-Pro-Val is NOT explicitly named on the WADA 2026 Prohibited List** [11, regulatory][12, regulatory]. The official 2026 list and its change-summary coverage do not name KPV, any tripeptide, melanocortin, or α-MSH fragment among additions or listed substances.
- **Nonetheless, KPV is prohibited at all times under category S0 (Non-Approved Substances).** S0 covers "any pharmacological substance which is not approved by any governmental regulatory health authority for human therapeutic use" (e.g., drugs in preclinical/clinical development, discontinued, designer, or veterinary/research-only). Because KPV has no human therapeutic approval anywhere, an athlete who used it and tested positive would fall under S0 [11, regulatory][13, regulatory].
- **Contrast with growth-factor peptides:** unlike BPC-157 (which anti-doping commentary names directly under S0) or true growth factors (S2), KPV is caught by the **catch-all S0 mechanism**, not by being individually enumerated. The practical outcome (prohibited) is the same; the legal route differs [13, regulatory]. Athletes should obtain written guidance from their National Anti-Doping Organization before any use.

### 4.4 Coverage gaps (Section 4)

- The exact KPV line-item on the FDA 503A page and the PCAC meeting page were not directly quoted (FDA pages/Federal Register returned partial/404 results at fetch time); the 15 April 2026 removal and the July 2026 PCAC agenda are **corroborated across four independent legal/industry sources**, not primary-quoted from fda.gov.
- The WADA "not explicitly named" conclusion rests on the change-summary plus the S0 catch-all logic; the master PDF was not exhaustively character-searched via tooling.
- EU/EMA status is "no approval found," not affirmatively characterized.

---

## 5. Concentration / Lab-Provenance Audit (first-class)

This section is carried **first-class and up front** — not buried — because single-lab concentration is one of the two largest honesty issues for KPV (the other being the complete absence of human data).

### 5.1 Method

Enumerate the **in-vivo efficacy primaries** for KPV that are retrievable with a verifiable citation (PMID/DOI), attribute each to its senior/corresponding lab, and compute single-lab share = (in-vivo efficacy primaries from the dominant lab) / (total enumerated in-vivo efficacy primaries). Two denominators are reported because the literature splits cleanly into an **IBD/gut track** and a small **non-gut track**, and the dominant-lab share is sensitive to which you count.

### 5.2 Enumerated in-vivo efficacy primaries

| # | Citation | Senior lab / institution | In-vivo model |
|---|----------|--------------------------|---------------|
| P1 | Dalmasso 2008, *Gastroenterology*, PMID 18061177 | **Merlin — Georgia State U / Atlanta VA** | DSS + TNBS colitis (mouse) |
| P2 | Viennois 2016, *Cell Mol Gastroenterol Hepatol*, PMID 27458604 | **Merlin — Georgia State U** | colitis-associated cancer (AOM/DSS, mouse) |
| P3 | Xiao 2017, *Molecular Therapy*, PMID 28143741 | **Merlin — Georgia State U** (Xiao corresp.; Southwest U co-lead) | DSS ulcerative colitis (mouse), HA-NP-delivered |
| P4 | Kannengiesser 2008, *Inflamm Bowel Dis*, PMID 18092346 | Kucharzik/Luger — U Münster, Germany (**independent**) | DSS + CD45RB-hi transfer colitis (mouse) |
| P5 | Bonfiglio 2006, *Exp Eye Res*, PMID 16965771 | Drago — U Catania, Italy (**independent**) | corneal epithelial wound healing (rabbit) — *non-gut domain* |
| P6 | Cutuli 2000, *J Leukoc Biol*, PMID 10670585 | Catania/Lipton α-MSH lineage (**independent of Merlin**) | antimicrobial vs *S. aureus* / *C. albicans* — *in-vitro-lead (tagged `in_vitro (+ animal)` in §7.3/Bibliography); counted here only for the all-cause denominator* |

### 5.3 Estimated single-lab share

- **All-cause in-vivo efficacy primaries (N=6):** Merlin/Georgia State = **3/6 ≈ 50%.**
- **Gut/IBD-only in-vivo efficacy primaries (N=4: P1–P4):** Merlin/Georgia State = **3/4 ≈ 75%** → **FLAG: ≥70% single-lab concentration within the gut/IBD efficacy literature** — and the gut/IBD literature is exactly what practitioner and vendor claims most lean on.

### 5.4 The dominant groups

1. **The Didier Merlin lab (Georgia State University Institute for Biomedical Sciences / Atlanta VA; earlier at Emory)** — the modern KPV-efficacy engine. It established the central mechanistic claim (KPV's anti-inflammatory effect is PepT1-mediated and MCR-independent) and authored the colitis, colitis-associated-cancer, and oral-nanoparticle-delivery primaries. Recurrent co-authors form a tight cluster (Dalmasso, Viennois, Xiao, Laroui, Charrier-Hisamuddin, Sitaraman).
2. **The Catania/Lipton α-MSH lineage** — the *origin* lineage. James M. Lipton and Anna Catania (1980s–2000s) identified KPV as the minimal anti-inflammatory/antipyretic "message" of α-MSH and hold the foundational US composition patents. The Italian Catania/Drago axis (U Catania) also produced the independent antimicrobial (Cutuli 2000) and corneal (Bonfiglio 2006) primaries.

### 5.5 The "~12,000×" figure — read it correctly

A frequently repeated headline is that nanoparticle-delivered KPV achieves colitis efficacy at a "~12,000-fold lower" concentration than free KPV. **This figure originates from a single group (Xiao/Merlin) and is an intra-study formulation comparison (nanoparticle vs free KPV) within one lab** [4 in §7]. It is **not** an independently replicated measure of KPV's absolute potency, and it should **not** be quoted as a general property of "KPV." Treat it strictly as a **delivery-formulation result** — interesting for drug-delivery science, not a claim about how potent KPV inherently is.

### 5.6 Provenance caveat

Because the gut/IBD efficacy base is ~75% one lab, the strongest KPV efficacy narrative (oral, PepT1-targeted, IBD) rests heavily on a single group whose findings have **not been independently reproduced in humans** and have limited cross-lab in-vivo replication outside the shared mechanism. The independent primaries (Münster IBD; Catania antimicrobial/corneal) corroborate the **direction** of effect but in different models and at different concentrations — they **reduce, but do not eliminate**, single-lab concentration risk. (Denominator-sensitivity note: the all-cause N=6 set counts the antimicrobial and corneal papers as "in-vivo efficacy primaries"; those are tagged in-vitro-lead in other sections. That tagging choice does not affect the headline gut/IBD 75% figure.)

---

## 6. Why this lands at evidence_tier C

The evidence_tier is a deliberate, conservative grade. KPV lands at **C** for the following converging reasons:

1. **Zero human evidence of any design.** No RCT, no cohort, no open-label trial, no registered protocol, no results posting — in any indication (§3). A higher tier is impossible without at least some controlled human data; KPV has none.
2. **Preclinical-only efficacy base.** Every efficacy claim is rodent or in-vitro. The mechanistic story is coherent and (for the gut) directionally replicated, which is why KPV does not fall to the lowest tier — but mechanism→human is extrapolation.
3. **Single-lab concentration in the headline indication.** ~75% of the gut/IBD in-vivo efficacy primaries come from one lab (§5). Direction replicates across ≥4 labs, but the magnitudes (and the famous 12,000× figure) are largely single-lab.
4. **Contested secondary claims.** The native-KPV antimicrobial claim has an independent failed replication (§7); the acne/gout "efficacy" belongs to analogues, not the monomer (§7).
5. **No human safety dataset.** No human AE rate can be quoted; the vendor tolerability figures are unverified (§8).

What keeps KPV at C rather than lower is the genuine, mechanistically detailed, cross-lab-directionally-replicated preclinical anti-inflammatory signal (especially in gut), plus a clean causal PepT1-knockout result. What prevents anything higher is the total absence of human data and the single-lab magnitude concentration. **C = preclinically promising, clinically unproven.**

---

## 7. Preclinical Efficacy by Domain

All evidence in this section is **preclinical** (rodent + in-vitro). Effect sizes are model-, route-, and formulation-dependent. Several papers report direction + significance (p<0.05) but exact percent reductions and SDs were not always extractable from accessible abstracts/full text (publisher paywalls), so cytokine/MPO deltas should generally be read as "significantly reduced," not as precise numbers.

### 7.1 Gastrointestinal / colitis (the strongest domain — Merlin-dominated)

- **Foundational oral colitis efficacy.** Oral KPV (100 µM in drinking water) reduced the severity of both **DSS- and TNBS-induced colitis** in mice — less body-weight loss, preserved colon length, reduced colonic MPO, and lower pro-inflammatory cytokine mRNA (IL-6, IL-12, IFN-γ, IL-1β, TNF-α), all p<0.05. Species/n: C57BL/6 mice, n=5/group (DSS), n=10/group (TNBS); route: oral (drinking water) [1, animal]. The cellular correlate (PepT1-mediated, nanomolar NF-κB/MAPK suppression in Caco2-BBE, HT29-Cl.19A, Jurkat) is the same paper's in-vitro arm [1, in_vitro].
- **Independent replication (Germany).** A different lab showed KPV reduced inflammation in two distinct mouse colitis models — DSS colitis and CD45RB^hi naïve T-cell adoptive-transfer colitis — with reduced inflammatory infiltrate, earlier weight regain, lower MPO, and improved histology. In MC1R-deficient (MC1R e/e) mice given DSS, KPV **rescued all treated animals from death**, indicating the effect does not require MC1R. Species: mice (C57BL/6 background incl. MC1R e/e); routes: oral and parenteral [2, animal].
- **PepT1 causality in colitis-associated cancer.** In an AOM/DSS model, oral KPV prevented/reduced tumorigenesis and inflammation in wild-type mice but produced **no inhibitory effect in PepT1-knockout mice** — establishing PepT1 as the required transporter for KPV efficacy in vivo. PepT1-overexpressing transgenic mice had larger tumor burden; PepT1-KO mice had reduced tumor number/size. Species: WT, PepT1-KO, PepT1-TG mice; AOM + DSS; route: oral [3, animal].
- **Nanoparticle delivery (the source of the 12,000× figure).** KPV loaded in PLGA-based nanoparticles achieved colitis efficacy similar to free KPV at a **~12,000-fold lower** KPV concentration; hyaluronic-acid-functionalized NPs (HA-KPV-NPs, ~272 nm) further targeted colonic epithelium + macrophages, normalizing body weight, colon length, MPO, TNF-α mRNA, and histology toward healthy controls. Delivered dose 16 µg/kg/day KPV. Species/n: FVB male mice, 8 wk, n=5/group; 3% DSS; route: oral gavage [4, animal]. **⚠ Concentration-audit flag:** the "12,000×" figure is a single-group (Xiao/Merlin) **intra-study formulation comparison**, not an independent replication of absolute potency — see §5.5.
- **Independent prodrug platform (China).** An ROS-responsive self-immolative KPV conjugate (proKPV) self-assembling into oral nanoparticles showed 3.8-fold greater colonic accumulation than free KPV and protected against DSS colitis at a ~20-fold lower dose than free KPV (free KPV 1 mg/kg = no benefit; proKPV 0.5 and 2.5 mg/kg = robust protection). proKPV at 2.5 mg/kg outperformed oral 5-ASA at 50 mg/kg on multiple endpoints. Species/n: C57BL/6J male mice (20–24 g), n=6/group; acute DSS, 7 days; route: oral [5, animal]. (Notably this is from an **independent** delivery-chemistry lab — Army Medical University.)
- **Independent IV co-assembled nanodrug (China).** A PepT1-targeted nanoparticle co-assembling KPV with the immunosuppressant FK506 reduced disease-activity index, restored colon length, and lowered MPO/NO/ROS and TNF-α/IL-1β/IL-6 in both acute (4% DSS) and chronic (2.5% DSS) colitis, outperforming KPV-alone and FK506-alone arms. Species/n: C57BL/6 male mice, 8 wk, n=6/group; KPV dose 1 mg/kg/day; **route: intravenous (not oral — note the route)** [6, animal].
- **Independent rectal/hydrogel route, different species.** A KPV-binding double-network hydrogel (PMSP-KPV), administered **rectally**, restored the colonic epithelial mucosal barrier, reduced oxidative stress, and modulated gut microbiota in TNBS-induced ulcerative colitis in **rats**. Species: rats; model: TNBS; route: rectal [7, animal].

**Replication structure for the gut domain (the honest read).** The **direction** of effect — KPV lowers colitis severity in rodents — replicates across **at least four independent labs** (Merlin; Münster; Army Medical University; Luzhou; plus the rat-rectal hydrogel group), across two species (mouse + rat), four models (DSS, TNBS, transfer, AOM/DSS), and three routes (oral, rectal, IV). That cross-lab directional replication is real and is the strongest thing KPV has going for it. But the **specific magnitudes** (the 12,000×, the exact cytokine deltas) are largely single-lab and should be reported as such. And none of it is human.

### 7.2 Skin / wound / mucosal repair

- **Oral mucositis (wound closure).** In a chemotherapy- (5-FU) and acid-induced oral-mucositis model, a mucoadhesive hydrogel releasing KPV promoted re-epithelialization (↑CK10, ↑PCNA) within 3–5 days, improved body-weight and food-intake recovery, and enhanced LPS-stimulated human oral keratinocyte (HOK) migration in scratch-wound assays. Species/n: male Sprague-Dawley rats 180–200 g, n=6/group; route: topical mucosal hydrogel, 100 µg/mL, 200 µL twice daily ×5 days [4, animal][4, in_vitro]. The same hydrogel showed direct antibacterial action in vivo (residual MRSA at the wound zone ~3.1-fold lower with the optimized formulation; KPV inhibited *S. aureus* in vitro comparably to amoxicillin) — i.e., a combined antibacterial + repair effect at an infected mucosal wound [4, animal][4, in_vitro].
- **Colonic mucosal healing.** Orally delivered KPV (HA-functionalized nanoparticles) promoted mucosal/wound healing in DSS colitis: in vitro it dose-dependently accelerated recovery of wounded Caco2-BBE monolayers; in vivo, treated colonic tissue was histologically near-normal versus DSS controls, with reduced TNF-α mRNA and MPO. Species/n: FVB male mice, 8 wk, n=5/group; route: oral gavage, KPV 16 µg/kg/day ×5–6 days [10, animal][10, in_vitro].
- **Cutaneous inflammation (foundational).** The C-terminal tripeptide α-MSH(11-13) = KPV inhibits **contact sensitivity** and acute skin/paw inflammation: α-MSH and α-MSH(11-13) significantly reduced acute ear inflammation, mouse-paw edema, and contact-sensitivity responses [12, animal] (mouse; route: systemic; rabbit capillary-permeability data also reported). This older work is the foundational in-vivo evidence for KPV in cutaneous inflammation.
- **KdPT (analogue, not KPV) — epithelial wound/barrier.** In colonic epithelial cells, KdPT increased proliferation, accelerated scratch-wound closure, raised transepithelial electrical resistance after IFN-γ/TNF-α challenge, and preserved tight-junction proteins and barrier function in vivo; it protected against DSS colitis and in IL-10⁻/⁻ mice, acting independently of IL-1RI and without melanogenic effect. **Direct wound/barrier-repair data are stronger for KdPT than for native KPV** [5, animal][5, in_vitro].

**Important gaps in the skin domain.** There is **no retrievable primary** for the marketed claims that "topical KPV closes wounds 40% faster" or that KPV lowers IgE/severity in NC/Nga atopic-dermatitis mice — these are **unsupported** and excluded. The real KPV wound/repair evidence is **mucosal** (oral mucositis, colonic), not dermal; no dermal (skin) wound-healing in-vivo model with native KPV (e.g., excisional/diabetic mouse wound) was retrievable — a notable gap given how heavily KPV is marketed for skin/wound repair.

### 7.3 Antimicrobial / antifungal — CONTESTED

- **Positive (originating lineage).** KPV (α-MSH 11-13), with α-MSH(1-13) and α-MSH(6-13), inhibited *S. aureus* colony formation and reduced *C. albicans* viability and germ-tube formation in vitro, down to the picomolar range; the candidacidal effect was attributed to raising fungal intracellular cAMP (cAMP rose in treated yeast; the adenylyl-cyclase inhibitor dideoxyadenosine partially reversed killing). Crucially, the peptides did **not** impair human-neutrophil killing of either organism — distinguishing them from conventional anti-inflammatories that blunt microbial clearance [1, in_vitro][8, mechanism_review].
- **Negative (independent replication — the integrity flag).** A later **independent** study synthesizing Ac-KPV-NH₂ (and glycoalkylated analogues) found **no antimicrobial activity** for capped KPV under a variety of standard microbiology conditions, while the glycoalkylated forms gained proteolytic stability. The KPV antimicrobial result is therefore **not robustly reproduced** and appears assay-condition-dependent [13, in_vitro].
- **Originating group concedes weak native activity.** A review from the originating lineage acknowledges that native α-MSH/KPV-type melanocortins have only **weak** antimicrobial activity in standard growth medium, motivating the design of more rigid synthetic analogues (Gly10-substituted MSH(6-13) scaffolds) with broad-spectrum activity — i.e., the strong antimicrobial promise sits with **engineered analogues, not unmodified KPV** [15, in_vitro][8, mechanism_review].
- **Engineered/dimerized derivatives (positive, but not the monomer).** A palmitoylated α-MSH(11-13) analogue conjugated to gold nanoparticles showed antibacterial activity against MSSA and MRSA in vitro (MIC ~18 µM for the conjugate, ~12 µM for free Pal-peptide) with biofilm inhibition [14, in_vitro]. And the **(CKPV)₂ dimer** cleared experimental *Candida albicans* vaginitis in rats: intravaginal (CKPV)₂ at 2 mg/kg/day drove vaginal *C. albicans* survival to ~12% by treatment day 11 (vs ~44.7% for miconazole 0.5 mg/kg), dose-dependently inhibited colony formation in vitro, and acted partly via MC1R-mediated cAMP induction and macrophage M1→M2 polarization [9, animal] (rat, female Sprague-Dawley, n=60 across groups; route: intravaginal gel).

**Net antimicrobial read:** native-KPV antimicrobial activity is **single-lineage positive + one independent negative + originating-group concession of weak activity** = **LOW confidence.** The robust antimicrobial signal belongs to **modified/dimerized/conjugated** derivatives, not native KPV.

### 7.4 "Other inflammation" — acne and gout are ANALOGUES, not KPV monomer

- **Acne = KdPT, not KPV.** In human SZ95 sebocytes (an in-vitro acne model), **KdPT** (not KPV) potently suppressed IL-1β-induced IL-6 and IL-8 expression by reducing IκBα degradation, p65 nuclear accumulation, and NF-κB DNA binding, lowering intracellular ROS, and decreasing IL-1β surface binding; molecular docking predicted KdPT binds IL-1R type I. KdPT did **not** bind MC1R (so no pigment/lipid induction) [6, in_vitro]. KPV-monomer-specific acne efficacy is unestablished.
- **Gout/MSU crystal arthritis = α-MSH + (CKPV)₂, not KPV monomer.** In MSU-crystal-induced inflammation, α-MSH and the KPV-dimer **(CKPV)₂** reduced MSU-stimulated monocyte→neutrophil priming, neutrophil chemotaxis, reactive-oxygen production, CD11b/TLR2/TLR4 expression, and IL-1β/IL-8/TNF-α/caspase-1 release. The active agents tested were α-MSH and (CKPV)₂ — **not the KPV monomer** [17, in_vitro] (human primary monocytes/neutrophils).

**Do not let the analogue data inflate KPV.** The widely repeated "KPV is good for acne / gout" claims trace to KdPT and (CKPV)₂, which are chemically distinct from the KPV monomer.

### 7.5 Mechanistic synthesis (extrapolation, not a single experiment)

Across studies, KPV efficacy in colitis is consistently attributed to **PepT1-mediated colonic uptake → NF-κB/MAPK inhibition → reduced TNF-α/IL-1β/IL-6 and MPO**, plus epithelial-barrier/mucosal-healing effects. This convergent mechanism is supported across the in-vivo and in-vitro claims above, but the **magnitude of clinical benefit in humans is unknown (no human data)** [synthesis].

### 7.6 Coverage gaps (Section 7)

- **No human data** — zero RCTs/open-label studies in any indication.
- **Effect-size precision is limited** — direction + significance reported, but exact deltas often paywalled; read as "significantly reduced," not precise numbers.
- **The 12,000× figure is single-lab and intra-study** — not an independently replicated property of KPV.
- **Native-KPV antimicrobial activity is fragile** — one positive lineage, one independent negative, originating-group concession; promise is for engineered/dimerized derivatives.
- **Acne and gout evidence is on analogues/dimers, not KPV monomer.**
- **No dermal (skin) wound-healing in-vivo model with native KPV** was retrievable.
- **Ocular:** KPV/KPV-dimer ophthalmic patents and α-MSH uveitis work surfaced, but no peer-reviewed KPV-specific ocular efficacy primary beyond the corneal-wound study; patents are not efficacy evidence.

---

## 8. Safety & Contraindications

**Headline:** human safety data on KPV is **essentially nonexistent.** All quantitative safety evidence is preclinical (animal/in-vitro). There are **no human RCTs, cohorts, or pharmacovigilance datasets.** This means AE *rates* in humans cannot be stated — only the *existence or absence of AEs in animals*, and uncontrolled human anecdote, can be described.

### 8.1 What the animal data show (existence-of-AE, not rates)

- In the foundational characterization, α-MSH(11-13) (KPV) inhibited histamine-induced vasopermeability/swelling dose-dependently; **no toxicity/AE was reported** at the doses tested (rodent; sample sizes not specified in the retrieved abstract) [1, animal].
- Oral KPV (100 µM in drinking water) reduced DSS colitis (C57BL/6, n=5/group) and TNBS colitis (n=10/group) with **no drug-attributable toxicity or adverse findings reported** (existence-of-AE: none reported — this is not a human AE rate) [2, animal].
- Orally delivered KPV via HA-functionalized nanoparticles (16 µg/kg/day ×5 days) alleviated ulcerative colitis in FVB mice; in vitro the KPV nanoparticles showed **no obvious cytotoxicity**, and treated mice had spleen weight, colon length, and colon histology **not significantly different from healthy controls** (existence-of-AE: none detected; not a human AE rate) [4, animal].

### 8.2 The unverified tolerability figures

Acute-toxicity narratives circulating in the secondary/practitioner literature claim that rodent studies failed to identify an LD50 (animals tolerating ≥100 mg/kg without mortality), implying a wide therapeutic window, and that chronic dosing (4–12 weeks) produced minimal adverse effects. **These specific dose figures could not be traced to any verifiable primary toxicology publication and are reported here only as practitioner-tier claims — treat as UNVERIFIED** [5, practitioner_protocol][6, vendor_label]. Reported real-world side effects in community/practitioner use are described as mild and self-limited (transient injection-site irritation, mild topical redness/itching, occasional mild GI discomfort) — but these are **uncontrolled anecdotal observations with no denominator** [5, practitioner_protocol][7, anecdote_aggregate].

### 8.3 Theoretical risks

- **Melanoma/pigmentation (residual theoretical concern).** Full-length α-MSH stimulates melanogenesis via MC1R and has been discussed as a theoretical proliferation concern. **KPV lacks the MC-receptor pharmacophore and does not stimulate pigmentation**, which is generally cited as *reducing* this concern. However, **no long-term human carcinogenicity data exist for KPV**, so the concern cannot be affirmatively cleared; practitioner sources nonetheless flag a history-of-cancer precaution [3, mechanism_review][5, practitioner_protocol].
- **Immunomodulation (open, not resolved).** KPV is an immunomodulator (it dampens pro-inflammatory cytokine production). The plausible theoretical risk is **blunted host defense** if used during active infection, in immunodeficiency, or alongside immunosuppressive drugs. Secondary sources assert KPV "does not suppress the immune system" systemically, but that is an over-strong claim given the absence of human immune-function data; treat the immunosuppression question as **open** [3, mechanism_review][5, practitioner_protocol].
- **Source/purity risk.** FDA's class-level concern for these peptides includes immunogenicity, peptide-related impurities, and incomplete active-ingredient characterization — meaning **product quality**, not just the molecule, is a risk vector for compounded or research-chemical KPV [9, regulatory][8, regulatory].

### 8.4 Contraindications / monitoring / stopping (as available)

- **No established human safety margin** — KPV has no human PK, dosing, or safety established by controlled research; this is itself the dominant risk-floor input [3, mechanism_review][8, regulatory].
- **Pregnancy / breastfeeding:** avoid — no safety data (practitioner precaution) [5, practitioner_protocol].
- **History of / active cancer:** caution / avoid pending clinician input — driven by the α-MSH melanocortin lineage and absence of carcinogenicity data [5, practitioner_protocol][3, mechanism_review].
- **Active infection / immunodeficiency / concurrent immunosuppressants:** caution — KPV is immunomodulatory [5, practitioner_protocol].
- **Objective monitoring (named assays, not a KPV-specific surrogate):** if KPV were used, objective monitoring would track **hs-CRP** (systemic inflammation; [[biomarkers/hs-crp]]), **fecal calprotectin** (objective gut-inflammation marker, for the IBD/gut use case), and **CBC + CMP** (general safety labs, warranted given KPV's immunomodulatory action). These are standard objective inflammation/safety assays — **NOT** validated surrogates of KPV activity; **no KPV-specific validated biomarker of effect exists** [3, mechanism_review][2, animal].
- **Stopping rule (inferable, not from a trial):** discontinue and seek care for any signs of worsening infection, allergic/injection-site reaction, or unexpected systemic symptoms. No KPV-specific validated monitoring panel and no KPV-specific biomarker-based stopping criterion is established (objective monitoring would use the general assays named above) [3, mechanism_review].

### 8.5 Coverage gaps (Section 8)

- **No human safety data of any tier** — every AE statement is animal existence-of-AE or uncontrolled anecdote; no human AE rate can be quoted.
- **No verifiable formal toxicology dossier** — the "no LD50 / ≥100 mg/kg / 4–12-wk chronic" figures trace only to practitioner/vendor sources; marked unverified.
- **Immunosuppression question is open, not resolved.**
- **EU/EMA and other jurisdictions** not affirmatively established beyond "no approval found."

---

## 9. Pharmacokinetics, Dose, Route & Formulation

> **Critical framing:** there is **no published human PK or human dose-finding study** for KPV. Everything below that resembles a "dose" is **practitioner convention**, tagged `practitioner_protocol`, used for **route/dose/cycle context ONLY — never as efficacy evidence.**

### 9.1 What is actually known about delivery

- **Oral is the best-supported route mechanistically**, because uptake is **PepT1-mediated** in inflamed gut epithelium [P1, animal] (= Dalmasso 2008). But a recurring preclinical theme is that **free oral KPV is delivery-limited** — it needs high doses, while nanoparticle/prodrug formulations work at far lower doses (§7.1). Any oral-dosing extrapolation should account for this.
- **Topical/transdermal** requires physical enhancement: plain topical KPV does not cross intact skin; microneedle poration ± iontophoresis is needed (§1.6).
- **No systemic/parenteral human PK** exists (§1.7).

### 9.2 Sourcing landscape (purity/formulation only — not efficacy)

- **Cosmetic/topical** is the oldest legitimate channel: a L'Oréal patent (WO2003002087A1) claims KPV for epidermal renewal at 10⁻¹²–10⁻³ M (preferred 10⁻⁹–10⁻⁴ M) in cosmetic compositions [S7, regulatory(patent)], and a US dermatological-use patent (US6894028B2) sits alongside the Lipton anti-inflammatory composition patents [S8, regulatory(patent)] — formulation/IP only.
- **Research-chem gray market (injectable — GRAY-MARKET FLAG):** KPV is sold widely online as a lyophilized "research only / not for human consumption" powder (commonly 5/10/15 mg vials). This is an **unregulated gray-market channel**; KPV is not an FDA-approved drug, so this material is research-grade and not established as fit for human use [S2/S3, vendor_label]. Vendors self-report HPLC ≥98–99% purity with optional batch-specific COAs (labs such as Janoshik, MZ Biolabs, Colmaric are named by sellers), but these are **vendor-commissioned and not buyer-auditable**; identity (is it actually Lys-Pro-Val?), endotoxin, and sterility for an injectable are the principal unverifiable risks. **No independent (non-vendor) purity survey of marketed KPV was retrieved.**

### 9.3 Practitioner dosing conventions (tagged practitioner_protocol — NOT efficacy)

- **Jay Campbell — JayCampbell.com, "KPV Peptide: Everything You Should Know"** (medically reviewed by Dr. Michael Fortunato, MD; last updated 29 Apr 2026): oral "two 250 [mc]g capsules … up to 2000 [mc]g/day depending on condition"; subcutaneous "200–500 mcg once a day"; topical cream "7.5 mg applied to affected area twice a day"; expects 3–4 weeks before results [S10, practitioner_protocol].
  - **⚠ Unit-error flag:** the oral figures are printed as "mg" (250 mg capsules, up to 2000 mg/day). Given that the SC range is in mcg and a 2000 mg/day oral tripeptide dose is implausible, this is almost certainly a **mg/mcg typo.** Do not propagate the "mg" figure without this caveat.
- **Jay Campbell — "KLOW" stack** (JayCampbell.com): KPV is described as a fourth component blended with BPC-157 + TB-500 + GHK-Cu in compounded multi-peptide vials — route/composition reference only [S11, practitioner_protocol].
- **Dr. Tyna Moore, ND, DC — interview, draliabadi.com** ("GLP-1 Microdosing, Peptides, Gut Health…", 2026-03-09): describes KPV as an anti-inflammatory peptide considered among the "least concerning for long-term use." Cycle/route framing only. (Note: this source pairs **TB-500 — not KPV — with BPC-157**; there is **no** practitioner-sourced KPV–BPC-157 pairing claim here) [S12, practitioner_protocol].
- **Anonymous aggregator pages** (peptides.org, peptidedossier.com, etc.) converge on oral 200–500 mcg/day (up to ~1 mg) and SC 250–500 mcg 1–2×/day, 4–8-week cycles. These do **not** meet the name+venue+date practitioner bar and are cited only to show consensus convergence, not as protocols [S13, anecdote_aggregate].

**Convergent practice picture (route/dose only):** oral low-mcg for gut indications; SC ~200–500 mcg/day for systemic; topical mg-scale for skin; short 2–8-week trials. **No published human dose-finding study exists**, so all of this is convention/extrapolation, not evidence-based dosing.

### 9.4 Coverage gaps (Section 9)

- **No human PK and no human dose-finding** — the entire dosing landscape is convention.
- **Free oral KPV is delivery-limited** — formulation matters; the cited mcg ranges are not validated.
- **The Campbell oral mg/mcg unit-error** illustrates how dosing misinformation propagates.
- **No independent purity survey** for gray-market injectable KPV; identity/endotoxin/sterility unverifiable from public sources.

---

## 10. N=1 / Trial-Design Considerations (goal-agnostic)

This section is **goal-agnostic** — it does not assume any particular operator goal. It outlines what a rigorous self-experiment would have to contend with, given the evidence state above.

1. **There is no human baseline to anchor on.** No human PK, no human dose-response, no validated biomarker of KPV effect. Any N=1 is exploratory by definition and cannot be benchmarked against a clinical literature, because none exists.
2. **The strongest preclinical signal is gut anti-inflammation via oral/lumenal PepT1 delivery.** If a self-experiment were contemplated, the gut domain is where the mechanism (PepT1 uptake, NF-κB suppression, colonic targeting during inflammation) is best worked out — and is also where free oral KPV is delivery-limited, so the dose actually reaching target tissue from a plain oral product is uncertain.
3. **Outcome measurement is the hard part.** Subjective "inflammation" endpoints are confounded and unblinded; for a gut indication, objective markers (e.g., fecal calprotectin, symptom-diary scoring) would be the only semi-credible readouts, and even those cannot distinguish KPV effect from regression to the mean or placebo in an uncontrolled N=1.
4. **Confounds and stacking.** KPV is frequently marketed inside multi-peptide stacks (e.g., the "KLOW" composition). Stacking destroys attribution — any N=1 intending to learn about KPV specifically must isolate it.
5. **Safety floor dominates design.** With no human safety dataset, an N=1 inherits all the open questions of §8 (immunomodulation during infection, source/purity for injectables, no validated monitoring panel). The conservative posture is to treat KPV as an experimental compound, keep cycles short, avoid use during active infection or immunosuppression, and involve a clinician — consistent with `doctor_discussion_required: true`.
6. **Regulatory/sport reality.** KPV is not lawfully compoundable and is prohibited in sport under S0 (§4); for any athlete this is disqualifying regardless of the biology.

The honest summary: KPV is a reasonable *mechanistic* candidate to think about, but the missing human PK, the delivery-limitation of free oral KPV, the absence of a validated readout, and the safety-data vacuum make a *clean, interpretable* N=1 very difficult.

---

## Post-fix refinement audit — objective-monitoring assays (§8.4)

**Trigger:** the Phase 7.5 risk-floor gate (health-gates.md §2) requires an experimental-tier compound's `monitoring` to name ≥1 OBJECTIVE lab assay or `[[biomarkers/<name>]]` (objective monitoring, not purely subjective/self-report). It does NOT require a compound-SPECIFIC validated biomarker. The prior §8.4 text ("No validated monitoring panel…") read as failing this gate.

**Edit (§8.4):** Added an "Objective monitoring (named assays…)" bullet naming standard objective assays a clinician would track IF KPV were used:
- **hs-CRP** — systemic inflammation — `[[biomarkers/hs-crp]]` (wiki entry exists → `vault/biomarkers/hs-crp.md`).
- **fecal calprotectin** — objective gut-inflammation marker (IBD/gut use case).
- **CBC + CMP** — general safety labs given KPV's immunomodulatory action (plain assays; no wiki entries exist, so unlinked).

**Honest caveat — PRESERVED:** the bullet states these are general objective inflammation/safety assays, **NOT validated surrogates of KPV activity**, and that **no KPV-specific validated biomarker of effect exists.** The stopping-rule bullet was reworded to "No KPV-specific validated monitoring panel…" so it no longer reads as "no objective monitoring at all" while keeping the honest negative. WADA/FDA facts and all other honest negatives unchanged.

**`[[biomarkers/hs-crp]]` resolves:** YES — correct form `[[biomarkers/hs-crp]]` (matches existing usage across the vault, e.g. meta/index.md, glyca.md).

---

## 11. Bottom Line — Supported vs Marketed

**What is genuinely supported (preclinical):**
- KPV is the C-terminal tripeptide of α-MSH that retains anti-inflammatory action while shedding the pigmentary action — a coherent, attractive premise.
- Its mechanism is unusually well-characterized for a tripeptide: intracellular NF-κB/MAPK suppression, melanocortin-receptor-independent in the key models, with PepT1-mediated cellular uptake whose **necessity is proven by a clean knockout result.**
- In **rodent colitis**, the **direction** of benefit replicates across ≥4 independent labs, two species, four models, and three routes — the strongest thing KPV has.

**What is marketed but NOT supported:**
- **Any human efficacy or safety claim.** There is zero human evidence of any design; the most-cited "human skin" paper is an ex-vivo permeation study, not a trial.
- **KPV's inherent potency framed via the "12,000×" figure** — that is a single-lab, intra-study delivery-formulation comparison, not a property of KPV.
- **Native-KPV antimicrobial activity** — contested (one positive lineage, one independent null, plus the originating group conceding weak native activity); the real antimicrobial signal belongs to engineered/dimerized derivatives.
- **Acne and gout "efficacy"** — those belong to the analogues **KdPT** and **(CKPV)₂**, not the KPV monomer; conflating them inflates KPV.
- **Topical-skin and atopic-dermatitis claims** (e.g., "40% faster wound closure," "lowers IgE in NC/Nga mice") — no retrievable primary supports these; the real KPV repair data are mucosal, not dermal.
- **"Wide therapeutic window / no LD50" tolerability** — untraceable to any primary toxicology study; unverified.

**Net:** KPV is a **mechanistically attractive, preclinically promising, clinically unproven** experimental compound. Its best real signal is gut anti-inflammation in rodents, concentrated heavily in one lab for magnitude; it has **no human evidence**, **no human safety data**, a **contested** antimicrobial claim, and a marketing footprint that borrows liberally from chemically distinct analogues. It is unapproved, not lawfully compoundable, and prohibited in sport. Treat all human-use framing as off-label experimentation, and discuss with a clinician.

---

## Citation numbering note + crosswalk

> **The unified Bibliography below is the canonical citation list.** Every source is listed there once under a single unified number `[N]` (N = 1–47). **Resolve every reference by the unified Bibliography.**
>
> A traceability caveat the reader must know: the section bodies above were drafted under **per-section local numbering**, and those inline local numbers do **not** map one-to-one to the unified Bibliography numbers. The same paper can appear under different local numbers in different sections (e.g., Dalmasso 2008 is local `[2]` in §1–§2 but local `[1]` in §7.1 and local `[P1]` in §9), and — within §7 — the same local token can denote two different papers in different subsections (e.g., §7.1 local `[4, animal]` = Xiao 2017 nanoparticle, but §7.2 local `[4, animal]` = Shao 2022 oral-mucositis hydrogel). An inline local `[N]` therefore must be resolved through the crosswalk below, **not** by reading it straight off the Bibliography. The underlying mapping was attested PASS by the upstream Phase-4.25 ID-reconcile and Phase-4.75 citation-integrity gate; the crosswalk simply makes that mapping reconstructable from the published artifact. No inline reference is dangling.
>
> **How to read the crosswalk:** find the section (and, where noted, the subsection/subject), then read across to the unified Bibliography number.

| Section | Inline local token | Subject / paper | → Unified |
|---|---|---|---|
| §1 | `[1, animal] / [1, in_vitro]` | Getting 2003 (MSU peritonitis, MC1R e/e, no cAMP) | **[1]** |
| §1 | `[2, …] / [2]` | Dalmasso 2008 (PepT1 colitis, Caco2-BBE) | **[2]** |
| §1 | `[3, in_vitro] / [3]` | Pawar 2017 (transdermal Franz cells) | **[26]** |
| §1 | `[4, animal] / [4, in_vitro]` | Bettenworth 2011 (KdPT) | **[4]** |
| §1 | `[5, mechanism_review]` | Brzoska 2008 (α-MSH/tripeptide review) | **[5]** |
| §1 | `[6, regulatory]` | PubChem CID 125672 (chemistry) | **[6]** |
| §1 | `[9, vendor_label]` | vendor labels (rejected MW "~400 Da") | **[47]** |
| §2 | `[1, mechanism_review] / [1]` | Getting 2003 | **[1]** |
| §2 | `[2, animal] / [2, in_vitro]` | Dalmasso 2008 | **[2]** |
| §2 | `[3, in_vitro] / [3]` | Land 2012 (importin-α3/p65, 16HBE) | **[3]** |
| §2 | `[4, animal]` | Kannengiesser 2008 (MC1R e/e colitis) | **[11]** |
| §2 | `[5, in_vitro]` | Mandrika 2001 (RAW 264.7 dual mechanism) | **[10]** |
| §2 | `[6, mechanism_review]` | Brzoska 2008 (message/HFRW-motif review) | **[5]** |
| §2 | `[7, animal]` | Viennois 2016 (PepT1-KO CAC necessity) | **[7]** |
| §2 | `[8, in_vitro]` | Cutuli 2000 (antimicrobial, originating) | **[8]** |
| §3 | `[1, regulatory]` | ClinicalTrials.gov registry null | **[27]** |
| §3 | `[2, regulatory]` | EU/EudraCT/CTIS registry null | **[28]** |
| §3 | `[3, anecdote_aggregate→null]` | PubMed KPV census | **[29]** |
| §3 | `[4, regulatory]` | ClinicalTrials.gov registry null (corroboration) | **[27]** |
| §3 | `[5, anecdote_aggregate→null]` | PMC KdPT census | **[30]** |
| §3 | `[6, regulatory]` | Pawar 2017 (ex-vivo skin trap) | **[26]** |
| §3 | `[7, anecdote_aggregate→null]` | PMC KdPT census / KdPT-null | **[30]** |
| §3 | `[8, regulatory]` | FDA 503A page (not approved) | **[31]** |
| §3 | `[9, anecdote_aggregate]` | practitioner/vendor guides | **[45]** |
| §3 | `[10, anecdote_aggregate]` | anecdote community aggregations | **[46]** |
| §4 | `[8, regulatory]` | FDA 503A page (not approved) | **[31]** |
| §4 | `[9, regulatory]` | Frier Levitt (503A / Cat-2 removal) | **[33]** |
| §4 | `[10, regulatory]` | NLR / FDA Law Blog (PCAC non-binding + rulemaking) | **[32]** |
| §4 | `[11, regulatory]` | WADA 2026 Prohibited List (not named) | **[37]** |
| §4 | `[12, regulatory]` | WADA 2026 change summary | **[38]** |
| §4 | `[13, regulatory]` | BSCG (S0 catch-all explainer) | **[39]** |
| §4 | `[14, regulatory]` | Cat-2-removal corroboration | **[34]** |
| §4 | `[15, regulatory]` | RAPS (2023 placement; PCAC dates) | **[35]** |
| §4 | `[S1, regulatory]` | RAPS (original 2023 Cat-2 placement) | **[35]** |
| §4 | (PCAC meeting page) | FDA advisory-committee calendar | **[36]** |
| §5 | `[4 in §7]` | Xiao 2017 (the "~12,000×" figure) | **[12]** |
| §7.1 | `[1, animal] / [1, in_vitro]` | Dalmasso 2008 (foundational oral colitis) | **[2]** |
| §7.1 | `[2, animal]` | Kannengiesser 2008 (German independent replication) | **[11]** |
| §7.1 | `[3, animal]` | Viennois 2016 (PepT1-KO CAC) | **[7]** |
| §7.1 | `[4, animal]` | Xiao 2017 (HA-NP, 12,000× figure) | **[12]** |
| §7.1 | `[5, animal]` | Cheng 2026 (proKPV prodrug, Sci Adv) | **[13]** |
| §7.1 | `[6, animal]` | Zhang 2024 (KPV+FK506 nanodrug, IV) | **[14]** |
| §7.1 | `[7, animal]` | Acta Biomater 2022 (rat TNBS rectal hydrogel) | **[15]** |
| §7.2 | `[4, animal] / [4, in_vitro]` | Shao 2022 (oral-mucositis hydrogel) | **[21]** |
| §7.2 | `[10, animal] / [10, in_vitro]` | Xiao 2017 (colonic mucosal healing) | **[12]** |
| §7.2 | `[12, animal]` | Hiltz/Lipton 1990 (contact sensitivity) | **[22]** |
| §7.2 | `[5, animal] / [5, in_vitro]` | Bettenworth 2011 (KdPT wound/barrier) | **[4]** |
| §7.3 | `[1, in_vitro]` | Cutuli 2000 (antimicrobial positive) | **[8]** |
| §7.3 | `[8, mechanism_review]` | Catania 2006 (antimicrobial review) | **[9]** |
| §7.3 | `[13, in_vitro]` | Songok 2018 (antimicrobial null) | **[16]** |
| §7.3 | `[14, in_vitro]` | Mitra 2022 (palmitoylated/gold-NP analogue) | **[17]** |
| §7.3 | `[15, in_vitro]` | Grieco 2013 (engineered analogues) | **[18]** |
| §7.3 | `[9, animal]` | Ji 2013 ((CKPV)₂ vaginitis) | **[20]** |
| §7.4 | `[6, in_vitro]` | Mastrofrancesco 2010 (KdPT sebocytes/acne) | **[19]** |
| §7.4 | `[17, in_vitro]` | Capsoni 2009 (α-MSH+(CKPV)₂ gout/MSU) | **[24]** |
| §8 | `[1, animal]` | Getting 2003 (vasopermeability, no AE reported) | **[1]** |
| §8 | `[2, animal]` | Dalmasso 2008 (oral KPV colitis, no AE) | **[2]** |
| §8 | `[3, mechanism_review]` | Brzoska 2008 (theoretical-risk framing) | **[5]** |
| §8 | `[4, animal]` | Xiao 2017 (HA-NP, no cytotoxicity) | **[12]** |
| §8 | `[5, practitioner_protocol]` | practitioner guides (unverified LD50/precautions) | **[45]** |
| §8 | `[6, vendor_label]` | vendor labels (unverified ≥100 mg/kg) | **[47]** |
| §8 | `[7, anecdote_aggregate]` | anecdote side-effect aggregations | **[46]** |
| §8 | `[8, regulatory]` | FDA 503A page (purity/class concern) | **[31]** |
| §8 | `[9, regulatory]` | NLR / FDA Law Blog (class-level concern) | **[32]** |
| §9 | `[P1, animal]` | Dalmasso 2008 (= explicitly Dalmasso 2008) | **[2]** |
| §9 | `[S2/S3, vendor_label]` | research-chem vendor labels | **[47]** |
| §9 | `[S7, regulatory(patent)]` | L'Oréal WO2003002087A1 | **[40]** |
| §9 | `[S8, regulatory(patent)]` | US6894028B2 | **[41]** |
| §9 | `[S10, practitioner_protocol]` | Campbell — KPV article | **[42]** |
| §9 | `[S11, practitioner_protocol]` | Campbell — KLOW stack | **[43]** |
| §9 | `[S12, practitioner_protocol]` | Moore interview | **[44]** |
| §9 | `[S13, anecdote_aggregate]` | aggregator dosing pages | **[46]** |

> Sections 6, 10, and 11 are synthesis/cross-reference and carry no numbered inline citations of their own (they point back to the sections above). The frontmatter "Read this first" block and the TL;DR are likewise un-numbered summaries.

---

## Bibliography

> Unified and deduped across all seven validated sections. **This list is canonical; inline local `[N]` tokens resolve to it via the "Citation numbering note + crosswalk" immediately above.** Each entry: `[N] Author Y, "Title", Journal Year. PMID/DOI/URL. tag=. tier=.` Where the same paper appeared under different local section numbers, it is listed once here. Per-section `## Post-fix grep audit` blocks were excluded per instructions.

**Primary preclinical (animal / in-vitro):**

[1] Getting SJ, Schiöth HB, Perretti M. "Dissection of the anti-inflammatory effect of the core and C-terminal (KPV) alpha-melanocyte-stimulating hormone peptides." *J Pharmacol Exp Ther.* 2003;306(2):631-637. PMID: 12750433. DOI: 10.1124/jpet.103.051623. tag=animal/in_vitro. tier=1.

[2] Dalmasso G, Charrier-Hisamuddin L, Nguyen HTT, Thomas-Gatewood C, Datta D, Laroui H, Yan Y, Sitaraman SV, Merlin D. "PepT1-mediated tripeptide KPV uptake reduces intestinal inflammation." *Gastroenterology.* 2008;134(1):166-178. PMID: 18061177. DOI: 10.1053/j.gastro.2007.10.026. tag=animal/in_vitro/mechanism_review. tier=1. (Foundational KPV-colitis paper; Merlin/GSU lineage. The single most-cited KPV-IBD source — and it is mouse, not human.)

[3] Land SC. "Inhibition of cellular and systemic inflammation cues in human bronchial epithelial cells by melanocortin-related peptides: mechanism of KPV action and a role for MC3R agonists." *Int J Physiol Pathophysiol Pharmacol.* 2012;4(2):59-73. PMID: 22837805. PMCID: PMC3403564. tag=in_vitro. tier=1. (The KPV-specific importin-α3/p65 mechanism — single-lab.)

[4] Bettenworth D, Buyse M, Böhm M, Mennigen R, Czorniak I, Kannengiesser K, Brzoska T, Luger TA, Kucharzik T, Domschke W, Maaser C, Lügering A. "The tripeptide KdPT protects from intestinal inflammation and maintains intestinal barrier function." *Am J Pathol.* 2011;179(3):1230-1242. PMID: 21741932. DOI: 10.1016/j.ajpath.2011.05.013. PMCID: PMC3157275. tag=animal/in_vitro. tier=1. (KdPT = Lys-D-Pro-Thr — a DIFFERENT molecule from KPV; cited for the non-conflation boundary.)

[5] Brzoska T, Luger TA, Maaser C, Abels C, Böhm M. "α-Melanocyte-Stimulating Hormone and Related Tripeptides: Biochemistry, Antiinflammatory and Protective Effects in Vitro and in Vivo, and Future Perspectives for the Treatment of Immune-Mediated Inflammatory Diseases." *Endocr Rev.* 2008;29(5):581-602. PMID: 18612139. DOI: 10.1210/er.2007-0027. tag=mechanism_review. tier=1.

[6] National Center for Biotechnology Information. "PubChem Compound Summary for CID 125672, MSH (11-13) / Lys-Pro-Val (KPV)." PubChem. URL: https://pubchem.ncbi.nlm.nih.gov/compound/125672 (retrieved 2026-06-19). tag=regulatory. tier=1. (Authoritative chemistry: C₁₆H₃₀N₄O₄; MW 342.43; CAS 67727-97-3; IUPAC name; SMILES.)

[7] Viennois E, Ingersoll SA, Ayyadurai S, Zhao Y, Wang L, Zhang M, Han MK, Garg P, Xiao B, Merlin D. "Critical Role of PepT1 in Promoting Colitis-Associated Cancer and Therapeutic Benefits of the Anti-inflammatory PepT1-Mediated Tripeptide KPV in a Murine Model." *Cell Mol Gastroenterol Hepatol.* 2016;2(3):340-357. PMID: 27458604. DOI: 10.1016/j.jcmgh.2016.01.006. tag=animal. tier=1. (PepT1-KO loss-of-effect = causal necessity; Merlin/GSU.)

[8] Cutuli M, Cristiani S, Lipton JM, Catania A. "Antimicrobial effects of alpha-MSH peptides." *J Leukoc Biol.* 2000;67(2):233-239. PMID: 10670585. DOI: 10.1002/jlb.67.2.233. tag=in_vitro (+ animal). tier=1. (Positive KPV antimicrobial result — Catania/Lipton lineage; contested by [13].)

[9] Catania A, Colombo G, Rossi C, Carlin A, Sordi A, Lonati C, Turcatti F, Leonardi P, Grieco P, Gatti S. "Antimicrobial properties of alpha-MSH and related synthetic melanocortins." *TheScientificWorldJournal.* 2006;6:1241-1246. PMID: 17028769. DOI: 10.1100/tsw.2006.227. PMCID: PMC5917254. tag=mechanism_review. tier=1.

[10] Mandrika I, Muceniece R, Wikberg JE. "Effects of melanocortin peptides on lipopolysaccharide/interferon-gamma-induced NF-kappaB DNA binding and nitric oxide production in macrophage-like RAW 264.7 cells: evidence for dual mechanisms of action." *Biochem Pharmacol.* 2001;61(5):613-621. PMID: 11239505. DOI: 10.1016/s0006-2952(00)00583-9. tag=in_vitro. tier=1. (Context for the parent α-MSH dual receptor-dependent/independent mechanism.)

[11] Kannengiesser K, Maaser C, Heidemann J, Luegering A, Ross M, Brzoska T, Böhm M, Luger TA, Domschke W, Kucharzik T. "Melanocortin-derived tripeptide KPV has anti-inflammatory potential in murine models of inflammatory bowel disease." *Inflamm Bowel Dis.* 2008;14(3):324-331. PMID: 18092346. DOI: 10.1002/ibd.20334. tag=animal. tier=1. (INDEPENDENT replication, U Münster; DSS + transfer colitis; MC1R e/e. Note: an earlier draft mis-recorded PMID 17973296 — corrected to 18092346.)

[12] Xiao B, Xu Z, Viennois E, Zhang Y, Zhang Z, Zhang M, Han MK, Kang Y, Merlin D. "Orally Targeted Delivery of Tripeptide KPV via Hyaluronic Acid-Functionalized Nanoparticles Efficiently Alleviates Ulcerative Colitis." *Mol Ther.* 2017;25(7):1628-1640. PMID: 28143741. DOI: 10.1016/j.ymthe.2016.11.020. PMCID: PMC5498804. tag=animal/in_vitro. tier=1. (Source of the "~12,000×" figure — single-lab, intra-study formulation comparison.)

[13] Cheng J, Wu P, Li C, Han Y, Sun M, Dou Y, Chen S, Zhang J. "Inflammation-triggered self-immolative conjugates enable oral peptide delivery by overcoming gastrointestinal barriers." *Sci Adv.* 2026;12(3):eaea2989. PMID: 41533788. PMCID: PMC12802832. DOI: 10.1126/sciadv.aea2989. tag=animal. tier=1. (INDEPENDENT proKPV prodrug; Army Medical University.)

[14] Zhang D, Jiang L, Yu F, Yan P, Liu Y, Wu Y, Yang X. "PepT1-targeted nanodrug based on co-assembly of anti-inflammatory peptide and immunosuppressant for combined treatment of acute and chronic DSS-induced colitis." *Front Pharmacol.* 2024;15:1442876. PMID: 39211778. PMCID: PMC11357942. DOI: 10.3389/fphar.2024.1442876. tag=animal. tier=1. (INDEPENDENT; KPV+FK506, IV route.)

[15] "A KPV-binding double-network hydrogel restores gut mucosal barrier in an inflamed colon." *Acta Biomater.* 2022;143:233-252. PMID: 35245681. DOI: 10.1016/j.actbio.2022.02.039. tag=animal. tier=1. (INDEPENDENT; RAT TNBS, rectal route.)

[16] Songok AC, Panta P, Doerrler WT, Macnaughtan MA, Taylor CM. "Structural modification of the tripeptide KPV by reductive 'glycoalkylation' of the lysine residue." *PLoS ONE.* 2018;13(6):e0199686. PMID: 29953505. DOI: 10.1371/journal.pone.0199686. PMCID: PMC6023233. tag=in_vitro. tier=1. (NEGATIVE/contradictory antimicrobial result — independent of the originating lineage; critical for honest antimicrobial appraisal.)

[17] Mitra S, Mondal AH, Mukhopadhyay K. "Mitigating the toxicity of palmitoylated analogue of α-melanocyte stimulating hormone(11-13) by conjugation with gold nanoparticle: characterisation and antibacterial efficacy against methicillin sensitive and resistant Staphylococcus aureus." *World J Microbiol Biotechnol.* 2022;38(11):186. PMID: 35972627. DOI: 10.1007/s11274-022-03365-7. PMCID: PMC9379238. tag=in_vitro. tier=1. (Modified KPV-derived construct, not native KPV.)

[18] Grieco P, Carotenuto A, Auriemma L, et al. "Novel α-MSH peptide analogues with broad spectrum antimicrobial activity." *PLoS ONE.* 2013;8(4):e61614. PMID: 23626703. DOI: 10.1371/journal.pone.0061614. PMCID: PMC3634028. tag=in_vitro. tier=1. (Engineered Gly10-substituted analogues; native melanocortins weak in standard medium.)

[19] Mastrofrancesco A, Kokot A, Eberle A, Gibbons NCJ, Schallreuter KU, Strozyk E, Picardo M, Zouboulis CC, Luger TA, Böhm M. "KdPT, a tripeptide derivative of alpha-melanocyte-stimulating hormone, suppresses IL-1β-mediated cytokine expression and signaling in human sebocytes." *J Immunol.* 2010;185(3):1903-1911. PMID: 20610647. DOI: 10.4049/jimmunol.0902298. tag=in_vitro. tier=1. (Acne = KdPT analogue, NOT KPV monomer.)

[20] Ji H-x, Zou Y-l, Duan J-j, et al. "The synthetic melanocortin (CKPV)₂ exerts anti-fungal and anti-inflammatory effects against Candida albicans vaginitis via inducing macrophage M2 polarization." *PLoS ONE.* 2013;8(2):e56004. DOI: 10.1371/journal.pone.0056004. tag=animal. tier=1. ((CKPV)₂ dimer, NOT KPV monomer.)

[21] Shao W, Chen R, Lin G, et al. "In situ mucoadhesive hydrogel capturing tripeptide KPV: the anti-inflammatory, antibacterial and repairing effect on chemotherapy-induced oral mucositis." *Biomater Sci.* 2022;10(1):227-242. PMID: 34846053. DOI: 10.1039/D1BM01466H. tag=animal/in_vitro. tier=1. (Rat oral-mucositis model; KPV hydrogel.)

[22] Hiltz ME, Lipton JM. "Alpha-MSH peptides inhibit acute inflammation and contact sensitivity." *Peptides.* 1990;11(5):979-982. PMID: 2284205. DOI: 10.1016/0196-9781(90)90020-6. tag=animal. tier=1. (Foundational cutaneous-inflammation evidence for KPV.)

[23] Hiltz ME, Lipton JM. "Antiinflammatory activity of a COOH-terminal fragment of the neuropeptide α-MSH." *FASEB J.* 1989;3(11):2282-2284. PMID: 2550304. DOI: 10.1096/fasebj.3.11.2550304. tag=animal. tier=1. (Distinct earlier foundational paper; verified as a different publication from [22].)

[24] Capsoni F, Ongari AM, Reali E, Catania A. "Melanocortin peptides inhibit urate crystal-induced activation of phagocytic cells." *Arthritis Res Ther.* 2009;11(5):R151. PMID: 19814819. DOI: 10.1186/ar2827. PMCID: PMC2787256. tag=in_vitro. tier=1. (Gout/MSU = α-MSH + (CKPV)₂, NOT KPV monomer.)

[25] Bonfiglio V, Camillieri G, Avitabile T, Leggio GM, Drago F. "Effects of the COOH-terminal tripeptide α-MSH(11-13) on corneal epithelial wound healing: role of nitric oxide." *Exp Eye Res.* 2006;83(6):1366-1372. PMID: 16965771. tag=animal. tier=1. (INDEPENDENT; rabbit corneal wounds; NO-dependent.)

**Pharmaceutics / delivery (in-vitro / ex-vivo human tissue — NOT clinical):**

[26] Pawar K, Kolli CS, Rangari VK, Babu RJ. "Transdermal Iontophoretic Delivery of Lysine-Proline-Valine (KPV) Peptide Across Microporated Human Skin." *J Pharm Sci.* 2017;106(7):1814-1820. PMID: 28343991. DOI: 10.1016/j.xphs.2017.03.017. tag=in_vitro. tier=2. (EX-VIVO excised human skin in Franz cells — NOT a clinical trial; commonly mis-cited as "human evidence.")

**Regulatory / anti-doping / registry:**

[27] ClinicalTrials.gov registry queries (intervention/term "KPV"; term "Lys-Pro-Val"; term "KdPT"), accessed 2026-06-19. URLs: https://clinicaltrials.gov/api/v2/studies?query.intr=KPV ; https://clinicaltrials.gov/api/v2/studies?query.term=KdPT . tag=regulatory. tier=1. (KPV and KdPT each return zero studies.)

[28] EU clinical-trials registry / EudraCT / CTIS search for "KdPT"/"KPV" in IBD/AD/psoriasis, accessed 2026-06-19. tag=regulatory. tier=2. (No registered or completed EU trial.)

[29] PubMed census, "KPV peptide" (~50+ records), accessed 2026-06-19. URL: https://pubmed.ncbi.nlm.nih.gov/?term=KPV+peptide . tag=regulatory. tier=1. (All therapeutic records are animal/in-vitro/reviews/formulation; no human clinical trial.)

[30] PMC census, "KdPT peptide" (~39 records) + web search for KdPT psoriasis/AD human trials, accessed 2026-06-19. URL: https://pmc.ncbi.nlm.nih.gov/search/?term=KdPT+peptide . tag=regulatory. tier=1. (No completed human KdPT trial.)

[31] FDA. "Bulk Drug Substances Used in Compounding Under Section 503A of the FD&C Act." fda.gov. URL: https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding-under-section-503a-fdc-act. tag=regulatory. tier=1. (503A Category 1/2 framework; KPV historically Cat-2, removed ~Apr 2026 — see [33][34].)

[32] National Law Review / FDA Law Blog peptide-compounding coverage. URLs: https://natlawreview.com/article/tiny-chains-big-changes-what-fdas-latest-actions-mean-peptide-compounding ; https://www.thefdalawblog.com/2026/04/fdas-peptide-rally-what-compounders-and-industry-need-to-know-post-1-of-2/ . tag=regulatory. tier=2. (FDA class-level safety rationale; July 2026 PCAC; non-binding + rulemaking caveat.)

[33] Frier Levitt. "FDA to Remove 12 Popular Peptides from the Category 2 'Do Not Compound' List." URL: https://www.frierlevitt.com/articles/fda-peptides-do-not-compound-list-update-2026/ . tag=regulatory. tier=2. (PRIMARY CORRECTION SOURCE: KPV removed from interim Category 2 ~15 Apr 2026, item #7 of 12, nomination withdrawn; "removal … does not render these bulk drug substances eligible for compounding under section 503A"; PCAC 23 Jul 2026.)

[34] FDA peptide-reclassification / Category-2-removal corroboration. URLs: https://thepeptidecatalog.com/articles/fda-removes-12-peptides-category-2-april-22 ; https://newtropin.com/blog/fda-503a-category-update-april-2026/ ; https://www.getpeptidewise.com/blog/fda-peptide-reclassification-2026/ . tag=regulatory. tier=2. (Corroborates 12-peptide Apr 2026 removal incl. KPV; PCAC slate; Federal Register 16 Apr 2026 notice; removal ≠ approval.)

[35] RAPS. "FDA considers adding a dozen peptides to its bulk drug compounding list." raps.org, 2026-04-16. URL: https://www.raps.org/resource/fda-considers-adding-a-dozen-peptides-to-its-bulk-drug-compounding-list.html . tag=regulatory. tier=1. (KPV free base + acetate; PCAC 23–24 Jul 2026; original 2023 Cat-2 placement.)

[36] FDA. PCAC (Pharmacy Compounding Advisory Committee) meeting, 23–24 July 2026, peptide agenda incl. KPV. fda.gov advisory-committee calendar. tag=regulatory. tier=1. (Meeting page returned 404 at fetch time; date/agenda corroborated by [32][33][34][35].)

[37] WADA. "The 2026 Prohibited List" (International Standard), in force 1 January 2026. URL: https://www.wada-ama.org/en/resources/2026-prohibited-list . tag=regulatory. tier=1. (S0 definition; KPV/tripeptide/melanocortin not individually named.)

[38] WADA 2026 Prohibited List change summary. URL: https://www.iwbf.org/news/wadas-2026-prohibited-list-now-in-force . tag=regulatory. tier=2. (No tripeptide/KPV/melanocortin addition — supports "not explicitly listed.")

[39] BSCG. "WADA Prohibited List — Banned Drugs and Supplement Risks" (S0 explainer) + "What's Changing with Peptide Regulation in 2026." URLs: https://www.bscg.org/wada-prohibited-list-banned-drugs-and-supplement-risks ; https://www.bscg.org/blogs/single/whats-changing-with-peptide-regulation-in-2026 . tag=regulatory. tier=2. (S0 catch-all applies to unapproved/research peptides — KPV caught by mechanism, not by name.)

**Patents / cosmetic-use IP (formulation only — NOT efficacy):**

[40] L'Oréal SA (inventor Mahé Y). "Use of a Lys-Pro-Val (KPV) tripeptide in cosmetics." WO2003002087A1; priority 2001-06-29, pub. 2003-01-09. tag=regulatory(patent). tier=2. (Cosmetic conc. 10⁻¹²–10⁻³ M; formulation only.)

[41] "Use of KPV tripeptide for dermatological disorders." US6894028B2. tag=regulatory(patent). tier=2. (Dermatological-use patent; IP only.)

**Practitioner / vendor / anecdote (dose/route/context ONLY — never efficacy or AE rate):**

[42] Campbell J (med-reviewed Fortunato M, MD). "KPV Peptide: Everything You Should Know." JayCampbell.com, last updated 2026-04-29. URL: https://jaycampbell.com/gut-health/kpv-the-anti-inflammatory-peptide/ . tag=practitioner_protocol. tier=2.7 (dose/route only; oral mg/mcg unit-error flagged).

[43] Campbell J. "KLOW peptide protocol" (BPC-157 + TB-500 + GHK-Cu + KPV). JayCampbell.com peptides section, 2024–2026. tag=practitioner_protocol. tier=2.7 (composition/route only).

[44] Moore T (ND, DC), interview, draliabadi.com, "GLP-1 Microdosing, Peptides, Gut Health…", 2026-03-09. URL: https://www.draliabadi.com/blog/glp1-microdosing-peptides-gut-health-women-guide/ . tag=practitioner_protocol. tier=2.7 (KPV among "least concerning for long-term use"; cycle/route framing only — source pairs TB-500, not KPV, with BPC-157).

[45] Practitioner/vendor KPV research guides (e.g., meetpeptide.com, drdanwool.com, innerbody.com) and vendor monographs (e.g., peptidebiologix.com, aminoclub.com). tag=practitioner_protocol / vendor_label. tier=3. (Source of the UNVERIFIED LD50/dose figures and contraindication precautions; qualitative only; never grounds a numeric AE rate.)

[46] Anecdotal community side-effect aggregations + anonymous aggregator dosing pages (e.g., realpeptides.co, pepdose.com, peptides.org, peptidedossier.com). tag=anecdote_aggregate. tier=3. (No denominator; consensus-convergence context only.)

[47] Research-chemical vendor labels + vendor COA practice (e.g., Limitless Biotech, researchchemical.com, DL Peptides; COAs from Janoshik / MZ Biolabs / Colmaric named by sellers). tag=vendor_label. tier=4. (GRAY-MARKET; purity/reconstitution context only; self-reported ≥98–99% HPLC, not buyer-auditable; also the rejected MW "~400 Da" discrepancy flag.)

---

## Provenance & Citation-Integrity Note

This report is a Phase-5 synthesis over a corpus that passed the full upstream pipeline: **deep paired-judge review @99**, **Phase-4.25 ID-reconcile = PASS** (no cross-section mismatches; the KPV-vs-KdPT distinction held cleanly everywhere; FDA-503A-removal date concordant across sections; human-trial-count = 0 consistent across sections E/F/G), and the **Phase-4.75 citation-integrity gate = PASS** (13 IC checks; two non-blocking WARNs — IC-1 tag-notation style for `(patent)`/`→null` decorations on otherwise valid base tags, and IC-13 paywalled full-text magnitude figures recorded as corpus-missing, not HALT). Canonical reconciled values carried forward verbatim: **Dalmasso 2008 = PMID 18061177; Kannengiesser 2008 = PMID 18092346** (an earlier draft's erroneous PMID 17973296 was corrected upstream); **KPV ≠ KdPT**; **FDA removed KPV from 503A Category 2 ~15 April 2026** (removal ≠ approval). The concentration audit's single-lab shares (50% all-cause, 75% gut/IBD, ≥70% flag) were independently re-derived in Phase-4.25 and reproduced exactly.

This synthesis was performed **corpus-read-only**: no new web retrieval was conducted, no citation or number was invented, and every claim traces to the validated sections' verified citations. Where the upstream pipeline substituted **WebSearch/WebFetch** for the intended Tavily MCP retrieval tool, that substitution is noted in the upstream gates and does not affect the citations carried here. Per-section `## Post-fix grep audit` blocks were treated as remediation metadata and excluded from the synthesized content. Tier-3/4 practitioner/vendor/anecdote sources are used strictly for dose/route/sourcing context and never to ground efficacy or AE-rate numbers.

---

## Post-fix refinement audit (Phase 7)

**Scope.** Address the Phase-6 critique (`gate-6.md`, verdict PASS, no CRITICAL) without introducing any new external citation (corpus frozen). No verified value, identifier, species+n, or honest negative was changed.

**MAJOR finding — citation traceability (FIXED).**
- The dual numbering scheme (section-local inline `[N, tag]` not mapping to the unified Bibliography) was the one major finding. Fixed by adding **`## Citation numbering note + crosswalk`** immediately before the Bibliography (mirroring the GHK-Cu report's "unified list is canonical" disclosure), with a **72-row section-local → unified crosswalk table** plus an explicit declaration that the unified Bibliography is canonical. The cleanest resolver was chosen over renumbering 200+ inline cites (which would risk breaking the upstream-attested Phase-4.25 mappings). The crosswalk is keyed by **section** and, in §7 where one local token denotes two different papers across subsections (e.g., §7.1 `[4]` = Xiao vs §7.2 `[4]` = Shao), by **subsection/subject** so every inline token resolves unambiguously. The Bibliography header now points to the crosswalk and re-declares canonicity.

**MINOR findings (gate-6) — disposition:**
1. *Zero-human-evidence carried pervasively* — confirmation, no fix required (gate-6 self-noted). **Accepted as-is.**
2. *Merlin single-lab concentration carried fairly* — confirmation. **Accepted as-is.**
3. *Contested antimicrobial balanced* — confirmation. **Accepted as-is.**
4. *Monomer-vs-analogue discipline consistent* — confirmation. **Accepted as-is.**
5. *§5.2 denominator classification slightly soft (Cutuli/Bonfiglio counted as in-vivo efficacy primaries)* — **FIXED (label tighten, no new cite):** P5 Bonfiglio annotated *non-gut domain*; P6 Cutuli annotated *in-vitro-lead (tagged `in_vitro (+ animal)` in §7.3/Bibliography); counted only for the all-cause denominator*. §5.6 already self-disclosed this; the table now flags it inline too. No number changed; the headline gut/IBD 75% is unaffected.
6. *Tone non-promotional* — confirmation. **Accepted as-is.**
7. *Overstatement traps all avoided* — confirmation. **Accepted as-is.**
8. *Regulatory/WADA accurate* — confirmation. **Accepted as-is.**
9. *Missing-perspective: removal-by-withdrawal ≠ vindication inference not drawn* — **FIXED (reasoning on an already-cited fact, no new cite):** §4.1 now states explicitly that nominator withdrawal is an administrative/commercial act and is a neutral-to-negative signal for the evidence base, not a vindication.

**Checklist item not applicable:** Pawar 2017 DOI-suffix consistency — the Pawar DOI (`10.1016/j.xphs.2017.03.017`) appears once and is internally consistent; no suffix discrepancy exists in this report. **Deferred/N-A** (would require nothing to change).

**No new citation introduced:** confirmed — `git diff` shows zero new PMIDs, DOIs, or URLs; the crosswalk references only author/year labels already in the unified Bibliography.

**Post-fix grep (clean):**
- Crosswalk section present (`Citation numbering note + crosswalk`): **yes** (1 section; header reference + heading = 2 hits).
- Crosswalk data rows: **72**; unified Bibliography entries: **47** (max entry [47]).
- No inline reference number exceeds 47 (no out-of-range/dangling token): **confirmed clean**.
- Every distinct section-local tagged token in the body (`[N, tag]`, `[Sn,…]`, `[P1,…]`, `[4 in §7]`) has a corresponding crosswalk row; bare unified inline tokens (§1.4 `[2]`/`[3]`, §2.3 `[1]`/`[3]`) already point to valid Bibliography entries.
- **No dangling inline reference.**
