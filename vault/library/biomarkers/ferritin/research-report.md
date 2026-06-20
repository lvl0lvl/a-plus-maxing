---
title: "Serum Ferritin: Canonical Research Report"
type: research-report
permalink: a-plus-maxing/library/biomarkers/ferritin/research-report
created: 2026-06-20
last_verified: 2026-06-20
review_cadence: per-lab-panel
provenance_dir: design/.ferritin-design-work
provenance_slug: labs-specialist
source_count: 35
---

# Serum Ferritin: Canonical Research Report

## Summary

Serum ferritin is the body's principal iron-storage marker — the best single laboratory test for assessing iron stores — and under non-inflammatory, steady-state conditions it tracks storage iron with reasonable fidelity (approximately 1 ng/mL ≈ 8–10 mg of stored iron). At the same time, ferritin is a **positive acute-phase reactant**: inflammatory cytokines drive hepatic and macrophage ferritin synthesis independently of iron status, so a normal or elevated ferritin does **not** exclude iron deficiency when inflammation, infection, or chronic disease is present. This duality — iron-stores mirror and acute-phase protein — is the central interpretive challenge. A low ferritin is essentially diagnostic of iron depletion; a high ferritin is, in most clinical contexts, far more likely to reflect inflammation, liver disease, or metabolic dysfunction than iron overload.

Ferritin is reported in ng/mL (numerically identical to µg/L, a 1:1 equivalence). Reference ranges are wide and sex-dependent: approximately 30–300 ng/mL in adult men and 13–150 ng/mL in adult women, with postmenopausal women converging toward male ranges. Three iron-deficiency cutoffs are in active clinical use: **< 15 ng/mL** (high specificity ~99%, sensitivity ~59%) [14, meta_analysis]; **< 30 ng/mL** (the current BSG and WHO operational standard; Cochrane 2021 evidence: 79% sensitivity, 98% specificity) [12, meta_analysis; 15, regulatory; 16, regulatory]; and **< 45–50 ng/mL** favoured by bodies seeking to maximize sensitivity in high-prevalence populations [13, meta_analysis]. When inflammation is present, these thresholds must be adjusted upward: WHO recommends < 70 ng/mL with concurrent high CRP; ESC heart-failure guidelines define absolute iron deficiency at < 100 ng/mL and functional deficiency at 100–299 ng/mL with TSAT < 20% [16, regulatory; 18, regulatory]; KDIGO extends the treatment trigger in dialysis patients to ≤ 500 ng/mL with TSAT ≤ 30% [17, mechanism_review].

There is no firm upper disease threshold for ferritin elevation. Values above 1,000 ng/mL widen the differential substantially — hemochromatosis, hemophagocytic lymphohistiocytosis (HLH), adult-onset Still's disease, hepatocellular disease, and systemic malignancy all drive marked elevation. True iron overload (hereditary hemochromatosis) requires **TSAT > 45% plus HFE genotyping** to establish; ferritin in this context is a severity marker, not a primary diagnostic test.

Ferritin is measured exclusively by immunoassay, but the assay landscape is poorly harmonized: inter-platform coefficients of variation exceed 22–23% on the same specimens [22, mechanism_review], meaning fixed numeric thresholds are not platform-agnostic. An additional pitfall is the **hook effect**: at extreme ferritin concentrations, antigen excess paradoxically suppresses the immunoassay signal, yielding falsely low readings — a clinically dangerous artifact in HLH and other hyperferritinemia emergencies [24, cohort; 25, cohort].

Serum ferritin should always be interpreted alongside **C-reactive protein (CRP)** to quantify the inflammatory contribution, **transferrin saturation (TSAT)** to assess iron availability for erythropoiesis, and — when inflammation complicates interpretation — **soluble transferrin receptor (sTfR)**, which rises with iron-deficient erythropoiesis and is not an acute-phase reactant [28, mechanism_review].

---

## Physiology & What Serum Ferritin Measures

### The Iron-Storage Nanocage

Ferritin is the body's principal intracellular **iron-storage protein**, a ~450 kDa hollow nanocage assembled from **24 protein subunits** of two distinct types: the **H (heavy) chain** (FTH1, ~21 kDa, 182 amino acids) and the **L (light) chain** (FTL, ~19 kDa, 174 amino acids) [1, mechanism_review; 2, mechanism_review]. The two subunit types perform complementary but separable roles. The **H-chain carries a ferroxidase center** — a di-iron catalytic site that rapidly oxidises soluble ferrous iron (Fe²⁺) to the less reactive ferric form (Fe³⁺), a critical first step that prevents Fenton-reaction chemistry and the cascade of free-radical damage that unsequestered iron would otherwise trigger [3, mechanism_review; 4, mechanism_review]. The **L-chain** lacks ferroxidase activity but contributes to **nucleation and mineralisation** of the ferrihydrite iron core within the protein shell, aiding long-term iron packing and stability [3, mechanism_review].

The completed 24-subunit cage — sometimes called apoferritin when iron-free — forms a roughly spherical shell with an outer diameter of ~12 nm and an internal cavity (~8 nm diameter) capable of sequestering **up to approximately 4,500 Fe³⁺ atoms** as a ferrihydrite mineral core [4, mechanism_review; 5, mechanism_review]. This architecture achieves two goals simultaneously: it renders iron non-toxic (by converting it to a non-reactive mineral phase and shielding it from aqueous redox chemistry) and keeps it biologically available for rapid mobilisation when iron demand rises [2, mechanism_review].

The **H:L ratio is not fixed — it is tissue-specific** and physiologically regulated. Tissues with high iron-oxidation demands (heart, brain, kidney) favour H-chain-rich isoforms; iron-storage organs (liver, spleen) produce predominantly L-chain-rich ferritin, which excels at packing large amounts of iron over the long term [4, mechanism_review; 5, mechanism_review]. This heterogeneity means "ferritin" is not a single molecular species but a family of isoforms whose biochemical properties vary with tissue context.

### Intracellular Distribution

The dominant pool of ferritin in the body is **intracellular**, concentrated in hepatocytes and Kupffer cells of the liver, splenic and bone-marrow macrophages, and more broadly across the **reticuloendothelial system (RES)** [2, mechanism_review; 6, mechanism_review]. Macrophages in the spleen and liver are responsible for erythrophagocytosis — the catabolism of senescent red cells and recycling of their haem iron — and they rely heavily on ferritin to transiently sequester this recycled iron (approximately 20–25 mg per day) before it re-enters circulation bound to transferrin [6, mechanism_review].

### Serum Ferritin: A Small but Informative Secreted Fraction

**Serum ferritin is a minor secreted fraction** of total body ferritin, and its molecular character differs systematically from its intracellular counterpart. Circulating ferritin is [3, mechanism_review; 7, mechanism_review; 8, mechanism_review]:

