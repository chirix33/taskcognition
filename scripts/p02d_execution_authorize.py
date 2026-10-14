"""Adopt conveyed approval once; creates no model process or real run slot."""
from pathlib import Path
from datetime import datetime,timezone
from taskcognition.artifacts import read_json
from taskcognition.contracts import file_hash
from taskcognition.p02d_plan import PLAN_DIR,RUN,LIMITS,require_authorization
from taskcognition.p02d_publication import write_new,replace_state

root=Path(__file__).resolve().parents[1];out=root/'reports/p02d_execution'
sha='c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365'
assert read_json(out/'preflight.json')['status']=='PASS'
assert not (root/RUN).exists() and not (root/'configs/p02d_execution_authorization.json').exists()
statepath=root/'configs/phase_state.json';state=read_json(statepath)
assert state['active_phase']=='P02D' and state['real_dispatch_enabled'] is False and state['p02d_plan_sha256']==sha
stamp=datetime.now(timezone.utc).isoformat()
reference="User-conveyed execution handoff in this TaskCognition conversation: approval dated 2026-10-14 America/Chicago, verbatim 'Yes I do.' in response to the coordinator's explicit one-v4-run request. No message ID or approval time-of-day was supplied."
write_new(out/'approval_adoption.json',dict(evidence_kind='development_observation',user_approval_verbatim='Yes I do.',user_approval_date='2026-10-14',
 approval_timezone='America/Chicago',user_approval_time_of_day=None,user_message_reference=reference,workstation_adoption_utc=stamp,
 coordinator_acceptance_date='2026-10-09',coordinator_acceptance_time_of_day=None,coordinator_review_sha256=file_hash(out/'authority/P02D_v4_acceptance_review.md'),
 plan_sha256=sha,invocations_authorized=1,source_changes_authorized=False))
write_new(root/'configs/state_snapshots/P02D_v4_before_execution_authorization.json',state)
acceptance='configs/state_events/020_P02D_v4_preflight_accepted.json'
write_new(root/acceptance,dict(event='P02D_V4_PREFLIGHT_ACCEPTED',timestamp_utc=stamp,review_date='2026-10-09',
 review_path='reports/p02d_execution/authority/P02D_v4_acceptance_review.md',review_sha256=file_hash(out/'authority/P02D_v4_acceptance_review.md'),
 evidence_kind='development_observation',plan_sha256=sha,real_dispatch_enabled=False,p02_sealed=False,p03_started=False,
 note='Coordinator preflight acceptance recorded separately from user execution approval; no new scientific freeze.'))
erratum=("# Append-only P02D corrected preflight erratum\n\nRecorded "+stamp+". The historical corrected completion sentence saying the next request is 'now bound to v3' means **v4**, SHA-256 `"+sha+"`. The historical report, review ZIP and bound source bytes are unchanged. This is a documentation erratum conveyed by the accepted coordinator review, not a plan revision.\n")
with (out/'preflight_report_erratum.md').open('x',encoding='utf-8',newline='\n') as f:f.write(erratum)
authpath=root/'configs/p02d_execution_authorization.json'
write_new(authpath,dict(phase='P02D',authorized=True,plan_sha256=sha,limits=LIMITS,user_message_reference=reference,
 approval_verbatim='Yes I do.',approval_date='2026-10-14',approval_timezone='America/Chicago',adopted_at_utc=stamp,invocations=1))
event='configs/state_events/021_P02D_v4_execution_authorized.json'
write_new(root/event,dict(event='P02D_V4_EXECUTION_AUTHORIZED',evidence_kind='development_observation',timestamp_utc=stamp,
 approval_record='reports/p02d_execution/approval_adoption.json',approval_record_sha256=file_hash(out/'approval_adoption.json'),
 previous_state_sha256=file_hash(statepath),authorization_sha256=file_hash(authpath),plan_sha256=sha,
 real_dispatch_enabled=True,p02_sealed=False,p03_started=False,one_invocation_only=True))
state.update(status='EXECUTION_AUTHORIZED',checkpoint='BOUNDED_DEVELOPMENT_EXECUTION',real_dispatch_enabled=True,
 p02d_authorization_sha256=file_hash(authpath),p02d_plan_sha256=sha,latest_event=event,
 accepted_previous_checkpoint='P02D_V4_PREFLIGHT',accepted_previous_checkpoint_record=acceptance)
replace_state(statepath,state)
require_authorization(root,root/PLAN_DIR/'run_plan.json',sha)
write_new(out/'authorization_check.json',dict(status='PASS',completed_utc=datetime.now(timezone.utc).isoformat(),
 authorization_sha256=file_hash(authpath),plan_sha256=sha,production_authorization_check=True,model_work=0))
print('PASS: conveyed approval adopted, exact v4 authorization bound; no invocation started by this script.')
