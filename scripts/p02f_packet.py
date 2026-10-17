"""Package the offline blocked decision, not a live execution request."""
from datetime import datetime,timezone
import hashlib,json,subprocess,time,zipfile
from p02f_prepare import ROOT,OUT,read,write,sha

start,cpu=time.perf_counter(),time.process_time()
v=read(OUT/'acceptance_verification.json'); state=read(ROOT/'configs/phase_state.json')
assert state['active_phase']=='P02F' and state['status']=='COST_DESIGN_BLOCKED'
assert not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
assert state['study_freeze'] is None and state['authorized_next_phase'] is None
for p,h in v['accepted_hashes'].items():assert sha(ROOT/p)==h,p
for p,h in v['bindings'].items():assert sha(ROOT/p)==h,p
for p,h in v['previous_source_hashes'].items():assert sha(ROOT/p)==h,p
index=read(ROOT/'reports/p02e/P02E_evidence_index.json'); changed={}
with zipfile.ZipFile(ROOT/'reports/p02e/P02E_review_packet.zip') as z:
    for p,h in index['files'].items():
        assert hashlib.sha256(z.read(p)).hexdigest()==h,p
        current=sha(ROOT/p)
        if current!=h:
            assert p in ['configs/phase_state.json','reports/decision_ledger.md'],p
            changed[p]=dict(accepted=h,current=current,reason='P02E acceptance and P02F offline state/decision events; historical bytes retained in accepted packet.')
assert len(index['files'])==63
write(OUT/'historical_reverification.json',dict(status='PASS',files_verified=63,
    changed_current_operational_files=changed,all_old_scientific_source_unchanged=True,
    accepted_hashes=v['accepted_hashes'],unchanged_authority=v['bindings']))
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
write(OUT/'source_commits.json',dict(source_evidence_commit=head,
    accepted_P02E_evidence_commit='2bc0131eb8cb70a314d6a8fcfe31f277aadf45b1',
    accepted_P02E_packet_commit='7c2fb57b3b895ae440a9cdd9606a13a4bbaf5384',
    P02F_packet_commit_lookup='git log -1 -- reports/p02f/P02F_review_packet.zip',no_push=True))
excluded={'P02F_review_packet.zip','P02F_evidence_index.json','P02F_packet_receipt.json'}
paths={p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name not in excluded and p.suffix!='.zip'}
paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'scripts').glob('p02f_*.py'))
paths.update(read(OUT/'fixture_files.json')['files'])
paths.update(['reports/p02f_prepare_command.json','reports/phases/P02F_preflight_completion.md',
    'src/taskcognition/p02f_cost_v1.py','tests/test_p02f_cost_v1.py',
    'src/taskcognition/__init__.py','src/taskcognition/contracts.py','src/taskcognition/artifacts.py','src/taskcognition/p02d_publication.py',
    'scripts/p01_command.py','configs/phase_state.json',
    'configs/state_events/025_P02E_accepted_P02F_offline_authorized.json',
    'configs/state_events/026_P02F_cost_design_blocked.json','reports/decision_ledger.md',
    'AGENTS.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/STATISTICAL_CONTRACT.md',
    'docs/DECISIONS_AND_GAPS.md','docs/amendments/CR01_2026-10-05_v1.md'])
files={p:sha(ROOT/p) for p in sorted(paths)}
indexpath=OUT/'P02F_evidence_index.json'
write(indexpath,dict(phase='P02F',status='COST_DESIGN_BLOCKED',files=files,
    indexed_files=len(files),source_evidence_commit=head,model_work=0,
    accepted_P02E_zip_sha256=v['accepted_hashes']['reports/p02e/P02E_review_packet.zip'],
    note='Original accepted evidence referenced by hash, not nested. Fixture files are synthetic and do not authorize execution.'))
packet=OUT/'P02F_review_packet.zip'; indexname=indexpath.relative_to(ROOT).as_posix()
with zipfile.ZipFile(packet,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(ROOT/p,p)
    z.write(indexpath,indexname)
with zipfile.ZipFile(packet) as z:
    assert set(z.namelist())==set(files)|{indexname}
    for p,h in files.items():assert hashlib.sha256(z.read(p)).hexdigest()==h==sha(ROOT/p),p
    assert z.read(indexname)==indexpath.read_bytes()
write(OUT/'P02F_packet_receipt.json',dict(status='PASS',checkpoint='P02F_COST_DESIGN_BLOCKED',
    timestamp_utc=datetime.now(timezone.utc).isoformat(),zip_sha256=sha(packet),index_sha256=sha(indexpath),
    completion_sha256=sha(ROOT/'reports/phases/P02F_preflight_completion.md'),
    cost_decision_sha256=sha(OUT/'cost_contract_decision.md'),
    indexed_files_verified=len(files),zip_members=len(files)+1,zip_bytes=packet.stat().st_size,
    indexed_bytes=sum((ROOT/p).stat().st_size for p in files),
    local_p02f_bytes_before_receipt=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
    source_evidence_commit=head,historical_P02E_files_reverified=63,
    wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
    real_dispatch_enabled=False,model_work=0,p02_sealed=False,p03_started=False,
    next_decision='cost-metric selection, not execution approval',
    backup='Verified local packet; external receipt is outside ZIP on workstation, not off-machine. No upload/push.'))
print(json.dumps(dict(status='PASS',files=len(files),zip_sha256=sha(packet),receipt_sha256=sha(OUT/'P02F_packet_receipt.json'))))
