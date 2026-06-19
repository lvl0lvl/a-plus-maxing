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

## STANDING GOAL (operator, 2026-06-18)
**Finish populating the wiki: complete ALL peptide research, round after round (triage → deep-pass
eligible → exclude rest → ship via PR cycle WITH review), until nothing is left on [[_triage]] —
without duplicating the other session's track 1 (plan pipeline). Follow the protocols.** Each round:
claim the next target in `_triage`, run it, review-gate before merge, log DONE vs CLAIMED here, claim
the next. Keep going until the triage taxonomy is fully Done/Excluded.

---

## 2026-06-19 — Cognitive class triage (round 9) — no deep-pass-eligible candidate

### DONE (verified)
- **Cognitive class triaged** (citations verified, Russian literature surveyed): **Semax 15/HOLD** (Russian open-label +
  animal; no blinded English RCT), **Selank 15/HOLD** (small Russian trials; no English RCT; NA-Selank-Amidate no distinct
  evidence — folded), **Cerebrolysin 14/HOLD** (large RCT base BUT Cochrane null/bias + non-fatal-SAE signal; IV/IM courses
  clash with no-clinic-visit limit), **Dihexa 10/EXCLUDE** (preclinical only; cornerstone papers retracted/Notice-of-Concern;
  oncogenic c-Met concern). **No deep-pass-eligible candidate.**
- Strong anti-fabrication: agents rejected two wrong-paper PMIDs (Selank), caught the Dihexa retraction (Benoist 2014 →
  PMID 40312093) + Notice of Concern (McCoy 2013), and flagged the same-class fosgonimeton Phase-2/3 failure.

### CLAIMED / RESERVED — next round
**Sexual/dopaminergic class triage** (PT-141/Bremelanotide [FDA-approved Vyleesi — likely deep-pass-eligible], Melanotan
II, Kisspeptin-10) → deep-pass eligibles. Then Immune/longevity remainder, Mitochondrial until [[_triage]] fully Done/Excluded.

---

## 2026-06-19 — GH-secretagogue class triage (round 8) — no deep-pass-eligible candidate

### DONE (verified)
- **GH-secretagogue class triaged** (citations verified): **Sermorelin 16/25 HOLD** (FDA-approved/discontinued; adult RCT
  thin — Khorram +1.26 kg LBM men-only vs Vittone NULL), **MK-677 15/25 HOLD** (real RCTs raise GH/IGF-1+FFM but FAILED
  clinical endpoints + insulin resistance + CHF signal), **CJC-1295 11/25 EXCLUDE** (surrogate-only; trial halted after a
  death), **Hexarelin 9/25 EXCLUDE** (GH desensitizes; no outcome RCT). **No deep-pass-eligible candidate** — the
  evidence-backed GHRH analog of this class (Tesamorelin) was already deep-passed. All four are gray-market + WADA S2.
- Agents held anti-fabrication: corrected a vendor misattribution (+1.26 kg LBM is Khorram, not Vittone); flagged the
  unadjudicated CJC-1295 trial death.

### CLAIMED / RESERVED — next round
**Cognitive class triage** (Selank, Semax, Cerebrolysin, Dihexa, NA-Selank-Amidate) — Russian literature will matter
(non-English layer). Then Sexual, Immune/longevity remainder, Mitochondrial until [[_triage]] is fully Done/Excluded.

---

## 2026-06-19 — Retatrutide deep pass (round 7) — METABOLIC CLASS COMPLETE

### DONE (verified)
- **Retatrutide deep pass** (triage 18/25) → entry + report + 2 layers + `.provenance/`. evidence_tier B (one Phase-2
  base; Phase-3 TRIUMPH topline NOT peer-reviewed) / risk_tier moderate. **Merge-gate review = PASS-WITH-FIXES** (5 PMIDs
  + DOI independently re-verified; investigational status + topline-not-peer-reviewed flagged everywhere; WADA accurate;
  2 nuance fixes applied: lean-to-total ratio comparable to tirzepatide, DXA completer attrition). No fabrication.
- **Metabolic class COMPLETE:** Semaglutide + Tirzepatide + Retatrutide Done; AOD-9604 Excluded.

### CLAIMED (re-checkable via `retatrutide/.provenance/sources-ledger.md`)
- **First-class caveat = SOURCING:** INVESTIGATIONAL, not approved anywhere, NO legitimate prescription/compounding
  pathway → gray-market only (unverified purity/dose). Posture = WAIT FOR APPROVAL, do not source — this overrides the
  class-leading efficacy. Plus incretin goal mismatch (lean −6.5 kg, no muscle RCT), thin long-term safety, HR rise (~+6.7 bpm).

