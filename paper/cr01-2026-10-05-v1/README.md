# Active CR01 manuscript revision, 2026-10-05 v1

This is the active revised source copy, derived from the preserved `docs/iclr2027` package. Original PDF/source hashes remain unchanged. Authority is the original reference plus adopted CR01 and C01-C03; see `docs/amendments/CR01_2026-10-05_v1.md` at repository root.

**Manuscript compilation: UNAVAILABLE in this workspace.** No pdflatex, bibtex, latexmk or tectonic was found on PATH, in bundled native dependencies, or the checked standard TeX installation locations. No toolchain was installed. This is a multi-file manuscript with bibliography/style/figure dependencies, outside the built-in standalone compiler's single-file contract. No amended full-manuscript PDF is claimed.

`taskcognition.tex` and `taskcognition.bib` are the active sources. Figure 1 uses the distinctly named CR01 PDF and matching SVG. The vector PDF removes the old cap text blocks and replaces only their text; it is not a raster edit or a hidden old-text overlay. Its changed box is rendered and inspected. Full revised pagination/citations/line breaking remain unverified until compilation.

With the existing required TeX packages in an independently available toolchain, run in this directory:

```text
pdflatex -interaction=nonstopmode -halt-on-error -jobname=TaskCognition_CR01_2026-10-05_v1 taskcognition.tex
bibtex TaskCognition_CR01_2026-10-05_v1
pdflatex -interaction=nonstopmode -halt-on-error -jobname=TaskCognition_CR01_2026-10-05_v1 taskcognition.tex
pdflatex -interaction=nonstopmode -halt-on-error -jobname=TaskCognition_CR01_2026-10-05_v1 taskcognition.tex
```

The manifest template remains incomplete/unfrozen. P02C performs offline adoption only; it starts no final labels, gate training, audit or P03 work. Historical diagnostic results are not confirmatory results.
