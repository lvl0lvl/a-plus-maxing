# Section A — Resistance-Training Adaptation Science & Dose-Response

*Goal-agnostic domain science to ground a personal-trainer specialist agent. No operator is personalized here; this is the canonical literature the agent reasons over. Every substantive claim carries exactly one type-tag `[N, tag]` where N indexes the Bibliography.*

---

## 1. Foundational principles the agent must reason over

**Progressive overload.** The ACSM position stand defines it as "the gradual increase in stress placed upon the body during exercise training," delivered by systematically manipulating load, volume, frequency, rest, and exercise selection [1, regulatory]. It is a consensus organizing principle, not a quantified law — the *optimal* magnitude/form of overload is what the dose-response literature below addresses. ESTABLISHED as a principle; the position stand's specific schedules (novice 8–12 RM, advanced 1–12 RM periodized) are graded expert consensus, not RCT-proven optima [1, regulatory].

**Specificity / SAID (Specific Adaptation to Imposed Demands).** Adaptations are specific to the imposed stimulus. The clearest modern demonstration is the load–outcome dissociation: maximal-strength (1RM) gains are specific to training with heavy loads, whereas hypertrophy is relatively load-agnostic when sets are taken near failure (Section 3) [4, meta_analysis]. Specificity also governs the concurrent-training interference effect (Section 7) and endurance modality transfer (Section 6). ESTABLISHED.

**Stimulus → fatigue → recovery → adaptation.** Standard framing: a stimulus induces acute fatigue/damage, followed by a recovery window during which adaptation occurs. Direct human time-course evidence: myofibrillar protein synthesis (MyoPS) over 10 weeks was *highest* after the first unaccustomed bout (when damage was also highest) but was NOT correlated with later hypertrophy; only once damage attenuated (weeks 2–3 on) did integrated MyoPS correlate with hypertrophy [6, rct]. The sequence is real, but the early high-turnover phase is partly repair, not net growth — not to be over-read as "more damage = more growth" (Section 5).

**Individual variability / responder heterogeneity.** Among the most ESTABLISHED yet coaching-underweighted facts. In 585 subjects training elbow flexors unilaterally for 12 weeks, muscle cross-sectional-area change ranged −2% to +59% and 1RM strength 0% to +250% — same program, vastly different responses [3, rct]. The HERITAGE Family Study (481 adults, 20-wk cycling) found mean VO2max gain ≈ 400 mL/min but individuals ranging from near-zero to > 1.0 L/min, with 2.5× more response variance *between* families than within → ~47% heritability of the VO2max training response [7, cohort]. IMPLICATION: population-mean dose-response curves describe the *expected* response; any individual prescription is a hypothesis to be revised against measured response, never a guarantee.

---

## 2. Hypertrophy dose-response: VOLUME (sets per week)

The anchor evidence is Schoenfeld, Ogborn & Krieger (2017), a meta-analysis of 34 treatment groups from 15 studies. It found a graded dose-response: each additional weekly set was associated with an effect-size increase of ~0.023, and higher-volume conditions out-grew lower-volume conditions by an effect size of 0.241 (≈ 3.9% greater hypertrophy) [2, meta_analysis]. The widely cited practical reading is that ≥10 sets/muscle/week tends to beat < 5 sets/week [2, meta_analysis]. ESTABLISHED: more volume → more hypertrophy, monotonic across the studied range.

WHERE THE EVIDENCE GETS THIN / CONTESTED:
- The curve's *upper end* is poorly characterized. Most studies tested low-to-moderate set counts; very-high-volume arms (20–30+ sets) are sparse, heterogeneous, and confounded by adherence/recovery. Newer meta-regression (Sports Medicine, 2025) extends the curve and reports continued but *diminishing* returns for hypertrophy, with strength returns diminishing far more steeply [9, meta_analysis]. PROVISIONAL at the high-volume end.
- **MEV / MAV / MRV "volume landmarks"** (minimum effective / maximum adaptive / maximum recoverable volume) are a popular practitioner framework, not evidence-grounded measurable thresholds. There is no validated per-muscle MRV number in the peer-reviewed literature; the landmarks are useful vocabulary but their attached numbers are practitioner-derived, not meta-analytically established [anecdote_aggregate]. The agent should treat them as a *conceptual scaffold*, never as numeric prescriptions to assert as fact.
- Any single "optimal volume" number is unsupported: the dose-response is a population curve with wide individual variation [3, rct].

