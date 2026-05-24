---
title: Wiki Operation Log
type: reference
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
last_updated: 2026-05-23
depends_on: []
superseded_by: null
review_cadence: session
permalink: a-plus-maxing/meta/log
---

# Wiki Operation Log

Append-only. One line per ingest/edit/lint/export operation.
Format: `YYYY-MM-DD | op | page | note`

Ops: `create`, `update`, `link`, `lint`, `export`, `delete`, `schema`

---

- 2026-05-23 | schema | WIKI.md | initial schema established (compounds, biomarkers, protocols, parameters, decisions)
- 2026-05-23 | create | meta/index.md | initial index seeded from existing pages
- 2026-05-23 | create | meta/contradictions.md | empty log seeded
- 2026-05-23 | create | meta/log.md | this file
- 2026-05-23 | create | compounds/_template.md | compound page template
- 2026-05-23 | create | biomarkers/_template.md | biomarker page template
- 2026-05-23 | update | meta/index.md | added compound + biomarker templates
- 2026-05-23 | create | meta/operator-profile.md | slow-changing Walter context (scaffold awaiting Jan 2026 issue characterization)
- 2026-05-23 | create | meta/current-state.md | fast-changing snapshot (biomarkers, active protocols/compounds)
- 2026-05-23 | create | meta/goals.md | goal hierarchy + hard limits + doctor-handout queue
- 2026-05-23 | create | library/peptides/_source-whitelist.md | type-tagged source whitelist with admissibility matrix
- 2026-05-23 | create | library/peptides/_triage.md | peptide class taxonomy + triage scoring rubric
- 2026-05-23 | update | meta/index.md | indexed all three meta files + peptide refs
- 2026-05-23 | move | library/peptides/_source-whitelist.md → library/_source-whitelist.md | generalized from peptide-only to all health research
- 2026-05-23 | update | library/_source-whitelist.md | retitled, domain-extension pattern documented
- 2026-05-23 | update | WIKI.md | added Agent Consumers section with 14-agent roster (peptide, endocrine, lymphatic, gi, cardio, recovery, sleep, longevity, trainer, nutrition, supplement, labs, mental-perf, medical-liaison)
- 2026-05-23 | update | meta/index.md | updated whitelist path
- 2026-05-23 | create | library/peptides/bpc-157/research-report.md | deep-mode dispatch; 10,193 words; ~80 distinct citations; Sikiric-share ~76-80% across deduplicated primaries
- 2026-05-23 | create | compounds/bpc-157.md | derived compound entry; evidence_tier C; risk_tier experimental; status researching
- 2026-05-23 | update | library/peptides/_triage.md | added BPC-157 to Done queue
- 2026-05-23 | update | meta/index.md | indexed bpc-157 research-report and compound entry
- 2026-05-23 | update | compounds/_template.md | added Non-English Literature Coverage and Prescribing-Practice Layer sections (every future compound entry gets these by default)
- 2026-05-23 | update | library/_source-whitelist.md | added Tier 2.7 (Practitioner protocols), Tier NE (Non-English literature), new `practitioner_protocol` type-tag, expanded admissibility matrix
- 2026-05-23 | create | library/peptides/bpc-157/practitioner-layer.md | supplementary dispatch — Compounding Lab AU is only dose-explicit current data sheet; Edwin Lee IV outlier; consensus subQ 250-500 µg/day 4-6 wk
- 2026-05-23 | create | library/peptides/bpc-157/non-english-layer.md | supplementary dispatch — Korean antinociception primaries (Park 2021, Jung 2022), Chinese porcine Xue 2004b + clopidogrel Wu 2020, Croatian conf abstracts (psoriasis, fistula, nephrotoxicity), Pliva patent estate; zero Russian primaries; PL 14736 Phase II UC not located in any language
- 2026-05-23 | update | library/peptides/bpc-157/research-report.md | author attribution fixed [A-11] He L 2022 ← was "Xu et al."; new §7.12 (pain/nociception), §7.13 (dermatology signal), §7.14 (porcine corroboration); §11 clopidogrel interaction; §19.5 supplementary dispatch summary
- 2026-05-23 | update | compounds/bpc-157.md | added Non-English Literature Coverage + Prescribing-Practice Layer sections; updated dose with full sourcing; added clopidogrel interaction; added 3 layer pointers in Relations
- 2026-05-24 | update | library/peptides/bpc-157/research-report.md | rebuilt deep-mode via /aplus-research --update=suspect-fabrications; prior version archived at vault/library/peptides/bpc-157/_archive/2026-05-24-suspect-fabrications/research-report.md; 20,635 words refined to 1,039 lines; 52 deduplicated primaries (post #22/#32 downgrade); 6 paired retrieval+judge dispatches (3 needed iter-2 remediation, all PASS at 99/100 deep threshold); IC-13 corpus-scoping 30/30 probes PASS, zero fabrications; FIXED canonical S2 misattribution of He L 2022 (was claimed as human PK study, is rat+beagle dog only — confirmed via PMC9794587)
- 2026-05-24 | update | compounds/bpc-157.md | rebuilt from new research-report; prior archived at vault/compounds/_archive/bpc-157-2026-05-24-suspect-fabrications.md; risk_tier remains experimental; surface FDA April 22 2026 Cat 2 removal-via-nominations-withdrawal (not safety clearance)
- 2026-05-24 | update | library/peptides/bpc-157/practitioner-layer.md | rebuilt; prior archived
- 2026-05-24 | update | library/peptides/bpc-157/non-english-layer.md | rebuilt; prior archived
- 2026-05-24 | update | meta/contradictions.md | 7 new resolved entries (C1–C7) from Phase 4.75 IC-10 + Phase 4 triangulation; 1 historical (C8 = He L 2022 species misattribution caught and corrected, supersedes the 2026-05-23 Xu/He attribution resolution which only fixed authorship not species)
