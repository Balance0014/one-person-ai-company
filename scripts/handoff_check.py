#!/usr/bin/env python3
"""Handoff records: if the account or the quota dies mid-task, a brand-new
session with no chat history must be able to pick the work up from the repo.

Each workstream keeps one Markdown file in handoff_dir. This script checks:
  1. The first line says when it was last updated:  "Updated YYYY-MM-DD HH:MM"
     (in the timezone set by timezone_offset_hours).
  2. All seven sections exist (exact headings below).
  3. Optional --repo PATH: the record is not older than the latest commit in
     that repo by more than handoff_stale_hours. Work that is committed but
     not written down is exactly what gets lost.

Exit 1 if any record fails, so it can run as a stop hook or in CI.
"""

import argparse
import glob
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import opsconfig

SECTIONS = [
    "## Done",
    "## In progress",
    "## Not done",
    "## Next",
    "## Blocked on",
    "## Branches",
    "## Uncommitted or unpushed",
]
STAMP = re.compile(r"Updated\s+(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})")


def last_commit_time(repo):
    out = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%ct"],
                         capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return datetime.fromtimestamp(int(out.stdout.strip()), timezone.utc)


def check_record(path, cfg, repo=None):
    problems = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    first = next((line for line in text.splitlines() if line.strip()), "")
    m = STAMP.search(first)
    updated = None
    if not m:
        problems.append('first line must be "Updated YYYY-MM-DD HH:MM"')
    else:
        updated = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H:%M")
        updated = updated.replace(tzinfo=opsconfig.local_tz(cfg))
    lines = {line.strip() for line in text.splitlines()}
    for heading in SECTIONS:
        if heading not in lines:
            problems.append(f'missing section "{heading}"')
    if repo and updated:
        committed = last_commit_time(repo)
        stale = timedelta(hours=float(cfg["handoff_stale_hours"]))
        if committed and committed - updated > stale:
            problems.append(f"stale: last commit is {committed - updated} newer than the record")
    return problems


def main(argv=None):
    p = argparse.ArgumentParser(description="Check handoff records")
    p.add_argument("--config")
    p.add_argument("--dir", help="override handoff_dir from the config")
    p.add_argument("--repo", help="compare each record against this repo's latest commit")
    args = p.parse_args(argv)
    cfg = opsconfig.load(args.config)
    folder = args.dir or opsconfig.resolve(cfg, "handoff_dir")
    records = sorted(glob.glob(os.path.join(folder, "*.md")))
    if not records:
        print(f"no handoff records in {folder}")
        return 1
    failed = 0
    for path in records:
        problems = check_record(path, cfg, args.repo)
        name = os.path.basename(path)
        if problems:
            failed += 1
            print(f"✗ {name}")
            for item in problems:
                print(f"    - {item}")
        else:
            print(f"✓ {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
