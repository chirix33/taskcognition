"""Prospective development version and independent authorization boundary."""
import importlib.metadata
from pathlib import Path
from .artifacts import read_json, child_path
from .contracts import IntegrityError, digest, file_hash, stream_id
from .p02b_runner import SYSTEM
from .p02_native import ENTRIES
from .p02d_features import FEATURE_SPEC, forward_schedule, validate_gate_input

VERSION='TaskCognition-CR01-2026-10-05-v1'
RUN='artifacts/development/p02d-cr01-tranche'
PLAN_DIR='artifacts/development/p02d-cr01-plan-v4'
MODEL_REVISION='b968826d9c46dd6066d109eabc6255188de91218'
ROOT_SEED=930261005
LIMITS=dict(answer_slots=192,output_tokens=393216,feature_forwards=50,feature_input_positions=102400,
    residency_seconds=14400,wall_seconds=18000,evidence_bytes=536870912,
    feature_residency_seconds=900,feature_wall_seconds=1200,
    generation_deadline_seconds=120,forward_deadline_seconds=120,load_deadline_seconds=150,
    cooperative_grace_seconds=10,cleanup_seconds=30,answer_reservation_seconds=300,
    feature_load_reservation_seconds=300,feature_forward_reservation_seconds=150,
    evidence_reservation_bytes=16777216,J=0,concurrency=1)

def identity(package,mode,input_id,draw):
    if mode not in ('D','R'):raise IntegrityError('mode')
    p=digest(dict(package=package,mode=mode,enable_thinking=mode=='R',max_new_tokens=2048))
    return p,stream_id(VERSION+'/'+RUN,ROOT_SEED,'DEVELOPMENT',input_id,p,draw)

def validate_plan(plan):
    if (plan.get('phase'),plan.get('specification_version'),plan.get('split'),plan.get('evidence_kind'))!=('P02D',VERSION,'DEVELOPMENT','development_observation'):
        raise IntegrityError('prospective CR01 development scope')
    if plan.get('scientific_freeze') is not False or plan.get('authorization')!='PENDING_SEPARATE_RECORD':raise IntegrityError('not a final manifest/authorization')
    if plan.get('completion_policy')!='descriptive':raise IntegrityError('CR01 completion is descriptive')
    if plan.get('output_directory')!=RUN or plan.get('limits')!=LIMITS or plan.get('caps')!={'D':2048,'R':2048}:
        raise IntegrityError('exact scope/caps/limits')
    if plan.get('feature_specification')!=FEATURE_SPEC:raise IntegrityError('feature specification')
    package=plan['package']
    if package['wrapper']!=SYSTEM or package['model_revision']!=MODEL_REVISION:raise IntegrityError('answer package changed')
    if package.get('model_id')!='Qwen/Qwen3-8B' or package.get('precision')!='BF16' or package.get('attention')!='sdpa forced MATH':raise IntegrityError('checkpoint/backend/precision')
    sampler=package['generation_config']
    if any(sampler.get(k)!=v for k,v in dict(max_new_tokens=2048,do_sample=True,temperature=.6,top_p=.95,top_k=20,min_p=0).items()):raise IntegrityError('matched sampler')
    inputs=plan['inputs']
    if len(inputs)!=24 or [r['family'] for r in inputs]!=[f for f in ENTRIES for _ in range(4)]:raise IntegrityError('input population')
    for fi,family in enumerate(ENTRIES):
        group=inputs[fi*4:fi*4+4]
        if [r['dataset_index'] for r in group]!=list(range(4)):raise IntegrityError('input indices')
        for r in group:
            if r['seed']!=ROOT_SEED+10000*fi or any(not 1<=r[k]<=2048 for k in ('raw_tokens','D_tokens','R_tokens')):raise IntegrityError('input selection/length')
    if len({r['input_id'] for r in inputs})!=24 or len({r['question_hash'] for r in inputs})!=24:raise IntegrityError('duplicate input')
    if plan['feature_schedule']!=forward_schedule(inputs):raise IntegrityError('forward schedule')
    requests=plan['requests'];expected=[]
    # Draw outer, native index next, family inner: each round covers all six families.
    for draw in range(4):
        for ix in range(4):
            for fi in range(6):
                row=inputs[fi*4+ix]
                for mode in (('D','R') if (ix+draw)%2==0 else ('R','D')):
                    expected.append((row['input_id'],mode,draw))
    if [(q['input_id'],q['mode'],q['draw_index']) for q in requests]!=expected:raise IntegrityError('answer order/count')
    for ix,q in enumerate(requests):
        if q.get('stage')!='answer' or q['slot_id']!=f'answer_{ix:03d}':raise IntegrityError('answer slot scope')
        p,s=identity(package,q['mode'],q['input_id'],q['draw_index'])
        if (q['cap'],q['package_hash'],q['stream_id'],q['sampling_seed'])!=(2048,p,s,int(s[:15],16)):raise IntegrityError('package/cap/stream')
    for key in ('slot_id','stream_id','sampling_seed'):
        if len({q[key] for q in requests})!=192:raise IntegrityError('duplicate '+key)
    return plan

