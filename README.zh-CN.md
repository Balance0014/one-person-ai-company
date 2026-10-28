# 一人 AI 公司

[English](README.md) · **中文**

**管 30 多个 AI agent 的 8 条规矩，每一条都来自一次真实的翻车。**

我一个人开公司。干活的是 18 个长期在跑的 Claude Code 会话（每个项目、每位负责人一个），外加大约 20 个定时任务，各自跑各自的提示词。它们写加密和 AI 投研简报，给我的社交账号起草帖子，开发和盯着我在做的产品 [GapMine](https://gapmine.com)。产出大多每天早上直接发到我的聊天群里。

这个仓库是我一路踩坑后留下来的那套管理办法：agent 怎么分层、会话被清空了活怎么不丢、怎么确认东西真发出去了、哪些规矩交给机器去拦。一共 8 章，附模板、4 个零依赖的 Python 检查脚本，还有一个能在你的仓库里一键搭好这套的 agent 技能。

[![CI](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml/badge.svg)](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml) ![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat) ![Python 3.9+ standard library](https://img.shields.io/badge/python-3.9%2B%20stdlib%20only-3776AB?style=flat) ![Used daily with Claude Code](https://img.shields.io/badge/used%20daily%20with-Claude%20Code-111827?style=flat)

---

## 先坏掉的那些事

这里的每一条，都是下面某件事发生之后才加上的：

- agent 说活干完了，理由是「没发现报错」。其实什么都没发出去。
- 会话做到一半撞上周额度上限，它知道的一切跟着聊天记录一起没了。
- 有几天开发太猛，把周额度烧光了，我每天早上的简报停了四天。
- 负责通知我「哪班没到」的那个任务，和被它盯的任务跑在同一个账号上。额度一断它也哑了，我整整五天什么都不知道。
- 同一条规矩，定时任务的提示词里一份、仓库里一份，没过几周两份就对不上了。
- 我自己的监控一周给我发了 28 条消息，没有一条是我能处理的。

## 怎么组织的

<p align="center"><img src="docs/org-chart.zh-CN.svg" alt="组织架构：我在最上面，下面是总部、四位负责人和各自的项目。总部能读每个项目的记录，但只给负责人派活。" width="760"></p>

总部是一个 agent 会话，管通用规矩、各本账、额度，以及「到底发没发出去」由谁说了算。它只给四位负责人派活，负责人各自管自己的项目。agent 只在四类事上找我：花钱、删了找不回来的东西、改我定过的规矩、对外发布。其余见[第 1 章](playbook/zh-CN/01-org-chart.md)。

## 8 章

| 章节 | 解决什么 | 配套 |
|---|---|---|
| [1 · 组织架构与沟通线](playbook/zh-CN/01-org-chart.md) | 所有 agent 都直接找你，每条规矩都抄进每份提示词 | 岗位卡、决策记录模板 |
| [2 · 派活账](playbook/zh-CN/02-dispatch-ledger.md) | 活丢在聊天里 | `scripts/dispatch.py` |
| [3 · 交接记录](playbook/zh-CN/03-handoff-records.md) | 会话一断，上下文跟着没了 | `scripts/handoff_check.py` |
| [4 · 一个问题一个裁判](playbook/zh-CN/04-one-judge-per-question.md) | agent 自己给自己判卷 | `scripts/reconcile.py` |
| [5 · 完成的定义](playbook/zh-CN/05-definition-of-done.md) | 「修好了」其实是「试了一次没报错」 | `dispatch.py done` |
| [6 · 额度预算](playbook/zh-CN/06-quota-budget.md) | 开发把要紧的定时任务挤掉 | 预算模板 |
| [7 · 规矩要变成闸](playbook/zh-CN/07-rules-become-gates.md) | 规矩悄悄没人管了 | `scripts/rules_check.py` |
| [8 · 有记性的报警](playbook/zh-CN/08-alerts-that-remember.md) | 报警太多没人看，或者看了也没人能处理 | 报警上线前要答的三个问题 |


## 我自己这套的真实数字（2026 年 10 月 28 日）

| | |
|---|---|
| agent | 18 个长期在跑的 Claude Code 会话（每位负责人、每个项目一个），另有约 20 个定时任务 |
| 架构 | 总部、4 位负责人、45 张岗位卡（每个角色一张，定时任务和暂停的项目也算在内） |
| 定时产出 | 21 项（日更和周更），每天对两次账。对账脚本不调用任何模型，跑在单独的一台小服务器上 |
| 规矩 | 登记 170 条：82 条写明了由哪个脚本拦，41 条定时查，47 条靠自觉 |
| 派活账 | 六周 67 件：33 件带齐五样证据关单，8 件写明理由拒掉，26 件还没关 |
| 交接记录 | 24 份，每个 agent 会话一份，暂停的也算。其中 15 份做过演练：把仓库交给一个没有任何聊天记录的新会话，再和真实情况逐条对 |

最糟的一次也写进去了：停摆 18 天，对账脚本几乎每天早上都报对了，报警却点了一个同样停掉的「负责人」（见[第 4 章](playbook/zh-CN/04-one-judge-per-question.md#那-18-天)）。

## 30 秒看效果

只要 Python 3.9+，什么都不用装：

```bash
git clone https://github.com/Balance0014/one-person-ai-company
cd one-person-ai-company/examples
python3 ../scripts/reconcile.py --date 2026-10-27
python3 ../scripts/handoff_check.py
python3 ../scripts/rules_check.py
```

示例数据是故意做成会报错的，一跑就能看到每个检查在抓什么。

## 用到你自己的仓库

**作为 agent 技能**，这条命令需要 Node.js 22.20 或更新版本：

```bash
npx skills add https://github.com/Balance0014/one-person-ai-company
```

然后对你的 agent 说：「在这个仓库里搭好一人 AI 公司的结构。」它会复制模板、问你有哪几位负责人、写好岗位卡和交接记录，再把四个检查跑一遍。每次更新，CI 都会用这条命令真装一遍。技能用的是开放的 `SKILL.md` 格式，不过我只在 Claude Code 上用过。

**手动：** 把 `templates/ops`、`templates/ops.config.json` 和 `scripts/` 复制到你的仓库，在仓库根目录跑：

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

有东西没到、超期或坏了就返回 1（晚到只算提醒），可以直接放进定时任务或 CI。Claude Code 的钩子只在返回码为 2 时拦，要在钩子里用就包一层：`python3 scripts/handoff_check.py --record content.md --repo . >&2 || exit 2`。路径都在 `ops.config.json` 里配，没有写死的。测试正反两头都测：好的输入放过，坏的输入报错（`python3 -m unittest discover tests`）。

## 局限

- 这些脚本是重新写的干净版。我自己在用的那套绑着我的服务器和账号，所以这里故意做得很小。
- 检查只看得见你写下来的东西。没登记进 `EXPECTATIONS.json` 的产出，没到也不会报。
- `rules_check.py` 只查拦截脚本还在、里面还有你选的标记字符串，证明不了它真的接进了钩子。
- 它不会自己跑起来。检查要你自己接进钩子、定时任务或 CI。

## 关于我

我是 [Balance Zhao](https://github.com/Balance0014)，做了很多年增长，后来自己动手做产品。这个仓库就是我自己在用的那套，去掉了所有公司内部的细节。后面还会陆续开源，想看下一个就[在 X 上关注我](https://x.com/balance0014)。

## 许可

MIT
