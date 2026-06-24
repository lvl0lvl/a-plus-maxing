# ADR Evaluation Rubric — Plan-Generation Engine Live-Wiring (ADR-0026, ADR-0027)

Pass: **every dimension ≥9/10**, then ship on honest+complete verification with a bounded revise loop (≤1 pass) — NOT a 99/100 aggregate chase (F-006). Auto-fail short-circuits to REJECT regardless of other scores.

The 10th dimension (**PII-Boundary Integrity**) is added for THIS run because the wiring crosses the crown-jewel PII boundary (the API de-id-IN seam + the API-for-PII / subscription-for-else split + the deterministic de-id-OUT). It mirrors the PII dimension the S92 engine ADR run added. This is the most-rigorous posture for a PII-wiring ADR set.

| # | Dimension | 10/10 Anchor | Auto-Fail Condition |
|---|-----------|-------------|---------------------|
| 1 | Citation Traceability | Every factual claim has a citation with a confidence tag ([VERIFIED]/[UNVERIFIED]/[VENDOR-CLAIM]/[SECONDARY-SOURCE]); every citation resolves to a real source (a real file:line/symbol, a real ADR, a real Anthropic API fact) | Any fabricated citation (a file:line/symbol or API fact that does not resolve) |
| 2 | Anti-Pattern Compliance | Zero anti-patterns across all 11 checks per section | AP-03 (Free Lunch Coupon): a Consequences section with no Negative consequence |
| 3 | DAG Integrity | All relationships bidirectional, no cycles, no orphans, types from the closed 5-type vocabulary (depends-on/enables/constrains/complements/tensions-with) | A cycle in the dependency graph |
| 4 | Falsification Quality | Every Validation Approach has BOTH a testable confirmation criterion AND a falsification criterion with quantitative thresholds (e.g., "0 raw PII tokens past the de-id seam in N fixtures"; "the live run dispatches exactly K specialists") | A Validation section that says only "review periodically" |
| 5 | Dissent Preservation | Every rejected alternative (A/B/C driver models; model-backed-OUT; folding 0027 into 0026) has a substantive rejection rationale, not a straw-man | A dummy alternative (AP-04) — an obvious-loser with no real analysis |
| 6 | Cross-Reference Consistency | Every Related-Decisions entry matches the DAG; relationship types accurate bidirectionally; the amends-ADR-0022 / implements-ADR-0020 edges are reciprocated | An ADR references a nonexistent ADR, or an edge that ADR-0022/0020 does not reciprocate |
| 7 | Y-Statement Fidelity | The Y-Statement faithfully compresses the full ADR — no claim absent from the body, no material body content omitted | The Y-Statement contradicts the body |
| 8 | Template Completeness | All 11 template sections present with substantive content; no placeholder/TBD/TODO | Any section empty or containing "TBD" |
| 9 | Analytical Depth | Context describes the forces with specific code-grounded evidence (the synchronous-dispatch tension is shown, not asserted); Rationale compares the driver models across ≥3 criteria (fidelity to the built loop, subscription-vs-metered cost, swappability); Consequences are specific + measurable | Context under 100 words, OR Rationale with no comparative analysis, OR Consequences with no measurable impact |
| 10 | **PII-Boundary Integrity** (crown-jewel, this run) | The ADR makes the PII boundary unambiguous: the de-id-IN model call is the ONLY raw-PII egress (no-train API), every subscription dispatch is over the de-identified summary (`SUMMARY_FIELD_SET`-bounded, ADR-0001), de-id-OUT is deterministic (no model), the key is runtime-injected + never tracked/printed/committed (ADR-0005); the seam stays swappable (all-API / local-model) without re-opening the boundary; reconciles ADR-0016's egress relaxation | The ADR permits raw PII into a subscription dispatch, OR a model on the de-id-OUT path, OR the API key in a tracked/printed/committed location, OR contradicts ADR-0001/0005/0016 |

## Notes for judges
- Dimension 10 is NON-NEGOTIABLE: this run exists because the wiring crosses the crown-jewel boundary. A 10 here requires an explicit verification statement (what was checked: the summary-field whitelist on the subscription path, the deterministic-OUT, the runtime key handling).
- 10/10 on any dimension requires an explicit verification statement (what was checked + how it passed) — not "generally good".
- Citation Traceability (dim 1) for code/API claims uses the verification report; do not re-verify in the judge.
