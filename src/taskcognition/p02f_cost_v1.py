"""P02F v1: fixture-only service accounting. No inference backend or live plan.

Synthetic durations test bookkeeping, never hardware support. Historical helpers
are reused byte-for-byte. The public supervisor and child paths always fail closed.
"""
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import math
import re
from .artifacts import fixture_output
from .contracts import IntegrityError, digest
from .p02d_publication import write_new, read_optional

VERSION = 'P02F-cost-fixture-v1'

class CostDesignBlocked(RuntimeError): pass
class NoReplay(IntegrityError): pass

def require_live(role, authorization=None, plan_hash=None, state=None):
    if role not in ('supervisor', 'worker'):
        raise CostDesignBlocked('unknown entry role')
    if not isinstance(authorization, dict) or not isinstance(state, dict):
        raise CostDesignBlocked('separate exact-plan authorization absent')
    if (authorization.get('phase') != 'P02F' or authorization.get('authorized') is not True
        or authorization.get('consumed') is not False
        or not isinstance(plan_hash, str) or not re.fullmatch('[a-f0-9]{64}', plan_hash)
        or authorization.get('plan_sha256') != plan_hash
        or state.get('active_phase') != 'P02F'
        or state.get('status') != 'EXECUTION_AUTHORIZED'
        or state.get('real_dispatch_enabled') is not True):
        raise CostDesignBlocked('absent, stale, wrong-hash, consumed or closed authorization')
    # Even a caller-supplied superficially valid record cannot enable this prototype.
    raise CostDesignBlocked('cost decision unresolved; no reviewed executable P02F plan/backend')

def supervisor_entry(**kwargs): return require_live('supervisor', **kwargs)
def worker_entry(**kwargs): return require_live('worker', **kwargs)

def publish(path, kind, slot, payload):
    write_new(path, dict(version=VERSION, evidence_kind='fixture', kind=kind,
                         slot=slot, payload=payload, payload_sha256=digest(payload)))

def read_record(path, kind, slot):
    record = read_optional(path)
    if record is None: return None
    if (record.get('version') != VERSION or record.get('evidence_kind') != 'fixture'
        or record.get('kind') != kind or record.get('slot') != slot
        or record.get('payload_sha256') != digest(record.get('payload'))):
        raise IntegrityError('committed record identity/hash invalid')
    return record['payload']

@dataclass
class FakeClock:
    seconds: float = 0.0
    def advance(self, duration):
        if not math.isfinite(duration) or duration < 0: raise IntegrityError('invalid duration')
        self.seconds += duration

@dataclass
class ScriptedWorker:
    """Closed fake implementation: cannot accept model callbacks or load weights."""
    fault: str | None = None
    safe_stop: bool = True
    answer_seconds: float = 3.0
    calls: list = field(default_factory=list)
    def stage(self, name, context):
        self.calls.append((name, dict(context)))
        if self.fault == name: raise RuntimeError('injected '+name+' failure')

def reconcile(events, start, end, safe_stopped):
    if end < start: raise IntegrityError('clock reversed')
    previous = start
    for e in events:
        a,b=e['start'],e['end']
        if not all(math.isfinite(v) for v in (a,b)) or a < previous or b < a or b > end:
            raise IntegrityError('overlapping, reversed or out-of-window component')
        for nested in e.get('nested',[]):
            if not a <= nested['start'] <= nested['end'] <= b:
                raise IntegrityError('nested timer outside parent')
        previous = b
    elapsed=end-start
    exclusive=sum(e['end']-e['start'] for e in events)
    return dict(observed_elapsed_seconds=elapsed,
                total_service_seconds=elapsed if safe_stopped else None,
                incurred_lower_bound_seconds=elapsed,
                exclusive_component_seconds=exclusive,
                unallocated_residual_seconds=elapsed-exclusive,
                nested_components_additive=False, safe_stopped=safe_stopped,
                hard_support_bound_seconds=None)

def recover(root):
    """Small fixture registry only, not a proposed growing production ledger."""
    consumed=[]; unresolved=[]; stopped=False; known=0.0
    for directory in sorted(Path(root).glob('slot_*')):
        slot=directory.name
        claim=read_record(directory/'claim.json','claim',slot)
        result=read_record(directory/'result.json','result',slot)
        if claim is None:
            if result is not None: raise IntegrityError('result without admission claim')
            continue
        consumed.append(slot)
        if result is None:
            unresolved.append(slot); continue
        if result['claim_sha256'] != digest(claim): raise IntegrityError('result/claim mismatch')
        known += result['accounting']['incurred_lower_bound_seconds']
        stopped |= result['status'] != 'COMPLETE_FIXTURE'
        if not result['accounting']['safe_stopped']: unresolved.append(slot)
    stop=read_record(Path(root)/'stop.json','stop','batch')
    if stop is not None:
        known += stop['accounting']['incurred_lower_bound_seconds']
        stopped=True
    return dict(consumed=consumed, unresolved=unresolved,
                stop_dispatch=stopped or bool(unresolved), known_incurred_seconds=known,
                unknown_cost_slots=unresolved, evidence_kind='fixture')

