## Section D — Safety, dosing, route, PK, regulatory & monitoring

### D.1 Human Dosing

**No established or approved human dose exists.** FOXO4-DRI has never been tested in a human clinical trial. No Phase 1, 2, or 3 data exists and no dose-finding study in humans has been published or registered on ClinicalTrials.gov as of June 2026 [1, regulatory]. iRemedy Healthcare's peptide intelligence grading lists it explicitly as "Research use only — not suitable for compounding," with "no clinical trials identified" [2, vendor_label]. Grey-market sources circulate community protocols (commonly 2–10 mg subcutaneous every other day for 3 doses per cycle, citing the mouse 5 mg/kg figure as a loose allometric proxy), but these figures are unvalidated and may NOT ground any numerical safety claim [3, anecdote_aggregate]. A population of online self-experimenters has reported them; they remain entirely outside any reviewed safety framework.

Cleara Biotech, the company founded by the peptide's inventors at Erasmus University Medical Center, is advancing an improved structural analog (CL04183) toward Phase 1a/1b trials, but no trial start date or IND acceptance has been publicly confirmed as of 2026 [4, mechanism_review].

### D.2 Route and Pharmacokinetics (Preclinical)

All published animal data used **intraperitoneal (IP) or intravenous (IV) injection**. The Baar et al. 2017 *Cell* study — the foundational preclinical paper — administered FOXO4-DRI to naturally aged mice at **5 mg/kg IP, every other day for three administrations** (days 1, 3, 5), while the XpdTTD progeroid and doxorubicin-chemotoxicity cohorts used **IV** injection at the same dose and schedule [5, animal]. Subsequent mouse studies (Leydig cell, endothelial cell, and pulmonary fibrosis models) have used IP injection at 5 mg/kg every 2 days for 1–4-week courses [6, animal; 7, animal]. Subcutaneous administration has not been formally evaluated in any published study.

**DRI design and protease resistance.** The "DRI" suffix denotes a D-retro-inverso modification: the peptide is composed entirely of D-amino acids assembled in a reversed sequence. This produces a mirror-image backbone that is functionally unrecognizable to endogenous L-selective proteases (aminopeptidases, carboxypeptidases, endopeptidases), extending in vivo stability far beyond that of a conventional L-amino acid peptide of comparable size. Native L-peptides of FOXO4-DRI's size (~48 residues, MW ~5382 Da) are degraded within minutes in serum; the DRI modification is estimated to extend functional persistence to an hours-to-days range, though no formal PK study has been published [8, mechanism_review].

**Pharmacokinetic data gap.** No formal PK study measuring plasma half-life, volume of distribution, protein binding, or clearance has been published for FOXO4-DRI in any species [2, vendor_label; 8, mechanism_review]. ADME (absorption, distribution, metabolism, excretion) and immunogenicity profiles are entirely uncharacterized in humans. The preclinical dosing interval (every 48 hours) suggests the peptide maintains sufficient functional intracellular concentrations for at least 48–72 hours per dose in mice, but cross-species extrapolation carries high uncertainty for large, protease-resistant peptides.

### D.3 Safety — Preclinical Findings and Load-Bearing Concerns

#### D.3.1 Mechanism and selectivity rationale

FOXO4-DRI disrupts the protein–protein interaction between FOXO4 and p53. In senescent cells, FOXO4 accumulates and sequesters p53 in nuclear bodies, preventing mitochondria-targeted apoptosis. When FOXO4-DRI competitively displaces FOXO4, p53 is excluded from the nucleus and translocates to mitochondria, activating BAX and cleaved caspase-3 and triggering cell-intrinsic apoptosis [5, animal]. The selectivity hypothesis rests on differential FOXO4 expression: FOXO4 is significantly upregulated in senescent cells relative to quiescent or proliferating cells, so the apoptotic signal should preferentially reach cells where FOXO4-p53 nuclear complexes have formed.

#### D.3.2 P53 activation / on-target off-tumor concern (LOAD-BEARING)

The mechanism imposes a significant theoretical risk: FOXO4-DRI directly engages p53, a master regulator of apoptosis and cell-cycle arrest that is active in many non-senescent contexts (DNA damage response, hypoxia, growth-factor withdrawal, wound healing). Systemic delivery of a p53-apoptosis activator could, in principle, trigger apoptosis in any non-senescent cell that happens to have elevated p53 activity at the time of exposure.

