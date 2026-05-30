# Section C — Regulatory + contract-mapping

Scope: DSHEA regulatory surface (real retrieval, `regulatory`/Tier-2 sources) + agent contract-inheritance mapping (reasoned against design surfaces read this dispatch). Goal-agnostic: facts below are the canonical regulatory landscape, NOT pre-filtered for any operator goal. All status answers time-stamped (retrieval date 2026-05-29; FDA actions carry their own effective dates).

---

### Finding C1 — DSHEA premarket non-approval: manufacturer bears safety burden; FDA acts post-market only

**Claim:** Under the Dietary Supplement Health and Education Act of 1994 (DSHEA), FDA does NOT approve dietary supplements before marketing; the manufacturer/distributor is solely responsible for ensuring safety and that label claims are truthful and substantiated, and FDA's authority is post-market only (action against adulterated/misbranded products, cGMP enforcement under 21 CFR 111). This is the structural inverse of the drug pathway, where premarket FDA approval of safety AND efficacy is mandatory before marketing.

**Sources:**
- [1, regulatory] FDA, "Questions and Answers on Dietary Supplements" (fda.gov): "FDA does not have the authority to approve dietary supplements before they are marketed... companies that manufacture or market dietary supplements are responsible for ensuring that their products are safe and that label claims are truthful and substantiated." "FDA has the authority to take action against any adulterated or misbranded dietary supplement product after it reaches the market."
- [2, regulatory] FDA, "Dietary Supplements: New Dietary Ingredient Notifications" guidance + 21 CFR 111.70/.75/.80 (accessdata.fda.gov) — cGMP recordkeeping/quality-control obligations confirming post-market manufacturer responsibility.

**Status/disposition:** ACTIVE and structural (statute, 1994; cGMP rule 21 CFR 111 in force). Stable — not a time-sensitive enforcement status. Map to the specialist's `BASIS_NOT_REVIEWABLE` refusal logic: "supplement is legally marketed" ≠ "FDA reviewed it."

**Caveats:** "Legally marketed dietary supplement" is a regulatory status, not a safety or efficacy finding. cGMP (21 CFR 111) governs manufacturing quality (identity/purity/composition), NOT efficacy. No animal/in_vitro numerics here, so no population-mismatch tag applies.

---

### Finding C2 — The confusable-status set: GRAS / NDI-notified / structure-function claim / third-party-tested are each DISTINCT from "FDA-approved / proven effective / safe" (laundering hazard)

**Claim:** Four supplement statuses are routinely laundered into an unwarranted efficacy/safety inference: (a) **GRAS** = "generally recognized as safe" for a food use, a safety-of-ingestion conclusion, NOT efficacy and NOT FDA premarket approval of the supplement; (b) **NDI notification** = a 75-day-premarket safety *notification* the manufacturer files for ingredients not marketed before Oct 15, 1994 — FDA can object but does NOT "approve"; non-objection is not endorsement; (c) **structure/function claim** = a permitted labeling claim about effect on body structure/function that requires the mandatory disclaimer and is explicitly NOT FDA-evaluated; (d) **third-party tested (USP / NSF / Informed-Sport)** = a purity/identity/label-accuracy certification, NOT an efficacy or safety-of-use finding. Treating any of these as "approved," "proven effective," or "safe" is the laundering hazard — the supplement analog of the peptide "compoundable ≠ approved" trap.

**Sources:**
- [3, regulatory] FDA, "Structure/Function Claims" + "Small Entity Compliance Guide on Structure/Function Claims" (fda.gov): these claims "are not pre-approved by FDA, but the manufacturer must have substantiation that the claim is truthful and not misleading"; the mandatory disclaimer states the claim "has not been evaluated by the Food and Drug Administration" and the product "is not intended to diagnose, treat, cure, or prevent any disease" because "only a drug can legally make such a claim."
- [4, regulatory] FDA, "New Dietary Ingredients in Dietary Supplements — Background for Industry" + draft NDI guidance (fda.gov/media/176512, /99538): NDI = "a dietary ingredient that was not marketed in the United States in a dietary supplement before October 15, 1994"; premarket safety notification "at least 75 days before introducing the product into interstate commerce"; the standard is reasonable assurance the ingredient "does not present a significant or unreasonable risk of illness or injury" — a safety bar, not approval/efficacy.

