---
name: dev-standards
description: |
  Full-stack development standards including code principles, React/Next.js best practices,
  AI Studio prototype normalization, file structures, and API response formats.
  Used by fullstack-dev and code-generator agents.
audience: developers
workflow: develop → verify → ship
license: MIT
compatibility: opencode
---

# Development Standards

## Core Principles

- **DRY**: Don't Repeat Yourself - extract common logic
- **KISS**: Keep It Simple - avoid over-engineering
- **Single Responsibility**: One function, one job. Split if >50 lines
- **YAGNI**: You Aren't Gonna Need It - don't build for future

---

## React/Next.js Best Practices

### Critical (Must Fix)

#### 1. Eliminate Waterfalls

**Problem**: Sequential data fetching
```typescript
// ❌ BAD - Waterfall
const user = await fetchUser(id);
const posts = await fetchPosts(user.id);
const comments = await fetchComments(posts[0].id);
```

**Solution**: Parallel or eager start
```typescript
// ✅ GOOD - Parallel
const [user, posts] = await Promise.all([
  fetchUser(id),
  fetchPosts(id)
]);

// ✅ GOOD - Eager start
const postsQuery = useQuery({ queryKey: ['posts', id], queryFn: () => fetchPosts(id) });
const userQuery = useQuery({ queryKey: ['user', id], queryFn: () => fetchUser(id) });
```

#### 2. Bundle Size Optimization

- Use dynamic imports for heavy components
- Avoid large libraries - use alternatives
- Tree-shake unused code
```typescript
// ❌ BAD
import _ from 'lodash';

// ✅ GOOD - specific imports
import debounce from 'lodash/debounce';
import throttle from 'lodash/throttle';

// ✅ BETTER - use native or smaller libs
import { debounce } from 'es-toolkit';
```

#### 3. Server-Side Rendering

- Render initial data on server
- Use Server Components by default
- Minimize client bundle
```typescript
// ❌ BAD - Fetching on client
'use client';
export default function Page({ params }) {
  const data = useQuery(['data'], () => fetch('/api/data'));
}

// ✅ GOOD - Server Component
export default async function Page({ params }) {
  const data = await fetch('/api/data', { cache: 'no-store' });
  return <Display data={data} />;
}
```

### High Priority

#### 4. Client Data Fetching

- Use React Query / SWR for client fetching
- Set proper stale times
- Prefetch on hover
```typescript
// ✅ GOOD - React Query
const { data, isLoading } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  staleTime: 5 * 60 * 1000, // 5 minutes
  prefetch: true
});
```

#### 5. Re-render Optimization

- Memoize expensive computations
- Use React.memo for list items
- Avoid inline functions in props
```typescript
// ❌ BAD
<List items={items} onItemClick={(id) => handleClick(id)} />

// ✅ GOOD
const handleClick = useCallback((id: string) => {
  // handler
}, [dep]);

<List items={items} onItemClick={handleClick} />
```

#### 6. Image Optimization

- Always specify dimensions
- Use next/image
- Lazy load below fold
```typescript
// ❌ BAD
<img src="/banner.png" />

// ✅ GOOD
import Image from 'next/image';
<Image src="/banner.png" width={800} height={400} alt="Banner" />
```

### Medium Priority

#### 7. Proper State Management

- Use useState for simple UI state
- Use Context for global state
- Use React Query for server state
- Avoid prop drilling

#### 8. Form Handling

- Use controlled components
- Validate on blur, not on change
- Show errors after submission attempt
- Use form libraries for complex forms (react-hook-form)

---

## AI Studio Prototype Normalization

When receiving prototype code from `prototypes/[feature]/`:

### ✅ Preserve (Don't Touch)
- UI layout structure
- Interaction logic and state management
- Visual styling (colors, spacing, fonts)
- Component behavior

### 🔧 Must Transform
- [ ] Split components by project structure
- [ ] Replace inline styles with Tailwind classes
- [ ] Add TypeScript type definitions
- [ ] Extract mock data to `/mocks` directory
- [ ] Add Loading skeleton
- [ ] Add Empty state
- [ ] Add Error state
- [ ] Add mobile responsive
- [ ] Replace API calls with real endpoint placeholders

### ❌ Forbidden
- Rewrite UI structure
- Rewrite interaction logic (except bugs)
- Change design style
- Discard mock data

---

## File Structure

### React / Next.js
```
app/[feature]/
  page.tsx
  layout.tsx
  loading.tsx
  error.tsx
  components/
    FeatureList.tsx
    FeatureItem.tsx
  hooks/
    useFeature.ts
  types.ts
  mocks/feature.mock.ts
```

### Node.js Backend
```
src/
  routes/
    feature.ts
  services/
    feature.service.ts
  middleware/
  types/
  utils/
```

### Python FastAPI
```
app/
  routers/
    feature.py
  services/
    feature.py
  schemas/
  models/
```

---

## API Response Format

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}
```

**Every API must include:**
- Input validation
- Unified error handling (no raw 500s)
- JSDoc comments (params, response, error codes)

---

## Forbidden Actions

- ❌ API without error handling
- ❌ Async operations without Loading state
- ❌ TypeScript `any` type
- ❌ Hardcoded secrets (use env variables)
- ❌ Full table queries without pagination
- ❌ Direct database access in controllers
- ❌ Waterfall data fetching
- ❌ Large bundle imports
- ❌ Unoptimized images
