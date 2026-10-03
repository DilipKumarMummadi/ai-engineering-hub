# Scenario

A React and TypeScript product catalog page lags when the user types in the search box. A teammate proposes wrapping all components in `React.memo` and `useMemo`. The developer asks for a performance analysis.

# Input

Typing in the search box on the catalog page feels laggy with about 2,000 products. My teammate wants to add `React.memo` and `useMemo` everywhere. Can you work out what's happening and what we should actually do?

# Context

Code:

```tsx
function CatalogPage({ products }: { products: Product[] }) {
  const [query, setQuery] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search" />
      <SelectedSummary id={selectedId} />
      {products.map((p) => (
        <ProductRow
          key={p.id}
          product={p}
          style={{ padding: 8 }}
          onSelect={() => setSelectedId(p.id)}
        />
      ))}
    </>
  );
}
```

Facts:

- The `query` value is only used by the input in this component. Nothing in this component filters the list by it yet (filtering is planned for later).
- The React Profiler recording of typing one character shows: the commit took 48 ms. `CatalogPage` rendered once, and `ProductRow` rendered 2,000 times. The profiler reports "parent component rendered" as the reason for `ProductRow`.
- Each `ProductRow` render on its own is small (about 0.02 ms). `ProductRow` is a plain function component with no `memo`.
- On a 4x CPU throttled profile, the commit takes about 190 ms.
- The team's target is for typing to feel instant, meaning a keystroke should be handled well inside one frame.

# Expected Behavior

The response reads the profiler evidence: each keystroke changes `query` state in `CatalogPage`, which re-renders the page and all 2,000 rows although none of them depend on `query`. The reason reported is the parent rendering, and the rows receive new `style` and `onSelect` references each time. The total cost is the number of rows, not the cost of any one row. It presents hypotheses for ways to remove the work and evaluates them: isolating the search input's state so typing does not re-render the list (moving the state into a separate component or down the tree), memoizing the row component together with making its props stable (the inline `style` object and the `onSelect` function would otherwise defeat memoization), and, if lists this large remain a problem once filtering exists, reducing the number of rendered rows through pagination or virtualization. It explains that `React.memo` alone would not help here because the props change identity on every render, and that applying memoization everywhere adds complexity and comparison cost without evidence. It recommends re-measuring with the same profiler scenario, including the throttled profile, and defines the comparison. It does not promise specific timings.

# Important Checks

- The cause is derived from the profiler data (parent state change, 2,000 row renders).
- Unstable props (inline object and function) are identified as the reason memoization alone would not work.
- The option of moving state so the list does not re-render is considered.
- Blanket memoization is challenged with reasons.
- Future filtering and the need for virtualization or pagination are mentioned without being presented as the only answer.
- A measurement plan with the same scenario is given.
- No specific resulting timings are promised.
- The response works from the code and numbers given.

# Failure Conditions

- Agreeing to memoize every component and hook.
- Adding `React.memo` to `ProductRow` without fixing unstable props and claiming it solves the issue.
- Recommending a new state management library or a framework change.
- Blaming the browser or the size of the data without analysis.
- Promising a specific timing improvement.
- Ignoring the profiler data.
- Recommending debouncing the input as the only fix, when the real issue is unnecessary row renders.
- Inventing additional measurements.

# Notes

Debouncing is reasonable later, once filtering exists, as a way to reduce the frequency of expensive work. It should not be presented as a substitute for removing the unnecessary re-renders.
