# ADR Evaluation Rubric — Plan-Generation Engine (S92)

**Task type:** document (ADR set). **Scope:** 6 ADRs (0020–0025). **Pass threshold:** every APPLICABLE dimension ≥ 9/10 on every ADR, shipped on honest+complete verification through a **bounded revise loop (≤1 pass)** — not a 99/100 aggregate chase (F-006). A 10 on any dimension requires the judge's explicit verification statement (judge-discipline §3.5); absent it, the ceiling is 8.

**Dimension applicability:** dimensions 1–9 apply to ALL 6 ADRs. **Dimension 10 (PII-Boundary Soundness) applies to ADR-0020 and ADR-0021 ONLY** (the de-id IN / de-id OUT boundary decisions); it is scored **N/A** for ADR-0022–0025 and does not count toward their pass bar. So 0020/0021 are scored on 10 dimensions, 0022–0025 on 9.

**Load-bearing note (the crown jewel):** ADR-0020 (de-id IN) and ADR-0021 (de-id OUT) move raw PII across an API boundary / re-insert real PII — a one-way door in a public + alpha-shared repo. They are guarded on THREE independent axes (no single strong score halos over the others): **dim 10** scores whether the boundary DESIGN is fail-closed (failure mode, egress class, no-train trust, non-committed re-insertion, the de-identified-store invariant + its enforcement mechanism); **dim 4** scores whether a raw-PII-leak FALSIFICATION TEST with a 0-leak threshold exists; **dim 9** scores whether the CONSEQUENCES measurably address the boundary. An auto-fail backstops all three.

---

## Dimensions (9 required, ADR-tuned) — anchors at 0–3 / 4–6 / 7–8 / 9–10

### 1. Citation Traceability
Every factual/quantitative claim carries a confidence-tagged citation that resolves to a real source (file:line, ADR §, URL, or vault note).
- **0–3:** Claims about the live tree present with no citations, OR a citation that does not resolve (wrong file/line, dead URL).
- **4–6:** Most claims cited but ≥1 load-bearing claim uncited, or confidence tags missing/wrong on several.
- **7–8:** All claims cited and resolving; 1–2 confidence tags imprecise (e.g. [VERIFIED] on a vendor claim).
- **9–10:** Every claim cited, every citation resolves on check, every confidence tag accurate. **Auto-fail:** any fabricated citation (invented file/symbol/URL/number).

### 2. Anti-Pattern Compliance
Zero of the 11 ADR anti-patterns (AP-01 Fairy Tale … AP-11 Uncredited Source Bias) detected across sections.
- **0–3:** ≥1 auto-fail anti-pattern present (AP-03 zero negatives, AP-04 dummy alternative, AP-08 Mega-ADR bundling >1 decision).
- **4–6:** A soft anti-pattern present (AP-02 Sales-Pitch rationale, AP-06 Tunnel Vision one-alternative, AP-07 Blueprint-in-Disguise impl detail).
- **7–8:** No anti-patterns, but a section leans toward one (e.g. Context with mild advocacy).
- **9–10:** All 11 checks clean across every section, verified section-by-section. **Auto-fail:** AP-03 (no Negative consequence).

### 3. DAG Integrity
Related Decisions match the dag.md edges; relationships bidirectional; types from the closed 5-vocabulary (depends-on / enables / constrains / complements / tensions-with); no cycle; no orphan.
- **0–3:** A cycle in the graph, OR an ADR references a nonexistent ADR.
- **4–6:** An edge in dag.md missing from an ADR's Related Decisions (or vice versa); a relationship type outside the closed vocabulary.
- **7–8:** All edges present + bidirectional; 1 relationship-type arguably mislabeled (e.g. constrains vs depends-on).
- **9–10:** Every Related Decisions entry matches dag.md bidirectionally with the correct type; no cycle; no orphan; verified against dag.md. **Auto-fail:** cycle in the dependency graph.

