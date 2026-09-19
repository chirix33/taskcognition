# TaskCognition Manuscript Evidence Pack

**Status:** Pre-results manuscript plan. **No TaskCognition experiment has been run, and no proposed effect has been observed.** Every TaskCognition architecture, hypothesis, comparison, table, and analysis below is prospective.

**Literature cutoff:** 19 September 2026.

**Recommended title:** **TaskCognition: Auditing Direct-to-Reasoning Routing with Paired Policy Swaps**

**Conditional post-results title, permitted only if the evidence supports it:** **TaskCognition: Risk-Calibrated Routing Between Direct and Bounded Reasoning Policies**

The supplied brief asks for one learned layer above a reasoning-capable model, the meeting calls for a criterion more precise than “easy,” “hard,” or vaguely “coupled,” and both require a focused nine-page paper with only two or three benchmarks. The title in the brief—“Learning When Overuse of Reasoning Models Degrades Answer Performance”—should not survive unchanged. It presupposes a broad result, echoes *Learning When to Plan*, and says “reasoning models” even though the clean treatment is two inference policies on one frozen model.[1] [2]

---

## 1. The paper story to settle

### 1.1 One-sentence claim

> **Proposed claim:** For one frozen base model and two permission-matched inference policies, TaskCognition will test whether a pre-generation gate trained on **paired direct-relative utility** and **direct-correct/reasoning-wrong risk** yields a better utility–harm–compute frontier than confidence, absolute-success/cost, and paired winner-classification routers under held-out template shift.

This is deliberately **not** a claim to invent reasoning routing. Select-then-Solve already routes among Direct, chain-of-thought (CoT), ReAct, Plan-Execute, Reflection, and ReCode; SynapseRoute trains a thinking/non-thinking classifier from paired outcomes; Think When Needed makes a pre-generation Non-Think/Think decision; Route to Reason predicts performance and length for model–strategy pairs; and DynaThink implements fast/slow selection.[3] [4] [5] [6] [7] The paper can survive that crowded field only if it makes the **paired estimand, matched policy comparison, harm-sensitive decision rule, and full counterfactual audit** the scientific object.

### 1.2 Why this story is worth testing

The motivation is conditional, not universal. Mind Your Step reports significant CoT degradation in three of six psychology-derived task archetypes, including implicit statistical learning and classification with exceptions.[8] When More Is Less finds an inverted-U relation between CoT length and accuracy.[9] LLMThinkBench reports that reasoning models can use far more tokens while attaining lower accuracy on dynamically generated basic mathematics.[10] These studies establish that more external reasoning can be inefficient or harmful in some regimes. They do **not** establish that TaskCognition’s gate will work, reveal a model’s cognition, or generalize across models and domains.

### 1.3 Contributions that the manuscript may propose now

1. **A matched two-policy object.** The study will compare one direct policy and one bounded visible-reasoning policy on the same frozen model, with the same task information, answer schema, decoding distribution, tool permissions, validator access, call cap, and output cap.
2. **A direct-relative learning target.** Rather than predicting only “reasoning succeeds” or a generic difficulty label, the proposed gate will estimate the incremental utility of replacing the direct policy with the reasoning policy.
3. **An operational harm target.** The proposed safety quantity is the observable event that the direct policy is correct and the reasoning policy is incorrect on a paired rollout. It is strategy-induced or avoidable harm under the named policies, not a claim about latent cognition or moral harm.
4. **A complete policy-swap audit.** Both policies will be forced on every final-test instance. This reveals the four direct/reasoning outcome quadrants, routing regret, rescue events, selected-route harm, and the actual source of any gain.
5. **A shift test, not merely an in-distribution classifier score.** Training, calibration, and testing will separate templates, renderers, or task families. The principal novelty test is whether paired-harm supervision changes decisions and retains value beyond incumbent routers under shift.

### 1.4 Explicit non-contributions

The paper will not claim the first learned router, the first evidence of overthinking, the first risk-aware reasoning controller, the first adaptive planning system, or a general theory of when models “think.” It will not headline typed contracts. It will not add tools, retrieval, reflection, self-consistency, multiple models, planning agents, repair, memory, or abstention as new action classes. “Global coupling” may appear only as an optional secondary annotation with a declared operational definition; it is not the headline mechanism.

### 1.5 Decision rule for whether this becomes a method paper or a negative-results audit

The method claim should survive only if the proposed paired benefit/harm target changes routing decisions and improves a preregistered harm–utility–compute frontier over both (i) a SynapseRoute-style paired winner classifier and (ii) a Route-to-Reason-style absolute performance/cost predictor, especially on held-out templates. If it does not, the honest paper is a **negative audit**: direct-relative harm adds little beyond existing routing targets, or it fails to calibrate under shift. That outcome is scientifically useful and should not be hidden by adding tasks or policy variants.

---

## 2. Exact proposed TaskCognition architecture

### 2.1 Architectural overview

```text
pre-decision instance x
        │
        ├── frozen text encoder e(x)
        └── cheap observable features f(x)
                 │
          shared shallow trunk
           ┌─────┴──────────┐
 benefit head bφ(x)      harm head qφ(x)
 ≈ E[UR − UD | x]       ≈ P(YD=1,YR=0 | x)
           │                  │
     held-out calibration: point predictions + uncertainty bounds
           └──────────┬───────┘
                      │
 R iff LCB[bφ(x)] > 0 and UCB[qφ(x)] ≤ α
 otherwise D          │
          ┌───────────┴───────────┐
 direct policy πD                 reasoning policy πR
 one answer-only call             one bounded visible-CoT call
          └───────────┬───────────┘
             same final-answer extractor
```

This is a constrained two-algorithm selector in the sense of classical algorithm selection.[11] The controller is intentionally small. Novelty must come from what is estimated and audited, not from a new neural routing architecture.

### 2.2 Base model

The recommended primary backbone is the **original unified Qwen3-8B (Qwen3-2504) checkpoint**, not the later separate Instruct-2507 and Thinking-2507 checkpoints. The original release supports thinking/non-thinking switching in one set of weights, whereas the later variants are distinct checkpoints.[12] The paper must archive the exact model revision, tokenizer and chat template, inference-engine version, numerical precision, hardware, and prompt hashes. A Qwen3-14B replication is desirable only after the 8B protocol is frozen; failure to complete it should be reported as a one-model limitation rather than covered with a model-general claim.

### 2.3 Primary gate inputs

The proposed gate receives only information available **before** either answer policy executes:

- a frozen query embedding `e(x)`;
- input token and character counts;
- numeric-token count;
- multiple-choice marker count;
- symbolic-operator count;
- a small set of deterministic format indicators, frozen before training.

The gate must not receive dataset identity, generator-private difficulty labels, reference answers, policy traces, verifier feedback, or a direct draft. Any structural annotations such as graph size, exception rate, or generator depth are for stratified analysis unless they are truly available to the deployed system. A direct-confidence method that first generates an answer is a **paid cascade baseline**, not the primary pre-generation gate.

### 2.4 Predictor and loss

Let a frozen encoder produce `e(x)`. Concatenate it with standardized observable features `f(x)` and pass the result through a two-layer multilayer perceptron with shared hidden representation. The two required heads are:

