---
name: self-improving-agent
description: Self Improving Agent - 自改进 Agent 系统，实现反思、学习、优化机制，持续提升 Agent 性能
metadata:
  version: 1.0.0
  author: openclaw
---

# Self Improving Agent - 自改进 Agent 系统

## 概述

实现反思、学习、优化三大机制，让 Agent 能够从经验中学习，持续提升性能和工作效率。

## 核心功能

### 1. 反思机制 (Reflection Engine)

分析每次重要对话和决策，提取经验教训：

- **上下文记录** - 记录决策背景
- **行动分析** - 分析采取的行动
- **结果评估** - 评估行动结果
- **教训提取** - 总结可复用的教训
- **改进建议** - 生成具体改进措施

### 2. 学习机制 (Learning Engine)

系统化记录和管理知识：

- **技能追踪** - 记录掌握的技能和熟练度
- **错误管理** - 记录错误和避免方法
- **最佳实践** - 积累有效的处理方式
- **偏好学习** - 学习用户偏好和习惯

### 3. 优化机制 (Optimization Engine)

持续改进工作方式：

- **优化建议** - 识别改进机会
- **实施追踪** - 跟踪优化实施情况
- **效果评估** - 评估优化效果
- **持续迭代** - 基于反馈持续改进

## 使用方法

### 命令行工具

```bash
# 查看当前状态
python3 skills/self-improving-agent/scripts/self_improving_agent.py status

# 添加反思记录
python3 skills/self-improving-agent/scripts/self_improving_agent.py reflect

# 记录学习进度
python3 skills/self-improving-agent/scripts/self_improving_agent.py learn

# 添加优化建议
python3 skills/self-improving-agent/scripts/self_improving_agent.py optimize

# 生成改进计划
python3 skills/self-improving-agent/scripts/self_improving_agent.py plan

# 运行演示
python3 skills/self-improving-agent/scripts/self_improving_agent.py demo
```

### Python API

```python
from self_improving_agent import SelfImprovingAgent

# 创建自改进 Agent
agent = SelfImprovingAgent()

# 添加反思
agent.reflect(
    context="处理汇率预测任务",
    action="使用单一数据源",
    outcome="预测准确率不够高",
    lesson="多源数据验证可以提高准确性",
    improvement="集成 market-data-fetch 和 multi-search-engine"
)

# 记录学习
agent.learn(
    skill_name="地缘风险分析",
    proficiency=8,
    notes="能够综合分析地缘风险对汇率的影响"
)

# 建议优化
agent.suggest_improvement(
    area="报告生成",
    current="手动整理数据",
    suggested="自动化数据整合",
    benefit="节省 50% 时间"
)

# 获取状态报告
report = agent.get_status_report()
print(f"已掌握 {report['learning']['skills_count']} 个技能")

# 生成改进计划
plan = agent.generate_improvement_plan()
print(plan)
```

## 数据结构

### 反思记录

```json
{
  "timestamp": "2026-03-16T09:30:00",
  "context": "处理汇率预测任务",
  "action": "使用单一数据源",
  "outcome": "预测准确率不够高",
  "lesson": "多源数据验证可以提高准确性",
  "improvement": "集成 market-data-fetch 和 multi-search-engine"
}
```

### 学习记录

```json
{
  "skills_learned": [
    {
      "name": "地缘风险分析",
      "proficiency": 8,
      "learned_at": "2026-03-16T09:30:00",
      "notes": "能够综合分析地缘风险对汇率的影响"
    }
  ],
  "mistakes_avoided": [],
  "best_practices": [],
  "user_preferences": {}
}
```

### 优化记录

```json
{
  "timestamp": "2026-03-16T09:30:00",
  "area": "报告生成",
  "current_approach": "手动整理数据",
  "suggested_approach": "自动化数据整合",
  "expected_benefit": "节省 50% 时间",
  "implemented": false
}
```

## 输出示例

### 状态报告

