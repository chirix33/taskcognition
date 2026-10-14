# P02D v4 execution completion

Status: **P02D EXECUTION READY_FOR_REVIEW**. Production status: **COMPLETE_DEVELOPMENT**. Dispatch is false. P02 remains incomplete/unsealed; P03 remains unstarted. This is a completed bounded DEVELOPMENT execution, not a study freeze or scientific acceptance.

## Scope and authority

The user conveyed approval on **2026-10-14, America/Chicago**, verbatim **“Yes I do.”**, referring to the coordinator's explicit request for one v4 invocation with 50 feature forwards followed by up to 192 answers. No message ID or approval time-of-day was supplied; none is invented. Workstation adoption occurred at **2026-10-14T18:40:41.222498+00:00**. Separate coordinator corrected-preflight acceptance is dated **2026-10-09** in `docs/P02D_v4_acceptance_review.md`; its time-of-day is unknown. Events 020 and 021 record these separate authorities once. Event 022 closes this execution checkpoint.

The approved handoff/review/check bundle and their exact hashes are archived under `reports/p02d_execution/authority/`. The separate authorization file hash is `db66a4d9dde575496c66587f7d2cf1fcaf68f933c8851e53d6c6ed3bf30de2e0`. The old completion's “now bound to v3” sentence is corrected only through `reports/p02d_execution/preflight_report_erratum.md`; historical report, packet, plan and bound source bytes were not edited.

| Binding | Exact identity |
|---|---|
| Authorized v4 plan | `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365` |
| Reviewed source commit | `b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4` |
| Reviewed preflight ZIP | `1f3c8f0bc16d04416052550d21449665197325a0b3d8096e97d32ae3a9db6950` |
| Reviewed preflight index | `ffbac753187f4ad21555c1506efb2af7611cce22f66635adbd116358ff8ad8dd` |
| Original reference PDF | `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8` |
| Approved CR01 v1 | `ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8` |
| Local authorization commit | `c4aa042df58095ed8732d87614eb6770aab7342a` |

Branch: `codex/p02d-offline-preflight`. The evidence commit is recorded in `reports/p02d_execution/source_commits.json` and the packet index/receipt; the subsequent packet commit is discoverable in local Git. User-owned untracked originals (`docs/P02D_v4_acceptance_review.md`, `docs/P02D_v4_coordinator_checks.zip`, `docs/prompts/P02D_v4_execution_prompt_APPROVED.md`) are preserved and excluded from task commits; authorized archival copies are included. No push, merge, download, upgrade, upload, remote query or unrelated cleanup occurred.

## Delivered slice and execution

Exactly one invocation of the approved entry point ran from the implementation root, with `.venv-inference/Scripts/python.exe`, `PYTHONPATH=src`, `PYTHONUTF8=1`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and `HF_HUB_DISABLE_TELEMETRY=1`. The command logger executed the exact production argv below and recorded exit 0. There was no second invocation, retry, replacement, model smoke call or unplanned autoregressive warm-up.

```text
.venv-inference/Scripts/python.exe -m taskcognition.p02d_runner --plan-hash c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365
```

Execution start was **2026-10-14T18:41:21.265721+00:00**, from the immutable start record. The monotonic invocation duration is recorded separately; the supervisor did not emit an exact UTC end timestamp. The OS stopped-process check was recorded at **2026-10-14T22:15:34.6778312Z**. It found no P02D runner/worker. All **193 worker sessions** (one feature worker plus 192 isolated answer workers) have safe-stop records, with no unknown residency. Dispatch was already false before offline reporting.

| Stage | Planned | Dispatched | Logged admitted | Valid retained records | Unexecuted | Consumed unscored | Reserved only before load |
|---|---:|---:|---:|---:|---:|---:|---:|
| Feature | 50 | 50 | 50 | 50 | 0 | 0 | 0 |
| Answer | 192 | 192 | 192 | 192 | 0 | 0 | 0 |