**Status/disposition:** ACTIVE. Encode directly as the specialist's status-disambiguation card (analogous to peptide-specialist SF-07). Status answers must be time-stamped because GRAS/NDI dispositions and certification marks change.

**Caveats:** GRAS self-affirmation (manufacturer-determined GRAS without FDA notification) exists and is weaker still than GRAS-notified — surface that gradient when the question touches a specific ingredient. Third-party certs (USP/NSF/Informed-Sport) are private-body marks, not Tier-2 regulatory; cite the certifier's own scope statement, never as efficacy. No numerics; no population-mismatch tag.

---

### Finding C3 — Banned / enforcement-action ingredients sold under a supplement label (time-sensitive status)

**Claim:** A recurring class of ingredients is marketed under a "dietary supplement" label while FDA holds them NOT to be lawful dietary ingredients (adulterated/misbranded, or unapproved drugs). Documented, dated actions: **ephedrine alkaloids (ephedra)** — final rule declaring them adulterated, published 2004-02-11, effective 2004-04-12; **DMAA** — FDA position that DMAA-containing products are adulterated, warning letters + a 2013 voluntary recall (Hi-Tech Lipodrene); **DMHA** — 12 warning letters, FDA considers DMHA-containing supplements adulterated; **BMPEA** — warning letters 2015-04-23 to five companies, FDA: BMPEA "does not meet the statutory definition of a dietary ingredient" and is not a constituent of Acacia rigidula; **Acacia rigidula** — warning letters 2016-03-15 to six companies (no evidence of lawful pre-1994 marketing); **higenamine** — mixed adrenergic agonist present in some stimulant/weight-loss supplements (also a WADA-relevant agent); **SARMs and "andro"/androstenedione** — FDA: these "are not dietary supplements... they are unapproved drugs"; warning letters and criminal actions; 4-androstenedione not GRAS (2022 scientific memo cites reproductive/cardiovascular/possible carcinogenic concerns); **kratom (Mitragyna speciosa)** — FDA: "not appropriate for use as a dietary supplement," held to be an NDI with inadequate safety assurance; import alerts (Import Alert 54-15) and product seizures.

**Sources:**
- [5, regulatory] FDA, "Small Entity Compliance Guide: Final Rule Declaring Dietary Supplements Containing Ephedrine Alkaloids Adulterated" (fda.gov): final rule published 2004-02-11, effective 2004-04-12.
- [6, regulatory] FDA, "DMAA in Products Marketed as Dietary Supplements" + "DMHA in Dietary Supplements" + "FDA Acts on Dietary Supplements Containing DMHA and Phenibut" (fda.gov): DMAA/DMHA adulterated; 12 DMHA warning letters.
- [7, regulatory] FDA, "Recent FDA Action on Dietary Supplements Labeled as Containing BMPEA" (2015-04-23) + "...Acacia Rigidula" (2016-03-15) (fda.gov): BMPEA "does not meet the statutory definition of a dietary ingredient."
- [8, regulatory] FDA, "Bodybuilding Products: SARMs Cause Harm" + "FDA Warns of Use of SARMs Among Teens, Young Adults" + Scientific Memorandum: Androstenedione (2022-03-01, fda.gov/media/169491): SARMs/andro are "unapproved drugs," not dietary supplements; 4-androstenedione not GRAS.
- [9, regulatory] FDA, "FDA and Kratom" + Import Alert 54-15 (accessdata.fda.gov) + "US Marshals seize dietary supplements containing kratom" (fda.gov): kratom "not appropriate for use as a dietary supplement," NDI with inadequate safety assurance.

