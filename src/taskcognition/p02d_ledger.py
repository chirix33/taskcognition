"""Single-writer durable, hash-linked research ledger for both P02D stages.

Session residency is charged once, not summed again from nested forward timings.
An unfinished session has a measured lower bound and unknown remaining cost.
It blocks recovery/admission until investigated; there is no automatic replay.
"""
import math
from datetime import datetime, timezone
from .artifacts import read_json, child_path
from .p02d_publication import write_new
from .contracts import IntegrityError, file_hash, number

def scan(run, tolerant=False):
    sessions={};slots={};events=[];incidents=[];stops=[];previous=None
    for ix,path in enumerate(sorted((run/'ledger').glob('*.json'))):
        try:
            e=read_json(path)
            if path.name!=f'{ix:06d}.json' or e['previous_sha256']!=previous:raise IntegrityError('ledger sequence/hash')
            previous=file_hash(path);kind=e['event'];sid=e.get('session_id')
            if kind=='session_start':
                if sid in sessions or any(not s.get('ended') for s in sessions.values()):raise IntegrityError('session replay/concurrency')
                sessions[sid]=dict(stage=e['stage'],ended=False,seconds=None,lower_bound_seconds=0,safe_stopped=False)
            elif kind=='heartbeat':
                s=sessions[sid];number(e['seconds'])
                if s['ended'] or e['seconds']<s['lower_bound_seconds']:raise IntegrityError('heartbeat order')
                s['lower_bound_seconds']=e['seconds']
            elif kind=='dispatch':
                key=e['slot_id'];s=sessions[sid]
                if key in slots or s['ended']:raise IntegrityError('slot replay')
                slots[key]=dict(session_id=sid,stage=s['stage'],state='UNKNOWN_ADMISSION',result=None,
                    output_reservation=e['output_reservation'],input_positions=e['input_positions'],request_hash=e['request_hash'])
            elif kind=='admitted':
                slot=slots[e['slot_id']]
                if slot['state']!='UNKNOWN_ADMISSION':raise IntegrityError('duplicate admission')
                slot['state']='ADMITTED'
            elif kind=='result':
                slot=slots[e['slot_id']]
                if slot['state']!='ADMITTED':raise IntegrityError('terminal order')
                p=child_path(run,e['path'])
                if file_hash(p)!=e['sha256']:raise IntegrityError('result missing/corrupt')
                data=read_json(p)
                if data['slot_id']!=e['slot_id'] or data['request_hash']!=slot['request_hash']:raise IntegrityError('result binding')
                slot.update(state='COMPLETE',result=data)
            elif kind=='session_end':
                s=sessions[sid];number(e['seconds']);number(e['cleanup_seconds'])
                if s['ended'] or e['seconds']<s['lower_bound_seconds']:raise IntegrityError('cost duplicate/under-report')
                s.update(ended=True,seconds=e['seconds'],safe_stopped=e['safe_stopped'],cleanup_seconds=e['cleanup_seconds'],exit_code=e['exit_code'])
                if 'resource_path' in e:
                    resource=child_path(run,e['resource_path'])
                    if file_hash(resource)!=e['resource_sha256']:raise IntegrityError('resource missing/corrupt')
                    r=read_json(resource)
                    if any(r[k]!=e[k] for k in ('session_id','seconds','cleanup_seconds','safe_stopped','exit_code')):raise IntegrityError('resource identity/cost mismatch')
            elif kind=='operational_stop':
                s=sessions[sid]
                if not s['ended'] or not s['safe_stopped']:raise IntegrityError('unsafe operational stop')
                p=child_path(run,e['path'])
                if file_hash(p)!=e['sha256']:raise IntegrityError('stop missing/corrupt')
                r=read_json(p)
                if r['session_id']!=sid or r['classification']!='OPERATIONAL_STOP':raise IntegrityError('stop identity/classification')
                stops.append(e)
                for slot in slots.values():
                    if slot['session_id']==sid and slot['state']!='COMPLETE':
                        slot.update(state='STOPPED_UNSCORED',stop_reason=r['error'])
            elif kind=='incident':incidents.append(e)
            else:raise IntegrityError('unknown ledger event')
            events.append(e)
        except Exception as exc:
            if not tolerant:raise IntegrityError('ledger integrity: '+str(exc)) from exc
            incidents.append(dict(event='ledger_integrity_incident',file=path.name,error=str(exc)))
            break
    # Independent supervisor diagnostic survives broken ledger publication.
    for p in (run/'incidents').glob('*.json'):
        incidents.append(dict(event='incident_artifact',path=p.relative_to(run).as_posix(),sha256=file_hash(p)))
    return dict(sessions=sessions,slots=slots,events=events,incidents=incidents,operational_stops=stops,
        operational_stop_artifacts=[p.relative_to(run).as_posix() for p in (run/'operational_stops').glob('*.json')],
        measured_residency_seconds=sum(s['seconds'] if s['ended'] else s['lower_bound_seconds'] for s in sessions.values()),
        unknown_residency=any(not s['ended'] or not s['safe_stopped'] for s in sessions.values()))

