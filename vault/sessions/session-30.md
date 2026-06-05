---
title: Session 30 — V1 execute stage, Wave 1; 3 design/measurement spikes (PII-boundary, store-keying, render-size); beads 394/bez/qbb closed
type: session
permalink: a-plus-maxing/sessions/session-30
created: 2026-06-05
session: S30
---

# Session 30 (2026-06-05)

## Goal (as contracted)

Execute **Wave 1** of the V1 build — the first execute-stage session (all prior sessions were design-only). Run the three dependency-free Wave-1 spikes (`ADR-0001-T0` PII-boundary, `ADR-0002-T0` store-keying, `ADR-0004-T0` render-size) through their approved recipes' adapted non-code TDD cycles, producing the (gitignored) spike design/measurement reports the downstream impl tasks consume, and close the three `v1-build` beads to unblock Wave 2. Read each recipe IN FULL first (PF-S17-01). Orchestrator coordinates; Architect workers produce all content (the recipes' `assigned-agent: Architect`); a fresh independent Architect reviews the wave (PF-S3-01).

## What happened

1. **Read all 3 recipes in full** before executing (PF-S17-01, per-invocation). Surfaced + verified the key fact: all three deliverables home in the **gitignored** `docs/spec/.pipeline/` (confirmed `git check-ignore`); every downstream consumer (`ADR-0001-T1`/`ADR-0002-T1`/`ADR-0003-T1`) `test -f`s the working-tree path and acknowledges "verified against the working tree, not git history"; `ADR-0003-T1` states the durable contract is the distilled tracked code (`scripts/store/keying.py`), not the spike report. This is intended, reviewed, merged design — the spikes are scaffolding whose decisions get baked into tracked code by the consuming impl tasks; gitignored reports survive branch ops, persisting in this checkout for later waves. Not relitigated.

2. **Dispatched 3 Architect workers (full 11-section profile inlined verbatim, INV-ROLE-INLINING) in parallel** — one per spike, each running the recipe's RED-equiv → GREEN-equiv → REFACTOR-equiv → REGRESSION-equiv cycle. Hard-Rule-1 held: the orchestrator coordinated + ran the mechanical verification batteries; workers produced all report content. No `Workflow`/hand-rolled-fan-out substitution.

