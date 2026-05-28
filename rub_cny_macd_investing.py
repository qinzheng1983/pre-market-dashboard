import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

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

# ==================== 数据源替换：Investing.com 爬取（零注册，不限流）====================
# 原 Wind G2006002（CNY/RUB） → Investing.com 抓取 CNY/RUB 历史数据
# URL: https://cn.investing.com/currencies/cny-rub-historical-data

def get_fx_data_investing(start_date="2023-11-10", end_date="2024-09-21"):
    """
    从 Investing.com 抓取 CNY/RUB 历史日频数据。
    页面结构变化可能导致解析失败，但零注册、不会被限流。
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

    # 新版页面表格 class
    table = soup.find("table", {"class": "freeze-column-w-1"})
    if table is None:
        # 旧版备用
        table = soup.find("table", {"id": "curr_table"})
    if table is None:
        raise RuntimeError("未能定位 Investing.com 数据表格，页面结构可能已变更")

    rows = table.find("tbody").find_all("tr")
    records = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        date_text = cols[0].get_text(strip=True)
        close_text = cols[1].get_text(strip=True).replace(",", "")
        try:
            # 格式示例: "2026年05月08日"
            dt = pd.to_datetime(date_text, format="%Y年%m月%d日")
            records.append({"date": dt, "close": float(close_text)})
        except Exception:
            continue

    df = pd.DataFrame(records).set_index("date").sort_index()
    df = df.loc[start_date:end_date]
    # 日频前向填充
    df = df.asfreq("D")
    df["close"] = df["close"].ffill().bfill()
    return df

start_date = "2023-11-10"
end_date = "2024-09-21"
df = get_fx_data_investing(start_date, end_date)

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