- **Predominantly L-subunit rich** (the preponderance of serum ferritin is immunologically related to ferritin-L)
- **Relatively iron-poor** (iron-poor L-subunit ferritins are preferentially released; iron-loaded H-subunit ferritins are sequestered locally)
- **Glycosylated** in 50–80% of the circulating pool under normal conditions, a signature of regulated secretory release rather than passive cellular leakage
- **Actively secreted** via nonclassical vesicular export pathways (secretory autophagy and multivesicular body–exosome routes), not simply spilled from dying cells — though tissue injury does add a non-glycosylated, iron-rich fraction

The regulation of ferritin export is only partially understood, but the available data confirm it is not a passive overflow [8, mechanism_review]. Mutations in endolysosomal trafficking machinery (BLOC complexes, Rab27A) alter circulating ferritin levels, demonstrating that secretion is subject to molecular regulation. The practical implication for interpretation: **when glycosylation falls below ~50% of serum ferritin, this signals a greater contribution from cell damage or iron overload** — and the proportion matters clinically [7, mechanism_review].

### The Load-Bearing Concept: Serum Ferritin Reflects Iron Stores — Under Steady Conditions

Under **non-inflammatory, steady-state conditions**, serum ferritin tracks total-body iron stores with reasonable fidelity. The widely cited conversion is approximately **1 ng/mL (= 1 µg/L) of serum ferritin ≈ 8–10 mg of storage iron** in healthy adults [9, mechanism_review]. Because total iron stores in replete adults typically range from ~500 mg (women) to ~1,500 mg (men), serum ferritin values in the mid-normal range (roughly 30–150 ng/mL) span most of this physiological variation. At the deficiency end, **serum ferritin < 15 ng/mL is a reliable indicator of absent iron stores**, essentially independent of the inflammatory state; at the repletion-to-overload end, a rising serum ferritin signals expanding storage iron in the liver and RES [9, mechanism_review; 6, mechanism_review]. This is why, in a non-inflamed individual, serum ferritin stands as the single most diagnostically powerful test for iron deficiency — far superior to serum iron alone.

### Dual Regulation: The Crux of Clinical Interpretation

Serum ferritin is governed by **two independent regulatory axes**, and this duality is the source of both its clinical power and its central limitation.

**Axis 1 — Iron-responsive (post-transcriptional, IRE/IRP):**
Intracellular ferritin synthesis is controlled by the **IRE/IRP (iron-responsive element / iron-regulatory protein) system**. H- and L-ferritin mRNAs each carry a stem-loop **IRE in their 5′ untranslated region**. When intracellular iron is scarce, IRP1 and IRP2 bind the IRE and **block ribosomal access, suppressing ferritin translation** — keeping iron available for haemoglobin synthesis and other essential functions. When iron is replete, iron-loaded IRP1 is converted to cytosolic aconitase (losing IRE-binding affinity) and IRP2 undergoes proteasomal degradation, **releasing the translational block and permitting ferritin synthesis** to safely sequester the surplus [1, mechanism_review; 6, mechanism_review]. This elegant post-transcriptional rheostat ensures that ferritin abundance tracks the immediate cellular iron economy.

**Axis 2 — Inflammation-responsive (transcriptional, cytokine-driven):**
Ferritin synthesis is also regulated **at the transcriptional level** by inflammatory cytokines. **IL-1β, IL-6, and TNF-α** stimulate ferritin gene expression in hepatocytes and macrophages through the **NF-κB signalling pathway**, decoupling ferritin production from actual iron stores [3, mechanism_review; 4, mechanism_review]. This makes ferritin a **positive acute-phase reactant**: serum ferritin rises with infection, autoimmune flares, malignancy, liver disease, and any sustained systemic inflammatory signal — regardless of whether body iron stores have changed. Notably, **IL-6** also drives transcription of **hepcidin** (via JAK2–STAT3 signalling), the 25-amino-acid liver peptide that is the master systemic iron regulatory hormone: hepcidin binds and degrades **ferroportin** (the sole known cellular iron exporter) in enterocytes, macrophages, and hepatocytes, thereby sequestering iron within cells, raising intracellular ferritin further, and simultaneously curtailing iron absorption [6, mechanism_review; 10, mechanism_review]. This cytokine–hepcidin–ferritin axis underlies the classical picture of **anemia of inflammation** — high serum ferritin alongside functional iron deficiency.

### Why This Matters: Serum Ferritin Is Not a Simple Iron Gauge

The practical consequence of dual regulation is that **the serum ferritin number cannot be interpreted without knowing the inflammatory context**. A ferritin of 80 ng/mL in a healthy, non-inflamed individual is reassuring (iron stores present, no deficiency). The same number in a patient with active rheumatoid arthritis may mask severe iron depletion that a standard cut-off would miss — because cytokine-driven transcriptional induction has elevated ferritin independently of stores. For this reason, serum ferritin is always best interpreted alongside **C-reactive protein (CRP)** and **transferrin saturation (TSAT)**: a low TSAT (< 20%) in the presence of even a "normal" ferritin, particularly if CRP is elevated, is grounds for suspecting functional iron deficiency.

---

## Reference Ranges, Units & The Iron-Deficiency Threshold Debate

### Units and Measurement

Serum ferritin is reported in **ng/mL**, numerically identical to µg/L — a 1:1 equivalence that eliminates unit-conversion error when comparing assays or guidelines expressed in either notation.

### Reference Intervals: Wide, Age- and Sex-Dependent

Ferritin reference intervals are broad and population-specific. Commonly cited approximate ranges are **30–300 ng/mL in adult men** and **13–150 ng/mL in adult women**, with postmenopausal women typically converging toward male ranges after cessation of menstrual blood loss [11, mechanism_review]. Because ferritin reflects cumulative iron stores built over years of dietary intake and physiological iron recycling, males accumulate higher stores than premenopausal females throughout adulthood.

Critically, published reference intervals vary substantially across clinical laboratories and assay platforms. A value that falls within one laboratory's "normal" range may fall below another's lower threshold — a recognized measurement harmonisation problem. This is one reason threshold debates turn on diagnostic accuracy evidence rather than reference-range consensus alone [12, meta_analysis]. A systematic review published in Lancet Haematology in 2024 found that laboratory-reported lower limits of normal are frequently set too low — often well below 30 µg/L — lacking rigorous scientific grounding and likely contributing to structural underdiagnosis of iron deficiency across populations [29, meta_analysis].

### The Core Threshold Debate: Where Does Iron Deficiency Begin?

Three cutoffs dominate clinical practice, each reflecting a different priority.

