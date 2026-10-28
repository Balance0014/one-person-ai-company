# 5 · The definition of done

## The problem

"Fixed" usually means "the error went away when I tried it once". Agents are especially prone to this: no errors found gets reported as done, and a patch that stops the bleeding gets reported as a cure.

## The rule

A task is done only when all five are true, each with evidence (a commit, a test name, a log line, a link):

1. **Root cause.** Which layer was actually wrong, and why it will not happen again.
2. **Prevention.** A regression test, a replay of past data, or a machine check that would catch it next time.
3. **Sweep.** The same mistake elsewhere: how many places, and were they fixed?
4. **Real verification.** It ran on real data or live: the scheduled job actually ran once more, the person actually received it, end to end.
5. **Cleanup.** Test files, temporary copies, retired code, schedules and references: deleted, and you can say what was deleted.

Rules that go with it:

- **Stopping the bleeding is not done.** Block the damage first if you must, but the task stays open until the cure ships.
- **If one item truly does not apply, write `n/a: <reason>`.** Leaving it blank is not allowed. Inventing evidence is the worst thing an agent can do.
- **Prove the problem before you change anything,** and verify the fix with the same check you used to prove it.
- **Before proposing any fix, answer three questions:** What is the real cause? What else has the same problem? How much will this cost to run every day? (One "fix" for a stuck agent was to wake every agent every 20 minutes. The alarms took about 30% of every session's calls and were pulled the next day. The real cause was one tool that hung without anyone noticing.)
- **Roll back with version control, not backup files.** No `file.bak`, no archive folders, no old and new versions living side by side.

## How to enforce it

`scripts/dispatch.py done` refuses to close a task unless all five fields are filled in.

## What it costs

More work per task. Less work in total, because the same bug stops coming back.