Feature work comprised two charged warm-ups and 48 measurements over 24 inputs. All 50 were valid and the feature worker stopped safely before answer admission. Answers comprised four independent draws per mode/input over four inputs in each of the six families. Exact original questions, native defaults, tokenizations, streams, order, P02B instruction, 2,048 caps, strict parser/native scorers and nine cheap observables were unchanged. Model: cached Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, native Windows BF16/SDPA MATH. Reasoning Gym: `21e6d2a9a581b3e11aafe711abfd37402f8482d5`. Fingerprints and all effective defaults remain in the v4 plan/environment and verified preflight packet.

No gate was fitted, no feature normalization learned, no simulation or audit/test run, and no final labels collected. No answer repair, scorer relaxation or secondary score substitution was performed. New reporting/packaging scripts are offline handoff tools; all plan-bound production source remains unchanged.

## Verification

Commands are relative to the implementation root; machine-readable command records preserve full argv, timestamps, exit codes and durations. `scripts/p01_command.py <log> <argv...>` was the unchanged command logger, not an alternative model path.

| Command/check actually executed | Exit/status | Evidence | Interpretation |
|---|---|---|---|
| `.venv-inference/Scripts/python.exe scripts/p02d_execution_preflight.py` | 0 / PASS | `preflight_command.json`, `preflight.json` | 661 indexed current/ZIP files, five accepted artifact hashes, 2,530 runtime/source/input bindings, reviewed source identity; real Windows disposable hard-link publication/duplicate check |
| `.venv-inference/Scripts/python.exe scripts/p02d_execution_authorize.py` | 0 / PASS | `authorize_command.json`, `authorization_check.json` | User approval bound to exact v4 plan/limits; no model work |
| Production command above | 0 | `production_command.json`, raw ledger/resources/start/end | Exactly one authorized invocation; 50 forwards and 192 answers |
| `Get-CimInstance Win32_Process` filtered for P02D runner/worker; `nvidia-smi --query-gpu=name,driver_version,memory.total,memory.used --format=csv` | PASS | `process_after.json` | No remaining P02D processes; GPU inventory is descriptive |
| `.venv-inference/Scripts/python.exe scripts/p02d_execution_report.py` | 0 | `offline_report_command.json` | Calls unchanged production report after dispatch closure; verifies all 24 complete K=4 clusters and retained records |
| `ast.parse` on offline report/packet scripts using `.venv/Scripts/python.exe` | 0 / PASS | `offline_helper_syntax_check.json` | Syntax-only check, no model import or inference |
| `.venv-inference/Scripts/python.exe scripts/p02d_execution_finalize.py` | PASS on creation | Event 022, this report, descriptive summary | Offline assertions on complete evidence, safe shutdown and closed phase |
| `.venv-inference/Scripts/python.exe scripts/p02d_execution_packet.py` | See external receipt | `P02D_execution_packet_receipt.json` | Rechecks plan/baseline; verifies every indexed ZIP member and full hashes; separately measures packaging |

A separate post-run offline check reverified all 2,530 bindings, unique 192 answer slots/streams, 24 complete clusters and the 129,371-token total. It confirmed no production-source diff from the reviewed commit and verified that the closed authorization guard rejects before importing torch or transformers (`post_run_verification.json`, exit 0, 17.6670795 seconds). No second runner invocation was used for this check.

The accepted 138-test Windows regression log and coordinator's qualified 15-check Linux/offline verification remain historical preflight evidence, not newly rerun tests or independent coordinator GPU verification. No production source changed, so no additional live test or regression rerun was necessary. Package verification is reported by its receipt only after it succeeds; no claim of backup beyond that local verification is made.

## All twelve cells and all input clusters

Every cell has 16 planned, dispatched, admitted and retained draws; zero missing/unscored draws and zero timeouts. The score lists, wrapper subtypes, native-syntax/channel failures, output lengths, per-draw timing/memory, and all 24 within-input D/R distributions are preserved in `reports/p02d_execution/production_execution_report.json` and the readable `cells_and_clusters.md`.

