# 4 · One judge per question

From September 11 to 16, 2026, my account hit its weekly limit and every scheduled AI job was rejected at startup. The script that compares expected deliveries with actual ones runs on its own small server, so it kept going and logged the gap. The job that was supposed to tell me about it ran on the same account, though, so it was rejected too. Five days went by before I knew, and I only found out because another agent happened to notice.

Ask an agent "did today's report go out?" and it'll usually say yes. It may be reading its own plan, a log line that says "sending...", or nothing at all. Meanwhile three different checks each decide "did it arrive" in their own way, and they disagree.

So every question gets exactly one judge, and a judge only reads hard evidence:

| Question | Judge | Reads |
|---|---|---|
| Did it arrive? | The reconciler | The schedule file vs. what the *sender* logged |
| Is it any good? | The area's lead | Its own quality checks |
| Are the ledgers current? | A periodic audit | The ledgers themselves |

- The delivery log is written by whatever sends the output, never by the agent that did the work.
- Bad news has one channel, and that channel can't depend on the thing it watches. If your scheduler can die, the alarm about the scheduler can't run on it.
- Before adding a check, ask whether the question already has a judge. If it does, read that verdict instead of writing a second one.

## Running it

1. List everything that should arrive on a schedule in `ops/EXPECTATIONS.json` (`"daily 09:00"`, `"weekly mon 17:00"`, plus a grace window).
2. Have whatever sends each output append one line to `ops/deliveries.jsonl`.
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

Run it somewhere that doesn't share a fate with your agents, like a small server or a CI job. It's plain file comparison with no model calls.

## The 18 days

After September 16, my reconciler started sending its own alerts instead of handing them to an agent. It runs twice a day and tracks 21 scheduled deliveries.

From September 26 to October 13, none of my AI-run scheduled jobs started. The account hit its usage limit, then my plan lapsed, and I didn't renew it until October 14. Every agent that might have investigated was down too. The reconciler wasn't. Across those 18 days its morning reports listed 210 missing deliveries, 11 to 26 at a time, and it messaged me almost every morning. It even guessed the cause: when that many deliveries are missing at once, check the account's quota first.

It still took me 18 days. The alert assigned the quota problem to HQ, which is an agent running on the same dead account. The only one who could fix it was me, and the alert never said that. [Chapter 8](08-alerts-that-remember.md) is about writing alerts that name someone who can actually act.
