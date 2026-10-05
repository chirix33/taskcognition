# Vertical phase roadmap

Active authority: original reference PDF + approved `TaskCognition-CR01-2026-10-05-v1` + C01-C03. This document does not authorize a new phase or live run.

Every phase produces an executable slice, tests for its scientific risks, a completion report, and a review decision. This is not a license to execute all phases in one Codex session.

| Phase | Usable result at completion | Main evidence | Progression condition |
|---|---|---|---|
| P00 | Repository, workstation inventory, contracts, offline fixture pipeline | Source hashes, environment inventory, fixture provenance, scope checks | Bootstrap reviewed |
| P01 | One real local Qwen D/R request path | Raw outputs, serialized modes, parser and interruption evidence, measured memory | Same checkpoint works in both modes |
| P02 | Six-family development pilot with labels and costs | 12-cell descriptive completion at fixed 2,048 cap, repeat estimates, workload estimate | Measurements trustworthy; remaining feature/cost/design requirements reviewed |
| P03 | End-to-end development simulation and study design | Power/false-enable/fallback reports, cost-bound derivation, locked decision proposal | Scientifically feasible design within user resources |
| P04 | Frozen study plus complete TRAIN/TUNE rollout tables | Immutable manifests, disjointness and completeness checks, collection report | Final datasets valid; held-out outcomes untouched |
| P05 | Three trained, calibrated, tune-selected candidate artifacts | Resource parity table, candidate hashes, selection trace | One frozen candidate per learned method |
| P06 | Independent audit and immutable deployment decisions | Four bounds per method; pass/fallback reasons | Valid audit process, regardless of candidate success |
| P07 | Final primary test and claim decision | Frozen action logs, full paired evidence, three lower bounds | Evidence valid; supported/not-supported status explicit |
| P08 | Prespecified secondary analyses and error accounting | Family, redraw, partial-credit, robustness and failure reports | Interpretations stay within their evidence |
| P09 | Evidence-backed manuscript and reproducibility handoff | Generated tables/figures, claim ledger, compiled manuscript or marked replacement draft | Every claim traceable; limitations and nulls retained |

## Review loop

Codex produces `reports/phases/PXX_completion.md` and a candidate seal record. The user sends those to the coordinating assistant. The assistant checks phase criteria, requests targeted repairs if needed, and recommends acceptance or a justified stop. The user's conveyed acceptance seals the phase. The next phase prompt is then issued with any evidence-driven adjustments.

Proposed statuses: `NOT_STARTED`, `IN_PROGRESS`, `READY_FOR_REVIEW`, `SEALED`, `BLOCKED`, `STUDY_STOPPED`. A valid negative scientific result can still belong to a sealed engineering phase.

## How phases stop

- P01 hardware incompatibility: report concrete requirements and available alternatives consistent with scope; no model replacement or cloud fallback.
- P02 under CR01: low completion at the fixed 2,048 cap is reported, not an automatic eligibility stop. Integrity failures, unresolved required contracts and resource exhaustion still stop the affected work. Final labels await P03 design review and P04 freeze.
- P03 no adequately informative affordable design: report attainable precision/power and a resource decision. Do not label an underpowered run confirmatory by default.
- P06 audit failure: that method deploys always-direct. This is an expected branch, not a reason to tune again. P07 remains useful if the study can validly continue; the primary superiority claim cannot succeed if TC deploys always-direct.
- P07 any required contrast fails: primary claim is not established. Complete prespecified reporting; do not search for a favorable replacement endpoint.

## Frozen stages versus sealed phases

Phase sealing is human review of completed work. Scientific freezing is an immutable contract protecting a later inference. Both are required, but they serve different purposes.

Avoid circular manifests: P04 writes immutable `study_manifest.json`, including all package, design, and selection rules plus the future record schema. P05 adds a separate immutable `candidate_manifest.json` referencing the study hash. P06 adds `deployment_manifest.json` referencing both. P07 adds a test evidence manifest. Do not rewrite an older manifest to insert later hashes. A final index can hash all completed records without altering them.

## Resource ladder

P00 inventory -> P01 tiny smoke -> P02 bounded pilot -> P03 affordable full-design proposal -> P04 main labels. No expensive run starts without a declared count, token ceiling, storage estimate, and cancellation/resumption policy.

At the first P02 review, obtain a user-confirmed ceiling for development work; by P03 obtain the full-study GPU-hour/wall-time and storage ceiling. These are phase decisions, not questions that prevent P00. No paid service is implicitly authorized. Report actual research expenditure separately from the paper's per-query deployment cost.

## Verification emphasis

Spend testing effort where a defect would invalidate inference: native-mode control, strict parsing, repeat independence, split leaks, weighting, all-in cost, failure retention, resumption, statistical direction/ranges, candidate immutability, paired bootstrapping, and paper-table provenance. Do not add a web application, dashboard, cluster scheduler, or elaborate platform unless the experiment requires it.
