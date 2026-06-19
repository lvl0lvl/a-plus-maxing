---
title: Wiki Index
type: reference
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
last_updated: 2026-05-23
depends_on: []
superseded_by: null
review_cadence: session
permalink: a-plus-maxing/meta/index
---

# Wiki Index

Catalog of every wiki entity page by type. Update on every page create/delete.
Non-wiki content (sessions, daily, weekly, reviews, interactions, artifacts) is NOT listed here — see folders directly.

---

## compounds/
- [[compounds/_template]] (template only)
- [[compounds/bpc-157]] (status: researching; evidence_tier: C; risk_tier: experimental)
- [[compounds/tb-500]] (status: researching; evidence_tier: C; risk_tier: experimental)
- [[compounds/ghk-cu]] (status: researching; evidence_tier: C; risk_tier: experimental)
- [[compounds/kpv]] (status: researching; evidence_tier: C; risk_tier: experimental)

## biomarkers/
- [[biomarkers/_template]] (template only)
- [[biomarkers/lp-a]] (Lp(a) — lipoprotein(a); category: blood; confidence: established)
- [[biomarkers/apob]] (ApoB — apolipoprotein B; category: blood; confidence: established)
- [[biomarkers/ldl-c]] (LDL-C — LDL cholesterol; category: blood; confidence: established)
- [[biomarkers/hdl-c]] (HDL-C — HDL cholesterol; category: blood; confidence: established)
- [[biomarkers/triglycerides]] (Triglycerides; category: blood; confidence: established)
- [[biomarkers/hs-crp]] (hs-CRP — high-sensitivity C-reactive protein; category: blood; confidence: established)
- [[biomarkers/glyca]] (GlycA — glycoprotein acetylation; category: blood; confidence: provisional)

## protocols/
- [[protocols/exercise]]
- [[protocols/meal-template]]
- [[protocols/sleep]]
- [[protocols/supplement-stack]]

> Note: existing protocol files predate the WIKI.md schema. They will be re-templated lazily — on next edit, conform to the protocols/ template.

## parameters/
_(none yet)_

## decisions/
- [[decisions/2026-05-16-system-architecture]]
- [[decisions/2026-05-23-wiki-schema]]
- [[decisions/2026-05-23-source-whitelist]]
- [[decisions/2026-05-23-aplus-research-skill]]
- [[decisions/2026-05-26-foundation-role-agent-md-location]]
- [[decisions/Project Setup]]

## experiments/
- [[experiments/_template]] (template only)

## library/
- [[library/_source-whitelist]]
- [[library/methodology/evidence-tiers]]
- [[library/methodology/n-of-1-trial-design]]
- [[library/peptides/_triage]]
- [[library/peptides/bpc-157/research-report]] (rebuilt 2026-05-24 via /aplus-research --update=suspect-fabrications; 1,039 lines / ~20K words refined; 52 dedup primaries; 80.8% Sikirić-Zagreb metro; 6 paired retrievals; IC-13 30/30 PASS; PRIOR ARCHIVED)
- [[library/peptides/bpc-157/practitioner-layer]] (rebuilt 2026-05-24; prescribing-practice; pharmacies + named physicians + consensus dose; PRIOR ARCHIVED)
- [[library/peptides/bpc-157/non-english-layer]] (rebuilt 2026-05-24; Croatian/Chinese/Russian/Korean coverage; PRIOR ARCHIVED)
- [[library/peptides/tb-500/research-report]] (2026-06-19 via /aplus-research --mode=deep; ~11K words; 79 dedup bibliography entries; 7 paired-judge sections @99; gates 2.75→8.5 attested PASS; chain intact)
- [[library/peptides/tb-500/practitioner-layer]] (2026-06-19; prescribing-practice; Seeds + A4M; no admissible compounding data sheet — non-compoundable)
- [[library/peptides/tb-500/non-english-layer]] (2026-06-19; Russian + Chinese verified primaries; originator-country English-origin)
- [[library/peptides/ghk-cu/research-report]] (2026-06-19 via /aplus-research --mode=deep; ~11.8K words; 67 dedup entries; 7 paired-judge sections @99; gates 2.75→8.5 attested PASS; chain intact)
- [[library/peptides/ghk-cu/practitioner-layer]] (2026-06-19; topical cosmetic + injectable conventions; Empower 0.5% compounded data sheets)
- [[library/peptides/ghk-cu/non-english-layer]] (2026-06-19; 3 Russian primaries; Chinese channel-gap; originator US-origin)
- [[library/peptides/kpv/research-report]] (2026-06-19 via /aplus-research --mode=deep; ~11.1K words; 47 dedup entries; 7 paired-judge sections @99; gates 2.75→8.5 attested PASS; chain intact)
- [[library/peptides/kpv/practitioner-layer]] (2026-06-19; oral/SC/topical conventions; no admissible compounding data sheet)
- [[library/peptides/kpv/non-english-layer]] (2026-06-19; Russian/Chinese/Italian all none-located — Chinese KPV science is English-published)
- [[library/biomarkers/lp-a/research-report]] (Lp(a) standard /aplus-research; 16 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/apob/research-report]] (ApoB standard /aplus-research; 23 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/ldl-c/research-report]] (LDL-C standard /aplus-research; 17 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/hdl-c/research-report]] (HDL-C standard /aplus-research; 19 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/triglycerides/research-report]] (Triglycerides standard /aplus-research; 19 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/hs-crp/research-report]] (hs-CRP standard /aplus-research; 23 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[library/biomarkers/glyca/research-report]] (GlycA standard /aplus-research; 19 sources; gates 2.75/3.5/4.25/4.75 attested)
- [[methodology/anthropic-skill-evaluation-rubric]]

## dna/
- [[dna/analysis]]

## labs/
_(none yet — first panel July 2026)_

---

## Cross-references to non-wiki anchors
- [[architecture/Architecture Overview]]
- [[design/artifact-design-protocol]]
- [[rubrics/Document Management Rubric]]
- [[meta/overview]]
- [[meta/targets]]
- [[meta/operator-profile]]
- [[meta/current-state]]
- [[meta/goals]]
- [[meta/contradictions]]
- [[meta/log]]
- [[meta/landmarks]] (NEW S4, landmark-agnostic register)
- INVARIANTS.md at repo root (NEW S4, 11 named invariants)
- .claude/skills/aplus-research/lib/gate_attest.py (NEW S4, canonical gate JSON writer)
- .claude/hooks/enforce-role-inlining.sh (NEW S4, role-profile PreToolUse hook)
- design/health-edge-case-reviewer-design.md — Pass-2 Role 3 design doc Final (S11 close, 2026-05-27)
- design/medical-safety-reviewer-design.md — Pass-2 Role 4 design doc Final (S12 close, 2026-05-28)
