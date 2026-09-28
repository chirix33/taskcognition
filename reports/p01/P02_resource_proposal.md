# Conditional P02 resource proposal

Evidence kind: `development_observation` for measurements; proposals below are unexecuted.
P02 is not authorized by the P01 run.

The initial D/R pair used the same tiny original-renderer number_sorting input, with
209/205 serialized input tokens respectively. D emitted 17 tokens in 1.079 s; R emitted
548 tokens in 17.879 s. These imply 15.75 and 30.65 output tokens/s **for these two
requests only**, including prefill and per-token ledger/stream synchronization overhead.
Per-process checkpoint load/transfer took 7.075-7.217 s. End-to-end worker durations were
11.990 s and 28.471 s. Peak PyTorch allocated memory reached 16,548,647,424 bytes
(15.41 GiB), reserved 16,689,135,616 bytes (15.54 GiB). Runtime+checkpoint footprint was
about 19.67 GiB. No long-input, other-family, batching, or persistent-worker throughput
was measured. These are not six-family completion rates or confidence estimates.

The D wrapper failure is unresolved live evidence. Before a cap pilot, the reviewed
P02 plan should name a small wrapper/interface diagnostic on fresh DEVELOPMENT inputs,
retain the original renderer, preserve any package changes and outcomes, and lock the
strict completion rule. Do not weaken parsing to retroactively pass P01 or filter tasks
based on correctness. The deliberate interruption is not a spontaneous completion-rate
failure and must not enter a cap-study denominator disguised as an ordinary draw.

## Proposed first bounded development slice

After P01 acceptance and an explicit P02 prompt, propose **one prespecified input per
family, K=2 per mode: 24 generations**, cap 1,024 each, at most 24,576 output tokens.
This is an integration/measurement slice across six original renderers and scorers,
not an adequately precise 99% cap certification or a high-repeat study. No final
sample size, K, budget, timeout or cap is selected by this proposal.

At the tiny-smoke 15.75-30.65 tokens/s rates, reaching every cap would suggest roughly
13-26 minutes of generation, plus about 3 minutes of per-process loading at observed
load times. This extrapolation may be wrong for other families/lengths. A prospective
**90-minute GPU-residency ceiling**, **2-hour wall ceiling** excluding downloads, and
**0.5 GiB new evidence allowance** would be a conservative proposal to review, not a
hard support theorem or authorization. If 120-second per-request smoke timeouts were
retained provisionally, 24 such deadlines alone sum to 48 minutes before load/cancel
overhead. Timeout validity and actual device cancellation must be revisited in P02.

The formal 12-cell cap study still needs a predeclared input/repeat denominator, resource
ceiling, and identical strict-valid-FINAL rule for all cells at 1,024 and, if necessary,
2,048. No recommendation for that denominator is inferred from three P01 requests.
The planned 15,000-generation high-repeat example remains a placeholder and was not
launched. A 40-GiB P01 allowance is not a blanket full-study compute or storage budget.

P02 should first obtain the user-confirmed development GPU/wall/disk ceiling, preserve
the P01 package as a diagnostic baseline, set disjoint DEVELOPMENT identities, and
measure the six-family distribution. Original-source/raw-output backup destination,
final cost ledger/support bounds and remaining D05-D17 decisions remain unresolved.
