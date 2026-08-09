# TronixMesh.com Deployment

**Repo:** [BuildTronixAI/tronixmesh](https://github.com/BuildTronixAI/tronixmesh)  
**Site root:** `tronixmesh/` (Vercel Root Directory)  
**Live:** https://tronixmesh.com (already on Vercel)

## Status

| Check | Result |
| --- | --- |
| Production build | `npm run build` in `tronixmesh/` (Node 24) |
| Git remote | `origin/main` on `BuildTronixAI/tronixmesh` |
| Custom domain | `tronixmesh.com` → Vercel (`76.76.21.21`) |
| DNS NS | GoDaddy (`ns75`/`ns76.domaincontrol.com`) |

## Step 1: Verify build

```bash
cd tronixmesh
# Use Node 24.x (engines field)
npm ci
npm run build
```

Expected: `✓ Compiled successfully` and static routes for `/`, `/architecture`, `/constitution`, `/contact`, `/ip`.

## Step 2: Push to GitHub

```bash
git push origin main
```

If the Vercel project is linked to this GitHub repo (recommended), a production deploy starts automatically on push to `main`.

## Step 3: Deploy via Vercel dashboard (first-time / relink)

1. Open https://vercel.com/dashboard
2. **Add New → Project**, or open the existing TronixMesh project
3. Import `BuildTronixAI/tronixmesh`
4. Set **Root Directory** to `tronixmesh`
5. Framework: Next.js (from `vercel.json`)
6. Deploy

Do **not** add `VERCEL_TOKEN` as a Next.js runtime env var. That token is only for CLI / GitHub Actions authentication.

## Step 4: Custom domain

1. Vercel project → **Settings → Domains**
2. Add `tronixmesh.com` (and `www` if desired)
3. At GoDaddy/Cloudflare, keep A/CNAME records pointed at Vercel (or switch nameservers to Vercel if preferred)

Current public DNS already resolves `tronixmesh.com` to Vercel.

## Optional: GitHub Actions deploy

Workflow: `.github/workflows/deploy.yml`

Add these **GitHub Actions secrets** (repo → Settings → Secrets):

| Secret | Source |
| --- | --- |
| `VERCEL_TOKEN` | https://vercel.com/account/tokens |
| `VERCEL_ORG_ID` | Project → Settings → General (or `.vercel/project.json` after `vercel link`) |
| `VERCEL_PROJECT_ID` | Same |

Then push to `main` or run the workflow manually (**Actions → Deploy to Vercel → Run workflow**).

## Local development

```bash
cd tronixmesh
npm run dev
# http://localhost:3000
```

## Production locally

```bash
cd tronixmesh
npm run build
npm start
```

## What’s in the site package

- Next.js 16 (React 19, TypeScript, App Router)
- Tailwind CSS v4 (navy / cyan theme)
- Pages: home, architecture, constitution, IP, contact (+ `/api/contact`)
- `vercel.json` + community Vercel adapter for Next 16.2.x
