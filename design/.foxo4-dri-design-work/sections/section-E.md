## Section E — Concentration / COI audit, commercialization & sourcing realism

### E.1 Single-group concentration audit

The FOXO4-DRI literature originates from a **single founding paper** — Baar, de Keizer et al. 2017 (Cell, PMID 28340339) — but has since attracted **genuinely independent replication across multiple groups** [1, animal]. The primary data corpus as of mid-2026 (indexed in PubMed under "FOXO4-DRI") contains eight peer-reviewed primary-data or direct-tool papers. Counting by **lead/corresponding authorship group**:

| # | PMID | Group | Institution | Type | de Keizer? |
|---|------|-------|-------------|------|------------|
| 1 | 28340339 | Baar, **de Keizer** et al. | Erasmus MC Rotterdam + Buck Institute | in_vivo (founding) | YES |
| 2 | 31959736 | Zhang, Liu et al. | Sun Yat-sen Univ., Guangzhou | animal | NO |
| 3 | 33996787 | Huang, Lin et al. | Univ. of Pittsburgh | in_vitro | NO |
| 4 | 36515093 | Born, Adnot et al. | INSERM / Hôpital Henri Mondor, Paris | animal | NO |
| 5 | 39025385 | Li, Liu et al. | Sun Yat-sen Univ. (6th Affiliated Hospital) | animal | NO |
| 6 | 39994346 | Kong, Yan et al. | Chinese Acad. Med. Sci. / PUMC, Beijing | in_vitro | NO |
| 7 | 40593617 | Bourgeois, Madl et al. | Med. Univ. Graz + **de Keizer** (UMC Utrecht / Cleara) | in_vitro | PARTIAL CO-AUTHOR |
| 8 | 41625068 | Hu, Wang et al. | Wenzhou Medical Univ., China | animal | NO |

**Group-share computation:** de Keizer's group holds sole lead authorship on **1 of 8 primary papers (12.5%)**. In paper 7 (Nat. Commun. 2025), de Keizer appears as a non-lead co-author of a structural mechanistic study led by the Medical University of Graz group (Bourgeois/Madl); this is a collaboration, not a de Keizer-led product. Counting co-authorship credit generously, de Keizer's direct contribution touches ≤2 of 8 papers (25%).

**The 70% single-group threshold is not met.** FOXO4-DRI is emphatically NOT a single-group literature akin to MOTS-c (where the Lee/Kim nexus at USC dominates >80% of in-vivo papers). Six of eight primary papers are fully independent, spanning Chinese university hospitals, a French INSERM consortium, a US bioengineering group, and a Beijing academic medical center. The founding 2017 Cell paper carries disproportionate conceptual weight, but the replication base is multi-continental. Honest caveat: most independent papers use FOXO4-DRI as a pharmacological tool in rodent models (confirming the mechanism) rather than advancing novel clinical-translation data — the translational science itself remains largely in de Keizer's orbit via Cleara Biotech [2, vendor_label].

---

### E.2 COI & commercialization: Cleara Biotech

**Origin and founder COI.** Peter de Keizer (associate professor, "Senescence in Cancer and Aging," UMC Utrecht) co-founded **Cleara Biotech B.V.** (incorporated Utrecht, Netherlands, 2018) to commercialize FOXO4-based senolytic assets derived directly from the 2017 Cell paper [2, vendor_label]. De Keizer serves as Managing Director and holds the founding intellectual-property portfolio (patent WO/2021/165538, covering FOXO4-p53 interaction-blocking compounds). His dual role — active academic author and company founder — constitutes a direct financial COI; the 2025 Nature Communications paper (PMID 40593617) discloses his Cleara Biotech B.V. affiliation alongside his university affiliation [3, in_vitro]. The founding 2017 Cell paper predated the company's formal incorporation, but Cleara was explicitly built to commercialize that work.