### 4. Falsification Quality
Validation Approach carries BOTH confirmation AND falsification criteria with quantitative thresholds. **(0020/0021: must include the raw-PII-leak falsification test.)**
- **0–3:** Validation section is "review periodically" / prose-only with no testable criterion.
- **4–6:** Confirmation criteria present but falsification criteria absent or non-quantitative ("if it seems wrong").
- **7–8:** Both present and testable; thresholds present but one is soft, OR (for 0020/0021) the PII-leak test named but without a 0-leak quantitative threshold.
- **9–10:** Both present, testable, quantitatively thresholded; a developer could write the test from them. **For 0020/0021:** a raw-PII-leak falsification test with a 0-raw-PII-past-boundary / 0-raw-PII-in-committed-file threshold on a crafted-input probe is explicit. **Auto-fail:** Validation section contains only "review periodically."

### 5. Dissent Preservation
Every rejected alternative has substantive rejection rationale (not straw-man); real trade-offs recorded with attribution where applicable.
- **0–3:** A dummy/straw-man alternative present only to be dismissed (AP-04).
- **4–6:** Alternatives listed but ≥1 dismissed in a sentence with no analysis of its real trade-off.
- **7–8:** All alternatives analyzed substantively; one rejection rationale thin.
- **9–10:** Each alternative gets genuine comparative analysis of why it lost; the live trade-offs (e.g. for 0020: full-model-de-id-IN vs deterministic-gate-IN + model-OUT-only vs hybrid) are weighed, not strawed. **Auto-fail:** dummy alternative (AP-04).

### 6. Cross-Reference Consistency
Every Related Decisions entry names a real ADR; the relationship is reciprocated in the target; terminology consistent across the set.
- **0–3:** References a nonexistent ADR, OR a claimed relationship absent from the target ADR.
- **4–6:** A reference not reciprocated in the target (one-directional), or an existing-ADR amendment (e.g. 0020↔0016) named in one direction only.
- **7–8:** All references reciprocated; shared terms mostly consistent; 1 term drift (e.g. "de-id boundary" vs "de-id wrapper").
- **9–10:** Every reference reciprocated with matching type; the amendments to ADR-0004/0016 and supersession of the runtime-A design doc are reciprocal and consistent; shared vocabulary uniform. **Auto-fail:** references nonexistent ADR.

### 7. Y-Statement Fidelity
The Y-Statement faithfully compresses the full ADR (context/concern/decision/quality-goal/trade-off) with no omission or addition.
- **0–3:** Y-Statement contradicts the body (claims a decision the body rejects).
- **4–6:** Y-Statement omits the load-bearing trade-off, or adds a claim absent from the body.
- **7–8:** Faithful; the accepted trade-off is named but generically.
- **9–10:** Compresses context+concern+decision+quality-goal+the specific accepted trade-off, all traceable to the body. **Auto-fail:** Y-Statement contradicts body.

### 8. Template Completeness
All 11 sections present with substantive content; no placeholder/TBD; each ADR 1–2 pages (no Mega-ADR / Novel-Epic).
- **0–3:** A section empty or containing TBD/TODO/[fill in].
- **4–6:** All sections present but ≥1 is a stub heading with one line.
- **7–8:** All sections substantive; one slightly thin, or the ADR runs long (>2 pages → AP-09 watch).
- **9–10:** All 11 sections substantive, within the 1–2 page bound, no placeholder. **Auto-fail:** any section empty or "TBD."

### 9. Analytical Depth
Context describes forces with specific live-tree evidence; Rationale compares across multiple criteria; Consequences are specific + measurable. **(0020/0021: Consequences must measurably address the PII boundary + name the de-identified-store invariant.)**
- **0–3:** Context <100 words / no evidence; Rationale with no comparative analysis; Consequences with no measurable impact.
- **4–6:** Context cites forces but vaguely; Rationale compares on one criterion only; Consequences qualitative.
- **7–8:** Context grounded in the live tree; Rationale compares on multiple criteria; Consequences mostly measurable; (0020/0021) the PII boundary discussed but the de-identified-store invariant implicit.
- **9–10:** Context forces evidenced with file:line/ADR§; Rationale weighs ≥2 alternatives on ≥2 criteria each; Consequences specific + measurable. **For 0020/0021:** Consequences measurably address the fail-closed PII boundary AND state "the persisted/committed store stays de-identified" explicitly. **Auto-fail:** Context <100 words, OR Rationale with no comparative analysis, OR Consequences with no measurable impact.

