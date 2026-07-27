"""Cognition boundary for department-internal agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import AgentFinding, Message


@dataclass(frozen=True, slots=True)
class AgentPrompt:
    department: str
    role: str
    mandate: str
    message: Message


class CognitionBackend(Protocol):
    def evaluate(self, prompt: AgentPrompt) -> AgentFinding:
        """Return one bounded finding for an internal agent role."""


class RuleBasedCognition:
    """Deterministic backend used to prove orchestration without an LLM SDK."""

    def evaluate(self, prompt: AgentPrompt) -> AgentFinding:
        normalized = " ".join(prompt.message.content.split())
        if prompt.role == "strategy":
            summary = (
                f"Align {prompt.department} response with mandate: {prompt.mandate}. "
                f"Primary objective: {normalized}"
            )
            confidence = 0.88
        elif prompt.role == "analysis":
            risks = self._risk_terms(normalized)
            risk_text = ", ".join(risks) if risks else "no explicit risk keyword"
            summary = f"Extracted constraints and risks: {risk_text}. Request length={len(normalized)}."
            confidence = 0.82
        else:
            summary = f"Recommended next concrete action for {prompt.department}: process and hand off '{normalized}'."
            confidence = 0.9
        return AgentFinding(role=prompt.role, summary=summary, confidence=confidence)

    @staticmethod
    def _risk_terms(text: str) -> tuple[str, ...]:
        terms = ("deadline", "two weeks", "audit", "legal", "security", "budget", "customer")
        lowered = text.lower()
        return tuple(term for term in terms if term in lowered)
