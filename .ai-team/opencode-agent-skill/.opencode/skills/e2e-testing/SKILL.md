# E2E Testing

## When to Use

- "写端到端测试"
- "用户流程测试"
- "UI 交互测试"
- "浏览器自动化测试"

## Tools

| 工具 | 适用场景 |
|------|----------|
| Playwright | 现代 Web 应用（推荐） |
| Cypress | 前端测试 |
| Selenium | 传统 Web 应用 |
| Puppeteer | Node.js 端到端 |

## Playwright 快速开始

```bash
# 安装
npm init playwright@latest

# 运行测试
npx playwright test

# 打开 UI 模式
npx playwright test --ui
```

## Playwright 基本语法

```python
from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # 访问页面
        page.goto("https://example.com")
        
        # 交互
        page.fill("#username", "testuser")
        page.fill("#password", "password123")
        page.click("#login-button")
        
        # 断言
        assert "Welcome" in page.title()
        
        browser.close()
```

## 测试场景示例

### 1. 用户登录流程

```python
def test_login_flow():
    # 1. 打开登录页
    page.goto("/login")
    
    # 2. 输入凭证
    page.fill("#email", "user@example.com")
    page.fill("#password", "correct-password")
    
    # 3. 点击登录
    page.click("button[type='submit']")
    
    # 4. 等待跳转
    page.wait_for_url("/dashboard")
    
    # 5. 验证成功
    assert page.locator(".user-name").text_content() == "Test User"
```

### 2. 表单提交

```python
def test_form_submission():
    page.goto("/form")
    
    # 填写表单
    page.fill("#name", "John Doe")
    page.select_option("#country", "US")
    page.check("#terms")
    
    # 提交
    page.click("#submit")
    
    # 验证成功消息
    assert page.locator(".success-message").is_visible()
```

### 3. 购物车流程

```python
def test_add_to_cart():
    # 1. 浏览商品
    page.goto("/products")
    
    # 2. 添加到购物车
    page.click(".product:first-child .add-to-cart")
    
    # 3. 验证购物车数量
    assert page.locator(".cart-count").text_content() == "1"
    
    # 4. 查看购物车
    page.click(".cart-icon")
    
    # 5. 验证商品在购物车
    assert page.locator(".cart-item").count() == 1
```

## 等待策略

```python
# 等待元素出现
page.wait_for_selector("#button")

# 等待元素可见
page.wait_for_selector("#button", state="visible")

# 等待 URL 变化
page.wait_for_url("**/dashboard")

# 等待网络请求完成
page.wait_for_load_state("networkidle")

# 等待函数返回 true
page.wait_for_function("() => document.readyState === 'complete'")
```

## 断言

```python
from playwright.sync_api import expect

# 文本断言
expect(page.locator(".title")).to_have_text("Welcome")

# 元素存在
expect(page.locator(".success")).to_be_visible()

# 元素不存在
expect(page.locator(".error")).to_be_hidden()

# 计数
expect(page.locator(".item")).to_have_count(5)

# URL
expect(page).to_have_url("**/dashboard")
```

## 调试

```bash
# UI 模式
npx playwright test --ui

# 只运行失败的测试
npx playwright test --last-failed

# 显示浏览器
npx playwright test --headed

# 跟踪
npx playwright show-report
```

## CI/CD 集成

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npx playwright install --with-deps
      - run: npx playwright test
```

## Checklist

- [ ] 测试覆盖核心用户流程
- [ ] 测试登录/注册
- [ ] 测试表单提交
- [ ] 测试错误处理
- [ ] 使用等待而非 sleep
- [ ] 测试通过
- [ ] 在 CI 中运行