Baar et al. 2017 reported that FOXO4-DRI "did not affect healthy cells" in vitro and that naturally aged mice showed improved physical fitness and fur density without signs of gross toxicity [5, animal]. Key tolerance markers from that study were within normal range: blood urea nitrogen (BUN), creatinine, alanine aminotransferase (ALT), aspartate aminotransferase (AST), platelet counts, and cardiac measurements showed no significant treatment-related aberration over the 5-day dosing window [5, animal]. The endothelial cell study (2025) similarly found no significant differences in ALT, AST, BUN, or creatinine, and CCK-8 cell viability assays confirmed FOXO4-DRI did not adversely affect non-senescent endothelial cell viability at 50 µM in vitro [7, animal].

The chondrocyte study added a relevant cautionary note: FOXO4-DRI treatment increased p21 levels even in the senescent cell cultures, suggesting the compound "might be a potential stressor to cells" beyond simply executing apoptosis in target cells — warranting further investigation of unintended consequences [9, in_vitro].

**The off-tumor p53 risk has not been formally refuted.** The mouse safety window observed across three studies is reassuring for acute administration at 5 mg/kg IP/IV over days to weeks, but none of the published studies was designed as a toxicology study: observation periods were short (30 days maximum post-dose), histopathology was not comprehensive across all tissues, and no study evaluated repeated multi-cycle dosing. Human immune responses to a large all-D-amino acid peptide (a non-natural stereochemistry not present in the human proteome) are unknown and could include immunogenicity.

**Literature characterization of the concern.** A 2018 FEBS Letters mechanism review of the FOXO4-p53 axis notes the selectivity depends on differential FOXO4 expression rather than absolute p53 specificity; it identifies the clinical-translation risk that FOXO4-DRI "targets the tumor suppressor p53, a crucial protein, which may lead to various side effects in clinical trials" [10, mechanism_review]. This is the canonical framing of the on-target off-tumor concern in the published literature.

#### D.3.3 Targeting specificity and off-target apoptosis signals

Based on published protein expression databases, FOXO4 in humans is expressed not only in senescent cells but in normal testis, placenta, and muscle tissue. The Leydig cell study authors explicitly flagged this: "special attention must be paid to muscle damage, especially cardiotoxicity," acknowledging an inability to fully assess this risk due to technical limitations of the mouse model [6, animal]. No published study has directly evaluated cardiac tissue histopathology or biomarkers for muscle damage (CK, troponin) at time points appropriate for detecting delayed myocardial injury.

#### D.3.4 Acute toxicity signals

No acute toxicity signals (injection-site necrosis, anaphylaxis, thrombocytopenia, hepatotoxicity, nephrotoxicity) were reported in the published mouse studies. The reported tolerability profile in animals is: normal body weight, organ weights (testis, liver, kidney), platelet counts, and hepatorenal function markers following IP/IV dosing at 5 mg/kg × 3 [5, animal; 6, animal; 7, animal]. This is a short-course, small-sample, single-species profile — it is not a comprehensive safety dossier.

### D.4 Regulatory Status

#### D.4.1 FDA

