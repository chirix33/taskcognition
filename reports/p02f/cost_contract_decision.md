# P02F cost-contract decision memo

Status: **COST_DESIGN_BLOCKED**. Written before the fixture prototype. This is a proposal and support assessment, not adoption of a cost metric. The next decision is **cost-metric selection**, not execution approval.

Recommend pursuing the protocol-permitted **explicit monetary token/call reference tariff**, conditional on the user accepting its narrower scientific interpretation and supplying or appointing an accountable owner for justified rates. Do not run the 24-answer service-boundary diagnostic to try to establish physical-time support. No numerical tariff is invented here. If the price-relative question is scientifically unacceptable, keep the present physical-time route blocked; changing the statistical requirement would need a separately reviewed amendment, not another timing sample.

## Authority and observed facts

P02E was accepted on 2026-10-17 America/Chicago; event 025 records the actual workstation adoption separately. Its 63 indexed files matched the accepted ZIP and current bytes before state changes. Its reproduction compared 17 files: **15 regenerated outputs plus two copied declaration/provenance inputs**, as clarified by the coordinator. This corrects the description, not the historical artifacts.

The original PDF page 3, equations 10–11, permits a single monetary token/call schedule or hardware service time. Pages 5–6, equations 16–18, require an analytically justified frozen cost range. Active CR01 TeX and protocol retain these requirements. CR01 changes only the cap/eligibility branch. No conflict licenses a third metric, clipped costs, a different concentration rule or empirical-support substitution. The generic preview charging phrase does not authorize previews.

Accepted P02D measured 193 conservative session intervals totaling 11,560.2217413 seconds and 12,836.8229112 execution-wall seconds. These are neither GPU kernel times nor hard maxima. Known safe cleanup on these sessions is evidence of observed handling, not a guarantee for all possible executions. P02E identified growing integrity/scanning overhead without separately timing every cause. No new physical timing evidence is collected in P02F.

## Route 1: actual hardware service time — unsupported support assumption

Define a prospective random variable C_time(X,U,E) in **seconds**: the monotonic interval from the first charged query validation/admission work through mandatory response handling and confirmed safe stop, under a declared cold-process policy. X is the input, U covers sampled answer randomness, and E covers the declared execution environment and scheduling/failure conditions. Serial non-overlapping phases partition the interval; concurrent nested component durations are descriptive and never added again. Failed attempts are included. If stop cannot be confirmed, only an observed lower bound exists and the full cost is unresolved; it is not a completed cost row.

“Cold” means a new isolated process and a charged checkpoint load per query. It does **not** assert cold OS file/page cache, disk cache, driver state, GPU power state or thermal conditions. Those states remain unspecified unless a future service policy measures and governs them. The same policy must apply to learned methods and gate-bypassed references.

Under this metric a supported paper claim would concern expected all-in query service time on that declared hardware/policy, including every active gate and selected answer. It would not establish pure GPU efficiency, energy savings, paid price efficiency or universal hardware performance.

Existing enforceable controls constrain requested output tokens, admitted call/forward counts, known input positions, retry count J=0, source identity and admission order. Software has provisional load/feature/answer deadlines, cancellation grace, terminate/wait procedures and reservations. These do not establish an upper bound on scheduling delays, file/driver operations, blocked synchronization, device cancellation, process termination, response persistence or parent failure. CPU head architecture and operation limits are also unresolved. Finite wait calls can return without establishing safe stop; charging ends only at safe stop, not at the wait deadline.

A finite deterministic c_max for this actual-time variable would require justified upper bounds across all charged CPU, filesystem, scheduler, model initialization, GPU execution/cancellation, response and cleanup work, plus failure/recovery and a reliable monotonic observer. No such hard-real-time platform contract is in the reviewed evidence. Do not assume one for this Windows workstation. If a process may remain active indefinitely, the service variable may lack finite support or be unresolved; renaming a timeout as a completed cost does not fix it. More observations cannot prove an absolute support bound.

Therefore **D08/D09 remain unresolved**. The physical-time audit route is blocked under its current support requirement. This is a cost-design block, not a whole-study infeasibility finding. Do not discard slow cases, clip overshoot, condition the analysis on successful cleanup or use 450/690 reserved seconds as realized cost. If a prospective support assumption is violated, preserve the observations and block the affected evidence/design under an approved invalidation policy; direct fallback cannot repair invalid accounting.

## Route 2: explicit monetary reference tariff — decision needed

