---
title: Ipamorelin
type: compound
permalink: a-plus-maxing/library/peptides/ipamorelin/research-report
class: peptide
evidence_tier: C
risk_tier: experimental
status: researching
created: 2026-06-20
last_verified: 2026-06-20
walter_status:
doctor_discussion_required: true
---

# Ipamorelin (NNC 26-0161)

## Metadata

- **class:** peptide (synthetic pentapeptide; ghrelin-receptor / GHS-R1a agonist; growth-hormone secretagogue, GHRP-class)
- **evidence_tier:** C — The mechanism and acute human pharmacology are clean and well characterized, but the *efficacy* evidence base is overwhelmingly preclinical (rat/swine), single-lineage (~80% Novo-Nordisk-origin), and the only human clinical-efficacy program — postoperative ileus — *failed* its Phase 2 primary endpoint and was discontinued. There is literally zero human efficacy data for the marketed muscle/fat/anti-aging use cases.
- **risk_tier:** experimental — Never approved for any indication anywhere; never reached Phase 3; one short (≤7-day) IV human safety RCT; removed from the FDA 503A interim Category 2 list and explicitly *rejected* for the 503A bulks list by the Pharmacy Compounding Advisory Committee (fluid-retention / hyperglycemia / congestive-heart-failure concerns cited); WADA-prohibited at all times; real-world use is chronic subcutaneous self-administration, a setting that has never been studied.
- **status:** researching
- **last_verified:** 2026-06-20

> **Read this first — the honest evidence state.**
>
> Ipamorelin is a synthetic **pentapeptide ghrelin-receptor (GHS-R1a) agonist** — historically billed as **"the first selective GH secretagogue,"** because it raises growth hormone **without** meaningfully raising ACTH, cortisol, or prolactin. That selectivity claim is real and important, but it is grounded **primarily in animal data** (Raun 1998, rats and swine); a head-to-head human hormone panel proving HPA-axis sparing in people was not located in the admissible primary literature. Treat selectivity as **animal-supported and mechanistically plausible, not human-proven.**
>
> The compound was developed by **Novo Nordisk** and licensed onward to **Helsinn Therapeutics**. The *only* clinical-efficacy program it ever had — **postoperative ileus** — **FAILED** its Phase 2 primary endpoint (Beck 2014; n≈114 analyzed; time to first tolerated meal 25.3 h vs 32.6 h, **p=0.15**), a larger confirmatory Phase 2 (NCT01280344, n=320) posted no results and produced no positive efficacy publication, and **development was discontinued.** There is **no approved indication, no Phase 3, and zero human efficacy data** for muscle gain, fat loss, athletic performance, or anti-aging.
>
> The acute human pharmacology *is* established — but only by the **intravenous** route: a single 15-minute IV infusion produces a clean, dose-proportional, self-limiting GH pulse with a terminal half-life of **~2 h** (Gobburu 1999, n=40 healthy men). The real-world route is **subcutaneous**, for which **no human PK exists** — the SC profile is an extrapolation from IV-human and animal data.
>
> The efficacy literature is also **concentrated**: ~80% of the in-vivo efficacy primaries trace to the single **Novo-Nordisk lineage** (≥70% single-lineage flag triggered); the only fully independent human trial is the one that failed.
>
> On regulation: ipamorelin was **never FDA-approved**, was **removed from the 503A interim Category 2 list around September 2024**, and on **October 29, 2024 the FDA's Pharmacy Compounding Advisory Committee (PCAC) voted AGAINST** adding it to the 503A bulk drug substances list (members citing fluid retention, hyperglycemia, and a congestive-heart-failure concern). It is **NOT** part of the April-2026 Federal Register action (FR Doc 2026-07361) that removed a *different* set of 12 peptides. WADA lists ipamorelin **by name** as **PROHIBITED AT ALL TIMES** under S2.2 (growth-hormone secretagogues).
>
> This is a **goal-agnostic library entry**: operator / dosing-for-a-specific-person fields are deliberately left blank. The purpose here is to state the evidence honestly, not to recommend use.

---

## 0. Evidence Map (read alongside the box)

> *Citation note: this synthesis table uses **unified** bibliography numbers [1]–[31] directly (it pools sources across all sections). The detail sections §1–§9 below use **section-local** numbers — see the "Citation Numbering Note + Crosswalk" before the bibliography.*

Because ipamorelin is so heavily marketed on the strength of one mechanistic property ("selective GH secretagogue") while its human-efficacy record is empty-to-negative, it is worth laying the evidence out by *strength* before the detail. The pattern that recurs throughout this report is **strong upstream, empty downstream**: the receptor pharmacology and acute human GH-release are well established, but everything a buyer actually cares about (body composition, recovery, anti-aging, chronic safety) is either unstudied in humans or actively negative.

| Question | Best evidence available | Verdict |
|---|---|---|
| Does it bind GHS-R1a and trigger GH release? | Receptor mechanism reviews [7,8] + in-vitro rat pituitary EC50 1.3 nmol/L [1] | **Established** (mechanism + animal) |
| Does it raise GH acutely in humans? | Phase 1 IV PK/PD, n=40 healthy men [4] | **Established** (acute, IV, biomarker) |
| Is it truly "selective" (no ACTH/cortisol/prolactin)? | Raun 1998 [1] — **rat & swine**, not a human hormone panel | **Animal-supported, NOT human-proven** |
| Does it raise IGF-1 chronically? | Rat data: intermittent dosing did **not** raise IGF-1 [10]; no human dose-response | **Not demonstrated; partly contradicted** |
| Does it build muscle / cut fat in humans? | None | **Zero human efficacy data** |
| Does it improve any clinical outcome in humans? | Postoperative-ileus Phase 2 RCT [15] — **failed** (p=0.15); larger Phase 2 [17] — no positive result | **Negative / discontinued** |
| Is the SC route (the real-world route) characterized? | No human SC PK; only IV human + rat IV/intranasal | **Extrapolated, not measured** |
| Is chronic safety known? | One ≤7-day IV RCT [15]; GH-axis risks are class-inferred [19] | **Uncharacterized for real-world use** |
| Is it legal / approved? | Never FDA-approved; PCAC-rejected for 503A [22]; WADA-banned [24] | **Unapproved + prohibited** |

Every row of this table is unpacked, with its citations, in the sections below.

---

## 1. Identity, Chemistry & PK

### 1.1 Sequence, structure, and identifiers

Ipamorelin is a synthetic **pentapeptide** with the sequence **Aib-His-D-2-Nal-D-Phe-Lys-NH₂** (a C-terminal carboxamide), developed by Novo Nordisk under the developmental code **NNC 26-0161** [1, animal][5, mechanism_review]. It was engineered within a GHRP-derived medicinal-chemistry series, designed deliberately *without* the central Ala-Trp dipeptide of GHRP-1 [1, animal].

Authoritative chemical identity (PubChem CID 9831659) [3, regulatory]:

- **Molecular formula:** C₃₈H₄₉N₉O₅
- **Average molecular weight:** ≈ **711.9 g/mol** (the corpus carries the same value to within rounding as 711.85 and 711.86, depending on whether the source is PubChem, dose-math, or a vendor label; the spread is <0.05 g/mol, ~0.007% — these are the same compound, not a discrepancy)
- **Monoisotopic mass:** 711.3857
- **CAS Registry Number:** **170851-70-4** (free base / parent) [3, regulatory]
- Commonly supplied as the **acetate salt** [3, regulatory][6, vendor_label]
- Physical form: white to off-white powder [6, vendor_label] *(vendor cite supports the physical description only; it is not used to ground any pharmacology number)*

### 1.2 Why the structure matters (protease resistance)

The structure is built for parenteral stability. The N-terminal residue **Aib (α-aminoisobutyric acid)** is a non-proteinogenic, conformationally constraining amino acid, and positions 3 and 4 are **D-amino acids (D-2-naphthylalanine and D-phenylalanine)** — both features confer protease resistance relative to an all-L peptide [1, animal][5, mechanism_review]. This is structural inference supported directly by the sequence; it explains the metabolic stability observed in animal PK (below) and the lack of meaningful oral bioavailability.

### 1.3 Human pharmacokinetics — IV only

Human PK comes from a single first-in-human study (Gobburu 1999; n=40 healthy males, 8 per dose × 5 dose levels, single 15-minute IV infusion) [4, open_label; species=human; route=IV infusion]:

- **Terminal half-life ≈ 2 h**
- **Plasma clearance 0.078 L/h/kg**
- **Steady-state volume of distribution 0.22 L/kg**
- PK was **dose-proportional** over the 4.21–140.45 nmol/kg range
- PK/PD link (indirect / turnover response model): GH-stimulation potency **SC50 = 214 nmol/L**, maximal GH production rate ≈ 694 mIU/L/h [4, open_label; species=human; route=IV]

> **ROUTE NOTE (first-class limitation).** The canonical "~2 h half-life" is established from **IV infusion in humans** [4]. **No verified human subcutaneous PK** (SC bioavailability / half-life / Tmax) was located in the admissible literature. Because **SC is the predominant real-world / compounded route**, the SC PK profile is currently an **extrapolation from IV-human plus animal data, not a measured quantity** [route-extrapolation]. This is the single most important PK gap for any wiki ingestion.

### 1.4 Animal pharmacokinetics (species + route tagged)

- **Rat (male Sprague-Dawley), IV:** Ipamorelin's systemic plasma clearance was **~5-fold lower than GHRP-6**; it was excreted **mainly in urine** (GHRP-6 is predominantly biliary), with **60–80% recovered as intact compound** across excretion pathways — confirming metabolic stability [10, animal; species=rat; route=IV] (Johansen PB et al. 1998).
- **Rat, intranasal:** intranasal bioavailability ≈ **20%** — lower than the related compounds NNC 26-0235 / NNC 26-0194 / GHRP-2 (~50%) [10, animal; species=rat; route=intranasal]. **No SC bioavailability was tested in this study**; the only directly measured routes in admissible literature are IV (human and rat) and intranasal (rat).

### 1.5 Structure-activity context and formulation

Ipamorelin was the **lead scaffold** from which a peptidomimetic SAR series was built (size reduction plus backbone N-methylation, in pursuit of oral bioavailability); the derived **tetrapeptide NNC 26-0235** reached ~10% oral bioavailability **in dogs**, whereas ipamorelin itself was developed as a **parenteral** peptide with no meaningful oral bioavailability claimed [5, mechanism_review; species=dog for the derivative].

