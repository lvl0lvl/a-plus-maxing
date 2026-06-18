---
name: aplus-research
description: Health-domain research pipeline that wraps deep-research with mechanically enforced gates. Use for any compound, intervention, biomarker, or protocol research where claims will be ingested into the project wiki. Adds paired-judge enforcement, type-tag discipline, three health-specific gates (population-mismatch, risk-floor, concentration-audit), and mandatory prescribing-practice + non-English literature layers for compound research at standard+ modes.
argument-hint: "<research question> [--mode=quick|standard|deep|ultradeep] [--target=<vault path>] [--update[=<reason-slug>]]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, mcp__basic-memory__write_note, mcp__basic-memory__search_notes
---

# aplus-research

Wraps the global `deep-research` skill with mechanically enforced gates for the a-plus-maxing project wiki. Designed to address the specific failure mode observed in the 2026-05-23 BPC-157 dispatch: an orchestrator can declare `--mode=deep` and skip paired judges, critique, and refine without mechanical resistance. This skill emits machine-readable gate JSON files that block downstream phases unless `verdict: PASS`.

## Calibration history (S3 → present)

The skill is edited in place. Each calibration is logged here with the session, evidence, and resulting change so the lineage is explicit.

| Cycle | Date | Finding | Change | Evidence |
|---|---|---|---|---|
| v1.0 | 2026-05-23 (S2) | initial build | 6 blocking gates; `attestation_chain` deferred to v1.1 | PF-S2-01 (deep-mode self-attestation in `/deep-research`) |
| v1.1 | 2026-05-25 (S4) | orchestrator self-attested 5 of 6 gates | `gate_attest.py` + `attestation_chain` required in 5 schemas; iter max 3→4; per-section iter_start_ts (BUG-001) | PF-S3-01 (recurrence_count=2) |
| v2 AC1 | 2026-05-25 (S6) | iter-2 remediations missed cross-section metadata mismatches | Phase 4.25 cross-section identity reconciliation as blocking gate between TRIANGULATE and OUTLINE-REFINE | S3/S4 BPC-157: iter-3 judges surfaced Section A Ref [2] PMID + Section C Xue-2004 narrative drift that iter-2 missed |
| v2 AC2 | 2026-05-25 (S6) | metadata fixes landed in obvious-place but missed adjacent narrative/tally lines | Post-fix grep enforcement mandatory in remediation briefs (Phase 3.5 iter-2+, 4.75 verifier remediation, 6 critique remediation) | AP-INCOMPLETE-PROPAGATION (S4 Top-3) |
| v2 AC3 | 2026-05-25 (S6) | judge JSONs returned divergent shapes; orchestrator hardcoded scores into gate-3.5 | Judge brief template includes literal JSON skeleton the judge MUST emit | PF-S3-01 §judge-shape divergence |
| v2 AC4 | 2026-05-25 (S6) | basic-memory linter auto-suffixed archived compound entry permalink with `-1` | Archived entries get scoped permalinks `a-plus-maxing/compounds/_archive/<slug>-<date>-<reason-slug>` | S3 BPC-157 archive |

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
9. **No orchestrator self-attestation of gate verdicts.** Gate JSONs for phases 3.5, 4.75, 6, 7.5, 8.5 MUST be produced by `lib/gate_attest.py attest` after an agent-written source file has been generated by a dispatched verifier. The script enforces (a) `start-iteration` was called first, (b) the agent-source markdown exists, (c) its mtime > iter_start_ts, (d) the markdown has a parsable `## Verdict` block, (e) the resulting gate JSON validates against schema with a required `attestation_chain`. Orchestrator-side composition of these gate JSONs from prose summaries is a documented protocol violation (see `memory/process-failures.md` PF-S3-01). Phase 2.75 is exempt (mechanical sha256 + filesystem ops, no agent verdict). See "Attestation chain" section below.

## Pipeline Overview

