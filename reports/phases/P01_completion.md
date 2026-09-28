# P01 completion report

Status: **READY_FOR_REVIEW**. P01 is **not sealed**. No P02 work was executed.

**Principal limitation:** the one live D answer omitted the FINAL wrapper and was
retained at score zero. R produced a valid, correct wrapped answer. A separate admitted
R request was deliberately interrupted and could not be replayed on restart. There
is no live valid-FINAL D example; offline success-path tests do not substitute for one.

## Scope

- Active authority: [reviewed Windows/RTX 5090 P01 prompt](../../docs/prompts/P01_reviewed_local_qwen.md),
  SHA-256 `f08794bfcf4a4f62361203f852d67e8f3735bdea9d2185fce3c43529f733e7a8`.
  The generic prompt remains unchanged as history. C01-C03 were not reopened.
- Previous acceptance: [P00 accepted seal](P00_accepted_seal.md), recorded
  `2026-09-28T14:15:45.561996+00:00`, references the user-conveyed coordinator review.
  That review was limited to reports; the coordinator did not inspect the repository
  or rerun tests. [Local preflight](../p01/preflight.json) supplied local verification.
- Verified P00 completion SHA-256:
  `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`.
  Verified P00 index SHA-256:
  `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`.
  All 162 indexed files matched both the original snapshot and worktree before backend
  work; 30 original files matched. P00 implementation is
  `255860890dd480cdd8607e27957b251aa3e1cb1f`, separate packet commit is
  `44cb33d8a178de9a15bf5ea3793e7d9ea64f7b6f`.
- Governing PDF SHA-256:
  `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`.
  Original TeX/BibTeX/protocol under `docs/iclr2027` remain preserved, not edited.
- Branch: `codex/p01-local-qwen`. Executed source/evidence snapshot:
  `683e9a3f7c5c539a3bb5d8d959b98d4c9319721f`. Final corrected code/state:
  `7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322`. This report packet is committed separately;
  the commit containing `P01_packet_receipt.json` identifies it without a circular hash.
- The pre-existing user file `docs/prompts/P01_reviwed_local_qwen.md` remains untouched
  and untracked; the correctly spelled copy records the active prompt. No push or merge.
- No study/candidate/deployment freeze. Final statistical values remain unresolved.

## Delivered slice

The native Windows path executes one hash-linked DEVELOPMENT request in an isolated
worker: official Qwen serialization, durable dispatch/admission, independent sampling
stream, native-channel parsing, strict FINAL validation, native syntax/scoring, immutable
raw output, terminal record and measured resource charge. The supervisor never retries
or rescues R with D. See [supervisor](../../src/taskcognition/p01_smoke.py),
[worker](../../src/taskcognition/p01_worker.py), [ledger](../../src/taskcognition/p01_ledger.py),
[parser](../../src/taskcognition/p01_parsing.py), and [tests](../../tests/test_p01.py).

Qwen/Qwen3-8B was pinned before download to
`b968826d9c46dd6066d109eabc6255188de91218`. All five original weight shards passed
published LFS SHA-256 checks. One checkpoint copy is kept in the project cache. Python
3.12.14, torch 2.11.0+cu128, CUDA runtime 12.8 and Transformers 4.57.6 executed on the
RTX 5090, compute capability 12.0. Synchronized FP32/BF16 known-answer tensor checks
and built-in SDPA MATH BF16 passed without warnings; `sm_120` is in the runtime's
architecture list. All Qwen parameters were asserted CUDA/BF16. No CPU inference,
quantization, optional CUDA extension, driver change or second serving stack was used.

Both modes use sampling, temperature .6, top_p .95, top_k 20, min_p 0, and a total
1,024-new-token cap including thinking. All effective defaults, EOS/pad IDs, rendered
prompts and input IDs are archived in the [run plan and requests](../../artifacts/development/p01-windows-5090-20260928-v2/run_plan.json).
The actual D template renders a closed empty thinking block; R leaves the opening
delimiter to generation. The parser handles both generated and prompt-prefilled
opening contexts, requires the R close, and never treats unclosed thinking as final.
Only ASCII space/tab/CR/LF is allowed outside one nonempty case-sensitive FINAL pair.
One recognized terminal EOS is excluded from parser text by ID; raw IDs/text are intact.

