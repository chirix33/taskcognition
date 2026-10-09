"""Read-only production plan checks and preservation checks; no model work."""
from pathlib import Path
import hashlib,json,zipfile,subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,digest,IntegrityError
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan
from taskcognition.p02d_runner import execute
from taskcognition.p02d_reporting import report

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d'
receipt=read_json(out/'plan_receipt.json');plan=verify_plan(root,root/receipt['plan_path'],receipt['sha256'])
assert not (root/RUN).exists(),'no actual run directory permitted in preflight'
try:execute(root,receipt['sha256'])
except IntegrityError as exc:
    assert 'pending separate authorization' in str(exc);rejection=str(exc)
else:raise AssertionError('pending execution accepted')
assert not (root/RUN).exists()
old=read_json(root/'reports/p02c/P02C_evidence_index.json')['files'];changes=[]
allowed={'README.md','configs/phase_state.json','reports/decision_ledger.md'}
with zipfile.ZipFile(root/'reports/p02c/P02C_review_packet.zip') as z:
    assert z.testzip() is None
    for n,h in old.items():
        assert hashlib.sha256(z.read(n)).hexdigest()==h,n
        if file_hash(root/n)!=h:
            assert n in allowed,n
            changes.append(n)
accepted=read_json(out/'acceptance_verification.json')['accepted_hashes']
for n,h in accepted.items():assert file_hash(root/n)==h,n
for n,h in read_json(root/'reports/source_inventory.json')['preserved_original_files'].items():assert file_hash(root/n)==h,n
assert file_hash(root/'reference/TaskCognition_Revised_Verified.pdf')=='9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8'
for n,h in read_json(root/'reports/p02b/P02B_evidence_index.json')['files'].items():
    if n.startswith(('src/','tests/','artifacts/')):assert file_hash(root/n)==h,n
environment=plan['environment'];modeldir=root/environment['model_directory']
for n,h in environment['tokenizer_metadata_verified'].items():assert file_hash(modeldir/n)==h,n
state=read_json(root/'configs/phase_state.json');assert state['active_phase']=='P02D' and state['real_dispatch_enabled'] is False
assert not (root/'configs/p02d_execution_authorization.json').exists()
empty=report(root,plan)
assert len(empty['cells'])==12 and all(c['executed']==c['retained']==0 for c in empty['cells'])
assert len(empty['clusters'])==24 and all(c['targets'] is None for c in empty['clusters'])
write_new(out/'unexecuted_plan_report.json',dict(empty,report_role='pre-dispatch planned denominators only; no empirical outputs'))
write_new(out/'verification.json',dict(evidence_kind='development_observation',status='PASS',plan_sha256=receipt['sha256'],
    bound_files_verified=len(plan['bound_files']),P02C_snapshot_files_verified=len(old),accepted_hashes_preserved=True,
    documented_current_changes=changes,original_pdf_and_manuscript_preserved=True,historical_source_tests_raw_unchanged=True,
    production_pending_rejection=rejection,run_directory_absent=True,authorization_record_absent=True,
    input_count=24,answer_slots=192,feature_slots=50,strictly_unique_streams=len({q['stream_id'] for q in plan['requests']}),
    new_model_loads=0,new_forwards=0,new_generations=0,new_gpu_measurements=0,new_simulations=0,
    historical_admitted_generations=75,historical_output_tokens=40555,P01_interruption='separate historical diagnostic',
    source_import='src/taskcognition/p02d_plan.py',runtime='.venv-inference/Scripts/python.exe with PYTHONPATH=src'))
print(json.dumps(read_json(out/'verification.json')))
