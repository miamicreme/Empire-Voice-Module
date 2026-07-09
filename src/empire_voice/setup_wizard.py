"""Setup wizard engine for Empire Voice.

This is UI-agnostic. A CLI, PyQt screen, or web setup wizard can all call this
class and render the same step/session state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from hashlib import sha1
from typing import Any, Literal

from .config import AssistantConfig, default_config, validate_config
from .router import route_transcript

WizardStep = Literal[
    "welcome",
    "system_check",
    "audio_input",
    "speech_recognition",
    "wake_behavior",
    "voice_output",
    "dictation",
    "privacy",
    "modules",
    "mcp_tools",
    "test_command",
    "finish",
]

_STEPS: list[WizardStep] = [
    "welcome",
    "system_check",
    "audio_input",
    "speech_recognition",
    "wake_behavior",
    "voice_output",
    "dictation",
    "privacy",
    "modules",
    "mcp_tools",
    "test_command",
    "finish",
]


@dataclass(frozen=True)
class WizardSession:
    session_id: str
    current_step: WizardStep
    completed_steps: list[WizardStep] = field(default_factory=list)
    status: Literal["not_started", "in_progress", "blocked", "complete"] = "not_started"
    config_draft: AssistantConfig = field(default_factory=default_config)
    validation_errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["config_draft"] = self.config_draft.to_dict()
        return data


class SetupWizard:
    """Deterministic setup wizard state manager."""

    def __init__(self, session: WizardSession | None = None) -> None:
        self.session = session or WizardSession(
            session_id="setup_" + sha1(b"empire-voice-default").hexdigest()[:12],
            current_step="welcome",
        )

    def start(self) -> WizardSession:
        self.session = replace(self.session, status="in_progress", current_step="welcome")
        return self.session

    def complete_step(self, step: WizardStep, updates: dict[str, Any] | None = None) -> WizardSession:
        if step != self.session.current_step:
            raise ValueError(f"Cannot complete {step}; current step is {self.session.current_step}")

        config = self._apply_updates(self.session.config_draft, updates or {})
        completed = list(dict.fromkeys([*self.session.completed_steps, step]))
        errors = validate_config(config)

        next_step = self._next_step(step)
        status = "complete" if next_step == "finish" and step == "finish" else "in_progress"
        if step == "test_command":
            test_errors = self._validate_test_command(config)
            errors.extend(test_errors)
            if test_errors:
                status = "blocked"

        self.session = replace(
            self.session,
            current_step=next_step,
            completed_steps=completed,
            status=status,  # type: ignore[arg-type]
            config_draft=config,
            validation_errors=errors,
        )
        return self.session

    def run_test_command(self, transcript: str = "Empire, what should I do next today?") -> dict[str, Any]:
        intent = route_transcript(transcript, wake_word=self.session.config_draft.wake_phrase)
        return {
            "passed": intent.target_module == "empireos" and intent.action == "create_empireos_command",
            "intent": intent.to_dict(),
        }

    def _next_step(self, step: WizardStep) -> WizardStep:
        index = _STEPS.index(step)
        if index + 1 >= len(_STEPS):
            return "finish"
        return _STEPS[index + 1]

    def _validate_test_command(self, config: AssistantConfig) -> list[str]:
        result = self.run_test_command(f"{config.assistant_name}, what should I do next today?")
        return [] if result["passed"] else ["test command did not route to EmpireOS"]

    def _apply_updates(self, config: AssistantConfig, updates: dict[str, Any]) -> AssistantConfig:
        # Keep this deliberately simple for the first module slice. A UI can build
        # typed config sections and pass them here later.
        allowed_top_level = {"assistant_name", "wake_phrase", "follow_up_window_seconds", "local_first"}
        top_level_updates = {key: value for key, value in updates.items() if key in allowed_top_level}
        return replace(config, **top_level_updates)
