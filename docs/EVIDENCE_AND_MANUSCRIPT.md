# Evidence and manuscript completion

## Evidence kinds

Every artifact records one of `fixture`, `development_observation`, `development_simulation`, `final_train_labels`, `final_tune_labels`, `confirmatory_audit`, `confirmatory_test`, or `secondary_descriptive`. A fixture checks code. A simulation checks behavior under declared assumptions. Neither is an observed TaskCognition result.

P00 user clarification (2026-09-28 UTC): `final_train_labels` requires split `TRAIN` and supports fitting; `final_tune_labels` requires split `TUNE` and supports the prescribed calibration and selection. Both require an accepted frozen study manifest before real collection. Keep and validate the separate split field. These new kinds do not authorize P00 collection.

## Required outputs

| Output | Required fields / interpretation |
|---|---|
| Environment/source report | Hardware, exact checkpoint/tokenizer/engine/scorer/encoder revisions, precision, template, code and source hashes |
| Package QC table | All 12 mode-family cells; admitted requests, pre-admission attempts, valid FINAL, cap failures, delimiter/wrapper/syntax failures, partial/wrong/perfect scores |
| Resource report | Actual research calls/tokens/time/disk plus separate single-query all-in deployment cost and hard-bound derivation |
| Development design report | K/n/sample decisions, simulation assumptions, Monte Carlo intervals, false enablement/fallback, conditional/unconditional power or minimum detectable effect |
| Parity table | Same features/data, trainable counts, loss definitions, optimizer budgets, trial counts, seeds, calibration opportunity, thresholds searched, consumed resources |
| Audit table | Candidate hash, B/LB, Z/UZ, C/UC, Delta/LDelta, all four checks, fallback decision |
| Adequacy table | Selected inputs, route rate, direct-success mass, raw nested successes, Kish weight concentration |
| Primary results | Score, R_spoil, R_DD, routing rate, scalar cost; actual audit-selected deployments, not just pre-audit candidates |
| Primary contrasts | TC minus D/winner/factorized, point estimates, three one-sided lower bounds, delta_score, all-three support flag |
| Diagnostics | Per-family effects, independent redraw reference, epsilon declines, failure composition, empirical oracle labeled optimistic |
| Secondary registry results | Planned analysis, actual execution, evidence population, uncertainty method, limitations, skipped/unavailable reasons |
| Claims ledger | Sentence/claim, artifact hash, population, estimate, uncertainty, allowed wording, manuscript location |

Recreate tables from machine-readable evidence; do not hand-copy values into LaTeX. Store commands, configurations, seeds, package identities, units, and plotting data beside figures. Research figures should use standard plotting tools and export PDF/SVG/PNG as needed.

## Claim decision categories

- `SUPPORTED_IN_DECLARED_SETTING`: valid study; all required primary lower bounds exceed delta_score. State the checkpoint/packages/population and uncertainty.
- `NOT_ESTABLISHED`: valid study; one or more criteria fail. Distinguish observed disadvantages from imprecision. Nonsignificant does not mean equivalent.
- `INFEASIBLE`: prescribed bounded package or informative design cannot meet feasibility requirements within declared resources.
- `INVALID_OR_INCOMPLETE`: protocol breach, missing evidence, or unexecuted required work prevents adjudication.

Frequent audit fallback is a result, not an omitted row. If TC falls back to D, its paired score difference versus D is zero and the primary superiority claim cannot hold.

## Paper deliverables

P09 uses original source TeX/BibTeX if recovered. Preserve a pristine copy and generate a diff. If source is unavailable, provide an explicitly labeled replacement manuscript draft plus generated tables/figures and an insertion map; do not pretend to have edited the original source.

Update abstract, methods, experiment design, results, uncertainty, limitations, compute/resources, reproducibility, and AI-use statement from observed evidence. Replace planning placeholders with actual values and mark every deviation. Do not infer submission status from the PDF's conference template text.

Explain:

1. Whether direct target learning helped over winner and factorized methods under matched resources.
2. Which audit constraints bound deployment and how often fallback occurred.
3. What score/cost/spoilage tradeoff was observed, including gate feature cost.
4. Whether apparent reasoning degradation was dominated by cap/parser failures or completed wrong answers.
5. Why the independent-draw target does not establish causal answer spoilage.
6. Why results do not generalize automatically to other checkpoints, caps, renderers, or free-form evaluation.

The broad question "when should a model reason?" is established prior work. Novelty must remain the tested direct-target comparison. Recheck citations against original sources in manuscript preparation; do not copy unsupported novelty claims from earlier meetings.

## Reproducibility release

Provide pinned environment, source fingerprints, frozen manifests, data-generation/config scripts, permitted data or reconstructable IDs, evaluation and table-generation commands, model download instructions, artifact hashes, known nondeterminism, and small offline smoke fixtures. Respect data/model licenses. Do not release credentials, private meetings, or proprietary material. This handoff does not authorize publishing the repository or submitting the paper.

Validate a clean reproduction of analysis from saved final rows without rerunning Qwen. Recompute the three claim contrasts and manuscript tables from the same hashes. If rendering a manuscript, inspect pages for clipping, broken references, missing figures, and malformed equations.
