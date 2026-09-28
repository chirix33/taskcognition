# P02A: seal accepted P01 and run one bounded six-family integration slice

The user is conveying the coordinator's P01 v2 acceptance and authorizing this prompt's bounded local work. Read `P01_v2_coordinator_acceptance.md`, root AGENTS.md, the governing revised PDF, protocol, C01-C03, decision register, and generic P02 prompt. This prompt limits the currently executable part of P02. P02A is a review checkpoint within P02, not a replacement for the full phase or a scientific freeze.

Do not import meeting/NSF/Jev/live-judge work. Keep the revised paper's model, targets, six families, scoring and required comparators intact. No other phase is authorized.

## 1. Verify and record P01 acceptance

Before any new live work, verify these local artifacts:

| Artifact | SHA-256 |
|---|---|
| reports/phases/P01_completion_v2.md | `e75e0f4e99396223b61beb3f378c10d3a3a7c9d5db4db0d248700fae5ac69f13` |
| reports/phases/P01_proposed_seal_v2.md | `ea632c19ffa3a9b842e6a3e74c7fe3cd078cf0dbceda7eb347307bbe12bcf4da` |
| reports/phases/P01_evidence_manifest_v2.json | `1237761e49fcee9a9e027324995f6452b27b83417b205e12c44d451940b09a3f` |
| reports/p01_correction_v2/P01_review_packet_v2.zip | `dab8fd3ae4ea7b09e5802de7f02ee12f9f00dbf843c857e5921ca9dc69a639b3` |

Verify indexed files against their accepted snapshot and identify corrected code/evidence commit `6e8cec19d3e7f374aebddaa4f9b410767b02676a` plus the separate report-packet commit. Do not rewrite old evidence to make current-state hashes match. Stop on a discrepancy.

Preserve both proposed seals and original/corrected reports. Create `reports/phases/P01_accepted_seal.md`, referencing this user-conveyed acceptance, the actual timestamp and verified hashes. Record a new state event sealing P01 and activating only P02A. Keep P01 dispatch disabled and its unused five slots inactive. Do not set P01 IN_PROGRESS merely to reuse its runner.

Preserve unrelated staged files, including any user prompt/review files. Use task-only local commits; no push, merge or history rewrite. The earlier report's staged-file warning is not permission to commit those files.

## 2. Exact execution envelope

This accepts the first bounded slice proposed in `reports/p01/P02_resource_proposal.md`:

- Six prespecified fresh DEVELOPMENT inputs: one per family.
- Exactly two planned independent D draws and two planned independent R draws per input: **24 answer generations maximum**, including all admitted/unknown attempts and any unsuccessful attempts. No replacement slots or hidden autoregressive warm-ups.
- **1,024 total new tokens per generation**, including thinking plus final output; maximum reserved output **24,576 tokens**.
- **90 minutes cumulative GPU residency**, **two hours elapsed execution wall time**, **0.5 GiB additional evidence**. Track code preparation separately. Reuse existing model weights and inference environment. Never hide overhead or clip actual measurements to these limits.
- Provisional 120-second generation timeout, J=0, sequential single-request execution. Preserve measured cancellation/cleanup overhead. Reserve sufficient time for one request's load, deadline and cleanup before admission; stop dispatching if the remaining envelope cannot accommodate it.
- Use the existing native BF16 Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, native Windows backend and verified SDPA MATH implementation. No new answer model, encoder model, quantization, backend, driver or environment upgrade.
- Minimal native dataset source/dependencies may be fetched at the pinned revision if missing, in the project environment only. Preflight their necessity and compatibility; keep additional source/dependency disk use within 1 GiB, separately from evidence. No upstream revision substitution or unrelated package upgrades. Stop with a concrete dependency proposal if this cannot be met.
- No paid/cloud work. Local raw evidence plus a verified local review ZIP are authorized; do not claim an off-machine backup. Propose a durable backup destination for the larger pilot without uploading private evidence elsewhere now.

These are operational limits, not mathematical support bounds for the paper's audit. No cap escalation to 2,048, extra live retry, formal cap study, high-repeat pilot, live feature-encoder measurement, or gate training is authorized by this prompt.

## 3. Build the six-family path before dispatch

Use Reasoning Gym revision `21e6d2a9a581b3e11aafe711abfd37402f8482d5`. Resolve and inspect the native entries for `number_sorting`, `number_format`, `letter_counting`, `graph_color`, `shortest_path`, and `knights_knaves`, including renderer, answer syntax, scoring range and any partial credit. Preserve source/version/license provenance. A missing or incompatible entry blocks its integration; do not replace the family or silently move revisions.

For this diagnostic, use the pinned native default difficulty configurations unless an existing approved six-family configuration is available. Materialize every effective setting in the run plan; do not reuse P01's tiny sorting configuration as an undocumented population choice. Dataset size/seed/index may be set for the six-input diagnostic. No outcome-informed simplification or easy-case screening. Integration configurations remain provisional for the later reviewed cap study; they are not the final population freeze.

Select one fresh input per family using declared seeds/indices before any live output. Give latent items, rendered inputs and requests stable identities. Ensure disjointness from P01 and reserve disjoint namespaces for later cap/high-repeat/final partitions. Check duplicate content as well as nominal IDs. Set and justify a serialized-input length ceiling before dispatch, using checkpoint/runtime constraints. If a selected input exceeds it, report the blocked plan rather than silently truncating or replacing it with an easier input.

