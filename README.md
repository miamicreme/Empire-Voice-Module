# Empire Voice Module

**Private local voice-command layer for EmpireOS, SkillForge, DealFlow, and MiamiCreme AI workflows.**

Empire Voice Module is a from-scratch module blueprint and implementation track for turning a local AI voice assistant into a private command surface for EmpireOS.

It is inspired by the best patterns in local-first assistants: wake-word style activation, conversational awareness, dictation, memory, tool routing, MCP access, screen/browser context, privacy redaction, and local/offline inference. The goal is not just to have a voice bot. The goal is to let Kohron talk to the entire operating system:

```text
"Empire, what should I do next?"
"Empire, prep my STT call."
"Empire, audit this repo with SkillForge."
"Empire, turn this video into a FrameBrief."
"Empire, check what changed overnight from GlobalIntel."
"Empire, which DealFlow opportunity needs attention today?"
```

---

## Module Position

```text
SignalBrief   = what people are saying
FrameBrief    = what videos show
GlobalIntel   = what is happening globally
SkillForge    = turns intelligence into plans, artifacts, and delivery gates
DealFlow      = deal intelligence and next actions
EmpireOS      = private command center and AI executive team
Empire Voice  = how Kohron talks to the system
```

Empire Voice should be a private voice interface and orchestration layer, not a public product by default.

---

## Core Capabilities

| Capability | Purpose |
|---|---|
| Voice Intent Capture | Convert spoken requests into structured commands |
| Wake Phrase / Directed Speech | Detect when the assistant is being addressed |
| Rolling Conversation Context | Understand "what do you think?" inside a discussion |
| Local Dictation | Speak into any app privately |
| Memory Events | Save useful facts, preferences, decisions, and commitments |
| Redaction | Strip sensitive data before storage or logging |
| Tool Router | Choose the right tool or module without context bloat |
| MCP Gateway | Connect to external tools through MCP boundaries |
| Permission Gate | Require confirmation before risky actions |
| Setup Wizard | Configure assistant, audio, privacy, modules, tools, and test command path |
| Runtime State Machine | Keep behavior predictable, interruptible, and testable |
| EmpireOS Handoff | Convert voice intent into missions, priorities, and AI-team tasks |
| SkillForge Handoff | Convert voice intent into specs, plans, audits, recipes, and artifacts |
| DealFlow Handoff | Convert voice intent into deal actions, buyer follow-ups, and risk checks |
| GlobalIntel Handoff | Convert global signals into watch items and alerts |
| Screen/Browser Context Boundary | Use visible context without leaking private data |

---

## First Architecture Rule

Keep the assistant brain separate from the private operating system.

```text
Voice input
  -> local transcript
  -> intent event
  -> redaction
  -> router
  -> permission gate
  -> assistant state machine
  -> module handoff
  -> EmpireOS / SkillForge / DealFlow / GlobalIntel action
```

Empire Voice should produce structured events. EmpireOS should decide what they mean privately.

---

## Full Assistant Behavior

Empire Voice now has a documented runtime behavior model:

- predictable assistant modes,
- wake/follow-up behavior,
- interruptibility,
- permission-required actions,
- memory rules,
- error recovery,
- done criteria.

See [`docs/assistant-behavior.md`](docs/assistant-behavior.md) and [`docs/state-machine.md`](docs/state-machine.md).

The first runtime implementation is `EmpireVoiceAssistant`, which accepts a transcript and returns a structured turn result with:

- status,
- message,
- voice intent,
- EmpireOS command,
- optional tool call,
- optional permission result,
- state transitions.

---

## Setup Wizard

Empire Voice now has a UI-agnostic setup wizard engine. A future CLI, PyQt app, Tauri shell, or web onboarding screen can render the same setup session.

Wizard steps:

1. Welcome
2. System Check
3. Audio Input
4. Speech Recognition
5. Wake Behavior
6. Voice Output
7. Dictation
8. Privacy
9. Modules
10. MCP Tools
11. Test Command
12. Finish

See [`docs/setup-wizard.md`](docs/setup-wizard.md), [`docs/configuration.md`](docs/configuration.md), [`contracts/assistant-config.schema.json`](contracts/assistant-config.schema.json), and [`contracts/setup-wizard.schema.json`](contracts/setup-wizard.schema.json).

---

## Repository Structure

