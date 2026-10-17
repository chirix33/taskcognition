Current authority: approved/adopted CR01; see the dated P02C section below. The following P00 decisions are retained historical records, not current phase authorization.

# P00 decision ledger

Status: pre-freeze; no empirical TaskCognition finding. Active authorization: user's P00 prompt.

| ID | Status / decision | Evidence and authority | Downstream consequence |
|---|---|---|---|
| D01 | Resolved inventory: Windows 11 build 26200, PowerShell 7.6.5, Core Ultra 9 285K, 24 logical CPUs, 68,135,153,664 bytes RAM, RTX 5090 32,607 MiB, driver 610.60, compute capability 12.0. | `environment_p00.json`; read-only P00 measurements. | P01 may propose native Windows Transformers; no compatibility claim yet. |
| D02 | Original TeX/BibTeX/protocol present in ignored `docs/iclr2027`; handoff assertion of absence superseded by discovery. | `source_inventory.json`; both verified PDFs have governing hash. Originals preserved byte for byte. | Original sources available for P09; not rebuilt, edited, or committed by P00. Back up ignored source before irreplaceable work. |
| D03 | Proposed only: one native Windows Transformers/PyTorch backend, exact compatible builds selected and pinned in P01. | `P01_resource_proposal.md`; primary vendor documentation. | No backend installed, no model revision frozen. |
| D04 | Proposed only: original checkpoint in BF16 if supported; FP16 is an explicit alternative requiring a recorded precision decision. | Approximate weight storage versus measured VRAM; no empirical load test. | No quantization or checkpoint substitution authorized. |
| D05-D17 | Unresolved as in supplied register. | P00 does not select encoders, cap-study counts, cost ledger, hard bounds, resource ceilings, K/n/splits, alpha, b_min, delta_score, gate budgets, statistical conventions, secondary registry, beta, or backup destination. | Resolve in specified development/review phases before applicable freeze. |
| P00-01 | Resolved: exact-byte preservation of handoff; add Git exceptions only for operational docs/reports. | Initial tracked worktree clean; supplied ignored instructions present. | Historical `docs/iclr2027` archive stays ignored and unchanged. No broad import of older scientific rules. |
| P00-02 | Resolved: standard-library runtime/tests; pinned existing bundled wheel builder; project-local venv. | Install/build commands and 32 passing tests. | No model/backend dependencies, paid services, system upgrades, or downloads. |
| C01 | Resolved by user: use staged hash-linked records, preserving original manuscript. | User answer verbatim: **“Yes, use staged hash-linked records”** to the question explaining the original pre-label candidate-hash requirement versus later candidate records. | Future base manifest binds candidate schema/selection; candidates/deployments are immutable children. P00 does not implement that freeze. Hash records externally, without circular self-hashes. |
| C02 | Resolved by user: retained model failures receive their frozen score; corruption stops analysis. Never zero a whole replicate or redraw to remove failure. | Exact clarification reproduced below; active statistics contract updated. | P00 retains the failed draw in its aggregate and rejects corrupted artifacts. No bootstrap implementation. |
| C03 | Resolved by user: add `final_train_labels`/`TRAIN` and `final_tune_labels`/`TUNE`; both require a frozen study before real collection. | Exact clarification reproduced below; active evidence, architecture and protocol docs, schemas and offline tests updated. | Fitting accepts TRAIN only; TUNE remains calibration/selection. All real collection stays disabled in P00. |

No phase was sealed. No statistical final values or empirical results were invented. The
remaining development choices do not change the offline K=4 estimators or authorize any final data.

## User clarification for C02 and C03 (verbatim)

> Model failures and corrupted evidence are different. A recorded model failure receives the frozen score—zero when no valid retainable answer exists—and remains in the input cluster during bootstrapping. Missing or corrupted evidence must stop the affected analysis for investigation. Never convert corruption into a zero score, zero an entire bootstrap replicate because one model answer failed, or redraw a replicate to remove failures.
>
> Add final_train_labels and final_tune_labels to the evidence-kind list. Keep the separate split field and validate that it matches the evidence kind. Both types require a frozen study manifest before real collection. TRAIN supports fitting; TUNE supports the prescribed calibration and selection.
>
> Stay within P00. Record these as resolved clarifications and update the relevant documentation, schema definitions, and offline validation tests. Real collection remains disabled; corrupted evidence remains rejected. Do not implement later-phase collection or bootstrap execution yet.

## P02C / CR01 adoption

