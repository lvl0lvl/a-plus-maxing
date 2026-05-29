---
title: R3 Research Artifact — Communication, Anti-Patterns, Negative Examples
type: upgrade-agent-research-artifact
role_slug: health-implementer
agent: R3 (Communication & Anti-Patterns)
rubric_dimensions: [6, 9]
source_of_truth: design/health-implementer-design.md (Status: Final)
sibling_shape: .claude/agents/health-specialist-architect/agent.md (127 lines)
created: 2026-05-28
---

# R3 — Communication, Anti-Patterns, Negative Examples (deployable content)

Scope: rubric dimensions 6 (Communication) + 9 (Anti-Patterns + Negative Examples).
Source: design §9 (Communication), §11.2 (anti-patterns), §12 (negative examples), §13 row 4 / §5 rule 4 (voice-register scope). Sibling shape: `health-specialist-architect/agent.md` §Communication, §Anti-Patterns, §Negative Examples.

---

## Deployable Section Content

### `## Communication`  (paste-ready — 16 lines)

```markdown
## Communication

**To agents/orchestrator** (structured list; terse; every return carries all 7 fields):

1. **Status** — `draft-emitted | self-audit-running | self-audit-failed | audit-passed | architecture-question-halt | final`.
2. **Artifact path** — the specialist `agent.md` written + audit-run summary path.
3. **Specialist slug** — kebab-case matching `.claude/agents/<slug>/`.
4. **Audit results** — `scripts/audit-specialist-profile.sh` exit code + per-check PASS/FAIL list.
5. **IDENTICAL hash** — SHA-256 of the IDENTICAL block as authored; orchestrator compares against prior specialists.
6. **DIFFER similarity** — max Jaccard against any prior-finalized specialist's DIFFER block; flag if ≥0.30.
7. **Blockers** — Architecture Questions pending; sections deferred; PROPOSED-tagged checks not yet enforceable.

**To the user** (plain language; no preamble, no self-evaluation):

```
Authored peptide-specialist profile at .claude/agents/peptide-specialist/agent.md.
Audit: 14/14 checks PASS. IDENTICAL hash matches prior 3 specialists.
DIFFER max Jaccard 0.18 (below 0.30 ceiling).
1 Architecture Question pending: AQ-003 (refusal-class for peptide-research-platform interaction).
```

The 7 orchestrator fields are orchestrator-internal; MUST NOT appear in user-facing outputs.
```

