# TaskCognition Frozen Manifest Template

**Status:** **PRE-DEVELOPMENT TEMPLATE — NOT FROZEN — NOT AUTHORIZED FOR EXECUTION**

This template is the schema for the dated, hash-bound manifest required after the disjoint DEVELOPMENT stage and before any final TRAIN, TUNE, AUDIT, or TEST rollout. It is not a substitute for the active scientific protocol in [`taskcognition.tex`](taskcognition.tex). A final manifest must be copied from this template, assigned a version and timestamp, populated with immutable values and content hashes, reviewed by the authors, and saved without modification before final label generation.

A missing, malformed, or hash-mismatched final manifest requires **always-direct deployment** and invalidates any claimed held-out audit.

## Required identity and scope

| Field | Frozen value required |
|---|---|
| Manifest ID, date, and author sign-off | Unique identifier, ISO timestamp, sign-off record |
| Study scope | Exactly Qwen3-8B, D/R packages, one input-only pre-generation gate, one deployed answer call |
| Protocol source | SHA-256 hash of `taskcognition.tex` and this manifest |
| Repository state | Commit or archive hash and dependency lockfile hash |

## Package contract

The final manifest must record the model and tokenizer revision, serving engine and version, API invocation, precision, hardware, batching, concurrency, warm-up and caching rule. It must include content hashes for serialized D and R prompts, chat templates, `enable_thinking` controls, sampling settings, min-p/top-k/top-p/temperature, maximum input length, output cap, EOS/stopping rules, native-thinking parser, outer FINAL parser, suite-native adapters, and evaluators.

It must declare the terminal development cap decision. The decision is 1,024 only if every mode-by-family strict-valid-FINAL cell reached 99%; otherwise it is 2,048 only if every such cell reached 99%. If neither rule passed, the confirmatory bounded-package study is marked infeasible and no final rollout is authorized.

## Operational contract

The final manifest must specify the deterministic random-stream derivation, deadline, maximum pre-admission retries, admission logging procedure, response-retention rule, and zero-score handling for admitted execution/response failure. It must fix a scalar ledger type—either monetary token/call tariff or hardware-service-time charge—without double charging the same serving work. It must provide analytical hard cost bounds from maximum input length, cap, retry ceiling, and tariff/service-time rule.

## Data and learning contract

The final manifest must bind the development, train, tune, audit, and test latent-problem/seed manifests; family membership; equal 1/6 family weights; renderer pairing status; K; high-repeat development allocation; feature extractor; encoder; architecture; parameter budget; optimizer/search space; calibration procedure; candidate-selection rule; tie-breaks; and direct fallback.

## Audit and inference contract

The final manifest must bind alpha, the common exogenous beta, b-min, delta-score, gamma, balanced audit count n and n-f, cost bounds, the empirical-Bernstein implementation, candidate hashes, all audit code, and the score noninferiority rule. It must also specify the test bootstrap as 10,000 family-stratified complete-input resamples with percentile lower bounds, deterministic bootstrap seed, K-draw score aggregation, and failed-resample handling.

## Change-control rule

Any change to a package, scorer, parser, feature, split, threshold, cost schedule, candidate, audit method, or inference code after manifest freeze invalidates all affected rollout-derived labels and requires a new disjoint audit. The old audit must not be reused. The test split must remain inaccessible to training, tuning, development, audit, and prompt design.