| Family | Mode | Planned/dispatched/admitted/retained | Strict FINAL | Perfect | Mean primary score | Failure subtypes (overlap allowed) |
|---|---|---|---:|---:|---:|---|
| number_sorting | D | 16 / 16 / 16 / 16 | 4 | 4 | 0.2500 | {"outer_wrapper_failure": 12} |
| number_sorting | R | 16 / 16 / 16 / 16 | 16 | 16 | 1.0000 | {} |
| number_format | D | 16 / 16 / 16 / 16 | 16 | 16 | 1.0000 | {} |
| number_format | R | 16 / 16 / 16 / 16 | 16 | 16 | 1.0000 | {} |
| letter_counting | D | 16 / 16 / 16 / 16 | 16 | 3 | 0.1875 | {} |
| letter_counting | R | 16 / 16 / 16 / 16 | 14 | 14 | 0.8750 | {"cap_without_valid_final": 2, "native_delimiter_failure": 2} |
| graph_color | D | 16 / 16 / 16 / 16 | 0 | 0 | 0.0000 | {"outer_wrapper_failure": 16} |
| graph_color | R | 16 / 16 / 16 / 16 | 6 | 6 | 0.3750 | {"cap_without_valid_final": 10, "native_delimiter_failure": 9, "outer_wrapper_failure": 1} |
| shortest_path | D | 16 / 16 / 16 / 16 | 14 | 0 | 0.0000 | {"cap_without_valid_final": 2, "outer_wrapper_failure": 2} |
| shortest_path | R | 16 / 16 / 16 / 16 | 0 | 0 | 0.0000 | {"cap_without_valid_final": 16, "native_delimiter_failure": 16} |
| knights_knaves | D | 16 / 16 / 16 / 16 | 16 | 7 | 0.4375 | {} |
| knights_knaves | R | 16 / 16 / 16 / 16 | 12 | 12 | 0.7500 | {"cap_without_valid_final": 4, "native_delimiter_failure": 4} |

All primary native scores were exactly 0 or 1 in this sample; there were no positive partial scores. Of 192 outputs, D had **66/96 strict-valid finals and 30/96 perfect scores**; R had **64/96 strict-valid finals and 64/96 perfect scores**. These are descriptive bounded-package results, including formatting and truncation, not an established native task-solving improvement or routing result. Equal-family mean scores are 0.3125 for D and 0.6666666666666666 for R; these summaries do not replace the cell results.

D omitted both tags in 12/16 sorting and 16/16 graph-color answers. Missing-close tags occurred in two D shortest-path outputs and one R graph-color output. No forbidden-outside-prose subtype was observed. **34 capped outputs lacked valid final answers**: two D shortest-path; R letter-counting two, graph-color ten, shortest-path sixteen, knights/knaves four. Thirty-one of the R capped outputs had no completed native final-channel delimiter. Failure labels overlap and must not be added as independent failure counts. There were **zero timeouts, forced terminations, operational stops, software incidents or unresolved records**. Wrong strict-valid answers retain zero under the unchanged native scorer; their absence of wrapper/channel failure flags does not mean correctness.

All **24 clusters** contain four D and four R draws and receive existing-contract T_b, T_h, direct-direct redraw and decline diagnostics at 0.10/0.25. The exact values and sample variances are preserved without rounding in the production report. T_b ranges from 0 to 1. T_h and both partial-decline diagnostics are zero for every sampled input. Direct-redraw is 0.25 for one letter-counting and one knights/knaves input, zero for the other 22. No negative T_b or positive independent-draw spoilage target was observed; this tiny sample cannot establish their absence in the population.

