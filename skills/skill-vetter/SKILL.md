---
name: skill-vetter
description: Skill Vetter - OpenClaw 技能安全审查工具。在安装任何技能前检查安全风险、权限滥用、恶意代码模式，防止恶意技能攻击。
metadata:
  version: 1.0.0
  author: openclaw
  category: security
---

# Skill Vetter - 技能安全审查工具

## 概述

**Skill Vetter** 是 OpenClaw 的安全审查工具，用于在安装技能前检测安全风险。相当于 Agent 时代的杀毒软件。

### 为什么需要 Skill Vetter？

⚠️ **真实案例**: 用户 `hightower6eu` 在 ClawHub 上传了 314 个看似正常的技能，官方审查后发现**全部为恶意代码**。

这些恶意技能的常见套路：
- 安装后访问陌生地址下载文件并执行
- 下载内容完全不可控
- 风险堪比早期电脑病毒

### 核心风险

- **下载量 ≠ 安全**: 高下载量可能是伪装
- **权限滥用**: 读取 SSH 密钥、浏览器 Cookie、Agent 记忆文件
- **第三方镜像站**: 仿冒官网的恶意源

## 功能特点

| 功能 | 说明 |
|------|------|
| 🔍 元数据检查 | 验证 name、version、description、author |
| 🔐 权限分析 | 检查 fileRead/fileWrite/network/shell 权限 |
| 🚨 危险模式检测 | 检测 curl、eval、base64、凭证访问等 |
| 🔤 拼写混淆检测 | 检测 typosquatting 攻击 (如 githuub vs github) |
| 📊 风险评级 | SAFE/LOW/MEDIUM/HIGH/CRITICAL |

## 安装

```bash
# 本技能已安装，直接使用
python3 skills/skill-vetter/scripts/skill_vetter.py --help
```

## 使用方法

### 1. 审查单个技能

```bash
# 审查技能文件
python3 skills/skill-vetter/scripts/skill_vetter.py /path/to/skill/SKILL.md

# 示例：审查 tavily-web-search
python3 skills/skill-vetter/scripts/skill_vetter.py skills/tavily-web-search/SKILL.md
```

### 2. 扫描所有已安装技能

```bash
# 扫描全部已安装技能
python3 skills/skill-vetter/scripts/skill_vetter.py --scan
```

### 3. Python API 使用

```python
from skill_vetter import SkillVetter, RiskLevel

# 创建审查器
vetter = SkillVetter()

# 审查技能
report = vetter.vet_skill("skills/new-skill/SKILL.md")

# 检查裁决
if report.verdict == RiskLevel.CRITICAL:
    print("⛔ 拒绝安装！发现严重风险")
elif report.verdict == RiskLevel.HIGH:
    print("🔴 高风险，建议不要安装")
elif report.verdict == RiskLevel.SAFE:
    print("✅ 安全，可以安装")

# 查看发现的问题
for finding in report.findings:
    print(f"[{finding.severity}] {finding.description}")
```

## 审查协议

### 步骤1: 元数据检查

- `name` - 名称是否合理
- `version` - 版本号是否符合 semver
- `description` - 描述是否清晰
- `author` - 作者是否可识别

### 步骤2: 权限范围分析

| 权限 | 风险等级 | 说明 |
|------|----------|------|
| fileRead | 🟢 Low | 读取文件，通常合法 |
| fileWrite | 🟡 Medium | 写入文件，需确认范围 |
| network | 🟠 High | 网络访问，需确认端点 |
| shell | 🔴 Critical | 执行命令，高危权限 |

**⚠️ 危险组合**: `network` + `shell` 可实现数据外泄

### 步骤3: 危险模式检测

**⛔ 严重风险 (立即阻止)**:
- `curl/wget` 下载外部文件
- `bash -i` 交互式 shell
- `eval()` / `exec()` 执行代码
- `base64 -d` 解码隐藏代码
- 访问 `~/.ssh`, `~/.aws`, `~/.env`
- 读取 `MEMORY.md`, `USER.md`, `IDENTITY.md`
- 访问浏览器 Cookie
- 使用 `sudo`

