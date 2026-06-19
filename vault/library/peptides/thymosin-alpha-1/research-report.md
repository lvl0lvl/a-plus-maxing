---
title: "Thymosin Alpha-1 — Research Report"
type: research-report
permalink: a-plus-maxing/library/peptides/thymosin-alpha-1/research-report
class: peptide
evidence_tier: B
risk_tier: low
status: complete
created: 2026-06-18
last_verified: 2026-06-18
review_cadence: on new RCT or 503A/regulatory change
---

# Thymosin Alpha-1 (Tα1, thymalfasin; brand Zadaxin)

## Metadata
- **Class:** peptide — 28-amino-acid N-acetylated cleavage fragment of prothymosin alpha (thymic origin); immunomodulator
- **Evidence tier:** **B** overall — real RCTs + meta-analyses and a 25-year approved-drug record abroad, BUT the single best-quality trial (sepsis) is negative and benefit is indication-specific. **Effectively D for the operator's goal** (general post-illness recovery/deconditioning — no direct RCT).
- **Risk tier:** **low** — notably clean safety profile across >2,000 patients and two large sepsis RCTs.
- **Regulatory:** NOT FDA-approved (US); approved in ~30+ countries (China principal market); removed from US 503A Category 2 (Sept 2024). WADA: NOT prohibited (contrast TB-500/thymosin-beta-4).
- **Last verified:** 2026-06-18

> Deep pass (peptide-library track). Method + full verified-source ledger: `.provenance/`. Companion layers:
> [[library/peptides/thymosin-alpha-1/practitioner-layer]] · [[library/peptides/thymosin-alpha-1/non-english-layer]].

---

## TL;DR

Thymosin alpha-1 is a thymic immunomodulatory peptide — an immune **rebalancer** (it both restores exhausted
T-cell/NK function and dampens over-inflammation via TLR→dendritic-cell→Th1 signaling with an IDO/Treg
counterweight). It is a real, marketed drug abroad (Zadaxin, ~30+ countries, ~25 years) for chronic hepatitis B/C,
cancer adjuvant, and immune/vaccine enhancement, with an **excellent safety record**. The decisive honest finding:
the **efficacy story recently shifted against it** in its most-studied acute indication — the largest, highest-quality
sepsis trial (**TESTS, BMJ 2025, n=1,089, double-blind**) was **NEGATIVE** on 28-day mortality (HR 0.99), and the
positive 2025 meta-analysis (OR 0.73) is an artifact of small single-center trials that vanishes (OR 0.86, NS) in the
high-quality subgroup. For the operator's actual goal — general post-illness recovery/immune restoration in a healthy
adult — **there is no RCT at all** (goal-fit gap). US access is doubly restricted: not FDA-approved AND removed from
503A Category 2. It is, however, low-risk and WADA-legal, and its best-supported uses (hepatitis B response, vaccine
immunogenicity in the elderly) are real. A doctor-handout candidate for immune-restoration *if* a specific indication
arises — not a general "recovery" peptide.

---

## 1. Identity & Mechanism

### 1.1 What Tα1 is
A 28-amino-acid, Nα-acetylated peptide (Ac-SDAAVDTSSEITTKDLKEKKEVVEEAEN; MW ~3108 Da) produced by cleavage of the
precursor prothymosin alpha (by legumain/asparaginyl endopeptidase), originally isolated from thymic tissue
`[in_vitro: Liu 2013, PMID 24288480]/[mechanism_review: Dominari 2020, PMID 33362999]`.

### 1.2 Mechanism — immune rebalancing, not blunt stimulation
Tα1 engages Toll-like receptors on dendritic cells and monocytes/macrophages, driving DC maturation via
MyD88 / p38-MAPK / NF-κB toward a **Th1-polarized** program (IL-12) `[animal/in_vitro: Romani 2004, PMID 14982877]`;
the specific receptors implicated (notably **TLR9 and TLR2**, with TLR3/4/7) are identified in the synthesis reviews
`[mechanism_review: Tao 2023, PMID 37110771]`.
Critically, the same TLR9 + type-I-IFN signaling co-activates the **IDO/tryptophan-catabolism** axis (IL-10,
regulatory T cells) `[animal/in_vitro: Romani 2006, PMID 16741252]` — so Tα1 simultaneously restores exhausted
T-cell/NK function AND restrains excess inflammation. This "rebalancing" is the mechanistic basis for using it in
immunosuppressed / post-infection states `[mechanism_review: Costantini 2019, PMID 31555601; Garaci 2000, PMID 11137613]`.
DC-priming and IDO mechanisms are best characterized in murine/in-vitro DC systems; human receptor-binding kinetics
are less directly resolved.

