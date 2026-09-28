"""Revalidate the accepted P00 snapshot before any P01 backend work."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CODE = '255860890dd480cdd8607e27957b251aa3e1cb1f'
PACKET = '44cb33d8a178de9a15bf5ea3793e7d9ea64f7b6f'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    output = ROOT/'reports/p01/preflight.json'
    if output.exists():
        raise RuntimeError('Preflight log already exists; never overwrite')
    result = {'evidence_kind': 'development_observation', 'purpose': 'P01_local_P00_revalidation',
              'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'code_commit': CODE,
              'packet_commit': PACKET, 'commands': [], 'checks': [], 'model_calls': 0}
    try:
        expected = {'reports/phases/P00_completion.md': 'd92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2',
                    'reports/phases/P00_evidence_manifest.json': 'cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935',
                    'reports/phases/P00_proposed_seal.md': 'e414b43d0d20ed6e69a1aa974be3f50ff00edc8ba4e6250695d67a5c75670331'}
        for name, digest in expected.items():
            assert sha((ROOT/name).read_bytes()) == digest, name
            result['checks'].append({'path': name, 'sha256': digest, 'matches': True})
        subprocess.run(['git', 'merge-base', '--is-ancestor', CODE, PACKET], cwd=ROOT, check=True)
        subprocess.run(['git', 'merge-base', '--is-ancestor', PACKET, 'HEAD'], cwd=ROOT, check=True)
        manifest = json.loads((ROOT/'reports/phases/P00_evidence_manifest.json').read_text(encoding='utf-8'))
        for name, digest in manifest['files'].items():
            snapshot = subprocess.check_output(['git', 'show', PACKET+':'+name], cwd=ROOT)
            assert sha(snapshot) == digest, 'snapshot '+name
            assert sha((ROOT/name).read_bytes()) == digest, 'worktree '+name
        result['indexed_files_verified_in_snapshot_and_worktree'] = len(manifest['files'])
        sources = json.loads((ROOT/'reports/source_inventory.json').read_text(encoding='utf-8'))
        for name, digest in sources['preserved_original_files'].items():
            assert sha((ROOT/name).read_bytes()) == digest, 'original '+name
        result['original_source_files_verified'] = len(sources['preserved_original_files'])
        result['C01_C03_present'] = all(c in (ROOT/'reports/decision_ledger.md').read_text(encoding='utf-8') for c in ['C01', 'C02', 'C03'])
        for args in ([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                     [sys.executable, '-m', 'taskcognition', 'verify-artifacts', '--run', 'artifacts/fixtures/p00-analytical-v2']):
            started = time.perf_counter()
            p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', timeout=120)
            result['commands'].append({'argv': ['.venv/Scripts/python.exe']+args[1:], 'exit': p.returncode,
                                        'stdout': p.stdout, 'stderr': p.stderr, 'seconds': time.perf_counter()-started})
            assert p.returncode == 0, args
        result['status'] = 'PASS'
    except Exception as exc:
        result['status'] = 'FAIL'
        result['failure'] = repr(exc)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['commands','checks']}))
    return 0 if result['status'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
