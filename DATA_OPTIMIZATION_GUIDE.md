# 中东风险报告数据优化指南

## 问题诊断

**原有问题**:
- 报告使用模拟/模板数据，未明确标记
- 用户无法区分真实数据与演示数据
- 数据来源和时间不清晰

**优化后**:
- 明确标记每条数据的来源和状态
- 提供获取真实数据的方法
- 优先尝试真实数据源 (AKShare, Yahoo Finance)

---

## 当前数据获取状态

| 数据类型 | 当前状态 | 真实数据源 |
|----------|----------|------------|
| USD/CNY | ✅ 真实数据 | AKShare (中国银行外汇牌价) |
| USD/RUB | ⚠️ 演示数据 | Yahoo Finance (需网络) |
| 油价 | ⚠️ 演示数据 | Yahoo Finance (需网络) |
| 新闻 | ⚠️ 模板数据 | kimi-search / web_search |
| 黄金价格 | ⚠️ 演示数据 | Yahoo Finance |

---

## 获取完整真实数据的方法

### 1. USD/CNY (已支持 ✅)

**当前**: 使用 AKShare 自动获取中国银行外汇牌价

```bash
# 验证数据
python3 -c "import akshare as ak; df=ak.fx_spot_quote(); print(df[df['货币对']=='USD/CNY'])"
```

### 2. 实时新闻 (需手动获取)

由于网络限制，需要手动使用搜索工具获取:

```bash
# 获取最新中东新闻
kimi_search --query "Israel Iran conflict latest news 2025 2026"
kimi_search --query "Middle East escalation today"
kimi_search --query "Iran sanctions US latest"

# 或使用 web_search (如果配置了 Brave API)
web_search --query "Israel Iran latest developments" --freshness pd
```

### 3. 其他汇率和商品价格

```bash
# USD/RUB
python3 skills/market-data-fetch/scripts/fetch_market_data.py --fx USDRUB=X --demo

# 油价
python3 skills/market-data-fetch/scripts/fetch_market_data.py --ticker BZ=F --demo

# 黄金
python3 skills/market-data-fetch/scripts/fetch_market_data.py --ticker GC=F --demo
```

**注意**: 移除 `--demo` 参数可尝试获取真实数据，但可能因网络限制失败

### 4. Kalshi 预测市场数据

```bash
# 需要 API Key 和网络访问
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --fed
```

---

## 优化后的报告生成

### 快速生成 (含演示数据)

```bash
# 基础报告
python3 skills/geopol-risk-dashboard/scripts/comprehensive_analysis.py

# 优化版报告 (明确标记数据来源)
python3 skills/geopol-risk-dashboard/scripts/optimized_analysis.py
```

### 获取真实新闻后手动输入

由于新闻数据需要实时获取，建议流程:

1. **获取新闻**:
   ```bash
   kimi_search --query "Israel Iran latest news"
   ```

2. **手动输入到分析** (修改脚本或创建新脚本)

3. **生成报告**:
   ```bash
   python3 skills/geopol-risk-dashboard/scripts/optimized_analysis.py
   ```

---

## 数据质量改进建议

### 方案1: 手动数据输入 (推荐)

创建一个接受手动输入的脚本:

```python
# manual_input_analysis.py
news_items = [
    {
        "source": "Reuters",
        "headline": "[从kimi_search获取的真实标题]",
        "impact": "high",
        "is_real_data": True
    }
]

usdcny_rate = 7.2485  # 从 akshare 获取的真实汇率
```

### 方案2: 数据缓存机制

定期获取数据并缓存:

```bash
# 每小时获取一次数据
crontab -e
0 * * * * python3 skills/geopol-risk-dashboard/scripts/fetch_and_cache_data.py
```

### 方案3: API 接入

接入付费 API 获取稳定数据:
- Alpha Vantage (股票、外汇)
- Reuters API (新闻)
- Bloomberg API (市场数据)

---

## 当前报告文件

| 文件 | 说明 |
|------|------|
| `comprehensive_geopol_fx_report_YYYYMMDD.md` | 综合分析报告 (可能含演示数据) |
| `optimized_report_YYYYMMDD.md` | 优化版报告 (明确标记数据来源) |
| `middle_east_risk_fx_analysis_2026-03-16.md` | 历史报告 |

---

## 验证数据真实性

### 检查 USD/CNY

```python
import akshare as ak

# 获取最新汇率
df = ak.fx_spot_quote()
usdcny = df[df['货币对'] == 'USD/CNY']

print(f"USD/CNY 买报价: {usdcny['买报价'].iloc[0]}")
print(f"USD/CNY 卖报价: {usdcny['卖报价'].iloc[0]}")
print(f"数据时间: {datetime.now()}")
```

### 验证报告中的数据标记

打开报告文件，检查表格:
```markdown
| 数据类型 | 来源 | 状态 |
|----------|------|------|
| USDCNY | AKShare (中国银行) | ✅ 真实 |
```

---

## 总结

**已优化**:
- ✅ USD/CNY 使用真实数据 (AKShare)
- ✅ 明确标记所有数据来源
- ✅ 提供获取真实数据的方法

**待优化** (需用户手动或网络环境):
- ⬜ 实时新闻 (需 kimi_search)
- ⬜ USD/RUB (需 Yahoo Finance 网络)
- ⬜ 商品价格 (需 Yahoo Finance 网络)
- ⬜ Kalshi 预测市场 (需 API Key)

**建议**:
1. 对于 USD/CNY，当前已使用真实数据 ✅
2. 对于新闻，建议定期使用 kimi_search 获取最新信息
3. 对于其他汇率，如 Yahoo Finance 受限，可考虑接入其他 API
