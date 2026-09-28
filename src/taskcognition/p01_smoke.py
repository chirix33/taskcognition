"""P01 supervisor: planned tiny pair and one deliberate interruption; no P02 path."""
import argparse
from datetime import datetime,timezone
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import time
from .artifacts import read_json,write_new
from .contracts import IntegrityError,digest,file_hash,stream_id
from .p01_ledger import reserve,reconcile,append,terminal,events
from .p01_native import native_dataset


def paths(root):
    plan=read_json(root/'configs/p01_resource_plan.json')
    return plan,root/plan['output_directory']


def prepare(root):
    from transformers import AutoTokenizer,GenerationConfig
    plan,run=paths(root)
    if run.exists():raise IntegrityError('run already planned; immutable')
    if read_json(root/'reports/p01/gpu_check.json')['status']!='PASS':raise IntegrityError('GPU checks missing')
    dataset=native_dataset(root,plan['dataset_config'])
    model=read_json(root/'reports/p01/model_download.json')
    model_dir=root/model['local_directory']
    tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True,trust_remote_code=False)
    config=GenerationConfig.from_pretrained(model_dir,local_files_only=True)
    config.update(do_sample=True,temperature=.6,top_p=.95,top_k=20,min_p=0.,max_new_tokens=1024,
                  num_beams=1,num_return_sequences=1,use_cache=True,return_dict_in_generate=False,
                  output_scores=False,output_logits=False)
    config.pad_token_id=config.eos_token_id[0] if isinstance(config.eos_token_id,list) else config.eos_token_id
    source={p.name:file_hash(p) for p in sorted(Path(__file__).parent.glob('*.py'))}
    package={'evidence_kind':'development_observation','model_id':plan['model_id'],'revision':plan['model_revision'],
             'precision':'BF16','attention':'sdpa forced MATH','torch':importlib.metadata.version('torch'),
             'transformers':importlib.metadata.version('transformers'),'generation_config':config.to_dict(),
             'model_files':{f['name']:f['sha256'] for f in model['files']},
             'native_source_manifest_sha256':file_hash(root/'vendor/reasoning_gym_p01/source_manifest_complete.json'),
             'source_files':source,'cap_includes_thinking_and_final':True,
             'parser_policy':'native channel in prompt context; single FINAL pair; ASCII whitespace only outside; original native scorer'}
    run.mkdir(parents=True)
    write_new(run/'package.json',package)
    checks=[]
    entry=dataset[0]
    # Native hand-checks, without model calls. Sorting tolerance is upstream, not exact match.
    for payload,expected in [(entry['answer'],1.),("['100','200','300']",0.),('nonsense',0.)]:
        score=dataset.score_answer(payload,entry)
        assert score==expected
        checks.append({'payload':payload,'expected':expected,'observed':score})
    write_new(root/('reports/p01/'+run.name+'_native_scorer_validation.json'),{'evidence_kind':'fixture',
        'scope':'hand-checked native scorer only; no empirical model answers','family':'number_sorting',
        'native_revision':plan['native_revision'],'entry':entry,'checks':checks,
        'partial_credit_note':'This family has binary native scores. Fractional score preservation uses explicitly synthetic parser unit tests.'})
    requests=[]
    for key,mode,index,purpose in [('initial_D','D',0,'initial smoke'),('initial_R','R',0,'initial smoke'),
                                  ('interrupt_R','R',1,'deliberate post-admission interruption diagnostic')]:
        entry=dataset[index]
        # Same two-message input information for D/R, no conversation history or outcome fields.
        messages=[{'role':'system','content':'Return your final answer as exactly one nonempty <FINAL>...</FINAL> pair, with the requested answer inside and no text outside the pair on the final answer channel.'},
                  {'role':'user','content':entry['question']}]
        rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=mode=='R')
        ids=tokenizer.encode(rendered,add_special_tokens=False)
        if len(ids)>256:raise IntegrityError('tiny smoke input exceeds 256-token plan')
        opening=rendered.rfind('<think>')>rendered.rfind('</think>')
        if mode=='D' and opening:raise IntegrityError('D template left a thinking channel open')
        package_hash=digest({**package,'mode':mode,'enable_thinking':mode=='R'})
        input_id=digest(['P01-DEVELOPMENT',plan['native_revision'],plan['dataset_config'],index,entry['question']])
        stream=stream_id('p01-windows-5090-20260928',20260928,'DEVELOPMENT',input_id,package_hash,0)
        request={'evidence_kind':'development_observation','split':'DEVELOPMENT','request_id':key,'purpose':purpose,
                 'mode':mode,'enable_thinking':mode=='R','dataset_index':index,'input_id':input_id,
                 'stream_id':stream,'sampling_seed':int(stream[:15],16),'package_hash':package_hash,
                 'messages':messages,'rendered_prompt':rendered,'rendered_prompt_hash':digest(rendered),
                 'input_ids':ids,'input_tokens':len(ids),'opening_in_prompt':opening,
                 'effective_generation_config':config.to_dict(),'max_new_tokens':1024,
                 'model_directory':model['local_directory'],'source_files':source}
        write_new(run/'requests'/f'{key}.json',request)
        requests.append({'request_id':key,'request_hash':digest(request),'mode':mode,'input_id':input_id,
                         'input_tokens':len(ids),'stream_id':stream,'purpose':purpose})
    write_new(run/'run_plan.json',{'evidence_kind':'development_observation','resource_plan':plan,
                                  'package_sha256':file_hash(run/'package.json'),'requests':requests,
                                  'pre_dispatch_counters':reconcile(run)})
    installed={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}
    write_new(root/'reports/p01/environment_lock.json',{'evidence_kind':'development_observation','python':sys.version,
        'distributions':installed,'torch_runtime_verification_sha256':file_hash(root/'reports/p01/gpu_check.json'),
        'runtime_requirements_sha256':file_hash(root/'configs/p01_requirements.lock'),'source_files':source})
    print(read_json(run/'run_plan.json'))


