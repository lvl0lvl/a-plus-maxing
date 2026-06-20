# Section A: Physiology & What AST Measures

## What AST Is

Aspartate aminotransferase (AST; EC 2.6.1.1) — historically designated SGOT (serum glutamic-oxaloacetic transaminase) or GOT — is a **pyridoxal-5'-phosphate (PLP, the active form of vitamin B6)-dependent enzyme** that catalyzes the reversible transamination reaction:

> **L-aspartate + α-ketoglutarate ⇌ oxaloacetate + L-glutamate**

This reaction sits at the intersection of amino acid catabolism and energy metabolism [1, mechanism_review]. It is the same reaction run in both directions depending on cellular energy state: in the cytosol, GOT1 (cytosolic AST, cAST) converts aspartate to oxaloacetate for gluconeogenesis; in the mitochondrial matrix, GOT2 (mitochondrial AST, mAST) catalyzes the reverse direction to regenerate aspartate for export [1, mechanism_review; 2, mechanism_review].

PLP is not merely a cofactor here in the generic sense — it is covalently bound at the active site via a Schiff base with a lysine residue, and serves as the direct carrier of the amino group during transamination [1, mechanism_review]. This PLP-dependence has a key clinical implication: vitamin B6 depletion (common in heavy alcohol use) reduces aminotransferase activity differentially, suppressing ALT activity more than AST activity, which shifts the observed AST/ALT ratio upward [6, cohort].

## Two Isoenzymes from Separate Genes

AST exists as **two genetically and immunologically distinct isoenzymes**, encoded by separate nuclear genes:

| Isoenzyme | Gene | Chromosomal location | Subcellular compartment |
|-----------|------|---------------------|------------------------|
| Cytosolic AST (cAST) | *GOT1* | Chromosome 10q24.2 | Cytoplasm |
| Mitochondrial AST (mAST) | *GOT2* | Chromosome 16q21 | Mitochondrial matrix |

Both are homodimeric class-I PLP-dependent aminotransferases [1, mechanism_review; 2, mechanism_review]. The cytosolic isoform (GOT1) is the dominant form measured in routine serum assays under most circumstances; the mitochondrial isoform (GOT2) is released in appreciable quantities into the circulation only when hepatocyte necrosis is severe enough to disrupt mitochondrial membranes [2, mechanism_review].

## Role in the Malate-Aspartate Shuttle

Beyond amino acid metabolism, the AST reaction is a **core component of the malate-aspartate shuttle (MAS)** — the primary mechanism by which cytosolic NADH reducing equivalents generated during glycolysis cross the inner mitochondrial membrane (which is impermeable to NADH itself) [3, mechanism_review].

The shuttle cycle proceeds as follows:

1. **Cytosol (MDH1):** Oxaloacetate + NADH → malate + NAD+ (recovers cytosolic NAD+ from glycolysis)
2. Malate enters the mitochondrion via the malate-α-ketoglutarate carrier; mitochondrial MDH2 converts it back to oxaloacetate, reducing mitochondrial NAD+ → NADH for the respiratory chain
3. **Mitochondrial matrix (GOT2):** Oxaloacetate + glutamate → aspartate + α-ketoglutarate
4. Aspartate exits via the aspartate-glutamate carrier (AGC, electrogenic — driven by the mitochondrial proton gradient)
5. **Cytosol (GOT1):** Aspartate + α-ketoglutarate → oxaloacetate + glutamate, regenerating oxaloacetate for step 1

GOT2 loss-of-function mutations in humans produce a severe neonatal encephalopathy with epilepsy, progressive microcephaly, hyperlactatemia, and elevated citrulline — a direct demonstration that GOT2 activity is non-redundant and indispensable for maintaining cytoplasmic redox homeostasis and mitochondrial aspartate supply [1, mechanism_review; 2, mechanism_review]. GOT1 deficiency produces a distinct, milder phenotype (familial macro-AST with persistent serum elevation but no organ pathology), reflecting the different metabolic roles of the cytosolic compartment.

## Tissue Distribution: Why AST Is Less Liver-Specific Than ALT

The central interpretive challenge with serum AST is its **broad multi-organ expression**. High AST catalytic activity is present in:

