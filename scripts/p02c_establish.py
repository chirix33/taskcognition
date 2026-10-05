"""Offline acceptance and immutable pre-amendment preservation; no model imports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,zipfile,shutil

root=Path(__file__).resolve().parents[1];out=root/'reports/p02c';out.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n')
expected={'reports/phases/P02B_completion.md':'75e858192c9a0f4ec863e51ffb3f0a4d37b0af3e2f229a1265c53ecc5a6b2534','reports/p02b/P02B_evidence_index.json':'f92a2903b0d44649ac9670e2108d8ef8092dbe5f4d516f57ea1954c2be174ddf','reports/p02b/P02B_review_packet.zip':'a66ae570dcd7c470fda399bd858bc19100d750db8c388951b977a6a138be314b','reports/p02b/P02B_packet_receipt.json':'44c8ae0433c23f7f26eb2cae87f447d0e536bee40d410b5e6a7f5baa690802cd'}
for n,h in expected.items():assert sha(root/n)==h,n
index=json.loads((root/'reports/p02b/P02B_evidence_index.json').read_text())['files'];assert len(index)==598
with zipfile.ZipFile(root/'reports/p02b/P02B_review_packet.zip') as z:
    assert z.testzip() is None
    for n,h in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
changed=[n for n,h in index.items() if sha(root/n)!=h]
assert not changed,changed
commits=['72d88843067b8a8f0f29d2937587a102d5a24f6b','ba3ef09dd8db95a1e60a380723f398f99e5d52d4','123a43ff198b2e1a450b98b6be226a2cbea896e9']
for c in commits:subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],check=True)
source=json.loads((root/'reports/source_inventory.json').read_text())
assert sha(root/'reference/TaskCognition_Revised_Verified.pdf')==source['source_sha256']
for n,h in source['preserved_original_files'].items():assert sha(root/n)==h,n
now=datetime.now(timezone.utc).isoformat()
save(out/'acceptance_verification.json',dict(evidence_kind='development_observation',operation='offline_hash_verification',timestamp_utc=now,accepted_artifacts=expected,indexed_files=598,accepted_zip_and_current_bytes_match=True,commits=commits,reference_pdf_sha256=source['source_sha256'],original_source_files_match=True,new_generations=0))
with zipfile.ZipFile(out/'pre_CR01_source_snapshot.zip','x',zipfile.ZIP_DEFLATED) as z:
    for n in source['preserved_original_files']:z.write(root/n,n)
    for n in ['AGENTS.md','README.md','reports/decision_ledger.md','configs/phase_state.json']+[p.relative_to(root).as_posix() for p in (root/'docs').glob('*.md') if p.name!='TaskCognition_CR01_APPROVED.md']+[p.relative_to(root).as_posix() for p in (root/'docs/prompts').glob('*.md') if p.name!='P02C_adopt_CR01_prompt.md']+[p.relative_to(root).as_posix() for p in (root/'docs/templates').glob('*.md')]:z.write(root/n,n)
with zipfile.ZipFile(out/'pre_CR01_source_snapshot.zip') as z:
    snapshots={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}
    assert all(sha(root/n)==h for n,h in snapshots.items())
save(out/'preservation_manifest.json',dict(evidence_kind='development_observation',snapshot_sha256=sha(out/'pre_CR01_source_snapshot.zip'),files=snapshots,base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),preserved_user_files=['ChatGPT Image Sep 29, 2026, 05_27_51 PM.png','docs/TaskCognition_CR01_APPROVED.md','docs/prompts/P02C_adopt_CR01_prompt.md','reports/p02a/P02A_coordinator_acceptance.md']))
statepath=root/'configs/phase_state.json';state=json.loads(statepath.read_text());assert state['active_phase']=='P02B' and state['real_dispatch_enabled'] is False
snapshot=root/'configs/state_snapshots/P02B_accepted_before_P02C.json';shutil.copyfile(statepath,snapshot)
record=root/'reports/phases/P02B_accepted_checkpoint.md'
record.write_text(f'''# P02B accepted development checkpoint

Recorded UTC: {now}.

Authority: current user P02C prompt conveys the coordinator's P02B acceptance and instructs recording it if not already completed. No prior P02B acceptance event exists. The separate review/draft documents were not found locally; this is not a claim of an independent coordinator GPU run.

All four supplied hashes, all 598 indexed ZIP/current files, pre-dispatch `{commits[0]}`, evidence `{commits[1]}`, and packet `{commits[2]}` were verified. See reports/p02c/acceptance_verification.json for exact hashes.

P01 remains sealed; P02A/P02B are accepted DEVELOPMENT checkpoints. P02 remains incomplete and unsealed. Only offline P02C is activated; all real dispatch remains disabled.
''',encoding='utf-8')
event='configs/state_events/012_P02B_accept_P02C_offline.json'
save(root/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='P02B_acceptance_and_offline_P02C_activation',previous_state_sha256=sha(snapshot),acceptance_record_sha256=sha(record),active_phase='P02C',real_dispatch_enabled=False,p02_complete=False,p02_sealed=False,p03_started=False))
state.update(active_phase='P02C',status='IN_PROGRESS',latest_event=event,real_dispatch_enabled=False,accepted_previous_checkpoint='P02B',accepted_previous_checkpoint_record='reports/phases/P02B_accepted_checkpoint.md',authorized_next_phase=None)
statepath.write_text(json.dumps(state,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
print('PASS: four artifacts, 598 ZIP/current files, commits and original manuscript; snapshot preserved; P02B accepted once, offline P02C active.')
