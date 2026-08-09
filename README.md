# TronixMesh

Governance architecture for autonomous systems — site + Phase B runtime docs/code.

**Live site:** https://tronixmesh.com  
**Next.js app:** `tronixmesh/` (Vercel project root)

## Quick start

```bash
cd tronixmesh
npm ci          # Node 24.x required
npm run dev     # http://localhost:3000
```

## Production build

```bash
cd tronixmesh
npm run build
npm start
```

## Deploy

See [docs/DEPLOY.md](docs/DEPLOY.md) for Vercel + domain + GitHub Actions steps.

Summary:

1. Build must pass in `tronixmesh/`
2. Push `main` (or import `BuildTronixAI/tronixmesh` in Vercel with root directory `tronixmesh`)
3. Domain `tronixmesh.com` is already pointed at Vercel

## Repo layout

```
tronixmesh/                 # Next.js marketing site (Vercel root)
├── app/                    # pages + API routes
├── components/
├── package.json
├── vercel.json
python/tronixmesh/          # Phase B runtime (envelope, handoff, provenance, …)
docs/                       # architecture + Phase B plan
.github/workflows/deploy.yml
```

## Phase B

Protocol/runtime work lives under `python/tronixmesh/` and `docs/phase-b/`. Soft-launch / production runtime deploy remains gated by the Phase B staged rollout — separate from the marketing site on Vercel.
