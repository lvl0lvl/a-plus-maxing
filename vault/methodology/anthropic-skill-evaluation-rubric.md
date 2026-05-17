---
title: anthropic-skill-evaluation-rubric
type: rubric
permalink: a-plus-maxing/methodology/anthropic-skill-evaluation-rubric
owner: Walter McGivney
created: 2026-05-16
last_reviewed: 2026-05-16
status: active
depends_on: []
superseded_by: null
review_cadence: phase
tags:
- rubric
- methodology
- upgrade-skill
---

# Anthropic Skill Evaluation Rubric

## Purpose

This rubric scores a Claude Code skill (slash command + supporting references and regression artifacts) against ten dimensions of skill quality, on a 0-10 scale per dimension. It is the source of truth for `/upgrade-skill` Phase 1 baseline scoring and Phase 2 rubric construction. It is consumed by skill authors, by upgrade-skill judges, and by adversarial reviewers in Phase 6. It is intentionally mechanical: every dimension carries greppable, file-existence, or shell-runnable checks so that two reviewers scoring the same skill arrive at the same number ±1. A skill scores as "ready" only when every dimension is at 9 or 10. Anything below 9 on any dimension is a research target for the upgrade pipeline.

## Scoring Scale

| Score | Label | Anchor |
|-------|-------|--------|
| 0 | Absent | The dimension is not addressed at all. The skill cannot be evaluated against this dimension because the artifact, section, or check that the dimension measures does not exist. |
| 5 | Sketched | The dimension is addressed in narrative prose but lacks the mechanical artifacts that make it enforceable. A reviewer could form an opinion but two reviewers would disagree by 2+ points. |
| 7 | Functional | The dimension is addressed with at least one mechanical check and at least one concrete example. There are visible gaps (missing edge cases, missing recovery paths, partial coverage) but the skill works on the happy path. |
| 9 | Ready | All mechanical checks pass. Edge cases and recovery paths are documented. The dimension is internally consistent with the rest of the skill. Two reviewers agree to within 1 point. Minor polish opportunities remain. |
| 10 | Exemplary | The dimension is a reference example that other skills should copy. Every check is mechanical, every failure mode is named, every example is tested, and the artifact has been validated against at least one real run that exercised the dimension's edge cases. |

The skill PASSES `/upgrade-skill` only when every dimension scores 9 or higher. A single dimension below 9 holds the entire skill below the bar regardless of the average.

## Dimensions

### 1. Identity & Purpose

What this dimension measures: whether the skill states clearly what problem it solves, who calls it, and the explicit boundary between when-to-use and when-not-to-use.

Anchors:
- 0: No identity statement. The command file opens with mechanics.
- 5: One-line description, no when-not-to-use.
- 7: Multi-paragraph identity, when-to-use enumerated, when-not-to-use sketched.
- 9: Identity, when-to-use, when-not-to-use all enumerated. At least three concrete trigger phrases. At least three explicit non-triggers (sibling skills that should be called instead).

Mechanical checks:
- `rg -c "^## (Identity|Purpose|When to use|When not to use)" <command>.md` returns ≥ 3.
- `rg -c "When (NOT|not) to use" <command>.md` ≥ 1.
- Identity section is one of the first three top-level sections (line number of `## Identity` < 200).
- At least one cross-reference to a sibling skill (`/<other-skill>`) with explicit "use that instead when X" language.

Common defects:
- Missing "when NOT to use" section; users invoke the skill on the wrong inputs.
- Identity section duplicates the YAML `description` rather than expanding it.
- No sibling-skill disambiguation; two skills overlap on the same trigger.
- Trigger phrases are abstract ("when investigating") rather than verbatim ("when the user says 'why is this slow'").

### 2. Content Organization

What this dimension measures: whether the orchestrator file is lean and progressive disclosure routes detail to references that load on demand.

Anchors:
- 0: Single file >10000 words; references not used.
- 5: References exist but orchestrator duplicates their content.
- 7: References exist; orchestrator file ≤ 5000 words; some duplication.
- 9: Orchestrator ≤ 4000 words. References loaded only when the relevant phase fires. Zero verbatim duplication between orchestrator and any reference.

