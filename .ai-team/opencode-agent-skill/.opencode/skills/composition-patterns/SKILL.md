---
name: composition-patterns
description: |
  React composition patterns that scale. Helps avoid boolean prop proliferation
  through compound components, state lifting, and internal composition.
  Use when: refactoring components, building reusable libraries, or designing flexible APIs.
audience: developers
workflow: analyze → pattern selection → implement → verify
license: MIT
compatibility: opencode
---

# React Composition Patterns

Patterns for building flexible, reusable React components without prop explosion.

## When to Use

- Refactoring components with many boolean props
- Building reusable component libraries
- Designing flexible APIs
- Reviewing component architecture

---

## Problem: Boolean Prop Proliferation

### Anti-Pattern

```typescript
// ❌ BAD - Boolean explosion
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
  isFullWidth?: boolean;
  hasIcon?: boolean;
  iconPosition?: 'left' | 'right';
  // ...10 more props
}

<Button 
  variant="primary"
  size="md"
  isLoading={false}
  isDisabled={false}
  isFullWidth={true}
  hasIcon={true}
  iconPosition="left"
/>
```

---

## Pattern 1: Compound Components

### Concept

Parent renders children, children access parent state via context.

### Implementation

```typescript
// Context
const TabsContext = createContext<{
  activeTab: string;
  setActiveTab: (id: string) => void;
}>({ activeTab: '', setActiveTab: () => {} });

// Parent
function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

// Child - Tab
function Tab({ children, id }: { children: ReactNode; id: string }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  const isActive = activeTab === id;
  return (
    <button 
      className={isActive ? 'active' : ''}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
}

// Child - Panel
function TabPanel({ children, id }: { children: ReactNode; id: string }) {
  const { activeTab } = useContext(TabsContext);
  return activeTab === id ? <div>{children}</div> : null;
}

// Usage
<Tabs defaultTab="overview">
  <Tab id="overview">Overview</Tab>
  <Tab id="pricing">Pricing</Tab>
  <TabPanel id="overview">Content here</TabPanel>
  <TabPanel id="pricing">Pricing info</TabPanel>
</Tabs>
```

### Benefits
- Explicit relationships
- Flexible composition
- Encapsulated state

---

## Pattern 2: State Lifting

### Concept

Move state up when needed by multiple children.

### Implementation

```typescript
// ❌ BAD - Local state in child
function List({ items }) {
  const [selected, setSelected] = useState(null);
  return (
    <div>
      {items.map(item => (
        <Item 
          key={item.id} 
          item={item}
          isSelected={selected === item.id}
          onSelect={() => setSelected(item.id)}
        />
      ))}
    </div>
  );
}

// ✅ GOOD - Lift state
function List({ items }) {
  const [selectedId, setSelectedId] = useState(null);
  
  return (
    <div>
      {items.map(item => (
        <Item 
          key={item.id} 
          item={item}
          isSelected={selectedId === item.id}
          onSelect={() => setSelectedId(item.id)}
        />
      ))}
    </div>
  );
}
```

### When to Lift

- Multiple children need same data
- Children need to communicate
- Share behavior across subtrees

---

## Pattern 3: Render Props

### Concept

Pass function as children to control rendering.

```typescript
// ✅ GOOD - Render prop
function DataFetcher({ render }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchData().then(setData);
  }, []);
  return render(data);
}

// Usage
<DataFetcher render={(data) => (
  data ? <List items={data} /> : <Loading />
)} />
```

---

## Pattern 4: Flexible Children

### Concept

Allow mixing predefined slots with custom children.

```typescript
function Card({ children, actions }: { 
  children: ReactNode; 
  actions?: ReactNode; 
}) {
  return (
    <div className="card">
      <div className="card-body">{children}</div>
      {actions && <div className="card-actions">{actions}</div>}
    </div>
  );
}

// Usage
<Card>
  <Card.Title>Hello</Card.Title>
  <Card.Content>Content here</Card.Content>
</Card>

<Card actions={<button>Click</button>}>
  Content with actions
</Card>
```

---

## Pattern 5: Slot Pattern

### Concept

Named slots instead of many props.

```typescript
function Modal({ 
  children,
  header,
  footer,
  closeButton 
}: { 
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  closeButton?: boolean;
}) {
  return (
    <div className="modal">
      {header && <div className="modal-header">{header}</div>}
      <div className="modal-body">{children}</div>}
      {footer && <div className="modal-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Modal 
  header={<h2>Confirm</h2>}
  footer={<><button>Cancel</button><button>OK</button></>}
>
  Are you sure?
</Modal>
```

---

## Choosing the Right Pattern

| Pattern | Use When |
|---------|----------|
| Compound Components | Related components that share state |
| State Lifting | Siblings need shared state |
| Render Props | Need control over rendering |
| Flexible Children | Mix default + custom content |
| Slot Pattern | Many optional sections |

---

## Refactoring Guide

1. **Identify boolean props** - `isX`, `hasY`, `showZ`
2. **Group related props** - Are they actually one concept?
3. **Choose pattern** - Based on use cases
4. **Extract context** - For compound components
5. **Test thoroughly** - Ensure flexibility preserved

---

## Anti-Patterns

- ❌ Prop drilling (use Context)
- ❌ Boolean explosion (use compound components)
- ❌ render prop without memoization
- ❌ Over-engineering simple components
- ❌ Forcing patterns where not needed
