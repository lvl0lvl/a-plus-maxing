---
description: "Health-domain research wrapping deep-research with mechanically enforced gates (paired judges, type-tag enforcement, population-mismatch / risk-floor / concentration-audit gates, mandatory prescribing-practice + non-English layers)."
argument-hint: "<research question> [--mode=quick|standard|deep|ultradeep] [--target=<class/slug>]"
allowed-tools: Skill, Agent, Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, mcp__basic-memory__write_note, mcp__basic-memory__search_notes
---

# /aplus-research

Invoke the `aplus-research` skill for the argument research question. Skill is project-local at `.claude/skills/aplus-research/`.

## Usage

```
/aplus-research "<research question>" [--mode=quick|standard|deep|ultradeep] [--target=<class/slug>]
```

Default mode: `standard`. Default target: derived from question.

Modes:
- `quick` — 10+ sources, 2,000w, 85/100 judge threshold; layers opt-in
- `standard` (DEFAULT) — 15+ sources, 4,000w, 92/100; layers **mandatory**
- `deep` — 25+ sources, 10,000w, 99/100; layers **mandatory**; full critique + refine
- `ultradeep` — 30+ sources, 15,000w, 99/100; layers **mandatory**; extended critique

## Project context auto-loaded (Phase 1)

- `vault/meta/operator-profile.md` (slow-changing)
- `vault/meta/current-state.md` (snapshot)
- `vault/meta/goals.md` (hard limits)
- `vault/library/_source-whitelist.md` (admissibility rules)

Missing any → HALT `context-load-missing`.

## Gates (all blocking)

1. **Phase 2.75 SCOPE GATE** — context-load verified, target identified, no compound-entry overwrite
2. **Phase 3.5 JUDGE GATE** — N paired judges dispatched and PASS
3. **Phase 4.75 INTEGRITY GATE** — type-tag enforcement + population-mismatch + concentration-audit + route-extrapolation
4. **Phase 6 CRITIQUE GATE** (deep/ultradeep) — separate dispatched red-team agent
5. **Phase 7.5 RISK-FLOOR GATE** (compounds) — experimental risk-tier requires contraindications + monitoring + stopping criteria + third-party monitoring biomarker
6. **Phase 8.5 LAYERS GATE** (standard+ compound) — practitioner-layer + non-English-layer present

## Output paths

| Target type | Research artifacts | Entity entry |
|---|---|---|
| Compound | `vault/library/<class>s/<slug>/research-report.md` + `practitioner-layer.md` + `non-english-layer.md` | `vault/compounds/<slug>.md` |
| Biomarker | `vault/library/biomarkers/<slug>/research-report.md` | `vault/biomarkers/<slug>.md` |
| Protocol | `vault/library/protocols/<slug>/research-report.md` | `vault/protocols/<slug>.md` |

## Re-rotation

Future use of `--update` flag (not yet implemented) will permit overwrite of existing compound entries for re-rotation events (e.g., FDA PCAC July 23-24, 2026 outcome for BPC-157).

## Reference

Full skill spec: `.claude/skills/aplus-research/SKILL.md`. Health gates: `.claude/skills/aplus-research/references/health-gates.md`. Citation integrity verifier brief: `.claude/skills/aplus-research/references/citation-integrity.md`.
