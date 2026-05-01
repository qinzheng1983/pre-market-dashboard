# 🌍 优化版地缘风险与汇率分析报告

**生成时间**: 2026-03-16 10:12:04
**数据周期**: 实时数据尝试 + 模拟数据补充
**报告版本**: v3.1 (数据质量优化版)

---

## ⚠️ 数据质量声明

**重要提示**: 本报告的数据来源情况如下：

| 数据类型 | 来源 | 状态 |
|----------|------|------|
| USDCNY | AKShare (中国银行) | ✅ 真实 |
| USDRUB | DEMO DATA (演示数据) | ⚠️ 演示 |
| OIL_BRENT | DEMO DATA (演示数据) | ⚠️ 演示 |
| GOLD | DEMO DATA (演示数据) | ⚠️ 演示 |
| DXY | DEMO DATA (演示数据) | ⚠️ 演示 |
| 新闻数据 | Template | ⚠️ 模板 |

**获取真实数据的方法**:
```bash
# 1. 获取 USD/CNY (推荐)
python3 -c "import akshare as ak; print(ak.fx_spot_quote())"

# 2. 获取新闻
kimi_search --query "Israel Iran conflict latest 2025"

# 3. 获取市场数据
python3 skills/market-data-fetch/scripts/fetch_market_data.py --fx USDCNY=X
```

---

## 📌 执行摘要

- **地缘风险等级**: 🟠 ELEVATED (62/100)
  - *数据质量: TEMPLATE DATA (模板数据)*
- **USD/CNY 当前**: 6.8965
  - *数据来源: AKShare (中国银行) (real)*
- **预测区间**: 6.9655 - 7.2413
- **对冲建议**: 维持65-75%对冲比例，关注谈判进展