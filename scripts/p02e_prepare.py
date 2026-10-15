"""Offline provenance/acceptance and prospective analytical declaration only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,shutil,subprocess,time,zipfile

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'reports/p02e'; PROV=OUT/'provenance'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
start=time.perf_counter();cpu=time.process_time();now=datetime.now(timezone.utc).isoformat()
expected={
 'artifacts/development/p02d-cr01-plan-v4/run_plan.json':'c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365',
 'reports/p02d_execution/P02D_execution_review_packet.zip':'8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9',
 'reports/p02d_execution/production_execution_report.json':'9a5f6c7cf713941284b1c125570b3e174c641e685e01284b6bf86f0f95ff4dab',
 'reports/p02d_execution/execution_accounting.json':'0dda412d334389fc5278e8e05c48667a151120f67dbc6d7dfed06ebb4af0ef03',
 'reports/p02d_execution/P02D_execution_evidence_index.json':'89d0ec3b67123b7a46fdfbd688a7875a0911fa2a969ba6cdaeb4db9a41944521',
 'reports/p02d_execution/P02D_execution_packet_receipt.json':'c5e68413663dad2e426a7426edd4b287f0d0bd7826fec10c576d9b4222a0ab71',
 'reference/TaskCognition_Revised_Verified.pdf':'9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8',
 'docs/amendments/CR01_2026-10-05_v1.md':'ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8'}
for n,h in expected.items():assert sha(ROOT/n)==h,n
idx=read(ROOT/'reports/p02d_execution/P02D_execution_evidence_index.json')
assert len(idx['files'])==8997
with zipfile.ZipFile(ROOT/'reports/p02d_execution/P02D_execution_review_packet.zip') as z:
 assert z.testzip() is None
 for n,h in idx['files'].items():
  assert hashlib.sha256(z.read(n)).hexdigest()==h,n
  assert sha(ROOT/n)==h,n
state=read(ROOT/'configs/phase_state.json')
assert state['active_phase']=='P02D' and not state['real_dispatch_enabled'] and not state['p02_sealed'] and not state['p03_started']
assert not (ROOT/'configs/state_events/023_P02D_execution_accepted_P02E_authorized.json').exists()
archive={}
for n in ['docs/P02D_execution_acceptance_review.md','docs/prompts/P02E_offline_design_prompt.md','docs/P02D_execution_coordinator_checks.zip']:
 p=ROOT/n;dest=PROV/p.name;assert not dest.exists();shutil.copyfile(p,dest);archive[n]=sha(p)
shutil.copyfile(ROOT/'configs/phase_state.json',PROV/'phase_state_before.json')
shutil.copyfile(ROOT/'reports/decision_ledger.md',PROV/'decision_ledger_before.md')
authority=['AGENTS.md','docs/PROTOCOL_SOURCE_OF_TRUTH.md','docs/STATISTICAL_CONTRACT.md','docs/ARCHITECTURE_AND_DATA.md',
 'docs/DECISIONS_AND_GAPS.md','docs/EVIDENCE_AND_MANUSCRIPT.md','docs/TaskCognition_CR01_APPROVED.md',
 'paper/cr01-2026-10-05-v1/taskcognition.tex','reports/phases/P02D_execution_completion.md','docs/P02D_RUNNER_CONTRACT.md']
sources=['src/taskcognition/p02d_runner.py','src/taskcognition/p02d_worker.py','src/taskcognition/p02d_ledger.py',
 'src/taskcognition/p02d_plan.py','src/taskcognition/p02d_features.py','src/taskcognition/p02d_reporting.py','src/taskcognition/p02_native.py']
for n in sources:
 assert sha(ROOT/n)==idx['files'][n] if n in idx['files'] else True
 # Exact source identities are already in the v4 plan and reviewed preflight packet.
plan=read(ROOT/'artifacts/development/p02d-cr01-plan-v4/run_plan.json')
source_hashes={n:sha(ROOT/n) for n in sources}
for n,h in source_hashes.items():assert plan['bound_files'][n]==h,n
write(OUT/'acceptance_verification.json',dict(evidence_kind='development_observation',analysis_kind='offline_provenance',status='PASS',
 timestamp_utc=now,accepted_hashes=expected,indexed_zip_and_current_files_verified=8997,archived_authority_hashes=archive,
 authority_hashes={n:sha(ROOT/n) for n in authority},source_hashes=source_hashes,
 source_commit='b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4',evidence_commit='de45085992a23a3731ea267388a84349344f4ca1',
 packet_commit='32897ffcf99d0e950dd4ffec43b3adf94307a9bb',head_before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 coordinator_qualification='Offline reproduction only; not independent workstation/GPU/weight verification.',
 prior_pdf_console_display_failure='PDF extraction succeeded; console printing exited 1 under cp1252. UTF-8 read of saved extraction succeeded; no PDF bytes changed.',
 seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,model_work=0))
write(OUT/'analytical_declaration.json',dict(evidence_kind='development_observation',analysis_kind='prospective_analytical_scenarios',
 declared_utc=datetime.now(timezone.utc).isoformat(),adopted=False,not_audit=True,not_simulation=True,
 fixed_rules=['always_D','always_R','observed_positive_benefit','complement_positive_benefit'],
 n_grid=[24,120,450,1200,2400,6000,15000],alpha_grid=[0.01,0.05,0.10],b_min_grid=[0.01,0.05],
 gamma=0.05,range_widths=dict(B=1,Z=1,Delta=2,C='symbolic independently justified W_C'),
 rationale='n=24 anchors observed clusters; 120 small breadth, 450 manuscript placeholder, 1200/2400/6000/15000 display resource scale. Alpha and b_min bracket illustrative risk/exposure magnitudes, never recommended tolerances. All combinations retained; no candidate search.',
 future_moment_assumption='Illustrations hold the 24-row descriptive mean and sample variance fixed as n changes; no duplicated rows or new evidence.',
 delta_score='symbolic, unfrozen test-superiority margin; not the audit noninferiority margin',
 rare_event_grid=dict(p_D=[0.1,0.5],p_R=[0.95,0.99],K=[4,8,16]),
 rare_event_rationale='Algebraic probability of an all-zero empirical harm target under hypothetical independent Bernoulli D/R draws; not fitted probabilities or confidence bounds.',
 resource_comparison=dict(K=[4,8],fresh_breadth_inputs=24,extra_repeats_on_existing_inputs=4),
 no_threshold_search=True,no_gate_fit=True,no_final_audit_path=True))
event=dict(evidence_kind='development_observation',event='P02D_EXECUTION_ACCEPTED_P02E_OFFLINE_AUTHORIZED',timestamp_utc=datetime.now(timezone.utc).isoformat(),
 user_conveyed_date='2026-10-15',timezone='America/Chicago',review='reports/p02e/provenance/P02D_execution_acceptance_review.md',
 review_sha256=archive['docs/P02D_execution_acceptance_review.md'],acceptance_verbatim='Decision: ACCEPTED as completed DEVELOPMENT evidence.',
 accepted_plan_sha256=expected['artifacts/development/p02d-cr01-plan-v4/run_plan.json'],verification='reports/p02e/acceptance_verification.json',
 real_dispatch_enabled=False,p02_sealed=False,p03_started=False,study_frozen=False,previous_state_sha256=sha(ROOT/'configs/phase_state.json'),
 scope='Offline denominator/cost design only; P02D single-run authorization consumed; no new model work.')
write(ROOT/'configs/state_events/023_P02D_execution_accepted_P02E_authorized.json',event)
state.update(active_phase='P02E',status='IN_PROGRESS',checkpoint='OFFLINE_DESIGN_REVIEW',accepted_previous_checkpoint='P02D_EXECUTION',
 accepted_previous_checkpoint_record='configs/state_events/023_P02D_execution_accepted_P02E_authorized.json',latest_event='configs/state_events/023_P02D_execution_accepted_P02E_authorized.json')
temp=ROOT/'configs/phase_state.p02e.pending';write(temp,state);temp.replace(ROOT/'configs/phase_state.json')
print(json.dumps(dict(status='PASS',accepted_files=8997,dispatch=False,active_phase='P02E',model_work=0)))
