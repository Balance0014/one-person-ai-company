# 6 · Quota budgets

From September 19 to 22, 2026, a burst of development used up my account's weekly limit. My scheduled AI jobs were rejected at startup, and the morning briefs stopped for four days. Those jobs and my development sessions draw from the same pool, and nothing protected the jobs.

The next day brought the short-term version of the same problem: nine sessions doing heavy work at once took the five-hour limit from 25% to 74% in half an hour.

## The rules

- **Scheduled deliveries come first.** At 90% of the weekly limit, no session starts new work. The last 10% keeps scheduled jobs running.
- **Each area gets a weekly budget** ([`templates/QUOTA-BUDGET.json`](../templates/QUOTA-BUDGET.json)). An area over budget stops starting new work until the week resets or HQ grants more. Without per-area budgets one area can stop everyone: on October 22, one area burned 63 of the 78 percentage points of weekly quota used in two days.
- **At most two sessions do heavy work at a time.** Heavy means sub-agents, large scans, and big refactors. Reading results and replying to messages don't count.
- **Keep heavy work away from scheduled run times.** Leave a buffer before and after each job.
- **Never re-run a missed scheduled job automatically.** If a report didn't go out, a person decides whether to send it late. Automatic re-runs pile up during an outage and flood everyone when it ends.

## Enforcing it

The budget file is just data. Enforcement belongs in your agent's pre-tool hook: read current usage, map the session's working directory to an area, and block file edits and sub-agents when that area is over budget.

If you add an override for "this protects a scheduled delivery", make it expire within hours. Mine used to last until the end of the day, so one session's one-line note let every session past the gate until then.