Formulation/stability specifics (reconstitution solvent, cold-chain, lyophilized and in-use shelf-life) are **not** documented in the admissible Tier-1/2 primary literature. Vendor labels assert a lyophilized-powder presentation and offer reconstitution math (reconstitute in sterile / bacteriostatic water to ≥100 µg/mL; refrigerate 2–7 days post-reconstitution; freeze for longer storage) (unified [28], [29], vendor_label; the same reconstitution-math sources used in §9.3) — admissible for administration arithmetic only, not to ground any stability number.

---

## 2. Mechanism of Action

Ipamorelin (Aib-His-D-2-Nal-D-Phe-Lys-NH₂) is a synthetic pentapeptide growth-hormone secretagogue (GHS) that acts as an **agonist at the growth-hormone-secretagogue receptor type 1a (GHS-R1a, the ghrelin receptor)** [5, mechanism_review]. Its defining mechanistic claim is *selective* GH release: it raises GH with a selectivity comparable to GHRH, without the ACTH/cortisol/prolactin co-stimulation seen with earlier GHRPs (GHRP-6, GHRP-2, hexarelin). The receptor-level signaling and the selectivity profile are well characterized; the downstream IGF-1 story in humans is thin (see §2.5).

### 2.1 The receptor and the shared ligand class

Ipamorelin binds the **same GHS-R1a receptor as ghrelin, GHRP-2, GHRP-6, and ibutamoren** [5, mechanism_review]. As a GHS it acts at the pituitary somatotroph (and the hypothalamus) to drive GH release [3, mechanism_review]. GHS-R/ghrelin-receptor expression is concentrated in the brain — greatest in the pituitary and in hypothalamic NPY/AgRP neurons — with lower peripheral expression (pancreas, spleen, kidney, adrenal) [4, mechanism_review].

### 2.2 The signal-transduction pathway

GHS-R1a is a **seven-transmembrane G-protein-coupled receptor**. Agonist binding couples primarily to **Gαq/11**, activating **phospholipase C (PLC)**, which cleaves PIP₂ into **IP₃ and DAG**. IP₃ mobilizes intracellular Ca²⁺ from endoplasmic-reticulum stores; DAG activates PKC, which inhibits K⁺ channels, depolarizing the membrane and triggering voltage-gated Ca²⁺ influx. The resulting rise in intracellular Ca²⁺ drives **GH-granule exocytosis** from pituitary somatotrophs [3, mechanism_review]. This is the canonical GHS-R1a transduction pathway; ipamorelin engages this shared receptor mechanism.

A regulatory feature worth flagging: **GHS-R1a exhibits unusually high constitutive (ligand-independent) activity**, and **β-arrestin recruitment** desensitizes G-protein signaling and targets the receptor for clathrin-mediated endocytosis [3, mechanism_review]. This is mechanistically relevant to the open question of whether *repeated* dosing preserves natural GH pulsatility or risks somatotroph desensitization / receptor downregulation (see gaps in §2.6).

The clinical-translation significance of these two receptor properties — high constitutive activity and β-arrestin-mediated internalization — is that they make the receptor's *steady-state* behavior under chronic agonist exposure genuinely uncertain. A single acute dose produces a clean GH pulse (demonstrated in humans [2]); but whether nightly chronic dosing keeps eliciting full-amplitude pulses, or whether the somatotroph progressively downregulates GHS-R1a and blunts the response, is **not characterized for ipamorelin in any verified source.** This is not an idle concern: it is exactly the kind of receptor that one would *expect* to desensitize, and the entire practitioner rationale for cycling (§9.2) is an implicit admission that continuous stimulation may not be sustainable. The honest position is that the acute single-pulse pharmacology cannot be assumed to extrapolate to a chronic-dosing benefit.

### 2.3 The selectivity claim (foundational — but animal-grounded)

This is ipamorelin's signature property. In **rats**, ipamorelin did **NOT** release ACTH or cortisol at levels significantly different from GHRH, **even at doses >200-fold above the GH ED50**; no significant effect on prolactin, FSH, LH, or TSH was observed for the secretagogues tested. By contrast, GHRP-6 and GHRP-2 **elevated ACTH and cortisol**. This is what earned ipamorelin the label **"the first selective GH secretagogue"** [1, animal] (anesthetized Sprague-Dawley rats and conscious swine; per-group n not stated in the source abstract).

**Honest framing:** the keystone "no cortisol/ACTH/prolactin" selectivity claim is grounded chiefly in Raun 1998 [1], which is **rat (and swine) data**. The human study [2] confirms the GH PD/PK and the single-pulse release pattern, but the abstract-level data accessed **did not quantify a head-to-head human ACTH/cortisol/prolactin panel**. Treat "HPA-axis sparing in humans" as **mechanistically plausible and animal-supported, not definitively human-proven** at the primary-source level reviewed. At the molecular level, *why* a shared GHS-R1a agonist avoids the ACTH/cortisol co-release that GHRP-6/2 cause is not fully resolved (biased agonism / differential downstream coupling is plausible but not confirmed in the verified sources).

Why does this distinction matter so much for a library entry? Because the entire commercial appeal of ipamorelin over older GHRPs is the selectivity claim — "all the GH, none of the cortisol/appetite/prolactin." If the selectivity is real in humans, ipamorelin would be a cleaner GH stimulus than GHRP-6 or hexarelin. But the strength of the underlying evidence is a single 1998 paper in rats and pigs, from the originator lab, that measured the hormone panel in animals at doses up to 200-fold above the GH ED50 and found no ACTH/cortisol/prolactin/FSH/LH/TSH rise [1]. That is a genuinely impressive *animal* result — the 200-fold safety margin is the most quantitatively striking part of the selectivity story — but it is **not** the same as a human dose-ranging study with a measured cortisol curve. A reader should hold the selectivity claim as the best-supported *mechanistic* property of the molecule while simultaneously recognizing it has never been confirmed in a human hormone panel. Note also that one review in the corpus [5] explicitly flags limited ipamorelin-specific human data and even raises a rodent finding of *GH-independent* weight gain — a caution that the simple "GH→IGF-1→lean mass" narrative may be incomplete even in animals.

### 2.4 Potency and the single-pulse human PD

- **In vitro (primary rat pituitary cells):** EC50 = **1.3 ± 0.4 nmol/L**, Emax = 85 ± 5% (GHRP-6 reference EC50 = 2.2 ± 0.3 nmol/L) — potency/efficacy comparable to GHRP-6 [1, in_vitro].
- **Anesthetized rats, IV:** ED50 = **80 ± 42 nmol/kg**, Emax ≈ 1545 ± 250 ng/mL [1, animal].
- **Conscious swine, IV:** ED50 = **2.3 nmol/kg** [1, animal] — note the ~35× interspecies potency gap vs rat, which makes any cross-species dose extrapolation unsafe.
- **Human, IV:** A 15-minute IV infusion in healthy men produced a **single discrete GH pulse peaking at ~0.67 h** and declining exponentially to negligible levels at all doses — i.e., it elicits a **single physiologic-style GH pulse rather than a sustained plateau** [2, open_label/rct] (40 healthy males, 8/dose × 5 IV doses, randomized double-blind placebo-controlled dose-escalation). The short half-life and single-pulse PD are consistent with pulsatile, self-limiting GH stimulation.

### 2.5 Downstream IGF-1 (the weak link)

GH released by ipamorelin is *expected* to stimulate hepatic IGF-1 via the standard GH→IGF-1 axis [2, mechanism_review (§E)]. **But the strongest verified primary sources characterize acute GH release and PK/PD — not chronic, ipamorelin-driven IGF-1 in humans.** The body-composition / IGF-1 framing in reviews is explicitly weaker for ipamorelin specifically [5, mechanism_review], and — importantly — a preclinical signal *contradicts* a simple IGF-1 story (see §3.1: intermittent dosing did **not** raise IGF-1 in rats). Do not assume a guaranteed IGF-1 rise, especially with pulsatile dosing.

### 2.6 Selectivity vs other GHRPs (synthesis)

All of these compounds bind GHS-R1a on somatotrophs, but GHRP-6/GHRP-2 also drive ACTH/cortisol elevation, and GHRP-6/hexarelin add appetite/prolactin effects; ipamorelin's structure confers near-exclusive GH-selective action with HPA-axis sparing [1, animal][5, mechanism_review]. The direct ACTH/cortisol superiority is grounded in [1] (animal); the receptor-sharing/selectivity framing in [5]. **No direct comparative human trial** of ipamorelin vs GHRP-6/hexarelin on the full hormone panel was located — the comparison rests on the single animal study plus the receptor-sharing review.

---

## 3. Preclinical Efficacy

> **SCOPE NOTE.** All evidence in this section is **preclinical (animal / in-vitro)**. None of it establishes efficacy in humans. The evidence is overwhelmingly **rat**, with one swine GH-release dataset; **no primate efficacy** was located. The gut-motility track features prominently because postoperative ileus was the clinical development indication.

### 3.1 GH / IGF-1 axis

- In primary **rat** pituitary cell culture, ipamorelin released GH with potency/efficacy similar to GHRP-6: EC50 = 1.3 ± 0.4 nmol/L, Emax = 85 ± 5% (GHRP-6 reference 100%, EC50 = 2.2 ± 0.3 nmol/L) [1, in_vitro].
- In pentobarbital-anesthetized **rats** (IV bolus), ED50 = 80 ± 42 nmol/kg, Emax = 1545 ± 250 ng/mL — comparable to GHRP-6 (ED50 = 115 ± 36 nmol/kg, Emax = 1167 ± 120 ng/mL) [1, animal].
- In conscious **swine** (IV), ED50 = 2.3 ± 0.03 nmol/kg, Emax = 65 ± 0.2 ng/mL plasma [1, animal].
- **Selectivity (efficacy-relevant):** ipamorelin did not release ACTH or cortisol above GHRH-stimulated baseline even at ~200× the GH ED50; prolactin/FSH/LH/TSH also unaffected — distinguishing it from GHRP-6 and other early secretagogues [1, animal].
- **CONTRARY / NUANCE on IGF-1:** in adult female **rats**, 15-day intermittent SC ipamorelin (3×/day) that produced clear somatic growth **did NOT raise total serum IGF-1, IGFBPs, or serum bone-turnover markers** [3, animal]. Sustained IGF-1 elevation is therefore **not a reliable feature of intermittent dosing in rodents**; GH pulse amplitude is the proximate driver. This is a direct caution against the vendor narrative of robust IGF-1 elevation.

