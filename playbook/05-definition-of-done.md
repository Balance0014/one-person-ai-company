# 5 · The definition of done

One of my projects kept going quiet in the middle of tasks. The proposed fix was to wake every agent every 20 minutes. It ran for a day. The wake-ups ate about 30% of every session's calls, and the actual cause turned out to be a single tool that hung without anyone noticing.

By most agents' standards that fix was done: the symptom went away. Agents call something fixed when they tried it once and saw no error, and they report a stopgap as a cure. So I wrote down what done means.

A task is done only when all five of these are true, each backed by evidence (a commit, a test name, a log line, a link):

1. **Root cause.** Which layer was actually wrong, and why it won't happen again.
2. **Prevention.** A regression test, a replay of past data, or a machine check that would catch it next time.
3. **Sweep.** The same mistake elsewhere: how many places, and were they fixed?
4. **Real verification.** It ran on real data or live. The scheduled job actually ran again, the person actually got the output, end to end.
5. **Cleanup.** Test files, temporary copies, retired code, schedules, and references are deleted, and you can say what was deleted.

And the rules that go with it:

- A stopgap isn't a fix. Ship one if you have to, but the task stays open until the real fix lands.
- If an item truly doesn't apply, write `n/a: <reason>`. Leaving it blank isn't allowed, and making up evidence is the worst thing an agent can do.
- Reproduce the problem before you change anything, then verify the fix with the same check.
- Before proposing a fix, answer three questions: what's the real cause, what else has the same problem, and what will this cost to run every day? The 20-minute wake-up would have failed the third one on paper.
- Roll back with version control. No `file.bak`, no archive folders, no old and new versions living side by side.

## Enforcing it

`scripts/dispatch.py done` won't close a task while any of the five fields is empty. It can't tell whether the evidence holds up. That's for whoever assigned the task to judge.
