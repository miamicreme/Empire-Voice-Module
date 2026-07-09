"""Empire Voice Module.

Contract-first voice intent, routing, redaction, setup, and EmpireOS handoff primitives.
"""

from .assistant import EmpireVoiceAssistant
from .config import AssistantConfig, default_config, validate_config
from .contracts import EmpireOSCommand, MemoryEvent, ToolCallRequest, VoiceIntent
from .redaction import redact_text
from .router import route_transcript
from .setup_wizard import SetupWizard, WizardSession

__all__ = [
    "AssistantConfig",
    "EmpireOSCommand",
    "EmpireVoiceAssistant",
    "MemoryEvent",
    "SetupWizard",
    "ToolCallRequest",
    "VoiceIntent",
    "WizardSession",
    "default_config",
    "redact_text",
    "route_transcript",
    "validate_config",
]
