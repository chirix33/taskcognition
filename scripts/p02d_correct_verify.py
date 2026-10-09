"""Final v4 preservation/authority checks; no model imports or model work."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile,subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,IntegrityError,canonical
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan
from taskcognition.p02d_runner import execute
from taskcognition.p02d_reporting import report

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_correction_v4'
receipt=read_json(out/'plan_receipt.json');plan=verify_plan(root,root/receipt['plan_path'],receipt['sha256'])
baseline=read_json(out/'baseline_verification.json')
for n,h in baseline['accepted_hashes'].items():assert file_hash(root/n)==h,n
old=root/'artifacts/development/p02d-cr01-plan-v2';new=root/PLAN_DIR
same={p.relative_to(old).as_posix():file_hash(p) for p in old.rglob('*') if p.is_file() and p.name!='run_plan.json'}
assert len(same)==256
assert {p.relative_to(new).as_posix() for p in new.rglob('*') if p.is_file() and p.name!='run_plan.json'}==set(same)
for n,h in same.items():assert file_hash(new/n)==h,n
oldplan=read_json(old/'run_plan.json')
for key in ('package','inputs','requests','feature_schedule','feature_specification','environment','caps','limits','initial_counters','clocks','stop_rules','unresolved'):
 assert plan[key]==oldplan[key],key
allowed={'README.md','docs/P02D_RUNNER_CONTRACT.md','scripts/p02d_publish.py','configs/phase_state.json','reports/decision_ledger.md',
 *['src/taskcognition/p02d_'+n+'.py' for n in ('ledger','plan','reporting','runner','worker')]}
changed={}
index=read_json(root/'reports/p02d/P02D_evidence_index.json')['files']
with zipfile.ZipFile(root/'reports/p02d/P02D_preflight_review_packet.zip') as z:
 for n,h in index.items():
  assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  if file_hash(root/n)!=h:
   assert n in allowed,n
   changed[n]=dict(v2=h,v3=file_hash(root/n))
for n,h in read_json(root/'reports/p02b/P02B_evidence_index.json')['files'].items():
 if n.startswith(('src/','tests/','artifacts/')):assert file_hash(root/n)==h,n
for n,h in read_json(root/'reports/source_inventory.json')['preserved_original_files'].items():assert file_hash(root/n)==h,n
assert file_hash(root/'reference/TaskCognition_Revised_Verified.pdf')=='9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8'
assert not (root/RUN).exists() and not (root/'configs/p02d_execution_authorization.json').exists()
try:execute(root,receipt['sha256'])
except IntegrityError as e:assert 'pending' in str(e);rejection=str(e)
else:raise AssertionError('pending plan accepted')
state=read_json(root/'configs/phase_state.json');assert not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
empty=report(root,plan);assert empty['status']=='INCOMPLETE'
assert all(c['executed']==c['retained']==0 for c in empty['cells'])
write_new(out/'unexecuted_plan_report.json',dict(empty,report_role='unexecuted plan only; no observations'))
write_new(out/'preservation_verification.json',dict(status='PASS',plan_sha256=receipt['sha256'],bound_files_verified=len(plan['bound_files']),
 baseline_zip_files_verified=len(index),materialized_files_identical=same,version_linking_changes='run_plan.json only; directory binding/source hashes/timestamp/plan_version. No request, input, package, stream, schedule, environment or feature file changes.',
 baseline_current_changes=changed,historical_source_tests_and_original_pdf_preserved=True,pending_rejection=rejection,
 new_model_loads=0,new_gpu_calls=0,new_forwards=0,new_answer_generations=0,new_simulations=0,historical_admitted=75,historical_output_tokens=40555))
print(json.dumps(dict(status='PASS',plan_sha256=receipt['sha256'],materialized_identical=len(same),bound_files=len(plan['bound_files']),baseline_snapshot=len(index))))
