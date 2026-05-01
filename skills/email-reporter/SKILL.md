---
name: email-reporter
description: Email Reporter - 邮件报告发送工具。支持139邮箱、Outlook等SMTP发送，完整报告内容(高信息密度)+PDF附件，自动发送地缘风险报告到指定邮箱。
metadata:
  version: 1.2.0
  author: openclaw
  category: notification
---

# Email Reporter - 邮件报告发送工具

## 概述

专业的邮件报告发送工具，支持：
- 📧 **139邮箱** (推荐，国内稳定)
- 📧 **Outlook/Hotmail**
- 📧 **QQ邮箱**
- 📧 **163邮箱**
- 📧 **Gmail**

**特色功能：**
- ✅ 完整报告内容 (高信息密度)
- ✅ 自动生成PDF报告附件
- ✅ 简洁HTML格式 (避免被拦截)

## 配置步骤

### 1. 获取邮箱授权码 (以139邮箱为例)

**授权码是什么？**
- 授权码是邮箱提供的专用密码，用于第三方应用发送邮件
- **不是**你的登录密码，需要单独获取

**获取步骤：**

1. **登录 139邮箱**
   - 访问 https://mail.10086.cn
   - 使用手机号 13911658378 登录

2. **进入设置**
   - 点击右上角「设置」
   - 选择「账户」→「POP3/IMAP/SMTP服务」

3. **开启 SMTP 服务**
   - 找到「SMTP服务」选项
   - 点击「开启」
   - 可能需要短信验证

4. **获取授权码**
   - 系统会生成一串授权码 (如: `abcd1234efgh`)
   - **保存好这个授权码**，它只显示一次
   - 如果丢失，可以重新生成

### 2. 配置环境变量

```bash
# 添加到 ~/.bashrc 使其永久生效
export EMAIL_SENDER="13911658378@139.com"
export EMAIL_PASSWORD="你的授权码"

# 使配置生效
source ~/.bashrc
```

### 3. 测试发送

```bash
# 发送测试邮件
python3 skills/email-reporter/scripts/email_reporter.py test
```

## 使用方法

### 发送测试邮件
```bash
python3 skills/email-reporter/scripts/email_reporter.py test
```

### 发送地缘风险报告 (完整内容 + PDF附件)
```bash
python3 skills/email-reporter/scripts/email_reporter.py report
```

### 发送地缘风险报告 (无PDF附件)
```bash
python3 skills/email-reporter/scripts/email_reporter.py report --no-pdf
```

### 发送自定义邮件
```bash
python3 skills/email-reporter/scripts/email_reporter.py send \
  --to baichiyishi@outlook.com \
  --subject "测试主题" \
  --content "这是一封测试邮件"
```

### 带附件发送
```bash
python3 skills/email-reporter/scripts/email_reporter.py send \
  --to 13911658378@139.com \
  --subject "风险报告" \
  --content "请查看附件" \
  --attachment /path/to/report.pdf
```

## 报告内容

### 邮件正文
- **高信息密度** - 包含完整Markdown报告内容
- **格式保留** - 标题、表格、列表完整呈现
- **简洁样式** - 避免复杂CSS，减少被拦截概率

### PDF附件
- **完整报告** - 包含所有数据和分析
- **专业排版** - A4版面，适合打印归档
- **约60-70KB** - 大小适中

## 定时任务设置

### 每日 06:00 自动发送风险报告

```bash
# 添加到 crontab
crontab -e

# 添加以下行
0 6 * * * cd /root/.openclaw/workspace && EMAIL_SENDER=13911658378@139.com EMAIL_PASSWORD=xxx python3 skills/email-reporter/scripts/email_reporter.py report
```

或使用 OpenClaw Cron:
```json
{
  "name": "daily-risk-report-email",
  "schedule": {"kind": "cron", "expr": "0 6 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "发送今日地缘风险报告到 13911658378@139.com"
  },
  "sessionTarget": "isolated"
}
```

## 各邮箱授权码获取方式

| 邮箱 | 授权码获取路径 |
|------|---------------|
| **139邮箱** | 设置 → 账户 → POP3/IMAP/SMTP服务 → 开启SMTP → 获取授权码 |
| **Outlook** | 账户安全 → 更多安全选项 → 创建应用密码 |
| **QQ邮箱** | 设置 → 账户 → 开启POP3/SMTP服务 → 生成授权码 |
| **163邮箱** | 设置 → POP3/SMTP/IMAP → 开启SMTP服务 → 设置授权码 |
| **Gmail** | 账户 → 安全性 → 应用密码 → 生成 |

## 常见问题

### Q: 提示 "登录失败"
- 检查授权码是否正确 (不是登录密码)
- 检查邮箱是否开启了 SMTP 服务
- 检查手机号/邮箱地址是否输入正确

### Q: 邮件进入垃圾箱
- 将发件人添加到通讯录
- 使用简洁的HTML格式（已优化）
- 避免使用emoji和敏感词

### Q: 提示 "Mail rejected"
- 139邮箱可能限制了发送频率
- 等待几分钟后重试
- 简化邮件内容后重试

### Q: PDF附件太大
- 当前PDF约60-70KB，大小合适
- 如需更小，可使用 `--no-pdf` 选项

### Q: 139邮箱发送限制
- 新授权账户只能发给自己
- 不能发送到外部邮箱 (如 Outlook)
- 建议发送到自己的139邮箱查看

## 文件结构

```
skills/email-reporter/
├── SKILL.md                      # 本文件
└── scripts/
    ├── email_reporter.py         # 主脚本 (高信息密度版)
    └── pdf_generator.py          # PDF生成器
```

## Python API

```python
from email_reporter import EmailReporter

# 初始化
reporter = EmailReporter(
    email="13911658378@139.com",
    password="你的授权码",
    provider="139"
)

# 发送邮件
reporter.send_email(
    to_email="baichiyishi@outlook.com",
    subject="测试",
    content="<h1>Hello</h1>",
    content_type="html"
)

# 发送风险报告 (完整内容 + PDF)
reporter.send_risk_report("13911658378@139.com", use_pdf=True)

# 生成PDF报告
pdf_path = reporter.generate_pdf_report()
```

## 更新日志

### v1.2.0 (2026-03-16)
- 恢复高信息密度的完整报告内容
- 简化HTML格式，减少被拦截概率
- PDF附件保持专业排版

### v1.1.0 (2026-03-16)
- 优化HTML邮件模板，响应式设计
- 自动生成PDF附件
- 风险等级可视化

### v1.0.0 (2026-03-16)
- 初始版本
- 支持139/Outlook/QQ/163/Gmail
- HTML邮件支持
- 附件发送
- 地缘风险报告自动发送