```
Phase 1   SCOPE            [auto-load 4 context files; HALT if missing]
Phase 2   PLAN             [deep-research]
Phase 2.5 RUBRIC           [emit rubric.json]
Phase 2.75 SCOPE GATE      [BLOCKING] context-load verified, class identified
Phase 3   RETRIEVE         [N paired (retrieval + judge) dispatches]
Phase 3.5 JUDGE GATE       [BLOCKING] N verdicts present, all PASS
Phase 4   TRIANGULATE      [cross-section concordance]
Phase 4.25 ID-RECONCILE GATE [BLOCKING for standard+] shared-entity cross-section consistency
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
| standard (DEFAULT) | 1, 2, 2.5, 2.75, 3, 3.5, 4, 4.25, 4.5, 4.75, 5, 7.5, 8, 8.5 | 15+ | 4,000w | 92/100 | **mandatory** |
| deep | 1-8 + 2.5/2.75/3.5/4.25/4.5/4.75/6/7/7.5/8.5 | 25+ | 10,000w | 99/100 | **mandatory** |
| ultradeep | deep + extended critique/refine | 30+ | 15,000w | 99/100 | **mandatory** |

### Gate-by-mode matrix

| Gate | quick | standard | deep | ultradeep |
|------|-------|----------|------|-----------|
| 2.75 SCOPE | ✓ | ✓ | ✓ | ✓ |
| 3.5 JUDGE | ✓ | ✓ | ✓ | ✓ |
| 4.25 ID-RECONCILE | **skipped** | ✓ | ✓ | ✓ |
| 4.75 INTEGRITY | **skipped** | ✓ | ✓ | ✓ |
| 6 CRITIQUE | **skipped** | **skipped** | ✓ | ✓ |
| 7.5 RISK-FLOOR (compounds only) | **skipped** | ✓ | ✓ | ✓ |
| 8.5 LAYERS (standard+ compounds only) | **skipped** | ✓ | ✓ | ✓ |

> **"compounds only" = a compound ENTRY**, i.e. `target.type=compound` in `gate-2.75.json` (risk_tier fields + prescribing/non-English layers) — NOT a goal-agnostic reference landscape (`target.type=reference`) nor the slug's coarse risk-table `target_class`. A reference-landscape dispatch skips 7.5/8.5, and the `bda` merge audit (`scripts/audit-research-provenance.sh`) keys its 7.5/8.5 requirement on the same `target.type` signal (bead `mhg`; INV-RESEARCH-PROVENANCE-DISJOINT change-discipline S21, 2026-06-02).

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

**Judge JSON skeleton — REQUIRED inline in every judge brief (v2 AC3 calibration).** S3 judges returned divergent JSON shapes (some used `total`, some `total_score`, some `score_summary`); the orchestrator hardcoded scores into gate-3.5 from prose rather than re-briefing. The defense: the brief carries the literal skeleton the judge MUST emit. Schema-conformant output at brief time, no orchestrator-side shape massaging.

The orchestrator MUST inject this verbatim block into every Phase 3 judge brief:

```
OUTPUT FORMAT (non-negotiable)

Write your verdict to: ${BASE}/judges/judge-<SECTION-LETTER>.json
Where <SECTION-LETTER> is the single-letter section ID (A, B, C, ...) the
paired retrieval agent covered.

Your output MUST validate against this exact JSON skeleton:

{
  "section": "A",                            // single uppercase letter
  "brief_hash": "<sha256 of your brief>",   // dispatching orchestrator records this
  "iteration": 1,                            // 1, 2, 3, or 4 (path-b)
  "dimension_scores": {
    "evidence_quality": 0,                   // 0-100 integer
    "citation_fidelity": 0,                  // 0-100 integer
    "type_tag_discipline": 0,                // 0-100 integer
    "population_annotation": 0,              // 0-100 integer
    "route_fidelity": 0,                     // 0-100 integer
    "concentration_audit_handling": 0,       // 0-100 integer
    "risk_floor_readiness": 0,               // 0-100 integer (or null if N/A
                                              //   for biomarker/protocol research)
    "reasoning_integrity": 0,                // 0-100 integer
    "completeness_vs_brief": 0               // 0-100 integer
  },
  "total": 0,                                // 0-100 integer (rounded mean of
                                              //   non-null dimensions)
  "threshold": 99,                           // mode threshold: 85/92/99/99
  "verdict": "PASS",                         // "PASS" or "HALT" exactly
  "findings": [                              // empty array if PASS
    {
      "severity": "critical",                // "critical"|"major"|"minor"
      "dimension": "citation_fidelity",      // must match a dimension_scores key
      "claim_or_location": "Section A line 47, Ref [12]",
      "issue": "First-author surname disagrees with cited PMID",
      "recommended_fix": "Re-verify against PMID 12345678 and correct attribution"
    }
  ]
}

Required structural rules:
- `verdict: "PASS"` requires `findings: []` (empty array). A non-empty findings
  array with verdict PASS is a schema violation; emit HALT instead.
- `total` MUST equal the rounded mean of the non-null `dimension_scores`. If
  your computed total < threshold, verdict MUST be "HALT", not "PASS".
- Do NOT add extra top-level keys. Do NOT rename keys. Do NOT use nested
  variants ("score_summary": {...}). The orchestrator reads only this shape.
- Do NOT emit prose outside this JSON. Write your reasoning into the `findings`
  array's `issue` fields, not as preamble.
```

This block does NOT replace the rubric — the rubric (Phase 2.5) defines what each dimension means and how to score it. The skeleton defines how to express the result.

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

## Phase 4.25 — ID-RECONCILE GATE (BLOCKING for standard+)

Cross-section identity reconciliation. Surfaces metadata mismatches BEFORE the integrity verifier (Phase 4.75) has to find them, and BEFORE outline refinement (Phase 4.5) locks structure around inconsistent identifiers. v2 calibration response to S3/S4 BPC-157: iter-3 judges caught Section A Ref [2] PMID inversion + Section C narrative drift on Xue 2004 institution attribution that iter-2 in-skill remediation had missed. A dedicated reconciliation step closes the gap upstream.

Orchestrator dispatches an ID-Reconcile agent that:

1. Scans all section drafts (`sections/section-*.md`) for **shared entities** of these classes:
   - **Citations** (`[N, tag]` references) — first-author surname + initials, year, PMID/DOI, source-title, source-type
   - **Institutions** named in any sentence — canonical name (e.g., "Fourth Military Medical University Xi'an", not "FMMU" without expansion)
   - **Compound/molecule identifiers** — CAS number, ChEMBL ID, InChI key (when given), brand vs INN vs research-code (e.g., PL 14736 vs BPC-157 vs Pliva-14736)
   - **Dates of regulatory events** — FDA action dates, EMA dates, trial-registration dates
   - **Trial registrations** — NCT/EudraCT/ChiCTR identifiers

2. For each shared entity that appears in 2+ sections: extract the values used in each section. If values disagree (string-identity for IDs, normalized-form-identity for names), record a `mismatch` entry.

3. Emit `${BASE}/sections/id-reconcile-source.md` with:
   - `## Verdict` block: `verdict: PASS` (no mismatches found) OR `verdict: HALT` (≥1 mismatch)
   - Per-class mismatch table: entity-id, sections involved, divergent values, suggested canonical value (with justification when possible)
   - Whole-corpus tally: total shared entities scanned, mismatch count by class

4. On HALT: the agent's report becomes the work-list for a paired remediation dispatch (Phase 4.25-remediation, treated as iter-2 of this phase). Remediation MUST follow the remediation-brief template (see "Remediation brief addendum" below) including the post-fix grep step.

5. After remediation, re-dispatch the ID-Reconcile agent. Iter max 3 per attestation_chain conventions.

