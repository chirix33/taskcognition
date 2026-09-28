"""P02A immutable plan guard and sequential supervisor. P01 stays closed."""
import os, subprocess, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path
from .artifacts import read_json,write_new
from .contracts import IntegrityError,digest,file_hash
from .p01_ledger import events,reconcile,append,terminal
from .p01_smoke import record_worker_exit

RUN='artifacts/development/p02a-six-family'

def require_real_dispatch(root):
    state=read_json(root/'configs/phase_state.json')
    if state.get('active_phase')!='P02A' or state.get('status')!='IN_PROGRESS' or state.get('real_dispatch_enabled') is not True:
        raise IntegrityError('P02A dispatch disabled')
    run=root/RUN
    if file_hash(run/'run_plan.json')!=state.get('p02a_plan_sha256'):raise IntegrityError('P02A plan changed')
    plan=read_json(run/'run_plan.json')
    for name,expected in plan['source_files'].items():
        if file_hash(root/'src/taskcognition'/name)!=expected:raise IntegrityError('planned source changed')
    for name,expected in plan['bound_files'].items():
        if file_hash(root/name)!=expected:raise IntegrityError('planned evidence changed')
    return plan

def reserve(run,request,plan):
    rows=reconcile(run)
    key=request['request_id']
    if key in rows:raise IntegrityError('no replay; J=0')
    index=len(rows)
    if index>=24 or sum(r['reserved_output_tokens'] for r in rows.values())+1024>24576:raise IntegrityError('P02A budget exhausted')
    expected=plan['requests'][index]
    if expected['request_id']!=key or expected['request_hash']!=digest(request):raise IntegrityError('request not next in immutable plan')
    if request.get('split')!='DEVELOPMENT' or request.get('evidence_kind')!='development_observation' or request.get('max_new_tokens')!=1024:raise IntegrityError('scope/cap')
    if request['stream_id'] in {r['stream_id'] for r in rows.values()}:raise IntegrityError('stream reuse')
    if any(r['state']!='COMPLETE' or not r.get('resource_recorded') for r in rows.values()):raise IntegrityError('unfinished previous attempt')
    append(run,'dispatch',key,request_hash=digest(request),stream_id=request['stream_id'],max_new_tokens=1024)

def envelope_check(spent,wall,evidence_bytes):
    # Reserve 300 s: up to 150 s startup/load, 120 s generation, 30 s cleanup.
    if spent+300>5400 or wall+300>7200 or evidence_bytes+16*1024**2>512*1024**2:raise IntegrityError('insufficient remaining envelope')

def supervise(run,request,command,env,monitor=None):
    """On any parent failure kill AND wait before propagating; incident is unscored."""
    key=request['request_id'];started=time.perf_counter();process=None
    cancel_time=None;admitted_seen=None;forced=False;error=None
    logs=run/'worker_logs';logs.mkdir(exist_ok=True)
    try:
        with (logs/f'{key}.stdout.txt').open('xb') as out,(logs/f'{key}.stderr.txt').open('xb') as err:
            process=subprocess.Popen(command,stdout=out,stderr=err,env=env,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            while process.poll() is None:
                if monitor is not None:monitor(process)
                current=[e for e in events(run) if e['request_id']==key]
                if admitted_seen is None and any(e['event']=='admitted' for e in current):admitted_seen=time.perf_counter()
                now=time.perf_counter()
                if admitted_seen is not None and now-admitted_seen>=120 and cancel_time is None:
                    cancel_time=now
                    write_new(run/'cancel'/f'{key}.json',dict(evidence_kind='development_observation',reason='timeout',timestamp_utc=datetime.now(timezone.utc).isoformat()))
                if (admitted_seen is not None and now-admitted_seen>=130) or now-started>=270:
                    forced=True;cancel_time=cancel_time or now;process.kill();break
                time.sleep(.02)
            process.wait(timeout=30)
    except BaseException as exc:
        error=exc
        raise
    finally:
        cleanup_start=time.perf_counter()
        if process is not None and process.poll() is None:process.kill()
        if process is not None:process.wait(timeout=30)
        elapsed=time.perf_counter()-started
        if error is not None:
            incident=dict(evidence_kind='development_observation',split='DEVELOPMENT',request_id=key,scored=False,status='supervisor_incident',error_type=type(error).__name__,error_message=str(error),seconds=elapsed,child_pid=None if process is None else process.pid,child_exit=None if process is None else process.returncode,child_waited=process is not None,cleanup_seconds=time.perf_counter()-cleanup_start,automatic_retry=False)
            # Independent diagnostic survives a broken monitoring ledger; never a result.
            write_new(run/'incidents'/f'{key}_supervisor.json',incident)
            append(run,'resource',key,seconds=elapsed,process_exit=incident['child_exit'],supervisor_incident=True,conservative_gpu_residency=True)
    return record_worker_exit(run,request,elapsed=elapsed,exit_code=process.returncode,forced=forced,cancellation_seconds=None if cancel_time is None else time.perf_counter()-cancel_time)

def execute(root):
    plan=require_real_dispatch(root);run=root/RUN
    startfile=run/'execution_start.json'
    if startfile.exists():raise IntegrityError('single execution invocation; investigate interrupted run without automatic resume')
    write_new(startfile,dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=file_hash(run/'run_plan.json')))
    start=time.perf_counter()
    try:
        for item in plan['requests']:
            require_real_dispatch(root)
            rows=reconcile(run)
            spent=sum(r['resource_seconds'] for r in rows.values())
            size=sum(p.stat().st_size for base in (run,root/'reports/p02a') for p in base.rglob('*') if p.is_file())
            envelope_check(spent,time.perf_counter()-start,size)
            request=read_json(run/'requests'/f'{item["request_id"]}.json')
            reserve(run,request,plan)
            env=os.environ.copy();env.update(PYTHONPATH=str(root/'src'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONUTF8='1')
            result=supervise(run,request,[sys.executable,'-m','taskcognition.p02_worker','--root',str(root),'--request',str(run/'requests'/f'{item["request_id"]}.json')],env)
            print(dict(request_id=item['request_id'],seconds=result['resource_seconds'],finish=result['result']['finish_reason']),flush=True)
    finally:
        write_new(run/'execution_end.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),execution_wall_seconds=time.perf_counter()-start))

if __name__=='__main__':execute(Path.cwd())
