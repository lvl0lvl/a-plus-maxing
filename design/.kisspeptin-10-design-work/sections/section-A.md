## Section A — Identity & molecular mechanism

### A.1 Identity and peptide family

Kisspeptin-10 (KP-10) is the 10-amino-acid C-terminal fragment of kisspeptin (historically termed metastin), produced through proteolytic processing of the prepropeptide encoded by the **KISS1 gene** (chromosome 1q32–41) [1, mechanism_review]. The KISS1 precursor is a 145-amino-acid protein (KP-145 in humans; in rodents the longest processed fragment spans 52 residues) that is cleaved to yield a family of C-terminal amidated peptides sharing the identical C-terminal RF-NH₂ motif essential for receptor binding [1, mechanism_review].

The four biologically recognised forms are:

| Fragment | Residues | Note |
|----------|----------|------|
| KP-54 (metastin) | 54 aa | Longest human form; original placental isolate; named metastin for its tumour-metastasis suppressor activity [2, in_vitro] |
| KP-14 | 14 aa | Present in some species; detected in circulation |
| KP-13 | 13 aa | Isolated alongside KP-54 from human placenta [4, in_vitro] |
| **KP-10** | **10 aa** | Minimal bioactive C-terminal fragment retaining full KISS1R agonism; most widely used research tool form |

The KP-10 sequence is **Tyr-Asn-Trp-Asn-Ser-Phe-Gly-Leu-Arg-Phe-NH₂ (YNWNSFGLRF-NH₂)**, C-terminally amidated; molecular formula C₆₃H₈₃N₁₇O₁₄; molecular weight **1302.5 Da** [5, in_vitro]. The C-terminal decapeptide is highly conserved across mammalian species (one amino acid difference between human and rodent) and retains equipotent receptor binding relative to longer forms in competitive radioligand assays (IC₅₀ ~1.0 nM at human KISS1R expressed in CHO cells) [5, in_vitro].

#### Naming history — metastin and the cancer connection

The KISS1 gene was first identified in 1996 (Lee et al., J Natl Cancer Inst) as a melanoma metastasis suppressor — introduction of normal chromosome 6 into metastatic melanoma cells suppressed metastasis by ~95% without affecting primary tumour growth [3, cohort]. The 54-aa processed peptide was subsequently named **metastin** when isolated from human placenta in 2001 and shown to be the endogenous ligand of orphan receptor hOT7T175 (GPR54), inhibiting cancer cell chemotaxis and invasion; the naming and in vitro anti-metastatic characterisation are from Ohtaki et al. 2001 (Nature) [2, in_vitro]. The name "kisspeptin" was coined separately by Kotani et al. (2001) on isolating the same peptide family (KP-54, KP-14, and KP-13) as natural ligands for GPR54, combining an interim laboratory sequence designation and the Hershey, Pennsylvania laboratory location [4, in_vitro]. Current nomenclature uses KISS1R for the receptor and kisspeptin for the peptide family; GPR54 and metastin remain synonyms in the older literature.

---

### A.2 Receptor and signal transduction mechanism

KP-10, KP-13, KP-14, and KP-54 are all agonists at **KISS1R** (GPR54; gene locus Xq21.3), a seven-transmembrane Gq/11-coupled receptor [1, 6, mechanism_review]. All four forms share equivalent receptor affinity in vitro, with KP-10 showing approximately 8-fold greater receptor-binding potency than KP-54 in some displacement assays — indicating the C-terminal decapeptide is the pharmacophore [6, mechanism_review].

The canonical intracellular cascade upon KP-10 binding to KISS1R on hypothalamic GnRH neurons:

1. **Gαq/11 activation** → phospholipase C-β (PLC-β) cleavage of phosphatidylinositol 4,5-bisphosphate (PIP₂)
2. Generation of **inositol-1,4,5-trisphosphate (IP₃)** and diacylglycerol (DAG)
3. IP₃-mediated **intracellular Ca²⁺ mobilisation** from the endoplasmic reticulum; DAG activates protein kinase C (PKC)
4. **Membrane depolarisation** of the GnRH neuron → action potential firing
5. **GnRH peptide secretion** into the hypophysial portal circulation [6, mechanism_review]

This mechanism is established primarily in rodent in vitro electrophysiology and calcium-imaging studies, and in cell lines (human KISS1R expressed in CHO cells [5, in_vitro]; mouse hypothalamic slice preparations [8, mechanism_review]). In humans, GnRH-dependence is confirmed by the finding that GnRH receptor antagonists completely block the gonadotropin response to intravenous KP-10, making the GnRH relay obligate [6, mechanism_review].

---

### A.3 The HPG axis: kisspeptin as master regulator

Kisspeptin neurons of the hypothalamic **arcuate nucleus (ARC)** and **anteroventral periventricular nucleus (AVPV)** project to GnRH neuronal perikarya and nerve terminals in the median eminence [8, mechanism_review]. The ARC kisspeptin population co-expresses neurokinin B and dynorphin (**KNDy neurons**); optogenetic and chemogenetic studies in mice (129S6/SvEv and C57Bl/6 backgrounds, n = 4–10/group) and transgenic calcium-reporter mice show tight temporal correlation between synchronised KNDy neuronal activity and LH pulses, identifying this population as the GnRH **pulse generator** pacemaker [8, mechanism_review].

The kisspeptin → GnRH → pituitary → gonadal steroidogenesis pathway:

- **Hypothalamus:** KP-10 at KISS1R on GnRH neurons → pulsatile GnRH release
- **Anterior pituitary:** GnRH at GnRH-R → LH and FSH secretion
- **Gonads:** LH → testosterone (males) / oestradiol + progesterone (females); FSH → spermatogenesis / folliculogenesis

In healthy men, intravenous bolus KP-10 (1 µg/kg IV) produced a peak serum LH of 12.4 ± 1.7 IU/L at 30 minutes vs. baseline 4.1 ± 0.4 IU/L (n = 10, within-subject crossover; JCEM 2011) [9, open_label]. Low-dose continuous infusion (1.5 µg/kg/h) increased LH pulse frequency from 0.7 ± 0.1 to 1.0 ± 0.2 pulses/hour, confirming kisspeptin's role in setting pulsatile GnRH drive in humans [9, open_label].

---

### A.4 Genetic evidence — KISS1R loss-of-function and puberty

The causal necessity of KISS1R signalling for human puberty was established in 2003. Seminara et al. identified homozygous loss-of-function mutations in GPR54 (L148S and compound R331X/X399R) in consanguineous pedigrees presenting with absent puberty and idiopathic hypogonadotropic hypogonadism (IHH); this was a genetic-pedigree study of consanguineous families with mouse knockout validation (GPR54-null mice replicating the human phenotype — failure to undergo puberty, immature reproductive organs, low gonadotropins, and low sex steroids) [3, cohort]. Gain-of-function KISS1R mutations (e.g., R385P) cause the mirror phenotype: central precocious puberty [6, mechanism_review]. The KISS1 gene itself was later shown causal: a homozygous inactivating KISS1 mutation (p.Pro74Ser) was identified in consanguineous Turkish kindred with normosmic IHH [6, mechanism_review], establishing both ligand and receptor as non-redundant gatekeepers of pubertal onset.

---

### A.5 Pharmacokinetics of KP-10 and desensitisation

