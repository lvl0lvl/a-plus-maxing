# Gate 6 — Critique (Phase 6, deep mode, BLOCKING red-team)

Draft: `/tmp/aplus-research/bpc-157/research-report.md`
Draft sha256: `8b30b8d1e515bbfd1e7e8449ec425bda85d0d0e3ce05ec3211a38cda40a40ee2`

## Verdict

```
verdict: PASS
```

No CRITICAL gaps. The report is unusually disciplined on its highest-risk axes (species/route tagging, the rat-IV half-life, the single-lab concentration, and the human-efficacy = blank thesis). One **major** regulatory-currency finding (the FDA Category-2 removal is now primary-corroborated and the report over-dismisses it) and several **minor/major** balance refinements are logged below as recommended (non-blocking) fixes. None flips a core efficacy or safety conclusion, so PASS — but the regulatory-currency item should be addressed before publication if the corpus is unfrozen.

---

## Adversarial assessment by axis

### 1. Missing perspectives / unexamined counter-evidence
The skeptical case is made thoroughly and is, if anything, the spine of the report. The single-lab (Sikiric/Zagreb ~85%) problem is carried as a first-class section (§4) placed *before* the efficacy detail, restated in the tier rationale (§4b), the efficacy summary (§5.7), the negative-space section (§5.9), and the bottom line (§9.2). It is not buried. The 11/13 ≈ 85% arithmetic is internally consistent and both denominators (in-vivo 11/13, all-primaries 11/14) are disclosed. No place drifts toward crediting a human effect the evidence doesn't support — every efficacy statement is tagged animal/preclinical.

One residual skeptical gap (minor→major): the report's "independent corroboration" rests on refs [3], [5], [8], which the bibliography shows **all share author J.S. Pang at Chang Gung** — i.e., the *entire* non-Zagreb evidence base is a **single second lab**, not "independent replication" in the plural sense the phrase "distinct labs/groups = 2" can imply. The report names the group, so this is disclosed, but the skeptical force ("two labs total, one of which originated it") could be sharpened.

### 2. Overclaiming / hedging failures
Very strong. The "~15-min half-life" is correctly tagged rat-IV (n=6) everywhere it appears (integrity note §7, §7.2, §9.4) and never presented as human. No animal finding is implied as human-applicable; the §5.8 dose-bridge paragraph explicitly denies a validated rodent→human bridge. Quantitative claims carry species/route/n. The LD50 ≈ 2 g/kg folk figure is correctly omitted as unattributable. `human_pk_exists = false` is asserted. No overclaim findings rise above minor.

### 3. Logical consistency & citation completeness
Internally consistent across sections. Citation discipline is high: quantitative claims carry numbered sources; the reserved-placeholder [29] and the [34]/[34b] split are explicitly explained in the provenance note. The one orphan-adjacent item: §6.6 cites the IV pilot to `[33b]` but the n≈30 "three human pilot/case studies" aggregate is grounded only to review [2] + practitioner ref [33] — the other two pilots (intra-articular knee, intravesical) are not individually citable in the bibliography. This is acknowledged as "qualitative only / no admissible rate," so it is hedged, but the n≈30 figure is a soft number leaning on a secondary review. Minor.

### 4. Regulatory currency — the one material finding
The report stakes §3.1/§3.6/§9.5 on "the documented, authoritative status therefore **remains FDA 503A Category 2**," and frames the 2026 removal as "reported only by a secondary low-trust source (agemd.com)... NOT confirmed against an FDA/HHS primary." Three adversarial retrievals (below) show this dismissal is now **too strong**: the April 15, 2026 HHS-directed removal of ~11–12 peptides (incl. BPC-157) from Category 2, effective ~April 22, 2026, is corroborated by a **Federal Register notice (2026-07361, pub. 2026-04-16; Docket FDA-2025-N-6895)** establishing the PCAC public docket, plus a regulatory-law firm and multiple industry trackers — not just a longevity blog. The report's *own* corpus ([14], Hyman Phelps) already confirms the PCAC review is real, which sits in tension with calling the surrounding reclassification "unverified low-trust."

**Why this is major, not critical:** (a) the report's load-bearing conclusion is explicitly insulated — it repeatedly states a reclassification "adds no new safety data" and "changes the legal channel, not the evidence"; (b) removal from Category 2 does **not** make BPC-157 approved or (yet) compoundable, so the net "unapproved as a drug anywhere / WADA-S0 / not a legal supplement" thesis survives intact. The defect is one of *currency and even-handedness* in the regulatory framing, not of the core evidence verdict.

---

## Findings (machine-readable below)

