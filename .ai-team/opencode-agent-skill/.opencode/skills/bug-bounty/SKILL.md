# Bug Bounty

## When to Use

- "漏洞赏金"
- "渗透测试"
- "安全评估"
- "红队"
- "发现漏洞"

## Bug Bounty 平台

| 平台 | 类型 |
|------|------|
| HackerOne | 商业平台 |
| Bugcrowd | 商业平台 |
| OpenBugBounty | 开源/免费 |
| Intigriti | 欧洲平台 |
| YesWeHack | 欧洲平台 |

## 信息收集

### 被动收集

```bash
# Subdomain Enumeration
subfinder -d target.com

# Wayback Machine
waybackurls target.com

# GitHub Dorks
gh --url target.com search code "password"
```

### 主动收集

```bash
# Port Scan
nmap -sV target.com

# Web Scan
nikto -h target.com

# Directory Brute
gobuster dir -u target.com -w wordlist.txt
```

## 常见漏洞

### IDOR

```bash
# 测试步骤
1. 用户A访问 /api/user/123/profile
2. 修改 ID 为 124
3. 如果能访问其他用户数据 = IDOR
```

### SSRF

```bash
# 探测
# URL 参数: url, src, dest, redirect, next, data, reference, site, html, val, validate, domain, callback, return, page, feed, host, port, to, out, view, dir, show, navigation, open, file, document, folder, pg, style, doc, img, source

# 内部探测
http://169.254.169.254/  # AWS metadata
http://metadata.google.internal/  # GCP metadata
```

### XXE

```xml
<!-- 测试 payload -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

### Business Logic

```python
# 金额篡改
# 1. 抓包修改 price=0.01
# 2. 负数 quantity
# 3. 积分溢出

# 越权操作
# 1. 普通用户访问 /admin/*
# 2. 修改其他用户数据
# 3. 批量操作绕过限制
```

## 测试清单

### 认证

- [ ] 暴力破解
- [ ] 密码重置逻辑
- [ ] Session 固定
- [ ] 2FA 绕过
- [ ] OAuth 配置

### 授权

- [ ] 水平越权
- [ ] 垂直越权
- [ ] IDOR
- [ ] 敏感功能访问

### 输入处理

- [ ] SQL 注入
- [ ] XSS
- [ ] Command Injection
- [ ] SSRF
- [ ] XXE
- [ ] Deserialization

### 业务逻辑

- [ ] 金额篡改
- [ ] 积分绕过
- [ ] 库存绕过
- [ ] 批量操作限制

## 报告模板

```markdown
# Bug Report

## Title
[漏洞类型] - [简短描述]

## Severity
Critical / High / Medium / Low

## Description
详细描述漏洞

## Steps to Reproduce
1. 步骤1
2. 步骤2

## Proof of Concept
截图/PoC

## Impact
影响说明

## Remediation
修复建议
```

## 工具推荐

```bash
# Web 漏洞扫描
 nuclei -t cves/ -l urls.txt

# 参数发现
paramspider -d target.com

# Fuzz
ffuf -u target.com/FUZZ -w wordlist.txt

# JavaScript 分析
subjs -i js_files.txt
```

## Rewards

| 严重性 | 常见奖励 |
|--------|----------|
| Critical | $5,000 - $100,000+ |
| High | $1,000 - $5,000 |
| Medium | $250 - $1,000 |
| Low | $50 - $250 |
