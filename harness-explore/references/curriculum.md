# 自适应课程地图

## 模块

1. LLM 基本机制：token、context window、attention、layer/head、采样、system prompt、tool call。
2. API 与推理：OpenAI-compatible messages/streaming/tools，推理模型、规划-执行、反思与自检。
3. Agent Loop 与 Harness：Observe/Plan/Act/Evaluate，ToolRouter/Registry，失败回填与动态重规划。
4. Context、Memory、State：选择、压缩、引用、防污染，KV cache 与 prompt caching，恢复与持久化。
5. 权限与安全：permission、sandbox、approval、HITL、prompt injection、数据外泄与最小权限。
6. MCP、Skills、Subagents、Multi-Agent：能力接入、渐进披露、隔离上下文、通信、汇总和冲突处理。
7. Workflow 与可观测性：状态机、重试、checkpoint、trace/span、事件流、成本与长任务恢复。
8. Eval 与实验：golden set、badcase、回归、人工评分、任务完成率、A/B、灰度、样本偏差与置信度。
9. 训练协作：SFT、RLHF、RLAIF、偏好数据、能力边界、训练反馈闭环，模型与 Harness 的分工。
10. 产品形态与 UX：CLI/IDE/Desktop/Cloud，Chat/Workflow/Canvas，状态、等待、失败和权限确认体验。
11. 产品选型：Claude Code、Codex、Cursor、GitHub Copilot、OpenCode、Manus、OpenClaw、Hermes、Claude Cowork/Projects/Artifacts、DeepSeek 生态。
12. Capstone：用真实项目做 Harness 拆解、PRD、工程沟通清单和 eval 方案。

## 当前常用选型讲法

每个模块都要说明“有哪些做法、各自优缺点、Codex 选了什么、为什么”。技术选型必须用本次运行抓取的官方资料或当前活跃源码校验，不把旧快照说成最新。

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
