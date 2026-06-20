# Gate 6 — CRITIQUE (red-team) — Hexarelin research report

**Agent:** critique-hex-i1 (Phase 6, adversarial; did NOT author the draft)
**Draft:** `vault/library/peptides/hexarelin/research-report.md` (564 lines)
**Corpus consulted:** sections A–F under `/tmp/aplus-research/hexarelin/sections/`

## Prose critique

I red-teamed the draft against the seven mandated defect axes. I attempted to break each claim; the draft held on every one. Summary of what I checked and found.

**1. GHRP-not-GHRH classification (CLEAN).** Every occurrence of "GHRH analogue" in the body is either an explicit negation ("Hexarelin is a GHRP / ghrelin-receptor agonist, NOT a GHRH analogue", lines 24, 30, 40) or refers to the *partner/contrast* drugs sermorelin / CJC-1295 / tesamorelin being a distinct receptor class. The mechanism (GHS-R1a, Gq/11→PLC→IP₃/Ca²⁺), the CD36 second target, and the discovery lineage (Bowers/Momany → Deghenghi GHRP-6 modification → Howard 1996 GHS-R cloning → ghrelin) are all correct. I specifically hunted for GHRH-analogue PK cross-attribution: the SC bioavailability (~77%) and the "~2× GHRH" potency are both attributed to hexarelin's own PK study [1, Ghigo 1994], and §8.2 line 373 *explicitly* states hexarelin's own dosing "is kept distinct from the GHRH-analogue partners and not cross-attributed." No misclassification, no cross-attribution.

**2. Tachyphylaxis prominence + acute≠sustained (CLEAN, exemplary).** Desensitization is the named defining limitation in the read-first box, TL;DR, §2.4 ("DEFINING LIMITATION"), §3, §5.2, and §7. The numbers match the corpus (section-B) exactly: GH AUC 19.1 ± 2.4 → 10.5 ± 1.8 µg/L·h (~45%), IGF-1/IGFBP-3 unchanged (P = 0.24 / 0.74), reversible recovery to 19.4 ± 3.7 µg/L·h. The "acute spikes overstate durable effect / no human evidence of a durable anabolic GH-IGF-1 signal" framing is repeated and prominent; acute GH potency is explicitly called "the trap." Acute does not read as durable efficacy anywhere.

**3. Non-selectivity (CLEAN).** Cortisol/ACTH/prolactin co-elevation is stated as a "defining liability," contrasted against ipamorelin in the read-first box, TL;DR, §2.3 (INTEGRITY FLAG), and §5.1, with the AVP-mediated CRH-independent HPA mechanism and the "ACTH/cortisol ≈ hCRH" comparison correctly carried from [9][11][2m].

**4. ABSENT efficacy + preclinical cardiac (CLEAN).** Body-comp / anti-aging / athletic are each labeled ABSENT with "ZERO robust human data" in §3.3 and elsewhere. Cardiac/CD36 is correctly framed as mostly preclinical: human data = acute inotropy only, and the dilated-cardiomyopathy (diseased-heart) human population explicitly did NOT respond acutely [15] — matches section-C verbatim.

**5. Regulatory (CLEAN).** Never approved (NCATS, [26]); FR-2026-07361 correctly presented as the PCAC July-23–24-2026 notice, NOT the removal action; hexarelin correctly stated as NOT among the April-2026 removed-12 (the 12 are enumerated, count verified = 12, hexarelin absent); WADA S2.2.4 named with examorelin(hexarelin) verbatim and the wada-ama.org PDF as primary. The §503A "never-nominated vs Category-2" ambiguity is honestly hedged, not overstated — and the end-state (ineligible) is correctly noted to hold either way.

**6. Citation integrity (CLEAN).** I extracted every inline token (body lines 1–454): {1,2,2_massoud,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,36,37,38,39,40,41,42,43,44,45}. Every one resolves to BOTH the crosswalk and the Bibliography (the `[2_massoud]` inline token → unified `[2m]` mapping is declared and consistent). The crosswalk and bibliography id-sets are identical. The "intentionally unused" numbers [16], [31]–[35] appear ONLY in the bookkeeping disclosure lines (451, 563) — no dangling inline reference exists. The Bowers-1990 / Massoud-1996 local-`[2]` collision is correctly disambiguated. No duplicate inline [n]. No Wikipedia anywhere (the only "wikipedia" string is the provenance assertion "No Wikipedia source is used"; an excluded-note is not present as a citation). Crosswalk present and complete.

**7. Tier / population / contradictions (CLEAN).** evidence_tier C and risk_tier experimental are defensible and well-argued in §7. Population annotation is consistent and, notably, the draft *resolved* a latent corpus inconsistency: section-B loosely called [7] "adults" in places while [8] said "12 healthy elderly." The report reconciles both to "healthy elderly (n=12)" uniformly with an explicit reconciliation note (§2.4 line 132, provenance line 562). [18] = 8 prepubertal short children, [1] = 12 healthy young adults, [13] = n=60 across 4 age groups — all distinct and correctly used. No contradiction between the "n=12 healthy adults" tag on [1] (Ghigo's healthy young volunteers) and the elderly Rahim population; they are different studies.

**Minor observations (NOT defects, no fix required).** (a) The §4 concentration audit counts the Rahim [7]/[8] pair as two primaries while acknowledging they are one underlying dataset — the draft already discloses this self-critically in its own coverage gaps, so it is not a hidden bias. (b) The Phase-II-discontinued-~2005 narrative rests on secondary source [27] and is flagged as such. Both are transparently hedged.

I could not manufacture a genuine major or critical defect against any of the seven axes. The draft is balanced, the absent/investigational/evidenced demarcation is rigorously applied, liabilities are foregrounded rather than buried, and citation bookkeeping is internally airtight.

## Verdict

verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-hex-i1","draft_path":"vault/library/peptides/hexarelin/research-report.md","findings":[],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
