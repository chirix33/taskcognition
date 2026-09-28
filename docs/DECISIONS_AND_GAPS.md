# Decisions, gaps, and scope controls

No blocking clarification is needed to start P00. Unknown workstation and repository details can be discovered locally. Scientific/resource choices below must be resolved before the relevant irreversible evidence stage, not guessed now.

## Decision register

| ID | Decision | Evidence / proposed handling | Must resolve by |
|---|---|---|---|
| D01 | Repository state, OS, GPU/VRAM, RAM, disk | P00 inventory; preserve existing work | P00 |
| D02 | Original TeX/BibTeX/protocol availability | Locate only in task repository; PDF governs if absent; reconcile differences | Affected freeze; TeX before P09 |
| D03 | Local inference backend and exact revisions | Prefer a simple native Transformers path if supported; optimize only if measurements require | P01/P02 |
| D04 | Precision/quantization | Prefer native supported precision; if memory demands a change, report package implications before adoption | P01, final lock P04 |
| D05 | Frozen input encoder | PDF leaves identity unspecified. Conservative scope-preserving candidate: input-only pooled features from the same frozen Qwen checkpoint, with exact pooling/layer/template frozen. Measure full encoding cost. A separate encoder checkpoint requires an explicit interpretation/decision; never quietly download an extra judge model | P02/P03 |
| D06 | Dataset version, difficulty configs, maximum input length | Inspect six native generators/scorers. Freeze configs and outcome-independent input eligibility. No tuning difficulty to help TC | Before cap pilot; final lock P04 |
| D07 | Cap-study sample plan and denominator | Predeclare inputs/repeats per cell and count failed requests conservatively in strict-valid-FINAL rates. Same evaluation rule at 1,024 and 2,048; no pooling cells to hide failure | Before cap run in P02 |
| D08 | Scalar cost and hard bound | Propose measured hardware service time for local workstation if enforceable bounded accounting is justified. A monetary reference tariff is possible but must be explicit and must cover gate work; not a claim of actual paid fees | P02/P03 |
| D09 | Timeouts, J, crash/admission proof, warm-up, cache and batching | Validate interruption semantics and truthful cost accounting. Timeout alone does not automatically bound actual hardware consumption | P02/P03 |
| D10 | Development and full-study resource ceilings | User-confirmed GPU-hours/wall-time, disk and backup plan; no cloud/paid fallback. Propose with observed throughput | Before substantial pilot; final before P04 |
| D11 | K, n, train/tune/test sizes | Development high-repeat and complete pipeline simulations; manuscript counts are placeholders | P03 |
| D12 | alpha, b_min, delta_score and simulation targets | Present scientific tradeoffs. Values are design decisions, not arbitrary defaults. Do not tune tolerances to obtain TC victory | P03 review |
| D13 | Feature transforms, gate sizes, losses, parameter tolerance, seeds, optimizer/search/calibration budgets | Same resources/opportunities for all methods; train-only fit; tune-only choice; exact selection/tie rules frozen | P03/P04 |
| D14 | Statistical numerical conventions and theorem check | Verify analytical examples, constants, cluster design, quantile and zero-denominator conventions | P03/P04 |
| D15 | Secondary analysis registry and licensing | Commit exact planned analyses before primary TEST; decide capability before freeze. No Jev/live judge by default | P03/P04 |
| D16 | Package/reference charges and beta | Common beta= c_D_ref+0.5*(c_R_ref-c_D_ref). If c_R_ref<=c_D_ref, report the observed fact and feasibility implications; do not force a positive gap | P03/P04 |
| D17 | Backups, immutable artifacts, statistical/software failure policy | Separate model failures from corrupted evidence; record accepted recovery/invalidation rules | P03/P04 |

Codex adds resolved values, provenance, authorizing review, and affected hashes to `reports/decision_ledger.md`. A null/TBD value may exist in a development template; `freeze` must reject it for a required final field.

## Logical gaps that need explicit handling

### Testing versus proving

No experiment guarantees a positive finding or universal proof. Completion is an honest evidence package and manuscript, with the primary claim stated only if all required comparisons pass. Do not make paper completion contingent on hiding nulls.

### Cap feasibility

The paper's small cap and 99% cellwise completion rule may make the planned package infeasible. A final output is not the same as a correct output. Freeze the completion definition before the pilot; do not weaken wrappers, omit failed rows, or simplify generators after observing failures to claim the original design passed. Legitimate development revisions are versioned and re-evaluated; the cap limit itself cannot be raised within the current confirmatory protocol.

### Cost of a "small" gate

A small MLP can still require an expensive encoder. Measure all live feature extraction and never treat precomputed embeddings as free inference. If reusing Qwen prompt computation, declare and test that mechanism for every method; no hidden free preview or mode-dependent feature leak.

### Cost bounds and statistical validity

Observed fastest/slowest durations are not support bounds. GPU cancellation, CPU feature work, watchdog overhead, and pre-admission attempts need a bounded contract. If this cannot be enforced, propose an explicit alternative permitted ledger before final labels; do not clip slow cases or assert a bound because a timeout flag exists.

### Single-use held-out evaluation

Software bugs can invalidate a run. After seeing audit/test outcomes, fixing the scientific decision rule and rerunning on the same held-out examples is not an untouched confirmation. Distinguish a verified implementation repair from a new analysis choice, disclose exposure, preserve old artifacts, and obtain a reviewed invalidation/fresh-evaluation plan. Fresh sampling alone does not erase prior outcome-informed design selection.

### Two distinct forms of fallback

Audit failure disables the gate before deployment. A live R call that fails is a scored failure, not permission to generate D. Tests must distinguish these paths.

### Decision freezes are staged

Candidate hashes do not exist before training. Bind the candidate schema and selection algorithm in the base manifest, then add an immutable child candidate record. Do not put fabricated hashes into the base freeze.

## Parked work

Live judges, Jev, additional answer checkpoints, causal same-answer spoilage, multi-agent orchestration, decomposition, memory management, new policy arms, and deployment cascades are outside the active plan. The orchestration requested here is the experiment's workflow, not an agent-based answer system. Revisiting parked work requires an explicit user redirection with a separate scope and evidence contract.
