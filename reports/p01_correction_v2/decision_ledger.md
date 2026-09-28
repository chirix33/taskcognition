# P01 targeted correction v2

Authority: current user's **P01 targeted correction: distinguish worker errors from
model outcomes**, and [coordinator review](../P01_coordinator_review.md). P01 remains
unsealed; P02 is not authorized. C02 is unchanged. This ledger supplements, rather
than edits, the original P00/P01 ledgers and packet.

| ID | Correction / evidence | Interpretation |
|---|---|---|
| P01-C02-1 | Unexpected exceptions around admission/generation/callbacks/returned-token checks/synchronization now write an unscored incident and re-raise the original exception. | No generic Exception or RuntimeError is recognized as a model outcome. Diagnostic-writing exceptions add context and never permit scoring. |
| P01-C02-2 | Stream and cancellation callbacks latch failures; a backend swallowing their exception still cannot authorize scoring. Partial token IDs survive where available. | Damaged evidence is neither deleted nor repaired. Token IDs in an incident are diagnostic only, even if they decode to a plausible answer. |
| P01-C02-3 | Supervisor charges observed resources once, then rejects incident-marked or legacy model_error terminal outcomes even on exit zero. | Unknown/admitted requests cannot replay. No replacement generation. Existing documented intentional cancellation/timeout rules remain. |
| P01-C02-4 | Main worker, supervisor and prepare path require explicit real_dispatch_enabled=true as well as P01 IN_PROGRESS. Current state explicitly disables dispatch; status stays READY_FOR_REVIEW while separate correction status tracks work. | Old installed 0.1.1 supervisor also rejects current READY_FOR_REVIEW status. No package/dependency installation during this correction; execute current source with PYTHONPATH=src. |
| P01-C02-5 | Actual worker.main is tested with fake backend modules, using real callbacks, admission ledger, parser and terminal publication. | No extraction into a separate toy classifier. The same final 19 tests fail on the reviewed source (11 failures, 5 errors, 3 passes); corrected full suite passes 81/81. Missing diagnostic files explain the expected pre-fix errors. |
| P01-C02-6 | Original ZIP/index/report/seal and all three raw outcomes remain byte-identical. Replay scores 0/1/0, null model_error fields, intact terminal evidence and exit-zero resource records. | No observed branch impact; no original outcome invalidation or rerun. D's numeric list is correct, but its primary score remains zero for missing FINAL. No live valid-FINAL D success. |

No prompts, parser, native renderer/scorer, cap, sampler, threshold, sample size or
statistical procedure changed. No new GPU work, model loads, generations, downloads,
backend installations or dependency changes. Historical totals remain 3 admitted
generations and 567 output tokens; the remaining five slots are inactive.

Validation incidents retained honestly: initial replay in the minimal `.venv` failed
because NumPy is absent; replay succeeded in the existing `.venv-inference` without
importing torch/Transformers. A repeated replay refused to overwrite its existing
immutable output log; rerunning with a new explicit log name succeeded. Neither
failure changed scientific evidence. The original source-block probe remains a
diagnostic only; production entry-point regressions supply the repair evidence.
