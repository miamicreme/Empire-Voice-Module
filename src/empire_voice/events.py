"""Event builders for Empire Voice handoffs."""

from __future__ import annotations

from hashlib import sha1

from .contracts import EmpireOSCommand, MemoryEvent, ToolCallRequest, VoiceIntent


def build_empireos_command(intent: VoiceIntent) -> EmpireOSCommand:
    """Build a simple EmpireOS command from a voice intent."""

    digest = sha1((intent.intent_id + intent.normalized_intent).encode("utf-8")).hexdigest()[:12]
    return EmpireOSCommand(
        command_id=f"cmd_{digest}",
        source_voice_intent_id=intent.intent_id,
        command_type=_command_type(intent),
        priority="high" if intent.target_module in {"dealflow", "skillforge"} else "medium",
        mission_area=intent.target_module,
        next_best_action=intent.next_action,
        time_horizon="today",
        risk_level="medium",
        confidence=intent.confidence,
        permission_status="not_required",
        target_module=intent.target_module,
        context={"normalized_intent": intent.normalized_intent},
    )


def build_tool_call_request(intent: VoiceIntent, tool_name: str, arguments: dict) -> ToolCallRequest:
    digest = sha1((intent.intent_id + tool_name).encode("utf-8")).hexdigest()[:12]
    high_risk_targets = {"mcp"}
    return ToolCallRequest(
        tool_call_id=f"tool_{digest}",
        source_voice_intent_id=intent.intent_id,
        target=intent.target_module,
        tool_name=tool_name,
        purpose=intent.normalized_intent,
        arguments=arguments,
        permission_required=intent.target_module in high_risk_targets,
        risk_level="medium" if intent.target_module in high_risk_targets else "low",
        sensitivity=intent.sensitivity,
        permission_reason="External tool action requested" if intent.target_module in high_risk_targets else "Read-only or internal action",
    )


def build_memory_event(intent: VoiceIntent, summary: str, reason: str) -> MemoryEvent:
    digest = sha1((intent.intent_id + summary).encode("utf-8")).hexdigest()[:12]
    if intent.sensitivity == "secret":
        return MemoryEvent(
            memory_id=f"mem_{digest}",
            source_voice_intent_id=intent.intent_id,
            memory_type="do_not_store",
            summary="Blocked secret memory candidate",
            sensitivity="secret",
            redaction_status="blocked",
            retention="none",
            reason_to_remember="Secrets must not be stored.",
            tags=["blocked"],
        )
    return MemoryEvent(
        memory_id=f"mem_{digest}",
        source_voice_intent_id=intent.intent_id,
        memory_type="project_note",
        summary=summary,
        sensitivity="private_memory",
        redaction_status=intent.redaction_status,
        retention="90d",
        reason_to_remember=reason,
        tags=[intent.target_module],
    )


def _command_type(intent: VoiceIntent) -> str:
    return {
        "skillforge": "repo_action",
        "dealflow": "deal_action",
        "globalintel": "watch_item",
        "signalbrief": "decision_support",
        "framebrief": "decision_support",
        "dictation": "task_create",
        "mcp": "task_create",
    }.get(intent.target_module, "daily_priority")
