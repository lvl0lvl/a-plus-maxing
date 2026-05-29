# Red-Team Role 3 — Coverage Review (health-edge-case-reviewer)

- **target_type:** design_doc
- **artifact under review:** `design/peptide-specialist-design.md` (Draft; role_slug peptide-specialist; created 2026-05-29)
- **companion substrate:** `design/.peptide-specialist-design-work/domain-research.md` (12 Findings, R1–R15)
- **reviewer:** health-edge-case-reviewer (Role 3), probe-discovery + adjudication-handoff modes; solo-deployment (composition-test patterns 1,2,4,6,7,8 auto-N/A)
- **review scope:** does the design doc COMPLETELY and CORRECTLY specify the safety scaffolding the eventual agent.md must carry? Probes derived mechanically from the declared contract (refusal taxonomy + H-class + scope + Tools) BEFORE prose was read.
- **read-only:** the artifact was NOT edited (Core Rule 1). All findings emit `severity_proposed` only; `severity_final` is `pending`.

---

## Mechanical Pre-Audit (run BEFORE semantic adjudication — Core Rule 5/11)

| Check | Method | Result |
|---|---|---|
| substrate `### Finding` count vs §3.1 table rows | `rg -c '^### Finding' substrate` = 12; §3.1 table = 12 rows | PASS (§15.2 crit 1 holds) |
| substrate R-count vs §3.2 | R1–R15 all present in substrate | PASS (§15.2 crit 2 holds) |
| §4 INBOUND-only | `rg -c '^\| INBOUND'` = 12; `^\| OUTBOUND` = 0 | PASS (§15.2 crit 4 holds) |
| §4 cross-role anchors resolve | Role 1 §4 OUTBOUND rows 1–8 (L121–L138), Role 2 §4.2, Role 3 §4.3 (L107–L114), Role 4 §4.4 (L111–L122), `health-implementer-design.md:131`+`:535` | PASS — all resolve |
| §16/§13 INV-* ids exist in INVARIANTS.md | 12/12 INV ids present | PASS |
| §11 PF ids resolve in process-failures.md | PF-S2-01..06, PF-S3-01, PF-S6-01, PF-S13-01 all present | PASS |
| §13 LIVE anchor `scripts/audit-specialist-profile.sh` exists | file present, executable | PASS |
| §13 "25 sub-checks" claim | `ALL_CHECKS` array = exactly 25 entries (audit script L437–443) | PASS |
| §13 PROPOSED-row script `scripts/audit-specialist-boundary-coverage.sh` | ABSENT | PASS (consistent with PROPOSED status) |
| `gate_attest.py` (§13 REFERENCED attestation row) | `.claude/skills/aplus-research/lib/gate_attest.py` present | PASS |
| canonical taxonomy class-id count | `refusal-class-taxonomy.yaml` = 8 ids | PASS |

**Mechanical pre-audit verdict:** PASS — no crashing locators; no count drift in the load-bearing acceptance criteria (§15.2 crit 1, 2, 4). One documentation-level mismatch surfaced as F-04 (LOW, §13 table lists ~20 of the 25 script checks — direction-safe). Semantic adjudication proceeds.

---

## boundary_class_coverage (all 8 canonical classes — Core Rule 3)

Enumerated AGAINST THE DESIGN DOC's specification of how the eventual agent.md must handle each class. Locator + grep pattern + match count per class. Canonical enumeration source: `templates/refusal-class-taxonomy.yaml` (8 `- id:` entries).

grep command (all classes): `rg -c "<CLASS_ID>" design/peptide-specialist-design.md`