#### The Classic Cutoff: < 15 ng/mL

The oldest widely used threshold, endorsed by historical WHO guidance and standard laboratory reference intervals, defines iron deficiency at ferritin **below 15 ng/mL**. At this cutoff, specificity for depleted bone marrow iron stores is approximately **99%** — meaning a positive test at this level almost never represents a false alarm [14, meta_analysis]. The practical consequence is that a value below 15 ng/mL needs no further corroboration: iron stores are definitively absent.

The cost is sensitivity. The same evidence base shows that using < 15 ng/mL catches only **59% of truly iron-deficient individuals** [14, meta_analysis]. In other words, more than four in ten iron-deficient patients are missed if the clinician acts only when ferritin falls below 15. This matters most in ambulatory settings — fatigue clinics, primary care, obstetrics — where iron deficiency without overt anemia is common and the pre-test probability is substantial.

The original landmark evidence establishing ferritin's superiority over other iron markers came from the **Guyatt 1992 meta-analysis**, which synthesised **55 studies** that compared laboratory tests to the gold standard of bone marrow biopsy [14, meta_analysis]. Ferritin produced the highest area under the receiver-operating-characteristic curve (AUROC = 0.95) of any single test, surpassing serum iron, transferrin saturation, red cell protoporphyrin, and mean corpuscular volume. Critically, the study documented how likelihood ratios varied continuously across the ferritin range rather than at any single threshold — foreshadowing the ongoing debate about where to draw the line.

#### The Sensitivity-Optimising Cutoff: < 30 ng/mL

Most contemporary haematology and gastroenterology guidelines have moved to **< 30 ng/mL** as the operational threshold. The British Society of Gastroenterology (BSG) 2021 guidelines define a ferritin below 30 µg/L as indicative of low body iron stores in the absence of inflammation, distinguishing this from the < 15 ng/mL threshold that signals absent stores [15, regulatory]. The WHO's 2020 guideline on ferritin concentrations similarly anchors its primary adult threshold at this level for standard populations [16, regulatory].

The rationale is that ferritin can be spuriously normal in the 15–30 range in patients with genuine iron depletion — particularly if those patients have any subclinical inflammatory stimulus that raises ferritin toward or above 15 even while stores decline. Applying < 30 recovers a meaningful fraction of these missed cases. The 2021 Cochrane review by Garcia-Casal et al. provides the most rigorously synthesised diagnostic-accuracy estimate currently available: at a 30 µg/L threshold, ferritin achieves **79% sensitivity and 98% specificity** for iron deficiency in adults presenting for medical care [12, meta_analysis].

#### The High-Sensitivity Cutoff: < 45–50 ng/mL

A third position, increasingly supported by physiological and diagnostic-accuracy evidence, recommends a threshold of **< 45–50 ng/mL** to maximise sensitivity without unacceptable loss of specificity. Peyrin-Biroulet and colleagues (2015) conducted a systematic review of 127 guidelines (29 selected) across multiple clinical indications and concluded that a ferritin cutoff of **< 100 µg/L** should be considered in most conditions when diagnosing iron deficiency — reflecting a broad consensus that the classical < 15–30 ng/mL thresholds under-diagnose iron deficiency in clinical practice [13, meta_analysis]. For standard outpatient populations without overt inflammation, the < 45–50 ng/mL range is endorsed by bodies such as the American Gastroenterological Association on the grounds that physiological iron absorption increases below approximately 51 ng/mL and remains stable above it, suggesting the body's regulatory machinery treats stores below this level as functionally suboptimal [9, mechanism_review].

#### Why the Debate Persists

The three cutoffs reflect genuinely different clinical priorities rather than a simple right-versus-wrong dispute. In a setting requiring high confidence before a diagnosis (e.g., ruling out iron deficiency as a cause of symptoms in a patient with comorbidities), the high-specificity < 15 ng/mL anchor may be appropriate. In high-prevalence settings — menstruating women, pregnant patients, athletes, inflammatory bowel disease — a < 30 or < 45 ng/mL threshold is more likely to identify the patients who will benefit from treatment. The movement in guidelines is broadly toward the higher cutoffs precisely because undiagnosed iron deficiency in ambulatory populations carries underappreciated morbidity.

### The Inflammation Adjustment: The Most Load-Bearing Caveat

Ferritin is an **acute-phase reactant**. Infection, tissue injury, malignancy, and chronic inflammatory conditions all drive hepatic and macrophage ferritin synthesis independently of iron stores via pro-inflammatory cytokines (IL-1β, TNF-α) acting through the NF-κB pathway [3, mechanism_review]. The practical consequence is that a patient with genuine iron deficiency can have a ferritin value in the nominally normal range — 30–100 ng/mL — simply because inflammation has artificially inflated it.

Guideline responses to this problem:

- **WHO 2020:** Recommends raising the cutoff to **< 70 ng/mL in adults** when infection or inflammation is present (CRP > 5 mg/L or elevated α-1 acid glycoprotein) [16, regulatory].
- **ESC 2021 Heart Failure Guidelines:** Define iron deficiency in heart failure using a two-tier schema — **absolute deficiency** at ferritin **< 100 ng/mL**, and **functional deficiency** when ferritin is 100–299 ng/mL but transferrin saturation (TSAT) is **< 20%** [18, regulatory]. Both categories warrant iron repletion, typically intravenous given gastrointestinal absorption barriers in this population.
- **KDIGO (CKD):** In non-dialysis CKD, ferritin **< 100 ng/mL** is commonly used to signal iron deficiency; in dialysis patients, international guidance extends the treatment trigger to ferritin ≤ 500 ng/mL with TSAT ≤ 30%, reflecting the profound inflammatory burden in end-stage kidney disease [17, mechanism_review].

The absolute/functional distinction is mechanistically coherent: in chronic disease, hepcidin is chronically elevated, diverting iron into macrophages and hepatocytes and blocking intestinal absorption. Even when total body iron appears adequate by ferritin, iron availability for erythropoiesis is impaired — hence "functional" deficiency despite non-low ferritin.

### The High End: Elevated Ferritin and Its Differential

There is no firm upper disease threshold — elevated ferritin does not define a single condition. Values above 1,000 ng/mL dramatically broaden the differential: haemochromatosis, haemophagocytic lymphohistiocytosis, adult-onset Still's disease, hepatocellular disease, and systemic malignancy all drive marked elevation. Ferritin in this range must be interpreted alongside clinical context, transferrin saturation, liver enzymes, and often further imaging or genetic testing.

### Ferritin Cannot Be Interpreted in Isolation

A single ferritin value without supporting context is often uninterpretable. The minimum interpretive panel is:

