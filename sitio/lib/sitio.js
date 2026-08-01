// URL pública del sitio. Hace falta absoluta para el sitemap, las etiquetas
// Open Graph y los hreflang: una ruta relativa no sirve cuando el consumidor es
// un buscador o el previsualizador de un chat.
//
// Se lee del entorno para no tener que tocar código al mover de dominio. En
// Cloudflare Pages se define como variable de entorno del proyecto.
export const URL_SITIO = (process.env.SITIO_URL || "https://unsu.pages.dev").replace(/\/$/, "");

// Rutas equivalentes entre idiomas, para los alternates hreflang.
export const RUTAS = {
  es: { inicio: "/", entidades: "/entidades", metodologia: "/metodologia" },
  en: { inicio: "/en", entidades: "/en/entities", metodologia: "/en/methodology" },
};
