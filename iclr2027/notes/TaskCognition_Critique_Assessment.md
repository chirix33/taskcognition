# TaskCognition Critique Assessment

## Overall conclusion

**The critique is substantially correct, and the proposed study remains worth implementing after major pre-freeze revision.** The viable contribution is narrow: test whether a learned, direct-relative benefit head plus an independent-draw perfect-to-imperfect head improves a constrained choice between **exactly two frozen inference packages** beyond strong, equally audited alternatives. The paper is not a general theory of reasoning harm, not the first thinking/non-thinking router, and not a new certification method. Prior work already covers dynamic thinking-mode routing, outcome/cost routing, and risk-controlled reasoning allocation. The manuscript’s contribution must therefore be earned by the preregistered comparative result rather than by the configuration alone.[1] [2] [3] [4] [5]

The current independent-draw estimand in Eqs. (1)–(2) is mathematically valid. It should be retained, renamed and interpreted more carefully, supplemented by a direct–direct independent-redraw reference, and implemented with explicit finite-\(K\) formulas. The local harm-head threshold in Eq. (5) may also remain, but only as a restricted routing heuristic. It is not a pointwise conditional-spoilage guarantee and does not itself solve the aggregate constrained objective in Eq. (4).

The draft is **not ready for confirmatory implementation**. The blocking defects are operational rather than conceptual: the repository has conflicting specifications; the package cap is selected after rollout labels are generated; the benefit loss does not necessarily elicit the declared conditional mean; the “absolute” baseline lacks the success-probability outputs needed to reproduce the paper’s own harm target; the certificate is underspecified and unsafe for zero observed events; the Kish quantity is mislabeled as an event-count requirement; the cost budget is not common across methods; and the primary inferential comparison does not match the contribution claim. All of these can be corrected without adding a policy or a second gate.

> **Evidence status — unexecuted:** No TaskCognition experiment, certification audit, comparator evaluation, renderer analysis, pilot, power simulation, or Jev integration result has been executed. Every performance statement, pass probability, superiority claim, and planned table entry discussed below is a protocol proposal, not an observed result.

## Point-by-point assessment

