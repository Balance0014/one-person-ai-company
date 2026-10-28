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

## What it costs

A few minutes per key step. It is the cheapest insurance you will ever buy.
