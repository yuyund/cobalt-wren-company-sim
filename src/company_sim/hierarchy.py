"""Hierarchical internal agent structure for one department persona."""

from __future__ import annotations

from dataclasses import dataclass

from .cognition import AgentPrompt, CognitionBackend
from .models import AgentFinding, Message


@dataclass(frozen=True, slots=True)
class InternalAgent:
    role: str
    mandate: str

    def evaluate(
        self,
        *,
        department: str,
        message: Message,
        backend: CognitionBackend,
    ) -> AgentFinding:
        return backend.evaluate(
            AgentPrompt(
                department=department,
                role=self.role,
                mandate=self.mandate,
                message=message,
            )
        )


@dataclass(frozen=True, slots=True)
class AgentHierarchy:
    strategy: InternalAgent
    analysis: InternalAgent
    execution: InternalAgent

    def deliberate(
        self,
        *,
        department: str,
        message: Message,
        backend: CognitionBackend,
    ) -> tuple[AgentFinding, ...]:
        return tuple(
            agent.evaluate(department=department, message=message, backend=backend)
            for agent in (self.strategy, self.analysis, self.execution)
        )


def default_hierarchy(mandate: str) -> AgentHierarchy:
    return AgentHierarchy(
        strategy=InternalAgent("strategy", f"Interpret business intent for {mandate}"),
        analysis=InternalAgent("analysis", f"Identify constraints and risks for {mandate}"),
        execution=InternalAgent("execution", f"Choose a bounded next action for {mandate}"),
    )
