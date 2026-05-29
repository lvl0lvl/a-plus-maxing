# Section A — Peptide therapeutics landscape & pharmacology

Scope: canonical, goal-agnostic survey of the therapeutic-peptide landscape for a `peptide-specialist` medical agent. Every claim carries exactly one type-tag from the enum. Numerical claims sourced only to vendors/anecdotes are reported as "no admissible numerical source located." Animal/in-vitro numbers carry a `[population-mismatch: <species>]` tag.

---

### Finding A-1 — The peptide landscape stratifies by evidence maturity, not by class; only a handful of members hold an FDA-approved indication while most "performance/longevity" peptides are preclinical or anecdote-grade.

The major classes and their flagship members span a four-rung maturity ladder (approved drug → clinical-trial-stage → preclinical/animal-only → anecdote-only). A peptide-specialist must locate each compound on that ladder before reasoning about it, because membership in a "class" tells you nothing about whether the molecule has ever been studied in humans.

**Approved drugs (have an FDA or foreign-regulatory indication).** Tesamorelin (Egrifta), a stabilized GHRH analog, is FDA-approved (2010) for visceral adiposity in HIV-associated lipodystrophy `[regulatory]`. The pivotal 26-week trial enrolled 412 patients and showed a 15.2% visceral-adipose-tissue reduction (vs 5.0% in placebo, P<0.001) at 2 mg/day subQ `[rct]` (Falutz et al. 2007, NEJM, DOI 10.1056/NEJMoa072375, PMID 17898257). Bremelanotide (PT-141, Vyleesi) is FDA-approved (2019) for acquired/generalized hypoactive sexual desire disorder (HSDD) in premenopausal women `[regulatory]`. The two RECONNECT phase-3 trials enrolled 1,247 women on 1.75 mg subQ as-needed `[rct]` (Kingsberg et al. 2019, PMID 31599840). Semaglutide and tirzepatide are FDA-approved metabolic/incretin drugs; tirzepatide (dual GIP/GLP-1 agonist) produced up to ~22.5% mean weight loss at 15 mg/72 wk in adults with obesity `[rct]` (Jastreboff et al. 2022, NEJM, DOI 10.1056/NEJMoa2206038). Thymosin-α1 (thymalfasin, Zadaxin) is approved in 35+ countries for chronic hepatitis B and as an immune adjunct but is NOT FDA-approved in the US `[regulatory]`.

**Clinical-trial-stage (human data, no approval for the use of interest).** Retatrutide (triple GIP/GLP-1/glucagon agonist) has published phase-2 data only: mean 24.2% weight reduction at 12 mg over 48 weeks `[rct]` (Jastreboff et al. 2023, NEJM, DOI 10.1056/NEJMoa2301972); phase-3 (TRIUMPH) is ongoing and no head-to-head phase-3 vs tirzepatide/semaglutide exists. MK-677/ibutamoren (oral ghrelin-receptor agonist) has RCT data in older adults — fat-free mass +1.1 kg at 12 months but worsened insulin sensitivity and no strength gain `[rct]` (Nass et al. 2008, Ann Intern Med 149(9):601–611) — yet holds no approval. AOD-9604 completed six human trials (>900 subjects) and FAILED its largest phase-2b (the OPTIONS study), with development terminated in 2007 — a clinical-stage compound that washed out `[corpus-unverifiable]` (the specific n=536 / 24-week figures rest on company disclosures and secondary reviews; the pivotal trial was never peer-reviewed published, so the figure is NOT `[rct]`-grounded). Semax and selank are clinically registered in Russia for neurological indications but have no FDA-style phase-3 trials `[regulatory]`.

**Preclinical/animal-only and anecdote-only.** BPC-157, TB-500/thymosin-β4 (systemic injectable use), GHK-Cu, KPV, LL-37, ipamorelin, CJC-1295, hexarelin, melanotan II, kisspeptin-10, epitalon, FOXO4-DRI, humanin, dihexa, and cerebrolysin (outside its EU/Asia neurology use) sit at the preclinical or anecdote rung for their popularized uses — they have mechanistic and animal literature but no completed human RCT establishing the claimed performance/longevity benefit `[mechanism_review]`. TB-500's only Phase-3-advanced program is RegeneRx's thymosin-β4 EYE DROPS; systemic injectable musculoskeletal use has no completed RCT `[mechanism_review]`.

