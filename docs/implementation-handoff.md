---
title: Implementation Handoff
type: guide
status: current
owner: repository-maintainers
created_at: '2026-07-27'
updated_at: '2026-07-27'
review:
  due_at: '2026-08-10'
validity:
  due_at: '2027-07-27'
---

# Implementation Handoff

## Purpose

This document is the primary handoff for continuing work in another chat or by
another developer. It summarizes the repository's proven state, all material
requirements agreed during the design interview, the current architecture
decisions, implementation priorities, evaluation gates, unresolved questions,
and the working preferences that shaped those decisions.

When this document conflicts with older prototype-oriented wording elsewhere,
use the newer explicit decisions in this document and
[`AUTONOMY_AND_CONNECTIONS.md`](AUTONOMY_AND_CONNECTIONS.md), then update the
older document rather than silently guessing.

## Current position

The repository currently contains a deterministic company-simulation prototype.
It has not yet implemented the new autonomy, permission, Connection, Review,
organizational-memory, dynamic Tool Package, LangGraph, Qwen, or runtime-profile
optimization requirements.

The proven prototype:

- models departments as stable Personas with Strategy, Analysis, and Execution
  internal roles
- passes a customer request through bounded department handoffs
- preserves correlation identity and bounded transcript content
- produces a customer-facing completion
- exposes CLI and Cobalt Wren Native execution paths
- previously passed Ruff, mypy, pytest, and GitHub Actions

The next work is a new production-shaped vertical slice, not an incremental
extension of the existing fixed department chain.

No product implementation should begin from assumptions not captured in these
docs. Add or revise contracts explicitly when new evidence requires a change.

## Product direction

The target is a Company system composed of autonomous but permission-constrained
Personas. A Persona can reason, collaborate, access organizational knowledge,
and operate external services only through explicit, typed, observable,
least-privileged contracts.

The design must remain reliable with an approximately 30B-class model. Safety,
permission correctness, secret handling, and executable validation are platform
responsibilities rather than model discretion.

The system should automatically improve its runtime profiles over time, but the
optimizer does not own safety policy or unrestricted production authority.

## Confirmed autonomy and permission requirements

### Persona authority

- Permissions are granted per Persona, not inherited merely because another
  Persona in the same Company has them.
- Permission scopes are explicit, typed, versioned, and least-privileged.
- A user can grant persistent permission or persistent prohibition.
- Rejection applies to the active intent and must not be bypassed by rephrasing.
- Unknown permission schemas, versions, operations, or targets fail closed.
- The model proposes actions; deterministic platform logic resolves and validates
  authority.

### Internal agents

A Persona may use Strategy, Analysis, Execution, and Review roles. An operation is
executable only when all of the following pass:

1. Persona permission
2. internal-agent capability
3. Review approval
4. Connection capability
5. contextual policy validation

Internal roles use separate prompts, schemas, bounded outputs, and responsibilities.
More agents are not automatically better. A split must demonstrate reduced error,
useful context isolation, or independent verification against a simpler baseline.
The default is the smallest topology that meets the evaluation gate.

### Review and human escalation

- Execution produces a typed `ToolIntent`; natural-language fallback is never
  executable.
- Review receives structured evidence and returns a typed decision.
- Review and revision are limited to three cycles.
- After exhaustion, the user receives a clear binary decision rather than an
  unbounded agent conversation.
- Review denial cannot be circumvented through semantically equivalent intents.
- Human confirmation is always required only for agreed critical/high-impact
  categories, not for every ordinary deletion or mutation.

Detailed Review, rejection, evidence, and critical-operation rules are in
[`AUTONOMY_AND_CONNECTIONS.md`](AUTONOMY_AND_CONNECTIONS.md).

## Connections, tools, and credentials

### Connections

- Connections are user-owned resources.
- Connection existence, Persona grant, and operation/target permission are
  separate checks.
- Credentials are isolated from prompts, model context, tool output, and durable
  knowledge.
- Provider capabilities do not themselves grant operation permission.
- If a Connection becomes invalid, its grants and permissions remain recorded but
  inactive; reconnection triggers compatibility re-evaluation.

### Tool Packages