| Critique issue | Verdict | Rationale | Exact decision |
|---|---|---|---|
| Contribution, novelty, and title | **Accept with scope** | Sections 1–2 already disclaim invention of routing and broad reasoning harm. SynapseRoute and DynaThink already route between thinking regimes, while Route to Reason predicts option performance and cost.[1] [2] [3] Novelty can only be the empirical value of the paired target and comparative audit. | Keep the current interrogative title, but add one explicit title-scope sentence. Rewrite the contribution paragraph so the target comparison—not held-out certification—is the proposed methodological contribution. |
| Object of study and causal language | **Accept** | The design compares two named Qwen3-8B inference packages, not latent cognition and not the causal effect of exposing a rationale. Section 5 correctly treats native modes as packages; the Qwen model card documents the mode switch and mode-specific recommendations.[6] | Preserve one checkpoint, two policies, and one pre-generation input-only gate. Replace causal verbs such as “caused,” “turned,” or “destroyed” with distributional, package-relative language. |
| Independent-draw spoilage in Eqs. (1)–(2) | **Accept with scope** | \(h_{\mathrm{ind}}(x)=p_D(x)[1-p_R(x)]\) is exactly the cross-package independent-draw perfect-to-imperfect probability. It is deliberately conservative: if both policies succeed with probability 0.8, \(h_{\mathrm{ind}}=0.16\) and \(R_{\mathrm{spoil}}=0.20\). This is not an algebraic error or a same-seed causal flip. | Retain Eqs. (1)–(2). Define independent copies explicitly and call the quantity **independent-draw perfect-to-imperfect spoilage**. State that it is neither a same-seed flip nor an individual causal effect. |
| Direct–direct reference and finite-\(K\) dependence | **Accept with scope** | A direct redraw can disagree with another direct redraw even when reasoning is no worse. The reference isolates that stochastic component, but its excess is not a complete score or causal estimand. Ordered pairs reuse draws and are not independent observations; the instance remains the inferential unit.[12] [13] | Add \(h_{DD}=p_D(1-p_D)\), routed \(R_{DD}\), and \(\Delta_{DD}=R_{\mathrm{spoil}}-R_{DD}\) as descriptive references only. Add the unbiased distinct-draw estimator and explicitly reject \(K^2\) as an inferential sample size. |
| Partial-credit degradation | **Accept** | Perfect-to-imperfect spoilage omits non-perfect score losses. Section 3 acknowledges this, but its \(\epsilon\)-metric does not specify the independent-draw estimator or reporting population. | Define \(d_\epsilon(x)=\Pr(S_D^{(1)}-S_R^{(1)}\ge\epsilon\mid x)\) and its \(K^{-2}\) cross-product estimator. Report expected score change and \(\epsilon\)-degradation descriptively; do not silently add either to the primary risk constraint. |
| Benefit and harm losses in §4.1 | **Accept** | Unqualified Huber loss targets a robust conditional location, not necessarily \(\mathbb E[S_R-S_D\mid X]\). Squared loss elicits the mean. One soft-label log loss on \(\widehat p_D(1-\widehat p_R)\) is proper for the mean harm target, but the reused cross-products are not independent observations.[10] [11] | Use squared loss on \(\bar S_R-\bar S_D\) as primary. Huber may be sensitivity-only unless its scale keeps all feasible residuals in the quadratic region. Use one unweighted soft-label log loss per instance for harm; allow only outcome-independent family/instance weights. |
| Factorized comparator in §6.2 | **Accept** | The present “absolute score/cost router” predicts mean score and cost but cannot reproduce \(p_D(1-p_R)\) on partial-credit tasks. A factorized learner can derive both targets from \(p_D,p_R,\mu_D,\mu_R\), so TaskCognition has no theoretical informational advantage. | Replace the current row with a fully executable **factorized outcome router** that predicts \(p_D,p_R,\mu_D,\mu_R\), forms \(b_F=\mu_R-\mu_D\) and \(h_F=p_D(1-p_R)\), and uses the same gate family, tuning resources, calibration, audit, and fallback. Predict costs only if the policy rule actually uses them. |
| Local \(q\)-threshold versus aggregate risk | **Accept with scope** | \(q(x)=h(x)\) is a local joint-event probability. For \(p_D(x)>0\), pointwise conditional spoilage is \(h(x)/p_D(x)=1-p_R(x)\). Thus \(q\le\eta\) is not a pointwise safety bound. Aggregate tuning and certification can still validate the restricted threshold family. | Keep Eq. (5), but call it a **restricted threshold family** and state that only Eq. (2) is the risk claim. Do not replace it with per-query lower/upper confidence-bound routing. |
| Certification scope and rare events in §4.3 | **Accept** | The current percentile bootstrap is not executable from the text and degenerates when all observed harm values are zero. Holding out a split is a deployment safeguard, not new risk-control methodology. Learn-then-Test and related work already formalize post-selection risk testing.[4] [5] [16] | Rename §4.3 “Held-out deployment audit.” Replace the decision rule with the fixed-candidate, weighted, cluster-level Hoeffding audit specified below. Keep bootstrap intervals descriptive only. State that the audit is empirical and supplies no conformal, pointwise, or distribution-free guarantee. |
| Denominator adequacy and Kish count | **Accept** | \((\sum a_i)^2/\sum a_i^2\) measures weight concentration, not direct-correct events. It can equal 100 when selected direct-success mass is only 20, and the present threshold automatically excludes routing fewer than 100 of 450 certification inputs. | Delete “100 effective selected direct-correct instances.” Require a positive one-sided lower bound \(L_B\ge b_{\min}>0\), with \(b_{\min}\) fixed by prospective simulation. Report selection count, direct-success mass, raw observed successes, and Kish concentration separately. |
| Score condition for enabling deployment | **Accept with scope** | The current certificate covers only spoilage and cost, although the paper’s objective is native score. A gate could pass while lowering score through partial-credit losses. This is not a logical defect if the audit is explicitly feasibility-only, but it conflicts with the current performance-oriented deployment language. | Adopt a score-preserving audit: require \(L_\Delta\ge0\), where \(\Delta=\mathbb E_w[S_g-S_D]\). Call this noninferiority, not superiority. Reserve superiority over baselines for untouched test data. |
| Package/cap sequencing in §5 and Appendix A.2 | **Accept** | Appendix A.2 generates and fits from training rollouts before selecting the cap. Changing a cap changes scores, failures, costs, and all learned targets. Qwen’s published guidance also shows that mode and generation settings are package-defining.[6] [7] | Add a disjoint DEVELOPMENT stage. Freeze the complete packages before every final TRAIN rollout. Use the predeclared 1,024/2,048 cellwise rule below; any package change invalidates and regenerates all rollout-derived labels. |
| Parser, retry, timeout, and cost contract | **Accept** | The two-level outer/native parser is a good start, but Qwen native thinking delimiters must be separated before final-wrapper validation. Unspecified retry and timeout behavior can create hidden resampling, extra calls, or uncharged cost. | Freeze native-channel parsing, strict FINAL parsing, native task scoring, admission, retry, timeout, response retention, and charging rules. Never retry an admitted generation; unknown admission counts as admitted and a missing retainable response scores zero. No automatic direct fallback after a reasoning runtime failure. |
| Primary claim, learned baselines, and inference | **Accept** | Section 6.3 tests only TaskCognition versus always-direct, while §7 claims improvement over winner and absolute routers. Each learned method also needs its own audit/fallback. A sign-flip test is not exact under a zero-mean null without swap exchangeability or sign symmetry.[17] | Define three conjunctive primary contrasts against always-direct, winner, and factorized deployment policies. Audit each learned candidate separately. Use family-stratified paired instance-cluster bootstrap lower bounds; remove the claim that sign flipping is exact. |
| Cascades, family diagnostic, and oracle | **Accept with scope** | A confidence cascade observes a realized direct preview, so its selected population differs from the input-only gate’s population. Family-only allocation is informative but not deployable. The same-rollout maximum is an optimistic empirical ceiling, not a population oracle. | Remove cascades from the primary comparison table. If retained, report them as secondary with a preview-conditional harm estimand and full preview cost. Add a nondeployable family-only reference and relabel the oracle as a same-rollout optimistic empirical ceiling. |
| Dataset design, renderer shift, and diagnostic | **Accept with scope** | Equal family weights define a finite-family target, not a natural deployment distribution. Paired renderings of the same latent problem better isolate surface rendering from difficulty. Reasoning Gym supports procedural instances and verifiers, but that alone does not create a renderer-population sample.[18] Mind Your Step and LLMThinkBench motivate stress tests, not universal harm claims.[8] [9] | State the weighted estimand explicitly and report per-family results. Pair renderer variants by latent problem if a renderer contrast is claimed; otherwise keep them as unpaired fixed-case descriptions. Freeze diagnostic validation criteria before generating final diagnostic test items. |
| Cost budget, workload, and power | **Accept** | The base manifest contains 4,100 instances and \(4{,}100\times2\times5=41{,}000\) answer generations, excluding development, retries, and sensitivities. The unnumbered budget definition immediately after Eq. (4) lets TaskCognition’s gate cost influence \(\beta\), undermining common-budget comparison. Current power planning omits certification selection. | Freeze one exogenous budget shared by all methods, use one nonduplicative scalar ledger, benchmark operational feasibility, and simulate the full TRAIN→TUNE→CERTIFY→TEST policy including direct fallback. |
| Figure and repository consistency | **Accept with scope** | The current 2×2 figure already communicates one gate, two policies, four stages, and fallback. A new main figure is unnecessary. The Evidence Pack conflicts with the TeX on title, per-query bounds, utility, same-seed framing, caps, renderers, and split structure, creating a direct implementation risk. | Keep the existing figure and clarify its caption. Designate `iclr2027/taskcognition.tex` plus one dated manifest as the sole implementation specification. Retain historical notes only under a prominent superseded banner with an incompatibility list. |