---

## 3. Intensity / load: the load–hypertrophy relationship

Schoenfeld, Grgic, Ogborn & Krieger (2017) meta-analyzed 21 studies of low-load (≤60% 1RM) vs high-load (>60% 1RM) training, all to momentary failure [4, meta_analysis]:
- **Hypertrophy:** no significant difference between loads — muscle growth is achievable across a wide loading spectrum *when sets are taken to/near failure* [4, meta_analysis]. ESTABLISHED.
- **Strength (1RM):** significantly greater with high loads; isometric strength did not differ significantly [4, meta_analysis]. ESTABLISHED — this is the load-specificity of maximal strength (SAID).

Practical caveats from the literature: light-load-to-failure imposes high metabolic discomfort that can hurt adherence, and heavy-load protocols may need more sets to match moderate-load hypertrophy [4, meta_analysis]. An independent network meta-analysis broadly corroborates that load matters more for strength than for hypertrophy [10, meta_analysis].

**Proximity to failure.** Refalo, Helms, Trexler, Hamilton & Fyfe (2022, Sports Medicine) meta-analyzed proximity-to-failure and hypertrophy: training *to* momentary failure was NOT superior to non-failure training (ES 0.12, 95% CI −0.13 to 0.37, p=0.343), suggesting a likely non-linear relationship where reaching a *sufficient* proximity matters more than hitting absolute failure [5, meta_analysis]. ESTABLISHED that absolute failure is not required; the precise RIR (reps-in-reserve) threshold below which hypertrophy drops off is PROVISIONAL (commonly placed around 0–5 RIR, with steeper drop-off beyond ~4–5 RIR, but this is an evolving estimate, not a fixed constant). Mechanistic rationale (motor-unit recruitment of higher-threshold units near failure) is a MECHANISM hypothesis, not a proven causal chain [5, meta_analysis].

---

## 4. Frequency (volume-equated)

Schoenfeld, Grgic & Krieger (2019), 25 studies, asked how weekly training frequency affects hypertrophy [8, meta_analysis]:
- **When weekly volume is equated:** no significant difference between higher and lower frequency — frequency is essentially a way to *distribute* a given volume, and can be chosen by preference/recovery [8, meta_analysis]. ESTABLISHED.
- **When volume is NOT equated:** a modest advantage for higher frequency appears, but this is confounded because higher frequency usually means more total volume [8, meta_analysis]. So the apparent "frequency effect" is largely a volume effect in disguise.

IMPLICATION: the agent should treat frequency as a recovery/logistics lever for delivering a target weekly volume, not as an independent hypertrophy driver.

---

## 5. Mechanisms of hypertrophy

The classic triad (Schoenfeld 2010) proposes mechanical tension, metabolic stress, and muscle damage as drivers [11, mechanism_review]:
- **Mechanical tension** — the most strongly supported primary driver; mechanotransduction → mTORC1-mediated elevation of muscle protein synthesis is the best-characterized pathway, though "key but not sole" [11, mechanism_review][12, mechanism_review]. ESTABLISHED as the leading mechanism.
- **Metabolic stress** — proposed contributor (cell swelling, metabolite accumulation, fiber recruitment). PROVISIONAL/CONTESTED — plausible and supported by some signaling data but its independent causal contribution in humans is not cleanly isolated [11, mechanism_review].
- **Muscle damage as a *driver* of hypertrophy** — this is the claim to flag hardest. Direct human time-course evidence shows damage and the early MyoPS spike are dissociated from eventual hypertrophy; growth tracks MyoPS only *after* damage attenuates [6, rct]. Post-2016 the field has largely moved to viewing damage as a *byproduct/consequence* of training rather than a *necessary cause* of growth. CONTESTED → leaning toward "not a required driver." The popular "you must feel sore / chase damage to grow" narrative is NOT supported and should be flagged by the agent as a coaching myth [6, rct].

