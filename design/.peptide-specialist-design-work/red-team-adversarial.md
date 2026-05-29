---
title: Adversarial Review — peptide-specialist-design.md
type: red-team-findings
method: /adversarial-review 8-category walk
reviewer: adversarial-review agent
date: 2026-05-29
doc-under-review: design/peptide-specialist-design.md
substrate: design/.peptide-specialist-design-work/domain-research.md
---

# Adversarial Review — peptide-specialist Design Doc

Read in full (483 lines). References verified against the actual cited files (see Category 4). Reward-hacking note: where a category has no finding, the specific check that returned clean is stated.

---

## 1. Ambiguity

**AMB-1 (Minor) — §6 step 6 / §6.6 "simpler assumption" is undefined for a safety agent.**
*Location:* §6 Default step ("proceed with the simpler assumption, state it explicitly").
*Issue:* For a safety-floor specialist, "simpler" is ambiguous — simpler-to-reason vs more-conservative are opposite directions. A synthesizer could encode "pick the less-restrictive reading," which inverts the safety posture. Every other step in §6 HALTs or refuses; only the default is permissive and under-specified.
*Why it matters downstream:* `/upgrade-agent` Phase 5 will reproduce the Ask-vs-Proceed tree near-verbatim; an ambiguous default in a medical refusal tree is the worst place to leave interpretation open.
*Suggested direction:* bind "simpler" to "more conservative / safer reading" explicitly, or scope the default to non-safety internal-wording ambiguity only (the second clause already gestures at this — make it the whole rule).

**AMB-2 (Minor) — "the inherited contract worked example reasons BPC-157 as high as H2" creates a floor/ceiling ambiguity (§4 row 2, §6 rule 6).**
*Location:* §5 rule 6 + §4 H-class row + §150 "must not under-anchor below H2."
*Issue:* The text says angiogenic peptides reason "to at least H3" but the worked example "reasons BPC-157 as high as H2; a downstream author must not under-anchor below H2." H-class ordering is unstated in this doc (is H2 worse than H3, i.e., lower number = worse?). A synthesizer that doesn't know the ordinal direction cannot encode the "auto-block at H1/H2" + "floor at H3" rule coherently — "at least H3" and "as high as H2" are only consistent if H2 > H3 in severity, which the doc never states.
*Why it matters downstream:* the `h-class-composition` audit row (WARN, frontmatter-gated) checks for the field's presence, not its ordinal logic — so a synthesized profile encoding the wrong direction passes the audit but is semantically inverted.
*Suggested direction:* state the ordinal direction once (H1 most severe → H8 least) at first H-class mention, and reconcile "at least H3" vs "as high as H2" into one anchor statement.

**AMB-3 (Nitpick) — §5 preamble voice budget vs audit semantics.**
*Location:* §5 preamble: "non-aggressive `you <modal>` ≤3."
*Issue:* The audit's `voice-register` check WARNs (does not BLOCK) at >3 and matches `you (must|should|will|are|need to|have to)`. The design doc's §5 text presents ≤3 as a hard budget without noting it is WARN-only, and "you are" counts toward it (the synthesized Identity "You are the peptide-specialist" already consumes one). A synthesizer treating ≤3 as a BLOCK budget may distort prose unnecessarily.
*Suggested direction:* annotate the budget as WARN-tier and note "you are" counts.

---

## 2. Edge Cases

**EC-MISS-1 (Major) — no edge case for an APPROVED-rung peptide query (the maturity-ladder top rung).**
*Location:* §14 EC-4..EC-8 all assume preclinical/experimental compounds; §17.2 assumption 6 + §18 OQ-3 both flag that approved peptides (tesamorelin, bremelanotide) and trial-stage agents (retatrutide, MK-677) sit at a different rung, but §14 has no edge case exercising the `approved_indication` ≠ `queried_use` split (§5 rule 1, R2).
*Issue:* §5 rule 1 mandates `approved_indication` distinct from `queried_use` for approved entries, and R2 is ACCEPTED, but no §14 case or test stimulus exercises an approved-rung compound. The uniform anti-pattern set (OQ-3) could over-block an approved on-label use, and there is no test stimulus to catch that.
*Why it matters downstream:* §15.2 criterion 3 requires every ACCEPTED Finding to have a traceable consumer; R2/Finding 1's approved-rung branch has a §5 rule but no §14 test — the consumer is thin and untested.
*Suggested direction:* add an EC for "operator asks about an approved-indication peptide for an off-label queried use" with expected `approved_indication`≠`queried_use` handling.

