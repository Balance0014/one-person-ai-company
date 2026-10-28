# 7 · Rules become gates

One of my content rules was registered as "checked on a schedule." When the registry check went looking for the script that runs it, there wasn't one. The rule had been sitting in a file for almost two weeks, enforced by nothing.

That's the usual way rules die. You write one into an agent's instructions and it works for a week. Then the instructions get long, the rule gets skimmed, and the old behavior comes back. Or someone rewrites the script that enforced it, and the rule is still written down but nothing checks it.

## Tiers

Every rule says which tier it's in on the day it's created:

| Tier | Meaning |
|---|---|
| `gate` | A machine blocks the wrong action: a hook, a pre-commit check, a CI step |
| `scheduled` | A job checks it on a timer and reports |
| `advisory` | It relies on discipline, and the registry says so |

- Gate and scheduled rules name the file that enforces them, plus a string that must appear in it.
- Claiming a gate that doesn't exist is worse than having no rule.
- Each fact lives in one file. Everywhere else holds a pointer to it. Two hand-edited copies of the same fact always drift apart.
- Before changing a rule or a script, list everything downstream that reads it. After the change, check each one.
- Keep always-loaded instruction files short. I cap mine at about 200 lines, because past that they get skimmed.

Template: [`templates/ops/RULES-REGISTRY.json`](../templates/ops/RULES-REGISTRY.json).

## Checking it

```bash
python3 scripts/rules_check.py
```

```
4 rules: 3 gate · 0 scheduled · 1 advisory
✗ R-06: enforcer scripts/link_gate.py does not exist — Posts with broken links never ship
```

Run it at the start of every session and a dead gate shows up the day it dies. It confirms the enforcing script exists and contains the check. It can't prove the script is actually wired into a hook, so that part is still on you.

## Where I am

Across HQ and four leads I have 170 registered rules. 82 name the script that blocks them (48%), 41 are checked on a schedule (24%), and 47 rely on discipline (28%), including the content rule above. Those 47 are the to-do list.
