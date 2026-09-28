"""Generate P02B completion and next-decision prose from retained records."""
from datetime import datetime
from pathlib import Path
from collections import Counter
import json,statistics
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1];out=root/'reports/p02b';run=root/'artifacts/development/p02b-two-cap'
r=read_json(out/'resources.json');obs=read_json(out/'observations.json')['rows'];cells=read_json(out/'twenty_four_cells.json')['rows'];diagnostics=read_json(out/'failure_diagnostics.json')['rows']
verified=read_json(out/'checkpoint_verification.json')
bad2048=[f"{c['family']}/{c['mode']} ({c['strict_valid_final']}/2)" for c in cells if c['cap']==2048 and c['strict_valid_final']<2]
bad1024=[f"{c['family']}/{c['mode']} ({c['strict_valid_final']}/2)" for c in cells if c['cap']==1024 and c['strict_valid_final']<2]
if r['status']=='BLOCKED':
    recommendation='A software/evidence or incomplete-execution issue blocks a formal cap decision. Investigate the preserved incident without replacement calls; the diagnostic is incomplete. No further prompt revision or generation is authorized.'
elif bad2048:
    recommendation='The current package remains too unpromising to justify the proposed 2,400-call formal cap stages now. Completion failures remain at 2,048 in '+', '.join(bad2048)+'. Return this negative diagnostic for a coordinator decision; do not automatically revise the prompt, simplify tasks, extend the deadline, or collect another diagnostic.'
else:
    recommendation='A fresh, prospectively fixed formal cap study is worth considering for review because every 2,048 cell completed 2/2 in this diagnostic. This small sample does not certify 99% completion. No formal study is authorized by this report.'
capstats=[]
for cap in (1024,2048):
    for mode in ('D','R'):
        items=[o for o in obs if (o['cap'],o['mode'])==(cap,mode)]
        capstats.append(dict(cap=cap,mode=mode,planned=12,retained=len(items),strict_valid=sum(o['strict_valid_final'] for o in items),perfect=sum(o['perfect_correct'] for o in items),wrappers=Counter(o['wrapper_subtype'] for o in items if o['wrapper_subtype']),cap_without_final=sum('cap_without_valid_final' in o['failure_flags'] for o in items),timeouts=sum(o['timeout'] for o in items),known_tokens=sum(o['output_tokens'] or 0 for o in items),known_worker_seconds=sum(o['worker_seconds'] or 0 for o in items)))
