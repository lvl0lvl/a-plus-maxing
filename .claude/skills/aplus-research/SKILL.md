---
name: aplus-research
description: Health-domain research pipeline that wraps deep-research with mechanically enforced gates. Use for any compound, intervention, biomarker, or protocol research where claims will be ingested into the project wiki. Adds paired-judge enforcement, type-tag discipline, three health-specific gates (population-mismatch, risk-floor, concentration-audit), and mandatory prescribing-practice + non-English literature layers for compound research at standard+ modes.
argument-hint: "<research question> [--mode=quick|standard|deep|ultradeep] [--target=<vault path>] [--update[=<reason-slug>]]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, mcp__basic-memory__write_note, mcp__basic-memory__search_notes
---

# aplus-research

Wraps the global `deep-research` skill with mechanically enforced gates for the a-plus-maxing project wiki. Designed to address the specific failure mode observed in the 2026-05-23 BPC-157 dispatch: an orchestrator can declare `--mode=deep` and skip paired judges, critique, and refine without mechanical resistance. This skill emits machine-readable gate JSON files that block downstream phases unless `verdict: PASS`.

## When to Use

Use for any research where output will be ingested into the project wiki:

- Compound research (peptides, supplements, hormones, nootropics, pharmaceuticals, herbals)
- Biomarker reference-range research
- Protocol literature research (training, sleep, nutrition, recovery)
- Lab-test interpretation research
- Any specialist-agent-dispatched research per [[vault/WIKI.md]] Agent Consumers section

## When NOT to Use

- Simple lookup (single fact) → `mcp__tavily__tavily_search` directly
- Library/framework documentation → `mcp__context7__query-docs`
- Debugging → Read/Grep
- General open-web investigation NOT destined for the wiki → `/deep-research` directly

## Hard Rules (non-negotiable)

