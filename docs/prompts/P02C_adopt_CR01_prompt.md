# P02C: adopt approved CR01 and synchronize the study

The user approved CR01 on **2026-10-05** with: **“Understood. I approve it”**. Read `TaskCognition_CR01_APPROVED.md` and apply it now. Do not request approval again for the same amendment.

This is the next offline vertical slice within P02: a coherent revised specification, any necessary validation changes, an updated manuscript and a concrete next-run proposal. It does not authorize live model work or complete/seal P02.

## 1. Establish current state without repeating completed work

Read the root AGENTS.md, current phase state, decision ledger, governing protocol/statistical contracts, CR01 draft/approval and P02B review. Inspect git status and preserve unrelated staged/untracked work. Use a dedicated task branch or continue the appropriate task branch with task-only commits; no push, merge, destructive cleanup or history rewrite.

If the P02B offline acceptance prompt was already completed, verify/reuse that acceptance and do not create duplicate acceptance events. Otherwise, record the coordinator's P02B acceptance now, after verifying these accepted artifacts against their preserved snapshot:

| Artifact | SHA-256 |
|---|---|
| P02B_completion.md | `75e858192c9a0f4ec863e51ffb3f0a4d37b0af3e2f229a1265c53ecc5a6b2534` |
| reports/p02b/P02B_evidence_index.json | `f92a2903b0d44649ac9670e2108d8ef8092dbe5f4d516f57ea1954c2be174ddf` |
| P02B_review_packet.zip | `a66ae570dcd7c470fda399bd858bc19100d750db8c388951b977a6a138be314b` |
| P02B_packet_receipt.json | `44c8ae0433c23f7f26eb2cae87f447d0e536bee40d410b5e6a7f5baa690802cd` |

Verify the 598 indexed files against the accepted ZIP, allowing later documented current-state changes without rewriting historical hashes. Identify pre-dispatch commit `72d88843067b8a8f0f29d2937587a102d5a24f6b`, evidence commit `ba3ef09dd8db95a1e60a380723f398f99e5d52d4` and the packet commit. Stop on an unexplained discrepancy rather than regenerating evidence.

Record the CR01 approval verbatim, approval date, adopted amendment hash and affected artifacts in the change/decision ledger. Record the actual adoption time separately from the user's approval date. P01 remains sealed; P02A/P02B are accepted development checkpoints. Activate offline P02C with real dispatch false. CR01 resolves the pending scientific-choice block; it does not resolve the remaining cost/design/resource questions.

## 2. Apply the amendment consistently

The approved change is precise: **primary D/R cap = 2,048 total generated tokens; completion is descriptive, with no 99% eligibility prerequisite or automatic stop based on that threshold.** Strict parsing/scoring, all retained failures, all audit checks and all primary comparisons continue unchanged.

