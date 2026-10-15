"""Close the authorized offline checkpoint; does not touch execution evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile
from p02e_analyze import ROOT, OUT, read, write, sha

now = datetime.now(timezone.utc).isoformat()
reproduction = read(OUT/'reproduction_workspace_command.json')
write(OUT/'reproduction_receipt.json', json.loads(reproduction['stdout']))

# Preserve and check supplied coordinator evidence without running its rescoring script.
with zipfile.ZipFile(OUT/'provenance/P02D_execution_coordinator_checks.zip') as z:
    manifest = json.loads(z.read('P02D_execution_coordinator_manifest.json'))
    files = manifest.get('files', manifest)
    verified = {}
    for name, digest in files.items():
        if not isinstance(digest, str) or len(digest) != 64:
            continue
        assert hashlib.sha256(z.read(name)).hexdigest() == digest, name
        verified[name] = digest
    for name in ['P02D_execution_coordinator_manifest.json', 'P02D_execution_coordinator_results.json']:
        with (OUT/'provenance'/name).open('xb') as f:
            f.write(z.read(name))
write(OUT/'coordinator_bundle_verification.json', dict(status='PASS', files=verified,
    bundle_sha256=sha(OUT/'provenance/P02D_execution_coordinator_checks.zip'),
    execution='No coordinator script executed; original offline results preserved with attribution.'))

ledger = ROOT/'reports/decision_ledger.md'
with ledger.open('a', encoding='utf-8', newline='\n') as f:
    f.write(f'''
## P02E offline design review ({now})

P02D execution accepted once in event 023, user-conveyed coordinator decision **“Decision: ACCEPTED as completed DEVELOPMENT evidence.”** Archived review SHA-256 `a332bdd5566d66cd800261771986de54632ac54cf24485253e9b7050f2fcb13f`. All 8,997 accepted indexed members verified against ZIP and current bytes before state transition. The consumed single-run authorization remains unchanged and unusable for P02E. Dispatch false; no new model/GPU work. P02 incomplete/unsealed, P03 unstarted, study unfrozen.

| Entry | Evidence or proposed resolution | Status and consequence |
|---|---|---|
| P02E signal | D 30/96 perfect, R 64/96; strict FINAL D 66/96 and R 64/96; 24 clusters, all primary scores binary. Eleven positive benefits, thirteen zero; all harm estimates zero. | Descriptive DEVELOPMENT only; no advantage over required routers established; no positive harm supervision. All outcomes retained. |
| P02E denominator | Positive-benefit oracle B=0.0625 from six nested successes/two inputs; always-R B=0.3125. Range penalty at n=24 is 0.3742341475, already above maximum B. | Analytical limitation under existing formula, not an audit, power estimate or whole-study infeasibility. No risk tolerance, b_min or n selected. |
| D08/D09 | Prefer investigating a cold isolated all-in hardware service boundary; physical support still unproved. A token/call tariff is an explicit alternative needing rate/count review. | **UNRESOLVED.** Deadline/reservation/observed maximum is not c_max. No scalar ledger, rates, hard support or overflow policy adopted. |
| D05/D16 | Full gate/calibration cost and consistent startup/failure reference policy still needed. Keep beta=c_D_ref+0.5(c_R_ref-c_D_ref). | **UNRESOLVED.** No free cached features, TC-specific budget, normalization fit, gate freeze or beta adoption. |
| D10/D11/D12 | Compare breadth and repeats; cost scales to hundreds/thousands of worker hours under explicit uncertain assumptions. | **UNRESOLVED.** No final allocation, K, alpha, b_min, delta_score or resource ceiling adopted. |
| D14/D17 | Theorem checks/simulation remain P03; local packets do not establish off-machine backup. | **UNRESOLVED.** No P03 work; durable backup/capacity before final collection. No upload/purchase requested here. |
| P02E next proposal | Next separately authorized offline cost-boundary/calibration preflight; contingent 12-existing-input, K=1/mode, 24-answer/26-feature diagnostic under 90-minute worker/120-minute wall/128-MiB ceilings. | **PROPOSAL ONLY / EXECUTION UNAPPROVED.** No new plan, seed or dispatch schedule materialized. Needs source/guard review and separate one-run authority. |

Detailed evidence: `reports/p02e/offline_design_report.md`, machine-readable tables and `next_step_proposal.md`. Historical P02A/P02B are not pooled. Native questions/scoring, runner, manuscript conclusions and old reports are unchanged. Residency interval starts before some process setup and ends before some terminal scans: this is a reporting-boundary clarification, not a change to the accepted 11,560.2217413 seconds. Growing ledger scans plausibly contribute to residual drift but lack isolated timing attribution. Earlier “pushed” statement remains corrected to **“nothing pushed”**; no new push or remote backup is inferred.
''')

completion = ROOT/'reports/phases/P02E_completion.md'
text = f'''# P02E completion — offline denominator and cost-design review

**P02E OFFLINE DESIGN READY_FOR_REVIEW**

## Scope and authority

Active prompt: archived `reports/p02e/provenance/P02E_offline_design_prompt.md`; user conveyed the P02D execution acceptance on 2026-10-15 America/Chicago. Actual workstation adoption: event 023 at 2026-10-15T20:40:22.410173+00:00; offline checkpoint closure: {now}. Acceptance is recorded once, not a new seal of P02. Review SHA-256 `a332bdd5566d66cd800261771986de54632ac54cf24485253e9b7050f2fcb13f`.

Branch `codex/p02e-offline-design`. Task-only local evidence and packet commits are identified in `reports/p02e/source_commits.json` and the external packet receipt; the packet commit can be resolved with `git log -1 -- reports/p02e/P02E_review_packet.zip`. The supplied untracked originals in docs (review, coordinator ZIP, prompt) are preserved and excluded from task staging. No push, merge, remote query, upload, download or installation.

Original PDF SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`; approved CR01 adopted v1 SHA-256 `ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8`. Original Sections 3–8 and active CR01 manuscript sections were read; CR01 fixes 2,048 tokens and descriptive completion, not an eligibility threshold. No manuscript edits, new scientific conflicts resolved silently, or final manifest/freeze.

Bound P02D plan `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`; ZIP `8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9`; production report `9a5f6c7cf713941284b1c125570b3e174c641e685e01284b6bf86f0f95ff4dab`; accounting `0dda412d334389fc5278e8e05c48667a151120f67dbc6d7dfed06ebb4af0ef03`. All 8,997 indexed files matched accepted ZIP and current bytes before operational state changes. Analysis binds 7,837 source records and checks the 7,257-event chain. Packet building repeats historical verification with explicit current phase-state exception; old packet remains authoritative for that historical state.

## Delivered slice

The [offline design report](../p02e/offline_design_report.md) covers all 24 input clusters, four fixed diagnostic rules, analytical sample-size constraints and a non-overlapping collection-cost map. CSV/JSON files preserve full precision and 192 original score outcomes. The precomputed scenario declaration precedes all illustrative calculations; none of its tolerances/counts is adopted. Analysis imports neither a final audit path nor model libraries.

The [next-step proposal](../p02e/next_step_proposal.md) recommends a separately authorized **offline cost-boundary/calibration preflight**, before spending on more labels. Its concrete contingent diagnostic is **UNAPPROVED**: zero fresh inputs, 12 fixed existing inputs, K=1/mode, 24 answer calls, 26 feature forwards including two charged warm-ups, 49,152 maximum output tokens; 90-minute worker, 120-minute wall and 128-MiB operational ceilings. No dispatch plan/seeds/requests were materialized. New shared-within-query loading is only a lifecycle proposal requiring review, not an implemented optimization or a hard-support proof.

## Verification and exact commands

Commands below ran from the implementation root. `scripts/p01_command.py LOG COMMAND...` is the existing stdout/stderr/exit/wall logger used for preparation, analysis, tests, documents and reproduction. All commands are CPU-only.

| Command actually executed | Exit/status | Evidence and interpretation |
|---|---|---|
| `.venv/Scripts/python.exe scripts/p02e_prepare.py` | 0 | `prepare_command.json`; accepted hashes/8,997 members and source identities, archive and event 023 |
| `.venv/Scripts/python.exe scripts/p02e_analyze.py` | 0 | `analysis_command.json`, `analysis_run_receipt.json`; 3.4861601 s wall / 3.40625 s CPU, 7,837 bound records |
| `.venv/Scripts/python.exe -m unittest discover -s tests -p test_p02e_design.py -v` | 0; 8 pass | `focused_tests_command.json`; formulas, retained Z range, zero denominators/Kish, cluster contract/missingness, costs, totals, bindings |
| `.venv/Scripts/python.exe scripts/p02e_documents.py` | 0 | Initial `documents_command.json`; corrected draft render is separately tracked in `document_correction_receipt.json` and current `document_render_receipt.json` |
| `.venv/Scripts/python.exe scripts/p02e_reproduce.py` (initial system-temp path) | 1 | `reproduction_command.json`; sandbox temp ACL blocked before analysis; no empirical evidence touched |
| `.venv/Scripts/python.exe scripts/p02e_reproduce.py` (workspace-temp version) | 0 | `reproduction_workspace_command.json` / `reproduction_receipt.json`; all 17 deterministic analytical/document files match; 3.0788512 s wall / 3.0625 s CPU |
| `.venv/Scripts/python.exe scripts/p02e_finalize.py` | 0 on completion | Archive verification, append-only decision record, completion/state event; no runner calls |
| `.venv/Scripts/python.exe scripts/p02e_packet.py` | See external receipt; PASS required | Every indexed member verified after compression, accepted historical hashes rechecked, CPU/wall/bytes and commit IDs recorded |

Offline PDF extraction succeeded with bundled pypdf Python, but initial console printing exited 1 under cp1252; reading saved `provenance/reference_pdf_text.txt` with UTF-8 succeeded. A draft rerender also initially hit the sandbox system-temp ACL; workspace-local temporary files resolved it. A draft synchronization subtotal was corrected from a manual transcription to the exact JSON-derived 0.0067902000 seconds; the original render receipt and old/new draft hashes remain recorded. These are preparation/display failures, not model/evidence failures. No full regression suite, GPU smoke tests, model execution, final audit decision or full simulation was run; production sources did not change. No new tests were added merely to raise a count.

## Data, costs and findings

Only accepted DEVELOPMENT P02D rows were analyzed: six families, four inputs/family, K=4/mode, 192 retained outcomes. P02A/P02B moments are not pooled. P01's deliberate interruption stays a separate diagnostic. New scheduled/admitted/dispatched/model/feature/answer/gate-fit/final-label counts are all **zero**. No execution authorization was created or consumed again.

D perfect 30/96 versus R 64/96; strict FINAL 66/96 versus 64/96. Only 8/24 inputs show any D success. Eleven benefits positive, thirteen zero, none negative; all 24 harm targets zero. Binary observed scores provide no target-information advantage over factorized routing here; there are no harm-positive supervision examples. These facts do not establish true zero harm, gate superiority or population feasibility.

Positive-benefit selection has six nested D successes on two inputs, B=0.0625; always-R B=0.3125. These are outcome-informed descriptions. At n=24 the contract range term 0.3742341475 exceeds maximum observed B even before variance; no g can meet a positive denominator check on these rows. This is algebra, **not an audit, theorem validation, power calculation or a whole-study stop**. Repeats cannot erase the independent-cluster penalty. K-squared pairs and Kish concentration are not independent success counts.

Existing P02D collection reconciles 193 sessions, 129,371 output tokens, 11,560.2217413 conservative worker seconds and 12,836.8229112 execution-wall seconds. Separate components, unallocated residuals, round/mode tables, CPU reporting/packaging and unavailable timing are in the cost report. Worker-minus-load-minus-generation rises about 5.9 to 20.5 seconds; source shows repeated growing ledger/evidence scans, consistent with but not proving attribution. No new benchmark or optimization. Current warm feature timing is not complete gate cost; live features, CPU heads, startup and failures must be charged under a reviewed service policy.

P02E CPU/wall costs are instrumented in preparation/analysis/render/reproduction/package receipts; reading, editing and all interactive overhead are not comprehensively CPU-profiled. P02D costs are not charged again for this analysis. Package receipt gives local size, full hashes and exact indexed count. Local raw evidence/verified packets are preserved; external receipt means outside the ZIP **on this workstation**, not a verified remote backup. No new off-machine copy exists from this task.

## Decisions and limitations

| Item | Status | Consequence |
|---|---|---|
| P02D acceptance | Recorded once, event 023 | Completed DEVELOPMENT checkpoint; consumed authority stays closed |
| D08/D09 hardware service ledger/support | UNRESOLVED; conditional cold one-query proposal | A timeout, reservation, observed maximum or successful cleanup does not prove finite support; overflow cannot be clipped or excluded |
| D05/D16 gate/init/reference charges | UNRESOLVED | Preserve common beta formula; no beta from collection-worker means or free cached embeddings |
| D10/D11/D12 resource/n/K/risk/score margins | UNRESOLVED | Illustrations are not selected tolerances or allocations |
| D14/D17 theorem/simulation and durable backup | UNRESOLVED | Remain later reviewed work; P03 unstarted |

No scientific rule, norm, tariff, cost bound, feature freeze or resource spend was adopted. No strict scoring, native source, runner, cap, sampler, inputs or manuscript conclusions changed. The report logs historical authority discrepancies and the residency-boundary clarification without rewriting history. All three required primary comparisons remain intact.

## Acceptance checklist and review packet

- PASS: authority/archive/hash bindings and once-only acceptance — `acceptance_verification.json`, event 023.
- PASS: all clusters/rules and denominator algebra — `cluster_rows.*`, `diagnostic_rules.*`, `analytical_constraints.json`, declared scenarios and report.
- PASS: non-overlapping costs, round/mode trends and support limitations — `cost_reconciliation.json`, `cost_sessions.csv`, `cost_round_mode.csv`.
- PASS: exact unapproved next proposal and longer-study implications — `next_step_proposal.*`, `longer_study_resource_scenarios.csv`.
- PASS: focused checks and deterministic reproduction — test/command/receipt files.
- PASS required by packaging: all indexed files match review ZIP and local bytes; exact count/hash in external `P02E_packet_receipt.json`.
- NOT RUN by design: any model work, candidate gate, full regression, final audit, P03 simulation or final data collection.

Review order: this completion; `offline_design_report.md`; `next_step_proposal.md`; tables/source/test receipts; `P02E_review_packet.zip`, `P02E_evidence_index.json`, external `P02E_packet_receipt.json`. The packet references accepted old ZIPs by hash instead of recursively embedding them; original raw evidence is needed to rerun analysis. Source diff and source/evidence commit are included. No P02 accepted seal or final manifest is proposed.

## Stop statement

**Dispatch false; zero new model work; P02 incomplete/unsealed; P03 unstarted; study unfrozen.** Event 024 closes only P02E at READY_FOR_REVIEW. Another phase or any execution requires a separate coordinator handoff after review.
'''
with completion.open('x', encoding='utf-8', newline='\n') as f:
    f.write(text)

state_path = ROOT/'configs/phase_state.json'
state = read(state_path)
assert state['active_phase']=='P02E' and not state['real_dispatch_enabled']
write(OUT/'provenance/P02E_active_state.json', state)
event_path = 'configs/state_events/024_P02E_offline_design_review_checkpoint.json'
write(ROOT/event_path, dict(event='P02E_OFFLINE_DESIGN_READY_FOR_REVIEW', timestamp_utc=now,
    evidence_kind='development_observation', completion_sha256=sha(completion),
    report_sha256=sha(OUT/'offline_design_report.md'), analysis_receipt_sha256=sha(OUT/'analysis_run_receipt.json'),
    previous_state_sha256=sha(state_path), real_dispatch_enabled=False,
    new_model_work=0, p02_sealed=False, p03_started=False, study_frozen=False,
    no_next_phase_authorized=True))
state.update(status='READY_FOR_REVIEW', latest_event=event_path, authorized_next_phase=None)
state_path.write_text(json.dumps(state,indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(status='READY_FOR_REVIEW', timestamp_utc=now, model_work=0)))
