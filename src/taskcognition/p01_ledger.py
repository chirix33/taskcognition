"""P01 single-host append-only admission ledger. No automatic retries."""
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from .artifacts import read_json, write_new, child_path
from .contracts import IntegrityError, file_hash, digest


def require_real_dispatch(root: Path):
    phase=read_json(root/'configs/phase_state.json')
    if (phase.get('active_phase')!='P01' or phase.get('status')!='IN_PROGRESS'
            or phase.get('real_dispatch_enabled') is not True):
        raise IntegrityError('real P01 dispatch disabled; offline correction does not authorize generation')


def events(run: Path):
    rows=[]
    previous=None
    for index,path in enumerate(sorted((run/'events').glob('*.json'))):
        if path.name!=f'{index:06d}.json': raise IntegrityError('ledger sequence gap')
        row=read_json(path)
        if row['previous_sha256']!=previous: raise IntegrityError('ledger hash chain mismatch')
        previous=file_hash(path)
        rows.append(row)
    return rows


def append(run: Path, event: str, request_id: str, **fields):
    rows=events(run)
    prior=run/'events'/f'{len(rows)-1:06d}.json'
    row={'evidence_kind':'development_observation','split':'DEVELOPMENT','event':event,
         'request_id':request_id,'timestamp_utc':datetime.now(timezone.utc).isoformat(),
         'previous_sha256':file_hash(prior) if rows else None, **fields}
    # Publish only after fsync so the supervising reader never sees partial JSON.
    pending=run/'events'/f'{len(rows):06d}.{uuid4().hex}.pending'
    write_new(pending,row)
    pending.rename(run/'events'/f'{len(rows):06d}.json')


def reconcile(run: Path):
    result={}
    for event in events(run):
        key=event['request_id']
        if event['event']=='dispatch':
            if key in result: raise IntegrityError('duplicate dispatch')
            result[key]={'state':'UNKNOWN_ADMISSION','request_hash':event['request_hash'],
                         'stream_id':event['stream_id'],'reserved_output_tokens':event['max_new_tokens'],
                         'resource_seconds':0.0}
        else:
            if key not in result: raise IntegrityError('event before dispatch')
            row=result[key]
            if event['event']=='admitted':
                if row['state']!='UNKNOWN_ADMISSION':raise IntegrityError('invalid admission transition')
                row['state']='ADMITTED_NO_TERMINAL'
            elif event['event']=='terminal':
                if row['state'] not in ('UNKNOWN_ADMISSION','ADMITTED_NO_TERMINAL'):
                    raise IntegrityError('duplicate terminal')
                path=child_path(run,event['result_path'])
                if not path.is_file() or file_hash(path)!=event['result_sha256']:
                    raise IntegrityError('missing/corrupted persisted result; not a model failure')
                data=read_json(path)
                if data['request_id']!=key:raise IntegrityError('result identity mismatch')
                row['state']='COMPLETE'
                row['result']=data
            elif event['event']=='proven_nonadmission':
                if row['state']!='UNKNOWN_ADMISSION' or not event.get('proof'):
                    raise IntegrityError('nonadmission requires proof before admission')
                row['state']='PROVEN_NONADMISSION_NO_RETRY'
            elif event['event']=='resource':
                if row.get('resource_recorded'):raise IntegrityError('duplicate resource charge')
                if event['seconds']<0:raise IntegrityError('negative resource charge')
                row['resource_seconds']=event['seconds']
                row['resource_recorded']=True
            elif event['event']!='first_token':
                raise IntegrityError('unexpected ledger event')
    return result


def reserve(run: Path, request: dict):
    rows=reconcile(run)
    key=request['request_id']
    if key in rows:raise IntegrityError('request already dispatched: never replay admitted/unknown/completed; J=0')
    if len(rows)>=8 or sum(r['reserved_output_tokens'] for r in rows.values())+1024>8192:
        raise IntegrityError('P01 global answer/output reservation budget exhausted')
    if request.get('split')!='DEVELOPMENT' or request.get('evidence_kind')!='development_observation':
        raise IntegrityError('P01 only DEVELOPMENT observations')
    if request.get('max_new_tokens')!=1024:raise IntegrityError('P01 cap must be 1024')
    if request['stream_id'] in {r['stream_id'] for r in rows.values()}:raise IntegrityError('stream reuse')
    append(run,'dispatch',key,request_hash=digest(request),stream_id=request['stream_id'],max_new_tokens=1024)


def terminal(run: Path, request_id: str, result: dict):
    if result.get('request_id')!=request_id:raise IntegrityError('result identity mismatch')
    path=run/'results'/f'{request_id}.json'
    write_new(path,result)
    append(run,'terminal',request_id,result_path=path.relative_to(run).as_posix(),result_sha256=file_hash(path))
