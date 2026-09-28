"""Offline correction evidence: reviewed-source regression or immutable output replay."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash
from taskcognition.p01_ledger import reconcile,events
from taskcognition.p01_parsing import parse_and_score
from taskcognition.p01_native import native_dataset

root=Path(__file__).resolve().parents[1]
output=root/'reports/p01_correction_v2'
parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['reviewed-tests','replay'])
parser.add_argument('--output',default='preservation_and_replay.json',help='New replay log filename; existing logs are never overwritten')
args=parser.parse_args()
if args.action=='reviewed-tests':
    # Identical final regression tests, actual reviewed modules, isolated import path.
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        with zipfile.ZipFile(root/'reports/p01/P01_review_packet.zip') as archive:
            for name in archive.namelist():
                if name.startswith('src/taskcognition/') and name.endswith('.py'):
                    path=tmp/name
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_bytes(archive.read(name))
        env=os.environ.copy(); env['PYTHONPATH']=str(tmp/'src'); env['PYTHONUTF8']='1'
        command=[sys.executable,'-m','unittest','discover','-s','tests','-p','test_p01_worker_correction.py','-v']
        start=time.perf_counter()
        proc=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8')
        record={'evidence_kind':'fixture','purpose':'final regression suite against unchanged reviewed production code',
            'reviewed_code_commit':'7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322','new_model_calls':0,
            'source':'original verified review ZIP src/taskcognition/*.py',
            'test_sha256':file_hash(root/'tests/test_p01_worker_correction.py'),
            'argv':['.venv/Scripts/python.exe']+command[1:],'exit':proc.returncode,'seconds':time.perf_counter()-start,
            'stdout':proc.stdout,'stderr':proc.stderr.replace(str(Path.home()),'<home>').replace(str(tmp),'<isolated-reviewed-source>')}
        write_new(output/'reviewed_source_final_tests.json',record)
        print(json.dumps({'reviewed_tests_exit':proc.returncode,'tail':record['stderr'][-160:]}))
        assert proc.returncode==1,'Expected meaningful regression failures on reviewed code'
else:
    before=read_json(output/'preservation_before.json')
    for name,expected in before['protected_files'].items():assert file_hash(root/name)==expected,name
    previous_index=read_json(root/'reports/phases/P01_evidence_manifest.json')
    allowed_changes={'configs/phase_state.json','src/taskcognition/p01_ledger.py',
                     'src/taskcognition/p01_smoke.py','src/taskcognition/p01_worker.py'}
    changed=[name for name,expected in previous_index['files'].items() if file_hash(root/name)!=expected]
    assert set(changed)==allowed_changes,changed
    run=root/'artifacts/development/p01-windows-5090-20260928-v2'
    original=read_json(run/'evidence_manifest.json')
    for name,expected in original['files'].items():assert file_hash(run/name)==expected,name
    plan=read_json(root/'configs/p01_resource_plan.json')
    dataset=native_dataset(root,plan['dataset_config'])
    rows=reconcile(run); replay=[]
    for key,row in rows.items():
        request=read_json(run/'requests'/f'{key}.json'); result=row['result']
        assert result['model_error'] is None
        parsed=parse_and_score(result['parsed']['raw_decoded_text'],request['mode'],request['opening_in_prompt'],
            result['finish_reason'],lambda p:dataset.score_answer(p,dataset[request['dataset_index']]))
        assert parsed['native_score']==result['parsed']['native_score']
        assert parsed['strict_valid_final']==result['parsed']['strict_valid_final']
        replay.append({'request_id':key,'score':parsed['native_score'],'valid_final':parsed['strict_valid_final'],
            'model_error':result['model_error'],'request_sha256':file_hash(run/'requests'/f'{key}.json'),
            'result_sha256':file_hash(run/'results'/f'{key}.json')})
    assert [r['score'] for r in replay]==[0.,1.,0.]
    assert len(rows)==3 and len(events(run))==15
    assert sum(r['result']['generated_tokens'] for r in rows.values())==567
    assert 'torch' not in sys.modules and 'transformers' not in sys.modules
    assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
    if Path(args.output).name!=args.output:raise ValueError('output must be a filename')
    write_new(output/args.output,{'evidence_kind':'development_observation',
        'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'protected_file_count':len(before['protected_files']),'original_files_unchanged':True,
        'unchanged_previous_indexed_files':len(previous_index['files'])-len(changed),
        'legitimately_changed_current_paths':changed,
        'request_result_event_fingerprints_unchanged':True,'replayed':replay,
        'historical_admitted':3,'historical_tokens':567,'historical_event_count':15,
        'new_model_loads':0,'new_real_generations':0,'new_gpu_work':0,'new_downloads':0,'dependency_changes':0,
        'D_valid_FINAL_success':False,'native_D_bare_payload_diagnostic_score':dataset.score_answer("['-6.0', '4.0', '6.0']",dataset[0]),
        'interpretation':'D numerically correct but wrapper invalid: primary score stays zero. R score one; interruption distinct. No historical branch impact found.',
        'current_source_files':{p.name:file_hash(p) for p in (root/'src/taskcognition').glob('*.py')}})
    print('PASS: protected files unchanged; 15 events, 3 historical calls, 567 tokens, scores 0/1/0; zero new model activity.')