Retain each native rendered question verbatim. D and R receive identical task information and the same wrapper instruction; native thinking-mode serialization may differ. A single common clarification of the FINAL instruction is permitted for this DEVELOPMENT interface diagnostic, fixed and hashed before all 24 outputs. It must not alter task wording, add solved examples/gold, request answer repair, or change the strict parser. Preserve its exact diff from P01. Do not try several prompt versions within these 24 draws or change it after seeing results.

Keep the matched sampler: do_sample=True, temperature=.6, top_p=.95, top_k=20, min_p=0; explicitly pin all other effective defaults. Archive exact messages, rendered prompts, token IDs, native channel context, package hashes and streams. Mode/draw streams must be distinct; do not pair D and R by identical random seeds. These two draws per mode are a diagnostic K, not a final K choice.

Keep metadata/gold/scorer fields in outcome stores. Any prospective gate-input record exposes only original text and approved input-only observables; no family/latent/gold/trace fields. Family remains available to offline evaluation and equal weighting.

## 4. Preserve the corrected execution boundary

Use a P02-scoped runner/guard with an explicit immutable P02A run plan and its own counters. Reuse corrected components where sensible, without reopening P01 or weakening its guards. Confirm actual import paths/source hashes in the chosen interpreter before launching: an old installed 0.1.1 wheel must not silently execute instead of reviewed source. Explicit `PYTHONPATH=src` is acceptable if the subprocess inherits it and verification demonstrates the imported code.

Carry forward durable dispatch/admission, no replay of admitted/unknown requests, unscored incident handling, callback-error propagation, token/result integrity, and cost-once accounting. Retain the 81 tests and add only necessary tests for six-family adapters, P02 scope/budget boundaries and generalized request handling.

Before live execution, verify supervisor cleanup under an injected monitoring/evidence error: a supervisor exception must stop further dispatch, terminate/wait for its active child as needed, preserve the incident and incurred-cost evidence, and never leave a generation running unnoticed. Keep this a small runner guarantee, not a serving-platform redesign. Known timeout/cancellation remains distinct from a software/evidence incident.

Validate each unchanged native scorer offline with hand-checked valid/wrong/malformed examples and partial-credit examples where supported. Preserve native tolerance and score precision. Test strict FINAL/channel separation with each native syntax. Do not replace the scorer with universal exact match or silently round near-one scores to perfect.

Write and hash the complete six-input/24-request plan before dispatch, including order, counters, limits, source/runtime versions and stopping rules. Fixture tests and native gold/scorer checks are not empirical generations. If preflight fails, finish BLOCKED without using model calls.

## 5. Execute once and report what happened

Run the predeclared requests sequentially. Retain wrong, malformed, capped and known-timeout outcomes under the declared rules. A missing/corrupt evidence record or unexpected software failure stops the run for investigation; it is not a score-zero draw and does not permit a replacement generation. On partial completion, report completed and unexecuted requests separately rather than filling missing rows.

Report all 12 family-by-mode cells with their planned denominator (two), executed/retained counts, strict-valid-FINAL count, native scores, perfect-correct count, failures, output lengths, durations, memory and costs. Show whether any live D output met the strict wrapper, without requiring success to make the diagnostic scientifically useful. Preserve all failures even if the wrapper clarification helped another family.

This slice is **not the formal cap-selection sample**. A 2/2 cell does not certify a 99% completion rate, and a poor cell here does not by itself invoke the formal 2,048 infeasibility stop. Do not pool these rows or P01's deliberate interruption into a later formal cap denominator. Later formal cap evaluation must use a reviewed predeclared plan and fresh DEVELOPMENT inputs.

For inputs with all four validly recorded draws, run the existing target aggregation and report T_b, T_h, direct-direct redraw and prespecified partial-credit diagnostics where implemented. Treat these as pipeline checks; six inputs with two draws per mode cannot establish target-noise precision or routing superiority. Do not turn K-squared cross-pairs into independent samples. Do not fit a gate or make a significance claim.

## 6. Deliver a review checkpoint and a concrete next proposal

Return:

1. `reports/phases/P02A_completion.md`, explicitly stating P02 is incomplete and unsealed.
2. The P01 accepted seal, new state events, pre-dispatch run plan, six native-adapter/source/config records, prompt diff and all raw outcomes/ledger/resource evidence.
3. Twelve-cell integration table, target pipeline checks, test logs, source commit/diff and exact hashes, plus a compact `P02A_review_packet.zip` and verified evidence index/receipt. Exclude weights/environments/secrets/private meetings.
4. A concrete proposal for the next P02 slice: formal 1,024/2,048 cap-study denominators, independent input/repeat structure, fixed completion rule, expected compute/storage, and handling of an unpromising interface. If recommending a development package revision, separate it from the subsequent fresh cap evaluation and retain all earlier attempts. No automatic execution.
5. A costed proposal for the high-repeat/feature-cost work and remaining P02 exit criteria, including backup and the unresolved scalar-cost/hard-bound issues. Use six-family observations with clear uncertainty; do not extrapolate a confident whole-study budget from a single tiny sorting example.

Finish **P02A READY_FOR_REVIEW**, **BLOCKED**, or an appropriately documented stop. Disable live dispatch at the checkpoint. Do not create a P02 accepted seal, mark all of P02 complete, start P03, or collect TRAIN/TUNE/AUDIT/TEST labels. The formal cap study and larger pilot await the next conveyed review prompt.
