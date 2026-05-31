# Gate 4.75 — Integrity Verifier (recovery-specialist, standard mode)

Independent adversarial citation-integrity audit across the 4 judged sections (A: metrics/wearables;
B: overtraining/load-management; C: recovery modalities; D: safety/red-flags/boundaries). All greps and
web-fetches run by the verifier; section self-checks were NOT trusted.

Auditor date: 2026-05-31. Mode: standard (IC-13 corpus-scoping = SKIP; IC-6 spot-verify is the adversarial sample).

---

## IC-1 Type-tag presence

**Status: PASS (with one documented WARN-grade nuance, no HALT).**

Every inline claim-site citation in all four section bodies carries the `[N, tag]` form with exactly one
enum tag. Independent extraction of `\[[0-9][0-9A-Za-z-]*,\s*[a-z_]+\]` returned only valid enum tags
across A/B/C/D (rct, meta_analysis, cohort, open_label, mechanism_review, regulatory, practitioner_protocol,
vendor_label). No untagged numeric claim-site was found in body prose.

- Section A: 17 distinct inline cites, all `[N, tag]`; every numeric (r, ICC, CV, SMD, MAPE, bias, HR, %)
  single-tagged at first statement (e.g., alcohol rMSSD suppression `[2, rct]`; Oura r=0.962 `[10, cohort]`;
  HRV-guided SMD 0.50 `[16, meta_analysis]`).
- Section B: 12 distinct inline cites, all tagged. Numerics (41–60% taper volume cut, 56-study count,
  6 POMS dimensions) traced to tagged meta_analysis/regulatory/mechanism_review.
- Section C: 15 inline cites (incl. suffixed -PBM/-AR/-PT), all tagged. Effect sizes (SMD −0.23, cSMD −0.22,
  HR 0.37, g 0.40–0.49, +7.1% plasma volume) single-tagged at first statement.
- Section D: 9 inline cites, all tagged. Numerics (>100 bpm, 3–6 mo abstention, 5–10 bpm RHR trend,
  ~30 s/~3 min cold-shock, iron-deficiency 15–35%/3–11%) traced to regulatory/mechanism_review.

**Nuance (WARN-grade, not HALT):** Section B line 49 carries a *bare-tag* inline citation `[practitioner_protocol]`
(no citation number) grounding the deload claim. This deviates from the canonical `[N, tag]` form. It does NOT
trigger HALT under IC-1 because (a) the claim it grounds is explicitly a *non-numeric, non-efficacy* statement
("convention rather than RCT-validated efficacy … not proven dose-response"), and (b) no numeric is attached.
The bare tag is a formatting blemish, not a numeric-grounding violation. Logged for the synthesis step to
normalize to a numbered cite or an explicit "no-source / convention" annotation.

---

## IC-2 Bibliography↔inline symmetry (per section)

**Status: PASS.**

- **Section A:** inline {1..17} all present; bib {1..17} all present. [6] deliberately reuses source [1]'s
  DOI under a distinct measurement-standardization claim, both numbered for traceability — not an orphan.
  No orphan in either direction.
- **Section B:** inline {1..12} all present; bib {1..12} all present. No orphan.
- **Section C:** inline {1,2,3,4,5,6,7,8,9,10,11-PBM,12-AR,12-PT,13,12(vendor)} all resolve; bib carries each.
  The three suffixed tags (-PBM Vanin, -AR Ortiz, -PT Sams) each map to a distinct real source; [12] (vendor)
  is the non-grounding vendor entry. No orphan.
- **Section D:** inline {1..9} all present; bib ends at [9]. The former [10] (Hachem/Cureus) was dropped and
  leaves no orphan inline reference in body prose (only self-check disposition prose references it). No orphan.

---

## IC-3 Vendor-not-numerical

**Status: PASS.**

Only Section C carries a `vendor_label` source ([12], percussive/sauna/plunge manufacturer pages). All three
body occurrences (`[12, vendor_label]` at lines 141, 181, 222) explicitly state the vendor source "grounds no
effect-size" / "ground nothing." No numeric anywhere in the corpus is grounded by a vendor_label cite. No HALT.

---

## IC-4 Anecdote-not-numerical

**Status: PASS.**

Zero `anecdote_aggregate` citations appear in any of the four sections (grep across all four returned no
`anecdote_aggregate` token outside self-check prose listing it as absent). No numeric is grounded by anecdote.
No HALT.

