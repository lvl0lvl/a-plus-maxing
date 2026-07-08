---
name:
  short-approach-title: edit-frozen-plan-step-for-dob-gate
type: approach
status: abandoned
session: S120
date: 2026-07-08
supersedes:
  or none: none
tags:
- area: de-id-boundary
- component: pii_scan
permalink: a-plus-maxing/approaches/2026-07-08-edit-frozen-plan-step-for-dob-gate
---

# Edit frozen plan_step.py to opt its GATE scan out of the DOB class

**What was tried:** To fix contracts-1 (the DOB class's `include_dob=True` default made `plan_step`'s GATE scan of the DERIVED plan fail-close on legitimate schedule dates → no plan), add `include_dob=False` directly to the `scan_text_full` call in `scripts/plan/plan_step.py:_scan_yield_payload`.

**Why abandoned:** `plan_step.py` is in the byte-FROZEN ADR-0032 engine glob (`scripts/plan/*.py` minus router/horizons/tailoring). The edit REDs `tests/serve/test_route.py::test_frozen_engine_byte_unchanged` + the `test_pdf_ingestion_e2e.py` numstat probe (EXTEND-NOT-REBUILD violation). Any edit — even a one-arg safety-add or a comment — adds bytes and breaks the freeze. Carving `plan_step` out of the frozen set would require an Architect ruling + updating the frozen glob in both test files = a guard-loosening (PF-S63-02 sensitivity), not a unilateral mid-review move.

**What would change the verdict:** Never, for any byte-frozen-engine file. The correct fix lives at the DEFAULT, not the call site: make the new PII class opt-IN (default off) so every frozen caller's behavior is unchanged, and opt in only at the non-frozen boundaries that need it. This generalizes: a new value-scan class added to a shared `pii_scan` utility MUST default off, because frozen callers rely on the default.

**Cross-references:**
- PR #316; the DOB-opt-in fix (commit `bfe04196`); INV-CORE-CAPABILITY; the ADR-0032 frozen-spine; [[session-120]].
