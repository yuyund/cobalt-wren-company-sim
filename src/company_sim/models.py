"""Domain models for the company simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


class ActorKind(StrEnum):
    USER = "user"
    CUSTOMER = "customer"
    DEPARTMENT = "department"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class Message:
    sender: str
    recipient: str
    content: str
    sender_kind: ActorKind
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    hop: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def forward(
        self,
        *,
        sender: str,
        recipient: str,
        content: str,
        sender_kind: ActorKind = ActorKind.DEPARTMENT,
        metadata: dict[str, Any] | None = None,
    ) -> "Message":
        return Message(
            sender=sender,
            recipient=recipient,
            content=content,
            sender_kind=sender_kind,
            correlation_id=self.correlation_id,
            hop=self.hop + 1,
            metadata={} if metadata is None else metadata,
        )


@dataclass(frozen=True, slots=True)
class AgentFinding:
    role: str
    summary: str
    confidence: float


@dataclass(frozen=True, slots=True)
class DepartmentDecision:
    department: str
    incoming_message: Message
    findings: tuple[AgentFinding, ...]
    summary: str
    outbound_messages: tuple[Message, ...]


@dataclass(frozen=True, slots=True)
class CompanyResult:
    correlation_id: str
    status: str
    customer_response: str | None
    transcript: tuple[Message, ...]
    decisions: tuple[DepartmentDecision, ...]
    rounds: int
