"""The one prospective CR01 feature recipe; no model construction at import."""
import math
import re
from .contracts import IntegrityError, digest

CHEAP_KEYS = ('character_count', 'token_count', 'ascii_digit_count', 'operator_count',
              'choice_marker_count', 'has_json', 'has_list', 'has_number', 'has_text')
FEATURE_SPEC = dict(version='p02d-input-only-v1', layer='model.model.last_hidden_state after final RMSNorm',
    pooling='attention-mask weighted mean; float32 accumulation and output',
    tokenization='original question only; add_special_tokens=False; no truncation',
    use_cache=False, past_key_values=None, normalization_fit=False, hidden_width=4096,
    character_count='Python len of original Unicode string (code points); no normalization',
    token_count='length of cached pinned tokenizer encoding', ascii_digit_count='characters in 0123456789',
    operator_count='characters in +-*/=<>%^',
    choice_marker_count='sum of re.match(r"^[A-D][.)]", line) over text.splitlines(); no leading-space allowance; case sensitive',
    format_flags='re.search(r"\\bWORD\\b", text, re.IGNORECASE), Python Unicode word boundaries; WORD=json,list,number,text',
    learned_feature_order=list(CHEAP_KEYS), join_metadata_only=['input_id'])

def cheap_features(text, token_ids):
    if not isinstance(text,str) or not text or not token_ids:
        raise IntegrityError('empty feature text/tokens')
    return dict(character_count=len(text), token_count=len(token_ids),
        ascii_digit_count=sum(c in '0123456789' for c in text),
        operator_count=sum(c in '+-*/=<>%^' for c in text),
        choice_marker_count=sum(bool(re.match(r'^[A-D][.)]',line)) for line in text.splitlines()),
        **{'has_'+word:int(bool(re.search(r'\b'+word+r'\b',text,re.IGNORECASE))) for word in ('json','list','number','text')})

def validate_gate_input(row):
    if set(row)!= {'input_id','text','token_ids','observables'}:
        raise IntegrityError('gate input allowlist')
    if not isinstance(row['input_id'],str) or not row['input_id']:
        raise IntegrityError('join identity required')
    ids=row['token_ids']
    if not isinstance(ids,list) or not 1<=len(ids)<=2048 or any(type(t)!=int or t<0 for t in ids):
        raise IntegrityError('feature input token bounds')
    if row['observables']!=cheap_features(row['text'],ids):
        raise IntegrityError('cheap feature definition mismatch')
    return row

def masked_pool(hidden, mask, width=4096):
    import torch
    if hidden.ndim!=3 or mask.ndim!=2 or hidden.shape[:2]!=mask.shape or hidden.shape[0]!=1 or hidden.shape[-1]!=width:
        raise IntegrityError('decoder/mask shape')
    if not bool(torch.isfinite(hidden).all()) or not bool(torch.isfinite(mask).all()):
        raise IntegrityError('nonfinite hidden state or mask')
    if not bool(((mask==0)|(mask==1)).all()) or int(mask.sum())==0:
        raise IntegrityError('invalid/empty attention mask')
    weights=mask.to(dtype=torch.float32).unsqueeze(-1)
    vector=(hidden.to(dtype=torch.float32)*weights).sum(dim=1)/weights.sum(dim=1)
    if not bool(torch.isfinite(vector).all()):raise IntegrityError('nonfinite pooled vector')
    return vector[0].to(dtype=torch.float32)

def decoder_feature(model, ids, mask, width=4096):
    """Installed Qwen3Model source verifies last_hidden_state is post-final-norm."""
    import torch
    model.eval()
    with torch.inference_mode():
        result=model.model(input_ids=ids,attention_mask=mask,use_cache=False,past_key_values=None,return_dict=True)
        if getattr(result,'past_key_values',None) is not None:raise IntegrityError('unexpected KV cache')
        return masked_pool(result.last_hidden_state,mask,width)

def gate_vector(input_row, vector, width=4096):
    validate_gate_input(input_row)
    if len(vector)!=width or any(type(x) not in (int,float) or not math.isfinite(x) for x in vector):
        raise IntegrityError('invalid float32 vector')
    # Only values below enter a future learner; join ID must be removed at learning boundary.
    return dict(input_id=input_row['input_id'],embedding=vector,observables=input_row['observables'])

def forward_schedule(inputs):
    if len(inputs)!=24:raise IntegrityError('24 fixed feature inputs required')
    selected=[(inputs[0],'warmup'),(inputs[1],'warmup')]
    selected += [(row,'measurement') for row in inputs]
    selected += [(row,'repeat') for row in inputs if row['dataset_index']<2 for _ in range(2)]
    if len(selected)!=50:raise IntegrityError('50 fixed feature forwards required')
    rows=[dict(slot_id=f'feature_{i:03d}',stage='feature',input_id=row['input_id'],kind=kind,
                 input_positions=row['raw_tokens']) for i,(row,kind) in enumerate(selected)]
    return [dict(row,request_hash=digest(row)) for row in rows]
