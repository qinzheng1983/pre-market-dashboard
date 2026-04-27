#!/usr/bin/env python3
"""
Find Skills - 技能查找器
快速发现、搜索和安装 OpenClaw 技能
"""

import argparse
import subprocess
import json
from typing import List, Dict, Optional

class SkillFinder:
    """技能查找器"""
    
    def __init__(self):
        self.common_skills = {
            "market-data": {
                "name": "market-data-fetch",
                "description": "市场数据获取 - 股票、外汇、加密货币价格",
                "category": "金融数据",
                "installed": True
            },
            "fx-geopol": {
                "name": "fx-geopol-forecast", 
                "description": "汇率地缘风险预测 - USD/CNY 走势分析",
                "category": "风险预测",
                "installed": True
            },
            "geopol-risk": {
                "name": "geopol-risk-dashboard",
                "description": "地缘冲突风险仪表盘 - 中东局势评估",
                "category": "风险监测",
                "installed": True
            },
            "kalshi": {
                "name": "kalshi-trader",
                "description": "Kalshi 预测市场 - 宏观经济事件概率",
                "category": "预测市场",
                "installed": True
            },
            "backtrader": {
                "name": "backtrader",
                "description": "量化回测框架 - Python 策略回测",
                "category": "量化交易",
                "installed": True
            },
            "akshare": {
                "name": "akshare",
                "description": "AKShare 财经数据 - 中国金融数据接口",
                "category": "金融数据",
                "installed": True
            },
            "multi-search-engine": {
                "name": "multi-search-engine",
                "description": "多搜索引擎聚合 - DuckDuckGo、SearXNG 聚合搜索",
                "category": "搜索工具",
                "installed": True
            },
            "find-skills": {
                "name": "find-skills",
                "description": "技能查找器 - 快速发现和安装技能",
                "category": "开发工具",
                "installed": True
            },
            "office-automation": {
                "name": "office-automation",
                "description": "办公自动化工具 - Excel/Word/PDF 处理",
                "category": "办公工具",
                "installed": True
            },
            "self-improving-agent": {
                "name": "self-improving-agent",
                "description": "自改进 Agent 系统 - 反思、学习、优化",
                "category": "AI 增强",
                "installed": True
            },
            "tavily-web-search": {
                "name": "tavily-web-search",
                "description": "Tavily Web Search - AI 实时网页搜索 API",
                "category": "搜索工具",
                "installed": True
            },
            "skill-vetter": {
                "name": "skill-vetter",
                "description": "Skill Vetter - 技能安全审查工具，防止恶意技能",
                "category": "安全工具",
                "installed": True
            },
            "email-reporter": {
                "name": "email-reporter",
                "description": "Email Reporter - 邮件报告发送工具，支持139/Outlook等",
                "category": "通知工具",
                "installed": True
            },
            "weather": {
                "name": "weather",
                "description": "天气查询 - 当前天气和预报",
                "category": "生活工具",
                "installed": False
            },
            "md-to-pdf": {
                "name": "md-to-pdf",
                "description": "Markdown 转 PDF - 文档转换工具",
                "category": "文档工具",
                "installed": False
            },
            "daily-report": {
                "name": "daily-report",
                "description": "每日情报简报 - 生成专业日报 PDF",
                "category": "报告生成",
                "installed": False
            },
            "feishu-doc": {
                "name": "feishu-doc",
                "description": "飞书文档 - 读写飞书云文档",
                "category": "办公集成",
                "installed": False
            },
            "healthcheck": {
                "name": "healthcheck",
                "description": "安全检查 - 系统安全审计和加固",
                "category": "系统管理",
                "installed": False
            },
            "clawhub": {
                "name": "clawhub",
                "description": "ClawHub CLI - 技能仓库管理",
                "category": "开发工具",
                "installed": True
            }
        }
        
    def search(self, keyword: str) -> List[Dict]:
        """搜索技能"""
        keyword_lower = keyword.lower()
        results = []
        
        for key, skill in self.common_skills.items():
            # 匹配名称、描述、类别
            if (keyword_lower in key.lower() or 
                keyword_lower in skill['name'].lower() or
                keyword_lower in skill['description'].lower() or
                keyword_lower in skill['category'].lower()):
                results.append({
                    "key": key,
                    **skill
                })
                
        return results
    
    def list_by_category(self, category: Optional[str] = None) -> Dict:
        """按类别列出技能"""
        if category:
            return {
                category: [s for s in self.common_skills.values() 
                          if s['category'] == category]
            }
        
        # 按类别分组
        categories = {}
        for key, skill in self.common_skills.items():
            cat = skill['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({"key": key, **skill})
        return categories
    
    def list_installed(self) -> List[Dict]:
        """列出已安装技能"""
        return [{"key": k, **v} for k, v in self.common_skills.items() 
                if v['installed']]
    
    def get_install_command(self, skill_key: str) -> str:
        """获取安装命令"""
        skill = self.common_skills.get(skill_key)
        if not skill:
            return f"# 技能 {skill_key} 未找到"
        
        if skill['installed']:
            return f"# {skill['name']} 已安装"
        
        # 根据不同技能返回不同安装命令
        if skill_key in ['market-data', 'kalshi', 'backtrader', 'akshare']:
            return f"""# 安装 {skill['name']}
pip install {skill_key.replace('-', '_')} --break-system-packages"""
        else:
            return f"""# 从 ClawHub 安装
clawhub install {skill['name']}"""
    
    def recommend_for_task(self, task: str) -> List[Dict]:
        """根据任务推荐技能"""
        task_lower = task.lower()
        
        recommendations = {
            "汇率": ["fx-geopol", "market-data", "kalshi"],
            "外汇": ["fx-geopol", "market-data", "kalshi"],
            "股票": ["market-data", "backtrader", "akshare"],
            "量化": ["backtrader", "market-data", "akshare"],
            "风险": ["geopol-risk", "fx-geopol"],
            "地缘": ["geopol-risk", "fx-geopol"],
            "预测": ["kalshi", "fx-geopol"],
            "数据": ["market-data", "akshare", "kalshi"],
            "报告": ["daily-report", "md-to-pdf"],
            "pdf": ["md-to-pdf", "daily-report"],
            "飞书": ["feishu-doc"],
            "天气": ["weather"],
            "安全": ["healthcheck"],
        }
        
        matched_skills = []
        for keyword, skill_keys in recommendations.items():
            if keyword in task_lower:
                for key in skill_keys:
                    if key in self.common_skills:
                        matched_skills.append({
                            "key": key,
                            **self.common_skills[key]
                        })
        
        # 去重
        seen = set()
        unique = []
        for s in matched_skills:
            if s['key'] not in seen:
                seen.add(s['key'])
                unique.append(s)
        
        return unique[:5]  # 最多返回5个

def print_skill(skill: Dict, show_command: bool = False):
    """打印技能信息"""
    status = "✅ 已安装" if skill['installed'] else "⬜ 未安装"
    print(f"\n📦 {skill['name']}")
    print(f"   描述: {skill['description']}")
    print(f"   类别: {skill['category']}")
    print(f"   状态: {status}")
    
    if show_command and not skill['installed']:
        finder = SkillFinder()
        cmd = finder.get_install_command(skill['key'])
        print(f"   安装: {cmd}")

def main():
    parser = argparse.ArgumentParser(
        description='Find Skills - 技能查找器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --search "汇率"           # 搜索汇率相关技能
  %(prog)s --search "market"         # 搜索市场数据技能
  %(prog)s --category 金融数据       # 按类别浏览
  %(prog)s --installed               # 列出已安装技能
  %(prog)s --recommend "量化交易"    # 任务推荐
  %(prog)s --list-all                # 列出所有技能
        """
    )
    
    parser.add_argument('--search', type=str, help='搜索技能')
    parser.add_argument('--category', type=str, help='按类别列出')
    parser.add_argument('--installed', action='store_true', help='列出已安装')
    parser.add_argument('--recommend', type=str, help='任务推荐')
    parser.add_argument('--list-all', action='store_true', help='列出所有')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔍 Find Skills - 技能查找器")
    print("=" * 60)
    
    finder = SkillFinder()
    
    if args.search:
        print(f"\n🔎 搜索: '{args.search}'")
        print("-" * 40)
        
        results = finder.search(args.search)
        if results:
            print(f"找到 {len(results)} 个相关技能:\n")
            for skill in results:
                print_skill(skill, show_command=True)
        else:
            print("❌ 未找到相关技能")
            print("\n💡 尝试其他关键词:")
            print("   - market (市场数据)")
            print("   - fx (外汇汇率)")
            print("   - risk (风险分析)")
            print("   - report (报告生成)")
            
    elif args.category:
        print(f"\n📂 类别: {args.category}")
        print("-" * 40)
        
        categories = finder.list_by_category(args.category)
        if args.category in categories and categories[args.category]:
            for skill in categories[args.category]:
                print_skill(skill, show_command=True)
        else:
            print("❌ 该类别暂无技能")
            print("\n可用类别:")
            all_cats = finder.list_by_category()
            for cat in all_cats.keys():
                print(f"   - {cat}")
                
    elif args.installed:
        print("\n✅ 已安装技能")
        print("-" * 40)
        
        installed = finder.list_installed()
        if installed:
            for skill in installed:
                print(f"\n📦 {skill['name']}")
                print(f"   {skill['description']}")
                print(f"   类别: {skill['category']}")
        else:
            print("暂无已安装技能")
            
    elif args.recommend:
        print(f"\n💡 任务: '{args.recommend}'")
        print("-" * 40)
        print("推荐技能:\n")
        
        recommendations = finder.recommend_for_task(args.recommend)
        if recommendations:
            for skill in recommendations:
                print_skill(skill, show_command=True)
        else:
            print("暂无特定推荐")
            print("\n尝试搜索:")
            print("   find-skills --search \"<关键词>\"")
            
    elif args.list_all:
        print("\n📚 所有可用技能")
        print("-" * 40)
        
        categories = finder.list_by_category()
        for cat, skills in categories.items():
            print(f"\n📂 {cat}")
            for skill in skills:
                status = "✅" if skill['installed'] else "⬜"
                print(f"   {status} {skill['name']}: {skill['description'][:40]}...")
    else:
        parser.print_help()
        print("\n" + "=" * 60)
        print("💡 快速开始:")
        print("=" * 60)
        print("\n1. 搜索技能:")
        print("   find-skills --search \"汇率\"")
        print("\n2. 查看已安装:")
        print("   find-skills --installed")
        print("\n3. 任务推荐:")
        print("   find-skills --recommend \"量化交易\"")
        print("\n4. 浏览所有:")
        print("   find-skills --list-all")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
