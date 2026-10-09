# P02D execution request — pending review, dispatch disabled

Request a separate conveyed authorization for **one** run of the immutable plan identified in `plan_receipt.json`, after review of this preflight packet. This document grants no execution authority. P02C acceptance and CR01 approval are settled; P02 remains incomplete/unsealed and P03 unstarted.

## Exact scope

- 24 fresh native DEVELOPMENT questions: four per family, seeds `930261005 + 10000*f`, size four, indices 0–3. No outcome screening, replacement, truncation or difficulty change. All three tokenization paths pass: raw 22–214 tokens; D 161–353; R 157–349. No historical content/identity collision was found. Future splits must exclude these identities/content; no final partitions were invented.
- 50 sequential same-checkpoint input forwards in one isolated worker: two charged warm-ups, 24 measurements, 24 repeat measurements. The fixed schedule processes **6,597 actual input positions**, bounded by 102,400. One recipe: raw question tokens, post-final-RMSNorm width 4,096, float32 masked mean; nine defined cheap observables. Zero normalization fitting or feature search.
- Only after all 50 are validly recorded and the feature worker is safely stopped: four independent D and R draws per input, **192 answer slots / 393,216 reserved total output tokens**. All caps are 2,048; J=0, no replacements or autoregressive warm-up. Exact P02B instruction, native questions, frozen Qwen revision, tokenizer, BF16/Windows/SDPA MATH and effective sampler are unchanged. Fixed round-robin schedule alternates first mode by input-index/draw parity.

## Operational ceilings and stopping

| Resource | Combined ceiling | Feature sublimit |
|---|---:|---:|
| Conservative worker residency | 14,400 seconds (4 h) | 900 seconds (15 min) |
| Execution wall time | 18,000 seconds (5 h) | 1,200 seconds (20 min) |
| Additional raw/vector/report/packet evidence | 536,870,912 bytes (0.5 GiB) | Within total |
| Answer generation / feature-forward deadline | 120 seconds each | 120 seconds |

Reserve at least 300 seconds plus 2,048 output tokens before each answer. Feature startup reserves 300 seconds; later feature passes reserve 150 seconds including cleanup, within both cumulative envelopes. Finite loader/termination procedures and measured cleanup/overshoot are detailed in `docs/P02D_RUNNER_CONTRACT.md`. Known timeouts are distinct from software incidents. No resource measurement is clipped to a ceiling. These operational policies do **not** establish the final audit's mathematical cost support.

A partial/timed-out/invalid feature stage stops before answers. Later answer resource exhaustion yields partial evidence and achieved denominators. Unknown admission consumes a slot; a software/evidence error stops unscored; missing records are never fabricated zeros. No automatic restart/replay, prompt revision, easy-case replacement, outcome-based early success stop or tranche extension. Execution requires a separate hash-bound authorization record and phase state; neither exists now.

## Expected cost and uncertainty

P02B's 2,048-cap subset had only one input/family and two draws/mode: 24 calls, 17,101 generated tokens, 954.4397468 worker seconds. Scaling by eight gives an **illustrative 136,808 tokens and 7,635.5179744 seconds (2.12 h)** for answers. New questions may behave differently. A 1.5x timing scenario is 3.18 h; a 2x scenario is 4.24 h before feature work and would not complete inside the 4 h ceiling. Feature throughput remains completely unmeasured. The proposed feature sublimit is an operational allowance, not a prediction. New source verification/ledger overhead is included in actual execution wall/worker costs and could reduce completion.

P02B raw evidence scaled by four in call count is about 3.78 MB; a threefold allowance illustrates 11.34 MB before feature vectors, logs and packets. Fifty 4,096-dimensional float32 vectors have 819,200 numeric payload bytes if stored binary; this implementation uses JSON floats, whose larger actual storage is measured. The 0.5 GiB ceiling includes local packet duplication. No model/environment/source download or upgrade, paid service or external transfer is requested.

## Questions this diagnostic can answer

It can show failure and direct-perfect coverage across four inputs/family, within-input score variation at K=4, complete-cluster target pipeline behavior, and measured cold-load/warm-feature costs and repeat-vector stability for one feature recipe. Reports have 12 planned cells (16 draws each), 24 input clusters, and explicit missing/unexecuted/incident counts. Complete clusters use T_b/T_h, direct redraw, and partial declines at 0.10/0.25. Cross-pairs remain dependent within input.

It cannot establish routing superiority, final sample/repeat allocation, reliable population completion, an audit denominator, or a hardware support bound. At K=4, perfect-rate conditional SE can be 0.25 and benefit-mean SE up to about 0.354. Four inputs/family do not establish broad population coverage. No significance, gate training, final labels or P03 simulation is proposed.

## Decisions still open

Do not adopt the earlier hypothetical reference-dollar tariff. Scalar cost choice, beta, hard support bounds, initialization allocation, final feature freeze, final input eligibility/population, K/n, margins and audit-denominator adequacy remain review items. Research collection totals must remain separate from one-query cost: every routed query needs its own live feature forward plus CPU gate and selected answer; cached training vectors are not free deployment embeddings. Charging 50 passes per query would also be wrong. Initialization cannot be made free by assumption.

Local raw historical evidence and verified review packets are present. The user's reported P02C push is consistent with local remote-tracking ancestry; no remote fetch/restore was performed, so complete off-machine coverage of ignored/raw artifacts is unverified. This preflight imposes no external-drive purchase or transfer requirement. Durable backup and final-study capacity must be reviewed before irreplaceable final collection.

**Pending decision:** authorize this exact plan hash and ceilings, or specify a concrete correction for another offline revision. Until a subsequent execution prompt, real dispatch remains false and no slot/forward is authorized.
