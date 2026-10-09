"""Isolated same-checkpoint worker; authorization checked before importing torch.

No invocation is authorized in P02D preflight. File commands are accepted only
after durable supervisor admission and bound to the immutable pending plan.
"""
import argparse
import time
import traceback
from pathlib import Path
from .artifacts import read_json,write_new
from .contracts import IntegrityError,digest,file_hash
from .p02d_plan import RUN,PLAN_DIR,require_authorization
from .p02d_ledger import scan
from .p02d_features import validate_gate_input,decoder_feature,gate_vector

def generate_answer(model,tokenizer,request,cancel,torch,GenerationConfig,StoppingCriteria,StoppingCriteriaList):
    """Original native-channel/scorer pipeline; no repair or callback swallowing."""
    from torch.nn.attention import sdpa_kernel,SDPBackend
    from .p02b_runner import finish_reason
    from .p02_native import native_dataset,syntax
    from .p01_parsing import parse_and_score
    ids=torch.tensor([request['input_ids']],device='cuda:0',dtype=torch.long);mask=torch.ones_like(ids)
    config=GenerationConfig.from_dict(request['effective_generation_config'])
    torch.manual_seed(request['sampling_seed']);torch.cuda.manual_seed_all(request['sampling_seed'])
    token_ids=[];first=True;callback_error=None;reason=None;start=time.perf_counter()
    def checked(fn):
        def wrapped(*a,**k):
            nonlocal callback_error
            try:return fn(*a,**k)
            except BaseException as exc:callback_error=exc;raise
        return wrapped
    class Stream:
        @checked
        def put(self,value):
            nonlocal first
            if first:first=False;return
            token_ids.extend(value.reshape(-1).tolist())
        def end(self):pass
    class Stop(StoppingCriteria):
        @checked
        def __call__(self,input_ids,scores,**kwargs):
            nonlocal reason
            if cancel.exists() or time.perf_counter()-start>=120:reason='timeout'
            return reason is not None
    try:
        with torch.inference_mode(),sdpa_kernel([SDPBackend.MATH]):
            returned=model.generate(input_ids=ids,attention_mask=mask,generation_config=config,streamer=Stream(),stopping_criteria=StoppingCriteriaList([Stop()]))
        if callback_error is not None:raise callback_error
        if returned[0,ids.shape[1]:].tolist()!=token_ids:raise IntegrityError('streamed/returned token mismatch')
        sync_start=time.perf_counter();torch.cuda.synchronize();sync_seconds=time.perf_counter()-sync_start
    except BaseException as exc:
        # Caller persists the incident; attach partial tokens without scoring them.
        exc.partial_token_ids=list(token_ids)
        raise
    generation_seconds=time.perf_counter()-start
    raw=tokenizer.decode(token_ids,skip_special_tokens=False);parse_ids=list(token_ids)
    eos=config.eos_token_id if isinstance(config.eos_token_id,list) else [config.eos_token_id]
    terminal=parse_ids[-1] if parse_ids and parse_ids[-1] in eos else None
    if terminal is not None:parse_ids.pop()
    finish=finish_reason(reason,terminal,len(token_ids),2048)
    root=Path(request['_root']);native=native_dataset(root,request['family'],request['dataset_config']);entry=native[request['dataset_index']]
    if digest(entry)!=request['entry_hash']:raise IntegrityError('native entry changed')
    parsed=parse_and_score(tokenizer.decode(parse_ids,skip_special_tokens=False),request['mode'],request['opening_in_prompt'],finish,
        lambda payload:native.score_answer(payload,entry),syntax_fn=lambda payload:syntax(request['family'],payload))
    if finish=='timeout':
        parsed['failure_flags'].append('timeout')
        if not parsed['strict_valid_final']:parsed['status']='admitted_execution_failure'
    original={k:v for k,v in request.items() if k!='_root'}
    return dict(evidence_kind='development_observation',split='DEVELOPMENT',slot_id=request['slot_id'],request_id=request['slot_id'],
        request_hash=digest(original),package_hash=request['package_hash'],stream_id=request['stream_id'],
        raw_token_ids=token_ids,raw_decoded_text=raw,removed_terminal_eos_id=terminal,generated_tokens=len(token_ids),
        parsed=parsed,finish_reason=finish,model_error=None,generation_seconds=generation_seconds,synchronization_seconds=sync_seconds,
        cancellation_observation='generate returned and CUDA synchronized',automatic_retry=False)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--session',required=True);parser.add_argument('--stage',choices=['feature','answer'],required=True);parser.add_argument('--plan-hash',required=True)
    args=parser.parse_args();root=args.root.resolve();directory=root/RUN/'workers'/args.session
    plan=require_authorization(root,root/PLAN_DIR/'run_plan.json',args.plan_hash)
    if Path(__file__).resolve()!=root/'src/taskcognition/p02d_worker.py':raise IntegrityError('wrong worker source')
    slots=plan['feature_schedule'] if args.stage=='feature' else [q for q in plan['requests'] if q['slot_id']==args.session]
    initial=scan(root/RUN)
    if not slots or initial['slots'].get(slots[0]['slot_id'],{}).get('state')!='UNKNOWN_ADMISSION':raise IntegrityError('worker requires unique consumed dispatch')
    load_start=time.perf_counter()
    try:
        # All cache bytes verified inside the metered loader interval, before load.
        modeldir=root/plan['environment']['model_directory']
        for name,info in plan['environment']['model_files'].items():
            if file_hash(modeldir/name)!=info['sha256']:raise IntegrityError('cached checkpoint bytes changed')
        import torch
        from torch.nn.attention import sdpa_kernel,SDPBackend
        from transformers import AutoModelForCausalLM,AutoTokenizer,GenerationConfig,StoppingCriteria,StoppingCriteriaList
        model=AutoModelForCausalLM.from_pretrained(modeldir,dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).to('cuda:0')
        model.eval()
        if not all(p.device.type=='cuda' and p.dtype==torch.bfloat16 for p in model.parameters()):raise IntegrityError('precision/device')
        tokenizer=AutoTokenizer.from_pretrained(modeldir,local_files_only=True,trust_remote_code=False) if args.stage=='answer' else None
        torch.cuda.synchronize();load_seconds=time.perf_counter()-load_start
        write_new(directory/'ready.json',dict(load_seconds=load_seconds,hidden_width=model.config.hidden_size,attention='sdpa forced MATH',dtype='bfloat16'))
        for slot in slots:
            command=directory/'commands'/f'{slot["slot_id"]}.json';wait_start=time.perf_counter()
            while not command.exists():
                if (directory/'finish.json').exists():return
                if time.perf_counter()-wait_start>150:raise IntegrityError('supervisor command absent; finite child exit')
                time.sleep(.02)
            if read_json(command)!=slot:raise IntegrityError('changed worker command')
            ledger=scan(root/RUN)['slots'][slot['slot_id']]
            if ledger['state']!='ADMITTED' or ledger['request_hash']!=slot['request_hash']:raise IntegrityError('durable admission mismatch')
            torch.cuda.reset_peak_memory_stats()
            if args.stage=='feature':
                cpu_start=time.perf_counter()
                row=validate_gate_input(read_json(root/PLAN_DIR/'gate_inputs'/f'{slot["input_id"]}.json'))
                cheap_seconds=time.perf_counter()-cpu_start
                ids=torch.tensor([row['token_ids']],device='cuda:0',dtype=torch.long);mask=torch.ones_like(ids)
                torch.cuda.synchronize();start=time.perf_counter()
                with sdpa_kernel([SDPBackend.MATH]):vector=decoder_feature(model,ids,mask,plan['feature_specification']['hidden_width'])
                torch.cuda.synchronize();seconds=time.perf_counter()-start
                if seconds>120:raise IntegrityError('feature forward exceeded deadline; tranche stops')
                cpu_start=time.perf_counter();gate=gate_vector(row,vector.cpu().tolist());cpu_seconds=cheap_seconds+time.perf_counter()-cpu_start
                result=dict(evidence_kind='development_observation',split='DEVELOPMENT',slot_id=slot['slot_id'],request_hash=slot['request_hash'],
                    status='OK',dtype='float32',gate=gate,input_positions=len(row['token_ids']),forward_seconds=seconds,
                    cpu_feature_seconds=cpu_seconds,kind=slot['kind'],use_cache=False)
            else:
                request=read_json(root/PLAN_DIR/'requests'/f'{slot["slot_id"]}.json')
                if digest(request)!=slot['request_hash']:raise IntegrityError('worker request hash')
                request['_root']=str(root)
                result=generate_answer(model,tokenizer,request,directory/'cancel'/f'{slot["slot_id"]}.json',torch,GenerationConfig,StoppingCriteria,StoppingCriteriaList)
            result.update(load_seconds=load_seconds,max_allocated_bytes=torch.cuda.max_memory_allocated(),max_reserved_bytes=torch.cuda.max_memory_reserved())
            write_new(directory/'results'/f'{slot["slot_id"]}.json',result)
        # Normal parent stop; finite wait prevents abandoned idle residency.
        start=time.perf_counter()
        while not (directory/'finish.json').exists():
            if time.perf_counter()-start>30:raise IntegrityError('finish handshake missing')
            time.sleep(.02)
    except BaseException as exc:
        write_new(directory/'incident.json',dict(evidence_kind='development_observation',scored=False,error=repr(exc),traceback=traceback.format_exc(),
            partial_token_ids=getattr(exc,'partial_token_ids',None),partial_tokens_unscored=True,elapsed_since_loader_start=time.perf_counter()-load_start))
        raise

if __name__=='__main__':main()