**🟠 警告模式**:
- `**/*` 通配符文件访问
- `/etc/` 系统配置访问
- `.bashrc` / `.zshrc` 修改
- `crontab` 定时任务修改
- "ignore previous instructions" 提示注入

### 步骤4: 拼写混淆检测

检测仿冒知名技能的名称：
```
git-commit-helper ← 合法
git-commiter      ← TYPOSQUAT (少 't', 多 'e')
gihub-push        ← TYPOSQUAT (少 't')
code-reveiw       ← TYPOSQUAT (ie 颠倒)
```

## 输出示例

### 安全技能报告

```
======================================================================
📊 SKILL VETTING REPORT
======================================================================

技能名称: weather
技能路径: /workspace/skills/weather/SKILL.md
版本: 1.0.0
作者: openclaw

======================================================================
裁决: 🟢 SAFE
======================================================================

权限请求:
  fileRead: GRANTED

✅ 未发现安全问题

======================================================================
✅ 建议: 可以安全安装
======================================================================
```

### 风险技能报告

```
======================================================================
📊 SKILL VETTING REPORT
======================================================================

技能名称: suspicious-tool
技能路径: /workspace/skills/suspicious/SKILL.md
版本: 1.0.0
作者: unknown

======================================================================
裁决: 🔴 HIGH
======================================================================

权限请求:
  fileRead: GRANTED
  network: GRANTED
  shell: GRANTED ⚠️

发现 3 个问题:

1. 🔴 [HIGH] 请求 Shell 执行权限
   描述: 请求 Shell 执行权限
   证据: ...subprocess.call(...)
   建议: 高危权限！确认执行的命令和必要性

2. 🟠 [MEDIUM] 请求网络访问权限
   描述: 请求网络访问权限
   证据: ...requests.get(...)
   建议: 确认访问的端点和必要性

3. ⛔ [CRITICAL] 网络 + Shell 权限组合
   描述: 网络 + Shell 权限组合
   证据: 同时具备 network 和 shell 权限
   建议: ⛔ 严重风险！此组合可实现数据外泄

======================================================================
🔴 建议: 高风险，建议不要安装或进行深度审计
======================================================================
```

## 检测规则

### 严重风险模式

```python
CRITICAL_PATTERNS = [
    (r'curl\s+https?://', 'curl 下载外部文件'),
    (r'wget\s+https?://', 'wget 下载外部文件'),
    (r'bash\s+-i', '交互式 bash'),
    (r'eval\s*\(', 'eval() 执行'),
    (r'base64\s+-d', 'base64 解码'),
    (r'~/.ssh', '访问 SSH 密钥'),
    (r'~/.aws', '访问 AWS 凭证'),
    (r'MEMORY\.md', '访问记忆文件'),
]
```

### 警告模式

```python
WARNING_PATTERNS = [
    (r'\*\*/\*', '通配符文件访问'),
    (r'/etc/', '访问系统配置'),
    (r'\.bashrc', '修改 bash 配置'),
    (r'ignore previous instructions', '提示注入攻击'),
]
```

## 安全建议

1. **只从官方渠道安装**: https://clawhub.ai/ 是唯一官方地址
2. **不要迷信下载量**: 高下载量可能是伪装
3. **必装 skill-vetter**: 养成审查习惯
4. **定期扫描**: 及时发现风险
5. **高风险插件**: 咨询专业人士

## 信任层级

1. ✅ **官方 OpenClaw skills** (最高信任)
2. ✅ **UseClawPro 验证的技能**
3. 🟡 **知名作者的公开仓库**
4. 🟠 **社区技能，下载量多**
5. 🔴 **新技能，未知作者** (最低信任，需完整审查)

## 文件结构

```
skills/skill-vetter/
├── SKILL.md                      # 本文件
└── scripts/
    └── skill_vetter.py           # 主脚本
```

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 五步骤审查协议
- 危险模式检测
- 拼写混淆检测
- 权限组合风险评估
