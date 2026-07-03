# Design Plan — Dynamic, Personalized, Time-Horizon Plan Loop (v2, post-review)

Status: VETTED (6-agent adversarial review complete; findings verified + resolved below). Ready for ADR.
Verification mandate (operator, hard): every claim + every build step is EMPIRICALLY verified (executed
with an assertion), never asserted from reading code.

## 0. What changed from v1 (the review verdicts)

Six adversarial reviewers (failure-modes, crown-jewel, contracts, architecture, verifiability,
prior-decisions) critiqued v1. Each finding below carries a VERDICT (I verified the load-bearing ones
against the live tree; I did not just accept them).

| # | Finding | Verdict | Design change |
|---|---|---|---|
| A | The automated re-adjust path (`adjust.py`, per-domain) skips `plan_driver.drive`→`gate_dispatch` (ADR-0023 judge + ADR-0024 safety lenses + ADR-0028 fail-closed + liaison adjudication) AND the 5 cross-domain holds. `adjust.py` is a *rare operator one-off*; automating it makes every plan after week 1 never see the safety composition again. | **CONFIRMED** (verified: `adjust.py` calls single-domain `generate_plan` only) | **The automated loop RE-RUNS THE FRONT DOOR** (`plan_driver.drive`/`run_orchestrated`) on trigger — not `adjust.py`. Every evolved plan gets the same safety composition as the first. `adjust.py` stays the manual one-off. |
| B | The "money shot" can't run: the adjust leg reads `plan-track::` (operator-LOGGED adherence, same-date), but wearables land in the separate `biomarker::` trend namespace → `has_tracking=False` → no-op. | **CONFIRMED** | Re-running the driver **re-summarizes the store**, which already reads `biomarker::` → `recent-trend-direction`. So the wearable trend reaches the re-generation *for free* via the summary — no bridge to `plan-track::` needed. Adherence (`plan-track::`) is a *separate, additional* input. |
| C | Free-text trigger (e.g. "my shoulder's flaring and I changed a dose this week") is RAW; nothing stops it reaching the de-id specialist lane. `adjust.py` doesn't de-identify — it's a recorder. | **CONFIRMED** | The trigger routes **only through the care agent's existing gated capture** (`persist_capture` → derived tokens: `recovery-status-band`, `active-issue-class`) → the store → `summarize` (whitelist) → re-generation. The raw free-text is **structurally incapable** of reaching the specialist dispatch (it never leaves the care lane / the store's de-id derivation). |
| D | Tailoring is an ungated raw model call; "not an authoring authority" + "safety-floor" are prose with no mechanism. Can shadow-prescribe a HELD domain / dose investigational compounds. | **CONFIRMED** | Tailoring gets **mechanical gates in code**: (1) emits for a domain ONLY when `plan::<domain>` exists AND was not in any hold set; (2) a dosing-token reject on tailoring output for compound domains; (3) the raw drug×supp×peptide screen is a **deterministic rule** that **fails CLOSED** (surfaces "see your doctor", never silently drops) — separate from the presentation model call. |
| E | `plan-tailor::` as a NEW **store stream** is forbidden by ADR-0021/0001/0005 (store + tracked renders stay de-identified; raw PII → the gitignored artifact only). | **CONFIRMED** | Tailoring renders **only into the gitignored `maintained` artifact** (ADR-0025, name-reinserted, realpath-guarded), **never** a store stream and **never** the de-identified dashboard. A load-time tripwire asserts no tailoring key is a `SUMMARY_FIELD_SET` member. |
| F | The tailoring pass is a NEW named raw-egress purpose; v1 waved it through as "the care lane already exists." Every raw egress here is a separately ADR-named, operator-signed-off carve-out (the ADR-0001 egress siblings: ADR-0016 intake-conversation, ADR-0032 de-associated-variant, ADR-0035 de-associated-meds). | **CONFIRMED** | The ADR names the tailoring egress as its own carve-out and amends ADR-0001's egress list, per the established discipline. (Note: ADR-0034 is the curated-rx-interaction-classes DATA SOURCE the screen builds on — a depends-on, NOT an egress sibling.) |
| G | Horizons: `plan_schema` is NOT "frozen flat" — ADR-0010 D2 is "closed on required, **open on extras**." AND `goal_schema` (baseline/current/target → derived progress %) + `calendar_schema` (dated cadences: lab-draw/check-in) already own milestones + cadences. AND peptides is NOT a `TRACKED_DOMAIN` (ADR-0010 D3). | **CONFIRMED** (verified all three) | Horizons **compose over** `goal_schema` (milestones/progress) + `calendar_schema` (cadences) + the **ADR-0010 extension seam** (enrich plan values via extras) — NO new `plan-arc::` stream reinventing them. Peptide "cadence" drops (it has no tracking); peptides ride the existing watch-out stream. |
| H | Verification was tautological ("plan changed" when the fixture SCRIPTED the change); relied on a live-probe harness that doesn't exist in the 0-spend suite; tested modules directly instead of the serve entry point (re-encoding the unwired state as green — PF-S63-02); had NO crown-jewel non-egress test. | **CONFIRMED** | Rewritten §6: paired **mutation controls** (behind→de-load AND on-track→NOT de-load); tests drive the **serve entry point**; a **wire-scan non-egress** test; deterministic loop mechanics pinned in CI with fixtures; reasoning-quality is a **PR-documented manual live dispatch**, never a CI assertion (the `test_adjust.py` convention). |
| I | Phasing inverted: tailoring isn't standalone (the loop re-runs it; the evaluation needs horizons); the cheap/safe first move is wiring the built measure/read legs. | **CONFIRMED** | Re-sequenced (see §9): wire the loop (safe, reuses the driver) → horizons → tailoring last (highest-risk, raw egress). |
| J | (prior-decisions) The re-emit automation increases exposure through the ADR-0021/0025 **OQ-1** name-scan hole (`vault/artifacts/generated/` outside the PII name scan). | **OUTDATED** | Verified: `vault/artifacts/generated/` **IS** in `DATA_BEARING_PREFIXES` now — the gross hole is closed. Residual: confirm the scan detects the reinserted *name* (not only contact tokens); a minor pre-ship check, not a gating blocker. |

