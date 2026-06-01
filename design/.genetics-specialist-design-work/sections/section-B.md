# Section B — Pharmacogenomics: CYP450 + Non-CYP Drug-Gene Interactions

Pharmacogenomics (PGx) studies how inherited variation in genes encoding drug-metabolizing enzymes, transporters, and targets alters the disposition and effect of medications. This section is canonical reference material: it describes *what is known* about the major pharmacogenes, the governance frameworks that translate gene variants into clinical guidance, and the highest-evidence drug-gene pairs. It deliberately frames every recommendation around a single load-bearing principle articulated at the end — **PGx informs prescribing; it never authorizes it.**

## 1. The Major Pharmacogenes and the Genotype-to-Phenotype Translation

### Star-allele nomenclature (PharmVar)

Variation in the cytochrome P450 (CYP) genes is catalogued using the "star" (*) allele system, in which `*1` is the reference (fully functional) haplotype and each numbered allele denotes a specific haplotype defined by one or more sequence variants. This nomenclature, originally developed in the mid-1990s for CYP2D6, was formalized when the Human Cytochrome P450 Allele Nomenclature Database transitioned to the Pharmacogene Variation (PharmVar) Consortium in 2017, which now serves as the central repository providing a "common language" for naming pharmacogene haplotypes [1, mechanism_review]. PharmVar launched with three high-priority genes — CYP2C9, CYP2C19, and CYP2D6 — and supplies the allele definitions that downstream resources (PharmGKB, CPIC) build on [1, mechanism_review].

### Activity scores and metabolizer phenotypes

A patient inherits two haplotypes (one per chromosome), together called the **diplotype** (e.g., CYP2D6 `*1/*4`). Each allele is assigned a **function status** — no function, decreased function, normal function, or increased function — and, for genes like CYP2D6, a numeric **activity value**. Summing the two alleles' activity values yields a diplotype **activity score**, which is then mapped to a **metabolizer phenotype**:

- **Poor Metabolizer (PM)** — minimal/absent enzyme activity
- **Intermediate Metabolizer (IM)** — reduced activity
- **Normal Metabolizer (NM)** — formerly "extensive metabolizer," the reference state
- **Rapid / Ultrarapid Metabolizer (RM/UM)** — elevated activity, often from gene duplication

For CYP2D6, a CPIC-led modified-Delphi consensus standardized this translation: activity score 0 → PM; >0 and <1.25 → IM (i.e., 0.25 to 1.0); ≥1.25 and ≤2.25 → NM (i.e., 1.25 to 2.25); >2.25 → UM. An activity score of exactly 1.25 is therefore a Normal Metabolizer. The consensus also downgraded the `*10` allele's activity value from 0.5 to 0.25 and reassigned an activity score of exactly 1 from NM to IM [2, mechanism_review]. This standardization matters because, before it, different laboratories assigned different phenotypes to identical genotypes.

### Structural and copy-number variation (CYP2D6 in particular)

CYP2D6 is unusually complex: it sits next to two pseudogenes (CYP2D7, CYP2D8) and is subject to gene deletions (`*5`), whole-gene duplications and multiplications, and hybrid/fusion alleles arising from non-allelic homologous recombination. Gene multiplication of a functional allele is the principal mechanism of the ultrarapid phenotype — an individual may carry three, four, or more functional copies, dramatically increasing enzyme capacity [1, mechanism_review]. This copy-number variation is why CYP2D6 genotyping requires assays (e.g., copy-number quantification, long-read sequencing) beyond simple SNP panels, and why CYP2D6 star-allele calling is recognized as the most technically demanding of the major pharmacogenes.

The other principal pharmacogenes follow the same star-allele/diplotype logic: **CYP2C19** (clopidogrel, voriconazole, SSRIs, PPIs), where `*2` and `*3` are common no-function alleles and `*17` is a gain-of-function allele producing rapid/ultrarapid phenotypes; **CYP2C9** (warfarin, phenytoin, NSAIDs), where `*2` and `*3` reduce function; and **CYP3A4/CYP3A5**, where the common `*3` allele in CYP3A5 *abolishes* expression — so, counterintuitively, most people of European ancestry are CYP3A5 non-expressers, while many of African ancestry retain expression (relevant to tacrolimus dosing).

