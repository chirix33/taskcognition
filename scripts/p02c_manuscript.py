"""Versioned manuscript/figure copy; preserve every original byte and equation."""
from pathlib import Path
from io import BytesIO
import shutil,json,hashlib,re,difflib
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
root=Path(__file__).resolve().parents[1];old=root/'docs/iclr2027';new=root/'paper/cr01-2026-10-05-v1';out=root/'reports/p02c'
new.mkdir(parents=True,exist_ok=False);(new/'figures').mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['taskcognition.tex','taskcognition.bib','iclr2027_conference.sty','iclr2027_conference.bst','math_commands.tex','natbib.sty','fancyhdr.sty']:
    shutil.copyfile(old/name,new/name)
before=(old/'taskcognition.tex').read_text(encoding='utf-8');text=before
def change(a,b):
    global text
    assert text.count(a)==1,a;text=text.replace(a,b)
change('No TaskCognition experiment, power study, audit, or test has been run, and all result cells are empty.','Bounded DEVELOPMENT diagnostics have been run; no gate comparison, power study, audit, or final test has been run, and all confirmatory result cells are empty.')
change('figures/taskcognition_architecture_critique_revised.pdf','figures/taskcognition_architecture_CR01_2026-10-05_v1.pdf')
change('DEVELOPMENT precedes TRAIN and freezes both packages before any final rollout label.','DEVELOPMENT precedes TRAIN and freezes both packages before any final rollout label. CR01 fixes both output caps at 2,048 total tokens; completion is descriptive and failures are retained.')
change('The active TeX and \\texttt{PROTOCOL\\_SOURCE\\_OF\\_TRUTH.md} govern the current draft.','This CR01 revision is governed by the preserved original reference PDF, the user-approved amendment dated 2026-10-05, and the synchronized operational protocol, including the previously accepted staged-manifest and failure-integrity clarifications.')
change('cost schedule, candidate hashes, and direct fallback.','cost schedule, candidate schema and selection rules, and direct fallback. Candidate hashes and deployment decisions are separate immutable child records created after tuning and audit, respectively.')
change('scalar cost accounting, cap feasibility, and sample/repeat allocation.','scalar cost accounting, descriptive completion at the fixed cap, and sample/repeat allocation.')
start='The cellwise terminal cap rule is fixed.';a=text.index(start);b=text.index('\n\n',a)
text=text[:a]+r'''The primary common D/R cap is fixed prospectively at \textbf{2,048 total generated tokens}, including native thinking and final output. Strict-valid-FINAL completion and failure subtypes are reported descriptively in all twelve mode-by-family cells. There is no 99\% completion eligibility prerequisite or automatic stop based on that threshold. Strict parsing and native scoring remain unchanged: valid partial scores are retained, and recorded model failures without a valid retainable answer score zero and remain in the distribution. Software/evidence integrity failures still stop the affected operation; unresolved design, cost support and audit-denominator requirements remain binding.

\paragraph{Development history and amendment.}
P02A and P02B were bounded six-family DEVELOPMENT diagnostics that exposed required-format and truncation problems. After inspecting those outcomes, the user approved CR01 on 2026-10-05, before any final labels. The original protocol had paused on development-feasibility concerns; these diagnostics did not formally test and reject its cap rule. Historical observations and scores retain their original package identities and remain DEVELOPMENT only. The exact P02B common instruction is retained as the candidate instruction; no further prompt search or scoring relaxation is adopted. The eventual comparison concerns these bounded answer packages, so differences may reflect solving, format compliance, truncation, or their combination; improved native task solving is not established by these diagnostics.''' +text[b:]
change('a failed resample is retained with its frozen zero-score rule rather than redrawn.','recorded model failures retain their frozen scores within each complete input-cluster resample, while missing or corrupted evidence stops analysis. A failed model answer does not zero an entire resample or permit redrawing to remove failure.')
change('one cap rule, fixed scorers','one fixed 2,048-token cap, strict format compliance, truncation risk, fixed scorers')
change('No TaskCognition result, audit passage, power estimate, or novel effect is reported in this manuscript.','The development history above is disclosed, but no learned-router comparison, audit passage, power estimate, final-test result, or novel effect is established.')
change('The active manuscript plus the governed dated manifest will be the sole implementation specification.','The original reference plus approved CR01 and accepted operational clarifications govern this active revision; the eventual reviewed, dated, hash-linked study and child manifests will govern execution.')
change('It did not execute TaskCognition experiments or generate evidence.','AI-assisted engineering also implemented and documented the bounded local DEVELOPMENT diagnostics. No final gate training, audit, or test was performed; the CR01 adoption itself used no model compute.')
change('retries, throughput, and one scalar ledger; apply the\n  cellwise cap rule; run high-repeat and full-pipeline','retries, throughput, and one scalar ledger; use the fixed\n  2,048-token cap and descriptive completion; run approved\n  repeated-draw pilots and full-pipeline')
change('terminal cap decision;','fixed 2,048-token CR01 contract and descriptive completion;')
(new/'taskcognition.tex').write_text(text,encoding='utf-8',newline='\n')
svg=(old/'figures/taskcognition_architecture_critique_revised.svg').read_text(encoding='utf-8')
for a,b in [('class="label">Cellwise cap','class="label">Fixed cap'),('class="small">1024 if all ≥99%','class="small">2,048 total'),('class="small">else 2048 if all ≥99%','class="tiny" style="font-size:16px">Report completion'),('class="small">else STOP','class="tiny" style="font-size:17px">Retain failures')]:
    assert svg.count(a)==1;svg=svg.replace(a,b)
