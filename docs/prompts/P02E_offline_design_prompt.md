# Codex handoff: P02E offline denominator and cost-design review

## Authority and stopping point

The coordinator has **accepted the P02D execution checkpoint as completed DEVELOPMENT evidence**, as recorded in the attached `P02D_execution_acceptance_review.md`. Archive that review and its hash without changing historical artifacts. Record a new acceptance/state event using the repository's existing conventions. Preserve the distinction: **P02 is incomplete/unsealed, P03 is unstarted, and the study is unfrozen.**

This prompt authorizes one vertical slice: **P02E OFFLINE DESIGN REVIEW**. Complete the analysis and return `READY_FOR_REVIEW`. Routine offline implementation and necessary analytical checks are authorized. Do not ask again merely to begin this work.

**Zero new model work:** no model loading, embedding/feature forwards, answer generation, GPU training, smoke calls or live retries. The single P02D execution authorization is consumed; never reuse it. Keep dispatch false. Do not fit or calibrate gates, normalize features, run full TRAIN→TUNE→AUDIT→TEST simulations, collect final labels, freeze scientific choices, or begin P03. Analytical calculations on existing DEVELOPMENT data are permitted and must be labeled as such.

Work within the existing implementation repository. Preserve unrelated files, use task-only local commits, and do not push, merge, upload or install new inference infrastructure.

## Read and bind the authority

Read AGENTS.md, the operational protocol, statistical contract, decision register, approved CR01, P02D execution completion and current state. Read the original reference PDF and CR01 manuscript sections needed for the gate, objective, cost and audit; identify discrepancies rather than silently resolving them. Meeting notes and other project proposals are not specifications.

Bind at least:

- P02D v4 plan: `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`.
- Execution ZIP: `8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9`.
- Production report: `9a5f6c7cf713941284b1c125570b3e174c641e685e01284b6bf86f0f95ff4dab`.
- Execution accounting: `0dda412d334389fc5278e8e05c48667a151120f67dbc6d7dfed06ebb4af0ef03`.

Use existing verified records and native source. Do not regenerate or repair any answer. Keep P02A/P02B historical packages distinct; do not silently pool outcome-informed exploratory draws with this prospective tranche. If historical observations help interpretation, report them separately with their package and sampling provenance.

## Deliverable A: reconcile the scientific signal and denominator

Produce a machine-readable table and readable report, one row per input cluster, with family, K, D/R score means, perfect rates, within-input variation, benefit, joint spoilage, direct-redraw spoilage and direct-perfect counts. Preserve all 192 outcomes, 24 input clusters and equal family weights. Verify the published totals and distinguish strict completion from correctness.

Explain these verified facts in simple English:

- D: 30/96 perfect; R: 64/96 perfect. Only 8/24 inputs have any observed D success.
- All 24 empirical harm targets are zero. Positive benefit occurs on 11 inputs, zero benefit on 13, negative benefit on none.
- Selecting observed positive benefit alone retains six D successes across two inputs, with weighted exposure B=0.0625. Always-R has B=0.3125. These are outcome-informed descriptive selections, not candidate gates or population estimates of feasibility.
- All observed scores are binary. Explain what this and the all-zero harm targets do and do not tell us about the proposed target advantage over winner and factorized routers.

For always-D, always-R, observed-positive-benefit selection and the complement of that selection, report selected input count, weighted routing rate, weighted numerator/exposure, raw nested direct successes, families contributing exposure, and Kish weight concentration where defined. Label undefined zero-denominator risks honestly. These four diagnostic rules are fixed by this prompt; do not search for the action vector that makes TaskCognition look best. No gate fitting or outcome-driven threshold search.

Discuss how small K can conceal rare spoilage and how increasing independent inputs differs from increasing repeats on existing inputs. Do not flatten K-squared pairs into independent observations, use a rule-of-three on dependent pairs, or equate Kish concentration with a count of independent successes. Explain why a zero observed harm target provides little evidence for learning the harm screen here, without asserting that the true harm probability is zero.

## Deliverable B: analytical audit-design constraints

Use the current contract algebra exactly; this is an **analytical DEVELOPMENT diagnostic, not an audit or theorem validation**. Do not import or exercise a final audit decision path. P03 retains theorem verification and full-pipeline simulation.

Express dependence on alpha, b_min, independent cluster count n, K, mean/variance of B, score margin and cost support width. Keep unfrozen quantities symbolic where practical. If numerical scenarios are useful, declare the scenario grid and its rationale before computing it, save that declaration, and label every value illustrative/unadopted. Do not select alpha, b_min, delta_score or n to obtain a preferred outcome.

Reproduce these anchors:

1. For B and Z the range-only term is `7*log(40)/(3*(n-1))`; at n=24 it is 0.3742341475. The maximum empirical B available from these rows is 0.3125. Thus these rows cannot pass the specified positive-denominator check for any g, even before adding the variance term.
2. With observed spoilage numerator zero, `Z_i = -alpha*B_i`. Retain the declared Z range `[-alpha, 1-alpha]`; do not shrink its width from 1 to alpha because the sample has zero spoilage. Derive the resulting necessary sample-size condition and clearly distinguish necessary conditions from sufficient passage or power.
3. The Delta range remains `[-1,1]`; zero empirical variance does not erase its finite-sample range term. The cost range requires an independently justified hard bound.
4. No direct routing exposure means undefined conditional spoilage and failed positive b_min adequacy. A failed candidate deploys direct with the gate bypassed; no runtime second answer is allowed.

