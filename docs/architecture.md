# Empire Voice Architecture

Empire Voice Module is the private voice-command layer for EmpireOS.

The module converts spoken language into structured, auditable events that can be routed to EmpireOS, SkillForge, DealFlow, GlobalIntel, SignalBrief, FrameBrief, or external MCP tools.

## Architecture Goal

Do not build a toy voice assistant.

Build a local command interface that can drive a private AI operating system.

```text
Microphone / Dictation
  -> Speech recognition
  -> Wake/directness detection
  -> Rolling context
  -> Intent extraction
  -> Redaction
  -> Sensitivity classification
  -> Tool/module router
  -> Contracted event
  -> EmpireOS / SkillForge / DealFlow / GlobalIntel / MCP
```

## Major Components

| Component | Responsibility |
|---|---|
| Listener | Captures audio and detects speech boundaries |
| Wake Detector | Decides whether the assistant was addressed |
| Transcript Buffer | Maintains short rolling discussion context |
| Intent Extractor | Converts transcript into structured intent |
| Redaction Layer | Removes sensitive values before storage/logging |
| Sensitivity Classifier | Decides whether content can be saved, routed, or must remain ephemeral |
| Router | Chooses the target module or tool |
| Memory Gate | Decides what becomes durable memory |
| MCP Gateway | Connects to external tools under permission controls |
| EmpireOS Adapter | Converts voice intent into missions, priorities, and next actions |
| SkillForge Adapter | Converts voice intent into specs, plans, audits, recipes, and artifacts |
| DealFlow Adapter | Converts voice intent into deal actions and follow-ups |
| GlobalIntel Adapter | Converts voice intent into risk/watch requests |

## Module Boundaries

### Empire Voice Owns

- local voice interaction,
- transcript events,
- intent extraction,
- redaction,
- tool-routing decisions,
- voice-to-module contracts,
- dictation boundary,
- MCP permission gates.

### Empire Voice Does Not Own

- private EmpireOS dashboard rendering,
- DealFlow proprietary scoring,
- SkillForge recipe internals,
- GlobalIntel source ingestion,
- SignalBrief search logic,
- FrameBrief video runtime,
- client data storage,
- personal financial logic.

## Event-First Design

Every meaningful voice request should become one of these events:

| Event | Meaning |
|---|---|
| `voice_intent` | A normalized request from speech |
| `empireos_command` | A private mission/priority/action request |
| `memory_event` | A durable fact, preference, commitment, or decision |
| `tool_call_request` | A request to use a tool/MCP/server/module |
| `dictation_event` | Text-only output to active app |
| `system_control_event` | Stop, pause, resume, mute, or settings action |

## Routing Targets

| Target | Use When |
|---|---|
| `empireos` | User asks what to do, wants a priority, mission, decision, or personal command |
| `skillforge` | User wants a plan, repo audit, spec, proposal, or implementation task |
| `dealflow` | User asks about deals, buyer follow-up, underwriting, opportunity, or next action |
| `globalintel` | User asks what changed globally, market risk, country risk, energy, aviation, or infrastructure |
| `signalbrief` | User asks what people are saying, market chatter, customer pain, trend, or competitor signal |
| `framebrief` | User asks about video, demo, ad, screen recording, or visual proof |
| `mcp` | User asks to operate a connected tool |
| `dictation` | User wants text pasted into the active app |

## Safety Model

Use three sensitivity modes:

| Mode | Meaning | Storage |
|---|---|---|
| `ephemeral` | Use only during current turn | Do not store |
| `private_memory` | Save only inside private EmpireOS memory | Private store only |
| `public_safe` | Can become sanitized artifact or public example | Safe to export |

Default to `ephemeral` unless the user explicitly wants memory or the event is clearly useful and non-sensitive.

## Quality Gate

A voice event is not ready to execute unless it has:

- transcript,
- normalized intent,
- target module,
- confidence,
- sensitivity level,
- redaction status,
- next action,
- permission status for tool use.
