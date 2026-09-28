"""Inspect official wheel sizes, pin download lock and smoke disk plan."""
import io
import json
from pathlib import Path
import urllib.request
import zipfile
from taskcognition.artifacts import write_new

root = Path(__file__).resolve().parents[1]
resolution = json.loads((root/'reports/p01/pip_resolve.json').read_text(encoding='utf-8'))
metadata = json.loads((root/'reports/p01/download_metadata.json').read_text(encoding='utf-8'))
files=[]
for item in resolution['install']:
    url=item['download_info']['url']
    request=urllib.request.Request(url,headers={'User-Agent':'pip/25.0.1','Range':'bytes=0-0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        size=int(response.headers['Content-Range'].split('/')[-1]) if response.status==206 else int(response.headers['Content-Length'])
    files.append({'name':item['metadata']['name'],'version':item['metadata']['version'],
                  'url':url,'bytes':size,'sha256':item['download_info']['archive_info']['hashes']['sha256']})

class Remote(io.RawIOBase):
    def __init__(self,url,size): self.url,self.size,self.pos=url,size,0
    def seek(self,offset,whence=0):
        self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.size+offset
        return self.pos
    def tell(self): return self.pos
    def seekable(self): return True
    def read(self,n=-1):
        n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
        if n==0:return b''
        req=urllib.request.Request(self.url,headers={'User-Agent':'pip/25.0.1','Range':f'bytes={self.pos}-{self.pos+n-1}'})
        with urllib.request.urlopen(req,timeout=60) as r:
            if r.status!=206: raise RuntimeError('Range access unavailable; cannot inspect wheel expansion')
            data=r.read(n)
        self.pos+=len(data)
        return data
torch=next(x for x in files if x['name']=='torch')
with zipfile.ZipFile(Remote(torch['url'],torch['bytes'])) as z:
    expanded=sum(i.file_size for i in z.infolist())
weights=sum(f['size'] for f in metadata['model_files'])
other=sum(f['bytes'] for f in files if f['name']!='torch')
estimate=weights+sum(f['bytes'] for f in files)+expanded+other*5+2*1024**3
assert estimate<40*1024**3
write_new(root/'configs/p01_download_lock.json',{'evidence_kind':'development_observation','files':files,
          'model_id':'Qwen/Qwen3-8B','model_revision':metadata['model_revision'],
          'reasoning_gym_revision':'21e6d2a9a581b3e11aafe711abfd37402f8482d5'})
write_new(root/'reports/p01/disk_plan.json',{'evidence_kind':'development_observation',
          'limit_bytes':40*1024**3,'model_bytes':weights,'compressed_dependency_bytes':sum(f['bytes'] for f in files),
          'torch_expanded_bytes':expanded,'other_expansion_allowance_bytes':other*5,
          'artifact_temp_margin_bytes':2*1024**3,'estimated_peak_additional_bytes':estimate,
          'model_storage':'one local directory, no second HF blob/snapshot copy',
          'wheel_storage':'one project cache copy; --no-cache-dir install',
          'runtime_env':'.venv-inference','no_generation':True})
lines=[f"{f['name']} @ {f['url']} --hash=sha256:{f['sha256']}" for f in files]
(root/'configs/p01_requirements.lock').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'model_revision':metadata['model_revision'],'torch_expanded_bytes':expanded,
                  'estimated_peak_GiB':estimate/1024**3,'limit_GiB':40,'dependency_count':len(files)}))
