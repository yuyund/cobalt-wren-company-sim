---
title: Scope and Non-goals
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

# Scope and Non-goals

## Existing prototype scope

- department-level Personas
- Strategy, Analysis, and Execution internal roles
- bounded chat-style interdepartmental handoffs
- external customer and user actor types
- deterministic routing and completion
- structured transcript and department decisions
- replaceable cognition backend contract
- CLI and Cobalt Wren Native wrapper paths

## Next vertical-slice scope

- application-owned versioned domain contracts
- Support Persona customer-response draft scenario
- deterministic fake Connection, Tool Package, provider, policy, clock, and
  cognition fixtures
- typed `ToolIntent`, Review, permission, knowledge, evidence, execution, and audit
- least-privileged Persona grants and persistent prohibitions
- redacted evidence and reproducible execution records
- LangGraph direct implementation with bounded parallel/join fixtures
- direct-LangGraph versus Cobalt-Wren-wrapped comparison
- Qwen-family dense versus MoE 30B-class baseline
- real Gmail draft Connection after the fake path is stable
- CI and explicit-developer runtime-profile optimization

## Explicit non-goals for the first slice

- sending email rather than creating a draft
- autonomous legal or contractual commitments
- autonomous financial approval or purchasing
- autonomous security exceptions
- unrestricted self-modification or self-activation
- optimizer ownership of safety policy
- production-trace-driven continuous optimization
- production-grade universal company-data retention
- unbounded agent conversation
- model-provider installation owned by Cobalt Wren
- LangGraph or Cobalt Wren types as Company domain APIs
- universal mapping of every organization structure
- realistic human psychology simulation
- cross-Company or public Tool Package distribution
- universal ingestion of service documentation without formal schemas

## Deferred capabilities

- detailed jurisdiction-specific retention windows
- advanced knowledge promotion, declassification, and cross-scope aggregation
- provider-specific partial Connection reactivation
- public package signing, trust, revocation, and distribution
- full customer/account history and production organizational memory
- autonomous profile rollout from production traces
- distributed workflow execution beyond the first measured need
- broader external-service operations beyond Gmail draft
