# Codex prompt: P02D offline preparation for the next CR01 development tranche

Proceed with this offline implementation slice. Read `AGENTS.md`, the active CR01 protocol, adopted amendment, statistical/architecture contracts, P02C proposal and attached coordinator review first. Preserve the paper's scientific scope. Do not request CR01 approval again.

## Authority, state and scope

The coordinator accepts P02C as the completed offline amendment checkpoint. Record that acceptance once, referring to `docs/P02C_coordinator_review.md` and the hashes below. P01 stays sealed; P02A/P02B/P02C are accepted development checkpoints. **P02 remains incomplete/unsealed; P03 stays unstarted.**

P02D here means offline preparation of a specific development runner and plan. Set dispatch false throughout. The proposed 192 answer slots and 50 feature forwards remain **unapproved for execution**. No model load, GPU work, encoder forward, answer generation, gate fitting, final labels, simulation, model/dependency downloads or upgrades. Reading the existing tokenizer/config and materializing native questions on CPU is permitted. No push/merge/new external transfer from this prompt. Use local task-only commits, preserving unrelated changes.

Verify the local P02C packet/index and accepted source identities before editing:

```text
ZIP:    287e8032566d2d284e8856b84eb9f9a53cf9b35064b6c9e94e98a6a684308407
Index:  3daef8e6d92b50ed25ec44d16d19788c848c7bffa09dc83048c2ba22a5c42b0e
Report: cf601dcc2ee336e427825a9236898d1d8a2fa9fa2d82c5fc9c7a14eaa7af6a12
Plan proposal: c4dabc27a0871ee0675e39cc33b0b14c06d6a36a043e65387d688f0818ee14b9
```

Do not rewrite accepted evidence or regenerate historical runs. Archive this prompt and review with their hashes. Treat later source changes as new versioned artifacts. If acceptance is already recorded, verify and reuse it.

## 1. Close provenance follow-ups without altering history

Append a dated note reconciling the historical report's no-push statement with the user's message that `4b0c200` and `53129ba` were pushed on `codex/p02c-cr01-adoption`. Use available Git evidence; distinguish known facts, local tracking state and anything unverified. Do not expose credentials or rewrite the old report/index/ZIP. Include the existing external P02C packet receipt in this handoff. A repository push is not automatically a complete verified backup of ignored/raw artifacts.

If supplied, archive the coordinator's unchanged-source compiled PDF and build evidence as externally compiled derivatives, with source/PDF hashes and environment attribution. The PDF hash is `a97b04ac1bf319abef5f10b93630b01ea31d3f9798977509e60efc019eef9859`. It has 13 pages and resolved citations/references. The workstation's earlier unavailable-build statement remains historically true. Do not claim Codex compiled it or replace the original governing PDF. Missing derivative attachments do not block runner preparation; record their absence.

## 2. Materialize the proposed run exactly, without model execution

Use the P02C proposal as the candidate plan, preserving its counts, seed selection and one feature recipe. Proposed family seeds are `930261005 + 10000*f`, in established six-family order, native size 4 and indices 0–3. Materialize all 24 questions/configs using the pinned Reasoning Gym revision. Record original text, generator config, native identity and hashes in the appropriate stores. Check collisions against P01/P02A/P02B and any reserved identities. Do not invent uncreated final partitions; preserve an exclusion manifest for later split construction.

Use only cached pinned tokenizer bytes. Check the proposed 2,048 input-token ceiling separately for:

- Raw question tokenization with `add_special_tokens=False`, used by the feature path.
- Exact serialized direct chat input with the unchanged P02B instruction/template.
- Exact serialized reasoning chat input with its native mode setting.

Record lengths, token IDs and hashes. An overlength, empty-token or colliding input blocks this candidate plan; do not truncate, replace it, adjust difficulty or search seeds. Report a concrete amendment if needed.

Generate a complete fixed schedule for four independent draws per mode per input: 192 unique slots, D/R cap 2,048 total generated tokens, J=0, no autoregressive warm-up and no replacement slots. Retain the existing independent stream derivation and archive stream/seed uniqueness checks; do not pair D/R by seed. Use the proposal's round-robin family/input/draw order and alternating first mode. Materialize the exact schedule so its meaning is unambiguous.

Bind plan hashes to CR01 version, source/environment, existing P02B instruction, model/tokenizer revision, precision/backend, effective sampler, native adapters, parser, timeout, feature specification and resource limits. Keep this a development run plan with authorization pending, not a final study/candidate/deployment manifest. A later authorization record may bind the plan hash without rewriting its content.

## 3. Implement the single input-only feature worker

Implement the proposed Qwen3-8B same-checkpoint decoder path: evaluation/inference mode, `model.model`, `use_cache=False`, final hidden states after final RMS normalization; mask-weighted mean over original question tokens accumulated in float32; output float32 vector. Pin expected hidden width from existing local config and confirm output semantics by inspecting installed source without loading model weights. Do not substitute layers, pooling, encoders, chat prompts or answer tokens. No cached key/value reuse across forwards.

Freeze exact cheap-feature definitions from the proposal, including regex/Unicode/line-boundary conventions. Make those routine definitions explicit before any outputs; no additional feature search. Keep input ID as join metadata, never a learned feature. Gate-facing vectors/observables must exclude family, gold, latent metadata, scores, failures, generation traces and source filenames. No normalization fit in this slice or the proposed diagnostic.

