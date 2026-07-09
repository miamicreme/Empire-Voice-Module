# EmpireOS Integration

Empire Voice should not replace EmpireOS. It should feed EmpireOS clean command events.

## Integration Goal

Turn spoken intent into private EmpireOS missions, priorities, decisions, and AI-team work items.

```text
Voice -> voice_intent -> empireos_command -> EmpireOS mission/task/dashboard
```

## EmpireOS Command Types

| Command Type | Example |
|---|---|
| `daily_priority` | "What should I do next?" |
| `mission_create` | "Make STT prep a mission." |
| `task_create` | "Add follow-up Kevin tomorrow." |
| `decision_support` | "Should I build this module?" |
| `client_prep` | "Prep my STT call." |
| `deal_action` | "What buyer should I call?" |
| `repo_action` | "Make a branch plan." |
| `memory_save` | "Remember this." |
| `watch_item` | "Monitor this risk." |

## Required Fields

An EmpireOS handoff should include:

- command type,
- priority,
- mission area,
- next best action,
- time horizon,
- risk level,
- confidence,
- source voice intent,
- required module,
- permission status.

## Example

```json
{
  "command_type": "daily_priority",
  "priority": "urgent",
  "mission_area": "STT consulting",
  "next_best_action": "Prepare a 30-minute discovery agenda and proposal outline for STT.",
  "time_horizon": "today",
  "risk_level": "medium",
  "confidence": "high",
  "source_voice_intent_id": "voice_123",
  "target_module": "skillforge",
  "permission_status": "not_required"
}
```

## Private Boundary

The public module can define the event shape.

Private EmpireOS owns:

- dashboards,
- memory,
- personal scheduling rules,
- financial context,
- private client data,
- AI team assignments,
- priority scoring,
- private workflows.

## First Integration Milestone

Create a minimal private adapter that accepts `empireos_command` JSON and turns it into:

- mission card,
- task list item,
- daily priority,
- decision note,
- follow-up reminder.
