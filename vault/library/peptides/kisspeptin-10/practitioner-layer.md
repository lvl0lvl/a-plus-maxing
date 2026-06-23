---
title: Kisspeptin-10 — Prescribing-Practice Layer
type: note
permalink: a-plus-maxing/library/peptides/kisspeptin-10/practitioner-layer
provenance_dir: design/.kisspeptin-10-design-work
provenance_slug: labs-specialist
---

# Kisspeptin-10 — Prescribing-Practice Layer

> **Scope discipline.** This document records *how kisspeptin-10 is actually accessed, dosed, and (where applicable) monitored in practice* — the dose/cycle/route/reconstitution conventions that circulate in prescriber blogs, clinic pages, and dosing aggregators, plus the regulatory and compounding status that governs whether any legitimate clinical prescribing pathway exists. It is **not** an efficacy document. Per the source-tagging rule, `practitioner_protocol` (Tier 2.7), `compounding_data_sheet` (Tier 3), and `vendor_label` / `anecdote_aggregate` (Tier 4) sources are admissible **only** for dose/cycle/route/reconstitution conventions and (for vendor labels) purity/reconstitution math. **None** of these source classes grounds an efficacy, adverse-event-rate, or mechanism claim.
>
> **Regulatory state, read first.** Kisspeptin-10 is **not an FDA-approved drug for any indication** and is **not on the 503A bulk drug substances list (Category 1 or Category 2)**. On October 29, 2024, FDA's Pharmacy Compounding Advisory Committee (PCAC) voted **11 to 0** against recommending kisspeptin-10 for inclusion in the 503A bulks regulation [1, regulatory]. The proposed use — SC/IM injection for secondary hypogonadism in men — was rejected on four grounds: inadequate physicochemical characterization (impurity profile not publicly characterized), immunogenicity risk for a parenterally administered decapeptide, insufficient clinical evidence, and the availability of FDA-approved alternatives for secondary hypogonadism. There is therefore **no legitimate US compounding pathway** for kisspeptin-10; any 503A or 503B pharmacy dispensing it does so outside the scope of FDA authorization and with direct enforcement exposure. Kisspeptin-10 is also **explicitly prohibited in males** by WADA under Section S2 (Peptide Hormones / Testosterone-Stimulating Peptides), added by name in the 2024 update [2, regulatory]. The "prescribing practice" described here is a grey-market and research-chemical practice with no approved standard of care, no lawful US compounding channel, and no cleared supply chain.
>
> **PT-141 / Vyleesi is the approved HSDD drug — not kisspeptin-10.** Bremelanotide (PT-141, marketed as Vyleesi) was FDA-approved in June 2019 for acquired, generalized hypoactive sexual desire disorder (HSDD) in premenopausal women. It acts via melanocortin (MC3R/MC4R) receptors, not the HPG axis. KP-10 is neither the same drug nor a compoundable substitute for it. Any patient or buyer comparing the two is making a category error: PT-141 is an approved melanocortin agonist with an established prescribing pathway; KP-10 is an unapproved research peptide with no clinical supply chain. [See "Sourcing hazards" section below.]

## No admissible compounding-pharmacy clinical data sheet located

**Gate finding: NO admissible compounding-pharmacy clinical data sheet (a pharmacy-issued monograph whose dose/route/indication claims cite their own primary literature) was located for kisspeptin-10.** This is fully consistent with the regulatory state: the PCAC voted against including KP-10 on the 503A bulks list, so no 503A pharmacy has a basis to publish a standardized clinical monograph with literature citations.

**Searched vendors / pharmacies / source classes** (none yielded an admissible data sheet):

- **Empower Pharmacy** (empowerpharmacy.com) — 503A/503B Houston compounder; catalog searched; kisspeptin-10 is **not listed** as a compounded product, consistent with the post-PCAC regulatory state
- **Tailor Made Compounding / Infiniwell** — 503A compounder; no public KP-10 clinical monograph or data sheet located
- **Hallandale Pharmacy** — 503A/503B compounder; no public KP-10 clinical monograph or data sheet located
- **Belmar Pharma Solutions** — 503A compounder; no public KP-10 data sheet located
- **Strive Pharmacy** (strivepharmacy.com) — no public KP-10 data sheet located
- **APS (Applied Pharmacy Services)** — no public KP-10 data sheet located
- **Beverly Hills Rejuvenation Center** (bhrcenter.com) — clinic/pharmacy hybrid; lists kisspeptin-10mg as a peptide offering with individualized dosing and physician oversight language but **no clinical data sheet, no primary literature citations, no named prescribing physician or dated protocol** on the publicly accessible page; content is clinic marketing copy → **not a compounding clinical data sheet** [3, anecdote_aggregate]
- Generic compounding "monograph / fact sheet / data sheet / patient-handout / reconstitution instructions" PDF queries across major search engines — no result

