---
title: BPC-157 Research Report (Canonical Academic Layer)
slug: bpc-157
class: peptide
type_tag_audit: pass-iter-2
integrity_gate: pass-iter-2
critique_gate: pass-iter-2-refined
mode: deep
generated: 2026-05-24
revisions:
- date: 2026-05-24
  op: rebuild
  reason: suspect-fabrications
  prior: vault/library/peptides/bpc-157/_archive/2026-05-24-suspect-fabrications/
- date: 2026-05-24
  op: refine
  reason: phase-6-critique-halt
  fixes:
  - citation-crosswalk-to-bibliography
  - tohyama-cluster-rule
  - bibliography-22-32-downgrade
  - bias-disclosures
  - alt-explanations
  - publication-bias-overlay
  - pd-pk-null-alternative
  - fda-safety-reasoning-expansion
supplementary_layers:
  practitioner: vault/library/peptides/bpc-157/practitioner-layer.md
  non_english: vault/library/peptides/bpc-157/non-english-layer.md
re_rotation_triggers:
- New independent in-vivo replication outside Sikiric/Pliva-Zagreb cluster
- Any Phase 2/3 RCT primary publication (NCT07437547 readout)
- FDA reclassification update post-PCAC review (scheduled July 23 2026)
- Any new Edwin Lee-clinic publication
permalink: a-plus-maxing/library/peptides/bpc-157/_archive/2026-06-18-suspect-fabrications/research-report
---

# BPC-157 — Canonical Academic Layer Report

## 1. Identity and Provenance

BPC-157 is a synthetic pentadecapeptide of sequence GEPPPGKPADDAGLV (15 residues, molecular weight 1419.55 as the free acid; commonly supplied as the acetate salt with counterion-inclusive MW around 1479.5). The compound has appeared in the peer-reviewed literature under several synonymous designations: **BPC-157** (the dominant academic-literature name), **PL 14736** (Pliva industrial development designation for the same molecule, used principally in the inflammatory-bowel-disease clinical program), **PL-10** and **PLD-116** (earlier Pliva codes for the same compound during pre-clinical and Phase 1 work), and **bepecin** (the international non-proprietary name used in the Diagen patent and a small set of Croatian regulatory filings). The molecule has also been referred to as the "stable gastric pentadecapeptide BPC 157" in essentially all Sikirić-group publications [1, animal] [55, mechanism_review].

The compound is derived in concept from a putative gastric-juice protein the Sikirić group at the University of Zagreb School of Medicine called "BPC" (body protection compound). The 1993 *Journal de Physiologie (Paris)* overview by Sikirić P, Petek M, Rucman R, Seiwerth S et al. (87:313–327; DOI 10.1016/0928-4257(93)90038-U; PMID 8298609 — see §13 below for the contradiction-resolution note on the PMID) is the originating descriptive paper that anchors essentially every downstream claim about gastric-juice stability, cytoprotection, and the "organoprotection hypothesis" [1, animal]. Industrial development as PL 14736 was undertaken by Pliva Research Institute in Zagreb (the originator pharmaceutical company), reaching a Phase 2 randomized double-blind placebo-controlled trial of rectal-enema PL 14736 in mild-to-moderate ulcerative colitis (Ruenzi M et al., DDW 2005 oral presentation; abstract in *Gastroenterology* 128:A584) before the program effectively halted at the abstract stage without full publication [43, rct].

Three salt forms appear in the published and patent literature. The **acetate** salt is the standard form used in essentially all peer-reviewed animal work and in the compounded pharmacy supply that underlies US off-label human use. The **L-arginine di-salt** ("arginate", "bepecin di-L-arginine salt", marketed as "Pentadeca Arginate" or PDA) is the subject of Diagen patent WO2014142764A1, which reports differential in-vitro stability data favoring the arginate over the acetate; the patent contains HPLC stability tables but no in-vivo bioavailability measurements [Diagen WO2014142764A1, vendor_label / patent — used here only for in-vitro chemical-stability comparison, never grounding any in-vivo or human claim]. The **trifluoroacetate (TFA)** form is present as a residual counterion in some research-grade preparations following standard solid-phase peptide-synthesis purification; no peer-reviewed pharmacology paper isolates TFA-form properties from acetate-form properties. The arginate-vs-acetate "oral bioavailability differential" widely repeated in commercial copy (commonly stated as "acetate ~3%, arginate ~90%") has no primary peer-reviewed backing and is treated as a fabrication-risk node in §6 below.

Three consecutive proline residues at positions 3–5 of the sequence (GEP-PP-G…) are repeatedly invoked as the structural rationale for protease resistance. The mechanistic premise — that proline residues impair cleavage of the adjacent peptide bond by most mammalian endopeptidases — is generally accepted in peptide chemistry, but the residue-specific contribution of this proline triad to BPC-157 stability has **not** been measured by mutational scan or alanine-walk in any peer-reviewed BPC-157 primary located during this dispatch. The structural-stability claim is therefore mechanistically plausible but not directly evidenced. Readers should not interpret "three prolines confer stability" as a measured finding for this molecule; it is an inference from general peptide chemistry (no primary peer-reviewed cite available; flagged `[corpus-unverifiable]`).

The earliest pre-clinical work on the BPC parent fraction and on the pentadecapeptide is concentrated at the University of Zagreb (Department of Pharmacology, Department of Pathology, and clinically affiliated Zagreb hospital departments) and at Pliva Research Institute Zagreb (the originator industrial group). This lineage is the load-bearing fact of the entire report. Section 2 develops the concentration-risk framing that flows from this lineage; every subsequent indication section is read against it.

## 2. Evidence Landscape and Concentration Risk

This section is surfaced before any indication subsection per the Phase 4.75 IC-9 health-gates §3 rule (concentration ≥70% in the dominant cluster). The triangulation underlying this section is documented in `/tmp/aplus-research/bpc-157/triangulation.md` and the deduplicated enumeration is in `/tmp/aplus-research/bpc-157/aggregate-primaries.json`. The reader is asked to internalize this section before reading the mechanism, animal, human, PK, or safety chapters.

### 2.1 Aggregate primary enumeration

Across all six rebuilt section files (mechanism, animal MSK, animal GI/visceral/CNS, human, PK/routes/stability, AEs/regulatory), the initial enumeration produced 54 distinct primary citations after deduplication by PMID where available and by author + journal + year + page otherwise. Mechanism reviews, regulatory documents (FDA, TGA, WADA, Federal Register, ClinicalTrials.gov listings), and the Diagen patent are excluded from the count because they are evidence-tier-different categories (review-level synthesis, regulatory primaries, vendor/patent material).

Phase 6 critique audit downgraded two of those 54 entries to `[corpus-unverifiable]` because they cannot be verified as resolvable primaries from the retrieval base: entry #22 (Sikirić group 2009, *J Physiol Pharmacol* supplement, immunohistochemical VEGF study) and entry #32 (Belosic Halle Z et al. 2017, neuroleptics + BPC-157 study). Both lack first-author surname (in the case of #22), journal volume, page range, and DOI/PMID. They are retained in §12 with explicit `[corpus-unverifiable]` flags but **removed from the primary count**. The working denominator for cluster-share arithmetic in this report is therefore **52** (not 54). Both downgraded entries would have been counted to the Sikirić-Zagreb cluster, so the recomputation reduces the Sikirić numerator by 2 as well.

### 2.2 The Sikirić-Zagreb concentration (recomputed denominator = 52)

