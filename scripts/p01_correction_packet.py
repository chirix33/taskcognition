"""Versioned offline-correction review packet; never replace the original packet."""
import argparse
from pathlib import Path
import subprocess
import zipfile
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['index','zip'])
args=parser.parse_args()
index=root/'reports/phases/P01_evidence_manifest_v2.json'
if args.action=='index':
    old=read_json(root/'reports/phases/P01_evidence_manifest.json')
    names=set(old['files'])
    names.update(['reports/P01_coordinator_review.md','tests/test_p01_worker_correction.py',
        'scripts/p01_correction_verify.py','scripts/p01_correction_packet.py',
        'reports/phases/P01_completion.md','reports/phases/P01_proposed_seal.md',
        'reports/phases/P01_evidence_manifest.json','reports/phases/P01_packet_receipt.json',
        'reports/p01/P01_review_packet.zip'])
    for folder in ['reports/p01_correction_v2','configs/state_events','configs/state_snapshots']:
        names.update(p.relative_to(root).as_posix() for p in (root/folder).glob('*') if p.is_file() and p.suffix!='.zip')
    write_new(index,{'evidence_kind':'development_observation','phase':'P01','revision':'targeted-correction-v2',
        'corrected_code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'original_execution_commit':'683e9a3f7c5c539a3bb5d8d959b98d4c9319721f',
        'reviewed_code_commit':'7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322',
        'files':{name:file_hash(root/name) for name in sorted(names)},
        'historical_packet':'reports/p01/P01_review_packet.zip contains unchanged original index, report, seal, all 215 indexed files and 17 executed snapshot files.',
        'hash_cycle_exclusions':'This v2 index, v2 completion/proposed seal, v2 ZIP and external v2 receipt are excluded from this file map. Receipt hashes the completed packet.',
        'no_new_generation':True,'historical_admitted':3,'historical_tokens':567})
    print('Indexed',len(names),'files, including unchanged historical packet')
else:
    data=read_json(index)
    names=set(data['files'])
    for name,expected in data['files'].items():assert file_hash(root/name)==expected,name
    names.update(['reports/phases/P01_completion_v2.md','reports/phases/P01_proposed_seal_v2.md',
                  'reports/phases/P01_evidence_manifest_v2.json'])
    path=root/'reports/p01_correction_v2/P01_review_packet_v2.zip'
    with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name in sorted(names):z.write(root/name,name)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert set(z.namelist())==names
        for name in names:assert z.read(name)==(root/name).read_bytes(),name
    write_new(root/'reports/phases/P01_packet_receipt_v2.json',{
        'evidence_kind':'development_observation','zip_path':path.relative_to(root).as_posix(),
        'zip_sha256':file_hash(path),'zip_bytes':path.stat().st_size,'entries':len(names),
        'all_entries_read_back_verified':True,'corrected_code_commit':data['corrected_code_commit'],
        'completion_sha256':file_hash(root/'reports/phases/P01_completion_v2.md'),
        'proposed_seal_sha256':file_hash(root/'reports/phases/P01_proposed_seal_v2.md'),
        'evidence_manifest_sha256':file_hash(index),
        'packet_commit_locator':'Separate local commit containing this receipt; identity given at delivery, not embedded in itself.'})
    print('Verified',len(names),'entries;',path.stat().st_size,'bytes')
