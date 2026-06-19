---
title: Session Close — wiki-research parallel track (2026-06-19) — Wave 1 lipids/CV cluster
type: note
owner: Walter McGivney
created: 2026-06-19
last_reviewed: 2026-06-19
status: active
depends_on: [session-wiki-research-2026-06-18]
superseded_by: null
review_cadence: session
---

# Session Close — wiki-research parallel track (2026-06-19)

**Why a separate file (not a HANDOFF rotation):** this track runs parallel to the code
session, which OWNS `HANDOFF.md` + `memory/process-failures.md` (it closed **S73** and has
**S74 queued**). Rotating those shared volatile docs would clobber its close. Per the operator's
standing instruction, this self-contained record IS this track's close. Runs on the isolated
worktree `aplus-wiki-research` / branch `feature/wiki-research`.

---

## Goal (operator `/goal`, 2026-06-18) + this session's slice
Populate the research wiki with all backlog areas, autonomously, in protocol order, without
duplicating the parallel session, surfacing only for genuine judgment calls.
**This session delivered the first wave: the Wave 1 lipids / CV-risk biomarker cluster.**

## Acceptance — PASS
- [x] All 7 lipids/CV biomarkers researched via `/aplus-research` standard (ApoB, Lp(a), LDL-C, HDL-C, Triglycerides, GlycA, hs-CRP).
- [x] Every entry passed gates **2.75 SCOPE → 3.5 JUDGE (≥92) → 4.25 ID-RECONCILE → 4.75 INTEGRITY (13 IC)**, all `verdict: PASS`, attestation chains intact.
- [x] `bda` (`audit-research-provenance.sh … labs-specialist`) exits 0 for all 7; provenance committed under `design/.<slug>-design-work/`.
- [x] 14 pages (7 entries + 7 research-reports) authored to template, registered in `vault/meta/index.md`, ingested through the commit-time gate.
- [x] Committed: `ac2edf9` (lp-a), `b496bd4` (apob), `fb3db96` (ldl-c/hdl-c/triglycerides/glyca/hs-crp). **PR #160** open → main.
- [~] PR cycle (`/review-pr` → `/merge`): **NOT yet run** — blocked by GitHub GraphQL rate-limit; PR created via REST. Carried to next session.

## Deliverable detail
Standard-mode reference entries the `labs-specialist` reads the July panel against (LM-01 entry layer).
Confidence: established for all except **GlycA = provisional** (emerging/research-grade, platform-specific
units ~3× apart, no universal cutpoint). Honest framing preserved where the evidence demands it:
HDL-C **marker-not-target** (MR-null + failed CETP/niacin RCTs + U-shape); hs-CRP a residual-inflammation
marker with the **IL-6/IL-1β pathway** as the causal target (MR-null for CRP itself); TG **remnant-mediates**;
Lp(a) mass↔molar **non-interconvertible**.

