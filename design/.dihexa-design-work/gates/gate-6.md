---
gate: "6"
agent: critique-dihexa-deep
draft: vault/library/peptides/dihexa/research-report.md
date: 2026-06-22
---

## Verdict

verdict: PASS

```json
{
  "phase": "6",
  "verdict": "PASS",
  "iterations": 1,
  "critique_agent_id": "critique-dihexa-deep",
  "draft_path": "vault/library/peptides/dihexa/research-report.md",
  "findings": [
    {
      "category": "citation-incomplete",
      "severity": "minor",
      "description": "Section C source section notes the Athira securities class action as '~$10 million' but the final report (§5.2) correctly hedges this as '~$10 million securities class action was also filed' without citing a primary source — consistent with the Retraction Watch tier-3 sourcing pattern used throughout. However, the source section C.3 also quotes '$10 million to settle securities fraud lawsuits' (not merely filed), which overstates the settlement figure versus the research report's more accurate 'filed' phrasing. The discrepancy between source-section language and final report language is resolved correctly in the final report, but neither document cites a primary court record for the securities action amount. Minor because the final report's phrasing ('also filed') is appropriately hedged and the $4M DOJ settlement is the load-bearing financial fact, not the securities suit."
    },
    {
      "category": "balance-issue",
      "severity": "minor",
      "description": "Section 3.2a ('Mechanistic Plausibility Without the Retracted Evidence') correctly distinguishes what the retractions destroy versus what they leave uncertain. However, this section could be read by a motivated reader as partially rehabilitating the HGF/c-Met mechanism via the observation that 'it is not impossible that Dihexa activates PI3K/AKT via an upstream receptor interaction that includes c-Met.' While the caveat is epistemically honest, the section does not equally foreground that this speculation has zero non-retracted experimental support and that the Sun 2021 paper explicitly does not test or confirm c-Met involvement. The balance is borderline: the intellectually honest framing at 3.2a's close ('the proposed HGF/c-Met mechanism is plausible in biological terms, unconfirmed by any trustworthy primary evidence') is correct, but the preceding speculative paragraph could be tightened to prevent it from doing soft rehabilitative work. Minor — the closing sentence of 3.2a is accurate and the overall report is strongly counterweighted against mechanism overclaiming."
    }
  ],
  "additional_retrievals": [],
  "halt_reasons": []
}
```

---

## Prose Detail

### 1. Retraction Handling — UNMISSABLE and accurate throughout

The retraction handling is exemplary. The foundational failure (Benoist 2014 RETRACTED, Kawas 2012 RETRACTED, McCoy 2013 under EoC) is declared in the **metadata block** — before the reader reaches the body — and then repeated with full specificity in the Summary (Six Load-Bearing Facts), §1.3, §2.3, §2.2, §4.1, §5.1, §5.2, and §6. There is no section in the report where the HGF/c-Met mechanism is presented as established. The potency claim ("100 million times more potent than BDNF") is explicitly traced to the now-retracted Benoist paper in §1.4, in the metadata, and in the Summary. A reader who skimmed only the metadata block and Summary would emerge with the correct understanding. PASS on this category.

### 2. Zero Human Data + Fosgonimeton Distinction — correctly handled

Zero human data is stated explicitly in the metadata block (risk_tier), Summary (Fact Four), §2.8, §4.1, and §6. The fosgonimeton distinction is handled with unusual care: the report correctly notes (a) it is a *structurally distinct* compound, (b) administered subcutaneously not orally, (c) with its own pharmacokinetics, (d) which failed every clinical endpoint. Critically, the report is careful NOT to use fosgonimeton's failures to condemn Dihexa via guilt-by-association, and NOT to use fosgonimeton's Phase 1 safety findings (no serious adverse events, n=88) as credit for Dihexa's safety — see §2.8 and §5.4. The §5.4 treatment of what the fosgonimeton failures "do and do not mean" is one of the most balanced passages in the report. PASS on this category.

### 3. c-Met Oncogenic Tension — correctly framed as theoretical, open, load-bearing

Section 3 handles this well. The concern is introduced in the metadata risk_tier, in Summary Fact Three, and developed at length in §3.1–3.2. The framing throughout is:
- The theoretical risk is **genuine and mechanistically grounded** (HGF/c-Met is an established oncogenic axis with FDA-approved inhibitors as pharmacological proof)
- It is **NOT a demonstrated Dihexa carcinogenicity** (no carcinogenicity study exists for Dihexa; the preclinical studies ran 4–12 weeks, structurally incapable of detecting tumor promotion)
- **Absence ≠ safety** is stated explicitly ("absence of a carcinogenicity study is the normal state for an academic compound that never reached IND development; it does not imply the risk was assessed and found absent")
- The **c-Met inhibitor contraindication** (capmatinib, tepotinib) is named explicitly in §3.2 and §4.2 as an absolute contraindication

The report does not overclaim a demonstrated carcinogenicity risk for Dihexa and does not dismiss the concern. PASS on this category.

### 4. Independent Replication Verdict — honest and accurate

