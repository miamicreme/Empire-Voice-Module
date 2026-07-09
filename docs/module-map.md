# Empire Voice Module Map

Empire Voice is the spoken interface to the MiamiCreme / EmpireOS stack.

## Stack Map

```text
User Voice
  -> Empire Voice
      -> EmpireOS
      -> SkillForge
      -> DealFlow
      -> GlobalIntel
      -> SignalBrief
      -> FrameBrief
      -> MCP Tools
```

## Module Responsibilities

| Module | Role | Voice Example |
|---|---|---|
| EmpireOS | Private command center | "What should I do next?" |
| SkillForge | Plans, specs, audits, artifacts | "Audit this repo and make a branch plan." |
| DealFlow | Deal intelligence and follow-up | "Which buyer should I follow up with?" |
| GlobalIntel | Global risk and market watch | "What changed overnight?" |
| SignalBrief | Market/social/customer chatter | "What are people saying about this niche?" |
| FrameBrief | Video/screen/demo intelligence | "Watch this video and make a brief." |
| MCP Tools | External tool actions | "Open GitHub and check the PR." |

## Voice Commands By Category

### Decide

- "Empire, what should I do next?"
- "Empire, should I take this deal?"
- "Empire, what is the highest leverage action today?"

### Build

- "Empire, turn this into a spec."
- "Empire, make a branch plan."
- "Empire, use SkillForge to audit this repo."

### Sell

- "Empire, write the follow-up."
- "Empire, prep the proposal."
- "Empire, give me the buyer angle."

### Research

- "Empire, find what people are saying."
- "Empire, check global risk."
- "Empire, summarize this video."

### Operate

- "Empire, open the dashboard."
- "Empire, update the task list."
- "Empire, log this as memory."

## Target Selection Rule

| Spoken Signal | Route To |
|---|---|
| next, today, priority, mission, decide | EmpireOS |
| repo, code, branch, audit, spec, plan | SkillForge |
| deal, buyer, seller, LOI, offer, follow-up | DealFlow |
| global, market, country, risk, overnight, energy | GlobalIntel |
| people saying, trend, competitor, pain, market chatter | SignalBrief |
| video, demo, screen, YouTube, ad, walkthrough | FrameBrief |
| open, click, browser, Slack, Gmail, GitHub | MCP / tool router |
| type this, dictate, paste | Dictation |

## Output Rule

Every routed command should produce one of:

- next action,
- mission,
- brief,
- artifact,
- proposal,
- branch plan,
- deal action,
- memory event,
- tool call request.