1. **CRP** (or other inflammatory marker) — to detect acute-phase inflation that may be masking iron deficiency or falsely elevating a borderline result.
2. **Transferrin saturation (TSAT)** — the ratio of serum iron to TIBC; below 20% with a borderline ferritin strongly supports functional iron deficiency.
3. **Clinical context** — menstrual status, pregnancy, chronic disease burden, symptom pattern, dietary history.

In ambiguous cases, soluble transferrin receptor (sTfR), reticulocyte haemoglobin content, and hepcidin measurement provide additional resolution, particularly when ferritin is raised by inflammation but iron deficiency is still suspected.

---

## Measurement & Standardization

### Assay Platforms and Mechanism

Serum ferritin is measured almost exclusively by immunoassay. Three principal platform families are in routine clinical use.

**Immunoturbidimetric and latex-enhanced nephelometric assays** mix patient serum with latex particles coated with anti-ferritin antibodies. Ferritin in the sample crosslinks the particles, increasing the turbidity of the solution; the change in absorbance (turbidimetry) or in light-scatter at a defined angle (nephelometry) is proportional to ferritin concentration. These methods are rapid and easily automated on general chemistry analyzers. Their linear range is narrower than dedicated immunometric platforms, and they can read falsely high at antigen excess — a point returned to below.

**Chemiluminescent immunoassays (CLIA) and electrochemiluminescent assays (ECLIA)** use a two-antibody sandwich architecture: a capture antibody immobilizes ferritin, a second labeled antibody generates a light signal proportional to bound antigen. This format is the workhorse of dedicated immunoanalyzers (e.g., Roche Cobas e series, Abbott Alinity i, Siemens Centaur) and delivers the high throughput and broad dynamic range needed for clinical throughput.

**ELISA (enzyme-linked immunosorbent assay)** is the classic manual-to-semi-automated sandwich format: capture → wash → enzyme-conjugated detection antibody → wash → substrate → colorimetric or fluorometric readout. ELISA is widely used in research, nutrition surveys, and lower-resource settings. Comparative data show close agreement between ELISA and ECLIA but divergence versus immunoturbidimetric platforms, particularly at mid-range concentrations [19, cohort; 20, cohort].

Crucially, these assays do not measure iron content directly. They detect ferritin protein by binding to epitopes on the shell — predominantly on the L (light) subunit, which predominates in secreted serum ferritin. Because serum ferritin is the glycosylated, largely iron-poor form secreted primarily by macrophages and hepatocytes rather than the iron-laden intracellular storage form, the immunoassay signal correlates with iron stores only indirectly and breaks down when inflammation, tissue injury, or disease upregulates ferritin synthesis independent of body iron [21, mechanism_review].

### Standardization: A Historically Poor Track Record

Despite decades of clinical use, ferritin remains one of the least harmonized analytes in routine laboratory medicine. Studies directly comparing commercial platforms on the same patient specimens consistently find inter-assay coefficients of variation exceeding 15–23% — well above the desirable analytical performance specifications for clinical use [22, mechanism_review]. The direct implication: a result of 28 ng/mL on one platform is not the same measurement as 28 ng/mL on another, and applying a fixed threshold across platforms introduces systematic misclassification.

The root cause is calibration fragmentation. Ferritin immunoassays across different manufacturers have been traceable to different primary reference materials at different points in time — and some continue to be, even now.

**The WHO International Standard** for serum ferritin has gone through four generations:
- **IS 80/602** (spleen-derived human ferritin, 1985) and **IS 80/578** (also spleen-derived, 1985) — the original primary standards, now depleted.
- **IS 94/572** (3rd International Standard, 1997) — a recombinant L-chain ferritin preparation, this became the dominant calibrant for most platforms.
- **IS 19/118** (4th International Standard, 2022) — the current WHO IS, also recombinant human L-chain ferritin, prepared by NIBSC. IS 19/118 has an assigned potency of 10.5 µg/ampoule and was established in an international collaborative study across 12 laboratories in 9 countries; it supersedes 94/572 [23, mechanism_review].

The harmonization problem is not resolved by the existence of this standard, because adoption is uneven. Braga et al. (2022), in a rigorous four-platform study published in *Clinical Chemistry*, found that two of them — the Abbott Alinity and Roche Cobas — remained traceable to the long-depleted IS 80/602 rather than to IS 94/572, creating independent calibration hierarchies in simultaneous clinical use (the study also assessed the Beckman Coulter Access Dxl and Siemens Advia Centaur CP). The study reported highly significant between-platform differences (P < 0.00001) with a median inter-assay CV of **22.9%** [22, mechanism_review]. This is the direct parallel to the well-known 25-hydroxyvitamin D harmonization problem: the same specimen, the same population, different analyzers — meaningfully different numbers.

The practical implication for threshold-based clinical decisions (e.g., ferritin < 30 ng/mL for iron deficiency) is that no single cutoff is fully platform-agnostic. Published reference ranges and diagnostic thresholds were derived on specific assay generations; applying them to a different platform without commutability verification can silently shift the classification. Laboratories implementing new analyzers should perform method-comparison studies bridging to the previous platform before applying the same decision thresholds.

### The Hook Effect: A Clinically Dangerous Pitfall

In one-step sandwich immunoassays, patient serum, capture antibody (bound to solid phase), and signal antibody (enzyme- or luminescent-labeled) are all combined simultaneously. At physiologically normal ferritin concentrations, each ferritin molecule binds one capture antibody and one signal antibody, forming a stable sandwich that generates a signal proportional to analyte concentration. At very high ferritin concentrations (antigen excess), free antigen molecules compete with sandwiched complexes for both antibody partners: capture sites become saturated with single antibodies bound to one ferritin, and excess free antigen competes with already-bound complexes for signal antibody, leaving fewer complete sandwiches. The result is paradoxically **reduced signal at extremely elevated concentration** — the instrument reports a falsely low (or even near-normal) ferritin value [24, cohort; 25, cohort].

This is not a theoretical artifact. Wu and Hayden (2018) documented on the Siemens Centaur XP platform that hook effect appeared in samples with ferritin as low as 86,028 µg/L (86 µg/mL) without upfront dilution; when mandatory 5-fold pre-dilution was applied, no hook effect was observed up to 126,050 µg/L [25, cohort]. In a pediatric case series following CAR-T cell therapy, a patient's in-house ferritin measurement was more than 1,000-fold lower than the dilution-confirmed true value at a reference laboratory — a clinically critical error in a context where ferritin is the primary severity marker for immune effector cell-associated hemophagocytic lymphohistiocytosis-like syndrome [24, cohort].

