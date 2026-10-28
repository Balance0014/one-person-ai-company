---
name: one-person-ai-company
description: Set up and run the operating system for a company where one person manages many AI agents. Use when the user wants to organize multiple agents or projects into a reliable structure (org chart, task ledger, handoff records, delivery reconciliation, definition of done, quota budgets, rules as gates, alert hygiene), or when they ask to check whether that structure is healthy.
---

# One-Person AI Company

You help one person run many AI agents like a small company. The full method is in `playbook/` (eight short chapters). Templates are in `templates/`, and the four checks are in `scripts/` (Python standard library only).

## When setting it up in a repo

1. Copy `templates/ops/` and `templates/ops.config.json` into the user's repo. Set `timezone_offset_hours` to the user's timezone.
2. Ask who the leads are (one per business area) and which projects each lead owns. Write a role card (`templates/ROLE-CARD.md`) at the top of each lead's instruction file. "Delivers" must be a checkable result, not a list of steps.
3. Create one handoff record per workstream in `ops/handoff/` from `templates/HANDOFF.md`, filled with the real current state.
4. List every scheduled delivery in `ops/EXPECTATIONS.json`. Make whatever sends each output append a line to `ops/deliveries.jsonl`, written by the sender and not by the agent that did the work.
5. Register each rule in `ops/RULES-REGISTRY.json` with an honest tier: `gate`, `scheduled`, or `advisory`. Never label something a gate unless a machine actually blocks it.
6. Run all four checks once and show the user the output.

## While working inside a set-up repo

- Tasks that cross a layer go through `scripts/dispatch.py`, not chat.
- Do not close a task without all five items of the definition of done (`playbook/05-definition-of-done.md`). Write `n/a: <reason>` when one truly does not apply. Never invent evidence.
- Update your handoff record after every key step: a commit, a release, a decision, or a change of direction.
- Do not answer "did it arrive?" from memory or from your own plan. Run `scripts/reconcile.py`.
- Before adding a new check or alert, ask whether the question already has a judge (`playbook/04-one-judge-per-question.md`) and replay any new alert against the last 7 days (`playbook/08-alerts-that-remember.md`).
- Respect the quota budget. Near the limit, only do work that protects scheduled deliveries (`playbook/06-quota-budget.md`).

## Health check

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py --repo .
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

Each exits 1 when something needs attention. Report results in plain language: what is wrong, who is affected, and who owns it.
