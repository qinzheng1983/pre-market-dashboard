import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import time
import random

# 兼容多平台中文字体
import platform
system = platform.system()
if system == "Windows":
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
elif system == "Darwin":
    plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC"]
else:
    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

# ==================== 数据源替换：yfinance（带重试+延时）====================
# 原 Wind G2006002（CNY/RUB） → yfinance CNYRUB=X
ticker = "CNYRUB=X"
start_date = "2023-11-10"
end_date = "2024-09-21"

def download_with_retry(ticker, start, end, max_retries=5, base_delay=3):
    """带指数退避重试的 yfinance 下载"""
    end_dt = pd.to_datetime(end) + pd.Timedelta(days=1)
    for attempt in range(max_retries):
        # 随机延时 2-6 秒，降低触发限流概率
        time.sleep(random.uniform(2, 6))
        try:
            hist = yf.download(
                ticker,
                start=start,
                end=end_dt.strftime("%Y-%m-%d"),
                progress=False,
                # 降低请求频率：不用并行，单线程拉
                threads=False,
            )
            if not hist.empty:
                return hist
            print(f"第 {attempt+1} 次尝试返回空数据，重试中...")
        except Exception as e:
            print(f"第 {attempt+1} 次尝试失败: {e}")
        # 指数退避：3s, 6s, 12s, 24s, 48s
        time.sleep(base_delay * (2 ** attempt))
    raise RuntimeError(f"yfinance 连续 {max_retries} 次请求失败，ticker={ticker}")

hist = download_with_retry(ticker, start_date, end_date)

# 取收盘价，与原 Wind close 对齐
df = hist[["Close"]].copy()
df.index = pd.to_datetime(df.index.date)
df.columns = ["close"]

# 日频前向填充（等效 Wind Fill=Previous）
df = df.asfreq("D")
df["close"] = df["close"].ffill().bfill()

# ==================== 以下逻辑与原代码完全一致 ====================

# 目标值因变量为人民币/卢布汇率 → 取倒数得到 RUB/CNY
df = df.rdiv(1)

# 线性插值
for f in df:
    df[f] = df[f].interpolate(method="linear", limit=10000, limit_direction="backward")

df.columns = ["y"]

# 计算汇率数据的 MACD
close = df["y"].values.T
data = pd.DataFrame(index=df.index, columns=["price", "diff", "dea", "my_macd", "limit", "divergence"])
data["diff"], data["dea"], data["my_macd"] = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
data["price"] = df["y"]

# 判断顶背离和底背离时长（30天），用期间的极值
t = 30
# 金叉、死叉比较时长，用期间的均值
T = 13

# Limit，判断金叉和死叉场景
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

# Divergence，判断顶底背离场景
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

# 考虑去重。前面5个价格中如果有重复，本期值再回到0
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
print("年化收益率为：{:.2%}".format(252 * PL / data["price"].values[-1] / len(data) / max(count_plus, count_minus)))

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
