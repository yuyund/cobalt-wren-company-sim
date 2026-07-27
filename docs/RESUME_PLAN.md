# Resume Plan

Work on this repository is paused after the first vertical slice.

## Proven state

- customer request crosses all configured departments
- every department invokes strategy, analysis, and execution roles
- messages retain correlation identity
- conversation content remains bounded
- customer-facing completion is produced
- CLI execution passes
- Cobalt Wren Native execution passes
- Ruff, mypy, pytest, and GitHub Actions pass

## Recommended restart order

1. Implement the smallest permission, Review, and observable tool-intent vertical slice described in `AUTONOMY_AND_CONNECTIONS.md`.
2. Add organizational memory contracts.
3. Add approval policy and escalation events.
4. Define typed conversation intents such as request, proposal, objection,
   approval, handoff, and customer response.
5. Add an application-owned LLM backend.
6. Add Cobalt Wren semantic events and observability coverage reporting.
7. Add concurrent department processing and deterministic conflict resolution.

## Dependency policy

The repository should declare every model SDK and workflow framework it uses.
Cobalt Wren should remain a framework-neutral operational dependency and should
not control those SDK versions.
