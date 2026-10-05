# Operational protocol: TaskCognition revised study

Status: active pre-freeze specification `TaskCognition-CR01-2026-10-05-v1`. Authority: original reference PDF plus [approved CR01 adoption](amendments/CR01_2026-10-05_v1.md) and accepted C01-C03. P02 remains incomplete/unsealed. The historical source is preserved; the active revision copy is `paper/cr01-2026-10-05-v1`.

## Scientific question

Does direct supervision on expected native-score benefit and independent-draw perfect-to-imperfect spoilage improve constrained deployment beyond equally resourced winner and factorized outcome routers?

The study is checkpoint-, package-, scorer-, cap-, and distribution-relative. "Overuse" means routing to R when the declared objective would prefer D; it does not establish excessive internal cognition or general harm from reasoning.

## Packages and population

- Frozen answer model: `Qwen/Qwen3-8B`; freeze revision, tokenizer, precision, backend, template, prompts, samplers, and stop rules.
- D: `enable_thinking=False`. R: `enable_thinking=True`.
- Primary sampler for BOTH: sampling enabled; temperature 0.6; top_p 0.95; top_k 20; min_p 0. Pin other effective sampler defaults.
- CR01 fixes the common primary D/R cap at 2,048 total generated tokens, including thinking and final output. Report strict-valid-FINAL completion and failure subtypes in all 12 cells descriptively; no 99% eligibility prerequisite or automatic threshold stop. Keep the exact P02B instruction and effective matched sampler/parser. Historical 1,024 artifacts remain valid under their original identities, never reinterpreted as CR01.
- Six families: `number_sorting`, `number_format`, `letter_counting`, `graph_color`, `shortest_path`, `knights_knaves`. Resolve registry names at a pinned Reasoning Gym commit. Freeze every generator configuration; use the original renderer.
- Equal family weights: E_w[T] = (1/6) sum_f E[T | F=f]. This is a declared balanced target, not a population-frequency estimate.
- Native deterministic score S_a in [0,1]; perfect correctness Y_a = 1{S_a=1}. Do not replace partial scores with exact match. Freeze scorer adapters and precision handling; do not silently round scores to 1.

## Targets and learning

For each input x:

```
p_a(x) = P(S_a = 1 | x)
mu_a(x) = E[S_a | x]
b(x) = mu_R(x) - mu_D(x)
h_ind(x) = p_D(x) * (1 - p_R(x))
```

The D and R draw sets are conditionally independent. Spoilage is not a same-seed transition or the causal effect of revising a correct answer.

Collect K >= 2 draws per package per input:

```
mean_S_a = mean_k S_aik
p_hat_a = mean_k 1{S_aik = 1}
T_b = mean_S_R - mean_S_D
T_h = p_hat_D * (1 - p_hat_R)
W = 1{mean_S_R > mean_S_D}    # ties direct
```

One shared-trunk MLP predicts b_phi and q_phi. Benefit uses squared error; harm uses fractional-label binary log loss. Huber is sensitivity-only. No outcome-dependent class weighting on the harm target. Any fixed family/instance weighting is outcome independent and frozen before labels.

The input is a frozen text embedding plus approved cheap observables: length, numeric-token count, symbolic-operator count, multiple-choice markers, format indicators. No family/dataset ID, latent generator parameters, gold answers, traces, verifier feedback, or answer drafts. Encoder choice, tokenization, truncation, normalization, and cost remain development decisions. Train-fitted transforms must never use TUNE/AUDIT/TEST.

After calibration, TaskCognition routes to R iff `b_cal > tau AND q_cal <= eta`. The q screen is local joint harm, not conditional spoilage `1-p_R`. The rectangular gate is a restricted family, not a globally optimal solution.

## Objective and cost

```
S_g = (1-g) S_D + g S_R
R_spoil(g) = E_w[g h_ind] / E_w[g p_D]  # positive denominator only
maximize E_w[S_g]
subject to E_w[C_g] <= beta AND R_spoil(g) <= alpha
beta = c_D_ref + 0.5 * (c_R_ref - c_D_ref)
```

Use one scalar ledger: a declared monetary token/call tariff OR hardware service time, not duplicate charges for both. Track raw tokens, calls, latency, CPU/GPU work, batching, cache, warm-up, and research expenses separately. Include encoder, features, MLP, calibration, dispatch, and the selected package. Cached offline training embeddings do not eliminate live feature cost. Beta is common and frozen; each method cannot expand it to accommodate its gate.

