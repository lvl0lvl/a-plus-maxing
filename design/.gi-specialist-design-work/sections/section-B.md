# Section B — GI Compounds: Evidence, Safety, Regulatory, Prescribing

Goal-agnostic library knowledge for the `gi-specialist` agent. Each claim carries exactly one
inline type-tag. Effect sizes are reported where the cited primary supplies them. This section
does NOT personalize for any operator.

Conventions: `[N, tag]` cites bibliography entry N with its dominant evidence type. Numeric claims
never rest on `vendor_label` or `anecdote_aggregate`. Animal/in-vitro numerics carry
`[population-mismatch: <species>]`. Route mismatches carry `[route-extrapolation]`.

---

## B-1 Probiotics (incl. PROPATRIA safety signal + immunocompromised contraindication)

**What it is.** Live micro-organisms (commonly *Lactobacillus*, *Bifidobacterium*, *Saccharomyces
boulardii* species, or defined multi-strain blends such as the 8-strain VSL#3 formulation) that,
when administered in adequate amounts, are claimed to confer a health benefit. In the US, probiotics
are sold as **dietary supplements** (no premarket efficacy review) unless marketed as a drug or
medical food `[10, regulatory]`.

**Cardinal principle — strain- and indication-specificity.** Efficacy demonstrated for one strain
in one indication does NOT transfer to other strains, blends, or indications. The 2020 AGA technical
review screened 1617 abstracts and included 55 RCTs in 5301 patients; those 55 trials tested **44
different species/strains or combinations**, so for the majority of probiotics the entire evidence
base is a single trial `[1, meta_analysis]`. Class membership ("it's a probiotic") is therefore not
evidence of effect for any given product.

**Strongest-evidence indications (with effect sizes):**

- **Antibiotic-associated diarrhea (AAD), prevention.** Pooled RR **0.62 (95% CI 0.51–0.74)** across
  36 studies / 9312 participants — a ~38% relative reduction `[2, meta_analysis]`. A separate larger
  pooled analysis (Hempel 2012, JAMA) reports a concordant RR **0.58 (95% CI 0.50–0.68)** across
  ~11,811 participants `[2b, meta_analysis]`.
- ***Clostridioides difficile*-associated diarrhea (CDAD), prevention.** 2017 Cochrane review: RR
  **0.36 (95% CI 0.26–0.51)** across 23 RCTs / 4213 participants, moderate-certainty evidence; in
  absolute terms ~85 fewer CDAD episodes per 1000 high-risk patients (NNT ≈ 12) `[3, meta_analysis]`.
  Benefit concentrated in patients at high baseline CDAD risk.
- **Chronic pouchitis, maintenance of remission (VSL#3).** In the Gionchetti maintenance RCT, 15%
  (3/20) of the VSL#3 arm relapsed within 9 months vs **100% (20/20)** of placebo `[4, rct]`; pooled
  across pouchitis maintenance trials the RR of relapse was ~**0.17–0.18** `[5, meta_analysis]`.
  This is the single strongest probiotic indication and is strain- AND formulation-specific.
- **Acute infectious diarrhea / some IBS** — historically cited but downgraded by recent guidelines
  (below); IBS evidence is heterogeneous and strain-dependent, not a class effect `[1, meta_analysis]`.

**2020 AGA / 2021 ACG guidance (practitioner_protocol — prescribing convention, NOT efficacy).**
The 2020 AGA clinical practice guideline recommends probiotics ONLY in three narrow contexts —
prevention of *C. difficile* infection in adults/children on antibiotics, maintenance of remission
in pouchitis (specific multi-strain blends), and NEC prevention in preterm <37-week / low-birth-weight
infants — and explicitly recommends **against** routine probiotic use for most adult GI conditions
including IBS and acute infectious gastroenteritis, citing very-low-certainty evidence
`[6, practitioner_protocol]`. The 2021 ACG IBS guideline likewise recommends **against** probiotics
for global IBS symptoms (component heterogeneity, lack of FDA-endpoint evaluation, inconsistent
results) `[7, practitioner_protocol]`.

### SAFETY SIGNAL — PROPATRIA (medium+ risk in critically ill)

The PROPATRIA trial (Besselink 2008, *Lancet*) randomized 298 patients with **predicted severe acute
pancreatitis** (APACHE-II ≥8, Imrie ≥3, or CRP >150 mg/L) to an enteral multispecies probiotic vs
placebo for 28 days `[8, rct]`. Findings:

- Probiotics did **not** reduce infectious complications: 46/152 (30%) vs 41/144 (28%), RR **1.06
  (95% CI 0.75–1.51)** `[8, rct]`.
- **Mortality was higher in the probiotic arm: 24/152 (16%) vs 9/144 (6%), RR 2.53 (95% CI
  1.22–5.25)** `[8, rct]`.
- **Bowel ischaemia** occurred in 9 probiotic patients (8 fatal) vs **0** in placebo (p=0.004)
  `[8, rct]`. The authors concluded probiotic prophylaxis should NOT be administered to this
  population. (The Lancet later issued an Expression of Concern about trial conduct, but the safety
  conclusion against use in predicted-severe pancreatitis stands `[9, regulatory]`.)

**Immunocompromised / critically ill — bacteremia & fungemia.** Probiotic organisms can translocate
and cause invasive infection. Case series document *Saccharomyces cerevisiae* var. *boulardii*
fungemia in ICU patients on enteral *S. boulardii* probiotics: a 7-patient series in intubated,
enterally-fed ICU patients with central venous catheters on broad-spectrum antibiotics; across the
pooled literature **~93% had a CVC and ~88% had received broad-spectrum antimicrobials**, with
fungemia detected a median ~10 days after probiotic start `[11, cohort]`. Management = stop the
probiotic, remove the CVC, and treat with an echinocandin or amphotericin-based antifungal
`[11, cohort]`.

**Risk tier.** `low` in healthy immunocompetent adults; **`medium`** (escalating toward `high`) in
the critically ill, predicted-severe acute pancreatitis, immunocompromised, or central-line patients.
Safety boundary stated explicitly: most probiotics in healthy adults are low-risk; the risk concentrates
in critical illness, compromised gut-barrier states, indwelling catheters, and immunosuppression.

---

## B-2 Prebiotics / fiber

**What it is.** Non-digestible substrates fermented by colonic microbiota (inulin, fructo-
oligosaccharides [FOS], galacto-oligosaccharides [GOS]) plus soluble bulking/viscous fibers (psyllium/
ispaghula, partially-hydrolyzed guar gum [PHGG]). Sold OTC as foods/supplements `[10, regulatory]`.

**Evidence (with effect sizes):**

- **Psyllium (soluble fiber), IBS global symptoms.** RR of persistent symptoms **0.78 (95% CI
  0.63–0.96)** across ~591 IBS patients; soluble (not insoluble/wheat-bran) fiber is the effective
  type `[12, meta_analysis]`. Soluble-fiber-vs-placebo benefit in IBS RR ~**0.86 (95% CI 0.80–0.94)**
  `[12, meta_analysis]`.
- **Fiber for chronic constipation.** In pooled constipation RCTs, ~66% (311/473) responded to fiber
  vs 41% (134/329) to control; psyllium specifically effective at doses **>10 g/d for ≥4 weeks**
  `[13, meta_analysis]`.
- **PHGG, IBS.** A 12-week double-blind RCT (6 g/d) improved bloating and gas scores vs placebo (effect
  persisting ≥4 weeks post-treatment) but did not move other IBS symptom or QoL scores; no significant
  side effects `[14, rct]`. PHGG 5 g/d for 4 weeks reduced laxative use in long-term-care residents vs
  placebo `[15, rct]`.

**Fermentation-vs-FODMAP tension.** Inulin/FOS/GOS are themselves **FODMAPs** — fermentable substrates
that produce gas. The benefit (microbiome substrate, bulking, bifidogenic effect) and the principal
adverse effect (gas, bloating, distension, flatulence) share the same mechanism, so effects are
**dose-dependent**: low doses tolerated, high doses provoke symptoms, and in FODMAP-sensitive IBS the
same prebiotic can worsen symptoms `[14, rct]`. Soluble, less-rapidly-fermented fibers (psyllium, PHGG)
are better tolerated than rapidly-fermented inulin/FOS at equal dose.

**Risk tier.** `low`. Adverse effects are GI-functional (gas/bloating/cramping), dose-dependent and
self-limiting; no monitoring biomarker required for healthy adults. Caution: bulk fibers need adequate
fluid; rare esophageal/bowel obstruction with dysphagia or strictures (bulk-former labeling warning)
`[10, regulatory]`.

---

## B-3 Digestive enzymes (PERT vs OTC; lactase)

**Pancreatic enzyme replacement therapy (PERT) — Rx, strong evidence for a defined indication.**
PERT (pancrelipase: lipase/amylase/protease) is an **FDA-approved prescription drug** for **exocrine
pancreatic insufficiency (EPI)** from chronic pancreatitis, cystic fibrosis, pancreatic
cancer/resection, or duct obstruction `[16, regulatory]`. Meta-analysis of 7 RCTs / 282 patients:
PERT increased the **coefficient of fat absorption (CFA)** vs both baseline and placebo
`[17, meta_analysis]`. PERT is dose-individualized (lipase units per meal/snack), taken **with**
meals; this is a treatment for a diagnosed deficiency, NOT a general digestive aid.

**OTC "digestive enzyme" supplements — weak/insufficient evidence.** Broad-spectrum OTC enzyme blends
(marketed for bloating, "food intolerance," general digestion in people WITHOUT EPI) lack RCT support
for those claims; efficacy demonstrated for PERT in EPI does not transfer to OTC blends in the general
population (class-membership-as-efficacy error) `[1, meta_analysis]` `[17, meta_analysis]`. Risk tier
`low`, but the evidence/claim mismatch is the salient issue, not toxicity.

**Lactase (β-galactosidase) — OTC, good evidence for a specific indication.** Exogenous lactase taken
with lactose-containing food reduces breath-hydrogen and symptoms in lactose-intolerant subjects: a
crossover placebo-controlled RCT showed cumulative breath-hydrogen reduced ~**55%** over 180 min with
lactase vs placebo, with improved symptom scores `[18, rct]`. Indication-specific (lactose intolerance
/ primary hypolactasia), not a general digestive aid. Risk tier `low`.

---

## B-4 Betaine HCl / stomach-acid support

**What it is.** Betaine hydrochloride (often with pepsin), a short-acting OTC acidifying agent marketed
for "low stomach acid" / functional hypochlorhydria `[10, regulatory]`. Distinct from betaine anhydrous
(a homocysteine-lowering Rx for homocystinuria) — a documented look-alike medication-error hazard
`[19, regulatory]`.

**Evidence — weak.** The strongest human data is a mechanistic pharmacology study: in healthy
volunteers with **rabeprazole-induced** (pharmacologic) hypochlorhydria, a 1500 mg betaine HCl dose
lowered gastric pH by ~**4.5 units**, reaching pH <3 in a mean **6.3 min**, but the reacidification
was transient (pH <3 lasting only ~**73 min**) `[20, rct]`. This demonstrates a transient
pharmacodynamic effect in drug-induced low acid — it does NOT establish that supplementation treats
symptoms in people with normal acid or improves clinical outcomes in spontaneous hypochlorhydria, where
evidence remains limited `[21, mechanism_review]`.

**Risk tier — `medium`** (low population evidence + plausible mucosal-irritation harm).
- *Adverse effects (literature):* heartburn/epigastric burning, GI irritation; acidifying agents are
  inadvisable with active or history of peptic ulcer disease, gastritis, or GERD `[21, mechanism_review]`.
- *Contraindications:* concurrent peptic ulcer / erosive gastritis / GERD; concurrent NSAID or
  corticosteroid use (additive mucosal risk); known autoimmune gastritis pending workup.
- *Monitoring:* clinical sign — new or worsening epigastric pain/heartburn; if a true acid-related
  diagnosis is suspected, gastric pH / endoscopic evaluation belongs with a clinician, not self-titration.
- *Stopping criteria:* any new epigastric pain, heartburn, melena, or GI bleeding → stop immediately
  and escalate to a clinician.

---

## B-5 Gut-barrier agents (glutamine, zinc-carnosine, colostrum, SBI)

Mostly limited/mechanistic; a few small human RCTs exist. Mechanism (barrier/permeability) must be kept
distinct from clinical outcome.

- **L-glutamine.** Strongest human signal: a randomized placebo-controlled trial in **post-infectious
  IBS-D with increased intestinal permeability** gave glutamine 5 g three-times-daily for 8 weeks; the
  primary endpoint was ≥50-point reduction on IBS-SS, and glutamine reduced symptoms and restored
  lactulose:mannitol permeability vs placebo in this defined subgroup `[22, rct]`. Effect is shown in a
  **permeability-defined subgroup**, not unselected populations; broader gut-barrier claims rest on
  animal/mechanistic data. Risk tier `low` in healthy adults at these doses.

- **Zinc-L-carnosine (polaprezinc).** A randomized crossover trial in **n=10 healthy volunteers**:
  indomethacin (50 mg TID ×5 d) caused a ~**threefold** rise in gut permeability (lactulose:rhamnose
  0.35→0.88) on placebo, which was **prevented** by zinc-carnosine 37.5 mg BID `[23, rct]`. Small n;
  permeability endpoint, not clinical outcome. Polaprezinc is a registered **drug for gastric ulcer in
  Japan/Korea**, an OTC supplement elsewhere `[10, regulatory]`. Risk tier `low` (zinc-related: chronic
  high-dose zinc can cause copper deficiency — relevant only at supraphysiologic total zinc intake).

- **Colostrum (bovine).** Human RCT evidence is limited and indication-scattered (athlete gut
  permeability, infectious diarrhea); evidence maturity is low and largely not GI-outcome-confirmatory.
  Marketed OTC `[10, regulatory]`. Treat as `experimental` for general gut-barrier claims (see risk
  scaffold below).

- **Serum-derived bovine immunoglobulin (SBI).** Regulated as a **prescription medical food** (managed
  under clinician supervision), NOT a routine OTC supplement `[24, regulatory]`. An RCT in IBS-D tested
  SBI 5 g/day, 10 g/day, vs placebo ×6 weeks, reporting improved GI symptom scores `[25, rct]`; a small
  pediatric d-IBS RCT (SBI 5 g BID vs placebo) tested safety/tolerability `[26, rct]`. Evidence is early
  and from a narrow sponsor-linked literature. Risk tier `low–medium` (bovine-protein source; contra in
  beef/dairy-protein allergy).

**Concentration-audit note.** Across B-5 the human RCT base is thin and several agents (zinc-carnosine,
SBI) rest on single small trials or a sponsor-linked cluster — claims carry **low certainty** and should
not be stated as established clinical efficacy. See Self-check for the single-cluster flag on SBI.

---

## B-6 Motility / symptom agents (peppermint oil, ginger, prokinetics)

- **Enteric-coated peppermint oil (IBS) — decent meta-analytic evidence.** Khanna meta-analysis: global
  IBS symptom improvement RR **2.23 (95% CI 1.78–2.81)** (5 studies / 392 patients) and abdominal-pain
  improvement RR **2.14 (95% CI 1.64–2.79)** (5 studies / 357 patients) vs placebo `[27, meta_analysis]`.
  A larger 2022 meta-analysis (12 RCTs) found global-symptom RR **2.39 (95% CI 1.93–2.97)** and
  abdominal-pain RR **1.78 (95% CI 1.43–2.20)** `[28, meta_analysis]`. ACG conditionally recommends
  peppermint for global IBS symptoms (low-quality evidence) `[7, practitioner_protocol]`. Adverse
  effects mild/transient — chiefly heartburn/GERD (relax lower-esophageal sphincter); enteric coating
  mitigates. Risk tier `low`; caution in GERD and with hiatal hernia.

- **Ginger — nausea / gastric emptying.** Pregnancy NVP: meta-analysis of 12 RCTs / 1278 women showed
  ginger improved nausea vs placebo but did NOT significantly reduce vomiting episodes; subgroups
  favored **<1500 mg/day** `[29, meta_analysis]`. Chemotherapy-induced nausea: systematic review of 23
  RCTs found ≤1 g/day for >4 days reduced acute vomiting vs control `[30, meta_analysis]`. Gingerols
  accelerate delayed gastric emptying `[31, animal]` `[population-mismatch: rodent/in-vitro cisplatin
  model]`. Risk tier `low`; standard cautions: high doses and bleeding-risk/anticoagulant interaction
  noted at supratherapeutic intake.

- **Prokinetics — mostly Rx (boundary).** True prokinetics (metoclopramide, domperidone, prucalopride,
  erythromycin-as-prokinetic) are **prescription drugs** for gastroparesis/chronic constipation and
  carry meaningful risks (metoclopramide → tardive dyskinesia / FDA boxed warning; domperidone →
  QT/cardiac, not FDA-approved in the US) `[32, regulatory]`. **Boundary flag for the agent:** these are
  clinician-managed Rx agents; the library/`compounds` class covers OTC/supplement digestive aids — it
  must NOT recommend or dose prescription prokinetics, only name them and route the operator to a
  clinician.

---

## Prescribing-practice conventions (consensus dosing/cycling — explicitly NOT-efficacy)

These are practitioner-convention/regulatory dosing references for the agent's `compounds` scaffold.
They describe HOW clinicians/labels administer these agents; they are NOT efficacy claims and must not
be cited as evidence of benefit.

- **Probiotics:** typically 1–50 billion CFU/day; product/strain-specific; for CDAD prevention started
  with the antibiotic course and continued through it `[6, practitioner_protocol]`. Refrigeration/
  viability per label.
- **Psyllium:** titrate up to >10 g/day with adequate fluid; ≥4-week trial before judging response;
  separate from medications by ~2 h (binding) `[13, practitioner_protocol]`.
- **Inulin/FOS/GOS:** start low (2–5 g/day), titrate to tolerance to limit gas `[14, practitioner_protocol]`.
- **PERT:** Rx, dose in lipase units per meal/snack, individualized, taken **with** food, do not
  crush enteric beads `[16, regulatory]`.
- **Lactase:** taken with the first bite of lactose-containing food; dose to lactose load `[18, practitioner_protocol]`.
- **Peppermint oil:** enteric-coated, ~180–225 mg TID before meals, 4-week trial `[7, practitioner_protocol]`.
- **Ginger:** ≤1–1.5 g/day for nausea `[29, practitioner_protocol]`.
- **Cycling:** no robust evidence base mandates cycling for any of these families; "cycling" claims are
  convention/marketing, not efficacy `[21, mechanism_review]`.

---

## Risk-tier table

| Compound family | risk_tier | Key contraindication | Monitoring (biomarker / clinical sign) | Stopping criterion |
|---|---|---|---|---|
| Probiotics (healthy adults) | low | none routine | none required | new GI infection signs |
| Probiotics (critically ill / immunocompromised / CVC / predicted-severe pancreatitis) | **medium→high** | critical illness, immunosuppression, central line, predicted-severe acute pancreatitis | new fever/sepsis, blood cultures (bacteremia/fungemia), signs of bowel ischaemia | any sepsis sign, positive culture, abdominal ischaemia → stop, pull line, escalate |
| Prebiotics / fiber | low | dysphagia, GI stricture/obstruction (bulk fibers) | clinical: bloating/distension severity | obstructive symptoms, severe distension |
| PERT (Rx) | low (with EPI) | fibrosing colonopathy risk at very high CF doses; pork allergy | nutritional status, steatorrhea, weight | new abdominal pain at high dose (colonopathy) |
| OTC digestive enzymes | low | — | clinical (no validated benefit to monitor) | persistent symptoms → reassess diagnosis |
| Lactase | low | — | clinical: residual lactose symptoms | n/a |
| Betaine HCl | **medium** | peptic ulcer / gastritis / GERD; NSAID/steroid co-use | clinical: new/worsening epigastric pain or heartburn | any epigastric pain, heartburn, melena, GI bleed → stop, escalate |
| Glutamine | low | — | clinical: symptom/permeability response | n/a |
| Zinc-carnosine | low | chronic high total-zinc intake → copper deficiency | serum copper only if chronic high-dose | signs of copper deficiency at chronic high dose |
| Colostrum | **experimental** | bovine-protein / dairy allergy | clinical (no validated GI biomarker) | allergic reaction; no benefit after trial |
| SBI (Rx medical food) | low–medium | beef/dairy-protein allergy | clinician-supervised | allergic reaction; clinician discretion |
| Peppermint oil | low | GERD, hiatal hernia | clinical: heartburn | worsening reflux |
| Ginger | low | high-dose + anticoagulant (bleeding) | clinical | bleeding signs at high dose |
| Prokinetics (Rx — boundary) | **clinician-only** | cardiac/QT (domperidone); neuro (metoclopramide) | ECG/neuro per drug | per prescriber |

---

## Key claims for the agent design

1. **Probiotics are strain- AND indication-specific; class membership ≠ efficacy.** The agent must
   never generalize one strain's trial to other products/indications `[1, meta_analysis]`.
2. **The strongest probiotic indications are AAD prevention (RR ~0.62), CDAD prevention (RR 0.36), and
   pouchitis maintenance (VSL#3, relapse RR ~0.17)** — narrow, not "good for gut health"
   `[2,3,4,5, meta_analysis/rct]`.
3. **PROPATRIA is the canonical safety landmine:** probiotics increased mortality (16% vs 6%, RR 2.53)
   and caused fatal bowel ischaemia in predicted-severe acute pancreatitis `[8, rct]`. The agent must
   carry a hard contraindication for critically ill / immunocompromised / central-line / severe-acute-
   pancreatitis contexts and surface bacteremia/fungemia risk `[11, cohort]`.
4. **2020 AGA + 2021 ACG recommend probiotics for only a few narrow indications and against routine IBS
   use** — the agent's defaults should mirror guideline restraint, not supplement-marketing optimism
   `[6,7, practitioner_protocol]`.
5. **Prebiotic benefit and gas/bloating share one mechanism (fermentation); dosing is the lever, and
   inulin/FOS/GOS are FODMAPs** that can worsen FODMAP-sensitive IBS `[14, rct]`.
6. **PERT (Rx, EPI) is strong evidence for a diagnosed deficiency and must not be conflated with OTC
   "digestive enzyme" blends** (weak/insufficient evidence for general use); lactase is the well-
   supported OTC enzyme for lactose intolerance `[17,18, meta_analysis/rct]`.
7. **Betaine HCl has weak human evidence and a real mucosal-irritation safety profile** → `medium` tier
   with PUD/GERD/NSAID contraindications and stop-on-epigastric-pain criteria `[20, rct]` `[21, mechanism_review]`.
8. **Gut-barrier agents (glutamine, zinc-carnosine, colostrum, SBI) are mostly mechanistic/small-RCT;
   permeability ≠ clinical outcome.** Glutamine has a permeability-defined-subgroup RCT; zinc-carnosine
   a single n=10 crossover; SBI a sponsor-linked cluster `[22,23,25, rct]`. State low certainty.
9. **Peppermint oil has the best symptom-agent evidence in IBS (global RR ~2.2–2.4)**; ginger helps
   nausea (not vomiting in pregnancy); prokinetics are Rx — name and route, never dose `[27,28,29, meta_analysis]`.

---

## Bibliography

1. Su GL, et al. (2020). *AGA Technical Review on the Role of Probiotics in the Management of
   Gastrointestinal Disorders.* Gastroenterology. PMC8018518.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC8018518/ — meta_analysis
2. Liao W, Chen C, Wen T, Zhao Q (2020). *Probiotics for the Prevention of Antibiotic-associated
   Diarrhea in Adults: A Meta-Analysis of Randomized Placebo-Controlled Trials* (36 studies, 9312
   participants; RR 0.62, 95% CI 0.51–0.74; ~38% reduction). J Clin Gastroenterol (online Nov 2020;
   issue dated 2021). PMC8183490. https://pmc.ncbi.nlm.nih.gov/articles/PMC8183490/ — meta_analysis
2b. Hempel S, et al. (2012). *Probiotics for the prevention and treatment of antibiotic-associated
   diarrhea: a systematic review and meta-analysis* (RR 0.58, 95% CI 0.50–0.68; ~11,811 participants).
   JAMA. PMID 22570464. https://pubmed.ncbi.nlm.nih.gov/22570464/ — meta_analysis
3. Goldenberg JZ, et al. (2017). *Probiotics for the prevention of Clostridium difficile-associated
   diarrhea in adults and children.* Cochrane Database Syst Rev. CD006095.pub4.
   https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD006095.pub4/full — meta_analysis
4. Gionchetti P, et al. (2000). *Oral bacteriotherapy as maintenance treatment in patients with chronic
   pouchitis: a double-blind, placebo-controlled trial.* Gastroenterology. PMID 10930365.
   https://pubmed.ncbi.nlm.nih.gov/10930365/ — rct
5. Holubar SD / meta-analysis of probiotics in pouchitis maintenance (relapse RR ~0.17, 95% CI
   0.10–0.30). Effect of probiotics in IBD/pouchitis: meta-analysis of RCTs. PMID 24280877.
   https://pubmed.ncbi.nlm.nih.gov/24280877/ — meta_analysis
6. Su GL, et al. (2020). *AGA Clinical Practice Guidelines on the Role of Probiotics in the Management
   of Gastrointestinal Disorders.* Gastroenterology. PMID 32531291.
   https://www.gastrojournal.org/article/S0016-5085(20)34729-6/fulltext — practitioner_protocol
7. Lacy BE, et al. (2021). *ACG Clinical Guideline: Management of Irritable Bowel Syndrome.* Am J
   Gastroenterol. PMID 33315591. https://pubmed.ncbi.nlm.nih.gov/33315591/ — practitioner_protocol
8. Besselink MGH, et al. (2008). *Probiotic prophylaxis in predicted severe acute pancreatitis: a
   randomised, double-blind, placebo-controlled trial (PROPATRIA).* Lancet 371:651-659. PMID 18279948.
   https://pubmed.ncbi.nlm.nih.gov/18279948/ — rct
9. The Lancet Editors (2010). *Expression of concern — Probiotic prophylaxis in predicted severe acute
   pancreatitis.* Lancet. PMID 20226971. https://pubmed.ncbi.nlm.nih.gov/20226971/ — regulatory
10. US FDA. Dietary supplement regulatory framework (DSHEA; supplements not premarket-reviewed for
    efficacy) + bulk-laxative labeling. https://www.fda.gov/ — regulatory
11. Atıcı S / Cassone M, et al. *Saccharomyces cerevisiae var. boulardii fungemia following probiotic
    treatment* (ICU case series; ~93% CVC, ~88% broad-spectrum antibiotics). PMC5333505 / PMID 28794958.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC5333505/ — cohort
12. Moayyedi P / Ford AC, et al. (soluble-fiber & psyllium in IBS: RR 0.78, 95% CI 0.63–0.96; soluble
    fiber RR 0.86, 95% CI 0.80–0.94). Effect of fibre, antispasmodics, peppermint oil in IBS. PMID
    19008265. https://pubmed.ncbi.nlm.nih.gov/19008265/ — meta_analysis
13. Christodoulides S, et al. / fiber-for-chronic-constipation meta-analysis (66% vs 41% responders;
    psyllium >10 g/d ≥4 wk). PMC3544045 / updated PMC9535527.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC9535527/ — meta_analysis
14. Niv E, et al. (2016). *Randomized clinical study: partially hydrolyzed guar gum (PHGG) versus
    placebo in IBS* (6 g/d ×12 wk; bloating/gas improvement). PMC4744437.
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4744437/ — rct
15. PHGG in long-term-care constipation (5 g/d ×4 wk reduces laxative use). PMID 35297467 / PMC12275608.
    https://pubmed.ncbi.nlm.nih.gov/35297467/ — rct
16. US FDA. Pancrelipase (PERT) prescribing information — approved for exocrine pancreatic
    insufficiency. https://www.fda.gov/ — regulatory
17. de la Iglesia-García D, et al. (2017). *Efficacy and safety of pancreatic enzyme replacement
    therapy on exocrine pancreatic insufficiency: a meta-analysis* (7 RCTs, 282 pts; CFA increased).
    PMID 29212278 / PMC5706924. https://pubmed.ncbi.nlm.nih.gov/29212278/ — meta_analysis
18. Ianiro / Ojetti V, et al. *Effect of lactase on symptoms and hydrogen breath levels in lactose
    intolerance: crossover placebo-controlled study* (~55% breath-H2 reduction). PMID 33490624 /
    PMC7812489. https://pubmed.ncbi.nlm.nih.gov/33490624/ — rct
19. ISMP Medication Error Report Analysis: *Betaine Anhydrous Versus Betaine Hydrochloride: Look-Alike
    Generic Names.* PMC5396982. https://pmc.ncbi.nlm.nih.gov/articles/PMC5396982/ — regulatory
20. Yago MR, et al. (2013). *Gastric reacidification with betaine HCl in healthy volunteers with
    rabeprazole-induced hypochlorhydria* (pH ↓4.5 units; pH<3 in 6.3 min, lasting 73 min). PMID
    23980906. https://pubmed.ncbi.nlm.nih.gov/23980906/ — rct
21. Guilliams TG, Drake LE (2020). *Meal-Time Supplementation with Betaine HCl for Functional
    Hypochlorhydria: What is the Evidence?* PMID 32549862. https://pubmed.ncbi.nlm.nih.gov/32549862/
    — mechanism_review
22. Zhou Q, et al. (2019). *Randomised placebo-controlled trial of dietary glutamine supplements for
    postinfectious IBS* (glutamine 5 g TID ×8 wk; IBS-SS ≥50-pt responder; permeability restored).
    Gut 68(6):996-1002. PMID 30108163. https://pubmed.ncbi.nlm.nih.gov/30108163/ — rct
23. Mahmood A, et al. (2007). *Zinc carnosine, a health food supplement that stabilises small bowel
    integrity and stimulates gut repair processes* (n=10 crossover; indomethacin 3× permeability
    prevented by ZnC 37.5 mg BID). Gut. PMID 16777920 / PMC1856764.
    https://pubmed.ncbi.nlm.nih.gov/16777920/ — rct
24. US FDA. Serum-derived bovine immunoglobulin / protein isolate regulated as a prescription medical
    food. https://www.fda.gov/ — regulatory
25. Wilson D, et al. (2013). *Evaluation of serum-derived bovine immunoglobulin protein isolate in
    subjects with diarrhea-predominant IBS* (SBI 5 g/d, 10 g/d, vs placebo ×6 wk). PMID 24833942 /
    PMC4020402. https://pubmed.ncbi.nlm.nih.gov/24833942/ — rct
26. Serum-derived bovine immunoglobulin for children with d-IBS (SBI 5 g BID vs placebo ×3 wk pilot).
    PMID 30498390 / PMC6207257. https://pmc.ncbi.nlm.nih.gov/articles/PMC6207257/ — rct
27. Khanna R, et al. (2014). *Peppermint oil for the treatment of irritable bowel syndrome: a
    systematic review and meta-analysis* (global RR 2.23, 95% CI 1.78–2.81; pain RR 2.14, 95% CI
    1.64–2.79). PMID 24100754. https://pubmed.ncbi.nlm.nih.gov/24100754/ — meta_analysis
28. Ingrosso MR, et al. (2022). *Systematic review and meta-analysis: efficacy of peppermint oil in
    IBS* (12 RCTs; global RR 2.39; pain RR 1.78). PMID 35942669.
    https://pubmed.ncbi.nlm.nih.gov/35942669/ — meta_analysis
29. Viljoen E, et al. (2014). *A systematic review and meta-analysis of the effect and safety of ginger
    in pregnancy-associated nausea and vomiting* (12 RCTs, 1278 women; nausea ↓, vomiting NS; <1500
    mg/d). PMC3995184. https://pmc.ncbi.nlm.nih.gov/articles/PMC3995184/ — meta_analysis
30. Effects of ginger on chemotherapy-induced nausea/vomiting: systematic review of 23 RCTs (≤1 g/d
    >4 d ↓ acute vomiting). PMID 36501010 / PMC9739555. https://pubmed.ncbi.nlm.nih.gov/36501010/
    — meta_analysis
31. Gingerols accelerate cisplatin-delayed gastric emptying (mechanistic rodent/in-vitro model). Cited
    within PMC9739555. — animal
32. US FDA. Prokinetic prescribing labels — metoclopramide (boxed warning, tardive dyskinesia);
    domperidone (not FDA-approved, QT); prucalopride (Rx). https://www.fda.gov/ — regulatory

**Distinct admissible primaries (Tier 1/2): 25+** (entries 1–9, 2b, 11–18, 20, 22–23, 25–30 are RCTs,
meta-analyses, Cochrane reviews, society guidelines, or regulator documents; entry 31 animal/in-vitro
is flagged and grounds no human numeric).

---

## Self-check

- **Every numeric claim type-tagged:** Yes. All effect sizes (RR 0.62, 0.36, 0.17, 2.53, 2.23, 2.39,
  etc.), n's, doses, and percentages carry `rct`/`meta_analysis`/`cohort`/`regulatory` tags.
- **Animal/in-vitro numerics flagged:** The gingerol gastric-emptying claim `[31, animal]` carries
  `[population-mismatch: rodent/in-vitro cisplatin model]` and grounds no human numeric (qualitative
  only). No other animal numeric is asserted.
- **Route fidelity:** PROPATRIA dosing is enteral (matches); PERT/lactase/peppermint are oral (matches).
  No cross-route dose extrapolation made; no `[route-extrapolation]` tags needed. Betaine HCl pH data
  is from drug-induced (rabeprazole) hypochlorhydria, flagged in-text as a model limitation (population,
  not route).
- **No vendor_label / anecdote_aggregate grounds any number:** Confirmed — no such tags used for any
  numeric; all doses/effect sizes rest on RCT/meta/regulatory sources.
- **Single-lab/sponsor dominance surfaced:** SBI (B-5) flagged as a **sponsor-linked cluster** with low
  certainty (entries 24–26 share a narrow originator literature). VSL#3 pouchitis evidence noted as
  formulation-specific. Concentration-audit note placed first-class in B-5, not buried.
- **Risk-floor fields fillable for medium+ families:** Probiotics-in-critically-ill (`medium→high`),
  Betaine HCl (`medium`), Colostrum (`experimental`), SBI (`low–medium`), prokinetics (`clinician-only`)
  — each has adverse effects, contraindication, monitoring sign/biomarker, and stopping criterion in the
  risk-tier table and in-text. Low-risk families (most probiotics in healthy adults, fiber, lactase,
  glutamine, zinc-carnosine, peppermint, ginger) stated explicitly with their safety boundary.
- **Reasoning integrity:** mechanism (permeability, gastric pH, fermentation) kept distinct from human
  clinical outcome throughout; class-membership-as-efficacy explicitly rejected for probiotics and OTC
  enzymes.
- **Source count:** ≥8 distinct admissible primaries required; **25+ delivered** (Tier 1/2).

---

*Iteration note:* **iter-3** (ITER-1 = initial draft; judge HALT 91/100. ITER-2 fixed two critical
citation_fidelity findings: (1) the AAD "RR 0.62 / 9312" claim re-attributed from Hempel 2012 to its
actual source (entry 2, PMC8183490, the adults RCT meta-analysis; study count corrected 30→36), with
Hempel 2012's own concordant RR 0.58 / n≈11,811 added as entry 2b; (2) the Zhou glutamine RCT PMID
corrected from 30244201 (a comment/letter) to 30108163 (the primary trial).) **ITER-3** fixed one
major citation_fidelity finding: bibliography entry 2's falsified byline "Cai J, 2018" corrected — via
WebFetch of the PMC8183490 page itself — to the verified byline **Liao W, Chen C, Wen T, Zhao Q
(2020), J Clin Gastroenterol** (online Nov 2020, issue dated 2021). The RR 0.62 / 36-studies / 9312
figure and `meta_analysis` tag are unchanged (verified correct against the source). Post-fix grep
audits (iter-2 + iter-3) below.

---

## Post-fix grep audit

Mandatory terminal discipline for iter-2. For each corrected value: OLD (wrong, replaced) → NEW
(correct). Greps run case-insensitive across the whole section file AFTER correction.

### Correction 1 — AAD effect-size misattribution + study count
- OLD attribution: `Hempel 2012 (PMID 22570464)` as the source of `RR 0.62 / 9312 / "30 studies"`.
- NEW attribution: entry **2 = PMC8183490** (Liao W et al., adults RCT meta-analysis; byline corrected
  in iter-3 — see below — from the erroneous "Cai J, 2018" first used here) reports RR 0.62,
  95% CI 0.51–0.74, **36 studies**, 9312 participants. Hempel 2012 retained as entry **2b** for its
  OWN concordant figure (RR 0.58, 95% CI 0.50–0.68, n≈11,811).

```
$ grep -inE '30 studies' section-B.md
(no hits)
$ grep -inE 'hempel' section-B.md
32:  pooled analysis (Hempel 2012, JAMA) reports a concordant RR **0.58 (95% CI 0.50–0.68)** across
318:2b. Hempel S, et al. (2012). *Probiotics for the prevention and treatment of antibiotic-associated
$ grep -inE '9,?312' section-B.md
31:  36 studies / 9312 participants — a ~38% relative reduction `[2, meta_analysis]`. A separate larger
315:   A Meta-Analysis of Randomized Placebo-Controlled Trials* (36 studies, 9312 participants; RR 0.62,
$ grep -inE '0\.62' section-B.md
30:  ...Pooled RR **0.62 (95% CI 0.51–0.74)** across
284:  ...AAD prevention (RR ~0.62)...
315:  ...(36 studies, 9312 participants; RR 0.62,...
411:  ...All effect sizes (RR 0.62, 0.36, 0.17, 2.53, 2.23, 2.39, etc.)...
$ grep -inE 'PMC8183490' section-B.md
316:   95% CI 0.51–0.74; ~38% reduction). PMC8183490.
317:   https://pmc.ncbi.nlm.nih.gov/articles/PMC8183490/ — meta_analysis
```

Disposition of each hit:
- `30 studies` → **0 hits.** Resolved: corrected to "36 studies" at both line 31 (in-text) and line
  315 (bibliography), matching PMC8183490 ("thirty-six studies with 9312 participants").
- `Hempel` line 32 → **legitimately present.** Now grounds only RR 0.58 / n≈11,811, which IS Hempel
  2012's reported figure (verified against JAMA abstract). No longer attached to the 0.62/9312 claim.
- `Hempel` line 318 → **legitimately present.** Bibliography entry 2b, correctly labeled with Hempel's
  own numbers.
- `9312` lines 31 & 315 → **legitimately unchanged.** 9312 is the correct participant count for the
  0.62 claim and now sits with its actual source (entry 2, PMC8183490), not Hempel. Same metadata
  instance, correctly re-homed.
- `0.62` lines 30, 284, 315, 411 → **legitimately unchanged.** 0.62 is the correct RR from PMC8183490;
  all four hits (in-text claim, key-claims summary, bibliography, self-check) refer to the same
  correctly-attributed value. No hit attributes 0.62 to Hempel.
- `PMC8183490` lines 316–317 → **present as intended** (the new correct AAD source).

### Correction 2 — Zhou glutamine PMID (comment → primary trial)
- OLD value: `PMID 30244201` (a comment/letter "Efficacy of glutamine in postinfection IBS").
- NEW value: `PMID 30108163` (the primary RCT, Zhou et al. 2019, Gut 68(6):996-1002). The reported
  effect (glutamine 5 g TID ×8 wk; primary endpoint = proportion with ≥50-point IBS-SS reduction;
  permeability restored) matches the primary trial; `rct` tag retained (it is the RCT, not the comment).

```
$ grep -inE '30244201' section-B.md
(no hits)
$ grep -inE '30108163' section-B.md
374:    Gut 68(6):996-1002. PMID 30108163. https://pubmed.ncbi.nlm.nih.gov/30108163/ — rct
```

Disposition:
- `30244201` → **0 hits.** Fully removed; the wrong comment-PMID no longer appears anywhere.
- `30108163` line 374 → **present as intended.** Single occurrence, bibliography entry 22, `rct` tag
  preserved (correct — this PMID is the randomized trial).

**Audit result: PASS.** Both OLD wrong values (`30 studies`, `30244201`) return zero hits. Every
retained hit of a shared value (`0.62`, `9312`, `Hempel`) is dispositioned as either correctly re-homed
to its true source or legitimately unchanged. No number remains attached to a source that does not
report it. Iter-2 corrections complete.

### iter-3 — Bibliography entry 2 byline correction (falsified author/year)

Mandatory terminal discipline for iter-3. OLD → NEW:
- OLD (entry 2 byline): `Cai J, et al. (2018)` — falsified first-author + year (number/PMCID were correct).
- NEW (entry 2 byline, verified by WebFetch of the PMC8183490 article page itself):
  **Liao W, Chen C, Wen T, Zhao Q (2020)**, *J Clin Gastroenterol* (published online Nov 2020; issue
  dated 2021). RR 0.62 / 36 studies / 9312 participants and `meta_analysis` tag unchanged (re-verified
  correct against the source: "Pooled Relative Risk 0.62 (95% CI 0.51–0.74); 36 RCTs; 9,312 subjects").

```
$ grep -inE 'Cai|2018' section-B.md
442:major citation_fidelity finding: bibliography entry 2's falsified byline "Cai J, 2018" corrected — via
457:  in iter-3 — see below — from the erroneous "Cai J, 2018" first used here) reports RR 0.62,
$ grep -inE 'Liao' section-B.md
314:2. Liao W, Chen C, Wen T, Zhao Q (2020). *Probiotics for the Prevention of Antibiotic-associated
443:WebFetch of the PMC8183490 page itself — to the verified byline **Liao W, Chen C, Wen T, Zhao Q
457:- NEW attribution: entry **2 = PMC8183490** (Liao W et al., adults RCT meta-analysis; byline corrected
```

Disposition of each `Cai|2018` hit (after the iter-3 correction):
- Line 442 → **legitimately present (fix-documentation).** This is the iter-3 iteration note quoting the
  OLD byline `"Cai J, 2018"` verbatim to record what was corrected. Not a live citation.
- Line 457/458 → **legitimately present (fix-documentation).** The iter-2 audit prose, amended in iter-3
  to read "Liao W et al." and to annotate that the byline was corrected from the erroneous
  `"Cai J, 2018"` it originally used here. The OLD value appears only as the quoted thing-being-corrected.
- Live bibliography entry 2 (line 314): now reads **Liao W, Chen C, Wen T, Zhao Q (2020)** — zero
  occurrences of `Cai` or `2018` in any live citation, claim, or bibliography entry.
- `2018` as a standalone year → **0 hits outside the two fix-documentation quotes above.** It never
  appeared anywhere except the now-replaced entry 2 byline.

Disposition of each `Liao` hit:
- Line 314 → **live bibliography entry 2**, verified correct byline.
- Lines 443, 457 → **fix-documentation** (iteration note + amended iter-2 audit prose), recording the
  verified replacement byline.

**iter-3 audit result: PASS.** The falsified byline "Cai J, 2018" no longer appears in any live
citation; bibliography entry 2 carries the source-verified byline Liao W et al. (2020), J Clin
Gastroenterol. Every residual `Cai`/`2018` string is a quoted record of the corrected value inside the
audit/iteration-note documentation. RR 0.62 / 36-studies / 9312 figure and `meta_analysis` tag intact.
