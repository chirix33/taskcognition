"""Close offline preflight; no live authorization is created."""
from pathlib import Path
from datetime import datetime,timezone
import json
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical
from taskcognition.p02d_plan import PLAN_DIR,RUN

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d';now=datetime.now(timezone.utc).isoformat()
verification=read_json(out/'verification.json');assert verification['status']=='PASS'
for n in ['regression_suite.json','focused_tests_final.json','authorization_followup_tests.json','feature_wall_test.json','verification_command.json']:
    assert read_json(out/n)['exit']==0,n
assert not (root/RUN).exists() and not (root/'configs/p02d_execution_authorization.json').exists()
statepath=root/'configs/phase_state.json';state=read_json(statepath)
assert state['active_phase']=='P02D' and state['real_dispatch_enabled'] is False
snapshot=root/'configs/state_snapshots/P02D_before_preflight_checkpoint.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
event='configs/state_events/016_P02D_preflight_review_checkpoint.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='P02D_PREFLIGHT_READY_FOR_REVIEW',
    previous_state_sha256=file_hash(snapshot),plan_sha256=verification['plan_sha256'],real_dispatch_enabled=False,
    authorized_answer_slots=0,authorized_feature_forwards=0,p02_sealed=False,p03_started=False,new_model_work=0))
state.update(status='READY_FOR_REVIEW',checkpoint='PREFLIGHT',real_dispatch_enabled=False,latest_event=event,
    p02d_plan_sha256=verification['plan_sha256'],p02_sealed=False,p03_started=False)
statepath.write_bytes(canonical(state)+b'\n')
with (root/'reports/decision_ledger.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## P02D preflight checkpoint ({now})\nFixed 24-input selection eligible; 192 unique answer streams and 50 feature slots prepared, zero executed. Plan {verification["plan_sha256"]}. One input-only post-norm masked-mean recipe and exact cheap observables implemented for this prospective diagnostic only. Physical cumulative ledger implemented; no reference tariff/beta/hard support/final feature or sample freeze adopted. Remaining decisions unchanged. Dispatch false; P02 incomplete/unsealed; P03 unstarted. See reports/phases/P02D_preflight_completion.md.\n')
commands=[]
for p in sorted(out.glob('*command.json')):
    v=read_json(p);commands.append(dict(log=p.name,argv=v['argv'],exit=v['exit'],seconds=v['seconds']))
for n in ['focused_tests_v1.json','focused_tests_v2.json','regression_suite.json','focused_tests_final.json','authorization_followup_tests.json','feature_wall_test.json']:
    v=read_json(out/n);commands.append(dict(log=n,argv=v['argv'],exit=v['exit'],seconds=v['seconds']))
write_new(out/'commands_summary.json',dict(evidence_kind='development_observation',commands=commands,
    scope='Offline preparation/test command durations only; no model execution time',
    code_preparation_interval_utc={'acceptance':read_json(out/'acceptance_verification.json')['timestamp_utc'],'checkpoint':now},
    new_model_loads=0,new_answer_generations=0,new_feature_forwards=0,new_gpu_measurements=0,new_simulations=0,
    additional_failures_reference='preparation_failures.json',gpu_smoke='NOT_RUN: explicitly unauthorized',
    temp_policy='TEMP and TMP set to resolved project-local tmp/p02d-tests for tests after initial sandbox-temp failure'))