Mechanical checks:
- `wc -w <command>.md` ≤ 5000 (target ≤ 4000 for ≥9).
- `wc -l <command>.md` ≤ 800.
- `ls references/` is non-empty for any non-trivial skill.
- `rg -f <reference-headings>.txt <command>.md` returns 0 (no reference content duplicated in orchestrator).

Common defects:
- Orchestrator file >5000 words; first read blows the budget for the actual task.
- References duplicate orchestrator content; both go stale independently.
- All references loaded eagerly on every invocation regardless of phase.
- Orchestrator buries the entry-point under several preamble sections.

### 3. Resource Completeness

What this dimension measures: whether every artifact the skill claims to need actually exists at the cited path: references, examples, validation checklists, regression suites.

Anchors:
- 0: Skill cites `references/foo.md` and the file does not exist.
- 5: Most cited paths exist; one or two stubs.
- 7: All cited paths resolve. Regression directory is empty or has fixtures only, no runner.
- 9: All cited paths resolve. Regression suite includes fixtures + runner script + expected-output snapshots. At least one example per phase.

Mechanical checks:
- For every path of the form `references/*.md` mentioned in the command, `test -f` succeeds.
- `ls regression/` contains at least one runnable script (`*.sh` or `*.py`) and at least three fixtures.
- `bash regression/<runner>.sh --help` exits 0.
- Every numbered phase in the command has at least one worked example in `examples/` or inline.

Common defects:
- `references/` directory empty or contains only README.
- Cited path uses an old name after a rename; the file moved but the citation did not update.
- Regression fixtures present but no runner; tests are not actually runnable.
- Examples missing for the phases that fail most often (typically Phase 4 / Phase 6).

### 4. Edge Case Coverage

What this dimension measures: whether the skill names the failure modes it expects to encounter and prescribes behavior for each.

Anchors:
- 0: Happy path only. No mention of partial states, retries, or recovery.
- 5: One or two edge cases named (e.g., empty input) but no recovery procedure.
- 7: 5+ edge cases enumerated with HALT-vs-continue routing.
- 9: 8+ edge cases with explicit handler. Every HALT condition specifies the resume protocol. At least one compaction-recovery procedure documented.

Mechanical checks:
- `rg -c "^### Edge Case|^### Failure Mode" <references>/*.md` ≥ 5.
- `rg -c "HALT|halt-and-resume|RESUME after" <command>.md <references>/*.md` ≥ 3.
- At least one edge-case fixture in `regression/` per documented edge case.
- `rg "compaction|context window|resume" <command>.md` returns ≥ 1 hit.

Common defects:
- No HALT specs; agents don't know when to stop versus continue.
- No recovery-after-compaction procedure; long-running skills cannot survive a compaction event.
- Edge cases listed in prose without corresponding regression fixtures.
- Partial-state behavior unspecified (skill ran 4 of 8 phases — what does the next session do?).

### 5. Verification & Testing

What this dimension measures: whether acceptance criteria are mechanical (greppable, executable, file-existence) rather than judgment-based.

Anchors:
- 0: No ACs, or ACs are subjective ("the output should be high quality").
- 5: ACs exist but mix mechanical and judgment-based; no AC checker script.
- 7: ACs are mechanical; AC checker script exists but is not run by the skill itself.
- 9: AC checker exits 0/non-zero based on every documented AC. Smoke test runs in <60s. Dry-run mode supported. Every AC has a regression fixture demonstrating both pass and fail behavior.

Mechanical checks:
- `test -f regression/ac-check.sh` (or equivalent) and the script's count of checks equals the count of `^- AC-` lines in the command.
- `bash regression/ac-check.sh` exits 0 against the canonical good fixture.
- `bash regression/ac-check.sh` exits non-zero against the canonical bad fixture.
- `rg -c "AC-[0-9]+" <command>.md` ≥ 10 for non-trivial skills.

Common defects:
- ACs rely on judgment ("the report is well-organized") rather than mechanics.
- AC checker exists but is not wired into Phase 8 or any HALT condition.
- No smoke test; only the full pipeline can be exercised.
- ACs in the command file don't appear in the checker, or vice versa.

### 6. Anti-Pattern Coverage

