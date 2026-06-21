# Gate 6 — CRITIQUE (red-team) — Semaglutide research-report.md

**Critique agent:** critique-sema-i1 (did NOT author the draft)
**Draft:** `vault/library/peptides/semaglutide/research-report.md` (538 lines, 8 sections + crosswalk + 48-entry bibliography + provenance note)
**Sources consulted:** sections A–F in `/tmp/aplus-research/semaglutide/sections/`

## Prose critique

I adversarially reviewed the synthesized draft against the seven mandated red-team axes. The draft is unusually disciplined for this library — it is the first A-tier entry and it neither under-sells a landmark-RCT drug nor over-sells a doctor-required one. Findings below are minor-only; nothing rises to major/critical.

### 1. Balance (benefit vs caveat) — PASS
The draft represents the real benefits accurately and at full strength: SUSTAIN/PIONEER glycemic (~1.5–1.8% HbA1c), STEP-1 −14.9% weight, SELECT −20% MACE (HR 0.80), FLOW −24% kidney composite (HR 0.76), plus MASH accelerated approval. It does NOT dismiss the drug — the "Read this first" header and TL;DR both frame it as a "genuinely approved, genuinely efficacious" agent with a landmark trial base. Equally, the caveats are surfaced and NOT buried: GI as the dominant discontinuation driver (§5.1, with explicit Wegovy discontinuation 16.6% vs 8.2% in SELECT), weight regain ~two-thirds within a year (§5.2), lean-mass loss ~39–45% of weight lost (§5.3), gallbladder/pancreatitis/aspiration (§5.4–5.5), and the boxed warning. The benefit/caveat symmetry is explicitly built into the header, TL;DR, §5, and §7.2. No under- or over-selling detected.

### 2. Population annotation — PASS
Population is annotated on essentially every efficacy/outcome claim, and the four landmark figures are kept distinct and never conflated: STEP-1 −14.9% (non-diabetic obesity), STEP-2 −9.6% (T2D obesity, same 2.4 mg dose), SELECT (non-diabetic, established CVD), FLOW (T2D + CKD). §2 opens with an explicit "figures are NOT interchangeable across programs" warning; §2.3/§2.4 spell out the STEP-1 vs STEP-2 attenuation as the canonical reason not to generalize; §3 repeats the SUSTAIN-6 (T2D) vs SELECT (non-diabetic) distinction. Matches the section-B/-C sources exactly.

### 3. Thyroid C-cell (rodent) & suicidality (investigated) — PASS
The thyroid C-cell boxed warning is consistently framed as rodent-derived and NOT human-demonstrated (header, TL;DR, §5.7, §5.10, §7.2, provenance note), quoting the label's own "It is unknown whether... in humans" wording and citing the reassuring 84,237-participant null meta-analysis [26]. Suicidality is consistently framed as investigated/not-confirmed, with the Wang 2024 cohort showing LOWER (not higher) ideation associations and the explicit caveat "not 'semaglutide causes suicidality'." Neither reads as a proven human risk. Faithful to section-D.

### 4. SURMOUNT-OSA = tirzepatide — PASS
The OSA integrity correction is preserved verbatim from section-C and reinforced in the header ("One integrity correction the reader must carry...") and §3.3 ("Do not credit OSA to semaglutide"). OSA benefit is explicitly NOT attributed to semaglutide; it is marked INVESTIGATIONAL/unestablished. The §1.4 tirzepatide-is-a-different-class passage is flagged as load-bearing for this correction.

### 5. Regulatory — PASS
Approval dates are correct: Ozempic Dec 5 2017 (NDA 209637), Rybelsus Sep 2019, Wegovy Jun 2021; Wegovy CV indication Mar 8 2024; MASH accelerated Aug 2025. EMA dates present. WADA: the "NOT prohibited" status is primary-anchored to the USADA list [40]; the 2026 Monitoring-Program addition is correctly presented as secondary-reported [41] and explicitly NOT a ban, with the un-rendered wada-ama.org primary [42] flagged as a carried re-check. The compounded-semaglutide arc is handled with care — shortage resolved Feb 21 2025, enforcement-discretion wind-down (503A Apr 22 / 503B May 22 2025), salt-form and counterfeit warnings — and explicitly does NOT endorse current compounding legality ("important not to overstate current legality... no longer permitted").

### 6. Citation integrity — PASS
Unified bibliography is complete: all inline numbers 1–48 are used and all 48 are defined (mechanically verified — no missing entry, no gap in the 1–48 range). No dangling inline [n]; no orphan bibliography entry. The crosswalk mapping section-local A–F tokens to unified numbers is present and explains the label-family de-duplication. No Wikipedia source is cited — the two "Wikipedia" string hits are both negative assertions ("No Wikipedia sources"), which the prompt explicitly permits and which are correctly NOT treated as citations.

### 7. Concentration/sponsor audit — PASS
The ~76% Novo Nordisk single-sponsor concentration is surfaced prominently (header, evidence_tier rationale, dedicated §4, §7.1, provenance flag) with honest mitigation (hard adjudicated endpoints, double-blind placebo control, FDA/EMA review, cross-population directional consistency) and an honest non-mitigation (no independent RWE cohort opened in-corpus). The AUD trial [19] is correctly identified as the non-sponsor exception. Tier A / risk medium are defensible and internally consistent (A = high evidence; medium = real, manageable, doctor-supervised risk; `doctor_discussion_required: true`). No contradictions found.

### Minor observations (non-blocking)
- **SUSTAIN-6 statistics nuance (minor / logical-inconsistency-adjacent):** §3.1 reports HR 0.74 (95% CI 0.58–0.95; P<0.001 for noninferiority). A CI excluding 1.0 is nominally superiority-significant, yet the P-value is labeled "for noninferiority." This is NOT an error — it faithfully reflects how SUSTAIN-6 was designed (a pre-approval noninferiority safety CVOT not powered for superiority), and the draft explicitly says so. A lay reader could momentarily misread it, but the framing is accurate and honest. No change required.
- **Lean-mass figure presentation (minor):** §5.3 gives "~39–45%" alongside "~6.9 kg of ~15.3 kg total" (=~45%) and "~5.3 kg lean vs ~8.4 kg fat" (a different ratio); the range is acknowledged as "reported figures include," so it is internally bounded rather than contradictory. Acceptable as a reported range.

These are documented for completeness only and do not affect the verdict.

## Verdict

verdict: PASS

```json
{"phase":"6","critique_agent_id":"critique-sema-i1","draft_path":"vault/library/peptides/semaglutide/research-report.md","findings":[{"category":"logical-inconsistency","severity":"minor","description":"SUSTAIN-6 (§3.1) reports HR 0.74 (95% CI 0.58–0.95; P<0.001 for noninferiority); the CI excludes 1.0 (nominally superiority-significant) while the P-value is labeled for noninferiority. This is faithful to the trial's noninferiority-powered design (and the draft says so explicitly), but a lay reader could momentarily misread it. Non-blocking."},{"category":"balance-issue","severity":"minor","description":"Lean-mass loss (§5.3) is given as ~39–45% with two underlying ratios (~6.9/15.3 kg ≈45%; ~5.3 kg lean vs ~8.4 kg fat). Presented as a reported range rather than a single figure; internally bounded and not contradictory, but the two ratios are not reconciled. Non-blocking."}],"additional_retrievals":[],"halt_reasons":[],"iterations":1,"verdict":"PASS"}
```
