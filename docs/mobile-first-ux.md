# Mobile-First UX Architecture

Empire Voice must work from a phone first.

The desktop app is powerful, but the phone is the daily control surface. The user should be able to ask Empire what to do, create tasks, trigger briefs, capture notes, review priorities, and route work even when the desktop is offline.

## UX Principle

```text
Phone = primary command surface
Desktop = power workstation / local execution node
Database = shared command/event backbone
Fallback = cloud/lightweight mobile execution when desktop is unavailable
```

## Product Modes

| Mode | When Used | What Works |
|---|---|---|
| Mobile Online + Desktop Online | Best experience | Phone sends command, desktop can execute local tools, screen/browser/STT/TTS, local memory sync |
| Mobile Online + Desktop Offline | Normal daily fallback | Phone sends command to DB, cloud/mobile-safe worker handles lightweight actions, desktop catches up later |
| Mobile Offline | Capture mode | Phone queues voice notes/intents locally and syncs when online |
| Desktop Online Only | Power mode | Desktop can run full local assistant, local models, screen/browser tools |
| No Network | Local-only mode | Device captures notes, dictation, and pending commands without remote actions |

## Mobile Home Screen

The mobile UX should be simple:

1. Big voice button.
2. Today’s top priority.
3. Mission queue.
4. Quick actions.
5. Inbox/captured notes.
6. Device status: desktop online/offline.

Suggested home layout:

```text
[ Empire ]
What should I do next?

[ Hold to Talk ]

Today
- Top Priority
- Next Action
- Due / Risk

Quick Actions
[ Capture ] [ Prep Call ] [ Repo Audit ] [ DealFlow ] [ GlobalIntel ]

Desktop: Online / Offline
Sync: Up to date / Pending / Offline
```

## Mobile Voice Flow

```text
Tap/hold mic
  -> local/mobile STT when available or server STT fallback
  -> create voice_intent
  -> write sync_event to DB
  -> show immediate confirmation
  -> if desktop online, desktop claims event
  -> if desktop offline, fallback worker handles safe subset
  -> result appears in mobile timeline
```

## Desktop Companion UX

The desktop app should show:

- connected mobile devices,
- incoming commands,
- claim/execution status,
- local tool permissions,
- screen/browser context permissions,
- local memory sync status,
- failed command retry queue.

Desktop is the best executor for:

- screen reading,
- browser control,
- local files,
- local models,
- dictation into desktop apps,
- heavy repo analysis,
- private local memory operations,
- high-risk actions requiring confirmation.

## Shared Timeline

Both phone and desktop should show the same event timeline:

```text
Voice captured
Intent created
Routed to SkillForge
Desktop claimed command
Permission requested
Action completed
Result available
```

## Fallback Behavior

When desktop is offline:

| Request | Mobile/Cloud Fallback |
|---|---|
| Capture note | Save locally and sync later |
| What should I do next? | Use last synced EmpireOS priorities |
| Create task | Write pending task event to DB |
| Prep call | Generate lightweight checklist from synced context |
| Repo audit | Queue for desktop unless repo is cloud-accessible |
| DealFlow action | Use synced deal summaries only; mark stale if needed |
| GlobalIntel | Use online data/API if available |
| Send email/post/commit/delete | Require desktop or explicit confirmation path |

## UX Rule

Never leave the user wondering what happened.

Every mobile action should show one of:

- Done,
- Queued,
- Needs desktop,
- Needs confirmation,
- Failed with retry,
- Captured offline.

## Minimum Viable Mobile App

The first mobile app can be simple:

- PWA or React Native shell,
- login,
- hold-to-talk or text input,
- timeline,
- top priority card,
- quick actions,
- desktop status,
- offline outbox.

Do not start with a complex full dashboard. Start with capture, command, timeline, and fallback.
