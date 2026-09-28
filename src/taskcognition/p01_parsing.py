"""Strict native Qwen channel -> FINAL -> pinned native syntax -> score."""
import json
import math
from .contracts import IntegrityError, number


def numeric_list_syntax(payload: str):
    # Matches native number_sorting's quote/JSON grammar. Does not change payload sent to scorer.
    value=json.loads(payload.replace("'", '"'))
    if not isinstance(value,list) or not value:raise ValueError('expected nonempty list')
    if any(isinstance(v,(list,dict,bool)) or not math.isfinite(float(v)) for v in value):
        raise ValueError('expected finite numeric items')


def parse_and_score(text: str, mode: str, opening_in_prompt: bool, finish_reason: str, score_fn,
                    syntax_fn=numeric_list_syntax):
    if mode not in ('D','R'):raise IntegrityError('mode')
    result={'raw_decoded_text':text,'thinking':None,'final_channel':None,'final_payload':None,
            'finish_reason':finish_reason,'failure_flags':[],'native_score':0.0,'perfect_correct':False,
            'strict_valid_final':False,'status':None}
    flags=result['failure_flags']
    def fail(flag):
        flags.append(flag)
        if finish_reason=='cap':flags.append('cap_without_valid_final')
        result['status']=flag
        return result
    if mode=='R':
        body=text
        if opening_in_prompt:
            if '<think>' in body:return fail('native_delimiter_failure')
        else:
            if not body.startswith('<think>'):return fail('native_delimiter_failure')
            body=body[len('<think>'):]
        if body.count('</think>')!=1:return fail('native_delimiter_failure')
        thought,final=body.split('</think>')
        if '<think>' in thought or '<think>' in final:return fail('native_delimiter_failure')
        result['thinking']=thought
    else:
        if '<think>' in text or '</think>' in text:return fail('native_delimiter_failure')
        final=text
    result['final_channel']=final
    # Declared whitespace: ASCII space/tab/CR/LF allowed outside wrapper, stripped payload.
    stripped=final.strip(' \t\r\n')
    if stripped.count('<FINAL>')!=1 or stripped.count('</FINAL>')!=1:
        return fail('outer_wrapper_failure')
    if not stripped.startswith('<FINAL>') or not stripped.endswith('</FINAL>'):
        return fail('outer_wrapper_failure')
    payload=stripped[len('<FINAL>'):-len('</FINAL>')].strip(' \t\r\n')
    if not payload:return fail('outer_wrapper_failure')
    result['final_payload']=payload
    try:syntax_fn(payload)
    except (ValueError,TypeError,OverflowError):return fail('native_syntax_failure')
    # Scorer/program errors are integrity errors, never fabricated zero-score answers.
    score=score_fn(payload)
    number(score,0,1)
    result.update(native_score=score,perfect_correct=score==1,strict_valid_final=True,
                  status='perfect' if score==1 else 'partial' if score>0 else 'wrong')
    return result
