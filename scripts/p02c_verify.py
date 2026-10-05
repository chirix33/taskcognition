"""Affected-risk offline checks only. Never imports or loads an answer model."""
from pathlib import Path
import json,re,hashlib,zipfile,subprocess,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from taskcognition.contracts import file_hash,IntegrityError
from taskcognition.p01_ledger import reconcile,events,require_real_dispatch as p01_guard
from taskcognition.p02_runner import require_real_dispatch as p02a_guard
from taskcognition.p02b_runner import require_real_dispatch as p02b_guard
from taskcognition.stages import guard_final_collection
root=Path(__file__).resolve().parents[1];out=root/'reports/p02c'
def load(n):return json.loads((root/n).read_text(encoding='utf-8-sig'))
def save(n,v):
    with (out/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n')
initial=load('reports/p02c/acceptance_verification.json')
for n,h in initial['accepted_artifacts'].items():assert file_hash(root/n)==h,n
index=load('reports/p02b/P02B_evidence_index.json')['files']
with zipfile.ZipFile(root/'reports/p02b/P02B_review_packet.zip') as z:
    for n,h in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
allowed=set(load('reports/p02c/active_edit_paths.json'))|{'reports/decision_ledger.md'}
current_changes=[n for n,h in index.items() if file_hash(root/n)!=h]
assert set(current_changes)<=allowed,current_changes
source=load('reports/source_inventory.json')
for n,h in source['preserved_original_files'].items():assert file_hash(root/n)==h,n
assert file_hash(root/'reference/TaskCognition_Revised_Verified.pdf')==source['source_sha256']
preserve=load('reports/p02c/preservation_manifest.json')
assert file_hash(root/'reports/p02c/pre_CR01_source_snapshot.zip')==preserve['snapshot_sha256']
with zipfile.ZipFile(root/'reports/p02c/pre_CR01_source_snapshot.zip') as z:
    for n,h in preserve['files'].items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
for n,h in index.items():
    if n.startswith(('src/','tests/','artifacts/')):assert file_hash(root/n)==h,n
for guard in (p01_guard,p02a_guard,p02b_guard):
    try:guard(root)
    except IntegrityError:pass
    else:raise AssertionError('historical phase dispatch reopened')
for split in ('TRAIN','TUNE','AUDIT','TEST'):
    try:guard_final_collection(split,None,None)
    except IntegrityError:pass
    else:raise AssertionError('final collection enabled')
state=load('configs/phase_state.json');assert state['active_phase']=='P02C' and state['real_dispatch_enabled'] is False and state['study_freeze'] is None
design=load('configs/cr01_development_design_template.json')
assert design['specification_version']=='TaskCognition-CR01-2026-10-05-v1'
assert design['primary_output_cap_total_tokens']=={'D':2048,'R':2048}
assert design['completion_policy']=='descriptive_no_eligibility_threshold' and design['strict_scoring_unchanged']
assert design['final_freeze'] is False and design['real_dispatch_enabled'] is False and all(x is None for x in design['unresolved'].values())
assert file_hash(root/design['amendment_path'])==design['amendment_sha256']==state['amendment_sha256']
assert file_hash(root/'docs/TaskCognition_CR01_APPROVED.md')==design['approval_source_sha256']
assert design['instruction_sha256']==load('reports/p02b/instruction_diff.json')['new_sha256']
assert (root/design['instruction_source']).is_file()
totals=[]
for n in ('p01-windows-5090-20260928-v2','p02a-six-family','p02b-two-cap'):
    path=root/'artifacts/development'/n;rows=reconcile(path);ledger=events(path)
    entries=[dict(request_id=k,finish_reason=v['result']['finish_reason'],generated_tokens=v['result']['generated_tokens']) for k,v in rows.items()]
    totals.append(dict(run=n,admitted=sum(e['event']=='admitted' for e in ledger),generated_tokens=sum(x['generated_tokens'] for x in entries),rows=entries))
assert sum(x['admitted'] for x in totals)==75 and sum(x['generated_tokens'] for x in totals)==40555
save('historical_totals.json',dict(evidence_kind='development_observation',operation='offline_reconciliation_only',runs=totals,total_admitted=75,total_output_tokens=40555,p01_deliberate_interruption='Third P01 request, retained separate diagnostic; not a completion-certification or final-label denominator',new_model_generations=0,new_model_loads=0,new_encoder_forwards=0,new_gate_training=0,new_gpu_measurements=0))
old=(root/'docs/iclr2027/taskcognition.tex').read_text(encoding='utf-8');new=(root/'paper/cr01-2026-10-05-v1/taskcognition.tex').read_text(encoding='utf-8')
eq=lambda s:re.findall(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}',s,re.S)
assert eq(old)==eq(new)
assert re.search(r'\\title\{.*?\}',old).group()==re.search(r'\\title\{.*?\}',new).group()
for start,end in [('\\section{Comparators and Experimental Design}','\\section{Held-Out Deployment Audit}'),('\\section{Held-Out Deployment Audit}','\\section{Primary Test, Planning, and Reporting}')]:
    assert old[old.index(start):old.index(end)]==new[new.index(start):new.index(end)]
assert 'The cellwise terminal cap rule is fixed' not in new and 'There is no 99\\% completion eligibility prerequisite' in new
assert '2,048 total generated tokens' in new and 'P02A and P02B' in new
assert 'raw simulated result' not in new
assert file_hash(root/'docs/iclr2027/taskcognition.bib')==file_hash(root/'paper/cr01-2026-10-05-v1/taskcognition.bib')
bib=(root/'paper/cr01-2026-10-05-v1/taskcognition.bib').read_text(encoding='utf-8');keys=set(re.findall(r'@\w+\s*\{\s*([^,]+),',bib))
cites={k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}',new) for k in group.split(',')};assert cites<=keys,cites-keys
labels=re.findall(r'\\label\{([^}]+)\}',new);refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',new);assert len(labels)==len(set(labels)) and set(refs)<=set(labels)
ET.parse(root/'paper/cr01-2026-10-05-v1/figures/taskcognition_architecture_CR01_2026-10-05_v1.svg')
with zipfile.ZipFile(root/'reports/p02c/pre_CR01_source_snapshot.zip') as z:
    original_stat=z.read('docs/STATISTICAL_CONTRACT.md').decode('utf-8');assert (root/'docs/STATISTICAL_CONTRACT.md').read_text(encoding='utf-8').startswith(original_stat)
# Search record classifies rather than replacing matching strings.
pattern=r'99|0\.99|1024|1,024|cap[ -]feasib|cap[ -]certif|terminal cap|cellwise cap|else STOP'
cmd=['rg','-n','--json',pattern,'AGENTS.md','README.md','docs','src','tests','configs','paper','--glob','!*.pdf','--glob','!*.png']
scan=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert scan.returncode in (0,1)
matches=[]
for line in scan.stdout.splitlines():
    x=json.loads(line)
    if x['type']!='match':continue
    d=x['data'];n=d['path']['text'].replace('\\','/');scope='active context or incidental numeric match; inspected in reference audit'
    if n.startswith(('src/','tests/','configs/state_','configs/p0')):scope='historical phase guard, regression fixture, snapshot or resource unit'
    elif n.startswith('docs/prompts/P0') and not any(f'docs/prompts/P0{i}_' in n for i in range(2,10)):scope='historical completed-phase prompt'
    elif n.endswith(('TaskCognition_CR01_feasibility_DRAFT.md','P02B_coordinator_review.md')):scope='historical pre-approval authority document'
    elif n.endswith(('.bib','.sty','.bst')):scope='unchanged bibliography/style incidental numeral'
    matches.append(dict(path=n,line=d['line_number'],text=d['lines']['text'].rstrip(),scope=scope))
save('reference_scan.json',dict(evidence_kind='development_observation',operation='offline_reference_audit',command=cmd,exit=scan.returncode,matches=matches,ignored_original_archive='Separately read and hash-verified docs/iclr2027; immutable historical cap rule retained.'))
save('verification.json',dict(evidence_kind='development_observation',operation='offline_consistency_and_preservation',timestamp_utc=datetime.now(timezone.utc).isoformat(),status='PASS',accepted_P02B_zip_files=598,accepted_artifact_hashes_match=True,documented_current_changes=current_changes,original_pdf_and_manuscript_unchanged=True,source_snapshot_verified=True,all_execution_and_test_source_unchanged=True,historical_dispatch_guards_reject=True,all_final_collection_guards_reject=True,cr01_template_consistent_not_frozen=True,all_equations_unchanged=True,comparators_and_entire_audit_section_unchanged=True,statistical_contract_prior_text_unchanged=True,citation_keys_resolve=len(cites),tex_references_resolve=True,svg_well_formed=True,full_manuscript_compiled=False,historical_admitted=75,historical_output_tokens=40555,new_model_compute=0,new_tests_added=0,regression_suite_rerun=False,reason='No executable contract changed; affected checks are consistency/hash verification, production closed-dispatch guards and manuscript structure. No theorem/audit/freeze implementation claimed.'))
print('PASS: CR01 consistency, 598 historical packet files, original sources, unchanged execution code/equations; historical 75 calls/40,555 tokens; zero new model work.')
