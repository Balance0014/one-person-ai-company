# One-Person AI Company

**English** · [中文](README.zh-CN.md)

**8 rules for running 30+ AI agents, each one from something that broke.**

I run a one-person company. The agents are 18 long-running Claude Code sessions, one per project or lead, and about 20 scheduled jobs that each run their own prompt. They write crypto and AI research briefs, draft posts for my social accounts, and build and monitor [GapMine](https://gapmine.com), a product I'm working on. Most of what they produce lands in my chat every morning.

This repo is the operating system I ended up with after things kept breaking: how the agents are organized, how work survives a cleared session, how I know what actually shipped, and which rules a machine enforces. It's eight short chapters, templates, four Python checks with no dependencies, and an agent skill that sets it up in your repo.

[![CI](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml/badge.svg)](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml) ![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat) ![Python 3.9+ standard library](https://img.shields.io/badge/python-3.9%2B%20stdlib%20only-3776AB?style=flat) ![Used daily with Claude Code](https://img.shields.io/badge/used%20daily%20with-Claude%20Code-111827?style=flat)

---

## What broke first

Everything in here was added after one of these happened:

- An agent reported a task as done because it found no errors. Nothing had shipped.
- A session hit the weekly limit mid-task, and everything it knew disappeared with the chat.
- A few days of heavy development burned through my weekly limit, and my morning briefs stopped for four days.
- The job that tells me about missing jobs ran on the same account as the jobs. When the quota ran out it went quiet too, and I heard nothing for five days.
- A rule lived in a scheduled job's prompt and in the repo. Within weeks the two copies disagreed.
- My own monitor sent me 28 messages in one week, and I couldn't act on any of them.

## How it's organized

<p align="center"><img src="docs/org-chart.svg" alt="Org chart: me at the top, HQ below, four leads, and their projects. HQ can read every project's records but gives work only to the leads." width="760"></p>

HQ is one agent session that owns the shared rules, the ledgers, the quota, and the answer to "did it arrive?" It gives work only to the four leads, and each lead runs its own projects. Agents only come to me about money, irreversible deletes, changes to my rules, and publishing. [Chapter 1](playbook/01-org-chart.md) has the rest.

## The chapters

| Chapter | The problem it fixes | Comes with |
|---|---|---|
| [1 · Org chart and lines of communication](playbook/01-org-chart.md) | Every agent reports to you, and every rule is pasted into every prompt | Role card and decision log templates |
| [2 · The dispatch ledger](playbook/02-dispatch-ledger.md) | Tasks get lost in chat | `scripts/dispatch.py` |
| [3 · Handoff records](playbook/03-handoff-records.md) | A session dies and takes its context with it | `scripts/handoff_check.py` |
| [4 · One judge per question](playbook/04-one-judge-per-question.md) | Agents grade their own homework | `scripts/reconcile.py` |
| [5 · The definition of done](playbook/05-definition-of-done.md) | "Fixed" means "worked once" | `dispatch.py done` |
| [6 · Quota budgets](playbook/06-quota-budget.md) | Development starves the jobs that matter | Budget template |
| [7 · Rules become gates](playbook/07-rules-become-gates.md) | Rules quietly stop being enforced | `scripts/rules_check.py` |
| [8 · Alerts that remember](playbook/08-alerts-that-remember.md) | Alert fatigue, and alerts nobody can act on | Three questions to answer before an alert ships |

## My setup, as of October 28, 2026

| | |
|---|---|
| Agents | 18 long-running Claude Code sessions (one per lead or project) and about 20 scheduled jobs |
| Org | HQ, 4 leads, and 45 role cards (one per role, including scheduled jobs and paused projects) |
| Scheduled deliveries | 21 daily and weekly ones, checked twice a day by a script that makes no model calls, running on its own small server |
| Rules | 170 registered: 82 name the script that blocks them, 41 are checked on a schedule, 47 rely on discipline |
| Dispatch ledger | 67 tasks in six weeks: 33 closed with all five pieces of evidence, 8 rejected, 26 still open |
| Handoff records | 24, one per agent session, including paused ones. I've run the drill on 15 of them: hand the repo to a fresh session with no chat history and compare |

My worst failure is in here too: an 18-day outage my reconciler reported correctly almost every morning, while the alert named an owner who was down as well ([chapter 4](playbook/04-one-judge-per-question.md#the-18-days)).

## Try it in 30 seconds

You only need Python 3.9+. Nothing to install.

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

The example data is set up to fail, so you can see what each check catches.

## Use it in your own repo

**As an agent skill.** You'll need Node.js 22.20 or newer for this command:

```bash
npx skills add https://github.com/Balance0014/one-person-ai-company
```

Then tell your agent: *"Set up the one-person AI company structure in this repo."* It copies the templates, asks who your leads are, writes role cards and handoff records, and runs the four checks. CI installs the skill this way on every push. The skill uses the open `SKILL.md` format, but I've only used it with Claude Code.

**By hand:**

```bash
cp -r templates/ops templates/ops.config.json /path/to/your/repo/
cp -r scripts /path/to/your/repo/
```

Then run the checks from your repo root:

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

Each one exits 1 when something is missing, overdue, or broken (a late delivery is only a warning), so you can run them from cron or CI. Claude Code hooks block only on exit code 2, so wrap a check to use it there: `python3 scripts/handoff_check.py --record content.md --repo . >&2 || exit 2`.

## The four checks

| Script | What it tells you | Model calls |
|---|---|---|
| `dispatch.py` | What's open, who owns it, and what's late. Won't close a task that was never acked, or while any of the five evidence fields is empty | 0 |
| `handoff_check.py` | Whether a fresh session could pick up each project right now: the seven sections, the timestamp, and (with `--record` and `--repo`) whether that project has commits newer than its record | 0 |
| `reconcile.py` | Whether every scheduled delivery arrived on time, according to what the sender logged | 0 |
| `rules_check.py` | Whether every rule marked as enforced still points to a script that exists and still contains the marker string you chose | 0 |

All paths come from `ops.config.json`, so nothing's hard-coded. The tests check both directions, good input passes and bad input fails: `python3 -m unittest discover tests`.

## Limits

- The scripts are a clean rewrite. My production versions are tied to my own servers and accounts, so these are deliberately small.
- The checks only see what you write down. A delivery that isn't in `EXPECTATIONS.json` never gets reported missing.
- `rules_check.py` only checks that a gate's script exists and contains your marker string. It can't prove the script is wired into a hook.
- Nothing runs on its own. You wire the checks into your hooks, cron jobs, or CI.

## About me

I'm [Balance Zhao](https://github.com/Balance0014). I spent years in growth marketing before I started building. This repo is my own setup with everything company-specific taken out. I'll be open-sourcing more of it; [follow me on X](https://x.com/balance0014) if you want to see what's next.

## License

MIT
