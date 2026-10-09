"""Offline coordinator probes against the submitted P02D source; no model libraries.

Usage: python3 p02d_review_reproductions.py /path/to/extracted/P02D_packet
These are defect demonstrations, not production fixes or live authorization.
"""
import json
import shutil
import sys
import tempfile
import threading
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'src'))
from taskcognition import artifacts
from taskcognition.p02d_runner import ProcessWorker, supervise_session
from taskcognition.p02d_plan import PLAN_DIR, RUN, validate_plan
from taskcognition.p02d_features import gate_vector
from taskcognition.p02d_ledger import BudgetStop, scan
from taskcognition.p02d_reporting import report

findings = {}

# Deterministically pause the production writer after final-path creation,
# before its first write. This is a legal OS scheduling interleaving.
with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp)
    entered = threading.Event()
    release = threading.Event()
    original = artifacts.canonical
    writer_errors = []
    def paused_encode(value):
        entered.set()
        if not release.wait(5):
            raise TimeoutError('probe synchronization')
        return original(value)
    def publish():
        try:
            artifacts.write_new(directory / 'ready.json', {'load_seconds': 2})
        except BaseException as exc:
            writer_errors.append(repr(exc))
    worker = ProcessWorker.__new__(ProcessWorker)
    worker.directory = directory
    with patch.object(artifacts, 'canonical', paused_encode):
        thread = threading.Thread(target=publish)
        thread.start()
        assert entered.wait(5)
        assert (directory / 'ready.json').exists()
        observed_size = (directory / 'ready.json').stat().st_size
        try:
            worker.ready()
            observed_error = None
        except Exception as exc:
            observed_error = type(exc).__name__
        finally:
            release.set()
            thread.join(5)
    assert not thread.is_alive() and not writer_errors
    assert observed_error == 'JSONDecodeError'
    assert worker.ready() == {'load_seconds': 2}
    findings['R1_partial_IPC_publication'] = {
        'visible_bytes_while_write_in_progress': observed_size,
        'production_reader_error': observed_error,
        'same_file_valid_after_writer_finishes': True,
        'no_worker_process_or_model_started': True,
    }

class Clock:
    t = 0.0
    def __call__(self): return self.t
    def sleep(self, seconds): self.t += seconds

class BudgetWorker:
    def __init__(self, root, sid, stage, plan_hash, clock):
        self.root = root
        self.clock = clock
        self.code = None
        clock.t += 2
    def ready(self): return {'load_seconds': 2}
    def poll(self): return self.code
    def incident(self): return False
    def send(self, slot): pass
    def result(self, slot):
        # Simulate measured cumulative work leaving insufficient reservation
        # for the next pass, with no software error or malformed evidence.
        self.clock.t += 751
        row = artifacts.read_json(self.root / PLAN_DIR / 'gate_inputs' / (slot['input_id'] + '.json'))
        return dict(slot_id=slot['slot_id'], request_hash=slot['request_hash'],
                    status='OK', dtype='float32', gate=gate_vector(row, [0.0] * 4096),
                    input_positions=slot['input_positions'], forward_seconds=.1,
                    cpu_feature_seconds=.001)
    def finish(self): self.code = 0
    def kill(self): self.code = -1
    def wait(self, timeout): return self.code
    def close(self): pass

plan = validate_plan(artifacts.read_json(root / PLAN_DIR / 'run_plan.json'))
with tempfile.TemporaryDirectory() as tmp:
    test_root = Path(tmp)
    shutil.copytree(root / PLAN_DIR, test_root / PLAN_DIR)
    clock = Clock()
    try:
        supervise_session(test_root, plan, plan['feature_schedule'], 'a' * 64, 0,
            worker_factory=lambda *args: BudgetWorker(*args, clock=clock),
            clock=clock, sleep=clock.sleep)
        raise AssertionError('expected budget stop')
    except BudgetStop as exc:
        reason = str(exc)
    artifacts.write_new(test_root / RUN / 'supervisor_stop.json',
                        {'resource_stop': True, 'error_type': 'BudgetStop', 'error': reason})
    state = scan(test_root / RUN)
    result = report(test_root, plan)
    assert not state['unknown_residency']
    assert result['status'] == 'INTEGRITY_INCIDENT'
    findings['R2_clean_budget_stop_mislabeled'] = {
        'stop_reason': reason,
        'safely_stopped': True,
        'completed_feature_slots': len(state['slots']),
        'report_status': result['status'],
        'incident_events': [item['event'] for item in result['incidents']],
        'real_model_work': 0,
    }

print(json.dumps(findings, indent=2))