## Required manuscript and protocol changes

### P0 — blockers before confirmatory implementation or preregistration

#### P0.1 Establish one source of truth

Designate `iclr2027/taskcognition.tex` and one dated, hash-bound manifest as the sole implementation specification. Mark `iclr2027/notes/TaskCognition_Evidence_Pack.md` **“SUPERSEDED—NOT AN IMPLEMENTATION SPECIFICATION.”** Its banner should link to the current TeX and manifest and list, at minimum, its incompatible recommendations for the title, per-query LCB/UCB gate, utility/same-seed estimand, 256-token cap, renderer allocation, and train/calibration/test split. Keep the file for traceability rather than deleting history.

The manifest must bind the candidate, code, model/tokenizer revision, serving engine, precision and hardware, rendered prompt/template hashes, cap, sampler, parser/scorer, feature pipeline, family weights, \(K\), \(\alpha\), \(\beta\), \(b_{\min}\), confidence level, RNG streams, cost schedule, retry/timeout rule, and direct fallback. Any mismatch or post-freeze change requires fresh independent certification; otherwise deployment is always-direct.

#### P0.2 Freeze both inference packages before generating labels

Insert a **DEVELOPMENT** stage before TRAIN in §5 and Appendix A.2. It must use a disjoint six-family pool and may determine only package validity, cap, repeat allocation, throughput feasibility, and the final manifest. No development output may enter the final rollout table.

Use the following precommitted cap rule. Define \(V_{m,f}(L)\) as a strict valid-final completion for mode \(m\), family \(f\), and cap \(L\). Use 1,024 tokens only if every mode-by-family estimate is at least 0.99. Otherwise test 2,048 and use it only if every cell reaches 0.99. If any cell remains below 0.99, stop the confirmatory implementation before final labels and report the bounded package as infeasible; a larger-cap run may remain a separate development diagnostic. This terminal rule is stricter and clearer than silently adapting the cap after labels exist.

For the controlled primary, apply the thinking sampler to both modes: sampling enabled, temperature 0.6, top-\(p\) 0.95, top-\(k\) 20, and min-\(p\) 0. Retain the model-card-faithful sensitivity with direct 0.7/0.8/20/0 and reasoning 0.6/0.95/20/0. These settings follow the distinction in the pinned Qwen materials, but the primary remains an intentionally controlled package comparison.[6] [7]

Before collection, assert that the pinned engine renders direct with `enable_thinking=false` and reasoning with `enable_thinking=true`. Archive serialized prompts and raw completions. The processing order must be:

1. Native think-delimiter channelization.
2. Strict outer `<FINAL>...</FINAL>` validation on the final channel only.
3. Version-pinned suite-native adapter and scorer.
4. Status and score recording.

A FINAL-like tag inside a reasoning trace is never authoritative. Separately record native-delimiter failure, outer-wrapper failure, native-syntax failure, cap-without-final, completed-native-wrong, valid partial credit, admitted execution/response failure, and success.

Each draw receives one admitted answer generation. Freeze deadline \(T\), maximum pre-admission retries \(J\), and a deterministic RNG stream. Retry only if logs establish that no generation was admitted, using the identical request and stream. Never resample an admitted length stop, malformed output, parser failure, timeout, transport loss, empty response, or wrong answer; unknown admission counts as admitted. Score an admitted request with no retainable response as zero. Charge every dispatched attempt. This preserves the declared two-policy, one-call action space; an automatic direct fallback after a reasoning failure would be a third operational policy and is therefore excluded.

