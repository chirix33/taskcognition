"""Build a local review ZIP and independently re-read every indexed byte."""
import hashlib, json, subprocess, zipfile
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical

root=Path(__file__).resolve().parents[1];out=root/'reports/p02a'
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
files=set()
for base in ['src/taskcognition','tests','vendor/reasoning_gym_p01','vendor/reasoning_gym_p02a','reports/p02a','artifacts/development/p02a-six-family']:
    files.update(p for p in (root/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
for pattern in ['scripts/p02a_*.py','configs/state_events/*.json','configs/state_snapshots/*.json']:
    files.update(root.glob(pattern))
for name in ['AGENTS.md','pyproject.toml','configs/phase_state.json','configs/p01_requirements.lock','reference/TaskCognition_Revised_Verified.pdf','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/ARCHITECTURE_AND_DATA.md','docs/STATISTICAL_CONTRACT.md','docs/EVIDENCE_AND_MANUSCRIPT.md','docs/DECISIONS_AND_GAPS.md','docs/prompts/P02_development_pilot.md','docs/prompts/P02A_six_family_integration_prompt.md','reports/decision_ledger.md','reports/phases/P01_accepted_seal.md','reports/phases/P01_completion_v2.md','reports/phases/P01_proposed_seal_v2.md','reports/phases/P01_evidence_manifest_v2.json','reports/p01_correction_v2/P01_v2_coordinator_acceptance.md','reports/phases/P02A_completion.md','reports/p01/P02_resource_proposal.md','reports/p01/model_download.json','reports/p01/gpu_check.json','scripts/p01_command.py']:
    files.add(root/name)
excluded={'P02A_review_packet.zip','P02A_evidence_index.json','P02A_packet_receipt.json'}
files={p for p in files if p.name not in excluded}
index={p.relative_to(root).as_posix():file_hash(p) for p in sorted(files)}
write_new(out/'P02A_evidence_index.json',dict(evidence_kind='development_observation',phase='P02A',files=index,source_commit=read_json(root/'configs/state_events/006_P02A_bounded_dispatch.json')['source_commit'],evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),exclusions='Index, ZIP and external receipt avoid hash cycles. No weights, environments, credentials or private meeting content.'))
packet=out/'P02A_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in index:z.write(root/name,name)
    z.write(out/'P02A_evidence_index.json','reports/p02a/P02A_evidence_index.json')
with zipfile.ZipFile(packet) as z:
    assert z.testzip() is None
    stored=json.loads(z.read('reports/p02a/P02A_evidence_index.json'))
    for name,h in stored['files'].items():assert hashlib.sha256(z.read(name)).hexdigest()==h,name
    assert len(z.namelist())==len(index)+1
receipt=dict(evidence_kind='development_observation',status='PASS',indexed_files=len(index),zip_sha256=file_hash(packet),zip_bytes=packet.stat().st_size,index_sha256=file_hash(out/'P02A_evidence_index.json'),completion_sha256=file_hash(root/'reports/phases/P02A_completion.md'),verified_zip_members=True,backup='verified local ZIP; no off-machine backup',total_p02a_evidence_bytes=sum(p.stat().st_size for base in [root/'artifacts/development/p02a-six-family',out] for p in base.rglob('*') if p.is_file()))
base_bytes=receipt['total_p02a_evidence_bytes']
for _ in range(5):receipt['total_p02a_evidence_bytes']=base_bytes+len(canonical(receipt))+1
write_new(out/'P02A_packet_receipt.json',receipt)
print(json.dumps(read_json(out/'P02A_packet_receipt.json'),indent=2))
