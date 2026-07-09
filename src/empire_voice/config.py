"""Configuration model and validation for Empire Voice."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class PrivacyConfig:
    default_sensitivity: Literal["ephemeral", "private_memory", "public_safe"] = "ephemeral"
    memory_default: Literal["never", "ask", "private_only"] = "ask"
    log_retention: Literal["session", "7d", "30d", "90d"] = "session"
    redaction_enabled: bool = True


@dataclass(frozen=True)
class AudioConfig:
    input_device: str = "default"
    output_device: str = "default"
    noise_gate_enabled: bool = True


@dataclass(frozen=True)
class SpeechRecognitionConfig:
    backend: Literal["faster_whisper", "mlx_whisper", "mock"] = "mock"
    model: str = "base.en"
    language: str = "en"


@dataclass(frozen=True)
class VoiceOutputConfig:
    enabled: bool = True
    backend: Literal["piper", "system", "mock", "none"] = "mock"
    voice: str = "default"


@dataclass(frozen=True)
class DictationConfig:
    enabled: bool = True
    hotkey: str = "ctrl+space"


@dataclass(frozen=True)
class ModuleConfig:
    empireos: bool = True
    skillforge: bool = True
    dealflow: bool = True
    globalintel: bool = True
    signalbrief: bool = True
    framebrief: bool = True


@dataclass(frozen=True)
class PermissionConfig:
    medium_risk: Literal["ask", "allow", "block"] = "ask"
    high_risk: Literal["ask", "block"] = "ask"
    blocked_actions: list[str] = field(default_factory=lambda: ["send_money", "delete_files", "post_publicly"])


@dataclass(frozen=True)
class AssistantConfig:
    config_version: str = "0.1.0"
    assistant_name: str = "Empire"
    wake_phrase: str = "empire"
    follow_up_window_seconds: int = 8
    local_first: bool = True
    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    speech_recognition: SpeechRecognitionConfig = field(default_factory=SpeechRecognitionConfig)
    voice_output: VoiceOutputConfig = field(default_factory=VoiceOutputConfig)
    dictation: DictationConfig = field(default_factory=DictationConfig)
    modules: ModuleConfig = field(default_factory=ModuleConfig)
    permissions: PermissionConfig = field(default_factory=PermissionConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_config() -> AssistantConfig:
    """Return safe setup defaults."""

    return AssistantConfig()


def validate_config(config: AssistantConfig) -> list[str]:
    """Return validation errors. Empty list means config is usable."""

    errors: list[str] = []
    if not config.assistant_name.strip():
        errors.append("assistant_name is required")
    if not config.wake_phrase.strip():
        errors.append("wake_phrase is required")
    if config.follow_up_window_seconds < 0 or config.follow_up_window_seconds > 60:
        errors.append("follow_up_window_seconds must be between 0 and 60")
    if not any(asdict(config.modules).values()):
        errors.append("at least one target module must be enabled")
    if config.privacy.redaction_enabled is False:
        errors.append("redaction_enabled should remain true for safe defaults")
    if config.permissions.high_risk == "allow":  # defensive; type excludes this
        errors.append("high risk actions cannot be always allowed")
    return errors