- Provider permission and operation schemas are typed and versioned.
- Tool Packages may be generated from formal schemas and service documentation,
  but generated packages start inactive.
- Registration, validation, tests, compatibility checks, and activation are
  separate control-plane operations.
- A Persona cannot self-activate a Tool Package.
- Packages may be shared only inside the same Company; permission authority is
  never shared with the package.
- Compatible package updates may auto-migrate with notification and rollback.
- Incompatible versions fail closed.
- Cross-Company/public package trust, signing, distribution, and revocation remain
  unresolved and are not needed for the first slice.

### Browser-assisted setup

The intended UX minimizes manual setup. Browser-assisted enablement may discover
service requirements and guide configuration through an isolated browser session
with typed browser permissions. MFA, CAPTCHA, sensitive account recovery, and
other protected interactions require secure user takeover. Browser automation
cannot silently broaden Connection or Persona permission.

## Organizational knowledge

Knowledge scope and confidentiality are independent dimensions.

Initial scopes:

- `company`
- `department`
- `customer`
- `project_case`
- `persona_private`

Access eligibility requires scope match, Persona access, classification,
current-goal relevance, and allowed purpose. A deterministic Knowledge Context
Resolver selects and injects the smallest relevant subset under explicit token
budgets.

Promotion to a broader scope is explicit and auditable. It must check
confidentiality, customer and contractual boundaries, personal data, secrets, and
provenance. Cross-scope references preserve the source boundary rather than
copying authority or silently widening visibility.

Raw execution evidence has short retention; durable organizational knowledge is a
separate lifecycle with provenance and legal-hold support. Concrete retention
windows and detailed promotion/declassification rules remain unresolved.

## Workflow-engine decision

### Current priority

LangGraph is the preferred workflow-semantics candidate because the target needs:

- explicit graph state
- parallel fan-out and deterministic join
- interrupt and resume
- checkpoint semantics
- bounded branch failure handling

Cobalt Wren Native is not the preferred internal graph engine. The installed
`cobalt-wren==0.1.0rc3` Native API is asynchronous but has no explicit supported
parallel primitive. Directly gathering multiple `ctx.step()` calls on one mutable
Native context is not treated as a production-safe contract.

### Cobalt Wren adoption is conditional

The first spike must compare:

1. LangGraph executed directly with Company-owned operational adapters
2. LangGraph wrapped by Cobalt Wren's official LangGraph integration

Cobalt Wren should remain only if it materially reduces Company-owned code or risk
for run management, observability, audit, cancellation, retry, resume, checkpoint,
artifact, secret, integration projection, or administration. A 20–30 percent
reduction in relevant operational implementation or tests is a useful indicator,
but semantic fidelity, coupling, latency, and long-term maintenance also matter.

The preferred arrangement, if Cobalt Wren proves useful, is:

```text
Company domain
    -> application-owned workflow port
        -> LangGraph workflow implementation
            -> Cobalt Wren outer execution/operations integration
```

LangGraph state and node types must not leak into Persona, permission, Review,
Connection, Tool Package, knowledge, or audit contracts. Cobalt Wren context and
models must not become the Company domain API.

## First vertical slice

Implementation proceeds in two provider stages using the same domain contracts.

### Stage 1: deterministic fake provider

The fake provider must prove the complete path quickly and reproducibly:

- Support Persona receives a customer inquiry
- deterministic knowledge retrieval supplies bounded relevant context
- Strategy and Analysis produce bounded structured outputs
- Execution proposes a typed draft `ToolIntent`
- permission and Connection resolution run deterministically
- Review detects at least one planned defect and requests revision
- a revised intent passes Review
- the fake draft tool executes idempotently
- redacted evidence and an inspectable audit record are produced
- interrupt/resume, failure, retry, cancellation, and deterministic join fixtures
  can be exercised without a live service

The fake path must not introduce shortcuts that a real provider cannot reuse.

### Stage 2: Gmail draft

Immediately after Stage 1 is stable, reuse the same contracts with a real Gmail
Connection to create a draft only. Sending email is outside the first slice.
The Gmail step validates real authentication, account identity, provider error
normalization, capability mapping, redaction, and compatibility behavior.

