# P04 prompt: freeze and collect TRAIN/TUNE evidence

Execute only after P03 design, resource ceiling, and all required decisions have been accepted. Implement P04 only. No AUDIT or TEST model outcomes may be generated or inspected.

## Work

1. Reconcile accepted decisions with the revised PDF and decision ledger. Create the immutable base study manifest, not a mutable config labeled frozen. It binds model/tokenizer/engine/precision, effective samplers, cap, templates/prompts/parsers/scorers, features, all generator configs, split rules, K/counts, alpha/beta/b_min/delta_score/gamma, cost bounds, timeout/retry behavior, resource budgets, selection/parity rules, secondary registry, analysis code and failure conventions.
2. Use staged hash records: base manifest now; candidate manifest after selection; deployment manifest after audit. Do not invent future candidate hashes or rewrite the base later.
3. Generate the frozen final split identity manifests using independent streams. Validate disjoint seeds AND latent problem identities; detect exact prompt duplicates/collisions under an outcome-independent rule committed before collection. Keep renderer variants of a latent problem together. Do not deduplicate by observed answer quality. Keep held-out outcomes hidden behind stage-specific access.
4. Validate cap decision provenance, cost bounds, analytical tests, feature schema, parity plan, resource plan, backups, and stage guard before first final generation. `freeze` rejects unresolved required values, unpinned revisions, or unsupported claims about bounds.
5. Collect the specified K independent D/R draws on TRAIN and TUNE only, using the frozen packages. Use stable IDs and append-only attempt records. Resume only genuinely unfinished/non-admitted work under the frozen policy. Retain all admitted failures; no answer repairs or new package configuration mid-run.
6. Aggregate and reconcile scheduled counts, attempts, admitted draws, scores, zero failures, per-cell QC, all-in package costs, and exact artifact hashes. Charge discarded pre-admission attempts as specified. Stop on integrity/range/manifest violations rather than force a clean table.
7. Produce a completeness/disjointness report and immutable data manifests; verify backup fingerprints. Collection may summarize TRAIN/TUNE operational quality, but must not alter the frozen study or choose models in this phase.

## Exit criteria

- Accepted study decisions become a valid immutable manifest with no unknown required fields.
- All TRAIN/TUNE cells contain exactly the planned draw records, including explicit admitted failures; no hidden missingness or duplicates.
- Raw-to-aggregate lineage and resource ledger reconcile.
- Frozen study remains unchanged; AUDIT/TEST outcomes unexposed.
- Research wall-time, disk, calls, and tokens reported against the accepted envelope.

Write `reports/phases/P04_completion.md`, study/data manifest paths, integrity/QC summaries, and proposed seal. If a package bug or package change is needed, preserve affected labels and open a change request; the paper requires downstream rollout-derived labels to be regenerated under a new freeze. Stop for review.
