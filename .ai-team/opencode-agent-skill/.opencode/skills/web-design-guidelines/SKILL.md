---
name: web-design-guidelines
description: |
  Web interface best practices for accessibility, performance, and UX.
  Use when: reviewing UI code, checking accessibility, auditing design,
  or implementing user interfaces.
audience: developers, designers
workflow: design → review → implement → verify
license: MIT
compatibility: opencode
---

# Web Design Guidelines

Comprehensive guidelines for building accessible, performant, and user-friendly web interfaces.

## When to Use

- "Review my UI"
- "Check accessibility"
- "Audit design"
- "Review UX"
- Building new UI components

---

## Accessibility (Critical)

### Semantic HTML

```typescript
// ❌ BAD
<div onClick={handleClick}>Click me</div>

// ✅ GOOD
<button onClick={handleClick}>Click me</button>
```

**Rules:**
- Use `<button>` for actions, `<a>` for links
- Use `<h1>`-`<h6>` for headings (skip levels)
- Use `<ul>/<ol>` for lists
- Use `<nav>` for navigation regions

### ARIA Labels

```typescript
// ❌ BAD - No accessible name
<button>X</button>

// ✅ GOOD - Descriptive
<button aria-label="Close dialog">X</button>

// ✅ GOOD - Icon button with label
<button aria-label="Search">
  <SearchIcon />
</button>
```

### Focus Management

```typescript
// ✅ GOOD - Visible focus styles
button:focus-visible {
  outline: 2px solid blue;
  outline-offset: 2px;
}

// ✅ GOOD - Focus trap in modals
useEffect(() => {
  if (isOpen) {
    focusFirstElement();
  }
}, [isOpen]);
```

---

## Forms

### Autocomplete

```typescript
// ✅ GOOD - Use autocomplete for user data
<input type="text" name="name" autocomplete="name" />
<input type="email" name="email" autocomplete="email" />
<input type="tel" name="phone" autocomplete="tel" />
```

### Validation

```typescript
// ✅ GOOD - Show errors after submission
const [touched, setTouched] = useState({});

const handleSubmit = (e) => {
  e.preventDefault();
  setTouched({ email: true });
  if (!isValid) return;
  // submit
};

// Show error only when touched
{errors.email && touched.email && <span>{errors.email}</span>}
```

### Labels

```typescript
// ❌ BAD - No label
<input placeholder="Email" />

// ✅ GOOD - Associated label
<label htmlFor="email">Email</label>
<input id="email" />

// ✅ GOOD - Wrapped label
<label>
  Email
  <input />
</label>
```

---

## Performance

### Layout Stability

```typescript
// ❌ BAD - Content shift
<div style={{ height: items.length ? '200px' : '0' }}>

// ✅ GOOD - Fixed dimensions or skeleton
<div style={{ minHeight: '200px' }}>
  {loading ? <Skeleton /> : <Content />}
</div>
```

### Image Optimization

```typescript
// ❌ BAD
<img src="/hero.png" />

// ✅ GOOD - Next.js Image
import Image from 'next/image';
<Image 
  src="/hero.png" 
  width={1200} 
  height={600}
  alt="Hero image"
  loading="lazy"
/>
```

### Preloading

```typescript
// ✅ GOOD - Preconnect to origins
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
```

---

## Animation

### Respect Reduced Motion

```typescript
// ❌ BAD - Always animate
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

// ✅ GOOD - Respect preference
@media (prefers-reduced-motion: no-preference) {
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
}
```

### Compositor-Only Properties

```typescript
// ✅ GOOD - GPU accelerated
transform: translateX(100px);
opacity: 0.5;

// ❌ BAD - Triggers layout
margin-left: 100px;
width: 50%;
```

---

## Typography

### Quotes

```typescript
// ❌ BAD
<p>He said "hello"</p>

// ✅ GOOD
<p>He said &ldquo;hellordquo;</p>
```

### Text Overflow

```typescript
// ✅ GOOD - Truncate with ellipsis
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// ✅ GOOD - Multi-line
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

## Dark Mode

### Color Scheme

```typescript
// ✅ GOOD - Prevent flash
<head>
  <meta name="color-scheme" content="dark light" />
</head>

// In CSS
:root {
  color-scheme: light dark;
}
```

### Theme Color

```typescript
// ✅ GOOD - Match browser UI
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
<meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)" />
```

---

## Touch & Interaction

### Touch Targets

```typescript
// ✅ GOOD - Minimum 44px tap target
button {
  min-height: 44px;
  min-width: 44px;
}
```

### Touch Action

```typescript
// ✅ GOOD - Enable pinch zoom
.pan-zoom {
  touch-action: pan-x pan-y pinch-zoom;
}

// ✅ GOOD - Disable for horizontal scroll
.horizontal-scroll {
  touch-action: pan-y;
}
```

---

## Navigation & State

### URL State

```typescript
// ✅ GOOD - URL reflects state
const [filter, setFilter] = useState('all');
const router = useRouter();

// Update URL when filter changes
useEffect(() => {
  router.push(`?filter=${filter}`, undefined, { shallow: true });
}, [filter]);
```

### Deep Linking

```typescript
// ✅ GOOD - Support direct links
// URL: /products?category=shoes&sort=price
// Should restore full state from URL
```

---

## Checklist

### Before Shipping

- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Focus states visible
- [ ] Keyboard navigable
- [ ] Color contrast 4.5:1 minimum
- [ ] No layout shift (CLS < 0.1)
- [ ] Images sized correctly
- [ ] Touch targets 44px minimum
- [ ] Reduced motion respected
- [ ] Dark mode supported
- [ ] Error messages descriptive

---

## Anti-Patterns

- ❌ Clickable divs without button semantics
- ❌ Missing alt on images
- ❌ Placeholder as label
- ❌ Focus outline removed
- ❌ Layout shifts on load
- ❌ Autoplay videos without controls
- ❌ Links without href
- ❌ Generic error messages
