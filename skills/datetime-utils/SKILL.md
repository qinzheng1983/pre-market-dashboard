# Datetime Utils - 日期时间工具

## 概述

专门用于金融数据报告的日期时间管理工具，确保数据时效性和日期准确性。

## 功能

### 1. 获取准确日期时间
- 带时区验证的当前时间
- ISO 8601 格式输出
- 支持上海/纽约/伦敦时区

### 2. 交易日判断
- 判断是否为工作日（中美）
- 中国节假日判断
- 美国节假日判断

### 3. 数据日期校验
- 验证数据日期是否符合报告要求
- 防止日期错误（如将T-1数据误认为T日）

### 4. 市场时间检查
- USD/CNY中间价发布时间（9:15）
- LME收盘时间
- 美股开盘/收盘时间

## 使用方法

```python
from datetime_utils import DateTimeUtils

utils = DateTimeUtils()

# 获取当前时间（上海时区）
current = utils.now("Asia/Shanghai")

# 判断是否为交易日
is_trading_day = utils.is_trading_day("2026-04-03", market="CN")

# 验证数据日期
utils.validate_data_date(data_date="2026-04-02", report_type="pre_market", current_time=current)
```

## 安装

```bash
pip install -r requirements.txt
```
