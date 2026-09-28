# TaskCognition implementation handoff

Prepared 2026-09-28. Status: implementation plan; no experiments or results.

## Start here

1. Extract this bundle into a dedicated TaskCognition repository. If a repository already exists, merge the files deliberately; never overwrite existing instructions, code, or user changes without examining them.
2. Keep `AGENTS.md` at the repository root and the supplied `docs/` and `reference/` directories beside it.
3. Open Codex in that repository on the workstation that will run Qwen.
4. Send Codex the entire contents of [P00](docs/prompts/P00_bootstrap.md).
5. Send the coordinating research assistant Codex's summary and `reports/phases/P00_completion.md`, including its linked evidence and any unresolved decisions. Do not start P01 until the P00 review is accepted.

Only P00 is initially authorized. The later prompts are staged instructions, not permission to run the whole study. The coordinator may replace a later prompt after reviewing actual evidence.

## What this study tests

Whether directly learning continuous reasoning benefit and independent-draw direct-correct/reasoning-imperfect spoilage gives a better constrained deployment than equally resourced winner and factorized outcome routers. One frozen Qwen3-8B answer checkpoint; two fixed packages; one input-only gate; one admitted answer generation per deployed query.

The objective is to evaluate this claim honestly. A positive finding requires the prespecified evidence. Null, negative, underpowered, frequent-fallback, and infeasible outcomes must remain visible. Completing an implementation phase does not imply that the scientific claim passed.

## Reading map

| File | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Codex's non-negotiable operating instructions |
| [Protocol](docs/PROTOCOL_SOURCE_OF_TRUTH.md) | Paper equations, scope, and decision contracts |
| [Roadmap](docs/IMPLEMENTATION_ROADMAP.md) | Vertical phases, dependencies, and review gates |
| [Architecture](docs/ARCHITECTURE_AND_DATA.md) | CLI, state machine, schemas, provenance, and resumption |
| [Statistics](docs/STATISTICAL_CONTRACT.md) | Estimation, auditing, power, and final claim test |
| [Decisions](docs/DECISIONS_AND_GAPS.md) | Choices to resolve during development; no invented final values |
| [Evidence](docs/EVIDENCE_AND_MANUSCRIPT.md) | Required reports, claim ledger, and paper completion |
| [Sources](docs/SOURCE_REGISTER.md) | Authoritative PDF fingerprint and external references |
| [Review template](docs/templates/PHASE_COMPLETION_TEMPLATE.md) | Codex completion report |
| [Seal template](docs/templates/PHASE_SEAL_TEMPLATE.md) | Review acceptance and evidence hash record |
| [Change template](docs/templates/CHANGE_REQUEST_TEMPLATE.md) | Changes and their consequences for validity |

The PDF is included as `reference/TaskCognition_Revised_Verified.pdf`. It is the unchanged revised paper, renamed only for portability. Verify its SHA-256 against the source register.

## Roles

- User: research owner, phase progression, resource limits, and scientific redirections.
- Coordinating assistant: reviews reports, identifies corrections, recommends seals, and provides the next Codex prompt.
- Codex: implements and verifies only the active phase, reports evidence, and stops at the phase boundary.

No external services, Jev integration, paid inference, manuscript submission, or remote publication are authorized by this handoff. Local Qwen implementation proceeds in the appropriate phase. A phase's bounded run plan authorizes routine execution within that phase without repeated permission questions.

## What to send back after each phase

Send the completion report, changed-file summary, commit or patch identity, commands and outcomes, failed checks, decision requests, run manifest, and relevant compact JSON/CSV evidence. Large raw generations remain in the repository's artifact store, addressed by hashes. A narrative saying "all tests passed" alone cannot seal a research phase.

The original TeX and bibliography are not included. Their recovery is tracked; it does not block bootstrap. They are needed before editing the original manuscript in P09.
