# P01 prompt: real local one-call D/R path

Execute only after accepted P00 review is conveyed. Record that acceptance in the P00 seal. Implement P01 only; read the governing contracts and P00 report. Resolve hardware/backend choices using measured evidence. Do not begin six-family cap certification or final labels.

## Work

1. Pin the official Qwen3-8B checkpoint/tokenizer revision and a compatible local inference stack. Verify current official APIs. Reuse an appropriate existing model cache; otherwise check disk and download the exact checkpoint. Native supported precision is preferred. If fitting requires quantization or a different precision, document the decision and its experimental impact before adoption; do not substitute a smaller model.
2. Implement D/R via actual `enable_thinking` template control. Archive exact request text/token IDs, template fingerprints, effective sampler fields, model configuration, and raw outputs. Use the primary matching sampler. Unsupported parameters are errors, not ignored warnings.
3. Implement native channel separation -> strict FINAL wrapper -> native adapter/scorer. Test FINAL tags inside thinking, missing delimiters, repeated/empty tags, trailing text, malformed native answers, valid partial credit, completed wrong answers, and cap stop.
4. Implement append-only dispatch/admission/terminal records and conservative restart reconciliation. Validate one admitted generation maximum per draw, only proven pre-admission retries, and no R-to-D rescue. Interrupt a controlled local smoke request to establish truthful admission/cancellation semantics, within the bounded smoke plan.
5. Run at most 24 real answer generations on disjoint DEVELOPMENT smoke inputs across both modes at cap 1,024. Use scheduled independent streams. This limit is an implementation default for P01, not a scientific sample count or cap feasibility test. Report every attempt, failed response, token count, memory peak, and measured time.
6. Produce a traceable example for each mode and a measured resource projection for P02. Ensure an inexpensive offline fixture path still works without model loading.

## Exit criteria

- Both modes use the same pinned checkpoint and validated native control.
- Real raw responses are archived; successful and failed parser paths are understood.
- Sampling settings and independent stream derivation are verifiable.
- Resume/retry tests prevent duplicate admitted generations and free retry costs.
- Resource report supports a bounded pilot proposal; no claim that 99% cap feasibility has been established.
- Final data and held-out outcomes remain untouched.

Write `reports/phases/P01_completion.md`, mode/parser evidence, resource plan, and a proposed seal. If hardware or parser control cannot support the protocol, stop with concrete evidence and a decision request. Do not install a cloud solution or silently change model/package. Stop for review.
