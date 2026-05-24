---
title: Session 2 — Wiki Schema + BPC-157 + aplus-research Skill
type: session
status: complete
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
depends_on: ["session-1"]
superseded_by: null
review_cadence: manual
permalink: a-plus-maxing/sessions/session-2
---

# Session 2 — Wiki Schema + BPC-157 + aplus-research Skill (2026-05-23)

Second working session. Three structural builds plus one library entry produced as both an exercise and a calibration case for the skill that came out of it.

## Scope (executed)

1. Karpathy-style wiki schema layered onto the existing operational vault
2. Agent roster + Prescribing-Practice Layer concept added to schema
3. First compound library entry (BPC-157) end-to-end
4. Two supplementary dispatches on BPC-157 (prescribing-practice + non-English literature) that surfaced an author-attribution error in the primary report
5. `aplus-research` project-local skill v1 with 6 blocking gates, then tightened with corpus scoping + JSON schemas + mode-aware gate skipping

## Key artifacts produced

- `vault/WIKI.md` — schema with 14-agent consumer roster + cross-cutting rules
- `vault/meta/{operator-profile,current-state,goals,contradictions,log,index}.md` — agent-shared context layer
- `vault/library/_source-whitelist.md` — 5-tier whitelist + Tier 2.7 (practitioner_protocol) + Tier NE (non-English) + 12-tag enum + admissibility matrix
- `vault/library/peptides/_triage.md` — peptide class taxonomy + scoring rubric
- `vault/library/peptides/bpc-157/{research-report,practitioner-layer,non-english-layer}.md` — first compound library entry
- `vault/compounds/{_template,bpc-157}.md` — compound template with mandatory Prescribing-Practice Layer + Non-English Literature Coverage sections
- `vault/biomarkers/_template.md`
- `.claude/skills/aplus-research/SKILL.md` + 2 reference files + 6 JSON schemas
- `.claude/commands/aplus-research.md`

## What worked

- **Wiki schema landed cleanly** as a layer on top of the operational vault — entities (compounds, biomarkers, protocols, parameters, decisions) + meta files + agent roster. The split between `vault/library/<class>s/<slug>/` (research artifacts) and `vault/compounds/<slug>.md` (flat entries) holds up.
- **Parallel agent dispatches for BPC-157** (5 retrieval + 2 supplementary) produced substantive coverage. Cross-section concordance check caught zero auto-fails.
- **Supplementary non-English dispatch caught the He L 2022 attribution error** that the original retrieval missed — fortunate byproduct of language-survey methodology, logged to `meta/contradictions.md` as resolved.
- **JSON schema invariants demonstrably block contradictions** — smoke-tested 6 representative bad payloads, all rejected (contradictory PASS+halt; PASS with loaded=False; PASS with judge HALT; experimental PASS without third-party marker).

## What did NOT work — see process-failures.md

`memory/process-failures.md` entries PF-S2-01 through PF-S2-04 added.

## Drift checks

### Task drift
- Original scope evolved through user direction. Started: "is the LLM wiki set up?" Ended: shipped the wiki schema + first compound entry + the wrapper skill that should have been used to produce that entry. Scope expansion was user-directed at each step.

### Architecture drift
- No INVARIANTS.md exists yet for this project. The closest project invariants are in CLAUDE.md (Cross-Document Ownership Matrix + rotation rule). All work this session honored those: each new fact lives in exactly one document; volatile sections respect the rotation rule.

### Vision drift
- Project remains: LLM-driven personal health agent (Bryan Johnson Blueprint, low-budget), markdown substrate + HTML on demand, A→B→C phased build, evidence-driven. After this session, the system IS: an LLM-driven personal health agent with a queryable knowledge base, an agent roster designed but not yet built, and a research wrapper skill with mechanically enforced gates. Same project; capability deepened.

## Next session

User explicitly stated: **re-run BPC-157 via `/aplus-research --mode=deep`** because the original run did not follow protocol and is suspected to contain hallucinations, fabrications, and false citations. The IC-13 corpus scoping check is specifically designed to catch this.

Re-run will need an `--update` flag to permit overwrite of the existing `vault/compounds/bpc-157.md` entry — this is documented as not-yet-implemented in SKILL.md Known Limitations. First-task next session is implementing `--update` flag handling before the re-run can proceed.

## Confidence + notes

- The skill exists on disk but has never been invoked end-to-end. Next session's re-run is the actual smoke test.
- Sikiric-dominance and PL 14736 publication-bias findings are robust regardless of any per-claim fabrications in the original report; those structural findings rest on cluster counts and registry queries, not on individual claim verification.
- Three commits ahead of origin/main; hooks block push to main per project convention.
