"""Focused mixed-cap, diagnostic and incomplete-evidence regression tests."""
import tempfile,unittest
from pathlib import Path
from taskcognition.artifacts import write_new,read_json
from taskcognition.contracts import IntegrityError,digest
from taskcognition.p01_ledger import append,terminal,reconcile
from taskcognition.p02b_runner import reserve,identity,finish_reason,require_real_dispatch
from taskcognition.p02b_reporting import inspect_ledger,primary_record,wrapper_subtype,diagnostic_payload,cell_summary

class MixedCapTests(unittest.TestCase):
    def q(self,i,cap):return dict(request_id=str(i),max_new_tokens=cap,effective_generation_config={'max_new_tokens':cap},stream_id=digest(i),split='DEVELOPMENT',evidence_kind='development_observation')
    def plan(self,qs):return {'requests':[dict(request_id=q['request_id'],request_hash=digest(q),cap=q['max_new_tokens']) for q in qs]}
    def complete(self,r,q):terminal(r,q['request_id'],dict(request_id=q['request_id']));append(r,'resource',q['request_id'],seconds=1)
    def test_all_48_mixed_reservations_and_unknown_no_replay(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);qs=[self.q(i,(1024,2048)[i%2]) for i in range(49)];p=self.plan(qs)
            for q in qs[:47]:reserve(r,q,p);self.complete(r,q)
            reserve(r,qs[47],p)
            self.assertEqual(sum(x['reserved_output_tokens'] for x in reconcile(r).values()),73728)
            with self.assertRaisesRegex(IntegrityError,'no replay'):reserve(r,qs[47],p)
            with self.assertRaisesRegex(IntegrityError,'budget'):reserve(r,qs[48],p)
    def test_cap_specific_budget_and_config_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);qs=[self.q(i,2048) for i in range(25)];p=self.plan(qs)
            for q in qs[:24]:reserve(r,q,p);self.complete(r,q)
            with self.assertRaisesRegex(IntegrityError,'cap-specific'):reserve(r,qs[24],p)
        with tempfile.TemporaryDirectory() as td:
            q=self.q(0,2048);q['effective_generation_config']['max_new_tokens']=1024
            with self.assertRaisesRegex(IntegrityError,'effective cap'):reserve(Path(td),q,self.plan([q]))
    def test_finish_detection_at_both_caps(self):
        for cap in (1024,2048):
            self.assertEqual(finish_reason(None,None,cap,cap),'cap')
            self.assertEqual(finish_reason(None,999,cap,cap),'eos')
            self.assertEqual(finish_reason('timeout',None,cap-1,cap),'timeout')
            with self.assertRaises(IntegrityError):finish_reason(None,None,cap+1,cap)
        self.assertEqual(finish_reason(None,None,1024,2048),'other')
        self.assertEqual(finish_reason(None,None,1500,2048),'other')
    def test_cap_mode_draw_package_and_stream_identity(self):
        ids=[identity({'x':1},m,c,'input',d) for c in (1024,2048) for m in ('D','R') for d in (0,1)]
        self.assertEqual(len({p for p,s in ids}),4);self.assertEqual(len({s for p,s in ids}),8)
    def test_old_phases_refused_even_when_enabled(self):
        for phase in ('P01','P02A','P02','P03'):
            with tempfile.TemporaryDirectory() as td:
                r=Path(td);write_new(r/'configs/phase_state.json',dict(active_phase=phase,status='IN_PROGRESS',real_dispatch_enabled=True))
                with self.assertRaises(IntegrityError):require_real_dispatch(r)