#### P0.3 Make the training targets and estimators exact

Revise §3 and §4.1 to define independent copies \(Y_D^{(1)}\) and \(Y_R^{(1)}\):

\[
h_{\mathrm{ind}}(x)=\Pr\{Y_D^{(1)}=1,Y_R^{(1)}=0\mid X=x\}=p_D(x)[1-p_R(x)].
\]

For instance \(i\), define

\[
\widehat p_{ai}=K^{-1}\sum_{k=1}^{K}Y_{aik},\qquad
\widehat h_{\mathrm{ind},i}=\widehat p_{Di}(1-\widehat p_{Ri})
 =K^{-2}\sum_{k,\ell}Y_{Dik}(1-Y_{Ri\ell}).
\]

Because the direct and reasoning draw sets are independent conditional on the input, this is unbiased for \(h_{\mathrm{ind}}(x_i)\). Its \(K^2\) cross-products are dependent and do not create \(K^2\) inferential units.

Use the instance target \(T_{b,i}=\bar S_{R,i}-\bar S_{D,i}\) and primary squared loss \((b_\phi(X_i)-T_{b,i})^2\). If Huber loss is retained as a sensitivity, state its scale and either enforce a quadratic-region condition or stop claiming that it generally targets the conditional mean.[10]

For harm, use one soft-label log loss per instance:

\[
-\widehat h_{\mathrm{ind},i}\log q_\phi(X_i)
-(1-\widehat h_{\mathrm{ind},i})\log[1-q_\phi(X_i)].
\]

Prevalence may set only a constant coefficient for the whole harm head. Positive/negative or outcome-dependent reweighting changes the elicited probability unless analytically inverted and recalibrated. Report calibration diagnostics on a held-out split without refitting on certification data.[11]

#### P0.4 Replace the incomplete “absolute” baseline with the factorized outcome baseline

In §6.2, Table 1, §7, and the certificate table, define a factorized comparator that predicts

\[
p_D(x),\quad p_R(x),\quad \mu_D(x)=\mathbb E[S_D\mid x],\quad
\mu_R(x)=\mathbb E[S_R\mid x],
\]

then constructs

\[
b_F(x)=\mu_R(x)-\mu_D(x),\qquad h_F(x)=p_D(x)[1-p_R(x)].
\]

For binary-score families, \(\mu_a=p_a\); for partial-credit families both outputs are required. Use proper fractional-label losses for \(p_a\) and squared losses for \(\mu_a\). Give this comparator the same input information, frozen encoder/features, rollout table, train/tune/certify splits, total search budget, calibration opportunities, threshold family, family weights, tuning objective, tie-to-direct rule, all-in cost accounting, and one-candidate audit/fallback. Different output-head counts are permissible because the target factorization requires them, but equalize the total trainable-parameter budget, including heads, or disclose and justify a prespecified negligible tolerance.

The manuscript must state that the direct paired-head approach is being tested for finite-data inductive bias, calibration, or shift behavior. It has **no theoretical information advantage** because \(h\) is algebraically determined by \(p_D,p_R\). Cost heads may be included only if a predeclared routing rule uses them; otherwise remove “cost prediction” from the comparator name and enforce cost through the same tuning and audit used for TaskCognition.

#### P0.5 Replace the certification decision with a zero-event-safe fixed-candidate audit

Rename §4.3 **“Held-out deployment audit.”** Let the six fixed families have \(\pi_f=1/6\), certification counts \(n_f=75\), and weights \(w_{fi}=\pi_f/n_f\). For the one frozen candidate, define

\[
\widehat B=\sum_{f,i}w_{fi}g_i\widehat p_{Di},
\]

\[
\widehat Z=\sum_{f,i}w_{fi}g_i\widehat p_{Di}
(1-\widehat p_{Ri}-\alpha),
\]

\[
\widehat\Delta=\sum_{f,i}w_{fi}g_i(\bar S_{Ri}-\bar S_{Di}),
\]

\[
\widehat C=\sum_{f,i}w_{fi}
\left[C_{\mathrm{gate},i}+(1-g_i)\bar C_{Di}+g_i\bar C_{Ri}\right].
\]

Here \(\mathbb E[Z]=B\{R_{\mathrm{spoil}}-\alpha\}\). This linearization avoids directly certifying a sparse ratio while preserving Eq. (2) whenever \(B>0\).

For a bounded cluster statistic in \([a,b]\), precommit \(\gamma=0.05\) and use

\[
r_{[a,b]}(\gamma)=(b-a)
\sqrt{\frac{\log(1/\gamma)}{2}\sum_{f,i}w_{fi}^{2}}.
\]

Compute

\[
U_Z=\widehat Z+r_{[-\alpha,1-\alpha]}(\gamma),\quad
U_C=\widehat C+r_{[c_{\min},c_{\max}]}(\gamma),
\]

\[
L_B=\widehat B-r_{[0,1]}(\gamma),\quad
L_\Delta=\widehat\Delta-r_{[-1,1]}(\gamma).
\]

