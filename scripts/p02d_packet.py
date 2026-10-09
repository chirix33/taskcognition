"""Compact local review packet; excludes actual inference environment/weights."""
from pathlib import Path
import hashlib,subprocess,zipfile,json
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical
from taskcognition.p02d_plan import PLAN_DIR,RUN

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d'
state=read_json(root/'configs/phase_state.json')
assert state['active_phase']=='P02D' and state['status']=='READY_FOR_REVIEW' and not state['real_dispatch_enabled']
assert not (root/RUN).exists()
paths=set()
for base in [out,root/PLAN_DIR,root/'src/taskcognition',root/'tests',root/'vendor/reasoning_gym_p02a']:
    paths.update(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
paths.update(root.glob('scripts/p02d_*.py'))
for n in ['.gitattributes','AGENTS.md','README.md','pyproject.toml','configs/p01_requirements.lock','configs/p01_resource_plan.json',
    'docs/P02D_RUNNER_CONTRACT.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/ARCHITECTURE_AND_DATA.md','docs/STATISTICAL_CONTRACT.md',
    'docs/DECISIONS_AND_GAPS.md','docs/EVIDENCE_AND_MANUSCRIPT.md','docs/amendments/CR01_2026-10-05_v1.md',
    'configs/phase_state.json','configs/state_events/015_P02C_accept_P02D_offline.json','configs/state_events/016_P02D_preflight_review_checkpoint.json',
    'configs/state_snapshots/P02C_accepted_before_P02D.json','configs/state_snapshots/P02D_before_preflight_checkpoint.json',
    'configs/state_events/017_P02D_preflight_v2_review_checkpoint.json','configs/state_snapshots/P02D_preflight_v1_before_v2.json',
    'reports/phases/P02C_accepted_checkpoint.md','reports/phases/P02D_preflight_completion.md','reports/decision_ledger.md',
    'reports/p02c/P02C_review_packet.zip','reports/p02c/P02C_evidence_index.json','reports/p02c/P02C_packet_receipt.json',
    'reports/phases/P02C_completion.md','reports/p02c/next_development_proposal.md','reports/p02a/adapter_contracts.md',
    'reports/p02b/runtime_preflight.json','reports/p01/model_download.json','artifacts/development/p02b-two-cap/package_base.json','scripts/p01_command.py']:
    paths.add(root/n)
exclude={'P02D_preflight_review_packet.zip','P02D_evidence_index.json','P02D_packet_receipt.json'}
paths={p for p in paths if not (p.parent==out and p.name in exclude)}
assert all('.venv' not in p.parts and '.venv-inference' not in p.parts and not p.name.endswith('.safetensors') for p in paths)
index={p.relative_to(root).as_posix():file_hash(p) for p in sorted(paths)}
idx=out/'P02D_evidence_index.json'
write_new(idx,dict(evidence_kind='development_observation',phase='P02D',status='PREFLIGHT_READY_FOR_REVIEW',files=index,
    evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
    plan_sha256=read_json(out/'plan_receipt.json')['sha256'],
    exclusions='This index, packet, external receipt excluded from child index to avoid cycles; weights/environments/secrets/unrelated user material excluded. Installed runtime source hashes are bound in plan; Qwen source/tokenizer and native source snapshots plus exact dependencies suffice for source review, not a full inference environment.'))
packet=out/'P02D_preflight_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in index:z.write(root/n,n)
    z.write(idx,idx.relative_to(root).as_posix())
with zipfile.ZipFile(packet) as z:
    assert z.testzip() is None and len(z.namelist())==len(index)+1
    for n,h in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
receipt=dict(evidence_kind='development_observation',status='PASS',phase='P02D_PREFLIGHT',indexed_files=len(index),
    zip_sha256=file_hash(packet),zip_bytes=packet.stat().st_size,index_sha256=file_hash(idx),
    completion_sha256=file_hash(root/'reports/phases/P02D_preflight_completion.md'),plan_sha256=read_json(out/'plan_receipt.json')['sha256'],
    execution_request_sha256=file_hash(out/'execution_request.md'),P02C_external_receipt_sha256=file_hash(out/'P02C_external_packet_receipt.json'),
    source_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),verified_all_zip_members=True,
    real_dispatch_enabled=False,new_model_loads=0,new_answer_generations=0,new_feature_forwards=0,new_gpu_measurements=0,new_simulations=0,
    historical_admitted=75,historical_output_tokens=40555,backup='verified local packet; user-reported earlier P02C push consistent with local tracking; no remote restore or complete raw off-machine verification',
    preparation_report_and_plan_bytes=0)
base=sum(p.stat().st_size for b in (out,root/PLAN_DIR) for p in b.rglob('*') if p.is_file())
for _ in range(5):receipt['preparation_report_and_plan_bytes']=base+len(canonical(receipt))+1
write_new(out/'P02D_packet_receipt.json',receipt)
print(json.dumps(receipt,indent=2))