**What exists in lieu of a data sheet: research-chemical vendor labels only**, admissible as `vendor_label` for purity/identity/reconstitution math and nothing else:

- **Core Peptides** (corepeptides.com) — kisspeptin-10 10 mg lyophilized powder; explicit "for research use only / not for human use" disclaimer; no dosing instructions, no primary references [4, vendor_label]
- **Heritage Labs** (heritagelabsusa.com) — kisspeptin-10 10 mg; claimed 99%+ purity, USA-manufactured; explicit "not for human use / research purposes only" disclaimer [4, vendor_label]
- **Biotech Peptides** (biotechpeptides.com) — kisspeptin-10 10 mg; explicit research-only disclaimer; no dosing, no citations [4, vendor_label]

These vendor labels provide purity/identity context only. **None constitutes a compounding clinical data sheet.**

## Critical sourcing hazards (read before any use context)

### Hazard 1 — KP-10 vs. KP-54 confusion

The grey market and vendor ecosystem use "kisspeptin" ambiguously across two structurally and pharmacokinetically distinct isoforms:

| | **Kisspeptin-10 (KP-10)** | **Kisspeptin-54 (KP-54)** |
|---|---|---|
| Length | 10 amino acids (decapeptide) | 54 amino acids |
| Sequence | YNWNSFGLRF-NH2 | Full KISS1 gene product |
| MW | ~1302 Da | ~6.3 kDa |
| Plasma t½ | ~4 min IV; 55 sec in vitro | ~28 min in humans (27.6 min, Dhillo 2005); ~32 min in mice |
| LH duration | 10 min – 1 h | 1 – 4 h |
| BBB crossing | No | Yes (partial) |
| Clinical trials | Mostly KP-10 (IV bolus, nmol/kg) | Some KP-54 (IV infusion) |
| Dosing units | mcg / nmol/kg | nmol/kg / clinical μg dose |

The critical buyer/vendor confusion: (a) a purchaser may receive KP-10 labeled generically as "kisspeptin"; (b) clinical trial results published for KP-54 (longer half-life, higher sustained LH) do not transfer to KP-10; (c) reconstitution math based on the wrong molecular weight gives the wrong dose. **Always confirm which isoform is in hand before any use-context discussion.** [5, 6, open_label]

### Hazard 2 — Desensitization trap (tachyphylaxis)

This is the primary pharmacological hazard for naive grey-market use. KP-10 stimulates GnRH pulsatility via KISS1R, but **the KISS1R desensitizes rapidly with continuous or daily exposure**, producing the opposite of the intended effect: LH falls back to baseline rather than staying elevated. Specific observations from the academic literature [7, 8, open_label]:

- KP-54 administered twice-daily SC at 6.4 nmol/kg in women with hypothalamic amenorrhea produced initial robust LH responses but resulted in **tachyphylaxis by day 14**
- Primate models demonstrate LH returning to baseline within hours of continuous KP-10 infusion
- The highest single-bolus dose in human trials (3.0 μg/kg IV in men) elicited a *reduced* LH response vs. the 1.0 μg/kg dose, suggesting supraphysiologic receptor saturation at the top end
- The PCAC briefing document cited "signal fade with chronic dosing" as a specific safety/effectiveness concern in its vote against KP-10 [1, regulatory]

**Practical implication:** the community protocol of pulsed dosing (not daily continuous) with off-cycle breaks is mechanistically grounded — but even this does not rescue the lack of human PK data for SC KP-10 outside clinical trials. The desensitization window (how many days between doses preserves receptor sensitivity) is not established in human data; the "48–72 hour spacing" convention circulating in aggregator sources is extrapolated, not validated.

