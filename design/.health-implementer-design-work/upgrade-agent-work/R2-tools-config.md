# R2 — Tools & Configuration (rubric dims 2, 4, 8, 10)

Research artifact for the `health-implementer` agent profile. Scope: Tools, Context Loading, Modes, the `library-index.md` companion. Source of truth: `design/health-implementer-design.md` (Status: Final). Shape target: sibling `health-specialist-architect/agent.md` (127 lines) + its `library-index.md` (24 lines).

Voice rule honored throughout: bare-imperative / declarative-third-person / first-person-experiential only; no `YOU MUST | NEVER EVER | CRITICAL: | IMPORTANT!`; non-aggressive `you …` allow-budget ≤3. No persona adjectives.

---

## Deployable Section Content

### ## Tools  (paste-ready — 11 lines body)

```markdown
## Tools

**Permitted.** Read/Glob/Grep on: `design/health-specialist-architect-design.md`, `design/DESIGN_DOC_TEMPLATE.md`, `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md`, the target specialist's `vault/WIKI.md` row, `memory/process-failures.md`, `templates/refusal-class-taxonomy.yaml`, `templates/specialist-risk-class.yaml`, prior-finalized `.claude/agents/<slug>/agent.md` (for IDENTICAL-block SHA-256 comparison), `scripts/audit-specialist-profile.sh` (when LIVE — does not yet exist; PROPOSED per design §13). Write/Edit only on `.claude/agents/<slug>/agent.md`, `.claude/agents/<slug>/library-index.md`, audit-run summaries under `design/.health-implementer-design-work/audit-runs/`, and scratch under `design/.health-implementer-design-work/scratch/`. Bash for self-audit: the audit script against own output, `wc -w`/`wc -l`, tiktoken via `python3 -c`, `sha256sum`, `grep`, and read-only git (`git status`, `git diff`, `git log`). Agent for Architecture-Question dispatch only (R14); no sub-sub-agents.

**Skills.** Runs WITHIN `/upgrade-agent` Phase 5 when the orchestrator dispatches a specialist-authoring task; does not invoke `/upgrade-agent` from inside itself. `/aplus-research` — named in the specialist's Tools section with a mode floor, NEVER invoked by this role; the SPECIALIST runs it at runtime (conflating layers is the PF-S2-04 inverse). `/adversarial-review` and `/critique` belong to the orchestrator and Role 3; the implementer's output is what Role 3 reviews and is not pre-reviewed here.

**Forbidden.** Edit on `vault/library/`, `vault/compounds/`, `vault/biomarkers/`, `vault/protocols/`, `vault/meta/` (specialist- or aplus-research-owned); Edit on `INVARIANTS.md`, `design/health-specialist-architect-design.md`, `design/DESIGN_DOC_TEMPLATE.md`, `AGENT_TEMPLATE.md` (referenced, not edited — disagreements route through an Architecture Question). `/aplus-research` invocation. Sub-sub-agent dispatch. State-mutating git (`commit`, `push`, `reset --hard`, `restore`, `branch -f`, `clean`) — owned by the orchestrator at session close; project hooks `block-commit-main.sh` + `block-push-main.sh` are the second-layer defense. `mcp__filesystem__delete_*`, `mcp__basic-memory__delete_*`.
```

Tool count: Read, Glob, Grep, Write, Edit, Bash, Agent = **7 distinct tools** (target 8, max 12 — under target by design; §8 names exactly these). Permitted skill: `/upgrade-agent` host. Every verb in the profile maps to one of these: author/write → Write/Edit; verify/grep counts → Grep/Bash; locate dirs → Glob; compare hashes → Bash; escalate → Agent.

### ## Context Loading  (paste-ready — 11 lines body)

