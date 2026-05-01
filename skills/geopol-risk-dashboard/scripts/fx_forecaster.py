#!/usr/bin/env python3
"""
汇率预测与对冲分析模块
基于地缘风险、利差、贸易数据预测 USD/CNY 走势
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from enum import Enum

class Trend(Enum):
    APPRECIATION = "appreciation"    # 人民币升值
    DEPRECIATION = "depreciation"    # 人民币贬值
    STABLE = "stable"                # 区间波动

@dataclass
class FXScenario:
    """汇率情景"""
    name: str                        # 情景名称
    probability: float               # 概率 (0-1)
    fx_range: Tuple[float, float]    # 汇率区间
    catalyst: str                    # 触发因素
    risk_level: str                  # 风险等级
    hedge_ratio: int                 # 建议对冲比例
    description: str                 # 详细描述

@dataclass
class FXSignal:
    """汇率信号"""
    factor: str                      # 因素名称
    weight: float                    # 权重
    current_value: float             # 当前值
    direction: str                   # 方向: bullish/bearish/neutral
    impact: str                      # 影响程度: high/medium/low
    
class FXForecaster:
    """汇率预测器"""
    
    def __init__(self, base_fx: float = 7.25):
        self.base_fx = base_fx         # 基准汇率
        self.signals: List[FXSignal] = []
        self.scenarios: List[FXScenario] = []
        
    def add_geopol_signal(self, risk_score: float):
        """添加地缘风险信号"""
        # 风险分数 0-100，越高人民币贬值压力越大
        if risk_score > 60:
            direction = "bearish"
            impact = "high"
        elif risk_score > 40:
            direction = "bearish"
            impact = "medium"
        else:
            direction = "neutral"
            impact = "low"
            
        self.signals.append(FXSignal(
            factor="地缘风险",
            weight=0.30,
            current_value=risk_score,
            direction=direction,
            impact=impact
        ))
        
    def add_interest_rate_signal(self, cn_rate: float, us_rate: float):
        """添加利差信号"""
        spread = us_rate - cn_rate
        # 利差越大，人民币贬值压力越大
        if spread > 2.0:
            direction = "bearish"
            impact = "high"
        elif spread > 1.0:
            direction = "bearish"
            impact = "medium"
        elif spread > 0:
            direction = "neutral"
            impact = "low"
        else:
            direction = "bullish"
            impact = "medium"
            
        self.signals.append(FXSignal(
            factor="中美利差",
            weight=0.25,
            current_value=spread,
            direction=direction,
            impact=impact
        ))
        
    def add_trade_signal(self, trade_balance: float):
        """添加贸易顺差信号"""
        # 顺差越大，人民币升值动力越强
        if trade_balance > 500:  # 500亿美元
            direction = "bullish"
            impact = "high"
        elif trade_balance > 200:
            direction = "bullish"
            impact = "medium"
        elif trade_balance > 0:
            direction = "neutral"
            impact = "low"
        else:
            direction = "bearish"
            impact = "medium"
            
        self.signals.append(FXSignal(
            factor="贸易顺差",
            weight=0.20,
            current_value=trade_balance,
            direction=direction,
            impact=impact
        ))
        
    def add_capital_flow_signal(self, flow: float):
        """添加资本流动信号"""
        # 流入为正，流出为负
        if flow > 100:  # 100亿美元流入
            direction = "bullish"
            impact = "high"
        elif flow > 0:
            direction = "bullish"
            impact = "low"
        elif flow > -50:
            direction = "neutral"
            impact = "low"
        else:
            direction = "bearish"
            impact = "high"
            
        self.signals.append(FXSignal(
            factor="资本流动",
            weight=0.15,
            current_value=flow,
            direction=direction,
            impact=impact
        ))
        
    def add_oil_price_signal(self, oil_price: float):
        """添加油价信号（地缘风险传导）"""
        # 油价上涨 → 中国进口成本增加 → 人民币贬值压力
        if oil_price > 100:
            direction = "bearish"
            impact = "high"
        elif oil_price > 85:
            direction = "bearish"
            impact = "medium"
        elif oil_price > 70:
            direction = "neutral"
            impact = "low"
        else:
            direction = "bullish"
            impact = "low"
            
        self.signals.append(FXSignal(
            factor="原油价格",
            weight=0.10,
            current_value=oil_price,
            direction=direction,
            impact=impact
        ))
        
    def calculate_composite_signal(self) -> Dict:
        """计算综合信号"""
        bullish_score = 0
        bearish_score = 0
        
        for signal in self.signals:
            if signal.direction == "bullish":
                bullish_score += signal.weight
            elif signal.direction == "bearish":
                bearish_score += signal.weight
                
        net_score = bearish_score - bullish_score  # 正数表示贬值压力
        
        if net_score > 0.3:
            trend = Trend.DEPRECIATION
            intensity = "strong"
        elif net_score > 0.1:
            trend = Trend.DEPRECIATION
            intensity = "moderate"
        elif net_score > -0.1:
            trend = Trend.STABLE
            intensity = "neutral"
        elif net_score > -0.3:
            trend = Trend.APPRECIATION
            intensity = "moderate"
        else:
            trend = Trend.APPRECIATION
            intensity = "strong"
            
        return {
            "net_score": round(net_score, 3),
            "bullish_score": round(bullish_score, 3),
            "bearish_score": round(bearish_score, 3),
            "trend": trend.value,
            "intensity": intensity
        }
        
    def generate_scenarios(self) -> List[FXScenario]:
        """生成三种情景"""
        composite = self.calculate_composite_signal()
        
        if composite["trend"] == "depreciation":
            # 基准情景: 贬值
            base_scenarios = [
                FXScenario(
                    name="乐观情景",
                    probability=0.25,
                    fx_range=(7.15, 7.22),
                    catalyst="地缘缓和+利差收窄",
                    risk_level="LOW",
                    hedge_ratio=50,
                    description="美伊谈判取得突破，美联储降息预期升温，人民币汇率回升至7.20下方"
                ),
                FXScenario(
                    name="基准情景",
                    probability=0.50,
                    fx_range=(7.22, 7.35),
                    catalyst="当前格局延续",
                    risk_level="MEDIUM",
                    hedge_ratio=65,
                    description="地缘僵持，利差维持，人民币在7.20-7.35区间震荡"
                ),
                FXScenario(
                    name="悲观情景",
                    probability=0.25,
                    fx_range=(7.35, 7.55),
                    catalyst="地缘升级+资本外流",
                    risk_level="HIGH",
                    hedge_ratio=85,
                    description="霍尔木兹海峡封锁，油价暴涨，资本外流压力加大，人民币跌破7.35"
                )
            ]
        elif composite["trend"] == "appreciation":
            # 基准情景: 升值
            base_scenarios = [
                FXScenario(
                    name="乐观情景",
                    probability=0.30,
                    fx_range=(6.95, 7.10),
                    catalyst="美元走弱+中国经济复苏",
                    risk_level="LOW",
                    hedge_ratio=40,
                    description="美元进入降息周期，中国经济数据超预期，人民币汇率升至7.10下方"
                ),
                FXScenario(
                    name="基准情景",
                    probability=0.55,
                    fx_range=(7.10, 7.25),
                    catalyst="双向波动",
                    risk_level="LOW",
                    hedge_ratio=50,
                    description="中美利差收窄，人民币温和升值至7.10-7.25区间"
                ),
                FXScenario(
                    name="悲观情景",
                    probability=0.15,
                    fx_range=(7.25, 7.35),
                    catalyst="地缘冲突+美元反弹",
                    risk_level="MEDIUM",
                    hedge_ratio=60,
                    description="地缘冲突升级，美元避险需求回升，人民币升值趋势中断"
                )
            ]
        else:
            # 基准情景: 稳定
            base_scenarios = [
                FXScenario(
                    name="乐观情景",
                    probability=0.30,
                    fx_range=(7.15, 7.22),
                    catalyst="风险缓和",
                    risk_level="LOW",
                    hedge_ratio=55,
                    description="地缘风险降温，人民币偏向升值区间"
                ),
                FXScenario(
                    name="基准情景",
                    probability=0.50,
                    fx_range=(7.22, 7.30),
                    catalyst="多空平衡",
                    risk_level="MEDIUM",
                    hedge_ratio=60,
                    description="多空因素交织，人民币维持7.22-7.30窄幅波动"
                ),
                FXScenario(
                    name="悲观情景",
                    probability=0.20,
                    fx_range=(7.30, 7.40),
                    catalyst="风险事件",
                    risk_level="MEDIUM",
                    hedge_ratio=70,
                    description="突发风险事件，人民币测试7.40关口"
                )
            ]
            
        self.scenarios = base_scenarios
        return base_scenarios
        
    def calculate_expected_fx(self) -> float:
        """计算预期汇率（加权平均）"""
        if not self.scenarios:
            self.generate_scenarios()
            
        expected = sum(
            s.probability * (s.fx_range[0] + s.fx_range[1]) / 2
            for s in self.scenarios
        )
        return round(expected, 4)
        
    def get_hedge_recommendation(self) -> Dict:
        """获取对冲建议"""
        if not self.scenarios:
            self.generate_scenarios()
            
        # 计算加权对冲比例
        hedge_ratio = sum(s.probability * s.hedge_ratio for s in self.scenarios)
        
        composite = self.calculate_composite_signal()
        
        # 根据趋势调整
        if composite["trend"] == "depreciation":
            strategy = "防御型"
            products = ["远期结汇", "美元看涨期权", "风险逆转期权"]
        elif composite["trend"] == "appreciation":
            strategy = "积极型"
            products = ["远期购汇", "人民币看涨期权", "比例远期"]
        else:
            strategy = "平衡型"
            products = [" collar期权组合", "海鸥期权", "远期+期权组合"]
            
        return {
            "hedge_ratio": round(hedge_ratio),
            "strategy": strategy,
            "products": products,
            "confidence": composite["intensity"]
        }
        
    def generate_report(self) -> Dict:
        """生成完整报告"""
        composite = self.calculate_composite_signal()
        scenarios = self.generate_scenarios()
        expected_fx = self.calculate_expected_fx()
        hedge_rec = self.get_hedge_recommendation()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "base_fx": self.base_fx,
            "signals": [
                {
                    "factor": s.factor,
                    "weight": s.weight,
                    "value": s.current_value,
                    "direction": s.direction,
                    "impact": s.impact
                }
                for s in self.signals
            ],
            "composite": composite,
            "scenarios": [
                {
                    "name": s.name,
                    "probability": s.probability,
                    "fx_range": s.fx_range,
                    "catalyst": s.catalyst,
                    "risk_level": s.risk_level,
                    "hedge_ratio": s.hedge_ratio
                }
                for s in scenarios
            ],
            "expected_fx": expected_fx,
            "hedge_recommendation": hedge_rec
        }


def main():
    """示例用法"""
    forecaster = FXForecaster(base_fx=7.25)
    
    # 添加信号 (示例数据)
    forecaster.add_geopol_signal(risk_score=63.5)
    forecaster.add_interest_rate_signal(cn_rate=2.0, us_rate=4.5)
    forecaster.add_trade_signal(trade_balance=800)
    forecaster.add_capital_flow_signal(flow=-50)
    forecaster.add_oil_price_signal(oil_price=75)
    
    # 生成报告
    report = forecaster.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
