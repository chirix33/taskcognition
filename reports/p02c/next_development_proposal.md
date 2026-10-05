# Next DEVELOPMENT tranche under CR01 — proposal only

**Not approved, not dispatched.** Review this as one bounded tranche after P02C. No part of it runs automatically. CR01 settled the primary cap, not these counts, features, deadlines, cost rates or ceilings. P02 remains incomplete; P03 is unstarted.

## Purpose and sequence

1. Publish a new immutable CR01 plan for **four fresh inputs per family (24 input clusters)**, native defaults at Reasoning Gym `21e6d2a9a581b3e11aafe711abfd37402f8482d5`. Proposed generator seed for family index f=0..5 in the established family order: `930261005 + 10000*f`, size 4, indices 0..3. This selection is a proposal, not an already materialized/eligible sample. Before any live work, materialize all native questions and configs, reject any collision with P01/P02A/P02B or reserved partitions, and check the provisional 2,048 serialized-input-token ceiling. An overlength/colliding selection blocks the plan; no truncation or outcome-informed replacement. Keep gold/family/latent metadata in outcome stores only.
2. Before answer outputs, run the single prespecified input-only feature-cost diagnostic below. It cannot choose a feature recipe based on labels. Archive exact input token IDs, feature definition and source fingerprints. A feature software/integrity incident stops this proposed tranche before answers, without silently skipping the measurement. Persist every incurred cost.
3. For every selected input, collect **four independent D and four independent R draws**, each at **2,048 total new tokens**. Exactly **192 answer dispatch slots**, **393,216 reserved output tokens**; J=0, no replacements or autoregressive warm-ups. Derive distinct streams from `(CR01 specification, run ID, input ID, mode/package hash, draw index)`; do not pair modes by seed. Predeclare a round-robin family/input/draw schedule, alternating which mode goes first by input/draw parity. No outcome adaptation.
4. Stop for review with 12 family-by-mode QC cells (16 planned draws each), 24 input-cluster targets, within-input variation and per-input direct-perfect counts. Report missing/unexecuted requests separately. Do not fit a gate, run P03 simulations, collect final labels or promote these development rows to final splits.

Retain the exact P02B common instruction, model revision `b968826d9c46dd6066d109eabc6255188de91218`, tokenizer, BF16 native Windows SDPA MATH, all effective sampler defaults, strict parser/native scorers, native questions and failure semantics. The prospective primary cap is fixed; there is no formal cap-selection stage or completion-based eligibility stop.

## What 24 inputs and K=4 can resolve

Four inputs per family broaden coverage beyond one, while four draws per mode expose some within-input instability. This remains a small convenience-sized prespecified native-generator sample, not a final population freeze. Use equal family weights and preserve clustering; 16 draws in a cell are not 16 independent input clusters, and 16 D/R cross-pairs per input are not independent observations.

For a fixed input, a Bernoulli perfect-rate estimate with K=4 has conditional standard error at most 0.25; a difference of two independent bounded-score means has conditional standard error at most sqrt(1/(2K)) = 0.354. These are worst-case bounds, not observed precision or confidence intervals. Between-input heterogeneity remains largely unknown with four inputs/family. Even four failures on one input are compatible with a substantial underlying perfect probability; extra repeats do not substitute for new inputs.

Report T_b, T_h, h_DD and d_0.10/d_0.25 per complete input, D/R score distributions, failure subtypes and actual direct-perfect counts. Use independent mode draws; retain primary zeros and native partial scores without diagnostic replacement. Summarize within-input variance descriptively, without claiming precise de-noising or target reliability. No significance or routing-superiority claim is possible.

This tranche assesses whether direct-perfect observations occur across multiple inputs, rather than merely measuring a tiny harm numerator. There is no selected gate yet, so routed B, b_min adequacy and audit passage cannot be established. The later audit still requires its positive lower denominator bound. A poor denominator may motivate a design/resource stop; it does not reinstate the removed completion threshold or authorize easier tasks.

## Same-checkpoint feature diagnostic, fully charged

One candidate only: original native question text tokenized by the pinned Qwen tokenizer with `add_special_tokens=False`, no chat instruction, no truncation and no answer tokens. Use `model.model` in evaluation/inference mode, `use_cache=False`, and its final decoder hidden states **after the final RMS normalization**. Take an attention-mask-weighted mean across all original-text tokens, accumulating in float32; save a float32 vector. No layer/pooling search, output head, sampled token, alternate encoder or answer-conditioned observable. Confirm the actual module/output shape against the pinned local config in offline preflight; a mismatch blocks this proposal rather than silently changing the recipe.