### 3.2 Bone — content/area, NOT volumetric density

This is a notable ipamorelin preclinical area and a common site of overstatement. The honest reading is **bigger bones, not denser bone matrix.**

- In 13-week-old female Sprague-Dawley **rats** (n=7 ipamorelin), 0.5 mg/kg/day delivered **continuously** by SC osmotic minipump for 12 weeks increased total tibial and vertebral **bone-mineral content (BMC, DXA in vivo)** vs vehicle; GHRP-6 (n=8) and GH (n=7) did likewise [2, animal].
- The BMC gain **tracked body-weight gain**: total BMC corrected for body weight (BMC:BW ratio) was **unaffected**; tibial area BMD rose, but **total and vertebral area BMDs were unchanged** [2, animal].
- By pQCT, the cortical BMC increase was driven by **increased cross-sectional bone area**, while cortical **volumetric BMD was unchanged** [2, animal].

> **Do not state "ipamorelin increases bone density."** The primary data show increased bone mineral *content* / bone *size* with **unchanged volumetric BMD**. There is also **no orchidectomized / ovariectomized osteoporosis model** for ipamorelin in the admissible set — the bone evidence is in intact young-adult female rats. (The corpus also references a 2001 glucocorticoid-induced-bone-loss rat study using Novo-Nordisk-origin compound [unified 12, animal], whose full text was paywalled — a corpus-missing item, not a load-bearing claim here.)

The distinction between bone *content/size* and bone *density* is not pedantic — it is the difference between two different physiologic claims. **Bone mineral content (BMC)** and **bone area** can rise simply because GH/IGF-1 make the whole animal bigger; a larger skeleton carries more total mineral and has larger cross-sections without the bone matrix being any denser. **Volumetric BMD** (mineral per unit bone volume, measured by pQCT) is the quantity that maps to the lay notion of "stronger, denser bones" and to fracture-resistance in osteoporosis. The Svensson 2000 data are explicit on this point: BMC rose, but when corrected for body weight (BMC:BW) the effect vanished, total and vertebral *area* BMD were unchanged, and cortical *volumetric* BMD was unchanged — the cortical BMC gain was driven entirely by increased cross-sectional area [2]. In plain terms: **ipamorelin made the rats' bones bigger in proportion to making the rats bigger; it did not make the bone matrix denser.** Vendor copy that compresses this into "ipamorelin increases bone density" is overstating the primary data. There is, additionally, a dosing-regimen confound running through the bone literature: the BMC study used *continuous* SC infusion (osmotic minipump) [2], whereas the longitudinal-growth study used *pulsatile* 3×/day SC dosing [3] — and continuous vs pulsatile GH-axis stimulation are mechanistically different (continuous exposure is the classic route to GH-axis desensitization). The two regimens cannot be pooled into a single "bone effect," and neither has any analogue in the human nightly-bolus convention.

### 3.3 Longitudinal growth

In adult female **rats**, SC ipamorelin 3×/day for 15 days dose-dependently increased longitudinal bone growth rate (tibial metaphysis, tetracycline-label method) from 42 µm/day (vehicle) to 44, 50, and 52 µm/day at 18, 90, and 450 µg/day respectively (P < 0.0001) [3, animal]. The same study showed pronounced, dose-dependent **body-weight gain** and no significant change in osteoclast-marker (TRAP-positive) multinuclear cell counts [3, animal].

### 3.4 Body composition / lean mass (with an explicit unverified flag)

Across the bone/growth studies, ipamorelin's reproducible preclinical body-composition signal in **rats** is GH-mediated **body-weight / lean somatic gain**, rather than a directly quantified fat-vs-lean DXA partition in the primary papers [2, animal][3, animal].

> **UNVERIFIED — do NOT ground a fat-loss number on it.** Claims of selective fat-mass reduction with preserved lean mass in "diet-induced obese rats" circulate in vendor/secondary write-ups but **could not be tied to a resolvable primary citation** during retrieval. Treat as unverified.

### 3.5 Gut motility — the development indication

This is the strongest *functional* (not just biomarker) preclinical track, consistent with the clinical target.

- In a **rat** postoperative-ileus model (laparotomy + intestinal manipulation), a single IV ipamorelin 1 mg/kg shortened time to first bowel movement vs vehicle; **repetitive** dosing (4×/day, 0.01–1 mg/kg) significantly increased cumulative fecal pellet output, food intake, and 48-h body-weight gain [4, animal; IV; fasted male rats].
- In a related **rat** gastric-dysmotility model, surgery delayed gastric emptying to 78 ± 5% of meal retained (vehicle); ipamorelin 0.014 µmol/kg IV accelerated emptying to 52 ± 11% retained, approaching nonsurgical controls (44 ± 6%) [5, animal].
- **Mechanism:** in isolated gastric smooth-muscle from operated **rats**, surgery blunted acetylcholine- and electrical-field-stimulation-evoked contractions; ipamorelin (and ghrelin) reversed this — i.e., gastroprokinesis via **GHS-R1a-mediated activation of cholinergic excitatory neurons, not a direct GH effect** [5, animal/ex_vivo].

> **Dose-translation caution.** Doses are species- and route-specific and **not human-translatable**. Continuous SC infusion [2] is mechanistically different from pulsatile/intermittent SC dosing [3] (GH-axis desensitization) and the two cannot be pooled. Gut studies report doses in two unit systems (mg/kg [4]; µmol/kg [5]) that must be normalized before comparison.

---

## 4. Human Clinical Evidence

> **Bottom line up front:** Ipamorelin's total human clinical footprint is **small and, on efficacy, negative.** Two Phase 2 RCTs (both postoperative ileus, both unsuccessful) plus one Phase 1 healthy-volunteer pharmacology study. There is **no approved human indication anywhere**, **no Phase 3 was ever run**, and **no human efficacy trial exists for athletic performance, body composition, or anti-aging.** A search of ClinicalTrials.gov for "ipamorelin" returns only the two ileus studies [3, rct][4, rct].

### 4.1 Phase 1 — pharmacology, not efficacy

The first-in-human study established that ipamorelin raises GH in healthy men in a **dose-proportional, short-lived pulse** (Gobburu 1999): n=40 healthy males (8/dose), single 15-minute IV infusion at 4.21–140.45 nmol/kg; terminal half-life ~2 h; clearance 0.078 L/h/kg; Vss 0.22 L/kg; GH peaked at ~0.67 h and declined to negligible levels within ~6 h; SC50 = 214 nmol/L; max GH production rate 694 mIU/L/h [2, open_label]. **This is a pharmacology/biomarker study — it shows the drug does what it was designed to do (raise GH acutely), and nothing about clinical benefit.**

### 4.2 Phase 2 POI trial #1 (Beck 2014 / NCT00672074) — FAILED its primary endpoint

A randomized, **quadruple-blinded** (participant/provider/investigator/assessor), placebo-controlled, parallel proof-of-concept study in bowel-resection patients; **n=117 enrolled (114 in safety/mITT analyses)**; IV ipamorelin **0.03 mg/kg BID** vs placebo for up to 7 days / discharge; primary endpoint = recovery of upper-GI function (time to first tolerated meal). **No significant difference vs placebo** in the key or secondary efficacy analyses — **time to first tolerated meal 25.3 h vs 32.6 h, p=0.15** [1, rct][3, rct]. Sponsor: Helsinn Therapeutics. Status: Completed (Dec 2009). This is the **single peer-reviewed human efficacy RCT** for ipamorelin, and it is negative.

### 4.3 Phase 2 POI trial #2 (NCT01280344) — larger, no positive result, no approval

A larger confirmatory RCT: randomized, quadruple-blinded, placebo-controlled, parallel; **n=320 enrolled**; three ipamorelin IV arms (0.03 mg/kg BID, 0.06 mg/kg BID, 0.06 mg/kg TID) vs saline placebo TID; primary endpoint = recovery of GI function (up to 10 days post-op). Sponsor: Helsinn. Status: Completed (primary completion Jun 2013; study completion May 2014). **No structured results are posted on ClinicalTrials.gov (hasResults = false), and no separate peer-reviewed positive efficacy publication was identified; development did not progress beyond this Phase 2 and no further trials are registered** [4, rct][3, rct][1, rct].

> **Honest limit on the negative read.** The registry record for NCT01280344 carries no "whyStopped" field and `hasResults=false`. Its negative read is **inferred** from (a) the absence of posted per-endpoint results, (b) the absence of any positive efficacy publication, and (c) the failed primary endpoint of the companion POI RCT [1] — **not** from a results table. This is stated transparently rather than overclaimed.

### 4.4 Trial table

| Study | Design (type-tag) | n | Sponsor | Status / Result | NCT / PMID |
|---|---|---|---|---|---|
| Gobburu 1999 — PK/PD, healthy males | Phase 1 dose-escalation, IV, no control arm (open_label) | 40 (8/dose × 5) | Novo Nordisk | Completed. Dose-proportional GH release; t½ ~2 h; SC50 214 nmol/L. **Biomarker only — no clinical-efficacy endpoint.** | PMID 10496658 |
| Beck 2014 / NCT00672074 ("Ipamorelin 201") — POI after bowel resection | RCT, quadruple-blind, placebo-controlled, parallel (rct) | 117 enrolled (114 mITT) | Helsinn Therapeutics | Completed Dec 2009. **NEGATIVE** — primary endpoint not met (25.3 h vs 32.6 h, p=0.15). | NCT00672074 / PMID 25331030 |
| NCT01280344 — POI / GI recovery, 3 dose arms | RCT, quadruple-blind, placebo-controlled, parallel (rct) | 320 enrolled | Helsinn Therapeutics | Completed May 2014. No posted results; no positive efficacy publication. **Program discontinued.** | NCT01280344 |
| Program-level: Novo Nordisk → Helsinn POI development | Inferred from registry + outcomes | — | Novo Nordisk → Helsinn | **Did not progress beyond failed Phase 2. No approval. No Phase 3. No further trials registered.** | — (inferred from [1],[3],[4]) |

### 4.5 Reading the discontinuation honestly

