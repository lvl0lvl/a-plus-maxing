# Gate 6 — CRITIQUE (red-team), AOD-9604 research report

**Agent:** critique-aod-i1 (did NOT author the draft)
**Draft:** vault/library/peptides/aod-9604/research-report.md (505 lines)
**Corpus consulted:** /tmp/aplus-research/aod-9604/sections/section-A…F.md

## Prose critique

I adversarially reviewed the synthesized draft against the seven red-team axes. The draft is, on the load-bearing honesty axes, strong — and in several places notably disciplined. Findings below are genuine defects only; none rise to major/critical.

**1. FAILED-efficacy discipline (the #1 axis) — PASS.** The report does not let preclinical lipolysis or marketing read as proven human fat loss. The phrase "no proven human fat-loss efficacy" appears in the read-this-first banner, the TL;DR, the §2 BLUF, §2.5 verdict, and §7.1 — and the §503A/safety sections repeatedly restate "safety is not efficacy." The failed 536-patient, 24-week Phase-2b oral RCT is the headline of §2 and is carried throughout; preclinical lipolysis is consistently species-annotated (Zucker rats / ob/ob mice / adipocytes / in-vitro) and explicitly labeled "clearly NOT human fat loss" (§2.3). The one "positive" human signal (Herd 2005, 1 mg inverse-dose) is correctly demoted to a non-PubMed-indexed conference abstract that the definitive trial did not confirm. The sections (section-B) carry the same "no proven human fat-loss efficacy" language — no leak. Clean.

**2. Mechanism — PASS.** The fragment identity (Tyr-hGH(177-191) / hGH(176-191), 16-residue, disulphide-cyclized) is correct and well-sourced. The "lipolysis WITHOUT GH-receptor / IGF-1" claim is presented as VERIFIED at the receptor-binding / IGF-1 / glucose-biomarker level, with an explicit honest boundary that "verified" = absence-of-GH-axis-liability, NOT evidence of fat loss (§1.2 closing parenthetical, §1.6, §7.1). §1.5 cleanly distinguishes AOD-9604 from GH replacement and GH secretagogues (which deliberately RAISE GH/IGF-1) — exactly the requested distinction. The β3-AR nuance (permissive/downstream, NOT the direct target; lost in chronic KO but preserved acutely) is handled with care, and the report quotes the sponsor review's own candor that "the mechanism of action is not understood."

**3. Paradigm-OA conflation — PASS (correctly EXCLUDED).** Every Paradigm mention (banner, TL;DR, §3.2 "conflation FLAGGED — do NOT propagate," §3.4, §6 cross-ref, Provenance note) identifies the "Paradigm Phase-II knee-OA" program as **pentosan polysulfate (iPPS/Zilosul), a different molecule, NOT AOD-9604**, and explicitly excludes it. The report nowhere credits the Paradigm Phase-II/III data to AOD-9604. OA claims are confined to preclinical-only (one Kwon/Park rabbit study + the sponsor patent). The unverifiable 2020 "Joint Dis Relat Surg" human-OA mention is correctly OMITTED per verify-or-omit. Exemplary.

**4. Safety honesty — PASS.** Well-tolerated / GH-axis-sparing (no IGF-1 rise, no glucose impairment, non-immunogenic AS THE CHARACTERIZED CLINICAL MATERIAL) is asserted but immediately bounded by: short-term only (max 24 wk, no Phase-III safety DB), NO published human SC-route data (clinical program was oral/IV; gray-market SC route has zero human exposure), and the FDA injectable immunogenicity/aggregation/impurity concern for uncharacterized product (§5.4, §5.7, §6.2). The framing "unapproved, uncharacterized injectable, no long-term data — NOT known to be harmful" is honest and consistent.

**5. Regulatory — PASS.** Never approved as a drug anywhere (verified across [13][14][15][16]). Self-affirmed GRAS is explicitly stated to be NOT FDA approval and NOT a lawful US dietary ingredient (DSHEA drug-exclusion), without overstatement. WADA PROHIBITED is anchored: S0 catch-all confirmed 2013 + S2 GH-fragment scope, Essendon/CAS saga correctly nuanced (the CAS verdict turned on thymosin beta-4; AOD-9604 was never directly charged for pre-April-2013 use). AOD-9604 is correctly stated as NOT among the April-2026 removed-12 peptides; it appears only via the Evexias/Farmakeio Category-2 litigation. Not lawfully compoundable (never Category-1).

**6. Citation integrity (the lesson) — PASS (clean).** Mechanical verification:
- Inline body `[n]` tokens (unique set) === Bibliography entry set, EXACTLY. 32 tokens each side, identical.
- **Zero dangling** (every inline token has a definition), **zero missing** (every definition is cited).
- **Zero collisions:** each bibliography number appears exactly once as a definition.
- `[6]` is an intentional gap (not used inline, not defined) — acceptable, and the unified-renumber discipline is disclosed in the Provenance note.
- The two deliberate same-paper dual-numbers are correctly disclosed and non-ambiguous: [2]/[7] = Heffernan *Int J Obes* (PMID 11673763), split by claim (receptor vs fat-oxidation); [5]/[12] = Moré/Kenley 2014 review (DOI 10.14740/jem213w), split by claim (mechanism/PK vs the FAILED Phase-2b). The [1]/[2]/[7] PMID-to-number mapping is internally consistent across §1.2, §1.3, §2.3, and the §4 concentration table (no inverted attribution).
- **Spot-checks:** the failed Phase-2b → [11] (sponsor OPTIONS disclosure) + [12] (peer-reviewed sponsor-affiliated review reporting the null) — correct sourcing. Kwon & Park rabbit OA → PMID **26275694** at [10] — correct, matches in body (§3.2), the §4 table (P5), and the bibliography.

**7. No Wikipedia / concentration / tier / contradictions — PASS.** "Wikipedia" appears only in the affirmative "No Wikipedia used" disclosure — no Wikipedia citation. The ~100% single-lineage concentration (Monash/Ng → Metabolic Pharmaceuticals; 5/5 enumerated primaries; Kwon/Park independent authors but sponsor-supplied material) is surfaced first-class in §4 with the ≥70% FLAG raised. Tier C / risk experimental is well-defended in §7 (failed pivotal human efficacy + preclinical-only + single-lineage; held at C rather than lower by the genuinely verified mechanistic differentiator and substantial clean human safety dataset).

### Minor defects (do not block)

- **(minor, logical-inconsistency) §503A Category-2 timeline tension.** §6.3 frames AOD-9604's status as "previously held in Category 2 (now contested in court)," reading as if it currently sits in Category 2, whereas §8.2 states it was "Removed from Category 2 (~27 Sep 2024) … because the nominator withdrew the nomination." The two are reconcilable (removed-by-withdrawal, then the Category-2 framework litigated) and both reach the identical operative conclusion — "never Category-1, not lawfully compoundable" — so the load-bearing claim is sound; only the present-tense status phrasing is loose. Tightening §6.3 to say "removed-by-withdrawal, never Category-1, now litigated" would remove the ambiguity.
- **(minor, citation-incomplete) Patent priority/grant gloss.** §3.1 / [9] state US 10,111,933 B2 "priority 2011 / granted 2018" as a parenthetical; this is provenance-level and not load-bearing for any efficacy claim, but the priority year is asserted without a distinct supporting locator beyond the patent itself. Acceptable as patent-self-disclosure; flag only for completeness.

Neither minor finding touches an efficacy, safety, mechanism, regulatory-conclusion, or citation-resolution claim. No major or critical defects found.

## Verdict
verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-aod-i1","draft_path":"vault/library/peptides/aod-9604/research-report.md","findings":[{"category":"logical-inconsistency","severity":"minor","description":"§503A Category-2 timeline: §6.3 reads as if AOD-9604 currently sits in Category 2 ('previously held … now contested'), while §8.2 says it was removed from Category 2 ~27 Sep 2024 by nominator withdrawal. Reconcilable and both reach the identical correct operative conclusion (never Category-1, not lawfully compoundable); only the present-tense status phrasing in §6.3 is loose."},{"category":"citation-incomplete","severity":"minor","description":"§3.1/[9] assert US Patent 10,111,933 B2 'priority 2011 / granted 2018' as provenance gloss without a locator distinct from the patent itself; non-load-bearing (no efficacy claim rides on it), acceptable as patent self-disclosure, flagged for completeness only."}],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
