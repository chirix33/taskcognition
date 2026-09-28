"""Read-only incomplete-run inspection. Diagnostics never modify primary outcomes."""
import re
from pathlib import Path
from .artifacts import read_json,child_path
from .contracts import IntegrityError,file_hash,digest
from .p02_native import syntax

def inspect_ledger(run):
    rows={};incidents=[];previous=None;chain_complete=True
    for index,path in enumerate(sorted((run/'events').glob('*.json'))):
        try:
            event=read_json(path)
            if path.name!=f'{index:06d}.json' or event['previous_sha256']!=previous:raise IntegrityError('ledger sequence/hash mismatch')
            previous=file_hash(path);key=event['request_id'];kind=event['event']
            if kind=='dispatch':
                if key in rows:raise IntegrityError('duplicate dispatch')
                rows[key]=dict(state='UNKNOWN_ADMISSION',request_hash=event['request_hash'],reserved_tokens=event['max_new_tokens'],resource_seconds=None,result=None)
            else:
                row=rows[key]
                if kind=='admitted':row['state']='ADMITTED_NO_TERMINAL'
                elif kind=='terminal':
                    try:
                        p=child_path(run,event['result_path'])
                        if file_hash(p)!=event['result_sha256']:raise IntegrityError('corrupt result')
                        data=read_json(p)
                        if data['request_id']!=key:raise IntegrityError('result identity')
                        row.update(state='COMPLETE',result=data,result_sha256=event['result_sha256'])
                    except Exception as exc:
                        row['state']='RESULT_INTEGRITY_INCIDENT';incidents.append(dict(request_id=key,error=str(exc)))
                elif kind=='resource':
                    if row['resource_seconds'] is not None or event['seconds']<0:raise IntegrityError('resource charge integrity')
                    row['resource_seconds']=event['seconds']
                elif kind not in ('first_token','proven_nonadmission'):raise IntegrityError('unexpected event')
        except Exception as exc:
            incidents.append(dict(path=str(path.name),error=str(exc)));chain_complete=False;break
    for p in (run/'incidents').glob('*.json'):incidents.append(dict(path=p.relative_to(run).as_posix(),sha256=file_hash(p)))
    if (run/'supervisor_stop.json').exists():incidents.append(dict(path='supervisor_stop.json',sha256=file_hash(run/'supervisor_stop.json')))
    return dict(rows=rows,incidents=incidents,chain_complete=chain_complete)

def primary_record(request,row):
    """Absent evidence yields None, never zero; explicit forced termination is retained."""
    result=row.get('result')
    if not result:return None
    if result.get('model_error') is not None:raise IntegrityError('software error is not a scored outcome')
    parsed=result.get('parsed')
    if parsed is None:
        if result.get('finish_reason')=='supervisor_forced_termination' and result.get('forced_termination') is True and result.get('native_score')==0 and result.get('valid_retainable_output') is False:
            return dict(native_score=0.0,perfect_correct=False,strict_valid_final=False,status='admitted_execution_failure',failure_flags=['known_forced_termination'],wrapper_subtype=None,output_tokens=None,generation_seconds=None,finish_reason=result['finish_reason'],timeout=False)
        raise IntegrityError('unexpected nonstandard result; unscored incident')
    if result.get('request_hash')!=digest(request) or result.get('package_hash')!=request['package_hash'] or result.get('stream_id')!=request['stream_id']:raise IntegrityError('request/result binding')
    if result['generated_tokens']!=len(result['raw_token_ids']) or result['generated_tokens']>request['max_new_tokens']:raise IntegrityError('token/cap integrity')
    return dict(native_score=parsed['native_score'],perfect_correct=parsed['perfect_correct'],strict_valid_final=parsed['strict_valid_final'],status=parsed['status'],failure_flags=parsed['failure_flags'],wrapper_subtype=wrapper_subtype(parsed),output_tokens=result['generated_tokens'],generation_seconds=result['generation_seconds'],finish_reason=result['finish_reason'],timeout=result['finish_reason']=='timeout')