It is worth being precise about *what kind* of failure this is, because "failed Phase 2" can mean several different things. Ipamorelin's failure is the most informative kind: a **drug that does exactly what it is pharmacologically designed to do (raise GH acutely, cleanly, dose-proportionally) but does not translate that biomarker effect into a clinical benefit.** The Phase 1 study [2] is a clean positive for the *mechanism*; the Phase 2 RCT [1] is a clean negative for the *outcome* it was tested on. That gap — biomarker moves, outcome does not — is exactly the gap that should make a reader skeptical of every marketed claim, because every marketed claim (muscle, fat, recovery, anti-aging) is precisely a leap from "raises GH" to "produces a desirable outcome," and the one time that leap was tested in a controlled human trial, it failed.

Two further nuances keep this honest. First, the failed endpoint was **postoperative ileus**, *not* a body-composition or anti-aging endpoint — so strictly, the failure does not directly disprove the marketed uses; it disproves the one thing that was actually studied. But it removes the only positive human-outcome data the molecule could have had, and it does so in a setting (gut motility) where the *preclinical* signal was the strongest (the Venkova rat POI studies, §3.5) — i.e., the indication most likely to succeed is the one that failed. Second, the negative read on the larger trial [4] is **inferred**, not from a results table (none is posted; `hasResults=false`), but from the convergent absence of posted results, the absence of any positive efficacy publication, the failed companion RCT [1], and the program's discontinuation. This inference is labeled as such throughout and is not overstated into a reported p-value.

### 4.6 What this means for the marketed uses

**ZERO human trials exist** for muscle gain, fat loss, athletic performance, anti-aging/longevity, sleep, or recovery. Every such claim circulating in the peptide market is **extrapolation from acute GH pharmacology**, not human outcome data. Long-term safety in humans is **uncharacterized**: all human trials were short (≤7–10 days), IV, and inpatient — there is **no chronic-dosing, subcutaneous-self-administration, or long-term safety data**, which is precisely the real-world use pattern. No non-English or prescribing-practice human literature exists either, because the drug is unapproved — the *absence* of prescribing guidance is itself a finding, not a gap waiting to be filled.

---

## 5. Concentration / Lab-Provenance Audit (FIRST-CLASS)

Ipamorelin (Aib-His-D-2-Nal-D-Phe-Lys-NH₂; CAS 170851-70-4) was discovered and characterized **in-house at Novo Nordisk A/S** (Department of GH Biology / Health Care Discovery, Måløv, Denmark). The compound's foundational pharmacology is **overwhelmingly attributable to this single corporate-academic lineage** and its immediate Danish academic collaborators (Aarhus University — Andreassen / Flyvbjerg / Ørskov groups), with the bone-content work via Gothenburg/Göteborg University in collaboration with Novo Nordisk.

**In-vivo efficacy primaries identified and verified:**

| # | Study | Lineage |
|---|---|---|
| 1 | Raun 1998 — discovery / selectivity / in-vivo GH release (swine & rats) | **Novo Nordisk** (all authors) |
| 2 | Johansen 1999 — longitudinal bone growth (rats) | **Novo Nordisk + Aarhus University** |
| 3 | Svensson 2000 — bone mineral content (adult female rats) | Göteborg University + **Novo Nordisk** (Novo-origin compound/design) |
| 4 | Glucocorticoid/bone 2001 — counters glucocorticoid-induced bone loss (rats) | Swedish academic + **Novo-Nordisk-supplied compound** |
| 5 | Beck 2014 — human Phase 2 RCT, postoperative ileus | Helsinn (independent licensee) — **FAILED** |

**Estimated single-lab (Novo-Nordisk-origin) share of in-vivo efficacy primaries: ~80% (4 of 5)**, and 100% of the molecule's foundational discovery/characterization. Method: every animal efficacy primary either originates entirely within Novo Nordisk or uses Novo-Nordisk-supplied compound under collaboration; only the 2014 human RCT is a fully independent (licensee-sponsored) clinical effort — **and it failed its primary endpoint.**

> **FLAG: single-lineage dominance ≥70% — confirmed.** The in-vivo efficacy evidence base is **concentrated and not independently replicated** outside the originator program for the GH/bone-anabolic claims; the one independent human trial was negative. (The Venkova gut-motility papers are an independent group, but they sit outside the GH/bone anabolic-efficacy scope and do not change the share below 70%.) There is **no independent, non-originator, positive human efficacy primary** for GH-secretagogue or anabolic indications.

---

## 6. Why This Lands at evidence_tier C

The grade is a deliberate balance of three honest facts:

1. **Mechanism + acute human pharmacology are solid.** Receptor identity, signal transduction, potency, and the acute single-pulse GH-release PD/PK in humans are well characterized and internally concordant across the corpus (the receptor/mechanism + acute-PK sources, unified [1], [4], [7], [8]). That alone keeps it off the floor.
2. **But efficacy evidence is preclinical, single-lineage, and the one human efficacy program failed.** ~80% of efficacy primaries are Novo-Nordisk lineage (≥70% flag); the keystone *selectivity* claim is animal-grounded; the only human-efficacy program (postoperative ileus) failed its Phase 2 primary endpoint and was discontinued; **zero** human efficacy data exist for the marketed uses. This is squarely below tier B.
3. **The honest limits are pervasive, not incidental:** no human SC PK; no chronic human safety data; no human IGF-1 dose-response; bone data show content/size not volumetric density; the headline "selective" property is not human-proven.

A compound with clean acute pharmacology but a *failed* efficacy program and an entirely preclinical, single-lineage anabolic case sits at **C** — not lower (the science is real and verifiable), not higher (there is no positive human efficacy and the evidence is concentrated).

---

## 7. Safety & Contraindications

> **Framing.** Human safety data are thin — **one** published Phase 2 RCT (short-course, IV, perioperative) plus early pharmacology. GH-axis risk is therefore reasoned largely from the **broader GH/IGF-1 literature** and labeled as such. Throughout, **AE *existence* (class-level) is distinguished from quantitative AE *rate*** (grounded only in primary human trials, never vendor/anecdote).

### 7.1 What the one human RCT actually showed (AE rate)

In the only published Phase 2 human RCT (postoperative ileus; n=114 safety/mITT; ipamorelin 0.03 mg/kg IV BID up to 7 days), ipamorelin was **well tolerated with no serious compound-related adverse events** [1, rct]. **AE rate (quantitative):** overall treatment-emergent AE incidence was **87.5% ipamorelin vs 94.8% placebo** — i.e., **not higher than placebo** in this short-course IV setting [1, rct].

> This is a **7-day perioperative IV exposure** and does **NOT** speak to chronic subcutaneous self-administration risk. There is **no peer-reviewed safety dataset for chronic SC use** — the real-world pattern.

### 7.2 GH-axis adverse effects (existence, class-level)

GH/secretagogue exposure in controlled adult studies produces **fluid-retention phenomena — peripheral edema, arthralgia, and carpal-tunnel-type symptoms — and impaired glucose tolerance / reduced insulin sensitivity** [3, mechanism_review]. Carpal-tunnel symptoms in GH/IGF-1 excess are mechanistically attributed to median-nerve compression from GH-induced sodium/water retention and soft-tissue edema (the acromegaly model) [3, mechanism_review]. These are **class effects** of driving the GH axis, not ipamorelin-specific measured rates.

### 7.3 Regulator-acknowledged signals for ipamorelin specifically

At FDA's PCAC review, committee members voting against ipamorelin cited reported adverse effects including **fluid retention, hyperglycemia, and a congestive-heart-failure concern**, alongside insufficient efficacy/safety evidence [4, regulatory]. (This is a regulatory characterization of the evidence base, not a measured trial AE rate.)

### 7.4 The sustained-IGF-1 / cancer caveat (associational, not shown for ipamorelin)

Higher circulating IGF-1 is **prospectively associated with increased risk of several cancers**:

- Pooled individual data from **17 prospective studies**: breast-cancer **OR 1.28 (95% CI 1.14–1.44)** highest vs lowest IGF-1, concentrated in ER-positive tumors [5, cohort].
- EPIC-Heidelberg prospective case-cohort (~7,461 with IGF-1): higher IGF-1 associated with **breast HR 1.25** and **prostate HR 1.31**, with a **U-shaped IGF-1–mortality** relationship [6, cohort].

> This is an association in **endogenous-IGF-1 epidemiology**. It has **NOT** been demonstrated that exogenous ipamorelin raises cancer risk — but it is the basis of the theoretical caution against chronically driving IGF-1 upward. The U-shaped curve also means the goal is **"keep IGF-1 in range," not "minimize IGF-1."**

### 7.5 Contraindications / cautions / monitoring (each cited)

- **Caution — active or history of malignancy:** the IGF-1–cancer prospective associations [5,6, cohort] make chronic GH-secretagogue-driven IGF-1 elevation a theoretical concern; the standard GH-therapy contraindication to active malignancy applies by extension [3, mechanism_review].
- **Caution — impaired glucose tolerance / diabetes:** GH-axis stimulation reduces insulin sensitivity and can raise glucose [3, mechanism_review]; hyperglycemia was a regulator-cited concern [4, regulatory].
- **Caution — fluid-overload states (e.g., heart failure):** edema/fluid retention is a class effect [3, mechanism_review] and a congestive-heart-failure concern was raised at PCAC [4, regulatory].
- **Monitoring (named objective assays):**
  - **Serum IGF-1** — the primary ceiling marker; keep within age/sex reference range (rationale from [2,3,5,6]). See [[biomarkers/igf-1]].
  - **Fasting glucose and HbA1c** — insulin-resistance / hyperglycemia surveillance [3,4].
  - **Clinical surveillance for edema, arthralgia, and carpal-tunnel symptoms** — the bedside readout of fluid retention [3].
- **Stopping rules:** discontinue / re-evaluate on IGF-1 rising above the age-adjusted reference range, new or worsening glucose dysregulation, or onset of edema/arthralgia/carpal-tunnel symptoms — each maps to a cited risk [3,4]. **No validated ipamorelin-specific stopping threshold exists** in the literature (gap).

### 7.6 The IGF-1 ceiling logic (why "in range," not "high")