**EC-MISS-2 (Minor) — Loop-Breaking §7 dispatch-loop cap interacts with EC-2 but the interaction is unspecified.**
*Location:* §7 "Dispatch-loop cap (numeric, 2)" vs §14 EC-2 (dispatch on not-in-wiki peptide).
*Issue:* EC-2 says dispatch `aplus-research` and write the entry; §7 says after 2 dispatches returning only vendor/anecdote/single-lab evidence, mark `evidence_tier: D` / `status: excluded`. The behavior when a NEW peptide (EC-2) hits the dispatch cap (§7) — i.e., a never-before-seen peptide that returns only inadmissible evidence twice — is not stated: does it get a `status: excluded` stub entry, or no entry at all? The two rules touch but don't compose.
*Suggested direction:* state the terminal artifact when EC-2 + §7 cap coincide (stub entry with `status: excluded` + recorded gap is the likely intent).

**EC-MISS-3 (Minor) — no failure mode for a contradiction between the live operator-profile and a hard-limit already encoded in a compound entry.**
*Location:* §6 step 2 + §11.1 PF-S6-01 row + §14 EC-1.
*Issue:* The doc covers "operator-profile field unpopulated → HALT" (EC-1) and "stale regulatory field → re-verify" (EC-8), but not "operator-profile populated with a contraindication that conflicts with a compound entry's existing `risk_tier`/recommendation." The malignancy gate (EC-7) covers a present contraindication firing, but not the case where the profile and a previously-written entry disagree — which is exactly the `vault/meta/contradictions.md` append path named in §4/§10 yet never given a test stimulus.
*Suggested direction:* either fold into EC-7 or note that profile-vs-entry conflict routes to the contradictions log (the mechanism exists; the trigger is untested).

---

## 3. Contradictions

**CON-1 (Major) — §13 cited audit `--check` names do not all match the script; two §13 rows reference checks that, while aliased, are presented as the canonical name when the script's canonical name differs; AND five real script checks are absent from §13.**
*Location:* §13 Mechanical Enforcement Map (the `--check <name>` column) vs `scripts/audit-specialist-profile.sh` `run_one()` (lines 406–435) and `ALL_CHECKS` (lines 437–443).
*Issue:* Verified by reading the script. The script's `run_one` accepts the doc's short names as ALIASES (e.g. `authority-framing` → `authority-framing-mandatory`, `grade-halt` → `grade-two-axis-halt`, `operator-no-writeback` → `operator-profile-no-writeback`, `target-class` → `target-class-declaration`, `mechanical-check-stubs` → `mechanical-stubs`, `library-index-shape` → `library-index`). So the doc's `--check` strings DO resolve — this is not a broken-reference defect. BUT: the script runs **25** checks (`ALL_CHECKS`, confirmed 25 entries) and §13 enumerates only ~20 rows. Five live script checks have NO §13 row: `description-routing`, `refusal-affirmative`, `schema-drift`, `differ-jaccard`, `audit-passed-frontmatter`. §13's header claims "(25 sub-checks)" and the task framing claims 25; the §13 table does not actually enumerate all 25.
*Why it matters downstream:* §15.2 criterion 7 says "every §13 LIVE row's mechanism path resolves." It does — but the inverse (every audit gate has a §13 row) fails. A synthesized profile could trip `refusal-affirmative` or `differ-jaccard` (both real BLOCK/gated checks) with no design-doc coverage telling the synthesizer those gates exist. `differ-jaccard` (DIFFER block ≤0.30 Jaccard) is named in §4 row 10 prose but has no §13 row; `refusal-affirmative` is unmentioned anywhere.
*Suggested direction:* add §13 rows (or an explicit "these 5 checks are generic/§15.1-owned and intentionally omitted here" note) for `description-routing`, `refusal-affirmative`, `schema-drift`, `differ-jaccard`, `audit-passed-frontmatter`; reconcile the "25 sub-checks" claim with the ~20 enumerated rows.