---

## IC-5 Practitioner-protocol not efficacy

**Status: PASS.**

Two practitioner-protocol usages, both compliant:
- Section B [8, practitioner_protocol] (Kentta & Hassmen TQR) grounds only the scale *construct* description
  (6–20 scale, TQR-10 variant) — explicitly "grounds no effect-size or prevalence claim."
- Section B line 49 bare `[practitioner_protocol]` grounds the deload claim, which is framed as the *opposite*
  of an efficacy claim ("convention rather than RCT-validated efficacy"). The efficacy claim adjacent to it
  (taper 41–60% volume cut improving performance) is grounded by [11, meta_analysis], not by the practitioner
  source. No practitioner_protocol cite solely grounds an efficacy/effect-size claim. No HALT.

---

## IC-6 First-author+year plausibility + independent spot-verify

**Status: PASS.**

**Fabrication-shape scan (all four bibliographies):** No anomalous DOI prefixes, no future-dated primaries
(the two 2025 entries — A[14] Apple Watch S25082380 and C[5] Wang network meta — and 2024 entries A[12] Liang,
C[2] Piñero, D[4] Dvořáková are within the 2026-05-31 corpus horizon and plausible), no fake TLDs, no PubMed
slug-not-PMID artifacts, no non-whitelisted hosts grounding standalone numerics. DOIs follow real registrant
prefixes (10.1249 LWW, 10.1113 Wiley/Physiol Soc, 10.1136 BMJ, 10.1001 JAMA, 10.3390 MDPI, 10.3389 Frontiers,
10.1007 Springer, 10.1080 T&F, 10.1519 LWW/NSCA, 10.26603 IJSPT, 10.1016 Elsevier). PMIDs are numeric and
length-plausible.

**Independent web-verification of 6 load-bearing numerical claims** (see Spot-Verify Summary for detail) — all
6 MATCH the cited primary. No mismatch found.

---

## IC-7 Population-mismatch

**Status: PASS.**

Confirmed expectation: these sections use NO `animal` or `in_vitro` primary citations. Grep for `animal` and
`in_vitro` tags returned zero body claim-site hits across all four sections. All populations are human (athletes,
trained/active adults, Finnish men cohort, etc.). Section D self-check (c) documents that the rabbit-heart
autonomic-conflict model surfaced in research was *deliberately excluded* in favor of the human-physiology
framing in [7, Shattock & Tipton]. No `[population-mismatch: <species>]` tag is required, and none is omitted
in error. No HALT.

---

## IC-8 Route/dose-extrapolation

**Status: PASS.**

Modality "doses" cited match the cited protocols:
- CWI: Section C cites medium-duration medium-temp 10–15 min at 11–15 °C (best for DOMS, SUCRA 84.3%) and
  colder 5–10 °C (best for CK/jump) — both attributed to the [5, meta_analysis] network MA dose strata, not
  extrapolated.
- Sauna (training-relevant): Scoon [7, rct] post-exercise sauna protocol grounds the +7.1% plasma-volume /
  ~32% run-time claim; the dose is the study's own protocol. The Laukkanen frequency exposure (4–7×/week) in
  C[6]/D[8] is the cohort's reported exposure category, not a prescribed dose.
- Photobiomodulation: wavelengths 655–950 nm, 20–60 J (small) / 60–300 J (large) attributed directly to the
  Vanin [11-PBM, meta_analysis] dose windows. No extrapolation beyond cited ranges. No HALT.

---

## IC-9 Concentration-surfacing (single-group dominance)

**Status: PASS.**

Two sub-topics with known single-group concentration risk are surfaced first-class, as required:
- **Photobiomodulation (Leal-Junior cluster):** Section C explicitly grades PBM PROVISIONAL and surfaces, in
  the body, that "a large fraction of the favourable photobiomodulation literature originates from a small
  cluster of overlapping research groups (notably Leal-Junior and collaborators), some with device-industry
  ties." The cited meta [11-PBM] Vanin 2018 includes Leal-Junior as senior author — the concentration is named,
  not buried. PASS.
- **Sauna (Laukkanen group):** Section C surfaces that the headline sauna-mortality evidence is "a single
  population (older Finnish men…)" with healthy-user bias and reverse causation flagged; Section D uses the
  Laukkanen 2018 review for hemodynamics/contraindications. The single-group provenance (Laukkanen/Kunutsor
  KIHD lineage) is surfaced as a single-cohort caveat first-class. PASS.

