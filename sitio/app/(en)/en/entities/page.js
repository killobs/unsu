import { obtenerEntidades } from "@/lib/datos";
import IndiceEntidades from "@/components/IndiceEntidades";

export default function PaginaEntidadesEn() {
  return (
    <IndiceEntidades locale="en" entidades={obtenerEntidades()} hrefEntidad={(id) => `/en/entities/${id}`} />
  );
}
