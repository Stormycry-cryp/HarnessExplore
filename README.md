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

它不是术语词典，也不是把 Agent 产品案例堆在一起的行业报告。它先从机制讲起，再用当前 Codex 官方源码解释真实 Harness 怎么实现，最后检查你能不能把原理、工程边界和产品决策连起来。

你不需要一次写很多。Skill 会逐题和你交流，记录理解状态，并根据回答动态调整课程顺序。

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

1. 验证本机 Codex CLI。
2. 全局 CLI 不可用时，在独立缓存中安装最新官方 `@openai/codex`。
3. 从 `openai/codex` 稀疏拉取课程需要的核心源码与版本化官方文档。
4. 记录真实 source commit，供每节课引用。

它不会修改用户已有的全局 Codex 安装，也不会下载整个源码仓库。核心源码清单写在 [`codex-source-files.txt`](./harness-explore/references/codex-source-files.txt)。

### 2. 做五题初始诊断

Skill 会逐题提出 5 道开放简答题，检查：

- Agent、Harness 和 Tool 的执行链路
- Permission、Sandbox 和 Approval
- Context、Memory、KV Cache 和 State
- Planning、Subagent 和 Multi-Agent
- Trace、Badcase、Eval 和产品评估

五题完成前不提示评分点。总分 20 分，从 `L0 初识` 到 `L5 Harness Owner`。答对结论但解释不清，不会按完全掌握计分。

### 3. 生成自适应课程

课程会优先补薄弱机制，压缩已经掌握的内容，但不会跳过安全、trace/eval，以及模型与 Harness 的边界。

除初诊外，每个教学单元都遵循同一顺序：

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
3. Agent Loop 与 Harness：Observe、Plan、Act、Evaluate、ToolRouter、ToolRegistry
4. Context、Memory 与 State：压缩、引用、防污染、KV cache、恢复和持久化
5. 权限与安全：permission、sandbox、approval、HITL、prompt injection、数据外泄
6. MCP、Skills、Subagent 与 Multi-Agent
7. Workflow、checkpoint、trace、span、事件流和成本
8. Eval 与实验：golden set、badcase、A/B、灰度、偏差和置信度
9. 训练协作：SFT、RLHF、RLAIF、偏好数据和训练反馈闭环
10. Agent 产品形态与 UX：CLI、IDE、Desktop、Cloud、Chat、Workflow、Canvas
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

其他支持 Agent Skills 的工具，把 `harness-explore` 放到对应的 skills 目录即可。运行 bootstrap 需要 `bash`、`git`、`curl` 和 `npm`。

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

课程状态默认保存在：

```text
${CODEX_HOME:-$HOME/.codex}/harness-explore/progress.md
```

只保存评分、掌握度、误区、完成物和下一步，不保存完整聊天记录。

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

---

## License

[MIT](./LICENSE)
