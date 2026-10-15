# P02E completion — offline denominator and cost-design review

**P02E OFFLINE DESIGN READY_FOR_REVIEW**

## Scope and authority

Active prompt: archived `reports/p02e/provenance/P02E_offline_design_prompt.md`; user conveyed the P02D execution acceptance on 2026-10-15 America/Chicago. Actual workstation adoption: event 023 at 2026-10-15T20:40:22.410173+00:00; offline checkpoint closure: 2026-10-15T20:58:21.403185+00:00. Acceptance is recorded once, not a new seal of P02. Review SHA-256 `a332bdd5566d66cd800261771986de54632ac54cf24485253e9b7050f2fcb13f`.

Branch `codex/p02e-offline-design`. Task-only local evidence and packet commits are identified in `reports/p02e/source_commits.json` and the external packet receipt; the packet commit can be resolved with `git log -1 -- reports/p02e/P02E_review_packet.zip`. The supplied untracked originals in docs (review, coordinator ZIP, prompt) are preserved and excluded from task staging. No push, merge, remote query, upload, download or installation.

Original PDF SHA-256 `9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8`; approved CR01 adopted v1 SHA-256 `ec07c0133224fb10f535fc9ac4d0816d12fb10acc683c09043de717cc089c0b8`. Original Sections 3–8 and active CR01 manuscript sections were read; CR01 fixes 2,048 tokens and descriptive completion, not an eligibility threshold. No manuscript edits, new scientific conflicts resolved silently, or final manifest/freeze.

Bound P02D plan `c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365`; ZIP `8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9`; production report `9a5f6c7cf713941284b1c125570b3e174c641e685e01284b6bf86f0f95ff4dab`; accounting `0dda412d334389fc5278e8e05c48667a151120f67dbc6d7dfed06ebb4af0ef03`. All 8,997 indexed files matched accepted ZIP and current bytes before operational state changes. Analysis binds 7,837 source records and checks the 7,257-event chain. Packet building repeats historical verification with explicit current phase-state exception; old packet remains authoritative for that historical state.

## Delivered slice

The [offline design report](../p02e/offline_design_report.md) covers all 24 input clusters, four fixed diagnostic rules, analytical sample-size constraints and a non-overlapping collection-cost map. CSV/JSON files preserve full precision and 192 original score outcomes. The precomputed scenario declaration precedes all illustrative calculations; none of its tolerances/counts is adopted. Analysis imports neither a final audit path nor model libraries.

The [next-step proposal](../p02e/next_step_proposal.md) recommends a separately authorized **offline cost-boundary/calibration preflight**, before spending on more labels. Its concrete contingent diagnostic is **UNAPPROVED**: zero fresh inputs, 12 fixed existing inputs, K=1/mode, 24 answer calls, 26 feature forwards including two charged warm-ups, 49,152 maximum output tokens; 90-minute worker, 120-minute wall and 128-MiB operational ceilings. No dispatch plan/seeds/requests were materialized. New shared-within-query loading is only a lifecycle proposal requiring review, not an implemented optimization or a hard-support proof.

## Verification and exact commands

Commands below ran from the implementation root. `scripts/p01_command.py LOG COMMAND...` is the existing stdout/stderr/exit/wall logger used for preparation, analysis, tests, documents and reproduction. All commands are CPU-only.

| Command actually executed | Exit/status | Evidence and interpretation |
|---|---|---|
| `.venv/Scripts/python.exe scripts/p02e_prepare.py` | 0 | `prepare_command.json`; accepted hashes/8,997 members and source identities, archive and event 023 |
| `.venv/Scripts/python.exe scripts/p02e_analyze.py` | 0 | `analysis_command.json`, `analysis_run_receipt.json`; 3.4861601 s wall / 3.40625 s CPU, 7,837 bound records |
| `.venv/Scripts/python.exe -m unittest discover -s tests -p test_p02e_design.py -v` | 0; 8 pass | `focused_tests_command.json`; formulas, retained Z range, zero denominators/Kish, cluster contract/missingness, costs, totals, bindings |
| `.venv/Scripts/python.exe scripts/p02e_documents.py` | 0 | Initial `documents_command.json`; corrected draft render is separately tracked in `document_correction_receipt.json` and current `document_render_receipt.json` |
| `.venv/Scripts/python.exe scripts/p02e_reproduce.py` (initial system-temp path) | 1 | `reproduction_command.json`; sandbox temp ACL blocked before analysis; no empirical evidence touched |
| `.venv/Scripts/python.exe scripts/p02e_reproduce.py` (workspace-temp version) | 0 | `reproduction_workspace_command.json` / `reproduction_receipt.json`; all 17 deterministic analytical/document files match; 3.0788512 s wall / 3.0625 s CPU |
| `.venv/Scripts/python.exe scripts/p02e_finalize.py` | 0 on completion | Archive verification, append-only decision record, completion/state event; no runner calls |
| `.venv/Scripts/python.exe scripts/p02e_packet.py` | See external receipt; PASS required | Every indexed member verified after compression, accepted historical hashes rechecked, CPU/wall/bytes and commit IDs recorded |

