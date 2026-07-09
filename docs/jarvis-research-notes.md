# Jarvis Research Notes

These notes capture useful design lessons from local-first AI voice assistant patterns and the Jarvis repository that inspired this module direction.

## Useful Ideas To Recreate From Scratch

| Pattern | Why It Matters For Empire Voice |
|---|---|
| Local-first processing | Keeps private speech, memory, and commands under user control |
| Natural wake phrase placement | Lets the user say the assistant name anywhere in the sentence |
| Rolling context | Supports "what do you think?" inside a live discussion |
| Echo detection | Prevents the assistant from responding to itself |
| Dictation mode | Turns the module into a practical daily input tool |
| MCP integration | Allows voice to operate many external systems |
| Tool routing | Avoids dumping every available tool into every model call |
| Memory graph | Lets the assistant learn preferences, facts, decisions, and goals |
| Redaction before storage | Reduces the risk of saving secrets or sensitive information |
| Evals | Makes voice intent, routing, and memory behavior measurable |
| Setup wizard | Makes local models and speech settings easier to configure |

## What To Improve For EmpireOS

Jarvis-style assistants are general personal assistants. Empire Voice should be more mission-focused.

Improve around:

- EmpireOS mission creation,
- SkillForge artifact creation,
- DealFlow action routing,
- GlobalIntel daily risk/watch briefing,
- explicit privacy modes,
- task/mission handoff contracts,
- daily command center integration,
- ranked next-best-action output,
- confidence and risk scoring,
- module-level audit logs.

## What Not To Copy Blindly

Do not make Empire Voice just a desktop toy.

Avoid:

- saving every conversation by default,
- routing every request to all tools,
- mixing private EmpireOS data into generic assistant code,
- weak permission gates for browser/system actions,
- hidden memory writes,
- unclear tool execution logs,
- vague answers without next actions.

## Empire Voice Differentiator

The differentiator is not voice alone.

The differentiator is voice-to-operating-system command:

```text
spoken intent -> structured event -> private decision -> module action -> verified output
```

## Feature Priority

1. Voice intent contract.
2. Redaction and sensitivity classification.
3. EmpireOS command handoff.
4. SkillForge artifact handoff.
5. MCP tool router.
6. Memory gate.
7. Dictation.
8. Screen/browser context boundary.
9. Evals.
10. Desktop UI and setup wizard.
