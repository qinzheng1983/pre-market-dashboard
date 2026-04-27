#!/usr/bin/env python3
"""
Skill Vetter - OpenClaw 技能安全审查工具
Security-first skill vetting for AI agents

在安装任何技能之前检查安全风险：
- 权限范围分析
- 危险代码模式检测
- 拼写混淆攻击检测
- 元数据验证
"""

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

class RiskLevel(Enum):
    """风险等级"""
    SAFE = "SAFE"           # 🟢 安全
    LOW = "LOW"             # 🟡 低风险
    MEDIUM = "MEDIUM"       # 🟠 中风险
    HIGH = "HIGH"           # 🔴 高风险
    CRITICAL = "CRITICAL"   # ⛔ 严重风险 / BLOCK

@dataclass
class Finding:
    """审查发现"""
    severity: RiskLevel
    category: str
    description: str
    evidence: str
    recommendation: str

@dataclass
class VettingReport:
    """审查报告"""
    skill_name: str
    skill_path: str
    verdict: RiskLevel
    findings: List[Finding] = field(default_factory=list)
    permissions: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def add_finding(self, finding: Finding):
        """添加发现"""
        self.findings.append(finding)
        # 更新整体评级为最严重的
        if finding.severity.value < self.verdict.value:
            self.verdict = finding.severity

