# OWASP Security

## When to Use

- "OWASP"
- "应用安全"
- "Web 安全标准"
- "安全加固"

## OWASP Top 10 (2021)

| 排名 | 漏洞 | 风险 |
|------|------|------|
| A01 | Broken Access Control | 访问控制失效 |
| A02 | Cryptographic Failures | 加密失败 |
| A03 | Injection | 注入 |
| A04 | Insecure Design | 不安全设计 |
| A05 | Security Misconfiguration | 安全配置错误 |
| A06 | Vulnerable Components | 易受攻击组件 |
| A07 | Auth Failures | 身份验证失败 |
| A08 | Data Integrity Failures | 数据完整性失败 |
| A09 | Logging Failures | 日志记录失败 |
| A10 | SSRF | 服务端请求伪造 |

## 修复方案

### A01 - 访问控制

```python
# ❌ 危险：未验证用户权限
@app.route('/admin/delete/<id>')
def delete_user(id):
    User.delete(id)

# ✅ 安全：检查权限
@app.route('/admin/delete/<id>')
@admin_required
def delete_user(id):
    current_user.can_delete(id)
    User.delete(id)
```

### A03 - 注入防护

```python
# ❌ SQL 注入
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ 参数化查询
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))

# ✅ ORM
user = User.filter(name=name).first()
```

### XSS 防护

```python
# ❌ 危险
return f"<div>{user_input}</div>"

# ✅ 安全
from markupsafe import escape
return f"<div>{escape(user_input)}</div>"

# ✅ React
<div>{userInput}</div>  # 自动转义
```

### CSRF 防护

```python
# Flask
from flask_wtf import CSRFProtect
csrf = CSRFProtect(app)

# 前端
fetch('/api/data', {
  method: 'POST',
  headers: { 'X-CSRFToken': getCsrfToken() }
})
```

### A07 - 密码安全

```python
import bcrypt

# 加密
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 验证
bcrypt.checkpw(password.encode(), hashed)
```

## 安全Headers

```python
# Flask
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, content_security_policy=None)
```

```apache
# .htaccess
Header always set X-Frame-Options "DENY"
Header always set X-Content-Type-Options "nosniff"
Header always set Strict-Transport-Security "max-age=31536000"
```

## 验证工具

```bash
# OWASP ZAP
zap-baseline.py -t https://site.com

# Nuclei
nuclei -u https://site.com

# SSL Labs
ssltest.py -d domain.com
```

## Checklist

- [ ] 修复 OWASP Top 10 漏洞
- [ ] 启用安全 Headers
- [ ] 实现 CSRF 防护
- [ ] 加密敏感数据
- [ ] 实施访问控制
- [ ] 配置安全 Headers
