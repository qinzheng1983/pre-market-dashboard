#!/usr/bin/env python3
"""
CNHRUB 目标汇率概率图 — Alpha Vantage 数据源替换版
替换原来的 get_fx_data_investing，保持接口完全一致
"""

import requests
import pandas as pd
from datetime import datetime, timedelta


def get_fx_data_alphavantage(start_date: str, end_date: str, api_key: str) -> pd.DataFrame:
    """
    从 Alpha Vantage FX_DAILY 获取 CNY/RUB 历史数据。
    
    参数
    ----
    start_date, end_date : str
        'YYYY-MM-DD'
    api_key : str
        从 https://www.alphavantage.co/support/#api-key 免费注册的 API key
    
    返回
    ----
    DataFrame
        与原来 Investing.com 版格式一致：
        index=Date, columns=['Close','Open','High','Low']
    """
    url = (
        "https://www.alphavantage.co/query"
        f"?function=FX_DAILY"
        f"&from_symbol=CNY"
        f"&to_symbol=RUB"
        f"&outputsize=full"
        f"&apikey={api_key}"
    )
    
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    
    if "Information" in data:
        raise RuntimeError(f"Alpha Vantage 限制: {data['Information']}")
    if "Error Message" in data:
        raise RuntimeError(f"Alpha Vantage 错误: {data['Error Message']}")
    
    ts = data.get("Time Series FX (Daily)", {})
    if not ts:
        raise RuntimeError("Alpha Vantage 返回数据为空，请检查 api_key 和货币对")
    
    # 构造 DataFrame
    records = []
    for date_str, vals in ts.items():
        records.append({
            "Date": pd.to_datetime(date_str),
            "Close": float(vals["4. close"]),
            "Open":  float(vals["1. open"]),
            "High":  float(vals["2. high"]),
            "Low":   float(vals["3. low"]),
        })
    
    df = pd.DataFrame(records).set_index("Date").sort_index()
    
    # 按用户指定的日期范围过滤
    start_dt = pd.to_datetime(start_date)
    end_dt   = pd.to_datetime(end_date)
    df = df.loc[start_dt:end_dt]
    
    return df


# ================= 以下为示例：如何替换你原文件中的调用 =================

if __name__ == "__main__":
    # 1. 把这里换成你申请的 Alpha Vantage API key
    API_KEY = "YOUR_API_KEY_HERE"
    
    # 2. 日期范围（保持和你原来一样）
    end_date   = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=365*5)).strftime("%Y-%m-%d")
    
    print(f"拉取 CNY/RUB 数据: {start_date} ~ {end_date}")
    df = get_fx_data_alphavantage(start_date, end_date, API_KEY)
    
    print(f"共 {len(df)} 条记录")
    print(df.tail(10))
    print("\n列名:", list(df.columns))
    print("\n最新收盘价:", df["Close"].iloc[-1])
