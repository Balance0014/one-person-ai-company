# 6 · Quota budgets

## The problem

Your scheduled jobs and your development sessions usually draw from the same account limit. One busy week of building can burn it all, and then the scheduled jobs that actually matter (the reports people are waiting for) fail to start. That happened to us: development used up the weekly limit and the scheduled reports stopped for four days.

A second version of the same problem: nine sessions doing heavy work at once burned half of a five-hour window in thirty minutes.

## The rule

- **Scheduled deliveries come first.** At 90% of the weekly limit, every session stops starting new changes. The last 10% is reserved for keeping scheduled deliveries alive.
- **Each area gets a weekly budget** ([`templates/QUOTA-BUDGET.json`](../templates/QUOTA-BUDGET.json)). An area over budget stops starting changes until the week resets or head office grants more. Without per-area budgets, one area can drag everyone to a stop: we once saw one area use about 63 of the 78 points spent in two days.
- **At most two sessions do heavy work at the same time** (sub-agents, large scans, big refactors).
- **Keep heavy work away from scheduled run times.** Leave a buffer before and after each scheduled job.
- **A missed scheduled job is never re-run automatically.** If a report did not go out, a person decides whether to send it late. Automatic re-runs pile up during an outage and spam people when it ends.

## How to enforce it

The budget file is data. Enforcement belongs in your agent's pre-tool hook: read current usage, map the session's working directory to an area, and block file edits and sub-agents when that area is over budget. A pass for "this protects a scheduled delivery" should expire within hours, not days. A pass that lasts all day quickly turns into an open door for everyone.

## What it costs

Some development weeks end early. That is the point.
