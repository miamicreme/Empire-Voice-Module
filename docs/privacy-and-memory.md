# Privacy and Memory Model

Empire Voice must be private by default.

The module should treat voice as sensitive until proven otherwise.

## Privacy Modes

| Mode | Meaning | Storage |
|---|---|---|
| `ephemeral` | Used only for the current response | No durable storage |
| `private_memory` | Useful for private EmpireOS memory | Private local store only |
| `public_safe` | Sanitized and safe for examples/artifacts | Export allowed |
| `secret` | Contains credentials or high-risk private data | Never store; redact immediately |

## Memory Types

| Type | Example | Store? |
|---|---|---|
| Preference | "I prefer calls after 2pm" | Yes, private |
| Goal | "Get STT contract" | Yes, private |
| Commitment | "Follow up with buyer tomorrow" | Yes, private |
| Personal fact | "My son is visiting" | Yes, private if useful |
| Secret | API key, password, token | Never |
| Raw transcript | Full conversation audio text | Usually no |
| Client detail | Buyer list, CRM data | Private only, never public |
| Temporary discussion | Background conversation | Ephemeral |

## Memory Gate

Before saving anything, ask:

1. Is this durable?
2. Is this useful later?
3. Is it sensitive?
4. Is it a secret?
5. Does the user expect it to be remembered?
6. Can it be summarized instead of stored raw?

## Redaction Strategy

Redact before logs, memory, or tool routing.

Patterns to handle:

- email addresses,
- phone numbers,
- credit cards,
- SSNs,
- API keys,
- OAuth tokens,
- passwords,
- addresses where not necessary,
- buyer/client names in public-safe mode.

## Memory Event Quality Gate

A memory event is valid only when it has:

- memory type,
- content summary,
- source transcript reference or user confirmation,
- sensitivity level,
- retention recommendation,
- redaction status,
- reason to remember.

## Default Rule

Do not save raw conversations by default.

Save distilled memory events.

Bad:

```text
Save everything Kohron said for the last 15 minutes.
```

Good:

```text
Kohron wants EmpireOS to prioritize STT prep before general product work this week.
```
