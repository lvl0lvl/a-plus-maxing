# Section C: Measurement & Standardization

## Assay Platforms and Mechanism

Serum ferritin is measured almost exclusively by immunoassay. Three principal platform families are in routine clinical use:

**Immunoturbidimetric and latex-enhanced nephelometric assays** mix patient serum with latex particles coated with anti-ferritin antibodies. Ferritin in the sample crosslinks the particles, increasing the turbidity of the solution; the change in absorbance (turbidimetry) or in light-scatter at a defined angle (nephelometry) is proportional to ferritin concentration. These methods are rapid and easily automated on general chemistry analyzers. Their linear range is narrower than dedicated immunometric platforms, and they can read falsely high at antigen excess — a point returned to below.

**Chemiluminescent immunoassays (CLIA) and electrochemiluminescent assays (ECLIA)** use a two-antibody sandwich architecture: a capture antibody immobilizes ferritin, a second labeled antibody generates a light signal proportional to bound antigen. This format is the workhorse of dedicated immunoanalyzers (e.g., Roche Cobas e series, Abbott Alinity i, Siemens Centaur) and delivers the high throughput and broad dynamic range needed for clinical throughput.

**ELISA (enzyme-linked immunosorbent assay)** is the classic manual-to-semi-automated sandwich format: capture → wash → enzyme-conjugated detection antibody → wash → substrate → colorimetric or fluorometric readout. ELISA is widely used in research, nutrition surveys, and lower-resource settings. Comparative data show close agreement between ELISA and ECLIA but divergence versus immunoturbidimetric platforms, particularly at mid-range concentrations [1, cohort; 2, cohort].

Crucially, these assays do not measure iron content directly. They detect ferritin protein by binding to epitopes on the shell — predominantly on the L (light) subunit, which predominates in secreted serum ferritin. Because serum ferritin is the glycosylated, largely iron-poor form secreted primarily by macrophages and hepatocytes rather than the iron-laden intracellular storage form, the immunoassay signal correlates with iron stores only indirectly and breaks down when inflammation, tissue injury, or disease upregulates ferritin synthesis independent of body iron [3, mechanism_review].

---

## Standardization: A Historically Poor Track Record

Despite decades of clinical use, ferritin remains one of the least harmonized analytes in routine laboratory medicine. Studies directly comparing commercial platforms on the same patient specimens consistently find inter-assay coefficients of variation exceeding 15–23% — well above the desirable analytical performance specifications for clinical use [4, mechanism_review]. The direct implication: a result of 28 ng/mL on one platform is not the same measurement as 28 ng/mL on another, and applying a fixed threshold across platforms introduces systematic misclassification.

The root cause is calibration fragmentation. Ferritin immunoassays across different manufacturers have been traceable to different primary reference materials at different points in time — and some continue to be, even now.

**The WHO International Standard** for serum ferritin has gone through four generations:
- **IS 80/602** (spleen-derived human ferritin, 1985) and **IS 80/578** (also spleen-derived, 1985) — the original primary standards, now depleted.
- **IS 94/572** (3rd International Standard, 1997) — a recombinant L-chain ferritin preparation, this became the dominant calibrant for most platforms.
- **IS 19/118** (4th International Standard, 2022) — the current WHO IS, also recombinant human L-chain ferritin, prepared by NIBSC. IS 19/118 has an assigned potency of 10.5 µg/ampoule and was established in an international collaborative study across 12 laboratories in 9 countries; it supersedes 94/572 [5, mechanism_review].

The harmonization problem is not resolved by the existence of this standard, because adoption is uneven. Braga et al. (2022), in a rigorous four-platform study published in *Clinical Chemistry*, found that two of them — the Abbott Alinity and Roche Cobas — remained traceable to the long-depleted IS 80/602 rather than to IS 94/572, creating independent calibration hierarchies in simultaneous clinical use (the study also assessed the Beckman Coulter Access Dxl and Siemens Advia Centaur CP). The study reported highly significant between-platform differences (P < 0.00001) with a median inter-assay CV of 22.9% [4, mechanism_review]. This is the direct parallel to the well-known 25-hydroxyvitamin D harmonization problem: the same specimen, the same population, different analyzers — meaningfully different numbers.

The practical implication for threshold-based clinical decisions (e.g., ferritin < 30 ng/mL for iron deficiency) is that no single cutoff is fully platform-agnostic. Published reference ranges and diagnostic thresholds were derived on specific assay generations; applying them to a different platform without commutability verification can silently shift the classification. Laboratories implementing new analyzers should perform method-comparison studies bridging to the previous platform before applying the same decision thresholds.

---

