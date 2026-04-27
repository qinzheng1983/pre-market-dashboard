#!/usr/bin/env python3
"""
datetime_utils - 日期时间验证工具
用于验证盘前简报数据日期是否为前一交易日
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional

class TradingCalendar:
    """交易日历工具"""
    
    # 2025年中国法定节假日（简化版，实际需要更完整的数据）
    CHINA_HOLIDAYS_2025 = [
        "2025-01-01",  # 元旦
        "2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31",  # 春节
        "2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04",
        "2025-04-04", "2025-04-05", "2025-04-06",  # 清明
        "2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05",  # 五一
        "2025-05-31", "2025-06-01", "2025-06-02",  # 端午
        "2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04", "2025-10-05",  # 国庆
        "2025-10-06", "2025-10-07", "2025-10-08",
    ]
    
    # 美国主要节假日（影响美股交易）
    US_HOLIDAYS_2025 = [
        "2025-01-01",  # New Year's Day
        "2025-01-20",  # Martin Luther King Jr. Day
        "2025-02-17",  # Presidents' Day
        "2025-04-18",  # Good Friday
        "2025-05-26",  # Memorial Day
        "2025-06-19",  # Juneteenth
        "2025-07-04",  # Independence Day
        "2025-09-01",  # Labor Day
        "2025-11-27",  # Thanksgiving
        "2025-12-25",  # Christmas Day
    ]
    
    @classmethod
    def is_china_holiday(cls, date_str: str) -> bool:
        """检查是否为中国法定节假日"""
        return date_str in cls.CHINA_HOLIDAYS_2025
    
    @classmethod
    def is_us_holiday(cls, date_str: str) -> bool:
        """检查是否为美国法定节假日"""
        return date_str in cls.US_HOLIDAYS_2025
    
    @classmethod
    def get_previous_trading_day(cls, date: datetime, market: str = "US") -> datetime:
        """
        获取前一交易日
        market: "US" 美股, "CN" 中国
        """
        prev_day = date - timedelta(days=1)
        
        # 回退到最近的交易日
        while True:
            date_str = prev_day.strftime("%Y-%m-%d")
            weekday = prev_day.weekday()
            
            # 跳过周末
            if weekday >= 5:  # 周六=5, 周日=6
                prev_day -= timedelta(days=1)
                continue
            
            # 跳过节假日
            if market == "US" and cls.is_us_holiday(date_str):
                prev_day -= timedelta(days=1)
                continue
            
            if market == "CN" and cls.is_china_holiday(date_str):
                prev_day -= timedelta(days=1)
                continue
            
            break
        
        return prev_day
    
    @classmethod
    def validate_data_date(cls, data_date_str: str, reference_date: datetime = None) -> Tuple[bool, str]:
        """
        验证数据日期是否为前一交易日
        
        Args:
            data_date_str: 数据日期字符串 (YYYY-MM-DD)
            reference_date: 参考日期，默认为今天
            
        Returns:
            (是否有效, 验证信息)
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        try:
            data_date = datetime.strptime(data_date_str, "%Y-%m-%d")
        except ValueError:
            return False, f"日期格式错误: {data_date_str}"
        
        # 获取美股前一交易日
        prev_us_trading_day = cls.get_previous_trading_day(reference_date, "US")
        prev_cn_trading_day = cls.get_previous_trading_day(reference_date, "CN")
        
        # 检查数据日期是否匹配前一交易日
        if data_date.date() == prev_us_trading_day.date():
            return True, f"数据日期 {data_date_str} 确认为美股前一交易日"
        elif data_date.date() == prev_cn_trading_day.date():
            return True, f"数据日期 {data_date_str} 确认为A股前一交易日"
        else:
            expected_us = prev_us_trading_day.strftime("%Y-%m-%d")
            expected_cn = prev_cn_trading_day.strftime("%Y-%m-%d")
            return False, f"数据日期 {data_date_str} 不匹配前一交易日 (美股预期: {expected_us}, A股预期: {expected_cn})"
    
    @classmethod
    def get_data_quality_rating(cls, data_freshness_hours: int, source_count: int) -> Tuple[int, str]:
        """
        计算数据质量评级
        
        Args:
            data_freshness_hours: 数据新鲜度（小时）
            source_count: 独立数据源数量
            
        Returns:
            (星级 1-5, 评级说明)
        """
        stars = 5
        
        # 根据数据新鲜度扣分
        if data_freshness_hours <= 1:
            pass  # 保持5星
        elif data_freshness_hours <= 6:
            stars -= 0.5
        elif data_freshness_hours <= 12:
            stars -= 1
        elif data_freshness_hours <= 24:
            stars -= 1.5
        else:
            stars -= 2
        
        # 根据数据源数量扣分
        if source_count >= 3:
            pass  # 保持
        elif source_count == 2:
            stars -= 0.5
        elif source_count == 1:
            stars -= 1
        else:
            stars -= 2
        
        stars = max(1, min(5, int(stars)))
        
        rating_desc = {
            5: "数据质量优秀 - 实时数据，多源交叉验证",
            4: "数据质量良好 - 近期数据，可靠来源",
            3: "数据质量中等 - 存在一定延迟或来源有限",
            2: "数据质量较低 - 延迟较长或来源单一",
            1: "数据质量差 - 严重延迟或来源不可靠"
        }
        
        return stars, rating_desc.get(stars, "未知")


def main():
    """主函数 - 用于测试验证"""
    
    # 设置参考日期为 2026-04-13（周一），前一交易日应为 2026-04-10（周五）
    reference = datetime(2026, 4, 13, 8, 30, 0)
    
    # 验证数据日期
    data_date = "2026-04-10"
    is_valid, message = TradingCalendar.validate_data_date(data_date, reference)
    
    print("=" * 60)
    print("盘前简报数据日期验证")
    print("=" * 60)
    print(f"参考日期: {reference.strftime('%Y-%m-%d %H:%M')} (周一)")
    print(f"美股前一交易日: {TradingCalendar.get_previous_trading_day(reference, 'US').strftime('%Y-%m-%d')}")
    print(f"数据日期: {data_date}")
    print(f"验证结果: {'通过' if is_valid else '失败'}")
    print(f"验证信息: {message}")
    
    # 计算数据质量评级
    # 假设数据为收盘数据（约16小时前），2个独立来源
    freshness = 16  # 小时
    sources = 3
    stars, desc = TradingCalendar.get_data_quality_rating(freshness, sources)
    
    print(f"\n数据质量评级: {'⭐' * stars}")
    print(f"评级说明: {desc}")
    print(f"数据时效: {freshness}小时前")
    print(f"独立来源: {sources}个")
    
    return is_valid, stars


if __name__ == "__main__":
    main()
