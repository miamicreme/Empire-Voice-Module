"""Assistant runtime orchestrator.

This is the first full-assistant behavior spine: transcript in, structured result out.
A later desktop app can plug microphone/STT/TTS/UI into this runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .config import AssistantConfig, default_config
from .events import build_empireos_command, build_tool_call_request
from .permissions import evaluate_permission
from .router import route_transcript
from .state import AssistantStateMachine

TurnStatus = Literal["answered", "routed", "permission_required", "blocked", "error"]


@dataclass(frozen=True)
class AssistantTurnResult:
    status: TurnStatus
    message: str
    intent: dict[str, Any] | None = None
    empireos_command: dict[str, Any] | None = None
    tool_call: dict[str, Any] | None = None
    permission: dict[str, Any] | None = None
    transitions: list[dict[str, Any]] | None = None


class EmpireVoiceAssistant:
    """UI-agnostic assistant runtime."""

    def __init__(self, config: AssistantConfig | None = None) -> None:
        self.config = config or default_config()
        self.state_machine = AssistantStateMachine()

    def handle_transcript(self, transcript: str) -> AssistantTurnResult:
        """Handle a transcript as if it came from STT or typed test input."""

        try:
            self.state_machine.transition("listening", "transcript received")
            self.state_machine.transition("transcribing", "using provided transcript")
            self.state_machine.transition("classifying", "classifying directness and sensitivity")

            intent = route_transcript(transcript, wake_word=self.config.wake_phrase)
            if intent.redaction_status == "blocked" or intent.sensitivity == "secret":
                self.state_machine.transition("blocked", "secret or blocked content", intent.intent_id)
                self.state_machine.transition("idle", "blocked turn complete")
                return AssistantTurnResult(
                    status="blocked",
                    message="I will not store or route that because it appears sensitive. I can use it ephemerally if you confirm the safe action.",
                    intent=intent.to_dict(),
                    transitions=[item.to_dict() for item in self.state_machine.history],
                )

            self.state_machine.transition("routing", "routing intent", intent.intent_id)

            if intent.target_module == "mcp":
                tool_call = build_tool_call_request(intent, tool_name="mcp_router", arguments={"transcript": intent.normalized_intent})
                permission = evaluate_permission(tool_call)
                if permission.decision == "blocked":
                    self.state_machine.transition("blocked", permission.reason, intent.intent_id)
                    self.state_machine.transition("idle", "blocked tool call complete")
                    return AssistantTurnResult(
                        status="blocked",
                        message=permission.reason,
                        intent=intent.to_dict(),
                        tool_call=tool_call.to_dict(),
                        permission=permission.__dict__,
                        transitions=[item.to_dict() for item in self.state_machine.history],
                    )
                if permission.decision == "required":
                    self.state_machine.transition("confirming", permission.reason, intent.intent_id)
                    return AssistantTurnResult(
                        status="permission_required",
                        message=f"I can do that, but I need confirmation first: {permission.reason}",
                        intent=intent.to_dict(),
                        tool_call=tool_call.to_dict(),
                        permission=permission.__dict__,
                        transitions=[item.to_dict() for item in self.state_machine.history],
                    )

            self.state_machine.transition("executing", "building EmpireOS command", intent.intent_id)
            command = build_empireos_command(intent)
            self.state_machine.transition("speaking", "turn response ready", intent.intent_id)
            self.state_machine.transition("idle", "turn complete")

            return AssistantTurnResult(
                status="routed",
                message=self._voice_summary(intent.target_module, command.next_best_action),
                intent=intent.to_dict(),
                empireos_command=command.to_dict(),
                transitions=[item.to_dict() for item in self.state_machine.history],
            )
        except Exception as exc:  # pragma: no cover - defensive runtime guard
            try:
                self.state_machine.transition("error", "runtime exception", error=str(exc))
                self.state_machine.transition("idle", "error handled")
            except Exception:
                pass
            return AssistantTurnResult(
                status="error",
                message="Something went wrong while handling that command. Try again or simplify the request.",
                transitions=[item.to_dict() for item in self.state_machine.history],
            )

    def _voice_summary(self, target_module: str, next_action: str) -> str:
        return f"Routed to {target_module}. Next action: {next_action}"