Offline PDF extraction succeeded with bundled pypdf Python, but initial console printing exited 1 under cp1252; reading saved `provenance/reference_pdf_text.txt` with UTF-8 succeeded. A draft rerender also initially hit the sandbox system-temp ACL; workspace-local temporary files resolved it. A draft synchronization subtotal was corrected from a manual transcription to the exact JSON-derived 0.0067902000 seconds; the original render receipt and old/new draft hashes remain recorded. These are preparation/display failures, not model/evidence failures. No full regression suite, GPU smoke tests, model execution, final audit decision or full simulation was run; production sources did not change. No new tests were added merely to raise a count.

## Data, costs and findings

Only accepted DEVELOPMENT P02D rows were analyzed: six families, four inputs/family, K=4/mode, 192 retained outcomes. P02A/P02B moments are not pooled. P01's deliberate interruption stays a separate diagnostic. New scheduled/admitted/dispatched/model/feature/answer/gate-fit/final-label counts are all **zero**. No execution authorization was created or consumed again.

D perfect 30/96 versus R 64/96; strict FINAL 66/96 versus 64/96. Only 8/24 inputs show any D success. Eleven benefits positive, thirteen zero, none negative; all 24 harm targets zero. Binary observed scores provide no target-information advantage over factorized routing here; there are no harm-positive supervision examples. These facts do not establish true zero harm, gate superiority or population feasibility.

Positive-benefit selection has six nested D successes on two inputs, B=0.0625; always-R B=0.3125. These are outcome-informed descriptions. At n=24 the contract range term 0.3742341475 exceeds maximum observed B even before variance; no g can meet a positive denominator check on these rows. This is algebra, **not an audit, theorem validation, power calculation or a whole-study stop**. Repeats cannot erase the independent-cluster penalty. K-squared pairs and Kish concentration are not independent success counts.

Existing P02D collection reconciles 193 sessions, 129,371 output tokens, 11,560.2217413 conservative worker seconds and 12,836.8229112 execution-wall seconds. Separate components, unallocated residuals, round/mode tables, CPU reporting/packaging and unavailable timing are in the cost report. Worker-minus-load-minus-generation rises about 5.9 to 20.5 seconds; source shows repeated growing ledger/evidence scans, consistent with but not proving attribution. No new benchmark or optimization. Current warm feature timing is not complete gate cost; live features, CPU heads, startup and failures must be charged under a reviewed service policy.

P02E CPU/wall costs are instrumented in preparation/analysis/render/reproduction/package receipts; reading, editing and all interactive overhead are not comprehensively CPU-profiled. P02D costs are not charged again for this analysis. Package receipt gives local size, full hashes and exact indexed count. Local raw evidence/verified packets are preserved; external receipt means outside the ZIP **on this workstation**, not a verified remote backup. No new off-machine copy exists from this task.

## Decisions and limitations

| Item | Status | Consequence |
|---|---|---|
| P02D acceptance | Recorded once, event 023 | Completed DEVELOPMENT checkpoint; consumed authority stays closed |
| D08/D09 hardware service ledger/support | UNRESOLVED; conditional cold one-query proposal | A timeout, reservation, observed maximum or successful cleanup does not prove finite support; overflow cannot be clipped or excluded |
| D05/D16 gate/init/reference charges | UNRESOLVED | Preserve common beta formula; no beta from collection-worker means or free cached embeddings |
| D10/D11/D12 resource/n/K/risk/score margins | UNRESOLVED | Illustrations are not selected tolerances or allocations |
| D14/D17 theorem/simulation and durable backup | UNRESOLVED | Remain later reviewed work; P03 unstarted |

No scientific rule, norm, tariff, cost bound, feature freeze or resource spend was adopted. No strict scoring, native source, runner, cap, sampler, inputs or manuscript conclusions changed. The report logs historical authority discrepancies and the residency-boundary clarification without rewriting history. All three required primary comparisons remain intact.

## Acceptance checklist and review packet

- PASS: authority/archive/hash bindings and once-only acceptance — `acceptance_verification.json`, event 023.
- PASS: all clusters/rules and denominator algebra — `cluster_rows.*`, `diagnostic_rules.*`, `analytical_constraints.json`, declared scenarios and report.
- PASS: non-overlapping costs, round/mode trends and support limitations — `cost_reconciliation.json`, `cost_sessions.csv`, `cost_round_mode.csv`.
- PASS: exact unapproved next proposal and longer-study implications — `next_step_proposal.*`, `longer_study_resource_scenarios.csv`.
- PASS: focused checks and deterministic reproduction — test/command/receipt files.
- PASS required by packaging: all indexed files match review ZIP and local bytes; exact count/hash in external `P02E_packet_receipt.json`.
- NOT RUN by design: any model work, candidate gate, full regression, final audit, P03 simulation or final data collection.

Review order: this completion; `offline_design_report.md`; `next_step_proposal.md`; tables/source/test receipts; `P02E_review_packet.zip`, `P02E_evidence_index.json`, external `P02E_packet_receipt.json`. The packet references accepted old ZIPs by hash instead of recursively embedding them; original raw evidence is needed to rerun analysis. Source diff and source/evidence commit are included. No P02 accepted seal or final manifest is proposed.

## Stop statement

**Dispatch false; zero new model work; P02 incomplete/unsealed; P03 unstarted; study unfrozen.** Event 024 closes only P02E at READY_FOR_REVIEW. Another phase or any execution requires a separate coordinator handoff after review.