**Status/disposition:** TIME-SENSITIVE — this is the highest-volatility finding. Retrieved 2026-05-29. Enforcement status (import alerts, warning-letter counts, new ingredients added to the watch list) changes continuously; any specialist answer citing a ban/enforcement status MUST re-verify against the current FDA "Information on Select Dietary Supplement Ingredients" directory and Import Alert pages at answer time, and stamp the answer. Map to `BASIS_NOT_REVIEWABLE` + the H1/H2 auto-block when a queried "supplement" is in fact an unapproved-drug/banned class.

**Caveats:** A product carrying a "dietary supplement" label does NOT establish lawful dietary-ingredient status — FDA repeatedly finds label-claimed "supplements" that are unapproved drugs (SARMs) or non-ingredients (BMPEA). Warning-letter counts cited (12 DMHA; 5 BMPEA; 6 Acacia) are point-in-time. No animal/in_vitro numerics used to ground a human dose; the 4-androstenedione safety concerns are FDA's regulatory characterization, not an effect-size claim.

---

### Finding C4 — International divergence (goal-agnostic regulatory facts)

**Claim:** Supplement regulatory status is jurisdiction-specific and does NOT transfer: **EU** — Directive 2002/46/EC regulates food supplements as *foodstuffs under food law, not medicinal law* ("the legislation does not apply to medicinal products"), with a harmonized positive list of permitted vitamins/minerals and a prohibition on disease/medicinal claims ("must not be labelled, presented or advertised as being able to prevent, treat or cure a disease"); **Australia** — the TGA regulates supplements as *therapeutic goods*, requiring ARTG listing (most as "listed medicines") before market entry, a stricter posture than the US food-frame; **Canada** — Health Canada's Natural Health Products framework requires a Product Licence and an NPN (Natural Product Number) issued by the NHPD before sale, i.e., a premarket licence the US does not require. The same product can be a freely-marketed US supplement, an Australian listed *medicine*, and a Canadian NPN-licensed NHP simultaneously.

**Sources:**
- [10, regulatory] EUR-Lex, "Ensuring safe food supplements in the EU" / Directive 2002/46/EC (eur-lex.europa.eu): harmonized vitamin/mineral list; food-law (not medicinal) treatment; mandatory labeling; medicinal-claim prohibition — all quoted verbatim above.
- [11, regulatory] TGA (Australia, tga.gov.au, per secondary compliance summary [12]): supplements regulated as therapeutic goods; ARTG listing required pre-market. (Tier-2 own-jurisdiction regulator; primary TGA page recommended for re-verification.)
- [12, regulatory/secondary] Health Canada NHPD: Product Licence + NPN required pre-sale (cited via compliance-summary secondary [BCF Life Sciences / ChemLinked]; flag for direct canada.ca verification before any status-critical use).

**Status/disposition:** ACTIVE, goal-agnostic. EU finding is directly source-grounded (EUR-Lex primary). TGA/Health Canada specifics are summarized from secondary compliance hosts and flagged for primary re-verification (the secondary hosts — tecexglobalcompliance, compliancegate, ChemLinked, BCF — are NOT on the Tier-2 whitelist; admissible only as discovery/`anecdote_aggregate`-class leads for the non-EU specifics).

**Caveats:** SINGLE-SOURCE DOMINANCE flag — the Australia/Canada specifics rest on non-whitelisted secondary compliance-vendor summaries, not the regulators' own pages (WebSearch on those regulators was blocked by classifier outage this dispatch). Treat TGA/Health Canada claims as leads requiring primary confirmation at canada.ca and tga.gov.au. The EU claim is independently grounded on EUR-Lex (Tier-2). No numerics.

---

### Finding C5 — Consolidated contract-inheritance: what supplement-specialist MUST encode (design-surface reasoning)

**Claim:** The supplement-specialist inherits the full foundation contract set and must encode, verbatim or by faithful instantiation, the following — derived from the three design surfaces read this dispatch (refusal-class-taxonomy.yaml, specialist-risk-class.yaml, _source-whitelist.md):