1. **Mandatory paired judges.** Phase 3 retrieval agents are dispatched in pairs with judge agents. N retrieval = N judges. Phase 4 entry blocked until N judge JSON verdicts exist with `verdict: PASS`.
2. **Mandatory critique dispatch (deep/ultradeep).** Phase 6 critique is a separate dispatched agent reading the synthesized draft. Orchestrator cannot self-attest critique.
3. **Mandatory layers (standard+).** Compound research at standard/deep/ultradeep MUST run prescribing-practice layer dispatch + non-English literature dispatch. Quick mode may skip.
4. **Type-tag enforcement.** Every claim carries exactly one tag from the [[vault/library/_source-whitelist]] enum. Vendor and anecdote tags never ground numerical claims (Phase 4.75 HALT).
5. **Three health-specific gates blocking.** Population-mismatch, risk-floor, concentration-audit per [[references/health-gates]]. Each emits `gate-<name>.json verdict: PASS|HALT`.
6. **Gate verdicts authoritative in JSON, schema-validated.** Orchestrator writes `gate-<N>.json` from each agent's `gate-<N>.md`. Each `gate-<N>.json` MUST validate against `schemas/gate-<N>.schema.json`. Invalid JSON → orchestrator HALT `schema-validation-failed` BEFORE downstream phase reads it. Downstream reads JSON only.
7. **Auto-loaded project context.** Phase 1 MUST read `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, `vault/library/_source-whitelist.md`. Missing any → HALT.
8. **Additive only.** Skill does NOT modify `~/.claude/skills/deep-research/`. Wraps it.

## Pipeline Overview

```
Phase 1   SCOPE            [auto-load 4 context files; HALT if missing]
Phase 2   PLAN             [deep-research]
Phase 2.5 RUBRIC           [emit rubric.json]
Phase 2.75 SCOPE GATE      [BLOCKING] context-load verified, class identified
Phase 3   RETRIEVE         [N paired (retrieval + judge) dispatches]
Phase 3.5 JUDGE GATE       [BLOCKING] N verdicts present, all PASS
Phase 4   TRIANGULATE      [cross-section concordance]
Phase 4.5 OUTLINE REFINE
Phase 4.75 INTEGRITY GATE  [BLOCKING] type-tag + population-mismatch + concentration-audit
Phase 5   SYNTHESIZE       [corpus-read-only, tool-log audited]
Phase 6   CRITIQUE         [BLOCKING for deep/ultradeep; dispatched red-team agent]
Phase 7   REFINE           [deep/ultradeep only]
Phase 7.5 RISK-FLOOR GATE  [BLOCKING for compounds with risk_tier=experimental]
Phase 8   PACKAGE          [+ mandatory layers for standard+]
Phase 8.5 LAYERS GATE      [BLOCKING for standard+ compound research]
```

## Modes

| Mode | Phases | Source floor | Report floor | Judge threshold | Layers |
|------|--------|--------------|--------------|-----------------|--------|
| quick | 1, 2.5, 2.75, 3, 3.5, 4, 8 | 10+ | 2,000w | 85/100 | opt-in |
| standard (DEFAULT) | 1, 2, 2.5, 2.75, 3, 3.5, 4, 4.5, 4.75, 5, 7.5, 8, 8.5 | 15+ | 4,000w | 92/100 | **mandatory** |
| deep | 1-8 + 2.5/2.75/3.5/4.5/4.75/6/7/7.5/8.5 | 25+ | 10,000w | 99/100 | **mandatory** |
| ultradeep | deep + extended critique/refine | 30+ | 15,000w | 99/100 | **mandatory** |

### Gate-by-mode matrix

| Gate | quick | standard | deep | ultradeep |
|------|-------|----------|------|-----------|
| 2.75 SCOPE | ✓ | ✓ | ✓ | ✓ |
| 3.5 JUDGE | ✓ | ✓ | ✓ | ✓ |
| 4.75 INTEGRITY | **skipped** | ✓ | ✓ | ✓ |
| 6 CRITIQUE | **skipped** | **skipped** | ✓ | ✓ |
| 7.5 RISK-FLOOR (compounds only) | **skipped** | ✓ | ✓ | ✓ |
| 8.5 LAYERS (standard+ compounds only) | **skipped** | ✓ | ✓ | ✓ |

**Quick-mode rationale:** quick exists for triage scans (e.g., "scan a peptide class to pick which candidate to deep-research"). At triage, the integrity gate's cost (corpus retrieval + grep + paraphrase checks) exceeds its value — the orchestrator is judging "is this candidate worth a real research run," not "is this citable in the wiki." The scope + judge gates remain mandatory because they catch context-load failures and judge-fakery that would invalidate even triage output.

**Standard/deep/ultradeep:** all gates fire. Output is wiki-canonical and must be defensible.

## Phase 1 — SCOPE (auto-load + framing)

### 1.1 Mandatory context load

Read these four files before any retrieval. Missing any = HALT `context-load-missing`:

- `vault/meta/operator-profile.md` — slow-changing operator context (relevant for any agent that may use the entry for personalization later)
- `vault/meta/current-state.md` — current biomarkers, active protocols, active compounds (interaction surface)
- `vault/meta/goals.md` — hard limits, doctor-handout queue, accepted tradeoffs (filtering)
- `vault/library/_source-whitelist.md` — admissibility rules + type-tag enum + tier definitions

**Library-build dispatches are goal-agnostic** — the operator/current/goals files load as context but are NOT injected into the research question. They exist so any future agent querying the entry has the linkage. Specialist-agent dispatches (where the agent IS personalizing for the operator) inject relevant fields into the question.

### 1.2 Target identification

The dispatch must declare:

- `target_class` — peptide | supplement | hormone | nootropic | pharmaceutical | herbal | biomarker | protocol | other
- `target_slug` — kebab-case name (e.g., `bpc-157`, `tirzepatide`, `vitamin-d-25-oh`)
- `target_type` — compound | biomarker | protocol | reference

For compound research, output paths derived from class:
- Research artifacts: `vault/library/<class>s/<target_slug>/research-report.md` (note the plural — `peptides/`, `supplements/`, etc.)
- Compound entry: `vault/compounds/<target_slug>.md` (flat — class is metadata)

## Phase 2 — PLAN

Execute `deep-research` Phase 2 unchanged. Output: search angles, triangulation rule, quality gates, parallel agent plan.

## Phase 2.5 — RUBRIC

Execute `deep-research` Phase 2.5. Add the following mandatory rubric dimensions for health research:

- **Sikiric-style concentration audit** — for any compound, count distinct primaries by lab affiliation; flag if ≥70% from single lab
- **Population annotation** — every animal cite must carry species + n
- **Route fidelity** — no route extrapolation without explicit `[route-extrapolation]` tag
- **Risk-floor readiness** — for compounds expected to land at risk_tier=experimental, contraindications + monitoring + stopping criteria fields must be fillable from retrieved sources

Save rubric to `${BASE}/rubric.md`.

## Phase 2.75 — SCOPE GATE (BLOCKING)

The orchestrator verifies:

1. All four context files in §1.1 were read (record file paths + sha256 in `gate-2.75.json`).
2. `target_class`, `target_slug`, `target_type` declared.
3. Output paths constructed and writable (test mkdir).
4. For compound research, evaluate overwrite policy:
   - **Without `--update`**: if `vault/compounds/<target_slug>.md` exists OR `vault/library/<class>s/<target_slug>/` contains anything besides `_archive/`, HALT `compound-entry-exists`.
   - **With `--update[=<reason-slug>]`**: archive existing artifacts BEFORE any new write. Reason-slug defaults to `rerotation` if omitted; must match `^[a-z0-9][a-z0-9-]{0,40}$`.
     - Library folder children (everything except an existing `_archive/`) → `vault/library/<class>s/<target_slug>/_archive/<YYYY-MM-DD>-<reason-slug>/`
     - Compound entry (if exists) → `vault/compounds/_archive/<target_slug>-<YYYY-MM-DD>-<reason-slug>.md`
     - If the archive target path already exists (two updates same day same reason) → HALT `archive-collision`. Caller must pass a distinct `--update=<reason-slug>` to disambiguate.
     - Any filesystem failure during archive → HALT `archive-write-failed`. No partial-state allowed: if any move fails the orchestrator rolls back already-moved files to original locations and HALTs.
     - Each archive move recorded in `archive_paths` as `{from, to, archived_at}`.
5. Source whitelist loaded; type-tag enum extracted.

Emit `${BASE}/gates/gate-2.75.json`:
```json
{
  "phase": "2.75",
  "verdict": "PASS|HALT",
  "context_files": [{"path": "...", "sha256": "...", "loaded": true}, ...],
  "target": {"class": "...", "slug": "...", "type": "..."},
  "output_paths": {"research_report": "...", "compound_entry": "..."},
  "update_mode": false,
  "archive_paths": [],
  "halt_reasons": []
}
```

When `--update` is in effect: `update_mode: true` and `archive_paths` lists each performed move (empty array allowed only if nothing existed to archive — first dispatch with redundant flag).

Phase 3 refuses entry unless `verdict: PASS`.

## Phase 3 — RETRIEVE (paired dispatches)

Execute `deep-research` Phase 3 with one structural change: **every retrieval agent is dispatched in a pair with a judge agent**. The orchestrator records both in `${BASE}/dispatch-ledger.jsonl`:

```jsonl
{"role": "retrieve", "agent_id": "<uuid>", "section": "A", "brief_hash": "<sha256>", "timestamp": "..."}
{"role": "judge",    "agent_id": "<uuid>", "section": "A", "brief_hash": "<sha256>", "judges_retrieve_id": "<uuid>", "timestamp": "..."}
```

Judge agent brief: read the retrieval agent's output, score against the Phase 2.5 rubric, emit `${BASE}/judges/judge-<section>.json` with dimension scores + total + verdict (`PASS` if ≥ mode threshold, `HALT` otherwise) + specific findings.

**The orchestrator MUST dispatch both agents.** Self-judging by the retrieval agent (5-question self-check) is NOT a substitute and does not satisfy this phase.

## Phase 3.5 — JUDGE GATE (BLOCKING)

Verify:

1. For each retrieval agent dispatched, a paired judge JSON exists.
2. Each judge JSON validates against schema (dimension scores + total + verdict).
3. All judge verdicts are `PASS` at mode threshold (85/92/99/99 per quick/standard/deep/ultradeep).
4. Any HALT verdict triggers re-dispatch of that retrieval agent with judge findings injected into brief, up to 3 iterations. After 3 iterations without convergence → HALT `judge-non-convergence`.

Emit `${BASE}/gates/gate-3.5.json` with per-section verdicts.

Phase 4 refuses entry unless gate-3.5 PASS.

## Phase 4 — TRIANGULATE & VERIFY

Execute `deep-research` Phase 4. Add inline validation:

- Cross-section concordance: any numerical claim appearing in multiple sections must match (otherwise contradictions log entry).
- Aggregate concentration audit: deduplicate primaries across sections; compute single-lab share.

## Phase 4.5 — OUTLINE REFINEMENT

Execute `deep-research` Phase 4.5.

## Phase 4.75 — INTEGRITY GATE (BLOCKING)

Per [[references/citation-integrity]], the orchestrator dispatches an Integrity Verifier agent that:

1. **Type-tag check.** Every inline `[N, tag]` carries a tag from the canonical enum. Untagged → HALT.
2. **Vendor/anecdote-not-numerical check.** No `vendor_label` or `anecdote_aggregate` cite grounds a numerical claim (dose, effect size, n, AE rate, half-life). HALT on any match.
3. **Population-mismatch check** (per [[references/health-gates]] §1). Animal evidence presented as human-applicable without explicit `[population-mismatch: species]` tag → HALT.
4. **Concentration audit** (per [[references/health-gates]] §3). If single-lab share ≥ 70%, must be surfaced as a first-class section in the draft. Buried-only-in-bibliography → HALT.
5. **Route-extrapolation check.** Any dose claim where the cited primary uses a different route than the claim's route requires `[route-extrapolation]` tag. HALT otherwise.

Emit `${BASE}/gates/gate-4.75.json`. Phase 5 refuses entry unless PASS.

## Phase 5 — SYNTHESIZE

Execute `deep-research` Phase 5 with corpus-read-only enforcement. Synthesis agent's brief: read only the validated corpus + judge findings + integrity verifier findings. Cannot dispatch additional retrieval.

## Phase 6 — CRITIQUE (BLOCKING for deep/ultradeep)

Orchestrator dispatches a **separate critique agent**. Agent reads the Phase 5 draft and:

1. Identifies missing perspectives, unexamined counter-evidence, alternative explanations, biases.
2. Validates logical consistency, citation completeness, balance, objectivity.
3. **May dispatch additional targeted retrieval IF NECESSARY** to test a specific counter-claim — capped at 3 additional retrieval dispatches; each must produce a paired judge verdict.

Emit `${BASE}/gates/gate-6.json` with findings + verdict (`PASS` if no critical gaps, `HALT` with required-fix list if gaps).

Self-critique by orchestrator is **not** a substitute.

## Phase 7 — REFINE

Address critique findings. Re-run Phase 4.75 if any new primary citations introduced.

## Phase 7.5 — RISK-FLOOR GATE (BLOCKING for compounds)

Per [[references/health-gates]] §2, if the synthesized compound entry would land at `risk_tier: experimental`, the orchestrator verifies the following fields are populated from retrieved sources:

- `Risk Profile › contraindications` — non-empty, citing primary or mechanism-review sources
- `Risk Profile › monitoring` — non-empty, citing primary or practitioner-protocol sources
- `Trial Status › stopping criteria` — non-empty (may be operator-specific placeholder, but must be present in template even if blank-for-library-entry)

Compound entries failing risk-floor gate cannot be written. HALT `risk-floor-incomplete`.

## Phase 8 — PACKAGE

Generate three artifacts:

1. **Research report** — `vault/library/<class>s/<target_slug>/research-report.md`. Frontmatter includes `revisions:` log, `supplementary_layers:` pointers, `re_rotation_triggers:` list.
2. **Compound entry** — `vault/compounds/<target_slug>.md` populated from template, operator-specific fields blank.
3. **Index + log updates** — append to `vault/meta/index.md` and `vault/meta/log.md`. When `update_mode: true`, the log op is `update` (not `create`) and the line MUST reference the archive folder so the prior version is one path-resolution away. Index entry path is unchanged (archive content is invisible to the live index).

For standard+ compound research, ALSO dispatch:

4. **Prescribing-practice layer** — separate dispatched agent per [[references/health-gates]] §4. Output: `vault/library/<class>s/<target_slug>/practitioner-layer.md`.
5. **Non-English literature layer** — separate dispatched agent. Output: `vault/library/<class>s/<target_slug>/non-english-layer.md`.

## Phase 8.5 — LAYERS GATE (BLOCKING for standard+ compound research)

Verify:

1. Both layer files exist at expected paths.
2. Each layer file has its own bibliography and self-check.
3. Prescribing-practice layer documents at least 1 compounding-pharmacy data sheet OR explicit "no admissible data sheet located" with searched-vendor list.
4. Non-English layer documents survey of at least Russian + Chinese + originator-country (if non-English) with explicit "no admissible primaries located" or new citations.

Emit `${BASE}/gates/gate-8.5.json`. Final report-package marked complete only on PASS.

## Recovery After Compaction

Surviving state under `${BASE}` (where `BASE=/tmp/aplus-research/<target_slug>/`):
- `dispatch-ledger.jsonl`
- `gates/gate-*.json`
- `judges/judge-*.json`
- `sections/section-*.md`
- `phase-5-tool-log.jsonl`

Procedure: read `${BASE}/gates/` for highest gate with `verdict: PASS` → resume at next phase.

## Reference Files

| File | Purpose | Loaded at |
|------|---------|-----------|
| [references/health-gates.md](./references/health-gates.md) | Three health-specific gates: population-mismatch, risk-floor, concentration-audit; plus mandatory-layers spec | Phase 4.75, Phase 7.5, Phase 8.5 |
| [references/citation-integrity.md](./references/citation-integrity.md) | 13 IC checks including per-citation corpus scoping (IC-13); integrity verifier brief | Phase 4.75 |

The base source whitelist + type-tag enum lives at `vault/library/_source-whitelist.md` and is NOT duplicated here — single source of truth.

## Schema Files (gate verdict validation)

| Schema | Validates |
|--------|-----------|
| [schemas/gate-2.75.schema.json](./schemas/gate-2.75.schema.json) | Phase 2.75 SCOPE gate verdict — context_files, target, output_paths, halt_reasons |
| [schemas/gate-3.5.schema.json](./schemas/gate-3.5.schema.json) | Phase 3.5 JUDGE gate verdict — per-section judge_verdicts, scores, brief_hash uniqueness |
| [schemas/gate-4.75.schema.json](./schemas/gate-4.75.schema.json) | Phase 4.75 INTEGRITY gate verdict — 13 IC checks, population_mismatch, concentration_audit, corpus_scoping |
| [schemas/gate-6.schema.json](./schemas/gate-6.schema.json) | Phase 6 CRITIQUE gate verdict — findings, additional_retrievals (max 3) |
| [schemas/gate-7.5.schema.json](./schemas/gate-7.5.schema.json) | Phase 7.5 RISK-FLOOR gate verdict — risk-tier-conditional field requirements |
| [schemas/gate-8.5.schema.json](./schemas/gate-8.5.schema.json) | Phase 8.5 LAYERS gate verdict — practitioner_layer + non_english_layer presence + structure |

**Validation procedure.** After writing each gate-N.json, orchestrator runs:
```bash
python3 -c "import json, jsonschema; jsonschema.validate(json.load(open('gate-N.json')), json.load(open('schemas/gate-N.schema.json')))"
```
or equivalent. Failure → HALT `schema-validation-failed`; orchestrator does NOT proceed to next phase. The verdict-PASS-but-halt-reasons-non-empty contradiction is mechanically caught by each schema's `allOf` constraint.

## Known Limitations

- v1 does not implement Quant-style agent-identity-ledger UUIDv4 disjointness enforcement. Brief-hash uniqueness via sha256 is the v1 substitute (enforced in gate-3.5 schema).
- v1 does not implement full corpus sanitization (prompt-injection scanning of retrieved corpora before grep). Tier-1/2 source whitelist + manual review of any Tier 2.5+ source is the v1 substitute.
- v1 IC-13 corpus scoping retrieves abstract-only for paywalled content; full-text retrieval bypass is not implemented. Claims relying on full-text-only content that the abstract doesn't cover get `corpus-missing` WARN, not HALT.
- v1 has no regression fixture suite. Failure modes will inform v2.
- Schema validation requires `jsonschema` Python package; orchestrator must verify presence at pre-flight. Missing → HALT `jsonschema-not-installed` with install instruction.

## Output Path Convention

| Research target | Research artifacts | Entity entry |
|---|---|---|
| Compound (peptide, supplement, hormone, etc.) | `vault/library/<class>s/<slug>/research-report.md` + `practitioner-layer.md` + `non-english-layer.md` | `vault/compounds/<slug>.md` |
| Biomarker | `vault/library/biomarkers/<slug>/research-report.md` | `vault/biomarkers/<slug>.md` |
| Protocol | `vault/library/protocols/<slug>/research-report.md` | `vault/protocols/<slug>.md` |

Compounds folder stays flat (class is metadata in frontmatter). Library folder is class-organized (research artifacts cluster by domain).