Cheap observables: character count, tokenizer input length, ASCII digit-character count, count of characters in `+-*/=<>%^`, line-leading multiple-choice markers `[A-D][.)]`, and case-insensitive whole-word presence flags for `json`, `list`, `number`, `text`. These are functions only of original text. No family/latent/gold/trace fields enter the gate-facing record. Any standardization is fitted on future TRAIN only; no normalization is fitted in this tranche.

Budget **50 pure input forward passes, zero answer generations**:

- Two explicit initialization/warm-up forwards on the first two prespecified inputs, charged and logged.
- One measured forward for each of 24 inputs.
- Two additional measured forwards on each of the first two inputs in each family (12 inputs x 2 = 24).

Thus 48 measured + 2 warm-up forwards, at most **102,400 processed input-token positions** at the ceiling. Store every timing, including warm-ups. Run sequentially in one isolated feature worker with one model load, no reuse of past-key-value caches between forwards. Record load, first-forward, warm-forward, CPU feature, serialization, peak memory, full worker residency and cleanup separately. This observes a warmed feature path plus its initialization, not final serving latency. If deployment uses isolated workers or another cache policy, its actual load cost must also be counted and reviewed; this benchmark cannot make it free.

Feature throughput is **unmeasured**. Propose a **15-minute GPU-residency / 20-minute wall-time sublimit**, contained in the combined ceiling below, with a 120-second per-forward deadline and explicit cleanup reservation. These are operational limits, not estimates of per-forward cost or mathematical support bounds. No repeat/recipe change after outputs. Deployment cost must include a live feature forward for each routed query; cached research vectors do not remove it. No MLP training or encoder benchmark is authorized by P02C itself.

## Measured basis, forecasts and proposed ceilings

P02B's 2,048 condition comprised only one input/family and two draws/mode: 24 calls, 17,101 generated tokens, 954.4397468 seconds worker residency. D: 243.0045899 s/12; R: 711.4351569 s/12. Scaling that same family-balanced mixture by eight gives **136,808 output tokens and 7,635.5179744 s (2.12 h)** for 192 calls. This is an illustration conditional on that tiny mixture, not a confident budget prediction for new inputs. P02B's entire raw run was 944,871 bytes; no feature measurements exist.

| Item | Central planning illustration | Reservation / proposed stop ceiling |
|---|---|---|
| Answer calls | 192 | 192 dispatch slots, counting failed/unknown admission; no replacements |
| Generated output | 136,808 using P02B mix | 393,216 tokens = 192 x 2,048 |
| Answer worker residency | 2.12 h | Within combined 4 h; never clip actual cost |
| Sensitivity to input/runtime variation | 1.5x: 3.18 h; 2x: 4.24 h for answers alone | A 2x scenario would not complete within 4 h; partial execution is acceptable evidence, not a filled denominator |
| Feature passes | 50, throughput unknown | 15 min residency / 20 min wall sublimit |
| Combined execution | About 2.12 h + measured feature/dispatch overhead, unknown now | **4 h cumulative GPU/worker residency, 5 h execution wall** |
| Evidence | Answer raw bytes scaled by calls: about 3.78 MB; allow 3x for longer texts/record overhead; vectors/ZIP add overhead | **0.5 GiB additional evidence**, including local packet and vector records |
| Source/environment/weights | Reuse current pinned bytes | **Zero new model/dependency downloads/upgrades** |
| Preparation | Offline plan/fixtures/validation separately recorded | No unlogged model work |

Continue sequential isolated answer workers with the current provisional 120-second generation deadline and load/cleanup policy. Reserve at least 300 seconds and the planned output cap before each dispatch; stop admitting when either remaining residency/wall/evidence envelope cannot accommodate the reservation. Record actual overshoot and cancellation/cleanup cost. This can stop short of 192 calls and must not trigger extra slots. Feature budget must be subtracted from the same combined counters, not hidden in a separate free ledger.

## One scalar ledger and hard-support question

Retain a unified dispatch/feature/answer ledger: every attempt and every feature/warm-up pass is logged once. Keep actual wall time, conservative worker residency, CPU work, tokens, loads, cancellation and memory as separate descriptive measurements. Neither P02B's observed maximum nor a 120-second timeout proves a hard service-time bound; process termination and cleanup can overshoot. Hardware-time C still needs an enforceable, audited bound on all gate and answer work before final labels. An out-of-range cost invalidates the relevant analysis; do not clip it.

