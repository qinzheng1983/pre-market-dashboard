#!/usr/bin/env python3
"""
Datetime Utils - 金融数据报告日期时间管理工具
"""

from datetime import datetime, timedelta
from typing import Optional, Literal
import pytz

class DateTimeUtils:
    """日期时间工具类"""
    
    # 中国节假日（2026年）
    CN_HOLIDAYS_2026 = [
        "2026-01-01",  # 元旦
        "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21", "2026-02-22", "2026-02-23",  # 春节
        "2026-04-04", "2026-04-05", "2026-04-06",  # 清明节
        "2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05",  # 劳动节
        "2026-06-19", "2026-06-20", "2026-06-21", "2026-06-22",  # 端午节
        "2026-09-25", "2026-09-26", "2026-09-27",  # 中秋节
        "2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08",  # 国庆节
    ]
    
    # 美国节假日（2026年）
    US_HOLIDAYS_2026 = [
        "2026-01-01",  # New Year's Day
        "2026-01-19",  # Martin Luther King Jr. Day
        "2026-02-16",  # Presidents' Day
        "2026-04-03",  # Good Friday
        "2026-05-25",  # Memorial Day
        "2026-07-03",  # Independence Day (observed)
        "2026-09-07",  # Labor Day
        "2026-11-26",  # Thanksgiving Day
        "2026-12-25",  # Christmas Day
    ]
    
    def __init__(self):
        self.tz_shanghai = pytz.timezone("Asia/Shanghai")
        self.tz_newyork = pytz.timezone("America/New_York")
        self.tz_london = pytz.timezone("Europe/London")
    
    def now(self, timezone: str = "Asia/Shanghai") -> datetime:
        """获取当前时间"""
        tz = pytz.timezone(timezone)
        return datetime.now(tz)
    
    def today(self, timezone: str = "Asia/Shanghai") -> str:
        """获取当前日期字符串 (YYYY-MM-DD)"""
        return self.now(timezone).strftime("%Y-%m-%d")
    
    def is_weekend(self, date_str: str) -> bool:
        """判断是否为周末"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.weekday() >= 5  # 5=Saturday, 6=Sunday
    
    def is_cn_holiday(self, date_str: str) -> bool:
        """判断是否为中国节假日"""
        return date_str in self.CN_HOLIDAYS_2026
    
    def is_us_holiday(self, date_str: str) -> bool:
        """判断是否为美国节假日"""
        return date_str in self.US_HOLIDAYS_2026
    
    def is_trading_day(self, date_str: str, market: Literal["CN", "US", "LME"] = "CN") -> bool:
        """判断是否为交易日"""
        if self.is_weekend(date_str):
            return False
        
        if market == "CN":
            return not self.is_cn_holiday(date_str)
        elif market == "US":
            return not self.is_us_holiday(date_str)
        elif market == "LME":
            # LME周末休市，但部分节假日仍开市
            return not self.is_weekend(date_str)
        
        return True
    
    def get_previous_trading_day(self, date_str: str, market: Literal["CN", "US", "LME"] = "CN") -> str:
        """获取前一个交易日"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        while True:
            date -= timedelta(days=1)
            date_str = date.strftime("%Y-%m-%d")
            if self.is_trading_day(date_str, market):
                return date_str
    
    def validate_data_date(self, data_date: str, report_type: Literal["pre_market", "finance_daily"], 
                          current_time: Optional[datetime] = None) -> dict:
        """
        验证数据日期是否符合报告要求
        
        Returns:
            dict: {"valid": bool, "expected_date": str, "message": str}
        """
        if current_time is None:
            current_time = self.now()
        
        today = current_time.strftime("%Y-%m-%d")
        
        if report_type == "pre_market":
            # 盘前简报应该使用前一交易日数据
            expected = self.get_previous_trading_day(today)
            if data_date == expected:
                return {
                    "valid": True,
                    "expected_date": expected,
                    "message": f"✓ 盘前简报数据日期正确：使用前一交易日 ({expected}) 收盘数据"
                }
            else:
                return {
                    "valid": False,
                    "expected_date": expected,
                    "message": f"✗ 盘前简报数据日期错误：期望 {expected}，实际 {data_date}"
                }
        
        elif report_type == "finance_daily":
            # 财资日报应该使用当日数据（如果是下午发送）
            if current_time.hour >= 15:  # 下午3点后，应该使用当日收盘数据
                expected = today
                if data_date == expected:
                    return {
                        "valid": True,
                        "expected_date": expected,
                        "message": f"✓ 财资日报数据日期正确：使用当日 ({expected}) 收盘数据"
                    }
                else:
                    return {
                        "valid": False,
                        "expected_date": expected,
                        "message": f"✗ 财资日报数据日期错误：期望 {expected}，实际 {data_date}"
                    }
            else:
                # 上午发送，可以使用前一交易日数据
                expected_prev = self.get_previous_trading_day(today)
                if data_date == expected_prev:
                    return {
                        "valid": True,
                        "expected_date": expected_prev,
                        "message": f"✓ 财资日报数据日期正确：使用前一交易日 ({expected_prev}) 数据（上午发送）"
                    }
                else:
                    return {
                        "valid": False,
                        "expected_date": f"{expected_prev} 或 {today}",
                        "message": f"✗ 财资日报数据日期错误：期望 {expected_prev} 或 {today}，实际 {data_date}"
                    }
        
        return {"valid": False, "expected_date": "", "message": "未知的报告类型"}
    
    def check_market_hours(self, market: Literal["USDCNY_MID", "LME_CLOSE", "US_MARKET"]) -> dict:
        """检查市场时间状态"""
        now = self.now("Asia/Shanghai")
        
        if market == "USDCNY_MID":
            # USD/CNY中间价发布时间：9:15
            published = now.hour > 9 or (now.hour == 9 and now.minute >= 15)
            return {
                "published": published,
                "publish_time": "09:15",
                "current_time": now.strftime("%H:%M"),
                "message": "USD/CNY中间价已发布" if published else "USD/CNY中间价尚未发布（9:15发布）"
            }
        
        elif market == "LME_CLOSE":
            # LME收盘时间：北京时间次日凌晨
            # 简单判断：下午4点后视为当日收盘数据可获取
            closed = now.hour >= 16
            return {
                "closed": closed,
                "close_time": "16:00",
                "current_time": now.strftime("%H:%M"),
                "message": "LME已收盘，当日数据可获取" if closed else "LME尚未收盘，使用前一交易日数据"
            }
        
        elif market == "US_MARKET":
            # 美股时间：北京时间21:30-次日04:00
            hour = now.hour
            is_open = hour >= 21 or hour < 4
            return {
                "is_open": is_open,
                "open_time": "21:30",
                "close_time": "04:00",
                "current_time": now.strftime("%H:%M"),
                "message": "美股交易中" if is_open else "美股已收盘"
            }
        
        return {}


