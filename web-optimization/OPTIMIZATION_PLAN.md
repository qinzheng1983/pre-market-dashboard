# Web 界面优化计划

## 目标
基于 `web-design` skill 的设计指南，创建统一设计系统，优化所有三个界面。

## 优化策略

### Phase 1: 创建统一设计系统
- 文件: `design-system.css` / `design-tokens.ts`
- 包含: 色彩、间距、排版、组件基础样式

### Phase 2: 优化盘前市场仪表板
- 统一使用 design tokens
- 改进无障碍支持 (focus indicators, reduced-motion)
- 优化响应式 (container queries)
- 改进色彩对比度

### Phase 3: 优化地缘风险仪表盘
- 替换渐变背景为 surface layering
- 优化暗色主题对比度
- 添加无障碍支持
- 改进动画性能

### Phase 4: 优化财务报告
- 添加响应式支持
- 优化打印样式
- 改进色彩系统
- 添加暗色模式支持

### Phase 5: 验证与测试
- 对照 web-design 检查清单验证
- 测试响应式
- 测试无障碍

## 设计系统规范

### 色彩 (HSL)
- Primary: hsl(220 80% 55%)
- Surface-0 (light): hsl(220 15% 98%)
- Surface-1 (light): hsl(220 15% 100%)
- Surface-2 (light): hsl(220 15% 96%)
- Text-primary: hsl(220 25% 15%)
- Text-secondary: hsl(220 15% 45%)

### 间距 (8px 基准)
- space-1: 0.25rem (4px)
- space-2: 0.5rem (8px)
- space-3: 0.75rem (12px)
- space-4: 1rem (16px)
- space-6: 1.5rem (24px)
- space-8: 2rem (32px)

### 排版
- 比例: 1.25 (major third)
- Body: 1rem, line-height 1.5
- Heading: line-height 1.1-1.2
- Max line length: 65ch

### 无障碍
- Focus: 2px solid primary, offset 2px
- Reduced motion: 0.01ms duration
- Touch target: min 44x44px
- Contrast: 4.5:1 for text
