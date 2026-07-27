---
title: Cobalt Wren Company Simulation
type: guide
status: current
created_at: '2026-07-27'
updated_at: '2026-07-27'
review:
  due_at: '2027-01-23'
---

# Cobalt Wren Company Simulation

A reference application that models a company as a set of department-level
personas. Each department persona owns a small hierarchy of internal agents and
communicates with other departments through a chat-style message bus.

The user supplies a goal or customer request. The simulation handles routing,
delegation, departmental collaboration, and customer-facing closure with minimal
user intervention.

## Model

```text
User / External Customer
          ↓
Company Chat Bus
          ↓
Department Persona
  ├─ Strategy agent
  ├─ Analysis agent
  └─ Execution agent
          ↓
Other Department Personas
```

The initial customer journey is:

```text
Customer → Sales → Product → Engineering → Operations → Support → Customer
                    ↘ Executive visibility
```

The implementation deliberately starts without an LLM dependency. A
`CognitionBackend` protocol isolates model reasoning from company orchestration.
The default `RuleBasedCognition` backend is deterministic, testable, and suitable
for proving Cobalt Wren workflow and observability boundaries.

## Install from TestPyPI

```bash
python -m venv .venv
source .venv/bin/activate
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  cobalt-wren==0.1.0rc3
pip install -e '.[dev]'
```

## Run

```bash
company-sim \
  --customer "Acme Corp" \
  --request "We need an auditable support automation pilot in two weeks."
```

Or invoke the Cobalt Wren Native workflow:

```bash
cobalt-wren native-run company_sim.workflow:simulate_company \
  --input '{"customer":"Acme Corp","request":"Design a support automation pilot"}'
```

## Current scope

- department personas with stable responsibilities
- three-level internal reasoning hierarchy
- asynchronous-style chat queue with correlation IDs
- bounded hop count and deterministic convergence
- customer and user actor types
- structured transcript and department decisions
- Cobalt Wren Native workflow wrapper

## Next steps

- persistent company memory and policy documents
- approval gates for financial, legal, and external commitments
- pluggable LLM backends implemented by the consuming application
- observability coverage and semantic projections
- concurrent department work and conflict resolution
