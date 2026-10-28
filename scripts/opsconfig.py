"""Shared config loader for the ops scripts.

Every path lives in one file, ops.config.json, so the scripts carry no
hard-coded paths or account names. Paths in the config are relative to the
config file itself.

Lookup order: --config argument, then the OPS_CONFIG environment variable,
then ./ops.config.json. Missing keys fall back to DEFAULTS.
"""

import json
import os
from datetime import datetime, timedelta, timezone

DEFAULTS = {
    "dispatch_file": "ops/DISPATCH.json",
    "handoff_dir": "ops/handoff",
    "expectations_file": "ops/EXPECTATIONS.json",
    "delivery_log": "ops/deliveries.jsonl",
    "rules_file": "ops/RULES-REGISTRY.json",
    "rules_root": ".",
    "timezone_offset_hours": 0,
    "handoff_stale_hours": 2,
    "ack_hours": 24,
}


def load(path=None):
    cfg = dict(DEFAULTS)
    path = path or os.environ.get("OPS_CONFIG") or "ops.config.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            cfg.update(json.load(f))
        cfg["_base"] = os.path.dirname(os.path.abspath(path))
    else:
        cfg["_base"] = os.getcwd()
    return cfg


def resolve(cfg, key):
    value = cfg[key]
    return value if os.path.isabs(value) else os.path.join(cfg["_base"], value)


def local_tz(cfg):
    return timezone(timedelta(hours=float(cfg.get("timezone_offset_hours", 0))))


def now_utc():
    override = os.environ.get("OPS_NOW")  # lets tests pin the clock
    if override:
        return datetime.fromisoformat(override.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)