## Initial domain contracts

The first implementation should define versioned application-owned contracts for
at least:

- `WorkRequest`
- `Goal`
- `PersonaRef`
- `ConnectionRef`
- `ToolPackageRef`
- `ToolIntent`
- `ReviewDecision`
- `PermissionDecision`
- `KnowledgeContext`
- `EvidenceRef`
- `ExecutionResult`
- `AuditRecord`
- `RuntimeProfileRef`

LangGraph transports these domain objects; it is not their source of truth.
Schemas should reject unknown executable fields and preserve correlation,
idempotency, version identity, and provenance.

## 30B-class model baseline

The first common baseline compares:

- a dense Qwen-family model near 32B parameters
- a Qwen-family 30B-class mixture-of-experts model

Use the same prompts, skills, schemas, context policies, and evaluation corpus
before model-specific tuning. Do not assume total parameter count implies equal
active compute or equal tool-use reliability.

The serving engine is not yet selected. Keep an application-owned LLM client
boundary over an OpenAI-compatible interface or equally thin adapter. Candidate
serving arrangements include vLLM, SGLang, a remote compatible endpoint, and an
optional LiteLLM routing layer. Domain and graph code must not import a provider
SDK directly.

### Initial role parameters

| Role | Temperature | Top-p | Maximum output | Thinking |
| --- | ---: | ---: | ---: | --- |
| Strategy | 0.3 | 0.9 | 2,048 tokens | candidate |
| Analysis | 0.2 | 0.9 | 3,072 tokens | enabled |
| Execution / ToolIntent | 0.0 | 1.0 | 1,024 tokens | disabled |
| Review | 0.0 | 1.0 | 1,536 tokens | disabled by default |
| User response | 0.3 | 0.9 | 2,048 tokens | disabled |
| Runtime-profile optimizer | 0.4 | 0.9 | 4,096 tokens | enabled |

Additional initial settings:

- fixed seed where supported
- no repetition, frequency, or presence penalties initially
- mandatory structured output for executable contracts
- at most two schema-repair attempts
- at most three Review/revision cycles
- fake-tool timeout: 10 seconds
- role-level model timeout: 60 seconds
- initial full-workflow deadline: 180 seconds

These are versioned runtime-profile settings, not domain constants.

### Context budget

Normal context construction targets approximately 16,000 tokens even if the model
supports more:

- system and role instructions: 2,000
- current goal and conversation summary: 2,000
- Knowledge Context: 4,000
- Permission Context: 2,000
- Tool Package definitions: 3,000
- evidence and prior attempts: 3,000
- reserve: 2,000

Context selection, ranking, deduplication, compression, and truncation are
deterministic. Do not inject entire transcripts, policy catalogs, knowledge bases,
or provider payloads.

## Evaluation and release gates

The initial corpus should contain roughly 100–150 scenarios spanning normal,
ambiguous, permission-missing, prohibited, conflicting-evidence, malformed-tool,
provider-change, injection, secret-leakage, high-impact, timeout, cancellation,
retry, checkpoint, interrupt/resume, branch-failure, and deterministic-join cases.

### Protected safety gates

The following require 100 percent success. One failure blocks promotion:

- no execution without required permission
- no persistent-prohibition bypass
- no secret exposure to model context or output
- no malformed-intent execution
- no unconfirmed high-impact execution
- no Persona authority sharing
- no Review-denial circumvention
- fail-closed unknown schema behavior

### Initial quality targets

- schema-valid output: at least 99 percent
- correct abstention: at least 95 percent
- permission-scope accuracy: at least 97 percent
- Review defect detection: at least 90 percent
- unsupported claims: under 1 percent
- fake-provider workflow completion: at least 98 percent
- Gmail-draft workflow completion: at least 95 percent
- convergence within three cycles: at least 95 percent
- unnecessary human escalation: under 10 percent

### Performance and promotion

Record p50/p95 latency, time to first valid `ToolIntent`, model-call count, input
and output tokens, retry count, peak concurrency, accelerator memory, throughput,
and estimated cost per workflow. A candidate must preserve safety gates and may
not worsen p95 latency or token use by more than 20 percent without an explicitly
approved quality tradeoff.

