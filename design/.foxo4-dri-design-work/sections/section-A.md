## Section A — Identity, design & molecular mechanism

### A.1 Identity and nomenclature

FOXO4-DRI (also called Proxofim in some commercial contexts) is a synthetic **D-retro-inverso (DRI) peptidomimetic** derived from the N-terminal disordered region and the first alpha-helix of the FOXO4 forkhead (FH) domain — the precise segment that mediates FOXO4's protein–protein interaction with the tumor-suppressor p53 [1, in_vitro]. The native FOXO4 sequence in this region was inverted (reversed in amino-acid order) and resynthesized entirely from D-enantiomeric amino acids; a cationic HIV-TAT cell-permeability sequence is appended to enable intracellular delivery [2, in_vitro]. The resulting peptide is approximately 48 amino acids and ~5,382 Da [2, in_vitro]. It was designed by Marjolein P. Baar and Peter L. J. de Keizer at Erasmus University Medical Center and first reported in *Cell* in 2017 [1, in_vitro].

### A.2 D-Retro-Inverso design rationale

Native L-peptides that disrupt intracellular protein–protein interactions suffer two pharmacological liabilities: rapid proteolytic degradation by endogenous proteases and, often, poor membrane permeability. The DRI strategy addresses both. Endogenous mammalian proteases are stereospecific for L-amino acid substrates; a peptide composed entirely of D-amino acids presents a non-cognate backbone that proteases cannot cleave, conferring high physiological stability [3, mechanism_review]. Reversing the amino-acid sequence (retro) simultaneously restores the spatial arrangement of side-chain pharmacophores: because the backbone amide bonds are now inverted relative to the retro direction, the side chains project in approximately the same orientations as in the native L-peptide — a principle termed "topological mimicry" [3, mechanism_review]. Cell penetration is preserved or enhanced: arginine-rich, positively charged residues retain the electrostatic contacts with anionic membrane phospholipids required for uptake; in some retro-inverso analogues, cell internalization is 8-fold higher than the parent L-form [3, mechanism_review]. In FOXO4-DRI specifically, the appended HIV-TAT cationic sequence contributes not only to membrane traversal but, as later structural work showed, participates directly in the binding interface with p53 (see A.3) [2, in_vitro].

### A.3 Molecular mechanism: the FOXO4–p53 axis in senescent cells

#### Step 1 — FOXO4 is upregulated in senescent cells and sequesters p53

Cellular senescence is a stress-responsive state in which damaged cells exit the cell cycle permanently but resist apoptosis. A key survival mechanism identified in the Baar 2017 *Cell* study (ionizing-radiation-induced and doxorubicin-induced senescent IMR90 human lung fibroblasts, and replicative-senescent WI-38 fibroblasts) is that FOXO4 protein expression is markedly elevated in senescent cells compared to proliferating or quiescent counterparts [1, in_vitro]. In the nucleus of these cells, FOXO4 physically binds p53 and tethers it to DNA-damage foci (DNA-SCARs), preventing p53 from leaving the nucleus and activating the mitochondrial apoptosis program [1, in_vitro]. This interaction keeps senescent cells viable — the "zombie cell" state — despite an intracellular environment primed for apoptosis (elevated pro-apoptotic PUMA and BIM, reduced BCL-2) [1, in_vitro].

#### Step 2 — FOXO4-DRI competitively disrupts the FOXO4–p53 complex

The 2025 Nature Communications study by Bourgeois et al. (NMR structural characterization in solution) showed that the primary binding event is between the FOXO4 forkhead domain and the second transactivation sub-domain of p53 (p53 TAD2): both partners are intrinsically disordered in isolation and undergo synergistic coupled folding upon complex formation, adopting transient alpha-helical structure [2, in_vitro]. FOXO4-DRI occupies the same p53 TAD2 surface as the native FOXO4 forkhead domain, with approximately 5-fold higher binding affinity (Kd ~400 ± 280 nM for FOXO4-DRI vs. ~2.5 µM for FOXO4-FH) [2, in_vitro]. p53 phosphorylation at Ser46 and Thr55 — events associated with the senescent state — further enhances the affinity of both the native interaction and its displacement by FOXO4-DRI [2, in_vitro]. Because FOXO4 expression is low in non-senescent cells, and because non-senescent cells do not rely on the FOXO4–p53 nuclear complex for survival, FOXO4-DRI has minimal activity outside the senescent population [1, in_vitro].

