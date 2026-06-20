## Section A — Identity, structure, mechanism

### The defining fact: two molecules, one name

The label "CJC-1295" is used in the literature and the marketplace to denote **two structurally distinct entities that are constantly conflated**, and almost every numerical claim about "CJC-1295" is meaningless until this is resolved:

- **CJC-1295 WITH DAC** ("DAC:GRF", Drug-Affinity-Complex): a tetrasubstituted hGRF(1-29) analogue carrying an added N-epsilon-3-maleimidopropionamide-lysine at the C-terminus, which **covalently binds circulating serum albumin in vivo**, conferring a half-life on the order of days (~6-8 d in humans) `[1][2]` `mechanism_review`/`rct`.
- **CJC-1295 WITHOUT DAC** = "Modified GRF 1-29" / "Mod GRF 1-29": the *same* tetrasubstituted GRF(1-29) backbone but **lacking the maleimido-Lys / DAC moiety**, so it does not conjugate albumin and has a short (~30 min order) half-life; it is the form commonly stacked with the ghrelin-receptor agonist ipamorelin `[1]` `mechanism_review`.

The pharmacokinetic data below (Teichman 2006, Ionescu 2006) are drawn from trials of the **DAC** form and must not be attributed to the no-DAC "Mod GRF 1-29." Mislabeling — including vendors selling "Mod GRF 1-29" as "CJC-1295 without DAC" while quoting the DAC half-life — is rampant; this is noted here as a structural caveat rather than cited to a primary source.

### Peptide identity and the core backbone

CJC-1295 is a synthetic analogue of **human growth-hormone-releasing factor / hormone, residues 1-29** (hGRF(1-29), equivalently GHRH(1-29) — the same biologically active 1-29 fragment that defines sermorelin) `[2]` `mechanism_review`. The native human GHRH peptide is a 44-amino-acid hypothalamic peptide; the 1-29 N-terminal fragment retains full GH-releasing activity, and it is this fragment that all GRF(1-29) analogues are built on `[3]` `mechanism_review`.

### The four substitutions (exactly four)

CJC-1295 is built on a **tetrasubstituted** hGRF(1-29) scaffold `[2]` `mechanism_review`. The canonical identification paper (Jetté et al., *Endocrinology* 2005) describes CJC-1295 as "a tetrasubstituted form of hGRF(1-29) with an added N-epsilon-3-maleimidopropionamide derivative of lysine at the C terminus" `[2]` `mechanism_review`. The four substitutions, relative to native hGRF(1-29), are:

1. **D-Ala at position 2** (Ala2 -> D-Ala) — blocks dipeptidyl-peptidase-IV (DPP-IV) cleavage at the N-terminus, the principal route of GHRH inactivation.
2. **Gln at position 8** (Asn8 -> Gln) — removes the asparagine that is prone to deamidation / rearrangement to aspartate.
3. **Ala at position 15** — improves bioactivity/stability.
4. **Leu at position 27** (Met27 -> Leu) — removes the oxidation-sensitive methionine.

That is a list of **exactly four** substitutions, matching the "tetrasubstituted" descriptor `[2]` `mechanism_review`. The mechanistic rationale (DPP-IV resistance at position 2; deamidation, bioactivity, and oxidation handling at 8/15/27) is the standard medicinal-chemistry account `[1]` `mechanism_review`. (Note: the published Jetté abstract verifies the "tetrasubstituted" status and the maleimido-Lys addition; the residue-by-residue enumeration is the widely reported set and is consistent with the DPP-IV-resistance design logic, but the individual residues are not all spelled out in the abstract text itself — flagged as a verification limit.)

### The DAC mechanism: covalent albumin bioconjugation

The "DAC" (Drug Affinity Complex) is the C-terminal **N-epsilon-3-maleimidopropionamide-lysine** group `[2]` `mechanism_review`. After subcutaneous injection, the electrophilic **maleimide reacts with the single free thiol of albumin — Cys34** — to form a stable covalent **thiosuccinimide (thioether) bond**, producing a peptide-albumin bioconjugate in vivo `[2][4]` `mechanism_review`. The chemistry is well characterised in the broader bioconjugate literature: "Maleimidopropionic acid (MPA) modification ... allows a specific and stable covalent attachment to cysteine 34 of albumin to form a thiosuccinimide bond," and "Multiple species such as rodents, dogs, rabbits, monkeys, and humans all possess a conserved cysteine residue of albumin (Cys34 in human), which is the only free thiol group in this protein" `[4]` `mechanism_review`. Because albumin itself has a very long circulating lifetime and the ~67 kDa conjugate is too large for renal filtration and is shielded from peptidases, the bioconjugate dramatically extends the analogue's half-life relative to the free peptide `[4]` `mechanism_review`. Jetté et al. confirmed the in-vivo consequence directly: CJC-1295 was "found to be present in plasma beyond 72 h" in rats `[2]` `mechanism_review`.

