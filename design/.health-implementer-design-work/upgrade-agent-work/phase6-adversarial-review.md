# Phase 6 — Adversarial Review: health-implementer agent profile

**Review target (reviewed as a unit):**
- `.claude/agents/health-implementer/agent.md` (162 lines, 4,889 cl100k tokens)
- `.claude/agents/health-implementer/library-index.md` (24 lines)

**Ground truth:** `design/health-implementer-design.md` (Final, 780 lines); `skills_library/roles/AGENT_TEMPLATE.md`; sibling `.claude/agents/health-specialist-architect/agent.md`; `memory/process-failures.md`.

**Method:** adversarial-review skill 8 document categories + 4 agent-specific criteria (operational completeness, scope creep, token economics, personality traps). Mechanical checks run: PF resolution, section count, voice-register greps, tiktoken count, per-section token cost, mode-floor source cross-check.

**Mechanical baseline (verified, not asserted):**
- 11 `## ` sections — matches the 10-base+Modes expectation. PASS.
- All 5 cited PF IDs (PF-S2-01, -S2-04, -S2-05, -S3-01, -S6-01) resolve in `memory/process-failures.md`. Anti-Patterns section carries 4 distinct PFs (≥3 floor met). PASS.
- Own-voice aggressive-modal usages: 0 (the 3 hits at L16/L101/L138-140 are MENTIONS — AQ-002, not re-litigated). `you-modal` budget = 3 (≤3 ceiling, exactly at limit). PASS.
- AUTHORITY_FRAMING_BYPASS present (L17). Jaccard/IDENTICAL discipline referenced. 3 Negative-Example BAD/GOOD pairs. PASS.
- `wc -l` = 162 (≤200 line ceiling). PASS. **tiktoken = 4,889 (FAILS the ≤2,500 binary the profile itself states in Core Rule 3, and ~2.4× the /upgrade-agent ~2,000 target).** See AR-001.

---

### AR-001: Profile self-violates the token binary it instructs (Core Rule 3)

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradiction / token economics |
| **Severity** | High |
| **Section** | Core Rules (L15) + profile-wide |
| **Resolution** | Prevent (partial — see token-economics verdict) |
| **Affected File** | agent.md |

**Description:** Core Rule 3 states "Hold the body at ≤200 lines / ≤2,500 tokens; target 150–180. Binary: `wc -l` ≤200; tiktoken ≤2,500." The deployed profile is 4,889 tokens — 1.96× its own stated ceiling. The rule is authored in the implementer's standing voice and reads as a discipline the implementer holds; a fresh agent loading this profile sees a role that broadcasts a 2,500-token discipline from inside a 4,889-token artifact. Even reading Rule 3 charitably as "the budget I enforce on the *specialists* I author" (which the design intends — it is the specialist body ceiling, §13 row 3), the profile gives no signal that the implementer's OWN budget differs, and §15.1 of the design separately names ≤2,000 as the /upgrade-agent generic constraint for *this* file. Either reading leaves the artifact roughly 2× over.

**Evidence:** L15: `3. Hold the body at ≤200 lines / ≤2,500 tokens; target 150–180. Binary: wc -l ≤200; tiktoken ≤2,500. [Finding 3, R3, R3]` — measured 4,889 tokens.

**Fix:** Bring the body toward target via the REDUCIBLE cuts in the token-economics verdict below (est. ~600–850 tokens recoverable without touching a safety threshold or a mechanical binary). The residual overrun above ~2,000 that is genuinely load-bearing medical-domain content should be dispositioned explicitly in HANDOFF/bead 2qq as an accepted, justified exception — not left as a silent contradiction against Rule 3. If the implementer's own ceiling is intentionally higher than the specialist ceiling it enforces, state that distinction in one clause so Rule 3 does not read as self-applying.

---

### AR-002: Mode-floor values hardcoded in §Tools duplicate the authoritative YAML and risk drift

