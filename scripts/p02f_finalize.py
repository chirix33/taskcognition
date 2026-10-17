"""Close P02F at its explicit cost-design block; no live plan is created."""
from datetime import datetime,timezone
from pathlib import Path
import json,time
from p02f_prepare import ROOT,OUT,read,write,sha

start,cpu=time.perf_counter(),time.process_time(); now=datetime.now(timezone.utc).isoformat()
v=read(OUT/'acceptance_verification.json'); first=read(OUT/'decision_first_receipt.json')
assert sha(OUT/'cost_contract_decision.md')==first['memo_sha256'] and first['before_prototype_created']
for p,h in v['previous_source_hashes'].items():assert sha(ROOT/p)==h,p
assert read(OUT/'focused_tests_final.json')['exit']==0
fr=read(OUT/'fixture_run_receipt.json'); assert fr['status']=='PASS'
statepath=ROOT/'configs/phase_state.json'; state=read(statepath)
assert state['active_phase']=='P02F' and state['status']=='IN_PROGRESS' and not state['real_dispatch_enabled']
write(OUT/'provenance/active_P02F_state.json',state)
write(OUT/'source_bindings.json',dict(evidence_kind='fixture',protocol='P02F-cost-fixture-v1',
    new_files={p.relative_to(ROOT).as_posix():sha(p) for p in [
        ROOT/'src/taskcognition/p02f_cost_v1.py',ROOT/'tests/test_p02f_cost_v1.py',
        ROOT/'scripts/p02f_prepare.py',ROOT/'scripts/p02f_fixture_evidence.py']},
    unchanged_helpers={p:sha(ROOT/p) for p in ['src/taskcognition/__init__.py',
        'src/taskcognition/p02d_publication.py','src/taskcognition/artifacts.py','src/taskcognition/contracts.py']},
    reviewed_model_plan_sha256=v['accepted_hashes']['artifacts/development/p02d-cr01-plan-v4/run_plan.json'],
    no_inference_environment_import=True,no_plan_created=True,real_dispatch_enabled=False))
write(OUT/'verification_summary.json',dict(status='PASS_WITH_COST_DESIGN_BLOCK',
    evidence_kind='fixture',final_focused_checks=12,initial_attempt='9 filesystem PermissionError failures among 11 checks; sandbox denied hard links.',
    windows_run='11 passed after authorized filesystem escalation; final 12 passed after cumulative budget check added.',
    previous_production_sources_unchanged=True,fixture_cases=6,actual_model_work=0,
    limits='Fixtures verify accounting semantics only, not support, hardware termination, real tensor/RNG equivalence, or final calibration.',
    full_regression='Not run; no historical implementation changed. Relevant publication/reader boundaries exercised directly.',
    incidental_read_error='An exploratory read of nonexistent src/taskcognition/evidence.py reported missing path; actual artifacts.py and contracts.py were read. No mutation or runtime impact.'))
