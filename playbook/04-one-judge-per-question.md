# 4 · One judge per question

## The problem

Ask an agent "did today's report go out?" and it will usually say yes. It may be reading its own plan, a log line that says "sending...", or nothing at all. Meanwhile three different checks each decide "did it arrive" in their own way, and they disagree.

Two failures we actually hit:

- **A self-check that never noticed the self was dead.** The process that was supposed to report outages was the one that went down.
- **The alarm went through the thing it was watching.** When the account ran out of quota, the scheduled jobs stopped, and so did the job that reported missing jobs. The owner heard nothing for days.

## The rule

Each question gets exactly one judge, and the judge only reads hard evidence:

| Question | Judge | Reads |
|---|---|---|
| Did it arrive? | The reconciler | What was expected (a schedule file) vs what the *sender* recorded |
| Is it any good? | The area's lead | Its own quality checks |
| Are the ledgers up to date? | A periodic audit | The ledgers themselves |

- **The record of what arrived is written by the sender, not by the agent that did the work.**
- **Bad news has one exit, and that exit must not depend on the thing being watched.** If your scheduler can die, the alarm about the scheduler cannot run on it.
- **Before adding a new check, ask: does this question already have a judge?** If it does, read its verdict instead of writing a second one.

## How to run it

1. List everything that must arrive on a schedule in `ops/EXPECTATIONS.json` (`"daily 09:00"`, `"weekly mon 17:00"`, plus a grace window).
2. Make whatever sends the output append one line to `ops/deliveries.jsonl`.
3. Run the reconciler the next morning:

```bash
python3 scripts/reconcile.py --date 2026-10-27
```

```
| | Delivery | Due | Result |
|---|---|---|---|
| ✅ | Morning brief | 2026-10-27 09:00 | on time |
| ❌ | Weekly report | 2026-10-27 17:00 | missing, nothing by 18:00 |
```

Run it somewhere that does not share a fate with your agents (a small server, a CI job), so it still reports when they are down.

## What it costs

Zero model calls. It is plain file comparison.
