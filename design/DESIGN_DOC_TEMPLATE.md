---
title: Design Doc Template — Medical Agent Roles
type: canonical-template
status: Final (red team reviewed, all 22 findings classified, synthesis complete)
created: 2026-05-26
adapts_from: ~/.claude/projects/-Users-waltermcgivney-Documents-Projects-Quant/memory/design-doc-protocol.md
downstream: /upgrade-agent command (consumes finalized design docs written to this template)
applies_to: 4 foundation roles (Pass-2) + 14 specialist roles (Pass-4)
last-PF-reviewed: PF-S6-01
---

# Design Doc Template — Medical Agent Roles

This is the canonical template every Pass-2 (foundation) and Pass-4 (specialist) design doc in the `a-plus-maxing` project conforms to. The template is the contract; the role profiles are its implementations. The downstream consumer is the `/upgrade-agent` command, which reads finalized design docs and synthesizes `~/Documents/Projects/skills_library/roles/{role-slug}/agent.md` conforming to `AGENT_TEMPLATE.md`.

---

## 0. How to use this template

1. **Copy** this file to `design/{role-slug}-design.md` (e.g., `design/health-specialist-architect-design.md`).
2. **Set frontmatter** per §0.2 below.
3. **Author sections 1–18** following each section's writer-produces spec. Sections marked CONDITIONAL may be OMITTED only with explicit "OMITTED — rationale" note.
4. **Phase 3 (red team) + Phase 4 (verification) populate Appendix A**.
5. **At Phase 5 finalize**, set frontmatter `status: Final (red team reviewed, all findings classified)`, commit on feature branch.

### 0.1 Pipeline placement

> **Status snapshot for any session picking this up (current as of S7 close 2026-05-26):**
>
> - **Pass-1 deep-research is COMPLETE for the 4 foundation roles.** The deliverables exist at `design/.{role}-design-work/domain-research.md` for each of: health-specialist-architect, health-implementer, health-edge-case-reviewer, medical-safety-reviewer. ~49,500 words total. Cleared 99/100 rubric. Do NOT re-run Pass-1 for these roles.
> - **Pass-2 design-doc-protocol has NOT YET RUN** for any of the 4 foundation roles. That is the work this template is for. Next session per S7 close: pick a role (recommended order: 1 → 2 → 3 → 4 per CONTINUATION_BRIEF §7) and run Phases 1–5 against this template.
> - **The 14 specialist roles have NO Pass-1 deliverable yet.** Their deep-research happens in Pass-3, AFTER the 4 foundation roles have been deployed via `/upgrade-agent`. Specialist design docs follow this template too, with the §3 specialist-fallback content path until their own Pass-1 lands in Pass-3.
> - **`/upgrade-agent` deployments: all 4 foundation roles deployed + incorporated** — health-specialist-architect (S9), health-implementer (S13), health-edge-case-reviewer (S14), medical-safety-reviewer (S15). Each was Session B for that role, after its Pass-2 design doc finalized. The 14 specialists remain NOT YET deployed.
> - **Canonical research-provenance layout (specialist Phase-0).** When a specialist's `/aplus-research` gate artifacts are committed into `design/.<slug>-design-work/`, keep the canonical dir names exactly: `gates/`, `judges/`, `sections/` (bare, no prefix). `gates/` is what `gate_attest.py` and `scripts/audit-research-provenance.sh` (bda) read; a prefixed variant such as `research-gates/` is non-canonical and bda-rejected. Single source of truth: aplus-research `SKILL.md` → "Canonical provenance directory layout".

```
Pass-1 deep-research → design/.{role}-design-work/domain-research.md (DONE for the 4 foundation roles; NOT YET for 14 specialists)
                              ↓
Pass-2/Pass-4 design-doc-protocol Phases 1–5:
  Phase 1: 3 parallel drafters (architect / senior-engineer / qa). For medical design docs: architect = project-local `.claude/agents/health-specialist-architect/agent.md` (deployed S9); senior-engineer = project-local `.claude/agents/health-implementer/agent.md` (deployed + incorporated S13); qa = project-local `.claude/agents/health-edge-case-reviewer/agent.md` (deployed + incorporated S14). See CONTINUATION_BRIEF §7 for the rotation table.
  Phase 2: orchestrator synthesizes into design/{role-slug}-design.md following THIS TEMPLATE
  Phase 3: 2 parallel red-team dispatches (/adversarial-review skill + safety = project-local `.claude/agents/medical-safety-reviewer/agent.md` (deployed + incorporated S15), replacing the software-security v1-substitute. See CONTINUATION_BRIEF §7 for the rotation table.)
  Phase 4: orchestrator personally verifies each finding (PF-S3-01 guard); finding classifications documented
  Phase 5: synthesis incorporates Legitimate findings; Rejected findings → Appendix A with cited evidence; Status: Final
                              ↓
Session B: /upgrade-agent reads the finalized design-doc → produces deployed agent.md
                              ↓
Pass-3 deep-research for specialists (uses the now-deployed foundation agents as drafters)
```

### 0.2 Frontmatter requirements

Every Pass-2 design doc carries:

```yaml
---
title: {Role Name} Design Doc
type: design-doc
status: Draft | Phase-3 Red-Team Pending | Phase-4 Verification | Final (red team reviewed, all findings classified)
role_slug: {role-slug, kebab-case, matches roles/{slug}/agent.md path}
role_class: foundation | specialist
pass_1_substrate: design/.{role-slug}-design-work/domain-research.md
authored_by: design-doc-protocol Pass-2/Pass-4
created: YYYY-MM-DD
last-PF-reviewed: PF-S<N>-<NN>  # the latest PF ID in memory/process-failures.md at time of authoring
adapts_template: design/DESIGN_DOC_TEMPLATE.md
downstream: /upgrade-agent → ~/Documents/Projects/skills_library/roles/{role-slug}/agent.md
---
```

`last-PF-reviewed` is load-bearing: at `/upgrade-agent` Phase 1, the upgrade-agent diff-checks PF entries against this field and surfaces any new PF entries as candidate Anti-Pattern additions.

---

## 1. Section inventory (18 sections + Appendix A)

