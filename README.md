# Empire Voice Module

**Mobile-first private voice-command layer for EmpireOS, SkillForge, DealFlow, and MiamiCreme AI workflows.**

Empire Voice Module is a from-scratch module blueprint and implementation track for turning a phone-first AI voice assistant into a private command surface for EmpireOS.

It is inspired by the best patterns in local-first assistants: wake-word style activation, conversational awareness, dictation, memory, tool routing, MCP access, screen/browser context, privacy redaction, and local/offline inference. The goal is not just to have a voice bot. The goal is to let Kohron talk to the entire operating system from the phone first, with desktop as a power companion:

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
Empire Voice  = phone-first way Kohron talks to the system
Desktop App   = optional local power executor
Database      = shared command/event backbone
```

Empire Voice should be a private mobile-first voice interface and orchestration layer, not a public product by default.

---

## Mobile-First Rule

The phone is the primary daily command surface.

```text
Phone = capture, command, review, approve, fallback
Desktop = heavy local execution, files, screen/browser, local models, dictation into desktop apps
Database = shared event timeline and command queue
Worker/Fallback = safe lightweight execution when desktop is offline
```

See [`docs/mobile-first-ux.md`](docs/mobile-first-ux.md) and [`docs/sync-and-fallback.md`](docs/sync-and-fallback.md).

---

## Core Capabilities

| Capability | Purpose |
|---|---|
| Mobile Voice UX | Capture commands from phone first |
| Desktop Companion | Execute local/heavy tasks when connected |
| Shared DB Sync | Phone and desktop coordinate through events and queues |
| Offline Outbox | Phone captures commands when offline and syncs later |
| Fallback Worker | Handles safe lightweight actions when desktop is offline |
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
Mobile voice input
  -> local/mobile transcript
  -> sync event
  -> database command queue
  -> fallback policy
  -> desktop claim OR worker fallback OR mobile-safe action
  -> module handoff
  -> result synced back to phone and desktop
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

## Mobile / Desktop Sync

The phone and desktop talk through database-backed events, not direct fragile pairing only.

New sync primitives:

- `DeviceSession`
- `SyncEvent`
- `CommandQueueItem`
- fallback policy selection
- preferred executor selection
- mobile status labels

Contracts:

- [`contracts/device-session.schema.json`](contracts/device-session.schema.json)
- [`contracts/sync-event.schema.json`](contracts/sync-event.schema.json)
- [`contracts/command-queue.schema.json`](contracts/command-queue.schema.json)

The desktop can still connect directly for a better experience, but the phone must remain useful when the desktop is offline.

---

## Setup Wizard

Empire Voice now has a UI-agnostic setup wizard engine. A future CLI, PyQt app, Tauri shell, web onboarding screen, or mobile app can render the same setup session.

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
  mobile-first-ux.md
  module-map.md
  privacy-and-memory.md
  setup-wizard.md
  state-machine.md
  sync-and-fallback.md
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
  device-session.schema.json
  sync-event.schema.json
  command-queue.schema.json

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
  sync.py

tests/
  test_empire_voice_contracts.py
  test_assistant_behavior.py
  test_mobile_sync.py
```

---

## Design Goals

1. **Mobile-first** — the phone must be useful even when desktop is offline.
2. **Local-first where possible** — desktop can run local/private/heavy work when connected.
3. **Database-synced** — mobile and desktop coordinate through durable events and command queues.
4. **Fallback-aware** — each command declares whether mobile, worker, desktop, queue-only, or blocked behavior applies.
5. **Private by default** — no secrets, private memories, or client data should leak into public modules.
6. **Contract-first** — every voice request becomes a structured event.
7. **Module-first** — SkillForge, DealFlow, GlobalIntel, SignalBrief, FrameBrief, and EmpireOS stay separate.
8. **Tool-safe** — MCP and browser control must be permissioned and auditable.
9. **Memory-aware** — save decisions and durable preferences, not random noise.
10. **Action-oriented** — every serious command should end in a next action, artifact, task, or decision.
11. **Setup-driven** — normal users should configure the assistant through a wizard, not hand-edit JSON.
12. **State-machine driven** — runtime behavior should be deterministic and testable.

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
| [`contracts/device-session.schema.json`](contracts/device-session.schema.json) | Mobile, desktop, and worker device presence/capabilities |
| [`contracts/sync-event.schema.json`](contracts/sync-event.schema.json) | Shared event timeline between devices |
| [`contracts/command-queue.schema.json`](contracts/command-queue.schema.json) | DB-backed executable command queue |

---

## Key Docs

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/mobile-first-ux.md`](docs/mobile-first-ux.md)
- [`docs/sync-and-fallback.md`](docs/sync-and-fallback.md)
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

### Daily Command From Phone

```text
"Empire, what should I do next?"
```

Output: `empireos_command` with mission type, priority, next action, and context. If desktop is offline, fallback worker uses last synced priorities.

### Repo Work

```text
"Empire, run SkillForge on this repo and tell me the first branch to fix."
```

Output: SkillForge repo-audit artifact or branch plan. If desktop is offline, queue as desktop-required unless the repo is cloud-accessible.

### DealFlow

```text
"Empire, what deals need attention today?"
```

Output: DealFlow action queue or follow-up mission, using synced deal summaries when desktop is offline.

### GlobalIntel

```text
"Empire, what changed overnight that affects money, markets, or clients?"
```

Output: GlobalIntel watch brief and EmpireOS alert. This can fall back to worker/API if desktop is offline.

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

Mobile sync example:

```python
from empire_voice import build_sync_event, queue_command_from_event

event = build_sync_event(
    event_type="voice_intent",
    source_device_id="phone_1",
    payload={"target_module": "skillforge", "request": "audit repo"},
)
queue_item = queue_command_from_event(event, target_module="skillforge", desktop_online=False)
print(queue_item.fallback_policy)  # desktop_required
```

---

## Development Status

This branch now defines the module plan, contracts, setup wizard, state machine, permission gate, mobile-first sync layer, fallback policy, and first assistant runtime skeleton.

Next implementation steps:

1. Add Supabase/Postgres schema migrations.
2. Add mobile PWA shell.
3. Add offline outbox persistence.
4. Add desktop companion heartbeat/claim loop.
5. Add fallback worker.
6. Add contract validators against JSON schemas.
7. Add CLI setup wizard wrapper.
8. Add local config load/save with migration support.
9. Add microphone/STT adapter interface.
10. Add TTS adapter interface.
11. Add local memory store.
12. Add MCP server registry and permission UI.
13. Add evals for voice-to-action reliability.
14. Add desktop tray/setup UI.

---

## Important Boundary

This module is intended for private EmpireOS use. Keep private logic, memories, client data, DealFlow scoring, credentials, and personal workflows out of public commits unless intentionally sanitized.
