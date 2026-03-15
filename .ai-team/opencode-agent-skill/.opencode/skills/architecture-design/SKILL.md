---
name: architecture-design
description: |
  System architecture design methodology and best practices.
  Use when: designing system architecture, making technology choices, planning scalability,
  or creating technical specifications.
audience: developers, architects
workflow: design → review → document
license: MIT
compatibility: opencode
---

# Architecture Design Skill

## What I do

- Design scalable system architectures
- Recommend appropriate technologies and patterns
- Create component diagrams and data flows
- Analyze trade-offs and document decisions

## When to use me

Use this when you need to:
- Design a new system or feature architecture
- Choose between technologies (databases, frameworks, etc.)
- Plan for scalability and performance
- Create architectural decision records (ADRs)

## Core Principles

### 1. Start with Requirements

Before designing:
- Understand functional requirements
- Identify non-functional requirements (performance, security, availability)
- Know constraints (budget, timeline, team skills)

### 2. Pattern Selection

Choose appropriate patterns:

| Pattern | Use Case |
|---------|----------|
| Layered (N-tier) | Traditional web apps |
| Microservices | Large systems needing independent scaling |
| Event-driven | Async processing, real-time updates |
| CQRS | Complex read/write patterns |
| Hexagonal (Ports & Adapters) | Testability, framework independence |
| Serverless | Variable load, cost optimization |

### 3. Technology Selection Framework

Evaluate technologies by:

| Criterion | Questions |
|-----------|-----------|
| Maturity | How stable? What's the community size? |
| Performance | Benchmarks? Latency/throughput? |
| Scalability | Horizontal/vertical? |
| Maintenance | Who's maintaining? How often updates? |
| Learning Curve | Team expertise needed? |
| Cost | License, infrastructure, training? |

### 4. Database Selection

| Type | Best For |
|------|----------|
| PostgreSQL | Relational data, ACID, complex queries |
| MongoDB | Document storage, rapid prototyping |
| Redis | Caching, sessions, real-time |
| Elasticsearch | Full-text search, analytics |
| DynamoDB | Serverless, massive scale |
| SQLite | Embedded, small apps |

### 5. API Design Principles

- RESTful for CRUD operations
- GraphQL for flexible queries
- gRPC for high-performance internal services
- Webhooks for async integrations

## Output Format

### Architecture Decision Record (ADR)

```markdown
# ADR-001: Use PostgreSQL for User Data

## Status
Accepted

## Context
We need a database for user management with:
- Complex queries
- ACID compliance
- JSON support for preferences

## Decision
Use PostgreSQL 15

## Consequences
### Positive
- ACID compliance
- Rich query capabilities
- JSON support

### Negative
- Requires separate server
- More complex than SQLite
```

### System Design Document

```markdown
## System: [Name]

### Overview
[Brief description]

### Architecture
[Diagram or description]

### Components
| Component | Responsibility | Technology |
|-----------|---------------|------------|
| API Gateway | Request routing | Kong |
| Auth Service | Authentication | Node.js |

### Data Flow
1. User → API Gateway
2. API Gateway → Auth Service
3. Auth Service → Database

### Scalability
[How to scale each component]
```

## Common Patterns

### Monolith → Microservices Migration
1. Identify bounded contexts
2. Start with strangler fig pattern
3. Extract one service at a time
4. Set up service mesh

### Event-Driven Architecture
1. Define events (past tense)
2. Choose event broker (Kafka, RabbitMQ, SQS)
3. Design event schema (JSON, Avro)
4. Plan for eventual consistency

### Caching Strategy
1. Cache aside (most common)
2. Write through
3. Write behind
4. Consider: TTL, invalidation, consistency

## Anti-Patterns to Avoid

- ❌ Premature optimization
- ❌ Over-engineering for future needs
- ❌ Ignoring team skills
- ❌ No consideration for operations
- ❌ Single point of failure
- ❌ Tight coupling between services

## Checklist

Before finalizing architecture:
- [ ] All requirements addressed
- [ ] Technology choices justified
- [ ] Trade-offs documented
- [ ] Scalability considered
- [ ] Security requirements met
- [ ] Operations/maintenance plan
- [ ] Team can implement
