#!/usr/bin/env python3
"""
deploy_to_github.py - 报告自动部署到GitHub Pages
自动上传报告并更新导航页，无需手动干预
"""

import base64
import json
import os
import sys
import urllib.request
from datetime import datetime

# 配置
REPO = "qinzheng1983/pre-market-dashboard"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

if not TOKEN:
    print("❌ 错误: 未设置 GITHUB_TOKEN 环境变量")
    print("   请执行: export GITHUB_TOKEN='ghp_xxx'")
    sys.exit(1)
REPORTS_DIR = "/root/.openclaw/workspace/reports"
GITHUB_API = f"https://api.github.com/repos/{REPO}/contents"

def github_api(path, method="GET", data=None):
    """调用GitHub API"""
    url = f"{GITHUB_API}/{path}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if method == "GET":
        req = urllib.request.Request(url, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        error_body = e.read().decode('utf-8')
        print(f"   ⚠️  GitHub API错误 ({e.code}): {error_body[:200]}")
        return None
    except Exception as e:
        print(f"   ⚠️  请求失败: {e}")
        return None

def get_file_sha(path):
    """获取文件SHA（如果存在）"""
    result = github_api(path)
    if result and 'sha' in result:
        return result['sha']
    return None

def upload_file(path, local_file, message):
    """上传文件到GitHub"""
    with open(local_file, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    sha = get_file_sha(path)
    
    payload = {
        "message": message,
        "content": content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha
    
    result = github_api(path, "PUT", payload)
    if result and 'content' in result:
        print(f"   ✅ 上传成功: {path}")
        return True
    else:
        print(f"   ❌ 上传失败: {path}")
        return False

def update_dashboard(report_type, date_str, display_date, summary):
    """更新导航页，保留最新一期盘前简报 + 最新一期财资日报 + 最新一期财资周报"""
    
    # 获取现有导航页
    dashboard_sha = get_file_sha("dashboard.html")
    
    # 构建报告卡片HTML
    pre_market_date = display_date if report_type == 'pre-market' else '点击查看'
    finance_daily_date = display_date if report_type == 'finance-daily' else '点击查看'
    finance_weekly_date = display_date if report_type == 'finance-weekly' else '点击查看'
    
    pre_market_summary = summary if report_type == 'pre-market' else '数据截止前一交易日收盘'
    finance_daily_summary = summary if report_type == 'finance-daily' else '当日完整收盘数据与深度分析'
    finance_weekly_summary = summary if report_type == 'finance-weekly' else '本周走势汇总+下周前瞻+CFO视角策略'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财资报告中心</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #1a1a2e;
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 16px;
            opacity: 0.7;
        }}
        .report-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            max-width: 1000px;
            width: 100%;
        }}
        .report-card {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s;
            text-decoration: none;
            color: white;
            display: block;
        }}
        .report-card:hover {{
            transform: translateY(-5px);
            background: rgba(255,255,255,0.15);
            border-color: #e94560;
        }}
        .report-card .date {{
            font-size: 14px;
            color: #e94560;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .report-card .title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .report-card .desc {{
            font-size: 14px;
            opacity: 0.7;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            opacity: 0.5;
        }}
        .badge {{
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>财资报告中心</h1>
        <p>跨国企业资金管理决策参考</p>
    </div>
    
    <div class="report-grid">
        <!-- 盘前简报 -->
        <a href="index.html" class="report-card">
            <div class="date">{pre_market_date} <span class="badge">最新</span></div>
            <div class="title">盘前市场简报</div>
            <div class="desc">每日08:30发布，覆盖全球市场开盘前关键数据与事件<br><br>{pre_market_summary}</div>
        </a>
        
        <!-- 财资日报 -->
        <a href="finance-daily/{date_str if report_type == 'finance-daily' else '20260424'}.html" class="report-card">
            <div class="date">{finance_daily_date} <span class="badge">最新</span></div>
            <div class="title">财资日报</div>
            <div class="desc">每日16:00发布，涵盖货币政策、汇率、新能源、有色金属、贵金属、地缘风险<br><br>{finance_daily_summary}</div>
        </a>
        
        <!-- 财资周报 -->
        <a href="finance-weekly/{date_str if report_type == 'finance-weekly' else '2026w17'}.html" class="report-card">
            <div class="date">{finance_weekly_date} <span class="badge">最新</span></div>
            <div class="title">财资周报</div>
            <div class="desc">每周五发布，周度走势汇总+下周前瞻+CFO视角对冲策略<br><br>{finance_weekly_summary}</div>
        </a>
    </div>
    
    <div class="footer">
        由 OpenClaw AI 自动生成 | 数据仅供参考 | 更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
</body>
</html>'''
    
    # 如果已有导航页，尝试保留另一份报告的信息
    if dashboard_sha:
        # 简化处理：直接上传新导航页
        pass
    
    # 上传导航页
    content = base64.b64encode(html.encode('utf-8')).decode('utf-8')
    payload = {
        "message": f"Update dashboard for {report_type} {date_str}",
        "content": content,
        "branch": "main"
    }
    if dashboard_sha:
        payload["sha"] = dashboard_sha
    
    result = github_api("dashboard.html", "PUT", payload)
    if result and 'content' in result:
        print(f"   ✅ 导航页更新成功")
        return True
    else:
        print(f"   ❌ 导航页更新失败")
        return False

def deploy_report(report_type, date_str, summary=""):
    """主部署函数"""
    print("=" * 60)
    print(f"🚀 部署 {report_type} {date_str} 到 GitHub Pages")
    print("=" * 60)
    
    # 确定源文件和目标路径
    if report_type == "pre-market":
        possible_files = [
            f"{REPORTS_DIR}/pre_market_briefing_{date_str}.html",
            f"{REPORTS_DIR}/pre_market_briefing_{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}.html",
        ]
        target_path = "index.html"
        display_date = f"{date_str[:4]}年{date_str[4:6]}月{date_str[6:]}日"
    elif report_type == "finance-daily":
        possible_files = [
            f"{REPORTS_DIR}/finance_daily_{date_str}.html",
            f"{REPORTS_DIR}/finance_daily_{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}.html",
        ]
        target_path = f"finance-daily/{date_str}.html"
        display_date = f"{date_str[:4]}年{date_str[4:6]}月{date_str[6:]}日"
    elif report_type == "finance-weekly":
        # date_str format: 2026w17
        possible_files = [
            f"{REPORTS_DIR}/finance_weekly_{date_str}.html",
        ]
        target_path = f"finance-weekly/{date_str}.html"
        # Extract year and week from 2026w17
        year = date_str[:4]
        week = date_str[5:]
        display_date = f"{year}年第{week}周"
    else:
        print(f"❌ 未知报告类型: {report_type}")
        return False
    
    # 查找存在的文件
    source_file = None
    for f in possible_files:
        if os.path.exists(f):
            source_file = f
            break
    
    if not source_file:
        print(f"❌ 找不到报告文件，尝试了: {possible_files}")
        return False
    
    print(f"\n1. 上传报告文件...")
    print(f"   源: {source_file}")
    print(f"   目标: {target_path}")
    
    if not upload_file(target_path, source_file, f"Deploy {report_type} {date_str}"):
        return False
    
    print(f"\n2. 更新导航页...")
    update_dashboard(report_type, date_str, display_date, summary)
    
    print(f"\n{'=' * 60}")
    print(f"✅ 部署完成")
    print(f"{'=' * 60}")
    print(f"报告URL: https://qinzheng1983.github.io/pre-market-dashboard/{target_path}")
    print(f"导航页: https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 deploy_to_github.py <pre-market|finance-daily> <YYYYMMDD> [summary]")
        print("示例: python3 deploy_to_github.py pre-market 20260423")
        sys.exit(1)
    
    report_type = sys.argv[1]
    date_str = sys.argv[2]
    summary = sys.argv[3] if len(sys.argv) > 3 else ""
    
    success = deploy_report(report_type, date_str, summary)
    sys.exit(0 if success else 1)