- `bφ(x)`, a scalar estimate of direct-relative utility `Δ(x)`;
- `qφ(x)`, a probability estimate of avoidable harm `h(x)`.

An optional third head may estimate incremental cost if raw utility labels are not used, but the direct-difference head remains primary. With repeated paired rollouts, train `bφ` with weighted Huber loss on the empirical mean utility difference and train `qφ` with fractional-binomial log loss on the empirical harm frequency. Fix loss weights from training data only. Use class-balanced weighting or focal loss only if preregistered and only after reporting the raw harm prevalence; otherwise a rare-event head can look calibrated by always predicting near zero.

### 2.5 Calibration and conservative routing

Reserve a template-disjoint calibration split. Calibrate `bφ` and `qφ` separately with a preregistered monotone calibrator such as isotonic regression. Construct uncertainty bounds with one frozen procedure—for example, cluster bootstrap prediction intervals or conformalized residual intervals. Deploy the proposed rule

\[
g_\phi(x)=
\begin{cases}
R,& \operatorname{LCB}_{1-\delta}\!\left[b_\phi(x)\right] > 0
\quad\land\quad
\operatorname{UCB}_{1-\delta}\!\left[q_\phi(x)\right] \le \alpha,\\
D,& \text{otherwise.}
\end{cases}
\]

Here `α` is the maximum accepted estimated harm rate for the reasoning-selected subset, and `δ` fixes the bound confidence level. Both are selected on calibration data and frozen before final testing. Conformal Risk Control can motivate calibration of a monotone bounded loss, but any guarantee is valid only under the declared loss, threshold family, exchangeability, policy, scorer, and data-distribution assumptions.[13] Conformal Thinking controls the stopping time of an already running trace, so it is adjacent rather than equivalent prior work.[14]

### 2.6 What must be frozen before final test

Freeze the base model and revision, both system/user prompts, thinking-mode control, answer tags, maximum input and output lengths, temperature, top-p, top-k, seed list, number of calls, timeout behavior, retry rule, parser, scorer version, gate features, encoder, architecture, training seed policy, calibration method, `λ`, `α`, `δ`, and test split manifest. Failed calls must be logged and rerun under the same seed; silent resampling is prohibited.

---

## 3. Compact formal problem statement

Let `X∈𝒳` be the pre-decision observable task instance and `A={D,R}` the action set. `π_D` is the declared direct policy and `π_R` the declared bounded explicit-reasoning policy. A forced execution of policy `π_a` from the same initial state produces

\[
O_a=(S_a,C_a,Z_a), \qquad a\in\{D,R\},
\]

where `S_a∈[0,1]` is the preregistered task score, `C_a` is the all-in cost ledger, and `Z_a` is an audit record containing the raw output, parsed answer, generation status, token counts, calls, and latency. Define

\[
U_a=S_a-\lambda C_a,
\qquad
\Delta(x)=\mathbb{E}[U_R-U_D\mid X=x].
\]

`λ≥0` is fixed before test analysis. Because its meaning depends on the units of `C`, raw score and every cost component must also be reported. For exact binary scoring, let

\[
Y_a=\mathbf 1\{S_a=1\},
\qquad
h(x)=\Pr(Y_D=1,Y_R=0\mid X=x).
\]

The realized paired events are

\[
H=\mathbf 1\{Y_D=1,Y_R=0\},
\qquad
B=\mathbf 1\{Y_D=0,Y_R=1\},
\]

where `H` is **avoidable strategy-induced harm** and `B` is a **reasoning rescue**. The proposed gate selects `A_g=gφ(X)`. Its selected utility is `U_g=U_D·1{g=D}+U_R·1{g=R}`. Its oracle regret is

\[
\mathcal{R}_{\mathrm{oracle}}
=\mathbb{E}\!\left[\max(U_D,U_R)-U_g\right].
\]

The primary estimand is the paired selected-utility contrast versus always-direct,

\[
\theta=\mathbb{E}[U_g-U_D],
\]

reported with a paired interval. The primary safety quantities are

\[
H_{\mathrm{sel}}=\mathbb{E}[\mathbf 1\{g=R\}H],
\qquad
H_{\mathrm{cond}}=\Pr(H=1\mid g=R),
\]

plus **excess harm above always-direct**, which equals `H_sel` under exact binary scoring because always-direct cannot itself create a D-correct/R-wrong switch. Report routing rate `ρ=Pr(g=R)` so low harm cannot be manufactured by almost never reasoning.

For stochastic policies, the expectation is over the declared generation randomness and any resettable environment randomness. Pair direct and reasoning executions by a fixed seed-coupling protocol and repeat `K` rollouts. With one rollout, call `H` a realized paired outcome, not a per-instance harm probability. On static tasks both outcomes can be observed offline; this identifies policy-relative differences on the evaluated distribution, not an LLM’s latent thought process.

> **Operational definition of direct:** one model call that emits the answer without an externally materialized rationale, subtask plan, or decomposition before the answer. It does not imply absence of hidden computation.

> **Operational definition of reasoning:** one model call under a fixed instruction to emit a visible reasoning trace followed by the answer, subject to a declared token ceiling. It is not interchangeable with tools, retrieval, self-consistency, reflection, planning agents, or multiple calls.

---

## 4. Direct and reasoning policies: the fairness contract

The comparison is interpretable only if the policies differ in the requested external reasoning behavior rather than in information or permissions. Select-then-Solve explicitly studies heterogeneous policy packages, some with tools and many more calls.[3] TaskCognition should instead use the following matched controls.

| Component | Proposed direct policy `π_D` | Proposed reasoning policy `π_R` | Fairness requirement |
|---|---|---|---|
| Backbone | Frozen original Qwen3-8B checkpoint | Same checkpoint | Same weights and revision |
| Mode | `enable_thinking=False` | `enable_thinking=True` | Native unified-mode switch only |
| Task input | Identical task text and demonstrations | Identical | No hidden metadata |
| Tools/retrieval | None | None | No calculators, browsing, code, or search |
| Calls | One | One | No retries, reflection, validation, or self-consistency |
| Output cap | Same hard `max_new_tokens` ceiling | Same ceiling | Recommended main cap: 256; ablate 128/512 |
| Decoding | Same temperature, top-p, top-k, and paired seed | Same | Recommended sampled setting: 0.6/0.95/20 plus deterministic sensitivity |
| Answer schema | `<FINAL>answer</FINAL>` only | Visible trace, then identical final tag | Same parser and failure rule |
| Validator | Evaluation-only | Evaluation-only | Neither policy sees scorer feedback |
| Cost ledger | Input/output tokens, one call, measured latency | Same components | Router cost included separately |

The equal cap does not imply equal realized compute; therefore report realized output tokens and latency. The direct output instruction should be minimal and should not ban hidden reasoning. The reasoning instruction should not prescribe decomposition, tools, branching, or a detailed plan; it should request a short visible step-by-step analysis bounded by the same call and output ceiling. If the native mode cannot reliably honor the same cap, that limitation must be logged as a policy-package difference.

A direct-confidence baseline is sequential: it first runs `π_D`, observes answer confidence, and conditionally runs `π_R`. Charge the first call and its tokens. Do not compare this privileged cascade to an input-only gate as though both receive the same information.