3. **Orchestrator re-ran the mechanical batteries independently** (PF-S3-01 — worker self-reports not trusted): all sections present; ADR-0002-T0 dedupe tuple proven ⊆ Line Field Set; **ADR-0004-T0 `wc -c` reproduced exactly (57741 bytes)** + 0-external-refs on the fixture; single-selection holds; tracked tree clean (only the orchestrator's HANDOFF scope-contract write).

4. **Fresh independent Architect review of the wave** caught a REAL blocking defect the mechanical checks passed: `ADR-0001-T0` selected `unshare -rn` (Linux-only) as the single egress mechanism, but the operator target is **macOS** (verified: `unshare` absent, `sandbox-exec` present) — so the downstream `ADR-0001-T1` guard build would HALT on the PII critical path. Plus two real findings: the PII-scan keyword list was a closed 5-biomarker vocabulary missing the broader clinical set (1B), and it assumed an informal line shape disagreeing with the `ADR-0002-T0`-fixed `{item,timepoint,source,value}` (1C). ADR-0002-T0 + ADR-0004-T0: ACCEPT.

5. **Remediation (Architect worker) fixed all three** (PF-S26-01, 0 suppressed): 1A → OS-level network isolation as one mechanism with a deterministic per-OS binding (`sandbox-exec` deny-network on Darwin, `unshare -rn` on Linux) dispatched by `platform.system()`, fail-closed-on-unavailable, catches subprocess egress (Security HIGH-1) — runnable on the macOS operator host AND clonable to Linux (ADR-0005), AC-6 single-selection preserved; 1B/1C → a biomarker-independent **structural** `{item,timepoint,source,value}` store-line detector replacing the keyword list.

6. **Blind re-verification (fresh Architect)** confirmed 1A/1B/1C resolved + design-sound + no regression, and (being skeptical) caught a NEW real defect: the PII-scan **command** `git ls-files -z | rg -0 --files-with-matches` searches the NUL-joined **filename stream**, not file **contents** — a silently false-passing PII scan (the worst failure mode for this check). Fixed (PF-S26-01) to `git ls-files -z | xargs -0 rg --files-with-matches`; orchestrator independently proved the plumbing via a `grep` real-binary topology stand-in (this sandbox's `rg` is a shell-function shim that `xargs` can't exec; the operator's machine has real ripgrep where `xargs -0 rg` is canonical).

## The deliverable (durable handoff — reports are gitignored; decisions recorded here)

Three spike reports in the working-tree `docs/spec/.pipeline/` (gitignored, consumed by Wave 2 from the working tree). Their decisions, recorded here as the durable provenance:

| Spike | Decision (the design contract Wave 2 builds against) |
|-------|------------------------------------------------------|
| **ADR-0001-T0** PII-boundary | **Egress guard:** OS-level network isolation, one mechanism, per-OS binding via `platform.system()` — macOS `sandbox-exec` deny-network profile, Linux `unshare -rn` namespace — behind `egress_guard.run(callable)`; **fail-closed** (falsy/default-deny) if the binding can't be established; catches whole-process-tree (subprocess) egress. **PII scan:** `git ls-files -z \| xargs -0 rg --files-with-matches` over tracked files with (a) exhaustive identity tokens (`Walter`/`McGivney`/`@gmail.com`) and (b) a structural `{item,timepoint,source,value}` store-line detector (ISO-8601 `timepoint` co-occurring with `item`/`value`, both field orders), biomarker-independent; pass = 0 hits on a fresh clone. **No-raw-to-model rule:** ingestion's only sink is the local store; static `rg` scan of the ingestion path for model/network imports + the egress-namespace runtime backstop. |
| **ADR-0002-T0** store-keying | One NDJSON file **per item** under `vault/store/` (slug-keyed `<item>.ndjson`, flat dir). Timepoint = **ISO-8601 to the second, UTC** (lexicographic = chronological). Source tag = `source`. **Line Field Set = `{item, timepoint, source, value}`** (the sole schema `ADR-0002-T1` crit-5 validates). **Dedupe tuple = `(item, timepoint, source)`** — proven ⊆ Line Field Set; `value` excluded so a corrected same-instant re-reading is the same reading (idempotency). |
| **ADR-0004-T0** render-size | Worst-case **10 biomarkers × 4 timepoints**, combined matrix+projection, inline-SVG / no-chart-library / 0-external-ref → **measured 57741 bytes** (`wc -c`, reproduced; UNDER the 500000 ceiling). **Cap = max 16 series-per-view AND max 12 timepoints-per-view** (cost model `2377 + S·(5536+579·(T−4))`, 2.0× density inflation for the real template + 30% ceiling reserve → ~330130 real bytes at the cap, 34% below 500000). **Mitigation = cap** (single). **`ADR-0004-T1` re-validation trigger:** re-measure against the real template before `ADR-0004-T2`/`ADR-0007-T2` consume the cap. |

**Handoff to Wave 2:** `bd ready` frontier = `89a` (ADR-0002-T1 store + `keying.py`) and `e9m` (ADR-0001-T1 egress/PII guard) — the enforcement-first PII pair. Work each by reading its recipe IN FULL, running its TDD cycles (real `pytest` code now — Wave 2 builds production modules), satisfying its Verification Checklist, then `bd close`.

## Carried flag for Wave 2 (surfaced, not lost — PF-S26-01)

- **`ADR-0001-T1` (e9m) — pii_scan.py MUST search file CONTENTS, not the filename stream.** The spike command was corrected to `git ls-files -z | xargs -0 rg` (args → contents); `ADR-0001-T1`'s `pii_scan.scan` must implement the args form and carry a **failing-capable test that injects operator-PII into a tracked file's CONTENTS and asserts the scan catches it** (a test that injects into a filename, or that pipes the path stream to the matcher, would mask the false-pass). This is the safety-relevant guard against reintroducing the false-negative the blind re-verify caught.

## Notable judgments

- **The review chain earned its place twice on the PII critical path.** Mechanical checks (sections, single-selection, follow-up IDs) all passed for ADR-0001-T0, yet the independent Architect caught a macOS-portability blocker (`unshare` absent) and the blind re-verifier caught a false-passing scan command. Both REAL, both fixed; neither suppressed by severity (PF-S26-01). A wave that had trusted the all-PASS mechanical battery + worker self-reports would have shipped a Wave-1 spike that HALTs its own Wave-2 consumer.
- **Gitignored spike deliverables → decisions captured in this tracked note.** The reports don't travel in git; the consuming impl tasks distill them into tracked code. Recording the 3 decisions here is the durable provenance hedge (clonability + recoverability) without force-adding the gitignored reports (recipe Commit convention).
- **`assigned-agent: Architect` honored, incl. the ADR-0004-T0 throwaway harness.** The Architect built an off-tree measurement harness (recipe Deviation 1) — not a role-boundary violation, because the production render path is built by the downstream tasks this spike blocks (no SE task to hand to). Throwaway, off-tree, not committed.

## Discipline notes

- **Read-before-invoke HELD** (PF-S17-01): all 3 recipes + the spec task blocks + build-plan Wave-1 sections read in full before executing.
- **Hard-Rule-1 HELD**: every report / review / remediation artifact was a dispatched Architect worker or a mechanical orchestrator check; the orchestrator never authored spike design content. The one orchestrator-side fix consideration (the `xargs -0` plumbing) was routed back to the remediation worker, not self-authored.
- **Anti-self-attestation HELD** (PF-S3-01): the orchestrator mechanically re-extracted every report (sections, subset proof, `wc -c` reproduction, single-selection) and dispatched a fresh reviewer + a fresh blind re-verifier (independent agents); the macOS blocker + the scan-command false-pass were both adjudicated on independently-verified evidence (verified `unshare` absent on-host; reproduced the pipe-vs-args topology with a real binary), not deferred to worker self-report.
- **PF-S26-01 window TRIPPED-CLEAN (guard HELD)**: 4 real findings (1A blocking + 1B + 1C + the scan-command false-pass) — ALL fixed, 0 suppressed; the macOS blocker was not waved off as "design detail," the false-passing command was not deferred as "ADR-0001-T1's problem." Every real finding fixed on the artifact in hand.

## State at close

- 3 gitignored Wave-1 spike reports in the working-tree `docs/spec/.pipeline/`; decisions recorded above. **No tracked code built** — the spikes are non-code design/measurement (the first execute session is the lightest part of execute). Tracked changes this session = HANDOFF + this note + log + 3 bead closures.
- Pipeline: PRD (S24) → ADR (S25) → spec [S26+S27] → build-plan [S28] → task-plan [S29] → **execute Wave 1 [S30] ✓** → Wave 2 (UNBLOCKED).
- Beads: `394`/`bez`/`qbb` CLOSED; `bd ready` frontier advanced to Wave 2 (`89a`, `e9m`). No new beads filed (the `ADR-0001-T1` contents-search obligation is carried as a HANDOFF flag + this note, not a bead).

See `docs/task-plan/` (the 3 recipes), `docs/spec/.pipeline/` (the 3 gitignored reports), `docs/build-plan/build-plan-v1-full.md` (Wave-1→2 boundary), HANDOFF S30 (contract + evaluation + What Is Next), [[design/vision]].
