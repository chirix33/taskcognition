"""Development-only cell/cluster inspection; missing evidence is never imputed."""
from collections import Counter
from dataclasses import asdict
from statistics import fmean,variance
from .artifacts import read_json
from .contracts import InputRecord,DrawRecord,IntegrityError,digest,file_hash
from .targets import aggregate
from .p02_native import ENTRIES
from .p02b_reporting import primary_record
from .p02d_plan import PLAN_DIR,RUN,validate_plan
from .p02d_ledger import scan
from .p02d_runner import validate_result

def report(root,plan):
    validate_plan(plan)
    run=root/RUN;state=scan(run,tolerant=True);observations=[];incidents=list(state['incidents'])
    stop=None
    if state['unknown_residency']:
        incidents.append(dict(event='unresolved_process_or_cost',scored=False))
    unresolved=[k for k,v in state['slots'].items() if v['state'] in ('UNKNOWN_ADMISSION','ADMITTED')]
    if unresolved:incidents.append(dict(event='unresolved_consumed_slots',slot_ids=unresolved,scored=False))
    # Final reporting, unlike a live ledger-prefix scan, requires independently
    # published resource/stop records to have their matching committed events.
    linked_resources={e['resource_path'] for e in state['events'] if e['event']=='session_end' and 'resource_path' in e}
    linked_stops={e['path'] for e in state['operational_stops']}
    for directory,linked in [('session_resources',linked_resources),('operational_stops',linked_stops)]:
        for p in (run/directory).glob('*.json'):
            if p.relative_to(run).as_posix() not in linked:
                incidents.append(dict(event='unresolved_publication',path=p.relative_to(run).as_posix(),scored=False))
    if (run/'supervisor_stop.json').exists():
        try:
            stop=read_json(run/'supervisor_stop.json')
            if not stop.get('resource_stop'):incidents.append(dict(event='supervisor_stop',record=stop))
        except Exception as exc:incidents.append(dict(event='supervisor_stop_integrity',error=str(exc)))
    for q in plan['requests']:
        row=state['slots'].get(q['slot_id'])
        if row is None or row['result'] is None:continue
        try:
            validate_result(root,plan,q,row['result'])
            request=read_json(root/PLAN_DIR/'requests'/f'{q["slot_id"]}.json')
            value=primary_record(request,row)
            session=state['sessions'][row['session_id']]
            if not session['ended'] or not session['safe_stopped']:raise IntegrityError('result has unresolved worker residency/cleanup')
            observations.append(dict(q,**value,worker_seconds=session['seconds'],
                max_allocated_bytes=row['result'].get('max_allocated_bytes'),max_reserved_bytes=row['result'].get('max_reserved_bytes')))
        except Exception as exc:incidents.append(dict(slot_id=q['slot_id'],error=str(exc),scored=False))
    cells=[];clusters=[]
    for family in ENTRIES:
        for mode in ('D','R'):
            planned=[q for q in plan['requests'] if q['family']==family and q['mode']==mode]
            retained=[o for o in observations if o['family']==family and o['mode']==mode]
            executed=[q for q in planned if q['slot_id'] in state['slots']]
            cells.append(dict(family=family,mode=mode,planned=16,executed=len(executed),retained=len(retained),
                executed_is_lower_bound=any(i.get('event')=='ledger_integrity_incident' for i in incidents),
                missing_or_unscored=[q['slot_id'] for q in planned if q['slot_id'] not in {o['slot_id'] for o in retained}],
                strict_valid_final=sum(o['strict_valid_final'] for o in retained),perfect_correct=sum(o['perfect_correct'] for o in retained),
                native_scores=[o['native_score'] for o in retained],wrapper_subtypes=dict(Counter(o['wrapper_subtype'] for o in retained if o['wrapper_subtype'])),
                failures=dict(Counter(f for o in retained for f in o['failure_flags'])),timeouts=sum(o['timeout'] for o in retained),
                output_tokens=[o['output_tokens'] for o in retained],generation_seconds=[o['generation_seconds'] for o in retained],
                worker_seconds=[o['worker_seconds'] for o in retained],peak_allocated_bytes=[o['max_allocated_bytes'] for o in retained]))
    for item in plan['inputs']:
        selected=[o for o in observations if o['input_id']==item['input_id']]
        counts={m:sum(o['mode']==m for o in selected) for m in ('D','R')}
        cluster=dict(input_id=item['input_id'],family=item['family'],achieved=counts,planned_per_mode=4,
            direct_perfect_count=sum(o['perfect_correct'] for o in selected if o['mode']=='D'),
            complete_K4=counts=={'D':4,'R':4},targets=None,
            within_input={m:dict(scores=[o['native_score'] for o in selected if o['mode']==m],
                sample_variance=variance([o['native_score'] for o in selected if o['mode']==m]) if counts[m]>=2 else None) for m in ('D','R')})
        if cluster['complete_K4']:
            native=read_json(root/PLAN_DIR/'outcome_inputs'/f'{item["input_id"]}.json')
            inp=InputRecord('development_observation',item['input_id'],'DEVELOPMENT',item['family'],item['latent_hash'],
                native['entry']['question'],item['raw_tokens'],item['seed'],digest(native['effective_config']),'pinned native scorer','outcome-only entry')
            draws=[]
            for o in selected:
                score=o['native_score'];status='perfect' if score==1 else 'partial' if score>0 else 'admitted_failure' if o['failure_flags'] else 'wrong'
                p=run/'results'/f'{o["slot_id"]}.json'
                draws.append(DrawRecord('development_observation',digest([o['input_id'],o['package_hash'],o['draw_index']]),
                    o['input_id'],'DEVELOPMENT',o['mode'],o['package_hash'],o['draw_index'],o['stream_id'],str(p.relative_to(root)),file_hash(p),
                    score,o['perfect_correct'],o['worker_seconds'],'descriptive_answer_worker_seconds_not_final_scalar_cost',status))
            agg=asdict(aggregate(inp,draws,4,{m:next(o['package_hash'] for o in selected if o['mode']==m) for m in ('D','R')}))
            cluster['targets']={k:agg[k] for k in ('benefit','joint_spoilage','direct_redraw','decline_010','decline_025','mean_score_D','mean_score_R','perfect_rate_D','perfect_rate_R')}
        clusters.append(cluster)
    summaries={}
    for mode in ('D','R'):
        family_means={f:fmean(o['native_score'] for o in observations if o['family']==f and o['mode']==mode)
                      for f in ENTRIES if any(o['family']==f and o['mode']==mode for o in observations)}
        summaries[mode]=dict(family_means=family_means,equal_family_mean=fmean(family_means.values()) if len(family_means)==6 else None,
            complete_population=len(observations)==192,warning='Available retained draws only; partial missingness changes the observed subset. No six-family mean if a family is missing.')
    feature_measurements=[];vectors={};feature_stability=[]
    for slot in plan['feature_schedule']:
        row=state['slots'].get(slot['slot_id'])
        if row is None or row['result'] is None:continue
        try:
            result=validate_result(root,plan,slot,row['result'])
            feature_measurements.append(dict(slot_id=slot['slot_id'],input_id=slot['input_id'],kind=slot['kind'],
                **{field:result.get(field) for field in ('forward_seconds','cpu_feature_seconds','load_seconds','input_positions','max_allocated_bytes','max_reserved_bytes')}))
            values=result['gate']['embedding'];first=vectors.setdefault(slot['input_id'],values)
            feature_stability.append(dict(slot_id=slot['slot_id'],input_id=slot['input_id'],max_abs_difference_from_first=max(abs(a-b) for a,b in zip(first,values)),new_independent_input=False))
        except Exception as exc:incidents.append(dict(slot_id=slot['slot_id'],error=str(exc),scored=False))
    stopped=bool(state['operational_stops'] or (stop and stop.get('resource_stop')))
    return dict(evidence_kind='development_observation',phase='P02D',status='INTEGRITY_INCIDENT' if incidents else 'STOPPED_INCOMPLETE' if stopped else 'INCOMPLETE' if len(observations)!=192 else 'COMPLETE_DEVELOPMENT',
        cells=cells,clusters=clusters,observations=observations,incidents=incidents,equal_family_summary=summaries,
        supervisor_stop=stop,operational_stops=state['operational_stops'],consumed_slots={k:v['state'] for k,v in state['slots'].items()},
        feature_measurements=feature_measurements,feature_stability=feature_stability,ledger_integrity_complete=not any(i.get('event')=='ledger_integrity_incident' for i in incidents),
        research_resources=dict(sessions=state['sessions'],measured_residency_seconds=state['measured_residency_seconds'],unknown_residency=state['unknown_residency'],
            output_tokens_observed=sum(o['output_tokens'] or 0 for o in observations),output_tokens_unknown=sum(o['output_tokens'] is None for o in observations)),
        deployment_projection='One live feature forward plus CPU gate plus one selected answer and reviewed initialization allocation per routed query. Research repeats/warmups are collection costs, not 50 passes per query. No tariff, beta or hard support bound adopted.',
        missingness='Unexecuted, admitted unknown, software incidents and corrupt results are missing/unresolved, not score zero. K-squared cross-pairs are dependent diagnostics within each of 24 input clusters.')
