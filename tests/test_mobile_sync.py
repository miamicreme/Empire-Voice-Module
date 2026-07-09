from empire_voice.sync import (
    DeviceSession,
    build_sync_event,
    fallback_policy_for_target,
    mobile_status_label,
    preferred_executor_for_target,
    queue_command_from_event,
)


def test_mobile_device_session():
    session = DeviceSession(
        device_id="phone_1",
        user_id="kohron",
        device_type="mobile",
        status="online",
        capabilities=["voice_capture", "mobile_safe_actions"],
    )
    assert session.device_type == "mobile"
    assert "voice_capture" in session.capabilities


def test_skillforge_waits_for_desktop_when_desktop_offline():
    event = build_sync_event(
        event_type="voice_intent",
        source_device_id="phone_1",
        payload={"target_module": "skillforge", "request": "audit repo"},
    )
    queue_item = queue_command_from_event(event, target_module="skillforge", desktop_online=False)
    assert queue_item.fallback_policy == "desktop_required"
    assert queue_item.preferred_executor == "mobile" or queue_item.preferred_executor in {"desktop", "worker"}
    assert mobile_status_label(queue_item) == "Waiting for desktop"


def test_globalintel_can_fallback_to_worker():
    assert fallback_policy_for_target("globalintel", desktop_online=False) == "worker_allowed"
    assert preferred_executor_for_target("globalintel", desktop_online=False) == "worker"


def test_empireos_phone_priority_has_fallback():
    event = build_sync_event(
        event_type="voice_intent",
        source_device_id="phone_1",
        payload={"target_module": "empireos", "request": "what should I do next"},
    )
    queue_item = queue_command_from_event(event, target_module="empireos", desktop_online=False)
    assert queue_item.fallback_policy == "worker_allowed"
    assert queue_item.preferred_executor == "worker"


def test_offline_event_label():
    event = build_sync_event(
        event_type="offline_capture",
        source_device_id="phone_1",
        payload={"note": "call STT"},
        status="queued_offline",
    )
    assert mobile_status_label(event) == "Captured offline"
