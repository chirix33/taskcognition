# TaskCognition — ICLR 2027 Draft Package

This directory contains the review-ready **pre-results manuscript** for:

> **TaskCognition: When Does Overuse of Reasoning Models Degrade Answer Performance?**

The paper follows the official anonymous ICLR 2027 format. It is intentionally prospective: **no experiment has been run, and no result is claimed**. The compiled PDF has 11 pages total; main text and required/recommended statements end on page 7, references begin on page 8, and appendices begin on page 10. This satisfies the nine-page main-text limit.

## Main files

| File | Purpose |
|---|---|
| `TaskCognition_ICLR_2027_Draft.pdf` | Compiled review copy |
| `taskcognition.tex` | Main LaTeX source |
| `taskcognition.bib` | Bibliography |
| `figures/taskcognition_architecture.pdf` | Vector architecture figure used by LaTeX |
| `figures/taskcognition_architecture.svg` | Editable architecture source |
| `TaskCognition_Revision_Summary.md` | Plain-language explanation of the protocol and revisions |
| `notes/TaskCognition_Evidence_Pack.md` | Literature, novelty, benchmark, and evaluation evidence base |
| `notes/Final_Validation.md` | Build, layout, and version checks |

The official ICLR style files are retained in this directory.

## Build

From this directory, run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
bibtex taskcognition
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
pdflatex -interaction=nonstopmode -halt-on-error taskcognition.tex
```

## Before submission

The experiments, power analysis, diagnostic generator, parser tests, frozen split manifests, and baseline implementations still need to be executed. Populate the empty result tables only from the preregistered pipeline. The draft-stage AI-use statement must be updated after the authors manually verify every source, citation, method, artifact, license, and result.
