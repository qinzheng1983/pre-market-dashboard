#!/usr/bin/env python3
"""
CNHRUB 目标汇率概率图 — Investing.com Selenium 修复版
解决 "未能定位数据表格，页面结构可能已变更" 的问题
原因：Investing.com 表格改为 JS 动态加载，requests 抓不到，需用浏览器渲染
"""

import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_fx_data_investing_selenium(start_date: str, end_date: str) -> pd.DataFrame:
    """
    用 Selenium 打开 Chrome，等 JS 渲染完表格后再抓取 CNY/RUB 历史数据。
    
    前提：已安装 selenium + Chrome + chromedriver
        pip install selenium webdriver-manager
    
    参数
    ----
    start_date, end_date : str
        'YYYY-MM-DD'（只用于过滤，Investing.com 页面默认展示最近 ~20 条）
    
    返回
    ----
    DataFrame
        index=Date, columns=['Close','Open','High','Low']
    """
    url = "https://cn.investing.com/currencies/cny-rub-historical-data"
    
    # --- 启动无头 Chrome ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")          # 无界面
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # 如果你 chromedriver 已加入 PATH，可直接:
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # 等待表格加载（最多 20 秒）
        wait = WebDriverWait(driver, 20)
        # Investing.com 历史数据表格现在的 class 可能变了，我们等任意 table 出现
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # 等 2 秒让 JS 填充完数据
        import time
        time.sleep(2)
        
        html = driver.page_source
    finally:
        driver.quit()
    
    # --- BeautifulSoup 解析 ---
    soup = BeautifulSoup(html, "html.parser")
    
    # 尝试多种选择器定位表格（Investing.com 经常改 class）
    table = (
        soup.find("table", class_="freeze-column-w-1")          # 旧 class
        or soup.find("table", {"data-test": "historical-data-table"})  # 可能的新 test id
        or soup.find("table", class_=lambda x: x and "historical" in x.lower())  # 模糊匹配
        or soup.find_all("table")[-1]                           # 兜底：最后一个 table
    )
    
    if not table:
        raise RuntimeError("Selenium 渲染后仍未找到任何表格，页面结构可能已大幅变更")
    
    # 解析行
    rows = table.find_all("tr")
    records = []
    
    for tr in rows[1:]:  # 跳过表头
        tds = tr.find_all("td")
        if len(tds) < 6:
            continue
        
        # Investing.com 中文站的列顺序：日期 | 收盘价 | 开盘价 | 最高价 | 最低价 | 交易量 | 涨跌幅
        # 注意：不同语言版本列序可能不同，以下是中文站实测顺序
        try:
            date_str = tds[0].get_text(strip=True)
            # 中文日期格式：2026年05月08日
            date_obj = pd.to_datetime(date_str, format="%Y年%m月%d日")
            
            records.append({
                "Date":  date_obj,
                "Close": float(tds[1].get_text(strip=True).replace(",", "")),
                "Open":  float(tds[2].get_text(strip=True).replace(",", "")),
                "High":  float(tds[3].get_text(strip=True).replace(",", "")),
                "Low":   float(tds[4].get_text(strip=True).replace(",", "")),
            })
        except Exception:
            continue
    
    if not records:
        raise RuntimeError("表格找到但解析不到数据，请检查列顺序是否与代码假设一致")
    
    df = pd.DataFrame(records).set_index("Date").sort_index()
    
    # 按日期过滤
    start_dt = pd.to_datetime(start_date)
    end_dt   = pd.to_datetime(end_date)
    df = df.loc[start_dt:end_dt]
    
    return df


# ================= 以下为示例 =================

if __name__ == "__main__":
    end_date   = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=365*2)).strftime("%Y-%m-%d")
    
    print(f"拉取 CNY/RUB 数据: {start_date} ~ {end_date}")
    df = get_fx_data_investing_selenium(start_date, end_date)
    
    print(f"共 {len(df)} 条记录")
    print(df.tail(10))
    print("\n列名:", list(df.columns))