def verify_plan(root, plan_path, expected_hash):
    if file_hash(plan_path)!=expected_hash:raise IntegrityError('reviewed plan hash mismatch')
    plan=validate_plan(read_json(plan_path))
    if plan.get('plan_version')!='P02D-offline-v4':raise IntegrityError('superseded prospective plan version')
    prior=read_json(root/'artifacts/development/p02b-two-cap/package_base.json')['generation_config']
    if plan['package']['generation_config']!=dict(prior,max_new_tokens=2048):raise IntegrityError('effective defaults changed')
    for name,sha in plan['bound_files'].items():
        if file_hash(child_path(root,name))!=sha:raise IntegrityError('bound source/input/config changed: '+name)
    current={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    if current!=plan['environment']['distributions']:raise IntegrityError('runtime distribution mismatch')
    for q in plan['requests']:
        request=read_json(root/PLAN_DIR/'requests'/f'{q["slot_id"]}.json')
        if digest(request)!=q['request_hash'] or request['effective_generation_config']!=plan['package']['generation_config']:
            raise IntegrityError('request/sampler binding')
        if request['split']!='DEVELOPMENT' or request['evidence_kind']!='development_observation':raise IntegrityError('request development scope')
        if request['max_new_tokens']!=2048 or request['enable_thinking']!=(q['mode']=='R'):raise IntegrityError('request cap/native mode')
        if any(request[k]!=q[k] for k in ('slot_id','input_id','mode','cap','package_hash','stream_id','sampling_seed','draw_index')):raise IntegrityError('schedule/request identity')
    for item in plan['inputs']:
        gate=validate_gate_input(read_json(root/PLAN_DIR/'gate_inputs'/f'{item["input_id"]}.json'))
        if gate['input_id']!=item['input_id'] or len(gate['token_ids'])!=item['raw_tokens'] or digest(gate['text'])!=item['question_hash']:raise IntegrityError('gate input binding')
    if Path(__file__).resolve()!=root.resolve()/'src/taskcognition/p02d_plan.py':raise IntegrityError('wrong source import')
    return plan

def require_authorization(root,plan_path,expected_hash):
    """Called by supervisor AND child, before any model loader imports or work."""
    state=read_json(root/'configs/phase_state.json')
    if state.get('active_phase')!='P02D' or state.get('status')!='EXECUTION_AUTHORIZED' or state.get('real_dispatch_enabled') is not True:
        raise IntegrityError('P02D live execution pending separate authorization')
    auth_path=root/'configs/p02d_execution_authorization.json'
    if not auth_path.is_file():raise IntegrityError('missing authorization record')
    if file_hash(auth_path)!=state.get('p02d_authorization_sha256'):raise IntegrityError('authorization state binding')
    auth=read_json(auth_path)
    if auth.get('plan_sha256')!=expected_hash or state.get('p02d_plan_sha256')!=expected_hash or auth.get('authorized') is not True:
        raise IntegrityError('authorization plan binding')
    if not auth.get('user_message_reference') or auth.get('phase')!='P02D' or auth.get('limits')!=LIMITS:
        raise IntegrityError('authorization scope/reference')
    return verify_plan(root,plan_path,expected_hash)