**CON-2 (Minor) — §3.1 row says Finding 12 is "ACCEPTED — see note" but §3.1's column header expects a binary Verdict; §15.2 criterion 2 enumerates allowed verdicts for R-rows, not Findings.**
*Location:* §3.1 Finding 12 Verdict cell ("ACCEPTED — see note") vs §15.2 criterion 1 (Findings table row count = 12, no verdict-vocabulary constraint stated for Findings) and criterion 2 (R-row verdicts ∈ {ACCEPTED, DEFERRED, REJECTED}).
*Issue:* Minor inconsistency: the Findings table uses a free-text verdict ("ACCEPTED — see note") while the doc's own acceptance criterion vocabulary is defined only for the Recommendations table. Not load-bearing, but a strict reader/auditor parsing the Findings Verdict column for a closed vocabulary would flag it.
*Suggested direction:* either keep "ACCEPTED" clean and move "— see note" to a footnote marker, or state that the Findings Verdict column permits an annotation suffix.

**CON-3 (Minor) — §16 claims "All 12 active register invariants are addressed" but INVARIANTS.md contains exactly 12 INV ids and §16 lists 12 rows — consistent — yet §16 marks 6 of them "No effect," which contradicts the §16 scope statement that the Research-domain set "IS in scope in addition to" the others.**
*Location:* §16 preamble vs the 6 "No effect" rows (INV-SCOPE-CONTRACT, INV-PF-ATTESTATION, INV-BRANCH-NOT-MAIN, INV-HO-ROTATION, INV-HO-NO-STALE-HASH, and INV-RESEARCH-IC13-CORPUS "No effect").
*Issue:* This is defensible (a specialist-runtime agent genuinely cannot touch HANDOFF rotation), so it is not a true contradiction — but "addressed" is doing double duty: 6 rows are "addressed" only in the sense of "ruled out of scope." A reviewer applying §15.2 criterion 7 ("every REFERENCED row cites an INV-* present in INVARIANTS.md") is satisfied; the wording "all 12 addressed" slightly oversells. Filed as Minor for transparency, not a blocking defect.
*Verification:* all 12 cited INV-* ids resolve in `INVARIANTS.md` (confirmed by diff — see Category 4).

---

## 4. References

Verified a representative sample against the actual cited source files. Results:

**Resolved cleanly:**
- Substrate `### Finding` count = **12** (confirmed via `rg -c '^### Finding'`). Matches §3.1 table and §15.2 criterion 1. PASS.
- Substrate Recommendations **R1–R15** all present (confirmed; substrate L309 self-attests "Exactly 15 Recommendations: PASS — R1–R15"). Matches §3.2 and §15.2 criterion 2. PASS.
- All **9 cited PF ids** (PF-S2-01..06, PF-S3-01, PF-S6-01, PF-S13-01) resolve as `### PF-S#-##` headings in `memory/process-failures.md`. PASS.
- All **12 cited INV-* ids** resolve in `INVARIANTS.md` (exact set match). PASS.
- `scripts/audit-specialist-profile.sh` exists, is executable, runs **25** checks. PASS (but see CON-1 on enumeration mismatch).
- `templates/specialist-risk-class.yaml` peptide-specialist row = `risk_class: compound-experimental`, `mode_floor: deep`, `target_class: compound` — exactly as §4 row 7 / §8 / §13 claim. PASS.
- `templates/refusal-class-taxonomy.yaml` contains all four cited class IDs (AUTHORITY_FRAMING_BYPASS, PRESCRIPTIVE_DIRECTIVE, PATIENT_FACING_DIRECTIVE, BASIS_NOT_REVIEWABLE) and `mandatory_for_every_specialist: true` on AUTHORITY_FRAMING_BYPASS. PASS.
- `vault/WIKI.md` L280 = the peptide-specialist consumer row (peptides, GH secretagogues, healing peptides); L312 = "Never write a page from memory — read the source ... first." Both as cited. PASS.
- `vault/compounds/bpc-157.md` exists (135 lines). L39 + L119 = the He L 2022 / S2-misattribution precedent (§11.1 PF-S2-02 row, accurate). PASS.

