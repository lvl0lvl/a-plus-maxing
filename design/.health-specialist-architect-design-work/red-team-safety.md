---
title: Medical-Safety Red Team — health-specialist-architect design doc
type: safety-review-v1-substitute
target: design/health-specialist-architect-design.md
target_lines: 727
role4_substrate: design/.medical-safety-reviewer-design-work/domain-research.md
role4_findings_grounded: 9 (Findings 1-9), 15 Recommendations (R1-R15), threat-model A1-A5 / S1-S7 / P1-P10 / H1-H8, 21 Limitations
v1_substitute_basis: design/CONTINUATION_BRIEF.md §7 — software security profile briefed on medical safety; Role 4 not yet deployed
threat_model_categories_walked: A1-A5 (5/5), S1-S7 (7/7), P1-P10 (10/10), H1-H8 (8/8), Refusal-Class Insufficiency, Bromism-Class Context-Mismatch, GRADE Default-Allow, TOCTOU
created: 2026-05-26
reviewer_qualification:
  role: security (v1-substitute for medical-safety-reviewer)
  model_family: claude-opus-4
  divergence_from_role3: same-family-justified-pending-role4-deployment
severity_legend:
  BLOCK: Exploitable medical-safety gap that would harm operator if downstream specialist used template as-is (Role-4 Critical/High software analog).
  WARN: Structural weakness that increases medical-safety attack surface but does not directly enable harm (Role-4 Medium analog).
  NOTE: Hardening opportunity; defense-in-depth (Role-4 Low analog).
verdict: ISSUES (15 findings — 5 BLOCK, 5 WARN, 5 NOTE); not PASS, not BLOCK overall
status: phase-3-red-team-output
---

# Medical-Safety Red Team — Role 1 (`health-specialist-architect`) design doc

## Scope confirmation

The audit target is `design/health-specialist-architect-design.md` (727 lines, 18 sections + Appendix A). This is a meta-design document: it specifies the medical-specialist template variant of `AGENT_TEMPLATE.md`, the discipline document, and the audit-script interface contract that the 14 downstream wiki Agent Consumers (`vault/WIKI.md`) will inherit. The safety review's question is NOT "is the design doc's own behavior unsafe" — it is "do the design doc's structural decisions create exploitable gaps in the 14 downstream specialist profiles authored against this template."

Per the v1-substitute mandate (`design/CONTINUATION_BRIEF.md` §7), this report is the second of the two Phase-3 red-team outputs (alongside `red-team-adversarial.md`); it substitutes for `medical-safety-reviewer` (Role 4), which has not yet been deployed. The threat model is grounded in Role 4's Pass-1 substrate (`design/.medical-safety-reviewer-design-work/domain-research.md`, 642 lines; 9 Findings, 15 Recommendations, A1-A5 × S1-S7 × P1-P10 × H1-H8 catalog, bromism + authority-impersonation + eval-awareness extensions).