The contrast is the crux: the **no-DAC** Mod GRF 1-29 has the same four backbone substitutions but no maleimido-Lys, so it never forms the albumin conjugate and is cleared in roughly half an hour `[1]` `mechanism_review`. The long half-life is therefore a property of the DAC, not of the substitutions.

### Receptor and signalling mechanism (GHRH-R, not the ghrelin receptor)

CJC-1295 acts as an agonist at the **growth-hormone-releasing-hormone receptor (GHRH-R)**, a **class B (secretin-like) G-protein-coupled receptor** that is physiologically expressed mainly on the **somatotrope cells of the anterior pituitary** `[5]` `mechanism_review`. Jetté et al. demonstrated this directly: the hGRF(1-29)-albumin conjugates "were bioactive in a GH secretion assay in cultured rat anterior pituitary cells," i.e. they activate the GRF receptor on pituitary somatotrophs `[2]` `mechanism_review`.

The downstream cascade is canonical Gs signalling: GHRH-R activation couples to Gαs, stimulating **adenylyl cyclase**, raising **cAMP**, which "binds and activates the regulatory subunits of protein kinase A (PKA), which phosphorylate and activate the transcription factor CREB protein" `[5]` `mechanism_review`. This drives two outputs — acute **release** of pre-formed GH from secretory granules, and de-novo **synthesis**: CREB "may induce the synthesis of pituitary-specific transcription factor Pit-1, and an increase in Pit-1 may lead to a subsequent increase in GH gene expression, ultimately replenishing the cellular stores of GH" `[5]` `mechanism_review`. The released GH in turn "stimulates the production of insulin-like growth factor I (IGF-I) in the liver" — the hepatic IGF-1 arm `[5]` `mechanism_review`.

**Contrast with ghrelin-receptor secretagogues.** CJC-1295 is **not** a ghrelin agonist. The GH-secretagogues such as ipamorelin act at a *different* receptor — the **GHS / ghrelin receptor (GHSR-1a)**, a GHRP-like receptor — and Raun et al. showed "ipamorelin, like GHRP-6, stimulates GH release via a GHRP-like receptor," concluding that "ipamorelin is the first GHRP-receptor agonist with a selectivity for GH release similar to that displayed by GHRH" `[6]` `animal` (rat/swine pharmacology). The two receptors and the two G-protein routes (GHRH-R -> Gs/cAMP/PKA versus GHSR-1a -> Gq/PLC/IP3/Ca2+) are distinct, which is the **mechanistic basis for the GHRH-analogue + GHRP "stack"**: a GHRH-R agonist (CJC-1295/Mod GRF) and a ghrelin-receptor agonist (ipamorelin) hit the somatotrope through complementary, non-redundant pathways, producing a larger combined GH response than either alone `[5][6]` `mechanism_review`/`animal`.

### Pulsatility and the basal-GH question (DAC honesty)

A central physiological concern with a long-acting GHRH analogue is whether continuous stimulation collapses the normal pulsatile GH rhythm into a tonic "bleed." The primary human data say it largely does not — but with an important caveat. **Ionescu & Frohman (2006)** sampled GH every 20 min overnight (12 h) in healthy men before and 1 week after a single 60 or 90 µg/kg injection of CJC-1295 (DAC). They found "GH secretion was increased after CJC-1295 administration with preserved pulsatility. The frequency and magnitude of GH secretory pulses were unaltered. However, basal (trough) GH levels were markedly increased (7.5-fold; P < 0.0001) and contributed to an overall increase in GH secretion (mean GH levels, 46%; P < 0.01) and IGF-I levels (45%; P < 0.001)" `[3]` `rct`. The honest reading: **pulse architecture is preserved**, but the DAC's continuous albumin-tethered exposure raises the **trough/basal** GH dramatically (~7.5-fold), and it is this elevation of trough GH — not a change in pulse amplitude or frequency — that the authors implicate in driving the IGF-1 rise `[3]` `rct`. So the "preserved pulsatility" claim is true for pulse shape but does not mean the GH profile is unchanged: basal tone goes up substantially with the DAC form.

