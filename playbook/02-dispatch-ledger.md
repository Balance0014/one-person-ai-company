# 2 · The dispatch ledger

I used to ask an agent to fix something in chat. Then the session got cleared, or a different agent took over the area the next week, and the request was gone. Nothing told me it had been dropped.

Now every task that crosses a layer (HQ to a lead, a lead to HQ, one area to another) is an entry in a single file in the repo:

```
new → acked (with a plan) → done (with evidence) | rejected (with a reason)
```

- The owner acknowledges within 24 hours, or the task gets flagged.
- An open task past its due date gets flagged.
- Closing a task takes all five pieces of evidence from [chapter 5](05-definition-of-done.md). The script won't close it while any of them is empty.
- A chat message can remind someone about a task. It isn't the task.

## Commands

```bash
python3 scripts/dispatch.py add --to content --title "Morning brief arrived late twice this week"
python3 scripts/dispatch.py ack D-20261028-01 --plan "Replay the scheduler log for the last 7 days"
python3 scripts/dispatch.py done D-20261028-01 \
  --root-cause "..." --prevention "..." --sweep "..." --verification "..." --cleanup "..."
python3 scripts/dispatch.py overdue   # exits 1 if anything is late; run it on a schedule
```

Each lead's session lists its own open tasks when it starts: `python3 scripts/dispatch.py list --to content --open`.

## How it's going

As of October 28, 2026, my ledger holds 67 tasks from the past six weeks. 33 are closed with all five pieces of evidence, 8 were rejected with a reason, 9 are in progress, and 17 haven't been acknowledged. 13 of those are overdue.

So the 24-hour rule gets broken a lot. The ledger hasn't made anyone faster. What it changed is that those 13 tasks show up on a list every day with an owner's name next to them. Before, they'd have been sitting in old chats where nobody would ever look again.

It's one JSON file, a few seconds per task, and no model calls.