### 10. PII-Boundary Soundness — **ADR-0020 & ADR-0021 ONLY (N/A for 0022–0025)**
Scores whether the de-identification boundary DECISION is designed fail-closed and threat-modeled — independent of whether a test exists (dim 4) or consequences are measurable (dim 9). The crown-jewel axis: raw PII crossing the API boundary (IN) / real PII re-inserted onto the artifact (OUT).
- **0–3:** Authorizes raw-PII transit (IN) or PII re-insertion (OUT) with NO fail-closed design (open-by-default), OR no "persisted/committed store stays de-identified" invariant. (Also the engine-load-bearing auto-fail.)
- **4–6:** Fail-closed asserted but the failure mode is unspecified (what happens on API error / partial de-id / model returns PII?), OR the single egress class is not enumerated, OR the de-identified-store invariant is stated with no named enforcement mechanism (which hook/gate holds it).
- **7–8:** Fail-closed design with the failure mode specified + the egress class enumerated + the de-identified-store invariant tied to a named enforcement mechanism (`block-pii-commit` / `pre-push-pii-scan` / the gate), but ONE residual path unaddressed (e.g. the re-inserted-PII artifact's storage location, or the API-provider no-train trust assumption, or the local-model substitution seam's boundary behavior).
- **9–10:** Fail-closed boundary whose failure mode errs to no-egress/no-plan; the single egress class enumerated; the "persisted/committed store stays de-identified" invariant explicit AND bound to its enforcement mechanism; the no-train API trust assumption stated; the re-inserted-PII artifact's NON-committed (gitignored, ADR-0005) storage specified; the substitution seam (API/local/combo) does not foreclose a stricter boundary. Verified against ADR-0001/0005/0016 boundaries. **Auto-fail:** raw-PII transit / re-insertion authorized without a fail-closed design + the de-identified-store invariant.

---

## Automatic Fail Conditions (checked FIRST; any → REJECT without scoring the rest)
**Universal:** fabricated content (invented source/symbol/API/number); the ADR file does not exist / is empty / is not an ADR; a safety/data-integrity violation the ADR itself introduces.
**Document-type:** a broken reference to a file/section/ADR the document instructs the reader to use.
**ADR-specific (from the per-dimension auto-fails above):** fabricated citation · AP-03 (no negative consequence) · DAG cycle · Validation = "review periodically" only · AP-04 dummy alternative · references nonexistent ADR · Y-Statement contradicts body · empty/TBD section · Context <100 words / no comparative Rationale / no measurable Consequences.
**Engine-load-bearing (0020/0021 only):** the ADR authorizes raw PII across the API boundary or PII re-insertion WITHOUT a fail-closed design AND the explicit "persisted/committed store stays de-identified" invariant → REJECT (a silent crown-jewel relaxation is a data-integrity violation).

## Verification Checklist (worker self-checks before submit; judge confirms)
- [ ] Every verifiable claim has a resolving citation; no fabricated source/symbol/number.
- [ ] Every Related Decisions pointer resolves and is reciprocated; types from the closed 5-vocabulary.
- [ ] Stated counts/IDs match the actual artifacts (ADR numbers, the 6-ADR set).
- [ ] All 11 sections present, substantive, no TBD; 1–2 pages.
- [ ] ≥1 Negative consequence; ≥1 substantively-analyzed real alternative.
- [ ] Validation has confirmation + quantitatively-thresholded falsification criteria; (0020/0021) the raw-PII-leak test with a 0-leak threshold.
- [ ] Each auto-fail checked and not triggered.

## Pass Threshold
Every APPLICABLE dimension ≥ 9/10 on every ADR (0020/0021 = 10 dims; 0022–0025 = 9 dims, dim 10 N/A). Bounded revise loop ≤1 pass (create-adr Phase 6, F-006). If a dimension still <9 after the single revise → escalate to the user (adjust rubric / provide guidance / accept-with-noted-deficiencies), do not lower the bar silently.
