---
title: Architecture, Model, and Evaluation
type: reference
status: current
owner: repository-maintainers
created_at: '2026-07-27'
updated_at: '2026-07-28'
review:
  due_at: '2026-08-10'
validity:
  due_at: '2027-07-28'
---

# Architecture, Model, and Evaluation

Normative architecture, workflow-engine selection, 30B-class model assumptions, runtime-profile optimization, evaluation, and release gates.

## Vertical-slice architecture principles

The first vertical slice should be small in user-visible scope but must not be a
throwaway implementation. It should exercise stable contracts across persona
reasoning, Review, permission resolution, Connection access, Tool Package
execution, knowledge use, and observability while keeping provider-specific and
policy-specific behavior replaceable.

The architecture should favor explicit contracts and dependency inversion over
shared mutable implementation state. Core orchestration must depend on interfaces
for tool discovery, scope-schema registration, permission matching, Connection
resolution, Review, evidence collection, knowledge retrieval, execution, and
audit persistence. Provider adapters, policy implementations, storage backends,
and UI surfaces should plug into those contracts without requiring changes to
the central workflow.

Dynamic behavior must be represented as validated data and versioned packages,
not as unbounded conditionals embedded in the orchestration layer. New services,
operations, capability bundles, scope dimensions, risk metadata, browser flows,
and knowledge scopes should normally be introduced through registries,
declarative schemas, or isolated adapters. Unknown types and versions fail
closed, while known contracts remain forward-extensible.

The system should separate control-plane concerns from execution-plane concerns:

- the control plane registers and validates Tool Packages, provider schemas,
  policies, Connections, grants, versions, and migrations
- the execution plane evaluates a concrete intent against an immutable snapshot
  of those definitions and performs only the authorized operation

Execution records should reference versioned definitions so later changes do not
alter the meaning of historical decisions. Long-running or retried work must use
idempotency keys, correlation identifiers, explicit state transitions, and
recoverable checkpoints rather than relying on in-process conversational state.

Extension points must be capability-oriented rather than provider-name-oriented.
For example, Review should evaluate declared effects and evidence requirements,
not contain Gmail- or GitHub-specific branches. Provider-specific semantics
belong in typed metadata and adapters, with deterministic platform validation at
the boundary.

The first slice should intentionally prove these seams with one low-risk use case,
such as creating an external-service draft. It should include at least one real
Connection, a typed ToolIntent, Review revision, permission matching, a versioned
Tool Package, redacted execution evidence, and an inspectable audit trail. Later
services should be addable primarily by registering new packages and schemas,
not by modifying the slice's orchestration path.

Implementation should proceed in two steps. First, a deterministic fake provider
should exercise the complete architecture quickly and reproducibly. Immediately
after that path is stable, the same contracts should be validated against a real
Gmail draft Connection. The fake-provider step must not define provider-specific
shortcuts that the Gmail step cannot reuse.

Architectural abstractions should still be evidence-driven. The project must not
build a speculative universal framework before the vertical slice exposes a real
variation point. When a second implementation cannot fit an existing contract
cleanly, the contract should be generalized with compatibility tests and a
recorded design rationale. Changes to Cobalt Wren itself should be proposed only
when the Company slice demonstrates a missing framework-level primitive rather
than an application-specific need.

Workflow-engine selection must also remain evidence-driven. The Company should not
use Cobalt Wren Native merely because the existing prototype does, nor remove
Cobalt Wren merely because LangGraph provides richer graph execution. The first
vertical slice should preserve application-owned workflow contracts and compare
at least:

- LangGraph executed directly with Company-owned operational integrations
- LangGraph wrapped by Cobalt Wren's official integration

The comparison should measure implementation complexity, parallel fan-out and
join behavior, interrupt and resume semantics, checkpoint durability, cancellation
and retry behavior, observability fidelity, audit and run administration,
artifact and secret integration, testability, latency, and operational coupling.
Cobalt Wren is justified only where its cross-framework run model, projections,
audit, controls, stores, UI, or integration boundaries remove more Company-owned
code and risk than the wrapper and dependency introduce.

LangGraph graph state and node semantics must not leak into Persona, permission,
Tool Package, Review, knowledge, or audit domain contracts. Conversely, Cobalt
Wren-specific workflow context must not become the application domain API. A
thin adapter boundary should allow the selected execution arrangement to change
without rewriting the core Company behavior.

