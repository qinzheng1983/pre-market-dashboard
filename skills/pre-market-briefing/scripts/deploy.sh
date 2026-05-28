#!/bin/bash
# deploy.sh - 盘前简报部署脚本
# 用法: ./deploy.sh pre-market YYYYMMDD
# 将 reports/pre_market_briefing_YYYYMMDD.html 部署到 GitHub Pages

set -e

REPO="qinzheng1983/pre-market-dashboard"
TOKEN="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"
REPORTS_DIR="/root/.openclaw/workspace/reports"
DASHBOARD_FILE="/root/.openclaw/workspace/dashboard.html"

if [ $# -ne 2 ]; then
    echo "用法: $0 <pre-market|finance-daily> <YYYYMMDD>"
    exit 1
fi

REPORT_TYPE=$1
DATE_STR=$2

echo "========================================"
echo " 报告部署 - $REPORT_TYPE $DATE_STR"
echo "========================================"

if [ "$REPORT_TYPE" == "pre-market" ]; then
    SOURCE_FILE="$REPORTS_DIR/pre_market_briefing_${DATE_STR}.html"
    TARGET_PATH="index.html"
    REPORT_NAME="盘前简报"
elif [ "$REPORT_TYPE" == "finance-daily" ]; then
    SOURCE_FILE="$REPORTS_DIR/finance_daily_${DATE_STR}.html"
    TARGET_PATH="finance-daily/${DATE_STR}.html"
    REPORT_NAME="财资日报"
else
    echo "错误: 报告类型必须是 pre-market 或 finance-daily"
    exit 1
fi

if [ ! -f "$SOURCE_FILE" ]; then
    echo "错误: 源文件不存在: $SOURCE_FILE"
    exit 1
fi

echo ""
echo "1. 上传报告文件..."
echo "   源: $SOURCE_FILE"
echo "   目标: $TARGET_PATH"

SHA=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/contents/$TARGET_PATH" | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")

CONTENT=$(base64 -w 0 "$SOURCE_FILE")
PAYLOAD="{\"message\":\"Deploy $REPORT_NAME $DATE_STR\",\"content\":\"$CONTENT\",\"branch\":\"main\"}"

if [ -n "$SHA" ]; then
    PAYLOAD="{\"message\":\"Update $REPORT_NAME $DATE_STR\",\"content\":\"$CONTENT\",\"sha\":\"$SHA\",\"branch\":\"main\"}"
fi

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
echo "2. 部署导航页 (dashboard.html)..."

if [ -f "$DASHBOARD_FILE" ]; then
    DASH_SHA=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$REPO/contents/dashboard.html" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")
    
    DASH_CONTENT=$(base64 -w 0 "$DASHBOARD_FILE")
    DASH_PAYLOAD="{\"message\":\"Update dashboard for $DATE_STR $REPORT_NAME\",\"content\":\"$DASH_CONTENT\",\"sha\":\"$DASH_SHA\",\"branch\":\"main\"}"
    
    DASH_RESPONSE=$(curl -s -X PUT \
        -H "Authorization: token $TOKEN" \
        -H "Content-Type: application/json" \
        "https://api.github.com/repos/$REPO/contents/dashboard.html" \
        -d "$DASH_PAYLOAD")
    
    if echo "$DASH_RESPONSE" | grep -q '"sha"'; then
        echo "   导航页更新成功"
    else
        echo "   导航页更新失败: $DASH_RESPONSE"
    fi
else
    echo "   警告: dashboard.html 不存在，跳过导航页更新"
fi

echo ""
echo "========================================"
echo " 部署完成"
echo "========================================"
echo "报告URL: https://qinzheng1983.github.io/pre-market-dashboard/$TARGET_PATH"
echo "导航页: https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html"
