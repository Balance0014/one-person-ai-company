# 1 · A three-layer org chart

## The problem

With five agents you can keep everything in your head. With thirty you cannot. Every agent reports straight to you, every rule is copied into every agent's instructions, and within a month the copies disagree. You become the bottleneck, and the inbox is noise.

## The rule

Run the agents like a company with three layers:

| Layer | Who | Owns |
|---|---|---|
| Head office | One coordinating agent session | Shared rules, the ledgers, the one judge of "did it arrive", the single channel for bad news, shared infrastructure and quota |
| Leads | One agent per business area (for example content, product, research) | That area's quality standards, its own checks, scheduling and assigning work |
| Workstreams | One agent session per project | Doing the work; they take direction from their lead |

Four habits keep it working:

1. **One line of command.** Head office talks only to leads. Leads talk to their workstreams. Nobody reaches past a layer to give orders.
2. **Read access is never taken away.** Head office can still read any workstream's real data (logs, delivery records, commits). Bad news must not be able to hide behind a layer.
3. **Rules live in one layer.** Head office sets rules for *how* to work (definition of done, quota, handoff). Leads set rules for *what good looks like* in their area. A lower layer may add rules but never copies or contradicts a higher one. When they collide: working discipline follows head office, business judgment follows the lead.
4. **Head office standardizes only what is costly to get wrong and invisible when right.** Business judgment stays with the leads.

## Role cards

Every role gets four lines at the top of its own instruction file: what it delivers, what it owns, how good is good enough, and what enforces it. Template: [`templates/ROLE-CARD.md`](../templates/ROLE-CARD.md).

"Delivers" must be a checkable result, never a list of steps. A reviewer agent's card does not say "answer these six questions". It says "responsible for every approved draft being correct and publishable".

## What it costs

Nothing to run. The cost is discipline: when you are tempted to fix a workstream yourself from head office, you hand it to the lead instead.