### CLAIMED / RESERVED — next round
**GH-secretagogue class triage** (CJC-1295 ±DAC, Sermorelin, Hexarelin, MK-677) → deep-pass eligibles. Then Cognitive,
Sexual, Immune/longevity remainder, Mitochondrial until [[_triage]] is fully Done/Excluded.

---

## 2026-06-18 — Tirzepatide deep pass (round 6)

### DONE (verified)
- **Tirzepatide deep pass** (triage 24/25) → entry + report + 2 layers + `.provenance/`. evidence_tier S / off-target
  for the operator's goal. **Merge-gate review = PASS-WITH-FIXES** (14/14 load-bearing citations independently
  re-verified to exact title/journal/finding; WADA-monitoring + all regulatory dates confirmed; 3 precision fixes
  applied: DXA substudy denominator −21.3%, "by mass" qualifier on the lean ratio, SURMOUNT-4 regain phrasing). No fabrication.

### CLAIMED (re-checkable via `tirzepatide/.provenance/sources-ledger.md`)
- Most potent agent in class (SURMOUNT-1 −20.9%; beats semaglutide head-to-head −20.2% vs −13.7%, SURMOUNT-5); first/only
  FDA OSA drug (SURMOUNT-OSA). **Same GOAL MISMATCH as semaglutide:** ~25% of mass lost is lean tissue, reverses on
  stopping, NO muscle-building RCT (lean-sparing only via add-on anti-myostatin). NOT WADA-prohibited (Monitoring).

### CLAIMED / RESERVED — next round
Deep pass **Retatrutide** (18/25, investigational — entry must gate toward "wait for approval", not acquisition). Then
the remaining classes (GH-secretagogues, Cognitive, Sexual, Immune/longevity remainder, Mitochondrial) until [[_triage]] is fully Done/Excluded.

---

## 2026-06-18 — Semaglutide deep pass (round 5)

### DONE (verified)
- **Semaglutide deep pass** (triage 24/25) → compound entry + report + 2 layers + `.provenance/`. evidence_tier S
  (indications) / off-target for the operator's goal. **Merge-gate review = clean PASS** (6/6 load-bearing citations
  independently re-verified to exact title/journal/finding; WADA-monitoring claim confirmed; lean-mass figure honestly
  tier-flagged; goal-mismatch caveat prominent). No blocking issues, no required fixes.

### CLAIMED (re-checkable via `semaglutide/.provenance/sources-ledger.md`)
- **First-class caveat = GOAL MISMATCH:** tier-S, FDA-approved, but answers a different question than the operator's —
  a weight-loss/appetite-suppressing drug that reduces absolute lean mass (−9.7% STEP 1 DEXA) and reverses on stopping
  (STEP 4); NO RCT for lean-building/recovery. Off-target for post-illness rebuilding.
- Safety well-mapped (boxed thyroid-C-cell; GI; pancreatitis/gallbladder/NAION/aspiration); NOT WADA-prohibited
  (Monitoring Program). Compounded salt-forms not the approved API; gray market winding down (shortage resolved Feb 2025).

### CLAIMED / RESERVED — next round
Deep pass **Tirzepatide** (24/25), then **Retatrutide** (18/25, with the investigational-sourcing caveat). Then the
remaining classes (GH-secretagogues, Cognitive, Sexual, Immune/longevity remainder, Mitochondrial) until [[_triage]] is fully Done/Excluded.

---

## 2026-06-18 — Metabolic class triage (round 4)

### DONE (verified)
- **Metabolic class triaged** (citations verified): **Semaglutide 24/25** (tier S, FDA-approved, STEP/SELECT/SUSTAIN),
  **Tirzepatide 24/25** (tier S, FDA-approved, SURMOUNT/SURPASS), **Retatrutide 18/25** (eligible but investigational —
  sourcing 2/5, hold for approval), **AOD-9604 12/25 → Excluded** (human fat-loss claim is an unverifiable 2005
  conference abstract; the one large Phase-2b trial failed; WADA S2). Triage agents held the anti-fabrication line
  (flagged the unverifiable AOD-9604 "2.6 kg" figure).