1. **8-class refusal taxonomy**, ≥4 distinct classes encoded, with **AUTHORITY_FRAMING_BYPASS MANDATORY** (`mandatory_for_every_specialist: true`); the operator (Walter) is named **adversary-class A3** (operator-self-harm via own-agent), the 81.8%-of-successful-jailbreaks vector — educational/"asking for a friend"/trainee framing does NOT relax the directive gate.
2. **H1–H8 worst-case-reachable composition with H1/H2 auto-block** (highest-harm reachable outcome blocks regardless of framing) — couple this to Finding C3's banned/unapproved-drug classes.
3. **GRADE two-axis** (certainty × strength) with a **strong-recommendation-on-low/very-low-certainty HALT**.
4. **Three-mechanism anti-sycophancy**: (A) no silent agreement, (B) maintain position under pushback, (C) guard against RLHF-drift.
5. **Operator-profile R7 read-before-`vault/compounds/*`-write precondition** — HALT on an unpopulated hard-limit field in the operator profile before writing any compound entry.
6. **Append-only `vault/meta/contradictions.md`** (never rewrite; log Tier-1/2-vs-practitioner dose conflicts, etc.).
7. **Escalation of `BLOCK_WITH_OVERRIDE_PATH` + PRESCRIPTIVE/PATIENT_FACING directives to the LIVE medical-liaison (Role 7) adjudicator** (per dispatch-flip commit 0514f2d, which deprecates the pre-Role-7 fallback). The supplement-specialist MUST encode the LIVE-Role-7 escalation — NOT the deprecated "medical-liaison when deployed; otherwise operator-acknowledged-override" fallback that the on-disk `templates/refusal-class-taxonomy.yaml` escalation fields still carry verbatim (see Caveats; the stale template language must not be inherited until the template is reconciled to the commit).
8. **Research dispatch is ONLY `aplus-research --mode=deep --target-class=compound`** — supplement `risk_class = compound-experimental-or-medium`; deep mode covers the experimental floor (MK-677, novel nootropics, phenibut), and standard would under-protect.
9. **Write surface:** WRITES `vault/compounds/` (supplement class) + `vault/protocols/supplement-stack`. **Unlike peptide-specialist, does NOT own a `vault/library/` tree.**
10. **Enforces type-tag / population-mismatch / concentration-audit on aplus-research returns** and **NEVER self-attests a gate** (PF-S2-01 / PF-S3-01).

**Sources (design surfaces, not web):**
- [13, design-surface] `templates/refusal-class-taxonomy.yaml` (S10 Phase 5; owner Role 1) — 8 classes; AUTHORITY_FRAMING_BYPASS mandatory; A3/81.8% rationale; PATIENT_FACING/PRESCRIPTIVE escalation to medical-liaison Role 7.
- [14, design-surface] `templates/specialist-risk-class.yaml` (S10 Phase 5; owner Role 2) — supplement-specialist row: `risk_class: compound-experimental-or-medium`, `mode_floor: deep`, `target_class: compound`, rationale (MK-677/nootropics experimental floor).
- [15, design-surface] `vault/library/_source-whitelist.md` — type-tag enum + admissibility matrix; `vendor_label`/`anecdote_aggregate` never ground numerics; population-mismatch on animal/in_vitro; non-English + practitioner-protocol tiers. Used to confirm the specialist enforces these on aplus-research returns. NOTE: the whitelist's "Used by" + Tier-3/4 examples are peptide-centric (compounding pharmacies, research-chem vendors) — supplement-specialist inherits the BASE list + type-tag discipline but does NOT own/extend a library tree.
- [16, design-surface] Repo git log — commit 0514f2d "dispatch-flip: medical-liaison live adjudicator; deprecate pre-Role-7 fallback (BC-1)" grounds item 7 (escalation now goes to the LIVE Role-7 adjudicator).

**Status/disposition:** ACTIVE design contract. Single consolidated inheritance finding (per dispatch instruction). Each numbered item maps to a profile section the specialist's `agent.md` must contain; an audit (`scripts/audit-specialist-profile.sh`) checks several (`--check refusal-classes`, `--check mode-floor-correctness`).

