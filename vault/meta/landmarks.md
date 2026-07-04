---
title: Landmark Register
type: reference
status: active
created: 2026-05-25
last_reviewed: 2026-06-19
review_cadence: session
permalink: a-plus-maxing/meta/landmarks
---

# Landmark Register

Append-only register of project landmarks. Each landmark declares relevant scopes and trigger windows. Discipline is **landmark-agnostic**: the periodic drift audit cadence (every 5 sessions) is the always-on baseline; landmarks add *additional* scoped audits with explicit trigger windows that fail-clean by transitioning to `status: completed` after the landmark passes.

**Why this design:** if "the doctor visit" became THE checkpoint, the discipline would silently degrade after that date. This register is permanent; specific landmarks come and go.

## Entry format

```
### LM-{NN} — <short name>
- **date:** YYYY-MM-DD
- **relevant_scopes:** <vault paths or content categories the landmark concerns>
- **trigger_windows:**
  - <window>: <action>
- **status:** active | completed | superseded
- **rationale:** <why this is a landmark, not just a date>
- **on_status_change:** <what happens after status flips>
```

---

## Active landmarks

### LM-01 — First MD visit (August 2026 doctor appointment)
- **date:** 2026-08-04 (RESCHEDULED from 2026-07-13 per operator S107, 2026-07-04; 14-day window opens 2026-07-21, 7-day 2026-07-28)
- **relevant_scopes:**
  - `vault/meta/operator-profile.md` (especially January 2026 health-issue section + medications + allergies)
  - `vault/compounds/*` where `risk_tier: medium+` or `risk_tier: experimental`
  - `vault/biomarkers/*` baseline-panel candidates
  - `vault/library/peptides/bpc-157/*` (currently the only compound in the queue; bears MD-handoff relevance because risk_tier=experimental)
  - `goals.md` doctor-handout-queue subsection
- **trigger_windows:**
  - **14 days before:** scoped drift audit on relevant_scopes only; verify each entry's `last_verified` is within 30 days; verify doctor-handout queue is current; surface any contradictions
  - **7 days before:** generate MD-handoff artifact (HTML or PDF — single document summarizing compounds being considered + biomarkers requesting + January-2026-issue-update + contraindication map)
  - **0–7 days after:** ingest visit outcomes — new prescriptions, lab orders, diagnoses, follow-up schedule
- **status:** active
- **rationale:** First primary-care relationship establishment for this operator. Without this visit, all `risk_tier: medium+` compounds remain blocked by operator-profile.md January-2026-section HALT rule. The visit is the first downstream consumer of the vault's research layer.
- **on_status_change (when status flips to `completed`):** Archive this entry (status: completed); register LM-02 (next MD follow-up) with new date. Do NOT delete — the historical entry stays. Next landmark of similar class registers as its own LM-NN.

### LM-02 — wearable strap + first 30-day wearable baseline
- **date:** TBD (source re-anchored to **Apple Health** per ADR-0012 — the operator uses Apple Health, not Whoop; the `healthkit` adapter reading the real `export.xml` is built S82; baseline-start pending the first real export)
- **relevant_scopes:** `vault/meta/current-state.md` Wearable (Apple Health) section; `vault/biomarkers/hrv.md` (TODO); `vault/biomarkers/rhr.md` (TODO); `vault/biomarkers/sleep-efficiency.md` (TODO)
- **trigger_windows:**
  - **baseline-start + 30 days:** ingest first 30-day baseline into `current-state.md` Wearable section; create biomarker pages with `last_verified` set to the 30-day window end
- **status:** active
- **rationale:** First continuous-measurement biomarkers become available; current-state.md transitions from labs-only to labs+wearable. Specialist agents (recovery-specialist, sleep-coach) gain queryable data. **Source re-anchored Oura→Whoop→Apple Health: as of ADR-0012 (S82) the operator uses Apple Health, and the `healthkit` adapter reads the operator's real `export.xml` (streamed + daily-aggregated). (Prior anchoring: Oura→Whoop per ADR-0011 D2/D3, re-decided S62 — superseded; the Whoop adapter remains wired for coexistence but is not the operator's source.)**

### LM-03 — 23andMe raw file ingest
- **date:** TBD (pending Walter at desktop)
- **relevant_scopes:** `vault/dna/raw/` + `vault/dna/analysis.md`
- **trigger_windows:**
  - **on receipt:** parse SNPs of clinical relevance; populate operator-profile.md "Known DNA variants of note" section; create `vault/dna/analysis.md`
- **status:** active

### LM-04 — First HTML artifact generation
- **date:** TBD
- **relevant_scopes:** project-wide; first artifact establishes the artifact-design-protocol baseline (per `vault/design/artifact-design-protocol.md`)
- **trigger_windows:**
  - **on generation:** validate against artifact-design-protocol; archive original artifact + screenshot in `vault/artifacts/{slug}/`
- **status:** active

---

## Completed landmarks

_(none yet — first will be LM-01 after July 2026 visit, at which point this section starts accumulating)_

---

## Pipeline integration

The cadence-based drift audit (every 5 sessions) is separate from landmark triggers and continues regardless of landmark state. Landmark triggers are *additional* scoped audits.

**Audit dispatch rule:** When checking active landmarks at session start, for each `active` landmark:
1. Compute days-to-landmark (or days-since if past trigger window).
2. If a trigger window is currently active (e.g., today is between landmark.date - 14 and landmark.date - 7), dispatch the audit/action specified.
3. If landmark.date has passed AND all post-landmark windows are exhausted, flag for status flip to `completed` at next session close.

**Audit fail mode:** A scoped audit failure is logged to PF only if it surfaces a previously-undetected contradiction or a violated invariant. Surfacing expected work (e.g., "doctor-handout queue is empty 14 days out") is a status report, not a PF.
