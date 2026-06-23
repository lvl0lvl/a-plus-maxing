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
- FDA removed from interim §503A Cat-2 ~Apr 2026 (parallel FDA Cat-2 action, NOT approval; FR Doc 2026-07361 = the July-2026 PCAC meeting notice, not the removal action); WADA S2.3 prohibited; evidence_tier C / risk_tier experimental.
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
- FDA: 503A Cat-2 (2023) → removed ~Apr 2026 (parallel FDA Cat-2 action, not approval; FR Doc 2026-07361 = the July-2026 PCAC meeting notice, not the removal action); deferred off Jul-2026 PCAC to ~Feb 2027. WADA not individually named but prohibited under S0. Native short half-life; no established human PK figure.
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
- FDA never approved; removed from 503A interim Cat-2 ~Sept 2024; PCAC voted AGAINST 503A bulks listing Oct 29 2024 (fluid-retention/hyperglycemia/CHF); NOT among the Apr-2026 Cat-2 removed-12 (and not among the 7 in FR Doc 2026-07361, the July-2026 PCAC meeting notice). WADA S2.2 prohibited (named). Monitoring: IGF-1 (keep in age/sex range) + fasting glucose/HbA1c.
- Canonical interim §503A Cat-2 removed-12 (verified, for cross-entry consistency) — this is the PARALLEL FDA Cat-2 action, NOT FR Doc 2026-07361 (which is the July-2026 PCAC meeting notice listing 7 peptides under review): BPC-157, TB-500, Epitalon, GHK-Cu, MOTS-c, DSIP/Emideltide, Dihexa, **PEG-MGF**, Melanotan-II, KPV, Semax, LL-37 — **MK-677 is NOT in it** (a prior-entry error to watch). [corrected 2026-06-20, fix/fr-2026-07361-consistency: heading previously mis-attributed the removed-12 to FR 2026-07361.]

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
- Regulatory: never approved; interim 503A Cat-2 (2023); PCAC voted AGAINST positive-list addition Dec 4 2024 (FR Doc 2024-24828); **NOT** among the 12 removed in the parallel FDA Cat-2 action (and not among the 7 in FR Doc 2026-07361, the July-2026 PCAC meeting notice — see META-FINDING below). WADA S2.2.4 prohibited (CJC-1295 named).
- **META-FINDING (cross-entry):** the independent judge verified the govinfo primary — **FR Doc 2026-07361 is the JULY-2026 PCAC MEETING NOTICE (7 peptides), not itself the "removal of 12" enumeration**; the removed-12 trace to FDA's parallel Category-2 action + secondaries. Prior entries (LL-37, KPV, etc.) framed 2026-07361 as "the removal action" — worth a consistency pass on those. **RESOLVED 2026-06-20: consistency pass applied across entries (fix/fr-2026-07361-consistency)** — BPC-157 + TB-500 (_triage.md), TB-500 + LL-37 + Ipamorelin + this CJC-1295 entry + the "Canonical removed-12" heading (_research-log.md), and the BPC-157 Cat-2 record (meta/contradictions.md) all re-framed so 2026-07361 = the July-2026 PCAC meeting notice (7 peptides) and the removal-of-12 = the parallel FDA Cat-2 action.

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
- **Efficient calibration held** — gates earned keep: §E HALT (90) on sourcing-tier (Apr-2026/503A facts rested on legal blogs → re-anchored to primaries: the FDA Cat-2 page (the parallel removal action) + FR Doc 2026-07361 govinfo (the July-2026 PCAC meeting notice) + 21 USC 353a statute; "Category 1" over-claim dropped/hedged to the component-of-approved-drug pathway). 4.75 json needed a structure fix (population_mismatch nested in ic_checks → lifted to top-level).
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

---