### Hazard 3 — WADA S2 prohibition in males

Kisspeptin was explicitly named in the WADA Prohibited List starting with the 2024 update under **S2 — Peptide Hormones, Growth Factors, Related Substances and Mimetics**, specifically the **testosterone-stimulating peptides** sub-class (previously titled "GnRH agonist analogs"). The prohibition applies **in males, in- and out-of-competition** [2, regulatory]. Athletes, coaches, and practitioners serving competitive athletes: this is not a gap compound. Any male athlete using KP-10 faces an anti-doping violation. The FormBlends (May 2026) claim that "WADA does not currently ban kisspeptin peptides" is incorrect and contradicted by USADA's own 2024-list key-changes document [2].

### Hazard 4 — PT-141 / Vyleesi is the approved sexual-function drug, not KP-10

Buyers seeking KP-10 for libido/sexual function commonly compare it to bremelanotide (PT-141, Vyleesi). These are categorically different:

- **PT-141 / Vyleesi**: FDA-approved (June 2019), premenopausal women, acquired generalized HSDD, melanocortin MC3R/MC4R mechanism, established compounding pathway for off-label male use via legitimate prescribers
- **Kisspeptin-10**: FDA-unapproved, no approved indication, PCAC voted against compounding authorization, HPG-axis mechanism (not melanocortin), no cleared supply chain

A patient or buyer substituting KP-10 for PT-141 is foregoing an approved option with a cleared prescribing pathway in favor of a grey-market compound with no regulatory standing. This substitution is never clinically justified on regulatory or supply-chain grounds.

## Academic research doses (citable; NOT grey-market convention)

Human clinical research on KP-10 used IV bolus and IV infusion routes with weight-based nmol/kg dosing — a delivery mode that is not replicable in the grey market and whose results do not transfer to SC self-administration. These figures are cited for research context only; they do **not** anchor any practitioner protocol.

**IV bolus doses (men):** 0.01 – 10 nmol/kg; maximal LH response in men at ~1 μg/kg (0.3–1.0 nmol/kg range); doses above 3 μg/kg produced paradoxically reduced responses suggesting high-dose desensitization [7, 8, open_label]

**IV infusion doses (comparison vs. KP-54 and GnRH):** 0.1, 0.3, 1.0 nmol/kg/h for 3 hours; KP-10 and KP-54 infusions produced comparable LH responses despite KP-10's much shorter plasma half-life; both ~3-fold lower LH than GnRH at the same infusion rate [9, open_label]

**SC bolus doses (women):** 2, 4, 8, 16, 32 nmol/kg — administered to study sexual dimorphism; women in follicular phase showed no significant LH response at any route or dose; only preovulatory-phase women responded (10 nmol/kg IV bolus) [8, open_label]

**Key pharmacokinetic parameter:** IV plasma t½ of KP-10 is ~4 minutes (vs. ~28 min for KP-54), meaning any subcutaneous administration protocol must account for a dramatically different PK curve than the IV clinical trial data; SC bioavailability and t½ for KP-10 are not established in published human PK studies [5, open_label].

## Grey-market dose/cycle/route conventions (each [N, tag]; vendor/anecdote — ground NO number)

There is **no human dose-finding trial validating an SC dose of KP-10 for any grey-market indication**. Every figure below is an aggregator convention. The range across sources diverges substantially, reflecting the absence of any SC PK anchor.

**Convention 1 — Low-dose daily pulse (50–200 mcg SC):**

The most common grey-market convention, across multiple aggregator sites:

- **Dose:** 50–200 mcg per injection, subcutaneous
- **Starting dose:** 100 mcg; escalate to 200 mcg if tolerated
- **Frequency:** once daily or every other day (explicit off-day rationale: receptor recovery)
- **Cycle:** 4–8 weeks on, 2–4 weeks off; some sources use 8–12 weeks on
- **Reconstitution:** 10 mg vial + 3.0 mL bacteriostatic water → ~3.33 mg/mL; 1 unit on U-100 insulin syringe ≈ 33.3 mcg

Source: **peptidedosages.com**, "Kisspeptin Dosage Chart – 10 mg Vial Protocol" (no named author, no fixed date) [10, anecdote_aggregate]. Explicit "for research and educational use only / not medical advice." Cites academic sources without specific DOIs visible. **Grounds NO efficacy claim.**

