---
title: Active Contradictions
type: reference
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
last_updated: 2026-05-23
depends_on: []
superseded_by: null
review_cadence: session
permalink: a-plus-maxing/meta/contradictions
---

# Active Contradictions

Log of unresolved disagreements between sources, between sources and Walter's n=1 data, or between protocol claims.
One section per contradiction. Close out when resolved with the resolution path noted.

## Template
```
### YYYY-MM-DD — short title
- **Pages involved:** [[page-a]], [[page-b]]
- **Claim A:** what page-a asserts, with source
- **Claim B:** what page-b asserts (or what Walter's data shows), with source
- **Why it matters:** what decision this blocks
- **Resolution plan:** experiment, additional research, doctor consult, etc.
- **Status:** open | resolved (YYYY-MM-DD)
```

---

## Open

_(none open)_

## Resolved

### 2026-06-04 — ADR/doc home: pipeline `docs/adr/` + `docs/prd/` vs project `vault/decisions/`
- **Status:** resolved 2026-06-04 (S25, bead `fm4`)
- **Was:** the `prd-development` + `adr-development` pipelines write to `docs/prd/` + `docs/adr/`, but the Cross-Document Ownership Matrix homed architectural decisions in `vault/decisions/`.
- **Resolution:** product-pipeline artifacts (PRD / ADR / spec / build-plan / task-plan) live under `docs/` (`docs/prd/`, `docs/adr/` — numbered ADRs from `/create-adr`); vault-native knowledge-graph / governance decisions stay in `vault/decisions/` (date-named). The CLAUDE.md Cross-Document Ownership Matrix was split to record this. The V1 ADR set (ADR-0001…0007) lands in `docs/adr/`; the vault-native `2026-05-16-system-architecture.md` was formally superseded by ADR-0002/0004/0006.

### 2026-05-24 — BPC-157 He L 2022 species misattribution (canonical S2 fabrication caught and corrected)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §6, §13.2; [[compounds/bpc-157]]
- **Claim A (prior S2 entry, archived):** He L 2022 *Front Pharmacol* 13:1026182 cited as a human pharmacokinetic study
- **Claim B (current rebuild):** PMC9794587 verified independently as rats (n=324 Sprague-Dawley) + beagle dogs (n=6); ZERO human subjects in this paper
- **Why it mattered:** the S2 misattribution propagated as "BPC-157 has published human PK data" — a load-bearing claim that justifies practitioner dose recommendations. The actual literature has NO peer-reviewed human PK paper; practitioner doses are rat-allometric extrapolations.
- **Resolution plan:** corrected in rebuilt research-report.md (§6); both Section D and Section E independently verified against PMC9794587 during Phase 3.5 judge gate; Phase 4.75 IC-13 corpus-scoping confirmed
- **Status:** resolved 2026-05-24 (this is the canonical fabrication catch that justified the rebuild)

### 2026-05-24 — Xu 2020 institution (Phase 4.75 IC-10 finding C1)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §8.4, biblio
- **Claim A (Section F prior):** PLA General Hospital (Beijing) / Academy of Military Medical Sciences
- **Claim B (verified):** Fourth Military Medical University / Air Force Medical University, Xi'an, China — same institutional cluster as Xu 2020 and He L 2022
- **Why it mattered:** placed in wrong cluster → corrupted concentration-audit. Correction: places three primaries (Xu 2020, He L 2022, Xue 2004 per C6) into a single Xi'an institutional cluster — the "independent Chinese signal" is itself single-cluster (3 papers from one institution).
- **Resolution plan:** corrected in section-F.md + research-report.md
- **Status:** resolved 2026-05-24

### 2026-05-24 — Sikirić 1993 PMID typo (Phase 4.75 IC-10 finding C2)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §6.3 biblio
- **Claim A (Section E prior):** PMID 8298605
- **Claim B (verified):** PMID 8298609 (Sikirić P et al., *J Physiol Paris* 1993;87(5):313-327)
- **Why it mattered:** one-digit typo would prevent downstream agents from PubMed-resolving the citation
- **Resolution plan:** corrected in section-E.md
- **Status:** resolved 2026-05-24

