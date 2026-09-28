# P01 proposed seal

Status: **PROPOSED / READY_FOR_REVIEW**. Acceptance: **PENDING**. P01 is **not SEALED**.

- Proposal recorded: `2026-09-28T14:52:28.083807+00:00`.
- Authority: reviewed Windows/RTX 5090 P01 prompt, SHA-256 `f08794bfcf4a4f62361203f852d67e8f3735bdea9d2185fce3c43529f733e7a8`.
- Previous phase: user-conveyed P00 report-level acceptance, `reports/phases/P00_accepted_seal.md`, SHA-256 `4a888ebc0edd85b3d566d2c6071ce2799f25544999a3d4b2991baa6bddb615f5`. Coordinator did not independently inspect code or rerun tests.
- Completion: `reports/phases/P01_completion.md`, SHA-256 `07edfed83482ed63e6e219a3e6439e6c30a6f58c12ebd1ba69dc2b01bbef71c3`.
- Evidence index: `reports/phases/P01_evidence_manifest.json`, SHA-256 `b525dfba19063550c8ad96adec528574c76133de792c6e31720fdbecdea312ed`.
- Executed source/evidence commit: `683e9a3f7c5c539a3bb5d8d959b98d4c9319721f` (TaskCognition 0.1.0).
- Final corrected code/state commit: `7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322` (TaskCognition 0.1.1; supervisor integrity fix; no real rerun).
- Separate report-packet commit: locate the local Git commit containing `reports/phases/P01_packet_receipt.json`; the commit ID is supplied on delivery rather than embedded in itself.
- Checkpoint: official `Qwen/Qwen3-8B@b968826d9c46dd6066d109eabc6255188de91218`, native BF16, built-in SDPA MATH, same sampler for D/R. This is a smoke pin, not the final study freeze.
- Run: `artifacts/development/p01-windows-5090-20260928-v2`; evidence kind `development_observation`, split DEVELOPMENT.
- Outcomes: D missing FINAL wrapper retained at 0; R strict-valid native score 1; deliberate admitted R interruption retained at 0. No live valid-FINAL D success; no repaired output or favorable rerun.
- Resource reconciliation: 3 admitted, 0 unknown, 0 retries; 567 output tokens, 3,072 reserved, 5 unused slots. Conservative GPU residency 57.495063 seconds of 1,800; about 19.67 GiB additional footprint of 40 GiB.
- Validation: 62 final offline tests pass; synchronized GPU/BF16/SDPA checks pass; native scorer hand checks pass; real controlled cancellation and no-replay restart demonstrated. Immutable raw output and P00 fixture verification pass.
- Final state event: `configs/state_events/002_P01_ready_for_review.json`; P00 remains SEALED by conveyed acceptance, P01 READY_FOR_REVIEW, no next phase authorized.
- Integrity correction: unexpected worker exits without terminal evidence now retain resource charges and stop for investigation, never impute zero. All three actual workers had intact terminal results and exit 0, so none were invalidated. Historical source and package hashes remain verifiable.
- Unverified: live D valid-FINAL success, forced-kill/120-second expiry behavior, six-family cap rates, general throughput and hard resource support bounds. No statistical claim is inferred.
- Excluded activity: P02 pilot, final labels, training, AUDIT/TEST access, paid/cloud calls, quantization, model substitution, source CUDA builds, driver changes, manuscript result updates.
- Review packet: `reports/p01/P01_review_packet.zip`; external hashes/read-back result in `reports/phases/P01_packet_receipt.json`. No weights, environments, credentials, private meetings or irrelevant manuscript history.
- Next phase: NONE authorized. The P02 proposal is conditional and unexecuted. Final scientific/statistical values remain unresolved.

Reviewer acceptance must be conveyed by the user/coordinator before a P01 accepted seal or P02 activation. This proposal cannot authorize itself.
