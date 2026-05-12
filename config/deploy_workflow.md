# 部署工作流文档 v1.0（2026-04-22 建立）

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

### 规则1：盘前简报部署
**触发条件**：每日08:30前生成新盘前简报后

**必须执行的三步**：
1. ✅ 上传/更新 `index.html`（盘前简报正文）
2. ✅ **同步更新 `dashboard.html` 导航页** — 修改"盘前市场简报"卡片：日期、标题、描述
3. ✅ **确认推送到 `main` 分支**（`git push origin main`）
4. ✅ 验证导航页链接可正常访问

**禁止行为**：只更新 index.html 不更新 dashboard.html

### 规则2：财资日报部署
**触发条件**：每日16:00后生成新财资日报后

**必须执行的四步**：
1. ✅ 上传新文件到 `finance-daily/YYYYMMDD.html`
2. ✅ **同步更新 `dashboard.html` 导航页** — 修改"财资日报"卡片：日期、标题、描述、链接
3. ✅ **确认推送到 `main` 分支**（`git push origin main`）
4. ✅ **验证文件可访问**：`curl -sI "https://qinzheng1983.github.io/pre-market-dashboard/finance-daily/YYYYMMDD.html"` 必须返回 200

**禁止行为**：只上传财资日报不更新导航页

### 规则3：导航页展示规则（来自USER.md）
- **仅展示最新一期**：导航页只保留最新一期盘前简报 + 最新一期财资日报
- **不展示多期历史列表**：保持页面清爽
- **历史报告保留**：虽然导航页不展示，但历史报告文件仍保留在仓库中，可通过直接URL访问
- **当日报告显示"最新" badge**

---

## 部署检查清单（每次部署前执行）

### 盘前简报部署检查清单
```
□ 当前在 main 分支：git branch 显示 * main
□ 盘前简报 HTML 文件已生成并验证内容
□ 文件路径：reports/pre_market_briefing_YYYYMMDD.html
□ 执行部署脚本或手动上传 index.html
□ 更新 dashboard.html 导航页（日期/标题/描述）
□ 上传 dashboard.html
□ 推送到 main 分支：git push origin main
□ 验证 https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html 显示正确
□ 验证导航页点击"盘前市场简报"跳转正常
□ 记录部署到 memory/YYYYMMDD.md
```

### 财资日报部署检查清单
```
□ 当前在 main 分支：git branch 显示 * main
□ 财资日报 HTML 文件已生成并验证内容
□ 文件路径：reports/finance_daily_YYYYMMDD.html
□ 上传 finance-daily/YYYYMMDD.html
□ 更新 dashboard.html 导航页（日期/标题/描述/链接）
□ 上传 dashboard.html
□ 推送到 main 分支：git push origin main
□ 验证 https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html 显示正确
□ 验证导航页点击"财资日报"跳转正常
□ 验证 finance-daily/YYYYMMDD.html 直接URL返回200
□ 记录部署到 memory/YYYYMMDD.md
```

---

## 自动化脚本

### 使用 scripts/deploy_report.sh（推荐）
```bash
# 部署盘前简报
./scripts/deploy_report.sh pre-market YYYYMMDD

# 部署财资日报
./scripts/deploy_report.sh finance-daily YYYYMMDD
```

脚本会自动：
1. 读取本地报告文件
2. 上传到正确位置（index.html 或 finance-daily/YYYYMMDD.html）
3. 自动更新 dashboard.html 导航页
4. 上传更新后的导航页
5. 输出部署状态

### 手动部署命令（备用）
见 MEMORY.md 中 "GitHub 部署配置" 部分的 curl 命令模板。

---

## 验证方法

部署后必须验证以下URL：
1. https://qinzheng1983.github.io/pre-market-dashboard/dashboard.html（导航页）
2. https://qinzheng1983.github.io/pre-market-dashboard/index.html（盘前简报）
3. https://qinzheng1983.github.io/pre-market-dashboard/finance-daily/YYYYMMDD.html（财资日报）

---

## 历史问题记录

| 日期 | 问题 | 原因 | 解决 |
|------|------|------|------|
| 2026-05-12 | finance-daily/20260512.html 404 | 部署脚本推送到 `master` 分支，但 Pages 构建源是 `main` 分支 | 强制所有脚本推送到 `main`；在检查清单中加入分支确认 |
| 2026-04-22 | 导航页显示过期信息（4月21日） | 只更新了index.html，未同步更新dashboard.html | 建立本工作流，更新导航页并归档 |