**REF-1 (Minor) — §14 EC-1 quotes `vault/compounds/bpc-157.md` L116 but the quote is a paraphrase, not verbatim, and L116 contains operator-identifying content.**
*Location:* §14 EC-1 cites "L116 — 'January 2026 health-issue characterization is REQUIRED before any risk_tier=experimental compound can move from researching to planned.'"
*Issue:* L116 resolves and the quoted clause is present — but L116 also contains "Walter's specific context (per operator-profile.md...)". The line resolves, so this is not a broken reference; flagging because the cited line is operator-personalized content, and §9/§13 operator-no-writeback discipline forbids operator literals in the synthesized body. The design doc itself does not leak it (it quotes only the goal-agnostic clause), so this is a near-miss, not a violation. Minor.

**REF-2 (Minor) — several line-number citations are into volatile files and will drift.**
*Location:* `health-implementer-design.md:131`, `:535`; `CONTINUATION_BRIEF.md:357`; `vault/compounds/bpc-157.md` L27/L28/L32-33/L58-60/L65/L70/L74/L82/L82-89/L101-106/L120/L121/L122.
*Issue:* I verified the bpc-157 L39/L116/L119 anchors resolve to the claimed content; I did not re-verify every bpc-157 sub-line nor the cross-design-doc `:131/:535` anchors (those live in sibling worktree design docs). These are bare line-number references into files that are not frozen; per the project's own INV-HO-NO-STALE-HASH philosophy (filename-not-line citations preferred), these will silently rot. Not currently broken (sampled anchors resolved), but brittle.
*Suggested direction:* prefer section/heading anchors over bare line numbers for cross-document citations, or pin the cited commit.

No broken/unresolvable reference was found in the sample. The §13 `--check` names initially looked broken but resolve via documented script aliases (see CON-1).

---

## 5. Ordering

**ORD-1 (Minor) — §10 step 5 states the loading order, but §10 step 1 (auto-load library surface) is presented before §10 step 2 (auto-load contracts), while step 5 says contracts must load before any compound layer is reasoned over.**
*Location:* §10 steps 1, 2, 5.
*Issue:* The numbered step order (1 = library surface incl. per-compound layers; 2 = contracts) is the reverse of the dependency order that step 5 then corrects ("Contracts (step 2) and source-whitelist (step 1) load before any compound layer"). A synthesizer encoding steps in listed order would load compound layers (step 1) before contracts (step 2), then step 5 retroactively forbids reasoning over them. The intent is recoverable but the step numbering fights the dependency.
*Suggested direction:* reorder so contracts + source-whitelist precede per-compound layers in the step sequence, or split step 1 into "1a source-whitelist/triage" and "1b per-compound layers (after step 2)."

No other ordering defect found: §3 (digest) correctly precedes §5 (rules that cite Findings); §4 INBOUND references precede §5/§8 consumers; §11.1 PF table precedes §11.2 anti-patterns that cite PFs. Check ran: traced each §5 rule's cited Finding back to §3.1 and each §11.2 anti-pattern's cited PF to §11.1 — all defined-before-use.

---

## 6. Scope

