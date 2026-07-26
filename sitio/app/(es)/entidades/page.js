import { obtenerEntidades } from "@/lib/datos";
import IndiceEntidades from "@/components/IndiceEntidades";

export default function PaginaEntidadesEs() {
  return (
    <IndiceEntidades locale="es" entidades={obtenerEntidades()} hrefEntidad={(id) => `/entidades/${id}`} />
  );
}
