# /upgrade-agent Phase 5 — genetics-specialist synthesis

Authored by the deployed `health-implementer` agent (Role 2), full profile inlined per INV-ROLE-INLINING.

## Deliverables
- `.claude/agents/genetics-specialist/agent.md` — foundation-shape (no frontmatter); H1 + ≤40-word function sentence + IDENTICAL block + exactly 11 `## ` sections, each carrying a `**Mechanical Check:**` line.
- `.claude/agents/genetics-specialist/library-index.md` — 9 lines, 1 `vault/library/` conditional ref.

## Metrics
- **agent.md line count:** 170 (≤200 BLOCK ceiling — PASS).
- **`## ` section count:** 11 (Identity, Core Rules, Role Boundaries, Ask vs Proceed, Loop-Breaking, Tools, Communication, Context Loading, Anti-Patterns, Modes, Negative Examples — R13-6.5 PASS).
- **library-index.md line count:** 9 (≤30 BLOCK ceiling — PASS).
- **Identity:** 40 words, 0 banned adjectives (R13-1 PASS).
- **Refusal classes in Role Boundaries:** 8/8 taxonomy classes, AUTHORITY_FRAMING_BYPASS present ×4 (R13-5 / R13-5.1 PASS).
- **GRADE:** certainty=2, strength=1, strong-with-low HALT pair=2 (R13-5.5 PASS).
- **Anti-sycophancy:** Mechanism A/B/C all present (R13-5.6 PASS — satisfied by the IDENTICAL block).
- **PF ids in Anti-Patterns:** 6 distinct (PF-S2-01, PF-S2-02, PF-S2-04, PF-S2-05, PF-S3-01, PF-S6-01), all resolving in `memory/process-failures.md` (R13-11 PASS).
- **Mode floor:** `aplus-research --mode=deep --target-class=reference`; mode-floor-correctness = deep against the genetics row in `specialist-risk-class.yaml`; no bare `deep-research` (R13-12 / 12.5 / 12.6 PASS).
- **Operator no-writeback:** 0 leaks, 5 operator-profile path refs (R13-6.7 PASS).
- **Negative Examples:** 6 BAD/GOOD markers (3 pairs), each citing an anti-pattern (R13-10 PASS).
- **Mechanical stubs:** all 11 sections covered (R13-7 PASS).

## Audit result
`scripts/audit-specialist-profile.sh ... --role-table <main>/templates/specialist-risk-class.yaml`
→ **0 violation(s) / EXIT=0**; 1 WARN (R13-3 token count 8622 cl100k > 2500 ~target — documented medical-density overrun per DOCUMENT_RUBRIC Rule 7 / bead 2qq; the ≤200-line ceiling is the BLOCK and is 170, so WARN does not flip the exit code).

## IDENTICAL block provenance
sha256 = `35dbda2fb9d99540aa7a1487f764c44b1553cfab33d13eb2015e0f4bd390b6f1` — byte-for-byte identical to the deployed `cardiovascular-specialist/agent.md` sibling (verified via `diff`, empty).
