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
  -> module handoff
  -> EmpireOS / SkillForge / DealFlow / GlobalIntel action
```

Empire Voice should produce structured events. EmpireOS should decide what they mean privately.

---

## Repository Structure

```text
docs/
  architecture.md
  jarvis-research-notes.md
  module-map.md
  privacy-and-memory.md
  voice-pipeline.md
  mcp-tool-router.md
  empireos-integration.md
  implementation-roadmap.md

contracts/
  voice-intent.schema.json
  empireos-command.schema.json
  memory-event.schema.json
  tool-call.schema.json

src/empire_voice/
  __init__.py
  contracts.py
  redaction.py
  router.py
  events.py

tests/
  test_empire_voice_contracts.py
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

---

## Main Contracts

| Contract | Purpose |
|---|---|
| [`contracts/voice-intent.schema.json`](contracts/voice-intent.schema.json) | Spoken input normalized into an actionable intent |
| [`contracts/empireos-command.schema.json`](contracts/empireos-command.schema.json) | Intent converted into a private EmpireOS mission or command |
| [`contracts/memory-event.schema.json`](contracts/memory-event.schema.json) | Durable memory event with redaction and sensitivity controls |
| [`contracts/tool-call.schema.json`](contracts/tool-call.schema.json) | Safe routed tool request boundary |

---

## Key Docs

- [`docs/architecture.md`](docs/architecture.md)
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

## Development Status

This branch defines the module plan, contracts, and first code skeleton. The next implementation steps are:

1. Build contract validators.
2. Build redaction and sensitivity classification.
3. Build intent event creation from transcript text.
4. Build router decisions for EmpireOS, SkillForge, DealFlow, GlobalIntel, SignalBrief, and FrameBrief.
5. Add local memory event persistence.
6. Add MCP permission gates.
7. Add evals for voice-to-action reliability.

---

## Important Boundary

This module is intended for private EmpireOS use. Keep private logic, memories, client data, DealFlow scoring, credentials, and personal workflows out of public commits unless intentionally sanitized.
