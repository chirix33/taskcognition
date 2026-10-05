"""Build and verify a local P02C review packet without environments or weights."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
root=Path(__file__).resolve().parents[1];out=root/'reports/p02c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
state=json.loads((root/'configs/phase_state.json').read_text());assert state['active_phase']=='P02C' and state['status']=='READY_FOR_REVIEW' and not state['real_dispatch_enabled']
files=set()
for base in ['reports/p02c','paper/cr01-2026-10-05-v1','src/taskcognition','tests']:
    files.update(p for p in (root/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
for pattern in ['scripts/p02c_*.py','docs/*.md','docs/prompts/P0[2-9]_*.md','docs/templates/*.md','configs/state_events/01*.json']:
    files.update(root.glob(pattern))
for n in ['.gitattributes','AGENTS.md','README.md','pyproject.toml','reference/TaskCognition_Revised_Verified.pdf','docs/amendments/CR01_2026-10-05_v1.md','docs/prompts/P02C_adopt_CR01_prompt.md','configs/phase_state.json','configs/cr01_development_design_template.json','configs/state_snapshots/P02B_accepted_before_P02C.json','reports/decision_ledger.md','reports/source_inventory.json','reports/phases/P01_accepted_seal.md','reports/phases/P02A_accepted_checkpoint.md','reports/phases/P02B_accepted_checkpoint.md','reports/phases/P02C_completion.md','reports/phases/P02B_completion.md','reports/p02b/P02B_evidence_index.json','reports/p02b/P02B_packet_receipt.json','reports/p02b/P02B_review_packet.zip','reports/p02b/observations.json','reports/p02b/instruction_diff.json','artifacts/development/p02b-two-cap/package_base.json','scripts/p01_command.py']:
    files.add(root/n)
# Include only task-related authority/docs. Never sweep arbitrary user documents.
allowed_docs={'ARCHITECTURE_AND_DATA.md','DECISIONS_AND_GAPS.md','EVIDENCE_AND_MANUSCRIPT.md','IMPLEMENTATION_ROADMAP.md','PROTOCOL_SOURCE_OF_TRUTH.md','SOURCE_REGISTER.md','STATISTICAL_CONTRACT.md','P02B_coordinator_review.md','TaskCognition_CR01_APPROVED.md','TaskCognition_CR01_feasibility_DRAFT.md'}
files={p for p in files if p.parent!=root/'docs' or p.name in allowed_docs}
exclude={'P02C_review_packet.zip','P02C_evidence_index.json','P02C_packet_receipt.json'}
files={p for p in files if p.name not in exclude}
index={p.relative_to(root).as_posix():sha(p) for p in sorted(files)}
save(out/'P02C_evidence_index.json',dict(evidence_kind='development_observation',operation='offline_review_packaging',phase='P02C',files=index,evidence_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),cycle_exclusions='Index, ZIP and external receipt; source snapshot and accepted P02B ZIP included; no weights/environments/secrets/unrelated private material'))
packet=out/'P02C_review_packet.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in index:z.write(root/n,n)
    z.write(out/'P02C_evidence_index.json','reports/p02c/P02C_evidence_index.json')
with zipfile.ZipFile(packet) as z:
    assert z.testzip() is None and len(z.namelist())==len(index)+1
    for n,h in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
receipt=dict(evidence_kind='development_observation',operation='offline_review_receipt',status='PASS',indexed_files=len(index),zip_sha256=sha(packet),zip_bytes=packet.stat().st_size,index_sha256=sha(out/'P02C_evidence_index.json'),completion_sha256=sha(root/'reports/phases/P02C_completion.md'),adopted_amendment_sha256=sha(root/'docs/amendments/CR01_2026-10-05_v1.md'),verified_zip_members=True,new_answer_generations=0,new_model_loads=0,new_encoder_forwards=0,new_gpu_measurements=0,historical_admitted=75,historical_output_tokens=40555,manuscript_compiled=False,backup='local only; no off-machine backup',p02c_report_and_manuscript_directory_bytes=0)
base=sum(p.stat().st_size for b in (out,root/'paper/cr01-2026-10-05-v1') for p in b.rglob('*') if p.is_file())
for _ in range(5):receipt['p02c_report_and_manuscript_directory_bytes']=base+len((json.dumps(receipt,sort_keys=True,indent=2)+'\n').encode())
save(out/'P02C_packet_receipt.json',receipt)
print(json.dumps(receipt,indent=2))
