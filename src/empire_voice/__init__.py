"""Empire Voice Module.

Contract-first voice intent, routing, redaction, setup, sync, and EmpireOS handoff primitives.
"""

from .assistant import EmpireVoiceAssistant
from .config import AssistantConfig, default_config, validate_config
from .contracts import EmpireOSCommand, MemoryEvent, ToolCallRequest, VoiceIntent
from .redaction import redact_text
from .router import route_transcript
from .setup_wizard import SetupWizard, WizardSession
from .sync import (
    CommandQueueItem,
    DeviceSession,
    SyncEvent,
    build_sync_event,
    fallback_policy_for_target,
    mobile_status_label,
    preferred_executor_for_target,
    queue_command_from_event,
)

__all__ = [
    "AssistantConfig",
    "CommandQueueItem",
    "DeviceSession",
    "EmpireOSCommand",
    "EmpireVoiceAssistant",
    "MemoryEvent",
    "SetupWizard",
    "SyncEvent",
    "ToolCallRequest",
    "VoiceIntent",
    "WizardSession",
    "build_sync_event",
    "default_config",
    "fallback_policy_for_target",
    "mobile_status_label",
    "preferred_executor_for_target",
    "queue_command_from_event",
    "redact_text",
    "route_transcript",
    "validate_config",
]