```json
{
  "phase": "6",
  "critique_agent_id": "critique-bpc157-p6-i1",
  "draft_path": "/tmp/aplus-research/bpc-157/research-report.md",
  "draft_sha256": "8b30b8d1e515bbfd1e7e8449ec425bda85d0d0e3ce05ec3211a38cda40a40ee2",
  "findings": [
    {
      "category": "objectivity-issue",
      "severity": "major",
      "description": "Regulatory currency: the report asserts BPC-157 'remains FDA 503A Category 2' and frames the 2026 removal as resting 'only' on a low-trust longevity blog (agemd.com), 'NOT confirmed against an FDA/HHS primary.' As of 2026-06-18 the HHS-directed removal of ~11-12 peptides (incl. BPC-157) from Category 2 (announced 2026-04-15, effective ~2026-04-22) is corroborated by a Federal Register notice (2026-07361, pub. 2026-04-16, Docket FDA-2025-N-6895) and a regulatory-law firm plus multiple industry trackers. The report's own [14] already confirms the PCAC review is real, which is in tension with labeling the reclassification 'unverified low-trust.' The dismissal is now overstated and one-sided.",
      "required_fix": "Soften \u00a73.1/\u00a73.6/\u00a79.5 from 'remains Category 2 / unverified low-trust' to: BPC-157 was removed from 503A Category 2 by HHS direction effective ~April 2026 (Federal Register 2026-07361; Docket FDA-2025-N-6895), pending the July 23-24 2026 PCAC vote on a possible Category-1 move; removal does NOT confer drug approval or current lawful compounding. Preserve the (correct) point that this changes the legal channel, not the human safety/efficacy evidence. If corpus is frozen, add a dated currency caveat rather than asserting present-tense Category-2 status."
    },
    {
      "category": "balance-issue",
      "severity": "major",
      "description": "The 'independent corroboration' base (refs [3], [5], [8]) all share author J.S. Pang at Chang Gung University/Memorial Hospital per the bibliography. The phrase 'distinct labs/groups = 2' can read as broader independence than exists: the entire non-Zagreb evidence base is a SINGLE second lab, and even the 'two themes' (tendon-cell repair, angiogenesis) come from that one group. The skeptical thesis is slightly under-stated here.",
      "required_fix": "In \u00a74.3/\u00a74.4 state explicitly that the independent support derives from one additional lab (Pang/Chang Gung), so the corpus is 'originating lab + exactly one corroborating lab,' not multi-lab replication; reiterate that no third group has reproduced any in-vivo finding."
    },
    {
      "category": "citation-incomplete",
      "severity": "minor",
      "description": "The \u00a76 human-exposure aggregate 'combined n ~= 30, three human pilot/case studies' is grounded to review [2] + practitioner ref [33]; only the IV pilot (n=2) is individually citable ([33b]). The intra-articular-knee and intravesical/cystitis pilots are not separately sourced, so the n~=30 is a soft secondary-review figure.",
      "required_fix": "Tag the n~=30 explicitly as a secondary-review aggregate (per [2]) with only the n=2 IV pilot independently citable, or down-state to 'a handful of tiny pilot/case reports' without the specific count carrying citation weight."
    },
    {
      "category": "unexamined-counter-evidence",
      "severity": "minor",
      "description": "\u00a76.2 cites the human-melanoma in-vitro abstract [31] (BPC-157 INHIBITS growth) as countervailing evidence against the oncologic worry, but [31] is itself a Sikiric/Zagreb-group abstract (Radeljak, Seiwerth, Sikiric). The 'reassuring' direct-tumor data thus inherit the same single-lab provenance the report otherwise flags - this self-consistency caveat is applied to efficacy claims but not to the reassuring safety counter-evidence.",
      "required_fix": "Note in \u00a76.2 that the melanoma-inhibition abstract [31] is also from the originating group, so the 'opposite-direction' tumor signal carries the same single-lab caveat; keep the net 'unproven/untested in humans' conclusion."
    },
    {
      "category": "balance-issue",
      "severity": "minor",
      "description": "\u00a76.1 calls the animal toxicology 'genuinely reassuring,' but per [28] the per-group n values were not stated in the accessible text (report acknowledges this). A negative tox finding (no LD50, negative genotox/embryo-fetal) from studies of unknown/possibly small n and unknown independence should be hedged a notch more on the reassurance.",
      "required_fix": "Add that the toxicology reassurance is limited by unreported per-group n and unconfirmed lab-independence of [28], so 'no toxic dose reached' is bounded by study power, not a positive demonstration of long-term safety."
    }
  ],
  "additional_retrievals": [
    {
      "retrieve_agent_id": "critique-bpc157-p6-i1",
      "judge_agent_id": "critique-bpc157-p6-i1",
      "question": "As of mid-2026, is BPC-157 still in FDA 503A Category 2, or was it removed/reclassified, and is there a primary FDA/HHS source?",
      "brief_hash": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    {
      "retrieve_agent_id": "critique-bpc157-p6-i1",
      "judge_agent_id": "critique-bpc157-p6-i1",
      "question": "Does a primary FDA/HHS/Federal Register record (Docket FDA-2025-N-6895) confirm the April 2026 removal of BPC-157 from 503A Category 2 and the July 23-24 2026 PCAC meeting?",
      "brief_hash": "0000000000000000000000000000000000000000000000000000000000000000"
    },
    {
      "retrieve_agent_id": "critique-bpc157-p6-i1",
      "judge_agent_id": "critique-bpc157-p6-i1",
      "question": "Is Federal Register document 2026-07361 the Category-2 removal instrument itself or only the PCAC meeting/public-docket notice? (Inconclusive: primary URL bot-blocked via redirect to unblock.federalregister.gov; not chased.)",
      "brief_hash": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ],
  "halt_reasons": []
}
```

## Retrieval notes (corpus otherwise frozen)
1. WebSearch — FDA 503A BPC-157 Category-2 2026 reclassification/PCAC. Result: multiple sources report HHS/Kennedy removed ~12 peptides incl. BPC-157 from Category 2 on 2026-04-15.
2. WebSearch — Docket FDA-2025-N-6895 / Federal Register 2026-07361. Result: primary Federal Register notice (pub. 2026-04-16) establishing PCAC docket for the July 23-24 2026 meeting; removal effective ~2026-04-22; regulatory-law firm (boesensnowlaw.com) corroborates.
3. WebFetch — Federal Register 2026-07361 primary text. Result: INCONCLUSIVE — 302 redirect to unblock.federalregister.gov (bot-block); not chased. Could not confirm whether 2026-07361 is the removal instrument itself or only the meeting/docket notice; the removal appears to be an FDA web-list update directed by HHS, which remains the thinly-documented link at strict-primary level. This nuance is why the finding is major (over-dismissal corrected) rather than the report being flatly wrong on the removal mechanism.