Plan 50 sequential forwards in one isolated feature worker: two charged warm-ups on the first two prespecified inputs, one measurement per input, and two extra measurements for each of the first two inputs in each family. Record all timings and costs, including warm-ups and load/cleanup. The repeated measurements assess cost/stability; they are not new independent labeled inputs. No forward runs now.

## 4. Add versioned runner/ledger guards and recovery

Reuse reviewed primitives where appropriate, preserving historical P01/P02A/P02B interpretation and scoring. Introduce the prospective CR01 path explicitly; do not reopen old runners by globally relaxing phase or cap guards. No final-freeze implementation or audit-method change is needed here.

The new entry point must reject live execution while authorization is absent and verify the exact reviewed plan hash before any future model load. Validate the development-only role, CR01 version, both 2,048 caps, immutable sources, counts and ceilings. A command-line convenience flag alone must not bypass the pending authorization/state check.

Implement one cumulative ledger with unique attempts and durable admission records across feature and answer stages. Persist costs on success, timeout, interruption and exception. No double charge and no forgotten incurred work. Restart must not replay consumed/unknown slots or recharge completed events. Preserve the worker-error versus scored-model-failure distinction. Unknown or corrupted evidence stays visibly unresolved and stops affected analysis; it is never an invented zero or successful answer.

Plan limits: 192 answer slots; 393,216 output tokens reserved; 50 forwards/102,400 feature input positions maximum; 4 hours cumulative worker/GPU residency; 5 hours execution wall time; 0.5 GiB additional evidence including vectors and packet. Feature sublimits are 15 minutes residency/20 minutes wall and 120 seconds per forward. Answer generation deadline remains the proposed provisional 120 seconds with current load/cleanup policy.

Make clock definitions and admission reservations executable and document them. Include model loads, warm-ups, cancellations, cleanup and any restart cost. At least the proposed 300-second reservation and output-cap reservation must be available before each answer dispatch; use conservative separate reservations for features within their sublimit. Enforce finite loader/worker termination procedures without claiming timeout guarantees a hard mathematical service-time bound. Record overshoot rather than clipping it. If cleanup cannot establish a safe stopped state, do not admit more work.

A partial, timed-out or invalid feature stage stops the tranche before answers; no silently skipped feature measurements. Resource exhaustion later stops further answer admission and returns partial evidence without replacement. Preserve any already incurred data and costs. No outcome-based early success stop, family replacement, prompt edits or large-run extension.

## 5. Prepare development reports and focused offline tests

Implement development-only aggregation for the 12 family/mode cells, failure subtypes, direct-perfect counts, score distributions and within-input variation. For complete K=4 clusters compute existing-contract `T_b`, `T_h`, direct–direct redraw and partial-decline diagnostics at 0.10/0.25. Partial clusters remain raw/descriptive with achieved counts; do not fill missing draws or label them complete K=4 targets. Explain missingness and equal-family summaries; do not treat K-squared cross-pairs as independent rows.

Record physical resource measurements and token counts. Keep research collection totals distinct from a one-query deployment-cost projection. Charge a live feature forward for every future routed query even if training uses cached vectors; do not add 50 research passes to every query or make serving initialization free by assumption. Record cold and warm timing separately.

**Do not adopt the hypothetical reference-dollar tariff, beta, hard cost-support bound, final feature freeze or final sample allocation.** Preserve the proposal as discussion history. The next report must identify which cost/support decisions remain open; this development runner may collect measurements without claiming they settle the final audit's bound.

Use focused offline tests with fake decoder outputs/workers/clocks, never a real model load. Cover new failure risks: post-norm masked pooling/shape/nonfinite checks; feature allowlist; exact forward counts; cumulative sublimits; pending authorization/cap/hash rejection before model load; exception propagation without scores; interrupted ledger recovery and no replay; and incomplete-cluster reporting. Tests must exercise production entry points/implementations. Existing accepted regression checks should run where shared runner/ledger code changes could affect them. No test-count target or unnecessary mirror tests.

Do not run GPU smoke tests to finish this phase. Any actual forward/generation waits for the separate execution authorization.

## 6. Deliver and stop

Return:

- `reports/phases/P02D_preflight_completion.md`, with exact scope, commits, checks, failures, limitations and zero-model-work accounting.
- The proposed immutable run plan and hash, actual input/schedule/feature/environment manifests, resource ledger schema, relevant source changes and focused test evidence.
- `reports/p02d/execution_request.md`: one concrete reviewable request for at most 192 answer slots and 50 feature forwards under the stated ceilings; state what the run can answer, remaining scientific decisions, estimated cost versus hard operational ceilings, partial-run behavior and current backup status.
- `reports/p02d/P02D_preflight_review_packet.zip`, index and an external receipt with full hashes. Include enough changed code and dependencies for independent offline review; no weights, environments, secrets or unrelated material.

Do not introduce an external-drive purchase or backup requirement merely to prepare this bounded local diagnostic. Preserve raw evidence plus verified local packets; describe actual off-machine coverage accurately. Durable backup and final-study capacity remain required review items before irreplaceable final collection.

Stop at **P02D PREFLIGHT READY_FOR_REVIEW** (or a specific BLOCKED condition), dispatch false. P02 remains incomplete/unsealed and P03 unstarted. Do not execute the proposed run, seal all of P02, choose final scientific parameters, or start another phase automatically.
