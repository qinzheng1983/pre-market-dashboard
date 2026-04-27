---
name: office-automation
description: Office Automation - 办公自动化工具，支持 Excel、Word、PDF 等常用办公文档处理
metadata:
  version: 1.0.0
  author: openclaw
  requires:
    - pandas>=2.0
    - openpyxl>=3.0
    - python-docx>=1.0
    - fpdf2>=2.0
---

# Office Automation - 办公自动化工具

## 概述

支持 Excel、Word、PDF 等常用办公文档处理的自动化工具。

## 功能特点

- 📊 **Excel 处理** - 读写、转换、合并 Excel 文件
- 📝 **Word 处理** - 创建和读取 Word 文档
- 📄 **PDF 生成** - 创建 PDF 文档
- 🔄 **格式转换** - Excel <-> CSV 互转

## 安装

```bash
# 安装依赖
pip install pandas openpyxl python-docx fpdf2 --break-system-packages

# 验证安装
python3 skills/office-automation/scripts/office_auto.py check-deps
```

## 使用方法

### Excel 操作

```bash
# 创建示例 Excel
python3 office_auto.py excel-create sample.xlsx

# 读取 Excel
python3 office_auto.py excel-read data.xlsx

# Excel 转 CSV
python3 office_auto.py excel-to-csv data.xlsx data.csv

# CSV 转 Excel
python3 office_auto.py csv-to-excel data.csv data.xlsx

# 合并多个 Excel
python3 office_auto.py excel-merge output.xlsx file1.xlsx file2.xlsx
```

### Word 操作

```bash
# 创建 Word 文档
python3 office_auto.py word-create doc.docx "标题" "文档内容"

# 读取 Word 文档
python3 office_auto.py word-read doc.docx
```

### PDF 操作

```bash
# 创建 PDF 文档
python3 office_auto.py pdf-create doc.pdf "标题" "文档内容"
```

## Python API

### Excel 处理

```python
from office_auto import ExcelHandler

excel = ExcelHandler()

# 读取 Excel
data = excel.read_excel('data.xlsx')
print(data['columns'])
print(data['data'])

# 创建 Excel
excel.create_sample('sample.xlsx')

# Excel 转 CSV
excel.excel_to_csv('data.xlsx', 'data.csv')

# CSV 转 Excel
excel.csv_to_excel('data.csv', 'data.xlsx')

# 合并 Excel
excel.merge_excel(['file1.xlsx', 'file2.xlsx'], 'merged.xlsx')
```

### Word 处理

```python
from office_auto import WordHandler

word = WordHandler()

# 创建 Word 文档
word.create_document('doc.docx', '标题', '内容')

# 读取 Word 文档
data = word.read_document('doc.docx')
print(data['content'])
```

### PDF 处理

```python
from office_auto import PDFHandler

pdf = PDFHandler()

# 创建 PDF
pdf.create_pdf('doc.pdf', '标题', '内容')
```

## 输出示例

### Excel 读取结果

```
✅ 读取成功: sample.xlsx
   行数: 3
   列名: 日期, 产品, 销量, 收入

前10行数据:
   {'日期': '2026-01-01', '产品': '产品A', '销量': 100, '收入': 10000}
   {'日期': '2026-01-02', '产品': '产品B', '销量': 150, '收入': 15000}
   {'日期': '2026-01-03', '产品': '产品C', '销量': 200, '收入': 20000}
```

## 依赖要求

| 包名 | 用途 | 版本 |
|------|------|------|
| pandas | Excel/CSV 数据处理 | >=2.0 |
| openpyxl | Excel 文件读写 | >=3.0 |
| python-docx | Word 文档处理 | >=1.0 |
| fpdf2 | PDF 文档生成 | >=2.0 |

## 应用场景

### 1. 批量数据处理

```python
from office_auto import ExcelHandler

excel = ExcelHandler()

# 读取多个 Excel 文件并合并
files = ['sales_2025.xlsx', 'sales_2026.xlsx']
excel.merge_excel(files, 'sales_all.xlsx')
```

### 2. 报告生成

```python
from office_auto import WordHandler, PDFHandler

# 生成 Word 报告
word = WordHandler()
word.create_document('report.docx', '月度报告', '报告内容...')

# 生成 PDF
pdf = PDFHandler()
pdf.create_pdf('report.pdf', '月度报告', '报告内容...')
```

### 3. 数据转换

```python
from office_auto import ExcelHandler

excel = ExcelHandler()

# Excel 转 CSV 进行文本处理
excel.excel_to_csv('data.xlsx', 'data.csv')

# 处理完成后转回 Excel
excel.csv_to_excel('data_processed.csv', 'data_processed.xlsx')
```

## 文件结构

```
skills/office-automation/
├── SKILL.md                      # 本文件
└── scripts/
    └── office_auto.py            # 主脚本
```

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- Excel 读写、转换、合并
- Word 创建和读取
- PDF 生成
