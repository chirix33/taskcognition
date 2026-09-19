# TaskCognition — ICLR 2027 Critique-Revised Draft Package

This directory contains the review-ready **pre-results protocol manuscript** for:

> **TaskCognition: When Does Overuse of Reasoning Models Degrade Answer Performance?**

The current draft follows the official anonymous ICLR 2027 format. It is intentionally prospective: **no TaskCognition experiment, development feasibility run, audit, power study, or test has been run, and no result is claimed.** The verified PDF has 12 pages total: main text ends on page 7, references start on page 8, and appendices follow the references. This is within ICLR’s nine-page main-text limit.

## Read this version

| File | Purpose |
|---|---|
| `TaskCognition_ICLR_2027_Critique_Revised_Verified.pdf` | **Authoritative verified review copy**, compiled from a clean copy of this package. |
| `taskcognition.tex` | Active LaTeX source. |
| `taskcognition.bib` | Active bibliography. |
| `TaskCognition_Critique_Assessment_and_Revision_Log.md` | Point-by-point assessment of the supplied critique, accepted changes, declined/narrowed requests, and validation record. |
| `PROTOCOL_SOURCE_OF_TRUTH.md` | Governance and change-control rule for the protocol. |
| `FROZEN_MANIFEST_TEMPLATE.md` | Pre-development schema for the dated manifest that must be frozen before final rollout labels. |
| `figures/taskcognition_architecture_critique_revised.pdf` | Vector architecture figure used by the active LaTeX source. |
| `figures/taskcognition_architecture_critique_revised.svg` | Editable source for the active figure. |
| `notes/TaskCognition_Critique_Assessment.md` | Detailed methodological assessment supporting the revision. |
| `notes/taskcognition_audit_design_calculation.py` | Deterministic design calculation showing why the original symmetric-Hoeffding audit was infeasible at the initial 450-input/midpoint-budget setup. It is not an experiment. |

`TaskCognition_ICLR_2027_Draft.pdf`, `TaskCognition_Revision_Summary.md`, `notes/Final_Validation.md`, and the original generic figure files are retained only as historical artifacts. They are **not** the active critique-revised manuscript or implementation specification. `notes/TaskCognition_Evidence_Pack.md` is explicitly superseded and must not be used to define the implementation.

## Build

From this directory, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
bibtex taskcognition
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
```

The package was independently rebuilt from a clean copy after the revision. The build has no LaTeX errors, unresolved citations, unresolved references, or overfull boxes. It may report non-blocking underfull spacing notices around bibliography/layout material.

## Before execution or submission

1. Run the disjoint **DEVELOPMENT** stage; it must validate the D/R package contract, parser, retry contract, cost support, and terminal 1,024/2,048 cap rule.
2. Use the full-pipeline simulation to freeze balanced audit size `n`, `K`, `b_min`, `alpha`, `beta`, the cost bounds, and the test threshold before final labels.
3. Populate and lock a dated manifest copied from `FROZEN_MANIFEST_TEMPLATE.md` before final TRAIN, TUNE, AUDIT, or TEST rollouts.
4. Keep all result and audit tables empty until the preregistered pipeline has run. Audit failure requires always-direct deployment.
5. Before a real submission, manually verify every source, citation, license, exact Qwen engine/API invocation, artifact, and result; then update the draft-stage AI-use disclosure.