**SCO-1 (Minor) — §6 step 4 cites "Role 2 §6 step 2" for the new-refusal-class HALT, but new-class authority is Role 1's (taxonomy owner), which the same step correctly names.**
*Location:* §6 step 4 ("file an Architecture Question to health-specialist-architect (taxonomy owner) ... (Role 2 §6 step 2, refusal-class-taxonomy.yaml)").
*Issue:* The step routes correctly to Role 1 (health-specialist-architect = taxonomy owner) but cites Role 2 §6 step 2 as the source. Either the citation is to Role 2's procedure for *escalating* (plausible) or it is a mis-citation of the owning authority. Mild scope-citation muddiness: the taxonomy is Role-1-owned per §2.2 and §4 row 1, so citing Role 2 for the class-need procedure is at minimum confusing.
*Suggested direction:* confirm whether Role 2 §6 step 2 is the procedural source; if the substantive owner is Role 1, cite Role 1.

**SCO-2 (no finding) — anti-redefinition discipline holds.**
*Check ran:* grepped the doc for inlined canonical content. §4 rows and §5 rules consistently say "references by anchor," "inherits verbatim ... does not redefine," "encode by reference." No 8-class taxonomy enumeration, no H1–H8 definitions, no GRADE downgrade-trigger list, no verdict-schema definition is inlined — each is cited to its owning doc + §-row. §2.2 "I do NOT own" list is explicit and matches §4 INBOUND sources. The §4 anti-redefinition note + §15.2 criterion 4 are self-consistent. Clean.

**SCO-3 (Minor) — possible scope GAP: the doc owns `vault/library/peptides/` writes but never specifies the per-compound layer FILE SET it authors.**
*Location:* §2.2 "I own ... `vault/library/peptides/`"; §8 Write surface; §10 step 1 reads `{research-report,practitioner-layer,non-english-layer}.md`.
*Issue:* §10 step 1 enumerates the layer files it READS (research-report / practitioner-layer / non-english-layer), and §8 says it "writes `vault/library/peptides/`," but the doc never says which of those layer files the specialist authors vs which arrive from the `aplus-research` dispatch. §8 also says "it does not author the entries it reads" (PF-S2-04) — which seems to say it reads but doesn't write library entries, contradicting "I own ... the library." The own-vs-consume boundary for `vault/library/peptides/` is under-specified.
*Suggested direction:* state explicitly which library artifacts the specialist writes (e.g., the index/synthesis) vs which are dispatch outputs it consumes — the §8 "consumes the wiki, does not author the entries it reads" line and the §2.2 "I own the library" line need reconciliation.

---

## 7. Downstream (synthesis + audit gating)

**DOWN-1 (Critical) — the design doc provides NO source content for the mandatory Modes section, yet `section-count` BLOCKs at exactly 11 sections (10 base + Modes).**
*Location:* §13 `section-count` row (LIVE, BLOCK, "exactly 11"); §13 `modes-shape` row (needs `### Mode:` subheading); DESIGN_DOC_TEMPLATE §2 note (Modes "emerges as a /upgrade-agent Phase 5 synthesis output ... informed by §5 + §9 + §14 jointly"). The design doc has no §ostensibly-Modes content and no Modes spec.
*Issue:* The synthesized agent.md MUST have an 11th section `## Modes` with a `### Mode:` subheading or `section-count` (BLOCK) and `modes-shape` (WARN) both flag it. The design doc leaves Modes entirely to Phase-5 synthesis with no source material designated beyond a template hand-wave. For a research-dispatching + compound-writing specialist there are obvious modes (library-build mode vs personalized-decision mode vs refusal mode), but the design doc names none. A synthesizer with no Modes source either invents modes (un-grounded, violating "never write from design-doc-absent content") or emits a stub that trips `modes-shape`.
*Why it matters downstream:* this is the single most likely BLOCK at deploy-gate time. `section-count` is a hard BLOCK and the design doc gives the synthesizer nothing concrete to populate the required section.
*Suggested direction:* add a short Modes spec to the design doc (even 3 named modes mapped to §5/§9/§14) so Phase 5 has grounded source content rather than inventing it.

