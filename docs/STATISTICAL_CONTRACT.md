# Statistical contract and verification

Transcribed from the revised manuscript. P03 must verify derivations, theorem conditions, and numerical conventions before final data. No software test or simulation alone establishes a theorem.

## 1. Unit of analysis and estimators

The unit is the complete input cluster, with K independent D and K independent R draws. If unavoidable shared system failures create a larger unit, resolve the redesign during development; the following formulas cannot be applied unchanged to dependent rows.

```
p_hat_a = sum_k 1{S_ak=1}/K
T_b = mean(S_R) - mean(S_D)
T_h = p_hat_D*(1-p_hat_R)
h_DD_hat = K/(K-1) * p_hat_D*(1-p_hat_D)
d_epsilon_hat = sum_{k,l} 1{S_Dk-S_Rl >= epsilon}/K^2
```

Epsilon is 0.10 and 0.25. K must be at least 2. Cross-pairs overlap: neither K^2 nor K(K-1) is the sample size for confidence bounds. Perfect-to-imperfect targets differ from partial-score declines.

For family-balanced rows, E_w uses exactly 1/6 of each family's mean. Ratios use a ratio of weighted numerator and denominator, not an average of per-family ratios. A zero denominator is `undefined/no exposure`, never silently zero risk. Direct fallback has no routed exposure; report a zero numerator and undefined risk where applicable.

## 2. Audit

For the frozen action g_i and per-input package summaries:

```
B_i = g_i*p_hat_Di
Z_i = g_i*p_hat_Di*(1-p_hat_Ri-alpha)
Delta_i = g_i*(mean_S_Ri-mean_S_Di)
C_i = C_gate_i + (1-g_i)*mean_C_Di + g_i*mean_C_Ri
```

Use complete balanced n rows, n/6 per family. Variance is sample variance with denominator n-1. For each bounded variable T in [a,b]:

```
r_EB(T) = sqrt(2*s_T^2*log(2/gamma)/n)
          + 7*(b-a)*log(2/gamma)/(3*(n-1))
gamma = 0.05
```

Ranges: Z in [-alpha,1-alpha], B in [0,1], Delta in [-1,1], C in [c_min,c_max]. C bounds must be analytically justified under enforced input limits, output cap, gate limits, retry ceiling, and resource rule. Observed pilot minimum/maximum are not hard support bounds. Do not clip out-of-range costs or scores to make the audit pass.

Enable only if all four hold:

```
mean(Z)+r_EB(Z) <= 0
mean(C)+r_EB(C) <= beta
mean(B)-r_EB(B) >= b_min > 0
mean(Delta)-r_EB(Delta) >= 0
```

This is score noninferiority, not test superiority. Keep unrounded values for decisions. Document boundary conventions and numerical tolerance; do not introduce a positive slack that changes the acceptance rule.

Verify the independent/nonidentical bounded-row version of Maurer-Pontil, including the variance normalization and lower-tail application. The balanced family design uses independent rows with different family distributions. The four-component intersection-union claim is per frozen candidate at gamma, not a simultaneous confidence rectangle and not a familywise guarantee over all three methods. No Bonferroni is imposed for this conjunction; do not generalize the guarantee beyond its stated scope.

Audit code checks artifact hashes and row completeness before statistics. A failed/missing/invalid audit forces D and bypasses the gate. An operationally invalid experiment must also be labeled invalid; fallback does not magically repair its scientific evidence. No selection, threshold change, seed search, or increased audit n after looking at audit outcomes.

Adequacy fields: selected input count, weighted routing rate, B mean and lower bound, raw nested direct successes K*sum(g*p_hat_D), and Kish concentration `(sum a_i)^2/sum(a_i^2)` with a_i=g_i*p_hat_Di/n. Kish is weight concentration, not a number of independent successes.

## 3. Final test

All actions derive from audit-selected deployments. Failed methods use D with zero live gate charge. For each comparator m in {always-direct, winner-deploy, factorized-deploy}, compute per-input mean-score difference versus TC-deploy and average with equal family weights.

