# P02B completion report

Status: **P02B READY_FOR_REVIEW**. **P02 remains incomplete and unsealed. Live dispatch is disabled.**

## Scope

Authority: current user prompt, “P02B: one fixed formatting revision, two-cap diagnostic,” conveying reports/p02a/P02A_coordinator_acceptance.md. Only this 48-call checkpoint is authorized. P01 remains sealed and closed; P02A is accepted as an integration checkpoint, not an accepted seal for all P02.

All four accepted P02A artifacts and all 359 indexed files matched both accepted ZIP bytes and the current checkout before work. Verified pre-dispatch commit d9f78e6467ab5509219390475930b361364257b2 and evidence commit 617b15fcb467422fa667e7c9a994ca217d349ac6; separate packet commit 00a9ffe. The new acceptance record is reports/phases/P02A_accepted_checkpoint.md; events 008–011 document activation, bounded dispatch, closure and checkpoint. The coordinator reviewed offline evidence and did not conduct a new independent GPU run.

Governing revised PDF SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`. Protocol, architecture, statistical/evidence contracts, C01–C03 and decision register remain in force. No model, task family, target, comparator or scientific rule was changed.

Branch `codex/p02b-two-cap`; pre-dispatch source/plan commit `72d88843067b8a8f0f29d2937587a102d5a24f6b`. Source/evidence/diff identities are in source_commits.json. The pre-existing untracked coordinator acceptance file was preserved and not committed. No push, merge or history rewrite.

## Delivered slice

One exact common system instruction from the user, identical for D/R and both caps; every native question preserved verbatim. Exact old/new text and hashes are in instruction_diff.json; system_instruction_display.diff provides a line-separated display. No appended hint, forced prefix, constrained decoding, extra turn, repair, rewritten output or parser relaxation.

Six prespecified fresh DEVELOPMENT inputs use the same pinned native default configurations, with only declared seeds/size/index changed. Selection was fixed before outputs; content hashes and input IDs are disjoint from historical requests. No concrete later input population exists; reserved future namespaces remain unused and future plans must reject historical latent/content identities. All selected serialized inputs are 160–346 tokens under the unchanged provisional 2,048 ceiling; none was truncated/replaced.

There are four cap/mode package records, six outcome-input records, separate input-only gate projections and 48 immutable serialized requests. Cap order is balanced within each input across draw index; 48 stream IDs and sampling seeds are distinct. Plan SHA-256 `9afcea3b3fe41aa39cfbf44e30f81514128f077ecdb42a18f13fb25f8f2eff36`. The base/effective generation settings preserve all P02A defaults except the explicit max_new_tokens value; no inference environment, tokenizer, weights, backend or native scorer change. Native BF16 Qwen3-8B b968826d9c46dd6066d109eabc6255188de91218, Windows Transformers 4.57.6/PyTorch 2.11.0+cu128, forced SDPA MATH, matched sampler retained. Actual source import and all model-file hashes were checked; subprocesses inherit absolute PYTHONPATH=src, avoiding the installed historical wheel.

The P02B runner has its own 48-slot/73,728-token/per-cap counters. The accepted ledger, supervisor cleanup, parser, native adapters and targets were reused unchanged. New worker finish detection uses each request's cap. All old accepted source bytes remain recoverable and hash-verifiable; no accepted shared source file was edited. Software incidents remain unscored, and admitted/unknown requests cannot replay. The execution finally block closes dispatch even on failure.

## Verification

| Command actually executed | Exit | Log in reports/p02b |
|---|---|---|
| .venv/Scripts/python.exe scripts/p02b_accept.py | 0 | acceptance_command.json |
| .venv-inference/Scripts/python.exe -m unittest discover -s tests -v | 0 | offline_tests_preflight.json |
| .venv-inference/Scripts/python.exe -m unittest discover -s tests -v | 0 | offline_tests_final_preflight.json |
| .venv-inference/Scripts/python.exe scripts/p02b_prepare.py | 0 | prepare_command.json |
| .venv-inference/Scripts/python.exe -m pip check | 0 | pip_check.json |
| .venv-inference/Scripts/python.exe -m taskcognition.p02b_runner | 0 | execution_command.json |
| .venv-inference/Scripts/python.exe scripts/p02b_report.py | 0 | report_command.json |
| .venv-inference/Scripts/python.exe scripts/p02b_failure_review.py | 0 | failure_review_command.json |
| .venv-inference/Scripts/python.exe scripts/p02b_verify_checkpoint.py | 0 | checkpoint_verify_command.json |

**102 offline tests passed before dispatch**, retaining the existing 91. Added checks cover mixed/per-cap reservations including unknown admission, no replay, 1,024/2,048 cap detection, package/stream identity, old-phase refusal, forced records without normal parsed fields, missing/corrupt results, actual report execution on unknown/unexecuted requests, wrapper subtypes and refusal to select ambiguous diagnostic answers. Existing actual-child supervisor cleanup and worker callback/error tests remain passing. Pip check is clean.

Preparation failure: a syntax check caught a missing parenthesis in the new report's resource summary. It was corrected and the actual incomplete-run report regression passed before any model call. preparation_failures.json preserves the failure. A later ad-hoc syntax check read UTF-8 report source with Windows cp1252 and failed; explicit UTF-8 reading succeeded (report_preparation_check.json), without any effect on the live source or generation. No failed preparation used a generation. Native sources and all environment distribution versions match P02A; no download/upgrade occurred.

Offline replay verifies retained token count/decoded text, native input identity, parser outputs and unchanged native scores. Missing/corrupt evidence is an integrity incident, not a zero. Explicit known forced-termination outcomes retain their declared failure semantics; missing normal fields cannot by themselves crash reporting. Detailed missing/unexecuted/incident inventory is separate from observed model outcomes.

Post-run verification: the optional CIM process query returned Access denied. Its initial empty-count draft is retained as process_query_invalid_draft.json and is explicitly invalid, not evidence of absence. The supported Get-Process inventory then found zero Python processes; all 48 ledger resource records also report process_exit=0 after supervisor wait. See process_cleanup_verification.json. This reporting check did not alter the run or its outcomes. Generic whitespace checks flagged preserved Windows carriage returns and one extra report EOF blank line; raw logs were not normalized, and the report-only blank line was removed (reporting_failures.json).

## Data and execution

Evidence kind `development_observation`, split DEVELOPMENT only; offline fixtures are test evidence. Planned: six inputs x two modes x two draws x two caps = 48 calls. Dispatched **48**, admitted **48**, resource records **48**, retained **48**, reserved output **73728**. Unexecuted: []. Dispatched without retained result: []. Incidents: 0. Full counters and caveats in resources.json.

Known generated tokens **28690**, unknown-token outcomes **0**. Conservative cumulative worker/GPU residency **1682.543 seconds / 5,400**; execution wall **1693.7150865000003 seconds / 7,200**. Known generation **1111.001 seconds**; loading **369.522 seconds**. Load, generation and cleanup are already inside worker residency, not extra duplicate scalar charges. Actual measurements are never clipped. Any missing resource record is explicitly reported as incomplete accounting, not zero work.

Peak allocated memory **16888340480 bytes**, reserved **17710448640 bytes**. Per-request lengths, load/generation/residency and memory remain in observations.json and raw ledger/results. Preparation acceptance-to-dispatch wall interval **604.855 seconds**, separately measured; initial reading preceded it, and report preparation overlapped execution without subtraction from runtime. No hidden warm-up, retry, encoder forward, gate fit, final label, audit/test exposure, paid/cloud work or external upload.

Raw run before packet **944871 bytes**. Final local evidence/ZIP sizes and hashes are in P02B_packet_receipt.json; the authorized limit is 0.5 GiB. No new weights/source/dependency footprint. Backup is local raw records plus verified local ZIP only.

## Findings and limits

The following pooled counts are descriptive only; the required **24 cells**, each with planned/executed/retained counts, scores, failure types, length and cost, are in integration_table.md and twenty_four_cells.json.

| Cap | Mode | Retained | Strict FINAL | Perfect | Wrapper subtypes | Cap-no-final | Timeout | Tokens | Worker seconds |
|---|---|---|---|---|---|---|---|---|---|
| 1024 | D | 12/12 | 7/12 | 4/12 | {'missing_both_tags': 4, 'missing_close_tag': 1} | 1 | 0 | 1304 | 194.616 |
| 1024 | R | 12/12 | 5/12 | 5/12 | {} | 7 | 0 | 10285 | 533.488 |
| 2048 | D | 12/12 | 7/12 | 4/12 | {'missing_both_tags': 4, 'missing_close_tag': 1} | 1 | 0 | 2328 | 243.005 |
| 2048 | R | 12/12 | 9/12 | 8/12 | {} | 3 | 0 | 14773 | 711.435 |

Missing tags and forbidden outside prose are distinct, with explicit zero counts and inspection of every non-perfect raw outcome in failure_inspection.md. Diagnostics in failure_diagnostics.json inspect only already bare syntactically valid payloads or a single unambiguous tagged payload surrounded by prose. Their native scores are explicitly diagnostic and do not replace primary scores, completion counts or target inputs. No favorable-answer selection from ambiguous prose, competing tags or thinking traces is performed. The unchanged text-native scorers' permissiveness is preserved; bare text diagnostic eligibility is deliberately conservative.

Complete four-draw clusters produce cap-specific T_b/T_h/direct-redraw/d_0.10/d_0.25 checks using the existing aggregation code. No cross-cap pooling, independent-cross-pair fiction, fitted gate, test of routing superiority or significance claim. Old/new formatting comparison is descriptive because inputs changed. The within-P02B comparison uses the same questions and independent generations; one sample did not continue into the other.

The current package remains too unpromising to justify the proposed 2,400-call formal cap stages now. Completion failures remain at 2,048 in number_sorting/D (0/2), graph_color/D (0/2), graph_color/R (1/2), shortest_path/D (1/2), shortest_path/R (0/2). Return this negative diagnostic for a coordinator decision; do not automatically revise the prompt, simplify tasks, extend the deadline, or collect another diagnostic.

This is **not formal cap selection**. Even 2/2 or all-success diagnostic cells do not establish 99% population completion. Tiny failures do not declare formal infeasibility. A fresh reviewed formal plan must exclude P01/P02A/P02B and keep the package fixed between formal stages except cap. No new prompt revision or larger proposed workload is authorized.

## Changes and decisions

| ID | Resolution / outstanding decision | Evidence / impact |
|---|---|---|
| P02B-01 | P02A checkpoint accepted; P01 seal unchanged; P02 unsealed | Four hashes, 359 files and acceptance record |
| P02B-02 | Exact user instruction; two allowed caps; all other generation defaults unchanged | instruction_diff, four package records, full plan |
| P02B-03 / D06 | Fresh declared default-config inputs, same 2,048 input ceiling | six native records; provisional, no final population freeze |
| P02B-04 / D09/D10 | 48 slots, J=0, 120-second deadline both caps, 300-second reservation, fixed envelope | no replacement; descriptive residency only |
| D05/D07/D08/D16/D17 | Encoder, formal cap decision, scalar hard bounds, beta and durable backup remain unresolved | no automatic larger slice or P03 work |

No old primary score or accepted evidence was changed. Current phase state alone advances from the accepted P02A index; its old bytes are preserved in a state snapshot. This is a user-authorized prospective package revision, not a prompt search. Existing P02A source and records remain intact. No full P02 accepted seal was created.

## Acceptance checklist

| Requirement | Status | Evidence |
|---|---|---|
| P02A acceptance verified and recorded; old phases closed | PASS | acceptance verification, state events |
| Exact fixed instruction, native questions/defaults retained | PASS | diff and six native records |
| 48 predeclared mixed-cap requests and distinct streams | PASS | immutable plan and pre-dispatch commit |
| Regression suite and incomplete-safe report review | PASS | 102 tests; preparation failure retained |
| Bounded once-only execution and full 24-cell report | READY_FOR_REVIEW | execution/resources/cell records |
| Separate primary and diagnostic scores; cap-specific targets | PASS for valid retained records | diagnostic/target files |
| Verified local ZIP/index/receipt | See receipt | P02B_packet_receipt.json |
| Formal cap selection, high-repeat/features, P03, final labels | NOT_RUN, unapproved | dispatch disabled; P02 incomplete |

## Review packet

Send P02B_review_packet.zip and P02B_packet_receipt.json with this report, integration_table.md and next_decision.md. The index binds source/diff, configuration, raw outcomes, ledger, resources, tests and state/acceptance records. No weights, environments, secrets or private meetings. Full hash verification does not imply independent GPU replication.

## Stop statement

**P02B READY_FOR_REVIEW. Live dispatch disabled. P02 incomplete and unsealed.** No further prompt revision, larger pilot, formal cap study, feature benchmark, P03 or final labels were started. The next decision is returned for review.