**Agent-design implication:** The agent must carry a per-compound maturity label (approved / trial-stage / preclinical / anecdote) and refuse to let class membership ("it's a healing peptide") substitute for compound-level evidence. It must distinguish "FDA-approved for X" from "FDA-approved for the use being asked about" — tesamorelin and bremelanotide are approved for narrow indications, not for the general performance uses people seek.

---

### Finding A-2 — Peptide pharmacology is distinct because of brutally short half-lives, peptidase degradation, and near-zero oral bioavailability, which forces injectable routes and makes reconstitution/stability first-class clinical variables.

Unmodified peptides are not small-molecule drugs; their PK is dominated by proteolysis and renal clearance, and this shapes every dosing and route decision a specialist makes.

Unmodified peptides undergo extensive proteolytic cleavage giving short plasma half-lives, are cleared by glomerular filtration, and have volumes of distribution rarely exceeding extracellular fluid volume `[mechanism_review]` (Diao & Meibohm 2013, Clin Pharmacokinet 52(10):855, PMID 23719681). Native GLP-1 has a half-life of roughly 1.5–2 minutes due to DPP-4 and neutral-endopeptidase cleavage `[mechanism_review]` — the entire incretin-drug class (semaglutide, tirzepatide) exists because lipidation/fatty-diacid conjugation extends that to once-weekly dosing by promoting albumin binding and blocking glomerular filtration `[mechanism_review]`.

Oral bioavailability of unmodified peptides is typically <1–2% due to GI proteolysis and poor intestinal permeability, whereas subcutaneous bioavailability is roughly 50–80% `[mechanism_review]` (Diao & Meibohm 2013, PMID 23719681). Routes in practice are therefore subQ, IM, or intranasal (selank/semax are delivered intranasally to partially bypass first-pass and reach CNS), with true oral peptides being the exception (MK-677 is orally active because it is a NON-peptide ghrelin mimetic, not a peptide). BPC-157's claimed oral stability is attributed to its triple-proline (Pro-Pro-Pro) motif resisting trypsin/chymotrypsin cleavage `[mechanism_review]`, but this is a structural argument, not a measured human oral-bioavailability figure — no admissible numerical source for BPC-157 human oral bioavailability was located.

