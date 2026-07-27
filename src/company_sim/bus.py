"""Bounded chat-style message bus."""

from __future__ import annotations

from collections import deque

from .models import Message


class MessageBus:
    def __init__(self, *, max_hops: int = 12) -> None:
        self._queue: deque[Message] = deque()
        self._transcript: list[Message] = []
        self.max_hops = max_hops

    def publish(self, message: Message) -> None:
        if message.hop > self.max_hops:
            raise RuntimeError(f"Message exceeded max_hops={self.max_hops}.")
        self._queue.append(message)
        self._transcript.append(message)

    def next_message(self) -> Message | None:
        return self._queue.popleft() if self._queue else None

    @property
    def transcript(self) -> tuple[Message, ...]:
        return tuple(self._transcript)
