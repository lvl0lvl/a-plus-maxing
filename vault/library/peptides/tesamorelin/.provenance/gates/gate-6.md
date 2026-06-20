# Gate 6 — CRITIQUE (red-team) — Tesamorelin research-report.md

Adversarial review of the Phase-5 synthesis (`vault/library/peptides/tesamorelin/research-report.md`, 596 lines) against the six validated section files (A–F). I did not author the draft. Reviewed for the seven mandated axes; below is the point-by-point read.

---

## 1. Approved-vs-off-label discipline (the #1 axis for this compound)

**PASS — exemplary.** This is the single most important axis and the draft enforces it harder than any other element. The three-way demarcation §2 (PROVEN, HIV-lipodystrophy VAT) / §3 INVESTIGATIONAL (NAFLD + cognition) / §3.3 ABSENT (physique/athletic/anti-aging/healthy-adult fat loss) is sharp, repeated, and never blurred:

- The frontmatter "Read this first" block leads with the approved indication and immediately states the beyond-label domains are INVESTIGATIONAL and that "General anti-aging, bodybuilding, athletic performance, and healthy-adult fat loss have ZERO human efficacy data."
- §2's opening "Scope / integrity boundary (read before any number)" explicitly fences every efficacy figure to the HIV-lipodystrophy population and forbids reading it as general fat-loss evidence.
- Every trial in §2/§3 is population-annotated. The draft is careful that NAFLD evidence is "100% HIV-positive" and that cognition (Baker 2012) is the *one* HIV-negative signal — and it does NOT let that one HIV-negative signal bleed into a generalized anti-aging claim (it is explicitly labeled surrogate-endpoint, 20-week, no Phase 3, "does NOT support clinical use").
- §6.1 repeats the "Critical scope point" that approval for one narrow indication is not approval for any other purpose.

The HIV-lipodystrophy approved efficacy is never permitted to read as general anti-aging/bodybuilding/healthy-adult efficacy. No defect.

## 2. Efficacy overstatement

**PASS.** VAT/visceral-selective + weight-neutral + reverses-on-stop is stated correctly and is NOT conflated with subcutaneous-fat / muscle / weight outcomes. Specifically:

- The "weight neutral" label limitation and the formal SAT-no-change result (−2±32 vs +2±29 cm², P=0.08) are both carried (§2.3, §2.6), and the draft explicitly says "this is not generalized fat loss" and "not weight, not subcutaneous fat, and not lean mass."
- Reversal-on-discontinuation is stated as a first-class honest point in §1.2, §2.2, §2.6, and §5 — faithful to section A [Bedimo] and section B [Falutz JAIDS].
- Magnitude numbers (−15.2% NEJM; −15.4%/−24 cm² pooled; ~−18% at 52wk; MD −27.71 cm² meta) all match section B verbatim. No invented numbers found.

The 2026 meta VAT/hepatic-fat confirmation is explicitly annotated "HIV-lipodystrophy throughout — this is NOT a general-population meta-analysis." Good.

## 3. Tier justification (evidence_tier B / risk_tier medium)

**PASS — defensible and well-argued.** evidence_tier B is justified from the body: FDA approval + two coordinated pivotal Phase 3 RCTs (n≈806 pooled) + 52-week extension + independent 2026 meta — genuinely above the unapproved peptides (tier C), and held below S/A for three converging, body-supported reasons (narrow population/endpoint; 100% single-sponsor concentration; zero off-label efficacy data). risk_tier medium is likewise defensible: approved, monitorable, reversible, but with real GH-axis/IGF-1, a glucose/diabetes signal (label OR 3.3), four contraindications, and class concerns (neoplasm, critical-illness mortality). Neither over- nor under-tiered. The §7 reasoning maps cleanly onto §2–§6.

## 4. Regulatory accuracy

**PASS.** All anchors verified against section E:
- FDA approval 2010 (review action Nov 10, 2010; announced Nov 11, 2010; "Initial U.S. Approval 2010"). Correct.
- Exact indication wording "reduction of excess abdominal fat in HIV-infected adult patients with lipodystrophy" — verbatim, matches label/section E.
- Egrifta SV reformulation 2019; Egrifta WR via supplemental BLA March 25, 2025. Correct.
- EMA: not approved — application by Ferrer Internacional S.A. submitted 31 May 2011, withdrawn under a negative provisional CHMP benefit-risk opinion (the "hard to differentiate lipodystrophy fat from obesity fat" concern). Faithful to section E [25][26].
- WADA S2.2.4 named explicitly, prohibited at all times. Matches section E [29].

