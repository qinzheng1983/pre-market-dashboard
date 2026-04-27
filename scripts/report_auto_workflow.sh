#!/bin/bash
# Report Auto-Workflow - 报告自动工作流 v2.0
# 由 cron 或 heartbeat 调用，自动检查、生成、发送并部署报告

set -e

WORKSPACE="/root/.openclaw/workspace"
REPORTS_DIR="$WORKSPACE/reports"
SCRIPTS_DIR="$WORKSPACE/scripts"
EMAIL_SENDER="13911658378@139.com"
EMAIL_PASSWORD="f79d697414966c63d600"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "📊 报告自动工作流 v2.0 - $(date)"
echo "========================================"

# 获取准确时间信息
echo ""
echo "🕐 获取时间信息..."
TIME_INFO=$(python3 "$WORKSPACE/skills/datetime-utils/datetime_utils.py" 2>/dev/null)
echo "$TIME_INFO"

# 解析日期
CURRENT_DATE=$(echo "$TIME_INFO" | grep "当前日期:" | cut -d: -f2 | tr -d ' ')
IS_TRADING_DAY=$(echo "$TIME_INFO" | grep "是否交易日(CN):" | grep -q "是" && echo "true" || echo "false")
PREV_TRADING_DAY=$(echo "$TIME_INFO" | grep "前一交易日:" | cut -d: -f2 | tr -d ' ')

echo ""
echo "📅 当前日期: $CURRENT_DATE"
echo "📈 是否交易日: $IS_TRADING_DAY"
echo "📊 前一交易日: $PREV_TRADING_DAY"

