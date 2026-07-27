# Architecture

## Purpose

This repository is a reference application for modeling a company as a set of
department-level personas. Each department owns a hierarchy of internal agents
and communicates with other departments through a bounded chat-style message
bus.

The system is intentionally separate from Cobalt Wren. It consumes Cobalt Wren
as an application dependency and is used to validate public workflow contracts,
Native authoring, observability boundaries, and package installation behavior.

## Current model

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

The current deterministic journey is:

```text
Customer -> Sales -> Product -> Engineering -> Operations -> Support -> Customer
                 `-> Executive visibility
```

## Core boundaries

### Company orchestration

`CompanySimulation` owns bounded message processing, department lookup,
correlation, completion detection, and the final result.

### Department persona

A `DepartmentPersona` owns a stable mandate, its internal hierarchy, and its
handoff policy. It does not own transport, persistence, or model SDK setup.

### Internal hierarchy

Each department currently has three internal roles:

- strategy: interprets intent and mandate alignment
- analysis: identifies constraints and risks
- execution: chooses a bounded next action

### Cognition backend

`CognitionBackend` is the model boundary. The default implementation is
`RuleBasedCognition`, which is deterministic and requires no LLM SDK.

Future LLM implementations belong in this consuming repository or another
application package. Cobalt Wren supplies contracts and observation helpers; it
does not own provider installation or version policy.

### Message bus

Messages carry a correlation ID, sender, recipient, actor kind, hop count,
content, and metadata. Original customer intent is retained in metadata so
handoffs remain bounded rather than recursively quoting the entire transcript.

### Cobalt Wren workflow

`company_sim.workflow:simulate_company` exposes the simulation as a Cobalt Wren
Native workflow. The workflow records progress and metrics while the company
domain remains independent of Cobalt Wren internals.

## Planned autonomy boundary

The agreed direction for permissions, review, external Connections, credential
isolation, rejection handling, and tool-call observability is recorded in
[`AUTONOMY_AND_CONNECTIONS.md`](AUTONOMY_AND_CONNECTIONS.md). These are planned
contracts rather than claims about the current prototype.

## Safety and convergence constraints

- bounded maximum hop count
- bounded maximum processing rounds
- short department handoff summaries
- explicit terminal customer response
- deterministic default cognition backend
- no financial, legal, security, or external commitment authority
