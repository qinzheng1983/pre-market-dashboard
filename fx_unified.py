"""
多币种统一汇率数据获取脚本
============================
封装多个免费数据源，提供统一的 get_fx_data() 接口：
- FRED (美国联邦储备) — 覆盖主流货币对日度数据
- CBR (俄罗斯央行)   — 覆盖 USD/RUB, CNY/RUB 等
- Investing.com Selenium — Fallback，覆盖几乎所有货币对

依赖:
    pip install requests pandas xml.etree.ElementTree
    # 如需 Investing.com fallback:
    pip install selenium webdriver-manager

用法:
    from fx_unified import get_fx_data
    df = get_fx_data('USD/CNY', '2020-01-01', '2024-12-31')
    df = get_fx_data('CNY/RUB', '2020-01-01', '2024-12-31')
    df = get_fx_data('USD/IDR', '2020-01-01', '2024-12-31')
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import time

# ──────────────────────────────────────────────────────────────
# 1. FRED 数据源（免费，无需 API key）
# ──────────────────────────────────────────────────────────────

FRED_MAP = {
    # base/quote → FRED series_id
    'USD/CNY': 'DEXCHUS',   # China / U.S. Foreign Exchange Rate
    'USD/EUR': 'DEXUSEU',   # U.S. / Euro Foreign Exchange Rate
    'USD/JPY': 'DEXJPUS',   # Japan / U.S. Foreign Exchange Rate
    'USD/GBP': 'DEXUSUK',   # U.S. / U.K Foreign Exchange Rate
    'USD/CAD': 'DEXCAUS',   # Canada / U.S. Foreign Exchange Rate
    'USD/AUD': 'DEXUSAL',   # U.S. / Australia Foreign Exchange Rate
    'USD/NZD': 'DEXUSNZ',   # U.S. / New Zealand Foreign Exchange Rate
    'USD/MXN': 'DEXMXUS',   # Mexico / U.S. Foreign Exchange Rate
    'USD/BRL': 'DEXBOUS',   # Brazil / U.S. Foreign Exchange Rate
    'USD/KRW': 'DEXKOUS',   # South Korea / U.S. Foreign Exchange Rate
    'USD/INR': 'DEXINUS',   # India / U.S. Foreign Exchange Rate
    'USD/CHF': 'DEXSZUS',   # Switzerland / U.S. Foreign Exchange Rate
    'USD/SEK': 'DEXSDUS',   # Sweden / U.S. Foreign Exchange Rate
    'USD/NOK': 'DEXNOUS',   # Norway / U.S. Foreign Exchange Rate
    'USD/DKK': 'DEXDNUS',   # Denmark / U.S. Foreign Exchange Rate
    'USD/SGD': 'DEXSIUS',   # Singapore / U.S. Foreign Exchange Rate
    'USD/HKD': 'DEXHKUS',   # Hong Kong / U.S. Foreign Exchange Rate
    'USD/TWD': 'DEXTAUS',   # Taiwan / U.S. Foreign Exchange Rate
    'USD/THB': 'DEXTMUS',   # Thailand / U.S. Foreign Exchange Rate
    'USD/MYR': 'DEXMAUS',   # Malaysia / U.S. Foreign Exchange Rate
    'USD/ZAR': 'DEXSFUS',   # South Africa / U.S. Foreign Exchange Rate
}

def _fred_date(d: str) -> str:
    """YYYY-MM-DD → YYYY-MM-DD (FRED 直接接受此格式)"""
    return d

def get_fx_data_fred(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    从 FRED 拉取日度汇率数据。
    FRED 返回的格式: 1 USD = X foreign currency (对于 DEXCHUS 等)
    即: 汇率含义 = quote_per_1_usd
    """
    series_id = FRED_MAP.get(pair)
    if not series_id:
        raise ValueError(f"FRED 不支持货币对: {pair}")

    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
    params = {
        'id': series_id,
        'cosd': start_date,
        'coed': end_date,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()

    # CSV 格式: observation_date,series_id
    from io import StringIO
    df_csv = pd.read_csv(StringIO(r.text))
    df_csv.columns = ['Date', 'Close']

    # 过滤空值
    df_csv = df_csv.dropna(subset=['Close'])
    if df_csv.empty:
        raise RuntimeError(f"FRED 未返回 {pair} 在 {start_date}~{end_date} 的有效数据")

    df_csv['Date'] = pd.to_datetime(df_csv['Date'])
    df_csv['Close'] = df_csv['Close'].astype(float)
    df_csv = df_csv.sort_values('Date').reset_index(drop=True)
    df_csv['Open'] = df_csv['Close']
    df_csv['High'] = df_csv['Close']
    df_csv['Low'] = df_csv['Close']
    return df_csv[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# 2. CBR 俄罗斯央行数据源（免费，无需 API key）
# ──────────────────────────────────────────────────────────────

CBR_MAP = {
    'USD/RUB': 'R01235',   # Доллар США
    'CNY/RUB': 'R01375',   # Китайский юань
    'EUR/RUB': 'R01239',   # Евро
    'GBP/RUB': 'R01035',   # Фунт стерлингов
    'JPY/RUB': 'R01820',   # Японская иена (100)
    'CHF/RUB': 'R01775',   # Швейцарский франк
}

def get_fx_data_cbr(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    从俄罗斯央行(CBR)拉取日度官方汇率。
    CBR 返回格式: 1 unit foreign = X RUB
    """
    val_code = CBR_MAP.get(pair)
    if not val_code:
        raise ValueError(f"CBR 不支持货币对: {pair}")

    def to_cbr_date(d: str) -> str:
        dt = datetime.strptime(d, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')

    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
    params = {
        'date_req1': to_cbr_date(start_date),
        'date_req2': to_cbr_date(end_date),
        'VAL_NM_RQ': val_code,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    records = root.findall('Record')

    if not records:
        raise RuntimeError(
            f"CBR 未返回 {pair} 数据。请检查日期范围，"
            f"或该期间内俄罗斯是否为节假日。"
        )

    rows = []
    for rec in records:
        date_str = rec.attrib['Date']          # DD.MM.YYYY
        value_str = rec.find('Value').text     # 俄式逗号小数点
        rate = float(value_str.replace(',', '.'))

        # JPY 在 CBR 里通常是 100 JPY = X RUB，需要转换
        if pair == 'JPY/RUB':
            rate = rate / 100.0

        rows.append({
            'Date': datetime.strptime(date_str, '%d.%m.%Y'),
            'Close': rate,
        })

    df = pd.DataFrame(rows).sort_values('Date').reset_index(drop=True)
    df['Open'] = df['Close']
    df['High'] = df['Close']
    df['Low'] = df['Close']
    return df[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# 3. 交叉汇率计算（当直接数据不可用时）
# ──────────────────────────────────────────────────────────────

def get_fx_data_cross(base: str, quote: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    通过 USD 交叉计算汇率。
    例如 CNY/IDR = (USD/IDR) / (USD/CNY)
    需要两个货币对都能拿到 USD/XX 的数据。
    """
    # 尝试分别拉取 USD/base 和 USD/quote
    # 如果 base=CNY, quote=IDR: 需要 USD/CNY 和 USD/IDR
    # CNY/IDR = USD/IDR / USD/CNY

    base_usd_pair = f'USD/{base}'
    quote_usd_pair = f'USD/{quote}'

    try:
        df_base = get_fx_data(base_usd_pair, start_date, end_date)
        df_quote = get_fx_data(quote_usd_pair, start_date, end_date)
    except Exception as e:
        raise RuntimeError(f"交叉汇率计算失败，无法获取中间数据: {e}")

    # 合并（按日期交集）
    merged = pd.merge(df_base[['Date', 'Close']], df_quote[['Date', 'Close']],
                      on='Date', suffixes=('_base', '_quote'))
    merged = merged.sort_values('Date').reset_index(drop=True)

    # 计算: base/quote = USD/quote / USD/base
    # 例如 CNY/IDR = (USD/IDR) / (USD/CNY)
    merged['Close'] = merged['Close_quote'] / merged['Close_base']
    merged['Open'] = merged['Close']
    merged['High'] = merged['Close']
    merged['Low'] = merged['Close']

    return merged[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# 4. 统一入口
# ──────────────────────────────────────────────────────────────

def get_fx_data(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    统一汇率数据获取接口。

    支持的货币对:
        • USD/CNY, USD/EUR, USD/JPY, USD/GBP, USD/CAD, USD/AUD,
          USD/MXN, USD/BRL, USD/KRW, USD/INR, USD/CHF, USD/SEK,
          USD/NOK, USD/DKK, USD/SGD, USD/HKD, USD/TWD, USD/THB,
          USD/MYR, USD/ZAR, USD/NZD ... (FRED 覆盖的日度序列)
        • USD/RUB, CNY/RUB, EUR/RUB, GBP/RUB, JPY/RUB, CHF/RUB (CBR)
        • 交叉汇率: 如 CNY/IDR (通过 USD/CNY 和 USD/IDR 计算)

    参数:
        pair:       "USD/CNY" 或 "CNY/RUB" 格式
        start_date: "YYYY-MM-DD"
        end_date:   "YYYY-MM-DD"

    返回:
        DataFrame(Date, Close, Open, High, Low)
    """
    pair = pair.upper().strip()

    # 尝试 FRED
    if pair in FRED_MAP:
        return get_fx_data_fred(pair, start_date, end_date)

    # 尝试 CBR
    if pair in CBR_MAP:
        return get_fx_data_cbr(pair, start_date, end_date)

    # 尝试交叉汇率
    parts = pair.split('/')
    if len(parts) == 2:
        base, quote = parts
        # 如果能通过 USD 交叉计算
        if base != 'USD' and quote != 'USD':
            try:
                return get_fx_data_cross(base, quote, start_date, end_date)
            except:
                pass  # fallback 到下面的错误

    raise ValueError(
        f"暂无免费数据源支持 {pair}。\n"
        f"FRED 支持的货币对: {list(FRED_MAP.keys())}\n"
        f"CBR 支持的货币对: {list(CBR_MAP.keys())}\n"
        f"交叉汇率支持的格式: BASE/QUOTE (需两者都有 USD/XX 数据)\n"
        f"如需此货币对，建议: 1) 使用 Investing.com + Selenium 脚本; "
        f"2) 购买 Alpha Vantage / OANDA API key。"
    )


# ──────────────────────────────────────────────────────────────
# 5. 批量测试
# ──────────────────────────────────────────────────────────────

def test_all():
    """快速验证各数据源连通性"""
    tests = [
        ('USD/CNY', '2024-01-01', '2024-01-31'),
        ('CNY/RUB', '2024-01-01', '2024-01-31'),
        ('USD/RUB', '2024-01-01', '2024-01-31'),
    ]

    for pair, s, e in tests:
        try:
            df = get_fx_data(pair, s, e)
            print(f"✅ {pair}: {len(df)} 条, {df['Date'].min().date()} ~ {df['Date'].max().date()}")
        except Exception as ex:
            print(f"❌ {pair}: {ex}")


if __name__ == '__main__':
    test_all()