The monitoring philosophy for any GH-axis intervention turns on a single biomarker — **serum IGF-1** — and the corpus supports a specific, non-obvious target for it. The naive assumption is "more GH/IGF-1 is better"; the epidemiology says otherwise on both ends. On the high side, elevated IGF-1 is prospectively associated with several cancers (breast OR 1.28 pooled across 17 studies [5]; breast HR 1.25 and prostate HR 1.31 in EPIC-Heidelberg [6]) — the rationale for not chronically pushing IGF-1 above the age/sex reference range. On the low side, EPIC-Heidelberg found a **U-shaped IGF-1–mortality relationship** [6]: very low IGF-1 *also* carries excess mortality. The synthesis is that the monitoring goal is to **keep IGF-1 within the age/sex reference range**, not to maximize it and not to minimize it. This is the anti-minimization correction that distinguishes a rigorous monitoring stance from a reflexive "lower is safer" one. Crucially, this entire IGF-1 logic is *class-level and associational* — it is built on endogenous-IGF-1 epidemiology, and **no study shows that exogenous ipamorelin alters cancer incidence**. The caution is theoretical, applied because chronically driving the GH→IGF-1 axis upward is the plausible-harm direction, not because ipamorelin has a demonstrated oncologic signal.

### 7.7 The thin-safety reality

All quantitative ipamorelin AE-rate data come from **one short-course (≤7-day) IV perioperative trial** [1]. Edema/glucose/IGF-1 risks under chronic dosing are **inferred** from the GH-axis class literature [3] and regulatory characterization [4], not from ipamorelin chronic trials. There is **no ipamorelin-specific human IGF-1 dose-response / ceiling data**. The cancer link is **associational and endogenous-IGF-1-based** — stated as theoretical caution, not established causation. The single most important caveat to carry forward is the **route-and-duration mismatch**: the one human safety dataset is 7-day IV inpatient exposure, while the real-world pattern is chronic subcutaneous self-administration over months. The reassuring AE rate (not higher than placebo) was earned in the *former* setting and tells us very little about the *latter*; it should not be read as a clean bill of health for nightly SC use over a multi-month cycle. Stated plainly: the **direction of the unknown is asymmetric** — the placebo-comparable AE rate cannot transfer to chronic SC use, and the GH-axis class risks (fluid retention, hyperglycemia, IGF-1 drift) are precisely the kind that *accumulate* with duration; so the absence of a chronic safety signal is an absence of data, not evidence of safety, and the unmeasured chronic-SC risk is more likely under- than over-stated by the 7-day IV record. AE *existence* (edema, arthralgia, carpal tunnel, glucose dysregulation) is established at the GH-class level; AE *rates* for chronic ipamorelin SC use are simply unknown.

---

## 8. Regulatory Status

- **FDA approval:** Ipamorelin has **never been FDA-approved**; clinical development was discontinued (no approved indication, anywhere, for anything) [8/9, regulatory (§F)].
- **FDA 503A compounding status:** Ipamorelin was placed on the **interim 503A Category 2** list (significant safety concern). It was **removed from Category 2 effective ~September 27, 2024** after the nomination was withdrawn, and referred to the **Pharmacy Compounding Advisory Committee (PCAC)**. At the **October 29, 2024 PCAC meeting**, FDA recommended against inclusion and the **committee voted NOT to add ipamorelin (acetate and free base) to the 503A bulk drug substances list** (alongside L-theanine, ibutamoren mesylate, and kisspeptin-10) [8/9, regulatory (§F)]. FDA's stated rationale for these peptides: immunogenicity risk from peptide-related impurities, inadequate API characterization, and limited/absent human safety data for the proposed routes [10, regulatory (§F)].
- **NOT part of the April-2026 Federal Register action.** FR Doc **2026-07361** (91 FR 20465, published April 16, 2026) removed a **different** set of **12 peptides** from Category 2 — BPC-157, TB-500 (thymosin β4 fragment), epitalon, GHK-Cu (injectable routes), MOTS-c, DSIP/emideltide, dihexa, **PEG-MGF (Mechano Growth Factor, pegylated)**, melanotan II, KPV, semax, LL-37/cathelicidin — and scheduled PCAC review meetings for **July 23–24, 2026** (with a further meeting before end of February 2027). **Ipamorelin is not among the removed peptides nor on that PCAC review agenda** [7, regulatory]. *(Note: an earlier draft of the 12-peptide list erroneously named "MK-677/ibutamoren" as the 12th substance; MK-677 is NOT in FR Doc 2026-07361 — the verified 12th is PEG-MGF.)*
  - **Net status for ipamorelin:** removed from Cat-2 (~Sept 2024) → PCAC-rejected (Oct 2024) → **NOT on the 503A bulks list** → **NOT part of the Apr-2026 action.** A follow-on PCAC meeting (Jul 23–24, 2026) was scheduled amid Evexias/Farmakeio litigation over the original Category-2 placement; treat compounding availability as a **moving target** [12, regulatory (§F)].
- **WADA anti-doping (2026 Prohibited List):** Ipamorelin is **PROHIBITED AT ALL TIMES** (in- and out-of-competition) under **S2 → S2.2 (Growth Hormone, its fragments and releasing factors)**, in the GH-secretagogue subsection. The 2026 List **names ipamorelin explicitly** among GHS examples ("…e.g. Anamorelin, Capromorelin, Ghrelin, Ibutamoren (MK-677), **Ipamorelin**, Lenomorelin (ghrelin)…"). It is a **non-specified substance** (strictest sanction tier) [8, regulatory].

---

## 9. Pharmacokinetics, Dose, Route & Formulation

### 9.1 The PK that exists vs the PK that's used

The **only** verified human PK is **IV**: terminal half-life ~2 h, clearance 0.078 L/h/kg, Vss 0.22 L/kg, dose-proportional over 4.21–140.45 nmol/kg, single GH pulse peaking ~0.67 h (Gobburu 1999, unified [4]; open_label; route=IV). The **real-world route is subcutaneous**, for which **no human PK exists** — SC bioavailability, half-life, and Tmax are **extrapolated**, not measured [route-extrapolation]. The only animal SC data are dosing studies [2,3] that did not characterize SC bioavailability; the only measured non-IV route is rat intranasal (~20%) (Johansen PB 1998, unified [9]).

### 9.2 Practitioner-convention dosing (NOT efficacy)

> **Type-tag discipline:** the following are **practitioner_protocol** conventions used **only** for dose/cycle/route. They are **not** regulatory-sanctioned dosing, and **no human efficacy is asserted from them.**

Two named protocols converge on the same pattern [13, practitioner_protocol][14, practitioner_protocol]:

- **Wittmer Rejuvenation Clinic** (Dr. Michael Wittmer), "CJC-1295/Ipamorelin Complete Guide," 2025: ipamorelin SC before bed, once daily; beginner 100–150 mcg / intermediate 200 mcg / advanced 200–300 mcg; cycles 12 weeks to 3–6 months; stacked with CJC-1295 as a 6 mg/6 mg blend; inject on empty stomach, wait 30–45 min before eating.
- **Optimal Clinic USA** (Dr. Michelle Anderson, Medical Director), CJC-1295 + Ipamorelin guide, 2026: ipamorelin 100–300 mcg per injection SC, 1–3×/day with a before-sleep dose emphasized, stacked with CJC-1295; the page explicitly states these are **non-standardized community protocols**, not controlled-trial regimens.

**Summary convention (admin only):** ~100–300 mcg SC at night (advanced ~200–300 mcg), once daily (sometimes AM+PM), on an empty stomach, frequently co-administered with **CJC-1295** (no-DAC preferred, to preserve pulsatility), in multi-week cycles. The empty-stomach / before-bed timing reflects the goal of stacking on a natural nocturnal GH pulse and avoiding the GH-blunting effect of postprandial somatostatin/insulin — but again, **no human outcome data validate this pattern for any goal.**

### 9.3 Sourcing reality

Two supply channels exist and must not be conflated:

1. **Gray-market research-chemical vendors** ("research-use-only / not-for-human-use"). Example: a vendor trading as "Empower Peptides" (empower-peptides.com — **NOT** the licensed compounder Empower Pharmacy) sells ipamorelin 5/10 mg lyophilized vials at ~$38–53, labeled "Research Grade … Not for injection," listing CAS 170851-70-4, C₃₈H₄₉N₉O₅, MW 711.86, with a self/vendor-asserted COA [6, vendor_label]. Community purity norm is HPLC ≥98% + MS identity, but commonly used third-party labs (e.g., Janoshik) are **NOT ISO/IEC 17025 accredited**, and analog-substitution fraud is documented [7, vendor_label].
2. **Licensed compounding pharmacies (503A/503B).** Following the 2024 FDA action, ipamorelin is **effectively delisted** — Empower Pharmacy (a licensed 503A/503B facility) does **not** currently list ipamorelin among its compounded peptides [11, regulatory/vendor]. **No admissible 503A/503B compounding-pharmacy clinical data sheet** for ipamorelin was located, consistent with the delisting.

> The only admissible technical data is vendor-label reconstitution/identity (admin math only): lyophilized white powder; reconstitute in sterile/bacteriostatic water to ≥100 µg/mL; refrigerate 2–7 days post-reconstitution; freeze for longer storage [6,7, vendor_label].

---

## 10. N=1 / Trial-Design Considerations

This is a **goal-agnostic** entry — operator/goal fields are intentionally blank. If a clinician and patient nonetheless contemplate use, the design constraints implied by the evidence are:

- **No validated efficacy endpoint exists for any non-ileus use.** Any N=1 is therefore *exploratory*; pre-specify the outcome and acknowledge the absence of human efficacy data up front.
- **Anchor on the biomarker the pharmacology actually moves:** **serum IGF-1** [[biomarkers/igf-1]] is the proximate, measurable readout of sustained GH-axis stimulation and the natural ceiling marker. Keep IGF-1 **within the age/sex reference range** — the EPIC-Heidelberg U-shaped mortality curve [6] means "minimize IGF-1" is wrong; "keep in range" is the target.
- **Monitor the GH-axis risk cluster:** **fasting glucose and HbA1c** (insulin resistance / hyperglycemia), plus clinical surveillance for **edema, arthralgia, and carpal-tunnel symptoms** [3,4].
- **Respect the dosing unknowns:** there is **no human SC PK**, so any SC regimen is an extrapolation; the practitioner-convention dose range (~100–300 mcg SC nightly) is a community pattern, not a validated dose (unified [30], [31]).
- **Respect the time-horizon gap:** human safety data extend to ~7–10 days IV only. Chronic SC use is wholly unstudied — the appropriate stance is conservative, with explicit stopping rules (§7.5).
- **Doctor discussion required** (frontmatter), and the WADA status (prohibited at all times) is disqualifying for any tested athlete.

---

## 11. Bottom Line — Supported vs Marketed

**Supported by evidence:**

