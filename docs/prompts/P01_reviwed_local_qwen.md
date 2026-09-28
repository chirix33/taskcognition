# Reviewed P01 prompt: Windows / RTX 5090 local Qwen smoke

The user is conveying the coordinator's P00 report-level acceptance and authorizing this P01 scope. This prompt supersedes `docs/prompts/P01_local_qwen.md` for the current run. Preserve the generic prompt as history and add this reviewed prompt to `docs/prompts/`. Work on P01 only; no P02 pilot or final labels.

Read root AGENTS.md, the accepted C01-C03 decision entries, current operational contracts, P00 completion/proposed seal, and the coordinator review. The original manuscript under `docs/iclr2027` remains preserved. Do not re-open already resolved C01-C03 questions.

## 1. Verify and record P00 acceptance

Before backend installation, model download, or generation:

- Verify `reports/phases/P00_completion.md` against SHA-256 `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`.
- Verify `reports/phases/P00_evidence_manifest.json` against SHA-256 `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`, then verify the indexed artifacts against their P00 snapshot.
- Confirm implementation commit `255860890dd480cdd8607e27957b251aa3e1cb1f` and identify the separate report-packet commit. Preserve unrelated work. Run the offline tests and current fixture verification using existing documented commands; save new logs separately, never overwrite the accepted validation JSON or immutable fixture run.
- Stop and report a discrepancy if verification fails. Do not regenerate evidence or update old hashes to pass.
- On success, retain `P00_proposed_seal.md` unchanged and create `reports/phases/P00_accepted_seal.md`. Reference the coordinator's limited review, user-conveyed prompt, verified hashes, and actual acceptance timestamp. Then record SEALED P00 and IN_PROGRESS P01 through a new state event. Preserve the original phase-state bytes in git/snapshot; historical hashes must remain verifiable even as current code/state evolves.

The coordinator has not inspected the source repository or rerun its tests. Do not describe this as independent external code verification. Local verification supplies the preflight evidence.

## 2. Bounded authorization and resource plan

Routine project-local package installation, official model download, reversible code changes, and the following bounded local runs are authorized. Do not repeatedly ask permission for these actions within this envelope. Honor actual runtime permission restrictions.

- Use native Windows first, the reported RTX 5090, and the existing project-local Python 3.12 environment or a separate project-local inference environment if dependency isolation requires it.
- One official `Qwen/Qwen3-8B` checkpoint; pin its exact immutable repository revision before download/generation. No model substitution or quantization.
- Maximum additional disk footprint for dependencies, cache and P01 artifacts: 40 GiB. Inspect metadata and available space first; reuse the model cache and avoid duplicate weight copies. If a trustworthy estimate exceeds this envelope, present the revised estimate before proceeding beyond it.
- No paid/cloud services, system Python installation, driver changes, source-built CUDA extensions, WSL/OS installation, or extra serving stacks.
- Start with two admitted answer generations: one D and one R on the same DEVELOPMENT smoke input, independent sampling streams, cap 1,024 each. This initial pair allows at most 2,048 generated tokens.
- Maximum eight admitted answer generations across the entire P01 run, including any autoregressive warm-up, unsuccessful attempts, interrupted requests and diagnostic follow-ups. Maximum 8,192 output tokens. No automatic pre-admission retries for this smoke: J=0.
- Follow-ups beyond the initial pair must address a named P01 uncertainty, use separate DEVELOPMENT diagnostic IDs, and stay within the eight-generation ceiling. Do not repeatedly solve the same question until a favorable answer appears. The controlled interruption may use one of these slots.
- Predeclare a 120-second per-generation timeout and a 30-minute cumulative GPU-active P01 envelope, including runtime checks/model smoke. These are operational smoke limits, not final study timeouts or proven service-time support bounds. Record synchronization/cancellation overhead and any limit overshoot honestly; never clip measured cost. Downloads and code-writing time are separately reported.
- Print/save the exact run plan before dispatch, including all counters, output directory and cancellation policy. No main study values are frozen here.

If the local stack cannot execute within scope, preserve diagnostics and stop with a concrete alternative proposal. Do not silently offload to CPU or change the model to make a smoke pass.

## 3. Verify the actual GPU runtime

Use current official PyTorch distribution guidance and the official Qwen model card; record source URLs and the exact compatible versions chosen. Do not guess the wheel's CUDA variant from the driver's displayed CUDA version. A driver inventory, import success, or `cuda.is_available()` alone is insufficient.

Install only needed runtime packages through the local environment. Prefer stable official prebuilt packages. Record Python, torch, its CUDA runtime/build, device name, compute capability, and relevant supported architecture information. Execute a small synchronized GPU tensor operation with a known finite numerical check; verify BF16 execution before choosing native BF16 for Qwen. Record any warnings or unsupported-kernel errors. A valid supported fallback kernel implementation in the same runtime is acceptable if disclosed and actually exercised; do not fail solely because an architecture-list string differs when valid compatibility is demonstrated.

If native BF16 is unavailable, report the concrete finding and a precision proposal before changing the recorded development package. Do not auto-quantize. Avoid installing FlashAttention or compiling extensions simply because they are optional examples in documentation. Use a supported built-in attention implementation, validate it and record the choice.

Pin the environment after verification. Keep the offline fixture path usable without loading model weights. Ensure the installed TaskCognition package reflects current source rather than accidentally running the old P00 wheel.

Primary references:

- https://pytorch.org/get-started/locally/
- https://huggingface.co/Qwen/Qwen3-8B
- https://qwen.readthedocs.io/en/v3.0/inference/transformers.html

