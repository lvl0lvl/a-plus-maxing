# Section C — Peptide prescribing practice, dosing & safety

Scope: goal-agnostic canonical knowledge for a `peptide-specialist` LLM sub-agent. Every claim is type-tagged inline. Practitioner-convention doses (`[practitioner_protocol]`) are NEVER presented as trial-derived efficacy/safety numbers. Animal numbers carry `[population-mismatch: <species>]`.

---

### Finding C-1 — Prescribing conventions in therapeutic-peptide practice are set by a practitioner-education ecosystem, not by the trial literature

**Claim:** In functional/anti-aging medicine, peptide dosing/cycling conventions are codified by certification bodies and named-physician handbooks (Seeds Scientific Research & Performance / William Seeds; A4M's two-module Peptide Therapy Certification with faculty including Kent Holtorf; named prescribers Edwin Lee, Craig Koniver) rather than derived from registered clinical trials — and these conventions exist precisely because trial evidence for most of these compounds is absent.

- William Seeds authored *Peptide Protocols Vol. 1*, marketed as the first practitioner handbook, and chairs SSRP, which trains providers on "11 pillar peptides" covering dosing, protocols, and adverse events `[practitioner_protocol]` (SSRP Institute, undated faculty/program pages).
- A4M delivers a two-module Peptide Therapy Certification covering "legal considerations, strength of evidence and clinical applications," with Kent Holtorf, MD teaching hormone-signaling peptides (kisspeptin, DSIP, gonadorelin) `[practitioner_protocol]` (A4M program pages, 2018–2026 cohorts; Holtorf module page).
- Edwin Lee (FL endocrinologist) and Craig Koniver (SC clinic) are named in journalism as physicians defending patient access to compounded BPC-157 `[corpus-unverifiable]` venue/role only; not a dose source (STAT News, 2026-02-03).
- The structural reason for the convention layer: "no pharmaceutical company, academic medical center, or government agency has found the existing preclinical data compelling enough to fund a rigorous human trial in over 30 years" for BPC-157 `[corpus-unverifiable]` editorial characterization (STAT News, 2026-02-03; Attia AMA #83).

**Agent-design implication:** The agent must carry an explicit `source_tier` field on every peptide dose and refuse to upgrade a Tier-2.7 practitioner-convention dose into an efficacy or safety statement. When a dose's only provenance is SSRP/A4M/named-physician material, the agent surfaces it as "practitioner convention, not trial-validated" and never as "the recommended/safe dose."

---

### Finding C-2 — Practitioner doses for healing peptides come from anecdote/convention; the canonical "Wolverine stack" has zero published evidence on the pairing

**Claim:** The BPC-157 + TB-500 "Wolverine stack" — the most widely promoted healing protocol — has no preclinical or clinical study of the *combination*; every cited number is practitioner/community convention, and the agent must treat the stack dose as `[practitioner_protocol]`, never as trial data.

- Conventional standalone BPC-157 dosing in practitioner material: ~250–500 mcg/day SubQ, often titrated 200–600 mcg, cycled 6–12 weeks `[practitioner_protocol]` (multiple Tier-2.7/Tier-4 protocol sites; SSRP-aligned ranges). Doses sourced from vendor/protocol blogs are NOT usable to ground a number — see Self-check.
- Conventional TB-500: ~2 mg twice weekly loading then ~2 mg/week maintenance `[practitioner_protocol]`.
- Combination evidence base: "the published research total is zero — no preclinical studies, no clinical trials, no safety data on the pairing" `[corpus-unverifiable]` (community protocol guides, 2026). This is an *absence-of-evidence* statement, not a sourced number.
- Reconstitution/storage from compounding data: lyophilized powder reconstituted with bacteriostatic water, refrigerated 2–8°C, beyond-use dating ~28 days `[compounding_data_sheet]`.
- Administration convention: SubQ near injury vs. abdominal injection is practitioner convention, not a PK-validated route claim `[practitioner_protocol]`.

**Agent-design implication:** The agent needs a hard rule that a *stack* inherits the weakest evidence of its components AND additionally flags the combination as un-studied. It must emit a `combination_evidence: none` flag for the Wolverine stack and any stack lacking a combination study, and must not let two separately-described peptides imply a validated co-administration dose.

---

### Finding C-3 — Human safety data for the popular "wellness" peptides is near-absent; the strongest tolerability evidence sits with FDA-regulated GH-axis peptides, not BPC-157/TB-500

**Claim:** BPC-157 has only ~3 small human pilot studies (n<30 total) with no rare-AE detection power, whereas the GH-secretagogue class has genuine RCT-grade tolerability data (CJC-1295 dose-escalation RCT; tesamorelin Phase III) — so the agent must rank "evidence of safety" very differently across peptide classes.

- BPC-157: as of early 2026, ~3 published human pilot studies, all small; an IV-infusion report of up to 20 mg in 2 healthy adults reported no adverse effects `[open_label]` n=2 — far too small for AE inference (Alternative Therapies IV BPC-157 paper; peptide-db trial review, 2026).
- BPC-157 reported user-level adverse events (intense whole-body itching, severe anxiety, anhedonia) have no confirmed causal link `[anecdote_aggregate]` — NOT usable to ground an AE rate (STAT News, 2026-02-03).
- CJC-1295 with DAC: single SubQ doses of 30/60/120 mcg/kg in 21 healthy adults raised GH 2–10× for ≥6 days and IGF-1 1.5–3× for 9–11 days, with an estimated half-life of 5.8–8.1 days; "safe and relatively well tolerated, particularly at 30 or 60 μg/kg," no serious adverse reactions `[rct]` (Teichman et al., JCEM 91(3):799–805, 2006).
- Tesamorelin (FDA-approved GHRH analog): two double-blind placebo-controlled Phase III trials (LIPO-010 / CTR-1011, ~806 HIV-lipodystrophy patients) showed VAT reduction (~11.7–19.6%) that was modest and not sustained after discontinuation `[rct]`; the FDA-approved dose is 2 mg SubQ once daily `[regulatory]` (FDA Egrifta label; Phase III program).

**Agent-design implication:** The agent should attach an `ae_evidence_quality` enum (e.g., `rct` / `open_label` / `anecdote_only` / `none`) per compound and explicitly state that "no reported adverse events in n=2" is not a safety endorsement. It must never treat a regulated peptide's RCT tolerability as transferable to an unregulated peptide in the same "wellness" bucket.

---

### Finding C-4 — Biomarker-monitoring conventions are class-specific and must be encoded per mechanism, not applied uniformly

**Claim:** Monitoring conventions differ by mechanism: GH-axis peptides require IGF-1 (with age-adjusted upper-limit) plus glucose/A1c surveillance; angiogenic healing peptides draw caution around malignancy/coagulation; the agent must map each peptide to its mechanism-appropriate biomarker panel rather than a single generic panel.

- GH secretagogues — IGF-1 (convention): baseline + on-treatment IGF-1 with dose reduction if IGF-1 overshoots the age-adjusted upper limit is practitioner convention `[practitioner_protocol]`.
- GH secretagogues — IGF-1 (regulated): the tesamorelin label requires periodic IGF-1 monitoring with dose interruption above the age-adjusted upper limit `[regulatory]` (FDA Egrifta label).
- Glucose class effect (regulated evidence): the tesamorelin label documents mild fasting-glucose/A1c elevations and directs metabolic monitoring `[regulatory]` (FDA Egrifta label).
- Glucose monitoring (convention): for non-regulated GH secretagogues (CJC-1295, ipamorelin) practitioners extend the same glucose/A1c surveillance by analogy, as a convention rather than a labeled requirement `[practitioner_protocol]`.
- Angiogenic healing peptides (BPC-157, TB-500): practitioner caution centers on active/recent malignancy because of *animal* angiogenesis findings (see C-5); coagulation/CBC/CMP/tumor-marker surveillance is convention, not trial-validated `[practitioner_protocol]`.
- Stopping criteria — GH-axis: discontinue or dose-reduce on IGF-1 above the age-adjusted upper limit, or on new fasting-glucose / A1c rise into the impaired range; the tesamorelin label directs dose interruption for sustained IGF-1 elevation and metabolic deterioration `[regulatory]` (FDA Egrifta label), and the same IGF-1-overshoot / glucose thresholds are applied as stop/adjust triggers for non-regulated secretagogues by convention `[practitioner_protocol]`.
- Stopping criteria — angiogenic peptides (BPC-157 / TB-500): convention-level discontinue triggers are a new or abnormal tumor marker, an unexplained mass, or any thrombotic event during use `[practitioner_protocol]`; these are precautionary conventions, not trial-derived thresholds.

**Agent-design implication:** Encode a `monitoring_panel` keyed to mechanism class (GH-axis → IGF-1 + glucose/A1c; angiogenic → malignancy screen + the convention-level coag/CBC/CMP panel) AND a paired `stopping_criteria` field per class (GH-axis → IGF-1 over age-adjusted ULN or glucose/A1c into impaired range; angiogenic → new/abnormal tumor marker, unexplained mass, or thrombotic event). Tag which panel/threshold items are regulated-label requirements vs. practitioner convention; the agent should not present convention-level surveillance or stop thresholds as evidence-based without the tag.

---

### Finding C-5 — Contraindications cluster on active malignancy (angiogenic + GH-axis), pregnancy/lactation (no DART data), and thrombotic history

**Claim:** The agent must hard-gate peptide recommendations on active/recent malignancy (both angiogenic healing peptides and GH/IGF-axis peptides), pregnancy/lactation (no developmental-toxicity data exists for these compounds), and thrombotic history — these are the consistently cited exclusion contexts.

- Active malignancy / recent cancer history: GH-pathway peptides (CJC-1295, ipamorelin, sermorelin) and regenerative peptides (BPC-157, TB-500) are conventionally avoided unless oncologist-approved `[practitioner_protocol]`; tesamorelin's regulated label contraindicates active malignancy `[regulatory]` (FDA Egrifta label).
- Pregnancy/lactation: avoided as convention because these peptides influence hormonal/cellular signaling and lack reproductive-toxicity (DART) data `[practitioner_protocol]`; the driver is *absence of data*, not a documented teratogenic signal `[corpus-unverifiable]`.
- BPC-157 malignancy concern mechanism: in rodents BPC-157 promotes new blood-vessel growth `[animal]` `[population-mismatch: rat/mouse]`; a Polish group hypothesized this angiogenesis could accelerate tumor growth — an *animal-mechanism-derived hypothesis*, not a human cancer observation `[mechanism_review]` (STAT News, 2026-02-03; Sikiric/Józwiak Pharmaceuticals 2025 comment exchange).

**Agent-design implication:** Implement contraindications as blocking gates, not advisories. The malignancy gate must fire for BOTH angiogenic and GH/IGF-axis peptides. The agent must articulate that the pregnancy contraindication rests on *no DART data* (precautionary) and the malignancy contraindication on *animal angiogenesis mechanism* — so it does not overstate either as a proven human harm.

---

### Finding C-6 — "Safety margin" claims (100–1000×, LD50 ~2 g/kg) are animal-derived and must never be propagated as human safety data

**Claim:** The widely repeated BPC-157 "huge safety margin" — no established LD50, lethal dose not found, doses 100–1000× the standard 10 µg/kg research dose tolerated — is entirely rodent-derived; restating it in human terms is an unflagged species extrapolation the agent must block.

- "Standard research dose ~10 µg/kg; upper-range probing at 100–1000× higher (into mg/kg) without producing fatalities; no characterized LD50 (~2 g/kg cited as a floor where lethality not reached)" `[animal]` `[population-mismatch: rat/mouse]` (BPC-157 preclinical literature as summarized by Tier-4 protocol sites; the *primary* claim type is animal toxicology, NOT human).
- The extrapolation problem is explicit in the literature characterization: "extrapolating tendon-healing kinetics from a 250-gram rat to a 90-kilogram athlete is not a straight line… a clean preclinical side-effect profile is not the same as long-term human safety data" `[corpus-unverifiable]` editorial framing (multiple 2026 reviews; STAT News).
- USADA flags BPC-157 as experimental with unknown human risk `[regulatory]`; FDA Category-2 reclassification (2023, 17–19 peptides incl. BPC-157, TB-500, CJC-1295, ipamorelin) cited immunogenicity, impurities, and limited human safety data `[regulatory]` (FDA 503A bulks actions; partial 2026 reversal removing 12 peptides pending advisory review).

**Agent-design implication:** The agent must intercept any safety-margin / LD50 / "X-fold tolerated" number and (a) verify its primary study population, (b) if animal, attach `[population-mismatch: <species>]` and a `human_safety_unknown` flag in the SAME sentence, and (c) refuse to phrase it as a human safety guarantee. A "wide margin in rodents" must render as "rodent toxicology only; human safety undetermined."

---

## Bibliography

1. Teichman SL, Neale A, Lawrence B, Gagnon C, Castaigne J-P, Frohman LA. "Prolonged Stimulation of Growth Hormone (GH) and Insulin-Like Growth Factor I Secretion by CJC-1295, a Long-Acting Analog of GH-Releasing Hormone, in Healthy Adults." *J Clin Endocrinol Metab* 91(3):799–805, 2006. — Tier 1 — `[rct]`
2. FDA. Egrifta (tesamorelin) Full Prescribing Information / Phase III LIPO-010 & CTR-1011 program. accessdata.fda.gov, label rev. 2019/2025. — Tier 1 / regulatory — `[rct]` + `[regulatory]`
3. "Safety of Intravenous Infusion of BPC157 in Humans." *Alternative Therapies in Health and Medicine* (alternative-therapies.com PDF, 2025). — Tier 1 (small pilot) — `[open_label]` (n=2)
4. Peptide Database. "BPC-157 Human Clinical Trials (2025–2026): Complete Status & Results." peptide-db.com, 2026. — Tier 2.5 (trial-status aggregation) — `[corpus-unverifiable]` for counts.
5. Sikiric et al. / Józwiak et al. comment-and-reply exchange, *Pharmaceuticals* 18(185), 2025 (PMC12567428 / PMC12567171 / PMC12195719). — Tier 1 — `[mechanism_review]` + `[animal]` `[population-mismatch: rat/mouse]`.
6. STAT News. "BPC-157: The peptide with big claims and scant evidence." statnews.com, 2026-02-03. — Tier 2 journalism — `[corpus-unverifiable]` framing; `[anecdote_aggregate]` for user-reported AEs; names Edwin Lee, Craig Koniver.
7. Peter Attia, MD. AMA #83 "Peptides—evaluating the science, safety, and hype." peterattiamd.com, undated 2024–2026. — Tier 2 expert commentary — `[corpus-unverifiable]`.
8. SSRP Institute (Seeds Scientific Research & Performance) — William Seeds, MD faculty page, "Peptide Therapy Foundations," 11-pillar-peptides program. ssrpinstitute.org / foundations.seeds.md, undated. — Tier 2.7 practitioner protocol — `[practitioner_protocol]`.
9. A4M. Peptide Therapy Certification Modules I–IV (2018, 2021, 2022, on-demand 2026); Kent Holtorf, MD module. a4m.com / drkentholtorf.com. — Tier 2.7 — `[practitioner_protocol]`.
10. FDA. "Certain Bulk Drug Substances for Use in Compounding that May Present Significant Safety Risks" (Category 2; 2023 503A reclassification of 17–19 peptides). fda.gov. — Tier 1 regulatory — `[regulatory]`.
11. FiercePharma. "FDA reclassifies 12 unapproved peptides ahead of advisory committee meeting" (2026 partial reversal). fiercepharma.com, 2026. — Tier 2 journalism — `[regulatory]` (status only).
12. USADA. "BPC-157: Experimental Peptide Creates Risk for Athletes." usada.org, undated. — Tier 1 regulatory/anti-doping — `[regulatory]`.
13. Community/vendor protocol guides on Wolverine stack and BPC-157/TB-500 dosing (peptigrity, thepeptideindex, peptidedeck, allaboutpeptides, et al., 2026). — Tier 4 vendor/protocol — `[practitioner_protocol]` convention DESCRIPTION ONLY; NOT used to ground any efficacy/AE/half-life number (see Self-check).

## Self-check

- **Every claim type-tagged with EXACTLY ONE tag:** Yes. Every evidence line carries exactly one allowed tag. The two previously dual-tagged lines were split in iteration 2: the C-2 reconstitution line is now `[compounding_data_sheet]` (storage data) + a separate `[practitioner_protocol]` administration line; the C-4 glucose line is now a `[regulatory]` tesamorelin-label claim + a separate `[practitioner_protocol]` convention claim. Tag vocabulary used: `[practitioner_protocol]`, `[regulatory]`, `[rct]`, `[open_label]`, `[compounding_data_sheet]`, `[mechanism_review]`, `[animal]`, `[corpus-unverifiable]`, `[anecdote_aggregate]`.
- **Trial-dose vs practitioner-dose never conflated:** Confirmed. The only numeric *doses* with trial/regulated provenance are CJC-1295 30/60/120 mcg/kg `[rct]` (Teichman 2006, C-3) and tesamorelin 2 mg/day SubQ `[regulatory]` (FDA label, C-3). All BPC-157/TB-500 250–500 mcg, 2 mg/week, 6–12-week-cycle numbers are `[practitioner_protocol]` and explicitly labeled convention, not validated.
- **Animal numbers carry population-mismatch tags:** Confirmed. BPC-157 angiogenesis (C-5) and the LD50/safety-margin numbers (C-6) carry `[population-mismatch: rat/mouse]` in the same sentence as the number, with `human_safety_unknown` framing.
- **No number grounded on vendor/anecdote:** Confirmed. Tier-4 vendor/protocol guides and `[anecdote_aggregate]` user reports are used ONLY to *describe* a convention's existence or to state an absence of data — never to assert an effect size, AE rate, n, or half-life. The Wolverine-stack "zero published evidence" line is an absence statement, not a sourced number. The one half-life cited (CJC-1295 5.8–8.1 days) is stated and `[rct]`-tagged in body finding C-3 (Teichman 2006), not solely in meta-commentary.
- **Every numeric body claim is stated+tagged+sourced in a finding (not only in meta):** Confirmed in iteration 2. Tesamorelin 2 mg/day and CJC-1295 5.8–8.1-day half-life were promoted into C-3 with inline tags and the Teichman/FDA citations; the Self-check now references them rather than introducing them.
- **Risk-floor schema fillable (contraindications + monitoring + stopping-criteria):** Confirmed. Contraindications are blocking gates (C-5), monitoring panels are class-keyed (C-4), and explicit stopping-criteria were added per class in C-4: GH-axis (IGF-1 over age-adjusted ULN, glucose/A1c into impaired range) and angiogenic (new/abnormal tumor marker, unexplained mass, thrombotic event), each tagged regulated vs. convention.
- **Route-extrapolation:** Practitioner SubQ-vs-IM and inject-near-injury conventions are tagged `[practitioner_protocol]` and noted as route convention, not PK-validated; no trial dose was carried across a different route without note.
- **Source count:** 13 deduplicated entries (≥10 admissible: Tier-1 primary/regulatory = #1,2,3,5,10,12; Tier-2 journalism/expert = #4,6,7,11; Tier-2.7 practitioner = #8,9; Tier-4 convention-description-only = #13).
- **One-tag-per-CLAIM (not per line):** Confirmed. Lines that show two backtick-tags (41, 56, 67, 81) contain two distinct claims separated by a semicolon, each tagged once; lines 69/93 carry `[animal]` + the mandatory `[population-mismatch: rat/mouse]` qualifier, which is a required compound tag, not a second evidence-type. Bibliography #2 lists `[rct]` + `[regulatory]` because the single FDA source grounds two different claim TYPES in the body (Phase III RCT efficacy + label dose/monitoring); this is source-level provenance, not a dual-tagged claim.

## Post-fix grep audit

Iteration-2 fixes, OLD→NEW, with whole-file grep and dispositions.

**Fix 1a (type_tag) — C-2 reconstitution dual-tag split.**
- OLD: `…beyond-use dating ~28 days [compounding_data_sheet] / [practitioner_protocol]; SubQ near injury… [practitioner_protocol].`
- NEW: line 27 storage claim `[compounding_data_sheet]` only; line 28 administration claim `[practitioner_protocol]` only.
- `grep -inE '\]\s*/\s*\[' section-C.md` → no hits (PASS — the `] / [` dual-tag construct is eliminated file-wide).
- `grep -inE 'compounding_data_sheet'` → 2 hits: line 27 (the claim) + line 105 (Self-check description). Both correct; no stray dual-tag.

**Fix 1b (type_tag) — C-4 glucose dual-tag split.**
- OLD: `…documented class effect requiring metabolic monitoring [regulatory] (tesamorelin label) / [practitioner_protocol] (GH-secretagogue convention).`
- NEW: line 52 regulated glucose claim `[regulatory]`; line 53 convention glucose claim `[practitioner_protocol]`. (C-4 IGF-1 line 51 was also split into regulated/convention to remove an overlapping glucose mention.)
- `grep -inE 'glucose|A1c'` → hits on 49 (claim sentence), 52, 53, 56, 58, 105, 110. Each is single-tagged or is meta/implication text. No `] / [` dual-tag remains. PASS.

**Fix 2 (citation_fidelity) — promote numbers from Self-check into body.**
- OLD: tesamorelin 2 mg/day and CJC-1295 5.8–8.1-day half-life appeared ONLY in the Self-check.
- NEW: tesamorelin `2 mg SubQ once daily [regulatory]` now in body line 41; CJC-1295 `half-life of 5.8–8.1 days` now in body line 40 inside the `[rct]` Teichman claim.
- `grep -inE '2 mg (SubQ )?once daily'` → line 41 (body) + lines 106,109 (Self-check referencing it). PASS — number now load-bearing in a finding.
- `grep -inE '5\.8|half-life'` → line 40 (body, `[rct]`), line 100 (biblio caveat), lines 108,109 (Self-check). The half-life is stated+tagged+sourced in body C-3; Self-check now references rather than introduces it. PASS.

**Fix 3 (risk_floor_readiness) — add stopping criteria per class.**
- OLD: no explicit stopping-criteria thresholds; only monitoring panels + contraindication gates.
- NEW: line 55 GH-axis stopping criteria (IGF-1 over age-adjusted ULN `[regulatory]`/`[practitioner_protocol]`, glucose/A1c into impaired range); line 56 angiogenic stopping criteria (new/abnormal tumor marker, unexplained mass, thrombotic event) `[practitioner_protocol]`; implication line 58 adds a paired `stopping_criteria` schema field.
- `grep -inE 'stopping crit|stop/adjust|discontinue|tumor marker|thrombotic'` → hits on 55, 56, 58 (C-4 additions), 64 (C-5 contraindication context), 110 (Self-check). PASS — both mechanism classes now have explicit, tagged discontinue thresholds.
