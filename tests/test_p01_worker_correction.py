"""Offline fault injection through the real worker.main; torch is never imported.

Only backend objects are replaced. Production admission, callbacks, parsing, terminal
publication and supervisor exit accounting run against disposable fixture directories.
"""
from contextlib import nullcontext
import io
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace as NS
import unittest
from unittest.mock import patch

from taskcognition import p01_worker as worker
from taskcognition.artifacts import read_json, write_new
from taskcognition.contracts import IntegrityError, digest, file_hash
from taskcognition.p01_ledger import append, events, reconcile, reserve, terminal
from taskcognition.p01_smoke import record_worker_exit, run_job


class Tensor:
    def __init__(self, values):self.values=values; self.shape=(1,len(values))
    def reshape(self,*args):return self
    def tolist(self):return self.values
    def __getitem__(self,key):return Tensor(self.values[key[1]])


class WorkerBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.run=self.root/'run'
        self.tokens=[ord(c) for c in '<FINAL>[1]</FINAL>']
        self.calls=0
        self.request={'request_id':'fixture','evidence_kind':'development_observation','split':'DEVELOPMENT',
            'stream_id':digest('fixture'),'max_new_tokens':1024,'model_directory':'nonexistent-mock',
            'source_files':{'p01_worker.py':file_hash(Path(worker.__file__))},'input_ids':[1],
            'sampling_seed':1,'effective_generation_config':{'eos_token_id':999},'dataset_index':0,
            'mode':'D','opening_in_prompt':False,'purpose':'offline worker regression fixture','package_hash':digest('mock')}
        self.path=self.run/'requests/fixture.json'
        write_new(self.path,self.request)
        write_new(self.root/'configs/p01_resource_plan.json',{'output_directory':'run','dataset_config':{}})
        write_new(self.root/'configs/phase_state.json',{'active_phase':'P01','status':'IN_PROGRESS','real_dispatch_enabled':True})
        reserve(self.run,self.request)
        self.behavior=lambda **kw:self.emit(kw)
        self.torch=ModuleType('torch')
        self.torch.bfloat16='mock-bf16'; self.torch.long='mock-long'
        self.torch.cuda=NS(synchronize=lambda:None,manual_seed_all=lambda _:None,reset_peak_memory_stats=lambda:None,
                           max_memory_allocated=lambda:0,max_memory_reserved=lambda:0)
        self.torch.tensor=lambda values,**kwargs:Tensor(values[0])
        self.torch.ones_like=lambda _:Tensor([1]); self.torch.manual_seed=lambda _:None
        self.torch.inference_mode=nullcontext
        attention=ModuleType('torch.nn.attention')
        attention.sdpa_kernel=lambda _:nullcontext(); attention.SDPBackend=NS(MATH='mock')
        model=NS(to=lambda _:model,eval=lambda:None,parameters=lambda:[NS(device=NS(type='cuda'),dtype='mock-bf16')],generate=self.generate)
        tokenizer=NS(decode=lambda ids,**kwargs:''.join(chr(i) for i in ids if i!=999))
        transformers=ModuleType('transformers')
        transformers.AutoModelForCausalLM=NS(from_pretrained=lambda *a,**kw:model)
        transformers.AutoTokenizer=NS(from_pretrained=lambda *a,**kw:tokenizer)
        transformers.GenerationConfig=NS(from_dict=lambda d:NS(**d))
        transformers.StoppingCriteria=object; transformers.StoppingCriteriaList=list
        self.modules={'torch':self.torch,'torch.nn':ModuleType('torch.nn'),'torch.nn.attention':attention,'transformers':transformers}
        self.dataset=type('Dataset',(list,),{'score_answer':lambda *args:1.0})([{}])

    def generate(self,**kwargs):
        self.calls+=1
        return self.behavior(**kwargs)

    def emit(self,kwargs,tokens=None):
        tokens=self.tokens+[999] if tokens is None else tokens
        kwargs['streamer'].put(Tensor([1]))  # prompt, not an answer token
        for token in tokens:kwargs['streamer'].put(Tensor([token]))
        kwargs['stopping_criteria'][0](None,None)
        return Tensor([1]+tokens)

    def execute(self):
        with patch.dict(sys.modules,self.modules),patch.object(sys,'argv',['worker','--root',str(self.root),'--request',str(self.path)]), \
             patch.object(worker,'native_dataset',return_value=self.dataset),patch('sys.stdout',new_callable=io.StringIO), \
             patch.object(worker,'parse_and_score',wraps=worker.parse_and_score) as score:
            self.score=score
            worker.main()

    def incident(self,error):
        self.assertFalse((self.run/'results/fixture.json').exists())
        self.assertFalse(any(e['event']=='terminal' for e in events(self.run)))
        self.score.assert_not_called()
        data=read_json(self.run/'incidents/fixture.json')
        self.assertEqual(data['error_type'],type(error).__name__)
        self.assertFalse(data['scored'])
        self.assertNotIn('native_score',data)
        return data

    def test_generate_typeerror_stops_without_score(self):
        self.check_generate_error(TypeError('injected bad argument'))

    def test_generate_valueerror_stops_without_score(self):
        self.check_generate_error(ValueError('injected bad configuration'))

    def test_arbitrary_runtimeerror_is_not_allowlisted(self):
        self.check_generate_error(RuntimeError('unclassified runtime failure'))

    def test_integrityerror_still_propagates(self):
        self.check_generate_error(IntegrityError('injected integrity fault'))

    def check_generate_error(self,error):
        def fail(**kwargs):raise error
        self.behavior=fail
        with self.assertRaises(type(error)) as caught:self.execute()
        self.assertIs(caught.exception,error)
        self.incident(error)
        self.assertEqual(reconcile(self.run)['fixture']['state'],'ADMITTED_NO_TERMINAL')

    def test_first_token_ledger_io_error_retains_partial_diagnostic(self):
        error=OSError('injected evidence write failure')
        damaged=self.run/'events/000002.pending'
        def callback(run,event,key,**fields):
            if event=='first_token':
                damaged.write_bytes(b'partial evidence')
                raise error
            return append(run,event,key,**fields)
        with patch.object(worker,'append',side_effect=callback),self.assertRaises(OSError):self.execute()
        data=self.incident(error)
        self.assertEqual(data['partial_token_ids'],[self.tokens[0]])
        self.assertEqual(damaged.read_bytes(),b'partial evidence')

    def test_admission_callback_error_stops_before_generate(self):
        error=OSError('admission fsync failed')
        with patch.object(worker,'append',side_effect=error),self.assertRaises(OSError):self.execute()
        self.incident(error)
        self.assertEqual(self.calls,0)
        self.assertEqual(reconcile(self.run)['fixture']['state'],'UNKNOWN_ADMISSION')
        with self.assertRaises(IntegrityError):record_worker_exit(self.run,self.request,elapsed=.125,exit_code=1,forced=False,cancellation_seconds=None)
        self.assertEqual(reconcile(self.run)['fixture']['resource_seconds'],.125)
        with self.assertRaises(IntegrityError):reserve(self.run,self.request)

    def test_damaged_cancellation_record_stops_after_tokens(self):
        path=self.run/'cancel/fixture.json'
        path.parent.mkdir(); path.write_bytes(b'{"reason":"timeout","reason":"deliberate_interruption"}')
        with self.assertRaises(IntegrityError) as caught:self.execute()
        data=self.incident(caught.exception)
        self.assertTrue(data['partial_token_ids'])
        self.assertEqual(path.read_bytes(),b'{"reason":"timeout","reason":"deliberate_interruption"}')

    def test_error_after_valid_looking_partial_output_never_scores(self):
        error=ValueError('failure after output')
        def fail(**kwargs):
            self.emit(kwargs,self.tokens)
            raise error
        self.behavior=fail
        with self.assertRaises(ValueError):self.execute()
        self.assertEqual(self.incident(error)['partial_token_ids'],self.tokens)

    def test_streamed_returned_mismatch_is_incident(self):
        def mismatch(**kwargs):
            self.emit(kwargs)
            return Tensor([1,77])
        self.behavior=mismatch
        with self.assertRaises(IntegrityError) as caught:self.execute()
        self.incident(caught.exception)

    def test_backend_swallowing_callback_cannot_enable_scoring(self):
        error=OSError('first-token evidence failure swallowed by backend')
        def callback(run,event,key,**fields):
            if event=='first_token':raise error
            return append(run,event,key,**fields)
        def swallowing(**kwargs):
            kwargs['streamer'].put(Tensor([1]))
            try:kwargs['streamer'].put(Tensor(self.tokens))
            except OSError:pass
            return Tensor([1]+self.tokens)
        self.behavior=swallowing
        with patch.object(worker,'append',side_effect=callback),self.assertRaises(OSError):self.execute()
        self.assertEqual(self.incident(error)['partial_token_ids'],self.tokens)
        with self.assertRaises(IntegrityError):record_worker_exit(self.run,self.request,elapsed=.5,exit_code=1,forced=False,cancellation_seconds=None)
        self.assertEqual(reconcile(self.run)['fixture']['resource_seconds'],.5)
        with self.assertRaises(IntegrityError):reserve(self.run,self.request)

    def test_stream_tensor_conversion_failure_stops(self):
        error=OSError('stream conversion failure')
        class BrokenTensor:
            def reshape(self,*args):raise error
        def fail(**kwargs):
            kwargs['streamer'].put(Tensor([1]))
            kwargs['streamer'].put(BrokenTensor())
        self.behavior=fail
        with self.assertRaises(OSError):self.execute()
        self.incident(error)

    def test_incident_write_failure_preserves_file_and_original_error(self):
        path=self.run/'incidents/fixture.json'
        path.parent.mkdir(); path.write_bytes(b'damaged prior diagnostic')
        error=ValueError('unexpected failure')
        def fail(**kwargs):raise error
        self.behavior=fail
        with self.assertRaises(ValueError) as caught:self.execute()
        self.assertIs(caught.exception,error)
        self.assertIn('Incident persistence also failed',error.__notes__[0])
        self.assertEqual(path.read_bytes(),b'damaged prior diagnostic')
        self.score.assert_not_called()
        self.assertFalse((self.run/'results/fixture.json').exists())

    def test_unknown_cancellation_reason_is_not_a_timeout(self):
        write_new(self.run/'cancel/fixture.json',{'reason':'bad configuration'})
        with self.assertRaises(IntegrityError) as caught:self.execute()
        self.incident(caught.exception)

    def test_error_accounted_once_and_unknown_exit_zero_cannot_hide_it(self):
        error=TypeError('injected')
        def fail(**kwargs):raise error
        self.behavior=fail
        with self.assertRaises(TypeError):self.execute()
        for exit_code in [0,1]:
            with self.assertRaises(IntegrityError):record_worker_exit(self.run,self.request,elapsed=.25,exit_code=exit_code,forced=False,cancellation_seconds=None)
        row=reconcile(self.run)['fixture']
        self.assertEqual(row['resource_seconds'],.25)
        self.assertEqual(sum(e['event']=='resource' for e in events(self.run)),1)
        with self.assertRaises(IntegrityError):reserve(self.run,self.request)
        self.incident(error)

    def test_supervisor_rejects_legacy_swallowed_model_error_even_exit_zero(self):
        append(self.run,'admitted','fixture')
        terminal(self.run,'fixture',{'request_id':'fixture','finish_reason':'model_error',
                                  'model_error':'TypeError: bad configuration','parsed':{'native_score':0.0}})
        with self.assertRaises(IntegrityError):record_worker_exit(self.run,self.request,elapsed=.25,exit_code=0,forced=False,cancellation_seconds=None)
        self.assertEqual(reconcile(self.run)['fixture']['resource_seconds'],.25)
        with self.assertRaises(IntegrityError):reserve(self.run,self.request)

    def test_successful_generation_scores_normally(self):
        self.execute()
        result=reconcile(self.run)['fixture']['result']
        self.assertEqual(result['parsed']['native_score'],1.0)
        self.assertIsNone(result['model_error'])
        self.assertFalse((self.run/'incidents').exists())

    def test_deliberate_cancellation_retains_documented_zero(self):
        write_new(self.run/'cancel/fixture.json',{'reason':'deliberate_interruption'})
        self.behavior=lambda **kw:self.emit(kw,[ord('x')])
        self.execute()
        result=reconcile(self.run)['fixture']['result']
        self.assertEqual(result['finish_reason'],'controlled_interruption')
        self.assertEqual(result['parsed']['native_score'],0.0)
        self.assertIsNone(result['model_error'])

    def test_known_timeout_retains_valid_output(self):
        write_new(self.run/'cancel/fixture.json',{'reason':'timeout'})
        self.execute()
        result=reconcile(self.run)['fixture']['result']
        self.assertEqual(result['finish_reason'],'timeout')
        self.assertEqual(result['parsed']['native_score'],1.0)

    def test_offline_correction_guard_before_backend_import_or_dispatch(self):
        path=self.root/'configs/phase_state.json'
        path.write_text(json.dumps({'active_phase':'P01','status':'IN_PROGRESS','real_dispatch_enabled':False}))
        with self.assertRaises(IntegrityError):self.execute()
        self.assertEqual(self.calls,0)
        with patch('taskcognition.p01_smoke.subprocess.Popen') as process, self.assertRaises(IntegrityError):
            run_job(self.root,'fixture')
        process.assert_not_called()


if __name__=='__main__':unittest.main()