## Runtime-profile optimization

Model quality is treated as a configuration graph, not a prompt-only problem.
Managed surfaces include model and decoding configuration, role topology, prompts,
examples, context policy, Tool Package descriptions and schemas, tool responses,
skills, Review criteria, retry/repair/routing, knowledge retrieval, and permission
context.

Each independently versioned component is assembled into a named or
content-addressed runtime profile. Every execution and evaluation record stores
the complete profile identity.

The system should own failure clustering, candidate generation, controlled
evaluation, staged rollout, and rollback. Initially, optimization runs only by
explicit developer invocation and in CI. Production-trace-driven continuous
optimization begins only after redaction, access control, retention, and eval
coverage are proven.

Low-risk profile changes may auto-promote only through deterministic, predeclared
gates. Changes affecting permission interpretation, high-impact classification,
secret handling, tool side effects, security boundaries, legal/compliance
behavior, or human-confirmation rules require explicit human approval unless a
separately authorized narrow migration policy exists.

Stable protected benchmarks cannot be rewritten by the optimizer. Failure-derived
cases may be proposed and validated as additions.

## Recommended implementation order

1. Define domain schemas, ports, versioning, correlation, and idempotency.
2. Build deterministic fake Connection, Tool Package, provider, policy, clock, and
   cognition fixtures.
3. Implement deterministic permission, knowledge-context, Review, and execution
   gates without a live LLM.
4. Implement the fake-provider draft slice using LangGraph directly.
5. Build the local scenario runner, golden fixtures, contract tests, and evaluation
   harness.
6. Wrap the same compiled graph with Cobalt Wren and perform the adoption spike.
7. Select the workflow arrangement from measured evidence.
8. Add the application-owned LLM adapter and run the two Qwen-family baselines.
9. Tune only from clustered failures, one surface at a time where possible.
10. Add the real Gmail draft Connection.
11. Add system-owned runtime-profile candidate generation and CI evaluation.

Do not connect a live LLM before deterministic domain and safety paths can be
exercised independently; otherwise model errors and architecture errors become
indistinguishable.

## Explicitly unresolved

These items are intentionally deferred unless the first slice demonstrates a need:

- exact Qwen model identifiers and serving engine/runtime
- provider-defined permission-schema governance and compatibility rules
- detailed resource-criticality and blast-radius thresholds
- cross-Company/public Tool Package signing, distribution, trust, and revocation
- documentation discovery and conversion where no formal API schema exists
- provider-specific reconnection and partial-reactivation rules
- concrete retention windows by evidence class and jurisdiction
- detailed knowledge promotion, declassification, and cross-scope aggregation
- exact first customer inquiry, knowledge fixture, expected draft, and planned
  Review defect

Resolve these with evidence and record the decision before implementation depends
on it.

## Working preferences and decision rules

The project owner has repeatedly preferred the following approach:

- evaluate frameworks and models flatly; do not preserve a dependency merely
  because it already exists in the prototype
- favor extensibility, replaceable boundaries, and development efficiency
- avoid throwaway slices, speculative universal frameworks, and central
  provider-name conditionals
- automate repetitive model-quality tuning where safe
- keep production authority separate from optimizer/model authority
- rely on deterministic policy and typed contracts for safety
- design explicitly for approximately 30B-class model limitations
- make failures reproducible with fixtures, record/replay, and complete version
  manifests
- document every confirmed decision, commit it, and push `main`
- when docs monitoring changes generated metadata or causes a commit failure,
  reconcile the generated output, rerun checks, and commit the final consistent
  state rather than bypassing the monitor

## Source-of-truth map

- This document: cross-cutting handoff, current position, and implementation order
- `AUTONOMY_AND_CONNECTIONS.md`: detailed normative autonomy, permission,
  Connection, Review, knowledge, architecture, model, optimization, and evaluation
  requirements
- `ARCHITECTURE.md`: concise current/proposed architecture and boundaries
- `SCOPE_AND_NON_GOALS.md`: current implementation scope and deferred areas
- `RESUME_PLAN.md`: immediate restart checklist
- generated `index.md` and `log.md` files: work-knowledge metadata; do not edit
  manually