# CLI接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Datetime Utils CLI")
    parser.add_argument("--today", action="store_true", help="获取当前日期")
    parser.add_argument("--now", action="store_true", help="获取当前时间")
    parser.add_argument("--is-trading-day", type=str, help="判断是否为交易日 (YYYY-MM-DD)")
    parser.add_argument("--market", type=str, default="CN", choices=["CN", "US", "LME"])
    parser.add_argument("--prev-trading-day", type=str, help="获取前一交易日 (YYYY-MM-DD)")
    parser.add_argument("--validate", type=str, help="验证数据日期 (YYYY-MM-DD)")
    parser.add_argument("--report-type", type=str, choices=["pre_market", "finance_daily"])
    parser.add_argument("--check-market", type=str, choices=["USDCNY_MID", "LME_CLOSE", "US_MARKET"])
    
    args = parser.parse_args()
    
    utils = DateTimeUtils()
    
    if args.today:
        print(utils.today())
    elif args.now:
        print(utils.now().isoformat())
    elif args.is_trading_day:
        result = utils.is_trading_day(args.is_trading_day, args.market)
        print(f"{args.is_trading_day}: {'交易日' if result else '非交易日'}")
    elif args.prev_trading_day:
        print(utils.get_previous_trading_day(args.prev_trading_day, args.market))
    elif args.validate and args.report_type:
        result = utils.validate_data_date(args.validate, args.report_type)
        print(f"验证结果: {result['message']}")
    elif args.check_market:
        result = utils.check_market_hours(args.check_market)
        print(result['message'])
    else:
        # 默认显示当前时间信息
        now = utils.now()
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"当前日期: {utils.today()}")
        print(f"是否交易日(CN): {'是' if utils.is_trading_day(utils.today()) else '否'}")
        print(f"前一交易日: {utils.get_previous_trading_day(utils.today())}")
        print(f"USD/CNY中间价: {utils.check_market_hours('USDCNY_MID')['message']}")
