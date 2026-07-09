# MCP Tool Router

Empire Voice should be able to call tools, but only through a controlled routing and permission layer.

## Goal

Let the user speak naturally while preventing unsafe tool use.

```text
"Empire, check GitHub and tell me if the repo is ready to merge."
```

The router should decide:

- target module,
- available tools,
- required permissions,
- whether user confirmation is required,
- what output contract should be returned.

## Router Inputs

- normalized voice intent,
- current active context,
- available MCP tools,
- tool permissions,
- sensitivity level,
- user preferences,
- target module.

## Router Output

```json
{
  "tool_call_id": "string",
  "target": "mcp | skillforge | empireos | dealflow | globalintel | signalbrief | framebrief | dictation",
  "tool_name": "string",
  "purpose": "string",
  "arguments": {},
  "permission_required": true,
  "risk_level": "low | medium | high",
  "sensitivity": "ephemeral | private_memory | public_safe | secret"
}
```

## Permission Levels

| Level | Examples | Confirmation |
|---|---|---|
| Low | Read repo, summarize page, list files | Usually no |
| Medium | Create draft, create task, open browser, query private data | Maybe |
| High | Send email, delete file, spend money, post publicly, modify repo | Always |
| Blocked | Expose secret, commit private data, bypass policy | Never |

## Tool Selection Strategy

1. Filter tools by target module.
2. Remove tools that violate sensitivity policy.
3. Rank by intent match.
4. Ask for confirmation if risk is medium/high.
5. Execute only after permission gate passes.
6. Return structured result.

## Routing Examples

| Voice Intent | Route |
|---|---|
| "Audit this repo" | SkillForge repo audit |
| "Send this email" | Gmail MCP/tool with confirmation |
| "What changed overnight?" | GlobalIntel + EmpireOS alert |
| "Summarize this video" | FrameBrief |
| "What are people saying?" | SignalBrief |
| "Open GitHub" | Browser/system MCP |

## Audit Log

Every tool call should produce a safe audit record:

- timestamp,
- voice intent ID,
- tool selected,
- permission status,
- sensitivity level,
- result summary,
- errors,
- whether memory was updated.

Do not log raw secrets.