## The Hook Effect: A Clinically Dangerous Pitfall

In one-step sandwich immunoassays, patient serum, capture antibody (bound to solid phase), and signal antibody (enzyme- or luminescent-labeled) are all combined simultaneously. At physiologically normal ferritin concentrations, each ferritin molecule binds one capture antibody and one signal antibody, forming a stable sandwich that generates a signal proportional to analyte concentration. At very high ferritin concentrations (antigen excess), free antigen molecules compete with sandwiched complexes for both antibody partners: capture sites become saturated with single antibodies bound to one ferritin, and excess free antigen competes with already-bound complexes for signal antibody, leaving fewer complete sandwiches. The result is paradoxically **reduced signal at extremely elevated concentration** — the instrument reports a falsely low (or even near-normal) ferritin value [6, mechanism_review; 7, cohort].

This is not a theoretical artifact. Wu and Hayden (2018) documented on the Siemens Centaur XP platform that hook effect appeared in samples with ferritin as low as 86,028 µg/L (86 µg/mL) without upfront dilution; when mandatory 5-fold pre-dilution was applied, no hook effect was observed up to 126,050 µg/L [7, cohort]. In a pediatric case series following CAR-T cell therapy, a patient's in-house ferritin measurement was more than 1,000-fold lower than the dilution-confirmed true value at a reference laboratory — a clinically critical error in a context where ferritin is the primary severity marker for immune effector cell-associated hemophagocytic lymphohistiocytosis-like syndrome [6, cohort].

**Clinical contexts where hook effect must be considered:** hemophagocytic lymphohistiocytosis (HLH), adult-onset Still's disease, macrophage activation syndrome, severe sepsis with secondary HLH features, and extreme iron overload. When the clinical picture demands a very high ferritin — markedly ill patient, cytopenias, splenomegaly, fever — and the reported value is paradoxically normal or merely modestly elevated, the laboratory should be alerted immediately to dilute and re-run the sample.

Two-step assays (which wash away unbound antigen before adding signal antibody) are substantially less susceptible to hook effect, but are not completely immune. The laboratory's declared methodology and dynamic range should always be checked when extreme hyperferritinemia is clinically suspected.

---

## Heterophile and Anti-Reagent Antibody Interference

Approximately 0.1% of patients carry circulating heterophile antibodies — broadly reactive immunoglobulins (often induced by animal exposure or subclinical infections) that can bind the animal-derived capture or detection antibodies used in ferritin assays. Depending on which antibody pair is affected, the result can be falsely elevated or falsely suppressed. Blanco and Varela (2006) documented falsely elevated ferritin (mean 244 µg/L versus 76 µg/L on an unaffected platform) in 13 of 13,143 samples on the Olympus ferritin assay; pretreatment with heterophilic blocking tubes normalized the values [8, cohort]. Discordance between platforms — particularly a markedly elevated result on one assay that does not match the clinical picture — should prompt heterophile antibody investigation.

---

## Glycosylation, Isoform Composition, and the Non-Identity of Serum and Tissue Ferritin

Intracellular ferritin (the storage form) is a 24-subunit heteropolymer of H (heavy, ferroxidase-active, ~21 kDa) and L (light, mineralization-active, ~19 kDa) chains assembled in the cytoplasm; it is not glycosylated and is iron-rich. The ferritin that circulates in serum is a distinct entity: it is predominantly L-subunit in composition, largely iron-poor (iron content 10–30% of intracellular ferritin at best), and bears N-linked glycosylation acquired during transit through secretory vesicles. Current evidence places its primary cellular source in macrophages, secreted via a nonclassical vesicular pathway rather than classical ER–Golgi exocytosis [3, mechanism_review]. Commercial immunoassays are calibrated against recombinant L-chain ferritin (WHO IS 19/118) and predominantly detect the L-rich glycosylated serum form.

The consequence: serum ferritin is not a direct measure of tissue iron content. It correlates with body iron stores across the population, but the correlation is confounded by any process that upregulates ferritin gene expression independent of iron — acute-phase response (IL-6, TNF-α, IL-1β all upregulate ferritin transcription), liver disease (leakage), malignancy, and alcohol. The assay cannot distinguish an elevated ferritin caused by iron overload from one caused by inflammation.

---

## Pre-Analytic Considerations and Companion Tests

Ferritin is pre-analytically robust: it is stable in serum or EDTA-plasma at 4°C for at least 5 days, and in samples frozen at −80°C for 3–5 years without significant degradation [9, cohort]. Both serum and EDTA-plasma are acceptable; plasma values average approximately 7% lower than serum on some platforms, a difference within most assay imprecision. Hemolysis is not a major interferent for ferritin (unlike hemoglobin-based analytes), but grossly lipemic samples may affect turbidimetric assays.