Only **8/24 inputs** had any direct-perfect draws (30 direct successes total); **16/24 had none**. Graph-color and shortest-path each had zero direct-perfect draws across all four sampled inputs. Direct success is concentrated: 16/30 successes are number-format. These are nested counts, not 30 independent inputs, and there is no learned routing exposure or audit denominator bound here. Two inputs had mixed D outcomes and two had mixed R outcomes. K=4 provides coarse, uncertain per-input probabilities. Four inputs/family do not establish population completion, target-noise precision, denominator adequacy or routing superiority. K-squared cross-pairs remain dependent within input. CR01 imposes no 99% eligibility prerequisite or automatic completion stop.

## Feature, token and physical costs

All 50 feature vectors passed the unchanged shape/finite/allowlist validation: 4,096 float32 coordinates from the final post-RMS-normalized decoder states, mask-weighted mean over original question tokens, no chat/answer/gold/family fields. Repeated measurements have maximum absolute coordinate difference **0.0 on this workstation in this run**; this is not a promise of bit-identical GPU reruns. Repeated passes are not new independent labeled inputs. Every feature timing, warm-up identity, input position count and stability check appears in `feature_measurements.md` and the production JSON.

| Measurement | Observed | Operational ceiling/reservation |
|---|---:|---:|
| Combined worker lifetime/residency | 11,560.2217413 s (3.2112 h) | 14,400 s |
| Supervisor execution wall | 12,836.8229112 s (3.5658 h) | 18,000 s |
| Command-wrapper wall (overlapping, not additive) | 12,837.0027497 s | descriptive |
| Feature worker residency | 52.8643334 s | 900 s |
| Feature stage wall | 53.3430577 s | 1,200 s |
| Feature cold load component | 20.0065404 s | included in residency |
| Two feature warm-up forwards | 0.4755707 s; 0.0479846 s | charged among 50 |
| Remaining 48 feature forwards | mean 0.05368644 s; range 0.0451346–0.2019627 s | 120 s per forward |
| All 50 feature forward components | 3.1005045 s | included in residency |
| CPU feature processing component | 0.0346428 s | included in residency |
| Feature input positions | 6,597 recorded and reserved | 102,400 |
| Answer output tokens, thinking plus final | **129,371 known; 0 unknown** | 393,216 reserved; 2,048/call |
| D generation / worker means | 3.6588955 / 34.5900998 s | descriptive components |
| R generation / worker means | 54.5294308 / 85.2782065 s | descriptive components |
| All load components | 3,273.9836642 s | included once in residency |
| Final stop/wait cleanup components | 0.0613837 s | included in residency |
| Feature peak GPU allocated / reserved | 16,435,685,888 / 16,586,375,168 bytes | measured, not support bounds |
| Answer peak GPU allocated / reserved | 16,889,215,488 / 17,708,351,488 bytes | measured, not support bounds |
| Offline reporting wall / process CPU | 30.7702649 / 30.703125 s | separate from execution |

CPU feature processing includes vector transfer, observable validation and gate-vector validation. Worker lifetime includes file verification, process startup/load, synchronization, computation, serialization, cancellation if any, and cleanup. Nested load/forward/generation/cleanup components are not charged a second time. The remaining wall overhead includes between-worker checks; it is not hidden. D produced 6,946 tokens and R 122,425. Reserved capacity is not actual generated work. No measured time/token count was clipped. All cumulative time/feature sublimit overshoots were zero; no cancellation was required. Peak memory is the worker's CUDA allocator metric, not a claim to measure all system RAM or every GPU allocation.

The former 75 admitted generations / 40,555 output tokens across P01/P02A/P02B remain unchanged and separate, including P01's deliberately interrupted diagnostic. This tranche adds 192 admitted generations / 129,371 output tokens (arithmetic cumulative totals 267 / 169,926), plus 50 feature forwards. No historical row is promoted into a final-label or cap-certification denominator.

These research collection costs do not define one-query deployment cost. Each future routed query must pay for one live feature forward plus CPU/gate/calibration work and one selected answer, with an explicitly reviewed initialization allocation. Cached research vectors cannot make that feature forward free. Conversely, 50 research passes must not be charged to every query. No gate timing was measured. The warm-forward numbers cannot make serving initialization free. Residency/deadlines are operational measurements and controls, not proved hard service-time support. No reference-dollar tariff, beta, final feature freeze, cost-support bound or final sample allocation was adopted.