```
============================================================
🧠 Self Improving Agent - 状态报告
============================================================

📊 反思分析:
   总反思数: 5
   最近7天: 2

📚 学习进度:
   技能: 3
   错误记录: 1
   最佳实践: 2

⚡ 优化状态:
   建议: 3
   已实施: 1
   实施率: 33.3%
```

### 改进计划

```markdown
# 自改进计划

生成时间: 2026-03-16 09:51:36

## 1. 反思分析
- 总反思数: 5
- 最近7天: 2
- 主要改进领域:
  - 数据获取自动化: 3次
  - 报告生成优化: 2次

## 2. 学习进度
- 已掌握技能: 3
- 记录的错误: 1
- 最佳实践: 2
- 熟练技能:
  - 地缘风险分析 (熟练度: 8/10)
  - 汇率预测 (熟练度: 7/10)

## 3. 优化状态
- 建议优化: 3
- 已实施: 1
- 待实施: 2
- 实施率: 33.3%

## 4. 建议行动

有待实施的优化建议 (2项):

1. **报告生成**
   - 当前: 手动整理数据到报告
   - 建议: 自动化数据整合和可视化
   - 收益: 节省 50% 报告生成时间

2. **数据获取**
   - 当前: 手动执行多个命令
   - 建议: 创建自动化工作流脚本
   - 收益: 提高效率，减少人为错误
```

## 应用场景

### 1. 技能发展追踪

```python
# 记录新技能学习
agent.learn(
    skill_name="Kalshi API 使用",
    proficiency=6,
    notes="能够获取预测市场数据"
)

# 提升技能熟练度
agent.learn(
    skill_name="Kalshi API 使用",
    proficiency=8,
    notes="熟练处理多种数据类型"
)
```

### 2. 错误预防

```python
# 记录错误和避免方法
agent.learning.record_mistake(
    mistake="忘记验证数据源时效性",
    context="生成汇率报告",
    prevention="每次获取数据时检查时间戳"
)
```

### 3. 最佳实践积累

```python
# 记录有效的工作方式
agent.learning.add_best_practice(
    practice="使用 find-skills 快速定位所需工具",
    category="效率提升",
    context="当不确定使用哪个 skill 时"
)
```

### 4. 持续改进循环

```python
# 每个重要任务后进行反思
agent.reflect(
    context="完成汇率预测报告",
    action="使用了新安装的 multi-search-engine",
    outcome="数据更全面，但耗时增加",
    lesson="需要平衡数据全面性和效率",
    improvement="设置搜索深度参数，根据任务紧急度调整"
)

# 基于反思生成优化建议
agent.suggest_improvement(
    area="数据获取",
    current="每次都进行完整搜索",
    suggested="根据任务类型使用预设搜索模板",
    benefit="减少 30% 数据获取时间"
)
```

## 与其他 Skill 集成

### 与 find-skills 集成

```python
from self_improving_agent import SelfImprovingAgent
from find_skills import SkillFinder

agent = SelfImprovingAgent()

# 记录 skill 使用偏好
agent.learning.record_preference(
    key="preferred_data_source",
    value="yfinance",
    confidence=0.8
)
```

### 与报告生成集成

```python
# 生成自改进报告作为日报的一部分
plan = agent.generate_improvement_plan()

# 保存到文件
with open('improvement_plan.md', 'w') as f:
    f.write(plan)
```

## 文件结构

```
skills/self-improving-agent/
├── SKILL.md                      # 本文件
├── scripts/
│   └── self_improving_agent.py   # 主脚本
└── memory/                       # 数据存储
    ├── reflections.json          # 反思记录
    ├── learnings.json            # 学习记录
    └── optimizations.json        # 优化记录
```

## 数据存储

所有数据存储在 `workspace/memory/` 目录：

- `reflections.json` - 反思记录
- `learnings.json` - 学习记录
- `optimizations.json` - 优化记录

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 反思引擎
- 学习引擎
- 优化引擎
- 改进计划生成
