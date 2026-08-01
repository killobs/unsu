/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: true,
  experimental: {
    // El sitio tiene dos root layouts (es/en), así que no hay un layout único
    // desde el que componer un 404 global: es el caso que la documentación de
    // Next señala para global-not-found.js.
    globalNotFound: true,
  },
};

export default nextConfig;
