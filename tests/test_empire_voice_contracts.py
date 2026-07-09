from empire_voice.events import build_empireos_command, build_memory_event
from empire_voice.redaction import redact_text, sensitivity_for_text
from empire_voice.router import route_transcript


def test_route_transcript_to_skillforge():
    intent = route_transcript("Empire, audit this repo and make a branch plan")
    assert intent.target_module == "skillforge"
    assert intent.directness == "directed"
    assert intent.action == "create_artifact_or_plan"


def test_route_transcript_to_dealflow():
    intent = route_transcript("Empire, which buyer should I follow up with on this deal?")
    assert intent.target_module == "dealflow"
    assert intent.action == "create_deal_action"


def test_redaction_detects_email():
    redacted, changed = redact_text("Email me at person@example.com")
    assert changed is True
    assert "[REDACTED_EMAIL]" in redacted


def test_secret_sensitivity_blocks_password_memory():
    intent = route_transcript("Empire remember my password is hunter2")
    assert sensitivity_for_text("my password is hunter2") == "secret"
    memory = build_memory_event(intent, "password candidate", "test")
    assert memory.memory_type == "do_not_store"
    assert memory.redaction_status == "blocked"


def test_build_empireos_command():
    intent = route_transcript("Empire, what should I do next today?")
    command = build_empireos_command(intent)
    assert command.source_voice_intent_id == intent.intent_id
    assert command.next_best_action
    assert command.permission_status == "not_required"
