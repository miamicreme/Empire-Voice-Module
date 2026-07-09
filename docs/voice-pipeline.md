# Voice Pipeline

The voice pipeline converts raw speech into safe structured actions.

## Pipeline

```text
1. Listen
2. Transcribe
3. Detect wake/directness
4. Normalize transcript
5. Add short rolling context
6. Extract intent
7. Redact sensitive data
8. Classify sensitivity
9. Route target module
10. Build contract event
11. Request permission if needed
12. Execute or hand off
13. Log safe audit event
14. Save memory only if allowed
```

## Stages

### 1. Listen

Capture audio locally. Support always-listening, push-to-talk, and hotkey dictation modes.

### 2. Transcribe

Convert audio to text using local speech recognition where possible.

### 3. Wake / Directness Detection

Determine whether the user is addressing Empire Voice.

Possible states:

- `ignored`
- `directed`
- `follow_up`
- `dictation`
- `system_control`

### 4. Rolling Context

Maintain a temporary context window for active discussion.

Do not save rolling context automatically.

### 5. Intent Extraction

Convert transcript into a structured intent:

- target module,
- action verb,
- object,
- urgency,
- confidence,
- missing info.

### 6. Redaction

Remove or mask:

- passwords,
- API keys,
- access tokens,
- SSNs,
- credit cards,
- phone numbers when sensitive,
- email addresses when not needed,
- private client/buyer details.

### 7. Sensitivity Classification

Set one of:

- `ephemeral`
- `private_memory`
- `public_safe`
- `secret`

### 8. Routing

Choose the target:

- EmpireOS,
- SkillForge,
- DealFlow,
- GlobalIntel,
- SignalBrief,
- FrameBrief,
- MCP tool,
- Dictation.

### 9. Permission Gate

Ask before:

- sending messages,
- purchasing,
- deleting,
- posting publicly,
- moving money,
- changing calendars,
- exposing private data,
- controlling browser/system state beyond safe actions.

### 10. Handoff

Create the appropriate event:

- `voice_intent`,
- `empireos_command`,
- `tool_call_request`,
- `memory_event`,
- `dictation_event`.

## Failure Modes

| Failure | Response |
|---|---|
| Low transcription confidence | Ask user to repeat |
| Ambiguous target | Ask a short clarifying question |
| Sensitive content | Keep ephemeral unless user approves memory |
| Tool risk high | Ask permission |
| Missing context | Request required field |
| No useful action | Return summary and one suggested next step |