## Decisions, limitations and smallest next step

The fixed v4 experiment was executed as approved. No scientific configuration, cap, parser, difficulty, native scorer, input, order or stream changed. There were no execution protocol deviations or empirical integrity failures. Negative formatting/truncation outcomes are retained in primary scoring.

**Recommend a small offline design review before any further live tranche**, using this exact packet: resolve what direct-perfect denominator adequacy would require given concentration in eight inputs and no observed spoilage; choose a defensible cost-unit/support and initialization contract; and decide whether the unchanged bounded package warrants broader fresh DEVELOPMENT input coverage. This requires no new model call, prompt search, gate fit or P03 simulation and is proposed for review only. Additional repeats of these same 24 inputs alone would not establish broad input coverage or solve absent direct-perfect mass in the two difficult families. If later fresh work is approved, retain all families and failures under CR01; any package amendment needs its own prospective review and fresh evaluation. No cap-certification stage or automatic scientific infeasibility declaration follows from this run.

Remaining decisions include scalar cost and hard support, beta/reference accounting, final K/input allocation and precision targets, feature/normalization/freeze choices, audit denominator/design and theorem verification, and durable backup/final-study capacity. Neither the all-zero harm targets nor higher R mean supports a trained gate or a superiority claim. No larger workload is authorized by this recommendation.

## Acceptance checklist and review packet

- PASS: exact v4 plan/source/environment and all accepted preflight hashes verified before work; unchanged identities checked again by offline report/packet verification.
- PASS: separate user approval and coordinator acceptance recorded; one invocation only; actual adoption/start timestamps distinct; historical erratum appended.
- PASS: all 50 feature forwards valid before all 192 sequential answer calls; no missing, unscored, replacement or unknown work; all 193 workers safely stopped.
- PASS: twelve cells and 24 complete clusters, primary failure retention, exact targets and all feature timings/stability delivered.
- PASS: dispatch closed; P01 sealed; P02A/P02B/P02C accepted checkpoints unchanged; P02 incomplete/unsealed; P03 unstarted.
- NOT RUN / NOT AUTHORIZED: gate fitting, simulation, final labels, new scientific freeze, extra empirical diagnostic or second invocation.
- Packet integrity and exact evidence size: **the external receipt is authoritative after packaging**. It lists every hash, member count, packaging CPU/wall and total execution evidence including the ZIP, against 536,870,912 bytes. Mandatory raw evidence is not omitted to meet a ceiling.

Review in order: this completion; `reports/p02d_execution/P02D_execution_packet_receipt.json`; `P02D_execution_review_packet.zip` and `P02D_execution_evidence_index.json`; production report/accounting; `cells_and_clusters.md`; `feature_measurements.md`; approval/state/provenance records. The packet contains every raw execution file under `artifacts/development/p02d-cr01-tranche` (results/vectors, commands/readiness, ledger, resource records and diagnostic streams), operational bindings and offline handoff source. No incident records were emitted. Unchanged preflight source/dependency/question/package artifacts are referenced by exact verified hashes to avoid needless duplication; their original local packet remains preserved.

Backup status: raw evidence plus a verified local packet on this workstation only. The receipt is external to the ZIP, not off-machine. There was no push, upload or remote query in this task. Earlier provenance was corrected by the user to “nothing pushed”; local remote-tracking ancestry does not establish current remote coverage. Off-machine backup is unverified. Durable backup remains a review item before irreplaceable final collection; no purchase or transfer is initiated here.

## Stop statement

**P02D EXECUTION READY_FOR_REVIEW**, with real dispatch disabled. The one-invocation approval has been used. The historical authorization remains preserved; closed state and existing execution records prohibit replay. P02 remains incomplete/unsealed, P03 unstarted, and no subsequent phase or model work is performed.
