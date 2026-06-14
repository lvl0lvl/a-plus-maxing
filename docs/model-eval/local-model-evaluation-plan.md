---
title: Local Model Evaluation Plan
type: plan
owner: Walter McGivney
created: 2026-06-14
last_reviewed: 2026-06-14
status: active
depends_on: [ADR-0001, ADR-0006]
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/model-eval/local-model-evaluation-plan
---

# Local Model Evaluation Plan

The executable plan for choosing (or training) the **local model that would run the
PII-sensitive personalization on-device**. The accepted V1 boundary (ADR-0001) currently
routes that work to a *no-train, non-retained commercial Anthropic API over summaries* —
so moving it on-device is a **proposed supersession of ADR-0001's plan-reasoning routing**
(see §1), driven by the operator's direction to take the off-cloud PII work local. The
Claude subscription keeps the goal-agnostic rest (the `/aplus-research` wiki research,
orchestration, the build). This plan decides *which local model*, on *what hardware*, at
*what quality and safety*, and how it slots in — its result is the evidence for that ADR.

> **Audience:** a future session that runs this eval end-to-end and reports a
> recommendation. Read it in full before starting. It is a *plan*, not the eval
> itself — it defines the candidates, the test, the scoring, the run-it checks, and
> the decision rule.

---

## 0. How to use this document

1. Read §1 to lock the architecture the model serves (what is local vs Claude).
2. Resolve the §7 operator inputs first — especially **hardware specs** (gates the
   run-it eval) and the **gold-standard source** (defines "correct"). The eval can't
   score without them.
3. Build the minimal harness (§5), assemble the task set + the gold standard, run the
   candidates (§3) through the two-axis eval (§4), score against the rubric (§5),
   apply the decision rule (§6), and report a recommendation.
4. Screen the small/weak candidates fast (cheap fail-out); deep-eval only the survivors.

---

## 1. Premises — what the local model is FOR, and what it supersedes

