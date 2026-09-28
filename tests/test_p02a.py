"""Offline native scorer, channel, scope and supervisor failure checks."""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from taskcognition.artifacts import write_new
from taskcognition.contracts import IntegrityError,digest
from taskcognition.p01_ledger import append,reconcile
from taskcognition.p01_parsing import parse_and_score
from taskcognition.p02_native import native_dataset,syntax,gate_record,ENTRIES
from taskcognition.p02_runner import reserve,envelope_check,supervise,require_real_dispatch

ROOT=Path(__file__).resolve().parents[1]

def scorer_cases():
    return {
      'number_sorting':({'answer':"['1', '3']",'metadata':{'direction':'ascending'}},[("['1','3']",1.),("['2','4']",1.),("['2.01','4.01']",0.),("['3','1']",0.),('bad',0.)]),
      'number_format':({'metadata':{'solution':12.0}},[('12',1.),('12.009',1.),('12.011',0.),('wrong',0.)]),
      'letter_counting':({'answer':'3'},[('3',1.),('4',0.),('33',.5),('bad',0.)]),
      'graph_color':({'metadata':{'puzzle':{'vertices':[0,1],'edges':[(0,1)],'color_options':[1,2]}}},[('{"0":1,"1":2}',1.),('{"0":1,"1":1}',.01),('{}',.01),('bad',0.)]),
      'shortest_path':({'answer':'right right','metadata':{'matrix':[['*','O','#'],['O','O','O']]}},[('right right',1.),('down right right up',.5),('left',0.),('bad',0.)]),
      'knights_knaves':({'answer':'Alice is a knight, and Bob is a knave.'},[('Alice is a knight, Bob is a knave',1.),('Alice is a knight, Bob is a knight',0.3+0.7/2),('Alice is a knave, Bob is a knight',0.),('bad',0.)])}

class NativeTests(unittest.TestCase):
    def test_native_hand_checked_scores_and_precision(self):
        for family,(entry,cases) in scorer_cases().items():
            ds=native_dataset(ROOT,family,dict(seed=710000,size=1))
            for payload,score in cases:
                with self.subTest(family=family,payload=payload):self.assertEqual(ds.score_answer(payload,entry),score)
    def test_each_native_syntax_and_channel_boundary(self):
        for family,(entry,cases) in scorer_cases().items():
            ds=native_dataset(ROOT,family,dict(seed=710000,size=1));payload=cases[0][0]
            fn=lambda text:parse_and_score(text,'R',False,'eos',lambda p:ds.score_answer(p,entry),lambda p:syntax(family,p))
            self.assertTrue(fn('<think>private</think><FINAL>'+payload+'</FINAL>')['strict_valid_final'])
            self.assertFalse(fn('<think><FINAL>'+payload+'</FINAL></think>bare')['strict_valid_final'])
            self.assertFalse(fn('<think>x</think><FINAL>'+payload+'</FINAL>tail')['strict_valid_final'])
    def test_native_partial_scores_survive_parser(self):
        for family,(entry,cases) in scorer_cases().items():
            ds=native_dataset(ROOT,family,dict(seed=710000,size=1))
            for payload,score in cases:
                if 0<score<1:
                    row=parse_and_score('<FINAL>'+payload+'</FINAL>','D',False,'eos',lambda p:ds.score_answer(p,entry),lambda p:syntax(family,p))
                    self.assertEqual(row['native_score'],score);self.assertFalse(row['perfect_correct'])
    def test_gate_no_metadata(self):
        self.assertEqual(set(gate_record('id','text')),{'input_id','text','observables'})

class BoundaryTests(unittest.TestCase):
    def request(self):return dict(request_id='q',stream_id='a'*64,split='DEVELOPMENT',evidence_kind='development_observation',max_new_tokens=1024)
    def test_no_replay_and_plan_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td);q=self.request();plan={'requests':[{'request_id':'q','request_hash':digest(q)}]}
            reserve(run,q,plan)
            with self.assertRaises(IntegrityError):reserve(run,q,plan)
    def test_scope_and_unplanned_request(self):
        for field,value in [('split','TRAIN'),('max_new_tokens',2048),('evidence_kind','fixture')]:
            with tempfile.TemporaryDirectory() as td:
                q=self.request();q[field]=value
                with self.assertRaises(IntegrityError):reserve(Path(td),q,{'requests':[{'request_id':'q','request_hash':digest(q)}]})
    def test_budget_reserves_cleanup(self):
        envelope_check(5100,6900,496*1024**2)
        for values in [(5100.001,0,0),(0,6900.001,0),(0,0,496*1024**2+1)]:
            with self.assertRaises(IntegrityError):envelope_check(*values)
    def test_p01_state_cannot_authorize_p02(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);write_new(root/'configs/phase_state.json',dict(active_phase='P01',status='IN_PROGRESS',real_dispatch_enabled=True))
            with self.assertRaises(IntegrityError):require_real_dispatch(root)
    def test_supervisor_monitor_error_kills_waits_charges_once(self):
        with tempfile.TemporaryDirectory() as td:
            run=Path(td);q=self.request();append(run,'dispatch','q',request_hash=digest(q),stream_id=q['stream_id'],max_new_tokens=1024)
            children=[]
            def fail(child):children.append(child);raise OSError('injected monitoring evidence failure')
            with self.assertRaisesRegex(OSError,'injected'):
                supervise(run,q,[sys.executable,'-c','import time; time.sleep(20)'],os.environ.copy(),monitor=fail)
            self.assertIsNotNone(children[0].poll())
            row=reconcile(run)['q'];self.assertTrue(row['resource_recorded']);self.assertEqual(row['state'],'UNKNOWN_ADMISSION')
            self.assertFalse((run/'results/q.json').exists());self.assertTrue((run/'incidents/q_supervisor.json').exists())

if __name__=='__main__':unittest.main()