## 2. The Governance and Knowledge Framework

### CPIC and its level system

The **Clinical Pharmacogenetics Implementation Consortium (CPIC)** publishes peer-reviewed guidelines that translate an *already-available* genotype into a prescribing recommendation. CPIC explicitly does not advise *whether* to order a test; it answers "given this genotype result, what should the prescriber do?" CPIC assigns each gene-drug pair a level:

- **Level A** — genetic information *should* be used to change prescribing; the pair carries a strong or moderate recommendation.
- **Level B** — genetic information *could* be used to change prescribing; an optional recommendation, because alternative therapies or dosing are extremely likely to be as effective and safe.
- **Levels C and D** — no prescribing recommendation; evidence or actionability is insufficient [3, mechanism_review].

Within Level A/B guidelines, individual recommendations also carry a strength (strong / moderate / optional) reflecting evidence quality and the balance of benefits and harms.

### PharmGKB clinical-annotation levels of evidence (1A–4)

**PharmGKB** is the knowledgebase that curates the underlying literature. Its clinical annotations are scored on a six-tier scale defined in the Whirl-Carrillo evidence framework [4, mechanism_review]:

- **1A** — high evidence; the variant-drug combination has variant-specific prescribing guidance in a clinical guideline (e.g., CPIC) or an FDA-approved label.
- **1B** — high evidence supported by ≥2 independent publications, but without formal prescribing guidance.
- **2A** — moderate evidence; variant is in a PharmGKB tier-1 Very Important Pharmacogene (VIP), ≥2 publications.
- **2B** — moderate evidence; variant *not* in a tier-1 VIP, ≥2 publications.
- **3** — low evidence; single publication or conflicting results.
- **4** — the evidence does not support an association (negative total score) [4, mechanism_review].

The two systems are complementary: PharmGKB grades the evidence, CPIC converts high-grade evidence into actionable dosing language.

### The FDA tables

The FDA maintains two distinct resources. The **Table of Pharmacogenomic Biomarkers in Drug Labeling** (maintained by CDER) lists approved products whose labeling contains PGx information; importantly, only *some* of these labels prescribe a specific action, while others merely note an association [5, regulatory]. The separate **Table of Pharmacogenetic Associations** (maintained by CDRH) catalogs gene-drug associations the FDA considers established, in tiers reflecting whether the data support therapeutic management recommendations versus potential impact only. Analyses comparing the FDA Table of Pharmacogenetic Associations with CPIC guidelines find substantial overlap but also discordance in scope and the specificity of recommendations, reflecting the agencies' different evidentiary and regulatory mandates [6, mechanism_review]. A label appearing in an FDA table does not guarantee a CPIC Level A recommendation, and vice versa.

## 3. Load-Bearing Drug-Gene Pairs

### DPYD / fluoropyrimidines (5-FU, capecitabine)

Dihydropyrimidine dehydrogenase (DPD, encoded by *DPYD*) is the rate-limiting catabolic enzyme for fluoropyrimidines. Patients with reduced or absent DPD activity accumulate the drug, risking life-threatening or fatal toxicity (severe mucositis, myelosuppression, diarrhea). CPIC uses a *DPYD* gene activity score from 0 (no activity) to 2 (normal), built from four well-characterized variants — `*2A`, `*13`, c.2846A>T, and c.1236G>A/HapB3. No-function alleles (`*2A`, `*13`) score 0; decreased-function alleles score 0.5. CPIC recommends that patients with an activity score of 1 or 1.5 begin at ~50% of the standard dose with subsequent titration, and that score-0 patients (complete DPD deficiency) avoid fluoropyrimidines entirely [7, mechanism_review]. Prospective genotyping with pre-emptive dose reduction has been shown to bring the severe-toxicity rate in heterozygous carriers down toward that of non-carriers [7, mechanism_review].

### TPMT + NUDT15 / thiopurines (azathioprine, 6-mercaptopurine, thioguanine)