Root cause of A–F (all six reviewers converged): v1 treated the crown-jewel as a single "specialists never
see raw" sentence, then relaxed the clauses it didn't quote (the `gate_dispatch` composition; the
de-identified store/render; the named-egress carve-out discipline). The design now enumerates the boundary
as that full **set** and stress-tests every new surface against each clause.

## 1. Goal (unchanged)

The care agent personalizes the plan with the operator's raw data; the plan spans daily/weekly/monthly
horizons and evolves toward goals; it dynamically re-adjusts as new data arrives — **without ever routing a
plan around the safety composition or raw data around the de-id boundary.**

## 2. Revised design

### The loop (dynamic adjustment) — RE-RUN THE FRONT DOOR

- **Trigger** = cadence (weekly) + data-event (new labs/wearables mirrored to `biomarker::`) + free-text via
  the care agent (which captures derived tokens through the existing gate). All converge on ONE action:
  **re-run the front-door generation** (`plan_driver.drive`/`run_orchestrated`) against the current store
  state, producing a NEW dated plan that passed the **full** `gate_dispatch` composition + cross-domain holds.
- **Why re-run the driver, not `adjust.py`:** safety parity (finding A) + it re-summarizes the store, so the
  wearable trend (`biomarker::`→`recent-trend-direction`) and the goal progress (`goal_schema`) reach the
  re-generation for free (finding B). `adjust.py`/`track.py` remain the manual measure/one-off surface.
- **Debounce (mechanical, in code, on ALL triggers incl. free-text):** a minimum re-generation interval +
  a sustained-signal requirement (a window/threshold over the `biomarker::` series, not a single reading);
  a second trigger inside the window is dropped. Free-text is rate-limited too (finding, security F7).
- **Absent-data:** no new signal in the window → hold + prompt to log; never re-generate on nothing.
- **Rationale + control:** each re-generation records a plain-language "what changed and why"; large changes
  surface for confirmation rather than silent swap.
- **Multi-domain coherence:** re-running the driver regenerates ALL domains on the new date (finding, contracts
  F3 — day-keying blanks non-adjusted domains otherwise), and re-runs cross-domain reconciliation. No
  per-domain fan-out that skips holds.

### Horizons — compose, don't reinvent

- Milestones + progress: **`goal_schema`** (`{label, baseline, current, target}` → derived %).
- Cadences / dated events (lab recheck, check-in): **`calendar_schema`** (`calendar::events`).
- Weekly/monthly framing: **ADR-0010 extras seam** — enrich the existing dated `plan::<domain>` values with
  phase/week-intent (no new stream); the "this week's block / month arc" is a **date-range query over the
  dated plan history**, not a second stored schedule (finding, code-quality F7).
- Peptides: NOT a tracked domain (ADR-0010 D3) — no peptide cadence/tracking; rides the watch-out stream.
- Open-ended goals (longevity): no deadline → rolling maintenance cycles (graceful degradation).

