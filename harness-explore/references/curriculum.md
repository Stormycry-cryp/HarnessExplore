# 自适应课程地图

## 模块

1. LLM 基本机制：token、context window、attention、layer/head、采样、system prompt、tool call。
2. API 与推理：OpenAI-compatible messages/streaming/tools，推理模型、规划-执行、反思与自检。
3. Agent Loop 与 Harness：模型、运行层、工具、执行环境和产品职责；Observe/Plan/Act/Evaluate，ToolRouter/Registry，失败回填与动态重规划。区分运行时 Harness 与环境、仓库知识、验证反馈等更广的 Harness Engineering。
4. Context、Memory、State：选择、压缩、引用、防污染，KV cache 与 prompt caching，恢复与持久化。区分模型当前上下文、持久 session 日志和磁盘产物，理解渐进披露与恢复记录。
5. 权限与安全：permission、sandbox、approval、HITL、prompt injection、数据外泄与最小权限。
6. MCP、Skills、Subagents、Multi-Agent：能力接入、渐进披露、隔离上下文、通信、汇总和冲突处理；按收益选择单 Agent 或独立 evaluator，比较协调成本与误判。
7. Workflow 与可观测性：状态机、重试、checkpoint、trace/span、事件流、成本与长任务恢复；完成契约、结构化交接、结果未知时查询原请求。
8. Eval 与实验：golden set、badcase、回归、人工评分、任务完成率、A/B、灰度、样本偏差与置信度；从 trace 构造案例，核查代码测试、实际运行、独立评估和人工验收分别证明什么。
9. 训练协作：SFT、RLHF、RLAIF、偏好数据、能力边界、训练反馈闭环，模型与 Harness 的分工；模型升级后用对照实验逐项评估已有补偿流程。
10. 产品形态与 UX：CLI/IDE/Desktop/Cloud，Chat/Workflow/Canvas，状态、等待、失败和权限确认体验；`codex exec`、SDK、app-server 与托管运行层的集成取舍。
11. 产品选型：Claude Code、Codex、Cursor、GitHub Copilot、OpenCode、Manus、OpenClaw、Hermes、Claude Cowork/Projects/Artifacts、DeepSeek 生态。
12. Capstone：用真实项目做 Harness 拆解、PRD、工程沟通清单和 eval 方案，交付完成契约、恢复交接和带证据的评估案例。

## 当前常用选型讲法

结合本课说明可选做法、优缺点、Codex 实现及其适用边界。参考 `official-sources.md` 的相关来源，技术选型用本次访问的官方资料或选定源码 commit 校验，不把旧快照说成最新。设计动机缺少官方解释时标为推断。

## 实践入口

按需使用 `harness-practice.md`：模块 3 用五层边界图，模块 4/7 用交接与结果未知案例，模块 6/8 用 trace 和 evaluator 练习，模块 9 用组件移除对照，模块 10 用集成方式表。先让学习者判断，再读评分依据；不把虚构 trace 填成真实验收记录。

## 自适应规则

- 初诊 0-1 分维度：完整教学 + 两道巩固题。
- 初诊 2 分维度：机制补课 + 一道边界题。
- 初诊 3 分维度：压缩讲解 + 工程产物审阅题。
- 初诊 4 分维度：直接进入取舍、反例和产品评审。
- 安全、trace/eval、模型与 Harness 边界不可跳过。

## 每章完成物

- 移动端速查手册：概念、机制链、常见误区、Codex 证据、PM 话术。
- 掌握度更新与一条未解决问题。
- 至少一个真实工程产物：tool schema、trace、permission config、state model、eval case 或产品流程。