def wrapper_subtype(parsed):
    if 'outer_wrapper_failure' not in parsed.get('failure_flags',[]):return None
    text=parsed.get('final_channel')
    if text is None:return 'no_final_channel'
    opening=text.count('<FINAL>');closing=text.count('</FINAL>')
    if opening==closing==0:return 'missing_both_tags'
    if opening==0:return 'missing_open_tag'
    if closing==0:return 'missing_close_tag'
    if opening!=1 or closing!=1:return 'multiple_or_ambiguous_tags'
    begin=text.index('<FINAL>');end=text.index('</FINAL>')
    if end<begin:return 'invalid_tag_order'
    if not text[begin+7:end].strip(' \t\r\n'):return 'empty_payload'
    if text[:begin].strip(' \t\r\n') or text[end+8:].strip(' \t\r\n'):return 'forbidden_outside_prose'
    return 'other_wrapper_failure'

def diagnostic_payload(family,parsed):
    """One unambiguous final-channel payload only; no search, traces or repair."""
    if parsed.get('strict_valid_final'):return None
    text=parsed.get('final_channel')
    if text is None:return None
    text=text.strip(' \t\r\n');kind=None;payload=None
    if '<FINAL>' not in text and '</FINAL>' not in text:
        payload=text;kind='bare_native_payload_diagnostic'
        # Text-native scorers are permissive; require unmistakable bare syntax for
        # diagnostic eligibility instead of selecting answers from explanations.
        if family=='letter_counting' and not re.fullmatch(r'[0-9]+',payload):return None
        if family=='knights_knaves':
            assignment=r'[A-Za-z]+\s+is\s+(?:a|an)\s+(?:knight|knave|pioneer|laggard|saint|sinner|hero|villain|angel|devil|altruist|egoist|sage|fool)'
            if not re.fullmatch(assignment+r'(?:(?:,?\s+and\s+|,\s*)'+assignment+r')*\.?',payload,re.I):return None
    elif text.count('<FINAL>')==text.count('</FINAL>')==1:
        begin=text.index('<FINAL>');end=text.index('</FINAL>')
        if begin>=end:return None
        if not (text[:begin].strip(' \t\r\n') or text[end+8:].strip(' \t\r\n')):return None
        payload=text[begin+7:end].strip(' \t\r\n');kind='single_tagged_payload_with_outside_prose_diagnostic'
    if not payload or '<FINAL>' in payload or '</FINAL>' in payload:return None
    try:syntax(family,payload)
    except (ValueError,TypeError,OverflowError):return None
    return dict(kind=kind,payload=payload,changes_primary_score=False,changes_completion=False)

def cell_summary(plan,inspection,observations,family,mode,cap):
    planned=[q for q in plan['requests'] if (q['family'],q['mode'],q['cap'])==(family,mode,cap)]
    selected=[o for o in observations if (o['family'],o['mode'],o['cap'])==(family,mode,cap)]
    rows=inspection['rows'];executed=[q for q in planned if q['request_id'] in rows]
    return dict(family=family,mode=mode,cap=cap,planned=len(planned),executed=len(executed),retained=len(selected),unexecuted=len(planned)-len(executed) if inspection['chain_complete'] else None,execution_unknown_due_ledger_integrity=not inspection['chain_complete'],strict_valid_final=sum(o['strict_valid_final'] for o in selected),perfect_correct=sum(o['perfect_correct'] for o in selected),native_scores=[o['native_score'] for o in selected],wrapper_subtypes=[o['wrapper_subtype'] for o in selected],native_syntax_failure=sum('native_syntax_failure' in o['failure_flags'] for o in selected),cap_without_final=sum('cap_without_valid_final' in o['failure_flags'] for o in selected),timeout=sum(o['timeout'] for o in selected),failure_flags=[o['failure_flags'] for o in selected],output_tokens=[o['output_tokens'] for o in selected],generation_seconds=[o['generation_seconds'] for o in selected],worker_seconds=[rows[q['request_id']]['resource_seconds'] for q in executed],missing_or_unscored_requests=[q['request_id'] for q in planned if q['request_id'] not in {o['request_id'] for o in selected}])
