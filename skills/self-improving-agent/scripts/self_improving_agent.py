#!/usr/bin/env python3
"""
Self Improving Agent - 自改进 Agent 系统
实现反思、学习、优化机制，持续提升 Agent 性能
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

class ReflectionEngine:
    """反思引擎 - 分析对话和决策"""
    
    def __init__(self, memory_dir: str = "/root/.openclaw/workspace/memory"):
        self.memory_dir = Path(memory_dir)
        self.reflections_file = self.memory_dir / "reflections.json"
        self.reflections = self._load_reflections()
        
    def _load_reflections(self) -> List[Dict]:
        """加载历史反思"""
        if self.reflections_file.exists():
            with open(self.reflections_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_reflections(self):
        """保存反思"""
        with open(self.reflections_file, 'w', encoding='utf-8') as f:
            json.dump(self.reflections, f, indent=2, ensure_ascii=False)
    
    def add_reflection(self, context: str, action: str, outcome: str, 
                      lesson: str, improvement: str):
        """添加反思记录"""
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'action': action,
            'outcome': outcome,
            'lesson': lesson,
            'improvement': improvement
        }
        self.reflections.append(reflection)
        self._save_reflections()
        return reflection
    
    def get_recent_reflections(self, days: int = 7) -> List[Dict]:
        """获取最近的反思"""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            r for r in self.reflections 
            if datetime.fromisoformat(r['timestamp']) > cutoff
        ]
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """分析反思模式"""
        if not self.reflections:
            return {'status': 'no_data'}
        
        # 统计改进领域
        improvements = {}
        for r in self.reflections:
            imp = r.get('improvement', '')
            if imp:
                improvements[imp] = improvements.get(imp, 0) + 1
        
        # 统计教训类型
        lessons = {}
        for r in self.reflections:
            lesson = r.get('lesson', '')
            if lesson:
                lessons[lesson] = lessons.get(lesson, 0) + 1
        
        return {
            'total_reflections': len(self.reflections),
            'recent_7d': len(self.get_recent_reflections(7)),
            'top_improvements': sorted(improvements.items(), key=lambda x: x[1], reverse=True)[:5],
            'top_lessons': sorted(lessons.items(), key=lambda x: x[1], reverse=True)[:5]
        }

class LearningEngine:
    """学习引擎 - 从经验中提取知识"""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.memory_file = self.workspace / "MEMORY.md"
        self.learning_file = self.workspace / "memory" / "learnings.json"
        self.learnings = self._load_learnings()
        
    def _load_learnings(self) -> Dict:
        """加载学习记录"""
        if self.learning_file.exists():
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'skills_learned': [],
            'mistakes_avoided': [],
            'best_practices': [],
            'user_preferences': {}
        }
    
    def _save_learnings(self):
        """保存学习记录"""
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learnings, f, indent=2, ensure_ascii=False)
    
    def learn_skill(self, skill_name: str, proficiency: int, notes: str):
        """记录技能学习"""
        skill = {
            'name': skill_name,
            'proficiency': proficiency,  # 1-10
            'learned_at': datetime.now().isoformat(),
            'notes': notes
        }
        # 更新或添加
        existing = [s for s in self.learnings['skills_learned'] if s['name'] == skill_name]
        if existing:
            existing[0].update(skill)
        else:
            self.learnings['skills_learned'].append(skill)
        self._save_learnings()
    
    def record_mistake(self, mistake: str, context: str, prevention: str):
        """记录错误和避免方法"""
        self.learnings['mistakes_avoided'].append({
            'mistake': mistake,
            'context': context,
            'prevention': prevention,
            'recorded_at': datetime.now().isoformat()
        })
        self._save_learnings()
    
    def add_best_practice(self, practice: str, category: str, context: str):
        """添加最佳实践"""
        self.learnings['best_practices'].append({
            'practice': practice,
            'category': category,
            'context': context,
            'added_at': datetime.now().isoformat()
        })
        self._save_learnings()
    
    def record_preference(self, key: str, value: Any, confidence: float = 0.5):
        """记录用户偏好"""
        self.learnings['user_preferences'][key] = {
            'value': value,
            'confidence': confidence,
            'updated_at': datetime.now().isoformat()
        }
        self._save_learnings()
    
    def get_learning_summary(self) -> Dict:
        """获取学习摘要"""
        return {
            'skills_count': len(self.learnings['skills_learned']),
            'mistakes_recorded': len(self.learnings['mistakes_avoided']),
            'best_practices': len(self.learnings['best_practices']),
            'preferences_known': len(self.learnings['user_preferences']),
            'top_skills': sorted(
                self.learnings['skills_learned'],
                key=lambda x: x.get('proficiency', 0),
                reverse=True
            )[:5]
        }

class OptimizationEngine:
    """优化引擎 - 改进工作方式"""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.optimizations_file = self.workspace / "memory" / "optimizations.json"
        self.optimizations = self._load_optimizations()
        
    def _load_optimizations(self) -> List[Dict]:
        """加载优化记录"""
        if self.optimizations_file.exists():
            with open(self.optimizations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_optimizations(self):
        """保存优化记录"""
        self.optimizations_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.optimizations_file, 'w', encoding='utf-8') as f:
            json.dump(self.optimizations, f, indent=2, ensure_ascii=False)
    
    def suggest_optimization(self, area: str, current: str, suggested: str, 
                           benefit: str) -> Dict:
        """建议优化"""
        opt = {
            'timestamp': datetime.now().isoformat(),
            'area': area,
            'current_approach': current,
            'suggested_approach': suggested,
            'expected_benefit': benefit,
            'implemented': False
        }
        self.optimizations.append(opt)
        self._save_optimizations()
        return opt
    
    def mark_implemented(self, index: int, result: str):
        """标记优化已实施"""
        if 0 <= index < len(self.optimizations):
            self.optimizations[index]['implemented'] = True
            self.optimizations[index]['implementation_result'] = result
            self.optimizations[index]['implemented_at'] = datetime.now().isoformat()
            self._save_optimizations()
    
    def get_pending_optimizations(self) -> List[Dict]:
        """获取待实施的优化"""
        return [o for o in self.optimizations if not o.get('implemented')]
    
    def get_optimization_stats(self) -> Dict:
        """获取优化统计"""
        total = len(self.optimizations)
        implemented = len([o for o in self.optimizations if o.get('implemented')])
        pending = total - implemented
        
        return {
            'total_suggested': total,
            'implemented': implemented,
            'pending': pending,
            'implementation_rate': implemented / total if total > 0 else 0
        }

class SelfImprovingAgent:
    """自改进 Agent 主类"""
    
    def __init__(self):
        self.reflection = ReflectionEngine()
        self.learning = LearningEngine()
        self.optimization = OptimizationEngine()
        
    def reflect(self, context: str, action: str, outcome: str, 
               lesson: str, improvement: str):
        """进行反思"""
        return self.reflection.add_reflection(context, action, outcome, 
                                             lesson, improvement)
    
    def learn(self, skill_name: str = None, proficiency: int = None, 
             notes: str = None, mistake: str = None, practice: str = None):
        """学习新知识"""
        if skill_name:
            self.learning.learn_skill(skill_name, proficiency or 5, notes or "")
        if mistake:
            self.learning.record_mistake(mistake, notes or "", "")
        if practice:
            self.learning.add_best_practice(practice, "general", notes or "")
    
    def suggest_improvement(self, area: str, current: str, 
                           suggested: str, benefit: str):
        """建议改进"""
        return self.optimization.suggest_optimization(area, current, 
                                                     suggested, benefit)
    
    def get_status_report(self) -> Dict:
        """获取状态报告"""
        return {
            'reflection': self.reflection.analyze_patterns(),
            'learning': self.learning.get_learning_summary(),
            'optimization': self.optimization.get_optimization_stats(),
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_improvement_plan(self) -> str:
        """生成改进计划"""
        report = self.get_status_report()
        
        plan = []
        plan.append("# 自改进计划")
        plan.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 反思部分
        plan.append("\n## 1. 反思分析")
        ref = report['reflection']
        if ref.get('status') == 'no_data':
            plan.append("暂无反思数据。建议开始记录每次重要决策的反思。")
        else:
            plan.append(f"- 总反思数: {ref['total_reflections']}")
            plan.append(f"- 最近7天: {ref['recent_7d']}")
            if ref.get('top_improvements'):
                plan.append("- 主要改进领域:")
                for imp, count in ref['top_improvements']:
                    plan.append(f"  - {imp}: {count}次")
        
        # 学习部分
        plan.append("\n## 2. 学习进度")
        learn = report['learning']
        plan.append(f"- 已掌握技能: {learn['skills_count']}")
        plan.append(f"- 记录的错误: {learn['mistakes_recorded']}")
        plan.append(f"- 最佳实践: {learn['best_practices']}")
        plan.append(f"- 用户偏好: {learn['preferences_known']}")
        
        if learn.get('top_skills'):
            plan.append("- 熟练技能:")
            for skill in learn['top_skills']:
                plan.append(f"  - {skill['name']} (熟练度: {skill['proficiency']}/10)")
        
        # 优化部分
        plan.append("\n## 3. 优化状态")
        opt = report['optimization']
        plan.append(f"- 建议优化: {opt['total_suggested']}")
        plan.append(f"- 已实施: {opt['implemented']}")
        plan.append(f"- 待实施: {opt['pending']}")
        plan.append(f"- 实施率: {opt['implementation_rate']*100:.1f}%")
        
        # 行动计划
        plan.append("\n## 4. 建议行动")
        pending_opts = self.optimization.get_pending_optimizations()
        if pending_opts:
            plan.append(f"\n有待实施的优化建议 ({len(pending_opts)}项):")
            for i, opt in enumerate(pending_opts[:3], 1):
                plan.append(f"\n{i}. **{opt['area']}**")
                plan.append(f"   - 当前: {opt['current_approach']}")
                plan.append(f"   - 建议: {opt['suggested_approach']}")
                plan.append(f"   - 收益: {opt['expected_benefit']}")
        else:
            plan.append("\n暂无待实施的优化建议。")
        
        return "\n".join(plan)

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Self Improving Agent')
    parser.add_argument('command', choices=[
        'status', 'reflect', 'learn', 'optimize', 'plan', 'demo'
    ], help='命令')
    
    args = parser.parse_args()
    
    agent = SelfImprovingAgent()
    
    if args.command == 'status':
        print("=" * 60)
        print("🧠 Self Improving Agent - 状态报告")
        print("=" * 60)
        
        report = agent.get_status_report()
        
        print("\n📊 反思分析:")
        print(f"   总反思数: {report['reflection'].get('total_reflections', 0)}")
        print(f"   最近7天: {report['reflection'].get('recent_7d', 0)}")
        
        print("\n📚 学习进度:")
        learn = report['learning']
        print(f"   技能: {learn['skills_count']}")
        print(f"   错误记录: {learn['mistakes_recorded']}")
        print(f"   最佳实践: {learn['best_practices']}")
        
        print("\n⚡ 优化状态:")
        opt = report['optimization']
        print(f"   建议: {opt['total_suggested']}")
        print(f"   已实施: {opt['implemented']}")
        print(f"   实施率: {opt['implementation_rate']*100:.1f}%")
        
    elif args.command == 'reflect':
        # 演示反思
        agent.reflect(
            context="处理中东风险报告",
            action="使用单一数据源",
            outcome="信息不够全面",
            lesson="多源验证可以提高准确性",
            improvement="使用 multi-search-engine 进行多源搜索"
        )
        print("✅ 已添加反思记录")
        
    elif args.command == 'learn':
        # 演示学习
        agent.learn(
            skill_name="汇率预测",
            proficiency=7,
            notes="已掌握地缘风险与汇率关联分析"
        )
        print("✅ 已记录学习进度")
        
    elif args.command == 'optimize':
        # 演示优化建议
        agent.suggest_improvement(
            area="数据获取",
            current="手动执行多个命令",
            suggested="创建自动化工作流脚本",
            benefit="提高效率，减少人为错误"
        )
        print("✅ 已添加优化建议")
        
    elif args.command == 'plan':
        print(agent.generate_improvement_plan())
        
    elif args.command == 'demo':
        print("=" * 60)
        print("🧠 Self Improving Agent - 演示")
        print("=" * 60)
        
        # 添加一些示例数据
        agent.reflect(
            context="生成汇率报告",
            action="手动搜索数据",
            outcome="耗时较长，数据不够全面",
            lesson="应该使用自动化的数据获取工具",
            improvement="集成 market-data-fetch 和 multi-search-engine"
        )
        
        agent.learn(
            skill_name="地缘风险分析",
            proficiency=8,
            notes="能够综合分析地缘风险对汇率的影响"
        )
        
        agent.learn(
            skill_name="kalshi-trader",
            proficiency=6,
            notes="了解预测市场数据的使用方法"
        )
        
        agent.suggest_improvement(
            area="报告生成",
            current="手动整理数据到报告",
            suggested="自动化数据整合和可视化",
            benefit="节省 50% 报告生成时间"
        )
        
        print("\n✅ 已生成示例数据")
        print("\n查看状态:")
        print(agent.generate_improvement_plan())

if __name__ == "__main__":
    main()