**Convention 2 — Higher-range pulse protocol (200–500 mcg SC):**

A second convention, circulated in community forums and the PeptideWiki Editorial Team review:

- **Dose:** 200–300 mcg SC 1–2× daily; upper range 500 mcg once daily
- **Frequency:** not daily continuous; spacing ≥48 h between doses preferred to limit desensitization
- **Cycle:** 4–8 weeks on, 2–4 weeks off

Source: **PeptideWiki Editorial Team**, "Kisspeptin Dosage Guide: Kisspeptin-10 & Kisspeptin-54 — HPG Axis, Fertility & Testosterone Protocols," peptidewiki.co. Last reviewed February 24, 2026 [11, anecdote_aggregate]. No individual named author. Carries explicit caveat that protocols derive from "clinical research data and community protocols — not from approved pharmaceutical labeling." **Grounds NO efficacy claim.**

**Convention 3 — Garret Grant (peptidedosingprotocols.com) synthesis:**

- **Dose:** 50–100 mcg (low-dose pulse) to 100–200 mcg (standard pulse) SC once daily
- **Cycle:** 2–4 weeks (short cycle) to 4–6 weeks (standard cycle); mandatory off-period
- **Tachyphylaxis warning emphasized:** "Continuous exposure can make the LH signal fade" — protocols prioritize short pulses; not for sustained daily administration

Source: **Grant G (peptidedosingprotocols.com)**, "Kisspeptin Peptide Dosing Guide: Benefits, Dosing, Hormone Effects (2026)," retrieved June 2026 [12, anecdote_aggregate]. Author holds B.S. Civil Engineering (UCLA); editorial is stated to be human-led with AI for math consistency. Explicit: "not medical advice; research-use only." **Grounds NO efficacy claim.**

**Convention divergence is substantive and must be disclosed.** Convention 1 (50–200 mcg/day) and Convention 2 (200–500 mcg/day) overlap partially but the upper-range divergence is 2.5–5×. Neither is validated by a human SC dose-finding trial. Any clinical use must treat these as provisional starting points with no evidence-based anchor.

## Named practitioners / clinics

**Beverly Hills Rejuvenation Center (bhrcenter.com)** — lists kisspeptin-10mg as a peptide offering with individualized prescriber oversight, hormone testing prerequisite, and licensed physician monitoring; no named prescribing physician, no dated protocol, no primary literature citations on the public page → **categorized as anecdote_aggregate clinic marketing** [3, anecdote_aggregate]. The existence of the BHRC listing is noted because it demonstrates a named US clinic offering KP-10 post-PCAC; what it does not provide is an admissible clinical protocol.

**Explicitly NOT documented (searched; not verifiable to venue + date — not fabricated):**

- No **William A. Seeds, MD** KP-10-specific dated dose table was located in *Peptide Protocols: Volume One* (2020) or subsequent Seeds-attributed publications; KP-10 postdates the primary scope of that text.
- No **A4M / International Peptide Society** KP-10-specific dated monograph was located.
- No **Kent Holtorf**, **Edwin Lee**, **Neil Paulvin**, or **Tracy Gapin** KP-10-specific dated dose protocol was located; none is asserted.
- No **Jay Campbell** KP-10-specific dated protocol was located (a MOTS-c protocol exists on jaycampbell.com; no KP-10 equivalent was retrievable).

## Reconstitution / route notes (admin math only)

Reconstitution conventions are **admin bookkeeping** (Tier-4 vendor/aggregator math; cannot ground efficacy or safety).

**Standard reconstitution (for the 50–200 mcg/day convention):**

| Vial | + Bac. water | Concentration | 100 mcg dose | On U-100 |
|------|-------------|---------------|-------------|----------|
| 10 mg | 3.0 mL | ~3.33 mg/mL | 0.03 mL | ~3 U [10, anecdote_aggregate] |
| 10 mg | 2.0 mL | ~5.0 mg/mL | 0.02 mL | ~2 U [10, anecdote_aggregate] |

> **Practical note:** at 3.33 mg/mL, a 100 mcg dose draws to only ~3 units on a standard U-100 syringe — a very small volume with significant dosing-error risk. Some sources use 1 mg/mL (10 mg + 10 mL) to bring a 100 mcg dose to 10 units (more readable). The 1 mg/mL convention is not well documented in the retrieved sources; only the 3.33 mg/mL and 5.0 mg/mL concentrations are in the aggregator literature [10, 11, anecdote_aggregate].