- Ipamorelin **acutely raises GH** in humans in a clean, dose-proportional, self-limiting pulse (IV; t½ ~2 h) — a verified *pharmacology* result (unified [4]).
- In **animals**, it is a potent, **selective** GH secretagogue (no ACTH/cortisol/prolactin co-release at high multiples of the GH ED50) (unified [1]) and produces GH-mediated somatic/bone-**content** growth in rats (unified [10], [11]).
- Its strongest *functional* preclinical track is **gut motility** (the development indication) (unified [13], [14]).

**Marketed but NOT supported in humans:**

- Muscle gain, fat loss, athletic performance, anti-aging/longevity, sleep, recovery — **zero human efficacy data**; all extrapolation from acute GH pharmacology.
- "Increases bone density" — overstated; the data show increased bone **content/size with unchanged volumetric BMD** (unified [11]).
- "Robust IGF-1 elevation" — contradicted by rat data showing intermittent dosing did **not** raise IGF-1 (unified [10]); no human IGF-1 dose-response exists.
- "Selective / no side effects in people" — selectivity is **animal-grounded**, and regulators flagged fluid retention / hyperglycemia / CHF concerns (unified [22]).

**Regulatory reality:** never approved; the only human efficacy program failed and was discontinued; removed from 503A Cat-2 (~Sept 2024) and PCAC-rejected for the 503A bulks list (Oct 2024); not part of the Apr-2026 FR action; WADA-prohibited at all times.

> **One-sentence bottom line:** Ipamorelin is a mechanistically clean, animal-validated *selective GH secretagogue* whose only human-efficacy program (postoperative ileus) failed and was discontinued — so despite solid acute human pharmacology, there is **zero human efficacy evidence** for any of its marketed muscle/fat/anti-aging uses, and it is unapproved, compounding-rejected, and WADA-banned.

---

## Bibliography (unified, deduped across all six sections)

> No Wikipedia citations anywhere. Type-tags and tiers carried from the validated corpus.

[1] Raun K, Hansen BS, Johansen NL, Thøgersen H, Madsen K, Ankersen M, Andersen PH. "Ipamorelin, the first selective growth hormone secretagogue." *European Journal of Endocrinology* 1998;139(5):552–561. PMID: 9849822. DOI: 10.1530/eje.0.1390552. tag=animal+in_vitro. tier=1. *(Foundational discovery / potency / selectivity paper; in-vitro rat pituitary + in-vivo rat & swine; Novo Nordisk, Måløv DK.)*

[2] Ankersen M, Johansen NL, Madsen K, Hansen BS, Raun K, Nielsen KK, Thøgersen H, Hansen TK, Peschke B, Lau J, Lundt BF, Andersen PH. "A new series of highly potent growth hormone-releasing peptides derived from ipamorelin." *Journal of Medicinal Chemistry* 1998;41(19):3699–3704. PMID: 9733495. DOI: 10.1021/jm9801962. tag=mechanism_review. tier=1. *(SAR / medicinal-chemistry series; ipamorelin as scaffold lead; oral-bioavailability SAR; source of the NNC 26-0235 dog ~10% oral-bioavailability derivative figure.)*

[3] PubChem Compound Summary, CID 9831659, "Ipamorelin." National Library of Medicine / NCBI. URL: https://pubchem.ncbi.nlm.nih.gov/compound/9831659 . tag=regulatory. tier=1. *(Authoritative chemical database: C₃₈H₄₉N₉O₅, average MW 711.9, monoisotopic 711.3857; CAS 170851-70-4; synonym NNC 26-0161.)*

[4] Gobburu JVS, Agersø H, Jusko WJ, Ynddal L. "Pharmacokinetic-pharmacodynamic modeling of ipamorelin, a growth hormone releasing peptide, in human volunteers." *Pharmaceutical Research* 1999;16(9):1412–1416. PMID: 10496658. DOI: 10.1023/A:1018955126402. tag=open_label. tier=1. *(First-in-human PK/PD; n=40 healthy males, 8/dose × 5 IV doses; t½ ~2 h; CL 0.078 L/h/kg; Vss 0.22 L/kg; SC50 214 nmol/L; single GH pulse ~0.67 h; randomized double-blind placebo-controlled dose-escalation. Biomarker-only, not an efficacy trial.)*

[5] Sinha DK, Balasubramanian A, Tatem AJ, Rivera-Mirabal J, Yu J, Kovac J, Pastuszak AW, Lipshultz LI. "Beyond the androgen receptor: the role of growth hormone secretagogues in the modern management of body composition in hypogonadal males." *Translational Andrology and Urology* 2020;9(Suppl 2):S149–S159. PMID: 32257855. PMCID: PMC7108996. tag=mechanism_review. tier=2. *(Ipamorelin as selective ghrelin/GHS-R1a agonist sharing the receptor with GHRP-2/GHRP-6/ibutamoren; explicitly flags limited ipamorelin-specific human data and a rodent GH-independent weight-gain finding.)*

[6] Cayman Chemical / vendor catalog — "Ipamorelin (acetate)." URL: https://www.caymanchem.com/product/39813/ipamorelin-(acetate) . tag=vendor_label. tier=3. *(Physical description [white/off-white powder] and acetate-salt presentation ONLY; not used to ground any pharmacology number.)*

[7] Yin Y, Li Y, Zhang W. "The Growth Hormone Secretagogue Receptor: Its Intracellular Signaling and Regulation." *International Journal of Molecular Sciences* 2014;15(3):4837–4855. PMID: 24651458. PMCID: PMC3975427. tag=mechanism_review. tier=1. *(Canonical GHS-R1a signaling: Gαq/11→PLC→IP₃/DAG→Ca²⁺→GH exocytosis; constitutive activity; β-arrestin desensitization/internalization.)*

[8] Colldén G, Tschöp MH, Müller TD. "Therapeutic Potential of Targeting the Ghrelin Pathway." *International Journal of Molecular Sciences* 2017;18(4):798. PMID: 28398233. PMCID: PMC5412382. tag=mechanism_review. tier=1. *(GHS-R1a tissue distribution [pituitary-dominant + hypothalamic NPY/AgRP]; 7TM GPCR; Gαq/11 + PI3K + ERK1/2 → intracellular Ca²⁺.)*

[9] Johansen PB, Hansen KT, Andersen JV, Johansen NL. "Pharmacokinetic evaluation of ipamorelin and other peptidyl growth hormone secretagogues with emphasis on nasal absorption." *Xenobiotica* 1998;28(11):1083–1092. PMID: 9879640. DOI: 10.1080/004982598238976. tag=animal. tier=2. *(Rat IV + intranasal PK; ~5-fold lower CL vs GHRP-6; mainly urinary excretion; ~20% intranasal bioavailability. Authorship per PubMed [Johansen PB], correcting a secondary "Agersø" attribution. A distinct paper from [11] below.)*

[10] Johansen PB, Nowak J, Skjærbæk C, Flyvbjerg A, Andreassen TT, Wilken M, Ørskov H. "Ipamorelin, a new growth-hormone-releasing peptide, induces longitudinal bone growth in rats." *Growth Hormone & IGF Research* 1999;9(2):106–113. PMID: 10373343. DOI: 10.1054/ghir.1999.9998. tag=animal. tier=1. *(Dose-dependent longitudinal bone-growth rate, tetracycline-label method; intermittent SC dosing did NOT raise total IGF-1/IGFBPs; Novo Nordisk + Aarhus University.)*

[11] Svensson J, Lall S, Dickson SL, Bengtsson B-Å, Rømer J, Ahnfelt-Rønne I, Ohlsson C, Jansson J-O. "The GH secretagogues ipamorelin and GH-releasing peptide-6 increase bone mineral content in adult female rats." *Journal of Endocrinology* 2000;165(3):569–577. PMID: 10828840. DOI: 10.1677/joe.0.1650569. tag=animal. tier=1. *(12-wk continuous SC osmotic minipump 0.5 mg/kg/day; DXA + pQCT; increased BMC via increased bone area, volumetric BMD unchanged; Gothenburg/Göteborg + Novo Nordisk.)*

[12] "The growth hormone secretagogue ipamorelin counteracts glucocorticoid-induced decrease in bone formation of adult rats." *Growth Hormone & IGF Research* 2001 (ScienceDirect S1096637401902394). tag=animal. tier=1. *(Novo-Nordisk-origin compound; counters methylprednisolone-induced bone loss; bibliographic listing verified, full text paywalled — corpus-missing WARN per gate-4.75 IC-13.)*

[13] Venkova K, Mann W, Nelson R, Greenwood-Van Meerveld B. "Efficacy of ipamorelin, a novel ghrelin mimetic, in a rodent model of postoperative ileus." *Journal of Pharmacology and Experimental Therapeutics* 2009;329(3):1110–1116. PMID: 19289567. DOI: 10.1124/jpet.108.149211. tag=animal. tier=1. *(Rat POI model; single IV + repetitive dosing improved transit, fecal output, food intake, body weight; independent group [Univ. of Oklahoma HSC / VA].)*

[14] Venkova K, Fraser G, Hoveyda HR, Greenwood-Van Meerveld B. "Efficacy of ipamorelin, a ghrelin mimetic, on gastric dysmotility in a rodent model of postoperative ileus." *Journal of Experimental Pharmacology* 2012;4:71–80. DOI: 10.2147/JEP.S35396. URL: https://www.tandfonline.com/doi/full/10.2147/JEP.S35396 . tag=animal. tier=2. *(Rat gastric-emptying %, ex-vivo smooth-muscle contractility; GHS-R1a-mediated cholinergic gastroprokinesis; Tranzyme co-authorship disclosed; open-access journal.)*

[15] Beck DE, Sweeney WB, McCarter MD; Ipamorelin 201 Study Group. "Prospective, randomized, controlled, proof-of-concept study of the ghrelin mimetic ipamorelin for the management of postoperative ileus in bowel resection patients." *International Journal of Colorectal Disease* 2014;29(12):1527–1534. PMID: 25331030. DOI: 10.1007/s00384-014-2030-8. NCT00672074. tag=rct. tier=1. *(The single peer-reviewed human efficacy RCT; n=117 enrolled / 114 mITT; primary endpoint NOT met — time to first tolerated meal 25.3 h vs 32.6 h, p=0.15; well tolerated, TEAE 87.5% drug vs 94.8% placebo; Helsinn. Short-course IV — does not address chronic SC use.)*