No buried-only dominant cluster found. No HALT.

---

## IC-10 Cross-section ID concordance (folds Phase-4.25 reconciliation)

**Status: PASS (one defensible tag-discordance noted; identifiers AGREE).**

Shared entities appearing in 2+ sections, with identifier reconciliation:

1. **Meeusen 2013 ECSS/ACSM OTS consensus** — appears as **B[1]** and **D[5]**.
   - B[1]: PMID 23247672, DOI 10.1249/MSS.0b013e318279a10a, MSSE 45(1):186-205, 2013, `regulatory`.
   - D[5]: PMID 23247672, DOI 10.1249/MSS.0b013e318279a10a, MSSE 45(1):186–205, 2013, `regulatory`.
   - **CONCORDANT** — identical PMID, DOI, year, volume/pages, and tag. (D[5] lists full author string;
     B[1] uses "et al." + the dual ECSS/ACSM journal pairing. Same work.) Independently web-verified (matches).

2. **Plews/Buchheit HRV** — A[8] vs D[9] are **distinct papers**, not a shared entity:
   - A[8]: Plews 2012, *Eur J Appl Physiol*, PMID 22367011, DOI 10.1007/s00421-012-2354-4, `open_label`
     (the 77-day two-triathlete case comparison).
   - D[9]: Plews 2013, *Sports Medicine*, PMID 23852425, DOI 10.1007/s40279-013-0071-8, `mechanism_review`
     (the "opening the door" monitoring review).
   - Different PMID/DOI/year/journal/title → two separate works sharing authorship. NOT a concordance
     conflict. Tags differ appropriately (primary case study vs narrative review). No HALT, no WARN.

3. **Laukkanen sauna** — C[6] vs D[8] are **distinct papers**, not a shared entity:
   - C[6]: Laukkanen T 2015, *JAMA Intern Med*, PMID 25705824, DOI 10.1001/jamainternmed.2014.8187, `cohort`
     (the KIHD primary mortality cohort).
   - D[8]: Laukkanen JA 2018, *Mayo Clin Proc*, PMID 30077204, DOI 10.1016/j.mayocp.2018.04.008,
     `mechanism_review` (the benefits-of-sauna review).
   - Different PMID/DOI/year/journal → two separate works sharing authorship. NOT a concordance conflict.
     Tags differ appropriately (cohort vs review). No HALT.

4. **Bellenger** — historical reconciliation only: Section A's self-check documents it REMOVED an erroneous
   "Bellenger 2024, Scientific Reports" attribution from A[11] (now correctly Fennell 2023). Section B[4]
   legitimately cites the real Bellenger 2016 (Sports Med, PMID 26888648, DOI 10.1007/s40279-016-0484-2,
   `meta_analysis`). No live cross-section Bellenger collision in current text — A no longer cites any
   Bellenger entry. Web-verified B[4] (matches). No HALT.

No shared-entity identifier mismatch found. No HALT.

---

## IC-11 No placeholder strings

**Status: PASS.**

Grep `TBD|TODO|lorem|citation needed|XXX|FIXME|placeholder` returned one hit: Section C self-check line 316
uses the word "placeholder" to describe the vendor_label entry's non-grounding role ("[vendor_label]
placeholder, by design"). This is descriptive self-check prose, not an unfilled citation placeholder. No
genuine placeholder string in any body claim or bibliography entry. No HALT.

---

## IC-12 No Wikipedia / excluded sources; host admissibility

**Status: PASS (with one resolved Tier-3 host, already dropped).**

- No Wikipedia, Reddit, Quora, Medium, Substack, LinkedIn, YouTube, or podcast source grounds any claim. The
  only "Substack/LinkedIn" string is in Section A self-check prose stating such hits were *excluded* from the
  bibliography.
- **Cureus (Tier-3):** Section D's former [10] (Hachem 2025, Cureus narrative review) was DROPPED before this
  audit; its claims were re-cited to whitelisted [8] Laukkanen (Mayo Clin Proc) and [7] Shattock & Tipton
  (J Physiol). No surviving Cureus host grounds any standalone claim. Confirmed: no `cureus` body/bibliography
  citation remains (only self-check disposition prose).