---

## 2. Human Clinical Evidence (by indication)

### 2.1 Sepsis — the efficacy story SHIFTED (FIRST-CLASS CAVEAT, see §4)
- **ETASS (Crit Care 2013, PMID 23327199), n=361, single-blind, 6 Chinese ICUs:** 28-day mortality 26.0% vs 35.0% —
  borderline (RR 0.74, 95% CI 0.54–1.02; log-rank p=0.049). `[rct]`
- **TESTS (BMJ 2025, PMID 39814420), n=1,089, DOUBLE-BLIND placebo-controlled phase 3, 22 Chinese centres:**
  28-day mortality 23.4% vs 24.1% — **NEGATIVE (HR 0.99, 95% CI 0.77–1.27, p=0.93)**; subgroups exploratory/inconsistent.
  `[rct]` — the largest, highest-quality trial, and it is null.
- **Meta-analysis (Front Cell Infect Microbiol 2025, PMID 40969554), 11 RCTs, n=1,927:** pooled OR 0.73 (0.59–0.90) —
  **but driven by small single-center trials**; high-quality/multicenter subgroup OR 0.86 (0.68–1.08, **NS**). `[meta_analysis]`

### 2.2 COVID-19 (moderate–severe)
- **RCT (Indian J Crit Care Med 2022, PMID 36042753), n=105, double-blind:** mortality 11.1% vs 38.5% placebo
  (the **severe subgroup**; the trial mixed 40 severe + 65 moderate) — small/underpowered. `[rct]`
- **Liu 2020 (Clin Infect Dis, PMID 32442287), Wuhan, retrospective:** severe-COVID mortality 11.1% vs 30.0% (p=0.044) —
  `[cohort]`, confounded; later cohorts inconsistent.
- **Meta-analysis (Inflammopharmacology 2023, PMID 37845598), 8 studies:** RR 0.59 (0.37–0.93) — heterogeneous, mostly
  observational/small-RCT. `[meta_analysis]`

### 2.3 Chronic hepatitis B (the historical approved indication)
- **Meta (Aliment Pharmacol Ther 2001, PMID 11736720), 5 RCTs n=353:** virological response NS at end-of-treatment,
  significant only at **12 months post-treatment** (OR 2.67, 1.25–5.68) — a **delayed/accumulating** effect. `[meta_analysis]`
- **vs interferon-α (Antiviral Res 2008, PMID 18078676), 4 RCTs n=199:** Tα1 superior at 6 mo post-treatment
  (OR 3.71, 2.05–6.71), better tolerated. `[meta_analysis]` (Pre-modern-antiviral era; endpoint is virological, not hard outcome.)

### 2.4 Vaccine adjuvant / cancer adjunct
- **Elderly influenza vaccine (J Am Geriatr Soc 1989, PMID 2642497), n=90 randomized (85 analyzed) RCT:** higher antibody response at 6 wk
  (p=0.023), strongest in the oldest. `[rct]` (Immunogenicity endpoint, not clinical influenza.)
- **Post-resection HBV-HCC (Medicine 2021, DOI 10.1097/MD.0000000000025749):** 5-yr OS 55.5% vs 47.2% — but
  **retrospective propensity-matched cohort**, confounding-prone. `[cohort]`

### 2.5 General post-illness recovery / deconditioning in healthy adults
- **NO ADMISSIBLE PRIMARY FOUND** — no RCT of Tα1 for general recovery/deconditioning/fatigue in otherwise-healthy
  adults (verified absence). This is the operator's goal, and it has no direct randomized support.

---

## 3. Safety, Contraindications, Monitoring

- **Tolerability is excellent.** Across >2,000 patients drug-related AEs were <1% with no clinically significant
  attributable reactions `[regulatory/vendor_label: Zadaxin PI]`; **ETASS reported no Tα1-related SAE and no AE
  discontinuations** `[rct: PMID 23327199]`; **TESTS found safety comparable to placebo** in n≈1,089 `[rct: PMID 39814420]`.
- **Common AE:** mild/infrequent **injection-site reactions**. Rare: transient muscle atrophy, polyarthralgia with hand
  edema, rash (qualitative, label) `[regulatory/vendor_label]`.
- **Contraindications/cautions:** hypersensitivity; **avoid in deliberate immunosuppression (organ-transplant recipients)**
  unless benefit clearly outweighs risk (its immune-enhancing action opposes intended immunosuppression); pregnancy
  Category C `[regulatory/vendor_label: Zadaxin PI]`. Theoretical autoimmune-flare caution (low-grade — not seen in the
  large pooled experience, but that rests on review/label tier, not an autoimmune-population RCT).
