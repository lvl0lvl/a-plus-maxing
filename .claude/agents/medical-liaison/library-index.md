# medical-liaison — library index

Conditional references. Load only when the named adjudication or collation step needs it; never pre-load.

- `vault/library/methodology/evidence-tiers.md` — the GRADE two-axis (certainty × strength) tier definitions. Load when tagging a surfaced interaction/contraindication line or resolving a strong-with-low HALT.
- `templates/refusal-class-taxonomy.yaml` — the 8 canonical classes. Load to recognize an `AUTHORITY_FRAMING_BYPASS` / `PRESCRIPTIVE_DIRECTIVE` frame at the adjudication boundary.
- `design/medical-safety-reviewer-design.md` §4.4 — the `safety_finding` schema and band→verdict mapping. Load when an inbound finding looks malformed.

Skip-pre-loading: do not load other specialists' wiki entries or design docs "just in case." Operator content is read at runtime from `vault/meta/operator-profile.md`, never persisted here.
