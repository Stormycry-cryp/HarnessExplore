# Codex 源码与文档检索地图

## 证据顺序

1. 当前缓存中由 `codex-source-files.txt` 定义的 `openai/codex` 官方核心源码快照。
2. 本次 bootstrap 获取的官方 Codex manual。
3. OpenAI 官方开发者文档。
4. 高质量社区实践，只用于补充，不替代官方事实。

先运行 `git -C <source_dir> rev-parse HEAD`。源码会变化，不依赖固定行号；使用 `rg` 找符号，再阅读上下文。

## 常用入口

- Agent loop：`codex-rs/core/src/session/`，搜索 `run_turn`、sampling、tool output。
- Tool contract：`codex-rs/tools/src/tool_executor.rs`。
- Tool routing/registry：`codex-rs/core/src/tools/router.rs`、`registry.rs`、`spec_plan.rs`、`parallel.rs`。
- Tool handlers：已下载的 `handlers/shell.rs`、`mcp.rs`、`plan.rs`、`request_permissions.rs`、`multi_agents.rs`。
- Context history/compaction：`codex-rs/core/src/context_manager/`、`compact*.rs`。
- Step/world state：`codex-rs/core/src/session/step_context.rs`、`context/world_state/`。
- Permission/sandbox/approval：`codex-rs/core/src/config/permissions.rs`、`sandboxing/`、`guardian/`、shell/exec handlers。
- Planning：搜索 `update_plan`、collaboration mode、plan templates；区分 checklist tool 与 Plan Mode。
- MCP：`codex-rs/core/src/mcp_tool_call.rs`、`core/src/tools/handlers/mcp.rs`、`codex-rs/docs/codex_mcp_interface.md`。
- Subagent/Multi-agent：`core/src/agent/`、`tools/handlers/multi_agents*`。
- Memory：`codex-rs/memories/`、memory API/config/citation。
- Trace/telemetry：搜索 `ToolDispatchTrace`、OTel、rollout、analytics。

## 每节课的 Codex 证据格式

```text
Codex snapshot: <commit>
Evidence: <真实文件路径或官方文档标题>
Observed behavior: <源码直接支持的结论>
Product inference: <为什么这样设计，明确标注为推断>
Tradeoff: <收益与代价>
```

不要把产品推断写成源码事实。找不到对应实现时直接说“当前官方源码/文档未建立该结论”。