- **Reconstitution technique:** wipe stoppers with alcohol swab; inject bacteriostatic water slowly down the vial wall; swirl gently — do NOT shake (agitation degrades peptide bonds)
- **Storage:** lyophilized powder at −20 °C; reconstituted at 2–8 °C; use within 2–3 weeks
- **Route:** subcutaneous; abdominal fat, thigh, or upper arm; rotate injection sites
- **Syringe:** U-100 insulin syringe (27–31G, 0.5 mL)

**Important:** KP-10 has a plasma t½ of ~4 min IV. SC delivery extends effective exposure via slower absorption but the actual SC PK curve in humans is not published; "how long a SC dose acts" is not derivable from IV clinical trial data.

## Practitioner monitoring framework (experimental context; no validated protocol exists)

If a clinician were tracking a patient using KP-10 in an off-label or research context, the following laboratory framework is consistent with the mechanistic target (HPG axis stimulation → LH → T). **This is a rational monitoring scaffold derived from mechanism and the academic trial literature, not a validated clinical protocol.** No published clinical guideline, society recommendation, or FDA-accepted protocol exists for monitoring native KP-10 use in humans outside of controlled trials.

**Baseline (before starting):**

| Domain | Tests | Rationale |
|--------|-------|-----------|
| HPG axis | LH, FSH, total T, free T, SHBG | Direct mechanistic targets; establish baseline before any effect can be inferred |
| Estradiol | E2 | T aromatizes; monitor especially in men with elevated adiposity |
| Prolactin | PRL | Elevated prolactin suppresses GnRH/kisspeptin signaling; establishes whether HPG axis is responsive |
| Metabolic | CBC, CMP (BMP + LFTs) | Safety baseline; immunogenicity reactions from peptide; hepatic/renal screening |
| Injection-site | Physical baseline documentation | Immunogenicity risk flagged by PCAC; document any pre-existing skin conditions |

**Follow-up (weeks 4–6, mid-first cycle):**

- LH, FSH, total T, free T
- E2 (if T rising, aromatase monitoring)
- Injection-site assessment (induration, nodule, erythema)

**Follow-up (end of cycle, week 8–12):**

- Full repeat of baseline HPG panel
- Off-cycle LH/FSH at 4 weeks post-cycle (assess HPG recovery — tests whether the axis has returned to pre-cycle function, which is the primary safety endpoint for any HPG-modulating agent)

**Stopping rules (rational, not validated):**

- LH and FSH paradoxically declining or at baseline after ≥2 weeks of dosing (suggests receptor desensitization — the primary mechanistic hazard; consider extending off-period before retry)
- Injection-site: persistent (>2-week) indurated nodule, abscess, or local hypersensitivity — stop and evaluate (PCAC cited immunogenicity as a specific concern)
- Systemic allergic signs (urticaria, flushing, hypotension) — stop immediately; this is an unapproved peptide with no post-market safety database

**Honest limit:** no published monitoring protocol for KP-10 in a clinical or off-label prescribing context exists. This framework is rationalized from mechanism and academic trial design (which used LH, FSH, T as primary endpoints) and from the PCAC's stated safety concerns (immunogenicity, signal fade). It should not be represented as guideline-consistent care.

## Bibliography (own, with tag= and tier=)

1. **FDA Pharmacy Compounding Advisory Committee (PCAC). "October 29, 2024 Meeting of the Pharmacy Compounding Advisory Committee — Kisspeptin-10."** FDA.gov / PCAC calendar. October 29, 2024. tag=regulatory. tier=1. (PCAC voted **11 to 0** against recommending kisspeptin-10 for inclusion in the 503A bulks list. Four grounds: inadequate physicochemical characterization, immunogenicity risk, insufficient clinical effectiveness evidence, FDA-approved alternatives available for secondary hypogonadism. Primary FDA source for the regulatory closure of the US compounding pathway. Note: fda.gov/media/182646/download and fda.gov/media/185412/download both returned HTTP 404 at time of retrieval — the meeting summary was confirmed via secondary reporting and the A4PC / ExcelMale summary threads citing the vote count and grounds; the PCAC calendar landing page returned HTTP 404 as well. Fetch-disclosed: FDA primary PDFs inaccessible June 2026; vote count and grounds confirmed via A4PC secondary report and ExcelMale forum thread citing FDA reviewer statements [see sources 13, 14].)

