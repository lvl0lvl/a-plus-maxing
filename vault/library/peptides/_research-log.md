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

### NEXT (reserved, my/primary lane): **Tesamorelin** (sweep entry 7), then Sermorelin → Hexarelin → MK-677 → Semaglutide → Tirzepatide → Retatrutide → AOD-9604 → Selank. (Bottom-13 [MOTS-c…Semax] owned by `feature/wiki-peptides`.)

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
