#!/bin/bash
# deploy_report.sh - 报告自动部署脚本 v1.0
# 用法: ./deploy_report.sh <pre-market|finance-daily> <YYYYMMDD>
# 示例: ./deploy_report.sh pre-market 20260422
#       ./deploy_report.sh finance-daily 20260422

set -e

REPO="qinzheng1983/pre-market-dashboard"
TOKEN="${GITHUB_TOKEN:-}"
REPORTS_DIR="/root/.openclaw/workspace/reports"
DASHBOARD_FILE="/root/.openclaw/workspace/dashboard.html"

if [ -z "$TOKEN" ]; then
    echo "错误: 未设置 GITHUB_TOKEN 环境变量"
    echo "请执行: export GITHUB_TOKEN='ghp_xxx'"
    exit 1
fi
if [ $# -ne 2 ]; then
    echo "用法: $0 <pre-market|finance-daily> <YYYYMMDD>"
    exit 1
fi

REPORT_TYPE=$1
DATE_STR=$2

echo "========================================"
echo " 报告部署脚本 - $REPORT_TYPE $DATE_STR"
echo "========================================"

# 确定源文件和目标路径
if [ "$REPORT_TYPE" == "pre-market" ]; then
    SOURCE_FILE="$REPORTS_DIR/pre_market_briefing_${DATE_STR}.html"
    TARGET_PATH="index.html"
    REPORT_NAME="盘前市场简报"
    NAV_SECTION="盘前市场简报"
elif [ "$REPORT_TYPE" == "finance-daily" ]; then
    SOURCE_FILE="$REPORTS_DIR/finance_daily_${DATE_STR}.html"
    TARGET_PATH="finance-daily/${DATE_STR}.html"
    REPORT_NAME="财资日报"
    NAV_SECTION="财资日报"
else
    echo "错误: 报告类型必须是 pre-market 或 finance-daily"
    exit 1
fi

# 检查源文件是否存在
if [ ! -f "$SOURCE_FILE" ]; then
    echo "错误: 源文件不存在: $SOURCE_FILE"
    exit 1
fi

echo ""
echo "1. 上传报告文件..."
echo "   源: $SOURCE_FILE"
echo "   目标: $TARGET_PATH"

# 获取文件SHA（如果存在）
SHA=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/contents/$TARGET_PATH" | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")

# 准备payload
CONTENT=$(base64 -w 0 "$SOURCE_FILE")
PAYLOAD="{\"message\":\"Deploy $REPORT_NAME $DATE_STR\",\"content\":\"$CONTENT\",\"branch\":\"main\"}"

if [ -n "$SHA" ]; then
    PAYLOAD="{\"message\":\"Update $REPORT_NAME $DATE_STR\",\"content\":\"$CONTENT\",\"sha\":\"$SHA\",\"branch\":\"main\"}"
fi

# 上传报告
RESPONSE=$(curl -s -X PUT \
    -H "Authorization: token $TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.github.com/repos/$REPO/contents/$TARGET_PATH" \
    -d "$PAYLOAD")

if echo "$RESPONSE" | grep -q '"sha"'; then
    echo "   上传成功"
else
    echo "   上传失败: $RESPONSE"
    exit 1
fi

echo ""
echo "2. 更新导航页 (dashboard.html)..."

# 这里需要根据实际情况更新导航页的日期和描述
# 简化版本：提示用户手动更新或使用Python脚本处理
# 完整版本需要解析HTML并替换对应部分

echo "   导航页更新需要手动处理或使用Python脚本"
echo "   请确保 dashboard.html 中的 '$NAV_SECTION' 卡片已更新为 $DATE_STR"

echo ""
echo "========================================"
echo " 部署完成"
echo "========================================"
echo "报告URL: https://qinzheng1983.github.io/pre-market-dashboard/$TARGET_PATH"
echo "导航页: https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html"
echo ""
echo "⚠️  请手动验证导航页是否显示最新日期"
