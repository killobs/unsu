import { t } from "@/lib/diccionario";

// Recorta en el límite de palabra: una descripción cortada a mitad de palabra se
// ve peor en el resultado de búsqueda que una un poco más corta.
function recortar(texto, max = 155) {
  const limpio = (texto || "").replace(/\s+/g, " ").trim();
  if (!limpio) return "";
  if (limpio.length <= max) return limpio;
  const corte = limpio.slice(0, max);
  const espacio = corte.lastIndexOf(" ");
  return `${espacio > 40 ? corte.slice(0, espacio) : corte}…`;
}

// El nombre del sistema va primero porque es lo distintivo: los títulos se
// truncan en los buscadores y el nombre de la entidad puede ocupar 70 caracteres.
export function metadatosSistema(locale, sistema, entidad) {
  const d = t(locale);
  if (!sistema) return {};
  const partes = [sistema.nombre, entidad?.nombre].filter(Boolean);
  return {
    title: partes.join(" — "),
    description: recortar(sistema.finalidad) || d.descripcionSitio,
  };
}

export function metadatosEntidad(locale, entidad, sistemas = []) {
  const d = t(locale);
  if (!entidad) return {};
  return {
    title: entidad.nombre,
    description: recortar(d.metaEntidad(entidad.nombre, sistemas.length)),
  };
}
