# Sync and Fallback Design

Empire Voice needs a shared event backbone so phone and desktop can talk through a database.

The database should not be treated as just storage. It is the command bus, sync layer, event timeline, offline queue, and device coordination system.

## Core Architecture

```text
Mobile App
  -> local outbox
  -> cloud database / realtime channel
  -> command queue
  -> desktop companion claims executable work
  -> fallback worker handles safe work when desktop is offline
  -> results sync back to DB
  -> mobile and desktop timelines update
```

## Recommended Backend Shape

Start with a hosted database that supports:

- authentication,
- row-level security,
- realtime subscriptions,
- offline-friendly IDs,
- server functions/workers,
- audit log tables.

Good fit:

```text
Supabase Postgres + Realtime + Edge Functions
```

This does not force Supabase forever. The important part is the contract:

```text
device_sessions
sync_events
command_queue
assistant_results
offline_outbox
permission_requests
```

## Tables

### `device_sessions`

Tracks phones, desktops, and fallback workers.

| Field | Purpose |
|---|---|
| `device_id` | Stable device ID |
| `user_id` | Owner |
| `device_type` | mobile, desktop, worker |
| `status` | online, offline, degraded |
| `capabilities` | what this device can execute |
| `last_seen_at` | heartbeat |

### `sync_events`

Append-only event timeline.

| Field | Purpose |
|---|---|
| `event_id` | Unique event |
| `event_type` | voice_intent, command, result, permission, heartbeat |
| `source_device_id` | who created it |
| `target_device_id` | optional device target |
| `status` | pending, claimed, completed, failed, queued_offline |
| `payload` | structured event payload |
| `sensitivity` | ephemeral, private_memory, public_safe, secret |
| `created_at` | event time |

### `command_queue`

Executable command queue derived from sync events.

| Field | Purpose |
|---|---|
| `command_id` | Command ID |
| `source_event_id` | Origin event |
| `target_module` | empireos, skillforge, dealflow, globalintel, etc. |
| `preferred_executor` | desktop, mobile, worker |
| `fallback_policy` | mobile_safe, desktop_required, worker_allowed, queue_only |
| `claim_status` | unclaimed, claimed, completed, failed |
| `claimed_by_device_id` | executor |

### `assistant_results`

Stores safe result summaries.

| Field | Purpose |
|---|---|
| `result_id` | Result ID |
| `command_id` | Command |
| `summary` | Safe user-facing result |
| `artifact_ref` | optional linked artifact |
| `next_action` | next best action |
| `requires_user_action` | yes/no |

### `permission_requests`

Used when a mobile or desktop action needs approval.

| Field | Purpose |
|---|---|
| `permission_id` | Permission request |
| `command_id` | Related command |
| `risk_level` | low, medium, high, blocked |
| `requested_action` | action summary |
| `status` | pending, granted, denied, expired |
| `expires_at` | timeout |

## Fallback Policy

Every command must declare a fallback policy.

| Policy | Meaning |
|---|---|
| `mobile_safe` | Phone can handle it directly |
| `worker_allowed` | Cloud/lightweight worker can handle it |
| `desktop_required` | Must wait for desktop |
| `queue_only` | Capture now, decide later |
| `blocked` | Do not execute |

## Examples

### Phone Asks For Priority

```text
Mobile -> voice_intent -> empireos command -> fallback worker reads last synced priorities -> result returns to phone
```

### Phone Requests Repo Audit

```text
Mobile -> voice_intent -> skillforge command -> desktop_required -> queued until desktop online
```

### Phone Captures Private Note Offline

```text
Mobile local outbox -> queued_offline -> sync_events when online -> private_memory gate
```

## Conflict Strategy

Use append-only events. Do not let devices overwrite each other's state directly.

Resolve by:

- latest result wins for display,
- commands remain immutable,
- corrections create new events,
- failed commands can be retried with a new attempt ID,
- permission decisions are explicit events.

## Sync Safety

Do not sync raw audio by default.

Prefer:

- transcript summary,
- redacted transcript,
- voice intent JSON,
- command/result summaries,
- artifact references.

Raw audio should be opt-in and local-only unless explicitly required.

## Desktop Reconnect

When desktop reconnects:

1. send heartbeat,
2. read unclaimed desktop-required commands,
3. claim one command at a time,
4. execute locally,
5. write result,
6. release or fail command with reason.

## Mobile UX Status Labels

| Status | Display |
|---|---|
| `pending` | Working... |
| `queued_offline` | Captured offline |
| `desktop_required` | Waiting for desktop |
| `claimed` | Desktop is working on it |
| `permission_required` | Needs approval |
| `completed` | Done |
| `failed` | Failed - retry available |
| `blocked` | Blocked for safety |
