"""Preserve exact small upstream module closure for one native family."""
from pathlib import Path
import urllib.request
from taskcognition.artifacts import write_new
from taskcognition.contracts import file_hash

root=Path(__file__).resolve().parents[1]
revision='21e6d2a9a581b3e11aafe711abfd37402f8482d5'
base=f'https://raw.githubusercontent.com/open-thought/reasoning-gym/{revision}/'
paths=['reasoning_gym/algorithmic/number_sorting.py','reasoning_gym/dataset.py',
       'reasoning_gym/factory.py','reasoning_gym/coaching/base_curriculum.py',
       'reasoning_gym/coaching/attributes.py','reasoning_gym/utils.py','LICENSE']
files={}
for relative in paths:
    dest=root/'vendor/reasoning_gym_p01'/relative
    dest.parent.mkdir(parents=True,exist_ok=True)
    with urllib.request.urlopen(base+relative,timeout=60) as response:
        data=response.read()
    if dest.exists():
        assert dest.read_bytes()==data
    else:
        with dest.open('xb') as f:f.write(data)
    files[relative]={'source_url':base+relative,'sha256':file_hash(dest)}
write_new(root/'vendor/reasoning_gym_p01/source_manifest_complete.json',{
    'evidence_kind':'development_observation','revision':revision,'files':files,
    'scope':'unchanged upstream number_sorting generator/scorer and minimal dependency modules',
    'local_initializers':'Local package initialization limits imports to this family; upstream algorithm and scorer bytes unchanged.'})
print('Saved pinned native source closure with individual hashes.')