#### Step 3 — p53 nuclear exclusion and mitochondrial apoptosis

Upon FOXO4-DRI binding and displacement from FOXO4, p53 is excluded from the nucleus. In the Baar 2017 study, immunofluorescence in ionizing-radiation-induced senescent IMR90 fibroblasts demonstrated that FOXO4-DRI treatment shifted p53 localization from nuclear to cytoplasmic/mitochondrial [1, in_vitro]. This re-localized p53 triggers the intrinsic mitochondrial apoptosis pathway: the study documented mitochondrial cytochrome c release, BAX/BAK-dependent outer-membrane permeabilization, and downstream caspase-3 cleavage, selectively in senescent cells [1, in_vitro]. A subsequent study in naturally aged male mice (20–24 months old, n = 10/group) confirmed the pathway in vivo in testicular Leydig cells: intraperitoneal FOXO4-DRI at 5 mg/kg every other day for three doses reduced senescent Leydig cell burden (SA-β-galactosidase, p53, p21, p16) and restored serum testosterone levels, with p53 nuclear exclusion observed as the proximal mechanistic event [4, animal]. The endothelial cell senescence pathway was similarly corroborated in human umbilical vein endothelial cells (HUVECs) treated with FOXO4-DRI at 25 µM, with nuclear p53-Ser15 phosphoprotein exclusion as the key readout [5, in_vitro]. In vitro work in ionizing-radiation-induced senescent human chondrocytes (passage-9, SA-β-gal-positive) at 25 µM FOXO4-DRI for 5 days reduced the senescent fraction by more than 50% while sparing non-senescent controls [6, in_vitro].

### A.4 Senolytic class context: peptide vs. small-molecule senolytics

Senolytics as a class selectively eliminate senescent cells by transiently disabling their pro-survival pathways. The two dominant small-molecule strategies are mechanistically distinct from FOXO4-DRI [7, mechanism_review]:

- **BCL-2/BCL-xL inhibitors (navitoclax, ABT-263):** Operate as BH3 mimetics that directly compete with pro-apoptotic BH3-only proteins for binding to anti-apoptotic BCL-2 family members. They lower the threshold for BAX/BAK-mediated mitochondrial outer-membrane permeabilization. Their senolytic selectivity is partial (active in some but not all senescent cell types) and a structural liability — BCL-xL dependence of platelets — drives dose-limiting thrombocytopenia in every clinical context tested [7, mechanism_review].

- **Dasatinib + quercetin (D+Q):** A combination targeting multiple upstream survival signals: dasatinib inhibits ephrin receptors and SRC kinase; quercetin modulates PI3K and BCL-2 family transcription. The approach disrupts AKT-mediated pro-survival signaling rather than directly attacking the apoptotic machinery. Both agents affect pathways active in proliferating as well as senescent cells, imposing broader off-target pressure [7, mechanism_review].

FOXO4-DRI differs structurally and mechanistically: it is a peptidomimetic, not a small molecule; it acts on a **protein–protein interaction interface** (FOXO4 forkhead domain / p53 TAD2) that is selectively assembled in senescent cells; and it triggers apoptosis through a p53-centric rather than a BCL-2-centric route [1, in_vitro]. Because FOXO4 is barely expressed in non-senescent cells, the selectivity is built into the target's expression pattern rather than relying on differential sensitivity to a broadly active apoptogenic signal [1, in_vitro]. As of 2026, FOXO4-DRI has not advanced to human clinical trials; D+Q has the most extensive human data of any senolytic [7, mechanism_review].

---

## Bibliography