| § | Section | Status | Budget (lines) |
|---|---|---|---|
| 1 | Problem Statement | REQUIRED | 5–15 |
| 2 | Role Definition (Identity + Boundaries) | REQUIRED | 25–40 |
| 3 | Pass-1 Deliverable Digest | REQUIRED | 30–60 |
| 4 | Cross-Role References (Directional) | REQUIRED | 15–30 |
| 5 | Core Behavioral Rules | REQUIRED | 30–50 |
| 6 | Ask vs Proceed Decision Tree | REQUIRED | 15–25 |
| 7 | Loop-Breaking Thresholds | REQUIRED | 10–15 |
| 8 | Tools and Permissions | REQUIRED | 15–25 |
| 9 | Communication Protocol | REQUIRED | 20–35 |
| 10 | Context Loading Protocol | REQUIRED | 15–25 |
| 11 | Anti-Patterns | REQUIRED | 25–40 |
| 12 | Negative Examples | REQUIRED | 25–45 |
| 13 | Mechanical Enforcement Map | REQUIRED | 25–40 |
| 14 | Edge Cases | REQUIRED | 20–35 |
| 15 | Acceptance Criteria (Role-Specific) | REQUIRED | 15–25 |
| 16 | Invariants at Risk | REQUIRED | 12–22 |
| 17 | Risk Assessment, Assumptions, and Break Conditions | REQUIRED | 25–40 |
| 18 | Open Questions | REQUIRED | 10–20 |
| A | Red Team Findings (Appendix) | REQUIRED at Phase-5 | variable |

**Total target: ~290–525 lines per design doc** (substantive but not bloated; well under the upper bound of a careful Pass-2 cycle).

---

## 2. The 18 sections — specs and templates

For every section: (i) the **writer-produces spec** stating what the section must contain (binary verifiable), (ii) the **status** (REQUIRED / CONDITIONAL with condition), (iii) the **budget** in lines, (iv) the **AGENT_TEMPLATE.md mapping** (which AGENT_TEMPLATE section consumes this; "N/A — meta-section" if the section serves the design-doc-protocol process itself), (v) the **`/upgrade-agent` phase mapping** (which phase consumes this).

> **AGENT_TEMPLATE.md note (per Finding F-001 disposition).** `AGENT_TEMPLATE.md` defines **10 base sections**: Identity, Core Rules, Role Boundaries, Ask vs Proceed, Loop-Breaking, Tools, Communication, Context Loading, Anti-Patterns, Negative Examples. Mature profiles add **1+ role-specific sections** between Anti-Patterns and Negative Examples (typically `## Modes`; sometimes `## Spec Amendment Protocol` etc.), per `/upgrade-agent` Phase 5 lines 236. The project's `enforce-role-inlining.sh` hook expects 11 sections (the 10 base + Modes) for role-tagged dispatches because mature profiles inline Modes. When this template's sections "map to AGENT_TEMPLATE.md," they map to the 10 base sections; the role-specific Modes content is informed by §5 (Core Behavioral Rules) + §9 (Communication Protocol) + §14 (Edge Cases) jointly and emerges as a `/upgrade-agent` Phase 5 synthesis output, not a 1:1 design-doc mapping.

### Section 1 — Problem Statement

- **Purpose.** State the gap this role fills and why the existing roster does not cover it. Frame the design doc reader in 30 seconds.
- **Writer produces.** A 3–7 sentence opening followed by a numbered list of 2–4 specific gaps in the existing roster (software roles, prior specialist roles, or the wiki) that this role addresses. Each gap cites concrete evidence (Pass-1 Finding number / wiki gap / specialist roster row). Binary verifiable: ≥2 numbered gaps; every gap has a citation.
- **Status.** REQUIRED.
- **Budget.** 5–15 lines.
- **AGENT_TEMPLATE.md mapping.** Identity (informs the first-30-seconds clarity dimension).
- **/upgrade-agent phase.** Phase 1 (Baseline Evaluation — frames what the agent is evaluating against).

Template:
```markdown
## 1. Problem Statement

{One-paragraph framing of the role's purpose and the gap it fills.}

Specific gaps this role addresses:

1. **{Gap title}** — {1-sentence claim}. Source: {Pass-1 Finding N / wiki gap / specialist roster row}.
2. **{Gap title}** — {1-sentence claim}. Source: {citation}.
```

---

### Section 2 — Role Definition (Identity + Boundaries)

- **Purpose.** State who this role IS and what it owns vs does not own. The Role Boundaries half is critical for cross-role-team composition (per CONTINUATION_BRIEF §10 references).
- **Writer produces.** Two subsections:
  - **2.1 Identity sentence.** ≤40 words, imperative or descriptive, stating the role's function. No personality adjectives. Must include the role's anti-sycophancy anchor (a one-sentence stance against unwarranted agreement; AGENT_TEMPLATE.md lines 7–11 are the pattern).
  - **2.2 Role Boundaries.** Two named lists: **I own:** (3–7 items) and **I do NOT own:** (3–7 items, each with the owning role in parentheses). Plus a one-sentence escalation rule for when this role detects a problem in a not-owned area.
  - Binary verifiable: identity sentence ≤40 words; "I own" + "I do NOT own" both present; every "do NOT own" item names an owning role.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Identity (2.1) + Role Boundaries (2.2).
- **/upgrade-agent phase.** Phase 5 (Synthesis — Identity + Role Boundaries authoring).

Template:
```markdown
## 2. Role Definition

### 2.1 Identity

You are the {Role Name}. {≤40-word function sentence. What this role receives, what it delivers, who it interacts with.}

{Anti-sycophancy anchor per AGENT_TEMPLATE.md pattern.}

### 2.2 Role Boundaries

**I own:** {item}, {item}, {item}, {item}.

**I do NOT own:** {item} ({owning role}), {item} ({owning role}), {item} ({owning role}).

When I detect a problem in a not-owned area, I {one-sentence escalation rule}.
```

---

### Section 3 — Pass-1 Deliverable Digest

- **Purpose.** Lift the load-bearing structural conclusions from this role's `domain-research.md` (or the role's foundation-inheritance substrate, for specialists) into a form the design doc can reference without paraphrase drift. This is the project's defense against the "design doc redefines what the research established" failure mode.
- **Pre-write step (per Finding F-015 disposition).** Before authoring, count `^### Finding ` headings in the role's `domain-research.md` (or the inherited foundation-role digest, for specialists). This is the row count for the Findings table.
- **Writer produces.**
  - **3.1 Findings table.** One row per Pass-1 Finding (count matches the pre-write count). Columns: Finding # / one-sentence claim / cited source line range in `domain-research.md` / AGENT_TEMPLATE.md section this Finding informs / whether this design doc ACCEPTS or MODIFIES the Finding (with rationale if MODIFIES).
  - **3.2 Recommendations list.** Pass-1 Recommendations R1–R<N> where N is the count in the source deliverable (per Finding F-006 disposition: foundation deliverables empirically have N=15; the softer phrasing is defensive forward-compat for specialists). Each Recommendation tagged ACCEPTED / DEFERRED / REJECTED. Deferrals and rejections require one-line rationale. No "TBD" verdicts.
  - **Specialist fallback (per Finding F-003 disposition).** For specialist roles (`role_class: specialist` in frontmatter) whose Pass-3 deep-research has not yet been completed, §3 instead documents the relevant foundation-role Pass-1 digests as inherited substrate, with explicit Finding-by-Finding inheritance verdict (ACCEPTED / NARROWED / NOT-APPLICABLE). The section remains REQUIRED — single status preserves the anti-paraphrase property across role classes.
  - Binary verifiable: row count in §3.1 matches Finding count in source `domain-research.md` (cited by `pass_1_substrate:` frontmatter field); §3.2 has every Recommendation in source with a verdict; no "TBD" verdicts.