---

## 5. Exactly three core benchmark suites

The main paper should use **three suites**. They create a positive-transfer regime, a routine overuse regime, and a known harm stress regime without turning the paper into a leaderboard.

### 5.1 Core suite A: Reasoning Gym control panel

Reasoning Gym supplies more than 100 procedural generators, adjustable complexity, seeds, metadata, and algorithmic verification through a standard `score_answer` interface.[15] Use only six preregistered generators rather than the full catalog:

- routine/pattern-oriented: `number_sorting`, `number_format`, `letter_counting`;
- structured reasoning: `graph_color`, `shortest_path`, `knights_knaves`.

For each family, write three semantics-preserving surface renderers. Train and calibrate on renderers 1–2; reserve renderer 3 for template shift. Generator metadata remains hidden from the gate. The suite is the main source of paired training labels because it can supply fresh, disjoint instances and exact scores. Public algorithms and generator code may still be represented in pretraining, so fresh generation reduces exact-instance duplication but does not prove contamination freedom.

**Why core:** it allows controllable disagreement, exact scoring, balanced sampling, and template-level shift in one infrastructure. It is not presented as evidence that all of its tasks need reasoning.

### 5.2 Core suite B: LLMThinkBench routine-math stress test

LLMThinkBench provides 14 dynamically generated, exact/basic-math task families and open tooling. The published study reports severe reasoning inefficiency and occasional accuracy loss, making it a direct adversarial test of unnecessary reasoning.[10] Use a preregistered subset that does not duplicate the Reasoning Gym tasks excessively: comparison, subtraction, multiplication, division, odd/even counting, mean, median, and mode. Generate new examples after prompts and policies are frozen.

Treat this suite as **external transfer**, not gate-training data in the headline experiment. Re-score every output with the package’s exact task evaluator, and report raw accuracy and token use rather than relying on the package’s normalized Overthinking Score.

**Why core:** it asks whether TaskCognition avoids spending bounded reasoning on deterministic routine work and whether reasoning creates D-correct/R-wrong flips. It also prevents a misleading success story in which the gate merely recognizes reasoning-heavy procedural tasks.

### 5.3 Core suite C: Mind Your Step exact-label harm diagnostic

Use two text-only, exact-label families from Mind Your Step: **implicit statistical learning/artificial grammar** and **classification with exceptions**. These belong in a held-out stress suite because the source already reports task-conditional CoT harm.[8] Prefer fresh, license-clear re-generation of the mechanisms while following the paper’s controls over prompt format, grammar or rule complexity, demonstrations, temperature, and exception rate. If the released data are reused, verify redistribution terms because the repository exposes a Drive download but no explicit repository license.[16]

Hold out grammar graphs, token alphabets, rule templates, exception placements, and paraphrase families. Do not include face recognition unless the entire paper is extended to identical multimodal inputs for both policies.

**Why core:** it directly tests the rare-event harm head in a published risky regime. It does not establish broad generalization and must not be used to claim discovery of overthinking.

### 5.4 Why not the tempting alternatives

BIG-Bench Hard is useful as an appendix sensitivity check, but its 23 public tasks and task-specific CoT heritage introduce prompt and exposure heterogeneity.[17] OptimalThinkingBench is highly relevant but partially reuses Reasoning Gym and already frames over-/underthinking with its own token-adjusted objective and LLM-judged overthinking items.[18] GSM8K is exact and familiar, but it is a fixed, highly exposed dataset that adds little beyond the controlled procedural suite. PopQA adds an atomic factual stratum, but its public facts and alias-substring evaluator create contamination and scoring concerns. Interactive planning, tool, and web-agent suites should remain future work because they introduce unmatched state, tools, retrieval, and recovery.

---

## 6. Proposed splits, sample plan, and execution matrix

### 6.1 Reasoning Gym split

For each of six generators, use 200 training, 75 calibration, and 100 in-distribution test instances across the two seen renderers. This yields 1,200 training, 450 calibration, and 600 in-distribution test instances. Add 50 examples per family in the unseen third renderer, yielding 300 template-shift instances. Use non-overlapping generator seeds and hold out at least one parameter range per family. Validate every reference answer before inference.

### 6.2 LLMThinkBench split

Generate 50 examples for each of eight task families after the complete TaskCognition system is frozen, for 400 external-transfer items. These data are test-only. Preserve independent generation seeds by task and stratify results by task family and list/operand size. If 400 items are not feasible, reduce families before reducing per-family coverage; do not tune on the retained set.

### 6.3 Mind Your Step diagnostic split

Target 200 artificial-grammar and 200 exception-classification items, all test-only. Use balanced labels and held-out grammar/rule structures. If generating fresh variants, create a separate development pool for validating only the parser and scorer; no outcome from the final 400 may influence prompts, thresholds, or feature design.

### 6.4 Repeated rollouts

Run both policies for every item under five paired decoding seeds, proposed as `{11,23,37,53,71}`. The inferential unit is the problem instance; seeds remain within-instance repeated measures. If budget forces a reduction, retain paired execution on every item and reduce from five to three seeds. Never substitute one policy outcome for the missing counterfactual.

### 6.5 Contamination and identity controls

Do not expose suite or generator names to the gate. Randomize renderer labels and superficial identifiers. Report per-suite results so a pooled gain cannot be attributed only to source recognition. Fresh generation reduces exact duplication but does not demonstrate absence from pretraining. Archive generator commit hashes, dates, configurations, and seeds.

---

## 7. Baselines that must appear

The main table should include the following baselines, all restricted to the same two frozen policies unless explicitly labeled as a cascade.

| Baseline | What it tests | Fair implementation |
|---|---|---|
| Always direct | Default-action floor | Run `π_D` on all items |
| Always reasoning | Upper-compute fixed policy | Run `π_R` on all items |
| Random, budget matched | Value beyond routing rate | 100 fixed random assignments at each reasoning-rate budget |
| Query length | Trivial observable heuristic | Threshold selected on calibration data |
| Declared difficulty/format heuristic | Easy-versus-hard alternative | Only observable counts; no generator metadata |
| Direct confidence | Post-draft confidence routing | Use normalized final-answer log probability, margin, `P(True)`, or verbalized confidence; charge the direct call |
| CAR-style draft-PPL cascade | Strong confidence cascade | First run direct, then PPL gate to reasoning; charge both calls when escalated [19] |
| Restricted Select-then-Solve style | Embedding router | Logistic regression and shallow MLP on the same input embedding [3] |
| SynapseRoute style | Paired winner classifier | Classify cheapest successful/winning D or R label; retain ties and both-fail cases rather than silently dropping them [4] |
| Route-to-Reason style | Absolute success/cost router | Predict `P(Y_D)`, `P(Y_R)`, and costs separately; select expected score minus cost [6] |
| Zero-shot self-routing | Model introspection baseline | One paid router call or a short routing token, with cost reported |
| Offline paired oracle | Non-deployable ceiling | Select the higher realized or estimated paired utility; report tie rate |

