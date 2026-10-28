# One-Person AI Company

**English** · [中文](README.zh-CN.md)

**How I run a company alone with 30+ AI agents, written up so you can copy it.** An org chart, a task ledger, handoff records, delivery reconciliation, a definition of done, quota budgets, and rules that machines actually enforce. Ships as templates, four small checks, and an agent skill that sets it all up for you.

![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat) ![Status: actively updated](https://img.shields.io/badge/status-actively%20updated-2EA44F?style=flat) ![Works with Claude Code and Codex](https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex-111827?style=flat)

---

## Why this exists

Running one agent is easy. Running thirty is a management problem. Every piece here exists because one of these actually happened:

- An agent reported "done" because it found no errors. Nothing had shipped.
- The account hit its weekly limit mid-task, and everything the agent knew vanished with the chat.
- Development work burned the whole week's quota, and the scheduled reports people were waiting for stopped for four days.
- The alarm that should have reported the outage ran on the same thing that was down.
- The same rule lived in three agents' instructions. A month later there were three different rules.
- An alert fired every hour until nobody read it, including the day it mattered.

## What's inside

| Chapter | Fixes | Comes with |
|---|---|---|
| [1 · A three-layer org chart](playbook/01-org-chart.md) | Everyone reports to you; rules copied everywhere | Role card template |
| [2 · The dispatch ledger](playbook/02-dispatch-ledger.md) | Tasks lost in chat | `scripts/dispatch.py` |
| [3 · Handoff records](playbook/03-handoff-records.md) | Account or quota dies, context dies with it | `scripts/handoff_check.py` |
| [4 · One judge per question](playbook/04-one-judge-per-question.md) | Agents grading their own homework | `scripts/reconcile.py` |
| [5 · The definition of done](playbook/05-definition-of-done.md) | "Fixed" meaning "worked once" | Enforced by `dispatch.py done` |
| [6 · Quota budgets](playbook/06-quota-budget.md) | Building starves the jobs that matter | Budget template |
| [7 · Rules become gates](playbook/07-rules-become-gates.md) | Rules that quietly stop being enforced | `scripts/rules_check.py` |
| [8 · Alerts that remember](playbook/08-alerts-that-remember.md) | Alert fatigue | Three-question checklist |

## See it in 30 seconds

No install needed. Python 3.9+ and the standard library only.

```bash
git clone https://github.com/Balance0014/one-person-ai-company
cd one-person-ai-company/examples
python3 ../scripts/reconcile.py --date 2026-10-27
python3 ../scripts/handoff_check.py
python3 ../scripts/rules_check.py
```

```
| | Delivery | Due | Result |
|---|---|---|---|
| ❌ | Morning brief | 2026-10-27 09:00 | missing, nothing by 09:40 |

✓ content.md
✗ research.md
    - missing section "## In progress"
    ...
✗ R-06: enforcer scripts/link_gate.py does not exist — Posts with broken links never ship
```

The example data is built to fail in instructive ways.

## Use it in your own repo

**As an agent skill** (Claude Code, Codex, and other agents that read `SKILL.md`):

```bash
npx skills add https://github.com/Balance0014/one-person-ai-company
```

Then ask your agent: *"Set up the one-person AI company structure in this repo."* It copies the templates, asks who your leads are, writes role cards and handoff records, and runs the four checks.

**By hand:**

```bash
cp -r templates/ops templates/ops.config.json /path/to/your/repo/
cp -r scripts /path/to/your/repo/
```

Then run the health check from your repo root:

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py --repo .
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

Each exits 1 when something needs attention, so they drop straight into a hook, a cron job, or CI.

## The four checks

| Script | Answers | Model calls |
|---|---|---|
| `dispatch.py` | What's open, who owns it, what's late? Refuses to close a task without the five-item definition of done | 0 |
| `handoff_check.py` | Could a fresh session pick up each workstream right now? | 0 |
| `reconcile.py` | Did every scheduled delivery actually arrive, on time? | 0 |
| `rules_check.py` | Is every enforced rule still enforced by something that exists? | 0 |

All paths come from `ops.config.json`. Nothing is hard-coded. Tests cover both directions (good input passes, bad input is caught): `python3 -m unittest discover tests`.

## Who made this

I'm [Balance Zhao](https://github.com/Balance0014), a growth marketer turned builder. I run 30+ agents that write articles, do investment research, research products, and maintain the products I vibe-code, including [GapMine](https://gapmine.com). This repo is that setup, with every company-specific detail stripped out.

More playbooks are on the way. [Follow on X](https://x.com/balance0014) to catch them.

## License

MIT
