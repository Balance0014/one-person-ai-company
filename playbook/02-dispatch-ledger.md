# 2 · The dispatch ledger

## The problem

You ask an agent to fix something in a chat. The chat ends, the session gets cleared, or a different agent picks up the area next week. Nobody remembers the request, and nothing tells you it was dropped.

## The rule

Every task that crosses a layer lives in one file in the repo, not in chat:

```
new → acked (with a plan) → done (with evidence) | rejected (with a reason)
```

- **Acknowledge within 24 hours.** An unacknowledged task is flagged.
- **Finish by the due date.** An open task past its due date is flagged.
- **"Done" requires evidence.** The ledger refuses to close a task without the five-item definition of done (see [5 · Definition of done](05-definition-of-done.md)).
- **A chat message is a reminder, not the task.** The ledger entry is the task.

## How to run it

```bash
python3 scripts/dispatch.py add --to content --title "Morning brief arrived late twice this week"
python3 scripts/dispatch.py ack D-20261028-01 --plan "Replay the scheduler log for the last 7 days"
python3 scripts/dispatch.py done D-20261028-01 \
  --root-cause "..." --prevention "..." --sweep "..." --verification "..." --cleanup "..."
python3 scripts/dispatch.py overdue   # exits 1 if anything is late; run it on a schedule
```

Each lead's session can list its own open tasks when it starts: `python3 scripts/dispatch.py list --to content --open`.

## What it looks like for us

As of 28 October our ledger has carried 67 cross-layer tasks since mid-September: 33 closed with all five items of evidence, 8 rejected with a reason, 9 being worked on, and 17 not yet acknowledged, 13 of them overdue. Those 13 are not a success story. Before the ledger they would have been 13 requests quietly lost in old chats. Now they show up on a list every day, with an owner next to each one.

## What it costs

One JSON file and a few seconds per task. No model calls.
