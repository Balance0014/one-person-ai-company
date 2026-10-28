#!/usr/bin/env python3
"""Dispatch ledger: every task gets an ID, an owner, a status, and evidence.

Chat messages get lost. A task that lives only in a conversation dies with
that conversation. The ledger is a plain JSON file in your repo, so any
agent (or a fresh session on a new account) can see what is open.

Usage:
  dispatch.py add --to OWNER --title TEXT [--due-days N]
  dispatch.py ack ID --plan TEXT
  dispatch.py done ID --root-cause T --prevention T --sweep T --verification T --cleanup T
  dispatch.py reject ID --reason TEXT
  dispatch.py list [--to OWNER] [--open]
  dispatch.py overdue

Status flow: new -> acked -> done | rejected.
`done` is refused unless all five definition-of-done fields are filled in.
If one truly does not apply, write "n/a: <reason>". An empty field is not allowed.
`overdue` exits 1 when anything is unacknowledged past ack_hours or unfinished
past its due date, so you can run it on a schedule.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import opsconfig

DONE_FIELDS = ["root_cause", "prevention", "sweep", "verification", "cleanup"]


def load_ledger(path):
    if not os.path.exists(path):
        return {"items": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_ledger(path, ledger):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def find(ledger, item_id):
    for item in ledger["items"]:
        if item["id"] == item_id:
            return item
    sys.exit(f"no task with id {item_id}")


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def next_id(ledger, now):
    prefix = now.strftime("D-%Y%m%d-")
    used = [int(i["id"].rsplit("-", 1)[1]) for i in ledger["items"] if i["id"].startswith(prefix)]
    return f"{prefix}{(max(used) + 1) if used else 1:02d}"


def main(argv=None):
    p = argparse.ArgumentParser(description="Dispatch ledger")
    p.add_argument("--config")
    p.add_argument("--ledger", help="override dispatch_file from the config")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--to", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--due-days", type=int, default=3)

    k = sub.add_parser("ack")
    k.add_argument("id")
    k.add_argument("--plan", required=True)

    d = sub.add_parser("done")
    d.add_argument("id")
    for field in DONE_FIELDS:
        d.add_argument("--" + field.replace("_", "-"), default="")

    r = sub.add_parser("reject")
    r.add_argument("id")
    r.add_argument("--reason", required=True)

    ls = sub.add_parser("list")
    ls.add_argument("--to")
    ls.add_argument("--open", action="store_true")

    sub.add_parser("overdue")

    args = p.parse_args(argv)
    cfg = opsconfig.load(args.config)
    path = args.ledger or opsconfig.resolve(cfg, "dispatch_file")
    ledger = load_ledger(path)
    now = opsconfig.now_utc()

    if args.cmd == "add":
        item = {
            "id": next_id(ledger, now),
            "to": args.to,
            "title": args.title,
            "status": "new",
            "created_at": iso(now),
            "due_days": args.due_days,
            "log": [],
        }
        ledger["items"].append(item)
        save_ledger(path, ledger)
        print(item["id"])
        return 0

    if args.cmd == "ack":
        item = find(ledger, args.id)
        if item["status"] != "new":
            sys.exit(f"{args.id} is {item['status']}, only new tasks can be acknowledged")
        item.update(status="acked", acked_at=iso(now))
        item["log"].append({"at": iso(now), "plan": args.plan})
        save_ledger(path, ledger)
        print(f"{args.id} acked")
        return 0

    if args.cmd == "done":
        item = find(ledger, args.id)
        if item["status"] not in ("new", "acked"):
            sys.exit(f"{args.id} is already {item['status']}")
        evidence = {f: getattr(args, f).strip() for f in DONE_FIELDS}
        missing = [f for f, v in evidence.items() if not v]
        if missing:
            sys.exit("refused: definition of done is missing " + ", ".join(missing)
                     + ' (write "n/a: <reason>" if one truly does not apply)')
        item.update(status="done", done_at=iso(now), evidence=evidence)
        save_ledger(path, ledger)
        print(f"{args.id} done")
        return 0

    if args.cmd == "reject":
        item = find(ledger, args.id)
        item.update(status="rejected", rejected_at=iso(now), reason=args.reason)
        save_ledger(path, ledger)
        print(f"{args.id} rejected")
        return 0

    if args.cmd == "list":
        for item in ledger["items"]:
            if args.to and item["to"] != args.to:
                continue
            if args.open and item["status"] in ("done", "rejected"):
                continue
            print(f"{item['id']}  [{item['status']:8}]  {item['to']:12}  {item['title']}")
        return 0

    if args.cmd == "overdue":
        ack_window = timedelta(hours=float(cfg["ack_hours"]))
        late = []
        for item in ledger["items"]:
            created = parse(item["created_at"])
            if item["status"] == "new" and now - created > ack_window:
                late.append(f"{item['id']}  not acknowledged after {cfg['ack_hours']}h  ({item['to']}: {item['title']})")
            elif item["status"] in ("new", "acked") and now - created > timedelta(days=item.get("due_days", 3)):
                late.append(f"{item['id']}  past due ({item['due_days']} days)  ({item['to']}: {item['title']})")
        for line in late:
            print(line)
        if not late:
            print("nothing overdue")
        return 1 if late else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
