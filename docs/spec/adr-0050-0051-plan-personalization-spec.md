---
scope: "ADR-0050 ADR-0051 (front-door plan personalization: wire the assembler into authoring + reverse the raw-genotype carve-out)"
adrs: [ADR-0050, ADR-0051]
tier: 2
created: 2026-07-17
status: approved
---

# Spec: Front-Door Plan Personalization — Wire the Context Assembler into Authoring, Contract-Driven Genetics-Aware Prompts, and the Raw Genetic Panel Identity-Stripped

## Component Overview

This spec implements the two-ADR plan-personalization cluster that makes the `/generate-plan` front door author each specialist from the operator's real, identity-stripped record instead of a coarse band-derived generic. It delivers three tasks across two ADRs: (1) repoint the front-door author input from `router.summarize`'s ~18-token band to ADR-0042's `assemble_context` identity-stripped FULL record, so the model author call reads the operator's real program/symptoms/supplement detail (ADR-0050-T1); (2) rewrite the author system prompt to be contract-driven — each specialist carries its own `design/specialist-plan-contracts.md` Inputs/Monitoring/Tracking/Analysis→plan contract — and genetics-aware, with an explicit directive to personalize off the de-identified record and interpret raw `GENE rsID = (C;C)`-shaped genotype calls, plus an uncertainty/confidence directive for the un-vetted SNPs (ADR-0050-T2); and (3) reverse the ADR-0032/0042 raw-genotype carve-out — carry the operator's FULL raw `dna-report` genetic panel (all ~117 stored SNPs — the live-measured count as of S145; the source ADR-0051's earlier "115" was an earlier point-in-time read) to the specialists identity-stripped through the assembler's existing `pii_scan` gate, via a separate `dna-report`-source read path that keeps `router.py` frozen (ADR-0051-T1).

The root cause the cluster fixes is verified against the live tree: `_do_generate_plan` derives `summary = router.summarize(store_read)` ([server.py:815](../../scripts/serve/server.py)), pre-authors it through the model at `self.client.author(domain, summary)` ([server.py:832](../../scripts/serve/server.py)), and hands the pre-authored envelopes to `orchestrate.generate_plans` ([server.py:843](../../scripts/serve/server.py)), which calls `compute_plan(domain, author_output, store_read, gates=gates)` with **no `client=`** ([orchestrate.py:794](../../scripts/plan/orchestrate.py)); inside `compute_plan`, `client = client if client is not None else _FixedEnvelopeClient(author_output)` ([generate_plan.py:555](../../scripts/plan/generate_plan.py)) replays the thin envelope and DISCARDS `summary = context_assembler.assemble_context(store_read)` ([generate_plan.py:560,566](../../scripts/plan/generate_plan.py)). The assembler ADR-0042 built to end DATA-COLLAPSE runs on the front door and reaches no model. ADR-0050 decides HOW the author consumes whatever the assembler carries (wire the record + upgrade the prompt); ADR-0051 decides WHAT genetic signal reaches it (raw genotypes identity-stripped, superseding the carve-out). Labs, medications, and free-text already flow identity-stripped as the assembler's built behavior under the operator's identity-stripping-only de-id standard ([context_assembler.py:54-65](../../scripts/plan/context_assembler.py)) — this spec consumes that, it does not decide it.

The upstream dependency is ADR-0042's `assemble_context` (built and importable) and the 494-line `design/specialist-plan-contracts.md` (the single source the activation roster is already built from). The downstream consumer is the operator-present LIVE run — the load-bearing, non-mock verification that real plan quality reflects the operator's actual record (ADR-0050 OQ-3) and cites operator-specific raw genetic detail (ADR-0051 OQ-4). It is a **mock/fixture build at $0**: fixture/spy model clients, synthetic-genotype store fixtures, no live SDK call and no spend. The operator-present run is operator-gated and **out of this spec's build scope**; it is recorded below as the Phase-1 and Phase-2 exit gates. The frozen ADR-0032 six (`store.py`/`keying.py`/`pipeline.py`/`adjudicate.py`/`adjust.py`/`router.py`) stay byte-frozen (numstat = 0 vs `3ab1c3ab`); every change lands in `server.py`/`client.py`/`context_assembler.py` and their tests. This is a PUBLIC repo — every fixture is synthetic.

**Informing artifacts:** `docs/adr/ADR-0050-wire-assembler-contract-driven-authoring.md`, `docs/adr/ADR-0051-reverse-raw-genotype-carve-out.md` (both read in full), `design/specialist-plan-contracts.md` (the per-specialist authoring contract), ADR-0042's built `scripts/plan/context_assembler.py`.

## Unresolved Concerns Disposition