text=f'''# P02D preflight completion

**P02D PREFLIGHT READY_FOR_REVIEW.** Recorded {now}. Real dispatch is false. P02 remains incomplete/unsealed; P03 is unstarted. The 192 answer slots and 50 feature forwards are still unapproved for execution.

## Scope and authority

The archived `reports/p02d/authorization_prompt.md` and `P02C_coordinator_review.md` authorize only offline preparation. P02C acceptance was recorded once in event 015 and `P02C_accepted_checkpoint.md`, after all four accepted hashes and all 115 indexed files matched both the accepted ZIP and current files. P01 remains sealed; P02A/B/C are accepted development checkpoints. No CR01 reapproval was requested.

Authority remains the original reference PDF SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`, accepted C01–C03, and adopted CR01 SHA-256 `ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8`. CR01 approval date is 2026-10-05; its original adoption timestamp is preserved. Both caps are 2,048 total generated tokens; completion is descriptive. All strict parser/scorer/failure/target/audit/test requirements remain unchanged.

Branch: `codex/p02d-offline-preflight`, baseline `55e8fbde2f43b43cfbf0b8cfaf840d3ed0998b22`. Exact local evidence/packet commits and source diff are in `reports/p02d/source_commits.json` and `source_diff.patch`. Pre-existing untracked coordinator review, build archive and P02D prompt remain untouched and are not included in task commits at their user-owned paths; exact task-owned archive copies are included. No push, merge, fetch, download, upgrade or external transfer occurred.

## Delivered slice

The immutable candidate plan is `{PLAN_DIR}/run_plan.json`, SHA-256 **`{verification['plan_sha256']}`**. It is a DEVELOPMENT plan with separate authorization pending, not a study/candidate/deployment manifest. Its 2,529 bound files cover source, runtime Python source/metadata fingerprints, native source, configs, all selected inputs, schedules and package information. A later authorization record can reference this hash without changing the plan. Runtime Python is the existing `.venv-inference`, with explicit `PYTHONPATH=src` and checked import paths; the old installed wheel cannot silently supply these modules.

- Materialized 24 native questions/configs with exact fixed seeds, size four, indices 0–3 and original question text. Raw token lengths are 22–214, D serialized lengths 161–353, R lengths 157–349; all pass the 2,048 ceiling separately. Exact tokens/prompts/hashes are stored. No truncation, replacement or outcome screening occurred. Historical nominal/native/latent/content exclusions and future split exclusions are explicit; no final populations were invented.
- Published 192 answer slots, four D/four R per input, 192 unique streams and sampling seeds, 393,216 output tokens reserved, J=0. The exact loop order and alternating first mode are fixed. P02B instruction and all non-cap effective generation defaults are preserved.
- Implemented one same-checkpoint feature path: `model.model`, eval/inference, no KV cache, post-final-RMSNorm width 4,096, masked float32 mean and float32 vector. Installed Qwen source semantics and cached config were inspected without weight loading. Exact nine cheap observables and leakage allowlists are fixed prospectively. 50 feature slots comprise two charged warm-ups and 48 measurements, totaling 6,597 actual planned input positions, bounded by 102,400. No feature or normalization was fitted or measured.
- Implemented hash-bound pending-authorization guards, a unified durable ledger, finite child supervision, measured overshoot, no replay/cost duplication, partial-run inspection and development aggregation through the existing target implementation. Old source/guards are untouched. New `p02d_*` modules do not reopen historical phases or final collection.
- Prepared 12 cell reports with denominator 16 and 24 cluster records. `unexecuted_plan_report.json` is a pre-dispatch denominator record: every executed/retained count is zero and all empirical targets are absent. Fake test rows never populate an empirical table. Complete future K=4 clusters alone receive T_b/T_h, redraw and 0.10/0.25 diagnostics; partial/corrupt evidence remains explicitly incomplete.

See `docs/P02D_RUNNER_CONTRACT.md`, `resource_ledger_schema.json`, source code and `execution_request.md` for clocks, source boundaries, reservation rules and exact stop behavior. No scalar tariff, beta, hard cost-support bound, final feature freeze or final sample allocation was adopted.

## Verification

All commands and durations actually logged are in `commands_summary.json`; complete output/exit logs are adjacent. Tests use CPU tensors and fake decoder/workers/clocks, never a real model load. Existing historical tests also remain offline. Relevant commands used `.venv-inference/Scripts/python.exe` and `PYTHONPATH=src` (plus `tests` for named test invocations).

| Command/check | Result | Evidence |
|---|---|---|
| `scripts/p02d_accept.py` | PASS, exit 0; 115 snapshot/current hashes and four accepted artifacts before edits | acceptance_verification.json |
| `scripts/p02d_prepare.py` | PASS, exit 0; all 24 eligible, no collisions, 192 unique streams/seeds, 50 planned forwards | preparation_command.json; plan preparation_checks.json |
| First focused discovery | FAIL, exit 1; seven Windows sandbox temporary-directory access errors, before relevant fake tests could run | focused_tests_v1.json |
| Focused discovery after project-local TEMP/TMP | PASS, 17 tests, exit 0 | focused_tests_v2.json |
| `-m unittest discover -s tests -v` | PASS, 119 tests: 102 existing plus then-current 17 new checks, exit 0 | regression_suite.json |
| Expanded focused discovery | PASS, 19 tests, exit 0 | focused_tests_final.json |
| Targeted authorization/recovery/report follow-up | PASS, eight tests, exit 0 after follow-up guard changes | authorization_followup_tests.json |
| Feature-stage wall overshoot test | PASS, one additional focused check, exit 0; overshoot retained, answer stage blocked | feature_wall_test.json |
| `scripts/p02d_publish.py` | PASS, exit 0; immutable pending plan published | publication_command.json; plan_receipt.json |
| `scripts/p02d_verify.py` | PASS, exit 0; 2,529 bound files; real production entry rejects pending execution; no run directory created | verification_command.json; verification.json |
| Original reference/manuscript and historical source/tests/raw evidence | PASS, hashes unchanged; original PDF relevant contracts read with bundled pypdf | verification.json |
| GPU/model smoke, forward, generation, simulation, fitting, final collection | NOT RUN, explicitly unauthorized | zero-work accounting |

There are 20 distinct new focused checks in the final test file; the last additions were run in targeted follow-ups, not falsely presented as one final 122-test full-suite invocation. Current source and full test bytes are included for review. Offline fixtures do not validate live GPU performance or final theorem assumptions.

Other preparation failures: the initial ad-hoc tokenizer command used the lightweight `.venv` and lacked Transformers; the existing inference environment worked. `pdftotext` was unavailable, and the first bundled-pypdf console print hit cp1252 math-symbol encoding; UTF-8 extraction succeeded. No dependencies were installed. Prepublication adapter-reference and P01 native-ID exclusion corrections changed no question, prompt, stream or output; they are disclosed separately. No empirical attempt exists to discard or replace.

## Data, resources and provenance

New model loads **0**, GPU work/measurements **0**, feature forwards **0**, answer generations **0**, gate fits **0**, simulations **0**, final labels **0**. CPU native question/tokenizer materialization and fixture validation are preparation. Historical totals remain **75 admitted generations / 40,555 output tokens**, with P01's deliberate interruption a separate diagnostic. No current GPU verification is claimed.

The proposed limits are 192 slots, 393,216 output tokens, 50 forwards/102,400 feature positions, four hours cumulative conservative residency, five hours execution wall, and 0.5 GiB execution evidence including vectors/packet; feature sublimits are 15/20 minutes with 120-second forwards. Answer deadline is 120 seconds; reserve 300 seconds before each answer. Operational cancellation/cleanup can overshoot: actual costs are retained, not clipped, and unknown safe-stop state blocks work. Physical cost measurements do not settle the final scalar support problem. Preparation durations and local artifact sizes are separate from these unexecuted limits; exact packet and local directory sizes are in the external receipt.

The provenance follow-up reconciles the historical no-push statement with the later user report. Local `origin/codex/p02c-cr01-adoption` at 55e8fbd contains 4b0c200 and 53129ba; no remote query or restore verified current remote contents. A source/packet push does not prove complete off-machine coverage of ignored raw artifacts. The previous external P02C packet receipt is included in this handoff.

The supplied coordinator build archive is preserved with member/source hashes and attribution to external pdfTeX/BibTeX TeX Live 2023/Debian. It contains logs and renders, **no PDF bytes**. The coordinator's 13-page PDF hash `a97b04ac1bf319abef5f10b93630b01ea31d3f9798977509e60efc019eef9859` is recorded as reported, not independently verified here. Codex did not compile it; the original governing PDF and historical workstation unavailable-build statement remain unchanged. Missing derivative PDF does not block this preparation.

## Findings, limitations and next request

The fixed selection is eligible and the offline code paths pass the described checks. This establishes a reviewable prospective runner/plan, not successful live execution, feature throughput, routing performance or final-study feasibility. Startup hashes, supervisor/ledger work and source checks add real future overhead and are included in the applicable measured clocks. Total storage failure cannot guarantee a new evidence write; any missing record remains an integrity incident and must not be scored.

`execution_request.md` requests only the exact pending 192-answer/50-forward tranche under the stated ceilings. The 2.12-hour answer estimate and 136,808-token illustration come from a tiny P02B subset; a 2x timing scenario exceeds the four-hour ceiling before features. A truthful partial run is possible. Four inputs/family and K=4 do not settle population precision, independent-sample allocation, direct-perfect audit denominator adequacy, or a hard cost bound. The reference-dollar tariff remains unapproved. No external-drive purchase or backup condition was imposed on this local diagnostic; durable backup and final-study capacity remain required review items before irreplaceable final collection.

## Changes and decisions

| Item | Status | Impact |
|---|---|---|
| P02C acceptance | Recorded once, event 015 | Offline P02D only |
| CR01 cap/completion | Unchanged approved v1 | Fixed 2,048, descriptive completion; no old eligibility branch |
| Feature conventions/order | Explicit candidate recipe, no search | Prospectively bound for this diagnostic, not final freeze |
| Unified physical ledger/reservations | Implemented and offline tested | No tariff or hard mathematical support adopted |
| Native/P02B strict pipeline | Reused unchanged components | Original primary scores/evidence untouched |
| Scientific/resource decisions | Still open | Scalar cost/beta/support, final features/K/n/margins/backup await review |

## Acceptance checklist and packet

PASS: accepted history/hash preservation; fixed input/token/schedule eligibility; source/runtime binding; pending execution rejection; feature allowlist/pooling; cumulative budgets, incidents, cleanup and no replay; partial reporting and existing-contract targets; regression/focused checks; concrete pending execution request. NOT RUN: any actual model/GPU work, final freeze or P03 work. Compiled derivative PDF bytes absent, nonblocking.

The verified local `P02D_preflight_review_packet.zip`, hash index and external receipt include this report, exact plan/input/schedule/config records, changed and reused source/tests, native source/license closure, cached tokenizer/config snapshots (no weights), source diff/commits, logs, P02C packet/receipt and coordinator derivative build evidence. They exclude environments, weights, secrets and unrelated user material. Source/dependency manifests identify any runtime dependencies requiring the existing pinned environment for execution; this is not a claim to bundle a complete inference environment.

**P02D PREFLIGHT READY_FOR_REVIEW. Dispatch false. P02 incomplete/unsealed. P03 unstarted.** A separate conveyed execution authorization must bind the exact plan before any live work. No next phase or run starts automatically.
'''
(root/'reports/phases/P02D_preflight_completion.md').write_text(text,encoding='utf-8')
print('P02D PREFLIGHT READY_FOR_REVIEW; dispatch false; zero model work')
