"""Check historical fingerprints after legitimate P01 code/state evolution."""
import hashlib
from pathlib import Path
import subprocess
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1]
packet='44cb33d8a178de9a15bf5ea3793e7d9ea64f7b6f'
manifest=root/'reports/phases/P00_evidence_manifest.json'
assert file_hash(manifest)=='cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935'
changed=[]
for name,expected in read_json(manifest)['files'].items():
    original=subprocess.check_output(['git','show',packet+':'+name],cwd=root)
    assert hashlib.sha256(original).hexdigest()==expected,name
    if file_hash(root/name)!=expected:changed.append(name)
assert file_hash(root/'reports/phases/P00_completion.md')=='d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2'
assert file_hash(root/'reports/phases/P00_proposed_seal.md')=='e414b43d0d20ed6e69a1aa974be3f50ff00edc8ba4e6250695d67a5c75670331'
for name,expected in read_json(root/'reports/source_inventory.json')['preserved_original_files'].items():
    assert file_hash(root/name)==expected,name
assert all(not p.startswith(('reports/','artifacts/fixtures/','docs/','reference/')) for p in changed),changed
write_new(root/'reports/p01/p00_preservation_final.json',{'evidence_kind':'development_observation',
          'P00_snapshot_verified':True,'snapshot_commit':packet,'indexed_files':162,
          'P00_reports_fixtures_original_sources_unchanged':True,'legitimately_evolved_current_paths':changed})
print('P00 snapshot, original sources, reports and fixtures preserved; current code/state changes:',changed)
