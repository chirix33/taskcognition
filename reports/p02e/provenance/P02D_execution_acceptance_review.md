# P02D execution: coordinator review

**Decision: ACCEPTED as completed DEVELOPMENT evidence.** No blocking discrepancy was found in the supplied execution packet. This accepts the bounded P02D execution checkpoint; **P02 remains incomplete and unsealed, P03 remains unstarted, and live dispatch stays disabled.** The single-run authorization has been consumed. This review does not approve another invocation, gate training, a scientific freeze, or final labels.

Reviewed run: 2026-10-14 UTC. Local evidence commit reported by Codex: `de45085992a23a3731ea267388a84349344f4ca1`; subsequent packet commit reported: `32897ff`. Those are archived provenance, not independently queried Git history.

## What was independently checked

- Execution ZIP SHA-256: `8b487fdbd321e997683e014a86caedf9bd006323544f03972e65d06239c8faa9`.
- All **8,997 indexed files** matched their recorded hashes. The production report reproduced exactly using hash-matched archived implementation dependencies.
- All **192 saved token sequences** decoded to their recorded text using the pinned tokenizer vocabulary. All **192 strict parser/native scorer results** reproduced; all **24 regenerated native entries** matched their recorded hashes. Supervisor and worker copies of each answer agreed.
- The **7,257-event ledger** formed a complete hash chain: 242 dispatches, admissions and results; 193 session starts and ends. All feature results and the feature worker's safe stop preceded the first answer dispatch.
- All 24 clusters contained four D and four R draws, with **192 distinct recorded seeds/streams**. Benefit, independent-draw spoilage, direct-redraw and partial-decline targets reconciled.
- Session resources summed to **11,560.2217413 seconds (3.21 hours)**. Reported execution wall time was **12,836.8229112 seconds (3.57 hours)**. Generated-token counts summed to **129,371**. All sessions recorded safe stops, exit zero and no integrity incidents.

These were offline checks, with zero model loads, forwards or generations and no Torch/Transformers import. They do not independently reproduce Windows/GPU execution, verify the workstation's installed runtime or model weights, or establish statistical independence from unique seeds alone. Native scoring used the pinned source; the coordinator's local NumPy version need not match the workstation's. Recorded process status is historical workstation evidence, not a live inspection.

## What the observations say

Each family/mode has 16 retained draws; all failure scores remain included.

| Family | D perfect | R perfect | D strict FINAL | R strict FINAL |
|---|---:|---:|---:|---:|
| number_sorting | 4 | 16 | 4 | 16 |
| number_format | 16 | 16 | 16 | 16 |
| letter_counting | 3 | 14 | 16 | 14 |
| graph_color | 0 | 6 | 0 | 6 |
| shortest_path | 0 | 0 | 14 | 0 |
| knights_knaves | 7 | 12 | 16 | 12 |
| Total, out of 96 per mode | **30** | **64** | **66** | **64** |

The equal-family mean primary scores are **0.3125 for D** and **0.6666667 for R**. All observed native scores are binary; the scoring contract still permits partial credit. There are 28 D outputs missing both FINAL tags and 34 capped outputs without a valid final answer (2 D, 32 R). Failure categories may overlap; they are not additive exclusions.

This shows observed benefit from the bounded R package on some DEVELOPMENT inputs. It does not establish that TaskCognition beats the winner or factorized routers. Formatting and truncation are part of these package-relative outcomes under CR01.

## Why the next checkpoint should be offline

### 1. Exposure is concentrated, and harm supervision is uninformative in this tranche

All **24 empirical joint-spoilage targets are zero**. Direct mode has a perfect draw on only **8/24 inputs**, while 16/30 direct successes come from number_format. The harm head has no positive target in this tranche. Zero estimated spoilage does not establish zero population risk, especially with K=4.

An outcome-informed diagnostic makes the denominator issue clearer. Selecting the **11 inputs with observed benefit greater than zero** retains only **six direct successes across two input clusters**. With equal family weights, its empirical exposure is:

`mean(g * p_hat_D) = (0.75 + 0.75) / 24 = 0.0625`.

Always reasoning would have empirical exposure 0.3125. Much of that exposure lies on observed benefit ties. This creates a practical tension between selecting useful reasoning and obtaining enough direct-perfect exposure for the safety audit. The diagnostic is an empirical oracle selection, not a learned gate, a cost-feasible deployment, or a population bound. Do not route otherwise unnecessary ties merely to manufacture audit exposure; analyze the declared objective and constraints faithfully.

Under the current statistical contract, the range-only term for B or Z at n=24 is `7*log(40)/(3*23) = 0.3742341`. It exceeds even the maximum empirical B=0.3125 available by routing all these inputs. Consequently these particular development rows cannot satisfy the specified positive-denominator lower-bound check for any action vector. **This is an algebraic diagnostic, not an AUDIT run or a conclusion that a larger study is infeasible.** More repeats do not turn 24 clusters into a larger n.

The current data also do not demonstrate the need for continuous-benefit/harm supervision over the required baselines: all harm targets are zero and all benefits are nonnegative. Preserve the comparison; do not assume the two-head method will win.

### 2. Collection time is not yet a frozen deployment cost

The 50 feature passes include two warm-ups and 48 measurements. The mean measured warm forward is approximately **0.05369 seconds**, while the feature session as a whole cost **52.86433 seconds**. Neither number alone is the all-in cost of a future routed query.

Average answer-worker residency is **34.59010 seconds for D** and **85.27821 seconds for R**. These isolated workers include loading, verification, IPC, scoring and other collection work. They are useful research-cost measurements, not automatically appropriate deployment reference costs. Across draw rounds, mean worker residency minus logged loading and generation rose from approximately **5.9 seconds to 20.5 seconds**. This is an observed residual, not a separately instrumented component or a proven causal attribution. The collection code repeatedly scans/verifies growing evidence; an offline review should determine what can and cannot be attributed from existing records.

Execution wall time exceeds summed worker residency by **1,276.60117 seconds**. Load and generation durations are nested within worker residency; wrapper wall overlaps execution wall. Do not double count them or silently discard overhead. A shared/persistent deployment process, initialization allocation, gate-head cost and enforceable scalar cost bounds remain unresolved.

## Authorized next step

Proceed to **P02E OFFLINE DENOMINATOR/COST-DESIGN REVIEW** using the companion prompt. This permits analysis of accepted DEVELOPMENT evidence, analytical design calculations and a concrete recommendation. It permits no model work, gate fitting, full-pipeline simulation, final-label collection or P03 activation.

Codex should return the reconciled exposure/cost analysis and a bounded proposal that makes the next decision reviewable. Completion rates alone must not restore CR01's removed eligibility stop. If the declared study cannot be made informative within realistic resources, document that honestly; do not change the benchmark, scoring, audit margins or comparators to rescue the claim.
