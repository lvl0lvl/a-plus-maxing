## Verdict

verdict: PASS

```json
{
  "phase": "6",
  "verdict": "PASS",
  "iterations": 1,
  "critique_agent_id": "critique-nasa-deep",
  "draft_path": "vault/library/peptides/n-acetyl-selank-amidate/research-report.md",
  "findings": [
    {
      "category": "citation-incomplete",
      "severity": "minor",
      "description": "Section B source sections tag refs [5] and [6] (Volkova 2016, Filatova 2017) as tier-1, but the research report's bibliography correctly flags them as lower-trust open-access outlets (tier-2 with flag). This inconsistency between the section-level bibliography and the final report is cosmetic — the final report's tiering and flagging is accurate and more cautious. No action needed for the wiki entry; but the discrepancy exists."
    },
    {
      "category": "missing-perspective",
      "severity": "minor",
      "description": "The report does not explicitly note that the psychostimulant/activating profile documented in Zozulia 2008 could be a desirable feature for some off-label healthy users seeking cognitive enhancement (not only framing it as a risk). The population-direction reversal framing is accurate but presents only the adverse-direction reading; a complete balance note would acknowledge the debate. This is a minor balance issue, not a factual error — the primary direction of concern for safety purposes is correctly stated."
    },
    {
      "category": "balance-issue",
      "severity": "minor",
      "description": "The Siuniakov 2015 'rct' tag is retained from the source sections despite the full report explicitly acknowledging 'no described double-blinding.' The tag is qualified in the bibliography, but the evidence-tier summary table lists it as 'Comparator RCT' which risks over-stating blinding. The main text and the final table caption adequately hedge, so this is minor, but a reader skimming the tier table could see 'rct' and miss the qualification."
    }
  ],
  "additional_retrievals": [],
  "halt_reasons": []
}
```

---

## Detailed Prose Assessment

### 1. Analog-Evidence Absence — Load-Bearing and UNMISSABLE

The report passes this probe decisively. The zero-analog-specific-evidence finding is stated in:

- The metadata block (evidence_tier field, first sentence)
- Six-fact Summary, Fact One (explicit, opening)
- Section 1.3 ("Critical finding" paragraph in bold)
- Section 3.1 framing header ("Everything Here Is Parent Evidence")
- Section 3.6 evidence-tier summary table (last row: "No evidence exists")
- Section 6.2 entire subsection devoted to "analog evidence absence"
- Section 8 "Honest Bottom Line" Problem 1
- Both vendor admissions quoted inline ([26], [27])

There is no point in the report where a reader could mistake Selank evidence for analog evidence. The distinction is structurally enforced throughout. The framing in Section 3.1 ("No Selank finding in this section is attributed to the analog as demonstrated — it is extrapolated at best, and possibly disrupted by the N-terminal acetylation at the receptor-binding epitope level") is the correct and sufficient caveat placed precisely where the parent evidence is reviewed.

No drift into treating Selank's evidence as the analog's was found.

### 2. Binding-Epitope Uncertainty — Prominent and Not Buried

The epitope concern is surfaced in:

- Section 1.3 under the explicit bold subheader "The binding-epitope uncertainty — the analog's most important unresolved pharmacological question" (6 paragraphs of dedicated treatment)
- Summary, Fact Four (full paragraph, standalone)
- risk_tier metadata (explicit mention: "N-terminal acetylation may disrupt the Tuftsin receptor-binding epitope")
- Section 8 Problem 3 ("the analog may disrupt the parent's mechanism")

The structural concern is grounded in Fridkin and Gottlieb [2] — a legitimate tier-1 primary structure-function reference — and the inference is correctly stated as a first-principle concern not refuted by any published binding study, not a confirmed disruption. This is accurate epistemic positioning. The section also correctly cites the Semax N-terminal acetylation study ([15]) as a structural parallel without overstating its applicability.

The epitope concern is front-facing, not buried.

### 3. Single-Lineage Concentration — Honest and Specific

Stated explicitly and quantitatively:

- Summary Fact Two (opening bullet, specific percentage: ~87–93%, mechanism cited)
- Section 4.3 (full institutional affiliation table, per-group breakdown, calculation shown)
- Section 6.1 (concentrated treatment of what the concentration means epistemically)
- Bibliography: inventor co-authorship flagged on [5] ("All seven authors from IMG RAS"), [6] ("IMG RAS + Blokhin"), [19] ("IMG RAS; used for institutional lineage documentation")

The report does not soften the conflict-of-interest framing. Myasoedov is named by role (inventor, patent holder, clinical trial author, mechanism reviewer) at each point where this matters. The "regulatory peptide paradigm not Western-accepted" point is stated in Section 4.3: "The 'regulatory peptide' paradigm as a scientific framework... has not been adopted into any Western drug development program or clinical guideline."

