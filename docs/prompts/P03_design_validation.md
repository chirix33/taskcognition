# P03 prompt: validate the full experimental design

Execute only after accepted P02 review. Implement P03 only using DEVELOPMENT observations, fixtures, and simulations. Do not generate final labels. A cap-infeasible study cannot proceed through this prompt.

## Work

1. Implement the scientific core end to end on development/synthetic partitions: train TC/winner/factorized, calibrate/select on a separate simulated tune partition, freeze one candidate per method, audit, choose pass/fallback deployments, and compute final paired test contrasts. Reuse production code paths wherever possible. Do not simulate only an oracle audit.
2. Build all three gate methods with the same input information and trainable-parameter/search/optimizer/calibration budgets. Freeze the proposed architecture grid, loss-head weighting, initialization trials, training budget, early stopping role, calibration options, threshold grid, and tie-break order. Fit all learned transforms only on each simulated TRAIN partition. Keep the factorized baseline strong and faithful.
3. Verify estimator formulas, empirical-Bernstein ranges/constants/directions, independent nonidentical row assumptions, intersection-union scope, 10,000-resample paired cluster procedure, and zero-denominator behavior against primary references. Write an equation-to-code derivation memo. Implement the analytical anchors and negative controls in the statistical contract.
4. Validate the cost ledger and analytical support bound, including live encoder, features, MLP, calibration, attempts, answer, timeout/cancellation behavior, and warm-up/cache policy. If actual bounded service-time accounting is not defensible, propose an explicitly declared permitted ledger before freeze. Never winsorize slow cases to fit a claimed support.
5. Predeclare the design grid, scenario suite, replication counts/Monte Carlo precision goal, and selection criterion before comparing simulated methods. Simulate null, beneficial, harmful, near-boundary, costly, low-denominator, weak-feature and failure-heavy regimes, preserving within-input variation and plausible score-cost association. Avoid latent/input overlap across simulated split roles. Explain extrapolation from the finite pilot.
6. Report useful enablement, unsafe false enablement, fallback, interval widths, conditional AND unconditional power/detectable effects. Include uncertainty for simulation proportions; no theoretical guarantee inferred from a small Monte Carlo run.
7. Propose concrete K, train/tune/audit/test sizes, alpha, b_min, delta_score, resource ceiling, input limits, cost rule/bounds, reference charges/beta, and all randomness/numerical conventions. Keep gamma=.05, rho=.5 and primary bootstrap count=10,000 as prescribed. Values require review before final freeze; do not choose tolerances to manufacture TC superiority. Show resource/power tradeoffs and plausible alternatives.
8. Build the secondary analysis registry: redraw and partial-credit analyses, per-family reporting, random/count/family/oracle references, package-faithful sampler sensitivity, renderer checks, LLMThinkBench, independently generated diagnostic. Pin exact data/access/license/validation/analysis rules where feasible. Mark unavailable items explicitly and propose any change to the paper's planned scope for review. Jev/live judges stay parked.
9. Exercise the complete fail-closed stage flow with fixtures: hash mismatch, missing family, corrupted artifact, no feasible tune candidate, no R exposure, audit fail, and identical deployed policies. A predeclared no-feasible-candidate rule can serialize an all-direct candidate for uniform audit bookkeeping; it cannot search beyond the declared budget.

## Exit criteria

- All three implementations and full pipeline run on nonfinal evidence with fair resource accounting.
- Statistical assumptions and code are checked; no unsupported certificate language.
- A scientifically informative design is feasible within a presented resource envelope, OR limitations/infeasibility are reported honestly.
- Every required freeze field has a concrete proposal and provenance; unresolved scientific/resource choices are listed for user/coordinator review.
- Selection and secondary analysis rules are written before final outcomes.

Deliver `reports/phases/P03_completion.md`, design proposal, derivation memo, simulation tables, resource estimate, secondary registry, and proposed seal. Stop. This phase proposes the design; it does not authorize final rollouts or automatically accept its own values.
