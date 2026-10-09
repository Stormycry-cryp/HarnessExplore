# Harness 一手资料索引

本轮核查日期：2026-10-09。按相关性选择资料，未声称覆盖所有最新研究。发布日期取自原页面；动态文档没有公开日期时保留未知。使用时重新打开与本课有关的页面，记录访问日期和版本，不把产品公告当成通用机制或生产验收。

## 近期更新

| 来源与发布日期 | 原文支持的要点 | 本课程的应用建议 | 模块 |
|---|---|---|---|
| [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)，2026-09-11 | 缩短 Skill 描述、按需披露内容，模型升级后复查已有指令与流程 | 用本 Skill 练习检查发现条件、资源路由、必要约束；移除流程前做对照验证 | 4、6、9 |
| [OpenAI: Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/)，2026-09-10 | 公测服务提供托管 Codex Harness；运行层与 sandbox 可分开 | 作为托管方案对照，比较运行责任、数据边界、恢复能力；课程无需开通或调用该 API | 3、5、7、11 |
| [OpenAI: Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform)，2026-08-19 | `exec`、SDK、app-server 提供不同集成方式；应用负责领域界面、上下文和业务工具 | 阅读本次源码中的 app-server 与 SDK，判断业务规则应放在哪一层 | 3、7、10 |
| [OpenAI Cookbook: Agent Improvement Loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)，2026-05-12 | 从真实 trace 和反馈构造 eval，再提出 Harness 更新 | 将故障样本变成回归案例，比较改动前后结果、成本与延迟 | 7、8、12 |
| [Anthropic: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)，2026-04-08 | 分开 session、Harness 与 sandbox；持久事件记录不同于模型当前上下文 | 画出日志、运行状态、文件产物的位置，讨论各自丢失后的恢复方式 | 4、5、7 |
| [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)，2026-03-24 | 以可测试契约和独立 evaluator 检查运行中的应用；不同模型需要的组件会变化 | 用真实操作核查完成情况；比较增加 evaluator 或简化流程后的收益和代价 | 6、8、9、12 |

应用建议由本课程作者提出。它们是对资料的教学转化，不能当成对应厂商的标准要求。文中实验的模型、任务、预算和基础设施有特定条件，数字与架构不直接外推。

## 基础阅读与动态文档

| 来源 | 日期与证据类型 | 用途与边界 |
|---|---|---|
| [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) | 2026-02-11，团队实践 | 认识环境可读性、仓库知识与验证反馈。文章讨论的工程实践范围比运行时 Agent Loop 更宽。 |
| [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 2025-11-26，团队实验 | 学习初始化、增量任务与跨会话交接；和 2026-03-24 的后续文章一起读，避免把早期补偿措施固定下来。 |
| [OpenAI: Skills](https://developers.openai.com/api/docs/guides/tools-skills) | 日期未知，动态 API 文档；本轮访问 2026-10-09 | 目录结构、发现机制和执行环境差异。本仓库是本地教学 Skill，安装到 Agent 不等于上传到托管 API。 |
| [OpenAI: Agents API architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) | 日期未知，动态 API 文档；本轮访问 2026-10-09 | 托管运行层、事件、工具与执行环境边界。具体字段、权限和可用性以调用时文档为准。 |
| [openai/codex](https://github.com/openai/codex) | 活跃源码；使用 bootstrap 输出的实际 commit | Codex 实现事实。CLI 版本、源码 commit 和网页文档是三个不同证据，不能假定来自同一版本。 |

## 阅读时写什么

记录 `URL / 发布日期或未知 / 本次访问日期 / 源码commit或文档版本 / 直接支持的结论 / 推断 / 未确认事项`。只更新当前课程需要的证据；离线时标明复用日期。页面不可达时保留缺口，不补写未经确认的产品功能。

产品比较按具体任务进行：谁运行 Harness、谁保存状态、工具和数据放在哪里、谁批准业务写入、如何打断和恢复、用什么证明完成。能力名称相似不能证明实现、权限和效果相同。