Passes.

### 4. Selank Parent Evidence Quality — Honestly Tiered

The three trials are correctly characterized throughout:

- Zozulia 2008: n=62, "randomized two-arm comparator" but "no placebo arm," "limited blinding description," inventor co-authorship (Miasoedov listed 13th of 14 authors), Russian-language, "tier-2 at best" — the "tier-2 at best" language is appropriate given it is characterized as `rct` with explicit qualification, not elevated to tier-1
- Medvedev 2014: n=60, open-label comparator, "open-label design means expectation bias cannot be excluded," no blinding described — correctly classified `open_label` tier-2
- Siuniakov 2015: n=70, classified `rct` in the bibliography but with the caveat "same limitations as above: small n, Russian language, Russian institution, no described double-blinding" in the Section 3.6 table — adequately hedged

The EEG study (Syunyakov 2012) is accurately noted as a conference abstract, n=20, open-label, no placebo arm. The PMID-missing Uchakina study is flagged "n: unconfirmed."

One minor finding: the Section 3.6 evidence table lists Siuniakov 2015 as a "Comparator RCT" in the type column. The word "RCT" may overstate the study since blinding is not confirmed; "Comparator trial (limited blinding)" would be more accurate. This is a minor balance issue — the body text and bibliography both qualify it. Flagged as minor, not critical.

No inflation of the Selank corpus was found.

### 5. WADA Framing — Doubly Hedged, Intact

Section 5.6 (WADA) and the corresponding Section D.4 in the source sections apply the two-layer hedge precisely:

- Layer 1: The claim comes from an MDPI review ([21], lower-trust tier-2), citing reference 85 in that article which was not directly accessible; the primary WADA Prohibited List document was not independently verified in this research run — stated explicitly
- Layer 2: S2 category-fit is "categorically non-obvious" for a GABAergic anxiolytic; S0 ("Non-Approved Substances") is identified as the more clearly applicable category, with reasoning

The phrasing "doubly hedged" is accurate: the prohibition itself is unconfirmed against primary source, AND the category assignment is contested even if prohibition were confirmed. The athlete guidance (NADO/GlobalDRO verification) is explicit.

No overstating of WADA status found.

### 6. Alternative Explanations and Objectivity

The report does not read as an endorsement. Affirmative-sounding language is consistently coupled with the limitation:

- "The theoretical pharmacological rationale is coherent" — immediately followed by "but the compound being purchased is not the studied compound, its pharmacological equivalence is assumed not demonstrated..." (Section 8)
- "mechanistically plausible" — consistently paired with "not established" or "not replicated"
- "the modification logic is standard medicinal chemistry" — immediately qualified by seven conditions of use that are "not minor qualifications"

Alternative explanations for positive clinical findings are explicitly offered: expectation bias and regression-to-mean are named as equally plausible to "neuroadaptation" in the Medvedev 2014 one-week persistence finding (Section 3.3, and echoed in Section 5.2).

The grey-market reality is clearly stated in Section 6.3 and in the route-specific cautions. The vendor-conflation dynamic (Selank evidence transferred to analog without basis) is named as a structural problem in Section 6.3 under "Identity conflation."

Passes objectivity and alternative-explanation probes.

### 7. Minor Finding: Tier Inconsistency Across Sections and Report

Source sections B and E tag Volkova 2016 and Filatova 2017 as tier-1 in their bibliographies, while the final report correctly retags them as tier-2 with a lower-trust flag. This inconsistency is harmless to the final entry (the report's tiering is more cautious and correct) but is worth noting as an editorial residual. No downstream downstream claim in the report rests on these sources being tier-1; the argument would hold whether they are tier-1 or tier-2.

### 8. No Targeted Retrievals Needed

The probes were resolvable by reading the report and source sections. No counter-claim emerged requiring empirical retrieval. Zero additional retrievals dispatched.

---

## Summary

**Verdict: PASS.** The research report is structurally honest throughout the eight-category red-team: the analog-evidence absence is unmissable and load-bearing at every level of the document, the binding-epitope uncertainty is prominently surfaced (not buried), the ~87–93% single-lineage concentration is stated quantitatively with inventor co-authorship named at each relevant point, the Selank parent evidence is correctly tiered as tier-2-at-best with all material limitations stated, the WADA framing carries the correct double-layer hedge, and the document does not read as an endorsement. Three minor findings logged (a tier-label inconsistency between source sections and final report for two Frontiers papers; a one-sided framing of the psychostimulant effect as purely adverse rather than use-case-dependent; and the Siuniakov 2015 "Comparator RCT" label in the evidence table slightly overstating blinding), none rising to major or critical.
