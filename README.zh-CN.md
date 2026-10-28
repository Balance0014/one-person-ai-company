# 一人 AI 公司

[English](README.md) · **中文**

**一个人用 18 个 Claude Code 会话、约 20 个定时 AI 任务开公司，翻过车之后总结的 8 条经验。**

我一个人开公司。干活的是 18 个长期在跑的 Claude Code 会话（每个项目、每位负责人一个），外加大约 20 个定时任务，各自跑各自的提示词。它们写加密货币和 AI 方向的投研简报，给我的社交账号起草帖子，开发、维护我在做的产品 [GapMine](https://gapmine.com)。产出大多每天早上发到我看的一个群里。

这个仓库是我一路踩坑后留下来的那套管理办法：agent 怎么分层、会话被清空了活怎么不丢、怎么确认东西真发出去了、哪些规矩交给机器去拦。一共 8 章，附模板、4 个零依赖的 Python 检查脚本，还有一个 agent 技能（Skill），能帮你在自己的仓库里把这套搭起来。

[![CI](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml/badge.svg)](https://github.com/Balance0014/one-person-ai-company/actions/workflows/ci.yml) ![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat) ![Python 3.9+ standard library](https://img.shields.io/badge/python-3.9%2B%20stdlib%20only-3776AB?style=flat)

---

## 翻过的车

这里的每一条，都是下面某件事发生之后才加上的：

- agent 说活干完了，理由是「没发现报错」。其实什么都没发出去。
- 会话做到一半撞上周额度（Claude 订阅每周的用量上限），前面攒下的上下文全跟着聊天记录没了。
- 有几天开发太猛，把周额度烧光了，我每天早上的简报停了四天。
- 负责通知我「哪项产出没到」的那个任务，和被它盯的任务跑在同一个账号上。额度一断它也哑了，我整整五天什么都不知道。
- 同一条规矩，定时任务的提示词里一份、仓库里一份，两份慢慢就对不上了。
- 我自己的监控一周给我发了 28 条消息，没有一条是我能处理的。

## 怎么组织的

<p align="center"><img src="docs/org-chart.zh-CN.svg" alt="组织架构：我在最上面，下面是总部、四位负责人和各自的项目。总部能读每个项目的记录，但只给负责人派活。" width="760"></p>

总部是一个 agent 会话，管通用规矩、各本账、额度，还管着回答「到底发没发出去」的对账脚本。它只给四位负责人（内容、研究、产品、基础设施各一位 agent）派活，负责人各自管自己的项目。除了坏消息和产品上的事，agent 只在四类事上找我：花钱、删了找不回来的东西、改我定过的规矩、对外发布。其余见[第 1 章](playbook/zh-CN/01-org-chart.md)。

## 8 章

| 章节 | 解决什么 | 配套 |
|---|---|---|
| [1 · 组织架构：谁跟谁说话](playbook/zh-CN/01-org-chart.md) | 所有 agent 都直接找你，每条规矩都抄进每份提示词 | 岗位卡、决策记录模板 |
| [2 · 派活账](playbook/zh-CN/02-dispatch-ledger.md) | 活丢在聊天里 | `scripts/dispatch.py` |
| [3 · 交接记录](playbook/zh-CN/03-handoff-records.md) | 会话一断，上下文跟着没了 | `scripts/handoff_check.py` |
| [4 · 一个问题一个裁判](playbook/zh-CN/04-one-judge-per-question.md) | agent 自己给自己判卷 | `scripts/reconcile.py` |
| [5 · 完成的定义](playbook/zh-CN/05-definition-of-done.md) | 「修好了」其实是「试了一次没报错」 | `dispatch.py done` |
| [6 · 额度预算](playbook/zh-CN/06-quota-budget.md) | 开发把要紧的定时任务挤掉 | 预算模板 |
| [7 · 规矩要变成闸](playbook/zh-CN/07-rules-become-gates.md) | 规矩悄悄没人管了 | `scripts/rules_check.py` |
| [8 · 有记性的报警](playbook/zh-CN/08-alerts-that-remember.md) | 报警太多没人看，或者看了也没人能处理 | 报警上线前要答的三个问题 |

## 我这套现在的数字（截至 2026 年 10 月 28 日）

| | |
|---|---|
| agent | 18 个长期在跑的 Claude Code 会话（总部、四位负责人和他们的项目），另有 6 个暂停的，加上约 20 个定时任务 |
| 架构 | 总部、4 位负责人、45 张岗位卡（每个角色一张，定时任务和暂停的项目也算在内） |
| 定时产出 | 21 项（日更和周更），每天对两次账。对账脚本不调用任何模型，跑在一台单独的小服务器上 |
| 规矩 | 登记 170 条：82 条写明了由哪个脚本拦，41 条定时查，47 条靠自觉 |
| 派活账 | 六周 67 件：33 件带齐五样证据（见[第 5 章](playbook/zh-CN/05-definition-of-done.md)）关单，8 件写明理由拒掉，26 件还没关 |
| 交接记录 | 24 份，每个 agent 会话一份，暂停的也算。其中 15 份做过演练：开一个没有任何聊天记录的新会话，只给它仓库，让它说出每个项目做到哪、下一步做什么，再和真实情况逐条对 |

失败也照写了，带着日期，包括还没解决的。

## 30 秒看效果

只要 Python 3.9+，什么都不用装：

```bash
git clone https://github.com/Balance0014/one-person-ai-company
cd one-person-ai-company/examples
python3 ../scripts/reconcile.py --date 2026-10-27
python3 ../scripts/handoff_check.py
python3 ../scripts/rules_check.py
```

```
| | Delivery | Due | Result |
|---|---|---|---|
| ❌ | Morning brief | 2026-10-27 09:00 | missing, nothing by 09:40 |

✓ content.md
✗ research.md
    - missing section "## In progress"
    ...
✗ R-06: enforcer scripts/link_gate.py does not exist — Posts with broken links never ship
```

示例数据是故意做成会报错的，一跑就能看到每个检查在抓什么。

## 用到你自己的仓库

**装成 agent 技能**（需要 Node.js 22.20 及以上）：

```bash
npx skills add https://github.com/Balance0014/one-person-ai-company
```

然后对你的 agent 说：「在这个仓库里搭好一人 AI 公司的结构。」它会复制模板、问你有哪几位负责人、和你一起写好岗位卡和交接记录，再把四个检查跑一遍。每次更新，CI 都会用这条命令真装一遍。技能用的是开放的 `SKILL.md` 格式，不过我只在 Claude Code 上用过。

**手动：** 把 `templates/ops`、`templates/ops.config.json` 和 `scripts/` 复制到你的仓库，在仓库根目录跑：

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

有东西没到、超期或坏了，退出码就是 1（晚到只算提醒），可以直接放进定时任务或 CI。Claude Code 把退出码 2 当作「拦下」（其他非 0 的退出码不拦），要在钩子里用就包一层：`python3 scripts/handoff_check.py --record content.md --repo . >&2 || exit 2`。

路径都在 `ops.config.json` 里配，没有写死的。测试正反两头都测：好的输入放过，坏的输入报错（`python3 -m unittest discover tests`）。

## 四个检查

| 脚本 | 回答什么 | 调用模型 |
|---|---|---|
| `dispatch.py` | 哪些活没关、归谁、哪些超期了。没认领过的、五样证据缺一样的，都不让关单 | 0 |
| `handoff_check.py` | 每份交接记录有没有时间、七项标题齐不齐；加上 `--record` 和 `--repo`，再查这个项目有没有比记录新 15 分钟以上的提交。记录写得对不对它看不出来，那要靠演练 | 0 |
| `reconcile.py` | 每项定时产出有没有按时到，以发送方记下的为准 | 0 |
| `rules_check.py` | 标成机器挡或定时查的规矩，执行脚本还在不在、里面还有没有你选的标记字符串 | 0 |

## 局限

- 方法就是我在用的那套。脚本是重新写的干净版，因为我自己在用的那套绑着我的服务器和账号，所以这里故意做得很小。
- 检查只看得见你写下来的东西。没登记进 `EXPECTATIONS.json` 的产出，没到也不会报。
- `rules_check.py` 只查拦截脚本还在、里面还有你选的标记字符串，证明不了它真的接进了钩子。
- 这些检查不会自己跑，要你自己接进钩子、定时任务或 CI。规矩登记表的模板在你接好之前，每条都先算靠自觉。
- 时间用的是固定的 UTC 时差（`timezone_offset_hours`），有夏令时的地方切换时要手动改。

## 关于我

我是 [Balance Zhao](https://github.com/Balance0014)，做了很多年增长，后来自己动手做产品。这个仓库就是我自己在用的那套方法，去掉了所有公司内部的细节。后面还会陆续开源，想看下一个就[在 X 上关注我](https://x.com/balance0014)。

## 许可

MIT