Confidence-Gated CoT evaluates direct-answer confidence measures, random routing, and oracle behavior across several task suites, so it is the principal evaluation precedent for cascade baselines.[20] DynaThink is the established fast/slow conceptual baseline.[7] Think When Needed and When to Reason are pre-generation classifier precedents; report the former as an arXiv preprint because its rendered venue metadata contains placeholders.[5] [21]

---

## 8. Metrics and statistical analysis

### 8.1 Primary endpoint

The primary proposed endpoint is the paired difference in selected utility versus always-direct at one preregistered operating point:

- main `λ`: report after cost normalization is fixed; recommended candidate sensitivity grid `{0, 0.01, 0.02, 0.05}` with one value declared primary before final test;
- main reasoning-rate budget: `B=0.50`, with `B∈{0.20,0.50,0.80}` shown as a frontier;
- main harm cap: `α=0.10`, justified as an operating constraint rather than a universal safety value.

Report a two-sided 95% paired, task-stratified cluster-bootstrap confidence interval over instances. The main hypothesis test is a two-sided paired permutation test on per-instance `U_g-U_D` with 10,000 sign flips at `α_test=.05`.

### 8.2 Mandatory paired outcome table

For every test suite publish the complete 2×2 table:

| Forced policy outcome | `R` correct | `R` incorrect |
|---|---:|---:|
| `D` correct | both correct | **avoidable harm `H`** |
| `D` incorrect | **reasoning rescue `B`** | both incorrect |

Report the unconditional harm rate, harm conditional on selecting reasoning, harm conditional on direct correctness, rescue rate, both-correct rate, both-wrong rate, and answer-flip rate. Aggregate accuracy alone can conceal both harm and rescue.

### 8.3 Utility, cost, and selection metrics

Report exact accuracy or native bounded score; mean `U_R-U_D`; selected utility; contrast with always-D and always-R; reasoning-selection rate; tokens, calls, and latency as distributions; paired oracle regret; fraction of oracle gain recovered; tie rate; parser failures; and timeout rate. Plot utility–harm–reasoning-rate frontiers at fixed expected-token budgets and at fixed harm caps.

The cost ledger should include gate inference, input tokens, generated tokens, number of language-model calls, and measured wall-clock latency on declared hardware. Do not collapse them into one monetary scalar in the main table. If a scalar cost is needed, normalize components before applying `λ` and publish the normalization.

### 8.4 Calibration metrics

For `bφ(x)`, report mean absolute error, root mean squared error, reliability by fixed bins, and interval coverage. For `qφ(x)`, report Brier score, log loss, calibration intercept/slope, fixed-bin expected calibration error, reliability diagrams, and interval coverage. Report all calibration results separately for in-distribution, unseen renderer, LLMThinkBench, and Mind Your Step. Marginal calibration may hide subgroup failure.

### 8.5 Statistical tests

Use the following preregistered analysis set:

- **Primary comparison:** paired permutation test on `U_g-U_D` at the main operating point.
- **Policy swap:** paired permutation test on `S_R-S_D`; exact McNemar test on one locked rollout as a sensitivity analysis for binary scores.
- **Baseline comparisons:** paired permutation tests on utility and paired bootstrap intervals on harm differences.
- **Shift interaction:** cluster bootstrap or mixed-effects regression for method × unseen-template/task-family interaction, with task family as a fixed effect and instance as the cluster.
- **Multiple comparisons:** Holm correction across all non-primary baseline, transfer, and ablation tests.
- **Rare harm events:** Clopper–Pearson or Wilson intervals for simple rates; if zero events occur, report the one-sided upper bound rather than “zero risk.”
- **Gate seeds:** train five initialization seeds, report min/median/max, and lock one seed by calibration-only selection for the primary test. Decoding seeds are repeated measures, not independent samples.

Every table should show effect size and confidence interval even when the corrected test is not significant.

---

## 9. Ablations and falsification tests

The core ablations must isolate whether TaskCognition is more than another difficulty router.

1. **Target ablation:** replace paired utility difference with absolute reasoning success.
2. **Absolute policy model:** predict direct success, reasoning success, and cost separately, then select expected utility.
3. **Winner-label ablation:** train a D/R classifier from the cheapest successful or higher-utility policy.
4. **Direct confidence only:** use a charged direct draft and confidence score.
5. **Generic difficulty only:** use length and simple format counts.
6. **No harm head:** route on benefit only.
7. **No conservative bounds:** use calibrated point estimates.
8. **No calibration:** use raw head outputs.
9. **Feature ablation:** embedding only versus observable counts only.
10. **Rollout ablation:** one paired rollout versus repeated paired rollouts.
11. **Reasoning-cap ablation:** 128, 256, and 512 output tokens.
12. **Decoding ablation:** sampled paired seeds versus deterministic temperature zero.
13. **Prompt robustness:** semantics-preserving policy-prompt and answer-tag paraphrases.
14. **Split ablation:** random-instance split versus held-out renderer/template split, explicitly to expose leakage.
15. **No-source-ID audit:** verify that neither explicit nor recoverable dataset identifiers enter training.

Pre-register negative regimes: harm may be too rare to model; direct confidence may match TaskCognition; a paired winner classifier may suffice; calibration may fail under shift; and always-direct may dominate on one or more suites. These are legitimate outcomes, not implementation failures.

---

## 10. Planned result tables and figures

All entries below are **planned and empty** until experiments are executed.

### Table 1 — Frozen policy and permission contract

| Item | Direct | Bounded reasoning | Verified match? |
|---|---|---|---|
| Model/revision | TBD | TBD | TBD |
| Prompt hash | TBD | TBD | TBD |
| Calls/tools/validator | TBD | TBD | TBD |
| Output cap/decoding | TBD | TBD | TBD |
| Parser/scorer | TBD | TBD | TBD |

### Table 2 — Data and split manifest

| Suite | Families | Train | Calibration | ID test | Shift/transfer test | Scorer |
|---|---:|---:|---:|---:|---:|---|
| Reasoning Gym | 6 | 1,200 | 450 | 600 | 300 unseen-renderer | Native verifier |
| LLMThinkBench | 8 | 0 | 0 | 0 | 400 | Exact task evaluator |
| Mind Your Step diagnostic | 2 | 0 | 0 | 0 | 400 | Exact binary label |

### Table 3 — Main in-distribution comparison

| Method | Score ↑ | Selected utility ↑ | Δ vs always-D [95% CI] | Harm ↓ | Rescue ↑ | R rate | Tokens | Latency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Always-D | — | — | reference | — | — | 0 | — | — |
| Always-R | — | — | — | — | — | 1 | — | — |
| Baselines | — | — | — | — | — | — | — | — |
| TaskCognition | — | — | — | — | — | — | — | — |

### Table 4 — Full policy-swap quadrant audit

| Suite/method-selected subset | D✓R✓ | D✓R✗ | D✗R✓ | D✗R✗ | Conditional harm | Oracle regret |
|---|---:|---:|---:|---:|---:|---:|
| Planned rows | — | — | — | — | — | — |

### Table 5 — Shift and transfer

| Method | RG ID | RG unseen renderer | LLMThinkBench | Mind Your Step | Harm-cap violation |
|---|---:|---:|---:|---:|---:|
| Planned rows | — | — | — | — | — |

### Table 6 — Calibration

