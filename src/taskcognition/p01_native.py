"""One upstream family only, bytes checked before loading its original implementation."""
from pathlib import Path
import sys
from .artifacts import read_json
from .contracts import IntegrityError,file_hash


def native_dataset(root: Path, config: dict):
    vendor=root/'vendor/reasoning_gym_p01'
    manifest=read_json(vendor/'source_manifest_complete.json')
    for name,info in manifest['files'].items():
        if file_hash(vendor/name)!=info['sha256']:raise IntegrityError('native upstream source mismatch')
    if str(vendor) not in sys.path:sys.path.insert(0,str(vendor))
    from reasoning_gym.algorithmic.number_sorting import NumberSortingConfig, NumberSortingDataset
    return NumberSortingDataset(NumberSortingConfig(**config))