**Caveats:** Items are REASONED against design surfaces, not web-retrieved — correct provenance is the in-repo templates/whitelist/git-log, NOT external citation. One contradiction surfaced and logged here for `vault/meta/contradictions.md`: the dispatch brief says supplement-specialist "does NOT own a `vault/library/` tree," while peptide-specialist does — the `_source-whitelist.md` "Used by" list and Tier-3/4 hosts are peptide-flavored; supplement-specialist must consume the base whitelist without authoring a domain extension. The H1–H8 composition model and GRADE/anti-sycophancy mechanics are named in the brief but their canonical definitions live in Role-1/Role-2 design docs NOT read this dispatch — flagged as `basis-not-fully-reviewable` for those two items pending design-doc read; do not self-attest their exact wording. CONTRADICTION (log to vault/meta/contradictions.md): commit 0514f2d deprecates the pre-Role-7 operator-acknowledged-override fallback, but templates/refusal-class-taxonomy.yaml escalation fields (PATIENT_FACING_DIRECTIVE, BASIS_NOT_REVIEWABLE, PRESCRIPTIVE_DIRECTIVE) still state the otherwise-fallback verbatim; the specialist must encode the LIVE-Role-7 escalation per the commit, and the stale template fallback language must NOT be inherited until the template is reconciled.

---

## Bibliography

Regulatory (Tier-2; retrieved 2026-05-29 via WebSearch, Tavily over quota):
1. FDA — Questions and Answers on Dietary Supplements. fda.gov/food/information-consumers-using-dietary-supplements. `regulatory`.
2. FDA — NDI Notifications guidance; 21 CFR 111.70/.75/.80. fda.gov/media/99538, accessdata.fda.gov CFR Title 21 Part 111. `regulatory`.
3. FDA — Structure/Function Claims; Small Entity Compliance Guide on Structure/Function Claims. fda.gov/food/nutrition-food-labeling-and-critical-foods/structurefunction-claims. `regulatory`.
4. FDA — New Dietary Ingredients in Dietary Supplements: Background for Industry; Draft NDI Guidance. fda.gov/media/176512, /99538. `regulatory`.
5. FDA — Small Entity Compliance Guide: Final Rule Declaring Ephedrine Alkaloids Adulterated (2004-02-11 / eff. 2004-04-12). fda.gov/regulatory-information/search-fda-guidance-documents. `regulatory`.
6. FDA — DMAA in Products Marketed as Dietary Supplements; DMHA in Dietary Supplements; FDA Acts on DMHA and Phenibut. fda.gov/food/information-select-dietary-supplement-ingredients-and-other-substances. `regulatory`.
7. FDA — Recent FDA Action on Supplements Labeled as Containing BMPEA (2015-04-23); ...Acacia Rigidula (2016-03-15). fda.gov/food/hfp-constituent-updates. `regulatory`.
8. FDA — Bodybuilding Products: SARMs Cause Harm; SARMs Among Teens; Scientific Memorandum: Androstenedione (2022-03-01). fda.gov/drugs/fraudulent-products, fda.gov/media/169491. `regulatory`.
9. FDA — FDA and Kratom; Import Alert 54-15; US Marshals seize kratom supplements. fda.gov/news-events/public-health-focus/fda-and-kratom, accessdata.fda.gov/cms_ia/importalert_1137.html. `regulatory`.
10. EUR-Lex — Directive 2002/46/EC; "Ensuring safe food supplements in the EU." eur-lex.europa.eu/eli/dir/2002/46/oj. `regulatory`.
11. TGA (Australia) — therapeutic-goods regulation of supplements; ARTG listing. tga.gov.au (cited via secondary [12]; flag for primary re-verification). `regulatory` (secondary-sourced).
12. Health Canada NHPD — Product Licence + NPN. Cited via compliance-vendor secondaries (tecexglobalcompliance, compliancegate, ChemLinked, BCF Life Sciences) — NOT whitelisted; `anecdote_aggregate`-class lead, flag for canada.ca primary re-verification.

