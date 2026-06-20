# Section A: What Resting Heart Rate Is & What the Device Measures

## Definition

Resting heart rate (RHR) is the number of heartbeats per minute (bpm) when the body is at complete physical and mental rest — no recent exertion, no acute emotional stress, no digestion-related cardiovascular demand. Normal adult RHR falls between 60 and 100 bpm by convention, though the meaningful physiological range is considerably narrower for most healthy adults and extends well below 60 bpm in conditioned individuals.

## The Electrical Origin: The Sinoatrial Node and Its Intrinsic Rate

The heart's rhythm originates at the **sinoatrial (SA) node**, a specialized cluster of pacemaker cells in the right atrium. These cells possess automaticity — they depolarize spontaneously without external input [1, mechanism_review]. Under complete pharmacological blockade of both the sympathetic and parasympathetic divisions (using propranolol plus atropine to eliminate all autonomic influence), the human SA node fires at an intrinsic rate of roughly **90–100 bpm**, declining with age according to the approximation IHR ≈ 118 − (0.57 × age) [2, mechanism_review]. This intrinsic rate represents the SA node's baseline automaticity — what the heart would do if the nervous system were entirely removed from the equation.

The resting heart rate a person actually has is almost always lower than this intrinsic rate. The gap is explained by the autonomic nervous system.

## Autonomic Balance: Why Vagal Tone Dominates at Rest

Two branches of the autonomic nervous system converge on the SA node and continuously modulate its firing rate [1, mechanism_review]:

- **Parasympathetic (vagal) input** — The vagus nerve releases acetylcholine, which binds M2 muscarinic receptors on SA-node cells. This hyperpolarizes the membrane (shifts the resting potential more negative), slows the rate of spontaneous depolarization, and increases the time to each action potential. The net effect is a reduced heart rate — **negative chronotropy**.
- **Sympathetic input** — Norepinephrine and epinephrine bind β1-adrenergic receptors, accelerating spontaneous depolarization and increasing firing rate — **positive chronotropy**.

At rest in healthy adults, parasympathetic tone is dominant [1, mechanism_review]. The vagus nerve exerts a continuous "brake" on the SA node, pulling the heart rate from its ~100 bpm intrinsic baseline down into the 50–80 bpm range typical of healthy resting adults. Higher vagal tone at rest is a recognized index of cardiovascular health; in animal models, lower vagal tone is associated with elevated cardiovascular risk [3, animal], a relationship that converges with human epidemiological data linking reduced heart rate variability (a proxy for vagal tone) to adverse outcomes.

## Fitness and RHR: The Athlete's Bradycardia

A lower RHR generally reflects greater aerobic fitness, and this relationship has a mechanistic basis in **stroke volume**. Cardiac output (CO) = stroke volume (SV) × heart rate (HR). An endurance-trained heart generates a larger stroke volume at rest — through structural remodeling of the left ventricle, including increased chamber volume and wall mass [4, cohort]. With each beat delivering more blood, fewer beats per minute are required to maintain the same resting cardiac output. The result is a physiologically low RHR.

Endurance athletes commonly exhibit resting heart rates in the **40–55 bpm range** — a phenomenon called **physiological sinus bradycardia** [5, mechanism_review; 10, meta_analysis]. In elite endurance athletes, RHR is substantially lower than in the general population, and this lower rate is mechanistically linked to the enlarged left ventricular dimensions and the compensatory cardiac output regulation they enable [4, cohort].

Interestingly, sustained endurance training does not lower RHR solely by increasing vagal tone. Animal studies (confirmed by autonomic blockade experiments) demonstrate that training also produces **intrinsic electrophysiological remodeling of the SA node itself** — specifically, downregulation of the HCN4 "funny current" channel that drives spontaneous pacemaker depolarization [6, animal] (mouse model; mechanism extrapolated to humans). This remodeling is reversible: detraining restores normal HCN4 expression and resting heart rate within weeks. The practical implication is that RHR reflects both the nervous system's influence on the heart and the heart's own structural-electrical state.

## Distinguishing RHR from Related Metrics

Two related concepts are sometimes conflated with RHR:

- **Maximum heart rate (HR_max)** — the highest heart rate achievable under maximal exertion. Unlike RHR, HR_max is largely determined by age (~220 − age as a rough estimate) and does not reflect fitness in the same direct way.
- **Heart rate reserve (HRR)** — HR_max minus RHR. HRR is used to set exercise intensity targets (e.g., the Karvonen formula: target HR = RHR + % × HRR). Because a lower RHR from fitness increases HRR, it expands the usable training range.

RHR is the resting anchor of this system. It is the metric most directly responsive to long-term aerobic training, day-to-day autonomic state, and chronic health changes.

## What Wearables Actually Measure

Consumer wearables derive heart rate from **photoplethysmography (PPG)** — an optical method in which a light-emitting diode (typically green LED, sometimes near-infrared) shines into the skin, and a photodetector captures the fraction of light reflected back [7, mechanism_review; 8, cohort]. As the heart beats, blood volume in the capillary bed beneath the sensor rises and falls; this modulates light absorption, producing a pulsatile signal. The device's algorithm extracts the pulse rate from this signal. Chest-strap monitors use a different approach — **ECG-derived electrical detection** of the R-wave — which is generally more accurate, especially during motion, because it measures the electrical event directly rather than its vascular consequence.

