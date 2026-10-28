#!/usr/bin/env python3
"""Rules become gates: a rule nobody enforces is a sticky note.

Every rule in the registry declares how it is enforced:
  gate       a machine blocks the wrong action (hook, CI check, pre-commit)
  scheduled  a job checks it on a timer and reports
  advisory   it relies on discipline (be honest: say so)

For gate and scheduled rules the registry names the file that enforces it
(enforced_by) and a string that must appear in that file (marker). This script
checks that each of those files still exists and still contains its marker.
When someone deletes or rewrites the enforcer, the rule is dead even though it
is still written down; this is how you find out the same day.

Exit 1 when any gate or scheduled rule is dead.
"""

import argparse
import json
import os
import sys

import opsconfig

TIERS = ("gate", "scheduled", "advisory")


def check(registry, root):
    dead, counts = [], {t: 0 for t in TIERS}
    for rule in registry["rules"]:
        tier = rule.get("tier")
        if tier not in TIERS:
            dead.append(f"{rule.get('id')}: unknown tier {tier!r}")
            continue
        counts[tier] += 1
        if tier == "advisory":
            continue
        path = rule.get("enforced_by", "")
        full = path if os.path.isabs(path) else os.path.join(root, path)
        if not path or not os.path.exists(full):
            dead.append(f"{rule['id']}: enforcer {path or '(none)'} does not exist — {rule['rule']}")
            continue
        with open(full, encoding="utf-8", errors="ignore") as f:
            if rule.get("marker", "") not in f.read():
                dead.append(f"{rule['id']}: marker {rule.get('marker')!r} not found in {path} — {rule['rule']}")
    return dead, counts


def main(argv=None):
    p = argparse.ArgumentParser(description="Check that every enforced rule still has a live enforcer")
    p.add_argument("--config")
    args = p.parse_args(argv)
    cfg = opsconfig.load(args.config)
    with open(opsconfig.resolve(cfg, "rules_file"), encoding="utf-8") as f:
        registry = json.load(f)
    dead, counts = check(registry, opsconfig.resolve(cfg, "rules_root"))
    print(f"{sum(counts.values())} rules: {counts['gate']} gate · {counts['scheduled']} scheduled · {counts['advisory']} advisory")
    for line in dead:
        print("✗ " + line)
    if not dead:
        print("all enforcers alive")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
