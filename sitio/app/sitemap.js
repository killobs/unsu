import { obtenerSistemas, obtenerEntidades } from "@/lib/datos";
import { URL_SITIO } from "@/lib/sitio";

// El sitemap sale de los mismos YAML que las páginas, así que no puede quedar
// desincronizado: si una ficha existe, su URL aparece aquí.
export const dynamic = "force-static";

export default function sitemap() {
  const sistemas = obtenerSistemas();
  const entidades = obtenerEntidades();
  const u = (ruta) => `${URL_SITIO}${ruta}`;

  const fijas = [
    { ruta: "/", prioridad: 1 },
    { ruta: "/en", prioridad: 1 },
    { ruta: "/entidades", prioridad: 0.8 },
    { ruta: "/en/entities", prioridad: 0.8 },
    { ruta: "/metodologia", prioridad: 0.7 },
    { ruta: "/en/methodology", prioridad: 0.7 },
  ].map(({ ruta, prioridad }) => ({ url: u(ruta), changeFrequency: "weekly", priority: prioridad }));

  // fecha_alta_registro es lo más cercano a "cuándo cambió esta ficha" que hay
  // en el dato; sin inventar una fecha de hoy que sería falsa.
  const fichasSistemas = sistemas.flatMap((s) => [
    { url: u(`/sistemas/${s.id}`), lastModified: s.fecha_alta_registro, priority: 0.6 },
    { url: u(`/en/systems/${s.id}`), lastModified: s.fecha_alta_registro, priority: 0.6 },
  ]);

  const fichasEntidades = entidades.flatMap((e) => [
    { url: u(`/entidades/${e.id}`), priority: 0.5 },
    { url: u(`/en/entities/${e.id}`), priority: 0.5 },
  ]);

  return [...fijas, ...fichasSistemas, ...fichasEntidades];
}
