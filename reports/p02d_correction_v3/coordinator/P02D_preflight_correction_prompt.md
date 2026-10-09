# Codex prompt: correct two P02D preflight defects offline

Continue within P02D. Read the attached coordinator review and reproduction bundle, then the applicable AGENTS/protocol and P02D runner contract. This is authorization to implement and verify the specific offline corrections below. Do not request another confirmation of CR01 or of ordinary reversible fixes.

**No live work:** zero model loads, GPU calls, feature forwards, answer generations, gate fitting, simulations or final labels. Dispatch stays false; no execution authorization record is created. P02 remains incomplete/unsealed; P03 unstarted. No push, merge, downloads, upgrades or external transfers. Preserve unrelated files and use task-only local commits.

## Baseline and evidence

Review applies to active v2 plan `67c3f5ee03ee25f077356e7ef27cb2d870d54caef12318dbe9bfab0b6688ab3d`, submitted ZIP `4a2c8a6834fbbebdd77ce1659bf9819aa61f152a82230fb282d57c916ba7f91b`, index `a05958cf01a877a9510c7b85bb2d40d6008c6e1014ca2509e1a06370bc35d993`. Verify/reuse that baseline and preserve v1/v2 artifacts and reports. This review does not accept P02D for execution.

Archive the coordinator review/reproductions with hashes. Reproduce the failures against the old source in disposable fixtures if needed, never against historical raw evidence. The supplied script takes the extracted packet/repository root as its sole argument and performs no model work.

## R1: complete publication before concurrent visibility

The current `write_new` publishes the final filename before all bytes have been written. Parent `ready/result` readers, child command readers and ledger scanners can parse incomplete files. Fix the P02D publication/read protocol so consumers observe a complete committed record or no committed record, never an in-progress record.

Choose a concrete mechanism supported by the actual Windows filesystem. Retain all of these properties:

- Serialization and durable preparation complete before publication to the name readers consume.
- Publishing an existing record fails without replacing it. A plain overwrite-capable rename/replace is insufficient by itself.
- Temporary/uncommitted files cannot be mistaken for ledger entries, commands, completed results or authorizations. Concurrent ledger scans see a complete valid prefix.
- Writer interruption before publication does not fabricate a completed record or permit replay of a consumed slot. Incurred work remains recorded or explicitly unresolved under the existing recovery policy.
- Invalid committed JSON/hash/identity still fails closed. Do not solve publication races by indefinitely suppressing parser errors or blindly retrying corrupt evidence.
- Cover the new P02D ready, command, result, cancellation/finish, incident/resource and ledger channels as applicable; inspect every concurrent read/write boundary, including the first ledger records visible to the child.

Prefer a scoped new helper or versioned protocol for P02D. Do not rewrite historical artifacts or broadly change closed P01/P02A/P02B behavior. If a shared helper must change, explain why and exercise the affected historical regression checks; keep original-version evidence verifiable.

Use deterministic synchronization in tests, not a probabilistic timing loop. Pause a real writer before publication while the actual reader polls; after commit require valid data. Exercise concurrent ledger scanning and worker command/result publication. Also test duplicate publication, interruption before commit, and malformed committed records. Exercise the actual filesystem publication implementation on Windows with small CPU-only subprocesses/threads; no fake model or GPU process is needed. Existing fake-dictionary worker tests alone are insufficient for this boundary.

## R2: distinguish normal stopping from integrity failure

The supervisor currently writes an incident for every exception, including `BudgetStop`; the report then classifies an ordinary safely handled resource stop as `INTEGRITY_INCIDENT` even when the outer stop says `resource_stop=true`.

Implement explicit operational-stop classification across supervisor, ledger, resource records and reporting. Keep costs, overshoot, stop reasons, achieved counts, partial clusters and consumed slots. Clean budget exhaustion or a known deadline that safely stops work must report stopped/incomplete development with no fabricated integrity error. It still closes dispatch and does not authorize continuation or replay.

Integrity errors must remain dominant when cleanup is unsafe, costs/process state are unresolved, committed evidence is missing/corrupt, or software fails. Do not drop such incidents merely because the initiating exception was a resource stop. Retain valid earlier outcomes with clear global validity/stop status; never convert missing feature/answer results to successful observations or invented zero scores.

Test at least a clean within-session reservation stop, a monitored deadline/resource stop, and a resource stop accompanied by failed cleanup or corrupt evidence. Check final report status and ledger/resource records, not only the raised exception. Verify answer admission remains blocked after an incomplete feature stage, and no consumed work is replayed.

## Preserve the proposed experiment

No change to the 24 inputs, six families, exact original text, native configs, three tokenizations, 192 answer slots, 50 feature slots, streams/seeds/order, feature recipe, 2,048 caps, existing strict scorer, or proposed resource ceilings. The arbitrary reference-dollar tariff and all final scientific freeze choices remain unapproved. Do not add a new scientific phase or rerun empirical diagnostics to test these fixes.

Source changes require a new immutable preflight plan version and hash, e.g. v3. Preserve v1/v2; update the prospective runner's plan selection consistently. Independently demonstrate that all input/package/schedule records retain their bytes, apart from any purely version-linking records that must be explicitly identified. Do not silently change request identity or randomness to simplify the version transition.

Keep explicit pending-authorization checks in both supervisor and child. Confirm the new production entry still rejects before any model import/load, and final-study guards stay closed. The later user approval must bind the new plan, never the superseded v2 hash.

## Report and stop

Return a corrected completion report, exact source diff/commits, new plan/hash, focused test logs, relevant regression results, updated execution request, review ZIP/index and external receipt. Preserve prior reports and their checksums as superseded history; distinguish new verification from earlier reported tests. Record zero model/GPU work.

For provenance, append the user's latest correction: the earlier “pushed” handoff was corrected to “nothing pushed.” Report local remote-tracking ancestry separately and do not infer a current push or verified remote backup from it. No remote query is required. This clarification must not trigger history rewriting.

Stop at **P02D CORRECTED PREFLIGHT READY_FOR_REVIEW**, dispatch false, or state a concrete blocker. Do not execute the 192-answer/50-forward plan, seal P02, or start P03. The purpose of this correction is to make the already proposed experiment reliable and reviewable for the next execution decision.
