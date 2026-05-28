"""
多币种统一汇率数据获取脚本 — 最终版
======================================
已验证可用的数据源组合：
  • FRED (美国联邦储备) — USD/CNY, USD/EUR, USD/JPY 等 20+ 主流货币对
  • CBR (俄罗斯央行)   — USD/RUB, CNY/RUB, EUR/RUB
  • 交叉汇率计算       — CNY/IDR 等 (通过 USD/XX ÷ USD/YY)

依赖: pip install requests pandas

用法:
    from fx_unified_v2 import get_fx_data
    df = get_fx_data('USD/CNY', '2020-01-01', '2024-12-31')
    df = get_fx_data('CNY/RUB', '2020-01-01', '2024-12-31')
    df = get_fx_data('USD/RUB', '2020-01-01', '2024-12-31')
    df = get_fx_data('CNY/IDR', '2020-01-01', '2024-12-31')  # 交叉计算
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from io import StringIO

# ──────────────────────────────────────────────────────────────
# FRED 数据源（免费，无需 API key，CSV 直链下载）
# ──────────────────────────────────────────────────────────────

FRED_MAP = {
    'USD/CNY': 'DEXCHUS', 'USD/EUR': 'DEXUSEU', 'USD/JPY': 'DEXJPUS',
    'USD/GBP': 'DEXUSUK', 'USD/CAD': 'DEXCAUS', 'USD/AUD': 'DEXUSAL',
    'USD/NZD': 'DEXUSNZ', 'USD/MXN': 'DEXMXUS', 'USD/BRL': 'DEXBOUS',
    'USD/KRW': 'DEXKOUS', 'USD/INR': 'DEXINUS', 'USD/CHF': 'DEXSZUS',
    'USD/SEK': 'DEXSDUS', 'USD/NOK': 'DEXNOUS', 'USD/DKK': 'DEXDNUS',
    'USD/SGD': 'DEXSIUS', 'USD/HKD': 'DEXHKUS', 'USD/TWD': 'DEXTAUS',
    'USD/THB': 'DEXTMUS', 'USD/MYR': 'DEXMAUS', 'USD/ZAR': 'DEXSFUS',
}

def get_fx_data_fred(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    series_id = FRED_MAP[pair]
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
    params = {'id': series_id, 'cosd': start_date, 'coed': end_date}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    df.columns = ['Date', 'Close']
    df = df.dropna(subset=['Close'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close'] = df['Close'].astype(float)
    df = df.sort_values('Date').reset_index(drop=True)
    df['Open'] = df['Close']
    df['High'] = df['Close']
    df['Low'] = df['Close']
    return df[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# CBR 俄罗斯央行数据源（免费，无需 API key）
# ──────────────────────────────────────────────────────────────

CBR_MAP = {
    'USD/RUB': 'R01235', 'CNY/RUB': 'R01375', 'EUR/RUB': 'R01239',
    'GBP/RUB': 'R01035', 'JPY/RUB': 'R01820', 'CHF/RUB': 'R01775',
}

def get_fx_data_cbr(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    val_code = CBR_MAP[pair]
    def fmt(d):
        return datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m/%Y')
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
    params = {'date_req1': fmt(start_date), 'date_req2': fmt(end_date), 'VAL_NM_RQ': val_code}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    records = root.findall('Record')
    if not records:
        raise RuntimeError(f"CBR 未返回 {pair} 数据")
    rows = []
    for rec in records:
        rate = float(rec.find('Value').text.replace(',', '.'))
        if pair == 'JPY/RUB':
            rate /= 100.0
        rows.append({'Date': datetime.strptime(rec.attrib['Date'], '%d.%m.%Y'), 'Close': rate})
    df = pd.DataFrame(rows).sort_values('Date').reset_index(drop=True)
    df['Open'] = df['Close']
    df['High'] = df['Close']
    df['Low'] = df['Close']
    return df[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# 交叉汇率计算
# ──────────────────────────────────────────────────────────────

def get_fx_data_cross(base: str, quote: str, start_date: str, end_date: str) -> pd.DataFrame:
    df_base = get_fx_data(f'USD/{base}', start_date, end_date)
    df_quote = get_fx_data(f'USD/{quote}', start_date, end_date)
    merged = pd.merge(df_base[['Date', 'Close']], df_quote[['Date', 'Close']],
                      on='Date', suffixes=('_base', '_quote'))
    merged['Close'] = merged['Close_quote'] / merged['Close_base']
    merged['Open'] = merged['Close']
    merged['High'] = merged['Close']
    merged['Low'] = merged['Close']
    return merged[['Date', 'Close', 'Open', 'High', 'Low']]


# ──────────────────────────────────────────────────────────────
# 统一入口
# ──────────────────────────────────────────────────────────────

def get_fx_data(pair: str, start_date: str, end_date: str) -> pd.DataFrame:
    pair = pair.upper().strip()
    if pair in FRED_MAP:
        return get_fx_data_fred(pair, start_date, end_date)
    if pair in CBR_MAP:
        return get_fx_data_cbr(pair, start_date, end_date)
    parts = pair.split('/')
    if len(parts) == 2 and parts[0] != 'USD' and parts[1] != 'USD':
        try:
            return get_fx_data_cross(parts[0], parts[1], start_date, end_date)
        except Exception:
            pass
    raise ValueError(
        f"暂无免费数据源支持 {pair}。\n"
        f"FRED 支持: {list(FRED_MAP.keys())}\n"
        f"CBR 支持: {list(CBR_MAP.keys())}\n"
        f"交叉汇率: BASE/QUOTE (需两者都有 USD/XX 数据)\n"
        f"如需其他货币对，建议注册 Alpha Vantage 免费 key。"
    )


if __name__ == '__main__':
    for p, s, e in [('USD/CNY', '2024-01-01', '2024-01-10'),
                    ('CNY/RUB', '2024-01-01', '2024-01-10'),
                    ('USD/RUB', '2024-01-01', '2024-01-10')]:
        try:
            df = get_fx_data(p, s, e)
            print(f"✅ {p}: {len(df)} 条, 最新 {df['Close'].iloc[-1]:.4f}")
        except Exception as ex:
            print(f"❌ {p}: {ex}")
