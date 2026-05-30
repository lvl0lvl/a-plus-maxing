# Section C — Clinical Red-Flags, Consumer-Test Validity, Safety Architecture

Goal-agnostic library research grounding the `gi-specialist` agent's refusal classes and critical-floor. This is canonical, vetted source material — NOT personalized for any operator. Personalization happens at dispatch, not here.

Every claim carries exactly one inline type-tag `[N, tag]`. Society/regulator position statements and clinical practice guidelines are tagged `regulatory`; mechanistic critiques of biomarker validity are tagged `mechanism_review`. The numbered Bibliography maps each N to a first-author Year + body + PMID/DOI/URL.

---

## C-1 GI alarm / red-flag features (require urgent in-person clinician evaluation)

Two professional-guideline anchors: the ACG/CAG dyspepsia guideline (Moayyedi 2017) [2, regulatory] and the ACG IBS guideline (Lacy 2021) [1, regulatory], cross-checked against the USPSTF CRC age threshold (Davidson 2021) [9, regulatory]. The alarm-feature set across these guidelines: unintentional weight loss, GI bleeding / iron-deficiency anemia, dysphagia/odynophagia, persistent (recurrent) vomiting, palpable abdominal mass or lymphadenopathy, and new-onset symptoms at older age [2, regulatory][1, regulatory].

TIME-CRITICAL = emergency / same-day evaluation (hemodynamic, perforation, obstruction, or acute hemorrhage risk). Urgent-referral = prompt in-person clinician work-up + endoscopy/imaging, not an LLM-managed symptom.

| Feature | Why it matters | TIME-CRITICAL vs urgent-referral | Source |
|---|---|---|---|
| Hematemesis / coffee-ground emesis | Active or recent upper-GI hemorrhage; airway + hemodynamic risk | **TIME-CRITICAL** | [2, regulatory] |
| Melena (black tarry stool) | Upper-GI bleed; volume loss can be occult-large | **TIME-CRITICAL** | [2, regulatory] |
| Hematochezia with hemodynamic change (dizziness, syncope, large-volume) | Brisk lower-GI bleed | **TIME-CRITICAL** | [2, regulatory][1, regulatory] |
| Acute severe / sudden abdominal pain, rigid abdomen, peritoneal signs | Possible perforation, ischemia, obstruction | **TIME-CRITICAL** | [2, regulatory] |
| Persistent vomiting with inability to tolerate fluids / signs of obstruction | Dehydration, electrolyte derangement, mechanical obstruction | **TIME-CRITICAL** | [2, regulatory] |
| Jaundice (new) | Biliary obstruction, hepatic / pancreatic malignancy | Urgent-referral (TIME-CRITICAL if with fever/sepsis = cholangitis) | [2, regulatory] |
| Dysphagia / odynophagia | Esophageal obstruction or malignancy; high specificity for organic findings | Urgent-referral (prompt endoscopy) | [2, regulatory] |
| Unintentional weight loss | High predictive value for organic/malignant disease | Urgent-referral | [1, regulatory][2, regulatory] |
| Iron-deficiency anemia / occult GI bleeding | Bi-directional endoscopy to exclude malignancy/IBD | Urgent-referral | [1, regulatory][2, regulatory] |
| Palpable abdominal mass or lymphadenopathy | Possible malignancy | Urgent-referral | [2, regulatory] |
| New-onset symptoms at older age (dyspepsia ≥60; any new GI alarm symptom in CRC-screening-eligible adult) | Rising malignancy pretest probability with age | Urgent-referral | [2, regulatory] |
| Nocturnal symptoms waking from sleep (diarrhea/pain) | Atypical for functional disease; raises organic suspicion | Urgent-referral | [1, regulatory] |
| Family history of colorectal cancer or IBD | Elevated baseline organic risk; modifies screening threshold | Urgent-referral (screening pathway) | [9, regulatory][1, regulatory] |

