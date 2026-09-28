"""One isolated GPU request per process; no repeat, fallback or answer repair."""
import argparse
from pathlib import Path
import time
import traceback
import warnings
from .artifacts import read_json,write_new
from .contracts import digest,file_hash,IntegrityError
from .p01_ledger import append,terminal,reconcile,require_real_dispatch
from .p01_native import native_dataset
from .p01_parsing import parse_and_score


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--request',type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve()
    require_real_dispatch(root)
    resource=read_json(root/'configs/p01_resource_plan.json')
    run=root/resource['output_directory']
    request=read_json(args.request)
    key=request['request_id']
    state=reconcile(run)[key]
    if state['state']!='UNKNOWN_ADMISSION' or state['request_hash']!=digest(request):
        raise IntegrityError('worker requires unique unchanged dispatch')
    for name,expected in request['source_files'].items():
        if file_hash(Path(__file__).parent/name)!=expected:raise IntegrityError('worker source changed after planning')
    import torch
    from torch.nn.attention import sdpa_kernel,SDPBackend
    from transformers import AutoModelForCausalLM,AutoTokenizer,GenerationConfig,StoppingCriteria,StoppingCriteriaList
    model_path=root/request['model_directory']
    start_load=time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        tokenizer=AutoTokenizer.from_pretrained(model_path,local_files_only=True,trust_remote_code=False)
        model=AutoModelForCausalLM.from_pretrained(model_path,dtype=torch.bfloat16,
                  attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).to('cuda:0')
        model.eval()
        assert all(p.device.type=='cuda' and p.dtype==torch.bfloat16 for p in model.parameters())
        torch.cuda.synchronize()
        load_seconds=time.perf_counter()-start_load
        config=GenerationConfig.from_dict(request['effective_generation_config'])
        inputs=torch.tensor([request['input_ids']],device='cuda',dtype=torch.long)
        mask=torch.ones_like(inputs)
        torch.manual_seed(request['sampling_seed'])
        torch.cuda.manual_seed_all(request['sampling_seed'])
        torch.cuda.reset_peak_memory_stats()
        cancel=run/'cancel'/f'{key}.json'
        token_ids=[]
        first=True
        generation_start=None
        stopping_reason=None
        callback_error=None
        def callback(fn):
            # Do not let a backend that swallows a callback exception authorize scoring.
            def checked(*args,**kwargs):
                nonlocal callback_error
                try:return fn(*args,**kwargs)
                except Exception as exc:
                    callback_error=exc
                    raise
            return checked
        class Stream:
            @callback
            def put(self,value):
                nonlocal first
                if first:
                    first=False
                    return
                values=value.reshape(-1).tolist()
                first_output=not token_ids
                token_ids.extend(values)  # diagnostic only if evidence publication then fails
                if first_output:
                    append(run,'first_token',key,elapsed_seconds=time.perf_counter()-generation_start)
            def end(self):pass
        class Stop(StoppingCriteria):
            @callback
            def __call__(self,input_ids,scores,**kwargs):
                nonlocal stopping_reason
                if cancel.exists():
                    reason=read_json(cancel)['reason']
                    if reason not in ('deliberate_interruption','timeout'):raise IntegrityError('unknown cancellation reason')
                    stopping_reason='controlled_interruption' if reason=='deliberate_interruption' else 'timeout'
                elif time.perf_counter()-generation_start>=120:stopping_reason='timeout'
                return stopping_reason is not None
        stage='admission'
        try:
            # Conservative admission boundary: durable admission immediately before generate.
            torch.cuda.synchronize()
            append(run,'admitted',key,boundary='immediately before model.generate',load_seconds=load_seconds)
            generation_start=time.perf_counter()
            stage='generation'
            with torch.inference_mode(),sdpa_kernel([SDPBackend.MATH]):
                generated=model.generate(input_ids=inputs,attention_mask=mask,generation_config=config,
                    streamer=Stream(),stopping_criteria=StoppingCriteriaList([Stop()]))
            if callback_error is not None:raise callback_error
            stage='returned_token_check'
            returned=generated[0,inputs.shape[1]:].tolist()
            if returned!=token_ids:raise IntegrityError('streamed/returned token mismatch')
            stage='synchronization'
            before_sync=time.perf_counter()
            torch.cuda.synchronize()
            sync_seconds=time.perf_counter()-before_sync
        except Exception as exc:
            # Diagnostic capture only: no exception allowlist and no score imputation.
            # Preserve any damaged files; if diagnostic writing fails, retain both errors
            # in the uncaught traceback/worker stderr and still stop the process.
            incident={'evidence_kind':request['evidence_kind'],'split':request['split'],
                'request_id':key,'request_hash':digest(request),'scored':False,
                'status':'unclassified_worker_incident','stage':'callback' if callback_error is not None else stage,
                'error_type':type(exc).__name__,'error_message':str(exc),'traceback':traceback.format_exc(),
                'partial_token_ids':list(token_ids),'partial_tokens_are_unscored':True,
                'automatic_retry':False,'device_completion':'unknown; no synchronization claim on incident path'}
            try:write_new(run/'incidents'/f'{key}.json',incident)
            except Exception as diagnostic_error:
                exc.add_note('Incident persistence also failed: '+repr(diagnostic_error))
            raise
        generation_seconds=time.perf_counter()-generation_start
        raw_text=tokenizer.decode(token_ids,skip_special_tokens=False)
        parse_ids=list(token_ids)
        eos=config.eos_token_id if isinstance(config.eos_token_id,list) else [config.eos_token_id]
        terminal_eos=parse_ids[-1] if parse_ids and parse_ids[-1] in eos else None
        if terminal_eos is not None:parse_ids.pop()
        text=tokenizer.decode(parse_ids,skip_special_tokens=False)
        finish=stopping_reason or ('eos' if terminal_eos is not None else 'cap' if len(token_ids)>=1024 else 'other')
        dataset=native_dataset(root,resource['dataset_config'])
        entry=dataset[request['dataset_index']]
        parsed=parse_and_score(text,request['mode'],request['opening_in_prompt'],finish,
                               lambda payload:dataset.score_answer(payload,entry))
        if finish in ('timeout','controlled_interruption'):
            parsed['failure_flags'].append(finish)
            if not parsed['strict_valid_final']:parsed['status']='admitted_execution_failure'
        result={'evidence_kind':'development_observation','split':'DEVELOPMENT','request_id':key,
                'purpose':request['purpose'],'mode':request['mode'],'package_hash':request['package_hash'],
                'request_hash':digest(request),'stream_id':request['stream_id'],
                'raw_token_ids':token_ids,'raw_decoded_text':raw_text,'removed_terminal_eos_id':terminal_eos,
                'generated_tokens':len(token_ids),'parsed':parsed,'finish_reason':finish,'model_error':None,
                'generation_seconds':generation_seconds,'synchronization_seconds':sync_seconds,
                'load_seconds':load_seconds,'max_allocated_bytes':torch.cuda.max_memory_allocated(),
                'max_reserved_bytes':torch.cuda.max_memory_reserved(),'warnings':[str(w.message) for w in caught],
                'cancellation_observation':'generate returned and CUDA synchronized; no asynchronous device work from this request remains',
                'native_scorer':'upstream number_sorting, unchanged, tolerance 1, binary',
                'model_device':'cuda:0','model_dtype':'bfloat16','attention':'sdpa forced MATH',
                'automatic_retry':False}
        terminal(run,key,result)
    print(digest(result),flush=True)

if __name__=='__main__':main()
