import json
from pathlib import Path
import tempfile
import unittest
from taskcognition.contracts import IntegrityError,digest
from taskcognition.artifacts import write_new
from taskcognition.p01_ledger import reserve,reconcile,append,terminal,events
from taskcognition.p01_parsing import parse_and_score


class ParserTests(unittest.TestCase):
    def parse(self,text,mode='R',opening=True,finish='eos',score=1.0):
        return parse_and_score(text,mode,opening,finish,lambda _:score)
    def test_prompt_open_native_delimiter(self):
        r=self.parse("compute</think>\n<FINAL>['1','2']</FINAL>")
        self.assertTrue(r['perfect_correct'])
        self.assertEqual(r['thinking'],'compute')
    def test_generated_open_delimiter(self):
        self.assertTrue(self.parse("<think>compute</think><FINAL>[1]</FINAL>",opening=False)['strict_valid_final'])
    def test_missing_required_close_never_accepts_thought_as_answer(self):
        r=self.parse('<FINAL>[1]</FINAL>')
        self.assertEqual(r['status'],'native_delimiter_failure')
        self.assertIsNone(r['final_channel'])
    def test_missing_open_in_nonprefilled_context(self):
        self.assertEqual(self.parse('x</think><FINAL>[1]</FINAL>',opening=False)['status'],'native_delimiter_failure')
    def test_duplicate_native_delimiters_rejected(self):
        for text in ('<think>x</think><FINAL>[1]</FINAL>', 'x</think></think><FINAL>[1]</FINAL>'):
            self.assertEqual(self.parse(text)['status'],'native_delimiter_failure')
    def test_final_tags_in_thought_not_authoritative(self):
        r=self.parse('<FINAL>[9]</FINAL></think><FINAL>[1]</FINAL>')
        self.assertEqual(r['final_payload'],'[1]')
        self.assertEqual(self.parse('<FINAL>[9]</FINAL></think>')['status'],'outer_wrapper_failure')
    def test_empty_duplicate_case_and_trailing_text(self):
        for body in ('<FINAL></FINAL>','<FINAL> \n </FINAL>','<FINAL>[1]</FINAL><FINAL>[2]</FINAL>',
                     '<final>[1]</final>','<FINAL>[1]</FINAL>extra','preamble<FINAL>[1]</FINAL>'):
            with self.subTest(body=body):self.assertEqual(self.parse(body,mode='D')['status'],'outer_wrapper_failure')
    def test_declared_ascii_whitespace(self):
        self.assertTrue(self.parse(' \t<FINAL> [1] </FINAL>\r\n',mode='D')['strict_valid_final'])
        self.assertFalse(self.parse('\u00a0<FINAL>[1]</FINAL>',mode='D')['strict_valid_final'])
    def test_malformed_native_payload(self):
        for p in ('word','{}','[]','[true]','["NaN"]','[1,,2]'):
            self.assertEqual(self.parse('<FINAL>'+p+'</FINAL>',mode='D')['status'],'native_syntax_failure')
    def test_partial_wrong_perfect_native_scores_retained(self):
        # Explicit scorer fixtures; number_sorting itself has binary native scores.
        for score,status in ((.375,'partial'),(0.,'wrong'),(1.,'perfect')):
            r=self.parse('<FINAL>[1]</FINAL>',mode='D',score=score)
            self.assertEqual((r['native_score'],r['status'],r['perfect_correct']),(score,status,score==1))
    def test_cap_without_final_and_valid_cap(self):
        r=self.parse('incomplete',finish='cap')
        self.assertIn('cap_without_valid_final',r['failure_flags'])
        self.assertTrue(self.parse('<FINAL>[1]</FINAL>',mode='D',finish='cap')['strict_valid_final'])
    def test_direct_cannot_emit_native_thinking(self):
        self.assertEqual(self.parse('<think></think><FINAL>[1]</FINAL>',mode='D')['status'],'native_delimiter_failure')
    def test_scorer_errors_not_zero(self):
        with self.assertRaises(IntegrityError):self.parse('<FINAL>[1]</FINAL>',mode='D',score=float('nan'))


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def request(self,key='one'):
        return {'evidence_kind':'development_observation','split':'DEVELOPMENT','request_id':key,
                'stream_id':digest(key),'max_new_tokens':1024}
    def test_never_dispatched_can_execute(self):
        self.assertEqual(reconcile(self.root),{})
        reserve(self.root,self.request())
    def test_unknown_admission_no_replay(self):
        reserve(self.root,self.request())
        self.assertEqual(reconcile(self.root)['one']['state'],'UNKNOWN_ADMISSION')
        with self.assertRaises(IntegrityError):reserve(self.root,self.request())
    def test_admitted_missing_response_no_replay(self):
        reserve(self.root,self.request())
        append(self.root,'admitted','one')
        self.assertEqual(reconcile(self.root)['one']['state'],'ADMITTED_NO_TERMINAL')
        with self.assertRaises(IntegrityError):reserve(self.root,self.request())
    def test_completed_immutable_result(self):
        reserve(self.root,self.request())
        append(self.root,'admitted','one')
        terminal(self.root,'one',{'request_id':'one','native_score':.5})
        self.assertEqual(reconcile(self.root)['one']['state'],'COMPLETE')
        with self.assertRaises(FileExistsError):terminal(self.root,'one',{'request_id':'one','native_score':1})
        with self.assertRaises(IntegrityError):reserve(self.root,self.request())
    def test_missing_or_corrupt_result_is_integrity_failure(self):
        reserve(self.root,self.request())
        terminal(self.root,'one',{'request_id':'one','native_score':0})
        path=self.root/'results/one.json'
        path.write_text('{}')
        with self.assertRaisesRegex(IntegrityError,'corrupted'):reconcile(self.root)
        path.unlink()
        with self.assertRaisesRegex(IntegrityError,'missing'):reconcile(self.root)
    def test_verified_preadmission_failure_no_retry_J0(self):
        reserve(self.root,self.request())
        append(self.root,'proven_nonadmission','one',proof='injected before generate entry; local executor never called')
        self.assertEqual(reconcile(self.root)['one']['state'],'PROVEN_NONADMISSION_NO_RETRY')
        with self.assertRaises(IntegrityError):reserve(self.root,self.request())
    def test_nonadmission_after_admission_rejected(self):
        reserve(self.root,self.request())
        append(self.root,'admitted','one')
        append(self.root,'proven_nonadmission','one',proof='invalid')
        with self.assertRaises(IntegrityError):reconcile(self.root)
    def test_global_eight_call_reservation(self):
        for i in range(8):reserve(self.root,self.request(str(i)))
        self.assertEqual(sum(r['reserved_output_tokens'] for r in reconcile(self.root).values()),8192)
        with self.assertRaises(IntegrityError):reserve(self.root,self.request('ninth'))
    def test_bad_split_reuse_and_bad_cap_rejected(self):
        for update in ({'split':'TEST'},{'max_new_tokens':2048}):
            with self.assertRaises(IntegrityError):reserve(self.root,{**self.request(),**update})
        reserve(self.root,self.request())
        with self.assertRaises(IntegrityError):reserve(self.root,{**self.request('two'),'stream_id':digest('one')})
    def test_hash_chain_tamper_rejected(self):
        reserve(self.root,self.request())
        append(self.root,'admitted','one')
        path=self.root/'events/000000.json'
        data=json.loads(path.read_text())
        data['max_new_tokens']=1
        path.write_text(json.dumps(data))
        with self.assertRaises(IntegrityError):events(self.root)
    def test_dispatched_cost_charged_once(self):
        reserve(self.root,self.request())
        append(self.root,'resource','one',seconds=2.5)
        self.assertEqual(reconcile(self.root)['one']['resource_seconds'],2.5)
        append(self.root,'resource','one',seconds=2.5)
        with self.assertRaises(IntegrityError):reconcile(self.root)

if __name__=='__main__':unittest.main()
