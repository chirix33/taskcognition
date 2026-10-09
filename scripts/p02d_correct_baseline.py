"""Verify and archive the submitted snapshot before correction; no model imports."""
from pathlib import Path
import hashlib, json, shutil, zipfile, subprocess, os
from datetime import datetime, timezone

root=Path(__file__).resolve().parents[1]
out=root/'reports/p02d_correction_v3';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
expected={
 'artifacts/development/p02d-cr01-plan-v2/run_plan.json':'67c3f5ee03ee25f077356e7ef27cb2d870d54caef12318dbe9bfab0b6688ab3d',
 'reports/p02d/P02D_preflight_review_packet.zip':'4a2c8a6834fbbebdd77ce1659bf9819aa61f152a82230fb282d57c916ba7f91b',
 'reports/p02d/P02D_evidence_index.json':'a05958cf01a877a9510c7b85bb2d40d6008c6e1014ca2509e1a06370bc35d993'}
for n,h in expected.items():assert sha((root/n).read_bytes())==h,n
index=json.loads((root/'reports/p02d/P02D_evidence_index.json').read_text())['files']
assert len(index)==400
with zipfile.ZipFile(root/'reports/p02d/P02D_preflight_review_packet.zip') as z:
 assert z.testzip() is None
 for n,h in index.items():
  assert sha(z.read(n))==h,n
  assert sha((root/n).read_bytes())==h,n
archive=out/'coordinator';archive.mkdir()
for n in ['docs/P02D_coordinator_reproductions.zip','docs/prompts/P02D_preflight_correction_prompt.md']:
 shutil.copyfile(root/n,archive/Path(n).name)
with zipfile.ZipFile(archive/'P02D_coordinator_reproductions.zip') as z:
 for n in z.namelist():
  assert '/' not in n and '\\' not in n
  (archive/n).write_bytes(z.read(n))
tmp=root/'tmp/p02d-tests';tmp.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env.update(TEMP=str(tmp),TMP=str(tmp))
command=[str(root/'.venv/Scripts/python.exe'),str(archive/'p02d_review_reproductions.py'),str(root)]
p=subprocess.run(command,env=env,capture_output=True,text=True)
(out/'baseline_reproductions.json').write_text(json.dumps(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr),indent=2)+'\n')
assert p.returncode==0,p.stderr
(out/'baseline_verification.json').write_text(json.dumps(dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),accepted_hashes=expected,
 indexed_zip_and_current_files_verified=len(index),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 archive_hashes={p.name:sha(p.read_bytes()) for p in archive.iterdir()},model_work=0),indent=2)+'\n')
print('PASS: 400 snapshot/current files; both old-source defects reproduced CPU-only.')