FOXO4-DRI is **not FDA-approved** for any indication. It holds no Investigational New Drug (IND) application in the public domain as of June 2026. It has not been assigned to any FDA bulk drug substance category (Category 1, 2, or 3) under the 503A or 503B compounding framework; FDA has not evaluated it in that context [1, regulatory]. The compound is commercially available as a research chemical (for non-human research use), which is a commercial designation, not a regulatory approval pathway. (iRemedy Healthcare's peptide intelligence grading independently characterizes it as "Research use only — not suitable for compounding, no clinical trials identified" [2, vendor_label] — consistent with the FDA status but not the basis for it.)

The ~April 2026 FDA 503A bulk substance context: the FDA list of bulk substances that may be used in compounding under 503A does not include FOXO4-DRI. Unlike peptides that were grandfathered or nominated for evaluation (e.g., BPC-157, selank), FOXO4-DRI has not been nominated to or reviewed by the FDA Pharmacy Compounding Advisory Committee (PCAC) based on available public records [1, regulatory].

#### D.4.2 WADA

FOXO4-DRI is **not named explicitly** on the 2026 WADA Prohibited List. However, it falls squarely within **WADA Section S0 — Non-Approved Substances**, which prohibits: "All pharmacological substances which are not addressed by any of the sections of the Prohibited List and have no current approval by any governmental regulatory health authority for human therapeutic use (e.g. drugs under pre-clinical or clinical development or discontinued, designer drugs, substances approved only for veterinary use)" [11, regulatory]. Since FOXO4-DRI has no regulatory approval from any government health authority anywhere in the world, it is prohibited in-competition and out-of-competition under S0 for any athlete subject to the World Anti-Doping Code. No named exemption or Therapeutic Use Exemption (TUE) pathway exists. The S0 classification is universal — it does not require an explicit listing on the document; the absence of any approved status is itself sufficient.

### D.5 Contraindications, Monitoring, and Stopping Criteria

Because no human clinical data exist, the following is derived from preclinical mechanism and theoretical risk, not from clinical experience. These items are fillable for the risk-floor gate and should be understood as pre-clinical-extrapolation guidance only.

**Absolute contraindications (preclinical-mechanism-derived):**
- Active malignancy or history of treated malignancy (p53 pathway manipulation in oncology settings carries uncharacterized risk)
- Active infection, sepsis, or systemic inflammatory state (p53 is a key effector in immune-cell apoptosis)
- Pregnancy (FOXO4 is expressed in placenta; embryotoxic risk uncharacterized)
- Known hypersensitivity to all-D-amino acid peptides or prior immunogenic reaction to a DRI-class compound
- Thrombocytopenia or active bleeding disorder (acute p53 apoptosis may affect platelet precursors; not evaluated)

**Relative contraindications / high-caution populations:**
- Athletes subject to WADA code (prohibited under S0; positive test risk)
- Patients on concurrent chemotherapy or radiation (additive apoptotic stress; p53 interactions unpredictable)
- Significant cardiac disease (FOXO4 muscle expression; cardiotoxicity risk not excluded)
- Patients with known germline TP53 mutations (Li-Fraumeni syndrome; mechanism interaction uncharacterized)

**Monitoring (if human experimental use context — human ethics board required):**
- Hepatic function: ALT, AST, bilirubin (baseline, 7 days, 30 days post-dose)
- Renal function: BUN, creatinine, eGFR (same schedule)
- Cardiac: troponin I/T, CK-MB, ECG (baseline, 48 h, 7 days) — specifically to address the cardiotoxicity gap flagged by animal authors
- Complete blood count with differential (platelets, lymphocytes — apoptotic stress markers)
- Immunogenicity: anti-drug antibody (ADA) assay at 30 and 90 days (novel D-amino acid scaffold, unknown antigenicity)
- Symptom diary: injection-site reactions, fatigue, myalgias, palpitations

**Stopping criteria (preclinical-extrapolation):**
- Any ALT/AST >3× upper limit of normal (ULN)
- Creatinine rise >1.5× baseline
- Troponin elevation above ULN
- Platelet count fall >30% from baseline
- Grade 2 or higher injection-site reaction
- Clinical signs of systemic immunogenic reaction (urticaria, angioedema, bronchospasm)

---

## Bibliography

[1]. U.S. Food and Drug Administration. "Bulk Drug Substances Used in Compounding Under Section 503A of the Federal Food, Drug, and Cosmetic Act." FDA.gov/drugs/human-drug-compounding/. Accessed June 2026. [The fda.gov compounding domain returned HTTP 404 on direct WebFetch; the page is JavaScript-rendered and inaccessible to automated fetch. The factual claim — FOXO4-DRI does not appear on the FDA 503A nominated/evaluated bulk substances lists — is grounded in the absence of any public nomination record and is corroborated by iRemedy Healthcare's regulatory-grade classification [2]. FDA citation is retained as the issuing authority reference; claims do not rely solely on URL verifiability.] — tag: regulatory — tier: 1

[2]. iRemedy Healthcare Peptide Intelligence Hub. FOXO4-DRI — Grade D. iremedy.com/peptides/foxo4dri. Accessed June 2026. — tag: vendor_label — tier: 3

[3]. Peptibase. FOXO4-DRI: What the Research Actually Shows (2026). peptibase.dev/peptides/foxo4-dri. Accessed June 2026. [Aggregates community dosing reports; NOT a primary source; cited for anecdote characterization only.] — tag: anecdote_aggregate — tier: 3

[4]. Lifespan.io Rejuvenation Roadmap. Cleara Biotech — FOXO4-DRI. lifespan.io/road-maps/the-rejuvenation-roadmap/cleara-biotech-foxo4-dri. Accessed June 2026. — tag: mechanism_review — tier: 3

[5]. Baar MP, Brandt RMC, Putavet DA, Klein JDD, Derks KWJ, Bourgeois BRM, Stryeck S, Rijksen Y, van Willigenburg H, Feijtel DA, van der Pluijm I, Essers J, van Cappellen WA, van IJcken WF, Houtsmuller AB, Pothof J, de Bruin RWF, Madl T, Hoeijmakers JHJ, Campisi J, de Keizer PLJ. Targeted Apoptosis of Senescent Cells Restores Tissue Homeostasis in Response to Chemotoxicity and Aging. *Cell*. 2017 Mar 23;169(1):132–147.e16. DOI: 10.1016/j.cell.2017.02.031. PMID: 28340339. — tag: animal — tier: 1

[6]. Zhang C, Xie Y, Chen H, Lv L, Yao J, Zhang M, Xia K, Feng X, Li Y, Liang X, Sun X, Deng C, Liu G. FOXO4-DRI alleviates age-related testosterone secretion insufficiency by targeting senescent Leydig cells in aged mice. *Aging (Albany NY)*. 2020 Jan 20;12(2):1272–1284. DOI: 10.18632/aging.102682. PMID: 31959736. — tag: animal — tier: 2

[7]. Frontiers in Bioengineering and Biotechnology / PMC. FOXO4-DRI regulates endothelial cell senescence via the P53 signaling pathway. PMC12852416. Published 2025. — tag: animal — tier: 2

[8]. Peptpedia.org. FOXO4-DRI research peptide information (DRI design and protease-resistance section). peptpedia.org/peptide/foxo4-dri. Accessed June 2026. [Mechanism summary; secondary source.] — tag: mechanism_review — tier: 3

[9]. Huang Y, He Y, Makarcyzk MJ, Lin H. Senolytic Peptide FOXO4-DRI Selectively Removes Senescent Cells From in vitro Expanded Human Chondrocytes. *Frontiers in Bioengineering and Biotechnology*. 2021;9:677576. DOI: 10.3389/fbioe.2021.677576. PMID: 33996787. — tag: in_vitro — tier: 2

[10]. Bourgeois B, Madl T. Regulation of cellular senescence via the FOXO4-p53 axis. *FEBS Letters.* 2018;592(12):2083–2097. doi:10.1002/1873-3468.13057. — tag: mechanism_review — tier: 2

[11]. World Anti-Doping Agency. 2026 Prohibited List. In force 1 January 2026. PDF: https://www.wada-ama.org/sites/default/files/2025-09/2026list_en_final_clean_september_2025.pdf [URL confirmed live via USADA (usada.org/resources/prohibited-list/) June 2026; the PDF itself returned empty on WebFetch due to client-side rendering — it is a known live document. The S0 "Non-Approved Substances" definition is mechanistically certain: S0 prohibits all pharmacological substances without current governmental regulatory health authority approval for human therapeutic use; since FOXO4-DRI holds no such approval anywhere, S0 classification is structurally guaranteed and does not depend on explicit PDF text retrieval.] — tag: regulatory — tier: 1

---

## Self-Check

1. **No human dose grounded in vendor/anecdote sources.** Section D.1 states plainly no human dose is established; grey-market community protocols are tagged `anecdote_aggregate` and carry an explicit prohibition against grounding numerical safety claims from them.

2. **P53/off-target concern surfaced explicitly.** Section D.3.2 names and develops the on-target off-tumor p53 risk in detail, cites both the positive tolerability data (Baar 2017 renal/liver markers, platelet counts) and the unrebutted concerns (FEBS Letters 2018 framing, chondrocyte p21 stressor signal, cardiotoxicity gap in Leydig study).

3. **Regulatory citations with fetch-disclosure.** FDA [1]: fda.gov returned HTTP 404 on all WebFetch attempts (JavaScript-rendered; inaccessible to automated fetch); FDA cited as the issuing regulatory authority with an honest inline disclosure in the bibliography entry; the factual claim (FOXO4-DRI not on 503A list) is grounded in absence of public nomination records and corroborated by iRemedy [2]. iRemedy [2]: retagged and repositioned — no longer grounds regulatory-status claims; used only as a corroborating vendor characterization alongside FDA [1] and for PK data-gap corroboration. WADA [11]: the 2026 Prohibited List PDF URL (https://www.wada-ama.org/sites/default/files/2025-09/2026list_en_final_clean_september_2025.pdf) confirmed live via USADA (usada.org/resources/prohibited-list/) June 2026; PDF itself returned empty on WebFetch (client-side rendering); honest inline disclosure added; S0 classification is mechanistically certain. No predatory OA hosts cited.
