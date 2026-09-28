# P01 v2 coordinator acceptance

Date: 2026-09-28. Decision: ACCEPTED FOR P01 SEAL, with the disclosed live-D limitation retained.

This acceptance closes the specific worker-error blocker from the previous review. When the user conveys this review and the accompanying P02A prompt to workstation Codex, Codex may verify the accepted artifacts locally, record the P01 accepted seal, and begin only the bounded P02A scope. This document does not assert that the workstation's phase state has already changed.

## Evidence reviewed independently

The supplied v2 ZIP was extracted into an isolated review directory. The user's repository was not modified, and no model or GPU execution was performed by the coordinator.

- All 242 v2 indexed files matched their SHA-256 values.
- Uploaded completion and proposed-seal files matched their ZIP copies byte for byte.
- The embedded original ZIP matched the previously reviewed ZIP byte for byte; its 215 indexed files were reverified.
- The supplied offline suite was rerun: **81 tests passed**, including 19 worker-boundary regressions.
- The supplied preservation/replay script was independently run with a new output filename. It verified 84 protected files, the original request/result/event fingerprints, 15 events, three requests, 567 output tokens, and retained scores **0, 1, 0**. Only the three corrected source files and current phase state differ among the 215 prior indexed current paths.
- The worker, supervisor, ledger diff, and actual-main fault-injection tests were inspected. Historical GPU behavior is supported by supplied P01 records, not a new coordinator GPU test.

| Accepted artifact | SHA-256 |
|---|---|
| P01_completion_v2.md | `e75e0f4e99396223b61beb3f378c10d3a3a7c9d5db4db0d248700fae5ac69f13` |
| P01_proposed_seal_v2.md | `ea632c19ffa3a9b842e6a3e74c7fe3cd078cf0dbceda7eb347307bbe12bcf4da` |
| P01_evidence_manifest_v2.json | `1237761e49fcee9a9e027324995f6452b27b83417b205e12c44d451940b09a3f` |
| P01_review_packet_v2.zip | `dab8fd3ae4ea7b09e5802de7f02ee12f9f00dbf843c857e5921ca9dc69a639b3` |

Accepted corrected code/evidence commit: `6e8cec19d3e7f374aebddaa4f9b410767b02676a`. The separate report-packet commit should be identified locally when recording the seal. The installed historical wheel does not contain this correction; subsequent execution must establish its actual imported source and preserve that distinction.

## Why the correction is accepted

Unclassified errors at the generation boundary now produce unscored incident diagnostics and propagate. Callback errors are latched, preventing a backend from swallowing an evidence failure and then authorizing scoring. Partial valid-looking text cannot override that failure. The supervisor charges observed work once, rejects incidents and legacy swallowed model errors, and retains no-replay protection. Intentional cancellation and known timeout semantics remain covered.

The new regressions call the production `worker.main()` with mocked backend dependencies and real callbacks/ledger/parser/supervisor components. They address the previously missed path. The supplied before/after logs also document that these tests detect the reviewed defect.

No evidence indicates that this previously unexercised defect affected the three historical observations. Their records remain valid for their original smoke/diagnostic purposes.

## Limits carried forward

P01 demonstrates the local D/R request path, strict scoring, and interruption/restart behavior. It does not establish six-family cap feasibility or the paper's routing claim.

The initial D output was numerically correct but missing FINAL tags. Its primary score remains zero. There is still no live valid-FINAL D success. This is a disclosed interface-development issue for P02, not a reason to rewrite P01 outcomes or consume its unused generation slots.

P01's remaining five slots stay inactive. The next prompt authorizes a separate 24-generation six-family integration slice within P02. It does not authorize the formal cap study, high-repeat pilot, final labels, training, audit, or test. P02 cannot be sealed on that slice alone.