| Split | Benefit MAE | Benefit coverage | Harm Brier | Harm ECE | Harm slope | Harm interval coverage |
|---|---:|---:|---:|---:|---:|---:|
| Planned rows | — | — | — | — | — | — |

### Table 7 — Ablations

| Variant | Utility Δ | Harm | R rate | Oracle regret | OOD degradation |
|---|---:|---:|---:|---:|---:|
| Full proposed method | — | — | — | — | — |
| Ablations | — | — | — | — | — |

### Planned figures

**Figure 1** will show the architecture in Section 2. **Figure 2** will plot the utility–harm–reasoning-rate frontier against all baselines. **Figure 3** will show reliability plots for benefit and harm in-distribution and under shift. **Figure 4** will show the D/R quadrant distribution and selected-route overlays. **Figure 5**, if space permits, will show per-family answer flips versus the reasoning cap.

---

## 11. Related-work taxonomy and claim boundary

### 11.1 Taxonomy

| Area | Representative work | What is already occupied | TaskCognition’s proposed boundary |
|---|---|---|---|
| Broad paradigm routing | Select-then-Solve [3] | Learned per-task selection among Direct, CoT, tool, planning, reflection, and code policies | Only two matched no-tool policies; paired utility and joint harm audit |
| Direct/non-thinking routing | SynapseRoute [4]; Think When Needed [5]; When to Reason [21] | Binary thinking/non-thinking classification before generation | Not a first router; test a direct-relative, harm-constrained estimand under shift |
| Performance/cost routing | Route to Reason [6] | Predict absolute correctness and length, then optimize quality–cost | Freeze model and compare paired difference/harm against this baseline |
| Confidence cascades | CAR [19]; Confidence-Gated CoT [20] | Generate a direct draft, estimate confidence, and conditionally run reasoning | Primary gate is input-only; cascade cost and information are charged |
| Fast/slow and effort allocation | DynaThink [7]; Ares [22]; Learning When to Plan [2] | Fast/slow selection, per-step reasoning effort, and dynamic planning | One pre-execution single-turn D/R choice; no broad effort-allocation claim |
| Risk-controlled reasoning | Conformal Thinking [14]; Conformal Risk Control [13] | Validation-calibrated stopping or expected-loss control | Target the D-correct/R-wrong route event; make only assumption-bounded guarantees |
| Reasoning-harm characterization | Mind Your Step [8]; When More Is Less [9]; LLMThinkBench [10] | Evidence that CoT/longer reasoning can hurt or waste tokens | Do not claim discovery; use these regimes to audit a router |
| Adaptive decomposition | Select-Then-Decompose [23]; ADaPT [24] | Selection among decomposition approaches and failure-triggered recursive decomposition | No decomposition-menu or agent-planning novelty claim |
| Interface/coupling mechanisms | Divide-and-Conquer noise decomposition [25] | Cross-chunk dependence and aggregation/model noise are formalized | Optional secondary annotations only; no typed-contract headline |
| Foundational framing | Rice’s algorithm selection [11] | Instance-to-algorithm mapping is a classical problem | A constrained two-policy empirical instantiation |

### 11.2 Closest-work paragraph for the manuscript

The closest generic collision is Select-then-Solve, which already demonstrates task-dependent gains and harms across six inference paradigms and learns an embedding router.[3] SynapseRoute is closer still at the binary-control level: it labels paired thinking/non-thinking outcomes and trains a classifier for medical questions.[4] Think When Needed similarly makes a pre-generation Non-Think/Think decision in ranking.[5] Route to Reason already predicts performance and output length for model–strategy pairs under a quality–cost objective.[6] TaskCognition therefore should not claim a new routing architecture. Its proposed distinction is methodological: freeze one model and two matched no-tool policies; estimate paired incremental utility and the direct-correct/reasoning-wrong event; route conservatively from pre-decision information; and audit both policies on every held-out test item. Whether this difference is empirically material is itself the paper’s falsifiable question.

---

## 12. Adversarial novelty audit

### 12.1 Fatal formulations

The following formulations are already occupied and should be deleted wherever they appear:

- “the first learned system to decide when to think or decompose”;
- “the first direct-versus-reasoning router”;
- “the first evidence that overthinking hurts”;
- “the first test-time-compute controller”;
- “the first risk-aware adaptive reasoning system”;
- “the first system to learn when to plan.”

Select-then-Solve, SynapseRoute, Think When Needed, Route to Reason, DynaThink, Learning When to Plan, Ares, CAR, Confidence-Gated CoT, and Conformal Thinking collectively preclude those claims.[2] [3] [4] [5] [6] [7] [14] [19] [20] [22]

### 12.2 Near-fatal method collisions

A binary classifier trained on “which paired mode was correct,” followed by accuracy/token/latency evaluation on one domain, would be materially SynapseRoute.[4] A generic input embedding or intent classifier selecting reasoning would overlap Think When Needed and When to Reason.[5] [21] A model that predicts absolute success and length and selects score-minus-cost would be a fixed-model restriction of Route to Reason.[6] A post-draft confidence gate would be a CAR/Confidence-Gated CoT cascade.[19] [20]

**Required defense:** the final paper must show whether the direct-relative harm head and conservative bound change decisions beyond each of these baselines. Architectural novelty alone is not defensible.

### 12.3 Identification failures reviewers will attack

1. **Unequal permissions.** If reasoning receives tools, retrieval, more calls, validators, retries, reflection, or self-consistency, the result compares policy packages, not visible reasoning.
2. **Free direct preview.** If the gate reads a direct answer without charging it, it receives privileged evidence and undercounts cost.
3. **Template leakage.** Random-instance splitting of procedural tasks can let the gate memorize task identity or renderer cues.
4. **One noisy rollout.** A single stochastic answer can create unstable winner and harm labels. Repeated paired seeds are required, or the labels must be described as realized outcomes.
5. **Metric gaming.** Post-hoc `λ`, `α`, thresholds, or near-zero reasoning coverage can manufacture an apparent win.
6. **Parser artifacts.** Visible reasoning may produce more answer-extraction failures. Report these separately and rerun with a robust, frozen parser sensitivity check.
7. **Native-mode asymmetry.** A model’s thinking and non-thinking modes may have different learned behavior beyond visible trace emission. Conclusions remain policy-relative.
8. **Calibration overclaim.** In-distribution empirical calibration is not OOD safety and does not imply conditional guarantees.
9. **Rare-event collapse.** If D-correct/R-wrong cases are very rare, a harm head may be uninformative. Publish prevalence, precision–recall behavior, and upper bounds.
10. **Dataset recognition.** A pooled three-suite gate can look successful by detecting the benchmark source. Exclude source IDs and report within-suite results.

### 12.4 Adversarial reviewer questions and required answers

**“Is this only SynapseRoute outside medicine?”** The paper must answer with a result showing that paired utility magnitude plus a retained harm event changes routing and improves a preregistered frontier over a faithful SynapseRoute-style winner classifier. If not, concede the collision.

**“Is this only Route to Reason with one model?”** The paper must compare against separate absolute score/cost heads. The residual claim is the value—or lack of value—of direct-relative and joint-harm estimation.

