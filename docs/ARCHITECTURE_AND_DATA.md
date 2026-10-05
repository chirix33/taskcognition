# Architecture and data contracts

Active authority: original reference PDF + approved `TaskCognition-CR01-2026-10-05-v1` + C01-C03. This document does not authorize a new phase or live run.

Implementation direction, not pre-existing code. Codex may adjust module organization for an existing repository while preserving interfaces and invariants.

## Minimal layout

```
AGENTS.md
docs/                       # supplied contracts, prompts, decision ledger
reference/                  # manuscript and source fingerprints
src/taskcognition/
  cli.py                    # stage-aware commands
  contracts.py              # validated records and manifest types
  stages.py                 # stage guards, phase status, hash validation
  datasets.py               # six pinned generators and native scorers
  inference.py              # frozen Qwen package adapter
  parsing.py                # native channels -> FINAL -> native syntax
  ledger.py                 # dispatch/admission, resumption, costs
  features.py               # frozen input-only encoder and cheap features
  targets.py                # one aggregate row per input
  gates.py                  # TC, winner, factorized
  selection.py              # train/tune calibration and frozen selection
  audit.py                  # fixed-candidate audit only
  evaluation.py             # action-first offline test and cluster intervals
  simulation.py             # development-only full pipeline
  reporting.py              # data-derived tables, figures, claim ledger
configs/                    # versioned development and frozen designs
tests/                      # fixtures and meaningful scientific checks
reports/phases/             # compact material sent back for review
artifacts/{fixtures,development,final}/
paper/                      # recovered source or labeled reconstruction
```

Use a small installable Python package, typed records, JSON/JSONL plus Parquet/CSV where useful, and a project-local dependency lock. Avoid a database/server unless necessary. Generated large files are content-addressed and not committed to ordinary git; commit their manifests, code, and small reports. Record a user-chosen backup location before irreplaceable final rollouts. Git alone does not preserve ignored raw outputs.

## Proposed CLI contract

Expose a consistent `python -m taskcognition ...` interface. Proposed commands are names to implement, not commands claimed to exist:

- `doctor`: hardware/dependency/source inventory.
- `fixture-run`: synthetic offline package-to-report path.
- `smoke`: tiny local model run on DEVELOPMENT inputs.
- `develop`: pilot, cap report, repeat estimates, throughput and cost.
- `simulate`: development-only design selection pipeline.
- `freeze`: validate decisions and create immutable study manifest.
- `collect --split train|tune|audit|test`: stage guards and frozen draw plan.
- `train`, `select`: train-only fitting; tune-only calibration/selection.
- `freeze-candidates`, `audit`, `freeze-deployments`.
- `evaluate`, `secondary`, `report`, `verify-artifacts`.

All execution commands have a dry-run/resource-plan path, machine-readable status, exact manifest references, explicit output directory, and resumable run ID. Actual flags may differ; document and test them. Fail if required design values remain null/TBD.

## Records

| Record | Required content |
|---|---|
| Study manifest | Study ID, source hash, code revision, environment lock, package fingerprints, design values, scalar ledger, bounds, splits, RNG scheme, selection/analysis rules, secondary registry |
| Input record | Stable ID, split, family for analysis, latent fingerprint, exact prompt, input token length, generation seed/config, scorer reference, gold reference in outcome-only store |
| Gate input | Input ID plus permitted text/features only; schema has no family, answer, trace, or generator metadata |
| Attempt event | Run ID, input ID, package ID, draw index, stream ID, attempt number, request hash, dispatch/admission timestamps and state, response/timeout details, incurred resources |
| Draw result | Evidence kind, frozen package hash, raw artifact hash/path, token IDs/text, final payload, finish reason, failure taxonomy, native score, correctness, all attempts' costs |
| Input aggregate | K per mode, both score means/perfect rates, benefit, joint harm, direct-redraw estimate, partial-decline estimates, cost means, status counts |
| Candidate | Study/feature/preprocessing/training hashes, method, weights hash, calibration hash, thresholds, trainable size, search trace, tie-break result |
| Action log | Input ID, method, deployment/candidate hash, timestamp/order, chosen D/R, route reason; created before answer generation |
| Audit report | All cluster rows and bounds, adequacy fields, all four decisions, fallback reason, integrity checks |
| Evidence table | Data hash, code/config hash, generation command, seed if relevant, units, population, uncertainty method, evidence kind |

