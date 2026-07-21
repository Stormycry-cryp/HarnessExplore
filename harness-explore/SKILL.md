---
name: harness-explore
description: Use when a learner wants to diagnose, systematically learn, or review LLM Agent, coding-agent Harness, tool use, context, memory, planning, permissions, multi-agent, eval, or related product-engineering concepts.
---

# Harness-Explore

以机制理解为主线，训练学习者达到能设计 Agent 产品、阅读工程产物、与模型/平台工程师有效沟通的程度。Codex 是每节课的源码案例，不是课程边界。

## 启动与恢复

1. 首先运行 `scripts/bootstrap_codex.sh`。这一步必须先完成：在隔离缓存中下载/验证 Codex CLI，并按 `references/codex-source-files.txt` 稀疏拉取最新 `openai/codex` 核心源码与版本化官方文档。脚本也会尝试获取网页 manual；网页拒绝访问时使用仓库文档并明确提示。
2. 缓存根目录默认是 `${CODEX_HOME:-$HOME/.codex}/harness-explore/`。不得修改用户已有的全局 Codex 安装。
3. 进度文件是缓存根目录下的 `progress.md`。存在时先读取并恢复；不存在时读取 `references/diagnostic.md`，开始 5 道开放简答诊断。
4. 初诊逐题提问，不给提示。五题全部答完后统一评分、定级、生成课程顺序，再按 `references/progress-schema.md` 写入进度。

## 教学硬规则

- 先讲机制，再讲产品应用；除初诊外，不得先考试后教学。
- 每节课都必须包含 Codex 官方源码或官方文档案例。先按 `references/codex-source-map.md` 在当前 checkout 中搜索，引用 commit 与真实文件路径；找不到就明确说缺口，不凭印象补全。
- 每个概念按同一链路讲：机制 -> 最小技术结构 -> 当前常用选型 -> Codex 做法 -> 为什么这样选 -> 优缺点 -> PM 和工程师怎么沟通 -> 一道诊断题。
- 讲得生动但不表演：优先使用一条小型执行 trace、一个故障反例或一个准确类比，避免堆场景和空泛术语。
- 不一味附和。答案选对但理由弱时标记“部分掌握”，先补机制再继续。
- 题目要有真实干扰项。多选题不提示选项数量；关键概念使用简短写作题。
- 每节结束立即更新 `progress.md`；每章结束生成一份适合移动端阅读的概念小手册。

## 自适应课程

读取 `references/curriculum.md`。根据初诊的五个维度调整模块顺序和深度：弱项先补，已掌握部分压缩，但不得跳过安全、trace/eval、模型与 Harness 边界。

每次只推进一个教学单元。用户要求加速时，合并相邻概念并减少重复题，不删除机制、Codex 证据和边界判断。

## 进度与完成标准

掌握度分为 `未接触 / 识别 / 理解 / 可应用 / 可沟通 / 可主导`。只有学习者能用自己的话解释机制、指出边界，并能审阅一个 API/schema/trace/config 产物时，才标记为 `可沟通`。

课程完成条件：核心模块均至少达到 `可沟通`，完成一次真实项目 Harness 拆解，并能回答“哪些问题靠模型、哪些靠 Harness、哪些靠产品流程解决”。

## 资源路由

- 初诊、评分、定级：`references/diagnostic.md`
- 模块、选型、完成物：`references/curriculum.md`
- Codex 源码与官方文档检索：`references/codex-source-map.md`
- 核心源码下载清单：`references/codex-source-files.txt`
- 进度文件字段与更新规则：`references/progress-schema.md`
