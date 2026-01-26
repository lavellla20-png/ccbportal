## Frontend Performance
- Add `preconnect` to `res.cloudinary.com` and backend origin; `dns-prefetch` for third‑party hosts
- Inject `rel=preload` for critical CSS; defer non‑critical scripts; keep `GENERATE_SOURCEMAP=false`
- Code‑split routes (news, academics, admissions, downloads) via dynamic imports; tree‑shake and analyze bundle size
- Lazy‑load images and sections using `loading="lazy"` plus IntersectionObserver for older browsers
- Add skeleton/placeholder states to reduce perceived latency and layout shift
- Optimize font loading (`font-display: swap`) and self‑hosted fonts; avoid CLS

## Media (Cloudinary)
- Normalize all image URLs to include smart transformations: `f_auto,q_auto` with size caps (e.g., `c_limit,w_1200`), and responsive `srcset`
- Generate secure video URLs with `f_auto,q_auto:best,vc_auto` and poster images; prefer HLS for long videos
- Pre‑transform common sizes on upload (thumbnails, cards, banners) to avoid runtime transformations
- Use `cdn` URLs consistently; add `preconnect` to Cloudinary; cache forever via versioned URLs

## Backend API Throughput
- Enable `GZipMiddleware` and `ConditionalGetMiddleware` for compressed, cacheable JSON
- Return paginated results (e.g., news/events `?page=`) with sane defaults to reduce payload sizes
- Use `select_related/prefetch_related` where applicable; avoid N+1 queries
- Add indexes on hot query fields (`is_active`, `display_order`, dates)
- Add `cache_page(60)` on public read endpoints (news, announcements) with `stale-while-revalidate` headers

## Static Assets & Caching
- Keep WhiteNoise; enable Brotli + Gzip; set long‑lived `Cache-Control` for hashed static files
- Verify hashed filenames for CSS/JS; ensure immutable caching (`max-age=31536000, immutable`)
- Add ETag/Last‑Modified on API responses where feasible

## Network & Render Configuration
- Ensure HTTP/2 enabled by Render; confirm gzip/brotli at edge
- Increase backend instance RAM if needed; keep DB connection pooling; tune `gunicorn` workers based on CPU

## Database Tuning
- Create migrations to add indexes; analyze queries for `News`, `Announcements`, `Events`
- Paginate admin list pages; limit per‑page items

## Monitoring & Budgets
- Add `web-vitals` collection in frontend; log LCP/CLS/FID to console initially
- Track API latencies and cache hit rates; add basic health/status endpoint metrics

## Implementation Outline (approved → deliver)
1. Frontend: add `preconnect`/`preload`, lazy‑load helpers, route code‑splitting, skeletons; update image utilities to inject Cloudinary transforms and `srcset`
2. Backend: enable gzip + conditional GET; paginate public endpoints; add indexes & query prefetch; cache hot endpoints; set cache headers
3. Cloudinary: update upload and URL normalization to produce versioned, transformed URLs; add common size presets
4. Static: verify hashed asset caching and Brotli; confirm WhiteNoise settings
5. Validate: run Lighthouse and WebPageTest; compare before/after metrics; iterate

If you approve, I’ll implement these changes in both frontend and backend, verify with a production build, and provide a before/after performance report with concrete metrics (LCP, TTI, total bytes).