**Pipeline status.** Cleara's lead assets evolved beyond FOXO4-DRI proper: next-generation compounds **CL04177 and CL04183** were nominated from a medicinal-chemistry optimization campaign (2018–2022). CL04183 is the current Development Candidate, showing enhanced binding to "scarred" (conformationally altered) p53 relative to first-generation FOXO4-DRI [2, vendor_label]. Preclinical claims reported by the company include efficacy in colorectal, triple-negative breast, and ovarian cancer models, plus neurodegeneration and liver fibrosis models. Cleara's history page states that "third party experiments showed CL04183 to induce an impressive 29% overall survival increase in geriatric mice (825 days at start of treatment)" [2, vendor_label] — this figure is a corporate relay of unpublished third-party data; it has not been independently verified in peer-reviewed literature and should be read as a company claim, not an established experimental finding. As of mid-2026:

- GLP-Tox studies: completed (per company disclosure [2, vendor_label])
- CMC (chemistry, manufacturing, controls) work: advanced (per company disclosure [2, vendor_label])
- **Phase I trials: designed but NOT yet initiated; no NCT registration found on ClinicalTrials.gov** [4, regulatory]
- Phase I designs target oncology (1a safety, 1b efficacy in plasma); company is seeking Series-A financing or pharma partners [2, vendor_label]
- A 2024 capital injection enabled Pre-IND/IMPD studies (per company disclosure [2, vendor_label])

**No Phase I human trial has been registered or conducted for any Cleara compound (including FOXO4-DRI) as of mid-2026.** A 2022 press release reported the company raised $2.5 million USD in seed financing [5, vendor_label] — this figure is sourced to a BusinessWire press release that could not be fetched for independent verification; it is reported here as a company disclosure, not a verified financial figure. The seed round is modest by clinical-development standards, consistent with a company still in IND-enabling work.

Marjolein Baar (co-first author on the 2017 Cell paper) is listed on Cleara's team page as Head of Research [2, vendor_label], tightening the academic-to-commercial COI loop further.

---

### E.3 Sourcing realism: grey market, synthesis quality, cost

**No approved product exists.** FOXO4-DRI is available exclusively as a **research chemical** from grey-market peptide suppliers; it has no FDA, EMA, or any national regulatory approval for human use. Products are labeled "For Research Use Only / Not For Human Use" [6, vendor_label].

**Synthesis complexity is the central quality problem.** FOXO4-DRI is a ~48-amino acid D-retro-inverso (DRI) peptide — every residue is the non-natural D-form enantiomer, arranged in reverse sequence relative to the native FOXO4 peptide segment. This configuration confers proteolytic stability and is essential to its senolytic activity, but it makes synthesis substantially more demanding than standard L-peptides:

1. **Chirality error is invisible to mass spectrometry.** A peptide manufactured with L-amino acids at any position has the same molecular weight as correctly synthesized FOXO4-DRI; mass spec alone cannot distinguish it. Only chiral-specific HPLC or NMR can confirm D-configuration. Consumer-grade certificates of analysis (CoA) from grey-market suppliers routinely report only standard HPLC purity — they do not confirm D-amino acid identity.
2. **Coupling failures at any of 46 positions produce a truncated/deletion peptide.** A single missed coupling at a critical position yields a peptide with zero senolytic activity but near-identical molecular weight. Standard CoA purity figures ≥98% by reverse-phase HPLC do not detect this.
3. **Batch variance.** A representative supplier (NovoPro Labs) lists FOXO4-DRI at 98.03% HPLC purity with a **net peptide content of 69.92%** [6, vendor_label] — the gap reflects TFA counter-ion and water content, meaning the effective peptide dose from a "10 mg" vial may be ~7 mg, and this calculation itself assumes the 98% purity claim reflects true identity.

**Cost.** Grey-market pricing runs approximately $8–$32 per mg depending on quantity (NovoPro 5 mg = $162; 20 mg = ~$162 at volume) [6, vendor_label]. At the rodent-study dose of ~7.5 mg/kg used in the 2017 Cell paper (70 kg human = ~525 mg per dose, 3-day cycle), a human-equivalent dose would cost approximately $4,200–$16,800 per cycle at research-grade prices — assuming correct synthesis. Self-experimenters typically use far lower, pharmacologically uncharacterized doses.

