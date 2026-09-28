# P00 seal record

Status: **PROPOSED**

- Phase: P00 (bootstrap and protect the study).
- Completion report hash: `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`.
- Code commit: `255860890dd480cdd8607e27957b251aa3e1cb1f` on `codex/p00-bootstrap`.
- Evidence manifest hash: `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`.
- Source PDF hash: `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`.
- Study / candidate / deployment hash chain: NONE; no study freeze or model revision selected.
- Checks passed: offline installation, 34 tests, exact K=4 aggregates, evidence isolation,
  freeze/split/feature/duplicate guards, immutable resume and artifact recomputation.
- Material limitations: fixture-only evidence; no native model/scorer/parser, CUDA runtime,
  admission recovery, theorem proof, final collection, fitting, audit or test execution.
  Original manuscript sources remain ignored and need backup before irreplaceable work.
- Clarifications: C01-C03 resolved by the user and recorded in the decision ledger.
- Unresolved decisions: D03-D17 remain development decisions. None blocks P00 review;
  compatible backend/revision/precision and a bounded plan must be settled in authorized P01.
- Acceptance message/reference: **PENDING**. User clarification is not phase acceptance.
- Acceptance timestamp: **PENDING**.
- Authorized next phase: **NONE** until an explicit next-phase prompt is issued.

## File fingerprints

| Relative path | SHA-256 | Role |
|---|---|---|
| `reports/phases/P00_completion.md` | `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2` | Review evidence |
| `reports/phases/P00_evidence_manifest.json` | `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935` | Review evidence |
| `reports/p00_validation_v2.json` | `e7d55c231a359c5d26d237d5502476cfed47a45a61ed2665ba16947f386794d9` | Review evidence |
| `reports/source_inventory.json` | `6beda63fcb7fea121ccf0d8b910bc77a1badaee837167790f16065fbb297ce26` | Review evidence |
| `reports/environment_p00_v2.json` | `afd17a52d695de90e8b9547232f8de20e3990bb275df9cc1669dbe52d3acb27f` | Review evidence |
| `reports/decision_ledger.md` | `8adf51a76e251bd358f700dd4ee8e7c0a3ff5de226a9b76b33a73a4559afc267` | Review evidence |
| `configs/phase_state.json` | `3b28ac0a195d00a0d1b60200efb2dd6f6dcbf7c0f7f91d606f5200cab4306ed6` | Review evidence |
| `artifacts/fixtures/p00-analytical-v2/manifest.json` | `c7575da8e3b7cef956138f172627b3d45f0821947dc7ed2471bae2ad3ea4db3a` | Review evidence |

The evidence index contains the complete implementation, contract, environment and
fixture fingerprints. This proposed seal references that index and the completion report;
it does not hash itself. The code commit predates this report packet to avoid a cycle.

## Later invalidation

None. If corrected after review, append a dated change request identifying affected
evidence and downstream records, preserving this record and the acceptance history.
Codex has not marked P00 SEALED or authorized P01.
