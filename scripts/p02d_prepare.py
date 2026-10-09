"""CPU-only fixed-selection materialization; no model loader or forward."""
import dataclasses, importlib.metadata, json, platform, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import digest,file_hash
from taskcognition.p02_native import ENTRIES,native_dataset
from taskcognition.p02b_runner import SYSTEM
from taskcognition.p02d_features import FEATURE_SPEC,cheap_features,validate_gate_input,forward_schedule
from taskcognition.p02d_plan import PLAN_DIR,RUN,VERSION,MODEL_REVISION,identity

root=Path(__file__).resolve().parents[1];out=root/PLAN_DIR
assert not out.exists()
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
selection=dict(evidence_kind='development_observation',split='DEVELOPMENT',namespace='P02D-CR01-DEVELOPMENT-v1',
    seeds={f:930261005+10000*i for i,f in enumerate(ENTRIES)},size=4,indices=[0,1,2,3],
    input_ceiling_each_path=2048,no_truncation=True,no_reselection=True,
    answer_order='draw outer 0..3; index next 0..3; family inner established order; D,R if (index+draw)%2==0 else R,D',
    feature_order='family-major input list; warmup first two; all 24; two extras adjacent per each family indices 0 and 1')
write_new(out/'selection.json',selection)
model=read_json(root/'reports/p01/model_download.json');modeldir=root/model['local_directory']
metadata={f['name']:f['sha256'] for f in model['files'] if not f['name'].endswith('.safetensors')}
for n,h in metadata.items():assert file_hash(modeldir/n)==h,n
config=read_json(modeldir/'config.json');assert config['hidden_size']==FEATURE_SPEC['hidden_width']==4096
from transformers import AutoTokenizer
tokenizer=AutoTokenizer.from_pretrained(modeldir,local_files_only=True,trust_remote_code=False)
environment={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
assert environment==read_json(root/'reports/p02b/runtime_preflight.json')['distributions'],'environment changed'
source=Path(sys.executable).parent.parent/'Lib/site-packages/transformers/models/qwen3/modeling_qwen3.py'
text=source.read_text(encoding='utf-8');start=text.index('class Qwen3Model(');end=text.index('class Qwen3ForCausalLM(')
assert 'hidden_states = self.norm(hidden_states)' in text[start:end] and 'last_hidden_state=hidden_states' in text[start:end]
write_new(out/'environment.json',dict(evidence_kind='development_observation',python=sys.version,platform=platform.platform(),
    interpreter='.venv-inference/Scripts/python.exe',distributions=environment,model_directory=model['local_directory'],
    model_revision=MODEL_REVISION,model_files={f['name']:dict(sha256=f['sha256'],bytes=f['bytes']) for f in model['files']},
    tokenizer_metadata_verified=metadata,hidden_width=config['hidden_size'],context_limit=config['max_position_embeddings'],
    qwen3_installed_source_sha256=file_hash(source),source_semantics='Qwen3Model.forward calls self.norm immediately before returning last_hidden_state',
    model_weights_loaded=False,forwards=0,new_dependencies=0,new_downloads=0,
    disk_free_bytes=shutil.disk_usage(root).free,hardware_reference='reports/p02b/runtime_preflight.json; historical GPU/driver, no new GPU measurement'))
(out/'source_snapshots').mkdir()
(out/'source_snapshots/modeling_qwen3.py').write_bytes(source.read_bytes())
write_new(out/'feature_specification.json',FEATURE_SPEC)
oldq=set();oldid=set();oldlatent=set();nativeids=set();sources=[]
for p in sorted((root/'artifacts/development').glob('p*/requests/*.json')):
    q=read_json(p);oldq.add(digest(q['messages'][1]['content']));oldid.add(q['input_id']);sources.append(p.relative_to(root).as_posix())
    if p.parent.parent.name.startswith('p01-'):
        p01=read_json(root/'configs/p01_resource_plan.json')
        nativeids.add(digest([p01['family'],p01['dataset_config']['seed'],q['dataset_index']]))
for p in sorted((root/'artifacts/development').glob('p*/outcome_inputs/*.json')):
    row=read_json(p);oldlatent.add(row['latent_hash'])
    nativeids.add(digest([row['family'],row['effective_config'].get('seed'),row['dataset_index']]))
reserved=read_json(root/'reports/p02a/selection_declaration.json')['reserved_namespaces']
inputs=[];seen=set();collisions=[]
for fi,family in enumerate(ENTRIES):
    prior=read_json(root/'artifacts/development/p02a-six-family/outcome_inputs'/f'{family}.json')
    cfg=dict(prior['effective_config'],seed=selection['seeds'][family],size=4)
    ds=native_dataset(root,family,cfg);assert dataclasses.asdict(ds.config)==cfg
    write_new(out/'adapters'/f'{family}.json',dict(family=family,revision='21e6d2a9a581b3e11aafe711abfd37402f8482d5',
        native_source_path=prior['native_source_path'],effective_config=cfg,defaults_except_seed_size=True,
        native_manifest_sha256=file_hash(root/'vendor/reasoning_gym_p02a/source_manifest.json'),
        provenance_reference='reports/p02a/adapter_contracts.md; vendor/reasoning_gym_p02a/source_manifest.json'))
    for ix in range(4):
        entry=ds[ix];question=entry['question'];qh=digest(question)
        latent=digest([family,cfg,ix,entry['metadata']]);nativeid=digest([family,cfg['seed'],ix])
        iid=digest([selection['namespace'],latent,qh])
        if qh in oldq|seen or latent in oldlatent or iid in oldid or nativeid in nativeids:collisions.append(dict(family=family,index=ix))
        seen.add(qh)
        raw=tokenizer.encode(question,add_special_tokens=False)
        gate=dict(input_id=iid,text=question,token_ids=raw,observables=cheap_features(question,raw));validate_gate_input(gate)
        write_new(out/'gate_inputs'/f'{iid}.json',gate)
        row=dict(evidence_kind='development_observation',split='DEVELOPMENT',family=family,input_id=iid,
            latent_hash=latent,question_hash=qh,native_identity_hash=nativeid,entry=entry,entry_hash=digest(entry),
            effective_config=cfg,dataset_index=ix,seed=cfg['seed'],raw_tokens=len(raw),tokenizations={})
        for mode in ('D','R'):
            messages=[dict(role='system',content=SYSTEM),dict(role='user',content=question)]
            rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=mode=='R')
            ids=tokenizer.encode(rendered,add_special_tokens=False)
            assert SYSTEM in rendered and question in rendered
            row[mode+'_tokens']=len(ids)
            row['tokenizations'][mode]=dict(messages=messages,rendered_prompt=rendered,input_ids=ids,
                input_ids_hash=digest(ids),rendered_prompt_hash=digest(rendered),
                opening_in_prompt=rendered.rfind('<think>')>rendered.rfind('</think>'))
        write_new(out/'outcome_inputs'/f'{iid}.json',row)
        inputs.append({k:row[k] for k in ('family','input_id','latent_hash','question_hash','native_identity_hash','dataset_index','seed','raw_tokens','D_tokens','R_tokens')})
