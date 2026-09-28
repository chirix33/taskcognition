# Sources and provenance

## Governing manuscript

- Supplied filename: `TaskCognition_ICLR_2027_Critique_Revised_Verified(1).pdf`.
- Bundle path: `reference/TaskCognition_Revised_Verified.pdf`.
- SHA-256: `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`.
- 12-page revised pre-results manuscript; verified by reading its main text and appendices for this handoff.
- Sections 3-4: estimands, objective, learning targets. Section 5: package/failure contract. Section 6: comparators and population. Sections 7-8: audit, planning, test. Appendix A-C: manifest, reporting, checklist.
- The source TeX, bibliography, and original `PROTOCOL_SOURCE_OF_TRUTH.md` referenced by the PDF were not supplied. This bundle's protocol is a new operational transcription. Locate originals at P00; reconcile conflicts before any affected freeze. Do not claim originals were inspected if absent.

## Context boundary

The September 19 part-2 meeting discussed judge-based routing and Jev. Those suggestions do not override the revised primary protocol. Earlier meeting files, the NSF macro-project proposal, and example use cases do not authorize decomposition, memory, or additional-model experiments here. The NSF proposal was not used as an implementation specification.

## Primary technical references

These are implementation references, not permission to change the paper. Recheck exact APIs in the pinned environment and archive the version used.

1. Qwen3-8B official model card: https://huggingface.co/Qwen/Qwen3-8B
2. Qwen official Transformers guide: https://qwen.readthedocs.io/en/v3.0/inference/transformers.html
3. Qwen official quickstart: https://qwen.readthedocs.io/en/v3.0/getting_started/quickstart.html
4. Reasoning Gym upstream: https://github.com/open-thought/reasoning-gym
5. Maurer and Pontil, Empirical Bernstein Bounds and Sample Variance Penalization (2009): https://www.cs.mcgill.ca/~colt2009/papers/012.pdf and https://arxiv.org/abs/0907.3740

References checked 2026-09-28: Qwen's official card supports native thinking switches and recommends much longer output allowance than this manuscript's 1,024/2,048 cap. Therefore the cap completion study is substantive, not a presumed pass. Verify the original theorem for independent, potentially nonidentically distributed bounded rows, sample variance convention, and both bound directions during P03.

No existing experiments, power estimates, or manuscript result cells were supplied as empirical evidence for this implementation. The handoff adds no empirical findings.

## P00 repository discovery and clarification (2026-09-28 UTC)

The handoff's absence statement above described the bundle, not the complete repository.
P00 found `docs/iclr2027/taskcognition.tex`, `taskcognition.bib`, the original protocol,
and its manifest template. Its verified PDF has exactly the governing SHA-256 above.
These ignored original files were read and preserved; P00 did not rebuild the manuscript.
Fingerprints are in `reports/source_inventory.json`. The user's current PDF-governed
scope and accepted clarifications govern implementation; recovered older notes do not
activate alternate specifications. Staged candidate hashes (C01), failure/corruption
handling (C02), and final TRAIN/TUNE evidence kinds (C03) are recorded in
`reports/decision_ledger.md`, with the user's acceptance/clarification text.