[16] ClinicalTrials.gov. "Safety and Efficacy of Ipamorelin for Management of Post-Operative Ileus." NCT00672074. Sponsor: Helsinn Therapeutics (U.S.), Inc. Phase II; randomized, quadruple-masking, parallel; n=117 (actual); Completed Dec 2009; hasResults=false. URL: https://clinicaltrials.gov/study/NCT00672074 . tag=rct. tier=1. *(Registry record for the trial published as [15].)*

[17] ClinicalTrials.gov. "Safety and Efficacy of Ipamorelin Compared to Placebo for the Recovery of Gastrointestinal Function." NCT01280344. Sponsor: Helsinn Therapeutics (U.S.), Inc. Phase II; randomized, quadruple-masking, parallel; 4 arms (ipamorelin 0.03 mg/kg BID, 0.06 mg/kg BID, 0.06 mg/kg TID, placebo); n=320 (actual); primary completion Jun 2013, completion May 2014; hasResults=false. URL: https://clinicaltrials.gov/study/NCT01280344 . tag=rct. tier=1. *(Larger confirmatory POI RCT; no structured results posted; no positive efficacy publication identified.)*

[18] Müller TD, Nogueiras R, Andermann ML, et al. "Ghrelin." *Molecular Metabolism* 2015;4(6):437–460. PMID: 26042199. DOI: 10.1016/j.molmet.2015.03.005. tag=mechanism_review. tier=1. *(Ghrelin / GHS-receptor → GH release → IGF-1 axis; mechanistic basis for both efficacy and GH-excess risk; class mechanism, not ipamorelin-specific chronic dose-response.)*

[19] Liu H, Bravata DM, Olkin I, et al. "Systematic review: the safety and efficacy of growth hormone in the healthy elderly." *Annals of Internal Medicine* 2007;146(2):104–115. PMID: 17227934. DOI: 10.7326/0003-4819-146-2-200701160-00005. tag=mechanism_review. tier=1. *(Controlled GH-exposure AEs — edema, arthralgia, carpal-tunnel syndrome, impaired glucose tolerance / insulin resistance. AE *existence* at class level, not ipamorelin AE rates.)*

[20] Endogenous Hormones and Breast Cancer Collaborative Group (Key TJ, Appleby PN, Reeves GK, Roddam AW). "Insulin-like growth factor 1 (IGF1), IGF binding protein 3 (IGFBP3), and breast cancer risk: pooled individual data analysis of 17 prospective studies." *Lancet Oncology* 2010;11(6):530–542. PMID: 20472501. DOI: 10.1016/S1470-2045(10)70095-4. tag=cohort. tier=1. *(Breast-cancer OR 1.28 [95% CI 1.14–1.44] highest vs lowest IGF-1; ER-positive predominant; endogenous-IGF-1 epidemiology; basis for the sustained-IGF-1 cancer caution.)*

[21] Mukama T, Srour B, Johnson T, Katzke V, Kaaks R. "IGF-1 and Risk of Morbidity and Mortality From Cancer, Cardiovascular Diseases, and All Causes in EPIC-Heidelberg." *Journal of Clinical Endocrinology & Metabolism* 2023;108(10):e1092–e1105. PMID: 37066827. DOI: 10.1210/clinem/dgad212. tag=cohort. tier=1. *(Prospective case-cohort, ~7,461 with IGF-1; higher IGF-1 → breast HR 1.25, prostate HR 1.31; U-shaped IGF-1–mortality curve; reinforces "keep IGF-1 in range" rather than minimize.)*

[22] U.S. FDA / Pharmacy Compounding Advisory Committee (PCAC), meeting October 29, 2024 — review of ipamorelin (acetate and free base) for the 503A Bulk Drug Substances List; FDA recommendation against inclusion; committee voted no. tag=regulatory. tier=1. URL: https://www.fda.gov/advisory-committees/advisory-committee-calendar/october-29-2024-meeting-pharmacy-compounding-advisory-committee-10292024 ; corroborated: https://a4pc.org/news/pcac-votes-against-four-nominated-bulk-drug-substances . *(Not-FDA-approved status; Cat-2 removal ~Sept 2024; PCAC no-vote; member-cited fluid retention / hyperglycemia / CHF / insufficient efficacy-safety concerns.)*

[23] U.S. FDA. "Pharmacy Compounding Advisory Committee; Notice of Meeting; … Bulk Drug Substances Nominated for Inclusion on the Section 503A Bulk Drug Substances List." 91 FR 20465, April 16, 2026; FR Doc 2026-07361. tag=regulatory. tier=1. URL: https://www.govinfo.gov/content/pkg/FR-2026-04-16/html/2026-07361.htm . *(Removes 12 peptides — BPC-157, TB-500, epitalon, GHK-Cu [injectable], MOTS-c, DSIP/emideltide, dihexa, PEG-MGF, melanotan II, KPV, semax, LL-37 — from Cat-2 and sets PCAC review Jul 23–24, 2026 + a further meeting before end of Feb 2027. **Ipamorelin NOT included.**)*

[24] World Anti-Doping Agency. "The 2026 Prohibited List" — Section S2.2 (Growth Hormone, its fragments and releasing factors), GH-secretagogue subsection. tag=regulatory. tier=1. URL: https://www.wada-ama.org/en/prohibited-list ; verbatim ipamorelin listing verified via national anti-doping authority mirror (SUEK, Finland): https://kamu.suek.fi/en/dopingsubstances/ . *(Ipamorelin named explicitly among GHS examples; PROHIBITED AT ALL TIMES, non-specified.)*

[25] PCAC sourcing/landscape coverage (FDA Law Blog "FDA's Pep(tide) Rally!" thefdalawblog.com, Apr 2026; Lexology FDA-peptide-Category-2 coverage). tag=regulatory. tier=2. *(FDA rationale for non-inclusion: immunogenicity from impurities, inadequate API characterization, limited human clinical data; ipamorelin acetate among litigated substances. Used for regulatory characterization only.)*

[26] Empower Pharmacy, "Expanding Access: Peptides" (empowerpharmacy.com — licensed 503A/503B). tag=regulatory/vendor. tier=2. *(Current compounded peptide list does NOT include ipamorelin — evidence of effective delisting.)*

[27] FDA, "July 23–24, 2026 Meeting of the PCAC" + FDA Law Blog. tag=regulatory. tier=1.5. *(Follow-on PCAC review amid Evexias/Farmakeio litigation over the 2023 Category-2 placement; unresolved as of research date.)*

[28] "Ipamorelin" product page, empower-peptides.com (gray-market research vendor; NOT Empower Pharmacy). tag=vendor_label. tier=4. *(5/10 mg vials; CAS 170851-70-4, C₃₈H₄₉N₉O₅, MW 711.86; "research-use-only, not for injection." Identity / reconstitution math ONLY; gray-market flag.)*

[29] Janoshik COA / peptide purity-testing explainers (vantixbio.com; thepeptidelist.com; vendor COA pages). tag=vendor_label. tier=4. *(Community purity norm HPLC ≥98% + MS identity; Janoshik NOT ISO/IEC 17025 accredited; documented analog-substitution fraud. Identity / QC context ONLY.)*

[30] Wittmer Rejuvenation Clinic (Dr. Michael Wittmer), "CJC-1295/Ipamorelin Complete Guide," 2025. tag=practitioner_protocol. tier=2.7. *(Ipamorelin SC before bed; 100–150 / 200 / 200–300 mcg tiers; 12 wk–6 mo cycles; CJC-1295 blend. Dose/cycle/route ONLY.)*

[31] Optimal Clinic USA (Dr. Michelle Anderson, Medical Director), "CJC-1295 + Ipamorelin Peptide Therapy," 2026. tag=practitioner_protocol. tier=2.7. *(Ipamorelin 100–300 mcg SC, 1–3×/day, before-sleep emphasized, CJC-1295 stack; self-labeled non-standardized community protocol. Dose/cycle/route ONLY.)*

**Unified bibliography source count: 31.**

---

## Citation Numbering Note + Crosswalk

