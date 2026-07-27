"""Department-level personas and routing policy."""

from __future__ import annotations

from dataclasses import dataclass

from .cognition import CognitionBackend
from .hierarchy import AgentHierarchy
from .models import ActorKind, DepartmentDecision, Message


@dataclass(frozen=True, slots=True)
class DepartmentPersona:
    name: str
    mandate: str
    hierarchy: AgentHierarchy
    next_departments: tuple[str, ...] = ()
    customer_facing: bool = False

    def handle(self, message: Message, *, backend: CognitionBackend) -> DepartmentDecision:
        findings = self.hierarchy.deliberate(
            department=self.name,
            message=message,
            backend=backend,
        )
        summary = self._summarize(message, findings)
        outbound = self._route(message, summary)
        return DepartmentDecision(
            department=self.name,
            incoming_message=message,
            findings=findings,
            summary=summary,
            outbound_messages=outbound,
        )

    def _summarize(self, message: Message, findings: tuple[object, ...]) -> str:
        del findings
        return f"{self.name} accepted '{message.content}' and completed its {self.mandate} review."

    def _route(self, message: Message, summary: str) -> tuple[Message, ...]:
        outbound = [
            message.forward(
                sender=self.name,
                recipient=recipient,
                content=f"{summary} Required handoff to {recipient}: {message.content}",
                metadata={"source_department": self.name},
            )
            for recipient in self.next_departments
        ]
        if self.customer_facing:
            customer = str(message.metadata.get("customer", "external-customer"))
            outbound.append(
                message.forward(
                    sender=self.name,
                    recipient=customer,
                    content=(
                        "We have aligned Sales, Product, Engineering, Operations, and Support. "
                        f"Proposed response: {message.content}"
                    ),
                    metadata={"terminal": True, "customer": customer},
                )
            )
        return tuple(outbound)