| Source | Item | Summary | Disposition | Rationale |
|--------|------|---------|-------------|-----------|
| ADR-0050 OQ-1 | Open Question | Inject the client through `generate_plans`→`compute_plan`, or repoint the server pre-author at `server.py:832`? | Proceed | **Pinned in ADR-0050-T1: repoint the server pre-author.** `_do_generate_plan` authors each domain against a newly-computed `context_assembler.assemble_context(store_read)` record (the existing `self.client.author` calls at [server.py:832](../../scripts/serve/server.py) candidate pass + [server.py:860](../../scripts/serve/server.py) Leg-2), leaving `summary = router.summarize(store_read)` ([server.py:815](../../scripts/serve/server.py)) for `active_plan_domains` selection unchanged. Chosen over the `compute_plan(client=)` injection because that path leaves the server's thin pre-author at :832 authoring the band into `author_output`, which `compute_plan` then ignores — a second model call per domain (double authoring). The repoint is the single-model-call seam. The confirmation test (author payload carries free-text) holds either way (ADR-0050 OQ-1). |
| ADR-0050 OQ-2 | Open Question | Full per-specialist contract vs a relevance slice of it, to bound prompt size? | Proceed | **Pinned in ADR-0050-T2: the full per-specialist contract section** — each domain's `_author_system_prompt(domain)` carries all four sub-sections (Inputs/Monitoring/Tracking/Analysis→plan) of that ONE domain's `specialist-plan-contracts.md` section, never all 18 specialist sections / never the whole file, and never a sub-slice. Token-cost tradeoff: each author call grows by that domain's ~30-line section; the ADR review trigger "re-evaluate the full-contract prompt against a per-specialist relevant slice" is the escape hatch if per-generation cost crosses an operational threshold — i.e. full-now / slice-if-needed, matching the ADR's stated posture. |
| ADR-0050 OQ-3 | Open Question | The operator-present LIVE `/generate-plan` run over the assembled record spends model budget on real data. | Proceed | Operator-gated, OUT of build scope. The build wires + mock/fixture-tests at $0; the LIVE run is recorded as the Phase-1 exit gate (Test Strategy → Operator-Present Exit Gates), the only step that confirms real plan quality — the load-bearing new dependency ADR-0050 creates. |
| ADR-0051 OQ-1 | Open Question | Genetics carry MECHANISM: a separate `dna-report`-source read path vs adding a genetics class to `_HEALTH_SUBSTANCE_ALLOWLIST`. | Proceed | **Pinned in ADR-0051-T1: a separate `dna-report`-source read path.** The allowlist mechanism trips the load-time partition assert ([context_assembler.py:80-84](../../scripts/plan/context_assembler.py)) — `dna-report` is not a `router.EXCLUDED_RAW_PII` class, so using the allowlist would force adding a genetics class to `EXCLUDED_RAW_PII`, a `router.py` edit (frozen). The separate path keeps `router.py` frozen (the frozen-surface probe enforces it). |
| ADR-0051 OQ-2 | Open Question | Scope the assembler genotype-rejection to exempt only genetics, or blanket-remove it? | Proceed | **Pinned in ADR-0051-T1: SCOPED exemption.** The `_RAW_GENOTYPE_PATTERNS` rejection at [context_assembler.py:178-187](../../scripts/plan/context_assembler.py) is exempted ONLY for the genetics read path; the guard STAYS fail-closed on every non-genetics carry (a genotype smuggled into `raw-nutrition-free-text` still raises). Blanket removal is a silent safety-property loss — out of scope by default. |
| ADR-0051 OQ-3 | Open Question | The RAW carry set — full stored panel or sensitive-variant exclusions? | Resolved | RESOLVED 2026-07-17 by explicit operator decision: the FULL stored panel crosses raw identity-stripped, INCLUDING APOE/DRD2/BDNF. The operator's uniform "raw if identity-stripped" standard supersedes ADR-0032's sensitive-variant exclusions. No exclusion in scope (ADR-0051-T1 AC-1 asserts the full panel, no filter). |
| ADR-0051 OQ-4 | Open Question | The operator-present LIVE run carries the operator's real genome to the no-train API. | Proceed | Operator-gated, OUT of build scope. The build wires + mock/fixture-tests at $0; the LIVE run is the Phase-2 exit gate (Test Strategy → Operator-Present Exit Gates) — the first time the real genome egresses. |
| ADR-0051 OQ-5 | Open Question | What verifies the specialist's genotype-interpretation quality for the ~105 un-vetted SNPs? | Proceed | Realized in ADR-0050-T2: an uncertainty/confidence directive in the specialist prompt (the model must flag confidence when interpreting an uncurated genotype from its own knowledge). The un-vetted read is operator-accepted "for now" (like the re-identification exposure); the derived/library layer stays the vetted read for the curated variants. |
| ADR-0009 tension | Tension (Pending) | The un-vetted raw carry — the ~105 uncurated SNPs reach the specialist interpreted from ungated model knowledge, not the vetted `aplus-research` library read. | Proceed | Documented assumption, operator-accepted "for now". Bounded by ADR-0050-T2's uncertainty directive (OQ-5); the derived/library layer remains the vetted read for the curated variants. A clinical-safety, not privacy, tension — recorded, not blocked. |
| ADR-0051 Negative-1 | Unmitigated Risk | Raw genotypes are inherently re-identifying; identity-stripping does NOT anonymize a genome. | Proceed | Non-falsifiable residual, stated not probed (ADR-0051 Validation). Operator-signed-off and provisional ("for now"); the standing retraction target is Alternative B (derived-classes path). Not mitigable by the build — the identity strip holds (ADR-0051-T1 AC-2), but anonymity is out of scope and unachievable. |
| ADR-0032 clinical-appropriateness axis (via ADR-0051 reversal) | Unmitigated Risk | ADR-0032 excluded APOE/DRD2/BDNF on TWO axes — privacy AND clinical-appropriateness (non-actionable / "APOE is a medical conversation, not a plan input"); the operator's "raw if identity-stripped" reversal (ADR-0051) dispositions ONLY the privacy axis. | Proceed | Documented residual, parallel to Negative-1 / Negative-2. The clinical-appropriateness / non-actionable axis is DISTINCT from the privacy axis the reversal resolved, and it is NOT actively mitigated on the front-door build path: §17 medical-safety-reviewer is a DEPLOY-gate, not a runtime contributor (`design/specialist-plan-contracts.md:436`), and ADR-0050-T2 AC-3's uncertainty directive targets interpretation-CONFIDENCE, not clinical-lane — no `safety_review`/§16/§17 pass is wired on the `_do_generate_plan` path (0 refs in `server.py`/`orchestrate.py`/`care_chat.py`). It rests on the operator's "for now" acceptance (the same posture as the re-identification Negative-1 and un-vetted Negative-2 / ADR-0009 residuals) plus the Phase-2 operator-present LIVE exit gate. The full raw 117-SNP panel still crosses identity-stripped exactly as specced — this row DOCUMENTS the residual, it does NOT narrow the carry or re-introduce any variant exclusion. Actively mitigating this axis (a runtime genetic-lane screen or a medical-safety pass wired on the front-door path) is a follow-on ADR decision — operator-owned, out of this spec's scope. |