The initial architecture decision should be made after a bounded spike using the
same fake-provider draft scenario and evaluation fixtures. LangGraph is the
preferred workflow-semantics candidate for that spike because the Company needs
explicit graph state, parallel fan-out and join, interrupt and resume, and
checkpoint behavior. Cobalt Native is not the preferred internal graph engine.

The spike should compare LangGraph executed directly with LangGraph wrapped by
Cobalt Wren. If Cobalt Wren adds no material operational value, LangGraph should
be used directly. If it materially reduces Company-owned operational code and
risk, the preferred arrangement is LangGraph for workflow semantics and Cobalt
Wren as an outer execution, observability, audit, and administration layer.
Cobalt Wren adoption is therefore conditional on measured value rather than a
project constraint.
## 30B-class model operating assumptions

The system must be designed to operate reliably with an approximately 30B-class
language model rather than assuming frontier-model reasoning quality. Correctness
must come from constrained responsibilities, typed contracts, deterministic
platform checks, and measurable evaluation rather than from increasingly broad
prompts or unconstrained autonomous planning.

Each LLM role should receive the smallest context and decision surface needed for
its task. Strategy, Analysis, Execution, and Review should use separate prompts,
explicit input schemas, bounded output schemas, short instruction hierarchies,
and task-specific examples. The model should propose classifications, plans,
claims, or typed intents; the platform remains responsible for normalization,
policy matching, permission decisions, schema validation, secret handling,
execution, and state transitions.

Structured generation must be treated as a compiler boundary. Outputs should be
validated against versioned schemas, rejected on unknown fields or invalid enum
values, and repaired through narrow, diagnostic retries rather than by replaying
an entire conversation. Natural-language fallbacks must not silently become
executable actions. The system should prefer constrained choices, retrieved
identifiers, and canonical values over requiring the model to reproduce opaque
IDs or provider-specific syntax from memory.

Context construction is a primary reliability mechanism. Permission Context,
Knowledge Context, Tool Package definitions, and evidence should be selected by
deterministic resolvers, ranked for relevance, deduplicated, and kept within
explicit token budgets. Large raw transcripts, policy stores, API documentation,
or tool catalogs should not be injected wholesale. Summaries must retain source
references so Review can distinguish retrieved facts from model inference.

The runtime should support model-adaptive execution without coupling application
logic to one model. Prompt templates, decoding settings, context budgets, retry
policies, and role assignments should be versioned configuration. A stronger or
smaller model may be substituted per role, but the same typed contracts and
platform gates must apply. Model self-reported confidence is advisory only and
must not bypass deterministic checks.

Evaluation is part of the product architecture. Every important contract should
have a reproducible evaluation set covering normal cases, ambiguous requests,
missing permissions, prohibitions, conflicting evidence, malformed tool output,
provider changes, prompt injection, secret leakage, and high-impact actions.
Metrics should include schema-valid output rate, correct abstention, permission
scope accuracy, Review defect detection, unsupported-claim rate, tool success,
retry count, latency, token use, and human-escalation rate. Regressions must block
prompt, schema, model, or Tool Package promotion according to defined thresholds.

Development efficiency should come from reusable fixtures and observability, not
from weakening the gates. The project should provide:

- deterministic fake Connections, tools, providers, clocks, and policy stores
- golden ToolIntent, Review, evidence, and audit fixtures
- record-and-replay of redacted model and tool interactions
- local scenario runners for one complete workflow
- contract tests for every adapter and schema version
- prompt and model comparison harnesses using the same evaluation corpus
- failure clustering that distinguishes model, prompt, context, schema, policy,
  adapter, and provider defects

The first vertical slice should establish a measurable baseline on the target
30B-class model before expanding functionality. A capability is not complete
merely because it succeeds in a demonstration; it must meet agreed reliability,
cost, and latency thresholds across the evaluation corpus. When the model fails,
the preferred remedy order is: reduce ambiguity, improve deterministic context,
tighten the schema, split the task, add platform validation, improve examples,
and only then consider model-specific tuning or a stronger model.

Fine-tuning may be considered after sufficient representative failure data
exists, but the architecture must not depend on fine-tuning for basic safety or
policy correctness. Prompt changes, model changes, and fine-tuned checkpoints
must be versioned and auditable alongside Tool Package and policy versions.

Model quality depends on a configuration graph rather than on prompts alone. The
managed tuning surfaces include at least:

- model and decoding configuration
- role and agent decomposition
- prompt templates and examples
- context selection, ordering, compression, and token budgets
- Tool Package descriptions and argument schemas
- tool return schemas, error taxonomies, and evidence formatting
- skills, procedures, and reusable task instructions
- Review criteria and escalation rules
- retry, repair, routing, and fallback policies
- knowledge retrieval and permission-context resolution

These surfaces must be versioned as independently replaceable components and
assembled into a named runtime profile. Every execution and evaluation result
should record the complete profile identity or a content-addressed manifest so a
behavior can be reproduced without guessing which combination was active.

Changes should be evaluated as controlled experiments against a shared corpus.
The tooling must support changing one surface at a time, comparing complete
profiles when interactions are unavoidable, and reporting metric deltas by
scenario class. Promotion should require evidence that the new profile improves
the intended failure modes without unacceptable regressions elsewhere. Ad hoc
production edits to prompts, skills, schemas, or routing rules are prohibited.

Skills should be treated as typed, versioned operational knowledge rather than
unstructured prompt fragments. A skill should declare its purpose, applicable
roles, required context and tools, expected output contract, preconditions,
failure modes, examples, evaluation cases, and compatibility constraints. Skills
may guide model behavior but cannot grant permission, expose credentials, or
bypass platform validation.

Tool responses are part of the model interface and require the same design rigor
as tool inputs. Responses should be small, typed, stable, and action-oriented;
separate machine-consumable facts from human display text; use canonical error
codes; identify retryability and missing prerequisites; include provenance; and
avoid returning large provider payloads unless specifically requested through a
bounded evidence reference. Tool adapters should normalize provider variation so
agents do not need provider-specific parsing strategies.

Agent decomposition should be justified by measured error reduction, context
isolation, or independent verification. More agents are not inherently more
accurate: they can add latency, cost, information loss, and correlated mistakes.
Each split must define ownership, input/output contracts, termination conditions,
and a comparison against a simpler baseline. The default should be the smallest
number of roles that meets the evaluation threshold.

To preserve development velocity, the evaluation harness should support a
configuration matrix, cached deterministic stages, replayable model boundaries,
and targeted test selection based on changed components. A prompt-only change
should not require live provider execution when recorded tool fixtures suffice;
a Tool Package change should run its contract and affected end-to-end scenarios;
a policy change should run permission and high-impact suites. Full profile tests
remain required before release.

Runtime-profile optimization should be system-owned by default. The platform may
analyze clustered failures, generate candidate changes to prompts, examples,
skills, agent topology, tool descriptions, tool-return normalization, context
policies, and retry or routing rules, then evaluate those candidates against the
shared corpus without requiring a developer to hand-edit every surface.

Initial optimization execution should be limited to explicit developer invocation
and CI runs. Production-trace-driven continuous optimization should be enabled
only after redaction, retention, access control, and representative evaluation
coverage are proven. This sequencing limits feedback-loop risk while preserving
the system-owned candidate-generation and evaluation workflow.

Candidate generation and production authority are separate. Automatically
generated profiles begin inactive and must pass schema validation, security and
policy checks, targeted evaluations, full regression suites, cost and latency
limits, and compatibility analysis. Candidates that satisfy predeclared promotion
criteria may be promoted automatically for low-risk profile changes. Promotion
criteria, metric thresholds, protected scenarios, allowed change classes, and
maximum regression budgets are deterministic policy owned by the platform, not
self-declared by the optimizing model.

Automatic promotion must be more restrictive for changes that affect permission
interpretation, high-impact classification, secret handling, tool side effects,
security boundaries, legal or compliance behavior, or human-confirmation rules.
Those changes require explicit human approval unless a separately authorized,
narrow automation policy permits a well-defined compatible migration. The
optimizer must never weaken invariant safety gates to improve task-success
metrics.

The system should use staged rollout where practical: offline evaluation,
shadow or replay evaluation, bounded canary traffic, then broader activation.
Each stage must use immutable profile versions, comparable metrics, and automatic
rollback when health, safety, quality, cost, or latency thresholds are violated.
Rollback restores the complete prior profile rather than attempting an ad hoc
partial reversal.

Optimization must remain reproducible and auditable. Each candidate should record
the triggering failures, proposed component diffs, generator identity and model,
training or evaluation data references, evaluation results, promotion decision,
rollout status, and rollback history. Production traces used for optimization
must be redacted, access-controlled, and subject to the applicable retention and
knowledge policies.

