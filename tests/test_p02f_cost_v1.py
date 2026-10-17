"""CPU-only production prototype checks; synthetic clocks are not measurements."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from unittest.mock import patch
import json, os, subprocess, sys, tempfile, unittest
from taskcognition import p02f_cost_v1 as p
from taskcognition import p02d_publication as publication

ROOT=Path(__file__).resolve().parents[1]

class CostFixtureTests(unittest.TestCase):
    def setUp(self):
        parent=ROOT/'artifacts/fixtures'; parent.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(prefix='p02f-test-',dir=parent)
        self.root=Path(self.tmp.name)
        assert self.root.resolve().parent==parent.resolve()
    def tearDown(self): self.tmp.cleanup()
    def runq(self,**kw):
        return p.run_fixture(ROOT,self.root,'slot_000','D',kw.pop('worker',p.ScriptedWorker()),**kw)

    def test_both_live_entries_reject_all_authorization_states(self):
        valid=dict(phase='P02F',authorized=True,consumed=False,plan_sha256='a'*64)
        state=dict(active_phase='P02F',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True)
        for entry in (p.supervisor_entry,p.worker_entry):
            for auth in [None,dict(valid,phase='P02D'),dict(valid,consumed=True),dict(valid,plan_sha256='b'*64),valid]:
                with self.assertRaises(p.CostDesignBlocked): entry(authorization=auth,plan_hash='a'*64,state=state)
        self.assertNotIn('torch',sys.modules); self.assertNotIn('transformers',sys.modules)

    def test_real_cpu_subprocess_direct_child_and_supervisor_closed(self):
        # Import blocker records any attempted inference import, including failed imports.
        code="""import sys,runpy
class Block:
 def find_spec(self,name,*args):
  if name.split('.')[0] in ('torch','transformers','numpy'):
   raise AssertionError('FORBIDDEN_INFERENCE_IMPORT:'+name)
