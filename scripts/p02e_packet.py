"""Build a compact P02E packet, verify old/new bytes, and write external receipt."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
import zipfile
from p02e_analyze import ROOT, OUT, read, write, sha

start, cpu = time.perf_counter(), time.process_time()
state = read(ROOT/'configs/phase_state.json')
assert state['active_phase']=='P02E' and state['status']=='READY_FOR_REVIEW'
assert not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
assert state['study_freeze'] is None and state['authorized_next_phase'] is None
verification = read(OUT/'acceptance_verification.json')
for name,digest in verification['accepted_hashes'].items():
    assert sha(ROOT/name)==digest, name
for name,digest in verification['source_hashes'].items():
    assert sha(ROOT/name)==digest, name
oldindex = read(ROOT/'reports/p02d_execution/P02D_execution_evidence_index.json')
current_changed = {}
with zipfile.ZipFile(ROOT/'reports/p02d_execution/P02D_execution_review_packet.zip') as z:
    for name,digest in oldindex['files'].items():
        assert hashlib.sha256(z.read(name)).hexdigest()==digest, name
        current = sha(ROOT/name)
        if current != digest:
            assert name=='configs/phase_state.json', name
            current_changed[name] = dict(accepted=digest,current=current,
                reason='Explicit P02D acceptance/P02E offline activation and checkpoint events 023/024; old bytes preserved in accepted ZIP.')
assert len(oldindex['files'])==8997
assert subprocess.check_output(['git','diff','b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4','--','src'],cwd=ROOT)==b''
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
write(OUT/'source_commits.json',dict(analysis_evidence_commit=head,
    source_diff='reports/p02e/source_changes.diff',
    accepted_source_commit=verification['source_commit'],
    accepted_execution_evidence_commit=verification['evidence_commit'],
    accepted_packet_commit=verification['packet_commit'],
    new_packet_commit_lookup='git log -1 -- reports/p02e/P02E_review_packet.zip',
    no_push=True, production_sources_unchanged=True))
write(OUT/'historical_reverification.json',dict(status='PASS',
    indexed_snapshot_files_verified=8997, current_state_changes=current_changed,
    all_other_indexed_current_files_unchanged=True, accepted_artifacts=verification['accepted_hashes'],
    timestamp_utc=datetime.now(timezone.utc).isoformat(),model_work=0))

paths = set()
excluded={'P02E_evidence_index.json','P02E_review_packet.zip','P02E_packet_receipt.json'}
for p in OUT.rglob('*'):
    if p.is_file() and p.name not in excluded and p.suffix.lower()!='.zip':
        paths.add(p.relative_to(ROOT).as_posix())
for p in (ROOT/'scripts').glob('p02e_*.py'):
    paths.add(p.relative_to(ROOT).as_posix())
paths.update([
    'scripts/p01_command.py','tests/test_p02e_design.py',
    'reports/phases/P02E_completion.md','reports/decision_ledger.md',
    'configs/phase_state.json',
    'configs/state_events/023_P02D_execution_accepted_P02E_authorized.json',
    'configs/state_events/024_P02E_offline_design_review_checkpoint.json',
    'AGENTS.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/STATISTICAL_CONTRACT.md',
    'docs/DECISIONS_AND_GAPS.md','docs/ARCHITECTURE_AND_DATA.md',
    'docs/amendments/CR01_2026-10-05_v1.md','docs/P02D_RUNNER_CONTRACT.md',
    'paper/cr01-2026-10-05-v1/taskcognition.tex'])
files={p:sha(ROOT/p) for p in sorted(paths)}
index_path=OUT/'P02E_evidence_index.json'
write(index_path,dict(phase='P02E',evidence_kind='development_observation',
    analysis_kind='offline_design',files=files,indexed_file_count=len(files),
    analysis_evidence_commit=head, accepted_plan_sha256=state['p02d_plan_sha256'],
    accepted_execution_zip_sha256=verification['accepted_hashes']['reports/p02d_execution/P02D_execution_review_packet.zip'],
    references_only='Accepted raw evidence/preflight sources are not duplicated. Original accepted packet(s) required to rerun analysis. Coordinator bundle archived locally and referenced by hash, not embedded recursively.',
    all_execution_unapproved=True,new_model_work=0))
packet=OUT/'P02E_review_packet.zip'
index_name=index_path.relative_to(ROOT).as_posix()
with zipfile.ZipFile(packet,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(ROOT/p,p)
    z.write(index_path,index_name)
with zipfile.ZipFile(packet) as z:
    assert set(z.namelist())==set(files)|{index_name}
    for p,digest in files.items():
        assert hashlib.sha256(z.read(p)).hexdigest()==digest==sha(ROOT/p),p
    assert z.read(index_name)==index_path.read_bytes()
write(OUT/'P02E_packet_receipt.json',dict(status='PASS',phase='P02E',
    timestamp_utc=datetime.now(timezone.utc).isoformat(),
    zip_sha256=sha(packet),index_sha256=sha(index_path),
    completion_sha256=sha(ROOT/'reports/phases/P02E_completion.md'),
    design_report_sha256=sha(OUT/'offline_design_report.md'),
    proposal_sha256=sha(OUT/'next_step_proposal.md'),
    indexed_files_verified=len(files),zip_members=len(files)+1,
    zip_bytes=packet.stat().st_size,indexed_uncompressed_bytes=sum((ROOT/p).stat().st_size for p in files),
    local_p02e_bytes_before_this_receipt=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
    historical_indexed_files_reverified=8997,analysis_evidence_commit=head,
    wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
    model_work=0,real_dispatch_enabled=False,p02_sealed=False,p03_started=False,
    receipt_location='Outside ZIP, local workstation only; no off-machine backup claimed.',
    no_push_upload_remote_query=True))
print(json.dumps(dict(status='PASS',files=len(files),zip_sha256=sha(packet),
    receipt_sha256=sha(OUT/'P02E_packet_receipt.json'))))
