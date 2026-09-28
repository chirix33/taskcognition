"""Publish the complete P02B plan without loading the answer model."""
import ctypes,dataclasses,difflib,importlib.metadata,json,platform,shutil,sys,subprocess
from datetime import datetime,timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import digest,file_hash
from taskcognition.p02_native import native_dataset,ENTRIES,gate_record
from taskcognition.p02b_runner import RUN,SYSTEM,identity

root=Path(__file__).resolve().parents[1];run=root/RUN;out=root/'reports/p02b'
assert not run.exists();assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
selection=dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),namespace='P02B-DEVELOPMENT',seeds={f:830260928+i*10000 for i,f in enumerate(ENTRIES)},index=0,size=1,serialized_input_ceiling=2048,native_defaults_unchanged=True,no_reselection=True,reserved_later_namespaces=read_json(root/'reports/p02a/selection_declaration.json')['reserved_namespaces'],order='draw outer, family next; cap order 1024/2048 if (family_index+draw)%2==0 else reverse; mode D/R if draw==0 else R/D; each input gets each cap first once',future_disjointness='No concrete later input manifest exists; reserved namespaces/seeds are not used, and later plans must reject historical latent/content hashes.')
write_new(out/'selection_declaration.json',selection)
from transformers import AutoTokenizer,GenerationConfig
model=read_json(root/'reports/p01/model_download.json');model_dir=root/model['local_directory']
for f in model['files']:assert file_hash(model_dir/f['name'])==f['sha256'],f['name']
tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False)
oldpackage=read_json(root/'artifacts/development/p02a-six-family/package.json')
oldconfig=oldpackage['generation_config']
oldsystem=oldpackage['wrapper']
write_new(out/'instruction_diff.json',dict(evidence_kind='development_observation',old=oldsystem,new=SYSTEM,old_sha256=digest(oldsystem),new_sha256=digest(SYSTEM),diff=''.join(difflib.unified_diff(oldsystem.splitlines(True),SYSTEM.splitlines(True),fromfile='P02A',tofile='P02B')),authority='exact fixed common instruction supplied in current P02B user prompt',no_native_question_change=True))
source={p.name:file_hash(p) for p in sorted((root/'src/taskcognition').glob('*.py'))}
environment={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
assert environment==read_json(root/'reports/p02a/runtime_preflight.json')['distributions'],'environment changed; stop'
package=dict(oldpackage,source_files=source,wrapper=SYSTEM,checkpoint='P02B',generation_config=oldconfig)
write_new(run/'package_base.json',package)
oldtexts=set();oldids=set()
for p in (root/'artifacts/development').glob('p*/requests/*.json'):
    q=read_json(p);oldtexts.add(digest(q['messages'][1]['content']));oldids.add(q['input_id'])
inputs={};seen=set()
for family in ENTRIES:
    prior=read_json(root/'artifacts/development/p02a-six-family/outcome_inputs'/f'{family}.json')
    config=dict(prior['effective_config'],seed=selection['seeds'][family],size=1)
    ds=native_dataset(root,family,config);entry=ds[0]
    assert dataclasses.asdict(ds.config)==config
    text_hash=digest(entry['question']);assert text_hash not in oldtexts|seen,'duplicate selected content; blocked, no replacement';seen.add(text_hash)
    latent=digest([family,config,0,entry['metadata']]);input_id=digest(['P02B-DEVELOPMENT',latent,text_hash]);assert input_id not in oldids
    gold=entry['answer'] if family!='graph_color' else json.dumps(entry['metadata']['possible_answer']);assert ds.score_answer(gold,entry)==1.
    row=dict(evidence_kind='development_observation',split='DEVELOPMENT',family=family,input_id=input_id,latent_hash=latent,question_hash=text_hash,entry=entry,entry_hash=digest(entry),effective_config=config,dataset_index=0,native_source_path=prior['native_source_path'],provisional=True)
    write_new(run/'outcome_inputs'/f'{family}.json',row)
    write_new(run/'gate_inputs'/f'{input_id}.json',dict(evidence_kind='development_observation',**gate_record(input_id,entry['question'])))
    inputs[family]=row
requests=[];packages={}
for draw in (0,1):
    for i,family in enumerate(ENTRIES):
        for cap in ((1024,2048) if (i+draw)%2==0 else (2048,1024)):
            config=dict(oldconfig,max_new_tokens=cap)
            assert {k:v for k,v in config.items() if k!='max_new_tokens'}=={k:v for k,v in oldconfig.items() if k!='max_new_tokens'}
            for mode in (('D','R') if draw==0 else ('R','D')):
                row=inputs[family];key=f'{len(requests):02d}_{family}_{mode}_{cap}_{draw}'
                messages=[dict(role='system',content=SYSTEM),dict(role='user',content=row['entry']['question'])]
                rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=mode=='R')
                assert SYSTEM in rendered and row['entry']['question'] in rendered,'exact instruction or question cannot be represented'
                ids=tokenizer.encode(rendered,add_special_tokens=False);assert len(ids)<=2048,'overlength selected input; blocked, no truncation/replacement'
                opening=rendered.rfind('<think>')>rendered.rfind('</think>');assert mode!='D' or not opening
                package_hash,stream=identity(package,mode,cap,row['input_id'],draw)
                package_key=f'{mode}_{cap}'
                if package_key not in packages:
                    pk=dict(evidence_kind='development_observation',base_sha256=file_hash(run/'package_base.json'),mode=mode,enable_thinking=mode=='R',cap=cap,effective_generation_config=config,package_hash=package_hash)
                    write_new(run/'packages'/f'{package_key}.json',pk);packages[package_key]=pk
                q=dict(evidence_kind='development_observation',split='DEVELOPMENT',request_id=key,purpose='fixed-format two-cap diagnostic, not formal cap selection',family=family,mode=mode,enable_thinking=mode=='R',cap=cap,max_new_tokens=cap,draw_index=draw,dataset_index=0,dataset_config=row['effective_config'],entry_hash=row['entry_hash'],input_id=row['input_id'],stream_id=stream,sampling_seed=int(stream[:15],16),package_hash=package_hash,messages=messages,rendered_prompt=rendered,rendered_prompt_hash=digest(rendered),input_ids=ids,input_tokens=len(ids),opening_in_prompt=opening,effective_generation_config=config,model_directory=model['local_directory'],source_files=source)
                write_new(run/'requests'/f'{key}.json',q)
                requests.append(dict(request_id=key,request_hash=digest(q),family=family,mode=mode,cap=cap,draw_index=draw,input_id=row['input_id'],stream_id=stream,sampling_seed=q['sampling_seed'],input_tokens=len(ids)))
