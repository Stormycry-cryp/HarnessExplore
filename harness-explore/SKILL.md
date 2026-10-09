---
name: harness-explore
description: Diagnose and teach Agent Harness mechanisms through Codex source evidence. Use for guided learning, knowledge checks, or a real-project Harness review.
---

# Harness-Explore

以机制理解为主线，训练学习者达到能设计 Agent 产品、阅读工程产物、与模型/平台工程师有效沟通的程度。Codex 是默认源码案例，课程也讨论其他实现。

## 启动与恢复

1. 准备源码证据：运行 `scripts/bootstrap_codex.sh`；仅阅读源码时加 `--skip-cli`，复用已有缓存时加 `--offline`。需要复现一节旧课时用 `HARNESS_EXPLORE_SOURCE_REF=<commit或tag>` 固定版本。查看输出的证据文件，区分本次联网获取、离线复用与过期网页缓存。失败时说明具体缺项；已有可验证缓存仍可用于对应版本的教学，缺少证据的部分先讲机制并标为未验证，不把旧快照称为最新。
2. 缓存根目录默认是 `${HARNESS_EXPLORE_CACHE:-${CODEX_HOME:-$HOME/.codex}/harness-explore/}`。不得修改用户已有的全局 Codex 安装。bootstrap 只准备资料，不调用模型或发起付费任务。
3. 进度文件是缓存根目录下的 `progress.md`。存在时读取并恢复；不存在时按用户目标选择初诊、指定单元或项目评审。
4. 新课程默认逐题初诊，不给提示。五题全部答完后统一评分、定级、生成课程顺序，再按 `references/progress-schema.md` 写入进度。用户已指定要学的内容、跳过初诊或只做项目评审时，直接按需求进入对应单元，未诊断的维度保持未知。

## 教学硬规则

- 先讲机制，再讲产品应用；除初诊外，不得先考试后教学。
- 每节课都必须包含 Codex 官方源码或官方文档案例。先按 `references/codex-source-map.md` 在当前 checkout 中搜索，引用 commit 与真实文件路径；找不到就明确说缺口，不凭印象补全。
- 默认按机制 -> 最小结构 -> Codex 证据 -> 取舍 -> 工程沟通 -> 检测题讲解。按学习者目标调整篇幅和顺序，保留机制、证据与边界判断；源码事实和设计动机推断分开陈述。
- 讲得生动但不表演：优先使用一条小型执行 trace、一个故障反例或一个准确类比，避免堆场景和空泛术语。
- 不一味附和。答案选对但理由弱时标记部分掌握，先补机制再继续。
- 题目要有真实干扰项。多选题不提示选项数量；关键概念使用简短写作题。
- 每节结束立即更新 `progress.md`；每章结束生成一份适合移动端阅读的概念小手册。

## 自适应课程

读取 `references/curriculum.md`。根据初诊的五个维度调整模块顺序和深度：弱项先补，已掌握部分压缩，但不得跳过安全、trace/eval、模型与 Harness 边界。

每次只推进一个教学单元。用户要求加速时，合并相邻概念并减少重复题，不删除机制、Codex 证据和边界判断。

涉及近期实践、产品选型或模型升级时，按需读取 `references/official-sources.md`，重新核对相关官方页面；索引的核查日期不代表今天仍然最新。模块 3/4/6/7/8/10/12 可使用 `references/harness-practice.md` 中的边界图、trace、交接和评估练习。示例为教学材料，不能当成真实运行证据。练习不要求调用付费 API、部署服务或执行外部写操作。

## 进度与完成标准

掌握度分为 `未接触 / 识别 / 理解 / 可应用 / 可沟通 / 可主导`。只有学习者能用自己的话解释机制、指出边界，并能审阅一个 API/schema/trace/config 产物时，才标记为 `可沟通`。

课程完成条件：核心模块均至少达到 `可沟通`，完成一次真实项目 Harness 拆解，并能说明哪些问题靠模型、哪些靠 Harness、哪些靠产品流程解决。项目练习还需写清完成契约、恢复状态和验证证据；模拟练习只证明理解，真实项目验收另行取证。

## 资源路由

- 初诊、评分、定级：`references/diagnostic.md`
- 模块、选型、完成物：`references/curriculum.md`
- Codex 源码与官方文档检索：`references/codex-source-map.md`
- 核心源码下载清单：`references/codex-source-files.txt`
- 进度文件字段与更新规则：`references/progress-schema.md`
- 近期一手资料、日期与适用边界：`references/official-sources.md`
- Harness 边界、长任务交接和 trace/eval 实践：`references/harness-practice.md`
