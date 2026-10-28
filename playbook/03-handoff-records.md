# 3 · Handoff records

A session would hit the weekly limit in the middle of a task, or fill its context window and get cleared. Everything it knew lived in the conversation. The next session started from zero and redid the work, or undid it.

Now every project keeps one handoff file in its repo. A fresh session with no chat history, possibly on a different account, has to be able to read it and say exactly what to do next.

- Line one: `Updated YYYY-MM-DD HH:MM`, plus which files to read first.
- Seven fixed sections: Done · In progress · Not done · Next · Blocked on · Branches · Uncommitted or unpushed.
- Update it after every key step: a commit, a release, a decision, a change of direction. Once the quota is about to run out, it's too late.
- It lives in the repo and gets pushed, so it survives the account.

Template: [`templates/HANDOFF.md`](../templates/HANDOFF.md).

## Checking it

```bash
python3 scripts/handoff_check.py                 # all seven sections and a timestamp?
python3 scripts/handoff_check.py --repo .        # also fail if there are commits newer than the record
```

Put the second command in your agent's stop hook and it can't end a turn with commits the record doesn't mention.

My first version of this check had a hole. It treated a record as fresh if it had been updated within two hours of the latest commit, so a session could write the record, keep working for another 90 minutes, and still pass. The check here allows 15 minutes, which is only there because the timestamp has minute precision.

## Drills

Every so often, open a fresh session, give it only the repo, and ask where each project stands and what comes next. Then compare its answer with reality, line by line.

I keep 24 records, one per session, including 6 for paused projects. Before I trusted the setup, I drilled 15 of them. Every drill found mismatches, usually five or more: a "next step" that was already done, a task marked unclaimed that someone was already working on, a setting the record placed in one file that was actually in nine. On the day I wrote this, the start-of-session check flagged 7 of the 24 as stale or incomplete.

Keeping a record current takes a few minutes per key step.
