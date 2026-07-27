"""Department-level personas and routing policy."""

from __future__ import annotations

from dataclasses import dataclass

from .cognition import CognitionBackend
from .hierarchy import AgentHierarchy
from .models import DepartmentDecision, Message


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
        outbound = self._route(message, summary, findings)
        return DepartmentDecision(
            department=self.name,
            incoming_message=message,
            findings=findings,
            summary=summary,
            outbound_messages=outbound,
        )

    def _summarize(self, message: Message, findings: tuple[object, ...]) -> str:
        del message, findings
        return f"{self.name} completed its {self.mandate} review."

    def _route(
        self,
        message: Message,
        summary: str,
        findings: tuple[object, ...],
    ) -> tuple[Message, ...]:
        del findings
        original_request = str(message.metadata.get("original_request", message.content))
        outbound = [
            message.forward(
                sender=self.name,
                recipient=recipient,
                content=(
                    f"{summary} Next owner: {recipient}. "
                    f"Original objective: {original_request}"
                ),
                metadata={**message.metadata, "source_department": self.name},
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
                        f"Proposed response for '{original_request}': proceed with a bounded pilot, "
                        "document controls, and maintain a customer-visible support plan."
                    ),
                    metadata={"terminal": True, "customer": customer},
                )
            )
        return tuple(outbound)
