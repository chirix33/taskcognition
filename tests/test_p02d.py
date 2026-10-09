"""Production preflight/worker boundaries with CPU tensors, fake workers/clocks."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import torch
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import IntegrityError,digest,file_hash
from taskcognition.p02d_features import cheap_features,masked_pool,decoder_feature,validate_gate_input,forward_schedule,gate_vector
from taskcognition.p02d_plan import PLAN_DIR,RUN,LIMITS,validate_plan,require_authorization,verify_plan
from taskcognition.p02d_ledger import append,scan,recover,dispatch,check_envelope,BudgetStop
from taskcognition.p02d_runner import execute,supervise_session,validate_result
from taskcognition.p02d_reporting import report

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publish',ROOT/'scripts/p02d_publish.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Features(unittest.TestCase):
    def test_swallowed_generation_callback_error_propagates_unscored(self):
        from taskcognition.p02d_worker import generate_answer
        class Backend:
            def generate(self,**kwargs):
                kwargs['streamer'].put(torch.tensor([[1]]))
                try:kwargs['streamer'].put(object())
                except AttributeError:pass  # Simulate a backend swallowing a broken callback.
                return torch.tensor([[1,2]])
        cpu_torch=SimpleNamespace(tensor=lambda data,**kw:torch.tensor(data,dtype=kw['dtype']),long=torch.long,
            ones_like=torch.ones_like,manual_seed=lambda _:None,cuda=SimpleNamespace(manual_seed_all=lambda _:None),inference_mode=torch.inference_mode)
        cfg=SimpleNamespace(from_dict=lambda _:object())
        request={'input_ids':[1],'effective_generation_config':{},'sampling_seed':1}
        with self.assertRaises(AttributeError):generate_answer(Backend(),None,request,Path('absent'),cpu_torch,cfg,object,list)
    def test_post_norm_decoder_and_masked_float32_pool(self):
        class Fake:
            def eval(self):self.evaluating=True
            def model(self,**kwargs):
                assert kwargs['use_cache'] is False and kwargs['past_key_values'] is None
                assert not torch.is_grad_enabled()
                # These are post-norm output values; masked padded token cannot leak.
                return SimpleNamespace(last_hidden_state=torch.tensor([[[1.,3.],[3.,7.],[99.,99.]]],dtype=torch.bfloat16),past_key_values=None)
        model=Fake();out=decoder_feature(model,torch.tensor([[1,2,0]]),torch.tensor([[1,1,0]]),2)
        self.assertTrue(model.evaluating);self.assertEqual(out.dtype,torch.float32);self.assertEqual(out.tolist(),[2.,5.])
    def test_shape_nonfinite_empty_mask_rejected(self):
        cases=[(torch.zeros(1,2,3),torch.ones(1,2),2),(torch.tensor([[[float('nan')]]]),torch.ones(1,1),1),
               (torch.ones(1,2,2),torch.zeros(1,2),2),(torch.ones(1,2,2),torch.tensor([[1.,.5]]),2)]
        for hidden,mask,width in cases:
            with self.subTest(width=width),self.assertRaises(IntegrityError):masked_pool(hidden,mask,width)
    def test_cheap_unicode_line_rules_and_allowlist(self):
        text='A) JSON 12\r\n B. text\u2028C. list number\nD) ٣ + ='
        row=dict(input_id='join',text=text,token_ids=[1,2],observables=cheap_features(text,[1,2]))
        self.assertEqual(row['observables']['choice_marker_count'],3)
        self.assertEqual(row['observables']['ascii_digit_count'],2)
        self.assertEqual(row['observables']['operator_count'],2)
        validate_gate_input(row)
        for key in ('family','gold','filename','trace','score','latent'):
            with self.assertRaises(IntegrityError):validate_gate_input(dict(row,**{key:'forbidden'}))
        with self.assertRaises(IntegrityError):gate_vector(row,[float('inf')],1)

class Plan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plan=module.candidate(ROOT)
    def test_fixed_selection_counts_streams_and_three_lengths(self):
        validate_plan(self.plan)
        self.assertEqual(sum(q['cap'] for q in self.plan['requests']),393216)
        fs=forward_schedule(self.plan['inputs']);self.assertEqual(len(fs),50)
        self.assertEqual(sum(q['kind']=='warmup' for q in fs),2)
        self.assertEqual(sum(q['input_positions'] for q in fs),6597)
    def test_bad_cap_scope_schedule_or_recipe_rejected(self):
        for mutate in (lambda p:p['caps'].update(D=1024),lambda p:p.update(phase='P02B'),
                       lambda p:p['requests'].pop(),lambda p:p['feature_schedule'].pop(),
                       lambda p:p['feature_specification'].update(pooling='last token')):
            p=copy.deepcopy(self.plan);mutate(p)
            with self.assertRaises(IntegrityError):validate_plan(p)
    def test_pending_authorization_rejects_before_worker(self):
        with patch('taskcognition.p02d_runner.ProcessWorker') as factory:
            with self.assertRaisesRegex(IntegrityError,'pending'):execute(ROOT,'0'*64,worker_factory=factory)
            factory.assert_not_called()
    def test_hash_and_authorization_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'plan.json';write_new(path,self.plan)
            with self.assertRaisesRegex(IntegrityError,'hash'):verify_plan(root,path,'0'*64)
            write_new(root/'configs/phase_state.json',dict(active_phase='P02D',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True))
            with self.assertRaisesRegex(IntegrityError,'missing authorization'):require_authorization(root,path,file_hash(path))
            write_new(root/'configs/p02d_execution_authorization.json',dict(authorized=True))
            with self.assertRaisesRegex(IntegrityError,'state binding'):require_authorization(root,path,file_hash(path))
    def test_authorized_but_wrong_cap_rejected_before_factory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);plan=copy.deepcopy(self.plan);plan['caps']['R']=1024
            path=root/PLAN_DIR/'run_plan.json';write_new(path,plan);sha=file_hash(path)
            auth=root/'configs/p02d_execution_authorization.json'
            write_new(auth,dict(phase='P02D',plan_sha256=sha,authorized=True,user_message_reference='FIXTURE ONLY',limits=LIMITS))
            write_new(root/'configs/phase_state.json',dict(active_phase='P02D',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True,
                p02d_plan_sha256=sha,p02d_authorization_sha256=file_hash(auth)))
            with patch('taskcognition.p02d_runner.ProcessWorker') as factory:
                with self.assertRaisesRegex(IntegrityError,'caps'):execute(root,sha,worker_factory=factory)
                factory.assert_not_called()

class Clock:
    def __init__(self):self.t=0.
    def __call__(self):return self.t
    def sleep(self,s):self.t+=s

class FakeWorker:
    def __init__(self,root,sid,stage,plan_hash,clock,fail=False):
        self.root=root;self.clock=clock;self.code=None;self.current=None;self.fail=fail;self.killed=False;self.waited=False
        clock.t+=2
    def poll(self):return self.code
    def ready(self):return {'load_seconds':2}
    def incident(self):return False
    def send(self,slot):self.current=slot;self.clock.t+=.1
    def result(self,slot):
        if self.fail:raise RuntimeError('injected evidence monitor error')
        row=read_json(self.root/PLAN_DIR/'gate_inputs'/f'{slot["input_id"]}.json')
        return dict(slot_id=slot['slot_id'],request_hash=slot['request_hash'],status='OK',dtype='float32',
            gate=gate_vector(row,[0.]*4096),input_positions=slot['input_positions'],forward_seconds=.1,cpu_feature_seconds=.001)
    def finish(self):self.code=0
    def kill(self):self.killed=True;self.code=-1
    def wait(self,timeout):self.waited=True;return self.code
    def close(self):pass

class LedgerAndSupervisor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plan=module.candidate(ROOT)
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.run=self.root/RUN;self.clock=Clock()
        import shutil
        shutil.copytree(ROOT/PLAN_DIR,self.root/PLAN_DIR)
    def tearDown(self):self.temp.cleanup()
    def test_feature_stage_all_50_one_cost_and_no_replay(self):
        workers=[]
        def factory(*args):
            w=FakeWorker(*args,clock=self.clock);workers.append(w);return w
        state=supervise_session(self.root,self.plan,self.plan['feature_schedule'],'a'*64,0,worker_factory=factory,clock=self.clock,sleep=self.clock.sleep)
        self.assertEqual(len(state['slots']),50);self.assertEqual(len(state['sessions']),1)
        self.assertAlmostEqual(state['measured_residency_seconds'],7)
        self.assertTrue(workers[0].waited)
        recover(self.run)
        with self.assertRaises(IntegrityError):dispatch(self.run,self.plan,self.plan['feature_schedule'][0],'features')
        before=scan(self.run)['measured_residency_seconds'];recover(self.run);self.assertEqual(scan(self.run)['measured_residency_seconds'],before)
    def test_monitor_error_stops_child_and_preserves_cost_without_score(self):
        workers=[]
        def factory(*args):
            w=FakeWorker(*args,clock=self.clock,fail=True);workers.append(w);return w
        with self.assertRaises(RuntimeError):supervise_session(self.root,self.plan,self.plan['feature_schedule'],'a'*64,0,worker_factory=factory,clock=self.clock,sleep=self.clock.sleep)
        state=scan(self.run);self.assertTrue(workers[0].killed and workers[0].waited)
        self.assertEqual(len(state['slots']),1);self.assertIsNone(next(iter(state['slots'].values()))['result'])
        self.assertGreater(state['measured_residency_seconds'],0)
        with self.assertRaises(IntegrityError):recover(self.run)
    def test_unknown_dispatch_recovery_and_corruption_fail_closed(self):
        append(self.run,'session_start',session_id='features',stage='feature')
        dispatch(self.run,self.plan,self.plan['feature_schedule'][0],'features')
        append(self.run,'heartbeat',session_id='features',seconds=4)
        with self.assertRaises(IntegrityError):recover(self.run)
        self.assertEqual(scan(self.run)['measured_residency_seconds'],4)
        (self.run/'ledger/000001.json').write_text('{}')
        with self.assertRaises(IntegrityError):recover(self.run)
        self.assertTrue(scan(self.run,tolerant=True)['incidents'])
    def test_rejected_restart_closes_authorized_state_without_recharge(self):
        write_new(self.root/'configs/phase_state.json',dict(active_phase='P02D',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True))
        append(self.run,'session_start',session_id='features',stage='feature')
        dispatch(self.run,self.plan,self.plan['feature_schedule'][0],'features')
        append(self.run,'heartbeat',session_id='features',seconds=3)
        with patch('taskcognition.p02d_runner.require_authorization',return_value=self.plan):
            with self.assertRaises(IntegrityError):execute(self.root,'a'*64)
        self.assertFalse(read_json(self.root/'configs/phase_state.json')['real_dispatch_enabled'])
        self.assertEqual(scan(self.run)['measured_residency_seconds'],3)
    def test_feature_stage_wall_overshoot_persisted_and_blocks_answers(self):
        write_new(self.root/'configs/phase_state.json',dict(active_phase='P02D',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True))
        with patch('taskcognition.p02d_runner.require_authorization',return_value=self.plan), \
             patch('taskcognition.p02d_runner.supervise_session') as supervisor, \
             patch('taskcognition.p02d_runner.time.perf_counter',side_effect=[0,1,1302,1303]):
            with self.assertRaises(BudgetStop):execute(self.root,'a'*64)
            self.assertEqual(supervisor.call_count,1)
        wall=read_json(self.run/'feature_stage_wall.json')
        self.assertEqual(wall['seconds'],1301);self.assertEqual(wall['overshoot_seconds'],101)
        self.assertFalse(read_json(self.root/'configs/phase_state.json')['real_dispatch_enabled'])
    def test_cumulative_and_feature_sublimits(self):
        state=dict(sessions={'prior':dict(ended=True,seconds=14000,stage='answer')})
        with self.assertRaises(BudgetStop):check_envelope(self.plan,state,'answer',0,0,active_seconds=101)
        with self.assertRaises(BudgetStop):check_envelope(self.plan,dict(sessions={}), 'feature',0,0,active_seconds=751)
        with self.assertRaises(BudgetStop):check_envelope(self.plan,dict(sessions={}), 'answer',17800,0)
        with self.assertRaises(BudgetStop):check_envelope(self.plan,dict(sessions={}), 'answer',0,260*1024**2)
    def test_partial_feature_blocks_answers(self):
        append(self.run,'session_start',session_id='answer_000',stage='answer')
        with self.assertRaisesRegex(IntegrityError,'feature stage'):dispatch(self.run,self.plan,self.plan['requests'][0],'answer_000')
    def test_feature_timeout_and_cleanup_failure_never_admit_answers(self):
        class Slow(FakeWorker):
            def result(self,slot):self.clock.t+=121;return None
        with self.assertRaises(BudgetStop):
            supervise_session(self.root,self.plan,self.plan['feature_schedule'],'a'*64,0,
                worker_factory=lambda *a:Slow(*a,clock=self.clock),clock=self.clock,sleep=self.clock.sleep)
        state=scan(self.run);self.assertEqual(len(state['slots']),1);self.assertGreater(state['measured_residency_seconds'],120)
        with self.assertRaises(IntegrityError):recover(self.run)
    def test_cleanup_failure_keeps_unknown_cost_and_stops(self):
        class Unstoppable(FakeWorker):
            def result(self,slot):raise RuntimeError('monitor failed')
            def kill(self):self.clock.t+=30
            def wait(self,timeout):self.clock.t+=timeout;raise TimeoutError('cannot establish stopped state')
        with self.assertRaisesRegex(IntegrityError,'cleanup'):
            supervise_session(self.root,self.plan,self.plan['feature_schedule'],'a'*64,0,
                worker_factory=lambda *a:Unstoppable(*a,clock=self.clock),clock=self.clock,sleep=self.clock.sleep)
        state=scan(self.run);self.assertTrue(state['unknown_residency']);self.assertGreater(state['measured_residency_seconds'],60)
        with self.assertRaises(IntegrityError):recover(self.run)
    def test_complete_cluster_uses_existing_targets_partial_is_not_filled(self):
        # Synthetic ledger records only: no worker/model is invoked.
        iid=self.plan['inputs'][0]['input_id'];group=[q for q in self.plan['requests'] if q['input_id']==iid]
        scores={'D':[1,1,1,0],'R':[1,1,0,0]}
        for q in group:
            sid=q['slot_id'];append(self.run,'session_start',session_id=sid,stage='answer')
            append(self.run,'dispatch',session_id=sid,slot_id=sid,request_hash=q['request_hash'],output_reservation=2048,input_positions=0)
            append(self.run,'admitted',session_id=sid,slot_id=sid)
            score=scores[q['mode']][q['draw_index']]
            value=dict(slot_id=sid,request_id=sid,request_hash=q['request_hash'],package_hash=q['package_hash'],stream_id=q['stream_id'],
                generated_tokens=1,raw_token_ids=[1],generation_seconds=1,finish_reason='eos',
                parsed=dict(native_score=score,perfect_correct=score==1,strict_valid_final=True,status='perfect' if score else 'wrong',failure_flags=[]))
            p=self.run/'results'/f'{sid}.json';write_new(p,value)
            append(self.run,'result',session_id=sid,slot_id=sid,path=p.relative_to(self.run).as_posix(),sha256=file_hash(p))
            append(self.run,'session_end',session_id=sid,seconds=2,cleanup_seconds=.1,safe_stopped=True,exit_code=0)
        r=report(self.root,self.plan);c=r['clusters'][0];self.assertTrue(c['complete_K4'])
        self.assertEqual(c['targets']['benefit'],-.25);self.assertEqual(c['targets']['joint_spoilage'],.375)
        self.assertEqual(c['targets']['direct_redraw'],.25);self.assertEqual(c['targets']['decline_010'],.375)
        self.assertIsNone(r['clusters'][1]['targets'])
        # A corrupted last result must not turn into a ninth fabricated draw/zero.
        p.write_text('{}');r=report(self.root,self.plan)
        self.assertFalse(r['clusters'][0]['complete_K4']);self.assertTrue(r['incidents'])
    def test_empty_and_corrupt_partial_report_has_no_fabricated_targets(self):
        r=report(self.root,self.plan);self.assertEqual(len(r['cells']),12);self.assertEqual(len(r['clusters']),24)
        self.assertTrue(all(c['targets'] is None for c in r['clusters']))
        append(self.run,'session_start',session_id='features',stage='feature')
        dispatch(self.run,self.plan,self.plan['feature_schedule'][0],'features')
        r=report(self.root,self.plan);self.assertTrue(r['research_resources']['unknown_residency'])
        self.assertEqual(sum(c['retained'] for c in r['cells']),0)

if __name__=='__main__':unittest.main()