class PartialReportingTests(unittest.TestCase):
    def test_actual_report_script_unknown_and_unexecuted_no_model(self):
        import runpy,sys,io
        from types import ModuleType,SimpleNamespace
        from unittest.mock import patch
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);(r/'scripts').mkdir()
            script=r/'scripts/p02b_report.py';script.write_bytes((root/'scripts/p02b_report.py').read_bytes())
            run=r/'artifacts/development/p02b-two-cap'
            qs=[dict(request_id=k,family='number_sorting',mode='D',cap=1024) for k in ('unknown','not_run')]
            write_new(run/'run_plan.json',dict(requests=qs,bound_files={}))
            for q in qs:write_new(run/'requests'/f'{q["request_id"]}.json',q)
            append(run,'dispatch','unknown',request_hash=digest(qs[0]),stream_id=digest('stream'),max_new_tokens=1024)
            append(run,'resource','unknown',seconds=3)
            write_new(r/'configs/phase_state.json',dict(active_phase='P02B',real_dispatch_enabled=False))
            write_new(r/'reports/p01/model_download.json',dict(local_directory='mock'))
            fake=ModuleType('transformers');fake.AutoTokenizer=SimpleNamespace(from_pretrained=lambda *a,**k:None)
            with patch.dict(sys.modules,{'transformers':fake}),patch('sys.stdout',new_callable=io.StringIO):runpy.run_path(str(script),run_name='__main__')
            result=read_json(r/'reports/p02b/resources.json')
            self.assertEqual(result['status'],'BLOCKED');self.assertEqual(result['retained'],0)
            self.assertEqual(result['unexecuted'],['not_run']);self.assertEqual(result['dispatched_without_retained_result'],['unknown'])
            self.assertEqual(result['conservative_gpu_residency_seconds'],3)
    def test_forced_record_without_parsed_and_unexecuted(self):
        q=dict(request_id='q',family='number_sorting',mode='D',cap=2048)
        result=dict(request_id='q',finish_reason='supervisor_forced_termination',forced_termination=True,native_score=0.,valid_retainable_output=False)
        row=primary_record(q,{'result':result});self.assertEqual(row['native_score'],0);self.assertIsNone(row['output_tokens'])
        self.assertIsNone(primary_record(q,{'result':None}))
        p={'requests':[q,dict(q,request_id='not_run')]};inspection=dict(chain_complete=True,rows={'q':{'resource_seconds':140}})
        cell=cell_summary(p,inspection,[dict(row,**q)],'number_sorting','D',2048)
        self.assertEqual((cell['planned'],cell['executed'],cell['retained'],cell['unexecuted']),(2,1,1,1))
    def test_missing_result_preserves_other_known_rows_without_zero(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)
            for k in ('good','missing','unknown'):
                append(r,'dispatch',k,request_hash=digest(k),stream_id=digest(k),max_new_tokens=1024)
                if k!='unknown':terminal(r,k,dict(request_id=k))
                append(r,'resource',k,seconds=7)
            (r/'results/missing.json').unlink()
            inspected=inspect_ledger(r)
            self.assertEqual(inspected['rows']['good']['state'],'COMPLETE')
            self.assertEqual(inspected['rows']['missing']['state'],'RESULT_INTEGRITY_INCIDENT')
            self.assertIsNone(inspected['rows']['missing']['result']);self.assertEqual(sum(x['resource_seconds'] for x in inspected['rows'].values()),21)
            self.assertTrue(inspected['incidents'])
    def test_unexplained_nonstandard_result_is_incident(self):
        with self.assertRaises(IntegrityError):primary_record({},dict(result={'native_score':0,'request_id':'q'}))
    def test_missing_tags_and_outside_prose_are_distinct(self):
        p=dict(failure_flags=['outer_wrapper_failure'],final_channel='[1,2]')
        self.assertEqual(wrapper_subtype(p),'missing_both_tags')
        self.assertEqual(diagnostic_payload('number_sorting',p)['payload'],'[1,2]')
        p['final_channel']='Explanation <FINAL>[1,2]</FINAL> trailing'
        self.assertEqual(wrapper_subtype(p),'forbidden_outside_prose')
        d=diagnostic_payload('number_sorting',p);self.assertEqual(d['payload'],'[1,2]');self.assertFalse(d['changes_primary_score'])
    def test_no_diagnostic_selection_from_ambiguous_or_thinking_text(self):
        for p in [dict(final_channel=None),dict(final_channel='<FINAL>1</FINAL><FINAL>2</FINAL>'),dict(final_channel='The answer is 3 because ...')]:
            self.assertIsNone(diagnostic_payload('letter_counting',p))

if __name__=='__main__':unittest.main()