- **Status.** REQUIRED (for both foundation and specialist roles; specialist fallback content per above).
- **Budget.** 30–60 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section. The Findings inform multiple AGENT_TEMPLATE sections downstream; the digest itself is design-doc-internal anchoring.
- **/upgrade-agent phase.** All phases (the upgrade-agent reads this section to know which Findings ground which content decisions).

Template:
```markdown
## 3. Pass-1 Deliverable Digest

Source: `{pass_1_substrate value from frontmatter}` (verify path resolves before authoring).

### 3.1 Findings table

| # | Claim (1 sentence) | Source lines | AGENT_TEMPLATE section | Verdict |
|---|---|---|---|---|
| 1 | ... | L42-L58 | Core Rules | ACCEPTED |
| 2 | ... | ... | ... | MODIFIED — {rationale} |
| ... | | | | |

### 3.2 Pass-1 Recommendations

| # | Recommendation (1 sentence) | Verdict | Rationale (only for DEFERRED/REJECTED) |
|---|---|---|---|
| R1 | ... | ACCEPTED | — |
| R2 | ... | DEFERRED | {reason} |
| ... | | | |
```

---

### Section 4 — Cross-Role References (Directional)

- **Purpose.** Document which other roles this role depends on or feeds, per CONTINUATION_BRIEF §10's cross-role reference table. Prevents content duplication across the 18 design docs.
- **"Applicable" (per Finding F-017 disposition).** A CONTINUATION_BRIEF §10 row is **applicable** to this design doc when this role's name appears in either the from-role column OR the to-role column of the table.
- **Directionality (per Finding F-004 disposition).** This section is DIRECTIONAL — for the first-authored foundation role under this template (Role 1 health-specialist-architect), §4 lists the OUTBOUND references this design doc establishes (i.e., what later roles will inherit FROM this one). For Roles 2+ and all specialists, §4 lists the INBOUND references this design doc inherits FROM finalized prior roles.
- **Writer produces.** A table with directionality column. For each applicable CB §10 row: direction (OUTBOUND / INBOUND), the cross-role item, the role this references to/from, what is being referenced, and how this design doc handles it (references-not-redefines / inherits-verbatim / role-specializes).
  - Binary verifiable: every applicable CB §10 row from the role's perspective is present; no referenced content is redefined inline (references only, with explicit pointers to the source); direction tag matches the role's authoring order.
- **Status.** REQUIRED.
- **Budget.** 15–30 lines.
- **AGENT_TEMPLATE.md mapping.** Role Boundaries (informs cross-role escalation paths) + Context Loading (cross-role references inform what context is loaded).
- **/upgrade-agent phase.** Phase 6 (Adversarial Review — the reviewer uses this section to check for content duplication / contradiction with sibling profiles).

Template:
```markdown
## 4. Cross-Role References (Directional)

Per CONTINUATION_BRIEF §10. Direction reflects authoring order: foundation roles' first-authored doc establishes OUTBOUND; later docs inherit INBOUND.

| Direction | Item | Counterpart role | What | How handled |
|---|---|---|---|---|
| OUTBOUND | Refusal-class taxonomy | Roles 2/3/4 | The 7-class taxonomy | Defined here; downstream references |
| INBOUND | GRADE evidence-tier discipline | Role 1 | GRADE scheme | Inherits verbatim from Role 1 §X |
| ... | | | | |
```

---

### Section 5 — Core Behavioral Rules

- **Purpose.** State the 8–12 testable behavioral rules this role follows. These become the Core Rules section of the deployed agent.md.
- **Writer produces.** A numbered list of 8–12 rules. Each rule is one of two voices (per Finding F-007 disposition, inheriting AGENT_TEMPLATE.md lines 20–21 verbatim):
  - **Imperative voice** for standing instructions ("Run all tests after changes.")
  - **First-person experiential voice** for learned-experience rules ("Every time I've X, Y happened. Now I Z.")
  Rule-by-rule the writer tags WHICH voice each rule uses (`[voice: imperative]` or `[voice: first-person]`) and the source category (`[source: standing-instruction]` or `[source: learned-experience]`).
  - Each rule has a concrete pass/fail condition — testable without seeing implementation.
  - Anti-sycophancy and self-attestation rules required (every role must guard against PF-S2-01 / PF-S3-01 class).
  - Binary verifiable: 8–12 rules; every rule has voice tag + source tag; every rule has a pass/fail condition.
- **Status.** REQUIRED.
- **Budget.** 30–50 lines.
- **AGENT_TEMPLATE.md mapping.** Core Rules.
- **/upgrade-agent phase.** Phase 3 (Research Agents R1 Behavioral Traits + R3 Communication & Anti-Patterns) + Phase 5 (Synthesis).

Template:
```markdown
## 5. Core Behavioral Rules

1. **{Rule title}.** {Rule body — imperative or first-person.} [voice: imperative] [source: standing-instruction]
2. **{Rule title}.** Every time I've {situation}, {outcome}. Now I {behavior}. [voice: first-person] [source: learned-experience]
3. ...
```

---

### Section 6 — Ask vs Proceed Decision Tree

- **Purpose.** State the 4–6 step decision tree the role follows when input is ambiguous. Prevents over-questioning (PF-S2-03) and over-acting-without-verification (PF-S6-01).
- **Writer produces.** A numbered decision tree (4–6 steps), each step a binary check with a "yes → action" / "no → next step" outcome. Final step is a default action with stated assumption. Includes the project's "Never fabricate {role-specific thing}" rule.
- **Status.** REQUIRED.
- **Budget.** 15–25 lines.
- **AGENT_TEMPLATE.md mapping.** Ask vs Proceed.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

Template:
```markdown
## 6. Ask vs Proceed Decision Tree

1. Can I find the answer in {role-relevant authoritative source}? Check there first.
2. Does the ambiguity affect {role-specific load-bearing thing}? Ask.
3. ...
4. Everything else: proceed with the simpler assumption, state it explicitly.

Never fabricate {role-specific fabrication risk}.
```

---

### Section 7 — Loop-Breaking Thresholds

