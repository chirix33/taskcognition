"""Six pinned native implementations; no gold or metadata in gate records."""
import importlib, json, math, sys
from pathlib import Path
from .artifacts import read_json
from .contracts import IntegrityError, file_hash
from .p01_parsing import numeric_list_syntax

ENTRIES={
 'number_sorting':('algorithmic','NumberSorting'),
 'number_format':('arithmetic','NumberFormat'),
 'letter_counting':('algorithmic','LetterCounting'),
 'graph_color':('algorithmic','GraphColor'),
 'shortest_path':('graphs','ShortestPath'),
 'knights_knaves':('logic','KnightsKnaves')}

def native_dataset(root, family, config):
    vendor=(root/'vendor/reasoning_gym_p02a').resolve()
    manifest=read_json(vendor/'source_manifest.json')
    for name,info in manifest['files'].items():
        if file_hash(vendor/name)!=info['sha256']:raise IntegrityError('native source mismatch')
    existing=sys.modules.get('reasoning_gym')
    if existing and Path(existing.__file__).parent!=vendor/'reasoning_gym':
        # Offline test processes may have loaded the P01 closure first.
        for name in list(sys.modules):
            if name=='reasoning_gym' or name.startswith('reasoning_gym.'):del sys.modules[name]
    sys.path.insert(0,str(vendor)) if str(vendor) not in sys.path else None
    category,cls=ENTRIES[family]
    module=importlib.import_module(f'reasoning_gym.{category}.{family}')
    if Path(module.__file__).resolve()!=vendor/f'reasoning_gym/{category}/{family}.py':raise IntegrityError('wrong native import')
    return getattr(module,cls+'Dataset')(getattr(module,cls+'Config')(**config))

def syntax(family, payload):
    if family=='number_sorting':numeric_list_syntax(payload)
    elif family=='number_format':
        if not math.isfinite(float(payload.replace(',',''))):raise ValueError('finite number required')
    elif family=='graph_color':
        if not isinstance(json.loads(payload),dict):raise ValueError('JSON map required')
    elif family=='shortest_path':
        if payload!='infeasible' and not all(p in ('up','down','left','right') for p in payload.split()):raise ValueError('directions required')
    elif family in ('letter_counting','knights_knaves'):
        # Native scorers intentionally accept text, including substring credit or
        # normalized name-role assignments. Do not narrow away native partial credit.
        if not payload:raise ValueError('nonempty text required')
    else:raise IntegrityError('unknown family')

def gate_record(input_id,text):
    return {'input_id':input_id,'text':text,'observables':{'character_count':len(text)}}