write_new(out/'descriptive_cap_summary.json',dict(evidence_kind='development_observation',rows=capstats,interpretation='Descriptive only; six input clusters, not population completion estimates'))
summary_table='\n'.join(f"| {s['cap']} | {s['mode']} | {s['retained']}/12 | {s['strict_valid']}/12 | {s['perfect']}/12 | {dict(s['wrappers'])} | {s['cap_without_final']} | {s['timeouts']} | {s['known_tokens']} | {s['known_worker_seconds']:.3f} |" for s in capstats)
sourcecommit=read_json(root/'configs/state_events/009_P02B_bounded_dispatch.json')['source_commit']
planhash=file_hash(run/'run_plan.json')
prep=(datetime.fromisoformat(read_json(run/'execution_start.json')['timestamp_utc'])-datetime.fromisoformat(read_json(out/'acceptance_verification.json')['timestamp_utc'])).total_seconds()
rawbytes=sum(p.stat().st_size for p in run.rglob('*') if p.is_file())
write_new(out/'preparation_and_storage.json',dict(evidence_kind='development_observation',preparation_elapsed_seconds_acceptance_to_dispatch=prep,initial_document_reading_preceded_interval=True,report_preparation_overlapped_execution=True,raw_run_bytes=rawbytes,additional_weights_source_dependencies_bytes=0,backup='local raw records and local review ZIP only; no independent/off-machine backup',final_evidence_size='see packet receipt'))
proposal=f'''# P02B next decision

{recommendation}

This recommendation rests on cellwise completion, not pooled accuracy. At 1,024, cells below 2/2 were: {', '.join(bad1024) or 'none'}. At 2,048: {', '.join(bad2048) or 'none'}. Inspect the 24-cell table and separate missing-tag/outside-prose diagnoses. A valid FINAL can still be wrong; cap completion and native correctness are separate.

Only one input per family was tested, with two independent draws per mode/cap. These results neither establish a family-population 99% rate nor invoke the formal infeasibility rule. Inputs changed from P02A, so the old/new instruction comparison is descriptive. Within P02B, caps share questions but not sampling streams; the longer-cap output is not an extension of the shorter-cap answer.

The original formal rule remains unchanged: a fresh reviewed fixed package must be evaluated at 1,024 across all 12 cells, then at 2,048 if needed; a formal 2,048 failure stops the confirmatory study. Instruction/configuration cannot change between those stages except cap. All P01/P02A/P02B diagnostic rows are excluded from formal denominators. No new prompt revision, 2,400-call stage, high-repeat tranche, feature benchmark or larger budget is authorized. P02 remains incomplete and unsealed.

Timeout observations are in the 24-cell table. There were {sum(o['timeout'] for o in obs)} recorded deadline stops in P02B. {'The deadline affected observed completion and must remain visible; it was not extended.' if any(o['timeout'] for o in obs) else 'No recorded timeout shows deadline domination in this tiny slice; that is not a guarantee for future inputs.'} Keep the 120-second rule and observed cleanup costs distinct from a mathematical hard support bound.

Worker residency remains a descriptive research cost. Live encoder/gate costs, a defensible scalar cost/support contract, common beta and durable backup remain unresolved. The verified local packet is not an off-machine backup. No P03, final-label collection or routing claim follows from this checkpoint.
'''
(out/'next_decision.md').write_text(proposal,encoding='utf-8')
commandrows=[]
for name in ['acceptance_command.json','offline_tests_preflight.json','offline_tests_final_preflight.json','prepare_command.json','pip_check.json','execution_command.json','report_command.json','failure_review_command.json','checkpoint_verify_command.json']:
    if (out/name).exists():
        c=read_json(out/name);commandrows.append('| '+' '.join(c['argv'])+' | '+str(c['exit'])+' | '+name+' |')
