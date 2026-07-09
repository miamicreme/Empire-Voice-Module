# Empire Voice Protection Policy

Empire Voice is intended to become a private module for EmpireOS.

This repository may contain public-safe architecture, contracts, adapters, tests, and generic module code. It must not contain private EmpireOS data, client data, buyer data, credentials, private memories, or proprietary scoring logic.

## Public-Safe

The following can live here:

- generic voice intent contracts,
- generic router logic,
- redaction utilities,
- public-safe examples,
- SkillForge / DealFlow / GlobalIntel / SignalBrief / FrameBrief adapter shapes,
- architecture docs,
- module tests.

## Private Only

The following must not be committed here:

- private EmpireOS memories,
- personal daily dashboards,
- private client notes,
- buyer lists,
- CRM exports,
- DealFlow scoring formulas,
- API keys,
- OAuth tokens,
- passwords,
- `.env` files,
- private model prompts that reveal strategy,
- real voice recordings unless sanitized.

## Golden Rule

If it reveals how Kohron, EmpireOS, MiamiCreme, DealFlow, a client, a buyer list, or a private decision system actually operates, it does not belong in a public commit.

## Branch Rule

Work on `develop` or feature branches.

Protect `main` with pull requests, no force pushes, and no direct commits.
