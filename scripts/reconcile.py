#!/usr/bin/env python3
"""Reconciler: one judge for one question — "did it arrive?"

Agents will tell you a job is done. The reconciler does not ask them. It
compares two plain files:
  - expectations_file: what should arrive, and when
      {"id": "morning-brief", "name": "Morning brief", "schedule": "daily 09:00", "grace_min": 40}
      schedule is "daily HH:MM" or "weekly mon HH:MM" (in timezone_offset_hours)
  - delivery_log: what actually arrived, one JSON object per line, written by
    whatever sends the output (not by the agent that wrote it)
      {"id": "morning-brief", "at": "2026-10-28T01:12:00Z"}

For a given date it prints one row per expected delivery:
  ✅ on time · 🟡 late (arrived after the grace window) · ❌ missing · ⏳ not due yet
Exit 1 when anything is missing.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import opsconfig

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def due_time(schedule, day, tz):
    """Return the due datetime on `day` (a date), or None if not scheduled that day."""
    parts = schedule.split()
    if parts[0] == "daily" and len(parts) == 2:
        hhmm = parts[1]
    elif parts[0] == "weekly" and len(parts) == 3:
        if DAYS.index(parts[1].lower()[:3]) != day.weekday():
            return None
        hhmm = parts[2]
    else:
        raise ValueError(f"bad schedule: {schedule!r} (use 'daily HH:MM' or 'weekly mon HH:MM')")
    hour, minute = map(int, hhmm.split(":"))
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=tz)


def load_deliveries(path):
    deliveries = {}
    if not os.path.exists(path):
        return deliveries
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            at = datetime.fromisoformat(row["at"].replace("Z", "+00:00"))
            deliveries.setdefault(row["id"], []).append(at)
    return deliveries


def judge(expectation, deliveries, day, tz, now):
    due = due_time(expectation["schedule"], day, tz)
    if due is None:
        return None
    grace = due + timedelta(minutes=int(expectation.get("grace_min", 30)))
    # a delivery counts for this shift from one hour before it is due until one hour before
    # the same time tomorrow, so an early run of tomorrow's shift is never counted twice
    window = (due - timedelta(hours=1), due + timedelta(hours=23))
    hits = [t for t in deliveries.get(expectation["id"], []) if window[0] <= t < window[1]]
    if any(t <= grace for t in hits):
        return "✅", "on time", due
    if hits:
        return "🟡", f"late, arrived {min(hits).astimezone(tz):%H:%M}", due
    if now < grace:
        return "⏳", "not due yet", due
    return "❌", f"missing, nothing by {grace:%H:%M}", due


def main(argv=None):
    p = argparse.ArgumentParser(description="Did every expected delivery arrive?")
    p.add_argument("--config")
    p.add_argument("--date", help="YYYY-MM-DD in the configured timezone (default: today)")
    args = p.parse_args(argv)
    cfg = opsconfig.load(args.config)
    tz = opsconfig.local_tz(cfg)
    now = opsconfig.now_utc()
    day = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else now.astimezone(tz).date()

    with open(opsconfig.resolve(cfg, "expectations_file"), encoding="utf-8") as f:
        expectations = json.load(f)["expectations"]
    deliveries = load_deliveries(opsconfig.resolve(cfg, "delivery_log"))

    print(f"| | Delivery | Due | Result |\n|---|---|---|---|")
    missing = 0
    for exp in expectations:
        verdict = judge(exp, deliveries, day, tz, now)
        if verdict is None:
            continue
        mark, text, due = verdict
        missing += mark == "❌"
        print(f"| {mark} | {exp['name']} | {due:%Y-%m-%d %H:%M} | {text} |")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