Define C_price(X,U) in a named reference currency under a versioned, reviewed schedule. It prices the allowed service operations; physical time remains separately reported research/serving evidence. This defines a price-relative constrained score claim for the specified bounded packages. It does **not** mean fees were paid locally, that a provider offers this exact service, or that hardware-time efficiency improved.

Concrete schedule structure, with **all rates currently unset**:

1. r_start per query attempt, at most one with J=0. Bundles first validation, process creation, required source/checkpoint identity checks, one initialization and necessary admission bookkeeping. These items cannot also be charged in the feature/answer bundles.
2. r_feature times raw-question token positions, at most 2,048 for the single live service feature pass on an active-gate query. Bundles original-text tokenization, the fixed same-checkpoint decoder feature forward and cheap observables; excludes startup, head/calibration and answer computation. No cached-training-vector credit. Two diagnostic-only warm-ups are separately priced research forwards, never silently folded into every query's deployment price.
3. r_head(M) for one CPU head/calibration/action evaluation with reviewed architecture and operation envelope M. Present M_max and this rate are **missing**; zero is not a measurement. The same source/pricing rule and parameter-parity requirements apply to TC, winner and factorized methods. Fixed-action prototype dispatch is not this head.
4. r_prefill times selected serialized answer input positions, at most 2,048 under the proposed input ceiling. Covers the sole D or R answer prompt preparation/prefill only. No KV reuse or feature-prefill credit.
5. r_output times actual recorded new answer tokens, at most 2,048 including thinking and final. D/R share the checkpoint and matched package; any mode-specific tariff would require independent justification, not outcome-driven rates.
6. r_terminal per attempted query, at most one. Bundles strict channel/FINAL/syntax handling, response/control publication, dispatch control, cancellation, mandatory serving integrity and cleanup, whether success or failure. Startup admission bookkeeping is excluded. Gold-dependent native evaluation and research packet generation are outside serving price and remain separately charged research work.

With finite nonnegative reviewed rates and truthful count records, one conservative price bound for an active-gate query would be

`r_start + 2048*r_feature + max_{M<=M_max} r_head(M) + 2048*r_prefill + 2048*r_output + r_terminal`.

For a gate-bypassed reference omit the feature/head charges, not startup/terminal work. A shared initialization is charged once. A zero lower bound is a conservative mathematical option if every rate is nonnegative; neither bound is adopted now. No price is computed while required rates or M_max are missing. Caps on discrete service requests do not prove bounded physical time.

Every rate needs an owner, source, date/version, currency, unit, exact inclusions, failure/partial-token rule and validity period. The coordinator/user must identify an applicable published contract/quotation **or** explicitly own a normative reference-price schedule and its scientific rationale. A provider generation-token price alone does not price local feature decoding, initialization and CPU gates. A normative schedule must be labeled as such, not attributed to a nonexistent provider. No external price lookup or unsupported current price claim is needed or performed in this checkpoint.

Terminal fixed pricing can bound the contractual price of a failure only if the chosen schedule expressly covers it; it cannot erase physical runaway work or make unresolved result evidence valid. Unknown output counts, corrupt billing records, unexpected operations or support overflow remain integrity/design incidents pending reconciliation, not zero-price draws. Any rule for billing unknown usage must be specified prospectively by the rate owner. Do not silently bill maximum reserved tokens as if they were observed token counts.

## Exact decision for the user/coordinator

Decide whether the primary study may use a **declared monetary reference-price schedule**, accepting the price-relative interpretation above. If yes, designate a rate owner/source and require the six categories, failure policy and gate envelope to be justified before adopting rates or c_min/c_max. If no, retain the physical-time support block or request an explicit scientific amendment. Do not respond by authorizing more timing samples as a proof of support.

This recommendation adopts neither route, rates nor bounds. The common budget stays `beta=c_D_ref+0.5*(c_R_ref-c_D_ref)`. Reference charges must come from the same declared service/failure/price policy, with gate-bypassed D/R measured directly as applicable, and be frozen before tuning. Preserve the four audit inequalities and three required final comparisons. No alpha, b_min, delta_score, beta, final n/K, feature freeze, rate schedule or spending authority is set here.

## Consequence for this checkpoint

Omit executable diagnostic plan preparation and an execution request. The measurement question—how much time belongs to mandatory one-query service versus growing research machinery—is useful, but is not the next unresolved scientific decision. A small **fixture-only** lifecycle/accounting implementation will test record semantics, isolation and honest incomplete outcomes. It will have no inference backend and both public live entry points will reject. Its synthetic durations are not empirical timings or a proof of support. Source review remains useful; source acceptance alone cannot authorize model work or choose the cost metric.
