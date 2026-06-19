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