Enable the gate only if **all four** conditions hold:

\[
U_Z\le0,\qquad U_C\le\beta,\qquad L_B\ge b_{\min}>0,
\qquad L_\Delta\ge0.
\]

The bounded-mean construction follows Hoeffding’s inequality for independent bounded cluster rows and remains nondegenerate at zero observed harm.[14] The denominator threshold \(b_{\min}\) must be fixed before confirmation through prospective useful/unsafe-scenario simulation; it is a scientific and precision requirement, not a renamed Kish threshold. Cost bounds require a frozen maximum input length, output cap, one-answer-call policy, timeout/retry ceiling, gate charge, and bounded cost schedule. Uncapped latency should remain descriptive unless capped or censored under a separately justified estimand.

This is an intersection-union feasibility test. Because deployment is enabled only when every level-\(\gamma\) component test rejects its component null, the false-enable probability is at most \(\gamma\) under the stated sampling assumptions. Do not apply Bonferroni to this conjunctive pass rule, and do not describe the displayed marginal bounds as simultaneous 95% coverage.[15]

The manuscript should add this sentence in substance:

> This prespecified empirical acceptance test is a deployment safeguard for one tune-frozen candidate. It is not a new certification method and supplies no conformal, pointwise, or distribution-free guarantee.

A different finite-sample, zero-event-safe audit may replace the Hoeffding rule only if it is fully derived for fixed family weights and complete instance clusters, frozen before certification, and shown by prospective simulation to preserve false-enable control. Percentile bootstrap intervals may remain descriptive, with the strata, replicate count, interval construction, RNG seed, and zero-denominator handling predeclared.[4] [14] [16]

#### P0.6 Replace the denominator contract and expand the certificate report

Delete the current requirement for “at least 100 effective selected direct-correct instances.” Report instead:

- selected input count \(N_{\mathrm{sel}}=\sum_i\mathbf 1\{g_i=1\}\) and weighted routing rate;
- \(\widehat B\) and \(L_B\), labeled direct-success mass and its lower bound;
- raw selected direct successes \(M_D=K\sum_i g_i\widehat p_{Di}\), explicitly labeled as nested draws rather than independent instances; and
- \(n_{\mathrm{Kish}}=(\sum_i a_i)^2/\sum_i a_i^2\), with \(a_i=w_i g_i\widehat p_{Di}\), labeled only as weight concentration.

A small or nonpositive \(L_B\) produces an uninformative/default-direct decision even if the Kish value is large.

#### P0.7 Align the confirmatory endpoint with the paper’s claim

Define the primary test universe as the six original-renderer Reasoning Gym test families with fixed weights \(1/6\). For each \(m\in\{\text{always-direct},\text{winner},\text{factorized}\}\), define

\[
\Delta_m=\sum_{f=1}^{6}\frac16\,
\overline{S_{\mathrm{TC,deploy}}-S_{m,\mathrm{deploy}}}^{\,(f)}.
\]

Each learned method must choose one candidate on tuning, receive its own identical held-out audit, and deploy its candidate only on pass; otherwise that method’s deployment policy is direct. Report both the pre-audit candidate and post-audit deployed policy, clearly separated.

Freeze a practically meaningful \(\delta_{\mathrm{score}}\ge0\) before confirmation. Support the primary contribution only if a family-stratified paired instance-cluster bootstrap gives a one-sided 95% lower bound above \(\delta_{\mathrm{score}}\) for **every** \(\Delta_m\). This is another conjunctive claim, so Holm correction is not applied to its three components. Holm remains appropriate for a separately declared family of nonprimary comparisons.

Replace the “10,000-sign-flip paired permutation test” in §6.3. A sign-flip procedure is exact only under the corresponding randomization invariance or paired-difference symmetry, neither of which the manuscript establishes.[17] The proposed bootstrap is asymptotic under independent instances and fixed family strata; describe it as such.

#### P0.8 Use one fixed-family estimand and one common cost budget

Define, throughout §§3, 4.3, 6.3 and Appendix B,

\[
\mathbb E_w[T]=\sum_{f=1}^{6}\frac16\mathbb E[T\mid F=f].
\]

Every score, cost, benefit, spoilage numerator, and spoilage denominator used for tuning, audit, and primary test must apply this operator. Any descriptive bootstrap must resample complete instances within family and recompute numerator and denominator inside each replicate.

Replace the unnumbered budget definition immediately after Eq. (4), which currently includes TaskCognition’s training gate cost in \(\beta\), with an exogenous common budget. A suitable rule is

\[
\beta=c_D^{\mathrm{ref}}+\rho(c_R^{\mathrm{ref}}-c_D^{\mathrm{ref}}),
\qquad \rho=1/2,
\]

where reference package charges are estimated in DEVELOPMENT and frozen before tuning. Every method is judged against this same \(\beta\). Charge the method’s gate, preview/router, all dispatched retry attempts, and selected answer exactly once. Choose either a monetary token/call schedule or a hardware-service-time schedule as the scalar resource measure; do not price the same serving work in both. Continue to report calls, tokens, latency, hardware, batching, concurrency, caching, and warm-up separately.