- All surviving bibliography hosts are Tier-1/2 admissible: PubMed/PMC (NCBI), JAMA, BMJ/BJSM, LWW/MSSE/JSCR,
  Wiley/J Physiol, Springer/Sports Med/EJAP, T&F, Elsevier (JSAMS, JSHS, Cardiology Clinics, Mayo Clin Proc),
  Frontiers (open-access, flagged), MDPI Sensors (open-access, flagged), Human Kinetics IJSPP, IJSPT,
  Georgian Med News (PubMed-indexed). MDPI/Frontiers open-access single-source flags are applied in-text
  (A[12]/[14]/[15], B[5], C Frontiers entries). No HALT.

---

## IC-13 Per-citation corpus scoping

**Status: SKIP (standard mode).** Per the citation-integrity reference, full per-citation corpus scoping is
skipped at standard mode. The IC-6 independent spot-verify of 6 load-bearing claims serves as the adversarial
sample in lieu of full corpus scoping.

---

## Concentration Audit

**Method:** Deduplicated all distinct PRIMARY citations (tags ∈ rct/meta_analysis/cohort/open_label/animal/
in_vitro) across the 4 sections. Cross-section duplicates collapsed to one entity. Mechanism_review/regulatory/
practitioner_protocol/vendor_label are non-primary and excluded from the denominator.

**Distinct primaries by section:**
- A (14): de Zambotti(rct), Pietilä(cohort), Mishra(cohort), Sandercock/de Souza(cohort), Tenan/Brar(cohort),
  Plews2012(open_label), Cao(cohort), Fennell(cohort), Liang(cohort), Miller(cohort), AppleWatchS6(cohort),
  Schaffarczyk(cohort), Manresa-Rocamora(meta), Al Haddad(cohort).
- B (5): Kajaia(cohort), Bellenger2016(meta), Coyne(cohort), Saw(meta), Bosquet(meta).
- C (12): Roberts(rct), Piñero(meta), Grgic(meta), Fyfe(rct), Wang(meta), Laukkanen2015(cohort), Scoon(rct),
  Bieuzen(meta), Hill(meta), Wiewelhove(meta), Vanin(meta), Dupuy(meta). (Ortiz & Sams are mechanism_review,
  excluded.)
- D (0): all D sources are mechanism_review/regulatory — no primaries.

No primary citation is shared across sections by identifier (Plews2012≠Plews2013; Laukkanen2015≠Laukkanen2018;
Bellenger appears only in B). 

**Total distinct primaries: 31.**

**Largest single-lab/single-group cluster:** the Buchheit/Laursen group — Plews 2012 (A[8], with Laursen,
Kilding, Buchheit) and Al Haddad 2011 (A[17], with Laursen, Buchheit). Both primary, both within Section A.
- **largest_cluster_name:** Buchheit/Laursen (Auckland/AIS HRV group)
- **largest_cluster_count:** 2
- **share:** 2/31 = **0.065 (6.5%)**
- **threshold_triggered (≥0.70): NO.**

(Runner-up clusters are also size-2 at most: Laukkanen lineage has only 1 *primary* — Laukkanen 2015 cohort;
the 2018 review is non-primary. Bosquet appears as senior author on Bosquet 2007 [B11] and as co-author on
Dupuy 2018 [C13] = a size-2 cluster, 6.5%. Dietetics of sub-topic concentration handled under IC-9.) The
corpus is well-distributed; no single lab dominates. Concentration risk: LOW.

---

## Spot-Verify Summary (independent WebFetch against cited primary)