## 2026-06-20 — Semaglutide (GLP-1 receptor agonist; Ozempic/Wegovy/Rybelsus) deep-pass (sweep entry 11, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Semaglutide entry shipped:** `compounds/semaglutide.md` + `library/peptides/semaglutide/research-report.md` (~10.6K words, 48 unified citations + crosswalk) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact.
- **Gates earned keep:** §E HALTed (89) — the elevated "2026 WADA Monitoring Program" claim rested on a non-authoritative secondary → downgraded to reported, with the load-bearing "NOT on the Prohibited List" anchored to the USADA list. 4.75 concentration_audit threshold_triggered=TRUE (Novo ~76% — expected for an approved drug, surfaced honestly). Phase-6 critique near-clean (2 cosmetic minors).
- **Final independent full-bib audit: 19/19 identifier entries verified, 0 fabrications, 0 first-author mismatches, 0 Wikipedia** (the misattribution failure mode absent). Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- **FIRST A-tier entry of the sweep.** Acylated long-acting GLP-1(7-37) analogue (Aib8/Arg34 + C18 diacid → albumin binding → ~1-wk t½); GLP-1 receptor agonist; SC-weekly (Ozempic/Wegovy) + oral-daily+SNAC (Rybelsus); Novo Nordisk. Distinct from tirzepatide (dual GIP/GLP-1).
- **REAL benefits (population-annotated):** glycemic (SUSTAIN ~1.5-1.8% HbA1c; PIONEER oral); **~14.9% weight loss in NON-DIABETIC obesity** (STEP-1 Wilding 2021 PMID 33567185) vs **~9.6% in T2D** (STEP-2 — magnitude is population-dependent); **CV MACE −20%** in overweight/obese WITHOUT diabetes + CVD (SELECT Lincoff 2023 PMID 37952131, HR 0.80); **renal** benefit (FLOW Perkovic 2024).
- **REAL caveats (not buried):** GI AEs (nausea/vomiting/diarrhea) dominate + are the main discontinuation driver; **~two-thirds weight REGAIN on discontinuation** (STEP-1 extension); **lean/muscle-mass loss** (~39-45% of weight lost); gallbladder; pancreatitis; gastroparesis/peri-op aspiration; SUSTAIN-6 retinopathy signal; the **thyroid C-cell/MTC BOXED WARNING is RODENT-based and NOT demonstrated in humans** (human meta null); **suicidality investigated and NOT confirmed** (Wang 2024 RWE points the other way).
- **Integrity:** SURMOUNT-OSA is **tirzepatide, NOT semaglutide** — OSA not credited to semaglutide. ~76% of pivotal primaries are Novo-sponsored (single-sponsor caveat, partially offset by adjudicated endpoints + regulatory review).
- Regulatory: FDA-approved Ozempic (T2D, Dec 2017), Rybelsus (oral T2D, Sept 2019), Wegovy (obesity, June 2021; +CV-risk Mar 2024) — obesity vs T2D are SEPARATE approvals/doses; EMA approved. The 2022-24 shortage enabled 503A/503B compounded semaglutide; FDA resolved the shortage Feb 2025 (compounding wind-down) + counterfeit/salt-form warnings. WADA: **NOT prohibited** (reportedly on the 2026 Monitoring Program — secondary-reported; the final audit later primary-confirmed the Monitoring-Program status via German NADO + EMJ).

---

## 2026-06-20 — Tirzepatide (dual GIP/GLP-1 agonist; Mounjaro/Zepbound) deep-pass (sweep entry 12, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Tirzepatide entry shipped:** `compounds/tirzepatide.md` + `library/peptides/tirzepatide/research-report.md` (~9.8K words, 42 unified citations) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6@iter2/7.5/8.5); verify-chain intact.
- **Gates earned keep:** all 6 judges PASS first-pass (cleanest A-tier judging); but the **§6 critique HALTed (major) on a real citation-integrity defect** — the synthesis built a unified bibliography + crosswalk but left the inline body tokens SECTION-LOCAL (collision: [1] = Sun cryo-EM in §1 vs SURMOUNT-1 in §2 → the ~20.9% figure resolved to the WRONG paper; danglers [16]/[22]/etc). Fixed via a mechanical renumber pass (`-trial`/`-osa` suffix split for the 2 collided numbers); re-critique PASS. **This is the recurring section-local↔unified numbering meta-finding — the synthesis prompt should mandate the renumber, not just the crosswalk.**
- **Final independent full-bib audit: 23/23 identifier entries verified, 0 fabrications, 0 first-author mismatches, 0 Wikipedia; citation integrity clean (42 tokens 1:1, 4 spot-checks correct).** Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- Dual **GIP + GLP-1 receptor agonist** ("twincretin"; single 39-aa peptide, C20 diacid, ~5-day t½, once-weekly SC; Eli Lilly) — mechanistically DISTINCT from semaglutide (GLP-1-only).
- **REAL benefits (population-annotated):** SURPASS (T2D HbA1c); **SURPASS-2 (Frías 2021 PMID 34170647) head-to-head BEAT semaglutide 1 mg**; **~20.9% weight loss in NON-DIABETIC obesity** (SURMOUNT-1 Jastreboff 2022 PMID 35658024) vs ~14.7% T2D (SURMOUNT-2); **OSA = APPROVED indication** (SURMOUNT-OSA Malhotra 2024 PMID 38912654 — the first FDA-approved drug for OSA); SURPASS-CVOT (Nicholls 2025) non-inferior to dulaglutide but **NOT superior** (no CV-reduction label).
- **REAL caveats:** GI AEs dominant (discontinuation driver); **~14% weight REGAIN on discontinuation** (SURMOUNT-4 Aronne 2024 PMID 38078870); **lean-mass loss** (roughly proportional, ~25% of weight lost); gallbladder; pancreatitis; gastroparesis/peri-op aspiration; the **thyroid C-cell/MTC BOXED WARNING is RODENT-based, NOT human-demonstrated**. HFpEF (SUMMIT) + MASH (SYNERGY-NASH) + SURMOUNT-MMO = INVESTIGATIONAL.
- ~95% of pivotal primaries are Eli-Lilly-sponsored (single-sponsor caveat, surfaced).
- Regulatory: FDA-approved Mounjaro (T2D, May 2022), Zepbound (obesity, Nov 2023), Zepbound-OSA (Dec 2024); EMA approved. The 2022-24 shortage enabled 503A/503B compounded tirzepatide; FDA resolved the shortage 2024 (before semaglutide) + 2025 wind-down + OFA litigation + counterfeit/salt-form warnings. WADA: **NOT prohibited** (on the 2026 Monitoring Program — NADA-anchored, WADA-verbatim-verified).

