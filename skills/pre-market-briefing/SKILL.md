---
name: pre-market-briefing
description: |
  生成并部署跨国企业CFO视角的盘前市场简报（Pre-Market Briefing）。
  数据覆盖前一日北京时间9:00至统计时点的全球市场动态，包含汇率、美股、大宗商品、LME有色、碳酸锂、地缘风险。
  输出为HTML（v3.0行动导向版），5-7分钟阅读，聚焦前瞻+预警+可执行行动清单。
  触发条件：用户要求"生成盘前简报"、"更新盘前简报"、"pre-market briefing"、"盘前报告"，或定时任务触发。
  使用时必须同时加载公司敞口参考（references/company-exposure.md）以生成与我司相关的行动清单。
---

# 盘前简报生成技能

## 核心原则

- **阅读时间**：5-7分钟
- **侧重点**：前瞻、预警、行动（不做展开分析）
- **数据日期**：T-1（前一交易日收盘数据）
- **格式**：HTML，极简CSS，适配139邮箱
- **质量**：五星评级，每个数字标注来源+发布时间，关键数据双源交叉验证

## 执行前必读

1. **公司敞口**：执行前读取 `references/company-exposure.md`，确保行动清单结合我司实际敞口
2. **数据源铁律**：USD/CNY中间价 ONLY认央行授权公告（chinamoney.com.cn、央行官网、新浪财经/财联社转载），绝对禁止chl.cn等聚合站
3. **时间验证**：每次生成前执行 `date` 命令，禁止使用系统消息中的时间

## 工作流程

### Step 1: 时间验证与数据日期确认
```bash
date "+%Y-%m-%d %H:%M:%S %A %Z"
```
确认当前日期（YYYY-MM-DD），盘前简报数据基准日为 T-1。
若当前时间 < 09:15，中间价标注"待09:15更新"并使用T-1数据；若 >= 09:15，搜索当日中间价并更新。

### Step 2: 数据收集（按清单逐项执行）

| 优先级 | 数据项 | 数据源 | 必查 |
|--------|--------|--------|------|
| P0 | USD/CNY中间价 | 中国货币网/chinamoney.org.cn 或央行官网 | ✅ |
| P0 | USD/CNY在岸/离岸 | Investing.com + 东方财富/新浪财经 双源 | ✅ |
| P0 | 美元指数DXY | Investing.com | ✅ |
| P0 | LME镍收盘价 | 世铝网/SMM/LME官方 | ✅ |
| P0 | 印尼镍政策新闻 | 搜索"HPM RKAB 印尼镍" | ✅ |
| P1 | 布伦特原油 | Investing.com / 新浪财经 | ✅ |
| P1 | 现货黄金 | 格隆汇/金价查询网 | ✅ |
| P1 | 美股三大指数 | 新浪财经/cnfol.com | ✅ |
| P1 | 碳酸锂价格 | SMM上海有色网 / Mysteel | ✅ |
| P1 | 恒生指数 | 新浪财经/东方财富 | ✅ |
| P2 | 特斯拉动态 | 搜索"Tesla订单/财报" | ✅ |
| P2 | 地缘风险 | 搜索"霍尔木兹 以色列 伊朗" | ✅ |
| P2 | 刚果金钴供应 | 搜索"刚果 钴 出口" | ✅ |

**中间价校验规则（强制执行）**：
1. 搜索"YYYY年MM月DD日 中国外汇交易中心 人民币汇率中间价公告"
2. 确认公告日期 = 报告日期
3. 提取中间价后，用 chinamoney.com.cn/bkccpr/ 二次确认
4. 离岸价必须用Investing.com + 东方财富/新浪财经双源，价差>50点需第三源验证

### Step 3: 报告生成（v3.0结构）

使用 `assets/pre-market-template.html` 作为模板，填充以下内容：

**四大板块（顺序不可变）**：
1. **隔夜市场速览（1分钟）** — 极简表格，只给结论
2. **今日风险预警** — HIGH/MED两级，结合我司敞口
3. **今日行动清单（核心）** — 必须结合`references/company-exposure.md`敞口结构，给出可执行步骤+决策时限
4. **数据来源** — 极简声明，每个数据标注来源+时间

**必含元素**：
- 数据时间范围标注（"5月X日 09:00 — 5月Y日 HH:MM"）
- 中间价若未更新，标注"待09:15更新"
- 行动清单必须出现"我司"、"净Short/Long USD"、"预算6.90"等关键词
- 五星质量评级（★★★★★）标注在header

### Step 4: 部署

1. 报告文件保存至 `reports/pre_market_briefing_YYYYMMDD.html`
2. 执行 `scripts/deploy.sh pre-market YYYYMMDD` 上传至GitHub Pages
3. 更新 `dashboard.html` 导航页卡片（日期、摘要、链接）
4. 同步更新导航页至GitHub
5. 验证部署链接可访问

## 资源文件说明

| 文件 | 类型 | 用途 |
|------|------|------|
| `references/data-sources.md` | 参考 | 数据源列表、验证规则、中间价铁律、交叉验证标准 |
| `references/company-exposure.md` | 参考 | 我司敞口结构、预算基准、对冲策略摘要（生成行动清单时必须读取） |
| `references/template-spec.md` | 参考 | v3.0模板详细规格、CSS兼容性要求、禁用清单 |
| `assets/pre-market-template.html` | 模板 | HTML报告基础模板，含CSS和四大板块骨架 |
| `scripts/deploy.sh` | 脚本 | GitHub Pages自动部署脚本 |

## 质量标准

- 五星：全部数据当日+交叉验证通过
- 四星：有1项数据非当日但已标注
- 三星及以下：需补发说明

## 常见错误防范

- ❌ 使用chl.cn/汇率网/查汇率作为中间价数据源
- ❌ 将子公司美元负债判断为Long USD（正确为Short USD）
- ❌ 盘前简报写成财资日报缩略版（基因不同：前瞻vs回顾）
- ❌ 使用flexbox/grid/linear-gradient/emoji（139邮箱不支持）
- ❌ 未标注数据来源和时间