- **Purpose.** State concrete thresholds at which the role abandons a sub-task to avoid loops.
- **Writer produces.** A bulleted list of 3–5 thresholds, each a concrete numeric or boundary condition. Examples: "If I have revised a section more than twice without new information, deliver it as-is"; "If a review has gone 3 rounds without convergence, escalate."
- **Status.** REQUIRED.
- **Budget.** 10–15 lines.
- **AGENT_TEMPLATE.md mapping.** Loop-Breaking.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

Template:
```markdown
## 7. Loop-Breaking Thresholds

- If {situation}, {action}.
- If {situation}, {action}.
- If context feels large, write intermediate analysis to a scratch file before rendering decisions.
```

---

### Section 8 — Tools and Permissions

- **Purpose.** State which Claude Code tools the role uses, role-specific usage patterns, and explicit restrictions (negative constraints).
- **Writer produces.** A bulleted list naming the role's tool palette + 2–4 role-specific usage patterns + 1–3 explicit restrictions (e.g., "Do not write implementation code"; "Do not run aplus-research dispatches — read finalized deliverables only"). Tool restrictions are load-bearing: a Role's tool restrictions may make certain PFs structurally out-of-scope (see Finding F-013 disposition / Section 11).
- **Status.** REQUIRED.
- **Budget.** 15–25 lines.
- **AGENT_TEMPLATE.md mapping.** Tools.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

Template:
```markdown
## 8. Tools and Permissions

Tool palette: Read, Grep, Glob, Write, Edit, Bash, Agent, {role-specific MCP servers}.

Role-specific patterns:
- Use {Tool} to {role-specific purpose}.
- Use {Tool} to {role-specific purpose}.

Restrictions:
- Do not {restricted action} ({owning role does this instead}).
- Do not {restricted action}.
```

---

### Section 9 — Communication Protocol

- **Purpose.** Define the role's two-audience output formats: how the role talks to other agents/orchestrator vs how the role talks to the user.
- **Writer produces (per Finding F-008 disposition).** Two named subsections (9.1 to-other-agents/orchestrator, 9.2 to-user), each containing a **format spec**. A "format spec" is defined as one of three concrete shapes:
  - **(a) A sample output** — 3–5 lines literal example demonstrating the output shape
  - **(b) A structured-list spec** — naming required fields (e.g., "interface definitions, file paths, type signatures, ADR references, constraint rationale")
  - **(c) A sentence pattern** — a template the agent fills (e.g., "I observed X; the contract violation is Y; the affected interface is Z")
  AGENT_TEMPLATE.md Communication section is the inheritance template; the design doc role-specializes.
  - Binary verifiable: both 9.1 and 9.2 present; each carries a format spec in one of the three shapes; format spec is non-empty and operationally specific (not "appropriate tone").
- **Status.** REQUIRED.
- **Budget.** 20–35 lines.
- **AGENT_TEMPLATE.md mapping.** Communication.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

Template:
```markdown
## 9. Communication Protocol

### 9.1 To other agents and the orchestrator

Format spec: {(a) sample output / (b) structured-list / (c) sentence pattern — pick one and instantiate}

### 9.2 To the user

Format spec: {(a) sample output / (b) structured-list / (c) sentence pattern — pick one and instantiate}
```

---

### Section 10 — Context Loading Protocol

- **Purpose.** State how the role decides what context to load and in what order.
- **Writer produces.** A numbered protocol (4–7 steps) covering: which library references the role consumes, role-specific loading order, when to skip pre-loading, what cross-role references (from §4) trigger context loads.
- **Status.** REQUIRED.
- **Budget.** 15–25 lines.
- **AGENT_TEMPLATE.md mapping.** Context Loading.
- **/upgrade-agent phase.** Phase 5 (Synthesis).

---

### Section 11 — Anti-Patterns

- **Purpose.** Enumerate 5–8 role-specific anti-patterns as concrete "I don't X" statements, grounded in project PF entries or Pass-1 Findings.
- **PF inclusion criterion (per Finding F-013 disposition).** A PF entry is **in-scope** for this role if the role's tool permissions + behavioral context allow the failure mode. A PF entry is **out-of-scope** if the role's tool restrictions or behavioral context structurally prevent it. Each PF entry gets an explicit per-role verdict (IN-SCOPE / OUT-OF-SCOPE — structural reason / OUT-OF-SCOPE — domain reason). Reference all 8 currently-documented PFs:
  - PF-S2-01 — orchestrator declared deep-mode but skipped paired judges (self-attestation class)
  - PF-S2-02 — citation error caught by accident (verification class)
  - PF-S2-03 — over-questioning user during scoping
  - PF-S2-04 — over-personalized library research (goal-agnostic vs personalized class)
  - PF-S2-05 — operating from mental-model rather than re-reading protocol
  - PF-S2-06 — branch hygiene (commits on main) — CONDITIONAL: in-scope only for roles whose tool permissions allow git commits
  - PF-S3-01 — orchestrator self-attested 5 of 6 gates (mechanical-fix-confused-with-verdict)
  - PF-S6-01 — acted on prior-session state without verifying current state
- **Writer produces.** Two subsections:
  - **11.1 PF coverage table.** All 8 PF entries with verdict (IN-SCOPE / OUT-OF-SCOPE + structural-or-domain reason). OUT-OF-SCOPE verdicts cite the structural reason (e.g., "tool restrictions exclude Write/Edit/Bash; cannot commit").
  - **11.2 Anti-patterns list.** 5–8 numbered anti-patterns, each: (a) concrete "I don't X" phrasing; (b) source link (PF-S<N>-<NN> or Pass-1 Finding N); (c) **recognition cue** (the situation/signal that should trigger the anti-pattern check — defined per glossary §3 below).
  - Binary verifiable: §11.1 has all 8 PF entries with verdicts; §11.2 count 5–8; each entry has source link + recognition cue.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** Anti-Patterns.
- **/upgrade-agent phase.** Phase 3 (Research Agents R3) + Phase 5 (Synthesis).

Template:
```markdown
## 11. Anti-Patterns

### 11.1 Project PF coverage

| PF | Behavior | In-scope for this role? | Reason |
|---|---|---|---|
| PF-S2-01 | Self-attests rigor | IN-SCOPE | Role produces verdicts |
| PF-S2-06 | Commits on main | OUT-OF-SCOPE | Tool restrictions exclude git |
| ... | ... | ... | ... |

### 11.2 Anti-patterns (role-specific)

1. **I don't {behavior}.** Source: PF-S2-01. Recognition cue: {situation/signal — see glossary §3}.
2. ...
```

---

### Section 12 — Negative Examples