The orchestrator composes the gate JSON via:
```bash
python3 .claude/skills/aplus-research/lib/gate_attest.py start-iteration \
    --base /tmp/aplus-research/<slug> --phase 4.25
python3 .claude/skills/aplus-research/lib/gate_attest.py attest \
    --base /tmp/aplus-research/<slug> --phase 4.25
```

Phase 4.5 refuses entry unless gate-4.25 PASS.

**Schema:** `schemas/gate-4.25.schema.json` validates the composed JSON (`attestation_chain` required, per-class mismatch counts, halt_reasons enum). **Invariant:** INV-RESEARCH-CROSS-SECTION-ID (added to INVARIANTS.md alongside this phase).

**Quick-mode exemption:** quick is a triage scan; cross-section reconciliation cost exceeds value when the output is "is this candidate worth a real run?" The gate is `skipped` in quick (consistent with the rest of the standard+-only blocking gates).

## Remediation brief addendum (Phase 3.5 iter-2+, 4.25 iter-2+, 4.75 verifier remediation, Phase 6 critique remediation)

**v2 AC2 calibration response to AP-INCOMPLETE-PROPAGATION (S4 Top-3).** Iter-2 remediations in S3/S4 landed corrected values in the obvious place (the bibliography line, the abstracted-cite line) but missed adjacent narrative/tally/self-check lines holding the same value. The defense is mechanical at brief time: every remediation agent dispatched for a corrective iteration MUST include the following terminal step in its brief.

The orchestrator MUST inject this verbatim block into every remediation brief:

```
POST-FIX GREP DISCIPLINE (mandatory before declaring iter-N done)

For each value you corrected:
  1. Record the OLD value (the wrong one you replaced) and NEW value (the correct one).
  2. Run grep for the OLD value across the WHOLE artifact (research-report.md or
     equivalent), case-insensitive, regex-friendly enough to catch trivial
     variants. Use:
         grep -inE '<old-value-regex>' <artifact>
  3. Report every hit found AFTER your correction with line number and 1 line of
     surrounding context.
  4. For each hit: either (a) replace with the NEW value (if it's the same
     instance of the metadata), or (b) annotate why this hit is legitimately
     unchanged (e.g., quoting the prior literature accurately).
  5. Include the grep output + your disposition in your final report under
     `## Post-fix grep audit`. Iteration is NOT done without this section.

Orchestrator will reject the iteration if `## Post-fix grep audit` is missing
or incomplete (any unresolved hit).
```

This block does NOT replace the existing remediation rubric — it's a terminal discipline added to every brief. The orchestrator's attest step refuses the iteration if the agent-source markdown lacks the `## Post-fix grep audit` heading.

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

   **Archive permalink policy (v2 AC4):** archived entries get scoped permalinks so basic-memory's linter does not silently append `-1` suffixes that look like typos in the index.
   - Live compound entry permalink: `a-plus-maxing/compounds/<slug>` (unchanged)
   - Archived compound entry permalink: `a-plus-maxing/compounds/_archive/<slug>-<YYYY-MM-DD>-<reason-slug>` (mirrors the filesystem path `vault/compounds/_archive/<slug>-<YYYY-MM-DD>-<reason-slug>.md` exactly)
   - Live library research-report permalink: `a-plus-maxing/library/<class>s/<slug>/research-report` (unchanged)
   - Archived library research-report permalink: `a-plus-maxing/library/<class>s/<slug>/_archive/<YYYY-MM-DD>-<reason-slug>/research-report`

   The orchestrator MUST rewrite the `permalink:` frontmatter field on every archived file BEFORE the archive move (Phase 2.75 step 4 when `--update` is in effect). Same for any nested layer files (`practitioner-layer.md`, `non-english-layer.md`). If the linter still appends a numeric suffix to a live entry, that signals a stale archive whose permalink was not rewritten — HALT `archive-permalink-collision` and instruct the operator to inspect.

   Decision rationale (S6): basic-memory's auto-suffix is silent corruption — `bpc-157-1` looks like a typo in the live index and degrades searchability. Scoping the permalink to the archive path makes the relationship explicit, matches the filesystem layout, and means the live entry's permalink never has to change.

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