**Clinical contexts where hook effect must be considered:** hemophagocytic lymphohistiocytosis (HLH), adult-onset Still's disease, macrophage activation syndrome, severe sepsis with secondary HLH features, and extreme iron overload. When the clinical picture demands a very high ferritin — markedly ill patient, cytopenias, splenomegaly, fever — and the reported value is paradoxically normal or merely modestly elevated, the laboratory should be alerted immediately to dilute and re-run the sample.

Two-step assays (which wash away unbound antigen before adding signal antibody) are substantially less susceptible to hook effect, but are not completely immune. The laboratory's declared methodology and dynamic range should always be checked when extreme hyperferritinemia is clinically suspected.

### Heterophile and Anti-Reagent Antibody Interference

Approximately 0.1% of patients carry circulating heterophile antibodies — broadly reactive immunoglobulins (often induced by animal exposure or subclinical infections) that can bind the animal-derived capture or detection antibodies used in ferritin assays. Depending on which antibody pair is affected, the result can be falsely elevated or falsely suppressed. Blanco and Varela (2006) documented falsely elevated ferritin (mean 244 µg/L versus 76 µg/L on an unaffected platform) in 13 of 13,143 samples on the Olympus ferritin assay; pretreatment with heterophilic blocking tubes normalized the values [26, cohort]. Discordance between platforms — particularly a markedly elevated result on one assay that does not match the clinical picture — should prompt heterophile antibody investigation.

### Glycosylation, Isoform Composition, and the Non-Identity of Serum and Tissue Ferritin

Intracellular ferritin (the storage form) is a 24-subunit heteropolymer of H and L chains assembled in the cytoplasm; it is not glycosylated and is iron-rich. The ferritin that circulates in serum is a distinct entity: it is predominantly L-subunit in composition, largely iron-poor (iron content 10–30% of intracellular ferritin at best), and bears N-linked glycosylation acquired during transit through secretory vesicles. Current evidence places its primary cellular source in macrophages, secreted via a nonclassical vesicular pathway rather than classical ER–Golgi exocytosis [21, mechanism_review]. Commercial immunoassays are calibrated against recombinant L-chain ferritin (WHO IS 19/118) and predominantly detect the L-rich glycosylated serum form.

The consequence: serum ferritin is not a direct measure of tissue iron content. It correlates with body iron stores across the population, but the correlation is confounded by any process that upregulates ferritin gene expression independent of iron — acute-phase response (IL-6, TNF-α, IL-1β all upregulate ferritin transcription), liver disease (leakage), malignancy, and alcohol. The assay cannot distinguish an elevated ferritin caused by iron overload from one caused by inflammation.

### Pre-Analytic Considerations and Companion Tests

Ferritin is pre-analytically robust: it is stable in serum or EDTA-plasma at 4°C for at least 5 days, and in samples frozen at −80°C for 3–5 years without significant degradation [27, cohort]. Both serum and EDTA-plasma are acceptable; plasma values average approximately 7% lower than serum on some platforms, a difference within most assay imprecision. Hemolysis is not a major interferent for ferritin (unlike hemoglobin-based analytes), but grossly lipemic samples may affect turbidimetric assays.

Because ferritin is an acute-phase reactant, it should not be interpreted in isolation. A full iron panel adds essential context:

- **Transferrin saturation (TSAT)** — serum iron ÷ TIBC × 100; low TSAT (< 20%) with low ferritin confirms functional iron deficiency; low TSAT with high ferritin suggests anemia of chronic disease or functional iron deficiency in inflammation.
- **Transferrin / TIBC** — inversely reflects iron stores; rises in iron deficiency.
- **Soluble transferrin receptor (sTfR)** — shed from erythroid precursor surface in proportion to erythropoietic iron demand. Crucially, sTfR is **not an acute-phase reactant** — it remains elevated in true iron deficiency even during inflammatory states where ferritin is falsely normal or elevated [28, mechanism_review]. The sTfR-to-log-ferritin index improves discrimination of iron-deficiency anemia from anemia of chronic disease.
- **Reticulocyte hemoglobin content (CHr/Ret-He)** — reflects the iron available for erythropoiesis in the most recent red cell cohort; a functional iron deficiency marker independent of iron stores.

---

## Determinants & Clinical Significance

Serum ferritin is not a single-meaning test. Its direction of deviation carries asymmetric diagnostic weight: a low ferritin is among the most specific tests in clinical medicine, while an elevated ferritin is a broad, non-specific signal that demands systematic unpacking before any conclusion about iron status is drawn.

### Low Ferritin: The Most Specific Direction

A serum ferritin below 15–30 ng/mL is the single most specific laboratory test for iron deficiency, reflecting genuinely depleted storage iron [29, meta_analysis]. Unlike most biomarkers, almost nothing other than true iron depletion causes the ferritin to fall: it does not drop with inflammation, infection, or acute illness — it rises. This unidirectional specificity means a low result is essentially diagnostic: if ferritin is below the assay's lower reference limit, iron stores are empty.

**Principal causes of true (absolute) iron deficiency by mechanism:**

- **Blood loss — the dominant cause in adults.** Occult gastrointestinal (GI) bleeding is the leading etiology in men and postmenopausal women; the 2021 BSG guidelines mandate bidirectional endoscopic evaluation in these groups because approximately one-third will have an underlying structural lesion, often GI malignancy [15, regulatory]. Heavy menstrual bleeding is the leading cause in premenopausal women. Frequent blood donors represent a well-documented iatrogenic source.

- **Malabsorption.** Celiac disease is under-recognized as a cause of refractory iron deficiency and should be tested in all cases of unexplained deficiency [15, regulatory]. Inflammatory bowel disease (IBD), atrophic gastritis, *Helicobacter pylori* infection (which reduces ascorbic acid and raises intragastric pH), and proton-pump inhibitor (PPI) use all impair dietary iron absorption. Bariatric surgery — particularly Roux-en-Y gastric bypass, which bypasses the primary iron absorptive segment (duodenum and proximal jejunum) — produces iron deficiency in a substantial fraction of patients unless actively supplemented.

- **Increased demand or physiological loss.** Pregnancy, infancy, and rapid growth phases impose iron requirements that outpace intake. **Endurance athletes** are disproportionately affected via a convergence of mechanisms: exercise-induced hepcidin surges (driven by interleukin-6 release, peaking 3–6 hours post-exercise) transiently block dietary iron absorption; foot-strike hemolysis destroys red cells mechanically; GI blood loss is amplified during prolonged running; and sweat losses add to the total deficit [30, mechanism_review]. Iron deficiency — including non-anemic iron deficiency that impairs aerobic performance — is common among female endurance athletes, affecting a substantial fraction of this population.

### Elevated Ferritin: The Central Interpretive Challenge