assert len(requests)==48 and len({q['stream_id'] for q in requests})==48 and len({q['sampling_seed'] for q in requests})==48
assert sum(q['cap'] for q in requests)==73728
class Memory(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ('total_physical','available_physical','total_page','available_page','total_virtual','available_virtual','extended')]
m=Memory();m.length=ctypes.sizeof(m);assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
import taskcognition.p02b_worker as worker
assert Path(worker.__file__).resolve()==root/'src/taskcognition/p02b_worker.py'
write_new(out/'runtime_preflight.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,os=platform.platform(),cpu=platform.processor(),ram_bytes=m.total_physical,available_ram_bytes=m.available_physical,disk_free_bytes=shutil.disk_usage(root).free,model_files_verified=True,model_bytes=model['total_bytes'],distributions=environment,environment_unchanged_from_P02A=True,source_files=source,worker_import=Path(worker.__file__).relative_to(root).as_posix(),gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.used','--format=csv'],text=True),new_downloads=0,new_dependencies=0,input_lengths=[q['input_tokens'] for q in requests],source_native_manifest_sha256=file_hash(root/'vendor/reasoning_gym_p02a/source_manifest.json')))
bound={p.relative_to(root).as_posix():file_hash(p) for p in run.rglob('*.json')}
for name in ['reports/p02b/selection_declaration.json','reports/p02b/instruction_diff.json','reports/p02b/runtime_preflight.json','vendor/reasoning_gym_p02a/source_manifest.json']:bound[name]=file_hash(root/name)
write_new(run/'run_plan.json',dict(evidence_kind='development_observation',phase='P02B',output_directory=RUN,timestamp_utc=datetime.now(timezone.utc).isoformat(),requests=requests,source_files=source,bound_files=bound,selection=selection,limits=dict(dispatch_slots=48,reserved_output_tokens=73728,cap_reservations={'1024':24576,'2048':49152},gpu_residency_seconds=5400,execution_wall_seconds=7200,evidence_bytes=536870912,generation_deadline_seconds=120,request_reservation_seconds=300,J=0,concurrency=1),stop_rules=['every dispatch counts; unknown admission consumes slot','no retry/resume/replacement','incident/corrupt/missing evidence stops without model-score imputation','retain wrong/malformed/known timeout/cap outcomes','adequate load/deadline/cleanup reservation before next dispatch','always disable live dispatch in execution finally'],initial_counters=dict(dispatch=0,admitted_or_unknown=0,reserved_tokens=0),warmups=0,scientific_freeze=False))
print(json.dumps(dict(status='PASS',requests=48,reserved_tokens=73728,min_input_tokens=min(q['input_tokens'] for q in requests),max_input_tokens=max(q['input_tokens'] for q in requests),plan_sha256=file_hash(run/'run_plan.json'))))
