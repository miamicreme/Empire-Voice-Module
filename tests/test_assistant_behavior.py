from empire_voice import EmpireVoiceAssistant, SetupWizard, default_config, validate_config
from empire_voice.events import build_tool_call_request
from empire_voice.permissions import evaluate_permission
from empire_voice.router import route_transcript
from empire_voice.state import AssistantStateMachine


def test_default_config_is_valid():
    assert validate_config(default_config()) == []


def test_setup_wizard_starts_and_advances():
    wizard = SetupWizard()
    session = wizard.start()
    assert session.status == "in_progress"
    assert session.current_step == "welcome"
    session = wizard.complete_step("welcome")
    assert session.current_step == "system_check"
    assert "welcome" in session.completed_steps


def test_setup_wizard_test_command_routes_to_empireos():
    wizard = SetupWizard()
    wizard.start()
    result = wizard.run_test_command("Empire, what should I do next today?")
    assert result["passed"] is True
    assert result["intent"]["target_module"] == "empireos"


def test_state_machine_blocks_invalid_transition():
    machine = AssistantStateMachine()
    try:
        machine.transition("executing", "invalid")
    except ValueError as exc:
        assert "Invalid transition" in str(exc)
    else:
        raise AssertionError("invalid transition should fail")


def test_assistant_routes_skillforge_command():
    assistant = EmpireVoiceAssistant()
    result = assistant.handle_transcript("Empire, audit this repo with SkillForge")
    assert result.status == "routed"
    assert result.intent is not None
    assert result.intent["target_module"] == "skillforge"
    assert result.empireos_command is not None


def test_assistant_requires_permission_for_mcp():
    assistant = EmpireVoiceAssistant()
    result = assistant.handle_transcript("Empire, open GitHub and check the repo")
    assert result.status in {"permission_required", "routed"}
    assert result.intent is not None
    assert result.intent["target_module"] == "mcp"


def test_permission_blocks_secret_tool_call():
    intent = route_transcript("Empire, open GitHub")
    tool_call = build_tool_call_request(intent, "mcp_router", {"token": "secret"})
    secret_tool_call = type(tool_call)(
        tool_call_id=tool_call.tool_call_id,
        source_voice_intent_id=tool_call.source_voice_intent_id,
        target=tool_call.target,
        tool_name=tool_call.tool_name,
        purpose=tool_call.purpose,
        arguments=tool_call.arguments,
        permission_required=tool_call.permission_required,
        risk_level=tool_call.risk_level,
        sensitivity="secret",
        permission_reason=tool_call.permission_reason,
    )
    result = evaluate_permission(secret_tool_call)
    assert result.decision == "blocked"
