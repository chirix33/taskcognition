"""Package actual execution evidence once, after offline report and local commit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time,zipfile
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import canonical,file_hash
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_execution';run=root/RUN
start=time.perf_counter();cpu=time.process_time()
sha='c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365'
verify_plan(root,root/PLAN_DIR/'run_plan.json',sha)
state=read_json(root/'configs/phase_state.json');assert state['real_dispatch_enabled'] is False
assert not state['p02_sealed'] and not state['p03_started']
assert read_json(out/'process_after.json')['p02d_processes']==[]
baseline=read_json(out/'preflight.json')['expected_artifact_hashes']
for n,h in baseline.items():assert file_hash(root/n)==h,n
paths={p for base in (run,out) for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
paths.update(root.glob('scripts/p02d_execution_*.py'))
for n in ['reports/phases/P02D_execution_completion.md','configs/p02d_execution_authorization.json','configs/phase_state.json',
 'configs/state_events/020_P02D_v4_preflight_accepted.json','configs/state_events/021_P02D_v4_execution_authorized.json',
 'configs/state_events/022_P02D_v4_execution_review_checkpoint.json','configs/state_snapshots/P02D_v4_before_execution_authorization.json',
 'configs/state_snapshots/P02D_v4_runner_exit_state.json',PLAN_DIR+'/run_plan.json',PLAN_DIR+'/environment.json',
 PLAN_DIR+'/feature_specification.json',PLAN_DIR+'/inputs.json',PLAN_DIR+'/answer_schedule.json',PLAN_DIR+'/feature_schedule.json',
 'reports/p02d_correction_v4/P02D_packet_receipt.json','reports/p02d_correction_v4/plan_receipt.json','scripts/p01_command.py']:
 paths.add(root/n)
exclude={'P02D_execution_review_packet.zip','P02D_execution_evidence_index.json','P02D_execution_packet_receipt.json'}
paths={p for p in paths if not (p.parent==out and p.name in exclude)}
assert all('.venv' not in p.parts and '.venv-inference' not in p.parts and not p.name.endswith('.safetensors') for p in paths)
files={p.relative_to(root).as_posix():file_hash(p) for p in sorted(paths)}
index=out/'P02D_execution_evidence_index.json'
write_new(index,dict(evidence_kind='development_observation',phase='P02D',files=files,plan_sha256=sha,
 source_commit='b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4',evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 unchanged_preflight_reference=dict(zip_sha256=baseline['reports/p02d_correction_v4/P02D_corrected_preflight_review_packet.zip'],
 index_sha256=baseline['reports/p02d_correction_v4/P02D_evidence_index.json'],indexed_files=661,
 note='Unchanged source, native adapters, all questions/tokenizations/packages and dependency source snapshots remain in the verified preflight packet. Not duplicated here.'),
 exclusions='No weights/environments/secrets/unrelated private files. Index/ZIP/external receipt excluded from child hashes to avoid circularity. All actual raw execution files included.'))
packet=out/'P02D_execution_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in files:z.write(root/n,n)
 z.write(index,index.relative_to(root).as_posix())
with zipfile.ZipFile(packet) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)+1
 for n,h in files.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
summary=read_json(out/'execution_accounting.json')
receipt=dict(evidence_kind='development_observation',status='PASS',timestamp_utc=datetime.now(timezone.utc).isoformat(),
 indexed_files=len(files),all_zip_members_verified=True,zip_sha256=file_hash(packet),zip_bytes=packet.stat().st_size,index_sha256=file_hash(index),
 completion_sha256=file_hash(root/'reports/phases/P02D_execution_completion.md'),production_report_sha256=file_hash(out/'production_execution_report.json'),
 accounting_sha256=file_hash(out/'execution_accounting.json'),plan_sha256=sha,authorization_sha256=file_hash(root/'configs/p02d_execution_authorization.json'),
 evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),source_commit=summary['source_commit'],
 packaging_wall_seconds=time.perf_counter()-start,packaging_cpu_process_seconds=time.process_time()-cpu,
 execution_evidence_bytes_including_packet=0,evidence_ceiling_bytes=536870912,evidence_overshoot_bytes=0,
 real_dispatch_enabled=False,p02_sealed=False,p03_started=False,production_status=summary['status'],
 counts=summary['counts'],worker_residency_seconds=summary['worker_residency_seconds'],unknown_residency=summary['unknown_residency'],
 backup='Verified local raw evidence and local ZIP only. No push, upload, remote backup or remote query in this task; off-machine coverage unverified.',
 receipt_location='External to ZIP on the same workstation, not an off-machine backup',
 scalar_tariff_beta_hard_support_adopted=False,new_gates=0,new_simulations=0,new_final_labels=0)
additional=[root/'reports/phases/P02D_execution_completion.md',root/'configs/p02d_execution_authorization.json',
 root/'configs/state_events/020_P02D_v4_preflight_accepted.json',root/'configs/state_events/021_P02D_v4_execution_authorized.json',
 root/'configs/state_events/022_P02D_v4_execution_review_checkpoint.json',root/'configs/state_snapshots/P02D_v4_before_execution_authorization.json',
 root/'configs/state_snapshots/P02D_v4_runner_exit_state.json']
base=sum(p.stat().st_size for b in (run,out) for p in b.rglob('*') if p.is_file())+sum(p.stat().st_size for p in additional)
for _ in range(8):
 receipt['execution_evidence_bytes_including_packet']=base+len(canonical(receipt))+1
 receipt['evidence_overshoot_bytes']=max(0,receipt['execution_evidence_bytes_including_packet']-536870912)
if receipt['evidence_overshoot_bytes']:receipt['status']='EVIDENCE_LIMIT_EXCEEDED'
write_new(out/'P02D_execution_packet_receipt.json',receipt)
print(json.dumps({k:receipt[k] for k in ['status','indexed_files','zip_sha256','index_sha256','completion_sha256','zip_bytes','execution_evidence_bytes_including_packet','evidence_overshoot_bytes','evidence_commit']},indent=2))
