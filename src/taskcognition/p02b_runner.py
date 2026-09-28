"""Exact P02B scope: 48 independent mixed-cap requests, no old-phase reopening."""
import os,sys,time,traceback
from datetime import datetime,timezone
from pathlib import Path
from .artifacts import read_json,write_new
from .contracts import IntegrityError,canonical,digest,file_hash,stream_id
from .p01_ledger import reconcile,append
from .p02_runner import supervise,envelope_check

RUN='artifacts/development/p02b-two-cap'
SYSTEM="""Follow this final-answer format for every task.
On the final answer channel, begin with the literal tag <FINAL> and end with the literal tag </FINAL>.
Between these tags, put only the answer in the format requested by the task. The task's instructions about lists, JSON, numbers, or text apply inside the tags.
Include exactly one pair of FINAL tags. Do not put explanations, headings, Markdown fences, or any other text before or after the pair on the final answer channel.
If a separate thinking channel is used, these restrictions apply to the final answer channel, not to that thinking channel."""

def identity(package,mode,cap,input_id,draw):
    if mode not in ('D','R') or cap not in (1024,2048):raise IntegrityError('P02B mode/cap')
    p=digest(dict(package=package,mode=mode,enable_thinking=mode=='R',max_new_tokens=cap))
    stream=stream_id('P02B-DEVELOPMENT',2026092803,'DEVELOPMENT',input_id,p,draw)
    return p,stream

def finish_reason(stopping_reason,terminal_eos,count,cap):
    if cap not in (1024,2048) or not 0<=count<=cap:raise IntegrityError('output cap integrity')
    return stopping_reason or ('eos' if terminal_eos is not None else 'cap' if count>=cap else 'other')

def require_real_dispatch(root):
    state=read_json(root/'configs/phase_state.json')
    if state.get('active_phase')!='P02B' or state.get('status')!='IN_PROGRESS' or state.get('real_dispatch_enabled') is not True:raise IntegrityError('P02B dispatch disabled')
    run=root/RUN
    if file_hash(run/'run_plan.json')!=state.get('p02b_plan_sha256'):raise IntegrityError('P02B plan changed')
    plan=read_json(run/'run_plan.json')
    if plan['phase']!='P02B' or plan['output_directory']!=RUN or len(plan['requests'])!=48:raise IntegrityError('P02B plan scope')
    if {c:sum(q['cap']==c for q in plan['requests']) for c in (1024,2048)}!={1024:24,2048:24}:raise IntegrityError('mixed cap counts')
    for name,h in plan['source_files'].items():
        if file_hash(root/'src/taskcognition'/name)!=h:raise IntegrityError('source changed')
    for name,h in plan['bound_files'].items():
        if file_hash(root/name)!=h:raise IntegrityError('bound plan file changed')
    return plan

def reserve(run,request,plan):
    rows=reconcile(run);key=request['request_id'];cap=request.get('max_new_tokens')
    if key in rows:raise IntegrityError('no replay; J=0')
    if cap not in (1024,2048):raise IntegrityError('unapproved cap')
    if len(rows)>=48 or sum(r['reserved_output_tokens'] for r in rows.values())+cap>73728:raise IntegrityError('P02B total budget exhausted')
    if sum(r['reserved_output_tokens'] for r in rows.values() if r['reserved_output_tokens']==cap)+cap>24*cap:raise IntegrityError('P02B cap-specific budget exhausted')
    if any(r['state']!='COMPLETE' or not r.get('resource_recorded') for r in rows.values()):raise IntegrityError('unfinished previous attempt')
    expected=plan['requests'][len(rows)]
    if expected['request_id']!=key or expected['request_hash']!=digest(request) or expected['cap']!=cap:raise IntegrityError('not next unchanged planned request')
    if request.get('split')!='DEVELOPMENT' or request.get('evidence_kind')!='development_observation':raise IntegrityError('scope')
    if request['effective_generation_config']['max_new_tokens']!=cap:raise IntegrityError('effective cap mismatch')
    if request['stream_id'] in {r['stream_id'] for r in rows.values()}:raise IntegrityError('stream reuse')
    append(run,'dispatch',key,request_hash=digest(request),stream_id=request['stream_id'],max_new_tokens=cap)

def close_dispatch(root,status,reason):
    path=root/'configs/phase_state.json';state=read_json(path)
    if state.get('active_phase')!='P02B':raise IntegrityError('refuse to change another phase')
    snapshot=root/'configs/state_snapshots/P02B_dispatch_ended.json'
    with snapshot.open('xb') as f:f.write(path.read_bytes())
    event='configs/state_events/010_P02B_dispatch_closed.json'
    write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),event='P02B_dispatch_closed',previous_state_sha256=file_hash(snapshot),status=status,reason=reason,p01_dispatch_enabled=False,p02a_dispatch_enabled=False,real_dispatch_enabled=False,p02_sealed=False))
    state.update(real_dispatch_enabled=False,status=status,latest_event=event)
    path.write_bytes(canonical(state)+b'\n')

def execute(root):
    plan=require_real_dispatch(root);run=root/RUN
    if (run/'execution_start.json').exists():raise IntegrityError('run already invoked; no automatic resume/replay')
    write_new(run/'execution_start.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=file_hash(run/'run_plan.json')))
    start=time.perf_counter();complete=False
    try:
        for item in plan['requests']:
            require_real_dispatch(root)
            spent=sum(r['resource_seconds'] for r in reconcile(run).values())
            size=sum(p.stat().st_size for base in (run,root/'reports/p02b') for p in base.rglob('*') if p.is_file())
            envelope_check(spent,time.perf_counter()-start,size)
            request=read_json(run/'requests'/f'{item["request_id"]}.json');reserve(run,request,plan)
            env=os.environ.copy();env.update(PYTHONPATH=str(root/'src'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONUTF8='1')
            row=supervise(run,request,[sys.executable,'-m','taskcognition.p02b_worker','--root',str(root),'--request',str(run/'requests'/f'{item["request_id"]}.json')],env)
            print(dict(request_id=item['request_id'],cap=item['cap'],seconds=row['resource_seconds'],finish=row['result']['finish_reason']),flush=True)
        complete=True
    except BaseException as exc:
        write_new(run/'supervisor_stop.json',dict(evidence_kind='development_observation',scored=False,error_type=type(exc).__name__,error_message=str(exc),traceback=traceback.format_exc(),automatic_retry=False))
        raise
    finally:
        # Disable first, even if reporting/persistence subsequently fails.
        close_dispatch(root,'IN_PROGRESS' if complete else 'BLOCKED','execution complete; offline reporting only' if complete else 'execution stopped; no replacement')
        write_new(run/'execution_end.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),execution_wall_seconds=time.perf_counter()-start,all_planned_executed=complete))

if __name__=='__main__':execute(Path.cwd())
