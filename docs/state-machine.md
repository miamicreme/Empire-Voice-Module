# Assistant State Machine

Empire Voice should be state-machine driven so behavior is predictable, testable, and safe.

## States

```text
idle
  -> listening
  -> transcribing
  -> classifying
  -> routing
  -> confirming
  -> executing
  -> speaking
  -> idle
```

Alternate flows:

```text
listening -> dictating -> idle
routing -> blocked -> idle
executing -> error -> idle
speaking -> interrupted -> idle
```

## State Definitions

| State | Meaning | Allowed Next States |
|---|---|---|
| `idle` | Waiting for wake phrase or hotkey | listening, dictating |
| `listening` | Capturing speech | transcribing, idle |
| `transcribing` | Converting audio to text | classifying, error |
| `classifying` | Detecting directness and sensitivity | routing, blocked, idle |
| `routing` | Choosing module/tool | confirming, executing, blocked, error |
| `confirming` | Waiting for permission | executing, idle, blocked |
| `executing` | Running command/tool/handoff | speaking, error, idle |
| `speaking` | Responding with TTS/text | idle, interrupted |
| `dictating` | Pasting text into active app | idle, error |
| `blocked` | Action refused or unsafe | idle |
| `error` | Recoverable failure | idle |
| `interrupted` | User stopped assistant speech/action | idle |

## Transition Guards

| Guard | Purpose |
|---|---|
| `has_transcript` | Do not classify empty input |
| `is_directed` | Do not route background conversation |
| `redaction_complete` | Do not store/log before redaction |
| `permission_granted` | Do not execute risky actions without approval |
| `memory_gate_passed` | Do not write memory unless safe |
| `tool_available` | Do not route to missing tools |

## Runtime Contract

Every state transition should record:

- previous state,
- next state,
- reason,
- timestamp,
- voice intent ID if available,
- error if any.

Do not record raw secrets.

## Best Practice

Business logic should not be spread through UI callbacks.

The UI should call the runtime state machine. The runtime state machine should call contracts, router, permission gate, and adapters.