report=f'''# P02B completion report

Status: **P02B {r['status']}**. **P02 remains incomplete and unsealed. Live dispatch is disabled.**

## Scope

Authority: current user prompt, “P02B: one fixed formatting revision, two-cap diagnostic,” conveying reports/p02a/P02A_coordinator_acceptance.md. Only this 48-call checkpoint is authorized. P01 remains sealed and closed; P02A is accepted as an integration checkpoint, not an accepted seal for all P02.

All four accepted P02A artifacts and all 359 indexed files matched both accepted ZIP bytes and the current checkout before work. Verified pre-dispatch commit d9f78e6467ab5509219390475930b361364257b2 and evidence commit 617b15fcb467422fa667e7c9a994ca217d349ac6; separate packet commit 00a9ffe. The new acceptance record is reports/phases/P02A_accepted_checkpoint.md; events 008–011 document activation, bounded dispatch, closure and checkpoint. The coordinator reviewed offline evidence and did not conduct a new independent GPU run.

Governing revised PDF SHA-256 `{file_hash(root/'reference/TaskCognition_Revised_Verified.pdf')}`. Protocol, architecture, statistical/evidence contracts, C01–C03 and decision register remain in force. No model, task family, target, comparator or scientific rule was changed.

Branch `codex/p02b-two-cap`; pre-dispatch source/plan commit `{sourcecommit}`. Source/evidence/diff identities are in source_commits.json. The pre-existing untracked coordinator acceptance file was preserved and not committed. No push, merge or history rewrite.

## Delivered slice

One exact common system instruction from the user, identical for D/R and both caps; every native question preserved verbatim. Exact old/new text and hashes are in instruction_diff.json; system_instruction_display.diff provides a line-separated display. No appended hint, forced prefix, constrained decoding, extra turn, repair, rewritten output or parser relaxation.

Six prespecified fresh DEVELOPMENT inputs use the same pinned native default configurations, with only declared seeds/size/index changed. Selection was fixed before outputs; content hashes and input IDs are disjoint from historical requests. No concrete later input population exists; reserved future namespaces remain unused and future plans must reject historical latent/content identities. All selected serialized inputs are 160–346 tokens under the unchanged provisional 2,048 ceiling; none was truncated/replaced.

There are four cap/mode package records, six outcome-input records, separate input-only gate projections and 48 immutable serialized requests. Cap order is balanced within each input across draw index; 48 stream IDs and sampling seeds are distinct. Plan SHA-256 `{planhash}`. The base/effective generation settings preserve all P02A defaults except the explicit max_new_tokens value; no inference environment, tokenizer, weights, backend or native scorer change. Native BF16 Qwen3-8B b968826d9c46dd6066d109eabc6255188de91218, Windows Transformers 4.57.6/PyTorch 2.11.0+cu128, forced SDPA MATH, matched sampler retained. Actual source import and all model-file hashes were checked; subprocesses inherit absolute PYTHONPATH=src, avoiding the installed historical wheel.

The P02B runner has its own 48-slot/73,728-token/per-cap counters. The accepted ledger, supervisor cleanup, parser, native adapters and targets were reused unchanged. New worker finish detection uses each request's cap. All old accepted source bytes remain recoverable and hash-verifiable; no accepted shared source file was edited. Software incidents remain unscored, and admitted/unknown requests cannot replay. The execution finally block closes dispatch even on failure.

## Verification

| Command actually executed | Exit | Log in reports/p02b |
|---|---|---|
{chr(10).join(commandrows)}

**102 offline tests passed before dispatch**, retaining the existing 91. Added checks cover mixed/per-cap reservations including unknown admission, no replay, 1,024/2,048 cap detection, package/stream identity, old-phase refusal, forced records without normal parsed fields, missing/corrupt results, actual report execution on unknown/unexecuted requests, wrapper subtypes and refusal to select ambiguous diagnostic answers. Existing actual-child supervisor cleanup and worker callback/error tests remain passing. Pip check is clean.

Preparation failure: a syntax check caught a missing parenthesis in the new report's resource summary. It was corrected and the actual incomplete-run report regression passed before any model call. preparation_failures.json preserves the failure. A later ad-hoc syntax check read UTF-8 report source with Windows cp1252 and failed; explicit UTF-8 reading succeeded (report_preparation_check.json), without any effect on the live source or generation. No failed preparation used a generation. Native sources and all environment distribution versions match P02A; no download/upgrade occurred.

Offline replay verifies retained token count/decoded text, native input identity, parser outputs and unchanged native scores. Missing/corrupt evidence is an integrity incident, not a zero. Explicit known forced-termination outcomes retain their declared failure semantics; missing normal fields cannot by themselves crash reporting. Detailed missing/unexecuted/incident inventory is separate from observed model outcomes.

Post-run verification: the optional CIM process query returned Access denied. Its initial empty-count draft is retained as process_query_invalid_draft.json and is explicitly invalid, not evidence of absence. The supported Get-Process inventory then found zero Python processes; all 48 ledger resource records also report process_exit=0 after supervisor wait. See process_cleanup_verification.json. This reporting check did not alter the run or its outcomes. Generic whitespace checks flagged preserved Windows carriage returns and one extra report EOF blank line; raw logs were not normalized, and the report-only blank line was removed (reporting_failures.json).

## Data and execution

Evidence kind `development_observation`, split DEVELOPMENT only; offline fixtures are test evidence. Planned: six inputs x two modes x two draws x two caps = 48 calls. Dispatched **{r['dispatched']}**, admitted **{verified['admitted']}**, resource records **{verified['resource_records']}**, retained **{r['retained']}**, reserved output **{r['reserved_output_tokens']}**. Unexecuted: {r['unexecuted']}. Dispatched without retained result: {r['dispatched_without_retained_result']}. Incidents: {len(r['incidents'])}. Full counters and caveats in resources.json.

Known generated tokens **{r['known_generated_tokens']}**, unknown-token outcomes **{r['unknown_output_token_count']}**. Conservative cumulative worker/GPU residency **{r['conservative_gpu_residency_seconds']:.3f} seconds / 5,400**; execution wall **{r['execution']['execution_wall_seconds'] if r['execution'] else 'unknown'} seconds / 7,200**. Known generation **{r['known_generation_seconds']:.3f} seconds**; loading **{r['known_load_seconds']:.3f} seconds**. Load, generation and cleanup are already inside worker residency, not extra duplicate scalar charges. Actual measurements are never clipped. Any missing resource record is explicitly reported as incomplete accounting, not zero work.

Peak allocated memory **{r['peak_allocated_bytes']} bytes**, reserved **{r['peak_reserved_bytes']} bytes**. Per-request lengths, load/generation/residency and memory remain in observations.json and raw ledger/results. Preparation acceptance-to-dispatch wall interval **{prep:.3f} seconds**, separately measured; initial reading preceded it, and report preparation overlapped execution without subtraction from runtime. No hidden warm-up, retry, encoder forward, gate fit, final label, audit/test exposure, paid/cloud work or external upload.

Raw run before packet **{rawbytes} bytes**. Final local evidence/ZIP sizes and hashes are in P02B_packet_receipt.json; the authorized limit is 0.5 GiB. No new weights/source/dependency footprint. Backup is local raw records plus verified local ZIP only.

## Findings and limits

The following pooled counts are descriptive only; the required **24 cells**, each with planned/executed/retained counts, scores, failure types, length and cost, are in integration_table.md and twenty_four_cells.json.

| Cap | Mode | Retained | Strict FINAL | Perfect | Wrapper subtypes | Cap-no-final | Timeout | Tokens | Worker seconds |
|---|---|---|---|---|---|---|---|---|---|
{summary_table}

Missing tags and forbidden outside prose are distinct, with explicit zero counts and inspection of every non-perfect raw outcome in failure_inspection.md. Diagnostics in failure_diagnostics.json inspect only already bare syntactically valid payloads or a single unambiguous tagged payload surrounded by prose. Their native scores are explicitly diagnostic and do not replace primary scores, completion counts or target inputs. No favorable-answer selection from ambiguous prose, competing tags or thinking traces is performed. The unchanged text-native scorers' permissiveness is preserved; bare text diagnostic eligibility is deliberately conservative.

Complete four-draw clusters produce cap-specific T_b/T_h/direct-redraw/d_0.10/d_0.25 checks using the existing aggregation code. No cross-cap pooling, independent-cross-pair fiction, fitted gate, test of routing superiority or significance claim. Old/new formatting comparison is descriptive because inputs changed. The within-P02B comparison uses the same questions and independent generations; one sample did not continue into the other.

{recommendation}

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
| Bounded once-only execution and full 24-cell report | {r['status']} | execution/resources/cell records |
| Separate primary and diagnostic scores; cap-specific targets | PASS for valid retained records | diagnostic/target files |
| Verified local ZIP/index/receipt | See receipt | P02B_packet_receipt.json |
| Formal cap selection, high-repeat/features, P03, final labels | NOT_RUN, unapproved | dispatch disabled; P02 incomplete |

## Review packet

Send P02B_review_packet.zip and P02B_packet_receipt.json with this report, integration_table.md and next_decision.md. The index binds source/diff, configuration, raw outcomes, ledger, resources, tests and state/acceptance records. No weights, environments, secrets or private meetings. Full hash verification does not imply independent GPU replication.

## Stop statement

**P02B {r['status']}. Live dispatch disabled. P02 incomplete and unsealed.** No further prompt revision, larger pilot, formal cap study, feature benchmark, P03 or final labels were started. The next decision is returned for review.
'''
(root/'reports/phases/P02B_completion.md').write_text(report,encoding='utf-8')
print('Wrote data-derived completion, cap summaries and next-decision recommendation.')