For **resting heart rate specifically**, PPG performance is strong. At rest, with minimal motion artifact and stable ambient light, wearable PPG devices achieve mean absolute errors of approximately **2 bpm** against ECG reference standards, with concordance classified as moderate to excellent [8, cohort]. This contrasts with the substantially larger errors seen during exercise, where motion artifact dominates. HR measurement at rest is fundamentally easier for PPG than heart rate variability (HRV) measurement — a single average beat rate is far less sensitive to timing noise than the precise beat-to-beat interval precision that HRV requires (Section C).

### The Definition Problem: What "Resting HR" Means on Your Device

The phrase "resting heart rate" is not standardized across manufacturers, and different device definitions produce systematically different numbers [9, cohort]:

- **Garmin** defines resting HR as the lowest 30-minute moving average within a 24-hour period.
- **Oura** computes a continuous overnight average from 10-minute segments throughout sleep.
- **WHOOP** weights the nightly calculation toward readings captured during slow-wave sleep.
- **Polar** restricts the window to the first four hours post-sleep-onset.
- **Apple and Samsung** sample HR every 5 minutes during rest periods and derive their reported value from these samples.

Validation data show that Oura (ring form factor, worn on the finger with a shorter optical path through tissue) achieves the highest nocturnal RHR accuracy (concordance correlation coefficient 0.97–0.98, mean absolute percentage error ~1.7–1.9%), outperforming wrist-worn devices in head-to-head nocturnal comparisons [9, cohort].

These definitional differences have a direct practical consequence: a person who owns both a Garmin and an Oura will routinely see different "resting HR" numbers even on the same night, not because one is wrong but because they are measuring different things under the same label. **Values from different devices are not directly interchangeable.** Trending within a single device is meaningful; cross-device comparisons require caution.

The wearable's reported RHR — whatever its specific definition — is a valid longitudinal health signal. A sustained rise of 5–7 bpm above personal baseline is a clinically meaningful deviation that warrants attention [9, cohort]. But the number should always be interpreted relative to the device and its algorithm, not as an absolute physiological ground truth.

---

## Bibliography

1. MacDonald EA, Rose RA, Quinn TA. Neurohumoral Control of Sinoatrial Node Activity and Heart Rate: Insight From Experimental Models and Findings From Humans. *Frontiers in Physiology*. 2020;11:170. doi:10.3389/fphys.2020.00170 — tag: mechanism_review — tier: 2

2. Opthof T. The normal range and determinants of the intrinsic heart rate in man. *Cardiovascular Research*. 2000;45(1):177–184. doi:10.1016/S0008-6363(99)00322-3 — tag: mechanism_review — tier: 2

3. Carnevali L, Sgoifo A. Vagal modulation of resting heart rate in rats: the role of stress, psychosocial factors, and physical exercise. *Frontiers in Physiology*. 2014;5:118. doi:10.3389/fphys.2014.00118 — tag: animal — tier: 2

4. Letnes JM, Nes BM, Sandbakk Ø, et al. Comparison of resting heart rate and left ventricular ejection fraction in elite endurance athletes and the general population. *European Journal of Preventive Cardiology*. 2024. doi:10.1093/eurjpc/zwae294 — tag: cohort — tier: 2

5. Jamieson A, Chico TJA, Jones S, et al. A guide to consumer-grade wearables in cardiovascular clinical care and population health for non-experts. *NPJ Cardiovascular Health*. 2025. PMID:40909206. doi:10.1038/s44325-025-00082-6 — tag: mechanism_review — tier: 2

6. D'Souza A, Bucchi A, Johnsen AB, et al. Exercise training reduces resting heart rate via downregulation of the funny channel HCN4. *Nature Communications*. 2014;5:3775. PMID:24825544. doi:10.1038/ncomms4775 — tag: animal — tier: 2

7. Charlton PH, Kyriacou PA, Mant J, et al. Wearable Photoplethysmography for Cardiovascular Monitoring. *Proceedings of the IEEE*. 2022. PMID:35356509. doi:10.1109/JPROC.2022.3149785 — tag: mechanism_review — tier: 2

8. Bent B, Goldstein BA, Kibbe WA, Dunn JP. Investigating sources of inaccuracy in wearable optical heart rate sensors. *NPJ Digital Medicine*. 2020;3:18. PMID:32047863. doi:10.1038/s41746-020-0226-6 — tag: cohort — tier: 2

9. Dial MB, Hollander ME, Vatne EA, et al. Validation of nocturnal resting heart rate and heart rate variability in consumer wearables. *Physiological Reports*. 2025. PMID:40834291. doi:10.14814/phy2.70527 — tag: cohort — tier: 2

10. Reimers AK, Knapp G, Reimers CD. Effects of exercise on the resting heart rate: a systematic review and meta-analysis of interventional studies. *Journal of Clinical Medicine*. 2018;7(12):503. PMID:30513777. doi:10.3390/jcm7120503 — tag: meta_analysis — tier: 1
