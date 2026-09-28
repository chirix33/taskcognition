# TaskCognition: instructions to Codex

## Mission and authority

Implement the revised TaskCognition study and produce traceable evidence that can support or fail its claim. Do not optimize the research process for a positive result.

Read this file, `docs/PROTOCOL_SOURCE_OF_TRUTH.md`, `docs/DECISIONS_AND_GAPS.md`, and the active phase prompt before work. Consult the architecture, statistical, and evidence contracts for the work you perform. Read the reference PDF before implementing scientific behavior.

The user's explicit instructions govern. The included revised PDF fixes the scientific scope; the markdown operationalizes it. Before freeze, unresolved implementation choices belong in the decision register. After development, the accepted immutable study manifest and its hash-linked candidate/deployment records govern execution. If the PDF, code, existing TeX, or these files conflict, document the conflict and stop the affected action. Do not silently resolve a scientific conflict in favor of convenient code. The older draft, meeting suggestions, NSF proposal, and unrelated projects are context, not alternate specifications.

## Scope lock

1. Answer checkpoint: `Qwen/Qwen3-8B`, exact immutable revision pinned before final labels. No Qwen substitute, fine-tuning, LoRA, extra solver, or change of checkpoint.
2. Exactly D (`enable_thinking=False`) and bounded R (`enable_thinking=True`). Native mode control must be verified in the actual serialized request.
3. One gate sees only input text and approved input-only features, before answer generation. Exactly one admitted answer generation is used for a deployed query.
4. No direct preview, answer-conditioned routing, cascade, reasoning retry, answer repair, agent, tool call, or reasoning-to-direct runtime rescue.
5. TaskCognition predicts continuous score benefit and independent-draw joint spoilage. Required learned comparators: winner and factorized outcome routers. Never omit a strong comparator because it wins.
6. Six original-renderer Reasoning Gym families and equal family weights. No replacement of hard families, easy-case filtering, or new tasks to rescue results.
7. Frozen package cap: 1,024 if all 12 mode-by-family development cells meet 99% strict-valid-FINAL; otherwise 2,048 if all meet it; otherwise stop the confirmatory study as infeasible. Any bigger cap is separate development-only diagnostic work.
8. Separate DEVELOPMENT, TRAIN, TUNE, AUDIT, TEST roles. No final labels before the development freeze. No audit/test use in training, feature normalization, calibration, design, or candidate selection.
9. Independent repeated draws are nested within input clusters. K-squared cross-products are not independent samples.
10. Charge all gate work, selected answer work, and dispatched pre-admission attempts once. Free embeddings or inflated method-specific budgets are forbidden.
11. One frozen candidate per learned method, one audit per candidate, direct fallback on any audit failure. No re-audit after tuning to audit outcomes.
12. The primary claim requires the frozen test criterion against always-direct, winner deployment, and factorized deployment, all three. No equivalent/noninferior wording inferred from nonsignificance.

Jev and live LLM judges are parked comparisons outside this primary implementation. Do not install or call them. They require a separately authorized protocol; they cannot replace the required baselines. Do not import NSF decomposition, memory, Phi-JEPA, or RegBridge work.

## Phase discipline

- Work only on the named active phase. P00 is the initial phase.
- Implement complete vertical slices: executable path, necessary tests, evidence report, and honest limitations.
- Within the authorized phase, make routine reversible implementation choices and fix defects without repeated confirmations.
- Stop at `READY_FOR_REVIEW`, `BLOCKED`, or `STUDY_STOPPED`. Codex cannot mark its own phase `SEALED`.
- A phase is sealed only after review acceptance is conveyed by the user/coordinator. Record the acceptance verbatim or reference the message; never fabricate it.
- The next phase prompt both records the accepted previous seal and authorizes that next phase. Merely possessing later prompts does not activate them.
- Seals protect evidence and scope, not bugs. Record a change request when a sealed artifact needs correction and identify all invalidated downstream artifacts.
- Do not make user-approved research changes silently. Preserve the old study and label a revised study separately when fresh evaluation is required.

## Workstation and repository

Inspect OS, available GPU/VRAM, RAM, disk, Python, drivers, existing model/cache, and git status. Do not assume CUDA, Linux, or any particular hardware capacity. Do not expose secrets, home-directory contents, or credentials in reports. No cloud fallback or paid resources without explicit authorization.

Preserve dirty files and existing root instructions. Use a dedicated branch where possible. Commit only task-owned files when the active prompt permits it; no push, merge, history rewrite, or destructive cleanup. An absent git identity is not a reason to alter the user's global configuration; deliver a patch instead.

Use a project-local environment, pinned dependencies, and portable Python entry points. Do not upgrade system drivers or install operating systems. Prefer the simplest verified inference backend; avoid building multiple serving stacks without need. Any precision, quantization, or backend change must be recorded and finalized before labels; never silently quantize to fit memory.

## Execution and data integrity

- Fixtures, simulations, development, and final evidence have separate roots and explicit `evidence_kind` fields. Never populate an empirical result table with a fixture or simulation.
- Use stable task IDs, package hashes, per-input/per-package/per-draw RNG streams, append-only attempt records, and immutable outputs.
- Save dispatch/admission state before work. Unknown admission counts as admitted. On restart, reconcile unfinished attempts; never automatically regenerate an answer already admitted or with unknown admission.
- Pre-admission retries require logged proof of non-admission and the same request/RNG stream; charge every dispatch. An admitted failure is retained under the frozen scoring rule.
- Missing files and corrupted records are integrity failures, not low-scoring answers. Fail closed; do not silently fabricate zeros for absent evidence.
- Stage guards are workflow controls, not a claimed security boundary. Do not bypass them with direct scripts or read sealed outcomes informally.
- Reproducibility means preserved artifacts, versions, seeds, and numerical tolerances. Do not promise bit-identical GPU reruns unless demonstrated.

## Tests and reporting

Write tests for scientific failure modes, boundaries, leakage, costs, integrity, and resumability; not tests that merely echo implementation. Include analytical examples with known answers and adversarial parser fixtures. Verify the statistical theorem's assumptions and constants before final data; simulation cannot prove a theorem.

Use `docs/templates/PHASE_COMPLETION_TEMPLATE.md` for every phase. State commands actually executed and their exit status, test outcomes, data accessed, run counts, hashes, deviations, and resource use. Report failures and skipped checks prominently. Do not claim to have trained, audited, or evaluated what you have not run.

If infeasible or null, preserve evidence and complete an honest report. If the claim is supported, update the manuscript through generated tables and an evidence ledger. Never invent findings, citations, significance, or submission status.
