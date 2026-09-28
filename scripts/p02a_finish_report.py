"""Write review prose using saved measurements; proposals do not authorize execution."""
from datetime import datetime,timezone
from pathlib import Path
import statistics
from taskcognition.artifacts import read_json,write_new
from taskcognition.contracts import file_hash
root=Path(__file__).resolve().parents[1];out=root/'reports/p02a';run=root/'artifacts/development/p02a-six-family'
r=read_json(out/'resources.json');obs=read_json(out/'integration_observations.json')['rows']
planhash=file_hash(run/'run_plan.json');commit=read_json(root/'configs/state_events/006_P02A_bounded_dispatch.json')['source_commit']
mean=statistics.fmean(o['worker_residency_seconds'] for o in obs)
rawbytes=sum(p.stat().st_size for p in run.rglob('*') if p.is_file())
start=datetime.fromisoformat(read_json(run/'execution_start.json')['timestamp_utc'])
accepted=datetime.fromisoformat(read_json(out/'p01_acceptance_verification.json')['timestamp_utc'])
prep=(start-accepted).total_seconds()
write_new(out/'preparation_and_storage.json',dict(evidence_kind='development_observation',preparation_elapsed_seconds_acceptance_to_dispatch=prep,definition='wall interval, including source inspection, test runs and commits; not GPU residency; initial governing-document reading precedes acceptance',raw_run_bytes=rawbytes,source_vendor_bytes=sum(p.stat().st_size for p in (root/'vendor/reasoning_gym_p02a').rglob('*') if p.is_file() and '__pycache__' not in p.parts),temporary_source_bytes=sum(p.stat().st_size for p in (root/'tmp/p02a-source').rglob('*') if p.is_file()),new_dependency_bytes=0,packet_bytes='external receipt measures final ZIP and all evidence'))
proposal=f'''# Proposed next P02 work — not authorized or executed

Evidence kind: `development_observation` only for the P02A measurements quoted here. All future counts, estimates and allowances below are proposals. P02 remains incomplete and unsealed.

## Interface checkpoint before spending a cap-study budget

P02A retained {r['dispatched']} attempts, with {r['live_D_valid_final']} live strict-valid D outputs. Inspect all twelve cells, including cap and wrapper failures, in integration_table.md. One input per family and two draws per mode give almost no distributional precision. Do not infer feasibility from a successful cell or invoke the formal 2,048 stop from a poor diagnostic cell.

Recommend a separately reviewed DEVELOPMENT package revision/interface checkpoint before the formal cap study if wrapper failures persist. Specify one common system instruction more explicitly requiring literal FINAL opening/closing tags around the task-native answer, retaining every original question verbatim. Review the exact wording/diff and hash it before any new outputs. Do not change the parser, native scorer, native default difficulty or sampler to rescue this run. Proposed check: six fresh inputs, K=2 each mode, 24 calls at 1,024, 90-minute residency/2-hour wall/0.5-GiB envelope again. No within-run prompt alternatives, gold examples, repair or replacement. Retain P01/P02A and any unsuccessful revised-package records separately. A subsequent fresh cap study must evaluate the finally reviewed package, never pool this diagnostic.

If the next interface checkpoint is still unpromising, bring that evidence back for a stop/development decision. Do not launch a large cap sample merely to spend its budget, suppress weak families, or keep revising until a tiny test looks favorable. Any authorized package revision is documented as development, and formal evaluation follows on new predeclared inputs.

## Concrete formal cap-study plan for review

- At cap 1,024: **100 independent fresh inputs per family, K=2 independent draws per mode per input**. Exactly **200 planned draws per family-mode cell**, 12 cells, **2,400 total attempts**. Interleave families and modes in a predeclared order. Independent input count is 100 per family; the two within-input repeats are nested, not 200 independent inputs.
- Fixed pass rule: at least **198/200 strict-valid-FINAL** in **every** cell. Use unchanged native channel separation, exactly one nonempty case-sensitive FINAL pair with ASCII-whitespace-only outside, and the reviewed native syntax. Completion is distinct from correctness. Every planned draw stays in the denominator; recorded malformed/capped/known-timeout outcomes fail completion unless a valid retainable output exists under the frozen rule. Missing/corrupt evidence or software incidents block the decision and require investigation, never score imputation/replacement.
- If 1,024 fails, a separately budgeted predeclared **fresh** set of 100 inputs/family at 2,048 uses the same 200/cell denominator and >=198 rule, with both packages assessed. No package/config change between formal stages except cap. If any 2,048 cell fails, preserve evidence and stop the confirmatory study as infeasible. Do not raise the primary cap. If operations cannot complete the planned sample, report an incomplete/blocked cap decision, not a scientific pass.
- Maximum output reservation: **2,457,600 tokens** at 1,024, **4,915,200** at 2,048; **7,372,800 combined** if both run. These counts exclude any prior diagnostic, P01 interruption, and high-repeat observations.
- Separate seeds, stream roots and latent/content checks from all historical DEVELOPMENT and reserved final partitions. Materialize defaults and ceiling in each plan. An overlength or duplicate selected input blocks preparation; no outcome-informed simplification or quiet substitution.
- This is an empirical 99% completion rule, **not a lower confidence bound establishing a population completion probability of 99%**. If the coordinator wants a confidence-based certification, that requires an explicit prospective statistical decision and independent-cluster treatment; do not silently add it to the paper's operational rule.

## Costed compute/storage proposals and uncertainty

P02A measured mean worker residency **{mean:.3f} s/request**, total **{r['conservative_gpu_residency_seconds']:.3f} s**, generation **{r['generation_seconds']:.3f} s**, load **{r['load_seconds']:.3f} s**, execution wall **{r['execution_wall_seconds']:.3f} s**, peak allocated **{r['peak_allocated_bytes']/1024**3:.3f} GiB**, and **{r['generated_tokens']} output tokens**. These include all six families but only one item per family. Repeated process loading, per-token synchronization and evidence logging are included. No persistent-worker speedup is assumed.

| Proposed workload | Generations / reserved tokens | P02A-rate illustration | Conservative planning allowance to review |
|---|---|---|---|
| Interface check | 24 / 24,576 at 1,024 | {24*mean/3600:.2f} residency hours | 1.5 GPU hours, 2 wall hours, 0.5 GiB evidence |
| Formal 1,024 stage | 2,400 / 2,457,600 | {2400*mean/3600:.1f} residency hours | Up to 100 GPU hours, 120 wall hours, 2 GiB evidence |
| Conditional formal 2,048 stage | 2,400 / 4,915,200 | {2400*mean/3600:.1f}–{4800*mean/3600:.1f} hours if per-request costs stay within 1–2x; unmeasured | Up to 150 GPU hours, 180 wall hours, 2 GiB evidence |
| First high-repeat tranche, after cap review | 5 fresh inputs/family x 20 draws/mode = 1,200; 1,228,800 or 2,457,600 tokens | {1200*mean/3600:.1f}–{2400*mean/3600:.1f} hours under 1–2x assumption | 100 GPU hours, 120 wall hours, 2 GiB evidence |
| Manuscript high-repeat reference | 25 inputs/family x 50 draws/mode = 15,000; 15,360,000 or 30,720,000 tokens | {15000*mean/3600:.1f}–{30000*mean/3600:.1f} hours under 1–2x assumption | Separate review; provisional 1,250 GPU hours / 1,500 wall hours and 8 GiB evidence |

These are resource-planning illustrations and proposed stopping ceilings, not confidence intervals or a reliable whole-study forecast. Per-request load + deadline + cleanup reservation remains 300 s provisionally (thus 2,400 requests could reserve 200 hours if each used all 300 s). Smaller proposed total ceilings may stop an unusually slow run before its denominator is complete. Re-estimate with each reviewed tranche, without moving its scientific acceptance rule or extending its slots after outcomes. At 2,048 a 120-second timeout may dominate the cap; validate timing before formal package freeze under separate authorization. Measure and report cancellation/cleanup overshoot without clipping actual costs.

The 1,200-draw tranche is useful for variance exploration but cannot substitute for broad independent-input coverage. If expanded to the manuscript reference, predeclare whether the first 30 inputs contribute 20 of their 50 repeats (9,000 additional draws for 90 fresh inputs plus 4,800 for the remaining 30 fresh inputs and 1,800 additional repeats on the first 30 would be miscounted); the simple recommended accounting is **retain first 30 inputs and add 30 draws/mode to each = 1,800 draws, plus 120 new inputs x 50/mode = 12,000 draws**, totaling 15,000 including the initial 1,200. This expansion is not authorized and requires outcome-independent selection and explicit review.

## Feature cost, scalar ledger, hard bounds and backup

Propose a separately authorized input-only same-checkpoint encoder benchmark: 30 fresh texts (5/family), three measured forwards each (90 total, no autoregressive answers), fixed masked mean pooling/layer/tokenization, plus cheap-feature timing. Freeze that proposal first; no encoder or gate was measured in P02A. Request 1 GPU hour, 2 wall hours and 0.25 GiB, counting all loads, warm-ups if declared, forwards, CPU features and any caching. If repeated forwards are too variable, report the measurement limitation. A separate encoder checkpoint remains an explicit scientific decision. MLP/calibration/dispatch cost must also be measured when available; do not treat cached offline embeddings as free live work.

Worker residency is currently a conservative descriptive hardware charge, not a frozen scalar support theorem. Timeout/kill/OS cleanup latency has no demonstrated deterministic upper bound, and there is no live gate-cost bound. Observed minima/maxima cannot supply [c_min,c_max]. Before design acceptance, either establish an enforceable service-time accounting contract including CPU/GPU, dispatch, pre-admission attempts, load/cache policy and cleanup, or review an explicit monetary reference token/call tariff that charges gate encoding/features/calibration and selected answers exactly once. Such a reference tariff is not a claim of actual paid fees; its finite counts/rates and bounds must be fixed prospectively. Do not mix duplicate monetary and time charges. Freeze common reference charges and beta midpoint only after measured all-in work; preserve c_R<=c_D if observed.

For the larger pilot propose a user-designated **encrypted external SSD**, e.g. a dedicated `TaskCognition/P02/` directory, with sufficient free capacity for raw data, an independent ZIP and checksum receipts (at least 20 GiB reserved for the proposed development evidence). Verify a second copy by hash before deleting or moving anything. Device/absolute destination remains unconfirmed; no backup was uploaded or copied off this workstation. The present local ZIP protects review transport, not disk-loss recovery.

## Remaining P02 exit criteria

Six-family integration and native scorer checks are now demonstrated within this diagnostic's limits. Still required: reviewed formal cap decision; adequate independent-input/high-repeat target-noise package; input-only feature implementation/cost; all-in scalar reference costs and credible hard support bounds; resource/backup approval; full future partition manifests; a P03 simulation input package. Statistical theorem assumptions/constants and full fit/tune/audit/fallback/test simulations belong to later authorized work. P03/P04 acceptance must remain blocked by unresolved cost/dependence issues. No gate, comparator training, audit or final labels is authorized here.
'''
# Avoid retaining an abandoned arithmetic alternative in the review proposal.
proposal=proposal.replace(' (9,000 additional draws for 90 fresh inputs plus 4,800 for the remaining 30 fresh inputs and 1,800 additional repeats on the first 30 would be miscounted)','')
(out/'next_P02_proposal.md').write_text(proposal,encoding='utf-8')
commands=[(p.name,read_json(p)) for p in out.glob('*command.json')]+[(p.name,read_json(p)) for p in [out/'offline_tests_v1.json',out/'offline_tests_v2.json',out/'pip_check.json']]
table='\n'.join('| '+' '.join(d.get('argv',[]))+' | '+str(d['exit'])+' | '+name+' |' for name,d in commands)
finding_summary='Across all 24 draws: 10 perfect, 1 strict-valid but wrong, 9 wrapper failures, and 4 capped R outputs without valid FINAL. The three valid D outputs include two perfect letter-counting answers and one wrong shortest-path answer. No live partial credit, timeout or software incident occurred. Zero observed spoilage targets in this tiny sample do not establish safety.'
report=f'''# P02A completion report

Status: **P02A {r['status']}**. **P02 is incomplete and unsealed.** Live dispatch is disabled.

## Scope

- Active authority: current user-conveyed P02A prompt, preserved at docs/prompts/P02A_six_family_integration_prompt.md. Generic P02 is limited by this bounded checkpoint.
- Accepted previous seal: reports/phases/P01_accepted_seal.md. All four accepted hashes and 242 indexed snapshot files verified before new work. Code/evidence commit 6e8cec19d3e7f374aebddaa4f9b410767b02676a; separate packet commit 0c92cb1. P01 five unused slots inactive.
- Governing PDF SHA-256 `{file_hash(root/'reference/TaskCognition_Revised_Verified.pdf')}`. C01–C03 retained. No study/candidate/deployment freeze.
- Branch `codex/p02a-six-family`; pre-dispatch source/plan commit `{commit}`. User prompt/review files were pre-existing untracked files and were not staged/committed by this work. No push, merge, history rewrite or unrelated cleanup.

## Delivered slice

Unchanged native source, renderer, effective default configs and native scorers for all six prescribed families; input-only gate projections; independent sampling streams; fixed common wrapper clarification; P02A guard and single-request supervisor; durable corrected admission/incident/cost handling; complete immutable 24-request plan. Exact plan SHA-256: `{planhash}`.

Source/config/scorer records: adapter_contracts.md, native_scorer_checks.json, native_git_blob_verification.json, vendor source_manifest.json and six outcome_inputs records. Exact prompt diff: prompt_diff.json. Actual .venv-inference source imports are recorded in runtime_preflight.json; subprocess explicitly inherits absolute PYTHONPATH=src. Historical installed 0.1.1 metadata was not mistaken for executed source.

## Verification

| Command actually executed | Exit | Result artifact under reports/p02a |
|---|---|---|
{table}

The pre-dispatch suite passed **90 tests**, retaining all original 81 and adding native-score/channel, gate-field, scope, budget and supervisor-error checks. The first run failed two assertions expecting decimal 0.65 where unchanged native arithmetic returns 0.6499999999999999; test expectations were corrected, without changing the scorer or rounding evidence. The small supervisor injection launches a real sleeping child, raises a monitoring/evidence error, verifies kill/wait, unscored incident persistence, resource charge and no replay. The final suite passed **91 tests**, including an additional exact 24-slot/unknown-admission boundary check; see offline_tests_final.json.

Other actual checks: all 15 native upstream files matched pinned Git-tree blobs; all local model files rehashed; pip check clean; offline gold checks for every selected native item; original question hashes disjoint from P01; retained output tokens decoded and every native score replayed offline. PDF extraction initially hit a console-encoding error and succeeded with PYTHONUTF8=1. Initial sandbox network fetch and Git branch creation were denied; authorized scoped escalations succeeded. Initial graph path guess returned 404; pinned tree resolved the actual algorithmic entry, with no revision substitution. CIM inventory was denied; native Windows memory API supplied RAM. These preparation failures used zero model generations.

## Data and execution

- Evidence: DEVELOPMENT observations only; fixture tests kept distinct. Six inputs, one/family; two D and two R draws each. Dispatched **{r['dispatched']}**, admitted **{r['admitted']}**, reserved output **{r['reserved_tokens']}**, retained observations **{len(obs)}**; planned requests 24. No retry/replacement, hidden warm-up, gate training, encoder run, final label, audit or test exposure.
- Generated output **{r['generated_tokens']} tokens**. Generation **{r['generation_seconds']:.3f} s**; load **{r['load_seconds']:.3f} s**; conservative cumulative GPU residency (full worker lifetime including load/cleanup) **{r['conservative_gpu_residency_seconds']:.3f} s / 5,400 s**; execution wall **{r['execution_wall_seconds']:.3f} s / 7,200 s**. Actual values are not clipped. Preparation acceptance-to-dispatch wall interval **{prep:.3f} s**, separately recorded; initial reading preceded that interval. Report preparation and the final offline test run overlapped live execution; no time was subtracted from measured worker residency or execution wall.
- Peak PyTorch allocated **{r['peak_allocated_bytes']} bytes**, reserved **{r['peak_reserved_bytes']} bytes**. Per-draw duration, failures, memory, tokens and costs are in integration_observations.json/twelve_cells.json. Ledger resource seconds are charged once; generation/load times are descriptive components, not extra additive scalar charges.
- Raw run size before reports/ZIP **{rawbytes} bytes**. No new dependencies or weights; source/data closure 149,485 bytes before manifest, with temporary source copy separately retained. Final evidence byte count and ZIP verification are in P02A_packet_receipt.json. Only local raw files and local ZIP exist; no off-machine backup claimed.
- Model revision b968826d9c46dd6066d109eabc6255188de91218, native BF16 Windows Transformers 4.57.6/PyTorch 2.11.0+cu128 with forced SDPA MATH, no backend change. Matched sampler and all effective defaults in package/request records. Input ceiling 2,048; observed serialized lengths 112–295; no truncation/replacement.

## Findings and limits

Live D strict-valid FINAL count is **{r['live_D_valid_final']}**. {finding_summary} The twelve cells, all retained failures and complete-cluster T_b/T_h/h_DD/d_0.10/d_0.25 checks follow in integration_table.md. Wrong/malformed/capped outcomes were not replaced. **This is not a formal cap selection**, a 99% certification, target-noise precision estimate, gate comparison, significance test or evidence of routing superiority. K-squared pairs are not independent samples. No pooling with P01 or a future cap denominator.

The unchanged text-native scorers for letter counting and knights/knaves accept text and retain their partial-credit logic; full details are explicit in adapter_contracts.md. The 2,048 input ceiling and hardware charge are provisional operational choices, not final population or support bounds. GPU bit-identical reruns were not established.

## Changes and decisions

| ID | Value/status | Evidence / authority | Downstream impact |
|---|---|---|---|
| P02A-01 | P01 sealed by conveyed acceptance | Accepted four hashes and 242 files; new event 005 | P01 remains closed; no old evidence rewritten |
| P02A-02 / D06 | Native defaults, six declared seeds, index 0, input ceiling 2,048; provisional | selection_declaration and immutable plan | Fresh reviewed cap population still required |
| P02A-03 | One common FINAL clarification, parser unchanged | prompt_diff.json, fixed before all outputs | P02A package differs from P01; preserve both |
| P02A-04 / D09 | J=0, 120 s generation deadline, 300 s load/deadline/cleanup reservation; sequential isolated workers | runner tests and live ledger | Operational controls, not hard audit support bounds |
| P02A-05 / D07,D10 | Formal cap and high-repeat plans proposed only | next_P02_proposal.md | No automatic execution |
| P02A-06 / D05,D08,D16,D17 | Encoder/cost/bounds/beta/durable backup unresolved | P02A measures answers only | Remain blockers for later design/freeze acceptance |

No scientific scope deviation or scorer/source change. Old P01 records remain byte-identical except the intentionally advanced current phase state; snapshot and event chain preserve it. Preparation test failures are retained. No accepted P02 seal exists.

## Acceptance checklist

| P02A requirement | Result | Evidence |
|---|---|---|
| Accepted P01 revalidation/seal, P01 disabled | PASS | acceptance verification/seal, events 005–007 |
| Six native default families and offline scorer checks | PASS | six outcome_inputs records, native checks/source hashes |
| Immutable six-input/24-request plan and disjoint streams | PASS | run_plan.json, requests, source commit |
| Corrected worker and supervisor incident cleanup | PASS | 90 preflight tests; raw live ledger |
| Bounded single execution, failures retained, twelve cells | {r['status']} | execution log, resources, twelve_cells.json |
| Complete input target pipeline checks | PASS for recorded complete clusters | target_pipeline_checks.json |
| Review ZIP/index verified | See external receipt | P02A_packet_receipt.json |
| Formal cap / high-repeat / encoder / scalar hard bounds | NOT_RUN / UNRESOLVED, outside authorization | next_P02_proposal.md |
| Full P02 completion/seal, P03 or final labels | NOT_RUN, prohibited | checkpoint phase state |

## Review packet

Send P02A_review_packet.zip with P02A_packet_receipt.json, this completion report, integration_table.md and next_P02_proposal.md. The index contains exact hashes for the raw evidence, source, source diff, tests, native configs, phase events and reports. Weights/environments/secrets/private meetings are excluded. Proposed next work and backup destination need a conveyed review prompt; the proposal is not execution authority.

## Stop statement

**P02A {r['status']}. Live dispatch disabled. P02 incomplete and unsealed.** No further slice, P03, formal cap study, high-repeat pilot, encoder benchmark, gate training or final-label work was started.
'''
(root/'reports/phases/P02A_completion.md').write_text(report,encoding='utf-8')
print('Wrote completion report and costed next-P02 proposal from retained observations.')
