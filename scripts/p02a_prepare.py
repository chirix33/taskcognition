"""Offline-only immutable six-input/24-request preparation; no model loading."""
import ctypes, dataclasses, difflib, importlib.metadata, json, os, platform, shutil, subprocess, sys
from datetime import datetime,timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import digest,file_hash,stream_id
from taskcognition.p02_native import native_dataset,gate_record,ENTRIES
from taskcognition.p02_runner import RUN

root=Path(__file__).resolve().parents[1];run=root/RUN
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
assert not run.exists()
now=datetime.now(timezone.utc).isoformat()
# Written before native item generation and before tokenizer inspection.
selection={'evidence_kind':'development_observation','timestamp_utc':now,'namespace':'P02A-DEVELOPMENT',
 'seeds':{f:720260928+i*10000 for i,f in enumerate(ENTRIES)},'index':0,'size':1,
 'difficulty':'all native dataclass defaults; only seed/size overridden',
 'serialized_input_ceiling':2048,'ceiling_reason':'provisional conservative SDPA MATH memory allowance; input+1024 <=3072, below native checkpoint context; no truncation/reselection',
 'reserved_namespaces':['P02-CAP-1024','P02-CAP-2048','P02-HIGH-REPEAT','FINAL-TRAIN','FINAL-TUNE','FINAL-AUDIT','FINAL-TEST'],
 'future_disjointness':'future plans must reject P01/P02A latent and question hashes as well as distinct namespace/seed; namespaces alone do not prove disjointness'}
write_new(root/'reports/p02a/selection_declaration.json',selection)
from transformers import AutoTokenizer,GenerationConfig
model=read_json(root/'reports/p01/model_download.json');model_dir=root/model['local_directory']
for f in model['files']:
    assert file_hash(model_dir/f['name'])==f['sha256'],f['name']
tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False)
config=GenerationConfig.from_pretrained(model_dir,local_files_only=True)
config.update(do_sample=True,temperature=.6,top_p=.95,top_k=20,min_p=0.,max_new_tokens=1024,num_beams=1,num_return_sequences=1,use_cache=True,return_dict_in_generate=False,output_scores=False,output_logits=False)
config.pad_token_id=config.eos_token_id[0] if isinstance(config.eos_token_id,list) else config.eos_token_id
original=read_json(root/'artifacts/development/p01-windows-5090-20260928-v2/requests/initial_D.json')['messages'][0]['content']
wrapper=original+' The task\'s requested answer format belongs inside the FINAL tags, even when the task says to output only the answer.'
write_new(root/'reports/p02a/prompt_diff.json',dict(evidence_kind='development_observation',original=original,revised=wrapper,diff=''.join(difflib.unified_diff([original+'\n'],[wrapper+'\n'],fromfile='P01',tofile='P02A')),revision_fixed_before_outputs=True,parser_unchanged=True))
source={p.name:file_hash(p) for p in sorted((root/'src/taskcognition').glob('*.py'))}
package=dict(evidence_kind='development_observation',model_id=model['model_id'],revision=model['revision'],precision='BF16',attention='sdpa forced MATH',generation_config=config.to_dict(),source_files=source,model_files={f['name']:f['sha256'] for f in model['files']},wrapper=wrapper,native_source_manifest_sha256=file_hash(root/'vendor/reasoning_gym_p02a/source_manifest.json'),torch=importlib.metadata.version('torch'),transformers=importlib.metadata.version('transformers'),cap_includes_thinking_and_final=True)
write_new(run/'package.json',package)
oldtexts=set()
for p in (root/'artifacts/development').glob('p01*/requests/*.json'):
    oldtexts.add(digest(read_json(p)['messages'][1]['content']))
inputs={};hashes=set();validation=[]
sys.path.insert(0,str(root/'tests'))
from test_p02a import scorer_cases
for family in ENTRIES:
    ds=native_dataset(root,family,dict(seed=selection['seeds'][family],size=1));effective=dataclasses.asdict(ds.config);entry=ds[0]
    text_hash=digest(entry['question']);assert text_hash not in oldtexts|hashes;hashes.add(text_hash)
    latent=digest([family,effective,0,entry['metadata']]);input_id=digest(['P02A-DEVELOPMENT',latent,text_hash])
    gold=entry['answer'] if family!='graph_color' else json.dumps(entry['metadata']['possible_answer'])
    assert ds.score_answer(gold,entry)==1.
    record=dict(evidence_kind='development_observation',split='DEVELOPMENT',family=family,input_id=input_id,latent_hash=latent,question_hash=text_hash,entry=entry,entry_hash=digest(entry),effective_config=effective,dataset_index=0,native_source_path=f'vendor/reasoning_gym_p02a/reasoning_gym/{ENTRIES[family][0]}/{family}.py',provisional=True)
    write_new(run/'outcome_inputs'/f'{family}.json',record);write_new(run/'gate_inputs'/f'{input_id}.json',gate_record(input_id,entry['question']));inputs[family]=record
    fixture,cases=scorer_cases()[family]
    validation.append(dict(evidence_kind='fixture',family=family,cases=[dict(payload=p,expected=s,observed=ds.score_answer(p,fixture)) for p,s in cases],fixture=fixture,native_gold_check=ds.score_answer(gold,entry)))