A 2018–2019 mechanistic synthesis frames load (40–80% 1RM for hypertrophy; >60% for max strength) within an mTORC1-centric model of stimulus sensing [12, mechanism_review] — consistent with Sections 2–3.

---

## 6. Endurance / aerobic adaptations

**VO2max trainability and its limiting factor.** Bassett & Howley (2000) is the canonical synthesis: in healthy humans VO2max is limited primarily by *central* oxygen delivery (maximal cardiac output), not peripheral muscle O2 extraction — supported by (a) VO2max tracking O2-delivery manipulations (blood doping, hypoxia, beta-blockade), (b) training-induced VO2max gains arising mainly from increased maximal cardiac output rather than widened a-v O2 difference, and (c) small-muscle-mass overperfusion showing huge local O2-consumption capacity [13, mechanism_review]. ESTABLISHED for healthy populations.
- *Central adaptations:* increased stroke volume / maximal cardiac output and blood/plasma volume dominate the VO2max improvement [13, mechanism_review]. ESTABLISHED.
- *Peripheral adaptations:* mitochondrial density, capillarization, and oxidative-enzyme increases improve fatigue resistance and submaximal economy/lactate handling but contribute less to the *VO2max ceiling* itself [13, mechanism_review]. ESTABLISHED that peripheral adaptations occur; their role is more about endurance *performance* than the VO2max number.
- *Trainability is heritable and heterogeneous:* ~47% heritability of the VO2max response, with non-responders existing (Section 1) [7, cohort].

**Training-intensity distribution (polarized vs threshold; Z2 / zone models).** Polarized distribution (≈75–80% of sessions in low-intensity Zone 1, <10% in Zone 2, 15–20% in high-intensity Zone 3) is heavily promoted. Evidence: an early RCT (Stöggl & Sperlich 2014) and a 2018 systematic review/meta-analysis of RCTs reported polarized tending to outperform threshold-emphasis training for endurance variables [14, meta_analysis]. PROVISIONAL/CONTESTED: a 2024 Sports Medicine systematic review with meta-analysis found polarized *may* yield greater performance gains than threshold but explicitly notes the "best-practice" intensity-distribution model remains open to debate, with conflicting retrospective data and heterogeneous study designs [15, meta_analysis]. The "Zone 2" / low-intensity base concept is a useful organizing model but the specific zone boundaries (lactate vs ventilatory vs %HRmax thresholds) are method-dependent and not universally standardized — the agent should flag that "Zone 2" is a family of operational definitions, not one fixed physiological line [15, meta_analysis].

---

## 7. Concurrent training / interference effect

Wilson, Marin, Rhea, Wilson, Loenneke & Anderson (2012) meta-analyzed 21 concurrent-training studies (422 effect sizes) [16, meta_analysis]:
- **Magnitude:** strength-only training produced larger strength ES (≈1.76) than concurrent training (≈1.44); hypertrophy ES was 1.23 (strength-only) vs 0.85 (concurrent). So interference is *real but moderate*, not catastrophic [16, meta_analysis]. ESTABLISHED that an interference effect exists.
- **Moderators:** the interference was driven by endurance *modality* (running impaired strength/hypertrophy, cycling did not, plausibly via overlapping musculature, eccentric damage, and higher metabolic stress), and scaled with endurance *frequency* and *duration*. Effects were largely *limb-specific* — lower-body strength suffered after lower-body endurance work, upper body was spared [16, meta_analysis]. ESTABLISHED moderators.

IMPLICATION: the agent can reason that interference is manageable via modality selection (cycling over running for lower-body lifters), controlling endurance frequency/duration, and separating sessions — but should present the magnitude honestly as moderate, not as "endurance ruins gains."

---

## 8. Minimal effective dose & maintenance / detraining resistance

