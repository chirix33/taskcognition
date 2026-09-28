"""Record P01 review readiness, never seal or activate P02."""
from datetime import datetime, timezone
from pathlib import Path
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash,canonical

root=Path(__file__).resolve().parents[1]
state=root/'configs/phase_state.json'
previous=state.read_bytes()
data=read_json(state)
assert data['active_phase']=='P01' and data['status']=='IN_PROGRESS'
snapshot=root/'configs/state_snapshots/P01_IN_PROGRESS.json'
with snapshot.open('xb') as f:f.write(previous)
event=root/'configs/state_events/002_P01_ready_for_review.json'
write_new(event,{'evidence_kind':'development_observation','event':'phase_ready_for_review',
    'timestamp_utc':datetime.now(timezone.utc).isoformat(),'active_phase':'P01','status':'READY_FOR_REVIEW',
    'previous_state_sha256':file_hash(snapshot),'accepted_previous_phase':'P00','authorized_next_phase':None,
    'acceptance':'P01 acceptance pending; no self seal','admitted_generations':3,'output_tokens':567,
    'tests':'reports/p01/offline_tests_final.json','limitations':['No live valid-FINAL D example; original failure retained'],
    'completion_report':'reports/phases/P01_completion.md'})
data.update(status='READY_FOR_REVIEW',latest_event=event.relative_to(root).as_posix())
state.write_bytes(canonical(data)+b'\n')
print('P01 READY_FOR_REVIEW; P00 remains SEALED; no next phase authorized')