write_new(out/'exclusion_manifest.json',dict(evidence_kind='development_observation',historical_question_hashes=sorted(oldq),
    historical_input_ids=sorted(oldid),historical_latent_hashes=sorted(oldlatent),historical_native_identity_hashes=sorted(nativeids),
    historical_request_files=sources,reserved_namespaces=reserved,concrete_final_partition_manifests=[],
    future_requirement='reject all historical and these 24 content/latent/native identities; no final partitions created; P01 native IDs use accepted resource config family/seed and request index',
    new_inputs=inputs,collisions=collisions))
write_new(out/'inputs.json',inputs)
blocked=[r for r in inputs if any(not 1<=r[k]<=2048 for k in ('raw_tokens','D_tokens','R_tokens'))]
assert not collisions and not blocked, 'fixed candidate blocked, no replacement'
old=read_json(root/'artifacts/development/p02b-two-cap/package_base.json')
package=dict(old,checkpoint='P02D',model_revision=MODEL_REVISION,specification_version=VERSION,
    generation_config=dict(old['generation_config'],max_new_tokens=2048))
# Historical source map is provenance, not an override of newly bound P02D source.
package.pop('source_files',None)
write_new(out/'package.json',package)
requests=[]
for draw in range(4):
 for ix in range(4):
  for fi,family in enumerate(ENTRIES):
   row=read_json(out/'outcome_inputs'/f'{inputs[fi*4+ix]["input_id"]}.json')
   for mode in (('D','R') if (ix+draw)%2==0 else ('R','D')):
    key=f'answer_{len(requests):03d}';p,s=identity(package,mode,row['input_id'],draw)
    q=dict(evidence_kind='development_observation',split='DEVELOPMENT',slot_id=key,request_id=key,
       stage='answer',family=family,mode=mode,cap=2048,max_new_tokens=2048,enable_thinking=mode=='R',
       input_id=row['input_id'],draw_index=draw,dataset_config=row['effective_config'],dataset_index=ix,entry_hash=row['entry_hash'],
       package_hash=p,stream_id=s,sampling_seed=int(s[:15],16),effective_generation_config=package['generation_config'],
       model_directory=model['local_directory'],**row['tokenizations'][mode])
    write_new(out/'requests'/f'{key}.json',q)
    requests.append({**{k:q[k] for k in ('slot_id','stage','family','mode','cap','input_id','draw_index','package_hash','stream_id','sampling_seed')},'request_hash':digest(q)})
features=forward_schedule(inputs)
write_new(out/'answer_schedule.json',requests);write_new(out/'feature_schedule.json',features)
write_new(out/'preparation_checks.json',dict(evidence_kind='development_observation',status='PASS',inputs=24,
    answer_slots=len(requests),distinct_streams=len({q['stream_id'] for q in requests}),distinct_seeds=len({q['sampling_seed'] for q in requests}),
    feature_forwards=len(features),actual_feature_input_positions=sum(q['input_positions'] for q in features),
    reserved_output_tokens=192*2048,collisions=collisions,input_lengths={k:[r[k] for r in inputs] for k in ('raw_tokens','D_tokens','R_tokens')},
    native_questions_verbatim=True,model_loads=0,forwards=0,generations=0))
print(json.dumps(read_json(out/'preparation_checks.json')))
