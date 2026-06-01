# Phase 0 — aplus-research PLAN (genetics-specialist domain research)

- **Skill:** aplus-research (wraps deep-research). **Mode:** deep. **target_type:** reference (clinical-genetics knowledge; NOT a compound/biomarker/protocol wiki entry).
- **target_class:** other. **target_slug:** genetics-specialist.
- **Deliverable:** `design/.genetics-specialist-design-work/domain-research.md` (≥10,000 words deep floor). NO vault writes (PROTOCOL DO-NOT).
- **Goal-agnostic (PF-S2-04):** the 4 meta context files load for linkage but operator personalization is NOT injected into the research question. This is canonical reference research the genetics-specialist agent later personalizes at dispatch.
- **Gates required (deep, reference):** 2.75 (schema-only), 3.5 (judge, attested), 4.25 (id-reconcile, attested), 4.75 (integrity, attested), 6 (critique, attested). NO 7.5/8.5 (compound-only).

## Research question (goal-agnostic)

What is the canonical, evidence-disciplined knowledge a genetics & pharmacogenomics specialist agent must hold to (1) interpret germline SNP/variant data, (2) translate drug-gene status into prescriber-facing PGx flags, (3) interpret common nutrigenomic/wellness variants, and (4) safely govern disease-risk variant findings — including the load-bearing safety floors (DTC-raw≠diagnostic, PGx-informs-not-authorizes, risk-variant≠disease→genetic-counselor+MD, genetic exceptionalism/privacy)?

## Section plan (4 retrieval + 4 paired judges)

| Sec | Title | Scope |
|---|---|---|
| A | Variant interpretation framework & DTC raw-data limitations | ACMG/AMP 2015 5-tier classification; penetrance vs expressivity; monogenic vs polygenic (PRS); allele frequency (gnomAD); ClinVar/ClinGen; **DTC 23andMe raw-genotype false-positive rates + FDA/clinical-confirmation requirement** |
| B | Pharmacogenomics: CYP450 + non-CYP drug-gene | CYP2D6/2C19/2C9/3A4-5 star alleles, activity scores, PM/IM/NM/RM/UM phenotypes; VKORC1+CYP2C9/warfarin, TPMT+NUDT15/thiopurines, DPYD/fluoropyrimidines, SLCO1B1/statins, UGT1A1/irinotecan; CPIC, PharmGKB levels, FDA Table of PGx Biomarkers; **PGx-informs-not-authorizes** |
| C | HLA immunogenetic risk alleles + nutrigenomics | HLA-B*57:01/abacavir, HLA-B*15:02 & A*31:01/carbamazepine, HLA-B*58:01/allopurinol, G6PD; nutrigenomics: MTHFR C677T/A1298C+folate, CYP1A2*1F/caffeine, FTO, APOE+diet, MCM6-LCT/lactase, ALDH2*2/alcohol; **overinterpretation caveats** |
| D | Disease-risk variants, counseling governance & data ethics | BRCA1/2 (HBOC), Lynch/MMR, APOE-ε4/Alzheimer, hereditary thrombophilia (FVL, prothrombin G20210A), familial hypercholesterolemia; ACMG SF v3 secondary findings; genetic counseling referral norms; GINA + genetic exceptionalism/privacy; **DTC→clinical-confirmation pathway; EMERGENCY-class finding routing** |

## Triangulation rule
Cross-section numerical/identifier claims (gene symbols, star-allele functional assignments, allele frequencies, PMIDs, guideline names/years) must agree (Phase 4 + 4.25 ID-reconcile).

## Source plan (per _source-whitelist.md)
Tier 1 (PubMed/PMC, NEJM/Lancet/Nature/AJHG/Genetics in Medicine), Tier 2 (FDA Table of PGx Biomarkers, FDA labels via DailyMed). Authoritative consortia/knowledgebases (CPIC, PharmGKB, ClinGen, ACMG) tagged `mechanism_review` (consensus/systematic synthesis of primaries) or `regulatory` for FDA/EMA. Studies tagged by design (rct/meta_analysis/cohort/open_label/animal/in_vitro). No vendor/anecdote grounding numerical claims. Every animal/in_vitro numerical claim carries `[population-mismatch: <species>]`.

## Parallel agent plan
Phase 3: 4 retrieval agents (A–D) parallel → start-iteration 3.5 → 4 judge agents (A–D) parallel. Deep judge threshold = 99/100; HALT sections re-dispatched with judge findings (iter ≤3). Then 4.25 id-reconcile, 4.75 integrity, 5 synthesize, 6 critique, 7 refine.