**Short half-life.** KP-10 has a circulating half-life of approximately **4 minutes** in mice (measured by plasma disappearance of equimolar doses vs. KP-54 half-life ~32 min) [10, animal]. The short half-life reflects susceptibility to N-terminal tyrosine cleavage and peptidase degradation; KP-54 is substantially more stable, in part because the 44-residue N-terminal extension protects the C-terminal pharmacophore [10, animal]. This pharmacokinetic difference explains why equimolar KP-54 and KP-10 produce strikingly different in vivo LH profiles despite near-identical in vitro binding — KP-54 reaches peak plasma levels ~50-fold higher than KP-10 after equimolar subcutaneous dosing in mice (n = 5–8 per group, 3–5-month male C57Bl/6) [10, animal]. KP-10 appears to act primarily at GnRH nerve terminals in the median eminence (outside the blood-brain barrier), whereas KP-54 additionally activates GnRH neuron perikarya behind the BBB, as evidenced by c-FOS immunostaining patterns [10, animal].

**Bolus vs. continuous desensitisation.** A critical pharmacodynamic distinction governs clinical application. Continuous or high-dose infusion of kisspeptin causes **GPR54 desensitisation** through phosphorylation, β-arrestin recruitment, and clathrin-mediated receptor internalisation — resulting in paradoxical **suppression** of LH and GnRH drive rather than sustained stimulation [6, mechanism_review]. This was demonstrated in:

- **Rodent and primate in vivo:** continuous kisspeptin infusion (kisspeptin-112-121, the KP-10 region) initially stimulates LH then abolishes the LH response; LH responsiveness to a subsequent bolus is restored within ~21 hours of stopping infusion [6, mechanism_review].
- **Human clinical (women with hypothalamic amenorrhoea, n = 10):** KP-54 continuous IV infusion at 1.0 nmol/kg/h showed peak LH at ~5 hours then progressive decline; the dose-response relationship was non-monotonic, with lower doses producing less desensitisation than the highest dose [7, open_label].

Intermittent **pulsatile** KP-10 administration, by contrast, maintains receptor responsiveness and sustains LH pulsatility [6, 9, mechanism_review, open_label].

---

### A.6 Central vs. peripheral kisspeptin biology

KISS1R is expressed in both central and peripheral tissues. Central expression is highest in the hypothalamus (ARC and AVPV kisspeptin neurons), where it drives the reproductive axis. Peripheral expression includes pituitary, gonads, placenta (the original discovery site of KP-54/metastin), liver, and kidney, as well as vascular smooth muscle and myocardium [1, mechanism_review]. Peripheral kisspeptin has been investigated in pregnancy (markedly elevated circulating KP-54 from placenta), insulin secretion, and cardiovascular tone, but these roles remain mechanistically less defined than the central HPG axis function. For the purpose of this entry, the HPG-axis mechanism is the primary evidence base.

---

## Bibliography

[1]. Mead EJ, Maguire JJ, Kuc RE, Davenport AP. Kisspeptins: a multifunctional peptide system with a role in reproduction, cancer and the cardiovascular system. Br J Pharmacol. 2007 Jun;151(8):1143–53. PMID: 17519946. — tag: mechanism_review — tier: 2

[2]. Ohtaki T, Shintani Y, Honda S, et al. Metastasis suppressor gene KiSS-1 encodes peptide ligand of a G-protein-coupled receptor. Nature. 2001;411(6837):613-617. doi:10.1038/35079135. PMID: 11385580. — tag: in_vitro — tier: 1
*(Isolated KP-54 from human placenta as endogenous ligand of orphan receptor hOT7T175/GPR54; coined the name "metastin"; in vitro: CHO-cell invasion assay; in vivo: B16-BL6 melanoma mouse pulmonary-metastasis model.)*

[3]. Seminara SB, Messager S, Chatzidaki EE, et al. The GPR54 gene as a regulator of puberty. N Engl J Med. 2003;349(17):1614-1627. doi:10.1056/NEJMoa035322. PMID: 14573733. — tag: cohort — tier: 1
*(Design: genetic-pedigree case-series of consanguineous families with homozygous GPR54 loss-of-function mutations + GPR54-null mouse knockout validation; the `cohort` tag reflects the human-family-genetics component; the mouse KO arm is the phenotypic validation layer.)*

