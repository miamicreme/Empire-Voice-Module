"""Mobile-first sync primitives for Empire Voice.

The phone is the primary UX. Desktop is an optional executor. These models create
an event/queue spine that can later be backed by Supabase, SQLite, Postgres, or
another realtime database.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha1
from typing import Any, Literal

DeviceType = Literal["mobile", "desktop", "worker"]
DeviceStatus = Literal["online", "offline", "degraded"]
SyncStatus = Literal["pending", "queued_offline", "claimed", "permission_required", "completed", "failed", "blocked"]
FallbackPolicy = Literal["mobile_safe", "worker_allowed", "desktop_required", "queue_only", "blocked"]
ClaimStatus = Literal["unclaimed", "claimed", "completed", "failed", "blocked"]
Executor = Literal["mobile", "desktop", "worker"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DeviceSession:
    device_id: str
    user_id: str
    device_type: DeviceType
    status: DeviceStatus
    capabilities: list[str]
    last_seen_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SyncEvent:
    event_id: str
    event_type: str
    source_device_id: str
    status: SyncStatus
    payload: dict[str, Any]
    sensitivity: Literal["ephemeral", "private_memory", "public_safe", "secret"]
    created_at: str = field(default_factory=utc_now)
    target_device_id: str | None = None
    updated_at: str | None = None
    attempt: int = 0
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommandQueueItem:
    command_id: str
    source_event_id: str
    target_module: str
    preferred_executor: Executor
    fallback_policy: FallbackPolicy
    claim_status: ClaimStatus
    created_at: str = field(default_factory=utc_now)
    claimed_by_device_id: str | None = None
    updated_at: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_sync_event(
    event_type: str,
    source_device_id: str,
    payload: dict[str, Any],
    sensitivity: Literal["ephemeral", "private_memory", "public_safe", "secret"] = "ephemeral",
    status: SyncStatus = "pending",
) -> SyncEvent:
    seed = f"{event_type}:{source_device_id}:{payload}:{utc_now()}"
    return SyncEvent(
        event_id="evt_" + sha1(seed.encode("utf-8")).hexdigest()[:12],
        event_type=event_type,
        source_device_id=source_device_id,
        status=status,
        payload=payload,
        sensitivity=sensitivity,
    )


def fallback_policy_for_target(target_module: str, desktop_online: bool) -> FallbackPolicy:
    """Decide how a mobile command should be handled if desktop is unavailable."""

    if target_module in {"dictation", "system"}:
        return "mobile_safe"
    if target_module in {"empireos", "globalintel", "signalbrief"}:
        return "worker_allowed" if not desktop_online else "mobile_safe"
    if target_module in {"skillforge", "framebrief", "dealflow"}:
        return "desktop_required" if not desktop_online else "worker_allowed"
    if target_module == "mcp":
        return "desktop_required"
    return "queue_only"


def preferred_executor_for_target(target_module: str, desktop_online: bool) -> Executor:
    if target_module in {"skillforge", "framebrief", "mcp"} and desktop_online:
        return "desktop"
    if target_module in {"empireos", "globalintel", "signalbrief"}:
        return "worker" if not desktop_online else "mobile"
    if target_module == "dealflow":
        return "desktop" if desktop_online else "worker"
    return "mobile"


def queue_command_from_event(event: SyncEvent, target_module: str, desktop_online: bool) -> CommandQueueItem:
    seed = f"{event.event_id}:{target_module}"
    policy = fallback_policy_for_target(target_module, desktop_online)
    return CommandQueueItem(
        command_id="cmdq_" + sha1(seed.encode("utf-8")).hexdigest()[:12],
        source_event_id=event.event_id,
        target_module=target_module,
        preferred_executor=preferred_executor_for_target(target_module, desktop_online),
        fallback_policy=policy,
        claim_status="blocked" if policy == "blocked" else "unclaimed",
        payload=event.payload,
    )


def mobile_status_label(event_or_queue: SyncEvent | CommandQueueItem) -> str:
    """Human-friendly mobile timeline label."""

    status = getattr(event_or_queue, "status", None) or getattr(event_or_queue, "claim_status", None)
    fallback = getattr(event_or_queue, "fallback_policy", None)
    if status == "queued_offline":
        return "Captured offline"
    if fallback == "desktop_required":
        return "Waiting for desktop"
    if status == "claimed":
        return "Desktop is working on it"
    if status == "permission_required":
        return "Needs approval"
    if status == "completed":
        return "Done"
    if status == "failed":
        return "Failed - retry available"
    if status == "blocked":
        return "Blocked for safety"
    return "Working..."