```text
docs/
  architecture.md
  assistant-behavior.md
  configuration.md
  jarvis-research-notes.md
  module-map.md
  privacy-and-memory.md
  setup-wizard.md
  state-machine.md
  voice-pipeline.md
  mcp-tool-router.md
  empireos-integration.md
  implementation-roadmap.md

contracts/
  voice-intent.schema.json
  empireos-command.schema.json
  memory-event.schema.json
  tool-call.schema.json
  assistant-config.schema.json
  setup-wizard.schema.json

src/empire_voice/
  __init__.py
  assistant.py
  config.py
  contracts.py
  events.py
  permissions.py
  redaction.py
  router.py
  setup_wizard.py
  state.py

tests/
  test_empire_voice_contracts.py
  test_assistant_behavior.py
```

---

## Design Goals

1. **Local-first** — voice, memory, and routing should work locally where possible.
2. **Private by default** — no secrets, private memories, or client data should leak into public modules.
3. **Contract-first** — every voice request becomes a structured event.
4. **Module-first** — SkillForge, DealFlow, GlobalIntel, SignalBrief, FrameBrief, and EmpireOS stay separate.
5. **Tool-safe** — MCP and browser control must be permissioned and auditable.
6. **Memory-aware** — save decisions and durable preferences, not random noise.
7. **Action-oriented** — every serious command should end in a next action, artifact, task, or decision.
8. **Setup-driven** — normal users should configure the assistant through a wizard, not hand-edit JSON.
9. **State-machine driven** — runtime behavior should be deterministic and testable.

---

## Main Contracts

| Contract | Purpose |
|---|---|
| [`contracts/voice-intent.schema.json`](contracts/voice-intent.schema.json) | Spoken input normalized into an actionable intent |
| [`contracts/empireos-command.schema.json`](contracts/empireos-command.schema.json) | Intent converted into a private EmpireOS mission or command |
| [`contracts/memory-event.schema.json`](contracts/memory-event.schema.json) | Durable memory event with redaction and sensitivity controls |
| [`contracts/tool-call.schema.json`](contracts/tool-call.schema.json) | Safe routed tool request boundary |
| [`contracts/assistant-config.schema.json`](contracts/assistant-config.schema.json) | Validated assistant configuration |
| [`contracts/setup-wizard.schema.json`](contracts/setup-wizard.schema.json) | Setup wizard session state |

---

## Key Docs

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/assistant-behavior.md`](docs/assistant-behavior.md)
- [`docs/setup-wizard.md`](docs/setup-wizard.md)
- [`docs/state-machine.md`](docs/state-machine.md)
- [`docs/configuration.md`](docs/configuration.md)
- [`docs/voice-pipeline.md`](docs/voice-pipeline.md)
- [`docs/mcp-tool-router.md`](docs/mcp-tool-router.md)
- [`docs/privacy-and-memory.md`](docs/privacy-and-memory.md)
- [`docs/empireos-integration.md`](docs/empireos-integration.md)
- [`docs/implementation-roadmap.md`](docs/implementation-roadmap.md)
- [`docs/jarvis-research-notes.md`](docs/jarvis-research-notes.md)

---

## Use Cases

### Daily Command

```text
"Empire, what should I do next?"
```

Output: `empireos_command` with mission type, priority, next action, and context.

### Repo Work

```text
"Empire, run SkillForge on this repo and tell me the first branch to fix."
```

Output: SkillForge repo-audit artifact or branch plan.

### DealFlow

```text
"Empire, what deals need attention today?"
```

Output: DealFlow action queue or follow-up mission.

### GlobalIntel

```text
"Empire, what changed overnight that affects money, markets, or clients?"
```

Output: GlobalIntel watch brief and EmpireOS alert.

### Dictation

```text
Hold hotkey -> speak -> release -> paste clean text into active app.
```

Output: local text, no memory save unless explicitly requested.

---

## First Working Slice

```python
from empire_voice import EmpireVoiceAssistant

assistant = EmpireVoiceAssistant()
result = assistant.handle_transcript("Empire, audit this repo with SkillForge")
print(result.status)
print(result.intent)
print(result.empireos_command)
```

---

## Development Status

This branch now defines the module plan, contracts, setup wizard, state machine, permission gate, and first assistant runtime skeleton.

Next implementation steps:

1. Add contract validators against JSON schemas.
2. Add CLI setup wizard wrapper.
3. Add local config load/save with migration support.
4. Add microphone/STT adapter interface.
5. Add TTS adapter interface.
6. Add local memory store.
7. Add MCP server registry and permission UI.
8. Add evals for voice-to-action reliability.
9. Add desktop tray/setup UI.

---

## Important Boundary

This module is intended for private EmpireOS use. Keep private logic, memories, client data, DealFlow scoring, credentials, and personal workflows out of public commits unless intentionally sanitized.