A high ferritin is not iron overload until proven otherwise. Ferritin is an acute-phase protein: inflammatory cytokines — principally IL-6 and TNF-α — directly upregulate hepatic ferritin synthesis regardless of body iron content [17, mechanism_review]. In most clinical settings, the most common explanation for an elevated ferritin is inflammation, liver disease, alcohol, or metabolic dysfunction — not iron excess. Failing to recognize this leads to missed diagnoses (iron deficiency masked by co-existing inflammation) and false diagnoses (unnecessary workup for hemochromatosis in patients with metabolic syndrome and mild hyperferritinemia).

**The differential is organized by ferritin magnitude and clinical context:**

#### Inflammation and Acute-Phase Response (Most Common Cause of Elevated Ferritin)

Any systemic inflammatory state — bacterial or viral infection, autoimmune/rheumatic disease, malignancy, major surgery, or tissue injury — can drive ferritin into the hundreds of ng/mL through cytokine-mediated upregulation. This is the most common reason a ferritin comes back elevated in routine practice. In this setting, the ferritin reflects the inflammatory load, not iron stores; iron stores may simultaneously be low, normal, or high. CRP is essential context: a markedly elevated ferritin alongside a high CRP argues strongly for an inflammatory etiology before any iron overload diagnosis is entertained [17, mechanism_review].

#### Liver Disease and Alcohol

Hepatocellular injury releases stored ferritin directly into the circulation. Hepatitis (viral, autoimmune, or toxic), cirrhosis, and acute liver failure all cause ferritin elevation proportionate to parenchymal damage. Alcohol independently elevates ferritin through both hepatic injury and direct stimulation of ferritin synthesis, making it a common cause of mild-to-moderate hyperferritinemia in clinical practice.

#### Metabolic Hyperferritinemia (Dysmetabolic Iron Overload Syndrome / MASLD)

A very common and under-recognized pattern: mildly-to-moderately elevated ferritin (typically 300–1,000 ng/mL) with a normal or only mildly elevated transferrin saturation (TSAT), in the setting of insulin resistance, obesity, type 2 diabetes, dyslipidemia, or metabolic dysfunction-associated steatotic liver disease (MASLD). A 2023 Nature Reviews Endocrinology consensus statement formalized "metabolic hyperferritinaemia" as a distinct entity driven by altered iron-regulatory gene expression in the setting of metabolic dysfunction [31, mechanism_review]. A multicenter cohort of 7,333 MASLD patients found elevated ferritin in 20% and, in multivariate analysis, ferritinemia was independently associated with all-cause mortality (HR 1.68) and liver-related events (HR 1.92) — driven by fibrosis progression rather than iron toxicity per se, and associated with PNPLA3 and TM6SF2 variant carriage but not with HFE mutations [32, cohort]. In this pattern, ferritin elevation reflects a combination of insulin-mediated transcriptional upregulation, hepatic steatoinflammation, and modest true iron deposition — but iron overload in the hemochromatosis sense is absent or mild.

#### Malignancy

Hematologic malignancies (lymphoma, leukemia, multiple myeloma) and solid tumors — especially hepatocellular carcinoma — can produce marked hyperferritinemia through tumor-derived ferritin, hepatic involvement, and systemic inflammation.

#### True Iron Overload: Hereditary Hemochromatosis and Transfusional Overload

**This is the diagnosis that requires proof, not assumption.** Hereditary hemochromatosis type 1 (HFE, C282Y homozygosity) is the most prevalent genetic disorder of iron overload in northern European populations. The Melbourne Collaborative Cohort Study (n = 31,192), which followed 203 C282Y homozygotes for 12 years, found that iron-overload-related disease developed in 28.4% of men and only 1.2% of women — demonstrating that C282Y homozygosity has markedly variable penetrance and that ferritin elevation alone is insufficient to establish clinically significant overload [33, cohort]. The diagnostic algorithm for true overload requires **transferrin saturation > 45%** (the earliest and most sensitive marker of iron excess) confirmed on a fasting sample, followed by HFE genotyping; ferritin serves as a disease-severity marker, not a primary diagnostic test. Transfusional iron overload is confirmed by transfusion history and MRI of liver/heart.

#### Extreme Hyperferritinemia (> 1,000–10,000+ ng/mL): A Red Flag for Life-Threatening States

Ferritin above 1,000–2,000 ng/mL — especially rising to the tens of thousands — triggers a specific differential: **hemophagocytic lymphohistiocytosis (HLH) / macrophage activation syndrome (MAS) / adult-onset Still's disease (AOSD)**. Hyperferritinemia in these syndromes reflects pathological macrophage activation and is both a diagnostic marker and a disease-monitoring tool. The revised 2024 HLH diagnostic guidelines (Blood) retain ferritin ≥ 500 µg/L as one criterion within a multivariable diagnostic framework; in a case-control analysis the overall 17-variable model achieved 97.1% sensitivity and 99.5% specificity — figures that describe the model's performance, not the ferritin threshold in isolation [34, regulatory]. The HScore — a validated nine-variable diagnostic score incorporating ferritin level, temperature, organomegaly, cytopenias, triglycerides, fibrinogen, and AST — achieves **93% sensitivity / 86% specificity** at a cutoff of 169 (multicenter validation cohort, n = 312) [35, cohort]. In these conditions, extreme hyperferritinemia is not explained by iron stores and is not an indication for phlebotomy; it is a marker of immune emergency requiring urgent diagnosis and treatment.

### Functional Iron Deficiency: High Ferritin, Iron-Starved Marrow

**Functional iron deficiency** describes a state in which total body iron stores are normal or elevated, but iron is sequestered by hepcidin and unavailable for erythropoiesis — producing the erythroid signature of iron deficiency (hypochromic, microcytic red cells; reduced reticulocyte hemoglobin content) despite a normal or elevated ferritin [17, mechanism_review]. This is the dominant iron-deficiency pattern in:

- **Chronic kidney disease (CKD):** Inflammatory cytokines drive hepcidin elevation, reducing ferroportin-mediated iron export from hepatocytes and macrophages. KDIGO-aligned thresholds define functional iron deficiency in CKD as TSAT < 20% with ferritin that may exceed 100–200 ng/mL on dialysis; functional deficiency affects an estimated 12–43% of CKD patients depending on dialysis status.
- **Chronic heart failure (CHF):** Systemic inflammation and elevated hepcidin cause iron sequestration; roughly 50% of CHF patients have iron deficiency by TSAT-based criteria even with non-low ferritin.
- **Active inflammatory states / IBD:** The same hepcidin-mediated mechanism applies; standard ferritin-only thresholds (< 30 ng/mL) are insensitive and must be replaced by TSAT-based criteria (TSAT < 20% when ferritin is 100–300 ng/mL, or either criterion when ferritin is < 100 ng/mL) [17, mechanism_review].

