# 学习进度规范

进度文件：`${HARNESS_EXPLORE_CACHE:-${CODEX_HOME:-$HOME/.codex}/harness-explore}/progress.md`。

```markdown
# Harness-Explore Progress

- Started: YYYY-MM-DD
- Updated: YYYY-MM-DD
- Codex source commit: <sha>
- Diagnostic score: <0-20>
- Level: <L0-L5>
- Current module: <name>
- Current lesson: <name>

## Dimension Scores
| Dimension | Score | Evidence | Priority |
|---|---:|---|---|
| Agent/Harness/Tool | 0-4 | ... | high/medium/low |
| Permission/Sandbox/Approval | 0-4 | ... | ... |
| Context/Memory/State | 0-4 | ... | ... |
| Planning/Subagent | 0-4 | ... | ... |
| Trace/Eval/Product | 0-4 | ... | ... |

## Module Progress
| Module | Mastery | Last check | Next action |
|---|---|---|---|
| ... | 未接触/识别/理解/可应用/可沟通/可主导 | ... | ... |

## Misconceptions
- <误区 -> 正确机制 -> 复测时间>

## Completed Artifacts
- <手册、schema、trace review、项目拆解等>

## Next Session
- <只保留一个最优先动作>
```

每次课程结束只更新变化字段。不要保存完整聊天或大段日志；保留结论、证据、误区和下一步。重新诊断时保留旧分数作为历史，不覆盖学习轨迹。