Maintaining adaptations costs far less than building them. The minimalist-training literature (Sports Medicine narrative review and minimal-dose overview, 2023–2024) indicates that low weekly volumes — on the order of a few hard sets per muscle — can drive strength gains, and that *maintenance* of strength and muscle mass is achievable at substantially reduced volume **provided intensity (load and proximity to effort) is maintained** [17, mechanism_review][18, mechanism_review]. The reduced meta-regression "minimum effective dose" estimate for strength is on the order of ~4 fractional weekly sets [9, meta_analysis]. PROVISIONAL on exact numbers (narrative-review and meta-regression syntheses, heterogeneous protocols), ESTABLISHED in direction: maintenance is cheaper than accumulation, and load-intensity is the variable you must NOT cut when reducing volume for maintenance.

IMPLICATION: when an operator must deload, travel, or rehab, the agent should reason that volume can be cut sharply while load/effort is preserved to defend existing adaptations — but should flag the maintenance-dose numbers as approximate, not precise thresholds.

---

## Bibliography

*First-author surname + initials, year, journal, design, identifiers. Identifiers verified against PubMed/PMC where stated; where not independently verified that is noted.*

1. Ratamess NA, Alvar BA, Evetoch TK, et al. (American College of Sports Medicine). Progression models in resistance training for healthy adults. *Med Sci Sports Exerc.* 2009;41(3):687–708. ACSM Position Stand. Type: regulatory/consensus. DOI 10.1249/MSS.0b013e3181915670. (Identity/year/journal verified via search; exact DOI not independently re-fetched — cite bibliographically.)

2. Schoenfeld BJ, Ogborn D, Krieger JW. Dose-response relationship between weekly resistance training volume and increases in muscle mass: a systematic review and meta-analysis. *J Sports Sci.* 2017;35(11):1073–1082. Meta-analysis (34 treatment groups, 15 studies). PMID 27433992; DOI 10.1080/02640414.2016.1210197. (PMID + DOI verified via PubMed fetch.)

3. Hubal MJ, Gordish-Dressman H, Thompson PD, et al. Variability in muscle size and strength gain after unilateral resistance training. *Med Sci Sports Exerc.* 2005;37(6):964–972. RCT-style intervention, n=585. PMID 15947721. (PMID verified via PubMed fetch; DOI not independently confirmed.)

4. Schoenfeld BJ, Grgic J, Ogborn D, Krieger JW. Strength and hypertrophy adaptations between low- vs. high-load resistance training: a systematic review and meta-analysis. *J Strength Cond Res.* 2017;31(12):3508–3523. Meta-analysis (21 studies). PMID 28834797; DOI 10.1519/JSC.0000000000002200. (PMID + DOI verified via PubMed fetch.)

5. Refalo MC, Helms ER, Trexler ET, Hamilton DL, Fyfe JJ. Influence of resistance training proximity-to-failure on skeletal muscle hypertrophy: a systematic review with meta-analysis. *Sports Med.* 2023;53(3):649–665 (epub 2022). Meta-analysis. PMID 36334240; PMCID PMC9935748; DOI 10.1007/s40279-022-01784-y. (PMID/PMCID/DOI verified via PMC fetch.)

6. Damas F, Phillips SM, Libardi CA, et al. Resistance training-induced changes in integrated myofibrillar protein synthesis are related to hypertrophy only after attenuation of muscle damage. *J Physiol.* 2016;594(18):5209–5222. Longitudinal human intervention (tagged rct as a controlled training intervention with mechanistic time-course). PMID/PMCID PMC5023708; DOI 10.1113/JP272472. (PMCID + DOI verified via search; PMID not independently re-fetched.)

7. Bouchard C, An P, Rice T, et al. Familial aggregation of VO2max response to exercise training: results from the HERITAGE Family Study. *J Appl Physiol.* 1999;87(3):1003–1008. Family cohort (n=481, 20-wk training). PMID 10484570; DOI 10.1152/jappl.1999.87.3.1003. (PMID + DOI verified via PubMed fetch.)

8. Schoenfeld BJ, Grgic J, Krieger J. How many times per week should a muscle be trained to maximize muscle hypertrophy? A systematic review and meta-analysis of studies examining the effects of resistance training frequency. *J Sports Sci.* 2019;37(11):1286–1295. Meta-analysis (25 studies). PMID 30558493; DOI 10.1080/02640414.2018.1555906. (PMID + DOI verified via PubMed fetch.)

