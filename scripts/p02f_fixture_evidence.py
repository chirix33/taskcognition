"""Write small CPU-only P02F fixtures; never imports or constructs a model."""
from pathlib import Path
from datetime import datetime,timezone
import json, sys, time
from p02f_prepare import ROOT, OUT, read, write, sha
from taskcognition.p02f_cost_v1 import run_fixture, ScriptedWorker, recover

start,cpu=time.perf_counter(),time.process_time()
base=ROOT/'artifacts/fixtures/p02f-cost-v1-evidence'
if base.exists():raise RuntimeError('fixture evidence root already exists; no overwrite')
records={}
cases=[('warmup_augmented',ScriptedWorker(),dict(warmups=2)),
       ('retained_failure',ScriptedWorker(fault='known_model_failure'),{}),
       ('feature_incident',ScriptedWorker(fault='feature'),{}),
       ('unsafe_stop',ScriptedWorker(fault='known_timeout',safe_stop=False),{}),
       ('overshoot',ScriptedWorker(answer_seconds=500),{})]
for name,worker,kwargs in cases:
    records[name]=run_fixture(ROOT,base/name,'slot_000','R',worker,**kwargs)
first=run_fixture(ROOT,base/'resource_stop','slot_000','D',ScriptedWorker(),remaining_seconds=465)
stop=run_fixture(ROOT,base/'resource_stop','slot_001','R',ScriptedWorker(),remaining_seconds=465)
records['resource_stop']=dict(first=first,stop=stop,recovered=recover(base/'resource_stop'))
write(OUT/'fixture_results.json',dict(evidence_kind='fixture',not_empirical=True,
    synthetic_clock_units='illustrative seconds, not observed hardware measurements',records=records))
write(OUT/'fixture_files.json',dict(evidence_kind='fixture',files={
    p.relative_to(ROOT).as_posix():sha(p) for p in sorted(base.rglob('*')) if p.is_file()}))
write(OUT/'accounting_schema.json',dict(version='P02F-cost-fixture-v1',kind='offline_prototype_schema_not_plan',
    serving_variable='t_safe_terminal_ack - t_first_charged_validation; unknown if safe stop unconfirmed',
    units='monotonic seconds; fixture values synthetic',
    exclusive_fields=['phase_start','phase_end','phase_name','validity','query_identity'],
    nested_fields=['parent_phase','nested_start','nested_end'],
    accounting_fields=['observed_elapsed_seconds','total_service_seconds_or_null','incurred_lower_bound_seconds',
        'exclusive_component_seconds','unallocated_residual_seconds','safe_stopped','overshoot_seconds'],
    control_not_cost=['reservation_seconds','output_tokens_reserved','deadline_seconds'],
    output_usage=['observed_output_tokens_or_null','unknown_output_count','reserved_output_tokens'],
    actual_head_cost=None,hard_support_bound=None,scalar_cost_adopted=False,
    future_gate_interface=dict(inputs=['embedding[4096]','nine approved input-only observables'],
        join_metadata_outside_learner=['input_id'],outputs=['method-specific raw/calibrated values','action','measured CPU costs','configuration hashes'],
        implementation=None,architecture_parity_and_calibration='unresolved'),
    no_execution_plan=True,dispatch=False))
assert not any(m in sys.modules for m in ['torch','transformers','numpy','taskcognition.audit','taskcognition.p02d_runner'])
write(OUT/'fixture_run_receipt.json',dict(status='PASS',evidence_kind='fixture',timestamp_utc=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(ROOT/'src/taskcognition/p02f_cost_v1.py'),script_sha256=sha(Path(__file__)),
    wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
    fixture_cases=6,actual_model_loads=0,actual_forwards=0,actual_answers=0,actual_gpu_work=0,
    note='Fake stages only; no final audit, learned gate or full-pipeline simulation.'))
print(json.dumps(dict(status='PASS',fixture_cases=6,model_work=0)))
