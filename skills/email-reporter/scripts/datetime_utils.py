#!/usr/bin/env python3
"""
Datetime Utils - 日期时间验证工具
用于验证报告数据的时效性
"""

from datetime import datetime, timedelta

def validate_data_date(target_date_str: str, current_date_str: str = None) -> dict:
    """
    验证数据日期是否符合报告要求
    
    Args:
        target_date_str: 目标数据日期 (YYYY-MM-DD)
        current_date_str: 当前日期 (YYYY-MM-DD)，默认为今天
    
    Returns:
        dict: 验证结果
    """
    if current_date_str is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    
    # 计算日期差
    delta = (current_date - target_date).days
    
    result = {
        "target_date": target_date_str,
        "current_date": current_date.strftime("%Y-%m-%d"),
        "delta_days": delta,
        "is_valid": delta <= 1,  # 盘前简报要求前一交易日数据
        "data_type": "前一交易日收盘数据 (T-1)" if delta == 1 else "当日数据 (T)" if delta == 0 else "历史数据",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return result

def get_last_trading_day(date_str: str = None) -> str:
    """
    获取前一交易日日期（考虑周末）
    """
    if date_str is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    
    weekday = date.weekday()  # 0=周一, 6=周日
    
    if weekday == 0:  # 周一，前一交易日是上周五
        last_trading = date - timedelta(days=3)
    elif weekday == 6:  # 周日，前一交易日是上周五
        last_trading = date - timedelta(days=2)
    else:
        last_trading = date - timedelta(days=1)
    
    return last_trading.strftime("%Y-%m-%d")

def format_report_timestamp() -> str:
    """生成报告时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M CST")

if __name__ == "__main__":
    # 测试
    print(validate_data_date("2026-04-13", "2026-04-14"))
    print(get_last_trading_day("2026-04-14"))