Thiopurine methyltransferase (TPMT) and NUDT15 jointly govern thiopurine metabolism; loss-of-function alleles in either gene reduce clearance of cytotoxic thioguanine nucleotides and predispose to severe, potentially fatal **myelosuppression** at standard doses [8, mechanism_review]. CPIC recommends substantial starting-dose reductions for intermediate metabolizers and dramatic reductions or alternative agents for poor metabolizers (e.g., for NUDT15 `*3/*3`, considering ~10 mg/m²/day mercaptopurine or an alternative) [8, mechanism_review]. The two genes are population-complementary: TPMT no-function alleles are more common in European and African populations, whereas NUDT15 loss-of-function alleles are common in East Asian and Hispanic populations — so testing only TPMT would miss a large share of at-risk patients of Asian ancestry [8, mechanism_review].

### VKORC1 + CYP2C9 / warfarin

Warfarin dosing is the archetypal multi-gene example. *VKORC1* encodes the drug's target (vitamin K epoxide reductase) and the promoter variant −1639G>A predicts sensitivity; *CYP2C9* governs clearance of the active S-warfarin enantiomer, with `*2` and `*3` reducing metabolism. Together with *CYP4F2* and the *CYP2C*-cluster variant rs12777823, plus non-genetic factors, common variants account for roughly 50% of warfarin dose variability [9, mechanism_review]. CPIC endorses genotype-guided dosing algorithms (e.g., warfarindosing.org / IWPC) to reach a target INR of 2–3, with recommendations specific to continental ancestry — CYP4F2`*3` modestly raises dose requirements in European/Asian ancestry, while rs12777823 reduces dose requirements in African ancestry [9, mechanism_review]. Warfarin illustrates that PGx is one input into an algorithm that still requires INR monitoring.

### SLCO1B1 / simvastatin

*SLCO1B1* encodes OATP1B1, a hepatic uptake transporter; the c.521T>C (rs4149056, p.V174A) decreased-function variant raises systemic statin exposure and **myopathy** risk. For 40 mg simvastatin, the relative risk of myopathy is ~2.6 per copy of the C allele; for 80 mg simvastatin the myopathy odds ratio is ~4.5 for TC and ~20 for CC genotypes [10, mechanism_review]. CPIC recommends a lower simvastatin dose or an alternative statin for C-allele carriers, with creatine-kinase surveillance [10, mechanism_review]. (Effect sizes are statin- and dose-specific; the strongest signal is for high-dose simvastatin.)

### UGT1A1 / irinotecan

UDP-glucuronosyltransferase 1A1 glucuronidates SN-38, irinotecan's active metabolite. The `*28` promoter allele (a TA-repeat insertion) reduces UGT1A1 expression; `*28/*28` homozygotes (poor metabolizers, ~10% of North American populations) clear SN-38 slowly and face markedly elevated risk of severe **neutropenia** and diarrhea, particularly at irinotecan doses ≥180 mg/m² [11, mechanism_review]. Genotype-guided dose reduction (e.g., an initial ~30% reduction in poor metabolizers) lowers the febrile-neutropenia rate while maintaining effective exposure [11, mechanism_review].

### CYP2C19 / clopidogrel (and SSRIs, PPIs); CYP2D6 / codeine, tramadol, tamoxifen, atomoxetine

**CYP2C19** bioactivates the prodrug clopidogrel. Poor and intermediate metabolizers (carrying `*2`/`*3` no-function alleles) generate less active metabolite, blunting platelet inhibition and raising the risk of major adverse cardiovascular events, including stent thrombosis, after PCI. For these patients the 2022 CPIC guideline recommends an alternative antiplatelet agent (prasugrel or ticagrelor, whose activity is CYP2C19-independent) absent a contraindication [12, mechanism_review]. CYP2C19 also influences SSRIs (e.g., citalopram/escitalopram dosing) and PPIs (where the relationship can be advantageous — poor metabolizers achieve higher PPI exposure and better acid suppression).