Protect gold outcomes by separate schemas and loader APIs, not merely "do not use" comments. Input IDs may be used as keys but never predictive features. Features/normalizers are train-fitted or frozen before fitting. Balance families in analysis; no family identifier in the gate forward call.

## RNG and independence

Derive deterministic stream identifiers with a documented cryptographic hash or SeedSequence from `(study_id, split, input_id, package, draw_index)` plus a frozen root seed. Do not use Python's salted `hash()`. Keep dataset generation RNG distinct from model sampling, gate initialization, random-reference routing, and bootstrap RNG. D and R may share input identity but not a sampling stream. Use declared separate streams for alternative sampler analyses.

Run scheduling must not pick examples based on outcomes. Interleave modes and families under an outcome-independent plan to reduce hardware drift. Start with single-request inference; freeze batching/cache/warm-up policy before final labels. If shared system failures introduce cluster dependence, do not pretend rows are independent: resolve or redesign the statistical cluster in DEVELOPMENT and freeze it before final data.

## Resumption and failures

Write an append-only dispatch intent before sending a generation, followed by admission and terminal state. Reconcile crashes conservatively. A completed draw cannot be overwritten or repeated to get a better answer. A genuinely proven pre-admission failure can retry within J; unknown admission cannot. A never-dispatched scheduled draw can execute on resumption. Distinguish these cases in tests.

Output taxonomy must separately count native delimiter failure, outer wrapper failure, native syntax failure, cap without final, valid partial credit, completed native wrong, admitted execution/response failure, and perfect success. Orthogonal flags may coexist; do not lose timing/cap information by forcing it into one label. Pin a primary status precedence for aggregate tables.

Never quietly recover malformed answers using regex guesses, an LLM, added turns, or a different scorer. Whitespace and token-delimiter treatment are declared parser behavior, not ad hoc repair. Score failures exactly once. Missing persisted artifacts trigger integrity failure, not automatic recollection.

## Immutability and test isolation

Use stable canonical JSON serialization and SHA-256. Hash actual serialized prompts, tokenizer/template files, effective sampler settings, dependency versions, and scorer sources. Canonical records must not include their own hash; parent manifests reference child artifacts without cycles.

Final collection only accepts a sealed base manifest. Train/tune readers reject audit/test partitions. The audit loader requires frozen candidate hashes. The test evaluator requires a deployment manifest and action log before any model draws; offline policy-swap evidence cannot alter actions. A global candidate freeze precedes exposing any audit result to avoid sequential comparator contamination.

P00 user clarification (2026-09-28 UTC): final TRAIN and TUNE label artifacts use `final_train_labels` and `final_tune_labels`, respectively, and validate that their separate split is exactly `TRAIN` or `TUNE`. Both require the accepted frozen study manifest before real collection. TRAIN supports fitting; TUNE supports prescribed calibration/selection. P00 implements schema and rejection tests only; real collection stays disabled.

The user also accepted staged hash-linked records: the pre-label base manifest binds the candidate schema and selection rules; later candidate/deployment records reference their immutable parents. Candidate hashes are not fabricated before training. See `reports/decision_ledger.md`, C01, for the acceptance reference; original manuscript sources remain preserved.

A hash mismatch, unsupported sampler, out-of-range score/cost, missing family, duplicate draw, or unexpected model revision fails closed. Preserve the run for review rather than relabeling it as valid.

## Versioned CR01 scope

Prospective primary contracts must identify `TaskCognition-CR01-2026-10-05-v1`, reference the approved amendment hash, use 2,048 total tokens for each D/R package and `completion_policy: descriptive`. See `configs/cr01_development_design_template.json`. This is an incomplete development template, not a study/candidate/deployment freeze. Any future production validator must reject other prospective primary caps and unresolved required freeze fields, while accepting no completion-threshold eligibility rejection.

Historical P01/P02A/P02B runners, immutable plans, schemas and fixtures retain their original versions/caps and remain closed. They cannot be reused to authorize CR01 dispatch. The existing StudyManifest is UNFROZEN-only and final collection always rejects; no full freeze validator is claimed. Score/cost ranges, exact perfect-score equality, denominator adequacy, no replay and evidence-integrity requirements remain unchanged.