9. Pelland JC, Remmert JF, Robinson ZP, et al. The resistance training dose-response: meta-regressions exploring the effects of weekly volume and frequency on muscle hypertrophy and strength gain. *Sports Med.* 2025 (also on SportRxiv as preprint). Meta-regression. DOI pending/2025 issue. (Existence verified via search; preprint/early version — flagged as not all identifiers independently confirmed. Used only for the diminishing-returns direction and ~4-set minimum-dose figure, both also consistent with [17][18].)

10. Lopez P, Radaelli R, Taaffe DR, et al. Resistance training load effects on muscle hypertrophy and strength gain: systematic review and network meta-analysis. *Med Sci Sports Exerc.* 2021;53(6):1206–1216. Network meta-analysis. PMID 33433148. (PMID surfaced via search; used only as corroboration of [4]; DOI not independently confirmed.)

11. Schoenfeld BJ. The mechanisms of muscle hypertrophy and their application to resistance training. *J Strength Cond Res.* 2010;24(10):2857–2872. Mechanism review. PMID 20847704. (PMID surfaced via search; DOI not independently confirmed.)

12. Wackerhage H, Schoenfeld BJ, Hamilton DL, Lehti M, Hulmi JJ. Stimuli and sensors that initiate skeletal muscle hypertrophy following resistance exercise. *J Appl Physiol.* 2019;126(1):30–43. Mechanism review. DOI 10.1152/japplphysiol.00685.2018. (Journal/DOI surfaced via search; PMID not independently confirmed.)

13. Bassett DR Jr, Howley ET. Limiting factors for maximum oxygen uptake and determinants of endurance performance. *Med Sci Sports Exerc.* 2000;32(1):70–84. Mechanism/review. PMID 10647532; DOI 10.1097/00005768-200001000-00012. (PMID + DOI verified via PubMed fetch.)

14. Rosenblat MA, Perrotta AS, Vicenzino B. Polarized vs. threshold training intensity distribution on endurance sport performance: a systematic review and meta-analysis of randomized controlled trials. *J Strength Cond Res.* 2019;33(12):3491–3500. Meta-analysis of RCTs. PMID 29863593. (PMID surfaced via search; DOI not independently confirmed. The Stöggl & Sperlich 2014 *Front Physiol* RCT is the supporting primary; flagged as a single RCT.)

15. González-Rave JM, et al. Comparison of polarized versus other types of endurance training intensity distribution on athletes' endurance performance: a systematic review with meta-analysis. *Sports Med.* 2024. PMCID PMC11329428; DOI 10.1007/s40279-024-02034-z. (PMCID + journal surfaced via search; first-author list not fully confirmed — cite bibliographically. Used for the "remains debated" CONTESTED framing.)

16. Wilson JM, Marin PJ, Rhea MR, Wilson SMC, Loenneke JP, Anderson JC. Concurrent training: a meta-analysis examining interference of aerobic and resistance exercises. *J Strength Cond Res.* 2012;26(8):2293–2307. Meta-analysis (21 studies, 422 ES). PMID 22002517. (PMID surfaced via search; DOI not independently confirmed.)

17. Iversen VM, Norum M, Schoenfeld BJ, Fimland MS. No time to lift? Designing time-efficient training programs for strength and hypertrophy: a narrative review. *Sports Med.* 2021;51(10):2079–2095. Narrative review. (Cited as a minimalist/time-efficiency synthesis; tagged mechanism_review for the narrative-review type. Identifiers not independently confirmed — cite bibliographically.)

18. Androulakis-Korakakis P, et al. Minimal dose / minimalist resistance training syntheses. *Sports Med.* 2023–2024 (Minimalist Training narrative review, PMCID PMC10933173; and Resistance Exercise Minimal Dose Strategies overview, DOI 10.1007/s40279-024-02009-0). Narrative review / overview of reviews. (PMCID + DOI surfaced via search; first-author attribution not fully confirmed — cite bibliographically.)

---

## Self-check

