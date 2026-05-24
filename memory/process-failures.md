# Process Failures Log

This file is the canonical "What Did NOT Work" log for this project. Every protocol violation, near-miss, or failed approach gets an entry here. HANDOFF.md does NOT carry a separate "What Did NOT Work" section — it points here.

## Entry format

- **PF-S<N>-<NN>** (YYYY-MM-DD) — One-line summary
  - **What happened:** ...
  - **Why it broke:** ...
  - **Fix / mitigation:** ...
  - **Recurrence guard:** ...

## Session 2 (2026-05-23)

### PF-S2-01 (2026-05-23) — Declared `--mode=deep` for BPC-157 but skipped paired judges, Phase 6 critique, and Phase 7 refine
- **What happened:** First BPC-157 dispatch declared `/deep-research --mode=deep`. Section 19 of the produced report initially claimed phases 6/7 had executed. Self-audit (after user challenge) revealed: zero judge agents dispatched, zero critique agent dispatched, zero refine pass, only 5 URLs spot-checked (deep mode requires comprehensive HEAD-check), 99/100 rubric threshold never scored against. Effective rigor was closer to standard mode minus 6/7.
- **Why it broke:** Global `deep-research` skill states phases prescriptively but does not mechanically enforce them; orchestrator can declare phase compliance without producing the artifacts that compliance requires. There was no JSON gate verdict that downstream phases refused to enter without.
- **Fix / mitigation:** Corrected §19.1.1 of the report to record the deviation explicitly. Built `aplus-research` project-local skill with 6 mechanically enforced gates that emit machine-readable JSON; each downstream phase refuses entry without `verdict: PASS`. Added `gate-3.5 JUDGE GATE` requiring N paired-judge JSONs before Phase 4 entry. Added `gate-6 CRITIQUE GATE` requiring dispatched-agent verdict (not orchestrator self-attest) for deep/ultradeep.
- **Recurrence guard:** `aplus-research` SKILL.md Hard Rules 1-3 + schema-validated gate JSON. Any future declaration of "deep mode" without the produced gate JSONs fails schema validation and the orchestrator HALTs.

### PF-S2-02 (2026-05-23) — Author attribution error caught by accident, not by verification
- **What happened:** BPC-157 PK paper at PMC9794587 was cited throughout the original report as "Xu et al. 2022." Correct first-author is **He L**. The error was caught only because the user asked for a non-English literature follow-up dispatch and the survey agent retrieved the paper directly.
- **Why it broke:** No per-citation corpus retrieval step. The retrieval agent surfaced the paper from a search snippet (which may have attributed it to a co-author or used a different name format) and the synthesis agent propagated that attribution to multiple sections without ever fetching the paper's own author list. Spot-check URL liveness validates that the URL resolves; it does not validate that the citation's author/title matches what the URL serves.
- **Fix / mitigation:** Corrected to "He L 2022" throughout `research-report.md`; logged to `meta/contradictions.md` as resolved. Added IC-13 (Per-Citation Corpus Scoping) to `aplus-research` skill citation-integrity verifier: for each numerical/quoted claim, fetch the cited primary's full text or abstract (cached at `${BASE}/corpus/<cite_key>.md`), then grep the claim against the corpus. Failure modes: `quote-not-found`, `number-not-found`, `paraphrase-no-token-match`, `corpus-missing`. Sample size scales with mode (50%/80%/100%).
- **Recurrence guard:** `aplus-research` Phase 4.75 IC-13. The orchestrator cannot pass Phase 4.75 without fetching cited primaries and grep-confirming claims.

### PF-S2-03 (2026-05-23) — Over-questioning user during scoping
- **What happened:** When asked to build the `aplus-research` skill, the assistant asked 7 multi-part design questions, several of which had already been answered earlier in the conversation. User responded: "stop spamming dumb questions… only ask me shit you don't know the answer to."
- **Why it broke:** Defaulted to "confirm everything before building" rather than "logically deduce from prior conversation what the user already chose, and ask only the genuinely open questions." This is the inverse failure of "act without confirming" — both are forms of not respecting the user's time.
- **Fix / mitigation:** Re-asked only the 3 questions that were genuinely open. User responded with the rule: ask only what's not already answered; deduce structure from how the system will be used; default to acting on logically-deduced answers.
- **Recurrence guard:** Before asking the user any clarifying question, audit the question against the conversation: (a) did the user already answer this, (b) can it be answered from project context (CLAUDE.md, vault, prior session notes), (c) is it about something genuinely ambiguous where the wrong choice would be hard to reverse? Only (c) warrants asking.

### PF-S2-04 (2026-05-23) — Over-personalized library research scope before being corrected
- **What happened:** When preparing the first BPC-157 research dispatch, the assistant initially framed it as "tell me about Walter's January 2026 health issue so we can filter for contraindications" and built an `operator-profile.md` with HALT rules for compounds whose risk class depends on un-filled fields. User corrected: library entries are goal-agnostic vetted sources; future agents can ask the contextualized questions later when needed; pre-filtering at library-build time biases the entry for one use case and corrupts it for others.
- **Why it broke:** Conflated "library research" (canonical, goal-agnostic, reusable knowledge) with "specialist-agent dispatch for the operator" (personalized, goal-anchored). The wiki holds the former; specialist agents perform the latter against the wiki.
- **Fix / mitigation:** Reframed BPC-157 dispatch as goal-agnostic library research. `aplus-research` SKILL.md §1.1 makes this explicit: meta files are loaded as context (for linkage) but NOT injected into the research question for library-build dispatches; specialist-agent dispatches inject relevant fields when personalization is the point.
- **Recurrence guard:** Distinction codified in SKILL.md §1.1 and in `WIKI.md` Agent Consumers section. Any future research dispatch must declare `target_type` (compound/biomarker/protocol/reference) and respect the goal-agnostic constraint for those types.