def run_fixture(repository, output, slot, action, worker, *, bypass=False, warmups=0,
                remaining_seconds=5400.0, remaining_tokens=49152, clock=None):
    """Only ScriptedWorker/FakeClock can run; writes under artifacts/fixtures.

    Each fixture query uses a durable no-clobber claim; interruption after claim
    consumes it even if result publication never happens. No retry/replay API.
    """
    root=fixture_output(Path(repository),Path(output))
    if type(worker) is not ScriptedWorker or (clock is not None and type(clock) is not FakeClock):
        raise IntegrityError('fixture-only worker/clock required')
    if not re.fullmatch('slot_[0-9]{3}',slot) or action not in ('D','R') or warmups not in (0,2):
        raise IntegrityError('invalid fixture identity/action/warm-up count')
    if bypass and warmups: raise IntegrityError('bypass cannot hide warm-up feature work')
    clock=clock or FakeClock(); start=clock.seconds; events=[]
    def phase(name, duration, context=None):
        a=clock.seconds
        try:
            clock.advance(duration)
            worker.stage(name,context or {})
        finally: events.append(dict(name=name,start=a,end=clock.seconds,nested=[]))
    # First validation is charged even when admission is refused.
    phase('validation',2)
    prior=recover(root)
    if slot in prior['consumed']: raise NoReplay('consumed/unknown slot cannot replay')
    if prior['stop_dispatch']: raise IntegrityError('unresolved or stopped fixture batch')
    reservation=690 if warmups else 450
    # Parameters are the initial available fixture envelope, not fresh grants
    # on each query. Prior committed incurred work/reservations count once.
    available_seconds=remaining_seconds-prior['known_incurred_seconds']
    available_tokens=remaining_tokens-2048*len(prior['consumed'])
    if available_seconds < reservation or available_tokens < 2048 or len(prior['consumed'])>=24:
        phase('rejection_response',1)
        stop=dict(status='STOPPED_INCOMPLETE',resource_stop=True,admitted=False,
                  reservation_seconds=reservation,primary_score=None,
                  accounting=reconcile(events,start,clock.seconds,True),events=events)
        publish(root/'stop.json','stop','batch',stop)
        return stop
    directory=root/slot
    claim=dict(action=action,warmups=warmups,bypass=bypass,reservation_seconds=reservation,
               output_tokens_reserved=2048,start_monotonic=start,invocation='fixture-only')
    publish(directory/'claim.json','claim',slot,claim)
    status='COMPLETE_FIXTURE'; error=None; primary=None; answers=0; features=0; loads=0
    try:
        loads+=1; phase('load',4)
        for j in range(warmups):
            features+=1; phase('warmup',1,dict(index=j,research_only=True,use_cache=False,past_key_values=None))
        if not bypass:
            phase('raw_tokenization',1,dict(original_text_only=True))
            features+=1
            phase('feature',1,dict(use_cache=False,past_key_values=None,input_buffer='fresh-feature',mask='fresh-feature',answer_information=False))
            phase('cheap_observables',.25)
            phase('fixed_action',.25,dict(action=action,learned_gate=False))
        phase('prompt',.5,dict(input_buffer='fresh-answer',mask='fresh-answer',enable_thinking=action=='R'))
        phase('reseed',.1,dict(stream='fixture-'+slot,full_reset=True))
        publish(directory/'answer_admitted.json','answer_admitted',slot,dict(count=1))
        answers+=1
        phase('answer',worker.answer_seconds,dict(use_feature_cache=False,past_key_values=None,max_new_tokens=2048))
        if worker.fault=='known_timeout' or worker.answer_seconds > 120:
            status='STOPPED_INCOMPLETE'; primary=0; phase('cancel',10)
        elif worker.fault=='known_model_failure': primary=0
        else: primary=1  # Fixture oracle ONLY, never a native scorer replacement.
        phase('strict_handling',.5,dict(score_evaluation='outside serving; fixture oracle only'))
        publish(directory/'response.json','response',slot,dict(fixture_primary=primary))
        phase('response_ack',.5)
    except Exception as exc:
        status='INTEGRITY_INCIDENT'; error=str(exc); primary=None
    finally:
        try: phase('cleanup',2)
        except Exception as exc:
            status='INTEGRITY_INCIDENT'; error=str(exc); worker.safe_stop=False
        if not worker.safe_stop:
            status='INTEGRITY_INCIDENT'; primary=None; error=error or 'safe stop unresolved'
    # Complete returned record includes post-cleanup mandatory serving handling.
    phase('terminal_handling',.25)
    accounting=reconcile(events,start,clock.seconds,worker.safe_stop)
    result=dict(evidence_kind='fixture',status=status,claim_sha256=digest(claim),
      primary_score=primary,error=error,accounting=accounting,events=events,
      loads=loads,feature_attempts=features,answer_attempts=answers,
      warmups=warmups,warmup_seconds=sum(e['end']-e['start'] for e in events if e['name']=='warmup'),
      warmups_in_elapsed=True,head_cost_seconds=None,learned_gate=False,
      all_in_reference_calibration=False,bypass_path_directly_exercised=bypass,
      reservation_seconds=reservation,overshoot_seconds=max(0,clock.seconds-start-reservation),
      output_tokens_observed=None,output_tokens_reserved=2048,model_work=0)
    publish(directory/'result.json','result',slot,result)
    return result

def reference_cost_from_diagnostic(_):
    raise CostDesignBlocked('feature-before-answer fixed action is not a bypass reference or learned gate; subtraction forbidden')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--role',choices=['supervisor','worker'],required=True)
    args=p.parse_args()
    require_live(args.role)

if __name__=='__main__':main()