sys.meta_path.insert(0,Block())
sys.argv=['p02f','--role',sys.argv[1]]
runpy.run_module('taskcognition.p02f_cost_v1',run_name='__main__')
"""
        for role in ('supervisor','worker'):
            env=dict(os.environ,PYTHONPATH=str(ROOT/'src'))
            r=subprocess.run([sys.executable,'-c',code,role],cwd=ROOT,env=env,capture_output=True,text=True,timeout=15)
            self.assertNotEqual(r.returncode,0)
            self.assertIn('CostDesignBlocked',r.stderr)
            self.assertNotIn('FORBIDDEN_INFERENCE_IMPORT',r.stderr)

    def test_one_load_passes_answer_reseed_no_cache_and_stub_not_gate(self):
        w=p.ScriptedWorker(); r=self.runq(worker=w,warmups=2)
        self.assertEqual((r['loads'],r['feature_attempts'],r['answer_attempts']),(1,3,1))
        self.assertEqual(r['warmup_seconds'],2); self.assertTrue(r['warmups_in_elapsed'])
        names=[n for n,c in w.calls]; self.assertEqual(names[names.index('answer')-1],'reseed')
        f=next(c for n,c in w.calls if n=='feature'); a=next(c for n,c in w.calls if n=='answer')
        self.assertIsNone(f['past_key_values']);self.assertFalse(f['use_cache']);self.assertFalse(a['use_feature_cache'])
        self.assertNotEqual(f['input_buffer'],next(c for n,c in w.calls if n=='prompt')['input_buffer'])
        self.assertIsNone(r['head_cost_seconds']);self.assertFalse(r['learned_gate'])
        with self.assertRaises(p.CostDesignBlocked):p.reference_cost_from_diagnostic(r)

    def test_bypass_is_distinct_directly_exercised_fixture_path(self):
        r=self.runq(bypass=True)
        self.assertEqual((r['loads'],r['feature_attempts'],r['answer_attempts']),(1,0,1))
        self.assertFalse(r['all_in_reference_calibration'])
        self.assertTrue(r['bypass_path_directly_exercised'])

    def test_feature_error_stops_unscored_before_answer(self):
        r=self.runq(worker=p.ScriptedWorker(fault='feature'))
        self.assertEqual(r['status'],'INTEGRITY_INCIDENT');self.assertIsNone(r['primary_score'])
        self.assertEqual(r['answer_attempts'],0);self.assertGreater(r['accounting']['total_service_seconds'],0)
        with self.assertRaises(p.IntegrityError):p.run_fixture(ROOT,self.root,'slot_001','R',p.ScriptedWorker())

    def test_known_failure_and_known_timeout_retained_but_cleanup_dominates(self):
        for i,w in enumerate([p.ScriptedWorker(fault='known_model_failure'),p.ScriptedWorker(fault='known_timeout'),p.ScriptedWorker(fault='known_timeout',safe_stop=False)]):
            r=p.run_fixture(ROOT,self.root/str(i),'slot_000','R',w)
            if w.safe_stop:
                self.assertEqual(r['primary_score'],0);self.assertIsNotNone(r['accounting']['total_service_seconds'])
            else:
                self.assertEqual(r['status'],'INTEGRITY_INCIDENT');self.assertIsNone(r['primary_score'])
                self.assertIsNone(r['accounting']['total_service_seconds']);self.assertGreater(r['accounting']['incurred_lower_bound_seconds'],0)
        self.assertEqual(p.recover(self.root/'1')['stop_dispatch'],True)

    def test_reservations_exhaustion_and_declared_count_arithmetic(self):
        for i,kwargs in enumerate([dict(remaining_seconds=449),dict(remaining_tokens=2047),dict(warmups=2,remaining_seconds=689)]):
            w=p.ScriptedWorker();r=p.run_fixture(ROOT,self.root/str(i),'slot_000','D',w,**kwargs)
            self.assertEqual(r['status'],'STOPPED_INCOMPLETE');self.assertFalse(r['admitted'])
            self.assertNotIn('load',[n for n,c in w.calls]);self.assertGreater(r['accounting']['total_service_seconds'],0)
        self.assertEqual(24*2048,49152);self.assertEqual((24+2)*2048,53248)
        self.assertEqual(450-(150+120+120+10+30),20)
        self.assertEqual(690-(150+3*120+120+10+30),20)

    def test_no_replay_recovery_preserves_cost_once_and_unknown(self):
        r=self.runq();a=p.recover(self.root);b=p.recover(self.root)
        self.assertEqual(a,b);self.assertEqual(a['known_incurred_seconds'],r['accounting']['incurred_lower_bound_seconds'])
        with self.assertRaises(p.NoReplay):self.runq()
        p.publish(self.root/'slot_001/claim.json','claim','slot_001',dict(start_monotonic=0))
        a=p.recover(self.root);self.assertEqual(a['unknown_cost_slots'],['slot_001'])
        with self.assertRaises(p.IntegrityError):p.run_fixture(ROOT,self.root,'slot_002','D',p.ScriptedWorker())

    def test_cumulative_budget_and_rejection_cost_remain_charged(self):
        first=p.run_fixture(ROOT,self.root,'slot_000','D',p.ScriptedWorker(),remaining_seconds=465)
        stop=p.run_fixture(ROOT,self.root,'slot_001','R',p.ScriptedWorker(),remaining_seconds=465)
        self.assertEqual(stop['status'],'STOPPED_INCOMPLETE');self.assertFalse(stop['admitted'])
        self.assertAlmostEqual(p.recover(self.root)['known_incurred_seconds'],
            first['accounting']['observed_elapsed_seconds']+stop['accounting']['observed_elapsed_seconds'])
        with self.assertRaises(p.IntegrityError):p.run_fixture(ROOT,self.root,'slot_002','D',p.ScriptedWorker())

    def test_overshoot_and_nonoverlapping_nested_reconciliation(self):
        r=self.runq(worker=p.ScriptedWorker(answer_seconds=500))
        self.assertGreater(r['overshoot_seconds'],0)
        self.assertGreater(r['accounting']['total_service_seconds'],r['reservation_seconds'])
        # Injected duration deliberately exceeds policy: measurement cannot clip it.
        a=p.reconcile([dict(start=0,end=3,nested=[dict(start=1,end=2)])],0,5,True)
        self.assertEqual((a['exclusive_component_seconds'],a['unallocated_residual_seconds'],a['total_service_seconds']),(3,2,5))
        with self.assertRaises(p.IntegrityError):p.reconcile([dict(start=0,end=3),dict(start=2,end=4)],0,5,True)

    def test_actual_atomic_publication_request_result_control_and_prefix(self):
        real_link=publication.os.link
        for kind in ('claim','command','result','cancel','finish','resource','incident'):
            path=self.root/(kind+'.json');prepared=Event();release=Event()
            def paused(source,target):
                prepared.set()
                if not release.wait(5):raise RuntimeError('test synchronization timeout')
                return real_link(source,target)
            with patch.object(publication.os,'link',paused),ThreadPoolExecutor(max_workers=1) as pool:
                future=pool.submit(p.publish,path,kind,'slot_000',{'bytes':'x'*2000})
                try:
                    self.assertTrue(prepared.wait(5))
                    self.assertIsNone(p.read_record(path,kind,'slot_000'))
                    self.assertNotIn(path,list(self.root.glob('*.json')))
                finally:release.set()
                future.result(timeout=5)
            self.assertEqual(p.read_record(path,kind,'slot_000')['bytes'],'x'*2000)
            with self.assertRaises(FileExistsError):p.publish(path,kind,'slot_000',{})
        # Scan real fixture registry while next fully prepared claim is unpublished.
        self.runq();prepared=Event();release=Event()
        def pause_claim(source,target):
            prepared.set()
            if not release.wait(5):raise RuntimeError('test timeout')
            return real_link(source,target)
        with patch.object(publication.os,'link',pause_claim),ThreadPoolExecutor(max_workers=1) as pool:
            f=pool.submit(p.publish,self.root/'slot_001/claim.json','claim','slot_001',{})
            try:
                self.assertTrue(prepared.wait(5));self.assertEqual(p.recover(self.root)['consumed'],['slot_000'])
            finally:release.set()
            f.result(timeout=5)
        self.assertEqual(p.recover(self.root)['unresolved'],['slot_001'])

    def test_precommit_interruption_and_corrupt_committed_fail_closed(self):
        path=self.root/'interrupt.json'
        with patch.object(publication.os,'link',side_effect=InterruptedError('injected before commit')):
            with self.assertRaises(InterruptedError):p.publish(path,'command','slot_000',{})
        self.assertIsNone(p.read_record(path,'command','slot_000'))
        path.write_text('{',encoding='utf-8')
        with self.assertRaises(ValueError):p.read_record(path,'command','slot_000')
        self.runq();result=self.root/'slot_000/result.json'
        obj=json.loads(result.read_text());obj['payload']['primary_score']=999
        result.write_text(json.dumps(obj),encoding='utf-8')
        with self.assertRaises(p.IntegrityError):p.recover(self.root)

if __name__=='__main__':unittest.main()