**“Why not just use direct confidence?”** Include several confidence signals and CAR/CGR-style cascades with all preview costs charged. A TaskCognition gain must remain at equal expected cost or equal reasoning rate.

**“Does the gate just recognize datasets?”** Train without dataset identity, use within-suite splits, hold out renderers/templates, and report each suite separately. Do not rely only on pooled accuracy.

**“Is the harm causal?”** Answer no at the cognitive level. It is a paired operational outcome under two declared policy interventions and a fixed randomness protocol.

**“What if the novelty disappears?”** Reframe as a rigorous negative result on the limits of harm-aware routing. Do not add typed contracts, agents, or extra policy arms late in the project.

### 12.5 Final cutoff search

Immediately before submission, repeat searches for “thinking non-thinking router,” “direct vs CoT routing,” “strategy-induced harm,” “counterfactual policy routing,” “when to reason,” and “risk-controlled reasoning.” Several closest works are 2025–2026 preprints, so the novelty assessment is time-sensitive.

---

## 13. Nine-page main-text budget

ICLR 2027 permits at most nine main-text pages at submission; references are excluded and appendices are unlimited. The required AI-use statement also does not count toward the limit.[26]

| Section | Pages | Required content |
|---|---:|---|
| Abstract | 0.25 | Conditional motivation, two policies, paired estimands, proposed evaluation; no result language |
| 1. Introduction | 0.90 | Problem, closest collisions, narrow contribution, three research questions |
| 2. Related Work | 0.80 | Taxonomy: routers, cascades, effort/risk control, harm studies |
| 3. Problem Setup | 0.80 | `π_D`, `π_R`, outcomes, utility, `Δ`, `h`, gate objective, claim boundaries |
| 4. TaskCognition | 1.25 | Architecture figure, heads, calibration, conservative route rule |
| 5. Policies and Audit Protocol | 0.80 | Matched permissions, paired seeds, cost accounting, final-answer scoring |
| 6. Experimental Setup | 1.35 | Three suites, splits, model, baselines, ablations, preregistration |
| 7. Results | 1.45 | Main utility table, D/R quadrant audit, frontiers, shift, calibration, ablations |
| 8. Analysis and Limitations | 0.85 | Error categories, prompt/cap sensitivity, model-relative scope, negative regimes |
| 9. Conclusion | 0.30 | Evidence-bounded takeaway only |
| Reproducibility paragraph | 0.20 | Artifact manifest and locked protocol |
| **Total** | **8.95** | Leaves 0.05 page for layout variance |

Put full prompts, model/server configurations, split seeds, generator parameters, parser code, all `λ/α/B` sensitivities, full per-task tables, raw paired logs, bootstrap and permutation details, additional model replication, ethics statement, and AI-use disclosure after the main text. Reviewers are not required to read the appendix, so the policy contract and main harm audit must stay in the nine pages.

---

## 14. Research questions and preregistered hypotheses

**RQ1 — Paired value:** Does a pre-generation gate trained on paired direct-relative utility improve selected utility over always-direct at a fixed expected-token budget?  
**Proposed H1:** It will improve utility on the Reasoning Gym in-distribution test. **No result is presently available.**

**RQ2 — Harm sensitivity:** Does explicit estimation of `P(D correct,R incorrect|x)` improve the harm–utility frontier over an otherwise matched benefit-only gate, paired winner classifier, direct-confidence cascade, and absolute success/cost router?  
**Proposed H2:** It will reduce selected-route harm at matched utility or increase utility at a fixed harm cap. **No result is presently available.**

**RQ3 — Shift:** Does benefit/harm calibration deteriorate under unseen renderers and external task-family shift, and does conservative routing reduce but not eliminate this deterioration?  
**Proposed H3:** calibration and utility will degrade under shift. **No result is presently available, and no OOD guarantee is claimed.**

**RQ4 — Policy effect heterogeneity:** How often do the four D/R outcome quadrants occur across controllable procedural tasks, routine mathematics, and known harm diagnostics?  
This is descriptive and remains worthwhile even if every learned gate fails.

---

## 15. Reproducibility and claim discipline

Release, subject to project approval, the exact model revision and environment lockfile; hashed prompts; policy wrappers; task-generator commits and configurations; split and seed manifests; frozen parsers and scorers; every raw D/R output; gate features and checkpoints; cost logs; calibration objects; statistical scripts; and empty-to-populated table templates. The anonymous submission must remove identity from both the paper and supplement.[26]

Every conclusion must be qualified as **model-, policy-, prompt-, cap-, scorer-, cost-, and distribution-relative**. A no-tool bounded-CoT result says nothing about retrieval, planning, multi-agent reasoning, reflection, or tool use. “Direct” does not mean cognitively shallow. `H` does not identify why the model failed. Entity popularity or procedural simplicity does not identify pretraining familiarity. A held-out template is a stronger test than a random split but is not proof of deployment robustness.

---

## 16. BibTeX-ready citation metadata

The entries below prioritize official proceedings metadata when available and otherwise identify an arXiv preprint explicitly. Long author lists are shortened with `and others` only where the official record is unusually long; retrieve the full list from the linked primary source before camera-ready submission.

