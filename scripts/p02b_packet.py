"""Create and verify a local review packet, without weights or environments."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import canonical,file_hash
root=Path(__file__).resolve().parents[1];out=root/'reports/p02b'
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
files=set()
for base in ['src/taskcognition','tests','vendor/reasoning_gym_p01','vendor/reasoning_gym_p02a','reports/p02b','artifacts/development/p02b-two-cap']:
    files.update(p for p in (root/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
for pattern in ['scripts/p02b_*.py','configs/state_events/*.json','configs/state_snapshots/*.json']:files.update(root.glob(pattern))
for n in ['AGENTS.md','pyproject.toml','configs/phase_state.json','configs/p01_requirements.lock','reference/TaskCognition_Revised_Verified.pdf','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/ARCHITECTURE_AND_DATA.md','docs/STATISTICAL_CONTRACT.md','docs/EVIDENCE_AND_MANUSCRIPT.md','docs/DECISIONS_AND_GAPS.md','docs/templates/PHASE_COMPLETION_TEMPLATE.md','reports/decision_ledger.md','reports/phases/P01_accepted_seal.md','reports/phases/P02A_accepted_checkpoint.md','reports/phases/P02A_completion.md','reports/p02a/P02A_coordinator_acceptance.md','reports/p02a/P02A_evidence_index.json','reports/p02a/P02A_packet_receipt.json','reports/p02a/integration_table.md','reports/p02a/adapter_contracts.md','reports/p01/model_download.json','scripts/p01_command.py','reports/phases/P02B_completion.md']:
    files.add(root/n)
exclusions={'P02B_review_packet.zip','P02B_evidence_index.json','P02B_packet_receipt.json'}
files={p for p in files if p.name not in exclusions}
index={p.relative_to(root).as_posix():file_hash(p) for p in sorted(files)}
write_new(out/'P02B_evidence_index.json',dict(evidence_kind='development_observation',phase='P02B',files=index,pre_dispatch_commit=read_json(root/'configs/state_events/009_P02B_bounded_dispatch.json')['source_commit'],evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),hash_cycle_exclusions='Index, ZIP and external receipt. No weights, environments, secrets, private meetings or external upload.'))
packet=out/'P02B_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in index:z.write(root/n,n)
    z.write(out/'P02B_evidence_index.json','reports/p02b/P02B_evidence_index.json')
with zipfile.ZipFile(packet) as z:
    assert z.testzip() is None
    for n,h in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
    assert len(z.namelist())==len(index)+1
receipt=dict(evidence_kind='development_observation',status='PASS',indexed_files=len(index),zip_sha256=file_hash(packet),zip_bytes=packet.stat().st_size,index_sha256=file_hash(out/'P02B_evidence_index.json'),completion_sha256=file_hash(root/'reports/phases/P02B_completion.md'),verified_zip_members=True,backup='local only; no off-machine backup',p02b_directory_evidence_bytes=0)
base=sum(p.stat().st_size for b in (out,root/'artifacts/development/p02b-two-cap') for p in b.rglob('*') if p.is_file())
for _ in range(5):receipt['p02b_directory_evidence_bytes']=base+len(canonical(receipt))+1
write_new(out/'P02B_packet_receipt.json',receipt)
print(json.dumps(receipt,indent=2))