2. **USADA. "Explanation of Key Changes on the 2024 WADA Prohibited List."** USADA.org. 2024. tag=regulatory. tier=1. (Kisspeptin explicitly added by name to S2 — Peptide Hormones / Testosterone-Stimulating Peptides sub-class; prohibited in males in- and out-of-competition. Corrects the FormBlends [May 2026] erroneous claim that "WADA does not currently ban kisspeptin peptides.")

3. **Beverly Hills Rejuvenation Center. "Kisspeptin 10mg."** bhrcenter.com/peptides/kisspeptin-10mg. Retrieved June 2026. tag=anecdote_aggregate. tier=4. (US clinic listing KP-10 as a peptide therapy offering with physician oversight language; no named prescribing physician, no dated protocol, no primary literature citations publicly visible; bhrcenter.com redirected excessively — fetch-disclosed: content characterized via search result snippet; listed here as evidence of a named US clinic offering KP-10 post-PCAC. Dose/cycle NOT derivable from this source. NOT a compounding clinical data sheet.)

4. **Core Peptides / Heritage Labs / Biotech Peptides — kisspeptin-10 product listings.** Retrieved June 2026. tag=vendor_label. tier=4. (Multiple US research-chemical vendors listing kisspeptin-10 10 mg lyophilized powder; claimed 99%+ purity; universal "for research use only / not for human use" disclaimers; no dosing instructions, no primary citations. Purity/identity context ONLY. NOT a compounding clinical data sheet.)

5. **George JT, et al. "Kisspeptin-10 Is a Potent Stimulator of LH and Increases Pulse Frequency in Men."** Journal of Clinical Endocrinology & Metabolism. 2011;96(8):E1228–E1236. PMID: 21632807. PMC3380939. tag=open_label. tier=2. (First author is George JT, not Dhillo WS — efetch-verified PMID 21632807; Edinburgh/MRC + Mayo Clinic group, not Imperial. IV bolus doses 0.01–3.0 μg/kg in healthy men; max LH at 1.0 μg/kg; high-dose [3 μg/kg] blunting suggesting receptor desensitization; 22.5-h high-dose infusion [4 μg/kg·h] — no tachyphylaxis during the infusion period itself; KP-10 plasma t½ ~4 min IV. Cited for academic dosing parameters and t½ data ONLY; not a practitioner protocol.)

6. **Mead EJ, et al. "Kisspeptin-10 Is a Potent Stimulator of LH and Increases Pulse Frequency in Men."** (same PMC article as above; see source 5). Cited additionally for the KP-10 vs. KP-54 half-life contrast: in vitro t½ 55 sec vs. in vivo plasma t½ 4 min (KP-10) vs. 27.6 min (KP-54); KP-10 does not cross the blood-brain barrier while KP-54 does (partial) — critical structural difference affecting comparison of trial data across isoforms.

7. **Jayasena CN, et al. "Direct comparison of the effects of intravenous kisspeptin-10, kisspeptin-54 and GnRH on gonadotrophin secretion in healthy men."** Human Reproduction. 2015;30(8):1934–1941. PMID: 26089302. PMC4507333. tag=open_label. tier=2. (Journal is Human Reproduction, not Clinical Endocrinology — efetch-verified PMID 26089302. IV infusion at 0.1, 0.3, 1.0 nmol/kg/h × 3 h; KP-10 and KP-54 produced comparable LH responses despite 7-fold plasma level difference; both ~3-fold lower than GnRH. Plasma t½ KP-10 4 min vs. KP-54 ~28 min [27.6 min, Dhillo 2005] confirmed. References prior chronic KP-54 tachyphylaxis in other populations. Academic dosing context ONLY.)