### CLAIMED / RESERVED — next rounds
Deep pass **Semaglutide → Tirzepatide → Retatrutide** (in that order), each with the merge-gate review before merge.
Then continue the loop (GH-secretagogues, Cognitive, Sexual, Immune/longevity remainder, Mitochondrial) until
[[_triage]] is fully Done/Excluded.

---

## 2026-06-18 — Thymosin Alpha-1 deep pass (round 3)

### DONE (verified)
- **Thymosin Alpha-1 deep pass** (triage 19/25) → compound entry + report + 2 layers + `.provenance/`.
  evidence_tier B (indications) / effectively D (operator's goal). **Merge-gate review ran BEFORE merge:**
  reviewer independently re-verified 13/13 citations real, confirmed TESTS is genuinely negative and the
  WADA Tα1≠TB-500 distinction is correct → **PASS-WITH-FIXES**; 3 precision fixes applied (Romani-2004 TLR
  attribution, elderly-flu n, COVID severe-subgroup). No fabrication, no blocking issues.

### CLAIMED (re-checkable via `thymosin-alpha-1/.provenance/sources-ledger.md`)
- Two first-class caveats: (a) **the efficacy story shifted** — the best-quality sepsis trial (TESTS, BMJ
  2025, n=1089) is NEGATIVE (HR 0.99); the positive 2025 meta (OR 0.73) is a small-single-center-trial
  artifact (HQ subgroup NS). (b) **Goal-fit gap** — NO RCT for general post-illness recovery in healthy adults.
- Low-risk (drug-related AEs <1% across >2000 pts; TESTS safety = placebo); NOT WADA-prohibited (contrast
  TB-500); not FDA-approved + removed from US 503A Cat-2 (Sept 2024). Chinese-authored RCT base, surveyed.

### CLAIMED / RESERVED — next round
**Metabolic class triage** (Semaglutide, Tirzepatide, Retatrutide, AOD-9604) → deep-pass winner(s); then
continue the loop through the remaining classes until [[_triage]] is fully Done/Excluded.

---

## 2026-06-18 — Healing-class triage + Tesamorelin deep pass (round 2)

### DONE (verified)
- **Healing/soft-tissue triage pass** — TB-500 (12), GHK-Cu (11), KPV (12), LL-37 (12): all ≤12 →
  **Excluded** with re-open triggers (see [[_triage]]). Every triage citation verified real; the honest
  finding is that the remaining healing class has no deep-pass-eligible candidate vs the recovery goal.
- **Tesamorelin deep pass** (triage 21/25, winner over Thymosin Alpha-1 19/25 and Ipamorelin 16/25) →
  **compound entry + research report + 2 layers + `.provenance/` (method, sources-ledger, triage-scores,
  review-verdict)**. evidence_tier A (HIV-lipodystrophy) / effectively D (operator's non-HIV goal).
- **Merge-gate review ran BEFORE merge** (the PR-cycle review I must not skip): independent reviewer
  re-verified all 10 load-bearing PMIDs real → **PASS-WITH-FIXES**; 3 precision fixes applied (503A→deemed-biologic
  reframe, EMA date 2012-06-21, WADA named-listing upgrade). No fabrication, no blocking issues.

### CLAIMED (asserted — re-checkable via `tesamorelin/.provenance/sources-ledger.md`)
- The central finding: **ALL tesamorelin body-composition efficacy is in HIV-associated lipodystrophy;
  NO RCT exists in non-HIV/general/post-illness adults** (verified absence). Population transfer = the
  first-class caveat (analog of BPC-157's single-lab concentration).
- Safety watch-items: IGF-1 +3 SDS in 36% at 26 wk; new HbA1c ≥6.5% in 5% vs 1% (HR ~3.3); active-malignancy
  contraindication; benefit reverses on stopping; WADA S2.2.4; effectively D for the operator's goal.
- Method caveat: produced via orchestrated dispatched agents + independent review, NOT the literal
  `gate_attest` CLI chain (no machine-signed gate-N.json). See `.provenance/method.md`.

### CLAIMED / RESERVED — next round
**Thymosin Alpha-1 deep pass** (ranked-queue top, triage 19/25). Then continue the loop through the
taxonomy until [[_triage]] is fully Done/Excluded.

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

### CLAIMED / RESERVED — next session
**Healing / soft-tissue triage pass** (see [[_triage]] "Current ranked queue"): score
**TB-500, GHK-Cu, KPV, LL-37** vs goals; then deep-pass the top scorer. Reserved so the
work isn't duplicated.

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
