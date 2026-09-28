"""Read-only final verification; no model imports or generation."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
import taskcognition
from taskcognition.artifacts import read_json, write_new
from taskcognition.contracts import file_hash
from taskcognition.p01_ledger import reconcile

root=Path(__file__).resolve().parents[1]
execution='683e9a3f7c5c539a3bb5d8d959b98d4c9319721f'
run=root/'artifacts/development/p01-windows-5090-20260928-v2'
manifest=read_json(run/'evidence_manifest.json')
for name,expected in manifest['files'].items():
    assert file_hash(run/name)==expected, name
package=read_json(run/'package.json')
for name,expected in package['source_files'].items():
    data=subprocess.check_output(['git','show',execution+':src/taskcognition/'+name],cwd=root)
    assert hashlib.sha256(data).hexdigest()==expected, name
source={p.name:file_hash(p) for p in (root/'src/taskcognition').glob('*.py')}
installed=Path(taskcognition.__file__).parent
assert all(file_hash(installed/name)==value for name,value in source.items())
rows=reconcile(run)
assert len(rows)==3 and all(r['state']=='COMPLETE' and r['resource_recorded'] for r in rows.values())
assert sum(r['result']['generated_tokens'] for r in rows.values())==567
assert 'torch' not in sys.modules and 'transformers' not in sys.modules
write_new(root/'reports/p01/final_source_verification.json',{
    'evidence_kind':'development_observation','status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'execution_source_commit':execution,'execution_source_hashes_verified':True,
    'immutable_run_files_verified':len(manifest['files']),'admitted':3,'output_tokens':567,
    'final_taskcognition_version':taskcognition.__version__,'final_source_files':source,
    'installed_source_matches':True,'final_distributions':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
    'model_imported':False,'new_generation':False,
    'correction_scope':'unexercised supervisor unexpected-exit integrity handling; no recorded result invalidated'})
print(json.dumps({'status':'PASS','run_files':len(manifest['files']),'admitted':3,'tokens':567,'version':taskcognition.__version__}))