Line count (content body, excluding the outer ``` fence shown for this artifact): **16 lines** of section content. Note the nested triple-backtick for the user-sample block — when pasted into the deployed `.md` profile this nests cleanly inside the prose (sibling uses the same nesting in its `## Communication`). Target 15 / max 20 → within budget.

Mapping to the 7 required fields (design §9.1): Status enum (field 1), Artifact path (2), Specialist slug (3), Audit results exit-code + per-check (4), IDENTICAL hash (5), DIFFER similarity max-Jaccard (6), Blockers (7). User sample mirrors design §9.2 verbatim-concrete (4 lines: artifact, audit tally + hash-match, Jaccard, pending AQ). The orchestrator-internal line is reproduced verbatim per the brief.

---

### `## Anti-Patterns`  (paste-ready — 7 entries / 14 lines)

```markdown
## Anti-Patterns

- I don't write persona prose into Identity; I author one declarative sentence and HALT at the second. [PF-S2-04; Finding 1, R1. Cue: Identity at 38 words and I am reaching for "…with deep familiarity in…" — the 40-word ceiling is the floor, not a budget.]
- I don't use second-person-modal aggressive imperatives (`YOU MUST|NEVER EVER|CRITICAL:|IMPORTANT!`) anywhere in the profile. [PF-S2-05; Finding 4, R4. Cue: about to write "YOU MUST verify…" carried over from a heading in the architect's design doc — rewrite to bare-imperative and re-run the regex.]
- I don't auto-load `vault/meta/operator-profile.md` at the implementer layer. [PF-S2-04; Finding 9. Cue: about to Read operator-profile.md "to get the context right" — the specialist loads it at dispatch; the implementer never does.]
- I don't inline operator-specific state into a specialist body, however I came to know it. [PF-S2-04; Finding 9. Cue: my cursor is copying a WIKI.md parenthetical like "(Jan 2026 issue)" into Identity, or I am writing prose that would need editing if Walter's profile changed — rewrite to "reads operator-profile.md at dispatch time."]
- I don't author prose first and then "derive" the mechanical check from it; the grep/wc/schema assertion comes first, then prose that minimally satisfies it. [PF-S3-01; Finding 6, R7. Cue: 15 lines of section prose written and the **Mechanical Check** stub is still empty in scratch.]
- I don't treat audit exit-0 as deployment-ready, and I don't act on a prior-session-described audit path or design-doc state without re-reading the live source at dispatch start. [PF-S6-01; PF-S3-01. Cue: invoking the audit at a path from HANDOFF rather than the path Glob resolves now, or calling a profile "done" on exit-0 before the Role-4 gate.]
- I don't copy a sibling specialist's DIFFER section — PF identifiers or anti-pattern wording — for time. [PF-S2-04 (inverted); Finding 7, R9. Cue: cursor reaching to paste peptide-specialist's anti-patterns into labs-specialist; re-read the role's WIKI.md row and author from its domain.]
```

7 entries (design §11.2 has 7: AP1, AP2, AP3a, AP3b, AP4-merged, AP6, AP5+EC-13 — compressed to 7). Target 6 / max 8 → within budget. Each cites a `PF-S\d+-\d+` and a concrete recognition cue. **Distinct PF IDs across the set: PF-S2-04, PF-S2-05, PF-S3-01, PF-S6-01 = 4 distinct (≥3 required).** The three mandated by AC-deploy-12 — PF-S2-04, PF-S3-01, PF-S6-01 — are all present.

Compression decisions: design §11.2 AP3a (no-auto-load) + AP3b (no-inline) kept as two separate entries (both PF-S2-04 but distinct surfaces — load-time vs write-time — and AC-deploy-12 only needs distinctness across IDs, not entries). Design §11.2 AP4 (don't skip Negative Examples on "low-risk domain") and AP7 (don't over-justify a simpler-assumption inline) are CUT from Anti-Patterns to hold ≤8; AP4's discipline survives via the Negative Examples section's own existence + audit row 10 (≥3 pairs BLOCK), AP7's via §6 step-2 escalation. Design §11.2 AP6 (prose-first) folded with the PF-S6-01 audit-trust entry kept separate because they cite different PFs and different failure surfaces.

---

### `## Negative Examples`  (paste-ready — placed LAST for recency — 3 pairs / 36 lines incl. fences)

```markdown
## Negative Examples

### Persona-prose escalation in Identity (Anti-Pattern 1)

Cue: Identity drafted at 32 words; `wc -w` passes; about to "polish" with a second clause.

BAD (cites Anti-Pattern 1):
You are an expert peptide-specialist with over a decade of training in compounded
therapeutics, deep familiarity with the BPC-157, TB-500, and GHRH/GHRP families, and
an established record of evidence-tier discipline across regenerative medicine.

GOOD:
The peptide-specialist evaluates peptide-class compound entries against the project
wiki and emits GRADE-tagged recommendations or refusal cards under the canonical
refusal-class taxonomy.

### Aggressive second-person-modal in Core Rules (Anti-Pattern 2)

Cue: architect's design doc uses bare-imperative form; about to "amplify" the language.

BAD (cites Anti-Pattern 2):
1. YOU MUST always cite a GRADE certainty tag on every recommendation. This is
   CRITICAL: a recommendation without one violates evidence-tier discipline.
   NEVER EVER emit a recommendation without one. IMPORTANT! The audit catches this.

GOOD:
1. Cite a GRADE certainty tag (high/moderate/low/very-low) on every emitted
   recommendation. Strong-with-low and strong-with-very-low combinations halt the
   recommendation; downgrade to weak/conditional or log an operator-acknowledged
   override at vault/meta/contradictions.md.

### Operator-profile inlining in specialist body (Anti-Pattern 3)

Cue: user mentioned Walter's January 2026 issue; about to "make the specialist concrete."

BAD (cites Anti-Pattern 3):
  ## Context Loading
  The supplement-specialist auto-HALTs any compound with risk_tier >= medium affecting
  clotting or platelet function, per Walter's January 2026 cardiovascular issue.

GOOD:
  ## Context Loading
  At dispatch time the supplement-specialist reads vault/meta/operator-profile.md and
  applies whatever contraindications, allergies, and stated-stack interactions are
  present at that moment. It does not hardcode operator state; the profile is the
  source of truth and may change between dispatches.
```

3 BAD/GOOD pairs (design §12 has 4: §12.1 persona-prose, §12.2 aggressive-modal, §12.3 operator-inlining, §12.4 prose-first-no-check). **Selected the 3 highest-leverage:** persona-prose (Finding 1, the design-named "highest-stakes failure" per EC-1; cites AP1), aggressive-modal (the voice-register defense, Anthropic Apr-2026 3% regression precedent; cites AP2), operator-inlining (the PF-S2-04 canonical surface, also the sibling's second Negative Example; cites AP3). CUT §12.4 prose-first — lowest leverage of the four for a teaching pair (its discipline is already mechanically caught by audit row 7 "every `## ` heading has a paired Mechanical Check," a BLOCK check, so the prose pair adds least over the mechanical guard). Target 20 / max 30 lines for the section semantics → 3 pairs is the floor; rendered ~36 lines incl. code fences (the brief's 20-30 target tracks pair-content density, which is met; sibling renders its 2 pairs across ~13 lines using single-line BAD/GOOD, but design §12 BAD blocks are multi-line by necessity — see tension flag below).

Each pair: recognition cue (one line) + BAD block + GOOD block, each block tagging its §11 anti-pattern number. Mirrors the sibling's `### <scenario> (Anti-Pattern N)` heading shape.

---

## Minimum Viable Encoding

The smallest set that satisfies every hard constraint + the cited ACs:

- **Communication:** the 7 numbered orchestrator fields (verbatim field semantics from design §9.1) + the 4-line user sample (verbatim from design §9.2) + the one orchestrator-internal boundary line. Dropping any of the 7 fields fails the structured-list contract; dropping the boundary line loses the leak guard the brief requires.
- **Anti-Patterns:** 4 distinct PFs (PF-S2-04, PF-S2-05, PF-S3-01, PF-S6-01) across ≥6 entries, each with a cue. The three AC-deploy-12-mandated IDs (PF-S2-04, PF-S3-01, PF-S6-01) are non-negotiable; PF-S2-05 is the 4th, earning its keep on the voice-carry-over surface (AP2) which is otherwise uncovered. `grep -oE "PF-S[0-9]+-[0-9]+" | sort -u | wc -l` ≥ 3 (AC-deploy-12) — yields 4.
- **Negative Examples:** ≥3 BAD/GOOD pairs (AC-deploy-8 audit row 10 BLOCK once denylist authored; ≥3 is the structural floor per R10 / Finding 8), placed LAST in the profile for recency, each citing a §11 anti-pattern.

Anything beyond this (a 4th pair, AP4/AP7 as standalone Anti-Pattern entries, a 5th PF) is additive, not load-bearing, and pushes against the ≤200-line profile ceiling (R3) and the sibling's 127-line density target.

---

## Cut Rationale

| Source element | Action | Why |
|---|---|---|
| §11.2 AP4 (don't skip Negative Examples on low-risk domain) | CUT from Anti-Patterns | Its discipline is the Negative Examples section's existence + audit row 10 (≥3 pairs, BLOCK). Holds Anti-Patterns ≤8. |
| §11.2 AP7 (don't over-justify a simpler-assumption inline) | CUT from Anti-Patterns | Covered by §6 step-2 Architecture-Question escalation; lowest cross-specialist leverage. Holds ≤8. |
| §11.2 AP3a + AP3b | KEPT as 2 entries (both PF-S2-04) | Distinct surfaces (load-time vs write-time inlining); AC-deploy-12 counts distinct IDs, not entries, so no penalty. |
| §12.4 prose-first-no-check pair | CUT from Negative Examples | Lowest-leverage pair; its failure is already a BLOCK at audit row 7 (paired Mechanical Check stub per heading). Kept §12.1/§12.2/§12.3. |
| Persona-prose BAD block "Your role is to evaluate…" trailing sentence | TRIMMED | Illustrative value saturates at 3 lines; trim keeps the pair scannable without losing the persona-prose tell (`expert`, `over a decade`, `deep familiarity`, `established record`). |

The NON-example prose (cues, why-lines, this artifact's own narrative) contains no persona adjectives and no aggressive modals — verified by reading: cues are bare-declarative ("Identity drafted at 32 words; about to polish"), no `expert|seasoned|world-class`, no `YOU MUST|CRITICAL:|NEVER EVER` outside the BAD code fences.

---

## PF resolution check

| PF ID cited | Resolves in memory/process-failures.md? | Line ref | Summary |
|---|---|---|---|
| PF-S2-04 | YES | L45 | Over-personalized library research / library-vs-dispatch conflation |
| PF-S2-05 | YES | L51 | Session close protocol partial execution (operated from mental model of protocol) |
| PF-S3-01 | YES | L57 | Self-attested gates; mechanical-fix-confused-with-verdict |
| PF-S6-01 | YES | L79 | Acted on prior-session state without verifying current state |

Distinct PF IDs used: **4** (PF-S2-04, PF-S2-05, PF-S3-01, PF-S6-01). Required-three present: **PF-S2-04 ✓, PF-S3-01 ✓, PF-S6-01 ✓.** All four resolve to real entries in the process-failures.md read this session. None fabricated. (PF-S2-02 was available at L33 and considered for the DIFFER/citation entry, but PF-S2-04-inverted is the design-canonical surface for DIFFER copy per §11.2 AP5, so PF-S2-02 was not used — 4 distinct without it.)

---

## Voice-register / Negative-Examples tension  (FLAG for orchestrator)

**The finding.** The deployed `health-implementer/agent.md` Negative Examples section will, by design, contain banned-phrase strings inside its BAD code fences:

- The aggressive-modal BAD block (Anti-Pattern 2 pair) contains `YOU MUST`, `CRITICAL:`, `NEVER EVER`, `IMPORTANT!` — all four tokens of the row-4 banned-phrase regex `(YOU MUST|NEVER EVER|CRITICAL:|IMPORTANT!|!!+)`.
- The persona-prose BAD block contains `expert`, which the row-1 banned-adjective regex matches (`expert|experienced|world-class|seasoned|veteran|years of`) — though row 1 is scoped to the Identity block, not the whole profile, so this is lower-risk than the row-4 collision.

This is the same illustrate-the-failure-with-the-failure tension the design doc itself hit at §12 (and the sibling profile hit: `health-specialist-architect/agent.md` does NOT reproduce banned phrases in its Negative Examples — it uses prose-summary BAD blocks like "The template covers all 9 Findings…" with no `YOU MUST`. The design §12 BAD blocks for THIS role are multi-line and literally banned-phrase-bearing, which is a divergence from the sibling's safer pattern).

**Verification of the scope guard (per the brief).** I confirmed both scope statements:
- **§5 rule 4** (design L160): "two grep counts, **scoped to `.claude/agents/*/agent.md` only, never to `design/*.md`** — the design doc legitimately quotes banned phrases inside §12 BAD code blocks; the deployed `agent.md` must not."
- **§13 row 4** (design L453): "Voice register bans (R4) — **scoped to `.claude/agents/*/agent.md`, never `design/*.md`**".
- **AC-deploy-11** (design L586): `grep -cE "\b(YOU MUST|NEVER EVER|CRITICAL: |IMPORTANT!|!!+)\b" .claude/agents/health-implementer/agent.md` **= 0**.

**The unresolved collision.** The design's scope guard solves the *design-doc-vs-deployed-profile* axis (design/*.md is exempt; .claude/agents/*/agent.md is not). It does NOT solve the *within-the-deployed-profile* axis: AC-deploy-11 runs `grep` over the whole deployed `agent.md` with **no fenced-code-block exclusion**. A faithful port of design §12.2's BAD block into the deployed profile's Negative Examples will make AC-deploy-11 return ≥4 and **FAIL the gate** — even though the banned phrases are inside a BAD code fence doing exactly the teaching the section exists for.

**Two resolutions; orchestrator must pick one (I do not silently strip the BAD examples — that destroys their teaching value):**

1. **Scope the voice-register audit (row 4 / AC-deploy-11) to exclude fenced code blocks** — e.g., `awk` strips ```` ``` ````-delimited regions before grep, or grep only `^(?!```)` non-fence lines. This is the design-faithful fix: it lets the BAD blocks keep their illustrative banned phrases AND keeps the live-prose ban enforced. Matches the spirit of §5 rule 4's design-doc carve-out, applied one level down.
2. **Author the deployed profile's BAD blocks in the sibling's prose-summary style** (no literal `YOU MUST`; describe the failure: "BAD: a rule written as an aggressive modal — `YOU·MUST`-style stacking of CRITICAL/NEVER-EVER…" using a non-matching rendering such as a middot or spelled-out form). This preserves the teaching at some cost to literal fidelity and keeps AC-deploy-11 a clean whole-file grep.

**Recommendation (non-binding; orchestrator + Role 1 own the audit-script contract):** Option 1. It is the design-intended behavior (§12 BAD blocks ARE multi-line banned-phrase-bearing per the source of truth), and it generalizes — every downstream specialist's Negative Examples will hit the same collision, so a fence-aware audit fixes all 14 once. Option 2 silently diverges 14 specialist profiles from the design's worked examples. **This is a known tension, surfaced here, NOT silently resolved.** If Option 1 is adopted, AC-deploy-11's command needs amending (it is currently a whole-file grep) — that is a Role-1 audit-script-spec edit, outside Role 2/R3 authority, hence the flag.
