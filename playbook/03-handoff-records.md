# 3 · Handoff records

## The problem

A model account hits its weekly limit in the middle of a task. Or the context fills up and the session is cleared. Everything the agent knew lived in the conversation, so it is gone. The next session starts from zero and redoes work, or worse, undoes it.

## The rule

Every workstream keeps one handoff file in the repo. A brand-new session, with no chat history and possibly on a different account, must be able to read it and say exactly what to do next.

- **First line:** `Updated YYYY-MM-DD HH:MM`, plus which files to read first.
- **Seven fixed sections:** Done · In progress · Not done · Next · Blocked on · Branches · Uncommitted or unpushed.
- **Update after every key step:** a commit, a release, a decision, a change of direction. Not when the quota is about to run out; by then it is too late.
- **The file lives in the repo and is pushed**, so it survives the account.

Template: [`templates/HANDOFF.md`](../templates/HANDOFF.md).

## How to check it

```bash
python3 scripts/handoff_check.py                 # all seven sections and a timestamp?
python3 scripts/handoff_check.py --repo .        # also fail if commits are newer than the record
```

Wire the second command into your agent's stop hook. The agent then cannot end a turn with committed work that the record does not mention.

## How to prove it works

Once in a while, open a fresh session, give it only the repo, and ask it to state where each workstream stands and what comes next. Compare with reality line by line. If it cannot say the next step precisely, the record is not good enough.

We keep 24 handoff records, one per long-running session. Before trusting the system we ran this drill on 15 of them. Every single drill found mismatches between the record and the actual repo, usually five or more: a "next step" that was already done, a task marked unclaimed that someone was already working on, a setting the record placed in one file that was actually in nine. On a normal day the start-of-session check still flags a few records as stale or incomplete (on the day this was written, 7 of 24). That is the check doing its job, not a reason to stop checking.

One blind spot we hit: our first version called a record fresh if it had been updated within the last two hours. A session could write the record, keep working for another hour and a half, and still pass. Compare timestamps exactly: the record must be newer than the last piece of work.

## What it costs

A few minutes per key step. It is the cheapest insurance you will ever buy.
