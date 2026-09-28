"""Verify saved evidence, replay refusal and total P01 resources without model calls."""
import json
from pathlib import Path
import shutil
import subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import IntegrityError,digest,file_hash
from taskcognition.p01_ledger import events,reconcile
from taskcognition.p01_smoke import run_job
from taskcognition.p01_parsing import parse_and_score
from taskcognition.p01_native import native_dataset

root=Path(__file__).resolve().parents[1]
plan=read_json(root/'configs/p01_resource_plan.json')
run=root/plan['output_directory']
before={p.relative_to(run).as_posix():file_hash(p) for p in run.rglob('*') if p.is_file()}
rows=reconcile(run)
try:
    run_job(root,'interrupt_R')
    raise AssertionError('Restart improperly admitted an already dispatched request')
except IntegrityError as exc:
    rejection=str(exc)
    assert 'already dispatched' in rejection
after={p.relative_to(run).as_posix():file_hash(p) for p in run.rglob('*') if p.is_file()}
assert before==after
write_new(root/'reports/p01/restart_proof.json',{'evidence_kind':'development_observation',
          'purpose':'fresh process supervisor restart on real deliberately interrupted request',
          'rejection':rejection,'all_run_file_hashes_unchanged':True,'before_after_files':before,
          'admitted_before':len(rows),'admitted_after':len(reconcile(run)),
          'new_generation_dispatched':False})

dataset=native_dataset(root,plan['dataset_config'])
summaries=[]
for key,state in rows.items():
    request=read_json(run/'requests'/f'{key}.json')
    result=state['result']
    assert digest(request)==state['request_hash']==result['request_hash']
    assert result['package_hash']==request['package_hash']
    assert result['generated_tokens']==len(result['raw_token_ids'])<=1024
    expected=parse_and_score(result['parsed']['raw_decoded_text'],request['mode'],request['opening_in_prompt'],
                             result['finish_reason'],lambda p:dataset.score_answer(p,dataset[request['dataset_index']]))
    assert expected['native_score']==result['parsed']['native_score']
    assert expected['strict_valid_final']==result['parsed']['strict_valid_final']
    summaries.append({'request_id':key,'mode':request['mode'],'purpose':request['purpose'],
                      'input_id':request['input_id'],'input_tokens':request['input_tokens'],
                      'package_hash':request['package_hash'],'stream_id':request['stream_id'],
                      'generated_tokens':result['generated_tokens'],'finish_reason':result['finish_reason'],
                      'status':result['parsed']['status'],'score':result['parsed']['native_score'],
                      'valid_final':result['parsed']['strict_valid_final'],
                      'generation_seconds':result['generation_seconds'],'load_seconds':result['load_seconds'],
                      'tokens_per_generation_second':result['generated_tokens']/result['generation_seconds'],
                      'max_allocated_bytes':result['max_allocated_bytes'],'max_reserved_bytes':result['max_reserved_bytes'],
                      'resource_seconds':state['resource_seconds'],'result_path':(run/'results'/f'{key}.json').relative_to(root).as_posix(),
                      'result_sha256':file_hash(run/'results'/f'{key}.json')})
assert rows['initial_D']['result']['request_id']=='initial_D'
assert summaries[0]['input_id']==summaries[1]['input_id']
assert len({s['stream_id'] for s in summaries})==len(summaries)
all_dispatches=[]
for eventdir in (root/'artifacts/development').glob('p01-*/events'):
    for row in events(eventdir.parent):
        if row['event']=='dispatch':all_dispatches.append(row)
assert len(all_dispatches)==len(rows)==3
costs=[e for e in events(run) if e['event']=='resource']
gpu_check=read_json(root/'reports/p01/gpu_check.json')['process_elapsed_seconds']
seconds=sum(s['resource_seconds'] for s in summaries)+gpu_check
tokens=sum(s['generated_tokens'] for s in summaries)
assert seconds<1800 and tokens<=8192 and len(rows)<=8
sizes={name:sum(p.stat().st_size for p in (root/name).rglob('*') if p.is_file()) for name in
       ['.venv-inference','.cache/p01','artifacts/development','reports/p01','vendor/reasoning_gym_p01']}
assert sum(sizes.values())<40*1024**3
write_new(root/'reports/p01/smoke_summary.json',{'evidence_kind':'development_observation','split':'DEVELOPMENT',
          'scope':'P01 interface smoke; not package cap certification','requests':summaries,
          'actual_admitted_generations':3,'unknown_admission':0,'pre_admission_retries':0,'automatic_regenerations':0,
          'actual_output_tokens':tokens,'reserved_output_tokens':3072,'maximum_allowed_generations':8,
          'maximum_allowed_output_tokens':8192,'remaining_unused_generation_slots':5,
          'gpu_check_conservative_seconds':gpu_check,'total_conservative_gpu_residency_seconds':seconds,
          'gpu_envelope_seconds':1800,'resource_events':costs,'observed_limit_overshoot_seconds':0,
          'footprint_by_directory_bytes':sizes,'additional_footprint_measured_bytes':sum(sizes.values()),
          'disk_limit_bytes':40*1024**3,'free_disk_bytes':shutil.disk_usage(root).free,
          'D_live_valid_final_demonstrated':False,'R_live_valid_final_demonstrated':True,
          'controlled_real_interruption_demonstrated':True,'restart_replay_refused':True,
          'interruption_excluded_from_spontaneous_failure_interpretation':True,
          'main_study_freeze':False,'P02_executed':False})
write_new(run/'evidence_manifest.json',{'evidence_kind':'development_observation','split':'DEVELOPMENT',
          'files':{p.relative_to(run).as_posix():file_hash(p) for p in run.rglob('*') if p.is_file()}})
metadata=root/'reports/p01/model_metadata'
metadata.mkdir()
model=root/read_json(root/'reports/p01/model_download.json')['local_directory']
for name in ['config.json','generation_config.json','tokenizer_config.json','model.safetensors.index.json']:
    with (metadata/name).open('xb') as f:f.write((model/name).read_bytes())
write_new(metadata/'provenance.json',{'evidence_kind':'development_observation','model_id':plan['model_id'],
          'revision':plan['model_revision'],'files':{p.name:file_hash(p) for p in metadata.iterdir() if p.is_file()},
          'template_sha256':digest(read_json(model/'tokenizer_config.json')['chat_template'])})
print(json.dumps({'admitted':3,'output_tokens':tokens,'conservative_gpu_seconds':seconds,
                  'actual_footprint_GiB':sum(sizes.values())/1024**3,'restart':'REFUSED_WITHOUT_NEW_DISPATCH'}))
