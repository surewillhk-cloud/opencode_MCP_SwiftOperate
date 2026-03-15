---
name: code-refactoring
description: |
  Code refactoring methodology and patterns for improving code quality.
  Use when: refactoring code, reducing complexity, eliminating duplication,
  improving readability, or cleaning up technical debt.
audience: developers
workflow: analyze → plan → refactor → verify
license: MIT
compatibility: opencode
---

# Code Refactoring Skill

## What I do

- Simplify complex code
- Eliminate duplication
- Improve naming and structure
- Apply design patterns appropriately
- Reduce technical debt

## When to use me

Use this when you need to:
- Refactor existing code
- Clean up technical debt
- Improve code readability
- Extract functions or classes
- Simplify complex logic

## Core Principles

### 1. Preserve Behavior

> "Refactoring is changing the internal structure of code without changing its external behavior"

- Tests must pass before and after
- Don't add new features while refactoring
- One change at a time

### 2. Small Steps

- Make incremental changes
- Run tests after each change
- Commit frequently
- Don't refactor everything at once

### 3. Readability First

- Clear naming over clever code
- Self-documenting code
- Remove dead code
- Simplify conditionals

## Common Refactoring Patterns

### Extract Function

**Before:**
```typescript
function processOrder(order: Order) {
  // Validate order
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  
  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  
  // Apply discount
  if (total > 100) {
    total *= 0.9;
  }
  
  // Save order
  db.orders.save(order);
  
  // Send notification
  email.send(order.customerEmail, 'Order confirmed');
}
```

**After:**
```typescript
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order.items);
  const finalTotal = applyDiscount(total);
  saveOrder(order, finalTotal);
  sendConfirmationEmail(order.customerEmail);
}

function validateOrder(order: Order): void {
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
}

function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

### Replace Conditional with Guard Clause

**Before:**
```typescript
function getPayAmount(employee: Employee) {
  if (employee.isSeparated) {
    return 0;
  } else {
    if (employee.isRetired) {
      return employee.retiredPay;
    } else {
      return employee.normalPay;
    }
  }
}
```

**After:**
```typescript
function getPayAmount(employee: Employee): number {
  if (employee.isSeparated) return 0;
  if (employee.isRetired) return employee.retiredPay;
  return employee.normalPay;
}
```

### Introduce Parameter Object

**Before:**
```typescript
function createEvent(
  title: string,
  startDate: string,
  startTime: string,
  endDate: string,
  endTime: string,
  location: string
) { /* ... */ }
```

**After:**
```typescript
interface EventTime {
  date: string;
  time: string;
}

interface EventDetails {
  title: string;
  start: EventTime;
  end: EventTime;
  location: string;
}

function createEvent(details: EventDetails) { /* ... */ }
```

### Rename Variable/Function

| Before | After | Reason |
|--------|-------|--------|
| `d` | `days` | More descriptive |
| `processData()` | `calculateOrderTotal()` | Verb describes action |
| `result` | `eligibleForDiscount` | Boolean should be clear |
| `Manager` | `OrderProcessor` | Class is a thing, not a person role |

### Remove Dead Code

- Unused variables
- Unused functions
- Commented out code
- Unreachable code
- Old feature flags

## Code Smells

### Complexity

| Smell | Indicator | Fix |
|-------|-----------|-----|
| Long function | > 50 lines | Extract functions |
| Deep nesting | > 3 levels | Guard clauses, early returns |
| Too many parameters | > 4 | Parameter object |
| Switch statements | Multiple cases | Polymorphism |

### Coupling

| Smell | Indicator | Fix |
|-------|-----------|-----|
| Feature envy | Accesses another object's data | Move function |
| Message chains | a.b.c.d.e | Hide delegates |
| Middle man | Delegates most calls | Remove |
| Parallel inheritance | Two hierarchies grow together | Combine |

### Discipline

| Smell | Indicator | Fix |
|-------|-----------|-----|
| Duplicate code | Same/similar code in 3+ places | Extract to function |
| Lazy class | Does too little | Inline or remove |
| Speculative generality | Unused code | Remove |
| Temporary field | Fields set sometimes | Extract object |

## Refactoring Workflow

### Step 1: Identify

Find code that needs refactoring:
- Long functions
- Duplication
- Poor naming
- Complex conditionals

### Step 2: Verify

Ensure tests exist and pass:
```bash
npm test          # Run all tests
npm run test:cov  # Check coverage
```

### Step 3: Refactor

Make small, incremental changes:
1. Extract one function
2. Run tests
3. Repeat

### Step 4: Verify Again

- All tests pass
- No new warnings
- Code is cleaner

### Step 5: Commit

```bash
git add -A
git commit -m "refactor: extract calculateTotal from processOrder"
```

## Naming Conventions

### Variables
- Use nouns: `user`, `order`, `items`
- Boolean: `isActive`, `hasPermission`, `canEdit`
- Collections: `users`, `orderItems` (plural)

### Functions
- Use verbs: `getUser`, `calculateTotal`, `sendEmail`
- Boolean: `isValid`, `hasAccess`, `canProcess`
- CRUD: `createUser`, `updateUser`, `deleteUser`

### Classes
- PascalCase: `UserService`, `OrderProcessor`
- Nouns describing responsibility

## Code Review Checklist

After refactoring:
- [ ] Tests still pass
- [ ] No new warnings
- [ ] Code is more readable
- [ ] Function names describe what it does
- [ ] No duplication introduced
- [ ] Single responsibility maintained

## Anti-Patterns

- ❌ Refactoring and adding features together
- ❌ Skipping tests
- ❌ Large refactors (do small)
- ❌ Changing behavior while "refactoring"
- ❌ Not running tests after each change
- ❌ Refactoring code you don't understand
