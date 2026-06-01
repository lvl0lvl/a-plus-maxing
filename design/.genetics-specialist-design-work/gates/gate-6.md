# Gate 6 — CRITIQUE (Phase-6, aplus-research deep mode)

Target: `design/.genetics-specialist-design-work/domain-research.md`
Critique agent: independent adversarial reviewer (did NOT author the synthesis).
Corpus cross-checked: sections/section-A.md, section-B.md, section-C.md, section-D.md.
Date: 2026-06-01.

## Summary

This is a strong, evidence-disciplined synthesis. All four safety floors (DTC-raw≠diagnostic; risk-variant≠disease→counselor+MD; PGx-informs-not-authorizes; genetic exceptionalism/privacy) are present, stated accurately, and traceable to cited primary/consensus sources; every author-year token in the body resolves to a bibliography entry; and the deep-mode body is materially complete relative to the section corpus. The findings below are improvement suggestions (major/minor) — no missing safety floor, no determinism overreach that misleads, no fabricated load-bearing citation, and no material logical inconsistency. The two genuine numeric/tag discrepancies against the corpus (Ryu N; Tandy-Connor tag) are disclosed and reconciled in the draft's own Limitations and Methodology, so they are not silent contradictions.

## Findings

### missing-perspective

1. **major — Several domain-relevant angles are absent and not even named as out-of-scope.** The report does not address: carrier screening / reproductive (recessive carrier status, partner testing); the somatic-vs-germline distinction (a recurring real-world confusion for any agent that may receive tumor-panel data); mosaicism beyond the single G6PD aside; mitochondrial / non-Mendelian inheritance; pediatric/prenatal genetics and the predictive-testing-of-minors norm; VUS reclassification over time (the report defines VUS but never states that VUS status is dynamic and re-contact/re-query is a live obligation — directly relevant to the agent's `vault/dna/` curation role); and pharmacovigilance / post-market signal evolution for PGx. Polygenic embryo screening is also untouched. The Limitations section claims "reference, not exhaustive" but does not enumerate which whole subdomains were excluded, so a design-doc drafter cannot tell deliberate scope-narrowing from oversight.
   - **required_fix:** Add an explicit "Out-of-scope subdomains (deliberate)" list to Limitations naming carrier/reproductive screening, somatic-vs-germline, mosaicism, mitochondrial inheritance, prenatal/pediatric testing, polygenic embryo screening, and pharmacovigilance — and add one sentence to Finding 1 or the Limitations stating that VUS classifications are dynamic and the agent must re-query rather than cache a stale tier (load-bearing for the vault-owner role).

2. **minor — The `vault/dna/` ownership handoff from labs/other specialists is asserted but its mechanics are thin.** The Synthesis (line 125) and R8/R11 establish the agent as owner/writer of `vault/dna/` and say "DNA was read by six specialists, written by none," and R11 says "read `vault/dna/raw/` before writing any variant page." But the report does not describe the provenance-tagging contract the agent must honor when it writes a page that downstream specialists will read (e.g., must every variant page carry assay-provenance + confirmation-status + ancestry-denominator fields). This is the single most design-load-bearing handoff and is underspecified relative to its prominence.
   - **required_fix:** Add one recommendation (or expand R8) specifying the minimum metadata a `vault/dna/` page must carry so the provenance/ancestry/confirmation discipline survives into downstream reads — i.e., make the four floors structurally enforced in the artifact, not only in agent prose.

### unexamined-counter-evidence

3. **minor — The PRS finding presents only the pessimistic portability framing without the active counter-development.** Finding 3 and the F3 evidence note correctly carry Martin 2019's portability-decay and equity warning, but omit that multi-ancestry GWAS and portability-correction methods are an active, partly-successful research front (the field has moved since 2019). For a goal-agnostic reference meant to age, stating only "poor portability, treat as far less reliable" risks the agent over-discounting a valid PRS for a non-European individual when better-calibrated multi-ancestry scores exist.
   - **required_fix:** Add a half-sentence acknowledging that multi-ancestry PRS development is an active mitigation, while keeping the operative rule (qualify by discovery-ancestry composition) intact.

### alternative-explanation

4. **minor — "PGx informs, never authorizes" leans on phenoconversion as "the technical proof"; that framing slightly overstates.** Phenoconversion is one strong technical reason, but the floor stands independently on scope-of-practice and the "one input among many" argument even in the absence of phenoconversion. Finding 9's subtitle "(phenoconversion is the technical proof)" could be read as implying the floor would weaken if phenoconversion were absent. The body text (line 92) actually states both reasons correctly; only the heading over-attributes.
   - **required_fix:** Soften the Finding 9 heading to "(phenoconversion is a key technical reason)" or similar, so the floor is not rhetorically made contingent on a single mechanism.

### bias

5. **minor — Mild U.S./Western regulatory centricity, correctly the dominant frame but not flagged as a frame.** GINA (U.S.), FDA, ACMG, CPIC, NSGC are all U.S./Western bodies; the privacy/insurance-gap analysis is U.S.-specific (GINA gaps, HIPAA). For a goal-agnostic library this is the right primary frame, but the report nowhere states that the data-ethics/insurance analysis is jurisdiction-specific and does not generalize (e.g., other jurisdictions have moratoria on life-insurance genetic use). A design-doc drafter could encode "state GINA protections" as universal.
   - **required_fix:** Add one clause to R15 or §4 noting the GINA/HIPAA analysis is U.S.-jurisdiction-specific and the residual-exposure framing must be localized.

### logical-inconsistency

6. **minor — Disclosed and reconciled, recorded for completeness, not a halt.** (a) Ryu et al. 2024 N is **937,939** in the draft body (lines 104, 167) vs **938,355** in section-D line 27; (b) Tandy-Connor 2018 type-tag is **open_label** in the draft vs **cohort** in section-D ([13, cohort], line 55/96). Both are real divergences from the corpus — but the draft explicitly surfaces and explains each (Limitations item 3, line 185; Methodology gate-4.25/4.75 notes, lines 287–288), correcting to the source-accurate values. The load-bearing ORs (5.24 / 4.53) are identical either way. This is transparent reconciliation, not a silent contradiction.
   - **required_fix:** None required. Optionally, push the section-D corrections back into section-D.md so the corpus and synthesis agree at rest (housekeeping only).

### citation-incomplete

7. **major — The headline "4.9-fold lower in individuals of African ancestry" (Martin 2019) is a body/figure-level figure, not abstract-supported, and is stated as if it were the paper's headline number.** I verified PMID 30926966: the abstract states PRS are "several times more accurate in individuals of European ancestry than other ancestries" and does NOT give the 4.9-fold figure (it lives in the paper's figures/results). The number is not fabricated and is widely attributed to this paper, but Finding 3 and the F3 evidence note present it as a clean quantified claim without signaling it is a within-paper analytic figure, and section A had already hedged it as "on average, roughly 4.9-fold." Load-bearing because it is the only quantification of the ancestry-portability floor.
   - **required_fix:** Either soften to "on average roughly 4.9-fold (paper's analysis; abstract states 'several times')" or attach the qualifier already present in section A. Confirm the figure against the paper body before it is encoded as a hard number in the agent.

