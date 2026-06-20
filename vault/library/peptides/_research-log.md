---
title: Peptide-Library Research Track — Log
type: note
permalink: a-plus-maxing/library/peptides/research-log
status: active
created: 2026-06-18
last_reviewed: 2026-06-18
review_cadence: per research session
---

# Peptide-Library Research Track — Log

Session-to-session continuity for the **peptide-library research track** (distinct
from the plan-generation pipeline track, a-plus S72–S73). Each entry separates
**DONE (verified)** from **CLAIMED (asserted — re-checkable, not yet re-audited by a
second party)** so the next session can re-check claims rather than trust them. The
canonical queue lives in [[_triage]]; this file owns the narrative + the claim ledger.

---

## 2026-06-18 — BPC-157 deep re-research + aplus-research skill operationalization

### DONE (verified — mechanical evidence on disk / on main)
- **BPC-157 wiki entry shipped** (PR #150, a-plus main `3bc257f`): `compounds/bpc-157.md`
  + `library/peptides/bpc-157/research-report.md` (~11.7k words) + practitioner-layer +
  non-english-layer + full `.provenance/` (8 gate JSONs, 5 judges, 6 sections). Prior
  suspect entry archived at `_archive/2026-06-18-suspect-fabrications/`. Triage "Done"
  row updated (dedup).
- **aplus-research skill made operational** — two merged PRs:
  - **#148** (`78fa63c`) — engine: AR-6 (gate_attest per-iteration freshness; partial
    remediation no longer false-stales earlier-passed sections) + AR-7 (structured gate
    fields accepted as a fenced ```json block) + SKILL.md verifier-output contract.
    Self-test 16→20.
  - **#151** (`2869530`) — doc/schema traps a real run would still hit: AR-5 (gate-2.75
    example was missing schema-required `timestamp` → first-gate HALT), AR-8 (gate-6/7.5/8.5
    schemas forbade the `iterations` field 4.25/4.75 require → later-gate rejection), AR-1
    (pre-flight HALTs if wrapped `deep-research` is missing/dangling, or `jsonschema` absent),
    AR-2 (documented WebSearch/WebFetch + filesystem-Write substitution for the MCP tools).
  - Generalized engine core also promoted to `skills_library` (PR #63, rigor 1.2.0) for
    reuse by other projects.
  - Verified: gate_attest self-test **20/20**; gate-2.75-without-timestamp correctly
    rejected; gate-6/7.5/8.5 accept `iterations` with/without. No regression.
- **Net: another session can pull a-plus main and run `/aplus-research` end-to-end** — no
  skill code or doc trap is left. Only prereqs are environment-level and now fail loudly
  (see prep checklist below).

### CLAIMED (asserted this session — backed by `.provenance/` but NOT independently re-audited)
A skeptical next session can re-check each via the cited artifact rather than re-running:
- All **7 attested gates PASS** (2.75/3.5/4.25/4.75/6/7.5/8.5), chain intact →
  re-check: `vault/library/peptides/bpc-157/.provenance/gates/*.json` + `verify-chain`.
- **Every citation independently verified real** (NCTs via clinicaltrials.gov API; PMIDs;
  Federal Register 2026-07361) → re-check: the report's reference list against the sources.
- Substantive conclusions to treat as claims, not settled fact:
  **no completed human RCT** with posted results; **~85% single-lab** concentration
  (11/13 in-vivo efficacy primaries Sikiric/Zagreb) with only tendon-repair + VEGFR2-
  angiogenesis independently corroborated; **"~15-min half-life" is rat-IV** (He 2022),
  no human PK; **FDA removed BPC-157 from 503A Cat-2 ~Apr 2026 ≠ approval** (still
  unapproved + WADA-S0). evidence_tier **C** / risk_tier **experimental**.
- Methodology caveat (claimed): this run executed the gates partly **by hand** with
  WebSearch/WebFetch + filesystem-Write substituted for Tavily/basic-memory (the skill was
  not registered in the orchestrating session). The gate logic is tool-agnostic, but the
  retrieval breadth depends on the substitute search — a re-run with Tavily may surface more.

### SWEEP DIRECTIVE (operator, 2026-06-19): deep-pass EVERY peptide
The two-pass triage model is overridden: every peptide in [[_triage]] gets a full
`/aplus-research --mode=deep` run + PR cycle, no ranking gate. Deep-mode baselines hold;
a ceiling may be lowered only with a documented evidence reason here (no guessing).

---

## 2026-06-19 — TB-500 / Thymosin Beta-4 deep-pass (sweep entry 1)

### DONE (verified — mechanical evidence on disk)
- **TB-500 entry shipped:** `compounds/tb-500.md` + `library/peptides/tb-500/research-report.md`
  (~11K words, 79 dedup primaries) + practitioner-layer + non-english-layer + full
  `.provenance/` (7 attested gate JSONs, 7 judge JSONs, 7 sections + id-reconcile).
- **All 7 gates attested PASS** (2.75 scope, 3.5 paired-judge @99, 4.25 reconcile, 4.75
  integrity, 6 critique, 7.5 risk-floor, 8.5 layers); `verify-chain` intact (system python3).
- **Independent paired-judge gate worked:** caught a CRITICAL FDA-503A inversion + 6 other
  real errors (DOI misattribution, population mislabel, trial-status, tally miscounts) across
  iter-1→4; cross-section reconcile caught 3 more (incl. the stale Cat-2 status); zero fabrications.

### CLAIMED (asserted this session — backed by `.provenance/`, re-checkable, not independently re-audited)
- Marketed "TB-500" = Ac-LKKTETQ fragment ≠ studied full-length Tβ4 (Esposito 2012). 
- No human RCT met a primary endpoint for ANY Tβ4 indication (SEER-1 p=0.0656 terminated; ARISE-3 missed); ZERO athletic human evidence.
- Bidirectional cancer signal (pro-metastatic melanoma over-expression; myeloma suppressor) — net prudent contraindication for active/recent malignancy.
- FDA removed from 503A Cat-2 ~Apr 2026 (FR 2026-07361, NOT approval); WADA S2.3 prohibited; evidence_tier C / risk_tier experimental.
- Methodology caveat: WebSearch/WebFetch substituted for Tavily MCP (AR-2); gate logic tool-agnostic, retrieval breadth may differ from a Tavily run.

### Process / skill meta-findings surfaced (for skill_consolidator beads)
- Retrieval-agent "source tally" counts are an error-prone class that slips first-pass judging → add a mechanical tally-vs-enumeration self-check to retrieval briefs.
- `gate_attest` requires `start-iteration` BEFORE the verifier writes (mtime guard) — dispatching judges first forces a wasteful re-run; document the ordering / support hashing pre-existing verifier output.
- bda merge audit (`audit-research-provenance.sh`) is keyed by SPECIALIST slug + needs a Python-3.14 `.venv`; doesn't cleanly apply to a direct library-entry slug on a py3.9 machine. Verify-chain (system python3) is the working integrity proof.

---

## 2026-06-19 — GHK-Cu (Copper Tripeptide-1) deep-pass (sweep entry 2)

### DONE (verified — mechanical evidence on disk)
- **GHK-Cu entry shipped:** `compounds/ghk-cu.md` + `library/peptides/ghk-cu/research-report.md` (~11.8K words, 67 dedup entries) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 7 judges + 7 sections + id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@99/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Independent gates caught real errors:** 3.5 paired judges caught a citation-provenance overclaim (decline figure), a stale tally line, a transposed PMID (8227352→8227353), and a WADA-completeness gap; 4.25 reconcile caught a cross-section PMID mismatch (Maquart 3169264 vs 3049153) + a Mulder design conflation. The suspicious high practitioner PMIDs (41490200/41476424) VERIFIED real. Zero fabrications. (Self-checks in retrieval briefs cut the HALT rate vs TB-500.)

### CLAIMED (asserted this session — backed by `.provenance/`, re-checkable)
- Human evidence is TOPICAL-only (Mulder 1994 positive diabetic-ulcer RCT, n-unstated/ProCyte-COI; Miller 2006 negative post-laser RCT; AAD-2002 anti-aging = non-peer-reviewed posters); NO injectable/systemic human study.
- Review/claims layer ~70-85% Pickart/Skin-Biology commercial nexus (a 2015 review denies COI despite all-author Skin Biology affiliation); efficacy-primary Pickart share ~0.11 (below 70% gate).
- Gene-resetting (~⅓ genome) + anti-cancer claims are cMap bioinformatic predictions, not efficacy; endogenous-GHK decline figure traces only to Pickart's 1973 unpublished thesis.
- Topical CIR "safe as used"; injectable copper-overload risk, Wilson's disease = absolute contraindication; monitorable via serum copper/ceruloplasmin. WADA not individually named (S0, arguably S2, exposure for injectable).
- Regulatory nuance (flagged, evolving): non-injectable reportedly restored to 503A Cat-1 ~2026-05-14 (inconsistent across trackers); injectable not on Cat-1.

### Additional meta-findings (skill_consolidator beads)
- Verifier agents sometimes emit schema-invalid gate JSON blocks (stray `note` key; string where integer; markdown-bold `verdict: **PASS**` breaks the parser) → add "emit schema-valid JSON + plain `verdict: PASS`, self-validate before returning" to every gate-verifier brief. (Extends bead 2h6/71c family.)

---

## 2026-06-19 — KPV (Lys-Pro-Val · α-MSH(11-13)) deep-pass (sweep entry 3)

### DONE (verified — mechanical evidence on disk)
- **KPV entry shipped:** `compounds/kpv.md` + `library/peptides/kpv/research-report.md` (~11.1K words, 47 dedup entries) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 7 judges + 7 sections + id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@99/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Independent gates caught real errors:** 3.5 judges caught a wrong-PMID note (17973296→18092346), a 503A regulatory inversion (KPV removed from Cat-2 ~Apr 2026, not "in Cat-2"), and a practitioner-citation defect (mis-dated Moore source + an unsupported "KPV+BPC-157" pairing that the source actually makes for TB-500). E-judge independently confirmed ZERO human studies AND caught+rejected a hallucinated "pilot trial." **7.5 risk-floor HALTed** on the experimental-tier third-party-marker rule → resolved honestly by naming objective assays (hs-CRP/calprotectin/CBC-CMP), NOT by fabricating a KPV-specific biomarker. Zero fabrications.

### CLAIMED (asserted this session — backed by `.provenance/`, re-checkable)
- ENTIRELY preclinical; **zero human studies of any design** (registry + literature null); Pawar 2017 is ex-vivo skin permeation, not a trial. KPV≠KdPT (Lys-D-Pro-Thr); neither has human trials.
- Mechanism: melanocortin-receptor-INDEPENDENT intracellular NF-κB inhibition; gut uptake via PepT1 (PepT1-KO abolishes benefit); importin-α3/p65 step is single-lab.
- Strongest data = rodent colitis (direction replicated ≥4 labs; magnitudes ~75% single-lab Merlin/GSU). Native-KPV antimicrobial contested (Cutuli positive single-lineage vs Songok null). Acne/gout efficacy = KdPT/(CKPV)₂ analogues, not monomer.
- FDA: 503A Cat-2 (2023) → removed ~Apr 2026 (nomination withdrawn), unlisted pending PCAC 23-24 Jul 2026; removal ≠ approval. WADA not individually named but prohibited under S0.
- Monitoring: no KPV-specific validated biomarker; objective monitoring = hs-CRP/fecal calprotectin/CBC-CMP (general assays).

### Meta-findings (skill_consolidator beads)
- FDA 503A Cat-2 removal (~Apr 2026) is a RECURRING retrieval miss (hit TB-500 + KPV) → bake "check the Apr-2026 503A Cat-2 removal status" into the safety/regulatory retrieval brief.
- 7.5 verifier over-read the third-party-marker rule (demanded a compound-SPECIFIC validated biomarker; the rule only needs a named OBJECTIVE assay) → clarify the verifier brief: a named objective lab assay (e.g. hs-CRP) satisfies it.

---

## 2026-06-20 — LL-37 (human cathelicidin) deep-pass (sweep entry 4)

### DONE (verified — mechanical evidence on disk)
- **LL-37 entry shipped:** `compounds/ll-37.md` + `library/peptides/ll-37/research-report.md` (~15K words, 80-entry bibliography) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 7 judges + 8 sections + id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@99/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Independent full-bibliography re-audit (operator-requested trust gate):** 4 independent agents re-checked all 80 entries against PubMed/Crossref → 61 VERIFIED, 15 legitimate NO-ID (regulatory/vendor/book/void), **0 fabrications**, 4 citation-precision defects found + fixed: [9] author Pahar→Radic/Muller, [32] first-author Wang→Lu, [47] PMID 31170213→31170191, [15] dead DOI. Independent integrity sweep: sound (no laundered numbers; Mahlapuu Phase IIb-negative + psoriasis-autoantigen + Kang log-kill spot-confirmed against source).

### CLAIMED (asserted this session — backed by `.provenance/` + independent re-audit)
- Genuinely DUAL-NATURED: antimicrobial/LPS-neutralizing/wound-healing/angiogenic AND a disease driver — psoriasis autoantigen + self-DNA/RNA→pDC→type-I-IFN (psoriasis/lupus/rosacea/atherosclerosis); context-dependent cancer (pro-tumor ovarian/lung/breast; anti-tumor colon/gastric).
- Human administration evidence = 4 small trials: Grönberg 2014 (positive Phase I/II VLU) → Mahlapuu 2021 HEAL (Phase IIb, PRIMARY ENDPOINT NEGATIVE) → Miranda 2023 DFU (granulation only) → melanoma n=4 dose-finding (skin toxicity). No Phase III, no approval. Endogenous-biomarker data is separate.
- FDA: 503A Cat-2 (2023) → removed ~Apr 2026 (FR 2026-07361), not approval; deferred off Jul-2026 PCAC to ~Feb 2027. WADA not individually named but prohibited under S0. Native short half-life; no established human PK figure.
- Monitoring: no LL-37-specific validated biomarker; objective via hs-CRP/inflammation markers. Dominant safety consideration = autoimmunity/psoriasis-flare risk (LL-37 is the autoantigen).

### Process note
This entry was finished under the operator's "Step 0" trust protocol after a long inefficiency failure: independent re-verification of the existing draft FIRST (passed: 0 fabrications), then the 3 remaining gates run via the actual skill machinery, then PR opened for OPERATOR review/merge (not auto-merged).

## 2026-06-20 — Ipamorelin (NNC 26-0161) deep-pass (sweep entry 5, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Ipamorelin entry shipped:** `compounds/ipamorelin.md` + `library/peptides/ipamorelin/research-report.md` (~10.2K words, 31-entry bibliography) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections w/ id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Ran under the EFFICIENT calibration** (after the LL-37 inefficiency): lean single-pass, 6 sections, judge bar 92, genuine-defects-only, recurring-error self-checks in retrieval briefs. Result: 5/6 sections passed first-pass; gates caught real defects in ONE round each — E's wrong 12-peptide Apr-2026 list (MK-677→PEG-MGF), a Section-D **Wikipedia citation IC-12 HALT** (removed, re-grounded to registry+RCT). Final independent full-bib audit: 18/18 identifier entries verified, **0 fabrications, 0 Wikipedia**, 1 misattributed PMID fixed (37139855→37066827); compound-entry consistency PASS (no invented PMID this time).

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- "First SELECTIVE GH secretagogue" — GH without ACTH/cortisol/prolactin — but ANIMAL-grounded (Raun 1998), not human-proven.
- Human evidence: acute PK/PD only (Gobburu 1999, IV); the sole efficacy program (postoperative ileus Phase 2, Beck 2014, n≈114, p=0.15) FAILED → Novo Nordisk/Helsinn discontinued development. No approval, no Phase 3, zero human efficacy for muscle/fat/anti-aging. Human PK IV-only (no human SC PK).
- ~80% Novo-Nordisk single-lineage concentration (≥70% flag, surfaced first-class). Bone = content/area not volumetric BMD; intermittent dosing did NOT raise IGF-1 in rats.
- FDA never approved; removed from 503A interim Cat-2 ~Sept 2024; PCAC voted AGAINST 503A bulks listing Oct 29 2024 (fluid-retention/hyperglycemia/CHF); NOT in the Apr-2026 FR 2026-07361 action. WADA S2.2 prohibited (named). Monitoring: IGF-1 (keep in age/sex range) + fasting glucose/HbA1c.
- Canonical FR-2026-07361 removed-12 (verified, for cross-entry consistency): BPC-157, TB-500, Epitalon, GHK-Cu, MOTS-c, DSIP/Emideltide, Dihexa, **PEG-MGF**, Melanotan-II, KPV, Semax, LL-37 — **MK-677 is NOT in it** (a prior-entry error to watch).

## 2026-06-20 — CJC-1295 (GRF(1-29) GHRH analogue) deep-pass (sweep entry 6, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **CJC-1295 entry shipped:** `compounds/cjc-1295.md` + `library/peptides/cjc-1295/research-report.md` (~9.7K words, 31 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Efficient calibration held** — 5/6 sections first-pass at bar 92; gates caught real defects in ONE round each: (a) §E HALT (88) on sourcing-tier — load-bearing regulatory facts rested on off-whitelist legal blogs → re-anchored to govinfo/fda primaries; (b) **4.25 ID-reconcile CAUGHT a genuine cross-section contradiction** — §D/§F wrongly said CJC-1295 "removed from Cat-2 ~Sept 2024" vs §E (NOT removed) → fixed D/F to defer to E.
- **Final independent full-bib audit: 16/16 identifier entries verified, 0 fabrications, 0 Wikipedia, 0 fixes — cleanest run of the sweep** (no PMID defect, unlike Ipamorelin). Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- **CJC-1295 = TWO molecules** constantly conflated: WITH DAC (maleimido-Lys→albumin-Cys34, t½ ~5.8–8.1 d; the Teichman 2006 PMID 16352683 Phase-1 PK/PD molecule) vs WITHOUT DAC = "Modified GRF 1-29" (~30 min; the ~100 mcg ipamorelin-stack partner). PK/trials/dosing NEVER cross-attributed.
- GHRH-receptor agonist (NOT ghrelin/GHSR — contrast ipamorelin); GH→hepatic IGF-1; DAC raises basal GH/IGF-1 over days.
- **No human efficacy, ever.** The only efficacy program (ConjuChem with-DAC Phase II HIV-lipodystrophy, NCT00267527) was TERMINATED July 2006 after a participant death; causation NOT established (on-scene MD: likely occult coronary disease). GH/IGF-1 elevation is a biomarker, not benefit. No approval, no Phase 3. no-DAC has zero human efficacy data.
- ConjuChem single-lineage ~100% of the 2 efficacy/PK preclinical primaries (Jette 2005 PMID 15817669 rat; Alba 2006 PMID 16822960 GHRHKO mouse) — concentration alert surfaced first-class.
- Regulatory: never approved; interim 503A Cat-2 (2023); PCAC voted AGAINST positive-list addition Dec 4 2024 (FR Doc 2024-24828); **NOT** among the 12 removed by FR Doc 2026-07361. WADA S2.2.4 prohibited (CJC-1295 named).
- **META-FINDING (cross-entry):** the independent judge verified the govinfo primary — **FR Doc 2026-07361 is the JULY-2026 PCAC MEETING NOTICE (7 peptides), not itself the "removal of 12" enumeration**; the removed-12 trace to FDA's parallel Category-2 action + secondaries. Prior entries (LL-37, KPV, etc.) framed 2026-07361 as "the removal action" — worth a consistency pass on those.

## 2026-06-20 — Tesamorelin (GHRH(1-44) analogue, Egrifta) deep-pass (sweep entry 7, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Tesamorelin entry shipped:** `compounds/tesamorelin.md` + `library/peptides/tesamorelin/research-report.md` (~11.1K words, 41 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Cleanest evidence base of the sweep** — 6/6 sections PASS first-pass at bar 92, NO section HALT. Gates still earned keep: 4.75 flagged a §D author-label error (PMID 28617838 first author is **Clemmons DR**, not "Stanley TL") → fixed before synthesis; 4.25 reconcile confirmed cross-section consistency (Egrifta SV vs WR setids correctly distinguished).
- **Final independent full-bib audit: 24/24 identifier entries verified, 0 fabrications, 0 Wikipedia, 0 fixes.** Compound-entry consistency PASS. (The suspicious 2026 Badran meta PMID 41545261 VERIFIED real.)

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- **The ONLY FDA-APPROVED GHRH analogue in the cluster** → deliberately tiered **evidence_tier B / risk_tier medium** (not C/experimental like the unapproved peptides). Demonstrates the pipeline tiers on evidence, not by rote.
- Structure: stabilized GHRH(1-44)NH2 + trans-3-hexenoyl N-cap (NOT the GRF(1-29) core of CJC-1295/sermorelin). GHRH-R agonist → pulsatile GH → IGF-1; effects REVERSE on discontinuation. Half-life ~8 min healthy / ~18–38 min HIV.
- **Approved efficacy is NARROW + real:** Falutz 2007 (NEJM PMID 18057338) + Falutz 2010 pooled (PMID 20554713) Phase 3 RCTs in HIV-lipodystrophy → ~15% VAT @26wk → ~18% @52wk; visceral-selective, weight-neutral; 2026 Badran meta (PMID 41545261) confirms. **INTEGRITY AXIS: that efficacy is HIV-lipodystrophy-VAT only.** NAFLD (Stanley 2019 Lancet HIV 31611038) + cognition (Baker 2012 Arch Neurol 22869065) = INVESTIGATIONAL (mostly HIV+). Bodybuilding/athletic/anti-aging/healthy-adult fat-loss = **ZERO human efficacy data** (off-label extrapolation).
- ~100% Theratechnologies single-sponsor concentration (academic-lineage MGH ~50%) — surfaced first-class.
- Regulatory: FDA approved 2010 (exact indication "reduction of excess abdominal fat in HIV-infected adult patients with lipodystrophy"); Egrifta SV 2019 / Egrifta WR 2025; EMA NOT approved (withdrawn, Ferrer); WADA S2.2.4 prohibited (tesamorelin named); ~$3000/mo brand. Contraindications (label): HPA-axis disruption, active malignancy, hypersensitivity incl. mannitol, pregnancy. Monitoring: IGF-1 + fasting glucose/HbA1c.
- Optional post-ship (non-blocking, no claim depends): refresh NCT02572323 status to "Completed"; note NCT07481734 "Mock Study" flag.

---

## 2026-06-20 — Sermorelin (GRF(1-29)NH2, brand Geref) deep-pass (sweep entry 8, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Sermorelin entry shipped:** `compounds/sermorelin.md` + `library/peptides/sermorelin/research-report.md` (~11.7K words, 35 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Efficient calibration held** — gates earned keep: §E HALT (90) on sourcing-tier (Apr-2026/503A facts rested on legal blogs → re-anchored to primary FR Doc 2026-07361 govinfo + 21 USC 353a statute; "Category 1" over-claim dropped/hedged to the component-of-approved-drug pathway). 4.75 json needed a structure fix (population_mismatch nested in ic_checks → lifted to top-level).
- **Final independent full-bib audit: 17/17 identifier entries verified, 0 fabrications, 0 Wikipedia, 0 fixes** (one optional §503A cascade-vs-alternatives wording nuance applied at ship). Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- GRF(1-29)NH2 = shortest fully bioactive GHRH fragment, the PROTOTYPE of the GRF(1-29) class (CJC-1295 no-DAC = "Mod GRF 1-29" is a stabilized sermorelin analogue). GHRH-R agonist → pulsatile GH → IGF-1; short half-life ~11-12 min (Geref label); DPP-IV degradation.
- **Genuine FDA-approval history → evidence_tier B** (above the unapproved C-tier peptides): Geref — diagnostic NDA 19-863 (1990) + pediatric idiopathic-GHD growth NDA 20-443 (1997); pivotal pediatric trial Thorner/Geref-Intl 1996 (PMID 8772599, n=110, height velocity 4.1→7.2 cm/yr). **WITHDRAWN ~2008 for COMMERCIAL reasons — FR 2013-04827 explicitly "not withdrawn for safety or effectiveness"** ("withdrawn" ≠ banned/unsafe).
- **INTEGRITY AXIS:** evidenced/approved use = pediatric-GHD + diagnostic; the popular ADULT anti-aging/body-comp/sleep use is OFF-LABEL, resting only on 4 small old aging-adult GHRH(1-29) studies (Corpas 1992 / Vittone 1997 / Khorram 1997 / Vitiello 2006 — biomarker-level GH/IGF-1, not robust clinical outcomes). Healthy-adult anti-aging/athletic/fat-loss = ZERO robust data.
- **Tesamorelin-miscredit guard held:** Baker 2012 (PMID 22869065) is tesamorelin and the GHRH-1,44 walk/stair/visceral-fat results are full-length GHRH — explicitly NOT credited to sermorelin (vendor blogs routinely conflate them). Single-lineage ~50% (below the 0.70 flag); folding in the miscredits would spuriously raise it.
- Regulatory: no marketed FDA product today but heavily §503A-COMPOUNDED via the component-of-a-formerly-approved-drug pathway (21 USC 353a(b)(1)(A); interim bulks-list category honestly hedged as not primary-confirmable); NOT among the Apr-2026 removed-12; FR Doc 2026-07361 = the July-2026 PCAC meeting notice (not "the removal action"). WADA S2.2.4 prohibited (named). Compounded convention ~100-500 mcg SC nightly ± GHRP/ipamorelin (Empower/Strive/Olympia data sheets); pediatric label 30 µg/kg/day kept distinct.

---

## 2026-06-20 — Hexarelin (GHRP, GHS-R1a + CD36) deep-pass (sweep entry 9, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Hexarelin entry shipped:** `compounds/hexarelin.md` + `library/peptides/hexarelin/research-report.md` (~11.5K words, 40 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Gates earned keep:** §E HALTed (91) on sourcing-tier (WADA naming rested on mirror sites with a "did not parse / indicative" hedge) → re-anchored to the **wada-ama.org primary 2026 List**, S2.2.4 verbatim (examorelin/hexarelin named). 4.75 json needed a structure fix (population_mismatch nested → lifted top-level). Phase-6 critique was zero-findings.
- **Final independent full-bib audit: 22/23 identifier entries verified, 0 fabrications, 0 Wikipedia; 1 fix** — citation [25] lead author Murphy N → **Knuppel A** (UK Biobank IGF-I/30-cancers, PMID 32709735) + 2 omitted PMIDs added ([7] 9589671, [9] 10404825). Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- Hexarelin is a **GHRP — a ghrelin-receptor (GHS-R1a) agonist + CD36 binder**, the SAME class as GHRP-6/GHRP-2/ipamorelin — **NOT a GHRH analogue** (contrast sermorelin/CJC-1295/tesamorelin). Synthetic hexapeptide (Deghenghi/Mediolanum; Turin/Ghigo research lineage). Short half-life; Ghigo 1994 human PK.
- **DEFINING LIMITATION = tachyphylaxis:** Rahim/O'Neill/Shalet 1998 (JCEM, PMID 9589671) — 1.5 µg/kg SC BID × 16 wk in healthy elderly (n=12) → GH AUC 19.1→10.5 µg/L·h (~45% decline), **IGF-1/IGFBP-3 UNCHANGED** (p=0.24/0.74), body-comp/BMD unchanged, reversible by wk-20. Acute GH spikes ≠ durable effect.
- **Less selective than ipamorelin:** meaningfully raises cortisol/ACTH (CRH-independent, AVP-mediated — Korbonits 1999) and prolactin.
- **CD36 cardiac line** (Bodart 2002 Circ Res; Broglio/Bisi): GH-independent cardioprotection, but mostly PRECLINICAL (rat I/R, perfused heart) — human = acute positive inotropy only; the diseased-heart (dilated-CMP) human study did NOT respond. INVESTIGATIONAL.
- **ABSENT:** body-composition/fat-loss/muscle, anti-aging/longevity, athletic performance, any Phase-3/approval — ZERO robust human data. Acute hexarelin did NOT alter glucose/insulin (unlike ghrelin); GH-axis metabolic risks flagged EXTRAPOLATED.
- Concentration audit: Turin/Ghigo first-author ~25% (below 0.70 flag), but Deghenghi/Mediolanum developer footprint ~50% + no cross-lab human replication of the cardiac signal — surfaced.
- Regulatory: never approved (Mediolanum Phase II discontinued); §503A NOT in the Apr-2026 removed-12, effectively unlisted/not-nominated (honest hedge); FR-2026-07361 = July-2026 PCAC notice; WADA S2.2.4 prohibited at all times (examorelin/hexarelin named, primary-anchored). No compounding data sheet found; gray-market only.

---

## 2026-06-20 — MK-677 (Ibutamoren; Merck MK-0677) deep-pass (sweep entry 10, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **MK-677 entry shipped:** `compounds/mk-677.md` + `library/peptides/mk-677/research-report.md` (~11.3K words, 38 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Gates earned keep:** §F HALTed (91) on a "~24h half-life" misstatement → fixed (molecular ~4-6 h vs PD ~24 h). 4.75 concentration_audit threshold_triggered=TRUE (Merck 6/8=75%). Phase-6 critique near-clean (1 cosmetic age-range nit).
- **Final independent full-bib audit: 16/16 identifier entries verified, 0 fabrications, 0 first-author mismatches, 0 Wikipedia — cleanest GH-secretagogue run** (the misattribution failure mode absent); 2 optional epub-vs-print year nits tidied ([5] Sigalos 2018, [6] Abizaid 2020). Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- MK-677 is an **ORAL, NON-PEPTIDIC SMALL MOLECULE** ghrelin-receptor (GHS-R1a) agonist (Merck MK-0677/L-163,191; spiroindane; Patchett/Nargund PNAS 1995; GHS-R1a cloned Howard 1996 Science) — NOT a peptide, NOT a GHRH analogue. Molecular elimination t½ ~4-6 h (~4.7 h); the "~24 h" figure is the PHARMACODYNAMIC GH/IGF-1 duration (don't conflate). Oral once-daily is the defining differentiator from the injectable peptide secretagogues.
- **Most-studied GH secretagogue in long-term human RCTs**, but biomarker-only: Nass 2008 (Ann Intern Med, 2-yr healthy elderly, PMID 18981485) — IGF-1 → young-adult range + fat-free mass **+1.1 kg**, but **NO strength/function** improvement + insulin sensitivity ↓; Chapman 1996 (JCEM). **biomarker/lean-mass ↑ ≠ functional benefit.**
- **Two major disease programs FAILED despite raising IGF-1:** Alzheimer's Phase 2b/3 (Sevigny 2008, Neurology, PMID 19015485, n=563 — IGF-1 +72.9% but no cognitive benefit on any endpoint); hip-fracture functional recovery (Adunsky 2011, Arch Gerontol Geriatr, PMID 21067829 — primary missed AND terminated early for a **CHF safety signal ~6.5% vs 1.7%**). Bodybuilding/athletic efficacy = ABSENT (no RCT).
- **DOMINANT safety issue = METABOLIC:** raised fasting glucose, reduced insulin sensitivity, ↑HbA1c (Nass +0.3 mmol/L; Chapman 5.4→6.8) — the key risk for diabetics/pre-diabetics; plus appetite ↑, edema, modest cortisol, lethargy; + the CHF signal. Malignancy/IGF-1 flagged EXTRAPOLATED class risk.
- Concentration audit: **Merck 6/8 (75%) — FLAGGED ≥0.70**; no Merck-independent disease-endpoint trial.
- Regulatory: never approved (Merck discontinued; LUM-201 successor still investigational); **NOT a lawful dietary ingredient** — FDA Dec-2025 warning letters (Prime Sports Nutrition; Agebox/iKids-Growth); as a SMALL MOLECULE it is **NOT** part of the §503A peptide action / FR-2026-07361 (distinction stated, not conflated); WADA S2 prohibited at all times (ibutamoren named). No compounding data sheet (not on §503A); oral gray-market "research chemical" ~10-25 mg/day.

### NEXT (reserved, my/primary lane): **Semaglutide** (sweep entry 11 — the GLP-1 metabolic class begins; FDA-APPROVED [Ozempic/Wegovy], so expect evidence_tier A/B). **Push branch as `research/semaglutide-deep-pass-gated`** (a stale predecessor `research/semaglutide-deep-pass` exists). Then Tirzepatide (`-gated`) → Retatrutide (`-gated`) → AOD-9604 → Selank. (Bottom-13 [MOTS-c…Semax] owned by `feature/wiki-peptides`.)

---

## Prep checklist — run BEFORE the next peptide research session
1. `cd ~/Documents/Projects/a+research && git checkout main && git pull --ff-only`
   (gets #148/#150/#151 — the operational skill).
2. Pre-flight the skill's runtime (now enforced by SKILL.md "Pre-Flight Dependencies"):
   - `[ -e ~/.claude/skills/deep-research/SKILL.md ]` — the wrapped skill resolves
     (a dangling symlink fails this and HALTs `deep-research-missing`).
   - `python3 -c 'import jsonschema'` — else `python3 -m pip install jsonschema`.
   - Tavily + basic-memory MCP connected? If **yes**, run as-is. If **no**, the skill is
     still runnable with WebSearch/WebFetch + filesystem-Write to the vault (note the
     substitution in the run log).
3. Read `meta/goals.md` + `meta/current-state.md` (goal anchor + current biomarkers) and
   [[_triage]] (the reserved target + scoring rubric).
4. Run the reserved **Healing/soft-tissue triage pass** (standard mode batches the four).
   On each completion, move the peptide to the triage "Done"/"Excluded" table and append a
   DONE/CLAIMED entry here.