**Unapproved alternative reference tariff**, explicitly hypothetical and not an actual bill or default:

- $1.00 per million input tokens processed in each full Qwen prefill, including the live feature pass.
- $2.00 per million generated answer tokens, including native thinking.
- $0.0001 per dispatched feature or answer call; the schedule expressly includes its loader/dispatch/cleanup work, so those are not billed again as time.
- $0.00005 per query for bounded CPU cheap features, one frozen MLP evaluation, normalization/calibration and route decision. Exact maximum MLP size and feature algorithm work remain required freeze fields; this flat reference charge is not an observed market price.

Proposed deployment count limits for that tariff: one feature forward, one CPU-gate evaluation, one selected answer dispatch, J=0, at most 2,048 tokens on each of the feature and answer input paths, and at most 2,048 generated tokens. No deployment warm-up/extra call is silently allowed; initialization policy must be bound to this schedule or explicitly added before freeze. Under those count assumptions, C_gate <= $0.002198, C_answer <= $0.006244 and **0 <= C_query <= $0.008442 reference dollars**. These algebraic tariff bounds do not bound real seconds, energy or fees. Counts outside the contract remain integrity failures. Unknown admitted output gets the full reserved-cap reference charge rather than a fabricated zero, with actual resource uncertainty reported separately.

Charge the two research warm-ups as feature calls with their actual input counts; keep research collection separate from one-query deployment. Compute c_D_ref and c_R_ref from approved development package charges, then the same beta midpoint for all methods; charge the live gate on top of each selected answer. Do not enlarge beta for expensive features or alter rates after comparing learned methods. If the ledger/beta makes useful routing infeasible, report that consequence. Rates, bounds, initialization, final timeout, beta and resource interpretation require review; CR01 approved none of them.

## What remains for P02 and P03

P02 still needs broader target-noise/failure evidence, feature cost under a declared deployment policy, a defensible all-in scalar ledger/support contract, dataset/input eligibility review, complete provenance and durable backup. This tranche may expose the next bottleneck but cannot finish those decisions by itself.

A later P03 proposal must consume complete input clusters, score/correctness distributions, within-input variation, approved input features, failure types and cost associations. With only 24 development inputs, resampling cannot supply genuine broad independent coverage; use explicit synthetic sensitivity scenarios and disclose their assumptions. Proposed *discussion grid*, not approved allocations: K in {4,8,16}; balanced audit n in {600,1200,2400}; TRAIN {100,200}/family, TUNE {50,75}/family and TEST {100,200}/family. Total final-call formula is `2*K*(6*n_train_family + 6*n_tune_family + n_audit + 6*n_test_family)`. No cell count is selected here, and alpha, b_min, delta_score, cost bounds and feature/gate search budgets remain unresolved.

Before any comparative simulation, review a reduced grid, outcome-independent selection rule and null/useful/harmful/low-denominator/failure-heavy scenarios. An initial proposed 200 replicates per scenario has worst-case Monte Carlo standard error 0.0354; 1,000 gives 0.0158 (about 0.0069 near a 5% event rate). These are planning calculations, not simulated results or proof of audit control. A separate proposed CPU-only simulation resource screen would cap at 4 wall hours, 8 GiB additional RAM and 1 GiB evidence, with no GPU/new labels; actual attainable replications are unknown until approved profiling. This is not authorization to start P03.

The earlier 2,400-call formal cap stages are no longer a required CR01 step. The 1,200/15,000-call pilot suggestions, any additional high-repeat tranche and the feature benchmark above remain unapproved. A larger follow-up must choose between more inputs and more repeats using this tranche's evidence and cost, without promoting diagnostics into final labels or silently extending the plan.

## Backup and review decision

Current evidence has local raw files plus a verified local ZIP, **not an off-machine backup**. Before irreplaceable final collection, propose a user-designated encrypted external physical drive, under `<approved-external-root>/TaskCognition/CR01/<run-id>/`, containing raw evidence, environment/source manifests, original/amended manuscripts and review packets. Require SHA-256 verification and a sample restore to a distinct local directory. The device/path, capacity, encryption and retention policy are unresolved; no external path is presumed mounted and nothing is uploaded or copied there now. Final-study capacity must be costed after sample allocation, with at least two copies plus restore headroom.

The next review should approve or amend this exact 192-answer/50-forward tranche, its deployment-cost interpretation and resource/backup conditions. It need not decide the entire final study. Until a subsequent conveyed execution prompt, all real dispatch stays disabled.
