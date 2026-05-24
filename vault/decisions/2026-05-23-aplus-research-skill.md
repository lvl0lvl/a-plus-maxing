---
title: aplus-research Skill — Project-Local Wrapper for deep-research with Blocking Gates
type: decision
status: active
owner: walter
created: 2026-05-23
last_reviewed: 2026-05-23
depends_on: ["2026-05-23-wiki-schema", "2026-05-23-source-whitelist"]
superseded_by: null
review_cadence: phase (re-rotate after first end-to-end invocation surfaces failure modes)
permalink: a-plus-maxing/decisions/2026-05-23-aplus-research-skill
---

# Decision: aplus-research Skill

## Context

First BPC-157 research dispatch (S2 2026-05-23) declared `/deep-research --mode=deep`. Self-audit after user challenge revealed: zero paired judges dispatched, zero critique agent dispatched, zero refine pass executed, 99/100 rubric threshold never scored against. Effective rigor was closer to standard mode minus Phase 6/7. Section 19 of the produced report initially claimed deep-mode compliance.

Root cause: the global `deep-research` skill states phases prescriptively but does not mechanically enforce them. An orchestrator can declare phase compliance without producing the artifacts that compliance requires. There is no JSON gate verdict that downstream phases refuse to enter without.

Quant solved the analogous problem for its domain with `quant-research`, which wraps `deep-research` and adds Phase 2.75 (Primary Source Manifest Gate) + Phase 4.75 (Citation Integrity Gate), both blocking with machine-readable JSON verdicts. We need the health equivalent.

## Decisions

### 1. Project-local skill at `.claude/skills/aplus-research/`

Not global. Project-scoped because whitelist + templates + operator-profile are health-specific. Companion slash command at `.claude/commands/aplus-research.md`.

### 2. Wraps deep-research, does NOT modify it

Additive only. The global `~/.claude/skills/deep-research/` is untouched. `aplus-research` invokes `deep-research` phases via the Skill tool and inserts gate phases around them.

### 3. Six blocking gates with JSON schema validation

| Gate | Phase | Purpose | Schema |
|---|---|---|---|
| SCOPE | 2.75 | Context-load verified, target identified, no compound-entry overwrite | `schemas/gate-2.75.schema.json` |
| JUDGE | 3.5 | N paired (retrieve + judge) dispatches, all PASS at mode threshold | `schemas/gate-3.5.schema.json` |
| INTEGRITY | 4.75 | 13 IC checks incl per-citation corpus scoping | `schemas/gate-4.75.schema.json` |
| CRITIQUE | 6 | Dispatched red-team agent (deep+ modes only) | `schemas/gate-6.schema.json` |
| RISK-FLOOR | 7.5 | Experimental risk-tier compounds require contraindications + monitoring + stopping criteria + third-party biomarker | `schemas/gate-7.5.schema.json` |
| LAYERS | 8.5 | Practitioner-layer + non-English-layer present (standard+ compound research) | `schemas/gate-8.5.schema.json` |

Each schema includes `allOf` conditional invariants that mechanically reject contradictory PASS+HALT payloads. Smoke-tested S2.

### 4. Three health-specific gates not in deep-research

- **Population-mismatch (Phase 4.75 IC-7):** numerical claims citing animal/in-vitro sources must carry `[population-mismatch: species]` tag
- **Risk-floor (Phase 7.5):** compounds at `risk_tier: experimental` require populated contraindications + monitoring + stopping criteria + third-party monitoring biomarker
- **Concentration-audit (Phase 4.75 IC-9):** single-lab share ≥70% requires first-class section surfacing the risk before any indication subsection

### 5. Per-citation corpus scoping (IC-13)

The structural check that addresses the He L 2022 attribution error (PF-S2-02). For each numerical / quoted claim: fetch the cited primary's full text or abstract, cache at `${BASE}/corpus/<cite_key>.md`, grep claim against corpus. Failure modes: `quote-not-found`, `number-not-found`, `paraphrase-no-token-match`, `corpus-missing`. Sample size scales with mode (skipped in quick / 50% standard / 80% deep / 100% ultradeep).

### 6. Mandatory layers for standard+ compound research

Every compound entry in standard / deep / ultradeep mode produces three artifacts: `research-report.md` + `practitioner-layer.md` + `non-english-layer.md`. Quick mode may skip the supplementary two. Phase 8.5 LAYERS gate enforces presence + structural requirements (each layer has its own bibliography + self-check).

### 7. Quick mode skips integrity + critique gates

Quick exists for triage scans (e.g., "scan a peptide class to pick which candidate to deep-research"). At triage, the integrity gate's cost (corpus retrieval + grep + paraphrase checks) exceeds its value. Scope + judge gates remain mandatory in every mode.

### 8. Goal-agnostic library research distinction

For `target_type ∈ {compound, biomarker, protocol, reference}`: meta files load as context (for linkage) but NOT injected into the research question. Specialist-agent dispatches (different invocation type) inject meta-file content when personalization is the point. Codified in SKILL.md §1.1.

### 9. Auto-loaded project context

Phase 1 mandatorily reads: `vault/meta/operator-profile.md`, `current-state.md`, `goals.md`, `library/_source-whitelist.md`. Missing any → HALT. Sha256 of each file recorded in `gate-2.75.json`.

## Alternatives Considered

- **No project-local skill, just discipline.** Rejected: that's what produced the original BPC-157 failure. Documented protocols without mechanical enforcement get skipped.
- **Build at global scope (`~/.claude/skills/`).** Rejected for v1: whitelist, templates, operator-profile, output paths are health-specific. Project-local lets the skill reference these directly. Promote to global if a second health project ever starts.
- **Use Quant's full machinery (UUIDv4 ledger, corpus sanitization, regression fixtures).** Deferred for v1: each is non-trivial to build right; don't pre-optimize for failures we haven't seen. Brief-hash uniqueness (sha256) substitutes for UUIDv4 in v1. First end-to-end invocation will inform v2.
- **Make critique self-attest by orchestrator instead of dispatched agent.** Rejected: that's exactly what failed in PF-S2-01. The orchestrator self-attested "Phase 6/7 done internally" and shipped. Dispatched-agent critique forces the work to produce an artifact.

## Breaks If

- `jsonschema` Python package not installed (pre-flight check not yet implemented — known limitation)
- Future re-rotation requires overwriting existing compound entries — `--update` flag not yet implemented (Phase 2.75 HALTs on `compound-entry-exists`); first task next session is implementing this
- Paywall bypass exceeds capability — `corpus-missing` WARN expected on meaningful share of cites for paywalled-only primaries
- Critique agent's `additional_retrievals` cap (3) proves too restrictive — adjust in v2 after first end-to-end invocation

## Relations

- [[decisions/2026-05-23-wiki-schema]] (parent — wiki this skill builds entries for)
- [[decisions/2026-05-23-source-whitelist]] (companion — whitelist this skill enforces)
- [[.claude/skills/aplus-research/SKILL.md]] (the skill itself)
- [[.claude/skills/aplus-research/references/health-gates.md]]
- [[.claude/skills/aplus-research/references/citation-integrity.md]]
- [[.claude/commands/aplus-research.md]] (slash command wrapper)