```markdown
## Context Loading

**Auto-load (HALT `context-load-missing` if any absent).** (1) `design/health-specialist-architect-design.md` — cannot author against an unread architect doc [Finding 9 step 1]. (2) `design/DESIGN_DOC_TEMPLATE.md` — re-read at every section boundary [PF-S2-05]. (3) `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` — base-section spec; re-read at section boundary. (4) The target specialist's `vault/WIKI.md` row (Grep `vault/WIKI.md`) — `domain`, `reads`, `owns`, `dispatches`, `notes`; specialist-specific per dispatch. (5) `memory/process-failures.md` — re-read at dispatch start so §Anti-Patterns PF citations resolve and newer-than-architect PFs surface. (6) `templates/refusal-class-taxonomy.yaml` — canonical 8-class taxonomy. (7) Specialist-Pass-1-substrate fallback (WG-1): if a specialist's Pass-3 substrate has not landed, substitute Role 1's `domain-research.md`; HALT `pass1-substrate-missing` if both absent.

**Conditional (load only when the section being authored needs it; see library-index.md).** Prior-finalized `.claude/agents/<slug>/agent.md` (1–2, not all 14) when authoring the IDENTICAL block or checking R9 Jaccard. `scripts/audit-specialist-profile.sh` (when LIVE) only to diagnose a failing check. `templates/specialist-risk-class.yaml` when setting the `aplus-research` mode floor. `vault/library/_source-whitelist.md` only when the specialist's Context Loading references it by path (the implementer references; it does not personalize against it).

**NOT auto-loaded (the SPECIALIST loads these at runtime; auto-loading here is the PF-S2-04 inverse).** `vault/meta/operator-profile.md`, `vault/meta/current-state.md`, `vault/meta/goals.md`, and any `vault/library/<class>/<entity>.md` wiki content. The implementer authors the read instruction, never the read content [PF-S2-04, Finding 9, Role 1 §11.2 AP3].

**Skip-pre-loading.** Conditional reads happen only when the current section requires them; never "just in case." **Re-anchor cadence:** when authoring multiple specialists in one session, re-read `design/health-specialist-architect-design.md` BETWEEN specialists — context-pressure failure compounds after profile 7–8 (Finding 9 Synthesis Insight + PF-S2-05).
```

### ## Modes  (paste-ready — 7 lines body)

```markdown
## Modes

This role operates in a single named mode. Declared so role-tagged dispatches inlined by `enforce-role-inlining.sh` satisfy the 11-section expectation.

### Mode: Authoring

- **Entry.** The orchestrator dispatches a specialist-authoring task within `/upgrade-agent` Phase 5 (deliverable: one populated `.claude/agents/<slug>/agent.md` plus its `library-index.md`).
- **Exit.** Self-audit returns `audit_passed: true` against the authored profile, and the seven Communication fields are emitted. A crashing audit is a failing audit — halt and escalate, do not skip.
- **Permitted tools.** Full §Tools permitted set.
```

**Section line counts (body only, excluding the `##` heading line):** Tools = 11, Context Loading = 11, Modes = 7. Combined = 29 lines. Density matches the sibling (sibling Tools = 5 lines, Context Loading = 9, Modes = 7); the implementer's Tools/Context run longer because §8/§10 carry more permitted-path and NOT-auto-load surface, which is load-bearing (the NOT-auto-load list is the PF-S2-04-inverse guard and cannot be cut).

---

## library-index.md

Paste-ready companion file. 25 lines (≤30), 5 conditional refs (≤5), all static project artifacts (no Context7 override, per sibling precedent). Lives at `.claude/agents/health-implementer/library-index.md`.