(new/'figures/taskcognition_architecture_CR01_2026-10-05_v1.svg').write_text(svg,encoding='utf-8',newline='\n')
# Remove the two original text blocks (not a white overlay hiding old searchable text).
original=old/'figures/taskcognition_architecture_critique_revised.pdf';reader=PdfReader(original);page=reader.pages[0];content=page.get_contents();ops=content.operations;kept=[];block=None;removed=0
for args,op in ops:
    if op==b'BT':assert block is None;block=[(args,op)]
    elif block is not None:
        block.append((args,op))
        if op==b'ET':
            if any(s in str(block) for s in ('Cellwise cap','1024 if all ')):removed+=1
            else:kept.extend(block)
            block=None
    else:kept.append((args,op))
assert removed==2 and block is None;content.operations=kept;page.replace_contents(content)
w,h=float(page.mediabox.width),float(page.mediabox.height);overlay=BytesIO();c=canvas.Canvas(overlay,pagesize=(w,h),invariant=1)
for label,y,size,bold,color in [('Fixed cap',116,25,True,'#172033'),('2,048 total',148,21,False,'#334155'),('Report completion',177,16,False,'#475569'),('Retain failures',206,17,False,'#475569')]:
    c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size*w/1600);c.drawCentredString(661*w/1600,h-y*h/900,label)
c.save();overlay.seek(0);page.merge_page(PdfReader(overlay).pages[0]);writer=PdfWriter();writer.add_page(page)
figure=new/'figures/taskcognition_architecture_CR01_2026-10-05_v1.pdf'
with figure.open('xb') as f:writer.write(f)
extracted=PdfReader(figure).pages[0].extract_text();assert '99%' not in extracted and 'else STOP' not in extracted and '2,048 total' in extracted
template=(old/'FROZEN_MANIFEST_TEMPLATE.md').read_text(encoding='utf-8')
template=template.replace('It is not a substitute for the active scientific protocol in [`taskcognition.tex`](taskcognition.tex).','It is not a substitute for the original reference plus adopted CR01/C01-C03 and active [`taskcognition.tex`](taskcognition.tex).')
template=template.replace('SHA-256 hash of `taskcognition.tex` and this manifest','Specification version, original PDF hash, approved/adopted CR01 hashes, active TeX hash; manifest hash recorded externally (no self-hash)')
a=template.index('It must declare the terminal development cap decision.');b=template.index('\n\n',a)
template=template[:a]+'It must bind `TaskCognition-CR01-2026-10-05-v1` and common primary D/R caps of 2,048 total generated tokens. Completion and failure subtypes are descriptive; no completion certification or automatic threshold stop applies. Strict scoring, failure retention and all audit requirements persist. Other prospective primary caps are unsupported under this version. Historical configurations keep their original version and are not relabelled.'+template[b:]
template=template.replace('candidate hashes, all audit code','the candidate schema and selection rules (later child records carry candidate hashes), all audit code').replace('and failed-resample handling','and retained model-failure scoring within complete resamples; missing/corrupt evidence must stop analysis, not zero or redraw an entire resample')
(new/'FROZEN_MANIFEST_TEMPLATE.md').write_text(template,encoding='utf-8',newline='\n')
(new/'README.md').write_text('''# Active CR01 manuscript revision, 2026-10-05 v1

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
''',encoding='utf-8',newline='\n')
equations=lambda s:re.findall(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}',s,re.S)
assert equations(before)==equations(text)
assert re.search(r'\\title\{.*?\}',before).group()==re.search(r'\\title\{.*?\}',text).group()
assert sha(old/'taskcognition.bib')==sha(new/'taskcognition.bib')
diff=''.join(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile='historical/taskcognition.tex',tofile='CR01/taskcognition.tex'))
diff+=''.join(difflib.unified_diff((old/'figures/taskcognition_architecture_critique_revised.svg').read_text(encoding='utf-8').splitlines(True),svg.splitlines(True),fromfile='historical/Figure1.svg',tofile='CR01/Figure1.svg'))
(out/'manuscript_source.diff').write_text(diff,encoding='utf-8',newline='\n')
(out/'manuscript_provenance.json').write_text(json.dumps(dict(evidence_kind='development_observation',operation='offline_document_revision',compiled_manuscript=False,compile_status='UNAVAILABLE',compiler_discovery={n:shutil.which(n) for n in ('pdflatex','bibtex','latexmk','tectonic')},original_tex_sha256=sha(old/'taskcognition.tex'),revised_tex_sha256=sha(new/'taskcognition.tex'),bibliography_unchanged=True,title_unchanged=True,all_equation_and_align_blocks_unchanged=True,original_figure_sha256=sha(original),revised_figure_sha256=sha(figure),figure_removed_text_blocks=removed,original_source_snapshot='reports/p02c/pre_CR01_source_snapshot.zip',new_model_work=0),indent=2)+'\n',encoding='utf-8')
print('Active revision created; equations/title/bibliography unchanged; CR01 vector figure generated; full manuscript UNCOMPILED.')
