import { URL_SITIO } from "@/lib/sitio";

// Todo el registro es público por decisión fundacional (docs/estrategia.md §1):
// no hay nada que ocultar a los rastreadores.
export const dynamic = "force-static";

export default function robots() {
  return {
    rules: [{ userAgent: "*", allow: "/" }],
    sitemap: `${URL_SITIO}/sitemap.xml`,
  };
}