- Hepatocytes (liver)
- Cardiac myocytes
- Skeletal muscle
- Red blood cells (erythrocytes)
- Kidney tubular epithelium
- Brain neurons
- Pancreas

In quantitative terms, AST activity in myocardial and skeletal muscle tissue is comparable to — or exceeds — hepatic concentrations, meaning that injury to any of these tissues, not only the liver, will elevate serum AST (in U/L) [4, cohort; 5, cohort]. In a large multi-center study of COVID-19, AST elevations could be fully explained by the summed contributions of hepatocellular injury (~67%) and skeletal/cardiac muscle damage (~43%), with neither source dominant — a direct empirical illustration of multi-tissue origin [5, cohort].

By contrast, **ALT** (alanine aminotransferase) is expressed at roughly 3,000-fold higher activity in hepatocyte cytosol than in any other tissue. Non-hepatic ALT concentrations are low enough that ALT elevation in the absence of muscle markers almost always reflects hepatocellular injury. This difference in tissue specificity is the biochemical foundation for the clinical dictum: **ALT is the more liver-specific enzyme; AST is the more sensitive but less specific marker of cellular injury across multiple organs** [4, cohort; 5, cohort].

## Plasma Half-Life: The Kinetic Basis of AST/ALT Patterns

The two enzymes are also cleared from plasma at different rates. Using first-order kinetic modeling applied to 6.5 million transaminase measurements in over 91,000 patients, Sherman and Goessling (2024) derived:

- **AST plasma half-life: ~15.8 hours** (clearance rate 1.13 day⁻¹)
- **ALT plasma half-life: ~34.6 hours** (clearance rate 0.47 day⁻¹)

AST is thus cleared from blood at more than twice the rate of ALT [7, cohort]. The practical implication: following an acute hepatocellular injury, both enzymes rise rapidly, but as injury resolves, **AST falls faster than ALT**. Conversely, in any setting where AST remains elevated relative to ALT — or where AST/ALT > 2 — it implies either (a) ongoing or severe injury that continues to release AST faster than it clears, (b) a non-hepatic source of AST (cardiac or skeletal muscle), or (c) disproportionate mAST release from mitochondrial disruption, as in alcoholic liver disease.

The mitochondrial isoform (mAST/GOT2) has a substantially longer serum retention time than cytosolic AST, because it is released only with necrotic injury and is subsequently complexed with other cellular proteins that slow clearance.

## The AST/ALT (De Ritis) Ratio

Introduced by Fernando De Ritis in 1957, the **AST/ALT ratio** (De Ritis ratio) integrates both the tissue-distribution and kinetic differences between the enzymes into a single clinically actionable number. Several patterns are diagnostically useful:

**AST/ALT > 2 in alcoholic liver disease.** The mechanism is dual: (1) Ethanol metabolism and its aldehyde intermediates accelerate the catabolism of PLP, the vitamin B6 cofactor shared by both enzymes. Because hepatic ALT is more acutely sensitive to PLP depletion than AST, ALT activity is preferentially suppressed, raising the ratio. (2) Alcohol-induced mitochondrial membrane injury causes disproportionate release of the mitochondrial isoform (mAST/GOT2), which does not occur in non-alcoholic hepatitis. Together these mechanisms generate an AST:ALT ratio > 2 in approximately 70% of patients with alcoholic liver disease, compared to < 1 in most patients with viral or non-alcoholic steatohepatitis [6, cohort].

Diehl et al. (1984) provided the founding clinical evidence: in 12 patients with biopsy-confirmed alcoholic hepatitis, in vitro addition of PLP to liver homogenates rescued ALT activity but not AST activity; after one month of abstinence and B6 repletion, serum ALT rose and serum AST fell, significantly normalizing the ratio [6, cohort].

**AST > ALT with AST > 500 U/L.** Markedly elevated AST out of proportion to ALT and in isolation from ALT suggests a non-hepatic source — particularly rhabdomyolysis (skeletal muscle necrosis), hemolysis, or myocardial infarction. In these settings, creatine kinase (CK) and lactate dehydrogenase (LDH) isoforms help resolve the source.