**No Block dispositions.** Nothing blocks the mock/fixture build. No research-spike (`T0`) task is required. Every Proceed is resolved by a named task's acceptance criteria or the recorded operator-present exit gate; the two non-falsifiable residuals (re-identification exposure, un-vetted read) are operator-accepted documented assumptions.

**Out-of-both-ADRs note (raw medications):** the raw `medication-list` on `_HEALTH_SUBSTANCE_ALLOWLIST` ([context_assembler.py:62](../../scripts/plan/context_assembler.py)) already crosses identity-stripped and coexists with ADR-0035's derived `rx-interaction-classes` token — no decision required (ADR-0050 revision history, 2026-07-17). No task in this spec touches the medication carry.

## File Manifest

| File | Action | Purpose |
|------|--------|---------|
| `scripts/serve/server.py` | Modify | (ADR-0050-T1) In `_do_generate_plan`, compute `context_assembler.assemble_context(store_read)` and repoint the two existing front-door author-input sites — the candidate-pass `self.client.author(domain, ...)` at :832 and the Leg-2 `_author_rich` at :860 — to author against that identity-stripped record instead of the `router.summarize` band; leave the `router.summarize`-derived `active_plan_domains` selection at :815-817 unchanged |
| `tests/serve/test_generate_plan_authoring.py` | Create | (ADR-0050-T1) RED-capable: drives `_do_generate_plan` with a spy `self.client` over a seeded store; asserts every captured author call's summary arg carries `assemble_context`'s free-text fields, the reversion-to-band mutation REDs it, active-domain selection is unchanged, no new model call, frozen-six numstat empty |
| `scripts/model/client.py` | Modify | (ADR-0050-T2) Rewrite `_author_system_prompt(domain)` at :510 into a contract-driven, genetics-aware prompt: source each domain's full `specialist-plan-contracts.md` section (runtime-derived or drift-guarded, not a hand-embedded copy — the single-source invariant, AC-6), add the personalize directive, the raw rsID+allele genotype-interpretation directive, and the uncertainty/confidence directive; add the domain→contract-section map |
| `tests/model/test_client.py` | Modify | (ADR-0050-T2) Add contract-content-present, genetics-directive-present, uncertainty-directive-present, per-specialist-scoping, and strip-REDs-it assertions for `_author_system_prompt` |
| `scripts/plan/context_assembler.py` | Modify | (ADR-0051-T1) Add a separate `dna-report`-source read path that carries the FULL raw genotype panel (all stored SNPs incl. APOE/DRD2/BDNF) through the reused `pii_scan` identity strip; SCOPE the `_RAW_GENOTYPE_PATTERNS` rejection at :178-187 to exempt ONLY the genetics path (guard stays on every non-genetics carry); the derived `genetic-trait-classes` token rides alongside unchanged |
| `tests/plan/test_context_assembler.py` | Modify | (ADR-0051-T1) Add raw-panel-carried, identity-leak-probe, genotype-rejection-scoped, derived-token-still-crosses, and frozen-surface-probe assertions |

**Cited input (read, not a manifest action):** `design/specialist-plan-contracts.md` is the single-source per-specialist authoring contract ADR-0050-T2's prompt is built from — read, never modified (listed for the RGC-3 cited-input probe, not the manifest).

**Shared-file coordination:** No file is modified by more than one task. `server.py` (ADR-0050-T1), `client.py` (ADR-0050-T2), and `context_assembler.py` (ADR-0051-T1) are file-disjoint. The two Tier-1 tasks (T1 on `server.py`, T2 on `client.py`) are fully parallel; ADR-0051-T1 (`context_assembler.py`) is Tier-2 (depends on both — see Dependency Map).

## Tasks