| Field | Value |
|-------|-------|
| **Category** | D — Downstream Breakage / R — Broken Reference |
| **Severity** | Medium |
| **Section** | Tools (L58–62) |
| **Resolution** | Prevent |
| **Affected File** | agent.md |

**Description:** §Tools hardcodes three mode-floor values (peptide→deep, sleep-coach→standard, labs→standard). The authoritative source is `templates/specialist-risk-class.yaml` (14 specialists, owned by this very role), which library-index.md already routes to. The hardcoded trio is an illustrative subset masquerading as a table: it is the *only* in-body source a careless reader sees, it omits 11 specialists, and if the YAML floor changes (e.g., longevity-strategist is `deep` in the YAML but absent here) the body silently drifts from canon. The design's own EC-5 names "mode floor wrong default" as the failure this role must prevent — embedding stale defaults in the role's own profile is the same anti-pattern at the meta layer. Cross-checked: the 3 values match the YAML today, so this is a latent drift hazard, not a current error.

**Evidence:** L58–62 list three `→ --mode=` pairs; `templates/specialist-risk-class.yaml` carries all 14 with rationale; library-index.md L10 already cites the YAML as the load-point.

**Fix:** Replace the hardcoded trio with a single pointer: "Per-role floors are read from `templates/specialist-risk-class.yaml` (this role owns it); never hardcode a floor in this profile." Keep at most peptide→deep as the one worked example tying to Core Rule 5a. Saves ~40 tokens and removes the drift surface. (Caution: AC-deploy-13 greps for ≥3 of a named specialist set in *this* file — confirm the AC is repointed at the YAML, or keep exactly 3 example pairs, before cutting all of them. Flag to correction agent.)

---

### AR-003: Core Rule 10 fuses three distinct obligations into one ~190-token rule

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions / L — Language Economy |
| **Severity** | Medium |
| **Section** | Core Rules (L22) |
| **Resolution** | Prevent |
| **Affected File** | agent.md |

**Description:** Core Rule 10 carries (a) the three-mechanism anti-sycophancy encoding, (b) the IDENTICAL/DIFFER bright-line partition with its full contents enumeration, and (c) a re-read-the-design-doc-at-each-boundary process discipline — three obligations with three different binaries crammed into one rule. The closing binary ("three distinct mechanism-keyed grep matches") only validates clause (a); clauses (b) and (c) have no binary in Rule 10, yet they are stated with equal force. A reader executing "Rule 10's binary" verifies one third of the rule. The design separates these cleanly (§5 rules 10, 11, 12 are three rules); the compression into one fused rule loses the rule/binary 1:1 mapping the role's own Rule 6 demands.

**Evidence:** L22 begins "Anti-sycophancy is encoded against three named mechanisms…" and ends "Binary: three distinct mechanism-keyed grep matches in IDENTICAL block." — the IDENTICAL/DIFFER partition and the "re-read at each section boundary" discipline sit between, unbinaried.

**Fix:** Split into the three rules the design already separates (§5 r10/r11/r12). This costs net tokens but is the correct fix for an agent-profile whose Rule 6 mandates check-paired-prose; if token budget forbids three rules, at minimum move the "re-read design doc at each section boundary" clause into §Context Loading (where its sibling already lives at L96) and the IDENTICAL/DIFFER partition into §Role Boundaries (where it already partly lives at L26), leaving Rule 10 as the anti-sycophancy rule with its matching binary. Net REDUCIBLE ~60–90 tokens by de-duplicating against L26 and L96.

---

### AR-004: "Author the mechanical check before the section prose" has no how for the implementer's OWN profile

| Field | Value |
|-------|-------|
| **Category** | Operational completeness / E — Edge Case Gap |
| **Severity** | Low |
| **Section** | Core Rules (L18), Anti-Patterns (L103) |
| **Resolution** | Handle |
| **Affected File** | agent.md |