# 如果不是交易日，退出
if [ "$IS_TRADING_DAY" != "true" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  非交易日，跳过报告生成${NC}"
    exit 0
fi

# ============================================
# 辅助函数：部署报告到GitHub
# ============================================
deploy_to_github() {
    local report_type=$1
    local date_str=$2
    local summary=$3
    
    echo ""
    echo "🚀 部署到GitHub Pages..."
    echo "   类型: $report_type"
    echo "   日期: $date_str"
    
    if python3 "$SCRIPTS_DIR/deploy_to_github.py" "$report_type" "$date_str" "$summary" 2>/dev/null; then
        echo -e "${GREEN}   ✅ GitHub部署成功${NC}"
        return 0
    else
        echo -e "${RED}   ❌ GitHub部署失败${NC}"
        return 1
    fi
}

# ============================================
# 辅助函数：发送邮件
# ============================================
send_email() {
    local report_file=$1
    local subject=$2
    
    echo ""
    echo "📧 发送邮件..."
    
    # 使用Python发送邮件
    python3 -c "
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = '$EMAIL_SENDER'
password = '$EMAIL_PASSWORD'
receiver = '$EMAIL_SENDER'

with open('$report_file', 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = '$subject'
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

try:
    server = smtplib.SMTP_SSL('smtp.139.com', 465, timeout=10)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    print('   ✅ 邮件发送成功')
except Exception as e:
    print(f'   ❌ 邮件发送失败: {e}')
" 2>/dev/null
}

# ============================================
# 检查盘前简报
# ============================================
echo ""
echo "📋 检查盘前简报..."
PRE_MARKET_FILE=$(find "$REPORTS_DIR" -name "pre_market_briefing_${CURRENT_DATE//-/}*.html" -type f 2>/dev/null | head -1)

if [ -n "$PRE_MARKET_FILE" ]; then
    echo -e "${GREEN}✅ 盘前简报已存在: $(basename "$PRE_MARKET_FILE")${NC}"
    
    # 检查是否已部署到GitHub（通过检查日志或状态文件）
    DEPLOY_STATUS_FILE="$WORKSPACE/memory/deploy_status_${CURRENT_DATE//-/}.json"
    if [ ! -f "$DEPLOY_STATUS_FILE" ] || ! grep -q '"pre_market": true' "$DEPLOY_STATUS_FILE" 2>/dev/null; then
        echo "   📤 未检测到GitHub部署记录，执行部署..."
        
        # 提取摘要（从HTML中提取"今日重点"内容）
        SUMMARY=$(grep -oP '(?<=<b>今日重点:</b>)[^<]+' "$PRE_MARKET_FILE" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' || echo "盘前简报已更新")
        
        deploy_to_github "pre-market" "${CURRENT_DATE//-/}" "$SUMMARY"
        
        # 记录部署状态
        mkdir -p "$WORKSPACE/memory"
        echo '{"pre_market": true}' > "$DEPLOY_STATUS_FILE"
    else
        echo -e "${GREEN}   ✅ GitHub已部署${NC}"
    fi
    
    # 检查是否已发送邮件
    if [ ! -f "$DEPLOY_STATUS_FILE" ] || ! grep -q '"email_sent": true' "$DEPLOY_STATUS_FILE" 2>/dev/null; then
        echo "   📧 未检测到邮件发送记录，执行发送..."
        WEEKDAY=$(date +%u)
        WEEKDAY_NAMES=("" "周一" "周二" "周三" "周四" "周五" "周六" "周日")
        SUBJECT="盘前市场简报 — ${CURRENT_DATE:0:4}年${CURRENT_DATE:5:2}月${CURRENT_DATE:8:2}日（${WEEKDAY_NAMES[$WEEKDAY]}）"
        send_email "$PRE_MARKET_FILE" "$SUBJECT"
    fi
else
    echo -e "${RED}❌ 盘前简报未生成${NC}"
    
    # 检查时间是否已过8:30
    CURRENT_HOUR=$(date +%H)
    CURRENT_MIN=$(date +%M)
    CURRENT_TIME=$((CURRENT_HOUR * 60 + CURRENT_MIN))
    CUTOFF_TIME=$((8 * 60 + 30))  # 8:30
    
    if [ $CURRENT_TIME -ge $CUTOFF_TIME ]; then
        echo ""
        echo -e "${YELLOW}🔴 已过08:30，需要生成盘前简报${NC}"
        echo "    请手动执行报告生成流程:"
        echo "    1. 收集前一交易日($PREV_TRADING_DAY)收盘数据"
        echo "    2. 生成盘前简报"
        echo "    3. 部署到GitHub + 发送邮件"
        
        # 记录到状态文件
        echo "{\"date\": \"$CURRENT_DATE\", \"type\": \"pre_market\", \"status\": \"missing\", \"timestamp\": \"$(date -Iseconds)\"}" >> "$WORKSPACE/memory/report_missing.log"
    else
        echo -e "${YELLOW}⏰ 未到08:30，暂不生成${NC}"
    fi
fi

# ============================================
# 检查财资日报
# ============================================
echo ""
echo "📋 检查财资日报..."
FINANCE_DAILY_FILE=$(find "$REPORTS_DIR" -name "finance_daily_${CURRENT_DATE//-/}*.html" -type f 2>/dev/null | head -1)

if [ -n "$FINANCE_DAILY_FILE" ]; then
    echo -e "${GREEN}✅ 财资日报已存在: $(basename "$FINANCE_DAILY_FILE")${NC}"
    
    # 检查是否已部署到GitHub
    DEPLOY_STATUS_FILE="$WORKSPACE/memory/deploy_status_${CURRENT_DATE//-/}.json"
    if [ ! -f "$DEPLOY_STATUS_FILE" ] || ! grep -q '"finance_daily": true' "$DEPLOY_STATUS_FILE" 2>/dev/null; then
        echo "   📤 未检测到GitHub部署记录，执行部署..."
        
        SUMMARY=$(grep -oP '(?<=<b>今日重点关注:</b>)[^<]+' "$FINANCE_DAILY_FILE" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' || echo "财资日报已更新")
        
        deploy_to_github "finance-daily" "${CURRENT_DATE//-/}" "$SUMMARY"
        
        # 记录部署状态
        echo '{"finance_daily": true}' >> "$DEPLOY_STATUS_FILE"
    else
        echo -e "${GREEN}   ✅ GitHub已部署${NC}"
    fi
else
    echo -e "${RED}❌ 财资日报未生成${NC}"
    
    # 检查时间是否已过16:00
    CURRENT_HOUR=$(date +%H)
    CURRENT_MIN=$(date +%M)
    CURRENT_TIME=$((CURRENT_HOUR * 60 + CURRENT_MIN))
    CUTOFF_TIME=$((16 * 60))  # 16:00
    
    if [ $CURRENT_TIME -ge $CUTOFF_TIME ]; then
        echo ""
        echo -e "${YELLOW}🔴 已过16:00，需要生成财资日报${NC}"
        echo "    请手动执行报告生成流程:"
        echo "    1. 收集当日($CURRENT_DATE)收盘数据"
        echo "    2. 生成财资日报"
        echo "    3. 部署到GitHub + 发送邮件"
        
        # 记录到状态文件
        echo "{\"date\": \"$CURRENT_DATE\", \"type\": \"finance_daily\", \"status\": \"missing\", \"timestamp\": \"$(date -Iseconds)\"}" >> "$WORKSPACE/memory/report_missing.log"
    else
        echo -e "${YELLOW}⏰ 未到16:00，暂不生成${NC}"
    fi
fi

# 输出状态摘要
echo ""
echo "========================================"
echo "📊 状态摘要"
echo "========================================"
echo "日期: $CURRENT_DATE"
echo "交易日: $IS_TRADING_DAY"
echo ""
echo "报告状态:"
if [ -n "$PRE_MARKET_FILE" ]; then
    echo -e "  盘前简报: ${GREEN}✅ 已生成${NC}"
else
    echo -e "  盘前简报: ${RED}❌ 未生成${NC}"
fi

if [ -n "$FINANCE_DAILY_FILE" ]; then
    echo -e "  财资日报: ${GREEN}✅ 已生成${NC}"
else
    echo -e "  财资日报: ${RED}❌ 未生成${NC}"
fi

echo ""
echo "========================================"
echo "工作流完成 - $(date)"
echo "========================================"
