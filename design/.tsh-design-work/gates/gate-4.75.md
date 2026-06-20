# Gate 4.75 — INTEGRITY (iteration 2)

biomarker: TSH
date: 2026-06-19
iteration: 2

## Verdict

verdict: PASS

Iteration 2 confirms the IC-10 fabricated-citation finding from iteration 1 is fully resolved. Section-A bibliography entry [2] now reads: Szkudlinski MW, Fremont V, Ronin C, Weintraub BD. "Thyroid-stimulating hormone and thyroid-stimulating hormone receptor structure-function relationships." *Physiol Rev.* 2002;82(2):473–502. PMID 11917095, DOI 10.1152/physrev.00031.2001 (tag: mechanism_review, tier: 1). A live WebFetch of PubMed PMID 11917095 confirms the paper resolves to that exact title, authors, journal, year, and volume/pages, and that its scope — TSH/TSHR structure-function relationships with explicit discussion of carbohydrate domains, bioactivity, and clearance — is appropriate source material for the section-A glycosylation claims (Asn-52/78 α-subunit, Asn-23 β-subunit, ~15% carbohydrate, sulfation/sialylation). A grep of section-A confirms PMID 24295758 and `er.2012-1036` are both absent. All IC-1..IC-13 checks, population_mismatch, concentration_audit, and corpus_scoping verdicts carry forward unchanged from iteration 1 (re-validation not required; only the IC-10 citation was in dispute). Three paywalled corpus-missing WARNs (TRUST CIs, Brabant pulse amplitude) remain WARN-only and do not affect the verdict.

```json
{"phase":"4.75","verdict":"PASS","ic_checks":{"IC-1":{"status":"PASS"},"IC-2":{"status":"PASS"},"IC-3":{"status":"PASS"},"IC-4":{"status":"PASS"},"IC-5":{"status":"PASS"},"IC-6":{"status":"PASS"},"IC-7":{"status":"PASS"},"IC-8":{"status":"PASS"},"IC-9":{"status":"PASS"},"IC-10":{"status":"PASS"},"IC-11":{"status":"PASS"},"IC-12":{"status":"PASS"},"IC-13":{"status":"PASS"}},"population_mismatch":{"verdict":"PASS","checked_citations":0},"concentration_audit":{"verdict":"PASS","total_primaries":28,"largest_cluster_count":8,"share":0.29,"threshold_triggered":false},"corpus_scoping":{"verdict":"PASS","claims_checked":16,"claims_failed":[]},"halt_reasons":[],"warnings":["TRUST CIs + Brabant pulse amplitude: paywalled corpus-missing"],"iterations":2}
```
