---
title: Resume Plan
type: reference
status: current
owner: repository-maintainers
created_at: '2026-07-27'
updated_at: '2026-07-27'
review:
  due_at: '2026-08-10'
validity:
  due_at: '2027-07-27'
---

# Resume Plan

## Start here

Read, in order:

1. [`implementation-handoff.md`](implementation-handoff.md)
2. [`AUTONOMY_AND_CONNECTIONS.md`](AUTONOMY_AND_CONNECTIONS.md)
3. [`ARCHITECTURE.md`](ARCHITECTURE.md)
4. [`SCOPE_AND_NON_GOALS.md`](SCOPE_AND_NON_GOALS.md)

The existing deterministic simulation is proven prototype code. The next task is
not to add an LLM to the fixed chain; it is to establish the new domain contracts
and fake-provider draft slice.

## Proven state

- bounded customer request routing across configured departments
- Strategy, Analysis, and Execution role invocation
- correlation identity and bounded content
- terminal customer response
- CLI execution
- Cobalt Wren Native wrapper execution
- prior Ruff, mypy, pytest, and GitHub Actions success

Re-run all checks before relying on this historical state.

## Immediate implementation sequence

1. Define versioned domain contracts and ports for `WorkRequest`, `Goal`, Persona,
   permission, Connection, Tool Package, `ToolIntent`, Review, knowledge, evidence,
   execution, audit, and runtime profiles.
2. Add deterministic fake provider, Connection, Tool Package, policy, clock,
   cognition, and error fixtures.
3. Implement deterministic permission, prohibition, knowledge-context, Review,
   schema, idempotency, and execution gates.
4. Build the fake-provider Support draft workflow in LangGraph direct mode.
5. Add the local scenario runner, golden fixtures, contract tests, and the initial
   100–150-scenario evaluation harness structure.
6. Run the same compiled graph through Cobalt Wren's official LangGraph integration
   and measure whether Cobalt Wren should remain.
7. Add an application-owned LLM adapter and compare the agreed Qwen-family dense
   and MoE baselines.
8. Add the real Gmail draft Connection using the same contracts.
9. Add system-owned runtime-profile candidate generation for explicit developer
   invocation and CI only.

## Do not do first

- do not connect a live LLM before deterministic safety paths are testable
- do not make Cobalt Wren or LangGraph types domain contracts
- do not implement provider-specific branches in central orchestration
- do not build public Tool Package distribution or universal documentation
  ingestion
- do not weaken safety gates to meet quality or latency targets
- do not allow optimizer-generated policy to grant its own production authority

## First decisions still required

- exact Qwen model identifiers
- serving engine and hardware/endpoint assumptions
- concrete customer inquiry and Knowledge fixture
- expected Gmail draft and planned Review defect

These do not block schema and fake-infrastructure work, but they must be recorded
before model benchmarking or the real Gmail scenario.

## Validation before each handoff

- run repository tests, type checks, lint, and any docs checks
- inspect `git diff --check`
- verify generated work-knowledge `index.md` and `log.md` metadata
- ensure docs contain no unresolved contradiction with `implementation-handoff.md`
- commit every confirmed decision
- push `main`
- report any monitor-generated follow-up commit explicitly
