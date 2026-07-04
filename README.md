# abraxor-website

The Abraxor Ltd agency site — static HTML/CSS (no JS, no build step), served by nginx.
Live at https://preview.abraxor.com (cutover target: www.abraxor.com).

- `site/` — the site (index.html + styles.css)
- `Dockerfile` — nginx:alpine serving `site/`

Local preview:

```bash
cd site && python3 -m http.server 8095 --bind 0.0.0.0
```

Deploys via Dokploy (Hetzner) on push to `main`.
Accessibility target: WCAG AAA — semantic landmarks, skip link, 7:1 contrast, no motion.
