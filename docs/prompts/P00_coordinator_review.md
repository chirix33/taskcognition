# P00 coordinator review

Date: 2026-09-28 UTC (2026-09-27 America/Chicago).

Decision: ACCEPTED FOR PROGRESSION on a report-level review, subject to the local evidence revalidation specified in the reviewed P01 prompt. Do not treat this as an independent code audit or a claim that the coordinator reran the 34 tests. Codex records the P00 seal only after the local revalidation passes and the user conveys this handoff.

## Material reviewed directly

- Uploaded `P00_completion.md`, read in full.
- Uploaded `P00_proposed_seal.md`, read in full.
- Computed completion report SHA-256: `d92635ea671490365e88a7b4a8d4adb98d9f3fe333d29fc93ae83cf05e0494f2`; matches the proposed seal exactly.
- Computed proposed-seal SHA-256: `e414b43d0d20ed6e69a1aa974be3f50ff00edc8ba4e6250695d67a5c75670331`.
- Cross-checked the reported analytical fixture against the handoff: benefit -0.25, joint harm 0.375, corrected direct redraw 0.25, and both partial-decline estimates 0.375 are correct for the stated binary arrays.

The repository, code, full validation JSON, evidence index, source inventory, and hardware logs were referenced in the report but not attached. Their contents and reported 34 passing tests were not independently verified here. The conditional local preflight verifies them before progression; the P01 return packet must include machine-readable supporting evidence for the next review.

## Assessment

The report addresses every P00 exit criterion with named commands and evidence paths. It distinguishes fixtures from real outcomes, preserves model failures, rejects corruption, prevents premature collection, records all three approved clarifications, and explicitly reports checks that were not run. No scope drift is apparent in the report.

The governing PDF fingerprint matches the previously supplied revised manuscript. Recovery of original TeX/BibTeX/protocol resolves the original-source availability question, provided the reported fingerprints verify locally. Ignored original sources still need a backup before irreplaceable final work.

The implementation/evidence commit is reported as `255860890dd480cdd8607e27957b251aa3e1cb1f`. The completion packet has a separate subsequent commit to avoid a circular hash. Record that packet commit in the local acceptance record; do not confuse it with the implementation commit or modify a report merely to insert its own future commit hash.

Hardware is reported as Windows 11, RTX 5090 with 32,607 MiB VRAM, about 63.46 GiB RAM, and ample free disk. This supports trying the proposed native Windows backend, but does not establish CUDA kernel compatibility, native BF16 execution, Qwen fit, parsing reliability, or cap feasibility.

## P00 seal conditions

Before editing state or installing the P01 backend, Codex must:

1. Verify the supplied report hash, the referenced evidence index hash `cf65f8d4ef5b398f0e527cb7d78590b347afaf84d9ebe1707737b687ddedd935`, and the original evidence fingerprints against the P00 snapshot.
2. Run the offline P00 tests and fixture verification without overwriting the original logs or fixture bundles. Save the new local preflight results separately.
3. Confirm C01-C03 remain present and no real generation/fitting/audit/test exposure occurred during P00.
4. Preserve the proposed seal and its referenced evidence. Create a separate accepted record referencing this review and the actual user handoff, with the current local acceptance timestamp.

If any condition fails, stop before model installation/download/generation and return a targeted P00 discrepancy report. Do not rewrite evidence hashes to make verification pass.

Updating the phase-state file after successful verification is an expected new event. Its historical P00 hash remains a fingerprint of the earlier state. Preserve that state through the existing commit or a snapshot; do not retroactively rewrite the old evidence index. The same principle applies to code legitimately evolving in P01.

## Authorized next scope when conveyed by the user

Use `P01_reviewed_local_qwen.md` in place of the generic P01 prompt. Perform native runtime checks, one official pinned Qwen3-8B checkpoint, a small DEVELOPMENT-only smoke, native parser and admission/restart validation, and a report. P02 remains unauthorized.

No changes to the central hypothesis, required baselines, primary sampler, cap rule, population, audit, or final test are approved by this review. P00 acceptance is engineering progress only.
