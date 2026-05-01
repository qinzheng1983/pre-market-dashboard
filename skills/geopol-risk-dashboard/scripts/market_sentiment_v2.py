#!/usr/bin/env python3
"""
市场情绪分析模块 v2.0 - 优化版
更合理地计算恐慌指数和避险需求
"""

from datetime import datetime
from typing import Dict, List, Tuple

class MarketSentimentAnalyzerV2:
    """市场情绪分析器 v2.0 - 优化权重和归一化"""
    
    def __init__(self):
        # 历史基准数据（用于归一化）
        self.historical_benchmarks = {
            'oil_volatility_normal': 2.0,  # 正常油价日波动约2%
            'oil_volatility_crisis': 20.0,  # 危机时可达20%+
            'gold_safe_haven_normal': 0.5,  # 正常黄金日波动约0.5%
            'gold_safe_haven_crisis': 5.0,  # 避险时可达5%+
            'dxy_normal': 0.3,  # 正常美元指数日波动约0.3%
            'dxy_crisis': 2.0,  # 危机时可达2%+
        }
    
    def calculate_panic_index(self, 
                              risk_score: float,  # 地缘风险评分 0-10
                              oil_change_pct: float,  # 油价变化率 %
                              conflict_days: int,  # 冲突持续天数
                              escalation_events: List[str]  # 升级事件列表
                              ) -> float:
        """
        计算恐慌指数 (0-100)
        
        考虑因素：
        1. 地缘风险基础评分 (40%)
        2. 油价波动幅度 (30%) - 相对于历史基准归一化
        3. 冲突持续时间 (15%) - 时间越长，疲劳但累积风险
        4. 升级事件 (15%) - 重大突发事件
        """
        # 1. 地缘风险基础分 (0-10映射到0-40)
        risk_component = min(40, risk_score * 4)
        
        # 2. 油价波动分 - 相对于危机基准归一化
        # 油价涨51.74%，危机基准20%，则油价分 = 51.74/20 * 30 = 77.6，但上限30
        oil_volatility_score = min(30, abs(oil_change_pct) / self.historical_benchmarks['oil_volatility_crisis'] * 30)
        
        # 3. 持续时间因子 - 冲突越久，市场越疲劳但风险累积
        # 1周内：低权重，1-4周：中等，1月+：高权重但边际递减
        if conflict_days <= 7:
            duration_factor = conflict_days / 7 * 10  # 0-10
        elif conflict_days <= 30:
            duration_factor = 10 + (conflict_days - 7) / 23 * 5  # 10-15
        else:
            duration_factor = 15  # 封顶
        
        # 4. 升级事件分
        escalation_score = min(15, len(escalation_events) * 5)  # 每个事件5分，封顶15
        
        panic_index = risk_component + oil_volatility_score + duration_factor + escalation_score
        return min(100, round(panic_index, 1))
    
    def calculate_safe_haven_demand(self,
                                   gold_change_pct: float,
                                   dxy_change_pct: float,
                                   panic_index: float) -> float:
        """
        计算避险需求 (0-100)
        
        逻辑：
        1. 黄金和美元同时上涨 = 强烈避险需求
        2. 相对于各自的历史波动基准归一化
        3. 与恐慌指数联动 - 恐慌越高，对避险资产的需求应该越高
        
        修正后的归一化：
        - 黄金涨1.37%：相对于危机基准5% = 27.4分
        - 美元涨3.55%：相对于危机基准2% = 53.3分
        - 综合：(27.4 + 53.3) / 2 = 40.3分
        """
        # 黄金避险分 - 相对于危机基准
        gold_score = min(50, abs(gold_change_pct) / self.historical_benchmarks['gold_safe_haven_crisis'] * 50)
        
        # 美元避险分 - 相对于危机基准
        dxy_score = min(50, abs(dxy_change_pct) / self.historical_benchmarks['dxy_crisis'] * 50)
        
        # 基础避险需求
        base_safe_haven = (gold_score + dxy_score) / 2
        
        # 与恐慌指数联动调整
        # 如果恐慌指数很高但避险需求低，可能是模型问题或资金犹豫
        # 调整：让避险需求向恐慌指数靠拢（恐慌应该驱动避险）
        expected_safe_haven = panic_index * 0.7  # 恐慌指数的70%应该是避险需求
        
        # 加权平均：实际观测60% + 预期40%
        final_safe_haven = base_safe_haven * 0.6 + expected_safe_haven * 0.4
        
        return min(100, round(final_safe_haven, 1))
    
    def calculate_overall_sentiment(self, panic_index: float, safe_haven_demand: float) -> Dict:
        """
        计算综合情绪指数 (-100到+100)
        
        逻辑：
        - 负值 = 恐慌/悲观
        - 正值 = 乐观
        - 0 = 中性
        
        权重：恐慌60% + 避险需求40%（避险需求高也反映不安情绪）
        """
        # 综合情绪 = -(恐慌 × 0.6 + 避险需求 × 0.4)
        # 避险需求高也是负面情绪的一部分（说明市场不安）
        overall_score = -(panic_index * 0.6 + safe_haven_demand * 0.4)
        
        # 情绪分类
        if overall_score <= -80:
            sentiment_label = "极度恐慌"
            sentiment_emoji = "🔴🔴🔴🔴"
            color = "#8B0000"
        elif overall_score <= -60:
            sentiment_label = "高度恐慌"
            sentiment_emoji = "🔴🔴🔴"
            color = "#DC143C"
        elif overall_score <= -40:
            sentiment_label = "中度恐慌"
            sentiment_emoji = "🔴🔴"
            color = "#FF6347"
        elif overall_score <= -20:
            sentiment_label = "轻度担忧"
            sentiment_emoji = "🟠"
            color = "#FF8C00"
        elif overall_score < 0:
            sentiment_label = "谨慎"
            sentiment_emoji = "🟡"
            color = "#FFD700"
        elif overall_score < 20:
            sentiment_label = "中性偏乐观"
            sentiment_emoji = "🟢"
            color = "#90EE90"
        else:
            sentiment_label = "乐观"
            sentiment_emoji = "🟢🟢"
            color = "#228B22"
        
        return {
            'overall_score': round(overall_score, 1),
            'sentiment_label': sentiment_label,
            'sentiment_emoji': sentiment_emoji,
            'color': color
        }
    
    def analyze_sentiment_reality_gap(self, 
                                       sentiment_score: float,
                                       market_movement: float,
                                       panic_index: float,
                                       safe_haven_demand: float) -> Dict:
        """
        分析情绪-现实差距 (Sentiment-Reality Gap)
        
        新逻辑：
        - 比较恐慌指数和避险需求的差距
        - 如果恐慌很高但避险需求不高 = 情绪与现实脱节 = 可能反转或继续恐慌
        """
        gap = panic_index - safe_haven_demand
        
        if gap > 30:
            gap_assessment = "恐慌远超避险，情绪过度反应"
            signal = "严重超卖，关注反弹机会"
            confidence = "高"
        elif gap > 15:
            gap_assessment = "恐慌高于避险，情绪略显过度"
            signal = "可能存在交易机会"
            confidence = "中高"
        elif gap < -20:
            gap_assessment = "避险高于恐慌，资金积极避险"
            signal = "市场已充分定价风险"
            confidence = "中"
        else:
            gap_assessment = "恐慌与避险基本匹配"
            signal = "情绪与现实一致，趋势可能延续"
            confidence = "中"
        
        return {
            'gap_value': round(gap, 1),
            'assessment': gap_assessment,
            'signal': signal,
            'confidence': confidence
        }
    
    def analyze_current_situation(self) -> Dict:
        """分析当前中东局势的市场情绪"""
        
        # 当前实际数据
        current_data = {
            'risk_score': 9.5,  # 地缘风险评分 (美国设施遭袭后)
            'oil_change_pct': 51.74,  # 油价涨幅
            'gold_change_pct': 1.37,  # 黄金涨幅
            'dxy_change_pct': 3.55,  # 美元指数涨幅
            'conflict_days': 16,  # 冲突持续天数
            'escalation_events': [
                '美国设施遭袭',  # 3月15日
                '新领导人上任',  # 3月12日
                '军事行动延长',  # 3月15日
            ]
        }
        
        # 计算各项指标
        panic_index = self.calculate_panic_index(
            current_data['risk_score'],
            current_data['oil_change_pct'],
            current_data['conflict_days'],
            current_data['escalation_events']
        )
        
        safe_haven_demand = self.calculate_safe_haven_demand(
            current_data['gold_change_pct'],
            current_data['dxy_change_pct'],
            panic_index
        )
        
        sentiment = self.calculate_overall_sentiment(panic_index, safe_haven_demand)
        
        gap_analysis = self.analyze_sentiment_reality_gap(
            sentiment['overall_score'],
            current_data['dxy_change_pct'],
            panic_index,
            safe_haven_demand
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'data_inputs': current_data,
            'panic_index': panic_index,
            'safe_haven_demand': safe_haven_demand,
            'overall_sentiment': sentiment,
            'gap_analysis': gap_analysis,
            'breakdown': {
                'panic_components': {
                    '地缘风险基础分': min(40, current_data['risk_score'] * 4),
                    '油价波动分': min(30, abs(current_data['oil_change_pct']) / 20 * 30),
                    '持续时间分': 15,  # 16天 = 封顶15分
                    '升级事件分': min(15, len(current_data['escalation_events']) * 5),
                },
                'safe_haven_components': {
                    '黄金避险分': min(50, abs(current_data['gold_change_pct']) / 5 * 50),
                    '美元避险分': min(50, abs(current_data['dxy_change_pct']) / 2 * 50),
                    '恐慌联动调整': panic_index * 0.7,
                }
            }
        }
    
    def generate_report(self) -> str:
        """生成完整的情绪分析报告"""
        result = self.analyze_current_situation()
        
        report = f"""
# 📊 市场情绪分析报告 v2.0

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**分析模型**: Sentiment Analyzer v2.0 (优化归一化)

---

## 核心指标

| 指标 | 数值 | 评估 | 说明 |
|------|------|------|------|
| **综合情绪** | {result['overall_sentiment']['overall_score']}/100 | {result['overall_sentiment']['sentiment_emoji']} {result['overall_sentiment']['sentiment_label']} | 负值=恐慌，正值=乐观 |
| **恐慌指数** | {result['panic_index']}/100 | {'🔴' if result['panic_index'] > 70 else '🟠' if result['panic_index'] > 50 else '🟡'} {'极高' if result['panic_index'] > 80 else '高' if result['panic_index'] > 60 else '中等'} | 地缘风险+油价+时间+升级事件 |
| **避险需求** | {result['safe_haven_demand']}/100 | {'🔴' if result['safe_haven_demand'] > 70 else '🟠' if result['safe_haven_demand'] > 50 else '🟡'} {'极高' if result['safe_haven_demand'] > 70 else '高' if result['safe_haven_demand'] > 50 else '中等'} | 黄金+美元，经历史基准归一化 |
| **情绪-现实差** | {result['gap_analysis']['gap_value']} | {'🔴 严重偏离' if abs(result['gap_analysis']['gap_value']) > 30 else '🟠 轻度偏离' if abs(result['gap_analysis']['gap_value']) > 15 else '🟢 基本匹配'} | 恐慌与避险的匹配度 |

---

## 恐慌指数计算明细

| 构成项 | 原始值 | 权重 | 得分 | 计算逻辑 |
|--------|--------|------|------|----------|
| 地缘风险基础 | {result['data_inputs']['risk_score']}/10 | 40% | {result['breakdown']['panic_components']['地缘风险基础分']}/40 | 风险分×4 |
| 油价波动 | +{result['data_inputs']['oil_change_pct']}% | 30% | {result['breakdown']['panic_components']['油价波动分']}/30 | 涨幅/20%×30 |
| 持续时间 | {result['data_inputs']['conflict_days']}天 | 15% | {result['breakdown']['panic_components']['持续时间分']}/15 | 16天=封顶 |
| 升级事件 | {len(result['data_inputs']['escalation_events'])}个 | 15% | {result['breakdown']['panic_components']['升级事件分']}/15 | 每个5分 |
| **总计** | - | 100% | **{result['panic_index']}**/100 | - |

**升级事件清单**:
"""
        for event in result['data_inputs']['escalation_events']:
            report += f"- {event}\n"
        
        report += f"""
---

## 避险需求计算明细

| 构成项 | 原始涨幅 | 历史基准 | 归一化得分 | 计算逻辑 |
|--------|----------|----------|------------|----------|
| 黄金 | +{result['data_inputs']['gold_change_pct']}% | 危机时5% | {result['breakdown']['safe_haven_components']['黄金避险分']:.1f}/50 | 1.37/5×50 |
| 美元 | +{result['data_inputs']['dxy_change_pct']}% | 危机时2% | {result['breakdown']['safe_haven_components']['美元避险分']:.1f}/50 | 3.55/2×50 |
| 基础避险分 | - | - | {(result['breakdown']['safe_haven_components']['黄金避险分'] + result['breakdown']['safe_haven_components']['美元避险分'])/2:.1f} | 黄金+美元平均 |
| 恐慌联动调整 | {result['panic_index']}×0.7 | 40% | {result['breakdown']['safe_haven_components']['恐慌联动调整']:.1f} | 恐慌应驱动避险 |
| **最终避险需求** | - | 100% | **{result['safe_haven_demand']}**/100 | 观测60%+预期40% |

---

## 情绪-现实差距分析

**差距值**: {result['gap_analysis']['gap_value']}

| 评估 | 信号 | 信心度 |
|------|------|--------|
| {result['gap_analysis']['assessment']} | {result['gap_analysis']['signal']} | {result['gap_analysis']['confidence']} |

**解读**: 
- 差距为正 = 恐慌 > 避险（情绪过度，可能超卖）
- 差距为负 = 避险 > 恐慌（资金已避险，风险定价充分）
- 当前差距{result['gap_analysis']['gap_value']} = {'恐慌远高于避险' if result['gap_analysis']['gap_value'] > 20 else '基本平衡'}

---

## 模型改进说明 v2.0

### 相对于v1.0的优化

1. **恐慌指数更合理**
   - 油价51%涨幅按危机基准20%归一化，得77分→封顶30分
   - 加入冲突持续时间和升级事件因子

2. **避险需求归一化修正**
   - v1.0：黄金1.37%×3=4.11分（过低）
   - v2.0：1.37%/5%×50=13.7分（更合理）
   - 加入恐慌联动调整，避免恐慌高但避险低的矛盾

3. **综合情绪区间细分**
   - 从4档细化为6档，更精确描述情绪状态
   - 当前{result['overall_sentiment']['sentiment_label']}（{result['overall_sentiment']['overall_score']}/100）

---

*模型版本: v2.0 | 数据截至: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return report


if __name__ == "__main__":
    analyzer = MarketSentimentAnalyzerV2()
    report = analyzer.generate_report()
    print(report)
    
    # 同时输出JSON格式结果
    result = analyzer.analyze_current_situation()
    print("\n\n" + "="*70)
    print("📊 核心结果摘要")
    print("="*70)
    print(f"综合情绪: {result['overall_sentiment']['overall_score']}/100 ({result['overall_sentiment']['sentiment_label']})")
    print(f"恐慌指数: {result['panic_index']}/100")
    print(f"避险需求: {result['safe_haven_demand']}/100")
    print(f"情绪-现实差: {result['gap_analysis']['gap_value']}")
