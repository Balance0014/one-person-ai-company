# 8 · Alerts that remember

## The problem

An alert fires every hour for the same problem. By day two nobody reads it. By day five a real outage is sitting in the same channel and nobody sees it.

## The rule

Before a new alert ships, it must answer three questions:

1. **Does it mean someone was affected?** Not "an error appeared in a log", but "a report did not arrive", "a number is stale", "a page will not open". Use ratios or comparisons to a baseline, not made-up absolute thresholds.
2. **Has it been replayed against the last 7 days?** How many times would it have fired, and was someone really affected each time? If the answer is off even once, fix the rule before shipping it.
3. **What can the reader do about it?** If they can act, say exactly what. If they cannot, it is your problem, not theirs. Keep it out of their channel and in your logs.

And three behaviors:

- **Report changes, not repeats.** The same problem with the same content stays quiet for 20 hours. Worse or wider goes out immediately.
- **Close the loop.** When the problem clears, send one "✅ recovered" line and drop it from memory.
- **Never put changing numbers in the de-duplication key.** If the key contains "3 hours ago", de-duplication never works.

Every red alert has three parts, in this order:

- **Problem:** one plain sentence, naming the thing (which report, which source). No function names, field names, or URLs.
- **Impact:** what the reader will notice (did not arrive, numbers are stale, money is leaking).
- **Owner:** which lead, or head office.

## What it costs

You will ship fewer alerts. Every one that ships gets read.
