"""Reproduce P02E offline outputs in a disposable directory; no model imports."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import time
import p02e_analyze as analysis

def main():
    start, cpu = time.perf_counter(), time.process_time()
    original = analysis.OUT
    compared = {}
    # Explicit workspace parent avoids Windows sandbox system-temp ACL failures.
    with tempfile.TemporaryDirectory(prefix='.p02e-offline-', dir=analysis.ROOT) as tmp:
        assert Path(tmp).resolve().parent == analysis.ROOT.resolve()
        analysis.OUT = Path(tmp)
        for name in ('analytical_declaration.json', 'acceptance_verification.json'):
            shutil.copyfile(original / name, analysis.OUT / name)
        with contextlib.redirect_stdout(io.StringIO()):
            analysis.main()
        runpy.run_path(str(analysis.ROOT / 'scripts/p02e_documents.py'))
        for path in sorted(analysis.OUT.iterdir()):
            if path.name.endswith('_receipt.json'):
                continue
            digest = analysis.sha(path)
            assert digest == analysis.sha(original / path.name), path.name
            compared[path.name] = digest
    analysis.OUT = original
    receipt = dict(status='PASS', compared_files=compared, count=len(compared),
                   wall_seconds=time.perf_counter()-start,
                   cpu_seconds=time.process_time()-cpu, model_work=0,
                   source_sha256=analysis.sha(Path(__file__)))
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