**CYP2D6** governs several therapeutically important conversions. For **codeine** and **tramadol**, CYP2D6 produces the active opioid (morphine; O-desmethyltramadol); *ultrarapid* metabolizers can generate toxic active-metabolite concentrations, with documented life-threatening or fatal respiratory depression — a landmark case described codeine intoxication in an ultrarapid metabolizer carrying extra functional gene copies, an event precipitated during an inflammatory illness (pneumonia) [13, open_label]. Conversely, *poor* metabolizers derive little analgesia. CPIC therefore recommends avoiding codeine and tramadol in both UMs and PMs and using a non-CYP2D6 opioid (e.g., morphine, hydromorphone) [14, mechanism_review]. For **tamoxifen**, CYP2D6 generates the active metabolite endoxifen, so PMs achieve lower endoxifen exposure; for **atomoxetine**, PMs have higher exposure and CPIC provides genotype-informed titration guidance.

## 4. The "PGx Informs, Never Authorizes" Principle (Load-Bearing)

Every recommendation above presupposes a **licensed prescriber acting within full clinical context.** A metabolizer phenotype is *one input* among many — drug-drug interactions, hepatic and renal function, the specific indication, comorbidity, age, adherence, and concurrent therapy all bear on the decision. A genotype result flags a conversation; it does not, by itself, authorize starting, stopping, or dose-adjusting any medication. CPIC's own framing is explicit on this: guidelines tell a clinician how to *interpret* a result that is already in hand, not whether the drug is appropriate for the patient [3, mechanism_review]. An AI agent must surface PGx-relevant flags as decision-support information for the prescriber and must never present metabolizer status as a directive to change therapy.

A second, technical reason this principle is non-negotiable is **phenoconversion** — the mismatch between genotype-predicted and actual metabolic capacity caused by non-genetic factors, such that genotype ≠ phenotype. Two mechanisms dominate:

- **Drug-induced phenoconversion**: a co-administered inhibitor (e.g., a strong CYP2D6 inhibitor like paroxetine or bupropion) can convert a genotypic normal metabolizer into a phenotypic poor metabolizer, abolishing codeine analgesia or raising tamoxifen-pathway risk despite a "normal" genotype [15, mechanism_review].
- **Inflammation-induced phenoconversion**: pro-inflammatory cytokines — IL-6 prominent among them — down-regulate multiple CYPs (CYP1A2, CYP2B6, CYP2C8/9/19, CYP2D6, CYP3A4) and phase-II enzymes/transporters during infection, cancer, autoimmune flare, or liver disease, transiently converting genotypic normal metabolizers into functional poor metabolizers [15, mechanism_review]. (Notably, the codeine-intoxication case in [13, open_label] occurred during pneumonia, consistent with this mechanism amplifying an already-ultrarapid genotype.)

Because phenoconversion is common — inflammatory states are highly prevalent — a static genotype can over- or under-predict real-time metabolism. This is precisely why genotype is a flag, not a verdict, and why interpretation belongs to a clinician who can integrate the patient's current drug list and inflammatory state. Stated plainly: PGx narrows the differential of *why* a patient may respond unusually; it does not replace clinical judgment, therapeutic monitoring, or the prescriber's authority.

## Bibliography

[1] Gaedigk A, Ingelman-Sundberg M, Miller NA, Leeder JS, Whirl-Carrillo M, Klein TE; PharmVar Steering Committee. The Pharmacogene Variation (PharmVar) Consortium: Incorporation of the Human Cytochrome P450 (CYP) Allele Nomenclature Database. Clin Pharmacol Ther. 2018;103(3):399-401. PMID: 29134625. DOI: 10.1002/cpt.910. [mechanism_review]

[2] Caudle KE, Sangkuhl K, Whirl-Carrillo M, et al. Standardizing CYP2D6 Genotype to Phenotype Translation: Consensus Recommendations from the CPIC and DPWG. Clin Transl Sci. 2020;13(1):116-124. PMID: 31647186. DOI: 10.1111/cts.12692. [mechanism_review]

[3] Relling MV, Klein TE, Gammal RS, Whirl-Carrillo M, Hoffman JM, Caudle KE. The Clinical Pharmacogenetics Implementation Consortium: 10 Years Later. Clin Pharmacol Ther. 2020;107(1):171-175. PMID: 31562822. DOI: 10.1002/cpt.1651. [mechanism_review]

