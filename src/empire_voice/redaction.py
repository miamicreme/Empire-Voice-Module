"""Simple redaction utilities for Empire Voice.

This is intentionally conservative. More patterns can be added as the module
matures. Redaction should happen before logs, memory, or public-safe exports.
"""

from __future__ import annotations

import re

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("[REDACTED_EMAIL]", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("[REDACTED_PHONE]", re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)")),
    ("[REDACTED_SSN]", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("[REDACTED_CARD]", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
    ("[REDACTED_API_KEY]", re.compile(r"\b(?:sk|pk|api|key|token|secret)[-_]?[A-Za-z0-9]{16,}\b", re.IGNORECASE)),
]


def redact_text(text: str) -> tuple[str, bool]:
    """Return redacted text and whether any replacement occurred."""

    redacted = text
    changed = False
    for replacement, pattern in _PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        changed = changed or count > 0
    return redacted, changed


def sensitivity_for_text(text: str) -> str:
    """Classify text sensitivity using conservative pattern checks."""

    redacted, changed = redact_text(text)
    if "[REDACTED_API_KEY]" in redacted or "password" in text.lower():
        return "secret"
    if changed:
        return "private_memory"
    return "ephemeral"
