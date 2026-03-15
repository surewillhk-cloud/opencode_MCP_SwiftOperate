---
name: devops-automation
description: |
  DevOps automation patterns for CI/CD, containers, and infrastructure.
  Use when: setting up CI/CD pipelines, configuring Docker, deploying applications,
  or automating infrastructure.
audience: developers, devops engineers
workflow: design → implement → verify
license: MIT
compatibility: opencode
---

# DevOps Automation Skill

## What I do

- Create CI/CD pipelines
- Configure Docker containers
- Set up deployment automation
- Design infrastructure configurations

## When to use me

Use this when you need to:
- Set up GitHub Actions or similar CI/CD
- Create Dockerfiles
- Configure docker-compose
- Automate deployments

## CI/CD Pipeline Patterns

### GitHub Actions Basic Structure

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

### Production Deployment

```yaml
name: Deploy Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
```

## Docker Best Practices

### Dockerfile Template

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs

# Copy from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "dist/index.js"]
```

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Image too large | Multi-stage builds, remove dev deps |
| Slow builds | Layer caching, .dockerignore |
| Security vulnerabilities | Scan images, non-root user |
| Missing dependencies | Check node_modules, COPY order |

### .dockerignore

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.env.*
!.env.example
dist
coverage
*.md
```

## docker-compose for Development

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## Environment Configuration

### .env.example

```
# App
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# External Services
REDIS_URL=redis://localhost:6379
S3_BUCKET=my-bucket

# Secrets (DO NOT COMMIT)
JWT_SECRET=your-secret-here
API_KEY=your-api-key-here
```

### Configuration Pattern

```typescript
interface Config {
  nodeEnv: 'development' | 'production' | 'test';
  port: number;
  database: {
    url: string;
  };
  redis: {
    url: string;
  };
}

const config: Config = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  database: {
    url: process.env.DATABASE_URL || '',
  },
  redis: {
    url: process.env.REDIS_URL || '',
  },
};

export { config };
```

## Deployment Strategies

### 1. Direct Deployment
```
Main → Server → Restart
```
Simple, brief downtime

### 2. Blue-Green Deployment
```
Blue (active) ← Traffic
Green (standby) → Test → Switch
```
Zero downtime, requires 2x resources

### 3. Canary Deployment
```
V1 (90%) → New Version
V2 (10%) → Monitor → Scale up
```
Gradual rollout, quick rollback

### 4. Rolling Deployment
```
V1 → V2 (one by one)
```
No downtime, slower

## Security Checklist

- [ ] No secrets in Docker images
- [ ] Non-root user in containers
- [ ] Images scanned for CVEs
- [ ] Secrets from environment/vault
- [ ] Health checks configured
- [ ] Resource limits set
- [ ] Logging configured

## Common Commands

```bash
# Build
docker build -t myapp .

# Run
docker run -p 3000:3000 myapp

# Compose
docker-compose up -d
docker-compose logs -f
docker-compose down

# Deploy
docker-compose pull
docker-compose up -d --force-recreate

# Debug
docker exec -it container_name sh
docker logs -f container_name
```

## Anti-Patterns

- ❌ Using `latest` tag in production
- ❌ Running containers as root
- ❌ Storing secrets in images
- ❌ No health checks
- ❌ No resource limits
- ❌ Exposing unnecessary ports
- ❌ No log management