**Description:** Core Rule 6 and Anti-Pattern 4 both instruct "author the grep/wc/schema check before the prose," targeting the *specialist* files the implementer writes (those get `**Mechanical Check:**` stubs per §13 row 7). But the implementer's own profile carries no per-section `**Mechanical Check:**` stubs — the binaries are inlined into Core Rules instead. A fresh agent could read Rule 6 as self-applying ("where are MY section checks?") and either retrofit stubs the profile doesn't use or stall. The verb "author the check first" has a concrete how for specialists (the stub format) but the profile models a *different* format for itself (inline binaries) without saying so.

**Evidence:** L18 Rule 6 + L103 AP4 both say "the grep/wc/schema assertion comes first"; the profile's own sections use inline `Binary:` clauses, not `**Mechanical Check:**` stubs — the two formats are never reconciled.

**Fix:** One clause clarifying the target: "This discipline applies to the per-section `**Mechanical Check:**` stubs in the specialist files I author; my own profile inlines binaries into Core Rules." Costs ~20 tokens; closes the self-application ambiguity.

---

### AR-005: §Communication "MUST NOT" is the only all-caps directive and is unscoped to a surface

| Field | Value |
|-------|-------|
| **Category** | A — Ambiguous Instructions |
| **Severity** | Low |
| **Section** | Communication (L86) |
| **Resolution** | Accept (or trivial prevent) |
| **Affected File** | agent.md |

**Description:** L86 "The 7 orchestrator fields are orchestrator-internal; MUST NOT appear in user-facing outputs." The `MUST NOT` is not a banned-aggressive token (the regex bans `YOU MUST`, not bare `MUST NOT`), so it passes the voice audit — verified. But it is the single all-caps modal in the profile's own voice, and the sibling architect profile expresses the identical constraint in the same all-caps form (L81), so it is a deliberate house convention, not a slip. Noted for completeness; the constraint itself is correct and load-bearing.

**Evidence:** L86 vs sibling L81 — identical phrasing. Voice-register grep for banned tokens returns 0 (confirmed).

**Fix:** Accept. If house style later bans bare `MUST NOT`, lowercase to "must not." No action required now.

---

### AR-006: "Walter is A3, 81.8%-of-attacks vector" inlines operator-identity into Core Rule 5

| Field | Value |
|-------|-------|
| **Category** | S — Scope Violation |
| **Severity** | Medium |
| **Section** | Core Rules (L17) |
| **Resolution** | Prevent |
| **Affected File** | agent.md |

**Description:** This is the sharpest internal tension in the profile. Core Rule 5 justifies the mandatory AUTHORITY_FRAMING_BYPASS class with "(Walter is A3, 81.8%-of-attacks vector)". The profile's *entire* §Context-Loading L94 NOT-auto-load block, Anti-Pattern 3 (L102), and Negative Example 3 (L148-162) exist to forbid exactly this: inlining operator identity ("Walter") into a profile body rather than referencing operator-profile at runtime. Anti-Pattern 3's recognition cue is literally "copying a WIKI.md parenthetical like '(Jan 2026 issue)' into Identity." Naming "Walter" in a Core Rule is the same class of leak — operator state hardcoded into authored prose. The design uses the same phrasing (§5 rule 5, §4.1 row 1), so this is inherited, not invented; but the design naming it does not make it consistent with the profile's own AP3. A fresh agent sees "never inline operator state" (AP3) and "Walter is A3" (Rule 5) and cannot reconcile which governs.

**Evidence:** L17: "…`AUTHORITY_FRAMING_BYPASS` mandatory among them (Walter is A3, 81.8%-of-attacks vector)…" vs L102 AP3: "I don't bind operator state at the implementer layer… copying a WIKI.md parenthetical like '(Jan 2026 issue)' into Identity."