#### P0.9 Simulate the complete decision pipeline before freezing the manifest

Replace the current one-stage power paragraph with a full-pipeline Monte Carlo plan using only development/training information and prespecified scenario models. Each replicate must simulate disjoint TRAIN, TUNE, CERTIFY, and TEST samples; fit and tune each method; freeze one candidate; apply exactly one audit; fall back to direct on failure; and evaluate the resulting deployment policy.

Report enablement probability, useful-candidate enablement, unsafe-candidate false enablement, \(L_B\) and \(U_Z\) distributions, certificate-width distributions, direct-fallback probability, and test power/MDE both conditional on enablement and unconditionally. Use a disjoint higher-repeat pool, for example 25 inputs per family with 50 draws per policy, to estimate within-input variance and compare repeat-versus-input allocations at fixed compute. This exercise may alter \(K\), counts, caps, or feasibility only before the confirmatory manifest is frozen.

The feasibility ledger must distinguish the base \(4{,}100\times2\times5=41{,}000\) answer generations from development draws, high-repeat draws, retries, comparator-only calls, mode-specific sensitivities, cap sensitivities, cascades, and any replication. This arithmetic is a planned capacity envelope, not an observed cost.

### P1 — required before final freeze, but not reasons to expand the core action space

#### P1.1 Clarify scope in the title, contribution, related work, and figure

Keep the title, then add after the Introduction’s routing boundary:

> In the title, “overuse” is policy-relative shorthand for routing an input to the declared bounded reasoning package when the declared score–cost–spoilage objective would prefer the direct package; it does not attribute excessive internal cognition to the model or claim that reasoning models generally degrade performance.

Revise §1’s contribution paragraph to foreground the comparison:

> The methodological question is whether estimating direct-relative native-score benefit together with independent-draw perfect-to-imperfect spoilage improves a constrained choice between two fixed packages beyond identically resourced winner and factorized outcome routers. The held-out audit is a prespecified deployment safeguard for that frozen choice, not a new certification or risk-control method.

At the end of §2, state that audit passage only authorizes the frozen deployment rule; novelty is evaluated through the preregistered comparison with winner and factorized routers.

Keep Figure 1. Revise its caption to say that deployment calls exactly one package, while the test-only policy-swap audit may run both packages offline after logging the selected action and never changes the gate. Also state that the held-out stage is an empirical acceptance check, not a new risk-control guarantee. No second main architecture figure is needed.

#### P1.2 Add the direct–direct independent-redraw reference

Immediately after Eq. (2), add

\[
h_{DD}(x)=p_D(x)[1-p_D(x)],
\]

\[
R_{DD}(g)=\frac{\mathbb E_w[g(X)h_{DD}(X)]}
{\mathbb E_w[g(X)p_D(X)]},
\]

\[
\Delta_{DD}(g)=R_{\mathrm{spoil}}(g)-R_{DD}(g)
=\frac{\mathbb E_w[g(X)p_D(X)\{p_D(X)-p_R(X)\}]}
{\mathbb E_w[g(X)p_D(X)]}.
\]

For \(K\ge2\), estimate

\[
\widehat h_{DD,i}=\frac{1}{K(K-1)}\sum_{k\ne\ell}
Y_{Dik}(1-Y_{Di\ell})
=\frac{K}{K-1}\widehat p_{Di}(1-\widehat p_{Di}).
\]

This is an unbiased order-two U-statistic for \(p_D(1-p_D)\), but overlapping ordered pairs remain dependent.[12] Call it the **direct–direct independent-redraw baseline**, not “resampling disagreement,” to avoid confusion with bootstrap resampling. Report \(R_{DD}\) and \(\Delta_{DD}\) beside \(R_{\mathrm{spoil}}\), joint mass, rescue masses, and routing rate. They do not alter the primary constraint.

#### P1.3 Make partial-credit diagnostics executable

Define

\[
d_\epsilon(x)=\Pr\{S_D^{(1)}-S_R^{(1)}\ge\epsilon\mid X=x\},
\]

with estimator

\[
\widehat d_{\epsilon,i}=K^{-2}\sum_{k,\ell}
\mathbf 1\{S_{Dik}-S_{Ri\ell}\ge\epsilon\},
\qquad \epsilon\in\{0.10,0.25\}.
\]

Predeclare all-item and routed-subset aggregation. State in §3, §6.3, and Limitations that expected native-score change and \(\epsilon\)-degradation are complementary distributional comparisons. Neither is an individual causal switching effect, and neither is called “spoilage” or added to certification without a new protocol.

#### P1.4 Separate cascades from the core comparison

The cleanest decision is to remove the confidence cascade from the primary Table 1 and retain it as a secondary, separately labeled analysis. If retained, let \((Y_{D0},T)\) be the direct preview and confidence, \(e=e(X,Y_{D0},T)\) the escalation decision, and \(Y_{R1}\) an independent reasoning draw. Report

\[
R_{\mathrm{cas\text{-}preview}}=
\frac{\mathbb E[eY_{D0}(1-Y_{R1})]}{\mathbb E[eY_{D0}]},
\]

