"""One official pinned snapshot, streamed once; no duplicate weight cache."""
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request
from taskcognition.artifacts import read_json, write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1]
meta=read_json(root/'reports/p01/download_metadata.json')
revision=meta['model_revision']
assert read_json(root/'reports/p01/gpu_check.json')['status']=='PASS'
dest=root/'.cache/p01/Qwen3-8B'/revision
dest.mkdir(parents=True,exist_ok=True)
started=time.perf_counter()
records=[]
for info in meta['model_files']:
    name=info['name']
    if name=='.gitattributes':continue
    path=dest/name
    if path.exists():
        actual=file_hash(path)
        assert path.stat().st_size==info['size']
        if info['lfs']:assert actual==info['lfs']['sha256']
        records.append({'name':name,'bytes':path.stat().st_size,'sha256':actual,'reused':True})
        continue
    partial=path.with_suffix(path.suffix+'.partial')
    if partial.exists():raise RuntimeError('Partial download retained; inspect before an explicit download recovery')
    url=f'https://huggingface.co/Qwen/Qwen3-8B/resolve/{revision}/{name}?download=true'
    h=hashlib.sha256()
    begin=time.perf_counter()
    print('Downloading '+name+' ('+str(info['size'])+' bytes)',flush=True)
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'TaskCognition-P01'}),timeout=60) as r, partial.open('xb') as f:
        while chunk:=r.read(1024*1024):
            h.update(chunk)
            f.write(chunk)
        f.flush()
        os.fsync(f.fileno())
    assert partial.stat().st_size==info['size'],name
    if info['lfs']:assert h.hexdigest()==info['lfs']['sha256'],name
    partial.rename(path)
    records.append({'name':name,'bytes':path.stat().st_size,'sha256':h.hexdigest(),'seconds':time.perf_counter()-begin,'reused':False})
    print('Verified '+name,flush=True)
write_new(root/'reports/p01/model_download.json',{'evidence_kind':'development_observation',
          'model_id':'Qwen/Qwen3-8B','revision':revision,'local_directory':dest.relative_to(root).as_posix(),
          'files':records,'elapsed_seconds':time.perf_counter()-started,'total_bytes':sum(r['bytes'] for r in records)})
print('Pinned snapshot complete; all weight LFS SHA-256 hashes verified.',flush=True)
