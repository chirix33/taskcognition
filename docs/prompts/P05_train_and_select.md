# P05 prompt: train, calibrate, and freeze three candidates

Active authority: original reference PDF + approved `TaskCognition-CR01-2026-10-05-v1` + C01-C03. This document does not authorize a new phase or live run.

Execute only after accepted P04 review. Implement P05 only. Use TRAIN to fit and TUNE to calibrate/select exactly as frozen. AUDIT and TEST outcomes remain inaccessible.

## Work

1. Verify study/data/feature hashes, split guards and valid frozen design. Fit train-only normalization/transforms and all three matched models using the prespecified seeds, parameter tolerances, optimizer budgets, loss weighting, and candidate grid. Do not add search trials after inspecting winners.
2. TaskCognition uses squared loss for continuous benefit and fractional-label log loss for joint harm. Winner uses W=1{mean_R>mean_D}, exact ties D. Factorized predicts p_D,p_R,mu_D,mu_R and reconstructs the same benefit/harm quantities. Do not collapse partial-credit means into perfect-correctness probabilities.
3. Apply only the frozen calibration procedures on TUNE. Select one candidate per method by the same constrained score objective, common beta/alpha, frozen finite candidate grids and tie-breaks. Charge live gate work. Report tuning failures and rejected candidates. Do not use empirical-Bernstein AUDIT outcomes as a tune criterion.
4. If a method has no feasible tune candidate, apply the predeclared no-candidate handling. Do not introduce post-hoc retries, extra thresholds, or extra model capacity.
5. Write immutable candidate artifacts containing weights, transforms, calibration, thresholds, exact feature identity, parameter/training/search budgets, and hashes linked to the base study. Freeze all three candidates before any audit exposure.
6. Validate integrated deployment on DEVELOPMENT inputs only: question -> frozen features -> gate -> exactly one selected Qwen generation -> strict parser -> score/ledger. Perform one-call-count and gate-cost checks without altering the finalized packages. No direct answer preview.
7. Produce an auditable parity and selection table, learning/calibration diagnostics, trial ledger, candidate feature permissions, and one manifest listing all frozen candidates.

## Exit criteria

- Three faithful, matched methods are implemented and fitted using their assigned data roles.
- Complete candidate search is accounted for; all compared methods receive the frozen opportunities.
- Exactly one selected candidate/declared degenerate candidate per method is immutable.
- One-call serving integration is demonstrated on development data with full feature cost.
- No audit/test data access, refitting on TRAIN+TUNE, or late search expansion.

Write `reports/phases/P05_completion.md`, parity/selection reports and candidate manifest. Stop for review. Candidate score on TUNE is not confirmatory evidence.
