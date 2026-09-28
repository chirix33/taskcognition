# P01 coordinator review: one correction before sealing

Date: 2026-09-28. Decision: NEEDS_TARGETED_CORRECTION. P01 remains unsealed; P02 is not authorized.

## Evidence actually examined

The uploaded completion report, proposed seal, and full review ZIP were inspected. The packet was extracted into an isolated review directory; the user's implementation repository was not modified.

- ZIP SHA-256: `11c3e935f38e7bbcb8e69e163c12acbff6bd5ac784863a2af793df619f127be6`.
- Completion SHA-256: `07edfed83482ed63e6e219a3e6439e6c30a6f58c12ebd1ba69dc2b01bbef71c3`.
- Evidence index SHA-256: `b525dfba19063550c8ad96adec528574c76133de792c6e31720fdbecdea312ed`.
- All 215 indexed files and 17 executed-source snapshot files matched their recorded hashes.
- The uploaded report and seal matched their packet copies byte for byte.
- Independently reran `PYTHONPATH=src python3 -m unittest discover -s tests -v` against the supplied final code: all 62 tests passed in the review environment.
- Independently reconciled the real ledger: 15 events, three requests, 567 generated tokens.
- Replayed the parser/native scorer on all three saved outputs: retained scores 0, 1, 0 match the report.
- Read runtime/kernel logs, raw serialized prompts and outputs, restart evidence, native scorer, parser, ledger, worker, supervisor, tests, and the executed-versus-corrected supervisor diff.

The GPU executions were reviewed from supplied records; the coordinator did not load Qwen or independently reproduce the workstation's GPU runs. Local offline tests and saved-output replay do not prove CUDA behavior beyond those records.

## What is satisfactory

The official checkpoint/native BF16 execution is documented with actual GPU checks. D and R use matching primary sampling settings and distinct streams. The strict parser correctly rejects the bare D answer and accepts R's wrapped answer. The controlled interruption has durable admission, recorded tokens/resources, and restart evidence refusing a duplicate request. Old and corrected code are distinguished, and historical evidence was retained.

The direct response was `['-6.0', '4.0', '6.0']`. It is the correct ordering, and a diagnostic call of the unchanged native scorer on that bare payload returns 1. The primary pipeline correctly assigns zero because the FINAL wrapper is missing. This diagnostic observation does not replace its stored score or establish a valid-final D success. Both modes produced the same correct numeric list in the initial pair; the measured score difference reflects formatting compliance here, not evidence of improved numerical reasoning.

The absent live valid-final D example is a disclosed limitation that can be addressed in the planned development interface work. It is not the blocker identified below. Do not consume extra generations just to make the P01 report look successful.

## Blocking finding: worker exception handling still imputes errors

In `src/taskcognition/p01_worker.py`, the try block around `model.generate(...)` re-raises `IntegrityError`, but catches every other `Exception` and assigns `model_error`. Processing then continues through parsing and `terminal(...)` as a scored result, normally with worker exit code zero.

This includes programming/configuration errors such as TypeError and ValueError and evidence-I/O errors raised by streamer/stopping callbacks. With no valid output, the path yields a native score of zero. With partial valid-looking output, it can even retain a score despite an unexplained software failure. Neither is a valid substitute for stopping on a software/evidence integrity incident.

The earlier supervisor repair only rejects unexplained nonzero/missing-terminal worker exits. It cannot protect against a worker that has already swallowed the error and written an apparently valid terminal result.

Reproduction: execute the existing generation try block unchanged with a fake generation callable that raises an injected exception. The source-block probe observed:

| Injected exception | Actual handling |
|---|---|
| TypeError | Swallowed as model_error; empty-output parser produces score 0 |
| ValueError | Swallowed as model_error; empty-output parser produces score 0 |
| OSError | Swallowed as model_error; empty-output parser produces score 0 |
| IntegrityError | Correctly propagated |

This is an isolated handler probe, not a real GPU failure injection or full worker execution. The attached `P01_worker_exception_probe.py` reproduces it on the reviewed source. The correction must add tests at the actual worker boundary, not only at the supervisor helper.

## Required correction

Unexpected software, configuration, callback, and evidence-I/O errors must stop the request/run for investigation without publishing a normal scored draw. Preserve consumed resources, the request's admitted/unknown state and no-replay protection. A narrow, documented, identifiable operational failure may use the declared failure-scoring rule; a broad Exception/RuntimeError catch or message-based assumption is insufficient. It is acceptable to stop on unclassified failures conservatively during P01.

The three historical results have null `model_error`, intact evidence, and normal worker exits. No evidence was found that this defect affected those observations. Preserve them byte for byte; no Qwen rerun or score alteration is required by this correction.

## Next authorized scope

Convey `P01_targeted_correction_prompt.md` to Codex. Perform an offline P01 repair and focused regression verification only. Return an updated report, proposed seal, and review ZIP containing new code/tests/logs plus the preserved original evidence. No new generation, model load, prompt revision, dependency change, P02 execution, or scientific parameter choice is authorized by this repair prompt.

After this correction is reviewed, the next decision can be sealing P01 and defining a bounded P02 integration slice. No six-family cap-feasibility or routing-effectiveness result has been established yet.