with (ROOT/'reports/decision_ledger.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write(f'''
## P02F offline cost-boundary checkpoint ({now})

P02E acceptance conveyed 2026-10-17 America/Chicago, recorded once in event 025 with actual workstation adoption timestamp. Verbatim decision: **“Decision: P02E OFFLINE DESIGN ACCEPTED.”** Review SHA-256 `{v['authority_hashes']['docs/P02E_acceptance_review.md']}`. All 63 accepted indexed files matched historical ZIP and current bytes before state changes. Coordinator clarification: reproduction compared 15 regenerated outputs plus two copied provenance/declaration inputs, not 17 newly generated outputs. Historical evidence is unchanged.

**P02F COST_DESIGN_BLOCKED.** D08/D09 remain unresolved: no justified finite support for actual all-in hardware service time on this platform. Additional timing samples do not establish it. Nominal ordinary/first deadline sums 430/670 seconds leave 20 seconds within 450/690 reservations for other mandatory work, with no established bound; no cap or reservation is enlarged.

Recommended route **for decision only**: explicit monetary token/call reference-price schedule with justified startup, feature, head/calibration, answer prefill/output and terminal/failure charges. This changes the interpretation to price-relative efficiency, not actual paid fees or physical-time savings. User/coordinator must accept that scope and identify a rate source/owner, otherwise retain the physical-time design block or request a separately reviewed amendment. No rates, third metric, support interval, beta or scientific change adopted.

Minimal separate `p02f_cost_v1.py` tests fixture accounting, atomic records, no replay and safe/unknown stop semantics. No live backend, plan or execution request exists; both public entries reject even superficially valid authorization. Twelve final focused checks and six synthetic examples use zero model/GPU work. Fake elapsed values are not empirical measurements. All prior source/scorer/runner bytes remain unchanged.

D05/D13/D16 remain unresolved: feature-first fixed action is not a fitted gate or gate-bypassed D/R reference; head parity/calibration and startup/reference policy need review. Beta formula remains common and unchanged. D10-D12/D14/D17 remain open for resources, allocation/tolerances, theorem/simulation and backup. Neither 24/26 diagnostic nor a described +24-call bypass delta is authorized or materialized. P02 incomplete/unsealed, P03 unstarted, study unfrozen, dispatch false. See `reports/p02f/cost_contract_decision.md`, `lifecycle_and_accounting.md`, and `calibration_gap_and_blocked_alternative.md`.
''')

report=ROOT/'reports/phases/P02F_preflight_completion.md'
report.write_text(f'''# P02F preflight completion

**P02F COST_DESIGN_BLOCKED — complete offline decision packet**

## Scope and authority

P02F authorizes only offline cost-boundary work. P02E was accepted on **2026-10-17 America/Chicago**; actual workstation adoption is event 025 at **{v['timestamp_utc']}**. Archived exact review and prompt hashes are in `reports/p02f/acceptance_verification.json`. No duplicate acceptance or P02 seal. P01 stays sealed, P02A–P02E accepted development checkpoints, P03 unstarted and study unfrozen.

All **63 P02E indexed files** matched ZIP and current bytes before changing operational state. Bound ZIP `9f3fddc83ff26a26726623a3a568d35b71bbf61f470ce1f724fa0ccfbbbdbe0f`, index `2cab5fc1f5e493a7ef081e948a09c753a4ae476f3220223040d4297b3e71d5e7`, design report `62bd6de18f851239e5833684f818072d1965a5f7da302320e258b7b610db4d24`, proposal `3220410a1d3a0f8e9194e3114d05ef4ae779860b27179da4b604de34b2770546`, P02D plan `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`. Original PDF `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8` and approved CR01 remain unchanged. Original PDF pages 3,5,6 and active TeX cost/audit sections were read. No new scientific discrepancy permits changing the audit or claim.

Branch `codex/p02f-cost-boundary`; local source/evidence and packet commits are identified in `source_commits.json` and the external receipt. The packet commit is resolvable with `git log -1 -- reports/p02f/P02F_review_packet.zip`. Pre-existing untracked originals `docs/P02E_acceptance_review.md`, `docs/P02E_coordinator_checks.zip`, `docs/prompts/P02F_cost_boundary_preflight_prompt.md` remain untouched and unstaged. No push, merge, download, infrastructure upgrade, upload or external transfer.

## Delivered slice and decision

The cost-contract memo was written and hashed **before** the prototype (`decision_first_receipt.json`). Actual all-in physical service time lacks a justified finite support bound. Timing observations, successful kills/waits and 450/690-second reservations cannot establish one. Required startup/source/CPU/response handling lacks a justified bound inside the remaining 20 seconds after nominal deadlines. The cost decision is therefore blocked, not hidden behind a proposed timing run.

Recommend considering the protocol-permitted **explicit monetary reference token/call tariff**, contingent on accepting its price-relative interpretation and identifying an accountable rate source/owner. Six non-overlapping price categories and a symbolic support expression are specified; all rates and head-operation bounds remain unset. No provider prices or actual fees are invented. If that interpretation is unacceptable, retain the physical-time block or request a separate scientific amendment. No third metric, clipping, empirical extrema or alternate concentration inequality is adopted.

The next decision is **cost-metric selection**, not generic source acceptance or model execution approval. Source review can accept the limited fixture semantics, but cannot choose the metric or unblock inference. No pending executable plan or execution request was prepared. The proposed 24-answer/26-forward service-boundary diagnostic cannot provide gate-bypassed references or learned-head cost; a separate +24 bypass-call delta is described solely to quantify the missing path, never scheduled or authorized.

## Implementation and verification

New separate module `src/taskcognition/p02f_cost_v1.py` is fixture-only. It has no inference backend and rejects public supervisor/direct-child entry, including absent/stale/wrong-hash/consumed or superficially valid caller-supplied authorization. It reuses unchanged P02D atomic publication and original strict JSON/hash helpers. Synthetic ScriptedWorker/FakeClock exercise one load, feature passes, fresh-buffer/no-cache flags, reseed ordering, one answer, failure stopping, cumulative reservation, no replay, safe/unknown cleanup, honest overshoot and interval reconciliation. A fixed action has null measured head cost and is never labeled a fitted gate or reference calibration.

Fixture records are under `artifacts/fixtures/p02f-cost-v1-evidence`; indexed copies/references accompany the packet. Their seconds/scores are synthetic, not empirical model results. The closed fake implementation checks orchestration labels, not actual tensors, native serialization, GPU numerical equivalence or physical cancellation. No live ledger redesign or serving platform was built. Interrupted claims remain consumed/unknown; missing/corrupt results stop recovery without zero imputation.

Commands ran from implementation root with `PYTHONPATH=src` and `PYTHONUTF8=1`; the existing `scripts/p01_command.py LOG COMMAND...` recorded command exit/wall/stdout/stderr. Its generic development-observation log envelope is command metadata; the fixture measurements themselves explicitly use `evidence_kind=fixture`.

| Command | Status | Evidence |
|---|---|---|
| `.venv/Scripts/python.exe scripts/p02f_prepare.py` | 0 | `reports/p02f_prepare_command.json`, acceptance verification; 63 snapshot/current matches |
| `.venv/Scripts/python.exe -m unittest discover -s tests -p test_p02f_cost_v1.py -v` (sandbox) | 1 | `focused_tests_initial.json`; 9 hard-link permission errors, no model work |
| Same focused command on Windows filesystem after authorized tool escalation | 0, 11 checks | `focused_tests_windows.json`; original publication protocol unchanged |
| Same focused command after cumulative-budget addition | 0, **12 checks** | `focused_tests_final.json`; current prototype source |
| `.venv/Scripts/python.exe scripts/p02f_fixture_evidence.py` | 0 | `fixture_command.json`, six synthetic cases and hash manifest |
| `.venv/Scripts/python.exe scripts/p02f_finalize.py` | 0 on successful closure | `finalize_command.json`, final state/decision ledger |
| `.venv/Scripts/python.exe scripts/p02f_packet.py` | PASS required in external receipt | Historical/current bindings, every new indexed byte and packet verification, CPU/wall cost |

Publication tests use real small Windows files/threads and deterministic Events pausing `os.link` before publication, with actual readers/registry scans observing no uncommitted record; after commit they require complete valid data. Duplicate publication, interruption before commit and malformed/hash-invalid committed records are covered. CPU-only subprocesses install import traps and exercise the actual public supervisor/worker module paths. No probabilistic race loops, inference imports or GPU smoke tests. Full historical regression was not rerun: no shared historical implementation changed, and reused publication/read paths were directly exercised. An exploratory read of nonexistent `evidence.py` reported a missing path; the actual helpers were then read. No consequence for evidence or execution.

## Costs, data and limitations

New real model loads, feature forwards, answers, GPU work, gate/calibration/normalization fits, full-pipeline simulations, audits and final labels: **all zero**. No historical answer was regenerated, rescored or repaired. P02E/P02D empirical summaries were referenced with their accepted package identities; no new pooled data or targets. P02D single-run authority remains consumed, unchanged and closed.

Preparation verification took {v['wall_seconds']:.6f} wall / {v['cpu_seconds']:.6f} process-CPU seconds. Fixture evidence took {fr['wall_seconds']:.6f} wall / {fr['cpu_seconds']:.6f} process-CPU seconds. Command logs retain all failed/successful test wall times; finalization and packet receipts record their own CPU/wall costs. Reading/writing and interactive overhead are not comprehensively CPU-profiled. FakeClock seconds must never be added to actual preparation time or historical research costs.

A finite tariff bound would follow algebraically only after justified finite rates and complete bounded count/envelope rules are adopted. It would bound reference price, not physical work. Unknown usage or failed accounting still blocks valid cost evidence. Physical time remains unresolved, so D08/D09 are not marked resolved. Common beta, alpha, b_min, delta_score, final n/K, head parity, reference aggregation and resource commitments remain unfrozen. All mandatory baselines, strict scores/failures and all-three primary contrasts are preserved. No study-wide infeasibility declaration or revived completion threshold.

## Acceptance checklist and packet

- PASS: archived exact acceptance/prompt and snapshot bindings; event 025 once.
- PASS: decision-first cost memo with unsupported physical support and explicit unadopted tariff alternative.
- PASS: lifecycle/measurement schema, non-overlapping accounting, warm-up treatment and unresolved reservation headroom.
- PASS: focused fixture implementation/checks, unknown/incident handling, atomic publication and no replay.
- PASS: diagnostic-versus-reference gap and concrete blocked-path alternative; no executable plan/request created.
- PASS required at packaging: all indexed files verified, historical hashes unchanged except documented active state/decision-ledger progression.
- NOT RUN by scope: live measurements, model paths, learned heads, full regression, final audit, simulations, final labels.

Read `reports/p02f/cost_contract_decision.md`, `lifecycle_and_accounting.md`, `calibration_gap_and_blocked_alternative.md`, fixture/test receipts and source diff. Send `P02F_review_packet.zip`, `P02F_evidence_index.json` and external `P02F_packet_receipt.json`; the receipt carries exact member count, sizes, full hashes and local commit. Accepted old ZIPs are referenced, never nested. Local raw evidence and packets remain available; no remote query/upload or new off-machine backup is claimed. “External receipt” means outside the ZIP on this workstation.

## Stop

**P02F COST_DESIGN_BLOCKED** at {now}. Next decision: **cost-metric selection and justified rate ownership**, or retaining the physical-time block. This complete review packet does not request execution. **Dispatch false; zero model work; P02 incomplete/unsealed; P03 unstarted; study unfrozen.** No automatic continuation into another preflight or phase.
''',encoding='utf-8',newline='\n')
event='configs/state_events/026_P02F_cost_design_blocked.json'
write(ROOT/event,dict(event='P02F_COST_DESIGN_BLOCKED',timestamp_utc=now,completion_sha256=sha(report),
    memo_sha256=sha(OUT/'cost_contract_decision.md'),previous_state_sha256=sha(statepath),
    next_decision='cost-metric selection',reason='Physical-time support unsupported; tariff source/rates and head envelope unresolved.',
    real_dispatch_enabled=False,p02_sealed=False,p03_started=False,study_frozen=False,model_work=0))
state.update(status='COST_DESIGN_BLOCKED',latest_event=event,authorized_next_phase=None)
statepath.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8',newline='\n')
write(OUT/'finalize_receipt.json',dict(status='COST_DESIGN_BLOCKED',timestamp_utc=now,
    wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,model_work=0))
print(json.dumps(dict(status='COST_DESIGN_BLOCKED',model_work=0,next_decision='cost-metric selection')))