### ADR-0050-T1: Wire the real assembler record into front-door authoring
**Status:** TODO
**ADR Source:** ADR-0050, Decision (author each specialist from `assemble_context`'s identity-stripped record, not the `_FixedEnvelopeClient` thin replay); ADR-0050, OQ-1 (the pinned seam — repoint the server pre-author); ADR-0050, Validation Approach (the front-door author call receives the assembled record; reverting the wiring leaves the plan unchanged → RED; identity token in the author payload → FAIL); ADR-0050, Consequences-Negative (wiring regression can silently reintroduce the thin replay; token cost rises; operator-present LIVE run becomes a hard dependency)
**Files to create/modify:**
- `scripts/serve/server.py` -- in `_do_generate_plan` ([:742](../../scripts/serve/server.py)) compute `context_assembler.assemble_context(store_read)` and author the candidate pass ([:832](../../scripts/serve/server.py)) and the Leg-2 rich synthesize ([:860](../../scripts/serve/server.py)) against it; leave `router.summarize` + `active_plan_domains` ([:815-817](../../scripts/serve/server.py)) unchanged
- `tests/serve/test_generate_plan_authoring.py` -- the RED-capable author-input test (spy `self.client`, seeded store, no live SDK)

**Acceptance Criteria:**
1. On the `/generate-plan` front-door path (`_do_generate_plan`), EVERY `self.client.author(domain, <input>)` invocation (the candidate pass at `server.py:832` and the Leg-2 rich author at `server.py:860`) receives `context_assembler.assemble_context(store_read)`'s record: a test driving the front door with a spy `self.client` over a store seeded with the operator's free-text asserts each captured author call's summary argument carries ≥3 of `assemble_context`'s free-text fields (`raw-training-detail-free-text`, `raw-symptom-free-text`, `raw-supplement-free-text`), never `router.summarize`'s ~18-token band.
2. RED-capable / non-tautological: reverting either author-input site to `router.summarize(store_read)` (the thin band) makes AC-1 FAIL — the free-text fields are absent from the captured author call. The test asserts the CLEAN direction (free-text present) truthy first, then RED-gates the mutation: the test is invalid — and fails — if the band-reversion does not RED it.
3. Active-domain selection is unchanged: `plan_loop.active_plan_domains(summary)` (`server.py:816`) still reads the `router.summarize` band (a value distinct from the enriched author input), so the authored-domain set for a fixed fixture store is identical to the pre-change set (a test asserts the two sets are equal).
4. No new author model call: a call-count spy over `self.client.author` records the same number of calls for a fixed fixture store before and after the change (the repoint changes the INPUT of the existing `:832` + `:860` calls, adding no model call — the guard against the `compute_plan(client=)` double-authoring seam OQ-1 rejects).
5. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing (frozen-six byte-frozen — the change lands in `server.py`, outside the six).
6. `$0`: the test uses a spy/fixture model client (no live SDK call, no spend); `pytest tests/serve/test_generate_plan_authoring.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures vs the session baseline).

**Risk Mitigations:** ADR-0050 Consequence-Negative "a wiring regression can silently reintroduce the thin replay" (AC-2, the RED-capable band-reversion guard); "the author prompt grows / operator-present LIVE run becomes a hard dependency" (AC-6 keeps the build at $0; the LIVE run is the recorded Phase-1 exit gate); ADR-0050 identity-strip invariant "no identity token reaches the author payload" (AC-1 authors against `assemble_context`'s `pii_scan`-stripped record — the load-bearing safety invariant, unchanged by the repoint)
**Dependencies:** None (entry point)

---

### ADR-0050-T2: Contract-driven, genetics-aware `_author_system_prompt`
**Status:** TODO
**ADR Source:** ADR-0050, Decision (make `_author_system_prompt` contract-driven — each specialist's `specialist-plan-contracts.md` Inputs/Analysis→plan contract — and genetics-aware, with a directive to personalize off the de-identified record and interpret raw rsID+allele calls); ADR-0050, OQ-2 (the pinned full-per-specialist-contract choice); ADR-0050, Validation Approach (the prompt carries the specialist's contract + the personalize directive); ADR-0050, Consequences-Negative (prompt grows / token cost rises; plan quality depends on contract quality; the genetics-aware prompt must interpret rsID+allele calls); ADR-0051 OQ-5 / Negative-2 (the uncertainty/confidence directive for the un-vetted SNPs)
**Files to create/modify:**
- `scripts/model/client.py` -- rewrite `_author_system_prompt(domain)` ([:510](../../scripts/model/client.py)); add a domain→`specialist-plan-contracts.md`-section map for the 4 renderable domains (workout→§1 personal-trainer, nutrition→§2 nutritionist, supplements→§4 supplement-specialist, peptides→§3 peptide-specialist)
- `tests/model/test_client.py` -- the contract/directive/scoping/strip-REDs assertions for `_author_system_prompt`

**Acceptance Criteria:**
1. For each of the 4 renderable domains, `_author_system_prompt(domain)` contains that specialist's `specialist-plan-contracts.md` contract content: a test asserts that for ≥1 domain a contract-derived substring unique to that section (an Inputs- or Analysis→plan-phrase drawn from `specialist-plan-contracts.md`) is present in `_author_system_prompt(domain)`.
2. The prompt carries a PERSONALIZE + genetics-interpretation directive: it instructs the specialist to personalize off the identity-stripped record and to interpret raw `GENE rsID = (C;C)`-shaped genotype calls, and it describes the input as the identity-stripped FULL record — NOT the pre-rewrite "no raw values" band ([client.py:516-517](../../scripts/model/client.py)). A test asserts the genetics-interpretation directive text is present AND the stale "no raw values" claim is absent.
3. The prompt carries an UNCERTAINTY/CONFIDENCE directive (ADR-0051 OQ-5): it instructs the specialist to flag confidence when interpreting an uncurated genotype from its own knowledge. A test asserts the uncertainty/confidence directive text is present.
4. Per-specialist scoping (OQ-2 full-per-specialist-contract pin): `_author_system_prompt(domain)` for domain X contains a phrase unique to X's contract section AND does NOT contain a phrase unique to a DIFFERENT specialist's section (the prompt is the domain's OWN full contract section, never all 18 specialist sections / never the whole file, never a sub-slice) — a test asserts the include/exclude pair for ≥1 domain-pair.
5. RED-capable / non-tautological: stripping the contract content from the prompt makes AC-1 FAIL; removing the genetics-interpretation or uncertainty directive makes AC-2/AC-3 FAIL. Each assertion is invalid unless its strip REDs it.
6. Single-source invariant (RED-capable against ADR-0050 Alternative C): the per-specialist prompt content is single-sourced from `design/specialist-plan-contracts.md`, not a divergent hand-embedded copy. A test proves it — seed a unique sentinel into domain X's §X contract section (via a fixture contracts source the prompt reads) and assert the sentinel reaches `_author_system_prompt(X)`'s output, so a §X change propagates to the prompt; OR a checked-in drift-guard FAILS when §X changes without the prompt regenerating. RED-capable: an embedded string-literal copy of §X passes the string-presence ACs (AC-1/AC-4/AC-5) but FAILS this one — a static copy does not change when the file changes (exactly the ADR-0050 Alternative-C fork the ADR rejected, and review trigger "`specialist-plan-contracts.md` changes → re-verify the prompt still sources from it"). The test is invalid unless the embedded-copy mutation REDs it.
7. `git diff --numstat 3ab1c3ab -- scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py scripts/plan/router.py` prints nothing; `pytest tests/model/test_client.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures).

