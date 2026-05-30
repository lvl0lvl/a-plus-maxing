# Section A — GI Physiology, Microbiome, Gut Barrier, and Biomarker Validity

*Goal-agnostic library knowledge for designing a `gi-specialist` sub-agent. Not personalized. Every numeric claim carries exactly one inline `[N, type-tag]`. `mechanism_review` ≠ proven human efficacy; reading a mechanism does NOT license an outcome claim.*

---

## A-1 Microbiome

**Established.** The colonic microbiota ferments non-digestible carbohydrate to short-chain fatty acids (SCFAs) — chiefly acetate, propionate, butyrate. Butyrate is the primary energy substrate of colonocytes and the most consistently described host-beneficial SCFA; observational data tie a "healthy" microbiota to greater diversity/richness and higher abundance of SCFA-producing taxa `[1, mechanism_review]`. SCFA pathways (GPR41/GPR43 signaling, hepatic and peripheral metabolic effects) are well mapped mechanistically `[2, mechanism_review]`.

**Causal evidence is thin and easily over-claimed — this is the load-bearing caution.** Most microbiome–disease links are *correlative*, not causal; "correlation does not mean causation" is the field's own central caveat `[3, mechanism_review]`. A dedicated methods review notes the field is "constrained by challenges in establishing causality, an over-reliance on correlative studies, and methodological and analytical limitations," compounded by publication bias (positive results favored; failures to replicate go unreported) and "pseudoscientific commercialization" `[3, mechanism_review]`. The strongest causal signal comes from **bidirectional Mendelian randomization** (human genetic instruments, not an RCT): host-genetic-driven gut butyrate production was associated with improved insulin response after OGTT, and impaired propionate handling was causally linked to higher type 2 diabetes risk `[4, cohort]` (MR design; treat as genetic-instrument inference, not interventional proof). High-level controlled-trial evidence that SCFAs *regulate* human metabolism is "largely lacking" `[1, mechanism_review]`.

**Strain- and context-specificity.** Effects attributed to "the microbiome" are frequently strain-, dose-, host-genetics-, and population-specific. In a multi-country cohort, *country of origin* was the single strongest explanatory factor for SCFA concentration and diversity differences across adiposity strata — i.e., geography/diet swamped the adiposity signal `[5, cohort]`. Reproducibility is a known weakness: "many results from microbiome studies are not reproducible" owing to the imprecision of describing/recreating a complex microbiome `[3, mechanism_review]`.

**Agent implication:** treat any "your microbiome shows X, therefore do Y" claim as low-confidence unless backed by an interventional human trial of the *specific* strain/exposure. Diversity is a population-level descriptor, not a validated individual diagnostic target.

---

## A-2 Gut barrier / intestinal permeability (incl. zonulin assay controversy)