Approval date: **2026-10-05**, America/Chicago. Verbatim user approval: **“Understood. I approve it”**. Actual adoption UTC: **2026-10-05T23:13:12.673586+00:00**. Approved source SHA-256 `463fa03de2604218524e74afc246d4e907c1382d602d146eb30ecd630f8a6ede`. Adopted amendment `docs/amendments/CR01_2026-10-05_v1.md`, SHA-256 `ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8`.

P02B accepted once in event 012 after four-artifact/598-file verification; the later supplied coordinator review confirms it. P01 remains sealed and P02A/P02B accepted. CR01 resolves the scientific-choice pause only: fixed 2,048 primary D/R total tokens, descriptive completion, no 99% eligibility or automatic threshold stop. P02 remains incomplete/unsealed; P03 unstarted; real dispatch false.

Affected artifacts: root AGENTS/README; active protocol, statistical scope annotation, decisions, roadmap, architecture/evidence/source guidance; future P02-P09 prompts; completion/freeze templates; versioned development design template; revised manuscript/figure in `paper/cr01-2026-10-05-v1`. Exact path/hash inventory: `reports/p02c/changed_artifacts.json`. Original sources and all diagnostic scores remain unchanged. C01-C03, method/comparators, audit inequalities and all primary superiority criteria continue to govern. D05/D06/D08-D17 remain unresolved where not already accepted; no final values or resource authority are inferred. No new generations or features were measured.

## P02D offline authorization (2026-10-09T16:00:26.979673+00:00)
P02C accepted once via docs/P02C_coordinator_review.md; verified 115 indexed files and four accepted hashes. CR01 approval unchanged. P02D preparation only; dispatch false, no live slots/forwards authorized. P02 incomplete/unsealed; P03 unstarted. See reports/p02d/acceptance_verification.json and provenance_followup.md.

## P02D preflight checkpoint (2026-10-09T16:26:48.623224+00:00)
Fixed 24-input selection eligible; 192 unique answer streams and 50 feature slots prepared, zero executed. Plan 662597e9610a2ef4951e9a0027756148d73a80ef4372b09b16168dd62c232ad0. One input-only post-norm masked-mean recipe and exact cheap observables implemented for this prospective diagnostic only. Physical cumulative ledger implemented; no reference tariff/beta/hard support/final feature or sample freeze adopted. Remaining decisions unchanged. Dispatch false; P02 incomplete/unsealed; P03 unstarted. See reports/phases/P02D_preflight_completion.md.

## P02D pre-execution v2 correction (2026-10-09T16:37:07.785365+00:00)
Malformed readiness could cause an additional error while persisting load/cost evidence. Corrected optional load metric handling and outer supervisor incident reporting; all 21 new checks rerun. Immutable v1 plan 662597e9610a2ef4951e9a0027756148d73a80ef4372b09b16168dd62c232ad0, v1 source commit fc2b8d4963e4e3473c2804d4d9ca79a75315d867 and v1 draft packet preserved. Active v2 plan 67c3f5ee03ee25f077356e7ef27cb2d870d54caef12318dbe9bfab0b6688ab3d; all 256 input/package/schedule files are byte-identical. No model work, retry or new selection. Dispatch false, no execution authorization.

## P02D offline v3 correction (2026-10-09T17:25:23.682903+00:00)
User authorizes only R1 complete no-overwrite publication and R2 operational-stop classification. v2 67c3f5ee03ee25f077356e7ef27cb2d870d54caef12318dbe9bfab0b6688ab3d remains preserved; v3 c036e7cce4237f637eb366941f87734575404b5876da636174186844a2f4e414 binds corrected source with all 256 materialized files unchanged. No P02D execution acceptance or authorization exists. User corrected the earlier push handoff to **“nothing pushed.”** Local remote-tracking ancestry is separate and cannot establish a push or verified remote backup. See reports/p02d_correction_v3/provenance_correction.md. Zero model/GPU work; dispatch false; P02 incomplete/unsealed; P03 unstarted.

## P02D offline v4 correction (2026-10-09T17:29:46.874215+00:00)
User authorizes only R1 complete no-overwrite publication and R2 operational-stop classification. v3 c036e7cce4237f637eb366941f87734575404b5876da636174186844a2f4e414 remains preserved; v4 c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365 binds corrected source with all 256 materialized files unchanged. No P02D execution acceptance or authorization exists. User corrected the earlier push handoff to **“nothing pushed.”** Local remote-tracking ancestry is separate and cannot establish a push or verified remote backup. See reports/p02d_correction_v3/provenance_correction.md. Zero model/GPU work; dispatch false; P02 incomplete/unsealed; P03 unstarted.

## P02E offline design review (2026-10-15T20:58:21.403185+00:00)

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