- **Purpose.** Provide 2–4 BAD/GOOD pairs demonstrating the role's anti-patterns in concrete form. Placed at end of agent.md for recency effect.
- **Writer produces (per Finding F-009 disposition).** 2–4 BAD/GOOD pairs. A "BAD/GOOD pair" (defined in glossary §3) is two code blocks with `BAD:` and `GOOD:` headers showing the same situation handled wrong then right.
  - Each pair is role-specific (not generic "be thorough" advice).
  - Each pair maps to an anti-pattern from §11 (cited by anti-pattern number).
  - Binary verifiable: 2–4 pairs; each has `BAD:` and `GOOD:` block; each cites a §11 anti-pattern number.
- **Status.** REQUIRED.
- **Budget.** 25–45 lines.
- **AGENT_TEMPLATE.md mapping.** Negative Examples.
- **/upgrade-agent phase.** Phase 5 (Synthesis — placed in last 30 lines of agent.md for recency effect).

Template:
```markdown
## 12. Negative Examples

### 12.1 {Anti-pattern N name}

```
BAD (cites §11 anti-pattern N):
{Concrete bad behavior, 3-6 lines}

GOOD:
{Same situation, role-correct behavior, 3-6 lines}
```

### 12.2 ...
```

---

### Section 13 — Mechanical Enforcement Map

- **Purpose.** Enumerate every mechanical check (audit script, grep pattern, schema validator, hook) this role's deployed agent.md requires. Anchors the project's "invariants get scripts" principle (INVARIANTS.md lines 14–15) into the design-doc layer.
- **Writer produces.** A table with one row per mechanical check. Columns: check name / what it verifies / mechanism (path or pattern) / **status tag** / failure consequence (BLOCK vs WARN).
- **Status tags (per Finding F-010 disposition).** Every row carries one of:
  - **LIVE** — script/hook/schema exists at the cited path; path verified via Glob; gates the resulting agent.md
  - **REFERENCED** — an existing INVARIANTS.md row enforces this; cite the INV-* ID; the deployed agent.md inherits the enforcement
  - **PROPOSED** — script/hook does not exist yet; row carries the expected path + one-sentence behavioral spec; does NOT gate the resulting agent.md (would falsely-claim mechanical enforcement)
