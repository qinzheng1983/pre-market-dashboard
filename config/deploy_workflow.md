# 部署工作流文档 v1.1（2026-05-12 更新）

## ⚠️ CRITICAL: Pages 构建失败根因（2026-05-12 确认）

**根因**：ec8c5b2（12个文件，构建成功）→ e4af766（378个文件，构建失败）。**文件数量过多导致 Pages legacy 构建系统超时/失败。**

**证据**：GitHub Pages builds API 返回所有 e4af766 之后的构建状态均为 `errored`，错误信息 `Page build failed.`。

**解决方案**：main 分支必须保持"干净"，只保留 Pages 需要的文件。工作文件（代码、报告、PDF、图片等）应保留在本地，不 push 到 main。

**Pages 必需文件清单（白名单）**：
- `index.html` — 导航页
- `dashboard.html` — 报告中心
- `finance-daily/*.html` — 财资日报历史
- `finance-weekly/*.html` — 财资周报历史
- `.nojekyll` — 禁用 Jekyll 构建
- `.gitignore` — 确保工作文件不被跟踪

**禁止推送到 main 的文件类型**：
- `.py` 脚本文件
- `.md` 工作文档（MEMORY.md, AGENTS.md 等）
- `.png/.jpg/.jpeg/.pdf` 媒体文件
- `.xlsx/.csv` 数据文件
- `venv/` 虚拟环境
- `__pycache__/` 缓存
- `.kimi/` `.openclaw/` 工作目录

**部署前检查清单**：
- [ ] `git ls-tree -r --name-only HEAD | wc -l` → 必须 < 50
- [ ] 如超过 50，先执行 `git rm --cached` 清理非 Pages 文件
- [ ] 确认 .gitignore 已包含所有工作文件目录

---

## 问题背景
之前部署时只更新了 index.html，未同步更新 dashboard.html（导航页），导致导航页显示过期信息。现建立明确工作流，确保每次部署完整性。

---

## GitHub 仓库结构

```
pre-market-dashboard/
├── index.html              ← 盘前市场简报（最新一期）
├── dashboard.html          ← 导航入口页（必须同步更新）
└── finance-daily/
    └── YYYYMMDD.html       ← 财资日报（按日期归档）
```

**Pages URL**: https://qinzheng1983.github.io/pre-market-dashboard/
**Token**: 请设置环境变量 `GITHUB_TOKEN`（不再硬编码于文件中，避免被GitHub Secret Scanning检测并revoke）

---

## 部署规则（强制执行）

### ⚠️ 分支一致性检查（2026-05-12 新增，强制）
**仓库默认分支为 `main`，GitHub Pages 构建源也是 `main` 分支。**

**每次部署前必须确认：**
1. 当前本地分支：`git branch` 应显示 `* main`
2. 远程默认分支：`git remote show origin` 确认 HEAD branch: main
3. 推送目标必须是 `main`：`git push origin main`

**绝对禁止推送到 `master` 分支**，master 分支不会被 Pages 构建。

**验证命令**：
```bash
git branch  # 必须显示 * main
git remote show origin | grep "HEAD branch"  # 必须显示 main
```

**如果当前在 master 分支**：
```bash
git checkout main
git merge master  # 可选：合并 master 的更改
git push origin main  # 必须推送到 main
```

---

## 部署步骤

### 1. 准备 HTML 文件
- 确保 `reports/finance_daily_YYYYMMDD.html` 已生成
- 复制到 `finance-daily/YYYYMMDD.html`

### 2. 更新导航页（必须同步！）
**每次部署财资日报时，必须同步更新 dashboard.html**：
```bash
cp templates/dashboard_index_template.html dashboard.html  # 或手动编辑
```

dashboard.html 必须包含：
- 最新一期盘前简报的链接
- 最新一期财资日报的链接
- 历史报告归档列表

### 3. 更新根目录 index.html
```bash
cp finance-daily/YYYYMMDD.html index.html  # 或其他方式
```

### 4. 提交并推送
```bash
git add index.html dashboard.html finance-daily/YYYYMMDD.html
git commit -m "Deploy 财资日报 YYYYMMDD + update dashboard"
git push origin main  # ← 必须是 main！
```

### 5. 验证
- 检查 Pages URL: https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html
- 确认所有链接可正常访问
- 检查 `finance-daily/YYYYMMDD.html` 可正常打开

---

## 自动化部署脚本

使用 `scripts/deploy_to_github.py` 或 `scripts/deploy_report.sh` 进行自动化部署。

**脚本已更新**：自动推送到 `main` 分支（不再推送到 master）。

---

## 历史问题记录

| 日期 | 问题 | 原因 | 解决方案 |
|------|------|------|----------|
| 2026-04-22 | 导航页未更新 | 只复制了 index.html，未更新 dashboard.html | 建立本工作流，强制同步更新 |
| 2026-05-12 | Pages 404 | 推送到 master 分支（非默认分支） | 强制推送到 main 分支 |
| 2026-05-12 | Pages 构建失败 | main 分支文件过多（378个），legacy 构建系统超时 | 清理 main 分支，只保留 Pages 必需文件 |

---

## 常见错误

### Error: 404 on Pages
- 检查是否推送到 main 分支
- 检查 GitHub Pages 设置中的构建源分支

### Error: Page build failed
- 检查文件数量：`git ls-tree -r --name-only HEAD | wc -l`
- 如超过 50，清理非 Pages 文件

### Error: Permission denied
- 检查 GITHUB_TOKEN 是否有仓库写入权限
- 检查 token 是否被 GitHub Secret Scanning revoke（硬编码 token 会被自动撤销）

---

*Last updated: 2026-05-12*
