# TaskCognition Protocol Source of Truth

**Status: active draft; not yet frozen for confirmatory execution.** No TaskCognition experiment, package-development study, audit, or test has been run.

This document and [`taskcognition.tex`](taskcognition.tex) are the only current implementation specifications for the TaskCognition paper. The TeX manuscript is the authoritative scientific description. This file records the governance rule needed to turn that description into an executable, preregistered protocol. [`FROZEN_MANIFEST_TEMPLATE.md`](FROZEN_MANIFEST_TEMPLATE.md) is the required pre-development schema. A dated `FROZEN` manifest copied from that template will replace this draft only after the required development stage has finished and before final train, tuning, certification, or test rollouts are generated.

## Scope that must not change without a new protocol

TaskCognition compares **exactly two fixed inference packages** on one frozen original Qwen3-8B checkpoint: a direct package and a bounded native-thinking package. It contains **exactly one input-only, pre-generation gate**. The deployed system makes exactly one answer call. A failed or missing deployment audit forces direct execution. The study does not claim that reasoning models generally degrade performance, that a visible rationale causally produces an error, or that the gate discovers a task’s intrinsic need for reasoning.

## Required manifest contents before execution

The frozen manifest must bind, by immutable hashes or explicit version identifiers, the model and tokenizer revisions; serving engine and version; precision and hardware; serialized prompts and chat templates; D/R mode controls; sampling parameters; output cap; stop/EOS behavior; native-think and outer-final parsers; suite adapters and scorers; feature extractor and encoder; gate architecture; initialization and training controls; family weights; split and latent-problem manifests; K; thresholds; alpha; common beta; denominator threshold; score noninferiority rule; audit confidence level; random-number streams; retry and timeout rules; cost schedule; direct fallback; and all analysis scripts. A mismatch must prevent learned deployment and trigger direct execution until a new independent audit is performed.

## Development-before-labeling rule

A disjoint development pool determines whether the two named inference packages are feasible. It verifies mode rendering, parser behavior, mode-by-family completion, package throughput, retry/timeout behavior, cost-accounting conventions, cap choice, and the final sample/replication allocation. It cannot contribute any rollout used to fit, tune, audit, or test the final system. If any frozen package component changes after development, every final rollout-derived label must be regenerated under the new package.

## Superseded supporting material

[`notes/TaskCognition_Evidence_Pack.md`](notes/TaskCognition_Evidence_Pack.md) remains preserved for literature traceability, but it is **not** an implementation specification. It conflicts with the current protocol by proposing a different title, per-query LCB/UCB routing, a utility-first/same-seed framing, a 256-token primary cap, different renderer allocation, and a train/calibration/test split that lacks the current separate tuning and held-out audit roles. No implementation may use it to define an estimator, gate, split, cap, or inference rule.

## Current next gate

Before any confirmatory rollout, the authors must complete the critique-driven manuscript revision, verify all citations and software facts from primary sources, run the separate development and feasibility study, select the audit’s precommitted numerical design values, and publish a dated frozen manifest. Until then, every design described in the paper remains prospective.
