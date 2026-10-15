"""Render offline P02E review tables/proposals from checked analytical outputs."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,time
from p02e_analyze import read,write,sha,ROOT,OUT

start=time.perf_counter();cpu=time.process_time()
rows=read(OUT/'cluster_rows.json')['rows'];rules=read(OUT/'diagnostic_rules.json')['rules']
cost=read(OUT/'cost_reconciliation.json');summary=read(OUT/'summary.json');constraints=read(OUT/'analytical_constraints.json')
verification=read(OUT/'acceptance_verification.json')
def md(path,text):
 with path.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
cluster_table=['| Family / native index | K D/R | Means D/R | Perfect rates D/R | Sample variances D/R | T_b | T_h | D-redraw | D-perfect | Strict D/R |',
 '|---|---|---|---|---|---:|---:|---:|---:|---|']
for c in rows:
 cluster_table.append(f"| {c['family']} / {c['dataset_index']} | 4/4 | {c['mean_D']:g}/{c['mean_R']:g} | {c['perfect_rate_D']:g}/{c['perfect_rate_R']:g} | {c['variance_D']:.6g}/{c['variance_R']:.6g} | {c['benefit']:g} | {c['joint_spoilage']:g} | {c['direct_redraw']:g} | {c['direct_perfect_count']} | {c['strict_final_D']}/{c['strict_final_R']} |")
rule_table=['| Fixed diagnostic rule | Selected / 24 | Routing weight | Numerator H | Exposure B | H/B | Nested D successes | Exposed inputs | Kish concentration | Exposure families |',
 '|---|---:|---:|---:|---:|---|---:|---:|---|---|']
for r in rules:
 rule_table.append(f"| {r['rule']} | {r['selected_input_count']} | {r['weighted_routing_rate']:.6f} | {r['weighted_spoilage_numerator']:g} | {r['weighted_exposure_B']:g} | {'undefined' if r['conditional_spoilage'] is None else '0 (observed)'} | {r['raw_nested_direct_successes']} | {r['selected_inputs_with_direct_success']} | {'undefined' if r['kish_concentration'] is None else format(r['kish_concentration'],'.6f')} | {', '.join(r['families_contributing_exposure']) or 'none'} |")
round_table=['| Round | Mode | Calls | Tokens | Worker mean s | Load mean s | Generation mean s | Residual mean s |',
 '|---:|---|---:|---:|---:|---:|---:|---:|']
for r in cost['round_mode']:
 round_table.append(f"| {r['draw_round']} | {r['mode']} | {r['count']} | {r['output_tokens']} | {r['worker_mean']:.6f} | {r['load_mean']:.6f} | {r['generation_mean']:.6f} | {r['residual_mean']:.6f} |")
proxy_table=['| Rule | Per-input selected answer-worker proxy s | Selected generation component s | Fraction × global means approximation s |',
 '|---|---:|---:|---:|']
for r in rules:
 rho=r['weighted_routing_rate'];simple=(1-rho)*rules[0]['selected_answer_worker_proxy_seconds']+rho*rules[1]['selected_answer_worker_proxy_seconds']
 proxy_table.append(f"| {r['rule']} | {r['selected_answer_worker_proxy_seconds']:.6f} | {r['selected_generation_component_seconds']:.6f} | {simple:.6f} |")
proposal=dict(evidence_kind='development_observation',analysis_kind='proposal_only',status='UNAPPROVED',
 recommendation='Next coordinator handoff: offline cost-boundary/calibration preflight, then separate execution review for the contingent diagnostic below.',
 dispatch_plan_created=False,execution_authorized=False,preflight_model_work=0,
 contingent_calibration=dict(fresh_inputs=0,repeated_P02D_inputs=12,selection='Native indices 0 and 1 in each of six families, fixed by index rather than outcomes; not materialized here.',
  K_per_mode=1,answer_calls_D=12,answer_calls_R=12,total_answer_calls=24,
  feature_forwards=26,charged_feature_warmups=2,measurement_forwards=24,
  feature_positions_max=53248,output_cap=2048,max_output_tokens=49152,
  workers_proposed=24,worker_policy='One cold isolated worker per routed query: load same checkpoint once, fresh input-only decoder forward, CPU dispatcher, exactly one selected answer, safe shutdown. First worker also performs two charged feature warm-ups.',
  serving_change='PROPOSED ONLY; new versioned preflight and independent source/guard review required; never reuse P02D execution authorization.',
  streams='Fresh cost-calibration namespace and one independent stream per input/mode; no P02D stream reuse; exact seeds require later prospective plan.',
  learned_gate='None fitted or calibrated; fixed outcome-independent action used for calibration. Real gate/calibration cost remains unmeasured until architecture/parity review.',
  cumulative_worker_seconds=5400,execution_wall_seconds=7200,evidence_bytes=134217728,
  load_deadline_seconds=150,feature_deadline_seconds=120,answer_deadline_seconds=120,cancellation_grace_seconds=10,cleanup_seconds=30,
  normal_query_admission_reservation_seconds=450,first_query_reservation_seconds=690,
  preadmission_retry_ceiling=0,replacements=0,answer_warmups=0,
  all_ceilings_operational_not_support_bounds=True,
  estimated_worker_seconds_current_allround_proxy=24*summary['allround_answer_worker_mean'],
  estimated_worker_seconds_current_lastround_proxy=24*summary['last_round_answer_worker_mean'],
  estimated_planning_window_minutes=[25,60],window_is_not_confidence_interval=True),
 unchanged=['six families/native default configs/renderers','Qwen3-8B revision','BF16 Windows SDPA MATH','P02B system instruction','native D/R modes','matched sampler','2048 total tokens','strict parser and native scores','feature recipe'],
 open_decisions=['cold isolated all-in service policy and gate/init charge boundary','whether hardware service time admits defensible hard support under explicit platform assumptions','future gate architecture/parity instrumentation','alpha/b_min/beta/delta_score/n/K remain unfrozen','durable backup before final collection'],
 stop_policy='Insufficient reservation, feature invalid/partial/timed out, unsafe cleanup, unresolved admission/process/cost, missing/corrupt evidence or unexpected software error stops; no replay/retry or invented zero for incidents. No outcome-based success stop. Existing failures/costs retained.',
 no_auto_execution=True)
write(OUT/'next_step_proposal.json',proposal)
md(OUT/'next_step_proposal.md',f'''# Proposed next step — UNAPPROVED

Recommend **one offline cost-boundary/calibration preflight** as the next separately authorized slice. It would implement and review instrumentation for a defensible one-query hardware-service ledger before spending on more outcome labels. It would return its own review checkpoint; **zero model work** would be allowed by that preflight. P02E has not implemented it or materialized any new request, seed or dispatch schedule.

The concrete target for that preflight is the following **contingent calibration diagnostic**, requiring separate source/plan review and explicit execution approval. This is a resource proposal, not an execution request already granted and not a larger study.

| Proposed diagnostic field | Exact proposal |
|---|---|
| Fresh inputs | 0 |
| Existing inputs | 12: native indices 0 and 1 in each family from P02D, selected by index without outcome screening |
| Repeats | K=1 per mode on each selected input; 12 D + 12 R = **24 new independent calls** |
| Feature forwards | **26**, including 2 charged warm-ups on the first two index-selected inputs plus one live feature pass before each of 24 answer calls |
| Feature input positions | At most 26 × 2,048 = **53,248** |
| Answer cap / total reservation | 2,048 total tokens / **49,152** tokens |
| Workers | 24 sequential isolated cold workers; each loads once, extracts input-only features, uses a fixed predeclared mode, generates one answer, and stops; the first additionally performs both warm-ups |
| Worker / wall ceilings | **90 minutes / 120 minutes** |
| Evidence ceiling | **128 MiB**, including vectors and verified local review packet |
| Deadlines and reservation | Load 150 s, feature 120 s, generation 120 s, cancellation grace 10 s, cleanup 30 s; reserve 450 s for an ordinary query and 690 s for the first with two warm-ups |
| Retry/replacement / answer warm-up | J=0 / none / none |

The reservation contains headroom but is not a proven worst-case stopping bound; measured overshoot remains charged. Before each admission reserve the whole next query, token cap and evidence headroom; if unavailable, stop with partial evidence. The total budget need not accommodate every query at every deadline. No request after a partial/invalid feature pass, unsafe cleanup, corruption or unresolved process/cost state. A known answer failure remains a failure under the unchanged strict scoring rule. Software/evidence failures remain unscored and stop. No replay, resumption of consumed/unknown slots, replacement or automatic budget extension; a separate one-invocation authorization must bind a new reviewed plan.

This proposal uses the same cached checkpoint, tokenizer, precision/backend, native questions/default configs, P02B instruction, sampler, 2,048 cap, parser/scorer and feature recipe. It proposes a **new query lifecycle**, not a model or scientific-package improvement: the raw-question feature pass and chosen answer share the one cold load within the query, with **no KV/prefill reuse**, no answer preview and a full RNG reseed before the sole answer. This path does not exist as an authorized runner now. Preflight must check state isolation, fresh masks/IDs, seeds, no past keys, mode serialization and failure propagation for all learned-method interfaces. Existing P02D source and authorization remain closed.

No learned gate or normalization is fitted. A fixed predeclared D/R action measures the service skeleton only; it cannot measure a future learned MLP/calibrator. An architecture/parameter-parity decision and CPU-only gate-cost checks would remain necessary before an all-in deployment reference. The real gate charge must be added to every active-gate query, even a D-routed query. An untrained synthetic head could be specified for a future cost-only check but is **not chosen or benchmarked here**.

Existing collection-worker means project approximately **{24*summary['allround_answer_worker_mean']/60:.1f} minutes** for 24 balanced calls; using the last round gives **{24*summary['last_round_answer_worker_mean']/60:.1f} minutes**. A **25–60 minute planning window** is deliberately broad, not a confidence interval or hard support bound. New instrumentation/lifecycle may add overhead; the old growing ledger also makes linear extrapolation unreliable. Feature arithmetic (26 warm-style passes) is roughly 1.4 seconds plus cold/first-pass effects, not an all-in gate forecast. Initialization is already substantial inside the worker proxy and must not be added twice. Expect roughly 5–20 MiB of raw plus packet evidence by current record sizes, subject to the 128 MiB operational ceiling. No fee or tariff is assumed. CPU preparation/reporting is separate and must be recorded.

Why this is worth doing first: another large label tranche cannot establish the missing cost support, and the present 5.9→20.5 second residual drift makes collection-worker means unsuitable as frozen deployment references. An instrumented boundary can separate mandatory serving work from growing research integrity machinery. It still cannot prove an OS/GPU termination guarantee from a successful short run. If no credible hardware support argument survives preflight, return a documented D08/D09 block and an explicit reference-tariff alternative for review rather than spending on this contingent live diagnostic.

Breadth versus depth remains a separate later decision. At equal **192-call** cost, 24 fresh inputs (four/family) at K=4 add 24 new input clusters; four extra draws/mode on all existing 24 keep n=24 and yield K=8 for those same inputs. The first probes population heterogeneity/direct-success exposure; the second reduces within-input noise and can expose rare failures on those inputs. Neither guarantees harm-positive observations. Current answer-worker arithmetic is about 3.20 hours at all-round means or 3.55 hours at last-round means, before new feature/supervision overhead. **Neither option is proposed for execution now.** A future fresh pool needs disjoint deterministic identities and original native selection, with no hunt for easy or harm-positive inputs; repeated/current/historical pools stay separately labeled.

Longer-study costs are consequential. With manuscript placeholders of 2,250 TRAIN/TUNE/TEST inputs plus n audit inputs, n=1,200 and K=4 already imply 27,600 answers and 56,524,800 reserved tokens: about **459–510 worker hours** under simplistic all-round/late-round proxies, excluding features, fitting, simulations, additional supervision and backup. n=6,000 gives 66,000 calls and roughly **1,099–1,219 hours**; K=8 doubles answer collection. The historical 15,000-call high-repeat suggestion alone is roughly 250–277 worker hours at these proxies and remains unapproved. Even n=450 does not establish adequacy. Full illustrative rows are in `longer_study_resource_scenarios.csv`; these are not precise forecasts or independently sampled evidence. At current total-evidence-per-call arithmetic, 27,600 calls would be about 3.46 GB including local packet copies, but growing ledgers/vectors can change this materially; model/environment, additional copies and final capacity are extra. Durable off-machine backup must be reviewed before irreplaceable final collection. No purchase or upload is requested for this offline checkpoint.

Required review decisions are concrete: whether to develop the cold isolated one-query service boundary; what platform assumptions could justify service-time support (or whether an explicitly priced tariff is scientifically acceptable instead); and how to define gate/init/reference charges consistently for TC, winner and factorized methods. Alpha, b_min, beta, delta_score, final n/K and resource commitments remain unadopted. A later live approval must bind a new immutable plan; it cannot reuse the consumed P02D approval.
''')
md(OUT/'offline_design_report.md',f'''# P02E offline denominator and cost-design review

**P02E OFFLINE DESIGN READY_FOR_REVIEW.** Analytical DEVELOPMENT review only: zero new model loads, feature forwards, answers, GPU work, gate fits, normalizer fits, simulations or final labels. Dispatch is false; P02 incomplete/unsealed, P03 unstarted, study unfrozen.

## Authority and evidence

The user conveyed acceptance of the P02D execution on 2026-10-15 (America/Chicago). The archived review and its SHA-256 are in `provenance/` and `acceptance_verification.json`; event 023 records acceptance once and activates only this offline slice. Actual workstation timestamps are separate UTC records. The coordinator's checks were offline and do not independently reproduce Windows/GPU behavior or establish independence merely from different seeds. No new execution authorization exists. The old P02D one-invocation authorization is consumed.

Bound plan `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`; execution ZIP `8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9`; production report `9a5f6c7cf713941284b1c125570b3e174c641e685e01284b6bf86f0f95ff4dab`; accounting `0dda412d334389fc5278e8e05c48667a151120f67dbc6d7dfed06ebb4af0ef03`. All **8,997 indexed files** matched both ZIP and current bytes before state changes. Analysis subsequently bound 7,837 input/report/resource/ledger records and verified the 7,257-event chain. No answer was regenerated, decoded differently, repaired or rescored. Machine-readable cluster and diagnostic tables contain exact values; readable decimals below are display rounding only.

P02A/P02B contribute no rows or moments to this analysis. Their outcome-informed development and CR01 provenance remain separate from this predeclared P02D tranche. Historical totals 75 generations / 40,555 tokens (including P01's separate deliberate interruption) remain untouched; P02D adds 192 / 129,371. None are final labels.

## A. Signal and denominator reconciliation

There are 24 independent-input **design units**, four per family with K=4 D and K=4 R draws; unique streams are recorded, not empirical proof of independence. Weight each family 1/6 and its four inputs 1/4, hence each row 1/24. All 192 outcomes and all zeros are retained. Strict FINAL counts are **66/96 D and 64/96 R**; perfect counts are **30/96 D and 64/96 R**. A completed strict answer can still be wrong: 36 strict D outputs were not perfect. This is package-relative scoring including compliance/truncation, not an isolated native-solving claim. No partial score appeared, although the unchanged native scorers allow partial credit.

{chr(10).join(cluster_table)}

`cluster_rows.json`/`.csv` preserve full input IDs, score lists and precision. There are **11 positive-benefit, 13 zero-benefit and no negative-benefit inputs**. All **24 T_h values are zero**. D succeeds at least once on only **8/24 inputs**, with 16/30 nested successes in number_format; graph_color and shortest_path have no observed D success. The direct-redraw diagnostic is 0.25 on letter_counting index 3 and knights_knaves index 2; other rows are zero. Both partial-decline diagnostics are zero everywhere. These finite-K estimates do not establish population absence of harm.

The four rules below were fixed by the user prompt. Positive-benefit and complement use observed outcomes and are **nondeployable outcome-informed descriptions**, not fitted candidates or population feasibility estimates. No other action vector or threshold was searched. For B_i=g_i p̂_Di and H_i=g_i T_hi, weighted numerator/exposure are sums with row weight 1/24; risk is their ratio, not an average of family ratios.

{chr(10).join(rule_table)}

Positive-benefit selection keeps six D successes from just **two** inputs (letter_counting index 3 and knights_knaves index 2), giving B=(0.75+0.75)/24=0.0625. Always-R has B=0.3125; its additional exposure largely comes from benefit ties. The complement carries 24 successes across six inputs and B=0.25 but has zero observed score benefit. This is a tension between useful reasoning and denominator precision, not an instruction to route unnecessary ties to manufacture exposure. The original objective/constraints and all comparator rules remain unchanged.

Kish=(Σa_i)²/Σa_i², a_i=g_i p̂_Di/24, measures **weight concentration**, not independent successful instances. Always-D has no R exposure: its conditional spoilage and Kish are undefined, not zero risk. As a candidate it cannot satisfy positive b_min; as fallback it is the specified gate-bypassing deployment, with no second answer after an R failure.

Because every observed S is binary, μ̂_a=p̂_a here. The factorized targets recover both T_b and T_h exactly; TC gains no information unavailable to that required comparator. Winner labels are 11 ones and 13 zeros, discarding benefit magnitude (0.25, 0.5 or 1), but this table cannot demonstrate that learning magnitude generalizes better. With all harm labels zero, a harm loss supplies no positive example of where the harm screen should activate. Shared representations or calibration do not create missing evidence. Do not fit a gate or infer superiority from the observed R advantage. The all-three final contrasts against always-D, winner deployment and factorized deployment remain required.

For hypothetical fixed input probabilities and independent draws, P(T̂_h=0)=(1-p_D)^K+p_R^K-(1-p_D)^K p_R^K: either no D success or all R successes. In the **predeclared illustrative**, unadopted p_D=0.5, p_R=0.95 example, true independent-draw harm is 0.025 yet K=4 gives an 82.61% chance of a zero empirical harm target. The saved grid shows K=8 and 16 as well, without fitting probabilities from these rows. This is algebra, not a confidence bound or a rule-of-three on dependent cross-pairs. More repeats reduce conditional noise and increase detection opportunities on existing inputs; more independent inputs explore heterogeneity and increase n. K² overlapping pairs do neither by themselves.

## B. Analytical audit-design constraints — not an AUDIT or theorem check

Use the current contract exactly, with L=ln(40), A=7L/3, q_n=A/(n−1), and sample variance denominator n−1:

```text
r(T) = sqrt(2 s_T² L / n) + width(T) q_n
B = g p̂_D; H = g p̂_D(1−p̂_R); Z = H−alpha B
Delta = g(μ̂_R−μ̂_D)
B lower expression = mean(B) − sqrt(2 s_B² L/n) − q_n
Z upper expression = mean(H) − alpha mean(B) + sqrt(2 s_Z² L/n) + q_n
Delta lower expression = mean(Delta) − sqrt(2 s_Delta² L/n) − 2q_n
Cost upper expression = mean(C) + sqrt(2 s_C² L/n) + W_C q_n
```

Widths are **B=1, Z=1, Delta=2**. W_C=c_max−c_min needs an independently justified hard support. This code evaluates symbolic/numerical expressions only and never imports or calls a final audit decision path. P03 retains theorem verification (including independent/nonidentical cluster assumptions/constants) and full-pipeline simulation. No candidate, audit, deployment or gate acceptance is produced.

At n=24, q_n=**0.3742341475188051**. The largest observed B achievable from these rows under any 0≤g≤1 is 0.3125, so even the variance-free upper envelope for its lower bound is **−0.06173414751880513**. It cannot reach any b_min>0. This proves an algebraic limitation of these 24 descriptive rows under the specified formula, not whole-study infeasibility or a formal audit result. No arbitrary action search is needed for this argument.

With observed H_i=0, Z_i=−alpha B_i and s_Z²=alpha² s_B². For alpha>0, the zero-harm expression requires

```text
mean(B) >= sqrt(2 s_B² L/n) + A/[alpha(n−1)].
Necessary (not sufficient): n >= 1 + A/[alpha mean(B)].
Denominator necessary: mean(B)>b_min and n >= 1 + A/[mean(B)−b_min].
```

The variance terms still have to fit, along with score and cost constraints. At alpha=0 no finite n can remove the positive range term even with empirical H=0. At B=0 the conditional risk is undefined and positive-denominator adequacy fails. **Never reduce Z width to alpha** because the sample contains no harm. Future H may be positive; generally s_Z²=s_H²+alpha²s_B²−2alpha Cov(H,B), so the zero-harm algebra need not describe future data.

The scenario declaration was saved and hashed before computing all combinations: n∈{{24,120,450,1200,2400,6000,15000}}, alpha∈{{0.01,0.05,0.10}}, b_min∈{{0.01,0.05}}, four fixed rules. Every scenario is illustrative/unadopted; none selects a tolerance or a favored result. Future-n expressions hold observed means/sample variances fixed as an explicit assumption; rows are not duplicated and labeled new evidence. Range-only balanced-n necessary conditions for alpha=0.05 are **552** at B=0.3125 and **2,760** at B=0.0625. At alpha=0.01 they become 2,760 and 13,776; at alpha=0.10, 282 and 1,380. These ignore variance, cost, score and randomness of future moments, so they are neither recommended n nor passage/power estimates. All scenarios and necessary bounds are retained in `analytical_scenarios.csv` and `analytical_constraints.json`.

For Delta, even a zero empirical variance leaves 2q_n. A zero observed score margin, as in always-D or the complement, gives a negative lower expression for every finite n under unchanged moments. Audit score noninferiority uses margin zero; the separate test threshold delta_score≥0 remains symbolic/unfrozen and requires three superiority contrasts. For cost, write margin M_C=beta−mean(C); a necessary condition with M_C>0 is n≥1+A W_C/M_C, before the variance term. Unknown W_C means no valid numerical audit-cost radius can be supplied.

For a future fixed input-only g, Var(B̂)=Var_X(g p_D)+E_X[g p_D(1−p_D)/K]. Likewise Var(Deltâ)=Var_X(g b)+E_X[g(Var(S_D|X)+Var(S_R|X))/K] under independent D/R draws. These explain K's noise role while retaining between-input variation and the n penalty. They do not license applying a frozen-policy confidence guarantee to our outcome-selected diagnostic rules. Repeats alone cannot change n=24 into a larger independent-cluster denominator.

## C. Cost reconciliation and measurement boundaries

All **193 sessions, 129,371 tokens, 11,560.2217413 residency seconds and 12,836.8229112 execution-wall seconds** reconcile. All 192 answer failures/successes, 50 feature passes including two warm-ups and their overhead remain charged. Unknown tokens/process cost are zero in this completed run; reserved output was 393,216, not generated tokens. No clipping or dropped expenditure.

| Non-overlapping execution-wall partition | Seconds | Meaning |
|---|---:|---|
| Recorded load components | 3273.983664200 | Includes cache hashing/import/load/device/tokenizer/sync inside each loader timer |
| Recorded generation + feature forwards | 5589.179833700 | Generation 5586.079329200 plus all feature forwards 3.100504500 |
| Recorded CPU feature processing | 0.034642800 | Input validation/vector transfer/gate-vector checks; no learned gate |
| Final cleanup components | 0.061383700 | Final kill/wait/close block only; normal finish handshake also has other accounting locations |
| Unallocated within recorded residency | 2696.962216900 | Difference, not a separately profiled operation |
| Outside residency but inside execution wall | 1276.601169900 | Difference, including inter-session/terminal supervisor work; not idle GPU time by definition |
| **Execution wall total** | **12836.822911200** | Sum of the six disjoint buckets |

The first five sum to the residency measure. GPU synchronization ({cost['nested_detail']['answer_sync_seconds_in_generation']:.10f} seconds across answers, exact sum in the JSON) is nested in generation, never added again. The feature session total 52.8643334 includes cold load 20.0065404, all 50 forwards 3.1005045, CPU feature 0.0346428, cleanup and residual. The 48 non-warm-up forwards average 0.05368644 seconds; that is neither total feature service nor total gate cost. Repeated vectors are repeated measurements, not independent inputs.

Offline P02D reporting additionally cost 30.7702649 wall / 30.703125 process-CPU seconds; packaging cost 28.8920755 / 28.53125 seconds. These follow execution, so add their wall durations only when describing the measured research workflow, never to worker residency. Command-wrapper wall overlaps supervisor wall; only its approximately 0.1798385-second difference is additional. Prior preparation, manual report preparation and some independent verification were not comprehensively CPU-profiled; their known command records remain preserved and unknown portions are not assigned zero. P02E's own CPU/wall receipts are separate. No paid charge is inferred.

{chr(10).join(round_table)}

Residual means rise **5.911198 → 12.014805 → 17.182749 → 20.460017 seconds**, for all modes within each round. Load means stay around 16.9–17.1 seconds while generation depends on mode/outputs. Recorded UTC start-to-admission intervals rise from 20.35 to 28.57 seconds and result-to-session-end from 1.59 to 4.40 seconds. These are event-publication intervals, not a profiler: timestamps are assigned after ledger scanning, and monotonic residency boundaries differ. Exact per-session components/intervals and ledger-prefix sizes are in `cost_sessions.csv`; round/mode totals in `cost_round_mode.csv`.

Source inspection of hash-bound code explains plausible contributors, **not causal time allocation**:

- `p02d_ledger.py:13` scans and verifies the entire committed ledger and referenced results/resources; `append` at line 79 calls that scan before each event. Dispatch/recover and every heartbeat therefore revisit growing history. Child scans occur before its loader timer and again after admission (`p02d_worker.py:83,107`).
- The supervisor starts its residency timer before envelope checks/session-start/dispatch and process creation (`p02d_runner.py:85` onward). It is a conservative session interval, not exact child lifetime or pure GPU busy time. `tick` recursively enumerates evidence and can append heartbeats while generation is active. These operations can overlap generation; adding their guessed cost would double count.
- Worker load timing begins only after authorization/source verification and initial ledger scan. Generation timing ends **before** decoding, native entry regeneration, strict parsing and scoring (`p02d_worker.py:56–67`); those costs fall into unallocated residency. Parent result validation and IPC also have no individual timers.
- Residency elapsed is captured at `p02d_runner.py:162` **before** final evidence re-scan/result validation and resource/session-end publication. Subsequent scans and inter-worker authorization/recovery contribute outside residency but inside execution wall. Native scorer, validation, filesystem enumeration and ledger verification cannot be separately quantified from current records. Existing read-only progress scans could also contend for CPU/storage; no instrumentation isolates them.

Thus repeated full-prefix reads have increasing work with history and are consistent with drift; hardware scheduling, caches, filesystem/antivirus effects and other overhead remain unseparated. No benchmark or optimization was run. No timer subtraction is a pure inference-kernel measurement. This is a factual boundary clarification of earlier shorthand “worker lifetime,” not a change to accepted numbers or their cost-once policy.

## Scalar ledger options and proposal

| Option permitted by protocol | Scientific meaning | Completeness / enforceability | Required review/validation |
|---|---|---|---|
| **Local all-in hardware service seconds (preferred conditional proposal)** | Resource occupancy/latency of the declared workstation serving policy | Covers cold start, CPU and GPU path, failed attempts, response and safe stop; shared-work allocation must be explicit. Current operational timers do not prove bounded support. | Precisely instrument one-query boundary; define platform assumptions and hard-stop/accounting feasibility, then parity and reference calibration |
| Explicit token/call monetary reference tariff | Utility under a declared price schedule, not actual hardware-time optimality or paid fees | Can be algebraically bounded when every bounded operation/attempt, gate and initialization is priced; omissions make it invalid. Rates cannot be selected to subsidize TC. | Review rate provenance and units, non-overlapping bundles, count ceilings, failure/overflow billing; adopt before references/tuning |

Recommend defining a **cold isolated one-query service boundary** from first charged validation/admission attempt through safe process stop and mandatory response/bookkeeping. Within one load: original-text tokenization/input-only decoder features, cheap observables, CPU learned head/calibration and dispatch, exactly one native D/R generation, strict output handling, cancellation/cleanup. There is no answer preview, no second answer, no KV reuse and no free feature pass on a query routed D. Gold/native evaluation and growing research archival scans are not needed to serve a query; if excluded from the serving metric they remain fully counted as research collection, with mandatory serving integrity work kept inside. This boundary is **proposed**, not implemented or adopted. CPU gate dimensions/calibration remain unfrozen; a fixed dispatcher diagnostic cannot replace their cost.

Cold per-query allocation is initially more defensible than assuming free initialization: all startup belongs to that query, including failed pre-admission attempts. Persistent/shared-model service or prefill reuse is only an alternative proposal. It would need a fixed session size, start/idle/restart/cleanup allocation, handling for partially used sessions, mode/RNG/cache isolation and identical opportunity/accounting for all three learned methods. Never add two cold loads when one shared load is the declared physical work; never divide by an imagined future number of queries to make startup vanish.

Current controls bound discrete counts (J=0, one selected answer, 2,048 new tokens, approved input ceilings, a bounded feature recipe), conditional on the correct execution contract. They **do not** establish a hard physical stopping time for OS/GPU work or bound missing gate/calibration work. Loader/generation deadlines, 300-second reservation, finite wait calls, observed maxima and total research ceiling are not mathematical service-time support. We cannot currently justify finite c_max for the proposed all-in hardware service distribution. **D08/D09 remain unresolved.** No cost bound is inferred from successful cleanup in 193 sessions.

A prospective overflow/accounting policy must preserve actual cost without clipping; stop admissions, mark unresolved process/cost explicitly, and block affected audit/analysis. It cannot silently drop expensive rows or condition on successful stops to restore support. If an assumed support contract fails, the affected design/candidate evidence is invalid for that bound and needs review under a predeclared invalidation policy, not a retuned/repeated audit. Direct fallback is operational protection, not repair of invalid statistical evidence.

A tariff alternative would require explicitly reviewed non-overlapping rates such as r_start, r_feature(P_raw), r_gate(M), r_answer_input(P_chat), r_output per token, r_dispatch and r_failure/cleanup. With P_raw,P_chat≤2,048, N_out≤2,048, J=0 and a reviewed gate operation bound M_max, a schedule could imply a finite charge bound by summing those maximum charges. Without gate/initialization/failure rates and count bounds it is incomplete. An explicit fixed failure fee could bound **contractual price**, not actual runaway hardware time. No numerical rates, currency charges or such schedule are adopted here; actual paid fees remain zero/not incurred by this task.

The budget remains **beta=c_D_ref+0.5(c_R_ref−c_D_ref)**, common to all methods. Obtain references on outcome-independent balanced development inputs with the *same* service/startup/failure policy and frozen reference averaging; do not set beta from isolated collection-worker means. Unconditional D/R references bypass the learned gate; active TC/winner/factorized costs include their entire gate even when routing D. If c_R_ref≤c_D_ref, report that fact and implications without forcing a gap or enlarging beta. References and beta must be fixed before tuning. No reference number or beta is set here.

{chr(10).join(proxy_table)}

These are **selected-answer component proxies from existing collection**, computed with per-input selected D/R means, not deployable all-in C_g or estimated fees. The last column intentionally illustrates the simplifying independence assumption of routing fraction times global means; the outcome-selected rules differ because input, action and cost are associated. For an active gate add its per-input live feature/CPU/calibration/init charge under the reviewed service policy, not a free cache and not 50 research passes per query. Always-D fallback bypasses the gate entirely. No cost-feasible or audit-feasible candidate is asserted from this table.

## D. Recommendation, authority discrepancies and limitations

Recommend the **offline cost-boundary/calibration preflight** detailed in `next_step_proposal.md`/`.json`, aimed at a contingent 24-answer/26-feature diagnostic. This is preferable to immediately scaling outcome labels: the cost boundary/support issue remains unsolved and concentrated direct exposure gives little evidence for learning a harm screen. All model work in that proposal is explicitly **UNAPPROVED**. No schedule or new inputs were materialized, and no serving or scientific change was implemented.

The original reference PDF (12 pages, SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`) Sections 3–8 and the active CR01 TeX Sections 3–8 were read. Original cap/99% stop and pre-label candidate-hash/failed-resample wording are already superseded by approved CR01/C01/C02; they are preserved, not silently reapplied. Active protocol and TeX agree on gate/objective, scalar choices, audit algebra and three-contrast success rule. The cost sentence “any declared preview” remains a generic charge clause in both; scope prohibits previews here, and no preview is proposed. Historical preflight documents' “no decoder ran/no authorization exists” statements describe their old checkpoint; P02D execution does not rewrite them. No new scientific contradiction blocks this offline algebra. Log the conservative-residency timing-boundary clarification above for future reporting; no manuscript conclusion or accepted artifact is edited.

Decision ledger entries explicitly separate evidence from proposed resolutions. Open: D08/D09 support/accounting, D05 full gate/feature freeze, D10 resources, D11 n/K and breadth/depth, D12 normative risk/score margins, D14 theorem/simulation work in P03, D16 common reference/beta, and D17 final backup. None is resolved by a successful small diagnostic. No study-wide infeasibility, significance, trained-route comparison or completion eligibility stop is declared. Jev, judges, extra checkpoints and cascades remain parked.

Reproduce using `.venv/Scripts/python.exe scripts/p02e_reproduce.py`; it writes to a disposable directory and compares deterministic outputs without overwriting accepted output. It imports only standard-library modules, verifies sources and writes new analytical files exclusively. Focused checks: `.venv/Scripts/python.exe -m unittest discover -s tests -p test_p02e_design.py -v`. Eight checks pass for formula ranges/zero variance, denominator/Kish, the contract example/incomplete/invalid-score rejection, cost partitioning, totals and bindings/no model/audit imports. No full regression suite was rerun because no production code changed.

Preparation's PDF text extraction succeeded but its first console print exited 1 due to Windows cp1252; a UTF-8 read of the saved extraction succeeded. This was an offline display error with no evidence/model impact. Preparation/analysis/test/documentation/package receipts record wall/CPU where instrumented; human reading/writing is not comprehensively CPU-timed. Original and CR01 manuscript/PDF bytes remain unchanged. All P02D raw evidence and immutable plans/packets remain preserved.

Backup is verified local files/packets only; no push, upload, remote query or external transfer. “External receipt” means outside the ZIP on this workstation, not off-machine backup. A later coordinator handoff is required after review. **Dispatch false; zero new model work; P02 incomplete/unsealed; P03 unstarted.**
''')
write(OUT/'document_render_receipt.json',dict(status='PASS',wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
 model_work=0,source_sha256=sha(Path(__file__)),rendered=['offline_design_report.md','next_step_proposal.md','next_step_proposal.json']))
