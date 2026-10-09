# 学习进度规范

进度文件：`${HARNESS_EXPLORE_CACHE:-${CODEX_HOME:-$HOME/.codex}/harness-explore}/progress.md`。

```markdown
# Harness-Explore Progress

- Started: YYYY-MM-DD
- Updated: YYYY-MM-DD
- Codex source commit: <sha/unknown>
- Evidence mode: <online/offline/unknown>
- Source acquired: <UTC时间/unknown>
- Diagnostic score: <0-20/unknown>
- Level: <L0-L5/unknown>
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

## Evidence Register
| Topic | URL or source path | Published/version | Checked | Status |
|---|---|---|---|---|
| <当前课程主题> | <官方URL或源码文件> | <发布日期或commit，未知则unknown> | <本次访问或核验时间> | verified/cached/simulated/unknown |

## Project Review
- Completion contract: <完成要求与适用验证>
- Verified: <已完成动作及证据路径>
- Unknown or blocked: <未知结果、缺失证据或准确阻塞>
- Next verification: <一个最有价值的下一步>

## Next Session
- <只保留一个最优先动作>
```

每次课程结束只更新变化字段。不要保存完整聊天或大段日志；保留结论、证据、误区和下一步。重新诊断时保留旧分数作为历史，不覆盖学习轨迹。

新字段按需补充，旧进度可直接恢复；没有记录的字段设为 unknown，不重置分数、不要求重做初诊。用户跳过初诊时分数和等级保持 unknown。Evidence Register 只记本课使用的来源；项目评审才填写 Project Review。虚构练习标记 simulated，不进入真实项目已验证列表。