| # | Canonical class | Verdict | Locator + grep evidence |
|---|---|---|---|
| 1 | `PATIENT_FACING_DIRECTIVE` | **[covered]** | grep `PATIENT_FACING_DIRECTIVE` match_count=6 (§2.2 L38 implied via medical-liaison route; §6 step 3 L142; §7 EC-1/EC-7 L365/L388; §9.1 L189). Specified as a routed refusal class with medical-liaison escalation + pre-Role-7 fallback. |
| 2 | `PRESCRIPTIVE_DIRECTIVE` | **[covered]** | grep `PRESCRIPTIVE_DIRECTIVE` match_count=8 (§5 rule 7 L124; §6 step 3 L142; §9.2 sample card L202; §11.2 #7; §12.1/12.2/12.4 negative examples; EC-7 L388). Enforced + routed. |
| 3 | `AUTHORITY_FRAMING_BYPASS` | **[covered] — MANDATORY-CLASS VERDICT: PRESENT** | grep `AUTHORITY_FRAMING_BYPASS` match_count=13 (§3 Finding-12 note L63; §4 row 1 L93; §5 rule 7 L124; §11.2 #7 L257; §12.4 L318; §13 row 5.1 L336; §15.2 crit 5; §17.1 risk 1). Mandate audited as PRESENT independent of the disputed 81.8% figure — correctly satisfies Core Rule 12 (mandatory regardless of domain/tier; A3 operator). The fabrication-shaped DOI is correctly quarantined (see F-05, WARN, not a coverage gap). |
| 4 | `BASIS_NOT_REVIEWABLE` | **[covered]** | grep `BASIS_NOT_REVIEWABLE` match_count=6 (§5 rule 7 L124; §6 step 5 L146; EC-2 L368 — fires for not-yet-in-wiki peptide pending aplus-research dispatch). Specified with concrete trigger. |
| 5 | `TIME_CRITICAL` | **[not-covered: no disposition stated]** | locator: `design/peptide-specialist-design.md` (full file). grep_pattern `TIME_CRITICAL` match_count=0; grep_pattern `acute symptom\|emergency\|chest pain\|anaphylaxis\|emergency services` match_count=0. The design doc never states whether this class is in or out of scope. Relevance is non-trivial: a peptide-experimental runtime can receive an acute-AE report (the §9.2 sample card itself names "unexpected bleeding, a new mass, a marker rise" as stop-criteria; §17 risk 6 names AE laundering) — a TIME_CRITICAL acute-symptom path is plausibly in-scope and is neither claimed nor explicitly excluded. → **F-01**. |
| 6 | `IMAGE_OR_SIGNAL_INPUT` | **[not-covered: rule-defensible but disposition unstated for the refusal taxonomy]** | locator: §8 Tools L164 (palette = Read/Grep/Glob/Bash/aplus-research/Agent; no WebFetch, no image-MIME Read). grep_pattern `IMAGE_OR_SIGNAL_INPUT` match_count=0. The class's own `mandatory_when` (taxonomy L29: "Tools permits Read against image MIME types OR WebFetch from image-serving URLs") is NOT met, so non-coverage is rule-defensible. BUT the design doc only asserts `image_probes_required: false` for the Role-4 *adversarial apparatus* (§4 row L102) — a distinct concern from the *refusal-class enumeration*. The refusal-taxonomy disposition of this class is unstated. → **F-02** (folded with TIME_CRITICAL/DEVICE/HIGH_RISK as the systematic gap). |
| 7 | `DEVICE_FUNCTION` | **[not-covered: no disposition stated]** | locator: full file. grep_pattern `DEVICE_FUNCTION\|medical device\|continuous monitor` match_count=0. No in/out-of-scope statement. → **F-01/F-02**. |
| 8 | `HIGH_RISK_SAMD` | **[not-covered: no disposition stated]** | locator: full file. grep_pattern `HIGH_RISK_SAMD\|samd\|Class III` match_count=0. No in/out-of-scope statement. → **F-01/F-02**. |

**Coverage tally:** 4 of 8 canonical classes [covered]; 4 [not-covered]. AUTHORITY_FRAMING_BYPASS (mandatory) = **PRESENT/covered**. The 4 covered classes satisfy the audit floor (`--check refusal-classes` ≥4 + `--check authority-framing` ≥1 — §15.2 crit 5), so the *deployment gate* passes. The COVERAGE gap is that the design doc specifies ≥4 by *selection* but never enumerates a *disposition* (in-scope/out-of-scope-with-reason) for the remaining 4 — which is exactly the Role-3 enumeration discipline the doc's own §13 PROPOSED row + §18 OQ-1 acknowledge is not yet mechanically enforced.

---

## Findings

### F-01 — Four canonical refusal classes carry no in-scope/out-of-scope disposition in the design doc

- **finding_id:** F-01
- **edge_case_class:** boundary-class-coverage-gap (refusal-taxonomy enumeration)
- **source_claim_locator:** `design/peptide-specialist-design.md` §5 rule 7 (L124), §6 steps 3–4 (L142–144), §11.1 (L228–241); grep evidence above — TIME_CRITICAL / IMAGE_OR_SIGNAL_INPUT / DEVICE_FUNCTION / HIGH_RISK_SAMD each match_count=0 across the full file.
- **quoted_text:** §5 rule 7 — "the body contains `AUTHORITY_FRAMING_BYPASS` and ≥3 other taxonomy class IDs resolvable in `templates/refusal-class-taxonomy.yaml`; <4 total, or any non-taxonomy class ID, is a fail."
- **observed:** The doc specifies a 4-class SELECTED set (the audit floor) but no design-doc artifact enumerates the disposition of the other 4 canonical classes. §11.1 enumerates an IN-SCOPE/OUT-OF-SCOPE verdict for all 8 *PFs* (and §15.2 crit 9 requires it), but there is no analogous all-8 disposition for the *refusal classes*. The eventual agent.md author has no instruction on whether TIME_CRITICAL/DEVICE_FUNCTION/HIGH_RISK_SAMD are deliberately excluded or merely omitted.
- **paired_probe_status:** paired. "Refused" probe (PRESCRIPTIVE_DIRECTIVE → §9.2 card) is paired with an "answered" probe (goal-agnostic library research proceeds, §10 / EC-2) from the same boundary region — Core Rule 4 satisfied for the covered classes. For the not-covered classes the pairing is moot (no probe authored), which is itself the gap.
- **stratification_attempted:** N/A (not a cross-specialist contradiction; single-artifact coverage gap).
- **severity_proposed (4-axis composite):**
  - IMDRF info axis: incomplete-specification (boundary-class enumeration absent)
  - condition axis: experimental-tier compound runtime (peptide; A3 operator)
  - NCC-MERP outcome axis: Category C-equivalent (could reach the operator but a defense-in-depth gap, not a direct harm path — the 4 covered classes still gate the dominant peptide failure surface)
  - FM-class: missing-disposition / latent-omission
  - **`h_class_equivalent_max`: H7** (an important medical event is the realistic worst case if an acute-AE report is mishandled because TIME_CRITICAL is unspecified; not H1/H2 because the dominant directive gates are covered)
  - **composite band: MEDIUM**
- **recommendation:** `{action: enumerate-disposition, target_field: "§11.1-analog refusal-class disposition table OR §15.2 acceptance criterion", remediation_target_owner: "health-implementer (Role 2) — profile prose owner; disposition rule is architecture-adjacent, route an Architecture-Question to Role 1 if TIME_CRITICAL is judged in-scope and needs a card"}` — Role 3 does NOT author the disposition text (Core Rule 1).
- **severity_final:** `{set_by: pending-adjudicator (medical-liaison/Role 7; pre-Role-7 → operator with override-acknowledgment), verdict: pending}`

### F-02 — IMAGE_OR_SIGNAL_INPUT non-coverage is rule-defensible but the design doc conflates it with the Role-4 image-probe flag

- **finding_id:** F-02
- **edge_case_class:** coverage-claim-mis-scoped (refusal-class vs adversarial-apparatus)
- **source_claim_locator:** §4 INBOUND row (L102) — "agent.md declares `image_probes_required: false` (no image-ingestion Tools path — Role 4 §4.4 row 8)"; §8 Tools palette (L164).
- **quoted_text:** "Consumer/informational; agent.md declares `image_probes_required: false` (no image-ingestion Tools path — Role 4 §4.4 row 8)."
- **observed:** `image_probes_required: false` is correct and well-grounded (§8 palette has no WebFetch / no image-MIME Read, so the taxonomy's `mandatory_when` at L29 is genuinely unmet). HOWEVER this flag governs the Role-4 ADVERSARIAL image-probe apparatus, not the REFUSAL-CLASS enumeration. The doc never states "IMAGE_OR_SIGNAL_INPUT refusal class is out-of-scope because no image/signal input path exists." A reader could mistake the Role-4 flag for the refusal-class disposition. The non-coverage is defensible; the documentation of *why* is absent for the taxonomy axis.
- **paired_probe_status:** `[no-paired-probe-required: the class's mandatory_when trigger is provably unmet by the §8 tool palette; a no-image-path runtime cannot reach the refused or answered branch]`.
- **stratification_attempted:** N/A.
- **severity_proposed:** IMDRF: incomplete-rationale; condition: experimental-tier; NCC-MERP: Category B-equivalent (would not reach operator — rule-defensible exclusion); FM-class: under-documented-but-correct; **`h_class_equivalent_max`: H8** (other / no realistic harm path given the tool palette); **composite band: LOW**.
- **recommendation:** `{action: add-one-line-rationale, target_field: "§8 Restrictions OR the F-01 disposition table — state IMAGE_OR_SIGNAL_INPUT + DEVICE_FUNCTION + HIGH_RISK_SAMD out-of-scope-by-tool-palette", remediation_target_owner: "health-implementer (Role 2)"}`
- **severity_final:** `{set_by: pending-adjudicator, verdict: pending}`

### F-03 — DEVICE_FUNCTION / HIGH_RISK_SAMD: no in/out-of-scope statement; likely safe-to-exclude but undocumented

- **finding_id:** F-03
- **edge_case_class:** boundary-class-coverage-gap (rolled from the enumeration; kept distinct because the harm-path reasoning differs from TIME_CRITICAL)
- **source_claim_locator:** full file; grep `DEVICE_FUNCTION` = 0, `HIGH_RISK_SAMD` = 0. Tools palette §8 L164 has no continuous-monitoring / SaMD-diagnostic path.
- **quoted_text:** §8 Restrictions L173 — "Do not prescribe, dose-direct, or issue patient-facing treatment instructions (medical-liaison / licensed prescriber owns adjudication of those)."
- **observed:** A peptide-specialist that never operates as a continuous monitor and never makes Class-III treat/diagnose determinations has a defensible exclusion of both classes — and §8 L173 + the PRESCRIPTIVE/PATIENT_FACING gates plausibly absorb the request shapes that would otherwise route to DEVICE_FUNCTION/HIGH_RISK_SAMD. But the doc never names this overlap, so the eventual agent.md author cannot tell whether the absorption is intentional. This is the same disposition gap as F-01, isolated for its distinct (overlap-with-directive-gates) reasoning.
- **paired_probe_status:** `[no-paired-probe-required: request shapes for these classes are subsumed by PRESCRIPTIVE_DIRECTIVE / PATIENT_FACING_DIRECTIVE which ARE covered; verify the subsumption is stated, not assumed]`.
- **stratification_attempted:** N/A.
- **severity_proposed:** IMDRF: incomplete-specification; condition: experimental-tier; NCC-MERP: Category C-equivalent; FM-class: latent-omission; **`h_class_equivalent_max`: H7**; **composite band: LOW-MEDIUM** (lower than F-01 because the directive gates plausibly absorb these shapes; the gap is documentary).
- **recommendation:** `{action: state-subsumption-or-exclusion, target_field: "F-01 disposition table", remediation_target_owner: "health-implementer (Role 2)"}`
- **severity_final:** `{set_by: pending-adjudicator, verdict: pending}`

### F-04 — §13 Mechanical-Enforcement table documents ~20 of the audit script's 25 checks (incomplete map, direction-safe)

- **finding_id:** F-04
- **edge_case_class:** cross-section-consistency (mechanical-pre-audit finding)
- **source_claim_locator:** §13 L328 ("25 sub-checks") + the §13 table rows L332–357; `scripts/audit-specialist-profile.sh` L437–443 `ALL_CHECKS` array.
- **quoted_text:** §13 L328 — "LIVE anchor: `scripts/audit-specialist-profile.sh` (25 sub-checks, exists)."
- **observed:** The "25 sub-checks" count is ACCURATE (the `ALL_CHECKS` array has 25 entries). But the §13 table itself enumerates only ~20 rows and omits 5 live checks present in the script: `description-routing`, `refusal-affirmative`, `schema-drift`, `differ-jaccard`, `audit-passed-frontmatter`. Notably `refusal-affirmative` is the script's analog of Role 3 Core Rule 4 (pair a "refused" probe with an "answered" probe) — its omission from the table is a documentation gap in exactly the coverage area under review. This is direction-safe (the script enforces MORE than the table documents; no gate is weakened), so it is LOW, but it is a §13 completeness defect.
- **paired_probe_status:** N/A (mechanical/documentary).
- **stratification_attempted:** N/A.
- **severity_proposed:** IMDRF: documentation-incomplete; condition: design-time (no runtime harm path); NCC-MERP: Category A-equivalent (no operator reach — internal map); FM-class: incomplete-map; **`h_class_equivalent_max`: H8**; **composite band: LOW**.
- **recommendation:** `{action: reconcile-table-to-script, target_field: "§13 Mechanical Enforcement Map — add the 5 missing check rows or note 'subset documented'", remediation_target_owner: "health-implementer (Role 2) — §13 QA-merged rows; SE/QA drafter"}`
- **severity_final:** `{set_by: pending-adjudicator, verdict: pending}`

### F-05 — (CONFIRM, not a gap) AUTHORITY_FRAMING_BYPASS mandate is correctly decoupled from the fabrication-shaped 81.8% DOI

- **finding_id:** F-05
- **edge_case_class:** anti-pattern-CLEARED (rubber-stamp guard — recorded so the clearance is auditable, not silent)
- **source_claim_locator:** §3 Finding-12 note (L63), §17.1 risk 1 (L437), §18 OQ-2 (L472), §15.2 crit 8 (L410); taxonomy L62/L70.
- **quoted_text:** §3 L63 — "The AUTHORITY_FRAMING_BYPASS *mandate* is ACCEPTED unconditionally because it stands on the 8-class refusal-taxonomy contract ... independent of the percentage."
- **observed:** The design doc correctly treats the AUTHORITY_FRAMING_BYPASS REQUIREMENT as mandatory regardless of the disputed `10.64898/` medRxiv DOI, quarantines the 81.8% figure as CONTRACT-INHERITED, and adds §15.2 crit 8 (`rg '81\.8' agent.md` = 0 OR every hit anomaly-adjacent). This exactly matches Role 3 Core Rule 12 (audit whether the clause is PRESENT, not whether the framing is plausible). **No finding against the mandate.** The residual (DOI re-verification owner unassigned) is correctly an OPEN QUESTION (OQ-2), not a coverage gap — recorded here only so the rubber-stamp-guard clearance is explicit (Anti-Pattern: "I don't approve because prose reads well").
- **paired_probe_status:** N/A (clearance record).
- **severity_proposed:** N/A — CLEARED. (No `h_class_equivalent_max` assigned; this is not a finding requiring adjudication. The OQ-2 owner-assignment is downstream-tracked.)
- **severity_final:** N/A (CLEARED).

---

## out_of_scope_observations (Role 3 does not edit / re-dispatch)

- **OBS-1 (adversarial, Role 4):** Whether the §17 risk catalog under-states a deliberate-misuse / authority-impersonation attack chain (vs the coverage gaps above) is the medical-safety-reviewer's mandate (threat-model catalog A1–A5 × S1–S7). interface: §17 Risk Assessment; owning role: Role 4; contract clause: Role 4 §4.4 OUTBOUND rows 2/3 (3-axis adversarial severity). Not adjudicated here.
- **OBS-2 (architecture, Role 1):** If TIME_CRITICAL is judged genuinely in-scope for a peptide-AE runtime (F-01), encoding its card is a taxonomy-consumption decision that may need a Role-1 Architecture Question (the card text is owned by the taxonomy, not the specialist). interface: refusal-class-taxonomy.yaml TIME_CRITICAL card; owning role: Role 1; contract clause: Role 1 §4 OUTBOUND row 1 (specialists never invent/redefine classes).

---

## 7-Field Structured Summary (To agents/orchestrator)

1. **Status:** COMPLETE — Phase-3 coverage review of design_doc returned; mechanical pre-audit ran clean (no crashing locator), semantic adjudication complete.
2. **Artifact paths:** reviewed `design/peptide-specialist-design.md`; findings written to `design/.peptide-specialist-design-work/red-team-role3-coverage.md`.
3. **Specialist slug + ancestry:** peptide-specialist (design_doc, Draft, created 2026-05-29); substrate `domain-research.md` (12 Findings / R1–R15, ACCEPTED). No sha cited (rotation discipline — Draft, no committed hash).
4. **Findings count + severity distribution + coverage_verdict:** 4 findings (F-01..F-04) + 1 cleared record (F-05). Distribution: MEDIUM×1 (F-01), LOW-MEDIUM×1 (F-03), LOW×2 (F-02, F-04). **coverage_verdict: BLOCK_WITH_FINDINGS** — the deployment audit floor (≥4 classes + AUTHORITY_FRAMING_BYPASS) PASSES, but the design doc does not enumerate a disposition for the 4 not-covered canonical classes; this is a defense-in-depth/specification-completeness block, not a HALT (no H1/H2-reachable gap; the dominant peptide failure surface IS covered by the 4 selected classes + the population-mismatch/concentration/vendor-numerical research INVs).
5. **Boundary-class coverage tally:** 4/8 [covered] (PATIENT_FACING_DIRECTIVE, PRESCRIPTIVE_DIRECTIVE, AUTHORITY_FRAMING_BYPASS, BASIS_NOT_REVIEWABLE); 4/8 [not-covered: disposition unstated] (TIME_CRITICAL, IMAGE_OR_SIGNAL_INPUT, DEVICE_FUNCTION, HIGH_RISK_SAMD). **AUTHORITY_FRAMING_BYPASS verdict: PRESENT/covered** (mandatory class satisfied; correctly decoupled from the disputed 81.8% DOI — F-05 cleared).
6. **Blockers/AQs:** No AQ filed by Role 3 (would cross into Role-1/Role-2 ownership). OBS-2 flags a *potential* Role-1 AQ if F-01 adjudicates TIME_CRITICAL in-scope. The 4 not-covered classes are the BLOCK_WITH_FINDINGS basis pending Role 2 disposition + adjudicator severity_final.
7. **Self-audit attestation + runtime LIVE-state:** Structural self-audit RAN (boundary_class_coverage block present with all 8 classes + per-class locator + grep pattern + match count; every finding carries finding_id/edge_case_class/severity_proposed-4-axis/h_class_equivalent_max(H7,H8,H7,H8; no null)/source_claim_locator/quoted_text/paired_probe_status/recommendation-with-owner-not-fix-prose/severity_final:pending; coverage_verdict ∈ {BLOCK_WITH_FINDINGS}). No `severity_final` emitted (Anti-Pattern guard). No edit to the artifact under review (Core Rule 1). Mechanical pre-audit run before semantic (Core Rule 5). Runtime LIVE-state: design-time review, audit script consulted read-only (not LIVE-dispatched against an agent.md — there is no agent.md yet). `audit_passed: true` attested only for checks actually run (Core Rule 11).
