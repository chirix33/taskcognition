"""Replay retained outputs, disable dispatch, and derive integration tables/targets."""
import dataclasses, json, statistics, subprocess, sys
from datetime import datetime,timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import canonical,digest,file_hash,InputRecord,DrawRecord
from taskcognition.p01_ledger import reconcile,events
from taskcognition.p01_parsing import parse_and_score
from taskcognition.p02_native import native_dataset,syntax,ENTRIES
from taskcognition.p02_runner import RUN
from taskcognition.targets import aggregate

root=Path(__file__).resolve().parents[1];run=root/RUN;out=root/'reports/p02a'
assert (run/'execution_end.json').exists(),'execution still active'
statepath=root/'configs/phase_state.json';state=read_json(statepath)
snapshot=root/'configs/state_snapshots/P02A_dispatch_ended.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
rows=reconcile(run);plan=read_json(run/'run_plan.json');all_complete=len(rows)==24 and all(r['state']=='COMPLETE' for r in rows.values())
status='READY_FOR_REVIEW' if all_complete and read_json(out/'execution_command.json')['exit']==0 else 'BLOCKED'
event='configs/state_events/007_P02A_checkpoint.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),event='bounded_checkpoint_dispatch_disabled',previous_state_sha256=file_hash(snapshot),status=status,active_phase='P02A',parent_phase='P02',p02_complete=False,p02_sealed=False,real_dispatch_enabled=False,p01_dispatch_enabled=False))
state.update(status=status,real_dispatch_enabled=False,latest_event=event);statepath.write_bytes(canonical(state)+b'\n')
for name,h in plan['bound_files'].items():assert file_hash(root/name)==h,name
for name,h in plan['source_files'].items():assert file_hash(root/'src/taskcognition'/name)==h,name
observations=[];targets=[];cells=[]
from transformers import AutoTokenizer
model=read_json(root/'reports/p01/model_download.json')
tokenizer=AutoTokenizer.from_pretrained(root/model['local_directory'],local_files_only=True,trust_remote_code=False)
for family in ENTRIES:
    native=read_json(run/'outcome_inputs'/f'{family}.json');ds=native_dataset(root,family,native['effective_config']);entry=ds[0]
    assert digest(entry)==native['entry_hash']
    draws=[];packages={}
    for item in [r for r in plan['requests'] if r['family']==family]:
        key=item['request_id'];request=read_json(run/'requests'/f'{key}.json');packages[item['mode']]=request['package_hash']
        if key not in rows or rows[key]['state']!='COMPLETE':continue
        retained=rows[key];result=retained['result'];parsed=result['parsed']
        assert result['request_hash']==digest(request) and result['package_hash']==request['package_hash'] and result['stream_id']==request['stream_id']
        assert len(result['raw_token_ids'])==result['generated_tokens']<=1024
        assert tokenizer.decode(result['raw_token_ids'],skip_special_tokens=False)==result['raw_decoded_text']
        replay=parse_and_score(parsed['raw_decoded_text'],item['mode'],request['opening_in_prompt'],result['finish_reason'],lambda p:ds.score_answer(p,entry),lambda p:syntax(family,p))
        assert replay['native_score']==parsed['native_score'] and replay['strict_valid_final']==parsed['strict_valid_final']
        record=dict(evidence_kind='development_observation',family=family,mode=item['mode'],request_id=key,draw_index=item['draw_index'],strict_valid_final=parsed['strict_valid_final'],native_score=parsed['native_score'],perfect_correct=parsed['perfect_correct'],status=parsed['status'],failures=parsed['failure_flags'],finish_reason=result['finish_reason'],input_tokens=request['input_tokens'],output_tokens=result['generated_tokens'],generation_seconds=result['generation_seconds'],load_seconds=result['load_seconds'],worker_residency_seconds=retained['resource_seconds'],max_allocated_bytes=result['max_allocated_bytes'],max_reserved_bytes=result['max_reserved_bytes'],result_sha256=file_hash(run/'results'/f'{key}.json'))
        observations.append(record)
        score=parsed['native_score'];draw_status='perfect' if score==1 else 'partial' if score>0 else 'wrong' if parsed['strict_valid_final'] else 'admitted_failure'
        draws.append(DrawRecord('development_observation',digest([request['input_id'],request['package_hash'],item['draw_index']]),request['input_id'],'DEVELOPMENT',item['mode'],request['package_hash'],item['draw_index'],request['stream_id'],f'results/{key}.json',record['result_sha256'],score,score==1,retained['resource_seconds'],'diagnostic_worker_residency_seconds',draw_status))
    for mode in ('D','R'):
        cell=[o for o in observations if o['family']==family and o['mode']==mode]
        cells.append(dict(evidence_kind='development_observation',family=family,mode=mode,planned=2,executed=sum(r['request_id'] in rows for r in plan['requests'] if r['family']==family and r['mode']==mode),retained=len(cell),unexecuted=2-sum(r['request_id'] in rows for r in plan['requests'] if r['family']==family and r['mode']==mode),strict_valid_final=sum(o['strict_valid_final'] for o in cell),perfect_correct=sum(o['perfect_correct'] for o in cell),scores=[o['native_score'] for o in cell],failures=[o['failures'] for o in cell],output_tokens=[o['output_tokens'] for o in cell],generation_seconds=[o['generation_seconds'] for o in cell],worker_residency_seconds=[o['worker_residency_seconds'] for o in cell],max_allocated_bytes=max((o['max_allocated_bytes'] for o in cell),default=None),max_reserved_bytes=max((o['max_reserved_bytes'] for o in cell),default=None)))
    if len(draws)==4:
        inp=InputRecord('development_observation',native['input_id'],'DEVELOPMENT',family,native['latent_hash'],entry['question'],None,native['effective_config']['seed'],digest(native['effective_config']),native['native_source_path'],f'outcome_inputs/{family}.json')
        targets.append(dataclasses.asdict(aggregate(inp,draws,2,packages)))
