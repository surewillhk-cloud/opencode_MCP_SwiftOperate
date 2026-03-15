---
name: code-generation
description: |
  Code generation patterns, templates, and best practices for rapid development.
  Use when: generating new code, implementing features, creating components,
  or building APIs from scratch.
audience: developers
workflow: analyze → generate → verify
license: MIT
compatibility: opencode
---

# Code Generation Skill

## What I do

- Generate production-ready code from requirements
- Apply language-specific best practices
- Include proper types, validation, and error handling
- Create corresponding tests

## When to use me

Use this when you need to:
- Create new components or functions
- Build API endpoints
- Implement features from PRD
- Generate boilerplate code

## Core Principles

### 1. Analyze Before Generating

Before writing code:
- Read existing patterns in the codebase
- Check tech stack and version
- Identify dependencies to use
- Determine file structure

### 2. TypeScript Best Practices

| Pattern | Use | Example |
|---------|-----|---------|
| Strict typing | Always | `string`, not `any` |
| Interfaces | Shape of objects | `interface User { id: string }` |
| Types | Unions, aliases | `type Status = 'active' \| 'inactive'` |
| Generics | Reusable components | `function identity<T>(arg: T): T` |
| Optional chaining | Safe access | `user?.profile?.name` |

### 3. React/Next.js Patterns

#### Functional Component
```typescript
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
  isLoading?: boolean;
}

export function MyComponent({ title, onSubmit, isLoading = false }: Props) {
  return (
    <div>
      {isLoading ? <Spinner /> : <form onSubmit={onSubmit}>{title}</form>}
    </div>
  );
}
```

#### Custom Hook
```typescript
function useDatafetching(url: string) {
  const [data, setData] = useState<Data | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

### 4. Node.js API Patterns

#### Express Handler
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

app.get('/users/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const user = await userService.findById(id);
    
    if (!user) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'User not found' }
      });
    }
    
    res.json({ success: true, data: user });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Server error' }
    });
  }
});
```

#### Input Validation (Zod)
```typescript
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().min(0).optional(),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

### 5. Testing Patterns

#### Unit Test
```typescript
describe('formatCurrency', () => {
  it('formats USD correctly', () => {
    expect(formatCurrency(100, 'USD')).toBe('$100.00');
  });
  
  it('handles zero', () => {
    expect(formatCurrency(0, 'USD')).toBe('$0.00');
  });
});
```

#### React Component Test
```typescript
render(<Button onClick={fn} label="Click me" />);
fireEvent.click(screen.getByText('Click me'));
expect(fn).toHaveBeenCalled();
```

## Code Templates

### CRUD API Endpoint
```
File: src/routes/{resource}.ts
- GET /{resources} - List with pagination
- GET /{resources}/:id - Get by ID
- POST /{resources} - Create
- PUT /{resources}/:id - Update
- DELETE /{resources}/:id - Delete
```

### React Component Structure
```
{ComponentName}/
  index.tsx        # Main component
  {ComponentName}.types.ts  # Types
  {ComponentName}.test.tsx  # Tests
  components/      # Sub-components
  hooks/           # Custom hooks
```

### Service Layer
```
src/services/{service}.ts
- Public methods for business logic
- TypeScript interfaces for inputs/outputs
- Error handling with typed errors
```

## Verification Checklist

After generating code:
- [ ] TypeScript compiles without errors
- [ ] ESLint passes (or no new warnings)
- [ ] All imports resolve
- [ ] Tests are included
- [ ] Error handling is present
- [ ] Input validation is included

## Anti-Patterns to Avoid

- ❌ Using `any` type
- ❌ Missing error handling
- ❌ No input validation
- ❌ Hardcoded values (use config)
- ❌ No TypeScript types
- ❌ Magic numbers/strings
- ❌ Synchronous operations in main thread
- ❌ No error boundaries in React

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase, use prefix | `useAuth.ts` |
| Utils | camelCase | `formatDate.ts` |
| Types | PascalCase | `UserTypes.ts` |
| Constants | UPPER_SNAKE_CASE | `API_ENDPOINTS.ts` |
| Tests | {name}.test.ts | `formatDate.test.ts` |