The only live family is original-renderer `number_sorting`, pinned to Reasoning Gym
`21e6d2a9a581b3e11aafe711abfd37402f8482d5`. The unchanged native scorer is binary with
numeric tolerance 1, not exact match. Its minimal vendored dependency closure is
hash-checked and licensed. Gold, absurd-number and invalid-payload hand checks passed.
Partial-credit preservation is tested with an explicitly synthetic scorer, not falsely
attributed to this binary family. P00 family labels remain synthetic fixtures.

## Verification

Commands below ran from the repository root. `PY` means `.venv/Scripts/python.exe`;
`IPY` means `.venv-inference/Scripts/python.exe`. JSON logs record actual argv, exit,
stdout/stderr and elapsed time. The logging wrapper is `PY scripts/p01_command.py LOG COMMAND`.

| Command actually executed | Exit/status | Result artifact | Interpretation |
|---|---|---|---|
| `PY scripts/p01_preflight.py` | 0/PASS | [preflight](../p01/preflight.json) | Accepted hashes, snapshots, 34 P00 tests and immutable fixture verified before backend work. |
| `IPY -m pip install --no-cache-dir --only-binary=:all: --disable-pip-version-check --require-hashes --report reports/p01/pip_install_report.json -r configs/p01_requirements.lock` | 0 | [install](../p01/install_runtime.json) | Official prebuilt runtime, exact dependency hashes. |
| `IPY -X utf8 scripts/p01_gpu_check.py` | 0/PASS | [kernel JSON](../p01/gpu_check.json), [command](../p01/gpu_check_command.json) | Actual synchronized kernels and BF16, not import-only compatibility. |
| `PY -X utf8 scripts/p01_download_model.py` | 0 | [download](../p01/download_command.json), [hashes](../p01/model_download.json) | One pinned official checkpoint; all weight hashes verified. |
| `IPY -m taskcognition.p01_smoke prepare` (first draft) | 1 | [failed preparation](../p01/prepare_smoke.json) | Incorrect assumption about R's prompt opening; zero dispatches. |
| `IPY -m taskcognition.p01_smoke prepare` (v2) | 0 | [pre-dispatch plan](../p01/prepare_smoke_v2.json) | Correct actual template context; original draft retained. |
| `PY -m unittest discover -s tests -v` | 0 | [pre-run 58 tests](../p01/offline_tests_installed.json), [final 62 tests](../p01/offline_tests_final.json) | Parser adversaries, integrity/admission/cost boundaries and all P00 guards. |
| `IPY -m taskcognition.p01_smoke initial` | 0 | [initial pair](../p01/initial_pair_command.json) | Exactly one D and one R on the same input. |
| `IPY -m taskcognition.p01_smoke interrupt` | 0 | [interruption](../p01/interruption_command.json) | One separate deliberate post-admission interruption. |
| `IPY -X utf8 scripts/p01_verify_smoke.py` | 0 | [restart proof](../p01/restart_proof.json), [verification](../p01/verify_smoke_command.json) | Fresh supervisor refuses replay; every run file unchanged. |
| Bundled Python `-m pip wheel . --no-deps --no-index --no-build-isolation --wheel-dir dist/p01-final` | 0 | [build](../p01/build_final_source.json) | Corrected package 0.1.1; installed locally in both environments with `--no-index --no-deps --force-reinstall`. |
| `IPY scripts/p01_final_verify.py` | 0/PASS | [final source verification](../p01/final_source_verification.json) | 30 immutable run files and executed source snapshot verified; installed source matches; no model import. |
| `PY -m taskcognition verify-artifacts --run artifacts/fixtures/p00-analytical-v2` | 0 | [final fixture verification](../p01/offline_fixture_verify_final.json) | All 54 fixture files and analytical aggregates still verified. |
| `IPY -m pip check` | 0 | [dependency check](../p01/runtime_pip_check_final.json) | No broken requirements. |
| `PY scripts/p01_ready.py` | 0 | [state command](../p01/ready_state_command.json) | New review-ready event; no P01 seal or P02 authorization. |
| `PY scripts/p01_review_packet.py index` / `zip` | See packet receipt | [manifest](P01_evidence_manifest.json), [receipt](P01_packet_receipt.json) | SHA-256 index and read-back ZIP validation; no weights/environments. |

Tests cover native delimiter absence/duplication, FINAL-looking thinking, empty/duplicate
tags, case mismatch, trailing text/whitespace, malformed payloads, fractional/wrong/perfect
scores and capped incomplete output. Fault injection covers undispatched, unknown,
admitted-without-response, immutable completed, proven non-admission with J=0, corrupt
evidence, duplicated costs/streams and the eight-call reservation boundary. New tests
ensure unexpected worker errors never become fabricated zero scores.

