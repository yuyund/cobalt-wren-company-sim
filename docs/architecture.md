---
title: Architecture
type: reference
status: current
owner: repository-maintainers
created_at: '2026-07-27'
updated_at: '2026-07-28'
review:
  due_at: '2026-08-10'
validity:
  due_at: '2027-07-27'
---

# Architecture

## Purpose

This repository is a reference application and proving ground for a Company
system composed of department-level Personas and bounded internal agents. The
current code is a deterministic prototype; the next slice establishes the stable
contracts for permission-constrained autonomy, external Connections, Review,
organizational knowledge, and observable tool execution.

The Company domain must remain independent of any workflow engine, model SDK, or
operations framework.

## Proven prototype

The current code models:

```text
External Customer / User
          |
          v
    Company Message Bus
          |
          v
  Department Persona
    |- Strategy agent
    |- Analysis agent
    `- Execution agent
          |
          v
 Other Department Personas
```

The fixed deterministic journey is:

```text
Customer -> Sales -> Product -> Engineering -> Operations -> Support -> Customer
                 `-> Executive visibility
```

This path proves bounded routing and correlation, not the target dynamic workflow
architecture.

## Target boundaries

```text
Company domain contracts
  |- Persona and internal roles
  |- Goal and WorkRequest
  |- Permission and prohibition
  |- ReviewDecision
  |- Connection and ToolPackage references
  |- KnowledgeContext and EvidenceRef
  |- ToolIntent and ExecutionResult
  `- AuditRecord and RuntimeProfileRef
              |
              v
      Application workflow port
              |
              v
       LangGraph implementation
              |
              v
 Optional Cobalt Wren operations wrapper
              |
              v
 Providers, stores, tools, and external services
```

### Company domain

The domain owns goals, Personas, authority, policy decisions, Review, knowledge
boundaries, executable intents, evidence references, audit semantics, correlation,
idempotency, and version identity. It does not expose LangGraph or Cobalt Wren
types.

### Workflow implementation

LangGraph is the preferred workflow-semantics candidate for the first spike. It
is responsible for graph state transport, fan-out/join, interrupt/resume, and
checkpoint-aware control flow. LangGraph state transports domain objects and is
not their source of truth.

### Operations integration

Cobalt Wren is conditional. Compare direct LangGraph with LangGraph wrapped by
Cobalt Wren. Retain Cobalt Wren only if its run administration, observability,
audit, cancellation, retry, resume, checkpoint, artifact, secret, and projection
capabilities materially reduce Company-owned code and risk.

Cobalt Wren Native is not the preferred internal graph engine.

### Cognition and model serving

An application-owned LLM client is the only model boundary. Domain and graph code
must not import provider SDKs. The first baseline compares dense and MoE
Qwen-family 30B-class profiles behind a thin compatible adapter. Serving-engine
selection remains open.

### Connections and Tool Packages

Connections are user-owned credential-bearing resources. Tool Packages are typed,
versioned operational interfaces. Connection existence, Persona grant,
operation/target permission, Review, and contextual policy are separate gates.
Credentials never enter model context or durable knowledge.

### Knowledge and evidence

A deterministic resolver selects the smallest relevant Knowledge Context under a
bounded budget. Raw evidence and durable organizational knowledge have separate
lifecycles and preserve provenance and scope boundaries.

## First slice

The first production-shaped slice is Support Persona draft creation:

1. run through a deterministic fake provider
2. validate the same contracts with a real Gmail draft Connection

It must prove typed `ToolIntent`, permission resolution, Review revision,
idempotent execution, redacted evidence, audit, failure/retry/cancel behavior,
and a framework comparison using the same fixtures.

## Safety and convergence

- unknown schemas and versions fail closed
- executable output is typed and platform-validated
- permission and secret handling are deterministic
- Review/revision is limited to three cycles
- model repair is limited to two attempts
- protected safety cases require 100 percent success
- graph branches and joins are bounded and deterministic
- every run records complete runtime-profile and contract versions

See [`autonomy-and-connections.md`](autonomy-and-connections.md) for normative
detail and [`implementation-handoff.md`](implementation-handoff.md) for the current implementation plan.