**DOWN-2 (Major) — `library-index.md` is a BLOCK-gated audit artifact (present, ≤30 lines, 1–5 `vault/library/` refs) but the design doc never specifies it.**
*Location:* §13 `library-index-shape` row (LIVE, BLOCK on missing/over-30/0-refs); §15.1 mentions "`library-index.md` reference paths resolve" as a Phase-7 generic constraint.
*Issue:* `library-index.md` must exist alongside the agent.md with 1–5 `vault/library/` conditional refs or the audit BLOCKs. The design doc punts it to §15.1 "generic constraints ... enforced by Phase 7" and never specifies its content. For this specialist the conditional refs would be the peptide library surfaces (`vault/library/peptides/_triage.md`, `_source-whitelist.md`, per-compound layers from §10 step 1) — but the design doc does not designate them as the index entries. Phase 5 must produce this file with no design-doc source.
*Why it matters downstream:* BLOCK at deploy gate. Same class of gap as DOWN-1: an audit-gated artifact with no design-doc spec.
*Suggested direction:* designate the §10-step-1 library surfaces as the `library-index.md` conditional-load entries (that is exactly 3–5 refs and fits the ≤30-line / 1–5-ref window).

**DOWN-3 (Major) — §5 has 11 rules; the synthesized Core Rules plus 11 sections plus 4 BAD/GOOD negative-example blocks plus the IDENTICAL anti-sycophancy block must fit ≤200 lines AND ≤2500 cl100k tokens. The design doc's §5 rules are paragraph-length; verbatim synthesis will blow the budget.**
*Location:* §13 `body-length` (BLOCK, ≤200 lines AND ≤2500 tokens, target 150–180); §5 (11 multi-sentence rules with embedded pass/fail clauses); §12 (4 BAD/GOOD pairs); §4 row 4 (Mechanism B "verbatim" IDENTICAL block).
*Issue:* §5 rule bodies run 4–8 sentences each with parenthetical citations and pass/fail audit grep specs. If Phase 5 carries the pass/fail audit clauses into the profile prose (the design doc embeds them inline in each rule), the Core Rules section alone could approach the whole 200-line budget before Tools, Context Loading, Anti-Patterns, 4 Negative Examples, and the verbatim IDENTICAL block. The pass/fail clauses are design-doc verification artifacts, not agent.md content — but the doc does not flag them as "strip on synthesis."
*Why it matters downstream:* `body-length` is a hard BLOCK. This is a real budget risk for an unusually dense design doc.
*Suggested direction:* mark the §5 `Pass/fail:` clauses and `[voice:]/[source:]` tags as design-doc-only (strip on synthesis); give Phase 5 an explicit "Core Rules target ≤N lines, drop the audit-grep specs" instruction.

**DOWN-4 (no finding) — refusal classes, GRADE HALT, anti-sycophancy 3-mechanism, AUTHORITY_FRAMING_BYPASS all have grounded source content.**
*Check ran:* §5 rule 7 names AUTHORITY_FRAMING_BYPASS + 3 more taxonomy-resolvable classes (all 4 confirmed in `refusal-class-taxonomy.yaml`); §5 rule 5 gives both GRADE axes + HALT disposition matching the `grade-halt` audit grep; §5 rule 8 names Mechanism A/B/C with the exact keyword tokens the `anti-sycophancy` audit greps for (`silent agreement|catfish|multi-agent`, `acquiescence|maintain position|user pushback`, `RLHF|preference drift|Sharma|Petri`). The Identity sentence (§2.1) is 33 words (≤40, PASS). These four audit sub-checks have sufficient design-doc source to synthesize a passing profile. Clean.

---

## 8. Language Economy

