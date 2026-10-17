# Codex handoff: P02F offline cost-boundary preflight

## Authority and intended outcome

The coordinator accepted **P02E OFFLINE DESIGN** on **2026-10-17 America/Chicago** in the accompanying `docs/P02E_acceptance_review.md`. Archive the exact review and this prompt, hash them, and record acceptance once using the existing state-event conventions. Record the actual workstation adoption timestamp separately. **P02 remains incomplete/unsealed, P03 unstarted and the study unfrozen.**

This prompt authorizes **P02F OFFLINE COST-BOUNDARY PREFLIGHT**, not a model run or adoption of a new scientific cost policy. The outcome must be a concrete, reviewable cost-contract decision and a minimal offline-tested implementation where useful. Routine reversible work within this scope needs no repeated confirmation.

Two valid stopping outcomes:

- `P02F PREFLIGHT READY_FOR_REVIEW`: the prototype and any conditional diagnostic plan are reviewable, with the exact unresolved choices clearly stated. This status never authorizes execution.
- `P02F COST_DESIGN_BLOCKED`: the evidence does not justify the proposed physical-time support or another required cost decision. Return a complete decision packet with alternatives; do not build unnecessary live machinery or run a timing study to disguise that block.

This is one bounded phase, not a mandate for repeated preflights. A documented block is useful progress when it identifies the actual scientific decision.

## Hard scope boundaries

- **Zero model/GPU work:** no model loading, feature forwards, answer generation, inference smoke calls, learned gate fitting, calibration fitting or feature normalization. CPU-only fake workers, fake clocks, contract calculations and ordinary file/process tests are allowed. Do not benchmark a new synthetic neural architecture or import inference libraries merely for a smoke test.
- Keep real dispatch false. Do not reopen or reuse the consumed P02D authorization. Any future worker and supervisor must require a separate exact-plan authorization before inference imports or device work.
- No final labels, statistical audit decisions, full-pipeline simulations, final manifest, cost/risk/sample-size freeze or P03 activation.
- Preserve accepted P02D/P02E artifacts and scientific code identities. Implement any prototype in a separate versioned P02F module; reuse reviewed helpers without silently editing their historical bytes.
- Preserve the checkpoint, native modes, BF16/SDPA MATH, original questions/default configurations, P02B instruction, sampler, 2,048 total-token cap, strict parser/native scoring and feature recipe. No KV/prefill reuse, preview, second answer, retry, repair or R-to-D rescue. Jev and live judges remain parked.
- Use task-only local commits; preserve unrelated work. No push, merge, uploads, paid resources, new infrastructure or inference dependency installation.

## 1. Verify authority and write the cost decision first

Read AGENTS.md, protocol, statistical contract, decision register, accepted P02E report/proposal, and the original/CR01 cost sections. Confirm these bindings:

| Artifact | SHA-256 |
|---|---|
| P02E review ZIP | `9f3fddc83ff26a26726623a3a568d35b71bbf61f470ce1f724fa0ccfbbbdbe0f` |
| P02E evidence index | `2cab5fc1f5e493a7ef081e948a09c753a4ae476f3220223040d4297b3e71d5e7` |
| P02E design report | `62bd6de18f851239e5833684f818072d1965a5f7da302320e258b7b610db4d24` |
| P02E next-step proposal | `3220410a1d3a0f8e9194e3114d05ef4ae779860b27179da4b604de34b2770546` |
| Accepted P02D v4 plan | `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365` |

Start with a short **cost-contract decision memo**. Define the random cost variable, units, service policy, charging boundary and what the resulting paper claim would mean. Separate observed facts, proposed implementation, mathematical assumptions and unverified platform assumptions.

Evaluate the two existing protocol-permitted choices:

1. **Actual all-in hardware service time.** Identify the exact enforced controls and any platform assumptions needed for finite support, including loading, CPU work, GPU cancellation, response handling and safe termination. Explain whether existing evidence supports those assumptions. A configured timeout, successful kill/wait, empirical maximum, reservation or total-run ceiling is insufficient by itself. Finite support cannot be proved by adding more timing samples. Do not assume a hard-real-time platform guarantee that has not been established.
2. **An explicit monetary reference token/call tariff.** If necessary, present a concrete schedule structure, non-overlapping charge categories, bounded counts and source/owner required for each rate. Explain that it defines price under a declared schedule, not actual physical-time efficiency or fees paid on this workstation. Do not invent a provider price, choose rates to favor TaskCognition, or call reserved seconds realized service time. Where justified rates are missing, name the missing decision rather than marking the ledger complete.