> **HOW TO READ EVERY INLINE CITATION IN THIS REPORT (read before resolving any `[N]`).**
>
> This report uses **two numbering schemes**, and the rule is mechanical:
>
> 1. **Detail sections §1–§9 use SECTION-LOCAL inline numbers.** A bare `[N]` inside §1–§9 is the *local* number of that section's source draft — it does **NOT** point at unified bibliography entry [N]. To resolve it, find the section's column letter (A–F, mapped below) in the **crosswalk table** and read across to the unified entry. *(Example: `[2]` in §2 is section-B-local and resolves via column B to unified **[4]** = Gobburu 1999; it is **not** unified [2] = Ankersen 1998.)*
> 2. **The synthesis layers — §0 (Evidence Map), §5 (Lineage Audit), and the Bibliography — use UNIFIED numbers** (because they pool sources across all sections and have no single home column). Their `[N]` points directly at unified bibliography entry [N].
> 3. **A few inline references span sections** (e.g., a §4 sentence pointing at a §3 preclinical paper). Where a marker would otherwise be ambiguous, it is written explicitly as **`unified [N]`** — that form always means the unified bibliography entry, regardless of which section it appears in.
>
> **In short:** bare `[N]` in §1–§9 → section-local (decode via the column for that section); `unified [N]`, and every `[N]` in §0/§5/Bibliography → unified. The crosswalk below is complete: every section-local number in every section resolves to exactly one unified entry.
>
> **Section → crosswalk-column map:** §1 = **A** · §2 = **B** · §3 = **C** · §4 = **D** · §6, §7, §10 = **E** · §8, §9 = **F**. (§0, §5, §11 cite unified numbers directly; §5's table "#" column is a study index, not a citation.)

The unified bibliography above ([1]–[31]) is the **canonical** numbering for this report. The original six section drafts (A–F) each numbered their citations locally; the table below maps **every** section-local citation to its unified number, leaving no inline marker unresolved. (Duplicate papers across sections collapse to a single unified entry; the same paper may carry slightly different section-local tags — e.g., Raun 1998 is `animal+in_vitro` in A/B/C and `mechanism_review/animal` in F — without conflict.)

| Unified | Source (short) | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| [1] | Raun 1998 (PMID 9849822) | [1] | [1] | [1] | — | — | [1] |
| [2] | Ankersen 1998 (PMID 9733495) | [5] | — | — | — | — | — |
| [3] | PubChem CID 9831659 | [3] | — | — | — | — | — |
| [4] | Gobburu 1999 (PMID 10496658) | [4] | [2] | — | [2] | — | — |
| [5] | Sinha 2020 (PMID 32257855) | — | [5] | — | — | — | — |
| [6] | Cayman vendor label | [6] | — | — | — | — | — |
| [7] | Yin 2014 (PMID 24651458) | — | [3] | — | — | — | — |
| [8] | Colldén 2017 (PMID 28398233) | — | [4] | — | — | — | — |
| [9] | Johansen PB 1998, Xenobiotica (PMID 9879640) | [10] | — | — | — | — | — |
| [10] | Johansen 1999, longitudinal growth (PMID 10373343) | — | — | [3] | — | — | [2] |
| [11] | Svensson 2000, BMC (PMID 10828840) | — | — | [2] | — | — | [3] |
| [12] | Glucocorticoid/bone 2001 (S1096637401902394) | — | — | — | — | — | [4] |
| [13] | Venkova 2009, POI (PMID 19289567) | — | — | [4] | — | — | — |
| [14] | Venkova 2012, gastric dysmotility (DOI 10.2147/JEP.S35396) | — | — | [5] | — | — | — |
| [15] | Beck 2014, POI RCT (PMID 25331030) | — | — | — | [1] | [1] | [5] |
| [16] | NCT00672074 registry | — | — | — | [3] | — | — |
| [17] | NCT01280344 registry | — | — | — | [4] | — | — |
| [18] | Müller 2015, "Ghrelin" (PMID 26042199) | — | — | — | — | [2] | — |
| [19] | Liu 2007, GH in elderly (PMID 17227934) | — | — | — | — | [3] | — |
| [20] | EHBCCG 2010, IGF-1/breast (PMID 20472501) | — | — | — | — | [5] | — |
| [21] | Mukama 2023, EPIC-Heidelberg (PMID 37066827) | — | — | — | — | [6] | — |
| [22] | FDA PCAC Oct 29 2024 | — | — | — | — | [4] | [8]/[9] |
| [23] | FR Doc 2026-07361 (Apr 16 2026) | — | — | — | — | [7] | — |
| [24] | WADA 2026 Prohibited List, S2.2 | — | — | — | — | [8] | — |
| [25] | FDA Law Blog / Lexology (regulatory) | — | — | — | — | — | [10] |
| [26] | Empower Pharmacy peptide list | — | — | — | — | — | [11] |
| [27] | FDA PCAC Jul 23–24 2026 / litigation | — | — | — | — | — | [12] |
| [28] | empower-peptides.com vendor page | — | — | — | — | — | [6] |
| [29] | Janoshik COA / purity explainers | — | — | — | — | — | [7] |
| [30] | Wittmer Clinic protocol (2025) | — | — | — | — | — | [13] |
| [31] | Optimal Clinic protocol (2026) | — | — | — | — | — | [14] |

*Note on the two "Johansen" papers:* unified [9] (Johansen PB 1998, *Xenobiotica*, nasal-absorption PK, PMID 9879640) and unified [10] (Johansen 1999, longitudinal bone growth, PMID 10373343) are **distinct papers** with distinct PMIDs — kept separate per the Phase-4.25 disambiguation. Section A also resolved an "Agersø vs Johansen" first-author discrepancy on [9] in favor of PubMed.

---

## Provenance & Citation-Integrity Note

- **Synthesis basis:** This report integrates ONLY the validated corpus (sections A–F + id-reconcile-source.md + gate-4.75) for Ipamorelin. **No new web retrieval** was performed during synthesis; every claim traces to a section's verified citation. `## Post-fix grep audit` blocks were read only to confirm the corrected live-body values and were excluded from content.
- **Deep paired-judge:** the corpus passed deep paired judges at the **92** bar (per documented efficient-calibration), with reconcile **PASS** and the 4.75 integrity gate **PASS**.
- **Phase 4.25 ID-Reconcile:** PASS — zero cross-section value disagreements across all five entity classes (citations, institutions, compound identifiers, regulatory dates, trial registrations). Numerical triangulation matched across sections; the Novo-Nordisk single-lineage concentration share independently recomputed to ~80%.
- **Phase 4.75 Integrity Gate:** PASS — all 13 IC checks pass; IC-13 carries **2 corpus-missing WARNs** (paywalled primaries: glucocorticoid-bone 2001 [unified 12]; Svensson 2000 full text [unified 11] — both PMID/listing-verified, abstract figures corroborated). The prior IC-12 HALT (a Wikipedia URL grounding the discontinuation claims in Section D) was **resolved** — the Wikipedia entry was removed and those claims re-grounded on the Beck 2014 RCT + the two ClinicalTrials.gov registry records. **No Wikipedia citation appears anywhere in this report.**
- **Carried canonical reconcile values:** Raun 1998 PMID 9849822; Gobburu 1999 PMID 10496658; Beck 2014 PMID 25331030 (NCT00672074; 25.3 h vs 32.6 h, p=0.15; n=117 enrolled / 114 mITT); NCT01280344 (n=320); FDA Cat-2 removed ~Sept 2024 + PCAC voted against Oct 29 2024 + NOT in the Apr-2026 FR action (FR Doc 2026-07361); WADA S2.2 prohibited at all times.
- **Tooling note:** in the upstream pipeline, **WebSearch/WebFetch were substituted for the Tavily MCP** retrieval layer; the **judge bar of 92** reflects the documented efficient-calibration policy for this run.
- **Type-tag discipline preserved:** vendor_label and practitioner_protocol citations ground only physical-description, identity/reconstitution math, and dose/cycle/route conventions — never efficacy, AE rates, or therapeutic dosing. Species + n are carried on every animal/in-vitro claim where the primary reports them. IV→SC route extrapolation and animal→human selectivity extrapolation are surfaced as first-class limitations, not silently bridged.

---

## Post-fix refinement audit (Phase 7)

**Scope:** address the Phase 6 critique (gate-6.md) WITHOUT adding any new external citation (corpus frozen at the unified [1]–[31] bibliography). No value, identifier, species+n, or honest-negative was altered; no Wikipedia introduced.

**MAJOR — citation-numbering collision (resolved via the SAFE path, not a unified renumber):**

- **Diagnosis confirmed.** The body detail sections §1–§9 were already *consistently section-local* (e.g., Gobburu = B-local/D-local [2], Svensson = C-local [2], Beck = D-local/E-local [1]); the defect was (a) a handful of **unified-number leaks** into those section-local sections and **garbled slash markers** (`[2/4]`, `[12/5]`, `[8/9]`, `[2/3/4]`), plus (b) the absence of a point-of-use warning, which is why a reader resolved §8's correct F-local `[10]`/`[12]` against the unified list and landed on animal papers (critique finding 3 — a *reading* artifact of the missing note, not a wrong citation).
- **Fix (a) — consistency restored.** Converted every leaked/garbled inline marker so each section is internally consistent:
  - §1.2 `[2]`→`[5]` (A-local Ankersen); §1.5 `[12/5]`→`[5]` (A-local Ankersen); §1.5 reconstitution-math `[6][7]`→explicit `unified [28], [29]` (same vendor pair §9.3 uses).
  - §2.3 `[2/4]`→`[2]` (B-local Gobburu).
  - §3.2 glucocorticoid `[12]`→explicit `unified [12]` (cross-section; not in column C).
  - §4 (the sharpest mixing, finding 2) `[15]`→`[1]`, `[17]`→`[4]` (D-local); §4 intro `[2/3/4]`→`[3, rct][4, rct]` (the two registries); the §4.5 Venkova `[13,14]` recast as a `(§3.5)` cross-reference.
  - §6 `[1,2,3,4 (§B)]`→explicit `unified [1],[4],[7],[8]`.
  - §8 FDA-approval `[4]`→`[8/9, regulatory (§F)]` and removed the redundant/incorrect `[4]` (F-local 4 = animal) from the PCAC-vote line.
  - §9.1 human IV PK `[2/4]`→`Gobburu 1999, unified [4]`; rat intranasal `[10]`→`Johansen PB 1998, unified [9]`.
  - §10 dose `[13,14]`→`unified [30], [31]`; §11 Bottom-Line markers all recast to explicit `unified [..]`.
- **Fix (b) — prominent resolver note + section→column map** added at the head of "Citation Numbering Note + Crosswalk," plus a one-line unified-numbering tag on §0. Convention is now mechanical: **bare `[N]` in §1–§9 = section-local (decode by the section's column); `unified [N]`, and all `[N]` in §0/§5/§11/Bibliography = unified.**
- **Crosswalk completeness verified mechanically.** Every section-local number actually used in each detail section resolves within that section's crosswalk column (script check): §1{1,3,4,5,6,10}⊂A · §2{1–5}⊂B · §3{1–5}⊂C · §4{1–4}⊂D · §7{1–6}⊂E · §8{7,8,9,10,12}⊂F · §9{2,6,7,11,13,14}⊂F · §10{3,6}⊂E. **Zero out-of-column markers remain.**

**MINORS (gate-6 findings 2–4):**

1. *Finding 2 (logical-inconsistency, §4.5 one-sentence mix)* — **FIXED.** Beck and the Phase 2 RCT are now both D-local `[1]`/`[4]`; the Venkova reference became a `(§3.5)` pointer. No two schemes share a sentence.
2. *Finding 3 (§8 regulatory markers resolving to animal papers)* — **FIXED at root.** §8's `[10]`/`[12]` are correct *F-local* regulatory sources (unified [25] FDA Law Blog, unified [27] PCAC-Jul); the resolver note + `(§F)` tags now make them resolve correctly. Also corrected the genuine error on the FDA-approval line (`[4]`→`[8/9]`).
3. *Finding 4 (balance — directional asymmetry of chronic-SC risk)* — **ADDRESSED.** §7.7 now states plainly that the unknown is directionally asymmetric: the 7-day IV placebo-comparable AE rate cannot transfer to chronic SC use, the GH-axis class risks accumulate with duration, and absence of a chronic signal is absence of data, not evidence of safety.
- **Deferred:** none.

**No new citation:** y (bibliography unchanged at 31 entries; all `unified [N]` references ∈ [1]–[31]).

**Grep/consistency clean:** y — no inline marker is left ambiguous; the only remaining slash markers (`[8/9, regulatory (§F)]`) are the intended F-local pair that the crosswalk maps (both → unified [22] PCAC); load-bearing values (p=0.15; 25.3 vs 32.6 h; n=117/114; n=320; SC50 214 nmol/L; MW 711.9; 200-fold; 87.5% vs 94.8%; all PMIDs) verified unchanged; no Wikipedia present (the only "Wikipedia" strings are the pre-existing "no Wikipedia" assurances).
