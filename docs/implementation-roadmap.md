# Implementation Roadmap

This roadmap turns Empire Voice from a Jarvis-inspired fork into a powerful private EmpireOS module.

## Phase 1: Contracts and Boundaries

- Reframe repo around Empire Voice Module.
- Add voice intent contract.
- Add EmpireOS command contract.
- Add memory event contract.
- Add tool call contract.
- Add privacy and memory policy.
- Add module routing map.

## Phase 2: Core Code Skeleton

- Add Python dataclasses for contract events.
- Add redaction utilities.
- Add simple rule-based router.
- Add tests for contract creation and routing.
- Keep code separate under `src/empire_voice/`.

## Phase 3: Voice Intent Layer

- Convert transcript into `VoiceIntent`.
- Add confidence scoring.
- Add wake/directness classification.
- Add follow-up mode.
- Add dictation mode.
- Add stop/pause/resume system controls.

## Phase 4: Tool Router

- Build target selection for:
  - EmpireOS,
  - SkillForge,
  - DealFlow,
  - GlobalIntel,
  - SignalBrief,
  - FrameBrief,
  - MCP tools,
  - Dictation.
- Add permission levels.
- Add audit logs.

## Phase 5: Memory Gate

- Add redaction before memory.
- Add sensitivity mode.
- Save distilled memory events only.
- Add user confirmation for sensitive durable memory.
- Add tests for secret rejection.

## Phase 6: EmpireOS Adapter

- Convert `VoiceIntent` into `EmpireOSCommand`.
- Add mission creation output.
- Add task creation output.
- Add daily priority output.
- Add decision support output.

## Phase 7: Module Handoffs

- SkillForge handoff: voice to spec/plan/audit/artifact.
- DealFlow handoff: voice to deal action or follow-up.
- GlobalIntel handoff: voice to watch brief or alert.
- SignalBrief handoff: voice to market/social research request.
- FrameBrief handoff: voice to video analysis request.

## Phase 8: Evals

Create tests/evals for:

- wake/directness detection,
- transcript normalization,
- routing accuracy,
- redaction,
- memory gate,
- permission gate,
- EmpireOS command creation,
- MCP tool selection,
- refusal/block behavior.

## Phase 9: Desktop Experience

- Tray app.
- Push-to-talk.
- Dictation overlay.
- Voice command log.
- Memory review panel.
- Tool permission confirmation dialog.
- Setup wizard.

## Phase 10: Production Hardening

- Local encrypted memory store.
- Secure config management.
- Backup/restore.
- Cross-platform packaging.
- Model selection UI.
- Performance timing.
- Crash recovery.
- Private telemetry only.

## Build First

The first working slice should be:

```text
Typed transcript -> VoiceIntent -> Router -> EmpireOSCommand JSON
```

This proves the module before spending time on UI, voice models, or packaging.
