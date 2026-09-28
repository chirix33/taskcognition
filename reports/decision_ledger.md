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
