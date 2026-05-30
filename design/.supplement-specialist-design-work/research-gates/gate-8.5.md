# Phase 8.5 — LAYERS GATE

Run: `aplus-research` deep / supplements-landscape
target_type: **reference** (landscape substrate)

**Reference-landscape adaptation:** Because target_type=reference, the two mandatory layers required by Hard Rule 3 (prescribing-practice + non-English) were not written as standalone vault compound-entry files. They were dispatched as Sections **D** and **E**, passed the Phase-3.5 judge gate at deep-99, and folded into the landscape substrate. This gate verifies them in their as-folded form at `sections/section-D.md` and `sections/section-E.md`.

Files verified:
- Prescribing-practice layer → `sections/section-D.md`
- Non-English layer → `sections/section-E.md`

---

## Check 1 — Each layer has its own `## Bibliography` and `## Self-check`

**PASS.**
- Section D: `## Bibliography` present (L146, 14 numbered sources) and `## Self-check` present (L240). (Also carries post-fix grep-audit appendices — out of gate scope, no impact.)
- Section E: `## Bibliography` present (L52, 7 numbered source-lineages) and `## Self-check` present (L64).

Both layers self-contained with their own apparatus.

---

## Check 2 — Prescribing-practice layer (D)

Required: (a) ≥1 compounding-pharmacy data sheet OR an explicit "no admissible data sheet located" with a searched list; (b) practitioner conventions rendered as convention-not-trial-validated.

**PASS.**

(a) **"No admissible data sheet located" + searched list — SATISFIED.** The self-check (L259-262) explicitly states "No admissible Tier-3 `compounding_data_sheet` was located for these OTC supplements (compounding-pharmacy data sheets in the whitelist are peptide-oriented; OTC supplements are not compounded)" and supplies a searched-but-blocked list: ifm.org vitamin-D article (HTTP-403), examine.com ashwagandha page (HTTP-403). The negative finding is well-reasoned (OTC supplements are not compounded, so the peptide-style data sheet has no analogue here) rather than an empty miss. A venue-level practitioner source ([2] IFM, `practitioner_protocol`) is additionally documented, with an honest PARTIAL flag that author+date are not yet captured.

(b) **Convention-not-trial-validated rendering — SATISFIED.** Every practitioner/community dose is rendered as convention, not as a validated/recommended dose:
- D1 vitamin D 50–80 ng/mL target = "practitioner convention, NOT trial-validated," with Tier-1 contradiction (Veugelers & Ekwaru) given primacy and both reported.
- D2 creatine loading = "speed-of-saturation convention, not a necessity," with the originating Tier-1 trial (Hultman 1996) explicitly contradicting the necessity framing.
- D3 stack doses = `combination_evidence: none` / inherits weakest component rung; branded-extract doses flagged manufacturer-funded and extract-specific.

No practitioner dose is phrased as "the recommended/safe dose." Where Tier-1 contradicts convention, academic source given primacy and both reported (per whitelist Tier-2.7 rule).

---

## Check 3 — Non-English layer (E)

Required: (a) survey of ≥3 of {Russian, Chinese, originator-country, Korean, Japanese} with explicit findings or "no admissible primaries located"; (b) single-source-language concentration surfaced as a caveat.

**PASS.**

(a) **≥3 languages surveyed with explicit findings — SATISFIED (3 of 5).** Three language families covered, each with explicit verified-primary findings:
- **Russian** (E1): Semax/Selank/Noopept preclinical [1, animal]; Mexidol EPICA RCT n=150 [2, rct]; Cerebrolysin Cochrane review [3, meta_analysis].
- **Chinese** (E2): Berberine 46-RCT meta-analysis via CNKI/Wanfang/VIP [4, meta_analysis]; Rhodiola CONSORT quality review with Chinese-only species [5, meta_analysis].
- **Originator-country** (E3): Ayurvedic classical texts for Withania [6]; German Commission E monographs for ginkgo/St. John's wort [7, regulatory].

Additionally carries an explicit "no admissible primaries located" note for the Khavinson peptide bioregulators (Epitalon/Thymalin/Vilon/Cortexin) — every hit was a non-whitelisted vendor/blog host; the 775-papers / lifespan / infection numericals are NOT carried as findings (self-check L68). This is the required negative-finding discipline.

(b) **Single-source-language concentration caveat — SATISFIED.** The section's framing (L5) treats originator-country / single-group / manufacturer-linked papers as a concentration-of-evidence hazard counted as ONE source-lineage, not N replications, carrying a `[non-English-literature]` caveat. Per-finding: E1 (Russian — originator-institute / Cochrane-documented Cerebrolysin sponsorship bias); E2 (Chinese — author-admitted China-concentration, China-exclusive Rhodiola species at lowest CONSORT scores); E3 correctly distinguishes a TIER hazard from a concentration hazard and notes no concentration hazard applies there. Khavinson flagged as the single largest unresolved concentration risk. Self-check L69 catalogs all concentration caveats raised.

---

## Verdict

```
verdict: PASS
```

Both folded layers satisfy their §4.3 checks. Section D (prescribing-practice) documents an explicit "no admissible compounding data sheet located" with a searched-blocked list (the well-reasoned negative path) and renders all practitioner doses as convention-not-trial-validated with Tier-1 contradictions given primacy. Section E (non-English) surveys 3 of 5 language families (Russian, Chinese, originator-country) with explicit verified-primary findings plus a disciplined "no admissible primaries located" note for the Khavinson corpus, and surfaces single-source-language concentration as both a section-level framing and per-finding caveats.

Reference-landscape adaptation noted and accepted: Hard Rule 3 layers were dispatched as Sections D/E (judge-passed at deep-99) and folded into the substrate rather than written as separate vault compound-entry files; both retain their own `## Bibliography` + `## Self-check`, satisfying Check 1.
