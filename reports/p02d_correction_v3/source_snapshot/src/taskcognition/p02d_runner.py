"""Authorized-only sequential supervisor; all preparation/tests stay offline."""
import os
import math
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from .artifacts import read_json
from .p02d_publication import write_new, read_optional, replace_state
from .contracts import IntegrityError, canonical, digest, file_hash, number, integer
from .p02d_plan import RUN, PLAN_DIR, require_authorization
from .p02d_ledger import append, scan, recover, dispatch, check_envelope, BudgetStop
from .p02d_features import gate_vector, validate_gate_input
from .p02b_reporting import primary_record

def evidence_size(root):
    return sum(p.stat().st_size for base in (root/RUN,root/'reports/p02d_execution') for p in base.rglob('*') if p.is_file())

def validate_result(root, plan, slot, result):
    if result.get('slot_id')!=slot['slot_id'] or result.get('request_hash')!=slot['request_hash']:
        raise IntegrityError('worker result identity')
    if result.get('model_error') is not None or result.get('scored') is False:raise IntegrityError('worker incident is not a result')
    if slot['stage']=='feature':
        if result.get('status')!='OK' or result.get('dtype')!='float32':raise IntegrityError('invalid feature result')
        row=read_json(root/PLAN_DIR/'gate_inputs'/f'{slot["input_id"]}.json')
        expected=gate_vector(row,result['gate']['embedding'],plan['feature_specification']['hidden_width'])
        if result['gate']!=expected:raise IntegrityError('feature boundary')
        if result['input_positions']!=slot['input_positions']:raise IntegrityError('feature positions')
        number(result['forward_seconds']);number(result['cpu_feature_seconds'])
    else:
        request=read_json(root/PLAN_DIR/'requests'/f'{slot["slot_id"]}.json')
        if digest(request)!=slot['request_hash']:raise IntegrityError('request changed')
        primary=primary_record(request,{'result':result})
        number(primary['native_score'],0,1)
        if type(primary['perfect_correct']) is not bool or type(primary['strict_valid_final']) is not bool:raise IntegrityError('boolean scoring flags required')
        if primary['output_tokens'] is not None:integer(primary['output_tokens'])
        if primary['perfect_correct']!=(primary['native_score']==1):raise IntegrityError('score/perfect integrity')
    return result

