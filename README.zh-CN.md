# 一人 AI 公司

[English](README.md) · **中文**

**我一个人带着 30 多个 AI agent 跑一家公司，这是背后那套管理办法，整理成了你能直接拿去用的版本。** 组织架构、派活账、交接记录、到没到的对账、完成的定义、额度预算，以及真正由机器执行的规矩。附模板、四个小检查脚本，还有一个能帮你一键搭好的 agent 技能。

---

## 为什么做这个

管一个 agent 很简单，管三十个就是管理问题。这里每一样东西，都来自一次真实踩过的坑：

- agent 说「做完了」，依据是「没发现错误」，其实什么都没发出去。
- 账号周额度在任务做到一半时用完，agent 知道的一切跟着聊天记录一起没了。
- 开发把整周额度吃光，大家等着看的定时报告连停四天。
- 本该报告故障的那个报警，跑在已经挂掉的那个东西上。
- 同一条规矩抄在三个 agent 的说明里，一个月后变成了三条不同的规矩。
- 一个报警每小时响一次，响到没人看，真出事那天也没人看。

## 里面有什么

| 章节 | 解决什么 | 配套 |
|---|---|---|
| [1 · 三层组织架构](playbook/01-org-chart.md) | 所有人都直接找你；规矩到处抄 | 岗位卡模板 |
| [2 · 派活账](playbook/02-dispatch-ledger.md) | 活丢在聊天里 | `scripts/dispatch.py` |
| [3 · 交接记录](playbook/03-handoff-records.md) | 账号或额度一断，上下文全没 | `scripts/handoff_check.py` |
| [4 · 一个问题一个裁判](playbook/04-one-judge-per-question.md) | agent 自己给自己判卷 | `scripts/reconcile.py` |
| [5 · 完成的定义](playbook/05-definition-of-done.md) | 「修好了」其实是「试了一次没报错」 | `dispatch.py done` 强制执行 |
| [6 · 额度预算](playbook/06-quota-budget.md) | 开发挤掉真正要紧的定时任务 | 预算模板 |
| [7 · 规矩要变成闸](playbook/07-rules-become-gates.md) | 规矩悄悄失效 | `scripts/rules_check.py` |
| [8 · 有记性的报警](playbook/08-alerts-that-remember.md) | 报警疲劳 | 上线前三问 |

章节正文目前是英文。

## 30 秒看效果

不用安装，只要 Python 3.9+ 和自带的标准库：

```bash
git clone https://github.com/Balance0014/one-person-ai-company
cd one-person-ai-company/examples
python3 ../scripts/reconcile.py --date 2026-10-27
python3 ../scripts/handoff_check.py
python3 ../scripts/rules_check.py
```

示例数据是故意做成会报错的，方便你一眼看懂每个检查在抓什么。

## 用到你自己的仓库

**作为 agent 技能**（Claude Code、Codex 等能读 `SKILL.md` 的 agent）：

```bash
npx skills add https://github.com/Balance0014/one-person-ai-company
```

然后对你的 agent 说：「在这个仓库里搭好一人 AI 公司的结构。」它会复制模板、问你有哪几位负责人、写好岗位卡和交接记录，再把四个检查跑一遍。

**手动：** 把 `templates/ops`、`templates/ops.config.json` 和 `scripts/` 复制到你的仓库，在仓库根目录跑：

```bash
python3 scripts/dispatch.py overdue
python3 scripts/handoff_check.py --repo .
python3 scripts/reconcile.py
python3 scripts/rules_check.py
```

有问题就返回 1，可以直接接进钩子、定时任务或 CI。四个脚本都不调用模型，路径全在 `ops.config.json` 里配置，没有写死的路径。测试正反两个方向都覆盖：`python3 -m unittest discover tests`。

## 作者

我是 [Balance Zhao](https://github.com/Balance0014)，市场运营出身的开发者。我带着 30 多个 agent 写文章、做投研、调研产品、维护我自己 vibe coding 的产品，包括 [GapMine](https://gapmine.com)。这个仓库就是这套做法，去掉了所有公司内部的细节。

更多方法会陆续开源，[在 X 上关注我](https://x.com/balance0014)。

## 许可

MIT