## Canonical provenance directory layout

The research-artifact subdirectories are named **exactly** `gates/`, `judges/`, `sections/` — bare, no prefix — both under the working `${BASE}` (`/tmp/aplus-research/<slug>/`) and when copied into `design/.<slug>-design-work/` for merge provenance (per the design-doc-protocol Phase-0 detail in `design/DESIGN_DOC_TEMPLATE.md`). This is the ONE canonical layout; builders MUST NOT diverge. This section is the single source of truth — other docs reference it rather than restating it.

- `gates/` is the directory `lib/gate_attest.py` reads and writes, and the directory `scripts/audit-research-provenance.sh` (bda) audits for the mode-required attested gates.
- A **prefixed variant** (e.g. `research-gates/`, `research-judges/`, `research-sections/`) is NON-CANONICAL. `gate_attest.py verify-chain` reads bare `gates/`/`judges/`/`sections/`; under a prefixed layout it finds no `gates/` and vacuously passes (checks nothing), while bda rejects the layout outright (INV-RESEARCH-PROVENANCE-DISJOINT). Even genuine `gate_attest.py` artifacts, if committed under prefixed names, are unverifiable in place — the chain only validates after the dirs are renamed canonical.
- Documented non-canonical instance: `supplement-specialist` (PR #14) committed all three artifact dirs under `research-`-prefixed names. The gate chain is genuine `gate_attest.py` output (it validates under `verify-chain` once the dirs are renamed canonical), but the prefix defeats in-place verification and bda correctly rejects it. Grandfathered as build-time scaffolding per the S19 hfm decision; quarantined under bead `0be`. Do NOT replicate it as a build template.

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
| [schemas/gate-4.25.schema.json](./schemas/gate-4.25.schema.json) | Phase 4.25 ID-RECONCILE gate verdict — per-class mismatch counts, halt_reasons enum (v2 AC1) |
| [schemas/gate-4.75.schema.json](./schemas/gate-4.75.schema.json) | Phase 4.75 INTEGRITY gate verdict — 13 IC checks, population_mismatch, concentration_audit, corpus_scoping |
| [schemas/gate-6.schema.json](./schemas/gate-6.schema.json) | Phase 6 CRITIQUE gate verdict — findings, additional_retrievals (max 3) |
| [schemas/gate-7.5.schema.json](./schemas/gate-7.5.schema.json) | Phase 7.5 RISK-FLOOR gate verdict — risk-tier-conditional field requirements |
| [schemas/gate-8.5.schema.json](./schemas/gate-8.5.schema.json) | Phase 8.5 LAYERS gate verdict — practitioner_layer + non_english_layer presence + structure |

**Validation procedure.** Per Hard Rule 9, gate JSONs for phases 3.5/4.75/6/7.5/8.5 MUST be produced by `lib/gate_attest.py attest`, which schema-validates as part of its write path. Schema validation failure → HALT `schema-validation-failed`. The verdict-PASS-but-halt-reasons-non-empty contradiction is mechanically caught by each schema's `allOf` constraint. The verdict-PASS-but-no-attestation-chain contradiction is mechanically caught by `attestation_chain` being a required field in all 5 attested-gate schemas.

## Attestation chain (gate_attest.py)

Built in response to PF-S3-01 (`memory/process-failures.md`): the v1 brief-hash uniqueness substitute for Quant's UUIDv4 identity ledger enforced format, not provenance. The orchestrator self-attested 5 of 6 gates in a single session by writing gate-N.json directly from prose agent reports. The attestation chain is the v1.1 mechanical resistance.

### Workflow per attested gate

For each of phases 3.5, 4.75, 6, 7.5, 8.5:

```bash
# 1. Before dispatching the verifier agent
python3 .claude/skills/aplus-research/lib/gate_attest.py start-iteration \
    --base /tmp/aplus-research/<slug> --phase <N>

# 2. Dispatch the verifier agent. Agent brief must require BOTH:
#    (a) a `## Verdict` block containing `verdict: PASS` or `verdict: HALT`, AND
#    (b) the gate's schema-required STRUCTURED FIELDS as a fenced ```json block in
#        the SAME source file — per `schemas/gate-<N>.schema.json`. Specifically:
#          4.25  entity_classes (citations/institutions/compound_identifiers/
#                regulatory_dates/trial_registrations, each scanned+mismatch_count)
#          4.75  ic_checks IC-1..IC-13 (each a status) + population_mismatch +
#                concentration_audit + corpus_scoping  (run the FULL 13 IC checks
#                from references/citation-integrity.md — not a reduced subset)
#          6/7.5/8.5  their schema-required fields
#        attest uses that ```json block as the scaffold and OVERRIDES only the
#        verdict from the `## Verdict` line (so the orchestrator never composes the
#        gate decision). WITHOUT the block the composed gate fails schema-validation
#        (AR-7, 2026-06-18). (Phase 3.5 is special: judge agents write per-section
#        `judges/judge-<X>.json`.)

# 3. Compose the canonical gate JSON from the agent's markdown
python3 .claude/skills/aplus-research/lib/gate_attest.py attest \
    --base /tmp/aplus-research/<slug> --phase <N>

# 4. (Optional) Verify chain integrity before starting the next phase
python3 .claude/skills/aplus-research/lib/gate_attest.py verify-chain \
    --base /tmp/aplus-research/<slug> --up-to <N>
```

### Halt reasons emitted by gate_attest.py

| Reason | Cause |
|---|---|
| `no-iteration-started` | `attest` called without prior `start-iteration` |
| `missing-agent-source` | `gates/gate-N.md` does not exist |
| `stale-agent-source` | `gates/gate-N.md` mtime ≤ `iter_start_ts` (verifier didn't re-run) |
| `verdict-not-parsable` | No `## Verdict` block with `verdict: PASS\|HALT` |
| `score-not-parsable` | Phase 3.5: judge JSON has no numeric score field |
| `schema-validation-failed` | Composed gate JSON does not satisfy schema |
| `max-iterations-exceeded` | Phase already at iter 3 |

### What this prevents

- Orchestrator transcribing prose agent summaries into gate-N.json (the gate JSON now requires `attestation_chain.agent_source_sha256` which must match the on-disk markdown)
- Orchestrator applying fixes via Edit and then declaring iter-2 PASS without re-dispatching the verifier (mtime check refuses stale agent source)
- Orchestrator manually toggling `verdict: HALT` → `verdict: PASS` after the fact (`attest` parses the markdown's verdict block, not the orchestrator's intent)

### What this does NOT prevent

A determined orchestrator could write a fake `gates/gate-N.md` itself, including a fake `## Verdict: PASS` block; the script would then produce a "valid" gate JSON with attestation_chain referencing the fake markdown. Mitigation deferred to v1.2: the verifier agent brief should include a self-identifying preamble (agent ID, dispatch timestamp from the orchestrator's `dispatch-ledger.jsonl`), and the script should require that preamble.

### Post-hoc audit

`verify-chain` re-reads each `gates/gate-N.md`, recomputes its sha256, and compares against the chain stored in `gates/gate-N.json`. If the markdown was edited after attestation, the sha256 changes and `verify-chain` returns exit code 1 with a per-phase failure list. This catches retroactive edits to agent outputs.

### Smoke tests

`tests/test_gate_attest.py` covers 9 cases: no-iteration HALT, missing-source HALT, stale-source HALT, fresh-PASS attest, orchestrator-lie-overridden, phase-3.5 multi-source composition, phase-3.5 single-judge-HALT propagation, post-attest tamper detection via verify-chain, max-iterations HALT. Run with `python3 tests/test_gate_attest.py`. Exit 0 = all pass.

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