def record_worker_exit(run,request,*,elapsed,exit_code,forced,cancellation_seconds):
    """Charge observed work, then fail closed on unexplained missing evidence."""
    key=request['request_id']
    if any(e['request_id']==key and e['event']=='resource' for e in events(run)):
        raise IntegrityError('worker resources already recorded; investigate without replay')
    append(run,'resource',key,seconds=elapsed,process_exit=exit_code,forced_termination=forced,
           cancellation_to_exit_seconds=cancellation_seconds,conservative_gpu_residency=True)
    state=reconcile(run)[key]
    if state['state']!='COMPLETE':
        if (run/'results'/f'{key}.json').exists():raise IntegrityError('orphan result requires investigation')
        if not forced:
            raise IntegrityError('unexpected worker exit without terminal evidence; investigate, never impute a model score')
        terminal(run,key,{'evidence_kind':'development_observation','split':'DEVELOPMENT','request_id':key,
                         'purpose':request['purpose'],'mode':request['mode'],'finish_reason':'supervisor_forced_termination',
                         'native_score':0.0,'valid_retainable_output':False,'generated_tokens':None,
                         'admission':'known' if state['state']=='ADMITTED_NO_TERMINAL' else 'unknown_counts_as_admitted',
                         'failure_record_basis':'supervisor deliberately killed the live worker at its operational limit; no result file existed',
                         'process_exit':exit_code,'forced_termination':True})
    if exit_code!=0:raise IntegrityError('worker failure; stop and inspect without retry')
    return reconcile(run)[key]


def run_job(root,key):
    plan,run=paths(root)
    phase=read_json(root/'configs/phase_state.json')
    if phase.get('active_phase')!='P01' or phase.get('status')!='IN_PROGRESS':raise IntegrityError('P01 not in progress')
    request=read_json(run/'requests'/f'{key}.json')
    rows=reconcile(run)
    if any(not r.get('resource_recorded') for r in rows.values()):raise IntegrityError('unreconciled previous worker resources')
    spent=read_json(root/'reports/p01/gpu_check.json')['process_elapsed_seconds']+sum(r['resource_seconds'] for r in rows.values())
    if spent+300>1800:raise IntegrityError('insufficient remaining GPU envelope for load/generate/cleanup')
    if key=='interrupt_R' and not all(k in rows and rows[k]['state']=='COMPLETE' for k in ('initial_D','initial_R')):
        raise IntegrityError('initial pair must finish before diagnostic')
    reserve(run,request)
    started=time.perf_counter()
    env=os.environ.copy()
    env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONUTF8='1')
    stdout=(run/'worker_logs'/f'{key}.stdout.txt')
    stdout.parent.mkdir(parents=True,exist_ok=True)
    stderr=run/'worker_logs'/f'{key}.stderr.txt'
    cancellation_requested=None
    admitted_seen=None
    forced=False
    with stdout.open('xb') as out,stderr.open('xb') as err:
        process=subprocess.Popen([sys.executable,'-m','taskcognition.p01_worker','--root',str(root),
                                  '--request',str(run/'requests'/f'{key}.json')],stdout=out,stderr=err,env=env,
                                  creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        while process.poll() is None:
            current=[r for r in events(run) if r['request_id']==key]
            if admitted_seen is None and any(r['event']=='admitted' for r in current):admitted_seen=time.perf_counter()
            interrupt=key=='interrupt_R' and any(r['event']=='first_token' for r in current)
            overdue=admitted_seen is not None and time.perf_counter()-admitted_seen>=120
            if (interrupt or overdue) and cancellation_requested is None:
                cancellation_requested=time.perf_counter()
                write_new(run/'cancel'/f'{key}.json',{'evidence_kind':'development_observation',
                           'reason':'deliberate_interruption' if interrupt else 'timeout',
                           'timestamp_utc':datetime.now(timezone.utc).isoformat()})
            if (admitted_seen is not None and time.perf_counter()-admitted_seen>130) or time.perf_counter()-started>min(300,1800-spent):
                process.kill()
                forced=True
                break
            time.sleep(.02)
        process.wait(timeout=30)
    elapsed=time.perf_counter()-started
    result=record_worker_exit(run,request,elapsed=elapsed,exit_code=process.returncode,forced=forced,
                             cancellation_seconds=None if cancellation_requested is None else time.perf_counter()-cancellation_requested)
    print({'request_id':key,'state':result['state'],'seconds':elapsed,'exit':process.returncode,
           'finish_reason':result['result']['finish_reason']},flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','initial','interrupt','reconcile'])
    args=parser.parse_args()
    root=Path.cwd()
    if args.action=='prepare':prepare(root)
    elif args.action=='initial':
        run_job(root,'initial_D')
        run_job(root,'initial_R')
    elif args.action=='interrupt':run_job(root,'interrupt_R')
    else:
        plan,run=paths(root)
        rows=reconcile(run)
        print({'requests':rows,'reserved_calls':len(rows),'reserved_tokens':sum(r['reserved_output_tokens'] for r in rows.values())})

if __name__=='__main__':main()