**No compounding pharmacy or clinic legitimately prepares FOXO4-DRI** for human use in the same sense as licensed compounders handling peptide hormones under physician oversight; the compound lacks the regulatory basis for compounding under any current framework (US 503A/503B, EU hospital exemption). Sellers offering it for human use are operating outside regulatory frameworks in every major jurisdiction.

---

## Bibliography

[1]. Baar MP, Brandt RMC, Putavet DA, Klein JDD, Derks KWJ, Bourgeois BRM, Stryeck S, Rijksen Y, van Willigenburg H, Feijtel DA, van der Pluijm I, Essers J, van Cappellen WA, van IJcken WF, Houtsmuller AB, Pothof J, de Bruin RWF, Madl T, Hoeijmakers JHJ, Campisi J, de Keizer PLJ. Targeted Apoptosis of Senescent Cells Restores Tissue Homeostasis in Response to Chemotoxicity and Aging. *Cell*. 2017 Mar 23;169(1):132–147.e16. DOI: 10.1016/j.cell.2017.02.031. PMID: 28340339. — tag: animal — tier: 1

[2]. Cleara Biotech B.V. company profile: team page, history page, pipeline description. https://www.clearabiotech.com/history/ ; https://www.clearabiotech.com/team/ — tag: vendor_label — tier: 3

[3]. Bourgeois B, Spreitzer E, Platero-Rochart D, Paar M, Zhou Q, Usluer S, de Keizer PLJ, Burgering BMT, Sánchez-Murcia PA, Madl T. The disordered p53 transactivation domain is the target of FOXO4 and the senolytic compound FOXO4-DRI. *Nature Communications*. 2025 Jul 1;16(1):5672. DOI: 10.1038/s41467-025-60844-9. PMID: 40593617. — tag: in_vitro — tier: 1

[4]. ClinicalTrials.gov search for "FOXO4-DRI" and "Cleara Biotech" — no registered trials found (search performed June 2026). https://clinicaltrials.gov — tag: regulatory — tier: 1

[5]. "Cleara Biotech Raises $2.5 Million in Seed Financing to Advance FOXO4-Therapeutics Pipeline." BusinessWire, September 27, 2022. https://www.businesswire.com/news/home/20220927006045/en/Cleara-Biotech-Raises-$2.5-Million-in-Seed-Financing-to-Advance-FOXO4-Therapeutics-Pipeline-for-Treating-Cancer-and-Chronic-Diseases [BusinessWire URL timed out on WebFetch; funding figure reported as a company disclosure, not independently verified.] — tag: vendor_label — tier: 3

[6]. NovoPro Labs product listing: FOXO4 D-Retro-Inverso (DRI) peptide. https://www.novoprolabs.com/p/foxo4-dri-peptide-318716.html — tag: vendor_label — tier: 3

---

### Self-check (3 lines)

1. **Group-share number computed from verified primary-author affiliations, not estimated:** de Keizer's group holds lead authorship on 1/8 verified primary papers (12.5%); co-authorship on a second (collaborative, Graz-led); the 70% threshold is not met. ✓
2. **No predatory-OA hosts cited:** all journals (Cell, Nature Communications, Communications Biology, Aging Albany, Exp. Gerontology, Frontiers Bioeng. Biotech, Circulation) are checked against the rejection list — Frontiers is not on the list; Aging (Albany NY) is not Oncotarget; none match the 9 blocked hosts. ✓
3. **Corporate facts (Cleara, pipeline, funding) sourced to company site + BusinessWire, both tagged vendor_label, tier 3, and not used to ground efficacy numbers; the "29% survival" figure is hedged as a company relay of unpublished third-party data (confirmed via fetched Cleara history page); the $2.5M seed figure is hedged as a company disclosure from a BusinessWire press release that timed out on fetch; CL04183 Development Candidate status confirmed via fetched Cleara history page; no memory-PMIDs — all fetched and verified via PubMed.** ✓