- **PROPOSED row handling.** Each PROPOSED row also surfaces in §18 (Open Questions) AND generates a follow-up bead at session close. The agent.md cites only LIVE and REFERENCED checks as live mechanical defenses.
- **Binary verifiable.** Row count ≥3; every row has a status tag; every LIVE row's path resolves; every REFERENCED row cites an INV-* ID present in INVARIANTS.md; every PROPOSED row appears in §18 too.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; informs the agent.md's deployment-gating but is not itself an agent.md section.
- **/upgrade-agent phase.** Phase 4 (Validation Loop — fact-checker verifies each LIVE row's path resolves) + Phase 5 (Synthesis — only LIVE/REFERENCED checks become cited in agent.md) + Phase 7 (Final Corrections — re-verifies the LIVE/REFERENCED set is intact).

Template:
```markdown
## 13. Mechanical Enforcement Map

| Check | Verifies | Mechanism | Status | Consequence |
|---|---|---|---|---|
| Role inlining | full 11-section profile in role dispatches | `.claude/hooks/enforce-role-inlining.sh` | LIVE | BLOCK |
| Cross-role attestation | verdict chain integrity | INV-RESEARCH-ATTESTATION | REFERENCED | BLOCK |
| {role-specific check} | {what} | `scripts/{role-specific-audit}.sh` | PROPOSED | (deferred per §18) |
```

---

### Section 14 — Edge Cases

- **Purpose.** Surface scenarios the role must handle that aren't covered by the routine paths in §5–§13.
- **Writer produces.** A bulleted list of 4–8 edge cases. Each: situation description / how the role handles it / **test stimulus** (defined per glossary §3 — a concrete input the role must handle the named way).
  - Cross-phase edge cases required: what happens when the role's upstream produces a HALT verdict; what happens when the role's downstream consumer doesn't exist yet (relevant for foundation roles).
  - Binary verifiable: 4–8 entries; each has handling + test stimulus.
- **Status.** REQUIRED.
- **Budget.** 20–35 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; informs operational completeness checks in `/upgrade-agent` Phase 6 (Adversarial Review).
- **/upgrade-agent phase.** Phase 6 (Adversarial Review — used as test stimuli for adversarial walks).

---

### Section 15 — Acceptance Criteria (Role-Specific)

- **Purpose.** State binary pass/fail criteria specific to THIS role's agent.md content. Generic agent.md constraints (line count ≤200, token count ≤2,000) are inherited from `/upgrade-agent` Phase 7 and **not restated here** (per Finding F-012 disposition — they live at the source of truth, not duplicated per design doc).
- **Writer produces.**
  - **15.1 Inherited criteria.** One subsection citing the generic constraints inherited from `/upgrade-agent` Phase 7 (lines 291–301 of `upgrade-agent.md`). Single-paragraph reference, not a restatement.
  - **15.2 Role-specific criteria.** A numbered list of 5–10 binary pass/fail criteria specific to THIS role. Examples: "Core Rule count is 8–12"; "Anti-patterns include explicit PF-S3-01 guard"; "Communication §9.1 format spec is in form (a), (b), or (c)"; "every Pass-1 Recommendation marked ACCEPTED in §3 is implemented in agent.md or has a deferred-rationale entry."
  - Binary verifiable: 15.1 references `/upgrade-agent` Phase 7 explicitly; 15.2 count 5–10; each criterion independently testable.
- **Status.** REQUIRED.
- **Budget.** 15–25 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 2 (Rubric Construction — feeds the agent-specific rubric per Finding F-002 disposition) + Phase 7 (Final Corrections — verified against this section).

Template:
```markdown
## 15. Acceptance Criteria (Role-Specific)

### 15.1 Inherited from `/upgrade-agent` Phase 7

Generic constraints (line count ≤200, token count ≤2,000, all AGENT_TEMPLATE.md sections present, library-index reference paths resolve, catalog entry consistency, BAD/GOOD pair count, anti-sycophancy placement, negative examples placement, operational completeness) are enforced by `/upgrade-agent` Phase 7 (lines 291–301 of `upgrade-agent.md`) and not restated here.

### 15.2 Role-specific

1. {Role-specific binary criterion}
2. {Role-specific binary criterion}
3. ...
```

---

### Section 16 — Invariants at Risk

- **Purpose.** Name the project invariants this role's design or behavior could affect.
- **Scope (per Finding F-011 disposition).** This section addresses invariants in 3 categories: **Format/Document** (INV-HO-* — HANDOFF.md hygiene), **Process** (INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN), and **Role-discipline** (INV-ROLE-INLINING). The Research-domain category (INV-RESEARCH-*) is OUT-OF-SCOPE for non-research roles (i.e., for all 4 foundation roles AND for 13 of the 14 specialists). Only specialist roles that dispatch `/aplus-research` (currently peptide-specialist + future research-dispatching specialists) include Research-domain INV-* in scope. The current active invariant count is 12; in-scope subset for a typical non-research role is ~6.
- **Writer produces.** A table with one row per in-scope invariant. Columns: INV-* ID / risk type (could this role's design move toward violation, or does the role's design strengthen the invariant?) / mechanism (how the role's design relates to the invariant).
  - If the role IS research-dispatching (peptide-specialist etc.), the Research-domain INV-* set is included.
  - Binary verifiable: every in-scope invariant per the scope criterion is addressed; out-of-scope categories not enumerated (the scope criterion + INVARIANTS.md is the audit path).
- **Status.** REQUIRED.
- **Budget.** 12–22 lines (smaller than originally proposed; scope restriction cuts the row count).
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 7 (Final Corrections — invariant-compliance check).

Template:
```markdown
## 16. Invariants at Risk

Scope: Format/Document + Process + Role-discipline categories. Research-domain INV-* out-of-scope for this role (rationale: {tool restrictions exclude aplus-research dispatch / role does not produce wiki content / etc.}).

| INV ID | Risk type | Mechanism |
|---|---|---|
| INV-ROLE-INLINING | Strengthens | This role's design doc inlines per `enforce-role-inlining.sh` |
| INV-SCOPE-CONTRACT | No effect | Role does not perform session-lifecycle work |
| ... | | |
```

---

### Section 17 — Risk Assessment, Assumptions, and Break Conditions

- **Purpose.** Surface what could go wrong with this role's design, what assumptions the design depends on, and what conditions would invalidate the design.
- **Writer produces (per Finding F-016 disposition — Assumptions added back).** Three subsections:
  - **17.1 Risk Assessment.** Numbered list of 3–7 risks. Each: risk title / mechanism / severity (BLOCK / WARN / NOTE) / mitigation.
  - **17.2 Assumptions.** Numbered list of 3–7 preconditions the design depends on. Each: assumption / `breaks-if:` condition (the concrete state under which the assumption fails).
  - **17.3 Break Conditions.** Numbered list of 2–5 specific external conditions that would invalidate this design as a whole (independent of mid-design corrections). Each: condition / how a future session would detect it.
  - Binary verifiable: 17.1 has 3–7 risks; 17.2 has 3–7 assumptions each with `breaks-if:`; 17.3 has 2–5 break conditions each with detection cue.
- **Distinction.** Risks = things that could go wrong during operation. Assumptions = preconditions whose violation invalidates the design. Break Conditions = external state changes that obsolete the design even if everything internally still works.
- **Status.** REQUIRED.
- **Budget.** 25–40 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 5 (Synthesis — informs the catalog update).

---

### Section 18 — Open Questions

- **Purpose.** Surface unresolved decisions the design doc cannot answer from its own sources. The orchestrator or a future session must adjudicate before deployment.
- **Writer produces.** A numbered list of 0–5 open questions. Each: question / why it could not be resolved at design time / who/what is positioned to answer it / blocker-or-non-blocker.
  - **PROPOSED checks from §13** must appear here too (per Finding F-010 disposition).
  - **False zero is worse than honest non-zero.** If the writer believes there are 0 open questions, write the attestation: "None — every section's spec is satisfied by current sources." A silent zero is a red flag.
  - Binary verifiable: section is present even if 0 items; every PROPOSED §13 row also appears as an entry.
- **Status.** REQUIRED.
- **Budget.** 10–20 lines.
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section.
- **/upgrade-agent phase.** Phase 8 (Close Out — feeds follow-up items / beads).

---

### Appendix A — Red Team Findings

- **Purpose.** Capture every red-team finding from Phase 3 with classification verdict from Phase 4. Documents what was caught and what was rejected (with cited evidence per the PF-S3-01 guard).
- **Writer produces (at Phase 5).** A table with one row per finding from the two Phase-3 red-team dispatches (adversarial + safety). Columns: Finding ID / Category / Section affected / Severity / Description / Cited evidence / Verdict (LEGITIMATE / LEGITIMATE-MODIFIED / REJECTED) / Disposition (how applied in the synthesized doc).
  - REJECTED findings include source-of-truth attestation in the cited-evidence column (not orchestrator prose).
  - Binary verifiable: every finding from both red-team dispatch outputs is present; every REJECTED row carries source-of-truth evidence.
- **Status.** REQUIRED at Phase 5 finalize (the appendix is created empty when the template is first instantiated and populated as Phase 3 → Phase 4 progress).
- **Budget.** Variable (typically 30–100 lines depending on finding count).
- **AGENT_TEMPLATE.md mapping.** N/A — meta-section; the appendix documents the design-doc-protocol's own quality gate.
- **/upgrade-agent phase.** Phase 1 (Baseline Evaluation reads to understand prior verification work) + Phase 8 (Close Out for any deferred items).

---

## 3. Glossary (load-bearing terms)

Per Finding F-009 disposition. Every Pass-2 design doc inherits this glossary; terms not defined here are role-specific and should be defined inline at first use.

- **Recognition cue.** The concrete situation, signal, or input pattern that should trigger an anti-pattern check at runtime. Distinct from the anti-pattern itself (which is the behavior the role avoids). Example: anti-pattern = "I don't self-attest verdicts"; recognition cue = "I notice I'm about to write a PASS verdict without a dispatched verifier output to cite."
- **Test stimulus.** A concrete input the role must handle in the manner specified. Used in §14 (Edge Cases) to make the handling specification testable. Example: not "the role should handle malformed JSON gracefully" but "test stimulus: the input is a JSON file with a trailing comma; the role detects the parse error, writes a one-line error report, and HALTs."
- **BAD/GOOD pair.** A two-block comparison in §12 (Negative Examples) with literal `BAD:` and `GOOD:` headers showing the same situation handled wrong then right. Each block is 3–6 lines. The pair maps to a specific §11 anti-pattern (cited by number).
- **Deferred-rationale entry.** A one-line `[DEFERRED: <reason>]` note attached to a Pass-1 Recommendation that this design doc accepts in principle but does not implement in this iteration. The reason cites a concrete blocker (e.g., "DEFERRED: requires Role 4 agent to be deployed").
- **Failure-mode tag.** A reference to a documented failure class, either a `PF-S\d+-\d+` identifier resolvable in `memory/process-failures.md` OR a free-text class name in the form `AP-XXX-NN` (anti-pattern class with sequential number).
- **Format spec.** Per §9 disposition, one of three shapes: (a) sample output 3–5 lines literal; (b) structured-list spec naming required fields; (c) sentence pattern the agent fills.
- **OUTBOUND / INBOUND reference.** Per §4 disposition, the directionality of a cross-role reference relative to authoring order. OUTBOUND = this design doc establishes the reference for later docs to inherit. INBOUND = this design doc inherits from a finalized prior doc.

---

## 4. Phase Coverage Matrix

Per Finding F-002 disposition. Every `/upgrade-agent` phase has at least one upstream design-doc section feeding it.

| `/upgrade-agent` phase | Upstream design-doc section(s) | Consumed for |
|---|---|---|
| Phase 1 (Baseline Evaluation) | §1, Appendix A | Frames evaluation target; prior verification context |
| Phase 2 (Rubric Construction) | §15 (Acceptance Criteria) | Agent-specific rubric dimensions |
| Phase 3 (Research Agents) | §5 (Core Rules), §11 (Anti-Patterns) | R1 Behavioral + R3 Communication & Anti-Patterns inputs |
| Phase 4 (Validation Loop) | §13 (Mechanical Enforcement Map), §15.2 (role-specific criteria) | Fact-checker verification criteria + judge dimensions |
| Phase 5 (Synthesis) | §2, §4, §5, §6, §7, §8, §9, §10, §11, §12, §13, §17 | All AGENT_TEMPLATE.md section contents in synthesis order (see §5 below) |
| Phase 6 (Adversarial Review) | §4 (Cross-Role), §14 (Edge Cases) | Sibling-consistency checks + adversarial test stimuli |
| Phase 7 (Final Corrections) | §13 (LIVE checks), §15.1 (inherited), §16 (Invariants) | Final consistency verification |
| Phase 8 (Close Out) | §18 (Open Questions), Appendix A | Follow-up items, deferred work, bead generation |

---

## 5. Synthesis Order (design-doc → AGENT_TEMPLATE.md mapping)

Per Finding F-014 disposition. `/upgrade-agent` Phase 5 synthesizes AGENT_TEMPLATE.md sections in this order; the design-doc-section feeding each is named.

| Order | AGENT_TEMPLATE.md section | Primary upstream | Secondary upstream |
|---|---|---|---|
| 1 | Identity | §2.1 | §1 (problem framing) |
| 2 | Core Rules | §5 | — |
| 3 | Role Boundaries | §2.2 | §4 (cross-role escalations) |
| 4 | Ask vs Proceed | §6 | — |
| 5 | Loop-Breaking | §7 | — |
| 6 | Tools | §8 | — |
| 7 | Communication | §9 | — |
| 8 | Context Loading | §10 | §4 (cross-role context loads) |
| 9 | (Role-specific Modes, etc.) | §5 + §9 + §14 | — |
| 10 | Anti-Patterns | §11 | §13 (mechanical defenses reference) |
| 11 | Negative Examples | §12 | §11 (each pair cites §11 anti-pattern) |

The 9th synthesis-step entry (role-specific Modes) is NOT a 1:1 design-doc section mapping — it emerges from §5 (rules that imply mode-switching) + §9 (communication patterns that differ by mode) + §14 (edge cases that trigger mode changes). The `/upgrade-agent` Phase 5 synthesizer decides whether to materialize a Modes section per role.

---

## 6. AGENT_TEMPLATE.md coverage (verification check)

Every AGENT_TEMPLATE.md base section has at least one upstream design-doc section:

| AGENT_TEMPLATE.md section | Upstream | OK? |
|---|---|---|
| Identity | §2.1 + §1 | ✓ |
| Core Rules | §5 | ✓ |
| Role Boundaries | §2.2 + §4 | ✓ |
| Ask vs Proceed | §6 | ✓ |
| Loop-Breaking | §7 | ✓ |
| Tools | §8 | ✓ |
| Communication | §9 | ✓ |
| Context Loading | §10 + §4 | ✓ |
| Anti-Patterns | §11 | ✓ |
| Negative Examples | §12 | ✓ |

All 10 base sections covered. Role-specific Modes (when present in deployed profile) emerges from §5+§9+§14 per §5 above.

---

## 7. Self-attest checklist (Phase 5 gate)

Before setting `status: Final` in frontmatter, the orchestrator verifies:

- [ ] All 18 sections + Appendix A present (no missing sections; CONDITIONAL omissions carry "OMITTED — rationale" note)
- [ ] Every section's binary-verifiable criteria satisfied (per the writer-produces spec)
- [ ] §3 row count matches Finding count in source `domain-research.md` (or specialist-fallback content present)
- [ ] §4 directionality matches role's authoring order (OUTBOUND for first foundation role; INBOUND for later)
- [ ] §5 every rule has voice tag + source tag
- [ ] §9 each of 9.1, 9.2 has format spec in shape (a), (b), or (c)
- [ ] §11 all 8 PF entries have in-scope/out-of-scope verdicts
- [ ] §11 anti-patterns count 5–8, each with source + recognition cue
- [ ] §12 BAD/GOOD pairs count 2–4, each cites §11 anti-pattern number
- [ ] §13 every row has status tag (LIVE / REFERENCED / PROPOSED); every LIVE path resolves
- [ ] §15.2 5–10 role-specific criteria; §15.1 references `/upgrade-agent` Phase 7
- [ ] §16 scope restriction stated; only in-scope invariant categories enumerated
- [ ] §17 three subsections present (Risk, Assumptions, Break Conditions)
- [ ] §18 present even if 0 items; every §13 PROPOSED row also appears here
- [ ] Appendix A populated with all Phase-3 red-team findings + Phase-4 verdicts
- [ ] Phase Coverage Matrix (§4 above) instantiated for this role
- [ ] Frontmatter `status: Final (red team reviewed, all findings classified)` set
- [ ] Frontmatter `last-PF-reviewed:` matches latest PF in `memory/process-failures.md`

---

## 8. Adaptation rationale (Quant → Medical)

Brief record of what changed from the Quant `design-doc-protocol.md` to this template.

### Transfers (8 sections / equivalents preserved)

| Quant section | This template | Why transferred |
|---|---|---|
| 1. Problem Statement | §1 | Universal design-doc opener |
| 12. Edge Cases | §14 | Universal; specialized for agent-role context |
| 15. Risk Assessment | §17.1 | Universal |
| 16. Acceptance Criteria | §15 | Universal; restructured to separate inherited vs role-specific |
| 17. Invariants at Risk | §16 | Universal; scope-restricted |
| 18. Assumptions/Break Conditions | §17.2 + §17.3 | Universal; split for clarity |
| 19. Open Questions | §18 | Universal |
| A. Red Team Findings | Appendix A | Universal |

### Dropped (8 sections / Quant-specific to command upgrades)

| Quant section | Why dropped |
|---|---|
| 2. Decision: Modify In Place | Foundation roles are net-new authoring; no prior agent.md to modify |
| 3. What Transfers As-Is | Vacuous for net-new authoring |
| 4. What Must Change | Vacuous for net-new authoring |
| 6. Cross-Phase Dependency Modeling | Agent profiles don't have phases in the Quant Phase-0/Phase-1 sense |
| 7. Carry-Forward Item Integration | Phase-specific concept |
| 9. Pipeline Path Isolation | Agent profiles don't own pipeline state |
| 11. State File Schema Changes | Agent profiles don't have state files |
| 13. Verification Protocol Changes | Phase-specific; subsumed by §13 (Mechanical Enforcement Map) |
| 20. Net Line Count Estimate | Net-new authoring — no delta to estimate |

### Reframed (4 sections / similar function, different shape)

| Quant section | This template | Why reframed |
|---|---|---|
| 8. Interface Contracts (Phase-1 task signatures) | §4 (Cross-Role References) | Agent profile "contracts" are cross-role reference points, not task interfaces |
| 10. Agent Brief Modifications | §9 (Communication Protocol) | Quant means edits to existing pipeline briefs; for new agent design, the format-spec IS the brief |
| 14. Anti-Pattern Updates | §11 (Anti-Patterns) | Quant means updates to existing list; for new agent, fresh authoring |
| 5. What Must Be Added | Distributed across §3 (Pass-1 Digest), §13 (Mechanical Enforcement), §14 (Edge Cases) | "What's added" is role-specific and surfaces per-section, not in one section |

### Net-new sections (5)

| Section | Why added |
|---|---|
| §2 Role Definition | AGENT_TEMPLATE.md requires Identity + Role Boundaries; no Quant equivalent |
| §3 Pass-1 Deliverable Digest | Project has Pass-1 substrate (~49,500 words of research); design doc must anchor against it without paraphrase drift |
| §4 Cross-Role References (Directional) | CONTINUATION_BRIEF §10's 7 cross-role references require explicit per-doc handling; new for medical multi-agent team |
| §13 Mechanical Enforcement Map | INVARIANTS.md "invariants get scripts" principle (lines 14–15) requires a section anchoring mechanical checks |
| §10 Context Loading | AGENT_TEMPLATE.md requires it; no Quant equivalent for agent-role design |

(Sections §5–§9 + §10–§12 are 1:1 AGENT_TEMPLATE.md mappings — they're not "added" in a Quant→Medical sense but they ARE new structural slots compared to Quant's command-upgrade flow.)

---

## 9. Adversarial review provenance

This template was synthesized through the design-doc-protocol Phases 1–5:

- **Phase 1.** Architect-role agent dispatched 2026-05-26; produced proposal at `design/.design-doc-template-work/architect-proposal.md` (422 lines, 18 sections, 12 required content blocks).
- **Phase 3.** `/adversarial-review` skill agent dispatched on the proposal; produced 22 findings (2 Critical, 9 Major, 8 Minor, 3 Nitpick) at `design/.design-doc-template-work/red-team-adversarial.md`. All 11 adversarial categories walked (8 standard + 3 agent-specific). Both mechanical coverage checks (AGENT_TEMPLATE.md + `/upgrade-agent` 8-phase) executed.
- **Phase 4.** Orchestrator personally verified each finding against cited source (PF-S3-01 guard); 16 Legitimate, 4 Legitimate-modified, 2 Rejected. Classifications at `design/.design-doc-template-work/finding-classifications.md`. Rejected findings (F-006, F-023) include source-of-truth attestation.
- **Phase 5.** This document. All Legitimate and Legitimate-modified dispositions applied; Rejected findings documented in §10 below for institutional memory.

---

## 10. Appendix — Rejected red-team findings (institutional record)

Rejected findings are preserved here so a future session can re-evaluate if the basis for rejection changes (e.g., Pass-3 specialist deliverables turn out to have variable R-counts).

### F-006 (REJECTED — empirical premise wrong; fix independently adopted)

**Reviewer's claim.** §3 hardcodes "Pass-1 Recommendations (R1–R15)" but Pass-1 deliverables may have other R-counts. Suggested fix: soften to "R1–R<N>".

**Rejection rationale.** I personally counted R-items in all 4 Pass-1 deliverables: Role 1 = 15, Role 2 = 15, Role 3 = 15, Role 4 = 15. Empirically uniform. The reviewer's claim that R-count varies across roles is factually wrong for the current consumers (the 4 foundation roles).

**Source-of-truth attestation.** Role 4 deliverable lines 414–442 verified directly (R1 through R15, no R16). Roles 1/2/3 R-counts verified via `grep -cE "^\*\*R[0-9]+" design/.{role}-design-work/domain-research.md` returning 15 for each.

**Why the fix was independently adopted.** The 14 Pass-3 specialists haven't been authored yet; their R-counts are unknown. Hardcoding R1–R15 today would not break any current consumer, but the softer "R1–R<N>" phrasing is a free defensive improvement for hypothetical future R-count variance. The fix is adopted because its value is independent of the finding's premise — not because the finding was correct.

**Discipline note (per S7 feedback memory).** Judge the claim and the fix separately. Rejecting a finding while independently adopting its proposed fix is a recognized pattern; the classification reflects the empirical claim, not the fix's downstream value.

### F-023 (REJECTED — copy-edit, not structural)

**Reviewer's claim.** §7 of the proposal (worked example) phrases Role 4's 3-axis severity as "most complex" in a way that reads as ranking Role 4 above Role 3, when Role 3 is actually 4-axis.

**Rejection rationale.** The phrasing IS awkward, but §7 was the proposal's own worked example — its prose does not propagate into this synthesized template. The synthesis output is this template; the proposal's §7 is not preserved as-is. Addressing the awkward phrasing is an editorial pass at synthesis time, not a Legitimate-or-Rejected classification of a structural defect that propagates to 18 downstream artifacts.

**Source-of-truth attestation.** Role 3 deliverable line 31 confirms 4-axis; Role 4 deliverable line 161 confirms 3-axis. The complexity comparison is qualitative, not orderable.

---

## 11. Template change discipline

This template is the contract; the design docs are implementations. Changes to this template require:

1. Cite the section being changed.
2. Present new evidence (failure observation, downstream gap, etc.).
3. Explicit user approval.
4. Append a Change Log row below with date / section / old / new / evidence / session.
5. Re-evaluate every existing design doc against the change (if any design docs have already been written against the prior template version).

### Change Log

| Date | Section | Change | Evidence | Session |
|---|---|---|---|---|
| 2026-05-26 | (initial) | Template created | Pass-1 deliverables complete; need adapted structure for Pass-2 | S7 |
