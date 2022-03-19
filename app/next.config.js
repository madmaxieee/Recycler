/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: "/",
        destination: "/Dashboard",
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
