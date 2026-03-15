---
name: ui-aistudio-guide
description: Google AI Studio 原型提示词规范，用于生成可交互前端原型，输出单文件可运行代码。UI 设计师使用。
---

# Google AI Studio 原型提示词规范

## 每个页面的 AI Studio 提示词格式

```
Build a fully interactive [页面类型] prototype with the following requirements:

**Stack:** React with hooks, Tailwind CSS, no backend needed

**Layout:**
[描述布局结构，如：top navigation bar + left sidebar(240px) + main content area]

**Components:**
- [组件1]: [详细描述包括交互行为，如：search input with debounce, shows results dropdown]
- [组件2]: [描述]

**Visual Style:**
- Primary color: [色值]
- Background: [色值]
- Font size: [规格]
- Border radius: [px]

**All States Must Be Functional:**
- Loading: skeleton screens for content areas
- Empty: illustrated empty state with CTA button
- Error: inline error messages with retry option
- Success: toast notification

**Mock Data:**
Include realistic mock data (minimum 5-10 items) so all interactions are demonstrable

**Important:**
- Output as a single self-contained HTML or JSX file
- All buttons, links, and interactions must be clickable
- No placeholder comments like "// add logic here"
- Must be runnable without any build step
```

## 写作要点

- **组件描述要具体**：不写"一个列表"，写"可点击展开的手风琴列表，点击标题展开内容区域"
- **交互必须可演示**：每个按钮和操作都要有对应的 mock 反应
- **mock 数据要真实**：用真实姓名、产品名、日期，不用 "Item 1"、"User A"
- **状态必须可触发**：加一个"切换状态"的隐藏按钮，方便演示 empty/error 状态

## 原型代码保存规范

```
prototypes/
  [功能名]/
    index.html 或 App.jsx   ← AI Studio 生成的原型
    README.md               ← 说明如何打开和演示
```