**Fix:** Depersonalize the rationale: "(the single-operator threat model classes the operator as A3; AUTHORITY_FRAMING_BYPASS is the 81.8%-of-successful-attacks vector per Role 1 §2.2)." This keeps the load-bearing threat-model fact and the percentage (both justify the mandatory class) while removing the operator's proper name from a standing Core Rule, resolving the AP3 contradiction. Net ~0 tokens. NOTE: this is a *threat-model* fact (A3 = "operator-self-harm-via-own-agent"), arguably distinct from operator *medical* state (Jan 2026 issue) which AP3 targets — but the proper-name leak is real either way and trivially removable.

---

### AR-007: library-index.md says audit script "does not yet exist"; agent.md treats it as conditionally LIVE

| Field | Value |
|-------|-------|
| **Category** | C — Internal Contradiction (cross-file) |
| **Severity** | Low |
| **Section** | library-index.md L11 vs agent.md L54/L92 |
| **Resolution** | Handle |
| **Affected File** | library-index.md + agent.md |

**Description:** library-index.md L11 states the audit script is "PROPOSED — does not yet exist (design §13 rows all PROPOSED)." agent.md §Tools L54 and §Context-Loading L92 both gate audit-script use on "(when LIVE)". These are consistent in intent (both acknowledge the script is not live), but a reader of agent.md alone does not learn the script is *currently absent* — only that it should be used "when LIVE," which reads as a future-tense conditional rather than a present-tense "this does not exist yet." Core Rule 9 ("Run the audit script on my own output before return… Binary: returned frontmatter `audit_passed: true`") then states an unconditional return-gate against a script that cannot run today. A fresh implementer dispatched now would hit Rule 9, find no script, and have no in-profile instruction for that state (Loop-Breaking's audit-failure threshold covers crash/non-zero, not absence).

**Evidence:** library-index.md L11 "does not yet exist" vs agent.md L21 Core Rule 9 unconditional "Binary: returned frontmatter `audit_passed: true` with audit-run artifact path."

**Fix:** Add a script-absent branch to §Loop-Breaking audit-failure threshold or Core Rule 9: "If the audit script does not yet exist (PROPOSED per design §13), return with `audit_passed: deferred-script-absent` + the AQ/bead reference; do not fabricate `audit_passed: true`." This prevents a fabricated-pass under the fabrication guard. ~25 tokens.

---

### AR-008: §Loop-Breaking dual-gate names "v1-substitute software-security agent" with no resolution path

| Field | Value |
|-------|-------|
| **Category** | E — Edge Case Gap / R — Broken Reference |
| **Severity** | Low |
| **Section** | Loop-Breaking (L50) |
| **Resolution** | Accept |
| **Affected File** | agent.md |

**Description:** L50: "Pre-Role-4, the v1-substitute software-security agent verdict log stands in. [PF-S3-01 medical analog, CB §7]". The profile references a v1-substitute verdict log and "CB §7" but gives no path for the log and no in-profile definition of CB. The design resolves both (§17.2 A-6, A-9 give the log schema + path `design/.{role}-design-work/v1-substitute-safety-log.json`), but the deployed profile points at neither. A fresh implementer hitting the dual-gate pre-Role-4 knows a log "stands in" but not where to find or write it. Low severity because the dual-gate's *primary* instruction (dispatch Role 4 after audit-PASS) is complete and the v1-substitute is a transitional fallback.

**Evidence:** L50 "the v1-substitute software-security agent verdict log stands in. [PF-S3-01 medical analog, CB §7]" — no path, no CB expansion.

**Fix:** Accept for now (transitional fallback, design carries the detail). If touched: add the log path inline. The CB abbreviation appears once and is opaque to a fresh agent — consider expanding to "CONTINUATION_BRIEF" on first use.

---

### AR-009: Identity paragraph 2 duplicates the §Identity body almost verbatim from the design

| Field | Value |
|-------|-------|
| **Category** | L — Language Economy |
| **Severity** | Low |
| **Section** | Identity (L7) + preamble (L3) |
| **Resolution** | Accept |
| **Affected File** | agent.md |

**Description:** The maintain-position / anti-sycophancy paragraph (L7) and the "do not begin with Great/Absolutely" line (L9) are the standard IDENTICAL-block anti-sycophancy scaffold, correctly present and matching the sibling. Not waste — this is the load-bearing Mechanism-B + RLHF-drift content the design mandates verbatim. Recorded here only to document that the L (Language Economy) probe was applied to Identity and found the density justified, not cuttable.

**Evidence:** L7-L9 match sibling architect L7-L9 structure; design §2.1 mandates this content.

**Fix:** Accept — load-bearing, verbatim-by-design.

---

## AQ-002 disposition soundness (commentary, not a fresh finding)

The orchestrator's disposition (deploy the 3 banned-modal MENTIONS faithfully; make voice-audit AC-deploy-11 mention-aware; beaded) is **sound**. The 3 sites are genuinely teaching/defining occurrences: Core Rule 4's regex literal (L16) and Anti-Pattern 2's regex literal (L101) must reproduce the banned tokens to *be* the ban, and the Negative-Example BAD block (L138-140) must show the prohibited form to teach the GOOD form. A mention-blind grep (current AC-deploy-11: `grep -cE "\b(YOU MUST|...)\b" ... = 0`) would FAIL this correctly-authored profile — so the AC, not the profile, is the defect. The bead to make the audit mention-aware (e.g., exclude fenced code blocks and backtick-wrapped regex literals before counting) is the right fix. One refinement: the mention-aware rule should be specified precisely (fenced-block + inline-backtick exclusion) so it does not become a loophole that lets a real aggressive-modal slip through in prose adjacent to a code fence.

---

## Summary table (counts by severity)

| Severity | Count | IDs |
|----------|-------|-----|
| Critical | 0 | — |
| High | 1 | AR-001 |
| Medium | 3 | AR-002, AR-003, AR-006 |
| Low | 5 | AR-004, AR-005, AR-007, AR-008, AR-009 |
| **Total** | **9** | |

Critical/High = 1/9 (11%) — below the AP-R1 40% inflation trip. No phantom findings; every finding carries a verbatim quote + line ref.

---

## Token-economics verdict

**Measured:** 4,889 cl100k tokens (162 lines). Per-section: Core Rules 911, Tools 569, Context Loading 565, Anti-Patterns 498, Negative Examples 466, Loop-Breaking 449, Role Boundaries 402, Ask-vs-Proceed 363, Communication 321, Modes 147, Identity 104.

**Verdict: MOSTLY LOAD-BEARING with a bounded REDUCIBLE tranche (~600–850 tokens recoverable; lands ~4,050–4,300, still over the ~2,000 target — the residual overrun is genuine medical-domain density, not waste).**

REDUCIBLE (cut without losing any safety threshold or mechanical binary):
- **Mode-floor hardcoded trio → single YAML pointer (AR-002): ~40 tokens.** The values live in `templates/specialist-risk-class.yaml`; library-index already routes there. (Repoint AC-deploy-13 first.)
- **Core Rule 10 de-duplication against L26/L96 (AR-003): ~60–90 tokens.** The IDENTICAL/DIFFER partition is already stated in §Role Boundaries (L26); the re-read-at-section-boundary discipline is already in §Context Loading (L96). Rule 10 restates both. Keep the anti-sycophancy clause + its binary; cut the two restatements.
- **Anti-Pattern / Core-Rule overlap (general): ~150–250 tokens.** Core Rule 6 ≈ Anti-Pattern 4 (prose-first), Core Rule 9 ≈ Loop-Breaking audit-threshold ≈ Anti-Pattern 5 (audit), Core Rule 1/Anti-Pattern 1 (persona-prose) all state the same discipline twice with near-identical recognition cues. The Anti-Patterns section is the right home for "recognition cue" framing; the Core Rules can shed the duplicated cue prose and keep the binary. This is the single largest safe recovery and does not remove any binary.
- **Context Loading verbosity (565 tokens): ~100–150 tokens.** §Context-Loading items restate the PF-S2-04 NOT-auto-load rationale three times (L94 block, plus L96 re-anchor, plus it recurs in Anti-Pattern 3). One canonical statement + pointers suffices.

LOAD-BEARING (do NOT cut to hit a number):
- The 10 Core Rules' **inline binaries** (`wc -w ≤40`, `≥4 grep-resolvable class IDs incl AUTHORITY_FRAMING_BYPASS`, `Jaccard ≤0.30`, `three distinct mechanism-keyed grep matches`, etc.) — each is a mechanical gate the design mandates; cutting any is cutting a safety/consistency check.
- The **three Negative Examples (466 tokens)** — R10 floor is ≥3; each teaches a distinct failure (persona-prose, aggressive-modal, operator-inlining) with the BAD form that the voice audit must learn to tolerate as a MENTION. Cutting drops below the floor.
- The full **§Tools permitted/forbidden surface (569 tokens)** — the forbidden list (vault write paths, state-mutating git, sub-sub-agent, MCP deletes) is the role's containment boundary; each entry maps to a scope-violation the design enumerates.
- The **§Context-Loading NOT-auto-load guard** (one canonical instance) — this is the PF-S2-04 structural defense; it is the most-cited failure surface for this role.
- The **7-field Communication contract + IDENTICAL/DIFFER hash/Jaccard discipline** — downstream orchestrator depends on the exact field set.

**Bottom line:** the profile is over budget primarily because it is a *meta-authoring* role compressing a 780-line design doc that itself encodes 12 Core Rules, 8 refusal classes, GRADE two-axis, three-mechanism anti-sycophancy, IDENTICAL/DIFFER, and a 25-row mechanical-enforcement map. The bulk is load-bearing medical-domain content. The ~600–850 reducible tokens are real and should be recovered (mode-floor pointer + Core-Rule/Anti-Pattern de-duplication), which also resolves AR-001's self-contradiction *direction* even if it cannot fully close the gap to 2,000. Recommend recording the justified residual (~2,000–2,300 over the generic target) as an accepted exception under bead 2qq rather than degrading any binary.

---

## Coverage matrix

| Section | A | E | C | R | O | S | D | L |
|---------|---|---|---|---|---|---|---|---|
| Identity | clean | clean | clean | clean | n/a | clean | clean | AR-009 |
| Core Rules | AR-003,004 | AR-004 | AR-001 | clean | clean | AR-006 | clean | AR-001,003 |
| Role Boundaries | clean | clean | clean | clean | n/a | clean | clean | AR-003(dup) |
| Ask vs Proceed | clean | clean | clean | clean | clean | clean | n/a | clean |
| Loop-Breaking | clean | AR-008 | AR-007 | AR-008 | clean | clean | clean | clean |
| Tools | clean | clean | clean | AR-002 | n/a | clean | AR-002 | AR-002 |
| Communication | AR-005 | clean | clean | clean | n/a | clean | clean | clean |
| Context Loading | clean | clean | AR-007 | clean | clean | clean | clean | (reducible) |
| Anti-Patterns | clean | clean | clean | clean | n/a | clean | clean | (dup w/ Core) |
| Modes | clean | clean | clean | clean | clean | clean | clean | clean |
| Negative Examples | clean | clean | clean | clean | n/a | clean | clean | LB (≥3) |
| library-index (cross-file) | clean | clean | AR-007 | AR-002 | n/a | clean | clean | clean |

**Coverage gaps:** O (Ordering) yielded zero findings after probing — the profile is declarative-rules-dominant, not a step procedure; the one ordered structure (Ask-vs-Proceed decision tree) was walked and is internally ordered correctly (authoritative-source → ownership → feasibility → operator-binding → internal-only → default), matching the design §6. Documented per AP-R6.