when its denominator is positive. Retain confidence and correctness jointly for every preview draw. Charge preview generation, confidence processing, retries, and escalation. Never present this quantity as numerically interchangeable with the input-only \(R_{\mathrm{spoil}}\).

#### P1.5 Improve interpretation without adding deployable policies

Add a nondeployable **family-only allocation reference** and per-family rows for score, cost, routing rate, \(R_{\mathrm{spoil}}\), direct-success mass, and primary score contrasts. It tests whether gains exceed coarse task-family allocation; it does not prove that the learned embedding “identified family” or enter certification.

Rename the current oracle to **same-rollout empirical oracle (optimistic under stochastic finite-\(K\) selection)** and rename oracle regret accordingly. Exclude it from confirmatory claims. A split-draw oracle is optional.

#### P1.6 Pair renderer variants if renderer contrast remains an intended claim

Define each renderer item through a latent problem ID or structured specification. Render 50 of the 100 original-renderer ID-test problems with renderer 2 and the other 50 with renderer 3, keep every rendering of one latent problem in the same split, and validate all renderings against the latent specification and native scorer before model execution. Resample latent-problem clusters for pooled renderer analyses.

If faithful latent-ID pairing cannot be implemented, retain unrelated renderer cases only as unpaired descriptive fixed-case evaluations. Remove language that attributes the difference specifically to rendering. This change is required for a clean renderer contrast but is not a blocker for the narrower original-renderer experiment.

#### P1.7 Freeze the independent diagnostic’s interpretation

Before generating final diagnostic test items, freeze the generator/version and construct-validation criteria. Development results may determine only whether the set is described as construct-validated. They may not select generator variants for a desired degradation pattern. If validation fails, retain the set only as a new procedural diagnostic, not as a replication of Mind Your Step.[8]

#### P1.8 Add the statistical citations and reporting fields

Add citations for U-statistics, cluster resampling, bounded-mean concentration, and intersection-union testing.[12] [13] [14] [15] Expand the certificate table to one row per learned method with candidate hash, \(\widehat B\), \(L_B\), \(\widehat Z\), \(U_Z\), cost estimate/UCB, score estimate/LCB, pass/fail, and deployed action. Expand package audits with mode-by-family counts for accepted generations, retries, transport/timeouts, finish reason, missing final before cap, native delimiter, outer wrapper, native syntax, partial native score, and completed wrong.

### P2 — optional extensions, not prerequisites

A cost-aware Lagrangian comparator is mathematically reasonable but should remain optional because it changes the decision family rather than isolating the value of paired versus factorized supervision. If preregistered before data, it may use

\[
g_{\lambda,\nu}(x)=\mathbf 1\{\widehat b(x)-\lambda\Delta\widehat c(x)
-\nu[\widehat h(x)-\alpha\widehat p_D(x)]>0\},
\]

with nonnegative multipliers selected only on tuning data and the same audit/fallback.

Other optional extensions are a split-draw oracle, a larger-cap diagnostic, a second checkpoint, alternative engines, a population-level renderer study, formal per-family certificates, a new partial-credit safety constraint, an empirical-Bernstein or e-process audit with a valid derivation, Jev-based feature pipelines, and tools or multi-call agents. Each requires a separate frozen design and, where deployable, its own fresh audit. None should be added to rescue an unfavorable core result.

## Declined or narrowed requests

**Replace the title.** Declined. The interrogative title does not itself assert a universal result, and the abstract, §§1–2, and Limitations already narrow the object. The required title-scope sentence is sufficient before results.

**Replace primary spoilage with \(h_{DD}\) or \(h_{\mathrm{ind}}-h_{DD}\).** Declined. That would change the declared safety question and could tolerate substantial absolute perfect-to-imperfect risk. The direct–direct quantity is a descriptive reference only.

**Treat pair cells as independent evidence.** Declined. Neither the \(K^2\) cross-policy cells nor the \(K(K-1)\) direct pairs create additional independent instances. They are within-instance calculations.

**Discard Eq. (5) or replace it with pointwise risk bounds.** Declined. The local screen may remain as a restricted heuristic because the actual aggregate risk is checked after tuning. It must not be described as a pointwise guarantee or as an optimizer of Eq. (4).

**Recast the audit as conformal certification.** Declined. Conformal Risk Control and Conformal Thinking are relevant precedents, but the proposed weighted bounded-mean test is an empirical fixed-candidate deployment audit under declared sampling assumptions, not a conformal or distribution-free method.[4] [5]

**Require a cost-aware Lagrangian rule.** Narrowed to an optional comparator. It is not needed to identify whether paired supervision outperforms factorized supervision under the same threshold family.

**Keep cascades on the same primary frontier.** Declined. A cascade conditions on a realized preview and therefore has a different information set and risk estimand. It may be reported separately with its own metric and complete cost.

**Add policies, tree-of-thought, tools, agents, or a second checkpoint now.** Declined. These additions would dilute and potentially invalidate the confirmatory two-policy, one-input-only-gate question.

**Require simultaneous family-specific safety guarantees.** Declined for the first study. Equal family weighting supports one finite-family aggregate guarantee. Per-family results are required diagnostically; per-family certificates would define a stronger, likely underpowered protocol.

