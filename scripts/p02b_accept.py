"""Verify P02A accepted snapshot before recording the user-conveyed checkpoint acceptance."""
import hashlib,subprocess,zipfile
from datetime import datetime,timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import canonical,file_hash
root=Path(__file__).resolve().parents[1]
expected={'reports/phases/P02A_completion.md':'731b96e784e84450ba18df2c0b2ed139a15e19eb69c491dcebccdb741b03f175','reports/p02a/P02A_evidence_index.json':'2637c610c539254964152ef091463b6df7e19506b60b987b7367722b735312bf','reports/p02a/P02A_review_packet.zip':'97784d3ae68a53343d0f458c72180f56430fb242ebcfe220a01d51b29171bfce','reports/p02a/P02A_packet_receipt.json':'b772af7f10527ade46da0204d07cba42a79d27ab54269f69556996f6badbb14c'}
for name,h in expected.items():assert file_hash(root/name)==h,name
index=read_json(root/'reports/p02a/P02A_evidence_index.json')
with zipfile.ZipFile(root/'reports/p02a/P02A_review_packet.zip') as z:
    assert len(index['files'])==359
    for name,h in index['files'].items():
        assert hashlib.sha256(z.read(name)).hexdigest()==h,name
        assert file_hash(root/name)==h,name
commits=['d9f78e6467ab5509219390475930b361364257b2','617b15fcb467422fa667e7c9a994ca217d349ac6']
for commit in commits:
    assert subprocess.check_output(['git','rev-parse',commit],text=True).strip()==commit
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],check=True)
packet=subprocess.check_output(['git','rev-parse','00a9ffe'],text=True).strip()
now=datetime.now(timezone.utc).isoformat()
write_new(root/'reports/p02b/acceptance_verification.json',dict(evidence_kind='development_observation',timestamp_utc=now,status='PASS',verified_artifacts=expected,indexed_files=359,current_and_packet_match=True,pre_dispatch_commit=commits[0],evidence_commit=commits[1],packet_commit=packet,new_gpu_work=0))
statepath=root/'configs/phase_state.json';snapshot=root/'configs/state_snapshots/P02A_accepted_before_P02B.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
record=root/'reports/phases/P02A_accepted_checkpoint.md'
with record.open('x',encoding='utf-8') as f:
    f.write(f'# P02A accepted checkpoint\n\nRecorded UTC: {now}.\n\nAuthority: current user P02B prompt: “The user is conveying `reports/p02a/P02A_coordinator_acceptance.md` and authorizing only this bounded P02B development checkpoint.”\n\nCoordinator review SHA-256: `{file_hash(root/"reports/p02a/P02A_coordinator_acceptance.md")}`. All four accepted artifacts and all 359 indexed current/packet files match.\n\n')
    for name,h in expected.items():f.write(f'- `{name}`: `{h}`\n')
    f.write(f'\nPre-dispatch commit `{commits[0]}`; evidence commit `{commits[1]}`; packet commit `{packet}`. Coordinator review used offline tests/replay and performed no independent GPU run.\n\nP02A is ACCEPTED as a completed integration checkpoint, not a full-phase seal or scientific freeze. P01 remains sealed. P01 and P02A dispatch remain closed. Only P02B is activated: 48 fixed mixed-cap calls maximum. P02 remains incomplete and unsealed. All old primary scores, raw evidence and snapshots remain unchanged.\n')
event='configs/state_events/008_P02A_accept_P02B_start.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='checkpoint_acceptance_and_bounded_activation',previous_state_sha256=file_hash(snapshot),accepted_checkpoint='P02A',acceptance_record_sha256=file_hash(record),active_phase='P02B',status='IN_PROGRESS',real_dispatch_enabled=False,p01_dispatch_enabled=False,p02a_dispatch_enabled=False,p02_sealed=False))
statepath.write_bytes(canonical(dict(active_phase='P02B',parent_phase='P02',status='IN_PROGRESS',real_dispatch_enabled=False,accepted_previous_checkpoint='P02A',accepted_previous_checkpoint_record='reports/phases/P02A_accepted_checkpoint.md',accepted_previous_phase='P01',accepted_previous_seal='reports/phases/P01_accepted_seal.md',latest_event=event,authorized_next_phase=None,study_freeze=None))+b'\n')
print('PASS: four hashes, 359 current/packet files, both commits; P02A accepted, only P02B active, dispatch off.')