Keep the current empirical-Bernstein audit and declared cost-support requirement. No clipping, changed concentration bound, empirical-support substitution or third metric may be adopted silently. An alternative beyond the current protocol needs a separately reviewed change request.

Return one recommended route, its limitations, and the precise user/coordinator decision still needed. Do not adopt that decision. If physical-time support is unsupported, say so directly and do not make the 24-answer diagnostic the supposed remedy. It may measure a boundary, but cannot solve that mathematical gap.

## 2. Specify and instrument one query without hidden charges

Prepare the proposed **cold isolated process per query** as a prototype, not an adopted final serving policy. State that process startup is cold while other cache states are unspecified unless measured and governed. Do not build a persistent serving stack in this phase. A persistent alternative may be described briefly if materially relevant.

Define a monotonic timeline that covers first charged validation/admission work through mandatory response handling and confirmed safe process stop. Explicitly assign:

- startup, necessary source/checkpoint validation and model initialization;
- original-text tokenization, the input-only feature forward and cheap observables;
- a future CPU head/calibration interface, action selection and dispatch;
- the sole selected answer's prompt preparation and generation;
- strict output handling, cancellation, response publication and cleanup;
- pre-admission failures and unresolved processes/costs.

Separate gold-dependent evaluation and growing research archival verification from serving work only if they truly are not required to serve the query. Preserve their actual research costs. Mandatory integrity checks cannot be relabeled optional collection work to lower the measured cost. Historical ledger rescanning should not be an accidental dependency of the proposed serving timer; any redesigned online state validation must preserve admission, integrity and no-replay semantics.

Provide a non-overlapping event/measurement schema. Total service time and nested components must reconcile; inclusive durations must not be added twice. Unknown residuals remain explicit. The prototype must record actual time including overshoot. A reservation is a control field, not a replacement for observed expenditure or proof of hard support.

Use a fixed action for the cost-only prototype. Do not label it TaskCognition, winner or factorized inference. Define a common gate interface for those later methods, but leave architecture, parameter parity, calibration procedure and actual head cost unresolved until their planned review. A zero-duration placeholder is **not** a measured gate charge. Active-gate D queries incur feature/head work; audit-fallback direct bypasses the gate completely.

The proposed feature and answer may share one loaded checkpoint within a query, with no reused past keys or answer information in features. Specify fresh masks/IDs, native mode serialization and a full reseed immediately before the single answer. Offline tests can check orchestration and state isolation; they do not establish numerical equivalence on GPU. Preserve unmodified scoring behavior outside the metered serving boundary as appropriate.

Keep feature warm-ups separately counted and timed. The proposed two extra passes in the first worker are charged research work; disclose whether they affect that query's timing. Do not silently drop the first query or treat warm-up-adjusted time as a final reference. Every worker performing the actual service feature still pays for that pass.

## 3. Resolve the meaning of calibration before preparing a live plan

The P02E proposal includes a feature pass before **every** answer and a fixed dispatcher. Thus it measures neither gate-bypassed always-D/always-R references nor a learned gate. Label it **service-boundary diagnostic**. It cannot alone freeze c_D_ref, c_R_ref or beta, and subtraction of component timers is not evidence from an unmeasured bypass path.

Document the eventual reference-calibration design separately: a common service/startup/failure policy, outcome-independent balanced inputs, directly measured gate-bypassed D/R paths, a reviewed reference aggregation rule, and the real gate cost for active learned methods. Preserve `beta = c_D_ref + 0.5*(c_R_ref-c_D_ref)` as a common budget. No method-specific enlargement or references from current collection-worker means.

Do not quietly enlarge the proposed run to collect those missing reference paths. If another path or call count is necessary, explain the exact delta and its purpose in an **unapproved proposal**. Do not claim that this checkpoint completes calibration when it only prepares instrumentation.