**AST/ALT < 1 in non-alcoholic fatty liver disease (NAFLD).** Here ALT tends to predominate because the hepatocellular injury is predominantly cytosolic (steatosis and mild inflammation) without significant mitochondrial disruption or PLP depletion, and ALT's longer half-life keeps it numerically higher.

## Summary

AST is a PLP-dependent transaminase that catalyzes the reversible interconversion of aspartate and oxaloacetate, and serves as an integral enzyme of both amino acid metabolism and the malate-aspartate shuttle. Its two isoforms — cytosolic GOT1 and mitochondrial GOT2 — are encoded by separate genes on chromosomes 10 and 16, respectively. Because AST is expressed at high catalytic activity in liver, heart, skeletal muscle, erythrocytes, kidney, brain, and pancreas, serum AST elevation is inherently non-specific. Its shorter plasma half-life (~16 hours vs. ~35 hours for ALT) means it clears faster after injury, making the AST/ALT ratio a useful dynamic signal: in alcoholic liver disease, both PLP depletion (suppressing ALT preferentially) and alcohol-driven mitochondrial injury (releasing mAST) combine to produce the characteristic AST/ALT > 2 pattern. AST is best interpreted alongside ALT, creatine kinase, and clinical context rather than in isolation.

---

## Bibliography

[1]. van Karnebeek CDM, Ramos RJ, Wen X-Y, Tarailo-Graovac M, Gleeson JG, Skrypnyk C, Brand-Arzamendi K, Karbassi F, Issa MY, van der Lee R, Drögemöller BI, Koster J, Rousseau J, Campeau PM, Wang Y, Cao F, Li M, Ruiter J, Ciapaite J, Kluijtmans LAJ, Willemsen MAAP, Jans JJ, Ross CJ, Wintjes LT, Rodenburg RJ, Huigen MCDG, Jia Z, Waterham HR, Wasserman WW, Wanders RJA, Verhoeven-Duif NM, Zaki MS, Wevers RA. Bi-allelic GOT2 Mutations Cause a Treatable Malate-Aspartate Shuttle-Related Encephalopathy. *Am J Hum Genet*. 2019;105(3):534–548. PMID: 31422819. DOI: 10.1016/j.ajhg.2019.07.015. — tag: mechanism_review — tier: 1

[2]. Broeks MH, van Karnebeek CDM, Wanders RJA, Jans JJM, Verhoeven-Duif NM. Inborn disorders of the malate aspartate shuttle. *J Inherit Metab Dis*. 2021;44(4):792–808. PMID: 33990986. DOI: 10.1002/jimd.12402. — tag: mechanism_review — tier: 1

[3]. Borst P. The malate–aspartate shuttle (Borst cycle): How it started and developed into a major metabolic pathway. *IUBMB Life*. 2020;72(11):2241–2259. PMID: 32916028. DOI: 10.1002/iub.2367. — tag: mechanism_review — tier: 1

[4]. Aloisio E, Colombo G, Arrigo C, Dolci A, Panteghini M. Sources and clinical significance of aspartate aminotransferase increases in COVID-19. *Clin Chim Acta*. 2021;522:88–95. PMID: 34411557. DOI: 10.1016/j.cca.2021.08.012. — tag: cohort — tier: 1

[5]. Aloisio E, Panteghini M. Aspartate aminotransferase in COVID-19: A probably overrated marker. *Liver Int*. 2021;41(11):2809–2810. PMID: 34609789. DOI: 10.1111/liv.15068. — tag: cohort — tier: 1

[6]. Diehl AM, Potter J, Boitnott J, Van Duyn MA, Herlong HF, Mezey E. Relationship between pyridoxal 5'-phosphate deficiency and aminotransferase levels in alcoholic hepatitis. *Gastroenterology*. 1984;86(4):632–636. PMID: 6698365. — tag: cohort — tier: 1

[7]. Sherman MS, Goessling W. Discovery of biophysical rate laws from the electronic health record enables real-time liver injury estimation from transaminase dynamics. *Cell Rep Med*. 2024;5(11):101828. PMID: 39536750. DOI: 10.1016/j.xcrm.2024.101828. — tag: cohort — tier: 1
