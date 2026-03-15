---
name: vercel-deploy
description: |
  Deploy applications and websites to Vercel instantly.
  Use when: user asks to "deploy", "push live", "publish", or "go to production".
audience: developers
workflow: prepare → deploy → verify
license: MIT
compatibility: opencode
---

# Vercel Deployment Skill

Deploy applications to Vercel with automatic framework detection.

## When to Use

- "Deploy my app"
- "Deploy this to production"
- "Push this live"
- "Deploy and give me the link"
- Need a shareable URL

---

## Auto-Detected Frameworks

Vercel automatically detects 40+ frameworks:

| Framework | Detection |
|-----------|-----------|
| Next.js | next.config.js |
| React | package.json + index.html |
| Vue | vue.config.js |
| Nuxt | nuxt.config.js |
| Svelte | svelte.config.js |
| Astro | astro.config.mjs |
| Remix | remix.config.js |
| Vite | vite.config.js |
| Express | package.json + server.js |
| Fastify | package.json + server.js |
| Static | index.html |

---

## Deployment Process

### 1. Prepare Project

```bash
# Ensure package.json has correct scripts
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

### 2. Create Deployment

```bash
# Option 1: Vercel CLI
npx vercel --prod

# Option 2: Git Integration
# Push to GitHub → Vercel auto-deploys
```

### 3. Verify

- Preview URL works
- Production URL works
- Environment variables set

---

## Environment Variables

### Required for Production

```bash
# Database
DATABASE_URL=postgresql://...

# API Keys
API_KEY=sk-...
JWT_SECRET=...

# URLs
NEXT_PUBLIC_API_URL=https://api.example.com
```

### Set via CLI

```bash
vercel env add DATABASE_URL production
vercel env add API_KEY production
```

---

## Configuration

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": null,
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

---

## Best Practices

### 1. Exclude from Upload

```json
// .vercelignore
node_modules
.git
.env*.local
*.log
dist
```

### 2. Use Edge Functions

```typescript
// api/hello.ts
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export function GET(request: NextRequest) {
  return NextResponse.json({ 
    message: 'Hello from Edge!' 
  });
}
```

### 3. Optimize Images

```typescript
// next.config.js
module.exports = {
  images: {
    domains: ['your-cdn.com'],
    formats: ['image/avif', 'image/webp'],
  },
};
```

---

## Troubleshooting

### Build Fails

| Error | Solution |
|-------|----------|
| Module not found | Check package.json dependencies |
| Build timeout | Increase timeout in vercel.json |
| TypeScript error | Run `npm run build` locally first |

### Runtime Errors

| Error | Solution |
|-------|----------|
| 500 Internal | Check function logs in dashboard |
| 404 on assets | Check outputDirectory config |
| ENV not set | Add via vercel env add |

---

## Output Format

```
Deployment successful! 🎉

Preview URL: https://project-abc123.vercel.app
Production URL: https://project.vercel.app

To transfer ownership:
1. Visit: https://vercel.com/claim-deployment?code=xxxxx
2. Click "Claim Deployment"
3. Connect your Vercel account
```

---

## Anti-Patterns

- ❌ Committing secrets to git
- ❌ Using `latest` tag for images in production
- ❌ Not setting up preview deployments
- ❌ Missing error boundaries
- ❌ No monitoring/alerting