### Tailoring — the operator's core ask, as a gated named egress

- **Placement:** after the driver records the de-id `plan::<domain>`, a care-lane pass personalizes for the
  operator, rendered **only** into the gitignored `maintained` artifact.
- **Named egress:** the ADR names it + amends ADR-0001's carve-out list (finding F).
- **Mechanical floor (code, not prompt):** emits for a domain ONLY when `plan::<domain>` exists AND not held;
  a dosing-token reject for compound domains; the raw drug×supp×peptide screen is a **deterministic rule**
  built ON ADR-0034's curated `rx-interaction-classes` + the existing BPMH/additive-AE lenses, and **fails
  closed** ("see your doctor").
- **Fail-safe (split):** presentation failure → degrade to the un-tailored (safe, de-id) plan. The safety
  screen does NOT ride the presentation model call and does NOT fail open.
- **Store/render:** never a de-id store stream (ADR-0021); never the de-id dashboard; tripwire that no
  tailoring key is a `SUMMARY_FIELD_SET` member.

## 3. Crown-jewel boundary = the FULL set (stress-tested against each)

(1) Every operator-held plan passed `gate_dispatch` → the loop re-enters the driver. (2) Store + tracked
renders stay de-identified → tailoring is artifact-only. (3) Specialists get only `summarize` field-set
tokens → the trigger routes only derived tokens; raw text can't reach the specialist dispatch. (4) Each raw
egress is a named ADR carve-out → tailoring is named. (5) The `maintained` artifact is name-reinserted under
the realpath guard → the automated re-emit reuses `reemit_maintained`, never a second writer.

## 4. Verification (empirical; CI-deterministic + mutation controls; reasoning = PR-documented live dispatch)

- **Loop fired through the SERVE entry point** (not the module directly): a wearable/free-text signal ingested
  at the real route CAUSES a new dated plan. NEGATIVE: absent the serve trigger, no re-gen (catches unwired).
- **Mutation controls:** behind-signal → de-load branch AND on-track/ahead → NOT de-load (falsifiable pair).
- **Debounce:** sustained week → fires; single reading → does NOT (paired); a unit test of the
  threshold/window function (deterministic).
- **Crown-jewel non-egress:** seed raw identifiers + raw meds, fire the loop, dump the specialist-lane payload,
  assert the raw tokens are ABSENT (wire-scan, per `test_care_chat` pattern).
- **Safety floor on re-gen:** a held domain stays held; clearance re-derived per re-gen (not inherited).
- **Tailoring:** personalized output asserted; held domain NOT emitted; dosing-token rejected; interaction
  screen fires on a known combo AND does NOT on a safe combo (deterministic rule); fail-closed on model error.
- **Reasoning quality** (clinical appropriateness of the de-load; tailoring prose) = a **manual live dispatch
  documented in the PR**, never a CI test (the 0-spend suite has no live-probe harness; `test_adjust.py`
  convention). If a live-probe harness is wanted, it is its own beaded build task.

## 5. Build sequencing (re-sequenced per finding I)

1. **Wire the loop:** trigger → re-run driver (reusing the built front door + reconciliation + gate) + debounce
   + rationale, driven from the serve layer. Reuses the measure leg (`record_tracking`) for adherence input.
   Cheapest, safest, no new raw egress. Realizes the "dynamic adjustment" against the existing safe machinery.
2. **Horizons:** compose over `goal_schema` + `calendar_schema` + the ADR-0010 extras seam; date-range views.
3. **Tailoring (last):** the raw-egress carve-out, artifact-only, mechanically gated + fail-closed screen.

## 6. ADR necessity: YES (confirmed by review)

Multiple crown-jewel/safety decisions: the loop re-enters the driver (safety-composition parity); tailoring
as a named raw egress amending ADR-0001; artifact-only rendering (ADR-0021); the deterministic fail-closed
interaction screen; debounce policy; horizons composing over `goal_schema`/`calendar_schema` + the ADR-0010
seam. Pipeline: **ADR → Spec → Build Plan → Task Plan → Execute Plan**. The ADR cites: `plan_driver.py`,
`gate_dispatch.py`, `orchestrate.py`, `adjust.py`, `track.py`, `plan_schema.py`, `goal_schema.py`,
`calendar_schema.py`, `store.py`, `maintained.py`, `care_chat.py`, `capture.py`, `router.py`, and
ADR-0001/0010/0016/0021/0023/0024/0025/0026/0028/0034/0035.
