# Codex execution handoff — P02D v4 APPROVED

**Status: user execution approval received. Proceed with the bounded v4 run after the existing production checks pass. Do not ask for this approval again.**

Approval date: **2026-10-14**, America/Chicago. The user replied verbatim **“Yes I do.”** to the coordinator's explicit question asking approval for one v4 run of 50 feature forwards followed by up to 192 answer calls, with four hours worker residency, five hours execution wall time and 0.5 GiB additional evidence. This paragraph records that approval; it does not claim the workstation authorization record has already been created or the run has started.

Approval reference: the user's “Yes I do.” message in this TaskCognition coordination conversation, following the P02D v4 acceptance and bounded execution request. Record the actual workstation adoption/execution timestamps separately. Do not invent a message ID.

The exact authorized plan SHA-256 is **`c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`**. Authorization covers one invocation only, under its existing limits and stop rules; no retries, replacements, budget extension, gate training, P03 work or final labels. If this run has already started or completed, do not launch it again: inspect and report its existing evidence.

Read AGENTS, active CR01/runner/statistical contracts, the v4 execution request and `P02D_v4_acceptance_review.md`. The original paper and approved CR01 govern the science. This is a bounded DEVELOPMENT execution within P02. All operational instructions below are retained from the reviewed handoff. P02 remains incomplete/unsealed; P03 remains unstarted.

## 1. Bind the reviewed baseline and authorization

Use the existing pinned Windows inference environment and the exact prospective v4 source. Preserve unrelated changes; use task-only local commits. No push, merge, upload, remote backup, dependency/model download, upgrade or unrelated cleanup is authorized.

Verify these exact identities before live work:

```text
Plan path: artifacts/development/p02d-cr01-plan-v4/run_plan.json
Plan SHA-256: c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365
Review ZIP SHA-256: 1f3c8f0bc16d04416052550d21449665197325a0b3d8096e97d32ae3a9db6950
Index SHA-256: ffbac753187f4ad21555c1506efb2af7611cce22f66635adbd116358ff8ad8dd
Reviewed source commit: b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4
```

Do not substitute v1/v2/v3, regenerate the plan, or change source after authorization. Existing runtime/source/input hashes must pass on the workstation. Do not patch code or relax guards to force a mismatching environment to run; stop with a concrete report instead.

Record corrected-preflight acceptance once. Append a report erratum: the completion sentence “now bound to v3” means v4 with the hash above. Leave historical completion/ZIP and all bound source files unchanged. Archive the user's actual approval wording/reference and its actual date/time separately from coordinator preflight acceptance; never invent either.

Create the separate `configs/p02d_execution_authorization.json` using the existing contract: phase P02D, authorized true, the exact plan hash, exact existing LIMITS, and the actual user-message reference. Bind its file hash and the plan hash in phase state with `active_phase=P02D`, `status=EXECUTION_AUTHORIZED`, and dispatch true. Record the state transition. These operational records are separate from the immutable plan.

Use the existing tested environment/filesystem where atomic hard-link publication succeeded. If permissions or filesystem support are unavailable, report that barrier; do not introduce an overwrite fallback or disable publication/authorization checks. Any small CPU-only publication precheck uses a disposable fixture and must not consume real run slots. No GPU smoke call or unplanned model warm-up is permitted.

## 2. Execute once, within the exact plan

Run from the implementation root using the existing inference Python and explicit `PYTHONPATH=src`. The production command is:

```text
.venv-inference/Scripts/python.exe -m taskcognition.p02d_runner --plan-hash c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365
```

Set the existing offline model/cache flags; do not download anything. The runner verifies source/runtime bindings and imports the intended source. No code-path substitutions, interactive model tests, manually issued feature forwards or separate answer calls.

The authorized scope is the reviewed immutable schedule:

- 24 fixed inputs, exact native questions/configs and serialized prompts.
- 50 feature forwards in the one feature worker, including two charged warm-ups, followed by safe worker shutdown. All must be validly recorded before any answer admission.
- Up to 192 answer slots, K=4 per mode/input, independent streams, total output cap 2,048 per call. Maximum reserved output 393,216 tokens. J=0; no replacement or retry.
- Four hours combined worker residency, five hours execution wall, 0.5 GiB additional evidence, including eventual execution packet. Feature sublimits 900 seconds residency / 1,200 seconds wall; generation/forward deadlines 120 seconds. Keep all existing reservations, loader deadline, cancellation grace and cleanup behavior.

Preserve the exact feature recipe, nine cheap observables, model/tokenizer revision, BF16/SDPA MATH, P02B instruction, sampler, parser and native scorers. Do not filter difficult inputs, relax FINAL requirements, repair outputs, change seed/order or extend budgets.

Retain actual measured costs, load/startup, warm-ups, partial outputs and cleanup/overshoot. Do not clip measurements or silently exclude failed calls. Operational limits do not establish the final audit's hard cost-support assumption. No hypothetical dollar tariff or beta is adopted.

## 3. Stop behavior and evidence

Allow the reviewed runner to finish or stop under its existing rules. Clean resource/deadline stops may return nonzero: report them as operational partial runs when safely stopped. Corruption, unexpected software errors, unsafe cleanup and unresolved process/cost states remain integrity incidents. Never turn those into scored model failures.

Do not restart the runner, reopen a consumed slot, delete a run directory to try again, manually finish missing requests, or launch another tranche. A failed/partial feature stage stops before answers. A later answer stop retains earlier evidence and explicit achieved denominators. If an external interruption occurs, preserve the evidence and report the recovery issue for review; this approval covers no second invocation.

After any exit, verify dispatch is closed and the child stopped using existing evidence/process checks. If safe stop cannot be established, stop further work and report the unresolved state; do not assume no process remains merely because the parent returned. Preserve all incident/resource records and measured lower bounds.

## 4. Report without further model work

Use the production report function on the exact v4 plan after dispatch closes. This reporting work is offline. Report:

- Planned, dispatched, admitted, retained, unexecuted and unscored counts separately; distinguish actual feature work from slots merely reserved before loading.
- All 12 family/mode cells, strict-valid and perfect counts, partial scores and failure subtypes; no repaired secondary result replaces primary scoring.
- All 24 input clusters, observed D/R distributions, direct-perfect counts and within-input variation. Only complete four-D/four-R clusters receive existing-contract targets. Keep partial clusters and dependent cross-pair limitations explicit.
- Every feature timing, two warm-ups, cold-load/warm-forward distinction, vector shape/finite checks and repeated-vector stability. Research cached vectors do not make future live gate features free.
- Actual output tokens and unknown counts/reservations separately; cumulative worker residency, invocation wall time, CPU reporting/packaging time separately, peak memory, cleanup and any overshoot. Count incurred work once.
- Execution evidence size including the review packet. Preserve mandatory raw evidence; if packaging cannot fit the remaining allowance, report the issue rather than dropping raw data or hiding an overrun. Reference unchanged preflight sources by hash where appropriate to avoid unnecessary duplication, while keeping execution evidence reviewable.

No gate fit, comparative significance claim, final-label promotion, P03 simulation, scalar-cost selection or larger-run recommendation masquerading as authorization. Explain what this small diagnostic can and cannot establish. Propose the smallest evidence-supported next step for review; do not execute it.

Return `reports/phases/P02D_execution_completion.md`, the production execution report, ledger/resource/incident records, raw outputs/vectors and source/environment/plan bindings, a verified execution review ZIP/index, and its external hash receipt. Include local commit identities and a truthful backup statement. All historical files, including v1–v4 plans and prior packets, retain their identities.

Stop at **P02D EXECUTION READY_FOR_REVIEW**, or clearly state **STOPPED_INCOMPLETE** / **BLOCKED_INTEGRITY** with achieved counts and reasons. P02 remains incomplete/unsealed and P03 unstarted. Do not start another phase or make a second model invocation sequence automatically.