---

## 2026-06-20 — Retatrutide (LY3437943; triple GIP/GLP-1/glucagon agonist) deep-pass (sweep entry 13, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **Retatrutide entry shipped:** `compounds/retatrutide.md` + `library/peptides/retatrutide/research-report.md` (~10.6K words, 22 unified citations) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact. All 6 judges PASS first-pass; §6 critique zero-findings (citations renumbered to the unified scheme FIRST-PASS — the tirzepatide lesson applied in the synthesis brief).
- **Final independent full-bib audit: 11/11 load-bearing identifier entries verified, 0 fabrications, 0 first-author mismatches, 0 Wikipedia.** Compound-entry consistency PASS.

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- **TRIPLE GIP + GLP-1 + GLUCAGON receptor agonist** (LY3437943, Eli Lilly; single acylated peptide, ~6-day t½, once-weekly SC) — the glucagon arm (energy expenditure + hepatic fat) is the differentiator vs tirzepatide (dual) and semaglutide (GLP-1-only).
- **CENTRAL FACT: INVESTIGATIONAL — NOT approved anywhere.** The LARGEST weight-loss signal of any incretin agent yet (**~24.2% at 48 wk/12 mg, Phase 2**, Jastreboff 2023 NEJM PMID 37366315, non-diabetic obesity) — but **Phase-2 only**; Rosenstock 2023 Lancet (T2D Phase 2); Sanyal 2024 Nat Med PMID 38858523 (MASH liver-fat −86%, Phase-2a imaging surrogate). **Phase 3 (TRIUMPH) ongoing with only sponsor TOPLINE PRESS RELEASES** (TRIUMPH-1 ~28%, TRIUMPH-4) — quarantined as not-peer-reviewed/not-verified, NOT treated as established efficacy.
- **Safety (Phase-2 only):** GI dominant (dose-dependent, discontinuation driver); the glucagon-component **dose-dependent heart-rate increase** (peaks wk24, grounded in the Tier-1 NEJM trial — a vendor-sourced ~bpm figure was DROPPED at §5); retatrutide-specific **cutaneous hyperesthesia ~7% vs 1%**; transient **eGFR** dip→recovery; NO long-term/CV/human-thyroid data (C-cell = class-extrapolated).
- ~100% Eli-Lilly single-sponsor (no independent replication, surfaced). FDA Fast Track for retatrutide = UNVERIFIED (not asserted; only tirzepatide had it).
- Regulatory: NOT approved (investigational); FDA gray-market caution (cannot be compounded / not a component of an approved drug / not safe-and-effective / warning letters). **Gray-market retatrutide is especially premature** (no approved product, China-sourced research-chem with documented sterility-test failures). WADA: **NOT prohibited** (2026 Prohibited List S4.4 has no GLP-1/glucagon agonists; 2026 Monitoring tracks only "Markers of semaglutide and tirzepatide" — retatrutide not individually named; verified by directly parsing the WADA PDFs).

---

## 2026-06-20 — AOD-9604 (hGH(176-191) lipolytic fragment) deep-pass (sweep entry 14, primary-session lane)

