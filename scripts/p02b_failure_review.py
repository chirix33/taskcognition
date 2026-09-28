"""Describe every retained failure; no new parsing, scoring, repair or generation."""
from pathlib import Path
from collections import Counter
from taskcognition.artifacts import read_json

root=Path(__file__).resolve().parents[1];out=root/'reports/p02b';run=root/'artifacts/development/p02b-two-cap'
assert read_json(root/'configs/phase_state.json')['real_dispatch_enabled'] is False
obs=read_json(out/'observations.json')['rows']
diagnostics={d['request_id']:d for d in read_json(out/'failure_diagnostics.json')['rows']}
lines=['# P02B offline failure inspection','',
       'This inspection uses retained final channels and the existing strict-parser/native-scorer replay. Primary scores and completion counts are unchanged. Excerpts below are shortened only for this report; original token IDs, decoded text, thinking and final channels remain intact in the linked raw records. No answer is selected from thinking or ambiguous prose.','',
       '| Cap | Mode | Missing both tags | Missing opening tag | Missing closing tag | Forbidden outside prose | Other wrapper subtype | Native channel failure | Native syntax failure | Cap without valid FINAL |',
       '|---|---|---|---|---|---|---|---|---|---|']
for cap in (1024,2048):
    for mode in ('D','R'):
        rows=[o for o in obs if (o['cap'],o['mode'])==(cap,mode)];c=Counter(o['wrapper_subtype'] for o in rows)
        other=sum(v for k,v in c.items() if k is not None and k not in ('missing_both_tags','missing_open_tag','missing_close_tag','forbidden_outside_prose'))
        native=sum('native_delimiter_failure' in o['failure_flags'] for o in rows)
        syntax=sum('native_syntax_failure' in o['failure_flags'] for o in rows)
        capped=sum('cap_without_valid_final' in o['failure_flags'] for o in rows)
        lines.append(f'| {cap} | {mode} | {c["missing_both_tags"]} | {c["missing_open_tag"]} | {c["missing_close_tag"]} | {c["forbidden_outside_prose"]} | {other} | {native} | {syntax} | {capped} |')
lines+=['','Categories may overlap (for example, a cap and a missing closing tag). Counts are descriptive, with six input clusters, not population estimates.','']
for o in obs:
    if o['perfect_correct']:continue
    key=o['request_id'];result=read_json(run/'results'/f'{key}.json');p=result.get('parsed',{});text=p.get('final_channel')
    lines += [f'## {key}','',f'Primary status `{o["status"]}`; native score **{o["native_score"]}**; strict-valid FINAL **{o["strict_valid_final"]}**; finish `{o["finish_reason"]}`; output tokens **{o["output_tokens"]}**. Flags: `{o["failure_flags"]}`.',
              f'[Unmodified raw record](../../artifacts/development/p02b-two-cap/results/{key}.json), SHA-256 `{o["result_sha256"]}`.','']
    if text is None:lines.append('No separated final channel exists. Reasoning-channel content is not eligible for a payload-only diagnostic.')
    else:
        excerpt=text if len(text)<=500 else text[:250]+'\n[report excerpt shortened; full raw output retained]\n'+text[-250:]
        lines+=['Final-channel inspection:','', '```text',excerpt,'```']
    if key in diagnostics:
        d=diagnostics[key];lines+=['',f'Separate **{d["kind"]}**: unchanged native score **{d["diagnostic_native_score"]}**. Primary score remains **{o["native_score"]}**; this does not repair the deployed output or increase completion.']
    elif not o['strict_valid_final'] and text is not None:lines+=['','No eligible unambiguous payload-only diagnostic is reported.']
    lines.append('')
with (out/'failure_inspection.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines).rstrip('\n')+'\n')
print('Inspected every retained non-perfect outcome; primary scores unchanged.')
