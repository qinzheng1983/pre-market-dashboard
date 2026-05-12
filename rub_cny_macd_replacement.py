"""
MACD交易策略 — 数据源替换方案（三选一）
原Wind G2006002（CNY/RUB） → 替换为以下任一方案

方案说明：
- 方案① Alpha Vantage：最推荐，官方API，数据可靠
- 方案② Yahoo Finance(yfinance)：次选，pip一行安装
- 方案③ Investing.com爬取：零注册，但页面结构变化会崩

原代码逻辑保留：
- y = RUB/CNY（经 rdiv(1) 取倒数）
- 金叉买入卢布 / 死叉卖出卢布
- MACD参数 fast=12 slow=26 signal=9 不变
"""

import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt

# ========== 方案①：Alpha Vantage FX_DAILY（推荐）==========
# 注册免费API Key: https://www.alphavantage.co/support/#api-key
# 免费版限制：每天500次请求，每分钟最多5次
import requests
import time

ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"  # ← 换成你的key

def get_fx_data_alphavantage(from_symbol="CNY", to_symbol="RUB",
                              start_date="2023-11-10", end_date="2024-09-21"):
    """
    从Alpha Vantage获取外汇日频数据
    from=CNY, to=RUB 返回 CNY/RUB（1人民币=多少卢布）
    与原Wind G2006002方向一致，保留 rdiv(1) 即可得到 RUB/CNY
    """
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=FX_DAILY"
        f"&from_symbol={from_symbol}"
        f"&to_symbol={to_symbol}"
        f"&outputsize=full"
        f"&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    r = requests.get(url, timeout=30)
    data = r.json()

    # 检查是否触发频率限制
    if "Note" in data:
        raise RuntimeError(f"Alpha Vantage频率限制: {data['Note']}")
    if "Error Message" in data:
        raise RuntimeError(f"Alpha Vantage错误: {data['Error Message']}")

    ts = data.get("Time Series FX (Daily)", {})
    if not ts:
        raise RuntimeError("未获取到数据，请检查API Key和货币对代码")

    records = []
    for date_str, values in ts.items():
        records.append({
            "date": pd.to_datetime(date_str),
            "close": float(values["4. close"])
        })

    df = pd.DataFrame(records).set_index("date").sort_index()
    # 按日期裁剪
    df = df.loc[start_date:end_date]
    # 日频填充（Fill=Previous）
    df = df.asfreq("D")
    df["close"] = df["close"].ffill().bfill()
    return df


# ========== 方案②：Yahoo Finance (yfinance) ==========
# pip install yfinance
import yfinance as yf

def get_fx_data_yfinance(ticker="CNYRUB=X",
                         start_date="2023-11-10", end_date="2024-09-21"):
    """
    从Yahoo Finance获取外汇历史数据
    CNYRUB=X → CNY/RUB（1人民币=多少卢布）
    与原Wind方向一致，保留 rdiv(1)
    备选：RUBCNY=X 可直接取到 RUB/CNY，无需倒数
    """
    tk = yf.Ticker(ticker)
    # end_date 在 yfinance 是开区间，往后延一天确保包含
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1)
    hist = tk.history(start=start_date, end=end_dt.strftime("%Y-%m-%d"))

    if hist.empty:
        raise RuntimeError(f"Yahoo Finance返回空数据，ticker={ticker}")

    df = hist[["Close"]].rename(columns={"Close": "close"})
    df.index = pd.to_datetime(df.index.date)  # 去掉时区
    # 日频前向填充
    df = df.asfreq("D")
    df["close"] = df["close"].ffill().bfill()
    return df


# ========== 方案③：Investing.com 网页爬取（零注册）==========
import requests
from bs4 import BeautifulSoup

def get_fx_data_investing(start_date="2023-11-10", end_date="2024-09-21"):
    """
    从 Investing.com 抓取 CNY/RUB 历史数据
    URL: https://cn.investing.com/currencies/cny-rub-historical-data
    零注册，但页面结构变化会导致解析失败
    """
    url = "https://cn.investing.com/currencies/cny-rub-historical-data"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"class": "freeze-column-w-1"})
    if table is None:
        # 备用：尝试通用表格
        table = soup.find("table", {"id": "curr_table"})
    if table is None:
        raise RuntimeError("未能定位Investing.com数据表格，页面结构可能已变更")

    rows = table.find("tbody").find_all("tr")
    records = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        date_text = cols[0].get_text(strip=True)
        close_text = cols[1].get_text(strip=True).replace(",", "")
        try:
            dt = pd.to_datetime(date_text, format="%Y年%m月%d日")
            records.append({"date": dt, "close": float(close_text)})
        except Exception:
            continue

    df = pd.DataFrame(records).set_index("date").sort_index()
    df = df.loc[start_date:end_date]
    df = df.asfreq("D")
    df["close"] = df["close"].ffill().bfill()
    return df


# ========== 主程序：选一个方案，其余注释掉 ==========

START_DATE = "2023-11-10"
END_DATE   = "2024-09-21"

# 三选一：取消注释你要用的方案
# df = get_fx_data_alphavantage("CNY", "RUB", START_DATE, END_DATE)
df = get_fx_data_yfinance("CNYRUB=X", START_DATE, END_DATE)
# df = get_fx_data_investing(START_DATE, END_DATE)

# ===== 以下逻辑与原代码完全一致，无需改动 =====

# 兼容多平台中文字体（Linux/macOS/Windows）
import platform
system = platform.system()
if system == "Windows":
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
elif system == "Darwin":
    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC"]
