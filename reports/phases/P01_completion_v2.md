# P01 corrected completion report — worker exception boundary

Status: **READY_FOR_REVIEW**. P01 is **not sealed**. P02 is not authorized.

The worker now stops on unexplained software/configuration/callback errors, preserves
unscored diagnostics and re-raises. It cannot convert those errors into a normal scored
draw. **81 tests pass**, including the existing 62 and 19 focused production-boundary
regressions. No new model loads, real generations, GPU work, downloads, installations
or dependency changes occurred. Historical totals remain **3 admitted / 567 tokens**.

The original D answer was numerically correct but lacked FINAL tags: its primary score
remains zero. R remains score one. The deliberate interruption remains a distinct
diagnostic failure. **No live valid-FINAL D success has been demonstrated.**

## Scope

- Active authority: user's **P01 targeted correction: distinguish worker errors from
  model outcomes**, plus [coordinator review](../P01_coordinator_review.md). C02's
  failure/integrity distinction remains unchanged. The five unused generation slots
  were not activated. No prompts, parser, scorer, renderer, cap or scientific values changed.
- P00 acceptance remains as recorded in [P00 accepted seal](P00_accepted_seal.md).
  P01 review requested this correction; it did not accept or seal P01.
- The coordinator inspected the full prior packet, verified 215 indexed files and 17
  executed snapshots, independently reran 62 tests and replayed saved outputs. The
  coordinator did **not** load Qwen or independently reproduce GPU execution.
- Governing PDF SHA-256 remains
  `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`.
  No study/candidate/deployment freeze exists.
- Branch: `codex/p01-local-qwen`. New code/evidence commit:
  `6e8cec19d3e7f374aebddaa4f9b410767b02676a`.
  Original execution commit: `683e9a3f7c5c539a3bb5d8d959b98d4c9319721f`;
  reviewed supervisor correction: `7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322`;
  original report packet: `ed3ad539132ea291d54059c0e6dc226d5f1a4636`.
- Pre-existing staged user files `docs/prompts/P01_reviwed_local_qwen.md` and
  `reports/P01_coordinator_review.md` were preserved in place and left staged. Explicit
  path-only commits excluded both. The review's bytes are included in the new packet.
  No push, merge, dependency installation or replacement of historical evidence.
- Original [completion](P01_completion.md), [proposed seal](P01_proposed_seal.md),
  index, ZIP, executed source, requests, results and events are retained unchanged.
  This version supplements and corrects the original completion assessment.

## Delivered slice

The repair uses the existing worker entry point, without a new serving abstraction:

1. Admission, generation, streamer/cancellation callbacks, returned-token checks and
   synchronization errors stop the worker. Diagnostic capture writes a separate
   `incidents/<request_id>.json` with exception provenance, traceback and available
   partial token IDs, explicitly `scored: false`. It then re-raises the same exception.
2. Stream/cancellation callbacks latch their error. Even if the backend swallows that
   callback error and returns plausible tokens, the worker raises before parsing.
   A damaged or existing evidence/incident file is never repaired or overwritten.
   If incident persistence itself fails, the original exception still propagates
   with an added diagnostic note in the traceback/stderr; no score is published.
3. The supervisor records measured work once, then rejects worker incidents and
   legacy unclassified `model_error` outcomes even with exit zero. Admitted/unknown
   requests remain non-replayable. Normal results are not created on this incident path.
4. No generic RuntimeError or other exception allowlist was introduced. Existing
   known timeout and deliberate-cancellation flags retain their documented valid-output
   or zero-score rules. Unknown cancellation reasons now stop as integrity incidents.
5. Prepare, supervisor dispatch and worker entry require explicit real-dispatch
   authorization. Current state sets it false. New events 003/004 track offline work
   and review readiness, with no acceptance or next-phase authorization. The public
   phase status stayed READY_FOR_REVIEW, so the old installed supervisor also refuses it.

Exact production diff: [source_diff.patch](../p01_correction_v2/source_diff.patch).
Regression implementation: [test_p01_worker_correction.py](../../tests/test_p01_worker_correction.py).
These tests call **production `worker.main()`** with fake backend modules and real
worker callbacks, admission/terminal ledger, parser and supervisor accounting. No
standalone toy classifier was substituted for the faulty path.

Corrected source hashes (SHA-256):

| Source | Hash |
|---|---|
| p01_worker.py | `7acc9c3ef172ab06d2aab0ea19a4a57ccffb909b1c9d6a6a4786475d47e8e599` |
| p01_smoke.py | `dc0c727b53196d204d9e080632f73f43380d90e72d9c5b0dd8e7a8bba4107a0a` |
| p01_ledger.py | `ba4b6de166d6bdb7667bb5cbe375618ed91e71173385146af28b199dd1ef2ee3` |

