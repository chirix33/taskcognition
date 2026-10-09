"""Package the corrected pending preflight; receipt remains outside the ZIP."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical
from taskcognition.p02d_plan import PLAN_DIR,RUN,verify_plan

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_correction_v4'
receipt=read_json(out/'plan_receipt.json');verify_plan(root,root/receipt['plan_path'],receipt['sha256'])
state=read_json(root/'configs/phase_state.json')
assert state['checkpoint']=='CORRECTED_PREFLIGHT' and state['status']=='READY_FOR_REVIEW'
assert not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
assert not (root/RUN).exists() and not (root/'configs/p02d_execution_authorization.json').exists()
paths=set()
for base in [out,root/'reports/p02d_correction_v3',root/PLAN_DIR,root/'artifacts/development/p02d-cr01-plan-v3',
             root/'src/taskcognition',root/'tests',root/'vendor/reasoning_gym_p02a']:
 paths.update(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
paths.update(root.glob('scripts/p02d_*.py'))
for n in ['AGENTS.md','README.md','.gitattributes','pyproject.toml','configs/p01_requirements.lock','scripts/p01_command.py',
 'docs/P02D_RUNNER_CONTRACT.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/STATISTICAL_CONTRACT.md','docs/ARCHITECTURE_AND_DATA.md',
 'docs/DECISIONS_AND_GAPS.md','docs/EVIDENCE_AND_MANUSCRIPT.md','docs/amendments/CR01_2026-10-05_v1.md',
 'reports/decision_ledger.md','configs/phase_state.json',
 'configs/state_events/018_P02D_corrected_preflight_v3_review_checkpoint.json','configs/state_events/019_P02D_corrected_preflight_v4_review_checkpoint.json',
 'configs/state_snapshots/P02D_preflight_v2_before_v3.json','configs/state_snapshots/P02D_preflight_v3_before_v4.json',
 'reports/phases/P02D_corrected_preflight_completion.md','reports/phases/P02D_preflight_completion.md',
 'reports/p02d/P02D_preflight_review_packet.zip','reports/p02d/P02D_evidence_index.json','reports/p02d/P02D_packet_receipt.json',
 'reports/p02d/P02C_external_packet_receipt.json','reports/p02d/execution_request.md','reports/p02c/next_development_proposal.md',
 'reports/p01/model_download.json','artifacts/development/p02b-two-cap/package_base.json',
 'artifacts/development/p02d-cr01-plan-v2/run_plan.json']:
 paths.add(root/n)
exclude={'P02D_corrected_preflight_review_packet.zip','P02D_evidence_index.json','P02D_packet_receipt.json'}
paths={p for p in paths if not (p.parent==out and p.name in exclude)}
assert all('.venv' not in p.parts and '.venv-inference' not in p.parts and not p.name.endswith('.safetensors') for p in paths)
files={p.relative_to(root).as_posix():file_hash(p) for p in sorted(paths)}
source_commit=read_json(out/'source_commits.json')['correction_source_evidence_commit']
idx=out/'P02D_evidence_index.json'
write_new(idx,dict(evidence_kind='development_observation',status='P02D_CORRECTED_PREFLIGHT_READY_FOR_REVIEW',files=files,
 source_commit=source_commit,plan_sha256=receipt['sha256'],
 exclusions='Index, ZIP, external receipt excluded from child hashes to avoid cycles. No weights/environments/secrets/unrelated material. Preserved v2 ZIP includes historical v1/P02C/P02B provenance.'))
packet=out/'P02D_corrected_preflight_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in files:z.write(root/n,n)
 z.write(idx,idx.relative_to(root).as_posix())
with zipfile.ZipFile(packet) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)+1
 for n,h in files.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
result=dict(status='PASS',checkpoint='P02D_CORRECTED_PREFLIGHT_READY_FOR_REVIEW',indexed_files=len(files),all_zip_members_verified=True,
 zip_sha256=file_hash(packet),zip_bytes=packet.stat().st_size,index_sha256=file_hash(idx),
 report_sha256=file_hash(root/'reports/phases/P02D_corrected_preflight_completion.md'),plan_sha256=receipt['sha256'],
 execution_request_sha256=file_hash(out/'execution_request.md'),source_diff_sha256=file_hash(out/'source_diff.patch'),
 source_commit=source_commit,baseline_packet_sha256=file_hash(root/'reports/p02d/P02D_preflight_review_packet.zip'),
 prior_external_P02C_receipt_sha256=file_hash(root/'reports/p02d/P02C_external_packet_receipt.json'),
 real_dispatch_enabled=False,p02_sealed=False,p03_started=False,execution_authorization_exists=False,
 new_model_loads=0,new_gpu_calls=0,new_feature_forwards=0,new_answer_generations=0,new_simulations=0,
 historical_admitted=75,historical_output_tokens=40555,
 backup='Verified local packet only. User corrected prior pushed claim to nothing pushed. Local tracking ancestry is not proof of a current push or remote backup; no remote query or transfer.',
 receipt_location='outside ZIP on the same workstation; external does not mean off-machine',preparation_bytes=0)
base=sum(p.stat().st_size for b in (out,root/'reports/p02d_correction_v3',root/PLAN_DIR,root/'artifacts/development/p02d-cr01-plan-v3') for p in b.rglob('*') if p.is_file())
for _ in range(5):result['preparation_bytes']=base+len(canonical(result))+1
write_new(out/'P02D_packet_receipt.json',result)
print(json.dumps(result,indent=2))