```bibtex
@techreport{rice1975algorithm,
  title        = {The Algorithm Selection Problem},
  author       = {Rice, John R.},
  institution  = {Purdue University, Department of Computer Science},
  number       = {75-152},
  year         = {1975},
  url          = {https://docs.lib.purdue.edu/cstech/99/}
}

@inproceedings{wei2022chain,
  title     = {Chain-of-Thought Prompting Elicits Reasoning in Large Language Models},
  author    = {Wei, Jason and Wang, Xuezhi and Schuurmans, Dale and Bosma, Maarten and Ichter, Brian and Xia, Fei and Chi, Ed and Le, Quoc V. and Zhou, Denny},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {35},
  year      = {2022},
  url       = {https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html},
  doi       = {10.52202/068431-1800}
}

@inproceedings{pan-etal-2024-dynathink,
  title     = {{D}yna{T}hink: Fast or Slow? A Dynamic Decision-Making Framework for Large Language Models},
  author    = {Pan, Jiabao and Zhang, Yan and Zhang, Chen and Liu, Zuozhu and Wang, Hongwei and Li, Haizhou},
  booktitle = {Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing},
  pages     = {14686--14695},
  year      = {2024},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2024.emnlp-main.814/},
  doi       = {10.18653/v1/2024.emnlp-main.814}
}

@inproceedings{prasad-etal-2024-adapt,
  title     = {{AD}a{PT}: As-Needed Decomposition and Planning with Language Models},
  author    = {Prasad, Archiki and Koller, Alexander and Hartmann, Mareike and Clark, Peter and Sabharwal, Ashish and Bansal, Mohit and Khot, Tushar},
  booktitle = {Findings of the Association for Computational Linguistics: NAACL 2024},
  pages     = {4226--4252},
  year      = {2024},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2024.findings-naacl.264/},
  doi       = {10.18653/v1/2024.findings-naacl.264}
}

@article{angelopoulos2024conformal,
  title   = {Conformal Risk Control},
  author  = {Angelopoulos, Anastasios N. and Bates, Stephen and Fisch, Adam and Lei, Lihua and Schuster, Tal},
  journal = {International Conference on Learning Representations},
  year    = {2024},
  eprint  = {2208.02814},
  archivePrefix = {arXiv},
  url     = {https://arxiv.org/abs/2208.02814}
}

@inproceedings{pmlr-v267-liu25t,
  title     = {Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse},
  author    = {Liu, Ryan and Geng, Jiayi and Wu, Addison J. and Sucholutsky, Ilia and Lombrozo, Tania and Griffiths, Thomas L.},
  booktitle = {Proceedings of the 42nd International Conference on Machine Learning},
  pages     = {38489--38517},
  year      = {2025},
  volume    = {267},
  series    = {Proceedings of Machine Learning Research},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v267/liu25t.html}
}

@inproceedings{liu-etal-2025-select-decompose,
  title     = {Select-Then-Decompose: From Empirical Analysis to Adaptive Selection Strategy for Task Decomposition in Large Language Models},
  author    = {Liu, Shuodi and Liu, Yingzhuo and Wang, Zi and Wang, Yusheng and Wu, Huijia and Xiang, Liuyu and He, Zhaofeng},
  booktitle = {Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing},
  pages     = {5454--5477},
  year      = {2025},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2025.emnlp-main.278/},
  doi       = {10.18653/v1/2025.emnlp-main.278}
}

@article{pan2025route,
  title   = {Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection},
  author  = {Pan, Zhihong and Zhang, Kai and Zhao, Yuze and Han, Yupeng},
  journal = {arXiv preprint arXiv:2505.19435},
  year    = {2025},
  url     = {https://arxiv.org/abs/2505.19435}
}

@article{lu2025prolonged,
  title   = {Prolonged Reasoning Is Not All You Need: Certainty-Based Adaptive Routing for Efficient LLM/MLLM Reasoning},
  author  = {Lu, Jinghui and Yu, Haiyang and Xu, Siliang and Ran, Shiwei and Tang, Guozhi and Wang, Siqi and Shan, Bin and Fu, Teng and Feng, Hao and Tang, Jingqun and Wang, Han and Huang, Can},
  journal = {arXiv preprint arXiv:2505.15154},
  year    = {2025},
  url     = {https://arxiv.org/abs/2505.15154}
}

@article{zhang2025synapseroute,
  title   = {SynapseRoute: An Auto-Route Switching Framework on Dual-State Large Language Model},
  author  = {Zhang, Wencheng and Qiao, Shiqin and Luo, Lingjie and Li, Yinfeng and Zheng, Chuanyang and Xu, Qian and Li, Meng and Gui, Yong and He, Yijun and Qiu, Jianing and Hong, Jindong and Sun, Jiankai},
  journal = {arXiv preprint arXiv:2507.02822},
  year    = {2025},
  url     = {https://arxiv.org/abs/2507.02822}
}

@article{stojanovski2025reasoninggym,
  title   = {Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards},
  author  = {Stojanovski, Zafir and Stanley, Oliver and Sharratt, Joe and Jones, Richard and Adefioye, Abdulhakeem and Kaddour, Jean and K{\"o}pf, Andreas},
  journal = {arXiv preprint arXiv:2505.24760},
  year    = {2025},
  url     = {https://arxiv.org/abs/2505.24760}
}

@article{yang2025qwen3,
  title   = {Qwen3 Technical Report},
  author  = {Yang, An and Li, Anfeng and Yang, Baosong and Zhang, Beichen and Hui, Binyuan and others},
  journal = {arXiv preprint arXiv:2505.09388},
  year    = {2025},
  url     = {https://arxiv.org/abs/2505.09388}
}

@article{paglieri2025learning,
  title   = {Learning When to Plan: Efficiently Allocating Test-Time Compute for LLM Agents},
  author  = {Paglieri, Davide and Cupia{\l}, Bart{\l}omiej and Cook, Jonathan and Piterbarg, Ulyana and Tuyls, Jens and Grefenstette, Edward and Foerster, Jakob Nicolaus and Parker-Holder, Jack and Rockt{\"a}schel, Tim},
  journal = {arXiv preprint arXiv:2509.03581},
  year    = {2025},
  url     = {https://arxiv.org/abs/2509.03581}
}

@article{aggarwal2025optimalthinkingbench,
  title   = {OptimalThinkingBench: Evaluating Over and Underthinking in LLMs},
  author  = {Aggarwal, Pranjal and Kim, Seungone and Lanchantin, Jack and Welleck, Sean and Weston, Jason and Kulikov, Ilia and Saha, Swarnadeep},
  journal = {arXiv preprint arXiv:2508.13141},
  year    = {2025},
  url     = {https://arxiv.org/abs/2508.13141}
}

@article{wang2025semantic,
  title   = {When to Reason: Semantic Router for vLLM},
  author  = {Wang, Chen and Liu, Xunzhuo and Liu, Yuhan and Zhu, Yue and Mo, Xiangxi and Jiang, Junchen and Chen, Huamin},
  journal = {arXiv preprint arXiv:2510.08731},
  year    = {2025},
  url     = {https://arxiv.org/abs/2510.08731}
}

@inproceedings{srivastava-etal-2026-llms,
  title     = {Do {LLM}s Overthink Basic Math Reasoning? Benchmarking the Accuracy-Efficiency Tradeoff in Language Models},
  author    = {Srivastava, Gaurav and Hussain, Aafiya Shamshad and Srinivasan, Sriram and Wang, Xuan},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2026},
  pages     = {25784--25826},
  year      = {2026},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2026.findings-acl.1285/},
  doi       = {10.18653/v1/2026.findings-acl.1285}
}

@inproceedings{wu2026more,
  title     = {When More is Less: Understanding Chain-of-Thought Length in LLMs},
  author    = {Wu, Yuyang and Wang, Yifei and Ye, Ziyu and Du, Tianqi and Jegelka, Stefanie and Wang, Yisen},
  booktitle = {International Conference on Learning Representations},
  year      = {2026},
  url       = {https://proceedings.iclr.cc/paper_files/paper/2026/hash/ce916251b4fe04f54f99c8d304d68877-Abstract-Conference.html}
}

@inproceedings{xu2026divide,
  title     = {When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework},
  author    = {Xu, Zach and Zhu, Shang and Wang, Jue and Wang, Junlin and Athiwaratkun, Ben and Wang, Chi and Zou, James Y. and Zhang, Ce},
  booktitle = {International Conference on Learning Representations},
  year      = {2026},
  url       = {https://proceedings.iclr.cc/paper_files/paper/2026/hash/8d260043c9b1f0c0a97d0e1d5c225795-Abstract-Conference.html}
}

@article{guo2026think,
  title   = {Think When Needed: Model-Aware Reasoning Routing for LLM-based Ranking},
  author  = {Guo, Huizhong and Wei, Tianjun and Wang, Dongxia and Du, Yingpeng and Wang, Ziyan and Zhang, Jie and Sun, Zhu},
  journal = {arXiv preprint arXiv:2601.18146},
  year    = {2026},
  note    = {Rendered source contains placeholder venue metadata; cite as arXiv preprint},
  url     = {https://arxiv.org/abs/2601.18146}
}

@article{lewislim2026confidence,
  title   = {Can Confidence Estimates Decide When Chain-of-Thought is Necessary for LLMs?},
  author  = {Lewis-Lim, Samuel and Tan, Xingwei and Zhao, Zhixue and Aletras, Nikolaos},
  journal = {arXiv preprint arXiv:2510.21007},
  year    = {2026},
  url     = {https://arxiv.org/abs/2510.21007}
}

@article{zhou2026select,
  title   = {Select-then-Solve: Paradigm Routing as Inference-Time Optimization for LLM Agents},
  author  = {Zhou, Heng and Tan, Zelin and Zhang, Zhemeng and Fan, Yutao and Lin, Yibing and others},
  journal = {arXiv preprint arXiv:2604.06753},
  year    = {2026},
  url     = {https://arxiv.org/abs/2604.06753}
}

@article{wang2026conformal,
  title   = {Conformal Thinking: Risk Control for Reasoning on a Compute Budget},
  author  = {Wang, Xi and Suresh, Anushri and Zhang, Alvin and More, Rishi and Jurayj, William and Van Durme, Benjamin and Farajtabar, Mehrdad and Khashabi, Daniel and Nalisnick, Eric},
  journal = {arXiv preprint arXiv:2602.03814},
  year    = {2026},
  url     = {https://arxiv.org/abs/2602.03814}
}

@article{yang2026ares,
  title   = {Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents},
  author  = {Yang, Jingbo and Hou, Bairu and Wei, Wei and Bao, Yujia and Chang, Shiyu},
  journal = {arXiv preprint arXiv:2603.07915},
  year    = {2026},
  url     = {https://arxiv.org/abs/2603.07915}
}
```

