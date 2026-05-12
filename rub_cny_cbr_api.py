"""
CBR (俄罗斯央行) API 获取 CNY/RUB 日度历史汇率
完全免费，无需注册，无需 API key
覆盖 1995 年至今，日度颗粒度

替代原 Investing.com 爬虫方案
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd


def get_fx_data_cbr(start_date: str, end_date: str) -> pd.DataFrame:
    """
    从俄罗斯央行(CBR)官方API获取 CNY/RUB 日度汇率历史数据。

    参数:
        start_date: 起始日期，'YYYY-MM-DD'
        end_date:   结束日期，'YYYY-MM-DD'

    返回:
        DataFrame，列: Date, Close, Open, High, Low
        注: CBR 官方日度汇率只发布单一收盘价（官方汇率），
            Open/High/Low 以 Close 填充，保持与原函数输出格式兼容。
    """
    # CBR 货币代码: R01375 = Chinese Yuan (注意: R01235 是 USD)
    val_code = 'R01375'

    # CBR 日期格式: DD/MM/YYYY
    def to_cbr_date(d: str) -> str:
        dt = datetime.strptime(d, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')

    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
    params = {
        'date_req1': to_cbr_date(start_date),
        'date_req2': to_cbr_date(end_date),
        'VAL_NM_RQ': val_code,
    }

    try:
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"CBR API 请求失败: {e}")

    # 解析 XML
    root = ET.fromstring(r.text)
    records = root.findall('Record')

    if not records:
        raise RuntimeError(
            f"CBR API 未返回数据。请检查日期范围是否有效，"
            f"或该期间内俄罗斯是否为节假日（CBR 仅发布工作日官方汇率）。"
        )

    data = []
    for rec in records:
        date_str = rec.attrib['Date']          # DD.MM.YYYY
        value_str = rec.find('Value').text     # 俄式逗号小数点，如 "78,2267"

        # 转换为标准浮点数
        rate = float(value_str.replace(',', '.'))

        # CBR 汇率含义: 1 CNY = ? RUB
        # 即 CNY/RUB 汇率，正好就是用户需要的
        data.append({
            'Date': datetime.strptime(date_str, '%d.%m.%Y'),
            'Close': rate,
        })

    df = pd.DataFrame(data)
    df = df.sort_values('Date').reset_index(drop=True)

    # CBR 官方汇率无 OHLC，为兼容原脚本，复制 Close
    df['Open'] = df['Close']
    df['High'] = df['Close']
    df['Low'] = df['Close']

    # 保持列顺序与原 Investing.com 输出一致
    df = df[['Date', 'Close', 'Open', 'High', 'Low']]
    return df


if __name__ == '__main__':
    # 快速测试
    df = get_fx_data_cbr('2024-01-01', '2024-12-31')
    print(f"共 {len(df)} 条记录")
    print(df.head(5))
    print("...")
    print(df.tail(5))
    print(f"\n日期范围: {df['Date'].min().date()} ~ {df['Date'].max().date()}")
    print(f"汇率范围: {df['Close'].min():.4f} ~ {df['Close'].max():.4f}")