The critical practical implication: **a "normal" or even elevated ferritin does not exclude iron deficiency when CRP is elevated or chronic disease is present.**

### Prognostic Associations

Ferritin correlates with inflammation severity across a range of acute illnesses (sepsis, COVID-19, pancreatitis), where very high ferritin tracks with disease severity as an acute-phase signal — though it does not independently add diagnostic precision beyond direct markers of organ dysfunction in these settings. Epidemiological associations between elevated ferritin and incident type 2 diabetes, cardiovascular events, and all-cause mortality in metabolic populations are well-documented but heavily confounded by co-existing insulin resistance, liver disease, and inflammation; these associations should not be interpreted causally without adjustment for inflammatory state.

### Interpretive Limitations (Load-Bearing)

1. **The acute-phase confound is the dominant pitfall.** A ferritin within or above the reference range does NOT exclude iron deficiency when inflammation, infection, or chronic disease is present. In these contexts, ferritin must be interpreted alongside **CRP** (to quantify the inflammatory contribution), **TSAT** (to assess iron availability for erythropoiesis), and — when available — **soluble transferrin receptor (sTfR)**, which rises with iron-deficient erythropoiesis and is not an acute-phase reactant, making it the most reliable single marker in inflammatory states [28, mechanism_review].
2. **Low specificity upward.** A high ferritin is almost never the end-point of a diagnostic workup — it is the beginning of one. The differential spans inflammation, liver disease, alcohol, metabolic syndrome, malignancy, extreme macrophage-activation states, and iron overload; true overload is the least common cause in unselected patients.
3. **Hook effect at extreme concentrations.** At very high ferritin concentrations (> 10,000 ng/mL), immunoassay hook effects can cause falsely low readings; serial dilution may be required to obtain an accurate result [24, cohort; 25, cohort].
4. **Assay non-standardization.** Ferritin immunoassays differ between manufacturers; reference intervals are not interchangeable, and the historical origin of many laboratory lower-limit normals lacks scientific validation [29, meta_analysis].

**The interpretive rule:** read ferritin with iron studies (TSAT, serum iron, TIBC), CRP, and the clinical picture. Treat an isolated elevated ferritin as a hypothesis-generating finding, not a conclusion.

---

## Bibliography

[1]. Wang J, Pantopoulos K. Regulation of cellular iron metabolism. *Biochem J*. 2011;434(3):365–381. PMID: 21348856 — tag: mechanism_review — tier: 1

[2]. Knovich MA, Storey JA, Coffman LG, Torti SV, Torti FM. Ferritin for the clinician. *Blood Rev*. 2009;23(3):95–104. PMID: 18835072 — tag: mechanism_review — tier: 1

[3]. Moreira AC, Mesquita G, Gomes MS. Ferritin: An inflammatory player keeping iron at the core of pathogen-host interactions. *Microorganisms*. 2020;8(4):589. PMID: 32325688 — tag: mechanism_review — tier: 2

[4]. Macone A, Cappelletti C, Incocciati A, Piacentini R, Botta S, Boffi A, Bonamore A. Challenges in exploiting human H ferritin nanoparticles for drug delivery: navigating physiological constraints. *WIREs Nanomed Nanobiotechnol*. 2024;16(6):e2016. PMID: 39541599 — tag: mechanism_review — tier: 2

[5]. Sandnes M, Ulvik RJ, Vorland M, Reikvam H. Hyperferritinemia — a clinical overview. *J Clin Med*. 2021;10(9):2008. PMID: 34067164 — tag: mechanism_review — tier: 2

[6]. Camaschella C, Nai A, Silvestri L. Iron metabolism and iron disorders revisited in the hepcidin era. *Haematologica*. 2020;105(2):260–272. PMID: 31949017 — tag: mechanism_review — tier: 1

[7]. Torti FM, Torti SV. Regulation of ferritin genes and protein. *Blood*. 2002;99(10):3505–3516. PMID: 11986201 — tag: mechanism_review — tier: 1

[8]. Truman-Rosentsvit M, Berenbaum D, Spektor L, Cohen LA, Belizowsky-Moshe S, Lifshitz L, Ma J, Li W, Kesselman E, Abutbul-Ionita I, Danino D, Gutierrez L, Li H, Li K, Lou H, Regoni M, Poli M, Glaser F, Rouault TA, Meyron-Holtz EG. Ferritin is secreted via 2 distinct nonclassical vesicular pathways. *Blood*. 2018;131(3):342–352. PMID: 29074498 — tag: mechanism_review — tier: 1

[9]. Cancado RD, Leite LAC, Muñoz M. Defining global thresholds for serum ferritin: a challenging mission in establishing the iron deficiency diagnosis in this era of striving for health equity. *Diagnostics (Basel)*. 2025;15(3):289. PMID: 39941219 — tag: mechanism_review — tier: 2

[10]. Rishi G, Wallace DF, Subramaniam VN. Hepcidin: regulation of the master iron regulator. *Biosci Rep*. 2015;35(3):e00192. PMID: 26182354 — tag: mechanism_review — tier: 2

[11]. DePalma RG, Hayes VW, O'Leary TJ. Optimal serum ferritin level range: iron status measure and inflammatory biomarker. *Metallomics*. 2021;13(6):mfab030. doi: 10.1093/mtomcs/mfab030 — tag: mechanism_review — tier: 2

[12]. Garcia-Casal MN, Pasricha SR, Martinez RX, Lopez-Perez L, Peña-Rosas JP. Serum or plasma ferritin concentration as an index of iron deficiency and overload. *Cochrane Database Syst Rev*. 2021;5(5):CD011817. PMID: 34028001 — tag: meta_analysis — tier: 1

[13]. Peyrin-Biroulet L, Williet N, Cacoub P. Guidelines on the diagnosis and treatment of iron deficiency across indications: a systematic review. *Am J Clin Nutr*. 2015;102(6):1585–94. PMID: 26561626 — tag: meta_analysis — tier: 2

[14]. Guyatt GH, Oxman AD, Ali M, Willan A, McIlroy W, Patterson C. Laboratory diagnosis of iron-deficiency anemia: an overview. *J Gen Intern Med*. 1992;7(2):145–53. PMID: 1487761 — tag: meta_analysis — tier: 1

[15]. Snook J, Bhala N, Beales ILP, et al. British Society of Gastroenterology guidelines for the management of iron deficiency anaemia in adults. *Gut*. 2021;70(11):2030–51. PMID: 34497146 — tag: regulatory — tier: 1

[16]. World Health Organization. *WHO Guideline on Using Ferritin Concentrations to Assess Iron Status in Individuals and Populations*. Geneva: WHO; 2020. — tag: regulatory — tier: 1

