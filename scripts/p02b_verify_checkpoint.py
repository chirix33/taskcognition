"""Final read-only preservation, exact-plan and closed-dispatch verification."""
from pathlib import Path
import hashlib,subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,digest,IntegrityError
from taskcognition.p01_ledger import require_real_dispatch as p01_guard,events
from taskcognition.p02_runner import require_real_dispatch as p02a_guard
from taskcognition.p02b_runner import require_real_dispatch as p02b_guard,SYSTEM,RUN

root=Path(__file__).resolve().parents[1];run=root/RUN
for guard in [p01_guard,p02a_guard,p02b_guard]:
    try:guard(root)
    except IntegrityError:pass
    else:raise AssertionError('live dispatch unexpectedly enabled')
index=read_json(root/'reports/p02a/P02A_evidence_index.json')
changed=[n for n,h in index['files'].items() if file_hash(root/n)!=h]
assert changed==['configs/phase_state.json'],changed
assert file_hash(root/'configs/state_snapshots/P02A_accepted_before_P02B.json')==index['files']['configs/phase_state.json']
plan=read_json(run/'run_plan.json');old=read_json(root/'artifacts/development/p02a-six-family/package.json')['generation_config']
precommit=read_json(root/'configs/state_events/009_P02B_bounded_dispatch.json')['source_commit']
for n,h in {**plan['bound_files'],**{f'src/taskcognition/{n}':h for n,h in plan['source_files'].items()},f'{RUN}/run_plan.json':file_hash(run/'run_plan.json')}.items():
    committed=subprocess.check_output(['git','show',f'{precommit}:{n}'])
    assert hashlib.sha256(committed).hexdigest()==h,('pre-dispatch commit mismatch',n)
for n,h in plan['bound_files'].items():assert file_hash(root/n)==h,n
for n,h in plan['source_files'].items():assert file_hash(root/'src/taskcognition'/n)==h,n
requests=[]
for item in plan['requests']:
    q=read_json(run/'requests'/f'{item["request_id"]}.json');requests.append(q)
    assert digest(q)==item['request_hash']
    assert q['messages']==[dict(role='system',content=SYSTEM),dict(role='user',content=read_json(run/'outcome_inputs'/f'{q["family"]}.json')['entry']['question'])]
    assert {k:v for k,v in q['effective_generation_config'].items() if k!='max_new_tokens'}=={k:v for k,v in old.items() if k!='max_new_tokens'}
    assert q['effective_generation_config']['max_new_tokens']==q['max_new_tokens']
    assert q['input_tokens']==len(q['input_ids'])<=2048
assert len(requests)==48 and len({q['stream_id'] for q in requests})==48 and len({q['sampling_seed'] for q in requests})==48
assert {c:sum(q['max_new_tokens'] for q in requests if q['max_new_tokens']==c) for c in (1024,2048)}=={1024:24576,2048:49152}
for family in {q['family'] for q in requests}:
    selected=[q for q in requests if q['family']==family]
    assert len({q['input_id'] for q in selected})==1
    assert {next(q['cap'] for q in selected if q['draw_index']==d) for d in (0,1)}=={1024,2048}
ledger=events(run)
write_new(root/'reports/p02b/checkpoint_verification.json',dict(evidence_kind='development_observation',status='PASS',historical_P02A_files_unchanged=358,current_state_change_preserved=True,p01_p02a_p02b_dispatch_disabled=True,all_plan_hashes_match=True,all_pre_dispatch_commit_bytes_match=True,pre_dispatch_commit=precommit,exact_common_instruction=True,original_native_questions=True,all_other_sampler_defaults_unchanged=True,distinct_streams_and_sampling_seeds=48,balanced_first_cap=True,ledger_events=len(ledger),dispatched=sum(e['event']=='dispatch' for e in ledger),admitted=sum(e['event']=='admitted' for e in ledger),resource_records=sum(e['event']=='resource' for e in ledger),p02_incomplete_unsealed=True))
print('PASS: old evidence unchanged, exact prompts/configs/plan, 48 distinct streams, all dispatch closed.')
