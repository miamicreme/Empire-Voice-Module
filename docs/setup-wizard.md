# Setup Wizard

The setup wizard should make Empire Voice usable without hand-editing config files.

It should verify the local environment, choose safe defaults, configure privacy, and test the first command path.

## Wizard Goals

1. Confirm hardware and OS readiness.
2. Configure microphone and speaker/TTS output.
3. Select local speech recognition settings.
4. Select local model/provider routing settings.
5. Configure wake phrase and push-to-talk.
6. Configure dictation.
7. Configure privacy and memory defaults.
8. Configure MCP and module connections.
9. Run a voice test.
10. Produce a validated `assistant_config` object.

## Wizard Steps

| Step | Purpose | Required? |
|---|---|---|
| Welcome | Explain private local assistant behavior | Yes |
| System Check | Verify OS, Python, microphone, speakers, optional GPU | Yes |
| Audio Input | Select microphone and noise settings | Yes |
| Speech Recognition | Choose local STT backend/model | Yes |
| Wake Behavior | Choose wake phrase, push-to-talk, follow-up window | Yes |
| Voice Output | Choose TTS or silent/text mode | No |
| Dictation | Configure hotkey and paste behavior | No |
| Privacy | Choose memory defaults, redaction, log retention | Yes |
| Modules | Enable EmpireOS, SkillForge, DealFlow, GlobalIntel, SignalBrief, FrameBrief | Yes |
| MCP Tools | Add/approve external tools | No |
| Test Command | Run a local test from transcript to command JSON | Yes |
| Finish | Save config and show next steps | Yes |

## Default Recommended Settings

```json
{
  "assistant_name": "Empire",
  "wake_phrase": "empire",
  "follow_up_window_seconds": 8,
  "default_sensitivity": "ephemeral",
  "memory_default": "ask",
  "tool_permission_default": "ask_for_medium_and_high",
  "dictation_enabled": true,
  "mcp_enabled": false,
  "local_first": true
}
```

## Setup Validation Rules

Setup is complete only when:

- assistant name exists,
- wake phrase exists,
- privacy mode is selected,
- memory policy is selected,
- at least one module target is enabled,
- test transcript produces a valid `voice_intent`,
- risky tool actions require confirmation.

## User Experience

The wizard should use plain language.

Bad:

```text
Configure routing provider for context reduction.
```

Good:

```text
How should Empire choose which tool to use when you speak?
```

## First Test

Use this test during setup:

```text
Empire, what should I do next today?
```

Expected output:

- target module: `empireos`,
- action: `create_empireos_command`,
- sensitivity: `ephemeral`,
- permission: `not_required`.

## Advanced Settings Later

- custom model choices,
- local memory path,
- encrypted store,
- voice clone/TTS choice,
- hotkey editor,
- per-tool permissions,
- startup behavior,
- screen context permissions,
- logging level,
- eval mode.
