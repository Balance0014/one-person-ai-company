# 8 · Alerts that remember

In one week in October 2026, my own HQ monitor sent me 28 messages, mostly the same overdue internal tasks repeated every day. I couldn't act on any of them. A few weeks earlier I had the opposite problem. During the 18-day outage in [chapter 4](04-one-judge-per-question.md#the-18-days), a correct alert went out almost every morning and never told me the one thing I had to do.

## Three questions before an alert ships

1. **Does it mean someone was affected?** "A report didn't arrive", "a number is stale", "a page won't load". An error showing up in a log doesn't count. Compare against a baseline or use a ratio; made-up absolute thresholds fire at the wrong times.
2. **What happens if you replay it against the last 7 days?** Count how often it would have fired and check whether someone was really affected each time. If even one case is wrong, fix the rule before it ships.
3. **Who can act on it, and what exactly should they do?** Name someone who'll still be up when the thing being watched is down. If the cause could be the account or the bill, that someone is you, and the alert should say "renew the plan", not "11 deliveries missing." If nobody who reads it can act, keep it out of their channel and put it in a ledger the responsible lead works through.

## How alerts should behave

- **Only report changes.** If the same problem has the same content, stay quiet for 20 hours. If it gets worse or spreads, send it right away.
- **Close the loop.** When the problem clears, send one "✅ recovered" line and forget it.
- **Keep changing numbers out of the de-duplication key.** If the key contains "3 hours ago", de-duplication never matches.

Every red alert has three parts, in this order:

- **Problem:** one plain sentence that names the thing (which report, which source). No function names, field names, or URLs.
- **Impact:** what the reader will notice (it didn't arrive, the numbers are stale, money is leaking).
- **Owner:** which lead, or HQ. Or you.

## What changed for me

After the 28-message week, internal backlog moved out of my chat and into a ledger HQ works through. My daily summary now opens with one sentence: what's missing, and whether I need to do anything.

The case it still gets wrong is the one from chapter 4. My reconciler can't see my billing, so when every job stops at once it guesses quota and points at HQ. That gap is still open.