**This supersedes ADR-0001's PII routing — it is not an open gap.** The PII trust
boundary is an *accepted* decision. **ADR-0001** (threat-model B) routes the PII-touching
plan reasoning to a **no-train, non-retained commercial Anthropic API over summaries**
(not raw PII), with the store / ingestion / generation all local; **ADR-0006** routes the
specialist plan-assembly on that same no-train-over-summaries lane. ADR-0001 **explicitly
evaluated and REJECTED "Alternative C: fully-local model" for V1** (it "sacrifices V1
capability," and reversing to local later "would force re-plumbing every data path") —
recording a revisit trigger: *"if local open-weight models reach parity for clinical-
reasoning tasks AND hardware cost is acceptable."* The bead `hil` (*"use operator PII
without sending it to Anthropic"*) is **CLOSED**, resolved by that ADR-0001 boundary.

So this plan does not fill an open gap — it is the **evidence-gathering for a proposed
supersession of ADR-0001's plan-reasoning routing**, exercising ADR-0001's own
Alternative-C revisit trigger, driven by the operator's direction to move the off-cloud
PII work to a local model. Its result is ADR-worthy: a recommendation here **supersedes
ADR-0001** (and re-validates ADR-0006's constraint) for the personalization layer, and
must account for the re-plumbing cost ADR-0001 flagged.

**The split being evaluated:**
- **Local model** → the **personalized** layer: the operator's context + the goal-agnostic
  wiki (via RAG) + a specialist role → a personalized **diagnostic + plan**, on-device.
  *Today this lane runs on the no-train commercial API over summaries (ADR-0001/0006); a
  local substrate is what would move it on-device — and could lift the summaries-not-raw
  constraint, a benefit to weigh.*
- **Claude subscription** → the **goal-agnostic** rest: `/aplus-research` wiki research
  (no operator PII — goal-agnostic by design), orchestration, the build, this kind of doc.

**The model is NOT autonomous — and its runtime output is gated by the specialist rules,
NOT by `medical-safety-reviewer`.** A correction to pin for the executor:
`medical-safety-reviewer` is a **pre-deployment gate** over `agent.md` profiles / wiki
entries (it emits DEPLOY/BLOCK) — it does NOT review per-dispatch plan output. The
**runtime** safety surfaces the model's output actually feeds are: the specialist agents'
own HALT / refusal rules (the compound-write HALT on unpopulated hard-limit fields; medium+
compounds blocked pre-MD by the operator-profile rule), the `medical-liaison` doctor-visit
queue + HIGH/MEDIUM adjudication, and the operator + doctor as human-in-the-loop. The bar is
**"good enough to draft recommendations that those runtime gates + the operator + the doctor
vet"** — not autonomous medical authority. (Distinct, secondary: `medical-safety-reviewer`
*could* gate the local model itself as a deployed component, profile-level.)

**It has the library (RAG).** The model reads the wiki at inference, so it does not
need to *memorize* the compound/biomarker corpus. **But medical facts still matter and
are weighted** (§4): the underlying medical grounding is what lets the model (a) catch a
wrong or contradictory wiki entry rather than parrot it, (b) reason soundly about a case
the wiki doesn't cover, and (c) not hallucinate a dose or a contraindication over the
operator's data. Facts *and* reasoning, both scored.

---

## 2. The job to evaluate — the actual task

The eval measures the model on the **specialist personalization task** it will run:

```
INPUT:  operator context — TODAY summaries (ADR-0001/0006 route plan-reasoning over
        SUMMARIES, not raw PII; the as-built specialist profiles "author the read
        instruction, never the content"); a local on-device substrate is what could
        admit richer/raw operator context — the proposed change to weigh
      + the relevant wiki entries (RAG: compounds / biomarkers / library)
      + a specialist role frame (e.g. peptide-specialist, labs-specialist)
TASK:   produce a personalized assessment + plan —
        - interpret the operator's data against the wiki evidence,
        - respect contraindications, the HALT rules, and the goal/limit anchors,
        - cite the wiki entry it grounds each recommendation in,
        - HALT / escalate to the doctor-visit queue where the rules require.
OUTPUT: a diagnostic + plan the runtime gates + operator + doctor then vet.
```

This is the specialist plan-reasoning task the deployed `agent.md` profiles run — TODAY on
the no-train commercial API over summaries (ADR-0006). The eval tests whether a local model
can take that lane acceptably (and whether it can do so over richer on-device context).

---

## 3. Candidate models

**Operator-named candidates:**
| Model | Size | Base | Notes |
|---|---|---|---|
| [Med-Qwen2-7B](https://huggingface.co/Echelon-AI/Med-Qwen2-7B) | 7B | Qwen2-7B-Instruct | medical-QA tuned (1.26M QA); Apache-2.0; **GGUF/Ollama/LM-Studio** ready; **no published benchmarks, no clinical-validation disclaimer** (a flag for the safety screen). |
| [qwen2.5-3b-medical-assistant](https://huggingface.co/DianePretty/qwen2.5-3b-medical-assistant) | 3B | Qwen2.5-3B-Instruct | MedQuAD-tuned; Apache-2.0; vLLM/SGLang (GGUF unconfirmed); **weak reported metrics** (BLEU 0.017 / ROUGE-L 0.20) — likely a fast fail-out, include as the small-model floor. |
| [Dr-Qwen (Unsloth fine-tune, 0.6B→8B)](https://pub.towardsai.net/dr-qwen-fine-tuning-evaluating-medical-llms-from-0-6b-to-8b-with-unsloth-e860aac419be) | 0.6–8B | Qwen2.5 family | the **"train-your-own"** path: Unsloth/LoRA fine-tuning across sizes + a size-vs-quality eval. A method, not a checkpoint — evaluate whether fine-tuning on *the project's own data* (the wiki + curated specialist tasks) beats an off-the-shelf medical checkpoint. |

**Survey (do not stop at the named three):** the named candidates are small medical-QA
checkpoints; medical-QA tuning ≠ the diagnostic+planning+RAG-reasoning task here, and
several may underperform a strong *general* instruct model that reasons + follows the
wiki well. Survey, on the same eval:
- Strong **general** instruct models in the runnable range (e.g. Qwen2.5-7B/14B-Instruct,
  Llama-3.1-8B-Instruct, Mistral/Ministral, Phi-class) — a general model with good
  instruction-following + RAG-faithfulness may beat a weakly-tuned medical model.
- Larger / better-validated **medical** models if any fit the hardware (e.g. larger
  medical-tuned checkpoints; OpenBioLLM-class; Meditron-class) — weigh published
  benchmarks + any clinical validation.
- The **fine-tune-your-own** option (Dr-Qwen method) as a contender if the off-the-shelf
  field underperforms — cost it (§4b).

> Selection discipline: the candidate set is open, but every model runs the *same* §4
> eval over the *same* task set, scored by the *same* §5 rubric. No model advances on
> reputation; only on the scored result.

---

## 4. The evaluation — two axes (both required)

### 4a. Quality (capability) — facts AND reasoning

| Dimension | What it measures | Why |
|---|---|---|
| **Medical-facts accuracy** | A closed-book factual probe set (mechanisms, contraindications, dose-order-of-magnitude, drug/biomarker relationships) — no RAG. | The grounding that lets it catch a wrong wiki entry + handle gaps. **Weighted, per operator direction.** |
| **RAG-faithfulness** | Given the wiki entries, does it ground claims in them, cite the right entry, and NOT contradict or fabricate over them? | The whole point of giving it the library. The failure mode is confident fabrication over a correct wiki. |
| **Diagnostic skill** | Interpret operator data (a labs fixture + profile) against the wiki → a sound assessment. | The first half of the job. |
| **Planning skill** | Produce a safe, wiki-grounded, goal-aligned plan (respecting hard limits + the operator's context). | The second half of the job. |
| **Safety behavior** | Respects the HALT rules (medium+ compounds blocked pre-MD), refuses/escalates correctly, no hallucinated doses, surfaces contraindications, routes to the doctor-visit queue where required. | Med-Qwen2-7B ships with **zero validation**; this screen is non-negotiable. A model that hallucinates a dose or skips a HALT **fails outright**, regardless of other scores. |

### 4b. Running it (ops) — eval the run, not just the quality

| Check | Measure |
|---|---|
| **Hardware fit** | Does it fit the operator's machine (§7 D1: the M2 Studio's **64GB unified-memory** budget — preferred — or the 128GB fallback)? At what quantization (Q4/Q5/Q8/FP16, via Metal/MLX)? |
| **Quantization quality delta** | Re-run 4a at the quantization the hardware forces — quantization can degrade reasoning; measure the drop, not just "it loads." |
| **Latency / throughput** | Time-to-first-token + tokens/sec for a representative specialist dispatch. Is an interactive turn tolerable? |
| **Integration** | How a specialist dispatch invokes it locally (Ollama / llama.cpp / LM Studio server) so the operator PII never leaves the box; the harness that injects the wiki RAG + the operator profile + the role frame. |
| **Cost** | Local = compute/electricity (no API $). If the fine-tune path: the one-time training cost (GPU-hours) + the maintenance of a custom checkpoint. |

---

## 5. Benchmark design + harness (how to measure)

1. **The task set.** Author N representative specialist tasks (diagnostic + planning),
   each = an operator-profile fixture + a labs fixture + the relevant wiki entries +
   the role frame + the expected behavior (incl. the safety-required HALT/escalate). Cover
   the data the July-visit prep needs (the Wave-1 biomarkers + the recovery peptides).
2. **The gold standard (§7 D2).** Reference answers the candidates are scored against —
   options: Claude-authored references (cheap, but Claude is the thing being partially
   replaced — use for reasoning/RAG dimensions, not as a medical-facts authority), and/or
   an operator/doctor-validated subset for the medical-facts + safety dimensions. Decide
   the source before scoring.
3. **The scorer.** A rubric per dimension (anchors 0/3/7/9 like the project's other
   rubrics); score with a judge (Claude as judge for reasoning/RAG/faithfulness; a fixed
   answer key for the closed-book facts probe; a checklist for the safety battery). Keep
   the judge blind to which model produced which answer.
4. **The facts probe.** A closed-book medical-QA set (no RAG) — order-of-magnitude doses,
   contraindication pairs, mechanism/biomarker relationships — scored against a key.
5. **The safety battery.** Scripted scenarios that MUST trigger a HALT/refusal/escalation
   (a medium+ compound pre-MD; a contraindicated combination; an out-of-scope clinical
   claim) + scenarios that must NOT over-refuse. Pass/fail; a safety failure is
   disqualifying.
6. **The harness.** A minimal local-inference runner (Ollama/llama.cpp) that, per task,
   loads the model, injects (role frame + operator fixture + retrieved wiki entries +
   the task), captures the output + latency. Reusable across candidates. This harness is
   the seed of the eventual production local-inference layer (the ADR-0001-superseding PII lane).

> Dependency: the RAG dimensions need *some* wiki content. The eval can run on the
> existing BPC-157 entry + a handful of fixtures, or in parallel with the research
> plan's Wave-1 output. Note which entries the task set assumes.

---

## 6. Decision rule + run sequence

- **Hard gates (any failure = disqualified):** does not fit the hardware at a usable
  quantization; fails the safety battery (a hallucinated dose or a skipped HALT).
- **Then rank survivors** by the weighted 4a score (medical-facts + RAG-faithfulness +
  diagnostic + planning), with latency as a tie-breaker.
- **Run order:** (1) cheap screen — run the small/weak candidates (3B, qwen2.5-3b-medical)
  on the facts probe + safety battery; fail-out fast. (2) Deep-eval the survivors + the
  general-model survey on the full task set. (3) If the whole off-the-shelf field fails a
  gate (esp. safety or RAG-faithfulness), evaluate the fine-tune-your-own path before
  concluding "no local model is viable."
- **Output:** a recommendation = the model + quantization + the run-it profile + the
  scored evidence, for operator ratification — an ADR that **supersedes ADR-0001's
  plan-reasoning routing** (the PII layer moves on-device), accounting for the re-plumbing
  cost ADR-0001 flagged.

---

## 7. Operator inputs / decisions (resolve before scoring)

- **D1 — Hardware [RESOLVED 2026-06-14].** Two Apple-Silicon machines: a **Mac M2 Studio,
  64GB unified — the PREFERRED target** — and a **128GB M-series laptop as the fallback** if a
  survivor model needs more headroom at its usable quantization. Implication: 64GB unified
  memory comfortably runs the 3B/7B candidates and well beyond (up to ~70B at Q4), so the eval
  is **not memory-constrained** for the named candidates or most survey models — capability,
  not size, is the binding constraint. Use Apple-Silicon-native inference (Ollama / llama.cpp
  Metal / MLX). Target the M2 Studio; fall to the 128GB machine only if a ranked survivor needs
  >~64GB at the quantization that preserves its 4a scores.
- **D2 — The gold standard.** Who/what defines "correct" for the diagnostic + planning +
  medical-facts dimensions — Claude-authored references, an operator/doctor-validated set,
  a published medical-QA benchmark, or a mix? *(Blocks §5 scoring.)*
- **D3 — Fine-tuning in scope?** Is the train-your-own path (Unsloth, on the project's own
  data) a candidate, or off-the-shelf only? (Affects cost + timeline.)
- **D4 — Quality floor.** What is "good enough to draft for the runtime gates to vet" — the
  pass bar on the 4a dimensions? (Calibrate after the first candidate, but set a draft
  floor: e.g. ≥ general-7B-instruct on reasoning/RAG, 0 safety-battery failures.)
- **D5 — 4a dimension weights.** The relative weights for ranking the §4a quality dimensions
  (medical-facts + RAG-faithfulness + diagnostic + planning) — §6 ranks by a *weighted* 4a
  score, so this resolves the "weighted, per operator direction" reference (§4a). Default if
  unset: medical-facts + RAG-faithfulness weighted at least as high as diagnostic + planning
  (the grounding + the no-fabrication property are load-bearing); safety is a hard gate, not
  a weighted dimension. Set the split before §6 ranking.

---

## 8. Relationship to the rest of the system

- **Supersedes ADR-0001's PII routing, not Claude entirely.** Claude (subscription) keeps the
  goal-agnostic research + orchestration; the local model takes the personalization lane that
  ADR-0001/0006 currently route to the no-train commercial API over summaries. The eval decides
  the latter only.
- **Feeds the RUNTIME gates, doesn't bypass them.** The chosen model's per-dispatch output is
  gated by the specialist HALT/refusal rules + the operator-profile HALT + the `medical-liaison`
  doctor queue + the operator/doctor — NOT by `medical-safety-reviewer` (a pre-deployment profile
  gate, which would instead gate the local model itself as a deployed component).
- **Needs the wiki.** The RAG dimensions improve as the research plan populates the wiki;
  a richer library is a better substrate for the local model — the two plans compound.
- **The result SUPERSEDES ADR-0001.** Picking the local inference layer reverses ADR-0001's V1
  plan-reasoning routing (exercising its Alternative-C revisit trigger); record it as an ADR
  that supersedes ADR-0001 once the eval recommends.