Other encountered failures: unprivileged networking was denied by the sandbox; the
authorized network escalation succeeded. A wheel-host HEAD returned 403; a byte-range
request enabled metadata/expanded-size inspection. Initial dependency resolution hit
the torch setuptools<82 versus P00 builder 84 conflict, resolved by a separate local
inference environment. The initial vendored native dependency closure needed upstream
`utils.py`; both source manifests are retained. A final state-script import typo
(`canonical_bytes` instead of `canonical`) failed before any state write and was fixed.
These preliminary terminal failures lack separate structured failure logs; they are
disclosed here rather than claimed as passed checks.

**Skipped/unverified:** live D valid-FINAL success; live forced-kill and full 120-second
timeout expiry; six-family feasibility/cap rates; deterministic GPU reruns. No hidden
rerun was used to improve D's result. No final study statistical procedure was executed.

## Data and execution

Evidence is `development_observation`, split DEVELOPMENT; offline/scorer fixtures remain
explicitly fixture evidence. No TRAIN/TUNE labels, AUDIT/TEST records or private meeting
content were accessed for the smoke. Two distinct tiny number_sorting inputs were used:
one initial input with one D and one R draw, and one separate interruption input. This
is not a repeated-draw study and does not set final K.

| Request | Input tokens | Output tokens | Generation seconds | Worker seconds | Retained outcome |
|---|---:|---:|---:|---:|---|
| initial_D | 209 | 17 | 1.079168 | 11.990325 | Bare native list; missing FINAL wrapper; score 0. |
| initial_R | 205 | 548 | 17.879149 | 28.471467 | Native thinking separated; valid FINAL; native score 1. |
| interrupt_R | 205 | 2 | .603901 | 11.275317 | Deliberate cancellation, incomplete thinking; score 0, diagnostic failure. |

All raw output references, hashes, streams and resource events are in the
[machine-readable summary](../p01/smoke_summary.json). Totals: **3 scheduled/dispatched/admitted,
0 unknown, 0 pre-admission retries, 0 automatic regenerations, 567 output tokens**.
Three 1,024-token reservations consumed 3,072 of 8,192 available reserved tokens; five
of eight generation slots remain unused. There was no autoregressive warm-up, gate
training or gate cost. Initial D/R sampling streams differ despite sharing the input.

Conservative cumulative GPU residency, including worker load/cleanup and the 5.758-second
kernel-check process, was **57.495063 seconds / 1,800 seconds**, with no observed limit
overshoot. This overcounts CPU portions and is not a direct device utilization integral.
The cancellation was requested after durable admission and a real first-token event;
generate returned, CUDA synchronized (0.0000281 seconds), and the worker exited normally.
Measured cancellation-to-exit overhead was **0.554971 seconds**. Device work from that
request had ceased after synchronization. The deliberate failure is excluded from any
future interpretation of spontaneous completion rates.

Peak torch memory was 15.41 GiB allocated / 15.54 GiB reserved. Pre-download conservative
peak estimate was 24.13 GiB additional; measured dependencies/cache/evidence footprint
was **19.67 GiB / 40 GiB**, leaving about 1.62 TiB free on the volume. Small final reports,
wheel and ZIP add only a few MiB. Runtime installation took 188.297 seconds and checkpoint
download/verification command 206.016 seconds. Preliminary metadata/resolver work and
code-writing time were not exhaustively timed; GPU accounting above excludes those.
Evidence is stored locally and committed; no off-machine backup was created or promised.

The exact executed [environment lock](../p01/environment_lock.json),
[requirements lock](../../configs/p01_requirements.lock), model/config/template hashes,
request package hashes and source fingerprints are retained. Final 0.1.1 source/environment
is separately recorded in `final_source_verification.json`; it is not retroactively
represented as the version that generated the three observations.

## Findings and limits

The workstation executes the official checkpoint in native BF16 with the common
sampler, and the pipeline preserves and classifies both valid and malformed real output.
Actual cancellation and no-replay restart were demonstrated. D's wrapper failure is
an unresolved live interface observation, not permission to relax parsing. Passing
tests and one R score of 1 establish neither Qwen superiority nor routing effectiveness.
The smoke establishes no 99% completion rate, audit validity, hard service-time bound,
six-family feasibility, statistical significance or final package freeze. D's mode
switch does not prove absence of latent reasoning.

## Changes and decisions

