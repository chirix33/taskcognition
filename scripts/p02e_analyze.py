"""Reproducible DEVELOPMENT algebra on accepted P02D data; standard library only.

No model libraries, scorer changes, audit implementation, gate fitting or simulation.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from statistics import mean,variance
import csv,hashlib,json,math,sys,time

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'reports/p02e'
L=math.log(40); A=7*L/3
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def table(path,rows):
 with path.open('x',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader()
  for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
def assert_close(x,y):
 if not math.isclose(x,y,rel_tol=1e-11,abs_tol=1e-9):raise ValueError(f'reconciliation mismatch {x} != {y}')
def radius(n,v,width=1):
 if n<2 or v<0 or width<0 or not all(math.isfinite(x) for x in (n,v,width)):raise ValueError('invalid algebra input')
 return math.sqrt(2*v*L/n)+width*A/(n-1)
def summarize_cluster(item,obs):
 ds={m:sorted([o for o in obs if o['mode']==m],key=lambda o:o['draw_index']) for m in ('D','R')}
 if any(len(ds[m])!=4 or [o['draw_index'] for o in ds[m]]!=[0,1,2,3] for m in ds):raise ValueError('incomplete K4 cluster')
 scores={m:[o['native_score'] for o in ds[m]] for m in ds}
 if any(type(s) not in (int,float) or not math.isfinite(s) or not 0<=s<=1 for vals in scores.values() for s in vals):raise ValueError('invalid score')
 p={m:mean(s==1 for s in scores[m]) for m in ds};mu={m:mean(scores[m]) for m in ds}
 return dict(input_id=item['input_id'],family=item['family'],dataset_index=item['dataset_index'],K_D=4,K_R=4,weight=1/24,
  scores_D=scores['D'],scores_R=scores['R'],mean_D=mu['D'],mean_R=mu['R'],perfect_rate_D=p['D'],perfect_rate_R=p['R'],
  variance_D=variance(scores['D']),variance_R=variance(scores['R']),benefit=mu['R']-mu['D'],joint_spoilage=p['D']*(1-p['R']),
  direct_redraw=4/3*p['D']*(1-p['D']),decline_010=sum(d-r>=.1 for d in scores['D'] for r in scores['R'])/16,
  decline_025=sum(d-r>=.25 for d in scores['D'] for r in scores['R'])/16,direct_perfect_count=sum(s==1 for s in scores['D']),
  strict_final_D=sum(o['strict_valid_final'] for o in ds['D']),strict_final_R=sum(o['strict_valid_final'] for o in ds['R']),
  worker_mean_D=mean(o['worker_seconds'] for o in ds['D']),worker_mean_R=mean(o['worker_seconds'] for o in ds['R']),
  generation_mean_D=mean(o['generation_seconds'] for o in ds['D']),generation_mean_R=mean(o['generation_seconds'] for o in ds['R']))
def diagnostic_rule(name,clusters):
 funcs={'always_D':lambda c:0,'always_R':lambda c:1,'observed_positive_benefit':lambda c:int(c['benefit']>0),
        'complement_positive_benefit':lambda c:int(c['benefit']<=0)}
 action=[funcs[name](c) for c in clusters];B=[g*c['perfect_rate_D'] for g,c in zip(action,clusters)]
 H=[g*c['joint_spoilage'] for g,c in zip(action,clusters)];delta=[g*c['benefit'] for g,c in zip(action,clusters)]
 weights=[c['weight'] for c in clusters];exposure=sum(w*b for w,b in zip(weights,B));numerator=sum(w*h for w,h in zip(weights,H))
 aw=[w*b for w,b in zip(weights,B)];kden=sum(v*v for v in aw)
 per_family={f:sum(c['weight']*b for c,b in zip(clusters,B) if c['family']==f) for f in sorted({c['family'] for c in clusters})}
 return dict(rule=name,interpretation='Fixed prompt diagnostic; outcome-informed for benefit/complement; no deployable candidate',
  selected_input_count=sum(action),weighted_routing_rate=sum(w*g for w,g in zip(weights,action)),
  weighted_spoilage_numerator=numerator,weighted_exposure_B=exposure,conditional_spoilage=None if exposure==0 else numerator/exposure,
  risk_status='undefined/no exposure' if exposure==0 else 'descriptive ratio only',
  raw_nested_direct_successes=sum(g*c['direct_perfect_count'] for g,c in zip(action,clusters)),
  selected_inputs_with_direct_success=sum(g and c['direct_perfect_count']>0 for g,c in zip(action,clusters)),
  exposure_by_family=per_family,families_contributing_exposure=[f for f,x in per_family.items() if x>0],
  kish_concentration=None if kden==0 else sum(aw)**2/kden,variance_B=variance(B),mean_delta=mean(delta),variance_delta=variance(delta),
  mean_selected_primary_score=sum(w*((1-g)*c['mean_D']+g*c['mean_R']) for c,w,g in zip(clusters,weights,action)),
  selected_answer_worker_proxy_seconds=sum(w*((1-g)*c['worker_mean_D']+g*c['worker_mean_R']) for c,w,g in zip(clusters,weights,action)),
  selected_generation_component_seconds=sum(w*((1-g)*c['generation_mean_D']+g*c['generation_mean_R']) for c,w,g in zip(clusters,weights,action)),
  gate_cost='unmeasured additive per query if active, including routed-D queries; bypassed for always-D fallback',
  input_actions=[dict(input_id=c['input_id'],g=g) for c,g in zip(clusters,action)])
def cost_partition(worker,load,work,cpu_feature,cleanup,wall):
 residual=worker-load-work-cpu_feature-cleanup;outside=wall-worker
 if residual < -1e-9 or outside < -1e-9:raise ValueError('overlapping or invalid costs')
 return dict(load_components=load,generation_and_forward_components=work,cpu_feature_component=cpu_feature,
  cleanup_components=cleanup,unallocated_within_residency=residual,outside_residency_in_execution_wall=outside,
  summed_residency=worker,execution_wall=wall)
def balanced_ceiling(x):return 6*math.ceil(x/6)
def main():
 start=time.perf_counter();cpu=time.process_time();verification=read(OUT/'acceptance_verification.json')
 # No final audit or production runner is imported. Re-bind every empirical source read.
 for n,h in verification['accepted_hashes'].items():
  if sha(ROOT/n)!=h:raise ValueError('accepted hash mismatch: '+n)
 idx=read(ROOT/'reports/p02d_execution/P02D_execution_evidence_index.json')['files']
 accessed={}
 def bound(n):
  h=sha(ROOT/n)
  if h!=idx[n]:raise ValueError('accepted source mismatch: '+n)
  accessed[n]=h;return read(ROOT/n)
 report=bound('reports/p02d_execution/production_execution_report.json')
 accounting=bound('reports/p02d_execution/execution_accounting.json')
 plan=bound('artifacts/development/p02d-cr01-plan-v4/run_plan.json')
 declaration=read(OUT/'analytical_declaration.json')
 assert report['status']=='COMPLETE_DEVELOPMENT' and not report['incidents']
 obs=report['observations'];assert len(obs)==192 and len({o['stream_id'] for o in obs})==192
 clusters=[summarize_cluster(i,[o for o in obs if o['input_id']==i['input_id']]) for i in plan['inputs']]
 assert Counter(c['family'] for c in clusters)=={f:4 for f in {c['family'] for c in clusters}}
 for c,old in zip(clusters,report['clusters']):
  assert c['input_id']==old['input_id']
  for k in ['benefit','joint_spoilage','direct_redraw','decline_010','decline_025']:assert_close(c[k],old['targets'][k])
 rules=[diagnostic_rule(n,clusters) for n in declaration['fixed_rules']]
 assert [r['raw_nested_direct_successes'] for r in rules]==[0,30,6,24]
 assert [r['selected_input_count'] for r in rules]==[0,24,11,13]
 assert sum(c['benefit']>0 for c in clusters)==11 and sum(c['benefit']<0 for c in clusters)==0
 assert sum(c['joint_spoilage'] for c in clusters)==0 and sum(c['direct_perfect_count']>0 for c in clusters)==8
 table(OUT/'cluster_rows.csv',clusters);write(OUT/'cluster_rows.json',dict(evidence_kind='development_observation',analysis_kind='offline_cluster_reconciliation',rows=clusters))
 table(OUT/'diagnostic_rules.csv',[{k:v for k,v in r.items() if k!='input_actions'} for r in rules])
 write(OUT/'diagnostic_rules.json',dict(evidence_kind='development_observation',not_candidates=True,rules=rules))
 events=[bound(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT/'artifacts/development/p02d-cr01-tranche/ledger').glob('*.json'))]
 previous=None
 for ix,e in enumerate(events):
  assert e['previous_sha256']==previous;previous=accessed[f'artifacts/development/p02d-cr01-tranche/ledger/{ix:06d}.json']
 assert len(events)==7257
 resources={r['session_id']:r for r in accounting['resource_records']}
 sessions=[]
 for o in obs:
  sid=o['slot_id'];res=bound(f'artifacts/development/p02d-cr01-tranche/session_resources/{sid}.json')
  assert res==resources[sid] and res['safe_stopped'] and res['exit_code']==0
  raw=bound(f'artifacts/development/p02d-cr01-tranche/results/{sid}.json')
  assert raw==bound(f'artifacts/development/p02d-cr01-tranche/workers/{sid}/results/{sid}.json')
  assert len(raw['raw_token_ids'])==o['output_tokens']
  timeline={e['event']:(j,e) for j,e in enumerate(events) if e.get('session_id')==sid and e['event'] in ['session_start','admitted','result','session_end']}
  def gap(first,last):return (datetime.fromisoformat(timeline[last][1]['timestamp_utc'])-datetime.fromisoformat(timeline[first][1]['timestamp_utc'])).total_seconds()
  sessions.append(dict(slot_id=sid,input_id=o['input_id'],family=o['family'],mode=o['mode'],draw_round=o['draw_index']+1,
   output_tokens=o['output_tokens'],primary_score=o['native_score'],worker_seconds=res['seconds'],load_seconds=res['load_seconds'],
   generation_seconds=o['generation_seconds'],sync_seconds_nested=raw['synchronization_seconds'],cleanup_seconds=res['cleanup_seconds'],
   worker_minus_load_minus_generation=res['seconds']-res['load_seconds']-o['generation_seconds'],
   residual_after_cleanup=res['seconds']-res['load_seconds']-o['generation_seconds']-res['cleanup_seconds'],
   ledger_events_before_session=timeline['session_start'][0],timestamp_start_to_admitted=gap('session_start','admitted'),
   timestamp_admitted_to_result=gap('admitted','result'),timestamp_result_to_end=gap('result','session_end'),
   timestamp_span=gap('session_start','session_end')))
 groups=[]
 for round_id in range(1,5):
  for mode in ['D','R','ALL']:
   ss=[s for s in sessions if s['draw_round']==round_id and (mode=='ALL' or s['mode']==mode)]
   groups.append(dict(draw_round=round_id,mode=mode,count=len(ss),output_tokens=sum(s['output_tokens'] for s in ss),
    worker_sum=sum(s['worker_seconds'] for s in ss),worker_mean=mean(s['worker_seconds'] for s in ss),
    load_mean=mean(s['load_seconds'] for s in ss),generation_mean=mean(s['generation_seconds'] for s in ss),
    residual_mean=mean(s['worker_minus_load_minus_generation'] for s in ss),residual_sum=sum(s['worker_minus_load_minus_generation'] for s in ss),
    start_to_admitted_mean=mean(s['timestamp_start_to_admitted'] for s in ss),admitted_to_result_mean=mean(s['timestamp_admitted_to_result'] for s in ss),
    result_to_end_mean=mean(s['timestamp_result_to_end'] for s in ss),ledger_events_before_min=min(s['ledger_events_before_session'] for s in ss),ledger_events_before_max=max(s['ledger_events_before_session'] for s in ss)))
 table(OUT/'cost_sessions.csv',sessions);table(OUT/'cost_round_mode.csv',groups)
 f=resources['features'];features=report['feature_measurements'];fw=sum(x['forward_seconds'] for x in features);fcpu=sum(x['cpu_feature_seconds'] for x in features)
 worker=sum(v['seconds'] for v in resources.values());load=sum(v['load_seconds'] for v in resources.values());gen=sum(o['generation_seconds'] for o in obs)
 cleanup=sum(v['cleanup_seconds'] for v in resources.values());wall=accounting['runner_execution_end']['wall_seconds']
 parts=cost_partition(worker,load,gen+fw,fcpu,cleanup,wall)
 assert_close(worker,11560.2217413);assert_close(wall,12836.8229112);assert len(resources)==193
 assert sum(s['output_tokens'] for s in sessions)==129371
 reportcost=bound('reports/p02d_execution/offline_reporting_cost.json')
 receipt=read(ROOT/'reports/p02d_execution/P02D_execution_packet_receipt.json')
 cost=dict(evidence_kind='development_observation',analysis_kind='offline_cost_reconciliation',sessions=193,answer_calls=192,feature_forwards=50,
  feature_warmups=2,known_output_tokens=129371,unknown_output_tokens=0,reserved_output_tokens=393216,partition=parts,
  nested_detail=dict(answer_generation_seconds=gen,feature_forward_seconds=fw,feature_cpu_seconds=fcpu,feature_residency=f['seconds'],feature_load=f['load_seconds'],
   feature_residual=f['seconds']-f['load_seconds']-fw-fcpu-f['cleanup_seconds'],answer_sync_seconds_in_generation=sum(s['sync_seconds_nested'] for s in sessions)),
  separate_collection_costs=dict(P02D_report_wall=reportcost['wall_seconds'],P02D_report_cpu=reportcost['cpu_process_seconds'],
   P02D_package_wall=receipt['packaging_wall_seconds'],P02D_package_cpu=receipt['packaging_cpu_process_seconds'],
   command_wrapper_wall=accounting['command_wall_seconds'],wrapper_extra_only=accounting['command_wall_seconds']-wall,
   other_preparation_validation_human_wall='Not comprehensively instrumented; recorded commands preserved in accepted packet; not assumed zero'),
  round_mode=groups,unavailable=['GPU kernel busy time','CPU total during collection','separate validation/scoring/ledger-scan/evidence-enumeration timings','trained gate/calibration service time','persistent service/init allocation','hard service-time support'],
  residual_causality='Observed arithmetic and timestamp intervals; no profiler or new benchmark. Growing scans in source are a plausible contributor, not measured attribution.',
  units='seconds; components are nested; do not sum resource and component totals twice',raw_bytes=sum(p.stat().st_size for p in (ROOT/'artifacts/development/p02d-cr01-tranche').rglob('*') if p.is_file()))
 write(OUT/'cost_reconciliation.json',cost)
 scenarios=[];necessary=[]
 for rule in rules:
  B=rule['weighted_exposure_B'];v=rule['variance_B'];delta=rule['mean_delta'];dv=rule['variance_delta']
  for alpha in declaration['alpha_grid']:
   for bmin in declaration['b_min_grid']:
    necessary.append(dict(rule=rule['rule'],alpha=alpha,b_min=bmin,
     zero_harm_range_only_n_min=None if alpha*B==0 else 1+A/(alpha*B),
     zero_harm_range_only_balanced_n_min=None if alpha*B==0 else balanced_ceiling(1+A/(alpha*B)),
     denominator_range_only_n_min=None if B<=bmin else 1+A/(B-bmin),
     denominator_range_only_balanced_n_min=None if B<=bmin else balanced_ceiling(1+A/(B-bmin)),
     null_meaning='no finite solution to that necessary condition',sufficient_or_power=False))
    for n in declaration['n_grid']:
     scenarios.append(dict(rule=rule['rule'],n=n,alpha=alpha,b_min=bmin,mean_B_assumed=B,variance_B_assumed=v,
      range_only_B_Z=A/(n-1),B_lower_expression=B-radius(n,v),Z_upper_expression=-alpha*B+radius(n,alpha*alpha*v,1),
      Delta_lower_expression=delta-radius(n,dv,2),eligibility_or_audit_decision=None,illustrative_unadopted=True))
 table(OUT/'analytical_scenarios.csv',scenarios)
 rare=[]
 for pd in declaration['rare_event_grid']['p_D']:
  for pr in declaration['rare_event_grid']['p_R']:
   for K in declaration['rare_event_grid']['K']:
    rare.append(dict(p_D=pd,p_R=pr,K=K,true_harm=pd*(1-pr),probability_empirical_harm_zero=(1-pd)**K+pr**K-(1-pd)**K*pr**K,illustrative_unadopted=True))
 write(OUT/'analytical_constraints.json',dict(evidence_kind='development_observation',analysis_kind='analytical_not_audit',
  declaration_sha256=sha(OUT/'analytical_declaration.json'),log40=L,A=A,anchor_range_term=A/23,max_available_B=.3125,
  anchor_best_range_only_B_lower=.3125-A/23,necessary_conditions=necessary,rare_event_examples=rare,
  no_theorem_validation=True,no_final_audit_import=True,cost_width='symbolic W_C',delta_score='symbolic test-only margin'))
 # Illustrative collection scale, NOT future independent data or a resource authorization.
 allmean=mean(s['worker_seconds'] for s in sessions);lastmean=next(g['worker_mean'] for g in groups if g['draw_round']==4 and g['mode']=='ALL')
 scale=[]
 for n in declaration['n_grid'][2:]:
  for K in declaration['resource_comparison']['K']:
   total_inputs=2250+n;calls=2*K*total_inputs
   scale.append(dict(illustrative_unadopted=True,audit_n_placeholder=n,K_placeholder=K,other_split_inputs_placeholder=2250,
    all_split_inputs=total_inputs,answer_calls=calls,max_output_tokens=2048*calls,
    hours_flat_allround_worker_proxy=calls*allmean/3600,hours_flat_last_round_worker_proxy=calls*lastmean/3600,
    warning='Excludes features/gates/retries/warmups and additional supervision; growing-ledger overhead can exceed linear scaling. No approved budget or precision estimate.'))
 table(OUT/'longer_study_resource_scenarios.csv',scale)
 summary=dict(evidence_kind='development_observation',analysis_kind='offline_design',outcomes=192,clusters=24,K=4,
  perfect_D=sum(c['direct_perfect_count'] for c in clusters),perfect_R=sum(o['perfect_correct'] for o in obs if o['mode']=='R'),
  strict_D=sum(c['strict_final_D'] for c in clusters),strict_R=sum(c['strict_final_R'] for c in clusters),
  positive_benefit=11,zero_benefit=13,negative_benefit=0,zero_harm_targets=24,inputs_with_D_success=8,
  all_scores_binary=all(o['native_score'] in [0,1] for o in obs),historical_draws_pooled=False,
  allround_answer_worker_mean=allmean,last_round_answer_worker_mean=lastmean,
  breadth_vs_depth=dict(equal_answer_budget=192,fresh_24_K4='24 new clusters; historical 24 remain a separate tranche',existing_24_extra_K4='same 24 clusters at K8; never increases independent n'),
  scalar_ledger_adopted=False,alpha_bmin_beta_delta_n_K_frozen=False)
 write(OUT/'summary.json',summary)
 write(OUT/'source_bindings.json',dict(accepted_packet_sha256=verification['accepted_hashes']['reports/p02d_execution/P02D_execution_review_packet.zip'],files=accessed))
 assert not any(m in sys.modules for m in ['torch','transformers','taskcognition.audit','taskcognition.p02d_runner'])
 write(OUT/'analysis_run_receipt.json',dict(evidence_kind='development_observation',analysis_kind='offline_design',status='PASS',
  timestamp_utc=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),declaration_sha256=sha(OUT/'analytical_declaration.json'),
  bound_records_read=len(accessed),wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
  new_model_loads=0,new_feature_forwards=0,new_answer_generations=0,new_gpu_work=0,gate_fits=0,simulations=0,final_labels=0,
  no_model_or_final_audit_import=True,scientific_choices_adopted=False))
 print(json.dumps(summary));print(json.dumps(parts))
if __name__=='__main__':main()