**Require paired renderers for the central in-distribution result.** Narrowed. Pairing is required only for a clean renderer-effect claim. The core original-renderer comparison can proceed without it if shift results remain unpaired descriptive cases.

**Archive all historical notes.** Declined. Preserve traceability, but label incompatible documents as superseded and prevent them from being treated as implementation specifications.

**Create a new primary architecture figure.** Declined. The current 2×2 figure already presents the four stages, one gate, two policies, one deployment answer call, and direct fallback. A caption correction is enough.

## Ordered revision plan

1. **Freeze governance first:** declare the TeX plus a dated hash-bound manifest as the sole specification; mark the Evidence Pack superseded and enumerate conflicts.
2. **Insert DEVELOPMENT before TRAIN:** validate mode rendering, parsers, costs, retries, throughput, and the 1,024/2,048 terminal cap rule on disjoint data.
3. **Rewrite the estimand implementation:** add independent-copy notation, finite-\(K\) estimators, squared benefit loss, one-instance soft-label harm loss, and dependence warnings.
4. **Implement the fair factorized comparator:** predict \(p_D,p_R,\mu_D,\mu_R\); match data, capacity, search, calibration, threshold family, audit, and fallback.
5. **Replace certification:** use the weighted cluster-level \(Z/B/C/\Delta\) audit, \(L_B\ge b_{\min}\), zero-event-safe bounds, score noninferiority, and a complete manifest hash.
6. **Repair the evaluation claim:** make deployed TaskCognition comparisons against always-direct, winner, and factorized routers the conjunctive primary test; remove the unjustified exact sign-flip claim.
7. **Standardize family weighting and cost:** define \(\mathbb E_w\), use one exogenous \(\beta\), and enforce a nonduplicative ledger for every method.
8. **Run only prospective design work:** conduct the high-repeat development study and full-pipeline power/false-enable simulation; freeze \(K\), counts, \(b_{\min}\), \(\delta_{\mathrm{score}}\), and feasibility decisions before final rollouts.
9. **Add P1 interpretation/reporting changes:** title-scope sentence, audit disclaimer, Figure 1 caption, direct–direct reference, \(\epsilon\)-metric formula, family-only diagnostic, oracle relabeling, and expanded audit tables.
10. **Resolve secondary studies:** either pair renderer variants or downgrade them to unpaired fixed cases; move cascades to a separate estimand; freeze the independent diagnostic’s validation rules.
11. **Lock and execute:** generate all final rollout tables anew under the frozen packages, tune once, audit each learned method once, invoke direct fallback on any failure, and access test data only after all preceding artifacts are immutable.

## References

[1]: https://arxiv.org/abs/2507.02822 "SynapseRoute: An Auto-Route Switching Framework on Dual-State Large Language Model"

[2]: https://aclanthology.org/2024.emnlp-main.814/ "DynaThink: Fast or Slow? A Dynamic Decision-Making Framework for Large Language Models"

[3]: https://arxiv.org/abs/2505.19435 "Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection"

[4]: https://openreview.net/forum?id=33XGfHLtZg "Conformal Risk Control"

[5]: https://arxiv.org/abs/2602.03814 "Conformal Thinking: Risk Control for Reasoning on a Compute Budget"

[6]: https://huggingface.co/Qwen/Qwen3-8B "Qwen3-8B Model Card"

[7]: https://qwen.readthedocs.io/en/latest/deployment/vllm.html "Qwen vLLM Deployment Guidance"

[8]: https://proceedings.mlr.press/v267/liu25t.html "Mind Your Step (by Step): Chain-of-Thought Can Reduce Performance on Tasks Where Thinking Makes Humans Worse"

[9]: https://aclanthology.org/2026.findings-acl.1285/ "Do LLMs Overthink Basic Math Reasoning? Benchmarking the Accuracy–Efficiency Tradeoff in Language Models"

[10]: https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full "Robust Estimation of a Location Parameter"

[11]: https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf "Strictly Proper Scoring Rules, Prediction, and Estimation"

[12]: https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-19/issue-3/A-Class-of-Statistics-with-Asymptotically-Normal-Distribution/10.1214/aoms/1177730196.full "A Class of Statistics with Asymptotically Normal Distribution"

[13]: https://academic.oup.com/jrsssb/article/69/3/369/7109361 "Bootstrapping Clustered Data"

[14]: https://www.jstor.org/stable/2282952 "Probability Inequalities for Sums of Bounded Random Variables"

[15]: https://projecteuclid.org/journals/statistical-science/volume-11/issue-4/Bioequivalence-trials-intersection-union-tests-and-equivalence-confidence-sets/10.1214/ss/1032280304.pdf "Bioequivalence Trials, Intersection-Union Tests and Equivalence Confidence Sets"

[16]: https://projecteuclid.org/journals/annals-of-applied-statistics/volume-19/issue-2/Learn-then-test--Calibrating-predictive-algorithms-to-achieve-risk/10.1214/24-AOAS1998.pdf "Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control"

[17]: https://arxiv.org/html/2406.09521 "Randomization Inference"

[18]: https://arxiv.org/abs/2505.24760 "Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards"