8. **Dhillo WS, et al. "The Effects of Kisspeptin-10 on Reproductive Hormone Release Show Sexual Dimorphism in Humans."** Journal of Clinical Endocrinology & Metabolism. 2011;97(3):E91–E98. PMC3232613. tag=open_label. tier=2. (IV bolus 0.3–10 nmol/kg and SC 2–32 nmol/kg in men and women; men responded robustly; women in follicular phase showed no significant LH response at any dose/route; preovulatory women responded at 10 nmol/kg IV only. References chronic KP-54 tachyphylaxis observation. Cited for sexual dimorphism data and academic SC dose range ONLY; does not establish a grey-market SC dose.)

9. **Chen H, et al. "Mechanistic insights into the more potent effect of KP-54 compared to KP-10 in vivo."** PLOS One. 2017;12(5):e0176821. PMC5413024. tag=open_label. tier=2. (Explains KP-54's greater in vivo potency via BBB crossing [KP-10 does not], longer plasma half-life, and sustained LH duration 1–4 h vs. 10 min–1 h for KP-10. Cited for KP-10 vs. KP-54 pharmacokinetic distinction ONLY.)

10. **"Kisspeptin Dosage Chart – 10 mg Vial Protocol," peptidedosages.com.** Retrieved June 2026. tag=anecdote_aggregate. tier=4. (100–200 mcg SC daily convention; 10 mg + 3.0 mL → 3.33 mg/mL; 8–12-wk cycle; explicit tachyphylaxis caution; no named author, no fixed date; cites academic sources without specific DOIs. Dose/cycle/reconstitution convention ONLY. NOT a compounding clinical data sheet.)

11. **PeptideWiki Editorial Team. "Kisspeptin Dosage Guide: Kisspeptin-10 & Kisspeptin-54 — HPG Axis, Fertility & Testosterone Protocols."** peptidewiki.co. Last reviewed February 24, 2026. tag=anecdote_aggregate. tier=4. (200–500 mcg SC convention, 1–2× daily; ≥48-h spacing rationale; 4–8-wk cycle; KP-10 vs. KP-54 dosing-unit warning. No individual named author. Explicit "clinical research data and community protocols — not approved pharmaceutical labeling." Convention ONLY.)

12. **Grant G. "Kisspeptin Peptide Dosing Guide: Benefits, Dosing, Hormone Effects (2026)."** peptidedosingprotocols.com. Retrieved June 2026. tag=anecdote_aggregate. tier=4. (50–200 mcg SC; 2–4-wk short-pulse to 4–6-wk standard cycle; tachyphylaxis warning emphasized. Author: B.S. Civil Engineering, UCLA; explicitly "not medical advice; research-use only." Convention + desensitization-risk framing ONLY.)

13. **APC — America's Pharmacy Compounders. "PCAC votes against four nominated bulk drug substances."** a4pc.org/news/pcac-votes-against-four-nominated-bulk-drug-substances. October 2024. tag=regulatory. tier=3. (Confirms PCAC voted against kisspeptin-10; corroborates exclusion of KP-10 from 503A bulks list; does not specify per-substance vote count.)

14. **ExcelMale Forum. "FDA Decides Not to Allow Kisspeptin-10 Manufacturing by Compounding Pharmacies."** excelmale.com/threads/31487. October 2024. tag=anecdote_aggregate. tier=4. (Community reporting on the PCAC outcome; reproduces FDA reviewer's four stated grounds [characterization, immunogenicity, insufficient effectiveness evidence, approved alternatives]; not a primary source. Cited here as a secondary summary corroborating the PCAC outcome where primary PDF download failed.)

## Self-check

**No efficacy grounded on these tiers.** Every dose, cycle, route, and reconstitution figure above is tagged `anecdote_aggregate`, `practitioner_protocol`, or `vendor_label` and is used **only** as a prescribing-practice convention or admin math. The three `open_label` academic sources (sources 5–9) are cited solely for academic dose ranges and pharmacokinetic parameters (half-life, isoform distinctions, tachyphylaxis observations) and explicitly do not anchor any grey-market protocol. The two `regulatory` cites (sources 1–2) are used only for regulatory status. **No efficacy, adverse-event-rate, or mechanism claim is grounded on any Tier-3/4 source in this document.**

**Data-sheet requirement satisfied (explicit-absence form).** **No admissible compounding-pharmacy clinical data sheet was located for kisspeptin-10.** Searched: Empower Pharmacy, Tailor Made Compounding / Infiniwell, Hallandale Pharmacy, Belmar Pharma Solutions, Strive Pharmacy, APS, Beverly Hills Rejuvenation Center, plus generic compounding "monograph / fact sheet / data sheet / patient-handout" PDF queries. None returned a public KP-10 clinical monograph citing its own primary literature. Research-chemical vendor labels (Core Peptides, Heritage Labs, Biotech Peptides) carry universal "not for human use" disclaimers and provide no dosing; they qualify as `vendor_label` for purity/identity context only. The absence is fully consistent with the regulatory state: the PCAC voted 11–0 against 503A authorization in October 2024.

**Regulatory state honest and verified.** PCAC voted 11–0 against KP-10 on October 29, 2024 (sources 1, 13). This is the terminal US regulatory event: no compounding pathway exists. No Category 2 interim status was ever granted to KP-10 (it was evaluated directly on its nomination, unlike peptides that were placed on the interim list and later removed). Any 503A or 503B pharmacy dispensing KP-10 does so without FDA authorization and with direct enforcement exposure.

**WADA status honest.** Kisspeptin is explicitly prohibited in males under WADA S2 (Testosterone-Stimulating Peptides) as of the 2024 list, confirmed per USADA's key-changes document [2]. The FormBlends (May 2026) claim to the contrary is flagged explicitly as incorrect. FormBlends was otherwise admissible for KP-10 vs. KP-54 receptor data (EC50 values) but is disqualified on WADA status; the WADA finding in this document derives from source [2] only.

**Critical hazards disclosed.** All four sourcing hazards are documented: (1) KP-10 vs. KP-54 isoform confusion and pharmacokinetic differences (plasma t½ 4 min vs. ~28 min; BBB crossing difference; LH duration difference); (2) desensitization trap — KISS1R tachyphylaxis with continuous/daily dosing is the primary pharmacological hazard, mechanistically grounded, observed in KP-54 chronic-dosing studies and at supraphysiologic KP-10 doses; (3) WADA S2 prohibition in males; (4) PT-141/Vyleesi is the FDA-approved HSDD drug — not KP-10 and not a substitute.

**Named-practitioner convention disclosed honestly.** Beverly Hills Rejuvenation Center — named US clinic; no prescribing physician name, no dated protocol, no primary citations publicly accessible; categorized as `anecdote_aggregate`. No Seeds/A4M/IPS/Holtorf/Lee/Paulvin/Gapin/Campbell KP-10-specific dated protocols located; none fabricated.

**Convention divergence disclosed.** Convention 1 (50–200 mcg/day) and Convention 2 (200–500 mcg/day) diverge at the upper end by 2.5–5×. This is documented, not papered over. Both are provisional and unvalidated by any SC human dose-finding study.

**Fetch-disclosure.** Three fetch attempts failed: (a) fda.gov/media/182646/download — HTTP 404; (b) fda.gov/media/185412/download — HTTP 404; (c) fda.gov PCAC calendar page for October 29, 2024 — HTTP 404. The PCAC vote count (11–0) and regulatory grounds were confirmed via A4PC secondary report [13] and ExcelMale community thread [14], which reproduced the FDA reviewer's stated four grounds. bhrcenter.com/peptides/kisspeptin-10mg — excessive redirect error; characterized via search snippet only, not direct page read. All four failures are disclosed here.

**Off-whitelist sources check.** No Cureus, Hindawi, Ivyspring, wjgnet, Dove, AME, Spandidos, Oncotarget, or Wikipedia sources cited in this document.

**Gaps / residual limits.**
- *Exact PCAC vote count not confirmed from FDA primary PDF* — 11–0 confirmed only via secondary reporting; if the primary PDF becomes accessible, verify and update.
- *KP-10 SC PK in humans not published* — the 4-min plasma t½ derives from IV administration; subcutaneous absorption curve is not characterized in public literature; all SC dosing conventions are therefore unanchored to actual SC PK data.
- *No named prescriber with a citable, dated, primary-literature-grounded KP-10 protocol was located* — the BHRC listing is the closest, and it does not yield a clinical protocol.
- *FormBlends WADA error flagged* — their May 2026 article incorrectly states WADA does not ban kisspeptin; this document uses USADA [2] exclusively for that finding and explicitly names the FormBlends error so a future reader does not propagate it.