To prevent self-reinforcing regressions, automatically generated evaluation cases
must not replace the stable human- or policy-approved benchmark corpus. New
failure-derived cases may extend the corpus after validation, while protected
safety and permission cases remain immutable except through explicit governance.
The optimizer should prefer minimal component changes and must demonstrate that a
more complex agent topology or skill set outperforms the simpler active baseline.
## Initial model profiles and release gates

The first model baseline should compare a dense Qwen-family model near 32B
parameters with a Qwen-family 30B-class mixture-of-experts model using the same
prompts, skills, tool schemas, context policies, and evaluation corpus. Model-
specific tuning begins only after the common baseline is recorded.

Initial role profiles are:

| Role | Temperature | Top-p | Maximum output | Thinking |
| --- | ---: | ---: | ---: | --- |
| Strategy | 0.3 | 0.9 | 2,048 tokens | candidate |
| Analysis | 0.2 | 0.9 | 3,072 tokens | enabled |
| Execution / ToolIntent | 0.0 | 1.0 | 1,024 tokens | disabled |
| Review | 0.0 | 1.0 | 1,536 tokens | disabled by default |
| User response | 0.3 | 0.9 | 2,048 tokens | disabled |
| Runtime-profile optimizer | 0.4 | 0.9 | 4,096 tokens | enabled |

A provider seed should be fixed where supported. Repetition, frequency, and
presence penalties are initially disabled. Structured output is mandatory for
executable contracts; unknown fields and invalid values are rejected. Schema
repair is limited to two attempts, Review/revision to three cycles, fake-provider
tool calls to ten seconds, role-level model calls initially to sixty seconds, and
the complete initial workflow to a 180-second deadline. These values are versioned
profile configuration, not hard-coded domain behavior.

Normal context construction should remain within approximately 16,000 tokens even
when the selected model supports a larger window. Initial component budgets are:
2,000 tokens for system and role instructions, 2,000 for the current goal and
conversation summary, 4,000 for Knowledge Context, 2,000 for Permission Context,
3,000 for Tool Package definitions, 3,000 for evidence and prior attempts, and
2,000 reserve. Deterministic resolvers may retrieve additional bounded material
only when the workflow explicitly requires it.

The initial evaluation corpus should contain roughly 100 to 150 scenarios covering
normal draft creation, Knowledge use, Review revision, Connection and Tool Package
resolution, Persona handoff, missing or prohibited permissions, account and scope
mismatch, high-impact actions, secret requests, prompt injection, ambiguous and
conflicting instructions, stale or incorrect knowledge, malformed tool results,
schema-version mismatch, timeout, cancellation, retry, checkpoint recovery,
interrupt/resume, partial branch failure, and deterministic parallel join.

Safety release gates require 100 percent success on protected cases, including:

- no execution without required permission
- no bypass of persistent prohibitions
- no secret exposure to model context or output
- no execution of malformed intents
- no high-impact execution without required confirmation
- no sharing of authority between Personas
- no circumvention after Review denial
- fail-closed behavior for unknown schemas

Any protected-case failure blocks promotion. Initial quality targets are at least
99 percent schema-valid output, 95 percent correct abstention, 97 percent permission
scope accuracy, 90 percent Review defect detection, under 1 percent unsupported
claims, 98 percent fake-provider workflow completion, 95 percent Gmail-draft
workflow completion, 95 percent convergence within three cycles, and under 10
percent unnecessary human escalation. These thresholds may be revised only from
recorded baseline evidence without weakening protected safety gates.

Performance baselines should record p50 and p95 latency, time to first valid
ToolIntent, model-call count, input and output tokens, retry count, peak
concurrency, accelerator memory, throughput, and estimated cost per workflow. A
candidate profile must preserve all safety gates and must not worsen p95 latency
or token consumption by more than 20 percent unless an explicitly approved quality
tradeoff justifies it.

The LangGraph-direct versus LangGraph-through-Cobalt-Wren spike uses the same
fake-provider scenario and fixtures. Cobalt Wren should be retained only if it
materially reduces Company-owned operational code or risk through run management,
observability, audit, cancellation, retry, resume, checkpoint, artifact, secret,
or administrative capabilities. A 20 to 30 percent reduction in relevant
operational implementation or tests is a useful indicator, but the decision must
also account for semantic fidelity, coupling, and long-term maintenance.