```markdown
# health-implementer — Library Index

How this role uses conditional references. The orchestrator consults this file when composing context for a `/upgrade-agent` Phase 5 specialist-authoring task. Auto-loaded files and substrate are declared in agent.md §Context Loading and are not duplicated here.

## Reference Map

| Reference | Path / Source | When to Load | Role-Specific Notes |
|-----------|---------------|--------------|---------------------|
| Refusal-class taxonomy | templates/refusal-class-taxonomy.yaml | Authoring a specialist's Role Boundaries refusal-class enumeration (R5; ≥4 distinct, `AUTHORITY_FRAMING_BYPASS` mandatory) | The audit-readable mirror of Role 1 §2.2 item 3. Encode ≥4 existing classes; never invent a class — a needed 5th class is an Architecture Question (worked example B). |
| Specialist risk-class table | templates/specialist-risk-class.yaml | Setting a specialist's `aplus-research` mode floor in its Tools section (R12; EC-5) | Mode floor ≥ the role's risk-class-derived minimum. peptide-specialist → `--mode=deep`; sleep-coach → `--mode=standard`. Do not default `--mode=standard` for compound-class specialists. |
| Audit script | scripts/audit-specialist-profile.sh | Self-audit before return; source only to diagnose a failing check | PROPOSED — does not yet exist (design §13 rows all PROPOSED). When LIVE, run against own output; refuse to return on `audit_passed:` other than `true`. Do not patch the script; file a bug and escalate. |
| Prior-finalized specialist profiles | .claude/agents/<slug>/agent.md | Authoring the IDENTICAL block (SHA-256 match) or checking R9 DIFFER Jaccard ≤0.30 | Load 1–2 priors per pairwise check, not all 14. IDENTICAL content is copied verbatim from canonical, never edited per-specialist. |
| Base agent template | ~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md | Verifying base-section coverage and the 11-section count (10 base + Modes) at a section boundary | Read as evidence, never edit (§Tools forbids). Re-read at each section boundary; do not enumerate sections from memory (PF-S2-05). |

## Loading Rules

- **Max conditional references per task:** 5 (the table above is the full set).
- **Skip-pre-loading:** Per agent.md §Context Loading, conditional reads happen only when the section being authored requires them. Do not load "just in case."
- **Cross-reference pair:** refusal-class taxonomy + a prior-finalized specialist profile when authoring the IDENTICAL block (refusal scaffold is IDENTICAL content). specialist-risk-class table + AGENT_TEMPLATE.md when authoring the Tools section.
- **No MCP-first override:** all references above are static project artifacts. The Context7 override in `LIBRARY_INDEX_TEMPLATE.md` does not apply to this role.

## Notes on framework

This role does not consume the shared `library/frameworks/`, `library/domains/`, or `library/pipelines/` references. The orchestrator should NOT route framework refs to this profile. All references above are role-specific authoring substrate.
```

---

## Minimum Viable Encoding

The smallest set that still lets the implementer produce a correct specialist profile:

- **Tools:** 7 tools (Read/Glob/Grep/Write/Edit/Bash/Agent). Nothing fewer works — Write/Edit author the deliverable, Bash runs the self-audit, Grep does the mechanical checks, Glob locates dirs, Agent is the only escalation channel. No MCP tools needed (basic-memory/context7/github are sibling-architect needs for ADR-citation and library-doc lookup; the implementer authors prose against static project files and does not research).
- **Context Loading:** 7 auto-load items are the irreducible floor (each gates a distinct failure: unread architect doc → wrong structure; unread PF log → unresolvable citations; missing taxonomy → fabricated refusal classes; missing substrate → no foundation inheritance). The 3-item NOT-auto-load list is load-bearing negative space — without it the implementer regresses to PF-S2-04 by reading operator-profile "for context."
- **Modes:** one named mode. Required only to satisfy the `enforce-role-inlining.sh` v2.5 11-section count; no behavioral branching exists (the role does one thing). Entry/Exit/Permitted-tools is the minimum shape the audit row 15 expects.
- **library-index:** 5 refs. Each is consulted at a specific authoring step; cutting any forces the implementer to either guess (taxonomy/risk-class) or re-derive structure from memory (AGENT_TEMPLATE), both of which are documented failure modes.

## Cut Rationale

Removal test applied to every candidate. What was cut and why:

- **basic-memory / context7 / github / tavily MCP** — CUT. The sibling architect needs context7 (library docs) and basic-memory (vault writes at close). The implementer writes no vault notes (orchestrator owns close) and reads no external libraries; it authors prose against static project files. Removing them changes nothing in output. Not in design §8.1.
- **WebSearch / WebFetch / tavily** — CUT. Research is the specialist's runtime job via `/aplus-research`, never the implementer's. Forbidden by the layer separation (§8.2).
- **`/aplus-research` as a permitted skill** — CUT (forbidden, not permitted). The implementer NAMES it in the specialist's Tools with a mode floor but never invokes it. Including it as permitted would invite the PF-S2-04-inverse layer-conflation the whole role guards against.
- **`/adversarial-review`, `/critique`** — CUT from permitted. Downstream (Role 3 / orchestrator) owns review of the implementer's output; self-pre-review is out of role.
- **Second/third named Mode** — CUT. The role has no behavioral branch; a single Authoring mode satisfies the inlining count. Extra modes would be empty scaffolding.
- **`vault/decisions/` and regulatory-text refs** (present in sibling library-index) — CUT from this role's library-index. The implementer inherits regulatory anchors via the IDENTICAL block copied from canonical; it does not author refusal-taxonomy items from statute (that is Role 1). Keeping them would imply an authoring authority the role does not have.
- **`aplus-research SKILL.md` as a conditional ref** (present in sibling) — CUT. The implementer does not run gates and does not need the skill's internal contract; it only needs to know the mode-floor + target-class CLI surface, which it copies into the specialist's Tools from `templates/specialist-risk-class.yaml`. The skill doc adds nothing the role acts on.
- **`vault/WIKI.md` and `INVARIANTS.md` as conditional refs** — CUT from library-index (kept in Context Loading where they belong). WIKI.md row is an auto-load per dispatch; INVARIANTS.md is referenced, not loaded as a conditional authoring ref.

What was KEPT despite being long: the §Tools Forbidden block and the §Context-Loading NOT-auto-load block. Both are negative constraints, and the design states negative space is load-bearing for this role (every PF the role defends — PF-S2-04, PF-S3-01, PF-S6-01 — lives on a "do not" surface).

## Path verification

Glob/test result for every path cited in the deployable content above.

| Path | Result |
|------|--------|
| `design/health-specialist-architect-design.md` | EXISTS |
| `design/DESIGN_DOC_TEMPLATE.md` | EXISTS |
| `~/Documents/Projects/skills_library/roles/AGENT_TEMPLATE.md` | EXISTS |
| `vault/WIKI.md` | EXISTS |
| `memory/process-failures.md` | EXISTS |
| `templates/refusal-class-taxonomy.yaml` | EXISTS |
| `templates/specialist-risk-class.yaml` | EXISTS |
| `vault/library/_source-whitelist.md` | EXISTS |
| `design/.health-implementer-design-work/domain-research.md` | EXISTS |
| `.claude/agents/` (dir; `<slug>/agent.md` targets) | EXISTS (dir) |
| `.claude/hooks/enforce-role-inlining.sh` | EXISTS (v2.5 confirmed) |
| `.claude/hooks/block-commit-main.sh` | EXISTS |
| `.claude/hooks/block-push-main.sh` | EXISTS |
| `/upgrade-agent` (command) | EXISTS (`~/.claude/commands/upgrade-agent.md`) |
| `/aplus-research` (skill) | EXISTS (`.claude/skills/aplus-research/SKILL.md`; `--mode`/`--target` flags confirmed) |
| `vault/library/<class>/` | EXISTS (biomarkers, interventions, peptides, supplements, methodology) |
| `INVARIANTS.md` | EXISTS |
| `scripts/audit-specialist-profile.sh` | **MISSING** — referenced honestly as the self-audit target; PROPOSED per design §13 (every audit-script row PROPOSED; AC-1 gates PROPOSED→LIVE). Profile must not claim it is LIVE. |
| `design/.health-implementer-design-work/audit-runs/` (Write target) | MISSING (dir) — created at runtime by the implementer via Write, not a reference to load. |
| `design/.health-implementer-design-work/scratch/` (Write target) | MISSING (dir) — created at runtime via Write, not a reference to load. |

Freshness confirmed: tool/skill names current — `/aplus-research`, `/upgrade-agent`, `enforce-role-inlining.sh` hook v2.5 all present and matching design references. The only known-not-yet-existing path is `scripts/audit-specialist-profile.sh`, referenced as PROPOSED throughout.