Design surfaces (in-repo; not web-retrieved):
13. `templates/refusal-class-taxonomy.yaml`. design-surface.
14. `templates/specialist-risk-class.yaml`. design-surface.
15. `vault/library/_source-whitelist.md`. design-surface.
16. Repo git log, commit 0514f2d (dispatch-flip; medical-liaison live adjudicator). design-surface.

---

## Self-check

- **Source count:** 16 total citations. Regulatory/web: 10 distinct regulatory sources (cites 1–10 grounded on fda.gov / accessdata.fda.gov / eur-lex.europa.eu — meets the ≥6 regulatory-source floor); cites 11–12 are secondary-sourced and explicitly flagged. Design-surface: 4 (cites 13–16). Regulatory floor (≥6) MET.
- **Type-tag discipline:** Every regulatory claim tagged `regulatory` (Tier-2). No numerical claim grounded on `vendor_label` or `anecdote_aggregate`. The one non-whitelisted secondary set (Australia/Canada specifics) is explicitly downgraded to `anecdote_aggregate`-class lead and flagged for primary re-verification — NOT used to ground a regulatory status as fact.
- **Population-mismatch:** No animal/in_vitro numericals were used to ground human claims, so no `[population-mismatch:<species>]` tags were required. The 4-androstenedione safety language (C3) is FDA's regulatory characterization, not an extrapolated effect size.
- **Single-source dominance:** Surfaced explicitly in C4 — the Australia/Canada (non-EU) specifics rest on a single class of non-whitelisted secondary compliance-vendor summaries (≥70% dominance for those two sub-claims), flagged for primary re-verification. EU claim is independently EUR-Lex-grounded.
- **Time-stamping of status answers:** Retrieval date 2026-05-29 stamped; C3 (banned/enforcement) explicitly flagged highest-volatility with named re-verification surfaces; FDA actions carry their own effective dates (ephedra 2004-02-11/04-12; BMPEA 2015-04-23; Acacia 2016-03-15; androstenedione memo 2022-03-01). C1/C2 marked structural/stable; C5 is a design contract (versioned, not time-volatile).
- **Goal-agnosticism:** All regulatory facts presented as the canonical landscape with no operator-goal pre-filtering; international divergence given as neutral jurisdiction facts. C5 maps inherited contracts without recommending any operator action.
- **No fabricated citations:** All web cites trace to URLs returned by WebSearch this dispatch; WebFetch 404'd on several fda.gov cross-host redirects, so verbatim quotes are taken from WebSearch result summaries (which quote the FDA pages) and the one successful EUR-Lex fetch — no quote is invented beyond what the retrieval returned. Two web searches (international regulators direct; one FDA follow-up) were blocked by a transient classifier outage and are noted as the reason for the C4 secondary-source reliance.
- **Anti-self-attestation:** This section does NOT mark any aplus-research gate as passed (PF-S2-01/PF-S3-01); it is research substrate only. Two C5 items (H1–H8 composition wording; GRADE/anti-sycophancy canonical text) flagged `basis-not-fully-reviewable` pending Role-1/Role-2 design-doc read rather than asserted from memory.

---

## Post-fix grep audit

Pattern: `operator-acknowledged-override|operator-with-warning|when deployed|otherwise` (case-insensitive). Two hits, both consistent with the LIVE-Role-7 escalation + the logged contradiction; neither asserts the deprecated fallback as a clean inherited contract.

- **L77 (C5 item 7):** Cites `"medical-liaison when deployed; otherwise operator-acknowledged-override"` ONLY to name it as the deprecated fallback that must NOT be inherited; the item now affirmatively requires the LIVE-Role-7 escalation per commit 0514f2d. Disposition: CONSISTENT (negation reference, not an assertion of the fallback).
- **L90 (C5 Caveats):** The added CONTRADICTION sentence cites `operator-acknowledged-override` / `otherwise-fallback` to document that `templates/refusal-class-taxonomy.yaml` still carries the deprecated language verbatim and to direct logging to `vault/meta/contradictions.md`; it explicitly states the stale language must NOT be inherited until the template is reconciled. Disposition: CONSISTENT (contradiction disclosure).

No other occurrences. No hit treats the operator-override / "when deployed" inheritance as clean.