write_new(root/'reports/p02a/native_scorer_checks.json',dict(evidence_kind='fixture',checks=validation,model_generations=0))
requests=[]
for draw in range(2):
    for family in ENTRIES:
        for mode in ('D','R'):
            row=inputs[family];key=f'{len(requests):02d}_{family}_{mode}_{draw}'
            messages=[{'role':'system','content':wrapper},{'role':'user','content':row['entry']['question']}]
            rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=mode=='R')
            ids=tokenizer.encode(rendered,add_special_tokens=False);assert len(ids)<=2048,'selected input blocked, no replacement'
            opening=rendered.rfind('<think>')>rendered.rfind('</think>')
            assert mode!='D' or not opening
            package_hash=digest({**package,'mode':mode,'enable_thinking':mode=='R'})
            stream=stream_id('P02A-DEVELOPMENT',2026092802,'DEVELOPMENT',row['input_id'],package_hash,draw)
            request=dict(evidence_kind='development_observation',split='DEVELOPMENT',request_id=key,purpose='six-family integration diagnostic; not formal cap sample',family=family,mode=mode,enable_thinking=mode=='R',draw_index=draw,dataset_index=0,dataset_config=row['effective_config'],entry_hash=row['entry_hash'],input_id=row['input_id'],stream_id=stream,sampling_seed=int(stream[:15],16),package_hash=package_hash,messages=messages,rendered_prompt=rendered,rendered_prompt_hash=digest(rendered),input_ids=ids,input_tokens=len(ids),opening_in_prompt=opening,effective_generation_config=config.to_dict(),max_new_tokens=1024,model_directory=model['local_directory'],source_files=source)
            write_new(run/'requests'/f'{key}.json',request)
            requests.append(dict(request_id=key,request_hash=digest(request),family=family,mode=mode,draw_index=draw,stream_id=stream,input_id=row['input_id'],input_tokens=len(ids)))
assert len({r['stream_id'] for r in requests})==24
bound={p.relative_to(root).as_posix():file_hash(p) for p in run.rglob('*.json')}
bound['vendor/reasoning_gym_p02a/source_manifest.json']=file_hash(root/'vendor/reasoning_gym_p02a/source_manifest.json')
write_new(run/'run_plan.json',dict(evidence_kind='development_observation',timestamp_utc=now,phase='P02A',source_files=source,bound_files=bound,requests=requests,selection=selection,package_sha256=file_hash(run/'package.json'),limits=dict(answer_generations=24,reserved_output_tokens=24576,total_new_tokens_per_generation=1024,gpu_residency_seconds=5400,execution_wall_seconds=7200,evidence_bytes=536870912,additional_source_dependency_bytes=1073741824,timeout_seconds=120,J=0,concurrency=1,request_reservation_seconds=300),initial_counters=dict(dispatched=0,admitted_or_unknown=0,reserved_tokens=0),stop_rules=['no replacement or retry','missing/corrupt/software incident stops; unscored','retain known timeouts/caps/wrong/malformed','reserve load+deadline+cleanup before dispatch','no further dispatch if remaining budget insufficient'],warmups=0,scientific_freeze=False))
import taskcognition.p02_worker as worker,taskcognition.p01_ledger as ledger
write_new(root/'reports/p02a/runtime_preflight.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,os=platform.platform(),cpu=platform.processor(),disk_free_bytes=shutil.disk_usage(root).free,model_files_verified=True,model_bytes=model['total_bytes'],gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.used','--format=csv'],text=True),imports={m.__name__:dict(path=Path(m.__file__).relative_to(root).as_posix(),sha256=file_hash(Path(m.__file__))) for m in [worker,ledger]},distributions={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},numpy_version=importlib.metadata.version('numpy'),additional_dependency_installs=0,plan_sha256=file_hash(run/'run_plan.json'),input_lengths=[r['input_tokens'] for r in requests],checkpoint_max_position_embeddings=read_json(model_dir/'config.json')['max_position_embeddings']))
print(json.dumps(dict(status='PASS',requests=len(requests),max_input_tokens=max(r['input_tokens'] for r in requests),plan_sha256=file_hash(run/'run_plan.json'))))