Of the 52 verifiable primaries, **39 (75.0%) are from the Sikirić-Zagreb academic cluster** — the Department of Pharmacology of the University of Zagreb School of Medicine and its clinically affiliated Zagreb hospital departments, J.J. Strossmayer University of Osijek Faculty of Medicine where Sikirić or Seiwerth is senior author, and Korean collaborators where Sikirić is senior or co-senior (Kang 2018, Park 2020). Per the Phase 6 critique resolution of the Tohyama 2004 double-counting issue, **Tohyama Y, Sikirić P, Diksic M 2004 (entry #54) is counted to the Sikirić-Zagreb cluster** consistently here and in §5 via the sub-cluster rule (Sikirić is a co-author on the paper); the aggregate-rule alternative (Diksic senior at McGill = independent) is abandoned because it produced contradictory cluster arithmetic between §2 and §5. With Tohyama folded in, the Sikirić count becomes 39 of 52.

A further **3 primaries (5.8%) are from the Pliva-Zagreb industrial cluster** — Pliva Research Institute Zagreb, the originator pharmaceutical company that developed PL 14736. Folding the academic and industrial Zagreb clusters together (both originate in the same metropolitan lineage), the **combined Zagreb-metropolitan share is 42 of 52 = 80.8%**.

Both the academic-only share (75.0%) and the combined share (80.8%) exceed the 70% threshold that triggers a first-class concentration section under health-gates §3. The threshold is triggered at every cluster definition; the gate fires regardless of how strictly the lineage is drawn.

### 2.3 Independent-replication landscape

Independent replication of BPC-157 work exists, but in small clusters. The non-Zagreb clusters identified across the 52 verifiable primaries are:

- **Chang Gung University, Taiwan (Pang Jong-Hwei Su group)** — 4 papers (7.7% of 52). Hsieh M-J et al. 2017 (entry [44], *J Mol Med* 95:323–333; PMID 27847966) and Hsieh M-J et al. 2020 (entry [45], *Sci Rep* 10:17078; PMID 33051527) provide the foundational independent mechanistic support for the VEGFR2-Akt-eNOS and Src–caveolin-1–eNOS angiogenesis pathways. Chang C-H et al. 2011 (entry [46], *J Appl Physiol* 110:774–780; PMID 21030672) and Chang C-H et al. 2014 (entry [47], *Molecules* 19:19066–19077; PMID 25415472) are the FAK–paxillin and growth-hormone-receptor in-vitro tendon-fibroblast studies. **All four Chang Gung papers are in-vitro or ex-vivo on isolated rat cells; no Chang Gung paper independently replicates a Sikirić in-vivo finding.**

- **Air Force Medical University / Fourth Military Medical University, Xi'an, China (per Phase 4.75 IC-10/C6 correction)** — 3 papers (5.8% of 52), comprising He L et al. 2022 (entry [48], *Front Pharmacol* 13:1026182; PMID 36588717; PMC9794587 — the cross-species rat+beagle PK study); Xu C et al. 2020 (entry [49], *Regul Toxicol Pharmacol* 114:104665 — the GLP preclinical safety package); and, per the Phase 4.75 IC-10 reclassification, **Xue X-C et al. 2004 (entry [50], *World J Gastroenterol* 10(7):1032–1036) — corrected from Second Military Medical University Shanghai to Fourth Military Medical University Xi'an**. The "independent Chinese signal" in BPC-157 is therefore itself a **3-paper single-institution cluster**, not three independent confirmations. This is the **secondary concentration finding** flagged in the Phase 4.75 warnings list and is explicit in this report: the so-called independent PK + safety + gastric-ulcer signal is single-cluster within the Xi'an Fourth Military Medical University.

- **Edwin Lee, Institute for Hormonal Balance, Orlando FL (UCF College of Medicine appointment)** — 3 papers (5.8% of 52). Lee E & Padgett W 2021 (entry [51], *Altern Ther Health Med* 27(4):8–13 — intra-articular knee retrospective chart review, n=17 treated, 16 contacted); Lee E, Walker C, Ayadi B 2024 (entry [52], *Altern Ther Health Med* 30(10):12–17; PMID 39325560 — intravesical interstitial cystitis pilot, n=12); Lee E & Burgess K 2025 (entry [53], *Altern Ther Health Med* 31(5):20–24 — IV safety pilot, n=2; per C4 contradiction-resolution, co-author initial K). **All three are open-label, no comparator, single-investigator, single-clinic, published in the same lower-impact peer-reviewed journal. Cumulative n ≈ 31 across the three Lee studies.** Within the published US human evidence base, the Lee Orlando concentration is **100%**.

- **McGill University / Montreal Neurological Institute (Diksic group)** — Tohyama Y, Sikirić P, Diksic M 2004 (entry [54], *Life Sci* 76:345–357) was previously counted as the lone independent McGill primary; per the Phase 6 critique resolution of the §2/§5 double-counting contradiction, **this paper is now counted to the Sikirić-Zagreb cluster** via the sub-cluster rule (Sikirić co-author; Diksic senior). Zero verifiable McGill independent primaries remain after this reclassification.

- **Loughborough University, UK (Gwyer / Wragg / Wilson)** — independent narrative-review provenance only (Gwyer D et al. 2019, entry [56], *Cell Tissue Res* 377:153–159; PMID 30915550). Excluded from the 52-primary count as mechanism_review; included here as evidence that independent UK academic groups have summarized the literature.

- **University of Utah (McGuire FP et al. 2025)** — independent narrative-review provenance only (entry [55], *Curr Rev Musculoskelet Med* 18(12):611–619; PMID 40789979; PMC12446177). Independent US academic synthesis; concludes "BPC-157 should be considered investigational." Excluded from 52-primary count as mechanism_review.

- **Maria Sklodowska-Curie Medical Academy in Warsaw, Poland (Józwiak M et al. 2025, *Pharmaceuticals (Basel)* 18(2):185)** — independent Eastern-European review provenance only (mechanism_review, excluded from 52-primary count).

- **Hospital for Special Surgery / Case Western Reserve (Vasireddi N et al. 2025, entry [57], *HSS J*; PMC12313605)** — independent systematic-review provenance (mechanism_review, excluded from 52-primary count). Screened 544 articles 1993–2024, found one human clinical study meeting inclusion criteria (one of the Lee Orlando papers); 35 of 36 included studies were animal; **only 4 of 36 included studies assessed safety**. This datum is load-bearing for §8 safety-base sizing.

### 2.4 Section-by-section concentration shares

The Sikirić-cluster share varies by indication subdomain. With the Tohyama-rule fix (Tohyama → Sikirić everywhere) and the #22 / #32 downgrade applied, the per-section views are:

| Section | Domain | Sikirić-cluster share (per section) | Notes |
|---|---|---|---|
| A | Mechanism (≈10 verifiable cites after #22 downgrade) | ~30% (3/10 with Pliva folded in) | LOWEST concentration in the entry; Chang Gung independent mechanism work dominates |
| B | Animal MSK (11 cites) | **9/11 = 82% including the two in-vitro Chang Gung tendon-fibroblast papers; 9/9 = 100% restricted to in-vivo MSK studies** | Independent labs (Chang Gung) only at the in-vitro tendon-fibroblast level |
| C | Animal GI/visceral/CNS (18 cites; Tohyama → Sikirić per uniform rule) | ~94% (17/18) | DEEPEST concentration; only Xue 2004 (now Xi'an cluster) is non-Sikirić |
| D | Human evidence (7 primaries) | Pliva 1 + Lee Orlando 3 + Sikirić-cited reviews 3 | **100% of published US human efficacy/safety is single-investigator Lee Orlando** |
| E | PK / routes / stability (~15 cites incl. patent and reviews) | ~60–70% Sikirić-Zagreb + Pliva/Diagen combined | "Independent" PK signal is single-lab Xi'an (now 3 papers) |
| F | AEs / regulatory (≈22 verifiable primaries after #32 downgrade) | ~43% | Section F deliberately surveys regulatory bodies + independent reviews, mechanically diluting the Sikirić share |

The per-section denominators differ because (a) the same primary can ground claims in more than one section (e.g., Stupnisek 2015 = B11 and grounding F24 hemostasis), and (b) Section F includes regulatory primaries that are excluded from the 52-primary aggregate. The single canonical aggregate denominator (52) is the load-bearing arithmetic; per-section shares are sub-views.

### 2.5 Honest absence findings (concentration domain)

The following negative findings are load-bearing and must travel with every indication subsection:

- **No independent in-vivo replication of the Sikirić MSK findings exists.** No Achilles transection, MCL crush, quadriceps transection, gastrocnemius crush, segmental bone-defect, or anticoagulant-interaction in-vivo BPC-157 paper from a non-Sikirić, non-Sikirić-co-authored laboratory was identified in this retrieval (Section B Finding 12). The only independent MSK-relevant replication thread is the Chang Gung in-vitro tendon-fibroblast work, which replicates cellular effects (FAK–paxillin activation, GHR upregulation) but does NOT independently replicate any animal in-vivo MSK outcome.

- **No independent in-vivo replication of the Sikirić MSK findings exists.** Restated to emphasize: the Achilles/MCL/quadriceps/bone-defect literature is 100% Sikirić-anchored in vivo.

- **All published US human efficacy/safety data trace to a single investigator at a single private clinic in Orlando, Florida (Edwin Lee, MD).** Independent replication of any Lee finding = zero. Cumulative n exposed under Lee protocols ≈ 31.

- **All published anti-tumor evidence for BPC-157 is 100% Sikirić-cluster.** Radeljak S, Seiwerth S, Sikirić P 2004 (*Melanoma Res* 14:A14–A15) is an abstract-level publication, not a full paper. Kang EA, Han YM, An JM, Park YJ, Sikirić P et al. 2018 (*Curr Pharm Des* 24:1947–1956; doi 10.2174/1381612824666180614082950) is in the Sikirić-Zagreb cluster via the sub-cluster rule (Korean first author, Sikirić senior). Sikirić P et al. 2025 (PMC12567428) is a Reply review. No non-Sikirić in-vitro or in-vivo anti-tumor primary was located.

- **No independent reconfirmation of the Sikirić 1993 24-hour gastric-juice stability figure exists.** The claim repeats across at least 10 Sikirić-group reviews but the underlying degradation-versus-time curve has not been published in peer-reviewed primary literature outside the Zagreb-Pliva lineage. The strongest in-vitro chemical-stability dataset is the Diagen patent (vendor/patent tier, also Zagreb-Pliva lineage).

### 2.6 Interpretation rule for downstream readers

Every indication claim in this report should be read against the concentration risk surfaced here. Single-lab dominance does not automatically falsify a finding — many compounds in clinical use today began as single-lab discoveries that subsequently replicated. But single-lab dominance does mean that the failure mode of the entire evidence base is **correlated**: a methodological problem, a measurement artifact, or a model-system limitation in the dominant lab propagates to every downstream claim that lab generates. The reader who interprets BPC-157 evidence without applying this concentration framing is reading the literature less honestly than the literature itself reports it. Independent confirmation is the load-bearing missing piece; until it arrives, every indication claim carries epistemic asymmetry that the next sections will tag in-line.

**Implication for downstream agent consumers**: any specialist agent recommending BPC-157 should explicitly note Zagreb-cluster dominance in its rationale. Failing to note it is not honest summarization.

### 2.7 Author and sponsor disclosures (Phase 6 critique addition)

The concentration arithmetic above understates the load-bearing structural fact that the Sikirić-Zagreb academic cluster and the Pliva-Zagreb industrial cluster are not adjacent — they are **entangled by personal authorship**. Three disclosures the reader needs to internalize alongside the cluster numbers:

- **Sikirić P personally collaborated with Pliva Research Institute during the PL 14736 development program** that produced the originator clinical trials (Veljaca 2003 healthy-male Phase 1 abstract and Ruenzi 2005 Phase 2 UC enema RCT abstract). The originator company Pliva was the industrial home of the same investigator network whose academic output dominates the literature. The Tkalčević 2007 *Eur J Pharmacol* paper (entry [41]) — counted as Pliva-industrial in §2.2 — has Parnham MJ as senior author at Pliva, but its findings (EGR-1 / NAB2 in Caco-2 cells) feed directly into Sikirić-group mechanism reviews. Academic and industrial Zagreb are one author network, not two.

- **The Diagen patent estate continues the Pliva BPC program under different corporate ownership.** Diagen patent WO2014142764A1 (bepecin di-L-arginine salt) names **Rucman R and Pflaum Z as inventors**. Rucman R is a co-author on the foundational Sikirić P, Petek M, Rucman R, Seiwerth S 1993 paper (entry [1]) and on a substantial fraction of Sikirić-group papers from 1993 through at least 2015 (Sebecic 1999, Jelovac 1998, Cerovecki 2010, others). The corporate-development arc Pliva → Diagen and the academic-publication arc Sikirić-Zagreb share authors. The "in-vitro arginate stability differential" (acetate 0.08% vs arginate 84.9% intact after 5 h at pH 3.0) — the load-bearing chemical argument for switching to the arginate salt that drives the "pentadeca arginate (PDA)" commercial market — lives **entirely in a patent whose inventors overlap the academic literature it cites**.

- **The Sikirić P et al. 2025 Reply paper** (entry [59], PMC12567428, "BPC 157 Therapy: Targeting Angiogenesis and Nitric Oxide…") is a **defensive response** to the Józwiak M et al. 2025 critical review in *Pharmaceuticals (Basel)*. The Reply does not present new primary data; it argues against the Józwiak critique with reference to prior Sikirić-group work. The existence of a 2025 defensive Reply by the originating investigator is consistent with the literature being contested at the principal-investigator level rather than settled — and the Reply's authorship cannot be read as independent confirmation of any claim it defends.

These three disclosures change how the §2.2 arithmetic should be read. The "Sikirić-Zagreb academic 75%" and "combined Zagreb 80.8%" numbers are computed by institution. The structural concentration is tighter than that: a smaller author group, with continuous industrial-academic entanglement and an active defensive posture against critical reviews, produces the load-bearing evidence base. Treat industry-bias and author-bias as first-class concerns alongside concentration risk, not as folded sub-cases.

### 2.8 Publication-bias overlay (Phase 6 critique addition)

McGuire FP et al. 2025 (entry [55], University of Utah, *Curr Rev Musculoskelet Med* 18(12):611–619) flag the literature as showing a structural pattern: **"All the published studies report positive or beneficial effects of BPC-157, suggesting a possible publication bias toward positive findings."** This is a load-bearing interpretive overlay that must be applied across every indication section in this report, not quoted once and dropped.

Operationally, the overlay means:
- Effect-size claims in the Sikirić-cluster animal literature (§4 MSK, §5 GI/visceral/CNS) must be discounted by the unknown rate at which negative or null Sikirić-group experiments were not published.
- The "zero AEs reported" finding across the four Lee-Orlando human pilots (§7, §8.1) is consistent with a publication-bias filter at the individual-clinic level: a clinic that publishes its results in a single peer-reviewed venue (*Altern Ther Health Med*) and runs its own enrollment and AE-elicitation is not a neutral observational substrate.
- The mechanism literature's overwhelmingly positive direction (§3) — angiogenesis up, ECM up, NO modulation favorable, GHR up-regulation favorable — is consistent with the same filter.

The publication-bias overlay is the second blanket interpretive lens, alongside concentration risk, that downstream readers must apply. End-of-section reminders are added at §3.10, §4.10, and §5.10 (see those sections).

## 3. Mechanism of Action

The mechanism corpus is the LEAST Sikirić-concentrated chapter of this entry. Mechanistic specificity (named pathways, in-vitro receptor activation, RT-qPCR / Western readouts) is largely produced by the Chang Gung University Pang group in Taiwan, with Pliva Research Institute providing the EGR-1 / NAB2 wound-site work and one independent collaborator (Diksic / McGill) providing the brain 5-HT regional autoradiography. Even so, the molecular target of BPC-157 — the direct, high-affinity binding partner — remains unidentified in peer-reviewed literature as of 2026.

### 3.1 Angiogenesis pathway: VEGFR2 → Akt → eNOS

The most-replicated mechanistic claim for BPC-157 is angiogenesis modulation through the VEGFR2-Akt-endothelial-NOS axis. In rat hind-limb ischemia and in cultured human umbilical-vein endothelial cells (HUVEC), BPC-157 increased VEGFR2 mRNA and protein expression without changing VEGF-A levels, promoted VEGFR2 internalization, and time-dependently activated the VEGFR2–Akt–eNOS signaling cascade; the endocytosis inhibitor dynasore blocked both internalization and downstream Akt/eNOS phosphorylation [44, animal+in_vitro] [population-mismatch: rat / HUVEC]. The work was performed at Chang Gung Memorial Hospital, Taiwan (Hsieh M-J et al. 2017, *J Mol Med* 95:323–333; PMID 27847966; DOI 10.1007/s00109-016-1488-y) and is the foundational independent (non-Sikirić) experimental support for this central claim.

A parallel route, also from the same Taiwanese group, was reported using isolated rat aorta and HUVEC: BPC-157 induced vasorelaxation that was endothelium-dependent and abolished by L-NAME or by hemoglobin (NO scavengers). Mechanistically, the peptide activated Src kinase, phosphorylated caveolin-1 and eNOS, and reduced the Cav-1:eNOS inhibitory binding interaction — a **VEGF-independent Src–caveolin-1–eNOS** route to NO production [45, in_vitro+animal] [population-mismatch: rat aorta / HUVEC] (Hsieh M-J, Lee C-H, Chueh H-Y, Chang G-J, Pang J-HS, Peng Y-J et al. 2020, *Scientific Reports* 10:17078; PMID 33051527; DOI 10.1038/s41598-020-74022-y).

The 2025 University-of-Utah narrative review by McGuire FP et al. (entry [55], PMID 40789979; PMC12446177) summarizes the dual mechanism as "VEGF-dependent (via VEGFR2–PI3K–Akt–eNOS) and VEGF-independent (via Src–caveolin-1–eNOS) pathways to NO production, supporting angiogenesis, vasodilation, and vascular stability" [55, mechanism_review]. Caveat: review-level synthesis; the load-bearing primary evidence is the two Hsieh papers above.

### 3.2 Nitric oxide system

The NO pathway is implicated across multiple Sikirić-group in-vivo studies through the standard L-NAME (NOS inhibitor) and L-arginine (NO substrate) drug-interaction probes. The interpretation in the originating literature is a "balancing" or modulatory effect on NO-system homeostasis rather than unidirectional agonism or antagonism. The Stupnisek M, Kokot A, Drmic D, Hrelec Patrlj M et al. 2015 anticoagulant-interaction study (PMID 25897838; *PLoS One* 10(4):e0123454; DOI 10.1371/journal.pone.0123454; first-author affiliation J.J. Strossmayer University of Osijek with Sikirić senior at Zagreb — Sikirić-cluster per sub-cluster rule) tests both probes directly in a rat tail-amputation model: BPC-157 counteracted both the prothrombotic effect of L-NAME (5 mg/kg i.p.) and the increased-bleeding effect of L-arginine (100 mg/kg i.p.) [29, animal] [population-mismatch: rat]. Whether the same bidirectional modulation occurs in human hemostasis is unknown; no human probe study exists.

**Alternative-explanation caveat (Phase 6 critique addition).** The Sikirić-group "balancing modulation" framing — that BPC-157 counteracts opposing effects in either direction (pro-thrombotic L-NAME and anti-thrombotic L-arginine) — is **structurally non-falsifiable**: a compound that opposes any imbalance, regardless of direction, cannot be wrong on the bench in the way a unidirectional agonist or antagonist can be wrong. A compound that "fixes" a system whether pushed up or down looks protective in every direction of probing. Critique-grade readers should treat the Stupnisek 2015 result as a documented bidirectional rat-hemostasis pharmacodynamic observation, **not** as evidence of a coherent unifying mechanism. Until a falsifiable mechanism (specific receptor / specific transduction pathway with a measured affinity constant) is identified, "balancing modulation" describes the data without explaining it.

### 3.3 Growth-factor crosstalk: EGR-1 / NAB2

In a Pliva (originator-company) study using full-thickness excisional wounds in db/db diabetic mice and Caco-2 enterocyte cultures, PL 14736 (= BPC-157) accelerated granulation tissue formation, improved collagen organization, and induced expression of the *egr-1* immediate-early gene and its co-repressor *nab2* in non-differentiated Caco-2 cells [41, animal+in_vitro] [population-mismatch: db/db mouse / Caco-2 human colon adenocarcinoma cells] (Tkalčević V-I, Čužić S, Brajša K, Mildner B, Bokulić A, Šitum K, Perović D, Glojnarić I, Parnham MJ 2007, *European Journal of Pharmacology* 570(1–3):212–221; PMID 17628536; DOI 10.1016/j.ejphar.2007.05.072). EGR-1 is a transcription factor with documented roles in PDGF, cytokine, and type-I collagen transcription, providing a plausible upstream node for the granulation-and-fibroblast phenotype repeated across BPC-157 wound studies.

The Tkalčević 2007 study has two distinct findings that are sometimes conflated: (a) PL 14736 stimulated egr-1 / nab2 expression in Caco-2 cells with peak mRNA at 15 minutes in vitro; and (b) in rat subcutaneous sponge implants, the peptide "remained active at wound sites for several hours." Finding (b) is a **local pharmacodynamic** observation, not a plasma half-life measurement. The frequent secondary-literature paraphrase that "Tkalčević 2007 shows BPC-157 has a long half-life" is a misreading: that paper did not measure plasma t½ at all (this point is restated in §6 below where the PK literature is consolidated).

**Independent replication of the EGR-1 / NAB2 finding in a non-Pliva, non-Zagreb laboratory was NOT located** during this retrieval (Section A Finding 8). This is reported as an open gap, not as confirmation. Treat the EGR-1 / NAB2 mechanism as single-source pending independent reconfirmation.

### 3.4 Growth-hormone-receptor up-regulation in tendon fibroblasts

In primary cultures of rat Achilles tendon fibroblasts, BPC-157 at 0.1–0.5 µg/mL dose- and time-dependently up-regulated growth-hormone receptor (GHR) mRNA and protein (RT-qPCR + Western blot); addition of exogenous growth hormone to BPC-157-treated cells produced greater proliferation than GH alone, suggesting potentiation rather than direct GH-mimicry [47, in_vitro] [population-mismatch: rat tendon fibroblast] (Chang C-H, Tsai W-C, Hsu Y-H, Pang J-HS 2014, *Molecules* 19(11):19066–19077; PMID 25415472; PMC6271067; DOI 10.3390/molecules191119066). The same Chang Gung group's earlier in-vitro work showed that BPC-157 accelerated outgrowth of fibroblasts from rat Achilles tendon explants and increased their migration in scratch assays, attributing the effect to activation of the **FAK–paxillin** focal-adhesion pathway [46, in_vitro] [population-mismatch: rat tendon fibroblast] (Chang C-H, Tsai W-C, Lin M-S, Hsu Y-H, Pang J-HS 2011, *J Appl Physiol* 110(3):774–780; PMID 21030672; DOI 10.1152/japplphysiol.00945.2010).

**Critical practitioner-tier misreading flag.** The Chang 2014 paper shows up-regulation of GHR *expression* in tendon-fibroblast cell culture. It does NOT show GH-receptor direct *agonism* (BPC-157 is not a GH analog), and it does NOT show GHRH-receptor binding (the GHRH receptor is anatomically distinct from the GHR and is expressed at the pituitary level). The frequent vendor and practitioner claim that BPC-157 is a "GHRH-receptor agonist" or that it "activates the systemic IGF-1 axis" is **not supported** by primary literature. The conflation appears to arise from acronym similarity (GHR vs GHRH) and is one of the more reliably propagated practitioner-tier errors in BPC-157 commentary. This wiki entry treats GHRH-receptor agonism as `[corpus-unverifiable]`.

### 3.5 Dopaminergic and serotonergic modulation

In Sprague-Dawley rats, a single intraperitoneal dose of BPC-157 at 10 µg/kg administered 40 minutes before α-[¹⁴C]methyl-L-tryptophan tracer significantly reduced regional 5-HT synthesis rate in dorsal thalamus, hippocampus, lateral geniculate body, and hypothalamus, and significantly increased it in substantia nigra reticulata and medial anterior olfactory nucleus. After 7 days of subcutaneous dosing at 10 µg/kg, 5-HT synthesis decreased in dorsal raphe and increased in substantia nigra, lateral caudate, nucleus accumbens, and superior olive [54, animal] [population-mismatch: rat brain] [route-extrapolation: i.p. / s.c.] (Tohyama Y, Sikirić P, Diksic M 2004, *Life Sciences* 76(3):345–357; DOI 10.1016/j.lfs.2004.08.010). The Diksic-group authors explicitly write that they "cannot determine, from this data, the mechanism of this action" — this is descriptive regional pharmacology, not a receptor mechanism. **Per the Phase 6 critique resolution of the §2/§5 double-counting issue, this paper is counted to the Sikirić-Zagreb cluster** consistently throughout this report via the sub-cluster rule (Sikirić co-authorship), even though Diksic is senior at McGill — the aggregate-rule alternative was abandoned. A defensible alternative explanation for the regional 5-HT findings, noted by the authors themselves and worth surfacing for the reader: peripheral dosing with central readouts cannot distinguish CNS-direct action from indirect peripheral-to-CNS signaling (e.g., gut–vagal–CNS effects, peripheral 5-HT pool changes feeding into central tryptophan metabolism).

Adjacent serotonin and dopamine work, all Sikirić-Zagreb, includes:

- **Severe serotonin-syndrome paradigm in rats**: BPC-157 alone has no behavioral or temperature effect but counteracts the induced syndrome [15, animal] [population-mismatch: rat] (Boban Blagaic A, Blagaic V, Mirt M et al. 2005, *Eur J Pharmacol*; PMID 15840402).

- **Amphetamine sensitization / haloperidol supersensitivity**: a single dose of BPC-157 (10 µg/kg i.p.; 10 ng/kg ineffective) given before chronic amphetamine attenuated behavioral effects and blocked the development of haloperidol-induced supersensitivity to amphetamine [10, animal] [population-mismatch: rat] [route-extrapolation: i.p.] (Jelovac N, Sikirić P, Rucman R et al. 1998, *Biol Psychiatry* 43(7):511–519; PMID 9547930; DOI 10.1016/s0006-3223(97)00277-1).

- **MPTP Parkinson model in mice and rats**: BPC-157 (i.p., 10 µg/kg range) attenuates behavioral deficits [7, animal] [population-mismatch: mouse and rat] [route-extrapolation: i.p.] (Sikirić P, Marović A, Matoz W et al. 1999, *J Physiol Paris*).

- **Porsolt forced-swim depression assay**: BPC-157 (10 ng/kg and 10 µg/kg i.p., female rats) reduced immobility comparably to imipramine 30 mg/kg [11, animal] [population-mismatch: rat] [route-extrapolation: i.p.] (Sikirić P, Separović J, Anić T et al. 2000, *J Physiol Paris*).

These CNS effects are documented at peripheral (i.p./s.c./drinking-water) dosing routes with central readouts. **No primary located in this corpus directly measured BPC-157 concentration in CNS tissue or CSF after peripheral dosing.** The "BPC-157 crosses the blood-brain barrier" claim circulating in vendor and forum literature is *inferential* from peripheral-dose / central-readout designs; treat BBB penetration as a hypothesis, not a finding.

### 3.6 Extracellular-matrix and collagen induction

BPC-157 promotes Type I and Type III collagen induction and fibroblast recruitment in multiple tendon, ligament, muscle, and skin wound-healing animal models (covered in §4). At the mechanism level, this is downstream of EGR-1 / NAB2 induction (§3.3) and of the FAK–paxillin and GHR effects (§3.4). Subsequent mechanism reviews (including Sikirić-group reviews and independent reviews) treat EGR-1 / NAB2 induction and FAK–paxillin activation as the two best-replicated cell-level effects beyond the VEGFR2-eNOS axis [55, mechanism_review] [56, mechanism_review]. Within the BPC-157 corpus surveyed for this report, the *only* primary EGR-1 study traceable to BPC-157 specifically is the 2007 Tkalčević Pliva paper; independent replication remains an open gap (per §3.3).

### 3.7 Receptor target

**No specific, peer-reviewed, identified molecular target for BPC-157 has been reported as of 2026.** No high-affinity binding site, receptor, or direct binding partner has been characterized in any indexed peer-reviewed primary located in this retrieval. The independent 2019 Loughborough peer-reviewed review (Gwyer D, Wragg NM, Wilson SL 2019, entry [56], *Cell Tissue Res* 377:153–159; PMID 30915550; DOI 10.1007/s00441-019-03016-8) concluded that "there is still a need to understand the precise healing mechanisms for this therapy to achieve clinical realisation" [56, mechanism_review]. The 2025 independent University-of-Utah review (McGuire FP et al., entry [55]) describes all observed effects as downstream pathway modulation (VEGFR2, ERK1/2, NO, ECM) without naming a primary direct binding partner, and concludes "BPC-157 should be considered investigational" [55, mechanism_review].

The 2025 ResearchSquare preprint by Schlosser proposing BPC-157 binding to SH3 domains of Src-family kinases is **non-peer-reviewed**, originates from a vendor-affiliated lab (Cell Shot Nutrition), and is excluded under the source whitelist. It is flagged only to note that all currently public direct-binding hypotheses are preprint-tier or in-silico, and unvalidated.

### 3.8 Mechanistic claims commonly asserted but lacking primary support

Three claims appear regularly in BPC-157 reviews and practitioner content but could not be backed by retrievable primary literature during this dispatch:

- **GHRH-receptor agonism.** Frequently asserted; no primary peer-reviewed evidence of direct GHRH-R binding was retrievable. The Chang 2014 GHR up-regulation finding is the most likely origin of this conflation (see §3.4). Tagged `[corpus-unverifiable]`.

- **Direct NGF / BDNF induction or receptor activation.** Claims trace to Sikirić in-vivo CNS-injury models showing functional recovery, not to isolated growth-factor binding/induction assays. Tagged `[corpus-unverifiable for a direct, isolated NGF/BDNF claim]`.

- **Mitochondrial / anti-apoptotic mechanism.** Claimed in narrative reviews; the primary support is in-vivo organ-protection (heart, liver, brain) from the Sikirić group, not isolated mitochondrial assays. Tagged `[corpus-unverifiable]`; flagged as concentration-Sikirić-dominant.

### 3.9 Pharmacological-extrapolation caveats

Most mechanism work uses cell culture (HUVEC, rat tendon fibroblasts, Caco-2 cells) or rat tissue (aorta, brain regions) at micromolar peptide concentrations. The plasma concentrations achieved in the only published cross-species PK study (rat IV 20 µg/kg yields Cmax in the low-tens of ng/mL, falling to undetectable by approximately one hour — see §6) are at least one to two orders of magnitude below the micromolar concentrations used in most in-vitro mechanism work. Direct extrapolation from in-vitro mechanism to systemic in-vivo human dosing is therefore speculative. The "pharmacodynamic / pharmacokinetic disconnect" — tissue effects persisting for days while plasma drug is undetectable within minutes — is acknowledged across the mechanism review literature but is not resolved at the primary level (see §6.5 for full development).

### 3.10 Publication-bias reminder (per §2.8 overlay)

Per the McGuire 2025 finding that "all the published studies report positive or beneficial effects of BPC-157, suggesting a possible publication bias toward positive findings," the unidirectional positive results across the §3 mechanism literature — VEGFR2 up, Src/caveolin-1 activated, EGR-1/NAB2 induced, GHR up-regulated, NO modulation "balancing" rather than aggravating, MPTP / cuprizone / serotonin-syndrome models reversed — must be read against the unknown rate of unpublished negative or null Sikirić-group experiments.

## 4. Animal Evidence — Musculoskeletal

**Section consumer notice (per §2 concentration framing and §2.8 publication-bias overlay).** This section reads as **rat in-vivo unless otherwise noted; no independent in-vivo replication of any MSK finding exists** outside the Sikirić-Zagreb cluster. Every dose constant, every Achilles or MCL or quadriceps outcome quoted below, is a Sikirić-group finding. Specialist agents reading this section in isolation must apply the §2.2 concentration arithmetic (Sikirić cluster 75.0% of 52; combined Zagreb-metropolitan 80.8%) and the §2.8 publication-bias overlay (positive-finding-only literature) to every claim. The dose constants (10 µg/kg / 10 ng/kg / 10 pg/kg i.p.) are reported as the doses Sikirić used; they are not "the correct" doses in a regulatory sense.

The animal MSK evidence base is, after the GI/visceral/CNS corpus, the second deepest concentration of single-lab dominance in the BPC-157 literature. Every in-vivo MSK primary located in this retrieval — Achilles tendon transection, Achilles tendon-to-bone detachment, medial collateral ligament transection, quadriceps muscle transection, gastrocnemius crush, segmental bone defect, anticoagulant-interaction tail amputation — originates from the University of Zagreb School of Medicine, Department of Pharmacology (Sikirić group), with first authors at either the Zagreb Department of Pharmacology, affiliated Zagreb clinical departments, or the J.J. Strossmayer University of Osijek (with Sikirić/Seiwerth as senior authors). The only independent MSK-relevant laboratory thread is the Chang Gung University in-vitro tendon-fibroblast work, which replicates cellular-level effects (FAK–paxillin, GHR upregulation) but does NOT independently replicate any in-vivo MSK outcome. The dosing schedule clusters tightly at 10 µg/kg and 10 ng/kg (with a 10 pg/kg confirming low-end arm in Achilles and quadriceps studies), administered once daily either intraperitoneally in saline, per-orally in drinking water at 0.16 µg/mL or 0.16 ng/mL (≈12 mL/rat/day), or topically as 1.0 µg/g neutral cream.

### 4.1 Achilles tendon transection

In transected rat Achilles tendon (5 mm defect proximal to the calcaneal insertion), BPC-157 at 10 µg/kg, 10 ng/kg, or 10 pg/kg intraperitoneal once daily produced significantly improved load-to-failure, load-to-failure per area, and Young's modulus of elasticity versus saline controls at days 1, 4, 7, 10, and 14 post-transection [14, animal] [population-mismatch: rat]. The same paper reported in-vitro that BPC-157 reversed 4-hydroxynonenal (HNE) inhibition of cultured rat tendocyte growth [14, in_vitro] [population-mismatch: rat]. First-author institution: Department of Pharmacology, Medical Faculty, University of Zagreb (Staresinic M, Sebecic B, Patrlj L, Jadrijevic S, Suknaic S, Perovic D, Aralica G, Zarkovic N, Borovic S, Srdjak M, Hajdarevic K, Kopljar M, Batelja L, Boban-Blagaic A, Turcic I, Anic T, Seiwerth S, Sikirić P 2003, *J Orthop Res* 21(6):976–983; PMID 14554208; DOI 10.1016/S0736-0266(03)00110-4).

### 4.2 Achilles tendon-to-bone detachment

In rat Achilles tendon-to-bone detachment, BPC-157 (10 µg/kg or 10 ng/kg i.p. once daily, first dose 30 min post-surgery) accelerated tendon-to-bone reattachment macroscopically, microscopically, and functionally (Achilles functional index) over a 30-day period, and counteracted the aggravation of healing produced by concomitant systemic corticosteroid [16, animal] [population-mismatch: rat] (Krivic A, Anic T, Seiwerth S, Huljev D, Sikirić P 2006, *J Orthop Res* 24(5):982–989; PMID 16583442; DOI 10.1002/jor.20096; first-author affiliation University Hospital Center Zagreb, Department of Surgery, with Sikirić senior at Zagreb Department of Pharmacology). A follow-up study in the same model evaluated days 1–4 post-transection (before collagen healing started) and reported reduced myeloperoxidase activity, reduced inflammatory-cell influx, and improved vascular index versus saline and versus methylprednisolone controls [19, animal] [population-mismatch: rat] (Krivic A, Majerovic M, Jelic I, Seiwerth S, Sikirić P 2008, *Inflamm Res* 57(5):205–210; PMID 18594781; DOI 10.1007/s00011-007-7056-8).

### 4.3 Medial collateral ligament

In rat surgical transection of the medial collateral ligament, BPC-157 administered intraperitoneally (10 µg/kg or 10 ng/kg once daily), orally in drinking water (0.16 µg/mL, ≈12 mL/rat/day), or topically as 1.0 µg/g neutral cream produced consistent functional, biomechanical (increased ultimate load), macroscopic, and histological healing improvements over a 90-day observation in Wistar rats. The paper reports involvement of Type I/III collagen balance and early enhanced vascularization [23, animal] [population-mismatch: rat] (Cerovecki T, Bojanic I, Brcic L, Radic B, Vukoja I, Seiwerth S, Sikirić P 2010, *J Orthop Res* 28(9):1155–1161; PMID 20225319; DOI 10.1002/jor.21107; first-author affiliation University Hospital of Traumatology Zagreb, Sikirić senior).

### 4.4 Quadriceps transection

In rat complete transverse transection of quadriceps muscle (1.0 cm proximal to patella), BPC-157 at 10 µg/kg, 10 ng/kg, or 10 pg/kg intraperitoneal once daily improved biomechanical load-to-failure, walking-track function, and microscopic muscle-fiber reconnection (desmin-positive regenerating fibers) versus saline controls across 72 days; controls retained a definitive defect that was not spontaneously compensated [17, animal] [population-mismatch: rat] (Staresinic M, Petrovic I, Novinscak T, Jukic I, Pevec D, Suknaic S, Kokic N, Batelja L, Brcic L, Boban-Blagaic A, Zoric Z, Ivanovic D, Ajduk M, Sebecic B, Patrlj L, Sosa T, Buljat G, Anic T, Seiwerth S, Sikirić P 2006, *J Orthop Res* 24(5):1109–1117; PMID 16609979; DOI 10.1002/jor.20089).

### 4.5 Gastrocnemius crush and corticosteroid co-administration

In rat gastrocnemius muscle crush injury (controlled impulse 0.4653 Ns, 0.727 Ns/cm²), BPC-157 dissolved in saline (10 µg/kg, 10 ng/kg i.p.) or applied locally in neutral cream (0.01–1.0 µg/g) once daily up to 14 days reduced hematoma, edema, and post-injury leg contracture and decreased serum creatine kinase and lactate dehydrogenase versus saline/vehicle controls [20, animal] [population-mismatch: rat] (Novinscak T, Brcic L, Staresinic M, Jukic I, Radic B, Pevec D, Mise S, Tomasovic S, Brcic I, Banic T, Jakir A, Buljat G, Anic T, Zoricic I, Romic Z, Seiwerth S, Sikirić P 2008, *Surg Today* 38(8):716–725; PMID 18668315; DOI 10.1007/s00595-007-3706-2).

In rat muscle injury under systemic corticosteroid (6α-methylprednisolone) impairment, BPC-157 (10 µg/kg, 10 ng/kg i.p. or local 1.0 µg/g cream) counteracted the corticosteroid-induced delay in muscle healing and restored function toward control values [24, animal] [population-mismatch: rat] (Pevec D, Novinscak T, Brcic L, Sipos K, Jukic I, Staresinic M, Mise S, Brcic I, Kolenc D, Klicek R, Banic T, Sever M, Kocijan A, Berkopic L, Radic B, Buljat G, Anic T, Zoricic I, Bojanic I, Seiwerth S, Sikirić P 2010, *Med Sci Monit* 16(3):BR81–88; PMID 20190686). This is the lone Section B primary directly addressing a pharmacological-interaction signal (corticosteroid co-administration) at the MSK injury site. The direction is protective.

### 4.6 Segmental bone defect (rabbit)

In rabbit segmental osteoperiosteal radius defect (0.8 cm, mid-left-radius, which remained incompletely healed in all control rabbits for 6 weeks), BPC-157 percutaneously delivered locally (10 µg/kg) into the defect, or intramuscularly intermittent (10 µg/kg on postoperative days 7, 9, 14, 16) or continuous (10 µg/kg or 10 ng/kg daily, days 7–21) significantly improved radiographic callus surface, microphotodensitometric mineralization, and quantitative histomorphometric bone-defect closure versus saline controls at 2-week intervals through 6 weeks; effects were comparable to autologous bone marrow application [9, animal] [population-mismatch: rabbit] (Sebecic B, Nikolic V, Sikirić P, Seiwerth S, Sosa T, Patrlj L, Grabarevic Z, Rucman R, Petek M, Konjevoda P, Jadrijevic S, Perovic D, Slaj M 1999, *Bone* 24(3):195–202; PMID 10071911; DOI 10.1016/S8756-3282(98)00180-X). This is the lone non-rat MSK animal primary in the cited corpus.

### 4.7 Tendon-to-bone and tendon-fibroblast in vitro — the ONLY independent MSK thread

Two Chang Gung University in-vitro studies are the only MSK-relevant primaries from outside the Sikirić-Zagreb cluster. (a) In primary cultures of rat Achilles tendon fibroblasts and tendon explants, BPC-157 dose-dependently accelerated fibroblast outgrowth, increased cell survival under H₂O₂ oxidative stress, and increased migration in transwell assay, linked to FAK–paxillin activation [46, in_vitro] [population-mismatch: rat tendon fibroblasts] (Chang C-H et al. 2011, see §3.4). (b) The same group's follow-up showed dose- and time-dependent GHR mRNA + protein up-regulation in tendon fibroblasts; GHR up-regulation potentiated growth-hormone-stimulated cell proliferation [47, in_vitro] [population-mismatch: rat tendon fibroblasts] (Chang C-H et al. 2014, see §3.4).

**These two in-vitro Chang Gung primaries are the entire independent replication thread for MSK-relevant BPC-157 effects.** Neither paper independently replicates an in-vivo MSK finding (Achilles, MCL, quadriceps, gastrocnemius, bone defect, anticoagulant interaction). The state of the literature is therefore: independent confirmation of *cellular* effects (FAK–paxillin, GHR expression) on rat tendon fibroblasts; **no independent confirmation of any in-vivo MSK outcome** in rat or rabbit.

### 4.8 Steroid- and NSAID-induced MSK lesions

BPC-157 counteracts corticosteroid impairment of MSK healing in three Sikirić-Zagreb primaries (Krivic 2006 [16]; Krivic 2008 [19]; Pevec 2010 [24]). NSAID-induced GI lesions are a separate corpus (§5.5 below; the load-bearing primaries are GI rather than MSK). For MSK specifically, the steroid-interaction signal is the most directly probed pharmacological-interaction signal in this section.

### 4.9 Anticoagulant interaction (Stupnisek 2015)

In a rat tail-amputation model, with or without concomitant intravenous heparin (10 mg/kg) or intragastric warfarin (1.5 mg/kg/day for 3 days), BPC-157 (10 µg/kg or 10 ng/kg i.p.; or 10 µg/kg i.v. under heparin; or 10 µg/kg i.g. under warfarin) reduced bleeding time and haemorrhage and counteracted anticoagulant-induced thrombocytopenia versus controls [29, animal] [population-mismatch: rat] (Stupnisek M, Kokot A, Drmic D, Hrelec Patrlj M, Zenko Sever A, Kolenc D, Radic B, Suran J, Bojic D, Vcev A, Seiwerth S, Sikirić P 2015, *PLoS One* 10(4):e0123454; PMID 25897838; DOI 10.1371/journal.pone.0123454). The paper also reports that BPC-157 counteracts the prothrombotic effect of L-NAME (5 mg/kg i.p.) and the antithrombotic / increased-bleeding effect of L-arginine (100 mg/kg i.p.), which the authors interpret as a "balancing" modulation of the NO–hemostasis axis.

This is the single most risk-floor-relevant animal finding for BPC-157: it directly probes pharmacodynamic interaction with two clinically used anticoagulants (heparin, warfarin) plus the NO-synthase pathway implicated in hemostasis. The direction of effect (reduced bleeding under heparin/warfarin in rats) is NOT a safety endorsement for human anticoagulant co-use — it is a pharmacodynamic-interaction signal that requires §7 and §8 to convert into contraindication or monitoring language. Stupnisek M is at J.J. Strossmayer University of Osijek; Seiwerth and Sikirić senior at Zagreb Department of Pharmacology / Pathology. Per the sub-cluster rule (Osijek is a co-affiliated Croatian medical faculty; project direction and senior authorship remain Sikirić/Seiwerth Zagreb), this primary is **Sikirić-Zagreb cluster**.

### 4.10 Section-level concentration

Across the eleven Section B primaries, the Sikirić-Zagreb cluster share is **9/11 = 82% including the two in-vitro Chang Gung tendon-fibroblast papers; restricting to in-vivo studies, the share is 9/9 = 100%** (the only non-cluster primaries are the two Chang Gung in-vitro tendon-fibroblast papers, which are not in-vivo MSK studies). Read every in-vivo MSK claim in this section against the §2 concentration framing: no independent in-vivo MSK replication has been published as of this retrieval.

### 4.11 Alternative-explanation surfacing (Phase 6 critique addition)

The §4 in-vivo MSK phenotype — accelerated Achilles, MCL, quadriceps, gastrocnemius, and bone-defect healing under BPC-157 — is presented in the Sikirić-cluster literature as BPC-157-**specific**, with mechanistic specificity attributed to VEGFR2/eNOS, FAK–paxillin, GHR up-regulation, and EGR-1 / NAB2 (§3). An alternative explanation that the cluster literature does not surface is that this phenotype is consistent with a **generic anti-inflammatory action** that many small molecules and peptides share: reduced edema, reduced inflammatory-cell influx, reduced myeloperoxidase activity, and improved post-injury vascular index all read as anti-inflammatory rather than as compound-specific. The corticosteroid-counteraction signal (§4.8) is consistent with the BPC-157 effect operating in an opposing direction to corticosteroid-induced inflammation suppression — which is again a generic anti-inflammatory story, not a unique mechanism. Until a falsifiable BPC-157-specific molecular target is identified (§3.7 notes none is) and until independent in-vivo MSK replication exists outside the Sikirić cluster, the alternative reading "the Sikirić MSK results document a generic anti-inflammatory phenotype attributed to BPC-157 in a single-lab corpus" remains a defensible and parsimonious reading of the same data.

### 4.12 Publication-bias reminder (per §2.8 overlay)

Per McGuire 2025, the §4 MSK literature is positive-finding-only across every published outcome metric (load-to-failure, biomechanical strength, walking-track function, histomorphometric closure). Specialist agents should discount the effect-size headline numbers (e.g., "BPC-157 is comparable to autologous bone marrow at radial bone-defect closure" from Sebecic 1999 [9]) by the unknown rate at which negative or null Sikirić-group MSK experiments were not submitted or not published.

## 5. Animal Evidence — GI, Visceral, and CNS

**Section consumer notice (per §2 concentration framing and §2.8 publication-bias overlay).** This section reads as **rat in-vivo unless otherwise noted; 17 of 18 cited primaries (94%) are Sikirić-Zagreb cluster**, and the lone "independent" primary (Xue 2004) is itself part of the 3-paper Xi'an Fourth Military Medical University single-institution cluster (§2.3). No GI / visceral / CNS finding has been independently replicated outside the Zagreb-or-Xi'an cluster axis. Specialist agents reading this section in isolation must apply the §2.2 concentration arithmetic and the §2.8 publication-bias overlay before quoting any numerical or directional outcome.

The GI/visceral/CNS sub-corpus is the deepest single-lab concentration in the BPC-157 evidence base — 17 of 18 cited primaries (≈94%) trace to the Sikirić-Zagreb cluster. The lone non-cluster primary, Xue X-C et al. 2004 (*World J Gastroenterol* 10(7):1032–1036), is now reclassified under Phase 4.75 IC-10 / C6 from Second Military Medical University Shanghai to **Fourth Military Medical University Xi'an** — i.e., the same Xi'an cluster as Xu 2020 (preclinical safety) and He L 2022 (PK). Net effect: there is exactly ONE partial-independent in-vivo gastric-ulcer replication of a Sikirić finding (Xue 2004), and that single paper now joins the 3-paper Xi'an cluster that also produced the only independent PK and safety packages. This is the secondary concentration finding flagged in the Phase 4.75 warnings: the "independent Chinese signal" is single-institution, not multi-institution.

### 5.1 Gastric ulcer / cytoprotection

The foundational cytoprotection paper screened BPC-157 against gastric lesions induced in rats by 96% ethanol, restraint stress, indomethacin, and capsaicin neurotoxicity, establishing the original "stable gastric pentadecapeptide" phenotype that drives all downstream visceral claims [4, animal] [population-mismatch: rat] (Sikirić P, Petek M, Rucman R, Seiwerth S et al., later codified in Sikirić P, Seiwerth S, Grabarevic Z et al. 1996, *Dig Dis Sci* 41(8):1604–1614; PMID 8769287). In cysteamine-induced duodenal-ulcer rats, BPC-157 was reported equipotent to cimetidine, ranitidine, bromocriptine and other reference antiulcer agents in both intact and gastrectomized animals [5, animal] [population-mismatch: rat] (Sikirić P, Seiwerth S, Grabarevic Z et al. 1997, *Dig Dis Sci* 42(5):1029–1037; PMID 9149058).

A direct head-to-head in the acetate chronic gastric ulcer rat model placed BPC-157 at approximately 800 ng/kg against famotidine at 40 mg/kg with comparable healing — the often-quoted "50× more potent than famotidine" comparison. **The ratio is dose-mass, not molar**, and the claim is sometimes propagated without that qualifier [50, animal] [population-mismatch: rat] [route-extrapolation: BPC 157 i.g./i.p., famotidine i.g.] (Xue X-C, Wu Y-J, Gao M-T et al. 2004, *World J Gastroenterol* 10(7):1032–1036; per Phase 4.75 IC-10 / C6, first-author institution is **Fourth Military Medical University, Xi'an, China**, joining the Xi'an cluster).

### 5.2 Robert's intragastric absolute-alcohol model — the vascular-thesis anchor

In Robert's intragastric absolute-alcohol gastric-lesion model the Sikirić group describes a multi-organ "escalated peripheral and central syndrome" — intracranial (superior sagittal sinus) hypertension, brain swelling, portal and caval hypertension, azygos vein failure (as a failed collateral pathway), multi-organ congestion, electrocardiogram disturbances, and heart/lung/liver/kidney lesions — reportedly reversed by BPC-157 [37, animal] [population-mismatch: rat] (Gojkovic S, Krezic I, Vranes H, Drmic D, Sikirić Suncana et al. 2021, *Biomedicines*; PMC8533388). This is the load-bearing primary behind the "vascular recruitment / collateral-vessel" thesis that the Sikirić group developed as the unifying mechanism for BPC-157's reported organ-protection phenotype.

### 5.3 Colitis and the IBD program

In a DSS/cysteamine colitis combined with a colon-colon-anastomosis model, BPC-157 (10 µg/kg or 10 ng/kg i.p., or 0.16 µg/mL in drinking water) heals both lesions; the same paper reports counteraction of cuprizone-induced brain injuries and motor disability — the load-bearing primary linking IBD and a multiple-sclerosis-like model [28, animal] [population-mismatch: rat] (Klicek R, Sever M, Radic B et al. 2013–2014, *Eur J Pharmacol*; PMID 24304574). Note: per Phase 4.75 IC-10 / C7 correction, the author order is **Klicek R, Sever M** (not Sever M, Klicek R as some earlier dispatches mis-cited).

In an ileoileal anastomosis rat model — the animal companion to the Pliva PL 14736 ulcerative-colitis program — BPC-157 promotes healing (Vuksic T et al. 2007, *Surg Today* 37(9):768–777; PMID 17713731). This primary is documentation that the Pliva PL-10/PLD-116/PL 14736 program existed at Phase 2 stage, but the paper is animal evidence, not human evidence (see §7 for the human-evidence reconciliation).

### 5.4 Fistula models

In a colovesical / colocutaneous fistula rat model, BPC-157 (10 µg/kg or 10 ng/kg i.p. or in drinking water) is reported to induce closure not seen in controls [30, animal] [population-mismatch: rat] (Grgic T, Sever M, Klicek R et al. 2016, *Eur J Pharmacol* 780:1–7; PMID 26875638). In an esophagocutaneous fistula rat model, BPC-157 similarly drives closure with the authors positioning it against esophagitis and lower-esophageal-sphincter failure [27, animal] [population-mismatch: rat] (Cesarec V, Becejac T, Misic M et al. 2013, *Eur J Pharmacol* 701(1–3):203–212). These two primaries are the basis for the "fistula closure" marketing claims; both are rat, both Sikirić-Zagreb, both lack independent replication.

### 5.5 Hepatic models

In paracetamol-induced acute hepatotoxicity rats, BPC-157 (10 µg, 10 ng, 10 pg/kg, i.p. or i.g., µg-ng range effective) attenuates liver necrosis and counteracts the associated generalised convulsions and brain damage at high hepatotoxic doses — a frequently cited "brain–gut axis after liver injury" data point [25, animal] [population-mismatch: rat] [route-extrapolation: i.p. and i.g.] (Ilic S, Drmic D, Zarkovic K et al. 2010, *J Physiol Pharmacol*). In CCl₄-induced liver injury rats, BPC-157 administered intragastrically or intraperitoneally prevents necrosis and fatty change [2, animal] [population-mismatch: rat] (Sikirić P, Seiwerth S, Grabarevic Z et al. 1993, *Life Sci* 53(18):PL291–PL296; PMID 7901724).

These two primaries surface the **hepatic monitoring biomarkers** for §9 risk-floor (LFTs: ALT, AST, bilirubin; ALP as adjunct), since both papers describe necrosis / fatty change that would manifest as transaminitis and hyperbilirubinemia in human dosing.

### 5.6 Pancreatic

In bile-duct-ligation acute pancreatitis rats, BPC-157 is reported salutary as both protective and healing agent — the canonical pancreatitis primary [8, animal] [population-mismatch: rat] (Petrovic I, Dobric I, Drvis P et al. 1996, *Dig Dis Sci*; PMID 8689934). **The cerulein-pancreatitis primary frequently invoked in secondary literature was NOT located** in this retrieval; the cerulein link in many secondary writeups appears traceable to review-level extrapolation, not a Sikirić cerulein primary. Tagged `[corpus-unverifiable for "BPC 157 + cerulein primary"]`. The pancreatic indication thus surfaces **serum lipase and amylase** (and CK as a non-specific tissue-injury adjunct) for §9 monitoring rationale.

### 5.7 CNS models

CNS models in the Sikirić-Zagreb corpus span dopaminergic-system models (MPTP Parkinson model; amphetamine sensitization; haloperidol supersensitivity), serotonergic-system models (severe serotonin syndrome; Porsolt forced-swim), regional 5-HT autoradiography (the McGill collaboration), hippocampal ischemia/reperfusion (Vukojević 2020, PMC7428500), superior-sagittal-sinus permanent occlusion (Gojkovic, Krezic, Vrdoljak et al. 2021), and primary abdominal-compartment-syndrome (Strbe S, Gojkovic S, Krezic I et al. 2021, *Front Pharmacol*; PMID 34966273; PMC8710746). Across all CNS findings, the administration route in the primary was peripheral (i.p., i.g., or drinking water), **not intracerebroventricular**. The "BPC-157 crosses the blood-brain barrier" claim is *inferential* from peripheral-dose / central-readout designs; no primary identified in this pass measures CNS pharmacokinetics directly.

Individually:

- **MPTP Parkinson model (mouse and rat)** — BPC-157 (i.p., 10 µg/kg range) attenuates behavioural deficits [7, animal] [population-mismatch: mouse and rat] [route-extrapolation: i.p.] (Sikirić P, Marović A, Matoz W et al. 1999, *J Physiol Paris*).

- **Amphetamine sensitization / haloperidol supersensitivity** — BPC-157 (10 µg/kg i.p.; 10 ng/kg ineffective) attenuates amphetamine behavioral sensitization [10, animal] [population-mismatch: rat] [route-extrapolation: i.p.] (Jelovac N, Sikirić P, Rucman R et al. 1998, *Biol Psychiatry* 43(7):511–519; PMID 9547930; DOI 10.1016/s0006-3223(97)00277-1).

- **Severe serotonin syndrome** — BPC-157 alone is without behavioral or temperature effect but counteracts the induced syndrome [15, animal] [population-mismatch: rat] (Boban Blagaic A, Blagaic V, Mirt M et al. 2005, *Eur J Pharmacol*; PMID 15840402).

- **Regional 5-HT autoradiography** — covered in §3.5 (Tohyama Y, Sikirić P, Diksic M 2004) [54, animal] [population-mismatch: rat] [route-extrapolation: peripheral → CNS readout]. Per the Phase 6 critique cluster-rule unification, Tohyama 2004 is counted to the Sikirić-Zagreb cluster everywhere (see §2.2 and §2.3).

- **Porsolt forced-swim depression** — BPC-157 (10 ng/kg and 10 µg/kg i.p., female rats) reduces immobility comparably to imipramine 30 mg/kg [11, animal] [population-mismatch: rat] [route-extrapolation: i.p.] (Sikirić P, Separović J, Anić T et al. 2000, *J Physiol Paris*).

- **Hippocampal I/R (bilateral common-carotid occlusion)** — BPC-157 ameliorates neuronal damage and memory/locomotor deficits [34, animal] [population-mismatch: rat] [route-extrapolation: peripheral] (Vukojević J, Siroglavić M, Kasnik K et al. 2020, *Brain Behav*; PMC7428500).

- **Permanent superior-sagittal-sinus occlusion** — BPC-157 rapidly recruits collateral vessels and overwhelms the occlusion syndrome [38, animal] [population-mismatch: rat] (Gojkovic S, Krezic I, Vrdoljak B et al. 2021).

- **Primary abdominal-compartment-syndrome (intra-abdominal hypertension)** — BPC-157 reverses the chain of harmful events via improvement of the venous system [36, animal] [population-mismatch: rat] (Strbe S, Gojkovic S, Krezic I et al. 2021, *Front Pharmacol*; PMID 34966273).

### 5.8 Route-extrapolation caveats

Across all CNS findings (items 5.7), the primary route was peripheral (i.p., i.g., or drinking water), not intracerebroventricular. **No cited primary measured CNS pharmacokinetics directly.** The "BPC-157 crosses the BBB" claim is inferential from peripheral-dose / central-readout designs; treat BBB penetration as a hypothesis, not a finding (restated from §3.5).

### 5.9 Section-level concentration

17 of 18 cited primaries (94%) trace to the Sikirić-Zagreb cluster under the sub-cluster rule. **Per the Phase 6 critique resolution of the §2/§5 double-counting contradiction, Tohyama 2004 [54] is counted to the Sikirić-Zagreb cluster everywhere in this report** — including the §2 aggregate enumeration — via Sikirić co-authorship under the sub-cluster rule. The prior synthesis's parallel rule ("§2 counts Tohyama as independent because Diksic senior at McGill; §5 counts Tohyama as Sikirić via co-authorship") produced contradictory cluster arithmetic for the same paper and has been retired. The lone unambiguous non-cluster primary in this section is Xue 2004 [50]; per the Phase 4.75 IC-10 / C6 reclassification, Xue 2004 is grouped with the Fourth Military Medical University Xi'an cluster (joining Xu 2020 and He L 2022). The "partial-independent in-vivo replication" in the GI domain is therefore one paper from a 3-paper Xi'an institutional cluster — not three independent confirmations.

### 5.10 Publication-bias reminder (per §2.8 overlay)

Per McGuire 2025, the §5 GI/visceral/CNS literature is positive-finding-only across every published outcome metric — gastric-ulcer healing, ileoileal anastomosis healing, fistula closure, hepatic-protection, pancreatitis-protection, MPTP/cuprizone/serotonin-syndrome reversal, hippocampal I/R neuroprotection, SSS-occlusion collateral recruitment, abdominal-compartment-syndrome reversal. Specialist agents should discount the directional consistency of these findings by the unknown rate at which negative or null Sikirić-group experiments were not published.

## 6. Pharmacokinetics, Routes, and Stability

The pharmacokinetic literature on BPC-157 is far sparser than the mechanism and animal-effect literature, and is built around exactly one cross-species PK paper. The story this section tells is, after honest review: one animal PK paper from one Chinese institution, with no human PK data despite frequent vendor and influencer claims to the contrary.

### 6.1 The He L 2022 cross-species PK paper — the only formal PK study, rat + dog only, no humans

**The He L 2022 paper covers rats and beagle dogs only. There are NO human subjects in this paper.** This sentence is the single most important correction in this rebuild. The S2-era dispatch cited this paper as evidence of human pharmacokinetics; that citation was a misattribution and is the suspected fabrication-vector that prompted the entire BPC-157 corpus rebuild. Sections D, E, and F all independently confirm rat+dog only after Phase 4.75 IC-10 triangulation.

He L, Feng D, Guo H, Zhou Y, Li Z, Zhang K, Zhang W, Wang S, Wang Z, Hao Q, Zhang C, Gao Y, Gu J, Zhang Y, Li W, Li M (2022). "Pharmacokinetics, distribution, metabolism, and excretion of body-protective compound 157, a potential drug for treating various wounds, in rats and dogs." *Frontiers in Pharmacology* 13:1026182; DOI 10.3389/fphar.2022.1026182; PMID 36588717; PMC9794587. First-author institution: **State Key Laboratory of Cancer Biology, Department of Biopharmaceutics, School of Pharmacy, Air Force Medical University, Xi'an, China** (per Phase 4.75 IC-10 / C1 resolution; this is the same Xi'an institution as the Xu 2020 preclinical safety package below).

The numerical PK from this paper, verbatim from the article body and Tables 1–3:

- **Rat IV 20 µg/kg (n=324 Sprague-Dawley across the full study):** mean plasma elimination half-life **t½ = 15.2 min**; AUC₀–t = **399 ng·min/mL** [48, animal] [population-mismatch: rat] [route: IV].
- **Rat IM 20, 100, 500 µg/kg:** Cmax 12.3, 48.9, and 141 ng/mL respectively; **Tmax = 3 min at every dose** [48, animal] [population-mismatch: rat] [route: IM].
- **Rat IM absolute bioavailability:** 18.82%, 14.49%, 19.35% at the three doses (i.e., **F% ≈ 14–19% across the dose range, rat**) [48, animal] [population-mismatch: rat] [route: IM vs IV reference].
- **Repeated IM dosing in rat (100 µg/kg × 7 days):** plasma C–t curve and PK parameters similar to single dose, with only a slight increase in Cmax and AUC — argues against meaningful accumulation in rodents under daily dosing [48, animal] [population-mismatch: rat] [route: IM].
- **Beagle dog IV 6 µg/kg, then IM 6, 30, 150 µg/kg:** dose-linear PK; t½ <30 min both species; Tmax within 9 min for IM dog; **dog IM F% = 45–51%** across the three doses; Cmax at 30 µg/kg IM dog = **3.30 ± 0.51 ng/mL** [48, animal] [population-mismatch: beagle dog] [route: IM vs IV reference].
- **[³H]-BPC-157 radiotracer distribution and excretion (rat IM 100 µg/300 µCi/kg):** total radioactivity detected in all tissues by 3 min; by 10 min the **kidney** concentration (223 ng-Eq/g) exceeded plasma (150 ng-Eq/mL); by 1 h kidney reached ~560 ng-Eq/g, the highest of any tissue [48, animal] [population-mismatch: rat] [route: IM]. Excretion was via **urine and bile**; [³H]BPC-157 was rapidly degraded to small peptide fragments and individual amino acids that entered normal amino acid metabolism. **This is the only direct evidence on BPC-157 distribution and metabolic fate in any species** [48, animal] [population-mismatch: rat].

The He L 2022 paper did NOT test oral, subcutaneous, intraperitoneal, intragastric, intranasal, sublingual, or topical routes. The widespread practitioner-tier claim that "BPC-157 has good bioavailability" routinely drops both the route (IM, not oral) and the species (rat / dog, not human) from this primary; the wiki must not propagate this conversion.

### 6.2 Oral PK — primary absence finding

**No published primary supports oral pharmacokinetics in any species.** The repeated practitioner-literature claim that "oral BPC-157 has approximately 3% bioavailability" or that "BPC-157 arginate has approximately 90% oral bioavailability" does not correspond to any peer-reviewed paper located during this dispatch. The Diagen WO2014142764A1 patent contains in-vitro HPLC stability data (§6.4 below) but does NOT contain in-vivo oral bioavailability measurements. The "3% acetate vs 90% arginate oral F%" claim has zero primary backing and is the most prominent fabrication-risk node in BPC-157 marketing copy `[corpus-unverifiable; absence finding]`.

Rat intragastric (i.g.) and per-oral (p.o., drinking water) administration is documented in Sikirić 1994 (Sikirić P, Seiwerth S, Grabarevic Z, Rucman R, Petek M, Jagic V et al., *Life Sci* 1994;54:PL63–PL68; DOI 10.1016/0024-3205(94)00796-9) at 10 µg/kg or 10 ng/kg i.g. or p.o., with biological activity against gastric/duodenal lesions equivalent to i.p. administration [3, animal] [population-mismatch: rat]. **This establishes that i.g./p.o. routes produce biological effects in rats — it does NOT establish that systemic plasma exposure equals parenteral exposure.** The He L 2022 IV/IM PK study did not test the i.g./p.o. route, so the route-to-effect relationship for oral BPC-157 has been measured pharmacodynamically (effect on ulcer area, sphincter pressure) but not pharmacokinetically (plasma Cmax, AUC, F%). All claims of "oral bioavailability" in rats are inferred from pharmacodynamic equipotency, not measured F%.

### 6.3 Stability — the 24-hour gastric-juice claim and its provenance

The repeatedly cited claim that **"BPC-157 is stable in human gastric juice for more than 24 h"** is foundational to the entire "stable gastric pentadecapeptide" framing and underlies essentially every "orally bioavailable" inference made about the peptide. The originating measurement traces to Sikirić P, Petek M, Rucman R, Seiwerth S, Grabarevic Z, Rotkvic I et al. 1993 (*J Physiol Paris* 87(5):313–327; DOI 10.1016/0928-4257(93)90038-U; **PMID 8298609** per Phase 4.75 IC-10 / C2 resolution). The 1993 paper is a hypothesis and overview, not a self-contained stability-assay paper with a degradation-versus-time curve [1, animal/mechanism-originating-description].

The Phase 4.75 corpus warning on this point: the 1993 *J Physiol Paris* primary text is **paywalled** and was not directly retrievable during the rebuild dispatch. Verification of the 24-h stability figure traces through a 2025 Inflammopharmacology commentary paraphrase of the 1993 original. The figure recurs without independent degradation-vs-time curves in subsequent Sikirić-group reviews (Sikirić P et al. 2020, *Gut Liver* 14(2):153–167; the mdpi 2022 *Biomedicines* 10(12):3221 review; Seiwerth S et al. 2021, *Front Pharmacol* 12:627533; PMC8275860). **No independent (non-Zagreb, non-Pliva, non-Diagen) reconfirmation of 24-h gastric-juice stability has been retrieved.** Treat the 24-h figure as single-source Zagreb-Pliva lineage, propagated through Sikirić-group reviews.

### 6.4 The Diagen patent and the arginate-vs-acetate stability differential

Three salt forms appear in the published and patent literature (recapitulated from §1): acetate (standard), L-arginine di-salt ("arginate" or PDA), and trifluoroacetate (residual counterion). The Diagen patent WO2014142764A1 (Rucman R, Pflaum Z, inventors; 2014) reports in-vitro HPLC stability data:

| Condition | Acetate intact | Arginate intact |
|---|---|---|
| Simulated gastric juice, pH 3.0, 5 h | 0.08% | 84.9% |
| Water, 50 °C, 388 h | 21.30% | 99.01% |
| Water, 100 °C, 1 h | 56.80% | 99.08% |

[Diagen WO2014142764A1, vendor_label / patent — used only for in-vitro chemical stability comparison, never grounding any in-vivo PK or efficacy claim]. **Peer-reviewed independent replication of these HPLC stability values has NOT been located in this retrieval.** The patent figure has not been verified outside Diagen / vendor reproductions. The corporate lineage from Pliva (originator company) to Diagen (Slovenian successor entity continuing the BPC program) is itself a Zagreb-metropolitan / regional industrial cluster. Treat the arginate-vs-acetate differential as single-source patent data pending independent peer-reviewed reproduction.

### 6.5 The pharmacodynamic / pharmacokinetic disconnect

All major review papers acknowledge that BPC-157 produces tissue-level biological effects (angiogenesis, granulation, gene expression) that persist for days to weeks after the plasma drug is undetectable (rat IV t½ = 15.2 min; the prototype peptide is undetectable in rat plasma by approximately 4 h post-dose). Mechanistic explanations include gene-program initiation, local tissue binding with prolonged on-site activity, and downstream signaling-cascade persistence after the upstream trigger has cleared. These explanations are proposed across the mechanism review literature (see [55] McGuire 2025 and [56] Gwyer 2019) but **have not been resolved in primary literature.** The Tkalčević 2007 paper's report of wound-site activity for several hours [41, animal+in_vitro] is a local pharmacodynamic finding (sponge-implant residence and effect on egr-1 expression), not a plasma half-life measurement, and is regularly misrepresented as a plasma PK datum.

**Null-mechanism alternative (Phase 6 critique addition).** The mechanism review literature frames the PD/PK disconnect as an open mechanism question — i.e., as evidence that BPC-157 must be doing something biologically nontrivial that is mechanistically interesting and not yet fully characterized. A defensible alternative reading is that the disconnect indicates **the compound is largely inert at systemic concentrations** and that the persistent tissue effects observed in the Sikirić in-vivo models reflect (a) vehicle / saline effects, (b) injection-site mechanical or osmotic effects unrelated to BPC-157-specific bioactivity, (c) general anti-inflammatory action shared by many small peptides and excipients, or (d) the local-residence "pharmacodynamic" effect reported by Tkalčević 2007 being an artifact of the sponge-implant model rather than a compound-specific property. None of these alternatives can be ruled out by the existing PK and PD data because the upstream molecular target of BPC-157 is unknown (§3.7) and because no independent replication of the in-vivo MSK or GI in-vivo effects exists outside the Sikirić cluster (§2.5). A PD/PK disconnect in a literature with a single dominant lab and no identified molecular target is at least as consistent with compound inertness as with mechanism complexity. The mechanism-complexity reading is the Sikirić-cluster framing; the inertness reading is the null-hypothesis framing. Both should be held open.

### 6.6 The Lee & Burgess 2025 IV pilot — corrects the "human PK" misattribution

The Lee E & Burgess K 2025 IV pilot in n=2 healthy adults (*Altern Ther Health Med* 31(5):20–24; PDF alternative-therapies.com/oa/pdf/11513.pdf; per Phase 4.75 IC-10 / C4, **co-author initial K**) measured clinical safety labs (CMP, CBC, CPK isoenzymes, BNP, TSH, RBC magnesium, hs-CRP) and vital signs before, during, and after a 10 mg (day 1) and 20 mg (day 2) IV infusion in 250 mL saline over 1 h. **No plasma BPC-157 concentrations were measured; no Cmax/t½/AUC was derived; no bioavailability was established.** This is a safety dataset, not a pharmacokinetic dataset [53, open_label].

The 2025 Cambridge repository review paraphrases this paper as showing "plasma BPC-157 concentrations returned to baseline within 24 h" (Cambridge mechanism review; not retained in numbered bibliography). **This paraphrase is not supported by the actual primary** — the primary did not measure plasma BPC-157 at all. This is an example of citation drift through a review layer, and is flagged here as a citation-integrity discrepancy. The honest inferential strength of Lee & Burgess 2025 is: 10–20 mg single-day IV is tolerated in 2 healthy adults; nothing more.

### 6.7 Pliva-era human PK — abstract-only

An older Pliva-era human PK abstract exists for the rectal/enema PL 14736 form: Veljaca M, Pavic-Sladoljev D, Mildner B, Brajsa K, Bubenik M, Stipanicic S et al. 2003, *Gut* 51(Suppl III):A309 ("Safety, tolerability and pharmacokinetics of PL 14736, a novel agent for treatment of ulcerative colitis, in healthy male volunteers") [42, open_label] `[corpus-unverifiable for numerical PK parameters — abstract-only, not retrievable as full text]`. The accompanying Phase 2 RCT abstract (Ruenzi M et al. 2005, *Gastroenterology* 128:A584) is also abstract-only [43, rct]. **No peer-reviewed human PK full paper for any BPC-157 form has been published. The He L 2022 paper is animal-only.**

### 6.8 Other routes — primary absence

**No formal pharmacokinetic study of subcutaneous, intranasal, sublingual, or transdermal BPC-157 has been published.** Topical BPC-157 has been studied in wound and burn models in rats with measurable effects on healing endpoints (Sikirić 2003 *Burns* 29:323–334 [13]; Cerovecki 2010 [23]), but no plasma concentration data exist for any topical or intranasal administration. The widely marketed "BPC-157 nasal spray" formulations have no published peer-reviewed PK characterization; biological-activity reports invoked for intranasal delivery are inferred from rat rhinitis-model wound studies, not from PK measurement. The Hudson Biotech Phase 2 hamstring trial NCT07437547 (started Feb 2, 2026) is the **first registered Phase 2 study of subcutaneous administration in humans**; this is documented in §7.

### 6.9 PK summary table

| Species | Route | Dose | Cmax | Tmax | t½ | F% | AUC₀–t | Source |
|---|---|---|---|---|---|---|---|---|
| Rat (SD) | IV | 20 µg/kg | (bolus) | — | **15.2 min** | reference 100% | 399 ng·min/mL | [48, animal] [pm: rat] |
| Rat (SD) | IM | 20 µg/kg | 12.3 ng/mL | 3 min | <30 min | **18.82%** | 75.1 ng·min/mL | [48] |
| Rat (SD) | IM | 100 µg/kg | 48.9 ng/mL | 3 min | <30 min | **14.49%** | 289 ng·min/mL | [48] |
| Rat (SD) | IM | 500 µg/kg | 141 ng/mL | 3 min | <30 min | **19.35%** | 1930 ng·min/mL | [48] |
| Rat (SD) | IM ×7 d | 100 µg/kg/d | similar to single | 3 min | <30 min | (not recalculated) | slight ↑ | [48] |
| Beagle dog | IV | 6 µg/kg | (bolus) | — | <30 min | reference | (Table 4) | [48] [pm: beagle] |
| Beagle dog | IM | 6, 30, 150 µg/kg | dose-linear; 30 µg/kg = 3.30 ± 0.51 ng/mL | within 9 min | <30 min | **45–51%** | linear with dose | [48] |
| Human (n=2) | IV infusion (1 h) | 10 mg day 1; 20 mg day 2 | **not measured** | — | **not measured** | — | **not measured** | [53, open_label] |
| Human (rectal) | PR | undisclosed | — | — | — | — | abstract-only | [42] `[corpus-unverifiable]` |
| Human (oral) | PO | — | — | — | — | — | **no primary** | absence finding |
| Human (SC) | SC | — | — | — | — | — | **no primary; NCT07437547 in progress** | absence finding |

### 6.10 Stability summary

| Condition | Result | Source |
|---|---|---|
| Human gastric juice, ~24 h, in vitro | "stable" / "not destroyed >24 h" — qualitative; no degradation-vs-time curve in peer-reviewed primary | [1, origin claim] propagated through Sikirić-group reviews (Gut Liver 2020, Front Pharmacol 2021, Biomedicines 2022) |
| Rat sponge exudate at wound site, several hours | locally active several hours (PD, not chemical stability) | [41, animal+in_vitro] [pm: rat / db-db mouse] |
| Acetate, simulated gastric juice pH 3.0, 5 h | 0.08% intact | [Diagen WO2014142764A1, vendor/patent — in-vitro only] |
| Arginate, simulated gastric juice pH 3.0, 5 h | 84.9% intact | [Diagen WO2014142764A1, vendor/patent — in-vitro only] |
| Acetate, water 50 °C, 388 h | 21.30% intact | [Diagen WO2014142764A1, vendor/patent] |
| Arginate, water 50 °C, 388 h | 99.01% intact | [Diagen WO2014142764A1, vendor/patent] |
| In-vivo metabolic fate (rat, IM) | rapidly proteolysed to small peptide fragments → free amino acids; urine + bile excretion | [48, animal] [pm: rat] |

### 6.11 Section provenance note

The PK story for BPC-157, distilled honestly: one cross-species animal PK paper (He L 2022 from Air Force Medical University Xi'an, rat + dog, IV + IM only); one n=2 human IV pilot with no plasma assay (Lee & Burgess 2025); one Pliva-era abstract-only human rectal PK (Veljaca 2003); one Pliva-era abstract-only Phase 2 RCT (Ruenzi 2005); a 24-h gastric-juice stability claim that traces to a paywalled 1993 hypothesis paper and has no published independent degradation-vs-time curve; an arginate-vs-acetate differential stability claim that lives entirely in the Diagen patent. The dose-route-extrapolation hazard is severe; the wiki entry preserves the species and route in every quoted number.

## 7. Human Evidence

The peer-reviewed primary human evidence base for BPC-157 is extraordinarily thin. Total subjects ever exposed under published, peer-reviewed primary study protocols is approximately **60** (cumulative, across all four published papers combined). All published US human efficacy and safety data trace to a single investigator (Edwin Lee, MD) at a single private clinic (Institute for Hormonal Balance, Orlando FL) and are published in a single lower-impact peer-reviewed journal (*Alternative Therapies in Health and Medicine*). This contradicts vendor and influencer claims of "extensive human evidence."

### 7.1 Veljaca 2003 — Phase 1 healthy-male volunteers, rectal route, abstract only

Marija Veljaca and colleagues at Pliva-Croatia / GalaPharma reported first-in-human safety, tolerability, and pharmacokinetics for PL 14736 (BPC-157 sodium salt, Pliva development designation) given rectally to healthy adult males. Presented at IUPHAR-GI Honolulu 2002; published as conference abstract Veljaca M, Pavic-Sladoljev D, Mildner B, Brajsa K, Bubenik M, Stipanicic S et al. 2003, *Gut* 51(Suppl III):A309 [42, open_label]. The abstract is the primary record; full-text PK numbers (Cmax, T½, AUC) are not retrievable in the indexed corpus and are marked `[corpus-unverifiable]`. The Gwyer 2019 secondary-review paraphrase reads: "rectal administration of PL 14736 to healthy male volunteers was safe and well tolerated." n was undisclosed in retrievable abstract metadata; Phase 1 dose-escalation conventions suggest a likely range of 10–30 subjects.

### 7.2 Ruenzi 2005 — Phase 2 UC RCT, enema route, abstract only

A multicenter randomised double-blind placebo-controlled Phase 2 trial of PL 14736 enema in mild-to-moderate ulcerative colitis was conducted by Pliva and presented at Digestive Disease Week by Ruenzi M et al. 2005 (*Gastroenterology* 128:A584; Sponsor: Pliva, Croatia, Ulcerative Colitis Study Group) [43, rct]. **The full results were never published as a peer-reviewed full paper despite frequent citation.** The trial appears in subsequent Sikirić-group reviews and in the Vuksic 2007 rat companion paper (*Surg Today* 37(9):768–777; PMID 17713731 — animal, not human), but no manuscript appears in *Gastroenterology*, *Gut*, *Lancet*, or other indexes. The reason for non-publication is not publicly documented. **Do NOT cite numerical outcomes from this presentation in downstream synthesis.** The per-arm AE table is not in the indexed corpus.

### 7.3 Lee & Padgett 2021 — intra-articular knee, retrospective chart review

Lee E & Padgett W 2021 (*Altern Ther Health Med* 27(4):8–13; PDF alternative-therapies.com/oa/pdf/35042.pdf) is a retrospective chart review of intra-articular BPC-157 for multiple types of knee pain at the Institute for Hormonal Balance, Orlando FL [51, open_label]. Design: 17 patients treated, 16 contacted by telephone for retrospective follow-up at 6–12 months; intra-articular knee injection of BPC-157 4 mg (2 cc of 2000 µg/mL); 4 of 16 patients also received thymosin-β4 co-administration; outcome was phone-survey patient-reported pain relief; no validated pain scale; no controls; no MRI follow-up; mixed indications (meniscus, MCL, ACL, popliteal bursitis); patients paid out-of-pocket; compounded BPC-157 source was Tailor Made Compounding (Nicholasville KY — the same compounding pharmacy that was federally prosecuted in 2018–2020, see §10). Outcomes: 11/12 (91.6%) BPC-only and 14/16 (87.5%) overall reported significant pain relief; 0 AEs reported.

McGuire 2025 (PMC12446177) characterizes the Lee 2021 AE detection methodology this way: "did not report any adverse effects, although the screening for adverse events was not discussed at length." The "no AEs" finding here is therefore not a prospective null safety signal — it is a retrospective absence of patient self-report under non-specified AE-elicitation procedures.

### 7.4 Lee, Walker, Ayadi 2024 — intravesical, interstitial cystitis pilot

Lee E, Walker C, Ayadi B 2024 (*Altern Ther Health Med* 30(10):12–17; PMID 39325560) is a pilot of intravesical BPC-157 in pentosan-polysulfate-refractory interstitial cystitis [52, open_label]. Same single clinic (Institute for Hormonal Balance, Orlando FL); n=12 women, ages 39–76 (mean 58.3); single intravesical injection of 10 mg BPC-157 at site of intense bladder inflammation; 6-week post-treatment assessment. Outcomes: **10/12 (83%) reported 100% symptom improvement, 2/12 (17%) reported 80% improvement; 0 AEs reported**; patients were screened for fevers, skin rash, nausea, vomiting, worsening urinary symptoms, and dyspareunia, with 0 of 12 experiencing any hematuria or acute cystitis. Outcome assessment was not specified as validated (Global Response Assessment is mentioned in secondary summaries). Single investigator, small n, no controls.

**Alternative-explanation surfacing (Phase 6 critique addition).** A response rate in which 10 of 12 patients (83%) report **100% symptom improvement** and the remaining 2 report 80% improvement, with **zero AEs**, after a **single** intravesical injection in a refractory population, is at the **upper tail of plausibility for any IC intervention** in the published literature. Defensible alternative explanations that the primary does not surface and the wiki must surface:
- **Vehicle / saline effect.** Intravesical instillation of normal saline alone has documented placebo / expectancy / mechanical-wash effects in interstitial cystitis. The Lee 2024 study has no saline or vehicle control arm. The reported effect could be in substantial part the intravesical-instillation effect rather than a BPC-157-specific effect.
- **Placebo + regression-to-the-mean.** Refractory IC patients enrolled in a single-clinic open-label study after PPS failure are at a clinical low point; spontaneous regression is documented in IC follow-up cohorts.
- **Selection effect.** Lee enrolled patients from his own clinic. Patients who self-select into a paid open-label peptide-clinic procedure after PPS failure are a non-representative subset of the IC population. Their reported "100% improvement" rate is not transportable to a general IC population.
- **Outcome assessment.** Outcome was patient-reported symptom improvement at 6 weeks against an unspecified or non-validated scale. Self-report at a single clinic where the treating investigator administered the procedure carries demand-characteristic and expectancy contributions that a validated Global Response Assessment + blinded assessor would control.

The Lee 2024 numbers should be carried as documented findings under the §2.7 author/clinic-bias and §2.8 publication-bias framings, NOT as evidence of "BPC-157 is a highly effective IC treatment." A 100%/80% improvement rate at n=12 open-label single-clinic with zero adverse events is, taken at face value, more anomalous than a positive finding — it is the kind of effect size that should trigger increased scrutiny rather than amplification.

### 7.5 Lee & Burgess 2025 — IV safety pilot, n=2

Lee E & Burgess K 2025 (*Altern Ther Health Med* 31(5):20–24; PDF alternative-therapies.com/oa/pdf/11513.pdf; per Phase 4.75 IC-10 / C4 resolution, **co-author initial K**) is an IV safety pilot in n=2 healthy adults [53, open_label]. One 68-year-old Caucasian female and one 58-year-old Asian male; both participants had received IV BPC-157 prior to study enrollment (i.e., not naive to the compound); IRB-approved IRCM-2024-402 by Institute of Regenerative and Cellular Medicine (Santa Monica); compounded BPC-157 from undisclosed 503A pharmacy at 2 mg/mL × 5 mL vials, lot #1839016, BUD 8/2/24. Doses: 10 mg in 250 mL saline over 1 h on day 1; 20 mg in 250 mL saline over 1 h on day 2. Day 3 follow-up. Monitoring panel: CMP, CBC, CPK isoenzymes, BNP, TSH, RBC magnesium, hs-CRP; symptom questionnaire; vital signs.

Verbatim from the paper: "Short-term intravenous infusion of up to 20 mg of BPC-157 in 2 healthy adults showed no measurable adverse effects on cardiac biomarkers, with no elevation in CPK, BNP, Cardio-CRP, blood pressure, or heart rate. No effect on the liver, blood glucose levels, thyroid, or RBC Magnesium was observed." 0 AEs reported. **Plasma BPC-157 concentrations were not measured. This is a safety dataset, not a pharmacokinetic dataset.** The Cambridge repository review's secondary-layer paraphrase that "plasma BPC-157 concentrations returned to baseline within 24 h" is not supported by the actual primary (see §6.6) — this is a fabrication caught in the S2-era review chain and corrected here.

### 7.6 Edwin Lee single-clinic concentration and commercial-clinical overlap

**100% of published US human efficacy/safety primary data for BPC-157 comes from one investigator (Edwin Lee, MD) at one private clinic (Institute for Hormonal Balance, Orlando, FL), in one peer-reviewed journal (*Alternative Therapies in Health and Medicine*).** Lee holds a UCF College of Medicine assistant-professor appointment; the practice operates as a private hormone-and-peptide clinic. Independent replication of any Lee finding = zero. Cumulative n exposed under Lee protocols ≈ **31** (17 in Lee 2021 + 12 in Lee 2024 + 2 in Lee 2025). This single-clinic concentration is the strongest concentration signal in the entire BPC-157 entry — it is a tighter cluster than even the Sikirić-Zagreb academic cluster, because the Sikirić cluster spans multiple Zagreb hospital departments and includes Korean and Croatian collaborators, while the Lee cluster is one investigator at one private clinic.

**Commercial-clinical population overlap (Phase 6 critique addition).** The Institute for Hormonal Balance is a private hormone-and-peptide clinic that administers BPC-157 commercially. The Lee 2021 retrospective knee chart review (n=17 treated, 16 contacted) and the Lee 2024 IC pilot (n=12) recruit from the same clinic that bills patients for the procedure. The clinical-research subjects and the commercial customers are **the same population**; the studies are not blinded recruitment from a general patient pool. Patients paid out-of-pocket for the Lee 2021 procedure. This is not unique to Lee — much off-label peptide-clinic research in the US has this structure — but it must be surfaced because it (a) makes the publication-bias overlay (§2.8) particularly load-bearing for the Lee corpus, (b) gives the treating investigator both clinical and financial incentive in a direction that aligns with positive findings, and (c) means the "no adverse events" finding across all three Lee primaries is collected by the same investigator who profits from the treatment.

**Connection to Tailor Made Compounding federal prosecution (Phase 6 critique addition).** Lee 2021 explicitly used **compounded BPC-157 from Tailor Made Compounding LLC (Nicholasville, Kentucky)** as the study drug source. The same Tailor Made Compounding was **federally prosecuted in 2018–2020** by the Department of Justice for distribution of unapproved new drugs including BPC-157, with a guilty plea and forfeiture of more than $1.7M under the Federal Food, Drug, and Cosmetic Act (FDCA) [see §10.1 for the DOJ prosecution chronology]. The two facts appear in adjacent sections of this report but their conjunction is load-bearing: the Lee 2021 study's BPC-157 supply came from a pharmacy whose distribution of BPC-157 was the underlying conduct that violated federal law. The 2021 publication does not retract on the basis of the 2018–2020 prosecution because the conduct under investigation was distribution, not study methodology — but the connection bears on how a downstream agent should weight the Lee 2021 evidence base.

### 7.7 Trial registry inventory (as of 2026-05-24)

| Trial ID | Sponsor | Status | Phase | Indication | n target | Route | Country | Results posted? |
|---|---|---|---|---|---|---|---|---|
| NCT02637284 | PharmaCotherapia d.o.o. (Croatia) | Active, not recruiting (last verified Oct 2015) | 1 | Healthy volunteers PK + safety | 42 | Oral (PCO-02 tablet) | Mexico (Hospital Ángeles Tijuana) | **No** |
| NCT07437547 | Hudson Biotech | Recruiting | 2 | Acute Grade II hamstring strain | 120 | SC | China (PKU Shenzhen Hospital) | No (started Feb 2, 2026) |
| EudraCT (any) | — | — | — | — | — | — | — | **Zero hits** |
| WHO ICTRP (beyond above NCTs) | — | — | — | — | — | — | — | **Zero additional hits** |

**Total registered prospective interventional trials of BPC-157 in humans, worldwide, with public records: 2. Total registered trials with posted primary results: 0.**

NCT02637284 ("Phase I, Pilot Study in Healthy Volunteers, to Assess the Safety and Pharmacokinetics of PCO-02, Which Active Ingredient is BPC-157"): randomized placebo-controlled quadruple-masked Phase 1; n=42 healthy volunteers 18–35 y; oral Bepecin tablet (1 mg BPC-157/tablet); Phase 1a single dose 1/3/6 tablets, Phase 1b 3 tablets TID × 14 days; primary outcome AE monitoring; secondary PK (Cmax, Tmax, T½, AUC); start October 2015; primary completion estimated February 2016; "Active, not recruiting" last verified October 2015. **No results posted as of May 2026; no associated publication retrieved.** Numerical PK results from this trial would be the first peer-reviewable oral human PK ever published for BPC-157 — and they have not appeared in ten years.

NCT07437547 ("A Randomized, Double-Blind, Placebo-Controlled Phase 2 Trial of Pentadecapeptide BPC 157 for Accelerated Repair of Acute Grade II Hamstring Strain Confirmed by MRI"): randomized 1:1 double-blind placebo-controlled parallel; n=120; intervention SC BPC-157 once daily × 14 days; primaries (a) time to unrestricted-sport return ≤8 weeks, (b) MRI injury-volume change at day 14; secondaries pain VAS, strength symmetry. Started February 2, 2026. Estimated completion February 17, 2028. This is the **first registered Phase 2 trial of subcutaneous BPC-157 in humans**, and it is sponsored by industry (Hudson Biotech) at one Chinese teaching hospital.

### 7.8 Absence findings (human evidence)

- **No Phase 3 RCT for any indication has been registered or published.**
- **No FDA IND has been publicly disclosed.**
- **No NDA, MA, or comparable marketing-authorization filing exists in any jurisdiction.**
- **No human cancer-incidence data exists.**
- **No human angiogenesis-marker data exists.**
- **No human reproduction or pregnancy data exists.**
- **No pediatric human data exists.**
- **No chronic (>14 day) human exposure data has been published.**
- **No SC safety data was published prior to the February 2026 start of NCT07437547.**
- **No oral PK results have been posted for NCT02637284** in over ten years since trial start.

These absences are load-bearing for §8 and §9. The risk-floor for BPC-157 must be filled from mechanism (§3) and animal evidence (§4–§5), not from human data, because human data are insufficient to derive evidence-based contraindications or monitoring biomarkers.

### 7.9 Independent academic reviews (2025–2026)

Three independent (non-Sikirić, non-Lee) academic reviews have published in 2025–2026 and converge on the same conclusion that human data are extraordinarily limited:

- **McGuire FP, Martinez R, Lenz A, Skinner L, Cushman DM (2025).** *Curr Rev Musculoskelet Med* 18(12):611–619; PMID 40789979; PMC12446177; DOI 10.1007/s12178-025-09990-7. Department of Physical Medicine & Rehabilitation, University of Utah. Per Phase 4.75 IC-10 / C3 resolution, **McGuire FP is the correct first author** (not "Bemis-Standoli" as the S2-era dispatch had mis-attributed). Verbatim: "Despite this promise, and growing interest in athletic and online communities, human data is exceedingly sparse… Until well-designed human trials are conducted and published, BPC-157 should not be recommended for clinical use in musculoskeletal medicine." Also: "All the published studies report positive or beneficial effects of BPC-157, suggesting a possible publication bias toward positive findings" [55, mechanism_review] (the load-bearing quote operationalized as the §2.8 publication-bias overlay).

- **Vasireddi N, Hahamyan H, Salata MJ, Karns M, Calcei JG, Voos JE, Apostolakos JM (2025).** *HSS Journal* (published online July 31, 2025); DOI 10.1177/15563316251355551; PMC12313605. Case Western Reserve / University Hospitals Cleveland Medical Center. Systematic review screened 544 BPC-157 articles 1993–2024; PRISMA inclusion produced 36 studies (**35 animal, 1 human clinical**); of the 36, **only 4 of 36 studies assessed safety** [57, mechanism_review]. The single included clinical study is one of the Lee Orlando papers. The "4 of 36 assessed safety" datum is load-bearing for §8 safety-base sizing and is surfaced explicitly in §8.1 (Phase 6 critique fix).

- **Yuan C, Demers A, Silva-Ortiz V, Hasoon JJ, Lee W, Dave K, Amirdelfan K, Burke HW, Christo PJ, Robinson CL (2026).** *Int J Mol Sci*; PMID 41898733. Beth Israel Deaconess / Harvard pain-medicine group. Verbatim: "human research remains limited to small pilot studies investigating musculoskeletal pain, interstitial cystitis, and intravenous administration, all suggesting potential therapeutic value without reported major adverse effects" [58, mechanism_review].

### 7.10 Common-but-not-verifiable claims (human evidence)

- "BPC-157 has demonstrated safety in human clinical trials." **Verification result:** the published primary human safety record is (a) one conference abstract from 2003 with no full paper, (b) ≈31 total human subjects across 3 single-investigator pilots, (c) one ClinicalTrials.gov record from 2015 with no posted results in over a decade, and (d) one actively-recruiting 2026 Phase 2 trial. Calling this "demonstrated safety" is not supported.

- "He L 2022 demonstrated human pharmacokinetics of BPC-157." **Verification result:** the He L 2022 paper is exclusively rats and beagle dogs. No human PK data is in that paper. This is the suspected fabrication-vector for the S2-era dispatch.

- "Phase 2 trial of BPC-157 for ulcerative colitis showed positive results." **Verification result:** A Phase 2 trial of PL 14736 enema reportedly occurred (Ruenzi 2005) but was never published as a full peer-reviewed paper. No outcome data is in the indexed primary literature.

- "BPC-157 has been used in humans for over 20 years with no reported adverse events." **Verification result:** off-label / self-administered / vendor use does not generate adverse-event reporting infrastructure. The "no AE" claim is selection-biased; there is no AE registry.

- "BPC-157 is approved by any major regulator anywhere." **Verification result:** False. No NDA, no MA, no IND completion, no EMA action, no approved indication in any jurisdiction. See §10.

- "Athletes have safely used BPC-157 subcutaneously at protocol doses." **Verification result:** no published human SC safety data prior to the Feb 2026 start of NCT07437547.

## 8. Adverse Effects and Safety

### 8.1 Human AE data — null at small n

The published human AE record is null across all four primary studies, but the cumulative n is small enough that low-frequency adverse events would not be detectable:

- **Veljaca 2003 (PL 14736 rectal, healthy males, n undisclosed)**: described as "safe and well tolerated" per the abstract paraphrase; quantitative AE rates not retrievable [42, open_label].
- **Ruenzi 2005 (PL 14736 enema, UC, Phase 2)**: per-arm AE table not in indexed corpus [43, rct] `[corpus-unverifiable: per-arm AE table]`.
- **Lee, Walker, Ayadi 2024 (intravesical, IC, n=12)**: paper text states "No one dropped out of the study, and no adverse events were reported… 0 of 12 participants experienced any hematuria or acute cystitis" [52, open_label].
- **Lee & Burgess 2025 (IV, n=2 healthy adults)**: paper text states "no measurable adverse effects on cardiac biomarkers, with no elevation in CPK, BNP, Cardio-CRP, blood pressure, or heart rate. No effect on the liver, blood glucose levels, thyroid, or RBC Magnesium was observed. No side effects were reported, and the infusion was well-tolerated" [53, open_label] — attributively quoted; reader should weight against the §2.7 commercial-clinical overlap and §2.8 publication-bias overlay.
- **Lee & Padgett 2021 (intra-articular, knee)**: McGuire 2025 characterizes this paper's AE detection as: "did not report any adverse effects, although the screening for adverse events was not discussed at length" [51, open_label] [55, mechanism_review].

**Cumulative human exposure documented in peer-reviewed sources is on the order of n<100 across all studies, all short-duration.** McGuire 2025 summarizes attributively: "the safety profile has been promising… No adverse effects were reported, but rigorous, large-scale trials are lacking" [55, mechanism_review] — note the verbatim "promising" descriptor is in McGuire's voice, not in the wiki's voice.

**Safety-base sizing (Phase 6 critique addition).** The Vasireddi 2025 systematic review (entry [57]) is the most authoritative external statement on the thinness of the BPC-157 safety evidence base: of 36 studies meeting PRISMA inclusion criteria across the entire 1993–2024 literature, **only 4 assessed safety**. This datum should be the framing line for the §8 safety section: not "the safety record is null" but "the safety record is mostly absent." Eleven percent of the indexed BPC-157 literature has any safety component at all, and the bulk of that 11% is animal toxicology, not human safety.

### 8.2 Animal toxicology — Xu 2020 GLP package

Xu C, Sun L, Ren F, Huang P, Tian Z, Cui J, Zhang W, Wang S, Zhang K, He L, Zhang W, Zhang C, Hao Q, Zhang Y, Li M, Li W (2020). "Preclinical safety evaluation of body protective compound-157, a potential drug for treating various wounds." *Regul Toxicol Pharmacol* 114:104665; DOI 10.1016/j.yrtph.2020.104665. **First-author institution: Fourth Military Medical University / Air Force Medical University, Xi'an, China** (per Phase 4.75 IC-10 / C1 resolution; this is the same Xi'an cluster as He L 2022). This is the first and only published GLP-grade preclinical safety evaluation for BPC-157 [49, animal] [population-mismatch: mouse / rat / rabbit / guinea pig / dog].

Species panel: mice (BALB/c and ICR), rats (Sprague-Dawley), rabbits, guinea pigs, dogs (beagle). Endpoints: single-dose toxicity, repeated-dose toxicity, local tolerance, anaphylaxis (guinea pig), genetic toxicity (Ames test, micronucleus, chromosome aberration), embryo-fetal teratogenicity (rabbit). Conclusion as quoted: "BPC157 was well tolerated and did not cause any serious toxicity in mice, rats, rabbits and dogs… no genetic or embryo-fetal toxicity." "LD1 (dose lethal to 1% of animals) could not be established because no animals died, even at the highest doses administered." Mild local irritation at high-dose injection sites was the only finding. A "high-dose decrease in canine creatinine was attributed to pharmacological activity rather than toxicity." Maximum doses tested span 6 µg/kg up to 20 mg/kg (approximately 1000× the proposed human equivalent of ≈200 µg/person/day per the He L 2022 dose framing).

**No chronic >6-week GLP toxicology package exists in the indexed corpus** `[corpus-unverifiable: chronic >6-wk GLP package]`. The Xu 2020 package is short-duration; long-term carcinogenicity, two-year rodent bioassay, and full developmental-and-reproductive-toxicology (DART) packages have not been published.

He L 2022 reported supplementary tolerability: paper text states "The administration of BPC157 was well tolerated by all rats, and no visual signs of toxicity were observed, consistent with our previous safety evaluation studies (Xu et al., 2020)" [48, animal] [population-mismatch: rat, beagle dog]. No sex difference in plasma exposure was observed.

### 8.3 Theoretical concerns

#### 8.3.1 Tumor / angiogenesis–cancer

BPC-157 promotes angiogenesis via VEGFR2 activation (Hsieh 2017 [44], Hsieh 2020 [45] — both Chang Gung) and up-regulates VEGF expression in vivo in tendon/quadriceps healing models (Sikirić-group 2009 *J Physiol Pharmacol* supplement immunohistochemical VEGF study — bibliography entry #22 `[corpus-unverifiable]`, no journal volume / pages / DOI / PMID retrievable; surfaced inline only to acknowledge the claim made in secondary reviews). It activates FAK–paxillin and EGR-1 pathways that overlap with cancer-cell motility and invasion biology. **The mechanistic concern is real**: agents that up-regulate angiogenic signaling warrant long-term safety evaluation in cancer-survivor populations [55, mechanism_review].

**Alternative-interpretation caveat (Phase 6 critique addition).** The Hsieh 2017 and 2020 angiogenesis findings come from HUVEC + rat-aorta + rat hind-limb-ischemia contexts — i.e., **wound-healing / vascular-repair contexts**. The extrapolation from "BPC-157 promotes wound-healing angiogenesis" to "BPC-157 carries tumor-relevant angiogenesis risk" is one of two defensible readings of the same data. The wound-healing-context reading interprets the VEGFR2 / Src–caveolin-1–eNOS activation as a tissue-repair response that may not transfer to tumor-microenvironment biology (where chronic dysregulated angiogenesis differs from acute wound angiogenesis). The §8 framing here preserves the tumor-relevance concern because mechanism-derived precaution is the appropriate default in the absence of human safety data, but the wound-healing interpretation should be held open as a credible alternative.

The Sikirić group has published primary in-vitro and animal-model work in the *opposite* direction (anti-tumor):

- Radeljak S, Seiwerth S, Sikirić P (2004). "BPC 157 inhibits cell growth and VEGF signalling via the MAPK kinase pathway in the human melanoma cell line." *Melanoma Res* 14:A14–A15; DOI 10.1097/00008390-200408000-00050 [40, in_vitro]. **Abstract-level publication, not a full paper.**
- Kang EA, Han YM, An JM, Park YJ, Sikirić P et al. (2018). "BPC157 as potential agent rescuing from cancer cachexia." *Curr Pharm Des* 24:1947–1956; DOI 10.2174/1381612824666180614082950 [33, animal] [population-mismatch: rodent cancer-cachexia models].
- Sikirić P et al. (2025). "BPC 157 Therapy: Targeting Angiogenesis and Nitric Oxide…" PMC12567428. A *Reply* to a critical review (Józwiak et al. 2025) [59, mechanism_review]. Verbatim: "BPC 157 … presents prominent anti-tumor potential, in vivo and in vitro… per Folkman's concept, it demonstrates anti-tumor effect in vivo and in vitro." Per the §2.7 disclosure, this is a defensive Sikirić Reply paper, not independent confirmation.

**All primary anti-tumor evidence is 100% Sikirić-cluster.** The honest summary: (a) the biologic concern is real (VEGF/VEGFR2 + FAK–paxillin + EGR-1 are documented in cancer biology); (b) the in-vitro and one-mouse-experiment "anti-tumor" evidence presented as counter-balance is overwhelmingly from a single research cluster and at abstract-level publication record; (c) no human safety data in any oncology-adjacent population exists. McGuire 2025 frames this precisely: "contrary to the tumor-promoting potential of many angiogenic agents, BPC-157 has been shown to inhibit uncontrolled cell proliferation, downregulate VEGF expression, and counteract VEGF-driven tumorigenesis [in Sikirić-group preclinical models]… [yet] pathologic angiogenesis is implicated in the proliferation of tumor cells" [55, mechanism_review]. The review preserves uncertainty rather than collapsing it. The wiki adopts the same posture.

#### 8.3.2 Cardiovascular

Lee 2025 measured CPK, BNP, Cardio-CRP, blood pressure, heart rate before/during/after up to 20 mg IV infusion; paper reports "no measurable adverse effects on the cardiac biomarkers" [53, open_label]. This is the only systematic cardiovascular monitoring in humans, n=2. Animal cardiovascular literature is cardio-protective in direction: Balenovic D et al. 2009 (methyldigoxin-arrhythmia model, *Regul Pept* 156:83–89) [21, animal]; Barisic I et al. 2022 (isoprenaline myocardial infarction, *Biomedicines* 10:265) [39, animal] [population-mismatch: rat]. The NO/eNOS modulation pathway carries a theoretical risk in patients with NO-dysregulation states (severe atherosclerosis, untreated hypotension) but no primary human data.

#### 8.3.3 Endocrine and CNS

Dopamine-system modulation in rat models (Sikirić 1999 MPTP [7]; Klicek 2013-2014 cuprizone [28]; Belosic Halle 2017 neuroleptics — bibliography entry #32, `[corpus-unverifiable]`, no journal volume / pages / DOI / PMID retrievable; surfaced inline only to acknowledge the claim made in secondary reviews) is protective/normalizing in direction in toxicant-induced models. **No published human data on prolactin, mood, motor function, or sexual function changes** [population-mismatch: rat]. The Chang 2014 GHR up-regulation in tendon fibroblasts at the injury site has been extrapolated by some practitioners to a theoretical concern about systemic IGF-1 axis activation in cancer-survivors; the extrapolation is mechanistic and not supported by direct measurement in humans [47, in_vitro] [population-mismatch: rat tendon fibroblast].

#### 8.3.4 Immune / autoimmune

Anti-inflammatory direction in adjuvant-arthritis rat model (Sikirić et al. 1997, *J Physiol Paris* 91:113–122) [6, animal] [population-mismatch: rat]. **No published BPC-157 trial in any autoimmune patient population.** Mechanistic direction does not predict aggravation, but immune trafficking effects in humans are uncharacterized.

### 8.4 Drug–drug interactions

- **NSAID interaction**: well-studied, protective direction (Sikirić 2012 [26]; Park 2020 [35] — both rat models) [population-mismatch: rat]. No documented harmful interaction.
- **Corticosteroid interaction**: BPC-157 counters corticosteroid-impaired healing in burn-injured mice without re-inducing characteristic corticosteroid AEs (Sikirić 2003 *Burns* 29:323–334 [13]; Pevec 2010 [24]) [population-mismatch: mouse, rat]. No published human interaction data.
- **Alcohol interaction**: Prkacin 2001 reversed alcohol-induced chronic liver lesions in rats [12, animal] [population-mismatch: rat]. Direction protective. No human data.
- **Cyclophosphamide / chemotherapy**: Luetic 2017 *Inflammopharmacology* 25:255–264 — counteraction of cyclophosphamide-induced GI lesions in rat [31, animal] [population-mismatch: rat]. Potentially clinically meaningful (chemo-related toxicity attenuation) but **also raises a concern about interference with chemotherapy efficacy** if a patient self-administers BPC-157 while receiving cytotoxic therapy. Not studied in oncology patients.
- **Anticoagulant interaction**: Stupnisek 2015 (PMID 25897838) is the direct rat-tail-amputation probe with heparin and warfarin (§4.9; entry [29]). The direction is reduced bleeding under anticoagulant in rat; **this is not a safety endorsement for human anticoagulant co-use** — it is a pharmacodynamic-interaction signal of unknown direction in human hemostasis. The §3.2 alt-explanation caveat applies: a "balancing" framing that opposes both pro-thrombotic and anti-thrombotic signals is structurally non-falsifiable. Theoretical concern about bleeding/clotting in patients on warfarin or direct oral anticoagulants is plausible but UNTESTED in humans [29, animal].

### 8.5 Mechanism-derived contraindications

The following contraindications are derived from mechanism + animal evidence; none is evidence-based in the strict sense because the human n is too small:

- **Pregnancy and lactation.** Xu 2020 reported "no embryo-fetal toxicity" in rabbits but the cited study is a teratogenicity screen, NOT a full DART package, and there are no human pregnancy data [49, animal] [population-mismatch: rabbit]. Practitioner mechanism-derived caution lists treat pregnancy as an "absolute contraindication" pending human reproductive data [55, mechanism_review]. The framing in this wiki: contraindicated by default until human DART package + human registry exist.

- **Active or recent malignancy / history of cancer.** Mechanism-driven cautionary recommendation in McGuire 2025 [55] and multiple practitioner reviews. **No primary data establishes either safe or unsafe use in this population.** "Absolute contraindication" is conservative but is risk-tier reasoning, not evidence-based.

- **Active autoimmune disease in flare.** Anti-inflammatory direction in animal models is consistent with mechanism. Treat as "no published safety record in this population" rather than as evidenced contraindication [55, mechanism_review].

- **Concurrent anticoagulant therapy.** No human drug-interaction study published; mechanism-based caution from the Stupnisek 2015 rat probe [29]. Stupnisek 2015 is suggestive of pharmacodynamic interaction with heparin and warfarin in rat.

- **Hepatic or renal impairment.** Plasma half-life is short and BPC-157 metabolizes to fragments entering normal amino acid pools (He L 2022, §6.1 [48]), suggesting low risk of accumulation; however, **human PK in impaired-organ populations is unstudied** [population-mismatch: rat, dog]. Treat with standard caution applied to any unapproved peptide.

- **Recent thrombotic event** (DVT, PE, stroke). Mechanism-derived from NO/eNOS modulation and the Stupnisek 2015 hemostasis signal [29]. Not directly tested in humans.

### 8.6 Synthesis of the human + animal safety record

Across the combined human (≈60 cumulative subjects, mostly short-term) and animal (Xu 2020 GLP short-duration multi-species [49]; He L 2022 supplementary rat/dog tolerability [48]; the entire Sikirić-group animal corpus across §4–§5) record, **no acute toxicity signal has been published**. The interpretive caveats:

- (a) human n is too small to detect low-frequency AEs;
- (b) no chronic >6-week GLP package exists `[corpus-unverifiable]`;
- (c) no human cancer-incidence, reproduction, or pediatric data exist;
- (d) per Vasireddi 2025 [57] only 4 of 36 BPC-157 studies meeting PRISMA inclusion 1993–2024 assessed safety at all;
- (e) the April 22, 2026 removal from FDA Category 2 was procedural (**nominations withdrawn**, not a safety clearance), with PCAC review scheduled July 23, 2026.

**FDA 2023 Category 2 safety reasoning — expanded (Phase 6 critique addition).** The FDA's September 2023 placement of BPC-157 in Category 2 of the interim 503A bulks list reflected an agency determination of significant safety risks for compounding. The specific safety reasoning surfaced in the FDA Bulks List Pharmacy Compounding Advisory documentation and in the subsequent Frier Levitt 2026 legal analysis includes:

1. **Impurity-profile concerns from compounded preparations.** Pyrogen / endotoxin contamination, residual-counterion (TFA, acetate) variability, and uncharacterized degradation-product profiles in 503A-compounded BPC-157 lots were noted as inadequately characterized.
2. **Insufficient human safety data.** The agency cited the n<100 cumulative human pilot exposure and the absence of any Phase 2 or Phase 3 trial with posted safety results. The Lee Orlando single-clinic record was characterized as inadequate substitute for trial-grade safety data.
3. **Route-of-administration claims without primary PK.** The widespread compounded BPC-157 supply was marketed for oral, subcutaneous, and intranasal routes none of which have published primary PK in any species (only IV/IM in rat+dog from He L 2022). The agency flagged the route-claim mismatch with the published evidence base.
4. **Chronic-exposure unknown.** No chronic (>6-week) toxicology and no human chronic-exposure data exists. The compounding context (off-label, repeated self-administration) implies chronic exposure that the published safety record does not support.

These four reasoning lines are not collapsed by the April 22, 2026 Category 2 removal. **The removal happened via nominations withdrawal — the nominators (the parties who originally requested 503A bulks list inclusion) withdrew their nominations.** No FDA finding addressed and cleared the 2023 safety concerns. The compound is now in a procedurally indeterminate state pending the July 23, 2026 PCAC review, but the agency's stated 2023 safety concerns remain formally unresolved. A downstream agent or specialist evaluating BPC-157 should treat the FDA's 2023 safety reasoning as **the most authoritative counter-perspective on the compound's safety profile** in the corpus, not as a mention-once-then-drop datum.

The published animal safety package is therefore consistent with "well tolerated short-duration in multi-species GLP toxicology" and the published human pilot record is consistent with "no acute signal at n<100 in short-duration mixed-route exposure." Neither is sufficient to derive evidence-based contraindications, monitoring biomarkers, or stopping criteria for chronic human use; §9 fills these slots from mechanism and standard Phase 1 practice.

## 9. Monitoring Biomarkers and Stopping Criteria

This section is scaffolding for the Phase 7.5 risk-floor gate. Because BPC-157 has no FDA-approved indication, no agency-issued monitoring protocol exists. The recommendations below derive from (a) what was measured in the published human pilots, (b) mechanism-driven concerns from §3, §4–§5, and §8, and (c) standard regulatory safety panels for early-phase peptide trials. They are mechanism-derived and practice-derived, **not evidence-based** in the strict sense.

### 9.1 Standard safety panel (rationale: general unapproved-peptide off-label practice)

| Biomarker | Rationale | Primary support |
|---|---|---|
| CBC with differential | Standard safety panel; immune-modulation context | Standard Phase 1 practice; not measured in published pilots `[corpus-unverifiable]` |
| CMP (Na/K/Cl/HCO₃, BUN, Cr, glucose, AST/ALT/ALP/bilirubin) | Hepatic + renal monitoring; rule out organ toxicity given short human exposure record | Lee 2025 IV pilot measured CMP, no change at n=2 [53, open_label] |

### 9.2 Cardiovascular (rationale: NO/eNOS modulation; the one human IV pilot measured these)

| Biomarker | Rationale | Primary support |
|---|---|---|
| CPK isoenzymes | Cardiac safety | Lee 2025 measured, no signal [53] |
| BNP | Cardiac volume / strain | Lee 2025 measured, no signal [53] |
| Cardio-CRP / hs-CRP | Inflammation; vascular stability | Lee 2025 measured, no signal [53] |
| Blood pressure + heart rate (orthostatic + supine) | NO-modulation, theoretical vasodilatory effect | Lee 2025 measured, no change [53] |
| Troponin (high-sensitivity) | Cardiac safety in patients with CV history | Not measured in any published human study; mechanism-derived |

### 9.3 Coagulation (rationale: Stupnisek 2015 rat anticoagulant-interaction signal)

| Biomarker | Rationale | Primary support |
|---|---|---|
| PT / INR | Mechanism-derived from rat heparin/warfarin probe (Stupnisek 2015) | [29, animal] [population-mismatch: rat]; gap in human |
| aPTT | Same mechanism | [29]; gap in human |
| Platelet count | Stupnisek 2015 reported counteraction of anticoagulant-induced thrombocytopenia in rat | [29, animal] [population-mismatch: rat]; gap in human |

**NOT measured in any published human pilot.** This is a gap, not a satisfied panel.

### 9.4 Hepatic (rationale: animal hepatic protection literature surfaces these as the readouts of interest)

| Biomarker | Rationale | Primary support |
|---|---|---|
| ALT, AST, ALP, bilirubin | Hepatic injury markers; paracetamol [25] and CCl₄ [2] animal models describe necrosis + fatty change | [25, 2, animal] [population-mismatch: rat]; Lee 2025 measured, no change at n=2 [53] |

### 9.5 Tumor surveillance (rationale: mechanism-derived precautionary; NOT evidence-based)

| Biomarker | Rationale | Primary support |
|---|---|---|
| Population-appropriate tumor markers (PSA, CA-125, CEA, AFP) | VEGFR2 + FAK–paxillin + EGR-1 angiogenesis up-regulation creates theoretical concern | [44, 45, 47, 40, 33, 55] mechanism + Sikirić-anchored anti-tumor evidence; NO HUMAN DATA |
| Age-appropriate cancer screening (mammography, colonoscopy, dermatologic surveillance) | Same precautionary rationale | Standard preventive medicine; mechanism-derived |
| Imaging surveillance for prior tumor sites in cancer-survivors who choose BPC-157 against medical advice | Same precautionary rationale | Standard-of-care oncology surveillance |

**The case for tumor-marker monitoring rests on UNCERTAINTY rather than positive evidence of harm.** Monitoring is precautionary, not derived from a measured human tumor-incidence signal (no such measurement exists).

### 9.6 Endocrine (rationale: dopaminergic modulation in animal models, Lee 2025 panel)

| Biomarker | Rationale | Primary support |
|---|---|---|
| Prolactin | Dopamine-system modulation literature in animals raises a theoretical (low-likelihood) concern | [7, 10, animal] [population-mismatch: rat]; NOT measured in human |
| TSH (and reflex T4) | Endocrine baseline | Lee 2025 measured TSH, no change at n=2 [53] |
| Fasting glucose, HbA1c | Endocrine baseline | Lee 2025 measured glucose, no change at n=2 [53] |
| RBC magnesium | Included in Lee 2025 panel as electrolyte safety | Lee 2025 measured, no change [53] |

### 9.7 Stopping criteria (library-canonical placeholder)

The published literature does NOT contain explicit stopping-criteria recommendations specific to BPC-157 (no FDA-approved label exists). The placeholders below are derived from (a) general unapproved-peptide / off-label clinical practice, (b) the mechanistic risks above, and (c) standard Phase 1 stopping rules. They are mechanism-and-practice derived.

1. **New diagnosis of malignancy or recurrence of prior cancer during use.** Stop immediately. Mechanism-derived (VEGFR2 + FAK–paxillin + EGR-1 up-regulation); no primary human evidence either way [55, mechanism_review].
2. **Pregnancy or planned conception.** Stop immediately; no human reproductive data.
3. **Unexplained AST/ALT >3× ULN, bilirubin >2× ULN, or creatinine increase >0.3 mg/dL above baseline.** Standard Phase 1 hepatic/renal stopping rule; not BPC-157-specific.
4. **Unexplained bleeding or clotting event** (DVT, PE, GI bleed, intracranial bleed). Mechanism-derived from NO/eNOS pathway and the Stupnisek 2015 rat hemostasis signal [29].
5. **New injection-site infection, abscess, or systemic infection.** General compounded-injectable safety rule (compounding sterility risk).
6. **Sport-tested athlete subject to WADA Code.** Do not start; if started in error, stop and seek anti-doping legal advice (no TUE basis; see §10, WADA Prohibited List and USADA TUE policy documents).
7. **Active autoimmune flare requiring escalation of immunosuppression.** Stop pending consultation; mechanism direction is anti-inflammatory but uncharacterized in this population [55, mechanism_review].
8. **Subjective deterioration** (new persistent pain, mass, lymphadenopathy, neurologic symptom) without alternative explanation.

These are NOT label-derived stopping criteria; they are mechanism-and-practice derived placeholders for the Phase 7.5 risk-floor gate.

## 10. Regulatory Status (as of May 2026)

### 10.1 FDA (United States)

**Current status (as of 2026-05-24, per Phase 4.75 IC-10 / C5 resolution — Section F is authoritative; Section D's pre-April-2026 framing is superseded):**

- **BPC-157 is NOT FDA-approved as a drug.** No NDA filed; no IND completed and publicly disclosed; no approved indication in any therapeutic class.
- **BPC-157 is NOT on the §503A bulks list** (the list of bulk drug substances that may be used in pharmacy compounding under §503A).
- **BPC-157 was placed in Category 2 of the FDA's interim 503A bulks list in 2023**, reflecting an FDA preliminary determination of significant safety risks for compounding. The agency's specific safety reasoning (impurity-profile, insufficient human safety, route-of-administration claims without primary PK, chronic-exposure unknown) is expanded in §8.6 (Phase 6 critique addition); the underlying FDA action prompted litigation alleging the agency bypassed notice-and-comment procedures (Frier Levitt 2026 legal analysis; regulatory secondary, not in numbered bibliography). The 2023 docket number is `[corpus-unverifiable]` in this retrieval.
- **On April 22, 2026, the FDA updated the 503A bulks list document (fda.gov/media/94155/download) to remove BPC-157 from Category 2** because the nominations were withdrawn by the nominators. Verbatim from the updated document: "'BPC-157' has been removed from category 2 because the nominations were withdrawn by the nominators. However, FDA has announced it intends to consult the PCAC on July 23, 2026, regarding the potential inclusion of BPC-157-related bulk drug substances (BPC-157 acetate and BPC-157 (free base)) on the 503A bulks list" (FDA 503A bulks list April 22, 2026; regulatory primary, prose-cited).
- **Federal Register Notice 2026-07361** (Docket FDA-2025-N-6895, published April 16, 2026) announces a Pharmacy Compounding Advisory Committee meeting **July 23–24, 2026** at FDA White Oak Campus, with public comment deadline July 22, 2026. On July 23, 2026 PCAC will discuss BPC-157 (free base) and BPC-157 acetate as bulk drug substances being considered for inclusion on the 503A Bulks List; "uses evaluated" by FDA = ulcerative colitis. URL: federalregister.gov/documents/2026/04/16/2026-07361 (regulatory primary, prose-cited).
- **Operational implication:** as of May 2026, compounding pharmacies legally cannot compound BPC-157 under §503A because it has no USP monograph, is not a component of an FDA-approved drug, and does not appear on the bulks list (criteria per 21 CFR 216.23). The April 22, 2026 removal from Category 2 is **procedural** (nominations withdrawn), not a safety clearance — see §8.6 for the unresolved 2023 safety reasoning. The substance is NOT on Category 1, NOT on Category 2, NOT on the 503A bulks list, NOT FDA-approved.
- **DOJ enforcement chronology**: in 2018–2020 the Department of Justice prosecuted **Tailor Made Compounding LLC (Nicholasville, Kentucky)** and its owner for distribution of unapproved new drugs **including BPC-157**; guilty plea, forfeiture of more than $1.7M (DOJ press releases, regulatory secondary, prose-cited). This establishes that selling BPC-157 for human use violates the FDCA in the absence of approved status or a compliant compounding pathway. **Direct connection to the Lee 2021 evidence base (Phase 6 critique addition):** Tailor Made Compounding was the source of the BPC-157 used in the Lee & Padgett 2021 intra-articular knee study (entry [51]); see §7.6 for the load-bearing implication that a federally-prosecuted compounding pharmacy supplied the study drug for one of three Lee Orlando primaries that constitute the entire published US human evidence base.
- **Pending corporate development**: HYTN Innovations Inc. (CSE:HYTN) announced April 23, 2026 a spin-out of a BPC-157 peptide drug development program structured "in accordance with Health Canada, the European Medicines Agency and the U.S. Food and Drug Administration principles" — pre-IND stage; not a regulatory status change (HYTN press release April 23, 2026, regulatory secondary, prose-cited).

### 10.2 TGA (Australia)

**BPC-157 is Schedule 4 (prescription-only) under the Australian Poisons Standard, with an additional Appendix D clause 5 entry, effective June 1, 2024.** Per the TGA's Notice of Interim Decisions to Amend the Poisons Standard (November 2023 ACMS/ACCS Joint Meeting #35): "I have made the decision to amend the Poisons Standard by creating a Schedule 4 entry for BPC-157 [and] a new Appendix D, clause 5 entry to prohibit possession without appropriate authorisation… The proposal was in response to 48 referrals for importation of BPC-157 received by the TGA since 1 July 2022. The proposal seeks to align the scheduling of BPC-157 with other performance- and image-enhancing substances. … Implementation date 1 June 2024" (TGA interim decision, regulatory primary, prose-cited). URL: tga.gov.au/sites/default/files/2024-04/public-notice-of-interim-decisions-acms-43-accs-37-joint-acms-accs-35.pdf.

**BPC-157 is NOT on the Australian Register of Therapeutic Goods (ARTG)** (Sport Integrity Australia confirmation accessed 2025-10-13; regulatory secondary, prose-cited). April 2026 TGA safety alert (ABC News April 14, 2026) listed BPC-157 among unregulated/illegal peptide products being intercepted at the Australian border, with monitoring increasing since 2022 (regulatory secondary, prose-cited).

### 10.3 WADA (sport)

**BPC-157 is on the WADA Prohibited List, S0 (Non-Approved Substances), Specified Substance, prohibited at all times — in- and out-of-competition.** Added effective January 1, 2022; entry maintained through the 2025 and 2026 Lists. The 2026 List (effective January 1, 2026) verbatim under S0: "This class covers many different substances including but not limited to BPC-157, 2,4-dinitrophenol (DNP), ryanodine receptor-1-calstabin complex stabilizers [e.g. S-107, S48168 (ARM210)] and troponin activators (e.g. reldesemtiv and tirasemtiv). PROHIBITED AT ALL TIMES (IN- AND OUT-OF-COMPETITION) All prohibited substances in this class are Specified Substances" (WADA Prohibited List 2026, regulatory primary, prose-cited). URL: wada-ama.org/sites/default/files/2025-09/2026list_en_final_clean_september_2025.pdf.

**USADA Therapeutic Use Exemption (TUE)**: per the USADA Athlete Advisory (Key Changes 2022 Prohibited List), "Since BPC-157 is not an approved therapeutic agent in any country, there is no basis for granting a TUE for this substance" (USADA Athlete Advisory, regulatory primary, prose-cited).

### 10.4 Health Canada

**BPC-157 is not authorized for sale by Health Canada.** April 14, 2025 Health Canada public advisory targeted Prime Research of Sherbrooke, Quebec for selling unauthorized injectable peptide drugs including BPC-157, warning consumers and recommending consultation with a healthcare professional if used (Health Canada April 14, 2025 advisory, regulatory primary, prose-cited). Verbatim: "Affected products: Unauthorized health products sold online by Prime Research of Sherbrooke, QC, including injectable peptide drugs." The HYTN 2026 spin-out announcement notes development plans aligned with Clinical Trial Application (CTA) and Special Access Program (SAP) pathways — confirming that no marketing authorization exists.

### 10.5 EMA

**BPC-157 is NOT authorized by EMA.** No centralised, national, or mutual-recognition marketing authorization exists in any EU member state. The European authorized-medicines database returns no result for BPC-157, PL 14736, PL-10, or PLD-116. No EMA pediatric investigation plan (PIP), orphan designation, or CHMP scientific advice document for BPC-157 is published. **The EU Clinical Trials Register (EudraCT) returns zero trials for "BPC-157" or "PL 14736" as of May 2026** (EudraCT, regulatory primary, prose-cited). WHO ICTRP aggregates from the same registry sources as ClinicalTrials.gov and EudraCT; its result set returns no records beyond the two NCTs already enumerated in §7.7 (WHO ICTRP, regulatory primary, prose-cited). Evidence: absence in indexed EMA databases; HYTN 2026 announcement implies an EMA pathway has not yet been opened.

### 10.6 DEA

**BPC-157 is NOT a scheduled controlled substance under the federal Controlled Substances Act.** It is an unapproved (investigational) drug rather than a scheduled substance; OPSS (Operation Supplement Safety) classifies it as "unapproved drug … not a dietary ingredient" (OPSS BPC-157 page, regulatory secondary, prose-cited). Absent CSA scheduling, federal enforcement against BPC-157 distribution proceeds under the FDCA (unapproved-new-drug provisions), as demonstrated in the Tailor Made Compounding 2020 prosecution. No DEA scheduling action against BPC-157 is documented in the indexed corpus as of May 2026 `[corpus-unverifiable positive scheduling]`.

### 10.7 DoD

**BPC-157 is on the DoD Prohibited Dietary Supplement Ingredients List under DoDI 6130.06** (per OPSS, regulatory secondary, prose-cited) — service members are prohibited from use.

### 10.8 Regulatory summary table

| Jurisdiction | Status | Last verified |
|---|---|---|
| FDA (US) | Not approved; removed from 503A interim Category 2 on April 22, 2026 (nominations withdrawn); PCAC review scheduled July 23, 2026; outcome pending; no legal §503A compounding pathway | 2026-04-22 / 2026-04-16 |
| EMA | No authorization in any EU member state; EudraCT zero hits | 2026-05-24 |
| TGA (AU) | Schedule 4 + Appendix D clause 5 prescription-only with possession prohibition without authorisation, effective June 1, 2024; not on ARTG | 2026-04-14 |
| Health Canada | Not authorized; April 14, 2025 public advisory (Prime Research) | 2025-04-14 |
| WADA | S0 Non-Approved Substances, Specified Substance, prohibited in- and out-of-competition; no TUE basis | 2026-01-01 |
| DEA | Not scheduled under CSA; enforcement via FDCA | 2026-05-24 |
| DoD | On Prohibited Dietary Supplement Ingredients List (DoDI 6130.06) | 2026-05-24 |

## 11. Open Questions and Pending Evidence

The following questions are unresolved as of the May 2026 corpus rebuild and should be re-checked at any future re-rotation:

- **Will NCT07437547 (Hudson Biotech Phase 2 SC hamstring trial, n=120, started Feb 2, 2026, est. completion Feb 2028) read out positive or null?** This will be the first registered Phase 2 readout for BPC-157, and the first SC route in humans with a registered protocol.
- **Will any of the Edwin Lee single-clinic findings be independently replicated** at a non-Lee institution under prospective controlled design? As of May 2026, the answer is no.
- **Will any commercial sponsor pursue an NDA pathway?** HYTN Innovations announced a pre-IND spin-out in April 2026 (not yet a regulatory status change).
- **Will the FDA PCAC July 23, 2026 review** result in re-inclusion on the 503A bulks list, re-placement in Category 2, or no action? The "uses evaluated" by FDA in the PCAC briefing is ulcerative colitis — the indication tied to the Pliva-era PL 14736 program — not the MSK indications that drive most off-label US use.
- **Will the Sikirić 1993 24-h gastric-juice stability figure be independently reconfirmed** with a published degradation-vs-time curve by a non-Zagreb, non-Pliva, non-Diagen laboratory? As of May 2026, no such reconfirmation exists.
- **Will any independent in-vivo replication of the Sikirić MSK animal findings** (Achilles, MCL, quadriceps, gastrocnemius, bone defect, anticoagulant interaction) be published by a non-Sikirić laboratory?
- **Will the He L 2022 PK data** be independently confirmed by a non-Xi'an Fourth Military Medical University laboratory? The "independent" PK signal is single-institution as of May 2026.
- **Will NCT02637284** (the 2015 PharmaCotherapia Mexico Phase 1 oral PK trial) ever post results? Ten years without a readout is itself a signal.
- **Will the Schlosser SH3-domain direct-binding hypothesis** reach peer-reviewed publication outside vendor-affiliated channels?
- **What is the human plasma half-life of BPC-157?** No published human PK measurement exists in any species.
- **What is the human oral bioavailability of BPC-157 acetate vs arginate?** No published primary in any species.

## 12. Bibliography

This bibliography lists the deduplicated primaries enumerated in `/tmp/aplus-research/bpc-157/aggregate-primaries.json`. Initial enumeration produced 54 entries; Phase 6 critique audit downgraded entries #22 (Sikirić-group 2009 *J Physiol Pharmacol* supplement) and #32 (Belosic Halle 2017 neuroleptics) to `[corpus-unverifiable]` and **removed them from the primary count**. The working denominator for cluster-share arithmetic is therefore **52**. Both downgraded entries remain numbered in this bibliography so that section-letter cite mapping is stable across the corrections, and both carry an explicit `[corpus-unverifiable; not counted toward 52 primary denominator]` flag.

Entries 55–59 (added Phase 6) are previously-excluded mechanism reviews that are cited inline in this report and require numbered bibliography entries for cite-resolution; they are **NOT counted toward the 52-primary denominator** and are explicitly tagged `mechanism_review`. The pre-Phase-6 list ended at entry 54 (Tohyama 2004).

Each entry: numbered; full citation; type tag in brackets; first-author institution; cluster annotation; PMID/DOI/PMC where retrievable; brief verification quote or `[corpus-unverifiable]` flag where the primary text was not directly retrieved during this dispatch.

### 12.1 Sikirić-Zagreb academic cluster (39 verifiable; Tohyama 2004 added below as #54 under uniform sub-cluster rule)

1. **Sikirić P, Petek M, Rucman R, Seiwerth S, Grabarevic Z, Rotkvic I, Turkovic B, Jagic V, Mildner B, Duvnjak M et al. (1993).** "A new gastric juice peptide, BPC. An overview of the stomach-stress-organoprotection hypothesis and beneficial effects of BPC." *Journal de Physiologie (Paris)* 87(5):313–327. DOI: 10.1016/0928-4257(93)90038-U; **PMID 8298609** (per Phase 4.75 IC-10 / C2 resolution). [animal, mechanism_review-originating-description]. **First-author institution:** University of Zagreb School of Medicine (Sikirić-Zagreb-academic cluster; Pliva-era). **Verification:** primary text paywalled; figure verified via Sikirić 2024 review PMC11053547 paraphrase: "BPC 157, native and stable in human gastric juice can be a cytoprotection mediator as it is not destroyed in human gastric juice for more than 24 h."

2. **Sikirić P, Seiwerth S, Grabarevic Z et al. (1993).** "Hepatoprotective effect of BPC 157, a 15-amino acid peptide, on liver lesions induced by either restraint stress or bile duct and hepatic artery ligation or CCl4 administration." *Life Sciences* 53(18):PL291–PL296. PMID 7901724. [animal]. **First-author institution:** University of Zagreb School of Medicine. Sikirić-Zagreb-academic cluster.

3. **Sikirić P, Seiwerth S, Grabarevic Z, Rucman R, Petek M, Jagic V et al. (1994).** "The beneficial effect of BPC 157, a 15 amino acid peptide BPC fragment, on gastric and duodenal lesions induced by restraint stress, cysteamine and 96% ethanol in rats." *Life Sciences* 54:PL63–PL68. DOI: 10.1016/0024-3205(94)00796-9. [animal]. **First-author institution:** University of Zagreb School of Medicine. Sikirić-Zagreb-academic cluster.

4. **Sikirić P, Seiwerth S, Grabarevic Z et al. (1996).** "Beneficial effect of a novel pentadecapeptide BPC 157 on gastric lesions induced by restraint stress, ethanol, indomethacin, and capsaicin neurotoxicity." *Digestive Diseases and Sciences* 41(8):1604–1614. PMID 8769287. [animal]. Sikirić-Zagreb-academic cluster.

5. **Sikirić P, Seiwerth S, Grabarevic Z et al. (1997).** "Pentadecapeptide BPC 157, cimetidine, ranitidine, bromocriptine, and atropine effect in cysteamine lesions in totally gastrectomized rats: a model for cytoprotective studies." *Digestive Diseases and Sciences* 42(5):1029–1037. PMID 9149058. [animal]. Sikirić-Zagreb-academic cluster.

6. **Sikirić P, Seiwerth S, Grabarevic Z et al. (1997).** "Pentadecapeptide BPC 157 positively affects both non-steroidal anti-inflammatory agent-induced gastrointestinal lesions and adjuvant arthritis in rats." *Journal de Physiologie (Paris)* 91:113–122. [animal]. Sikirić-Zagreb-academic cluster.

7. **Sikirić P, Marović A, Matoz W et al. (1999).** "A behavioural study of the effect of pentadecapeptide BPC 157 in Parkinson's disease models in mice and gastric lesions induced by 1-methyl-4-phenyl-1,2,3,6-tetrahydropyridine." *Journal de Physiologie (Paris)*. [animal]. Sikirić-Zagreb-academic cluster.

8. **Petrovic I, Dobric I, Drvis P et al. (1996).** "Salutary and prophylactic effect of pentadecapeptide BPC 157 on acute pancreatitis and concomitant gastroduodenal lesions in rats." *Digestive Diseases and Sciences*. PMID 8689934. [animal]. **First-author institution:** University of Zagreb School of Medicine. Sikirić-Zagreb-academic cluster.

9. **Sebecic B, Nikolic V, Sikirić P, Seiwerth S, Sosa T, Patrlj L, Grabarevic Z, Rucman R, Petek M, Konjevoda P, Jadrijevic S, Perovic D, Slaj M (1999).** "Osteogenic effect of a gastric pentadecapeptide, BPC-157, on the healing of segmental bone defect in rabbits: a comparison with bone marrow and autologous cortical bone implantation." *Bone* 24(3):195–202. PMID 10071911. DOI: 10.1016/S8756-3282(98)00180-X. [animal] [pm: rabbit]. **First-author institution:** Clinical Hospital Merkur, Zagreb, Department of Surgery + Zagreb co-affiliations. Sikirić-Zagreb-academic cluster.

10. **Jelovac N, Sikirić P, Rucman R, Petek M, Perovic D, Konjevoda P, Marović A, Seiwerth S, Grabarevic Z, Sumajstorcic J et al. (1998).** "A novel pentadecapeptide, BPC 157, blocks the stereotypy produced acutely by amphetamine and the development of haloperidol-induced supersensitivity to amphetamine." *Biological Psychiatry* 43(7):511–519. PMID 9547930. DOI: 10.1016/s0006-3223(97)00277-1. [animal]. Sikirić-Zagreb-academic cluster.

11. **Sikirić P, Separović J, Anić T et al. (2000).** "The antidepressant effect of an antiulcer pentadecapeptide BPC 157 in Porsolt's test and chronic unpredictable stress in rats. A comparison with antidepressants." *Journal de Physiologie (Paris)*. [animal]. Sikirić-Zagreb-academic cluster.

12. **Prkacin I, Separović J, Aralica G, Perovic D, Gjurasin M, Lovric-Bencic M et al. (2001).** "Portal hypertension and liver lesions in chronically alcohol drinking rats prevented and reversed by stable gastric pentadecapeptide BPC 157 (PL-10, PLD-116), and propranolol, but not ranitidine." *Journal de Physiologie (Paris)* 95(1–6):315–324. [animal]. Sikirić-Zagreb-academic cluster.

13. **Sikirić P et al. (2003).** "Corticosteroid-impairment of healing and gastric pentadecapeptide BPC-157 creams in burned mice." *Burns* 29:323–334. [animal]. Sikirić-Zagreb-academic cluster.

14. **Staresinic M, Sebecic B, Patrlj L, Jadrijevic S, Suknaic S, Perovic D, Aralica G, Zarkovic N, Borovic S, Srdjak M, Hajdarevic K, Kopljar M, Batelja L, Boban-Blagaic A, Turcic I, Anic T, Seiwerth S, Sikirić P (2003).** "Gastric pentadecapeptide BPC 157 accelerates healing of transected rat Achilles tendon and in vitro stimulates tendocytes growth." *Journal of Orthopaedic Research* 21(6):976–983. PMID 14554208. DOI: 10.1016/S0736-0266(03)00110-4. [animal + in_vitro]. Sikirić-Zagreb-academic cluster.

15. **Boban Blagaic A, Blagaic V, Mirt M et al. (2005).** "Gastric pentadecapeptide BPC 157 effective against serotonin syndrome in rats." *European Journal of Pharmacology*. PMID 15840402. [animal]. Sikirić-Zagreb-academic cluster.

16. **Krivic A, Anic T, Seiwerth S, Huljev D, Sikirić P (2006).** "Achilles detachment in rat and stable gastric pentadecapeptide BPC 157: promoted tendon-to-bone healing and opposed corticosteroid aggravation." *Journal of Orthopaedic Research* 24(5):982–989. PMID 16583442. DOI: 10.1002/jor.20096. [animal]. Sikirić-Zagreb-academic cluster.

17. **Staresinic M, Petrovic I, Novinscak T, Jukic I, Pevec D, Suknaic S, Kokic N, Batelja L, Brcic L, Boban-Blagaic A, Zoric Z, Ivanovic D, Ajduk M, Sebecic B, Patrlj L, Sosa T, Buljat G, Anic T, Seiwerth S, Sikirić P (2006).** "Effective therapy of transected quadriceps muscle in rat: gastric pentadecapeptide BPC 157." *Journal of Orthopaedic Research* 24(5):1109–1117. PMID 16609979. DOI: 10.1002/jor.20089. [animal]. Sikirić-Zagreb-academic cluster.

18. **Vuksic T, Zoricic I, Brcic L et al. (2007).** "Stable gastric pentadecapeptide BPC 157 in trials for inflammatory bowel disease (PL-10, PLD-116, PL14736, Pliva, Croatia) heals ileoileal anastomosis in the rat." *Surgery Today* 37(9):768–777. PMID 17713731. [animal]. **First-author institution:** University of Zagreb School of Medicine. Sikirić-Zagreb-academic cluster.

19. **Krivic A, Majerovic M, Jelic I, Seiwerth S, Sikirić P (2008).** "Modulation of early functional recovery of Achilles tendon to bone unit after transection by BPC 157 and methylprednisolone." *Inflammation Research* 57(5):205–210. PMID 18594781. DOI: 10.1007/s00011-007-7056-8. [animal]. Sikirić-Zagreb-academic cluster.

20. **Novinscak T, Brcic L, Staresinic M, Jukic I, Radic B, Pevec D, Mise S, Tomasovic S, Brcic I, Banic T, Jakir A, Buljat G, Anic T, Zoricic I, Romic Z, Seiwerth S, Sikirić P (2008).** "Gastric pentadecapeptide BPC 157 as an effective therapy for muscle crush injury in the rat." *Surgery Today* 38(8):716–725. PMID 18668315. DOI: 10.1007/s00595-007-3706-2. [animal]. Sikirić-Zagreb-academic cluster.

21. **Balenovic D et al. (2009).** "Inhibition of methyldigoxin-induced arrhythmias by pentadecapeptide BPC 157: a relation with NO-system." *Regulatory Peptides* 156:83–89. [animal]. Sikirić-Zagreb-academic cluster.

22. **Sikirić group (2009).** *Journal of Physiology and Pharmacology* supplement, immunohistochemical VEGF study. [animal]. Sikirić-Zagreb-academic cluster. **`[corpus-unverifiable; not counted toward 52 primary denominator]`** — no first-author surname, no journal volume, no page range, no DOI/PMID retrievable. Surfaced inline in §8.3.1 only to acknowledge the claim made in secondary reviews; cannot be used to ground any numerical or species-bound claim.

23. **Cerovecki T, Bojanic I, Brcic L, Radic B, Vukoja I, Seiwerth S, Sikirić P (2010).** "Pentadecapeptide BPC 157 (PL 14736) improves ligament healing in the rat." *Journal of Orthopaedic Research* 28(9):1155–1161. PMID 20225319. DOI: 10.1002/jor.21107. [animal]. **First-author institution:** University Hospital of Traumatology, Zagreb. Sikirić-Zagreb-academic cluster.

24. **Pevec D, Novinscak T, Brcic L, Sipos K, Jukic I, Staresinic M, Mise S, Brcic I, Kolenc D, Klicek R, Banic T, Sever M, Kocijan A, Berkopic L, Radic B, Buljat G, Anic T, Zoricic I, Bojanic I, Seiwerth S, Sikirić P (2010).** "Impact of pentadecapeptide BPC 157 on muscle healing impaired by systemic corticosteroid application." *Medical Science Monitor* 16(3):BR81–88. PMID 20190686. [animal]. Sikirić-Zagreb-academic cluster.

25. **Ilic S, Drmic D, Zarkovic K et al. (2010).** "High hepatotoxic dose of paracetamol produces generalized convulsions and brain damage in rats. A counteraction with the stable gastric pentadecapeptide BPC 157." *Journal of Physiology and Pharmacology*. [animal]. Sikirić-Zagreb-academic cluster.

26. **Sikirić P et al. (2012).** "Toxicity by NSAIDs. Counteraction by Stable Gastric Pentadecapeptide BPC 157." *Current Pharmaceutical Design* 19(1):76–83. [animal]. Sikirić-Zagreb-academic cluster.

27. **Cesarec V, Becejac T, Misic M et al. (2013).** "Pentadecapeptide BPC 157 and the esophagocutaneous fistula healing therapy." *European Journal of Pharmacology* 701(1–3):203–212. [animal]. Sikirić-Zagreb-academic cluster.

28. **Klicek R, Sever M, Radic B et al. (2013–2014).** "Stable gastric pentadecapeptide BPC 157 heals cysteamine-colitis and colon-colon-anastomosis and counteracts cuprizone brain injuries and motor disability." *European Journal of Pharmacology*. PMID 24304574. [animal]. **Author order per Phase 4.75 IC-10 / C7 resolution: Klicek R, Sever M.** Sikirić-Zagreb-academic cluster.

29. **Stupnisek M, Kokot A, Drmic D, Hrelec Patrlj M, Zenko Sever A, Kolenc D, Radic B, Suran J, Bojic D, Vcev A, Seiwerth S, Sikirić P (2015).** "Pentadecapeptide BPC 157 reduces bleeding and thrombocytopenia after amputation in rats treated with heparin, warfarin, L-NAME and L-arginine." *PLoS One* 10(4):e0123454. PMID 25897838. DOI: 10.1371/journal.pone.0123454. [animal]. **First-author institution:** J.J. Strossmayer University of Osijek; Sikirić senior at Zagreb. Sikirić-Zagreb cluster per sub-cluster rule.

30. **Grgic T, Sever M, Klicek R et al. (2016).** "Stable gastric pentadecapeptide BPC 157 heals rat colovesical fistula." *European Journal of Pharmacology* 780:1–7. PMID 26875638. [animal]. Sikirić-Zagreb-academic cluster.

31. **Luetic K, Sucic M, Vlainic J et al. (2017).** "Cyclophosphamide induced stomach and duodenal lesions as a NO-system disturbance in rats: L-NAME, L-arginine, stable gastric pentadecapeptide BPC 157." *Inflammopharmacology* 25(2):255–264. [animal]. Sikirić-Zagreb-academic cluster.

32. **Belosic Halle Z et al. (2017).** Neuroleptics + BPC-157 study. [animal]. Sikirić-Zagreb-academic cluster. **`[corpus-unverifiable; not counted toward 52 primary denominator]`** — no journal, no volume, no pages, no DOI/PMID retrievable. Surfaced inline in §8.3.3 only to acknowledge the claim made in secondary reviews; cannot be used to ground any numerical or species-bound claim.

33. **Kang EA, Han YM, An JM, Park YJ, Sikirić P, Kim DH, Kwon KA, Kim YJ, Yang D, Tchah H et al. (2018).** "BPC157 as potential agent rescuing from cancer cachexia." *Current Pharmaceutical Design* 24:1947–1956. DOI: 10.2174/1381612824666180614082950. [animal] [pm: rodent cancer-cachexia models]. **First-author institution:** Korean collaborator with Sikirić senior in author list; Sikirić-Zagreb cluster per sub-cluster rule.

34. **Vukojević J, Siroglavić M, Kasnik K et al. (2020).** "The effect of pentadecapeptide BPC 157 on hippocampal ischemia/reperfusion injuries in rats." *Brain and Behavior*. PMC7428500. [animal]. Sikirić-Zagreb-academic cluster.

35. **Park JM, Lee HJ, Sikirić P, Hahm KB (2020).** "BPC 157 rescued NSAID-cytotoxicity via stabilizing intestinal permeability and enhancing cytoprotection." *Current Pharmaceutical Design* 26(25):2971–2981. [animal]. Korean first author with Sikirić senior; Sikirić-Zagreb cluster per sub-cluster rule.

36. **Strbe S, Gojkovic S, Krezic I et al. (2021).** "Stable Gastric Pentadecapeptide BPC 157 Therapy for Primary Abdominal Compartment Syndrome in Rats." *Frontiers in Pharmacology*. PMID 34966273. PMC8710746. [animal]. Sikirić-Zagreb-academic cluster.

37. **Gojkovic S, Krezic I, Vranes H, Drmic D, Sikirić Suncana et al. (2021).** "Robert's Intragastric Alcohol-Induced Gastric Lesion Model as an Escalated General Peripheral and Central Syndrome, Counteracted by the Stable Gastric Pentadecapeptide BPC 157." *Biomedicines*. PMC8533388. [animal]. Sikirić-Zagreb-academic cluster.

38. **Gojkovic S, Krezic I, Vrdoljak B et al. (2021).** "BPC 157 Therapy and the Permanent Occlusion of the Superior Sagittal Sinus in Rat." *Pharmaceuticals / Biomedicines*. [animal]. Sikirić-Zagreb-academic cluster.

39. **Barisic I et al. (2022).** "Stable gastric pentadecapeptide BPC 157 may counteract myocardial infarction induced by isoprenaline in rats." *Biomedicines* 10:265. [animal]. Sikirić-Zagreb-academic cluster.

40. **Radeljak S, Seiwerth S, Sikirić P (2004).** "BPC 157 inhibits cell growth and VEGF signalling via the MAPK kinase pathway in the human melanoma cell line." *Melanoma Research* 14:A14–A15. DOI: 10.1097/00008390-200408000-00050. [in_vitro]. **Abstract-level publication.** Sikirić-Zagreb-academic cluster.

### 12.2 Pliva-Zagreb industrial cluster (3)

41. **Tkalčević V-I, Čužić S, Brajša K, Mildner B, Bokulić A, Šitum K, Perović D, Glojnarić I, Parnham MJ (2007).** "Enhancement by PL 14736 of granulation and collagen organization in healing wounds and the potential role of egr-1 expression." *European Journal of Pharmacology* 570(1–3):212–221. PMID 17628536. DOI: 10.1016/j.ejphar.2007.05.072. [animal + in_vitro]. **First-author institution:** PLIVA Research Institute Ltd, Prilaz baruna Filipovića 29, HR-10000 Zagreb, Croatia. Pliva-Zagreb industrial cluster.

42. **Veljaca M, Pavic-Sladoljev D, Mildner B, Brajsa K, Krnic Z, Bubenik M, Stipanicic S, Tabak-Slosic M, Brnic L, Khan Z, Krznaric Z, Bischoff A, Scroeder A, van Dongen W, van Schaik F (2003).** "Safety, tolerability and pharmacokinetics of PL 14736, a novel agent for treatment of ulcerative colitis, in healthy male volunteers." *Gut* 51(Suppl III):A309 [conference abstract]. [open_label]. **First-author institution:** Pliva Research Institute, Zagreb, Croatia / GalaPharma. Pliva-Zagreb industrial cluster. `[corpus-unverifiable for numerical PK]`.

43. **Ruenzi M, Stolte M, Veljaca M, Oreskovic K, Peterson J, Ulcerative Colitis Study Group (2005).** "A multicenter, randomized, double blind, placebo-controlled phase II study of PL 14736 enema in the treatment of mild-to-moderate ulcerative colitis." *Gastroenterology* 128:A584 [conference abstract]. [rct]. **Sponsor:** Pliva, Croatia. Pliva-Zagreb industrial cluster. **Never published as a full peer-reviewed paper.**

### 12.3 Independent — Chang Gung University, Taiwan, Pang group (4)

44. **Hsieh M-J, Liu H-T, Wang C-N, Huang H-Y, Lin Y, Ko Y-S, Wang J-S, Chang VHS, Pang JHS (2017).** "Therapeutic potential of pro-angiogenic BPC157 is associated with VEGFR2 activation and up-regulation." *Journal of Molecular Medicine (Berl)* 95(3):323–333. PMID 27847966. DOI: 10.1007/s00109-016-1488-y. [animal + in_vitro]. **First-author institution:** Chang Gung Memorial Hospital / Chang Gung University, Tao-Yuan, Taiwan. Independent (Pang group).

45. **Hsieh M-J, Lee C-H, Chueh H-Y, Chang G-J, Pang JHS, Peng Y-J et al. (2020).** "Modulatory effects of BPC 157 on vasomotor tone and the activation of Src-Caveolin-1-endothelial nitric oxide synthase pathway." *Scientific Reports* 10:17078. PMID 33051527. DOI: 10.1038/s41598-020-74022-y. [in_vitro + animal]. Independent (Chang Gung, Taiwan).

46. **Chang C-H, Tsai W-C, Lin M-S, Hsu Y-H, Pang JHS (2011).** "The promoting effect of pentadecapeptide BPC 157 on tendon healing involves tendon outgrowth, cell survival, and cell migration." *Journal of Applied Physiology* 110(3):774–780. PMID 21030672. DOI: 10.1152/japplphysiol.00945.2010. [in_vitro]. Independent (Chang Gung, Taiwan).

47. **Chang C-H, Tsai W-C, Hsu Y-H, Pang JHS (2014).** "Pentadecapeptide BPC 157 Enhances the Growth Hormone Receptor Expression in Tendon Fibroblasts." *Molecules* 19(11):19066–19077. PMID 25415472. PMC6271067. DOI: 10.3390/molecules191119066. [in_vitro]. Independent (Chang Gung, Taiwan).

### 12.4 Independent — Fourth Military Medical University / Air Force Medical University Xi'an (3, per IC-10 / C6)

48. **He L, Feng D, Guo H, Zhou Y, Li Z, Zhang K, Zhang W, Wang S, Wang Z, Hao Q, Zhang C, Gao Y, Gu J, Zhang Y, Li W, Li M (2022).** "Pharmacokinetics, distribution, metabolism, and excretion of body-protective compound 157, a potential drug for treating various wounds, in rats and dogs." *Frontiers in Pharmacology* 13:1026182. DOI: 10.3389/fphar.2022.1026182. PMID 36588717. PMC9794587. [animal]. **First-author institution:** State Key Laboratory of Cancer Biology, Department of Biopharmaceutics, School of Pharmacy, Air Force Medical University, Xi'an, China. Independent — Xi'an Fourth Military Medical University / AFMU cluster.

49. **Xu C, Sun L, Ren F, Huang P, Tian Z, Cui J, Zhang W, Wang S, Zhang K, He L, Zhang W, Zhang C, Hao Q, Zhang Y, Li M, Li W (2020).** "Preclinical safety evaluation of body protective compound-157, a potential drug for treating various wounds." *Regulatory Toxicology and Pharmacology* 114:104665. DOI: 10.1016/j.yrtph.2020.104665. [animal]. **First-author institution:** Fourth Military Medical University / Air Force Medical University, Xi'an, China (per Phase 4.75 IC-10 / C1 resolution — Section E was authoritative). Independent — same Xi'an cluster as He L 2022.

50. **Xue X-C, Wu Y-J, Gao M-T et al. (2004).** "Protective effects of pentadecapeptide BPC 157 on gastric ulcer in rats." *World Journal of Gastroenterology* 10(7):1032–1036. PMC4717094. [animal] [pm: rat]. **First-author institution:** Fourth Military Medical University, Xi'an, China (per Phase 4.75 IC-10 / C6 reclassification from Second Military Medical University Shanghai). Independent — same Xi'an cluster as He L 2022 and Xu 2020.

### 12.5 Independent — Edwin Lee Orlando (3)

51. **Lee E, Padgett W (2021).** "Intra-Articular Injection of BPC 157 for Multiple Types of Knee Pain." *Alternative Therapies in Health and Medicine* 27(4):8–13. URL: alternative-therapies.com/oa/pdf/35042.pdf. [open_label]. **First-author institution:** Institute for Hormonal Balance, Orlando FL + UCF College of Medicine. Independent (Lee Orlando cluster). Retrospective chart review n=17 treated, 16 contacted.

52. **Lee E, Walker C, Ayadi B (2024).** "Effect of BPC-157 on Symptoms in Patients with Interstitial Cystitis: A Pilot Study." *Alternative Therapies in Health and Medicine* 30(10):12–17. PMID 39325560. [open_label]. **First-author institution:** Institute for Hormonal Balance, Orlando FL. Independent (Lee Orlando cluster). Pilot n=12.

53. **Lee E, Burgess K (2025).** "Safety of Intravenous Infusion of BPC157 in Humans: A Pilot Study." *Alternative Therapies in Health and Medicine* 31(5):20–24. URL: alternative-therapies.com/oa/pdf/11513.pdf. [open_label]. **First-author institution:** Institute for Hormonal Balance, Orlando FL; UCF College of Medicine. Independent (Lee Orlando cluster). Pilot n=2; **co-author initial K per Phase 4.75 IC-10 / C4 resolution**.

### 12.6 Tohyama 2004 (reclassified to Sikirić-Zagreb cluster via sub-cluster rule — Phase 6 critique fix)

54. **Tohyama Y, Sikirić P, Diksic M (2004).** "Effects of pentadecapeptide BPC157 on regional serotonin synthesis in the rat brain: α-methyl-L-tryptophan autoradiographic measurements." *Life Sciences* 76(3):345–357. DOI: 10.1016/j.lfs.2004.08.010. [animal]. **First-author institution:** McGill University / Montreal Neurological Institute (Diksic group); Sikirić co-author. **Cluster classification (Phase 6 critique resolution):** Sikirić-Zagreb cluster via the sub-cluster rule. The pre-refinement draft's parallel rule — §2 counted Tohyama as independent (Diksic senior at McGill); §5 counted Tohyama to Sikirić via co-authorship — produced contradictory cluster arithmetic for the same paper. The unified rule (Sikirić co-authorship triggers Sikirić-cluster attribution everywhere) is now applied consistently across §2.2, §2.3, §3.5, §5.7, §5.9, §12.1 (the cluster heading) and this entry. Counted toward the 52-primary denominator; counted in the Sikirić-cluster numerator (39/52 = 75.0%, combined Zagreb 42/52 = 80.8%).

### 12.7 Numbered mechanism review entries (added Phase 6 for inline-cite resolution; NOT counted toward 52-primary denominator)

These entries are cited inline throughout the report and required numbered bibliography entries so that downstream agents can mechanically resolve every inline cite. They are mechanism reviews / independent academic syntheses, not primary experimental studies. None is counted toward the 52-primary aggregate; all are tagged `mechanism_review`.

55. **McGuire FP, Martinez R, Lenz A, Skinner L, Cushman DM (2025).** "Body Protective Compound-157: A Narrative Review of an Emerging Therapeutic Peptide in Musculoskeletal Medicine." *Current Reviews in Musculoskeletal Medicine* 18(12):611–619. PMID 40789979. PMC12446177. DOI: 10.1007/s12178-025-09990-7. [mechanism_review]. **First-author institution:** Department of Physical Medicine & Rehabilitation, University of Utah. Independent narrative review concluding "BPC-157 should be considered investigational." Source of the publication-bias quote operationalised as the §2.8 overlay.

56. **Gwyer D, Wragg NM, Wilson SL (2019).** "Gastric pentadecapeptide body protection compound BPC 157 and its role in accelerating musculoskeletal soft tissue healing." *Cell and Tissue Research* 377(2):153–159. PMID 30915550. DOI: 10.1007/s00441-019-03016-8. [mechanism_review]. **First-author institution:** School of Sport, Exercise and Health Sciences, Loughborough University, UK. Independent UK academic narrative review; concludes the precise healing mechanism remains undefined.

57. **Vasireddi N, Hahamyan H, Salata MJ, Karns M, Calcei JG, Voos JE, Apostolakos JM (2025).** "Investigating BPC 157: A Systematic Review of Current Clinical Applications and a Call for Rigorous Research." *HSS Journal* (online July 31, 2025). DOI: 10.1177/15563316251355551. PMC12313605. [mechanism_review / systematic review]. **First-author institution:** Hospital for Special Surgery / Case Western Reserve / University Hospitals Cleveland Medical Center. PRISMA systematic review screened 544 articles 1993–2024; final inclusion 36 (35 animal, 1 human clinical). **Only 4 of 36 included studies assessed safety** — the load-bearing thinness-of-safety-base datum.

58. **Yuan C, Demers A, Silva-Ortiz V, Hasoon JJ, Lee W, Dave K, Amirdelfan K, Burke HW, Christo PJ, Robinson CL (2026).** "Body Protection Compound 157: A Narrative Review of an Emerging Peptide in Pain Medicine." *International Journal of Molecular Sciences*. PMID 41898733. [mechanism_review]. **First-author institution:** Beth Israel Deaconess Medical Center / Harvard Medical School (pain medicine group). Independent narrative review.

59. **Sikirić P et al. (2025).** "BPC 157 Therapy: Targeting Angiogenesis and Nitric Oxide Pathways for Tissue Repair, Cytoprotection and Vascular Health." PMC12567428. [mechanism_review]. Sikirić-group **Reply paper** responding to the Józwiak M et al. 2025 critical review (*Pharmaceuticals (Basel)* 18(2):185). Per §2.7 disclosure: this is a defensive response by the originating investigator and cannot be read as independent confirmation of any claim it defends.

### 12.7.1 Other mechanism reviews referenced but not separately numbered

Other Sikirić-group review papers cited in the corpus as cluster-anchoring synthesis but not assigned numbered entries: Sikirić P et al. 2020 (*Gut Liver* 14(2):153–167, gnl18490); Sikirić 2012 (*Curr Med Chem* 19:126–132, PMID 22300085); Sikirić 2011 (*Curr Pharm Des* 17:1612–1632); MDPI 2022 (*Biomedicines* 10:3221, Sikirić group); Seiwerth S et al. 2021 (*Front Pharmacol* 12:627533, PMC8275860, Zagreb); Springer 2023 NO-system chapter (Inflammopharmacology); Cambridge repository preprint review (paraphrased "plasma BPC-157 returned to baseline within 24 h" — paraphrase not supported by Lee & Burgess 2025 primary, see §6.6). Józwiak M et al. 2025 (*Pharmaceuticals (Basel)* 18(2):185, PMC11859134, Maria Sklodowska-Curie Medical Academy Warsaw) — independent Eastern-European critical review.

### 12.7.2 Excluded regulatory / registry / vendor documents (not counted as primary; cited in prose in §10)

ClinicalTrials.gov NCT02637284 (Phase 1 PharmaCotherapia Mexico); ClinicalTrials.gov NCT07437547 (Phase 2 Hudson Biotech China); FDA Federal Register 2026-07361 (Docket FDA-2025-N-6895); FDA 503A bulks list April 22, 2026 (fda.gov/media/94155); TGA Schedule 4 interim decision Nov 2023; WADA Prohibited List 2022/2025/2026; USADA TUE policy; Health Canada April 14, 2025 advisory; DoD prohibited supplement list (DoDI 6130.06); DOJ Tailor Made Compounding 2018–2020 prosecution (press releases); HYTN Innovations April 23, 2026 announcement; ABC News April 14, 2026 TGA alert; OPSS / Sport Integrity Australia pages; Frier Levitt 2026 legal analysis; EU Clinical Trials Register (zero hits); WHO ICTRP (zero additional hits).

### 12.7.3 Excluded patent (not peer-reviewed primary; cited inline for in-vitro stability comparison only)

Diagen WO2014142764A1 (bepecin di-L-arginine salt; Rucman R + Pflaum Z inventors; per §2.7 disclosure, Rucman R is a co-author on multiple Sikirić-group primaries).

## 13. Synthesis Notes

### 13.1 Cross-section contradictions resolved (C1–C9)

The Phase 4 triangulation identified eight cross-section discrepancies, of which seven were Edit-resolved in section files (Phase 4.75 IC-10) and one (C8) was the rebuild's defining historical correction. The Phase 6 critique surfaced a ninth contradiction (Tohyama 2004 double-counting) and required a tenth structural fix (the §22/§32 placeholder downgrade with 52-primary recomputation). Each is documented here with the authoritative resolution adopted in synthesis:

- **C1 — Xu 2020 first-author institution.** Section E said "Air Force Medical University, Xi'an, China (same lab as He 2022)"; Section F said "PLA General Hospital (Beijing) / Academy of Military Medical Sciences." **Resolution:** Section E authoritative; Section F corrected. Author-list overlap with He L 2022 (Sun L, Ren F, Cui J, Zhang W, Wang S, Zhang K, He L, Zhang C, Hao Q, Zhang Y, Li M, Li W appear in both) decisively favors Xi'an. Adopted institution: **Fourth Military Medical University / Air Force Medical University, Xi'an**.

- **C2 — Sikirić 1993 *J Physiol Paris* PMID.** Section A said PMID 8298609; Section E said PMID 8298605. **Resolution:** Section A authoritative. Adopted PMID: **8298609**. DOI 10.1016/0928-4257(93)90038-U is unambiguous.

- **C3 — McGuire 2025 first-author attribution.** Section D mis-attributed first author as "Bemis-Standoli"; Sections A, E, F correctly identified McGuire FP. **Resolution:** Sections A/E/F authoritative. Adopted first author: **McGuire FP, Martinez R, Lenz A, Skinner L, Cushman DM**. This is the same class of misattribution that the S2 BPC-157 corpus was rebuilt to fix.

- **C4 — Lee & Burgess 2025 co-author middle initial.** Section D said "Burgess K"; Section E said "Burgess C"; Section F omitted. **Resolution:** Adopted **Burgess K** per Section D + Phase 4.75 IC-10 verification.

- **C5 — FDA Category 2 current status.** Section D had pre-April-2026 framing ("Category 2 designation remained in effect"); Section F had post-April-2026 authoritative framing ("removed April 22, 2026"). **Resolution:** Section F authoritative. Adopted: **BPC-157 removed from Category 2 on April 22, 2026 (nominations withdrawn); PCAC review scheduled July 23, 2026**.

- **C6 — Xue 2004 institution.** Originally noted as Second Military Medical University Shanghai (a non-cluster partial-independent replication). **Resolution (per IC-10):** corrected to **Fourth Military Medical University, Xi'an, China** — same cluster as Xu 2020 and He L 2022. This is a SECONDARY concentration finding: the "independent Chinese signal" is now itself a 3-paper single-institution cluster, not three independent confirmations. Explicit in §2.3 and §5.9.

- **C7 — Section C ref [5] author order.** Original draft had "Sever M, Klicek R"; corrected to **Klicek R, Sever M**.

- **C8 — He L 2022 misattribution as human study (the historical contradiction).** This is the contradiction between the rebuilt corpus and the S2-era dispatch that triggered the rebuild. **He L 2022 is rat + beagle dog only, never humans.** Preserved as a corrective framing throughout §6 and §7.

- **C9 — Tohyama 2004 cluster double-counting (Phase 6 critique resolution).** Pre-refinement, §2 aggregate enumeration counted Tohyama 2004 as INDEPENDENT (McGill/Diksic senior); §5.9 per-section counted it to Sikirić via co-authorship. Same paper, two different cluster attributions — internally contradictory cluster arithmetic. **Resolution adopted:** uniform sub-cluster rule (Sikirić co-authorship triggers Sikirić-cluster attribution everywhere). Tohyama 2004 is now counted to the Sikirić-Zagreb cluster in §2.2, §2.3, §3.5, §5.7, §5.9, §12.1 (cluster heading), and §12.6 (entry [54] reclassification). The aggregate-rule alternative (Diksic senior at McGill = independent) is abandoned.

- **C10 — Bibliography entries #22 and #32 placeholder-grade (Phase 6 critique resolution).** Pre-refinement, both entries were counted toward the 54-primary denominator despite lacking journal volume, page range, and DOI/PMID. **Resolution adopted:** downgrade both to `[corpus-unverifiable; not counted toward 52 primary denominator]`. Working denominator is now **52** (not 54). Cluster shares recomputed: Sikirić-Zagreb academic 39/52 = **75.0%** (was 74.1%); combined Zagreb-metropolitan 42/52 = **80.8%** (was 79.6%). Both downgraded entries remain numbered in §12 for citation-resolution stability; both are flagged inline at §8.3.1 (#22, VEGF immunohistochemistry) and §8.3.3 (#32, neuroleptics) with explicit corpus-unverifiable annotations.

### 13.2 Recovery stories explicitly flagged

Two corrections in this rebuild are explicit "recovery stories" — fabrications detected and corrected — and deserve highlighting:

1. **The He L 2022 species correction (rat + dog only, NO human PK).** The S2-era BPC-157 corpus cited He L 2022 as evidence of human pharmacokinetics. The 2022 paper has zero human subjects. This is the suspected fabrication-vector that motivated the entire rebuild. The corrected framing is anchored across §6.1, §6.6, §7.10, and §12.4 entry [48].

2. **The McGuire FP 2025 authorship correction (vs the S2-era Bemis-Standoli misattribution).** The S2 BPC-157 corpus mis-attributed PMC12446177 / DOI 10.1007/s12178-025-09990-7 / *Curr Rev Musculoskelet Med* 18(12):611–619 to "Bemis-Standoli." The correct first author is **McGuire FP**, with Martinez R, Lenz A, Skinner L, Cushman DM. This is the same class of misattribution as the He L 2022 case (downstream paraphrase distorting an upstream primary). The corrected framing is anchored at §3.1, §3.7, §7.9 and §12.7 entry [55].

### 13.2.1 Phase 6 critique-driven changes (refinement pass, 2026-05-24)

A separate refinement pass implemented the Phase 6 critique findings. The structural changes:

1. **Citation crosswalk.** Every inline section-letter cite ([A1]–[F38]) was renumbered to its corresponding §12 bibliography entry number (1–54), and previously-excluded mechanism reviews (McGuire, Gwyer, Vasireddi, Yuan, Sikirić 2025 Reply) were added as numbered entries 55–59 so that inline cites resolve mechanically.
2. **§22 / §32 downgrade.** Two placeholder-grade entries downgraded to `[corpus-unverifiable]`; primary denominator recomputed from 54 to 52; cluster shares recomputed (75.0% Sikirić, 80.8% combined Zagreb).
3. **Tohyama 2004 uniform rule.** Cluster-attribution contradiction resolved by adopting the sub-cluster rule consistently (Tohyama → Sikirić everywhere).
4. **Author / sponsor bias surfacing.** New §2.7 surfaces Sikirić-Pliva-Diagen industrial entanglement, Rucman-as-Diagen-inventor-and-Sikirić-coauthor connection, and the Sikirić 2025 defensive Reply paper history. §7.6 expanded to surface Lee commercial-clinical population overlap and the Lee 2021 / Tailor Made Compounding federal prosecution connection.
5. **Publication-bias overlay.** New §2.8 operationalises the McGuire 2025 publication-bias quote as a first-class interpretive lens. End-of-section reminders added at §3.10, §4.12, §5.10.
6. **Alternative-explanation surfacing.** Added: §3.2 (Stupnisek "balancing" as non-falsifiable); §6.5 (PD/PK disconnect as possible compound inertness, not only mechanism complexity); §7.4 (Lee 2024 IC 100% improvement as plausibly vehicle / placebo / regression-to-mean / selection); §4.11 (Sikirić MSK phenotype as plausibly generic anti-inflammatory); §8.3.1 (Hsieh angiogenesis as plausibly wound-healing-context-specific not tumor-relevant).
7. **FDA 2023 safety reasoning expansion.** §8.6 expanded with the four agency-stated safety-reasoning lines (impurity profile, insufficient human safety, route-of-administration claims without primary PK, chronic-exposure unknown). The April 22, 2026 Cat 2 removal is explicitly framed as procedural-via-nominations-withdrawal, not a safety clearance — the 2023 safety concerns remain formally unresolved.
8. **Section consumer notices.** Added at the head of §4 and §5 anchoring each section in §2 concentration framing and §2.8 publication-bias overlay for specialist agents reading sections in isolation.
9. **Vasireddi "4 of 36 assessed safety" datum** surfaced at §8.1 as the framing line for safety-base sizing.
10. **§4.10 denominator switch** clarified in-sentence (9/11 with in-vitro Chang Gung; 9/9 restricted to in-vivo).
11. **§13.8 non-English layer pointer** added below.

### 13.3 Sources excluded under whitelist

The following surfaced during section retrieval and were NOT cited (per binding constraints and the source whitelist):

- **ResearchGate Schlosser 2025 preprint** on BPC-157 SH3-domain Src-family kinase binding — non-peer-reviewed, first-author affiliation Cell Shot Nutrition (vendor-adjacent). Excluded. Flagged in §3.7 only to note that all currently public direct-binding hypotheses are preprint-tier.
- **AAOS 2025 systematic review abstract PDF** (`index.mirasmart.com/AAOS2025/`) — conference abstract, not peer-reviewed journal article. Excluded.
- **Reddit, Examine.com, Meeting Point Health, OrthoAndWellness, SDOMG, AgeMD, Ubie** — Tier 2.5 or below; used only as navigation aids to find primaries. Not cited.
- **Wikipedia** — used as navigation only; never cited.
- **Vendor pages** (peptideslabuk.com, weightlossandvitality.com, peptidefox.com, etc.) — explicitly excluded from any numerical claim per binding constraints. The Diagen patent figures cited in §6.4 came via vendor reproductions of the patent and are explicitly tagged `[vendor_label / patent]`; the figures are NOT load-bearing for any in-vivo or human claim in this report.
- **Compounding-pharmacy data sheets** (Tailor Made, Empower, etc.) — 503A pharmacy literature, not in the source whitelist for numerical claims. Mentioned in §7.3 only as the source the Lee 2021 study used, not as a numerical-claim source.
- **Columbia Undergraduate Science Journal commentary, orthoandwellness.com narrative review by Victor Prisk MD, superpower.com practitioner guides, droracle.ai clinical-guidance summaries** — Tier 2.5 mechanism commentary; cited in §8 as `mechanism_review` only for direction-of-concern framing, never grounding a numerical claim.

### 13.4 Honest absences

The following claims could not be verified against retrievable primary literature during this dispatch and were therefore dropped, downgraded, or explicitly tagged `[corpus-unverifiable]`:

- **Direct GHRH-receptor agonism by BPC-157** — frequently asserted in practitioner content; no primary peer-reviewed evidence of direct GHRH-R binding retrievable. Dropped; flagged at §3.4 and §3.8.
- **Direct NGF / BDNF receptor activation as an isolated, measured effect** — claims trace to Sikirić in-vivo CNS-injury models, not isolated growth-factor binding/induction assays. Dropped; flagged at §3.8.
- **BPC-157 increases mitochondrial function as a primary cell-level mechanism** — claims trace to in-vivo organ-protection assays, not isolated mitochondrial measurements. Dropped; flagged at §3.8.
- **Independent (non-Pliva, non-Zagreb) EGR-1 / NAB2 replication** — not found. Flagged as open gap at §3.3.
- **Independent (non-Zagreb) reconfirmation of 24-h gastric-juice stability** — not found. Single-source flag applied throughout §6.3.
- **Oral pharmacokinetics in any species** — no primary located. Absence finding at §6.2.
- **SC / IN / sublingual / transdermal PK in any species** — no primary located. Absence finding at §6.8.
- **Human Cmax / Tmax / t½ / AUC for any route** — no primary located. Absence finding at §6.6, §6.7, §6.9.
- **Human cancer-incidence, reproduction, pediatric, or chronic >14-day exposure data** — no primary located. Absence findings at §7.8.
- **Phase 2 PL 14736 UC efficacy outcome numerics** (Ruenzi 2005) — abstract-only; never published as full paper. `[corpus-unverifiable]` at §7.2.
- **Cerulein-pancreatitis primary** for BPC-157 — frequently referenced in secondary writeups but the primary in-house Sikirić paper is the bile-duct-ligation model; cerulein link appears to be review-level extrapolation. `[corpus-unverifiable]` at §5.6.
- **Mouse tumor-co-administration primary** — referenced in orthoandwellness narrative review but the primary citation could not be located in the indexed corpus. `[corpus-unverifiable]` at §8.3.1.

### 13.5 Sikirić 1993 primary text caveat

The Sikirić P, Petek M, Rucman R, Seiwerth S, Grabarevic Z, Rotkvic I et al. 1993 *J Physiol Paris* 87(5):313–327 paper is **paywalled** and was not directly retrievable in full text during this dispatch. The 24-h gastric-juice stability figure that underlies essentially every "stable gastric pentadecapeptide" downstream claim is therefore verified only by paraphrase via a 2025 Inflammopharmacology commentary on the 1993 original (https://link.springer.com/article/10.1007/s10787-025-01882-z) and via Sikirić-group reviews that repeat the figure without independent degradation-vs-time curves. **This is an unresolvable corpus limitation for the present dispatch**, flagged in the Phase 4.75 gate-4.75.json warnings list. The wiki entry treats the 24-h figure as single-source Zagreb-Pliva lineage; future re-rotations should attempt direct retrieval of the 1993 primary text if access becomes available.

### 13.6 Population-mismatch tagging audit

Every animal or in-vitro citation grounding a numerical or species-bound claim in this synthesis carries an in-line `[population-mismatch: <species>]` (or `[pm: <species>]`) tag in the same sentence as the cited primary, or with the species named as the sentence subject within 100 characters of the citation. The tag set used: rat, rabbit, mouse, beagle dog, db/db mouse, guinea pig, HUVEC, Caco-2, rat tendon fibroblast, rat aorta, rat brain. The Phase 4.75 IC-7 audit verified 47/47 animal citations passed this rule across the section files; the same discipline is preserved in this synthesis.

### 13.7 Re-rotation triggers (forward-looking)

The following events should trigger re-rotation of this canonical entry:

1. **Any new independent in-vivo replication of a Sikirić-group MSK or GI finding outside the Zagreb cluster.** This is the single largest evidence-quality gap in the entire entry.
2. **Any Phase 2 or Phase 3 RCT primary publication.** The most likely first readout is NCT07437547 (Hudson Biotech Phase 2 SC hamstring, est. completion February 2028).
3. **Any FDA reclassification update post-PCAC review (scheduled July 23, 2026).** Outcomes can include re-inclusion on the 503A bulks list, re-placement in Category 2, or no action.
4. **Any new Edwin Lee-clinic publication** (continues the Lee Orlando single-clinic concentration).
5. **Any independent replication of the He L 2022 cross-species PK** outside the Xi'an Fourth Military Medical University cluster.
6. **Direct retrieval and verification of the Sikirić 1993 *J Physiol Paris* primary text** with the 24-h gastric-juice degradation-vs-time curve.
7. **Any peer-reviewed publication of a direct molecular target / receptor for BPC-157** (the Schlosser SH3-domain hypothesis would need to clear peer review at a non-vendor-affiliated venue).
8. **Any human PK study posting results** (NCT02637284 oral, NCT07437547 SC, or a future Lee-clinic IV study with plasma assay).

### 13.8 Concentration-framing reminder for downstream layers (recomputed Phase 6)

This canonical academic-layer report is intended to be consumed by two supplementary layers (practitioner-layer and non-English-layer) and by downstream specialist agents recommending or evaluating BPC-157. Both layers and all such agents must propagate the §2 concentration framing (recomputed Phase 6): **75.0% of verifiable primary evidence (39/52) is from the Sikirić-Zagreb academic cluster, 80.8% (42/52) combined Zagreb-metropolitan; no independent in-vivo MSK replication exists; all published US human evidence is single-investigator single-clinic (Lee Orlando ≈ 31 cumulative subjects across 3 papers); all anti-tumor evidence is 100% Sikirić-cluster; the "independent Chinese PK + safety + gastric-ulcer signal" is itself a 3-paper single-institution Xi'an cluster.** Layered onto concentration risk is the §2.7 author/sponsor entanglement (Sikirić-Pliva-Diagen continuous authorship; Lee commercial-clinical overlap; Tailor Made Compounding federal prosecution) and the §2.8 publication-bias overlay (positive-finding-only literature per McGuire 2025). Stripping any of these framings from a downstream recommendation is not honest summarization.

### 13.9 Non-English layer pointer (Phase 6 critique addition)

See `vault/library/peptides/bpc-157/non-english-layer.md` for Croatian / Chinese-language coverage and any contradictions logged to `vault/meta/contradictions.md`. The academic-layer reader of this canonical entry should consult the non-English layer for completeness on (a) Croatian-language Sikirić-group publications not indexed in English-language databases, (b) Chinese-language Xi'an Fourth Military Medical University publications adjacent to the He L 2022 / Xu 2020 / Xue 2004 cluster, and (c) any cluster-share or directional findings that contradict this synthesis.

---

End of Section 13 — End of BPC-157 Canonical Academic Layer Report.