8. **minor — One load-bearing regulatory URL does not resolve programmatically.** The FDA March-2018 press-announcement URL (bibliography #10, line 227) returned HTTP 404 on fetch. The quoted controls ("three out of more than 1,000," "negative result does not rule out," "should not be used as a substitute for seeing your doctor") are corroborated by the independently-real Kilbride et al. 2019 analysis (PMID 31173557) and the DEN170046 De Novo citation, so the underlying facts are sound — but the primary URL itself is stale/blocked.
   - **required_fix:** Replace or supplement bibliography #10 with the stable De Novo decision summary (DEN170046, already cited as #42 in the consolidated list) or a permalink, so the FDA quotations have a resolving anchor.

9. **minor — "more than 1,000 known BRCA mutations" appears as a quoted FDA figure but the corpus also says ">1,000 known pathogenic" loosely.** Not a fabrication (consistent across A, D, and the FDA framing), but the report mixes "1,000 known BRCA mutations" (FDA quote) and ">1,000 known pathogenic BRCA variants" (section D line 13/167) — "mutations" vs "pathogenic variants" are not interchangeable. Minor precision.
   - **required_fix:** Use the FDA's verbatim wording inside quotes and the precise "pathogenic variants" outside quotes; do not blend.

### balance-issue

10. **minor — Finding 11 under-weights ALDH2 relative to the section-C evidence.** The body Finding 11 reduces ALDH2 to "actionable (flushing + esophageal-cancer risk in drinkers)" and drops the concrete, encodable figures present in section C (~540 million carriers, esophageal-SCC OR 3.7–18.1, two-question flushing survey ~90% sensitivity/~88% specificity). The detailed evidence note (line 163) restores them, so the data are not lost — but the Finding tier (which design-doc drafters read first) is thinner than the HLA Finding 10, creating an actionability-asymmetry in the reader's first pass. Given ALDH2 is the one nutrigenomic variant the report calls genuinely actionable, the headline finding should carry at least the OR range.
   - **required_fix:** Add the ALDH2 OR range and the flushing-survey sensitivity to Finding 11 so the "actionable" claim is quantified at the finding tier, matching the rigor applied to HLA.

### objectivity-issue

11. **major — The document's own front matter pre-declares the Phase-6/Phase-7 outcome before this critique has run.** Front matter line 8 reads `status: synthesized (Phase 5) → critiqued (Phase 6) → refined (Phase 7)` and line 10 lists `gates 2.75 / 3.5 / 4.25 / 4.75 / 6 attested`; the Methodology (lines 290–291, 305) and "Phase 7 Refinement Log" (lines 309–312) likewise pre-stage gate-6 as attested/refined. This is a process-hygiene/objectivity problem: the artifact asserts a gate verdict and a refinement pass it has not yet received. It directly maps to the project's PF-S3-01 anti-pattern ("the gate JSON is just bookkeeping" / pre-declaring outcomes). It does not affect the scientific content, hence not a halt — but it must be corrected before the document is treated as final.
   - **required_fix:** Revert `status` to `synthesized (Phase 5) → critiqued (Phase 6)` (no "refined" claim until Phase 7 actually runs), drop "6" from the "attested" gate list in front matter until gate-6.json is attested, and leave the Refinement Log empty/"pending" until Phase-7 edits land. The gate-6 verdict must come from this file, not be pre-asserted by the draft.

12. **minor — A handful of mild advocacy/certainty phrasings.** "the highest safety weight" (F6 heading), "the most safety-critical subtopic," "non-negotiable" (F9) are defensible given the evidence, but cluster as emphatic framing. Acceptable for a safety-floor document; flagged only so Phase-7 keeps them tied to evidence rather than rhetoric.
   - **required_fix:** None required; retain if each remains anchored to the cited PPV/false-positive data.

## Citation spot-check

Verified ≥3 load-bearing sources against PubMed/NCBI:

1. **Weedon MN et al., BMJ 2021 (PMID 33589468)** — VERIFIED, supports claim. Title, journal, year exact. Abstract confirms 49,908 UK Biobank participants; BRCA PPV **4.2%** (sensitivity 34.6%, specificity 98.3%); very-rare-variant PPV **16%** (of 4,757 heterozygous genotypes). The draft's "of 889 chip-detected pathogenic BRCA calls, only 37 were true positives" is a paper-body raw count (consistent with 4.2% PPV; not in the abstract — body-level, acceptable).

2. **Tandy-Connor S et al., Genet Med 2018 (PMID 29565420)** — VERIFIED, supports claim. Title/journal/year exact. Abstract confirms retrospective review of **49 patient samples** and "**40% of variants** ... were false positives," with some "increased risk" calls reclassified benign. Confirms both the 40% figure AND the `open_label`/case-series tagging the draft adopted (section-D's `cohort` tag was the wrong one; the draft corrected it).

3. **Martin AR et al., Nat Genet 2019 (PMID 30926966)** — VERIFIED exists, PARTIALLY supports claim as stated. Title/journal/year exact; abstract supports the qualitative portability/equity claim ("several times more accurate in individuals of European ancestry"). The specific **"4.9-fold lower in African ancestry"** is NOT in the abstract — it is a within-paper figure. Real number, but the draft presents it more crisply than the abstract warrants (see Finding 7).

Additional check: **FDA 2018 press-announcement URL (bib #10)** — does NOT resolve (HTTP 404 on fetch). Underlying facts corroborated by the real Kilbride 2019 (PMID 31173557) and DEN170046; URL is stale/blocked (see Finding 8).

## Verdict

```
verdict: PASS
halt_reasons: []
```

Rationale: All four safety floors are present, accurate, and complete; no determinism overreach that misleads a reader; no fabricated or unresolvable load-bearing citation (the FDA URL is stale but the fact is independently corroborated, and the Martin 4.9-fold is a real within-paper figure, not an invention); and the only numeric/tag divergences from the corpus are explicitly disclosed and reconciled in the draft itself. The findings are improvement suggestions for Phase-7 refine. The two `major` items most worth addressing in refine are Finding 11 (front-matter pre-declares the gate-6/Phase-7 outcome — fix before final) and Finding 7 (qualify the Martin 4.9-fold as a paper-body figure).