Do not promote the 24 inputs to an audit, extrapolate a precise power estimate from them, or assert that increasing repeats alone fixes the independent-cluster penalty. If an illustrative future n preserves observed moments, label that assumption; do not duplicate rows and call them new independent evidence.

## Deliverable C: reconcile costs and propose a defensible ledger

Reconcile 193 sessions, 129,371 output tokens, 11,560.2217413 worker seconds and 12,836.8229112 execution-wall seconds. Give a non-overlapping accounting map: measured quantities, nested components, unallocated residuals and unavailable quantities. Explain that conservative worker residency is not pure GPU kernel time. Preserve all collection expenditure, including failures, warm-ups and reporting.

Inspect existing timestamps/resources and source to explain what is measured for loading, feature extraction, generation, validation, scoring, evidence scanning and supervision. Tabulate costs by draw round and mode. The coordinator observed worker-minus-load-minus-generation residuals rising from about 5.9 to 20.5 seconds. Investigate offline; distinguish code-based inference from direct timing evidence. No new runtime benchmarks or production optimization in this checkpoint.

Separate:

- Actual research collection costs, including K repeated draws and integrity machinery.
- The currently measured feature/answer components that might inform deployment.
- Proposed serving arrangements and initialization allocation, which are unmeasured until separately tested.

Compare the protocol-permitted scalar-ledger choices on scientific meaning, completeness, enforceability and required validation. Prioritize a credible local hardware service-time proposal if possible. A token/call reference tariff is an explicit alternative requiring review, not an arbitrary dollar conversion or a way to make an expensive gate free. Never claim actual paid fees from a reference tariff.

For the recommended proposal, define the costed service boundary and one-query path: input-only feature extraction, CPU gate/calibration/dispatch and exactly one selected D/R answer. Include startup, pre-admission attempts, failure/cancellation/cleanup and shared-process allocation where applicable. Treat cached embeddings as collection artifacts, not free live features. A persistent/shared model or prefill reuse is only a proposal; describe mode isolation and tests required for all learned methods. Do not assume the warm 0.05369-second feature measurement is a complete gate cost.

State what analytic hard bounds follow from enforceable controls and what remains unproved. A timeout, observed maximum, reserved budget or hypothetical watchdog does not by itself prove a bound on consumed service time. Do not clip costs or scores. Any overflow or accounting failure needs an honest prospective invalidation policy, not silent exclusion. If a support bound cannot yet be justified, record D08/D09 as unresolved.

Keep the common budget formula `beta = c_D_ref + 0.5*(c_R_ref-c_D_ref)` and explain how references would be obtained under the same declared service policy. Do not freeze beta from collection-worker means by default or inflate it for TaskCognition. Cost depends on which inputs are routed: use per-input selected costs in diagnostics; routing fraction times global mean cost is only a labeled simplifying assumption. Gate cost applies even on queries routed direct while the gate is active.

## Deliverable D: a concrete next-step recommendation

Update the decision ledger with evidence, open questions and proposed resolutions; do not mark unapproved proposals as decisions. Recommend one next step and explain why it is worth its resource cost. The options may be a bounded additional DEVELOPMENT tranche, a necessary serving/cost calibration preflight, or a documented feasibility block. Do not declare the whole study infeasible solely from these tiny cells or revive the removed completion eligibility rule.

If more data is recommended, compare input breadth versus repeat depth and state the scientific question each resolves. Preserve the same six families, native configurations/renderers, package, cap, sampler and strict scoring unless a separately reviewed change is explicitly proposed. No targeting easy cases, dropping failures, or searching for harm-positive cases to bias the primary population. Maintain disjoint DEVELOPMENT identities and independent streams. A fresh broad tranche, more repeats on existing inputs and historical data must remain distinguishable.

Prepare a **proposal only** with exact counts for fresh/repeated inputs, per-mode K, feature forwards/warm-ups, answer calls, maximum tokens, conservative worker/wall/disk ceilings, stop conditions and no-auto-retry semantics. Ground cost estimates in observed measurements; disclose scaling overhead and uncertainty. Include the longer-study resource implications, not just the cheapest next tranche. Do not materialize or execute a new dispatch plan in P02E.

No numerical tolerances, normative risk tolerance, new ledger, serving change or resource spend is adopted by this prompt. Make any required user decision concrete and explain its scientific consequence. Preserve all required comparisons and the primary three-contrast success rule. Jev, live judges, extra checkpoints and cascades remain parked.

## Packaging and acceptance criteria

Use a small coherent set of outputs under `reports/p02e/` plus `reports/phases/P02E_completion.md`:

1. Offline design report, including cluster/denominator and cost tables, limitations and recommendation.
2. Reproducible analysis source, declared analytical scenarios if used, machine-readable outputs and run receipt. Record CPU/wall cost; zero model/GPU work.
3. Next-step proposal with execution explicitly **UNAPPROVED** if it involves model work.
4. A review ZIP, evidence index and external hash receipt. Include changed analysis sources and necessary provenance; reference accepted immutable packet hashes rather than recursively embedding old ZIPs. Verify every indexed file and report the exact count.

Use focused checks for formulas, zero denominators, cost overlap and source bindings. Do not rerun the entire regression suite merely to increase the test count. Do not edit accepted raw evidence, scoring, runner behavior or manuscript conclusions. A factual manuscript issue may be logged for later correction.

Finish with `P02E OFFLINE DESIGN READY_FOR_REVIEW`, the recommendation, unresolved decisions and file paths. State explicitly: dispatch false; zero new model work; P02 incomplete/unsealed; P03 unstarted. The next phase requires a separate coordinator handoff after review.