### DONE (verified — mechanical evidence on disk)
- **AOD-9604 entry shipped:** `compounds/aod-9604.md` + `library/peptides/aod-9604/research-report.md` (~11.1K words, 32 unified citations) + practitioner-layer + non-english-layer + full `.provenance/` (7 attested gate JSONs + 6 judges + 7 sections incl. id-reconcile).
- **All 7 gates attested PASS** (2.75/3.5@92/4.25/4.75/6/7.5/8.5); verify-chain intact. All 6 judges PASS first-pass; §6 critique PASS (2 minor); citations renumbered to unified first-pass (a dangling [6] caught + fixed at synthesis).
- **Final independent full-bib audit: 6/6 load-bearing identifier entries verified, 0 fabrications, 0 first-author mismatches, 0 Wikipedia.** Compound-entry consistency PASS. (Applied the audit's optional §6.3-vs-§8.2 §503A-timeline reconciliation polish.)

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- AOD-9604 = synthetic **C-terminal fragment of human GH, hGH(176-191)/Tyr-hGH(177-191)** ("lipolytic fragment"; Metabolic Pharmaceuticals/Monash/Ng). Claimed lipolysis + anti-lipogenesis WITHOUT GH-receptor binding or IGF-1 elevation — **verified at receptor/IGF-1/glucose levels** (the GH-axis-sparing differentiator vs full GH and the GH secretagogues). Very short t½ (~4 min).
- **THE CENTRAL FACT: pivotal human efficacy FAILED.** The Phase-2b obesity RCT (~536 pts, 24 wk, oral 0.25/0.5/1 mg) did NOT beat placebo → obesity development discontinued ~2007. The Herd 2005 12-wk study (conference abstract, modest unconfirmed signal) was not confirmed. All robust lipolysis is PRECLINICAL (Ng 2000 Zucker rats PMID 11146367; Heffernan 2001 mice PMID 11673763). **No proven human fat-loss efficacy.** Never registered on ClinicalTrials.gov.
- **Safety:** well-tolerated/placebo-indistinguishable in 6 RCTs (~893 adults); **failed on EFFICACY, not safety**; no IGF-1 rise, no glucose/insulin impairment (verified). BUT short-term-only (≤24 wk), NO published human SC-route data (the gray-market route), FDA flagged immunogenicity/aggregation/impurity for uncharacterized injectable.
- **OA/cartilage pivot = PRECLINICAL-only** (Kwon&Park 2015 rabbit PMID 26275694 + patent; ZERO registered human OA trials). **The "Paradigm Phase-II knee-OA" claim is a MOLECULE CONFLATION — that program is pentosan polysulfate (iPPS/Zilosul), NOT AOD-9604 — correctly excluded.**
- ~100% Metabolic Pharmaceuticals/Monash single-lineage (no sponsor-independent replication).
- Regulatory: never approved as a drug (FDA/TGA/EMA); **self-affirmed GRAS ≠ FDA approval and NOT a lawful US dietary ingredient** (DSHEA drug-exclusion); TGA Schedule-4; NOT in the Apr-2026 §503A removed-12 (interim Cat-2 Sept 2023 → removed ~Sep 2024 by nominator withdrawal; never Cat-1 → not lawfully compoundable). **WADA: PROHIBITED** (S0 non-approved-substance [clarified to ASADA 2013-04-22] + S2 GH-fragment scope; the Essendon AFL saga, CAS 2016). Gray-market ~300 mcg SC/day convention (trial doses were oral ~1 mg — trial-derived, not a label).

---

## 2026-06-20 — Selank (TP-7, Tuftsin-analogue heptapeptide) deep-pass (sweep entry 15, primary-session lane — **PRIMARY LANE COMPLETE**)

### DONE (verified — mechanical evidence on disk)
- **Selank entry shipped:** `compounds/selank.md` + `library/peptides/selank/research-report.md` (~75K file, full bibliography) + practitioner-layer + non-english-layer + full `.provenance/`.
- **All 7 gates attested PASS** (2.75→8.5, chain intact).
- **Independent full-bib audit: 21/21 PMIDs verified, 0 fabrications, 0 fixes.** Compound-entry consistency PASS.
- **This is the LAST entry of the primary lane — all top-12/primary-lane peptides are now done.** (Bottom-13 [MOTS-c…Semax] remain owned by `feature/wiki-peptides`.)

### CLAIMED (asserted this session — backed by `.provenance/` + independent audit)
- Selank = synthetic **Tuftsin-analogue heptapeptide Thr-Lys-Pro-Arg-Pro-Gly-Pro** (IMG RAS / Zakusov Institute, Russia) — a stabilized tuftsin analogue. **Russia-REGISTERED intranasal anxiolytic** (reg. no. **ЛСР-003338/09**, 0.15% solution, GAD/neurasthenia) but **NOT FDA/EMA-approved**.
- Mechanism: **enkephalinase inhibition** (slows enkephalin degradation) + **BDNF/monoamine/GABAergic modulation** + **Tuftsin-lineage immunomodulation** (incl. an antiviral/IFN signal).
- **INTEGRITY AXIS:** the headline "anxiolysis comparable to a benzodiazepine but WITHOUT sedation, amnesia, dependence, or withdrawal" is a **Russian-clinical claim, honestly scoped** — backed by 4 small (n≈60–70) benzodiazepine-comparator (NOT placebo-controlled) Russian-language trials, **NOT Western-validated**, with **no dedicated dependence trial**. Western counterweight cited first-class (**Doyno & White 2021** flags class-level abuse/dependence as unsettled).
- Evidence is **predominantly Russian-language** and **~100% single-lineage** (IMG RAS / Zakusov / Serbsky-Korsakov network; ~7/7 admissible primaries) — internally consistent but the opposite of independent corroboration; limited independent Western replication surfaced first-class.
- Regulatory: outside Russia an unapproved gray-market "research chemical"; **§503A Selank-acetate/TP-7 was Category-2, removed Sept 27 2024 by nomination withdrawal → PCAC, NEVER Category-1 → not lawfully compoundable**; WADA **NOT prohibited** (not on the 2026 List; holds a governmental approval so not swept under S0). evidence_tier **C** / risk_tier **experimental**.
- **Kept DISTINCT from Semax and from N-Acetyl-Selank-Amidate** throughout. NOTE: **Semax is the OTHER session's (bottom-13) — NOT touched.** (Bottom-13 [MOTS-c…Semax] owned by `feature/wiki-peptides`.)

---

## 2026-06-20 — PARALLEL SESSION SPLIT (operator directive) — `feature/wiki-peptides` claims the BOTTOM 13

**Operator directive (2026-06-20):** the deep-pass sweep is split across TWO sessions to accelerate (the primary peptide-library session was behind — 4 shipped + Ipamorelin in flight). A SECOND session (`feature/wiki-peptides`, the wiki-research session that just shipped the Wave-1 biomarker clusters via PR #180) takes the **bottom half** of the sweep, working **bottom-up**.

### CLAIMED by `feature/wiki-peptides` (bottom 13 — do NOT deep-pass these in the primary session)
Working bottom-up from MOTS-c:
**MOTS-c → SS-31 → Humanin → FOXO4-DRI → Epitalon → Thymosin-α1 → Kisspeptin-10 → Melanotan-II → PT-141 → N-Acetyl-Selank-Amidate → Dihexa → Cerebrolysin → Semax.**

### Retained by the PRIMARY session (top 12 — `feature/wiki-peptides` will NOT touch these)
**LL-37 → Ipamorelin (IN PROGRESS) → CJC-1295 → Tesamorelin → Sermorelin → Hexarelin → MK-677 → Semaglutide → Tirzepatide → Retatrutide → AOD-9604 → Selank.**

Coordination: each session ships its claimed entries via its own PR cycle (deep mode, all 7 gates). The shared `_triage.md` + `_research-log.md` union-merge (same pattern as the biomarker `vault/meta/log.md` resolution in PR #180). On completion this session appends a DONE/CLAIMED entry per peptide below.

**This session's progress:** claimed 2026-06-20.

### DONE (verified — mechanical evidence on disk)
- **MOTS-c shipped** (2026-06-20, sweep entry 1 of this session's bottom-13): `compounds/mots-c.md` + `library/peptides/mots-c/{research-report,practitioner-layer,non-english-layer}.md` (~10K-word report, 35 dedup sources) + full `design/.mots-c-design-work/` provenance (7 attested gate JSONs 2.75→8.5 + 5 judges + 5 sections + id-reconcile). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest-lint + whole-vault wiki-lint clean.**

### CLAIMED (asserted this session — backed by `.provenance/`, re-checkable, not independently re-audited)
- Efficacy evidence ~entirely MOUSE (exogenous, IP, male, n≤10); human data OBSERVATIONAL biomarker only; NO human trial of native MOTS-c (one Phase-2a recruiting, NCT07505745).
- Foundational primary literature **100% single-group** (Cohen/Lee USC, P1–P4 through 2021); first independent rodent replication 2023+ (Tang/Yang/Pham); CohBar COI throughout.
- Only human clinical program = **CB4211** (a DIFFERENT stabilized analog ≠ native; company-press-release only; formulation unsuitable; discontinued 2023 on CohBar dissolution).
- **WADA-prohibited** (S4.4 AMPK-activator metabolic-modulator class; name-vs-class unconfirmed from inaccessible primary PDF — honestly disclosed). FDA-unapproved, not 503A-compoundable (FR 2026-07361 = PCAC nomination notice; eval pending Jul 23-24 2026).
- Gate catches: regulatory claims re-grounded off vendor blogs onto the FDA Federal Register; CB4211/contamination numbers from dead press-releases stripped/verified; concentration audit surfaced the 100% single-group share first-class; aging-us.com whitelisted (tier 2).

### DONE (verified — mechanical evidence on disk)
- **SS-31 / Elamipretide shipped** (2026-06-20, bottom-13 sweep entry 2): `compounds/ss-31.md` + `library/peptides/ss-31/{research-report,practitioner-layer,non-english-layer}.md` (~10.4K-word report, 40 dedup sources) + full `design/.ss-31-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 5 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: FDA-approved for Barth ONLY (Forzinity, Oct 30 2025, on uncontrolled OLE knee-strength) while every controlled trial missed its primary; ≥90% single-sponsor (Stealth) + Szeto/Cornell COI; strong-preclinical/failed-clinical translation gap; 5 Chinese-language primaries. The 4.25 gate caught + discarded a subagent that falsified a PASS verdict (integrity layer working).

- **Humanin shipped** (2026-06-20, bottom-13 sweep entry 3): `compounds/humanin.md` + `library/peptides/humanin/{research-report,practitioner-layer,non-english-layer}.md` (~12K-word report, 41 dedup sources) + full `design/.humanin-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 6 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: first-discovered MDP (MT-RNR2/16S); human evidence biomarker-only, NO administration trial (causal direction unresolved — possible stress-marker); efficacy mostly the S14G-HNG analog (~1000× native); anti-apoptotic→PRO-TUMOR contraindication (TNBC + GBM); FDA-unapproved/no-503A/WADA-S0; concentration ~59% (below the 70% flag — genuine independent breadth, unlike MOTS-c/SS-31); 8 non-English primaries. Synthesis expanded 8.1K→12K to hold the deep floor.

- **FOXO4-DRI shipped** (2026-06-20, bottom-13 sweep entry 4): `compounds/foxo4-dri.md` + `library/peptides/foxo4-dri/{research-report,practitioner-layer,non-english-layer}.md` (~11.3K-word report, 28 dedup sources) + full `design/.foxo4-dri-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 6 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: senolytic D-retro-inverso FOXO4–p53 disruptor; ALL preclinical, ZERO human data (evidence_tier D — weaker than the C-tier MDPs); behind D+Q/fisetin in translation; on-target p53/cardiotox + the Born-2023 *Circulation* pulmonary-hypertension ADVERSE finding; concentration ~12.5% (well below flag, multi-continental independence); D-chirality unverifiable by HPLC CoA. The 4.25 needed a one-pass shared-citation canonicalization (heaviest reconciliation of the 4 peptides); the Phase-6 critique surfaced the Born-2023 adverse result.

- **Epitalon shipped** (2026-06-21, bottom-13 sweep entry 5): `compounds/epitalon.md` + `library/peptides/epitalon/{research-report,practitioner-layer,non-english-layer}.md` (~10.8K-word report, 23 dedup sources) + full `design/.epitalon-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 6 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: AEDG tetrapeptide (Khavinson); telomerase claim in-vitro-only (Khavinson 2003 + independent Brunel 2025, ALT-in-cancer); human longevity claims open-label single-group on crude Epithalamin EXTRACT ≠ synthetic peptide; ≥80% Khavinson concentration (above flag); telomerase→oncogenic tension; cytomedine paradigm not Western-accepted; evidence_tier D. The SWEEP'S HEAVIEST gate round (all 5 judges HALTed iter-1 on weak-secondary-sourcing → re-grounded on Federal Register/primary papers, removed Wikipedia + aggregators, canonicalized 11 shared cites); 10 Russian-language primaries (the Russian corpus is its primary record).

- **Thymosin-α1 shipped** (2026-06-21, bottom-13 sweep entry 6): `compounds/thymosin-alpha-1.md` + `library/peptides/thymosin-alpha-1/{research-report,practitioner-layer,non-english-layer}.md` (~10.5K-word report, 39 dedup sources) + full `design/.thymosin-alpha-1-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 6 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: the bottom-13's HIGHEST-evidence + only non-experimental entry — evidence_tier B / risk_tier MEDIUM; approved in >35 countries (Zadaxin), genuine RCT HBV/vaccine-adjuvant evidence, exceptional approved-drug safety; the sepsis hype DEFLATED by the 2025 TESTS phase-3 null (HR 0.99); NOT FDA-approved-US (503A off-limits post-Dec-2024 PCAC); concentration ~15-20% (genuinely replicated, ≥8 groups); anti-aging use = extrapolation; Tα1≠Tβ4 hazard. 18 non-English primaries (ZH/IT/RU). All 5 judges HALTed iter-1 on citation-hygiene (content 90-98); the 4.25 caught the ETASS-vs-TESTS sponsor conflation.

- **Kisspeptin-10 shipped** (2026-06-21, bottom-13 sweep entry 7): `compounds/kisspeptin-10.md` + `library/peptides/kisspeptin-10/{research-report,practitioner-layer,non-english-layer}.md` (~10.6K-word report, 33 dedup sources) + full `design/.kisspeptin-10-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 6 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: evidence_tier C / risk_tier experimental; KISS1R/GPR54→GnRH→LH/FSH master HPG regulator; KP-10's OWN human data THIN (3 studies n≤10) — the HPG/IVF evidence is KP-54 (distinct, ~28min vs ~4min t½), efficacy extrapolated; sexual/HSDD = 5 RCTs but ALL single-center (Comninos/Dhillo Imperial), surrogate endpoints; bolus-stimulates/continuous-DESENSITIZES (tachyphylaxis day-14 → HPG-suppression risk); WADA S2.2.1 EXPLICITLY prohibited; FDA-unapproved (503A closed Oct-2024 PCAC 11-0); concentration ~50% Imperial broad-field (below flag) but sexual sub-literature ~100% Imperial; PT-141/Vyleesi is the approved HSDD drug NOT KP-10. 18 non-English entries (JP/ZH/RU). All 5 judges HALTed iter-1 on citation-attribution + the evidence-ceiling; the 4.25 caught a copy-pasted wrong author list (PMID 24517142) + a transposed JAMA article number.

- **Melanotan-II shipped** (2026-06-21, bottom-13 sweep entry 8): `compounds/melanotan-ii.md` + `library/peptides/melanotan-ii/{research-report,practitioner-layer,non-english-layer}.md` (~10.1K-word report, 40 dedup sources) + full `design/.melanotan-ii-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 5 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: evidence_tier C / risk_tier experimental; non-selective melanocortin agonist (MC1R tan/MC4R erectile); real-but-single-site human evidence (Dorr tanning pilot + 3 Wessells erectile crossover RCTs, all Arizona, unreplicated); SERIOUS SAFETY — the nevi/MELANOMA case-report signal (biologically plausible, regulator-acknowledged, NOT proven causation) + idiosyncratic SAEs (rhabdo/renal/PRES); NEVER approved (abandoned ~2000) — the 2 approved descendants afamelanotide/Scenesse + bremelanotide/Vyleesi are SEPARATE compounds; grey-market w/ FDA/MHRA/TGA warnings; concentration ~90% Arizona (ABOVE flag); WADA NOT explicitly named (S2 catch-all may apply — verify NADO); MT-I≠MT-II≠PT-141 hazard. 6 non-English primaries (DE/ES/RU). **THE SWEEP'S MOST CITATION-HYGIENE-INTENSIVE entry** (section A: 4 judge iters; 4.25: 3 iters for a case-report-tag cascade) — the gates caught a fabricated regulatory number, a compound author-tangle citation, a WADA over-reach, a systematic RCT-mistag, a Wikipedia citation, a ResearchGate placeholder, an unsupported metabolite claim, + 2 judge-misidentifications correctly rejected-with-evidence.

- **PT-141 shipped** (2026-06-21, bottom-13 sweep entry 9): `compounds/pt-141.md` + `library/peptides/pt-141/{research-report,practitioner-layer,non-english-layer}.md` (~11.4K-word report, 32 dedup sources) + full `design/.pt-141-design-work/` provenance (7 attested gates 2.75→8.5 + 5 judges + 5 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: evidence_tier B / risk_tier medium — the sexual class's APPROVED member (bremelanotide/Vyleesi, the des-amide analog of MT-II); FDA-approved Jun-21-2019 for HSDD in premenopausal women ONLY (RECONNECT phase-3, n~1247) but the effect is HONESTLY MODEST (FSFI +0.35, Cohen's d ~0.27-0.39; nausea ~40%); NOT cleanly MC4R-selective (label MC1R>MC4R); off-label MALE/grey-market UNSUPPORTED (the only large male RCT under an active EoC); AEs nausea/hyperpigmentation[not-reversible]/BP+CV-contraindication; WADA not-explicitly-named; pivotal efficacy ~100% Palatin/AMAG-sponsored; Vyleesi commercially collapsed (→Cosette); flibanserin/Addyi is the other approved option; MT-II≠PT-141≠afamelanotide. Gate work: caught a Wikipedia cite the A-judge missed, a wrong DOI, a systematic Simon-extension rct-mistag, a FULLY-mismatched bib entry (27977473 Portman→White WB), 4 corporate-sources-mistagged-regulatory, the Evans-Brown editorial tag, + the practitioner-layer Safarinejad n-error+missing-EoC. 0 genuine non-English primaries (English-dominated, as expected).

- **N-Acetyl-Selank-Amidate shipped** (2026-06-21, bottom-13 sweep entry 10): `compounds/n-acetyl-selank-amidate.md` + `library/peptides/n-acetyl-selank-amidate/{research-report,practitioner-layer,non-english-layer}.md` (~10.4K-word report, 29 dedup sources) + full `design/.n-acetyl-selank-amidate-design-work/` provenance (7 attested gates + 5 judges + 5 sections). **All 7 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest + whole-vault lint clean.** Key: evidence_tier D / risk_tier experimental — THE THINNEST-EVIDENCE ENTRY; ZERO analog-specific evidence (the entire base is the Selank parent, extrapolated by an unvalidated equivalence assumption); the parent is ~87-93% single-lineage (IMG-RAS + Zakusov), Russian-only, small/open-label, inventor-co-authored, no Western RCT; the N-acetyl modification may disrupt the Tuftsin binding epitope (activity not guaranteed); Selank Russia-registered/analog-approved-nowhere; WADA doubly-hedged (S2-claim MDPI-only; S0 more plausible). 10 genuine Russian-language Selank primaries; the analog = 0 in any language. THE HEAVIEST JUDGE ROUND (all 5 sections HALTed iter-1) — gates caught a Wikipedia cite, a SCIRP predatory source, a transposed PMID (→a physics paper), a garbled Selank sequence, 2 wrong-author bib entries, an orphan-cite, + rebuilt the WADA hedge.
- **Dihexa shipped** (2026-06-22, bottom-13 sweep entry 11): `compounds/dihexa.md` + `library/peptides/dihexa/{research-report,practitioner-layer,non-english-layer}.md` (~10.6K-word report, 22 dedup sources) + full `design/.dihexa-design-work/` provenance (gates 2.75→8.5 + 5 judges + 5 sections). **All 9 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest clean.** Key: evidence_tier D / risk_tier experimental — THE MOST INTEGRITY-COMPROMISED ENTRY. The foundational HGF/c-Met mechanism papers are RETRACTED (Benoist 2014 + Kawas 2012, April 2025; McCoy 2013 dosing-anchor under a 2021 EoC); the "~100M×-more-potent-than-BDNF" marketing figure traces to the retracted paper; the only independent replication (Sun 2021) found PI3K/AKT NOT HGF/c-Met → zero non-retracted-non-WSU mechanism support (+ a Wells-2024 null); ZERO human data; the DISTINCT clinical compound fosgonimeton (Athira→LeonaBio) failed ALL trials (LIFT-AD n=554) — does not transfer to grey-market Dihexa; LOAD-BEARING safety tension = HGF/c-Met potentiation is the pathway c-Met INHIBITORS (capmatinib/tepotinib) target as cancer drugs → theoretical tumor-promotion risk (no carcinogenicity study); concentration ~67% WSU but effectively single-group-AND-retracted; $4M DOJ settlement; not-FDA/not-compoundable; WADA S0. Primary monitoring = clinical oncologic surveillance. ALL 5 sections HALTed iter-1; the gates caught FABRICATED layer authors (a hallucinated 'Bhatt' author-list — the layer-hygiene pass is load-bearing), off-enum retraction/eoc tags, a notice-cite fold; iter-2 re-judges weathered a sustained ~25-min API overload, all state preserved on disk.
- **Cerebrolysin shipped** (2026-06-22, bottom-13 sweep entry 12): `compounds/cerebrolysin.md` + `library/peptides/cerebrolysin/{research-report,practitioner-layer,non-english-layer}.md` (~10.5K-word report, 50 dedup sources) + full `design/.cerebrolysin-design-work/` provenance (gates 2.75→8.5 + 5 judges + 5 sections). **All 9 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest clean.** Key: evidence_tier B / risk_tier medium — a nationally-approved (~50-country, NOT FDA/EMA-central) porcine-brain peptide preparation whose INDEPENDENT synthesis is null/cautious. 638 peptides but NO growth-factor fragments → mimicry-not-delivery; CASTA null + the 2023-Cochrane non-fatal-SAE signal (RR 2.39); TWO integrity axes — ~60-70%-manufacturer-sponsored/E-Europe+Asia-geography/selective-outcome-reporting + the Masliah NIH-ORI misconduct finding (132 papers, 8 Cerebrolysin-specific) + 2 Rockenstein AD-paper retractions compromising the AD-mechanism evidence; healthy-adult population-mismatch; porcine-prion-theoretical. THE GATES' BIGGEST CATCH OF THE SWEEP: the iter-2 D judge caught FABRICATED + misattributed citations (a fabricated porcine-prion paper resolving to a butterfly-genetics + a tsetse-fly paper; 4 author-misattributions; a Cureus entry) that the iter-1 judge missed — repaired to eutils-verified real sources (the prion claim re-grounded on the REAL Wells 2003), then 4.75 IC-10 independently re-verified 12 PMIDs. monitoring clinical-infusion-hypersensitivity + [[biomarkers/egfr]].
- **Semax shipped** (2026-06-22, bottom-13 sweep entry 13 — THE FINAL ENTRY; **BOTTOM-13 SWEEP COMPLETE**): `compounds/semax.md` + `library/peptides/semax/{research-report,practitioner-layer,non-english-layer}.md` (~10.1K-word report, 39 dedup sources) + full `design/.semax-design-work/` provenance (gates 2.75→8.5 + 5 judges + 5 sections). **All 9 gates attested PASS; verify-chain intact; bda 0-violation; wiki-ingest clean.** Key: evidence_tier C / risk_tier experimental — a Russia-registered ACTH(4-7)-analog neuropeptide (the Selank cousin) whose 20-yr preclinical signal is almost entirely single-lineage/open-label/unreplicated. Non-corticotropic; the BDNF/NGF-TrkB mechanism is Tier-C preclinical; NO RCTs/Western-trials; the single-lineage concentration ~78-89%/~90-95% IMG-RAS/Zakusov, 0/9 independent, ZERO independent BDNF-mechanism replication, Peptogen=IMG-RAS-spinout (a structural concentration concern NOT fraud); Russia-registered-not-FDA/EMA (facts author-reported via the in-apparatus Deigin review); healthy-adult mismatch; grey-market intranasal + NASA (near-zero, N-acetylation may abolish neuroprotection). EVERY PMID eutils-verified at the source (the Cerebrolysin-fabrication lesson applied; a retrieval discarded a wrong perovskite-chemistry PMID proactively). monitoring cognitive-scale + [[biomarkers/hs-crp]].

### DONE — **BOTTOM-13 SWEEP COMPLETE** (2026-06-22): MOTS-c ✅ + SS-31 ✅ + Humanin ✅ + FOXO4-DRI ✅ + Epitalon ✅ + Thymosin-α1 ✅ + Kisspeptin-10 ✅ + Melanotan-II ✅ + PT-141 ✅ + N-Acetyl-Selank-Amidate ✅ + Dihexa ✅ + Cerebrolysin ✅ + Semax ✅ — all 13 deep-passed, all 9 gates attested PASS, chains intact, bda 0-violation. (The top-12 were the parallel session.)

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