What this dimension measures: whether the skill explicitly documents the failure patterns endemic to its domain and prescribes guards against them.

Anchors:
- 0: No anti-pattern section.
- 5: One or two anti-patterns mentioned in passing.
- 7: Dedicated anti-pattern section with 3-5 patterns, each named.
- 9: 6+ anti-patterns. Each names the failure pattern, the symptom, the guard, and a concrete example from a prior session. At least one anti-pattern is enforced mechanically (regex/check) rather than narratively.

Mechanical checks:
- `rg -c "^### Anti-Pattern|^## Anti-Patterns" <command>.md <references>/*.md` ≥ 1.
- Anti-pattern section enumerates ≥ 6 patterns.
- At least one anti-pattern has an associated regex check in `regression/` or a HALT clause in the command.
- At least one anti-pattern cites a session ID or PR number where the pattern actually fired.

Common defects:
- Silent self-classification of findings as non-blocking (the agent decides its own work passes).
- Rewriting working code as review feedback instead of flagging.
- Tests written against the current broken state (tautological tests).
- "Defensive programming" added without justification.
- Affirmation openers ("Great", "Absolutely") that signal sycophancy.

### 7. Internal Consistency

What this dimension measures: whether the command, references, examples, and regression suite tell the same story without contradicting each other.

Anchors:
- 0: Command lists 8 phases; references describe 6.
- 5: Names match but counts and orderings drift.
- 7: Counts match; some terminology drift between command and references.
- 9: Counts, names, ordering, and ACs are identical across all artifacts. A grep for any AC ID returns the same count in command and checker. Phase names are byte-identical.

Mechanical checks:
- `rg -c "^## Phase " <command>.md` equals the phase count cited in references.
- For every `AC-N` in the command, the same `AC-N` appears in `regression/ac-check.sh`.
- `rg "Phase [0-9]+" <command>.md | sort -u` matches `rg "Phase [0-9]+" <references>/*.md | sort -u`.
- No two artifacts give different counts for the same enumerable thing (phases, ACs, anti-patterns, dimensions).

Common defects:
- ACs in §14 don't appear in the command body; checker drifts from spec.
- Reference says "8 phases" but command has 9.
- Phase named `Phase 4 - Validation` in command, `Phase 4: Validate` in reference.
- Two references disagree on the same parameter value.

### 8. External Cross-References

What this dimension measures: whether every external citation (paths, line numbers, tool names, ADR numbers, vault notes) actually resolves at the cited target, today.

Anchors:
- 0: Links and paths are unverified; many are dead.
- 5: Paths resolve; line numbers stale.
- 7: Paths and section anchors resolve; tool versions unpinned.
- 9: All paths resolve. All section anchors resolve. Every cited tool has a pinned version or "any version that supports flag X" guard. Every ADR/vault citation resolves to a file that exists. Line-number citations include a verification command.

Mechanical checks:
- For every path in the command, `test -e <path>` succeeds.
- For every `<file>:<line>` citation, the line still contains the expected text (regex check).
- For every tool invoked (e.g., `rg`, `gh`, `bd`), there is a version constraint or a feature-detection guard.
- Every `vault/<x>` and `docs/adr/<n>` citation resolves to an existing file.

Common defects:
- Line numbers cited but file changed; reader follows a stale anchor.
- Tool versions unpinned; `gh` flag works for one user, fails for another.
- ADR cited by number but the ADR was renamed.
- Vault note paths missing the `quant/` project prefix.

### 9. Failure Handling & Recovery

What this dimension measures: whether the skill degrades gracefully when its inputs, tools, or environment are partly broken, and whether work-in-progress can be resumed.

Anchors:
- 0: Tool unavailable → skill aborts with no guidance.
- 5: One fallback documented; no resume protocol.
- 7: Fallbacks for the most likely failures; partial resume possible but not specified.
- 9: Every external dependency has a documented fallback or a clean HALT. Every long-running phase has a resume protocol that can pick up after a compaction or restart. Failure modes are enumerated with handler IDs (FM-1, FM-2, ...).

