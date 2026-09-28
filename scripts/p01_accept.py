"""Record user-conveyed report-level acceptance after local revalidation."""
from datetime import datetime, timezone
import json
from pathlib import Path
from taskcognition.artifacts import write_new
from taskcognition.contracts import file_hash, canonical

root = Path(__file__).resolve().parents[1]
preflight = root/'reports/p01/preflight.json'
assert json.loads(preflight.read_text(encoding='utf-8'))['status'] == 'PASS'
timestamp = datetime.now(timezone.utc).isoformat()
review = root/'docs/prompts/P00_coordinator_review.md'
prompt = root/'docs/prompts/P01_reviewed_local_qwen.md'
with prompt.open('xb') as f:
    f.write((root/'docs/prompts/P01_reviwed_local_qwen.md').read_bytes())
state = root/'configs/phase_state.json'
snapshot = root/'configs/state_snapshots/P00_READY_FOR_REVIEW.json'
snapshot.parent.mkdir(parents=True, exist_ok=True)
with snapshot.open('xb') as f:
    f.write(state.read_bytes())
accepted = root/'reports/phases/P00_accepted_seal.md'
with accepted.open('x', encoding='utf-8', newline='\n') as f:
    f.write(f'''# P00 accepted seal

Status: **ACCEPTED**; P00 is **SEALED** by user-conveyed coordinator acceptance.

- Acceptance recorded at: `{timestamp}` (UTC).
- Authority: current user's "Reviewed P01 prompt: Windows / RTX 5090 local Qwen smoke",
  preserved at `docs/prompts/P01_reviewed_local_qwen.md`, SHA-256 `{file_hash(prompt)}`.
- Coordinator review: `docs/prompts/P00_coordinator_review.md`, SHA-256 `{file_hash(review)}`.
- Review limitation: report-level acceptance only. The coordinator did not inspect the
  repository or rerun tests. This is not independent external code verification.
- Local revalidation: `reports/p01/preflight.json`, SHA-256 `{file_hash(preflight)}`;
  162 indexed files matched both P00 snapshot and worktree, 30 original files matched,
  C01-C03 present, 34 offline tests and current fixture verification passed.
- Completion report SHA-256: `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`.
- Evidence index SHA-256: `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`.
- Proposed seal SHA-256: `e414b43d0d20ed6e69a1aa974be3f50ff00edc8ba4e6250695d67a5c75670331`; unchanged.
- Implementation commit: `255860890dd480cdd8607e27957b251aa3e1cb1f`.
- Report-packet commit: `44cb33d8a178de9a15bf5ea3793e7d9ea64f7b6f`.
- Original phase-state snapshot: `{snapshot.relative_to(root).as_posix()}`,
  SHA-256 `{file_hash(snapshot)}`; also preserved in the P00 commit.
- User acceptance reference: "The user is conveying the coordinator's P00 report-level
  acceptance and authorizing this P01 scope." The reviewed prompt supersedes only
  the generic P01 prompt for this run. C01-C03 remain resolved.
- Authorized next phase: **P01 only**, reviewed eight-generation/40-GiB envelope.
- Scientific study/candidate/deployment freezes: NONE. P00 is engineering acceptance.

No old evidence hashes were changed. Future P01 source/state changes are checked against
the P00 Git snapshot, not misrepresented as unchanged current files. No final labels,
real generation, training, or held-out exposure occurred in the P00 revalidation.
''')
event = {'evidence_kind':'development_observation','timestamp_utc':timestamp,
         'event':'phase_acceptance_and_activation','previous_state_sha256':file_hash(snapshot),
         'accepted_phase':'P00','accepted_status':'SEALED','active_phase':'P01','status':'IN_PROGRESS',
         'acceptance_record':'reports/phases/P00_accepted_seal.md','acceptance_sha256':file_hash(accepted),
         'authorized_prompt_sha256':file_hash(prompt),'authorized_next_phase':None}
write_new(root/'configs/state_events/001_P00_accept_P01_start.json',event)
state.write_bytes(canonical({'active_phase':'P01','status':'IN_PROGRESS','accepted_previous_phase':'P00',
                            'accepted_previous_seal':'reports/phases/P00_accepted_seal.md',
                            'latest_event':'configs/state_events/001_P00_accept_P01_start.json',
                            'authorized_next_phase':None,'study_freeze':None})+b'\n')
print('P00 acceptance recorded; P01 IN_PROGRESS; historical state and proposed seal preserved.')
