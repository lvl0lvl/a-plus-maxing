---
title: Local Model Evaluation Plan
type: plan
owner: Walter McGivney
created: 2026-06-14
last_reviewed: 2026-06-14
status: active
depends_on: []
superseded_by: null
review_cadence: phase
permalink: a-plus-maxing/model-eval/local-model-evaluation-plan
---

# Local Model Evaluation Plan

The executable plan for choosing (or training) the **local model that runs the
PII-sensitive personalization** — the work that must stay off the cloud, which the
project was otherwise going to send to the Anthropic API. The Claude subscription
keeps the goal-agnostic rest (the `/aplus-research` wiki research, orchestration,
the build). This plan decides *which local model*, on *what hardware*, at *what
quality and safety*, and how it slots in.

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

## 1. Premises — what the local model is FOR

**The architecture split (the `hil` gap resolution).** The project's standing open
problem (bead `hil`): *"the system uses operator PII without sending it to Anthropic."*
The answer is a **local-inference layer**:

- **Local model** → the **personalized** layer: take the operator's PII
  (`operator-profile.md`, labs, `goals.md`, `current-state.md`) + the goal-agnostic
  wiki (via RAG) + a specialist role, and produce a personalized **diagnostic + plan**
  — entirely on-device. This is the work that would otherwise hit the API.
- **Claude subscription** → the **goal-agnostic** rest: `/aplus-research` wiki research
  (no operator PII — goal-agnostic by design), orchestration, the build, this kind of
  planning doc.

**The model is NOT autonomous.** Its outputs feed the *existing* safety apparatus —
the `medical-safety-reviewer` agent, the operator-profile HALT rules (medium+ compounds
blocked until the January-2026 section + MD clearance), the `medical-liaison`
doctor-visit queue, and the operator + doctor as human-in-the-loop. The bar is
therefore **"good enough to draft personalized recommendations that the safety layer,
the operator, and the doctor vet"** — not "autonomous medical authority." That bar
still requires real medical grounding and safe behavior; it does not require a
clinician-grade autonomous diagnostician.

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
INPUT:  operator PII (profile + labs + goals + current-state)
      + the relevant wiki entries (RAG: compounds / biomarkers / library)
      + a specialist role frame (e.g. peptide-specialist, labs-specialist)
TASK:   produce a personalized assessment + plan —
        - interpret the operator's data against the wiki evidence,
        - respect contraindications, the HALT rules, and the goal/limit anchors,
        - cite the wiki entry it grounds each recommendation in,
        - HALT / escalate to the doctor-visit queue where the rules require.
OUTPUT: a diagnostic + plan the safety layer + operator + doctor then vet.
```

This is exactly what the deployed specialist `agent.md` profiles describe — the eval is
"can a local model run that role acceptably, given the wiki + the operator profile."

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
| **Hardware fit** | Does it run on the operator's machine (§7 D1: VRAM/RAM/CPU/GPU)? At what quantization (Q4/Q5/Q8/FP16)? |
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
   the seed of the eventual production local-inference layer (`hil`).

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
  scored evidence, for operator ratification (an ADR-worthy decision: it sets the local
  inference layer).

---

## 7. Operator inputs / decisions (resolve before scoring)

- **D1 — Hardware.** What machine runs the local model (CPU/GPU, VRAM, RAM, OS)? This
  gates the entire run-it axis + the candidate size ceiling. *(Blocks §4b.)*
- **D2 — The gold standard.** Who/what defines "correct" for the diagnostic + planning +
  medical-facts dimensions — Claude-authored references, an operator/doctor-validated set,
  a published medical-QA benchmark, or a mix? *(Blocks §5 scoring.)*
- **D3 — Fine-tuning in scope?** Is the train-your-own path (Unsloth, on the project's own
  data) a candidate, or off-the-shelf only? (Affects cost + timeline.)
- **D4 — Quality floor.** What is "good enough to draft for the safety layer to vet" — the
  pass bar on the 4a dimensions? (Calibrate after the first candidate, but set a draft
  floor: e.g. ≥ general-7B-instruct on reasoning/RAG, 0 safety-battery failures.)

---

## 8. Relationship to the rest of the system

- **Replaces the API for PII work, not Claude entirely.** Claude (subscription) keeps the
  goal-agnostic research + orchestration; the local model takes the personalization. The
  eval decides the latter only.
- **Feeds, doesn't bypass, the safety apparatus.** The chosen model's outputs still go
  through `medical-safety-reviewer` + the operator-profile HALT rules + the doctor queue.
- **Needs the wiki.** The RAG dimensions improve as the research plan populates the wiki;
  a richer library is a better substrate for the local model — the two plans compound.
- **The result is ADR-worthy.** Picking the local inference layer is an architecture
  decision (it resolves `hil`); record it as an ADR once the eval recommends.
