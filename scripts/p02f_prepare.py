"""Verify P02E acceptance and activate offline P02F; standard library only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, platform, shutil, subprocess, sys, time, zipfile
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'reports/p02f'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(v,f,indent=2,allow_nan=False); f.write('\n')
def main():
    start,cpu=time.perf_counter(),time.process_time()
    expected={
      'reports/p02e/P02E_review_packet.zip':'9f3fddc83ff26a26726623a3a568d35b71bbf61f470ce1f724fa0ccfbbbdbe0f',
      'reports/p02e/P02E_evidence_index.json':'2cab5fc1f5e493a7ef081e948a09c753a4ae476f3220223040d4297b3e71d5e7',
      'reports/p02e/offline_design_report.md':'62bd6de18f851239e5833684f818072d1965a5f7da302320e258b7b610db4d24',
      'reports/p02e/next_step_proposal.md':'3220410a1d3a0f8e9194e3114d05ef4ae779860b27179da4b604de34b2770546',
      'artifacts/development/p02d-cr01-plan-v4/run_plan.json':'c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365',
      'reference/TaskCognition_Revised_Verified.pdf':'9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8'}
    for p,h in expected.items(): assert sha(ROOT/p)==h,p
    index=read(ROOT/'reports/p02e/P02E_evidence_index.json')
    with zipfile.ZipFile(ROOT/'reports/p02e/P02E_review_packet.zip') as z:
        for p,h in index['files'].items():
            assert hashlib.sha256(z.read(p)).hexdigest()==h==sha(ROOT/p),p
    assert len(index['files'])==63
    OUT.mkdir(exist_ok=True); (OUT/'provenance').mkdir(exist_ok=True)
    authority={}
    for p in ['docs/P02E_acceptance_review.md','docs/prompts/P02F_cost_boundary_preflight_prompt.md']:
        dest=OUT/'provenance'/Path(p).name
        with dest.open('xb') as f:f.write((ROOT/p).read_bytes())
        authority[p]=sha(dest)
    state_path=ROOT/'configs/phase_state.json'; state=read(state_path)
    assert state['active_phase']=='P02E' and state['status']=='READY_FOR_REVIEW' and not state['real_dispatch_enabled']
    for p in ['configs/phase_state.json','reports/decision_ledger.md']:
        dest=OUT/'provenance'/('before_'+Path(p).name)
        with dest.open('xb') as f:f.write((ROOT/p).read_bytes())
    now=datetime.now(timezone.utc).isoformat()
    bindings={p.as_posix():sha(ROOT/p) for p in [
      Path('AGENTS.md'),Path('docs/PROTOCOL_SOURCE_OF_TRUTH.md'),Path('docs/STATISTICAL_CONTRACT.md'),
      Path('docs/DECISIONS_AND_GAPS.md'),Path('docs/ARCHITECTURE_AND_DATA.md'),Path('docs/EVIDENCE_AND_MANUSCRIPT.md'),
      Path('docs/amendments/CR01_2026-10-05_v1.md'),Path('paper/cr01-2026-10-05-v1/taskcognition.tex'),
      Path('configs/p02d_execution_authorization.json'),Path('reports/p02d_execution/workstation_before.json')]}
    source={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'src').rglob('*.py')}
    write(OUT/'acceptance_verification.json',dict(status='PASS',timestamp_utc=now,accepted_hashes=expected,
      indexed_zip_and_current_files_verified=63,authority_hashes=authority,bindings=bindings,previous_source_hashes=source,
      original_cost_pages_read=[3,5,6],new_gpu_inspection=False,model_work=0,
      workstation='Existing P02D inventory referenced, not a new GPU measurement.',python=sys.version,
      os=platform.platform(),disk_free_bytes=shutil.disk_usage(ROOT).free,
      head_before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu))
    event='configs/state_events/025_P02E_accepted_P02F_offline_authorized.json'
    write(ROOT/event,dict(event='P02E_ACCEPTED_P02F_OFFLINE_AUTHORIZED',timestamp_utc=now,
      user_conveyed_acceptance_date='2026-10-17',timezone='America/Chicago',
      acceptance_verbatim='Decision: P02E OFFLINE DESIGN ACCEPTED.',
      review_sha256=authority['docs/P02E_acceptance_review.md'],prompt_sha256=authority['docs/prompts/P02F_cost_boundary_preflight_prompt.md'],
      verification='reports/p02f/acceptance_verification.json',previous_state_sha256=sha(state_path),
      real_dispatch_enabled=False,p02_sealed=False,p03_started=False,study_frozen=False,
      scope='Offline cost decision and minimal fixture-only prototype; consumed P02D authorization remains closed.'))
    state.update(active_phase='P02F',checkpoint='OFFLINE_COST_BOUNDARY_PREFLIGHT',status='IN_PROGRESS',
      accepted_previous_checkpoint='P02E_OFFLINE_DESIGN',accepted_previous_checkpoint_record=event,latest_event=event)
    state_path.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='PASS',indexed_files=63,adoption_utc=now,model_work=0)))
if __name__=='__main__': main()