**Risk Mitigations:** ADR-0050 Consequence-Negative "plan quality now depends on the quality of the contract content" (AC-1, the contract IS the authoring input); "the prompt grows per specialist / token cost rises" (AC-4, the full-per-specialist scope bounds the payload to the domain's own section; the slice escape hatch is the ADR review trigger); "the genetics-aware prompt must interpret raw rsID+allele calls" (AC-2); ADR-0051 Negative-2 / OQ-5 "the ~105 uncurated SNPs reach the specialist un-vetted" (AC-3, the uncertainty directive); ADR-0050 Alternative C (the rejected off-contract fork) + review trigger "`specialist-plan-contracts.md` changes → re-verify the prompt still sources from it" (AC-6, the single-source invariant — RED-capable against an embedded-copy fork)
**Dependencies:** None (entry point)

---

### ADR-0051-T1: Carry the raw genetic panel to the specialists identity-stripped
**Status:** TODO
**ADR Source:** ADR-0051, Decision (reverse the raw-genotype carve-out: carry the operator's raw `dna-report` genotypes — the FULL stored panel — to the specialists identity-stripped through the assembler's `pii_scan` gate, derived token alongside); ADR-0051, Decision §1 / OQ-3 (the full panel, no sensitive-variant exclusion); ADR-0051, OQ-1 (separate `dna-report`-source read path, keeps `router.py` frozen); ADR-0051, OQ-2 / Negative-5 (scoped genotype-rejection, not blanket-removed); ADR-0051, Validation Approach (identity-leak probe; genotype-rejection-removed probe; frozen-surface probe); ADR-0051, Negative-3 (the `pii_scan` strip must be verified on a genetics payload)
**Files to create/modify:**
- `scripts/plan/context_assembler.py` -- add a separate `dna-report`-source read path (reads `source == "dna-report"` items, keyed `<GENE> <rsID>` with `(X;Y)` values) that carries the FULL raw panel through the reused `pii_scan.scan_operator_value` identity strip; SCOPE the `_RAW_GENOTYPE_PATTERNS` rejection ([:178-187](../../scripts/plan/context_assembler.py)) to exempt ONLY the genetics path; NOT via `_HEALTH_SUBSTANCE_ALLOWLIST` (keeps the partition assert at [:80-84](../../scripts/plan/context_assembler.py) satisfied and `router.py` frozen)
- `tests/plan/test_context_assembler.py` -- the raw-panel/identity-leak/rejection-scoped/derived-token/frozen-surface assertions

**Acceptance Criteria:**
1. The assembled record carries the raw genotypes for the FULL stored panel: seed a store with `dna-report` genotypes across the stored SNPs (including APOE/DRD2/BDNF — no sensitive-variant exclusion, OQ-3), call the assembler, and assert `(X;Y)`-shaped allele-call values keyed `<GENE> <rsID>` are present in the assembled record for every seeded SNP; threshold ≥ the seeded-genotype count reaches the record, 0 silently dropped.
2. IDENTITY-leak probe (fail-closed RAISE): seed a synthetic operator legal name (or DOB/contact) INTO a `dna-report` genetics field, run the assembler, and assert it RAISES (fail-closed) — the reused `pii_scan.scan_operator_value` identity-strip holds on the genetics path exactly as on the other carries ([context_assembler.py:188-193](../../scripts/plan/context_assembler.py)), so a seeded identity token never crosses. Binary + RED-capable: dropping the `pii_scan` scan on the genetics read path lets the seeded name cross WITHOUT raising (RED); the test is invalid unless that mutation REDs it.
3. Genotype-rejection SCOPED (not blanket-removed): a genotype smuggled into a NON-genetics carry (`raw-nutrition-free-text`) STILL fails closed — the assembler RAISES the `_RAW_GENOTYPE_PATTERNS` rejection ([context_assembler.py:178-187](../../scripts/plan/context_assembler.py)) — RED if a smuggled non-genetics genotype crosses; AND the genetics read path completes WITHOUT that raise for a real `(C;C)` genotype (the exemption is scoped to the genetics path only).
4. FROZEN-SURFACE probe: `git diff --numstat 3ab1c3ab -- scripts/plan/router.py scripts/store/store.py scripts/store/keying.py scripts/plan/pipeline.py scripts/plan/adjudicate.py scripts/plan/adjust.py` prints nothing (the carry used a separate `dna-report`-source read path, so the partition assert did not force a `router.EXCLUDED_RAW_PII` edit) — RED if `router.py` or any frozen-six file changed.
5. The derived `genetic-trait-classes` token STILL crosses alongside the raw (additive, not a replacement): a test asserts the assembled record carries BOTH the raw genotypes AND the derived `genetic-trait-classes` token ([router.py:59,178](../../scripts/plan/router.py) field-name literal / [:305](../../scripts/plan/router.py) token-value deriver) — the raw carry does not displace the summary layer.
6. `$0`: fixture/synthetic genotypes only (no live spend); `pytest tests/plan/test_context_assembler.py -q` passes and `.venv/bin/python -m pytest -q` stays green (0 NEW failures).

**Risk Mitigations:** ADR-0051 Consequence-Negative-3 "the `pii_scan` identity strip must be VERIFIED on a raw genetics payload" (AC-2, the identity-leak probe); Negative-5 "the assembler genotype-rejection must be SCOPED, not blanket-removed" (AC-3); Negative-6 / OQ-1 "mechanism constraint to keep `router.py` frozen" (AC-4, the frozen-surface probe + the separate-read-path mechanism); ADR-0051 Neutral "the derived token persists as the summary layer" (AC-5); ADR-0051 Negative-1 (re-identification exposure) and Negative-2 (un-vetted read) are non-falsifiable / prompt-side residuals — documented assumptions per the Unresolved Concerns table, not build ACs (Negative-2 is bounded by ADR-0050-T2 AC-3)
**Dependencies:** ADR-0050-T1, ADR-0050-T2

---

## Dependency Map

```
ADR-0050-T1 --> ADR-0051-T1
ADR-0050-T2 --> ADR-0051-T1
```

**Data flow per edge:**
- `ADR-0050-T1 --> ADR-0051-T1`: an integration/usability edge (per the ADR-0051 `depends-on ADR-0050` relationship, operator-signed-off Tier-2). ADR-0050-T1 makes the assembled record reach the model author (repoints the author input to `assemble_context`); until it lands, ADR-0051-T1's raw genotypes are carried but never reach the model. ADR-0051-T1's unit tests exercise `assemble_context`'s RETURN value directly (runnable in isolation), but the feature's end-to-end value requires T1 — the edge is a real feature-integration ordering constraint, not a compile-time import.
- `ADR-0050-T2 --> ADR-0051-T1`: an integration/usability edge. ADR-0050-T2's genetics-interpretation directive is what makes ADR-0051-T1's raw `GENE rsID = (C;C)` calls interpretable by the specialist (ADR-0051 Negative-4: "if the ADR-0050 authoring prompt cannot read genotype calls, the raw signal is carried but unused"). Until T2 lands, the raw genotypes are carried but uninterpreted.

**Topological order (Kahn's; parallel groups):**
1. `ADR-0050-T1`, `ADR-0050-T2` (parallel — entry points, no dependencies; file-disjoint: `server.py` vs `client.py`)
2. `ADR-0051-T1` (after both `ADR-0050-T1` and `ADR-0050-T2`)

**Entry points:** `ADR-0050-T1`, `ADR-0050-T2`
**Critical path:** `ADR-0050-T1 → ADR-0051-T1` (equal-length: `ADR-0050-T2 → ADR-0051-T1`); 2 tasks. Acyclic — all 3 nodes ordered by Kahn's with none remaining.

## Constraint Propagation

Cross-cutting constraints from the ADRs and their enforcing acceptance criteria (each is a falsifiable AC, not prose):

| Constraint | Source | Enforced in | Enforcing AC |
|-----------|--------|-------------|--------------|
| Frozen ADR-0032 six numstat == 0 vs `3ab1c3ab` (`store.py`, `keying.py`, `pipeline.py`, `adjudicate.py`, `adjust.py`, `router.py`) | ADR-0050 Related Decisions + ADR-0051 Validation (frozen-surface probe) | ADR-0050-T1, ADR-0050-T2, ADR-0051-T1 | the `git diff --numstat 3ab1c3ab -- <six>` prints-nothing AC in each (ADR-0050-T1 AC-5, ADR-0050-T2 AC-6, ADR-0051-T1 AC-4) |
| Identity-strip invariant: no name/DOB/contact/health-identifier reaches the model (via `pii_scan`) | ADR-0050 Decision + Validation (identity-strip falsification); ADR-0051 Decision §3 + Validation (identity-leak probe) | ADR-0050-T1, ADR-0051-T1 | ADR-0050-T1 AC-1 (author reads `assemble_context`'s `pii_scan`-stripped record); ADR-0051-T1 AC-2 (identity-leak probe on the genetics carry) |
| `router.py` frozen — genetics carry uses a separate `dna-report`-source read path, not the allowlist | ADR-0051 OQ-1 + Decision (mechanism to keep `router.py` untouched) | ADR-0051-T1 | AC-4 (frozen-surface probe: `router.py` numstat == 0) |
| Genotype-rejection stays fail-closed on every non-genetics carry (scoped exemption, not blanket removal) | ADR-0051 OQ-2 + Negative-5 | ADR-0051-T1 | AC-3 (a non-genetics genotype still raises; only the genetics path is exempt) |
| Genetics-aware prompt must interpret raw rsID+allele calls (else the raw signal is carried but unused) | ADR-0050 Negative-5 + ADR-0051 Negative-4 | ADR-0050-T2 | AC-2 (the genotype-interpretation directive present) |
| Un-vetted read bounded by an uncertainty directive (the ~105 uncurated SNPs) | ADR-0051 OQ-5 + Negative-2 + ADR-0009 tension | ADR-0050-T2 | AC-3 (the uncertainty/confidence directive present) |
| `$0` build until the operator-present run (synthetic/mock fixtures, PUBLIC repo) | ADR-0050 OQ-3 + ADR-0051 OQ-4 (LIVE run operator-gated, out of build scope) | ADR-0050-T1, ADR-0050-T2, ADR-0051-T1 | ADR-0050-T1 AC-6 (spy client, no spend); ADR-0050-T2 AC-6; ADR-0051-T1 AC-6 (synthetic genotypes) |

## Test Strategy

### Unit Tests
- **Scope:** `scripts/model/client.py` (`_author_system_prompt` — ADR-0050-T2), `scripts/plan/context_assembler.py` (the genetics read path — ADR-0051-T1).
- **Approach:** pytest; `_author_system_prompt(domain)` asserted as a pure string function (no model call); the assembler driven with a synthetic `store_read` fixture seeding `dna-report` genotypes + free-text fields. No network, no live SDK, no real genome.
- **Criteria covered:** ADR-0050-T2 AC-1..6; ADR-0051-T1 AC-1, AC-3, AC-5.

### Integration Tests
- **Scope:** the front-door `_do_generate_plan` authoring path (`router.summarize` selection + `assemble_context` author input + the `generate_plans`→`compute_plan` replay) — ADR-0050-T1; the assembler's identity-leak probe across a full specialist payload — ADR-0051-T1.
- **Approach:** in-process `_do_generate_plan` driven with a spy/fixture `self.client` (captures each `author(domain, summary)` call's args + call count) over a seeded store on the single-operator instance root; the assembler run end-to-end over a store seeding identity strings into a `dna-report` field.
- **Criteria covered:** ADR-0050-T1 AC-1, AC-3, AC-4; ADR-0051-T1 AC-2.

### Risk-Specific Tests
- **Scope:** the wiring-regression guard (ADR-0050-T1 AC-2, the band-reversion RED), the prompt-strip guards (ADR-0050-T2 AC-5), the single-source-invariant guard (ADR-0050-T2 AC-6, RED against the Alternative-C embedded-copy fork), the identity-leak probe (ADR-0051-T1 AC-2), the genotype-rejection-scoped guard (ADR-0051-T1 AC-3), the frozen-six / frozen-surface numstat probes (all three tasks), and the no-new-model-call cost guard (ADR-0050-T1 AC-4).
- **Approach:** each ruling is mutation-gated — the test asserts the CLEAN direction truthy first, then a planted violation (reverting the author input to `router.summarize`; stripping the contract/directive from the prompt; embedding a static copy of a contract section in place of the runtime source; smuggling a genotype into a non-genetics carry; smuggling identity into a `dna-report` field) must flip it RED, so the test cannot be built green-always.
- **Criteria covered:** ADR-0050-T1 AC-2, AC-4, AC-5; ADR-0050-T2 AC-5, AC-6; ADR-0051-T1 AC-2, AC-3, AC-4.

**Self-verifying ACs (covered by execution, not a separate test asset):** each task's terminal `pytest …` AC is the run itself — ADR-0050-T1 AC-6, ADR-0050-T2 AC-7, ADR-0051-T1 AC-6. With these, every acceptance criterion maps to a test or a verification command.

### Operator-Present Exit Gates (out of build scope, `$0`-until-run)
These are the load-bearing NON-mock verifications (ADR-0050 OQ-3, ADR-0051 OQ-4). Every build AC above is mock/fixture-satisfiable at $0; only the operator-present run confirms real quality. Recorded here, teed up in the HANDOFF — NOT build tasks.
- **Phase-1 exit gate (after ADR-0050-T1 + ADR-0050-T2 land):** the operator runs `/generate-plan` on their REAL data through the web app and confirms the plan reflects their actual program / symptoms / trait-classes (NOT a generic template) — resolves ADR-0050 OQ-3. Threshold: ≥1 operator-specific detail per active domain that the coarse band would have erased; a plan expressible from the band alone fails.
- **Phase-2 exit gate (after ADR-0051-T1 lands):** the operator re-runs `/generate-plan`; the plan cites operator-specific raw genetic detail — a recommendation grounded in a raw genotype the derived 8-class token would not have carried — resolves ADR-0051 OQ-4. This is the first time the real genome egresses to the no-train API (operator-gated).

## Repo-Grounding Ledger

Grounded against the live worktree on `feature/plan-personalization-spec` (Phase-4 author RGC probes; the Phase-6 judge re-runs all four independently). Frozen-six numstat vs `3ab1c3ab` verified EMPTY at author time.

| Task | RGC-1 (manifest) | RGC-2 (premise) | RGC-3 (cited input) | RGC-4 (dup) | Disposition |
|------|------------------|-----------------|---------------------|-------------|-------------|
| ADR-0050-T1 | pass (`server.py` present → Modify; `tests/serve/test_generate_plan_authoring.py` absent → Create) | pass (`_do_generate_plan`@742, `router.summarize`@815, `active_plan_domains`@816, candidate author@832, `generate_plans`@843, Leg-2 `_author_rich`@860 all confirmed; `compute_plan` computes then discards `assemble_context`@560/566 confirmed) | pass (`context_assembler.assemble_context`@109 is a strict superset of `router.summarize`, base = `dict(router.summarize(...))`@145-147, so `active_plan_domains` compatibility holds under the pin; `normalize_author_output`@intake_aggregate.py:224) | pass (no existing front-door author-input repoint; the `client=` compute_plan seam exists@503 but OQ-1 rejects it for double-authoring) | Grounded |
| ADR-0050-T2 | pass (`client.py` present → Modify; `test_client.py` present → Modify [0 `_author_system_prompt` refs today]) | pass (`_author_system_prompt`@510 is the generic scaffold, "no names, no raw values"@516-517, `_AUTHOR_SPECIALIST`@487, `author`@749 sends `json.dumps(summary)`@773, `MODEL="claude-opus-4-8"`@687) | pass (`design/specialist-plan-contracts.md` = 494 lines, §1-4 = personal-trainer/nutritionist/peptide-specialist/supplement-specialist mapping the 4 renderable domains; each § has Inputs/Monitoring/Tracking/Analysis→plan) | pass (no contract-driven prompt exists; the current prompt carries none of the contract) | Grounded |
| ADR-0051-T1 | pass (`context_assembler.py` present → Modify; `test_context_assembler.py` present → Modify [25 genotype/dna-report/scan_operator refs today]) | pass (`_HEALTH_SUBSTANCE_ALLOWLIST`@54-65 [no `dna-report`], partition assert@80-84 [would force `router.EXCLUDED_RAW_PII` edit if genetics went on the allowlist], `assemble_context`@109, genotype-rejection@178-187 uses `router._RAW_GENOTYPE_PATTERNS`@192, `dna-report` carve-out@28-31) | pass (store holds ~117 `dna-report` items keyed `<GENE> <rsID>` with `(X;Y)` values incl. APOE/DRD2/BDNF; `pii_scan.scan_operator_value`@188 the reused gate; `genetic-trait-classes` token — field-name literal@router.py:59,178 / deriver@router.py:305) | pass (no `dna-report`-source read path in the assembler today; the carve-out is active — the genetics carry is a NEW path, no duplicate) | Grounded |

## Validation Checklist

### Traceability
- [x] Every task has a non-empty ADR Source field citing a specific ADR section
- [x] Every ADR ID in the `adrs` frontmatter field has at least one task (ADR-0050: T1–T2; ADR-0051: T1)
- [x] All ADR IDs resolve to actual ADR files on disk (`docs/adr/ADR-0050-…md`, `docs/adr/ADR-0051-…md` read in full)

### Acceptance Criteria Quality
- [x] Every task has at least one acceptance criterion (ADR-0050-T1: 6, ADR-0050-T2: 7, ADR-0051-T1: 6)
- [x] All acceptance criteria are binary (a command/condition with a pass/fail outcome)
- [x] No criterion uses "appropriate", "reasonable", "adequate", "properly", "correctly", "robust", "efficient"

### File Manifest Integrity
- [x] Every task has a file manifest
- [x] Every file in any task block appears in the top-level File Manifest
- [x] Every file in the top-level File Manifest appears in at least one task block
- [x] No task lists a directory instead of a specific file

### Dependency Map Integrity
- [x] Dependency map has no cycles (Kahn's orders all 3 nodes; none remain)
- [x] Every task ID in any Dependencies field appears as a node in the Dependency Map
- [x] Every edge in the Dependency Map corresponds to a Dependencies entry in a task block
- [x] Entry points are listed (ADR-0050-T1, ADR-0050-T2) and have Dependencies: "None (entry point)"

### Constraint Propagation
- [x] Constrained ADR tasks reflect upstream ADR constraints in their acceptance criteria (frozen-six, identity-strip, router.py-frozen, scoped-rejection, genotype-interpretation, uncertainty, $0 — see Constraint Propagation table)
- [x] Constraint Propagation Table entries have corresponding acceptance criteria in affected tasks

### Unresolved Concerns
- [x] Unresolved Concerns Disposition section is present
- [x] Every open question / pending tension / unmitigated risk has a disposition (Proceed / Resolved; no Block applies)
- [x] Block dispositions have corresponding research spike tasks (none — no Block dispositions)
- [x] Defer dispositions have justifications (none — the LIVE-run OQs are Proceed with the recorded operator-present exit gates; the two non-falsifiable residuals are operator-accepted documented assumptions)

### Risk Coverage
- [x] Risk Mitigations field present on every task
- [x] Every negative consequence in in-scope ADRs is covered by at least one task's Risk Mitigations or a documented assumption (ADR-0050: 5/5 — token-cost→T2 AC-4, contract-quality→T2 AC-1, LIVE-run-dependency→Phase-1 gate, wiring-regression→T1 AC-2, genetics-interpretation→T2 AC-2; ADR-0051: 6/6 — re-identification→documented assumption, un-vetted→T2 AC-3, pii_scan-verified→T1 AC-2, prompt-interprets→T2 AC-2, scoped-rejection→T1 AC-3, router.py-frozen→T1 AC-4)

### Test Coverage
- [x] Every acceptance criterion appears in at least one Test Strategy category
- [x] Risk-specific tests exist for every mitigated risk (the band-reversion guard, the prompt-strip guards, the identity-leak probe, the genotype-rejection-scoped guard, the frozen-six/frozen-surface probes, the no-new-model-call guard, the single-source-invariant guard)

### Downstream Readiness
- [x] Frontmatter has all required fields (scope, adrs, tier, created, status)
- [x] All section headers match the template (Component Overview → Unresolved Concerns → File Manifest → Tasks → Dependency Map → Test Strategy → Validation Checklist, plus Constraint Propagation + Repo-Grounding Ledger)
- [x] No placeholder text ("TBD", "TODO: fill in", "...")

### Live-Repo Grounding
- [x] Every File Manifest `Modify` row names a path that exists in the current worktree (`server.py`, `client.py`, `context_assembler.py`, `test_client.py`, `test_context_assembler.py` all present)
- [x] Every File Manifest `Create` row names a path that does NOT already exist (`tests/serve/test_generate_plan_authoring.py` confirmed absent)
- [x] Every ADR premise a task relies on was re-verified against the current repo (all seams confirmed at the cited lines; no stale premise)
- [x] Every cited input a task reads declares its structural assumption AND the live file satisfies it (`assemble_context` superset of `summarize`; `specialist-plan-contracts.md` §1-4; ~117 `dna-report` `(X;Y)` genotypes; the partition assert; `_RAW_GENOTYPE_PATTERNS`)
- [x] No task proposes a new artifact that duplicates an existing repo capability (no front-door author-input repoint, no contract-driven prompt, no `dna-report` assembler read path exists today)
- [x] Repo-Grounding Ledger present, one row per task, with a disposition (3 Grounded)