The package version/dependencies were not changed or reinstalled. For corrected code,
use **`$env:PYTHONPATH='src'`** in PowerShell before the commands below. Source commit
and hashes distinguish this repair from the installed historical 0.1.1 wheel.

## Verification

All commands ran locally without real backend execution. `PY` is
`.venv/Scripts/python.exe`; `IPY` is `.venv-inference/Scripts/python.exe`.
Command logs preserve argv, exit, stdout/stderr and duration. The logger command was
`PY scripts/p01_command.py LOG COMMAND` where applicable.

| Command actually executed | Exit/status | Evidence | Interpretation |
|---|---|---|---|
| Prior ZIP SHA and all contained index/snapshot hashes checked with Python/zipfile | PASS | [preservation before](../p01_correction_v2/preservation_before.json) | 215+17 original indexed entries verified; 84 protected current files snapshotted. |
| `PY artifacts/development/P01_worker_exception_probe.py --repo .` | 1, expected diagnostic finding | [probe before](../p01_correction_v2/source_probe_before.json) | Reviewed block swallowed TypeError, ValueError, OSError; IntegrityError propagated. Probe only, not main regression evidence. |
| `PY -m unittest discover -s tests -p test_p01_worker_correction.py -v` before repair | 1, expected regression failure | [first before log](../p01_correction_v2/worker_tests_before.json) | Initial 15 tests: 8 failures, 4 missing-diagnostic errors, 3 success/cancel/timeout passes. |
| Same command after initial repair | 0 | [first after log](../p01_correction_v2/worker_tests_after.json) | Initial 15 pass. Four further edge-case tests added afterward. |
| `PY scripts/p01_correction_verify.py reviewed-tests` | Harness 0; inner suite 1, expected | [identical final tests on reviewed code](../p01_correction_v2/reviewed_source_final_tests.json) | Final 19 tests run against original reviewed modules extracted to an isolated import path: 11 failures, 5 errors, 3 passes. Test-file SHA recorded. |
| `PY -m unittest discover -s tests -v` | 0 | [all tests after](../p01_correction_v2/all_tests_after.json) | 81/81 pass in 3.114 seconds test runtime; original 62 plus 19 additions. |
| `PY scripts/p01_correction_verify.py replay` | 1 | [initial replay failure](../p01_correction_v2/replay_command.json) | Minimal environment lacked NumPy; no installation attempted. |
| `IPY scripts/p01_correction_verify.py replay` | 0 | [existing runtime replay](../p01_correction_v2/replay_command_existing_runtime.json) | Existing native-scorer dependencies used; torch/Transformers remained unimported. |
| Updated replay repeated with same output name | 1 | [immutable log refusal](../p01_correction_v2/replay_final_command.json) | Refused to overwrite prior log; all earlier evidence preserved. |
| `IPY scripts/p01_correction_verify.py replay --output preservation_and_replay_final.json` | 0 | [final replay](../p01_correction_v2/preservation_and_replay_final.json), [command](../p01_correction_v2/replay_final_command_v2.json) | 84 protected files unchanged; 211 of 215 previous indexed current files unchanged; only three corrected source files and current state differ. |
| `PY scripts/p01_correction_packet.py index` / `zip` | See v2 receipt | [v2 index](P01_evidence_manifest_v2.json), [v2 receipt](P01_packet_receipt_v2.json) | Versioned manifest and full ZIP read-back verification; prior packet retained inside. |

Focused tests cover generation TypeError/ValueError/arbitrary RuntimeError, existing
IntegrityError, admission-write failure, first-token ledger I/O failure, malformed
cancellation evidence, stream conversion, returned-token mismatch, errors after valid-looking
partial output, a backend swallowing a callback exception, and diagnostic-write failure.
They verify no parsing/normal terminal result on incidents, unmodified damaged files,
partial diagnostics where available, cost once, replay refusal and legacy exit-zero
`model_error` rejection. Mock success, deliberate cancellation and known timeout pass.

No new GPU or model tests were run, as required. These are offline software boundary
tests; they do not independently re-establish hardware cancellation behavior. No new
statistical/audit tests or statistical procedures were added.

## Data and execution

- Fixture tests use disposable temporary directories and mocked tensor/model/tokenizer
  objects; fake backend calls are not empirical generations. No torch weight load or
  GPU operation occurs. Test observations/logs are distinct from saved DEVELOPMENT evidence.
- Saved DEVELOPMENT records were read only. No TRAIN/TUNE/AUDIT/TEST data or gate
  training was accessed. No scientific K, sample size, threshold, cap or timeout changed.
- **New real loads/generations/GPU work/downloads/installations: zero.** Historical
  totals remain 3 admitted, 0 unknown, 567 tokens and 15 ledger events. Five slots stay inactive.
  Historical resource measurements remain in the unchanged original report; no new
  device measurement or cost estimate is claimed.
