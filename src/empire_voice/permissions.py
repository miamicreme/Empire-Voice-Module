"""Permission gate for risky assistant actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .contracts import ToolCallRequest

PermissionDecision = Literal["not_required", "required", "blocked"]


@dataclass(frozen=True)
class PermissionResult:
    decision: PermissionDecision
    reason: str


_BLOCKED_KEYWORDS = {
    "send_money",
    "delete_files",
    "post_publicly",
    "share_secret",
    "bypass_policy",
}

_ALWAYS_CONFIRM_KEYWORDS = {
    "send",
    "delete",
    "purchase",
    "buy",
    "post",
    "merge",
    "commit",
    "deploy",
    "move money",
}


def evaluate_permission(tool_call: ToolCallRequest) -> PermissionResult:
    """Return the required permission decision for a tool call."""

    haystack = f"{tool_call.tool_name} {tool_call.purpose} {tool_call.arguments}".lower()
    if tool_call.sensitivity == "secret":
        return PermissionResult("blocked", "Secret-sensitive tool calls are blocked by default.")
    if any(keyword in haystack for keyword in _BLOCKED_KEYWORDS):
        return PermissionResult("blocked", "Action is on the blocked action list.")
    if tool_call.risk_level in {"high", "blocked"}:
        return PermissionResult("required", "High-risk action requires explicit confirmation.")
    if tool_call.permission_required:
        return PermissionResult("required", tool_call.permission_reason or "Tool requested confirmation.")
    if any(keyword in haystack for keyword in _ALWAYS_CONFIRM_KEYWORDS):
        return PermissionResult("required", "Potentially state-changing action requires confirmation.")
    return PermissionResult("not_required", "Read-only or internal action.")