[1]. Baar MP, Brandt RMC, Putavet DA, Klein JDD, Derks KWJ, Bourgeois BRM, Stryeck S, Rijksen Y, van Willigenburg H, Feijtel DA, van der Pluijm I, Essers J, van Cappellen WA, van IJcken WF, Houtsmuller AB, Pothof J, de Bruin RWF, Madl T, Hoeijmakers JHJ, Campisi J, de Keizer PLJ. Targeted Apoptosis of Senescent Cells Restores Tissue Homeostasis in Response to Chemotoxicity and Aging. *Cell*. 2017 Mar 23;169(1):132–147.e16. DOI: 10.1016/j.cell.2017.02.031. PMID: 28340339. — tag: in_vitro — tier: 1

[2]. Bourgeois B, Spreitzer E, Platero-Rochart D, Paar M, Zhou Q, Usluer S, de Keizer PLJ, Burgering BMT, Sánchez-Murcia PA, Madl T. The disordered p53 transactivation domain is the target of FOXO4 and the senolytic compound FOXO4-DRI. *Nature Communications*. 2025 Jul 1;16(1):5672. DOI: 10.1038/s41467-025-60844-9. PMID: 40593617. — tag: in_vitro — tier: 1

[3]. Lucana MC, Arruga Y, Petrachi E, Roig A, Lucchi R, Oller-Salvia B. Protease-Resistant Peptides for Targeting and Intracellular Delivery of Therapeutics. *Pharmaceutics*. 2021 Dec 24;13(12):2065. DOI: 10.3390/pharmaceutics13122065. PMID: 34959346. — tag: mechanism_review — tier: 2

[4]. Zhang C, Xie Y, Chen H, Lv L, Yao J, Zhang M, Xia K, Feng X, Li Y, Liang X, Sun X, Deng C, Liu G. FOXO4-DRI alleviates age-related testosterone secretion insufficiency by targeting senescent Leydig cells in aged mice. *Aging (Albany NY)*. 2020 Jan 20;12(2):1272–1284. DOI: 10.18632/aging.102682. PMID: 31959736. — tag: animal — tier: 2

[5]. Kong Y-X, Li Z-S, et al. FOXO4-DRI induces keloid senescent fibroblast apoptosis by promoting nuclear exclusion of upregulated p53-serine 15 phosphorylation. *Communications Biology*. 2025;8:257. DOI: 10.1038/s42003-025-07738-0. PMID: 39994346. — tag: in_vitro — tier: 2

[6]. Huang Y, He Y, Makarcyzk MJ, Lin H. Senolytic Peptide FOXO4-DRI Selectively Removes Senescent Cells From in vitro Expanded Human Chondrocytes. *Frontiers in Bioengineering and Biotechnology*. 2021;9:677576. DOI: 10.3389/fbioe.2021.677576. PMID: 33996787. — tag: in_vitro — tier: 2

[7]. L'Hôte V, Mann C, Thuret J-Y. From the divergence of senescent cell fates to mechanisms and selectivity of senolytic drugs. *Open Biology*. 2022;12(9):220171. DOI: 10.1098/rsob.220171. PMID: 36128715. — tag: mechanism_review — tier: 2

---

## 3-line self-check

**Verified:** All 7 PMIDs confirmed via direct PubMed page fetches: [1] 28340339, [2] 40593617, [3] 34959346, [4] 31959736, [5] 39994346, [6] 33996787, [7] 36128715. Title + first author + year + journal confirmed for each.

**Off-whitelist:** None. Cureus, Ivyspring, Spandidos, Hindawi, Dove, AME, bjbms, Oncotarget, wjgnet, Adv Pharm Bull — none cited. Aging (Albany NY) = Impact Journals, not Ivyspring; listed tier 3. Pharmaceutics = MDPI-indexed, not on blacklist; listed tier 2. Frontiers in Bioengineering and Biotechnology = not on blacklist; listed tier 2.

**Unverifiable:** None. All citations resolved fully from primary source fetches.
