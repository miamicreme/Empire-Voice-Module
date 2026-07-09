"""Contract models for Empire Voice.

These dataclasses are intentionally lightweight so they can be used before the full
voice stack exists. They mirror the JSON contracts in /contracts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Directness = Literal["ignored", "directed", "follow_up", "dictation", "system_control"]
TargetModule = Literal[
    "empireos",
    "skillforge",
    "dealflow",
    "globalintel",
    "signalbrief",
    "framebrief",
    "mcp",
    "dictation",
    "system",
]
Sensitivity = Literal["ephemeral", "private_memory", "public_safe", "secret"]
RedactionStatus = Literal["not_needed", "redacted", "blocked"]
RiskLevel = Literal["low", "medium", "high", "critical"]
Priority = Literal["low", "medium", "high", "urgent"]


@dataclass(frozen=True)
class VoiceIntent:
    """A normalized request created from spoken text."""

    intent_id: str
    transcript: str
    normalized_intent: str
    directness: Directness
    target_module: TargetModule
    action: str
    confidence: float
    sensitivity: Sensitivity
    redaction_status: RedactionStatus
    next_action: str
    entities: dict[str, Any] = field(default_factory=dict)
    missing_information: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EmpireOSCommand:
    """A private command object that EmpireOS can convert into missions/tasks."""

    command_id: str
    source_voice_intent_id: str
    command_type: str
    priority: Priority
    mission_area: str
    next_best_action: str
    time_horizon: Literal["now", "today", "this_week", "this_month", "later"]
    risk_level: RiskLevel
    confidence: float
    permission_status: Literal["not_required", "required", "granted", "denied"]
    target_module: str = "empireos"
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MemoryEvent:
    """A durable memory candidate. Store only after the memory gate passes."""

    memory_id: str
    source_voice_intent_id: str
    memory_type: str
    summary: str
    sensitivity: Sensitivity
    redaction_status: RedactionStatus
    retention: Literal["none", "session", "30d", "90d", "long_term"]
    reason_to_remember: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolCallRequest:
    """A permission-aware request to call a tool, MCP server, or module."""

    tool_call_id: str
    source_voice_intent_id: str
    target: TargetModule
    tool_name: str
    purpose: str
    arguments: dict[str, Any]
    permission_required: bool
    risk_level: Literal["low", "medium", "high", "blocked"]
    sensitivity: Sensitivity
    permission_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
