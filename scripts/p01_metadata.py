"""Official metadata only; no weights, installation or generation."""
import json
from pathlib import Path
import re
import shutil
import urllib.request
from taskcognition.artifacts import write_new

root = Path(__file__).resolve().parents[1]
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'TaskCognition-P01-metadata'}), timeout=60) as response:
        return response.read()

model_url = 'https://huggingface.co/api/models/Qwen/Qwen3-8B?blobs=true'
model = json.loads(get(model_url))
index_url = 'https://download.pytorch.org/whl/cu128/torch/'
index = get(index_url).decode()
urls = re.findall(r'href="([^"]+cp312-cp312-win_amd64.whl[^\"]*)"', index)
tf = json.loads(get('https://pypi.org/pypi/transformers/4.57.6/json'))
record = {'evidence_kind':'development_observation','purpose':'official_metadata_before_download',
          'model_url':model_url,'model_revision':model['sha'],
          'model_files':[{'name':f['rfilename'],'size':f.get('size'),'lfs':f.get('lfs')} for f in model['siblings']],
          'torch_index':index_url,'torch_windows_cp312_wheels':urls,
          'transformers_version':tf['info']['version'],'transformers_requires_dist':tf['info']['requires_dist'],
          'transformers_wheels':[{'url':f['url'],'size':f['size'],'sha256':f['digests']['sha256']} for f in tf['urls'] if f['filename'].endswith('.whl')],
          'free_disk_bytes':shutil.disk_usage(root).free}
write_new(root/'reports/p01/download_metadata.json', record)
print(json.dumps(record,indent=2))