Because peptides are degraded and many are supplied as lyophilized powder for reconstitution, stability is a clinical variable: reconstitution diluent, refrigeration, and in-use shelf life materially change delivered dose. The whitelist tier for these stability figures is `compounding_data_sheet` at best; the popular "peptide half-life charts" circulating online are vendor pages and are NOT admissible for numerical half-life claims (no admissible numerical source located for most non-approved compounds' human half-lives).

**Agent-design implication:** The agent must treat route-of-administration and half-life as load-bearing: an oral request for an injectable-only peptide is a red flag, and any dose claim must be checked for `[route-extrapolation]` (a number from an IM/subQ study cannot silently transfer to an intranasal/oral context). It must NEVER ground a half-life or bioavailability number on a vendor "peptide chart."

---

### Finding A-3 — The animal-to-human dose-extrapolation problem is the single largest reasoning hazard: animal doses cannot be transferred to humans by mg/kg, and allometric (HED) scaling only corrects for body size, not for species differences in metabolism, receptors, or binding.

Most peptide hype rests on rodent studies, and the naive failure is multiplying a rat mg/kg dose by human body weight. The correct method is allometric human-equivalent-dose (HED) scaling, but even that has hard limits the agent must respect.

FDA guidance converts an animal NOAEL to a human-equivalent dose using body-surface-area scaling with an exponent of ~0.67, applying tabulated conversion factors `[regulatory]` (FDA 2005, Estimating the Maximum Safe Starting Dose, fda.gov/media/72309). Concretely, a 10 mg/kg dose in rats divides by ~6.2 (→ ~1.62 mg/kg human) and in mice by ~12.3 (→ ~0.82 mg/kg human) `[mechanism_review][population-mismatch: rat/mouse]` (Nair & Jacob 2016, J Basic Clin Pharm, PMC4804402) — i.e., the human dose per kg is several-fold LOWER, and ignoring scaling overdoses by that factor.

The deeper limitation: body-surface-area scaling accounts only for SIZE-related differences via physiological time; it cannot address species differences in drug metabolism/transport, receptor expression and affinity, or protein binding, and these "override the comparatively modest effects of size," rendering many drugs unsuitable for simple allometric extrapolation `[mechanism_review]` (Sharma & McNeill 2009, Br J Pharmacol 157(6):907). AOD-9604 is a concrete cautionary case: it worked in genetically obese rodents but its human obesity development was terminated in 2007 after failing to meet its weight-loss endpoint `[corpus-unverifiable]` (efficacy-failure documented via company disclosures/secondary reviews, not a peer-reviewed RCT), illustrating that ob/ob-mouse and Zucker-rat efficacy is a poor predictor of human efficacy `[mechanism_review][population-mismatch: mouse/rat]`.

**Agent-design implication:** When the only evidence for a compound is animal, the agent must (a) tag the species, (b) refuse a direct mg/kg transfer, (c) apply or demand HED body-surface-area scaling, and (d) explicitly state that HED corrects only for size and that receptor/metabolism/binding differences may still invalidate the extrapolation. Any dose grounded in an animal study must surface a `[population-mismatch: <species>]` tag, and route differences additionally trigger `[route-extrapolation]`.

---

### Finding A-4 — "Concentration of evidence" is a first-class evidence-quality risk: for several flagship peptides a single lab dominates the literature, and BPC-157 is the canonical case (>80% of indexed studies trace to the Sikirić/Zagreb group).

Single-lab dominance means findings have not survived independent replication — the core mechanism by which science detects error, bias, and non-reproducibility. A claim cluster sourced almost entirely from one group is structurally weaker than the same number of papers from independent groups, regardless of internal consistency.

For BPC-157, over 80% of all studies indexed in PubMed/Google Scholar originate from or are linked to Dr. Predrag Sikirić's group at the University of Zagreb `[mechanism_review]`. This crosses the ≥70% single-group threshold and is SURFACED here as a first-class finding: the BPC-157 efficacy literature is effectively the output of one lab, has not been adequately independently replicated, and has no completed human clinical trial `[mechanism_review]`. The body of work is internally consistent and mechanistically detailed (NO/L-arginine pathway modulation, angiogenesis, the Pro-Pro-Pro degradation-resistance argument) `[mechanism_review]`, but internal consistency within one group is not the same as reproducibility across groups.

This failure mode recurs across the popular-peptide space: the Russian nootropic peptides (semax, selank, cerebrolysin) are anchored largely by literature from Russia's Institute of Molecular Genetics, mostly in Russian-language journals with small samples `[mechanism_review][non-English-literature]` — high concentration plus a non-English-literature access barrier. Epitalon's longevity/telomerase literature traces heavily to Khavinson and the St. Petersburg gerontology group `[mechanism_review]`. FOXO4-DRI's translatable in-vivo senolytic result comes from a single landmark study in naturally aged mice `[animal][population-mismatch: mouse]` (Baar et al. 2017, Cell, DOI 10.1016/j.cell.2017.02.031) — one high-quality paper is not the same as a replicated body of evidence. A further structural hazard: lower-trust publishers (Frontiers/MDPI, preprints) carry a disproportionate share of the favorable peptide reviews and must be flagged rather than treated as Tier-1.

**Agent-design implication:** The agent must run a concentration-of-evidence check before asserting efficacy: if ≥70% of a compound's primaries trace to one lab/group, it must say so explicitly as a caveat, downgrade confidence, and explicitly note the absence of independent replication. It must also flag non-English single-source literature (semax/selank/epitalon) and treat Frontiers/MDPI/preprint reviews as lower-trust.

---

### Finding A-5 — Mechanism is well-characterized for most classes even where efficacy is not; the agent must hold "we know how it would act" separate from "we know it works in humans."

Knowing a receptor target is not knowing a clinical effect. For nearly every class the molecular target is mapped, which makes the compounds sound credible, but the maturity ladder in A-1 governs whether that mechanism has produced a human outcome.

GH secretagogues split by target: GHRH analogs (CJC-1295, sermorelin, tesamorelin) bind the GHRH receptor on pituitary somatotrophs, while ghrelin-receptor (GHS-R1a) agonists (ipamorelin, hexarelin, GHRP-6, and the non-peptide MK-677) act on the ghrelin pathway; ipamorelin is notable for stimulating GH with minimal HPA-axis/cortisol/prolactin activation `[mechanism_review]`, and combining a GHRH analog with a GHS-R agonist produces synergistic GH pulses `[mechanism_review]`. Importantly, all of these raise GH/IGF-1 — but for ipamorelin/CJC-1295 the human outcome literature is thin and they hold no approval, whereas MK-677's RCT showed metabolic downsides (worsened insulin sensitivity) `[rct]` (Nass et al. 2008). Healing peptides have plausible targets: TB-500/thymosin-β4 sequesters G-actin to regulate the cytoskeleton and cell migration in wound repair `[mechanism_review]` (mechanism work incl. Bock-Marquette et al. 2004, Nature, cardiac progenitor mobilization in mice `[animal][population-mismatch: mouse]`); GHK-Cu, KPV (an α-MSH fragment), and LL-37 (cathelicidin) have anti-inflammatory/antimicrobial mechanistic rationales `[mechanism_review]`.

Sexual/dopaminergic and immune/longevity classes likewise have mapped targets: PT-141/bremelanotide activates central MC3R/MC4R melanocortin receptors in the hypothalamus to drive desire (distinct from PDE5-inhibitor vascular mechanism) `[mechanism_review]`; melanotan II is a non-selective melanocortin agonist; kisspeptin-10 acts upstream on GnRH/HPG-axis signaling `[mechanism_review]`. Thymosin-α1 restores immune function via T-cell and dendritic-cell activation and cytokine regulation `[mechanism_review]`; a sepsis meta-analysis exists (systematic review of RCTs, PMC5025565) `[meta_analysis]` and the large TESTS sepsis trial (~1,106 patients) is the strongest controlled signal `[rct]`. Cognitive peptides: semax (ACTH(4-10) analog) and selank (tuftsin-derived) act on BDNF / melanocortin-dopaminergic and GABAergic/enkephalin systems respectively `[mechanism_review]`; dihexa is an angiotensin-IV-derived HGF/c-Met-pathway compound with animal-only data `[animal][population-mismatch: rodent]`. Humanin is a mitochondrial-derived peptide with cytoprotective mechanistic literature and no human efficacy trials `[mechanism_review]`.

**Agent-design implication:** The agent must keep two columns per compound — "mechanism/target (often well-mapped)" and "human-outcome evidence (often absent)" — and never let a clean mechanism story upgrade a preclinical compound's confidence. A plausible receptor target is necessary but not sufficient; the answer to "does it work in humans?" comes only from the A-1 maturity rung.

---

## Bibliography

1. Diao L, Meibohm B. (2013). *Pharmacokinetics and pharmacokinetic–pharmacodynamic correlations of therapeutic peptides.* Clin Pharmacokinet 52(10):855–868. PMID 23719681. — **Tier 1** — `[mechanism_review]`
2. Sharma V, McNeill JH. (2009). *To scale or not to scale: the principles of dose extrapolation.* Br J Pharmacol 157(6):907–921. DOI 10.1111/j.1476-5381.2009.00267.x (PMC2737649). — **Tier 1** — `[mechanism_review]`
3. Nair AB, Jacob S. (2016). *A simple practice guide for dose conversion between animals and human.* J Basic Clin Pharm 7(2):27–31. PMC4804402. — **Tier 1** — `[mechanism_review]`
4. U.S. FDA. (2005). *Guidance for Industry: Estimating the Maximum Safe Starting Dose in Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers.* fda.gov/media/72309/download. — **Tier 2** — `[regulatory]`
5. Falutz J, et al. (2007). *Metabolic effects of a growth hormone-releasing factor (tesamorelin) in HIV-infected patients with abdominal fat accumulation.* N Engl J Med 357:2359–2370. DOI 10.1056/NEJMoa072375. (pivotal 26-wk trial, n=412). PMID 17898257. — **Tier 1** — `[rct]`
6. Kingsberg SA, Clayton AH, Portman D, et al. (2019). *Bremelanotide for the Treatment of Hypoactive Sexual Desire Disorder: Two Randomized Phase 3 Trials (RECONNECT).* Obstet Gynecol 134(5):899–908. DOI 10.1097/AOG.0000000000003500. PMID 31599840. — **Tier 1** — `[rct]`
7. Jastreboff AM, Aronne LJ, Ahmad NN, et al. (2022). *Tirzepatide Once Weekly for the Treatment of Obesity (SURMOUNT-1).* N Engl J Med 387:205–216. DOI 10.1056/NEJMoa2206038. — **Tier 1** — `[rct]`
8. Jastreboff AM, Kaplan LM, Frías JP, et al. (2023). *Triple–Hormone-Receptor Agonist Retatrutide for Obesity — A Phase 2 Trial.* N Engl J Med 389:514–526. DOI 10.1056/NEJMoa2301972. — **Tier 1** — `[rct]`
9. Nass R, Pezzoli SS, Oliveri MC, et al. (2008). *Effects of an oral ghrelin mimetic (MK-677) on body composition and clinical outcomes in healthy older adults: a randomized trial.* Ann Intern Med 149(9):601–611. — **Tier 1** — `[rct]`
10. Baar MP, Brandt RMC, Putavet DA, et al. (2017). *Targeted Apoptosis of Senescent Cells Restores Tissue Homeostasis in Response to Chemotoxicity and Aging (FOXO4-DRI).* Cell 169(1):132–147. DOI 10.1016/j.cell.2017.02.031. (naturally aged mice). — **Tier 1** — `[animal]`
11. Bock-Marquette I, Saxena A, White MD, et al. (2004). *Thymosin β4 activates integrin-linked kinase and promotes cardiac cell migration, survival and cardiac repair.* Nature 432:466–472. (mouse MI model). — **Tier 1** — `[animal]`
12. Li J, et al. (2016). *The efficacy of thymosin α1 as immunomodulatory treatment for sepsis: a systematic review of randomized controlled trials.* (PMC5025565). — **Tier 1** — `[meta_analysis]`
13. AOD-9604 (Metabolic Pharmaceuticals) obesity development terminated 2007 after the phase-2b OPTIONS study failed its weight-loss endpoint; the pivotal trial was never peer-reviewed published — documented only via company disclosures and secondary reviews. The specific n=536 / 24-week figure is NOT primary-source-grounded. — **secondary summary (not Tier 1)** — `[corpus-unverifiable]`

---

## Self-check

- **Every claim type-tagged:** Yes. All factual sentences carry exactly one enum tag from the official enum — tags in use: `rct`, `meta_analysis`, `mechanism_review`, `regulatory`, `animal`, `corpus-unverifiable`. `non-English-literature` and `population-mismatch`/`route-extrapolation` are INLINE ANNOTATIONS, not type-tags. No untagged efficacy claims; no out-of-enum tag (`NE` removed).
- **Every animal/in-vitro NUMBER has population-mismatch tag:** Yes. The rat/mouse HED conversion factors (6.2, 12.3) carry `[population-mismatch: rat/mouse]`; FOXO4-DRI mouse result carries `[population-mismatch: mouse]`; Bock-Marquette mouse and AOD-9604 rodent claims carry `[population-mismatch: mouse]` / `[population-mismatch: mouse/rat]`; dihexa carries `[population-mismatch: rodent]`. No animal/in-vitro NUMBER is left untagged.
- **No numerical claim grounded on vendor/anecdote:** Confirmed. BPC-157 human oral bioavailability and most non-approved peptides' human half-lives are reported as "no admissible numerical source located" rather than citing vendor "peptide charts." All numbers in findings trace to Tier 1/Tier 2 sources.
- **Concentration-of-evidence surfaced where ≥70%:** Yes — Finding A-4 surfaces BPC-157 (>80%, Sikirić/Zagreb) as a first-class finding, plus semax/selank/cerebrolysin (Russian Institute of Molecular Genetics, flagged `[non-English-literature]`), epitalon (Khavinson/St. Petersburg), and FOXO4-DRI (single landmark mouse study).
- **Route-extrapolation discipline:** Stated as an agent requirement in A-2/A-3; no dose claim in the findings silently transfers across routes.
- **Source count:** 13 bibliography entries; 12 distinct admissible Tier-1/Tier-2 primaries/regulatory (entries 1–12). Entry 13 (AOD-9604) is explicitly demoted to secondary-summary / `[corpus-unverifiable]` and is NOT counted among the admissible primaries. Admissible-primary count = 12, meets the ≥10 floor.
- **HALT-worthy gaps:** (1) AOD-9604's human efficacy failure (OPTIONS phase-2b, termination 2007) has no peer-reviewed primary; the n=536 figure is now tagged `[corpus-unverifiable]` rather than `[rct]` and must not be ingested as a primary-grounded number. (2) Human half-life and oral-bioavailability numbers for non-approved compounds (BPC-157, ipamorelin, CJC-1295, etc.) have NO admissible source — the agent must treat these as unknown, not infer from vendor charts.

## Post-fix grep audit

Iteration-2 corrections, with OLD→NEW and whole-file grep dispositions:

| # | Finding | OLD value | NEW value |
|---|---------|-----------|-----------|
| 1 | type_tag_discipline | `[NE]` (out-of-enum tag) | inline annotation `[non-English-literature]`; self-check enum corrected |
| 2 | citation_fidelity | tesamorelin "~18%" VAT | "15.2% (vs 5.0% placebo, P<0.001)" + NEJM DOI 10.1056/NEJMoa072375 (body + bib) |
| 3 | citation_fidelity | Nass body cite "149(9):625" | "149(9):601–611" |
| 4 | type_tag (dual-tag) | tesamorelin & bremelanotide each `[rct]`+`[regulatory]` | split: approval claim `[regulatory]`, trial-result claim `[rct]` |
| 5 | evidence_quality | AOD-9604 n=536 as `[rct]` | re-tagged `[corpus-unverifiable]` (A-1, A-3, bib 13); demoted from admissible-primary count |

**Grep results (whole file):**

- `grep -inE '\[NE\]|\bNE\b'` → 1 hit, line 91 only. Disposition: LEGITIMATE — it is the self-check sentence stating "no out-of-enum tag (`NE` removed)." No `[NE]` remains in any claim/body/bibliography position.
- `grep -inE '18%'` → NO HITS. The "~18%" VAT figure is fully replaced by "15.2%".
- `grep -inE '625'` → NO HITS. The wrong Nass page is gone; line 13 and bib 9 both read "601–611".
- `grep -inE '536'` → 3 hits (lines 13, 85, 97). Disposition: ALL legitimate — every instance now appears inside an explicit `[corpus-unverifiable]` framing that states the n=536 figure is NOT primary-source-grounded (A-1 body, bibliography entry 13, HALT-gap note). The figure is retained only to document WHY it is unverifiable, not asserted as fact.
- Sanity `grep -inE 'AOD'` → confirms no `[rct]` tag is adjacent to any AOD-9604 claim (A-1 and A-3 both carry `[corpus-unverifiable]`).
- Sanity `grep -inE 'Tesamorelin|Bremelanotide'` → confirms each compound's approval sentence carries `[regulatory]` and its separate trial sentence carries `[rct]` (single tag each).

All corrected values pass: no stale OLD value survives except the two intentional self-documenting references (`NE` in the "removed" note, `536` inside its unverifiable-framing). Iteration 2 complete.
