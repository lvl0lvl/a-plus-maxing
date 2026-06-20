# Section A: What Respiratory Rate Is & What the Device Measures

## Definition and Units

**Respiratory rate (RR)** is the number of complete breathing cycles — one inhalation plus one exhalation — completed per minute, expressed in **breaths per minute (breaths/min, brpm)**. At rest in healthy adults, RR normally falls in the range of **12–20 breaths/min** [1, cohort]. During sleep — the window most consumer wearables target — resting nocturnal RR in a large healthy-adult cohort (n = 10,000) centers around **15.4 breaths/min**, with 90% of values falling between 11.8 and 19.2 breaths/min [2, cohort]. Common clinical documentation of 18 or 20 breaths/min as a default, rather than an actual count, is a well-characterized measurement failure [1, cohort]. RR is distinct from **tidal volume** (air volume per breath, typically ~0.5 L at rest) and **minute ventilation** (RR × tidal volume, ~6–8 L/min at rest): wearables measure rate only, not volume or flow.

RR occupies a foundational place in clinical medicine as one of the **four classic vital signs** alongside heart rate, blood pressure, and temperature. It is also a durable prognostic signal: in a prospective community cohort of older adults, a mean nocturnal RR ≥ 16 breaths/min was independently associated with cardiovascular mortality (HR 1.57–2.58 across two cohorts) and all-cause mortality (HR 1.18–1.50), after adjustment for sleep-disordered breathing and comorbidities [3, cohort].

---

## Neural Architecture of Breathing: The Brainstem Control System

RR is not determined at the lungs; it emerges from a distributed network of brainstem nuclei. The **pre-Bötzinger complex (preBötC)**, located in the ventrolateral medulla, serves as the primary **inspiratory rhythm generator**. It contains glutamatergic excitatory interneurons and GABAergic/glycinergic inhibitory interneurons arranged in circuits capable of producing rhythmic inspiratory bursts [4, mechanism_review]. Rhythm generation in the preBötC appears to depend on emergent network properties rather than solely on intrinsic neuronal pacemaker activity: blocking persistent sodium current does not abolish the rhythm, implicating circuit-level recurrence [5, mechanism_review].

The **parafacial respiratory group / retrotrapezoid nucleus (pFRG/RTN)**, ventral to the facial nucleus, governs active expiration and functions as the primary **CO₂-sensing relay** to the rhythm generator. Phox2b-expressing neurons here are intrinsically sensitive to CO₂ and pH, directly coupling brainstem chemistry to ventilatory drive [4, mechanism_review; 6, mechanism_review]. During quiet breathing at rest, expiration is passive; the pFRG/RTN becomes recruitable under hypercapnic load or high metabolic demand.

The **pontine respiratory groups** — principally the Kölliker-Fuse nucleus (KF) and the parabrachial complex in the dorsolateral pons — do not generate rhythm independently. They **shape and adapt the breathing pattern** by governing the inspiratory off-switch (the phase transition from inspiration to expiration) and coordinating upper-airway resistance via descending projections [7, mechanism_review]. The KF-area receives ascending drive from the preBötC and projects back to modulate phase timing, thereby influencing breath duration and, through its inverse, respiratory rate.

---

## Chemical Drive: CO₂/pH Is Primary, O₂ Is Secondary

The dominant **chemical drive** to breathe is CO₂ and its surrogate, arterial pH, sensed by **central chemoreceptors** distributed across multiple brainstem loci including the RTN, locus ceruleus, and raphe nuclei. These neurons detect rising PCO₂ / falling pH and increase the output of the inspiratory rhythm generator, accelerating both depth and rate of breathing [6, mechanism_review]. The response is tonic and continuous: normal resting PaCO₂ (~40 mmHg) exerts background drive that, if withdrawn by prolonged hyperventilation, would produce apnea.

**Peripheral chemoreceptors** — principally the carotid bodies at the carotid bifurcation — are the primary sensors of arterial **O₂ partial pressure (PaO₂)**. They fire when PaO₂ falls below roughly 70 mmHg and relay signals via the glossopharyngeal nerve to the nucleus tractus solitarius [6, mechanism_review]. They also potentiate the central CO₂ response: bilateral carotid denervation depresses hyperoxic CO₂ sensitivity and causes sustained hypoventilation with PaCO₂ retention of 5–13 mmHg [6, mechanism_review]. In healthy adults at sea level, CO₂/pH dominates moment-to-moment RR regulation; the hypoxic drive is a reserve mechanism.

Beyond chemistry, RR is modulated by:

- **Mechanoreceptor feedback** — pulmonary stretch receptors (Hering-Breuer reflex) limit tidal volume inflation, influencing rate via vagal afferents.
- **Metabolic demand** — exercise increases RR and tidal volume; central command and muscle afferent feedback together account for ~40–50% of exercise hyperpnea [6, mechanism_review].
- **Emotional and volitional override** — cortical and limbic projections to the brainstem allow voluntary breath-holding, emotional sighing, and speech patterning.
- **Sleep state** — RR is most stable and lowest in NREM sleep; REM sleep introduces irregularity. The NREM window is the physiological basis for wearable nocturnal averaging.

