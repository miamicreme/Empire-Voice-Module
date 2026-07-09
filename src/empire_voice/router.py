"""Rule-based first-pass router for Empire Voice.

This creates a usable spine before any model-based router is added. Later, an LLM
or embedding router can replace the keyword rules while preserving the contract.
"""

from __future__ import annotations

from hashlib import sha1

from .contracts import VoiceIntent
from .redaction import redact_text, sensitivity_for_text

_TARGET_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("skillforge", ("repo", "code", "branch", "audit", "spec", "plan", "build", "ship")),
    ("dealflow", ("deal", "buyer", "seller", "loi", "offer", "underwrite", "follow up")),
    ("globalintel", ("global", "overnight", "market", "country", "risk", "energy", "aviation", "infrastructure")),
    ("signalbrief", ("people are saying", "trend", "competitor", "customer pain", "market chatter")),
    ("framebrief", ("video", "youtube", "demo", "screen recording", "watch this", "ad")),
    ("dictation", ("dictate", "type this", "paste this", "write this down")),
    ("mcp", ("open", "click", "browser", "github", "gmail", "calendar", "slack")),
]


def route_transcript(transcript: str, wake_word: str = "empire") -> VoiceIntent:
    """Convert a transcript into a first-pass VoiceIntent."""

    raw = transcript.strip()
    lowered = raw.lower()
    redacted, was_redacted = redact_text(raw)
    sensitivity = sensitivity_for_text(raw)

    if wake_word.lower() in lowered:
        directness = "directed"
    elif lowered.startswith(("what should i", "can you", "please")):
        directness = "directed"
    else:
        directness = "follow_up"

    target = "empireos"
    for candidate, keywords in _TARGET_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            target = candidate
            break

    if "stop" in lowered or "pause" in lowered or "resume" in lowered:
        target = "system"
        directness = "system_control"

    action = _infer_action(lowered, target)
    intent_id = "voice_" + sha1(raw.encode("utf-8")).hexdigest()[:12]

    return VoiceIntent(
        intent_id=intent_id,
        transcript=redacted,
        normalized_intent=redacted.replace(wake_word, "").strip(),
        directness=directness,  # type: ignore[arg-type]
        target_module=target,  # type: ignore[arg-type]
        action=action,
        confidence=0.72,
        sensitivity=sensitivity,  # type: ignore[arg-type]
        redaction_status="redacted" if was_redacted else "not_needed",
        next_action=_next_action_for(target),
        entities={},
        missing_information=[],
    )


def _infer_action(text: str, target: str) -> str:
    if target == "dictation":
        return "dictate_text"
    if target == "skillforge":
        return "create_artifact_or_plan"
    if target == "dealflow":
        return "create_deal_action"
    if target == "globalintel":
        return "create_global_watch_brief"
    if target == "signalbrief":
        return "create_signal_research_request"
    if target == "framebrief":
        return "create_video_brief_request"
    if target == "mcp":
        return "route_tool_request"
    if target == "system":
        return "system_control"
    if "remember" in text:
        return "save_memory"
    return "create_empireos_command"


def _next_action_for(target: str) -> str:
    return {
        "empireos": "Create an EmpireOS command with priority, mission area, and next best action.",
        "skillforge": "Create a SkillForge handoff for spec, plan, audit, or artifact generation.",
        "dealflow": "Create a DealFlow action request with deal context and next action.",
        "globalintel": "Create a GlobalIntel watch or risk brief request.",
        "signalbrief": "Create a SignalBrief research request.",
        "framebrief": "Create a FrameBrief video analysis request.",
        "mcp": "Create a permission-aware tool call request.",
        "dictation": "Return text to active app without saving memory.",
        "system": "Execute safe system control or ask for confirmation.",
    }.get(target, "Ask a clarifying question.")
