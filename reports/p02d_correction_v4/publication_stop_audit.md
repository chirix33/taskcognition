# P02D v4 boundary audit

This correction changes operational reliability only. `artifacts.write_new` and all closed P01/P02A/P02B sources remain unchanged and hash-verifiable. The old coordinator script remains a reproduction of the old helper; it is not a test that should pass unchanged against v4's separate publication protocol.

| Channel | Writer / consumer | v3 boundary |
|---|---|---|
| Session start, dispatch, admission, heartbeat, result link, session end, stop, incident | Single supervisor / supervisor and child ledger scanners | Fully prepared `.pending` bytes then atomic no-overwrite `os.link`; only sequential `*.json` names enter the hash chain. First records obey the same rule. |
| Ready / result | Child / `ProcessWorker.ready/result` | Shared publication helper; only absence returns pending. Committed malformed JSON or null fails immediately. |
| Command | Parent `ProcessWorker.send` / child `read_optional` and exact slot comparison | Admission is committed before the command. No command appears before all its bytes exist. |
| Cancel / finish | Parent / child's `control_present` | Same publication; exact expected control object required. No existence-only success for corrupt control contents. |
| Worker incident / operational stop | Child / parent monitor and post-stop check | Published complete. Incident presence is fail-closed; worker stop objects are parsed and validated. Post-stop checks catch committed corrupt results or incidents racing with a budget trigger. |
| Canonical outcome / independent session resource / independent terminal stop or incident | Parent / ledger and final report | Same publication. Resource and stop hashes are linked from the ledger; unlinked final artifacts are unresolved integrity errors, not completed work. |
| Execution start/end, feature wall, supervisor stop | Parent / report/restart guard | Same publication. Start consumes the invocation; no automatic replay. Final stop classification cannot suppress ledger/cost/cleanup incidents. |
| Phase state | Parent / future authorization checks | Prepared atomic replacement, deliberately mutable and separate from immutable record publication. Closed before return. No new authorization exists. |
| Plan, package, original inputs, proposed authorization | Offline prepared immutable files / hash-bound preflight | No concurrent mutation allowed. Future authorization must use complete publication and bind v3 plus phase state, not v2. |
| stdout/stderr | Child streams / human diagnostics | Not JSON commit records; never mistaken for admission, result, or authorization. |

Hard-link publication was exercised on the actual Windows filesystem outside the sandbox, which denied hard-link creation. Duplicate publication raises without replacement. Tests pause the real publication call after flush/fsync and before `os.link`, poll real readers, then release and require valid records. An abruptly exiting CPU-only subprocess leaves a pending file without creating a result. Tests also retain a consumed slot after interrupted admission publication, and an independent stop after interrupted ledger linkage blocks recovery.

This is not a power-loss proof: file fsync prepares contents, but directory metadata durability is not asserted. Storage/permission failure remains a concrete integrity failure, with no overwrite fallback. Pending files never authorize work. A dispatch record must be committed before a worker is created, and admission before a command. If publication fails after work, the earlier consumed records prevent replay and expose unresolved work.

R2 classification: safe `BudgetStop` with valid evidence produces `OPERATIONAL_STOP` and report `STOPPED_INCOMPLETE`. Valid earlier measurements remain descriptive; stopped unfinished slots are `STOPPED_UNSCORED` with reservations intact. Unsafe cleanup, unknown cost/process state, software error, committed corruption or incomplete evidence linkage produces dominant `INTEGRITY_INCIDENT`. Both stop further dispatch; neither changes scores or supplies missing cluster draws. Known recorded answer timeout semantics remain unchanged.

V4 additionally treats a safely terminated loader deadline as a BudgetStop. Unexpected loader software failures still remain integrity incidents. The intermediate v3 plan/source snapshot and its verification logs are preserved.
