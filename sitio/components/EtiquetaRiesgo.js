import { t } from "@/lib/diccionario";

export default function EtiquetaRiesgo({ locale, valor }) {
  const d = t(locale);
  const clave = valor || "pendiente_de_clasificar";
  return <span className={`etiqueta riesgo-${clave}`}>{d.riesgos[clave] ?? clave}</span>;
}