The deployed cost per query is distinct from the research cost of collecting both packages K times. Do not charge K-fold offline evaluation to the single-call deployment; do not hide it from the research resource report.

## Answer and failure contract

Parse in order: native thinking/final channel separation; one nonempty case-sensitive `<FINAL>...</FINAL>` pair on the final channel with no trailing text under frozen whitespace handling; native syntax adapter and native scorer. A FINAL-looking tag inside the thinking trace is not authoritative. Preserve raw text and token IDs.

Freeze timeout T and maximum pre-admission retry count J. Retry only on logged proof that generation was not admitted; preserve request and stream. Unknown admission is admitted. An admitted timeout, lost response, malformed output, or cap stop has no second generation; score zero if no valid retainable output exists. Never rescue R with D. Preserve partial credit where valid.

## Required comparisons

1. TaskCognition: direct benefit and harm targets, two thresholds.
2. Winner: fractional probability of W via binary log loss, calibrated, single strict threshold.
3. Factorized: p_D, p_R via fractional-label log loss and mu_D, mu_R via squared loss; reconstruct b_F=mu_R-mu_D and h_F=p_D(1-p_R), then use the same benefit/harm threshold family.

All share input information, frozen features, rollout table, trainable parameter budget within frozen tolerance, optimizer/search budget, calibration opportunity, tuning objective, family weights, accounting, single-candidate audit, and fallback. A four-head factorized model is valid across mixed partial-credit families; do not use hidden family identity to choose heads at deployment.

Descriptive references: always-direct, always-reasoning, fixed random allocation, observable-count thresholds, nondeployable family-only allocation, and an optimistic same-rollout oracle. Declare their selection rules before test; label oracle finite-K selection bias. No oracle in confirmatory claims.

## Experimental order and deployment

DEVELOPMENT -> base manifest freeze -> TRAIN -> TUNE candidate freeze -> AUDIT deployment freeze -> TEST.

Train/tune labels may be collected in the same bounded data phase after freeze, but code fitting parameters sees TRAIN only. TUNE is for calibration/selection; never refit on TRAIN+TUNE unless a different protocol is explicitly approved before labels. AUDIT and TEST outcomes remain inaccessible until their stages. Final input IDs/seeds may be committed earlier without revealing outcomes to the learner.

P00 user clarification (2026-09-28 UTC): label evidence kinds are `final_train_labels` for split `TRAIN` and `final_tune_labels` for split `TUNE`. Both require a frozen study manifest before real collection. A mismatch between kind and split is an integrity failure. This documentation/schema clarification does not activate collection in P00.

Each learned method gets one audit. It passes only all four inequalities in the statistical contract. Any failed/missing/mismatched audit invokes direct deployment with the gate bypassed. Audit fallback is a deployment-level decision; runtime R failure is not a fallback opportunity.

On TEST log all frozen method actions before generating answers. Obtain both packages offline using independent K draws for evaluation. These forced calls cannot change any action or become a live cascade.

## Success rule and secondary scope

For m in {always-direct, winner deployment, factorized deployment}, the one-sided 95% stratified paired input-cluster bootstrap lower bound on `score_TC_deploy - score_m_deploy` must be strictly greater than the frozen delta_score >= 0. All three must pass. Use 10,000 resamples and frozen conventions. Audit passage alone is insufficient.

Report direct-direct redraw spoilage, partial-credit declines at epsilon 0.10/0.25, and per-family results. The PDF also plans sampler sensitivity, renderer variants, LLMThinkBench, and an independently generated diagnostic. Their exact availability, license, freeze, and scope belong in P03/P04 before test; never invent or introduce them in response to primary results. External/renderer shifts inherit no audit guarantee. Jev and live judges are not primary requirements.

No outcome here is a proof of universal superiority. An unsuccessful comparison is evidence to report, not authorization to broaden the study.

## CR01 development provenance

P02A/P02B exposed formatting and truncation problems on DEVELOPMENT inputs. The user approved CR01 on 2026-10-05 before any final labels. This outcome-informed amendment concerns bounded answer packages, including compliance and truncation; it does not establish improved native solving or routing. The original rule was not formally rejected. Completion alone cannot reject CR01 eligibility; unresolved freeze fields, invalid scores/costs, inadequate audit denominator bounds and software/evidence incidents still block the relevant action.
