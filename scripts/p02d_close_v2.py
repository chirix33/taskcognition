"""Record the reviewed-code correction without replacing the immutable v1 plan."""
from pathlib import Path
from datetime import datetime,timezone
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical

r=Path(__file__).resolve().parents[1];o=r/'reports/p02d';now=datetime.now(timezone.utc).isoformat()
v=read_json(o/'verification_v2.json');assert v['status']=='PASS'
assert read_json(o/'focused_tests_v2_revision.json')['exit']==0
old=read_json(o/'superseded_v1/plan_receipt.json')['sha256'];new=read_json(o/'plan_receipt.json')['sha256']
assert old!=new
a=r/'artifacts/development/p02d-cr01-plan-v1';b=r/'artifacts/development/p02d-cr01-plan-v2'
same=[p for p in a.rglob('*') if p.is_file() and p.name!='run_plan.json']
for p in same:assert file_hash(p)==file_hash(b/p.relative_to(a))
statepath=r/'configs/phase_state.json';state=read_json(statepath);assert not state['real_dispatch_enabled']
snapshot=r/'configs/state_snapshots/P02D_preflight_v1_before_v2.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
event='configs/state_events/017_P02D_preflight_v2_review_checkpoint.json'
write_new(r/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='P02D_PREFLIGHT_v2_READY_FOR_REVIEW',
    previous_state_sha256=file_hash(snapshot),superseded_plan_sha256=old,active_plan_sha256=new,
    reason='malformed readiness could break cost cleanup; repaired before execution and retested',
    identical_input_package_schedule_files=len(same),real_dispatch_enabled=False,new_model_work=0,p02_sealed=False,p03_started=False))
state.update(latest_event=event,p02d_plan_sha256=new,status='READY_FOR_REVIEW',checkpoint='PREFLIGHT',real_dispatch_enabled=False)
statepath.write_bytes(canonical(state)+b'\n')
with (r/'reports/decision_ledger.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## P02D pre-execution v2 correction ({now})\nMalformed readiness could cause an additional error while persisting load/cost evidence. Corrected optional load metric handling and outer supervisor incident reporting; all 21 new checks rerun. Immutable v1 plan {old}, v1 source commit fc2b8d4963e4e3473c2804d4d9ca79a75315d867 and v1 draft packet preserved. Active v2 plan {new}; all {len(same)} input/package/schedule files are byte-identical. No model work, retry or new selection. Dispatch false, no execution authorization.\n')
p=r/'reports/phases/P02D_preflight_completion.md';text=p.read_text(encoding='utf-8')
text=text.replace(old,new).replace('p02d-cr01-plan-v1/run_plan.json','p02d-cr01-plan-v2/run_plan.json')
text=text.replace('`unexecuted_plan_report.json`','`unexecuted_plan_report_v2.json`')
text=text.replace('There are 20 distinct new focused checks in the final test file; the last additions were run in targeted follow-ups, not falsely presented as one final 122-test full-suite invocation.',
    'There are 21 distinct new focused checks in the final test file; all 21 were rerun successfully after the v2 correction. The 102 unchanged legacy checks passed in the earlier combined 119-test run; this is not represented as a final 123-test combined invocation.')
text=text.replace('| GPU/model smoke, forward, generation, simulation, fitting, final collection |',
    '| v2 complete focused discovery | PASS, all 21 focused tests, exit 0 | focused_tests_v2_revision.json |\n| Active v2 production plan/source/authorization verification | PASS, exit 0; same 2,529 bound files, pending guard rejects | verification_command_v2.json; verification_v2.json |\n| GPU/model smoke, forward, generation, simulation, fitting, final collection |')
text=text.replace('## Findings, limitations and next request',f'''## Pre-execution v2 correction

At final review, a malformed worker-readiness record was found able to raise again while the supervisor constructed its cost record. The corrected implementation stores an invalid/missing load metric as unknown while preserving measured whole-session residency, safely stops the child, and retains the unscored incident. Outer supervisor failures are also retained for report inspection. A focused malformed-readiness test exercises this production cleanup path.

This was found before any live execution. Immutable v1 plan `{old}`, source commit `fc2b8d4963e4e3473c2804d4d9ca79a75315d867` and its draft packet/index/receipt are preserved in the repository and `reports/p02d/superseded_v1`. Active v2 is `{new}`. All {len(same)} input/package/schedule files are byte-identical; no question, seed, stream, cap or feature recipe changed. Event 017 records this preflight revision at {now}. No accepted historical evidence was rewritten. `verification.json` and earlier logs describe v1; `verification_v2.json` and `focused_tests_v2_revision.json` describe the active source/plan. The active receipt supersedes the v1 draft receipt for execution review.

## Findings, limitations and next request''')
p.write_text(text,encoding='utf-8')
write_new(o/'v2_validation_summary.json',dict(evidence_kind='development_observation',timestamp_utc=now,active_plan_sha256=new,
    superseded_plan_sha256=old,identical_materialized_files=len(same),focused_tests=21,
    command_logs=['focused_tests_v2_revision.json','publication_command_v2.json','verification_command_v2.json'],
    new_model_loads=0,new_generations=0,new_forwards=0,real_dispatch_enabled=False))
print('P02D PREFLIGHT v2 READY_FOR_REVIEW; identical inputs/schedules; dispatch false')