---

## What Consumer Wearables Actually Measure

Most consumer wearables (Oura Ring, Apple Watch, Fitbit, WHOOP, Garmin) **do not directly count breaths**. Instead, they **derive RR from the photoplethysmography (PPG) signal** — an optical sensor that shines infrared or green light into peripheral tissue and detects pulsatile changes in blood volume. Three physiological mechanisms allow respiration to be extracted from the cardiac waveform [2, cohort; 8, open_label]:

1. **Respiratory sinus arrhythmia (RSA) — frequency modulation:** Vagal tone to the sinoatrial node varies with the respiratory cycle; heart rate rises slightly during inhalation and falls during exhalation. This creates a spectral peak in the heart-rate-variability power spectrum at exactly the breathing frequency. Isolating this RSA peak from the inter-beat-interval time series yields RR. This method achieves root-mean-square error of ~0.65 breaths/min and mean absolute error of ~0.46 breaths/min against polysomnography ground truth, with mean absolute percentage error of ~3% and Pearson r = 0.95 [2, cohort] (note: all authors were Fitbit employees; manufacturer-affiliated validation).

2. **Amplitude modulation:** Intrathoracic pressure swings during breathing alter venous return and stroke volume, which in turn modulates the peak-to-trough amplitude of the PPG waveform on a breath-by-breath basis.

3. **Baseline / baseline-wander modulation:** Changes in arterial vasoconstriction and peripheral tissue blood volume driven by respiratory mechanics produce a slow oscillation in the DC baseline of the PPG signal at the breathing frequency.

Device algorithms typically **fuse** two or more of these signals to improve robustness against artifact. Some platforms also incorporate **accelerometry** (wrist or ring micro-movement driven by chest excursion) as an additional modality [8, open_label]. Because motion artifacts corrupt all three PPG modulation mechanisms, virtually all consumer devices restrict their RR estimate to the **overnight sleep window** and report a **single nightly average** rather than continuous breath-by-breath data.

**What this means for interpretation:** PPG-derived nocturnal RR is an **estimate of resting ventilatory rate** during sleep, not a direct measurement of airflow or ventilation. It captures rate but not tidal volume or minute ventilation. It is most accurate in the low-motion NREM sleep window; accuracy degrades at higher respiratory rates because RSA amplitude weakens as RR rises above ~20 breaths/min [2, cohort]. The signal is fundamentally different from clinical capnography or respiratory inductance plethysmography — the gold standard used in polysomnography — but provides a practical, high-frequency window into resting breathing physiology that was previously inaccessible outside a sleep laboratory.

---

## Bibliography

1. Badawy J, Nguyen OK, Clark C, Halm EA, Makam AN. Is everyone really breathing 20 times a minute? Assessing epidemiology and variation in recorded respiratory rate in hospitalised adults. *BMJ Quality & Safety*. 2017;27(11):842–848. PMID: 28652259 — tag: cohort — tier: 2

2. Natarajan A, Su H-W, Heneghan C, Blunt L, O'Connor C, Niehaus L. Measurement of respiratory rate using wearable devices and applications to COVID-19 detection. *npj Digital Medicine*. 2021;4:136. PMID: 34526602 — tag: cohort — tier: 2

3. Baumert M, Linz D, Stone K, McEvoy RD, Cummings S, Redline S, Mehra R, Immanuel S. Mean nocturnal respiratory rate predicts cardiovascular and all-cause mortality in community-dwelling older men and women. *European Respiratory Journal*. 2019;54(1):1900120. PMID: 31151958 — tag: cohort — tier: 1

4. Ikeda K, Kawakami K, Onimaru H, Okada Y, Yokota S, Koshiya N, Oku Y, Iizuka M, Koizumi H. The respiratory control mechanisms in the brainstem and spinal cord: integrative views of the neuroanatomy and neurophysiology. *Journal of Physiological Sciences*. 2017;67(1):45–62. PMID: 27535569 — tag: mechanism_review — tier: 2

5. Feldman JL, Mitchell GS, Nattie EE. Breathing: rhythmicity, plasticity, chemosensitivity. *Annual Review of Neuroscience*. 2003;26:239–266. PMID: 12598679 — tag: mechanism_review — tier: 1

6. Dempsey JA, Smith CA. Pathophysiology of human ventilatory control. *European Respiratory Journal*. 2014;44(2):495–512. PMID: 24925922 — tag: mechanism_review — tier: 1

7. Dutschmann M, Dick TE. Pontine mechanisms of respiratory control. *Comprehensive Physiology*. 2012;2(4):2443–2469. PMID: 23720253 — tag: mechanism_review — tier: 2

8. Kim H, Kim J-Y, Im C-H. Fast and robust real-time estimation of respiratory rate from photoplethysmography. *Sensors (Basel)*. 2016;16(9):1494. PMID: 27649182 — tag: open_label — tier: 3
