<div align="center">

# Harness-Explore

#### 一个用 Codex 官方源码讲透 Agent Harness 的交互式学习 Skill

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)
[![Source Grounded](https://img.shields.io/badge/Source-Codex_Official-10B981?style=for-the-badge)](https://github.com/openai/codex)

![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Bootstrap-111827?style=flat-square&logo=gnubash&logoColor=white)
![Adaptive Learning](https://img.shields.io/badge/Learning-Adaptive-2563EB?style=flat-square)

</div>

Harness-Explore 是一套给 Agent 产品经理、设计师和工程协作者使用的交互式技术课程。

它先从机制讲起，再用选定版本的 Codex 官方源码解释真实 Harness 怎么实现，最后检查你能不能把原理、工程边界和产品决策连起来。

你不需要一次写很多。Skill 会逐题和你交流，记录理解状态，并根据回答动态调整课程顺序。

这里的 Agent Harness 指模型周围的运行系统：调用模型、管理状态、路由工具、执行权限约束、接收反馈和恢复任务。Harness Engineering 还包括让 Agent 能理解的环境、仓库知识与验证机制。课程会分别讨论模型、Harness、工具、执行环境和产品的职责。

## 2026-10-09 更新

- 补充到 2026 年 9 月的相关官方资料，记录发布日期、核查日期与适用边界，见 [一手资料索引](./harness-explore/references/official-sources.md)。
- 加入长任务交接、完成契约、trace/eval、Codex 集成方式，以及模型升级后的流程对照练习，见 [Harness 实践](./harness-explore/references/harness-practice.md)。
- 修复当前 Codex 源码中已变化的入口，补齐 ToolExecutor、app-server、SDK、恢复和遥测资料。
- bootstrap 支持固定源码版本、离线验证和只下载源码，并保存证据状态；学习方式可按用户目标调整，旧进度可继续使用。

本轮重点参考了 OpenAI 的 [Codex 平台化](https://developers.openai.com/blog/codex-as-a-platform)、[Agents API](https://openai.com/index/introducing-the-agents-api/)、[Skill 与提示词更新](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)，以及 Anthropic 的 [长任务 Harness 设计](https://www.anthropic.com/engineering/harness-design-long-running-apps)。这些是具体产品和实验的资料，教学建议与原文事实分别标注。

---

## 它解决什么

学习 Agent 技术时最容易出现几种问题：

- 记住了 Tool Use、Memory、MCP，却说不清一次调用实际怎么流转。
- 把模型能力、Harness 行为和产品流程混在一起。
- 看过很多产品案例，但无法判断方案为什么这样选。
- 会描述成功体验，却不会看 trace、badcase、permission config 或 eval case。
- 资料更新很快，旧文章里的 Codex 实现已经和当前源码不同。

Harness-Explore 的思路很简单：

**先理解机制，再读真实实现，最后训练工程沟通和产品判断。**

---

## 怎么工作

### 1. 准备当前证据

第一次运行时，Skill 会执行 `scripts/bootstrap_codex.sh`：

1. 拉取并核验选定版本的 Codex 核心源码。
2. 全局 CLI 不可用时，在独立缓存中安装最新官方 `@openai/codex`。
3. 获取官方网页 manual，失败时记录缺失或旧缓存状态。
4. 将实际源码 SHA、获取时间、CLI 版本和文档状态写入 `bootstrap-evidence.txt`，供每节课引用。

它不会修改用户已有的全局 Codex 安装，也不会下载整个源码仓库。核心源码清单写在 [`codex-source-files.txt`](./harness-explore/references/codex-source-files.txt)。

```bash
# 仅学习源码，跳过 CLI 安装
bash harness-explore/scripts/bootstrap_codex.sh --skip-cli

# 复用已下载资料，不联网、不安装
bash harness-explore/scripts/bootstrap_codex.sh --offline --skip-cli

# 固定已验证的源码版本，便于复现课程
HARNESS_EXPLORE_SOURCE_REF=2351d9e1b608e6f9d9a3699b71d7eb39ee41cfa4 \
  bash harness-explore/scripts/bootstrap_codex.sh --skip-cli
```

未指定版本时联网获取 `main`；离线模式复用已有 HEAD，不宣称最新。CLI 与源码分别标记版本。网页状态为 `downloaded`、`cached_stale` 或 `unavailable`，仓库文档可能只包含官网链接。源码清单失效会汇总缺项，更新失败保留原有缓存；已有源码目录有修改或来源不符时停止替换。

### 2. 做五题初始诊断

Skill 会逐题提出 5 道开放简答题，检查：

- Agent、Harness 和 Tool 的执行链路
- Permission、Sandbox 和 Approval
- Context、Memory、KV Cache 和 State
- Planning、Subagent 和 Multi-Agent
- Trace、Badcase、Eval 和产品评估

默认五题完成前不提示评分点。总分 20 分，从 `L0 初识` 到 `L5 Harness Owner`。答对结论但解释不清，不会按完全掌握计分。已有明确学习目标时，可以跳过初诊，未诊断的分数保持未知。

### 3. 生成自适应课程

课程会优先补薄弱机制，压缩已经掌握的内容，但不会跳过安全、trace/eval，以及模型与 Harness 的边界。

除初诊外，每个教学单元默认沿以下主线展开，可按目标调整顺序和篇幅：

```text
机制
→ 最小技术结构
→ 当前常用选型
→ Codex 怎么做
→ Codex 为什么这样选
→ 优缺点
→ PM 怎么和工程师沟通
→ 一道检测题
```

每章结束会生成一份适合移动端阅读的概念速查手册。

---

## 课程范围

课程包含 12 个模块：

1. LLM 基本机制：token、context window、attention、layer/head、采样、system prompt、tool call
2. API 与推理：messages、streaming、function calling、推理模型、规划和自检
3. Agent Loop 与 Harness：五层职责、Observe、Plan、Act、Evaluate、ToolRouter、ToolRegistry
4. Context、Memory 与 State：压缩、引用、防污染、KV cache、持久 session、恢复和渐进披露
5. 权限与安全：permission、sandbox、approval、HITL、prompt injection、数据外泄
6. MCP、Skills、Subagent 与 Multi-Agent
7. Workflow、checkpoint、trace、span、事件流、完成契约、结果未知和交接
8. Eval 与实验：golden set、badcase、独立评估、运行验收、A/B、偏差和置信度
9. 训练协作：SFT、RLHF、RLAIF、偏好数据、反馈闭环和模型升级后的流程复查
10. Agent 产品形态与 UX：CLI、IDE、Desktop、Cloud、Chat、Workflow、Canvas，exec/SDK/app-server 的集成取舍
11. 产品选型：Codex、Claude Code、Cursor、Copilot、OpenCode、Manus、Claude Cowork、DeepSeek 等
12. Capstone：拆解一个真实项目的 Harness、PRD、工程沟通清单和 eval 方案

---

## 安装方式

在支持 `SKILL.md` / Agent Skills 结构的 Agent 里直接说：

```text
帮我安装这个 skill：https://github.com/Stormycry-cryp/HarnessExplore/tree/main/harness-explore
```

Codex 手动安装：

```bash
git clone https://github.com/Stormycry-cryp/HarnessExplore.git
mkdir -p ~/.codex/skills
cp -R HarnessExplore/harness-explore ~/.codex/skills/harness-explore
```

其他支持 Agent Skills 的工具，把 `harness-explore` 放到对应的 skills 目录即可。读取 Skill 与执行脚本的能力取决于具体工具；本项目使用本地缓存，安装到 Agent 不等于上传到托管 Agents API。

bootstrap 需要 `bash` 和 `git`；联网获取 manual 使用 `curl`，CLI 不可用且未加 `--skip-cli` 时需要 `npm`。执行准备脚本只下载和验证资料，不调用模型或产生 API 推理费用。

---

## 怎么用

安装后直接说：

```text
用 Harness-Explore 测试我的 Agent / Harness 基础，并开始学习。
```

也可以恢复上一次课程：

```text
继续我的 Harness-Explore 课程。
```

也可以直接指定目标：

```text
跳过初诊，用 Harness-Explore 教我怎么判断长任务真的完成了。
用 Harness-Explore 审阅我的 Agent trace，找出恢复和验收缺口。
```

课程状态默认保存在：

```text
${CODEX_HOME:-$HOME/.codex}/harness-explore/progress.md
```

只保存评分、掌握度、误区、完成物和下一步，不保存完整聊天记录。

设置 `HARNESS_EXPLORE_CACHE` 可选择独立缓存位置。新增证据字段按需补充，旧进度不会因此重置。完整课程的完成条件是核心模块达到可沟通，并交付一次真实项目 Harness 拆解；模拟练习与真实项目运行验收分别记录。

---

## 仓库结构

```text
harness-explore/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── bootstrap_codex.sh
└── references/
    ├── curriculum.md
    ├── official-sources.md
    ├── harness-practice.md
    ├── diagnostic.md
    ├── progress-schema.md
    ├── codex-source-map.md
    └── codex-source-files.txt
```

- `SKILL.md`：教学流程和硬规则
- `diagnostic.md`：五题初诊、评分和能力等级
- `curriculum.md`：课程模块、适应规则和完成物
- `progress-schema.md`：长期学习进度格式
- `codex-source-map.md`：每个主题对应的 Codex 源码入口
- `bootstrap_codex.sh`：隔离 CLI、稀疏源码和官方文档准备
- `official-sources.md`：一手资料日期、相关结论与应用建议
- `harness-practice.md`：边界图、集成选型、完成契约、交接和评估练习

---

## 证据规则

每次使用 Codex 举例时，都要区分四件事：

```text
Codex snapshot: 当前源码 commit
Evidence: 真实文件路径或官方文档
Observed behavior: 源码直接支持的结论
Product inference: 基于实现做出的产品推断
```

找不到实现时必须明确说不知道，不能把产品推断写成源码事实。源码发生变化时，以当次 bootstrap 获取的 commit 为准。

---

## 适合谁

适合：

- 想成为 Agent、Coding Agent 或 Desktop Agent 产品负责人的人
- 需要和模型、平台、客户端或基础设施工程师讨论方案的人
- 术语听过很多，但技术边界还不稳定的人
- 想用真实源码建立长期理解，而不是只看二手总结的人

不适合：

- 只想快速背面试关键词的人
- 只需要一份静态 Agent 行业报告的人
- 不愿意回答任何诊断题或接受纠错的人

---

## 边界

- Codex 是默认源码案例，不代表所有 Agent 都应该照搬 Codex。
- 当前产品选型必须在教学时重新查证，不能把仓库里的课程地图当成永远最新的结论。
- Skill 教你理解和评审工程方案，不替代真实系统的安全审计、性能测试或模型评估。
- 官方网页 manual 不可访问时，bootstrap 会明确提示，并使用相同源码 commit 下的版本化仓库文档。

## 验证更新

```bash
bash -n harness-explore/scripts/bootstrap_codex.sh
python3 -m unittest discover -s tests -v
```

行为测试使用临时 Git 仓库与命令替身，覆盖离线、固定版本、路径缺失、旧 manual 和缓存保护，不联网、不调用付费模型。GitHub Actions 自动运行相同检查；真实联网下载单独验证，不能由 fixture 测试替代。

---

## License

[MIT](./LICENSE)
