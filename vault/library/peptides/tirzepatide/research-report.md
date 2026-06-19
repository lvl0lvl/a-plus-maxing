---
title: "Tirzepatide — Research Report"
type: research-report
permalink: a-plus-maxing/library/peptides/tirzepatide/research-report
class: peptide
evidence_tier: S
risk_tier: moderate
status: complete
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: on new pivotal RCT or label/compounding change
---

# Tirzepatide (dual GIP/GLP-1 receptor agonist; Mounjaro / Zepbound)

## Metadata
- **Class:** peptide — single 39-aa dual GIP/GLP-1 receptor agonist (GIP-biased), C20-acylated (Eli Lilly)
- **Evidence tier:** **S** — large Phase-3 RCT base (SURMOUNT, SURPASS, SURMOUNT-OSA); FDA-approved; the most potent agent in its class (superior to semaglutide head-to-head).
- **Risk tier:** **moderate** — boxed thyroid-C-cell warning, GI AEs, serious-AE signals; contraindication screening required.
- **Goal caveat:** like semaglutide, a **goal MISMATCH** for the operator's rebuilding goal — see §4.
- **Last verified:** 2026-06-18

> Deep pass (peptide-library track). Method + ledger: `.provenance/`. Layers:
> [[library/peptides/tirzepatide/practitioner-layer]] · [[library/peptides/tirzepatide/non-english-layer]].
> Shares the GLP-1-class context (WADA monitoring, compounding wind-down) with [[compounds/semaglutide]].

---

## TL;DR

Tirzepatide is a single peptide that agonizes **both** the GIP and GLP-1 receptors (imbalanced, GIP-biased), giving the
**most potent weight loss of any approved agent** — ~20.9% at 72 weeks (SURMOUNT-1) and a decisive head-to-head win
over semaglutide (−20.2% vs −13.7%, SURMOUNT-5). It is FDA-approved for type 2 diabetes (Mounjaro), obesity (Zepbound),
and — uniquely — **moderate-to-severe obstructive sleep apnea** (Dec 2024). **But for THIS operator it carries the same
goal mismatch as semaglutide:** it is a weight-loss agent in which **~25% of the mass lost is lean tissue** (−10.9% lean
vs −33.9% fat in the SURMOUNT-1 DXA substudy), the benefit **reverses on discontinuation** (SURMOUNT-4: continued −25.3%
vs placebo −9.9%), and **no RCT tests it for building or recovering muscle** (the only lean-sparing signal comes from adding a separate anti-myostatin
drug). Safety is well-mapped (boxed thyroid-C-cell warning; GI AEs higher than semaglutide at obesity doses;
pancreatitis/gallbladder/aspiration signals). WADA: monitored, not prohibited (2026). Compounding is winding down
(shortage resolved Dec 2024).

---

## 1. Identity & Mechanism

- **What it is:** a synthetic 39-aa linear peptide based on the native GIP sequence, with a **C20 fatty-diacid
  acylation** → >99% albumin binding → ~5-day half-life / once-weekly dosing `[mechanism_review: PMID 34819089;
  Coskun, Mol Metab 2018, PMID 30473097]`.
- **Mechanism — imbalanced dual agonism:** agonizes both receptors but is **GIP-biased** — near-native potency at GIPR
  yet ~5-fold lower affinity / ~20-fold lower cAMP potency at GLP-1R, with cAMP-over-β-arrestin bias at GLP-1R
  `[in_vitro: Willard, JCI Insight 2020, PMID 32730231]`. The added GIPR engagement is proposed to improve adipose
  insulin sensitivity and lipid/triglyceride clearance on top of GLP-1-mediated appetite/glycemic effects — the leading
  rationale for greater weight loss than GLP-1 alone, **though the GIP-specific weight pathway remains partly
  inferential** `[mechanism_review: PMID 34819089]`.

---

## 2. Human Clinical Evidence

### 2.1 Obesity (the goal-adjacent one)
- **SURMOUNT-1 (NEJM 2022, PMID 35658024), n=2,539, 72 wk:** −15.0% / −19.5% / **−20.9%** (5/10/15 mg) vs −3.1% placebo
  ("up to ~22.5%" is the completer estimand). `[rct]`
- **SURMOUNT-1 DXA substudy (Diabetes Obes Metab 2025, DOI 10.1111/dom.16275; substudy n=160, total weight −21.3%):**
  fat mass −33.9%, **lean mass −10.9%** → **~75% of the mass lost was fat / ~25% lean** — same fat:lean ratio as placebo
  loss (obligatory deficit effect, not accelerated). `[rct substudy]`
- **SURMOUNT-4 (JAMA 2024, NCT04660643):** withdrawal → regain; continued −25.3% vs placebo −9.9% (~15-pp difference). `[rct]`

### 2.2 Type 2 diabetes — superior to semaglutide
- **SURPASS-2 (NEJM 2021, PMID 34170647), n=1,879:** HbA1c −2.0 to −2.3% (superior to semaglutide 1 mg at all doses);
  weight difference vs semaglutide −1.9 to −5.5 kg. `[rct]`

### 2.3 Obstructive sleep apnea (unique approval)
- **SURMOUNT-OSA (NEJM 2024, PMID 38912654):** AHI −25.3 to −29.3 events/h (vs −5.3 to −5.5 placebo); ~50% met
  resolution criteria — basis for the **Dec 2024 OSA approval**, the first drug approved for OSA. `[rct]`

