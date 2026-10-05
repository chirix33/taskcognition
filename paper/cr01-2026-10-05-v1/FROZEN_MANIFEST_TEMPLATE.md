# TaskCognition Frozen Manifest Template

**Status:** **PRE-DEVELOPMENT TEMPLATE — NOT FROZEN — NOT AUTHORIZED FOR EXECUTION**

This template is the schema for the dated, hash-bound manifest required after the disjoint DEVELOPMENT stage and before any final TRAIN, TUNE, AUDIT, or TEST rollout. It is not a substitute for the original reference plus adopted CR01/C01-C03 and active [`taskcognition.tex`](taskcognition.tex). A final manifest must be copied from this template, assigned a version and timestamp, populated with immutable values and content hashes, reviewed by the authors, and saved without modification before final label generation.

A missing, malformed, or hash-mismatched final manifest requires **always-direct deployment** and invalidates any claimed held-out audit.

## Required identity and scope

| Field | Frozen value required |
|---|---|
| Manifest ID, date, and author sign-off | Unique identifier, ISO timestamp, sign-off record |
| Study scope | Exactly Qwen3-8B, D/R packages, one input-only pre-generation gate, one deployed answer call |
| Protocol source | Specification version, original PDF hash, approved/adopted CR01 hashes, active TeX hash; manifest hash recorded externally (no self-hash) |
| Repository state | Commit or archive hash and dependency lockfile hash |

## Package contract

The final manifest must record the model and tokenizer revision, serving engine and version, API invocation, precision, hardware, batching, concurrency, warm-up and caching rule. It must include content hashes for serialized D and R prompts, chat templates, `enable_thinking` controls, sampling settings, min-p/top-k/top-p/temperature, maximum input length, output cap, EOS/stopping rules, native-thinking parser, outer FINAL parser, suite-native adapters, and evaluators.

It must bind `TaskCognition-CR01-2026-10-05-v1` and common primary D/R caps of 2,048 total generated tokens. Completion and failure subtypes are descriptive; no completion certification or automatic threshold stop applies. Strict scoring, failure retention and all audit requirements persist. Other prospective primary caps are unsupported under this version. Historical configurations keep their original version and are not relabelled.

## Operational contract

The final manifest must specify the deterministic random-stream derivation, deadline, maximum pre-admission retries, admission logging procedure, response-retention rule, and zero-score handling for admitted execution/response failure. It must fix a scalar ledger type—either monetary token/call tariff or hardware-service-time charge—without double charging the same serving work. It must provide analytical hard cost bounds from maximum input length, cap, retry ceiling, and tariff/service-time rule.

## Data and learning contract

The final manifest must bind the development, train, tune, audit, and test latent-problem/seed manifests; family membership; equal 1/6 family weights; renderer pairing status; K; high-repeat development allocation; feature extractor; encoder; architecture; parameter budget; optimizer/search space; calibration procedure; candidate-selection rule; tie-breaks; and direct fallback.

## Audit and inference contract

The final manifest must bind alpha, the common exogenous beta, b-min, delta-score, gamma, balanced audit count n and n-f, cost bounds, the empirical-Bernstein implementation, the candidate schema and selection rules (later child records carry candidate hashes), all audit code, and the score noninferiority rule. It must also specify the test bootstrap as 10,000 family-stratified complete-input resamples with percentile lower bounds, deterministic bootstrap seed, K-draw score aggregation, and retained model-failure scoring within complete resamples; missing/corrupt evidence must stop analysis, not zero or redraw an entire resample.

## Change-control rule

Any change to a package, scorer, parser, feature, split, threshold, cost schedule, candidate, audit method, or inference code after manifest freeze invalidates all affected rollout-derived labels and requires a new disjoint audit. The old audit must not be reused. The test split must remain inaccessible to training, tuning, development, audit, and prompt design.
