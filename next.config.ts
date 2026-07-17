import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Avoid Turbopack production path on Vercel builders that mishandle modifyConfig
  // with Next 16.2.x (ERR_INVALID_ARG_TYPE during "Applying modifyConfig from Vercel").
  // Webpack remains the stable remote-build path until platform adapter is fixed.
}

export default nextConfig