[4]. Kotani M, Detheux M, Vandenbogaerde A, Communi D, Vanderwinden JM, Le Poul E, et al. The metastasis suppressor gene KiSS-1 encodes kisspeptins, the natural ligands of the orphan G protein-coupled receptor GPR54. J Biol Chem. 2001 Sep 14;276(37):34631–6. PMID: 11457843. — tag: in_vitro — tier: 2
*(Isolated KP-54, KP-14, and KP-13 from human placenta as GPR54 ligands; coined the name "kisspeptin"; pharmacological characterisation in CHO-K1 cells.)*

[5]. Curtis AE, Faure MO, Funes S, Dowell SJ, Millar RP, Davidson JS, et al. A kisspeptin-10 analog with greater in vivo bioactivity than kisspeptin-10. Am J Physiol Endocrinol Metab. 2010 Jan;298(1):E296–303. PMID: 19934405. — tag: in_vitro — tier: 2
*(In vitro characterisation performed in human KISS1R–CHO cells; in vivo arm in adult male C57Bl/6 mice, n = 4–8/group.)*

[6]. Gianetti E, Seminara S. Kisspeptin and KISS1R: a critical pathway in the reproductive system. Reproduction. 2008 Sep;136(3):295–301. PMID: 18515314. — tag: mechanism_review — tier: 2

[7]. Jayasena CN, Abbara A, Veldhuis JD, et al. Increasing LH pulsatility in women with hypothalamic amenorrhoea using intravenous infusion of kisspeptin-54. J Clin Endocrinol Metab. 2014;99(6):E953-E961. doi:10.1210/jc.2013-1569. PMID: 24517142. — tag: open_label — tier: 1
*(n = 10 women with hypothalamic amenorrhoea; continuous IV KP-54 dose-escalation; human desensitisation datum.)*

[8]. Plant TM. The neurobiological mechanism underlying hypothalamic GnRH pulse generation: the role of kisspeptin neurons in the arcuate nucleus. F1000Res. 2019;8:F1000 Faculty Rev-982. PMID: 31297186. — tag: mechanism_review — tier: 2
*(Animal evidence from mice [various transgenic lines] and rhesus monkeys; KNDy neuron model.)*

[9]. George JT, Veldhuis JD, Roseweir AK, et al. Kisspeptin-10 is a potent stimulator of LH and increases pulse frequency in men. J Clin Endocrinol Metab. 2011;96(8):E1228-E1236. doi:10.1210/jc.2011-0089. PMID: 21632807. — tag: open_label — tier: 1
*(Within-subject crossover, n = 10 healthy men; IV bolus dose-ranging 0.01–3.0 µg/kg; continuous infusion arm.)*

[10]. d'Anglemont de Tassigny X, Semaan SJ, Bhatt DL, et al. Mechanistic insights into the more potent effect of KP-54 compared to KP-10 in vivo. PLoS One. 2017 May 3;12(5):e0176511. PMID: 28464043. — tag: animal — tier: 2
*(Male wild-type 129S6/SvEv mice, 3–5 months; n = 5–8/group. In vitro arm: human KISS1R–CHO cells.)*

---

### Self-check (3 lines)

1. **No predatory-OA journals cited.** All sources are Br J Pharmacol, N Engl J Med, J Biol Chem, Am J Physiol, Reproduction, JCEM, PLoS One, F1000Research — none on the rejected list.
2. **All PMIDs verified via search/fetch.** PMIDs 17519946, 11385580, 14573733, 11457843, 19934405, 18515314, 24517142, 31297186, 21632807, 28464043 confirmed against title + first-author + year + journal; no memory-only citations.
3. **Animal/in vitro models named in prose, not stated as human evidence.** KP-10 half-life (~4 min) and KNDy optogenetics are attributed to mouse models; human data (George 2011, Jayasena 2014) cited separately for the HPG axis LH-response and desensitisation claims.
