# P01 decisions and limitations

Evidence kind: `development_observation`. No main-study design is frozen.

| ID | Decision / observation | Authority and evidence | Consequence |
|---|---|---|---|
| P01-01 | P00 SEALED after local preflight; P01 activated by new state event. | User-conveyed reviewed prompt, coordinator's explicitly limited report review, accepted seal and preflight JSON. | P00 proposed seal/report/index remain unchanged; P00 source/state verified against Git snapshot. |
| P01-02 | Native Windows, PyTorch 2.11.0+cu128, Transformers 4.57.6, original Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`. | Official wheel index, model API metadata, hash-pinned requirements; no alternate checkpoint. | One runtime and weight copy, no quantization or CPU offload. |
| P01-03 | Separate `.venv-inference` because torch requires setuptools<82 while P00 wheel builder pins 84.0.0. | Initial resolver conflict; final resolver/install report; inference setuptools 81.0.0. | P00 build/runtime environment kept usable. Executed TaskCognition 0.1.0; final corrected 0.1.1 installed in both environments. |
| P01-04 | Native BF16 and built-in SDPA MATH, no extensions. | Synchronized FP32/BF16 matmul and BF16 SDPA checks pass; architecture list includes sm_120; no warnings. | Same precision/attention for D/R. This is a smoke package decision, not the study freeze. |
| P01-05 | Pinned unchanged number_sorting generator/scorer, small local initializer/dependency closure. | Reasoning Gym commit `21e6d2a9a581b3e11aafe711abfd37402f8482d5`; source hashes/license; native hand-checks. | One family only. Native scorer is binary and has numeric tolerance 1; do not relabel it exact match. No P02 suite integration. |
| P01-06 | Pre-dispatch template-context assumption repaired. | Failed preparation expected R opening in prompt; actual official R prompt leaves opening to generation. Actual D renders a closed empty thinking block. | No calls had occurred. Prior draft package/request, failed log, old resource plan and source retained. New run identity ends `-v2`; no model output repaired. |
| P01-07 | Parser uses exact native delimiters, one FINAL pair, ASCII space/tab/CR/LF outside wrapper, nonempty stripped payload, native numeric-list grammar/scorer. | Offline adversarial tests and serialized requests. | Missing R close cannot expose thinking as final. Exactly one recognized terminal EOS is removed by token ID for parsing; raw IDs/text preserved. |
| P01-08 | Three admitted calls, 567 output tokens; no retries; J=0. | All dispatch/admission/terminal/resource events and global reconciliation. | Initial D wrapper failure retained at zero; R native score 1; separate deliberate R cancellation at two tokens retained at zero. Five authorized slots unused. |
| P01-09 | Controlled cancellation is cooperative at a token boundary in an isolated process. | Admission and first-token events precede cancel request; generate returns, CUDA sync completes, process exits; restart refuses replay without changing any run file. | Real interruption demonstrated; forced-kill branch and 120-second deadline expiration were not live-tested. Neither this check nor the configured deadline proves a hard service-time support bound. |
| P01-10 | D live valid-FINAL success remains unobserved. | Initial D emitted a bare list; strict parsing rejected it. Offline D valid/partial/wrong paths passed; R live success passed. | Report this limitation prominently. No follow-up reran the initial question or repaired its answer. The bounded plan used the initial pair plus one named interruption diagnostic and then stopped. Wrapper reliability needs future reviewed development attention before cap certification. |
| P01-11 | Correct unexercised unexpected-worker-exit handling before review. | Review found the supervisor could impute zero after a scoring/program exception left no terminal result. Version 0.1.1 charges observed resources then raises an integrity failure; explicit supervisor forced termination remains separately recorded. Four added offline tests exercise unexplained exit, corruption, orphan evidence and forced kill. | All three workers exited normally with complete results, so none are invalidated. Executed version 0.1.0 is preserved at `683e9a3f7c5c539a3bb5d8d959b98d4c9319721f`; original environment/source hashes and run remain immutable. No GPU rerun. |
| P01-12 | Stop P01 at READY_FOR_REVIEW with no next phase authorized. | Final source also requires IN_PROGRESS for real dispatch. | P01 is not sealed. P02 resource proposal is conditional only; D live valid-FINAL success is still an explicit limitation. |

C01-C03 remain resolved exactly as accepted. No final TRAIN/TUNE labels, fitting,
AUDIT/TEST outcomes, empirical-Bernstein audit, bootstrap execution, encoder, or gate
was used. The original renderer text is preserved inside the user message. The FINAL
wrapper instruction is in the same system message for both modes. D's native control
does not establish absence of latent reasoning.

## Official runtime sources

- [PyTorch local installation guidance](https://pytorch.org/get-started/locally/): stable prebuilt Windows/pip route. The webpage's selector text appeared stale, so exact wheel availability was checked in the official index.
- [Official CUDA 12.8 torch wheel index](https://download.pytorch.org/whl/cu128/torch/): selected the listed CPython 3.12 Windows 2.11.0+cu128 wheel; kernel checks, rather than driver text, established local execution.
- [Official Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B): native template switch and model usage. Original pinned template/config bytes are archived in this review packet.
- [Qwen Transformers guide](https://qwen.readthedocs.io/en/v3.0/inference/transformers.html): supported Transformers path. Primary D/R sampler remains the study's common .6/.95/20/0 settings.

Official metadata retrieval and installation needed sandbox network escalation, which
was approved. Initial unprivileged network attempts failed; an initial HEAD request
to the wheel host returned 403, then a one-byte Range request plus ZIP central-directory
inspection succeeded. No credentials or signed download redirect URLs are in the packet.
