# P00 accepted seal

Status: **ACCEPTED**; P00 is **SEALED** by user-conveyed coordinator acceptance.

- Acceptance recorded at: `2026-09-28T14:15:45.561996+00:00` (UTC).
- Authority: current user's "Reviewed P01 prompt: Windows / RTX 5090 local Qwen smoke",
  preserved at `docs/prompts/P01_reviewed_local_qwen.md`, SHA-256 `f08794bfcf4a4f62361203f852d67e8f3735bdea9d2185fce3c43529f733e7a8`.
- Coordinator review: `docs/prompts/P00_coordinator_review.md`, SHA-256 `85fc76aba65def9c24a08bc89467ab3e344363e06e8b6b60953937d07714f893`.
- Review limitation: report-level acceptance only. The coordinator did not inspect the
  repository or rerun tests. This is not independent external code verification.
- Local revalidation: `reports/p01/preflight.json`, SHA-256 `2bc7161ea9e4fafc15cbf7c5b87f9676c92cf3c4d3eee040220064b76f09ae8e`;
  162 indexed files matched both P00 snapshot and worktree, 30 original files matched,
  C01-C03 present, 34 offline tests and current fixture verification passed.
- Completion report SHA-256: `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`.
- Evidence index SHA-256: `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`.
- Proposed seal SHA-256: `e414b43d0d20ed6e69a1aa974be3f50ff00edc8ba4e6250695d67a5c75670331`; unchanged.
- Implementation commit: `255860890dd480cdd8607e27957b251aa3e1cb1f`.
- Report-packet commit: `44cb33d8a178de9a15bf5ea3793e7d9ea64f7b6f`.
- Original phase-state snapshot: `configs/state_snapshots/P00_READY_FOR_REVIEW.json`,
  SHA-256 `3b28ac0a195d00a0d1b60200efb2dd6f6dcbf7c0f7f91d606f5200cab4306ed6`; also preserved in the P00 commit.
- User acceptance reference: "The user is conveying the coordinator's P00 report-level
  acceptance and authorizing this P01 scope." The reviewed prompt supersedes only
  the generic P01 prompt for this run. C01-C03 remain resolved.
- Authorized next phase: **P01 only**, reviewed eight-generation/40-GiB envelope.
- Scientific study/candidate/deployment freezes: NONE. P00 is engineering acceptance.

No old evidence hashes were changed. Future P01 source/state changes are checked against
the P00 Git snapshot, not misrepresented as unchanged current files. No final labels,
real generation, training, or held-out exposure occurred in the P00 revalidation.