| # | Claim (section) | Cited as | Web-verified result | Match |
|---|-----------------|----------|---------------------|-------|
| 1 | CWI attenuates strength gains SMD −0.23 (95% CI −0.45, −0.01), 10 studies, n=170 (C) | [3] Grgic 2023, Eur J Sport Sci, PMID 35068365 | Title/author/year/journal confirmed; SMD −0.23 (95% CI −0.45, −0.01; p=0.041), 10 studies, n=170 | MATCH |
| 2 | Sauna 4–7×/wk vs 1×/wk SCD HR 0.37 (95% CI 0.18–0.75), n=2,315, median 20.7 y (C) | [6] Laukkanen 2015, JAMA Intern Med, PMID 25705824 | Confirmed; HR 0.37 (0.18–0.75), 2,315 men, 20.7 y median | MATCH |
| 3 | ECSS/ACSM OTS joint consensus, MSSE 45(1):186-205, PMID 23247672 (B[1]/D[5]) | Meeusen 2013 | Title/10-author list/journal/45(1):186-205/PMID all confirmed; is joint ECSS/ACSM consensus | MATCH |
| 4 | Oura time-domain HR/rMSSD strong vs ECG; frequency-domain (LF, LF/HF) poor, n=35 (A) | [10] Cao 2022, JMIR, PMID 35040799 | n=35 confirmed; HR & RMSSD "high positive correlations"; LF & LF:HF "low positive correlations" — directional pattern matches (abstract is qualitative; precise r=0.962/0.42/0.36 are full-text strata, pattern corroborated) | MATCH |
| 5 | Resting HRV "largely unaffected by overreaching"; post-ex HRV rises with both adaptations (B) | [4] Bellenger 2016, Sports Med, PMID 26888648 | Title/author/journal confirmed; verbatim "Resting HRV is largely unaffected by overreaching"; post-exercise HRV/HRR increases occur with overreaching too | MATCH |
| 6 | Subjective self-report "trumps" objective; 56-study systematic review (B) | [10] Saw 2016, BJSM, PMID 26423706 | Title/author/journal confirmed; 56 studies; subjective superior sensitivity/consistency | MATCH |

**6/6 verified claims MATCH the cited primary. No mismatch.**

---

## Verdict

verdict: PASS

- **IC-1 type-tag presence:** PASS (1 WARN-grade bare-tag `[practitioner_protocol]` in B line 49 grounding a
  non-numeric convention claim; formatting blemish, not numeric violation).
- **IC-2 inline↔bib symmetry:** PASS (all four sections, no orphans either direction).
- **IC-3 vendor-not-numerical:** PASS (C[12] vendor_label grounds zero numerics, explicitly barred).
- **IC-4 anecdote-not-numerical:** PASS (zero anecdote_aggregate cites in corpus).
- **IC-5 practitioner-protocol not efficacy:** PASS (both uses ground only construct/anti-efficacy statements).
- **IC-6 plausibility + spot-verify:** PASS (no fabrication artifacts; 6/6 spot-verified claims match).
- **IC-7 population-mismatch:** PASS — no animal/in_vitro primaries; expectation confirmed; no tags required.
- **IC-8 route/dose-extrapolation:** PASS (all modality doses match cited protocols).
- **IC-9 concentration-surfacing:** PASS (Leal-Junior PBM cluster and Laukkanen single-cohort both surfaced
  first-class).
- **IC-10 cross-section ID concordance:** PASS (Meeusen 2013 identifiers AGREE across B/D; Plews and Laukkanen
  cross-section appearances are distinct works with distinct identifiers, not collisions; Bellenger has no
  live cross-section collision).
- **IC-11 no placeholders:** PASS (sole "placeholder" hit is descriptive self-check prose).
- **IC-12 no excluded sources / host admissibility:** PASS (Cureus already dropped; all surviving hosts
  Tier-1/2; open-access MDPI/Frontiers flagged in-text).
- **IC-13 corpus-scoping:** SKIP (standard mode; IC-6 spot-verify is the adversarial sample).
- **population_mismatch:** none required (no animal/in_vitro citations).
- **concentration_audit:** 31 distinct primaries; largest cluster = Buchheit/Laursen, count 2, share 0.065;
  threshold_triggered (≥0.70) = NO.
- **corpus_scoping:** SKIP-mode (standard).
- **halt_reasons:** none.
- **warnings:**
  1. Section B line 49 uses a bare-tag inline `[practitioner_protocol]` (no citation number) for the deload
     convention claim — normalize to a numbered cite or an explicit "convention / no primary source"
     annotation in synthesis. Non-blocking (grounds no numeric, no efficacy claim).
  2. Section A [10] Cao 2022 abstract reports frequency-domain accuracy qualitatively ("low positive
     correlations"); the precise inline r-values (r=0.42 LF, r=0.36 LF/HF; rMSSD r=0.962) are full-text
     stratum figures. Directional claim fully corroborated; precise values not independently re-derived from
     the abstract. Non-blocking — recommend a full-text confirmation note if these specific r-values become
     load-bearing downstream.
  3. Open-access single-source flags (MDPI Sensors A[12]/[14]/[15], Frontiers B[5]/C[5]/C[10]/C[13]) are
     correctly applied in-text; carried forward as advisory, not a defect.
