## Section A — Identity, discovery & molecular mechanism

### A.1 Identity and molecular structure

Humanin (HN) is a 24-amino-acid mitochondrial-derived peptide (MDP) with the sequence **MAPRGFSCLLLLTSEIDLPVKRRA** [1, mechanism_review]. It was the first MDP discovered — preceding MOTS-c (MT-RNR1 / 12S rRNA) and the small humanin-like peptides (SHLPs 1–6). Humanin is encoded by a short open reading frame (ORF) embedded within the **MT-RNR2 gene** (16S mitochondrial rRNA gene) of the mitochondrial genome [1, mechanism_review].

**Cytoplasmic vs. mitochondrial translation.** The humanin ORF is transcribed from mtDNA but the peptide is also produced via cytoplasmic (nuclear-encoded) ribosomes. The founding cDNA was isolated from a human brain library (occipital lobe of an Alzheimer's patient), making its cellular origin initially ambiguous; subsequent work confirmed that both mitochondrial and cytosolic ribosomes can translate the humanin ORF [1, mechanism_review] [6, in_vitro].

**Nuclear-encoded paralogs (MTRNR2L1–13).** Thirteen humanin-like nuclear pseudogenes — designated MTRNR2L1 through MTRNR2L13 — have been identified in the human nuclear genome and share 92–95% amino-acid identity with mitochondrial humanin. Several (e.g., MTRNR2L2, MTRNR2L4) encode isoforms with four additional C-terminal residues and may produce functional peptides [6, in_vitro]. These paralogs are a potential confound in expression studies: transcripts attributed to MT-RNR2 can include nuclear-derived copies. No MTRNR2L isoform has undergone the same depth of mechanistic characterization as the original mtDNA-encoded humanin.

### A.2 Discovery

Humanin was identified in 2001 by Hashimoto, Nishimoto and colleagues using a functional "death-trap" screen of a cDNA library constructed from surviving neurons in the occipital lobe of an Alzheimer's disease (AD) patient brain [2, in_vitro]. The screen sought factors capable of blocking neuronal death caused by familial AD gene products (e.g., V642I APP, N141I presenilin-2) and Aβ amyloid. The cDNA isolated encoded a 24-amino-acid polypeptide whose nucleotide sequence was 99% identical to the 16S rRNA region of mtDNA — establishing the MT-RNR2 encoding origin. The founding paper reported that synthetic humanin peptide (1 nM–10 µM range) blocked death of rat hippocampal neurons (primary culture) and PC12 cells caused by multiple FAD gene products and Aβ₁₋₄₃, without affecting non-AD-relevant toxins (model: rat primary hippocampal neurons + PC12 cells) [2, in_vitro].

A companion paper from the same group published concurrently in the *Journal of Neuroscience* provided detailed dose-response characterization and introduced the S14G analog (see A.4) (model: rat primary hippocampal neurons, IMR-32 human neuroblastoma) [3, in_vitro].

**Founding citation confirmed:** Hashimoto Y, Niikura T, Tajima H, Yasukawa T, Sudo H, Ito Y, Kita Y, Kawasumi M, Kouyama K, Doyu M, Sobue G, Koide T, Tsuji S, Lang J, Kurokawa K, Nishimoto I. "A rescue factor abolishing neuronal cell death by a wide spectrum of familial Alzheimer's disease genes and Aβ." *Proc Natl Acad Sci USA.* 2001;98(11):6336–41. PMID: 11371646.

### A.3 Molecular mechanism — anti-apoptotic / cytoprotective pathways

Humanin exerts cytoprotection through at least two parallel arms: (i) intracellular direct sequestration of pro-apoptotic proteins and (ii) extracellular receptor-mediated signaling cascades.

#### A.3.1 Intracellular arm: Bax and Bid sequestration

In a 2003 *Nature* study using human embryonic kidney (HEK293) cells and *in vitro* biochemical assays, Guo et al. showed that humanin directly binds Bax and prevents its translocation from cytosol to the outer mitochondrial membrane (model: HEK293 cells, cell-free Bax activation assay) [4, in_vitro]. Small interfering RNA knockdown of endogenous humanin-like sequences sensitized cells to Bax-induced death. This mechanism is purely intracellular: humanin must be present in the cytoplasm to sequester Bax before the conformational activation step. Subsequent work confirmed that humanin also binds **tBid** (truncated Bid), a BH3-only activator of Bax, further blocking the intrinsic apoptosis pathway [4, in_vitro]. Both interactions are direct protein–protein binding events characterized by co-immunoprecipitation and pull-down, but established at the in-vitro/cell level only — no human clinical data exist for this arm.

#### A.3.2 IGFBP-3 binding

Using a yeast two-hybrid screen, Ikonen et al. (2003) identified **insulin-like growth factor-binding protein 3 (IGFBP-3)** as a high-affinity humanin binding partner (model: yeast mating, mouse testis coimmunoprecipitation) [5, animal]. The interaction is mediated by the C-terminal heparin/GAG-binding domain of IGFBP-3. By binding IGFBP-3, humanin blocks IGFBP-3's ability to recruit importin-β and induce nuclear apoptotic signaling. This establishes an additional anti-apoptotic axis distinct from the Bax pathway. The interaction was confirmed in vivo in mouse testes (in-tissue coimmunoprecipitation), but the physiological significance in humans is unknown.

#### A.3.3 Extracellular receptor arm 1: FPRL1 / FPR2

The G protein-coupled receptor **formyl peptide receptor-like 1 (FPRL1, now designated FPR2)** was identified as a functional extracellular receptor for humanin by Ying et al. (2004) in the *Journal of Immunology*, using PC12 neuronal cells and transfection models (model: PC12 cells, transfected HEK293 cells) [6, in_vitro]. Humanin binding to FPR2 activates ERK1/2 via Gᵢ-coupled signaling and contributes to anti-inflammatory and neuroprotective effects. This receptor is expressed on neurons, monocytes, and neutrophils. The structural basis of FPR2–humanin recognition has since been characterized by cryo-EM (Zhu et al. 2022, *Nature Communications*), revealing a polar binding cavity within the receptor helical bundle and a hydrophobic binding groove in the extracellular region that together govern humanin recognition [9, in_vitro].

#### A.3.4 Extracellular receptor arm 2: trimeric CNTFR/WSX-1/gp130 complex → STAT3

Hashimoto et al. (2009) demonstrated that humanin inhibits neuronal apoptosis by binding a **trimeric cytokine receptor complex** comprising **CNTF receptor α (CNTFRα)**, **WSX-1 (IL-27Rα)**, and **gp130 (IL6ST)** (model: rat primary cortical neurons, GP130/WSX-1/CNTFR-overexpressing COS-7 and neuronal cells) [7, in_vitro]. Overexpression of CNTFRα and/or WSX-1 enhanced humanin binding and neuronal protection; GP130 was required for downstream protection. This complex engagement activates **JAK2 → STAT3** phosphorylation and transcription of cytoprotective genes. **AKT** and **ERK1/2** are also phosphorylated downstream of this receptor (model: hippocampal tissue from young (3-month) vs. aged (18-month) male C57BL/6 mice) [8, anecdote_aggregate]. One study in aged mice (Kim et al. 2016, Oncotarget) suggested qualitatively that ERK1/2/AKT/STAT3 responses to humanin may differ by age in hippocampal tissue; this finding has not been replicated in a peer-reviewed whitelisted journal and has not been validated in human tissue.

**Mechanism summary — evidence tier by level:**

| Mechanism | Best evidence | Level |
|---|---|---|
| Bax sequestration (cytoplasmic) | Cell-free + HEK293 knockdown [4, in_vitro] | In-vitro/cell |
| tBid/Bid sequestration | Co-IP in cell models [4, in_vitro] | In-vitro/cell |
| IGFBP-3 binding (anti-apoptotic) | Yeast 2-hybrid + mouse testis co-IP [5, animal] | In-vitro + animal |
| FPR2 / FPRL1 signaling (ERK) | PC12 + HEK293 transfection [6, in_vitro] | In-vitro/cell |
| CNTFR/WSX-1/gp130 → STAT3 | Rodent primary neurons + COS-7 [7, in_vitro] | In-vitro/cell |
| ERK/AKT/STAT3 age-dependency | Mouse hippocampal tissue [8, anecdote_aggregate] | Animal (non-whitelisted source) |

No mechanism has been directly demonstrated in controlled human in-vivo studies.

### A.4 The HNG / HNGF6A analogs

The Hashimoto/Nishimoto group characterized a panel of humanin analogs in the same J. Neurosci. 2001 paper [3, in_vitro]. The single Ser→Gly substitution at position 14 (**S14G-humanin**, abbreviated **HNG**) increases bioactivity approximately **1,000-fold** relative to native humanin in neuronal protection assays (rat hippocampal primary neurons). A second potent analog, **HNGF6A** (substitution of Phe6→Ala in addition to S14G), has been used in some cardiovascular and metabolic models. Because native humanin requires high nanomolar to low micromolar concentrations in cell assays, the vast majority of published in-vivo animal efficacy work uses HNG or HNGF6A rather than the unmodified peptide. This is a critical interpretive caveat: most preclinical claims about "humanin" in animal disease models (AD, diabetes, ischemia) are pharmacological effects of the analog, not the endogenous 24-mer. Whether circulating endogenous humanin ever reaches tissue concentrations equivalent to the HNG doses used in animal studies is unknown.

---

## Bibliography

[1]. Miller B, Kim SJ, Kumagai H, Yen K, Cohen P. "Mitochondria-derived peptides in aging and healthspan." *J Clin Invest.* 2022;132(9):e158449. DOI: 10.1172/JCI158449. PMID: 35499074. — tag: mechanism_review — tier: 1

[2]. Hashimoto Y, Niikura T, Tajima H, Yasukawa T, Sudo H, Ito Y, Kita Y, Kawasumi M, Kouyama K, Doyu M, Sobue G, Koide T, Tsuji S, Lang J, Kurokawa K, Nishimoto I. "A rescue factor abolishing neuronal cell death by a wide spectrum of familial Alzheimer's disease genes and Aβ." *Proc Natl Acad Sci USA.* 2001;98(11):6336–41. PMID: 11371646. — tag: in_vitro — tier: 1

[3]. Hashimoto Y, Niikura T, Ito Y, Sudo H, Hata M, Arakawa E, Abe Y, Kita Y, Nishimoto I. "Detailed characterization of neuroprotection by a rescue factor humanin against various Alzheimer's disease-relevant insults." *J Neurosci.* 2001;21(23):9235–45. PMID: 11717357. — tag: in_vitro — tier: 2

[4]. Guo B, Zhai D, Cabezas E, Welsh K, Nouraini S, Satterthwait AC, Reed JC. "Humanin peptide suppresses apoptosis by interfering with Bax activation." *Nature.* 2003;423(6938):456–61. PMID: 12732850. — tag: in_vitro — tier: 1

[5]. Ikonen M, Liu B, Hashimoto Y, Ma L, Lee KW, Niikura T, Nishimoto I, Cohen P. "Interaction between the Alzheimer's survival peptide humanin and insulin-like growth factor-binding protein 3 regulates cell survival and apoptosis." *Proc Natl Acad Sci USA.* 2003;100(22):13042–7. PMID: 14561895. — tag: animal — tier: 1

[6]. Ying G, Iribarren P, Zhou Y, Gong W, Zhang N, Yu ZX, Le Y, Cui Y, Wang JM. "Humanin, a newly identified neuroprotective factor, uses the G protein-coupled formylpeptide receptor-like-1 as a functional receptor." *J Immunol.* 2004;172(11):7078–85. PMID: 15153530. — tag: in_vitro — tier: 2

[7]. Hashimoto Y, Kurita M, Aiso S, Nishimoto I, Matsuoka M. "Humanin inhibits neuronal cell death by interacting with a cytokine receptor complex or complexes involving CNTF receptor α/WSX-1/gp130." *Mol Biol Cell.* 2009;20(12):2864–73. PMID: 19386761. — tag: in_vitro — tier: 2

[8]. Kim SJ, Guerrero N, Wassef G, Xiao J, Mehta HH, Cohen P, Yen K. "The mitochondrial-derived peptide humanin activates the ERK1/2, AKT, and STAT3 signaling pathways and has age-dependent signaling differences in the hippocampus." *Oncotarget.* 2016;7(30):46899–912. PMID: 27384491. — tag: anecdote_aggregate — tier: 3

[9]. Zhu Y, Lin X, Zong X, Han S, Wang M, Su Y, Ma L, Chu X, Yi C, Zhao Q, Wu B. "Structural basis of FPR2 in recognition of Aβ42 and neuroprotection by humanin." *Nat Commun.* 2022;13(1):1775. DOI: 10.1038/s41467-022-29361-x. PMID: 35365641. — tag: in_vitro — tier: 1

---

### Self-check (3 lines)

**Verified PMIDs:** All 9 citations confirmed against PubMed or authoritative publisher pages (title + first author + year + journal cross-matched): 35499074 (JCI 2022), 11371646 (PNAS 2001), 11717357 (J Neurosci 2001), 12732850 (Nature 2003), 14561895 (PNAS 2003), 15153530 (J Immunol 2004), 19386761 (Mol Biol Cell 2009), 27384491 (Oncotarget 2016), 35365641 (Nat Commun 2022).

**Off-whitelist journals:** Oncotarget [8] is a non-whitelisted (predatory-adjacent) journal. No whitelisted-journal replication of the age-dependent ERK/AKT/STAT3 hippocampus finding was found. [8] is therefore tagged `anecdote_aggregate` (tier 3) and grounds only a qualitative, hedged claim — not a numerical assertion. The JCI review [1] (tier 1) is the primary narrative anchor for humanin pathway coverage.

**Unverifiable citations:** Zero. PMID 11553805 (initial candidate, wrong paper) and 11948216 (second candidate, wrong paper) were screened and rejected. No memory-derived PMIDs were accepted without direct publisher confirmation.