class SkillVetter:
    """技能审查器"""
    
    # 已知恶意模式
    CRITICAL_PATTERNS = [
        (r'curl\s+https?://[^\s\'"]+', 'curl 下载外部文件', '检查下载来源是否可信'),
        (r'wget\s+https?://[^\s\'"]+', 'wget 下载外部文件', '检查下载来源是否可信'),
        (r'nc\s+-[l]*\s*\d+', 'nc 网络连接命令', '可能用于反向 shell'),
        (r'bash\s+-i', '交互式 bash', '可能用于反向 shell'),
        (r'eval\s*\(', 'eval() 执行', '可能执行恶意代码'),
        (r'exec\s*\(', 'exec() 执行', '可能执行恶意代码'),
        (r'base64\s+-d', 'base64 解码', '可能隐藏恶意代码'),
        (r'python\s+-c\s*"', 'Python 内联代码', '检查代码内容'),
        (r'~/.ssh', '访问 SSH 密钥', '不应访问敏感凭证'),
        (r'~/.aws', '访问 AWS 凭证', '不应访问云凭证'),
        (r'~/.env', '访问环境变量文件', '不应访问敏感配置'),
        (r'MEMORY\.md', '访问记忆文件', '不应读取敏感记忆'),
        (r'USER\.md', '访问用户文件', '不应读取用户信息'),
        (r'IDENTITY\.md', '访问身份文件', '不应读取身份信息'),
        (r'SOUL\.md', '访问灵魂文件', '不应读取灵魂配置'),
        (r'cookie', '访问浏览器 Cookie', '不应访问会话凭证'),
        (r'sudo', '使用 sudo', '不应要求提权'),
    ]
    
    # 警告模式
    WARNING_PATTERNS = [
        (r'\*\*/\*', '通配符文件访问', '检查访问范围是否合理'),
        (r'/etc/', '访问系统配置', '不应修改系统文件'),
        (r'\.bashrc', '修改 bash 配置', '不应修改 shell 配置'),
        (r'\.zshrc', '修改 zsh 配置', '不应修改 shell 配置'),
        (r'crontab', '修改定时任务', '检查任务内容'),
        (r'ignore previous instructions', '提示注入攻击', '检测到提示注入'),
        (r'you are now', '身份覆盖攻击', '检测到身份劫持'),
        (r'system\s*=', '系统提示修改', '检测到系统提示修改'),
    ]
    
    # 拼写混淆检测 - 知名技能名称
    LEGITIMATE_SKILLS = [
        'git-commit-helper', 'github', 'web-search', 'tavily',
        'market-data-fetch', 'geopol-risk-dashboard', 'fx-geopol-forecast',
        'kalshi-trader', 'backtrader', 'akshare', 'multi-search-engine',
        'office-automation', 'self-improving-agent', 'find-skills',
        'md-to-pdf', 'daily-report', 'weather', 'healthcheck'
    ]
    
    def __init__(self):
        self.report = None
        
    def vet_skill(self, skill_path: str) -> VettingReport:
        """审查技能"""
        print(f"\n🔍 正在审查技能: {skill_path}")
        print("=" * 70)
        
        skill_file = Path(skill_path)
        if not skill_file.exists():
            print(f"❌ 技能文件不存在: {skill_path}")
            return None
        
        # 初始化报告
        self.report = VettingReport(
            skill_name=skill_file.stem,
            skill_path=str(skill_file.absolute()),
            verdict=RiskLevel.SAFE
        )
        
        # 读取技能内容
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return None
        
        # 执行审查步骤
        self._check_metadata(content)
        self._check_permissions(content)
        self._check_critical_patterns(content)
        self._check_warning_patterns(content)
        self._check_typosquatting(skill_file.stem)
        
        return self.report
    
    def _check_metadata(self, content: str):
        """步骤1: 元数据检查"""
        print("\n📋 步骤1: 元数据检查")
        
        # 检查是否有 name
        name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
        if name_match:
            self.report.metadata['name'] = name_match.group(1).strip()
        else:
            self.report.add_finding(Finding(
                severity=RiskLevel.LOW,
                category="Metadata",
                description="缺少 name 字段",
                evidence="未找到 name: 声明",
                recommendation="所有技能都应该有明确的名称"
            ))
        
        # 检查是否有 description
        desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
        if desc_match:
            self.report.metadata['description'] = desc_match.group(1).strip()
            # 检查描述是否清晰
            if len(desc_match.group(1).strip()) < 10:
                self.report.add_finding(Finding(
                    severity=RiskLevel.LOW,
                    category="Metadata",
                    description="描述过于简短",
                    evidence=f"描述: {desc_match.group(1).strip()}",
                    recommendation="提供清晰的技能功能描述"
                ))
        else:
            self.report.add_finding(Finding(
                severity=RiskLevel.LOW,
                category="Metadata",
                description="缺少 description 字段",
                evidence="未找到 description: 声明",
                recommendation="所有技能都应该有清晰的描述"
            ))
        
        # 检查是否有 version
        version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
        if version_match:
            self.report.metadata['version'] = version_match.group(1).strip()
        
        # 检查是否有 author
        author_match = re.search(r'^author:\s*(.+)$', content, re.MULTILINE)
        if author_match:
            self.report.metadata['author'] = author_match.group(1).strip()
        else:
            self.report.add_finding(Finding(
                severity=RiskLevel.LOW,
                category="Metadata",
                description="缺少 author 字段",
                evidence="未找到 author: 声明",
                recommendation="应提供作者信息以便追溯"
            ))
        
        print(f"   ✅ 名称: {self.report.metadata.get('name', 'Unknown')}")
        print(f"   ✅ 描述: {self.report.metadata.get('description', 'Unknown')[:50]}...")
    
    def _check_permissions(self, content: str):
        """步骤2: 权限范围分析"""
        print("\n🔐 步骤2: 权限范围分析")
        
        # 检查权限声明
        permissions = {
            'fileRead': False,
            'fileWrite': False,
            'network': False,
            'shell': False
        }
        
        # 检查 fileRead
        if re.search(r'read|fileRead|open\s*\(', content, re.IGNORECASE):
            permissions['fileRead'] = True
            self.report.permissions['fileRead'] = 'GRANTED'
            print(f"   🟢 fileRead: GRANTED — 读取文件权限")
        
        # 检查 fileWrite
        if re.search(r'write|fileWrite|save|\.write\(|\.save\(', content, re.IGNORECASE):
            permissions['fileWrite'] = True
            self.report.permissions['fileWrite'] = 'GRANTED'
            print(f"   🟡 fileWrite: GRANTED — 写入文件权限")
            self.report.add_finding(Finding(
                severity=RiskLevel.LOW,
                category="Permissions",
                description="请求文件写入权限",
                evidence="检测到 write/fileWrite 操作",
                recommendation="确认写入范围和必要性"
            ))
        
        # 检查 network
        if re.search(r'http|https|request|curl|wget|fetch|api', content, re.IGNORECASE):
            permissions['network'] = True
            self.report.permissions['network'] = 'GRANTED'
            print(f"   🟠 network: GRANTED — 网络访问权限")
            self.report.add_finding(Finding(
                severity=RiskLevel.MEDIUM,
                category="Permissions",
                description="请求网络访问权限",
                evidence="检测到 HTTP/网络相关操作",
                recommendation="确认访问的端点和必要性，防止数据外泄"
            ))
        
        # 检查 shell
        if re.search(r'shell|subprocess|os\.system|exec|spawn', content, re.IGNORECASE):
            permissions['shell'] = True
            self.report.permissions['shell'] = 'GRANTED'
            print(f"   🔴 shell: GRANTED — 执行命令权限 ⚠️")
            self.report.add_finding(Finding(
                severity=RiskLevel.HIGH,
                category="Permissions",
                description="请求 Shell 执行权限",
                evidence="检测到 shell/subsystem/exec 操作",
                recommendation="高危权限！确认执行的命令和必要性"
            ))
        
        # 检查网络 + Shell 组合 (高危)
        if permissions['network'] and permissions['shell']:
            self.report.add_finding(Finding(
                severity=RiskLevel.CRITICAL,
                category="Permissions",
                description="网络 + Shell 权限组合",
                evidence="同时具备 network 和 shell 权限",
                recommendation="⛔ 严重风险！此组合可实现数据外泄，必须人工审核"
            ))
        
        if not any(permissions.values()):
            print(f"   🟢 无特殊权限请求 — 最小权限原则")
    
    def _check_critical_patterns(self, content: str):
        """步骤3: 关键模式检查"""
        print("\n🚨 步骤3: 危险模式检测")
        
        found_count = 0
        for pattern, desc, recommendation in self.CRITICAL_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                found_count += 1
                # 获取上下文
                start = max(0, match.start() - 30)
                end = min(len(content), match.end() + 30)
                context = content[start:end].replace('\n', ' ')
                
                self.report.add_finding(Finding(
                    severity=RiskLevel.CRITICAL,
                    category="Critical Pattern",
                    description=desc,
                    evidence=f"...{context}...",
                    recommendation=recommendation
                ))
                print(f"   ⛔ CRITICAL: {desc}")
        
        if found_count == 0:
            print(f"   ✅ 未检测到危险模式")
        else:
            print(f"   ⚠️  发现 {found_count} 个危险模式")
    
    def _check_warning_patterns(self, content: str):
        """步骤4: 警告模式检查"""
        print("\n⚠️  步骤4: 警告模式检测")
        
        found_count = 0
        for pattern, desc, recommendation in self.WARNING_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                found_count += 1
                start = max(0, match.start() - 20)
                end = min(len(content), match.end() + 20)
                context = content[start:end].replace('\n', ' ')
                
                self.report.add_finding(Finding(
                    severity=RiskLevel.MEDIUM,
                    category="Warning Pattern",
                    description=desc,
                    evidence=f"...{context}...",
                    recommendation=recommendation
                ))
                print(f"   🟠 WARNING: {desc}")
        
        if found_count == 0:
            print(f"   ✅ 未检测到警告模式")
    
    def _check_typosquatting(self, skill_name: str):
        """步骤5: 拼写混淆检测"""
        print("\n🔤 步骤5: 拼写混淆检测")
        
        for legit_skill in self.LEGITIMATE_SKILLS:
            # 检查是否是拼写混淆
            if self._is_typosquat(skill_name, legit_skill):
                self.report.add_finding(Finding(
                    severity=RiskLevel.CRITICAL,
                    category="Typosquatting",
                    description=f"可能是 '{legit_skill}' 的拼写混淆",
                    evidence=f"{skill_name} vs {legit_skill}",
                    recommendation="⛔ 拒绝安装！这可能是钓鱼攻击"
                ))
                print(f"   ⛔ TYPOQUATTING: {skill_name} vs {legit_skill}")
                return
        
        print(f"   ✅ 未发现拼写混淆")
    
    def _is_typosquat(self, name1: str, name2: str) -> bool:
        """检测拼写混淆"""
        if name1 == name2:
            return False
        
        # 忽略大小写和分隔符
        n1 = name1.lower().replace('-', '').replace('_', '')
        n2 = name2.lower().replace('-', '').replace('_', '')
        
        # 如果完全相同
        if n1 == n2:
            return False
        
        # 检查编辑距离
        if len(n1) > 3 and len(n2) > 3:
            # 简单检查：字符差异
            if abs(len(n1) - len(n2)) <= 1:
                diff = sum(1 for a, b in zip(n1, n2) if a != b)
                if diff <= 2:
                    return True
        
        return False
    
    def print_report(self):
        """打印审查报告"""
        if not self.report:
            return
        
        print("\n" + "=" * 70)
        print("📊 SKILL VETTING REPORT")
        print("=" * 70)
        
        # 基本信息
        print(f"\n技能名称: {self.report.skill_name}")
        print(f"技能路径: {self.report.skill_path}")
        print(f"版本: {self.report.metadata.get('version', 'Unknown')}")
        print(f"作者: {self.report.metadata.get('author', 'Unknown')}")
        
        # 裁决
        verdict_emoji = {
            RiskLevel.SAFE: "🟢",
            RiskLevel.LOW: "🟡",
            RiskLevel.MEDIUM: "🟠",
            RiskLevel.HIGH: "🔴",
            RiskLevel.CRITICAL: "⛔"
        }
        print(f"\n{'=' * 70}")
        print(f"裁决: {verdict_emoji.get(self.report.verdict, '❓')} {self.report.verdict.value}")
        print(f"{'=' * 70}")
        
        # 权限
        print("\n权限请求:")
        for perm, status in self.report.permissions.items():
            print(f"  {perm}: {status}")
        
        # 发现
        if self.report.findings:
            print(f"\n发现 {len(self.report.findings)} 个问题:")
            for i, finding in enumerate(self.report.findings, 1):
                emoji = {
                    RiskLevel.CRITICAL: "⛔",
                    RiskLevel.HIGH: "🔴",
                    RiskLevel.MEDIUM: "🟠",
                    RiskLevel.LOW: "🟡"
                }.get(finding.severity, "⚪")
                
                print(f"\n{i}. {emoji} [{finding.severity.value}] {finding.category}")
                print(f"   描述: {finding.description}")
                print(f"   证据: {finding.evidence}")
                print(f"   建议: {finding.recommendation}")
        else:
            print("\n✅ 未发现安全问题")
        
        # 建议
        print(f"\n{'=' * 70}")
        if self.report.verdict == RiskLevel.SAFE:
            print("✅ 建议: 可以安全安装")
        elif self.report.verdict == RiskLevel.LOW:
            print("🟡 建议: 低风险，可以安装但请注意警告")
        elif self.report.verdict == RiskLevel.MEDIUM:
            print("🟠 建议: 中风险，请仔细审查后决定是否安装")
        elif self.report.verdict == RiskLevel.HIGH:
            print("🔴 建议: 高风险，建议不要安装或进行深度审计")
        elif self.report.verdict == RiskLevel.CRITICAL:
            print("⛔ 建议: 严重风险，强烈建议拒绝安装！")
        print(f"{'=' * 70}")

