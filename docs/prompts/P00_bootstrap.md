# P00 prompt: bootstrap and protect the study

Implement P00 only for TaskCognition. Read root `AGENTS.md`, `README.md`, the supplied protocol, decision register, architecture, statistics, and roadmap. Read `reference/TaskCognition_Revised_Verified.pdf`; verify the source hash. This is the revised two-package Qwen3-8B routing study. The objective is to test the claim fairly, including null/infeasible outcomes.

The user has a workstation and wants phase-by-phase implementation. Do not start P01 or run any real model generation/training in P00.

## Work

1. Inspect the repository and preserve all existing instructions and dirty work. If these handoff files have not yet been merged, integrate them without destructive replacement. Record conflicts; do not silently replace scientific rules. Use a task branch where possible.
2. Inventory OS, shell, Python, available GPU(s)/VRAM, driver/runtime compatibility, RAM, free disk, existing Qwen files/cache, and relevant repository tooling. Report useful capacities, not secrets. Do not modify system drivers or assume a particular OS.
3. Locate original TeX/BibTeX and any existing protocol within the task repository. Record present/absent and conflicts. The supplied PDF is sufficient to bootstrap; missing original manuscript source is tracked for later.
4. Build a minimal installable Python package with a stage-aware CLI, typed manifest/input/draw/aggregate records, explicit evidence kinds, stable hashes, a phase state file, and isolated fixture/development/final directories. Project-local lightweight dependencies are allowed; no model downloads or paid calls.
5. Implement an OFFLINE fixture vertical slice: synthetic D/R draw records -> native-score/perfect-correctness aggregates -> machine-readable report. Include the K=4 analytical example from the statistical contract. Label every output `fixture`; do not put fixture metrics into manuscript result tables.
6. Define and test guards: final collection rejects missing freeze; train readers reject held-out splits; feature records reject prohibited outcome/family metadata; duplicate draw IDs are rejected. Provide an explicit no-generation `doctor` command and an artifact verification command.
7. Create `reports/decision_ledger.md`, `reports/phases/P00_completion.md`, and a proposed P00 seal. Identify P01-compatible backend options from actual hardware and the smallest real smoke-run plan. Leave final statistical values unresolved.

## Exit criteria

- Source hash matches and current project scope is explicit.
- Hardware/repository facts are measured; missing original TeX is honestly recorded.
- Package installs locally; offline fixture pipeline runs; analytical aggregates match.
- Evidence isolation, duplicate records, split boundaries, and freeze guards have meaningful tests.
- No model calls, GPU training, audit/test exposure, paid work, or later-phase implementation.
- Completion report provides commands, outputs, changed files, failures, and P01 resource proposal.

Commit only task-owned changes if the repository supports it and identity is configured; otherwise provide a patch. Do not push or merge. Use the phase completion template. Finish as READY_FOR_REVIEW or BLOCKED and stop. Send a concise summary plus exact paths of the report and proposed seal. Do not claim P00 is sealed.