**Age threshold note.** USPSTF (2021) recommends average-risk CRC screening begin at **age 45** — Grade A for ages 50–75, Grade B for ages 45–49 [9, regulatory]. The legacy "age ≥50 new-onset" alarm threshold in older GI texts is therefore superseded for CRC-screening purposes by **age ≥45**; the dyspepsia-specific endoscopy age cutoff (≥60) remains a separate, narrower trigger [2, regulatory]. The agent must encode the lower 45 threshold for new-onset symptoms, not the legacy 50.

**Design implication.** TIME-CRITICAL features map to an immediate "seek emergency care now" refusal-and-redirect with no triage dialogue. Urgent-referral features map to a "this needs in-person clinician evaluation before any further self-management discussion" gate. Both are *floor* behaviors — they fire regardless of how benign the rest of the presentation looks.

---

## C-2 Why an LLM must not diagnose (IBS / IBD / celiac / CRC / functional dyspepsia differential)

The core hazard is **anchoring on a benign functional label** (IBS, functional dyspepsia) when an alarm feature signals organic or malignant disease. The conditions in the differential — IBS, IBD (Crohn's / ulcerative colitis), celiac disease, colorectal cancer, functional dyspepsia — share overlapping presenting symptoms (abdominal pain, bloating, altered bowel habit, dyspepsia), yet diverge enormously in consequence.

- IBS is defined by **Rome IV symptom-based criteria**: recurrent abdominal pain ≥1 day/week on average over the prior 3 months, with onset ≥6 months prior, associated with ≥2 of {related to defecation, change in stool frequency, change in stool form} [1, regulatory]. The modern ACG position is that IBS is a **positive diagnosis** made on characteristic symptom pattern *after alarm features are excluded* — NOT a label applied by default once tests come back normal [1, regulatory].
- A "positive diagnostic strategy" is non-inferior to an exhaustive strategy of exclusion for health-related quality of life [10, rct], but this presupposes alarm features have already been screened out and ruled absent [1, regulatory]. The non-inferiority result does NOT license skipping alarm-feature screening.
- Alarm features (anemia, fecal occult blood, unintentional weight loss) carry **high predictive value for organic disease** in patients otherwise meeting IBS criteria [1, regulatory]. Their presence flips the entire diagnostic frame from functional to organic.

**Why an LLM specifically must not diagnose here:** distinguishing IBS from early IBD, celiac, or CRC requires physical examination, serology/calprotectin, and frequently endoscopy with biopsy — none of which an LLM can perform or order. An LLM that pattern-matches a symptom cluster to "sounds like IBS" performs exactly the anchoring error the guidelines warn against. IBS remains a diagnosis reachable *only after* a clinician has excluded alarm features [1, regulatory]; the agent cannot perform that exclusion and therefore cannot license the label. The agent's role is to recognize alarm features and route to in-person care, never to assign or confirm a diagnostic label.

---

## C-3 Consumer / direct-to-consumer GI-test validity (load-bearing for refusing invalid tests)

### IgG / IgG4 "food sensitivity" panels — multiple allergy-society position statements: NOT validated, potentially harmful

- **EAACI Task Force (Stapel 2008):** "Testing for IgG4 against foods is not recommended as a diagnostic tool." Food-specific IgG4 reflects **immunological tolerance** (a physiologic response to dietary exposure), not hypersensitivity; measuring it for food-related complaints is "irrelevant for the laboratory work-up of food allergy or intolerance and should not be performed" [3, regulatory].
- **AAAAI** formally endorsed the EAACI IgG4 position paper, agreeing serum antibody tests cannot diagnose food allergy in the absence of history + challenge testing [4, regulatory].
- **CSACI (Carr 2012):** there is "no body of research that supports the use of this test to diagnose adverse reactions to food or to predict future adverse reactions"; the society expressed concern about DTC marketing of food-specific IgG as a "food sensitivity" detector [5, regulatory].
- **ASCIA** maintains/hosts the same position (IgG/IgG4 food testing not recommended as a diagnostic tool) [6, regulatory].

The convergence across four independent allergy societies (EAACI, AAAAI, CSACI, ASCIA) makes this the strongest refusal-class anchor in the section: IgG/IgG4 food panels are not merely low-value, they are affirmatively contraindicated and a documented driver of unnecessary food elimination.

### At-home microbiome tests (Viome, Thorne, Tiny Health, etc.) — limited analytic + clinical validity, not actionable

- A controlled benchtest of **seven DTC gut-microbiome services** using standardized reference material found methodological variability between providers was **of the same magnitude as the biological variability between different donors**; for 17 of 18 common taxa, between-method variability matched or exceeded between-donor differences (only *Haemophilus* varied less between methods than between people) [7, mechanism_review]. A result this provider-dependent cannot support an individualized health claim.
- A regulatory-framework analysis concludes DTC microbiome tests "lack analytical and clinical validity," may yield false positives/negatives, "can harm consumers who rely on them," and have "no proven value in clinical practice" with "scant" evidence for clinical utility [8, mechanism_review].

### SIBO breath-test controversy — no gold standard, poor specificity, overdiagnosis

- No perfect SIBO test exists; the nominal reference (small-bowel aspiration + quantitative culture) is invasive, unstandardized, and prone to sampling error [11, mechanism_review].
- Lactulose hydrogen breath test sensitivity/specificity ~**68% / 44%** vs quantitative culture; in one comparison **35% of IBS patients and 45% of controls** had a positive lactulose breath test while only **~4%** had SIBO confirmed by jejunal aspirate culture — a positivity rate dominated by false positives and rapid transit, not overgrowth [11, mechanism_review]. A test that is positive in nearly half of *controls* cannot ground a confident diagnosis.

### "Leaky gut" / zonulin and other unvalidated DTC panels

- The widely sold commercial zonulin ELISA does not actually measure zonulin: it was built on a sequence later shown unrelated to the zonulin protein and instead detects unknown proteins (e.g., properdin), so its readings "do not reflect actual zonulin levels" [12, mechanism_review].
- Independently, commercial-kit serum zonulin (ZO-1 IDK) showed **no significant correlation** with the gold-standard lactulose–mannitol permeability ratio in first-degree relatives of Crohn's patients [13, cohort]. The biomarker fails both at the assay level and at the physiologic-correlation level — DTC "leaky gut" panels built on it are unvalidated.

---

## C-4 Elimination-diet / restriction risks (+ disordered-eating cross-reference)

Restriction driven by invalid testing is not benign. Two harm channels:

1. **Nutritional inadequacy and food fear.** Restrictive, unsupervised elimination diets risk malnutrition and food-related anxiety that, in severe cases, progress to orthorexia or restrictive disordered eating — the food-allergy cohort documents both unsupervised-elimination prevalence and the orthorexia/disordered-eating link [14, cohort].
2. **Disordered-eating interaction.** In a food-allergy cohort, **74% of those with both food allergy and an eating disorder reported implementing an elimination diet, and only 15% had it medically supervised**; female participants showed ~**50% prevalence of eating-disorder symptoms** vs ~**6.7%** in healthy peers, with unsupervised elimination diets a significant amplifier of vulnerability to anorexia/bulimia presentations [14, cohort]. Unsupervised restriction is a documented vector into disordered eating, not a side note.

A specific compounding loop the agent must block: an invalid IgG "food sensitivity" panel [3, regulatory][5, regulatory] generates a long list of "reactive" foods → driving food-fear-based elimination → feeding orthorexia / restrictive disordered eating [14, cohort]. The invalid test is the ignition source; refusing it upstream prevents the downstream restriction cascade.

**Cross-reference (ownership boundary):** the **eating-disorder critical floor is owned by the `nutritionist` agent**, not `gi-specialist`. Section C documents the GI-side ignition mechanism (invalid food-sensitivity testing → unsupervised elimination) and the orthorexia/ARFID risk so the `gi-specialist` design can (a) refuse to endorse invalid food-sensitivity panels, and (b) hand off / defer to the nutritionist's ED floor rather than re-implement it. The `gi-specialist` must not independently prescribe or validate elimination diets; that touches the nutritionist's owned floor.

---

## C-5 Non-English literature survey (standard-mode requirement)

**Scope of survey.** The GI / gut-microbiome evidence base relevant to this section (alarm features, consumer-test validity, IgG/IgG4 panels, SIBO breath testing, zonulin) is overwhelmingly English-language and English-indexed. The originator-relevant non-English clusters worth checking are: (a) **Japanese** probiotic-strain primaries — Yakult / *Lacticaseibacillus (Lactobacillus) casei* strain Shirota (LcS); (b) **European** Nestlé / Danone strain trials (these are typically published in English even when authored in francophone/germanophone institutions); (c) **Russian** "gut bioregulator" / peptide literature.

**Databases searched.** PubMed/MEDLINE (`pubmed.ncbi.nlm.nih.gov`), PMC (`ncbi.nlm.nih.gov/pmc`), and web index via Tavily/WebSearch, restricted to the Tier-1/Tier-2 whitelist.

**Findings.**
- The Japanese LcS / Yakult program is real and substantial, but the located primaries are **published in English in English-indexed journals** (e.g., LcS-fermented-milk RCTs in healthy stressed students, prediabetic men, and type-2 diabetes cohorts — all PubMed-indexed, English). They are not non-English primaries; they are Japanese-*originated* work already inside the English index.
- The European (Nestlé/Danone) strain trials likewise surface as English-language publications.
- Russian gut-bioregulator / peptide literature did not surface any **admissible** primary (Tier-1/Tier-2 whitelisted, position-statement or controlled-trial grade) on the Section-C topics (alarm features, consumer-test validity) within the databases searched.

**Confirmed-absence statement (explicit, per standard-mode requirement):** *No admissible non-English-language primary source bearing on Section-C topics (GI alarm features, IgG/IgG4 food-panel validity, DTC microbiome-test validity, SIBO breath-test validity, zonulin/leaky-gut validity, elimination-diet harm) was located beyond English-indexed work in the databases searched (PubMed/MEDLINE, PMC, whitelisted web index). The originator-relevant Japanese LcS/Yakult and European Nestlé/Danone programs are represented in the literature by English-language, English-indexed publications; the Russian bioregulator cluster yielded no admissible Section-C-relevant primary.* The English-language convergence of the four allergy-society IgG/IgG4 statements (EAACI/AAAAI/CSACI/ASCIA) further indicates the refusal-class evidence base is not gated behind a non-English source.

---

## Key claims for the agent design (refusal-class + critical-floor implications)

1. **TIME-CRITICAL refusal class (emergency redirect, no triage dialogue):** hematemesis, melena, hematochezia with hemodynamic change, acute severe/peritoneal abdominal pain, intractable vomiting with obstruction signs, jaundice-with-fever (cholangitis). Fires unconditionally [2, regulatory][1, regulatory].
2. **Urgent-referral gate (in-person clinician before further self-management):** dysphagia/odynophagia, unintentional weight loss, iron-deficiency anemia / occult bleeding, palpable mass, new-onset GI symptoms at age ≥45 (CRC) or ≥60 (dyspepsia endoscopy), nocturnal symptoms, family history of CRC/IBD [1, regulatory][2, regulatory][9, regulatory].
3. **No-diagnosis floor:** the agent never assigns or confirms IBS / IBD / celiac / CRC / functional-dyspepsia labels. IBS is a clinician's positive diagnosis reachable *only after* alarm-feature exclusion the agent cannot perform [1, regulatory]. Anchoring on a benign functional label in the presence of an alarm feature is the named failure mode to prevent.
4. **Invalid-test refusal class:** refuse to endorse / interpret IgG or IgG4 food-sensitivity panels [3,4,5,6, regulatory], DTC at-home microbiome kits as actionable [7,8, mechanism_review], SIBO breath tests as standalone diagnoses [11, mechanism_review], and zonulin/"leaky gut" panels [12, mechanism_review][13, cohort]. State the validity problem, do not relay the result as meaningful.
5. **Restriction-cascade block (defers to nutritionist's ED floor):** the agent must not validate invalid food-sensitivity testing or prescribe unsupervised elimination diets, because that ignites the food-fear → orthorexia / restrictive-ED cascade [14, cohort]; the ED critical floor is owned by `nutritionist` and must be deferred to, not duplicated.

---

## Bibliography

1. Lacy BE, et al. (2021). "American College of Gastroenterology Clinical Guideline: Management of Irritable Bowel Syndrome." *Am J Gastroenterol* 116(1):17–44. DOI: 10.14309/ajg.0000000000001036. — `regulatory`
2. Moayyedi P, et al. (2017). "ACG and CAG Clinical Guideline: Management of Dyspepsia." *Am J Gastroenterol* 112(7):988–1013. PMID: 28631728. https://gi.org/guideline/management-of-dyspepsia-2/ — `regulatory`
3. Stapel SO, et al. (2008). "Testing for IgG4 against foods is not recommended as a diagnostic tool: EAACI Task Force Report." *Allergy* 63(7):793–796. PMID: 18489614. — `regulatory`
4. American Academy of Allergy, Asthma & Immunology (2010). "AAAAI Support of the EAACI Position Paper on IgG4." PMID: 20451986. https://www.aaaai.org/Aaaai/media/MediaLibrary/PDF%20Documents/Practice%20and%20Parameters/EACCI-IgG4-2010.pdf — `regulatory`
5. Carr S, et al. (2012). "CSACI Position statement on the testing of food-specific IgG." *Allergy Asthma Clin Immunol* 8(1):12. PMID: 22835332 / PMCID: PMC3443017. — `regulatory`
6. ASCIA (Australasian Society of Clinical Immunology and Allergy). "Testing for IgG4 against foods is not recommended as a diagnostic tool" (position, hosting EAACI consensus). https://www.allergy.org.au/hp/papers/testing-for-igg4-against-foods-is-not-recommended-as-a-diagnostic-tool — `regulatory`
7. Servetas SL, et al. (2026). "Evaluating the analytical performance of direct-to-consumer gut microbiome testing services." *Communications Biology* 9. DOI: 10.1038/s42003-025-09301-3 / PMCID: PMC12946161. — `mechanism_review`
8. (DTC microbiome regulatory-framework analysis, 2024). "Direct-to-consumer microbiome testing needs regulation" / regulatory-framework review. PMID: 38870959; PMCID: PMC12728816. https://pmc.ncbi.nlm.nih.gov/articles/PMC12728816/ — `mechanism_review`
9. Davidson KW, Barry MJ, et al. / US Preventive Services Task Force (2021). "Screening for Colorectal Cancer: US Preventive Services Task Force Recommendation Statement." *JAMA* 325(19):1965–1977. (Grade A ages 50–75; Grade B ages 45–49.) https://jamanetwork.com/journals/jama/fullarticle/2779985 — `regulatory`
10. Begtrup LM, et al. (2013). "A positive diagnostic strategy is noninferior to a strategy of exclusion for patients with irritable bowel syndrome." *Clin Gastroenterol Hepatol* 11(8):956–962. PMID: 23357491. — `rct`
11. (SIBO breath-test diagnostic-accuracy review). "Diagnosis by Microbial Culture, Breath Tests and Urinary Excretion Tests, and Treatments of Small Intestinal Bacterial Overgrowth." PMCID: PMC9952535 (lactulose breath test sens/spec ~68%/44%; high control positivity vs aspirate culture). — `mechanism_review`
12. Massier L, Chakaroun R, Kovacs P, Heiker JT (2021). "Blurring the picture in leaky gut research: how shortcomings of zonulin as a biomarker mislead the field of intestinal permeability." *Gut* 70(9):1801–1802. PMID: 33037053 / PMCID: PMC8355880. — `mechanism_review`
13. Power N, et al. (2021). "Serum Zonulin Measured by Commercial Kit Fails to Correlate With Physiologic Measures of Altered Gut Permeability in First Degree Relatives of Crohn's Disease Patients." *Front Physiol* 12. PMID: 33841181 / PMCID: PMC8027468. — `cohort`
14. Wróblewska B, et al. (2018). "Increased prevalence of eating disorders as a biopsychosocial implication of food allergy." *PLoS One* 13(6):e0198607. DOI: 10.1371/journal.pone.0198607. PMID: 29944672 / PMCID: PMC6019672. (74% of FA+/ED+ used elimination diets, only 15% medically supervised; ~50% vs ~6.7% ED-symptom prevalence.) — `cohort`

Distinct admissible primaries / position statements: **14** (society/regulator position statements + clinical guidelines: 1,2,3,4,5,6,9; controlled trial: 10; cohort: 13,14; mechanism/validity reviews: 7,8,11,12). Exceeds the ≥8 floor.

*Iter-2 note:* the prior bibliography entry [15] (Wróblewska 2018) is renumbered to [14] after removing the former non-primary entry [14] (the ScienceDirect "Topics" aggregator overview), which was mistagged `cohort`; that aggregator is an Elsevier index page, not a primary study, and grounded no numeric claim — it is removed entirely rather than retagged. All inline elimination-diet → disordered-eating cascade claims now resolve to the renumbered [14, cohort] (Wróblewska 2018), a genuine human cohort that independently carries the claim.

---

## Self-check

- **Every numeric claim is type-tagged and grounded by an admissible source (no `vendor_label`/`anecdote_aggregate` grounding numbers):**
  - USPSTF age 45 / Grade A (50–75) / Grade B (45–49) — [9, regulatory]. ✓
  - Dyspepsia endoscopy age ≥60 — [2, regulatory]. ✓
  - Lactulose breath test sens/spec ~68%/44%; 35% IBS vs 45% controls positive; ~4% aspirate-confirmed — [11, mechanism_review]. ✓
  - DTC microbiome: 7 services; 17/18 taxa methodological variability ≥ biological — [7, mechanism_review]. ✓
  - Eating-disorder cohort: 74% elimination-diet use, 15% supervised, ~50% vs ~6.7% ED-symptom prevalence — [14, cohort]. ✓
  - Rome IV ≥1 day/week / 3 months / 6 months onset — [1, regulatory]. ✓
- **Animal / in_vitro numerics requiring `[population-mismatch]`:** none. No `animal` or `in_vitro` tags are used in this section; all numerics derive from human guidelines, human RCT/cohort data, or assay-validity reviews. No population-mismatch annotation is triggered. ✓
- **No `vendor_label` or `anecdote_aggregate` tags used anywhere; no numbers sourced from vendors or anecdote aggregates.** ✓
- **Non-English literature survey documented (C-5):** scope (Japanese LcS/Yakult, European Nestlé/Danone, Russian bioregulators), databases (PubMed/MEDLINE, PMC, whitelisted web index), and explicit confirmed-absence statement provided. ✓
- **Type-tag discipline:** position statements/guidelines → `regulatory` (1,2,3,4,5,6,9); positive-vs-exclusion non-inferiority trial → `rct` (10); biomarker/test-validity critiques → `mechanism_review` (7,8,11,12); human correlation/cohort data → `cohort` (13,14). One tag per claim. ✓
- **Source count:** 14 distinct admissible primaries / society position statements (≥8 floor met; the former non-primary ScienceDirect "Topics" aggregator was removed in iter-2, dropping the count from 15 to 14). ✓
- **`risk_floor_readiness`:** N/A — Section C contains no compound/dose content (no compound dosing, route, or concentration claims); the dimension is null for this section by design. ✓
- **Cross-reference integrity:** eating-disorder critical floor explicitly attributed to `nutritionist` ownership, not duplicated here (C-4). ✓

---

## Post-fix grep audit (iter-2, iter-3)

### iter-2 audit

**Correction record (OLD → NEW):**

| Item | OLD | NEW |
|---|---|---|
| Bibliography entry: ScienceDirect "Topics" aggregator | `[14] ... — cohort` (mistagged non-primary) | **removed entirely** (not a primary; grounded no numeric claim) |
| Bibliography entry: Wróblewska 2018 ED cohort | `[15] ... — cohort` | renumbered to `[14] ... — cohort` |
| Inline citation, C-4 channel-1 (food fear/orthorexia) | `[14, cohort]` (→ aggregator) | `[14, cohort]` (→ Wróblewska, after renumber; rewritten to drop the aggregator-only claim) |
| Inline citation, C-4 cascade loop | `[14, cohort]` (→ aggregator) | removed from that node; cascade endpoint cites `[14, cohort]` (Wróblewska) only |
| Inline citation, C-4 channel-2 + Key-claim 5 + Self-check ED line | `[15, cohort]` | `[14, cohort]` |
| Source count | `15 distinct` | `14 distinct` |
| Self-check type-tag roster | `mechanism_review (7,8,11,12,14)`, `cohort (13,15)` | `mechanism_review (7,8,11,12)`, `cohort (13,14)` |

**Grep command run** (case-insensitive, whole file):
`grep -inE '\[14|15 distinct|cohort' section-C.md`

**Hits found AFTER correction + disposition:**

- **L73** `... first-degree relatives of Crohn's patients [13, cohort]` — matched on `cohort`. *Unchanged, legitimate:* this is the Power 2021 zonulin cohort [13], unrelated to the [14]/[15] renumber. Correctly tagged `cohort`.
- **L81** `... orthorexia or restrictive disordered eating — ... link [14, cohort]` — matched on `[14`/`cohort`. *Corrected:* now resolves to renumbered [14] Wróblewska 2018 (genuine cohort); claim rewritten so no clause depends on the removed aggregator.
- **L82** `... 74% ... only 15% had it medically supervised ... [14, cohort]` — matched on `[14`/`cohort` (the "15%" substring inside "15% medically supervised" is a data value, not a citation index). *Corrected:* citation now [14] Wróblewska; the "15%" is a numeric finding from that same cohort, correctly grounded.
- **L84** `... feeding orthorexia / restrictive disordered eating [14, cohort].` — matched on `[14`/`cohort`. *Corrected:* cascade endpoint now cites renumbered [14] Wróblewska; the mid-cascade aggregator citation was deleted (cascade prose needs no separate citation for the elimination step).
- **L110** `... zonulin/"leaky gut" panels [12, mechanism_review][13, cohort].` — matched on `cohort`. *Unchanged, legitimate:* [13] Power 2021 cohort, unrelated to renumber.
- **L111** `... food-fear → orthorexia / restrictive-ED cascade [14, cohort];` — matched on `[14`/`cohort`. *Corrected:* now renumbered [14] Wróblewska (was [15]).
- **L129** `13. Power N, et al. (2021). ... — cohort` — matched on `cohort`. *Unchanged, legitimate:* bibliography entry [13], correctly `cohort`.
- **L130** `14. Wróblewska B, et al. (2018). ... only 15% medically supervised ... — cohort` — matched on `[14`(via "14.")/`15`/`cohort`. *Corrected:* this is the renumbered [14] entry (was [15]); the embedded "15%" is the supervised-elimination data value, correctly part of this cohort's findings.
- **L132** `Distinct admissible primaries ... **14** ... cohort: 13,14 ...` — matched on `[14`(via "14")/`cohort`. *Corrected:* count is now 14; cohort roster is 13,14 (was 13,15).
- **L134** `*Iter-2 note:* the prior bibliography entry [15] (Wróblewska 2018) is renumbered to [14] ... former non-primary entry [14] (the ScienceDirect "Topics" aggregator) ...` — matched on `[14`. *Intentional, legitimate:* this is the iter-2 provenance note documenting the renumber/removal. The "[15]" and "[14]" here are historical references in narrative, not live citations.
- **L145** `Eating-disorder cohort: 74% ... 15% supervised ... — [14, cohort]. ✓` — matched on `[14`/`15`/`cohort`. *Corrected:* Self-check attestation now cites [14] Wróblewska; "15%" is the data value.
- **L150** `Type-tag discipline: ... cohort (13,14). ...` — matched on `[14`(via "14")/`cohort`. *Corrected:* cohort roster now 13,14 (was 13,15); mechanism_review roster dropped the former [14] aggregator.

**Audit conclusion:** every live elimination-diet → disordered-eating cascade claim now grounds on [14] Wróblewska 2018 (a genuine human cohort, correctly tagged `cohort`). The non-primary ScienceDirect "Topics" aggregator is removed entirely and grounds no claim. No inline numeric claim is grounded by a non-primary aggregator. All `cohort` tags resolve to admissible human studies ([13] Power 2021, [14] Wróblewska 2018). Source count reconciled to 14 (≥8 floor intact). Remaining "15" string-matches are all the in-data "15% medically supervised" finding or the historical "[15]" in the iter-2 note — neither is a stray live citation.

### iter-3 audit

**Defect:** citation_fidelity — bibliography entry [14] (Wróblewska 2018) carried article-number `e0198940`, which is wrong. Verified against the resolving source (PMCID PMC6019672) via WebFetch: the page serves `PLoS One. 2018 Jun 26;13(6):e0198607. doi: 10.1371/journal.pone.0198607`.

**Correction record (OLD → NEW):**

| Item | OLD | NEW |
|---|---|---|
| Entry [14] article-number / e-locator | `e0198940` | `e0198607` |
| Entry [14] DOI | (none listed) | `10.1371/journal.pone.0198607` (added, from resolving source) |
| Entry [14] author / year / PMID / PMCID | Wróblewska B 2018 / PMID 29944672 / PMCID PMC6019672 | unchanged (confirmed correct against source) |

**Grep command run** (case-insensitive, whole file):
`grep -inE '0198940|0198607|Wróblewska|Wroblewska' section-C.md`

**Hits found AFTER correction + disposition:**

- `0198940`: **zero hits as a live citation** — the wrong article-number is fully removed from the bibliography and all citing prose. The only `0198940` strings remaining in the file are inside THIS iter-3 audit trail (this defect statement, the OLD→NEW table row, the grep-command literal, and the conclusion), where recording the OLD value is mandated by the grep-discipline. None is a live citation. ✓
- **L130** `14. Wróblewska B, et al. (2018). ... *PLoS One* 13(6):e0198607. DOI: 10.1371/journal.pone.0198607. PMID: 29944672 / PMCID: PMC6019672. ... — cohort` — matched on `0198607`/`Wróblewska`. *Corrected:* this is the bibliography entry, now carrying the verified `e0198607` + DOI. Author/year/PMID/PMCID unchanged.
- **L134** `*Iter-2 note:* the prior bibliography entry [15] (Wróblewska 2018) is renumbered to [14] ...` — matched on `Wróblewska`. *Unchanged, legitimate:* iter-2 provenance narrative; references the author by name, carries no article-number, so the iter-3 fix does not touch it.
- **L164** `| Bibliography entry: Wróblewska 2018 ED cohort | ... |` — matched on `Wróblewska`. *Unchanged, legitimate:* iter-2 audit correction-record row; documents the [15]→[14] renumber, not the article-number, so out of iter-3 scope.
- **L177–L189** (iter-2 audit body + conclusion) — several `Wróblewska` matches. *Unchanged, legitimate:* iter-2 audit prose attributing the cascade claims to Wróblewska by author name; none cites an article-number, so the iter-3 article-number fix leaves them correct as written.

**iter-3 audit conclusion:** the wrong article-number `e0198940` is fully purged (zero hits); the sole bibliographic instance now reads the source-verified `e0198607` with its matching DOI `10.1371/journal.pone.0198607`. PMID/PMCID/author/year were confirmed correct and left untouched. All remaining `Wróblewska` hits are author-name references in narrative (the bibliography entry itself plus the iter-2 audit), none of which restates an article-number, so no further edits are required. The renumbered [14] cohort still independently grounds every live elimination-diet → disordered-eating cascade claim.
