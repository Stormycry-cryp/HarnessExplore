# Codex 源码与文档检索地图

## 先确认版本

读取 bootstrap 输出的 `evidence_path`，核对 `source_commit`、`source_state`、`source_acquired_at_utc`、`manual_status`。再运行 `git -C <source_dir> rev-parse HEAD`，引用实际 SHA。CLI 版本与源码 commit 分别记录，不能假定两者对应。

以下入口在 2026-10-09 的官方 tree `2351d9e1b608e6f9d9a3699b71d7eb39ee41cfa4` 中核对存在。它们是检索入口，存在路径不能证明行为。源码持续变化，以选定 commit 中读到的实现为准，不固定行号；先 `rg` 找符号，再阅读调用上下文。

## 已纳入稀疏清单的入口

路径相对于 `<source_dir>`；首次只读当前主题所需文件。

| 主题 | 文件入口 | 检索方向 |
|---|---|---|
| Agent loop | `codex-rs/core/src/session/turn.rs`、`session.rs` | `run_turn`、sampling、tool output、结束条件 |
| Tool contract | `codex-rs/tools/src/tool_executor.rs` | 调用与执行结果的边界 |
| Tool routing/registry | `codex-rs/core/src/tools/router.rs`、`registry.rs`、`parallel.rs`、`spec_plan.rs` | handler 选择、schema、并行执行 |
| Shell 执行 | `codex-rs/core/src/tools/handlers/shell_spec.rs`、`unified_exec/exec_command.rs` | 工具声明与执行处理分别查证 |
| Context/compaction | `codex-rs/core/src/context_manager/history.rs`、`mod.rs`、`normalize.rs`、`updates.rs`；`codex-rs/core/src/compact.rs`、`compact_remote_v2.rs` | 历史选择、规范化、压缩和回填 |
| Step/world state | `codex-rs/core/src/session/step_context.rs`、`world_state.rs` | 本轮执行状态与上下文 |
| Permission/sandbox/approval | `codex-rs/core/src/config/permissions.rs`、`tools/sandboxing.rs`、`tools/orchestrator.rs`、`tools/handlers/request_permissions.rs` | 权限判定、执行边界与审批流程 |
| Planning | `codex-rs/core/src/tools/handlers/plan.rs` | `update_plan`；检查列表工具与 Plan Mode 的区别 |
| MCP | `codex-rs/core/src/mcp_tool_call.rs`、`tools/handlers/mcp.rs` | 调用、结果转换与错误回填 |
| Subagents | `codex-rs/core/src/tools/handlers/multi_agents.rs`、`multi_agents_v2.rs` | 实际注册的版本、派发与生命周期 |
| Memory | `codex-rs/memories/README.md`、`read/src/citations.rs`、`write/src/guard.rs`、`runtime.rs`、`storage.rs` | 读取、引用、写入约束、持久化 |
| Resume/state | `codex-rs/core/src/session/rollout_reconstruction.rs` | 历史重建、恢复时的状态边界 |
| Trace/telemetry | `codex-rs/core/src/tools/tool_dispatch_trace.rs`、`codex-rs/otel/README.md` | 调用追踪与可观测配置，记录与验收的区别 |
| 产品集成 | `codex-rs/app-server/README.md`；`sdk/typescript/README.md`、`src/codex.ts`、`src/exec.ts`、`src/thread.ts` | thread/turn、事件、取消、审批与恢复 |
| 仓库指令/基础提示 | `codex-rs/core/src/agents_md.rs`、`codex-rs/protocol/src/prompts/base_instructions/default.md` | 指令发现、组合与角色边界 |

`docs/skills.md`、`sandbox.md`、`config.md` 等仓库文档可能只包含动态官网链接。链接存在不等于当前页面内容已经下载；网页不可达时用相关源码，保留文档缺口。

历史协议文件中的字段不可直接套用到当前 app-server 或业务 API。Codex thread ID、模型 response ID 和业务 request ID 的语义分别核对，恢复 Agent 会话不能证明外部业务动作已执行。

## 证据顺序与缺项

实现问题先查选定 commit 的官方源码；产品接口、支持范围和托管服务查本次访问的官方文档；网页 manual 只有状态为 `downloaded` 才是本次获取，`cached_stale` 需要标明复用。研究背景见 `official-sources.md`，社区材料只作补充。

清单报缺项时，用 `git ls-tree -r --name-only <commit>` 或官方 GitHub tree 查新路径，确认对应实现后再调整 `codex-source-files.txt`。不要只删失败项让脚本通过；记录该主题的新入口或证据缺口。需要清单之外的文件时，先确认当前 tree，再按任务扩展稀疏路径；未下载的目录不能当成已可读证据。

## 每节课的 Codex 证据格式

```text
Codex snapshot: <实际commit>
Evidence: <真实文件路径/官方URL，访问日期和版本>
Observed behavior: <读取源码或文档直接支持的结论>
Product inference: <设计动机或产品推断，明确标记>
Tradeoff: <收益与代价>
Unknown: <本次仍未确认的行为>
```

找不到实现时写明当前官方源码或文档未建立该结论。源码阅读、fixture 测试、CLI 启动与真实产品验收分别说明，不能相互替代。