### 2.4 Head-to-head for weight
- **SURMOUNT-5 (NEJM 2025, NCT05822830), n=751:** tirzepatide **−20.2% vs semaglutide −13.7%** (diff −6.5 pp, P<0.001) —
  tirzepatide superior. `[rct]`

### 2.5 Lean-mass building / recovery (the operator's goal)
- **NO ADMISSIBLE PRIMARY FOUND.** No RCT tests tirzepatide for increasing muscle mass, sarcopenia, or recovery. Every
  controlled body-comp dataset shows lean mass *decreasing* (~25% of loss; SURPASS-3 MRI: muscle volume −0.64 L). The
  only lean-sparing signal comes from **adding an anti-myostatin antibody** (apitegromab, Nat Med 2026) — i.e. the
  muscle benefit is from the co-drug, not tirzepatide. Goal mismatch (verified absence).

---

## 3. Safety, Contraindications, Monitoring (FDA Mounjaro/Zepbound label of record)

- **Boxed warning:** thyroid C-cell tumors / MTC (rodent signal; human relevance unknown) — **contraindicated with
  personal/family MTC or MEN2**; also hypersensitivity `[regulatory]`.
- **Common AEs (Zepbound, obesity doses):** nausea 25–29%, diarrhea 19–23%, constipation 11–17%, vomiting 8–13%,
  abdominal pain 9–10% — higher than at T2D doses (Mounjaro nausea 12–18%) `[regulatory]`.
- **Serious:** acute pancreatitis, gallbladder disease (0.6% vs 0%), AKI (volume depletion), hypoglycemia with
  insulin/SU, anaphylaxis/angioedema, **aspiration under anesthesia** (delayed gastric emptying) `[regulatory]`.
- **Lean-mass:** −10.9% in the SURMOUNT-1 DXA substudy (not a label warning; body-comp concern).
- **Monitoring:** thyroid symptoms; pancreatitis/gallbladder; renal function during severe GI AEs; glucose if on
  insulin/SU; perioperative aspiration precautions.
- **Anti-doping:** **NOT prohibited** — WADA **Monitoring Program** (2026), same as semaglutide. *(A vendor "S4 ban"
  claim was false and excluded.)* `[regulatory]`

---

## 4. The Goal-Mismatch Caveat (FIRST-CLASS)

Tirzepatide is the **most effective weight-loss drug available** — but the operator's goal is **post-illness
deconditioning recovery / rebuilding**, and tirzepatide is **catabolic-leaning, not anabolic**: ~25% of the mass lost
is lean tissue, the effect reverses on stopping, and there is **no RCT** supporting it for muscle gain or recovery. The
honest framing is identical to semaglutide's, only more potent: a **first-line tool when fat loss (or OSA) is clinically
indicated** — paired with resistance training + protein, MTC/MEN2 screened out — **not** a recovery or muscle-building
peptide. evidence_tier S for what it does; **off-target for the stated goal.**

---

## 5. Pharmacokinetics & Dosing

- **Dosing:** SC once weekly, titrate **2.5 → 5 → 7.5 → 10 → 12.5 → 15 mg** (≥4 wk per step; 2.5 mg is initiation, not
  maintenance). Mounjaro max 15 mg; Zepbound maintenance 5/10/15 mg; OSA dosing 10 or 15 mg `[regulatory]`.
- **PK:** half-life **~5 days**; Tmax median ~24 h (8–72 h); SC bioavailability **~80%**; steady state ~4 wk; 99%
  albumin-bound; Vd ~10.3 L `[regulatory: FDA label / NDA 215866 ClinPharm]`.
- **Storage:** refrigerate 2–8 °C; room temp ≤30 °C up to 21 d; do not freeze `[regulatory — VERIFIED:partial; label-derived, accessdata PDF not directly loaded]`.

---

## 6. Regulatory & Sourcing

- **FDA:** Mounjaro (T2D, **May 2022** — first dual GIP/GLP-1 agonist), Zepbound (obesity, **Nov 2023**; **OSA, Dec 20
  2024**). EMA: Mounjaro authorised **Sept 2022** (T2D + weight management). Manufacturer: Eli Lilly. `[regulatory]`
- **Compounding:** **shortage resolved (FDA declaratory order Dec 19 2024)** → wind-down (503A Feb 18 2025, 503B ~Mar 19
  2025); compounded tirzepatide is not FDA-approved/quality-assured. `[regulatory]`
- **Cost:** ~$1,080/28-day list (Mounjaro $1,079.77; Zepbound $1,086.37); LillyDirect self-pay vials ~$299–499/mo.
- **Non-English:** global multicentre but **English-published — no distinct non-English primary located.**
- **Prescribing-practice:** on-label titration is standard; "microdosing" is off-label with **no RCT support**
  (`practitioner_protocol`, dose/route only). See the layers.

---

## 7. Bottom line for the operator

The strongest fat-loss/metabolic drug available and the only one approved for OSA — genuinely impressive, FDA-approved,
tier-S. But **off-target for the operator's recovery/rebuilding goal**: it is catabolic-leaning (sheds ~25% lean),
reverses on stopping, and has no muscle-building evidence. Reserve for clinically-indicated fat loss or OSA (with
resistance training + protein + MTC/MEN2 screen), discussed at the July-2026 visit — not a compounded self-sourced
protocol, and not a rebuilding tool.