[4] Whirl-Carrillo M, Huddart R, Gong L, Sangkuhl K, Thorn CF, Whaley R, Klein TE. An Evidence-Based Framework for Evaluating Pharmacogenomics Knowledge for Personalized Medicine. Clin Pharmacol Ther. 2021;110(3):563-572. PMID: 34216021. DOI: 10.1002/cpt.2350. [mechanism_review]

[5] U.S. Food and Drug Administration. Table of Pharmacogenomic Biomarkers in Drug Labeling. https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling [regulatory]

[6] Pritchard D, Patel JN, Stephens LE, McLeod HL. Comparison of FDA Table of Pharmacogenetic Associations and Clinical Pharmacogenetics Implementation Consortium guidelines. Am J Health Syst Pharm. 2022;79(12):993-1005. PMID: 35230418. DOI: 10.1093/ajhp/zxac064. PMC9171570. [mechanism_review]

[7] Amstutz U, Henricks LM, Offer SM, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) Guideline for Dihydropyrimidine Dehydrogenase Genotype and Fluoropyrimidine Dosing: 2017 Update. Clin Pharmacol Ther. 2018;103(2):210-216. PMID: 29152729. DOI: 10.1002/cpt.911. PMC5760397. [mechanism_review]

[8] Relling MV, Schwab M, Whirl-Carrillo M, et al. Clinical Pharmacogenetics Implementation Consortium Guideline for Thiopurine Dosing Based on TPMT and NUDT15 Genotypes: 2018 Update. Clin Pharmacol Ther. 2019;105(5):1095-1105. PMID: 30447069. DOI: 10.1002/cpt.1304. PMC6576267. [mechanism_review]

[9] Johnson JA, Caudle KE, Gong L, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) Guideline for Pharmacogenetics-Guided Warfarin Dosing: 2017 Update. Clin Pharmacol Ther. 2017;102(3):397-404. PMID: 28198005. DOI: 10.1002/cpt.668. PMC5546947. [mechanism_review]

[10] Wilke RA, Ramsey LB, Johnson SG, et al. The Clinical Pharmacogenomics Implementation Consortium: CPIC Guideline for SLCO1B1 and Simvastatin-Induced Myopathy. Clin Pharmacol Ther. 2012;92(1):112-117. PMID: 22617227. DOI: 10.1038/clpt.2012.57. PMC3384438. [mechanism_review]

[11] Dean L. Irinotecan Therapy and UGT1A1 Genotype. In: Medical Genetics Summaries. Bethesda (MD): National Center for Biotechnology Information; 2015. NBK294473. https://www.ncbi.nlm.nih.gov/books/NBK294473/ [mechanism_review]

[12] Lee CR, Luzum JA, Sangkuhl K, et al. Clinical Pharmacogenetics Implementation Consortium Guideline for CYP2C19 Genotype and Clopidogrel Therapy: 2022 Update. Clin Pharmacol Ther. 2022;112(5):959-967. PMID: 35034351. DOI: 10.1002/cpt.2526. PMC9287492. [mechanism_review]

[13] Gasche Y, Daali Y, Fathi M, et al. Codeine intoxication associated with ultrarapid CYP2D6 metabolism. N Engl J Med. 2004;351(27):2827-2831. PMID: 15625333. DOI: 10.1056/NEJMoa041888. [open_label]

[14] Crews KR, Gaedigk A, Dunnenberger HM, et al. Clinical Pharmacogenetics Implementation Consortium (CPIC) Guidelines for Codeine Therapy in the Context of Cytochrome P450 2D6 (CYP2D6) Genotype. Clin Pharmacol Ther. 2012;91(2):321-326. DOI: 10.1038/clpt.2011.287. PMID: 22205192. [mechanism_review]

[15] Shah RR, Smith RL. Inflammation-induced phenoconversion of polymorphic drug metabolizing enzymes: hypothesis with implications for personalized medicine. Drug Metab Dispos. 2015;43(3):400-410. PMID: 25519488. DOI: 10.1124/dmd.114.061093. [mechanism_review]
