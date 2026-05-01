#!/usr/bin/env python3
"""
市场情绪分析模块
分析地缘冲突对市场情绪的影响
"""

from datetime import datetime
from typing import Dict, List, Tuple

class MarketSentimentAnalyzer:
    """市场情绪分析器"""
    
    def __init__(self):
        # 情绪指标权重
        self.indicators = {
            'vix': 0.25,  # 波动率指数
            'risk_appetite': 0.25,  # 风险偏好
            'safe_haven_flow': 0.25,  # 避险资金流向
            'media_tone': 0.25,  # 媒体语调
        }
    
    def analyze_geopol_sentiment(self, risk_score: float, oil_change: float, 
                                  gold_change: float, dxy_change: float) -> Dict:
        """
        分析地缘冲突对市场情绪的影响
        
        Args:
            risk_score: 地缘风险评分 (0-100)
            oil_change: 油价变化率
            gold_change: 金价变化率
            dxy_change: 美元指数变化率
        
        Returns:
            情绪分析结果
        """
        # 计算各个维度的情绪指标
        
        # 1. 恐慌指数 (基于风险评分和油价)
        fear_level = min(100, risk_score * 0.8 + abs(oil_change) * 2)
        
        # 2. 避险需求 (基于黄金和美元)
        safe_haven_demand = (gold_change * 3 + dxy_change * 5) / 2
        
        # 3. 整体情绪评分 (-100到+100，负值表示恐慌)
        overall_sentiment = -(fear_level * 0.6 + safe_haven_demand * 0.4)
        
        # 4. 情绪分类
        if overall_sentiment < -60:
            sentiment_label = "极度恐慌"
            sentiment_emoji = "🔴🔴🔴"
            color = "#8B0000"
        elif overall_sentiment < -30:
            sentiment_label = "恐慌"
            sentiment_emoji = "🔴🔴"
            color = "#DC143C"
        elif overall_sentiment < -10:
            sentiment_label = "担忧"
            sentiment_emoji = "🟠"
            color = "#FF8C00"
        elif overall_sentiment < 10:
            sentiment_label = "中性"
            sentiment_emoji = "🟡"
            color = "#FFD700"
        else:
            sentiment_label = "乐观"
            sentiment_emoji = "🟢"
            color = "#228B22"
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_score': round(overall_sentiment, 2),
            'fear_level': round(fear_level, 2),
            'safe_haven_demand': round(safe_haven_demand, 2),
            'sentiment_label': sentiment_label,
            'sentiment_emoji': sentiment_emoji,
            'color': color,
            'indicators': {
                'geopolitical_risk': {'value': risk_score, 'weight': 0.35, 'impact': 'high'},
                'oil_volatility': {'value': abs(oil_change) * 10, 'weight': 0.25, 'impact': 'high'},
                'gold_safe_haven': {'value': gold_change * 10, 'weight': 0.20, 'impact': 'medium'},
                'dxy_strength': {'value': dxy_change * 20, 'weight': 0.20, 'impact': 'medium'},
            }
        }
    
    def analyze_sentiment_reality_gap(self, sentiment_score: float, 
                                       actual_market_move: float) -> Dict:
        """
        分析情绪与现实的差距 (Sentiment-Reality Gap)
        
        当情绪过度悲观/乐观时，往往预示着市场反转机会
        """
        gap = abs(sentiment_score) - abs(actual_market_move) * 10
        
        if gap > 30:
            gap_assessment = "情绪过度反应"
            signal = "可能出现反转"
            confidence = "高"
        elif gap > 15:
            gap_assessment = "情绪略显过度"
            signal = "谨慎观察"
            confidence = "中"
        else:
            gap_assessment = "情绪与现实基本一致"
            signal = "趋势可能延续"
            confidence = "低"
        
        return {
            'gap_value': round(gap, 2),
            'assessment': gap_assessment,
            'signal': signal,
            'confidence': confidence,
            'interpretation': self._get_gap_interpretation(gap, sentiment_score)
        }
    
    def _get_gap_interpretation(self, gap: float, sentiment: float) -> str:
        """获取差距解读"""
        if sentiment < -50 and gap > 20:
            return "市场过度恐慌，可能存在超卖机会。关注反弹信号。"
        elif sentiment > 50 and gap > 20:
            return "市场过度乐观，需警惕回调风险。"
        elif -20 <= sentiment <= 20:
            return "市场情绪相对平衡，关注基本面变化。"
        else:
            return "情绪与走势基本匹配，当前趋势可能延续。"
    
    def generate_sentiment_report(self) -> str:
        """生成市场情绪分析报告"""
        # 基于当前地缘冲突情况的数据
        risk_score = 90  # 极高风险
        oil_change = 15.56  # 原油涨幅
        gold_change = 7.55  # 黄金涨幅
        dxy_change = 0.16  # 美元涨幅
        
        sentiment = self.analyze_geopol_sentiment(risk_score, oil_change, gold_change, dxy_change)
        gap_analysis = self.analyze_sentiment_reality_gap(sentiment['overall_score'], dxy_change)
        
        report = f"""
## 📊 市场情绪分析报告

### 综合情绪评分

**当前情绪**: {sentiment['sentiment_emoji']} {sentiment['sentiment_label']} ({sentiment['overall_score']:.1f}/100)

**恐慌指数**: {sentiment['fear_level']:.1f}/100
**避险需求**: {sentiment['safe_haven_demand']:.1f}/100

---

### 情绪指标分解

| 指标 | 数值 | 权重 | 影响 |
|------|------|------|------|
| 地缘风险 | {sentiment['indicators']['geopolitical_risk']['value']:.1f} | 35% | 极高 |
| 原油波动 | {sentiment['indicators']['oil_volatility']['value']:.1f} | 25% | 高 |
| 黄金避险 | {sentiment['indicators']['gold_safe_haven']['value']:.1f} | 20% | 中 |
| 美元强势 | {sentiment['indicators']['dxy_strength']['value']:.1f} | 20% | 中 |

---

### 情绪-现实差距分析 (Sentiment-Reality Gap)

**差距评估**: {gap_analysis['assessment']}
**信号**: {gap_analysis['signal']}
**信心度**: {gap_analysis['confidence']}

**解读**: {gap_analysis['interpretation']}

---

### 情绪趋势判断

- **短期 (1周内)**: 恐慌情绪可能维持高位，波动加剧
- **中期 (1-3月)**: 情绪取决于冲突进展，若缓和则恐慌回落
- **长期 (3月+)**: 市场将逐步消化风险，情绪回归基本面

---

### 对冲建议 (基于情绪分析)

1. **恐慌高峰期** (当前): 避免追涨杀跌，保持理性对冲比例
2. **情绪过度反应**: 关注反向交易机会，如超卖后的反弹
3. **避险资产**: 黄金、美元短期受追捧，注意估值风险
4. **风险资产**: 原油波动大，适合波段操作而非长期持有

---

*报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return report

if __name__ == "__main__":
    analyzer = MarketSentimentAnalyzer()
    report = analyzer.generate_sentiment_report()
    print(report)
