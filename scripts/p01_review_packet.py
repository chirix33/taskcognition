"""Build a compact private review packet from an explicit allowlist; no model files."""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess
import zipfile
from taskcognition.artifacts import read_json, write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1]
execution='683e9a3f7c5c539a3bb5d8d959b98d4c9319721f'
index=root/'reports/phases/P01_evidence_manifest.json'
parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['index','zip'])
args=parser.parse_args()
if args.action=='index':
    selected=set()
    for directory in ['src','tests','scripts','configs','vendor/reasoning_gym_p01','reports/p01',
                      'artifacts/development/p01-windows-5090-20260928',
                      'artifacts/development/p01-windows-5090-20260928-v2',
                      'artifacts/fixtures/p00-analytical-v2']:
        for path in (root/directory).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc','.zip'):
                selected.add(path.relative_to(root).as_posix())
    for path in (root/'docs').glob('*.md'):selected.add(path.relative_to(root).as_posix())
    selected.update(['AGENTS.md','README.md','pyproject.toml','.gitignore','.gitattributes',
        'docs/templates/PHASE_COMPLETION_TEMPLATE.md','docs/prompts/P01_reviewed_local_qwen.md',
        'docs/prompts/P01_local_qwen.md','docs/prompts/P00_coordinator_review.md',
        'reports/phases/P00_completion.md','reports/phases/P00_proposed_seal.md',
        'reports/phases/P00_accepted_seal.md','reports/phases/P00_evidence_manifest.json',
        'reports/decision_ledger.md','reports/source_inventory.json','reference/TaskCognition_Revised_Verified.pdf'])
    files={name:file_hash(root/name) for name in sorted(selected)}
    old_names=subprocess.check_output(['git','ls-tree','-r','--name-only',execution,'--','src','tests','pyproject.toml'],cwd=root,text=True).splitlines()
    snapshots={name:hashlib.sha256(subprocess.check_output(['git','show',execution+':'+name],cwd=root)).hexdigest() for name in old_names}
    write_new(index,{'evidence_kind':'development_observation','phase':'P01','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'final_code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        'execution_code_commit':execution,'files':files,'executed_snapshot_files':snapshots,
        'index_exclusions':'This index, P01 completion/proposed seal, ZIP and external ZIP receipt are excluded to avoid circular hashes. ZIP contains all indexed files plus completion/seal/index and executed_source snapshot.',
        'excluded_large_or_private_content':'Weights, environments, caches, private meetings, original manuscript history, unrelated files. Published model weight hashes remain in model_download.json.'})
    print('Indexed',len(files),'files;',len(snapshots),'executed source snapshots')
else:
    data=read_json(index)
    contents={}
    for name,expected in data['files'].items():
        assert file_hash(root/name)==expected,name
        contents[name]=(root/name).read_bytes()
    for name,expected in data['executed_snapshot_files'].items():
        content=subprocess.check_output(['git','show',execution+':'+name],cwd=root)
        assert hashlib.sha256(content).hexdigest()==expected,name
        contents['executed_source/'+name]=content
    for name in ['reports/phases/P01_evidence_manifest.json','reports/phases/P01_completion.md','reports/phases/P01_proposed_seal.md']:
        contents[name]=(root/name).read_bytes()
    output=root/'reports/p01/P01_review_packet.zip'
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,content in sorted(contents.items()):archive.writestr(name,content)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist())==set(contents)
        assert all(archive.read(name)==content for name,content in contents.items())
    write_new(root/'reports/phases/P01_packet_receipt.json',{'evidence_kind':'development_observation',
        'zip_path':output.relative_to(root).as_posix(),'zip_sha256':file_hash(output),'zip_bytes':output.stat().st_size,
        'entries':len(contents),'all_entries_read_back_verified':True,
        'evidence_manifest_sha256':file_hash(index),'completion_sha256':file_hash(root/'reports/phases/P01_completion.md'),
        'proposed_seal_sha256':file_hash(root/'reports/phases/P01_proposed_seal.md'),
        'final_code_commit':data['final_code_commit'],'execution_code_commit':execution,
        'report_packet_commit_locator':'The separate local Git commit containing this receipt; its identity is reported after committing, avoiding a self-referential hash.'})
    print('Verified ZIP:',output.name,output.stat().st_size,'bytes;',len(contents),'entries')
