#!/usr/bin/env python3
"""
Report Auto-Generator - 报告自动生成器
自动检查并生成盘前简报和财资日报
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path('/root/.openclaw/workspace')
REPORTS_DIR = WORKSPACE / 'reports'
MEMORY_DIR = WORKSPACE / 'memory'
STATE_FILE = MEMORY_DIR / 'report_state.json'

def get_datetime_util():
    """调用 datetime-utils skill 获取准确时间"""
    import subprocess
    result = subprocess.run(
        ['python3', str(WORKSPACE / 'skills/datetime-utils/datetime_utils.py')],
        capture_output=True, text=True
    )
    # 解析输出
    lines = result.stdout.strip().split('\n')
    current_date = None
    is_trading_day = False
    prev_trading_day = None
    
    for line in lines:
        if '当前日期:' in line:
            current_date = line.split(':')[1].strip()
        elif '是否交易日(CN):' in line:
            is_trading_day = '是' in line
        elif '前一交易日:' in line:
            prev_trading_day = line.split(':')[1].strip()
    
    return {
        'date': current_date,
        'is_trading_day': is_trading_day,
        'prev_trading_day': prev_trading_day
    }

def load_state():
    """加载报告状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'pre_market': {},
        'finance_daily': {},
        'last_check': None
    }

def save_state(state):
    """保存报告状态"""
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_report_exists(report_type: str, date_str: str) -> bool:
    """检查某日期报告是否存在"""
    if report_type == 'pre_market':
        pattern = f'pre_market_briefing_{date_str.replace("-", "")}*.html'
    elif report_type == 'finance_daily':
        pattern = f'finance_daily_{date_str.replace("-", "")}*.html'
    else:
        return False
    
    import glob
    files = glob.glob(str(REPORTS_DIR / pattern))
    return len(files) > 0

def should_generate_pre_market(time_info: dict) -> bool:
    """判断是否应该生成盘前简报"""
    if not time_info['is_trading_day']:
        return False
    
    current_time = datetime.now()
    cutoff_time = current_time.replace(hour=8, minute=30, second=0, microsecond=0)
    
    # 如果已经过了8:30，且今天的报告还没有生成
    if current_time >= cutoff_time:
        today = time_info['date']
        if not check_report_exists('pre_market', today):
            return True
    
    return False

def should_generate_finance_daily(time_info: dict) -> bool:
    """判断是否应该生成财资日报"""
    if not time_info['is_trading_day']:
        return False
    
    current_time = datetime.now()
    cutoff_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
    
    # 如果已经过了16:00，且今天的报告还没有生成
    if current_time >= cutoff_time:
        today = time_info['date']
        if not check_report_exists('finance_daily', today):
            return True
    
    return False

def get_missing_reports(time_info: dict) -> dict:
    """获取所有漏发的报告"""
    missing = {
        'pre_market': [],
        'finance_daily': []
    }
    
    today = datetime.strptime(time_info['date'], '%Y-%m-%d')
    
    # 检查过去7个工作日
    for i in range(7):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime('%Y-%m-%d')
        
        # 跳过周末
        if check_date.weekday() >= 5:
            continue
        
        # 检查盘前简报
        if not check_report_exists('pre_market', date_str):
            missing['pre_market'].append(date_str)
        
        # 检查财资日报
        if not check_report_exists('finance_daily', date_str):
            missing['finance_daily'].append(date_str)
    
    return missing

def main():
    """主函数"""
    print("=" * 70)
    print("📊 Report Auto-Generator - 报告自动生成检查")
    print("=" * 70)
    
    # 获取准确时间信息
    print("\n🕐 获取准确时间信息...")
    time_info = get_datetime_util()
    print(f"   当前日期: {time_info['date']}")
    print(f"   是否交易日: {'是' if time_info['is_trading_day'] else '否'}")
    print(f"   前一交易日: {time_info['prev_trading_day']}")
    
    # 加载状态
    state = load_state()
    
    # 检查漏发的报告
    print("\n📋 检查报告状态...")
    missing = get_missing_reports(time_info)
    
    needs_action = False
    
    if missing['pre_market']:
        print(f"   ⚠️  漏发盘前简报: {', '.join(missing['pre_market'])}")
        needs_action = True
    else:
        print(f"   ✅ 盘前简报: 已生成 {time_info['date']}")
    
    if missing['finance_daily']:
        print(f"   ⚠️  漏发财资日报: {', '.join(missing['finance_daily'])}")
        needs_action = True
    else:
        print(f"   ✅ 财资日报: 已生成 {time_info['date']}")
    
    # 判断当前是否应该生成报告
    should_gen_pre = should_generate_pre_market(time_info)
    should_gen_fin = should_generate_finance_daily(time_info)
    
    print("\n⏰ 当前时间触发检查:")
    current_time = datetime.now()
    print(f"   当前时间: {current_time.strftime('%H:%M')}")
    
    if should_gen_pre:
        print(f"   🔴 需要生成盘前简报 (已过08:30，报告未生成)")
        needs_action = True
    
    if should_gen_fin:
        print(f"   🔴 需要生成财资日报 (已过16:00，报告未生成)")
        needs_action = True
    
    # 更新状态
    state['last_check'] = {
        'timestamp': current_time.isoformat(),
        'date': time_info['date'],
        'needs_action': needs_action,
        'missing_reports': missing
    }
    save_state(state)
    
    print("\n" + "=" * 70)
    
    if needs_action:
        print("❌ 需要采取行动: 有报告需要生成")
        print("\n请执行以下命令生成报告:")
        if missing['pre_market'] or should_gen_pre:
            print("  - 盘前简报: 需要收集前一交易日(T-1)收盘数据")
        if missing['finance_daily'] or should_gen_fin:
            print("  - 财资日报: 需要收集当日(T)收盘数据")
        sys.exit(1)  # 返回错误码，触发后续处理
    else:
        print("✅ 所有报告已生成，无需操作")
        sys.exit(0)

if __name__ == "__main__":
    main()