Preserve the original reference PDF (SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`) and the original manuscript/source snapshot. Do not replace them with a newly hashed file under the same historical identity.

Create a dated, versioned amendment record referencing the original PDF and the approved CR01. Synchronize active documents where applicable:

- AGENTS.md scope rule for cap selection and the old automatic infeasibility stop.
- PROTOCOL_SOURCE_OF_TRUTH, DECISIONS_AND_GAPS, IMPLEMENTATION_ROADMAP, architecture/data and evidence/manuscript guidance.
- Active future P02/P03/P04 prompts, applicable templates, configuration schemas and validation rules that currently require cap certification or the old selection branch.
- Relevant README/navigation and authority statements so users and runners can identify the active revised specification.

Search active source/documentation for `99`, `0.99`, `1024`, `1,024`, cap-feasibility/certification and stop-rule references; inspect matches in context. Do not perform blanket replacements. Historical prompts, immutable runs, regression fixtures and reports legitimately retain the old values. Preserve them and label/link their historical scope. Produce a short reference audit listing changed active references and intentionally retained historical ones.

Where existing validators encode the old scientific rule, update them narrowly for the explicitly versioned CR01 configuration. Historical validation must remain possible. Do not globally reject a historical 1,024 artifact or silently reinterpret it as CR01. New prospective primary CR01 configurations must use 2,048; low completion alone cannot be an active eligibility rejection. Missing required freeze fields, invalid scores/costs, insufficient denominator bounds and software/evidence integrity errors must still block the relevant action.

Do not create a final study/candidate/deployment manifest or mark the package scientifically frozen. Dataset settings, features, budgets, repeat counts and final cost bounds still require development and design review. Keep the P02B instruction, checkpoint, sampler and parsing behavior unchanged.

## 3. Update the manuscript without claiming new findings

Locate the active TeX/BibTeX under the task repository (previously `docs/iclr2027`). Preserve a recoverable source snapshot before editing. Respect unrelated changes and local instructions; use a separate revision copy if that is the established manuscript workflow. Do not silently edit only an obsolete draft.

Update Section 5 and Figure 1's cap-selection box, plus any other affected active statements, to describe the fixed 2,048-token contract. Add a concise development-history disclosure: P02A/P02B revealed format/truncation problems; the user adopted CR01 before any final labels. Explain that completion is now reported and failures stay in the score distribution.

Ensure the claim/limitations concern the specified bounded answer packages, including format compliance and truncation. Do not present improved native task solving as established, insert a gate result, or imply that P02B formally rejected the old cap rule. Preserve the method, baselines, audit inequalities and test success criteria. Do not lower tolerances/margins or revise the title merely because this amendment exists.

Compile with the existing local toolchain if available and inspect the changed text/figure for consistency. Save a distinct amended PDF with provenance. If compilation is unavailable, deliver exact TeX/figure edits and a clear uncompiled status; no large toolchain installation is authorized or necessary for this slice. The historical reference PDF remains unchanged.

## 4. Verify only the affected risks

If executable contract validation changes, add focused offline checks showing: a prospective CR01 primary cap of 2,048 is accepted; unsupported prospective caps are rejected; poor completion is reported without the removed eligibility stop; strict score/failure/integrity rules persist; and old evidence remains verifiable under its original version. Exercise production validation rather than a parallel toy rule. Run the relevant existing suite if shared code changes require it.

If the work is documentation/configuration-only with no executable change, use consistency and artifact-hash checks; do not manufacture tests merely to increase the count. Do not rerun historical generations. Report exact commands and results, including any skipped compile or verification.

Verify preserved P02B evidence and original reference hashes. Historical totals remain **75 admitted generations / 40,555 output tokens** across P01/P02A/P02B. Keep P01's deliberate interruption labelled as a separate diagnostic. No current GPU measurement or new empirical result is claimed.

## 5. Prepare the next bounded development proposal

Produce one concrete proposal under CR01, to be reviewed before live dispatch. Resolve the sequencing of:

1. Fresh multi-input repeated D/R observations at the fixed cap to estimate target variation, failures and direct-perfect denominator adequacy. Specify inputs/family, repeats/mode, independent streams, exact call/token totals and useful precision limits. Do not reuse historical diagnostics as final labels or mistake many repeats on one input for broad input coverage.
2. Same-checkpoint input-only feature extraction and its live cost. Specify candidate layer/pooling/tokenization, cheap features, forward/warm-up counts and costs. No separate encoder checkpoint or free cached deployment embeddings.
3. A single cost ledger with credible support bounds, including gate/feature/selected-answer work. Distinguish measured residency from a hard bound. Present any reference-tariff option as a proposal with explicit rates/count bounds, not an actual fee or an approved default.
4. Remaining P03 simulation inputs, sample/repeat allocation, resource ceilings and durable backup needs.

Choose a modest next tranche from measured P02B throughput and show token/residency/storage estimates with uncertainty. State exactly what the tranche would resolve and what remains uncertain. The earlier 2,400-call cap study is no longer a required CR01 stage; the 1,200/15,000-call pilot suggestions and encoder benchmark remain unapproved proposals. This prompt does not activate them.

## 6. Return package and stop

Return:

- `reports/phases/P02C_completion.md` with approval/adoption trace, changes, validation, limitations and zero-new-compute statement.
- The adopted CR01 record, active revised specifications, exact source/manuscript diff, authority/reference audit, and amended manuscript PDF if compiled.
- `reports/p02c/next_development_proposal.md` with concrete counts, ceilings and unresolved decisions.
- A compact `P02C_review_packet.zip`, hash index and receipt; include recoverable changed source and evidence needed for review, excluding weights/environments/secrets/unrelated private material.

Finish **P02C READY_FOR_REVIEW** or **BLOCKED** on a concrete implementation issue. Keep real dispatch disabled, P02 incomplete/unsealed, and P03 unstarted. CR01 approval is already settled; this review checks its faithful adoption and the next execution plan. No additional confirmation is needed to perform the offline work above.