def scan_installed_skills(skills_dir: str = "/root/.openclaw/workspace/skills"):
    """扫描已安装的技能"""
    print("=" * 70)
    print("🔍 扫描已安装技能")
    print("=" * 70)
    
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        print(f"❌ 技能目录不存在: {skills_dir}")
        return
    
    vetter = SkillVetter()
    total = 0
    safe = 0
    risky = 0
    
    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                total += 1
                report = vetter.vet_skill(str(skill_file))
                if report:
                    if report.verdict in [RiskLevel.SAFE, RiskLevel.LOW]:
                        safe += 1
                    else:
                        risky += 1
                    print(f"\n{'-' * 70}")
    
    print(f"\n{'=' * 70}")
    print("扫描完成:")
    print(f"   总计: {total} 个技能")
    print(f"   ✅ 安全: {safe} 个")
    print(f"   ⚠️  风险: {risky} 个")
    print(f"{'=' * 70}")

def main():
    parser = argparse.ArgumentParser(
        description='Skill Vetter - OpenClaw 技能安全审查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 审查单个技能
  skill_vetter.py /path/to/skill/SKILL.md
  
  # 扫描所有已安装技能
  skill_vetter.py --scan
  
  # 详细输出
  skill_vetter.py skill.md --verbose

安全建议:
  1. 所有新技能安装前必须审查
  2. 高风险技能需要人工复核
  3. 定期重新扫描已安装技能
  4. 只从可信来源安装技能
        """
    )
    
    parser.add_argument('skill', nargs='?', help='要审查的技能文件路径')
    parser.add_argument('--scan', action='store_true', help='扫描所有已安装技能')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🔒 Skill Vetter - OpenClaw 技能安全审查工具")
    print("=" * 70)
    
    if args.scan:
        scan_installed_skills()
    elif args.skill:
        vetter = SkillVetter()
        report = vetter.vet_skill(args.skill)
        if report:
            vetter.print_report()
    else:
        parser.print_help()
        print("\n" + "=" * 70)
        print("💡 安全提示:")
        print("=" * 70)
        print("\n在安装任何技能之前，请使用本工具进行安全审查。")
        print("已知约 1,200 个 ClawHub 技能曾被发现包含恶意代码。")
        print("\n推荐工作流程:")
        print("   1. 发现感兴趣的技能")
        print("   2. 使用 skill-vetter 审查")
        print("   3. 通过审查后安装")
        print("   4. 定期重新扫描")

if __name__ == "__main__":
    main()
