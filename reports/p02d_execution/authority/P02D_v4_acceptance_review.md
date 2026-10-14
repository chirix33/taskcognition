# P02D v4 corrected preflight — coordinator acceptance

Date: 2026-10-09 (America/Chicago).

**Decision: accept the corrected P02D preflight. R1 and R2 are resolved sufficiently for the proposed bounded development run to be submitted for user execution approval.** This review itself does not authorize live work. Dispatch remains false until that separate approval is conveyed and bound to the reviewed v4 plan. P02 remains incomplete/unsealed; P03 is unstarted.

## Evidence reviewed and independently verified

| Artifact/check | Result |
|---|---|
| Corrected review ZIP | Matches external receipt |
| Index | Hash matches receipt; all 661 indexed files match |
| Separately attached report and execution request | Match receipt hashes |
| Active v4 run plan | Hash matches receipt |
| Materialized experiment records | All 256 non-plan records byte-identical to previously reviewed v2 |
| R1 implementation | P02D-only prepared/fsynced/closed temporary file, then atomic no-overwrite hard-link publication; historical shared writer unchanged |
| R2 implementation | Clean operational stops retain costs and consumed slots and report STOPPED_INCOMPLETE; corruption/unsafe cleanup remain dominant integrity failures |
| Supplied full Windows test log | Reports 138 passing tests, including 15 correction checks |
| Independent focused verification here | All 15 supplied correction checks pass with the test-scaffolding qualification below |
| New model work by coordinator | Zero |

Reviewed identities:

```text
Plan v4:
c46977bfc0de1040965f08df8acbd55b9b063b386ccfb97f247a280ae2472365
Corrected ZIP:
1f3c8f0bc16d04416052550d21449665197325a0b3d8096e97d32ae3a9db6950
Index:
ffbac753187f4ad21555c1506efb2af7611cce22f66635adbd116358ff8ad8dd
Completion:
38fea2199a540f136c12fabcace93ab8572bc1f42cac6abd71ac4894f4c0fe08
Execution request:
0d688444a8c584b2c811f163e6ad0be0380e287d5fdb0b1b3d28ff5610e291f0
Source commit:
b5c6abd5edf6e1d8032d68567dd2f8e9c23bd7a4
```

The source and submitted test evidence resolve the two previously reproduced defects. Independent checks cover real concurrent file publication and ledger-prefix reads, duplicate publication, interrupted preparation, malformed committed records, safe resource/forward/loader stops, integrity-error precedence, orphan-stop recovery, dispatch closure and parent/child rejection before model imports. Old v2/v3 prospective plans are rejected.

Independent test qualification: this coordinator environment does not reproduce the pinned Windows inference installation and has no system torch. I ran the supplied 15 correction tests using their unchanged Clock/FakeWorker class definitions and a small harness that reads the submitted immutable plan instead of invoking the environment-dependent plan builder. Production functions were not replaced by this harness. The supplied tests retain their own intentional mocks for fake workers/clocks and authorization scenarios. This is independent Linux/offline evidence, not an independent rerun of all 138 Windows tests or of live model behavior. The harness and receipt are in `P02D_v4_coordinator_checks.zip`.

The 2,530 runtime bindings must still be verified by the production runner on the workstation. No GPU performance, final cost support, gate accuracy or audit feasibility is established by preflight.

## Minor documentation correction, not an execution blocker

One sentence in the corrected completion says the next request is “now bound to v3.” The active code, plan, request heading and receipt identify **v4**, with the hash above. Record an append-only erratum stating that this sentence should say v4. Do not rewrite the historical completion/ZIP or modify any plan-bound file just to fix this report typo.

The corrected no-push provenance is now explicit. No new remote query or transfer is needed.

## Concrete run recommended for user approval

One invocation of the existing v4 runner, with no code or experimental changes:

- 24 fresh DEVELOPMENT inputs, four per family.
- First, 50 same-checkpoint feature forwards: two charged warm-ups and 48 measurements. If that stage is incomplete or invalid, stop before answers.
- Then, at most 192 answer dispatch slots: four independent D and four independent R draws per input, 2,048 total generated tokens per call, no retries/replacements. Maximum output reservation: 393,216 tokens.
- Combined operational ceilings: four hours worker residency, five hours execution wall time, 0.5 GiB additional execution evidence. Feature sublimits remain 15 minutes residency and 20 minutes wall time; generation/forward deadlines remain 120 seconds.
- Preserve actual costs, failures, overshoot and partial execution. No automatic restart, slot replacement, larger run, gate training, P03 simulation or final labels.

The earlier approximately 2.12-hour answer forecast is illustrative, based on a tiny prior sample; total time may differ and the run may stop partially. The time limits govern admission and stopping, not a proved hard mathematical bound on service time.

The run asks whether the broader small development sample provides usable direct-success/target-variation evidence and what the single proposed feature recipe costs. It does not prove the paper's central superiority claim. Scalar cost choice/support, beta, final allocation and later audit design remain unresolved.

## Handoff

`P02D_v4_execution_prompt_PENDING_APPROVAL.md` is prepared for use **only after the user explicitly approves the bounded run above**. Once approval is conveyed, Codex can record this preflight acceptance and the separate execution authorization, validate the exact hash/environment, run once, close dispatch and return the execution review packet. No extra approval of CR01 is required.
