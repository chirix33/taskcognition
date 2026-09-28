# P01 corrected proposed seal v2

Status: **PROPOSED / READY_FOR_REVIEW**. Acceptance **PENDING**. P01 is **not SEALED**.

- Proposed at `2026-09-28T16:17:44.022328+00:00` under the user's offline targeted correction prompt.
- Coordinator review: `reports/P01_coordinator_review.md`, SHA-256 `e7a46b8c3719d7ae6e85685c9c6655b48e05f7b8094a59e9b1c7052586b7bf85`. Review requested a correction; it did not seal P01. Coordinator independently ran supplied offline tests/replay, not GPU generation.
- Corrected completion: `reports/phases/P01_completion_v2.md`, SHA-256 `e75e0f4e99396223b61beb3f378c10d3a3a7c9d5db4db0d248700fae5ac69f13`.
- Corrected index: `reports/phases/P01_evidence_manifest_v2.json`, SHA-256 `1237761e49fcee9a9e027324995f6452b27b83417b205e12c44d451940b09a3f`.
- Corrected code/evidence commit: `6e8cec19d3e7f374aebddaa4f9b410767b02676a`.
- Original execution source: `683e9a3f7c5c539a3bb5d8d959b98d4c9319721f`; reviewed code: `7c71cb368eb2eaf97e42df8e0eacc6f2f3f0e322`. Exact production diff in `reports/p01_correction_v2/source_diff.patch`; source hashes in final preservation/replay JSON.
- Repair: unclassified generation/admission/callback/token-check/synchronization errors preserve unscored incident diagnostics and re-raise. Callback failures remain fatal if swallowed by a backend. No generic exception/runtime-error outcome allowlist. Supervisor charges observed work once, stops on incidents/legacy model_error outcomes and forbids replay.
- Validation: all original 62 plus 19 focused tests pass (81 total). Identical final 19 regressions against reviewed source produce 11 failures, 5 missing-diagnostic errors and 3 success-path passes. Actual worker.main is exercised with mocked backend dependencies; no GPU or weights.
- Historical preservation: 84 protected files unchanged; 211 previous indexed current files unchanged, with only three corrected source files and phase state evolving. Original index/report/seal/ZIP and 15 real ledger events remain unchanged. All three historical model_error values are null and results intact; no observed branch impact and no automatic invalidation.
- Scientific interpretation: D's correct numeric list lacks FINAL tags and retains primary score 0; R retains score 1; deliberate interruption retains score 0 as its distinct diagnostic. No live valid-FINAL D example exists. No wrapper relaxation, answer repair or new D generation.
- Resource statement: zero new model loads, real generations, GPU work, downloads, installs or dependency changes. Historical totals remain 3 admitted and 567 tokens. Five unused slots inactive. No change to scientific values or P02 plan.
- State: event `004_P01_correction_v2_ready.json`, P01 READY_FOR_REVIEW, real_dispatch_enabled=false, P00 acceptance preserved, no next phase authorized.
- Runtime note: corrected source was tested with PYTHONPATH=src; installed historical wheel was not replaced. Commit/hashes identify this repair separately.
- Packet: `reports/p01_correction_v2/P01_review_packet_v2.zip`; read-back hashes/size in `reports/phases/P01_packet_receipt_v2.json`. Prior packet retained byte for byte inside the new packet. Separate local packet commit contains the receipt and is identified on delivery.
- Exclusions: model weights/environments/secrets/private meetings; no push/merge/publication, no training/final labels/AUDIT/TEST/P02 work.

Reviewer acceptance must be conveyed by the user/coordinator before any P01 accepted seal or next-phase activation. This proposal cannot seal itself.