[17]. Ueda N, Takasawa K. Impact of Inflammation on Ferritin, Hepcidin and the Management of Iron Deficiency Anemia in Chronic Kidney Disease. *Nutrients*. 2018;10(9):1173. PMID: 30150549 — tag: mechanism_review — tier: 2

[18]. McDonagh TA, Metra M, Adamo M, et al. 2021 ESC Guidelines for the diagnosis and treatment of acute and chronic heart failure. *Eur Heart J*. 2021;42(36):3599–3726. PMID: 34447992. doi: 10.1093/eurheartj/ehab368 — tag: regulatory — tier: 1

[19]. Dahman LS, Sumaily KM, Sabi EM, Hassan MA, Bin Thalab AM, Sayad AS, Bin Kolaib SM, Alhadhrmi FM. A comparative study for measuring serum ferritin levels with three different laboratory methods: enzyme-linked immunosorbent assay versus Cobas e411 and Cobas Integra 400 methods. *Diagnostics (Basel)*. 2022;12(2):320. PMID: 35204412. PMC8870818. doi: 10.3390/diagnostics12020320 — tag: cohort — tier: 2

[20]. Fox AL, Fairweather-Tait SJ, Dainty JR, et al. Comparison of four immunoassays to measure serum ferritin concentrations and iron deficiency prevalence among non-pregnant Cambodian women and Congolese children. *Clin Chem Lab Med*. 2017;55(1):65–71. doi: 10.1515/cclm-2016-0015 — tag: cohort — tier: 1

[21]. Leimberg MJ, Prus E, Konijn AM, Fibach E. Macrophages function as a ferritin iron source for cultured human erythroid precursors. *Blood*. 2010;116(9):1574–1576. doi: 10.1182/blood-2009-08-239459 — tag: mechanism_review — tier: 1

[22]. Braga F, Pasqualetti S, Frusciante E, Borrillo F, Chibireva M, Panteghini M. Harmonization status of serum ferritin measurements and implications for use as marker of iron-related disorders. *Clin Chem*. 2022;68(9):1202–1210. doi: 10.1093/clinchem/hvac099 — tag: mechanism_review — tier: 1

[23]. Fox B, Roberts G, Atkinson E, Rigsby P, Ball C. International collaborative study to evaluate and calibrate two recombinant L chain ferritin preparations for use as a WHO International Standard. *Clin Chem Lab Med*. 2022;60(3):359–368. PMID: 34939377. doi: 10.1515/cclm-2021-1139 — tag: mechanism_review — tier: 2

[24]. Harb R, Xu J, Cendales M, et al. Diagnostic pitfalls in assessment of ferritin following CAR-T cell therapy: understanding the hook effect. *Pediatr Blood Cancer*. 2024;e31171. doi: 10.1002/pbc.31171 — tag: cohort — tier: 1

[25]. Wu SJ, Hayden JA. Upfront dilution of ferritin samples to reduce hook effect, improve turnaround time and reduce costs. *Biochemia Medica*. 2018;28(1):010903. doi: 10.11613/BM.2018.010903 — tag: cohort — tier: 1

[26]. Blanco M, Varela C. Interference from heterophilic antibodies in the Olympus ferritin method. *Clin Chem*. 2006;52(8):1623–1624. doi: 10.1373/clinchem.2006.068486 — tag: cohort — tier: 1

[27]. Sacri AS, Ferreira D, Khoshnood B, Gouya L, Barros H, Chalumeau M. Stability of serum ferritin measured by immunoturbidimetric assay after storage at −80°C for several years. *PLoS ONE*. 2017;12(12):e0188332. PMID: 29228047. PMC5724861. doi: 10.1371/journal.pone.0188332 — tag: cohort — tier: 2

[28]. Oustamanolakis P, Koutroubakis IE. Soluble transferrin receptor-ferritin index is the most efficient marker for the diagnosis of iron deficiency anemia in patients with IBD. *Inflamm Bowel Dis*. 2011;17(12):E158–E159. doi: 10.1002/ibd.21881 — tag: mechanism_review — tier: 1

[29]. Truong J, Naveed K, Beriault D, Lightfoot D, Fralick M, Sholzberg M. The origin of ferritin reference intervals: a systematic review. *Lancet Haematol*. 2024;11(10):e721–e530. doi: 10.1016/s2352-3026(24)00103-0 — tag: meta_analysis — tier: 1

[30]. Damian MT, Vulturar R, Login CC, Damian L, Chis A, Bojan A. Anemia in sports: a narrative review. *Life (Basel)*. 2021;11(9):987. PMID: 34575136 — tag: mechanism_review — tier: 2

[31]. Valenti L, Corradini E, Adams L, et al. Consensus statement on the definition and classification of metabolic hyperferritinaemia. *Nat Rev Endocrinol*. 2023;19(5):299–310. doi: 10.1038/s41574-023-00807-6 — tag: mechanism_review — tier: 1

[32]. Suresh D, Li A, Miller MJ, Wijarnpreecha K, Chen VL. Associations between metabolic hyperferritinemia, fibrosis-promoting alleles, and clinical outcomes in steatotic liver disease. *Liver Int*. 2023 Nov 16. PMID: 37971775 — tag: cohort — tier: 1

[33]. Allen KJ, Gurrin LC, Constantine CC, Osborne NJ, Delatycki MB, Nicoll AJ, McLaren CE, Bahlo M, Nisselle AE, Vulpe CD, Anderson GJ, Southey MC, Giles GG, English DR, Hopper JL, Olynyk JK, Powell LW, Gertig DM. Iron-overload-related disease in HFE hereditary hemochromatosis. *N Engl J Med*. 2008;358(3):221–30. PMID: 18199861. doi: 10.1056/NEJMoa073286 — tag: cohort — tier: 1

[34]. Henter JI, Sieni E, Eriksson J, Bergsten E, Hed Myrberg I, Canna SW, Coniglio ML, Cron RQ, Kernan KF, Kumar AR, Lehmberg K, Minoia F, Naqvi A, Ravelli A, Tang YM, Bottai M, Bryceson YT, Horne A, Jordan MB. Diagnostic guidelines for familial hemophagocytic lymphohistiocytosis revisited. *Blood*. 2024;144(22):2308–2318. PMID: 39046779. doi: 10.1182/blood.2024025077 — tag: regulatory — tier: 1

[35]. Fardet L, Galicier L, Lambotte O, Marzac C, Aumont C, Chahwan D, Coppo P, Hejblum G. Development and validation of the HScore, a score for the diagnosis of reactive hemophagocytic syndrome. *Arthritis Rheumatol*. 2014;66(9):2613–20. PMID: 24782338. doi: 10.1002/art.38690 — tag: cohort — tier: 1
