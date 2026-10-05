"""Finalize the offline checkpoint and its review report; no live execution path."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[1];out=root/'reports/p02c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n')
assert load(out/'verification.json')['status']=='PASS'
assert load(out/'instruction_hash_verification.json')['status']=='PASS'
assert load(out/'visual_verification.json')['all_pixels_outside_cap_box_unchanged']
commands=[
 dict(command='git switch -c codex/p02c-cr01-adoption',exit=0,result='Task branch; unrelated user files preserved'),
 dict(command='.venv/Scripts/python.exe scripts/p02c_establish.py',exit=0,result='Accepted P02B hashes/598 files/commits verified; original source snapshot; one acceptance event'),
 dict(command='.venv/Scripts/python.exe scripts/p02c_adopt.py',exit=0,result='CR01 authority and active document synchronization'),
 dict(command='bundled node .../pdf/container_tools/mark_artifact_operation_started.mjs --operation-kind edit --expected-output-count 1 --output-format pdf',exit=0,result='PDF operation marker'),
 dict(command='bundled Python scripts/p02c_manuscript.py',exit=0,result='Revised TeX and vector figure; equations/title/BibTeX unchanged',warning='pypdf replace_contents deprecation; result independently text/raster checked'),
 dict(command='pdftoppm -png -singlefile -r 96 paper/cr01-2026-10-05-v1/figures/taskcognition_architecture_CR01_2026-10-05_v1.pdf reports/p02c/visual_check/figure_CR01',exit=0,result='Rendered and visually inspected changed box'),
 dict(command='pdftoppm -png -singlefile -r 96 docs/iclr2027/figures/taskcognition_architecture_critique_revised.pdf reports/p02c/visual_check/figure_original',exit=0,result='Historical comparison render',warning='Missing display fonts Symbol/ArialUnicode notices; only cap-box pixels differ'),
 dict(command='.venv/Scripts/python.exe scripts/p01_command.py reports/p02c/verification_command.json .venv/Scripts/python.exe scripts/p02c_verify.py',exit=1,result='New template referenced nonexistent package.json; corrected to package_base.json'),
 dict(command='.venv/Scripts/python.exe scripts/p01_command.py reports/p02c/verification_command_v2.json .venv/Scripts/python.exe scripts/p02c_verify.py',exit=0,result='Affected-risk checks passed'),
 dict(command='Ad-hoc exact-wrapper hash comparison with hashlib.sha256(wrapper.encode())',exit=1,result='Compared raw UTF-8 to historical canonical-JSON hash; investigated original serializer, no content mismatch'),
 dict(command='Exact-wrapper comparison using taskcognition.contracts.digest plus separate raw UTF-8 SHA',exit=0,result='Exact P02B text preserved; both hash encodings explicit in template and verification'),
 dict(command='pdflatex / bibtex full-manuscript compilation',exit=None,status='NOT_RUN_UNAVAILABLE',result='No toolchain on PATH, bundled native runtime or standard checked paths; multi-file project unsupported by standalone app compiler; no installation'),
 dict(command='Historical regression suite',exit=None,status='NOT_RERUN',result='No execution/test source changed; consistency/hash and production closed-dispatch checks used; no manufactured tests')]
save(out/'commands_and_limitations.json',dict(evidence_kind='development_observation',operation='offline_command_receipt',commands=commands,new_model_compute=0))
statepath=root/'configs/phase_state.json';state=load(statepath);assert state['active_phase']=='P02C' and not state['real_dispatch_enabled']
now=datetime.now(timezone.utc).isoformat();event='configs/state_events/014_P02C_review_checkpoint.json'
save(root/event,dict(evidence_kind='development_observation',event='P02C_offline_review_checkpoint',timestamp_utc=now,previous_state_sha256=sha(statepath),status='READY_FOR_REVIEW',verification_sha256=sha(out/'verification.json'),instruction_verification_sha256=sha(out/'instruction_hash_verification.json'),real_dispatch_enabled=False,p02_complete=False,p02_sealed=False,p03_started=False,new_generations=0))
state.update(status='READY_FOR_REVIEW',latest_event=event,real_dispatch_enabled=False);statepath.write_text(json.dumps(state,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
paths=set(load(out/'active_edit_paths.json'))
paths.update(p.relative_to(root).as_posix() for p in (root/'paper/cr01-2026-10-05-v1').rglob('*') if p.is_file())
paths.update(p.relative_to(root).as_posix() for p in (root/'scripts').glob('p02c_*.py'))
paths.update(['reports/decision_ledger.md','reports/phases/P02B_accepted_checkpoint.md','configs/state_snapshots/P02B_accepted_before_P02C.json','configs/state_events/012_P02B_accept_P02C_offline.json',event])
paths.discard('reports/p02c/active_edit_paths.json')
save(out/'changed_artifacts.json',dict(evidence_kind='development_observation',operation='offline_change_inventory',files={n:sha(root/n) for n in sorted(paths)},authority='User P02C prompt and approved CR01; no final manifest or live authorization',self_report_packet_hashes='Bound externally by P02C_evidence_index.json/receipt to avoid cycles'))
amendment=root/'docs/amendments/CR01_2026-10-05_v1.md';approval=root/'docs/TaskCognition_CR01_APPROVED.md';verify=load(out/'verification.json')
report=f'''# P02C completion report

Status: **P02C READY_FOR_REVIEW**. **Real dispatch is disabled. P02 remains incomplete and unsealed; P03 is unstarted.**

## Scope and approval trace

Authority: user prompt “P02C: adopt approved CR01 and synchronize the study.” User approval date **2026-10-05**, America/Chicago; approval verbatim **“Understood. I approve it”**. No repeat approval was requested. Approved source SHA-256 `{sha(approval)}`. Adopted [CR01 v1](../../docs/amendments/CR01_2026-10-05_v1.md) SHA-256 `{sha(amendment)}`; its actual UTC adoption time and the approval date are separately recorded in event 013 and the decision ledger.

P02B was not previously recorded accepted. All four supplied hashes and all **598 indexed ZIP/current files** matched before editing. Verified pre-dispatch `72d88843067b8a8f0f29d2937587a102d5a24f6b`, evidence `ba3ef09dd8db95a1e60a380723f398f99e5d52d4`, packet `123a43ff198b2e1a450b98b6be226a2cbea896e9`. Event 012 records acceptance once and offline P02C activation. The draft/review were absent from the initial inventory; after the user supplied their local paths, both were read and hash-linked in authority_supplement.json and event 013. The original acceptance event was not duplicated or rewritten. No independent coordinator GPU verification is claimed.

P01 remains sealed; P02A/P02B are accepted development checkpoints. CR01 resolves the pending scientific-choice pause only. Original reference PDF SHA-256 **9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8** is unchanged. The complete original manuscript/source snapshot and active pre-edit documents are recoverable from pre_CR01_source_snapshot.zip and its verified manifest.

Branch `codex/p02c-cr01-adoption`, based on packet commit `123a43ff198b2e1a450b98b6be226a2cbea896e9`. Task-only local commits and source diff are identified in source_commits.json. No push, merge, history rewrite, destructive cleanup or unrelated-file commit. The user's PNG, approval, draft, review, P02C prompt and P02A review remain untouched and untracked; authority copies may appear in the local review ZIP.

## Delivered slice

The active CR01 specification fixes both primary output caps at **2,048 total generated tokens** and makes completion descriptive, without a 99% eligibility prerequisite or automatic stop based on that threshold. Strict channel/FINAL/syntax/native scoring, partial credit, failure retention, all-in cost, denominator adequacy, four audit checks, matched winner/factorized comparators and all three primary superiority criteria remain intact.

AGENTS, protocol, decisions/ledger, roadmap, architecture, evidence/source guidance, navigation, future P02-P09 prompts and applicable templates are synchronized. The new incomplete development design template records version/amendment and both cap values; remaining freeze values are null, final_freeze false and dispatch false. It is **not a study/candidate/deployment manifest**. The exact P02B wrapper is preserved, with its canonical-JSON hash and raw UTF-8 hash explicitly distinguished.

[Reference audit](../p02c/reference_audit.md) and reference_scan.json classify changed active references, preserved historical rules and incidental numerals. Original prompts, reports, plans, scores, receipts, ZIPs, source snapshots and regression fixtures retain their historical identities. No blanket replacement or reinterpretation of historical 1,024 observations occurred.

No general completion-eligibility validator exists in current executable code. Existing cap guards are closed P01/P02A/P02B workflow rules; they remain unchanged. StudyManifest remains UNFROZEN-only and final collection rejects. No inference, scorer, target, statistical, stage or test source changed; no new freeze implementation or parallel toy validation was introduced. A later authorized CR01 runner/freeze validator must enforce the explicit version/cap and remaining required fields. This slice does not claim that production final-freeze validation is complete.

## Manuscript

The active revision is [paper/cr01-2026-10-05-v1/taskcognition.tex](../../paper/cr01-2026-10-05-v1/taskcognition.tex), with unchanged BibTeX/style dependencies. Section 5, Figure 1's cap box, affected abstract/status, limitations, reproducibility, appendix/checklist and AI-use history now reflect fixed bounded packages and outcome-informed P02A/P02B development. The original route was paused, not formally cap-rejected. No gate result, new native-solving conclusion, significance claim or final-label result was inserted. C01 staged-hash and C02 failed-model-versus-corruption wording were synchronized as previously accepted clarifications.

The **title, every equation/align block, entire comparator section and entire audit section are unchanged**. All {verify['citation_keys_resolve']} distinct citation keys resolve to the unchanged bibliography; labels/references resolve in source. Source checks are not a substitute for compilation.

**Full manuscript is UNCOMPILED.** No pdflatex, bibtex, latexmk or tectonic was found on PATH, in bundled native tools or the checked standard installations. No toolchain was installed. The built-in standalone compiler does not support this multi-file project. Exact TeX/SVG/template edits, reproducible build commands and the distinct amended vector figure PDF are delivered; no amended full-manuscript PDF is claimed.

The figure's obsolete cap text blocks were removed, not hidden under a white overlay. Its new box reads “Fixed cap / 2,048 total / Report completion / Retain failures.” Rendering and pixel comparison show changes only in rectangle x564–756, y97–206; all outside pixels are identical. The changed box is legible. Existing crowding elsewhere is unchanged, and amended full-document pagination/line breaks remain unverified. See visual_verification.json and manuscript_provenance.json.

## Verification and failures

| Command/check actually performed | Result |
|---|---|
| p02c_establish.py | Exit 0; four artifacts, 598 files, commits, source snapshot, one acceptance event |
| p02c_adopt.py | Exit 0; approved scoped document/config adoption |
| p02c_manuscript.py using bundled Python | Exit 0; separate source/figure, unchanged equations/title/BibTeX; pypdf deprecation warning retained |
| pdftoppm original/revised figure at 96 DPI; visual/pixel check | Exit 0; changed cap box only. Historical-render font notices retained |
| p02c_verify.py, first check | Exit 1; caught incorrect new instruction-source filename. Corrected before packaging |
| p02c_verify.py, corrected check | Exit 0; preservation, contract consistency, original-version verification and production closed-dispatch guards pass |
| Additional exact-wrapper check | Initial raw-vs-canonical hash comparison failed; serializer inspection explained it. Exact text and both documented hashes now pass; no old hash changed |
| TeX/BibTeX compilation | NOT_RUN: unavailable toolchain, no installation |
| New tests / historical suite rerun | None added; suite not rerun because no executable contract changed. Existing 102-test result remains historical, not a new P02C test result |

Exact commands, failures/warnings and skips are in commands_and_limitations.json; verification_command.json preserves the failed check and verification_command_v2.json the successful correction. No skipped check is reported as passed. Current differences from the P02B index are limited to the documented active documents/state; the accepted ZIP itself and its hashes remain unchanged. Old execution/test source and raw evidence still match accepted hashes.

## Data and resource accounting

**Zero new model compute:** 0 answer generations, 0 model loads, 0 encoder forwards, 0 gate training, 0 final labels, 0 current GPU measurements. Offline reading, hash reconciliation, prose edits and figure rendering used CPU work only; CPU preparation time was not instrumented as GPU/model cost. No downloads, dependency/driver/backend upgrades, paid/cloud services or external uploads.

Historical totals were reconciled once from the corrected P01 ledger and P02A/P02B ledgers: **3 + 24 + 48 = 75 admitted generations; 567 + 11,298 + 28,690 = 40,555 output tokens**. P01's deliberate interruption remains a separate diagnostic; none of these observations becomes a final label or formal cap denominator. No outcomes were rescored or repaired. Historical totals JSON lists request identities and finish reasons.

Final local packet/evidence sizes and hashes are in P02C_packet_receipt.json. Backup status remains **local original/raw files + verified local ZIP only**, not an off-machine backup. The source snapshot makes ignored original manuscript bytes recoverable; it does not provide device-independent durability.

## Next development proposal and unresolved decisions

[next_development_proposal.md](../p02c/next_development_proposal.md) proposes, but does not authorize, four fresh inputs/family, K=4 per mode: **24 input clusters, 192 answer calls, 393,216 reserved output tokens**, plus **50 pure same-checkpoint input forwards** (48 measured, 2 charged warm-ups; at most 102,400 input-token positions). Features precede answers under one fixed input-only recipe. No prompt change, gate fitting or P03 execution.

P02B's 2,048 mix gives a planning illustration of **136,808 generated tokens / 2.12 answer-worker hours**; one prior input/family is too little for a confident forecast. Proposed combined limits are **4 h residency, 5 h wall, 0.5 GiB evidence**, including a 15-minute feature-residency sublimit. A 2x answer-time scenario would exceed the ceiling and leave a truthful partial run. The proposal states conditional precision limits, cluster structure, denominator limitations, support-bound problems, an explicit hypothetical reference tariff (not actual fees/default), later simulation allocation questions and external-backup needs.

CR01 removes the requirement for the old 2,400-call formal cap stage. The 1,200/15,000-call suggestions, feature benchmark, future simulations and any larger run remain unapproved. Dataset final settings, features, K/n, timeout, scalar ledger/support, beta, alpha/b_min/delta_score and resource/backup decisions still require review. Low completion alone is no longer the stop rule; integrity, cost, denominator and informative-design requirements still block their relevant actions.

## Acceptance checklist

| Requirement | Status / evidence |
|---|---|
| P02B accepted snapshot/commits verified; acceptance not duplicated | PASS; acceptance_verification, event 012, later authority supplement |
| CR01 approval/adoption trace and limited scope | PASS; approved/adopted hashes, verbatim quote, distinct date/timestamp, event 013 |
| Active cap/authority references synchronized; history preserved | PASS; reference audit/scan, changed_artifacts, source diff and preserved snapshot |
| Strict method/scoring/audit/test constraints retained | PASS by source/hash/section comparison; no new empirical/statistical validation claimed |
| Manuscript source and cap box updated | PASS; exact diff and visual evidence |
| Full amended manuscript compiled | NOT_RUN, unavailable; exact sources and build instructions delivered |
| Next bounded tranche/cost/design/backup proposal | DELIVERED FOR REVIEW ONLY |
| No new live work; dispatch closed; P02 unsealed; P03 unstarted | PASS; historical totals, closed guards and event 014 |
| Local review ZIP/index/receipt | See verified receipt |

## Review package and stop

Review this completion, adopted CR01, next_development_proposal.md, reference audit, manuscript diff/source and verification receipts. P02C_review_packet.zip includes recoverable original/changed source and authority evidence, not weights, environments, secrets, the unrelated user image or private meetings. It is a local review packet only.

**P02C READY_FOR_REVIEW. Real dispatch disabled. P02 incomplete and unsealed. P03 unstarted.** CR01 approval is settled; the next review assesses faithful adoption and the proposed execution plan. No final study, candidate or deployment manifest and no P02 accepted seal were created.
'''
with (root/'reports/phases/P02C_completion.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
print('P02C READY_FOR_REVIEW; offline only; P02 unsealed; report and event 014 written.')
