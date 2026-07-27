"""Company-level autonomous orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .bus import MessageBus
from .cognition import CognitionBackend, RuleBasedCognition
from .departments import DepartmentPersona
from .hierarchy import default_hierarchy
from .models import ActorKind, CompanyResult, DepartmentDecision, Message


@dataclass(slots=True)
class CompanySimulation:
    departments: dict[str, DepartmentPersona]
    backend: CognitionBackend
    max_rounds: int = 32

    def run_customer_request(self, *, customer: str, request: str) -> CompanyResult:
        bus = MessageBus()
        initial = Message(
            sender=customer,
            recipient="sales",
            content=request,
            sender_kind=ActorKind.CUSTOMER,
            metadata={"customer": customer, "original_request": request},
        )
        bus.publish(initial)
        decisions: list[DepartmentDecision] = []
        customer_response: str | None = None
        rounds = 0

        while rounds < self.max_rounds:
            message = bus.next_message()
            if message is None:
                break
            rounds += 1
            department = self.departments.get(message.recipient)
            if department is None:
                if message.metadata.get("terminal"):
                    customer_response = message.content
                continue
            decision = department.handle(message, backend=self.backend)
            decisions.append(decision)
            for outbound in decision.outbound_messages:
                bus.publish(outbound)

        status = "completed" if customer_response else "incomplete"
        return CompanyResult(
            correlation_id=initial.correlation_id,
            status=status,
            customer_response=customer_response,
            transcript=bus.transcript,
            decisions=tuple(decisions),
            rounds=rounds,
        )


def build_default_company(*, backend: CognitionBackend | None = None) -> CompanySimulation:
    specifications = (
        ("sales", "customer discovery and commercial framing", ("product", "executive"), False),
        ("executive", "strategic visibility and policy alignment", (), False),
        ("product", "problem definition and product scope", ("engineering",), False),
        ("engineering", "technical feasibility and implementation plan", ("operations",), False),
        ("operations", "delivery, reliability, and rollout readiness", ("support",), False),
        ("support", "customer communication and service continuity", (), True),
    )
    departments = {
        name: DepartmentPersona(
            name=name,
            mandate=mandate,
            hierarchy=default_hierarchy(mandate),
            next_departments=next_departments,
            customer_facing=customer_facing,
        )
        for name, mandate, next_departments, customer_facing in specifications
    }
    return CompanySimulation(departments=departments, backend=backend or RuleBasedCognition())