- Original request/result/event fingerprints and the full old packet remain byte-identical.
  The unchanged parser/native scorer replays retained scores **D=0, R=1, interruption=0**.
  All three old results have null `model_error`; their terminal evidence and exit-zero
  resource records are intact. No affected branch execution was found, so none of those
  observations are invalidated or regenerated by this repair.
- D's bare list obtains native score 1 only in a diagnostic direct scorer call; its
  primary pipeline score remains zero because the wrapper is absent. The initial
  pair's score difference reflects formatting compliance, not demonstrated better
  numerical reasoning. R's score one and deliberate interruption retain their meanings.
- Source fingerprints and replay details are machine-readable in
  `preservation_and_replay_final.json`. New local reports are small; the new ZIP receipt
  records exact size. No new remote backup or publication occurred.

## Findings and limits

The reviewed worker defect is reproduced and repaired at its real execution boundary.
The previous supervisor-only fix did not close this path; this report explicitly
supersedes that sufficiency assessment, while retaining all original evidence.

No live valid-FINAL D example exists. No six-family completion rate, cap feasibility,
routing improvement, statistical significance, final hard resource bound or final
package freeze follows from this correction. Exception diagnostics preserve available
partial data but make no claim that device work synchronized on an error path.
GPU behavior was not rerun or changed. No P02 proposal or sample-size choice was added.

## Changes and decisions

| ID | Resolved correction | Reason / downstream impact | Authority |
|---|---|---|---|
| P01-C02-1/2 | Stop and diagnose unclassified errors, including latched callback failures | Prevents software/evidence errors from becoming scored answers; partial output does not override integrity | Coordinator finding, C02, current user prompt |
| P01-C02-3 | Supervisor rejects incidents/legacy model_error even on exit zero after charging work | Stops the run and preserves no-replay protection | Targeted correction requirement |
| P01-C02-4 | Explicit dispatch disable; offline current-source execution | No remaining live quota activated; no dependency change | Zero-compute scope |
| P01-C02-5/6 | Actual-main regression plus historical replay | 81 pass; same 19 regressions fail reviewed source; old results unaffected | Required regression and preservation evidence |

Full [correction ledger](../p01_correction_v2/decision_ledger.md) records these changes.
No scientific rule changed. Old reports/seal/ZIP stay historical; P01 acceptance remains
pending. The coordinator review is not interpreted as acceptance of this new code.

## Acceptance checklist

| Targeted requirement | Status and evidence |
|---|---|
| Record correction; preserve original packet/outcomes; new state events; disable dispatch | PASS — events 003/004, original snapshots, 84 protected file hashes and prior ZIP verified. |
| Unexpected generation/configuration errors stop without scored draw | PASS — actual-main TypeError/ValueError/RuntimeError tests and unscored incident records. |
| Callback/evidence errors and partial tokens cannot authorize score | PASS — ledger, cancellation, stream conversion, swallowed-callback and partial-output regressions. |
| Preserve supported cancellation/timeout and IntegrityError semantics | PASS — mocked success/cancel/timeout paths and original exception propagation. No exception allowlist introduced. |
| Account work once, stop, no replay, no false successful model_error terminal | PASS — integrated supervisor tests, including exit-zero rejection. |
| Original 62 plus focused tests and saved-output replay | PASS — 81 tests; 19 identical final tests fail reviewed code; historical scores/fingerprints unchanged. |
| No new live activity or scientific reinterpretation | PASS — zero new activity; original 3/567 totals; D limitation explicit. |
| Versioned completion, proposed seal, source diff/commit, index and ZIP | PASS subject to validated v2 packet receipt — all paths below. |

## Review packet

- [P01_review_packet_v2.zip](../p01_correction_v2/P01_review_packet_v2.zip) and
  [external receipt](P01_packet_receipt_v2.json).
- This corrected completion and [proposed seal v2](P01_proposed_seal_v2.md).
- [Exact source diff](../p01_correction_v2/source_diff.patch), production sources,
  regression tests and pre/post logs, correction ledger and replay verification.
- [Evidence index v2](P01_evidence_manifest_v2.json), SHA-256
  `1237761e49fcee9a9e027324995f6452b27b83417b205e12c44d451940b09a3f`.
  Current corrected files are indexed normally; the unchanged original ZIP is also
  included, preserving its 215 indexed files and 17 executed snapshots at their old hashes.
- The report-packet commit is the separate local commit containing the v2 receipt;
  its identity is reported after committing, avoiding a self-referential hash.

Weights, environments, caches, secrets, private meetings and unrelated manuscript
history remain excluded. Packet is for coordinator review, not public release.

## Stop statement

P01 correction ends **READY_FOR_REVIEW**, with real dispatch disabled. P01 is not sealed.
P02 is not authorized or started. Stop for coordinator review; no additional model
calls or automatic continuation is authorized by this packet.
