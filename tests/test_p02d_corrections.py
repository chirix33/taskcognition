"""Deterministic real-filesystem publication and production stop/report tests."""
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from taskcognition import p02d_publication as pub
from taskcognition.artifacts import read_json
from taskcognition.contracts import IntegrityError
from taskcognition.p02d_runner import ProcessWorker,supervise_session,execute
from taskcognition.p02d_ledger import append,scan,dispatch,recover,BudgetStop
from taskcognition.p02d_reporting import report
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan
from taskcognition.contracts import file_hash
from test_p02d import ROOT,Clock,FakeWorker,module

class Publication(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def paused(self,writer,reader,before,after):
        entered=threading.Event();release=threading.Event();errors=[];link=os.link
        def commit(src,dst):
            # File is closed and fsynced; actual final namespace still absent.
            self.assertTrue(Path(src).name.endswith('.pending'))
            read_json(src)
            entered.set()
            if not release.wait(10):raise TimeoutError('test synchronization')
            link(src,dst)
        def run():
            try:writer()
            except BaseException as e:errors.append(e)
        with patch.object(pub.os,'link',commit):
            thread=threading.Thread(target=run);thread.start()
            try:
                self.assertTrue(entered.wait(10))
                for _ in range(3):before(reader())
            finally:release.set();thread.join(10)
        self.assertFalse(thread.is_alive());self.assertEqual(errors,[])
        after(reader())
    def test_ready_result_and_command_visibility(self):
        worker=ProcessWorker.__new__(ProcessWorker);worker.directory=self.root
        slot={'slot_id':'feature_000','request_hash':'a'*64}
        for name,writer,reader,value in (
            ('ready',lambda:pub.write_new(self.root/'ready.json',{'load_seconds':2}),worker.ready,{'load_seconds':2}),
            ('command',lambda:worker.send(slot),lambda:pub.read_optional(self.root/'commands/feature_000.json'),slot),
            ('result',lambda:pub.write_new(self.root/'results/feature_000.json',slot),lambda:worker.result(slot),slot)):
            with self.subTest(channel=name):
                self.paused(writer,reader,lambda x:self.assertIsNone(x),lambda x:self.assertEqual(x,value))
    def test_first_ledger_and_admission_visible_as_complete_prefix(self):
        self.paused(lambda:append(self.root,'session_start',session_id='s',stage='feature'),lambda:scan(self.root),
            lambda x:self.assertEqual(len(x['events']),0),lambda x:self.assertEqual(len(x['events']),1))
        self.paused(lambda:append(self.root,'dispatch',session_id='s',slot_id='f',request_hash='h',output_reservation=0,input_positions=1),lambda:scan(self.root),
            lambda x:self.assertEqual(len(x['slots']),0),lambda x:self.assertEqual(x['slots']['f']['state'],'UNKNOWN_ADMISSION'))
        self.paused(lambda:append(self.root,'admitted',session_id='s',slot_id='f'),lambda:scan(self.root),
            lambda x:self.assertEqual(x['slots']['f']['state'],'UNKNOWN_ADMISSION'),lambda x:self.assertEqual(x['slots']['f']['state'],'ADMITTED'))
    def test_controls_incident_resource_and_finish_publication(self):
        worker=ProcessWorker.__new__(ProcessWorker);worker.directory=self.root
        slot={'slot_id':'f'}
        for path,writer,value in [
            ('cancel/f.json',lambda:worker.cancel(slot),{'reason':'timeout'}),
            ('finish.json',worker.finish,{'stop':True}),
            ('incident.json',lambda:pub.write_new(self.root/'incident.json',{'scored':False}),{'scored':False}),
            ('session_resources/s.json',lambda:pub.write_new(self.root/'session_resources/s.json',{'seconds':2}),{'seconds':2})]:
            self.paused(writer,lambda:pub.read_optional(self.root/path),lambda x:self.assertIsNone(x),lambda x:self.assertEqual(x,value))
    def test_no_clobber_interruption_and_committed_corruption(self):
        p=self.root/'ready.json';pub.write_new(p,{'load_seconds':2});old=p.read_bytes()
        with self.assertRaises(FileExistsError):pub.write_new(p,{'load_seconds':99})
        self.assertEqual(p.read_bytes(),old)
        append(self.root,'session_start',session_id='s',stage='feature')
        append(self.root,'dispatch',session_id='s',slot_id='f',request_hash='h',output_reservation=0,input_positions=1)
        with patch.object(pub.os,'link',side_effect=InterruptedError('before commit')):
            with self.assertRaises(InterruptedError):append(self.root,'admitted',session_id='s',slot_id='f')
        self.assertEqual(scan(self.root)['slots']['f']['state'],'UNKNOWN_ADMISSION')
        with self.assertRaises(IntegrityError):recover(self.root)
        # Abandoned pre-commit file is not a ledger member.
        (self.root/'ledger/.000002.json.abandoned.pending').write_text('{')
        self.assertEqual(len(scan(self.root)['events']),2)
        worker=ProcessWorker.__new__(ProcessWorker);worker.directory=self.root
        for bad in ('{','null'):
            p.write_text(bad)
            with self.assertRaises((ValueError,IntegrityError)):worker.ready()
        (self.root/'ledger/000002.json').write_text('{')
        with self.assertRaises(IntegrityError):scan(self.root)
    def test_process_crash_before_commit_does_not_publish(self):
        # Actual lightweight child exits with prepared file still present. No model.
        code="from pathlib import Path; import os; from taskcognition.p02d_publication import _prepare; _prepare(Path(__import__('sys').argv[1]),{'ok':True}); os._exit(23)"
        p=subprocess.run([sys.executable,'-c',code,str(self.root/'ready.json')],capture_output=True)
        self.assertEqual(p.returncode,23,p.stderr)
        self.assertIsNone(pub.read_optional(self.root/'ready.json'))
        self.assertEqual(len(list(self.root.glob('*.pending'))),1)

class StopClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plan=module.candidate(ROOT)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.run=self.root/RUN;self.clock=Clock()
        shutil.copytree(ROOT/PLAN_DIR,self.root/PLAN_DIR)
    def tearDown(self):self.tmp.cleanup()
    def run_worker(self,kind,monitor=None):
        return supervise_session(self.root,self.plan,self.plan['feature_schedule'],'a'*64,0,
            worker_factory=lambda *a:kind(*a,clock=self.clock),clock=self.clock,sleep=self.clock.sleep,monitor=monitor)
    def assert_stopped(self,completed):
        state=scan(self.run);r=report(self.root,self.plan)
        self.assertEqual(r['status'],'STOPPED_INCOMPLETE');self.assertEqual(r['incidents'],[])
        self.assertFalse(state['unknown_residency']);self.assertEqual(len(state['operational_stops']),1)
        self.assertEqual(len(r['feature_measurements']),completed)
        self.assertEqual(read_json(self.run/'session_resources/features.json')['classification'],'OPERATIONAL_STOP')
        self.assertTrue(all(c['targets'] is None for c in r['clusters']))
        before=state['measured_residency_seconds']
        with self.assertRaises(IntegrityError):recover(self.run)
        with self.assertRaises(IntegrityError):dispatch(self.run,self.plan,self.plan['requests'][0],'features')
        self.assertEqual(scan(self.run)['measured_residency_seconds'],before)
    def test_within_session_reservation_stop_keeps_valid_first_measurement(self):
        class Costly(FakeWorker):
            def result(self,slot):self.clock.t+=751;return super().result(slot)
        with self.assertRaises(BudgetStop):self.run_worker(Costly)
        self.assert_stopped(1)
    def test_monitored_deadline_known_stopped_slot_is_unscored(self):
        class Slow(FakeWorker):
            def result(self,slot):self.clock.t+=121;return None
        with self.assertRaises(BudgetStop):self.run_worker(Slow)
        self.assert_stopped(0)
        self.assertEqual(set(report(self.root,self.plan)['consumed_slots'].values()),{'STOPPED_UNSCORED'})
    def test_safe_loader_deadline_is_operational_not_software_failure(self):
        class Loading(FakeWorker):
            def ready(self):self.clock.t+=151;return None
        with self.assertRaisesRegex(BudgetStop,'loader deadline'):self.run_worker(Loading)
        self.assert_stopped(0)
        self.assertEqual(set(report(self.root,self.plan)['consumed_slots'].values()),{'STOPPED_UNSCORED'})
    def test_monitored_resource_stop_and_corrupt_resource_dominance(self):
        def monitor(worker):raise BudgetStop('fixture measured resource stop')
        with self.assertRaises(BudgetStop):self.run_worker(FakeWorker,monitor)
        self.assert_stopped(0)
        (self.run/'session_resources/features.json').write_text('{}')
        self.assertEqual(report(self.root,self.plan)['status'],'INTEGRITY_INCIDENT')
    def test_budget_with_unsafe_cleanup_is_integrity_incident(self):
        class Unsafe(FakeWorker):
            def result(self,slot):self.clock.t+=121;return None
            def kill(self):self.clock.t+=30
            def wait(self,timeout):self.clock.t+=timeout;raise TimeoutError('still active')
        with self.assertRaisesRegex(IntegrityError,'cleanup'):self.run_worker(Unsafe)
        self.assertEqual(report(self.root,self.plan)['status'],'INTEGRITY_INCIDENT')
        resource=read_json(self.run/'session_resources/features.json')
        self.assertEqual(resource['classification'],'INTEGRITY_INCIDENT');self.assertFalse(resource['safe_stopped'])
    def test_budget_with_corrupt_ledger_retains_independent_cost_incident(self):
        def monitor(worker):
            (self.run/'ledger/000000.json').write_text('{')
            raise BudgetStop('resource stop concurrent with corrupt evidence')
        with self.assertRaises(IntegrityError):self.run_worker(FakeWorker,monitor)
        self.assertEqual(report(self.root,self.plan)['status'],'INTEGRITY_INCIDENT')
        self.assertGreater(read_json(self.run/'session_resources/features.json')['seconds'],0)
        self.assertTrue((self.run/'incidents/features.json').exists())
    def test_orphan_stop_after_crash_blocks_recovery_without_recharge(self):
        pub.write_new(self.run/'operational_stops/features.json',{'classification':'OPERATIONAL_STOP'})
        with self.assertRaises(IntegrityError):recover(self.run)
        with self.assertRaises(IntegrityError):dispatch(self.run,self.plan,self.plan['requests'][0],'features')
        r=report(self.root,self.plan)
        self.assertEqual(r['status'],'INTEGRITY_INCIDENT')
        self.assertEqual(r['research_resources']['measured_residency_seconds'],0)
    def test_outer_stop_closes_dispatch_and_never_starts_answers(self):
        class Slow(FakeWorker):
            def result(self,slot):self.clock.t+=121;return None
        pub.write_new(self.root/'configs/phase_state.json',dict(active_phase='P02D',status='EXECUTION_AUTHORIZED',real_dispatch_enabled=True))
        def supervised(root,plan,slots,sha,start,**kw):
            return supervise_session(root,plan,slots,sha,0,worker_factory=lambda *a:Slow(*a,clock=self.clock),clock=self.clock,sleep=self.clock.sleep)
        with patch('taskcognition.p02d_runner.require_authorization',return_value=self.plan),patch('taskcognition.p02d_runner.supervise_session',side_effect=supervised) as run:
            with self.assertRaises(BudgetStop):execute(self.root,'a'*64)
            self.assertEqual(run.call_count,1)
        self.assert_stopped(0)
        self.assertFalse(read_json(self.root/'configs/phase_state.json')['real_dispatch_enabled'])
        self.assertEqual(read_json(self.run/'supervisor_stop.json')['classification'],'OPERATIONAL_STOP')
        self.assertFalse(read_json(self.run/'execution_end.json')['all_planned_executed'])

class PendingEntrypoints(unittest.TestCase):
    def test_superseded_v2_plan_rejected_by_prospective_verifier(self):
        for version in ('v2','v3'):
            path=ROOT/f'artifacts/development/p02d-cr01-plan-{version}/run_plan.json'
            with self.assertRaisesRegex(IntegrityError,'superseded'):verify_plan(ROOT,path,file_hash(path))
    def test_parent_and_child_reject_before_model_library_import(self):
        code="""import sys,runpy
class RejectModels:
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('torch','transformers'):raise AssertionError('MODEL IMPORT REACHED')
sys.meta_path.insert(0,RejectModels())
module=sys.argv.pop(1)
runpy.run_module(module,run_name='__main__')
"""
        for module_name,extra in [('taskcognition.p02d_runner',[]),('taskcognition.p02d_worker',['--session','features','--stage','feature'])]:
            p=subprocess.run([sys.executable,'-c',code,module_name,'--root',str(ROOT),'--plan-hash','0'*64,*extra],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertIn('pending',p.stderr);self.assertNotIn('MODEL IMPORT REACHED',p.stderr)
        self.assertFalse((ROOT/RUN).exists())

if __name__=='__main__':unittest.main()
