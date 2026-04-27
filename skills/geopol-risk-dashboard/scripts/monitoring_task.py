#!/usr/bin/env python3
"""
中东地缘风险综合监控任务
定时执行综合分析并生成报告
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/geopol-risk-dashboard/scripts')

from comprehensive_analysis import ComprehensiveRiskAnalyzer
from self_improving_agent import SelfImprovingAgent
from datetime import datetime
import json

def run_monitoring_task():
    """执行监控任务"""
    print("="*70)
    print("🔄 中东地缘风险综合监控任务")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 1. 执行综合分析
    analyzer = ComprehensiveRiskAnalyzer()
    report = analyzer.generate_comprehensive_report()
    
    # 2. 保存报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"/root/.openclaw/workspace/geopol-risk-reports/comprehensive_report_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存: {report_file}")
    
    # 3. 自改进记录
    agent = SelfImprovingAgent()
    agent.reflect(
        context="执行定时地缘风险监控任务",
        action="综合分析新闻、市场数据、汇率影响",
        outcome=f"生成综合报告: {report_file}",
        lesson="多源数据整合可以提高分析全面性",
        improvement="增加自动化数据获取pipeline"
    )
    
    # 4. 生成摘要
    summary = {
        'timestamp': datetime.now().isoformat(),
        'report_file': report_file,
        'status': 'success',
        'next_run': '根据cron配置'
    }
    
    with open('/root/.openclaw/workspace/geopol-risk-reports/monitoring_log.json', 'a') as f:
        f.write(json.dumps(summary) + '\n')
    
    print("\n✅ 监控任务完成")
    print("="*70)

if __name__ == "__main__":
    run_monitoring_task()
