---
title: Estradiol (E2)
type: biomarker
permalink: a-plus-maxing/biomarkers/estradiol
category: blood
unit: pg/mL
source: lab
confidence: established
created: 2026-06-19
last_verified: 2026-06-19
review_cadence: per-lab-panel
provenance_dir: design/.estradiol-design-work
provenance_slug: labs-specialist
---

# Estradiol (E2)

## Metadata
- category: blood
- unit: pg/mL (× 3.671 → pmol/L; 1 pmol/L ≈ 0.272 pg/mL)
- source: lab
- confidence: established
- review_cadence: per-lab-panel
- last_verified: 2026-06-19

## Target Range
- **STRONGLY sex-, cycle phase-, and reproductive-stage-dependent — no single universal cutpoint**
- premenopausal women — early follicular (days 1–7): ~12–80 pg/mL (44–294 pmol/L)
- premenopausal women — mid-cycle / preovulatory surge (days 8–14): ~85–500+ pg/mL (~312–1,836+ pmol/L)
- premenopausal women — luteal phase (days 15–28): ~40–260 pg/mL (147–955 pmol/L)
- postmenopausal women (no HRT): ~<10–30 pg/mL (<37–110 pmol/L)
- adult men (LC-MS/MS, Frederiksen 2020, n=1,838): ~14–41 pg/mL (50–150 pmol/L)
- **ASSAY CAVEAT: immunoassays are INACCURATE at low E2 levels (<20–30 pg/mL). Use LC-MS/MS for men, postmenopausal women, AI-monitoring, and pediatric testing. Immunoassay positive bias 14–239% vs. GC-MS reference.**
- **Interpret premenopausal women's values WITH documented cycle phase — result uninterpretable otherwise.**
- source of target: [[library/biomarkers/estradiol/research-report]] + Frederiksen 2020 (PMID 31720688) + Rosner 2013 Endocrine Society position statement (PMID 23463657) + Stuenkel 2015 (PMID 26444994)

## Current Value
- value: pending (not yet measured)
- trend: n/a
- history pointer: pending — first lab panel July 2026

## Affected By
- RAISED: obesity/↑adipose aromatase (↑E2 in both sexes; functional hypogonadotropic hypogonadism loop in obese men); exogenous estrogen/HRT (oral, transdermal, injectable); estrogen-secreting tumors (ovarian granulosa cell, Sertoli-Leydig, adrenal cortical, ectopic aromatase-producing); hCG (stimulates gonadal E2 secretion); cirrhosis/liver disease (impaired E2 clearance + ↑aromatization); pregnancy (fetoplacental E2, rises to tens of thousands of pg/mL at term); hyperthyroidism (↑SHBG → altered E2/T ratio); aromatase excess syndrome (rare CYP19A1 gain-of-function)
- LOWERED: menopause/ovarian failure/POI (cessation of follicular production → <10–30 pg/mL); aromatase inhibitors (anastrozole, letrozole, exemestane — suppress E2 >95% in postmenopausal women; used in breast cancer, sometimes misused in men); GnRH agonists/antagonists (castrate-level suppression); primary or secondary hypogonadism; low energy availability/anorexia/hypothalamic amenorrhea (GnRH suppression → near-absent follicular E2; mechanism of bone loss in female athlete triad); clomiphene/fulvestrant (block or degrade ER — functional E2 antagonism rather than true lowering)
- Assay artifact — RAISED falsely: immunoassay at low E2 levels (positive bias 14–239%); high-dose biotin ≥5 mg/day (competitive immunoassay platforms); heterophile antibodies (rare; documented cases of extreme false elevation); estrone/estrone-sulfate cross-reactivity
- Assay artifact — direction reverses: biotin in sandwich immunoassay formats (false suppression)

## Why It Matters
Estradiol is the most potent estrogen and the dominant sex steroid of the reproductive years. In premenopausal women it drives the menstrual cycle (follicular growth, endometrial proliferation, the LH surge), is the primary marker for ovarian function and reserve, guides IVF stimulation protocols, and tracks the menopausal transition. In postmenopausal women, E2 monitoring guides hormone replacement adequacy and aromatase-inhibitor therapy in breast cancer. In men, E2 is not a trace byproduct — it is physiologically required: Finkelstein 2013 (N Engl J Med, N=400 RCT) demonstrated that E2 deficiency (from aromatase inhibition) causes fat mass accumulation and sexual dysfunction in men regardless of testosterone status, and bone-protective effects in men require E2 ≥~20 pg/mL. The testosterone:E2 balance from peripheral aromatization (CYP19A1 in adipose, bone, brain) is a key axis; over-suppression of E2 in men via exogenous aromatase inhibitors causes bone loss, impaired libido, and metabolic dysfunction. Clinically meaningful associations: breast cancer risk in postmenopausal women follows a dose-response relationship (EHBCCG RR 2.00 for highest vs. lowest quintile; 663 cases, 1,765 controls); cardiovascular benefit of estradiol replacement follows a timing hypothesis (ELITE trial: CIMT benefit with initiation ≤6 years of menopause, absent ≥10 years postmenopause). The measurement caveat is load-bearing: immunoassays are inaccurate at the low concentrations found in men, postmenopausal women, and children — LC-MS/MS is the required method for clinical decisions in these groups.

## Relations
- [[biomarkers/total-testosterone]]
- [[biomarkers/shbg]]
- [[biomarkers/free-testosterone]]
- [[library/biomarkers/estradiol/research-report]]