**Claims I could NOT fully ground to an independently re-fetched whitelisted primary** (surfaced via search-engine snippet only, identifiers not all re-verified by direct fetch — flagged, not fabricated):
- [1] ACSM 2009 position stand DOI not independently re-fetched; identity/journal/year confirmed via search.
- [9] Pelland/Remmert/Robinson 2025 dose-response meta-regression — preprint/recent version; not all identifiers confirmed. Used only for diminishing-returns *direction* and the ~4-set minimum-dose figure, both corroborated by [17][18]. NOT used as the sole basis for any hard number stated as established.
- [10][11][12][14][16][17][18] PMIDs/DOIs surfaced via search but not each independently re-fetched; authorship of [15] and [18] not fully confirmed. All are real, well-known papers in the field; cited bibliographically per instruction. No identifier was invented.
- The MEV/MAV/MRV "volume landmarks" have NO grounding citation by design — explicitly flagged as a practitioner heuristic (`anecdote_aggregate`), not peer-reviewed thresholds.
- The specific RIR drop-off threshold (~4–5 RIR) is a literature *estimate*, flagged PROVISIONAL, not asserted as a fixed constant.

**Independently re-fetched and verified (PMID/DOI confirmed by direct PubMed/PMC fetch):** [2] PMID 27433992 / DOI 10.1080/02640414.2016.1210197; [3] PMID 15947721; [4] PMID 28834797 / DOI 10.1519/JSC.0000000000002200; [5] PMID 36334240 / PMC9935748 / DOI 10.1007/s40279-022-01784-y; [7] PMID 10484570 / DOI 10.1152/jappl.1999.87.3.1003; [8] PMID 30558493 / DOI 10.1080/02640414.2018.1555906; [13] PMID 10647532 / DOI 10.1097/00005768-200001000-00012.

**Evidence-strength summary**

*Source-concentration disclosure:* the hypertrophy dose-response backbone (volume [2], load [4], frequency [8], mechanism [11][12]) derives substantially from the Schoenfeld/Krieger research collaboration; what upgrades these findings from single-group results to ESTABLISHED is independent corroboration — Refalo et al. [5] on proximity-to-failure, Pelland et al. [9] on the dose-response meta-regression, and Lopez et al. [10] network meta-analysis on load — converging on the same conclusions from outside that group.

ESTABLISHED (replicated meta-analysis / strong consensus):
- Volume → hypertrophy is graded and positive across the studied low-to-moderate range [2].
- Load is specific to *strength* (heavy > light for 1RM) but largely irrelevant to *hypertrophy* when sets are near failure [4].
- Frequency does not independently drive hypertrophy when volume is equated [8].
- Mechanical tension is the leading hypertrophy mechanism (mTORC1-mediated MPS) [11][12].
- VO2max is centrally limited (cardiac output) in healthy humans; central > peripheral for the VO2max ceiling [13].
- Concurrent-training interference is real but moderate, modality- and limb-specific (running worse than cycling) [16].
- Large individual response heterogeneity in both hypertrophy/strength [3] and VO2max (~47% heritable) [7].
- Absolute failure is not required for hypertrophy; sufficient proximity matters more [5].
- Maintenance is achievable at sharply reduced volume if load/effort is preserved [17][18].

PROVISIONAL / CONTESTED (flagged honestly):
- The upper end of the volume curve (very high sets) and the existence of a clear MRV — diminishing returns are likely but the ceiling is poorly characterized [9].
- **MEV/MAV/MRV volume landmarks** — practitioner heuristic, NOT validated numeric thresholds.
- **Muscle damage as a *driver* (vs byproduct) of hypertrophy** — post-2016 evidence leans against the "chase damage/soreness" narrative [6].
- Metabolic stress as an independent causal mechanism — plausible, not cleanly isolated in humans [11].
- Polarized vs threshold intensity distribution superiority — leans polarized but explicitly debated; "Zone 2" is a family of operational definitions, not one fixed line [14][15].
- Exact minimum-effective and maintenance dose *numbers* — direction established, precise thresholds approximate [9][17][18].

**HALT-risk note:** No fabricated identifiers. The only structural risk is reliance on search-snippet-level identifiers for ~7 of 18 sources (flagged above); all are real field-standard papers and none anchor a unique numeric claim that isn't independently corroborated. MEV/MAV/MRV is the single most important honesty flag — it is the popular framework most likely to be mistaken for established science.
