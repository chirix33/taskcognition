"""Offline replay, incomplete-safe reporting and checkpoint closure; no model loads."""
import dataclasses,json,statistics
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import canonical,digest,file_hash,InputRecord,DrawRecord
from taskcognition.p01_parsing import parse_and_score
from taskcognition.p02_native import native_dataset,syntax,ENTRIES
from taskcognition.p02b_runner import RUN
from taskcognition.p02b_reporting import inspect_ledger,primary_record,diagnostic_payload,cell_summary
from taskcognition.targets import aggregate

root=Path(__file__).resolve().parents[1];run=root/RUN;out=root/'reports/p02b'
state=read_json(root/'configs/phase_state.json');assert state['real_dispatch_enabled'] is False,'report requires live dispatch closed'
plan=read_json(run/'run_plan.json');inspection=inspect_ledger(run);incidents=inspection['incidents'];rows=inspection['rows']
for n,h in plan['bound_files'].items():
    try:
        if file_hash(root/n)!=h:raise ValueError('bound-file mismatch')
    except Exception as exc:incidents.append(dict(path=n,error=str(exc)))
observations=[];diagnostics=[];targets=[];requests={};inputrows={}
from transformers import AutoTokenizer
model=read_json(root/'reports/p01/model_download.json')
tokenizer=AutoTokenizer.from_pretrained(root/model['local_directory'],local_files_only=True,trust_remote_code=False)
for item in plan['requests']:
    key=item['request_id']
    try:q=read_json(run/'requests'/f'{key}.json');requests[key]=q
    except Exception as exc:
        incidents.append(dict(request_id=key,error='request integrity: '+str(exc),scored=False));continue
    if key not in rows:continue
    row=rows[key]
    try:
        obs=primary_record(q,row)
        if obs is None:continue
        result=row['result'];family=q['family']
        native=read_json(run/'outcome_inputs'/f'{family}.json');inputrows[family]=native
        ds=native_dataset(root,family,native['effective_config']);entry=ds[0]
        if digest(entry)!=q['entry_hash']:raise ValueError('native entry changed')
        if result.get('parsed') is not None:
            parsed=result['parsed']
            if tokenizer.decode(result['raw_token_ids'],skip_special_tokens=False)!=result['raw_decoded_text']:raise ValueError('raw token decode mismatch')
            replay=parse_and_score(parsed['raw_decoded_text'],q['mode'],q['opening_in_prompt'],result['finish_reason'],lambda p:ds.score_answer(p,entry),lambda p:syntax(family,p))
            for field in ('native_score','strict_valid_final','perfect_correct','final_payload','final_channel','thinking'):
                if replay[field]!=parsed[field]:raise ValueError('parser replay mismatch: '+field)
            diagnostic=diagnostic_payload(family,parsed)
            if diagnostic:
                diagnostics.append(dict(evidence_kind='development_observation',request_id=key,family=family,mode=q['mode'],cap=q['max_new_tokens'],primary_score=parsed['native_score'],diagnostic_native_score=ds.score_answer(diagnostic['payload'],entry),**diagnostic))
        observations.append(dict(evidence_kind='development_observation',request_id=key,family=family,mode=q['mode'],cap=q['max_new_tokens'],draw_index=q['draw_index'],input_id=q['input_id'],worker_seconds=row['resource_seconds'],max_allocated_bytes=result.get('max_allocated_bytes'),max_reserved_bytes=result.get('max_reserved_bytes'),load_seconds=result.get('load_seconds'),result_sha256=row['result_sha256'],**obs))
    except Exception as exc:incidents.append(dict(request_id=key,error_type=type(exc).__name__,error=str(exc),scored=False))
cells=[cell_summary(plan,inspection,observations,f,m,c) for c in (1024,2048) for f in ENTRIES for m in ('D','R')]
for family in ENTRIES:
    for cap in (1024,2048):
        cluster=[o for o in observations if o['family']==family and o['cap']==cap]
        if len(cluster)!=4 or any(o['worker_seconds'] is None for o in cluster):continue
        native=inputrows[family];draws=[];packages={}
        for o in cluster:
            q=requests[o['request_id']];score=o['native_score'];packages[q['mode']]=q['package_hash']
            status='perfect' if score==1 else 'partial' if score>0 else 'wrong' if o['strict_valid_final'] else 'admitted_failure'
            draws.append(DrawRecord('development_observation',digest([q['input_id'],q['package_hash'],q['draw_index']]),q['input_id'],'DEVELOPMENT',q['mode'],q['package_hash'],q['draw_index'],q['stream_id'],f'results/{q["request_id"]}.json',o['result_sha256'],score,score==1,o['worker_seconds'],'diagnostic_worker_residency_seconds',status))
        inp=InputRecord('development_observation',native['input_id'],'DEVELOPMENT',family,native['latent_hash'],native['entry']['question'],None,native['effective_config']['seed'],digest(native['effective_config']),native['native_source_path'],f'outcome_inputs/{family}.json')
        targets.append(dict(cap=cap,**dataclasses.asdict(aggregate(inp,draws,2,packages))))
