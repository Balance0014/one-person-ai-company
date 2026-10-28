# 1 · Org chart and who talks to whom

**English** · [中文](zh-CN/01-org-chart.md)

Somewhere past a dozen agents I lost track. Every agent reported to me, every rule was pasted into every prompt, and before long the copies disagreed. I'd become the bottleneck, and the message that mattered looked like all the others.

So I set the agents up like a small company with three layers.

<p align="center"><img src="../docs/org-chart.svg" alt="Org chart: me at the top, HQ below, four leads, and their projects. HQ can read every project's records but gives work only to the leads." width="760"></p>

| Layer | Who | Owns |
|---|---|---|
| HQ | One coordinating agent session | Shared rules, the ledgers, quota, and the reconciler that answers "did it arrive?" The reconciler runs outside the AI account and is the only way bad news reaches me |
| Leads | One agent per business area. I have four: content, research, product, and infrastructure | Their area's quality bar, their own checks, scheduling and assigning work |
| Projects | One agent session per project | The work itself. They take direction from their lead |

HQ doesn't write product code or judge content. If it spots a problem inside an area, it tells that area's lead and leaves the fix to them, even when fixing it directly would be faster.

## Where I sit

The layers exist so that I talk to fewer agents, less often, about things only I can decide.

- I settle product questions directly with the lead who owns the product. HQ doesn't relay them (relays lose detail) and doesn't decide for me.
- Bad news reaches me through one channel (see [chapter 4](04-one-judge-per-question.md)).
- HQ brings me the decisions only I can make: spending money, deleting anything unrecoverable, changing a rule I set, and publishing anything. Everything else gets done first and reported afterward.
- Agents check before they ask. I keep a decision log with the date, my exact words, and what changed ([`templates/ops/DECISIONS.md`](../templates/ops/DECISIONS.md)). If the answer's already in there, they act on it instead of asking me again.
- Agents lead with the answer, in plain language, and skip the play-by-play.

## Who talks to whom

| Direction | Rule |
|---|---|
| Down | HQ gives work only to leads, never directly to a lead's projects. Leads run their own projects. |
| Up | Only leads report to HQ, and only about their own area. |
| Across | Anything that spans two areas goes through HQ. |
| Reading | HQ can read any project's raw logs, delivery records, and commits without asking, so problems can't hide behind a lead. |

Tasks and conclusions go in the [dispatch ledger](02-dispatch-ledger.md), and the recipient reads them when it finishes what it's doing. A direct message is for two cases only: someone needs a decision now, or someone is blocked. A day's small items go out as one message. Nobody sets an alarm to keep checking on another agent. I once had agents woken every 20 minutes; [chapter 5](05-definition-of-done.md) has what that cost.

## Rules live in one place

HQ sets rules about how to work: what "done" means, quota, handoffs, how to talk to me. Leads set rules about what good looks like in their area. A lower layer can add rules but never copies or contradicts a higher one. If two rules conflict, HQ wins on process, the lead wins on business calls, and the fix happens in one file.

## Role cards

Every role has four lines at the top of its own instruction file: what it delivers, what it owns, how good is good enough, and what enforces that. Template: [`templates/ROLE-CARD.md`](../templates/ROLE-CARD.md).

The "delivers" line has to describe a result you can check. My reviewer agents' cards don't list the six questions they ask; they say every draft they approve is accurate and ready to publish. I have 45 of these cards, one per role, including scheduled jobs and paused projects, and a scheduled check flags any card whose "delivers" line just points somewhere else.