This is consistent with the foundational pharmacokinetics. **Teichman et al. (2006)**, in two randomized, placebo-controlled, double-blind ascending-dose trials in healthy adults (single subcutaneous doses, and weekly/biweekly multiple doses), reported that a single CJC-1295 (DAC) injection produced "dose-dependent increases in mean plasma GH concentrations by 2- to 10-fold for 6 d or more" and "IGF-I concentrations increased 1.5- to 3-fold for 9-11 d," with "the estimated half-life of CJC-1295 was 5.8-8.1 d" and IGF-I remaining elevated for up to 28 days with repeated dosing; "no serious adverse reactions were reported" `[1]` `rct`. These multi-day GH/IGF-1 elevations are the signature of the **DAC** form and again must not be attributed to no-DAC Mod GRF 1-29.

Animal data corroborate the GH-axis competence of the analogue: **Alba et al. (2006)** showed that once-daily CJC-1295 (DAC) restored normal body weight and length and GH-axis output in the **GHRH-knockout mouse**, while the same dose given every 48 or 72 h was less effective — demonstrating that the analogue acts through the intact GHRH-R/somatotrope axis and that dosing interval matters even for a long-acting agent `[7]` `animal` (GHRH-knockout mouse).

---

## Section A bibliography

[1] Teichman SL, Neale A, Lawrence B, Gagnon C, Castaigne J-P, Frohman LA. 2006 — Prolonged stimulation of growth hormone (GH) and insulin-like growth factor I secretion by CJC-1295, a long-acting analog of GH-releasing hormone, in healthy adults — *J Clin Endocrinol Metab* 91(3):799-805 — DOI 10.1210/jc.2005-1536 / PMID 16352683 — `rct`

[2] Jetté L, Léger R, Thibaudeau K, Benquet C, Robitaille M, Pellerin I, Paradis V, van Wyk P, Pham K, Bridon DP. 2005 — Human growth hormone-releasing factor (hGRF)1-29-albumin bioconjugates activate the GRF receptor on the anterior pituitary in rats: identification of CJC-1295 as a long-lasting GRF analog — *Endocrinology* 146(7):3052-3058 — DOI 10.1210/en.2004-1286 / PMID 15817669 — `mechanism_review` (primary structure-identification + rat pituitary bioassay)

[3] Ionescu M, Frohman LA. 2006 — Pulsatile secretion of growth hormone (GH) persists during continuous stimulation by CJC-1295, a long-acting GH-releasing hormone analog — *J Clin Endocrinol Metab* 91(12):4792-4797 — DOI 10.1210/jc.2006-1702 / PMID 17018654 — `rct`

[4] Feng J, et al. 2018 — Development of a novel albumin-based and maleimidopropionic acid-conjugated peptide with prolonged half-life and increased in vivo anti-tumor efficacy — *Theranostics* 8(8):2094-2106 — DOI 10.7150/thno.22069 — PMC5928873 — `mechanism_review` (MPA->albumin-Cys34 thiosuccinimide chemistry)

[5] Halmos G, Szabo Z, Dobos N, Juhasz E, Schally AV. 2025 — Growth hormone-releasing hormone receptor (GHRH-R) and its signaling — *Rev Endocr Metab Disord* 26(3):343-352 — DOI 10.1007/s11154-025-09952-x — PMC12137518 — `mechanism_review`

[6] Raun K, Hansen BS, Johansen NL, Thøgersen H, Madsen K, Ankersen M, Andersen PH. 1998 — Ipamorelin, the first selective growth hormone secretagogue — *Eur J Endocrinol* 139(5):552-561 — DOI 10.1530/eje.0.1390552 / PMID 9849822 — `animal` (GHSR/ghrelin-receptor contrast)

[7] Alba M, Fintini D, Sagazio A, Lawrence B, Castaigne J-P, Frohman LA, Salvatori R. 2006 — Once-daily administration of CJC-1295, a long-acting growth hormone-releasing hormone (GHRH) analog, normalizes growth in the GHRH knockout mouse — *Am J Physiol Endocrinol Metab* 291(6):E1290-E1294 — DOI 10.1152/ajpendo.00201.2006 / PMID 16822960 — `animal` (GHRH-knockout mouse)
