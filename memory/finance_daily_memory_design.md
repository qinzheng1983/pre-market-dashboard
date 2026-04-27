# 财经日报信息记忆与遗忘机制设计

## 系统架构

### 1. 记忆存储结构

```json
{
  "metadata": {
    "last_updated": "2026-03-30",
    "total_entries": 150,
    "version": "1.0"
  },
  "information_index": {
    "monetary_policy": {
      "lpr": {
        "current_value": "3.00%|3.50%",
        "last_change_date": "2025-06-20",
        "frequency": "monthly",
        "entries": [
          {
            "date": "2026-03-20",
            "value": "3.00%|3.50%",
            "weight": 1.0,
            "hash": "lpr_20260320_3.00_3.50",
            "is_change": false
          }
        ]
      }
    },
    "new_energy": {
      "lithium_carbonate_price": {
        "current_value": 145000,
        "unit": "元/吨",
        "entries": []
      }
    },
    "metals": {},
    "market_data": {}
  },
  "daily_snapshots": {
    "2026-03-30": {
      "generated_at": "2026-03-30T10:00:00+08:00",
      "key_facts": [
        {
          "category": "monetary_policy",
          "subcategory": "lpr",
          "content": "LPR连续10个月维持不变",
          "hash": "fact_lpr_stable_10m",
          "significance": "high",
          "first_seen": "2026-03-30",
          "last_seen": "2026-03-30",
          "presentation_count": 1,
          "weight": 1.0
        }
      ]
    }
  }
}
```

### 2. 权重计算机制

```python
# 权重衰减公式
def calculate_weight(entry_date, current_date, half_life_days=30):
    """
    基于指数衰减的权重计算
    - half_life_days: 半衰期，默认30天
    - 超过365天的信息权重趋近于0
    """
    days_diff = (current_date - entry_date).days
    if days_diff > 365:
        return 0.0
    weight = 0.5 ** (days_diff / half_life_days)
    return max(weight, 0.01)  # 最小权重0.01

# 重要性调整
def adjust_weight_by_significance(base_weight, significance):
    """
    根据重要性调整权重
    """
    multipliers = {
        "critical": 2.0,   # 重大政策变化、地缘冲突
        "high": 1.5,       # 重要数据发布
        "medium": 1.0,     # 常规数据
        "low": 0.7         # 次要信息
    }
    return base_weight * multipliers.get(significance, 1.0)
```

### 3. 信息去重与呈现策略

```python
class DailyReportMemory:
    def __init__(self, memory_file="finance_daily_memory.json"):
        self.memory_file = memory_file
        self.data = self.load_memory()
    
    def is_new_information(self, content_hash, category):
        """检查信息是否为新信息"""
        for date, snapshot in self.data["daily_snapshots"].items():
            for fact in snapshot["key_facts"]:
                if fact["hash"] == content_hash:
                    return False, fact
        return True, None
    
    def decide_presentation(self, fact_hash, fact_content, category, significance="medium"):
        """
        决定信息呈现方式
        返回: {
            "action": "present" | "compare" | "skip",
            "reason": str,
            "comparison_data": {}  # 如果是compare
        }
        """
        is_new, existing_fact = self.is_new_information(fact_hash, category)
        
        if is_new:
            return {
                "action": "present",
                "reason": "新信息，首次出现",
                "comparison_data": None
            }
        
        # 计算现有信息的权重
        weight = calculate_weight(
            datetime.strptime(existing_fact["first_seen"], "%Y-%m-%d"),
            datetime.now(),
            half_life_days=30
        )
        weight = adjust_weight_by_significance(weight, existing_fact["significance"])
        
        # 根据权重决定呈现方式
        if weight < 0.1:
            return {
                "action": "skip",
                "reason": f"信息权重过低({weight:.2f})，用户已充分了解",
                "comparison_data": None
            }
        elif existing_fact["presentation_count"] >= 3:
            return {
                "action": "compare",
                "reason": "信息已多次呈现，进行趋势对比",
                "comparison_data": self.get_comparison_data(category, fact_hash)
            }
        else:
            return {
                "action": "present",
                "reason": f"信息已呈现{existing_fact['presentation_count']}次，继续展示",
                "comparison_data": None
            }
    
    def get_comparison_data(self, category, fact_hash):
        """获取历史对比数据"""
        # 获取该类别的历史数据用于对比
        history = []
        for date, snapshot in sorted(self.data["daily_snapshots"].items()):
            for fact in snapshot["key_facts"]:
                if fact["category"] == category:
                    history.append({
                        "date": date,
                        "content": fact["content"],
                        "weight": fact["weight"]
                    })
        return history[-30:]  # 最近30天
```