class ProcessWorker:
    """File IPC with one child, bounded waits and no mutable result publication."""
    def __init__(self,root,session_id,stage,plan_hash):
        self.directory=root/RUN/'workers'/session_id
        self.directory.mkdir(parents=True,exist_ok=False)
        self.out=(self.directory/'stdout.txt').open('xb');self.err=(self.directory/'stderr.txt').open('xb')
        env=os.environ.copy();env.update(PYTHONPATH=str(root/'src'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONUTF8='1')
        self.process=None
        try:
            self.process=subprocess.Popen([sys.executable,'-m','taskcognition.p02d_worker','--root',str(root),
                '--session',session_id,'--stage',stage,'--plan-hash',plan_hash],stdout=self.out,stderr=self.err,env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        except BaseException:
            self.out.close();self.err.close();raise
    def poll(self):return self.process.poll()
    def ready(self):
        p=self.directory/'ready.json'
        return read_optional(p)
    def incident(self):return (self.directory/'incident.json').exists()
    def operational_stop(self):
        value=read_optional(self.directory/'operational_stop.json')
        if value is not None:
            if value.get('scored') is not False or not isinstance(value.get('error'),str):raise IntegrityError('invalid worker stop')
        return value
    def send(self,slot):write_new(self.directory/'commands'/f'{slot["slot_id"]}.json',slot)
    def result(self,slot):
        p=self.directory/'results'/f'{slot["slot_id"]}.json'
        return read_optional(p)
    def cancel(self,slot):write_new(self.directory/'cancel'/f'{slot["slot_id"]}.json',{'reason':'timeout'})
    def finish(self):write_new(self.directory/'finish.json',{'stop':True})
    def kill(self):
        if self.poll() is None:self.process.kill()
    def wait(self,timeout):return self.process.wait(timeout=timeout)
    def close(self):self.out.close();self.err.close()

def supervise_session(root,plan,slots,plan_hash,execution_start,*,worker_factory=ProcessWorker,
                      clock=time.perf_counter,sleep=time.sleep,monitor=None,size_fn=evidence_size):
    """Persist costs even when load, callbacks, monitor, evidence, or cleanup fail.

    Fake-worker tests exercise this same supervisor. No factory is reached before
    the public execute() authorization boundary in real execution.
    """
    run=root/RUN;stage=slots[0]['stage'];sid='features' if stage=='feature' else slots[0]['slot_id']
    state=recover(run);L=plan['limits'];started=clock();worker=None;error=None;ready=None
    check_envelope(plan,state,stage,started-execution_start,size_fn(root),loading=True)
    append(run,'session_start',session_id=sid,stage=stage)
    last_heartbeat=started;safe=False;exit_code=None;cleanup_start=None
    def tick():
        nonlocal last_heartbeat
        now=clock()
        if monitor is not None:monitor(worker)
        if worker.incident():raise IntegrityError('worker software/evidence incident')
        stop=getattr(worker,'operational_stop',lambda:None)()
        if stop is not None:raise BudgetStop('worker deadline: '+stop['error'])
        if now-last_heartbeat>=1:
            append(run,'heartbeat',session_id=sid,seconds=now-started);last_heartbeat=now
        if now-execution_start>=L['wall_seconds']-L['cleanup_seconds']:raise BudgetStop('execution wall termination')
        if 2*size_fn(root)>=L['evidence_bytes']-L['evidence_reservation_bytes']:raise BudgetStop('evidence termination')
        elapsed=now-started
        prior=sum(s['seconds'] for s in state['sessions'].values() if s['ended'])
        if prior+elapsed>=L['residency_seconds']-L['cleanup_seconds']:raise BudgetStop('residency termination')
        if stage=='feature' and elapsed>=L['feature_residency_seconds']-L['cleanup_seconds']:raise BudgetStop('feature residency termination')
    try:
        # First slot is durably consumed even if startup/load has an unknown outcome.
        dispatch(run,plan,slots[0],sid)
        worker=worker_factory(root,sid,stage,plan_hash)
        while (ready:=worker.ready()) is None:
            tick()
            if worker.poll() is not None:raise IntegrityError('worker exited before readiness')
            if clock()-started>=L['load_deadline_seconds']:raise IntegrityError('loader deadline; unscored incident')
            sleep(.02)
        number(ready['load_seconds'])
        for ix,slot in enumerate(slots):
            tick()
            if ix:
                current=scan(run)
                check_envelope(plan,current,stage,clock()-execution_start,size_fn(root),active_seconds=clock()-started,feature_wall=clock()-started)
                dispatch(run,plan,slot,sid)
            append(run,'admitted',session_id=sid,slot_id=slot['slot_id'])
            worker.send(slot);forward_start=clock();cancelled=False;forced=False
            while (result:=worker.result(slot)) is None:
                tick()
                if worker.poll() is not None:raise IntegrityError('worker exited without result')
                elapsed=clock()-forward_start
                if elapsed>=120 and not cancelled:
                    if stage=='feature':raise BudgetStop('feature forward timeout; no answer admission')
                    worker.cancel(slot);cancelled=True
                if elapsed>=130 and stage=='answer':
                    # Known deadline, no reported software incident: explicit retained failure.
                    worker.kill();exit_code=worker.wait(L['cleanup_seconds']);forced=True
                    result=dict(evidence_kind='development_observation',split='DEVELOPMENT',slot_id=slot['slot_id'],
                        request_id=slot['slot_id'],request_hash=slot['request_hash'],finish_reason='supervisor_forced_termination',
                        forced_termination=True,native_score=0,valid_retainable_output=False,
                        output_tokens_unknown=True,reason='known generation deadline followed by finite cancellation grace')
                    break
                sleep(.02)
            validate_result(root,plan,slot,result)
            path=run/'results'/f'{slot["slot_id"]}.json';write_new(path,result)
            append(run,'result',session_id=sid,slot_id=slot['slot_id'],path=path.relative_to(run).as_posix(),sha256=file_hash(path))
            if forced:break
        if worker.poll() is None:worker.finish()
        exit_code=worker.wait(L['cleanup_seconds'])
        if exit_code!=0 and not forced:raise IntegrityError('worker nonzero exit after result')
    except BaseException as exc:
        error=exc
        raise
    finally:
        cleanup_start=clock();cleanup_error=None
        try:
            if worker is not None:
                if worker.poll() is None:worker.kill()
                exit_code=worker.wait(L['cleanup_seconds']);safe=worker.poll() is not None
                worker.close()
            else:safe=True  # factory failed before returning child; production constructor has no post-spawn operations
        except BaseException as exc:
            cleanup_error=exc;safe=False
            if worker is not None:
                try:worker.close()
                except BaseException:pass  # original cleanup failure remains dominant
        finally:
            elapsed=clock()-started;cleanup=clock()-cleanup_start
            # Check evidence again after stopping the child: a budget trigger must
            # never conceal an incident/result committed during cancellation.
            evidence_error=None
            try:
                scan(run)
                if worker is not None:
                    if worker.incident():raise IntegrityError('worker incident during cleanup')
                    if isinstance(worker,ProcessWorker):
                        worker.operational_stop()  # malformed committed stop is an incident
                        allowed={s['slot_id']:s for s in slots}
                        for p in (worker.directory/'results').glob('*.json'):
                            if p.stem not in allowed:raise IntegrityError('unknown worker result')
                            validate_result(root,plan,allowed[p.stem],read_json(p))
            except BaseException as exc:evidence_error=exc
            operational=isinstance(error,BudgetStop) and safe and cleanup_error is None and evidence_error is None
            classification='OPERATIONAL_STOP' if operational else 'INTEGRITY_INCIDENT' if error or cleanup_error or evidence_error else 'COMPLETE'
            value=ready.get('load_seconds') if isinstance(ready,dict) else None
            recorded_load=value if type(value) in (int,float) and math.isfinite(value) and value>=0 else None
            record=dict(evidence_kind='development_observation',session_id=sid,stage=stage,seconds=elapsed,
                cleanup_seconds=cleanup,safe_stopped=safe,exit_code=exit_code,load_seconds=recorded_load,
                clock='perf_counter from before process creation through final wait; conservative residency, not GPU kernel time',
                error=None if error is None else repr(error),cleanup_error=None if cleanup_error is None else repr(cleanup_error),
                evidence_error=None if evidence_error is None else repr(evidence_error),classification=classification,scored=False)
            # Independent cost record is written first, even if the main ledger is corrupt.
            resource=run/'session_resources'/f'{sid}.json';write_new(resource,record)
            # Independent classification survives a corrupt/unappendable ledger.
            terminal=run/('operational_stops' if operational else 'incidents')/f'{sid}.json'
            if classification!='COMPLETE':write_new(terminal,record)
            append(run,'session_end',session_id=sid,seconds=elapsed,cleanup_seconds=cleanup,safe_stopped=safe,exit_code=exit_code,
                resource_path=resource.relative_to(run).as_posix(),resource_sha256=file_hash(resource))
            if operational:
                append(run,'operational_stop',session_id=sid,path=terminal.relative_to(run).as_posix(),sha256=file_hash(terminal))
            elif classification=='INTEGRITY_INCIDENT':
                append(run,'incident',session_id=sid,error=record['error'],cleanup_error=record['cleanup_error'],scored=False)
            if cleanup_error is not None:raise IntegrityError('cleanup did not establish stopped state') from cleanup_error
            if evidence_error is not None:raise IntegrityError('cleanup evidence integrity failure') from evidence_error
    return scan(run)

def execute(root,expected_hash,*,worker_factory=ProcessWorker):
    root=root.resolve();planpath=root/PLAN_DIR/'run_plan.json'
    run=root/RUN
    started=time.perf_counter();complete=False;began=False
    try:
        plan=require_authorization(root,planpath,expected_hash)
        recover(run)
        if (run/'execution_start.json').exists():raise IntegrityError('single invocation; no automatic restart/replay')
        write_new(run/'execution_start.json',dict(evidence_kind='development_observation',timestamp_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=expected_hash))
        began=True
        feature_started=time.perf_counter()
        try:
            supervise_session(root,plan,plan['feature_schedule'],expected_hash,started,worker_factory=worker_factory)
        finally:
            feature_wall=time.perf_counter()-feature_started
            write_new(run/'feature_stage_wall.json',dict(evidence_kind='development_observation',seconds=feature_wall,
                includes_supervisor_recording=True,ceiling_seconds=plan['limits']['feature_wall_seconds'],overshoot_seconds=max(0,feature_wall-plan['limits']['feature_wall_seconds'])))
        if feature_wall>plan['limits']['feature_wall_seconds']:raise BudgetStop('feature stage wall exceeded; answers blocked')
        for slot in plan['requests']:
            require_authorization(root,planpath,expected_hash)
            supervise_session(root,plan,[slot],expected_hash,started,worker_factory=worker_factory)
        complete=True
    except BaseException as exc:
        if began:
            write_new(run/'supervisor_stop.json',dict(evidence_kind='development_observation',scored=False,
                error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc(),resource_stop=isinstance(exc,BudgetStop),
                classification='OPERATIONAL_STOP' if isinstance(exc,BudgetStop) else 'INTEGRITY_INCIDENT'))
        raise
    finally:
        # Close dispatch before reporting, including on evidence/cleanup exceptions.
        state=read_json(root/'configs/phase_state.json')
        if state.get('active_phase')=='P02D' and (state.get('real_dispatch_enabled') is True or began):
            state.update(real_dispatch_enabled=False,status='EXECUTION_RECORDED' if complete else 'BLOCKED')
            replace_state(root/'configs/phase_state.json',state)
        if began:
            write_new(run/'execution_end.json',dict(evidence_kind='development_observation',all_planned_executed=complete,
                wall_seconds=time.perf_counter()-started,real_dispatch_enabled=False))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--plan-hash',required=True)
    a=p.parse_args();execute(a.root,a.plan_hash)