Mechanical checks:
- `rg -c "^### FM-[0-9]+|^### Failure Mode" <references>/*.md` ≥ 5.
- For every Tier-1 dependency (binary, network endpoint, file path), there is a fallback or a HALT clause.
- `rg "resume|RESUME|after compaction" <command>.md <references>/*.md` ≥ 1.
- At least one regression fixture exercises a tool-unavailable scenario.

Common defects:
- No graceful degradation when a tool is unavailable; skill HALTs with stack trace instead of a recoverable message.
- No resume-after-compaction procedure; a 2-hour skill that compacts at 90 minutes loses everything.
- Fallback documented but never tested; the fallback path itself is broken.
- HALT message points the user at a runbook that does not exist.

### 10. User Communication

What this dimension measures: whether the skill specifies what the user sees at each phase, in what format, with what calibration.

Anchors:
- 0: Output format unspecified; the user sees whatever the agent writes.
- 5: Final report format specified; intermediate output free-form.
- 7: Output format specified at every phase boundary; no calibration examples.
- 9: Every user-visible output has a template, a worked example showing pass/fail/partial, and a length budget. Confidence statements have calibration tables. Every HALT message specifies what the user must do next.

Mechanical checks:
- `rg -c "^### Output|^### User Sees|^## Output Format" <command>.md <references>/*.md` ≥ 3.
- At least one calibration example per dimension where the skill emits a numeric judgment.
- Every HALT clause specifies a "next action for the user" line.
- Length budgets cited for every long-form output (e.g., "report 800-1200 words").

Common defects:
- Output format unspecified; one run produces a table, the next produces prose.
- Confidence numbers ("85%") emitted with no calibration anchor.
- HALT message says "fix the issue" with no specifics.
- Long-form outputs have no length budget; reports drift to 5000 words.

## Pass Threshold

A skill passes `/upgrade-skill` when **every dimension scores 9 or higher** at the end of the upgrade cycle. The average is irrelevant; a single dimension at 8 fails the gate. Each dimension below 9 in Phase 1 baseline becomes a research target for Phase 2 (rubric construction) and a candidate finding for Phase 6 (adversarial review). The Phase 4 fact-checker / judge pair re-scores after Phase 3 fork. The Phase 7 refine loop closes findings until the next Phase 4 re-score returns ≥ 9 on every dimension.

A passing skill must additionally satisfy:
- All mechanical checks above succeed (no exceptions for "minor").
- At least one full end-to-end dry-run in regression/ exits 0.
- Phase 6 adversarial review found 0 CRITICAL findings unaddressed.

## How to Use

**Phase 1 baseline scoring (`/upgrade-skill`).** Read every artifact of the candidate skill: the command file, every reference, every example, the regression directory. Score each dimension 0-10 against the anchors above, applying every mechanical check. Record the score, the failed checks, and one sentence of evidence per dimension. Dimensions below 9 become the research targets for Phase 2.

**Phase 2 rubric construction.** For each dimension below 9, construct a domain-specific sub-rubric that operationalizes the generic anchor at 9 and 10 for the specific skill being upgraded. Example: dimension 4 "Edge Case Coverage" at 9 demands 8+ edge cases — for `/quant-research`, list the 8 expected edge cases (network failure during fetch, marker timeout, FRED 3-year cap, paywall, etc.). The Phase 2 sub-rubrics drive Phase 3 fork content.

**Phase 4 re-scoring.** After Phase 3 fork, dispatch a fact-checker and a judge per dimension. Each agent re-runs the mechanical checks, applies the anchors, and emits a score with evidence. The skill enters Phase 7 refine if any dimension scores below 9. The skill enters Phase 8 deploy if every dimension is ≥ 9 AND Phase 6 adversarial findings are closed.

**Phase 6 adversarial review.** The adversarial reviewer uses the "Common defects" lists above as a checklist, hunting for each defect in the candidate skill. Every defect found becomes a Phase 6 finding with severity (CRITICAL / HIGH / MEDIUM / LOW) and a fix recipe. CRITICAL findings block Phase 8 deploy.

**Authoring new skills.** Read this rubric before drafting a skill. Each dimension's mechanical checks list is the minimum viable structure for the corresponding section. A skill that does not pass this rubric on first authorship is faster to fix during authorship than to upgrade later.