**Where permeability is a *validated* disease mechanism (real science).** The intestinal barrier is regulated by tight-junction (TJ) protein complexes governing the paracellular pathway `[6, mechanism_review]`. Barrier defects are mechanistically and temporally implicated in specific diseases:
- **Celiac disease** — gliadin-driven TJ disruption increases permeability and is part of the immune-activation cascade; celiac and type 1 diabetes are the canonical "permeability + autoimmunity" paradigms `[7, mechanism_review]`.
- **IBD (Crohn's)** — increased epithelial permeability *precedes* clinical relapse, and modestly increased leak-pathway permeability in first-degree relatives is an *independent risk factor* for IBD — among the strongest temporal (cause-before-effect) evidence in the field `[6, mechanism_review]`.
- **Critical illness / systemic conditions** — barrier dysfunction is documented across IBD, IBS, type 1 diabetes, and other systemic disease, though the temporal cause-vs-consequence direction is often unresolved `[6, mechanism_review]`.

**The validated *research* probe** is the dual-sugar **lactulose/mannitol (or lactulose/rhamnose) urinary recovery test**, used in research settings; in vitro work uses transepithelial electrical resistance (TER) `[6, mechanism_review]`. Note even these probes are too large to traverse the smallest "pore pathway," so they index the leak/unrestricted pathways `[6, mechanism_review]`.

**Zonulin assay controversy — load-bearing for refusing "leaky gut" test claims.** Zonulin (described as pre-haptoglobin-2) was proposed as a circulating regulator of TJ permeability. The problem is **the commercial ELISA does not measure what it claims**:
- A widely used commercial zonulin ELISA **does not detect the precursor of haptoglobin-2** (the purported zonulin); instead it recognizes **properdin** as a candidate second "zonulin family" member, and the kit cross-reacts with complement C3 and albumin `[8, in_vitro]`. (Antibody/immunoassay characterization study.)
- A methods critique titled "Blurring the picture in leaky gut research" concludes the ELISA measures **zonulin family peptides (ZFP), not zonulin per se**, that signal does not correlate with haptoglobin genotype as it should if it were pre-HP2, and that **ELISA-zonulin correlates only poorly with functional permeability** (e.g., lactulose/mannitol) `[9, mechanism_review]`.
- In first-degree relatives of Crohn's patients, **serum zonulin by commercial kit failed to correlate** with physiologic gut-permeability measures `[10, cohort]`.

**Agent implication:** "leaky gut" as a stand-alone consumer diagnosis, and especially a *commercial serum/fecal zonulin number*, is not a validated readout of intestinal permeability. The agent should refuse to treat a zonulin ELISA result as a quantitative permeability measurement, while affirming that permeability IS a real, validated mechanism in celiac and IBD specifically.

---

## A-3 Digestion + motility

**Normal landmarks an agent must know:**
- **Migrating motor complex (MMC):** the interdigestive (fasting) motility cycle that begins ~2–3 h after a meal once digestion/absorption finish; its role is mechanical/chemical "housekeeping" — clearing residue and bacteria from the stomach and small bowel before the next meal `[11, mechanism_review]`. The MMC cycle is driven by motilin and 5-HT (serotonin) interaction `[11, mechanism_review]`. Disruption of MMC housekeeping is a plausible contributor to bacterial overgrowth.
- **Small-bowel transit:** mean ~4 h 48 min ± 2 h 11 min by capsule measurement `[12, cohort]`.
- **Whole-gut transit:** wireless-motility-capsule passage in healthy individuals typically 2–5 days `[12, cohort]`.
- **Colonic motility:** colonic MMCs and high-amplitude propagating contractions propel fecal content and are mucosal/neuronal-serotonin dependent; they are altered in slow-transit constipation `[13, animal]` `[population-mismatch: mouse]` (CMMC generation mechanism characterized largely in murine/knockout models — mechanistic, not a human quantitative claim).

**Common dysmotility patterns:** gastroparesis (delayed gastric emptying), slow-transit constipation (reduced colonic propulsive activity), and rapid transit; formal classification relies on manometry, scintigraphy, and wireless motility capsule `[14, mechanism_review]`.

---

## A-4 Food sensitivity vs allergy vs intolerance taxonomy

This taxonomy is load-bearing for later refusal of invalid "food sensitivity" claims. Adverse food reactions split cleanly by mechanism `[15, mechanism_review]` `[16, mechanism_review]`:

| Category | Mechanism | Diagnostic basis | Example |
|---|---|---|---|
| **IgE-mediated food allergy** | Immune, IgE | Skin-prick / serum specific IgE + **oral food challenge** (gold standard); rapid, reproducible, can be anaphylactic | Peanut, shellfish allergy |
| **Non-IgE / mixed immune** | Immune, non-IgE | Clinical + histology | Celiac disease, FPIES, eosinophilic esophagitis |
| **Enzymatic intolerance** | Non-immune, enzyme deficiency | Breath test / genetic / dietary challenge | **Lactose intolerance** (lactase deficiency → incomplete lactose hydrolysis → fermentation symptoms) `[17, mechanism_review]` |
| **Pharmacologic / chemical** | Non-immune | Dietary challenge | Histamine, caffeine, vasoactive amines |
| **FODMAP / fermentable-carb intolerance** | Non-immune, osmotic + fermentation | Dietary challenge (low-FODMAP) | Fructose, polyol, fructan intolerance |
| **Non-celiac gluten/wheat sensitivity (NCGS)** | Disputed/undefined; a **diagnosis of exclusion** | Requires ruling OUT celiac (negative celiac serology/biopsy) AND wheat allergy (negative IgE), then symptom response to gluten | NCGS `[15, mechanism_review]` |

**Critical distinctions for the agent:**
- "Allergy" (IgE) ≠ "intolerance" (enzymatic/fermentative). Conflating them is the most common consumer error.
- **NCGS is defined by exclusion** — it is NOT confirmed by any "IgG food sensitivity panel." NCGS diagnosis explicitly requires exclusion of celiac disease and wheat allergy first `[15, mechanism_review]`.
- Commercial "food sensitivity / IgG" panels are not in this validated taxonomy and have no place in diagnosing any of these categories (the validated allergy assay is specific *IgE*, not IgG).

---

## A-5 GI / inflammation biomarker validity (per-marker)

For each: what it validly measures, the evidence, and what it does NOT establish.

### Fecal calprotectin
- **Validly measures:** neutrophil-derived protein in stool → a marker of *mucosal/intestinal inflammation*. Best-established use is **discriminating IBD from IBS** and tracking IBD activity.
- **Evidence:** pooled sensitivity **93%** and specificity **94%** at a 50 µg/g cutoff for IBD-vs-IBS in adults `[18, meta_analysis]`; a more recent meta-analysis gave summary sensitivity **85.8%** (95% CI 78.3–91) and specificity **91.7%**, with better performance at the ≤50 µg/g cutoff and in Western populations `[19, meta_analysis]`. It correlates with endoscopic activity better than CRP `[20, meta_analysis]`.
- **Does NOT establish:** a *specific* diagnosis (elevated in any neutrophilic GI inflammation — infection, NSAID enteropathy, neoplasia), and it does not localize disease. Cutoff choice trades sensitivity for specificity; a normal value is most useful for *ruling out* IBD in IBS-type symptoms.

### Fecal occult blood — FIT vs gFOBT
- **FIT (fecal immunochemical test):** antibody-specific for human globin → human GI blood. Pooled sensitivity **0.79** (0.69–0.86) and specificity **0.94** (0.92–0.95) for colorectal cancer `[21, meta_analysis]`; best sensitivity/specificity balance at cutoffs ~15–25 µg Hb/g `[21, meta_analysis]`. No dietary restriction needed (globin antibody is human-specific) `[22, mechanism_review]`.
- **gFOBT (guaiac):** chemical, detects peroxidase of any blood/peroxidase-active food → lower sensitivity and **diet/drug interference** (false positives from non-human blood, peroxidase-rich foods); FIT outperformed gFOBT (e.g., 53% vs 40% sensitivity for any neoplasia in one comparison) and guidelines favor replacing gFOBT with FIT `[22, mechanism_review]`.
- **Does NOT establish:** a diagnosis — a positive FIT is a *referral-to-colonoscopy* trigger, not proof of cancer; a negative does not exclude non-bleeding lesions.

### Commercial zonulin assay
- **Claims to measure:** zonulin (pre-HP2) as a permeability marker. **Validity contested → effectively invalid as labeled.** The commercial ELISA does not detect pre-HP2, cross-reacts with properdin/C3/albumin `[8, in_vitro]`, measures "zonulin family peptides" rather than zonulin, and correlates poorly with functional permeability tests `[9, mechanism_review]`; commercial-kit serum zonulin did not correlate with physiologic permeability in Crohn's first-degree relatives `[10, cohort]`.
- **Does NOT establish:** intestinal permeability, "leaky gut," or any disease state. The agent should not treat a zonulin number as a permeability measurement.

### Fecal secretory IgA (sIgA)
- **Validly reflects:** mucosal humoral immune activity; fecal IgA has been proposed as a useful mucosal-immunity marker `[23, mechanism_review]`.
- **Limits:** **non-specific** — explicitly stated as limited for IBD due to non-specificity; fecal IgA is **less stable** than IgA in other compartments, and commercial stool sIgA tests are **not validated** for clinical diagnosis `[23, mechanism_review]`.
- **Does NOT establish:** any specific GI diagnosis or "immune strength." A single fecal sIgA value should not drive any clinical decision.

### hs-CRP (for GI inflammation)
- **Validly measures:** systemic acute-phase inflammation (liver-produced). **Non-specific** — rises with any inflammatory/systemic process (RA, pneumonia, etc.), so it is an *indirect, non-specific* GI marker `[24, meta_analysis]`.
- **Evidence:** in IBS-symptom patients, CRP ≤0.5 mg/dL combined with calprotectin ≤40 µg/g essentially excludes IBD `[24, meta_analysis]`; calprotectin tracks endoscopic activity better than CRP `[20, meta_analysis]`.
- **Does NOT establish:** GI-specific inflammation or location; should be used in combination, never in isolation `[24, meta_analysis]`.

### Hydrogen/methane breath tests (SIBO; lactose/fructose malabsorption)
- **SIBO (glucose or lactulose substrate):** **North American Consensus (2017)** thresholds — H₂ rise ≥20 ppm by 90 min = positive; CH₄ ≥10 ppm = methane-positive `[25, mechanism_review]`. **Ongoing controversy:** sensitivity for glucose breath test ranges **20–93%** and specificity **30–86%** vs culture `[26, mechanism_review]`; lactulose as a substrate is contested (substrate dose materially changes positivity), and symptom–breath-result correlation is poor `[26, mechanism_review]` `[27, mechanism_review]`.
- **Lactose malabsorption (lactose H₂ breath test):** the most validated carbohydrate-malabsorption application; 4-sample lactose H₂ breath testing showed sensitivity **90–100%** and specificity up to **100%** `[27, mechanism_review]`. Caveat: malabsorption (the test result) ≠ symptomatic intolerance (the clinical syndrome); blind lactose challenge is the stricter intolerance standard `[27, mechanism_review]`.
- **Fructose malabsorption:** weaker — breath testing "could not add diagnostic advantage compared with direct dietary intervention," and symptom reliability for fructose *intolerance* is inaccurate `[27, mechanism_review]`. Methane-cutoff validity for malabsorption is itself questioned due to reading variability `[27, mechanism_review]`.
- **Does NOT establish:** for SIBO, a definitive diagnosis (no true gold standard; culture itself is imperfect); for sugars, a breath-positive does not by itself confirm a symptomatic clinical intolerance.

### Comprehensive stool analysis / consumer microbiome kits (assay science here; deep consumer-validity → Section C)
- **What the assay does:** 16S rRNA amplicon or shotgun metagenomic sequencing → relative-abundance taxonomic profile (plus, in panels, calprotectin/sIgA/elastase add-ons).
- **Analytical/clinical validity:** **poor and unregulated.** An evaluation of seven DTC services found major within- and across-provider discrepancies, with inter-provider variability "on the same scale as biological variability between different donors," attributed to method variability and weak QC `[28, in_vitro]`. There are **no regulatory-approved clinical microbiome diagnostic tests**; claims to detect an "abnormal" microbiome are **not substantiated** and DTC marketing is often misleading `[29, regulatory]`; a professional body (French Society of Microbiology) advised against microbiome testing given no defined "healthy" reference `[29, regulatory]`.
- **Does NOT establish:** a clinical diagnosis, a validated "dysbiosis" call, or a basis for targeted intervention. (Full consumer-test validity treatment deferred to Section C.)

---

## Key claims for the agent design (load-bearing conclusions)

1. **Microbiome = correlation, rarely causation.** Diversity/SCFA links are mostly observational; the agent must not convert a microbiome profile into a personalized "do Y" without an interventional human trial of the specific strain/exposure `[3, mechanism_review]` `[4, cohort]`.
2. **Permeability is real in *specific* diseases (celiac, IBD relapse-prediction, FDR risk), but "leaky gut" as a consumer diagnosis is not** `[6, mechanism_review]` `[7, mechanism_review]`.
3. **Refuse the commercial zonulin number as a permeability measurement** — the ELISA does not measure pre-HP2, cross-reacts (properdin/C3/albumin), and correlates poorly with functional permeability `[8, in_vitro]` `[9, mechanism_review]` `[10, cohort]`.
4. **Hold the food-reaction taxonomy firmly:** IgE allergy ≠ enzymatic intolerance ≠ FODMAP intolerance ≠ NCGS; **NCGS is a diagnosis of exclusion**; reject IgG "food sensitivity" panels as the wrong assay class `[15, mechanism_review]` `[16, mechanism_review]`.
5. **Calprotectin is the strong GI inflammation discriminator** (≈86–93% sens / ≈92–94% spec, IBD-vs-IBS) but is non-specific to a diagnosis `[18, meta_analysis]` `[19, meta_analysis]`.
6. **FIT > gFOBT; both are colonoscopy-referral triggers, not diagnoses** `[21, meta_analysis]` `[22, mechanism_review]`.
7. **hs-CRP and fecal sIgA are non-specific; never decision-drive on either alone** `[23, mechanism_review]` `[24, meta_analysis]`.
8. **Breath tests: lactose H₂ is well-validated; SIBO breath testing is contested (wide sens/spec, lactulose controversy); fructose breath testing adds little over dietary trial; malabsorption ≠ intolerance** `[25, mechanism_review]` `[26, mechanism_review]` `[27, mechanism_review]`.
9. **Consumer microbiome / comprehensive stool kits lack analytical and clinical validity and have no regulator-approved diagnostic status** `[28, in_vitro]` `[29, regulatory]`.

---

## Bibliography

1. Cronin et al. 2021. *Gut microbiota-derived SCFAs facilitate microbiota:host crosstalk and modulate obesity/hypertension* / SCFA-metabolism review. PMC7992370. https://pmc.ncbi.nlm.nih.gov/articles/PMC7992370/ — `mechanism_review`
2. den Besten et al. 2013. *The role of SCFAs in the interplay between diet, gut microbiota, and host energy metabolism.* PMC4939913. https://pmc.ncbi.nlm.nih.gov/articles/PMC4939913/ — `mechanism_review`
3. Walter & Hornef / field critique. *Credible inferences in microbiome research: rigour, reproducibility and relevance.* Nat Rev Gastroenterol Hepatol 2025; PMID 40745489. https://www.nature.com/articles/s41575-025-01100-9 (discovery also: "Hoops, Hopes, and Hypes of Human Microbiome Research," PMC5045145) — `mechanism_review`
4. Sanna et al. 2019. *Causal relationships among the gut microbiome, SCFAs and metabolic diseases* (bidirectional Mendelian randomization). Nat Genet; PMID 30778224 / s41588-019-0350-x. https://www.nature.com/articles/s41588-019-0350-x — `cohort` (MR / genetic-instrument human study)
5. Dugas et al. 2023. *Gut microbiota and fecal SCFAs differ with adiposity and country of origin: METS-microbiome study.* Nat Commun; s41467-023-40874-x. https://www.nature.com/articles/s41467-023-40874-x — `cohort`
6. Horowitz et al. 2023. *Paracellular permeability and tight junction regulation in gut health and disease.* PMC10127193. https://pmc.ncbi.nlm.nih.gov/articles/PMC10127193/ (corroborated by PMC4316216 IBD-TJ review) — `mechanism_review`
7. Fasano A. 2009/2012. *Tight junctions, intestinal permeability, and autoimmunity: celiac disease and type 1 diabetes paradigms.* PMID 19538307; PMC2886850. https://pmc.ncbi.nlm.nih.gov/articles/PMC2886850/ — `mechanism_review`
8. Scheffler et al. 2018. *Widely Used Commercial ELISA Does Not Detect Precursor of Haptoglobin-2, but Recognizes Properdin as a Potential Second Member of the Zonulin Family.* PMID 29459849; PMC5807381. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5807381/ — `in_vitro` (immunoassay characterization)
9. Massier et al. 2021. *Blurring the picture in leaky gut research: how shortcomings of zonulin as a biomarker mislead the field of intestinal permeability.* Gut; PMC8355880. https://pmc.ncbi.nlm.nih.gov/articles/PMC8355880/ — `mechanism_review`
10. Sapone-type cohort 2021. *Serum Zonulin Measured by Commercial Kit Fails to Correlate With Physiologic Measures of Altered Gut Permeability in First-Degree Relatives of Crohn's Patients.* PMC8027468. https://pmc.ncbi.nlm.nih.gov/articles/PMC8027468/ — `cohort`
11. Deloose et al. 2016. *Interdigestive migrating motor complex — its mechanism and clinical importance.* PMC5137267. https://pmc.ncbi.nlm.nih.gov/articles/PMC5137267/ — `mechanism_review`
12. Capsule-transit study (small-bowel/whole-gut transit). PMC10152174 — *Prolonged Gastric Transit Time in Small-Bowel Capsule Endoscopy.* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10152174/ — `cohort`
13. Spencer/Dinning et al. 2014. *Colonic Migrating Motor Complexes, High-Amplitude Propagating Contractions, Neural Reflexes and Serotonin.* PMC4204412 (mechanisms characterized in murine/nNOS-KO models). https://pmc.ncbi.nlm.nih.gov/articles/PMC4204412/ — `animal` (mouse)
14. *Advances in the diagnosis and classification of gastric and intestinal motility disorders.* PMC6646879. https://pmc.ncbi.nlm.nih.gov/articles/PMC6646879/ — `mechanism_review`
15. *New Insights and Evidence on "Food Intolerances": Non-Celiac Gluten Sensitivity and Nickel Allergic Contact Mucositis.* PMC10222428. https://pmc.ncbi.nlm.nih.gov/articles/PMC10222428/ — `mechanism_review`
16. Turnbull et al. 2015. *Differentiating food allergies from food intolerances.* PMID 21792544. https://pubmed.ncbi.nlm.nih.gov/21792544/ — `mechanism_review`
17. *Nutrition in Patients with Lactose Malabsorption, Celiac Disease, and Related Disorders.* PMC8746545. https://pmc.ncbi.nlm.nih.gov/articles/PMC8746545/ — `mechanism_review`
18. Waugh et al. 2013. *Faecal calprotectin testing for differentiating inflammatory and non-inflammatory bowel diseases: systematic review and economic evaluation* (93% sens / 94% spec at 50 µg/g, IBD-vs-IBS). PMC4781415 / NBK261316. https://pmc.ncbi.nlm.nih.gov/articles/PMC4781415/ — `meta_analysis`
19. 2023 systematic review/meta-analysis. *Diagnostic performance of faecal calprotectin in distinguishing IBD from IBS in adults* (sens 85.8%, spec 91.7%). PMID 37823411. https://pubmed.ncbi.nlm.nih.gov/37823411/ — `meta_analysis`
20. Mosli et al. 2015. *C-Reactive Protein, Fecal Calprotectin, and Stool Lactoferrin for Detection of Endoscopic Activity in Symptomatic IBD: Systematic Review and Meta-Analysis.* PMID 25964225. https://pubmed.ncbi.nlm.nih.gov/25964225/ — `meta_analysis`
21. Lee et al. 2014. *Accuracy of fecal immunochemical tests for colorectal cancer: systematic review and meta-analysis* (sens 0.79, spec 0.94; cutoff 15–25 µg/g). PMID 24658694; PMC4189821. https://pmc.ncbi.nlm.nih.gov/articles/PMC4189821/ — `meta_analysis`
22. *Utility of Stool-Based Tests for Colorectal Cancer Detection: A Comprehensive Review* (FIT vs gFOBT: FIT human-globin-specific, no diet restriction, superior sensitivity). PMC11353969. https://pmc.ncbi.nlm.nih.gov/articles/PMC11353969/ — `mechanism_review`
23. Vernia et al. / Sipponen. *Update on clinical and research application of fecal biomarkers for gastrointestinal diseases* (fecal sIgA non-specific, less stable, commercial stool tests unvalidated). PMC5292605. https://pmc.ncbi.nlm.nih.gov/articles/PMC5292605/ — `mechanism_review`
24. Menees et al. 2015. *Meta-analysis of CRP, ESR, fecal calprotectin and fecal lactoferrin to exclude IBD in adults with IBS* (CRP non-specific; CRP ≤0.5 + calprotectin ≤40 excludes IBD). PMID 25732419. https://pubmed.ncbi.nlm.nih.gov/25732419/ — `meta_analysis`
25. Rezaie et al. 2017. *Hydrogen and Methane-Based Breath Testing in GI Disorders: The North American Consensus.* PMID 28323273. https://pubmed.ncbi.nlm.nih.gov/28323273/ — `mechanism_review` (consensus guideline)
26. *Overview of Breath Testing in Clinical Practice in North America* / Performance and interpretation of HMBT under NA Consensus (glucose BT sens 20–93%, spec 30–86%; lactulose controversy). PMC10191541 / PMC9652228. https://pmc.ncbi.nlm.nih.gov/articles/PMC9652228/ — `mechanism_review`
27. Hammer et al. 2021. *Hydrogen Breath Tests: Are They Really Useful in the Nutritional Management of Digestive Disease?* (lactose H₂ sens 90–100%/spec ~100%; fructose adds little vs dietary trial; methane-cutoff variability). PMC8002624. https://pmc.ncbi.nlm.nih.gov/articles/PMC8002624/ — `mechanism_review`
28. 2025. *Evaluating the analytical performance of direct-to-consumer gut microbiome testing services* (7 services; inter-provider variability on the scale of inter-donor biological variability; weak QC). Commun Biol s42003-025-09301-3; PMC12946161. https://www.nature.com/articles/s42003-025-09301-3 — `in_vitro` (analytical-performance evaluation)
29. 2024. *The DTC microbiome testing industry needs more regulation* (no regulator-approved clinical microbiome diagnostic; "abnormal" claims unsubstantiated; professional bodies advise against). Science adk4271; corroborated PMC12728816. https://www.science.org/doi/10.1126/science.adk4271 — `regulatory`

**Single-lab / single-source flags:** Zonulin-validity cluster (refs 7, 9; Fasano group originated the zonulin construct, and several critiques respond directly to that body of work) — the *critical* findings here (refs 8, 9, 10) come from **independent** groups (Scheffler/Schulzke; Massier; Crohn's-FDR cohort), so the "ELISA is invalid" conclusion is NOT single-lab-dependent — confidence high. Microbiome-causality framing leans on review-class sources (refs 1, 3); the one quantitative causal claim (ref 4) is a single large MR study — flagged as genetic-instrument inference, not interventional proof.

---

## Self-check

- **Every numeric claim type-tagged:** Yes. Sens/spec figures (calprotectin 93/94, 85.8/91.7; FIT 0.79/0.94; lactose 90–100/100; glucose-BT 20–93/30–86), transit times, and threshold values each carry an inline `[N, tag]`.
- **Animal/in_vitro numerics carry [population-mismatch]:** The colonic-MMC mechanism (ref 13, mouse) carries `[population-mismatch: mouse]`; it grounds a *mechanistic* statement, not a human numeric. The zonulin-ELISA cross-reactivity (ref 8) is `in_vitro` and grounds an assay-characterization (qualitative) claim, not a clinical numeric — no human-numeric population-mismatch required. The DTC-performance evaluation (ref 28) is `in_vitro`/analytical; its "variability on the scale of inter-donor variability" is qualitative, not a clinical effect size.
- **No vendor_label / anecdote_aggregate grounding numbers:** Confirmed — neither tag is used anywhere; no numeric rests on vendor or anecdote sourcing.
- **No route-extrapolation issues:** No dose/route claims in this section (biomarker/physiology section; no compound dosing) → `risk_floor_readiness = null` for Section A.
- **Single-lab dominance surfaced:** Yes — zonulin construct (Fasano group) flagged, with explicit note that the disconfirming evidence is independent-group; microbiome-causality flagged as review-heavy + single MR study.
- **Source count:** 29 numbered references; all on Tier-1/Tier-2 whitelisted hosts (PMC/PubMed, Nature, Cell-press-adjacent, Science, BMJ-Gut-adjacent). Distinct admissible primaries/meta-analyses ≥ 8 (refs 4, 5, 8, 10, 18, 19, 20, 21, 24, 25, 27, 28 alone = 12 primary/meta/consensus). Target met. No biorxiv/medrxiv preprints were used as load-bearing citations (some appeared in discovery lists but were not cited).
