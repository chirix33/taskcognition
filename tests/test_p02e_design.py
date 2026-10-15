"""Focused offline checks of the P02E analysis, not a final audit or simulation."""
import importlib.util,json,math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('p02e_analyze',ROOT/'scripts/p02e_analyze.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class P02EDesignChecks(unittest.TestCase):
 def test_range_and_zero_variance_anchor(self):
  self.assertAlmostEqual(a.radius(24,0),.3742341475188051)
  self.assertGreater(a.radius(24,0),.3125)
  self.assertAlmostEqual(a.radius(24,0,2),2*.3742341475188051)
 def test_zero_harm_retains_full_Z_range(self):
  alpha=.05;v=.2078804347826087;n=1200
  self.assertAlmostEqual(a.radius(n,alpha*alpha*v,1),alpha*math.sqrt(2*v*math.log(40)/n)+a.A/(n-1))
  self.assertGreater(a.radius(n,alpha*alpha*v,1),a.radius(n,alpha*alpha*v,alpha))
 def test_formula_rejects_invalid_inputs(self):
  for args in [(1,0,1),(24,-1,1),(24,0,-1),(24,float('nan'),1)]:
   with self.assertRaises(ValueError):a.radius(*args)
 def test_cluster_contract_example_and_incomplete_rejection(self):
  item=dict(input_id='fixture',family='fixture',dataset_index=0)
  obs=[dict(mode=m,draw_index=i,native_score=s,strict_valid_final=True,worker_seconds=1,generation_seconds=.5)
   for m,ss in [('D',[1,1,1,0]),('R',[1,1,0,0])] for i,s in enumerate(ss)]
  r=a.summarize_cluster(item,obs)
  self.assertEqual((r['benefit'],r['joint_spoilage'],r['direct_redraw'],r['decline_010'],r['decline_025']),(-.25,.375,.25,.375,.375))
  with self.assertRaises(ValueError):a.summarize_cluster(item,obs[:-1])
  obs[0]['native_score']=1.001
  with self.assertRaises(ValueError):a.summarize_cluster(item,obs)
 def test_fixed_rules_zero_exposure_and_concentration(self):
  rows=a.read(ROOT/'reports/p02e/cluster_rows.json')['rows']
  result={n:a.diagnostic_rule(n,rows) for n in ['always_D','always_R','observed_positive_benefit','complement_positive_benefit']}
  self.assertIsNone(result['always_D']['conditional_spoilage']);self.assertIsNone(result['always_D']['kish_concentration'])
  self.assertEqual(result['observed_positive_benefit']['weighted_exposure_B'],.0625)
  self.assertEqual(result['observed_positive_benefit']['kish_concentration'],2)
  self.assertEqual(result['complement_positive_benefit']['raw_nested_direct_successes'],24)
  self.assertAlmostEqual(result['always_R']['kish_concentration'],7.894736842105263)
 def test_no_cost_double_charge(self):
  parts=a.cost_partition(100,20,40,1,2,115)
  self.assertEqual(parts['unallocated_within_residency'],37)
  self.assertEqual(parts['outside_residency_in_execution_wall'],15)
  self.assertEqual(sum(parts[k] for k in ['load_components','generation_and_forward_components','cpu_feature_component','cleanup_components','unallocated_within_residency','outside_residency_in_execution_wall']),115)
  with self.assertRaises(ValueError):a.cost_partition(100,80,40,1,2,115)
 def test_recorded_totals_and_full_outcome_retention(self):
  rows=a.read(ROOT/'reports/p02e/cluster_rows.json')['rows'];cost=a.read(ROOT/'reports/p02e/cost_reconciliation.json')
  self.assertEqual(len(rows),24);self.assertEqual(sum(len(c['scores_D'])+len(c['scores_R']) for c in rows),192)
  self.assertEqual(sum(c['direct_perfect_count'] for c in rows),30)
  self.assertEqual(sum(c['benefit']>0 for c in rows),11);self.assertEqual(sum(c['joint_spoilage'] for c in rows),0)
  self.assertEqual(cost['sessions'],193);self.assertEqual(cost['known_output_tokens'],129371)
  self.assertAlmostEqual(sum(cost['partition'][k] for k in ['load_components','generation_and_forward_components','cpu_feature_component','cleanup_components','unallocated_within_residency']),11560.2217413,places=6)
 def test_analysis_bound_source_and_no_forbidden_imports(self):
  receipt=a.read(ROOT/'reports/p02e/analysis_run_receipt.json')
  self.assertEqual(receipt['source_sha256'],a.sha(ROOT/'scripts/p02e_analyze.py'))
  self.assertEqual(receipt['declaration_sha256'],a.sha(ROOT/'reports/p02e/analytical_declaration.json'))
  for m in ['torch','transformers','taskcognition.audit','taskcognition.p02d_runner']:self.assertNotIn(m,sys.modules)
  bindings=a.read(ROOT/'reports/p02e/acceptance_verification.json')
  for p,h in bindings['accepted_hashes'].items():self.assertEqual(a.sha(ROOT/p),h,p)
if __name__=='__main__':unittest.main()