- **Interactions:** not fully evaluated; caution with other immunomodulators/immunosuppressants; do not physically mix.
- **Monitoring:** no mandatory lab regimen in the label; ETASS tracked routine labs without Tα1-attributable
  abnormalities. Stop on hypersensitivity/intolerance.
- **Anti-doping:** **NOT explicitly on the WADA Prohibited List** (its mechanism doesn't trigger the S2 growth-factor
  criteria) — **contrast thymosin BETA-4 / TB-500, which IS banned.** Catch-all caveat: re-verify the current annual list. `[regulatory: WADA list]`

---

## 4. The Two First-Class Caveats

### 4.1 The efficacy story shifted (the headline)
Tα1's most-studied acute indication is sepsis, and the evidence there **moved against it** in 2025: the largest,
double-blind, multicenter trial (TESTS, n=1,089) is **null** (HR 0.99), and the contemporaneous positive meta-analysis
is a **small-single-center-trial artifact** (the benefit disappears in the high-quality subgroup). A wiki entry written
a year earlier would have over-sold sepsis efficacy. The durable positives are narrower: hepatitis-B virological
response (delayed) and vaccine immunogenicity in the elderly.

### 4.2 Goal-fit gap
The operator's goal is general post-illness immune restoration / recovery. **No RCT tests that.** Tα1's evidence is in
specific disease populations (sepsis, COVID, hepatitis, vaccinees), not healthy-adult recovery. Using it for "recovery"
is mechanism-plausible (it restores exhausted immunity) but **clinically unproven in that use** → effectively tier D
for the goal, even though the compound is tier B for its studied indications.

---

## 5. Pharmacokinetics & Dosing

- **Dosing by indication:** chronic hepatitis B — **1.6 mg SC twice weekly** (40 µg/kg if <40 kg), 6–12 mo
  `[regulatory: Zadaxin PI]`; sepsis (ETASS) — 1.6 mg SC twice daily ×5 d then once daily ×2 d `[rct: PMID 23327199]`;
  COVID pilots — 1.6 mg SC daily ×7 d.
- **Human PK (Zadaxin PI):** Tmax ~2 h; **half-life ~2 h**; dose-proportional Cmax/AUC; returns to baseline by 24 h;
  no accumulation; urinary excretion 31–60% `[regulatory]`. (Volume of distribution: **NO ADMISSIBLE PRIMARY FOUND** —
  the commonly-cited ~5–8 L is not in the verifiable label; absolute SC bioavailability not stated.)
- **Administration:** **SC only (not IV)**; reconstitute lyophilized powder with 1.0 mL Sterile Water → 1.6 mg/mL,
  use immediately; store 2–8 °C `[regulatory]`.

---

## 6. Regulatory, Sourcing, Layers

- **Regulatory:** **NOT FDA-approved** (US) for any indication; approved in **~30+ countries** (China principal market;
  registered in Italy as an influenza-vaccine enhancer per the sponsor's filings) for chronic hepatitis B/C, cancer
  adjuvant, immune/vaccine enhancement `[regulatory: SciClone SEC filings — VERIFIED:partial]`. Holds US FDA **orphan
  designations** (hep B, HCC, melanoma, DiGeorge — designation ≠ approval). **Removed from US 503A Category 2 effective
  Sept 27, 2024** (nomination withdrawn); FDA proposed against 503A inclusion at the Dec 2024 PCAC `[regulatory: FDA 503A actions]`.
- **Sourcing:** international Rx as branded Zadaxin; US access via compounding (now legally contested post-2024) and a
  large gray market (vendor `vendor_label`/`anecdote` — inadmissible for clinical claims).
- **Prescribing-practice & non-English:** the only admissible protocol-tier source is the **2025 Chinese Expert
  Consensus** (Infect Microb Dis, DOI 10.1097/IM9.0000000000000176) — no admissible Western practitioner protocol; the
  circulating "1.6 mg twice weekly" off-label figure is just the hepatitis dose repurposed. The RCT base is heavily
  **Chinese-authored** (in English-language international journals — citable without translation). See the two layers.

---

## 7. Bottom line for the operator

Tα1 is **low-risk, WADA-legal, and a real approved drug abroad** — a genuinely better-behaved peptide than most in this
class. But its evidence is **indication-specific and recently weakened** (the best sepsis trial is null), and there is
**no randomized evidence for the operator's actual goal** (general recovery/immune restoration in a healthy adult). It
belongs on the **doctor-handout queue** as an immune-restoration option *if a specific clinical indication emerges*
(e.g., documented immune deficit, hepatitis), discussed at the July-2026 visit — not adopted as a general "recovery"
peptide on mechanism alone.