complete=len(observations)==48 and len(rows)==48 and not incidents and all(row['resource_seconds'] is not None for row in rows.values())
status='READY_FOR_REVIEW' if complete else 'BLOCKED'
knownseconds=sum(row['resource_seconds'] or 0 for row in rows.values())
resources=dict(evidence_kind='development_observation',status=status,planned=48,dispatched=len(rows),retained=len(observations),reserved_output_tokens=sum(row['reserved_tokens'] for row in rows.values()),known_generated_tokens=sum(o['output_tokens'] or 0 for o in observations),unknown_output_token_count=sum(o['output_tokens'] is None for o in observations)+sum(row['result'] is None for row in rows.values()),conservative_gpu_residency_seconds=knownseconds,resource_records_missing=[key for key,row in rows.items() if row['resource_seconds'] is None],cost_is_lower_bound_if_records_missing=any(row['resource_seconds'] is None for row in rows.values()),execution=read_json(run/'execution_end.json') if (run/'execution_end.json').exists() else None,known_generation_seconds=sum(o['generation_seconds'] or 0 for o in observations),known_load_seconds=sum(o['load_seconds'] or 0 for o in observations),peak_allocated_bytes=max((o['max_allocated_bytes'] or 0 for o in observations),default=0),peak_reserved_bytes=max((o['max_reserved_bytes'] or 0 for o in observations),default=0),incidents=incidents,unexecuted=[q['request_id'] for q in plan['requests'] if q['request_id'] not in rows] if inspection['chain_complete'] else None,dispatched_without_retained_result=[key for key in rows if key not in {o['request_id'] for o in observations}],new_model_downloads=0,dependency_changes=0,encoder_forwards=0,gate_training=0,final_labels=0,backup='local raw evidence plus local review ZIP; no off-machine backup')
for name,data in [('observations',observations),('twenty_four_cells',cells),('failure_diagnostics',diagnostics),('cap_specific_targets',targets)]:write_new(out/f'{name}.json',dict(evidence_kind='development_observation',rows=data))
write_new(out/'resources.json',resources)
write_new(out/'incomplete_and_incident_inventory.json',dict(evidence_kind='development_observation',rows={key:{k:v for k,v in row.items() if k!='result'} for key,row in rows.items()},incidents=incidents,unexecuted=resources['unexecuted'],dispatched_without_retained_result=resources['dispatched_without_retained_result']))
lines=['# P02B 24-cell diagnostic','', 'One input per family; K=2 per mode/cap. All primary scores preserved. This is not formal cap selection.','', '| Family | Mode | Cap | Planned/executed/retained | Strict FINAL | Perfect | Native scores | Wrapper subtype | Syntax / cap-no-final / timeout | Output tokens | Worker seconds |','|---|---|---|---|---|---|---|---|---|---|---|']
for c in cells:lines.append(f'| {c["family"]} | {c["mode"]} | {c["cap"]} | {c["planned"]}/{c["executed"]}/{c["retained"]} | {c["strict_valid_final"]}/2 | {c["perfect_correct"]}/2 | {c["native_scores"]} | {c["wrapper_subtypes"]} | {c["native_syntax_failure"]}/{c["cap_without_final"]}/{c["timeout"]} | {c["output_tokens"]} | {[None if t is None else round(t,3) for t in c["worker_seconds"]]} |')
lines+=['','Missing/unexecuted records and incidents are listed explicitly in incomplete_and_incident_inventory.json. None is imputed as a zero. Per-request generation/load times and allocated/reserved memory are in observations.json.','','## Cap-specific input-cluster targets','','| Family | Cap | T_b | T_h | h_DD | d_0.10 | d_0.25 |','|---|---|---|---|---|---|---|']
for t in targets:lines.append(f'| {t["family"]} | {t["cap"]} | {t["benefit"]} | {t["joint_spoilage"]} | {t["direct_redraw"]} | {t["decline_010"]} | {t["decline_025"]} |')
lines+=['','No cross-cap pooling. Independent stochastic draws share each native input; an observed 2,048 output is not a continuation of an observed 1,024 output. Cross-pairs are not independent samples.','','## Offline payload-only diagnostics — never primary scores','','| Request | Primary score | Diagnostic native score | Eligibility |','|---|---|---|---|']
for d in diagnostics:lines.append(f'| {d["request_id"]} | {d["primary_score"]} | {d["diagnostic_native_score"]} | {d["kind"]} |')
lines+=['','Only an already bare, syntactically valid payload or one uniquely tagged payload with outside prose is eligible. No selection among competing answers, thinking-channel text, extraction from explanatory prose, rewriting or deployment repair. Text-native bare diagnostics require unmistakable count/assignment syntax. Primary completion counts and scores remain unchanged.']
(out/'integration_table.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
event='configs/state_events/011_P02B_review_checkpoint.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),event='P02B_review_checkpoint',status=status,previous_state_sha256=file_hash(root/'configs/phase_state.json'),real_dispatch_enabled=False,p02_complete=False,p02_sealed=False))
state.update(status=status,real_dispatch_enabled=False,latest_event=event);(root/'configs/phase_state.json').write_bytes(canonical(state)+b'\n')
print(json.dumps(resources,indent=2))
