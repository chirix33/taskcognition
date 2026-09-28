"""Verify the accepted immutable P01 snapshot before recording conveyed acceptance."""
import hashlib, json, subprocess, zipfile
from datetime import datetime, timezone
from pathlib import Path
from taskcognition.artifacts import write_new
from taskcognition.contracts import file_hash, canonical

root=Path(__file__).resolve().parents[1]
expected={
 'reports/phases/P01_completion_v2.md':'e75e0f4e99396223b61beb3f378c10d3a3a7c9d5db4db0d248700fae5ac69f13',
 'reports/phases/P01_proposed_seal_v2.md':'ea632c19ffa3a9b842e6a3e74c7fe3cd078cf0dbceda7eb347307bbe12bcf4da',
 'reports/phases/P01_evidence_manifest_v2.json':'1237761e49fcee9a9e027324995f6452b27b83417b205e12c44d451940b09a3f',
 'reports/p01_correction_v2/P01_review_packet_v2.zip':'dab8fd3ae4ea7b09e5802de7f02ee12f9f00dbf843c857e5921ca9dc69a639b3'}
for n,h in expected.items(): assert file_hash(root/n)==h,n
index=json.loads((root/'reports/phases/P01_evidence_manifest_v2.json').read_text())
with zipfile.ZipFile(root/'reports/p01_correction_v2/P01_review_packet_v2.zip') as z:
 for n,h in index['files'].items():
  assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  assert file_hash(root/n)==h,n
code='6e8cec19d3e7f374aebddaa4f9b410767b02676a'
packet=subprocess.check_output(['git','rev-parse','0c92cb1'],cwd=root,text=True).strip()
subprocess.run(['git','merge-base','--is-ancestor',code,packet],cwd=root,check=True)
now=datetime.now(timezone.utc).isoformat()
write_new(root/'reports/p02a/p01_acceptance_verification.json',dict(evidence_kind='development_observation',timestamp_utc=now,status='PASS',artifacts=expected,indexed_files=len(index['files']),zip_and_current_match=True,code_commit=code,packet_commit=packet,new_generations=0))
snapshot=root/'configs/state_snapshots/P01_accepted_v2_before_P02A.json'
with snapshot.open('xb') as f:f.write((root/'configs/phase_state.json').read_bytes())
seal=root/'reports/phases/P01_accepted_seal.md'
with seal.open('x',encoding='utf-8') as f:
 f.write('# P01 accepted seal\n\nP01 is SEALED by user-conveyed coordinator acceptance.\n\n')
 f.write(f'Recorded UTC: {now}. Authority: current user P02A prompt, “The user is conveying the coordinator\'s P01 v2 acceptance and authorizing this prompt\'s bounded local work.”\n\n')
 f.write('Acceptance: reports/p01_correction_v2/P01_v2_coordinator_acceptance.md, SHA-256 '+file_hash(root/'reports/p01_correction_v2/P01_v2_coordinator_acceptance.md')+'\n\n')
 for n,h in expected.items():f.write(f'- `{n}`: `{h}`\n')
 f.write(f'\nAll {len(index["files"])} indexed files match accepted ZIP and current checkout. Corrected code/evidence commit `{code}`; separate report-packet commit `{packet}`. Both proposed seals and all historical evidence remain unchanged.\n\nP01 dispatch remains disabled; five unused slots remain inactive. Live D valid-FINAL success remains unestablished in P01. Only P02A is activated within incomplete, unsealed P02. No scientific freeze or final labels authorized.\n')
event='configs/state_events/005_P01_accept_P02A_start.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='phase_acceptance_and_bounded_activation',previous_state_sha256=file_hash(snapshot),accepted_phase='P01',accepted_status='SEALED',acceptance_sha256=file_hash(seal),active_phase='P02A',parent_phase='P02',status='IN_PROGRESS',real_dispatch_enabled=False,p01_dispatch_enabled=False,p01_unused_slots_inactive=5,authorized_prompt_sha256=file_hash(root/'docs/prompts/P02A_six_family_integration_prompt.md')))
(root/'configs/phase_state.json').write_bytes(canonical(dict(active_phase='P02A',parent_phase='P02',status='IN_PROGRESS',real_dispatch_enabled=False,accepted_previous_phase='P01',accepted_previous_seal='reports/phases/P01_accepted_seal.md',latest_event=event,authorized_next_phase=None,study_freeze=None))+b'\n')
print('PASS: accepted P01 snapshot; P01 sealed; only P02A active, dispatch disabled.')