### 4. 信息分类与重要性分级

| 类别 | 子类 | 重要性 | 半衰期 | 呈现策略 |
|------|------|--------|--------|----------|
| **货币政策** | LPR调整 | critical | 90天 | 必须呈现，重大变化突出显示 |
| | LPR维持不变 | medium | 30天 | 3次后转为对比 |
| | 央行公开市场操作 | low | 7天 | 1次后跳过 |
| **汇率** | USD/CNY中间价 | high | 7天 | 连续3天后对比 |
| **新能源** | 碳酸锂价格 | high | 7天 | 波动>5%时呈现 |
| | 动力电池装机 | medium | 30天 | 月度对比 |
| | 钠电池技术突破 | critical | 180天 | 长期跟踪 |
| **有色金属** | 铜铝价格 | medium | 3天 | 日度对比 |
| | 镍价地缘影响 | high | 7天 | 持续跟踪 |
| **地缘风险** | 冲突升级 | critical | 90天 | 持续呈现直至降级 |
| | 制裁措施 | high | 30天 | 跟踪影响 |

### 5. 遗忘机制实现

```python
def cleanup_expired_memory(self, current_date):
    """
    清理过期记忆
    - 删除超过365天的快照
    - 权重低于0.01的信息标记为归档
    """
    expired_dates = []
    for date_str in self.data["daily_snapshots"].keys():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if (current_date - date).days > 365:
            expired_dates.append(date_str)
    
    for date in expired_dates:
        del self.data["daily_snapshots"][date]
    
    # 归档低权重信息
    for category, subcategories in self.data["information_index"].items():
        for subcategory, data in subcategories.items():
            if "entries" in data:
                for entry in data["entries"]:
                    entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
                    entry["weight"] = calculate_weight(entry_date, current_date)
    
    self.save_memory()
```

### 6. 报告生成流程整合

```python
def generate_daily_report_with_memory(current_date):
    """带记忆的日报生成流程"""
    
    # 1. 初始化记忆系统
    memory = DailyReportMemory()
    
    # 2. 收集当日原始数据
    raw_data = collect_raw_data(current_date)
    
    # 3. 信息处理与去重
    processed_facts = []
    for item in raw_data:
        fact_hash = generate_hash(item["content"])
        decision = memory.decide_presentation(
            fact_hash, 
            item["content"],
            item["category"],
            item.get("significance", "medium")
        )
        
        if decision["action"] == "present":
            processed_facts.append({
                **item,
                "presentation": "full"
            })
        elif decision["action"] == "compare":
            processed_facts.append({
                **item,
                "presentation": "comparison",
                "comparison_data": decision["comparison_data"]
            })
        # action == "skip" 则跳过
    
    # 4. 生成报告
    report = format_report(processed_facts, current_date)
    
    # 5. 更新记忆
    memory.update_snapshot(current_date, processed_facts)
    memory.cleanup_expired_memory(current_date)
    
    return report
```

### 7. 存储位置

- **记忆文件**: `memory/finance_daily_memory.json`
- **历史快照**: `memory/finance_daily_snapshots/` (按年分子目录)
- **配置参数**: `skills/finance-daily-report/config/memory_config.json`

### 8. 关键规则

1. **首次呈现**：新信息必须完整展示，标注"首次"
2. **重复呈现**：第2-3次重复时简化展示
3. **对比呈现**：超过3次后只展示变化趋势和对比
4. **自动遗忘**：权重<0.01或超过365天的信息自动归档
5. **强制保留**：critical级别的地缘风险信息保留180天

---

## 实施计划

1. **Phase 1** (立即): 设计JSON Schema，建立基础存储结构
2. **Phase 2** (本周): 实现权重计算和去重逻辑
3. **Phase 3** (下周): 整合到报告生成流程，测试运行
4. **Phase 4** (持续): 根据反馈调整参数（半衰期、权重阈值）
