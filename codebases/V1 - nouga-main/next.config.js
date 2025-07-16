/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'utfs.io',
        port: ''
      },
      {
        protocol: 'https',
        hostname: 'api.slingacademy.com',
        port: ''
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: ''
      },
      {
        protocol: 'https',
        hostname: 'yzxtjaqwmhsazvnhqdwh.supabase.co',
        port: ''
      }
    ]
  },
  transpilePackages: ['geist'],
  experimental: {
    serverActions: {
      serverActions: true,
      bodySizeLimit: '100mb'
    }
  },
  allowedDevOrigins: ['*.ngrok-free.app']
};

module.exports = nextConfig;
