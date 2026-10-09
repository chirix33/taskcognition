"""Append the offline correction checkpoint; never execution authorization."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_correction_v3'
stamp=datetime.now(timezone.utc).isoformat();statepath=root/'configs/phase_state.json'
state=read_json(statepath);assert not state['real_dispatch_enabled'] and state['active_phase']=='P02D'
sha=read_json(out/'plan_receipt.json')['sha256']
snapshot=root/'configs/state_snapshots/P02D_preflight_v2_before_v3.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
eventpath='configs/state_events/018_P02D_corrected_preflight_v3_review_checkpoint.json'
write_new(root/eventpath,dict(evidence_kind='development_observation',event='P02D_CORRECTED_PREFLIGHT_READY_FOR_REVIEW',
 timestamp_utc=stamp,previous_state_sha256=file_hash(snapshot),superseded_plan_sha256=state['p02d_plan_sha256'],active_plan_sha256=sha,
 authority='user-conveyed P02D correction instructions; not execution acceptance',prompt_sha256=file_hash(out/'coordinator/P02D_preflight_correction_prompt.md'),
 reproduction_bundle_sha256=file_hash(out/'coordinator/P02D_coordinator_reproductions.zip'),real_dispatch_enabled=False,
 new_model_work=0,p02_sealed=False,p03_started=False,identical_materialized_files=256))
state.update(status='READY_FOR_REVIEW',checkpoint='CORRECTED_PREFLIGHT',latest_event=eventpath,p02d_plan_sha256=sha)
statepath.write_bytes(canonical(state)+b'\n')
tracking=subprocess.check_output(['git','rev-parse','refs/remotes/origin/codex/p02c-cr01-adoption'],text=True).strip()
ancestry={c:subprocess.run(['git','merge-base','--is-ancestor',c,tracking]).returncode==0 for c in ('4b0c200','53129ba')}
note=f'''# P02D v3 provenance correction

Recorded {stamp}. The user's latest correction is **“nothing pushed.”** This supersedes the user's earlier pushed handoff. Earlier P02C/P02D reports, indexes, receipts and ZIPs remain unchanged as historical records; their push-related interpretation is not a current backup claim.

Read-only local Git evidence: refs/remotes/origin/codex/p02c-cr01-adoption = {tracking}; local ancestry checks: {ancestry}. This is cached local tracking state only. It establishes neither a current push nor current remote contents nor verified remote backup. No remote query, push, merge, external transfer or history rewrite occurred in this correction. Local packets remain verified; off-machine coverage is unverified. No new backup purchase requirement is imposed.

The P02C external packet receipt remains included through the preserved v2 packet and its original reports/p02d/P02C_external_packet_receipt.json. No new coordinator GPU verification is claimed. Original reference PDF and historical source snapshots remain unchanged.
'''
(out/'provenance_correction.md').write_text(note,encoding='utf-8')
with (root/'reports/decision_ledger.md').open('a',encoding='utf-8') as f:f.write(f'''\n## P02D offline v3 correction ({stamp})
User authorizes only R1 complete no-overwrite publication and R2 operational-stop classification. v2 {read_json(snapshot)['p02d_plan_sha256']} remains preserved; v3 {sha} binds corrected source with all 256 materialized files unchanged. No P02D execution acceptance or authorization exists. User corrected the earlier push handoff to **“nothing pushed.”** Local remote-tracking ancestry is separate and cannot establish a push or verified remote backup. See reports/p02d_correction_v3/provenance_correction.md. Zero model/GPU work; dispatch false; P02 incomplete/unsealed; P03 unstarted.\n''')
print(sha)