Bootstrap 10,000 times: sample complete input clusters WITH replacement independently within each family, use the SAME selected indices for every method in a replicate, retain all nested draws, and preserve 1/6 weights. The lower one-sided 95% percentile bound is the frozen 0.05 quantile convention. Do not bootstrap individual draws or flatten cross-pairs. Freeze RNG and interpolation conventions before TEST.

Primary support requires all three lower bounds STRICTLY greater than the development-frozen delta_score >= 0. It is a conjunction, with no Holm correction for this primary all-three claim. Any separately declared nonprimary inferential family uses its prespecified multiplicity rule (the PDF specifies Holm). Bootstrap coverage is asymptotic conditional on frozen deployments, not exact randomization inference.

Handle failed model draws using their frozen valid zero-score rule and retain them in every resample. A score contrast of complete valid rows should remain computable. A programming error, corrupted record, or missing row must fail the computation rather than be imputed as a model failure. Ratio resamples with zero denominators are retained and counted as undefined under a frozen convention; never redraw only unfavorable/undefined replicates.

P00 user clarification (2026-09-28 UTC): model failures and corrupted evidence are different. A recorded model failure receives the frozen score (zero when no valid retainable answer exists) and remains in the input cluster during bootstrapping. Missing or corrupted evidence stops the affected analysis for investigation. Never convert corruption into a zero score, zero an entire bootstrap replicate because one model answer failed, or redraw a replicate to remove failures. This resolves the manuscript's ambiguous “failed resample” wording without implementing bootstrap execution in P00.

## 4. Development simulation and sample design

Use a disjoint high-repeat pilot to estimate realistic joint distributions of features, score draws, correctness, cost, and failures. A proposed starting pilot is 25 inputs/family x 50 draws/package = 15,000 admitted generations; this is a manuscript placeholder and must be budgeted, not automatically launched.

Simulation must include fitting, tuning, one candidate freeze, audit, fallback, and final test. Freezing an oracle gate and simulating only its audit does not validate the full pipeline. Resampling pilot inputs must not leak the same latent identity across a simulated train/tune/audit/test split. With a small pilot, synthetic models for larger n are assumptions; report sensitivity to several plausible feature/outcome/cost relationships and distinguish them from observations.

Include null, useful/safe, harmful, boundary-risk, expensive, low-direct-success, weak-feature, and high-failure scenarios. Preserve within-input stochastic variation and outcome-cost association. Report each method's false enablement, useful enablement, fallback, bounds, conditional power among passes, unconditional power including fallback, and detectable score effects. Include Monte Carlo uncertainty and replication counts. No claim that finite simulations certify gamma control.

Select K, audit n, train/tune/test sizes, b_min, alpha, cost details, and delta_score based on declared scientific goals and available resources. Predefine the search grid/decision criterion before inspecting simulated comparative results; do not choose settings because TC happens to beat the factorized router. Show attainable effects over a resource curve. n=450 is not presumed adequate; the manuscript expressly warns about audit feasibility.

## 5. Independent check examples

Use these as analytical anchors, alongside randomized and adversarial tests:

- K=4, D scores [1,1,1,0], R scores [1,1,0,0]: T_b=-0.25, T_h=0.375, h_DD_hat=0.25. For epsilon 0.10 or 0.25, d_epsilon_hat=6/16=0.375.
- D and R all perfect: benefit=0, harm=0; no reason to pass the strict positive-benefit gate merely because harm is zero.
- g=0 for every row: B=0; candidate fails positive b_min; deployment fallback is direct and routed risk is undefined.
- Two deployments with identical actions on the same draws: every paired score contrast and bootstrap bound is exactly 0. They cannot establish strict superiority at delta_score>=0.
- Constant bounded audit rows: the variance term vanishes but the finite-sample range term does not. Never set the radius to zero.
- If p_D=p_R between 0 and 1, independent redraw spoilage can be positive even when expected benefit is zero. It cannot be called a causal reasoning penalty.
- Imbalanced stored family counts must still yield equal-family reporting, while the primary audit rejects a non-balanced manifest rather than silently changing its theorem inputs.

Analytical tests, pipeline negative controls, and external theorem verification are required before final labels. Retain a short derivation memo with equation-to-code links.