The report accurately documents:
- Sun 2021: independent group, PI3K/AKT not HGF/c-Met, no c-Met data, lower-trust open-access journal
- Wells 2024: independent group, null result in HD model
- Ho & Nation 2018: pre-retraction systematic review, does not adjudicate IRAP vs HGF/c-Met

The critical distinction — that Sun 2021 found PI3K/AKT and *explicitly not* HGF/c-Met — is called out prominently in both §2.5 and the Summary. The report correctly notes that Sun 2021 is "consistent with multiple mechanistic accounts" without allowing it to vindicate the retracted mechanism. The Wells 2024 null result is reported fairly without overextending it to prove Dihexa cannot work in any model. PASS on this category.

### 5. Concentration and Integrity Story — factual and calibrated

The §5.1 concentration table is accurate (~67% WSU/Harding-Wright, consistent with the source section E.1 enumeration). The Kawas/WSU/DOJ/Athira story is documented factually in §5.2 with the key facts attributed to Retraction Watch (tier-3) and labeled as such. The one detail worth noting: the source section C.3 characterizes the securities class action as resulting in a $10 million settlement ("Athira later paid $10 million to settle securities fraud lawsuits"), whereas the final report correctly uses "~$10 million securities class action was also filed" — the latter is more accurate, as the filed amount is not the same as a confirmed settlement. The final report's language is correct; the source section language was a subtle overstatement that was not carried forward, which is the right outcome.

The Kawas image-manipulation facts are accurately reported. The $4M DOJ settlement (January 2025) is correctly distinguished from the securities class action.

**Minor finding flagged:** neither the source sections nor the final report cites a primary court record for the securities action; the entire integrity story rests on Retraction Watch (tier-3). This is disclosed honestly in the bibliography (source [18]: "tag: anecdote_aggregate — tier: 3"), which is the correct treatment given the sourcing reality. However, a reader who wants to verify the securities action cannot do so from the citations provided. This is a minor citation-incomplete finding — not a fabrication or misrepresentation, but a sourcing gap in a secondary fact.

### 6. Balance / Objectivity — neither a sales pitch nor a hit piece

The report avoids both failure modes. It:
- Acknowledges the genuine preclinical signal (behavioral rescue in multiple rodent models, independent cognitive-rescue replication in Sun 2021) without inflating it
- Notes the IRAP/AT4 hypothesis as a parallel mechanistic candidate with cleaner integrity provenance
- Does not suppress the Sun 2021 finding because it might seem to rehabilitate Dihexa
- Does not treat the Wells 2024 null result as proof that Dihexa cannot work in any context
- Explicitly notes that fosgonimeton's clinical failures "do not prove that HGF/c-Met potentiation cannot work in any population" (§5.4)

The overall tone is accurately severe about the integrity situation — which is appropriate given that this is the most integrity-compromised entry in the sweep — but is not punitive beyond what the evidence supports.

**Minor balance finding flagged:** §3.2a contains a speculative passage noting that Sun 2021's PI3K/AKT finding is "not impossible" to reconcile with upstream c-Met involvement. This is epistemically honest but runs a small risk of doing soft rehabilitative work for the retracted mechanism. The closing sentence of §3.2a ("the proposed HGF/c-Met mechanism is plausible in biological terms, unconfirmed by any trustworthy primary evidence, and neither proven nor disproven") is the correct conclusion, but the intermediate speculative reasoning could be tightened. This is minor because the conclusion is accurate and the report's overall framing is strongly weighted against mechanism overclaiming.

### 7. Logical Consistency — no inconsistencies found

No internal contradictions were identified. The claim counts in the Summary (six load-bearing facts), the evidence-tier declaration, and the §6 bottom line are all mutually consistent. The distinction between "what the retractions destroy" and "what they leave uncertain" (§3.2a) is logically sound and correctly delineated.

### 8. No Additional Retrievals Needed

The primary probative claims in this report (retraction notice PMIDs, EoC PMIDs, ClinicalTrials.gov zero-results, FDA approval records, DOJ settlement) are documented with their primary sources or transparently labeled with their sourcing tier where primary sources were unavailable. No targeted retrieval is needed to validate or challenge the report's core findings.

---

## Summary

**Verdict: PASS.** The Dihexa research report handles the most integrity-sensitive elements correctly throughout: the retraction of Benoist 2014 and Kawas 2012 is unmissable and repeated at every relevant use point, the zero-human-data and fosgonimeton-distinction are explicit and carefully maintained, the c-Met oncogenic concern is framed as a genuine unresolved theoretical risk without overclaiming demonstrated carcinogenicity, and the independent-replication verdict (Sun 2021 PI3K/AKT not HGF/c-Met; Wells 2024 null) is accurately and prominently stated. Two minor findings: (1) the securities class action is cited only to Retraction Watch without a primary court record; (2) §3.2a's speculative passage on PI3K/AKT-c-Met reconciliation could be tightened to prevent soft rehabilitative reading of the retracted mechanism, though the closing sentence of that section is correct.
