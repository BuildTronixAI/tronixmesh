/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Pin the community adapter so Vercel's remote NEXT_ADAPTER_PATH inject
  // (which crashes in modifyConfig on Next 16.2.x) is overridden.
  // This adapter has no modifyConfig; it only runs onBuildComplete.
  adapterPath: require.resolve("@next-community/adapter-vercel"),
};

module.exports = nextConfig;