Because ferritin is an acute-phase reactant, it should not be interpreted in isolation. A full iron panel adds essential context:

- **Transferrin saturation (TSAT)** — serum iron ÷ TIBC × 100; low TSAT (< 20%) with low ferritin confirms functional iron deficiency; low TSAT with high ferritin suggests anemia of chronic disease or functional iron deficiency in inflammation.
- **Transferrin / TIBC** — inversely reflects iron stores; rises in iron deficiency.
- **Soluble transferrin receptor (sTfR)** — shed from erythroid precursor surface in proportion to erythropoietic iron demand. Crucially, sTfR is **not an acute-phase reactant** — it remains elevated in true iron deficiency even during inflammatory states where ferritin is falsely normal or elevated [10, mechanism_review]. The sTfR-to-log-ferritin index improves discrimination of iron-deficiency anemia from anemia of chronic disease.
- **Reticulocyte hemoglobin content (CHr/Ret-He)** — reflects the iron available for erythropoiesis in the most recent red cell cohort; a functional iron deficiency marker independent of iron stores.

---

## Bibliography

1. A Comparative Study for Measuring Serum Ferritin Levels with Three Different Laboratory Methods: Enzyme-Linked Immunosorbent Assay versus Cobas e411 and Cobas Integra 400 Methods. Dahman LS, Sumaily KM, Sabi EM, Hassan MA, Bin Thalab AM, Sayad AS, Bin Kolaib SM, Alhadhrmi FM. (2022). *Diagnostics* (MDPI). 12(2):320. DOI: 10.3390/diagnostics12020320. PMID: 35204412. PMC8870818. — tag: cohort — tier: 2

2. Comparison of four immunoassays to measure serum ferritin concentrations and iron deficiency prevalence among non-pregnant Cambodian women and Congolese children. Fox et al. (2017). *Clinical Chemistry and Laboratory Medicine*, 55(1):65–71. DOI: 10.1515/cclm-2016-0015. — tag: cohort — tier: 1

3. Serum ferritin is derived primarily from macrophages through a nonclassical secretory pathway. Leimberg et al. (2010). *Blood*, 116(9):1574–1576. DOI: 10.1182/blood-2009-08-239459. — tag: mechanism_review — tier: 1

4. Harmonization Status of Serum Ferritin Measurements and Implications for Use as Marker of Iron-Related Disorders. Braga F, Pasqualetti S, Frusciante E, Borrillo F, Chibireva M, Panteghini M. (2022). *Clinical Chemistry*, 68(9):1202–1210. DOI: 10.1093/clinchem/hvac099. — tag: mechanism_review — tier: 1

5. International collaborative study to evaluate and calibrate two recombinant L chain Ferritin preparations for use as a WHO International Standard. Fox B, Roberts G, Atkinson E, Rigsby P, Ball C. (2022). *Clinical Chemistry and Laboratory Medicine*, 60(3):359–368. DOI: 10.1515/cclm-2021-1139. PMID: 34939377. — tag: mechanism_review — tier: 2

6. Diagnostic pitfalls in assessment of ferritin following CAR-T cell therapy: Understanding the hook effect. Harb et al. (2024). *Pediatric Blood & Cancer*, e31171. DOI: 10.1002/pbc.31171. — tag: cohort — tier: 1

7. Upfront dilution of ferritin samples to reduce hook effect, improve turnaround time and reduce costs. Wu SJ, Hayden JA. (2018). *Biochemia Medica*, 28(1):010903. DOI: 10.11613/BM.2018.010903. — tag: cohort — tier: 1

8. Interference from Heterophilic Antibodies in the Olympus Ferritin Method. Blanco M, Varela C. (2006). *Clinical Chemistry*, 52(8):1623–1624. DOI: 10.1373/clinchem.2006.068486. — tag: cohort — tier: 1

9. Stability of serum ferritin measured by immunoturbidimetric assay after storage at −80°C for several years. Sacri AS, Ferreira D, Khoshnood B, Gouya L, Barros H, Chalumeau M. (2017). *PLoS ONE*. 12(12):e0188332. DOI: 10.1371/journal.pone.0188332. PMID: 29228047. PMC5724861. — tag: cohort — tier: 2

10. Soluble transferrin receptor-ferritin index is the most efficient marker for the diagnosis of iron deficiency anemia in patients with IBD. Oustamanolakis P, Koutroubakis IE. (2011). *Inflammatory Bowel Diseases*, 17(12):E158–E159. DOI: 10.1002/ibd.21881. — tag: mechanism_review — tier: 1