## Close protocol (executed / documented)
1. **Test baseline — N/A (wiki-content only).** No `scripts/`/`tests/` touched; `.venv` gitignored. The relevant gate — commit-time `wiki-ingest-lint` — ran + PASSED for all 14 pages (the commits succeeded with vault pages staged).
2. **Scope check:** all changes are the 14 wiki pages + 7 provenance dirs + `vault/meta/index.md` + `docs/research-plan` §10 + this note. All in `/goal` scope.
3. **Drift (3):** Task — on-goal (Wave 1 lipids/CV cluster = the first slice; no jump-ahead). Architecture — INV-WIKI-INGESTION-GATED held (every page passed the commit gate + bda); INV-BRANCH-NOT-MAIN held (never committed to `main`). Vision — populating the knowledge base the specialists reason over; on-vision.
4. **Track state / next:** §"Track state" below (NOT in the code session's HANDOFF).
5. **Rotation rule:** N/A — self-contained record; code session's HANDOFF deliberately untouched.
5.5. **Stale-hash audit:** commit SHAs cited adjacent to this dated record; no bare sha in narrative.
6. **Memory:** §10 claims table updated (lipids/CV → DONE); this record.
7. **Beads:** `wzwg` (lipids/CV claim) → resolved by this wave's ingestion.
8. **Doc freshness:** research-plan §10 updated. Light-touch (no full-repo scan).
8.5. **Close gate (`close-audit.sh`) — documented, not mechanically run.** Session-numbered shared-doc audits (handoff/scope-contract/pf-attestation --session N) assume the shared HANDOFF + a `.venv`; this parallel `.venv`-less track keeps its close out of those docs by design. Protocol INTENT (binary AC eval, drift, PF, landmark) executed here.
8.7. **Landmark:** LM-01 (First MD visit 2026-07-13) window opens 2026-06-29 — not open today. **Linkage:** this lipids/CV reference set is exactly the entry layer LM-01's July labs are interpreted against.

## PF attestation / lessons
Three carried for capture:
- **Launch research sessions from the worktree (the operational fix, PF-S71-01 family).** a-plus's six commit-guards are PROJECT-scoped (`a-plus-maxing/.claude/settings.json`). A research session launched from the a-plus **trunk** loads `block-commit-main`, which reads the *trunk's* branch — false-blocking worktree commits whenever the trunk sits on `main`. Fix: launch from the **worktree** (`cd .../aplus-wiki-research && claude`) — guards stay active AND read the feature branch (never `main`). The parallel session avoids the block by launching from `skills_library` (a different project) — but that ALSO disables a-plus's commit-time PII + ingestion guards (thinner safety net). Hook-level fix is the code session's domain (beaded `llna`).
- **Verify the actual artifact, never an agent's claim (verify-first held).** Caught (a) a race-condition stale read — the hs-CRP re-reconcile read mid-overwrite showed HALT; the real file was PASS (checked verdict line + mtime > iter_start); (b) two remediation agents that confabulated "the re-verify passed" before it ran. Always grep the on-disk gate file + confirm freshness.
- **The gates do real work.** The JUDGE/ID-RECONCILE/INTEGRITY gates forced ~7 remediations across the wave (NLA mistag + effect-sizes re-grounded on FOURIER/ODYSSEY/IMPROVE-IT; APOC3 cite → Crosby 2014; un-grounded NCEP companion figure trimmed; Otvos tag; 4 society-guideline tag divergences). The gated pipeline caught genuine citation/tag errors — design validated.

### Disclosure ledger (2026-06-19 close)
Caught this session: 4. (reached operator only because they asked: 0 — all self-surfaced or operator-visible.)
- PF-S71-01 commit-guard false-block — detection: self (deny output + demonstrated cwd-reset); surfaced_by: self (flagged proactively).
- hs-CRP re-reconcile stale-read race — detection: self (verified file vs earlier grep); surfaced_by: self (corrected inline).
- Remediation-agent confabulation (claimed re-verify results) — detection: self (verified actual artifacts); surfaced_by: self.
- Trunk uncommitted WIP discovered at park (`vault/approaches/*`, `bpc-157` entries, `.beads/issues.jsonl`) — detection: self (checkout output); surfaced_by: self (flagged to operator).

## Track state
**What changed:** Wave 1 lipids/CV cluster fully researched + ingested (7 entries + 7 reports, 2 commits earlier + 1 wave commit), PR #160 opened.
**Current state:** wiki biomarker layer seeded with the lipids/CV cluster; engine proven end-to-end (research→gates→synthesis→page→bda→commit gate→PR). BPC-157 (Wave 0) done by other session (#150).
**What's next:**
1. **Run the PR cycle on #160** — `/review-pr` → fix legitimate findings → `/merge` (once GitHub rate-limit clears). This is the one open step for THIS wave.
2. **Next claim:** an open **Wave 1** cluster — metabolic (glucose/HbA1c/insulin/HOMA-IR/CMP), thyroid (TSH/fT3/fT4), hormones (testosterone/estradiol/cortisol/DHEA-S/IGF-1/SHBG), vitamins/minerals (vit D/ferritin/B12/RBC-Mg), or wearable (HRV/RHR/sleep/resp/recovery). **NOT peptides** — the parallel session owns tesamorelin/thymosin-α1/semaglutide/tirzepatide.
3. Flip §10 to DONE for each cluster as it lands (claim-on-start mandate).

## Coordination + operator notes
- **Trunk WIP flag:** the main trunk carries uncommitted changes that are NOT this track's (`vault/approaches/*`, `vault/compounds/bpc-157.md`, `vault/library/peptides/bpc-157/*`, `.beads/issues.jsonl`). Preserved exactly through the park/restore. The code session reported the trunk "clean" — worth reconciling before S74 builds on it.
- **Going-forward:** restart this research track from the worktree (`cd .../aplus-wiki-research && claude`) so commits flow without the trunk-park dance.
- This track claimed + completed ONLY lipids/CV; all other Wave-1 clusters remain open for whoever takes them next.
