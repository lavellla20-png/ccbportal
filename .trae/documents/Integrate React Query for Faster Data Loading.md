## What React Query Does
- Caches API responses on the client with smart keys, avoiding repeated fetches
- De‑duplicates concurrent requests, retries on transient failures, and refetches in background
- Supports pagination/infinite scroll, optimistic updates, and stale‑while‑revalidate UX
- Reduces perceived latency on navigation (instant data from cache), improving LCP on data‑heavy pages

## Where It Helps in Your App
- News, Events, Announcements, Downloads lists: cache results by filters/page
- Detail views: keep previous data while refetching; prefetch likely next items
- Top‑level navigation: prefetch popular queries when a user hovers/opens menu

## Integration Plan
1. Install dependencies: `@tanstack/react-query` (and optional `@tanstack/react-query-devtools`)
2. Create a `QueryClient` with sensible defaults: `staleTime` (e.g., 60–120s), `cacheTime` (5–10m), exponential `retry` for GET
3. Wrap app with `QueryClientProvider` in `src/index.js` or `src/App.js`
4. Refactor `apiService` callers to hooks:
   - List endpoints: `useQuery(['news', page], () => apiService.getNews(page), { keepPreviousData: true })`
   - Mutations (admin actions): `useMutation` with optimistic update (optional for public UI)
5. Add prefetch on hover/focus for nav: `queryClient.prefetchQuery(['news', 1], ...)`
6. Configure refetching: disable `refetchOnWindowFocus` for stability; enable background refresh on interval for news (optional)
7. Instrumentation: expose query cache size/latency logs in dev; add React Query Devtools (dev only)

## Expected Impact
- Fewer network requests and faster repeat navigations across pages
- Smoother pagination with `keepPreviousData`
- Better resilience to intermittent network issues via retries

## Constraints & Complements
- React Query optimizes data fetching; it doesn’t compress assets or transform images—continue Cloudinary `f_auto,q_auto` and backend gzip/caching
- Works well with the existing `apiService`; we’ll adapt calls progressively without breaking behavior

If approved, I’ll implement the provider, convert key screens (News/Events/Announcements/Downloads) to React Query, add prefetching and sensible caching defaults, and ship with a small devtools toggle for troubleshooting.