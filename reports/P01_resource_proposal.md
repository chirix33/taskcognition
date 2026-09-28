# Conditional P01 resource proposal (not authorization)

Evidence kind: `development_observation` for measured inventory; the run plan below is unexecuted.

The local inventory reports Windows 11 build 26200, PowerShell 7.6.5, Python 3.12.14,
Intel Core Ultra 9 285K (24 logical CPUs), 63.46 GiB usable physical RAM (42.38 GiB free
at inspection), RTX 5090 with 32,607 MiB VRAM (30,553 MiB free), driver 610.60 and
compute capability 12.0. Free workspace disk is 1,806,095,446,016 bytes (~1.64 TiB).
`nvidia-smi` also reported CUDA UMD 13.3; this describes the installed driver, not a
verified installed CUDA toolkit or working PyTorch runtime. `nvcc` is absent on PATH.
Torch, Transformers, Accelerate and Hugging Face Hub are absent from the project venv.
No Qwen directory was found in the default/configured HF hub or task-local model/cache
locations. This bounded search is not a whole-disk claim.

## Backend options

1. **Preferred candidate:** native Windows, a Blackwell-compatible CUDA PyTorch wheel,
   Transformers `AutoTokenizer` / `AutoModelForCausalLM`, eager execution, one request at
   a time, original `Qwen/Qwen3-8B` weights, explicit BF16 if validated. Qwen documents
   Transformers support and native `enable_thinking` control in `apply_chat_template`.
   Pin exact versions and checkpoint/tokenizer commit in P01 after verifying their
   compatibility; do not treat a minimum version as the dependency lock.
2. **Conditional local diagnostic:** the same checkpoint and Transformers path with CPU
   execution if GPU compatibility fails. FP32 weights alone are approximately 33 GB
   for 8.2B parameters; memory overhead and loading peaks remain unmeasured. This is
   likely slower and needs a separately bounded plan. Do not silently switch precision,
   quantize, change the checkpoint, or install another OS/serving stack.

For BF16, 8.2B parameters imply about 16.4 GB (15.3 GiB) of weight storage before cache,
activations, allocator, and loading overhead. The measured VRAM makes a short,
single-request trial plausible; it does not prove fit. A GPU load/kernel check is
required. The PyTorch Blackwell release notes document CUDA 12.8 support but do not
alone verify the Windows wheel to be chosen here. Consult current Windows wheel
availability in P01. No CUDA kernel, model load, BF16 check, or throughput measurement
was run in P00.

Primary references checked read-only during P00:

- [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B): native thinking switch and direct `generate` example.
- [Qwen Transformers guide](https://qwen.readthedocs.io/en/v3.0/inference/transformers.html): Transformers support; installed versions must be pinned rather than copied as unbounded requirements.
- [PyTorch 2.7 release notes](https://pytorch.org/blog/pytorch-2-7/): Blackwell/CUDA 12.8 support. This is background, not a request to install that historical version.

## Smallest real smoke run to propose after P00 acceptance

- One fixed DEVELOPMENT input, same exact text for both modes, D then R, one draw each:
  **2 admitted generations maximum**, no automatic retries (`J=0`). This is interface
  smoke evidence only, not a K>=2 estimation study or six-family cap pilot.
- Pin original model/tokenizer immutable revision, exact wheel versions, precision,
  template, serialized inputs and all effective sampler parameters before dispatch.
  Use native `enable_thinking=False/True`, matched sampling (0.6, 0.95, 20, 0), and
  1,024 maximum generated tokens including thinking. Maximum smoke output: **2,048
  tokens total**, each input at most **256 tokens**. This does not select the final cap.
- Save dispatch intent first; retain raw generated IDs/text, serialized mode controls,
  finish reason, timing, VRAM and parser outcomes. A failure is retained; no rescue or
  automatic regeneration. Unknown admission blocks repeat. Offline adversarial parser
  and interruption tests accompany P01; extra live interruption attempts require an
  explicit count in its plan.
- Proposed ceiling: 20 minutes for the two requests after loading, at most 10 minutes
  per request. These are operational stop triggers, **not a proven service-time support
  bound**. Confirm cancellation and admission reconciliation before any restart. Stop
  on OOM/incompatibility and report; no silent alternate backend.
- Reserve **40 GiB disk** for one original weight snapshot plus dependencies/temporary
  files, and **100 MiB** for tiny smoke logs. These are allowances, not measured download
  sizes. Allow up to 30 minutes loading/compatibility work after download; download time
  remains bandwidth-dependent. No throughput estimate or substantial pilot is justified
  until P01 measures it. No cloud or paid fallback.

This document does not activate P01. P00 review acceptance and an explicit next-phase
prompt are required. Final K, n, split sizes, alpha, b_min, delta_score, beta, hard cost
bounds, and total-study budgets remain unresolved.