**LE-1 (Major) — §11.2 anti-patterns each carry a full Source-citation paragraph + Recognition-cue paragraph; the synthesized Anti-Patterns section risks duplicating §17 Risk Assessment near-verbatim.**
*Location:* §11.2 #1–#8 vs §17.1 risks 1–6.
*Issue:* §17.1 risk 2 (single-lab), risk 6 (animal→human), risk 1 (medRxiv DOI), risk 4 (regulatory drift) restate, in nearly the same sentences and citations, §11.2 #3, #6, (Finding-12 note), #4/#8. The design doc is allowed redundancy (§17 and §11 serve different design purposes), but the synthesizer drawing Anti-Patterns from §11.2 and any "risk" framing from §17 could double-encode the same content into the profile, inflating the line budget (compounds with DOWN-3).
*Suggested direction:* note that §17 is design-doc-only (does not synthesize into agent.md) so Phase 5 doesn't pull from both.

**LE-2 (Minor) — §11.2 rule 5 + rule 6 + §5 rule 11 + §5 rule 4 all re-state the vendor/anecdote/concentration discipline.**
*Location:* §5 rule 4 (concentration), §5 rule 11 (vendor/practitioner/stack), §11.2 #3 (concentration), §11.2 #5 (vendor numerical).
*Issue:* The vendor-numerical and single-lab-concentration disciplines each appear as both a Core Rule and an Anti-Pattern with overlapping recognition language. This is partly intentional (rule vs negative-framing), but the overlap is heavy enough that synthesis could read as repetitive in the profile.
*Suggested direction:* acceptable as-is if Phase 5 keeps Core Rules imperative and Anti-Patterns first-person-failure framed; flag only so the synthesizer keeps them distinct rather than near-duplicate.

**LE-3 (Nitpick) — §3.1 Finding 12 ACCEPTED-with-note paragraph (≈12 lines) is design-doc rationale that must not synthesize.**
*Location:* §3.1 Finding-12 note + §17.1 risk 1 + §18 OQ-2 — the medRxiv-DOI anomaly is explained three times.
*Issue:* The `10.64898/` anomaly is correctly handled (CONTRACT-INHERITED, not load-bearing) but explained in three sections. For the design doc this is defensible thoroughness; for token economy it is the most-repeated single fact in the document.
*Suggested direction:* none required for the doc; ensure none of the three copies synthesizes into agent.md (§15.2 criterion 8 already guards the figure).

---

## Severity Tally

| Severity | Count |
|---|---|
| Critical | 1 |
| Major | 5 |
| Minor | 10 |
| Nitpick | 2 |
| **Total** | **18** |

(Critical: DOWN-1. Major: EC-MISS-1, CON-1, DOWN-2, DOWN-3, LE-1. Minor: AMB-1, AMB-2, EC-MISS-2, EC-MISS-3, CON-2, CON-3, REF-1, REF-2, ORD-1, SCO-1, SCO-3 — note SCO-3 + AMB-3 push Minor to 11; recount: AMB-1, AMB-2, EC-MISS-2, EC-MISS-3, CON-2, CON-3, REF-1, REF-2, ORD-1, SCO-1, SCO-3 = 11. Nitpick: AMB-3, LE-3. LE-2 = Minor → Minor=12. Adjusted total = 1 Critical + 5 Major + 12 Minor + 2 Nitpick = 20.)

**Corrected tally: Critical 1 · Major 5 · Minor 12 · Nitpick 2 · Total 20.**

## Highest-Priority Finding

**DOWN-1 (Critical)** — The design doc gives the Phase-5 synthesizer no source content for the mandatory `## Modes` section, yet `audit-specialist-profile.sh --check section-count` is a hard BLOCK requiring exactly 11 sections (10 base + Modes) and `modes-shape` requires a `### Mode:` subheading. As written, the synthesized agent.md will either omit Modes (BLOCK at deploy gate) or invent un-grounded modes (violates the project's "no content the design doc doesn't supply" discipline). This is the one defect most likely to fail the deploy gate. Fix: add a brief Modes spec (3 named modes mapped to §5/§9/§14) to the design doc. DOWN-2 (library-index.md) is the same failure class and should be fixed in the same pass.