The actual workstation tests determine compatibility; no version in a cached web snippet is a scientific freeze.

## 4. Implement and test the package path

Use the same exact frozen-for-this-smoke checkpoint, tokenizer and precision for both modes. Serialize the official template with `enable_thinking=False` for D and `True` for R. Archive template/config hashes, exact rendered prompts, input IDs and effective generation parameters. Do not claim absence of latent reasoning in D merely from the switch.

Primary sampler for BOTH: sampling enabled, temperature=.6, top_p=.95, top_k=20, min_p=0. Pin other effective defaults, including EOS/pad/stop behavior. The cap is total new output tokens, including thinking plus final output, not 1,024 thinking tokens plus a second final-answer budget. Do not use model-card differing D settings for the primary smoke.

Implement native channel separation -> one nonempty case-sensitive FINAL pair on the final channel -> native syntax adapter -> deterministic scorer. The prompt/template may already contain the opening native thinking delimiter: interpret output in context rather than assuming both delimiters appear in generated tokens. A missing required closing delimiter must not allow thinking text to be treated as the final answer. Never repair raw model output or borrow the official example's permissive fallback without validating it against the strict paper contract.

Offline adversarial parser tests cover missing native delimiters, FINAL-looking tags inside thinking, empty/duplicate FINAL tags, case mismatch, trailing text/declared whitespace behavior, malformed native payloads, partial credit, wrong answers, perfect answers, and cap-without-final. Preserve raw token IDs, decoded text, parsed channels/payload, finish reason, score, and failure flags separately.

Use one fixed, tiny DEVELOPMENT example from a named primary family with a version-pinned native adapter/scorer for the live smoke. Inspect only the necessary generator/scorer integration; implementing six-family sampling/cap certification belongs to P02. Do not claim the P00 synthetic family labels already exercised native scorers. If using Reasoning Gym, pin the revision used and confirm its native score on hand-checked valid and invalid payloads without model calls.

## 5. Admission ledger, cancellation and restart

Before any real answer generation, implement durable dispatch intent, request/stream ID, admission, and terminal records. For an in-process backend, define a conservative admission boundary immediately before calling the generation operation. Unknown admission is treated as admitted.

Offline fault-injection tests must cover: never dispatched, dispatch intent without reliable admission resolution, known admitted with missing response, completed immutable result, and verified pre-admission failure. Distinguish recorded model failure from corrupt/missing persisted evidence. Do not convert a corrupted result file into a model failure or silently rerun it.

Perform a controlled real interruption after demonstrated admission, within the eight-call budget, if the process mechanism supports it safely. Mark it as a deliberate DEVELOPMENT interruption diagnostic; retain its incurred resources and failure record, and do not treat it as an ordinary spontaneous model failure when proposing later completion-rate studies. Demonstrate restart will not issue that admitted/unknown request again. Do not replay an uncertain request merely to prove resumption.

No failed R call can trigger D. No second admitted generation can repair a missing response. Dispatched attempts remain charged. Record whether cancellation actually halted device work and the measured overhead; do not infer a final hard resource bound from a configured timeout. If safe real interruption cannot be demonstrated, report that P01 criterion as blocked/unverified rather than declaring full completion from mocks alone.

## 6. Execute the initial pair and bounded follow-ups

Proceed with the two planned requests only after runtime, ledger, parser and scorer checks pass. Use independent D/R RNG streams and do not promise deterministic repeated GPU output. No chat history, tools, verifier feedback, answer preview, added answer turns, or gate training. Store all results under a new DEVELOPMENT run ID with `development_observation` evidence kind and explicit smoke purpose.

A wrong, malformed or capped model output is valid diagnostic evidence when the pipeline classifies it correctly. It does not justify a hidden rerun. Record any necessary development package/parser correction, preserve earlier outputs and counters, and use a new package/run identity for any follow-up. A real unmodified valid-final example per mode is desirable to validate the success path; if unavailable within the budget, report the remaining uncertainty and stop without fabricated success.

The smoke does not establish a 99% completion rate, gate quality, audit validity, Qwen superiority, or the final model/package freeze. P02 owns systematic six-family feasibility.

## 7. Deliverables, review packet and stop

Produce the P01 completion report with actual commands, resource usage, raw-output references, tests, failures/skipped checks, source hashes and limitations. Include:

1. `reports/phases/P01_completion.md` and proposed seal.
2. Accepted P00 seal and the separate P01 preflight verification log.
3. Exact runtime/environment lock and GPU kernel verification JSON.
4. P01 resource/run manifest, eight-call counter reconciliation, raw-output hashes, request/admission/failure summary, and a compact machine-readable smoke summary.
5. Parser/native-scorer validation and controlled interruption/resumption evidence.
6. A P01 evidence manifest and a compact review ZIP containing these reports, configurations, actual test logs, key implementation/test source files and relevant small raw smoke artifacts. Exclude model weights, entire environments, secrets, private meetings and irrelevant manuscript history. This packet is for the coordinating assistant to inspect, not a public release.
7. A measured P02 proposal: throughput/memory/storage observations and a proposed pilot budget. Clearly label extrapolation from tiny smoke evidence; do not assume six-family rates or launch the 15,000-generation high-repeat pilot.

Preserve original sources and all P00 evidence. Commit only task-owned P01 changes locally if configured; record code and report-packet identities without circular hashes. Do not push or merge. End at READY_FOR_REVIEW or BLOCKED, not SEALED. Do not begin P02 or ask again whether an already authorized P01 step is permitted unless a real access restriction or resource/scope expansion arises.
