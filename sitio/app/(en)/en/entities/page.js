import { obtenerEntidades } from "@/lib/datos";
import { t } from "@/lib/diccionario";
import IndiceEntidades from "@/components/IndiceEntidades";

export const metadata = {
  title: t("en").navEntidades,
  description: t("en").metaEntidades,
  alternates: { canonical: "/en/entities", languages: { "es-PE": "/entidades", en: "/en/entities" } },
};

export default function PaginaEntidadesEn() {
  return (
    <IndiceEntidades locale="en" entidades={obtenerEntidades()} hrefEntidad={(id) => `/en/entities/${id}`} />
  );
}