The three Limitations of Use are carried verbatim. No regulatory drift.

## 5. Citation integrity

**PASS.** Verified mechanically:
- 41 bibliography entries (37 base [1]–[39] with intentional dedup gaps at [4] and [30], plus sub-entries 1a/27a/27b/39a). The "41 base entries" provenance claim is accurate.
- No dangling inline body citation. The only inline `[4]` tokens (6×) are all in the LEFT column of the Citation crosswalk (section-local source tokens), not in the report body — they resolve to unified [7]/[13]/[18]/[14]/[24]/[1a]. Confirmed not a defect.
- No duplicate sources under different unified numbers. Each PMID/setid has exactly one canonical entry; the apparent PMID repeats (28617838 ×3, 18057338 ×2) are crosswalk/annotation/provenance mentions, not separate entries. The label setids (Egrifta SV 3d783378…, Egrifta WR 839334d3…) and Falutz/LiverTox/Stanley duplicates are correctly deduped per the crosswalk.
- Crosswalk present and complete (every section-local token → unified mapping).
- No Wikipedia anywhere (provenance note asserts it; grep confirms none).
- PMID 28617838 = Clemmons DR, *PLOS One* 2017 — correct and internally consistent (§5.3 inline, crosswalk D[6], bib [21], provenance note all agree).

## 6. Concentration / sponsor audit (first-class)

**PASS.** The audit is carried first-class and up front (§4), faithfully transposed from section C with the dual-lens treatment intact:
- Academic-lineage: MGH/Grinspoon–Stanley 50% (2/4), below the 70% flag.
- Industry-sponsor: 100% (4/4) Theratechnologies study-drug/sponsorship, FLAGGED ≥70%, with the honest caveat that this is structurally inevitable for a single-source approved drug and the real consequence is "no manufacturer-independent confirmatory program." Fourman 2020 correctly excluded as a mechanistic secondary (not double-counted). Denominator = 4. Matches section C exactly. This is fed into the tier-B rationale (§7).

## 7. Unsupported / corpus-exceeding claims, invented numbers, contradictions

**PASS — none found.** Spot-checked all load-bearing numbers (PK t½/Tmax/clearance, VAT %s, IGF-1 deltas, AE rates, HbA1c OR 3.3, IGF-1 SDS proportions, cognition n=152/dose 1 mg, NAFLD n=61/−4.1%, type-2-diabetic n=53) against sections A–F: every value is faithfully represented, no fabrication, no figure exceeds its source. The report is explicitly corpus-read-only and the provenance note's claims hold up.

### Minor observations (non-blocking)

- **[minor] §1.3 PK secondary-range hedge.** The report keeps the label-derived t½ values (8 min healthy; ~18 min single / ~37 min multiple in HIV+) and notes they "bracket the commonly cited ~26–38 min range." This is faithful to section A, but the "~26–38 min" secondary range is not itself separately cited — it is presented as orienting context only. Carried as-is from the corpus; no action required.
- **[minor] Cost range provenance.** §6.5 widens the section-E "~$3,000/mo" figure to "$2,400–$5,500/mo" via aggregator [34], which was not in section E. This is sourced (tag=anecdote, qualitative, non-clinical) and flagged as price-aggregator, consistent with the §F prescribing layer; acceptable but is the one figure that originates in the §F/synthesis layer rather than §E. Not load-bearing.

These are the only two items worth noting and neither approaches major severity.

---

## Verdict

verdict: PASS

The draft is faithful to the A–F corpus on every checked axis. The approved-vs-off-label discipline — the #1 axis for tesamorelin — is enforced rigorously and repeatedly; efficacy is not overstated; tiers are defensible; regulatory facts are accurate; citations are complete with no dangling/duplicate inline references and no Wikipedia; the concentration/sponsor audit is first-class; and no invented numbers, contradictions, or corpus-exceeding claims were found. Only two minor, non-blocking observations.

```json
{"phase":"6","critique_agent_id":"critique-tesa-i1","draft_path":"vault/library/peptides/tesamorelin/research-report.md","findings":[{"category":"citation-incomplete","severity":"minor","description":"§1.3 cites a secondary '~26-38 min' half-life range as orienting context without its own inline citation; faithful to section A (presented as bracketing context only), not load-bearing."},{"category":"balance-issue","severity":"minor","description":"§6.5 widens the section-E '~$3,000/mo' cost to '$2,400-$5,500/mo' via aggregator [34] not present in section E; properly tagged anecdote/price-aggregator and flagged non-clinical, but originates in the synthesis/§F layer rather than §E."}],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