| ID | Resolved value/change | Evidence and reason | Downstream impact | Authority |
|---|---|---|---|---|
| P01-01 | Accept P00; preserve old state/report/proposed seal | Exact preflight hashes; limited coordinator review | Historical hashes remain verifiable | User reviewed prompt |
| P01-02 to 05 | One pinned official checkpoint, separate environment, BF16 SDPA MATH, pinned native scorer | Official sources plus real kernel/native checks | Smoke-only package, no scientific freeze | Bounded P01 authorization |
| P01-06 | Correct R prompt-context assumption before dispatch; use v2 run ID | Official serialized template | Old failed draft preserved, no output invalidated | Routine reversible correction |
| P01-07 to 10 | Strict parsing, retained failures, three-call stop, explicit D limitation | Raw output and admission/resource evidence | No favorable rerun or result repair | Reviewed P01 contracts |
| P01-11 | Final 0.1.1 supervisor charges cost then rejects unexplained worker exit | Review found an unexercised branch could impute zero after a scoring/program error; four new tests pass | Executed 0.1.0 preserved; all three exited normally with complete records, so no observation invalidated | C02 integrity rule and authorized fixes |
| P01-12 | READY_FOR_REVIEW and no next phase | New state event; dispatch requires IN_PROGRESS | P01 remains unsealed | Phase discipline |

Detailed decisions and official reference URLs are in [P01 ledger](../p01/decision_ledger.md).
No C01-C03 scientific rule changed. Original P00 evidence is unchanged, with current
code/state evolution explicitly checked against its Git snapshot. No manuscript tables
were populated. The old v1 draft is historical, not an empirical run; no evidence was
deleted to make validation pass.

## Acceptance checklist

| Reviewed P01 requirement | Status | Evidence / qualification |
|---|---|---|
| Verify and record P00 acceptance before backend work | PASS | Preflight, accepted seal, original-state snapshot and event 001. |
| Bounded resource plan printed/saved before dispatch | PASS | Resource/run manifests; 3/8 calls, 567/8192 actual tokens, 57.50/1800 seconds. |
| Demonstrate actual GPU/BF16 and supported attention | PASS | Synchronized GPU checks and real model outputs; no warnings. |
| Exact native mode/template/sampler, strict parser and pinned native scorer | PASS with limitation | Archived requests, native hand checks, adversarial tests; live D valid-FINAL not observed. |
| Durable admission, integrity distinction, cancellation and no-replay restart | PASS | Fifteen real ledger events, cancellation trace, restart proof; error branches covered offline. |
| Initial pair and bounded named diagnostic, all failures retained | PASS | Three immutable results; separate interruption input; no corrective model rerun. |
| Completion/seal proposal, locks, counters, evidence manifest and compact packet | PASS subject to packet receipt | ZIP entry hashes read back before delivery; weights/environments excluded. |
| Measured P02 proposal without P02 execution | PASS | Conditional proposal; throughput extrapolation explicitly limited. |

## Review packet

1. [P01_review_packet.zip](../p01/P01_review_packet.zip), validated by [external receipt](P01_packet_receipt.json).
2. This report and [proposed seal](P01_proposed_seal.md), then accepted P00 seal/preflight.
3. [Smoke summary](../p01/smoke_summary.json), raw requests/results/events, restart proof,
   GPU JSON, native validation, runtime locks, actual test logs and key source/tests.
4. [Evidence manifest](P01_evidence_manifest.json), SHA-256
   `b525dfba19063550c8ad96adec528574c76133de792c6e31720fdbecdea312ed`.
   The ZIP contains 0.1.0 executed source under `executed_source/` and the final code
   at normal paths. The index excludes itself/report/seal/ZIP receipt to avoid hash
   cycles; the external receipt hashes the completed report, seal, index and ZIP.
5. [Conditional P02 resource proposal](../p01/P02_resource_proposal.md): after acceptance,
   propose 24 generations across six families as an integration slice, not 99% cap
   certification, within a separately reviewed budget. No 15,000-generation pilot.

Review should assess the D limitation, strict parser/native adapter, real interruption
evidence and supervisor correction. Final cap-study denominators, timeout/support bounds,
encoder, budgets/statistical values and backup destination remain later decisions.
This packet is for coordinating-assistant review, not public release; it excludes model
weights, environments, credentials, private meetings and irrelevant manuscript history.

## Stop statement

P01 ended at **READY_FOR_REVIEW**. P00 is sealed only by the conveyed user/coordinator
acceptance. P01 is not sealed, and no next phase is authorized in current state. P02 may
start only after user-conveyed P01 acceptance and an explicit next-phase prompt.