else:
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

# 目标值因变量为人民币/卢布汇率 → 取倒数得到 RUB/CNY
df = df.rdiv(1)

# 线性插值（与原代码一致）
for f in df:
    df[f] = df[f].interpolate(method="linear", limit=10000, limit_direction="backward")

df.columns = ["y"]

# 计算 MACD
close = df["y"].values.T
data = pd.DataFrame(index=df.index, columns=["price", "diff", "dea", "my_macd", "limit", "divergence"])
data["diff"], data["dea"], data["my_macd"] = talib.MACD(
    close, fastperiod=12, slowperiod=26, signalperiod=9
)
data["price"] = df["y"]

# 顶底背离和金叉死叉参数
t = 30   # 顶底背离比较时长
T = 13   # 金叉死叉比较时长

# Limit：判断金叉和死叉场景
for i in range(len(data)):
    if data["my_macd"][i] > data.iloc[i - T:i]["my_macd"].mean():
        if data["price"][i] > data.iloc[i - t:i]["price"].mean() and data["diff"][i] < data.iloc[i - t:i]["diff"].mean():
            data.loc[data.index[i], "limit"] = 0
        else:
            data.loc[data.index[i], "limit"] = 1
    elif data["my_macd"][i] < data.iloc[i - T:i]["my_macd"].mean():
        if data["price"][i] < data.iloc[i - t:i]["price"].mean() and data["diff"][i] > data.iloc[i - t:i]["diff"].mean():
            data.loc[data.index[i], "limit"] = 0
        else:
            data.loc[data.index[i], "limit"] = -1
    else:
        data.loc[data.index[i], "limit"] = 0

# Divergence：判断顶底背离场景
for i in range(len(data)):
    if data["price"][i] < data.iloc[i - t:i]["price"].mean() and data["diff"][i] > data.iloc[i - t:i]["diff"].mean():
        if data["diff"][i] < data["dea"][i]:
            data.loc[data.index[i], "divergence"] = 0
        else:
            data.loc[data.index[i], "divergence"] = 1
    elif data["price"][i] > data.iloc[i - t:i]["price"].mean() and data["diff"][i] < data.iloc[i - t:i]["diff"].mean():
        if data["diff"][i] > data["dea"][i]:
            data.loc[data.index[i], "divergence"] = 0
        else:
            data.loc[data.index[i], "divergence"] = -1
    else:
        data.loc[data.index[i], "divergence"] = 0

# 去重：前面5个价格中如果有重复，本期值再回到0
droprepeat = 5
for i in range(len(data)):
    if 1 in data.iloc[i - droprepeat:i]["limit"].values:
        data.loc[data.index[i], "limit"] = 0
    elif -1 in data.iloc[i - droprepeat:i]["limit"].values:
        data.loc[data.index[i], "limit"] = 0
for i in range(len(data)):
    if 1 in data.iloc[i - droprepeat:i]["divergence"].values:
        data.loc[data.index[i], "divergence"] = 0
    elif -1 in data.iloc[i - droprepeat:i]["divergence"].values:
        data.loc[data.index[i], "divergence"] = 0

x1 = data[data["limit"] == 1]
x2 = data[data["limit"] == -1]
y1 = data[data["divergence"] == -1]
y2 = data[data["divergence"] == 1]

# 量化投资收益率
PL = 0
count_plus = 0
count_minus = 0
for i in range(len(data)):
    if data["divergence"][i] == 1 or data["limit"][i] == 1:
        PL -= data["price"][i]
        count_plus += 1
    elif data["divergence"][i] == -1 or data["limit"][i] == -1:
        PL += data["price"][i]
        count_minus += 1

PL = PL - (count_minus - count_plus) * data["price"].values[-1]

price_buy = data.query("(divergence == 1) | (limit == 1)")["price"].mean()
price_sell = data.query("(divergence == -1) | (limit == -1)")["price"].mean()

print("量化模拟期间，观望，暂不卖出时机:{:.2f}次，平均成本:{:.4f}".format(count_plus, price_buy))
print("量化模拟期间，止损/止盈，卖出时机:{:.2f}次，平均成本:{:.4f}".format(count_minus, price_sell))
print("量化模拟期间，获得的汇兑损益为：{:.2f}人民币".format(PL))
print("年化收益率为：{:.2%}".format(
    252 * PL / data["price"].values[-1] / len(data) / max(count_plus, count_minus)
))

# 画图
plt.figure(figsize=(14, 10))
plt.title("MACD交易策略", fontsize=14, color="k")
plt.subplot(2, 1, 1)
plt.plot(df.index, df["y"], "b-")
plt.scatter(x2.index, x2["price"], s=35, c="r", marker="o", label="死叉止损点，卖出卢布，换汇人民币")
plt.scatter(y1.index, y1["price"], s=35, c="k", marker="o", label="顶背离止盈点，卖出卢布，换汇人民币")
plt.scatter(x1.index, x1["price"], s=35, c="gold", marker="x", label="金叉买入点，持有卢布，暂不换人民币")
plt.scatter(y2.index, y2["price"], s=35, c="m", marker="x", label="底背离买入点，持有卢布，暂不换人民币")
plt.ylabel("RUB/CNY Price", fontsize=14)
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(data["diff"], "r-", label="DIFF")
plt.plot(data["dea"], "b-", label="DEA")
plt.bar(data.index, data["my_macd"], color="lime", width=5, label="MACD-Bar")
plt.ylabel("MACD Indicator", fontsize=14)
plt.xlabel("Date", fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()
