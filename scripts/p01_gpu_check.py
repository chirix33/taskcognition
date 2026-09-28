"""No autoregressive work: synchronized numeric and native BF16 GPU checks."""
import json
import platform
from pathlib import Path
import time
import warnings
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[1]
output=root/'reports/p01/gpu_check.json'
if output.exists(): raise RuntimeError('immutable output exists')
start=time.perf_counter()
report={'evidence_kind':'development_observation','purpose':'GPU kernel compatibility, no model',
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'model_calls':0,'python':platform.python_version()}
try:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        import torch
        from torch.nn.attention import sdpa_kernel, SDPBackend
        report.update(torch=torch.__version__,cuda_runtime=torch.version.cuda,
                      device=torch.cuda.get_device_name(0),capability=list(torch.cuda.get_device_capability(0)),
                      architectures=torch.cuda.get_arch_list(),native_bf16_reported=torch.cuda.is_bf16_supported(including_emulation=False))
        assert report['native_bf16_reported'], 'Native BF16 not supported; stop before precision choice'
        checks=[]
        for dtype in (torch.float32,torch.bfloat16):
            torch.cuda.synchronize()
            t=time.perf_counter()
            a=torch.ones((64,64),device='cuda',dtype=dtype)
            b=a@a
            torch.cuda.synchronize()
            ok=bool(torch.isfinite(b).all().item() and torch.equal(b,torch.full_like(b,64)))
            checks.append({'operation':'64x64 ones matmul','dtype':str(dtype),'expected':64,'passed':ok,'seconds':time.perf_counter()-t})
            assert ok
        q=torch.zeros((1,2,8,32),device='cuda',dtype=torch.bfloat16)
        v=torch.ones_like(q)
        t=time.perf_counter()
        with sdpa_kernel([SDPBackend.MATH]):
            result=torch.nn.functional.scaled_dot_product_attention(q,q,v)
        torch.cuda.synchronize()
        ok=bool(torch.isfinite(result).all().item() and torch.equal(result,v))
        checks.append({'operation':'built-in SDPA MATH BF16','expected':1,'passed':ok,'seconds':time.perf_counter()-t})
        assert ok
        report['checks']=checks
        report['warnings']=[str(w.message) for w in caught]
        report['max_allocated_bytes']=torch.cuda.max_memory_allocated()
        report['max_reserved_bytes']=torch.cuda.max_memory_reserved()
        report['gpu_free_total_bytes']=list(torch.cuda.mem_get_info())
        del a,b,q,v,result
        torch.cuda.synchronize()
    report['status']='PASS'
except Exception as exc:
    report['status']='FAIL'
    report['error']=repr(exc)
report['process_elapsed_seconds']=time.perf_counter()-start
with output.open('x',encoding='utf-8',newline='\n') as f:json.dump(report,f,indent=2)
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['status']=='PASS' else 1)
