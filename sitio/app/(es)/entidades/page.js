import { obtenerEntidades } from "@/lib/datos";
import { t } from "@/lib/diccionario";
import IndiceEntidades from "@/components/IndiceEntidades";

export const metadata = {
  title: t("es").navEntidades,
  description: t("es").metaEntidades,
  alternates: { canonical: "/entidades", languages: { "es-PE": "/entidades", en: "/en/entities" } },
};

export default function PaginaEntidadesEs() {
  return (
    <IndiceEntidades locale="es" entidades={obtenerEntidades()} hrefEntidad={(id) => `/entidades/${id}`} />
  );
}
