# 7 · Rules become gates

## The problem

You write a rule into an agent's instructions. It works for a week. Then the instructions get long, the rule gets skimmed, and the behavior comes back. Or someone rewrites the script that enforced it, and the rule is still written down but nothing checks it any more.

## The rule

Every rule, the day it is created, says which tier it is:

| Tier | Meaning |
|---|---|
| `gate` | A machine blocks the wrong action: a hook, a pre-commit check, a CI step |
| `scheduled` | A job checks it on a timer and reports |
| `advisory` | It relies on discipline. Say so honestly |

- Gate and scheduled rules name the file that enforces them and a string that must appear in it.
- **Claiming a gate that does not exist is worse than having no rule.**
- **One fact, one home.** A rule lives in exactly one file. Everywhere else holds only a pointer to it. Two hand-edited copies of the same fact will always drift apart.
- **Change it, then connect it.** Before changing a rule or script, list everything downstream that reads it; after changing it, check each one.
- Keep always-loaded instruction files short (we cap them at about 200 lines). Long ones get skimmed.

Template: [`templates/ops/RULES-REGISTRY.json`](../templates/ops/RULES-REGISTRY.json).

## How to check it

```bash
python3 scripts/rules_check.py
```

```
4 rules: 3 gate · 0 scheduled · 1 advisory
✗ R-06: enforcer scripts/link_gate.py does not exist — Posts with broken links never ship
```

Run it when each session starts. A dead gate shows up the same day it dies.

## What it costs

Nothing to run. Writing the registry entry takes a minute per rule.
