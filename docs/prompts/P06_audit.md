# P06 prompt: one held-out audit and deployment freeze

Active authority: original reference PDF + approved `TaskCognition-CR01-2026-10-05-v1` + C01-C03. This document does not authorize a new phase or live run.

Execute only after accepted P05 review. Implement P06 only. All candidates must already be frozen. No TEST outcomes may be generated or inspected.

## Work

1. Verify study/candidate/analysis hashes and audit split identity/size. Establish that the audit sample is balanced and independent under the frozen cluster design. Do not change any sample count or threshold based on observed outcomes.
2. Log every candidate's audit actions from input only, then collect the frozen K D/R draws per audit input. Reuse the same audit rollout table for every method to ensure matched information. Preserve scheduled failures and integrity controls. No candidate changes after the first audit result is visible.
3. Form complete B/Z/C/Delta input-cluster rows and verify their declared ranges. Compute exact frozen empirical-Bernstein bounds and all four acceptance checks. Use live gate charges including features, not zero from offline embedding reuse.
4. Report per-method score, cost, spoilage and denominator bounds; adequacy fields; package failures; and acceptance/fallback reasons. Missing/invalid/mismatched audit evidence fails closed. Distinguish a valid statistical rejection from invalid experiment records.
5. Freeze deployment records: candidate enabled only if all checks pass; otherwise always-direct with gate bypassed. Verify fallback does not execute encoder/MLP and does not mean rescuing a failed R generation.
6. Save immutable audit and deployment manifests referencing all candidate and study hashes. Prepare the untouched TEST execution plan from already frozen rules.

## Exit criteria

- Exactly one audit per frozen method, no retuning/re-audit or audit-based enlargement.
- All four decisions and their raw numerical inputs are reproducible.
- Failures trigger declared deployment fallback with reasons.
- Deployment artifacts are immutable; TEST is still unexposed.
- No language suggesting conformal, pointwise, shift-wide, or cross-method familywise guarantees.

Write `reports/phases/P06_completion.md`, full audit/adequacy tables, deployment manifest and proposed seal. Stop for review even if every method fails. A statistically valid fallback can seal this phase; it is not an implementation success claim for TaskCognition. If TC deploys direct, explicitly state that superiority over direct cannot be established by identical actions.