### 2026-05-24 — McGuire 2025 first-author misattribution (Phase 4.75 IC-10 finding C3)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §7.10, biblio
- **Claim A (Section D prior):** Bemis-Standoli et al. (residue of S2-era misattribution)
- **Claim B (verified):** McGuire FP, Martinez R, Lenz A, Skinner L, Cushman DM. *Curr Rev Musculoskelet Med* 2025;18(12):611-619 (Univ of Utah)
- **Resolution plan:** corrected in section-D.md
- **Status:** resolved 2026-05-24

### 2026-05-24 — Lee & Burgess 2025 co-author initial (Phase 4.75 IC-10 finding C4)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §6.1, §7.6, biblio
- **Claim A (Section E prior):** Burgess C
- **Claim B (verified — Section D had right):** Burgess K
- **Resolution plan:** corrected in section-E.md
- **Status:** resolved 2026-05-24

### 2026-05-24 — FDA Cat 2 status currency (Phase 4 triangulation finding C5)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §10
- **Claim A (Section D pre-update):** "FDA September 2023 placed BPC-157 in Category 2; designation remained in effect as of March 2025"
- **Claim B (Section F current):** FDA REMOVED BPC-157 from Cat 2 / nominations withdrawn April 22, 2026 (Fed Reg 2026-07361, docket FDA-2025-N-6895); PCAC review scheduled July 23, 2026
- **Why it mattered:** removal was VIA NOMINATIONS WITHDRAWAL, NOT safety clearance — the FDA's 2023 safety concerns (impurity profile, insufficient safety data, chronic-exposure unknown) remain formally unresolved
- **Resolution plan:** Section F authoritative; Section D updated with cross-reference; framing carried through Phase 7 refine
- **Status:** resolved 2026-05-24

### 2026-05-24 — Xue 2004 institution (Phase 4.75 IC-10 finding C6 — secondary concentration finding)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §5.1, §2 (concentration enumeration)
- **Claim A (Section C prior):** Second Military Medical University, Shanghai, China
- **Claim B (verified):** Fourth Military Medical University, Xi'an, China
- **Why it mattered:** **secondary concentration finding** — places Xue 2004 in the same Xi'an institutional cluster as Xu 2020 (C1) and He L 2022. The "independent Chinese replication" of BPC-157 work is itself a single-institution cluster (3 papers from Fourth Military Medical Univ Xi'an). The narrative that BPC-157 has been independently replicated by a non-Sikirić Chinese group needs heavy qualification.
- **Resolution plan:** corrected in section-C.md and surfaced as a first-class finding in research-report.md §2
- **Status:** resolved 2026-05-24

### 2026-05-24 — Section C [5] author order (Phase 4.75 IC-10 finding C7)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §5.3, biblio
- **Claim A (Section C prior):** Sever M, Klicek R, Radic B et al.
- **Claim B (verified PMID 24304574):** Klicek R, Sever M, Radic B et al.
- **Resolution plan:** corrected in section-C.md
- **Status:** resolved 2026-05-24

### 2026-05-23 — BPC-157 PK paper author misattribution (resolved same-session)
- **Pages involved:** [[library/peptides/bpc-157/research-report]] §6 and bibliography [A-11]
- **Claim A:** original deep-mode dispatch attributed PMC9794587 PK paper to "Xu et al. 2022"
- **Claim B:** non-English literature follow-up dispatch (Agent G) confirmed correct first-author is **He L** (Fourth Military Medical University Department of Biopharmaceutics group, co-author overlap with Xue 2004 and Huang 2015)
- **Why it mattered:** misattribution would propagate to future citations and downstream queries; "Xu et al. 2022" doesn't resolve to the actual paper on author search
- **Resolution plan:** corrected throughout research-report.md in 2026-05-23 supplementary edit pass; bibliography entry updated with full author list; revision-log frontmatter records the fix
- **Status:** resolved 2026-05-23