write_new(out/'integration_observations.json',dict(evidence_kind='development_observation',rows=observations))
write_new(out/'twelve_cells.json',dict(evidence_kind='development_observation',cells=cells,formal_cap_sample=False))
write_new(out/'target_pipeline_checks.json',dict(evidence_kind='development_observation',unit='complete input cluster; cross-pairs not independent',K=2,rows=targets,equal_family_pipeline_means={key:sum(t[key] for t in targets)/6 for key in ('benefit','joint_spoilage','direct_redraw','decline_010','decline_025')} if len(targets)==6 else None,interpretation='pipeline checks only; no precision, superiority or significance claim'))
resources=dict(evidence_kind='development_observation',status=status,dispatched=len(rows),admitted=sum(e['event']=='admitted' for e in events(run)),reserved_tokens=sum(r['reserved_output_tokens'] for r in rows.values()),generated_tokens=sum(o['output_tokens'] for o in observations),conservative_gpu_residency_seconds=sum(r['resource_seconds'] for r in rows.values()),generation_seconds=sum(o['generation_seconds'] for o in observations),load_seconds=sum(o['load_seconds'] for o in observations),execution_wall_seconds=read_json(run/'execution_end.json')['execution_wall_seconds'],peak_allocated_bytes=max((o['max_allocated_bytes'] for o in observations),default=0),peak_reserved_bytes=max((o['max_reserved_bytes'] for o in observations),default=0),live_D_valid_final=sum(o['strict_valid_final'] for o in observations if o['mode']=='D'),software_incidents=len(list((run/'incidents').glob('*.json'))),warmups=0,gate_generations=0,gate_training=0,final_labels=0,scalar_cost='provisional conservative worker residency; not frozen audit support bounds',backup='local raw evidence plus verified local ZIP only; no off-machine backup')
write_new(out/'resources.json',resources)
lines=['# P02A twelve-cell integration','', 'Planned denominator is two in every cell. DEVELOPMENT diagnostic only; not the formal cap study.','', '| Family | Mode | Executed / retained / planned | Strict FINAL | Perfect | Native scores | Failure flags | Output tokens | Generation seconds | Worker seconds (cost) | Peak allocated / reserved MiB |','|---|---|---|---|---|---|---|---|---|---|---|']
for c in cells:lines.append(f'| {c["family"]} | {c["mode"]} | {c["executed"]}/{c["retained"]}/{c["planned"]} | {c["strict_valid_final"]}/2 | {c["perfect_correct"]}/2 | {c["scores"]} | {c["failures"]} | {c["output_tokens"]} | {[round(t,3) for t in c["generation_seconds"]]} | {[round(t,3) for t in c["worker_residency_seconds"]]} | {None if c["max_allocated_bytes"] is None else round(c["max_allocated_bytes"]/1024**2,2)} / {None if c["max_reserved_bytes"] is None else round(c["max_reserved_bytes"]/1024**2,2)} |')
lines+=['','Full precision, failure flags, individual generation times and memory are in twelve_cells.json and integration_observations.json. All cells retain their planned denominators; missing rows are not imputed.','','## Complete-cluster target checks','','| Family | T_b | T_h | h_DD | d_0.10 | d_0.25 |','|---|---|---|---|---|---|']
for t in targets:lines.append(f'| {t["family"]} | {t["benefit"]} | {t["joint_spoilage"]} | {t["direct_redraw"]} | {t["decline_010"]} | {t["decline_025"]} |')
(out/'integration_table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(resources,indent=2))