---

## 17. Manuscript-ready abstract skeleton

> **Proposed abstract; no results claimed.** Explicit reasoning can improve multi-step problem solving, but recent studies also document settings in which longer or elicited reasoning increases cost or reduces accuracy.[8] [9] [10] Existing systems already route among direct, thinking, planning, and tool-using policies.[3] [4] [5] [6] We propose **TaskCognition**, a tightly controlled study of routing between two policies on one frozen model: an answer-only direct policy and a one-call, token-bounded visible-reasoning policy with matched information, tools, decoding, and output constraints. Rather than predicting generic difficulty or absolute reasoning success, the proposed gate estimates the paired utility of replacing direct execution with reasoning and the probability of an observable avoidable-harm event in which direct is correct and reasoning is incorrect. A conservative rule escalates only when a calibrated lower bound on incremental utility is positive and an upper bound on harm is below a predeclared threshold. We will evaluate every route through a complete offline policy swap on Reasoning Gym, LLMThinkBench, and exact-label Mind Your Step diagnostics, with held-out renderers and task families. Planned comparisons include direct-confidence cascades, paired winner classification, and absolute performance/cost routing. The study is designed to determine whether direct-relative harm supervision materially changes the utility–harm–compute frontier; a null result would bound, rather than confirm, the value of this routing objective.

---

## References

[1]: /home/ubuntu/taskcognition_paper_brief.md "TaskCognition ICLR 2027 Paper Brief"
[2]: https://arxiv.org/html/2509.03581v1 "Learning When to Plan: Efficiently Allocating Test-Time Compute for LLM Agents"
[3]: https://arxiv.org/html/2604.06753v1 "Select-then-Solve: Paradigm Routing as Inference-Time Optimization for LLM Agents"
[4]: https://arxiv.org/html/2507.02822v1 "SynapseRoute: An Auto-Route Switching Framework on Dual-State Large Language Model"
[5]: https://arxiv.org/html/2601.18146v1 "Think When Needed: Model-Aware Reasoning Routing for LLM-based Ranking"
[6]: https://arxiv.org/html/2505.19435v1 "Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection"
[7]: https://aclanthology.org/2024.emnlp-main.814/ "DynaThink: Fast or Slow? A Dynamic Decision-Making Framework for Large Language Models"
[8]: https://proceedings.mlr.press/v267/liu25t.html "Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse"
[9]: https://proceedings.iclr.cc/paper_files/paper/2026/hash/ce916251b4fe04f54f99c8d304d68877-Abstract-Conference.html "When More is Less: Understanding Chain-of-Thought Length in LLMs"
[10]: https://aclanthology.org/2026.findings-acl.1285/ "Do LLMs Overthink Basic Math Reasoning? Benchmarking the Accuracy-Efficiency Tradeoff in Language Models"
[11]: https://docs.lib.purdue.edu/cstech/99/ "The Algorithm Selection Problem"
[12]: https://github.com/QwenLM/Qwen3 "Qwen3 official repository and thinking-mode documentation"
[13]: https://arxiv.org/html/2208.02814v2 "Conformal Risk Control"
[14]: https://arxiv.org/html/2602.03814v2 "Conformal Thinking: Risk Control for Reasoning on a Compute Budget"
[15]: https://github.com/open-thought/reasoning-gym "Reasoning Gym official repository"
[16]: https://github.com/JiayiGeng/CoT_overthinking "Mind Your Step official code and data-access repository"
[17]: https://github.com/suzgunmirac/BIG-Bench-Hard "BIG-Bench Hard official repository"
[18]: https://arxiv.org/html/2508.13141v1 "OptimalThinkingBench: Evaluating Over and Underthinking in LLMs"
[19]: https://arxiv.org/html/2505.15154v1 "Prolonged Reasoning Is Not All You Need: Certainty-Based Adaptive Routing for Efficient LLM/MLLM Reasoning"
[20]: https://arxiv.org/html/2510.21007v3 "Can Confidence Estimates Decide When Chain-of-Thought is Necessary for LLMs?"
[21]: https://arxiv.org/html/2510.08731v1 "When to Reason: Semantic Router for vLLM"
[22]: https://arxiv.org/html/2603.07915v1 "Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents"
[23]: https://aclanthology.org/2025.emnlp-main.278/ "Select-Then-Decompose: From Empirical Analysis to Adaptive Selection Strategy for Task Decomposition in Large Language Models"
[24]: https://aclanthology.org/2024.findings-naacl.264/ "ADaPT: As-Needed Decomposition and Planning with Language Models"
[25]: https://proceedings.iclr.cc/paper_files/paper/2026/hash/8d260043c9b1f0c0a97d0e1d5c225795-Abstract-Conference.html "When Does Divide and Conquer Work for Long Context LLM? A Noise Decomposition Framework"
[26]: https://iclr.cc/Conferences/2027/AuthorGuidelines "ICLR 2027 Author Guidelines"
[27]: https://github.com/ctrl-gaurav/LLMThinkBench "LLMThinkBench official repository"
[28]: https://arxiv.org/abs/2505.09388 "Qwen3 Technical Report"
[29]: https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
[30]: /mnt/dfaa80d1-1d03-4580-b1cc-b43f49de5bf1/Research%20ideas/meeting%20notes/meeting_september_18_2026.docx "TaskCognition meeting transcript, 18 September 2026"
[31]: /mnt/dfaa80d1-1d03-4580-b1cc-b43f49de5bf1/Research%20ideas/decomposition_holistic_research_ideas_report.md "Prior decomposition and holistic research ideas report"