def append(run,event,**fields):
    # Validate previous evidence before extending; atomic no-clobber publication.
    state=scan(run);paths=sorted((run/'ledger').glob('*.json'))
    sid=fields.get('session_id')
    if event=='session_start' and (sid in state['sessions'] or any(not s['ended'] for s in state['sessions'].values())):
        raise IntegrityError('session already consumed or active')
    if event=='session_end' and (sid not in state['sessions'] or state['sessions'][sid]['ended']):
        raise IntegrityError('session cost already charged or unknown')
    if event=='dispatch' and fields['slot_id'] in state['slots']:raise IntegrityError('slot already consumed')
    if event=='admitted' and state['slots'][fields['slot_id']]['state']!='UNKNOWN_ADMISSION':raise IntegrityError('already admitted')
    if event=='result' and state['slots'][fields['slot_id']]['state']!='ADMITTED':raise IntegrityError('already terminal or not admitted')
    record=dict(evidence_kind='development_observation',event=event,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),previous_sha256=file_hash(paths[-1]) if paths else None,**fields)
    write_new(run/'ledger'/f'{len(paths):06d}.json',record)

def recover(run):
    state=scan(run)
    if state['incidents'] or state['operational_stop_artifacts'] or state['unknown_residency'] or any(r['state']!='COMPLETE' for r in state['slots'].values()):
        raise IntegrityError('unresolved interrupted/unknown work; no automatic replay or recharge')
    return state

class BudgetStop(IntegrityError):
    """Operational envelope exhausted; preserve partial evidence, no replacements."""

def check_envelope(plan,state,stage,wall,evidence_bytes,active_seconds=0,feature_wall=0,loading=False):
    L=plan['limits']
    for v in (wall,evidence_bytes,active_seconds,feature_wall):number(v)
    reserve=L['answer_reservation_seconds'] if stage=='answer' else L['feature_load_reservation_seconds'] if loading else L['feature_forward_reservation_seconds']
    spent=sum(s['seconds'] for s in state['sessions'].values() if s['ended'])+active_seconds
    if spent+reserve>L['residency_seconds'] or wall+reserve>L['wall_seconds']:raise BudgetStop('combined time reservation')
    # Reserve a full second copy for the eventual local ZIP, plus next-request headroom.
    if 2*evidence_bytes+L['evidence_reservation_bytes']>L['evidence_bytes']:raise BudgetStop('raw plus packet evidence reservation')
    if stage=='feature':
        fs=sum((s['seconds'] if s['ended'] else 0) for s in state['sessions'].values() if s['stage']=='feature')+active_seconds
        if fs+reserve>L['feature_residency_seconds'] or feature_wall+reserve>L['feature_wall_seconds']:raise BudgetStop('feature time reservation')

def dispatch(run,plan,slot,session_id):
    state=scan(run);slots=state['slots'];schedule=plan['feature_schedule'] if slot['stage']=='feature' else plan['requests']
    prior=[v for v in slots.values() if v['stage']==slot['stage']]
    if slot['slot_id'] in slots or len(prior)>=len(schedule) or schedule[len(prior)]!=slot:raise IntegrityError('not next unchanged slot; no replay')
    if state['incidents'] or state['operational_stop_artifacts'] or any(r['state']!='COMPLETE' for r in slots.values()):raise IntegrityError('unresolved or stopped preceding work')
    if slot['stage']=='answer':
        feature=[r for r in slots.values() if r['stage']=='feature']
        if len(feature)!=50 or any(r['result'].get('status')!='OK' for r in feature):raise IntegrityError('feature stage incomplete/invalid')
        if any(not s['ended'] or not s['safe_stopped'] for s in state['sessions'].values() if s['stage']=='feature'):raise IntegrityError('feature worker not safely stopped')
        if sum(r['output_reservation'] for r in slots.values())+2048>plan['limits']['output_tokens']:raise BudgetStop('output reservation')
    else:
        if len(prior)>=50 or sum(r['input_positions'] for r in prior)+slot['input_positions']>plan['limits']['feature_input_positions']:raise BudgetStop('feature count/position reservation')
    append(run,'dispatch',session_id=session_id,slot_id=slot['slot_id'],request_hash=slot['request_hash'],
           output_reservation=2048 if slot['stage']=='answer' else 0,input_positions=slot.get('input_positions',0))