Conditional preparation of the existing diagnostic is permitted only if the memo identifies a useful measurement question, the instrumentation is reviewable, and the unresolved cost decision is prominently recorded. Its existing envelope is **not an execution approval**:

| Field | Offline preparation limit |
|---|---|
| Inputs | 12 existing P02D inputs: indices 0 and 1 in each family; zero fresh inputs |
| Answers | K=1/mode; 12 D + 12 R = 24; new independent namespace/streams |
| Features | 24 service passes + 2 charged warm-ups = 26; at most 53,248 input positions |
| Output | 2,048 tokens/call; total reservation 49,152 |
| Workers | 24 sequential fresh processes, one load and one answer per process |
| Operational ceilings | 5,400 worker seconds; 7,200 wall seconds; 128 MiB including review evidence |
| Deadlines | Load 150 s; feature 120 s; answer 120 s; cancellation grace 10 s; cleanup 30 s |
| Admission reservation | 450 s ordinary query; 690 s first worker including two extra passes |
| Retry/replacement/answer warm-up | Zero / zero / zero |

Verify that reservations conservatively cover the intended timeline and that counts include every pass. These operational numbers do not establish c_max. The aggregate ceiling need not cover every slot at every deadline; insufficient remaining budget must yield a clearly incomplete run without extension.

If preparing a plan is justified, create an immutable **pending** plan, exact source/request/environment bindings and a separate pending execution request. Do not create an active authorization. Public supervisor and worker paths must reject absent, stale, wrong-hash or consumed authorization before inference imports. Do not alter the accepted P02D plan or materialize any final-label inputs. If the design is blocked, omit executable plan preparation and state why; do not manufacture a READY execution request.

## 4. Focused offline verification

Use fake workers and deterministic clocks to cover the newly introduced risks, reusing accepted integrity tests where appropriate:

- authorization rejection before any model/device activity, including direct child invocation;
- one load, the scheduled input-only passes and exactly one answer per query; explicit no-cache/no-preview isolation and answer RNG reset;
- feature failure prevents answer admission; known answer failure is retained under the existing scoring contract; software/corrupt evidence stops unscored;
- reservation exhaustion stops before additional admission; consumed/unknown slots cannot replay; timeout or crash costs remain recorded;
- response and safe-stop accounting, nested-timer reconciliation, observable overshoot and unknown termination state;
- atomic publication and safe reading of request/result/control records under concurrency;
- fixed-action stub cannot be reported as a fitted gate or all-in reference calibration; bypass-path costs cannot be synthesized by subtracting timers.

Test the minimal prototype, not a broad serving rewrite. If the hardware support argument fails, fake-clock success does not repair it. Report that difference explicitly. No model smoke test, full regression run without a specific need, architecture search or numerical GPU comparison.

## 5. Deliver a decision-ready checkpoint

Write a coherent packet under `reports/p02f/` and `reports/phases/P02F_preflight_completion.md` containing:

1. Cost-contract decision memo with recommended route, exact unresolved decision, proposed scope of the resulting claim and support argument or blocker.
2. One-query lifecycle, accounting/instrumentation contract, minimal prototype sources/diff and focused check results. Label fixture measurements and exclude them from empirical result tables.
3. Diagnostic-versus-reference-calibration gap table. Include pending diagnostic plan/request only if the conditional preparation criteria above hold; otherwise include the concrete blocked-path alternative.
4. Reproducibility commands, CPU/wall preparation costs, immutable source bindings and verified review ZIP/index/external receipt. Reference accepted packet hashes without recursive ZIP nesting.

Archive P02E acceptance and update the decision ledger with evidence and proposals, not fabricated resolutions. Leave all normative tolerances, support bounds, beta, final n/K and resource commitments unfrozen. Preserve both mandatory learned baselines and the all-three success criterion.

The final completion message must state whether the next decision is **cost-metric selection**, **preflight/source acceptance**, or a later **explicit bounded execution approval**, and why. Do not imply a generic READY label answers all three. Finish with dispatch false; zero model work; P02 incomplete/unsealed; P03 unstarted. Return to review at this point.
