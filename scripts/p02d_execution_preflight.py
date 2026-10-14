"""Read-only reviewed-source checks plus disposable CPU publication precheck."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,platform,shutil,subprocess,tempfile,time,zipfile
from taskcognition.artifacts import read_json
from taskcognition.contracts import file_hash
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan
from taskcognition.p02d_publication import write_new,read_optional

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/p02d_execution'
SHA='c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365'
SOURCE='b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4'
start=time.perf_counter();stamp=datetime.now(timezone.utc).isoformat()
OUT.mkdir(exist_ok=True)
assert not (OUT/'preflight.json').exists(),'preflight already exists; inspect rather than replace'
assert not (ROOT/RUN).exists(),'prior run evidence exists; no launch permitted'
assert not (ROOT/'configs/p02d_execution_authorization.json').exists(),'existing authorization requires inspection'
expected={PLAN_DIR+'/run_plan.json':SHA,
 'reports/p02d_correction_v4/P02D_corrected_preflight_review_packet.zip':'1f3c8f0bc16d04416052550d21449665197325a0b3d8096e97d32ae3a9db6950',
 'reports/p02d_correction_v4/P02D_evidence_index.json':'ffbac753187f4ad21555c1506efb2af7611cce22f66635adbd116358ff8ad8dd',
 'reports/phases/P02D_corrected_preflight_completion.md':'38fea2199a540f136c12fabcace93ab8572bc1f42cac6abd71ac4894f4c0fe08',
 'reports/p02d_correction_v4/execution_request.md':'0d688444a8c584b2c811f163e6ad0be0380e287d5fdb0b1b3d28ff5610e291f0'}
for n,h in expected.items():assert file_hash(ROOT/n)==h,n
index=read_json(ROOT/'reports/p02d_correction_v4/P02D_evidence_index.json')['files']
with zipfile.ZipFile(ROOT/'reports/p02d_correction_v4/P02D_corrected_preflight_review_packet.zip') as z:
 assert z.testzip() is None and len(index)==661
 for n,h in index.items():
  assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  assert file_hash(ROOT/n)==h,n
assert subprocess.check_output(['git','rev-parse',SOURCE],text=True).strip()==SOURCE
plan=verify_plan(ROOT,ROOT/PLAN_DIR/'run_plan.json',SHA)
for n,h in plan['bound_files'].items():
 if n.startswith('src/'):
  assert hashlib.sha256(subprocess.check_output(['git','show',SOURCE+':'+n])).hexdigest()==h,n
assert file_hash(ROOT/'reference/TaskCognition_Revised_Verified.pdf')=='9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8'
state=read_json(ROOT/'configs/phase_state.json')
assert state['active_phase']=='P02D' and not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
tmp=ROOT/'tmp/p02d-execution-publication';tmp.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(dir=tmp) as td:
 p=Path(td)/'record.json';write_new(p,{'fixture':True,'model_work':0});assert read_optional(p)=={'fixture':True,'model_work':0}
 try:write_new(p,{'overwrite':True})
 except FileExistsError:pass
 else:raise AssertionError('no-clobber precheck failed')
 assert read_optional(p)=={'fixture':True,'model_work':0}
archive=OUT/'authority';archive.mkdir(exist_ok=False)
for n in ['docs/P02D_v4_acceptance_review.md','docs/P02D_v4_coordinator_checks.zip','docs/prompts/P02D_v4_execution_prompt_APPROVED.md']:
 shutil.copyfile(ROOT/n,archive/Path(n).name)
with zipfile.ZipFile(archive/'P02D_v4_coordinator_checks.zip') as z:
 coordinator_members={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith('/')}
write_new(OUT/'preflight.json',dict(evidence_kind='development_observation',status='PASS',timestamp_utc=stamp,completed_utc=datetime.now(timezone.utc).isoformat(),
 seconds=time.perf_counter()-start,expected_artifact_hashes=expected,indexed_zip_and_current_files_verified=661,bound_runtime_source_input_files_verified=len(plan['bound_files']),
 reviewed_source_commit=SOURCE,head_before_execution=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 source_import=str(__import__('taskcognition.p02d_plan',fromlist=['x']).__file__).replace(str(ROOT),'.'),
 interpreter='.venv-inference/Scripts/python.exe',platform=platform.platform(),publication_precheck='PASS: existing helper; actual Windows same-filesystem hard link; duplicate fails; disposable CPU fixture only',
 archive_hashes={p.name:file_hash(p) for p in archive.iterdir()},coordinator_bundle_member_hashes=coordinator_members,
 prior_authorization_absent=True,prior_run_directory_absent=True,prior_dispatch_false=True,new_model_work=0,
 preserved_user_files=['docs/P02D_v4_acceptance_review.md','docs/P02D_v4_coordinator_checks.zip','docs/prompts/P02D_v4_execution_prompt_APPROVED.md']))
print(json.dumps(dict(status='PASS',indexed_files=661,bound_files=len(plan['bound_files']),plan_sha256=SHA,seconds=time.perf_counter()-start)))
