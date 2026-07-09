"""State machine primitives for full assistant behavior."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Literal

AssistantState = Literal[
    "idle",
    "listening",
    "transcribing",
    "classifying",
    "routing",
    "confirming",
    "executing",
    "speaking",
    "dictating",
    "blocked",
    "error",
    "interrupted",
]

_ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "idle": {"listening", "dictating"},
    "listening": {"transcribing", "idle", "interrupted"},
    "transcribing": {"classifying", "error"},
    "classifying": {"routing", "blocked", "idle", "error"},
    "routing": {"confirming", "executing", "blocked", "error"},
    "confirming": {"executing", "idle", "blocked"},
    "executing": {"speaking", "idle", "error"},
    "speaking": {"idle", "interrupted"},
    "dictating": {"idle", "error"},
    "blocked": {"idle"},
    "error": {"idle"},
    "interrupted": {"idle"},
}


@dataclass(frozen=True)
class StateTransition:
    previous_state: AssistantState
    next_state: AssistantState
    reason: str
    timestamp: str
    voice_intent_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class AssistantStateMachine:
    """Small deterministic state machine for assistant runtime behavior."""

    def __init__(self) -> None:
        self.state: AssistantState = "idle"
        self.history: list[StateTransition] = []

    def can_transition(self, next_state: AssistantState) -> bool:
        return next_state in _ALLOWED_TRANSITIONS[self.state]

    def transition(
        self,
        next_state: AssistantState,
        reason: str,
        voice_intent_id: str | None = None,
        error: str | None = None,
    ) -> StateTransition:
        if not self.can_transition(next_state):
            raise ValueError(f"Invalid transition: {self.state} -> {next_state}")
        event = StateTransition(
            previous_state=self.state,
            next_state=next_state,
            reason=reason,
            timestamp=datetime.now(timezone.utc).isoformat(),
            voice_intent_id=voice_intent_id,
            error=error,
        )
        self.state = next_state
        self.history.append(event)
        return event

    def reset(self, reason: str = "reset") -> StateTransition:
        if self.state == "idle":
            return StateTransition("idle", "idle", reason, datetime.now(timezone.utc).isoformat())
        return self.transition("idle", reason)
