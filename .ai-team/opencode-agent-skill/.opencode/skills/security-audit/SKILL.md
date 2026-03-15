---
name: security-audit
description: |
  Security auditing methodology and vulnerability detection patterns.
  Use when: auditing code for security issues, finding vulnerabilities,
  reviewing authentication/authorization, or performing security checks.
audience: developers, security engineers
workflow: scan → analyze → report → remediate
license: MIT
compatibility: opencode
---

# Security Audit Skill

## What I do

- Identify security vulnerabilities in code
- Check for common security anti-patterns
- Review authentication and authorization logic
- Provide actionable remediation recommendations

## When to use me

Use this when you need to:
- Audit code for security issues
- Review authentication implementation
- Check for OWASP Top 10 vulnerabilities
- Perform security review before release

## OWASP Top 10 (2021)

| # | Category | Description |
|---|----------|-------------|
| A01 | Broken Access Control | Users acting outside intended permissions |
| A02 | Cryptographic Failures | Failures related to cryptography leading to data exposure |
| A03 | Injection | SQL, NoSQL, OS command injection |
| A04 | Insecure Design | Missing or ineffective security controls |
| A05 | Security Misconfiguration | Improperly configured permissions or settings |
| A06 | Vulnerable Components | Using components with known vulnerabilities |
| A07 | Auth Failures | Broken authentication mechanisms |
| A08 | Data Integrity Failures | Software and data integrity failures |
| A09 | Logging Failures | Insufficient logging, detection, monitoring |
| A10 | SSRF | Server-Side Request Forgery |

## Vulnerability Patterns

### 1. SQL Injection

**Bad:**
```typescript
db.query(`SELECT * FROM users WHERE id = ${userId}`);
```

**Good:**
```typescript
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

**Detection:** Search for string concatenation in queries

### 2. Cross-Site Scripting (XSS)

**Bad:**
```typescript
element.innerHTML = userInput;
dangerouslySetInnerHTML={{ __html: userInput }}
```

**Good:**
```typescript
element.textContent = userInput;
```

**Detection:** `innerHTML`, `dangerouslySetInnerHTML`

### 3. Command Injection

**Bad:**
```typescript
exec(`ls ${userDirectory}`);
system(`rm -rf ${userPath}`);
```

**Good:**
```typescript
execFile('ls', [userDirectory]);
```

**Detection:** `exec`, `system`, `spawn`, `eval`, `Function`

### 4. Hardcoded Secrets

**Bad:**
```typescript
const API_KEY = 'sk-abc123...';
const password = 'secret123';
```

**Good:**
```typescript
const API_KEY = process.env.API_KEY;
```

**Detection:** Search for `API_KEY`, `password`, `secret`, `token`, `key`

### 5. Weak Cryptography

**Bad:**
```typescript
crypto.createHash('md5');
crypto.createCipher('des');
```

**Good:**
```typescript
crypto.createHash('sha256');
crypto.createCipheriv('aes-256-gcm', key, iv);
```

**Detection:** `md5`, `sha1`, `des`, `rc4`

### 6. Missing Authentication

**Bad:**
```typescript
app.get('/api/admin/users', (req, res) => {
  // No auth check!
  db.query('SELECT * FROM users');
});
```

**Good:**
```typescript
app.get('/api/admin/users', requireAuth, (req, res) => {
  // Auth check in middleware
});
```

### 7. Insecure Direct Object References (IDOR)

**Bad:**
```typescript
app.delete('/api/notes/:id', (req, res) => {
  db.delete('DELETE FROM notes WHERE id = ?', [req.params.id]);
  // Any user can delete any note!
});
```

**Good:**
```typescript
app.delete('/api/notes/:id', requireAuth, async (req, res) => {
  const note = await db.get('SELECT * FROM notes WHERE id = ?', [req.params.id]);
  if (note.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await db.delete('DELETE FROM notes WHERE id = ?', [req.params.id]);
});
```

## Audit Checklist

### Authentication
- [ ] Passwords properly hashed (bcrypt, argon2)
- [ ] Sessions use secure cookies
- [ ] MFA available
- [ ] Password reset tokens are random, expire
- [ ] No credentials in URLs

### Authorization
- [ ] All endpoints check permissions
- [ ] IDOR vulnerabilities fixed
- [ ] Role-based access control (RBAC)
- [ ] Least privilege principle

### Input Validation
- [ ] All user input validated
- [ ] Parameterized queries used
- [ ] File uploads validated
- [ ] No eval() or similar

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS everywhere
- [ ] Secrets in environment variables
- [ ] No sensitive data in logs

### Dependencies
- [ ] npm audit / security checks run
- [ ] No known CVEs in dependencies
- [ ] Dependencies up to date
- [ ] No unnecessary dependencies

## Output Format

### Security Report

```markdown
## Security Audit Report

### 🔴 Critical Issues

| ID | Vulnerability | Location | Impact | Fix |
|----|---------------|----------|--------|-----|
| S-01 | SQL Injection | src/db.ts:45 | Data breach | Use parameterized queries |
| S-02 | Hardcoded API Key | src/config.ts:10 | Credential leak | Use env variables |

### 🟡 Medium Issues

| ID | Vulnerability | Location | Impact | Fix |
|----|---------------|----------|--------|-----|
| M-01 | XSS Risk | src/components/Editor.tsx:23 | Script injection | Use textContent |

### 🟢 Info / Recommendations

| ID | Suggestion | Location |
|----|------------|----------|
| I-01 | Add rate limiting | src/server.ts |
```

## Tools for Auditing

### npm
```bash
npm audit              # Check for vulnerabilities
npm audit fix          # Auto-fix some
npm outdated           # Check outdated packages
```

### GitHub
```bash
npm install -g retire  # Retire.js
retire.js              # Scan for vulnerable JS libraries
```

### Custom Searches
```bash
grep -r "eval(" --include="*.js"
grep -r "innerHTML" --include="*.ts" --include="*.tsx"
grep -r "password.*=" --include="*.ts"
```

## Remediation Priority

1. **Critical (24h)**: SQL Injection, RCE, Auth bypass
2. **High (1 week)**: XSS, Hardcoded secrets, IDOR
3. **Medium (1 month)**: Weak crypto, Missing validation
4. **Low (next release)**: Info disclosure, Logging issues

## Anti-Patterns

- ❌ Ignoring security warnings
- ❌ Custom crypto implementations
- ❌ Storing secrets in code
- ❌ Client-side only validation
- ❌ Trusting user input
- ❌ No security testing in CI/CD
