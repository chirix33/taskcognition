"""Offline handoff only; calls the unchanged v4 production report after exit.

Never imports a model loader, dispatches a worker or changes a primary score.
Additional accounting distinguishes ledger dispatch from logged admission/work.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
from statistics import mean
import json,math,subprocess,time
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan
from taskcognition.p02d_ledger import scan
from taskcognition.p02d_reporting import report

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_execution';run=root/RUN
sha='c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365'
started=time.perf_counter();cpu=time.process_time()
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
assert read_json(out/'process_after.json')['p02d_processes']==[], 'safe stopped state not established'
command=read_json(out/'production_command.json')
plan=verify_plan(root,root/PLAN_DIR/'run_plan.json',sha)
state=scan(run,tolerant=True);result=report(root,plan)
write_new(out/'production_execution_report.json',result)
admitted={e['slot_id'] for e in state['events'] if e['event']=='admitted'}
retained={o['slot_id'] for o in result['observations']}
features={o['slot_id'] for o in result['feature_measurements']}
counts={}
for stage,schedule,kept in [('feature',plan['feature_schedule'],features),('answer',plan['requests'],retained)]:
 ids={q['slot_id'] for q in schedule};consumed=ids & state['slots'].keys()
 counts[stage]=dict(planned=len(ids),dispatched=len(consumed),admitted_logged=len(ids & admitted),retained=len(kept),
  unexecuted=len(ids-consumed),consumed_unscored=len(consumed-kept),reserved_before_load_without_logged_admission=len(consumed-admitted),
  unexecuted_slots=sorted(ids-consumed),unscored_consumed_slots=sorted(consumed-kept),
  slots_reserved_without_admission=sorted(consumed-admitted))
counts['feature']['recorded_completed_forwards']=len(features)
counts['feature']['completed_warmups']=sum(q['kind']=='warmup' and q['slot_id'] in features for q in plan['feature_schedule'])
counts['feature']['actual_work_note']='Completed result records establish performed forwards. Admission means a command was authorized, not proof of a completed forward; a pre-load reservation alone is not a forward.'
counts['answer']['known_output_tokens']=sum(o['output_tokens'] or 0 for o in result['observations'])
counts['answer']['retained_unknown_token_count']=sum(o['output_tokens'] is None for o in result['observations'])
counts['answer']['planned_output_reservation']=393216
counts['answer']['consumed_output_reservation']=sum(v['output_reservation'] for v in state['slots'].values())
partial_tokens=[]
for q in plan['requests']:
 if q['slot_id'] not in state['slots'] or q['slot_id'] in retained:continue
 p=run/'workers'/q['slot_id']/'incident.json'
 if p.exists():
  incident=read_json(p);tokens=incident.get('partial_token_ids')
  partial_tokens.append(dict(slot_id=q['slot_id'],observed_partial_tokens=len(tokens) if isinstance(tokens,list) else None,scored=False))
counts['answer']['unscored_partial_tokens']=partial_tokens
resources=[read_json(p) for p in sorted((run/'session_resources').glob('*.json'))]
feature_times=result['feature_measurements']
end=read_json(run/'execution_end.json') if (run/'execution_end.json').exists() else None
wall=read_json(run/'feature_stage_wall.json') if (run/'feature_stage_wall.json').exists() else None
summary=dict(evidence_kind='development_observation',status=result['status'],counts=counts,
 plan_sha256=sha,source_commit='b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4',
 authorization_commit=subprocess.check_output(['git','log','-1','--format=%H','--','configs/p02d_execution_authorization.json'],text=True).strip(),
 command_exit=command['exit'],command_wall_seconds=command['seconds'],runner_execution_end=end,feature_stage_wall=wall,
 worker_residency_seconds=state['measured_residency_seconds'],unknown_residency=state['unknown_residency'],
 completed_session_count=sum(s['ended'] for s in state['sessions'].values()),safe_stopped_sessions=sum(s['safe_stopped'] for s in state['sessions'].values()),
 resource_records=resources,load_seconds_by_session={r['session_id']:r['load_seconds'] for r in resources},
 cleanup_seconds_total=sum(r['cleanup_seconds'] for r in resources),
 feature_forward_seconds_including_warmups=sum(r['forward_seconds'] for r in feature_times),
 feature_forward_seconds_warmups=sum(r['forward_seconds'] for r in feature_times if r['kind']=='warmup'),
 feature_cpu_processing_seconds=sum(r['cpu_feature_seconds'] for r in feature_times),
 feature_input_positions_completed=sum(r['input_positions'] for r in feature_times),
 feature_input_positions_reserved=sum(v['input_positions'] for v in state['slots'].values()),
 feature_width=4096,feature_output_dtype='float32',feature_shape_finite_validation='unchanged production validate_result/gate_vector; only valid results counted',
 feature_max_abs_repeated_vector_difference=max((r['max_abs_difference_from_first'] for r in result['feature_stability']),default=None),
 feature_peak_allocated_bytes=max((r['max_allocated_bytes'] for r in feature_times if r['max_allocated_bytes'] is not None),default=None),
 feature_peak_reserved_bytes=max((r['max_reserved_bytes'] for r in feature_times if r['max_reserved_bytes'] is not None),default=None),
 answer_peak_allocated_bytes=max((r['max_allocated_bytes'] for r in result['observations'] if r['max_allocated_bytes'] is not None),default=None),
 answer_peak_reserved_bytes=max((r['max_reserved_bytes'] for r in result['observations'] if r['max_reserved_bytes'] is not None),default=None),
 overshoot=dict(worker_residency_seconds=max(0,state['measured_residency_seconds']-14400),
  execution_wall_seconds=max(0,end['wall_seconds']-18000) if end else None,
  feature_residency_seconds=max(0,state['sessions'].get('features',{}).get('seconds',0)-900) if state['sessions'].get('features',{}).get('ended') else None,
  feature_wall_seconds=wall['overshoot_seconds'] if wall else None),
 complete_K4_clusters=sum(c['complete_K4'] for c in result['clusters']),
 historical_before=dict(admitted_generations=75,output_tokens=40555,P01_interruption='separate deliberate diagnostic'),
 cost_once='Session residency is charged once. Load, nested forward/generation and cleanup timings are components, not additional charges. Wrapper wall overlaps runner wall; reporting/packaging measured separately.',
 scalar_tariff_beta_hard_support_adopted=False,reported_utc=datetime.now(timezone.utc).isoformat())
write_new(out/'execution_accounting.json',summary)
lines=['# P02D v4 execution: all planned cells','',
 'Primary scores are unchanged. Dispatched includes consumed reservations before load; logged admission and retained records are separate. No missing draw is imputed.',
 '', '| Family | Mode | Planned | Dispatched | Admitted | Retained | Unexecuted | Unscored consumed | Strict FINAL | Perfect | Partial scores | Tokens known |',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|']
for c in result['cells']:
 slots={q['slot_id'] for q in plan['requests'] if q['family']==c['family'] and q['mode']==c['mode']}
 lines.append(f"| {c['family']} | {c['mode']} | 16 | {c['executed']} | {len(slots & admitted)} | {c['retained']} | {16-c['executed']} | {c['executed']-c['retained']} | {c['strict_valid_final']} | {c['perfect_correct']} | {json.dumps([s for s in c['native_scores'] if 0<s<1])} | {sum(t or 0 for t in c['output_tokens'])} |")
lines+=['','## Failure subtypes, score distributions and measured costs','',
 'Exact score/token/duration/memory lists, including unknowns, are in production_execution_report.json. Values below are direct summaries of those primary records.','',
 '| Family / mode | Native scores | Wrapper subtype counts | Failure flags | Timeouts | Output lengths | Worker seconds sum |',
 '|---|---|---|---|---:|---|---:|']
for c in result['cells']:
 lines.append(f"| {c['family']} / {c['mode']} | {json.dumps(c['native_scores'])} | {json.dumps(c['wrapper_subtypes'])} | {json.dumps(c['failures'])} | {c['timeouts']} | {json.dumps(c['output_tokens'])} | {sum(c['worker_seconds']):.6f} |")
lines+=['','## All 24 input clusters','',
 'Only complete K=4 D/R clusters receive targets. T_b/T_h/redraw/partial-decline values are existing-contract pipeline checks, not independent cross-pair samples or routing evidence. Full input identities and unrounded target values are in the JSON report.','',
 '| Family / index | Input ID prefix | D scores | R scores | D perfect | D/R sample variance | Complete K4 | Targets |',
 '|---|---|---|---|---:|---|---|---|']
for c,item in zip(result['clusters'],plan['inputs']):
 lines.append(f"| {c['family']} / {item['dataset_index']} | {c['input_id'][:16]} | {json.dumps(c['within_input']['D']['scores'])} | {json.dumps(c['within_input']['R']['scores'])} | {c['direct_perfect_count']} | {json.dumps([c['within_input'][m]['sample_variance'] for m in ('D','R')])} | {c['complete_K4']} | {json.dumps(c['targets'])} |")
with (out/'cells_and_clusters.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines)+'\n')
lines=['# P02D feature timings and stability','',
 'Load is a once-per-worker component. Its repeated presence in result records must not be summed 50 times. Warm-ups are charged research work. Repeated vectors are repeated measurements of the same inputs, not additional independent labels. Every future routed query still incurs a live feature forward. CPU feature processing includes vector transfer, input-observable validation and gate-vector validation.','',
 '| Slot | Kind | Input ID prefix | Positions | Forward seconds | CPU feature processing seconds | Load component seconds | Max abs difference from first |',
 '|---|---|---|---:|---:|---:|---:|---:|']
stability={r['slot_id']:r for r in result['feature_stability']}
for r in feature_times:
 lines.append(f"| {r['slot_id']} | {r['kind']} | {r['input_id'][:16]} | {r['input_positions']} | {r['forward_seconds']!r} | {r['cpu_feature_seconds']!r} | {r['load_seconds']!r} | {stability[r['slot_id']]['max_abs_difference_from_first']!r} |")
with (out/'feature_measurements.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines)+'\n')
write_new(out/'offline_reporting_cost.json',dict(wall_seconds=time.perf_counter()-started,cpu_process_seconds=time.process_time()-cpu,
 includes_binding_verification=True,model_loads=0,feature_forwards=0,answer_generations=0,production_report_sha256=file_hash(out/'production_execution_report.json')))
print(json.dumps(dict(status=result['status'],counts=counts,worker_seconds=state['measured_residency_seconds'],complete_clusters=summary['complete_K4_clusters'])))