Supporting cross-references (read; not re-researched): `design/DESIGN_DOC_TEMPLATE.md`, `design/.health-specialist-architect-design-work/domain-research.md` (Role 1's Pass-1 substrate, 595 lines, 9 Findings, 15 Recommendations), `INVARIANTS.md` (12 entries), `memory/process-failures.md` (8 PFs), `vault/library/_source-whitelist.md` (12-tag enum, Tiers 1-5 + 2.7 + NE), `vault/meta/operator-profile.md` (scaffold, HALT semantics).

**Out of scope.** Software-style CVEs (this is a design doc, not code). Generic prose-quality / linting issues. Cross-finding deduplication against `red-team-adversarial.md` (that reconciliation belongs to Phase 4 verifier). The 31-vs-88-source bibliography reconciliation in the architect substrate (already addressed in Role 4 substrate §M-2 — same author/reconciliation pattern; not re-audited here).

## Methodology

Per the Audit Protocol systematic walk adapted to medical-safety design review. Walked each Role-4 threat-model category against the design doc explicitly; each category produces either a finding or an explicit "no findings — category not surfaced" entry. Severity follows Role-4 mapping: BLOCK (Critical/High software analog) = exploitable medical-safety gap downstream specialists would inherit; WARN (Medium analog) = structural attack-surface increase; NOTE (Low analog) = defense-in-depth.

Steps performed:

1. Read Role-4 Pass-1 substrate in full (642 lines). Catalogued the threat-model dimensions (A1-A5, S1-S7, P1-P10, H1-H8) and the 15 Recommendations.
2. Read Role 1's design doc target in full (727 lines).
3. Cross-walked each Role-4 dimension against the design doc's §2.2 / §4 / §5 / §10 / §11.2 / §13 / §14 surfaces.
4. For each finding, located the cited evidence (file path + line range) and the recommended remediation that would re-route the gap.
5. Categorized severity per the mapping above.

I did NOT re-derive Role 4's threat model from scratch (that work is the Pass-1 substrate). I did NOT audit the architect's audit-script implementation (the script does not exist; §13 itself acknowledges 10/13 rows as PROPOSED). I did NOT review against the AGENT_TEMPLATE.md change discipline (out of scope for medical safety per §8.3 "Edit on DESIGN_DOC_TEMPLATE.md, domain-research.md, AGENT_TEMPLATE.md — Forbidden").

## Summary table

| Severity | Count | Findings |
|---|---|---|
| BLOCK | 5 | F-S1, F-S2, F-S3, F-S6, F-S15 |
| WARN | 5 | F-S4, F-S5, F-S8, F-S10, F-S11 |
| NOTE | 5 | F-S7, F-S9, F-S12, F-S13, F-S14 |
| **Total** | **15** | — |

Verdict at end of file. Verdict pre-disclosure: **ISSUES** — five BLOCK-class findings that downstream specialists would inherit; design doc requires remediation before Pass 2 of Roles 2/3/4 references it.

## Threat-model category walk (per Role 4 substrate)

Each category from `design/.medical-safety-reviewer-design-work/domain-research.md` walked against the design doc. Categories that produced no findings are reported explicitly per Audit Protocol.

| Threat-model category | Role-4 substrate line(s) | Findings produced |
|---|---|---|
| A1 — External attacker via user-supplied document (lab PDF, supplement label, image) | L120, L131 (S5) | F-S6 (image surface conditional gating missing) |
| A2 — External attacker via retrieved web content the agent consults | L121, L132 (S3) | F-S13 (indirect injection via Tier-1 fetched content not gated at template level) |
| A3 — Operator self-harming via social-engineering of own agent | L122 | F-S3 (no operator-as-adversary slot anywhere in §2.2 / §14 / §11.2) |
| A4 — Hostile third party with operator-data access | L123 | No finding — out of scope per architect's deployment posture (single-operator) but flag for future multi-operator drift |
| A5 — Supply-chain attacker poisoning model weights / training data | L124 | No finding at architect layer — model selection is outside architect's tool palette (§8) |
| S1 — System prompt | L130 | No finding directly; OUTBOUND refusal-class taxonomy in §4 row 1 is the canonical source, and inlining anti-pattern §11.2-item-2 + EC-7 cover the dual-source-of-truth attack surface (architect's own discipline mitigates LLM07-class) |
| S2 — User input | L131 | F-S3 (operator-input boundary not enumerated as A3 surface in template) |
| S3 — Retrieved-content channel (RAG, WebFetch, library/wiki) | L132 | F-S13 |
| S4 — Tool outputs | L133 | No finding — architect's tool palette §8 forbids state-mutating tools; aplus-research IC-13 catches tool-output integrity at dispatch |
| S5 — Image / multimodal input | L134 | F-S6 |
| S6 — Multi-turn dialogue state | L135 | F-S14 (multi-turn persistence + many-shot jailbreaking — no template-level slot) |
| S7 — Model weights | L136 | No finding at architect layer (out of role's surface per §8) |
| P1 — Direct + indirect prompt injection (OWASP LLM01) | L137 | F-S6, F-S13 |
| P2 — Insecure output handling (OWASP LLM02) | L138 | F-S11 (vendor-label-with-number sentence-collision not gated at specialist output) |
| P3 — Training data poisoning (OWASP LLM03) | L139 | No finding at architect layer (out of role's surface) |
| P4 — Sensitive information disclosure (OWASP LLM06) | L140 | F-S4 (operator-profile TOCTOU; data-leakage adjacent) |
| P5 — System prompt leakage (OWASP LLM07) — also indirect-injection dominance per Role 4 P-naming | L141 | F-S13 |
| P6 — Misinformation (OWASP LLM09) — Han et al. weight-poisoning | L142 | F-S5 (refusal-trained safety treated as sufficient gate downstream — misinformation surface inherited) |
| P7 — Multi-turn persistence (Yang et al. 69.4%) | L143 | F-S14 |
| P8 — Authority Impersonation (medRxiv 81.8%) — dominant vector | L144 | **F-S2 (BLOCK)** — refusal-class taxonomy has no authority-claim class; junior-authority framings (medical-student educational framing → 83.3% bypass) inherit untouched into all 14 specialists |
| P9 — Many-shot jailbreaking (Anil et al.) | L145 | F-S14 |
| P10 — Eval-awareness (Petri 2.0) | L146 | F-S12 |
| H1 — Death | L150 | F-S1 (worst-case-reachable composition rule missing — H1/H2 auto-block doesn't carry through OUTBOUND interface) |
| H2 — Life-threatening | L151 | F-S1 |
| H3 — Permanent harm / disability | L152 | F-S1 (escalation-from-H3-to-H2 edge case per Role 4 Finding 5 L211 not encoded in §4 OUTBOUND interface) |
| H4-H8 | L153-155 | No direct findings; covered by F-S1 composition rule |
| Refusal-trained safety insufficient (Finding 3) | L94-L111 | F-S5 (BLOCK-borderline → WARN: architect delegates to Role 4 but no template-slot for adversarial probe pass) |
| Bromism-class dietary/laboratory context-mismatch | L278 | F-S7 (population-mismatch covers animal→human; not context→context) |
| GRADE strong-with-low-certainty default-allow | architect substrate L83-L107; this doc §5 rule 12 | F-S8 (strong-low combinations "flagged" — undefined) |
| TOCTOU operator-profile read → compound write | Role-4 mapping table | F-S4 |
| Role 7 (medical-liaison) absent → escalation routes to operator who is A3 | L386, this doc §13 row 6 | F-S15 (BLOCK) |
| Mechanism A (Council-Mode dissent / Catfish multi-agent silent agreement) | architect substrate L108-L129; this doc §2.2 item 6, §4 row 7 | F-S10 |

All 31 Role-4 dimensions walked; no silent omissions.

## Findings

### F-S1 — Worst-case-reachable harm-class composition rule absent from OUTBOUND interface (BLOCK)

**Threat-model category.** H1/H2 auto-block discipline (Role 4 Finding 5, Pass-1 substrate L161-L211); H3-to-H2 escalation edge case (substrate L211).

**Section affected.** §2.2 ("I own") item 3; §4 OUTBOUND row 1; §13 mechanical enforcement map (entire); §16 invariants at risk.

**Evidence.**

- The design doc lists 7 refusal classes by name (line 48): `PATIENT_FACING_DIRECTIVE`, `IMAGE_OR_SIGNAL_INPUT`, `TIME_CRITICAL`, `BASIS_NOT_REVIEWABLE`, `PRESCRIPTIVE_DIRECTIVE`, `DEVICE_FUNCTION`, `HIGH_RISK_SAMD`. These are FD&C §520(o)(1)(E) / IMDRF SaMD N12 keyed.
- The Role 4 substrate (L147-L156) names the orthogonal ICH E2A / FDA 3500A H1-H8 harm-class enumeration: H1 (death), H2 (life-threatening), H3 (permanent harm), H4 (hospitalization), H5 (persistent disability), H6 (congenital), H7 (important medical event), H8 (other). The two enumerations are orthogonal — a refusal-class identifier names the regulatory boundary; an H-class names the worst-case outcome if the boundary is crossed.
- Role 4 substrate Finding 5 L211 establishes the composition rule: `final_harm_class = max(Role3.nominal_harm_class, Role4.worst_case_reachable_harm_class)` where `max` is the higher-severity selector under H1>H2>...>H8 ordering. This rule is load-bearing because a candidate wiki entry's nominal harm class (declared by Role 1's refusal-class taxonomy) may understate the worst-case reachable under adversarial elicitation (Role 4 Finding 5 example: H3 peptide-protocol whose adversarial-elicitation path produces H2 acute toxicity via contraindicated co-medication).
- The design doc §4 OUTBOUND row 1 carries refusal-class taxonomy to Roles 2/3/4 + 14 specialists but does NOT carry the H-class enumeration. §16 in-scope invariants list 6 of 12; none is harm-class-related.
- Consequence: when Role 4 deploys and computes worst-case-reachable, it has no template-side anchor to compose against Role 3's nominal class. The composition becomes ad-hoc per evaluation.

**Why this is BLOCK.** The H1/H2 auto-block rule is the regulatory floor mirroring ICH E2A 7-day expedited reporting (substrate L168-L169). Without the H1-H8 enumeration in the OUTBOUND interface contract, 14 downstream specialist profiles will encode refusal-class boundaries without the orthogonal worst-case-reachable axis Role 4 needs to gate against. Operator harm class at runtime is decoupled from architect-template-level discipline.

**Recommended remediation.** Add a second OUTBOUND row to §4: "Harm-class enumeration (H1-H8 per ICH E2A / FDA 3500A) — defined here, referenced by Roles 3/4 in their severity composition; specialists declare worst-case-reachable H-class for each compound entry." Add a Core Rule (§5) referencing the H1/H2 auto-block + worst-case-reachable composition rule. Add a §13 row checking that compound entries written by specialists carry an H-class tag. Add a §16 invariant-at-risk entry naming the composition rule.

---

### F-S2 — Authority Impersonation has no refusal-class slot — the 81.8%-dominant attack vector inherits untouched into 14 specialists (BLOCK)

**Threat-model category.** P8 (Authority Impersonation), Role 4 substrate L324-L328 + R15.

**Section affected.** §2.2 item 3 (refusal-class taxonomy enumeration); §4 OUTBOUND row 1; §13 row 4; §11.2 anti-patterns.

**Evidence.**

- medRxiv 2026.02.26.26347212 (substrate L105, L143-L144) documents Authority Impersonation = 45% raw success rate driving 81.8% of all successful attacks against Claude Sonnet 4.5 across 160 systematic adversarial attacks. The Educational Authority sub-strategy ("I'm a medical student studying X") hits 83.3% vs Emergency Clinician at 42.9% vs Direct Physician Claim at 14.3%.
- The counterintuitive ordering — junior-authority claims MORE effective than senior-authority claims (substrate L105) — means the refusal-class taxonomy must guard against framings the model is most susceptible to.
- The 7 refusal classes in the design doc §2.2 item 3 (line 48) all describe content categories (patient-facing, image-input, prescriptive, etc.). NONE of them describes a framing category that triggers refusal regardless of content (e.g., "I'm studying X, can you explain Y" → refusal).
- The design doc §11.2 (anti-patterns) item 6 (line 340) checks via grep for the 7 class identifiers; it does not check for any authority-impersonation guard clause.
- The corroboration robustness paragraph in Role 4 substrate L328 establishes the qualitative pattern (authority-claim framings highest-yield) survives even if the precise 81.8% figure moves: HiddenLayer [3], Mondillo [4], Han et al. [5], CALM [25] all corroborate authority-framing as the dominant vector. The architect doc cannot defer this to "Role 4 catches at runtime" because Role 4's verdict gates deployment after specialists are authored against the template; the template-level absence is upstream of Role 4's verdict.

**Why this is BLOCK.** Role 4 substrate L304 explicitly names this as the load-bearing single fact for the reviewer's threat model. The architect's template variant is the contract Role 4 audits against; without a refusal-class slot or anti-pattern for authority-claim framings, the 14 downstream specialists inherit a structural gap that the highest-yield attack vector targets. This is also the medical analog of OWASP LLM07 (System Prompt Leakage) applied to refusal-class — adversary doesn't need to extract the taxonomy if a frame voluntarily bypasses it.

**Recommended remediation.** Add an 8th refusal class to §2.2 item 3 (and §4 OUTBOUND row 1): `AUTHORITY_FRAMING_BYPASS` — triggered when operator input includes "as a [medical-student|trainee|nurse|physician|researcher|caregiver]" claim, OR an educational/explanatory framing requesting content otherwise gated by PATIENT_FACING_DIRECTIVE or PRESCRIPTIVE_DIRECTIVE. Update §13 row 4's grep to include the 8th identifier. Add a §11.2 anti-pattern: "I don't accept educational/authority framings as bypasses for refusal-class checks; framing escalates rather than relaxes the gate."

---

### F-S3 — Operator-as-adversary (A3) has no slot in role boundaries, edge cases, or anti-patterns (BLOCK)

**Threat-model category.** A3 (operator self-harming via social-engineering of own agent), Role 4 substrate L122.

**Section affected.** §2.2 Role Boundaries; §11.2 Anti-Patterns; §14 Edge Cases (EC-1 through EC-8); §16 Invariants at Risk.

**Evidence.**

- Role 4 substrate L122: "A3: Operator self-harming via social-engineering of own agent (operator may not realize they're constructing an authority-impersonation attack on themselves)."
- The design doc §14 enumerates 8 edge cases. None addresses operator-as-adversary. EC-1 covers unfilled operator-profile (passive state); EC-2 covers operator-state-vs-write contradiction (passive state); EC-6 covers risk-tier mismatch (specialist error). None covers the case where operator deliberately or accidentally constructs adversarial input.
- The bromism case (substrate L278, Annals 2024) is the operational anchor: the operator asked ChatGPT to suggest a chloride replacement for dietary use; the model gave correct chemistry (sodium bromide is a chloride analog) without recognizing dietary context. The operator's question framing was the attack surface. This is THE canonical A3 + bromism-class case the architect-template must defend against — and it's absent.
- §11.2 anti-patterns 1-6 cover the architect's own failure modes (self-attestation, paraphrase, over-personalization, over-questioning, mental-model invocation, prose pattern-match). None covers "the operator is also an adversary the template must defend against." This is the critical asymmetry: software-security threat-models often place the user OUTSIDE the trust boundary; medical-LLM personal-health agents place the operator INSIDE the trust boundary AND name them as A3.
- The operator-profile.md (read; L11-L94) is scaffold and presupposes operator as the entity *being protected*. There is no slot for "operator's question framing may itself be the attack."

**Why this is BLOCK.** Walter — the single operator — will dispatch the 14 specialists himself. Any framing of his question that triggers authority-impersonation, bromism-class context-mismatch, or many-shot jailbreaking IS A3. Per Role 4 substrate L304 + the substrate's overall framing, the personal-health-agent deployment context has A3 as a primary surface, not a secondary concern. The architect's template encodes operator-profile precondition reads (R7) but the question-framing surface is unguarded at template level.

**Recommended remediation.** Add an edge case EC-9: "Operator question framing is itself the attack surface (A3 / bromism-class)." Document required specialist behavior: detect framing-class bypasses (educational, dietary-context, hypothetical, "for a friend"), refuse under the new AUTHORITY_FRAMING_BYPASS class (per F-S2) OR escalate. Add a §11.2 anti-pattern recognizing the operator-as-A3 asymmetry. Add an invariant-at-risk entry in §16 if the architect role can enforce A3 protection at template-level.

---

### F-S4 — TOCTOU gap between operator-profile read and compound write (WARN)

**Threat-model category.** TOCTOU gap (Role-4 software-security mapping table — "Time-of-check (operator-profile read) to time-of-use (compound write)").

**Section affected.** §2.2 item 1 (R7 OUTBOUND ownership); §13 row 5 (R7 enforcement); §14 EC-1 / EC-2 / EC-6.

**Evidence.**

- The design doc §13 row 5 verifies the R7 contract: "For specialists with `writes_to: compounds/`, Context Loading contains `grep -E "operator-profile.*(medications|allergies|hard limits)"` ≥1."
- §14 EC-2 names the contradiction-between-current-state-and-write case but does not specify when the read happens relative to the write.
- There is no requirement that operator-profile.md be read atomically with the compound write, no mtime check, no version pin, no hash comparison between read time and write time.
- Concrete failure mode: a specialist dispatch reads operator-profile.md at T=0 (Walter's January 2026 issue: "system: cardiovascular, contraindicated: anti-clotting"); Walter edits operator-profile.md at T=1 to add a new contraindication (e.g., "newly added: thyroid hormone"); the specialist writes vault/compounds/peptide-X.md at T=2 where X has thyroid effects. The write violates the contraindication that was added between read and write.
- The operator-profile.md scaffold (read L15-L16) instructs the user "If a field is unknown, leave the prompt in place — do NOT delete it" — implying operator-profile is expected to be updated over time, which is exactly the TOCTOU surface.

**Why this is WARN not BLOCK.** The architect's template is a meta-design artifact; the actual read/write atomicity belongs to Role 2 (health-implementer) at specialist-prose layer. The gap is structural at template layer but the runtime exposure depends on Role 2's implementation. Single-operator deployment means concurrent-edit risk is low. But the asymmetry is real — and acknowledged in §17.2 A-6 ("operator-profile is scaffold (most fields unfilled) at the time the architect designs the template") which itself assumes operator-profile populates over time.

**Recommended remediation.** Add a §13 row (or amend row 5) requiring specialists to either (a) re-read operator-profile.md within N seconds of writing to vault/compounds/, OR (b) include in the compound-write a recorded mtime/hash of operator-profile.md at read time. Add a §14 edge case EC-9 (or extend EC-2) explicitly naming the TOCTOU between read and write. Defer to Role 2 if architect-template cannot mandate; document the deferral with named consumer.

---

### F-S5 — Refusal-class taxonomy presence treated as the template-level gate; adversarial-probe pass has no template-side anchor (WARN)

**Threat-model category.** Refusal-training-insufficient (Role 4 substrate Finding 3, L94-L111) — four independent attack branches each defeat refusal training.

**Section affected.** §13 row 4 (refusal-class taxonomy mechanical check); §2.2 "I do NOT own" item 3 (delegation to Role 4); §11.2 anti-patterns.

**Evidence.**

- §13 row 4 verifies "Role Boundaries contains ≥1 of the 7 taxonomy identifiers; Communication contains refusal template citing the class + statutory criterion." This is a presence check on the specialist's prose; it does NOT verify the specialist actually refuses on adversarial elicitation.
- Role 4 substrate Finding 3 (L94-L111): four independent attack branches each defeat refusal training — HiddenLayer universal-bypass XML configs, Mondillo obscure-text iteration, Han et al. fine-tuning poisoning, Authority Impersonation. The substrate explicitly notes (L109-L111): "the reviewer's verdict must NOT rely on the candidate model's own refusal behavior as the gating signal."
- §2.2 "I do NOT own" item 3 delegates adversarial red-team / exploitability evaluation to Role 4. But Role 4 audits against the template the architect specifies — and the template-level audit (§13) currently has no slot for "this specialist's refusal output was confirmed by an independent grader against adversarial probes."
- §11.2 anti-pattern 6 (line 340) is the closest defense: "I don't classify a specialist profile as 'passing the refusal-class taxonomy check' because the prose mentions FDA; I grep for the 7 named class identifiers from Finding 5." But this is still prose-pattern-matched-then-grep — it is a stronger version of the same surface failure. Substrate L468 (PF-S2-02 medical analog row): "Refusal-trained safety output is necessary but not sufficient evidence."

**Why this is WARN not BLOCK.** The architect explicitly delegates this to Role 4 (§2.2 item 3) and the §13 audit-script absence already acknowledges (§13 status verification: "the design doc cannot claim a defense that hasn't been built"). The structural gap is real but is consistent with the role-boundary discipline. The BLOCK condition would be the architect treating §13 row 4 as the runtime safety gate; the design doc does not make that claim. WARN is appropriate because Role 4's audit cycle needs an anchor — and the anchor isn't in the template's mechanical enforcement map.

**Recommended remediation.** Add a §13 row (PROPOSED, owned by Role 4 contract): "Adversarial-probe pass anchor — specialist's deployment is gated by a Role-4 evaluation log file (path TBD by Role 4 design doc) showing adversarial-probe verdict = DEPLOY or DEPLOY_WITH_OVERRIDE_PATH for this candidate." The architect's template provides the slot; Role 4 fills the procedure.

---

### F-S6 — Image-handling specialists not conditionally required to cite IMAGE_OR_SIGNAL_INPUT + add adversarial-image probes (BLOCK)

**Threat-model category.** S5 multimodal attack surface (Role 4 substrate Finding 2, L81-L92) — Clusmann + Huang documented GPT-4o 70% adversarial-image ASR; Role 4 R13 mandates ≥3 sub-visual injection probes per image-handling candidate.

**Section affected.** §13 row 4 (refusal-class taxonomy mechanical check); §2.2 item 3.

**Evidence.**

- §13 row 4: "Role Boundaries contains ≥1 of the 7 taxonomy identifiers." The check is unconditional and disjunctive — a specialist mentioning ANY one of the 7 class names passes. This means an image-handling specialist (e.g., labs-specialist that reads lab PDFs, future imaging-specialist that reads radiology) can pass §13 row 4 by mentioning, say, `PATIENT_FACING_DIRECTIVE` alone, even if it never references `IMAGE_OR_SIGNAL_INPUT`.
- Role 4 substrate Finding 2 (L81-L92): Clusmann/Kather et al. (Nature Communications, Feb 2025; PMC11785991) demonstrated prompt-injection attacks on lesion-detection VLMs at GPT-4o 70% ASR using sub-visual "black-in-black" injections at 4457×2846 px invisible to human radiologists. Huang et al. (arXiv:2405.20775) extended this to medical MLLMs with 2M-attack and O2M-attack methods. Surgical-video VLM follow-up (medRxiv) extends to temporal injection.
- Role 4 substrate R13 (L438): "Image-handling probes when candidate specialist accepts image input. If candidate specialist's Tools section includes image-input paths, reviewer's probe set includes ≥3 adversarial-image probes including sub-visual injection. **Mechanical Check:** Conditional probe-coverage audit."
- The architect's template §10.4 conditional-load list does NOT include image-content discipline. The lab-PDF read path is plausible at the labs-specialist Tools layer (substrate WIKI.md Agent Consumer).

**Why this is BLOCK.** The labs-specialist is on the critical path to the July 2026 doctor visit per CONTINUATION_BRIEF (read; L25). If lab PDFs contain adversarial injections (third-party-uploaded screenshots, manipulated supplement labels, downloaded radiology reports), the specialist authored against the current template will not have a conditional refusal-class requirement on image input, will not have an adversarial-image probe slot, and §13 row 4 will green-light deployment via the unconditional grep. The 70% ASR figure on GPT-4o is the runtime exposure.

**Recommended remediation.** Amend §13 row 4 to be Tools-conditional: "If specialist's Tools section permits Read against image MIME types OR WebFetch from image-serving URLs, Role Boundaries MUST cite `IMAGE_OR_SIGNAL_INPUT` (mandatory, not disjunctive)." Add a §13 row (PROPOSED): "Image-specialists' Role-4 evaluation log shows ≥3 adversarial-image probes per evaluation cycle (mirrors Role 4 R13)." Add a §14 edge case naming the lab-PDF + sub-visual injection scenario.

---

### F-S7 — Bromism-class dietary/laboratory context-mismatch has no template slot beyond animal→human population-mismatch (NOTE)

**Threat-model category.** Bromism-class context-failure (Role 4 substrate L278, L394-L400, L472).

**Section affected.** §14 EC-4 (population-mismatch); §5 Core Rules; §11.2 anti-patterns.

**Evidence.**

- §14 EC-4 (line 505) covers population-mismatch as animal-only evidence → human dose. This is the INV-RESEARCH-POPULATION-MISMATCH surface (aplus-research IC-7).
- Role 4 substrate L278: the bromism case (Annals of Internal Medicine, 2024/2025) is dietary-context vs laboratory-context — both populations are human. The model gave categorically-correct chemistry (sodium bromide IS a chloride analog) but failed to recognize the dietary-context of the question.
- Substrate L394-L400: "the broader category — 'model gives correct factual content but fails to recognize the deployment context' — is harder to enumerate. The reviewer's probe-generation step must include explicit context-mismatch probes (operator describing a domain that differs from the specialist's declared scope; operator asking a question framed in a context the specialist's training data does not represent). Without this discipline, the reviewer will catch obvious exploit patterns but miss subtle context failures that produce real-world harm."
- The design doc §5 Core Rules has rule 12 (line 160) on GRADE certainty + recommendation-strength, but no rule on context-recognition. §11.2 anti-patterns are all about the architect's own failure modes, not about specialist context-detection.
- The §10 Context Loading list is operator-profile-shape (slow-changing context) and current-state.md (fast-changing context) — no slot for "context of the question itself."

**Why this is NOT (rather than WARN/BLOCK).** The bromism class is mostly a runtime-detection problem; Role 4's probe set carries the procedure. The architect's template-level gap is real but secondary to F-S2 (authority impersonation) and F-S3 (operator-as-adversary) since those are the upstream surfaces of context-bypass. NOTE per Role-4-mapping ("hardening opportunity; defense-in-depth").

**Recommended remediation.** Add a §14 edge case EC-10 (or extend EC-4): "Context-mismatch — operator question's framing differs from the specialist's declared scope (bromism-class)." Specialist must refuse rather than answer with correct factual content in the wrong context. Document required specialist behavior in §5 (a Core Rule on context-recognition) and §11.2 (an anti-pattern recognizing "correct chemistry, wrong context" as a failure mode).

---

### F-S8 — GRADE strong-with-low-certainty "flagged" is undefined; default-allow vulnerability (WARN)

**Threat-model category.** Default-allow analog (Role-4 software-security mapping table — "Default-recommend without GRADE certainty tag = default-allow vulnerability").

**Section affected.** §5 Core Rules item 12; §13 row 2 (evidence-tier ownership mechanical check).

**Evidence.**

- §5 rule 12 (line 160): "Every claim-emitting section requires a GRADE certainty tag (high/moderate/low/very-low) and a recommendation-strength tag (strong/weak/conditional). Strong-with-low-certainty combinations are flagged. The architect does not collapse the two axes into a single 'evidence rating.'"
- The word "flagged" is undefined. Flagged-but-shipped is default-allow. There is no §13 row that HALTs on a strong+low or strong+very-low combination; row 2 only checks that the GRADE vocabulary is present.
- The architect's Pass-1 substrate Finding 2 (read L83-L107 of `design/.health-specialist-architect-design-work/domain-research.md` — not re-quoted here) names GRADE as the two-axis discipline; the architect's design doc encodes the discipline name but not the gating.
- The medical-safety analog of cryptographic-choices: weak-evidence backing a strong recommendation is the medical analog of weak-algorithm-backing a security claim. Per Role 4 substrate L292-L298 (Constitutional AI is the internal-judge primitive), GRADE is the architect's analog primitive; if it's present but not enforced, the gate is decorative.

**Why this is WARN.** The architect documents the discipline and provides Core Rule + §13 row anchoring. The gap is the "flagged means what" ambiguity — which a downstream Role 2 / Role 3 / Role 4 audit could resolve, but only if the architect's template defines the semantics. Without that definition the 14 specialists will interpret "flagged" 14 different ways.

**Recommended remediation.** Define "flagged" mechanically in §5 rule 12: "strong-with-low-certainty combinations HALT the claim and require either (a) downgrading recommendation strength, (b) supplemental evidence raising certainty, or (c) explicit operator-acknowledged-override logged in vault/meta/contradictions.md." Update §13 row 2 to check the HALT condition. Add a §14 edge case naming the GRADE strong+low scenario.

---

### F-S9 — No template slot for many-shot jailbreaking / multi-turn persistence (NOTE)

**Threat-model category.** P7 (multi-turn persistence; Yang et al. 69.4% — substrate L73, L143) + P9 (many-shot jailbreaking; Anil et al. NeurIPS 2024 — substrate L145).

**Section affected.** §5 Core Rules; §13 mechanical enforcement map; §10 Context Loading.

**Evidence.**

- Role 4 substrate Finding 1 (L69-L79): Yang et al. JAMA Network Open reports persistence at turn 6 = 75/108 (69.4%); for one LLM, 86.1%. The ginseng-recommendation subset persisted in 91.1%.
- Role 4 substrate R8 (L428) mandates probe coverage including "many-shot jailbreaking" and "multi-turn dialogue" probes for Role 4 evaluation.
- The architect's design doc has no slot for max-context discipline, no anti-context-flooding clause, no rule constraining how many turns a specialist persists with an operator before re-anchoring against operator-profile / refusal-class taxonomy.
- §10 Context Loading is auto-load discipline at dispatch start; there is no re-anchor discipline mid-dispatch.

**Why this is NOTE.** Per Role 4 substrate, multi-turn is a Role-4 runtime detection surface (probe coverage). The architect's template-level gap is real but recoverable at Role 4's evaluation — provided Role 4 actually probes multi-turn. NOTE rather than WARN because the architect's design doc doesn't structurally exclude this discipline; Role 2 (health-implementer) could add multi-turn re-anchor clauses to specialist Core Rules sections.

**Recommended remediation.** Add a §13 row (PROPOSED): "Specialist Core Rules contains ≥1 re-anchor clause for multi-turn dialogues (re-read operator-profile.md every N turns, default N=3, OR after any operator framing change)." Defer multi-turn-probe-coverage to Role 4's design doc per role-boundary discipline.

---

### F-S10 — Mechanism A (Council-Mode dissent) depends on Role 4 deployment — no fallback during pre-Role-4 phase (WARN)

**Threat-model category.** Three-mechanism anti-sycophancy (architect substrate Finding 3, L108-L129); design doc §2.2 item 6, §4 OUTBOUND row 7.

**Section affected.** §2.2 "I own" item 6 (architectural slot for medical-safety-reviewer as Council-Mode dissent); §4 OUTBOUND row 7; §5 rule 2 (anti-sycophancy three-mechanism).

**Evidence.**

- §2.2 item 6 (line 51): "The architectural slot for `medical-safety-reviewer` (Role 4) as the Council-Mode dissent role; I specify the slot, Role 4's own design doc specifies its internal behavior."
- §4 OUTBOUND row 7: "Architectural slot for medical-safety-reviewer (Role 4) as Council-Mode dissent — Role 4 design doc — Role 4 operates as the structurally-separate Mechanism-A dissent agent for any compound moving researching → planned. Slot defined here; Role 4's internal contract (axes, severity composition, threat-model catalog) is owned by Role 4."
- §5 rule 2 (line 140): "Mechanism A (multi-agent silent agreement, Catfish Agent), Mechanism B (single-model user acquiescence, SycoEval-EM), Mechanism C (RLHF preference drift, Sharma 2024 + Petri). A single 'do not be sycophantic' clause that collapses the three is rejected."
- §17.2 A-3 (line 607): "The 4 foundation roles run sequentially (Role 1 first, OUTBOUND references established for 2/3/4)." This implies the foundation roles deploy before any specialist runs against the template. But §18 OQ-2 (line 633) explicitly notes Role 4 is not deployed at Phase-3 red-team time — the current report is the v1-substitute path.
- Role 4 substrate Limitation 20 (L386): "The deploy/block verdict's adjudication path assumes medical-liaison (Role 7) exists. During the pre-Role-7 phase of the project, override paths route directly to the user — which IS itself a documented risk (operator self-override of safety blocks)." Same structural gap applies to Role 4 during the pre-Role-4 phase: if any specialist deploys against the template before Role 4 exists, Mechanism A's structural counter is missing.

**Why this is WARN not BLOCK.** The architect doc CONTINUATION_BRIEF §7 explicitly carries the v1-substitute path: software security profile briefed on medical-safety. During the pre-Role-4 phase, this is the dissent role. The architect doc does not name the fallback explicitly — that's the structural gap. The gap is recoverable by referencing the v1-substitute in the design doc.

**Recommended remediation.** Add a §17.2 assumption: "A-7 — Pre-Role-4 phase fallback: Mechanism A dissent role is performed by the v1-substitute `security` agent briefed on medical-safety per CONTINUATION_BRIEF §7. The breaks-if condition: Role 4 deployment is delayed past first specialist deployment, AND the v1-substitute is not actually dispatched at design-doc Phase 3 of any specialist." Add a §13 row checking that every specialist's design doc Phase 3 dispatched at least the v1-substitute Mechanism-A dissent agent.

---

### F-S11 — vendor_label-with-number sentence-collision not gated at specialist output layer (WARN)

**Threat-model category.** P2 (LLM02 Insecure Output Handling); INV-RESEARCH-NO-VENDOR-NUMERICAL (whitelist L249); Role-4 mapping ("Citation-integrity / source-whitelist tier discipline").

**Section affected.** §13 rows 11-12; §14 EC-3.

**Evidence.**

- §14 EC-3 (line 497-503) covers the case at dispatch-time: aplus-research IC-3/IC-4 verifier catches vendor_label cite grounding a numerical claim.
- §13 row 11 verifies "Context Loading contains `grep -E 'vault/(library|compounds|biomarkers)|primekg'` ≥1" — KG-grounded retrieval enumeration.
- §13 row 12 verifies "Tools section contains `grep -E 'verify_citation|check_source|wiki_grep'` ≥1" — citation-verification tool listed.
- Neither row greps the SPECIALIST'S OUTPUT for the vendor_label + numerical-claim sentence collision. The aplus-research IC-3/IC-4 catches it at the research-dispatch layer if the specialist USES aplus-research. But §8.1 permits Read against `vault/library` directly — meaning specialists can read existing wiki entries and emit numerical claims sourced from prior entries without dispatching aplus-research again.
- If a prior wiki entry's `vendor_label` tag had a numerical claim slip past IC-3/IC-4 (e.g., an audit-script defect, an unaudited legacy entry, a contradictions.md unresolved entry), the specialist reading that entry would inherit the gap.

**Why this is WARN not NOTE.** INV-RESEARCH-NO-VENDOR-NUMERICAL is an active invariant (INVARIANTS.md L38) with mechanical verification via aplus-research IC-3 + IC-4. The architect's template should mirror that at specialist-output layer, not just at dispatch layer.

**Recommended remediation.** Add a §13 row (PROPOSED): "Specialist output (Communication section emissions writing to vault/compounds/) is grep-audited: a vendor_label tag never appears in the same sentence as dose/effect-size/AE-rate/n claim. Mirror of INV-RESEARCH-NO-VENDOR-NUMERICAL applied to specialist write-paths, not just aplus-research dispatch-paths."

---

### F-S12 — No template slot for eval-awareness probe seeding (Petri 2.0) (NOTE)

**Threat-model category.** P10 (eval-awareness); Role 4 substrate Finding 9 L298-L302; Limitation 15 L394.

**Section affected.** §14 Edge Cases; §13 mechanical enforcement map.

**Evidence.**

- Role 4 substrate L298-L302: "Include explicit eval-awareness mitigations per Petri 2.0 [21] (because models behave differently on evaluations than in production)."
- Role 4 substrate Limitation 15 (L394): "the reviewer's adversarial probes are themselves a safety-relevant evaluation that the candidate model may recognize as an evaluation, producing artificially-safe behavior that does not survive deployment. Petri 2.0 added explicit eval-awareness mitigations [21]; the reviewer's probe set must include eval-awareness probes (probes that look like real production queries with embedded adversarial properties, not probes that look like evaluations)."
- The architect's §14 edge cases (EC-1 through EC-8) all look like evaluations — they have a Situation / Handling / Test stimulus structure. The architect's template encodes test-shaped probes; it does not encode production-shaped probes.
- The single-operator deployment context (substrate L394: "the operator is the only production user") means production-shaped probes can only be derived from operator's actual past dispatch patterns — which the architect's template does not have a slot for.

**Why this is NOTE.** Production-shaped probe generation is a Role 4 runtime concern; the architect's template-level gap is structural-but-recoverable. NOTE per defense-in-depth framing.

**Recommended remediation.** Add a §17.2 assumption: "A-8 — Eval-awareness mitigations are owned by Role 4's probe-generation step; the architect's template does not anchor production-shaped probes. Breaks-if: Role 4's probe set is dominated by test-shaped stimuli (e.g., copies of §14 EC content); the candidate model's eval-awareness produces artificially-safe behavior the architect's template cannot detect."

---

### F-S13 — Indirect injection via Tier-1 fetched content not gated at template-level (NOTE)

**Threat-model category.** A2 + S3 + P1 (indirect injection through retrieved-content channel); Role 4 substrate L121, L132, L137.

**Section affected.** §8.1 Tool palette (Read against vault/library); §10 Context Loading.

**Evidence.**

- §8.1 (line 193): "Read — Pass-1 substrate, source whitelist, existing role profiles (as evidence), INVARIANTS.md, memory/process-failures.md, vault/WIKI.md, vault/meta/*, regulatory primary text." This is permissive at architect-role layer; the template the architect produces will inherit this permissiveness to 14 specialists.
- Source whitelist Tier 1 (read L51-L70 of `vault/library/_source-whitelist.md`) admits 20 hosts including pubmed.ncbi.nlm.nih.gov, ncbi.nlm.nih.gov, nature.com, science.org, etc. These hosts are admissible by tier but the specific page contents can be poisoned — adversarial PMC entries, manipulated PDFs, supplement-page redirects.
- aplus-research IC-13 verifier (INVARIANTS.md L39: INV-RESEARCH-IC13-CORPUS) catches retrieval-time issues — every numerical/quoted claim grep-verified against retrieved source corpus. But specialists may Read vault directly per §8.1, bypassing aplus-research.
- Role 4 substrate L132 (S3 retrieved-content channel) + L137 (P1 indirect injection) jointly establish this as an attack surface independent of refusal-class.

**Why this is NOTE.** The aplus-research dispatch path is the canonical mitigation. The architect's template-level direct-Read permission is a real but narrow exposure surface (operator must construct a wiki entry that the specialist then reads under adversarial framing).

**Recommended remediation.** Add a §10.6 cross-role-reference trigger: "Specialists reading vault/library/ directly (outside aplus-research dispatch) must declare a Tier-Tag-gated Read discipline in their Context Loading section — minimum tier per claim-type per the source whitelist L229-L240 admissibility matrix."

---

### F-S14 — No template slot for multi-turn re-anchor against operator-profile / refusal-class taxonomy (NOTE)

**Threat-model category.** S6 multi-turn dialogue state; P7 + P9 (multi-turn persistence + many-shot jailbreaking).

**Section affected.** §5 Core Rules; §13 mechanical enforcement map; §10 Context Loading.

**Evidence.**

- Substrate L143 (P7) + L145 (P9). Yang et al. 69.4% persistence at turn 6; one LLM 86.1%.
- The architect's §10 Context Loading is dispatch-start auto-load — operator-profile.md / current-state.md / goals.md / source-whitelist are read once at dispatch start. There is no re-read discipline for multi-turn dialogues.
- §5 Core Rules item 8 (line 152) forbids user-supplied unstructured text from grounding template defaults, but this is architect-self discipline, not specialist multi-turn discipline.
- The §10.6 "Cross-role reference triggers" section addresses §4 OUTBOUND/INBOUND but not turn-by-turn re-anchoring.

**Why this is NOTE.** Largely a Role 4 runtime detection surface (per F-S9 above). Listed separately because the multi-turn re-anchor discipline is at template-level (Core Rules emission) whereas multi-turn probe coverage (F-S9) is at evaluation-level. Both NOTE.

**Recommended remediation.** Combine with F-S9's recommendation: §13 row that specialist Core Rules include a multi-turn re-anchor clause; default re-anchor cadence: every N=3 turns OR after any framing-class change in operator input.

---

### F-S15 — Pre-Role-7 escalation routes BLOCK to operator who is A3 (BLOCK)

**Threat-model category.** Role-7 absence (Role 4 substrate L386, Limitation 20); §13 row 6 (R8 risk-floor escalation target).

**Section affected.** §13 row 6; §14 EC-2 + EC-6; §17.2 Assumptions.

**Evidence.**

- §13 row 6: "Loop-Breaking contains `grep -iE '(halt|stop|escalate).*(contraindication|risk.tier)'` ≥1; escalation target is `medical-liaison`."
- §14 EC-2 (line 489): "escalate to medical-liaison's doctor-visit queue."
- §14 EC-6 (line 524): "the specialist routes to medical-liaison."
- medical-liaison is Role 7 of the 14 specialists (per CONTINUATION_BRIEF; read L25-L30 — explicitly named alongside labs-specialist, peptide-specialist as the Pass-3 deferred specialists).
- Role 4 substrate L386: "During the project's pre-Role-7 phase (medical-liaison not yet built), override paths route to the user directly — which is itself a documented risk surface (operator self-override of safety blocks)."
- Per F-S3 above, the operator (Walter) is A3 — the operator-self-harm adversary in Role 4's threat catalog (L122).
- Composition: during the pre-Role-7 phase, every §13 row 6 escalation lands on A3. The architect's template encodes the escalation target without naming the pre-Role-7 fallback. The 14 specialists authored against this template will encode escalation to medical-liaison; specialists deployed before Role 7 exists will route safety blocks to the operator with no separate adjudicator.

**Why this is BLOCK.** This is the structural medical-safety analog of "default-allow under config failure." The escalation path is defined; the escalation target is unbuilt; the fallback target is A3. Per Role 4 substrate L386 ("itself a documented risk surface"), this is acknowledged as a runtime exposure in the substrate but not encoded as a structural defense in the architect's template. Three of the 14 specialists Walter needs by July 2026 (labs-specialist, peptide-specialist, medical-liaison itself per CONTINUATION_BRIEF L25) will be authored against this template — and at least labs-specialist and peptide-specialist could deploy before medical-liaison does.

**Recommended remediation.** Add §13 row 6 amendment: "Escalation target is `medical-liaison` OR — during the pre-Role-7 phase — escalation requires (a) explicit operator-acknowledged-override prose in the specialist response naming the safety block being overridden, AND (b) logging to `vault/meta/contradictions.md` with both the block and the override rationale." Add §17.2 assumption: "A-9 — Pre-Role-7 escalation fallback: until medical-liaison (Role 7) is deployed, escalations route to operator with mandatory override-acknowledgment + contradictions-log. Breaks-if: this assumption is dropped without Role 7 deployment first." Add §14 EC-9 explicitly naming this scenario.

---

## Per-finding rows (compact)

| ID | Threat-model category | Section affected | Severity | One-line description | Cited evidence | Recommended remediation summary |
|---|---|---|---|---|---|---|
| F-S1 | H-class composition (H1/H2 auto-block + worst-case-reachable) | §2.2 item 3; §4 OUTBOUND row 1; §13; §16 | BLOCK | H-class enumeration (H1-H8) absent from OUTBOUND interface; composition rule `max(Role3.nominal, Role4.worst_case_reachable)` has no template-side anchor | substrate L147-L156, L211; doc line 48 | Add 2nd OUTBOUND row + Core Rule + §13 row + §16 invariant for H-class composition |
| F-S2 | P8 Authority Impersonation (81.8% dominant) | §2.2 item 3; §4 row 1; §13 row 4; §11.2 | BLOCK | Refusal-class taxonomy has no `AUTHORITY_FRAMING_BYPASS` class; junior-authority claims (83.3% bypass) inherit untouched into 14 specialists | substrate L105, L143-L144, L304, L324-L328; doc line 48 | Add 8th refusal class; update §13 row 4 grep; add §11.2 anti-pattern |
| F-S3 | A3 (operator self-harm via own-agent) | §2.2; §11.2; §14; §16 | BLOCK | Operator-as-adversary has no slot in role boundaries, anti-patterns, or edge cases; bromism case is the canonical A3 vector and is missing | substrate L122, L278; doc §14 EC-1 through EC-8 | Add §14 EC-9; add §11.2 anti-pattern recognizing operator-as-A3 asymmetry |
| F-S4 | TOCTOU operator-profile → compound write | §2.2 item 1; §13 row 5; §14 EC-1/2/6 | WARN | Operator-profile read and compound write not atomic; no mtime check, no version pin between read and write | doc §13 row 5; operator-profile.md L11-L94 | Add §13 row requiring read+write atomicity OR recorded mtime/hash |
| F-S5 | Refusal-training insufficient as gate | §13 row 4; §2.2 item 3; §11.2 | WARN | Template gates refusal-class taxonomy via prose-presence grep; no template-side anchor for Role 4's adversarial-probe verdict | substrate L94-L111, L468; doc §11.2 item 6 line 340 | Add §13 row (PROPOSED) anchoring Role-4 evaluation log file as deployment gate |
| F-S6 | S5 multimodal injection (Clusmann GPT-4o 70% ASR) | §13 row 4; §2.2 item 3 | BLOCK | §13 row 4 is unconditional disjunctive grep over 7 class names; image-handling specialists pass without citing `IMAGE_OR_SIGNAL_INPUT`; no Role-4 R13 image-probe slot | substrate L81-L92, R13 L438; doc §13 row 4 | Make §13 row 4 Tools-conditional; add Image-specialist §13 row; add §14 edge case |
| F-S7 | Bromism-class context-mismatch | §14 EC-4; §5; §11.2 | NOTE | Population-mismatch covers animal→human; doesn't cover dietary→laboratory or context→context | substrate L278, L394-L400, L472; doc §14 EC-4 line 505 | Add §14 EC-10; add §5 context-recognition Core Rule |
| F-S8 | GRADE strong-with-low-certainty default-allow | §5 rule 12; §13 row 2 | WARN | "Flagged" semantics undefined; flagged-but-shipped is default-allow | doc §5 rule 12 line 160; §13 row 2 | Define "flagged" mechanically; HALT condition; update §13 row 2 |
| F-S9 | P7 + P9 multi-turn / many-shot | §5; §13; §10 | NOTE | No max-context discipline, no multi-turn re-anchor cadence in template | substrate L73 (Yang 69.4%), L142 (Anil), R8 L428 | Add §13 row for multi-turn re-anchor clause in specialist Core Rules |
| F-S10 | Mechanism A pre-Role-4 fallback | §2.2 item 6; §4 row 7; §5 rule 2 | WARN | Council-Mode dissent role depends on Role-4 deployment; no documented v1-substitute fallback | doc §2.2 item 6 line 51, §4 row 7, §18 OQ-2 line 633; substrate L386 | Add §17.2 A-7 v1-substitute assumption; add §13 row for design-doc-Phase-3 dispatch check |
| F-S11 | vendor_label-with-number at specialist output | §13 rows 11-12; §14 EC-3 | WARN | INV-RESEARCH-NO-VENDOR-NUMERICAL mirrored at dispatch layer but not at specialist write-path layer | INVARIANTS.md L38; whitelist L249; doc §14 EC-3 line 497-503 | Add §13 row grep-auditing specialist-output sentence-collision |
| F-S12 | P10 eval-awareness (Petri 2.0) | §14; §13 | NOTE | All §14 edge cases are test-shaped; no production-shaped probe slot; single-operator deployment limits the surface | substrate L298-L302, L394 | Add §17.2 A-8 documenting Role-4 ownership of eval-awareness mitigations |
| F-S13 | A2 + S3 + P1 indirect injection via Tier-1 fetched content | §8.1; §10 | NOTE | Direct Read against vault/library/ permitted in tool palette; bypasses aplus-research IC-13 corpus check | substrate L121, L132, L137; doc §8.1 line 193; whitelist L51-L70 | Add §10.6 cross-role trigger requiring Tier-Tag-gated Read discipline |
| F-S14 | S6 multi-turn re-anchor | §5; §13; §10 | NOTE | No turn-by-turn re-anchor against operator-profile / refusal-class taxonomy | substrate L143, L145; doc §10 Context Loading | Combine with F-S9 remediation: §13 row + Core Rule for multi-turn re-anchor cadence |
| F-S15 | Role-7 absent → escalation lands on A3 | §13 row 6; §14 EC-2/6; §17.2 | BLOCK | Escalation target `medical-liaison` is unbuilt; fallback during pre-Role-7 phase routes to operator (A3); no template-level guard | substrate L386 (Limitation 20); CONTINUATION_BRIEF L25; doc §13 row 6, §14 EC-2 line 489, EC-6 line 524 | Amend §13 row 6 with override-acknowledgment + contradictions-log requirement; add §17.2 A-9; add §14 EC-9 |

## Verdict

**ISSUES** (not PASS, not BLOCK overall).

Rationale: Five BLOCK-class findings (F-S1, F-S2, F-S3, F-S6, F-S15) each correspond to gaps in the architect's OUTBOUND interface contracts that 14 downstream specialists will inherit if Pass 2 of Roles 2/3/4 proceeds without remediation. The design doc is structurally well-formed (audit-script triangle, Pass-1 anchor discipline, body↔bibliography symmetry, Phase-Coverage Matrix) and the architect's role-boundary discipline correctly delegates runtime adversarial review to Role 4. The findings are template-level structural gaps — not architect-role failures — but they nonetheless block downstream consumers.

The verdict is ISSUES rather than BLOCK because:
1. The design doc itself acknowledges (§13 status verification block; §18 OQ-1, OQ-2; §17.1 R-6) that the audit-script is unbuilt and several mechanical defenses are PROPOSED. The architect is not overclaiming mechanical resistance.
2. The BLOCK findings are remediable by adding rows/edge-cases/anti-patterns to the existing structure — no architectural rework required.
3. Role 4 (this v1-substitute) is itself not yet deployed; the report's authority is bounded by the v1-substitute scope per CONTINUATION_BRIEF §7. A real Role 4 audit post-deployment may produce additional findings or downgrade some present findings; this report should be re-run when Role 4 deploys.

Remediation order (highest leverage first):

1. F-S2 (Authority Impersonation refusal-class) — single-row taxonomy addition + grep update; 81.8% attack surface immediately covered.
2. F-S15 (Role-7 escalation fallback) — single §13 amendment + §14 EC-9 + §17.2 A-9; addresses single largest pre-deployment runtime exposure.
3. F-S3 (operator-as-A3 slot) — single §14 EC-9 + §11.2 anti-pattern; addresses the upstream of F-S2 and F-S7.
4. F-S6 (image-handling conditional gating) — single §13 row 4 amendment; addresses labs-specialist critical-path exposure.
5. F-S1 (H-class composition) — single §4 OUTBOUND row + Core Rule + §13 row + §16 invariant; addresses the entire Role-3/Role-4 severity composition interface.

WARN-class findings (F-S4, F-S5, F-S8, F-S10, F-S11) should be addressed in the same Pass-2 cycle but are not blocking. NOTE-class findings (F-S7, F-S9, F-S12, F-S13, F-S14) are hardening opportunities for Pass-3 (specialist roles).

Final attestation: this is a v1-substitute report. All 31 Role-4 threat-model dimensions walked; 15 findings produced; 5 explicit no-finding categories reported per Audit Protocol. The findings are intended to compose with `red-team-adversarial.md` (the first Phase-3 red-team output, already present at 44KB) at Phase 4 verifier reconciliation. Phase 4 verifier (orchestrator-level per PF-S3-01 guard) should re-read each cited line range against the design doc and Role-4 substrate before accepting or rejecting any finding.
