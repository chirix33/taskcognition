"""Verify P02C and record the single conveyed offline acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess, zipfile
from taskcognition.artifacts import read_json, write_new
from taskcognition.contracts import file_hash, canonical

root = Path(__file__).resolve().parents[1]
out = root / 'reports/p02d'
expected = {
 'reports/p02c/P02C_review_packet.zip':'287e8032566d2d284e8856b84eb9f9a53cf9b35064b6c9e94e98a6a684308407',
 'reports/p02c/P02C_evidence_index.json':'3daef8e6d92b50ed25ec44d16d19788c848c7bffa09dc83048c2ba22a5c42b0e',
 'reports/phases/P02C_completion.md':'cf601dcc2ee336e427825a9236898d1d8a2fa9fa2d82c5fc9c7a14eaa7af6a12',
 'reports/p02c/next_development_proposal.md':'c4dabc27a0871ee0675e39cc33b0b14c06d6a36a043e65387d688f0818ee14b9'}
for n, h in expected.items(): assert file_hash(root/n) == h, n
index = read_json(root/'reports/p02c/P02C_evidence_index.json')['files']
with zipfile.ZipFile(root/'reports/p02c/P02C_review_packet.zip') as z:
    assert z.testzip() is None
    for n,h in index.items():
        assert hashlib.sha256(z.read(n)).hexdigest() == h == file_hash(root/n), n
statepath = root/'configs/phase_state.json'
state = read_json(statepath)
assert state['active_phase'] == 'P02C' and not state['real_dispatch_enabled']
now = datetime.now(timezone.utc).isoformat()
out.mkdir(exist_ok=True)
for src, dest in [('docs/prompts/P02D_offline_preflight_prompt.md','authorization_prompt.md'),
                  ('docs/P02C_coordinator_review.md','P02C_coordinator_review.md'),
                  ('reports/p02c/P02C_packet_receipt.json','P02C_external_packet_receipt.json')]:
    target=out/dest
    with target.open('xb') as f: f.write((root/src).read_bytes())
refs = subprocess.check_output(['git','for-each-ref','--format=%(refname:short) %(objectname)','refs/remotes'],text=True)
commits = {}
for short in ('4b0c200','53129ba'):
    commit=subprocess.check_output(['git','rev-parse',short],text=True).strip()
    assert subprocess.run(['git','merge-base','--is-ancestor',commit,'origin/codex/p02c-cr01-adoption']).returncode==0
    commits[short]=commit
build=root/'docs/P02C_coordinator_build_evidence.zip'
derivative={'supplied':build.exists(),'coordinator_claimed_pdf_sha256':'a97b04ac1bf319abef5f10b93630b01ea31d3f9798977509e60efc019eef9859',
            'compiled_by':'coordinator external environment, not Codex workstation','reported_pages':13}
if build.exists():
    shutil.copyfile(build,out/'P02C_coordinator_build_evidence.zip')
    with zipfile.ZipFile(build) as z:
        assert z.testzip() is None
        derivative.update(archive_sha256=file_hash(build),members={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()},
                          pdf_supplied=any(n.lower().endswith('.pdf') for n in z.namelist()))
        for name in ['P02C_coordinator_verification.json','build/build_commands.json']:
            derivative[name]=json.loads(z.read(name))
write_new(out/'acceptance_verification.json',dict(evidence_kind='development_observation',timestamp_utc=now,
    accepted_hashes=expected,indexed_files_verified=len(index),current_files_match=True,commits=commits,
    source_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
    prompt_sha256=file_hash(out/'authorization_prompt.md'),review_sha256=file_hash(out/'P02C_coordinator_review.md'),
    prior_receipt_sha256=file_hash(out/'P02C_external_packet_receipt.json'),local_tracking_refs=refs,external_derivative=derivative))
note=f'''# P02C acceptance and provenance follow-up — 2026-10-09

Actual record time: {now}. The user conveys `docs/P02C_coordinator_review.md`: **accept P02C as the completed offline CR01-adoption checkpoint**. The four accepted hashes and all 115 indexed ZIP/current files passed before source changes. See `acceptance_verification.json`. This is one checkpoint acceptance, not a P02 seal.

The earlier P02C report's no-push statement describes Codex's work at that checkpoint. The user's later handoff reports commits 4b0c200 and 53129ba pushed on codex/p02c-cr01-adoption. Local origin/codex/p02c-cr01-adoption points to 55e8fbde2f43b43cfbf0b8cfaf840d3ed0998b22 and contains both commits. This is consistent with a subsequent push. No fetch, remote inspection, push, transfer or remote restore was performed here; current remote contents and complete off-machine coverage are unverified. Those commits include source and local review packets (the P02C packet nests accepted P02B evidence); ignored weights/environments and any other ignored raw files are not thereby proven backed up. Durable final-study backup remains open, not a precondition imposed on this offline diagnostic.

The supplied coordinator build archive is preserved with member hashes and external attribution. It contains logs/renders/build metadata, but no PDF member. The claimed 13-page PDF hash is recorded as coordinator-supplied, not locally verified PDF bytes. No derivative PDF is substituted for the governing reference. The workstation's historical unavailable-build statement remains true. The existing external P02C receipt is included in this handoff, not claimed independently checked by the earlier coordinator review.
'''
(out/'provenance_followup.md').write_text(note,encoding='utf-8')
(root/'reports/phases/P02C_accepted_checkpoint.md').write_text(note.split('The earlier')[0],encoding='utf-8')
snapshot=root/'configs/state_snapshots/P02C_accepted_before_P02D.json'
with snapshot.open('xb') as f:f.write(statepath.read_bytes())
event='configs/state_events/015_P02C_accept_P02D_offline.json'
write_new(root/event,dict(evidence_kind='development_observation',timestamp_utc=now,event='P02C_accepted_P02D_offline_authorized',
    acceptance_reference='docs/P02C_coordinator_review.md',acceptance_hash=file_hash(out/'P02C_coordinator_review.md'),
    previous_state_sha256=file_hash(snapshot),p01_sealed=True,p02a_accepted=True,p02b_accepted=True,p02c_accepted=True,
    p02_sealed=False,p03_started=False,real_dispatch_enabled=False,answer_slots_authorized=0,feature_forwards_authorized=0))
state.update(active_phase='P02D',status='IN_PROGRESS',real_dispatch_enabled=False,accepted_previous_checkpoint='P02C',
    accepted_previous_checkpoint_record='reports/phases/P02C_accepted_checkpoint.md',latest_event=event)
statepath.write_bytes(canonical(state)+b'\n')
with (root/'reports/decision_ledger.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## P02D offline authorization ({now})\nP02C accepted once via docs/P02C_coordinator_review.md; verified 115 indexed files and four accepted hashes. CR01 approval unchanged. P02D preparation only; dispatch false, no live slots/forwards authorized. P02 incomplete/unsealed; P03 unstarted. See reports/p02d/acceptance_verification.json and provenance_followup.md.\n')
print('PASS: accepted P02C once; offline P02D active, dispatch false')
